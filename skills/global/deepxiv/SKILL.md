---
name: deepxiv
description: Use DeepXiv as an agent-first paper search and progressive reading lane for arXiv, PMC, bioRxiv, and medRxiv friendly literature. Best for fast paper discovery, `brief -> head -> section -> full` reading, and identifier recovery before a local library intake step.
---

# DeepXiv

Use this skill when the user needs a paper-native search and reading surface, not a broad web crawl.

DeepXiv is best treated as:

- a literature access substrate
- a progressive reading interface
- a shortlist and identifier recovery lane

Do not treat it as:

- a replacement for the user's long-term literature library
- the only acquisition path
- a project-specific knowledge base

## Best-Fit Use Cases

Use this skill for:

- arXiv / PMC friendly paper search
- quickly shortlisting papers before deep reading
- `brief -> head -> section -> full` progressive access
- recovering arXiv IDs, DOI-based bioRxiv / medRxiv access, or PMC handles
- preparing inputs for `literature-finder-downloader` or a project-local library skill

Prefer another lane when:

- the task is broad web discovery across blogs, repos, news, and forums
- the user already has BibTeX / RIS / DOI batches and wants end-to-end downloading
- the main job is bibliography management or long-term attachment organization

## Setup

Prefer the bundled isolated runtime first:

```bash
deepxiv-local --help
```

Fallback wrapper path:

```bash
$CODEX_HOME/skills/deepxiv/scripts/deepxiv_local.sh --help
```

If that wrapper is unavailable, check whether the CLI is already available:

```bash
command -v deepxiv
```

If not installed, install it with Python user packages:

```bash
python3 -m pip install --user -U "deepxiv-sdk[all]"
```

Minimum package if only the reader/CLI lane is needed:

```bash
python3 -m pip install --user -U deepxiv-sdk
```

Recommended local-isolated install for this skill:

```bash
python3 -m venv $CODEX_HOME/skills/deepxiv/.venv
$CODEX_HOME/skills/deepxiv/.venv/bin/python -m pip install -U pip setuptools wheel
$CODEX_HOME/skills/deepxiv/.venv/bin/python -m pip install -U "deepxiv-sdk[all]"
```

Important token behavior:

- on first CLI use, DeepXiv may auto-register an anonymous token and write it to `~/.env`
- if the user wants explicit control, prefer configuring the token manually instead of relying on auto-registration

Explicit token options:

```bash
deepxiv config --token YOUR_TOKEN
export DEEPXIV_TOKEN="YOUR_TOKEN"
deepxiv paper 2409.05591 --token YOUR_TOKEN --brief
```

## Default Workflow

### 1. Search

Start with a small search pass:

```bash
deepxiv-local search "trajectory recovery" --limit 5
deepxiv-local search "trajectory representation learning" --limit 10
deepxiv-local search "image generation" --date-from 2026-03-01 --limit 20
```

If machine-readable output is helpful:

```bash
deepxiv-local search "trajectory recovery" --limit 20 --format json
```

For web-profile search:

```bash
deepxiv-local wsearch "karpathy"
deepxiv-local wsearch "karpathy" --json
```

### 2. Progressive Reading

Once you have a candidate paper id, read in layers:

```bash
deepxiv-local paper 2505.13857 --brief
deepxiv-local paper 2505.13857 --head
deepxiv-local paper 2505.13857 --section Introduction
deepxiv-local paper 2505.13857 --section Experiments
deepxiv-local paper 2505.13857
```

Interpretation:

- `--brief`
  - low-cost paper triage
- `--head`
  - section map and token distribution
- `--section`
  - load only the useful part
- bare `paper`
  - full content access when the cheaper layers were not enough

Use `--brief` before `--head`, and `--head` before section or full reads unless the user explicitly asks for the full paper immediately.

### 3. Non-arXiv Open Literature

PMC:

```bash
deepxiv-local pmc PMC544940 --head
```

bioRxiv / medRxiv by DOI:

```bash
deepxiv-local biorxiv 10.1101/2021.02.26.433129 --section Introduction,Methods
deepxiv-local paper 10.1101/2021.02.26.433129 --biorxiv
deepxiv-local paper 10.1101/2021.02.26.433129 --biorxiv --section Introduction
```

Source-specific search:

```bash
deepxiv-local search "protein design" --biorxiv --limit 5
deepxiv-local search "Alzheimer" --medrxiv --date-from 2024-01
```

## Acquisition Boundaries

DeepXiv is excellent for shortlist construction and progressive reading, but it is not the user's durable library home.

When the user wants:

- many papers downloaded locally
- a seed folder with PDF attachments
- metadata tables and unresolved queues

route from DeepXiv into `literature-finder-downloader`.

When the user wants:

- a project-specific paper library
- both local PDF and Markdown under a stable repo path

route from DeepXiv into the relevant project-local literature skill.

## Practical Patterns

### Pattern A: shortlist first, acquire later

1. `deepxiv search ...`
2. `deepxiv paper <id> --brief`
3. `deepxiv paper <id> --head`
4. keep only the papers worth acquisition
5. pass the identifiers into `literature-finder-downloader`

### Pattern B: compare methods cheaply

1. search one focused topic
2. run `--brief` on 3 to 10 candidates
3. run `--head` only on the strongest subset
4. read `Introduction`, `Method`, and `Experiments` sections only

### Pattern C: prepare a project library update

1. use DeepXiv to recover strong candidates and identifiers
2. acquire durable local attachments through the project's literature lane
3. keep DeepXiv as the external access layer, not the final storage layer

## Output Contract

When using this skill, report:

- what was searched
- which identifiers or papers were shortlisted
- which progressive-reading layer was used
- what remains uncertain
- whether the next step should be:
  - more DeepXiv reading
  - durable acquisition via `literature-finder-downloader`
  - handoff into a project-local paper library

## Common Triggers

- “用 DeepXiv 先搜几篇相关论文”
- “先别整篇读，先给我 brief/head 看看值不值得深读”
- “帮我用 DeepXiv 找到这篇论文的 arXiv / PMC 入口”
- “把 DeepXiv 当成论文搜索和预读入口，再接到本地下载链”
