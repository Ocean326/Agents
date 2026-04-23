# Pattern Selection

Use this reference when deciding whether to stay simple or escalate into a richer workflow.

## Primitive Ladder

Escalate only when the lower layer becomes brittle.

| Primitive | Best for | Escalate when |
| --- | --- | --- |
| Prompt | one focused request | repeated misses or too many branches |
| Instruction | persistent guidance | needs reusable assets or workflow logic |
| Skill | reusable workflow or reference bundle | needs ownership transfer or live delegation |
| Single agent | one role with bounded tools and context | context overload, tool overload, or branching overload |
| Multi-agent | separable roles or ownership transitions | only after simpler variants fail or become unmaintainable |
| Hook or deterministic guardrail | enforcement and lifecycle checks | only when behavior must be automatic and reliable |

## Escalation Signals

Stay single-agent by default.
Escalate when one or more signals are clearly present:

- `context overload`
  - one role needs too many unrelated knowledge packs
- `tool overload`
  - tool choices are numerous or semantically overlapping
- `ownership transfer`
  - a specialist must take over the interaction, not just return a result
- `time-spanning work`
  - the workflow must pause, wait, resume, or survive human approval
- `stable rubric`
  - a reviewer or evaluator can judge outputs consistently enough to drive iteration
- `independent parallel work`
  - multiple subtasks can run concurrently without shared mutable state

## Pattern Matrix

| Pattern | Use when | Avoid when | Required externalized state |
| --- | --- | --- | --- |
| Prompt chain | stages are fixed and ordered | decomposition changes every run | `stage`, `inputs`, `validation_result` |
| Router | input type or intent determines path | routing confidence is low and downstream actions are risky | `route`, `route_confidence`, `fallback_path` |
| Planner-executor-reviewer | the plan is dynamic but review criteria are clear | workers need constant coordination with each other | `plan`, `current_step`, `review_status` |
| Orchestrator-workers | one front door should coordinate bounded workers | the manager would need to micromanage every token | `manager_state`, `worker_assignments`, `worker_outputs` |
| Evaluator-optimizer | feedback is structured and likely to improve the output | grading is subjective or contradictory | `rubric`, `score`, `revision_count`, `threshold` |
| Handoff | a specialist must own the next turn | results can just be returned to a central controller | `active_owner`, `handoff_payload`, `history_slice` |
| Wake-up or re-entry | work spans time, approvals, or external waits | everything can finish in one bounded run | `checkpoint_id`, `resume_cursor`, `side_effect_log` |

## Topology Rules

- prefer one visible controller when the user expects one front door
- prefer specialist handoff when long specialist ownership is natural
- prefer workers as tools when the controller should stay the user-facing owner
- split by boundary:
  - tool boundary
  - context boundary
  - approval boundary
  - ownership boundary
- do not split just to create role theater

## Pattern Compositions

Use composition only when the seam is explicit:

- `router -> specialist`
  - classify first, then hand off to the right owner
- `orchestrator -> workers -> evaluator`
  - decompose, execute, then quality-check the synthesis
- `planner -> executor -> reviewer -> re-entry`
  - long task loop with checkpoints and human review
- `router -> evaluator-optimizer`
  - path differs by input, but each path still iterates to threshold

## Minimality Check

Before finalizing the design, ask:

1. Can one single agent plus a better prompt contract solve this?
2. Can a skill or instruction replace one of the agents?
3. Does each additional role have a unique boundary and failure mode?
4. Is the chosen pattern earning its complexity in reliability or clarity?

If the answer to any of these is no, simplify first.
