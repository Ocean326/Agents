# Site Note: Generic Pages

## Default Path

Use auto-detection or `--platform generic`.

The generic extractor is for:

- blogs
- documentation pages
- forum posts
- public article pages
- research notes

## Extraction Strategy

1. JSON-LD `articleBody` if present
2. `<article>` content
3. `<main>` content
4. fallback paragraph extraction

## Limitations

- login walls and heavy client-side apps may need cookies or browser assistance
- comments and dynamic widgets are not part of the default contract
- generic extraction favors readable article text, not exact DOM fidelity
