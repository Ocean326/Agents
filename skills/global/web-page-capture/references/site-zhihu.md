# Site Note: Zhihu

## Default Path

Use the bundled script with auto-detection or `--platform zhihu`.

## What Usually Works

- public pages first
- private cookie if the page returns a challenge or `403`
- answer pages and article pages both map to the same output contract

## Common Failure Mode

Zhihu often returns a challenge page instead of the article or answer body.

Signs:

- HTTP `403`
- challenge HTML markers such as `zh-zse-ck`
- title/body reduced to login or challenge text

## Fix

Provide a cookie through a private env var or private file and retry.

Recommended cookie storage:

- `~/.codex/private/web-page-capture/zhihu.cookie`
- or repo-local `butler_private/zhihu_cookie.txt`

## Capture Notes

- image URLs may include site-hosted CDN assets
- the extracted body may come from JSON-LD or rich-text HTML
- comments are not part of the default capture contract
