# Review Packet Contract

## Objects

### `review_batch_manifest`

Use this object to freeze the batch before deep review.

Required fields:

- `review_batch_id`
- `primary_lane`
- `selected_rollouts`
- `selection_reason`
- `stop_condition`

Optional fields:

- `thread_candidates`
- `notes`

### `session_review_packet`

Use this object for one rollout file.

Required fields:

- `schema_version`
- `packet_id`
- `source.rollout_file`
- `source.session_id`
- `observations`
- `inferences`
- `manual_fill`

Recommended observation fields:

- `cwd`
- `started_at`
- `top_level_event_counts`
- `response_item_counts`
- `tool_calls_by_name`
- `custom_tools_by_name`
- `web_queries`
- `message_role_counts`
- `verification_signal_hits`
- `closeout_signal_hits`

Recommended inference fields:

- `suggested_labels`
- `suggested_routes`
- `candidate_hints`
- `confidence`
- `notes`

Recommended manual fields:

- `task_summary`
- `successes`
- `failures`
- `pattern_labels`
- `candidate_cues`
- `route_override`
- `next_action`
- `notes`

### `evolution_candidate`

Use this object only after at least one packet exists.

Required fields:

- `candidate_id`
- `candidate_type`
- `evidence_packets`
- `intended_benefit`
- `tradeoff`
- `evaluation_plan`
- `suggested_owner`

Allowed `candidate_type` values:

- `workflow`
- `prompt`
- `skill_patch`
- `defer`

### `evolution_decision`

Use this object when a candidate reaches a real decision point.

Required fields:

- `candidate_id`
- `decision`
- `evidence_refs`
- `evaluation_mode`
- `approval_state`

Allowed `decision` values:

- `keep`
- `revert`
- `queue`
- `defer`

## Minimal Packet Example

```json
{
  "schema_version": "codex_session_review_packet_v0_1",
  "packet_id": "review_packet_019d70a4",
  "source": {
    "rollout_file": "$CODEX_HOME/archived_sessions/rollout-....jsonl",
    "session_id": "019d70a4-...."
  },
  "observations": {
    "top_level_event_counts": {
      "function_call": 214
    }
  },
  "inferences": {
    "suggested_labels": [
      "exploration-heavy",
      "verification-thin"
    ],
    "suggested_routes": [
      "workflow"
    ]
  },
  "manual_fill": {
    "task_summary": "",
    "pattern_labels": [],
    "candidate_cues": [],
    "route_override": ""
  }
}
```

## Durable Write Boundary

Safe to promote:

- short task summaries
- pattern labels
- candidate cues
- evidence refs
- sanitized observations

Keep machine-local:

- raw transcript blocks
- full tool outputs
- hidden instructions
- large copied argument payloads

## Promotion Rule

Promote a pattern only when it is:

- repeated
- decision-relevant
- attributable to evidence packets
- small enough to route into one downstream owner
