import os
import re
import ast
import shutil
import argparse
from openai import OpenAI

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "") 
BASE_URL = "https://api.deepseek.com" # 如果你用的代理平台，请改成代理的URL
# ⚠️ 如果你是官方API，这里填 "deepseek-reasoner"
# ⚠️ 如果你是代理平台(如SiliconFlow)，请查阅文档填入准确的 R1 名字，例如 "deepseek-ai/DeepSeek-R1"
MODEL_NAME = "deepseek-reasoner"

# ==========================================
# 0. 全局游标：如果纯Python运行，默认用这个
# ==========================================
CURRENT_PROJECT = "flutils"  

# ==========================================
# 1. 项目大一统配置字典 (引入 Stage2 输入与 Stage3 输出的双轨制)
# ==========================================
PROJECT_CONFIGS = {
    "httpie": {
        "stage2_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_httpie/stage2_v3",
        "stage3_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_httpie/stage3_cascade",
        "src_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/codamosa/replication/test-apps/httpie",
        "prompt_file": "prompt/httpie_incremental.md",
        "mutmut_report": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_httpie/stage2_v3/mutation_report_stage2.txt",
        "modules": {
            "test_httpie_core.py": "httpie/core.py",
            "test_httpie_client.py": "httpie/client.py",
            "test_httpie_context.py": "httpie/context.py",
            "test_httpie_models.py": "httpie/models.py",
            "test_httpie_cli_argparser.py": "httpie/cli/argparser.py",
            "test_httpie_cli_requestitems.py": "httpie/cli/requestitems.py",
            "test_httpie_sessions.py": "httpie/sessions.py",
            "test_httpie_plugins_manager.py": "httpie/plugins/manager.py"
        }
    },
    "sanic": {
        "stage2_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_sanic/stage2_v3",
        "stage3_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_sanic/stage3_cascade", 
        "src_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/sanic_src",
        "prompt_file": "prompt/sanic_incremental.md",
        "modules": {
            #"sanic_router": "sanic/router.py",
            #"sanic_blueprints": "sanic/blueprints.py",
            #"sanic_config": "sanic/config.py",        # 🎯 当前主战场
            #"sanic_exceptions": "sanic/exceptions.py",
            #"sanic_headers": "sanic/headers.py"
            "http_protocol": "sanic/server/protocols/http_protocol.py"
        }
    },
    "flutils": {
        "src_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/flutils_src",
        "mutmut_report": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_flutils/mutation_report_stage2.txt",
        "prompt_file": "/root/codamosa_llm_experiment-feat-batch-experiment/prompt/flutils_incremental.md",
        "stage2_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_flutils/stage2_v3",
        "stage3_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_flutils/stage3_cascade",
        "modules": {
            "test_flutils_cmdutils.py": "flutils/cmdutils.py",
            "test_flutils_codecs.py": "flutils/codecs/__init__.py",
            "test_flutils_txtutils.py": "flutils/txtutils.py",
            "test_flutils_decorators.py": "flutils/decorators.py",
            "test_flutils_validators.py": "flutils/validators.py",
            "test_flutils_packages.py": "flutils/packages.py",
            "test_flutils_moduleutils.py": "flutils/moduleutils.py"
        }
    },
    "cookiecutter": {
        "src_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/cookiecutter_src",
        "mutmut_report": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_cookiecutter/mutation_report_stage2.txt",
        "prompt_file": "/root/codamosa_llm_experiment-feat-batch-experiment/prompt/cookiecutter_incremental.md",
        "stage2_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_cookiecutter/stage2_v3",
        "stage3_dir": "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_cookiecutter/stage3_cascade",
        "modules": {
            "test_cookiecutter_main.py": "cookiecutter/main.py",
            "test_cookiecutter_generate.py": "cookiecutter/generate.py",
            "test_cookiecutter_prompt.py": "cookiecutter/prompt.py",
            "test_cookiecutter_config.py": "cookiecutter/config.py",
            "test_cookiecutter_vcs.py": "cookiecutter/vcs.py",
            "test_cookiecutter_hooks.py": "cookiecutter/hooks.py"
        }
    }
}

# 变异静态日志路径
# 变异静态日志路径 (指向咱们刚生成的满血版 Diff 战报)
REPORT_FILE = "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_flutils/mutation_report_stage2.txt"
LOG_FILE = "/root/codamosa_llm_experiment-feat-batch-experiment/codamosa/mutmut_progress.log"

# ==========================================
# 2. 幸存变异体静态解析器 (✨ 升级版：智能区块解析 + 兜底解析)
# ==========================================
def extract_surviving_mutants(src_rel_path, custom_report=None):
    filename = os.path.basename(src_rel_path)  # 例如: "config.py"
    survivors = []
    
    # 优先找当前项目的专属 report，如果没有则使用全局的兜底
    target_files = [custom_report, REPORT_FILE, LOG_FILE] if custom_report else [REPORT_FILE, LOG_FILE]
    
    for file_path in target_files:
        if file_path and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # ✨ 策略 A：针对标准 mutmut results 的区块级深度解析
            if filename in content:
                lines = content.splitlines()
                in_target_file_block = False
                current_status = "Unknown Status"
                
                for line in lines:
                    if "Survived" in line or "🙁" in line or "Timeout" in line or "⏰" in line:
                        current_status = line.strip()
                    
                    if "----" in line and filename in line:
                        in_target_file_block = True
                        survivors.append(f"[{current_status}]")
                        survivors.append(line.strip())
                        continue
                    
                    if in_target_file_block and "----" in line and filename not in line:
                        in_target_file_block = False
                    
                    if in_target_file_block and line.strip():
                        survivors.append(line.strip())
                
                if len(survivors) > 1:
                    break
                else:
                    survivors = []
            
            # ✨ 策略 B：针对扁平化日志的单行兜底匹配
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if filename in line and ("Survived" in line or "🙁" in line or "mutmut apply" in line or "🐾" in line):
                        survivors.append(line.strip())
            if survivors:
                break
                
    return "\n".join(survivors) if survivors else "No explicit surviving mutants recorded for this module in logs."

# ==========================================
# 3. 算子驱动的 Prompt 生成器
# ==========================================
def generate_incremental_prompt(file_path, src_code, v3_code, oracle_constraints, survivors_info):
    return f"""
We have an existing base test suite generated by V3 for the Python module `{file_path}`. 
Your task is to write ONLY SUPPLEMENTARY pytest test cases to augment the existing test suite and kill surviving mutants listed below. 
Do not rewrite or recreate the whole file.

=== ORACLE CONSTRAINTS (CRITICAL RULES) ===
{oracle_constraints}
===========================================

[Surviving Mutants (Your focused target to KILL)]
{survivors_info}

[Full Source Code under Test]
{src_code}

[Existing V3 Base Test Code (Do not duplicate these cases)]
{v3_code}

Output ONLY the supplementary Python code enclosed in a single markdown block (```python ... ```). 
Do not output imports or mocks that are already available in the file unless absolutely necessary.
"""

# ==========================================
# 4. 核心增量引擎
# ==========================================
def main():
    # 🎯 [微创手术 1]：引入参数解析，接收 Bash 传递的 --test-file
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-file", required=False, help="目标测试文件的路径")
    parser.add_argument("--max-iterations", type=int, default=3)
    args = parser.parse_args()

    # 🎯 [微创手术 2]：根据 test-file 自动切换 CURRENT_PROJECT
    global CURRENT_PROJECT
    if args.test_file:
        if "flutils" in args.test_file:
            CURRENT_PROJECT = "flutils"
        elif "cookiecutter" in args.test_file:
            CURRENT_PROJECT = "cookiecutter"
        elif "sanic" in args.test_file:
            CURRENT_PROJECT = "sanic"
        elif "httpie" in args.test_file:
            CURRENT_PROJECT = "httpie"

    if CURRENT_PROJECT not in PROJECT_CONFIGS:
        raise ValueError(f"❌ 未知的项目配置: {CURRENT_PROJECT}")

    cfg = PROJECT_CONFIGS[CURRENT_PROJECT]
    TARGET_MODULES = cfg["modules"]
    STAGE2_DIR = cfg["stage2_dir"]
    STAGE3_DIR = cfg["stage3_dir"]
    SRC_DIR = cfg["src_dir"]
    PROMPT_FILE = cfg["prompt_file"]
    MUTMUT_REPORT = cfg.get("mutmut_report")

    print(f"🚀 启动静态变异感知增量级联引擎 [{CURRENT_PROJECT.upper()} 模式]...")
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    oracle_constraints = "No specific constraints provided."
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            oracle_constraints = f.read()

    system_prompt = (
        "You are an expert Python QA engineer specializing in test suite augmentation and mutation score acceleration."
    )

    for mod, src_rel_path in TARGET_MODULES.items():
        # 🎯 [微创手术 1 的延伸]：如果传递了 test-file，只处理匹配的那个模块
        if args.test_file and mod not in args.test_file:
            continue

        src_path = os.path.join(SRC_DIR, src_rel_path)
        mod_stage2_target = os.path.join(STAGE2_DIR, mod)
        
        if not os.path.exists(src_path):
            print(f"⏩ 源码不存在，跳过模块: {mod}")
            continue

        v3_test_filename = None
        v3_stage2_path = None
        v3_stage3_path = None

        # 🎯 [微创手术 3]：智能兼容 Sanic 的子目录结构 与 Flutils 的扁平文件结构
        if os.path.isdir(mod_stage2_target):
            # Sanic 模式 (mod 是目录名)
            mod_stage3_dir = os.path.join(STAGE3_DIR, mod)
            valid_files = [f for f in os.listdir(mod_stage2_target) if f.startswith("test_") and f.endswith(".py") and "_patch" not in f]
            if not valid_files:
                print(f"⏩ 目录 {mod_stage2_target} 下未找到合法的测试用例，跳过。")
                continue
            v3_test_filename = next((f for f in valid_files if "failing" in f), valid_files[0])
            v3_stage2_path = os.path.join(mod_stage2_target, v3_test_filename)
            v3_stage3_path = os.path.join(mod_stage3_dir, v3_test_filename)
            os.makedirs(mod_stage3_dir, exist_ok=True)
            
        else:
            # Flutils/Cookiecutter 模式 (mod 直接是 test_xxx.py 文件名)
            v3_test_filename = mod
            failing_name = mod.replace(".py", "_failing.py")
            
            # 优先寻找 _failing.py 影子兵团
            if os.path.exists(os.path.join(STAGE2_DIR, failing_name)):
                v3_test_filename = failing_name
            elif not os.path.exists(os.path.join(STAGE2_DIR, mod)):
                # 如果都没有，可能是 Bash 脚本 touch 出来的空文件
                if args.test_file and os.path.exists(args.test_file):
                    v3_test_filename = os.path.basename(args.test_file)
                else:
                    print(f"⏩ 目录 {STAGE2_DIR} 下未找到 {mod}，跳过。")
                    continue
                    
            v3_stage2_path = os.path.join(STAGE2_DIR, v3_test_filename)
            v3_stage3_path = os.path.join(STAGE3_DIR, v3_test_filename)
            os.makedirs(STAGE3_DIR, exist_ok=True)

        print(f"\n🎯 正在处理模块: {mod} -> 目标靶位: {v3_test_filename}")
        
        # 安全拷贝：处理 Bash 脚本可能已经建了同名空文件的情况
        if os.path.exists(v3_stage2_path) and not os.path.samefile(v3_stage2_path, v3_stage3_path):
            shutil.copy_file = shutil.copy(v3_stage2_path, v3_stage3_path)
            print(f"📦 [自动备份] 已将 Stage2 基础用例安全同步至 Stage3 隔离区。")

        survivors_info = extract_surviving_mutants(src_rel_path, MUTMUT_REPORT)
        print(f"📊 已成功检索到变异体关联行数: {len(survivors_info.splitlines())} 行")

        with open(src_path, "r", encoding="utf-8") as f:
            src_code = f.read()
            
        with open(v3_stage3_path, "r", encoding="utf-8") as f:
            v3_code = f.read()

        user_prompt = generate_incremental_prompt(src_rel_path, src_code, v3_code, oracle_constraints, survivors_info)

        try:
            print(f"🧠 正在向 DeepSeek R1 发送请求 (等待慢思考过程)...")
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt}, 
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=8192
            )
            
            message = response.choices[0].message
            final_content = message.content or ""
            
            # 🔥 官方 API 专属：暴力提取推理思维链并写盘保存
            reasoning = getattr(message, 'reasoning_content', '')
            if not reasoning and hasattr(message, 'model_extra') and message.model_extra:
                reasoning = message.model_extra.get('reasoning_content', '')

            if reasoning:
                print(f"\n🤔 [R1 深度思考流] 👇\n{reasoning[:500]}...\n👆 [思考结束]\n")
                # 级联保存推理详情，为后续论文的 Case Study 留存第一手科研数据
                reasoning_log_path = v3_stage3_path + ".reasoning.txt"
                try:
                    with open(reasoning_log_path, "w", encoding="utf-8") as rf:
                        rf.write(reasoning)
                    print(f"📝 [思考记录] 已成功保存思考链至: {reasoning_log_path}")
                except Exception as fe:
                    print(f"⚠️ 保存思考日志失败: {fe}")
            else:
                print("⚠️ [警告] 未抓取到 reasoning_content。")

            if not final_content:
                print("❌ 失败: R1 返回内容为空")
                continue
                
            # 1. 安全前置清洗：剔除正文可能夹带的任何 <think> 标签残留
            final_content = re.sub(r'<think>.*?</think>', '', final_content, flags=re.DOTALL)

            # 2. 健壮提取：匹配 ```python ... ```，使用十六进制表示反引号，避免平台编译冲突
            match = re.search(r'\x60{3}(?:python)?\s*(.*?)(?:\x60{3}|$)', final_content, re.DOTALL | re.IGNORECASE)
            
            if match:
                patch_code = match.group(1).strip()
            else:
                # 兜底提取：若大模型直接把代码吐在正文里，直接使用全文
                patch_code = final_content.strip()
                print("⚠️ 未检测到 \x60\x60\x60python 标记，采用兜底逻辑尝试直接提取正文...")

            # 3. 终极净化：剔除可能遗漏在两端的零散反引号
            patch_code = re.sub(r'^`{3}(?:python)?\s*', '', patch_code, flags=re.IGNORECASE)
            patch_code = re.sub(r'`{3}\s*$', '', patch_code)
            
            if patch_code:
                # 4. AST 语法检验防线
                try:
                    ast.parse(patch_code)
                except SyntaxError as se:
                    print(f"❌ 语法校验失败！错误信息: {se}")
                    continue

                with open(v3_stage3_path, "a", encoding="utf-8") as f:
                    f.write("\n\n# === R1 INCREMENTAL BOOSTER PATCH ===\n")
                    f.write(patch_code)
                print(f"✅ [级联成功] 增量高强度补丁已成功追加到 Stage3 的 {v3_test_filename}！")
            else:
                print(f"❌ 失败: 无法从 R1 的回复中提取有效的 Python 代码块。")
                
        except Exception as e:
            print(f"❌ API 请求或文件操作失败: {e}")

if __name__ == "__main__":
    main()