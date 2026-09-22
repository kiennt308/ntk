# Notebook 09: Explainable AI (XAI) & Neurophysiological Model Interpretability
**Chủ đề Tiếng Việt**: Trí tuệ Nhân tạo Giải thích được (XAI), SHAP, Grad-CAM & Minh bạch Quyết định  
**Chương Luận án liên kết**: **Chương 5 & Chương 7 (Phân tích Trực quan hóa Bản đồ Não & Ý nghĩa Sinh học)**  
**Trọng tâm nghiên cứu**: SHAP feature attribution, Grad-CAM attention topographic mapping, Layer-wise Relevance Propagation (LRP), spatial-frequency band attribution (alpha/beta asymmetry), and clinical trust.  

---

## 1. Danh mục Toàn bộ Bài báo Khoa học trong Notebook này (12 bài)

| ID | Năm | Tiêu đề bài báo | Nơi công bố / Tạp chí | Trích dẫn | Tình trạng Tài liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW9_001` | **2023** | **Artificial Intelligence and Sensor Innovations: Enhancing Livestock Welfare with a Human-Centric Approach**<br>*Suresh Neethirajan* | Human-Centric Intelligent Systems | 134 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW9_002` | **2025** | **Artificial Intelligence and Neuroscience: Transformative Synergies in Brain Research and Clinical Applications**<br>*Răzvan Onciul, Cătălina-Ioana Tătar...* | Journal of Clinical Medicine | 108 | 🌐 Link bài báo Open Access |
| `OA_KW9_003` | **2024** | **Enhancing early Parkinson’s disease detection through multimodal deep learning and explainable AI: insights from the PPMI database**<br>*Vincenzo Dentamaro, Donato Impedovo...* | Scientific Reports | 107 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW9_004` | **2023** | **State-of-the-Art of Stress Prediction from Heart Rate Variability Using Artificial Intelligence**<br>*Yeaminul Haque, Rahat Shahriar Zawa...* | Cognitive Computation | 107 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW9_005` | **2024** | **Causal Inference Meets Deep Learning: A Comprehensive Survey**<br>*Licheng Jiao, Yuhan Wang, Xu Liu, L...* | Research | 103 | 🌐 Link bài báo Open Access |
| `OA_KW9_006` | **2023** | **MedMetaverse: Medical Care of Chronic Disease Patients and Managing Data Using Artificial Intelligence, Blockchain, and Wearable Devices State-of-the-Art Methodology**<br>*Dileep Kumar Murala, Sandeep Kumar ...* | IEEE Access | 100 | 🌐 Link bài báo Open Access |
| `OA_KW9_007` | **2023** | **Machine learning with multimodal neuroimaging data to classify stages of Alzheimer’s disease: a systematic review and meta-analysis**<br>*Modupe Odusami, Rytis Maskeliūnas, ...* | Cognitive Neurodynamics | 83 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW9_008` | **2025** | **Advances in Neuroimaging and Deep Learning for Emotion Detection: A Systematic Review of Cognitive Neuroscience and Algorithmic Innovations**<br>*Constantinos Halkiopoulos, Evgenia ...* | Diagnostics | 74 | 🌐 Link bài báo Open Access |
| `OA_KW9_009` | **2023** | **Application of Artificial Intelligence Techniques for Brain–Computer Interface in Mental Fatigue Detection: A Systematic Review (2011–2022)**<br>*Hamwira Yaacob, Farhad Hossain, Sha...* | IEEE Access | 65 | 🌐 Link bài báo Open Access |
| `OA_KW9_010` | **2024** | **SHAP value-based ERP analysis (SHERPA): Increasing the sensitivity of EEG signals with explainable AI methods**<br>*Sophia Sylvester, Merle Sagehorn, T...* | Behavior Research Methods | 60 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW9_011` | **2023** | **AI-Based Epileptic Seizure Detection and Prediction in Internet of Healthcare Things: A Systematic Review**<br>*Sobhana Jahan, Farhana Nowsheen, Ma...* | IEEE Access | 60 | 🌐 Link bài báo Open Access |
| `OA_KW9_012` | **2023** | **ADHD/CD-NET: automated EEG-based characterization of ADHD and CD using explainable deep neural network technique**<br>*Hui Wen Loh, Chui Ping Ooi, Shu Lih...* | Cognitive Neurodynamics | 37 | 📄 Có sẵn PDF trong thư mục |


---

## 2. Bộ Prompt Master Class (Google NotebookLM) Theo Chuẩn 20 Tiêu Chí

Dưới đây là 7 Prompts chuyên dụng được thiết kế riêng cho **Notebook 09: Explainable AI (XAI) & Neurophysiological Model Interpretability**. Bạn chỉ cần tải các bài báo/tài liệu trong thư mục này lên Google NotebookLM ([https://notebooklm.google.com/](https://notebooklm.google.com/)) và dán lần lượt các prompt bên dưới:

### 🔹 PROMPT 1: Trích xuất Bảng Nhận dạng & Đóng góp Khoa học
```text
Bạn là trợ lý phân tích tài liệu khoa học chuyên sâu cho đề tài Luận án Tiến sĩ "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".
Hãy phân tích TẤT CẢ các nguồn tài liệu trong notebook này và lập BẢNG TỔNG HỢP NHẬN DẠNG BÀI BÁO gồm các cột:
1. ID / Citation (Tác giả, Năm, Tạp chí/Hội nghị)
2. Bài toán nghiên cứu chính (Research Problem)
3. Phương thức tín hiệu sử dụng (EEG, ECG, EDA, v.v.)
4. Đóng góp khoa học then chốt (Key Claimed Contributions)
5. Loại bằng chứng: [EXPLICIT] / [SUPPORTED] / [INFERRED]

Yêu cầu: Tuyệt đối không suy diễn thông tin bị thiếu; nếu không có hãy ghi "Not reported".
```

### 🔹 PROMPT 2: Kiểm toán Rò rỉ Dữ liệu & Quy trình Phân chia (Data Leakage Audit)
```text
Hãy thực hiện KIỂM TOÁN RÒ RỈ DỮ LIỆU (Data Leakage Audit) trên tất cả các công trình nghiên cứu trong notebook này.
Đối với từng bài báo, hãy trả lời chính xác:
1. Quy trình phân chia dữ liệu là Subject-Dependent hay Subject-Independent (LOSO)?
2. Việc phân đoạn cửa sổ trượt (Sliding Window Segmentation) được thực hiện TRƯỚC hay SAU khi chia tập Train/Test?
3. Các tham số chuẩn hóa (Z-score mean, std) được tính trên toàn bộ dữ liệu hay chỉ trên tập Train?
4. Đánh giá Mức độ Rủi ro Rò rỉ (High Risk / Low Risk / Clean Leak-Free) kèm bằng chứng vị trí trong bài báo.
```

### 🔹 PROMPT 3: Bóc tách Kiến trúc Mô hình & Cơ chế Kết hợp (Architecture & Fusion)
```text
Tập trung vào khía cạnh KIẾN TRÚC MẠNG NƠ-RON VÀ KẾT HỢP ĐA PHƯƠNG THỨC trong các bài báo:
1. Phân loại cấu trúc: Mạng đơn khối (Monolithic), Đa nhánh (Multi-Branch), hay Đồ thị (Graph / Transformer)?
2. Cơ chế kết hợp thuộc loại nào: Early Fusion, Late Fusion, Intermediate Concat, hay Cross-Modal Attention?
3. Có cơ chế phân tách không gian con dùng chung - riêng biệt (Shared-Private Disentanglement) không? Nếu có, hàm mất mát ràng buộc là gì?
4. Trình bày chi tiết luồng xử lý tensor từ Đầu vào -> Trích xuất đặc trưng -> Kết hợp -> Đầu ra.
```

### 🔹 PROMPT 4: Phân tích Tối ưu Đa nhiệm vụ & Hàm Mất mát (Multi-Task Learning)
```text
Phân tích khía cạnh HỌC ĐA NHIỆM VỤ (Multi-Task Learning) trong các tài liệu:
1. Mô hình dự báo đồng thời các nhiệm vụ nào (Valence, Arousal, Dominance, Discrete Emotion)?
2. Hàm mất mát tổng thể được kết hợp như thế nào? (Ví dụ: L_total = λ1 L_v + λ2 L_a + λ3 L_c).
3. Các trọng số nhiệm vụ là CỐ ĐỊNH (Static Grid Search) hay TỰ HỌC THÍCH NGHI (Dynamic Uncertainty Weighting)?
4. Có hiện tượng chuyển giao tiêu cực (Negative Transfer) hoặc xung đột gradient giữa hồi quy và phân loại không?
```

### 🔹 PROMPT 5: Đánh giá Độ bền vững khi Mất Cảm biến & Khả năng Tổng quát hóa
```text
Phân tích ĐỘ BỀN VỮNG VÀ TỔNG QUÁT HÓA (Generalization & Robustness):
1. Hiệu năng mô hình thay đổi ra sao khi kiểm thử trên đối tượng hoàn toàn mới (Leave-One-Subject-Out)?
2. Có thực nghiệm stress-test khi khuyết thiếu một hoặc nhiều cảm biến (Missing Modality: Mất 100% EEG hoặc ECG/EDA) không?
3. Nếu có mất cảm biến, mô hình xử lý bằng cách nào (Zero-padding, Mean Imputation, hay Latent Cross-Modal Inpainting)?
4. Đo kiểm độ trễ tính toán thời gian thực (Inference Latency) trên phần cứng nào (GPU, Jetson, CPU)?
```

### 🔹 PROMPT 6: Tổng hợp Khoảng trống Nghiên cứu (Research Gaps Synthesis)
```text
Dựa trên toàn bộ phân tích từ các bài báo trong notebook này, hãy tổng hợp:
1. 3 ĐIỂM NGHẼN LỚN NHẤT mà các công trình hiện tại vẫn chưa giải quyết triệt để.
2. Tại sao kiến trúc MMB-EmotionNet (Đa nhánh chuyên biệt + Tách không gian trực giao Frobenius + Chú ý chéo QKV + Cân bằng mất mát bất định Homoscedastic) lại vượt trội và giải quyết được các điểm nghẽn này?
3. Trích dẫn các bằng chứng cụ thể để đưa vào Chương 2 (Tổng quan) của Luận án Tiến sĩ.
```

---

## 3. Hướng dẫn Tích hợp vào Quyển Luận án Tiến sĩ:
- **Tài liệu này phục vụ trực tiếp cho**: Chương 5 & Chương 7 (Phân tích Trực quan hóa Bản đồ Não & Ý nghĩa Sinh học).
- **Kết quả bóc tách từ NotebookLM**: Copy trực tiếp vào các mục tương ứng trong Luận án và bản thảo bài báo Journal IEEE TAFFC.
