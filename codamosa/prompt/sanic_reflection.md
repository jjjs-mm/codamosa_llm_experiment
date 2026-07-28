[Feedback Pass: Error Correction & Oracle Generation]
The following test case `{case_name}` FAILED in the execution sandbox while testing Sanic.
File being tested: {test_file_path}

[Failed Code]:
{failing_code}

[Runtime Traceback]:
{error_trace}

<Reflection_Task>:
1. Analyze the crash. Pay special attention to Sanic's heavy reliance on asyncio Event Loops, asynchronous request/response lifecycles, and Blueprint routing trees.
2. STRICT AST CONSTRAINTS: You CANNOT use `mocker` fixture, and you CANNOT use `with pytest.raises(...)`. To assert exceptions (like `SanicException`, `NotFound`, or `ServerError`), you MUST use standard `try-except` blocks and assert the exception type (e.g., `except SanicException: assert True`).

# === 🛡️ Sanic 专属框架生命周期算子 (Sanic Specific Constraints) ===
3. RULE FOR ASYNCIO EVENT LOOP SANDBOXING (CRITICAL): Sanic async handlers and protocols require an active running asyncio event loop. Your test cases MUST NOT invoke `asyncio.get_event_loop()` without handling loop initialization. Use `asyncio.run(...)` or wrap async calls inside `loop.run_until_complete(...)` using `asyncio.new_event_loop()`.
4. RULE FOR SANIC APP & TEST CLIENT ISOLATION: When testing `sanic.app` or `blueprints.py`, NEVER create un-isolated global `Sanic("name")` instances, as duplicate app names throw `SanicException("Called Sanic('name') more than once...")`. You MUST generate unique app names dynamically (e.g., `Sanic(f"test_app_{uuid.uuid4().hex}")`).
5. RULE FOR MOCKING REQUEST & RESPONSE OBJECTS: When testing `sanic.router`, `headers.py`, or `handlers`, do NOT pass empty mocks as Request objects. Ensure `request.headers`, `request.args`, `request.json`, and `request.stream` are properly initialized dictionary or mock attributes to avoid early `AttributeError` crashes.
6. RULE FOR WEBSOCKET & HTTP PROTOCOL MOCKING: When testing `sanic.server.protocols.http_protocol` or websocket handlers, mock the underlying `asyncio.Transport` and `asyncio.Protocol` objects. NEVER allow real TCP socket binding or network port listening (`app.run(port=8000)`) in headless test runners!

# === 神谕强制注入规则 (The Oracle Constraints) ===
7. RULE FOR IMPORTS: Explicitly import necessary Sanic modules and exceptions (e.g., `from sanic import Sanic, Blueprint`, `from sanic.exceptions import NotFound, ServerError`). Do not rely on global or wildcard imports.
8. RULE FOR ASSERTIONS (CRITICAL): Your generated test MUST NOT be "execute-only". You MUST add strong `assert` statements at the end of the test to verify status codes (e.g., `assert response.status == 200`), body byte strings, or route registration signatures.

### 🚨 [CRITICAL: SANIC FRAMEWORK RULES - MUST FOLLOW] 🚨
当你修复 Sanic 的路由树、蓝图机制和网络协议组件用例时，必须绝对遵守以下底层 API 规则：

1. **关于 Blueprint 注册铁律**：
   调用 `app.blueprint(bp)` 时，若蓝图重复注册或路由前缀冲突，Sanic 会抛出 `ValueError` 或 `SanicException`。测试负向用例时请务必包裹在 `try-except` 块中。
2. **关于 HTTP 响应类型**：
   `sanic.response.json(...)` 或 `text(...)` 返回的是 `HTTPResponse` 对象，判断内容时必须断言 `response.body` (bytes) 或 `response.status` (int)，切勿将响应对象当作字典解包！

# === OUTPUT FORMAT ===
Output the refined `<Trace>`, `<Solve>`, `<Oracle_Design>`, and finally the EXACT corrected Python `<Code>`.
The code inside `<Code>` MUST start with exactly `def {case_name}(tmp_path):` or `def {case_name}():` to match the original failing signature.
