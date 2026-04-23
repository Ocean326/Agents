# Repository Guidelines

## Purpose

This repository is a public-safe home for agent assets:

- reusable skills
- project-local skill snapshots
- config examples
- usage notes and operating conventions

Keep it clean, portable, and easy to browse.

## Structure

- `skills/global/`
  - global custom skills from `~/.codex/skills`
  - do not mirror built-in `.system` or `codex-primary-runtime` here
- `skills/project/<project_name>/`
  - project-local skills that originally lived in a specific repo
- `configs/examples/`
  - sanitized examples only
- `docs/usage/`
  - end-user instructions
- `docs/reference/`
  - repository conventions and indexes

## Content Rules

- never commit secrets, tokens, auth files, local state DBs, or personal session logs
- exclude `.venv/`, `__pycache__/`, `.DS_Store`, and other machine-local artifacts
- keep skill directory names stable once published
- preserve internal skill structure when copying: `SKILL.md`, `references/`, `scripts/`, `assets/`, `agents/`
- if a skill came from a project repo, keep it under `skills/project/<project>/...`

## Editing

- use ASCII by default
- prefer small, reviewable changes
- update docs when the repository layout changes
- if you add or remove a skill directory, update `skills/INDEX.md`

## Review Checklist

- does the tree still make sense to a new reader
- are private or machine-bound files excluded
- are links still valid
- does the change preserve the original skill name and structure
