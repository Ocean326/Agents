# Default Flows

## Flow Selection

Select the lightest flow that still protects correctness and intent.

### 1. New Feature

Use when the user is asking for net-new capability.

Default sequence:
1. sweep context
2. clarify goal, success criteria, and scope boundary
3. propose options if the solution shape is not obvious
4. create brief and design artifacts sized to complexity
5. produce implementation plan
6. implement
7. generate or run tests
8. verify
9. run innovation pass
10. close out

### 2. Existing Feature Iteration

Use when the user wants to extend, polish, or reshape something already present.

Default sequence:
1. inspect current behavior and surrounding constraints
2. identify delta from current to desired behavior
3. create a lightweight brief or design note if behavior changes are non-trivial
4. implement the delta
5. add or update tests
6. verify
7. suggest low-risk follow-on improvements

### 3. Bugfix

Use when the user reports a broken behavior, regression, or failing test.

Default sequence:
1. reproduce or anchor the symptom
2. identify likely root cause
3. choose the narrowest fix that solves the real problem
4. add or update regression coverage
5. verify the symptom and adjacent risk surface
6. close out with cause, fix, and evidence

Compression rule:
- skip heavy design artifacts unless the bug reveals a broader design flaw

### 4. Refactor or Optimization

Use when the goal is maintainability, performance, or developer experience.

Default sequence:
1. define the intended gain
2. mark preserved behavior and interfaces
3. assess blast radius
4. implement in small reversible steps
5. run existing tests plus targeted validation
6. report tradeoffs and residual risk

Compression rule:
- keep documents lightweight unless interfaces or architecture change

### 5. Research-Backed Implementation

Use when implementation depends on external facts, API choices, or unfamiliar surfaces.

Default sequence:
1. collect the minimum facts needed
2. separate observations from inferences
3. recommend a path
4. capture the decision in a brief or design note
5. implement
6. verify against the chosen constraints

### 6. Opportunistic Improvement Pass

Use near the end of another flow.

Ask:
- what small change reduces future pain
- what missing test or guardrail would have caught this earlier
- what polish item improves the delivery at low risk

Do directly:
- missing tests
- naming cleanup
- tiny docs improvements
- guardrails and validation checks
- low-risk UX polish

Propose first:
- architecture reshaping
- large UI redesign
- breaking contract changes
- medium or high-cost cleanup

## Phase Compression

Compress aggressively when:
- the scope is tiny
- the user asked for speed
- the change is local and well understood
- verification is straightforward

Do not compress away:
- problem framing
- risk gating
- verification
- closeout evidence

## Oversized Work

If the request spans multiple subsystems or milestones:
1. define the top-level outcome
2. split into stages or subprojects
3. fully drive only the first executable slice
4. leave the rest as an ordered plan
