---
name: research-router
description: 面向 AI 研究工作的总入口路由器。用于在查文献与建文献库、读论文、idea 澄清、新颖性压测、实验设计、结果分析、论文写作、slides/poster 与网页材料抓取之间选择最合适的下一步；当研究阶段不清楚、材料混杂、或用户只知道“想推进研究”时优先使用。
---

# Research Router

Use this as the public front door for AI research work.
Keep it thin: classify the current research stage, identify the main blocker, and route to the narrowest useful research skill.

Do not add a second routing hop unless it clearly improves the decision.
If the user already named the exact research skill they want, prefer the direct specialist entry.

## Use This Router For

- vague or mixed research requests
- a pile of papers, notes, runs, and half-formed ideas
- deciding whether the next step is finding papers, building a literature library, reading, sharpening, designing experiments, analyzing results, writing, or presenting
- research requests where the blocker is not yet obvious

## Do Not Use This Router For

- market research, competitor scans, or product discovery
  - use `delivery-router` or `business-analyst`
- architecture or system design for software products
  - use `architect-router`
- prompt optimization, official docs lookup, or PersonalBrain attachment
  - use `knowledge-router`

## Routing Table

1. `research-flow-navigator`
   Use when the request spans multiple research phases, the next step is unclear, or the user wants one coordinated research lane.

2. `literature-finder-downloader`
   Use for paper discovery, identifier recovery, accessible PDF download, and local literature-library bootstrapping from BibTeX, EndNote, RIS, DOI, arXiv, or title batches. Prefer this when the blocker is obtaining papers rather than understanding them. This lane can become context-heavy quickly; for large mixed batches, suggest a fresh subagent or fresh thread.

3. `research-paper-reading-compass`
   Use for paper reading, core claim extraction, positioning, and citation-context understanding.

4. `research-supplement-digestion`
   Use for appendix-level implementation details, hidden settings, reproduction clues, and long supplemental material.

5. `web-page-capture`
   Use for capturing a specific web page into reusable artifacts for later research use.

6. `research-idea-clarifier`
   Use when the idea is rough, hypotheses are weak, or the contribution needs sharper framing.

7. `research-novelty-audit`
   Use when the contribution claim needs prior-work pressure testing, reviewer-risk surfacing, or novelty positioning.

8. `research-experiment-design-planner`
   Use when the next step is experiment design, ablation planning, compute-aware evaluation, or success criteria design.

9. `research-training-and-ablation-loop`
   Use for reading runs, curves, ablations, and failure modes after experiments exist.

10. `research-paper-production-pipeline`
   Use for writing, rewriting, related-work positioning, abstract polish, response letters, and rebuttal packaging.

11. `research-slides-and-poster-studio`
   Use for talk decks, reading-group reports, posters, and research storytelling for presentation.

## Decision Rules

1. First classify the current research stage:
   - literature intake / acquisition
   - reading
   - idea shaping
   - novelty pressure test
   - experiment planning
   - result analysis
   - writing
   - presentation

2. Then identify the main blocker:
   - cannot find or obtain the right papers
   - understanding gap
   - contribution not sharp enough
   - experiment plan too weak
   - evidence not mature
   - narrative not clear

3. Route to the narrowest skill that removes the blocker fastest.

4. If more than one stage is genuinely active, use `research-flow-navigator` as the coordinating lane.

5. Avoid these bad jumps:
   - writing before novelty and evidence are clear
   - running lots of experiments before the idea is sharp
   - claiming novelty before prior work is compressed
   - debating results before the experiment contract is sound

## Direct-Entry Exceptions

Skip this router and use the specialist directly when:

- the user explicitly names `research-paper-reading-compass`, `research-novelty-audit`, `research-experiment-design-planner`, or another research specialist
- the user explicitly asks to find papers, download PDFs, or build a literature library from exports or identifier lists
- the request is obviously one-lane, such as “读这篇论文” or “给我设计 ablation matrix”
- the task is a single-page web capture with no broader research orchestration needed

## Output Contract

Always return:

- current research stage
- main blocker
- chosen skill
- why that lane is the best next move
- one concrete next action
- whether a direct specialist entry would be better next time

## Guardrails

- do not turn product-market research into AI research workflow
- do not route to writing just because it feels productive
- do not add a second specialist unless the task truly crosses phases
- if the best answer is “stay in the current skill and keep working,” say so explicitly

## Example Triggers

- `Use $research-router to decide whether I should read, design, analyze, or write next.`
- `使用 $research-router 看看我这堆论文、想法和 runs 该先处理哪一块。`
- `使用 $research-router 看看我该先查文献建库、先读论文，还是先做实验设计。`
- `Use $research-router to choose the best next research skill for this ambiguous project state.`
