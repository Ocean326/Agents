---
name: research-training-and-ablation-loop
description: 分析 AI、深度学习和序列表征学习任务中的训练过程、消融结果、评测表格和失败模式。当 Codex 需要解释模型行为、排序下一步实验，或把 runs 总结成清晰结论时使用。
---

# 训练与消融循环

当 runs 已经存在，任务是尽快从结果中学到东西时，使用这个技能。

当结果需要更强的可视化、统计检验或实验跟踪模式时，读取 [references/upstream-patterns.md](references/upstream-patterns.md)。

## 工作流程

1. 先明确你的核心问题：
   - 为什么失败
   - 哪个 ablation 真正起作用
   - 下一步该跑什么
   - 哪些结果值得写进论文
2. 把结果整理成几个块：
   - headline metrics
   - training dynamics
   - ablation deltas
   - error analysis
   - unresolved anomalies
3. 对 AI 和序列任务，重点检查：
   - loss 与下游指标是否不匹配
   - seed 是否导致不稳定
   - 序列长度拉长后是否退化
   - 数据少与数据多时表现是否不同
   - train 与 inference 是否存在错位
   - decoding 是否敏感
4. 对每个结果分类：
   - supports the main claim
   - weakly supports the claim
   - contradicts the claim
   - is probably a bug or setup artifact
5. 推荐下一轮动作：
   - rerun
   - 更紧的 ablation
   - error slice
   - baseline 修复
   - 可直接用于写作的总结
6. 如果证据已经成熟，转交给 `research-paper-production-pipeline`。

## 输出要求

返回：
- 主发现
- 最可能的失败模式或解释
- 价值最高的下一个实验
- 可直接用于写作的证据总结

## 示例

- “使用 $research-training-and-ablation-loop 解释这些训练曲线，并告诉我下一步该跑什么。”
- “使用 $research-training-and-ablation-loop 判断这里到底哪个 ablation 真正重要。”
- “使用 $research-training-and-ablation-loop 把这张结果表整理成可直接写进论文的证据总结。”
