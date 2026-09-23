# 📘 CẨM NANG HƯỚNG DẪN KHAI THÁC TOÀN DIỆN GOOGLE NOTEBOOKLM
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH ĐA PHƯƠNG THỨC

Tài liệu này hướng dẫn chi tiết quy trình chuẩn hóa từ A-Z cách tạo, tải tài liệu và khai thác sức mạnh AI của **Google NotebookLM** với kho dữ liệu 375 bài báo khoa học và 240 file PDF toàn văn phục vụ luận án Tiến sĩ.

---

## 🗺️ 1. Bản Đồ 10 Notebooks Chuẩn Hóa Theo Cấu Trúc Luận Án

| STT | Mã Notebook & Tên Thư Mục | Tên Tiếng Việt | Số Bài | Số PDF | Phục Vụ Viết Chương Luận Án |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **01** | [`notebook_01_Multimodal_EEG_Biosignals`](./notebook_01_Multimodal_EEG_Biosignals) | **Nền tảng Tín hiệu Não (EEG) & Sinh lý Tự chủ (ECG, EDA, PPG)** | 50 | **50 PDF** | Chương 2 (Tổng quan) & Chương 4 (Dữ liệu) |
| **02** | [`notebook_02_Multi_Task_Learning_Affect`](./notebook_02_Multi_Task_Learning_Affect) | **Học Đa Nhiệm Vụ trong Tính toán Cảm xúc** | 43 | **38 PDF** | Chương 3 (Kiến trúc đề xuất) & Chương 6 (Thực nghiệm Đa nhiệm) |
| **03** | [`notebook_03_Multi_Branch_Cross_Modal_Attention`](./notebook_03_Multi_Branch_Cross_Modal_Attention) | **Kiến trúc Đa nhánh & Chú ý Chéo (Cross-Attention)** | 46 | **22 PDF** | Chương 3 (Mã hóa đa nhánh) & Chương 5 (Ablation Attention) |
| **04** | [`notebook_04_Subspace_Disentanglement_Domain_Adaptation`](./notebook_04_Subspace_Disentanglement_Domain_Adaptation) | **Tách Không gian con (Disentanglement) & Thích ứng Miền** | 47 | **28 PDF** | Chương 3 (Tách biểu diễn) & Chương 5 (Tổng quát hóa LOSO) |
| **05** | [`notebook_05_Missing_Modality_Wearable_Robustness`](./notebook_05_Missing_Modality_Wearable_Robustness) | **Bền vững Khuyết thiếu Cảm biến & Thiết bị Đeo** | 50 | **28 PDF** | Chương 5 (Thực nghiệm Bền vững & Rớt cảm biến) |
| **06** | [`notebook_06_Foundation_Models_Self_Supervised_Biosignals`](./notebook_06_Foundation_Models_Self_Supervised_Biosignals) | **Mô hình Nền tảng (Foundation Models) & Học Tự Giám Sát** | 50 | **29 PDF** | Chương 2 (Xu hướng công nghệ) & Chương 7 (Mở rộng) |
| **07** | [`notebook_07_Graph_Neural_Networks_Brain_Connectivity`](./notebook_07_Graph_Neural_Networks_Brain_Connectivity) | **Mạng Nơ-ron Đồ thị (GNN) & Liên kết Chức năng Vỏ não** | 50 | **22 PDF** | Chương 2, 4 & 5 (Các mô hình đối sánh SOTA) |
| **08** | [`notebook_08_Transformers_Crossmodal_Affective_Computing`](./notebook_08_Transformers_Crossmodal_Affective_Computing) | **Kiến trúc Transformer Đa phương thức** | 18 | **13 PDF** | Chương 2 & Chương 3 (Đối sánh Transformer MulT) |
| **09** | [`notebook_09_Explainable_AI_Interpretable_Biosignals`](./notebook_09_Explainable_AI_Interpretable_Biosignals) | **Trí tuệ Nhân tạo Giải thích được (XAI) & Bản đồ Não** | 12 | **6 PDF** | Chương 5 & Chương 7 (Minh bạch hóa & Ý nghĩa Sinh học) |
| **10** | [`notebook_10_Closed_Loop_BCI_RealTime_Affective_Systems`](./notebook_10_Closed_Loop_BCI_RealTime_Affective_Systems) | **BCI Vòng lặp Khép kín, Tính toán Biên Thời gian thực** | 9 | **4 PDF** | Chương 7 (Ứng dụng thực tiễn & Thiết bị đeo BCI) |
| **TỔNG**| **10 Notebooks Độc Lập** | **Toàn diện 10 Trụ Cột Đề Tài** | **375** | **240 PDF** | **Phủ toàn bộ 7 Chương Luận Án Tiến Sĩ** |

---

## ⚡ 2. Quy Trình Khởi Tạo & Khai Thác Chuẩn (3 Bước Đơn Giản)

### 📌 Bước 1: Khởi tạo Notebook trên Google
1. Mở trình duyệt và truy cập: **[https://notebooklm.google.com/](https://notebooklm.google.com/)**
2. Đăng nhập bằng tài khoản Google.
3. Bấm **"New Notebook"** và đặt tên chuẩn (Ví dụ: `NB01 - Multimodal EEG Biosignals`).

### 📌 Bước 2: Tải các file PDF lên NotebookLM
1. Trên máy tính của bạn, mở thư mục tương ứng:
   `eeg_paper_research/notebooklm_workspace/notebook_01_Multimodal_EEG_Biosignals/pdfs/`
2. Chọn toàn bộ file PDF trong thư mục và kéo thả (Drag & Drop) vào cửa sổ NotebookLM.
3. *(Khuyến nghị)*: Tải thêm file `00_NOTEBOOKLM_PROMPTS_AND_INDEX.md` làm tài liệu định hướng tổng hợp.

### 📌 Bước 3: Đặt câu hỏi bằng Bộ 6 Prompts Master Class
Trong từng Notebook, mở file `00_NOTEBOOKLM_PROMPTS_AND_INDEX.md` và sao chép lần lượt 6 prompt chuẩn để NotebookLM tự động tổng hợp:

1. **Prompt 1 (Đột phá công nghệ)**: Bóc tách xu hướng mới nhất 2023–2026.
2. **Prompt 2 (Chi tiết toán học & kiến trúc)**: Bóc tách hàm mất mát, công thức Cross-Attention, Disentanglement.
3. **Prompt 3 (Kiểm toán dữ liệu & chống rò rỉ)**: Kiểm tra các giao thức Train/Val/Test, LOSO, chống rò rỉ cửa sổ trượt.
4. **Prompt 4 (Ma trận so sánh & Research Gaps)**: Lập bảng so sánh độ chính xác và chỉ ra khoảng trống học thuật.
5. **Prompt 5 (Đề xuất giải pháp cho luận án)**: Định hình đóng góp mới cho các chương 3, 5, 6 của đề tài.
6. **Prompt 6 (Trích dẫn học thuật)**: Trích xuất toàn văn danh mục tài liệu tham khảo chuẩn IEEE/APA.
