---
name: research-paper-reading-compass
description: 深度阅读 AI、深度学习和序列表示学习论文，结构化提取问题定义、核心主张、模型结构、训练目标、数据集、基线、消融和失败模式。当 Codex 需要读论文、比较多篇工作，或在立题、实验、写作前整理研究笔记时使用。
---

# 论文阅读罗盘

使用这个技能，把论文整理成可复用的研究资产，而不是松散摘要。

当任务需要更强的文献综述、引用整理或审稿式阅读模式时，读取 [references/upstream-patterns.md](references/upstream-patterns.md)。

## 最小提取框架

- 任务与设定
- 论文声称的贡献
- 表征方式选择
- 模型结构与训练目标
- 数据与预处理
- 基线设置与比较强度
- 评估指标
- 消融与失败分析
- 仍然不清楚的点

## 工作流程

1. 先明确阅读目标：
   - 快速筛查
   - 深入理解
   - 与其他方法对比
   - 为实验设计做准备
2. 按顺序阅读标题、摘要、引言、方法、实验和结论。
3. 将论文整理成固定结构：
   - `problem`
   - `claim`
   - `method`
   - `evidence`
   - `limits`
   - `follow_up_questions`
4. 对 AI 和序列任务，额外关注：
   - 序列长度或上下文窗口假设
   - 预训练与微调的边界
   - tokenizer 或输入编码选择
   - 算力规模与 batch size 敏感性
   - 提升究竟来自结构、目标函数、数据还是调参
5. 如果 appendix 很关键，或者正文写得不够清楚，转交给 `research-supplement-digestion`。
6. 如果论文暴露出一个新方向或研究空档，转交给 `research-idea-clarifier` 或 `research-novelty-audit`。
7. 如果这篇论文主要用于给 draft 或汇报提供证据，转交给 `research-paper-production-pipeline` 或 `research-slides-and-poster-studio`。

## 输出要求

返回：
- 一段 5-10 行的核心总结
- 一个 claim-to-evidence 对照表
- 最强基线对比结论
- 最可疑或最薄弱的一环
- 下一步最合适的转交方向

## 示例

- “使用 $research-paper-reading-compass 读这篇序列建模论文，并告诉我真正的新意是什么。”
- “使用 $research-paper-reading-compass 对比这三篇表征学习论文。”
- “使用 $research-paper-reading-compass 消化这篇论文，帮助我判断要不要复现。”
