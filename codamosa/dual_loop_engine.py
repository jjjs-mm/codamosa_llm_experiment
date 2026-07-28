import subprocess
import re
import os
import time
import requests
import ast
import urllib3
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

# ==========================================
# 0. 全局配置：切换项目时，只需要改这里！
# ==========================================
CURRENT_PROJECT = "httpie"  


# ==========================================
# 1. AST 高级替换引擎 (搭载去毒管线、异步雷达与激进裁剪)
# ==========================================
class TestCaseReplacer(ast.NodeTransformer):
    def __init__(self, target_func_name, new_func_node):
        self.target_func_name = target_func_name
        self.new_func_node = new_func_node

    # 捕获普通的 def
    def visit_FunctionDef(self, node):
        if node.name == self.target_func_name:
            print(f"🌲 [AST] 成功定位靶点: {self.target_func_name}，执行【同步】替换！")
            return self.new_func_node
        return node
        
    # 🎯 核心修复 1：捕获大模型升维后的 async def
    def visit_AsyncFunctionDef(self, node):
        if node.name == self.target_func_name:
            print(f"🌲 [AST] 成功定位靶点: {self.target_func_name}，执行【异步】升维替换！")
            return self.new_func_node
        return node

def clean_llm_code_string(raw_code):
    if not raw_code: return ""
    match = re.search(r'\x60{3}(?:python)?\s*(.*?)\x60{3}', raw_code, re.DOTALL | re.IGNORECASE)
    code_block = match.group(1) if match else raw_code
        
    lines = code_block.split('\n')
    while lines and not lines[0].strip(): lines.pop(0)
    while lines and not lines[-1].strip(): lines.pop()
    if not lines: return ""
        
    first_line = lines[0]
    first_line_indent = len(first_line) - len(first_line.lstrip())
    if first_line_indent > 0:
        return '\n'.join([l[first_line_indent:] if l.startswith(' ' * first_line_indent) else l for l in lines])
    return '\n'.join(lines)

def safe_replace_code_with_ast(file_path, target_func_name, new_code_string):
    with open(file_path, "r", encoding="utf-8") as f:
        original_code = f.read()
    
    tree = ast.parse(original_code)
    sanitized_code = clean_llm_code_string(new_code_string)
    
    try:
        new_tree = ast.parse(sanitized_code)
    except SyntaxError as e:
        # 🎯 核心修复 2：激进裁剪模式。如果遇到自然语言废话，强行从装饰器或 def 截断！
        print(f"⚠️ 捕获到杂质语法错误，启动激进裁剪引擎...")
        pattern = rf'((?:^[ \t]*@[^\n]+\n)*^[ \t]*(?:async\s+)?def\s+{target_func_name}\s*\(.*\):.*)'
        match = re.search(pattern, sanitized_code, re.DOTALL | re.MULTILINE)
        if match:
            try:
                new_tree = ast.parse(match.group(1))
                print("✅ 激进裁剪成功！已剥离自然语言，恢复纯净 AST。")
            except SyntaxError:
                print("❌ 激进裁剪后仍存在乱码，放弃替换。")
                return False
        else:
            print(f"❌ 无法从文本中提纯出函数，拦截替换: {e}")
            return False

    # 🎯 核心修复 3：让雷达同时识别普通函数和异步函数！
    new_func_node = None
    for node in new_tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            new_func_node = node
            break
            
    if not new_func_node:
        print(f"❌ 大模型返回的代码中未找到有效的函数结构，拦截替换！")
        return False
        
    new_func_node.name = target_func_name 
    
    replacer = TestCaseReplacer(target_func_name, new_func_node)
    modified_tree = replacer.visit(tree)
    ast.fix_missing_locations(modified_tree)
    new_source = ast.unparse(modified_tree)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_source)
    return True

# ==========================================
# 2. 大模型反思接口
# ==========================================
def call_deepseek_reflection(error_trace, failing_code, case_name, test_file_path):
    print(f"🧠 正在向 DeepSeek 发送 {case_name} (文件: {test_file_path}) 的反馈...")
    prompt_path = f"prompt/{CURRENT_PROJECT}_reflection.md"
    
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"❌ 找不到当前项目的 Prompt 模板: {prompt_path}")
        
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    prompt = prompt_template.format(case_name=case_name, test_file_path=test_file_path, failing_code=failing_code, error_trace=error_trace)
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    payload = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
    
    max_api_retries = 3
    for attempt in range(max_api_retries):
        try:
            response = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload, timeout=30, verify=False)
            response.raise_for_status() 
            content = response.json()["choices"][0]["message"]["content"]
            
            match = re.search(r'<Code>(.*?)</Code>', content, re.DOTALL | re.IGNORECASE)
            if not match:
                match = re.search(r'\x60{3}(?:python)?\s*(.*?)\x60{3}', content, re.DOTALL | re.IGNORECASE)
                
            if match:
                code = match.group(1).strip()
                code = re.sub(r'^\x60{3}(?:python)?\s*', '', code, flags=re.IGNORECASE)
                code = re.sub(r'\x60{3}\s*$', '', code)
                return code.strip()
            else:
                if attempt < max_api_retries - 1:
                    time.sleep(3)
                    continue
                return None
        except requests.exceptions.RequestException:
            if attempt < max_api_retries - 1:
                time.sleep(3)
                continue
            return None

# ==========================================
# 3. 沙盒调度器
# ==========================================
def run_sandbox_and_feedback(test_file_path, force_rewrite=False):
    print(f"\n🧪 启动沙盒环境执行测试: {test_file_path}")
    result = subprocess.run(["pytest", test_file_path, "-q", "--tb=short"], capture_output=True, text=True)
    
    if result.returncode == 0 and not force_rewrite:
        print("🎉 沙盒测试 100% 完美通过！")
        return True

    with open(test_file_path, "r", encoding="utf-8") as f:
        test_code = f.read()

    if force_rewrite:
        print("🔥 [方案B] 激活强制重构模式：无视绿灯，强行抓取所有测试用例交由 V3 升维！")
        # 统一使用兼容所有英文、数字、下划线的正则，并且匹配 def 开头
        failed_cases = list(set(re.findall(r'def (test_[a-zA-Z0-9_]+)', test_code)))
        output = "强制重构触发：请结合算子库将该同步用例重构为深层异步生命周期测试。"
    else:
        print("💥 捕获到测试失败！开始解析...")
        output = result.stdout + result.stderr
        # 完美！这个正则能接住 Pytest 所有的报错信息
        failed_cases = list(set(re.findall(r"::(test_[a-zA-Z0-9_]+)", output)))
        
    print(f"🔍 找到 {len(failed_cases)} 个目标用例进行大模型交互: {failed_cases}")
    
    for case_name in failed_cases:
        case_pattern = rf"((?:async\s+)?def {case_name}\(.*?)(?=^(?:async\s+)?def test_|\Z)"
        match = re.search(case_pattern, test_code, re.DOTALL | re.MULTILINE)
        if match:
            new_code = call_deepseek_reflection(output, match.group(1), case_name, test_file_path)
            if new_code:
                safe_replace_code_with_ast(test_file_path, case_name, new_code)
                
    return False

# ==========================================
# 4. 主入口
# ==========================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-file", required=True)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--force-rewrite", action="store_true")
    args = parser.parse_args()

    if not DEEPSEEK_API_KEY or not os.path.exists(args.test_file):
        print("❌ 致命错误：API 密钥未配置或文件不存在。")
        return

    current_force = args.force_rewrite
    for i in range(args.max_retries):
        print(f"\n========== [第 {i+1} 轮迭代 | 文件: {args.test_file}] ==========")
        if run_sandbox_and_feedback(args.test_file, current_force):
            print("\n🏆 该文件防御阵地已全面构筑完成！\n")
            break
        current_force = False 
    else:
        print(f"\n⚠️ 达到最大重试次数，仍有未能修复的用例。")

if __name__ == "__main__":
    main()