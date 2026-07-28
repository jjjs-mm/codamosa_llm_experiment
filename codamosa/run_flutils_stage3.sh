#!/bin/bash
export ROOT_DIR="/root/codamosa_llm_experiment-feat-batch-experiment"
export INPUT_DIR="$ROOT_DIR/final_mutmut_suite_flutils/stage2_v3"
export OUTPUT_DIR="$ROOT_DIR/final_mutmut_suite_flutils/stage3_cascade"

if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  错误: 检测到 \$DEEPSEEK_API_KEY 未设置！"
    exit 1
fi

echo "📂 [物理隔离] 同步 flutils Stage 2 精英用例至 Stage 3 级联专属沙箱..."
mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_DIR"/*.py 

# 核心精髓：不仅复制主测试用例，连同 failing.py 和防死锁的 conftest.py 一并继承过去
cp "$INPUT_DIR"/*.py "$OUTPUT_DIR"/ 2>/dev/null || true

TARGET_MODULES=(
    "flutils.cmdutils"
    "flutils.codecs"
    "flutils.txtutils"
    "flutils.decorators"
    "flutils.validators"
    "flutils.packages"
    "flutils.moduleutils"
)

echo "🧠 [级联引擎点火] 启动 r1_incremental_booster.py 强攻 flutils..."
echo "----------------------------------------------------------------"

for MODULE in "${TARGET_MODULES[@]}"; do
    FILE_NAME="test_${MODULE//./_}.py"
    FULL_TEST_PATH="$OUTPUT_DIR/$FILE_NAME"
    
    echo "🔥 [R1 级联强化中] 模块: $MODULE"
    
    if [ ! -f "$FULL_TEST_PATH" ]; then
        echo "⚠️  注意: $MODULE 没有历史种子，创建空基底触发 R1 零样本生成！"
        touch "$FULL_TEST_PATH"
    fi
    
    # 驱动 R1 开启慢思考增量迭代，默认高强度迭代 3 轮
    python r1_incremental_booster.py \
        --test-file "$FULL_TEST_PATH" \
        --max-iterations 3
        
    echo "----------------------------------------------------------------"
done

echo "🎉 flutils 满血版 Stage 3 级联增强全部完毕！"