# Query Recipes

Use these as starting patterns, not rigid templates.
Run a small first pass, inspect results, then sharpen the next query.

## Broad Topic Split

For a topic-only request, usually run three query shapes:

1. Official or primary source
2. Community discussion
3. Recent change, comparison, or news

Example pattern:
- `"<topic>" official docs`
- `"<topic>" reddit OR hacker news OR forum`
- `"<topic>" latest OR comparison OR migration OR release`

## GitHub

- Repo discovery: `site:github.com "<topic>" "github"`
- Issue discussion: `site:github.com "<repo or topic>" issue`
- PR or release context: `site:github.com "<repo>" pull request OR releases`
- Adjacent blog coverage: `site:github.com "<topic>" blog OR release notes`

Prefer platform-native GitHub search when available for repos, code, issues, and PRs.

## Blogs, Docs, and Product Pages

- Official docs: `site:docs.example.com "<topic>"`
- Vendor blog: `site:blog.example.com "<topic>"`
- General article sweep: `"<topic>" tutorial OR guide OR blog`
- Migration or change notes: `"<topic>" migration OR breaking change OR changelog`

## Reddit and Forums

- Broad Reddit: `site:reddit.com "<topic>"`
- Subreddit-targeted: `site:reddit.com/r/<subreddit> "<topic>"`
- Forum sweep: `"<topic>" forum OR discussion OR thread`
- Compare opinions: `"<topic>" worth it OR alternatives OR review`

## Hacker News

- `site:news.ycombinator.com "<topic>"`
- `site:news.ycombinator.com "<company or repo>"`
- `site:news.ycombinator.com "<topic>" Show HN`

## X, Zhihu, Xiaohongshu

- X: `site:x.com "<topic>"`
- Zhihu: `site:zhihu.com "<topic>"`
- Xiaohongshu: `site:xiaohongshu.com "<topic>"` or `site:xhslink.com "<topic>"`

If you find a promising URL, stop broad searching and switch to capture.

## Freshness Shaping

Add one of these only when freshness matters:
- current year
- `latest`
- `recent`
- `today`
- `this week`
- `release`
- `announcement`

For unstable topics, vary the freshness phrasing instead of trusting one query.

## Precision Controls

- Add source hints: `official`, `docs`, `blog`, `forum`, `review`
- Add comparison hints: `vs`, `comparison`, `alternatives`
- Add exclusion hints when noise is high: `-jobs -hiring -course`
- Add domain filters when one source family matters more than breadth

## Stop Rules

- Stop broadening once you have enough high-signal sources for the requested deliverable.
- Stop repeating the same source family when results converge.
- Switch from search to capture once the target pages are clear.
