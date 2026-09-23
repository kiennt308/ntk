# 📚 SỔ TAY NOTEBOOKLM #03: KIẾN TRÚC ĐA NHÁNH & CHÚ Ý CHÉO ĐA PHƯƠNG THỨC
## Multi-Branch Architectures & Cross-Modal Attention Mechanisms

> **Mục tiêu chuyên sâu:** Nắm vững các mô hình mã hóa tín hiệu chuyên biệt theo đặc tính vật lý (Spatial-GCN cho EEG, TCN cho ECG, CWT-CNN cho EDA), cơ chế tương tác chú ý chéo định hướng (Directional Cross-Modal Attention $Q_{\text{EEG}} \leftrightarrow K,V_{\text{Bio}}$), và các thực nghiệm bóc tách Ablation Studies.

---

## 📑 DANH MỤC 50 BÀI BÁO KHOA HỌC TRONG NOTEBOOK (100% FULLTEXT PDF CỤC BỘ)

| ID | Năm | Tiêu đề bài báo | Tạp chí / Nguồn | Trích dẫn | Trạng thái PDF |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `OA_KW3_001` | **2022** | **EEG Based Emotion Recognition: A Tutorial and Review**<br>*Xiang Li, Yazhou Zhang, Prayag Tiwari, Dawei ...* | ACM Computing Surveys | 492 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_002` | **2019** | **Current Directions in the Auricular Vagus Nerve Stimulation I – A Physiological Perspective**<br>*Eugenijus Kaniušas, Stefan Kampusch, Marc Tit...* | Frontiers in Neuroscience | 330 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_003` | **2024** | **Pathology of pain and its implications for therapeutic interventions**<br>*Bo Cao, Qixuan Xu, Yajiao Shi, Ruiyang Zhao, ...* | Signal Transduction and Targeted Therapy | 186 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_004` | **2023** | **Recent advancements in multimodal human–robot interaction**<br>*Hang Su, Wen Qi, Jiahao Chen, Chenguang Yang,...* | Frontiers in Neurorobotics | 180 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_005` | **2024** | **CTNet: a convolutional transformer network for EEG-based motor imagery classification**<br>*Wei Zhao, Xiaolu Jiang, Baocan Zhang, Shixiao...* | Scientific Reports | 172 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_006` | **2022** | **Inhalation Aromatherapy via Brain-Targeted Nasal Delivery: Natural Volatiles or Essential Oils on Mood Disorders**<br>*Jieqiong Cui, Meng Li, Yuanyuan Wei, Huayan L...* | Frontiers in Pharmacology | 166 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_007` | **2024** | **Role of machine learning and deep learning techniques in EEG-based BCI emotion recognition system: a review**<br>*Priyadarsini Samal, Mohammad Farukh Hashmi...* | Artificial Intelligence Review | 147 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_008` | **2023** | **Deep learning-based EEG emotion recognition: Current trends and future perspectives**<br>*Xiaohu Wang, Yongmei Ren, Ze Luo, He Geng Wei...* | Frontiers in Psychology | 133 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_009` | **2023** | **Generative adversarial networks in EEG analysis: an overview**<br>*Ahmed G. Habashi, Ahmed M. Azab, Seif Eldawla...* | Journal of NeuroEngineering and Rehabilitation | 124 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_010` | **2023** | **Multimodal Emotion Recognition Based on Facial Expressions, Speech, and EEG**<br>*Jiahui Pan, Weijie Fang, Zhihang Zhang, Bingz...* | IEEE Open Journal of Engineering in Medicine and Biology | 119 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_011` | **2025** | **A review on EEG-based multimodal learning for emotion recognition**<br>*Rajasekhar Pillalamarri, S. Udhayakumar...* | Artificial Intelligence Review | 117 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_012` | **2023** | **Review of Studies on Emotion Recognition and Judgment Based on Physiological Signals**<br>*Wenqian Lin, Chao Li...* | Applied Sciences | 116 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_013` | **2023** | **State-of-the-Art of Stress Prediction from Heart Rate Variability Using Artificial Intelligence**<br>*Yeaminul Haque, Rahat Shahriar Zawad, Chowdhu...* | Cognitive Computation | 107 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_014` | **2023** | **Transformer-Based Self-Supervised Multimodal Representation Learning for Wearable Emotion Recognition**<br>*Yujin Wu, Mohamed Daoudi, Ali Amad...* | IEEE Transactions on Affective Computing | 106 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_015` | **2023** | **Stress and Workload Assessment in Aviation—A Narrative Review**<br>*Giulia Masi, Gianluca Amprimo, Claudia Ferrar...* | Sensors | 97 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_016` | **2023** | **Multimodal Hierarchical CNN Feature Fusion for Stress Detection**<br>*Radhika Kuttala, Ramanathan Subramanian, O.V....* | IEEE Access | 79 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_017` | **2024** | **Machine learning for human emotion recognition: a comprehensive review**<br>*Eman M. G. Younis, Someya Mohsen, Essam H. Ho...* | Neural Computing and Applications | 75 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_018` | **2023** | **Approaches, Applications, and Challenges in Physiological Emotion Recognition—A Tutorial Overview**<br>*Yekta Said Can, Bhargavi Mahesh, Elisabeth An...* | Proceedings of the IEEE | 73 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_019` | **2024** | **EEG-based emotion recognition using graph convolutional neural network with dual attention mechanism**<br>*Wei Chen, Yuan Liao, Rui Dai, Yuanlin Dong...* | Frontiers in Computational Neuroscience | 58 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_020` | **2024** | **Region-Disentangled Diffusion Model for High-Fidelity PPG-to-ECG Translation**<br>*Debaditya Shome, Pritam Sarkar, Ali Etemad...* | Proceedings of the AAAI Conference on Artificial Intelligence | 39 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_021` | **2023** | **A novel feature fusion network for multimodal emotion recognition from EEG and eye movement signals**<br>*Baole Fu, Chunrui Gu, M.W. Fu, Yuxiao Xia, Yi...* | Frontiers in Neuroscience | 34 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_022` | **2023** | **Recognition of single upper limb motor imagery tasks from EEG using multi-branch fusion convolutional neural network**<br>*Rui Zhang, Yadi Chen, Zongxin Xu, Lipeng Zhan...* | Frontiers in Neuroscience | 26 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_023` | **2023** | **An improved model using convolutional sliding window-attention network for motor imagery EEG classification**<br>*Yuxuan Huang, Jianxu Zheng, Binxing Xu, Xuhan...* | Frontiers in Neuroscience | 22 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_024` | **2026** | **RAMamba-Net: A Reliability-Aware and Mamba-Based Multimodal Fusion Network for Auditory Attention Detection**<br>*Xingyi He, Ziwei Wang, Dongrui Wu...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_025` | **2026** | **Neural Visual Decoding via Cognitive guided Adaptive Blurring and Information Constrained Alignment**<br>*Fan Yin, Chuhang Zheng, Peiliang Gong, Dongha...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_026` | **2025** | **Geometric-Stochastic Multimodal Deep Learning for Predictive Modeling of SUDEP and Stroke Vulnerability**<br>*Preksha Girish, Rachana Mysore, Mahanthesha U...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_027` | **2025** | **An Emotion Recognition Framework via Cross-modal Alignment of EEG and Eye Movement Data**<br>*Jianlu Wang, Yanan Wang, Tong Liu...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_028` | **2025** | **ZIA: A Theoretical Framework for Zero-Input AI**<br>*Aditi De...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_029` | **2024** | **NeuroSpex: Neuro-Guided Speaker Extraction with Cross-Modal Attention**<br>*Dashanka De Silva, Siqi Cai, Saurav Pahuja, T...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_030` | **2024** | **Toward Robust Early Detection of Alzheimer's Disease via an Integrated Multimodal Learning Approach**<br>*Yifei Chen, Shenghao Zhu, Zhaojie Fang, Chang...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_031` | **2025** | **HEDN: A Hard-Easy Dual Network with Source Reliability Assessment for Cross-Subject EEG Emotion Recognition**<br>*Qiang Wang, Liying Yang, Jiayun Song, Yifan B...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_032` | **2024** | **Multi-Source EEG Emotion Recognition via Dynamic Contrastive Domain Adaptation**<br>*Yun Xiao, Yimeng Zhang, Xiaopeng Peng, Shuzhe...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_033` | **2026** | **LuMamba: Latent Unified Mamba for Electrode Topology-Invariant and Efficient EEG Modeling**<br>*Danaé Broustail, Anna Tegon, Thorir Mar Ingol...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_034` | **2022** | **A Joint Cross-Attention Model for Audio-Visual Fusion in Dimensional Emotion Recognition**<br>*R. Gnana Praveen, Wheidima Carneiro de Melo, ...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_035` | **2026** | **MUPA$^{2}$E: Multimodal Unified Perception with Asymmetric Attention for Emotion Assessment**<br>*Stefanos Gkikas, Eric Nichols, Christian Arza...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_036` | **2025** | **NeuroLingua: A Language-Inspired Hierarchical Framework for Multimodal Sleep Stage Classification Using EEG and EOG**<br>*Mahdi Samaee, Mehran Yazdi, Daniel Massicotte...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_037` | **2025** | **MECASA: Motor Execution Classification using Additive Self-Attention for Hybrid EEG-fNIRS Data**<br>*Gourav Siddhad, Juhi Singh, Partha Pratim Roy...* | arXiv Preprints (Cross-Modal Attention) | 20 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_038` | **2024** | **Attention model of EEG signals based on reinforcement learning**<br>*Wei Zhang, Xianlun Tang, Mengzhou Wang...* | Frontiers in Human Neuroscience | 17 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_039` | **2025** | **A composite improved attention convolutional network for motor imagery EEG classification**<br>*Wenzhe Liao, Zipeng Miao, Shuaibo Liang, Liny...* | Frontiers in Neuroscience | 17 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_040` | **2025** | **DGAT: a dynamic graph attention neural network framework for EEG emotion recognition**<br>*Shihang Ding, Kaixuan Wang, Wenhao Jiang, Con...* | Frontiers in Psychiatry | 17 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_041` | **2025** | **Directional Spatial and Spectral Attention Network (DSSA Net) for EEG-based emotion recognition**<br>*Jiyao Liu, Lang He, Haifeng Chen, Dongmei Jia...* | Frontiers in Neurorobotics | 12 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_042` | **2025** | **Multimodal physiological signal emotion recognition based on multi-head cross attention with representation learning**<br>*Shihang Ding, Lin Ma, Haifeng Li...* | Frontiers in Psychiatry | 6 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_043` | **2024** | **A Comprehensive Survey on Emerging Techniques and Fusion Technologies in Spatio-Temporal EEG Data Analysis**<br>*Pengfei Wang, Huanran Zheng, Silong Dai, Yiqi...* | Chinese journal of information fusion. | 6 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_044` | **2024** | **STAFNet: an adaptive multi-feature learning network via spatiotemporal fusion for EEG-based emotion recognition**<br>*Fo Hu, Kailun He, Mengyuan Qian, Xiaofeng Liu...* | Frontiers in Neuroscience | 6 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_045` | **2025** | **Segmentation-enhanced approach for emotion detection from EEG signals using the fuzzy C-mean and SVM**<br>*Mahmood A. Mahmood, Khalaf Okab Alsalem, Murt...* | Scientific Reports | 6 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_046` | **2026** | **MSGM: a multi-scale spatiotemporal graph Mamba for EEG emotion recognition**<br>*Hanwen Liu, Yifeng Gong, Zuwei Yan, Zeheng Zh...* | Frontiers in Neuroscience | 5 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_047` | **2025** | **A Review of Deep Learning Techniques for EEG-Based Emotion Recognition: Models, Methods, and Datasets**<br>*P. Sreehari, U. Raghavendra, Anjan Gudigar...* | F1000Research | 5 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_048` | **2023** | **BiTCAN: An emotion recognition network based on saliency in brain cognition**<br>*Yanling An, Shaohai Hu, Shuaiqi Liu, Bing Li...* | Mathematical Biosciences & Engineering | 4 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_049` | **2024** | **DuA: Dual Attentive Transformer in Long-Term Continuous EEG Emotion Analysis**<br>*Yue Pan, Qile Liu, Qing Huo Liu, Li Zhang...* | arXiv (Cornell University) | 4 | 📄 Có sẵn PDF trong thư mục |
| `OA_KW3_050` | **2024** | **miMamba: EEG-based Emotion Recognition with Multi-scale Inverted Mamba Models**<br>*Xin Zhou, Huang, Dawei, Peng, Xiaojing, Yin, ...* | arXiv (Cornell University) | 3 | 📄 Có sẵn PDF trong thư mục |

---

## 🎯 BỘ PROMPT PHÂN TÍCH NOTEBOOKLM CHUYÊN SÂU

*(Sử dụng các prompt trong file `NOTEBOOKLM_PER_PAPER_PROMPTS.md` để phân tích từng bài báo trong danh mục trên).*
