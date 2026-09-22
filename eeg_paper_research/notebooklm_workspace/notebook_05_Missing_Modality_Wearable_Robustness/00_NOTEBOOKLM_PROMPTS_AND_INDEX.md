# Notebook 05: Missing-Modality Inpainting, Wearable Montage Decay & Noise Robustness
**Chủ đề Tiếng Việt**: Độ bền vững khi Khuyết thiếu Cảm biến, Suy thoái Kênh đo & Nhiễu Thực tế  
**Chương Luận án liên kết**: **Chương 5 (Thực nghiệm Bền vững, Rớt cảm biến & Đo kiểm Độ trễ Biên)**  
**Trọng tâm nghiên cứu**: Zero-shot sensor dropouts, latent cross-modal inpainting, spherical spline interpolation (32->14->4 ch), Gaussian/EMG noise injection, and sub-12ms real-time latency.  

---

## 1. Danh mục Toàn bộ Bài báo Khoa học trong Notebook này (50 bài)

| ID | Năm | Tiêu đề bài báo | Nơi công bố / Tạp chí | Trích dẫn | Tình trạng Tài liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW5_001` | **2023** | **Generative adversarial networks in EEG analysis: an overview**<br>*Ahmed G. Habashi, Ahmed M. Azab, Se...* | Journal of NeuroEngineering and Rehabilitation | 124 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_002` | **2023** | **Virtual nature, psychological and psychophysiological outcomes: A systematic review**<br>*Giuseppina Spano, Annalisa Theodoro...* | Journal of Environmental Psychology | 119 | 🌐 Link bài báo Open Access |
| `OA_KW5_003` | **2025** | **A review on EEG-based multimodal learning for emotion recognition**<br>*Rajasekhar Pillalamarri, S. Udhayak...* | Artificial Intelligence Review | 117 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_004` | **2023** | **State-of-the-Art of Stress Prediction from Heart Rate Variability Using Artificial Intelligence**<br>*Yeaminul Haque, Rahat Shahriar Zawa...* | Cognitive Computation | 107 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_005` | **2023** | **Transformer-Based Self-Supervised Multimodal Representation Learning for Wearable Emotion Recognition**<br>*Yujin Wu, Mohamed Daoudi, Ali Amad* | IEEE Transactions on Affective Computing | 106 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_006` | **2023** | **An interpretable machine learning approach to multimodal stress detection in a simulated office environment**<br>*Mara Naegelin, Raphael P. Weibel, J...* | Journal of Biomedical Informatics | 81 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_007` | **2024** | **Machine learning for human emotion recognition: a comprehensive review**<br>*Eman M. G. Younis, Someya Mohsen, E...* | Neural Computing and Applications | 75 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_008` | **2024** | **Multimodal Emotion Recognition Using Visual, Vocal and Physiological Signals: A Review**<br>*Gustave Udahemuka, Karim Djouani, A...* | Applied Sciences | 74 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_009` | **2024** | **Personalized Stress Detection Using Biosignals from Wearables: A Scoping Review**<br>*Marco Bolpagni, Susanna Pardini, Ma...* | Sensors | 57 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_010` | **2023** | **Reducing Stress with Yoga: A Systematic Review Based on Multimodal Biosignals**<br>*Aayushi Khajuria, Amit Kumar, Deepa...* | International Journal of Yoga | 50 | 🌐 Link bài báo Open Access |
| `OA_KW5_011` | **2023** | **Machine learning in biosignals processing for mental health: A narrative review**<br>*Elena Sajno, Sabrina Bartolotta, Co...* | Frontiers in Psychology | 43 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_012` | **2023** | **Augmenting ECG Data with Multiple Filters for a Better Emotion Recognition System**<br>*Muhammad Anas Hasnul, Nor Azlina Ab...* | Arabian Journal for Science and Engineering | 39 | 🌐 Link bài báo Open Access |
| `OA_KW5_013` | **2023** | **Evaluating Multimodal Wearable Sensors for Quantifying Affective States and Depression With Neural Networks**<br>*Abdullah Ahmed, Jayroop Ramesh, San...* | IEEE Sensors Journal | 36 | 🌐 Link bài báo Open Access |
| `OA_KW5_014` | **2025** | **A recent advances on autism spectrum disorders in diagnosing based on machine learning and deep learning**<br>*Hajir Ammar Hatim, Zaid Abdi Alkare...* | Artificial Intelligence Review | 35 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_015` | **2024** | **Wearable Solutions Using Physiological Signals for Stress Monitoring on Individuals with Autism Spectrum Disorder (ASD): A Systematic Literature Review**<br>*Sandra Cano, Claudio Cubillos, Rodr...* | Sensors | 35 | 🌐 Link bài báo Open Access |
| `OA_KW5_016` | **2025** | **Mapping EEG Metrics to Human Affective and Cognitive Models: An Interdisciplinary Scoping Review from a Cognitive Neuroscience Perspective**<br>*Evgenia Gkintoni, Constantinos Halk...* | Biomimetics | 30 | 🌐 Link bài báo Open Access |
| `OA_KW5_017` | **2023** | **Emotion recognition and artificial intelligence: A systematic review (2014–2023) and research recommendations**<br>*Smith K. Khare, Victoria Blanes‐Vid...* | Information Fusion | 462 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_018` | **2023** | **Generalizable machine learning for stress monitoring from wearable devices: A systematic literature review**<br>*Gideon Vos, Kelly Trinh, Zóltan Sar...* | International Journal of Medical Informatics | 160 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_019` | **2024** | **Role of machine learning and deep learning techniques in EEG-based BCI emotion recognition system: a review**<br>*Priyadarsini Samal, Mohammad Farukh...* | Artificial Intelligence Review | 147 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_020` | **2025** | **From Neural Networks to Emotional Networks: A Systematic Review of EEG-Based Emotion Recognition in Cognitive Neuroscience and Real-World Applications**<br>*Evgenia Gkintoni, Anthimos Aroutzid...* | Brain Sciences | 144 | 🌐 Link bài báo Open Access |
| `OA_KW5_021` | **2023** | **Deep Learning in EEG-Based BCIs: A Comprehensive Review of Transformer Models, Advantages, Challenges, and Applications**<br>*Berdakh Abibullaev, Aigerim Keutaye...* | IEEE Access | 136 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_022` | **2023** | **Deep learning-based EEG emotion recognition: Current trends and future perspectives**<br>*Xiaohu Wang, Yongmei Ren, Ze Luo, W...* | Frontiers in Psychology | 133 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_023` | **2023** | **Emotion Recognition Using Different Sensors, Emotion Models, Methods and Datasets: A Comprehensive Review**<br>*Yujian Cai, Xingguang Li, Jinsong L...* | Sensors | 133 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_024` | **2023** | **Affective Computing: Recent Advances, Challenges, and Future Trends**<br>*Guanxiong Pei, Haiying Li, Yandi Lu...* | Intelligent Computing | 132 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_025` | **2023** | **Electrocardiogram Monitoring Wearable Devices and Artificial-Intelligence-Enabled Diagnostic Capabilities: A Review**<br>*Luca Neri, Matt T. Oberdier, Kirste...* | Sensors | 132 | 🌐 Link bài báo Open Access |
| `OA_KW5_026` | **2023** | **Approaches, Applications, and Challenges in Physiological Emotion Recognition—A Tutorial Overview**<br>*Yekta Said Can, Bhargavi Mahesh, El...* | Proceedings of the IEEE | 73 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_027` | **2025** | **Conversational health agents: a personalized large language model-powered agent framework**<br>*Mahyar Abbasian, Iman Azimi, Amir M...* | JAMIA Open | 41 | 🌐 Link bài báo Open Access |
| `OA_KW5_028` | **2024** | **Early detection of cardiorespiratory complications and training monitoring using wearable ECG sensors and CNN**<br>*HongYuan Lu, XinMiao Feng, Jing Zha...* | BMC Medical Informatics and Decision Making | 24 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_029` | **2019** | **Emotion Recognition from Physiological Signal Analysis: A Review**<br>*Maria Egger, Matthias Ley, Sten Han...* | Electronic Notes in Theoretical Computer Science | 561 | 🌐 Link bài báo Open Access |
| `OA_KW5_030` | **2020** | **Development of a Real-Time Emotion Recognition System Using Facial Expressions and EEG based on machine learning and deep neural network methods**<br>*Aya Hassouneh, A. M. Mutawa, M. Mur...* | Informatics in Medicine Unlocked | 276 | 🌐 Link bài báo Open Access |
| `OA_KW5_031` | **2019** | **Wearable-Based Affect Recognition—A Review**<br>*Philip Schmidt, Attila Reiss, Rober...* | Sensors | 223 | 🌐 Link bài báo Open Access |
| `OA_KW5_032` | **2022** | **Emotion Recognition for Everyday Life Using Physiological Signals From Wearables: A Systematic Literature Review**<br>*Stanisław Saganowski, Bartosz Perz,...* | IEEE Transactions on Affective Computing | 206 | 🌐 Link bài báo Open Access |
| `OA_KW5_033` | **2021** | **Trends in Heart-Rate Variability Signal Analysis**<br>*Syem Ishaque, Naimul Khan, Sridhar ...* | Frontiers in Digital Health | 160 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_034` | **2020** | **Advances in Multimodal Emotion Recognition Based on Brain–Computer Interfaces**<br>*Zhipeng He, Zina Li, Fuzhou Yang, L...* | Brain Sciences | 153 | 🌐 Link bài báo Open Access |
| `OA_KW5_035` | **2019** | **Electronic Skin: Recent Progress and Future Prospects for Skin‐Attachable Devices for Health Monitoring, Robotics, and Prosthetics**<br>*Jun Chang Yang, Jaewan Mun, Se Youn...* | Advanced Materials | 1660 | 🌐 Link bài báo Open Access |
| `OA_KW5_036` | **2024** | **Exploring contactless techniques in multimodal emotion recognition: insights into diverse applications, challenges, solutions, and prospects**<br>*Umair Ali Khan, Qianru Xu, Yang Liu...* | Multimedia Systems | 56 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_037` | **2025** | **Integrating artificial intelligence with nanodiagnostics for early detection and precision management of neurodegenerative diseases**<br>*Youssef M. Hassan, Ahmed Wanas, Aya...* | Journal of Nanobiotechnology | 34 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_038` | **2025** | **Trends and Challenges in Real-Time Stress Detection and Modulation: The Role of the IoT and Artificial Intelligence**<br>*Manuel Paniagua-Gómez, Manuel F. Fe...* | Electronics | 27 | 🌐 Link bài báo Open Access |
| `OA_KW5_039` | **2025** | **POC Sensor Systems and Artificial Intelligence—Where We Are Now and Where We Are Going?**<br>*K. Prashanthi, Krishna Mohan Kovur,...* | Biosensors | 19 | 🌐 Link bài báo Open Access |
| `OA_KW5_040` | **2024** | **Effect of Interruptions and Cognitive Demand on Mental Workload: A Critical Review**<br>*Nitin Koundal, Abdualrhman Abdalhad...* | IEEE Access | 17 | 🌐 Link bài báo Open Access |
| `OA_KW5_041` | **2024** | **Biomarker discovery using machine learning in the psychosis spectrum**<br>*Walid Yassin, Kendra M Loedige, Cas...* | Biomarkers in Neuropsychiatry | 10 | 🌐 Link bài báo Open Access |
| `OA_KW5_042` | **2026** | **Universal Time-Series Representation Learning: A Survey**<br>*Patara Trirat, Yooju Shin, Jun-Hyeo...* | ACM Computing Surveys | 9 | 🌐 Link bài báo Open Access |
| `OA_KW5_043` | **2026** | **IoT‑Enabled Multimodal Approach for Low‑Latency Prediction of Elite Athlete Performance Dynamics**<br>*Mensah Sitti, Prince James Adeti* | International Journal of Physical Education Fitness and Sports | 7 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_044` | **2025** | **FatigueNet: A hybrid graph neural network and transformer framework for real-time multimodal fatigue detection**<br>*Seyyed Ali Zendehbad, Jamal Ghasemi...* | Scientific Reports | 7 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_045` | **2026** | **Generative Adversarial Networks for Modeling Bio-Electric Fields in Medicine: A Review of EEG, ECG, EMG, and EOG Applications**<br>*Jiaqi Liang, Yuheng Zhou, K. Ma, Yi...* | Bioengineering | 6 | 🌐 Link bài báo Open Access |
| `OA_KW5_046` | **2024** | **A Comprehensive Survey on Emerging Techniques and Fusion Technologies in Spatio-Temporal EEG Data Analysis**<br>*Pengfei Wang, Huanran Zheng, Silong...* | Chinese journal of information fusion. | 6 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_047` | **2026** | **Examining the Use of Consumer Wearable Devices and Digital Tools for Stress Measurement in College Students: Scoping Review of Methods**<br>*Aarti Sathyanarayana, Ohida Binte A...* | JMIR mhealth and uhealth | 2 | 🌐 Link bài báo Open Access |
| `OA_KW5_048` | **2025** | **AI-ENABLED NEUROBIOLOGICAL DIAGNOSTIC MODELS FOR EARLY DETECTION OF PTSD AND TRAUMA DISORDERS**<br>*Md. Akbar Hossain, Sharmin Ara* | American Journal of Interdisciplinary Studies | 2 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_049` | **2025** | **A hypergraph convolution-based intelligent healthcare platform for aging population management**<br>*Wenjie Li, Bing Hou, Xiaoxiao Wang* | Frontiers in Public Health | 1 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW5_050` | **2024** | **A Survey of Spatio-Temporal EEG data Analysis: from Models to Applications**<br>*Pengfei Wang, Huanran Zheng, Silong...* | arXiv (Cornell University) | 1 | 📄 Có sẵn PDF trong thư mục |


---

## 2. Bộ Prompt Master Class (Google NotebookLM) Theo Chuẩn 20 Tiêu Chí

Dưới đây là 7 Prompts chuyên dụng được thiết kế riêng cho **Notebook 05: Missing-Modality Inpainting, Wearable Montage Decay & Noise Robustness**. Bạn chỉ cần tải các bài báo/tài liệu trong thư mục này lên Google NotebookLM ([https://notebooklm.google.com/](https://notebooklm.google.com/)) và dán lần lượt các prompt bên dưới:

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
- **Tài liệu này phục vụ trực tiếp cho**: Chương 5 (Thực nghiệm Bền vững, Rớt cảm biến & Đo kiểm Độ trễ Biên).
- **Kết quả bóc tách từ NotebookLM**: Copy trực tiếp vào các mục tương ứng trong Luận án và bản thảo bài báo Journal IEEE TAFFC.
