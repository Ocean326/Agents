---
name: research-paper-production-pipeline
description: 将研究笔记和实验结果转成论文段落、摘要、相关工作定位、贡献表述、修改计划或 rebuttal，适用于 AI、深度学习和序列表征学习工作。当 Codex 需要起草、重构或修改论文时使用。
---

# 论文生产流水线

使用这个技能，把实验与证据组织成“论点-证据”对齐清晰的论文叙事。

当草稿需要更强的 scientific-writing、ML paper 或 figure planning 模式时，读取 [references/upstream-patterns.md](references/upstream-patterns.md)。

## 核心原则

在论文具备以下基础之前，不要直接开始写长段 prose：
- 一句主贡献表达
- 一套 figure plan
- 一条清楚的 baseline story
- 一句解释“为什么这项结果重要”

## 工作流程

1. 先搭一个紧凑的论文骨架：
   - problem
   - gap
   - method idea
   - evidence
   - takeaway
2. 把每个 claim 映射到支撑它的具体实验、图或引用。
3. 按以下顺序起草：
   - title candidates
   - abstract skeleton
   - introduction logic
   - method outline
   - experiment narrative
   - conclusion and limits
4. 对 AI 论文，显式检查：
   - 是否基于弱增益过度宣称
   - 基线叙事是否不公平
   - 数据设定是否含糊
   - 是否缺少算力或成本讨论
   - 是否缺少失败案例
5. 如果证据还不够强，回退到 `research-experiment-design-planner` 或 `research-training-and-ablation-loop`。
6. 如果方法表述仍然模糊，回退到 `research-idea-clarifier` 或 `research-novelty-audit`。

## 修改与 Rebuttal

当任务与 review 或 rebuttal 有关时：
- 把每条 reviewer 意见转成 action item
- 标记它属于 `writing`、`evidence` 或 `positioning`
- 用最小但有把握的 claim 回答
- 只有在论文不补实验就过不去时，才请求新实验

## 输出要求

返回：
- 当前论文骨架
- 缺失证据清单
- 你需要的 draft 段落或改写版本
- 如果被卡住，给出最合适的下一步转交

## 示例

- “使用 $research-paper-production-pipeline 把这些笔记整理成一篇序列表征学习论文的大纲。”
- “使用 $research-paper-production-pipeline 重写引言，让贡献更清楚。”
- “使用 $research-paper-production-pipeline 写一版不夸大的 reviewer 2 rebuttal。”
