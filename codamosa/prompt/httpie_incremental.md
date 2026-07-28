[Mutation-Aware Incremental Boosting: HTTPie Targeted DeepSeek-R1 Ultimate Attack v3.2]
The following Python test file needs incremental enhancement to kill surviving mutants discovered during mutation testing of HTTPie.

Target Test File Path: {test_file_path}
Target Module Name: {module_name}

[Current Test Code Baseline]:
{test_code}

[Surviving Mutants Mutation Report]:
{mutation_report}

<DeepSeek_R1_Incremental_Task>
1. Analyze the [Surviving Mutants Mutation Report]. Identify exact surviving logic (e.g., arg parsing groups, colorizer escape sequences, stream termination, session file synchronization).
2. Formulate an aggressive strategy to append new precise test cases or inject dense semantic assertions specifically designed to KILL these specific surviving mutants.

# === 🛡️ HTTPie 专属硬核靶向突防规则 (HTTPie-Specific Surface Attack) ===
3. RULE FOR TTY & COLORIZER INTROSPECTION: HTTPie heavily optimizes and branches based on whether stdout/stdin is a TTY terminal. To kill mutants inside formatting, colorizing (Pygments), and streams, you MUST mock TTY introspection:
   with patch('sys.stdout.isatty', return_value=True), patch('sys.stderr.isatty', return_value=True):
       pass

4. RULE FOR ENVIRONMENT OBJECT MANIPULATION: Instead of passing loose dicts, explicitly construct and inject HTTPie's native `Environment` object (`from httpie.context import Environment`) with forced properties like `colors=256`, `stdout_isatty=True`, and a controlled `config_dir` to bypass config file errors.

5. RULE FOR PLUGINS REGISTRY INTERACTION: If the target is `httpie.plugins.manager`, mutants inside registration, ordering, or filtering can only be killed by declaring a PURELY LOCAL dummy subclass inside the test file (e.g., define `class DummyPlugin: pass` directly in the code). Do not import non-existent plugin submodules.

6. RULE FOR SESSIONS & FILESYSTEM MOCKING: HTTPie's sessions module reads/writes JSON files under `~/.config/httpie/sessions`. To kill mutants inside cookie/header merging or session loading, you MUST use `unittest.mock.patch` to mock `pathlib.Path.open`, `Path.exists`, and `Path.mkdir`, OR patch `json.load`/`json.dump` to return valid session structures containing custom dicts of 'headers' and 'cookies'.

7. RULE FOR ARGPARSER DILEMMAS (TARGETED): To kill mutants inside `httpie.cli.argparser` and `definition.py`, pass highly conflicting and diverse arguments to `parser.parse_args()`. Test explicitly with combinations of `--form` mixed with JSON data, `--verbose` mixed with `--quiet`, invalid custom `--auth` strings, proxy strings, and missing URLs. Meticulously assert the internal attributes of the returned `Namespace` object (e.g., `assert args.form is True`, `assert args.json is False`).

8. RULE FOR FULL-BODY RESPONSES & DOWNLOADS: When mocking `requests.Response` for `httpie.client` or `downloads.py`, do NOT use a blank mock. You MUST supply complex headers (e.g., `{'Content-Type': 'application/json; charset=utf-8', 'Content-Encoding': 'gzip'}`), rich `raw` stream wrappers, and mock `iter_content` to return an actual generator/list of bytes (`mock_resp.iter_content.return_value = [b'chunk1', b'chunk2']`).

9. RULE FOR ANSI ESCAPE CODES & COLORIZER: To kill mutants in `output/formatters/colors.py` and `ui/palette.py`, your tests MUST capture stdout and assert the EXACT presence of ANSI escape codes (e.g., checking for `\x1b[` or specific Pygments style strings), rather than just asserting truthiness or length.

# === ⚙️ 物理沙箱与防爆舱严格约束 (Sandbox & Robustness Constraints) ===
10. STRICT AST CONSTRAINTS: You CANNOT use the `mocker` fixture, and you CANNOT use `with pytest.raises(...)`.
11. RULE FOR CLI OUTPUT CAPTURE: Since the function signature MUST be strictly `def test_case_xxx():` with NO arguments, you CANNOT use pytest's `capsys` fixture. Use `unittest.mock.patch('sys.stdout', new_callable=io.StringIO)` or `contextlib.redirect_stdout` to capture outputs.
12. RULE FOR NETWORKING: HTTPie must not make real network calls. Mock `requests.Session.send` or use `responses` library.

13. ANTI-DEADLOCK FILE MOCKING (CRITICAL): When mocking file objects via `patch('builtins.open')`, NEVER leave the mocked file object blank. A blank `MagicMock` method returns truthy values infinitely, causing infinite `while chunk := f.read()` loops. You MUST explicitly force file read methods to terminate by configuring EOF boundaries:
    `mock_file.read.return_value = b''`
    `mock_file.readline.return_value = ''`
    `mock_file.__iter__.return_value = iter([])`

14. MULTI-CASE AGGRESSIVE GENERATION (CRITICAL): DO NOT be concise. To kill maximum mutants, you MUST generate AT LEAST 8 to 12 distinct test functions (e.g., test_case_1 to test_case_12) per module. Each test function must target a completely different combination of conflicting arguments, environment states, or corrupted session payloads. Mass production of test cases is highly encouraged!

15. SELF-CONTAINED DEPENDENCY RULE (CRITICAL): Every single generated test function MUST be fully self-contained. If you use `io.StringIO` or `json`, you MUST import them inside or at the top of the file. If you reference `Environment`, `HTTPieArgumentParser`, or `requests.Response`, ensure they are correctly imported from their valid top-level paths. Never reference unimported variables or attributes to prevent early syntax/collection crashes.

16. ROBUST MOCK ATTRIBUTES: When mocking HTTPie internal objects (like Environment, Configuration, or Response), do not just mock one property. Always ensure basic dunder methods and common fields (e.g., `mock_obj.headers = {}`, `mock_obj.status_code = 200`, `mock_obj.__dict__ = {}`) are reasonably initialized to prevent early runtime AttributeError crashes during framework collection.