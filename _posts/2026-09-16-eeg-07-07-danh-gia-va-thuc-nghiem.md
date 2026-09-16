---
layout: post
title: "[Bài 07] Đánh Giá & Thực Nghiệm: Cross-Validation Subject-Independent, Metrics F1/AUC, Ablation Study & Phân Tích Thống Kê"
date: 2026-09-16 14:00:00 +0700
categories: [EEG]
tags: [eeg, bci, deap-dataset, seed-dataset, dreamer, mahnob-hci, multimodal-datasets, data-loader]
series: "EEG & Emotion Recognition AI"
series_order: 7
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80"
summary: "Thiết lập chuẩn mực khoa học trong nghiên cứu AI y sinh: Phân tích giao thức Leave-One-Subject-Out (LOSO), hệ chỉ số đa chiều F1/Kappa/Confusion Matrix, kiểm định thống kê Paired t-Test & Wilcoxon, hiệu chỉnh so sánh bội Bonferroni/FDR và trực quan hóa XAI với t-SNE."
tldr:
  - "Giao thức Leave-One-Subject-Out (LOSO) là tiêu chuẩn bắt buộc để đo lường năng lực tổng quát hóa thực tế của hệ thống BCI."
  - "Hệ số đồng thuận Cohen's Kappa (kappa) loại bỏ yếu tố đoán ngẫu nhiên, phản ánh chính xác độ tin cậy của mô hình trên tập dữ liệu mất cân bằng."
  - "Kiểm định ý nghĩa thống kê (Paired t-Test / Wilcoxon Signed-Rank) bảo chứng khoa học cho mọi tuyên bố vượt trội giữa các kiến trúc AI."
  - "Hiệu chỉnh Bonferroni và Benjamini-Hochberg (FDR) ngăn chặn hiện tượng bùng nổ sai lầm loại I (P-Hacking) khi so sánh đa mô hình."
  - "Nghiên cứu triệt tiêu (Ablation Study) định lượng chính xác tỷ trọng đóng góp độc lập của từng module trong hệ thống học sâu."
---
{% raw %}
# Đánh Giá & Thực Nghiệm: Cross-Validation Subject-Independent, Metrics F1/AUC, Ablation Study & Phân Tích Thống Kê

Trong nghiên cứu khoa học và phát triển hệ thống trí tuệ nhân tạo y sinh (**Biomedical AI**), việc đạt được độ chính xác cao trên tập dữ liệu huấn luyện không có nhiều ý nghĩa nếu không được kiểm chứng qua các **giao thức đánh giá nghiêm ngặt** (**Rigorous Evaluation Protocols**), các **chỉ số đo lường đa chiều** (**Multi-Dimensional Metrics**) và các **phép kiểm định thống kê khoa học** (**Statistical Significance Testing**).

Một công bố khoa học hay một sản phẩm BCI chỉ thực sự đáng tin cậy khi chứng minh được khả năng tổng quát hóa trên người dùng mới (**Subject-Independent Generalization**) và loại trừ hoàn toàn các cạm bẫy rò rỉ dữ liệu (*Data Leakage*).

---

## 1. Ba Giao Thức Đánh Giá Chuẩn Mực Trong BCI

```mermaid
flowchart TD
    subgraph PROTOCOLS["🧪 3 GIAO THỨC ĐÁNH GIÁ TRONG AI Y SINH"]
        direction TB
        P1["1. WITHIN-SUBJECT EVALUATION<br/>(Train/Test trên cùng một cá nhân)"]
        P2["2. CROSS-SUBJECT / LOSO EVALUATION<br/>(Train trên N-1 người, Test trên 1 người mới toanh)"]
        P3["3. TEMPORAL TRAIN-TEST SPLIT<br/>(Train trên nửa đầu phiên đo, Test trên nửa cuối)"]
    end

    P1 -->|"Xác định"| UP_BOUND["Cận trên lý thuyết tối đa (Personalized Upper Bound)"]
    P2 -->|"Xác định"| REAL_WORLD["Hiệu năng thực tế khi triển khai thương mại (Zero-shot)"]
    P3 -->|"Triệt tiêu"| NO_LEAK["Loại bỏ 100% rò rỉ tương quan thời gian lân cận"]

    style PROTOCOLS fill:none,stroke:#6366f1,stroke-width:1.75px
    style P1 fill:none,stroke:#3b82f6,stroke-width:1.5px
    style P2 fill:none,stroke:#10b981,stroke-width:2px
    style P3 fill:none,stroke:#f59e0b,stroke-width:1.5px
    style UP_BOUND fill:none,stroke:#64748b,stroke-width:1.5px
    style REAL_WORLD fill:none,stroke:#10b981,stroke-width:1.5px
    style NO_LEAK fill:none,stroke:#06b6d4,stroke-width:1.5px
```

### 1.1. Cài Đặt Giao Thức Leave-One-Subject-Out (LOSO) Bằng PyTorch

```python
import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score

class LOSOEvaluator:
    def __init__(self, model_class, model_args, device: str = 'cuda'):
        self.model_class = model_class
        self.model_args = model_args
        self.device = device
        
    def evaluate(self, subjects_dict: dict, epochs: int = 30, lr: float = 0.001) -> dict:
        """
        subjects_dict: {'sub_01': {'x': Tensor, 'y': Tensor}, ...}
        """
        subject_ids = list(subjects_dict.keys())
        results = {}
        
        for test_id in subject_ids:
            # 1. Tách tập Train (N-1 người) và Test (1 người)
            train_x = torch.cat([subjects_dict[s]['x'] for s in subject_ids if s != test_id]).to(self.device)
            train_y = torch.cat([subjects_dict[s]['y'] for s in subject_ids if s != test_id]).to(self.device)
            test_x = subjects_dict[test_id]['x'].to(self.device)
            test_y = subjects_dict[test_id]['y'].to(self.device)
            
            # 2. Khởi tạo lại trọng số mô hình từ đầu
            model = self.model_class(**self.model_args).to(self.device)
            optimizer = torch.optim.Adam(model.parameters(), lr=lr)
            criterion = torch.nn.CrossEntropyLoss()
            
            # 3. Huấn luyện
            model.train()
            for ep in range(epochs):
                optimizer.zero_grad()
                loss = criterion(model(train_x), train_y)
                loss.backward()
                optimizer.step()
                
            # 4. Kiểm thử trên đối tượng chưa từng xuất hiện
            model.eval()
            with torch.no_grad():
                preds = model(test_x).argmax(dim=-1).cpu().numpy()
                y_true = test_y.cpu().numpy()
                
                acc = accuracy_score(y_true, preds)
                f1 = f1_score(y_true, preds, average='weighted')
                results[test_id] = {'acc': acc, 'f1': f1}
                
        accs = [r['acc'] for r in results.values()]
        f1s = [r['f1'] for r in results.values()]
        return {
            'mean_acc': np.mean(accs),
            'std_acc': np.std(accs),
            'mean_f1': np.mean(f1s),
            'std_f1': np.std(f1s),
            'per_subject': results
        }
```

---

## 2. Hệ Chỉ Số Đo Lường Đa Chiều (Evaluation Metrics)

Khi tập dữ liệu cảm xúc bị mất cân bằng mẫu (*Class Imbalance* - ví dụ: trạng thái bình thường chiếm $70\%$, sợ hãi chiếm $10\%$), chỉ số **Accuracy** sẽ phản ánh sai lệch nghiêm trọng chất lượng của mô hình.

### 2.1. Hệ Số Đồng Thuận Cohen’s Kappa ($\kappa$)

Cohen’s Kappa đo lường mức độ đồng thuận giữa dự đoán của AI và nhãn thực tế sau khi **đã loại trừ toàn bộ yếu tố trùng hợp ngẫu nhiên**:

$$\kappa = \frac{p_o - p_e}{1 - p_e}$$

* $p_o$: Độ chính xác quan sát được ($\text{Accuracy}$).
* $p_e$: Xác suất trùng hợp ngẫu nhiên lý thuyết dựa trên phân phối biên của ma trận nhầm lẫn.

| Giá Trị $\kappa$ | Mức Độ Đồng Thuận & Độ Tin Cậy | Đánh Giá Ứng Dụng Y Sinh |
| :---: | :--- | :--- |
| <span class="badge badge--rose">$< 0.20$</span> | Rất kém / Đoán mò ngẫu nhiên (*Slight*) | Không thể sử dụng |
| <span class="badge badge--amber">$0.21 - 0.40$</span> | Tương đối (*Fair*) | Cần cải tiến thuật toán |
| <span class="badge badge--primary">$0.41 - 0.60$</span> | Trung bình khá (*Moderate*) | Đạt ngưỡng chấp nhận nghiên cứu |
| <span class="badge badge--cyan">$0.61 - 0.80$</span> | Rất tốt (*Substantial*) | Chuẩn mực cho thiết bị y tế |
| <span class="badge badge--emerald">$0.81 - 1.00$</span> | Gần như hoàn hảo (*Almost Perfect*) | Đạt độ tin cậy vàng lâm sàng |

```python
from sklearn.metrics import cohen_kappa_score, confusion_matrix, classification_report

def evaluate_multi_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    cm = confusion_matrix(y_true, y_pred)
    kappa = cohen_kappa_score(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average='macro')
    weighted_f1 = f1_score(y_true, y_pred, average='weighted')
    
    return {
        'accuracy': acc,
        'cohen_kappa': kappa,
        'macro_f1': macro_f1,
        'weighted_f1': weighted_f1,
        'confusion_matrix': cm
    }
```

---

## 3. Kiểm Định Ý Nghĩa Thống Kê (Statistical Significance Testing)

Để khẳng định "Mô hình Mamba vượt trội hơn mô hình CNN", sự chênh lệch độ chính xác bắt buộc phải vượt qua bài kiểm định giả thuyết thống kê để chứng minh không phải do ngẫu nhiên:

```mermaid
flowchart TD
    subgraph STAT_DECISION["📊 CÂY QUYẾT ĐỊNH KIỂM ĐỊNH THỐNG KÊ"]
        direction TB
        INPUT_D["Hiệu số độ chính xác giữa 2 mô hình:<br/>d = Acc_A - Acc_B (trên N đối tượng)"]
        TEST_NORM{"Kiểm định phân phối chuẩn<br/>(Shapiro-Wilk Test)"}
        PARAM["Kiểm định tham số:<br/>Paired Student's t-Test (stats.ttest_rel)"]
        NON_PARAM["Kiểm định phi tham số:<br/>Wilcoxon Signed-Rank Test (stats.wilcoxon)"]
        DECIDE{"p-value < 0.05?"}
        SIG["✅ Khác biệt có ý nghĩa thống kê thực thụ"]
        NOT_SIG["❌ Không đủ bằng chứng khẳng định vượt trội"]
    end

    INPUT_D --> TEST_NORM
    TEST_NORM -->|"p > 0.05 (Phân phối chuẩn)"| PARAM
    TEST_NORM -->|"p ≤ 0.05 (Không chuẩn / N nhỏ)"| NON_PARAM
    PARAM --> DECIDE
    NON_PARAM --> DECIDE
    DECIDE -->|"Đạt chuẩn"| SIG
    DECIDE -->|"Không đạt"| NOT_SIG

    style STAT_DECISION fill:none,stroke:#6366f1,stroke-width:1.75px
    style INPUT_D fill:none,stroke:#64748b,stroke-width:1.5px
    style TEST_NORM fill:none,stroke:#f59e0b,stroke-width:1.75px
    style PARAM fill:none,stroke:#3b82f6,stroke-width:1.5px
    style NON_PARAM fill:none,stroke:#8b5cf6,stroke-width:1.5px
    style DECIDE fill:none,stroke:#f59e0b,stroke-width:1.75px
    style SIG fill:none,stroke:#10b981,stroke-width:2px
    style NOT_SIG fill:none,stroke:#f43f5e,stroke-width:1.5px
```

```python
from scipy import stats

def statistical_significance_test(accs_a: list, accs_b: list) -> dict:
    diffs = np.array(accs_a) - np.array(accs_b)
    
    # 1. Kiểm tra giả định phân phối chuẩn bằng Shapiro-Wilk
    _, p_norm = stats.shapiro(diffs)
    
    # 2. Chọn phép kiểm định phù hợp
    if p_norm > 0.05:
        stat, p_val = stats.ttest_rel(accs_a, accs_b)
        test_type = "Paired Student's t-Test"
    else:
        stat, p_val = stats.wilcoxon(accs_a, accs_b)
        test_type = "Wilcoxon Signed-Rank Test"
        
    return {
        'test_applied': test_type,
        'statistic': stat,
        'p_value': p_val,
        'is_statistically_significant': bool(p_val < 0.05),
        'mean_improvement': float(np.mean(diffs))
    }
```

### 3.1. Hiệu Chỉnh So Sánh Bội (Bonferroni & Benjamini-Hochberg FDR)
Khi so sánh đồng thời $M$ cặp mô hình, xác suất xuất hiện sai lầm loại I (báo cáo vượt trội giả mạo) tăng theo công thức:

$$\alpha_{\text{total}} = 1 - (1 - \alpha)^M$$

* **Hiệu chỉnh Bonferroni:** Chia ngưỡng ý nghĩa: $\alpha_{\text{adjusted}} = \frac{0.05}{M}$.
* **Hiệu chỉnh Benjamini-Hochberg (FDR):** Kiểm soát tỷ lệ phát hiện sai trên các giá trị $p\text{-value}$ được sắp xếp tăng dần.

---

## 4. Nghiên Cứu Triệt Tiêu (Ablation Study) & Khả Năng Giải Thích (XAI)

**Ablation Study** là kỹ thuật tháo rời từng thành phần của kiến trúc để đo lường chính xác giá trị đóng góp độc lập:

### 4.1. Bảng Ma Trận Nghiên Cứu Triệt Tiêu (Benchmark DEAP)

| Cấu Hình Kiến Trúc | Accuracy | F1-Score | Mức Độ Suy Giảm ($\Delta$) | Giá Trị $p$-Value |
| :---: | :---: | :---: | :---: | :---: |
| <span class="badge badge--emerald">Mô hình hoàn chỉnh (Full MAS)</span> | **$82.5\%$** | **$0.814$** | **Baseline** | — |
| <span class="badge badge--primary">Triệt tiêu Adaptation Agent</span> | $76.5\%$ | $0.752$ | $-6.0\%$ | $p < 0.001$ |
| <span class="badge badge--cyan">Triệt tiêu Cross-Modal Attention</span> | $77.2\%$ | $0.760$ | $-5.3\%$ | $p = 0.002$ |
| <span class="badge badge--purple">Triệt tiêu Dynamic Graph CNN (DGCNN)</span> | $78.4\%$ | $0.771$ | $-4.1\%$ | $p = 0.008$ |
| <span class="badge badge--amber">Triệt tiêu Tín hiệu ngoại biên (AUX)</span> | $75.0\%$ | $0.738$ | $-7.5\%$ | $p < 0.001$ |
| <span class="badge badge--rose">Baseline CNN truyền thống</span> | $62.0\%$ | $0.605$ | $-20.5\%$ | $p < 0.001$ |

---

## 5. Trực Quan Hóa Không Gian Biểu Diễn Ẩn Bằng t-SNE

```python
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def plot_tsne_clusters(features: np.ndarray, labels: np.ndarray):
    """
    Trực quan hóa không gian vector ẩn để kiểm tra mức độ phân tách cụm cảm xúc.
    """
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    embeds_2d = tsne.fit_transform(features)
    
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(embeds_2d[:, 0], embeds_2d[:, 1], c=labels, cmap='viridis', alpha=0.8)
    plt.colorbar(scatter, label='Emotion Class ID')
    plt.title("t-SNE Latent Space Clustering (Subject-Independent)")
    plt.xlabel("t-SNE Component 1")
    plt.ylabel("t-SNE Component 2")
    plt.grid(True, linestyle='--', alpha=0.5)
```

---

## 6. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

### Tình Huống Sự Cố Thực Tế:
<span class="badge badge--rose">🕒 05:20 AM</span> Một bài báo khoa học về BCI nhận dạng cảm xúc công bố mô hình đạt độ chính xác kỷ lục **$96.8\%$** khi so sánh đồng thời 12 biến thể kiến trúc khác nhau trên tập dữ liệu DEAP. Tuy nhiên, khi gửi bài báo đến hội đồng thẩm định của tạp chí hàng đầu (*IEEE Transactions on Affective Computing*), bài báo bị từ chối thẳng thừng (*Desk Reject*) với kết luận mắc lỗi **P-Hacking** và **So sánh bội không hiệu chỉnh** (**Uncorrected Multiple Hypothesis Testing**).

### Hậu Quả & Log Lỗi Thực Tế:
Phân tích thống kê từ hội đồng phản biện chỉ ra rằng trong số 12 bài kiểm định được nhóm tác giả tuyên bố $p < 0.05$, có tới 9 bài kiểm định trở thành không có ý nghĩa sau khi áp dụng chuẩn Bonferroni:

```text
================================================================================
PEER REVIEW AUDIT: MULTIPLE HYPOTHESIS TESTING VIOLATION (P-HACKING)
================================================================================
[WARNING] Number of Model Comparisons: M = 12 pairwise hypothesis tests
[WARNING] Nominal Alpha Threshold: alpha = 0.05
[FATAL] Family-Wise Error Rate (FWER): alpha_total = 1 - (1 - 0.05)^12 = 45.96%!

>> MULTIPLE COMPARISON AUDIT TABLE:
   - Comparison 01 (Mamba vs CNN)      : p = 0.0002  < 0.00416  [VALID SIGNIFICANCE]
   - Comparison 02 (EEGNet vs LSTM)    : p = 0.0120  > 0.00416  [FALSE DISCOVERY / TYPE I ERROR]
   - Comparison 03 (Cross-Attn vs Concat): p = 0.0340 > 0.00416 [FALSE DISCOVERY / TYPE I ERROR]
   - Comparison 04 (Gated vs Linear)   : p = 0.0480  > 0.00416  [FALSE DISCOVERY / TYPE I ERROR]

[CONCLUSION] The claimed superiority of sub-modules was purely driven by random noise!
The authors committed P-Hacking by publishing nominal p-values without Bonferroni correction.
================================================================================
```

### 5-Whys Root Cause Analysis:
1. <span class="badge badge--primary">Why 1</span> **Tại sao bài báo bị hội đồng khoa học từ chối?** $\rightarrow$ Do các tuyên bố vượt trội giữa các biến thể mô hình không có ý nghĩa thống kê thực thụ sau khi hiệu chỉnh so sánh bội.
2. <span class="badge badge--primary">Why 2</span> **Tại sao nhóm tác giả lại thấy $p < 0.05$ trong kết quả ban đầu?** $\rightarrow$ Vì khi thực hiện 12 phép kiểm định độc lập, xác suất xảy ra ít nhất một kết quả dương tính giả lên tới **$45.96\%$**.
3. <span class="badge badge--primary">Why 3</span> **Tại sao nhóm tác giả không áp dụng hiệu chỉnh Bonferroni?** $\rightarrow$ Do thiếu kiến thức về thống kê đa biến và ngộ nhận rằng kiểm định t-Test thông thường $p < 0.05$ là đủ cho mọi bài toán.
4. <span class="badge badge--primary">Why 4</span> **Tại sao việc báo cáo sai lệch này lại nguy hiểm trong y sinh?** $\rightarrow$ Vì nó tạo ra ảo tưởng về các module không có tác dụng thực tế, gây lãng phí tài nguyên nghiên cứu khi áp dụng lâm sàng.
5. <span class="badge badge--emerald">Root Cause Remedy</span> **Biện pháp khắc phục chuẩn nghiên cứu khoa học:**
   - <span class="badge badge--rose">Bắt Buộc Hiệu Chỉnh Bonferroni / FDR</span> Khi so sánh $M$ mô hình, điều chỉnh ngưỡng ý nghĩa thành $\alpha_{\text{adj}} = \frac{0.05}{M}$ hoặc dùng kiểm định Benjamini-Hochberg.
   - <span class="badge badge--cyan">Thực Hiện Kiểm Định Repeated Measures ANOVA</span> Dùng ANOVA đa biến trước khi chạy các phép so sánh cặp Post-Hoc.
   - <span class="badge badge--emerald">Công Bố Ma Trận Ablation Study Đầy Đủ</span> Báo cáo đầy đủ Mean $\pm$ STD, giá trị Effect Size (Cohen’s $d$) và mã nguồn tái lập.

---

## 7. Câu Hỏi Tự Kiểm Tra Chuyên Sâu (Q&A Accordion)

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q01</span>
    <span>Tại sao chỉ số Cohen’s Kappa lại quan trọng hơn Accuracy trên các tập dữ liệu cảm xúc mất cân bằng?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  <div style="margin-bottom: 8px;">Nếu một tập dữ liệu có 80% mẫu thuộc trạng thái Bình thường, một mô hình lười biếng luôn đoán lớp Bình thường sẽ đạt Accuracy 80% nhưng thực chất không có năng lực nhận diện cảm xúc. <b style="color: var(--accent-primary);">Cohen’s Kappa trừ đi xác suất trùng hợp ngẫu nhiên p_e</b>, do đó trong tình huống này Kappa sẽ rơi về mức 0.0, vạch trần ngay lập tức sự yếu kém của mô hình.</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q02</span>
    <span>Khi nào bắt buộc phải sử dụng kiểm định phi tham số Wilcoxon Signed-Rank thay cho Paired t-Test?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  <div style="margin-bottom: 8px;">Paired t-Test đòi hỏi giả định hiệu số độ chính xác giữa hai mô hình phải tuân theo phân phối chuẩn Gaussian (kiểm tra qua Shapiro-Wilk với p &gt; 0.05). Khi số lượng đối tượng kiểm thử nhỏ (N &lt; 15) hoặc <b style="color: var(--accent-amber);">phân phối hiệu số bị lệch/chứa ngoại lai</b>, bắt buộc phải chuyển sang kiểm định phi tham số Wilcoxon Signed-Rank Test dựa trên thứ hạng (Rank) để kết luận không bị sai lệch.</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q03</span>
    <span>Hiện tượng rò rỉ dữ liệu thời gian (Temporal Data Leakage) xảy ra như thế nào nếu dùng Random K-Fold trên chuỗi EEG?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  <div style="margin-bottom: 8px;">Các cửa sổ trượt liên tiếp gối nhau 50% trong cùng một phút ghi có tính tự tương quan (Autocorrelation) sinh học cực cao. Khi trộn ngẫu nhiên vào tập Train và Test, mô hình thực chất <b style="color: var(--accent-rose);">chỉ đang thực hiện phép nội suy giữa các điểm dữ liệu lân cận</b> chứ không học được quy luật cảm xúc tổng quát, dẫn tới độ chính xác ảo trên 95% nhưng sập hoàn toàn ở thực tế.</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q04</span>
    <span>Mục đích của việc hiệu chỉnh Bonferroni trong các nghiên cứu so sánh đa mô hình là gì?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  <div style="margin-bottom: 8px;">Khi thực hiện M phép kiểm định cặp độc lập, xác suất bắt gặp một kết quả dương tính giả do ngẫu nhiên tăng vọt. Hiệu chỉnh Bonferroni <b style="color: var(--accent-emerald);">hạ ngưỡng ý nghĩa xuống alpha_adj = 0.05 / M</b>, kiểm soát chặt chẽ tỷ lệ sai lầm loại I của toàn bộ nghiên cứu không vượt quá 5%.</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q05</span>
    <span>Sự khác biệt giữa Macro-Averaged F1 và Weighted-Averaged F1 là gì?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  <div style="margin-bottom: 8px;"><b style="color: var(--accent-primary);">Macro-F1</b> tính trung bình cộng đơn thuần F1-score của tất cả các lớp, gán trọng số ngang hàng cho mọi trạng thái cảm xúc (dù lớp đó có ít mẫu). Trong khi đó, <b style="color: var(--accent-cyan);">Weighted-F1</b> nhân trọng số theo tỷ lệ số lượng mẫu thực tế của từng lớp, khiến kết quả bị chi phối bởi các lớp chiếm đa số. Trong nghiên cứu y sinh, Macro-F1 luôn được ưu tiên để bảo vệ các lớp cảm xúc hiếm gặp.</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q06</span>
    <span>Nghiên cứu triệt tiêu (Ablation Study) đóng vai trò gì trong việc chứng minh tính hợp lý của kiến trúc đa tác tử?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  <div style="margin-bottom: 8px;">Ablation Study chứng minh rằng hiệu năng vượt bậc của hệ thống đến từ sự phối hợp khoa học của các thành phần (như Cross-Attention, Gated Fusion, DGCNN) chứ không phải do may mắn hoặc do tăng số lượng tham số ngẫu nhiên. Nó cung cấp bằng chứng định lượng chính xác <b style="color: var(--accent-emerald);">tỷ lệ đóng góp phần trăm của từng module vào độ chính xác chung</b>.</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q07</span>
    <span>Thuật toán t-SNE giúp đánh giá chất lượng của mô hình học sâu như thế nào?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  <div style="margin-bottom: 8px;">t-SNE chiếu không gian vector ẩn nhiều chiều (128d) xuống mặt phẳng 2D bảo toàn cấu trúc lân cận. Trên biểu đồ t-SNE: (1) Nếu các điểm dữ liệu <b style="color: var(--accent-emerald);">tự động gom thành các cụm màu sắc rõ ràng theo nhãn cảm xúc</b>, mô hình đã học thành công biểu diễn cảm xúc phân tách; (2) Nếu các điểm gom theo ID người đo, mô hình đã bị học vẹt sinh trắc học cá nhân.</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q08</span>
    <span>Tại sao cần báo cáo độ lệch chuẩn (STD) bên cạnh giá trị trung bình (Mean) trong giao thức LOSO?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  <div style="margin-bottom: 8px;">Tín hiệu não bộ có phương sai rất lớn giữa các đối tượng. Một mô hình có độ chính xác trung bình 80% nhưng STD = 15% đồng nghĩa với việc có người đạt 95% nhưng có người chỉ đạt 50% (rất thiếu ổn định). <b style="color: var(--accent-cyan);">Độ lệch chuẩn STD đo lường tính đồng đều và độ tin cậy</b> của giải thuật trên toàn bộ quần thể người dùng.</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q09</span>
    <span>Làm thế nào để thiết kế một bài kiểm tra tính bền vững khi mất kênh (Missing Modality Robustness)?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  <div style="margin-bottom: 8px;">Mô phỏng lần lượt các kịch bản lỗi phần cứng trong tập Test: (1) Gán vector 0 cho kênh EEG (mất điện não); (2) Gán 0 cho ECG; (3) Gán 0 cho GSR; (4) Ngẫu nhiên mất 20% - 50% số kênh. Đánh giá mức độ suy giảm F1-score để khẳng định khả năng tự phục hồi của Orchestrator Agent.</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q10</span>
    <span>Bốn tiêu chí bắt buộc để một nghiên cứu BCI đạt chuẩn khả năng tái lập kết quả (Reproducibility) là gì?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  <div style="margin-bottom: 8px;">4 tiêu chí chuẩn mực gồm: (1) <b style="color: var(--accent-primary);">Công bố đầy đủ mã nguồn và Random Seed</b>; (2) <b style="color: var(--accent-emerald);">Mô tả chi tiết pipeline tiền xử lý</b> (tần số lọc, thứ tự chia đoạn); (3) <b style="color: var(--accent-cyan);">Sử dụng các bộ dữ liệu Benchmark công khai</b> (DEAP, SEED); và (4) <b style="color: var(--accent-amber);">Tuân thủ giao thức kiểm chuẩn LOSO không rò rỉ dữ liệu</b>.</div>
</div>
</details>

---

## 8. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

Nắm vững các phương pháp đánh giá chuẩn mực từ **Giao thức LOSO**, **Hệ số Cohen’s Kappa**, **Kiểm định Paired t-Test / Wilcoxon**, **Ablation Study** đến **Trực quan hóa t-SNE** là thước đo bảo chứng chất lượng và giá trị học thuật cho toàn bộ công trình AI y sinh.

> [!TIP]
> **BÀI HỌC TIẾP THEO:**
> Trong **[[Bài 08] Các Bộ Dữ Liệu Benchmark Phổ Biến: Khai Thác Chuẩn DEAP, SEED, DREAMER, MAHNOB-HCI & FACED](eeg-08-08-cac-bo-du-lieu-pho-bien.html)**, chúng ta sẽ đi sâu vào thực hành khai thác 5 kho dữ liệu chuẩn mực thế giới: Nạp cấu trúc tệp `.mat` / `.pkl`, chuẩn hóa siêu dữ liệu (*Metadata*), tiền xử lý các kịch bản kích thích video/âm nhạc và thiết lập môi trường Benchmark chuẩn.
{% endraw %}
