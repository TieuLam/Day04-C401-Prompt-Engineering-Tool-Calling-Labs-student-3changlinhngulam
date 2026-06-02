from __future__ import annotations

from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


TRACKING_PARAMS = {
    "fbclid",
    "gclid",
    "dclid",
    "gbraid",
    "wbraid",
    "mc_cid",
    "mc_eid",
    "igshid",
    "msclkid",
    "yclid",
}


def _domain(url: str) -> str:
    parsed = urlparse(url or "")
    if not parsed.scheme and "." in parsed.path:
        parsed = urlparse("https://" + (url or ""))
    return parsed.netloc.lower().replace("www.", "")


def _canonical_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if not parsed.scheme and "." in parsed.path:
        parsed = urlparse("https://" + url)

    kept = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        lower = key.lower()
        if lower.startswith("utm_") or lower in TRACKING_PARAMS:
            continue
        kept.append((key, value))

    query = urlencode(kept, doseq=True)
    path = parsed.path.rstrip("/") or parsed.path

    return urlunparse(
        (
            parsed.scheme.lower() or "https",
            parsed.netloc.lower().replace("www.", ""),
            path,
            "",
            query,
            "",
        )
    )


def _title_key(title: str) -> str:
    return " ".join((title or "").lower().strip().split())


def dedupe_sources(
    items: list[dict[str, Any]] | None = None,
    unique_by: str = "url",
    max_items: int = 20,
) -> dict[str, Any]:
    """
    Remove duplicate source items from lookup/fetch/social results.

    unique_by:
      - "url": remove items with the same canonical URL
      - "domain": keep one item per domain
      - "title": remove items with the same normalized title
      - "url_or_title": remove by canonical URL, falling back to normalized title
    """
    try:
        items = items or []
        unique_by = (unique_by or "url").lower()
        max_items = max(1, min(int(max_items or 20), 100))

        if unique_by not in {"url", "domain", "title", "url_or_title"}:
            unique_by = "url"

        seen: dict[str, int] = {}
        unique_items: list[dict[str, Any]] = []
        duplicate_groups: dict[str, list[dict[str, Any]]] = {}

        for item in items:
            if not isinstance(item, dict):
                continue

            url = str(item.get("url", "") or "")
            title = str(item.get("title", "") or "")
            canonical_url = _canonical_url(url)
            domain = _domain(url)

            if unique_by == "domain":
                key = domain or canonical_url or _title_key(title)
            elif unique_by == "title":
                key = _title_key(title) or canonical_url
            elif unique_by == "url_or_title":
                key = canonical_url or _title_key(title)
            else:
                key = canonical_url or _title_key(title)

            if not key:
                key = f"item_{len(unique_items)}"

            cleaned_item = dict(item)
            if canonical_url:
                cleaned_item["url"] = canonical_url
            if domain:
                cleaned_item.setdefault("source", domain)

            if key in seen:
                duplicate_groups.setdefault(key, []).append(cleaned_item)
                continue

            seen[key] = len(unique_items)
            unique_items.append(cleaned_item)
            if len(unique_items) >= max_items:
                break

        return {
            "tool": "dedupe_sources",
            "unique_by": unique_by,
            "unique_items": unique_items,
            "input_count": len(items),
            "unique_count": len(unique_items),
            "removed_count": max(0, len(items) - len(unique_items)),
            "duplicate_group_count": len(duplicate_groups),
            "duplicate_keys": list(duplicate_groups.keys())[:20],
        }
    except Exception as exc:
        return {
            "tool": "dedupe_sources",
            "error": type(exc).__name__,
            "message": str(exc),
        }
