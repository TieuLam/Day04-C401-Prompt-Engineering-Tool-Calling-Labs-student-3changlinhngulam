from tools import TOOL_FUNCTIONS

for name in ["url_cleaner", "source_quality", "extract_entities", "dedupe_sources"]:
    assert name in TOOL_FUNCTIONS, f"{name} is not registered in TOOL_FUNCTIONS"

print(TOOL_FUNCTIONS["url_cleaner"]("https://example.com/a?id=1&utm_source=x&fbclid=abc"))
print(TOOL_FUNCTIONS["source_quality"]("https://www.who.int/news-room"))
print(TOOL_FUNCTIONS["extract_entities"]("VinUni announced it on 28/05/2026. Contact ai@vinuni.edu.vn"))
print(TOOL_FUNCTIONS["dedupe_sources"]([
    {"title": "AI news", "url": "https://example.com/a?utm_source=x"},
    {"title": "AI news", "url": "https://example.com/a"}
]))
