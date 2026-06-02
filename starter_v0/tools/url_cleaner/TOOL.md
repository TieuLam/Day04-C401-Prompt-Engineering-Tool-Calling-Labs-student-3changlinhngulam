---
name: url_cleaner
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [url, keep_params, remove_params, remove_fragment]
outputs: [clean_url, domain, removed_params, removed_count]
side_effect: false
---

# url_cleaner

Cleans URLs before citation or reporting by removing common tracking parameters such as `utm_*`, `fbclid`, `gclid`, `mc_cid`, and similar fields.

## When to use

Use this tool when the agent has a URL that may contain tracking parameters and needs a cleaner link for `fetch`, `format`, or final citation.

## Example

Input:

```json
{
  "url": "https://example.com/article?id=123&utm_source=facebook&fbclid=abc"
}
```

Output includes:

```json
{
  "clean_url": "https://example.com/article?id=123",
  "removed_params": ["utm_source", "fbclid"]
}
```

## Notes

This tool does not access the internet and does not verify whether the URL exists.
