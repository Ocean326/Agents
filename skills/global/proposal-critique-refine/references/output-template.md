# Critique-Refine Memo Template

Use this template for the final artifact.
Keep it concise and decision-oriented.

## 1. Proposal Brief

Rewrite the proposal faithfully in at most 12 bullets.
Do not invent a larger proposal than the user supplied.

## 2. Review Stance

State:

- `default_or_requested`: `neutral` or the user-requested preference profile
- `active_overlays`: list the overlays actually applied, if any
- `how_priority_shifted`: 1-3 bullets on how issue ordering or repair direction changed

## 3. Round Summary

For each round, include:

- `round`
- `lenses_used`
- `major_issues_found`
- `repairs_attempted`
- `verification_result`
- `continue_or_stop`

## 4. Issue Register Snapshot

List the active and most important resolved issues with:

- `id`
- `round`
- `lens`
- `issue`
- `severity`
- `confidence`
- `status`

## 5. Repairs Applied

List the targeted repairs worth keeping.
Map them to issue ids when possible.
If a preference overlay was active, note how the repair direction reflected it.

## 6. Residual Risks

Keep only risks that still matter after the final round.
Separate:

- `needs evidence`
- `accepted risk`
- `still unresolved`

## 7. Preserved Disagreements

Keep only disagreements that still matter after repair.
Label them as one of:

- `empirical uncertainty`
- `value conflict`
- `scope ambiguity`

## 8. Final Recommendation

Choose exactly one:

- `proceed`
- `revise`
- `de-scope`
- `test`
- `pause`
- `stop`

Add 1-3 sentences explaining why this is the most honest move.

## 9. Next-Step Artifact

Choose one:

- revised proposal
- experiment plan
- decision memo
- risk register
- research brief
- implementation plan

Add 1-3 sentences on what that artifact should contain.

## 10. Why This Pass Stops Here

State the stopping reason explicitly:

- configured round limit reached
- no materially new high-severity issues appeared
- further critique is becoming repetitive
- missing evidence blocks stronger judgment
- remaining disagreement is non-analytical
