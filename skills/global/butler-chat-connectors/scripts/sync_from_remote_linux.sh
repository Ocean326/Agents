#!/usr/bin/env bash
set -euo pipefail

REMOTE_ALIAS="${1:-${BUTLER_REMOTE_ALIAS:-butler-remote}}"
LOCAL_REPO_ROOT="${2:-${BUTLER_REPO_ROOT:-/absolute/path/to/butler-repo}}"
STAMP="$(date +%Y%m%d-%H%M%S)"

LOCAL_CONFIG="${LOCAL_REPO_ROOT}/butler_main/butler_bot_code/configs/butler_bot.json"
LOCAL_WEIXIN_DIR="${LOCAL_REPO_ROOT}/工作区/weixin_state"
REMOTE_CONFIG="${BUTLER_REMOTE_CONFIG_PATH:-/absolute/path/to/remote/butler_bot.json}"
REMOTE_WEIXIN_JSON="${BUTLER_REMOTE_WEIXIN_JSON_PATH:-/absolute/path/to/remote/weixin.json}"
REMOTE_WEIXIN_QR="${BUTLER_REMOTE_WEIXIN_QR_PATH:-/absolute/path/to/remote/weixin_qr_login.md}"

TMP_CONFIG="$(mktemp /tmp/butler_bot.remote.XXXXXX.json)"
cleanup() {
  rm -f "${TMP_CONFIG}"
}
trap cleanup EXIT

mkdir -p "${LOCAL_WEIXIN_DIR}"

if [[ -f "${LOCAL_CONFIG}" ]]; then
  cp "${LOCAL_CONFIG}" "${LOCAL_CONFIG}.bak-${STAMP}"
fi
if [[ -f "${LOCAL_WEIXIN_DIR}/weixin.json" ]]; then
  cp "${LOCAL_WEIXIN_DIR}/weixin.json" "${LOCAL_WEIXIN_DIR}/weixin.json.bak-${STAMP}"
fi

scp "${REMOTE_ALIAS}:${REMOTE_CONFIG}" "${TMP_CONFIG}"
scp "${REMOTE_ALIAS}:${REMOTE_WEIXIN_JSON}" "${LOCAL_WEIXIN_DIR}/weixin.json"
scp "${REMOTE_ALIAS}:${REMOTE_WEIXIN_QR}" "${LOCAL_WEIXIN_DIR}/weixin_qr_login.md"

python3 - "${TMP_CONFIG}" "${LOCAL_CONFIG}" "${LOCAL_REPO_ROOT}" <<'PY'
import json
import sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
repo_root = sys.argv[3]
data = json.loads(src.read_text(encoding="utf-8"))
data["workspace_root"] = repo_root
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

echo "Synced Butler chat connector files from ${REMOTE_ALIAS} to ${LOCAL_REPO_ROOT}"
echo "Feishu config: ${LOCAL_CONFIG}"
echo "Weixin state dir: ${LOCAL_WEIXIN_DIR}"
