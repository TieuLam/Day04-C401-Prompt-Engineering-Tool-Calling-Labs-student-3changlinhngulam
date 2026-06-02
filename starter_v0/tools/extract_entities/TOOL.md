---
name: extract_entities
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [text, max_items]
outputs: [urls, emails, dates, money, hashtags, mentions, possible_organizations, counts]
side_effect: false
---

# extract_entities

Extracts useful entities from text using local regex rules.

## When to use

Use this after `fetch`, `paper_text`, `policy`, or user-provided text when the agent needs to pull out URLs, emails, dates, money values, hashtags, mentions, or possible organization names.

## Example

Input:

```json
{
  "text": "VinUni announced the AI program on 28/05/2026. Contact ai@vinuni.edu.vn."
}
```

Output includes:

```json
{
  "emails": ["ai@vinuni.edu.vn"],
  "dates": ["28/05/2026"],
  "possible_organizations": ["VinUni"]
}
```

## Limitations

Entity extraction is heuristic and may miss or over-detect names. It is best used as a helper, not a final reasoning source.
