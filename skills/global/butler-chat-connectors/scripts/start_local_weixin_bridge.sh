#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${1:-${BUTLER_REPO_ROOT:-/absolute/path/to/butler-repo}}"
HOST="${2:-0.0.0.0}"
PORT="${3:-8789}"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

resolve_public_base_url() {
  python3 - "$PORT" <<'PY'
import socket
import subprocess
import sys

port = sys.argv[1]
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
print(f"http://{preferred}:{port}")
PY
}

PUBLIC_BASE_URL="${BRIDGE_PUBLIC_BASE_URL:-$(resolve_public_base_url)}"

cd "${REPO_ROOT}"
exec "${PYTHON_BIN}" -m butler_main.chat.weixi \
  --serve-bridge \
  --bridge-host "${HOST}" \
  --bridge-port "${PORT}" \
  --bridge-public-base-url "${PUBLIC_BASE_URL}"
