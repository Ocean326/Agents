# Prompt Reliability

Use this reference when prompt quality is a workflow bottleneck rather than a one-off rewrite request.

Keep the boundary clean:
- if the task is only to rewrite a prompt, use `thinking-lenses`
- if prompt quality affects routing, handoff fidelity, tool use, schema adherence, or stop behavior, keep the design here and optionally delegate the rewrite step

## Failure Signatures

Common signs that the loop needs prompt refinement by design:

- controller keeps decomposing the task into smaller and smaller packets with no quality gain
- the agent keeps adding requirements that were never in scope
- workers keep escalating because the done condition is underspecified
- outputs repeatedly violate schemas or omit required evidence fields
- routing confidence stays low because route boundaries are unclear
- prompt wording conflicts with externalized state or approval status
- tool use is either too broad or too timid because the contract is vague
- handoff packets bloat because upstream prompts do not enforce scoped context

## Minimal Prompt Reliability Lane

When prompt quality is in scope, define:

1. `failure_signature`
   - what is going wrong, with one or two concrete trace examples
2. `refinement_trigger`
   - the measurable condition that allows prompt editing
3. `rewrite_owner`
   - who rewrites the prompt
   - default: delegate rewrite to `thinking-lenses`
4. `evaluation_bundle`
   - rubric
   - regression cases
   - pass threshold
   - max prompt revisions
5. `change_control`
   - who approves
   - when rollback happens
   - whether automatic prompt promotion is allowed

Do not create a prompt-refinement lane just because the workflow is imperfect.
Use it only when traces show the prompt contract is a material cause of failure.

## Prompt Refiner Input Packet

Send the refiner only the minimum packet needed:

- `current_prompt`
- `task_frame`
- `constraints`
- `output_contract`
- `failure_signature`
- `trace_snippets`
- `known_good_cases`
- `known_bad_cases`

Avoid passing the full session unless it is required to preserve nuance.

## Prompt Evaluation Bundle

Prompt changes should be evaluated separately from task output quality.

Minimum bundle:
- 3-10 regression cases
- one pass/fail rubric
- one threshold
- one plateau rule
- one rollback rule

Good rubric dimensions:
- scope discipline
- schema adherence
- tool-use clarity
- escalation clarity
- stop-rule clarity
- resistance to prompt drift or prompt injection

## Versioning and Rollback

Externalize prompt-change state whenever prompt quality affects control flow.

Useful fields:
- `prompt_pack_id`
- `prompt_pack_version`
- `prompt_revision_count`
- `prompt_quality_status`
- `prompt_regression_results`
- `prompt_change_approved`
- `rollback_to_version`

Rollback quickly when:
- the new prompt broadens scope
- regression failures increase
- the same guidance repeats without score improvement
- prompt edits create controller bottlenecks or worker confusion

## Anti-Patterns

- using prompt refinement to hide a broken topology
- grading the task output when the real defect is prompt ambiguity
- letting the refiner silently change the job-to-be-done
- shipping prompt edits with no regression cases
- letting prompts mutate while approval or state still points at an older version
