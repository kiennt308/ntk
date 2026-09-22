# Notebook 03: Multi-Branch Encoders & Directional Cross-Modal Attention
**Chủ đề Tiếng Việt**: Bộ mã hóa Đa nhánh theo Vật lý Tín hiệu & Cơ chế Chú ý Chéo QKV  
**Chương Luận án liên kết**: **Chương 3 & Chương 5 (Tầng mã hóa chuyên biệt & Thực nghiệm Triệt tiêu Attention)**  
**Trọng tâm nghiên cứu**: EEGNet Spatial-temporal 2D-CNN, ECG/EDA Dilated Multi-Scale 1D-CNNs, QKV autonomic modulation, and intermediate fusion paradigms.  

---

## 1. Danh mục Toàn bộ Bài báo Khoa học trong Notebook này (46 bài)

| ID | Năm | Tiêu đề bài báo | Nơi công bố / Tạp chí | Trích dẫn | Tình trạng Tài liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW3_001` | **2023** | **Emotion recognition and artificial intelligence: A systematic review (2014–2023) and research recommendations**<br>*Smith K. Khare, Victoria Blanes‐Vid...* | Information Fusion | 462 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_002` | **2024** | **Integrating artificial intelligence to assess emotions in learning environments: a systematic literature review**<br>*Angel Olider Rojas Vistorte, Ángel ...* | Frontiers in Psychology | 271 | 🌐 Link bài báo Open Access |
| `OA_KW3_003` | **2023** | **Gut Microbiome–Brain Alliance: A Landscape View into Mental and Gastrointestinal Health and Disorders**<br>*Janet M. Sasso, Ramy M. Ammar, Rumi...* | ACS Chemical Neuroscience | 207 | 🌐 Link bài báo Open Access |
| `OA_KW3_004` | **2024** | **Pathology of pain and its implications for therapeutic interventions**<br>*Bo Cao, Qixuan Xu, Yajiao Shi, Ruiy...* | Signal Transduction and Targeted Therapy | 186 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_005` | **2023** | **Deep Learning in EEG-Based BCIs: A Comprehensive Review of Transformer Models, Advantages, Challenges, and Applications**<br>*Berdakh Abibullaev, Aigerim Keutaye...* | IEEE Access | 136 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_006` | **2023** | **Affective Computing: Recent Advances, Challenges, and Future Trends**<br>*Guanxiong Pei, Haiying Li, Yandi Lu...* | Intelligent Computing | 132 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_007` | **2023** | **Electrocardiogram Monitoring Wearable Devices and Artificial-Intelligence-Enabled Diagnostic Capabilities: A Review**<br>*Luca Neri, Matt T. Oberdier, Kirste...* | Sensors | 132 | 🌐 Link bài báo Open Access |
| `OA_KW3_008` | **2024** | **Graph Neural Network-Based EEG Classification: A Survey**<br>*Dominik Klepl, Min Wu, Fei He* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 126 | 🌐 Link bài báo Open Access |
| `OA_KW3_009` | **2023** | **Generative adversarial networks in EEG analysis: an overview**<br>*Ahmed G. Habashi, Ahmed M. Azab, Se...* | Journal of NeuroEngineering and Rehabilitation | 124 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_010` | **2023** | **Multimodal Emotion Recognition Based on Facial Expressions, Speech, and EEG**<br>*Jiahui Pan, Weijie Fang, Zhihang Zh...* | IEEE Open Journal of Engineering in Medicine and Biology | 119 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_011` | **2025** | **A review on EEG-based multimodal learning for emotion recognition**<br>*Rajasekhar Pillalamarri, S. Udhayak...* | Artificial Intelligence Review | 117 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_012` | **2024** | **Role of machine learning and deep learning techniques in EEG-based BCI emotion recognition system: a review**<br>*Priyadarsini Samal, Mohammad Farukh...* | Artificial Intelligence Review | 147 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_013` | **2023** | **Review of Studies on Emotion Recognition and Judgment Based on Physiological Signals**<br>*Wenqian Lin, Chao Li* | Applied Sciences | 116 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_014` | **2023** | **State-of-the-Art of Stress Prediction from Heart Rate Variability Using Artificial Intelligence**<br>*Yeaminul Haque, Rahat Shahriar Zawa...* | Cognitive Computation | 107 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_015` | **2023** | **Transformer-Based Self-Supervised Multimodal Representation Learning for Wearable Emotion Recognition**<br>*Yujin Wu, Mohamed Daoudi, Ali Amad* | IEEE Transactions on Affective Computing | 106 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_016` | **2023** | **Stress and Workload Assessment in Aviation—A Narrative Review**<br>*Giulia Masi, Gianluca Amprimo, Clau...* | Sensors | 97 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_017` | **2023** | **An interpretable machine learning approach to multimodal stress detection in a simulated office environment**<br>*Mara Naegelin, Raphael P. Weibel, J...* | Journal of Biomedical Informatics | 81 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_018` | **2023** | **Multimodal Hierarchical CNN Feature Fusion for Stress Detection**<br>*Radhika Kuttala, Ramanathan Subrama...* | IEEE Access | 79 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_019` | **2024** | **Machine learning for human emotion recognition: a comprehensive review**<br>*Eman M. G. Younis, Someya Mohsen, E...* | Neural Computing and Applications | 75 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_020` | **2024** | **Multimodal Emotion Recognition Using Visual, Vocal and Physiological Signals: A Review**<br>*Gustave Udahemuka, Karim Djouani, A...* | Applied Sciences | 74 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_021` | **2023** | **Approaches, Applications, and Challenges in Physiological Emotion Recognition—A Tutorial Overview**<br>*Yekta Said Can, Bhargavi Mahesh, El...* | Proceedings of the IEEE | 73 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_022` | **2023** | **Cross-Subject Emotion Recognition Brain–Computer Interface Based on fNIRS and DBJNet**<br>*Xiaopeng Si, He Huang, Jiayue Yu, D...* | Cyborg and Bionic Systems | 70 | 🌐 Link bài báo Open Access |
| `OA_KW3_023` | **2025** | **Artificial Intelligence in Psychiatry: A Review of Biological and Behavioral Data Analyses**<br>*Ismail BAYDİLİ, Burak Taşçı, Gülay ...* | Diagnostics | 69 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_024` | **2024** | **MASA-TCN: Multi-Anchor Space-Aware Temporal Convolutional Neural Networks for Continuous and Discrete EEG Emotion Recognition**<br>*Yi Ding, Su Zhang, Chuangao Tang, C...* | IEEE Journal of Biomedical and Health Informatics | 60 | 🌐 Link bài báo Open Access |
| `OA_KW3_025` | **2023** | **A novel feature fusion network for multimodal emotion recognition from EEG and eye movement signals**<br>*Baole Fu, Chunrui Gu, M.W. Fu, Yuxi...* | Frontiers in Neuroscience | 34 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_026` | **2023** | **Depressive Disorder Recognition Based on Frontal EEG Signals and Deep Learning**<br>*Yanting Xu, Hongyang Zhong, Shangya...* | Sensors | 33 | 🌐 Link bài báo Open Access |
| `OA_KW3_027` | **2024** | **Diagnosis of mental disorders using machine learning: Literature review and bibliometric mapping from 2012 to 2023**<br>*Chandra Mani Sharma, Vijayaraghavan...* | Heliyon | 28 | 🌐 Link bài báo Open Access |
| `OA_KW3_028` | **2024** | **EEG Emotion Recognition Model Based on Attention and GAN**<br>*Wenxuan Qiao, Li Sun, Jinhui Wu, P....* | IEEE Access | 21 | 🌐 Link bài báo Open Access |
| `OA_KW3_029` | **2024** | **Resting-State Electroencephalogram Depression Diagnosis Based on Traditional Machine Learning and Deep Learning: A Comparative Analysis**<br>*Haijun Lin, Jing Fang, Junpeng Zhan...* | Sensors | 17 | 🌐 Link bài báo Open Access |
| `OA_KW3_030` | **2024** | **MSLTE: multiple self-supervised learning tasks for enhancing EEG emotion recognition**<br>*Guangqiang Li, Ning Chen, Yixiang N...* | Journal of Neural Engineering | 17 | 🌐 Link bài báo Open Access |
| `OA_KW3_031` | **2023** | **Transformer-based ensemble deep learning model for EEG-based emotion recognition**<br>*Xiaopeng Si, Dong Huang, Yulin Sun,...* | Brain Science Advances | 17 | 🌐 Link bài báo Open Access |
| `OA_KW3_032` | **2019** | **Deep learning for electroencephalogram (EEG) classification tasks: a review**<br>*Alexander Craik, Yongtian He, José ...* | Journal of Neural Engineering | 1776 | 🌐 Link bài báo Open Access |
| `OA_KW3_033` | **2019** | **Stress detection in daily life scenarios using smart phones and wearable sensors: A survey**<br>*Yekta Said Can, Bert Arnrich, Cem E...* | Journal of Biomedical Informatics | 479 | 🌐 Link bài báo Open Access |
| `OA_KW3_034` | **2019** | **MPED: A Multi-Modal Physiological Emotion Database for Discrete Emotion Recognition**<br>*Tengfei Song, Wenming Zheng, Lu Che...* | IEEE Access | 340 | 🌐 Link bài báo Open Access |
| `OA_KW3_035` | **2019** | **Current Directions in the Auricular Vagus Nerve Stimulation I – A Physiological Perspective**<br>*Eugenijus Kaniušas, Stefan Kampusch...* | Frontiers in Neuroscience | 330 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_036` | **2024** | **CTNet: a convolutional transformer network for EEG-based motor imagery classification**<br>*Wei Zhao, Xiaolu Jiang, Baocan Zhan...* | Scientific Reports | 172 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_037` | **2023** | **Recent advancements in multimodal human–robot interaction**<br>*Hang Su, Wen Qi, Jiahao Chen, Cheng...* | Frontiers in Neurorobotics | 180 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_038` | **2023** | **EEG-Based BCIs on Motor Imagery Paradigm Using Wearable Technologies: A Systematic Review**<br>*Aurora Saibene, Mirko Caglioni, Sil...* | Sensors | 82 | 🌐 Link bài báo Open Access |
| `OA_KW3_039` | **2023** | **Cognitive workload estimation using physiological measures: a review**<br>*Debashis Das Chakladar, Partha Prat...* | Cognitive Neurodynamics | 76 | 🌐 Link bài báo Open Access |
| `OA_KW3_040` | **2023** | **TS-GAN: Time-series GAN for Sensor-based Health Data Augmentation**<br>*Zhenyu Yang, Yantao Li, Gang Zhou* | ACM Transactions on Computing for Healthcare | 70 | 🌐 Link bài báo Open Access |
| `OA_KW3_041` | **2023** | **Neural Applications Using Immersive Virtual Reality: A Review on EEG Studies**<br>*Jin Woo Choi, Haram Kwon, Jae-Hoon ...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 69 | 🌐 Link bài báo Open Access |
| `OA_KW3_042` | **2025** | **Fusing Wearable Biosensors with Artificial Intelligence for Mental Health Monitoring: A Systematic Review**<br>*Ali Kargarandehkordi, Shizhe Li, Ka...* | Biosensors | 66 | 🌐 Link bài báo Open Access |
| `OA_KW3_043` | **2023** | **Detection of Driver Cognitive Distraction Using Machine Learning Methods**<br>*Apurva Misra, Siby Samuel, Shi Cao,...* | IEEE Access | 66 | 🌐 Link bài báo Open Access |
| `OA_KW3_044` | **2023** | **Large-scale neural dynamics in a shared low-dimensional state space reflect cognitive and attentional dynamics**<br>*Hayoung Song, Won Mok Shim, Monica ...* | eLife | 63 | 🌐 Link bài báo Open Access |
| `OA_KW3_045` | **2023** | **SchizoNET: a robust and accurate Margenau–Hill time-frequency distribution based deep neural network model for schizophrenia detection using EEG signals**<br>*Smith K. Khare, Varun Bajaj, U. Raj...* | Physiological Measurement | 59 | 🌐 Link bài báo Open Access |
| `OA_KW3_046` | **2023** | **Incorporation of seafarer psychological factors into maritime safety assessment**<br>*Shiqi Fan, Eduardo Blanco‐Davis, St...* | Ocean & Coastal Management | 58 | 🌐 Link bài báo Open Access |


---

## 2. Bộ Prompt Master Class (Google NotebookLM) Theo Chuẩn 20 Tiêu Chí

Dưới đây là 7 Prompts chuyên dụng được thiết kế riêng cho **Notebook 03: Multi-Branch Encoders & Directional Cross-Modal Attention**. Bạn chỉ cần tải các bài báo/tài liệu trong thư mục này lên Google NotebookLM ([https://notebooklm.google.com/](https://notebooklm.google.com/)) và dán lần lượt các prompt bên dưới:

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
- **Tài liệu này phục vụ trực tiếp cho**: Chương 3 & Chương 5 (Tầng mã hóa chuyên biệt & Thực nghiệm Triệt tiêu Attention).
- **Kết quả bóc tách từ NotebookLM**: Copy trực tiếp vào các mục tương ứng trong Luận án và bản thảo bài báo Journal IEEE TAFFC.
