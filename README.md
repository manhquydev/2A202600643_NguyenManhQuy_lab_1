# Ngày 1 — Nền Tảng LLM API

## Mục Tiêu

Học cách gọi OpenAI API, hiểu các tham số sinh text quan trọng, so sánh GPT-4o và GPT-4o-mini, xây dựng chatbot streaming có lịch sử hội thoại.

---

## Cài Đặt

### Yêu Cầu
- Python 3.10+
- OpenAI API key

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
```

---

## Cấu Trúc Project

```
day1/
├── solution/
│   ├── solution.py        # Triển khai chính (Tasks 1–4 + Bonus A–C)
│   └── exercises.md       # Bài tập phân tích đã hoàn thành
├── ui/
│   └── terminal.py        # Rich TUI components (console, panels, tables, spinner)
├── tests/
│   └── test_solution.py   # Pytest test suite (mock-based)
├── chatbot_rich.py         # Chatbot terminal dùng Rich TUI
├── web_app.py              # Chatbot web dùng Gradio
├── template.py             # Template gốc
└── requirements.txt
```

---

## Các Nhiệm Vụ Đã Hoàn Thành

### Task 1 — `call_openai`
Gọi OpenAI Chat Completions API với GPT-4o, trả về `(response_text, latency_seconds)`.

- Hỗ trợ các tham số: `model`, `temperature`, `top_p`, `max_tokens`
- Đo latency chính xác, đảm bảo latency > 0

### Task 2 — `call_openai_mini`
Gọi GPT-4o-mini bằng cách tái sử dụng `call_openai(model=OPENAI_MINI_MODEL)`.

### Task 3 — `compare_models`
Gọi cả GPT-4o và GPT-4o-mini với cùng prompt, trả về dict so sánh:

| Key | Mô tả |
|-----|-------|
| `gpt4o_response` | Phản hồi GPT-4o |
| `mini_response` | Phản hồi GPT-4o-mini |
| `gpt4o_latency` | Thời gian phản hồi GPT-4o (giây) |
| `mini_latency` | Thời gian phản hồi GPT-4o-mini (giây) |
| `gpt4o_cost_estimate` | Chi phí ước tính USD cho GPT-4o |

Chi phí ước tính: GPT-4o $0.010/1K tokens, GPT-4o-mini $0.0006/1K tokens (~16.7× rẻ hơn).

### Task 4 — `streaming_chatbot`
Chatbot terminal tương tác với streaming tokens và lịch sử 3 lượt hội thoại gần nhất.

---

## Bonus Tasks Đã Hoàn Thành

### Bonus A — `retry_with_backoff`
Gọi lại hàm tối đa `max_retries` lần với exponential backoff (`base_delay × 2^attempt`) khi gặp lỗi.

### Bonus B — `batch_compare`
Chạy `compare_models` trên danh sách nhiều prompts, trả về list kết quả kèm key `"prompt"`.

### Bonus C — `format_comparison_table`
Định dạng kết quả batch thành bảng text, tự căn chỉnh cột, cắt ngắn text dài hơn 40 ký tự.

---

## Giao Diện Mở Rộng

### Rich TUI (`chatbot_rich.py`)
Chatbot terminal được nâng cấp bằng thư viện [Rich](https://github.com/Textualize/rich):
- Panels màu sắc cho tin nhắn user/assistant
- Spinner animation trong khi chờ phản hồi
- Bảng so sánh model được định dạng đẹp

```bash
python chatbot_rich.py
```

### Gradio Web UI (`web_app.py`)
Ứng dụng web với 2 tabs:

| Tab | Tính năng |
|-----|-----------|
| 💬 Chat | Chat streaming, chọn model, điều chỉnh temperature & max_tokens |
| 🔬 So Sánh Models | So sánh GPT-4o vs GPT-4o-mini, batch comparison nhiều prompts |

```bash
python web_app.py
# Mở trình duyệt: http://localhost:7860
```

---

## Chạy Kiểm Thử

```bash
pytest tests/ -v
```

Tất cả tests dùng `unittest.mock` — **không cần API key thật**.

---

## Chấm Điểm

| Tiêu Chí | Điểm |
|----------|------|
| Tất cả pytest tests pass | 50 |
| `compare_models` trả về cấu trúc dict đúng | 10 |
| `streaming_chatbot` duy trì lịch sử hội thoại | 10 |
| Exercise 2.1 — Phân tích temperature | 10 |
| Exercise 2.2 — Phân tích chi phí | 10 |
| Exercise 2.3 — Streaming UX | 10 |
| **Tổng** | **100** |

---

## Danh Sách Kiểm Tra Nộp Bài

- [x] `pytest tests/ -v` — tất cả kiểm thử pass
- [x] `solution/exercises.md` — tất cả câu trả lời đã điền
- [x] `solution/solution.py` — triển khai cuối cùng
- [x] Bonus A: `retry_with_backoff` đã triển khai
- [x] Bonus B: `batch_compare` đã triển khai
- [x] Bonus C: `format_comparison_table` đã triển khai
- [x] Rich TUI chatbot (`chatbot_rich.py`)
- [x] Gradio Web UI (`web_app.py`)
