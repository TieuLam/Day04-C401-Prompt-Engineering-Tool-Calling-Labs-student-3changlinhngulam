# Kế hoạch triển khai & Phân công công việc (Team 3 người) - Day 04 Lab v2

Dựa trên yêu cầu của `README.md`, dự án yêu cầu hoàn thành nhiệm vụ bắt buộc và có mục tiêu đạt **điểm thưởng (Bonus Point)** (làm cả UI và tự viết >3 tools mới). Tổng thời gian: **4 tiếng**.

## 1. Phân công vai trò (Roles)

**Thành viên 1 (M1) - Prompt & Evaluation Lead**
*Trách nhiệm chính:* Đảm bảo vòng lặp tối ưu Agent hoạt động đúng theo chuẩn evidence-driven (dựa trên logs).
- Chạy Baseline, phân tích JSON logs.
- Chỉnh sửa `artifacts/system_prompt.md` và `artifacts/tools.yaml` (v1, v2, v3).
- Cập nhật liên tục `artifacts/version_log.csv`.
- Chạy Live Chat và trích xuất transcripts.

**Thành viên 2 (M2) - Tooling & Logic Engineer**
*Trách nhiệm chính:* Phát triển các công cụ (tools) mới để đảm bảo chức năng và lấy trọn điểm Bonus.
- Viết ít nhất 3-4 tools mới (gồm mã nguồn `tool.py`, tài liệu `TOOL.md` và đăng ký trong `__init__.py`).
- Hiện thực hóa các logic khó như Bonus Tool `send` (có confirmation).
- Tích hợp Bonus tools (`policy`, `papers`, `paper_text`).
- Phối hợp với M1 để map chính xác tên tool vào `tools.yaml`.

**Thành viên 3 (M3) - UI, Data & Documentation**
*Trách nhiệm chính:* Phát triển giao diện người dùng, cung cấp test cases và viết báo cáo cuối cùng.
- Phát triển giao diện web (Streamlit hoặc Vercel) để ăn điểm Bonus.
- Tự viết 10 Eval cases vào `data/eval_group.json` (5 single turn, 5 multi turn).
- Viết và tổng hợp `artifacts/REPORT.md` dựa trên metrics và logs thực tế do M1 cung cấp.

---

## 2. Kế hoạch triển khai chi tiết theo Timeline (4 Giờ)

### Phase 1: Setup & Preflight (0:00 - 0:25)
- **Cả team:** Clone repo, cài đặt venv, `pip install -r requirements.txt`. Lấy các API Keys cần thiết điền vào `.env`.
- **M1:** Chạy `scripts/preflight_provider.py` để đảm bảo API hoạt động.
- **M2:** Đọc file `TOOL-SETUP.md` và hiểu cấu trúc thư mục tool mới (`tools/<tool_name>/`).
- **M3:** Lên khung project Streamlit (hoặc Next.js/Vercel) cơ bản (Hello World) và đọc cấu trúc file `data/eval_group.json`.

### Phase 2: Chạy Baseline & Phân tích (0:25 - 0:55)
- **M1:** Chạy lệnh eval baseline (`version v0`). Parse file logs ra CSV bằng script có sẵn. Phân tích file JSON để xem agent sai ở đâu (sai tool, sai args...).
- **M2:** Bắt đầu code tool mới đầu tiên (Ví dụ: `send` hoặc `policy`). Khởi tạo thư mục, `TOOL.md`, và viết hàm thực thi.
- **M3:** Tập trung viết 5 cases (single turn) đầu tiên vào `eval_group.json`, bàn bạc nhanh với M1 về các lỗi hệ thống để viết case "gài" agent.

### Phase 3: Tối ưu Prompt & Tool - Lần 1 & 2 (0:55 - 1:45)
- **M1:** Sửa `system_prompt.md` và `tools.yaml` dựa trên lỗi Baseline -> Chạy eval v1, v2 -> Ghi file `version_log.csv`. 
- **M2:** Đẩy nhanh tiến độ code để hoàn thành tổng cộng **>3 tools mới** (Ví dụ: `policy`, `papers`, `paper_text` hoặc các custom tools sáng tạo khác). Đảm bảo đăng ký xong ở `__init__.py`.
- **M3:** Code UI Streamlit. Giao diện cần có khung chat, và có thể hiển thị kết quả tool-call (tham khảo repo starter). Hoàn thành 5 cases (multi turn) còn lại vào `eval_group.json`.

### Phase 4: Chạy Eval Group & Cập nhật Tools (1:45 - 2:15)
- **M1 + M2:** M2 bàn giao tên các tool mới cho M1 để cập nhật vào `tools.yaml`. M1 rà soát lại không làm gãy tên tool trong eval_base.
- **M3:** Nộp file `eval_group.json` (10 cases hoàn chỉnh). Chạy thử Streamlit UI xem kết nối được agent base hay chưa.
- **M1:** Sửa lỗi hệ thống từ lần test trước, chuẩn bị bản prompt hoàn thiện nhất cho v3.

### Phase 5: Run v3 + Group Eval (2:15 - 2:45)
- **M1:** Chạy lệnh eval cho v3 trên toàn bộ `eval_base.json` và `eval_group.json`. Ghi log số liệu v3 vào `version_log.csv`.
- **M2:** Testing các Bonus tools trên môi trường cục bộ để đảm bảo không bị crash khi agent gọi tới. Hỗ trợ M3 gắn agent vào UI.
- **M3:** Chuẩn bị sườn Report. Bắt đầu phân tích số liệu từ `v0` đến `v3` do M1 xuất ra để viết dàn ý.

### Phase 6: Live Chat & Lấy Transcript (2:45 - 3:20)
- **Cả team:** Cùng chạy `chat.py` (hoặc test trực tiếp trên UI Streamlit của M3).
- Phân chia test các kịch bản:
  - 1 request research thông thường.
  - 1 request thiếu thông tin xem agent có hỏi lại không (`clarify` tool).
  - 1 request đòi gửi tin nhắn lên Telegram để test confirmation (`send` tool).
- **M1:** Thu thập các file JSON transcript sau khi chat live thành công.

### Phase 7: Viết Báo Cáo (Report) (3:20 - 3:50)
- **M3:** Viết chính nội dung vào `artifacts/REPORT.md`. Đưa ra bằng chứng (evidence-driven) từ file run JSON: sai lầm ban đầu là gì, giả thuyết là gì, kết quả sau khi sửa prompt/tool ra sao.
- **M1:** Trợ giúp M3 điền các thông số metric chính xác, check lại `version_log.csv` xem đã đủ log v0 -> v3 chưa.
- **M2:** Viết đoạn tài liệu giới thiệu về các tools mới tự làm, nộp `TOOL.md` của từng tool đầy đủ. Rà soát UI/Code lần cuối.

### Phase 8: Đóng gói và Kiểm tra (3:50 - 4:00)
- **Cả team cùng Review:**
  - Check file `tools.yaml` và `__init__.py` (Có đồng bộ tên tool không?).
  - Check `eval_base.json` có vô tình bị sửa không (BẮT BUỘC KHÔNG ĐƯỢC SỬA).
  - Check lại đủ 10 cases trong `eval_group.json`.
  - Check `version_log.csv` (Đủ các cột `prompt_hash`, `tools_hash`, `metric_after`, ...).
  - Đảm bảo **XÓA/ẨN** file `.env` (Tuyệt đối không commit API keys).
- **M1:** Gom toàn bộ thư mục `starter_v0/`, nén lại và Nộp bài theo chuẩn.

---

## 3. Quy tắc làm việc chung (Git & Sync)
- Mọi thành viên **push code liên tục** (ít nhất sau mỗi task xong).
- **Cấm tự ý đổi tên các tool có sẵn** trong các file test, nếu đổi để dễ nhận diện thì chỉ đổi qua `tools.yaml` và `__init__.py` và phải bảo cho M1 biết để sửa.
- Nếu API Key (OpenRouter/Tavily) hết hạn ngạch (rate limit), thông báo ngay để share key khác.
- Report phải **bám sát vào log thật** trong thư mục `runs/`, tuyệt đối không chém gió cảm tính.
