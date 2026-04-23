# Route Matrix

## Use This Skill vs Nearby Skills

| Situation | Preferred skill | Why | Typical output |
| --- | --- | --- | --- |
| Review one or more skills used in the current thread | `$skill-skill-usage-close-loop` | Keep the main task unblocked and log passive evidence | usage review rows |
| Review archived Codex sessions across history | `$codex-session-evolution` | Build the missing ingress layer from raw history to reusable evidence | review packets and candidates |
| Score one known skill change | `$skill-skill-scorecard` | Compare one skill against the shared rubric | score row and recommendation |
| Optimize one known weak skill | `$skill-skill-optimizer-darwin` | Make one bounded repair and rescore | keep or revert decision |
| Stress-test or reshape a non-trivial candidate | `$proposal-critique-refine` | Improve the proposal before canonical edits | critique-refine memo |

## Default Historical Pass

1. Inventory the history surfaces.
2. Pick `3-5` archived rollouts.
3. Build one review packet per rollout.
4. Aggregate packets.
5. Pick the top `1-3` candidate directions.
6. Critique any non-trivial candidate before editing canonicals.
7. Route one candidate at a time downstream.

## Design Principles

- Treat session history as state evidence, not just chat text.
- Prefer event, tool, and transition cues over long transcript summaries.
- Keep raw logs machine-local.
- Keep candidate changes versioned and reversible.
- Promote only repeated or clearly decision-relevant patterns.

## Stop Conditions

- Stop when the next move depends on evidence you do not yet have.
- Stop when the batch no longer stays bounded.
- Stop when the likely improvement is current-thread-only and should move to the close-loop skill instead.
- Stop when the candidate is still too ambiguous to route cleanly.
