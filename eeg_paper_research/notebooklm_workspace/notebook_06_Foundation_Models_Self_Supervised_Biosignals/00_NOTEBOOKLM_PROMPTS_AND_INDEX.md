# Notebook 06: Foundation Models & Self-Supervised Learning for Biosignals
**Chủ đề Tiếng Việt**: Mô hình Nền tảng (Foundation Models) & Học Tự Giám Sát (MAE / Contrastive)  
**Chương Luận án liên kết**: **Chương 2 & Chương 7 (Xu hướng Công nghệ Mới 2023–2026 & Hướng Phát triển)**  
**Trọng tâm nghiên cứu**: Masked Autoencoders (MAE), Contrastive Learning (SimCLR/MoCo for EEG), foundation pre-training on large-scale biosignal archives (TUH EEG, Sleep-EDF), and zero-shot transfer.  

---

## 1. Danh mục Toàn bộ Bài báo Khoa học trong Notebook này (50 bài)

| ID | Năm | Tiêu đề bài báo | Nơi công bố / Tạp chí | Trích dẫn | Tình trạng Tài liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW6_001` | **2023** | **Emotion recognition and artificial intelligence: A systematic review (2014–2023) and research recommendations**<br>*Smith K. Khare, Victoria Blanes‐Vid...* | Information Fusion | 462 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_002` | **2024** | **Integrating artificial intelligence to assess emotions in learning environments: a systematic literature review**<br>*Angel Olider Rojas Vistorte, Ángel ...* | Frontiers in Psychology | 271 | 🌐 Link bài báo Open Access |
| `OA_KW6_003` | **2023** | **DICE-Net: A Novel Convolution-Transformer Architecture for Alzheimer Detection in EEG Signals**<br>*Ανδρέας Μιλτιάδους, Emmanouil Giona...* | IEEE Access | 196 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_004` | **2023** | **LGGNet: Learning From Local-Global-Graph Representations for Brain–Computer Interface**<br>*Yi Ding, Neethu Robinson, Chengxuan...* | IEEE Transactions on Neural Networks and Learning Systems | 194 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_005` | **2024** | **CTNet: a convolutional transformer network for EEG-based motor imagery classification**<br>*Wei Zhao, Xiaolu Jiang, Baocan Zhan...* | Scientific Reports | 172 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_006` | **2023** | **TMS combined with EEG: Recommendations and open issues for data collection and analysis**<br>*Julio C. Hernandez-Pavon, Domenica ...* | Brain stimulation | 251 | 🌐 Link bài báo Open Access |
| `OA_KW6_007` | **2024** | **Role of machine learning and deep learning techniques in EEG-based BCI emotion recognition system: a review**<br>*Priyadarsini Samal, Mohammad Farukh...* | Artificial Intelligence Review | 147 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_008` | **2023** | **Electrocardiogram Monitoring Wearable Devices and Artificial-Intelligence-Enabled Diagnostic Capabilities: A Review**<br>*Luca Neri, Matt T. Oberdier, Kirste...* | Sensors | 132 | 🌐 Link bài báo Open Access |
| `OA_KW6_009` | **2025** | **A review on EEG-based multimodal learning for emotion recognition**<br>*Rajasekhar Pillalamarri, S. Udhayak...* | Artificial Intelligence Review | 117 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_010` | **2023** | **Review of Studies on Emotion Recognition and Judgment Based on Physiological Signals**<br>*Wenqian Lin, Chao Li* | Applied Sciences | 116 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_011` | **2023** | **Transformer-Based Self-Supervised Multimodal Representation Learning for Wearable Emotion Recognition**<br>*Yujin Wu, Mohamed Daoudi, Ali Amad* | IEEE Transactions on Affective Computing | 106 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_012` | **2024** | **Review of Stress Detection Methods Using Wearable Sensors**<br>*Georgios V. Taskasaplidis, Dimitris...* | IEEE Access | 105 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_013` | **2023** | **Stress and Workload Assessment in Aviation—A Narrative Review**<br>*Giulia Masi, Gianluca Amprimo, Clau...* | Sensors | 97 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_014` | **2024** | **Machine learning for human emotion recognition: a comprehensive review**<br>*Eman M. G. Younis, Someya Mohsen, E...* | Neural Computing and Applications | 75 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_015` | **2024** | **Epileptic seizure prediction via multidimensional transformer and recurrent neural network fusion**<br>*Rong Zhu, Wen-Xin Pan, Jin‐Xing Liu...* | Journal of Translational Medicine | 74 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_016` | **2024** | **Multimodal Emotion Recognition Using Visual, Vocal and Physiological Signals: A Review**<br>*Gustave Udahemuka, Karim Djouani, A...* | Applied Sciences | 74 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_017` | **2023** | **Approaches, Applications, and Challenges in Physiological Emotion Recognition—A Tutorial Overview**<br>*Yekta Said Can, Bhargavi Mahesh, El...* | Proceedings of the IEEE | 73 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_018` | **2024** | **Machine Learning and Digital Biomarkers Can Detect Early Stages of Neurodegenerative Diseases**<br>*Artur Chudzik, Albert Śledzianowski...* | Sensors | 119 | 🌐 Link bài báo Open Access |
| `OA_KW6_019` | **2024** | **Workplace Well-Being in Industry 5.0: A Worker-Centered Systematic Review**<br>*Francesca Giada Antonaci, Elena Car...* | Sensors | 73 | 🌐 Link bài báo Open Access |
| `OA_KW6_020` | **2024** | **Multimodal Mental Health Digital Biomarker Analysis From Remote Interviews Using Facial, Vocal, Linguistic, and Cardiovascular Patterns**<br>*Zifan Jiang, Salman Seyedi, Emily G...* | IEEE Journal of Biomedical and Health Informatics | 52 | 🌐 Link bài báo Open Access |
| `OA_KW6_021` | **2024** | **A Systematic Literature Review of Modalities, Trends, and Limitations in Emotion Recognition, Affective Computing, and Sentiment Analysis**<br>*Rosa A. García-Hernández, Huizilopo...* | Applied Sciences | 45 | 🌐 Link bài báo Open Access |
| `OA_KW6_022` | **2023** | **Multimodal Adaptive Emotion Transformer with Flexible Modality Inputs on A Novel Dataset with Continuous Labels**<br>*Wei-Bang Jiang, Xuan-Hao Liu, Wei‐L...* | Open Access Journal | 43 | 🌐 Link bài báo Open Access |
| `OA_KW6_023` | **2024** | **DMMR: Cross-Subject Domain Generalization for EEG-Based Emotion Recognition via Denoising Mixed Mutual Reconstruction**<br>*Yiming Wang, Bin Zhang, Yujiao Tang* | Proceedings of the AAAI Conference on Artificial Intelligence | 41 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_024` | **2023** | **EEG driving fatigue detection based on log-Mel spectrogram and convolutional recurrent neural networks**<br>*Dongrui Gao, Xue Tang, Manqing Wan,...* | Frontiers in Neuroscience | 39 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_025` | **2024** | **Multi-Scale Masked Autoencoders for Cross-Session Emotion Recognition**<br>*Miaoqi Pang, Hongtao Wang, Jiayang ...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 37 | 🌐 Link bài báo Open Access |
| `OA_KW6_026` | **2023** | **ASTDF-Net: Attention-Based Spatial-Temporal Dual-Stream Fusion Network for EEG-Based Emotion Recognition**<br>*Peiliang Gong, Ziyu Jia, Pengpai Wa...* | Open Access Journal | 37 | 🌐 Link bài báo Open Access |
| `OA_KW6_027` | **2023** | **EEG-based investigation of effects of mindfulness meditation training on state and trait by deep learning and traditional machine learning**<br>*Baoxiang Shang, Feiyan Duan, Ruiqi ...* | Frontiers in Human Neuroscience | 29 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_028` | **2024** | **Harnessing Few-Shot Learning for EEG signal classification: a survey of state-of-the-art techniques and future directions**<br>*Chirag Ahuja, Divyashikha Sethia* | Frontiers in Human Neuroscience | 28 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_029` | **2025** | **Emotionally adaptive support: a narrative review of affective computing for mental health**<br>*Michelle Schlicher, Yupei Li, Sunil...* | Frontiers in Digital Health | 26 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_030` | **2024** | **Emotion Recognition Using EEG Signals and Audiovisual Features with Contrastive Learning**<br>*Ju-Hwan Lee, Jin Young Kim, Hyoung‐...* | Bioengineering | 24 | 🌐 Link bài báo Open Access |
| `OA_KW6_031` | **2025** | **Application Status, Challenges, and Development Prospects of Smart Technologies in Home-Based Elder Care**<br>*Jialin Shi, Ning Zhang, Kai Wu, Zon...* | Electronics | 23 | 🌐 Link bài báo Open Access |
| `OA_KW6_032` | **2024** | **Generative AI Models in Time-Varying Biomedical Data: Scoping Review**<br>*Rosemary He, Varuni Sarwal, Xinru Q...* | Journal of Medical Internet Research | 22 | 🌐 Link bài báo Open Access |
| `OA_KW6_033` | **2023** | **EEG-based Cognitive Load Classification using Feature Masked Autoencoding and Emotion Transfer Learning**<br>*Dustin Pulver, Prithila Angkan, Pau...* | INTERNATIONAL CONFERENCE ON MULTIMODAL INTERACTION | 22 | 🌐 Link bài báo Open Access |
| `OA_KW6_034` | **2025** | **A Systematic Review of Mental Health Monitoring and Intervention Using Unsupervised Deep Learning on EEG Data**<br>*Akhila Reddy Yadulla, Guna Sekhar S...* | Psychology International | 20 | 🌐 Link bài báo Open Access |
| `OA_KW6_035` | **2024** | **Integrating IoMT and AI for Proactive Healthcare: Predictive Models and Emotion Detection in Neurodegenerative Diseases**<br>*Virginia Săndulescu, Marilena Iancu...* | Algorithms | 20 | 🌐 Link bài báo Open Access |
| `OA_KW6_036` | **2024** | **Large Brain Model for Learning Generic Representations with Tremendous EEG Data in BCI**<br>*Wei-Bang Jiang, Liming Zhao, Bao‐Li...* | arXiv (Cornell University) | 19 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_037` | **2023** | **Recent advancements in multimodal human–robot interaction**<br>*Hang Su, Wen Qi, Jiahao Chen, Cheng...* | Frontiers in Neurorobotics | 180 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_038` | **2024** | **Brain–computer interfaces: the innovative key to unlocking neurological conditions**<br>*Hongyu Zhang, Le Jiao, Songxiang Ya...* | International Journal of Surgery | 167 | 🌐 Link bài báo Open Access |
| `OA_KW6_039` | **2025** | **From Neural Networks to Emotional Networks: A Systematic Review of EEG-Based Emotion Recognition in Cognitive Neuroscience and Real-World Applications**<br>*Evgenia Gkintoni, Anthimos Aroutzid...* | Brain Sciences | 144 | 🌐 Link bài báo Open Access |
| `OA_KW6_040` | **2023** | **Deep Learning in EEG-Based BCIs: A Comprehensive Review of Transformer Models, Advantages, Challenges, and Applications**<br>*Berdakh Abibullaev, Aigerim Keutaye...* | IEEE Access | 136 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_041` | **2023** | **Emotion Recognition Using Different Sensors, Emotion Models, Methods and Datasets: A Comprehensive Review**<br>*Yujian Cai, Xingguang Li, Jinsong L...* | Sensors | 133 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_042` | **2024** | **Graph Neural Network-Based EEG Classification: A Survey**<br>*Dominik Klepl, Min Wu, Fei He* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 126 | 🌐 Link bài báo Open Access |
| `OA_KW6_043` | **2023** | **Generative adversarial networks in EEG analysis: an overview**<br>*Ahmed G. Habashi, Ahmed M. Azab, Se...* | Journal of NeuroEngineering and Rehabilitation | 124 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_044` | **2023** | **Application of data fusion for automated detection of children with developmental and mental disorders: A systematic review of the last decade**<br>*Smith K. Khare, Sonja March, Prabal...* | Information Fusion | 111 | 🌐 Link bài báo Open Access |
| `OA_KW6_045` | **2025** | **Artificial Intelligence and Neuroscience: Transformative Synergies in Brain Research and Clinical Applications**<br>*Răzvan Onciul, Cătălina-Ioana Tătar...* | Journal of Clinical Medicine | 108 | 🌐 Link bài báo Open Access |
| `OA_KW6_046` | **2023** | **State-of-the-Art of Stress Prediction from Heart Rate Variability Using Artificial Intelligence**<br>*Yeaminul Haque, Rahat Shahriar Zawa...* | Cognitive Computation | 107 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_047` | **2023** | **A Spiking Neural Network With Adaptive Graph Convolution and LSTM for EEG-Based Brain-Computer Interfaces**<br>*Peiliang Gong, Pengpai Wang, Yueyin...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 105 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_048` | **2025** | **Transformers in EEG Analysis: A Review of Architectures and Applications in Motor Imagery, Seizure, and Emotion Classification**<br>*Elnaz Vafaei, Mohammad Hosseini* | Sensors | 104 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_049` | **2023** | **The transformative power of music: Insights into neuroplasticity, health, and disease**<br>*Muriel Tahtouh Zaatar, Kenda Alhaki...* | Brain Behavior & Immunity - Health | 102 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW6_050` | **2023** | **A Large Finer-grained Affective Computing EEG Dataset**<br>*Jingjing Chen, Xiaobin Wang, Chen H...* | Scientific Data | 98 | 📄 Có sẵn PDF trong thư mục |


---

## 2. Bộ Prompt Master Class (Google NotebookLM) Theo Chuẩn 20 Tiêu Chí

Dưới đây là 7 Prompts chuyên dụng được thiết kế riêng cho **Notebook 06: Foundation Models & Self-Supervised Learning for Biosignals**. Bạn chỉ cần tải các bài báo/tài liệu trong thư mục này lên Google NotebookLM ([https://notebooklm.google.com/](https://notebooklm.google.com/)) và dán lần lượt các prompt bên dưới:

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
- **Tài liệu này phục vụ trực tiếp cho**: Chương 2 & Chương 7 (Xu hướng Công nghệ Mới 2023–2026 & Hướng Phát triển).
- **Kết quả bóc tách từ NotebookLM**: Copy trực tiếp vào các mục tương ứng trong Luận án và bản thảo bài báo Journal IEEE TAFFC.
