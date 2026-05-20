import subprocess
import re
import os
import json
import requests
import ast
import subprocess
import re
import os
import json
import requests
import ast
import time  # <--- 新增这行，用于重试时的等待
import urllib3  # <-- 新增

# 强行关闭 SSL 警告，保持终端清爽
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# === 配置区 ===
# 确保你在终端里先执行了 export DEEPSEEK_API_KEY="sk-..."
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-5f2243ac76ae477eb7df8c093e2a1b06")
TEST_FILE_PATH = "test_output_cot_v8.2/test_cookiecutter_utils.py"

# ==========================================
# 1. AST 高级替换引擎
# ==========================================
class TestCaseReplacer(ast.NodeTransformer):
    def __init__(self, target_func_name, new_func_node):
        self.target_func_name = target_func_name
        self.new_func_node = new_func_node

    def visit_FunctionDef(self, node):
        if node.name == self.target_func_name:
            print(f"🌲 [AST] 成功定位到靶点函数: {self.target_func_name}，执行精准替换！")
            return self.new_func_node
        return node

def safe_replace_code_with_ast(file_path, target_func_name, new_code_string):
    with open(file_path, "r", encoding="utf-8") as f:
        original_code = f.read()
    
    tree = ast.parse(original_code)
    
    try:
        new_tree = ast.parse(new_code_string)
        # 提取出大模型生成的新函数节点
        new_func_node = new_tree.body[0]
        
        # 确保大模型没有改错名字
        if not isinstance(new_func_node, ast.FunctionDef) or new_func_node.name != target_func_name:
            # 强制改回正确的函数名，防止大模型乱起名
            new_func_node.name = target_func_name 
            
    except SyntaxError as e:
        print(f"❌ 大模型生成的代码存在语法错误，无法构建 AST，拦截替换: {e}")
        return False
    
    replacer = TestCaseReplacer(target_func_name, new_func_node)
    modified_tree = replacer.visit(tree)
    ast.fix_missing_locations(modified_tree)
    
    new_source = ast.unparse(modified_tree)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_source)
        
    return True

# ==========================================
# 2. 大模型反思接口 (Reflection Pass) - 坚如磐石版
# ==========================================
def call_deepseek_reflection(error_trace, failing_code, case_name):
    print(f"🧠 正在向 DeepSeek 发送 {case_name} 的反馈并请求纠偏...")
    
    prompt = f"""
    [Feedback Pass: Error Correction]
    The following test case `{case_name}` FAILED in the execution sandbox.
    
    [Failed Code]:
    {failing_code}
    
    [Runtime Traceback]:
    {error_trace}
    
    <Reflection_Task>:
    1. Analyze the crash.
    2. STRICT AST CONSTRAINTS: You CANNOT use `mocker` fixture, and you CANNOT use `with pytest.raises(...)`.
    3. RULE FOR OSError (stdin): If the error trace contains 'pytest: reading from stdin while output is captured', you MUST explicitly mock the click prompt like this:
       import unittest.mock
       patcher = unittest.mock.patch("cookiecutter.prompt.click.prompt", return_value=True)
       patcher.start()
       # execute target function here
       patcher.stop()
    4. RULE FOR ModuleNotFoundError: If the error says "No module named 'module_0'", DO NOT write `import module_0`. If you need the module, explicitly import the real target: `import cookiecutter.utils as module_0`.
    5. RULE FOR GARBAGE INPUTS: If the code crashed because of invalid input types (like negative integers for paths), DO NOT use try-except to swallow it! You MUST REWRITE the input variables to valid values (e.g., `"dummy_path"`).
    
    Output the refined `<Trace>`, `<Solve>`, `<Oracle_Design>`, and finally the EXACT corrected Python `<Code>`.
    The code inside `<Code>` MUST start with `def {case_name}():`
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    
    # 工业级重试机制：最多尝试 3 次
    
    max_api_retries = 3
    for attempt in range(max_api_retries):
        try:
            response = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload, timeout=30, verify=False)
            response.raise_for_status() 
            
            content = response.json()["choices"][0]["message"]["content"]
            
            # 策略1：优先寻找 <Code> 标签
            match = re.search(r'<Code>(.*?)</Code>', content, re.DOTALL | re.IGNORECASE)
            
            # 策略2：没找到就找 Markdown 块
            if not match:
                match = re.search(r'`{3}(?:python)?\s*(.*?)`{3}', content, re.DOTALL | re.IGNORECASE)
                
            if match:
                code = match.group(1).strip()
                # 强力清道夫：不管带不带 'python'，只要开头或结尾有反引号，统统抹除！
                code = re.sub(r'^`{3}(?:python)?\s*', '', code, flags=re.IGNORECASE)
                code = re.sub(r'`{3}\s*$', '', code)
                return code.strip()
            else:
                # 【关键修复】不要 return None！打印调试后，等待 3 秒继续重试！
                print(f"\n⚠️ [格式错误 - 尝试 {attempt + 1}/{max_api_retries}] 未能提取到纯代码，准备重试！\n原始回复片段：{content[:200]}...\n")
                if attempt < max_api_retries - 1:
                    import time
                    time.sleep(3)
                    continue  # 进入下一轮重试
                else:
                    print(f"❌ {case_name} 连续 3 次格式错误，跳过。")
                    return None
                    
        except requests.exceptions.RequestException as e:
            print(f"⚠️ 网络请求异常 (尝试 {attempt + 1}/{max_api_retries}): {e}")
            if attempt < max_api_retries - 1:
                import time
                time.sleep(3)
                continue
            else:
                print(f"❌ {case_name} 网络彻底失败，跳过。")
                return None
# ==========================================
# 3. 沙盒调度器 (Sandbox Orchestrator)
# ==========================================
def run_sandbox_and_feedback():
    print("\n🧪 启动沙盒环境执行测试...")
    result = subprocess.run(
        ["pytest", TEST_FILE_PATH, "-q", "--tb=short"], 
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print("🎉 沙盒测试 100% 完美通过！无需反思！")
        return True

    print("💥 捕获到测试失败！开始解析错误日志...")
    output = result.stdout + result.stderr
    
    # 解析出哪些用例挂了 (匹配 test_case_0, test_case_1 等)
    failed_cases = re.findall(r'FAILED.*?::(test_case_\d+)', output)
    failed_cases = list(set(failed_cases))
    
    print(f"🔍 找到 {len(failed_cases)} 个失败用例: {failed_cases}")
    
    with open(TEST_FILE_PATH, "r", encoding="utf-8") as f:
        test_code = f.read()

    for case_name in failed_cases:
        error_trace = output 
        
        # 提取失败用例的原始代码用于喂给大模型
        case_pattern = rf"(def {case_name}\(.*?)(?=^def test_case_|\Z)"
        match = re.search(case_pattern, test_code, re.DOTALL | re.MULTILINE)
        
        if match:
            failing_code = match.group(1)
            new_code = call_deepseek_reflection(error_trace, failing_code, case_name)
            
            if new_code:
                # 🚀 降维打击：调用 AST 安全替换引擎
                success = safe_replace_code_with_ast(TEST_FILE_PATH, case_name, new_code)
                if success:
                    print(f"✅ AST 手术完成，{case_name} 已安全更新！\n")
            else:
                print(f"⚠️ 无法从大模型获取 {case_name} 的合法代码。")
                
    print("💾 修复代码已写入，准备进入下一轮沙盒测试...")
    return False

# ==========================================
# 4. 主循环入口
# ==========================================
def main():
    if not DEEPSEEK_API_KEY:
        print("❌ 致命错误：未找到 DEEPSEEK_API_KEY 环境变量，请先执行 export DEEPSEEK_API_KEY=...")
        return
        
    if not os.path.exists(TEST_FILE_PATH):
        print(f"❌ 致命错误：找不到测试文件 {TEST_FILE_PATH}。请确保 Pynguin 已经生成了初始用例。")
        return

    max_retries = 3
    for i in range(max_retries):
        print(f"\n========== [第 {i+1} 轮迭代] ==========")
        success = run_sandbox_and_feedback()
        if success:
            print("\n🏆 变异得分攻坚战：防御阵地已全面构筑完成！所有用例完美通过！")
            break
    else:
        print("\n⚠️ 达到最大重试次数 (3次)，仍有未能修复的用例。请检查大模型输出或手动干预。")

if __name__ == "__main__":
    main()