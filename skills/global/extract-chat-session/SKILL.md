---
name: extract-chat-session
description: "Extract memory, decisions, key outputs, and pending work from one or more Codex or Cursor chat session IDs, then continue execution in the current thread with a concrete next-step plan. Use when user says resume/continue session, hand over by chat id, recover context from old sessions, or asks to reconnect old conversations. When user asks to save/archive notes, invoke /compile-tech-notes and produce a local markdown artifact."
argument-hint: "[session-id ...] [current goal]"
---

# Extract Chat Session

## What This Skill Does

Turn one or more chat session IDs into a continuation packet that is immediately usable for implementation work in the current Codex thread.

Outputs include:
- recovered goals and constraints
- what is already completed
- open loops and pending steps
- workspace and artifact paths
- the next executable action set for the current thread

## When To Use

Use this skill when the request includes one or more of the following patterns:
- continue a prior Codex or Copilot chat by id
- continue a prior Cursor agent/composer chat by `requestId` or `composerId`
- recover memory or key points from old sessions
- resume long-running research/engineering tasks
- merge context from multiple sessions before continuing execution

## Procedure

1. Normalize the request.
- Collect target session IDs.
- Capture the current objective (what to do next, not just what to summarize).
- If objective is missing, infer from the newest session messages.

2. Harvest session evidence.
- For Codex sessions, inspect local artifacts under `~/.codex/`.
- Prefer rollout files in `~/.codex/sessions/**/rollout-<...>.jsonl`.
- Use `session_index.jsonl` and `history.jsonl` as supporting context.
- For Cursor sessions, inspect `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`.
- Prefer `cursorDiskKV` keys of the form `composerData:*` and `bubbleId:<composerId>:<bubbleId>`.
- Accept either:
  - a Cursor `composerId` directly, or
  - a Cursor `requestId` that appears inside a bubble payload
- Recover workspace, title, recent user/assistant messages, and any attached local artifact paths from bubble JSON plus decoded `conversationState` payloads when available.
- Use [extractor script](./scripts/extract_sessions.py) to build a concise packet.

3. Build a continuation packet per session.
- Required fields:
  - `provider`
  - `session_id`
  - `intent_summary`
  - `workspace_paths`
  - `completed_work`
  - `open_loops`
  - `known_artifacts`
  - `risks_or_unknowns`
  - `recommended_next_actions`
- Cursor packets should also expose:
  - `cursor_composer_id`
  - `matched_request_ids`
  - `chat_title`
- Keep claims evidence-backed; do not invent missing facts.

4. Merge packets (when multiple sessions are provided).
- Deduplicate repeated outcomes.
- Resolve conflicts by recency and evidence strength.
- Produce one merged execution lane with explicit assumptions.

5. Continue execution in current thread.
- Default behavior for Cursor is to continue in the current Codex thread after extraction; do not assume the user wants to jump back into Cursor UI.
- If the user asked for delivery, route with `$delivery-conductor` and execute.
- If remote compute is needed (for example 179 server), route with `$conductor-remote-long-task`.
- Keep verification explicit before completion claims.

6. Save mode (on user request).
- If user asks to save, archive, memo, or write notes, invoke `$compile-tech-notes`.
- Produce a local markdown artifact with:
  - scope and source session IDs
  - key decisions and evidence
  - completed work and pending tasks
  - execution checklist for next resume
- Use [save mode contract](./references/save-mode.md).

## Output Contract

Always return:
- session continuation packet(s)
- one merged next-step execution plan
- explicit assumptions and missing evidence

When save mode is requested, additionally return:
- local markdown path
- compact note abstract and action checklist

## Quality Checks

Before closeout, verify:
- each key claim maps to session evidence
- pending tasks are concrete and executable
- workspace paths are valid
- Cursor `requestId` or `composerId` resolves to exactly one recoverable chat lane, or ambiguity is stated explicitly
- no unresolved blocker is hidden inside summary prose

## References

- [save mode contract](./references/save-mode.md)
- [extractor script](./scripts/extract_sessions.py)
