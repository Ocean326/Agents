---
name: knowledge-router
description: 面向知识接入、上下文挂接、官方文档检索与 prompt 结构化的总入口路由器。用于在 PersonalBrain 挂接与检索、OpenAI 官方文档查询、以及 prompt 优化之间选择最合适的技能；当用户知道需要“先补上下文/先查资料/先把 prompt 变稳”但不知道具体技能名时优先使用。
---

# Knowledge Router

Use this as the public front door for context and knowledge operations.
Keep the scope tight: this router is about attaching the right knowledge surface before or around work, not about skill lifecycle management.

## Use This Router For

- “先查 brain 再答”
- “先查官方文档再建议方案”
- “把这个 prompt 优化成更稳的输入”
- requests where context acquisition is the missing step

## Do Not Use This Router For

- creating, installing, or packaging skills
  - use `skillops-router`
- AI research paper reading or appendix digestion
  - use `research-router`
- product planning or delivery orchestration
  - use `delivery-router`

## Routing Table

1. `attach-personalbrain`
   Use when the task should attach to PersonalBrain for durable memory lookup, prior conclusions, project-aware context, or thin writeback.

2. `openai-docs`
   Use when the user wants current OpenAI product or API guidance, citations, model selection, upgrade advice, or official docs answers.

3. `thinking-lenses`
   Use when the task is really a prompt-quality problem: underspecified prompts, handoff prompts, high-risk prompts, or requests to improve reasoning structure.

## Decision Rules

1. If the user wants durable memory or PersonalBrain context, route to `attach-personalbrain`.
2. If the source of truth should be official OpenAI documentation, route to `openai-docs`.
3. If the main issue is that the prompt or handoff is weak, route to `thinking-lenses`.
4. If the request is actually research evidence capture or paper digestion, hand off to `research-router`.
5. If no extra context layer is needed, say so explicitly and keep the task direct.

## Direct-Entry Exceptions

Skip this router and go direct when:

- the user explicitly names `attach-personalbrain`, `openai-docs`, or `thinking-lenses`
- the task is obviously just an OpenAI docs lookup
- the task is already inside a stable PersonalBrain-attached workflow

## Output Contract

Always return:

- missing context or knowledge need
- chosen skill, or the decision that none is needed
- why that route fits
- one concrete next action

## Guardrails

- do not expand this router into skill management
- do not confuse research reading with general knowledge routing
- do not insert a prompt-optimization pass when the prompt is already good enough
- preserve the lightest possible context move

## Example Triggers

- `Use $knowledge-router to decide whether this needs PersonalBrain, OpenAI docs, or prompt optimization first.`
- `使用 $knowledge-router 看看这件事该先挂 brain、查官方文档，还是先重写 prompt。`
- `Use $knowledge-router to pick the thinnest useful context layer before execution.`
