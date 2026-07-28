#cookiecutter_incremental.md
# [Incremental Testing Pass: Mutant Killing & Test Augmentation]
The following test case `{case_name}` FAILED or needs augmentation in the execution sandbox while testing Cookiecutter.
File being tested: {test_file_path}

[Failed Code / Existing Code Base]:
{failing_code}

[Runtime Traceback / Mutation Logs]:
{error_trace}

<Reflection_Task>
1. Analyze the crash or the surviving mutants. Pay special attention to Cookiecutter's high reliance on disk I/O, file system templates, and Click CLI runner contexts.
2. STRICT AST CONSTRAINTS: You CANNOT use `mocker` fixture, and you CANNOT use `with pytest.raises(...)`. To assert exceptions (like `RepositoryNotFound` or `UnknownExtension`), you MUST use standard `try-except` blocks and assert the exception type (e.g., `except RepositoryNotFound: assert True`).

# === 框架特异性生命周期算子 (Cookiecutter Specific Constraints) ===
3. RULE FOR FILE SYSTEM ISOLATION (CRITICAL): Cookiecutter generates real directories on disk based on template rendering (e.g., `{{cookiecutter.project_slug}}`). Your test case MUST NOT use static or relative system paths. You MUST use pytest's `tmp_path` fixture or `tmpdir` factory for all file creations, directory searches, and test executions to prevent file collision or write permission failures.
4. RULE FOR JINJA2 CONTEXT WRAPPING: When testing functions inside `generate.py` (such as `render_and_create_dir` or `generate_files`), the template context dictionary MUST be wrapped under a top-level `"cookiecutter"` key (e.g., `context = {"cookiecutter": {"project_slug": "test_proj"}}`). Providing a flat dictionary will cause Jinja2 to throw an `UndefinedError` or `ContextDecodingException`.
5. RULE FOR CLICK PROMPT INTERCEPTION (CRITICAL): Functions inside `prompt.py` heavily invoke `click.prompt()` which waits for interactive user input. If executed directly, the test runner will HANG indefinitely. You MUST mock `click.prompt` using `unittest.mock.patch('click.prompt', return_value='mocked_user_value')` or wrap the test using `click.testing.CliRunner`.
6. RULE FOR REPOS & GIT CLONING ISOLATION: When targeting `vcs.py` (e.g., `clone` or `is_vcs_url`), you MUST NOT allow real Git clone network calls, as it causes `Authentication failed` or `Repository not found` in headless CI/CD environments. You MUST mock `subprocess.check_output` or short-circuit `vcs.clone` with a mocked local repository path string.
7. RULE FOR HOOKS AND SUBPROCESS SANDBOXING: Script hooks inside `hooks.py` (e.g., `pre_gen_project.py`) will trigger real OS process lifecycles via `subprocess.Popen`. Ensure that hook lookup targets point to dummy script paths created strictly inside your `tmp_path` context, and ensure file paths are converted using `os.fspath()` or `str()` where primitive strings are required.

# === 神谕强制注入规则 (The Oracle Constraints) ===
8. RULE FOR IMPORTS: Explicitly import necessary Cookiecutter modules and exceptions (e.g., `from cookiecutter.main import cookiecutter`, `from cookiecutter.exceptions import RepositoryNotFound`). Do not rely on global imports.
9. RULE FOR ASSERTIONS (CRITICAL): Your generated test MUST NOT be "execute-only". You MUST add strong `assert` statements at the end of the test to verify file existence (e.g., `assert (tmp_path / 'test_proj').exists()`) or configuration value matches.

### 🚨 [CRITICAL: COOKIECUTTER FRAMEWORK RULES - MUST FOLLOW] 🚨
当你修复 Cookiecutter 的主入口、模板生成器和核心钩子组件用例时，必须绝对遵守以下底层 API 规则：

1. **关于 `cookiecutter()` 函数返回值铁律**：
   成功调用 `cookiecutter(...)` 返回的永远是**生成的项目目录的原始路径字符串 (str)**，绝对禁止将其作为布尔值或元组进行不当解包与类型断言！
2. **关于 Hook 脚本的执行签名**：
   `hooks.run_hook(hook_name, project_dir, context)` 中，`hook_name` 只能是 `'pre_gen_project'` 或 `'post_gen_project'`。传入自定义名称会导致框架直接抛出 `ValueError`。
3. **关于配置文件字典的加载规则**：
   `config.get_user_config(config_file)` 期望接收一个合法的 YAML 文件路径。如果你传入一个非文件的字符串，它会引发 `InvalidConfiguration`。测试负向用例时请确保将其包裹在对应的 `try-except` 块内。

# === OUTPUT FORMAT ===
Output the refined `<Trace>`, `<Solve>`, `<Oracle_Design>`, and finally the EXACT corrected Python `<Code>`.
The code inside `<Code>` MUST start with exactly `def {case_name}(tmp_path):` or `def {case_name}():` to match the original failing signature.