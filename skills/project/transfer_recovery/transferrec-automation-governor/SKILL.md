---
name: transferrec-automation-governor
description: Thin governor for the Transfer_Recovery mainline automation loop. Use when the task is recurring experiment control, state transition, ledger/docs/memory closeout, or handoff recovery. Do not use for open-ended method ideation or historical batch review.
---

# TransferRec Automation Governor

Use this skill when the work is:

- recurring automation on the active Transfer_Recovery mainline
- manual recovery of an interrupted automation loop
- state classification and one-step experiment governance
- ledger, docs, and memory synchronization after a run-state change

Do not use this skill for:

- broad research ideation
- historical rollout review
- prompt polishing unrelated to the active mainline
- expanding parameter matrices without an explicit keep/stop/turn decision

## Primary Goal

Keep the controller focused on one active mainline and one bounded action per round, while keeping `179` evidence, the active run ledger, 0417 docs, and automation memory aligned.

## Evidence Order

Always resolve conflicts in this order:

1. `179` latest JSON / log / process
2. current active run ledger
3. 0417 main docs
4. automation memory
5. current prompt or prior assumptions

Never let stale docs, stale memory, or a stale prompt override live `179` evidence.

## State Machine

Classify the round into exactly one state before broad probing:

- `A = live mainline sync`
- `B = completed harvest`
- `C = next mainline launch`
- `D = incident / handoff`

If the state is unclear, spend the first tool budget resolving the state. Do not start with wide exploration.

## Allowed Actions

For each state, authorize exactly one bounded worker action:

- `A -> live_sync`
  - probe `179`
  - update active ledger
  - minimally sync queue/live docs
  - refresh memory

- `B -> result_harvest`
  - extract final metrics
  - update ledger
  - update 0417 docs
  - make one keep/stop/turn decision

- `C -> launch_prep`
  - write pending ledger with goal, control, single variable, success criteria, stop rule, command, artifact path
  - launch one next run only after the ledger exists

- `D -> incident_probe`
  - record exact time, machine, SSH path, PID, log path, last refresh time, attempted actions, current judgment
  - leave one concrete first command for the next round

## Hard Guardrails

- Maintain exactly one active mainline.
- Do not start a new formal batch in state `A` or `D`.
- Do not treat Lenovo smoke as accepted evidence.
- Do not backfill formal tables before `179` evidence is sufficient.
- Do not reopen an old parameter matrix without an explicit prior decision.
- Do not bring `codex-session-evolution` into the normal hourly loop.

## Skill Routing

- default owner: `delivery-conductor`
- use `research-router` only if state classification is genuinely ambiguous after snapshot
- use `proposal-critique-refine` only when revising the workflow, prompt, or this skill itself
- reserve `codex-session-evolution` for offline governance audits

## Output Contract

Every run should close with:

1. current state summary
2. actions actually taken
3. evidence vs inference
4. files updated
5. next handoff with the first command

If no new results are available, still leave a recoverable handoff.
