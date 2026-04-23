# Privacy And Cookies

## Allowed Cookie Sources

Use this precedence:

1. explicit CLI flags: `--cookie`, `--cookie-file`, `--cookie-env`
2. site-specific environment variables
3. ignored private files

## Recommended Private Locations

Preferred global private directory:

- `~/.codex/private/web-page-capture/`

Optional repo-local private directory when the project already ignores it:

- `./butler_private/`

Recommended filenames:

- `zhihu.cookie`
- `x.cookie`
- `xiaohongshu.cookie`

Common repo-local alternatives:

- `butler_private/zhihu_cookie.txt`
- `butler_private/x_cookie.txt`
- `butler_private/xiaohongshu_cookie.txt`

## Env Var Names

The bundled script checks these by site:

- Zhihu: `WEB_PAGE_CAPTURE_ZHIHU_COOKIE`, `ZHIHU_COOKIE`
- X: `WEB_PAGE_CAPTURE_X_COOKIE`, `X_COOKIE`, `TWITTER_COOKIE`
- Xiaohongshu: `WEB_PAGE_CAPTURE_XIAOHONGSHU_COOKIE`, `XIAOHONGSHU_COOKIE`, `XHS_COOKIE`

## Rules

- never store real cookie values in tracked files
- never echo cookie values into summaries or handoff notes
- keep cookies in private storage only
- keep final outputs and images, but not undeclared caches
- if a browser fallback is used, remove transient browser profiles after capture
