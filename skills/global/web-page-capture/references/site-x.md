# Site Note: X

## Default Path

Use the bundled script with auto-detection or `--platform x`.

The script prefers the public syndication endpoint because it works without login in many cases.

## Strengths

- stable public endpoint for many public posts
- no login required for ordinary public tweets
- good for text, author, post time, and basic engagement counts

## Known Limitation

Some long-form X posts expose only truncated `text` through the public syndication result and return a `note_tweet` stub without the full note text.

When that happens:

- keep the captured JSON/Markdown anyway
- record the limitation in `notes`
- if the task needs the full note, fall back to a browser-assisted path and preserve the same output contract

## Media

- photo URLs may be available directly
- video attachments may only expose a preview image in public capture mode
