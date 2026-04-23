# Distillation Tests

Use these tests before deciding that source material should become a skill.

## Skill-Worthy Tests

### 1. Repeatability Test

Can the extracted behavior be reused across multiple future tasks?

If no, keep it as reference-only.

### 2. Operationality Test

Does the material change what an agent should do, not just what it should know?

If no, keep it as reference-only.

### 3. Boundaries Test

Is there a clear job-to-be-done with inputs, outputs, and trigger conditions?

If no, do not create a skill yet.

### 4. Non-Overlap Test

Would this naturally extend an existing skill instead of creating a new one?

If yes, prefer extension.

### 5. Evidence Test

Is the extracted pattern supported by repeated or clearly central source evidence rather than one anecdote?

If no, mark it as lower-confidence or keep it as reference-only.

### 6. Task Signature Test

Can you name a stable:
- preferred task grain
- favored starting point
- done condition
- escalation rule

If no, do not pretend the bundle teaches a reusable `task_signature`.

### 7. Taste Rubric Test

Can you point to repeated comparisons, critiques, or trade-off choices that show what the source rewards or rejects?

If no, do not invent a `taste_rubric` from one colorful remark.

## Failure Modes

- a famous source gets over-weighted just because it is famous
- the output becomes a summary instead of a skill
- a long source bundle creates a bloated skill
- one-off preferences get mistaken for durable operating rules
- one-off task anecdotes get mistaken for durable task signatures
- aesthetic remarks get mistaken for operational taste
- admiration replaces boundary discipline

## Honest Outcomes

Allowed final outcomes:
- `create_new_skill`
- `extend_existing_skill`
- `route_to_adjacent_skill`
- `keep_reference_only`

`keep_reference_only` is a successful result when the material is useful but not skill-worthy.
`route_to_adjacent_skill` is a successful result when another distillation lane is the better front door.
