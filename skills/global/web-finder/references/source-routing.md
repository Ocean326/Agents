# Source Routing

Use this table to pick the first discovery lane.
Stay local-first unless the selected lane clearly needs something broader.

| Situation | Prefer First | Then | Capture Follow-up |
| --- | --- | --- | --- |
| GitHub repo, issue, PR, release, code discussion | GitHub-native search surfaces or GitHub MCP | Public web search for surrounding discussion | Capture issue, PR, release, or linked posts only if they will be reused |
| Topic-only search about a tool, company, trend, or product | Local/self-hosted web search if available | Targeted public web search with domain filters | Capture the strongest official and community pages |
| Official documentation or vendor guidance | Domain-filtered search to official docs or vendor blog | Broader web search for comparisons or migration notes | Capture docs or blog pages that will be cited |
| Forum or community sentiment | Platform-specific lane such as Reddit or Hacker News | Generic web search with `site:` filters | Capture only the most representative threads |
| X, Zhihu, Xiaohongshu, or a known post/thread URL | Switch directly to capture | Use discovery only if URL is unknown | Use `web-page-capture` when available |
| Blog or article cleanup | `article-extractor` if available | Generic page capture | Save cleaned text if it will be reused |
| YouTube or video content | Discover candidate videos | Extract transcript | Keep transcript or notes, not raw media, unless requested |
| Broad comparison across official plus community sources | Search official lane first, then community lane | Add news or media only if useful | Capture a balanced sample across source families |

## Local-First Order

1. Existing platform-native or MCP search
2. Self-hosted local search such as a local SearXNG stack
3. Installed local capture or extraction skills
4. Generic public web search
5. API-key-backed search such as Tavily

## Practical Heuristics

- If the user names a platform, start there.
- If the user names a URL, capture rather than search.
- If the topic is breaking or recent, widen the source mix early.
- If the user wants durable notes, capture early.
- If a topic is controversial, mix official sources with community discussion before concluding.
