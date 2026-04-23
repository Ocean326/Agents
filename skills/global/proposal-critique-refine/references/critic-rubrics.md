# Critique Lenses

Use this file when choosing critique lenses for `proposal-critique-refine`.
Pick 3 lenses by default. Choose deliberately different viewpoints; do not pick 3 variants of the same concern.

Reuse the same lenses across rounds unless a materially new risk class appears.

Default to a neutral stance unless the user explicitly asks for a preference overlay.
If a preference is requested, also read [preference-overlays.md](./preference-overlays.md).

## Shared Output Shape

Each lens should return:

- `strongest_concern`
- `what_still_works`
- `assumption_under_attack`
- `why_this_matters_now`
- `evidence_that_would_change_the_view`
- `concrete_repair_direction`
- `severity`: `low`, `medium`, `high`, `critical`
- `confidence`: `low`, `medium`, `high`
- `evidence_type`: `user-provided`, `source-backed`, `inference`, or `assumption`

Each lens should be constructive, not merely harsh.
Do not emit generic criticism without mechanism, consequence, and repair direction.

## Default Lens Sets

### Product, feature, or workflow proposal

- `value-user`
  Focus on usefulness, adoption friction, differentiation, and whether the proposal solves a real problem.
- `execution-feasibility`
  Focus on dependencies, complexity, operational burden, sequencing, and failure to ship.
- `risk-edge-case`
  Focus on failure modes, ambiguous behavior, abuse paths, and scale or reliability surprises.

### Strategy, roadmap, or investment proposal

- `value-strategy`
  Focus on upside, leverage, opportunity cost, and strategic fit.
- `execution-feasibility`
  Focus on capability gaps, timing, dependency chains, and delivery realism.
- `downside-risk`
  Focus on reversibility, blast radius, second-order effects, and what happens if the bet is wrong.

### Process, policy, or org change proposal

- `stakeholder-fit`
  Focus on incentives, adoption, ownership, and who absorbs the burden.
- `execution-operations`
  Focus on rollout, maintenance, coordination cost, and failure to sustain the change.
- `failure-adversarial`
  Focus on loopholes, gaming, edge behavior, and harm transfer.

## Optional Supplemental Lenses

- `minority-risk`
  Use when the downside is unevenly distributed or when the proposal may disadvantage a weaker group.
- `simplification-pressure`
  Use when the proposal is becoming bloated and needs an explicit push toward scope reduction.
- `evidence-gap`
  Use when the main problem is uncertainty, weak assumptions, or lack of contact with reality.

## Lens Selection Rules

- Prefer orthogonal lenses over exhaustive coverage.
- If one lens already covers a concern well, do not add a near-duplicate.
- Add at most 1 new lens in a later round.
- If a later round introduces a new lens, say why the previous lens set was insufficient.
- If a user preference is active, apply at most 2 overlays.
- Preference overlays adjust prioritization and repair direction; they do not excuse real flaws.

## Multi-Agent Mode

If subagents are available and worth the cost:

- give each critic the same proposal brief
- give each critic only its own lens
- do not show one critic another critic's output before synthesis

If subagents are not available:

- run serial passes
- label the result as reduced-independence perspective-taking

## Round Guidance

- Round 1:
  identify the biggest structural weaknesses
- Round 2:
  test whether repairs actually resolved the key issues
- Round 3:
  pressure-test residual risks, overfitting, and unintended consequences

When a preference overlay is active:

- Round 1:
  keep the neutral baseline visible before shifting emphasis
- Round 2:
  check whether repairs improved the preferred direction without creating hidden regressions
- Round 3:
  test whether the proposal has become overfit to the preference rather than generally sound

If the user requests more than 3 rounds:

- keep the same default lenses unless there is a strong reason to rotate
- treat later rounds as diminishing-return checks, not invitations to reopen the entire proposal
