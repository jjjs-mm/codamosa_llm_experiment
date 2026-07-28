#!/bin/bash
# ==============================================================================
# 课题实验：HTTPie Stage 1 (SBST 基线重构) 批量测试生成脚本
# ==============================================================================

export ROOT_DIR="/root/CODAMOSA"
export OUTPUT_DIR="$ROOT_DIR/final_mutmut_suite_httpie/stage1_sbst"
export PROJECT_PATH="$ROOT_DIR/httpie_src" 

mkdir -p "$OUTPUT_DIR"

if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  警告: 检测到 \$DEEPSEEK_API_KEY 环境变量未设置！"
    exit 1
fi

# 🎯 像素级对齐 HTTPie 的 8 大核心骨干模块
TARGET_MODULES=(
    "httpie.core"
    "httpie.client"
    "httpie.context"
    "httpie.models"
    "httpie.cli.argparser"
    "httpie.cli.requestitems"
    "httpie.sessions"
    "httpie.plugins.manager"
)

echo "🚀 开始批量生成 HTTPie 目标模块的 Stage 1 测试用例..."
echo "📂 输出目标目录: $OUTPUT_DIR"
echo "----------------------------------------------------------------"

for MODULE in "${TARGET_MODULES[@]}"; do
    echo "⚡ [正在处理] 模块: $MODULE"
    
    python -m pynguin.generator \
        --project_path "$PROJECT_PATH" \
        --module_name "$MODULE" \
        --algorithm DYNAMOSA \
        --maximum-search-time 300 \
        --output-path "$OUTPUT_DIR" \
        --assertion_generation SIMPLE \
        --large_language_model_seeding True \
        --large_language_model_mutation True \
        --model_name "deepseek-chat" \
        --authorization_key "$DEEPSEEK_API_KEY" \
        --model-base-url "https://api.deepseek.com" \
        --model_relative_url "/chat/completions"

    if [ $? -eq 0 ]; then
        echo "✅ [成功] 模块 $MODULE 处理完毕。"
    else
        echo "❌ [失败] 模块 $MODULE 处理异常。"
    fi
    echo "----------------------------------------------------------------"
done

echo "🎉 HTTPie 的 Stage 1 基线数据重构完毕！"