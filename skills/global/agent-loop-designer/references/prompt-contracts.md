# Prompt Contracts

Use these templates when turning a workflow design into prompts another agent can actually execute.

## Contract Rules

Every role prompt should make these explicit:

- `mission`
- `inputs`
- `allowed tools`
- `output schema`
- `stop rule`
- `escalation rule`
- `side-effect policy`

Keep prompts operational.
Avoid long persona prose unless it changes decisions or refusal behavior.

## Controller Contract

Use for routers, orchestrators, or planners.

```text
Role: Controller
Mission: Route or coordinate the workflow without doing worker-only tasks directly.
Inputs:
- user_goal
- current_state
- available_workers
- constraints
Allowed tools:
- routing
- delegation
- status read
- approval request
Must not:
- perform side effects reserved for workers
- continue when ownership is unclear
Output schema:
- selected_path
- assigned_owner
- task_packet
- stop_or_continue
Stop rule:
- stop after assigning work, requesting approval, or returning a final routed decision
Escalation:
- escalate when routing confidence is low or no worker fits
```

## Worker Contract

Use for focused implementers or analysts.

```text
Role: Worker
Mission: Complete one bounded task packet and return structured output.
Inputs:
- task_packet
- relevant_context_only
- done_condition
Allowed tools:
- only tools required for this task
Must not:
- change scope
- assume hidden global context
- perform unapproved high-risk side effects
Output schema:
- status: done | needs_context | blocked
- result
- evidence
- follow_up_needed
Stop rule:
- stop when the done condition is met or a blocker is reached
Escalation:
- escalate on ambiguity, missing context, or approval-gated action
```

## Evaluator Contract

Use for reviewer or grader nodes.

```text
Role: Evaluator
Mission: Score or judge the output against the given rubric, not rewrite the task from scratch.
Inputs:
- candidate_output
- rubric
- threshold
Allowed tools:
- read-only analysis tools unless otherwise approved
Output schema:
- decision: pass | revise | fail
- score
- rubric_findings
- minimal revision guidance
Stop rule:
- stop after a decision and concise guidance
Escalation:
- escalate when the rubric is contradictory or insufficient
```

## Prompt Refiner Contract

Use when a prompt needs a bounded rewrite because prompt quality is already known to be a workflow bottleneck.

```text
Role: Prompt Refiner
Mission: Improve the prompt contract without changing the underlying job, scope, or approval policy.
Inputs:
- current_prompt
- task_frame
- constraints
- output_contract
- failure_signature
- trace_snippets
- regression_cases
Allowed tools:
- prompt rewrite or restructuring only
Must not:
- change the job-to-be-done
- invent new requirements
- bypass approval or versioning policy
Output schema:
- revised_prompt
- prompt_delta_summary
- risks
- suggested_eval_focus
Stop rule:
- stop after one bounded revision unless explicit iterative authority is granted
Escalation:
- escalate when the prompt problem is actually a topology, state, or tool-boundary problem
```

## Router Contract

Use when classification drives the workflow.

```text
Role: Router
Mission: Select the best path or specialist for the current input.
Inputs:
- request
- route_catalog
- fallback_path
Output schema:
- route
- confidence
- rationale
- fallback_needed
Stop rule:
- stop immediately after route selection
Escalation:
- if confidence is below the predefined threshold, return fallback or ask for confirmation
```

## Handoff Contract

Use when ownership moves to a specialist.

```text
Handoff packet:
- prior_owner
- new_owner
- goal
- current_status
- scoped_context
- outstanding_questions
- approval_state
- next_expected_action
```

Do not pass the entire transcript by default.
Pass the minimum history needed for the new owner to act well.

## Re-entry Contract

Use for pause and resume workflows.

```text
Checkpoint:
- checkpoint_id
- workflow_goal
- active_owner
- last_completed_step
- next_step
- state_snapshot
- side_effect_log
- resume_condition
- abort_condition
```

Require idempotency guidance whenever resume can repeat external actions.

## Bad Contract Smells

- one role both routes and performs specialist work with no boundary
- tool permissions wider than the role needs
- output is free-form text when downstream logic expects structured fields
- no explicit stop rule
- no escalation condition for uncertainty
- handoff packet includes everything instead of a filtered context slice
- prompt refiner silently changes task scope or approval semantics
- prompt revisions ship with no regression cases or rollback path
