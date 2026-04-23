#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import http.client
import json
import re
import time
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

USER_AGENT = "Codex Literature Finder/1.0"
REQUEST_GAP_SEC = 0.1
REQUEST_TIMEOUT_SEC = 10

try:
    import bibtexparser  # type: ignore
except ImportError:
    bibtexparser = None


@dataclass
class Entry:
    entry_type: str
    cite_key: str
    title: str
    authors: str
    year: str
    venue: str
    doi: str
    url: str


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_doi(value: str) -> str:
    value = normalize_whitespace(value)
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.I)
    return value.strip()


def safe_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
    return value[:120] or "paper"


def title_similarity(a: str, b: str) -> float:
    norm_a = re.sub(r"[^a-z0-9]+", " ", a.lower()).strip()
    norm_b = re.sub(r"[^a-z0-9]+", " ", b.lower()).strip()
    if not norm_a or not norm_b:
        return 0.0
    return SequenceMatcher(None, norm_a, norm_b).ratio()


def infer_year(value: str) -> str:
    match = re.search(r"(19|20)\d{2}", value or "")
    return match.group(0) if match else ""


def get_json(url: str) -> Any | None:
    for attempt in range(3):
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=REQUEST_TIMEOUT_SEC) as response:
                return json.loads(response.read().decode("utf-8"))
        except (
            HTTPError,
            URLError,
            TimeoutError,
            json.JSONDecodeError,
            http.client.RemoteDisconnected,
            ConnectionResetError,
        ):
            if attempt == 2:
                return None
            time.sleep(0.8 * (attempt + 1))
    return None


def parse_bib_value(value: str) -> str:
    value = value.strip().rstrip(",").strip()
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    elif value.startswith("{") and value.endswith("}"):
        value = value[1:-1]
    value = value.replace(r"\/", "/")
    value = value.replace(r"\&", "&")
    value = value.replace(r"\\", "\\")
    return normalize_whitespace(value)


def parse_bibtex(text: str) -> list[Entry]:
    if bibtexparser is not None:
        parser = bibtexparser.bparser.BibTexParser(common_strings=True)
        db = bibtexparser.loads(text, parser=parser)
        return [
            Entry(
                entry_type=(item.get("ENTRYTYPE") or "").lower(),
                cite_key=item.get("ID") or "",
                title=normalize_whitespace(item.get("title") or ""),
                authors=normalize_whitespace(item.get("author") or ""),
                year=normalize_whitespace(item.get("year") or ""),
                venue=normalize_whitespace(
                    item.get("journal") or item.get("booktitle") or item.get("publisher") or ""
                ),
                doi=normalize_doi(item.get("doi") or ""),
                url=normalize_whitespace(item.get("url") or ""),
            )
            for item in db.entries
        ]

    chunks = re.split(r"(?m)^@", text)
    field_re = re.compile(
        r'(?ms)^\s*([A-Za-z][A-Za-z0-9_]*)\s*=\s*(".*?"|\{.*?\}|[^,\n]+)\s*,?\s*$'
    )
    entries: list[Entry] = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        entry_text = "@" + chunk
        header = re.match(r"@(\w+)\{([^,]+),", entry_text)
        if not header:
            continue
        entry_type, cite_key = header.groups()
        fields: dict[str, str] = {}
        for match in field_re.finditer(entry_text):
            fields[match.group(1).lower()] = parse_bib_value(match.group(2))
        entries.append(
            Entry(
                entry_type=entry_type.lower(),
                cite_key=cite_key,
                title=fields.get("title", ""),
                authors=fields.get("author", ""),
                year=fields.get("year", ""),
                venue=fields.get("journal") or fields.get("booktitle") or fields.get("publisher") or "",
                doi=normalize_doi(fields.get("doi", "")),
                url=fields.get("url", ""),
            )
        )
    return entries


def parse_enw(text: str) -> list[Entry]:
    entries: list[Entry] = []
    current: dict[str, list[str]] = {}
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("%0 ") and current:
            entries.append(build_enw_entry(current))
            current = {}
        if len(line) >= 3 and line[0] == "%" and line[2] == " ":
            current.setdefault(line[1], []).append(line[3:].strip())
    if current:
        entries.append(build_enw_entry(current))
    return [entry for entry in entries if entry.title or entry.doi or entry.url]


def build_enw_entry(fields: dict[str, list[str]]) -> Entry:
    doi = ""
    for value in fields.get("R", []):
        if normalize_doi(value).startswith("10."):
            doi = normalize_doi(value)
            break
    year = ""
    for key in ("D", "8"):
        if fields.get(key):
            year = infer_year(fields[key][0])
            if year:
                break
    return Entry(
        entry_type=(fields.get("0") or [""])[0].lower(),
        cite_key="",
        title=normalize_whitespace(" ".join(fields.get("T", []))),
        authors=normalize_whitespace(" and ".join(fields.get("A", []))),
        year=year,
        venue=normalize_whitespace(" ".join(fields.get("B", []) or fields.get("J", []))),
        doi=doi,
        url=normalize_whitespace(" ".join(fields.get("U", []))),
    )


def parse_ris(text: str) -> list[Entry]:
    entries: list[Entry] = []
    current: dict[str, list[str]] = {}
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.startswith("ER"):
            if current:
                entries.append(build_ris_entry(current))
            current = {}
            continue
        if len(line) >= 6 and line[2:6] == "  - ":
            current.setdefault(line[:2], []).append(line[6:].strip())
    if current:
        entries.append(build_ris_entry(current))
    return [entry for entry in entries if entry.title or entry.doi or entry.url]


def build_ris_entry(fields: dict[str, list[str]]) -> Entry:
    year = ""
    for key in ("PY", "Y1", "DA"):
        if fields.get(key):
            year = infer_year(fields[key][0])
            if year:
                break
    return Entry(
        entry_type=(fields.get("TY") or [""])[0].lower(),
        cite_key="",
        title=normalize_whitespace(" ".join(fields.get("TI", []) or fields.get("T1", []))),
        authors=normalize_whitespace(" and ".join(fields.get("AU", []) or fields.get("A1", []))),
        year=year,
        venue=normalize_whitespace(
            " ".join(fields.get("JO", []) or fields.get("JF", []) or fields.get("T2", []) or fields.get("BT", []))
        ),
        doi=normalize_doi(" ".join(fields.get("DO", []))),
        url=normalize_whitespace(" ".join(fields.get("UR", []))),
    )


def parse_identifier_lines(text: str) -> list[Entry]:
    entries: list[Entry] = []
    for line in text.splitlines():
        raw = normalize_whitespace(line)
        if not raw or raw.startswith("#"):
            continue
        doi = ""
        url = ""
        title = ""
        arxiv_match = re.fullmatch(r"(\d{4}\.\d{4,5})(v\d+)?", raw)
        if raw.startswith("10."):
            doi = normalize_doi(raw)
        elif raw.startswith("http://") or raw.startswith("https://"):
            url = raw
            doi_match = re.search(r"doi\.org/(10\.\S+)", raw, flags=re.I)
            if doi_match:
                doi = normalize_doi(doi_match.group(1))
        elif arxiv_match:
            title = raw
            doi = f"10.48550/arXiv.{arxiv_match.group(1)}"
        else:
            title = raw
        entries.append(
            Entry(
                entry_type="",
                cite_key="",
                title=title,
                authors="",
                year="",
                venue="",
                doi=doi,
                url=url,
            )
        )
    return entries


def parse_source(source: Path) -> list[Entry]:
    text = source.read_text(encoding="utf-8", errors="ignore")
    suffix = source.suffix.lower()
    if suffix == ".bib":
        return parse_bibtex(text)
    if suffix == ".enw":
        return parse_enw(text)
    if suffix == ".ris":
        return parse_ris(text)
    return parse_identifier_lines(text)


def load_manual_overrides(path: Path | None) -> dict[str, dict[str, str]]:
    if path is None:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    overrides: dict[str, dict[str, str]] = {}
    for key, value in data.items():
        overrides[normalize_whitespace(key).lower()] = {
            str(inner_key): str(inner_value)
            for inner_key, inner_value in (value or {}).items()
            if inner_value is not None
        }
    return overrides


def extract_openalex_record(data: dict[str, Any] | None) -> dict[str, str]:
    if not data:
        return {}
    best_oa_location = data.get("best_oa_location") or {}
    primary_location = data.get("primary_location") or {}
    open_access = data.get("open_access") or {}
    ids = data.get("ids") or {}
    return {
        "resolved_doi": normalize_doi(ids.get("doi") or ""),
        "is_oa": "yes" if open_access.get("is_oa") else "no",
        "landing_page_url": (
            best_oa_location.get("landing_page_url")
            or primary_location.get("landing_page_url")
            or ""
        ),
        "pdf_url": best_oa_location.get("pdf_url") or "",
        "host_venue": normalize_whitespace(((best_oa_location.get("source") or {}).get("display_name")) or ""),
    }


def openalex_by_doi(doi: str) -> dict[str, str]:
    if not doi:
        return {}
    time.sleep(REQUEST_GAP_SEC)
    url = f"https://api.openalex.org/works/https://doi.org/{quote(doi, safe='')}"
    return extract_openalex_record(get_json(url))


def openalex_by_title(title: str, year: str) -> dict[str, str]:
    if not title:
        return {}
    time.sleep(REQUEST_GAP_SEC)
    url = f"https://api.openalex.org/works?search={quote(title)}&per-page=5"
    data = get_json(url)
    if not data or not data.get("results"):
        return {}
    year_int = int(year) if year.isdigit() else None
    ranked: list[tuple[float, dict[str, Any]]] = []
    for result in data["results"]:
        score = title_similarity(title, result.get("display_name") or "")
        if year_int and result.get("publication_year") == year_int:
            score += 0.08
        ranked.append((score, result))
    ranked.sort(key=lambda item: item[0], reverse=True)
    best_score, best_result = ranked[0]
    if best_score < 0.72:
        return {}
    return extract_openalex_record(best_result)


def manual_search_url(title: str) -> str:
    return f"https://www.semanticscholar.org/search?q={quote(title)}" if title else ""


def build_rows(entries: list[Entry], overrides: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    total = len(entries)
    for index, entry in enumerate(entries, start=1):
        print(f"[{index}/{total}] resolving {entry.title[:100] or entry.doi or entry.url}", flush=True)
        doi = normalize_doi(entry.doi)
        arxiv_id = ""
        if doi.lower().startswith("10.48550/arxiv."):
            arxiv_id = re.sub(r"^10\.48550/arxiv\.", "", doi, flags=re.I)

        oa = openalex_by_doi(doi) if doi and not arxiv_id else {}
        resolved_via = "openalex-doi" if oa else ""
        if not oa and entry.title:
            oa = openalex_by_title(entry.title, entry.year)
            if oa:
                resolved_via = "openalex-title"

        best_landing_url = ""
        best_pdf_url = ""
        if arxiv_id:
            best_landing_url = f"https://arxiv.org/abs/{arxiv_id}"
            best_pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            resolved_via = "arxiv-doi"
        else:
            best_landing_url = oa.get("landing_page_url") or entry.url or (f"https://doi.org/{doi}" if doi else "")
            best_pdf_url = oa.get("pdf_url") or ""

        resolved_doi = oa.get("resolved_doi") or doi
        is_oa = "yes" if arxiv_id else oa.get("is_oa") or "unknown"
        host_venue = oa.get("host_venue") or ""

        retrieval_note = "manual_title_search"
        if best_pdf_url:
            retrieval_note = "direct_oa_pdf"
        elif doi or resolved_doi:
            retrieval_note = "landing_page_or_publisher"
        elif entry.url:
            retrieval_note = "source_url_only"

        override = overrides.get(normalize_whitespace(entry.title).lower(), {})
        if override:
            resolved_doi = override.get("resolved_doi") or resolved_doi
            best_landing_url = override.get("best_landing_url") or best_landing_url
            best_pdf_url = override.get("best_pdf_url") or best_pdf_url
            retrieval_note = override.get("retrieval_note") or retrieval_note
            resolved_via = override.get("resolved_via") or resolved_via
            is_oa = override.get("is_oa") or is_oa

        rows.append(
            {
                "index": str(index),
                "entry_type": entry.entry_type,
                "cite_key": entry.cite_key,
                "title": entry.title,
                "authors": entry.authors,
                "year": entry.year,
                "venue": entry.venue,
                "original_doi": doi,
                "original_url": entry.url,
                "resolved_doi": resolved_doi,
                "resolved_via": resolved_via,
                "is_oa": is_oa,
                "best_landing_url": best_landing_url,
                "best_pdf_url": best_pdf_url,
                "host_venue": host_venue,
                "manual_search_url": manual_search_url(entry.title),
                "retrieval_note": retrieval_note,
            }
        )
    return rows


def summarize(rows: list[dict[str, str]]) -> dict[str, int]:
    summary = {
        "total": len(rows),
        "direct_oa_pdf": 0,
        "landing_page_or_publisher": 0,
        "source_url_only": 0,
        "manual_title_search": 0,
    }
    for row in rows:
        note = row["retrieval_note"]
        if note in summary:
            summary[note] += 1
    return summary


def write_csv(rows: list[dict[str, str]], path: Path, fieldnames: list[str] | None = None) -> None:
    fieldnames = fieldnames or list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        if fieldnames:
            writer.writerows(
                [{field: row.get(field, "") for field in fieldnames} for row in rows]
            )
        else:
            writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]], path: Path, title: str, count_label: str) -> None:
    lines = [
        f"# {title}",
        "",
        f"- Count: `{len(rows)}`",
        "",
        "| # | Year | Title | DOI | Landing | PDF URL |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        title_value = row["title"].replace("|", "\\|")
        landing = f"[link]({row['best_landing_url']})" if row["best_landing_url"] else ""
        pdf_url = f"[pdf]({row['best_pdf_url']})" if row["best_pdf_url"] else ""
        lines.append(
            f"| {row['index']} | {row['year']} | {title_value} | {row['resolved_doi']} | {landing} | {pdf_url} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_references_markdown(
    rows: list[dict[str, str]],
    summary: dict[str, int],
    path: Path,
    source: Path,
) -> None:
    lines = [
        "# Literature Library Seed",
        "",
        f"- Source file: `{source}`",
        f"- Total entries: `{summary['total']}`",
        f"- Direct OA PDF found: `{summary['direct_oa_pdf']}`",
        f"- Landing page or publisher page available: `{summary['landing_page_or_publisher']}`",
        f"- Manual title search still needed: `{summary['manual_title_search']}`",
        "",
        "## Retrieval Table",
        "",
        "| # | Year | Title | DOI | OA PDF | Landing | Note |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        doi = row["resolved_doi"] or row["original_doi"]
        pdf_md = f"[pdf]({row['best_pdf_url']})" if row["best_pdf_url"] else ""
        landing_md = f"[link]({row['best_landing_url']})" if row["best_landing_url"] else ""
        title_value = row["title"].replace("|", "\\|")
        lines.append(
            f"| {row['index']} | {row['year']} | {title_value} | {doi} | {pdf_md} | {landing_md} | {row['retrieval_note']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_identifier_list(rows: list[dict[str, str]], path: Path) -> None:
    identifiers: list[str] = []
    for row in rows:
        doi = row["resolved_doi"] or row["original_doi"]
        if doi:
            identifiers.append(doi)
            continue
        landing = row["best_landing_url"]
        match = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]+\.[0-9]+)", landing)
        if match:
            identifiers.append(match.group(1))
    deduped = list(dict.fromkeys(item for item in identifiers if item))
    path.write_text("\n".join(deduped) + ("\n" if deduped else ""), encoding="utf-8")


def write_pdf_candidate_list(rows: list[dict[str, str]], path: Path) -> None:
    deduped = list(dict.fromkeys(row["best_pdf_url"] for row in rows if row["best_pdf_url"]))
    path.write_text("\n".join(deduped) + ("\n" if deduped else ""), encoding="utf-8")


def download_pdfs(rows: list[dict[str, str]], pdf_dir: Path) -> list[str]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/pdf,application/octet-stream,*/*",
    }
    pdf_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[str] = []
    for row in rows:
        pdf_url = row["best_pdf_url"]
        if not pdf_url:
            continue
        filename = safe_filename(f"{row['index']}_{row['year']}_{row['title']}") + ".pdf"
        out_path = pdf_dir / filename
        if out_path.exists():
            downloaded.append(filename)
            continue
        request = Request(pdf_url, headers=headers)
        try:
            with urlopen(request, timeout=REQUEST_TIMEOUT_SEC) as response:
                content_type = response.headers.get("Content-Type", "")
                data = response.read()
            if "pdf" not in content_type.lower() and not data.startswith(b"%PDF"):
                continue
            out_path.write_bytes(data)
            downloaded.append(filename)
            time.sleep(REQUEST_GAP_SEC)
        except (HTTPError, URLError, TimeoutError, http.client.RemoteDisconnected, ConnectionResetError):
            continue
    return downloaded


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manual-overrides", type=Path)
    parser.add_argument("--download-pdfs", action="store_true")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    entries = parse_source(args.source)
    overrides = load_manual_overrides(args.manual_overrides)
    rows = build_rows(entries, overrides)
    summary = summarize(rows)

    references_csv = args.output_dir / "references.csv"
    references_md = args.output_dir / "references.md"
    summary_json = args.output_dir / "summary.json"
    identifiers_txt = args.output_dir / "zotero_identifiers.txt"
    oa_urls_txt = args.output_dir / "oa_pdf_urls.txt"
    remaining_csv = args.output_dir / "remaining_oa_to_resolve.csv"
    remaining_md = args.output_dir / "remaining_oa_to_resolve.md"

    write_csv(rows, references_csv)
    write_references_markdown(rows, summary, references_md, args.source)
    write_identifier_list(rows, identifiers_txt)
    write_pdf_candidate_list(rows, oa_urls_txt)

    remaining_rows = [
        row
        for row in rows
        if row["retrieval_note"] == "direct_oa_pdf" and row["best_pdf_url"]
    ]

    downloaded: list[str] = []
    if args.download_pdfs:
        downloaded = download_pdfs(remaining_rows, args.output_dir / "pdfs")
        downloaded_prefixes = {name.split("_", 1)[0] for name in downloaded}
        remaining_rows = [
            row for row in remaining_rows if row["index"] not in downloaded_prefixes
        ]

    write_csv(
        remaining_rows,
        remaining_csv,
        fieldnames=["index", "year", "title", "resolved_doi", "best_landing_url", "best_pdf_url"],
    )
    write_markdown(
        remaining_rows,
        remaining_md,
        title="Remaining OA To Resolve",
        count_label="Count",
    )

    payload: dict[str, Any] = {
        "source_file": str(args.source),
        "output_dir": str(args.output_dir),
        "summary": summary,
        "identifier_file": str(identifiers_txt),
        "oa_pdf_url_file": str(oa_urls_txt),
        "remaining_oa_file": str(remaining_csv),
    }
    if args.manual_overrides:
        payload["manual_overrides"] = str(args.manual_overrides)
    if args.download_pdfs:
        payload["downloaded_pdfs"] = len(downloaded)
        payload["downloaded_filenames"] = downloaded

    summary_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
