#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from dataclasses import asdict, dataclass
from typing import Dict, List, Sequence, Tuple


@dataclass(frozen=True)
class RouteCandidate:
    alias: str
    remote_shell_command: str
    probe_command: str
    route_family: str
    note: str


ROUTE_MAP: Dict[Tuple[str, str], List[RouteCandidate]] = {
    ("workstation", "linux"): [
        RouteCandidate(
            alias="workstation-linux-primary",
            remote_shell_command="bash -s",
            probe_command="hostname && whoami",
            route_family="direct-linux",
            note="Use the primary Linux SSH endpoint first for workstation compute.",
        ),
        RouteCandidate(
            alias="workstation-linux-via-host",
            remote_shell_command="wsl -e bash -s",
            probe_command='wsl -e bash -lc "hostname && whoami"',
            route_family="host-bridge",
            note="Fall back to the host shell and bridge into Linux.",
        ),
        RouteCandidate(
            alias="workstation-linux-campus",
            remote_shell_command="wsl -e bash -s",
            probe_command='wsl -e bash -lc "hostname && whoami"',
            route_family="campus-wsl-bridge",
            note="Use the campus alias only when the host route is unavailable and trust is already established.",
        ),
    ],
    ("workstation", "windows"): [
        RouteCandidate(
            alias="workstation-windows-primary",
            remote_shell_command="powershell -NoProfile -NonInteractive -Command -",
            probe_command="hostname",
            route_family="direct-windows",
            note="Use the primary Windows shell for Windows-native tasks.",
        ),
        RouteCandidate(
            alias="workstation-windows-campus",
            remote_shell_command="powershell -NoProfile -NonInteractive -Command -",
            probe_command="hostname",
            route_family="campus-windows",
            note="Use the campus Windows shell only when the overlay alias is unavailable.",
        ),
    ],
    ("shared-server", "linux"): [
        RouteCandidate(
            alias="shared-server-primary",
            remote_shell_command="bash -s",
            probe_command="hostname && whoami",
            route_family="direct",
            note="Prefer direct access to the shared server when it is reachable from the current machine.",
        ),
        RouteCandidate(
            alias="shared-server-via-linux",
            remote_shell_command="bash -s",
            probe_command="hostname && whoami",
            route_family="proxy-via-linux",
            note="Fall back through a Linux jump host when direct access is unavailable.",
        ),
        RouteCandidate(
            alias="shared-server-via-workstation",
            remote_shell_command="bash -s",
            probe_command="hostname && whoami",
            route_family="proxy-via-workstation",
            note="Use the workstation as the last fallback path to the shared server.",
        ),
    ],
}


def run_probe(alias: str, probe_command: str, timeout_seconds: int) -> Dict[str, object]:
    ssh_cmd: Sequence[str] = [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        f"ConnectTimeout={timeout_seconds}",
        alias,
        probe_command,
    ]
    try:
        completed = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds + 2,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or "").strip()
        stderr = (exc.stderr or "").strip()
        return {
            "alias": alias,
            "ok": False,
            "returncode": 124,
            "stdout": stdout,
            "stderr": stderr or f"Probe timed out after {timeout_seconds + 2}s",
            "ssh_command": list(ssh_cmd),
        }

    return {
        "alias": alias,
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "ssh_command": list(ssh_cmd),
    }


def shell_exports(payload: Dict[str, object]) -> str:
    selected = payload.get("selected_route") or {}
    exports = {
        "SELECTED_SSH_TARGET": selected.get("alias", ""),
        "SELECTED_REMOTE_SHELL_COMMAND": selected.get("remote_shell_command", ""),
        "SELECTED_ROUTE_FAMILY": selected.get("route_family", ""),
        "SELECTED_ROUTE_NOTE": selected.get("note", ""),
        "ROUTE_TARGET_MACHINE": payload.get("target_machine", ""),
        "ROUTE_RUNTIME": payload.get("runtime", ""),
    }
    return "\n".join(
        f"export {key}={shlex.quote(str(value))}" for key, value in exports.items()
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe SSH aliases for a target machine and return the first reachable route."
    )
    parser.add_argument(
        "--target-machine", required=True, choices=["workstation", "shared-server"]
    )
    parser.add_argument("--runtime", required=True, choices=["linux", "windows"])
    parser.add_argument("--timeout-seconds", type=int, default=6)
    parser.add_argument("--format", choices=["json", "env"], default="json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    key = (args.target_machine, args.runtime)
    if key not in ROUTE_MAP:
        print(
            json.dumps(
                {
                    "target_machine": args.target_machine,
                    "runtime": args.runtime,
                    "selected_route": None,
                    "error": "unsupported_target_runtime_combo",
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 2

    probes: List[Dict[str, object]] = []
    selected: RouteCandidate | None = None
    for candidate in ROUTE_MAP[key]:
        probe = run_probe(candidate.alias, candidate.probe_command, args.timeout_seconds)
        probe["remote_shell_command"] = candidate.remote_shell_command
        probe["route_family"] = candidate.route_family
        probe["note"] = candidate.note
        probes.append(probe)
        if probe["ok"]:
            selected = candidate
            break

    payload: Dict[str, object] = {
        "target_machine": args.target_machine,
        "runtime": args.runtime,
        "probe_timeout_seconds": args.timeout_seconds,
        "selected_route": asdict(selected) if selected else None,
        "probes": probes,
    }

    if args.format == "env":
        print(shell_exports(payload))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 0 if selected else 1


if __name__ == "__main__":
    raise SystemExit(main())
