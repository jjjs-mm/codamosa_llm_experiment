[Feedback Pass: Error Correction & Oracle Generation]
    The following test case `{case_name}` FAILED in the execution sandbox.
    File being tested: {test_file_path}
    
    [Failed Code]:
    {failing_code}
    
    [Runtime Traceback]:
    {error_trace}
    
    <Reflection_Task>:
    1. Analyze the crash. 
    2. STRICT AST CONSTRAINTS: You CANNOT use `mocker` fixture, and you CANNOT use `with pytest.raises(...)`.
    3. RULE FOR BLOCKING CALLS: If the error trace shows 'reading from stdin' or network timeouts, explicitly mock the underlying blocking function using `unittest.mock.patch`.
    4. RULE FOR IMPORTS: Explicitly import the target module based on the test file path.
    5. RULE FOR GARBAGE INPUTS: DO NOT use try-except to swallow invalid inputs! REWRITE the inputs to valid mock values (e.g., valid strings, dummy dicts, or create real temporary directories using `tempfile`).
    
    # === 新增：神谕强制注入规则 (The Oracle Constraints) ===
    6. RULE FOR ASSERTIONS (CRITICAL): Your generated test MUST NOT be "execute-only". You MUST add strong `assert` statements at the end of the test to verify the function's return value, output, or state changes. For example: `assert result == expected_value` or `assert result is not None`.
    7. RULE FOR EXCEPTIONS: If the function is expected to raise an exception, you must catch it and ASSERT its type or message. 
       Example:
       try:
           target_function(invalid_input)
           assert False, "Expected exception was not raised!"
       except Exception as e:
           assert type(e).__name__ == "ExpectedErrorName"

    Output the refined `<Trace>`, `<Solve>`, `<Oracle_Design>`, and finally the EXACT corrected Python `<Code>`.
    The code inside `<Code>` MUST start with `def {case_name}():`