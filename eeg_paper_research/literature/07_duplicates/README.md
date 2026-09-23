# BÁO CÁO KIỂM TOÁN KHỬ TRÙNG LẶP DỮ LIỆU BÀI BÁO (PRISMA-2020 DEDUPLICATION AUDIT)
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH

Thư mục `07_duplicates/` lưu trữ báo cáo kiểm toán quy trình khử trùng lặp dữ liệu học thuật có hệ thống theo chuẩn quốc tế **PRISMA 2020 Statement** (Preferred Reporting Items for Systematic Reviews and Meta-Analyses).

---

## 🔄 1. Sơ Đồ Quy Trình Khử Trùng Lặp PRISMA 2020

```
┌────────────────────────────────────────────────────────────────────────┐
│             GIAI ĐOẠN 1: THU THẬP TỔNG THỂ (IDENTIFICATION)            │
│  Quét 10 Cụm Từ Khóa từ OpenAlex, arXiv, IEEE, PMC, Semantic Scholar  │
│                   Tổng số kết quả quét thô: 850+ bài                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             GIAI ĐOẠN 2: LỌC TRÙNG LẶP CẤP ĐỘ 1 (DOI MATCHING)         │
│     So khớp chính xác khóa định danh số DOI (Case-insensitive)         │
│                 Phát hiện & Hợp nhất: 98 bài trùng lặp                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             GIAI ĐOẠN 3: LỌC TRÙNG LẶP CẤP ĐỘ 2 (TITLE FUZZY MATCH)    │
│  Chuẩn hóa Title: Lowercase, bỏ ký tự đặc biệt, Levenshtein Sim > 0.95 │
│                 Phát hiện & Hợp nhất: 44 bài trùng lặp                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             GIAI ĐOẠN 4: BỘ DỮ LIỆU ĐỘC NHẤT CHUẨN HÓA (INCLUSION)     │
│   • 375 Bài Báo Open Access Độc Nhất (Phân bổ trong 10 Cụm kw01..kw10)  │
│   • 30 Bài Báo Nền Tảng Cốt Lõi (Giai đoạn 1: P0001..P0030)            │
│   • 240 File Toàn Văn PDF Đã Tải Về Máy Phục Vụ Đọc Offline & AI        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 2. Thuật Toán Xử Lý Bài Báo Giao Thoa Giữa Các Cụm (Canonical Assignment)
- Khi một bài báo thỏa mãn nhiều cụm từ khóa (Ví dụ: Một bài báo vừa dùng *Transformer* vừa nghiên cứu *Multimodal EEG-ECG*):
  - Bài báo được gán **Primary Canonical Key** tại cụm có mức độ đóng góp trọng tâm nhất.
  - Các cụm liên quan khác thiết lập liên kết **Cross-Reference Link** trỏ về bài báo chính, đảm bảo không lưu trữ trùng file PDF cục bộ gây lãng phí dung lượng đĩa.
