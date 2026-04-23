---
name: persona-perspective-builder
description: Distill a real, historical, fictional, or privately known person from mixed source channels into a reusable skill. Combines multi-channel evidence intake with mindset, task-signature, taste-rubric, and persona extraction, then chooses the right output shape: a perspective skill, a persona skill, or a hybrid simulation skill. Use when the user wants to extract how someone thinks, structures work, chooses trade-offs, speaks, decides, and behaves across interviews, writings, chats, documents, social posts, timelines, and third-party commentary, then turn that into a new skill rather than a simple report.
---

# Persona Perspective Builder

Fuse the best parts of `nuwa-skill` and `anyone-skill` without inheriting their worst constraints.

This skill is for building a new person-derived skill from evidence, not for writing a flattering summary.

It should:
- intake mixed evidence from many channels
- separate `thinking framework`, `task signature`, and `taste rubric` from `surface mimicry`
- decide whether the result should be `perspective`, `persona`, or `hybrid`
- produce a bounded, honest, reusable skill package

## Core Thesis

Use `nuwa` ideas for:
- mental models
- decision heuristics
- anti-patterns
- worldview tensions
- repeated task structure
- repeated taste and critique patterns

Use `anyone` ideas for:
- source intake across chats, documents, archives, and public content
- interaction style
- memory anchors
- values and contradictions
- iterative correction and update flow

Do not force every subject into full-person simulation.
Many targets only justify a strong `perspective` skill.
Many of the most valuable outputs in the agent era are not mimic voice, but reusable `task signatures` and `taste rubrics`.

## Output Modes

Choose exactly one primary output mode.

### 1. `perspective`

Use when the main value is:
- how this person thinks
- how they make decisions
- how they frame trade-offs
- how they evaluate new problems
- how they tend to structure work
- what kind of solutions they consistently reward or reject

Best for:
- public thinkers
- founders
- researchers
- historical figures
- thin but high-quality public evidence

Default deliverable:
- `[slug]-perspective/`
- `SKILL.md`
- `agents/openai.yaml`
- `references/evidence_profile.md`

### 2. `persona`

Use when the main value is:
- how this person speaks
- how they react
- how they relate to others
- how they carry memory, tone, and interpersonal style

Best for:
- private or user-supplied archives
- rich chat logs
- letters, diaries, emails
- user-known people with strong behavioral traces

Default deliverable:
- `[slug]-persona/`
- `SKILL.md`
- `agents/openai.yaml`
- `references/persona_profile.md`

### 3. `hybrid`

Use when both are strong:
- the target has stable thinking patterns
- the target also has enough evidence for believable interaction style

Best for:
- well-documented public figures with long-form interviews
- personal archives plus reflective writing
- targets where the user explicitly wants both advisor value and character fidelity

Default deliverable:
- `[slug]-hybrid/`
- `SKILL.md`
- `agents/openai.yaml`
- `references/evidence_profile.md`
- `references/persona_profile.md`

## Input Contract

Require only:
- who the subject is
- what the user wants the resulting skill to do

Infer when possible:
- subject type
- likely source channels
- best output mode
- whether the goal is advisory, simulation, or both

If the material is really a generic method, evaluator, or playbook with a person wrapper, route to `source-to-skill` instead of forcing a person-derived build.

Ask follow-up questions only when one of these changes the result:
- private vs public use
- availability of private archives
- whether distribution is intended
- whether the user wants a `perspective`, `persona`, or `hybrid` result

If not specified, default rules are:
- public figure -> `perspective`
- private archive-heavy subject -> `persona`
- mixed rich evidence + explicit simulation/advisor goal -> `hybrid`

## Mutual Routing With `source-to-skill`

Stay here when:
- the person remains the main product
- the user wants a person-derived advisor, perspective, persona, or hybrid result
- the extracted task signatures and taste should stay attached to that person-shaped lens

Route to `source-to-skill` when:
- the bundle is really teaching a generic method, playbook, evaluator, or router
- task structure and taste matter more than personhood
- the person is mainly a carrier for a reusable workflow
- evidence is too weak for a person-derived result but strong enough for operational extraction

When routing, pass forward:
- `thinking_frameworks`
- `task_signatures`
- `taste_rubrics`
- `operator_rules`
- `exemplars_and_anti_exemplars`

## Workflow

### 1. Frame the Subject

Classify the target:
- `self`
- `someone-known`
- `public-figure`
- `historical-figure`
- `fictional-character`
- `archetype`

Then classify the user's intent:
- `advisor`
- `simulation`
- `both`

Do not proceed as if the target is public-safe if the user is supplying private material.

### 2. Build the Evidence Map

Normalize every source into an evidence ledger with:
- `source_id`
- `channel`
- `publicness`
- `time_span`
- `subject_distance`
- `confidence_level`
- `perspective_value`
- `task_value`
- `taste_value`
- `persona_value`

Recommended channels:
- writings and long-form essays
- interviews and podcasts
- short social posts
- chat exports
- email or document archives
- biographies and external commentary
- decision records and major actions
- timeline and turning points

Score each source four ways:
- `perspective_value`: how much it reveals thought structure
- `task_value`: how much it reveals preferred task shape and workflow behavior
- `taste_value`: how much it reveals quality bar, trade-off logic, and anti-slop judgment
- `persona_value`: how much it reveals interaction and behavior

Use these rough heuristics:
- essays, books, talks -> high perspective
- demos, code reviews, design critiques, planning artifacts -> high task and taste
- chats, emails, DMs -> high persona
- interviews -> medium-high for both
- interviews about projects or decisions -> medium-high task and taste
- social posts -> medium persona, medium perspective only if repeated patterns appear
- third-party commentary -> low-medium, never primary if first-party evidence exists

### 3. Choose the Build Shape

Use this decision table:

| Evidence shape | Best mode |
|---|---|
| Mostly public, reflective, idea-rich | `perspective` |
| Mostly private, conversational, behavior-rich | `persona` |
| Strong first-person reflection plus strong interaction traces | `hybrid` |

If the evidence is wide but shallow, degrade gracefully to `perspective`.
Do not claim full-person simulation without strong persona evidence.

### 4. Run Multi-Lane Extraction

Run all lanes even if one will later be downweighted.

#### Pass A: Cognitive Extraction

Extract:
- 3-7 mental models
- 5-10 decision heuristics
- recurring trade-off logic
- anti-patterns and refusal rules
- contradictions worth preserving

This is the `nuwa`-style core.

#### Pass B: Task Extraction

Extract:
- recurring task shapes
- preferred task grain
- favored starting point
- done conditions
- delegation or escalation rules
- favored interfaces, tools, or surfaces
- recurring transformation from vague ask to executable unit

This is the `tasky` lane.

#### Pass C: Taste Extraction

Extract:
- what this person consistently rewards
- what they consistently reject
- repeated trade-off preferences
- signals of elegance, durability, or overbuilding
- examples and anti-examples they use to teach judgment
- likely operator rules another agent could reuse

This is the `taste` lane.

#### Pass D: Persona Extraction

Extract:
- vocabulary and sentence habits
- emotional temperature
- conflict style
- humor and softness/harshness
- memory anchors
- pride, fear, fixation, avoidance
- core values and prohibitions

This is the `anyone`-style core.

### 5. Grade the Evidence

Every non-trivial claim should be tagged as:
- `L1` direct quote or direct artifact
- `L2` strong paraphrase or well-sourced report
- `L3` inference from multiple signals
- `L4` inspired extrapolation

Higher-stakes traits need stronger evidence:
- `voice style` may tolerate some `L3`
- `non-negotiable values` should prefer `L1-L2`
- `hard prohibitions` should almost never rely only on `L4`
- `task signatures` should prefer repeated observed choices, not one project
- `taste rubrics` should prefer repeated critiques, comparisons, or trade-off decisions

If evidence conflicts, preserve the tension.
Do not smooth contradictions into fake coherence.

### 6. Build the Skill Packet

Produce a packet with:
- `subject_frame`
- `source_inventory`
- `chosen_mode`
- `durable_units`
- `honesty_boundaries`
- `target_skill_shape`

`durable_units` should separate:
- `thinking_frameworks`
- `task_signatures`
- `taste_rubrics`
- `operator_rules`
- `interaction_patterns`
- `memory_anchors`
- `values_and_red_lines`
- `failure_modes`

### 7. Generate the New Skill

Create the generated skill directory for the subject.

Default shape:
- `SKILL.md`
- `agents/openai.yaml`
- `references/*.md` only when needed

The generated `SKILL.md` should include:
- clear trigger text
- what the skill is for
- what it must not pretend to know
- how it should answer new questions
- how to express uncertainty

For `perspective` mode:
- optimize for advice, analysis, decision framing, task shaping, and critique
- do not over-index on mimic voice
- expose stable `operator rules` when they are genuinely evidenced

For `persona` mode:
- optimize for interaction fidelity and boundaries
- do not overclaim worldview depth when evidence is mostly conversational

For `hybrid` mode:
- make `thinking core` primary
- make `voice and behavior` a controlled overlay
- if the two conflict, preserve the cognitive core over surface mimicry

### 8. Validate Before Delivery

Run at least these checks:

1. `known-stance test`
   Compare 3 generated answers against known subject positions.

2. `new-problem test`
   Ask one novel question and confirm the skill answers from extracted principles, task signatures, and taste rubrics rather than generic filler.

3. `boundary test`
   Ask beyond the evidence and confirm the skill says what is unknown.

4. `mode-fit test`
   Confirm the chosen `perspective/persona/hybrid` mode matches the actual evidence mix.

5. `task-fit test`
   Ask the skill to structure a new task and verify the output reflects the extracted task grain, starting point, and done condition.

6. `taste-fit test`
   Ask the skill to compare two options and verify the judgment uses repeated trade-off signals rather than vague aesthetics.

If the validation fails:
- reduce scope
- downgrade `hybrid -> perspective` or `persona -> perspective`
- mark weak areas explicitly

## Guardrails

- do not confuse `voice cloning` with `person understanding`
- do not grant `hybrid` status unless both lanes are genuinely evidenced
- do not use sparse social posts as the whole person
- do not treat biography as behavior
- do not build deception tools for impersonation, harassment, or manipulation
- do not present public-figure simulations as the real person
- do not turn weak inference into strong canon

## Honesty Boundaries

Always include these in the generated skill when relevant:
- this is evidence-shaped, not the real person
- public evidence has blind spots
- private archives still do not expose the whole interior self
- changed positions over time should be preserved with dates when possible

## Recommended Defaults

If building for public thinkers:
- prioritize `perspective`
- use long-form writing, interviews, decisions, and criticism
- pay special attention to task-shaping and taste signals in project choices, reviews, and demos

If building for people known personally:
- prioritize `persona` or `hybrid`
- use chat logs, emails, notes, and user-supplied memories

If building for fictional characters:
- use `persona`
- switch to inspired-by mode when distribution is intended

## Example Requests

- `Use $persona-perspective-builder to turn this founder's interviews, essays, and tweets into a perspective skill.`
- `Use $persona-perspective-builder to build a hybrid skill from these chats, emails, and voice notes about my former collaborator.`
- `Use $persona-perspective-builder to decide whether this target deserves a perspective skill or a full persona skill before generating anything.`
- `Use $persona-perspective-builder to fuse public research and private archives, then create the best-fit person-derived skill.`
- `Use $persona-perspective-builder to extract how this person structures work and what kinds of solutions they consistently reward or reject.`
- `Use $persona-perspective-builder to decide whether this bundle should stay person-derived or route to $source-to-skill because the reusable method matters more than the person.`
