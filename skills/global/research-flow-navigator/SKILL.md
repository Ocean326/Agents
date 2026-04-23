---
name: research-flow-navigator
description: 面向 AI 研究流程的总入口路由器，覆盖读论文、想法澄清、实验设计、结果分析和论文写作。当下一步不明确、任务跨越多个阶段，或 Codex 需要协调完整的深度学习与序列表征学习研究链路时使用。
---

# 研究流程导航器

当用户不知道从哪里开始，或者希望整条研究链路被统一协调时，使用这个技能作为主入口。

当任务跨越多个阶段，需要更强的研究编排模式时，读取 [references/upstream-patterns.md](references/upstream-patterns.md)。

## 路由分工

- `research-paper-reading-compass`
  - 用于论文消化、appendix 阅读和引用语境整理
- `research-supplement-digestion`
  - 用于 appendix 级复现细节和隐藏设定挖掘
- `research-idea-clarifier`
  - 用于想法澄清与 hypothesis 打磨
- `research-novelty-audit`
  - 用于新颖性压测与 reviewer 风险检查
- `research-experiment-design-planner`
  - 用于实验设计与消融规划
- `research-training-and-ablation-loop`
  - 用于 runs 解读与证据整理
- `research-paper-production-pipeline`
  - 用于论文写作与 rebuttal
- `research-slides-and-poster-studio`
  - 用于 talk、slides 和 poster

## 工作流程

1. 先识别当前状态：
   - vague idea
   - 读论文或文献整理
   - 实验设计阶段
   - 结果分析阶段
   - 写作或汇报阶段
2. 再识别主要阻塞点：
   - 理解不足
   - 贡献不清楚
   - 实验设计太弱
   - 证据还不成熟
   - 叙事不够强
3. 立刻路由到最能解阻的最窄技能，不要贪大而全。
4. 一次只保持一个主工作流，不要让“先写着看看”掩盖证据问题，也不要让“先多跑点实验”掩盖想法本身不清楚的问题。
5. 对 AI 研究，重点防止这些错误跳转：
   - 基线公平性还没查清就开始写论文
   - compute 没对齐就谈 scaling claim
   - prior work 还没压透就宣称 novelty
   - 核心 idea 还没 sharpen 就先堆很多实验

## 输出要求

返回：
- 当前阶段
- 主阻塞点
- 推荐 skill
- 一个具体下一步动作
- 再下一步建议

## 示例

- “使用 $research-flow-navigator 看看我当前的研究状态，并告诉我下一步最该做什么。”
- “使用 $research-flow-navigator 把这份混乱笔记路由成一个可执行研究流程。”
- “使用 $research-flow-navigator 帮我决定这些论文、半成型想法和几次 runs 接下来怎么处理。”
