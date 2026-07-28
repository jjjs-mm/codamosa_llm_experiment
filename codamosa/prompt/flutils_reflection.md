[Feedback Pass: Error Correction & Oracle Generation]
The following test case `{case_name}` FAILED in the execution sandbox while testing flutils.
File being tested: {test_file_path}

[Failed Code]:
{failing_code}

[Runtime Traceback]:
{error_trace}

<Reflection_Task>:
1. Analyze the crash. Pay special attention to flutils's high reliance on system calls (`subprocess`), OS user/group permissions, path manipulations (`pathutils`), and dynamic module imports.
2. STRICT AST CONSTRAINTS: You CANNOT use `mocker` fixture, and you CANNOT use `with pytest.raises(...)`. To assert exceptions (like `FileNotFoundError`, `PermissionError`, or `TypeError`), you MUST use standard `try-except` blocks and assert the exception type (e.g., `except TypeError: assert True`).

# === 框架特异性生命周期算子 (flutils Specific Constraints) ===
3. RULE FOR FILE SYSTEM & PERMISSION ISOLATION (CRITICAL): Functions inside `pathutils.py` (e.g., `chmod`, `chown`, `directory`) interact directly with POSIX file permissions. Your test case MUST NOT attempt to change permissions or ownership on system folders (`/root`, `/etc`). You MUST create temporary mock files/folders using pytest's `tmp_path` fixture.
4. RULE FOR SUBPROCESS & COMMAND EXECUTION (CRITICAL): When testing `cmdutils.run_script_for_annotated_posix_path`, it executes actual shell scripts via `subprocess`. You MUST ensure the target script exists inside `tmp_path`, is marked executable (`os.chmod(..., 0o755)`), or mock `subprocess.run`/`Popen` to prevent command execution lockup in headless CI/CD containers.
5. RULE FOR DYNAMIC CODECS REGISTRATION: Testing `codecs` (e.g., `b64` or `raw_utf8_escape`) modifies Python's global `codecs` registry. Ensure register functions are invoked safely without corrupting default system string encodings.
6. RULE FOR PACKAGE VERSION PARSING: When testing `packages.find_executable` or version comparison functions, ensure you handle deprecation warnings gracefully (such as `distutils.version.StrictVersion`) and pass valid string arguments.

# === 神谕强制注入规则 (The Oracle Constraints) ===
7. RULE FOR IMPORTS: Explicitly import necessary flutils modules and exceptions (e.g., `from flutils.cmdutils import run_script_for_annotated_posix_path`, `from flutils.pathutils import exists`). Do not rely on global or wildcard imports.
8. RULE FOR ASSERTIONS (CRITICAL): Your generated test MUST NOT be "execute-only". You MUST add strong `assert` statements at the end of the test to verify return tuple structures, string outputs, or state modifications.

### 🚨 [CRITICAL: FLUTILS FRAMEWORK RULES - MUST FOLLOW] 🚨
当你修复 flutils 的系统工具、路径与代码包组件用例时，必须绝对遵守以下底层 API 规则：

1. **关于 `cmdutils` 返回值解包铁律**：
   调用 `run_script_for_annotated_posix_path(...)` 返回的是一个 `CompletedProcess` 或特定的命名元组 `(stdout, stderr)`，必须对 `stdout` 和 `returncode` 进行严格类型匹配与断言。
2. **关于 `pathutils` 路径转换**：
   所有接收 Path-like 参数的函数期望 `AnsiPath`、`Path` 或 `str`。传递 `None` 或非法类型会直接抛出 `TypeError`，必须使用 `try-except TypeError` 进行捕获验证。
# === OUTPUT FORMAT ===
Output the refined `<Trace>`, `<Solve>`, `<Oracle_Design>`, and finally the EXACT corrected Python `<Code>`.
The code inside `<Code>` MUST start with exactly `def {case_name}(tmp_path):` or `def {case_name}():` to match the original failing signature.
