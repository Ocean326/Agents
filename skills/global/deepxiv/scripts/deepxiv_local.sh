#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILL_ROOT="${DEEPXIV_SKILL_ROOT:-$CODEX_HOME/skills/deepxiv}"
VENV_BIN="$SKILL_ROOT/.venv/bin"

if [[ ! -x "$VENV_BIN/deepxiv" ]]; then
  echo "DeepXiv isolated runtime is missing." >&2
  echo "Initialize it with:" >&2
  echo "  python3 -m venv \"$SKILL_ROOT/.venv\"" >&2
  echo "  \"$VENV_BIN/python\" -m pip install -U pip setuptools wheel" >&2
  echo "  \"$VENV_BIN/python\" -m pip install -U \"deepxiv-sdk[all]\"" >&2
  exit 1
fi

exec "$VENV_BIN/deepxiv" "$@"
