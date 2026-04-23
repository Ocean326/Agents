#!/usr/bin/env python3
import argparse
import codecs
import json
import os
import pty
import select
import subprocess
import sys
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Cursor stream-json into cleaner stdout.")
    parser.add_argument("--render", choices=("assistant-text", "md"), required=True)
    parser.add_argument("--requested-model", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    return parser.parse_args()


def extract_text(payload: dict[str, Any]) -> str:
    message = payload.get("message") or {}
    content = message.get("content") or []
    parts: list[str] = []
    for item in content:
        if item.get("type") == "text":
            parts.append(item.get("text", ""))
    return "".join(parts)


def merge_piece(existing: str, incoming: str) -> tuple[str, str]:
    if not incoming:
        return "", existing
    if not existing:
        return incoming, incoming
    if incoming == existing:
        return "", existing
    if incoming.startswith(existing):
        return incoming[len(existing):], incoming
    if existing.startswith(incoming):
        return "", existing
    if incoming in existing:
        return "", existing
    return incoming, existing + incoming


def emit(text: str) -> None:
    sys.stdout.write(text)
    sys.stdout.flush()


def main() -> int:
    args = parse_args()
    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]

    if not command:
        emit("[cursor-stream-render] missing command\n")
        return 2

    aggregated = ""
    emitted_any = False
    result_seen = False
    init_payload: dict[str, Any] = {}
    result_payload: dict[str, Any] = {}

    if args.render == "md":
        emit("## Cursor Response\n\n")
        emit(f"- requested_model: `{args.requested_model}`\n")
        emit(f"- mode: `{args.mode}`\n")
        emit("\n")

    master_fd, slave_fd = pty.openpty()
    process = subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
    )
    os.close(slave_fd)

    buffer = ""
    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")

    def handle_line(line: str) -> None:
        nonlocal aggregated, emitted_any, init_payload, result_payload, result_seen
        stripped = line.strip()
        if not stripped:
            return
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            return

        payload_type = payload.get("type")
        if payload_type == "system" and payload.get("subtype") == "init":
            init_payload = payload
            return

        if payload_type == "assistant":
            text = extract_text(payload)
            piece, aggregated = merge_piece(aggregated, text)
            if piece:
                emit(piece)
                emitted_any = True
            return

        if payload_type == "result":
            result_payload = payload
            result_seen = True
            final_text = payload.get("result") or ""
            piece, aggregated = merge_piece(aggregated, final_text)
            if piece:
                emit(piece)
                emitted_any = True
            return

    try:
        while True:
            ready, _, _ = select.select([master_fd], [], [], 0.1)
            if ready:
                try:
                    chunk = os.read(master_fd, 4096)
                except OSError:
                    chunk = b""
                if chunk:
                    buffer += decoder.decode(chunk)
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        handle_line(line.rstrip("\r"))
                    continue
            if process.poll() is not None:
                break
        buffer += decoder.decode(b"", final=True)
        if buffer:
            handle_line(buffer.rstrip("\r"))
    finally:
        try:
            os.close(master_fd)
        except OSError:
            pass

    return_code = process.wait()

    if args.render == "md":
        if emitted_any:
            emit("\n")
        else:
            emit("_No assistant text returned._\n")
        emit("\n<details>\n<summary>Cursor run metadata</summary>\n\n")
        reported_model = init_payload.get("model")
        session_id = result_payload.get("session_id") or init_payload.get("session_id")
        request_id = result_payload.get("request_id")
        duration_ms = result_payload.get("duration_ms")
        is_error = result_payload.get("is_error")
        usage = result_payload.get("usage") or {}
        if reported_model:
            emit(f"- reported_model: `{reported_model}`\n")
        if session_id:
            emit(f"- session_id: `{session_id}`\n")
        if request_id:
            emit(f"- request_id: `{request_id}`\n")
        if duration_ms is not None:
            emit(f"- duration_ms: `{duration_ms}`\n")
        if is_error is not None:
            emit(f"- result: `{'error' if is_error else 'success'}`\n")
        emit(f"- workspace: `{args.workspace}`\n")
        if usage:
            usage_parts = []
            for key in ("inputTokens", "outputTokens", "cacheReadTokens", "cacheWriteTokens"):
                if key in usage:
                    usage_parts.append(f"{key}={usage[key]}")
            if usage_parts:
                emit(f"- usage: `{', '.join(usage_parts)}`\n")
        emit("\n</details>\n")

    if not result_seen:
        if not emitted_any:
            emit("\n[cursor-stream-render] no result event received\n")
        return 1 if return_code == 0 else return_code

    if result_payload.get("is_error"):
        return 1
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
