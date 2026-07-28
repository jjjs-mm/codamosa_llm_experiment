# [Mutation-Aware Incremental Boosting: flutils Targeted DeepSeek-R1 Ultimate Attack v3.2]
The following Python test file needs incremental enhancement to kill surviving mutants discovered during mutation testing of flutils.

Target Test File Path: {test_file_path}
Target Module Name: {module_name}

[Current Test Code Baseline]:
{test_code}

[Surviving Mutants Mutation Report]:
{mutation_report}

<DeepSeek_R1_Incremental_Task>
1. Analyze the [Surviving Mutants Mutation Report]. Identify exact surviving logic (e.g., path permission boundaries, POSIX user/group resolution, nested tuple conversions, string formatting, byte encoding escapes).
2. Formulate an aggressive strategy to append new precise test cases or inject dense semantic assertions specifically designed to KILL these specific surviving mutants.

# === 🛡️ flutils 专属硬核靶向突防规则 (flutils-Specific Surface Attack) ===
3. RULE FOR POSIX PERMISSIONS & CHMOD/CHOWN: `flutils.pathutils` heavily interacts with OS permission bits (e.g., `0o777`, `0o644`). To kill mutants inside permission calculations or ownership checks without needing root privileges, you MUST mock `os.chmod`, `os.chown`, `pwd.getpwnam`, and `grp.getgrnam` using `unittest.mock.patch`:
   with patch('os.chmod') as mock_chmod, patch('os.chown') as mock_chown:
       pass

4. RULE FOR SUBPROCESS & COMMAND EXECUTION (DEADLOCK PREVENTION): When targeting `flutils.cmdutils` (e.g., `run_script_for_annotated_posix_path`), it executes actual shell scripts. To kill mutants inside return code evaluation or stdout/stderr parsing, NEVER allow real external processes to block. Mock `subprocess.run` or `subprocess.Popen` and explicitly supply completed process mocks with distinct `stdout`, `stderr`, and `returncode` values.

5. RULE FOR DYNAMIC CODECS REGISTRATION: To kill mutants inside `flutils.codecs` (such as `b64` or `raw_utf8_escape`), test explicitly with non-ASCII Unicode strings, empty byte strings, corrupted base64 payloads, and invalid surrogate pairs. Meticulously assert the exact returned `(bytes, int)` or `(str, int)` tuples mandated by Python's `codecs` API.

6. RULE FOR NAMEDTUPLE & OBJUTILS CONVERSIONS: To kill mutants inside `flutils.namedtupleutils` and `objutils` (e.g., `to_namedtuple`, `has_any_attrs`), pass deeply nested dictionaries containing lists, sets, generators, and custom class instances. Explicitly assert the exact attribute access syntax on the generated NamedTuple (e.g., `assert res.a.b[0] == 1`), rather than just checking truthiness.

7. RULE FOR PACKAGE VERSION PARSING (STRICT): To kill mutants inside `flutils.packages` (e.g., `find_executable` or version comparison), pass edge-case version strings (e.g., `'1.0.0a1'`, `'0.0.0'`, `'99.99.99'`). Do not let deprecation warnings from `StrictVersion` break collection; wrap edge-case assertions tightly.

# === ⚙️ 物理沙箱与防爆舱严格约束 (Sandbox & Robustness Constraints) ===
8. STRICT AST CONSTRAINTS: You CANNOT use the `mocker` fixture, and you CANNOT use `with pytest.raises(...)`. To assert exceptions (like `FileNotFoundError`, `PermissionError`, or `TypeError`), you MUST use standard `try-except` blocks and assert the exception type (e.g., `except TypeError: assert True`).

9. RULE FOR CLI/STDOUT OUTPUT CAPTURE: Since the function signature MUST be strictly `def test_case_xxx():` with NO arguments, you CANNOT use pytest's `capsys` or `tmp_path` fixtures directly in signature. Use `tempfile.TemporaryDirectory()` for filesystem isolation, and `contextlib.redirect_stdout` or `patch('sys.stdout', new_callable=io.StringIO)` to capture outputs.

10. ANTI-DEADLOCK FILE & STREAM MOCKING (CRITICAL): When mocking file reads or stream iterators via `patch('builtins.open')` or `io.BytesIO`, NEVER leave the mocked object blank. A blank `MagicMock` method returns truthy values infinitely, causing infinite loops. You MUST explicitly force EOF boundaries:
    `mock_file.read.return_value = b''`
    `mock_file.readline.return_value = ''`
    `mock_file.__iter__.return_value = iter([])`

11. MULTI-CASE AGGRESSIVE GENERATION (CRITICAL): DO NOT be concise. To kill maximum mutants, you MUST generate AT LEAST 8 to 12 distinct test functions (e.g., test_case_1 to test_case_12) per module. Each test function must target a completely different combination of conflicting arguments, edge-case types, or boundary conditions. Mass production of test cases is highly encouraged!

12. SELF-CONTAINED DEPENDENCY RULE (CRITICAL): Every single generated test function MUST be fully self-contained. If you use `io.StringIO`, `tempfile`, or `patch`, you MUST import them inside or at the top of the file. Ensure target functions (e.g., `from flutils.pathutils import normalize_path`) are correctly imported from their valid top-level modules. Never reference unimported variables or attributes to prevent early syntax/collection crashes.

13. ROBUST MOCK ATTRIBUTES: When mocking flutils internal structures or OS objects, do not just mock one property. Always ensure basic dunder methods and common fields are reasonably initialized to prevent early runtime `AttributeError` crashes during framework collection.

# === OUTPUT FORMAT ===
Output the refined `<Trace>`, `<Solve>`, `<Oracle_Design>`, and finally the EXACT appended/enhanced Python `<Code>`.
The code inside `<Code>` MUST contain valid Python test functions starting with `def test_case_xxx():`.