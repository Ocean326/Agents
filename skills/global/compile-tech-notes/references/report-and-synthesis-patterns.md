# Report And Synthesis Patterns

Use this reference when the draft needs a stronger reporting shape, a more useful briefing style, or a more mature synthesis pattern.
The goal is not to imitate any one skill or article.
Borrow the moves that make reports and notes genuinely useful:

- clear reader and purpose
- fast situational awareness
- explicit decisions and actions
- strong evidence discipline
- concise synthesis before detail
- reusable structure

## Distilled patterns from existing skills

### 1. Meeting secretary pattern

Borrowed from:

- `marcklingen/personal-productivity` meeting notes skill
- local `meeting-insights-analyzer` as a contrast case

Useful moves:

- separate `notes mode` from `tasks mode`
- always extract action items, commitments, and meeting-specific next steps
- merge multiple sources for the same meeting when they complement each other
- do not replay the transcript when the user really needs decisions and owners

What to borrow here:

- `meeting-secretary-memo` should default to decisions, action items, open questions, and who owns what
- when the request is about behavior coaching or communication style, route to `meeting-insights-analyzer` instead of pretending this is a secretary memo

### 2. Team brief pattern

Borrowed from:

- `huytieu/COG-second-brain` team brief skill
- `opencodos/opencodos` Morning Brief

Useful moves:

- cross-reference signals from multiple operational sources
- lead with what needs attention, not just what exists
- include carryover, priorities, blockers, and follow-ups
- write like a teammate, not like a dashboard export

What to borrow here:

- `task-status-update` and `feasibility-brief` should surface carryover, blockers, and leverage
- concise synthesis should come before the long detail dump

### 3. Situational awareness brief pattern

Borrowed from:

- `ken-cavanagh-glean/fieldkit` account brief

Useful moves:

- start from current state, checklist progress, risks, last interaction, and open to-dos
- combine local record with fresher external or system-of-record inputs
- optimize for “what do I need to know before I act”

What to borrow here:

- `feasibility-brief` and `task-status-update` should include a quick situation block near the top
- do not bury the main risk or next move

### 4. Markdown report pattern

Borrowed from:

- `jnotsknab/mux-swarm` markdown-report

Useful moves:

- lead with conclusions, not process
- use a one-line summary and short TL;DR
- organize by topic, not by source list
- keep sections scannable and source-backed

What to borrow here:

- every deliverable should have an opening answer or synthesis block
- sources should support the draft, not replace it

## Mature writing references beyond skills

### Google Technical Writing

Borrow:

- define scope and audience early
- summarize key points near the start
- compare new ideas to familiar ones
- organize around what the reader should know or do next

Useful source:

- [Google Technical Writing: Documents](https://developers.google.com/tech-writing/one/documents)

### Write the Docs

Borrow:

- make sections discoverable and addressable
- order prerequisites before dependent ideas
- either cover a chosen concept fully or label the coverage as partial

Useful source:

- [Write the Docs: Documentation principles](https://www.writethedocs.org/guide/writing/docs-principles/)

### Progressive Summarization

Borrow:

- capture first, compress later
- summarize in layers instead of trying to get the final abstraction right immediately
- optimize for future rediscovery

Useful source:

- [Progressive Summarization](https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/)

### Technical blog exemplars

Borrow:

- explain the old pain before the new structure
- show system layers and tradeoffs, not just features
- publish reusable conceptual frames rather than raw event logs

Useful sources:

- [Stripe: How Stripe builds interactive docs with Markdoc](https://stripe.com/blog/markdoc)
- [Cloudflare: the technology behind Cloudflare Radar 2.0](https://blog.cloudflare.com/technology-behind-radar2/)
- [Martin Fowler: Writing Fragments](https://martinfowler.com/articles/writing-fragments.html)

## Anti-patterns

Avoid:

- a polished intro with no reporting question
- a beautiful note with no action register
- a meeting memo with no owners
- a feasibility brief with no downside analysis
- a material digest that is really just annotated bookmarks
- a status report that lists activity but does not change any decision

## Source examples used for this pattern map

- [marcklingen/personal-productivity](https://github.com/marcklingen/personal-productivity)
- [huytieu/COG-second-brain](https://github.com/huytieu/COG-second-brain)
- [jnotsknab/mux-swarm](https://github.com/jnotsknab/mux-swarm)
- [ken-cavanagh-glean/fieldkit](https://github.com/ken-cavanagh-glean/fieldkit)
- [opencodos/opencodos](https://github.com/opencodos/opencodos)
