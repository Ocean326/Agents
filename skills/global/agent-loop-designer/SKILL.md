---
name: agent-loop-designer
description: Design single-agent or multi-agent workflows, orchestration loops, handoffs, evaluator-optimizer cycles, and wake-up or re-entry patterns for agentic systems. Use when Codex needs to decide whether work should stay as a prompt, instruction, skill, single agent, or multi-agent topology, and when turning that choice into concrete prompt contracts, prompt-refinement gates, externalized state schemas, stop rules, approval gates, and close-loop evaluation plans.
---

# Agent Loop Designer

Design the smallest agentic workflow that can do the job reliably.
Prefer explicit state, typed handoffs, bounded loops, and reviewable stop rules over vague autonomy.

Read these references only when needed:
- [pattern-selection.md](./references/pattern-selection.md) for pattern choice, escalation signals, and topology rules
- [prompt-contracts.md](./references/prompt-contracts.md) for controller, worker, router, evaluator, handoff, and re-entry prompt shapes
- [prompt-reliability.md](./references/prompt-reliability.md) for diagnosing when prompt quality is breaking loop reliability, and for prompt refinement and rollback design
- [eval-close-loop.md](./references/eval-close-loop.md) for evaluation gates, traces, approval rules, and iteration loops
- [failure-modes.md](./references/failure-modes.md) for common breakpoints and stress tests before rollout

## Use This Skill For

- designing a single-agent or multi-agent workflow before implementation
- deciding between prompt, instruction, skill, single agent, multi-agent, or hook
- designing recurring prompt-driven automations that should greedily advance one bounded macro packet per wake-up instead of fragmenting into tiny handoffs
- designing planner-executor-reviewer, router, orchestrator-workers, evaluator-optimizer, handoff, or wake-up and re-entry loops
- turning agent ideas into concrete prompt contracts, tool boundaries, state schemas, and stop conditions
- designing prompt refinement as a first-class reliability mechanism when prompt quality is causing routing, tool, handoff, or schema failures
- defining prompt-quality gates such as a prompt rubric, regression cases, plateau rules, and approval checkpoints for prompt changes
- designing prompt artifact lifecycle, including ownership, versioning, approval, rollback, and delegation to a prompt refiner
- shaping self-improving or self-iterating task loops that need review gates instead of unconstrained recursion
- defining how agents should collaborate, hand off work, share context, and recover from pause or failure

## Do Not Use

- the task is only to improve one prompt and there is no loop, ownership, state, or workflow design question
  - use `thinking-lenses`
- the main question is broader agent-system architecture across tools, memory, and autonomy policy
  - use `agent-systems-architecture`
- the main blocker is whether to execute locally, in parallel, or through subagents right now
  - use `execution-router`
- the user wants a retrospective on current-thread skill usage
  - use `skill-skill-usage-close-loop`
- the user wants cross-session evidence about prompt or workflow failures
  - use `codex-session-evolution`

## Output Contract

Always produce:
- `task frame`
- `minimum viable primitive`
- `topology`
- `loop pattern`
- `macro packet contract` when the workflow is recurring or wake-up based
- `state and checkpoint model`
- `artifact surface`
- `prompt contract pack`
- `prompt quality and refinement plan`
- `evaluation and approval plan`
- `stop rules and failure recovery`

When the design is for real implementation or handoff, also produce:
- `pattern choice rationale`
- `input and output schemas`
- `ownership map`
- `next experiment`

## Core Rules

- start with the simplest primitive that can succeed
- split by boundary, not by vibe
- for recurring work, default to `one wake-up = one primary mission`
- allow one recurring mission to include multiple same-mission substeps in a single wake-up when they do not require a new external wait or a new control decision
- keep one owner for each turn or state transition
- pass structured state between nodes whenever possible
- externalize any state that affects routing, memory, permissions, or durable truth
- lock `target_boundary`, `success_evidence`, and `exact_refuse_boundary` before execution whenever the workflow is expected to resume later
- reward real boundary crossing over document churn; wording cleanup, memory sync, and handoff polish are not completion by themselves
- prefer a thin entry prompt plus repo-local durable instructions over ever-growing prompt monoliths
- prefer short natural-language control text plus a few exact fields over pseudo-legal prompt contracts
- define the minimum fixed rules zone that automation may not self-rewrite, then keep the rest in mutable task bodies or artifacts
- treat human-readable artifact surfaces as part of the design, not as afterthoughts
- for long-running external work, separate `launch now` from `harvest later`
- treat prompts as versioned artifacts when they affect routing, tool use, safety, or control flow
- define exit conditions for every loop before proposing the loop
- separate task-output evaluation from prompt-quality evaluation when the prompt itself may be the bottleneck
- every prompt change loop needs a rubric, threshold, max prompt revisions, and a no-scope-change rule
- prefer evaluation-backed iteration over open-ended self-improvement claims
- make pause and resume idempotent when the workflow crosses time, human review, or external side effects

## Workflow

### 1. Frame the Real Job

Pin down:
- what the workflow is trying to accomplish
- what the unit of work is
- whether the task is deterministic, branching, open-ended, or time-spanning
- what evidence would prove the design is good enough

If the user is still vague, design the workflow around the narrowest stable job-to-be-done instead of the grand vision.

### 2. Choose the Minimum Viable Primitive

Before proposing agents, decide whether the job should be:
- `prompt`
- `instruction`
- `skill`
- `single agent`
- `multi-agent`
- `hook` or deterministic guardrail

Use [pattern-selection.md](./references/pattern-selection.md) when the escalation boundary is unclear.

Default rule:
- if one role with one context window and one tool surface can do the work, stay single-agent
- escalate only when branching, tool overload, context overload, ownership transfer, or pause and resume make the simpler design brittle

### 3. Select the Loop Pattern

Choose the smallest pattern that matches the job:
- `prompt chain`
  - for fixed sequential stages with validation between steps
- `router`
  - for input-dependent branching
- `greedy bounded macro-packet loop`
  - for recurring prompt-driven work where one automation or owner should greedily push one bounded packet through a real boundary each wake-up
- `planner-executor-reviewer`
  - for dynamic task decomposition plus explicit review
- `orchestrator-workers`
  - for one front door coordinating multiple bounded workers
- `evaluator-optimizer`
  - for refine-until-threshold workflows with a stable rubric
- `handoff`
  - for ownership transfer to a specialist
- `wake-up or re-entry`
  - for long-running work with checkpoints, external waits, or human approval

If more than one pattern seems necessary, compose them intentionally and name the seam between them.
Do not hide a second pattern inside vague prose.

### 3a. Greedy Bounded Macro-Packet Loop

Use this pattern when:
- one automation or agent wakes up on a cadence
- the user wants high autonomy and visible progress, not micro-task theater
- long-running work may outlive one turn
- the workflow needs durable, human-readable artifacts for re-entry

Design it around these fields:
- `hourly_objective` or `current_objective`
- `primary_mission`
- `target_boundary`
- `success_evidence`
- `candidate_macro_packet`
- `exact_refuse_boundary`
- `next_reentry_command`

Default chain:
1. `proposal synthesis`
   - only when the next action is not already forced by a live run, closeout duty, or frozen active packet
   - generate 2-3 adjacent candidate macro packets, not a long backlog
2. `proposal critique and tighten`
   - select or tighten one packet until command, artifact path, and proof surface are exact
3. `execution routing`
   - decide whether the packet should stay local, go to validation, launch, close out, or stop on an exact refusal
4. `delivery execution`
   - push the chosen packet through the highest-value natural boundary available this turn
5. `brief and notes`
   - write the smallest durable artifact that preserves the new truth for the next wake-up

Key rules:
- one wake-up owns one primary mission; do not split the same still-advancing object into multiple pseudo-complete turns
- within that mission, allow a short `mission ladder` of 2-4 same-mission steps when each step only unlocks the next one
- if the packet reaches `launch`, stop at a launch receipt plus recall contract; do not mix `harvest` into the same completion claim unless the run already finished
- treat `exact_refuse_boundary` as the end of the mission only after same-mission fallbacks have been exhausted
- if the packet cannot cross the target boundary honestly, emit an `exact_refuse_boundary` with the missing proof and the next exact command
- multi-agent divergence belongs mainly in bounded proposal generation or critique; keep execution ownership single-threaded unless there is a real boundary split

### 4. Design State, Ownership, and Boundaries

Define:
- who owns the workflow at each stage
- which context each agent sees
- what state is ephemeral
- what state must be externalized
- what side effects need approval, serialization, or idempotency

Externalize at least the fields that affect control flow, for example:
- `goal`
- `active_owner`
- `plan`
- `work_item`
- `target_boundary`
- `success_evidence`
- `exact_refuse_boundary`
- `checkpoint_id`
- `prompt_pack_id`
- `prompt_pack_version`
- `prompt_quality_status`
- `prompt_regression_results`
- `prompt_revision_count`
- `quality_status`
- `approval_status`
- `trace_ref`

Use [prompt-contracts.md](./references/prompt-contracts.md) when you need concrete schemas or handoff fields.
Use [prompt-reliability.md](./references/prompt-reliability.md) when prompt drift, fragmentation, weak stop rules, or repeated contract failures suggest that the loop needs prompt refinement by design.

### 5. Write the Prompt Contract Pack

For each node or role, specify:
- mission
- allowed inputs
- allowed tools
- output schema
- stop rule
- escalation rule
- side-effect rule

Do not write agent prompts as broad persona essays.
Write them as operational contracts another agent can actually follow.

For recurring prompt-driven automations, prefer a three-layer prompt surface:
- `fixed guardrails`
  - minimal, stable, non-self-modifiable rules
- `task body`
  - the current recurring mission, startup snapshot, macro-packet rules, and output contract
- `active artifacts`
  - the current control plane, stage packet, pending ledger, and most recent decision notes

Keep the entry prompt thin:
- reading order
- fixed stop conditions
- which repo-local surfaces define the live truth
- which skills or helper lanes are preferred

For recurring work, prefer one short natural-language control note that makes these three things explicit:
- what the mission is
- what counts as real completion
- which same-mission fallbacks should happen before stopping

If prompt refinement is in scope, also specify:
- failure signature
- refinement trigger
- refiner input packet
- prompt regression cases
- prompt approval and rollback rule

### 5b. Design Prompt Reliability

Only add this lane when prompt quality is part of the workflow bottleneck.

Pin down:
- what the prompt failure signature is
  - ambiguity, scope drift, controller micromanagement, schema failure, tool misuse, stale state conflict, or prompt injection exposure
- what should trigger refinement
  - repeated schema failures, repeated low-confidence routing, evaluator finding prompt underspecification, or repeated fragmentation with no gain
- who rewrites the prompt and with what boundary
  - usually delegate actual rewrite work to `thinking-lenses`, but keep ownership, evaluation, and approval here
- how prompt changes are evaluated
  - rubric, regression cases, threshold, max prompt revisions, and plateau rule
- how prompt changes are governed
  - versioning, approval, rollback, and whether prompt changes can happen automatically or require a human gate

Use [prompt-reliability.md](./references/prompt-reliability.md) when you need a concrete checklist for this lane.

### 6. Add Evaluation and Close Loop Logic

For every workflow, define:
- what gets measured
- who evaluates it
- whether the evaluator can block, revise, or only comment
- what threshold ends the loop
- what trace or log is kept for debugging

Use [eval-close-loop.md](./references/eval-close-loop.md) when designing evaluator-optimizer or reviewer loops.

### 7. Stress Test the Design

Check the design against [failure-modes.md](./references/failure-modes.md).
At minimum ask:
- will routing confidence ever be too low for automatic action
- can the controller become a bottleneck
- can two agents believe they both own the same turn
- can the loop continue forever
- can pause and resume duplicate side effects
- can untrusted text leak into trusted instructions
- can the prompt itself cause task fragmentation, silent scope growth, or schema drift
- can prompt edits change the job instead of improving execution reliability
- will the workflow reward documentation churn instead of boundary crossing
- does the prompt force tiny steps when a larger bounded packet could finish this turn
- is the artifact surface readable enough that a human or later run can resume without replaying the whole chat

Shrink the design if a smaller pattern solves the same problem more safely.

## Recommended Response Shape

When using this skill, prefer this structure:

1. `Task frame`
2. `Minimum viable primitive`
3. `Recommended topology`
4. `Loop pattern`
5. `Macro packet contract`
6. `State and ownership model`
7. `Artifact surface`
8. `Prompt contract pack`
9. `Prompt quality and refinement plan`
10. `Evaluation and stop rules`
11. `Risks and next experiment`

## Prompt Refinement Boundary

- use `thinking-lenses` when the job is to rewrite or tighten a prompt directly
- stay in this skill when prompt quality is part of the workflow design problem
  - routing ambiguity
  - controller bloat
  - handoff packet drift
  - repeated schema violations
  - state and prompt disagreement
- treat `thinking-lenses` as the rewrite engine, not the owner of workflow topology, approval policy, or prompt change governance

## Adjacent Skills

- use `agent-systems-architecture` when the design question expands into memory layers, tool permissions, autonomy policy, or auditability across the whole system
- use `thinking-lenses` after this skill when one chosen prompt or prompt packet now needs a bounded rewrite
- use `execution-router` after this skill when the workflow is designed and the next question is how to run it in this environment
- use `source-to-skill` when blogs, docs, or transcripts should be distilled into additional reusable loop patterns

## Example Triggers

- `Design a multi-agent workflow for research planning, execution, review, and resume-after-human-feedback.`
- `Should this stay single-agent or split into planner, worker, and reviewer loops?`
- `Help me design prompt contracts and typed state for an orchestrator-workers system.`
- `Create a wake-up or re-entry loop for long tasks that need checkpoints and approval gates.`
- `Design a self-improving agent workflow without allowing unbounded recursion.`
- `Help me figure out whether my agent loop needs better prompt contracts, a prompt refiner, or a simpler topology.`
- `Design a workflow where prompt changes are versioned, evaluated, and rolled back if they make the agent noisier.`
