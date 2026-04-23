# 实验档案：Vanilla LLM (纯大模型基线)

## 1. 实验基本信息
- **测试目标 (Target)**: `codetiming._timer`
- **算法设定 (Algorithm)**: DYNAMOSA + LLM Seeding + LLM Mutation
- **最大搜索时间 (Time)**: 60s
- **断言策略 (Assertion)**: `SIMPLE`
- **实验日期**: 2026-04-23

## 2. 大模型配置
- **LLM 引擎**: `deepseek-chat`
- **API 提供商**: DeepSeek 官方 API
- **温度 (Temperature)**: 1.0 (CODAMOSA 默认)

## 3. 当前 Prompt (系统提示词)
*(由于目前是纯基线，我们没有使用 CoT，只是使用了最基础的代码补全指令)*
- **System Prompt**: (无，直接传递了源码作为 Context)
- **User Prompt**: "Fill in the ??" (针对 Mutation) / 源码 Context (针对 Seeding)

## 4. 实验结果
- **成功用例 (Successful)**: 0 个
- **失败用例 (Failing)**: 7 个
- **结论**: 证明了“直接将未经约束的大模型接入 SBST 框架，会导致大量非法语法的生成，无法通过测试执行引擎的校验”。这为后续引入 Reasoning Patterns (思维链约束) 提供了强有力的反面基线。