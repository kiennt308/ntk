# Notebook 10: Closed-Loop BCI, Real-Time Edge Affective Computing & Healthcare
**Chủ đề Tiếng Việt**: Giao tiếp Não - Máy tính Vòng lặp Khép kín, Tính toán Biên & Sức khỏe Tâm thần  
**Chương Luận án liên kết**: **Chương 7 (Ứng dụng Thực tiễn Y tế, BCI Thiết bị đeo & Định hướng Tương lai)**  
**Trọng tâm nghiên cứu**: Closed-loop neurofeedback, real-time edge execution (TensorRT on Jetson, ONNX on Raspberry Pi), wearable depression/stress monitoring, and digital mental health interventions.  

---

## 1. Danh mục Toàn bộ Bài báo Khoa học trong Notebook này (9 bài)

| ID | Năm | Tiêu đề bài báo | Nơi công bố / Tạp chí | Trích dẫn | Tình trạng Tài liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW1_001` | **2024** | **Leveraging AI in E-Learning: Personalized Learning and Adaptive Assessment through Cognitive Neuropsychology—A Systematic Analysis**<br>*Constantinos Halkiopoulos, Evgenia ...* | Electronics | 313 | 🌐 Link bài báo Open Access |
| `OA_KW1_002` | **2025** | **Challenging Cognitive Load Theory: The Role of Educational Neuroscience and Artificial Intelligence in Redefining Learning Efficacy**<br>*Evgenia Gkintoni, Hera Antonopoulou...* | Brain Sciences | 284 | 🌐 Link bài báo Open Access |
| `OA_KW1_003` | **2024** | **Integrating artificial intelligence to assess emotions in learning environments: a systematic literature review**<br>*Angel Olider Rojas Vistorte, Ángel ...* | Frontiers in Psychology | 271 | 🌐 Link bài báo Open Access |
| `OA_KW1_004` | **2023** | **Gut Microbiome–Brain Alliance: A Landscape View into Mental and Gastrointestinal Health and Disorders**<br>*Janet M. Sasso, Ramy M. Ammar, Rumi...* | ACS Chemical Neuroscience | 207 | 🌐 Link bài báo Open Access |
| `OA_KW1_005` | **2023** | **LGGNet: Learning From Local-Global-Graph Representations for Brain–Computer Interface**<br>*Yi Ding, Neethu Robinson, Chengxuan...* | IEEE Transactions on Neural Networks and Learning Systems | 194 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_006` | **2023** | **Recent advancements in multimodal human–robot interaction**<br>*Hang Su, Wen Qi, Jiahao Chen, Cheng...* | Frontiers in Neurorobotics | 180 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_007` | **2024** | **CTNet: a convolutional transformer network for EEG-based motor imagery classification**<br>*Wei Zhao, Xiaolu Jiang, Baocan Zhan...* | Scientific Reports | 172 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_008` | **2024** | **Brain–computer interfaces: the innovative key to unlocking neurological conditions**<br>*Hongyu Zhang, Le Jiao, Songxiang Ya...* | International Journal of Surgery | 167 | 🌐 Link bài báo Open Access |
| `OA_KW1_009` | **2023** | **Generalizable machine learning for stress monitoring from wearable devices: A systematic literature review**<br>*Gideon Vos, Kelly Trinh, Zóltan Sar...* | International Journal of Medical Informatics | 160 | 📄 Có sẵn PDF trong thư mục |


---

## 2. Bộ Prompt Master Class (Google NotebookLM) Theo Chuẩn 20 Tiêu Chí

Dưới đây là 7 Prompts chuyên dụng được thiết kế riêng cho **Notebook 10: Closed-Loop BCI, Real-Time Edge Affective Computing & Healthcare**. Bạn chỉ cần tải các bài báo/tài liệu trong thư mục này lên Google NotebookLM ([https://notebooklm.google.com/](https://notebooklm.google.com/)) và dán lần lượt các prompt bên dưới:

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
- **Tài liệu này phục vụ trực tiếp cho**: Chương 7 (Ứng dụng Thực tiễn Y tế, BCI Thiết bị đeo & Định hướng Tương lai).
- **Kết quả bóc tách từ NotebookLM**: Copy trực tiếp vào các mục tương ứng trong Luận án và bản thảo bài báo Journal IEEE TAFFC.
