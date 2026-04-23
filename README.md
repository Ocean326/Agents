# Agents

Public home for Ocean's agent-facing assets:

- reusable custom skills
- project-local skills worth preserving outside a single repo
- public-safe config examples
- usage notes for Codex / agent workflows

This repository intentionally does **not** mirror machine-private state.
It is meant to be a clean, shareable source tree for agent building blocks.

## What Is Included

- `skills/global/`
  - Ocean's global custom skills from `~/.codex/skills`
  - only custom skills are mirrored here
  - built-in `.system` and `codex-primary-runtime` skills are intentionally excluded
- `skills/project/transfer_recovery/`
  - project-local skills promoted from `Transfer_Recovery/.agents/skills`
- `configs/examples/`
  - sanitized examples for future Codex or agent configuration
- `docs/usage/`
  - practical notes on browsing, copying, and using the skills
- `docs/reference/`
  - repository structure and maintenance conventions

## Initial Layout

```text
Agents/
├── configs/
│   └── examples/
│       └── codex/
├── docs/
│   ├── reference/
│   └── usage/
└── skills/
    ├── global/
    └── project/
        └── transfer_recovery/
```

## Current Content

- `64` global custom skills
- `2` project-local `Transfer_Recovery` skills

## Design Rules

- keep directory names stable so links and prompts stay valid
- preserve each skill as a self-contained folder
- keep project-local skills namespaced under their source project
- exclude secrets, auth files, caches, virtualenvs, and machine-local state
- prefer readable docs over clever automation in the bootstrap phase

## Start Here

- [Repository Map](./docs/reference/repository-map.md)
- [Getting Started](./docs/usage/getting-started.md)
- [Skills Index](./skills/INDEX.md)
