# Prompt Templates

## Lens Pair Defaults

- `clarify`
  - primary: `Socratic questioning`
  - support: `5 Whys` or `JTBD`
- `design`
  - primary: `First principles` or `Lateral thinking`
  - support: `MECE` or `SCAMPER`
- `decide`
  - primary: `MoSCoW`, `RICE`, or `Kano`
  - support: `Premortem` or `Inversion`
- `teach`
  - primary: `Bloom's taxonomy`
  - support: `Worked examples` or `Compare-and-contrast`
- `verify`
  - primary: `Acceptance criteria` or `Red-team critique`
  - support: `Test cases` or `Evidence tagging`

If the task is ambiguous, choose the simplest pair that clarifies intent without bloating the prompt.

## Delivery Mode Templates

### `inline-lite`

Use when the base request is already clear and only needs a little more structure.

```text
Before answering, restate the task in one sentence. Use {primary_method} with support from {supporting_method}. Keep the response concise, include the final recommendation, and name the main risk or tradeoff.
```

### `inline-structured`

Use for repeatable prompts, medium complexity, or handoff-friendly work.

```text
Goal:

Context:

Use this method:
- Primary lens: {primary_method}
- Supporting lens: {supporting_method}

Constraints:

Output:

Evaluation:
- clear
- actionable
- bounded
- verifiable
```

### `pre-optimizer`

Use only when the task is high-risk, high-cost, long-chain, or ambiguity-heavy.

```text
You are a prompt polisher.

Input task:
{raw_task}

Target scenario:
{target_scenario}

Required output:
1. Task restatement
2. Chosen primary and supporting methods
3. Optimized prompt for the executor
4. Remaining ambiguities
5. Main risks and failure modes
6. Brief edit rationale

Rules:
- Preserve user intent
- Do not expand scope
- Prefer one primary method and one supporting method
- Keep the executor prompt compact and operational
```

## Strict Additions

When `rigor = strict`, also call out:

- the biggest assumption
- the main failure mode
- the smallest missing detail that would most improve the prompt
