#!/usr/bin/env python3
"""Aggregate review packets and suggest the smallest repeated candidate directions."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

RULES = {
    "verification-thin": {
        "candidate_type": "workflow",
        "suggested_action": "Strengthen verification-before-completion or add an explicit evidence gate.",
    },
    "closeout-weak": {
        "candidate_type": "workflow",
        "suggested_action": "Strengthen closeout structure with outcome, evidence, risk, and next action.",
    },
    "exploration-heavy": {
        "candidate_type": "workflow",
        "suggested_action": "Tighten the exploration-to-plan handoff and lock a primary lane earlier.",
    },
    "tool-overkill": {
        "candidate_type": "workflow",
        "suggested_action": "Constrain tool fan-out and prefer the smallest capable helper earlier.",
    },
    "resume-fragile": {
        "candidate_type": "workflow",
        "suggested_action": "Add a stronger resume or open-loop inventory step before new execution.",
    },
    "prompt-ambiguity": {
        "candidate_type": "prompt",
        "suggested_action": "Tighten route wording, trigger descriptions, or guardrail phrasing.",
    },
    "skill-overlap": {
        "candidate_type": "skill_patch",
        "suggested_action": "Clarify skill ownership, trigger language, or routing boundaries.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="Packet JSON files or directories containing packet JSON files")
    parser.add_argument("--output", help="Write the aggregate summary to this JSON file")
    return parser.parse_args()


def expand_inputs(values: Iterable[str]) -> list[Path]:
    packets: list[Path] = []
    for value in values:
        path = Path(value).expanduser()
        if path.is_dir():
            packets.extend(sorted(path.glob("*.json")))
        else:
            packets.append(path)
    return packets


def load_packet(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def packet_labels(packet: dict[str, Any]) -> list[str]:
    manual = packet.get("manual_fill", {}).get("pattern_labels", []) or []
    if manual:
        return [str(item) for item in manual]
    return [str(item) for item in packet.get("inferences", {}).get("suggested_labels", []) or []]


def packet_routes(packet: dict[str, Any]) -> list[str]:
    override = packet.get("manual_fill", {}).get("route_override", "")
    if override:
        return [str(override)]
    return [str(item) for item in packet.get("inferences", {}).get("suggested_routes", []) or []]


def main() -> int:
    args = parse_args()
    packet_paths = expand_inputs(args.inputs)
    packets = [load_packet(path) for path in packet_paths]

    label_counts: Counter[str] = Counter()
    route_counts: Counter[str] = Counter()
    tool_counts: Counter[str] = Counter()
    label_to_packets: dict[str, list[str]] = defaultdict(list)
    packet_ids: list[str] = []

    for packet in packets:
        packet_id = packet.get("packet_id", "")
        packet_ids.append(packet_id)
        labels = packet_labels(packet)
        routes = packet_routes(packet)
        label_counts.update(labels)
        route_counts.update(routes)
        for label in labels:
            label_to_packets[label].append(packet_id)

        observations = packet.get("observations", {})
        tool_counts.update(observations.get("tool_calls_by_name", {}) or {})
        tool_counts.update(observations.get("custom_tools_by_name", {}) or {})

    candidate_hypotheses = []
    for label, count in label_counts.most_common():
        rule = RULES.get(label)
        if not rule or count < 2:
            continue
        candidate_hypotheses.append(
            {
                "label": label,
                "count": count,
                "candidate_type": rule["candidate_type"],
                "suggested_action": rule["suggested_action"],
                "evidence_packets": label_to_packets[label],
            }
        )

    if len(packets) < 3:
        next_best_action = "Collect more packets before promoting a historical pattern."
    elif candidate_hypotheses:
        next_best_action = "Take the top candidate through proposal critique or downstream scorecard routing."
    else:
        next_best_action = "Review manual packet labels and candidate cues before promoting a change."

    summary = {
        "schema_version": "codex_session_aggregate_v0_1",
        "packet_count": len(packets),
        "packet_ids": packet_ids,
        "labels": [{"label": key, "count": value} for key, value in label_counts.most_common()],
        "route_suggestions": [{"route": key, "count": value} for key, value in route_counts.most_common()],
        "top_tools": [{"name": key, "count": value} for key, value in tool_counts.most_common(10)],
        "candidate_hypotheses": candidate_hypotheses,
        "next_best_action": next_best_action,
    }

    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
