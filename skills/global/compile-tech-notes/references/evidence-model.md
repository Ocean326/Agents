# Evidence Model

Use this reference when deciding what to search, how much to trust each source, how to classify claims, and how to extract decisions and action items without overclaiming.

## 1. Source priority

Prefer sources in this order unless the task itself is about community sentiment:

1. `local operational material`
   Examples: meeting transcripts, screenshots, task logs, personal notes, captured chats, prior notes, checkpoints, speaker slides.
   Best for: event-specific facts, who said what, what changed in this thread, what was actually decided or shown.

2. `official or system-of-record material`
   Examples: official docs, product pages, repositories, source code, release notes, specs, tracker state, speaker-provided links.
   Best for: definitions, current behavior, APIs, architecture, supported workflows, current task or status truth.

3. `mature technical blogs`
   Examples: Cloudflare Blog, Stripe Engineering, Martin Fowler, strong engineering team writeups with named authors.
   Best for: system explanations, tradeoffs, implementation lessons, narrative structure, comparable patterns.

4. `community discussion`
   Examples: forum posts, GitHub issues, Reddit, Hacker News discussions.
   Best for: edge cases, confusion points, practical friction, debugging breadcrumbs.

5. `prior synthesized notes`
   Examples: previous learning notes, internal briefs, prior summaries, earlier reports.
   Best for: recurring structure and previous conclusions.
   Caution: treat as second-order sources, not raw truth.

Community discussion is supporting evidence, not default truth.
Prior synthesized notes are reusable, but should be linked back to better anchors when possible.

## 2. Trigger external research only when needed

Stay local-first.
Trigger external research only when one of these conditions holds:

- the local material cannot define the core mechanism
- the note needs current truth and the local material may be stale
- the note makes a strong claim that should be validated
- terminology, naming, or platform boundaries are unclear
- the reader would not understand the topic without external comparison
- a missing official artifact blocks the source map
- the user explicitly wants a current-state brief or feasibility answer

If none of the above applies, keep the workflow local-first and use the user's material as the primary evidence base.

## 3. Source map schema

Record the source map in a compact table with these fields:

| id | source | type | confidence | role | supports |
| --- | --- | --- | --- | --- | --- |
| S1 | internal transcript | local raw | high for event facts, low for exact terminology | anchor | intro, decisions, action register |

Guidance:

- `type`: local raw, official, technical blog, forum, prior note, task history
- `confidence`: high, medium, low, with a brief reason when non-obvious
- `role`: anchor, validator, comparator, background, edge-case witness, system-of-record
- `supports`: section names, claim ids, paragraph roles, or action/decision rows

## 4. Claim layers

Every important statement should fit one of these buckets.
When in doubt, classify downward conservatively.

### `fact`

Use when the statement is directly supported by a traceable source.

Tests:

- Can you point to a source that explicitly states or shows it?
- Would the wording survive quotation or close paraphrase?
- If time-sensitive, do you know when it was true?

### `judgment`

Use when the statement is an evaluative choice about importance, emphasis, or interpretation.

Tests:

- Is this a prioritization or framing choice rather than a bare fact?
- Would another careful reader possibly rank it differently?

### `inference`

Use when the statement is concluded from several facts or from incomplete evidence.

Tests:

- Is the conclusion reasonable but not explicitly stated?
- Does it depend on combining multiple sources or reading between the lines?

### `extension`

Use when the statement intentionally goes beyond the sources.

Tests:

- Is this a generalization, analogy, proposed pattern, or future-looking idea?
- Would the original source owner reasonably say, "That goes beyond what I claimed"?

## 5. Conflict handling

When two sources disagree:

1. Prefer the higher-confidence source for factual claims.
2. Prefer the more local source when the question is `what happened in this event`.
3. Prefer the more recent source when the question is current product behavior.
4. Preserve the disagreement explicitly if the conflict cannot be cleanly resolved.

Do not silently merge incompatible claims into bland prose.

## 6. Decisions and action items

For report and secretary work, decisions and action items need their own discipline.

### Decision extraction

Mark something as a decision only when one of these is true:

- it is explicitly agreed in the source
- it is recorded as next plan in a system-of-record artifact
- the speaker or owner clearly commits to the direction

If the material only suggests a direction but does not settle it, label it as:

- `candidate decision`
- `proposed next step`
- or `open question`

### Action item extraction

An action item is strongest when you can identify:

- what needs to be done
- who owns it
- by when
- where the commitment came from

If one or more of these fields is missing:

- keep the action item, but lower confidence
- do not invent owner or due date
- say `owner unclear`, `due date not stated`, or `inferred from context`

### Status wording

Use compact, evidence-matching statuses:

- `agreed`
- `open`
- `blocked`
- `inferred`
- `unclear`

## 7. Safe wording rules

Use wording that matches evidence strength.

- `fact`: `X does`, `the speaker said`, `the repo contains`
- `judgment`: `the key takeaway is`, `the most useful lens is`
- `inference`: `this suggests`, `this likely means`, `one plausible reading is`
- `extension`: `a useful extension is`, `we can generalize this into`

For actions and decisions:

- `confirmed action`: `X will do Y`, `the team agreed to Y`, `next step is Y`
- `inferred follow-up`: `a likely next action is`, `this suggests a follow-up to`
- `unresolved`: `it remains unclear whether`, `ownership is not explicit`

## 8. Browsing checklist

Before adding an external source, answer:

1. What specific gap does this source close?
2. Why is this source a better fit than local material?
3. Which section, claim, or decision/action row will it support?

If you cannot answer all three, skip the source.
