---
name: research-idea-clarifier
description: 将模糊的 AI、深度学习和序列表征学习想法整理成更清晰的目标、假设、可检验命题、对比维度和最小可行实验。当用户只有粗糙 idea、半成型方法或零散笔记，需要把它们变成研究方向时使用。
---

# 想法澄清器

在你真正投入实验预算之前，用这个技能先压缩不确定性。

当一个 idea 需要更强的科学式发散或更明确的 hypothesis framing 时，读取 [references/upstream-patterns.md](references/upstream-patterns.md)。

## 工作流程

1. 先把 idea 重述为：
   - task
   - pain point
   - proposed change
   - expected benefit
2. 强制把想法压缩进一个小决策框架：
   - 要改进的表征是什么
   - 引入了什么 inductive bias
   - 应该击败什么已有 baseline
   - 什么证据会让这个 idea 变得可信
3. 明确区分：
   - core idea
   - optional bells and whistles
   - assumptions that might break
4. 对序列表征学习，显式检查：
   - 提升到底来自更长上下文、更好的目标函数、更强数据还是更强结构
   - 方法是否在序列长度变化或 domain shift 下仍然稳定
   - 是否有一个简单 baseline 就能解释看似显著的提升
5. 将结果整理成：
   - 一句贡献总结
   - 2-3 个可检验 hypotheses
   - 第一个最小可行实验
6. 如果想法看起来太弱或赛道太拥挤，转交给 `research-novelty-audit`。
7. 如果 framing 已经稳定，转交给 `research-experiment-design-planner`。

## 输出要求

返回：
- 一版整理后的 idea statement
- 关键假设与风险
- 两个核心对比维度
- 第一个该跑的实验

## 示例

- “使用 $research-idea-clarifier 把这个粗糙的序列表征想法磨成可验证方案。”
- “使用 $research-idea-clarifier 把这份方法笔记整理成一个研究方向。”
- “使用 $research-idea-clarifier 告诉我这里真正的核心贡献是什么。”
