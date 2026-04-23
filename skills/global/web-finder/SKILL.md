---
name: web-finder
description: Local-first router for internet discovery and evidence synthesis across GitHub, official docs, blogs, forums, news, and social platforms. Use when Codex needs to search, discover, compare, or collect current external sources about a topic, repo, company, tool, trend, product, or discussion; choose an adaptive search path by source and freshness; capture high-value pages locally when helpful; and return a concise, source-backed synthesis instead of a loose link dump.
---

# Web Finder

## Overview

Use this skill as the top-level router for web discovery work.
Prefer local or self-hosted search and existing local skills first, then fall back to broader public web search, and only use API-key-dependent search when the chosen lane truly needs it.
The intended local-first companion stack is:
- `searxng-search` for broad local web search
- `web-page-capture` for post and page capture
- `article-extractor` for cleaned article text
- `reddit-fetch` for Reddit retrieval
- `youtube-transcript` for video-to-text follow-up

## Workflow

1. Normalize the request.
   Decide whether the user is asking for:
   - a source-specific search
   - a topic-first discovery pass
   - a comparison across sources
   - a current-state or recent-discussion sweep
   - a follow-up capture of already known URLs

2. Set the evidence target before searching.
   Decide:
   - freshness requirement: historical, recent, or latest
   - source mix: official, community, media, or mixed
   - deliverable: quick answer, source map, comparison brief, or reusable capture set

3. Check the environment only when needed.
   In a new environment, or when a lane depends on optional tooling, run `python3 ./scripts/check_setup.py`.
   Use `--json` only if machine-readable status is useful.

4. Choose the narrowest effective discovery lane.
   Use the routing table in [references/source-routing.md](./references/source-routing.md).
   Keep the search local-first:
   - existing MCP or connector search
   - `searxng-search` or another self-hosted local search stack
   - platform-specific fetch or capture skill
   - generic public web search
   - optional API-key-backed search

5. Search in small passes.
   Start with 1-3 focused queries, inspect the hit quality, then expand.
   Do not spray dozens of weak queries when the first pass already shows the right source family.

6. Capture only the pages worth reusing.
   When the result should survive beyond the current turn, capture priority pages into local artifacts instead of relying on transient browsing.
   Prefer:
   - `web-page-capture` for X, Zhihu, Xiaohongshu, and generic pages
   - `article-extractor` for blog and article cleanup
   - `reddit-fetch` for Reddit threads
   - `youtube-transcript` for YouTube text extraction

7. Synthesize, do not just list.
   Return:
   - a short framing of what was searched
   - the highest-signal sources
   - grouped findings
   - uncertainty or gaps
   - recommended next captures or follow-up searches

## Lane Selection

### GitHub and developer ecosystem

Prefer GitHub-native search surfaces first:
- repo search
- code search
- issue and PR search
- release or changelog pages

Use generic web search only to widen discovery around public discussion, comparisons, blog posts, or issue threads not surfaced well by platform-native search.

### Official docs, blogs, and product pages

Prefer self-hosted search if available locally.
If not, use targeted public web queries and domain filters.
Capture final pages locally when they are likely to be cited or revisited.

### Forums and communities

Prefer platform-aware routes over blind generic search.
For Reddit, prefer `reddit-fetch` if present.
For Hacker News, use a platform-specific lane if available; otherwise use targeted web search.

### Social posts and threads

If the URL is already known, switch from discovery to capture immediately.
If only the topic is known, discover candidate URLs first, then capture the strongest few.
Do not over-index on a single viral post when the user asked for broader discovery.

### Video and media

Discover first, then extract text.
Prefer transcript or page capture once you know which items are worth reading.

Read [references/query-recipes.md](./references/query-recipes.md) when query shaping or source-specific phrasing matters.

## Output Contract

Default response shape:

1. `Search frame`
   State what was searched, what freshness target was used, and which source families were included.

2. `Source map`
   List the most useful sources with:
   - title
   - URL
   - source type
   - freshness
   - why it matters

3. `Synthesis`
   Group findings by theme, not by search engine.
   Distinguish observed facts from inference when the evidence is mixed.

4. `Gaps`
   Name what is still uncertain, thinly sourced, or missing.

5. `Next step`
   Recommend the best follow-up:
   - deeper GitHub search
   - targeted forum sweep
   - page capture
   - transcript extraction
   - optional tool configuration

## Local-First Rules

- Prefer already-installed local skills and connectors before introducing new services.
- Treat optional API-key tools as upgrades, not prerequisites.
- Do not ask the user to configure everything up front.
- Ask for configuration only when a selected lane is blocked or would be materially better with that setup.
- If a missing tool is the only blocker, run `scripts/check_setup.py`, summarize exactly what is missing, and guide the user through only that configuration.

## Scope Control

- Favor 5-12 high-signal sources over noisy exhaustiveness unless the user explicitly asks for a broad scan.
- Prefer a mixed source set when the topic is controversial or fast-moving.
- Prefer official and primary sources when accuracy matters.
- Avoid turning one-page capture tools into whole-site crawlers.
- Avoid long verbatim excerpts when a short summary plus source links is enough.

## Common Triggers

- "Find recent discussions about this repo across GitHub and blogs."
- "Search the web for high-signal takes on this tool."
- "帮我按 GitHub、论坛、博客、社交平台把这个主题搜一遍。"
- "Find current sources about this startup and summarize the strongest evidence."
- "Discover articles, threads, and repo discussions about this framework."
- "Search broadly, then capture the best pages locally."
