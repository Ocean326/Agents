#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${1:-${BUTLER_REPO_ROOT:-/absolute/path/to/butler-repo}}"
CONFIG_PATH="${2:-${REPO_ROOT}/butler_main/butler_bot_code/configs/butler_bot.json}"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

cd "${REPO_ROOT}"
exec "${PYTHON_BIN}" -m butler_main.chat --config "${CONFIG_PATH}" --preflight
