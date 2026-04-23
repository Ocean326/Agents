# Evaluation and Close Loop

Use this reference when the workflow should improve through review, grading, or iterative refinement.

## What to Measure

Choose a small set of signals before building the loop:

- task success
- rubric score
- latency or cycle count
- tool error rate
- approval frequency
- handoff failure rate
- resume failure rate

Do not create a refinement loop without a measurable exit condition.

## Loop Types

### Evaluator-Optimizer

Use when:
- quality criteria are clear
- the evaluator can explain what to fix
- a better next draft is realistically achievable

Need:
- rubric
- threshold
- max revisions
- trace of each revision and score

### Reviewer Gate

Use when:
- a human or trusted reviewer must approve side effects
- quality matters more than iteration speed

Need:
- approval status
- block vs comment semantics
- escalation target

### Trace-Then-Tune

Use when:
- the workflow is failing unpredictably
- the problem might be routing, tool design, prompt contract, or state loss

Need:
- traces
- per-node inputs and outputs
- failure classification

Tune only after the traces show where the design is breaking.

### Prompt-Refinement Loop

Use when:
- traces show the prompt contract is a repeat cause of failure
- prompt edits can be evaluated with a stable rubric and regression set

Need:
- failure signature
- prompt version
- regression cases
- max prompt revisions
- rollback condition

Keep prompt evaluation separate from task-output evaluation whenever possible.

## Close-Loop Rules

- set `max_iterations` explicitly
- distinguish `pass`, `revise`, and `stop`
- keep the evaluator read-only unless rewrite authority is intentional
- log the reason each loop continues
- stop when improvement plateaus, not only when perfection is absent
- re-run prompt regressions after each prompt edit before promoting the new prompt

## Approval Gates

Use approval gates for:
- writes to durable truth
- deletions
- external communications
- money movement
- privileged actions

Approval state should be explicit, for example:
- `not_required`
- `pending`
- `approved`
- `rejected`

Do not infer approval from silence.

## Minimal Evaluation Output

Every evaluation node should return:

- `decision`
- `score` or threshold judgment
- `findings`
- `recommended_next_action`
- `continue_loop`

## Plateau Test

Stop iterating when:
- the score does not improve meaningfully over multiple rounds
- revision guidance repeats
- the remaining gap is outside the workflow's current scope
- a human decision is now cheaper than another cycle
