---
name: codex-session-evolution
description: Review historical Codex sessions in `~/.codex/session_index.jsonl`, `~/.codex/history.jsonl`, and `~/.codex/archived_sessions/rollout-*.jsonl` to discover recurring workflow, prompt, and skill issues across past conversations. Use when Codex needs to turn archived session evidence into sanitized review packets, cross-session pattern summaries, and bounded workflow or skill improvement proposals without copying raw private logs into durable memory. Prefer this skill for historical or cross-session retrospectives; for current-thread-only skill retrospectives use `$skill-skill-usage-close-loop` instead.
---

# Codex Session Evolution

## Overview

Review historical Codex evidence safely, then turn that evidence into small, auditable improvement candidates for workflows, prompts, and skills.
Use this skill as the missing ingress layer before scorecard or optimizer flows, not as a replacement for them.

Read these references only when needed:

- `references/route-matrix.md` for lane selection and handoff rules
- `references/review-packet-contract.md` for packet, candidate, and decision shapes
- `references/pattern-labels.md` for reusable labels and route hints

## Boundaries

- Keep raw session logs machine-local.
- Distill sessions into observation and inference packets; do not paste large transcript blocks into durable memory.
- Treat rollout files as event and state-transition evidence, not just message history.
- Prefer candidate snapshots and suggest-first patch proposals over direct canonical skill rewrites.
- Do not promise automatic thread-to-rollout mapping. If mapping is unclear, work from explicit rollout files or user-confirmed batches.

## Quick Route

- Use this skill when the ask spans multiple past sessions, archived rollouts, or recurring patterns across history.
- Use `$skill-skill-usage-close-loop` when the user only wants a current-thread skill retrospective.
- Use `$skill-skill-scorecard` or `$skill-skill-optimizer-darwin` after this skill produces enough evidence for one bounded skill change.
- Use `$proposal-critique-refine` when the candidate improvement is substantial, contested, or still fuzzy after aggregation.

## Workflow

### 1. Inventory the history surface

- Run `scripts/inventory_codex_history.py` to inspect recent thread index rows, history snippets, and rollout files.
- Build a bounded batch; default to `3-5` sessions.
- Mix success cases and failure-prone cases when possible.

### 2. Select one review lane

- `pilot-batch`
  - Use when this is the first pass and the goal is to discover recurring patterns.
- `workflow-targeted`
  - Use when the likely improvement area is orchestration, verification, closeout, routing, or resume behavior.
- `skill-targeted`
  - Use when one or two named skills appear implicated across history.
- `prompt-targeted`
  - Use when the likely issue is route wording, guardrails, or task framing rather than workflow sequence.

Keep one primary lane per batch. Do not let one batch try to fix workflow, prompts, and multiple skills at the same time.

### 3. Build one review packet per rollout

- Prefer explicit rollout files under `~/.codex/archived_sessions/`.
- Run `scripts/build_review_packet.py --rollout-file ... --output ...`.
- Keep task snippets off by default. Add them only when necessary and safe.
- Separate observations from inferences.
- Fill the packet's manual fields:
  - `task_summary`
  - `successes`
  - `failures`
  - `pattern_labels`
  - `candidate_cues`
  - `route_override`
  - `next_action`

### 4. Aggregate across packets

- Run `scripts/aggregate_review_packets.py packet-1.json packet-2.json ...`.
- Look for recurring labels, tool patterns, and route cues.
- Promote only repeated or decision-relevant issues. Do not treat one bad session as canonical truth.

### 5. Generate bounded candidates

- For workflow issues, propose the smallest workflow guardrail or sequence change that addresses the pattern.
- For prompt issues, create candidate versions with representative inputs and explicit evaluation criteria.
- For skill issues, produce a suggest-first patch proposal or route to scorecard and optimizer flows.
- Keep each candidate attributable to packet ids or rollout files.

### 6. Route the follow-up

- Route `workflow` candidates to the owning workflow skill or a small decision memo.
- Route `prompt` candidates to a bounded evaluation pass before keeping them.
- Route `skill_patch` candidates to `$proposal-critique-refine` first when the repair shape is still ambiguous, then to `$skill-skill-scorecard` or `$skill-skill-optimizer-darwin`.
- Route weak or noisy evidence to `defer` and stop honestly.

## Output Contract

Produce, at minimum:

- one bounded review batch definition
- one sanitized review packet per selected rollout
- one aggregate pattern summary
- the top `1-3` candidates, each with:
  - candidate type
  - evidence refs
  - why it matters
  - proposed route
  - evaluation plan

When working inside PersonalBrain, prefer writing only sanitized `source` and `output` pages. Keep raw rollout files outside durable memory.

## Script Notes

- `scripts/inventory_codex_history.py`
  - Inventory the three main Codex history surfaces without assuming they already map cleanly to each other.
- `scripts/build_review_packet.py`
  - Build a sanitized packet from one rollout file and keep raw snippets optional.
- `scripts/aggregate_review_packets.py`
  - Count recurring labels and suggest the smallest candidate directions worth advancing.

## Quality Checks

- Keep the batch bounded.
- Keep raw logs local.
- Keep observations separate from inferences.
- Keep candidates small and attributable.
- Keep direct canonical rewrites out of this skill unless the user explicitly changes the task.

## Common Mistakes

- Treat a current-thread retrospective as a historical batch review.
- Paste raw transcript blocks into durable notes.
- Assume `session_index.jsonl` ids and rollout ids are the same object.
- Rewrite multiple skills before one candidate has been evaluated.
- Rewrite prompts based on vibes instead of repeated evidence.
