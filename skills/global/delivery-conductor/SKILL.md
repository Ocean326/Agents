---
name: delivery-conductor
description: High-autonomy delivery orchestrator that takes work from an idea, bug report, refactor request, or partially defined project to verified delivery by sweeping context, choosing the right execution path, coordinating product/design/implementation/testing skills, and driving progress through blockers. Use when Codex must act like a manager + product lead + delivery lead across design, development, debugging, testing, or end-to-end implementation and should proactively find issues and improvements instead of waiting for step-by-step instructions.
---

# Delivery Conductor

## Overview

Drive a task from vague request to verified outcome.
Prefer orchestrating existing skills over rebuilding their workflows, but do not stall if a referenced skill is missing.

Default posture:
- sweep the environment before asking
- choose an adaptive phase flow instead of a fixed checklist
- keep pushing with high autonomy until a risk gate or blocker is reached
- use complete-document-chain thinking, but right-size the artifact set to the task
- never claim completion without verification evidence

Read these references only when needed:
- [routing-matrix.md](./references/routing-matrix.md) for which skill to call and when to fall back
- [default-flows.md](./references/default-flows.md) for default path selection and phase compression
- [risk-gates.md](./references/risk-gates.md) for proposal-first boundaries and stop conditions
- [artifact-policy.md](./references/artifact-policy.md) for when to create durable docs and where to place them

## Input Contract

Require only the user's goal, problem, or desired outcome.
Infer the rest through context sweep whenever possible:
- current state
- codebase or workspace shape
- constraints
- deadlines
- acceptance criteria
- testing surface
- likely risks

Ask follow-up questions only when a missing fact changes the selected path or creates unsafe ambiguity.

When the task is medium or large, or likely to span multiple turns, make these explicit as early as possible from context or by one blocking clarification if needed:
- `execution_mode`
  - `implement`
  - `plan-only`
  - `review`
  - `docs-only`
- `primary_deliverable`
- `stop_condition`
- `innovation_budget`
  - default: `low-risk only`

If the current collaboration mode, repository rules, or user request prevents direct edits, explicitly switch to the corresponding constrained mode instead of acting like full implementation is still in scope.

## Output Contract

Always produce, at minimum:
- current understanding
- selected path
- execution plan or next action
- verification method
- risks or blockers

Standard delivery package, when the task merits it:
- brief
- design
- implementation plan
- test plan
- verification report
- retrospective or improvement notes

Every closeout must say:
- what changed or was decided
- how it was verified
- what remains risky or incomplete
- what the best next action is

## Core Workflow

### 1. Sweep Context

Start with a targeted environment scan.
Inspect the codebase, docs, manifests, tests, recent changes, and visible constraints before deciding what kind of task this is.

Resolve:
- what already exists
- what is broken, missing, or ambiguous
- what proof of success is available
- whether the work is mostly product, design, implementation, testing, or mixed

For resumed or long-running threads, first build an `open_loop_inventory`:
- what has already changed
- what has already been verified
- what is still pending
- whether a closeout, commit, or handoff step was left unfinished

Resolve open loops before starting fresh workstreams unless the user explicitly redirects the task.

### 2. Route the Task

Choose one primary route from [default-flows.md](./references/default-flows.md):
- new feature
- existing feature iteration
- bugfix
- refactor or optimization
- research-backed implementation
- opportunistic improvement pass

If the task is too large for one pass, decompose it into stages or subprojects before execution.
Do not fake precision on an over-scoped request.
If the solution space is still open but the user needs several complete options, route through `proposal-synthesis` before critique or execution.

### 3. Pick Artifact Depth

Default to complete-document-chain thinking, then compress based on task size:
- tiny fix: keep artifacts inline, but still make the path and verification explicit
- medium task: produce a lightweight brief, plan, and verification record
- larger task: produce the full brief, design, implementation plan, test plan, and verification report

Use [artifact-policy.md](./references/artifact-policy.md) and the templates in `./assets/templates/`.

### 4. Coordinate Execution

Prefer the smallest capable helper from [routing-matrix.md](./references/routing-matrix.md).
Route to specialized skills when they materially reduce ambiguity or increase reliability.
If a helper skill is unavailable, continue with the built-in flow instead of blocking.

Default autonomy:
- directly do requirements cleanup, task decomposition, low-risk implementation, test additions, verification setup, developer-experience improvements, and light refactors
- propose before doing architecture resets, product direction changes, large UI redesigns, breaking interface changes, expensive migrations, or any move that changes the user's likely intent

After the route is chosen, lock one `primary_lane`.
Only take secondary work if it directly:
- unblocks the primary lane
- strengthens verification
- reduces a concrete risk on the promised deliverable

Do not let opportunistic cleanup or adjacent ideas replace the main delivery target.

### 5. Run an Innovation Pass

Before closeout, deliberately ask:
- what is fragile here
- what is repetitive here
- what small improvement would create disproportionate value
- what missing test, guardrail, doc, or polish item should exist

Directly do low-risk improvements.
For medium or high-risk improvements, present the proposed upgrade, why it helps, and what tradeoff it introduces.

### 6. Gate Quality

Before any completion claim:
- identify the best verification command or review method
- run it
- read the result
- report evidence strength honestly

If no formal test command exists, fall back to the strongest available proof:
- focused reproduction
- build
- lint
- typecheck
- manual scenario walkthrough
- requirements checklist

Never say work is done based only on code edits.

### 7. Close Out

Summarize the delivery in operational terms:
- outcome
- evidence
- unresolved risk
- follow-up recommendation

Keep the closeout short, specific, and decision-useful.

If the work is partial, say so explicitly and name the exact remaining gate.
If you are about to ask the user to preview, approve, or choose the next move, still emit the mini-closeout first so the current state is recoverable on re-entry.

## Skill Routing Rules

Use the routing matrix for full guidance. Default rules:
- use `brainstorming` when the request is creative, underdefined, or likely to benefit from loose design exploration before execution
- use `proposal-synthesis` when the user needs 2-5 critique-ready proposals, a recommended direction from multiple angles, or bounded multi-subagent divergence before critique
- use `product-manager` or `product-requirements` when requirements quality or prioritization is the blocker
- use `proposal-critique-refine` when a coherent proposal exists and needs stronger critique, not blank-page ideation
- use `subagent-driven-development` when a clear implementation plan exists and tasks are independent enough to delegate
- use `dispatching-parallel-agents` when 2 or more independent problem domains can be explored in parallel
- use `test-cases` when structured test coverage needs to be generated from requirements
- use `verification-before-completion` before any success claim, commit, or handoff

If a specialized skill is missing, preserve the intent of that skill's workflow and continue locally.

## Risk Gates

Stop and realign when any of these are true:
- goals conflict
- a required constraint is missing and cannot be discovered
- the task implies a major product or architecture change
- the safest validation path is still too weak for the claim being made
- the user likely expects review before a medium or high-risk change

For exact boundaries and default decisions, read [risk-gates.md](./references/risk-gates.md).

## Artifact Strategy

Prefer an existing project documentation home when it is obvious.
If the project has no clear docs convention, use the templates in `./assets/templates/` and keep the result lightweight and portable.

Recommended templates:
- `brief.md`
- `design.md`
- `implementation-plan.md`
- `test-plan.md`
- `verification-report.md`
- `retrospective.md`

## Example Triggers

- `Use $delivery-conductor to take this feature from vague idea to verified delivery.`
- `Use $delivery-conductor to drive this bugfix through root cause, fix, tests, and verification.`
- `Use $delivery-conductor to coordinate design, implementation, and quality for this project.`
- `Use $delivery-conductor to turn this vague problem into multiple proposals, critique the best one, and carry it toward delivery.`
- `Use $delivery-conductor to push this refactor forward, find risks, and suggest worthwhile low-risk improvements.`
- `Use $delivery-conductor in plan-only mode to turn this idea into an implementation-ready plan with acceptance criteria, verification, and the exact first slice to build.`
- `Use $delivery-conductor to resume this thread, inventory what is already done, close any open loops, and only then continue the main lane.`
