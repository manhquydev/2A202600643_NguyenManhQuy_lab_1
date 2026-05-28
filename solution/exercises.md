# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature tăng từ 0.0 đến 1.5, phản hồi của mô hình trở nên đa dạng, sáng tạo và sinh động hơn về cả từ vựng lẫn cấu trúc câu. Ở mức temperature thấp (0.0 và 0.5), nội dung câu trả lời rất chi tiết, có cấu trúc chặt chẽ và tập trung vào các sự kiện lịch sử/khoa học chính xác (như kích thước hang, năm phát hiện 1991). Ở temperature cao (1.0 và 1.5), ngôn từ bắt đầu linh hoạt, mang tính bay bổng hơn, tuy nhiên cấu trúc bắt đầu lặp lại hoặc có khả năng phát sinh sai lệch thông tin nếu tăng quá cao.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Tôi sẽ đặt temperature từ **0.0 đến 0.2** (ví dụ: 0.1). Chatbot hỗ trợ khách hàng yêu cầu độ chính xác, nhất quán và tin cậy cực kỳ cao đối với các chính sách và tài liệu nghiệp vụ của công ty; việc đặt temperature thấp giúp hạn chế mô hình tự ý sáng tạo thông tin ("ảo tưởng") và đảm bảo phản hồi luôn rõ ràng, chuẩn xác.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> GPT-4o đắt hơn GPT-4o-mini đúng **16.67 lần** (với đơn giá output token lần lượt là 0.010 USD và 0.0006 USD mỗi 1K token). Với workload này (10.000 users * 3 lần gọi * 350 tokens = 10,5 triệu tokens/ngày), chi phí hàng ngày của GPT-4o sẽ là **105.00 USD/ngày** trong khi GPT-4o-mini chỉ tiêu tốn **6.30 USD/ngày**.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> - **GPT-4o xứng đáng:** Khi thực hiện các tác vụ đòi hỏi khả năng suy luận logic chuyên sâu, lập trình code phức tạp, phân tích dữ liệu nghiên cứu lớn hoặc xử lý ngôn ngữ chuyên ngành (như trợ lý chẩn đoán y khoa, trợ lý pháp lý phân tích hợp đồng).
> - **GPT-4o-mini tốt hơn:** Khi cần vận hành chatbot trả lời FAQ thông thường, phân loại email, tóm tắt nội dung văn bản ngắn, hoặc trích xuất thông tin có cấu trúc đơn giản với lượng người dùng đồng thời cực kỳ lớn và yêu cầu độ trễ thấp.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất trong các ứng dụng đối thoại tương tác trực tiếp với người dùng cuối (như chatbot, trợ lý ảo, công cụ viết lách) nhằm giảm thiểu thời gian chờ phản hồi đầu tiên (Time to First Token), đem lại cảm giác mượt mà và trực quan. Ngược lại, non-streaming phù hợp hơn trong các hệ thống backend chạy ngầm xử lý hàng loạt (batch processing), phân tích cảm xúc (sentiment analysis) số lượng lớn, trích xuất dữ liệu có cấu trúc qua API, hoặc các tác vụ mà kết quả cuối cùng cần được hoàn thiện và kiểm tra trước khi chuyển đến hệ thống khác.


## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/ -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `retry_with_backoff` đã triển khai và kiểm thử
- [x] `batch_compare` đã triển khai và kiểm thử
- [x] `format_comparison_table` đã triển khai và kiểm thử
- [x] `exercises.md` đã điền đầy đủ
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
