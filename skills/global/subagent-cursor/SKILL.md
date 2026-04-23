---
name: subagent-cursor
description: Use local Cursor CLI as an external subagent through `cursor-agent` when the user explicitly wants Cursor, Claude 4.6/4.7, Cursor premium models, or a shell-driven second agent outside Codex native `spawn_agent`. Use for quick independent passes, external model comparison, or delegating a bounded prompt to local Cursor with model routing guidance and a safe default wrapper.
---

# Subagent Cursor

## Overview

Use local `cursor-agent` as an external subagent.
Prefer this skill when the user explicitly asks to use Cursor or specific Cursor-exposed models, or when a bounded second pass is useful and shell invocation is acceptable.

Keep the distinction explicit:

- `verified-now`: model/command was actually executed successfully on this machine
- `listed-only`: model appears in `cursor-agent models`, but was not re-executed in this skill creation pass

Do not claim account quota, billing tier, or future availability from a one-time local check.

## Quick Start

1. Confirm the CLI exists and the account is logged in.
2. Choose a model using the routing table below.
3. Use `scripts/run_cursor_subagent.sh` for a safe default call.
4. Default to read-only (`plan` or `ask`) unless the user clearly wants Cursor to edit or run commands directly.

Useful checks:

```bash
which cursor-agent
cursor-agent about
cursor-agent models
```

Safe default wrapper:

```bash
$CODEX_HOME/skills/subagent-cursor/scripts/run_cursor_subagent.sh \
  --model claude-4.6-sonnet-medium \
  --workspace /absolute/workspace/path \
  --mode plan \
  --prompt "Read the docs and summarize the main risks."
```

Streaming JSON wrapper:

```bash
$CODEX_HOME/skills/subagent-cursor/scripts/run_cursor_subagent.sh \
  --model auto \
  --workspace /absolute/workspace/path \
  --mode plan \
  --output-format stream-json \
  --stream-partial-output \
  --prompt "Write 20 short numbered lines and do not use tools."
```

Codex-friendly clean streaming:

```bash
$CODEX_HOME/skills/subagent-cursor/scripts/run_cursor_subagent.sh \
  --model auto \
  --workspace /absolute/workspace/path \
  --mode plan \
  --render assistant-text \
  --prompt "Return concise markdown with a summary and one next step."
```

Markdown envelope for copy/paste or subagent handoff:

```bash
$CODEX_HOME/skills/subagent-cursor/scripts/run_cursor_subagent.sh \
  --model auto \
  --workspace /absolute/workspace/path \
  --mode plan \
  --render md \
  --prompt "Return concise markdown with a summary and one next step."
```

Attach a Codex skill explicitly:

```bash
$CODEX_HOME/skills/subagent-cursor/scripts/run_cursor_subagent.sh \
  --model auto \
  --workspace /absolute/workspace/path \
  --mode plan \
  --skill $CODEX_HOME/skills/web-finder/SKILL.md \
  --prompt "Use the attached skill to choose the right search workflow."
```

## Verified Local Availability

These were verified on this machine during skill creation:

- CLI present: `/opt/homebrew/bin/cursor-agent`
- Alternate launcher example: `/absolute/path/to/cursor`
- Logged-in account visible via `cursor-agent about`
- `verified-now` models:
  - `claude-4.6-sonnet-medium`
  - `claude-opus-4-7-high`
  - `claude-opus-4-7-max`

Important clarification:

- `premium` is not a standalone CLI flag
- In Cursor CLI, premium capability is expressed by choosing a premium model, for example `claude-opus-4-7-max`

## Model Routing

Read [references/model-routing.md](./references/model-routing.md) when you need the full matrix.

Short routing rules:

- `auto`
  - Use for low-friction exploratory prompts when model choice is not important.
  - Treat as convenience-first, not as a reproducible research setting.

- `claude-4.6-sonnet-medium`
  - Use for fast, strong general reasoning, drafting, lightweight code reading, concise critique, and doc synthesis.
  - Best default when the user explicitly wants Claude but the task is not the hardest one.

- `claude-opus-4-7-high`
  - Use for deeper specification critique, architecture tradeoffs, research framing, and longer-form reasoning.
  - Good “serious second opinion” default.

- `claude-opus-4-7-max`
  - Use for the hardest high-value prompts where premium latency/cost is justified.
  - Prefer for dense proposal critique, research synthesis, subtle tradeoff analysis, or very important writing.

- `gpt-5.x` and `gpt-5.x-codex-*`
  - Use when the user wants Cursor specifically but the task is code-heavy, implementation-oriented, or repository-sensitive.
  - Keep in mind that if Codex itself is already doing the implementation, Cursor should be used only for an independent pass or bounded sidecar, not duplicate work.

- `composer-*`
  - Use for generic Cursor-native flows when strict model reproducibility is not important.
  - `auto` often lands near this family.

- `gemini-*`, `grok-*`, `kimi-*`
  - Treat as optional alternates visible in the account.
  - Use only when the user explicitly wants cross-model comparison or one of these families.

## Recommended Invocation Pattern

Prefer a bounded prompt with:

- one concrete task
- one workspace
- one requested output shape
- no hidden expected answer

Good pattern:

```text
Read these docs and return:
1. top 3 risks
2. missing assumptions
3. one recommended next step
Do not edit files.
```

Avoid:

- open-ended “solve the whole project”
- overlapping implementation with current Codex work
- passing your intended answer and then calling the result “independent”

When reusing Codex skills with Cursor:

- pass the relevant `SKILL.md` file explicitly through `--skill`
- treat the skill as attached instructions, not as a native auto-triggered capability
- keep the task bounded so Cursor can actually follow the attached workflow

## Safety Defaults

The wrapper script defaults to:

- `--print`
- `--trust`
- explicit `--workspace`
- `--mode plan`

This keeps Cursor in a read-only planning posture unless you intentionally relax it.

When true streaming is helpful but raw JSON noise is not:

- use `--render assistant-text` to keep live assistant text while stripping the `stream-json` envelope
- use `--render md` to emit a compact Markdown wrapper with the streamed response plus a small run-metadata footer
- keep `--render raw` only when you explicitly need the original Cursor event stream for debugging or custom tooling

If the user truly wants Cursor to perform edits or commands:

- either omit `--mode`
- or call `cursor-agent` directly with the needed arguments

Be explicit when escalating from read-only to write-capable execution.

## Resources

### `scripts/run_cursor_subagent.sh`

Use this wrapper for consistent local invocation.
It supports:

- `--model`
- `--workspace`
- `--mode`
- `--skill` repeatably
- `--output-format`
- `--stream-partial-output`
- `--render`
- `--prompt`

### `references/model-routing.md`

Read this when:

- deciding between `auto`, Claude, premium, GPT/Codex, Composer, Gemini, Grok, or Kimi
- you need to remember which models are `verified-now` versus `listed-only`
- you want a quick task-to-model routing table
