---
name: proposal-synthesis
description: Generate 2-5 structured candidate proposal briefs from a vague goal, problem, or opportunity, then synthesize them into a critique-ready recommendation packet. Use when the user needs blank-page ideation to become multiple complete proposals across research, development, product, or general problem-solving, especially before `proposal-critique-refine`, when several materially different options should be compared, or when bounded subagent divergence would improve coverage.
---

# Proposal Synthesis

Turn an open problem into a small design space of complete proposal briefs.
This skill sits between loose ideation and critique: it should create critique-ready options, not just brainstorm fragments and not yet run the bounded critique loop itself.

Read these references only when needed:
- [output-contract.md](./references/output-contract.md) for the `proposal_packet` shape and handoff fields
- [domain-lens-packs.md](./references/domain-lens-packs.md) for default divergence criteria across research, development, and general problem-solving
- [subagent-patterns.md](./references/subagent-patterns.md) for bounded multi-subagent role sets and isolation rules
- [prompt-shaping.md](./references/prompt-shaping.md) for how to tighten the input with `thinking-lenses`

## Use This Skill For

- vague goals that need 2-5 complete proposal options rather than one recommended direction
- requests that say `give me several plans`, `compare multiple approaches`, or `generate proposals before critique`
- cross-domain work where the user wants research, engineering, or decision options in a common proposal shape
- cases where `proposal-critique-refine` would be premature because no stable `proposal_brief` exists yet
- bounded multi-subagent divergence where each subagent should generate a different candidate instead of critiquing one shared draft

## Do Not Use

- the user only wants loose exploration, sketches, or clarifying conversation
  - use `brainstorming`
- a coherent proposal already exists and mainly needs critique, repair, or stress testing
  - use `proposal-critique-refine`
- the task is mostly product discovery, stakeholder research, or market analysis
  - use `business-analyst`
- the user wants implementation planning or coding right now
  - use `delivery-conductor` or a narrower execution lane
- the main missing ingredient is external fact-finding rather than proposal generation
  - do the research first instead of inventing around missing evidence

## Input Contract

Require only:
- the problem, opportunity, or desired outcome

Infer when possible:
- target user or stakeholder
- constraints
- decision criteria
- time horizon
- what makes the options meaningfully different

Ask follow-up questions only when a missing fact would make the candidate proposals non-comparable, unsafe, or obviously mis-scoped.

## Output Contract

Always produce a `proposal_packet` containing:
- `problem_frame`
- `decision_criteria`
- `candidate_proposals`
- `recommended_candidate`
- `open_questions`
- `handoff_hint`

Each candidate proposal must be complete enough for a downstream critic to attack it without inventing the missing core.

## Workflow

### 1. Frame the Problem

Normalize the ask into:
- objective
- target user or stakeholder
- constraints
- success criteria
- biggest unknown

Keep the frame compact and faithful.
Do not quietly upgrade a small request into a bigger strategy exercise.

### 2. Tighten the Prompt When Needed

If the request is underspecified, high-cost, or likely to branch too widely, first tighten the generation prompt with `thinking-lenses`.
Prefer the lightest shaping that still protects quality:
- `inline-structured` for most medium tasks
- `pre-optimizer` only when the solution space is wide, ambiguous, or expensive

Do not spend more effort polishing the prompt than producing the proposals.

### 3. Choose the Divergence Shape

Default to `3` candidate proposals.

Use:
- `2` when the scope is small or urgency is high
- `4-5` when the task is broad and the additional options remain meaningfully different

Pick one domain lens pack from [domain-lens-packs.md](./references/domain-lens-packs.md):
- research
- development
- general problem-solving

The candidate set should differ in mechanism, risk posture, or sequencing, not just wording.

### 4. Generate Candidate Proposal Briefs

Each candidate should include:
- `title`
- `core_thesis`
- `approach`
- `why_this_could_work`
- `main_tradeoff`
- `key_assumptions`
- `main_risks`
- `first_validation_step`

Favor complete, attackable proposals over a long list of thin ideas.

### 5. Use Subagents Only When They Improve Coverage

If subagents are available and the design space is genuinely wide, use up to `4` bounded proposal generators.
Give every subagent:
- the same `problem_frame`
- the same hard constraints
- the same decision criteria
- one distinct role or lens

Do not show one subagent another subagent's output before synthesis.
If subagents are not available, run serial passes and explicitly label the result as reduced-independence perspective-taking.

### 6. Synthesize the Design Space

Merge duplicates.
Keep only the `2-5` options that remain materially different and decision-relevant.

Then produce:
- a comparison grid
- the best-fit recommendation
- one sentence on why each rejected option was not selected

If a hybrid is recommended, explain what is borrowed from each source option and why the hybrid is cleaner than either parent.

### 7. Prepare the Critique Handoff

Select one `proposal_brief` as the critique candidate.
Package it with:
- alternative options that were considered
- decision criteria
- unresolved questions
- recommended critique lenses

Use the schema in [output-contract.md](./references/output-contract.md).

### 8. Stop at the Proposal Layer

This skill stops once the proposal set is ready.

Next handoffs:
- use `proposal-critique-refine` when the best candidate now needs bounded critique and repair
- use `delivery-conductor` when the direction is good enough to push into planning, implementation, testing, or verified delivery

Do not silently continue into implementation planning unless the user explicitly changes the task.

## Multi-Agent Mode

Use multi-agent divergence only when it materially improves coverage.

Default role sets live in [subagent-patterns.md](./references/subagent-patterns.md).
Each subagent should return one candidate proposal with:
- `thesis`
- `main_tradeoff`
- `largest_assumption`
- `first_validation_step`

Good uses:
- cross-disciplinary research directions
- product or engineering strategy with real architecture tradeoffs
- ambiguous problem-solving where reversibility and risk posture differ

Poor uses:
- tiny scoped tasks
- cases where all roles would generate near-identical proposals
- requests where the real blocker is missing facts, not missing options

## Guardrails

- do not confuse this skill with free-form brainstorming
- do not run a critique loop here and pretend it replaces `proposal-critique-refine`
- do not let more candidates crowd out meaningful differences
- do not invent evidence to make weak proposals look grounded
- do not produce one polished option plus cosmetic variants
- do not present same-model serial passes as independent validation
- do not jump into implementation plans, task lists, or code changes unless the user explicitly asks to continue

## Example Triggers

- `Use $proposal-synthesis to turn this vague direction into 3 critique-ready proposal briefs.`
- `Use $proposal-synthesis to generate multiple research plans, recommend one, and package it for critique.`
- `Use $proposal-synthesis to explore several engineering directions before we send one to proposal-critique-refine.`
- `Use $proposal-synthesis with bounded subagent divergence so I can compare multiple complete solutions instead of one draft.`
