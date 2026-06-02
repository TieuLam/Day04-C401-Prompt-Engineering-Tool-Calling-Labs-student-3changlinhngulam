---
name: source_quality
track: bonus
kind: local_knowledge
provider: local
requires_env: []
inputs: [url, claim_type]
outputs: [domain, source_type, quality_score, warnings, recommendation]
side_effect: false
---

# source_quality

Heuristically scores a source from its URL/domain so the agent can prioritize stronger references.

## When to use

Use this after `lookup`, `social_search`, or `fetch` when the agent needs to choose which links are better for a report or digest.

## Scoring

- 5: official, government, academic, or recognized institutional source
- 4: strong news or organization source
- 3: general commercial/media source
- 2: social, forum, blog, or weak source
- 1: invalid, shortened, or risky source

## Limitations

This tool is not a fact-checker. It only uses URL/domain heuristics and should not replace reading the source content.
