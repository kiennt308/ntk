# Notebook 07: Dynamic Graph Neural Networks & Functional Brain Connectivity
**Chủ đề Tiếng Việt**: Mạng Nơ-ron Đồ thị Động (DGCNN, RGNN) & Liên kết Chức năng Vỏ não  
**Chương Luận án liên kết**: **Chương 2, 4 & 5 (Các Mô hình Đối sánh SOTA Đồ thị)**  
**Trọng tâm nghiên cứu**: Dynamic Graph CNN (DGCNN), Regularized GNN (RGNN), Phase Locking Value (PLV), spatial adjacency matrices over standard 10-20 electrode positions, and inter-hemispheric asymmetry.  

---

## 1. Danh mục Toàn bộ Bài báo Khoa học trong Notebook này (50 bài)

| ID | Năm | Tiêu đề bài báo | Nơi công bố / Tạp chí | Trích dẫn | Tình trạng Tài liệu |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW7_001` | **2023** | **LGGNet: Learning From Local-Global-Graph Representations for Brain–Computer Interface**<br>*Yi Ding, Neethu Robinson, Chengxuan...* | IEEE Transactions on Neural Networks and Learning Systems | 194 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_002` | **2023** | **MSFR-GCN: A Multi-Scale Feature Reconstruction Graph Convolutional Network for EEG Emotion and Cognition Recognition**<br>*Deng Pan, Haohao Zheng, Feifan Xu, ...* | IEEE Transactions on Neural Systems and Rehabilitation Engineering | 93 | 🌐 Link bài báo Open Access |
| `OA_KW7_003` | **2023** | **STGATE: Spatial-temporal graph attention network with a transformer encoder for EEG-based emotion recognition**<br>*Jingcong Li, Weijian Pan, Haiyun Hu...* | Frontiers in Human Neuroscience | 72 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_004` | **2023** | **EEG-based emotion recognition using a temporal-difference minimizing neural network**<br>*Xiangyu Ju, Ming Li, Wenli Tian, De...* | Cognitive Neurodynamics | 57 | 🌐 Link bài báo Open Access |
| `OA_KW7_005` | **2023** | **Bi-Branch Vision Transformer Network for EEG Emotion Recognition**<br>*Wei Lu, Tien-Ping Tan, Hua Ma* | IEEE Access | 57 | 🌐 Link bài báo Open Access |
| `OA_KW7_006` | **2023** | **Emotion Recognition from Spatio-Temporal Representation of EEG Signals via 3D-CNN with Ensemble Learning Techniques**<br>*Rajamanickam Yuvaraj, Arapan Baranw...* | Brain Sciences | 53 | 🌐 Link bài báo Open Access |
| `OA_KW7_007` | **2023** | **Fractal Spiking Neural Network Scheme for EEG-Based Emotion Recognition**<br>*Wei Li, Cheng Fang, Zhihao Zhu, Chu...* | IEEE Journal of Translational Engineering in Health and Medicine | 44 | 🌐 Link bài báo Open Access |
| `OA_KW7_008` | **2023** | **Multimodal Adaptive Emotion Transformer with Flexible Modality Inputs on A Novel Dataset with Continuous Labels**<br>*Wei-Bang Jiang, Xuan-Hao Liu, Wei‐L...* | Open Access Journal | 43 | 🌐 Link bài báo Open Access |
| `OA_KW7_009` | **2024** | **DMMR: Cross-Subject Domain Generalization for EEG-Based Emotion Recognition via Denoising Mixed Mutual Reconstruction**<br>*Yiming Wang, Bin Zhang, Yujiao Tang* | Proceedings of the AAAI Conference on Artificial Intelligence | 41 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_010` | **2024** | **Attention-Based Temporal Graph Representation Learning for EEG-Based Emotion Recognition**<br>*Chao Li, Feng Wang, Ziping Zhao, Ha...* | IEEE Journal of Biomedical and Health Informatics | 39 | 🌐 Link bài báo Open Access |
| `OA_KW7_011` | **2024** | **Mini review: Challenges in EEG emotion recognition**<br>*Zhihui Zhang, Josep Maria Fort Mir,...* | Frontiers in Psychology | 38 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_012` | **2024** | **Subject-Independent Emotion Recognition Based on EEG Frequency Band Features and Self-Adaptive Graph Construction**<br>*Jinhao Zhang, Yanrong Hao, Xin Wen,...* | Brain Sciences | 37 | 🌐 Link bài báo Open Access |
| `OA_KW7_013` | **2023** | **A novel feature fusion network for multimodal emotion recognition from EEG and eye movement signals**<br>*Baole Fu, Chunrui Gu, M.W. Fu, Yuxi...* | Frontiers in Neuroscience | 34 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_014` | **2023** | **Emotion recognition based on convolutional gated recurrent units with attention**<br>*Zhu Ye, Yuan Jing, Q. Wang, Pengrui...* | Connection Science | 32 | 🌐 Link bài báo Open Access |
| `OA_KW7_015` | **2024** | **Adaptive neuro-fuzzy based hybrid classification model for emotion recognition from EEG signals**<br>*Fatma Kebire Bardak, Muhammet Nuri ...* | Neural Computing and Applications | 31 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_016` | **2024** | **EEG Emotion Recognition Network Based on Attention and Spatiotemporal Convolution**<br>*Xiaoliang Zhu, Chen Liu, Liang Zhao...* | Sensors | 29 | 🌐 Link bài báo Open Access |
| `OA_KW7_017` | **2024** | **Review of EEG Affective Recognition with a Neuroscience Perspective**<br>*Rosary Yuting Lim, Wai-Cheong Linco...* | Brain Sciences | 28 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_018` | **2024** | **A temporal-spectral graph convolutional neural network model for EEG emotion recognition within and across subjects**<br>*Rui Li, Xuanwen Yang, Jun Lou, Juns...* | Brain Informatics | 21 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_019` | **2024** | **A Local-Ascending-Global Learning Strategy for Brain-Computer Interface**<br>*Dongrui Gao, Haokai Zhang, Pengrui ...* | Proceedings of the AAAI Conference on Artificial Intelligence | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_020` | **2023** | **Modified Earthworm Optimization With Deep Learning Assisted Emotion Recognition for Human Computer Interface**<br>*Fadwa Alrowais, Noha Negm, Majdi Kh...* | IEEE Access | 20 | 🌐 Link bài báo Open Access |
| `OA_KW7_021` | **2024** | **A study on the combination of functional connection features and Riemannian manifold in EEG emotion recognition**<br>*Minchao Wu, Rui Ouyang, Chang Zhou,...* | Frontiers in Neuroscience | 19 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_022` | **2023** | **Multi-channel EEG emotion recognition through residual graph attention neural network**<br>*Chao Hao, Yiming Cao, Yongli Liu* | Frontiers in Neuroscience | 18 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_023` | **2025** | **Multi-branch convolutional neural network with cross-attention mechanism for emotion recognition**<br>*Fei Yan, Zekai Guo, Abdullah M. Ili...* | Scientific Reports | 17 | 🌐 Link bài báo Open Access |
| `OA_KW7_024` | **2023** | **Spatial–temporal features-based EEG emotion recognition using graph convolution network and long short-term memory**<br>*Fa Zheng, Bin Hu, Xiangwei Zheng, Y...* | Physiological Measurement | 13 | 🌐 Link bài báo Open Access |
| `OA_KW7_025` | **2026** | **Graph Neural Networks in EEG-Based Emotion Recognition: A Survey**<br>*Chenyu Liu, Yuqiu Deng, Yihao Wu, R...* | Lecture notes in computer science | 12 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_026` | **2025** | **Directional Spatial and Spectral Attention Network (DSSA Net) for EEG-based emotion recognition**<br>*Jiyao Liu, Lang He, Haifeng Chen, D...* | Frontiers in Neurorobotics | 12 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_027` | **2024** | **FC-TFS-CGRU: A Temporal–Frequency–Spatial Electroencephalography Emotion Recognition Model Based on Functional Connectivity and a Convolutional Gated Recurrent Unit Hybrid Architecture**<br>*Xia Wu, Yumei Zhang, Jingjing Li, H...* | Sensors | 12 | 🌐 Link bài báo Open Access |
| `OA_KW7_028` | **2023** | **Emotion Classification from Multi-Band Electroencephalogram Data Using Dynamic Simplifying Graph Convolutional Network and Channel Style Recalibration Module**<br>*Xiaoliang Zhu, Gendong Liu, Liang Z...* | Sensors | 11 | 🌐 Link bài báo Open Access |
| `OA_KW7_029` | **2024** | **Enhancing cross-subject emotion recognition precision through unimodal EEG: a novel emotion preceptor model**<br>*Yihang Dong, Changhong Jing, Mufti ...* | Brain Informatics | 10 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_030` | **2024** | **CIT-EmotionNet: convolution interactive transformer network for EEG emotion recognition**<br>*Wei Lu, Lingnan Xia, Tien-Ping Tan,...* | PeerJ Computer Science | 9 | 🌐 Link bài báo Open Access |
| `OA_KW7_031` | **2023** | **Emotion Recognition Using Narrowband Spatial Features of Electroencephalography**<br>*Iffat Farhana, Jungpil Shin, Shabbi...* | IEEE Access | 9 | 🌐 Link bài báo Open Access |
| `OA_KW7_032` | **2023** | **EEG-Based Emotion Recognition Using Spatial-Temporal Connectivity**<br>*Wenhao Chu, Baole Fu, Yuxiao Xia, Y...* | IEEE Access | 9 | 🌐 Link bài báo Open Access |
| `OA_KW7_033` | **2025** | **EEG Emotion Recognition Using AttGraph: A Multi-Dimensional Attention-Based Dynamic Graph Convolutional Network**<br>*Shuai Zhang, Chengxi Chu, Xin Zhang...* | Brain Sciences | 8 | 🌐 Link bài báo Open Access |
| `OA_KW7_034` | **2023** | **A Method for Classification and Evaluation of Pilot’s Mental States Based on CNN**<br>*Qianlei Wang, Zaijun Wang, Renhe Xi...* | Computer Systems Science and Engineering | 7 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_035` | **2025** | **Deep learning for electroencephalography emotion recognition**<br>*Hesamoddin Pourrostami, Mohammad M....* | AIMS Public Health | 6 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_036` | **2024** | **Set-pMAE: spatial-spEctral-temporal based parallel masked autoEncoder for EEG emotion recognition**<br>*Chenyu Pan, Huimin Lu, Chenglin Lin...* | Cognitive Neurodynamics | 6 | 🌐 Link bài báo Open Access |
| `OA_KW7_037` | **2024** | **VSGT: Variational Spatial and Gaussian Temporal Graph Models for EEG-based Emotion Recognition**<br>*Chenyu Liu, Xinliang Zhou, Jiaping ...* | Open Access Journal | 6 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_038` | **2024** | **GC-STCL: A Granger Causality-Based Spatial–Temporal Contrastive Learning Framework for EEG Emotion Recognition**<br>*Lei Wang, Siming Wang, Bo Jin, Xiao...* | Entropy | 6 | 🌐 Link bài báo Open Access |
| `OA_KW7_039` | **2023** | **LSTM-enhanced multi-view dynamical emotion graph representation for EEG signal recognition**<br>*Guixun Xu, Wenhui Guo, Yanjiang Wan...* | Journal of Neural Engineering | 6 | 🌐 Link bài báo Open Access |
| `OA_KW7_040` | **2026** | **MSGM: a multi-scale spatiotemporal graph Mamba for EEG emotion recognition**<br>*Hanwen Liu, Yifeng Gong, Zuwei Yan,...* | Frontiers in Neuroscience | 5 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_041` | **2024** | **A novel methodology for emotion recognition through 62-lead EEG signals: multilevel heterogeneous recurrence analysis**<br>*Yujie Wang, Cheng‐Bang Chen, Toshih...* | Frontiers in Physiology | 5 | 🌐 Link bài báo Open Access |
| `OA_KW7_042` | **2024** | **Mind to Music: An EEG Signal‐Driven Real‐Time Emotional Music Generation System**<br>*Shuang Ran, Wei Zhong, Lin Ma, Dan-...* | International Journal of Intelligent Systems | 5 | 🌐 Link bài báo Open Access |
| `OA_KW7_043` | **2023** | **Possibilistic distribution distance metric: a robust domain adaptation learning method**<br>*Jianwen Tao, Yufang Dan, Di Zhou* | Frontiers in Neuroscience | 5 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_044` | **2025** | **CNN-BiLSTM and DC-IGN fusion model and piecewise exponential attenuation optimization: an innovative approach to improve EEG emotion recognition performance**<br>*Shaohua Zhang, Feng Yan, Ruzhen Che...* | Frontiers in Computational Neuroscience | 4 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_045` | **2024** | **EmT: A Novel Transformer for Generalized Cross-subject EEG Emotion Recognition**<br>*Yi Ding, Chengxuan Tong, Shuailei Z...* | arXiv (Cornell University) | 4 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_046` | **2023** | **Emotion recognition and artificial intelligence: A systematic review (2014–2023) and research recommendations**<br>*Smith K. Khare, Victoria Blanes‐Vid...* | Information Fusion | 462 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW7_047` | **2024** | **Leveraging AI in E-Learning: Personalized Learning and Adaptive Assessment through Cognitive Neuropsychology—A Systematic Analysis**<br>*Constantinos Halkiopoulos, Evgenia ...* | Electronics | 313 | 🌐 Link bài báo Open Access |
| `OA_KW7_048` | **2025** | **Challenging Cognitive Load Theory: The Role of Educational Neuroscience and Artificial Intelligence in Redefining Learning Efficacy**<br>*Evgenia Gkintoni, Hera Antonopoulou...* | Brain Sciences | 284 | 🌐 Link bài báo Open Access |
| `OA_KW7_049` | **2023** | **Exploring the Frontiers of Neuroimaging: A Review of Recent Advances in Understanding Brain Functioning and Disorders**<br>*Chiahui Yen, Chia-Li Lin, Ming‐Chan...* | Life | 279 | 🌐 Link bài báo Open Access |
| `OA_KW7_050` | **2024** | **Integrating artificial intelligence to assess emotions in learning environments: a systematic literature review**<br>*Angel Olider Rojas Vistorte, Ángel ...* | Frontiers in Psychology | 271 | 🌐 Link bài báo Open Access |


---

## 2. Bộ Prompt Master Class (Google NotebookLM) Theo Chuẩn 20 Tiêu Chí

Dưới đây là 7 Prompts chuyên dụng được thiết kế riêng cho **Notebook 07: Dynamic Graph Neural Networks & Functional Brain Connectivity**. Bạn chỉ cần tải các bài báo/tài liệu trong thư mục này lên Google NotebookLM ([https://notebooklm.google.com/](https://notebooklm.google.com/)) và dán lần lượt các prompt bên dưới:

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
- **Tài liệu này phục vụ trực tiếp cho**: Chương 2, 4 & 5 (Các Mô hình Đối sánh SOTA Đồ thị).
- **Kết quả bóc tách từ NotebookLM**: Copy trực tiếp vào các mục tương ứng trong Luận án và bản thảo bài báo Journal IEEE TAFFC.
