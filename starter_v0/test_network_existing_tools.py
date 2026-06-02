from pathlib import Path
from env_loader import load_lab_env

load_lab_env(Path(__file__).resolve().parent)

from tools import TOOL_FUNCTIONS


def run_tool(name, args):
    print(f"\n=== Testing {name} ===")
    try:
        result = TOOL_FUNCTIONS[name](**args)
        print(result)
    except Exception as exc:
        print(f"ERROR in {name}: {type(exc).__name__}: {exc}")


def main():
    run_tool("lookup", {
        "query": "OpenAI news",
        "topic": "news",
        "timeframe": "week",
        "max_results": 2,
    })

    run_tool("fetch", {
        "url": "https://example.com",
    })

    run_tool("papers", {
        "query": "retrieval augmented generation",
        "max_results": 1,
        "sort_by": "relevance",
    })

    run_tool("paper_text", {
        "arxiv_url": "https://arxiv.org/abs/1706.03762",
        "max_pages": 1,
        "max_chars": 2000,
    })

    run_tool("social_search", {
        "query": "AI",
        "search_type": "Latest",
        "limit": 2,
    })

    run_tool("timeline", {
        "screenname": "OpenAI",
        "limit": 2,
    })


if __name__ == "__main__":
    main()