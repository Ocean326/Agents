# Proposal Packet Contract

Use this schema when packaging the final result of `proposal-synthesis`.
Keep the packet compact, comparable, and ready for downstream critique.

## Top-Level Shape

- `problem_frame`
  - objective
  - target user or stakeholder
  - constraints
  - success criteria
  - biggest unknown
- `decision_criteria`
  - 3-5 criteria that explain how options should be compared
- `candidate_proposals`
  - 2-5 proposal briefs
- `recommended_candidate`
  - one candidate id or an explicit hybrid
- `open_questions`
  - only the unresolved points that still matter
- `handoff_hint`
  - where the next skill should go

## Candidate Proposal Shape

Each candidate proposal should contain:
- `id`
- `title`
- `core_thesis`
- `approach`
- `why_this_could_work`
- `main_tradeoff`
- `key_assumptions`
- `main_risks`
- `first_validation_step`

## Recommendation Rules

- Recommend exactly one candidate unless a hybrid is materially cleaner.
- If recommending a hybrid, name the parent candidates and what is borrowed from each.
- Include one sentence on why the rejected candidates were not selected.

## Handoff to Proposal Critique Refine

When the next step is `proposal-critique-refine`, include:
- the selected `proposal_brief`
- `recommended_lenses`
- `review_stance`
- `alternatives_considered`
- `questions_the_critic_should_resolve`

The critic should not need to reconstruct the design space from scratch.
