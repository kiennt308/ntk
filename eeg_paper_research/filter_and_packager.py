#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Multimodal Biosignal Emotion Recognition - PhD Roadmap Filter & Packager
Đề tài: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức
=============================================================================
Tự động phân loại, chấm điểm tương quan và đóng gói các bài báo nghiên cứu
theo 5 Trục chính của Luận án Tiến sĩ:

  Notebook 01: Biosignal Emotion Recognition (Single Modalities: EEG, ECG, EDA/GSR, EMG, PPG, Respiration)
  Notebook 02: Multimodal Emotion Recognition (Datasets: DEAP, DREAMER, AMIGOS, MAHNOB-HCI, CASE, K-EmoCon...)
  Notebook 03: Multi-Task Learning for Emotion (Valence-Arousal Regression + Classification, Multi-task Loss...)
  Notebook 04: Multi-Branch & Multimodal Fusion Architectures (Cross-modal Attention, Shared-Private, MoE, Transformers...)
  Notebook 05: Generalization, Robustness & Missing Modalities (Cross-subject, Cross-dataset, Incomplete Multimodal, Noisy Sensors...)

Tính năng:
  - Phân tích Title + Abstract của toàn bộ bài báo trong checklist.db.
  - Tuyển chọn Top 25-45 bài báo tốt nhất cho từng Notebook.
  - Chuẩn hóa tên file PDF theo chuẩn học thuật: [Năm]_[Tác giả chính]_[Tiêu đề].pdf
  - Tự động sinh file `00_NOTEBOOKLM_PROMPTS_AND_INDEX.md` chứa:
    + Danh mục bài báo trong Notebook kèm DOI/URL.
    + Bộ Prompt Master Class 20 tiêu chí bóc tách sâu.
    + Prompt phân loại mức độ liên quan (A, B, C, D, E).
    + Ma trận nghiên cứu Multimodal Research Matrix.
    + Khung giả thuyết (H1-H6) và câu hỏi nghiên cứu (RQ1-RQ6).
=============================================================================
"""

import os
import re
import sys
import json
import shutil
import sqlite3
import argparse
from datetime import datetime

# Đảm bảo in UTF-8 mượt mà trên Windows console
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# =============================================================================
# CẤU HÌNH 5 NOTEBOOKS CHUẨN ĐỀ TÀI MULTIMODAL MULTI-TASK MULTI-BRANCH
# =============================================================================
MULTIMODAL_ROADMAP_TRACKS = {
    "nb_01": {
        "folder_name": "notebook_01_Biosignal_Emotion_Recognition",
        "title": "Notebook 01: Biosignal Modality Foundations (EEG, ECG, EDA, EMG, PPG, Respiration)",
        "topic_focus": "Nghiên cứu cơ sở sinh lý và đặc trưng của từng phương thức tín hiệu đơn lẻ (Brain activity, Cardiac activity, Autonomic nervous system, Muscle activity).",
        "keywords": {
            "high": [
                "ecg emotion recognition", "eda emotion recognition", "gsr emotion recognition",
                "emg emotion recognition", "ppg emotion recognition", "respiration emotion recognition",
                "galvanic skin response", "electrodermal activity", "photoplethysmography",
                "heart rate variability", "hrv emotion", "physiological signals emotion", "peripheral signals"
            ],
            "medium": [
                "eeg emotion recognition", "electroencephalogram", "cardiac activity",
                "autonomic nervous system", "skin conductance", "electromyography", "blood volume pulse",
                "bvp", "physiological emotion", "single modality", "biosignal features"
            ],
            "bonus": [
                "feature extraction", "time-domain", "frequency-domain", "spectral power",
                "wavelet", "differential entropy", "skin temperature"
            ]
        }
    },
    "nb_02": {
        "folder_name": "notebook_02_Multimodal_Emotion_Recognition",
        "title": "Notebook 02: Multimodal Emotion Recognition & Benchmark Datasets",
        "topic_focus": "Nghiên cứu kết hợp đa phương thức (EEG + ECG, EEG + EDA/GSR, EEG + EMG, Peripheral) và các bộ benchmark datasets kinh điển (DEAP, AMIGOS, DREAMER, MAHNOB-HCI, CASE, K-EmoCon, ASCERTAIN).",
        "keywords": {
            "high": [
                "multimodal emotion recognition", "multimodal biosignals", "multimodal physiological",
                "eeg and ecg", "eeg and eda", "eeg and gsr", "eeg and peripheral", "eeg-ecg", "eeg-eda",
                "deap dataset", "amigos dataset", "dreamer dataset", "mahnob-hci", "case dataset",
                "k-emocon", "ascertain dataset", "mped dataset"
            ],
            "medium": [
                "multimodal affective computing", "multimodal fusion emotion", "bimodal emotion",
                "multi-sensor emotion", "heterogeneous biosignals", "wearable multimodal",
                "valence arousal dominance", "sam ratings", "circumplex model"
            ],
            "bonus": [
                "synchronization", "sampling rate alignment", "sensor fusion", "multimodal benchmark"
            ]
        }
    },
    "nb_03": {
        "folder_name": "notebook_03_Multi_Task_Learning_Emotion",
        "title": "Notebook 03: Multi-Task Learning & Emotion Dimensionality",
        "topic_focus": "Nghiên cứu học đa nhiệm vụ: dự đoán đồng thời Valence/Arousal/Dominance (Regression) kết hợp Phân loại cảm xúc rời rạc (Classification), Multi-task loss functions, Dynamic task weighting, Shared representation.",
        "keywords": {
            "high": [
                "multi-task learning", "multitask learning", "multi-task emotion", "multi-task affective",
                "joint classification and regression", "valence arousal joint", "valence and arousal multi-task",
                "multi-label emotion", "auxiliary task", "task weighting", "gradnorm", "uncertainty weighting",
                "shared representation multi-task"
            ],
            "medium": [
                "multi-task", "multitask", "joint learning", "multi-objective", "valence regression",
                "arousal regression", "discrete emotion classification", "loss balance", "task correlation",
                "shared latent space", "multi-output"
            ],
            "bonus": [
                "negative transfer", "task interference", "joint loss", "multi-branch multi-task"
            ]
        }
    },
    "nb_04": {
        "folder_name": "notebook_04_Multi_Branch_Fusion_Architecture",
        "title": "Notebook 04: Multi-Branch & Advanced Fusion Architectures",
        "topic_focus": "Kiến trúc mạng đa nhánh (Multi-branch CNN, Multi-stream Transformer), Biểu diễn Riêng-Chung (Shared-Private Networks), Cross-modal Attention, Cross-modal Transformer, Mixture of Experts (MoE), Hierarchical / Adaptive Fusion.",
        "keywords": {
            "high": [
                "multi-branch", "multibranch", "multi-stream", "multistream", "cross-modal attention",
                "cross-modal transformer", "cross attention", "shared-private", "shared and private",
                "modality-specific branch", "mixture of experts", "moe", "hierarchical fusion",
                "adaptive fusion", "intermediate fusion", "dual-branch", "multi-branch cnn"
            ],
            "medium": [
                "early fusion", "late fusion", "hybrid fusion", "tensor fusion", "feature fusion",
                "co-attention", "modal interaction", "modality encoder", "representation alignment",
                "transformer fusion", "graph fusion", "attention fusion"
            ],
            "bonus": [
                "cross-modal interaction", "modality-specific encoder", "shared encoder", "feature aggregation"
            ]
        }
    },
    "nb_05": {
        "folder_name": "notebook_05_Generalization_Robustness_Missing_Modality",
        "title": "Notebook 05: Generalization, Robustness & Missing/Noisy Modalities",
        "topic_focus": "Khả năng khái quát hóa và độ bền vững: Cross-subject, Cross-dataset, LOSO, Xử lý thiếu phương thức (Incomplete/Missing Modality Imputation), Tín hiệu nhiễu cảm biến, Domain Adaptation, Domain Generalization.",
        "keywords": {
            "high": [
                "missing modality", "incomplete multimodal", "missing sensors", "modality dropout",
                "noisy biosignals", "cross-subject generalization", "cross-dataset generalization",
                "leave-one-subject-out", "loso", "subject-independent multimodal", "domain adaptation multimodal",
                "domain generalization multimodal", "modality hallucination", "robust multimodal"
            ],
            "medium": [
                "cross-subject", "cross-dataset", "subject variability", "sensor failure", "sensor noise",
                "incomplete data", "distribution shift", "transfer learning multimodal", "unsupervised domain adaptation",
                "inter-subject variability"
            ],
            "bonus": [
                "robustness", "missing channel", "modality-agnostic", "zero-shot", "few-shot"
            ]
        }
    }
}


# =============================================================================
# TEMPLATE PROMPT MASTER CLASS CHUẨN ĐỀ TÀI MULTIMODAL MULTI-TASK MULTI-BRANCH
# =============================================================================
NOTEBOOKLM_PROMPT_TEMPLATE = """# 🧠 Google NotebookLM Prompts & Research Matrix Master Guide
## 🎓 ĐỀ TÀI TIẾN SĨ: "Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức"
### 📂 Notebook Focus: {track_title}
### 🎯 Mục tiêu: {track_focus}
---

## 📌 DANH SÁCH BÀI BÁO ĐÃ NẠP TRONG NOTEBOOK NÀY ({paper_count} bài)

| STT | Năm | Tác giả chính | Tiêu đề bài báo | Nguồn / DOI / URL | File PDF Đã Chuẩn Hóa |
| :--- | :--- | :--- | :--- | :--- | :--- |
{paper_table_rows}

---

## 🚀 QUY TRÌNH HỎI NOTEBOOKLM CHUẨN NGHIÊN CỨU SINH (PhD)

> **NGUYÊN TẮC CỐT LÕI:**
> 1. Không bao giờ chỉ yêu cầu "Tóm tắt bài này".
> 2. Đọc và bóc tách theo đúng lăng kính của đề tài: **Multimodal Biosignals + Multi-Branch Architecture + Multi-Task Learning**.
> 3. Luôn yêu cầu trích dẫn chính xác trang, mục, bảng, hình vẽ (**Exact Citation**).
> 4. Tuyệt đối cấm AI tự suy diễn thông tin tác giả không viết (**Do not infer missing experimental details**).
> 5. Phân loại thông tin thành 3 mức: `[EXPLICIT]`, `[SUPPORTED]`, `[INFERRED]`.

---

### 🔹 PROMPT 1: Bóc Tách Chuyên Sâu 20 Tiêu Chí Của Paper Theo Đề Tài

```text
Analyze this paper specifically from the perspective of my PhD research topic:
"Multi-task multi-branch architecture for emotion recognition from multimodal biosignals."

Do not merely summarize the paper. Extract the following 20 structured items:

1. Biosignal modalities used (EEG, ECG, EDA/GSR, EMG, PPG, Respiration, etc.)
2. Dataset(s) and benchmark details (DEAP, AMIGOS, DREAMER, MAHNOB-HCI, etc.)
3. Emotion representation (Valence-Arousal continuous vs. Discrete categories)
4. Prediction tasks (Single-task vs. Multi-task: Valence/Arousal regression + Emotion classification)
5. Modality-specific encoder architecture for each branch
6. Shared encoder or shared representation (if any)
7. Multi-branch architecture design (How branches are structured per modality)
8. Fusion strategy (Early, Intermediate, Late, Cross-modal Attention, Cross-modal Transformer, MoE)
9. Multi-task learning strategy and auxiliary objectives
10. Loss functions (Multi-task loss formulation)
11. Task weighting mechanism (Fixed weights, Dynamic weighting, GradNorm, Uncertainty weighting)
12. Cross-modal interaction mechanisms (How information is exchanged between modalities)
13. Evaluation protocol (Subject-dependent vs. Subject-independent / LOSO)
14. Missing or noisy modality handling (Is incomplete multimodal data addressed?)
15. Baseline models compared against
16. Ablation studies (What specific modules/branches were ablated and what did it prove?)
17. Computational complexity (Parameter count, FLOPs, Inference latency)
18. Main claimed technical contribution
19. Explicit limitations acknowledged by the authors
20. Potential research gaps directly relevant to my PhD thesis

Rules:
- For every claim, cite the exact page, section, table, or figure.
- If information is not reported, explicitly write "Not reported".
- Do not infer missing experimental details.
```

---

### 🔹 PROMPT 2: Đánh Giá Mức Độ Liên Quan Trực Tiếp Với Đề Tài PhD

```text
Compared with my PhD research topic:
"Multi-task multi-branch architecture for emotion recognition from multimodal biosignals"

Which parts of this paper are directly relevant, which parts are supporting literature, and which parts are unrelated?

Classify into:
A. Directly relevant (Architecture, Multimodal fusion, Multi-task, or Biosignal modeling)
B. Supporting literature (Dataset insights, Preprocessing pipelines, Feature engineering)
C. Potential baseline (A model to implement and compare against in my experimental section)
D. Potential competing approach (Alternative methodology solving the same challenge)
E. Not relevant (Out of scope)

For each classification, explain the concrete rationale with specific citations.
```

---

### 🔹 PROMPT 3: Kiểm Toán Nguy Cơ Rò Rỉ Dữ Liệu & Tính Toàn Vẹn Thực Nghiệm

```text
Audit this paper for potential data leakage, invalid experimental setups, or inflated accuracy in multimodal emotion recognition.

Check carefully:
1. When was temporal windowing/segmentation performed (Before or after train/test split)?
2. Were multi-sensor signals synchronized before windowing?
3. Can windows from the same subject or same trial appear in both train and test sets?
4. Was normalization (e.g. z-score, min-max) fitted ONLY on the training set?
5. Was cross-validation strictly Subject-Independent / Leave-One-Subject-Out (LOSO)?
6. Did multimodal fusion introduce lookahead or data leakage across modalities?

Classify state: [CLEAN], [POTENTIAL LEAKAGE RISK], or [INSUFFICIENT DETAILS REPORTED].
```

---

### 🔹 PROMPT 4: Xuất Ma Trận Nghiên Cứu Đa Bài Báo (Multimodal Research Matrix)

```text
Compare all papers in this notebook.

Create a comprehensive Markdown Literature Matrix with the following exact columns:
1. Paper (First Author & Year)
2. Modalities (EEG/ECG/EDA/EMG/PPG/Resp)
3. Dataset & Subjects
4. Target Tasks (Classification / Regression / Joint Multi-task)
5. Emotion Target (Valence / Arousal / Discrete)
6. Branch Architecture (Modality-specific encoders)
7. Fusion Mechanism (Early/Mid/Late/Cross-modal Attention/Transformer/MoE)
8. Shared vs. Private Representation (Is there explicit disentanglement?)
9. Multi-Task Strategy & Loss Weighting (Fixed / Dynamic)
10. Evaluation Setup (Subject-dependent / LOSO / Cross-dataset)
11. Missing Modality Support (Yes / No / Method)
12. Key Performance (Acc %, F1 %, RMSE)
13. Model Complexity (Params, Latency)
14. Main Contribution
15. Key Limitation & Unresolved Gap

Format as a clean, highly structured Markdown table.
```

---

### 🔹 PROMPT 5: Khai Thác Research Gap Tại Điểm Giao Thoa (Intersection Gap Discovery)

```text
Based strictly and ONLY on the papers in this notebook:

Identify the unresolved research gaps at the INTERSECTION of:
[Multimodal Biosignals] x [Multi-Branch Architectures] x [Multi-Task Learning] x [Generalization & Missing Modalities]

Group the gaps into:
1. Modality Discrepancy & Fusion Bottlenecks (How to fuse signals with different temporal resolutions and physical dynamics?)
2. Shared vs. Private Feature Disentanglement Gaps (How to separate common emotional states from sensor-specific noise?)
3. Multi-Task Negative Transfer & Gradient Conflict Gaps (How to prevent emotion classification from degrading valence/arousal regression?)
4. Cross-Subject & Cross-Dataset Generalization Gaps under Multimodal Inputs
5. Robustness to Incomplete / Missing / Noisy Modalities in Real-World BCI

MANDATORY CITATION RULE:
Classify every statement as:
- [EXPLICIT]: Directly stated by authors (cite Paper & Section).
- [SUPPORTED]: Strongly supported by experimental drops or ablation failure in the paper.
- [INFERRED]: Inferred from cross-comparing limitations across multiple papers.
```

---

### 🔹 PROMPT 6: Kết Nối Với Khung Giả Thuyết PhD (Hypotheses H1 - H6 Validation)

```text
Based on the evidence from the papers in this notebook, analyze the empirical support for the following 6 PhD Hypotheses:

- Hypothesis H1: Multimodal biosignals outperform any single modality in emotion recognition.
- Hypothesis H2: Modality-specific branches outperform a single shared encoder for heterogeneous biosignals.
- Hypothesis H3: Joint multi-task learning (Valence + Arousal + Emotion) produces better latent representations than single-task learning.
- Hypothesis H4: Cross-modal attention/transformer fusion outperforms simple concatenation or tensor fusion.
- Hypothesis H5: Disentangled shared-private representations improve cross-subject generalization.
- Hypothesis H6: A specialized multi-branch architecture can maintain robust performance even when 1-2 modalities are missing during inference.

For each hypothesis:
1. Which papers provide direct supporting evidence?
2. Which papers report conflicting or negative results?
3. Where does the empirical gap remain open for my thesis to prove?
```

---

### 🔹 PROMPT 7: Chuyển Giao Sang ChatGPT Để Thiết Kế Kiến Trúc & Thí Nghiệm (Bridge to ChatGPT)

> Sau khi NotebookLM xuất kết quả từ Prompt 4, 5, 6, copy toàn bộ nội dung đó và gửi vào ChatGPT cùng với prompt sau:

```text
Tôi là nghiên cứu sinh tiến sĩ (PhD candidate). Đề tài luận án của tôi là:
"Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức"
(Multi-task multi-branch architecture for emotion recognition from multimodal biosignals).

Dưới đây là Literature Matrix, Gap Analysis và Bằng chứng thực nghiệm đã được trích xuất chính xác bằng NotebookLM:

[DÁN KẾT QUẢ TỪ NOTEBOOKLM VÀO ĐÂY]

Hãy đóng vai trò là Giáo sư Hướng dẫn (PhD Advisor) và giúp tôi:
1. Xây dựng Research Questions (RQ1 - RQ6) và ánh xạ tương ứng vào 6 Giả thuyết khoa học (H1 - H6).
2. Thiết kế chi tiết Kiến trúc mô hình đề xuất (Proposed Multi-Branch Multi-Task Network):
   - Thiết kế nhánh EEG (Spatial-Temporal), ECG (HRV/1D-CNN), EDA (Continuous Conductance).
   - Thiết kế khối Disentanglement (Shared vs. Modality-Private features).
   - Thiết kế khối Cross-Modal Attention Fusion.
   - Thiết kế Multi-Task Output Heads (Valence/Arousal regression + Discrete emotion classification).
   - Thiết kế Dynamic Loss Weighting để tránh Gradient Conflict.
   - Thiết kế cơ chế Masking / Modality Dropout để chống Missing Modality.
3. Lập kế hoạch thực nghiệm (Datasets: DEAP, AMIGOS, DREAMER, MAHNOB-HCI; Protocols: LOSO; Baselines: Single-branch, Concat fusion, Single-task).
4. Thiết kế ma trận Ablation Study để chứng minh tính độc lập của từng module.
5. Phân bổ lộ trình 3 bài báo Q1 (Core Method -> Generalization & Fusion -> Edge & Missing Modality).
```
"""


# =============================================================================
# HÀM CHUẨN HÓA VÀ XỬ LÝ DỮ LIỆU
# =============================================================================
def sanitize_filename(text, max_length=60):
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = re.sub(r"\s+", "_", text).strip("_")
    if len(text) > max_length:
        text = text[:max_length].rstrip("_")
    return text


def extract_first_author(authors_str):
    if not authors_str:
        return "Unknown"
    first = re.split(r",| and |;", authors_str)[0].strip()
    parts = first.split()
    if parts:
        clean_name = re.sub(r"[^\w\-]", "", parts[-1])
        return clean_name if clean_name else "Author"
    return "Author"


def calculate_relevance_score(text, keywords_dict):
    text_lower = text.lower()
    score = 0
    matched_keywords = []

    for kw in keywords_dict.get("high", []):
        count = text_lower.count(kw.lower())
        if count > 0:
            score += min(count, 3) * 6
            matched_keywords.append(kw)

    for kw in keywords_dict.get("medium", []):
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        matches = len(re.findall(pattern, text_lower))
        if matches > 0:
            score += min(matches, 3) * 3
            matched_keywords.append(kw)

    for kw in keywords_dict.get("bonus", []):
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        matches = len(re.findall(pattern, text_lower))
        if matches > 0:
            score += min(matches, 2) * 1

    return score, matched_keywords


# =============================================================================
# CHƯƠNG TRÌNH CHÍNH
# =============================================================================
class MultimodalRoadmapPackager:
    def __init__(self, db_path="downloaded_papers/checklist.db", output_dir="notebooklm_workspace", max_per_track=40):
        self.db_path = db_path
        self.output_dir = output_dir
        self.max_per_track = max_per_track
        self.papers = []

    def load_papers_from_db(self):
        if not os.path.exists(self.db_path):
            print(f"[!] Không tìm thấy database tại: {self.db_path}")
            return False

        print(f"[*] Đang đọc dữ liệu từ database: {self.db_path}...")
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT id, source, doi, title, authors, year, journal, pdf_url, local_path, file_size, abstract, landing_url
            FROM papers
            WHERE status = 'Success' AND local_path IS NOT NULL AND local_path != '';
        """)
        rows = cur.fetchall()
        conn.close()

        self.papers = []
        for r in rows:
            p = dict(r)
            local_file = p.get("local_path", "")
            if os.path.exists(local_file) and os.path.getsize(local_file) > 1024:
                self.papers.append(p)

        print(f"[+] Tìm thấy {len(self.papers)} bài báo PDF hợp lệ trên đĩa cứng.")
        return True

    def categorize_and_package(self):
        if not self.papers:
            print("[!] Không có bài báo nào để xử lý.")
            return

        # Dọn dẹp cấu trúc thư mục cũ nếu có để đồng bộ sang chuẩn 5 Notebooks
        os.makedirs(self.output_dir, exist_ok=True)
        summary_report = []

        print("\n" + "="*80)
        print("🧠 PHÂN LOẠI & ĐÓNG GÓI 5 NOTEBOOKS CHO ĐỀ TÀI MULTIMODAL MULTI-TASK MULTI-BRANCH")
        print("="*80)

        for track_id, track_info in MULTIMODAL_ROADMAP_TRACKS.items():
            folder_name = track_info["folder_name"]
            track_title = track_info["title"]
            track_focus = track_info["topic_focus"]
            keywords = track_info["keywords"]
            target_dir = os.path.join(self.output_dir, folder_name)
            os.makedirs(target_dir, exist_ok=True)

            print(f"\n[+] Đang xử lý {track_title}...")

            scored_papers = []
            for paper in self.papers:
                text_to_analyze = f"{paper.get('title', '')} {paper.get('abstract', '')} {paper.get('journal', '')}"
                score, matched_kws = calculate_relevance_score(text_to_analyze, keywords)
                if score > 0:
                    scored_papers.append({
                        "paper": paper,
                        "score": score,
                        "matched_keywords": matched_kws
                    })

            # Sắp xếp theo điểm tương quan giảm dần
            scored_papers.sort(key=lambda x: (x["score"], x["paper"].get("year", "0000")), reverse=True)

            # Lấy top bài báo phù hợp nhất (25-40 bài/notebook)
            selected_papers = scored_papers[:self.max_per_track]
            print(f"    - Tìm thấy {len(scored_papers)} bài phù hợp. Chọn lọc Top {len(selected_papers)} bài tiêu biểu nhất.")

            packaged_papers = []
            table_rows = []

            for idx, item in enumerate(selected_papers, 1):
                p = item["paper"]
                year = str(p.get("year", "Year")).strip()
                if not year or year == "None":
                    year = "2024"
                author = extract_first_author(p.get("authors", ""))
                title = p.get("title", "Untitled")
                clean_title = sanitize_filename(title, max_length=50)

                # Tên file học thuật chuẩn hóa
                std_filename = f"{year}_{author}_{clean_title}.pdf"
                dest_path = os.path.join(target_dir, std_filename)
                src_path = p.get("local_path", "")

                try:
                    if not os.path.exists(dest_path) or os.path.getsize(dest_path) != os.path.getsize(src_path):
                        shutil.copy2(src_path, dest_path)
                except Exception as e:
                    print(f"    [!] Lỗi copy {src_path}: {e}")
                    continue

                url_or_doi = p.get("doi") or p.get("landing_url") or p.get("pdf_url") or "N/A"
                if url_or_doi.startswith("10."):
                    url_or_doi = f"https://doi.org/{url_or_doi}"

                packaged_papers.append({
                    "stt": idx,
                    "year": year,
                    "first_author": author,
                    "authors": p.get("authors", ""),
                    "title": title,
                    "url": url_or_doi,
                    "pdf_filename": std_filename,
                    "relevance_score": item["score"],
                    "matched_keywords": item["matched_keywords"]
                })

                table_rows.append(
                    f"| {idx} | {year} | {author} | {title} | [{url_or_doi}]({url_or_doi}) | `{std_filename}` |"
                )

            # Tạo file hướng dẫn Prompt và Index cho từng Notebook
            guide_md_path = os.path.join(target_dir, "00_NOTEBOOKLM_PROMPTS_AND_INDEX.md")
            guide_content = NOTEBOOKLM_PROMPT_TEMPLATE.format(
                track_title=track_title,
                track_focus=track_focus,
                paper_count=len(packaged_papers),
                paper_table_rows="\n".join(table_rows) if table_rows else "| - | - | - | Chưa có bài báo | - | - |"
            )

            with open(guide_md_path, "w", encoding="utf-8") as f:
                f.write(guide_content)

            meta_json_path = os.path.join(target_dir, "notebook_metadata.json")
            with open(meta_json_path, "w", encoding="utf-8") as f:
                json.dump({
                    "track_id": track_id,
                    "track_title": track_title,
                    "topic_focus": track_focus,
                    "total_papers": len(packaged_papers),
                    "created_at": datetime.now().isoformat(),
                    "papers": packaged_papers
                }, f, ensure_ascii=False, indent=2)

            summary_report.append({
                "track_id": track_id,
                "folder": folder_name,
                "title": track_title,
                "matched_count": len(scored_papers),
                "selected_count": len(packaged_papers)
            })

            print(f"    [✔] Đã tạo thành công {folder_name}/ ({len(packaged_papers)} PDF + Prompt Guide)")

        self.generate_global_summary(summary_report)

    def generate_global_summary(self, summary_report):
        summary_md_path = os.path.join(self.output_dir, "README_WORKSPACE_OVERVIEW.md")
        lines = [
            "# 🧠 PhD Workspace Overview: Multimodal Multi-Task Multi-Branch Biosignal Emotion Recognition",
            f"*Đề tài: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức*",
            f"*Cập nhật lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
            "Dưới đây là 5 thư mục Notebook tương ứng với 5 trụ cột cốt lõi của đề tài nghiên cứu. Mỗi thư mục chứa top các bài báo PDF chất lượng cao nhất kèm file `00_NOTEBOOKLM_PROMPTS_AND_INDEX.md` chứa sẵn toàn bộ bộ Prompt Master Class 20 tiêu chí bóc tách:\n",
            "| Thư mục Notebook | Trụ Cột Nghiên Cứu | Số bài tìm thấy | Số bài chọn lọc vào Notebook |",
            "| :--- | :--- | :--- | :--- |"
        ]
        for item in summary_report:
            lines.append(f"| [`{item['folder']}`](./{item['folder']}) | **{item['title']}** | {item['matched_count']} bài | **{item['selected_count']} bài** |")

        lines.extend([
            "\n## 🚀 Quy trình đọc trên Google NotebookLM:",
            "1. Truy cập [https://notebooklm.google.com/](https://notebooklm.google.com/).",
            "2. Tạo 5 Notebooks tương ứng với 5 thư mục trên.",
            "3. Kéo thả toàn bộ các file PDF trong từng thư mục vào Notebook tương ứng trên web.",
            "4. Mở file `00_NOTEBOOKLM_PROMPTS_AND_INDEX.md` trong từng thư mục, copy lần lượt Prompt 1 -> 6 dán vào NotebookLM.",
            "5. Copy kết quả Literature Matrix và Research Gaps sang ChatGPT bằng Prompt 7 (Bridge to ChatGPT) để thiết kế kiến trúc và viết bài báo Q1."
        ])

        with open(summary_md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print("\n" + "="*80)
        print(f"[🎉 HOÀN THÀNH!] Workspace 5 Notebooks đã sẵn sàng tại:")
        print(f"👉 {os.path.abspath(self.output_dir)}")
        print(f"👉 File tổng quan: {os.path.abspath(summary_md_path)}")
        print("="*80)


def main():
    parser = argparse.ArgumentParser(description="Multimodal Emotion Recognition Roadmap Packager")
    parser.add_argument("--db", default="downloaded_papers/checklist.db", help="Đường dẫn file checklist SQLite")
    parser.add_argument("--output", default="notebooklm_workspace", help="Thư mục xuất các Notebook")
    parser.add_argument("--max-per-track", type=int, default=35, help="Số bài tối đa cho mỗi Notebook")
    args = parser.parse_args()

    packager = MultimodalRoadmapPackager(
        db_path=args.db,
        output_dir=args.output,
        max_per_track=args.max_per_track
    )

    if packager.load_papers_from_db():
        packager.categorize_and_package()


if __name__ == "__main__":
    main()
