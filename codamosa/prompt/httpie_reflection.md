[Feedback Pass: Error Correction & Oracle Generation]

The following test case `{case_name}` FAILED in the execution sandbox while testing HTTPie.

File being tested: {test_file_path}

[Failed Code]:

{failing_code}

[Runtime Traceback]:

{error_trace}

<Reflection_Task>:

1. Analyze the crash.

2. STRICT AST CONSTRAINTS: You CANNOT use `mocker` fixture, and you CANNOT use `with pytest.raises(...)`.

3. RULE FOR CLI OUTPUT CAPTURE (CRITICAL): Since the function signature MUST be strictly `def {case_name}():` with NO arguments, you CANNOT use pytest's `capsys` fixture. To capture and assert stdout/stderr (e.g., for --help or error messages), you MUST use standard Python `unittest.mock.patch('sys.stdout', new_callable=io.StringIO)` or `contextlib.redirect_stdout`.

4. RULE FOR NETWORKING & BLOCKING CALLS: HTTPie must not make real network calls. Use `responses` library or `unittest.mock.patch` to mock `requests.Session.send` if the error trace involves network connection or timeout.

5. RULE FOR IMPORTS: Explicitly import necessary HTTPie modules (e.g., `from httpie.cli.parser import ...`) and required stdlibs (`import io`, `import sys`, `from unittest.mock import patch`).

6. RULE FOR GARBAGE INPUTS: DO NOT use try-except to swallow invalid inputs! REWRITE the inputs to valid mock values (e.g., valid command strings, custom header tuples, or dummy environment dicts).



# === 神谕强制注入规则 (The Oracle Constraints) ===

7. RULE FOR ASSERTIONS (CRITICAL): Your generated test MUST NOT be "execute-only". You MUST add strong `assert` statements at the end of the test to verify the parser's return value, args, output, or state changes.

8. RULE FOR CLI EXITS & EXCEPTIONS: When HTTPie parser encounters invalid arguments or help flags, it calls `sys.exit()`, raising a `SystemExit`. You MUST catch it using try-except and ASSERT its code or type.

Example:

import sys

try:

# call httpie parser here

pass

except SystemExit as e:

assert e.code in [0, 1, 2] # Verify exit status

except Exception as e:

assert type(e).__name__ == "ExpectedErrorName"



Output the refined `<Trace>`, `<Solve>`, `<Oracle_Design>`, and finally the EXACT corrected Python `<Code>`.

The code inside `<Code>` MUST start with `def {case_name}():` 