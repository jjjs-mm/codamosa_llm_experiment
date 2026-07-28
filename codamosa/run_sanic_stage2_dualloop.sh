#!/bin/bash
export ROOT_DIR="/root/codamosa_llm_experiment-feat-batch-experiment"
export INPUT_DIR="$ROOT_DIR/final_mutmut_suite_sanic/stage1_sbst"
export OUTPUT_DIR="$ROOT_DIR/final_mutmut_suite_sanic/stage2_v3"

if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  错误: 未设置 \$DEEPSEEK_API_KEY"
    exit 1
fi

echo "📂 [物理隔离] 同步 Stage 1 纯净种子至 Stage 2 专属沙箱..."
mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_DIR"/*.py 
cp "$INPUT_DIR"/*.py "$OUTPUT_DIR"/

TARGET_MODULES=(
    "sanic.router"
    "sanic.blueprints"
    "sanic.config"
    "sanic.exceptions"
    "sanic.headers"
    "sanic.server.protocols.http_protocol"
)

echo "🚀 [强制神谕注入] 启动 dual_loop_engine.py (--force-rewrite) 强攻 Sanic..."
echo "----------------------------------------------------------------"

for MODULE in "${TARGET_MODULES[@]}"; do
    FILE_NAME="test_${MODULE//./_}.py"
    FULL_TEST_PATH="$OUTPUT_DIR/$FILE_NAME"
    
    echo "🔥 [神谕注入中] 靶点副本: $FULL_TEST_PATH"
    
    if [ ! -f "$FULL_TEST_PATH" ]; then
        echo "⚠️  警告: 未找到种子文件 $FULL_TEST_PATH ，跳过。"
        continue
    fi
    
    python dual_loop_engine.py \
        --test-file "$FULL_TEST_PATH" \
        --max-retries 3 \
        --force-rewrite
        
    echo "----------------------------------------------------------------"
done

echo "🎉 Sanic 神谕强制注入演进完毕！"