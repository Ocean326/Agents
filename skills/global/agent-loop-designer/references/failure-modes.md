# Failure Modes

Use this checklist before trusting a workflow design.

## Ownership Failures

- two agents both think they own the next turn
- no owner is responsible after a handoff
- the controller secretly does worker tasks and bypasses its own protocol

## State Failures

- important routing or approval state lives only in model memory
- resume lacks a checkpoint or side-effect log
- downstream nodes depend on free-form text instead of typed fields

## Loop Failures

- no max iteration count
- no quality threshold
- retrying despite the same blocker appearing repeatedly
- self-improvement loop mutates goals instead of improving execution

## Routing Failures

- low-confidence route still triggers a high-risk action
- router has no fallback path
- route catalog overlaps too heavily for reliable classification

## Handoff Failures

- full transcript passed when a scoped packet would do
- specialist lacks the fields needed to continue
- handoff oscillates between two agents with no tie-breaker

## Controller Failures

- manager becomes the bottleneck for every micro-decision
- workers are so constrained they keep escalating trivial questions
- controller context grows every cycle without pruning

## Prompt Reliability Failures

- prompt revisions keep expanding scope instead of improving execution
- controller prompt encourages over-decomposition and task fragmentation
- prompt and externalized state disagree about owner, stage, or approval status
- schema failures repeat because the output contract is vague
- prompt edits ship without regression checks, so failures bounce between versions

## Safety Failures

- untrusted user text leaks into trusted developer instructions
- risky tools are available to roles that do not need them
- approvals are implicit instead of explicit

## Stress Test Questions

Ask these before rollout:

1. What exactly stops the loop?
2. What state must survive a crash or wake-up?
3. What side effects can happen twice, and how will duplicates be prevented?
4. What happens when routing confidence is low?
5. What happens when the evaluator and optimizer disagree repeatedly?
6. Which role can ask for human intervention, and under what condition?
7. What stops prompt refinement from becoming open-ended prompt churn?
8. How will you detect that a prompt change made the loop noisier, broader, or more fragile?

If the answers are fuzzy, the design is not ready yet.
