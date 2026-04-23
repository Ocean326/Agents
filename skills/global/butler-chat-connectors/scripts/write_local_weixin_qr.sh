#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${1:-${BUTLER_REPO_ROOT:-/absolute/path/to/butler-repo}}"
OUTPUT_PATH="${2:-${REPO_ROOT}/工作区/weixin_state/weixin_qr_login.local.md}"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

resolve_public_base_url() {
  python3 - <<'PY'
import subprocess

candidates = []
for iface in ("en13", "en0", "en1"):
    try:
        ip = subprocess.check_output(["ipconfig", "getifaddr", iface], text=True).strip()
    except Exception:
        ip = ""
    if ip:
        candidates.append(ip)
try:
    output = subprocess.check_output(["ifconfig"], text=True)
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("inet "):
            ip = line.split()[1]
            if ip.startswith("127."):
                continue
            if ip not in candidates:
                candidates.append(ip)
except Exception:
    pass
preferred = ""
for ip in candidates:
    if ip.startswith(("10.", "192.168.", "172.")):
        preferred = ip
        break
if not preferred and candidates:
    preferred = candidates[0]
if not preferred:
    preferred = "127.0.0.1"
print(f"http://{preferred}:8789/")
PY
}

BRIDGE_BASE_URL="${3:-${BRIDGE_PUBLIC_BASE_URL:-$(resolve_public_base_url)}}"

mkdir -p "$(dirname "${OUTPUT_PATH}")"

cd "${REPO_ROOT}"
exec "${PYTHON_BIN}" -m butler_main.chat.weixi \
  --official-write-bridge-qr-link "${OUTPUT_PATH}" \
  --official-bridge-base-url "${BRIDGE_BASE_URL}"
