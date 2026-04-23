---
name: research-novelty-audit
description: 评估 AI、深度学习和序列表征学习 idea 或 draft 的新颖性与竞争定位。当 Codex 需要对比 prior work、压力测试贡献主张、提前暴露 reviewer 质疑，或判断一个想法是否值得继续做实验时使用。
---

# 新颖性审计

在你把故事写成 reviewer 一看就会说“只是 baseline tweak”之前，先使用这个技能。

当任务需要更强的 critical-thinking 或更偏 AI 的 idea 压测模式时，读取 [references/upstream-patterns.md](references/upstream-patterns.md)。

## 工作流程

1. 用一句话写出你声称的新颖性。
2. 把 novelty 拆成几个组成部分：
   - objective
   - architecture
   - data or augmentation
   - training recipe
   - evaluation setting
3. 对每一部分判断它是：
   - 真正新
   - 旧元素重组
   - 主要是调参优化
   - 只在当前任务设定下才算新
4. 对 AI 工作，重点盯这些问题：
   - 是否缺少强基线
   - benchmark 是否有 cherry-pick
   - 提升是否在 compute matching 后消失
   - 新颖性是否本质上只是 scaling
   - 是否缺少序列长度或数据规模维度测试
5. 最终给出三种结果之一：
   - novelty 已经足够强
   - novelty 偏弱，但可以通过重 framing 挽救
   - novelty 需要新实验，或者必须收窄 claim
6. 如果还能通过 framing 挽救，转交给 `research-paper-production-pipeline`。
7. 如果需要更多证据，转交给 `research-experiment-design-planner`。

## 输出要求

返回：
- 新颖性结论
- 最强的 prior-work 冲突点
- reviewer 风格的质疑
- 最小但最有效的增强改动

## 示例

- “使用 $research-novelty-audit 判断这个 idea 到底算不算新。”
- “使用 $research-novelty-audit 像 reviewer 一样压测这个表征学习 claim。”
- “使用 $research-novelty-audit 在我开始写论文前找出最强的 prior-work 冲突。”
