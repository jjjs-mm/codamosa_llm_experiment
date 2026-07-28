#!/bin/bash

set +e 

# 目标文件全部对准这些崩溃的用例集合！
TEST_FILES=(
    "test_output_main/test_cookiecutter_main_failing.py"
    "test_output_repo/test_cookiecutter_repository_failing.py"
    "test_output_find/test_cookiecutter_find_failing.py"
)

echo "🚀 开始执行大批量双循环实验..."

for file in "${TEST_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "====================================================="
        echo "🎯 正在集中火力攻坚: $file"
        echo "====================================================="
        
        python dual_loop_engine.py --test-file "$file"
        
        echo "✅ $file 修复流程结束。"
    else
        echo "⚠️ 跳过: 找不到文件 $file"
    fi
done

echo "🎉 所有实验批处理完成！"