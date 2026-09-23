# 📑 BỘ PROMPT GOOGLE NOTEBOOKLM PHÂN TÍCH CHUYÊN SÂU TỪNG BÀI BÁO (PER-PAPER ANALYSIS SUITE)
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH
*(Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals)*

Tài liệu này cung cấp hệ thống prompt chuẩn mực được thiết kế riêng cho **Google NotebookLM**, cho phép nghiên cứu sinh bóc tách và phân tích toàn diện **từng bài báo khoa học đơn lẻ** theo 20 tiêu chí khoa học nghiêm ngặt quy định trong [`NotebookLM.md`](../NotebookLM.md).

---

## 🎯 1. NGUYÊN TẮC BẮT BUỘC KHI TRÍCH XUẤT (EVIDENTIARY RULES)

Khi gửi prompt vào NotebookLM, hệ thống AI bắt buộc phải tuân thủ 4 nhãn bằng chứng:
- **`[EXPLICIT]`**: Tác giả nêu trực tiếp trong bài báo (kèm số trang / mục / bảng).
- **`[SUPPORTED]`**: Được hỗ trợ mạnh mẽ bởi kết quả thực nghiệm báo cáo.
- **`[INFERRED]`**: Suy luận logic hợp lý nhưng không ghi trực diện.
- **`[UNKNOWN]`**: Không thể xác định từ tài liệu (Tuyệt đối không tự suy đoán hoặc bịa đặt).

> [!IMPORTANT]
> **Quy Tắc Chuỗi Giá Trị Bắt Buộc:**
> Tuyệt đối không viết: *"Bài báo chứng minh phương pháp X là tốt nhất."*  
> Bắt buộc phải viết theo chuỗi:  
> $$\text{METHOD} \longrightarrow \text{DATASET} \longrightarrow \text{PROTOCOL} \longrightarrow \text{METRIC} \longrightarrow \text{RESULT}$$  
> *(Ví dụ: "Tác giả đề xuất mô hình MMB-EmotionNet trên tập dữ liệu DEAP theo giao thức Leave-One-Subject-Out (LOSO) đạt độ chính xác Valence 85.2% và F1-score 84.6%").*

---

## 🚀 2. BỘ PROMPTS CHUYÊN DỤNG PHÂN TÍCH TỪNG BÀI BÁO (5 GÓI THEMATIC BUNDLES)

Khi phân tích một bài báo cụ thể trong NotebookLM, bạn hãy thay thế `[TÊN BÀI BÁO HOẶC MÃ BÀI BÁO]` bằng tiêu đề hoặc mã bài báo tương ứng (Ví dụ: `OA_KW1_001` hoặc `LGGNet`).

---

### 📦 GÓI 1: ĐỊNH DANH, DỮ LIỆU & TIỀN XỬ LÝ (Identity, Dataset & Preprocessing)
*(Bao gồm Task 1, Task 2, Task 3)*

```markdown
Bạn là trợ lý phân tích tài liệu khoa học cho đề tài Tiến sĩ: "Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức".

Hãy phân tích bài báo sau: [TÊN BÀI BÁO HOẶC MÃ BÀI BÁO]. 
Chỉ sử dụng thông tin có trong tài liệu nguồn. Phân định rõ [EXPLICIT], [SUPPORTED], [INFERRED], [UNKNOWN].

Trích xuất chi tiết 3 nội dung sau:

1. ĐỊNH DANH BÀI BÁO (Paper Identity):
   - Tiêu đề chính xác (Title)
   - Danh sách tác giả & Năm xuất bản
   - Tạp chí / Hội thảo (Venue) & DOI
   - Vấn đề nghiên cứu cốt lõi (Research Problem)
   - Mục tiêu chính & Đóng góp khoa học tự tuyên bố (Claimed Contributions)

2. ĐẶC TẢ BỘ DỮ LIỆU (Dataset Specification):
   - Tên bộ dữ liệu (DEAP, SEED, DREAMER, AMIGOS, hoặc Custom)
   - Số lượng đối tượng tham gia & Nhân khẩu học (Tuổi, giới tính)
   - Các phương thức tín hiệu thu thập (EEG, ECG, EDA/GSR, PPG, EMG, Respiration, Eye-tracking)
   - Số lượng kênh đo và tần số lấy mẫu (Sampling Rate) của từng tín hiệu
   - Phương pháp kích thích cảm xúc (Audio-visual, Video clips, Âm nhạc)
   - Không gian nhãn (Valence, Arousal, Dominance / Rời rạc) & Thang đo (1-9, 1-5)
   - Thời lượng mỗi trial, Độ dài cửa sổ trượt (Window length) và Độ gối (Overlap)

3. QUY TRÌNH TIỀN XỬ LÝ (Preprocessing Protocol):
   - Phương pháp lọc dải tần (Bandpass filtering), Lọc notch 50/60 Hz
   - Kỹ thuật khử nhiễu (ICA, EOG/EMG artifact removal, Baseline correction, CAR/REST)
   - Kỹ thuật chuẩn hóa (Z-score, Min-Max, Per-subject vs Global)
   - Trích xuất đặc trưng (DE, PSD, CWT, HRV, Tonic/Phasic EDA)
   - QUAN TRỌNG: Xác định việc tiền xử lý/chuẩn hóa được thực hiện TRƯỚC hay SAU khi chia tập Train/Test?
```

---

### 📦 GÓI 2: KIẾN TRÚC MÔ HÌNH, DUNG HỢP ĐA PHƯƠNG THỨC & HỌC ĐA NHIỆM (Architecture, Fusion & MTL)
*(Bao gồm Task 5, Task 6, Task 7, Task 8)*

```markdown
Hãy phân tích sâu về Kiến trúc Kỹ thuật của bài báo: [TÊN BÀI BÁO HOẶC MÃ BÀI BÁO].
Chỉ căn cứ vào bài báo, không tự suy diễn cấu trúc không được mô tả.

Trích xuất 4 thành phần sau:

1. KIẾN TRÚC MẠNG TỔNG THỂ (End-to-End Architecture):
   - Sơ đồ dòng chảy dữ liệu: Input → Preprocessing → Feature Encoder → Shared/Private Latent Space → Fusion → Task Heads → Output
   - Các khối mạng học sâu được sử dụng (CNN 1D/2D, GCN/GAT, Transformer, BiLSTM, TCN, Conformer)
   - Kích thước chiều ẩn (Hidden dimensions) và cơ chế kích hoạt (Activation functions)

2. CẤU TRÚC ĐA NHÁNH (Multi-Branch Design):
   - Số lượng nhánh mạng nơ-ron độc lập
   - Đầu vào và bộ mã hóa của từng nhánh (Ví dụ: Nhánh EEG xử lý thế nào, nhánh ECG/EDA xử lý thế nào?)
   - Lý do tác giả thiết kế đa nhánh (Có dựa trên đặc thù vật lý tín hiệu hay không?)

3. CƠ CHẾ DUNG HỢP ĐA PHƯƠNG THỨC (Multimodal Fusion Mechanism):
   - Phân loại: Early Fusion, Intermediate Fusion, Late Fusion, hay Cross-Modal Attention?
   - Vị trí thực hiện dung hợp và các vector biểu diễn tham gia dung hợp
   - Có cơ chế Cross-Attention Query-Key-Value giữa EEG và tín hiệu sinh lý ngoại vi không?
   - Mô hình có học trọng số thích nghi (Modality Importance Weights) cho từng cảm biến không?

4. HỌC ĐA NHIỆM VỤ (Multi-Task Learning Formulation):
   - Mô hình là Single-Task hay Multi-Task?
   - Các nhiệm vụ đồng thời là gì (Ví dụ: Dự đoán đồng thời Valence và Arousal, hoặc Cảm xúc + Subject ID)?
   - Các tầng nào chia sẻ tham số (Shared layers) và tầng nào riêng biệt (Task-specific heads)?
   - Công thức hàm mất mát tổng quát (L_total = λ1 L_task1 + λ2 L_task2 + ...)?
   - Trọng số nhiệm vụ λ là cố định (Fixed) hay tự học động (Learned / Kendall Uncertainty / GradNorm)?
```

---

### 📦 GÓI 3: KIỂM TOÁN RÒ RỈ DỮ LIỆU & GIAO THỨC CHIA TẬP (Data Leakage Audit & Validation Protocol)
*(Bao gồm Task 4, Task 17)*

```markdown
Hãy thực hiện KIỂM TOÁN RÒ RỈ DỮ LIỆU NGHIÊM NGẶT (Data Leakage Audit) đối với bài báo: [TÊN BÀI BÁO HOẶC MÃ BÀI BÁO].

Phân tích chi tiết 2 nội dung:

1. GIAO THỨC CHIA TẬP DỮ LIỆU (Data Partitioning):
   - Đánh giá phụ thuộc đối tượng (Subject-Dependent) hay độc lập đối tượng (Subject-Independent)?
   - Giao thức cụ thể: Random K-Fold, Subject-wise K-Fold, Leave-One-Subject-Out (LOSO), hay Cross-Session?
   - Tỷ lệ phân chia Train / Validation / Test chính xác là bao nhiêu?
   - Các cửa sổ trượt (Sliding windows) của cùng một đối tượng/trial có thể xuất hiện đồng thời ở cả tập Train và Test không?

2. BẢNG KIỂM TOÁN 8 CHIỀU RÒ RỈ DỮ LIỆU (8-Dimensional Leakage Matrix):
   Lập bảng đánh giá với các cột: [Loại Rò Rỉ | Bằng Chứng Trong Bài | Mức Độ Rủi Ro (Cao/TB/Thấp/Không) | Độ Tin Cậy [EXPLICIT/INFERRED]]
   - Subject Leakage (Rò rỉ danh tính đối tượng)
   - Trial Leakage (Rò rỉ giữa các thử nghiệm cùng kích thích)
   - Windowing Leakage (Rò rỉ do xáo trộn sliding windows trước khi chia tập)
   - Normalization Leakage (Rò rỉ chuẩn hóa Z-score/Min-Max toàn cục trước khi split)
   - Feature Extraction Leakage (Rò rỉ lọc thời gian LDS/Moving Average qua ranh giới train/test)
   - Augmentation Leakage (Rò rỉ dữ liệu tăng cường sinh ra từ tập test)
   - Hyperparameter Leakage (Tinh chỉnh tham số trực tiếp trên tập test)
   - Cross-Dataset / Montage Shift (Trộn lẫn cấu hình điện cực không chuẩn hóa)
```

---

### 📦 GÓI 4: KẾT QUẢ THỰC NGHIỆM, ABLATION, TỔNG QUÁT HÓA & TÍNH TOÁN BIÊN
*(Bao gồm Task 9, Task 10, Task 11, Task 12, Task 13, Task 14)*

```markdown
Hãy trích xuất KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG & ĐỘ BỀN VỮNG của bài báo: [TÊN BÀI BÁO HOẶC MÃ BÀI BÁO].

Trích xuất 6 nội dung:

1. MA TRẬN ĐỐI SÁNH BASELINES:
   Lập bảng so sánh các mô hình đối sánh trong bài: [Tên Baseline | Phương thức (Unimodal/Multimodal) | Kiến trúc | Giao thức Đánh giá | Kết quả so sánh]

2. KẾT QUẢ CHÍNH XÁC ĐÃ CÔNG BỐ (Exact Reported Metrics):
   - Độ chính xác (Accuracy, Balanced Accuracy)
   - Macro-F1 / Weighted-F1, Precision, Recall, ROC-AUC
   - MAE, RMSE, Pearson correlation r (nếu là hồi quy liên tục)
   - Giá trị trung bình ± độ lệch chuẩn (Mean ± Std), Khoảng tin cậy, Kiểm định ý nghĩa thống kê (p-value, Wilcoxon, ANOVA, t-test)

3. THỰC NGHIỆM TRIỆT TIÊU (Ablation Study):
   - Thành phần bị loại bỏ/thay đổi:
   - Kết quả mô hình đầy đủ (Full Model) vs Kết quả mô hình bị cắt giảm (Ablated):
   - Mức độ chênh lệch (Δ Performance):
   - Ý nghĩa thực nghiệm chứng minh vai trò của thành phần đó.

4. KHẢ NĂNG TỔNG QUÁT HÓA (Generalization):
   - Kết quả đánh giá Cross-Subject (LOSO), Cross-Session, hoặc Cross-Dataset (nếu có).

5. ĐỘ BỀN VỮNG & KHUYẾT THIẾU CẢM BIẾN (Robustness & Missing Modalities):
   - Bài báo có thử nghiệm khi mất 1 hoặc nhiều cảm biến (Missing Modality) không?
   - Bài báo có kiểm tra độ bền vững trước nhiễu (Noise / Motion artifacts) không? Nếu không, ghi rõ "Not evaluated".

6. CHI PHÍ TÍNH TOÁN & KHẢ THI TRÊN THIẾT BI ĐEO (Computational Cost & Edge Feasibility):
   - Số lượng tham số (Parameter count), FLOPs, Kích thước file mô hình (Model Size MB)
   - Thời gian huấn luyện (Training time) và Độ trễ suy luận (Inference Latency ms)
   - Phần cứng thực nghiệm (GPU/CPU/Embedded Device). Nếu không báo cáo, ghi rõ "Not reported".
```

---

### 📦 GÓI 5: TỔNG HỢP 18 ĐIỂM, BẢNG BẰNG CHỨNG KHOA HỌC & ÁNH XẠ ĐỀ TÀI TIẾN SĨ
*(Bao gồm Task 15, Task 16, Task 18, Task 19, Task 20)*

```markdown
Hãy thực hiện TỔNG HỢP TOÀN DIỆN & ĐÁNH GIÁ ĐÓNG GÓP CHO LUẬN ÁN TIẾN SĨ từ bài báo: [TÊN BÀI BÁO HOẶC MÃ BÀI BÁO].

Trích xuất 4 nội dung:

1. BẢNG BẰNG CHỨNG KHOA HỌC (Scientific Evidence Table):
   Lập bảng gồm các cột: [Tuyên Bố Khoa Học (Claim) | Bằng Chứng Cụ Thể Trong Bài | Vị Trí Nguồn (Mục/Bảng/Hình/Trang) | Loại Bằng Chứng [EXPLICIT / SUPPORTED / INFERRED]]

2. HẠN CHẾ & KHẢ NĂNG TÁI LẬP (Limitations & Reproducibility):
   - Hạn chế do chính tác giả thừa nhận (Stated Limitations)
   - Hạn chế quan sát thấy từ phương pháp luận (Observed Methodological Limitations)
   - Đánh giá khả năng tái lập (Reproducibility: HIGH / MEDIUM / LOW / UNKNOWN) dựa trên: Mã nguồn công khai, Dữ liệu mở, Siêu tham số chi tiết.

3. TỔNG KẾT 18 ĐIỂM CHUẨN MỰC (18-Point Paper Synthesis):
   Tóm tắt bài báo theo đúng 18 mục:
   1. Vấn đề | 2. Dữ liệu | 3. Phương thức | 4. Tiền xử lý | 5. Biểu diễn đặc trưng | 6. Kiến trúc | 7. Cơ chế dung hợp | 8. Học đa nhiệm | 9. Giao thức đánh giá | 10. Baselines | 11. Kết quả chính | 12. Ablation | 13. Tổng quát hóa | 14. Bền vững khuyết thiếu | 15. Chi phí tính toán | 16. Hạn chế | 17. Khả năng tái lập | 18. Chất lượng bằng chứng.

4. ĐÁNH GIÁ MỨC ĐỘ LIÊN QUAN ĐẾN ĐỀ TÀI TIẾN SĨ (Relevance to PhD Thesis):
   Chấm điểm (HIGH / MEDIUM / LOW) kèm giải thích ngắn gọn cho 7 chiều:
   - Multimodal Biosignals (EEG + ECG/EDA): [HIGH/MEDIUM/LOW] - Lý do: ...
   - Multi-Task Learning (Valence + Arousal + Dominance): [HIGH/MEDIUM/LOW] - Lý do: ...
   - Multi-Branch Architecture (Physics-informed encoders): [HIGH/MEDIUM/LOW] - Lý do: ...
   - Multimodal Fusion (Cross-Modal QKV Attention): [HIGH/MEDIUM/LOW] - Lý do: ...
   - Cross-Subject Generalization (LOSO / Disentanglement): [HIGH/MEDIUM/LOW] - Lý do: ...
   - Missing Modality Robustness: [HIGH/MEDIUM/LOW] - Lý do: ...
   - Edge / Wearable Efficiency: [HIGH/MEDIUM/LOW] - Lý do: ...
```

---

## ⚡ 3. PROMPT TỔNG LỰC 1-CLICK (ALL-IN-ONE MASTER DEEP EXTRACTION PROMPT)

Nếu bạn muốn NotebookLM bóc tách toàn diện **tất cả 20 tiêu chí trong một lần gửi duy nhất**, hãy sử dụng prompt dưới đây:

```markdown
Bạn là trợ lý phân tích tài liệu khoa học cho đề tài Tiến sĩ: "Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức".

Hãy phân tích toàn diện bài báo: [TÊN BÀI BÁO HOẶC MÃ BÀI BÁO] dựa trên các nguồn tài liệu trong notebook này.
Tuân thủ nghiêm ngặt nguyên tắc: Chỉ dựa trên tài liệu nguồn, không bịa đặt, phân định rõ [EXPLICIT], [SUPPORTED], [INFERRED], [UNKNOWN], và luôn tuân thủ chuỗi METHOD → DATASET → PROTOCOL → METRIC → RESULT.

Hãy xuất báo cáo phân tích theo đúng cấu trúc chuẩn sau:

# BÁO CÁO PHÂN TÍCH CHUYÊN SÂU BÀI BÁO KHOA HỌC: [TÊN BÀI BÁO]

## 1. THÔNG TIN ĐỊNH DANH & BỐI CẢNH
- Tiêu đề, Tác giả, Năm, Tạp chí/Hội thảo, DOI.
- Vấn đề nghiên cứu & Đóng góp khoa học cốt lõi.

## 2. BỘ DỮ LIỆU & QUY TRÌNH TIỀN XỬ LÝ
- Bộ dữ liệu, Số đối tượng, Các kênh tín hiệu (EEG, ECG, EDA, PPG,...), Tần số lấy mẫu.
- Kích thích, Thang đo nhãn (Valence/Arousal/Dominance), Cửa sổ trượt (Window/Overlap).
- Phương pháp lọc, Khử nhiễu, Chuẩn hóa đặc trưng.

## 3. KIẾN TRÚC MÔ HÌNH & CƠ CHẾ KỸ THUẬT
- Luồng kiến trúc: Input → Encoders → Shared/Private Latent Space → Fusion → Task Heads → Output.
- Cấu trúc Đa nhánh (Multi-Branch): Thiết kế từng nhánh theo đặc tính vật lý tín hiệu.
- Cơ chế Dung hợp (Multimodal Fusion): Early / Late / Cross-Modal QKV Attention / Bilinear.
- Học Đa Nhiệm Vụ (Multi-Task Learning): Các nhiệm vụ liên hợp, Hàm mất mát & Cân bằng trọng số (Kendall/GradNorm).

## 4. KIỂM TOÁN GIAO THỨC & RÒ RỈ DỮ LIỆU (ANTI-LEAKAGE AUDIT)
- Giao thức chia tập: Subject-Dependent vs LOSO (Subject-Independent).
- Bảng kiểm toán rò rỉ: Rò rỉ cửa sổ trượt, Rò rỉ đối tượng, Rò rỉ chuẩn hóa toàn cục.

## 5. KẾT QUẢ THỰC NGHIỆM & MA TRẬN ĐỐI SÁNH
- Bảng so sánh với các Baselines.
- Kết quả định lượng chi tiết: Accuracy, F1-score, MAE, RMSE, Mean ± Std, p-value.
- Phân tích thực nghiệm triệt tiêu (Ablation Study): Vai trò của từng khối mạng.
- Đánh giá Tổng quát hóa (LOSO) & Độ bền vững khi khuyết thiếu cảm biến (Missing Modalities).
- Chi phí tính toán: Parameters, FLOPs, Độ trễ suy luận (Inference Latency), Phần cứng.

## 6. ĐÁNH GIÁ ĐÓNG GÓP & ÁNH XẠ VÀO LUẬN ÁN TIẾN SĨ
- Hạn chế của bài báo (Tác giả thừa nhận vs Phương pháp luận quan sát được).
- Khả năng tái lập (Reproducibility: High/Medium/Low).
- Bảng chấm điểm mức độ liên quan 7 chiều đến đề tài Tiến sĩ (Multimodal, MTL, Multi-Branch, Fusion, Disentanglement, Robustness, Efficiency).
```
