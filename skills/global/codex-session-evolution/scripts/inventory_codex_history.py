#!/usr/bin/env python3
"""Inventory local Codex history surfaces without assuming they map cleanly."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    home = Path.home()
    codex_home = home / ".codex"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-index", default=str(codex_home / "session_index.jsonl"))
    parser.add_argument("--history", default=str(codex_home / "history.jsonl"))
    parser.add_argument("--archived-dir", default=str(codex_home / "archived_sessions"))
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--history-rows", type=int, default=8)
    parser.add_argument("--rollouts", type=int, default=5)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_epoch_seconds(value: int | float) -> datetime:
    return datetime.fromtimestamp(float(value), tz=timezone.utc)


def compact(text: str, limit: int = 90) -> str:
    token = " ".join(str(text).split())
    if len(token) <= limit:
        return token
    return token[: limit - 3] + "..."


def summarize_threads(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    ranked = sorted(rows, key=lambda row: row.get("updated_at", ""), reverse=True)
    summary = []
    for row in ranked[:limit]:
        summary.append(
            {
                "id": row.get("id", ""),
                "updated_at": row.get("updated_at", ""),
                "thread_name": row.get("thread_name", ""),
            }
        )
    return summary


def summarize_history(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        session_id = row.get("session_id", "")
        ts = row.get("ts", 0)
        text = row.get("text", "")
        bucket = grouped.setdefault(
            session_id,
            {"session_id": session_id, "count": 0, "latest_ts": 0, "latest_text": ""},
        )
        bucket["count"] += 1
        if ts >= bucket["latest_ts"]:
            bucket["latest_ts"] = ts
            bucket["latest_text"] = compact(text)
    ranked = sorted(grouped.values(), key=lambda row: row["latest_ts"], reverse=True)
    summary = []
    for row in ranked[:limit]:
        latest_iso = ""
        if row["latest_ts"]:
            latest_iso = parse_epoch_seconds(row["latest_ts"]).isoformat()
        summary.append(
            {
                "session_id": row["session_id"],
                "count": row["count"],
                "latest_at": latest_iso,
                "latest_text": row["latest_text"],
            }
        )
    return summary


def summarize_rollout(path: Path) -> dict[str, Any]:
    event_counts: Counter[str] = Counter()
    session_meta: dict[str, Any] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            payload = json.loads(line)
            item_type = payload.get("type", "")
            event_counts[item_type] += 1
            if item_type == "session_meta" and not session_meta:
                session_meta = payload.get("payload", {})
    return {
        "file": str(path),
        "session_id": session_meta.get("id", ""),
        "started_at": session_meta.get("timestamp", ""),
        "cwd": session_meta.get("cwd", ""),
        "event_counts": dict(sorted(event_counts.items())),
    }


def summarize_rollouts(archived_dir: Path, limit: int) -> list[dict[str, Any]]:
    if not archived_dir.exists():
        return []
    files = sorted(archived_dir.glob("rollout-*.jsonl"), reverse=True)
    return [summarize_rollout(path) for path in files[:limit]]


def render_text(report: dict[str, Any]) -> str:
    lines = []
    surfaces = report["surfaces"]
    lines.append("Codex History Inventory")
    lines.append("")
    lines.append(f"session_index rows: {surfaces['session_index_rows']}")
    lines.append(f"history rows: {surfaces['history_rows']}")
    lines.append(f"archived rollout files: {surfaces['archived_rollout_files']}")
    lines.append("")
    lines.append("Recent threads:")
    for row in report["recent_threads"]:
        lines.append(f"- {row['updated_at']} | {row['id']} | {row['thread_name']}")
    lines.append("")
    lines.append("Recent history sessions:")
    for row in report["recent_history_sessions"]:
        lines.append(
            f"- {row['latest_at']} | {row['session_id']} | count={row['count']} | {row['latest_text']}"
        )
    lines.append("")
    lines.append("Recent rollout files:")
    for row in report["recent_rollouts"]:
        counts = ", ".join(f"{key}={value}" for key, value in row["event_counts"].items())
        lines.append(f"- {row['started_at']} | {row['session_id']} | {row['cwd']}")
        lines.append(f"  file: {row['file']}")
        lines.append(f"  counts: {counts}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    session_index_path = Path(args.session_index).expanduser()
    history_path = Path(args.history).expanduser()
    archived_dir = Path(args.archived_dir).expanduser()

    session_rows = load_jsonl(session_index_path)
    history_rows = load_jsonl(history_path)
    rollout_files = sorted(archived_dir.glob("rollout-*.jsonl"), reverse=True) if archived_dir.exists() else []

    report = {
        "schema_version": "codex_history_inventory_v0_1",
        "surfaces": {
            "session_index": str(session_index_path),
            "history": str(history_path),
            "archived_dir": str(archived_dir),
            "session_index_rows": len(session_rows),
            "history_rows": len(history_rows),
            "archived_rollout_files": len(rollout_files),
        },
        "recent_threads": summarize_threads(session_rows, args.threads),
        "recent_history_sessions": summarize_history(history_rows, args.history_rows),
        "recent_rollouts": summarize_rollouts(archived_dir, args.rollouts),
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
