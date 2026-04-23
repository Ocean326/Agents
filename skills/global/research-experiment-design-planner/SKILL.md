---
name: research-experiment-design-planner
description: 为 AI 研究规划考虑算力约束的实验方案，包括数据集、划分、基线、指标、消融和成功标准。当 Codex 需要把一个 idea 变成可执行的深度学习或序列表征学习实验计划时使用。
---

# 实验设计规划器

使用这个技能，把一个有潜力的 idea 变成精炼且有说服力的实验计划。

当计划需要更强的 evaluation、tokenization、long-context 或 run-tracking 模式时，读取 [references/upstream-patterns.md](references/upstream-patterns.md)。

## 工作流程

1. 先锁定实验目标：
   - 要验证的 claim 是什么
   - 什么结果算成功
2. 明确第一轮比较对象：
   - trivial baseline
   - 当前强基线
   - 最接近的 prior method
3. 选择：
   - datasets and splits
   - metrics
   - compute budget
   - reporting format
4. 设计消融阶梯：
   - 去掉主改动
   - 替换目标函数
   - 替换模型结构
   - 改变数据规模或数据条件
   - 压测序列长度或上下文大小
5. 检查 AI 任务常见失败点：
   - 是否存在隐藏调参优势
   - 预训练数据是否不公平
   - 参数量是否不可比
   - seed 是否不稳定
   - 指标是否和 claim 不匹配
6. 第一轮尽量保持最小化。优先一个能定性的关键结果，而不是一大堆模糊矩阵。
7. 如果计划被“贡献点不清楚”卡住，回退到 `research-idea-clarifier`。

## 输出要求

返回：
- 实验目标
- 基线集合
- 指标与数据设置
- 消融矩阵
- 成功与失败判据

## 示例

- “使用 $research-experiment-design-planner 为这个序列模型想法设计第一版实验计划。”
- “使用 $research-experiment-design-planner 选择最小但有说服力的消融集合。”
- “使用 $research-experiment-design-planner 把这个 novelty claim 变成清晰的评测计划。”
