---
name: skill-skill-usage-close-loop
description: Asynchronously close the loop on skills used in the current thread by routing to PersonalBrain's canonical `skill_skill_usage_close_loop` workflow, spawning one bounded background subagent, and appending per-skill evidence rows for later aggregate analysis. Use when a user explicitly asks to record, review, or retrospectively evaluate the performance of one or more skills used in the conversation without blocking the main task.
---

# Skill Usage Close Loop

## Overview

Use this skill as the global wrapper for PersonalBrain's canonical `skill_skill_usage_close_loop`.

Source of truth:

- `<PERSONALBRAIN_ROOT>/30_skills/meta/skill_skill_usage_close_loop.md`
- `<PERSONALBRAIN_ROOT>/40_governance/skill_evolution/ownership_registry.md`
- `<PERSONALBRAIN_ROOT>/40_governance/skill_evolution/results.tsv`

If the canonical PersonalBrain path is unavailable, stop and report that the durable close-loop target is missing instead of improvising a parallel ledger.

## Workflow

### 1. Resolve the canonical context

- treat the PersonalBrain skill file as the durable contract
- if already working inside PersonalBrain, operate there directly
- otherwise read the canonical file above before proceeding

### 2. Identify the review roster

- prefer the explicit skill list from the user
- otherwise infer only clearly used skills from the current thread
- skip ambiguous candidates rather than inventing a fake roster

### 3. Keep the main task unblocked

- spawn at most one bounded background subagent
- pass only the minimal task summary, reviewed skills, failures, touched artifacts, and verification signals
- do not wait by default while the main task still has critical-path work
- wait only if the user explicitly wants the review result now or the thread is already at a natural pause

### 4. Append the durable review ledger

- append one JSON object per reviewed skill to `<PERSONALBRAIN_ROOT>/40_governance/skill_evolution/usage_reviews.jsonl`
- create the file lazily on first real append
- use `eval_mode: thread_review_dry_run` unless stronger replay evidence actually exists

### 5. Route follow-up actions

- keep the review as passive evidence by default
- escalate recurring issues to the PersonalBrain dashboard when they become pattern-level, not one-off noise
- route canonical improvement work to the scorecard or Darwin optimizer flow instead of editing skills silently

## Review Row Shape

Include at least:

- `timestamp`
- `review_batch_id`
- `thread_scope`
- `reviewed_skill`
- `used_with`
- `task_summary`
- `observed_strengths`
- `observed_failures`
- `recommended_next_action`
- `evidence_refs`
- `eval_mode`
- `review_agent`
- `blocking_mode`

## Guardrails

- log meaningful skill usage, not every tool call
- keep private or low-signal session chatter out of durable memory
- do not silently edit canonical `30_skills/*.md`
- do not create a second ledger outside PersonalBrain
- record a deferred or partial review when evidence is too weak
