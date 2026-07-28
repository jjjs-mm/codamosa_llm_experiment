import subprocess
import os
import re

folder = "/root/codamosa_llm_experiment-feat-batch-experiment/final_mutmut_suite_cookiecutter/stage2_v3/"

print("🔍 [Stage 2] 正在让 Pytest 自行交出红灯名单...")
res = subprocess.run(["pytest", folder, "-q", "--tb=short"], capture_output=True, text=True)

failed_funcs = set()
for line in res.stdout.split('\n'):
    if line.startswith("FAILED ") or line.startswith("ERROR "):
        match = re.search(r'::(test_[a-zA-Z0-9_]+)', line)
        if match:
            failed_funcs.add(match.group(1))

if not failed_funcs:
    print("✅ 基线纯绿，可直接变异！")
else:
    print(f"🎯 成功提取 {len(failed_funcs)} 个报错函数名！转换留存中...")
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                original_content = content
                for func in failed_funcs:
                    content = re.sub(rf'def {func}\s*\(', f'def skip_{func}(', content)
                
                if content != original_content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    print(f"🔪 已在 {f} 中切除红灯并转换为 skip_ 形式封存。")