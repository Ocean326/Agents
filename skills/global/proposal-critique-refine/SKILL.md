---
name: proposal-critique-refine
description: Refine an existing proposal, draft, or partially formed plan through bounded multi-round critique, targeted improvement, and re-verification. Use when a coherent proposal already exists and needs critique rather than blank-page ideation or multi-option proposal generation. Default to a neutral review stance, and adjust critique direction when the user explicitly asks for preferences such as innovation, simplicity, speed, safety, or cost discipline.
---

# Proposal Critique Refine

Use this skill when the user already has a coherent idea, proposal, outline, strategy, or partial plan and wants to strengthen it through structured critique and improvement.

This skill is not for blank-page ideation.
If the input is too raw to form a proposal brief, route to `proposal-synthesis` when the user needs complete candidate proposals, or to `brainstorming` when they only need loose exploration first.

## Do Not Use

- No proposal, draft, or coherent idea exists yet
- The user wants open-ended brainstorming or invention
- The user wants 2-5 competing proposal options before critique
- The user wants research-heavy fact finding before critique
- The user wants implementation planning or coding right now
- The proposal is so underspecified that multiple critics would end up critiquing different things

## Entry Gate

Before starting critique, confirm the input can be normalized into a `proposal_brief`.

A valid `proposal_brief` should capture:
- problem or opportunity
- proposed approach
- target user or stakeholder
- key constraints
- success criteria
- main unknowns

If this cannot be done from the user message, ask up to 3 blocking questions.
If it still cannot be done, stop and route to `proposal-synthesis` or `brainstorming` instead of faking rigor.

## Core Principle

This is a critique-improve loop, not a debate club.

The goal is to:
- expose weaknesses
- strengthen the proposal
- preserve meaningful disagreement
- stop when additional rounds no longer produce meaningful improvement

Do not optimize for rhetorical winning.
Do not force consensus.
Do not pretend multiple passes are independent validation.

## Calibration and Preferences

Default to a neutral review stance.
Neutral means:
- do not quietly act as innovation-first, safety-first, or simplicity-first
- do not reward novelty for its own sake
- do not punish uncertainty more than the evidence supports
- balance value, feasibility, and risk unless the user asks otherwise

If the user explicitly states preferences, treat them as weighting overlays, not truth overrides.
Common overlays include innovation, simplicity, speed, safety, cost discipline, and evidence-first review.
Read [preference-overlays.md](./references/preference-overlays.md) when the user wants a specific bias in the critique or repair direction.

Preferences may change:
- which issues are prioritized
- which repair direction is preferred
- what tradeoffs are considered acceptable

Preferences must not:
- hide critical flaws
- turn weak evidence into strong evidence
- silently replace the neutral baseline

## Round Policy

- Default to 3 rounds
- If the user specifies a round count, use that count instead
- Stop early if:
  - no materially new high-severity issues appear
  - critiques become repetitive
  - remaining disagreement is mainly preference, politics, or values
  - further progress is blocked by missing evidence rather than proposal quality

Each round has 3 stages:
1. critique
2. improve
3. verify

## Default Workflow

### 1. Build Proposal Brief

Normalize the user's input into a stable `proposal_brief`.
Keep it short and concrete.
Do not quietly expand the scope.

### 2. Select Critique Lenses

Choose 3 deliberately different lenses by default.
Read [critic-rubrics.md](./references/critic-rubrics.md) when selecting them.
Read [preference-overlays.md](./references/preference-overlays.md) if the user specifies a preference profile.

Common default set:
- value
- feasibility
- failure-mode

Keep the set small and non-overlapping.
Reuse the same lenses across rounds unless a materially new risk class appears.
If a preference overlay is active, use it to adjust issue ordering and repair direction, not to invent a different proposal category.

### 3. Run Critique

For each lens, return:
- strongest concern
- what still holds up
- assumption under attack
- why this matters now
- severity
- confidence
- evidence type
- what would change the critique
- concrete repair direction

If subagents are available and the extra cost is justified, critics may run independently.
If not, run serial rubric passes and explicitly state that independence is limited.

Keep the critique constructive.
Avoid generic statements like `too risky`, `unclear`, or `too complex` unless you also explain:
- the failure mechanism
- the consequence
- the smallest repair worth trying

### 4. Build the Issue Register

Record round findings in an `issue_register`.
Read [issue-register.md](./references/issue-register.md) for the schema and status values.

Merge duplicates.
Keep only decision-relevant issues.
Default to 3-5 active issues per round.

### 5. Improve

Repair only the top 1-3 issues for the round unless a critical blocker forces more.

Improvement modes:
- repair: minimal changes that address the issue directly
- redesign: larger structural change when local repair is not enough
- simplify: remove scope or complexity instead of adding mechanism

If subagents are available and the repair direction is genuinely ambiguous, use up to 2 improvers with different modes.
If not, run a single bounded improvement pass.

Do not rewrite the proposal from scratch unless the current structure is unsalvageable.
If user preferences are active, prefer repairs that move the proposal in that direction while still naming the new tradeoffs created.

### 6. Verify

Re-check the repaired proposal against the original critique lenses.

Verification should answer:
- which issues were actually addressed
- which issues remain open
- whether any new issue was introduced
- whether another round is justified

Verification is not a fresh unlimited critique round.
It is a bounded re-check against known issues.

### 7. Repeat or Stop

Move to the next round only if there is still meaningful improvement to make.

Stop early when:
- high-severity issues are resolved
- the next round would mostly repeat prior objections
- unresolved issues require evidence, testing, or stakeholder input rather than more internal critique

### 8. Final Synthesis

Produce a final memo with:
1. proposal brief
2. round-by-round major critiques
3. repairs applied
4. remaining risks
5. preserved disagreements
6. final recommendation
7. next-step artifact

Read [output-template.md](./references/output-template.md) when you need the exact section format.

## Evidence Contract

- Distinguish `observation`, `inference`, and `assumption`
- Label evidence as one of: `user-provided`, `source-backed`, `inference`, or `assumption`
- Include `severity` and `confidence` for each issue
- If key evidence is missing, say so plainly and recommend a test, interview, or research step instead of faking certainty

## Constructive Critique Contract

Every non-trivial critique should help the proposal get better.

Each serious issue should include:
- what is working and should be preserved
- what is wrong or fragile
- why it matters
- what evidence would change the judgment
- what repair is worth trying next

Do not reward empty toughness.
Sharper critique is only better when it is more specific, more testable, or more useful for repair.

## Multi-Agent Mode

Use multi-agent execution only when it materially improves the result.

If subagents are available:
- give all critics the same proposal brief
- give each critic only its own lens
- do not let one critic see another critic's output before synthesis
- use multiple improvers only when the repair path is genuinely contested

If subagents are not available:
- run serial passes
- label the result as reduced-independence perspective-taking

Do not present same-model serial passes as independent validation.

## Guardrails

- Do not use this skill for blank-page ideation
- Do not generate a first draft when no proposal brief exists
- Do not generate multiple candidate proposals here; route to `proposal-synthesis` instead
- Do not move into planning or implementation unless the user explicitly changes the task
- Do not use scoring theater or fake precision without a user-provided rubric
- Do not let every round reopen the whole proposal
- Do not continue refining just because another round is possible
- Do not silently apply a strong bias when the user did not ask for one
- Do not let user preferences erase critical blockers or weak evidence
- Do not produce critique that is vague, performative, or purely negative

## Output

Produce a `Critique-Refine Memo` with these sections:

1. `Proposal Brief`
2. `Review Stance`
3. `Round Summary`
4. `Issue Register Snapshot`
5. `Repairs Applied`
6. `Residual Risks`
7. `Preserved Disagreements`
8. `Final Recommendation`
9. `Next-Step Artifact`
10. `Why This Pass Stops Here`

Allowed `Final Recommendation` values:
- `proceed`
- `revise`
- `de-scope`
- `test`
- `pause`
- `stop`

Allowed `Next-Step Artifact` values:
- revised proposal
- experiment plan
- decision memo
- risk register
- research brief
- implementation plan

## Quality Bar

A good run should:
- make the proposal more concrete than it started
- surface non-overlapping critiques
- show visible improvement across rounds
- preserve unresolved disagreement honestly
- stop before the process becomes performative
