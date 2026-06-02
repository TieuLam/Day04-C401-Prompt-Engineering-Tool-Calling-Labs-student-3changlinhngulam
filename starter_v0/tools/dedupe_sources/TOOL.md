---
name: dedupe_sources
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [items, unique_by, max_items]
outputs: [unique_items, input_count, unique_count, removed_count, duplicate_group_count]
side_effect: false
---

# dedupe_sources

Removes duplicate source items from web/social/research results.

## When to use

Use this after `lookup`, `social_search`, or manually collected source lists when the agent has repeated URLs, repeated titles, or too many items from the same domain.

## Supported modes

- `url`: deduplicate by canonical URL
- `domain`: keep one item per domain
- `title`: deduplicate by normalized title
- `url_or_title`: use URL first, then title

## Example

Input:

```json
{
  "items": [
    {"title": "AI news", "url": "https://example.com/a?utm_source=x"},
    {"title": "AI news", "url": "https://example.com/a"}
  ],
  "unique_by": "url"
}
```

Output includes:

```json
{
  "unique_count": 1,
  "removed_count": 1
}
```
