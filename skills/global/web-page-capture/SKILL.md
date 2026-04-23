---
name: web-page-capture
description: Capture a single web page into JSON, Markdown, handoff notes, and downloaded images. Use when a user provides a Zhihu, X, Xiaohongshu, or generic article URL and wants reusable local artifacts for follow-on agent work; the skill auto-detects the site, prefers private cookies from env or ignored files, and avoids leaving undeclared caches behind.
---

# Web Page Capture

## Overview

Use this skill when the task is "pull the contents of this page/post/thread so another agent can keep working from local artifacts".
It gives one entrypoint for site detection, capture, image download, and handoff output, while keeping cookies in private storage and avoiding stray caches.

## When To Use It

Use `$web-page-capture` when:

- the user gives one or more page URLs and wants the actual page contents extracted
- the output needs to be reusable by another agent without re-fetching the page
- the page includes important images that should be downloaded locally
- the page may require a site-specific cookie or authenticated fetch
- the target is one of: `zhihu`, `x`, `xiaohongshu`, or a normal article page

Do not use it for:

- whole-site crawling
- login-heavy product UIs that need a persistent browser session
- API integrations where the user actually wants structured API data instead of page capture
- pages that are already provided inline in the prompt

## Quick Start

Use the bundled script:

```bash
python3 $CODEX_HOME/skills/web-page-capture/scripts/capture_page.py \
  "https://example.com/article" \
  --output-dir /absolute/path/to/output
```

Recommended output location:

- use a declared task output folder such as `工作区/.../web_capture_*`
- do not scatter capture artifacts across the repo root
- do not keep raw caches unless the task explicitly asks for them

The script writes:

- `*.json`
- `*.md`
- `*_handoff.md`
- `images/` for downloaded images

## Workflow

1. Pick a declared output directory for this task.
2. Run `capture_page.py` with the source URL or share text.
3. Let the script auto-detect the site unless you need `--platform`.
4. If the site is gated, provide a cookie through a private env var or ignored private file.
5. Read the generated `*_handoff.md` first when handing off to another agent.
6. Continue from the local artifacts; do not re-crawl unless the capture is incomplete.

## Output Contract

Every successful capture should produce the same four surfaces:

- JSON: structured fields for programmatic follow-up
- Markdown: human-readable capture
- handoff Markdown: what the next agent should read first
- local images: downloaded into `images/` and referenced from JSON/Markdown

Read [output-contract.md](./references/output-contract.md) if you need the expected keys and handoff behavior.

## Privacy And Cache Rules

- Never paste real cookies into `SKILL.md`, `references/`, repo-tracked files, or final user-facing notes.
- Prefer explicit env vars or ignored private files.
- The bundled script is cacheless by default: it keeps only declared outputs and downloaded images.
- If you use browser automation as a fallback, clean transient browser data after capture unless the user explicitly asks to retain it.

Read [privacy-and-cookies.md](./references/privacy-and-cookies.md) before handling authenticated pages.

## Site Notes

- Zhihu: [site-zhihu.md](./references/site-zhihu.md)
- X: [site-x.md](./references/site-x.md)
- Xiaohongshu: [site-xiaohongshu.md](./references/site-xiaohongshu.md)
- Generic article pages: [site-generic.md](./references/site-generic.md)

Read only the site note that matches the detected platform.

## Fallback Policy

The bundled script is the default path because it is deterministic and does not depend on a heavyweight browser.

If capture is incomplete:

1. try a private cookie for the site
2. retry with a site hint via `--platform`
3. if the page is still incomplete and the task justifies it, use a browser-assisted capture path
4. keep the same output contract and delete transient browser caches afterwards

## Common Commands

Zhihu with a private cookie file:

```bash
python3 $CODEX_HOME/skills/web-page-capture/scripts/capture_page.py \
  "https://www.zhihu.com/question/.../answer/..." \
  --output-dir /absolute/path/to/output
```

X post:

```bash
python3 $CODEX_HOME/skills/web-page-capture/scripts/capture_page.py \
  "https://x.com/user/status/1234567890" \
  --output-dir /absolute/path/to/output
```

Xiaohongshu share text or short link:

```bash
python3 $CODEX_HOME/skills/web-page-capture/scripts/capture_page.py \
  "share text with http://xhslink.com/..." \
  --output-dir /absolute/path/to/output
```

## Expected Agent Behavior

- Start from the generated `*_handoff.md`.
- If `should_read_images_first` is `true`, inspect the downloaded local images before summarizing.
- When replying to the user, treat the local capture artifacts as the working truth for that page.
- If the capture failed, report the exact blocker and the next private input needed, such as a cookie.
