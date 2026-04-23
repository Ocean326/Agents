# Getting Started

## What This Repo Is For

This repository is a clean source tree for agent assets that are worth keeping,
sharing, and reusing across machines or projects.

## What It Is Not

This repository is not a dump of:

- local Codex state
- secrets
- auth files
- logs
- caches
- built-in system skills

## Using A Skill From This Repo

1. Find the skill in `skills/global/` or `skills/project/`.
2. Read `SKILL.md` first.
3. Copy or sync the whole skill directory into the target environment.
4. Keep sibling folders like `references/`, `scripts/`, `assets/`, and `agents/` together.

## Suggested Copy Pattern

For a global skill:

```bash
cp -R skills/global/<skill-name> ~/.codex/skills/
```

For a project-local skill:

```bash
cp -R skills/project/transfer_recovery/<skill-name> ~/.codex/skills/
```

Adjust the destination if your runtime uses a different skills root.

## Maintenance Notes

- do not copy `.venv/` or cache directories across platforms
- prefer keeping skill names unchanged
- if you move a skill, update links and indexes in this repo
