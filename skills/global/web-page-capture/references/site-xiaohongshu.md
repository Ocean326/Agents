# Site Note: Xiaohongshu

## Default Path

Use the bundled script with auto-detection or `--platform xiaohongshu`.

It accepts:

- full share URLs
- `xhslink.com` short links
- share text that contains a short link

## What It Extracts Reliably

- note id
- title or first visible line
- author
- main description text
- image URLs
- basic engagement counters when present on the share page

## Known Limitation

The default capture uses the share-page HTML and does not collect full comments.

## Follow-On Behavior

If the note is image-heavy and text-light, the handoff will usually recommend reading local images first.
