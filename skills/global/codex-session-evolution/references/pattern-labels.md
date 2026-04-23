# Pattern Labels

Use these labels to keep historical review packets comparable.

| Label | Use when | Typical route hint |
| --- | --- | --- |
| `exploration-heavy` | Search or tool exploration dominates before a stable plan emerges | `workflow` |
| `verification-thin` | The session changes artifacts but shows weak verification evidence | `workflow` |
| `closeout-weak` | The session ends without a strong closeout, risk note, or clear next step | `workflow` |
| `resume-fragile` | Resumed work loses prior context or fails to rebuild the open-loop inventory | `workflow` |
| `tool-overkill` | Tool fan-out grows beyond what the task seems to need | `workflow` |
| `prompt-ambiguity` | The likely issue is route wording, trigger ambiguity, or underspecified guardrails | `prompt` |
| `skill-overlap` | Two skills appear to own the same job or the wrong skill is repeatedly chosen | `skill_patch` |
| `candidate-ready` | The packet already supports a small, attributable improvement proposal | route by candidate type |

## Labeling Rules

- Prefer `1-3` labels per packet.
- Use repeated labels consistently across batches.
- Keep heuristic labels and manual labels separate when possible.
- Add `candidate-ready` only when the packet can already support a bounded next action.
