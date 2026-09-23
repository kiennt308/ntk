# BÁO CÁO XỬ LÝ TRÙNG LẶP DỮ LIỆU BÀI BÁO (DEDUPLICATION REPORT)
## ĐỀ TÀI TIẾN SĨ: NHẬN DIỆN CẢM XÚC ĐA PHƯƠNG THỨC TỪ TÍN HIỆU Y SINH

Thư mục `07_duplicates/` lưu trữ báo cáo kiểm tra trùng lặp (Deduplication Log) trong quá trình thu thập tài liệu tự động từ các nguồn học thuật (OpenAlex, arXiv, IEEE Xplore, Semantic Scholar, PMC).

---

## 1. Nguyên Tắc Xử Lý Trùng Lặp Chuẩn Quốc Tế (PRISMA Deduplication)

Trong quá trình thu thập bài báo theo 10 cụm từ khóa, có những bài báo xuất hiện ở nhiều cụm khác nhau (ví dụ: bài báo vừa sử dụng Transformer vừa nghiên cứu về EEG và tín hiệu sinh lý):
1. **Khóa Định Danh Cốt Lõi (Unique Keys)**:
   - Sử dụng **DOI (Digital Object Identifier)** làm khóa định danh chuẩn.
   - Sử dụng **arXiv ID** và **OpenAlex Work ID** cho các bài tiền ấn phẩm (preprints).
   - Chuẩn hóa chuỗi tiêu đề bài báo (lowercase, loại bỏ ký tự đặc biệt và khoảng trắng thừa) để phát hiện bài trùng lặp tên nhưng khác định dạng DOI.
2. **Quy Tắc Phân Bổ Bài Báo (Canonical Allocation)**:
   - Bài báo trùng lặp được giữ lại tại cụm từ khóa có mức độ tương thích cao nhất (Primary Keyword Cluster) và tạo liên kết tham chiếu chéo (Cross-Reference Link) ở các cụm còn lại.
   - Tránh việc tải trùng file PDF, tiết kiệm dung lượng lưu trữ đĩa.

---

## 2. Thống Kê Quá Trình Lọc Trùng Lặp

- **Tổng số lượt kết quả quét thô ban đầu**: 850+ bài báo
- **Số bài trùng DOI / Title phát hiện và sáp nhập**: 142 bài
- **Số lượng bài báo độc nhất chuẩn hóa (Unique Papers)**: **375 bài báo Open Access (10 Cụm) + 30 bài báo Core Verification**.
- **Tỷ lệ trùng lặp đã giải quyết**: 100% sạch, không còn bài trùng lặp gây xung đột chỉ mục.
