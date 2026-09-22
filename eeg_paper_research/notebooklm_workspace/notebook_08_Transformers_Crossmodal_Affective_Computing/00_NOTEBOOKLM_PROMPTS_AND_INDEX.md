# Notebook 08: Multimodal Transformers & Hierarchical Cross-Attention Networks
**Chủ đề Tiếng Việt**: Kiến trúc Multimodal Transformer & Chú ý Đa tầng trong Cảm xúc  
**Chương Luận án liên kết**: **Chương 2 & Chương 3 (So sánh Đối sánh Transformer & MulT / MISA)**  
**Trọng tâm nghiên cứu**: Multimodal Transformer (MulT), MISA modality-invariant/specific representations, cross-modal scaled dot-product attention, and spatio-temporal self-attention.  

---

## 1. Danh mục Toàn bộ Bài báo Khoa học trong Notebook này (18 bài)

| ID | Năm | Tiêu đề bài báo | Nơi công bố / Tạp chí | Trích dẫn | Tình trạng Tài liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW8_001` | **2023** | **Emotion recognition and artificial intelligence: A systematic review (2014–2023) and research recommendations**<br>*Smith K. Khare, Victoria Blanes‐Vid...* | Information Fusion | 462 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_002` | **2024** | **CTNet: a convolutional transformer network for EEG-based motor imagery classification**<br>*Wei Zhao, Xiaolu Jiang, Baocan Zhan...* | Scientific Reports | 172 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_003` | **2024** | **Role of machine learning and deep learning techniques in EEG-based BCI emotion recognition system: a review**<br>*Priyadarsini Samal, Mohammad Farukh...* | Artificial Intelligence Review | 147 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_004` | **2023** | **Deep Learning in EEG-Based BCIs: A Comprehensive Review of Transformer Models, Advantages, Challenges, and Applications**<br>*Berdakh Abibullaev, Aigerim Keutaye...* | IEEE Access | 136 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_005` | **2023** | **Emotion Recognition Using Different Sensors, Emotion Models, Methods and Datasets: A Comprehensive Review**<br>*Yujian Cai, Xingguang Li, Jinsong L...* | Sensors | 133 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_006` | **2023** | **Affective Computing: Recent Advances, Challenges, and Future Trends**<br>*Guanxiong Pei, Haiying Li, Yandi Lu...* | Intelligent Computing | 132 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_007` | **2023** | **Electrocardiogram Monitoring Wearable Devices and Artificial-Intelligence-Enabled Diagnostic Capabilities: A Review**<br>*Luca Neri, Matt T. Oberdier, Kirste...* | Sensors | 132 | 🌐 Link bài báo Open Access |
| `OA_KW8_008` | **2023** | **Multimodal Emotion Recognition Based on Facial Expressions, Speech, and EEG**<br>*Jiahui Pan, Weijie Fang, Zhihang Zh...* | IEEE Open Journal of Engineering in Medicine and Biology | 119 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_009` | **2025** | **A review on EEG-based multimodal learning for emotion recognition**<br>*Rajasekhar Pillalamarri, S. Udhayak...* | Artificial Intelligence Review | 117 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_010` | **2023** | **DICE-Net: A Novel Convolution-Transformer Architecture for Alzheimer Detection in EEG Signals**<br>*Ανδρέας Μιλτιάδους, Emmanouil Giona...* | IEEE Access | 196 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_011` | **2024** | **Graph Neural Network-Based EEG Classification: A Survey**<br>*Dominik Klepl, Min Wu, Fei He* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 126 | 🌐 Link bài báo Open Access |
| `OA_KW8_012` | **2023** | **Application of data fusion for automated detection of children with developmental and mental disorders: A systematic review of the last decade**<br>*Smith K. Khare, Sonja March, Prabal...* | Information Fusion | 111 | 🌐 Link bài báo Open Access |
| `OA_KW8_013` | **2023** | **EEGformer: A transformer–based brain activity classification method using EEG signal**<br>*Zhijiang Wan, Manyu Li, Shichang Li...* | Frontiers in Neuroscience | 108 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_014` | **2024** | **Enhancing early Parkinson’s disease detection through multimodal deep learning and explainable AI: insights from the PPMI database**<br>*Vincenzo Dentamaro, Donato Impedovo...* | Scientific Reports | 107 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_015` | **2023** | **D 2 PAM : Epileptic seizures prediction using adversarial deep dual patch attention mechanism**<br>*Arfat Ahmad Khan, Rakesh Kumar Made...* | CAAI Transactions on Intelligence Technology | 105 | 🌐 Link bài báo Open Access |
| `OA_KW8_016` | **2023** | **Multimodal Human–Robot Interaction for Human‐Centric Smart Manufacturing: A Survey**<br>*Tian Wang, Pai Zheng, Shufei Li, Li...* | Advanced Intelligent Systems | 187 | 🌐 Link bài báo Open Access |
| `OA_KW8_017` | **2023** | **Recent advancements in multimodal human–robot interaction**<br>*Hang Su, Wen Qi, Jiahao Chen, Cheng...* | Frontiers in Neurorobotics | 180 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW8_018` | **2023** | **Deep learning and machine learning in psychiatry: a survey of current progress in depression detection, diagnosis and treatment**<br>*Matthew Squires, Xiaohui Tao, Soman...* | Brain Informatics | 157 | 📄 Có sẵn PDF trong thư mục |


---

## 2. Bộ Prompt Master Class (Google NotebookLM) Theo Chuẩn 20 Tiêu Chí

Dưới đây là 7 Prompts chuyên dụng được thiết kế riêng cho **Notebook 08: Multimodal Transformers & Hierarchical Cross-Attention Networks**. Bạn chỉ cần tải các bài báo/tài liệu trong thư mục này lên Google NotebookLM ([https://notebooklm.google.com/](https://notebooklm.google.com/)) và dán lần lượt các prompt bên dưới:

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
- **Tài liệu này phục vụ trực tiếp cho**: Chương 2 & Chương 3 (So sánh Đối sánh Transformer & MulT / MISA).
- **Kết quả bóc tách từ NotebookLM**: Copy trực tiếp vào các mục tương ứng trong Luận án và bản thảo bài báo Journal IEEE TAFFC.
