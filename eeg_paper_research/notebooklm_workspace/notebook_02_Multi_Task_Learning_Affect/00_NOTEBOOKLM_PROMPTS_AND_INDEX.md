# Notebook 02: Multi-Task Learning & Homoscedastic Uncertainty Balancing
**Chủ đề Tiếng Việt**: Học Đa Nhiệm Vụ & Cân bằng Mất mát theo Độ bất định Đồng phương sai  
**Chương Luận án liên kết**: **Chương 3 & Chương 6 (Kiến trúc Đề xuất MMB-EmotionNet & Kiểm định Đa nhiệm vụ)**  
**Trọng tâm nghiên cứu**: Joint continuous regression (Valence, Arousal) and discrete classification, gradient conflict resolution, Kendall's homoscedastic uncertainty loss, and negative transfer mitigation.  

---

## 1. Danh mục Toàn bộ Bài báo Khoa học trong Notebook này (43 bài)

| ID | Năm | Tiêu đề bài báo | Nơi công bố / Tạp chí | Trích dẫn | Tình trạng Tài liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW2_001` | **2023** | **Emotion recognition and artificial intelligence: A systematic review (2014–2023) and research recommendations**<br>*Smith K. Khare, Victoria Blanes‐Vid...* | Information Fusion | 462 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_002` | **2023** | **LGGNet: Learning From Local-Global-Graph Representations for Brain–Computer Interface**<br>*Yi Ding, Neethu Robinson, Chengxuan...* | IEEE Transactions on Neural Networks and Learning Systems | 194 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_003` | **2024** | **Role of machine learning and deep learning techniques in EEG-based BCI emotion recognition system: a review**<br>*Priyadarsini Samal, Mohammad Farukh...* | Artificial Intelligence Review | 147 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_004` | **2023** | **Deep Learning in EEG-Based BCIs: A Comprehensive Review of Transformer Models, Advantages, Challenges, and Applications**<br>*Berdakh Abibullaev, Aigerim Keutaye...* | IEEE Access | 136 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_005` | **2023** | **Deep learning-based EEG emotion recognition: Current trends and future perspectives**<br>*Xiaohu Wang, Yongmei Ren, Ze Luo, W...* | Frontiers in Psychology | 133 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_006` | **2023** | **Emotion Recognition Using Different Sensors, Emotion Models, Methods and Datasets: A Comprehensive Review**<br>*Yujian Cai, Xingguang Li, Jinsong L...* | Sensors | 133 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_007` | **2023** | **Affective Computing: Recent Advances, Challenges, and Future Trends**<br>*Guanxiong Pei, Haiying Li, Yandi Lu...* | Intelligent Computing | 132 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_008` | **2023** | **Generative adversarial networks in EEG analysis: an overview**<br>*Ahmed G. Habashi, Ahmed M. Azab, Se...* | Journal of NeuroEngineering and Rehabilitation | 124 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_009` | **2023** | **Multimodal Emotion Recognition From EEG Signals and Facial Expressions**<br>*Shuai Wang, Jingzi Qu, Yong Zhang, ...* | IEEE Access | 123 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_010` | **2023** | **Multimodal Emotion Recognition Based on Facial Expressions, Speech, and EEG**<br>*Jiahui Pan, Weijie Fang, Zhihang Zh...* | IEEE Open Journal of Engineering in Medicine and Biology | 119 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_011` | **2025** | **A review on EEG-based multimodal learning for emotion recognition**<br>*Rajasekhar Pillalamarri, S. Udhayak...* | Artificial Intelligence Review | 117 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_012` | **2023** | **Review of Studies on Emotion Recognition and Judgment Based on Physiological Signals**<br>*Wenqian Lin, Chao Li* | Applied Sciences | 116 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_013` | **2023** | **EEGformer: A transformer–based brain activity classification method using EEG signal**<br>*Zhijiang Wan, Manyu Li, Shichang Li...* | Frontiers in Neuroscience | 108 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_014` | **2023** | **Self-Supervised EEG Emotion Recognition Models Based on CNN**<br>*Xingyi Wang, Yuliang Ma, Jared Camm...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 108 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_015` | **2023** | **Transformer-Based Self-Supervised Multimodal Representation Learning for Wearable Emotion Recognition**<br>*Yujin Wu, Mohamed Daoudi, Ali Amad* | IEEE Transactions on Affective Computing | 106 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_016` | **2024** | **Review of Stress Detection Methods Using Wearable Sensors**<br>*Georgios V. Taskasaplidis, Dimitris...* | IEEE Access | 105 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_017` | **2023** | **A Spiking Neural Network With Adaptive Graph Convolution and LSTM for EEG-Based Brain-Computer Interfaces**<br>*Peiliang Gong, Pengpai Wang, Yueyin...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 105 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_018` | **2025** | **Transformers in EEG Analysis: A Review of Architectures and Applications in Motor Imagery, Seizure, and Emotion Classification**<br>*Elnaz Vafaei, Mohammad Hosseini* | Sensors | 104 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_019` | **2023** | **The transformative power of music: Insights into neuroplasticity, health, and disease**<br>*Muriel Tahtouh Zaatar, Kenda Alhaki...* | Brain Behavior & Immunity - Health | 102 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_020` | **2023** | **A Large Finer-grained Affective Computing EEG Dataset**<br>*Jingjing Chen, Xiaobin Wang, Chen H...* | Scientific Data | 98 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_021` | **2023** | **Stress and Workload Assessment in Aviation—A Narrative Review**<br>*Giulia Masi, Gianluca Amprimo, Clau...* | Sensors | 97 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_022` | **2023** | **Multi-view domain-adaptive representation learning for EEG-based emotion recognition**<br>*Chao Li, Ning Bian, Ziping Zhao, Ha...* | Information Fusion | 89 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_023` | **2024** | **A comprehensive review of deep learning in EEG-based emotion recognition: classifications, trends, and practical implications**<br>*Weizhi Ma, Yujia Zheng, Tianhao Li,...* | PeerJ Computer Science | 87 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_024` | **2023** | **The now and future of ChatGPT and GPT in psychiatry**<br>*Szu‐Wei Cheng, Chung‐Wen Chang, Wan...* | Psychiatry and Clinical Neurosciences | 198 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_025` | **2023** | **DICE-Net: A Novel Convolution-Transformer Architecture for Alzheimer Detection in EEG Signals**<br>*Ανδρέας Μιλτιάδους, Emmanouil Giona...* | IEEE Access | 196 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_026` | **2023** | **Generalizable machine learning for stress monitoring from wearable devices: A systematic literature review**<br>*Gideon Vos, Kelly Trinh, Zóltan Sar...* | International Journal of Medical Informatics | 160 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_027` | **2023** | **An interpretable machine learning approach to multimodal stress detection in a simulated office environment**<br>*Mara Naegelin, Raphael P. Weibel, J...* | Journal of Biomedical Informatics | 81 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_028` | **2023** | **Multimodal Hierarchical CNN Feature Fusion for Stress Detection**<br>*Radhika Kuttala, Ramanathan Subrama...* | IEEE Access | 79 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_029` | **2024** | **Machine learning for human emotion recognition: a comprehensive review**<br>*Eman M. G. Younis, Someya Mohsen, E...* | Neural Computing and Applications | 75 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_030` | **2024** | **Multimodal Emotion Recognition Using Visual, Vocal and Physiological Signals: A Review**<br>*Gustave Udahemuka, Karim Djouani, A...* | Applied Sciences | 74 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_031` | **2023** | **Approaches, Applications, and Challenges in Physiological Emotion Recognition—A Tutorial Overview**<br>*Yekta Said Can, Bhargavi Mahesh, El...* | Proceedings of the IEEE | 73 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_032` | **2024** | **Personalized Stress Detection Using Biosignals from Wearables: A Scoping Review**<br>*Marco Bolpagni, Susanna Pardini, Ma...* | Sensors | 57 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_033` | **2025** | **A recent advances on autism spectrum disorders in diagnosing based on machine learning and deep learning**<br>*Hajir Ammar Hatim, Zaid Abdi Alkare...* | Artificial Intelligence Review | 35 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_034` | **2024** | **Emerging Frontiers in Human–Robot Interaction**<br>*Farshad Safavi, Parthan Olikkal, Di...* | Journal of Intelligent & Robotic Systems | 31 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_035` | **2023** | **A Narrative Review of Speech and EEG Features for Schizophrenia Detection: Progress and Challenges**<br>*Felipe Teixeira, Miguel Rocha e Cos...* | Bioengineering | 31 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_036` | **2024** | **Integrating artificial intelligence to assess emotions in learning environments: a systematic literature review**<br>*Angel Olider Rojas Vistorte, Ángel ...* | Frontiers in Psychology | 271 | 🌐 Link bài báo Open Access |
| `OA_KW2_037` | **2023** | **TMS combined with EEG: Recommendations and open issues for data collection and analysis**<br>*Julio C. Hernandez-Pavon, Domenica ...* | Brain stimulation | 251 | 🌐 Link bài báo Open Access |
| `OA_KW2_038` | **2023** | **Electrocardiogram Monitoring Wearable Devices and Artificial-Intelligence-Enabled Diagnostic Capabilities: A Review**<br>*Luca Neri, Matt T. Oberdier, Kirste...* | Sensors | 132 | 🌐 Link bài báo Open Access |
| `OA_KW2_039` | **2023** | **State-of-the-Art of Stress Prediction from Heart Rate Variability Using Artificial Intelligence**<br>*Yeaminul Haque, Rahat Shahriar Zawa...* | Cognitive Computation | 107 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_040` | **2023** | **Automatic stress detection in car drivers based on non-invasive physiological signals using machine learning techniques**<br>*Ali I. Siam, Samah A. Gamel, Fatma ...* | Neural Computing and Applications | 103 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW2_041` | **2023** | **Multimodal Human–Robot Interaction for Human‐Centric Smart Manufacturing: A Survey**<br>*Tian Wang, Pai Zheng, Shufei Li, Li...* | Advanced Intelligent Systems | 187 | 🌐 Link bài báo Open Access |
| `OA_KW2_042` | **2023** | **Improving the study of brain-behavior relationships by revisiting basic assumptions**<br>*Christiana Westlin, Jordan E. Theri...* | Trends in Cognitive Sciences | 170 | 🌐 Link bài báo Open Access |
| `OA_KW2_043` | **2023** | **Deep learning and machine learning in psychiatry: a survey of current progress in depression detection, diagnosis and treatment**<br>*Matthew Squires, Xiaohui Tao, Soman...* | Brain Informatics | 157 | 📄 Có sẵn PDF trong thư mục |


---

## 2. Bộ Prompt Master Class (Google NotebookLM) Theo Chuẩn 20 Tiêu Chí

Dưới đây là 7 Prompts chuyên dụng được thiết kế riêng cho **Notebook 02: Multi-Task Learning & Homoscedastic Uncertainty Balancing**. Bạn chỉ cần tải các bài báo/tài liệu trong thư mục này lên Google NotebookLM ([https://notebooklm.google.com/](https://notebooklm.google.com/)) và dán lần lượt các prompt bên dưới:

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
- **Tài liệu này phục vụ trực tiếp cho**: Chương 3 & Chương 6 (Kiến trúc Đề xuất MMB-EmotionNet & Kiểm định Đa nhiệm vụ).
- **Kết quả bóc tách từ NotebookLM**: Copy trực tiếp vào các mục tương ứng trong Luận án và bản thảo bài báo Journal IEEE TAFFC.
