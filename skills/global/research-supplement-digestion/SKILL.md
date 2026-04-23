---
name: research-supplement-digestion
description: 消化 AI 和深度学习论文中的 appendix、补充材料、长表格、实现细节和隐藏实验设置。当正文写得不够清楚，或 Codex 需要复现关键细节、消融设置、面向审稿人的补充证据时使用。
---

# 补充材料消化

当 appendix 或 supplement 和正文一样重要时，使用这个技能。

当任务需要更强的严谨性检查、引用支撑或相关工作追踪时，读取 [references/upstream-patterns.md](references/upstream-patterns.md)。

## 重点搜寻内容

- 精确的数据划分与过滤方式
- 训练流程与优化器细节
- 超参数搜索范围与最终取值
- 被藏在正文之外的负结果
- 额外消融与敏感性实验
- 会改变结果的实现细节
- 能真正支撑论文主张的附加图表

## 工作流程

1. 先明确你希望补充材料回答什么问题。
2. 先扫章节标题、图注和表题，再进行逐段阅读。
3. 只提取会实质影响以下内容的细节：
   - 可复现性
   - 性能提升的解释
   - 基线比较是否公平
   - 后续实验设计
4. 将信息拆分为：
   - `hard_details`
   - `probable_assumptions`
   - `still_missing`
5. 对 AI 和序列任务，重点检查：
   - masking 或 padding 规则
   - 序列截断方式
   - batch 构造策略
   - curriculum 或采样技巧
   - checkpoint 选择标准
   - decoding 或 retrieval 设置
6. 如果补充材料暴露出证据不足的问题，转交给 `research-novelty-audit`。
7. 如果补充材料提供了清晰的复现路径，转交给 `research-experiment-design-planner`。

## 输出要求

返回：
- 一份高价值隐藏细节清单
- 一份实验关键设置清单
- 一次基线公平性检查
- 仍然阻塞复现的未解问题

## 示例

- “使用 $research-supplement-digestion 告诉我作者在正文里漏掉了什么。”
- “使用 $research-supplement-digestion 从 appendix 里提取全部复现关键设置。”
- “使用 $research-supplement-digestion 检查补充材料是否真的支撑论文主结论。”
