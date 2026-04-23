---
name: source-to-skill
description: Distill source material such as a person, book, theory, blog post, article, transcript, PDF, or source bundle into a skill-ready packet, emphasizing reusable workflows, task signatures, taste rubrics, operator rules, and failure modes. Use when Codex needs to extract repeatable ways of working from source material before deciding whether to extend an existing skill, create a new one, keep it reference-only, or route person-derived cases to `persona-perspective-builder`.
---

# Source To Skill

Turn source material into a skill candidate, not just a summary.
This skill is the bridge between source digestion and skill creation: it extracts what is reusable, filters out what should stay reference-only, and packages the result for `skill-creator` or a nearby owner.

Read these references only when needed:
- [source-archetypes.md](./references/source-archetypes.md) for extraction patterns across people, books, theories, blogs, and mixed source bundles
- [skill-candidate-packet.md](./references/skill-candidate-packet.md) for the packet schema and handoff fields
- [distillation-tests.md](./references/distillation-tests.md) for deciding whether the material is skill-worthy, reference-only, or still too weak
- [upstream-patterns.md](./references/upstream-patterns.md) for external and local patterns worth borrowing without copying blindly

## Use This Skill For

- turning a person, book, theory, blog, article, transcript, PDF, or note bundle into a reusable skill candidate
- extracting repeatable heuristics, workflows, task signatures, taste rubrics, operator rules, and failure modes from source material
- deciding whether source material should extend an existing skill, create a new one, or remain a reference page
- converting captured material into a `skill_candidate_packet` before using `skill-creator`
- synthesis tasks where the user wants more than a summary and specifically wants a reusable operational artifact

## Do Not Use

- the user only wants a summary, notes, or reading memo
- the task is just to capture or download a page
  - use `web-page-capture`
- the task is academic paper reading without a skill-creation goal
  - use `research-paper-reading-compass`
- the user already knows the exact skill they want and needs scaffolding or editing
  - use `skill-creator`
- the source is anchored to a person and the user primarily wants a person-derived advisor, perspective, persona, or hybrid skill
  - route to `persona-perspective-builder`
- the source material is too thin, too noisy, or too one-off to support repeatable behavior
  - keep it as reference-only knowledge

## Mutual Routing With `persona-perspective-builder`

These two skills overlap on person-shaped source bundles.

Route to `persona-perspective-builder` when:
- the person remains the main product, not just the source carrier
- the user wants `how this person thinks / decides / speaks / should advise`
- task signatures and taste should remain attached to that person-derived lens

Stay in `source-to-skill` when:
- the person is mainly carrying a reusable method or evaluator
- personhood becomes incidental once task structure and taste are extracted
- the best output is a `playbook`, `method`, `evaluator`, or `router`, not a person-derived skill

When routing, pass forward any extracted:
- `task_signature`
- `taste_rubric`
- `operator_rules`
- `exemplars_and_anti_exemplars`

## Input Contract

Require only:
- source material or source pointers
- the intended use, if known

Source material may be:
- a URL
- pasted text
- a PDF or notes
- a PersonalBrain page or source bundle
- several mixed artifacts around one person, book, theory, or blog series

Infer when possible:
- source archetype
- likely skill owner
- whether the output should be `extend`, `create`, `reference-only`, or `route`

Ask follow-up questions only when the target use is ambiguous enough to change the distillation shape.

## Output Contract

Always produce a `skill_candidate_packet` with:
- `source_frame`
- `extract_type`
- `durable_units`
- `skill_shape`
- `ownership_decision`
- `handoff_hint`

The packet should be concrete enough that `skill-creator` does not have to re-read the whole source set.

## Workflow

### 1. Normalize the Source Bundle

Collect the minimum working bundle first.

Preferred helpers:
- use `web-page-capture` when the input is one or more article or social URLs
- use `research-paper-reading-compass` when the source is a paper or theory-heavy technical document
- use `attach-personalbrain` when the relevant source set already lives in PersonalBrain

Do not start distillation from a broken or partial capture unless the user explicitly accepts that limitation.

### 2. Classify the Source Archetype

Choose one primary archetype from [source-archetypes.md](./references/source-archetypes.md):
- person
- book
- theory
- blog or article
- mixed bundle

If the bundle is mixed, choose one anchor archetype and treat the rest as supporting evidence.

If the anchor is `person`, make one explicit decision before continuing:
- `person-as-product`
- `person-as-carrier`

If it is `person-as-product`, route to `persona-perspective-builder`.
If it is `person-as-carrier`, stay here and keep extracting the reusable operational core.

### 3. Extract Durable Units

Pull out only the units that can survive beyond the original source:
- job-to-be-done
- task signature
- recurring workflow
- taste rubric
- operator rules
- heuristics or decision rules
- vocabulary or framing
- constraints and anti-goals
- failure modes
- examples and anti-examples worth preserving

Use these definitions:

- `task_signature`
  - preferred task grain
  - favored starting point
  - expected inputs
  - done condition
  - escalation or delegation rule
- `taste_rubric`
  - what gets rewarded
  - what gets penalized
  - preferred trade-offs
  - what feels overbuilt, sloppy, naive, elegant, or durable
- `operator_rules`
  - compact instructions another agent could actually follow
  - rules, defaults, and refusal criteria that survive outside the source wording

Separate:
- `observation`
- `inference`
- `assumption`

Do not let admiration or source prestige turn weak evidence into canonical behavior.

### 4. Separate Skill-Worthy Content From Reference-Only Content

Run the tests in [distillation-tests.md](./references/distillation-tests.md).

Keep skill-worthy:
- repeatable procedures
- reusable evaluators
- stable task signatures
- stable taste criteria
- operator rules that can guide future execution
- stable heuristics
- robust routing cues

Keep reference-only:
- biography
- long anecdotes
- historical context without action value
- one-off preferences that do not generalize
- single aesthetic remarks that never reappear in actions, critiques, or comparisons

### 5. Check Existing Ownership

Before proposing a new skill:
- search nearby skills first
- inspect the likely owner or adjacent owner
- decide whether the source material naturally extends an existing skill

Adjacent owners to check early:
- `persona-perspective-builder` for person-derived advisor or persona work
- `proposal-critique-refine` for critique logic that is already proposal-scoped
- `thinking-lenses` for prompt-shaping patterns that are mostly reasoning structure

Prefer:
- `extend_existing_skill`

over:
- `create_new_skill`

unless the source bundle clearly defines a new, non-overlapping job.

### 6. Choose the Skill Shape

Common output shapes:
- `playbook`
  - for repeatable workflows
- `persona`
  - for distilling a person's style, priorities, and decision patterns
- `method`
  - for theory-backed procedures or frameworks
- `evaluator`
  - for critique, audit, or review logic
- `router`
  - for choosing between related lanes

Choose the smallest shape that preserves the reusable core.

Do not force a `persona` shape here when the person-derived route should really be handled by `persona-perspective-builder`.

### 7. Build the Skill Candidate Packet

Use [skill-candidate-packet.md](./references/skill-candidate-packet.md).

Include:
- what the source is really teaching
- which `task_signature` seems most stable
- which `taste_rubric` appears repeated enough to operationalize
- which `operator_rules` are strong enough for direct reuse
- what should become trigger text
- what should become body instructions
- what should stay in references only
- whether the packet is strong enough to create now

### 8. Route the Follow-Up

Allowed next actions:
- `extend_existing_skill`
- `create_new_skill`
- `route_to_adjacent_skill`
- `keep_reference_only`

If the answer is `create_new_skill` or `extend_existing_skill`, hand off to `skill-creator`.
If the answer is `route_to_adjacent_skill`, say which skill should take over and pass the packet forward.
If the answer is `keep_reference_only`, stop honestly and suggest where the distilled notes should live instead.

## Source-Type Notes

### Person

Distill:
- the person's operating principles
- recurring choices and tradeoffs
- repeated task signatures
- repeated taste criteria
- signature vocabulary
- anti-patterns and red lines

Do not overfit to personality trivia.
If personhood remains the main product rather than a carrier for a method, route to `persona-perspective-builder`.

### Book

Distill:
- the core framework
- the chapters or concepts that actually change action
- the repeatable sequence or checklist
- what evidence or examples anchor the method

Do not recreate the whole book as a skill.

### Theory

Distill:
- primitives
- assumptions
- when the theory applies
- when it breaks
- how it changes decisions in practice

Do not keep it purely abstract if the goal is a skill.

### Blog Or Article

Distill:
- the operational playbook
- key distinctions
- concrete steps
- failure modes
- useful copyable examples

Do not preserve all prose; preserve only what changes execution.

## Guardrails

- do not confuse source digestion with source worship
- do not create a new skill just because the source is interesting
- do not silently convert weak or one-off material into canonical behavior
- do not duplicate an existing skill when a bounded extension would do
- do not copy large source passages into `SKILL.md`
- do not mistake one nice sentence for a stable taste rubric
- do not mistake one successful task for a durable task signature
- do not skip the `reference-only` outcome when the evidence is not strong enough

## Example Triggers

- `Use $source-to-skill to distill this blog series into a reusable playbook skill.`
- `Use $source-to-skill to screen this person and their writing, extract the reusable task/taste core, and decide whether to route to persona-perspective-builder.`
- `Use $source-to-skill to convert this book's method into a skill-ready packet, then tell me whether it should extend an existing skill.`
- `Use $source-to-skill to extract the operational core of this theory and decide if it deserves a new skill or just references.`
- `Use $source-to-skill to extract the task signature and taste rubric from this mixed source bundle, then decide whether it should stay generic or route to persona-perspective-builder.`
