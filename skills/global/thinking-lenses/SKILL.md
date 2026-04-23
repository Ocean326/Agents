---
name: thinking-lenses
description: "Optimize prompts by routing requests into inline-lite, inline-structured, or pre-optimizer modes, then rewrite them using one primary reasoning lens plus one supporting lens. Use when a prompt is underspecified, repetitive, handoff-oriented, high-cost, or high-risk, and needs clearer goals, constraints, output contracts, evaluation criteria, or tighter reasoning before another agent or model executes it. Common triggers include: improve this prompt, rewrite this for another agent, make this task more structured, choose the right reasoning framework, or stress-test this prompt before running it."
---

# Thinking Lenses

Optimize a task prompt without turning prompt polish into a mandatory heavy workflow.

## Quick Start

- Skip this skill if the request is already simple, clear, and low-stakes.
- Use `inline-lite` for short one-shot tasks that only need a little more structure.
- Use `inline-structured` for recurring work, medium complexity, or handoff-friendly prompts.
- Use `pre-optimizer` only for high-risk, high-cost, long-chain, or ambiguity-heavy tasks.
- Read [prompt-templates.md](./references/prompt-templates.md) when choosing a lens pair or assembling the final prompt.

## Inputs

- `task`
  - the raw prompt, request, or task description
- `mode`
  - one of: `clarify`, `design`, `decide`, `teach`, `verify`
- `constraints`
  - hard limits, style limits, banned moves, budget, timing, or safety boundaries
- `output_contract`
  - the required deliverable shape, sections, format, or acceptance criteria
- `rigor`
  - `light` by default, `strict` when ambiguity or failure cost is high
- `delivery_mode`
  - optional override: `inline-lite`, `inline-structured`, or `pre-optimizer`

If `mode` is missing, infer the closest fit.
If `constraints` or `output_contract` are missing, infer only the minimum needed and name the biggest assumption.

## Workflow

1. Restate the real task in one or two sentences.
2. Capture the goal, audience, constraints, and what a good output must do.
3. Route the request into the lightest delivery mode that still protects quality.
4. Choose exactly one primary lens and one supporting lens.
5. Produce a compact optimized prompt rather than a long explanation about frameworks.
6. Add ambiguity and risk notes only when `rigor = strict` or `delivery_mode = pre-optimizer`.

Default output sections:

1. `Task restatement`
2. `Method choice`
3. `Optimized prompt`

Add these only for stricter runs:

4. `Ambiguities`
5. `Risks`
6. `Edit rationale`

## Guardrails

- Use exactly one primary lens and one supporting lens.
- Prefer the lowest-friction delivery mode unless escalation is justified.
- Preserve user intent and wording when nuance matters.
- Do not expand scope while "improving" the prompt.
- Make the output contract verifiable when another agent or model will execute the result.
- Keep the optimized prompt shorter than the explanation about it.
- Avoid forcing a second agent when the task is simple enough to handle inline.

## Failure Modes

- Over-framework a trivial request.
- Stack many methods into one bloated prompt.
- Explain the methods instead of producing an operational prompt.
- Quietly change the scope while polishing the task.
- Default to a separate optimizer pass even when the task is low-stakes.
- Omit evaluation criteria, making the prompt sound smart but hard to verify.

## Reference Use

- Read [prompt-templates.md](./references/prompt-templates.md) when:
  - `mode` is ambiguous
  - choosing the primary/supporting pair
  - converting the result into `inline-lite`, `inline-structured`, or `pre-optimizer`
  - tightening the output contract for another agent
