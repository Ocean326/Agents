---
name: skillops-router
description: 面向 skill 体系运维的总入口路由器。用于在技能发现、安装、来源材料抽取成 skill、创建/更新、插件脚手架、以及 skill 使用闭环复盘之间选择最合适的技能；当用户要扩技能体系、整理 skills、决定该扩现有 skill 还是新建 skill，或把人/书/理论/博客蒸馏成 skill 时优先使用。
---

# SkillOps Router

Use this as the public front door for skill lifecycle work.
This router owns skill-system questions, not general knowledge questions.

Its main job is to answer:

- search or install?
- distill sources into a skill candidate?
- extend an existing skill or create a new one?
- create a skill or scaffold a plugin?
- do a usage review or not?

## Use This Router For

- growing or cleaning up the skill system
- deciding whether a workflow should become a new skill
- installing or discovering external skills
- scaffolding plugins only when packaging is truly needed
- reviewing how skills performed in a thread

## Do Not Use This Router For

- PersonalBrain retrieval, OpenAI docs lookup, or prompt optimization
  - use `knowledge-router`
- product delivery or architecture decisions that merely mention skills
- defaulting to plugin creation when a plain skill would do

## Routing Table

1. `skill-finder`
   Use for inventory, search, comparison, and general skill collection management.

2. `skill-installer`
   Use when the user wants to install a curated skill or install a skill from a GitHub repo/path.

3. `source-to-skill`
   Use when the user wants to turn a person, book, theory, blog, article, transcript, or mixed source bundle into a skill-ready packet before deciding whether to extend or create a skill.

4. `skill-creator`
   Use when the user wants to create a new skill or update an existing skill.

5. `plugin-creator`
   Use only when the user explicitly needs plugin packaging, plugin namespace scaffolding, or marketplace-facing plugin structure.

6. `skill-skill-usage-close-loop`
   Use when the user wants a bounded retrospective on skills used in the current thread.

## Decision Rules

1. First decide whether the request is about discovery, installation, source distillation, creation, packaging, or review.
2. If the task starts from source material and not yet a stable skill shape, prefer `source-to-skill` before `skill-creator`.
3. Prefer extending or refining an existing skill before creating a new overlapping one.
4. Prefer a plain skill before a plugin unless distribution, namespacing, or packaging is the actual need.
5. If a repo-local intake router or ownership registry exists, use it before creating new canonical skill scope.
6. If the request does not actually need skill-system work, say so explicitly instead of forcing a skillops lane.
7. If the request is really about prompt quality or official docs, hand off to `knowledge-router`.

## Direct-Entry Exceptions

Skip this router and go direct when:

- the user explicitly says `Use $skill-creator`, `Use $skill-installer`, or `Use $plugin-creator`
- the user explicitly wants to distill source material into a skill candidate
- the task is obviously one-lane, such as “install this skill” or “scaffold a plugin”
- the user only wants a bounded retrospective on skills already used

## Output Contract

Always return:

- skillops task type
- selected lane
- whether the decision is `search_existing_skill`, `install_skill`, `distill_source_to_skill_packet`, `extend_existing_skill`, `create_new_skill`, `scaffold_plugin`, or `usage_review`
- one concrete next action

## Guardrails

- do not create a plugin by default
- do not create overlapping skills without first checking for a natural owner
- do not route general knowledge work into skillops
- if the correct answer is “keep this manual for now,” say so explicitly

## Example Triggers

- `Use $skillops-router to decide whether this should extend an existing skill, create a new one, or stay manual.`
- `使用 $skillops-router 看看这件事该搜现有 skill、安装 skill、写新 skill，还是只做 plugin 脚手架。`
- `使用 $skillops-router 判断这批人/书/理论/博客材料该先蒸馏成 skill candidate，还是直接改现有 skill。`
- `Use $skillops-router to choose the right skill-management lane for this workflow idea.`
