# Source Stack

## What this skill is for

This skill owns the literature-intake lane:

- finding papers
- recovering stable identifiers
- downloading accessible PDFs
- building a local seed library
- leaving a clean unresolved list for the hard cases

It does not replace paper reading, novelty critique, experiment design, or writing.

## Delivery posture

This lane should feel like `delivery-conductor` applied to literature intake:

- sweep context first
- choose one primary mode
- create durable artifacts instead of chat-only advice
- verify the actual outputs
- close with exact blockers and the next handoff

## Core architecture

### 1. Metadata backbone

Use standardized exports or stable identifiers as the truth source.

Preferred order:

- BibTeX
- EndNote `.enw`
- RIS
- DOI or arXiv identifier lists

Reason:

- metadata can survive even when downloads fail
- deduplication and later Zotero import depend on stable identifiers
- the download layer should not be the only source of truth

### 2. Acquisition layer

Use the smallest reliable combination of:

- `OpenAlex`
  - OA classification, best available landing page, and candidate PDF URL
- `DOI`
  - publisher or repository landing page when direct OA PDF is missing
- `manual title recovery`
  - only for the leftover items that still lack stable identifiers

Interpretation rule:

- `found`
  - a stable paper record exists
- `reachable`
  - there is a useful landing page or candidate OA URL
- `downloaded`
  - a local PDF exists and was verified as a PDF

Do not collapse these statuses.

### 3. Content enrichment layer

Use `DeepXiv` for the arXiv-friendly subset when the user wants:

- TLDRs
- section previews
- keywords
- GitHub links
- arXiv search

DeepXiv is not the long-term library home.

### 4. Durable library layer

Use `Zotero` when the user wants:

- collections
- tags
- notes
- deduplication
- long-term attachment management
- a real literature library instead of a one-off batch folder

## Recommended artifact set

For a batch run, prefer this output shape:

- `references.csv`
  - machine-readable master table
- `references.md`
  - human-readable inspection table
- `summary.json`
  - compact run summary
- `zotero_identifiers.txt`
  - identifiers for later Zotero intake
- `oa_pdf_urls.txt`
  - direct OA candidates
- `remaining_oa_to_resolve.csv`
  - unresolved OA or publisher-followup queue
- `remaining_oa_to_resolve.md`
  - human-readable unresolved queue
- `pdfs/`
  - only the files actually downloaded

## Subagent recommendation

This lane becomes expensive in context quickly because it mixes:

- source-format normalization
- identifier recovery
- web acquisition
- download verification
- unresolved-case bookkeeping

Recommend a fresh subagent or fresh thread when:

- the batch is larger than roughly 30 papers
- the user gave more than one export format
- there are many partial titles instead of stable identifiers
- there are multiple acquisition sources to compare
- the main thread also needs to preserve research planning or writing context

If subagents are explicitly allowed:

- let one worker own the batch acquisition pass
- keep the main thread for synthesis, verification, and final handoff
- keep the worker on a bounded write scope such as one output directory

## Common failure modes

- OA links return HTML or `403` instead of a PDF
- DOI resolves, but publisher access still blocks the full text
- title-only records map to the wrong paper if similarity checks are too weak
- downloaded files are landing pages renamed as `.pdf`

The correct response is to record these as unresolved or partially resolved, not to overclaim completion.

