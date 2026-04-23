# Deliverable Taxonomy

Use this reference to choose one primary deliverable before writing.
Do not mix three half-finished document types into one draft.

## Rule of one primary deliverable

Pick one primary deliverable based on the user's real question, reader, and time window.
Secondary artifacts are allowed only when they directly support the primary deliverable.

Examples:

- A meeting recap may include a short situational summary, but the primary deliverable is still `meeting-secretary-memo`.
- A feasibility brief may include a compact source map appendix, but the primary deliverable is still `feasibility-brief`.
- A learning note may include a checklist, but the primary deliverable is still `systematic-learning-note`.

## Deliverable chooser

| Deliverable | Use when | Core question | Must include | Common failure mode |
| --- | --- | --- | --- | --- |
| `task-status-update` | The user wants a work summary, progress report, or task record | What changed, what is blocked, and what happens next? | progress, evidence, blockers, next actions | activity log with no decision value |
| `meeting-secretary-memo` | The source anchor is a meeting, call, sync, or transcript | What was decided, who owns what, and what remains open? | summary, decisions, action items, owners, open questions | replaying the meeting instead of extracting decisions |
| `feasibility-brief` | The user needs a recommendation, pre-research, or “should we do this” brief | Is this worth pursuing, under what constraints, and why? | scope, options, evidence, risks, recommendation | fake certainty from thin evidence |
| `material-digest` | The user has many links, docs, screenshots, or raw materials that need整理汇总 | What do these materials collectively say, and what matters most? | source map, grouped themes, signal vs. noise, gaps | link dump with weak synthesis |
| `systematic-learning-note` | The goal is re-study, internal knowledge reuse, or technical concept consolidation | What should the reader understand well enough to revisit later? | central question, early answer, structure, mechanisms, tradeoffs, next-use hints | pretty summary with low future reuse |
| `blog-style-synthesis` | The user wants a more public-facing article or shareable technical piece | What reusable insight is worth sharing broadly? | strong narrative, evidence, reader payoff, clear through-line | smoothing uncertainty into polished prose |

## Lightweight decision tree

1. If the input is mainly a workstream or project checkpoint, choose `task-status-update`.
2. If the input is mainly a meeting or call record, choose `meeting-secretary-memo`.
3. If the user is asking “whether / why / under what conditions,” choose `feasibility-brief`.
4. If the input is many materials and the user first needs整理与提炼, choose `material-digest`.
5. If the goal is durable technical understanding, choose `systematic-learning-note`.
6. If the goal is broader sharing and the evidence is already strong, choose `blog-style-synthesis`.

## Secondary mode hints

These are allowed pairings when helpful:

- `material-digest` -> `feasibility-brief`
  Use when the materials need compression before a recommendation can be made.

- `material-digest` -> `systematic-learning-note`
  Use when scattered sources first need synthesis before becoming a durable note.

- `meeting-secretary-memo` -> `task-status-update`
  Use when the meeting directly changes current work priorities.

- `systematic-learning-note` -> `blog-style-synthesis`
  Use only when the note is already evidence-strong and the user explicitly wants shareability.

## Downgrade rules

If evidence is weak, downgrade instead of over-writing:

- `task-status-update` -> `checkpoint-only`
- `meeting-secretary-memo` -> `action-register-only`
- `feasibility-brief` -> `options-and-gaps memo`
- `material-digest` -> `source-map-plus-gaps`
- `systematic-learning-note` -> `source-map-plus-gaps`
- `blog-style-synthesis` -> `systematic-learning-note`
