---
name: delivery-router
description: 面向交付与产品工作的总入口路由器。用于在端到端交付、产品发现、方案生成、需求定义、PRD/tech spec、方案批判、测试用例与最终验证之间选择最合适的技能；当用户要“把事情做成”但尚未明确是 discovery、proposal、planning、implementation 还是 verification 时优先使用。
---

# Delivery Router

Use this as the public front door for delivery and product work.
Treat it as a thin category router, not a second delivery manager.

Its main job is to decide whether the task needs:

- an end-to-end owner
- discovery
- proposal generation
- requirements and prioritization
- critique
- test planning
- a verification gate

## Use This Router For

- vague feature or project requests
- bugfixes or refactors that need product, design, implementation, and verification coordination
- requests that say “take this from idea to delivery”
- cases where the user knows the desired outcome but not the best delivery lane

## Do Not Use This Router For

- pure architecture or system-boundary work
  - use `architect-router`
- AI research workflow decisions
  - use `research-router`
- prompt optimization, docs lookup, or PersonalBrain attachment
  - use `knowledge-router`
- remote execution topology or explicit subagent orchestration
  - use `execution-router`

## Routing Table

1. `delivery-conductor`
   Use when the task needs one owner across discovery, planning, implementation, testing, and verification, or when the thread should be resumed and pushed toward a verified outcome.

2. `brainstorming`
   Use when the request is creative, underdefined, or benefits from ideation before planning or implementation.

3. `proposal-synthesis`
   Use when the user wants several complete candidate proposals, a recommended direction, or a critique-ready proposal packet from a still-open design space.

4. `business-analyst`
   Use for product discovery, stakeholder questions, competitive analysis, user needs, problem framing, and product briefs.

5. `product-manager`
   Use for PRDs, tech specs, acceptance criteria, feature prioritization, epics, and user-story breakdown.

6. `product-requirements`
   Use when the user wants an interactive, question-driven requirements pass that converges toward a high-quality PRD.

7. `proposal-critique-refine`
   Use when a coherent proposal already exists and now needs critique, stress testing, or bounded refinement.

8. `test-cases`
   Use when the main missing artifact is structured test coverage derived from requirements.

9. `verification-before-completion`
   Use when the work is already near done and the highest-value move is an honest verification gate before any completion claim, handoff, commit, or PR.

10. `bmad-orchestrator`
   Use when the request is explicitly about BMAD workflow setup, workflow status, or phase routing inside that system.

## Decision Rules

1. If the task needs one end-to-end owner, route to `delivery-conductor`.
2. If the task is blocked by not knowing what to build or why, route to `brainstorming` or `business-analyst`.
3. If the user needs several complete proposal options before critique, route to `proposal-synthesis`.
4. If the problem is mostly requirements quality, route to `product-manager` or `product-requirements`.
5. If a proposal exists and needs sharper judgment, route to `proposal-critique-refine`.
6. If the artifact gap is test coverage, route to `test-cases`.
7. If the work mostly exists and evidence is the weak point, route to `verification-before-completion`.

When in doubt, prefer `delivery-conductor` over piecing together a fragile chain of narrow skills.

## Direct-Entry Exceptions

Skip this router and use the specialist directly when:

- the user explicitly says `Use $delivery-conductor`
- the task is clearly one-lane, such as “写一个 PRD” or “给我测试用例”
- the user explicitly wants multiple complete proposal options before critique
- the user already has a stable proposal and only wants critique
- the task is already in final verification mode

## Output Contract

Always return:

- task type
- selected lane
- why the lane fits better than the nearby alternatives
- the next concrete action
- whether this should stay one-lane or be handed to `delivery-conductor`

## Guardrails

- do not force every product task through `delivery-conductor`
- do not turn pure implementation work into unnecessary product process
- do not send architecture-heavy work into product planning first
- if the real blocker is outside delivery scope, hand off cleanly instead of pretending this router owns it

## Example Triggers

- `Use $delivery-router to pick the right product or delivery skill for this feature request.`
- `使用 $delivery-router 看看这个需求该先 discovery、先写 PRD，还是直接交给 delivery-conductor。`
- `Use $delivery-router to decide whether this bugfix needs end-to-end ownership or just a focused planning skill.`
