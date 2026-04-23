# Risk Gates

Use this reference whenever the next action could materially change intent, cost, or blast radius.

## Default Autonomy Bands

### Safe to Do Directly

- requirements cleanup
- implementation planning
- low-risk code changes
- adding or fixing tests
- small refactors with preserved behavior
- developer-experience improvements
- missing docs tied to the current task
- small polish improvements

### Propose Before Doing

- architecture reshaping
- breaking API or schema changes
- large UI redesign
- product direction changes
- data migration with non-trivial impact
- broad dependency swaps
- multi-day or high-cost work

### Stop and Ask

- goals conflict
- a key constraint is unknown and not discoverable
- validation cannot support the likely claim
- the request touches sensitive or high-stakes domains
- current repo state suggests another human's in-progress work would be disrupted

## Evidence Strength

When verification is weak, say so plainly.

Ordered strongest to weakest:
1. automated tests proving the intended scenario
2. reproducible regression check
3. build, typecheck, lint, or compile proof
4. focused manual scenario walkthrough
5. static reasoning only

Do not speak as if level 5 equals level 1.

## Proposal Format for Medium/High-Risk Changes

When proposing instead of acting, include:
- current issue
- proposed change
- expected gain
- main tradeoff
- minimum validation plan

Keep it short.

## Conflict Handling

If two goals compete, resolve in this order:
1. preserve user intent
2. protect correctness
3. protect reversibility
4. optimize speed
5. optimize polish

If that still does not resolve the conflict, pause and ask.
