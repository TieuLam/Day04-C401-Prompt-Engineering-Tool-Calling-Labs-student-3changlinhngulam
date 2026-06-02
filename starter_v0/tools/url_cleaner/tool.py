from __future__ import annotations

from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


DEFAULT_TRACKING_PARAMS = {
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
    "vero_id",
    "trk",
    "spm",
    "ref",
    "ref_src",
}


def _looks_like_url(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


def _normalize_input_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if not parsed.scheme and "." in parsed.path:
        return "https://" + url
    return url


def _should_remove_param(name: str, remove_params: set[str]) -> bool:
    lower = name.lower()
    return (
        lower in remove_params
        or lower.startswith("utm_")
        or lower.startswith("ga_")
    )


def clean_url(
    url: str = "",
    keep_params: list[str] | None = None,
    remove_params: list[str] | None = None,
    remove_fragment: bool = True,
) -> dict[str, Any]:
    """
    Remove common tracking parameters from a URL while preserving useful query params.

    This is a local, deterministic helper for making fetched/cited links cleaner.
    """
    try:
        normalized_input = _normalize_input_url(url)
        if not normalized_input:
            return {
                "tool": "clean_url",
                "original_url": url,
                "clean_url": "",
                "is_valid": False,
                "domain": "",
                "removed_params": [],
                "message": "No URL provided.",
            }

        parsed = urlparse(normalized_input)
        if not _looks_like_url(normalized_input):
            return {
                "tool": "clean_url",
                "original_url": url,
                "clean_url": normalized_input,
                "is_valid": False,
                "domain": "",
                "removed_params": [],
                "message": "Invalid URL format.",
            }

        keep_set = {p.lower() for p in (keep_params or [])}
        remove_set = set(DEFAULT_TRACKING_PARAMS)
        remove_set.update(p.lower() for p in (remove_params or []))

        kept_pairs: list[tuple[str, str]] = []
        removed_params: list[str] = []

        for key, value in parse_qsl(parsed.query, keep_blank_values=True):
            if key.lower() in keep_set:
                kept_pairs.append((key, value))
            elif _should_remove_param(key, remove_set):
                removed_params.append(key)
            else:
                kept_pairs.append((key, value))

        clean_query = urlencode(kept_pairs, doseq=True)
        clean_fragment = "" if remove_fragment else parsed.fragment

        clean = urlunparse(
            (
                parsed.scheme.lower(),
                parsed.netloc.lower(),
                parsed.path,
                parsed.params,
                clean_query,
                clean_fragment,
            )
        )

        return {
            "tool": "clean_url",
            "original_url": url,
            "clean_url": clean,
            "is_valid": True,
            "domain": parsed.netloc.lower().replace("www.", ""),
            "removed_params": removed_params,
            "removed_count": len(removed_params),
            "fragment_removed": bool(parsed.fragment and remove_fragment),
        }
    except Exception as exc:
        return {
            "tool": "clean_url",
            "original_url": url,
            "error": type(exc).__name__,
            "message": str(exc),
        }
