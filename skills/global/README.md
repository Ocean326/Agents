# Global Skills

This directory holds Ocean's reusable custom skills mirrored from the local
Codex skills tree.

## Included

- custom skills only
- each skill keeps its own internal structure
- `PACKAGES.md` is preserved when available

## Excluded

- built-in `.system` skills
- `codex-primary-runtime`
- virtual environments
- caches and machine-local artifacts

## Convention

Each child directory should be a complete skill folder with `SKILL.md` at its
root and any supporting `references/`, `scripts/`, `assets/`, or `agents/`
folders alongside it.
