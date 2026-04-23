# Subagent Patterns

Use subagents only when they create genuinely different candidate proposals.
If the task is narrow, stay serial.

## Shared Context Slice

Give every subagent only:
- `problem_frame`
- hard constraints
- decision criteria
- one assigned role
- the required output shape

Do not leak:
- your preferred answer
- another subagent's output
- downstream critique results

## Default Role Sets

### Research

- `novelty-scout`
  Push for a stronger contribution or a cleaner hypothesis.
- `experiment-realist`
  Prefer the smallest validating experiment with believable evidence.
- `failure-mode-skeptic`
  Attack assumptions, confounds, and weak comparisons.
- `simplifier`
  Remove decorative complexity and protect the core claim.

### Development

- `bold-builder`
  Propose the highest-upside product or technical move.
- `systems-pragmatist`
  Prefer the path that fits current architecture and delivery reality.
- `operational-skeptic`
  Focus on maintenance, rollout, and edge-case cost.
- `simplifier`
  Push for the narrowest change that still solves the problem.

### General Problem-Solving

- `leverage-seeker`
  Look for the move with disproportionate upside.
- `implementation-realist`
  Favor the option that can actually happen soon.
- `adversarial-checker`
  Pressure-test risks, failure modes, and second-order effects.
- `simplifier`
  Reduce moving parts and decision burden.

## Return Shape

Each subagent should return:
- `candidate_title`
- `core_thesis`
- `main_tradeoff`
- `largest_assumption`
- `first_validation_step`

## Synthesis Rule

After the subagent pass:
- merge near-duplicates
- keep only materially different candidates
- explain the recommendation in terms of the stated decision criteria

Do not count the number of subagents as evidence quality by itself.
