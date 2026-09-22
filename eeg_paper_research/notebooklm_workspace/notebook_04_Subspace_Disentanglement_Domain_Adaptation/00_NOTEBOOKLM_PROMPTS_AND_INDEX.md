# Notebook 04: Shared-Private Subspace Disentanglement & Cross-Subject Generalization
**Chủ đề Tiếng Việt**: Tách Không gian con Dùng chung - Riêng biệt & Thích ứng Miền LOSO  
**Chương Luận án liên kết**: **Chương 3 & Chương 5 (Phân tách Biểu diễn & Thử nghiệm Tổng quát hóa LOSO)**  
**Trọng tâm nghiên cứu**: CMD similarity loss, Frobenius soft orthogonality difference loss, Gradient Reversal Layer (GRL DANN), and Leave-One-Subject-Out (LOSO) adaptation.  

---

## 1. Danh mục Toàn bộ Bài báo Khoa học trong Notebook này (47 bài)

| ID | Năm | Tiêu đề bài báo | Nơi công bố / Tạp chí | Trích dẫn | Tình trạng Tài liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW4_001` | **2023** | **Consequences of adolescent drug use**<br>*Michael Steinfeld, Mary M. Torregro...* | Translational Psychiatry | 236 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_002` | **2024** | **Pathology of pain and its implications for therapeutic interventions**<br>*Bo Cao, Qixuan Xu, Yajiao Shi, Ruiy...* | Signal Transduction and Targeted Therapy | 186 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_003` | **2023** | **Generalizable machine learning for stress monitoring from wearable devices: A systematic literature review**<br>*Gideon Vos, Kelly Trinh, Zóltan Sar...* | International Journal of Medical Informatics | 160 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_004` | **2024** | **Role of machine learning and deep learning techniques in EEG-based BCI emotion recognition system: a review**<br>*Priyadarsini Samal, Mohammad Farukh...* | Artificial Intelligence Review | 147 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_005` | **2025** | **From Neural Networks to Emotional Networks: A Systematic Review of EEG-Based Emotion Recognition in Cognitive Neuroscience and Real-World Applications**<br>*Evgenia Gkintoni, Anthimos Aroutzid...* | Brain Sciences | 144 | 🌐 Link bài báo Open Access |
| `OA_KW4_006` | **2023** | **Deep Learning in EEG-Based BCIs: A Comprehensive Review of Transformer Models, Advantages, Challenges, and Applications**<br>*Berdakh Abibullaev, Aigerim Keutaye...* | IEEE Access | 136 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_007` | **2023** | **Deep learning-based EEG emotion recognition: Current trends and future perspectives**<br>*Xiaohu Wang, Yongmei Ren, Ze Luo, W...* | Frontiers in Psychology | 133 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_008` | **2023** | **Affective Computing: Recent Advances, Challenges, and Future Trends**<br>*Guanxiong Pei, Haiying Li, Yandi Lu...* | Intelligent Computing | 132 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_009` | **2023** | **Generative adversarial networks in EEG analysis: an overview**<br>*Ahmed G. Habashi, Ahmed M. Azab, Se...* | Journal of NeuroEngineering and Rehabilitation | 124 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_010` | **2025** | **Recent Advances in Portable Dry Electrode EEG: Architecture and Applications in Brain-Computer Interfaces**<br>*Meihong Zhang, Bocheng Qian, Jianmi...* | Sensors | 27 | 🌐 Link bài báo Open Access |
| `OA_KW4_011` | **2023** | **Multimodal Physiological Signals Fusion for Online Emotion Recognition**<br>*Tongjie Pan, Yalan Ye, Hecheng Cai,...* | Open Access Journal/Conference | 21 | 🌐 Link bài báo Open Access |
| `OA_KW4_012` | **2024** | **A review of artificial intelligence methods enabled music-evoked EEG emotion recognition and their applications**<br>*Yan Su, Yong Liu, Yan Xiao, Jiaqi M...* | Frontiers in Neuroscience | 18 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_013` | **2024** | **Multi-level Disentangling Network for Cross-Subject Emotion Recognition Based on Multimodal Physiological Signals**<br>*Ziyu Jia, Fengming Zhao, Yuzhe Guo,...* | Open Access Journal/Conference | 11 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_014` | **2024** | **MISNet: multi-source information-shared EEG emotion recognition network with two-stream structure**<br>*Ming Gong, Wei Zhong, Long Ye, Qin ...* | Frontiers in Neuroscience | 11 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_015` | **2023** | **AffectFAL: Federated Active Affective Computing with Non-IID Data**<br>*Zixin Zhang, Fan Qi, Shuai Li, Chan...* | Open Access Journal/Conference | 8 | 🌐 Link bài báo Open Access |
| `OA_KW4_016` | **2025** | **Anonymization Techniques for Behavioral Biometric Data: A Survey**<br>*Simon Hanisch, Patricia Arias-Cabar...* | ACM Computing Surveys | 5 | 🌐 Link bài báo Open Access |
| `OA_KW4_017` | **2023** | **DICE-Net: A Novel Convolution-Transformer Architecture for Alzheimer Detection in EEG Signals**<br>*Ανδρέας Μιλτιάδους, Emmanouil Giona...* | IEEE Access | 196 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_018` | **2025** | **A review on EEG-based multimodal learning for emotion recognition**<br>*Rajasekhar Pillalamarri, S. Udhayak...* | Artificial Intelligence Review | 117 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_019` | **2023** | **Review of Studies on Emotion Recognition and Judgment Based on Physiological Signals**<br>*Wenqian Lin, Chao Li* | Applied Sciences | 116 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_020` | **2023** | **State-of-the-Art of Stress Prediction from Heart Rate Variability Using Artificial Intelligence**<br>*Yeaminul Haque, Rahat Shahriar Zawa...* | Cognitive Computation | 107 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_021` | **2023** | **Transformer-Based Self-Supervised Multimodal Representation Learning for Wearable Emotion Recognition**<br>*Yujin Wu, Mohamed Daoudi, Ali Amad* | IEEE Transactions on Affective Computing | 106 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_022` | **2024** | **Review of Stress Detection Methods Using Wearable Sensors**<br>*Georgios V. Taskasaplidis, Dimitris...* | IEEE Access | 105 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_023` | **2023** | **Stress and Workload Assessment in Aviation—A Narrative Review**<br>*Giulia Masi, Gianluca Amprimo, Clau...* | Sensors | 97 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_024` | **2023** | **An interpretable machine learning approach to multimodal stress detection in a simulated office environment**<br>*Mara Naegelin, Raphael P. Weibel, J...* | Journal of Biomedical Informatics | 81 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_025` | **2023** | **Multimodal Hierarchical CNN Feature Fusion for Stress Detection**<br>*Radhika Kuttala, Ramanathan Subrama...* | IEEE Access | 79 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_026` | **2024** | **Machine learning for human emotion recognition: a comprehensive review**<br>*Eman M. G. Younis, Someya Mohsen, E...* | Neural Computing and Applications | 75 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_027` | **2024** | **Multimodal Emotion Recognition Using Visual, Vocal and Physiological Signals: A Review**<br>*Gustave Udahemuka, Karim Djouani, A...* | Applied Sciences | 74 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_028` | **2023** | **Approaches, Applications, and Challenges in Physiological Emotion Recognition—A Tutorial Overview**<br>*Yekta Said Can, Bhargavi Mahesh, El...* | Proceedings of the IEEE | 73 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_029` | **2012** | **The brain basis of emotion: A meta-analytic review**<br>*Kristen A. Lindquist, Tor D. Wager,...* | Behavioral and Brain Sciences | 2370 | 🌐 Link bài báo Open Access |
| `OA_KW4_030` | **2019** | **Deep learning for electroencephalogram (EEG) classification tasks: a review**<br>*Alexander Craik, Yongtian He, José ...* | Journal of Neural Engineering | 1776 | 🌐 Link bài báo Open Access |
| `OA_KW4_031` | **2022** | **EEG Conformer: Convolutional Transformer for EEG Decoding and Visualization**<br>*Yonghao Song, Qingqing Zheng, Bingc...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 1053 | 🌐 Link bài báo Open Access |
| `OA_KW4_032` | **2008** | **Music listening enhances cognitive recovery and mood after middle cerebral artery stroke**<br>*Teppo Särkämö, Mari Tervaniemi, S. ...* | Brain | 906 | 🌐 Link bài báo Open Access |
| `OA_KW4_033` | **2020** | **EEG-Based Emotion Recognition Using Regularized Graph Neural Networks**<br>*Peixiang Zhong, Di Wang, Chunyan Mi...* | IEEE Transactions on Affective Computing | 896 | 🌐 Link bài báo Open Access |
| `OA_KW4_034` | **2020** | **Virtual Reality with 360-Video Storytelling in Cultural Heritage: Study of Presence, Engagement, and Immersion**<br>*Filip Škola, Selma Rizvić, Marco Co...* | Sensors | 174 | 🌐 Link bài báo Open Access |
| `OA_KW4_035` | **2022** | **Automatic autism spectrum disorder detection using artificial intelligence methods with MRI neuroimaging: A review**<br>*Parisa Moridian, Navid Ghassemi, Ma...* | Frontiers in Molecular Neuroscience | 124 | 🌐 Link bài báo Open Access |
| `OA_KW4_036` | **2024** | **CTNet: a convolutional transformer network for EEG-based motor imagery classification**<br>*Wei Zhao, Xiaolu Jiang, Baocan Zhan...* | Scientific Reports | 172 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_037` | **2023** | **A paradigm shift in translational psychiatry through rodent neuroethology**<br>*Yair Shemesh, Alon Chen* | Molecular Psychiatry | 132 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_038` | **2023** | **A Spiking Neural Network With Adaptive Graph Convolution and LSTM for EEG-Based Brain-Computer Interfaces**<br>*Peiliang Gong, Pengpai Wang, Yueyin...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 105 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_039` | **2025** | **Transformers in EEG Analysis: A Review of Architectures and Applications in Motor Imagery, Seizure, and Emotion Classification**<br>*Elnaz Vafaei, Mohammad Hosseini* | Sensors | 104 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_040` | **2023** | **Multi-view domain-adaptive representation learning for EEG-based emotion recognition**<br>*Chao Li, Ning Bian, Ziping Zhao, Ha...* | Information Fusion | 89 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW4_041` | **2023** | **EEG-Based BCIs on Motor Imagery Paradigm Using Wearable Technologies: A Systematic Review**<br>*Aurora Saibene, Mirko Caglioni, Sil...* | Sensors | 82 | 🌐 Link bài báo Open Access |
| `OA_KW4_042` | **2023** | **Cognitive workload estimation using physiological measures: a review**<br>*Debashis Das Chakladar, Partha Prat...* | Cognitive Neurodynamics | 76 | 🌐 Link bài báo Open Access |
| `OA_KW4_043` | **2024** | **Workplace Well-Being in Industry 5.0: A Worker-Centered Systematic Review**<br>*Francesca Giada Antonaci, Elena Car...* | Sensors | 73 | 🌐 Link bài báo Open Access |
| `OA_KW4_044` | **2023** | **TS-GAN: Time-series GAN for Sensor-based Health Data Augmentation**<br>*Zhenyu Yang, Yantao Li, Gang Zhou* | ACM Transactions on Computing for Healthcare | 70 | 🌐 Link bài báo Open Access |
| `OA_KW4_045` | **2023** | **Neural Applications Using Immersive Virtual Reality: A Review on EEG Studies**<br>*Jin Woo Choi, Haram Kwon, Jae-Hoon ...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 69 | 🌐 Link bài báo Open Access |
| `OA_KW4_046` | **2024** | **Thermally Conductive and UV-EMI Shielding Electronic Textiles for Unrestricted and Multifaceted Health Monitoring**<br>*Yidong Peng, Jiancheng Dong, Jiayan...* | Nano-Micro Letters | 68 | 🌐 Link bài báo Open Access |
| `OA_KW4_047` | **2023** | **Detection of Driver Cognitive Distraction Using Machine Learning Methods**<br>*Apurva Misra, Siby Samuel, Shi Cao,...* | IEEE Access | 66 | 🌐 Link bài báo Open Access |


---

## 2. Bộ Prompt Master Class (Google NotebookLM) Theo Chuẩn 20 Tiêu Chí

Dưới đây là 7 Prompts chuyên dụng được thiết kế riêng cho **Notebook 04: Shared-Private Subspace Disentanglement & Cross-Subject Generalization**. Bạn chỉ cần tải các bài báo/tài liệu trong thư mục này lên Google NotebookLM ([https://notebooklm.google.com/](https://notebooklm.google.com/)) và dán lần lượt các prompt bên dưới:

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
- **Tài liệu này phục vụ trực tiếp cho**: Chương 3 & Chương 5 (Phân tách Biểu diễn & Thử nghiệm Tổng quát hóa LOSO).
- **Kết quả bóc tách từ NotebookLM**: Copy trực tiếp vào các mục tương ứng trong Luận án và bản thảo bài báo Journal IEEE TAFFC.
