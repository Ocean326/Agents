# Routing Matrix

Use this matrix after the initial context sweep.
Pick one primary route and only add helpers that materially improve the outcome.

| Situation | Primary Helper | Fallback if Missing | Notes |
| --- | --- | --- | --- |
| Idea is vague, creative, or solution space is still open | `brainstorming` | Run a brief design-discovery pass locally | Use before implementation on creative work. |
| User needs multiple complete proposal options or a critique-ready recommendation from an open brief | `proposal-synthesis` | Generate 2-4 proposal briefs locally | Use before `proposal-critique-refine` when multiple viable directions still exist. |
| Requirements, priorities, or acceptance criteria are weak | `product-manager` | Structure a brief and implementation plan locally | Prefer when testable requirements are the blocker. |
| User explicitly wants a PRD or stronger requirement capture | `product-requirements` | Use `product-manager` style questioning locally | Best for higher-friction requirement gathering. |
| Coherent plan exists but needs sharper critique or stronger tradeoffs | `proposal-critique-refine` | Run a bounded critique-improve-verify loop locally | Do not use for blank-page ideation. |
| Clear implementation plan exists and tasks can be delegated | `subagent-driven-development` | Execute locally in ordered phases | Best after scope and acceptance criteria are stable. |
| Multiple independent issues or workstreams can proceed in parallel | `dispatching-parallel-agents` | Solve serially and keep isolation explicit | Do not parallelize tightly coupled work. |
| Coverage or QA scenarios need to be derived from requirements | `test-cases` | Write a focused test matrix locally | Use for structured validation planning. |
| Completion is about to be claimed | `verification-before-completion` | Apply its rules manually with fresh evidence | Never skip this gate. |

## Fallback Rule

If the matching helper skill is not available:
1. Preserve the helper's intent.
2. Run the smallest local workflow that achieves the same outcome.
3. Keep moving unless a real risk gate is hit.

## Tie-Breakers

If multiple helpers fit, prefer this order:
1. unblock ambiguity
2. lock requirements
3. execute
4. expand coverage
5. verify

Examples:
- vague feature request: `brainstorming` before `subagent-driven-development`
- vague request needing several full options: `proposal-synthesis` before `proposal-critique-refine`
- explicit spec with parallelizable tasks: `subagent-driven-development` and `dispatching-parallel-agents`
- bugfix near completion: `verification-before-completion` is mandatory even if no other helper is used
