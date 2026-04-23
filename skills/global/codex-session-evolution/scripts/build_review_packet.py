#!/usr/bin/env python3
"""Build a sanitized review packet from one archived rollout file."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

VERIFICATION_RE = re.compile(
    r"\b(test|tests|tested|verify|verified|verification|lint|typecheck|passed|repro|reproduction)\b|验证|测试|已跑|通过",
    re.IGNORECASE,
)
CLOSEOUT_RE = re.compile(
    r"\b(what changed|how it was verified|remaining risk|next step|best next action|verified)\b|下一步|风险|验证",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rollout-file", required=True, help="Path to one rollout-*.jsonl file")
    parser.add_argument("--output", help="Write the packet to this JSON file")
    parser.add_argument(
        "--include-task-snippets",
        action="store_true",
        help="Include a few short user or assistant text snippets in the packet",
    )
    parser.add_argument("--max-snippets", type=int, default=3)
    return parser.parse_args()


def compact(text: str, limit: int = 120) -> str:
    token = " ".join(str(text).split())
    if len(token) <= limit:
        return token
    return token[: limit - 3] + "..."


def extract_text_chunks(payload: dict[str, Any]) -> list[str]:
    chunks: list[str] = []
    for item in payload.get("content", []) or []:
        text = item.get("text")
        if text:
            chunks.append(str(text))
    return chunks


def make_packet(rollout_file: Path, include_task_snippets: bool, max_snippets: int) -> dict[str, Any]:
    top_level_counts: Counter[str] = Counter()
    response_item_counts: Counter[str] = Counter()
    function_calls: Counter[str] = Counter()
    custom_tools: Counter[str] = Counter()
    message_roles: Counter[str] = Counter()
    event_message_types: Counter[str] = Counter()
    web_queries: list[str] = []
    user_snippets: list[str] = []
    assistant_snippets: list[str] = []
    session_meta: dict[str, Any] = {}
    verification_hits = 0
    closeout_hits = 0

    with rollout_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            row_type = row.get("type", "")
            top_level_counts[row_type] += 1

            if row_type == "session_meta" and not session_meta:
                session_meta = row.get("payload", {})
                continue

            if row_type == "event_msg":
                event_message_types[row.get("payload", {}).get("type", "")] += 1
                continue

            if row_type != "response_item":
                continue

            payload = row.get("payload", {})
            item_type = payload.get("type", "")
            response_item_counts[item_type] += 1

            if item_type == "function_call":
                function_calls[payload.get("name", "")] += 1
            elif item_type == "custom_tool_call":
                custom_tools[payload.get("name", "")] += 1
            elif item_type == "web_search_call":
                action = payload.get("action", {}) or {}
                query = action.get("query", "")
                if query:
                    web_queries.append(compact(query, limit=100))
            elif item_type == "message":
                role = payload.get("role", "")
                message_roles[role] += 1
                texts = extract_text_chunks(payload)
                joined = "\n".join(texts)
                if role == "assistant":
                    if VERIFICATION_RE.search(joined):
                        verification_hits += 1
                    if CLOSEOUT_RE.search(joined):
                        closeout_hits += 1
                    if include_task_snippets and texts and len(assistant_snippets) < max_snippets:
                        assistant_snippets.append(compact(texts[0]))
                elif role == "user" and include_task_snippets and texts and len(user_snippets) < max_snippets:
                    user_snippets.append(compact(texts[0]))

    function_call_count = response_item_counts.get("function_call", 0)
    function_output_count = response_item_counts.get("function_call_output", 0)
    custom_tool_count = response_item_counts.get("custom_tool_call", 0)
    web_search_count = response_item_counts.get("web_search_call", 0)

    suggested_labels: list[str] = []
    candidate_hints: list[str] = []

    if web_search_count >= 5 or function_call_count >= 25:
        suggested_labels.append("exploration-heavy")
        candidate_hints.append("Tighten the exploration-to-plan handoff before wider tool fan-out.")
    if function_call_count >= 40 or custom_tool_count >= 5:
        suggested_labels.append("tool-overkill")
        candidate_hints.append("Constrain tool fan-out or lock a primary lane earlier.")
    if function_call_count > 0 and verification_hits == 0:
        suggested_labels.append("verification-thin")
        candidate_hints.append("Add a stronger verification gate or explicit evidence step.")
    if message_roles.get("assistant", 0) > 0 and closeout_hits == 0:
        suggested_labels.append("closeout-weak")
        candidate_hints.append("Strengthen closeout structure with outcome, evidence, and next action.")

    suggested_routes: list[str] = []
    if any(label in {"exploration-heavy", "tool-overkill", "verification-thin", "closeout-weak"} for label in suggested_labels):
        suggested_routes.append("workflow")

    confidence = "low"
    if len(suggested_labels) >= 2:
        confidence = "medium"

    packet = {
        "schema_version": "codex_session_review_packet_v0_1",
        "packet_id": f"review_packet_{session_meta.get('id', rollout_file.stem).replace('-', '_')}",
        "source": {
            "rollout_file": str(rollout_file),
            "session_id": session_meta.get("id", ""),
            "started_at": session_meta.get("timestamp", ""),
            "cwd": session_meta.get("cwd", ""),
            "originator": session_meta.get("originator", ""),
            "model_provider": session_meta.get("model_provider", ""),
        },
        "observations": {
            "top_level_event_counts": dict(sorted(top_level_counts.items())),
            "response_item_counts": dict(sorted(response_item_counts.items())),
            "event_message_types": dict(sorted(event_message_types.items())),
            "message_role_counts": dict(sorted(message_roles.items())),
            "tool_calls_by_name": dict(sorted(function_calls.items())),
            "custom_tools_by_name": dict(sorted(custom_tools.items())),
            "web_queries": web_queries[:10],
            "function_call_output_gap": function_call_count - function_output_count,
            "verification_signal_hits": verification_hits,
            "closeout_signal_hits": closeout_hits,
        },
        "inferences": {
            "suggested_labels": suggested_labels,
            "suggested_routes": suggested_routes,
            "candidate_hints": candidate_hints,
            "confidence": confidence,
            "notes": [
                "These inferences are heuristic and should be reviewed before promotion.",
                "Raw rollout logs remain the source of truth for anything disputed.",
            ],
        },
        "manual_fill": {
            "task_summary": "",
            "successes": [],
            "failures": [],
            "pattern_labels": [],
            "candidate_cues": [],
            "route_override": "",
            "next_action": "",
            "notes": "",
        },
    }

    if include_task_snippets:
        packet["safe_snippets"] = {
            "user": user_snippets,
            "assistant": assistant_snippets,
        }

    return packet


def main() -> int:
    args = parse_args()
    rollout_file = Path(args.rollout_file).expanduser()
    packet = make_packet(rollout_file, args.include_task_snippets, args.max_snippets)

    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(packet, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
