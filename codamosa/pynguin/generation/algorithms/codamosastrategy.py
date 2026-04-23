#  This file is part of Pynguin and CodaMOSA.
#
#  SPDX-FileCopyrightText: Microsoft, 2019–2022 Pynguin Contributors
#
#  SPDX-License-Identifier: MIT
#
"""Provides the CodaMOSA test-generation strategy."""
from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, List, Set
import openai
from ordered_set import OrderedSet

import pynguin.configuration as config
import pynguin.ga.computations as ff
import pynguin.ga.testcasechromosome as tcc
import pynguin.testcase.testcase as tc
import pynguin.utils.statistics.statistics as stat
from pynguin.analyses.seeding import languagemodelseeding
from pynguin.ga.operators.ranking.crowdingdistance import (
    fast_epsilon_dominance_assignment,
)
from pynguin.generation.algorithms.abstractmosastrategy import AbstractMOSATestStrategy
from pynguin.generation.export.pytestexporter import PyTestExporter
from pynguin.generation.stoppingconditions.stoppingcondition import (
    MaxSearchTimeStoppingCondition,
)
from pynguin.testcase.statement import (
    ASTAssignStatement,
    ConstructorStatement,
    FunctionStatement,
    MethodStatement,
)
from pynguin.utils import randomness
from pynguin.utils.exceptions import ConstructionFailedException
from pynguin.utils.statistics.runtimevariable import RuntimeVariable

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    import pynguin.ga.testsuitechromosome as tsc


# pylint: disable=too-many-instance-attributes
class CodaMOSATestStrategy(AbstractMOSATestStrategy):
    """MOSA + Regular seeding by large language model."""

    _logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        self._num_codamosa_tests_added = 0
        self._num_mutant_codamosa_tests_added = 0
        self._num_added_tests_needed_expansion = 0
        self._num_added_tests_needed_uninterp = 0
        self._num_added_tests_needed_calls = 0
        self._plateau_len = config.configuration.codamosa.max_plateau_len

    def _log_num_codamosa_tests_added(self):
        scs = [
            sc
            for sc in self.stopping_conditions
            if isinstance(sc, MaxSearchTimeStoppingCondition)
        ]
        report_dir = config.configuration.statistics_output.report_dir
        if len(scs) > 0 and report_dir != "pynguin-report":
            search_time: MaxSearchTimeStoppingCondition = scs[0]
            with open(
                os.path.join(report_dir, "codamosa_timeline.csv"),
                "a+",
                encoding="UTF-8",
            ) as log_file:
                log_file.write(
                    f"{search_time.current_value()},{self._num_codamosa_tests_added}\n"
                )

    def _register_added_testcase(
        self, test_case: tc.TestCase, was_mutant: bool
    ) -> None:
        """Register that test_case was a test case generated during the targeted
        LLM generation phase, and any additional statistics we're tracking.

        Args:
            test_case: the test case to register
        """
        self._num_codamosa_tests_added += 1
        if was_mutant:
            self._num_mutant_codamosa_tests_added += 1
        exporter = PyTestExporter(wrap_code=False)
        logger.info(
            "New population test case:\n %s",
            exporter.export_sequences_to_str([test_case]),
        )
        if any(
            var in config.configuration.statistics_output.output_variables
            for var in [
                RuntimeVariable.LLMNeededExpansion,
                RuntimeVariable.LLMNeededUninterpretedCallsOnly,
                RuntimeVariable.LLMNeededUninterpreted,
            ]
        ):
            needed_expansion = False
            needed_calls = False
            needed_uninterp = False
            for stmt in test_case.statements:
                if isinstance(
                    stmt, (ConstructorStatement, FunctionStatement, MethodStatement)
                ):
                    # If this variable is tracked, must be using an expandable cluster.
                    was_backup = self.test_cluster.was_added_in_backup(  # type: ignore
                        stmt.accessible_object()
                    )
                    if was_backup:
                        needed_expansion = True
                        logger.info("Required test cluster expansion to parse.")
                elif isinstance(stmt, ASTAssignStatement):
                    if stmt.rhs_is_call():
                        needed_calls = True
                    else:
                        needed_uninterp = True

            self._num_added_tests_needed_expansion += 1 if needed_expansion else 0
            self._num_added_tests_needed_uninterp += (
                1 if (needed_calls or needed_uninterp) else 0
            )
            self._num_added_tests_needed_calls += (
                1 if (needed_calls and not needed_uninterp) else 0
            )

            stat.track_output_variable(
                RuntimeVariable.LLMNeededExpansion,
                self._num_added_tests_needed_expansion,
            )

            stat.track_output_variable(
                RuntimeVariable.LLMNeededUninterpreted,
                self._num_added_tests_needed_uninterp,
            )

            stat.track_output_variable(
                RuntimeVariable.LLMNeededUninterpretedCallsOnly,
                self._num_added_tests_needed_calls,
            )

        stat.track_output_variable(
            RuntimeVariable.LLMStageSavedTests, self._num_codamosa_tests_added
        )
        stat.track_output_variable(
            RuntimeVariable.LLMStageSavedMutants, self._num_mutant_codamosa_tests_added
        )

    def generate_tests(self) -> tsc.TestSuiteChromosome:
        self.before_search_start()
        self._number_of_goals = len(self._test_case_fitness_functions)
        stat.set_output_variable_for_runtime_variable(
            RuntimeVariable.Goals, self._number_of_goals
        )

        self._population = self._get_random_population()
        self._archive.update(self._population)

        # Calculate dominance ranks and crowding distance
        fronts = self._ranking_function.compute_ranking_assignment(
            self._population, self._archive.uncovered_goals  # type: ignore
        )
        for i in range(fronts.get_number_of_sub_fronts()):
            fast_epsilon_dominance_assignment(
                fronts.get_sub_front(i), self._archive.uncovered_goals  # type: ignore
            )

        self.before_first_search_iteration(
            self.create_test_suite(self._archive.solutions)
        )

        last_num_covered_goals = len(self._archive.covered_goals)
        its_without_update = 0
        while (
            self.resources_left()
            and self._number_of_goals - len(self._archive.covered_goals) != 0
        ):
            num_covered_goals = len(self._archive.covered_goals)
            if num_covered_goals == last_num_covered_goals:
                its_without_update += 1
            else:
                its_without_update = 0
            last_num_covered_goals = num_covered_goals
            if its_without_update > self._plateau_len:
                its_without_update = 0
                self.evolve_targeted(self.create_test_suite(self._archive.solutions))
            else:
                self.evolve()
            self.after_search_iteration(self.create_test_suite(self._archive.solutions))

        self.after_search_finish()
        return self.create_test_suite(
            self._archive.solutions
            if len(self._archive.solutions) > 0
            else self._get_best_individuals()
        )

    def evolve_targeted(self, test_suite):
        # 1. 提取染色体
        test_case_chromosomes = [
            cast(TestCaseChromosome, tcc)
            for tcc in test_suite.chromosomes
            if isinstance(tcc, TestCaseChromosome)
        ]

        # 【关键修复】：如果列表为空，说明当前没有可进化的种子，直接返回空列表，不要往下走
        if not test_case_chromosomes:
            # 这里的打印可以帮你确认：是不是 LLM 生成的种子没被正确加载
            print("\n[DEBUG] No chromosomes found for targeted evolution. Skipping...\n")
            return []

        new_offspring: list[TestCaseChromosome] = []

        while (
            len(new_offspring) < config.configuration.search_algorithm.population
            and self.resources_left()
        ):
            # 在执行 choice 之前再次检查长度（双重保险）
            if len(test_case_chromosomes) == 0:
                break
            
            try:
                # 报错就发生在这里，有了上面的 if 判定，这里就不会崩溃了
                offspring_1 = randomness.choice(test_case_chromosomes).clone()
                offspring_2 = randomness.choice(test_case_chromosomes).clone()
                
                if randomness.next_float() < config.configuration.search_algorithm.crossover_rate:
                    self._crossover.cross_over(offspring_1, offspring_2)

                for offspring in (offspring_1, offspring_2):
                    if len(new_offspring) < config.configuration.search_algorithm.population:
                        offspring.mutate()
                        new_offspring.append(offspring)
            except (IndexError, ValueError):
                # 万一运行中列表变动，捕获异常防止整个程序挂掉
                break

        return new_offspring
    
    def evolve(self) -> None:
        """Runs one evolution step."""
        offspring_population = self._breed_next_generation()
        self.evolve_common(offspring_population)

    def evolve_common(self, offspring_population) -> None:
        """The core logic to save offspring if they are interesting.

        Args:
            offspring_population: the offspring to try and save
        """

        # Create union of parents and offspring
        union: list[tcc.TestCaseChromosome] = []
        union.extend(self._population)
        union.extend(offspring_population)

        uncovered_goals: OrderedSet[
            ff.FitnessFunction
        ] = self._archive.uncovered_goals  # type: ignore

        # Ranking the union
        self._logger.debug("Union Size = %d", len(union))
        # Ranking the union using the best rank algorithm
        fronts = self._ranking_function.compute_ranking_assignment(
            union, uncovered_goals
        )

        remain = len(self._population)
        index = 0
        self._population.clear()

        # Obtain the next front
        front = fronts.get_sub_front(index)

        while remain > 0 and remain >= len(front) != 0:
            # Assign crowding distance to individuals
            fast_epsilon_dominance_assignment(front, uncovered_goals)
            # Add the individuals of this front
            self._population.extend(front)
            # Decrement remain
            remain -= len(front)
            # Obtain the next front
            index += 1
            if remain > 0:
                front = fronts.get_sub_front(index)

        # Remain is less than len(front[index]), insert only the best one
        if remain > 0 and len(front) != 0:
            fast_epsilon_dominance_assignment(front, uncovered_goals)
            front.sort(key=lambda t: t.distance, reverse=True)
            for k in range(remain):
                self._population.append(front[k])

        self._archive.update(self._population)
