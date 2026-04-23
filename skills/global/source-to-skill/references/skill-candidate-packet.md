# Skill Candidate Packet

Use this schema as the main output of `source-to-skill`.

## Top-Level Shape

- `source_frame`
  - source type
  - source list
  - intended use
  - confidence of coverage
- `extract_type`
  - playbook
  - persona
  - method
  - evaluator
  - router
- `durable_units`
  - reusable procedures
  - task signature
  - taste rubric
  - operator rules
  - heuristics
  - constraints
  - failure modes
  - examples and anti-examples
- `skill_shape`
  - likely trigger text
  - likely `SKILL.md` body sections
  - what should stay in `references/`
- `ownership_decision`
  - `extend_existing_skill`
  - `create_new_skill`
  - `route_to_adjacent_skill`
  - `keep_reference_only`
- `handoff_hint`
  - next owner or next skill

## Durable Units Rules

Only keep units that are:
- reusable
- reasonably stable
- operational
- attributable to evidence

If a unit is interesting but not operational, move it to reference-only.

For `task_signature`, prefer repeated evidence about:
- preferred unit of work
- favored starting point
- done condition
- escalation rule

For `taste_rubric`, prefer repeated evidence from:
- comparisons
- critiques
- trade-off choices
- explicit anti-patterns

## Ownership Decision Rules

- `extend_existing_skill`
  - the source clearly strengthens an existing owner's job
- `create_new_skill`
  - the source defines a distinct, repeatable, non-overlapping job
- `route_to_adjacent_skill`
  - another distillation skill is the better front door, especially for person-derived advisor or persona work
- `keep_reference_only`
  - the source is informative but not skill-worthy yet

## Handoff To Skill Creator

When handing off to `skill-creator`, include:
- recommended skill name
- why the job is distinct
- trigger examples
- body sections to create
- what belongs in `references/`
- the `task_signature`
- the `taste_rubric`
- the `operator_rules`

The creator should not need to rediscover the source logic from scratch.
