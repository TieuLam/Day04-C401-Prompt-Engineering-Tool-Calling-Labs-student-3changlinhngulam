from tools import TOOL_FUNCTIONS


def run_tool(name, args):
    print(f"\n=== Testing {name} ===")
    try:
        result = TOOL_FUNCTIONS[name](**args)
        print(result)
    except Exception as exc:
        print(f"ERROR in {name}: {type(exc).__name__}: {exc}")


def main():
    # Tool local, không gọi internet
    run_tool("clarify", {
        "question": "Bạn muốn tìm thông tin về chủ đề nào?",
        "response_type": "text",
        "options": [],
    })

    # Tool format local, an toàn
    run_tool("format", {
        "items": [
            {
                "title": "Sample source",
                "url": "https://example.com",
                "source": "example.com",
                "summary": "This is a test item.",
                "section": "Test",
            }
        ],
        "template": "brief",
        "headline": "Test Digest",
    })

    # Tool policy thường là local search trong tài liệu nội bộ
    run_tool("policy", {
        "query": "citation",
        "policy_area": "all",
        "top_k": 2,
    })

    # send chỉ test confirmed=False để tránh gửi thật
    run_tool("send", {
        "text": "Test message only. Do not send.",
        "confirmed": False,
    })


if __name__ == "__main__":
    main()