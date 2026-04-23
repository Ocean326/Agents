#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import random
import re
import ssl
import string
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, urljoin, urlparse
from urllib.request import Request, urlopen


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
GOOGLEBOT_USER_AGENT = (
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
)
TRAILING_URL_CHARS = "，。；！？】）》」』'\""
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".svg"}
COOKIE_ENV_NAMES = {
    "zhihu": ["WEB_PAGE_CAPTURE_ZHIHU_COOKIE", "ZHIHU_COOKIE"],
    "x": ["WEB_PAGE_CAPTURE_X_COOKIE", "X_COOKIE", "TWITTER_COOKIE"],
    "xiaohongshu": [
        "WEB_PAGE_CAPTURE_XIAOHONGSHU_COOKIE",
        "XIAOHONGSHU_COOKIE",
        "XHS_COOKIE",
    ],
}


class CaptureError(RuntimeError):
    pass


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\r\n?", "\n", value).strip()


def html_unescape(value: str | None) -> str:
    return html.unescape(value or "")


def regex_first(text: str, patterns: list[str], flags: int = 0, group: int = 1) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags)
        if match:
            return match.group(group)
    return None


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def extract_first_url(text: str) -> str:
    match = re.search(r"https?://[^\s\u3000]+", text)
    if not match:
        raise CaptureError("No URL found in the provided text.")
    return match.group(0).rstrip(TRAILING_URL_CHARS)


def detect_platform(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "zhihu.com" in host:
        return "zhihu"
    if "x.com" in host or "twitter.com" in host:
        return "x"
    if "xiaohongshu.com" in host or "xhslink.com" in host:
        return "xiaohongshu"
    return "generic"


def strip_html(fragment: str | None) -> str:
    if not fragment:
        return ""
    text = fragment
    text = re.sub(r"<\s*br\s*/?\s*>", "\n", text, flags=re.I)
    text = re.sub(r"</\s*p\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"</\s*li\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<\s*li[^>]*>", "- ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return normalize_text(text)


def decode_js_string(value: str | None) -> str:
    if value is None:
        return ""
    try:
        return json.loads(f'"{value}"')
    except json.JSONDecodeError:
        return html.unescape(value.replace("\\/", "/"))


def sanitize_filename(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", value).strip("_") or "capture"


def first_non_empty(*values: str | None) -> str:
    for value in values:
        if value and str(value).strip():
            return str(value).strip()
    return ""


def private_cookie_candidates(platform: str) -> list[Path]:
    home = Path.home()
    base = home / ".codex" / "private" / "web-page-capture"
    repo_local = Path.cwd() / "butler_private"
    if platform == "zhihu":
        return [
            base / "zhihu.cookie",
            base / "zhihu_cookie.txt",
            repo_local / "zhihu_cookie.txt",
        ]
    if platform == "x":
        return [
            base / "x.cookie",
            base / "x_cookie.txt",
            repo_local / "x_cookie.txt",
        ]
    if platform == "xiaohongshu":
        return [
            base / "xiaohongshu.cookie",
            base / "xiaohongshu_cookie.txt",
            repo_local / "xiaohongshu_cookie.txt",
        ]
    return []


def load_cookie_header(args: argparse.Namespace, platform: str) -> str | None:
    if args.cookie:
        return args.cookie.strip()
    if args.cookie_file:
        return Path(args.cookie_file).expanduser().read_text(encoding="utf-8").strip()
    if args.cookie_env:
        return os.environ.get(args.cookie_env, "").strip() or None
    for env_name in COOKIE_ENV_NAMES.get(platform, []):
        value = os.environ.get(env_name, "").strip()
        if value:
            return value
    for path in private_cookie_candidates(platform):
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
    return None


def decode_response_bytes(body: bytes, content_type: str) -> str:
    charset = regex_first(content_type, [r"charset=([a-zA-Z0-9_-]+)"], flags=re.I)
    for encoding in [charset, "utf-8", "utf-16", "gb18030", "gbk", "latin-1"]:
        if not encoding:
            continue
        try:
            return body.decode(encoding, errors="replace")
        except LookupError:
            continue
    return body.decode("utf-8", errors="replace")


def http_get(
    url: str,
    timeout: int,
    *,
    accept: str = "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
    cookie_header: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> tuple[str, bytes, dict[str, str], int]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept": accept,
    }
    if cookie_header:
        headers["Cookie"] = cookie_header.strip()
    if extra_headers:
        headers.update(extra_headers)
    request = Request(url, headers=headers)
    context = ssl.create_default_context()
    try:
        with urlopen(request, timeout=timeout, context=context) as response:
            body = response.read()
            response_headers = {key: value for key, value in response.headers.items()}
            return response.geturl(), body, response_headers, getattr(response, "status", 200)
    except HTTPError as exc:
        body = exc.read()
        response_headers = {key: value for key, value in exc.headers.items()}
        return exc.geturl(), body, response_headers, exc.code
    except URLError as exc:
        raise CaptureError(f"Network error while fetching {url}: {exc}") from exc


def http_get_text(
    url: str,
    timeout: int,
    *,
    accept: str = "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
    cookie_header: str | None = None,
    extra_headers: dict[str, str] | None = None,
) -> tuple[str, str, dict[str, str], int]:
    final_url, body, headers, status = http_get(
        url,
        timeout,
        accept=accept,
        cookie_header=cookie_header,
        extra_headers=extra_headers,
    )
    content_type = headers.get("Content-Type", "")
    return final_url, decode_response_bytes(body, content_type), headers, status


def json_ld_candidates(html_text: str) -> list[Any]:
    matches = re.findall(
        r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
        html_text,
        flags=re.I | re.S,
    )
    objects: list[Any] = []
    for match in matches:
        raw = html_unescape(match).strip()
        if not raw:
            continue
        try:
            objects.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return objects


def find_json_ld_article_body(html_text: str) -> str:
    for candidate in json_ld_candidates(html_text):
        stack = [candidate]
        while stack:
            current = stack.pop()
            if isinstance(current, dict):
                article_body = current.get("articleBody")
                if isinstance(article_body, str) and article_body.strip():
                    return normalize_text(article_body)
                graph = current.get("@graph")
                if isinstance(graph, list):
                    stack.extend(graph)
                stack.extend(current.values())
            elif isinstance(current, list):
                stack.extend(current)
    return ""


def extract_image_urls(html_text: str, base_url: str) -> list[str]:
    raw_urls: list[str] = []
    raw_urls.extend(
        re.findall(
            r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"',
            html_text,
            flags=re.I,
        )
    )
    raw_urls.extend(
        re.findall(
            r'<img[^>]+(?:src|data-src|data-original)="([^"]+)"',
            html_text,
            flags=re.I,
        )
    )
    result: list[str] = []
    for raw_url in raw_urls:
        cleaned = html_unescape(raw_url).strip()
        if not cleaned or cleaned.startswith("data:"):
            continue
        result.append(urljoin(base_url, cleaned))
    return dedupe_keep_order(result)


def extract_paragraph_text(html_text: str) -> str:
    paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", html_text, flags=re.I | re.S)
    cleaned = [strip_html(item) for item in paragraphs]
    cleaned = [item for item in cleaned if len(item) >= 40]
    return normalize_text("\n\n".join(cleaned[:30]))


def build_sessionless_image_headers(referer: str) -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        "Referer": referer,
    }


def guess_image_extension(url: str, content_type: str | None) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in IMAGE_SUFFIXES:
        return suffix
    lowered = (content_type or "").lower()
    if "png" in lowered:
        return ".png"
    if "webp" in lowered:
        return ".webp"
    if "gif" in lowered:
        return ".gif"
    if "bmp" in lowered:
        return ".bmp"
    if "svg" in lowered:
        return ".svg"
    return ".jpg"


def download_images_for_result(
    result: dict[str, Any],
    output_dir: Path,
    timeout: int,
    cookie_header: str | None,
) -> None:
    image_urls = result.get("images") or []
    if not image_urls:
        return
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    referer = str(result.get("resolved_url") or result.get("source_url") or "")
    assets: list[dict[str, Any]] = []
    for index, image_url in enumerate(image_urls, start=1):
        item: dict[str, Any] = {
            "index": index,
            "url": image_url,
            "status": "pending",
        }
        last_error = ""
        for _ in range(3):
            try:
                _, body, headers, status = http_get(
                    image_url,
                    timeout,
                    accept="image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                    cookie_header=cookie_header,
                    extra_headers=build_sessionless_image_headers(referer),
                )
                if status >= 400:
                    raise CaptureError(f"HTTP {status}")
                suffix = guess_image_extension(image_url, headers.get("Content-Type"))
                digest = hashlib.sha1(image_url.encode("utf-8")).hexdigest()[:12]
                file_path = (images_dir / f"{index:02d}_{digest}{suffix}").resolve()
                file_path.write_bytes(body)
                item["status"] = "downloaded"
                item["local_path"] = str(file_path)
                last_error = ""
                break
            except Exception as exc:
                last_error = str(exc)
        if last_error:
            item["status"] = "error"
            item["error"] = last_error
        assets.append(item)
    result["image_assets"] = assets
    result["image_local_paths"] = [
        str(item["local_path"]) for item in assets if item.get("local_path")
    ]
    if result.get("image_local_paths"):
        result.setdefault("notes", []).append(
            "Images were downloaded locally; follow-on agents should prefer image_local_paths over re-fetching."
        )
    failed = [item for item in assets if item.get("status") != "downloaded"]
    if failed:
        result.setdefault("notes", []).append(
            f"{len(failed)} image downloads failed; see image_assets for details."
        )


def summarize_title_from_text(text: str, fallback: str) -> str:
    first_line = normalize_text(text).splitlines()[0] if normalize_text(text) else ""
    if first_line:
        return first_line[:120]
    return fallback


def infer_content_mode(result: dict[str, Any]) -> tuple[str, str]:
    images = result.get("images") or []
    local_images = result.get("image_local_paths") or []
    text_length = len(normalize_text(str(result.get("content_text") or "")))
    if images and local_images and text_length < 120:
        return "image_primary", "The page is image-heavy or text-light, so local images should be reviewed first."
    if images and local_images:
        return "mixed", "Both extracted text and downloaded images matter for follow-up work."
    return "text_primary", "The extracted text is sufficient as the main working surface."


def attach_agent_handoff(result: dict[str, Any]) -> None:
    content_mode, reason = infer_content_mode(result)
    image_paths = result.get("image_local_paths") or []
    should_read_images_first = bool(image_paths) and content_mode == "image_primary"
    next_step = (
        "Read local images first, then merge the visual details into the summary."
        if should_read_images_first
        else "Start from content_text and use images only as needed."
    )
    result["agent_handoff"] = {
        "content_mode": content_mode,
        "reason": reason,
        "image_count": len(result.get("images") or []),
        "local_image_count": len(image_paths),
        "should_read_images_first": should_read_images_first,
        "recommended_next_step": next_step,
        "ordered_image_paths": image_paths,
    }


def capture_xiaohongshu(source_text: str, timeout: int, cookie_header: str | None) -> dict[str, Any]:
    raw_url = extract_first_url(source_text)
    resolved_url, html_text, _, status = http_get_text(raw_url, timeout, cookie_header=cookie_header)
    if status >= 400:
        raise CaptureError(f"Xiaohongshu returned HTTP {status}.")
    parsed = urlparse(resolved_url)
    raw_parsed = urlparse(raw_url)
    query = parse_qs(parsed.query)
    note_id = (
        (query.get("target_note_id") or [None])[0]
        or regex_first(parsed.path, [r"/explore/([0-9a-z]+)", r"/discovery/item/([0-9a-z]+)"], flags=re.I)
        or regex_first(html_text, [r'"noteId":"([0-9a-z]+)"'], flags=re.I)
        or regex_first(raw_parsed.path, [r"/explore/([0-9a-z]+)", r"/discovery/item/([0-9a-z]+)"], flags=re.I)
    )
    if not note_id:
        raise CaptureError("Opened the Xiaohongshu page but could not locate a note id.")
    xsec_token = (query.get("xsec_token") or [None])[0]
    anchor = html_text.find(f'"noteId":"{note_id}"')
    if anchor == -1:
        anchor = html_text.find(f'"id":"{note_id}"')
    window = html_text[max(0, anchor - 4000) : anchor + 50000] if anchor != -1 else html_text
    title = decode_js_string(regex_first(window, [r'"displayTitle":"(.*?)"', r'"title":"(.*?)"'], flags=re.S))
    desc = decode_js_string(regex_first(window, [r'"desc":"(.*?)"'], flags=re.S))
    author = decode_js_string(
        regex_first(
            window,
            [r'"user":\{"userId":"[^"]+","nickname":"(.*?)"', r'"nickname":"(.*?)"'],
            flags=re.S,
        )
    )
    author_id = regex_first(window, [r'"userId":"([^"]+)"'])
    ip_location = decode_js_string(regex_first(window, [r'"ipLocation":"(.*?)"']))
    published_raw = regex_first(window, [r'"time":(\d{10,13})'])
    updated_raw = regex_first(window, [r'"lastUpdateTime":(\d{10,13})'])
    tags_blob = regex_first(window, [r'"tagList":\[(.*?)\](?:,"lastUpdateTime"|,"cover")'], flags=re.S)
    tags = dedupe_keep_order(
        [decode_js_string(match) for match in re.findall(r'"name":"(.*?)"', tags_blob or "", flags=re.S)]
    )
    images = dedupe_keep_order(
        [decode_js_string(match) for match in re.findall(r'"urlDefault":"(http.*?)"', window, flags=re.S)]
    )
    engagement = {
        "likes": regex_first(window, [r'"likedCount":"([^"]*)"']),
        "comments": regex_first(window, [r'"commentCount":"([^"]*)"']),
        "collects": regex_first(window, [r'"collectedCount":"([^"]*)"']),
        "shares": regex_first(window, [r'"shareCount":"([^"]*)"']),
    }
    content_text = normalize_text(desc)
    title = title or summarize_title_from_text(content_text, note_id)
    return {
        "platform": "xiaohongshu",
        "platform_variant": "share-page",
        "status": "ok",
        "source_url": raw_url,
        "resolved_url": resolved_url,
        "id": note_id,
        "xsec_token": xsec_token,
        "title": title,
        "author": author,
        "author_id": author_id,
        "published_at": iso_from_timestamp_ms(published_raw),
        "updated_at": iso_from_timestamp_ms(updated_raw),
        "ip_location": ip_location,
        "content_text": content_text,
        "tags": tags,
        "images": images,
        "engagement": engagement,
        "notes": [
            "Captured from the share-page HTML; full comment capture is not part of the default contract.",
        ],
    }


def iso_from_timestamp_ms(value: str | None) -> str | None:
    if not value:
        return None
    raw = str(value)
    number = int(raw)
    if len(raw) == 10:
        number *= 1000
    return (
        dt.datetime.fromtimestamp(number / 1000, tz=dt.timezone.utc).astimezone().isoformat()
    )


def normalize_datetime_value(value: str | None) -> str | None:
    if not value:
        return None
    raw = str(value).strip()
    if raw.isdigit():
        return iso_from_timestamp_ms(raw)
    return raw


def extract_zhihu_body(html_text: str) -> str:
    json_ld_body = find_json_ld_article_body(html_text)
    if json_ld_body:
        return json_ld_body
    rich_text_html = regex_first(
        html_text,
        [
            r'<div[^>]+class="[^"]*RichContent-inner[^"]*"[^>]*>([\s\S]*?)</div>\s*</div>',
            r'<div[^>]+class="[^"]*RichText ztext[^"]*"[^>]*>([\s\S]*?)</div>\s*</div>\s*</article>',
            r'<div[^>]+class="[^"]*Post-RichText[^"]*"[^>]*>([\s\S]*?)</div>\s*</div>',
            r'<div[^>]+class="[^"]*RichText[^"]*"[^>]*>([\s\S]*?)</div>',
        ],
        flags=re.S | re.I,
    )
    if rich_text_html:
        cleaned = re.sub(r"<style[\s\S]*?</style>", "", rich_text_html, flags=re.I)
        cleaned = re.sub(r"<script[\s\S]*?</script>", "", cleaned, flags=re.I)
        cleaned = re.sub(r"<button[\s\S]*?</button>", "", cleaned, flags=re.I)
        cleaned = re.sub(r"<figure[\s\S]*?</figure>", "", cleaned, flags=re.I)
        cleaned = re.sub(r'<a [^>]*href="[^"]*"[^>]*>', "", cleaned, flags=re.I)
        cleaned = cleaned.replace("</a>", "")
        return strip_html(cleaned)
    article_html = regex_first(html_text, [r"<article[\s\S]*?</article>"], flags=re.S | re.I, group=0)
    return strip_html(article_html)


def capture_zhihu(source_text: str, timeout: int, cookie_header: str | None) -> dict[str, Any]:
    raw_url = extract_first_url(source_text)
    resolved_url, html_text, _, status = http_get_text(raw_url, timeout, cookie_header=cookie_header)
    if status == 403 or 'id="zh-zse-ck"' in html_text or 'class="Captcha"' in html_text:
        raise CaptureError(
            "Zhihu returned a challenge page or HTTP 403. Provide a private cookie via env or an ignored file and retry."
        )
    if status >= 400:
        raise CaptureError(f"Zhihu returned HTTP {status}.")
    title = normalize_text(
        html_unescape(
            regex_first(
                html_text,
                [
                    r'<meta[^>]+itemProp="headline"[^>]+content="([^"]+)"',
                    r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"',
                    r"<title>(.*?)</title>",
                ],
                flags=re.S | re.I,
            )
            or ""
        )
    )
    author = normalize_text(
        html_unescape(
            regex_first(
                html_text,
                [
                    r'<div[^>]+class="[^"]*AuthorInfo[^"]*"[^>]*itemProp="author"[\s\S]*?<meta[^>]+itemProp="name"[^>]+content="([^"]+)"',
                    r'data-zop="[^"]*&quot;authorName&quot;:&quot;(.*?)&quot;',
                    r'<meta[^>]+itemProp="name"[^>]+content="([^"]+)"',
                    r'<meta[^>]+name="author"[^>]+content="([^"]+)"',
                    r'"authorName":"(.*?)"',
                ],
                flags=re.S | re.I,
            )
            or ""
        )
    )
    published_at = first_non_empty(
        regex_first(
            html_text,
            [
                r'<meta[^>]+itemProp="dateCreated"[^>]+content="([^"]+)"',
                r'<meta[^>]+itemProp="datePublished"[^>]+content="([^"]+)"',
                r'<meta[^>]+property="article:published_time"[^>]+content="([^"]+)"',
                r'"datePublished":"(.*?)"',
                r'"createdTime":(\d+)',
            ],
            flags=re.S | re.I,
        )
    )
    updated_at = first_non_empty(
        regex_first(
            html_text,
            [
                r'<meta[^>]+itemProp="dateModified"[^>]+content="([^"]+)"',
                r'<meta[^>]+property="article:modified_time"[^>]+content="([^"]+)"',
                r'"dateModified":"(.*?)"',
            ],
            flags=re.S | re.I,
        )
    )
    excerpt = normalize_text(
        html_unescape(
            regex_first(
                html_text,
                [
                    r'<meta[^>]+name="description"[^>]+content="([^"]+)"',
                    r'<meta[^>]+property="og:description"[^>]+content="([^"]+)"',
                ],
                flags=re.S | re.I,
            )
            or ""
        )
    )
    content_text = extract_zhihu_body(html_text)
    question_id = regex_first(raw_url, [r"/question/(\d+)"])
    answer_id = regex_first(raw_url, [r"/answer/(\d+)"]) or regex_first(
        html_text,
        [r'"answerId":"?(\d+)"?', r'"token":"(\d+)"'],
        flags=re.S | re.I,
    )
    article_id = regex_first(raw_url, [r"/p/(\d+)"])
    capture_id = answer_id or article_id or question_id or hashlib.sha1(resolved_url.encode("utf-8")).hexdigest()[:12]
    platform_variant = "answer" if answer_id else "article" if article_id else "page"
    images = extract_image_urls(html_text, resolved_url)
    return {
        "platform": "zhihu",
        "platform_variant": platform_variant,
        "status": "ok",
        "source_url": raw_url,
        "resolved_url": resolved_url,
        "id": capture_id,
        "question_id": question_id,
        "answer_id": answer_id,
        "article_id": article_id,
        "title": title or summarize_title_from_text(content_text, capture_id),
        "author": author,
        "published_at": normalize_datetime_value(published_at),
        "updated_at": normalize_datetime_value(updated_at),
        "excerpt": excerpt,
        "content_text": content_text,
        "images": images,
        "engagement": {},
        "notes": [
            "Zhihu often requires a cookie; a successful body capture usually means the current IP or cookie passed validation.",
        ],
    }


def random_token(length: int = 10) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def capture_x(source_text: str, timeout: int, cookie_header: str | None) -> dict[str, Any]:
    raw_url = extract_first_url(source_text)
    status_id = regex_first(raw_url, [r"/status/(\d+)"])
    if not status_id:
        raise CaptureError("Could not determine the X status id from the URL.")
    syndication_url = (
        "https://cdn.syndication.twimg.com/tweet-result"
        f"?id={quote(status_id)}&token={quote(random_token())}&lang=en"
    )
    notes: list[str] = []
    payload: dict[str, Any] | None = None
    last_error: str | None = None
    for _ in range(3):
        try:
            _, raw_json, _, status = http_get_text(
                syndication_url,
                timeout,
                accept="application/json,text/plain;q=0.9,*/*;q=0.8",
                cookie_header=cookie_header,
                extra_headers={"User-Agent": GOOGLEBOT_USER_AGENT},
            )
            if status >= 400:
                raise CaptureError(f"HTTP {status}")
            candidate = json.loads(raw_json or "{}")
            if isinstance(candidate, dict) and candidate:
                payload = candidate
                break
        except Exception as exc:
            last_error = str(exc)
    if not payload:
        fallback_url = (
            "https://publish.twitter.com/oembed?omit_script=true&url=" + quote(raw_url, safe="")
        )
        _, fallback_json, _, status = http_get_text(
            fallback_url,
            timeout,
            accept="application/json,text/plain;q=0.9,*/*;q=0.8",
        )
        if status >= 400:
            raise CaptureError(f"X capture failed: {last_error or f'HTTP {status}'}")
        payload = json.loads(fallback_json or "{}")
        html_block = payload.get("html") or ""
        text = strip_html(regex_first(html_block, [r"<p[^>]*>(.*?)</p>"], flags=re.S | re.I))
        author = payload.get("author_name") or ""
        title = summarize_title_from_text(text, f"Post by @{author}" if author else status_id)
        notes.append("Used oEmbed fallback; text may be shortened compared with the canonical post.")
        return {
            "platform": "x",
            "platform_variant": "oembed-fallback",
            "status": "ok",
            "source_url": raw_url,
            "resolved_url": payload.get("url") or raw_url,
            "id": status_id,
            "title": title,
            "author": author,
            "author_handle": "",
            "published_at": regex_first(html_block, [r">([A-Z][a-z]+ \d{1,2}, \d{4})<"]),
            "updated_at": None,
            "content_text": text,
            "images": [],
            "engagement": {},
            "notes": notes,
        }

    user = payload.get("user") or {}
    text = normalize_text(str(payload.get("text") or ""))
    if isinstance(payload.get("note_tweet"), dict) and "text" not in payload.get("note_tweet", {}):
        notes.append(
            "The public syndication payload exposed a note_tweet stub; long-form post text may be truncated."
        )
    title = summarize_title_from_text(
        text,
        f"Post by @{user.get('screen_name')}" if user.get("screen_name") else status_id,
    )
    images = dedupe_keep_order(
        [item.get("url") for item in (payload.get("photos") or []) if isinstance(item, dict) and item.get("url")]
    )
    media_details = payload.get("mediaDetails") or []
    images.extend(
        [
            item.get("media_url_https")
            for item in media_details
            if isinstance(item, dict) and item.get("media_url_https")
        ]
    )
    images = dedupe_keep_order([str(item) for item in images if item])
    engagement = {
        "likes": payload.get("favorite_count"),
        "replies": payload.get("conversation_count"),
    }
    return {
        "platform": "x",
        "platform_variant": "syndication",
        "status": "ok",
        "source_url": raw_url,
        "resolved_url": raw_url,
        "id": status_id,
        "title": title,
        "author": user.get("name") or "",
        "author_handle": user.get("screen_name") or "",
        "published_at": payload.get("created_at"),
        "updated_at": None,
        "content_text": text,
        "images": images,
        "engagement": engagement,
        "notes": notes,
    }


def capture_generic(source_text: str, timeout: int, cookie_header: str | None) -> dict[str, Any]:
    raw_url = extract_first_url(source_text)
    resolved_url, html_text, _, status = http_get_text(raw_url, timeout, cookie_header=cookie_header)
    if status >= 400:
        raise CaptureError(f"Generic capture returned HTTP {status}.")
    title = normalize_text(
        html_unescape(
            regex_first(
                html_text,
                [
                    r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"',
                    r'<meta[^>]+name="twitter:title"[^>]+content="([^"]+)"',
                    r"<title>(.*?)</title>",
                ],
                flags=re.S | re.I,
            )
            or ""
        )
    )
    author = normalize_text(
        html_unescape(
            regex_first(
                html_text,
                [
                    r'<meta[^>]+name="author"[^>]+content="([^"]+)"',
                    r'<meta[^>]+property="article:author"[^>]+content="([^"]+)"',
                ],
                flags=re.S | re.I,
            )
            or ""
        )
    )
    published_at = first_non_empty(
        regex_first(
            html_text,
            [
                r'<meta[^>]+property="article:published_time"[^>]+content="([^"]+)"',
                r'<time[^>]+datetime="([^"]+)"',
            ],
            flags=re.S | re.I,
        )
    )
    updated_at = first_non_empty(
        regex_first(
            html_text,
            [
                r'<meta[^>]+property="article:modified_time"[^>]+content="([^"]+)"',
                r'<meta[^>]+name="last-modified"[^>]+content="([^"]+)"',
            ],
            flags=re.S | re.I,
        )
    )
    excerpt = normalize_text(
        html_unescape(
            regex_first(
                html_text,
                [
                    r'<meta[^>]+name="description"[^>]+content="([^"]+)"',
                    r'<meta[^>]+property="og:description"[^>]+content="([^"]+)"',
                ],
                flags=re.S | re.I,
            )
            or ""
        )
    )
    content_text = find_json_ld_article_body(html_text)
    if not content_text:
        article_html = regex_first(html_text, [r"<article[\s\S]*?</article>"], flags=re.S | re.I, group=0)
        main_html = regex_first(html_text, [r"<main[\s\S]*?</main>"], flags=re.S | re.I, group=0)
        content_text = strip_html(article_html) or strip_html(main_html) or extract_paragraph_text(html_text)
    images = extract_image_urls(html_text, resolved_url)
    capture_id = hashlib.sha1(resolved_url.encode("utf-8")).hexdigest()[:12]
    return {
        "platform": "generic",
        "platform_variant": "article",
        "status": "ok",
        "source_url": raw_url,
        "resolved_url": resolved_url,
        "id": capture_id,
        "title": title or summarize_title_from_text(content_text, capture_id),
        "author": author,
        "published_at": published_at,
        "updated_at": updated_at,
        "excerpt": excerpt,
        "content_text": content_text,
        "images": images,
        "engagement": {},
        "notes": [
            "Generic extraction favors readable article text over exact DOM fidelity.",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    metadata_keys = [
        "platform",
        "platform_variant",
        "id",
        "source_url",
        "resolved_url",
        "author",
        "author_handle",
        "published_at",
        "updated_at",
        "question_id",
        "answer_id",
        "article_id",
    ]
    lines = [f"# {result.get('title') or result.get('id')}", ""]
    for key in metadata_keys:
        value = result.get(key)
        if value:
            lines.append(f"- {key}: {value}")
    if result.get("engagement"):
        lines.append(f"- engagement: {json.dumps(result['engagement'], ensure_ascii=False)}")
    lines.extend(["", "## Content", "", result.get("content_text") or ""])
    images = result.get("images") or []
    if images:
        lines.extend(["", "## Images", ""])
        assets_by_url = {
            str(item.get("url")): item
            for item in (result.get("image_assets") or [])
            if isinstance(item, dict) and item.get("url")
        }
        for index, image_url in enumerate(images, start=1):
            lines.extend([f"### Image {index}", "", f"- url: {image_url}"])
            asset = assets_by_url.get(str(image_url)) or {}
            if asset.get("local_path"):
                lines.append(f"- local_path: {asset['local_path']}")
            if asset.get("status"):
                lines.append(f"- download_status: {asset['status']}")
            if asset.get("error"):
                lines.append(f"- error: {asset['error']}")
            lines.append("")
    local_paths = result.get("image_local_paths") or []
    if local_paths:
        lines.extend(["## Image Local Paths", ""])
        lines.extend(f"- {path}" for path in local_paths)
    handoff = result.get("agent_handoff") or {}
    if isinstance(handoff, dict) and handoff:
        lines.extend(["", "## Agent Handoff", ""])
        for key in [
            "content_mode",
            "reason",
            "should_read_images_first",
            "recommended_next_step",
        ]:
            value = handoff.get(key)
            if value is not None and value != "":
                lines.append(f"- {key}: {str(value).lower() if isinstance(value, bool) else value}")
    notes = result.get("notes") or []
    if notes:
        lines.extend(["", "## Notes", ""])
        lines.extend(f"- {note}" for note in notes)
    return "\n".join(lines).strip() + "\n"


def render_handoff_markdown(result: dict[str, Any], json_path: Path, md_path: Path) -> str:
    handoff = result.get("agent_handoff") or {}
    lines = [
        "# Web Page Capture Handoff",
        "",
        f"- source_json: {json_path.resolve()}",
        f"- source_md: {md_path.resolve()}",
        f"- platform: {result.get('platform') or ''}",
        f"- note_id: {result.get('id') or ''}",
        f"- title: {result.get('title') or ''}",
        f"- author: {result.get('author') or ''}",
        f"- content_mode: {handoff.get('content_mode') or ''}",
        f"- should_read_images_first: {str(bool(handoff.get('should_read_images_first'))).lower()}",
    ]
    if handoff.get("reason"):
        lines.append(f"- reason: {handoff['reason']}")
    if handoff.get("recommended_next_step"):
        lines.append(f"- recommended_next_step: {handoff['recommended_next_step']}")
    lines.extend(["", "## Ordered Image Paths", ""])
    image_paths = result.get("image_local_paths") or []
    if image_paths:
        lines.extend(f"{index}. {path}" for index, path in enumerate(image_paths, start=1))
    else:
        lines.append("(none)")
    return "\n".join(lines).strip() + "\n"


def output_stem(result: dict[str, Any]) -> str:
    base = f"{result.get('platform') or 'capture'}_{result.get('id') or 'capture'}"
    return sanitize_filename(base)


def write_outputs(result: dict[str, Any], output_dir: Path) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = output_stem(result)
    json_path = output_dir / f"{stem}.json"
    md_path = output_dir / f"{stem}.md"
    handoff_path = output_dir / f"{stem}_handoff.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(result), encoding="utf-8")
    handoff_path.write_text(render_handoff_markdown(result, json_path, md_path), encoding="utf-8")
    return json_path, md_path, handoff_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture a single web page into JSON, Markdown, handoff, and images.")
    parser.add_argument("source", help="A single URL, or share text that contains a URL.")
    parser.add_argument("--platform", choices=["auto", "generic", "x", "zhihu", "xiaohongshu"], default="auto")
    parser.add_argument("--cookie", help="Inline Cookie header value.")
    parser.add_argument("--cookie-file", help="Read the Cookie header from a file.")
    parser.add_argument("--cookie-env", help="Read the Cookie header from an environment variable.")
    parser.add_argument("--output-dir", help="Output directory. If omitted, only JSON is printed.")
    parser.add_argument("--timeout", type=int, default=20, help="Per-request timeout in seconds.")
    parser.add_argument(
        "--skip-image-download",
        action="store_true",
        help="Do not download images even when an output directory is supplied.",
    )
    return parser.parse_args()


def main() -> int:
    configure_stdout()
    args = parse_args()
    try:
        raw_url = extract_first_url(args.source)
        platform = args.platform if args.platform != "auto" else detect_platform(raw_url)
        cookie_header = load_cookie_header(args, platform)
        if platform == "zhihu":
            result = capture_zhihu(args.source, args.timeout, cookie_header)
        elif platform == "x":
            result = capture_x(args.source, args.timeout, cookie_header)
        elif platform == "xiaohongshu":
            result = capture_xiaohongshu(args.source, args.timeout, cookie_header)
        elif platform == "generic":
            result = capture_generic(args.source, args.timeout, cookie_header)
        else:
            raise CaptureError(f"Unsupported platform: {platform}")
        if args.output_dir:
            output_dir = Path(args.output_dir).expanduser().resolve()
            if not args.skip_image_download:
                download_images_for_result(result, output_dir, args.timeout, cookie_header)
            attach_agent_handoff(result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            json_path, md_path, handoff_path = write_outputs(result, output_dir)
            print(f"OUTPUT_JSON={json_path}")
            print(f"OUTPUT_MD={md_path}")
            print(f"OUTPUT_HANDOFF={handoff_path}")
        else:
            attach_agent_handoff(result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        error_payload = {
            "status": "error",
            "platform": locals().get("platform", args.platform),
            "source_url": locals().get("raw_url", args.source),
            "message": str(exc),
        }
        print(json.dumps(error_payload, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
