---
name: literature-finder-downloader
description: End-to-end paper discovery, identifier recovery, accessible PDF download, and local literature library bootstrapping. Use when Codex needs to turn BibTeX, EndNote `.enw`, RIS, DOI or arXiv lists, title batches, or a vague "帮我把这些文献找齐并落到本地" request into local artifacts with metadata tables, OA or publisher links, downloaded PDFs, unresolved items, and a clean handoff. Prefer this when the blocker is finding or obtaining papers rather than reading, critiquing, or writing about them.
---

# Literature Finder Downloader

## Overview

Use this skill to finish the literature-intake lane end to end: normalize the user's source material, recover stable identifiers, locate accessible PDFs, download what is actually obtainable, and leave a local artifact pack plus an exact next-step handoff.

Treat this as a delivery lane, not a search-only lane. The job is not complete when links are found; the job is complete when the local library seed, unresolved list, and verification summary all exist.

This lane is context-heavy. For large or mixed batches, for example more than 30 records, multiple export formats, mixed title and DOI inputs, or several source families, recommend opening a fresh subagent or fresh thread to preserve mainline context. If the user explicitly allows subagents, prefer one bounded worker for the long acquisition pass while the main thread keeps ownership of synthesis, verification, and handoff.

## Workflow

### 1. Sweep the input and choose one primary mode

Classify the request before acting:

- `batch-bootstrap`
  - the user already has a `.bib`, `.enw`, `.ris`, or identifier list and wants a library seed
- `search-and-acquire`
  - the user has titles, topics, or partial citations and needs the papers found first
- `acquisition-followup`
  - a library seed already exists and the next step is resolving remaining inaccessible items
- `arxiv-enrichment`
  - the user mostly wants structured arXiv content, TLDRs, or GitHub links after acquisition

Lock one primary mode. Do not let reading, novelty critique, or writing displace the acquisition lane.

### 2. Separate the three layers

Keep these layers explicit:

- `metadata backbone`
  - title, authors, year, venue, DOI, URL, citation export
- `acquisition handle`
  - OA PDF URL, DOI landing page, repository mirror, or publisher page
- `local attachment`
  - the PDF actually downloaded into the workspace

Never collapse these into one status. A paper can be found without being downloaded, and it can be downloaded without having clean metadata.

Read [references/source-stack.md](./references/source-stack.md) when you need the full architecture for OpenAlex, DOI landing pages, DeepXiv, and Zotero roles.

### 3. Prefer the narrowest reliable source stack

Default order:

1. Use standardized exports as the metadata backbone.
   - Prefer `.bib` when both `.bib` and `.enw` describe the same batch.
2. Resolve DOI or arXiv identifiers first.
3. Use OpenAlex to classify OA vs non-OA and get the best available landing or PDF URL.
4. Use title-level recovery only for the records that still lack stable identifiers.
5. Use DeepXiv only for the arXiv-friendly subset when content enrichment is needed after acquisition.
6. Use Zotero as the durable long-term home when the user wants a true literature library, not just a one-off batch folder.

Do not present DeepXiv as a replacement for local bibliography management.

### 4. Use the bundled bootstrap script for batch formation

Use `scripts/bootstrap_literature_library.py` when the user already has exports or identifier lists and wants a local seed library.

Supported inputs:

- `.bib`
- `.enw`
- `.ris`
- plain-text identifier lists with one DOI, arXiv id, URL, or title per line

The script creates a local artifact pack with:

- `references.csv`
- `references.md`
- `summary.json`
- `zotero_identifiers.txt`
- `oa_pdf_urls.txt`
- `remaining_oa_to_resolve.csv`
- `remaining_oa_to_resolve.md`
- optional `pdfs/` when downloads are requested

Use `--manual-overrides path/to/overrides.json` when title-level recovery needs stable local corrections. Keep overrides explicit instead of silently patching rows.

### 5. Download conservatively and verify honestly

When downloading PDFs:

- only count a file as downloaded if the response really is a PDF
- check `Content-Type` and the `%PDF` header, not just the URL suffix
- expect some OA URLs to return `403`, HTML, or repository landing pages
- move those items into `remaining_oa_to_resolve` instead of looping forever

Do not claim success just because OpenAlex marked a record as OA. OA classification and automated retrieval are different gates.

### 6. Close the lane with a delivery-style handoff

End every run with:

- total record count
- direct OA count
- actually downloaded PDF count
- unresolved OA-direct-link count
- unresolved publisher-access count
- the exact local output directory
- the strongest next action

Recommended next actions after acquisition:

- route to `research-paper-reading-compass` for paper reading
- route to `research-novelty-audit` for positioning and prior-work pressure testing
- route to `research-paper-production-pipeline` for writing
- stay in this skill for another bounded acquisition pass if the blocker is still finding or obtaining papers

## Verification

Before saying the lane is done:

1. verify the script completed without crashing
2. verify the expected output files exist
3. verify the downloaded PDF count by inspecting the `pdfs/` directory
4. verify at least a small sample of downloaded files with `file` or equivalent
5. report the remaining failure modes explicitly

If `quick_validate.py` is unavailable or blocked by missing dependencies, do a manual validation pass on frontmatter shape, `agents/openai.yaml`, and script execution instead of skipping verification.

## References

- Read [references/source-stack.md](./references/source-stack.md) when deciding how to combine OpenAlex, DOI, DeepXiv, and Zotero.

