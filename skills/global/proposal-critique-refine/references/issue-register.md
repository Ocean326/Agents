# Issue Register

Use this file when recording critique findings.
Default to an issue register, not a numeric scorecard.

## Record Shape

Each issue should contain:

- `id`: short stable identifier such as `I1`, `I2`
- `round`: which round surfaced or re-opened the issue
- `lens`: which critique lens raised it
- `issue`: short statement of the problem
- `why_it_matters`: consequence if ignored
- `priority_note` (optional): why this issue is especially important under the current neutral baseline or active preference overlay
- `evidence_type`: `user-provided`, `source-backed`, `inference`, or `assumption`
- `evidence_note`: the concrete fact, quote, source, or reasoning basis
- `severity`: `low`, `medium`, `high`, `critical`
- `confidence`: `low`, `medium`, `high`
- `suggested_repair`: the smallest meaningful fix
- `status`: `open`, `patched`, `accepted-risk`, or `rejected-critique`

## Status Meanings

- `open`
  The issue is live and has not been addressed.
- `patched`
  The proposal changed in a way that addresses the issue well enough for this pass.
- `accepted-risk`
  The issue remains real, but the proposal can proceed with explicit acknowledgment.
- `rejected-critique`
  The critique was judged weak, misapplied, or outside scope.

## Rules

- Record only the most decision-relevant issues.
- Prefer 3-5 issues for a normal round.
- If a critique is interesting but weakly supported, record it with low confidence rather than inflating certainty.
- If multiple lenses raise the same issue, merge them into one entry and note the supporting lenses.
- Do not mark an issue `patched` unless the proposal actually changed or the critique was directly answered.
- If a later round reopens an issue, keep the same `id` and update the `round` plus status rather than creating a duplicate.
- If a user preference changes the issue ordering, explain that in `priority_note` without inflating `severity`.

## Round Use

- After critique:
  open new issues and merge duplicates
- After improve:
  update `suggested_repair` and note what changed
- After verify:
  mark each issue as `patched`, `open`, `accepted-risk`, or `rejected-critique`

## When to Escalate

Escalate from a normal pass to a stronger warning when:

- an issue is `critical`
- the proposal depends on a missing fact that would flip the decision
- the proposal creates uneven downside for a specific stakeholder group
- the critiques expose a fundamental mismatch between the proposal and the stated goal
- later rounds keep reopening the same high-severity issue
