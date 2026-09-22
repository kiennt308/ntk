# Notebook 01: Multimodal EEG & Peripheral Biosignals (EEG, ECG, EDA, PPG, Respiration)
**Chủ đề Tiếng Việt**: Nền tảng Tín hiệu Não (EEG) và Tín hiệu Sinh lý Tự chủ (ECG, EDA)  
**Chương Luận án liên kết**: **Chương 2 & Chương 4 (Tổng quan Sinh học Thần kinh & Giao thức Dữ liệu)**  
**Trọng tâm nghiên cứu**: Cortical cognitive appraisal vs. Autonomic physiological arousal, DEAP/DREAMER benchmarks, signal filtering, CAR, and HRV/CDA feature extraction.  

---

## 1. Danh mục Toàn bộ Bài báo Khoa học trong Notebook này (50 bài)

| ID | Năm | Tiêu đề bài báo | Nơi công bố / Tạp chí | Trích dẫn | Tình trạng Tài liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW1_001` | **2023** | **Generalizable machine learning for stress monitoring from wearable devices: A systematic literature review**<br>*Gideon Vos, Kelly Trinh, Zóltan Sar...* | International Journal of Medical Informatics | 160 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_002` | **2024** | **Role of machine learning and deep learning techniques in EEG-based BCI emotion recognition system: a review**<br>*Priyadarsini Samal, Mohammad Farukh...* | Artificial Intelligence Review | 147 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_003` | **2023** | **Emotion Recognition Using Different Sensors, Emotion Models, Methods and Datasets: A Comprehensive Review**<br>*Yujian Cai, Xingguang Li, Jinsong L...* | Sensors | 133 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_004` | **2025** | **A review on EEG-based multimodal learning for emotion recognition**<br>*Rajasekhar Pillalamarri, S. Udhayak...* | Artificial Intelligence Review | 117 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_005` | **2023** | **Review of Studies on Emotion Recognition and Judgment Based on Physiological Signals**<br>*Wenqian Lin, Chao Li* | Applied Sciences | 116 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_006` | **2023** | **State-of-the-Art of Stress Prediction from Heart Rate Variability Using Artificial Intelligence**<br>*Yeaminul Haque, Rahat Shahriar Zawa...* | Cognitive Computation | 107 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_007` | **2023** | **Transformer-Based Self-Supervised Multimodal Representation Learning for Wearable Emotion Recognition**<br>*Yujin Wu, Mohamed Daoudi, Ali Amad* | IEEE Transactions on Affective Computing | 106 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_008` | **2024** | **Review of Stress Detection Methods Using Wearable Sensors**<br>*Georgios V. Taskasaplidis, Dimitris...* | IEEE Access | 105 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_009` | **2023** | **An interpretable machine learning approach to multimodal stress detection in a simulated office environment**<br>*Mara Naegelin, Raphael P. Weibel, J...* | Journal of Biomedical Informatics | 81 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_010` | **2024** | **Predicting stress levels using physiological data: Real-time stress prediction models utilizing wearable devices**<br>*Evgenia Lazarou, Themis P. Exarchos* | AIMS neuroscience | 79 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_011` | **2023** | **Multimodal Hierarchical CNN Feature Fusion for Stress Detection**<br>*Radhika Kuttala, Ramanathan Subrama...* | IEEE Access | 79 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_012` | **2024** | **Machine learning for human emotion recognition: a comprehensive review**<br>*Eman M. G. Younis, Someya Mohsen, E...* | Neural Computing and Applications | 75 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_013` | **2023** | **Stress monitoring using wearable sensors: IoT techniques in medical field**<br>*Fatma M. Talaat, Rana Mohamed El-Ba...* | Neural Computing and Applications | 75 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_014` | **2024** | **Detection and monitoring of stress using wearables: a systematic review**<br>*Anuja Pinge, Vinaya R. Gad, Dheryta...* | Frontiers in Computer Science | 74 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_015` | **2024** | **Multimodal Emotion Recognition Using Visual, Vocal and Physiological Signals: A Review**<br>*Gustave Udahemuka, Karim Djouani, A...* | Applied Sciences | 74 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_016` | **2023** | **Approaches, Applications, and Challenges in Physiological Emotion Recognition—A Tutorial Overview**<br>*Yekta Said Can, Bhargavi Mahesh, El...* | Proceedings of the IEEE | 73 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_017` | **2023** | **Comprehensive Analysis of Feature Extraction Methods for Emotion Recognition from Multichannel EEG Recordings**<br>*Rajamanickam Yuvaraj, Prasanth Thag...* | Sensors | 73 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_018` | **2024** | **Personalized Stress Detection Using Biosignals from Wearables: A Scoping Review**<br>*Marco Bolpagni, Susanna Pardini, Ma...* | Sensors | 57 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_019` | **2023** | **Analyzing psychophysical state and cognitive performance in human-robot collaboration for repetitive assembly processes**<br>*Riccardo Gervasi, Matteo Capponi, L...* | Production Engineering | 56 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_020` | **2023** | **Deep Learning in EEG-Based BCIs: A Comprehensive Review of Transformer Models, Advantages, Challenges, and Applications**<br>*Berdakh Abibullaev, Aigerim Keutaye...* | IEEE Access | 136 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_021` | **2023** | **Deep learning-based EEG emotion recognition: Current trends and future perspectives**<br>*Xiaohu Wang, Yongmei Ren, Ze Luo, W...* | Frontiers in Psychology | 133 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_022` | **2023** | **Affective Computing: Recent Advances, Challenges, and Future Trends**<br>*Guanxiong Pei, Haiying Li, Yandi Lu...* | Intelligent Computing | 132 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_023` | **2023** | **Multimodal Emotion Recognition From EEG Signals and Facial Expressions**<br>*Shuai Wang, Jingzi Qu, Yong Zhang, ...* | IEEE Access | 123 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_024` | **2023** | **A Spiking Neural Network With Adaptive Graph Convolution and LSTM for EEG-Based Brain-Computer Interfaces**<br>*Peiliang Gong, Pengpai Wang, Yueyin...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 105 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_025` | **2023** | **Multi-view domain-adaptive representation learning for EEG-based emotion recognition**<br>*Chao Li, Ning Bian, Ziping Zhao, Ha...* | Information Fusion | 89 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_026` | **2025** | **Artificial Intelligence in Psychiatry: A Review of Biological and Behavioral Data Analyses**<br>*Ismail BAYDİLİ, Burak Taşçı, Gülay ...* | Diagnostics | 69 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_027` | **2024** | **Emotion recognition with EEG-based brain-computer interfaces: a systematic literature review**<br>*Kübra Erat, Elif Bilge Şahin, Furka...* | Multimedia Tools and Applications | 69 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_028` | **2023** | **An Investigation of Olfactory-Enhanced Video on EEG-Based Emotion Recognition**<br>*Minchao Wu, Wei Teng, Cunhang Fan, ...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 62 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_029` | **2023** | **A Model for EEG-Based Emotion Recognition: CNN-Bi-LSTM with Attention Mechanism**<br>*Zhentao Huang, Yahong Ma, Rongrong ...* | Electronics | 59 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_030` | **2023** | **EmotionKD: A Cross-Modal Knowledge Distillation Framework for Emotion Recognition Based on Physiological Signals**<br>*Yucheng Liu, Ziyu Jia, Haichao Wang* | Open Access Journal/Conference | 55 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_031` | **2023** | **A Novel Baseline Removal Paradigm for Subject-Independent Features in Emotion Classification Using EEG**<br>*Md. Zaved Iqubal Ahmed, Nidul Sinha...* | Bioengineering | 55 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_032` | **2023** | **Cross Dataset Analysis for Generalizability of HRV-Based Stress Detection Models**<br>*Mouna Benchekroun, Pedro Elkind Vel...* | Sensors | 54 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_033` | **2023** | **Developing a Physiological Signal-Based, Mean Threshold and Decision-Level Fusion Algorithm (PMD) for Emotion Recognition**<br>*Qiuju Zhang, Hongtao Zhang, Keming ...* | Tsinghua Science & Technology | 49 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_034` | **2024** | **Emotion Detection from EEG Signals Using Machine Deep Learning Models**<br>*João Vitor Marques Rabelo Fernandes...* | Bioengineering | 48 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_035` | **2023** | **ECG and EEG based detection and multilevel classification of stress using machine learning for specified genders: A preliminary study**<br>*Apit Hemakom, Danita Atiwiwat, Pasi...* | PLoS ONE | 44 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_036` | **2023** | **Machine learning in biosignals processing for mental health: A narrative review**<br>*Elena Sajno, Sabrina Bartolotta, Co...* | Frontiers in Psychology | 43 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_037` | **2023** | **Deep Learning Models for Stress Analysis in University Students: A Sudoku-Based Study**<br>*Qicheng Chen, Boon Giin Lee* | Sensors | 42 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_038` | **2023** | **A Graph Neural Network for EEG-Based Emotion Recognition With Contrastive Learning and Generative Adversarial Neural Network Data Augmentation**<br>*S. Soleimani Gilakjani, Hussein Al ...* | IEEE Access | 38 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_039` | **2023** | **K-EmoPhone: A Mobile and Wearable Dataset with In-Situ Emotion, Stress, and Attention Labels**<br>*Soowon Kang, Woohyeok Choi, Cheul Y...* | Scientific Data | 32 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_040` | **2023** | **Emotion recognition with multi-modal peripheral physiological signals**<br>*Jennifer Gohumpu, Mengru Xue, Yanch...* | Frontiers in Computer Science | 29 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_041` | **2023** | **Driver Stress Detection from Physiological Signals by Virtual Reality Simulator**<br>*Nuria Mateos-García, Ana Belén Gil ...* | Electronics | 29 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_042` | **2025** | **An ensemble deep learning framework for emotion recognition through wearable devices multi-modal physiological signals**<br>*Durgesh Nandini, Jyoti Yadav, Vijan...* | Scientific Reports | 28 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_043` | **2024** | **Review of EEG Affective Recognition with a Neuroscience Perspective**<br>*Rosary Yuting Lim, Wai-Cheong Linco...* | Brain Sciences | 28 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_044` | **2023** | **MGEED: A Multimodal Genuine Emotion and Expression Detection Database**<br>*Yiming Wang, Hui Yu, Weihong Gao, Y...* | IEEE Transactions on Affective Computing | 28 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_045` | **2023** | **PhyMER: Physiological Dataset for Multimodal Emotion Recognition With Personality as a Context**<br>*Sudarshan Pant, Hyung-Jeong Yang, E...* | IEEE Access | 24 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_046` | **2024** | **EmoWear: Wearable Physiological and Motion Dataset for Emotion Recognition and Context Awareness**<br>*Mohammad Hasan Rahmani, Michelle Sy...* | Scientific Data | 23 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_047` | **2025** | **Stress and Emotion Open Access Data: A Review on Datasets, Modalities, Methods, Challenges, and Future Research Perspectives**<br>*Aleksandr Ometov, Anzhelika Mezina,...* | Journal of Healthcare Informatics Research | 18 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_048` | **2024** | **Multimodal emotion recognition based on the fusion of vision, EEG, ECG, and EMG signals**<br>*Shripad Bhatlawande, Swati Shilaska...* | International journal of electrical and computer engineering systems | 17 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_049` | **2023** | **Real-Time Emotion Recognition Using Deep Learning Methods: Systematic Review**<br>*Muthana Alisawi, Nursel Yalçın* | Intelligent Methods in Engineering Sciences | 16 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW1_050` | **2025** | **Deep Learning-Based EEG Emotion Recognition: A Review**<br>*Y. H. Liu, Wenbo Xue, Li Yang, Meng...* | Brain Sciences | 9 | 📄 Có sẵn PDF trong thư mục |


---

## 2. Bộ Prompt Master Class (Google NotebookLM) Theo Chuẩn 20 Tiêu Chí

Dưới đây là 7 Prompts chuyên dụng được thiết kế riêng cho **Notebook 01: Multimodal EEG & Peripheral Biosignals (EEG, ECG, EDA, PPG, Respiration)**. Bạn chỉ cần tải các bài báo/tài liệu trong thư mục này lên Google NotebookLM ([https://notebooklm.google.com/](https://notebooklm.google.com/)) và dán lần lượt các prompt bên dưới:

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
- **Tài liệu này phục vụ trực tiếp cho**: Chương 2 & Chương 4 (Tổng quan Sinh học Thần kinh & Giao thức Dữ liệu).
- **Kết quả bóc tách từ NotebookLM**: Copy trực tiếp vào các mục tương ứng trong Luận án và bản thảo bài báo Journal IEEE TAFFC.
