# 🧠 CẨM NANG TOÀN DIỆN: NGHIÊN CỨU & TRIỂN KHAI CHO ĐỀ TÀI TIẾN SĨ (PhD)

---

> ### 🎓 **ĐỀ TÀI TIẾN SĨ (PhD THESIS TOPIC):**
> **“Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức”**
> *(Multi-task Multi-branch Architecture for Emotion Recognition from Multimodal Biosignals)*

---

Hướng đọc paper của đề tài này **rộng hơn EEG Emotion Recognition rất nhiều**. Bạn không chỉ xây literature review quanh một mình EEG mà cần đọc và phát triển theo **4 trục chính** hội tụ tại trung tâm:

```text
                    ĐỀ TÀI CỦA BẠN
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   Multimodal         Multi-task       Multi-branch
   Biosignals         Learning         Architecture
        │                 │                 │
   EEG + ECG          Emotion          CNN/Transformer
   EDA/GSR            Valence          Attention
   EMG                Arousal          Fusion
   etc.               Discrete         Experts
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                  Emotion Recognition
```

---

## 📑 MỤC LỤC
1. [Giải Phẫu Đề Tài: 4 Khái Niệm Cốt Lõi Cần Xây Literature](#1-giải-phẫu-đề-tài-4-khái-niệm-cốt-lõi-cần-xây-literature)
2. [Cấu Trúc 5 Nhóm NotebookLM Chuyên Biệt](#2-cấu-trúc-5-nhóm-notebooklm-chuyên-biệt)
3. [Hệ Thống Tải & Phân Loại Bài Báo Tự Động Vào 5 Workspace](#3-hệ-thống-tải--phân-loại-bài-báo-tự-động-vào-5-workspace)
4. [Bảng Ma Trận Nghiên Cứu (Research Matrix) Chuẩn PhD](#4-bảng-ma-trận-nghiên-cứu-research-matrix-chuẩn-phd)
5. [Bộ Prompt NotebookLM Khai Thác Bài Báo Chuyên Sâu](#5-bộ-prompt-notebooklm-khai-thác-bài-báo-chuyên-sâu)
6. [Research Gap Nằm Ở Điểm Giao Thoa](#6-research-gap-nằm-ở-điểm-giao-thoa)
7. [Khung Câu Hỏi Nghiên Cứu (RQ1 - RQ6) & Giả Thuyết Khoa Học (H1 - H6)](#7-khung-câu-hỏi-nghiên-cứu-rq1---rq6--giả-thuyết-khoa-học-h1---h6)
8. [Kiến Trúc Tổng Thể & Thiết Kế Luận Án](#8-kiến-trúc-tổng-thể--thiết-kế-luận-án)
9. [Quy Trình Phối Hợp: NotebookLM + ChatGPT](#9-quy-trình-phối-hợp-notebooklm--chatgpt)
10. [Kinh Nghiệm Phản Biện Thực Chiến Chuẩn Q1](#10-kinh-nghiệm-phản-biện-thực-chiến-chuẩn-q1)

---

## 1. GIẢI PHẪU ĐỀ TÀI: 4 KHÁI NIỆM CỐT LÕI CẦN XÂY LITERATURE

Có 4 khái niệm mà bạn phải đọc literature riêng biệt và thấu đáo:

### A. Multimodal Biosignals (Tín hiệu Y sinh Đa phương thức)
Các tín hiệu chính:
* **EEG** (Electroencephalogram): Hoạt động điện não vỏ não (Brain activity)
* **ECG** (Electrocardiogram): Hoạt động tim mạch / biến thiên nhịp tim HRV (Cardiac activity)
* **EDA / GSR** (Electrodermal Activity / Galvanic Skin Response): Hoạt động hệ thần kinh tự chủ (Autonomic nervous system)
* **EMG** (Electromyogram): Hoạt động cơ mặt / biểu cảm vi mô (Muscle activity)
* **Respiration & PPG**: Tần số hô hấp và biến thiên thể tích mạch quang học

> **Câu hỏi nghiên cứu cốt lõi:**
> *Các modality khác nhau bổ sung thông tin cảm xúc cho nhau như thế nào (Modality Complementarity)?*

---

### B. Multi-task Learning (Học Đa Nhiệm Vụ)
Không chỉ đơn thuần dự đoán nhãn cảm xúc phân loại rời rạc (Discrete Emotion), mà mô hình học cùng lúc trên không gian biểu diễn chung (Shared Representation):

```text
             Shared representation
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
    Valence       Arousal      Emotion
    regression    regression   classification
```

Hàm mất mát đa nhiệm vụ (Multi-task Loss):
$$\mathcal{L}_{total} = \lambda_1 \mathcal{L}_{valence} + \lambda_2 \mathcal{L}_{arousal} + \lambda_3 \mathcal{L}_{emotion}$$

> Đây chính là **một trục đóng góp khoa học (contribution) trọng yếu** của luận án.

---

### C. Multi-branch Architecture (Kiến Trúc Đa Nhánh)

```text
EEG ─────► EEG Branch ─────┐
                           │
ECG ─────► ECG Branch ─────┤
                           ├──► Cross-modal Fusion ──► Multi-Task Output
EDA ─────► EDA Branch ─────┤
                           │
EMG ─────► EMG Branch ─────┘
```

Nghiên cứu sinh cần đặt các câu hỏi phản biện sâu:
* *Tại sao EEG cần branch riêng? (Do đặc tính không gian - thời gian đa kênh trên vỏ não).*
* *Tại sao ECG cần branch riêng? (Do phụ thuộc chu kỳ nhịp tim R-peak và miền tần số HRV).*
* *Có nên dùng cùng một encoder chung không? (Heterogeneous signals vs. Homogeneous).*
* *Nên thực hiện Fusion ở Early, Intermediate hay Late stage?*

---

### D. Multimodal Fusion (Dung Hợp Đa Phương Thức)
Đây là một mảng literature độc lập cực lớn:
```text
Early Fusion (Feature Concatenation)
     ↓
Intermediate / Mid-level Fusion
     ↓
Late Fusion (Decision / Score-level)
     ↓
Cross-modal Attention
     ↓
Cross-modal Transformer / Co-attention
     ↓
Adaptive Fusion & Mixture-of-Experts (MoE)
```

---

## 2. CẤU TRÚC 5 NHÓM NOTEBOOKLM CHUYÊN BIỆT

**Tuyệt đối không dồn toàn bộ paper vào một Notebook duy nhất.** Hãy chia thành 5 nhóm chuyên sâu:

### 📁 Notebook 1 — Biosignal Emotion Recognition
* **Nguồn:** EEG, ECG, EDA, EMG, PPG, Respiration đơn lẻ.
* **Mục tiêu:** Hiểu sâu đặc tính sinh lý và cách trích xuất đặc trưng của từng modality.

### 📁 Notebook 2 — Multimodal Emotion Recognition
* **Nguồn:** EEG + ECG, EEG + EDA, EEG + ECG + EDA, EEG + EMG, EEG + Peripheral signals (trên các benchmark DEAP, AMIGOS, DREAMER, MAHNOB-HCI, CASE, K-EmoCon).
* **Mục tiêu:** Tìm hiểu các phương pháp đồng bộ và chiến lược dung hợp (Fusion).

### 📁 Notebook 3 — Multi-task Learning
* **Nguồn:** Valence, Arousal, Dominance regression + Emotion classification, Multi-label emotion, Task relationships, Loss balancing (GradNorm, Uncertainty).
* **Mục tiêu:** Hiểu sâu mối tương quan giữa các nhiệm vụ cảm xúc.

### 📁 Notebook 4 — Multi-branch / Fusion Architecture
* **Nguồn:** Multi-branch CNN, Multi-stream CNN, Dual-stream Transformer, Cross-attention, Mixture-of-Experts, Shared-private networks, Hierarchical fusion.
* **Mục tiêu:** Tìm ra khoảng trống kiến trúc (Architecture Gap).

### 📁 Notebook 5 — Generalization & Robustness (KHÔNG ĐƯỢC BỎ QUA)
* **Nguồn:** Cross-subject (LOSO), Cross-session, Cross-dataset, Missing modality, Noisy modality, Domain adaptation, Domain generalization, Ablation, Interpretability.
* **Mục tiêu:** Đảm bảo mô hình có tính bền vững trong thực tế. *(Một kiến trúc đẹp nhưng chỉ chạy tốt trên 1 dataset cố định thì giá trị đóng góp khoa học sẽ rất yếu).*

---

## 3. HỆ THỐNG TẢI & PHÂN LOẠI BÀI BÁO TỰ ĐỘNG VÀO 5 WORKSPACE

Thư mục làm việc: `d:\ntk\eeg_paper_downloader`

### 3.1. Phân loại và đóng gói bài báo sẵn có vào 5 Track:
```powershell
python filter_and_packager.py --max-per-track 35
```
*Kết quả:* Tự động quét cơ sở dữ liệu SQLite, phân loại và copy bài báo PDF vào `notebooklm_workspace/notebook_01` đến `notebook_05`.

### 3.2. Tải bài chuyên sâu từ Open Access (Semantic Scholar & Europe PMC):
```powershell
# Track 3: Multi-Task Learning trong Biosignals
python oa_paper_fetcher.py --track 3 --limit 20

# Track 4: Multi-Branch & Cross-Modal Attention
python oa_paper_fetcher.py --track 4 --limit 20

# Track 5: Missing Modality & Robustness
python oa_paper_fetcher.py --track 5 --limit 20
```

---

## 4. BẢNG MA TRẬN NGHIÊN CỨU (RESEARCH MATRIX) CHUẨN PhD

Khi đọc bất kỳ paper nào, bạn cần điền đầy đủ vào Research Matrix này:

| Tiêu chí (Category) | Câu hỏi kiểm tra (Questions) |
| :--- | :--- |
| **Modalities** | Sử dụng EEG, ECG, EDA, EMG, PPG hay tín hiệu nào? |
| **Dataset** | DEAP, AMIGOS, DREAMER, MAHNOB-HCI, CASE, K-EmoCon...? |
| **Subjects** | Bao nhiêu đối tượng tham gia thử nghiệm? |
| **Task** | Classification, Regression hay Joint Multi-task? |
| **Emotion** | Valence, Arousal, Dominance hay Discrete categories? |
| **Encoder** | CNN, RNN, Transformer, GNN, hay Hybrid? |
| **Branches** | Bao nhiêu branch riêng biệt cho từng modality? |
| **Fusion** | Early, Mid, Late, Cross-attention, Transformer, MoE? |
| **Shared** | Có không gian biểu diễn chung (Shared representation)? |
| **Private** | Có không gian đặc trưng riêng (Modality-specific representation)? |
| **Tasks** | Có bao nhiêu task cùng được tối ưu đồng thời? |
| **Loss** | Multi-task loss formulation như thế nào? |
| **Weighting** | Trọng số loss là Fixed (cố định) hay Dynamic (động)? |
| **Missing Modality** | Có giải pháp xử lý khi thiếu kênh/cảm biến không? |
| **Cross-subject** | Đánh giá Subject-independent / LOSO hay Subject-dependent? |
| **Cross-dataset** | Có thử nghiệm trên dataset khác để chứng minh generalization? |
| **Ablation** | Có thí nghiệm bóc tách chứng minh từng module không? |
| **Parameters & Latency**| Số lượng tham số và thời gian suy luận là bao nhiêu? |
| **Main Contribution** | Đóng góp kỹ thuật cốt lõi là gì? |
| **Limitation** | Tác giả thừa nhận hạn chế nào? |
| **Research Gap** | Khoảng trống nào mở ra cho đề tài của bạn? |

---

## 5. BỘ PROMPT NOTEBOOKLM KHAI THÁC BÀI BÁO CHUYÊN SÂU

Sau khi tải các file PDF vào từng Notebook trong NotebookLM, hãy sử dụng chuỗi prompt chuẩn sau:

### 🔹 Prompt 1: Bóc Tách Chuyên Sâu 20 Tiêu Chí Của Paper
```text
Analyze this paper specifically from the perspective of my PhD research topic:

"Multi-task multi-branch architecture for emotion recognition from multimodal biosignals."

Do not merely summarize the paper.

Analyze:
1. Biosignal modalities
2. Dataset
3. Emotion representation
4. Prediction tasks
5. Modality-specific encoder
6. Shared encoder
7. Multi-branch architecture
8. Fusion strategy
9. Multi-task learning strategy
10. Loss functions
11. Task weighting
12. Cross-modal interaction
13. Subject-dependent/independent evaluation
14. Missing/noisy modality handling
15. Baselines
16. Ablation studies
17. Computational complexity
18. Main contribution
19. Explicit limitations
20. Potential research gaps relevant to my thesis

For every important claim, cite the exact page, section, table, or figure.
If information is not reported, write "Not reported".
Do not infer missing experimental details.
```

---

### 🔹 Prompt 2: Đánh Giá & Phân Loại Mức Độ Liên Quan Đến Đề Tài
```text
Compared with my research topic,
which parts of this paper are directly relevant,
which parts are partially relevant,
and which parts are unrelated?

Classify into:
A. Directly relevant
B. Supporting literature
C. Potential baseline
D. Potential competing approach
E. Not relevant

Explain why for each classification.
```
> **Ý nghĩa:** Giúp bạn tránh bẫy phổ biến của nghiên cứu sinh: *đọc hàng trăm paper nhưng cuối cùng literature review không phục vụ trực tiếp cho research questions của đề tài.*

---

### 🔹 Prompt 3: Xuất Bảng Ma Trận Tổng Hợp Cả Notebook
```text
Compare all papers in this notebook.

Generate a comprehensive Markdown Research Matrix with the following columns:
1. Paper (Author & Year)
2. Modalities (EEG/ECG/EDA/EMG/etc.)
3. Dataset & Number of Subjects
4. Target Tasks (Valence/Arousal/Discrete)
5. Modality Encoders (CNN/RNN/Transformer/GNN)
6. Branch Architecture (Number of branches)
7. Fusion Strategy (Early/Mid/Late/Cross-Attention/MoE)
8. Shared vs Private Features (Yes/No & Method)
9. Multi-Task Strategy & Loss Weighting
10. Missing Modality Handling (Yes/No)
11. Evaluation Setup (Subject-dependent / LOSO)
12. Best Performance (Acc / F1 / RMSE)
13. Main Technical Contribution
14. Unresolved Limitations & Gaps

Format as a clean Markdown table.
```

---

## 6. RESEARCH GAP NẰM Ở ĐIỂM GIAO THOA

Đừng chỉ đi tìm câu hỏi nhỏ như: *"Có ai dùng Transformer cho EEG chưa?"* (câu hỏi đó quá đơn giản và đã có hàng trăm bài làm rồi).

Hãy tìm **khoảng trống tại giao điểm (Intersection)**:

```text
                    Multimodal
                       │
                       │
            ┌──────────┼──────────┐
            │          │          │
            ▼          ▼          ▼
           EEG        ECG        EDA
            │          │          │
            └──────────┼──────────┘
                       │
                  Multi-branch
                       │
                       ▼
                Shared/Private
                  features
                       │
                       ▼
                Cross-modal
                  fusion
                       │
                       ▼
                 Multi-task
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
           Valence   Arousal  Emotion
                       │
                       ▼
                Generalization
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
          Cross-user Cross-    Missing
                    dataset   modality
```

> **Khoảng trống có giá trị khoa học cao nhất luôn nằm ở giao điểm này**, chứ không nhất thiết ở việc chế tạo thêm một layer mới đơn thuần.

---

## 7. KHUNG CÂU HỎI NGHIÊN CỨU (RQ1 - RQ6) & GIẢ THUYẾT KHOA HỌC (H1 - H6)

Thay vì đặt câu hỏi mơ hồ: *"Can Transformer improve EEG emotion recognition?"*, một câu hỏi nghiên cứu tổng thể chuẩn mực của luận án sẽ là:

> **"How can modality-specific and shared representations be jointly learned through a multi-branch multi-task architecture to improve multimodal emotion recognition under cross-subject and missing-modality conditions?"**

Từ đó, luận án được tách thành 6 Research Questions (RQ) tương ứng với 6 Hypotheses (H) và các kịch bản thực nghiệm cụ thể:

| Câu hỏi nghiên cứu (RQ) | Giả thuyết khoa học (Hypothesis) | Thí nghiệm kiểm chứng (Experiment) |
| :--- | :--- | :--- |
| **RQ1** | **H1:** Multimodal biosignals cải thiện emotion recognition vượt trội so với từng single modality riêng lẻ. | So sánh Single modality (EEG only, ECG only, EDA only) vs. Multimodal model. |
| **RQ2** | **H2:** Modality-specific branches hiệu quả hơn đáng kể so với việc dùng chung 1 shared encoder cho các tín hiệu dị thể. | So sánh Multi-Branch Architecture vs. Single Shared Backbone trên raw signals. |
| **RQ3** | **H3:** Multi-task learning (Valence + Arousal + Discrete Emotion) giúp biểu diễn representation tốt hơn single-task learning. | So sánh Multi-task Loss vs. các mô hình Single-task độc lập. |
| **RQ4** | **H4:** Cross-modal attention/fusion cải thiện chất lượng biểu diễn đa phương thức so với phép nối vector (concatenation) đơn giản. | Ablation study thay thế Cross-modal Attention bằng Concatenation, Early fusion, Late fusion. |
| **RQ5** | **H5:** Biểu diễn phân tách Shared-Private (Shared-Private representation) giúp mô hình generalize tốt hơn trên đối tượng chưa từng thấy (Cross-subject / LOSO). | Đánh giá giao thức Leave-One-Subject-Out (LOSO) khi bật và tắt cơ chế Shared-Private Disentanglement. |
| **RQ6** | **H6:** Kiến trúc đề xuất duy trì tính bền vững (robustness) ngay cả khi bị mất 1 hoặc nhiều modality (Missing / Noisy Modality). | Giả lập mất tín hiệu EEG, ECG hoặc EDA trong quá trình inference và đánh giá độ sụt giảm hiệu năng. |

---

## 8. KIẾN TRÚC TỔNG THỂ & THIẾT KẾ LUẬN ÁN

Cấu trúc kiến trúc hoàn chỉnh của luận án:

```text
                 Multimodal Biosignals
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
           EEG          ECG          EDA
            │            │            │
            ▼            ▼            ▼
         Encoder      Encoder      Encoder
      (S-T Graph)      (TCN)      (BiLSTM)
            │            │            │
            └────────────┼────────────┘
                         ▼
              Modality-specific
                  representation
                         │
                  ┌──────┴──────┐
                  ▼             ▼
              Shared         Private
             feature         feature
                  │             │
                  └──────┬──────┘
                         ▼
                 Cross-modal Fusion
              (Cross-modal Transformer)
                         │
                         ▼
              Shared multimodal feature
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          Valence      Arousal     Emotion
          Task         Task        Task
       (Regression) (Regression) (Classification)
             │           │           │
             └───────────┼───────────┘
                         ▼
                  Multi-task Loss
        (Dynamic Loss Weighting: GradNorm)
```

Luận án không chỉ dừng ở tuyên bố: *"Model của tôi đạt accuracy cao"*, mà lần lượt bảo vệ thành công từng giả thuyết `H1 → H6`. **Mỗi giả thuyết tương ứng với 1 bài báo Q1 hoặc 1 chương trọng tâm của Thesis.**

---

## 9. QUY TRÌNH PHỐI HỢP: NOTEBOOKLM + CHATGPT

```text
                PAPERS
                  │
                  ▼
          NotebookLM đọc
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
   Dataset     Method       Results
      │           │           │
      └───────────┼───────────┘
                  ▼
             Research Matrix
                  │
                  ▼
             30–50 papers
                  │
                  ▼
             Gap Analysis
                  │
                  ▼
             Research Questions
                  │
                  ▼
               ChatGPT
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
    Architecture Experiments Papers (Q1)
```

* **NotebookLM:** Đóng vai trò đọc, trích xuất chính xác và kiểm chứng bằng chứng thực nghiệm từ kho tài liệu.
* **ChatGPT:** Đóng vai trò tổng hợp, phản biện, thiết kế khung nghiên cứu (Research Framework) và kịch bản thực nghiệm (Experiment Design).

> 💡 **Lời khuyên khởi đầu:**
> Chưa vội thiết kế model ngay từ đầu. Hãy xây dựng trước một **Literature Map khoảng 40–60 paper**, chia thành `EEG / Peripheral biosignals / Multimodal fusion / Multi-task / Multi-branch / Generalization`. Khi đó kiến trúc đề xuất của bạn sẽ xuất phát từ **Research Gap thực sự**, thay vì cố tìm một kiến trúc rồi gượng ép tìm lý do biện minh cho nó.

---

## 10. KINH NGHIỆM PHẢN BIỆN THỰC CHIẾN CHUẨN Q1

1. **Tránh bẫy "Ghép tầng cơ học" (Engineering Stacking):**
   * Đừng ghép nối tùy tiện các khối phức tạp (CNN + LSTM + Transformer + GNN) mà không có cơ sở lý giải sinh lý học. Reviewer Q1 sẽ chất vấn: *"Tại sao ECG lại cần cấu trúc không gian GNN trong khi nó không có topo đa cực như EEG?"*
2. **Cân bằng Temporal Resolution giữa các Modality:**
   * Tín hiệu EEG có tần số lấy mẫu cao (128–512 Hz), trong khi EDA biến thiên rất chậm (4–16 Hz). Nhánh đa nhánh phải có cơ chế **Multi-scale Temporal Pooling hoặc Resampling** trước khi đưa vào khối Cross-modal Fusion.
3. **Cân bằng Gradient trong Multi-Task Loss:**
   * Gradient của Classification (Cross-Entropy) và Regression (MSE / Smooth L1) chênh lệch rất lớn. Bắt buộc phải áp dụng **Dynamic Weighting** (như Homoscedastic Uncertainty Weighting hoặc GradNorm) để tránh một nhiệm vụ lấn át các nhiệm vụ còn lại.
