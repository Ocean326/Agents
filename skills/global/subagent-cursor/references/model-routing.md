# Cursor Model Routing

## Status Legend

- `verified-now`: actually executed successfully on this machine
- `listed-only`: visible in `cursor-agent models` during skill creation, but not re-executed in this pass

## Local Availability Snapshot

### CLI and account

| item | status | notes |
| --- | --- | --- |
| `cursor-agent` binary | `verified-now` | `/opt/homebrew/bin/cursor-agent` |
| `cursor` launcher | `example-path` | `/absolute/path/to/cursor` |
| account login | `verified-now` | Account visible via `cursor-agent about` |

### Models verified by execution

| model id | status | best fit |
| --- | --- | --- |
| `claude-4.6-sonnet-medium` | `verified-now` | fast doc synthesis, lightweight repo reading, concise critique |
| `claude-opus-4-7-high` | `verified-now` | stronger reasoning, proposal critique, architecture and research discussion |
| `claude-opus-4-7-max` | `verified-now` | premium deep reasoning for highest-value prompts |

### Model families visible in `cursor-agent models`

| family | status | notes |
| --- | --- | --- |
| `auto` | `listed-only` | convenience route; model may vary |
| `composer-*` | `listed-only` | Cursor-native default family |
| `gpt-5.4-*`, `gpt-5.2-*`, `gpt-5.1-*` | `listed-only` | strong general and coding options |
| `gpt-5.x-codex-*` | `listed-only` | implementation-leaning code tasks |
| `claude-4.6-*` | `listed-only` except one verified | includes Sonnet and Opus variants |
| `claude-opus-4-7-*` | `listed-only` except two verified | premium Claude 4.7 family |
| `claude-4.5-*`, `claude-4-*` | `listed-only` | older Claude families |
| `gemini-*` | `listed-only` | alternate comparison family |
| `grok-*` | `listed-only` | alternate comparison family |
| `kimi-*` | `listed-only` | alternate comparison family |

## Premium Clarification

`premium` is not exposed as a separate CLI switch.
Treat premium access as “choose a premium model id”.

Locally verified premium example:

- `claude-opus-4-7-max`

Do not infer remaining quota or billing entitlement from local model visibility alone.

## Simple Task Routing

| task shape | recommended model | why |
| --- | --- | --- |
| quick second opinion on docs/spec | `claude-4.6-sonnet-medium` | good balance of speed and reasoning |
| architecture critique or research framing | `claude-opus-4-7-high` | stronger deep reasoning without always paying max latency |
| hardest prompt, premium justified | `claude-opus-4-7-max` | best for dense, important thinking |
| generic Cursor use, user does not care | `auto` | lowest friction |
| cross-model comparison versus Claude | one `gpt-5.x` or `gpt-5.x-codex-*` model | gives a different model family perspective |
| code-heavy bounded sidecar in Cursor | `gpt-5.x-codex-*` or `gpt-5.4-*` | stronger coding orientation |
| explicitly test a non-Claude family | `gemini-*`, `grok-*`, `kimi-*` | only when comparison itself is the goal |

## Good Prompt Shapes

If the task should reuse a Codex skill, attach the skill file through the wrapper:

```bash
run_cursor_subagent.sh \
  --model auto \
  --workspace /abs/workspace \
  --mode plan \
  --skill $CODEX_HOME/skills/web-finder/SKILL.md \
  --prompt "Use the attached skill and summarize the best search lane."
```

Treat attached skills as explicit prompt context, not as a native skill runtime.

### Planning pass

```text
Read these files and return:
1. top risks
2. hidden assumptions
3. best next step
Do not edit files.
```

### Review pass

```text
Review this design note as a skeptical collaborator.
Prioritize bugs, regressions, unclear assumptions, and missing tests.
Do not rewrite the whole proposal.
```

### Bounded implementation pass

```text
In this workspace, make only the requested change in the named file.
Report what changed and any residual risk.
```
