#!/usr/bin/env python3
"""
Check local-first prerequisites for the web-finder skill.

Reports core tools, optional local discovery upgrades, and installed helper skills.
Returns exit code 0 even when optional components are missing.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path


def has_command(name: str) -> bool:
    return shutil.which(name) is not None


def env_present(name: str) -> bool:
    return bool(os.environ.get(name))


def http_ok(url: str, timeout: float = 2.0) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "web-finder-check"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 300
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return False


def build_report() -> dict:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    skills_root = codex_home / "skills"

    helper_skills = {
        "skill-finder": skills_root / "skill-finder",
        "searxng-search": skills_root / "searxng-search",
        "web-page-capture": skills_root / "web-page-capture",
        "reddit-fetch": skills_root / "reddit-fetch",
        "article-extractor": skills_root / "article-extractor",
        "youtube-transcript": skills_root / "youtube-transcript",
    }

    commands = {
        "python3": has_command("python3"),
        "curl": has_command("curl"),
        "jq": has_command("jq"),
        "rg": has_command("rg"),
        "yt-dlp": has_command("yt-dlp"),
        "tmux": has_command("tmux"),
        "trafilatura": has_command("trafilatura"),
        "docker-compose": has_command("docker-compose"),
        "gh": has_command("gh"),
    }

    services = {
        "searxng_adapter": {
            "url": "http://localhost:8000/health",
            "ok": http_ok("http://localhost:8000/health"),
        }
    }

    env_vars = {
        "TAVILY_API_KEY": env_present("TAVILY_API_KEY"),
    }

    skills = {name: path.is_dir() for name, path in helper_skills.items()}

    core_ready = commands["python3"] and commands["curl"]
    local_first_upgrades = (
        services["searxng_adapter"]["ok"]
        or skills["searxng-search"]
        or skills["web-page-capture"]
    )
    tavily_ready = env_vars["TAVILY_API_KEY"]

    recommendations = []
    if not commands["jq"]:
        recommendations.append("Install `jq` for easier structured API and search result handling.")
    if not commands["trafilatura"]:
        recommendations.append("Install `trafilatura` so `article-extractor` can clean blog and article pages reliably.")
    if not commands["docker-compose"]:
        recommendations.append("Install `docker-compose` so the local SearXNG adapter stack can be started.")
    if not skills["searxng-search"]:
        recommendations.append("Install `searxng-search` to route broad web discovery through a local-first search lane.")
    if not skills["web-page-capture"]:
        recommendations.append("Install `web-page-capture` to turn discovered URLs into reusable local artifacts.")
    if not services["searxng_adapter"]["ok"]:
        recommendations.append("Optional: start a local SearXNG adapter on `localhost:8000` for self-hosted local-first search.")
    if not tavily_ready:
        recommendations.append("Optional: set `TAVILY_API_KEY` only if you need broader fallback search beyond local/public routes.")
    if not skills["reddit-fetch"]:
        recommendations.append("Optional: install `reddit-fetch` for cleaner Reddit thread retrieval.")
    if not skills["article-extractor"]:
        recommendations.append("Optional: install `article-extractor` for blog/article cleanup.")
    if not skills["youtube-transcript"]:
        recommendations.append("Optional: install `youtube-transcript` for video-to-text follow-up.")

    return {
        "codex_home": str(codex_home),
        "skills_root": str(skills_root),
        "core_ready": core_ready,
        "local_first_ready": local_first_upgrades,
        "tavily_ready": tavily_ready,
        "commands": commands,
        "services": services,
        "env_vars": env_vars,
        "skills": skills,
        "recommendations": recommendations,
    }


def print_human(report: dict) -> None:
    def marker(ok: bool) -> str:
        return "[OK]" if ok else "[MISSING]"

    print("Web Finder Setup Check")
    print()
    print("Core tools")
    for name in ("python3", "curl", "jq", "rg"):
        print(f"  {marker(report['commands'][name])} {name}")

    print()
    print("Optional commands")
    for name in ("gh", "tmux", "yt-dlp", "trafilatura", "docker-compose"):
        print(f"  {marker(report['commands'][name])} {name}")

    print()
    print("Local services")
    for name, item in report["services"].items():
        label = f"{name} ({item['url']})"
        print(f"  {marker(item['ok'])} {label}")

    print()
    print("Installed helper skills")
    for name, ok in report["skills"].items():
        print(f"  {marker(ok)} {name}")

    print()
    print("Optional environment")
    for name, ok in report["env_vars"].items():
        print(f"  {marker(ok)} {name}")

    print()
    print("Summary")
    print(f"  core_ready={report['core_ready']}")
    print(f"  local_first_ready={report['local_first_ready']}")
    print(f"  tavily_ready={report['tavily_ready']}")

    if report["recommendations"]:
        print()
        print("Recommended next steps")
        for idx, item in enumerate(report["recommendations"], start=1):
            print(f"  {idx}. {item}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable output.")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        json.dump(report, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print_human(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
