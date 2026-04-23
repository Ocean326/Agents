#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import re
import sqlite3
from collections import deque
from pathlib import Path
from typing import Any

ARTIFACT_PATH_PATTERN = re.compile(r"/Users/[^\s)>'\"\\]+")
OPEN_LOOP_PATTERN = re.compile(
    r"(next step|pending|todo|not yet|remain|follow[- ]up|phase 2|下一步|还没做|后续|下一阶段|要不要我直接|如果你更想)",
    re.IGNORECASE,
)


def read_jsonl(path: Path):
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def extract_text_from_content(content: list[dict[str, Any]]) -> str:
    texts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        for key in ("output_text", "input_text", "text"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                texts.append(value.strip())
    return "\n".join(texts).strip()


def squash_text(text: str, limit: int = 600) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def decode_sqlite_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value)


def normalize_path_candidate(candidate: str) -> str:
    candidate = candidate.strip().rstrip(".,:;")
    if not candidate.startswith("/Users/"):
        return ""
    if Path(candidate).exists():
        return candidate
    trimmed = candidate
    while len(trimmed) > len("/Users/") and not Path(trimmed).exists():
        trimmed = trimmed[:-1]
    if Path(trimmed).exists():
        return trimmed
    return ""


def extract_paths_from_text(text: str) -> set[str]:
    results: set[str] = set()
    for match in ARTIFACT_PATH_PATTERN.findall(text or ""):
        normalized = normalize_path_candidate(match)
        if normalized:
            results.add(normalized)
    return results


def extract_paths_from_cursor_state_blob(encoded_state: str) -> set[str]:
    if not isinstance(encoded_state, str) or not encoded_state:
        return set()
    payload = encoded_state[1:] if encoded_state.startswith("~") else encoded_state
    try:
        decoded = base64.b64decode(payload + "=" * (-len(payload) % 4))
    except Exception:
        return set()
    results: set[str] = set()
    start = 0
    needle = b"/Users/"
    stop_bytes = set(b"\"'<> )]\\}\r\n\t")
    while True:
        idx = decoded.find(needle, start)
        if idx == -1:
            break
        end = idx
        while end < len(decoded):
            current = decoded[end]
            if current < 32 or current in stop_bytes:
                break
            end += 1
        candidate = decoded[idx:end].decode("utf-8", errors="ignore").strip()
        normalized = normalize_path_candidate(candidate)
        if normalized:
            results.add(normalized)
        start = idx + len(needle)
    return results


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def collect_session_index_entries(codex_home: Path, session_id: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    index_path = codex_home / "session_index.jsonl"
    if not index_path.exists():
        return entries
    for row in read_jsonl(index_path):
        if row.get("id") == session_id:
            entries.append(row)
    return entries


def find_rollout_files(codex_home: Path, session_id: str) -> list[Path]:
    candidates = set()
    patterns = [
        f"sessions/**/rollout-*{session_id}.jsonl",
        f"archived_sessions/rollout-*{session_id}.jsonl",
        f"sessions/**/{session_id}*.jsonl",
        f"archived_sessions/**/*{session_id}*.jsonl",
    ]
    for pattern in patterns:
        for p in codex_home.glob(pattern):
            if p.is_file():
                candidates.add(p)
    return sorted(candidates)


def parse_rollout(path: Path, max_messages: int) -> dict[str, Any]:
    user_messages: deque[str] = deque(maxlen=max_messages)
    assistant_messages: deque[str] = deque(maxlen=max_messages)
    cwd_candidates: set[str] = set()
    tools: set[str] = set()
    phases: set[str] = set()
    artifact_paths: set[str] = set()

    for row in read_jsonl(path):
        row_type = row.get("type")
        payload = row.get("payload", {})

        if row_type == "turn_context":
            cwd = payload.get("cwd")
            if isinstance(cwd, str) and cwd:
                cwd_candidates.add(cwd)

        elif row_type == "event_msg":
            event_type = payload.get("type")
            if event_type == "user_message":
                message = payload.get("message", "")
                if isinstance(message, str) and message.strip():
                    user_messages.append(squash_text(message))
                    artifact_paths.update(extract_paths_from_text(message))
            elif event_type == "agent_message":
                message = payload.get("message", "")
                phase = payload.get("phase")
                if isinstance(phase, str) and phase:
                    phases.add(phase)
                if isinstance(message, str) and message.strip():
                    assistant_messages.append(squash_text(message))
                    artifact_paths.update(extract_paths_from_text(message))

        elif row_type == "response_item":
            item_type = payload.get("type")
            if item_type == "message":
                role = payload.get("role")
                content = payload.get("content", [])
                if isinstance(content, list):
                    text = extract_text_from_content(content)
                    if text:
                        if role == "user":
                            user_messages.append(squash_text(text))
                        elif role == "assistant":
                            assistant_messages.append(squash_text(text))
                        artifact_paths.update(extract_paths_from_text(text))
            elif item_type == "function_call":
                name = payload.get("name")
                if isinstance(name, str) and name:
                    tools.add(name)

    open_loops: list[str] = []
    for message in reversed(list(assistant_messages)):
        if OPEN_LOOP_PATTERN.search(message):
            open_loops.append(message)
    open_loops = open_loops[:3]

    return {
        "rollout_file": str(path),
        "cwd_candidates": sorted(cwd_candidates),
        "recent_user_messages": list(user_messages),
        "recent_assistant_messages": list(assistant_messages),
        "tools": sorted(tools),
        "phases": sorted(phases),
        "artifact_paths": sorted(artifact_paths),
        "open_loops": open_loops,
    }


def build_codex_report(codex_home: Path, session_id: str, max_messages: int) -> dict[str, Any]:
    index_entries = collect_session_index_entries(codex_home, session_id)
    rollouts = find_rollout_files(codex_home, session_id)
    parsed_rollouts = [parse_rollout(path, max_messages=max_messages) for path in rollouts]

    merged_cwds: set[str] = set()
    merged_artifacts: set[str] = set()
    merged_tools: set[str] = set()
    merged_open_loops: list[str] = []

    for parsed in parsed_rollouts:
        merged_cwds.update(parsed["cwd_candidates"])
        merged_artifacts.update(parsed["artifact_paths"])
        merged_tools.update(parsed["tools"])
        for item in parsed["open_loops"]:
            if item not in merged_open_loops:
                merged_open_loops.append(item)

    return {
        "provider": "codex",
        "session_id": session_id,
        "session_index_entries": index_entries,
        "rollout_count": len(rollouts),
        "rollouts": parsed_rollouts,
        "workspace_paths": sorted(merged_cwds),
        "artifact_paths": sorted(merged_artifacts),
        "tools_seen": sorted(merged_tools),
        "open_loops": merged_open_loops[:5],
    }


def load_cursor_composer_headers(cursor_db: Path) -> dict[str, dict[str, Any]]:
    if not cursor_db.exists():
        return {}
    conn = sqlite3.connect(cursor_db)
    try:
        row = conn.execute(
            "select value from ItemTable where key = 'composer.composerHeaders'"
        ).fetchone()
    finally:
        conn.close()
    if not row:
        return {}
    payload = decode_sqlite_text(row[0])
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return {}
    headers: dict[str, dict[str, Any]] = {}
    for entry in data.get("allComposers", []):
        composer_id = entry.get("composerId")
        if isinstance(composer_id, str) and composer_id:
            headers[composer_id] = entry
    return headers


def find_cursor_matches(cursor_db: Path, session_id: str) -> dict[str, dict[str, Any]]:
    matches: dict[str, dict[str, Any]] = {}
    if not cursor_db.exists():
        return matches

    conn = sqlite3.connect(cursor_db)
    try:
        composer_key = f"composerData:{session_id}"
        row = conn.execute("select key from cursorDiskKV where key = ?", (composer_key,)).fetchone()
        if row:
            matches[session_id] = {
                "composer_id": session_id,
                "matched_request_ids": set(),
                "matched_bubble_ids": set(),
                "matched_by": {"composer_id"},
            }

        pattern = f'%"requestId":"{session_id}"%'
        rows = conn.execute(
            "select key, value from cursorDiskKV where key like 'bubbleId:%' and cast(value as text) like ?",
            (pattern,),
        ).fetchall()
    finally:
        conn.close()

    for key, value in rows:
        key_text = decode_sqlite_text(key)
        parts = key_text.split(":", 2)
        if len(parts) != 3:
            continue
        _, composer_id, bubble_id = parts
        payload = decode_sqlite_text(value)
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            continue
        if data.get("requestId") != session_id:
            continue
        match = matches.setdefault(
            composer_id,
            {
                "composer_id": composer_id,
                "matched_request_ids": set(),
                "matched_bubble_ids": set(),
                "matched_by": set(),
            },
        )
        match["matched_request_ids"].add(session_id)
        match["matched_bubble_ids"].add(bubble_id)
        match["matched_by"].add("request_id")

    return matches


def parse_cursor_composer(
    cursor_db: Path,
    composer_id: str,
    composer_headers: dict[str, dict[str, Any]],
    matched_request_ids: set[str],
    max_messages: int,
) -> dict[str, Any]:
    conn = sqlite3.connect(cursor_db)
    try:
        row = conn.execute(
            "select value from cursorDiskKV where key = ?",
            (f"composerData:{composer_id}",),
        ).fetchone()
        if not row:
            return {}
        composer_data = json.loads(decode_sqlite_text(row[0]))
        header_items = composer_data.get("fullConversationHeadersOnly", [])

        user_messages: deque[str] = deque(maxlen=max_messages)
        assistant_messages: deque[str] = deque(maxlen=max_messages)
        artifact_paths: set[str] = set()
        request_ids: list[str] = []

        for header in header_items:
            bubble_id = header.get("bubbleId")
            if not isinstance(bubble_id, str) or not bubble_id:
                continue
            bubble_row = conn.execute(
                "select value from cursorDiskKV where key = ?",
                (f"bubbleId:{composer_id}:{bubble_id}",),
            ).fetchone()
            if not bubble_row:
                continue
            bubble = json.loads(decode_sqlite_text(bubble_row[0]))
            request_id = bubble.get("requestId")
            if isinstance(request_id, str) and request_id:
                request_ids.append(request_id)

            text_candidates = []
            for key in ("text", "markdown"):
                value = bubble.get(key)
                if isinstance(value, str) and value.strip():
                    text_candidates.append(value.strip())
            text = "\n".join(text_candidates).strip()

            for state_key in ("conversationState",):
                artifact_paths.update(extract_paths_from_cursor_state_blob(bubble.get(state_key, "")))
            artifact_paths.update(extract_paths_from_text(text))

            bubble_type = bubble.get("type")
            if text:
                if bubble_type == 1:
                    user_messages.append(squash_text(text))
                elif bubble_type == 2:
                    assistant_messages.append(squash_text(text))

        header = composer_headers.get(composer_id, {})
        workspace_paths: set[str] = set()
        workspace = header.get("workspaceIdentifier", {})
        if isinstance(workspace, dict):
            uri = workspace.get("uri", {})
            if isinstance(uri, dict):
                fs_path = uri.get("fsPath")
                if isinstance(fs_path, str) and fs_path:
                    workspace_paths.add(fs_path)

        composer_state = composer_data.get("conversationState", "")
        artifact_paths.update(extract_paths_from_cursor_state_blob(composer_state))

        open_loops: list[str] = []
        for message in reversed(list(assistant_messages)):
            if OPEN_LOOP_PATTERN.search(message):
                open_loops.append(message)

        cursor_rules = []
        context = composer_data.get("context", {})
        if isinstance(context, dict):
            rules = context.get("cursorRules", [])
            if isinstance(rules, list):
                for item in rules:
                    if isinstance(item, dict):
                        filename = item.get("filename")
                        if isinstance(filename, str) and filename:
                            cursor_rules.append(filename)

        title = composer_data.get("name") or header.get("name") or ""
        return {
            "composer_id": composer_id,
            "title": title,
            "status": composer_data.get("status", ""),
            "last_updated_at": composer_data.get("lastUpdatedAt"),
            "created_at": composer_data.get("createdAt"),
            "workspace_paths": sorted(workspace_paths),
            "artifact_paths": sorted(artifact_paths),
            "recent_user_messages": list(user_messages),
            "recent_assistant_messages": list(assistant_messages),
            "open_loops": dedupe_keep_order(open_loops)[:3],
            "matched_request_ids": sorted(set(request_ids).union(matched_request_ids)),
            "cursor_rules": dedupe_keep_order(cursor_rules),
            "model_name": (
                composer_data.get("modelConfig", {}).get("modelName", "")
                if isinstance(composer_data.get("modelConfig"), dict)
                else ""
            ),
            "subtitle": header.get("subtitle", ""),
        }
    finally:
        conn.close()


def build_cursor_report(cursor_db: Path, session_id: str, max_messages: int) -> dict[str, Any]:
    matches = find_cursor_matches(cursor_db, session_id)
    composer_headers = load_cursor_composer_headers(cursor_db)

    chats: list[dict[str, Any]] = []
    for match in matches.values():
        parsed = parse_cursor_composer(
            cursor_db=cursor_db,
            composer_id=match["composer_id"],
            composer_headers=composer_headers,
            matched_request_ids=match["matched_request_ids"],
            max_messages=max_messages,
        )
        if parsed:
            parsed["matched_by"] = sorted(match["matched_by"])
            chats.append(parsed)

    chats.sort(
        key=lambda item: (
            item.get("last_updated_at") is not None,
            item.get("last_updated_at") or 0,
        ),
        reverse=True,
    )

    merged_workspaces: set[str] = set()
    merged_artifacts: set[str] = set()
    merged_open_loops: list[str] = []
    merged_rules: list[str] = []
    matched_request_ids: list[str] = []
    for chat in chats:
        merged_workspaces.update(chat.get("workspace_paths", []))
        merged_artifacts.update(chat.get("artifact_paths", []))
        matched_request_ids.extend(chat.get("matched_request_ids", []))
        merged_rules.extend(chat.get("cursor_rules", []))
        for loop in chat.get("open_loops", []):
            if loop not in merged_open_loops:
                merged_open_loops.append(loop)

    ambiguity_notes: list[str] = []
    if len(chats) > 1:
        ambiguity_notes.append(
            f"session id matched {len(chats)} Cursor composers; report is ordered by most recent lastUpdatedAt"
        )

    primary = chats[0] if chats else {}
    return {
        "provider": "cursor",
        "session_id": session_id,
        "cursor_db": str(cursor_db),
        "chat_count": len(chats),
        "cursor_composer_id": primary.get("composer_id", ""),
        "cursor_composer_ids": [chat["composer_id"] for chat in chats],
        "chat_title": primary.get("title", ""),
        "workspace_paths": sorted(merged_workspaces),
        "artifact_paths": sorted(merged_artifacts),
        "open_loops": merged_open_loops[:5],
        "cursor_rules": dedupe_keep_order(merged_rules),
        "matched_request_ids": dedupe_keep_order(matched_request_ids),
        "risks_or_unknowns": ambiguity_notes,
        "chats": chats,
    }


def render_codex_report(report: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    lines.append(f"# Session {report['session_id']}")
    lines.append("")
    lines.append("- provider: codex")
    lines.append(f"- rollout_count: {report['rollout_count']}")

    thread_names = [
        entry.get("thread_name", "")
        for entry in report.get("session_index_entries", [])
        if entry.get("thread_name")
    ]
    if thread_names:
        lines.append(f"- thread_names: {', '.join(thread_names)}")
    if report.get("workspace_paths"):
        lines.append("- workspace_paths:")
        for p in report["workspace_paths"]:
            lines.append(f"  - {p}")
    if report.get("artifact_paths"):
        lines.append("- artifact_paths:")
        for p in report["artifact_paths"][:20]:
            lines.append(f"  - {p}")
    if report.get("tools_seen"):
        lines.append(f"- tools_seen: {', '.join(report['tools_seen'])}")

    lines.append("")
    lines.append("## Open Loops")
    if report.get("open_loops"):
        for item in report["open_loops"]:
            lines.append(f"- {item}")
    else:
        lines.append("- none detected")

    lines.append("")
    lines.append("## Recent Messages")
    for parsed in report.get("rollouts", []):
        lines.append(f"### {parsed['rollout_file']}")
        if parsed.get("recent_user_messages"):
            lines.append("- user:")
            for msg in parsed["recent_user_messages"][-3:]:
                lines.append(f"  - {msg}")
        if parsed.get("recent_assistant_messages"):
            lines.append("- assistant:")
            for msg in parsed["recent_assistant_messages"][-3:]:
                lines.append(f"  - {msg}")
        lines.append("")

    return lines


def render_cursor_report(report: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    lines.append(f"# Session {report['session_id']}")
    lines.append("")
    lines.append("- provider: cursor")
    lines.append(f"- chat_count: {report['chat_count']}")
    if report.get("cursor_composer_id"):
        lines.append(f"- cursor_composer_id: {report['cursor_composer_id']}")
    if report.get("chat_title"):
        lines.append(f"- chat_title: {report['chat_title']}")
    if report.get("matched_request_ids"):
        lines.append(f"- matched_request_ids: {', '.join(report['matched_request_ids'])}")
    if report.get("workspace_paths"):
        lines.append("- workspace_paths:")
        for p in report["workspace_paths"]:
            lines.append(f"  - {p}")
    if report.get("artifact_paths"):
        lines.append("- artifact_paths:")
        for p in report["artifact_paths"][:20]:
            lines.append(f"  - {p}")
    if report.get("cursor_rules"):
        lines.append(f"- cursor_rules: {', '.join(report['cursor_rules'])}")
    if report.get("risks_or_unknowns"):
        lines.append("- risks_or_unknowns:")
        for item in report["risks_or_unknowns"]:
            lines.append(f"  - {item}")

    lines.append("")
    lines.append("## Open Loops")
    if report.get("open_loops"):
        for item in report["open_loops"]:
            lines.append(f"- {item}")
    else:
        lines.append("- none detected")

    lines.append("")
    lines.append("## Recent Messages")
    for chat in report.get("chats", []):
        lines.append(f"### Composer {chat['composer_id']}")
        if chat.get("title"):
            lines.append(f"- title: {chat['title']}")
        if chat.get("model_name"):
            lines.append(f"- model: {chat['model_name']}")
        if chat.get("status"):
            lines.append(f"- status: {chat['status']}")
        if chat.get("subtitle"):
            lines.append(f"- subtitle: {chat['subtitle']}")
        if chat.get("recent_user_messages"):
            lines.append("- user:")
            for msg in chat["recent_user_messages"][-3:]:
                lines.append(f"  - {msg}")
        if chat.get("recent_assistant_messages"):
            lines.append("- assistant:")
            for msg in chat["recent_assistant_messages"][-3:]:
                lines.append(f"  - {msg}")
        lines.append("")

    return lines


def render_markdown(reports: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for report in reports:
        if report.get("provider") == "cursor":
            lines.extend(render_cursor_report(report))
        else:
            lines.extend(render_codex_report(report))
        if not lines[-1]:
            continue
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_session_report(
    session_id: str,
    provider: str,
    codex_home: Path,
    cursor_db: Path,
    max_messages: int,
) -> dict[str, Any]:
    if provider in {"codex", "auto"}:
        codex_report = build_codex_report(codex_home, session_id, max_messages)
        if provider == "codex" or codex_report["rollout_count"] or codex_report["session_index_entries"]:
            return codex_report

    if provider in {"cursor", "auto"}:
        cursor_report = build_cursor_report(cursor_db, session_id, max_messages)
        if provider == "cursor" or cursor_report["chat_count"]:
            return cursor_report

    return {
        "provider": provider,
        "session_id": session_id,
        "workspace_paths": [],
        "artifact_paths": [],
        "open_loops": [],
        "risks_or_unknowns": ["no matching session evidence found"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract continuation packets from Codex or Cursor session ids."
    )
    parser.add_argument("--session-id", action="append", required=True, help="Session id to extract (repeatable).")
    parser.add_argument(
        "--provider",
        choices=["auto", "codex", "cursor"],
        default="auto",
        help="Session provider to inspect (default: auto).",
    )
    parser.add_argument(
        "--codex-home",
        default=str(Path.home() / ".codex"),
        help="Codex home directory (default: ~/.codex).",
    )
    parser.add_argument(
        "--cursor-state-db",
        default=str(Path.home() / "Library/Application Support/Cursor/User/globalStorage/state.vscdb"),
        help="Cursor state database (default: ~/Library/Application Support/Cursor/User/globalStorage/state.vscdb).",
    )
    parser.add_argument("--max-messages", type=int, default=8, help="Max recent messages per role per session.")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="Optional output file path.")
    args = parser.parse_args()

    codex_home = Path(args.codex_home).expanduser().resolve()
    cursor_db = Path(args.cursor_state_db).expanduser().resolve()
    reports = [
        build_session_report(
            session_id=sid,
            provider=args.provider,
            codex_home=codex_home,
            cursor_db=cursor_db,
            max_messages=args.max_messages,
        )
        for sid in args.session_id
    ]

    if args.format == "json":
        rendered = json.dumps(reports, ensure_ascii=False, indent=2)
    else:
        rendered = render_markdown(reports)

    if args.output:
        out = Path(args.output).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
