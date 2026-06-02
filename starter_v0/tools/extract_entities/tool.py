from __future__ import annotations

import re
from typing import Any


URL_RE = re.compile(r"https?://[^\s<>)\]]+", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
DATE_RE = re.compile(
    r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4})\b",
    re.IGNORECASE,
)
MONEY_RE = re.compile(
    r"(?:[$€£¥₫]\s?\d[\d,]*(?:\.\d+)?|\d[\d,]*(?:\.\d+)?\s?(?:USD|EUR|GBP|VND|JPY|đ|dong|dollars))",
    re.IGNORECASE,
)
HASHTAG_RE = re.compile(r"(?<!\w)#[A-Za-z0-9_À-ỹ]+")
MENTION_RE = re.compile(r"(?<!\w)@[A-Za-z0-9_]{2,30}")
ORG_RE = re.compile(
    r"\b(?:[A-ZÀ-Ỵ][A-Za-zÀ-ỹ0-9&.-]+(?:\s+|$)){2,5}"
)


def _unique(items: list[str], max_items: int) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        cleaned = item.strip().strip(".,;:!?)]}")
        if cleaned and cleaned.lower() not in seen:
            seen.add(cleaned.lower())
            result.append(cleaned)
        if len(result) >= max_items:
            break
    return result


def _extract_possible_orgs(text: str, max_items: int) -> list[str]:
    matches = []
    for match in ORG_RE.findall(text or ""):
        candidate = " ".join(match.split())
        words = candidate.split()
        if len(words) < 2:
            continue
        if candidate.lower().startswith(("the ", "this ", "that ")):
            continue
        if len(candidate) <= 4:
            continue
        matches.append(candidate)
    return _unique(matches, max_items)


def extract_entities(text: str = "", max_items: int = 20) -> dict[str, Any]:
    """
    Extract common entities from text using local regex heuristics.
    """
    try:
        text = text or ""
        max_items = max(1, min(int(max_items or 20), 100))

        urls = _unique(URL_RE.findall(text), max_items)
        emails = _unique(EMAIL_RE.findall(text), max_items)
        dates = _unique(DATE_RE.findall(text), max_items)
        money = _unique(MONEY_RE.findall(text), max_items)
        hashtags = _unique(HASHTAG_RE.findall(text), max_items)
        mentions = _unique(
            [m for m in MENTION_RE.findall(text) if m.lower() not in {email.split("@")[0].lower() for email in emails}],
            max_items,
        )
        possible_organizations = _extract_possible_orgs(text, max_items)

        return {
            "tool": "extract_entities",
            "urls": urls,
            "emails": emails,
            "dates": dates,
            "money": money,
            "hashtags": hashtags,
            "mentions": mentions,
            "possible_organizations": possible_organizations,
            "counts": {
                "urls": len(urls),
                "emails": len(emails),
                "dates": len(dates),
                "money": len(money),
                "hashtags": len(hashtags),
                "mentions": len(mentions),
                "possible_organizations": len(possible_organizations),
            },
        }
    except Exception as exc:
        return {
            "tool": "extract_entities",
            "error": type(exc).__name__,
            "message": str(exc),
        }
