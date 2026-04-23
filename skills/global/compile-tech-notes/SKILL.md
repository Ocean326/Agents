---
name: compile-tech-notes
description: "Compile fragmented local and external materials into report-grade deliverables with local-first evidence mapping, adaptive web discovery, and explicit separation of facts, judgments, inferences, decisions, and next actions. Use when Codex needs to turn meeting notes, transcripts, screenshots, task history, official docs, GitHub repos, blogs, forum threads, or personal notes into one of: (1) task update or work summary, (2) meeting/secretary memo with decisions and action items, (3) feasibility or recommendation brief, (4) material digest or source pack, (5) systematic technical learning note, or (6) blog-style synthesis. Acts as a report/secretary front door: pick the right deliverable, route to search or critique helpers when needed, and keep major claims traceable."
---

# Compile Tech Notes

## Overview

Use this skill as the top-level router for report, brief, summary, memo, and note-compilation work.
Turn scattered material into a deliverable that someone can act on, review later, share internally, or promote into durable knowledge.

Prefer a local-first workflow: start from the user's raw material, search externally only when a gap blocks a confident explanation, and keep every important claim traceable.

Write in the user's working language unless asked otherwise.
When writing in Chinese, preserve important English product names, APIs, or repository terms in parentheses when that reduces ambiguity.

This skill is no longer only for “技术学习笔记”.
It should now behave like a `报告 / 秘书` front door: choose the right report shape first, then synthesize.

## Boundaries

Do not use this skill for blank-page ideation.
If there is no stable topic, no central question, or no usable material, switch to ideation first.

Do not use this skill for pure search when the user only wants links or discovery and no compiled artifact.
Use `$web-finder` first, then come back if a report or digest is needed.

Do not use this skill for pure project delivery when the user actually needs execution ownership, not a document artifact.
Use `$delivery-conductor` when the main problem is driving work, not compiling it.

If the task is mostly paper reading, novelty pressure testing, or experiment planning, use `$research-router` to pick a narrower research skill.

Do not use this skill for communication-style coaching from meetings.
If the user wants to understand facilitation style, filler words, conflict avoidance, or leadership patterns, use `meeting-insights-analyzer`.

Do not promise a polished article, brief, or recommendation when the evidence only supports an outline or a gap memo.
Downgrade early instead of filling gaps with smooth prose.

## Deliverable Modes

Choose one primary deliverable using [references/deliverable-taxonomy.md](./references/deliverable-taxonomy.md):

- `task-status-update`
- `meeting-secretary-memo`
- `feasibility-brief`
- `material-digest`
- `systematic-learning-note`
- `blog-style-synthesis`

## Default Posture

1. Lock one primary deliverable.
Do not write before you know what artifact you are building.

Default tendencies:

- meeting transcript or sync notes -> `meeting-secretary-memo`
- task history, work log, checkpoint notes -> `task-status-update`
- many links/docs/screenshots needing整理 -> `material-digest`
- “should we do this” / “值得吗” / “怎么选” -> `feasibility-brief`
- technical concept consolidation -> `systematic-learning-note`
- public-facing shareout with strong evidence -> `blog-style-synthesis`

2. Treat the user's local material as the anchor source.
Use local notes, transcripts, screenshots, pasted text, and previously compiled notes to define the topic before browsing outward.

3. Separate evidence from organization.
The source says what happened; the artifact explains how to organize it.
Never hide the difference between fact, judgment, inference, extension, and operational follow-up.

4. Optimize for reuse, not just first-pass readability.
The draft should help the reader return later, act on it, or use it as the next decision surface.

5. Prefer strong intermediate objects over early prose.
If the contract, source map, action register, or outline is weak, keep working there.

## Workflow

### 1. Lock the job contract

State these items before doing heavy synthesis:

- `deliverable`
- `target_reader`
- `central_question`
- `time_window`
- `stop_condition`
- `innovation_budget`

Good central questions are answerable, narrow, and explanatory.
Bad central questions are just topic labels.

Examples:

- Good: `What problem is this platform actually solving, and how is the workflow organized end to end?`
- Good: `How did the speaker's local workflow change the usual cloud-first agent development model?`
- Good: `What changed this week, what is still blocked, and what should the reader pay attention to next?`
- Good: `What was actually decided in this meeting, and who owns the next actions?`
- Bad: `OpenJiuwen`
- Bad: `Today's meeting notes`

### 2. Choose the primary deliverable before outlining

Use [references/deliverable-taxonomy.md](./references/deliverable-taxonomy.md).
Do not keep the deliverable vague as `summary`.
Force one of the named modes unless the user gave an even more specific artifact.

### 3. Build the source map first

Create a source inventory before writing.
At minimum, record:

- source id
- title or label
- source type
- local or external
- confidence level
- why it matters
- which section or claim it supports

Use [references/evidence-model.md](./references/evidence-model.md) for source tiers, confidence rules, claim classification, and action extraction.

### 4. Normalize the material

Do the cleanup that turns raw capture into usable material:

- deduplicate repeated passages
- fix obvious ASR noise
- unify names, product terms, and abbreviations
- convert timeline-order notes into concept buckets
- mark unresolved terms instead of guessing
- extract candidate facts and open questions separately
- extract candidate decisions and action items separately when applicable

If the user already has several prior notes on the same topic, treat them as second-order sources rather than raw truth.
Mine them for recurring structure and stable claims, but keep them linked back to the underlying evidence where possible.

### 5. Decide whether external research is required

Browse only when at least one of these is true:

- the core mechanism is unclear from local material
- terminology is inconsistent or ambiguous
- a strong claim needs validation
- a missing official definition blocks the outline
- a comparison to the broader ecosystem is necessary
- the topic is time-sensitive and current truth matters
- the user explicitly wants a feasibility or current-state brief

When browsing, use this preference order:

1. official docs, official repos, source code, or speaker-provided material
2. strong engineering or technical blogs with clear authorship and concrete mechanisms
3. community discussions and forum threads for implementation experience or edge cases

Never use community discussion as the only support for a factual claim if a higher-confidence source should exist.

If external discovery is the blocker, use `$web-finder` first and then compile the result here.

### 6. Produce mandatory intermediate objects

Before drafting full prose, create these objects:

- `job_contract`
- `source_map`
- `claim_layers`
- `action_and_decision_register` when applicable
- `deliverable_outline`

Use [references/output-contract.md](./references/output-contract.md) for the exact object contract and draft templates.

### 7. Choose the narrative skeleton

Choose one primary skeleton instead of mixing three half-finished ones:

- `status-and-blockers`
  Use for work summaries, progress reports, and task records.
- `decision-and-actions`
  Use for meeting memos and secretary-style artifacts.
- `problem-driven`
  Use when the artifact answers why something exists and what problem it solves.
- `system-dissection`
  Use when the artifact explains components, layers, or workflow boundaries.
- `case-synthesis`
  Use when the artifact compares examples, materials, or usage styles.
- `comparison-evaluation`
  Use when the reader needs to understand tradeoffs between alternatives.

Use [references/report-and-synthesis-patterns.md](./references/report-and-synthesis-patterns.md) when the skeleton is unclear or when you need a reminder of mature reporting, briefing, and technical writing patterns.

### 8. Draft the deliverable

Use the skeleton that matches the chosen deliverable.
Do not force every output into a learning-note structure.

General writing rules:

- start with a useful answer, not a timeline replay
- explain why the reader should care before diving into detail
- group by theme, decision, or workstream, not by raw source order
- keep unresolved points visible instead of smoothing them away
- include owner / due / status when the artifact is operational
- include one reusable organizing frame whenever possible

Mode-specific emphasis:

- `task-status-update`
  Emphasize changes, evidence, blockers, and next actions.
- `meeting-secretary-memo`
  Emphasize decisions, action items, owners, and open questions.
- `feasibility-brief`
  Emphasize recommendation, evidence, tradeoffs, risks, and next move.
- `material-digest`
  Emphasize source grouping, signal vs. noise, and gaps.
- `systematic-learning-note`
  Emphasize central question, mechanisms, tradeoffs, and future reuse.
- `blog-style-synthesis`
  Emphasize narrative payoff, conceptual frame, and careful evidence.

### 9. Use helper skills when they materially improve the artifact

- use `$web-finder` when source discovery, recency, or ecosystem sweep is the blocker
- use `$proposal-critique-refine` for a critique pass on the outline or draft
- use `$delivery-conductor` when the user actually needs the project driven forward, not just documented
- use `$research-router` when the underlying work is really literature reading, novelty testing, or experiment design
- use `meeting-insights-analyzer` when the task is about communication behavior rather than meeting reporting

### 10. Run a critique pass before closeout

Use a lightweight `$proposal-critique-refine` pass on the draft or outline.
Check at least these three lenses:

- `value`: does this artifact help repeated study, action, or alignment, or is it just a prettier summary?
- `feasibility`: are the strongest claims truly supported by sources?
- `failure-mode`: did the structure accidentally inherit a note pattern and pretend it works for all report types?

Repair the most important 1 to 3 issues, then stop.

### 11. Downgrade gracefully when evidence is thin

If the material is insufficient, do not force a polished report.
Use one of these downgraded outcomes:

- `checkpoint-only`
- `source-map-plus-gaps`
- `options-and-gaps memo`
- `open-questions memo`

When sources conflict, preserve the conflict and label the current best-supported interpretation.

## Quality Gates

Do not call the work complete unless the output:

- answers the central question directly
- shows where the important claims came from
- separates fact, judgment, inference, and extension
- preserves decisions and action items as explicit registers when they matter
- contains at least one reusable organizing frame
- contains at least one action-oriented takeaway, checklist, or next-use hint
- avoids presenting unsupported extrapolation as fact

## Resources

Read only the reference that matches the current blocker:

- [references/deliverable-taxonomy.md](./references/deliverable-taxonomy.md)
  Use for choosing the primary artifact and avoiding note-shape overfitting.
- [references/evidence-model.md](./references/evidence-model.md)
  Use for source tiers, confidence rules, claim-layer classification, action extraction, and conflict handling.
- [references/output-contract.md](./references/output-contract.md)
  Use for the intermediate objects, source-map fields, action registers, and deliverable templates.
- [references/report-and-synthesis-patterns.md](./references/report-and-synthesis-patterns.md)
  Use for mature briefing, report, note, and synthesis patterns drawn from existing skills and technical writing references.
