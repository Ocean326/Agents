---
name: architect-router
description: 面向架构类工作的总入口路由器。用于在广义架构总控、ADR/治理、现有代码库重构、规格驱动设计、DDD/clean architecture、agent systems architecture 与架构文档评审之间选择最合适的入口；当用户知道“这是架构问题”但不知道具体 lane 时优先使用。
---

# Architect Router

Use this as the public front door for architecture work.
It keeps a stable category-level entry while preserving direct specialist access.

This router should usually do one of two things:

- hand broad architecture work to `architect`
- send clearly scoped architecture problems straight to the correct specialist lane

## Use This Router For

- broad system design requests
- ADR and trade-off questions where the exact architecture lane is unclear
- requests that mix codebase structure, governance, requirements, and agent boundaries
- users who want a stable “architecture front door” instead of remembering many lane names

## Do Not Use This Router For

- pure product discovery or delivery coordination
  - use `delivery-router`
- AI research workflow decisions
  - use `research-router`
- prompt shaping, docs lookup, or PersonalBrain attachment
  - use `knowledge-router`
- straightforward implementation or bugfix work without architecture uncertainty

## Routing Table

1. `architect`
   Use for broad, ambiguous, or cross-cutting architecture requests that need one architect-grade synthesis and lane selection.

2. `architecture-governance`
   Use for ADRs, trade-offs, architecture decisions, review gates, and governance-oriented recommendations.

3. `codebase-architecture`
   Use for existing codebases, module boundaries, dependency direction, modernization, and refactor sequencing.

4. `spec-driven-architecture`
   Use when architecture should be derived from PRDs, user flows, acceptance criteria, or greenfield requirements.

5. `ddd-clean-architecture`
   Use when domain boundaries, aggregates, bounded contexts, or clean layering are central.

6. `agent-systems-architecture`
   Use for agents, tools, memory layers, orchestration, autonomy boundaries, and human approval flows.

7. `architecture-docs-review`
   Use when the main task is reviewing an RFC, design doc, ADR, diagram, or dependency map.

8. `architecture-workbench`
   Use only as a fallback when the architecture shape is still unclear after the first classification pass.

## Decision Rules

1. If the request spans multiple architecture concerns, route to `architect`.
2. If the request clearly names a narrow architecture problem, go straight to the lane.
3. If the task is really implementation disguised as architecture, say so and avoid unnecessary routing.
4. Prefer one primary architecture lane; add a secondary lane only when it materially changes the recommendation.

## Direct-Entry Exceptions

Skip this router and use the specialist directly when:

- the user explicitly asks for `architect`
- the task is plainly one-lane, such as “review this RFC” or “analyze this codebase architecture”
- the user already knows they need agent systems architecture or DDD specifically

## Output Contract

Always return:

- architecture problem shape
- chosen lane
- why it is the right lane
- nearby lanes that were considered but rejected
- one concrete next architecture action

## Guardrails

- do not hide `architect` behind needless wrapper behavior
- do not force architecture framing onto pure coding tasks
- do not multiply lanes when one clear lane is enough
- if architecture is not the current blocker, hand off cleanly

## Example Triggers

- `Use $architect-router to choose the right architecture lane for this problem.`
- `使用 $architect-router 看看这个任务该走 architect 总控，还是直接进某个 architecture specialist。`
- `Use $architect-router to decide whether this is governance, codebase refactor, spec-driven design, or agent architecture.`
