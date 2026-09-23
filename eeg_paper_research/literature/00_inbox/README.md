# HỘP THƯ TIẾP NHẬN TÀI LIỆU MỚI (LITERATURE INBOX & SCREENING PIPELINE)
## ĐỀ TÀI TIẾN SĨ: NHẬN DIỆN CẢM XÚC ĐA PHƯƠNG THỨC TỪ TÍN HIỆU Y SINH

Thư mục `00_inbox/` đóng vai trò là trạm tiếp nhận trung chuyển (Staging & Ingestion Gateway) cho tất cả các tài liệu, bản thảo bài báo khoa học (Preprints/PDFs), tệp trích dẫn (`.bib`, `.ris`, `.enw`) hoặc danh sách DOI mới được phát hiện trong quá trình nghiên cứu.

---

## 📋 1. Tiêu Chuẩn Tiếp Nhận & Sàng Lọc (Eligibility Criteria - PRISMA 2020)

Mọi bài báo mới đưa vào `00_inbox/` phải trải qua 4 bước sàng lọc chất lượng:

### A. Tiêu chí Đưa vào (Inclusion Criteria)
1. **Đối tượng nghiên cứu**: Nhận diện cảm xúc (Valence, Arousal, Dominance hoặc Discrete Categories), trạng thái căng thẳng (Stress), hoặc tải lượng nhận thức (Cognitive Load).
2. **Phương thức tín hiệu**: Có sử dụng tín hiệu **EEG** (Thần kinh trung ương) kết hợp với ít nhất một tín hiệu sinh lý tự chủ (**ECG, EDA/GSR, PPG, Respiration, EMG**) hoặc theo dõi chuyển động mắt (**Eye-tracking**).
3. **Mô hình học máy / Học sâu**: Sử dụng các phương pháp hiện đại: Học đa nhiệm vụ (Multi-Task), Kiến trúc đa nhánh (Multi-Branch), Cơ chế chú ý chéo (Cross-Modal Attention), Mạng nơ-ron đồ thị (GNN), Transformer, Tách biểu diễn (Disentanglement), hoặc Học tự giám sát (SSL).
4. **Năm công bố**: Ưu tiên bài báo công bố từ **2023 đến 2026** (đón đầu các đột phá mới nhất).

### B. Tiêu chí Loại trừ (Exclusion Criteria)
1. Các nghiên cứu chỉ nhận diện cảm xúc từ hình ảnh khuôn mặt RGB thuần túy hoặc giọng nói âm học mà không có tín hiệu sinh lý y sinh.
2. Các bài báo ngắn dưới 4 trang, tóm tắt hội thảo (Extended Abstract) thiếu chi tiết kỹ thuật và giao thức thực nghiệm.
3. Các nghiên cứu có nguy cơ rò rỉ dữ liệu nghiêm trọng (ví dụ: trộn lẫn cửa sổ trượt giữa tập Train và Test).

---

## ⚙️ 2. Quy Trình Xử Lý Tự Động Hóa (Ingestion Workflow)

```
[File PDF / DOI thả vào 00_inbox/]
             │
             ▼
[Bước 1: Trích xuất Metadata (Tiêu đề, Tác giả, Năm, Tạp chí, Abstract, DOI)]
             │
             ▼
[Bước 2: Kiểm tra Trùng lặp (Đối chiếu với 07_duplicates/ & open_access_repository/)]
             │
             ├── Trùng lặp ──> [Hủy bỏ / Lưu log vào 07_duplicates/]
             └── Hợp lệ
                  │
                  ▼
[Bước 3: Phân loại vào 1 trong 10 Cụm Từ Khóa (kw01 -> kw10)]
                  │
                  ▼
[Bước 4: Tạo Paper Note chuẩn hóa (.md) & Di chuyển PDF vào thư mục pdfs/]
```

---

## 📂 3. Hướng Dẫn Thao Tác Thủ Công Cho Nghiên Cứu Sinh
- Khi tải một file PDF bài báo mới về máy, đặt tên theo cú pháp: `YYYY_Author_ShortTitle.pdf` (Ví dụ: `2026_Smith_MultimodalEEG.pdf`).
- Thả file vào `literature/00_inbox/`.
- Phân loại và chuyển file vào cụm tương ứng trong [`literature/open_access_repository/`](../open_access_repository/).
