# HỆ THỐNG SCRIPTS TỰ ĐỘNG HÓA NGHIÊN CỨU (`scripts/`)
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH

Thư mục `scripts/` chứa toàn bộ các công cụ, mã nguồn Python phục vụ tự động hóa việc thu thập, lọc dữ liệu, tải file PDF, trích xuất metadata và đồng bộ hóa không gian làm việc Google NotebookLM.

---

## 🛠️ Danh Mục & Chức Năng Các Scripts

### 1. Thu Thập & Tải Bài Báo Khoa Học (Data Ingestion & PDF Download)
- `fetch_open_access_papers.py` / `oa_paper_fetcher.py`: Truy vấn OpenAlex API và Semantic Scholar để thu thập danh mục bài báo Open Access theo từ khóa.
- `download_all_oa_pdfs.py` / `downloader.py`: Tải tự động các file PDF toàn văn từ Unpaywall, PMC, arXiv, HAL.
- `resolve_and_download_extra_pdfs.py`: Quét lại và tải bổ sung các file PDF còn thiếu qua các nguồn thứ cấp.
- `expand_and_download_literature.py` / `expand_to_10_clusters.py`: Mở rộng cơ sở dữ liệu từ 5 cụm lên 10 cụm nghiên cứu Tiến sĩ toàn diện.

### 2. Xử Lý & Sinh Ghi Chú Phân Tích (Processing & Paper Notes Generation)
- `build_literature_system.py`: Khởi tạo hệ thống thư mục và tài liệu cốt lõi ban đầu.
- `generate_notes_and_index.py` / `generate_notes_batch2.py` / `generate_notes_batch3.py`: Sinh các file tóm tắt chi tiết (`paper_notes/*.md`) theo mẫu chuẩn IEEE.
- `process_batch1.py` / `process_batch2.py` / `process_batch3.py`: Tiền xử lý dữ liệu và trích xuất bảng chỉ mục CSV.
- `select_batch1.py` / `select_batch2.py` / `select_batch3.py`: Lọc và chọn bài báo chất lượng cao theo tiêu chí PRISMA.
- `filter_and_packager.py`: Đóng gói và kiểm tra tính toàn vẹn của các file PDF tải về.

### 3. Đồng Bộ Hóa & Chuẩn Hóa Không Gian Làm Việc (Workspace Standardization)
- `standardize_notebook_workspace.py`: Chuẩn hóa 10 thư mục Google NotebookLM, tạo `notebook_metadata.json` và `README.md`.
- `update_notebooklm_workspace.py`: Cập nhật liên kết tài liệu và danh mục prompt cho từng Notebook.
- `update_open_access_readmes.py`: Cập nhật bảng chỉ mục và link đọc PDF trong kho tài liệu mở 10 cụm.
- `optimize_structure.py`: Chuẩn hóa định dạng tên thư mục 2 chữ số (`kw01..kw10`, `notebook_01..notebook_10`) và xóa tàn dư trùng lặp.
- `populate_02_classified.py` / `populate_04_reviews.py` / `populate_all_literature_folders.py`: Bổ sung nội dung và cấu trúc cho các thư mục chuyên đề.
- `update_dataset_index.py`: Đồng bộ danh mục các bộ dữ liệu Benchmark (DEAP, SEED, DREAMER, AMIGOS, WESAD).
