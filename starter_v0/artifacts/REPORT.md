# Day 04 Lab v2 Report — Research Agent

## Team

- Team: 3changlinhngulam
- Members: M1, M2, M3
- Provider/model: OpenAI / vuduongcalvin/gemini-3.5-flash

## Final Metrics

- Final version: v3
- Final artifact_version: v3+pbc98a1208746+t0fc84af93111
- Best base run file: `runs/v3_B_base_openai_20260602T163011590283.json`
- Base case accuracy: 1.0 (100%)
- Base tool routing accuracy: 1.0 (100%)
- Base argument accuracy: 1.0 (100%)
- Group eval run file: `runs/v3_B_group_openai_20260602T164705391436.json`
- Group eval accuracy: 0.875 (87.5%)
- Chat transcript file: `transcripts/` (Sẽ cập nhật ở Phase 6)

## Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu | - | 0.60 | `runs/v0_B_base_...json` |
| v1 | system_prompt.md, tools.yaml | Cấm đoán sai tool, ép rule query news | 0.60 | 1.00 | `runs/v1_B_base_...json` |
| v2 | system_prompt.md | Cấm send email | 0.80 | 1.00 | `runs/v2_B_group_...json` |
| v3 | system_prompt.md, tools.yaml, __init__.py | Thêm bonus tools và rules cho multi-turn | 0.80 | 1.00 (Base) | `runs/v3_B_base_...json` |

## Failure Analysis

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| G04_source_quality_shortlink | wrong_tool | `fetch` | Gọi nhầm fetch thay vì source_quality do link rút gọn (bit.ly) | Thêm logic hướng dẫn prompt cụ thể khi nhận diện shortlink thì phải dùng source_quality. |
| R02_search_tweets_routing (v0) | wrong_tool | `get_user_tweets` | Dùng sai hàm khi tìm tweet theo chủ đề | Cập nhật mô tả tool rõ ràng trong tools.yaml. |
| R03_web_news_routing (v0) | wrong_tool | `web_search` | Tìm tin tức nhưng gọi nhầm tool general | Đổi mô tả và hướng dẫn định tuyến trong prompt. |

## Team Eval Cases

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_url_cleaner_tracking_params | Xử lý params URL | `url_cleaner` | Passed |
| G02_url_cleaner_plain_domain | Chạy tool với domain thuần | `url_cleaner` | Passed |
| G03_source_quality_medical | Đánh giá độ tin cậy nguồn y tế | `source_quality` | Passed |
| G04_source_quality_shortlink | Xử lý link rút gọn | `source_quality` | Failed (wrong_tool) |
| G05_extract_entities_text | Trích xuất thông tin cơ bản | `extract_entities` | Passed |
| G06_extract_entities_max_items | Trích xuất có limit | `extract_entities` | Passed |
| G07_dedupe_sources_by_url | Lọc trùng theo url | `dedupe_sources` | Passed |
| G08_dedupe_sources_by_domain | Lọc trùng theo domain | `dedupe_sources` | Passed |

## Live Chat Evidence

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tìm tin tức AI hôm nay có gì hot? | `lookup`, `format` | Xử lý đa luồng thông tin và định dạng tốt | Lấy được 4 tin AI nổi bật và xuất format đẹp. |
| 2 | Có thông tin gì về account này trên X/Twitter không? | `clarify` | Nhận diện thiếu thông tin (account) | Agent hỏi lại user: "Bạn có thể cung cấp tên tài khoản..." |
| 3 | @vinuni_ai | `timeline` | Nhớ ngữ cảnh multi-turn để gọi tool | Tra cứu thành công (trả về trống do account không có bài). |
| 4 | Gửi kết quả vừa rồi thành 1 tin nhắn lên Telegram đi. | `clarify` | Cấm gửi tin nhắn tự động khi chưa confirm | Agent dừng lại hỏi: "Bạn có đồng ý gửi thông tin..." |
| 5 | Có | `send` | Xác nhận xong mới gọi tool send | Thực hiện gửi (hoặc mock gửi do thiếu Token). Đúng logic. |

## Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Bonus M2 Tools | `eval_group.json` | Thêm 4 tools xử lý URL thành công | Cần xử lý edge cases cho link rút gọn (như bit.ly). |
| UI | `ui/src/app/page.tsx` | Next.js Chat UI giao tiếp tốt với Python Agent | Đã xử lý kịch bản AI trả về chuỗi rỗng và bypass lỗi HMR WebSockets. |

## Reflection

- Which fixes belonged in `system_prompt.md`? Các quy tắc định tuyến phức tạp, hành vi từ chối, và hướng dẫn đa lượt (multi-turn).
- Which fixes belonged in `tools.yaml`? Mô tả ngắn gọn để model hiểu chức năng chính yếu của tool.
- Which failure needed manual review instead of automatic grading? Các đoạn chat fallback, hiện tượng agent im lặng, hoặc lỗi logic trên UI.
- What would you improve next? Tinh chỉnh lại logic xử lý shortlink cho `source_quality`, hoàn thiện chức năng ghi đè lịch sử (chat transcript) và thêm UI báo lỗi đẹp hơn.
