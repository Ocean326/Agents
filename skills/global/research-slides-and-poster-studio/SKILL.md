---
name: research-slides-and-poster-studio
description: 基于 AI 和深度学习材料构建 talk deck、读书汇报、组会更新、poster 和研究简报。当 Codex 需要整理报告叙事、图表顺序、视觉层级或口头表达结构时使用。
---

# 幻灯片与海报工作室

当任务不只是“总结”，而是要让内容快速讲清、讲透时，使用这个技能。

当报告或 poster 需要更强的 figure planning 或 ML 论文叙事模式时，读取 [references/upstream-patterns.md](references/upstream-patterns.md)。

## 工作流程

1. 先明确展示模式：
   - 论文阅读汇报
   - 项目进展汇报
   - conference talk
   - poster
2. 构建叙事主线：
   - why this problem matters
   - what is broken in current methods
   - what the new idea changes
   - what evidence proves it
   - what remains limited
3. 先确定图表顺序，再写 slide 文本。
4. 对 AI 报告，优先遵循：
   - 一页只讲一个主点
   - 除非公式真的改变理解，否则少放公式
   - 让基线比较清楚可见
   - 用支撑主 claim 的 ablation 做重点展示
   - 留一页诚实的 limitations
5. 如果源笔记很弱或很散，转交给 `research-paper-reading-compass`。
6. 如果讲稿暴露出逻辑空档，转交给 `research-idea-clarifier`。
7. 如果某页还缺关键证据，转交给 `research-training-and-ablation-loop`。

## 输出要求

返回：
- slide 或 poster 大纲
- 推荐的图表顺序
- 每一部分的主讲信息
- 哪些内容应该删掉以避免分散主线

## 示例

- “使用 $research-slides-and-poster-studio 从这篇论文做一份 10 页组会报告。”
- “使用 $research-slides-and-poster-studio 把这份实验总结改成 poster 结构。”
- “使用 $research-slides-and-poster-studio 帮我把这个 idea 在 3 分钟内讲清楚新意。”
