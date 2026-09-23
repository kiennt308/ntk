# QUẢN TRỊ BÀI BÁO THUỘC DIỆN TRẢ PHÍ & CHIẾN LƯỢC KHAI THÁC BẢN MỞ (PAYWALLED PAPERS MANAGEMENT & OPEN RETRIEVAL)
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH

Thư mục `08_unavailable/` theo dõi các bài báo khoa học giá trị cao thuộc diện bảo hộ bản quyền trả phí (Paywalled - Elsevier ScienceDirect, Springer Nature, IEEE Xplore, Taylor & Francis) và cung cấp các quy trình khai thác bản toàn văn mở hợp pháp phục vụ nghiên cứu phi thương mại.

---

## 🏛️ 1. Ba Kênh Khai Thác Bản Toàn Văn Hợp Pháp (Legal Full-Text Retrieval)

```
┌────────────────────────────────────────────────────────────────────────┐
│   KÊNH 1: KHO BẢN THẢO TÁC GIẢ TỰ LƯU TRỮ (GREEN OPEN ACCESS)         │
│   • arXiv.org (Computer Science / Signal Processing)                  │
│   • bioRxiv.org / medRxiv.org (Neuroscience / Biomedical Engineering)  │
│   • HAL Open Science (hal.science) & Europe PMC                        │
│   • Semantic Scholar Open Access Corpus / Unpaywall API               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│   KÊNH 2: CỔNG THƯ VIỆN ĐẠI HỌC QUỐC GIA / VIỆN HÀN LÂM (SHIBBOLETH)  │
│   • Sử dụng tài khoản chứng thực trường đại học qua VPN / Proxy       │
│   • Đăng nhập IEEE Xplore, ScienceDirect qua Shibboleth Institutional │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│   KÊNH 3: LIÊN HỆ TRỰC TIẾP TÁC GIẢ CHÍNH (CORRESPONDING AUTHOR)      │
│   • Gửi email học thuật lịch sự đề nghị xin Author's Copy             │
│   • Yêu cầu trực tiếp qua cổng mạng nghiên cứu ResearchGate           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📈 2. Thống Kê Hiện Trạng Toàn Văn Trong Kho Nghiên Cứu
- **Tổng số bài báo khoa học đã lập chỉ mục**: **375 bài (10 Cụm) + 30 bài (Core)**
- **Số bài đã có file PDF toàn văn tải về máy offline**: **240 file PDF** (Tỷ lệ tải thành công đạt 64.0%).
- **Đối với 135 bài còn lại chưa có PDF tự động**:
  - Hệ thống đã lưu trữ toàn diện: **Abstract đầy đủ, Danh sách Tác giả, Năm, Tạp chí, Số trích dẫn, DOI gốc và Ghi chú phân tích phương pháp** trong thư mục [`paper_notes/`](../open_access_repository/) của từng cụm.
  - Người nghiên cứu có thể tra cứu nhanh tóm tắt và bấm trực tiếp vào liên kết DOI gốc để tải bản toàn văn qua cổng thư viện trường.
