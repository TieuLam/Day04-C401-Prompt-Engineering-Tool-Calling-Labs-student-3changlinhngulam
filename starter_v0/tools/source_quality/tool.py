from __future__ import annotations

from typing import Any
from urllib.parse import urlparse


SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "buff.ly",
    "cutt.ly",
    "rebrand.ly",
    "is.gd",
    "s.id",
}

SOCIAL_DOMAINS = {
    "twitter.com",
    "x.com",
    "facebook.com",
    "instagram.com",
    "tiktok.com",
    "youtube.com",
    "reddit.com",
    "linkedin.com",
}

FORUM_DOMAINS = {
    "quora.com",
    "stackoverflow.com",
    "stackexchange.com",
    "medium.com",
    "substack.com",
}

ACADEMIC_DOMAINS = {
    "arxiv.org",
    "doi.org",
    "semanticscholar.org",
    "pubmed.ncbi.nlm.nih.gov",
    "nature.com",
    "science.org",
    "pnas.org",
    "ieee.org",
    "acm.org",
    "springer.com",
    "sciencedirect.com",
}

ORG_DOMAINS = {
    "who.int",
    "un.org",
    "worldbank.org",
    "oecd.org",
    "europa.eu",
    "nasa.gov",
    "nih.gov",
    "cdc.gov",
    "openai.com",
}

NEWS_DOMAINS = {
    "reuters.com",
    "apnews.com",
    "bbc.com",
    "bbc.co.uk",
    "nytimes.com",
    "washingtonpost.com",
    "theguardian.com",
    "bloomberg.com",
    "ft.com",
    "techcrunch.com",
    "theverge.com",
}


def _domain(url: str) -> str:
    parsed = urlparse((url or "").strip())
    if not parsed.scheme and "." in parsed.path:
        parsed = urlparse("https://" + url.strip())
    return parsed.netloc.lower().replace("www.", "")


def _is_subdomain_or_same(domain: str, known: set[str]) -> bool:
    return any(domain == item or domain.endswith("." + item) for item in known)


def assess_source_quality(url: str = "", claim_type: str = "general") -> dict[str, Any]:
    """
    Heuristically assess source quality from URL/domain features.

    This is not a fact-checker. It helps the agent prioritize sources and flag weak links.
    """
    try:
        original_url = url or ""
        normalized_url = original_url.strip()
        if normalized_url and not urlparse(normalized_url).scheme and "." in normalized_url:
            normalized_url = "https://" + normalized_url

        parsed = urlparse(normalized_url)
        domain = _domain(normalized_url)

        warnings: list[str] = []
        source_type = "unknown"
        score = 2

        if not domain:
            warnings.append("Missing or invalid domain.")
            score = 1
        elif _is_subdomain_or_same(domain, SHORTENERS):
            source_type = "short_link"
            score = 1
            warnings.append("Shortened URLs hide the final source; expand or fetch before trusting.")
        elif domain.endswith(".gov") or domain.endswith(".mil") or _is_subdomain_or_same(domain, ORG_DOMAINS):
            source_type = "official_or_organization"
            score = 5
        elif domain.endswith(".edu") or _is_subdomain_or_same(domain, ACADEMIC_DOMAINS):
            source_type = "academic"
            score = 5
        elif _is_subdomain_or_same(domain, NEWS_DOMAINS):
            source_type = "news"
            score = 4
        elif _is_subdomain_or_same(domain, SOCIAL_DOMAINS):
            source_type = "social_media"
            score = 2
            warnings.append("Social media is useful for primary posts, but weak for verified factual claims.")
        elif _is_subdomain_or_same(domain, FORUM_DOMAINS):
            source_type = "forum_or_blog"
            score = 2
            warnings.append("Forum/blog content should be cross-checked with stronger sources.")
        elif domain.endswith(".org"):
            source_type = "organization"
            score = 4
        elif domain.endswith(".com") or domain.endswith(".net"):
            source_type = "commercial_or_media"
            score = 3

        if parsed.scheme != "https" and domain:
            warnings.append("URL does not use HTTPS.")
            score = max(1, score - 1)

        claim = (claim_type or "general").lower()
        if claim in {"medical", "legal", "financial", "safety"} and score < 5:
            warnings.append(f"For {claim} claims, prefer official, academic, or primary sources.")

        if score >= 5:
            recommendation = "Strong source candidate. Still verify the exact claim and date."
        elif score == 4:
            recommendation = "Good supporting source. Cross-check if the topic is sensitive or fast-changing."
        elif score == 3:
            recommendation = "Usable background source, but not ideal as the only citation."
        else:
            recommendation = "Weak source for factual claims. Use mainly for context or primary social posts."

        return {
            "tool": "assess_source_quality",
            "url": original_url,
            "domain": domain,
            "source_type": source_type,
            "quality_score": score,
            "claim_type": claim_type,
            "warnings": warnings,
            "recommendation": recommendation,
        }
    except Exception as exc:
        return {
            "tool": "assess_source_quality",
            "url": url,
            "error": type(exc).__name__,
            "message": str(exc),
        }
