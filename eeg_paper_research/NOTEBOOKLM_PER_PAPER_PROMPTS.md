# 📑 NotebookLM Individual Task Prompts per Paper (English Suite)
## Doctoral Research: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals
*(Working Title: "Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức")*

---

> ### 🎯 Context & Integration Links:
> This document provides the standardized, task-by-task **English Academic Prompts** for **Google NotebookLM** to conduct deep literature audits on any individual research paper.
> - **Core Reference Framework**: [`NotebookLM.md`](NotebookLM.md)
> - **PhD Implementation Handbook (Vietnamese)**: [`HUONG_DAN_TRIEN_KHAI_PHD_NOTEBOOKLM.md`](HUONG_DAN_TRIEN_KHAI_PHD_NOTEBOOKLM.md)
> - **Doctoral Agent Operating Rules**: [`AGENTS.md`](AGENTS.md)
> - **Research Design & Dissertation State**: [`research/state.md`](research/state.md) · [`research/01-phd-executive-handbook.md`](research/01-phd-executive-handbook.md)

---

## 🏛️ 1. Executive Workflow & Evidentiary Rules

### 1.1. The 3-Tier Execution Workflow
To optimize research efficiency when analyzing hundreds of publications across the 10 NotebookLM workspaces:
1. **Tier 1 — Fast Screening (3–5 min)**: Run the [All-in-One Master Deep Extraction Prompt](#appendix--all-in-one-master-deep-extraction-prompt) or [PROMPT 1](#prompt-1--paper-identity--scope) + [PROMPT 19](#prompt-19--executive-synthesis-summary-18-point) + [PROMPT 20](#prompt-20--research-relevance-matrix) to extract core findings, benchmarks, and dissertation relevance.
2. **Tier 2 — Deep Technical Audit (15–20 min)**: Run [PROMPT 1](#prompt-1--paper-identity--scope) through [PROMPT 18](#prompt-18--scientific-evidence-table) for direct competitor papers and SOTA baselines to audit data splitting, forensic data leakage, multimodal fusion, ablation rigor, and statistical validity.
3. **Tier 3 — Strategic PhD Synthesis (20–30 min)**: Run [PROMPT 21](#prompt-21--research-gap-extraction--formulation-phase-p3) through [PROMPT 26](#prompt-26--research-decision-map-synthesis-phases-p0p13) to transform the paper's shortcomings into verified novelty claims, formal research questions ($RQ_1 - RQ_6$), testable hypotheses ($H_1 - H_6$), and controlled experimental ablations for your dissertation.

### 1.2. The 10 Standardized NotebookLM Workspaces
All literature PDFs are organized into 10 focused workspaces in `eeg_paper_research/notebooklm_workspace/`:
- `notebook_01_Multimodal_EEG_Biosignals`: CNS-ANS brain-body synergy (EEG + ECG/EDA/PPG).
- `notebook_02_Multi_Task_Learning_Affect`: Multi-task learning, Valence-Arousal coupling, dynamic loss weighting.
- `notebook_03_Multi_Branch_Cross_Modal_Attention`: Heterogeneous multi-branch encoders, cross-attention mechanics.
- `notebook_04_Subspace_Disentanglement_Domain_Adaptation`: Shared-Private disentanglement, DANN, MMD, cross-subject transfer.
- `notebook_05_Missing_Modality_Wearable_Robustness`: Sensor dropout recovery, teacher-student knowledge distillation.
- `notebook_06_Foundation_Models_Self_Supervised_Biosignals`: Masked autoencoders, contrastive learning (SimCLR/MoCo).
- `notebook_07_Graph_Neural_Networks_Brain_Connectivity`: GCN, Dynamic GCN, Graph Attention (GAT), 10–20 electrode topology.
- `notebook_08_Transformers_Crossmodal_Affective_Computing`: Patch-based transformers, spatio-temporal attention.
- `notebook_09_Explainable_AI_Interpretable_Biosignals`: Neurobiological grounding, topographic saliency maps.
- `notebook_10_Closed_Loop_BCI_RealTime_Affective_Systems`: Real-time BCI, edge deployment feasibility.

### 1.3. Strict Evidentiary Rules (Applied to All Prompts)
1. **Single-Source Direct Execution (Zero Manual Editing)**: Each NotebookLM notebook contains exactly one uploaded research paper (source file). All prompts are 100% copy-paste ready and instruct NotebookLM to directly read and analyze the uploaded source file without requiring any placeholder or title replacement.
2. **Closed-World Evaluation**: NotebookLM must evaluate **ONLY** the uploaded source paper in the active notebook. Never hallucinate or assume unstated details.
3. **Epistemic Classification**: Every claim and extracted fact must be classified using:
   - **`[EXPLICIT]`**: Directly stated, mathematically formulated, or reported in the text (with section/table/page citation).
   - **`[SUPPORTED]`**: Strongly verified and backed by quantitative empirical experiments/tables.
   - **`[INFERRED]`**: Logically deduced from stated parameters, but not verbatim in the source.
   - **`[UNKNOWN]`**: Unstated, omitted, or unverifiable from the source document (explicitly state why).
4. **Evaluation Chain Invariance**:
   $$\text{METHOD} \longrightarrow \text{DATASET} \longrightarrow \text{PROTOCOL} \longrightarrow \text{METRIC} \longrightarrow \text{RESULT}$$

---

## 📑 Table of Contents (26 Discrete Task Prompts)

### Part I: Technical Extraction & Forensic Audit
- [PROMPT 1 — Paper Identity & Scope](#prompt-1--paper-identity--scope)
- [PROMPT 2 — Dataset & Affective Ground-Truth](#prompt-2--dataset--affective-ground-truth)
- [PROMPT 3 — Preprocessing & Signal Physiology](#prompt-3--preprocessing--signal-physiology)
- [PROMPT 4 — Data Splitting Protocol & Partitioning](#prompt-4--data-splitting-protocol--partitioning)
- [PROMPT 5 — Model Architecture & Topology](#prompt-5--model-architecture--topology)
- [PROMPT 6 — Multimodal Fusion & Cross-Modal Dynamics](#prompt-6--multimodal-fusion--cross-modal-dynamics)
- [PROMPT 7 — Multi-Task Learning & Objectives](#prompt-7--multi-task-learning--objectives)
- [PROMPT 8 — Multi-Branch Topology & Justification](#prompt-8--multi-branch-topology--justification)
- [PROMPT 9 — Benchmark Baselines & Comparative Rigor](#prompt-9--benchmark-baselines--comparative-rigor)
- [PROMPT 10 — Experimental Results & Statistical Rigor](#prompt-10--experimental-results--statistical-rigor)
- [PROMPT 11 — Ablation Study Audit](#prompt-11--ablation-study-audit)
- [PROMPT 12 — Generalization Across Domains & Subjects](#prompt-12--generalization-across-domains--subjects)
- [PROMPT 13 — Robustness, Missing Modalities & Noise](#prompt-13--robustness-missing-modalities--noise)
- [PROMPT 14 — Computational Complexity & Edge Feasibility](#prompt-14--computational-complexity--edge-feasibility)
- [PROMPT 15 — Methodological Limitations Audit](#prompt-15--methodological-limitations-audit)
- [PROMPT 16 — Reproducibility Audit](#prompt-16--reproducibility-audit)
- [PROMPT 17 — Comprehensive Data Leakage Audit](#prompt-17--comprehensive-data-leakage-audit)
- [PROMPT 18 — Scientific Evidence Table](#prompt-18--scientific-evidence-table)

### Part II: Synthesis & Strategic PhD Alignment
- [PROMPT 19 — Executive Synthesis Summary (18-Point)](#prompt-19--executive-synthesis-summary-18-point)
- [PROMPT 20 — Research Relevance Matrix](#prompt-20--research-relevance-matrix)
- [PROMPT 21 — Research Gap Extraction & Formulation (Phase P3)](#prompt-21--research-gap-extraction--formulation-phase-p3)
- [PROMPT 22 — Novelty & Prior Art Collision Check (Phase P7)](#prompt-22--novelty--prior-art-collision-check-phase-p7)
- [PROMPT 23 — Research Directions & Architectural Taxonomy (Phases P2/P7)](#prompt-23--research-directions--architectural-taxonomy-phases-p2p7)
- [PROMPT 24 — Research Questions & Testable Hypotheses Formulation (Phase P4)](#prompt-24--research-questions--testable-hypotheses-formulation-phase-p4)
- [PROMPT 25 — Experimental Verification & Protocol Design (Phases P5/P6/P8)](#prompt-25--experimental-verification--protocol-design-phases-p5p6p8)
- [PROMPT 26 — Research Decision Map Synthesis (Phases P0/P13)](#prompt-26--research-decision-map-synthesis-phases-p0p13)

### Part III: Master Prompt
- [APPENDIX — All-in-One Master Deep Extraction Prompt](#appendix--all-in-one-master-deep-extraction-prompt)

---

### PROMPT 1 — Paper Identity & Scope

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Do not invent missing information. For each item, provide source locations (section/page) and categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 1 — PAPER IDENTITY & SCOPE:
Extract:
1. Exact Title of the publication
2. Authors and Research Affiliations / Laboratories
3. Publication Year
4. Venue / Journal / Conference (include Volume, Issue, Impact Factor, or Conference Tier if mentioned)
5. DOI and Official Repository / Publisher URL
6. Core Research Problem addressed (the central scientific or engineering challenge)
7. Main Objective of the proposed methodology
8. Primary Claimed Scientific Contributions (list all explicit novelty claims made by the authors)
```

---

### PROMPT 2 — Dataset & Affective Ground-Truth

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Do not invent missing information. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 2 — DATASET & AFFECTIVE GROUND-TRUTH:
Extract:
1. Benchmark Dataset Name (e.g., DEAP, SEED, SEED-IV, DREAMER, AMIGOS, WESAD, ASCERTAIN, or custom/private dataset)
2. Subject Cohort Details:
   - Total subjects (N)
   - Demographics: Age distribution (mean ± std), gender breakdown (M/F), handedness
   - Health and clinical status (healthy vs neuropsychiatric conditions)
3. Affective Ground-Truth Model:
   - Dimensional Space (Valence, Arousal, Dominance, Liking) vs Categorical Discrete Emotions (Ekman 6, Plutchik 8) vs Compound States (Stress, Cognitive Load)
   - Rating Scale & Granularity: Continuous vs Discrete (e.g., SAM 1–9, continuous joystick, binary high/low median split, ternary classification)
   - Rating Methodology: Subjective self-assessment vs External expert raters vs Behavioral consensus
   - Label Reliability Metrics: Inter-rater agreement metrics (Cohen's Kappa κ, Krippendorff's α, ICC) if reported
4. Recorded Physiological Modalities:
   - Central Nervous System (CNS): Scalp EEG (channel count, 10–20 electrode montage, reference and ground electrodes)
   - Autonomic Nervous System (ANS / Peripheral): ECG (lead configuration), EDA/GSR (skin conductance), PPG (blood volume pulse), Respiration, Skin Temperature (SKT), EMG, EOG
5. Sampling Frequency (Hz) for raw and downsampled signals across each modality
6. Stimulus Elicitation Paradigm: Stimulus type (film clips, music videos, IAPS images, VR immersion, cognitive stressors), duration per stimulus, and baseline resting-state recording
7. Trial & Windowing Structure: Total trials per subject, trial length (s), analysis window length (seconds/samples), step size / overlap percentage (%)
```

---

### PROMPT 3 — Preprocessing & Signal Physiology

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 3 — PREPROCESSING & SIGNAL PHYSIOLOGY:
Extract:
1. Filtering & Denoising:
   - Bandpass filter cutoff frequencies (Hz) for EEG (e.g., 0.5–45 Hz, 4–45 Hz) and peripheral signals
   - Notch filtering for powerline interference (50/60 Hz mains)
2. Physiological Artifact Removal:
   - Ocular (EOG / blink) and Myogenic (EMG / muscle) removal methods (ICA, FastICA, EEMD, Wavelet Denoising, BSS)
   - Cardiac baseline wander and motion artifact removal for ECG/EDA
   - Neurobiological Verification: Did the authors verify that cleaned signals represent true neural dynamics rather than residual artifact leakage?
3. Normalization & Scaling:
   - Method: Z-score normalization, Min-Max scaling, Baseline subtraction or relative ratio ((Signal - Baseline) / Baseline)
   - Partition Isolation: Crucial — was normalization computed within-subject or globally across the dataset? Was it fitted strictly on training folds or the entire corpus?
4. Physiological Feature Extraction:
   - EEG: Power Spectral Density (PSD), Differential Entropy (DE), Wavelet Energy (CWT/DWT), Asymmetry indices (FAA, DASM, RASM, DCAU), Phase Locking Value (PLV) across frequency bands (δ, θ, α, β, γ)
   - ECG/PPG: Heart Rate Variability (HRV time-domain: SDNN, RMSSD, pNN50; frequency-domain: LF, HF, LF/HF ratio, VLF)
   - EDA: Tonic Skin Conductance Level (SCL) vs Phasic Skin Conductance Response (SCR), peak frequency, rising time
5. Data Augmentation: Jittering, temporal cropping, Gaussian noise injection, Mixup, GAN-based synthetic signal generation
```

---

### PROMPT 4 — Data Splitting Protocol & Partitioning

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 4 — DATA SPLITTING PROTOCOL & PARTITIONING:
Determine:
1. Partitioning Strategy:
   - Subject-Dependent (Intra-Subject / Subject-Specific)
   - Subject-Independent (Cross-Subject / Inter-Subject)
   - Leave-One-Subject-Out (LOSO) Cross-Validation
   - Cross-Session (Subject-Specific across different recording days/weeks)
   - Cross-Dataset / Cross-Corpus Validation (e.g., DEAP → SEED/DREAMER)
2. Train / Validation / Test Construction:
   - Splitting Unit: Sample-level random split vs Trial-level split vs Subject-level split
   - Exact ratio (e.g., 80/10/10) or K-fold cross-validation scheme
3. Anti-Leakage Verification:
   - Do overlapping windows from the same continuous trial appear across both training and test sets?
   - Do segments from the same subject appear in both training and test folds during cross-subject claims?
   - If ambiguous or unstated, explicitly output [UNKNOWN].
```

---

### PROMPT 5 — Model Architecture & Topology

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 5 — MODEL ARCHITECTURE & TOPOLOGY:
Trace the complete computational graph:
$$\text{Input Tensor} \longrightarrow \text{Feature Transformation} \longrightarrow \text{Modality Encoders} \longrightarrow \text{Branch Topology} \longrightarrow \text{Latent Fusion} \longrightarrow \text{Task Heads} \longrightarrow \text{Outputs}$$

Identify:
1. Spatial Encoders: Graph Convolutional Networks (GCN), Dynamic GCN, Graph Attention (GAT), Topographic 2D/3D CNNs
2. Temporal Encoders: Dilated Temporal Convolutional Networks (TCN), LSTM, Bi-LSTM, GRU, 1D-CNN
3. Spatiotemporal / Spectral Encoders: Continuous Wavelet Transform (CWT) + CNN, Vision Transformers (ViT)
4. Self-Supervised / Foundation Encoders: Masked Autoencoders (MAE), Contrastive Learning (SimCLR, MoCo)
5. Representation Topography: Modality-shared representations vs Modality-private representations vs Task-private representations
```

---

### PROMPT 6 — Multimodal Fusion & Cross-Modal Dynamics

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 6 — MULTIMODAL FUSION & CROSS-MODAL DYNAMICS:
Classify the fusion mechanism:
1. Fusion Paradigm:
   - Early / Data-level Fusion (Raw feature concatenation)
   - Intermediate / Feature-level Fusion (Joint latent bottleneck representation)
   - Late / Decision-level Fusion (Weighted voting, ensemble averaging, meta-classifier)
   - Directional Cross-Modal Attention (Q_A × K_B × V_B, Cross-Transformers)
   - Tensor Fusion / Bilinear Pooling
   - Dynamic / Gated Adaptive Fusion (Modality gating networks)
2. Mathematical Formulation & Operators:
   - State the exact mathematical equation of the fusion layer
   - Directional Cross-Attention: Does EEG act as query ($Q_{\text{EEG}}$) while peripheral bio-signals act as key/value ($K_{\text{Bio}}, V_{\text{Bio}}$), or vice versa?
3. Modality Interaction Dynamics:
   - Does CNS (EEG) guide or calibrate ANS (ECG/EDA) features?
   - Modality Dominance & Gradient Starvation: Does the model prevent dominant modalities (e.g., high-channel EEG) from suppressing subtle physiological signals (e.g., EDA/ECG)?
```

---

### PROMPT 7 — Multi-Task Learning & Objectives

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 7 — MULTI-TASK LEARNING & OBJECTIVES:
Determine:
1. Task Configuration:
   - Single-Task (STL) vs Multi-Task (MTL)
   - Target tasks: Simultaneous Valence + Arousal, Quadrant classification (HVHA, HVLA, LVHA, LVLA), Subject identification (Adversarial Decoupling), Domain classification, Signal reconstruction
2. Parameter Sharing Mechanism:
   - Hard parameter sharing vs Soft parameter sharing vs Cross-stitch / Sluice networks
3. Total Loss Function Formulation:
   - Extract the exact loss equation. Does it take the form:
     $$\mathcal{L}_{\text{total}} = \sum_{t=1}^{T} w_t \mathcal{L}_t + \alpha \mathcal{L}_{\text{reg}} + \beta \mathcal{L}_{\text{disentangle}}$$
   - Or Kendall Homoscedastic Aleatoric Uncertainty Weighting:
     $$\mathcal{L}_{\text{total}} = \sum_{t=1}^{T} \left( \frac{1}{2\sigma_t^2} \mathcal{L}_t + \log \sigma_t \right) + \alpha \mathcal{L}_{\text{diff}} + \beta \mathcal{L}_{\text{sim}}$$
4. Task Balancing Strategy:
   - Fixed static weights ($w_t = \text{const}$)
   - Homoscedastic Aleatoric Uncertainty Weighting (Kendall et al.)
   - Gradient Normalization (GradNorm), Dynamic Weight Averaging (DWA), MGDA (Multi-Gradient Descent)
   - Negative Transfer & Gradient Interference: Did the authors address inter-task gradient conflict or negative transfer?
```

---

### PROMPT 8 — Multi-Branch Topology & Justification

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 8 — MULTI-BRANCH TOPOLOGY & JUSTIFICATION:
Extract:
1. Branch Breakdown:
   - Number of dedicated parallel branches
   - Dedicated input modality / sensor group assigned to each branch
   - Heterogeneous vs Homogeneous encoder design across branches (e.g., GCN for EEG, TCN for ECG, CWT for EDA)
2. Shared vs Private Subspaces:
   - Do dedicated branches extract modality-private features while a central branch extracts cross-modal shared features?
   - Orthogonality / Difference constraints implemented between branches:
     $$\mathcal{L}_{\text{diff}} = \sum_{m=1}^{M} \| {S^{(m)}}^\top P^{(m)} \|_F^2$$
3. Architectural Justification:
   - What explicit theoretical, physical, or neurobiological justification do the authors provide for using multiple branches?
   - If no explicit theoretical reason is given, state: "The paper does not provide an explicit theoretical or neurobiological justification for the multi-branch design."
```

---

### PROMPT 9 — Benchmark Baselines & Comparative Rigor

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 9 — BENCHMARK BASELINES & COMPARATIVE RIGOR:
Construct the comparative baseline table:
| Baseline Model | Modality | Architecture Category | Task Configuration | Reported Metric | Source Location |
|---|---|---|---|---|---|

Classify baselines into:
1. Unimodal vs Multimodal baselines
2. Classical Machine Learning (SVM, Random Forest, XGBoost) vs Deep Learning
3. Published State-of-the-Art (SOTA) vs Re-implemented baselines vs Naive ablation baselines
```

---

### PROMPT 10 — Experimental Results & Statistical Rigor

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 10 — EXPERIMENTAL RESULTS & STATISTICAL RIGOR:
Extract quantitative performance metrics:
1. Classification Metrics:
   - Accuracy (%), Balanced Accuracy (%), Precision, Recall, Macro-F1, Weighted-F1, Cohen's Kappa (κ), ROC-AUC
2. Regression Metrics (continuous emotion tracking):
   - Mean Absolute Error (MAE), Root Mean Square Error (RMSE), Pearson's r, Concordance Correlation Coefficient (CCC), R²
3. Statistical Dispersion & Rigor:
   - Mean ± Standard Deviation over folds/subjects/runs
   - 95% Confidence Intervals (CI)
   - Number of independent repetitions / random seeds
   - Statistical hypothesis tests: Paired t-test, Wilcoxon Signed-Rank test, ANOVA, Holm-Bonferroni / FDR corrections (p-values)
```

---

### PROMPT 11 — Ablation Study Audit

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 11 — ABLATION STUDY AUDIT:
Extract every individual ablation experiment:
For every ablated component / module:
- Component Removed / Replaced (e.g., without Cross-Attention, without EDA branch, without Uncertainty Loss weighting):
- Baseline Configuration:
- Ablation Result vs Full Model Result: Exact performance delta (ΔAcc, ΔF1)
- Isolated Contribution: Does the ablation isolate the specific module or introduce confounding hyperparameter shifts?
- Source Location: Table / Figure number
```

---

### PROMPT 12 — Generalization Across Domains & Subjects

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 12 — GENERALIZATION ACROSS DOMAINS & SUBJECTS:
Evaluate:
1. Evaluated Generalization Paradigm:
   - Intra-Subject (Same subject, different trials)
   - Cross-Subject (Unseen subjects, LOSO)
   - Cross-Session (Unseen recording sessions across different days/weeks)
   - Cross-Dataset / Cross-Corpus (e.g., Trained on DEAP → Evaluated on SEED/DREAMER)
2. Domain Adaptation & Generalization Techniques:
   - Maximum Mean Discrepancy (MMD), Domain-Adversarial Neural Networks (DANN), Wasserstein Distance, Optimal Transport, Adaptive Batch Normalization (AdaBN)
3. Degradation Severity:
   - Exact quantification of performance drop from Subject-Dependent to Subject-Independent mode (ΔAcc, ΔF1).
```

---

### PROMPT 13 — Robustness, Missing Modalities & Noise

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 13 — ROBUSTNESS, MISSING MODALITIES & NOISE:
Audit the system's operational resilience:
1. Sensor Dropout & Missing Modalities:
   - Does the model support inference when 1 or more modalities are completely missing (e.g., EEG disconnected, EDA unreadable)?
   - Mechanism: Feature Imputation vs Zero-padding vs Knowledge Distillation (Teacher-Student) vs Joint Multimodal Autoencoding
2. Signal Quality & Noise Sensitivity:
   - Resistance to motion artifacts, electrode impedance spikes, electrode displacement
3. Class Imbalance Resilience:
   - Handling of skewed emotional distributions (e.g., dominant Neutral/Calm classes, focal loss, re-weighting)
```

---

### PROMPT 14 — Computational Complexity & Edge Feasibility

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 14 — COMPUTATIONAL COMPLEXITY & EDGE FEASIBILITY:
Extract efficiency and deployment metrics:
1. Model Footprint: Total learnable parameters (M), Model storage size (MB/GB)
2. Compute Complexity: Floating Point Operations (FLOPs / GFLOPs / MACs)
3. Execution Latency: Training time per epoch, Inference latency per time-window (ms)
4. Hardware & Runtime Environment: GPU/CPU specs, Embedded / Edge platform compatibility (e.g., NVIDIA Jetson, Google Coral, Raspberry Pi)
If not reported, state: "[UNKNOWN] — Computational cost and inference latency not reported."
```

---

### PROMPT 15 — Methodological Limitations Audit

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 15 — METHODOLOGICAL LIMITATIONS AUDIT:
Categorize all limitations into three formal academic levels:
- Tier A — Explicit Author-Disclosed Limitations: Weaknesses openly stated by the authors in the Discussion/Conclusion sections.
- Tier B — Implicit Methodological Flaws: Observable technical weaknesses (e.g., small cohort N < 15, lack of LOSO protocol, uncorrected multiple comparisons, homogeneous encoders).
- Tier C — Potential Critical Concerns: Theoretical risks requiring experimental verification (e.g., vulnerability to modality collapse, sensor noise dominance, unverified neurobiological grounding).
```

---

### PROMPT 16 — Reproducibility Audit

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 16 — REPRODUCIBILITY AUDIT:
Classify overall reproducibility score: HIGH / MEDIUM / LOW / UNKNOWN
Evaluate:
1. Public Source Code URL (GitHub/GitLab/Zenodo) and working status
2. Open Benchmark Dataset Access & preprocessed feature availability
3. Exact Hyperparameters Disclosed (Learning rate, batch size, optimizer, weight decay, dropout rate, scheduler)
4. Random Seed Control and Software Versions (PyTorch, TensorFlow, MNE-Python, TorchEEG)
```

---

### PROMPT 17 — Comprehensive Data Leakage Audit

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 17 — COMPREHENSIVE DATA LEAKAGE AUDIT:
Perform a forensic audit across 6 academic data leakage mechanisms (Rule 7 of AGENTS.md):
1. Subject Leakage: Did windows/samples from the same subject exist across both training and test partitions in cross-subject claims?
2. Temporal / Windowing Leakage: Did overlapping sliding windows from the same continuous trial bleed across train and test sets?
3. Preprocessing & Scaling Leakage: Was Z-score / Min-Max normalization computed globally over the entire dataset prior to splitting, rather than fitted solely on training folds?
4. Feature Extraction & Dimensionality Reduction Leakage: Was PCA / ICA / CSP / DE fitted on the entire dataset prior to cross-validation?
5. Hyperparameter Tuning Leakage: Were hyperparameters or model checkpoints selected directly on the test set without a held-out validation set?
6. Augmentation Leakage: Were data augmentations generated prior to dataset partitioning?

State the final forensic verdict:
[CLEAN] / [POTENTIAL LEAKAGE] / [CONFIRMED LEAKAGE] / [INDETERMINABLE]
Provide exact citations and reasoning.
```

---

### PROMPT 18 — Scientific Evidence Table

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook.

Perform TASK 18 — SCIENTIFIC EVIDENCE TABLE:
Synthesize all core claims into a structured evidence table:
| Claimed Hypothesis / Contribution | Supporting Empirical Evidence | Source Location | Epistemic Status ([EXPLICIT] / [SUPPORTED] / [INFERRED]) |
|---|---|---|---|

Focus on claims related to:
- Multimodal biosignal interaction (CNS vs ANS)
- Multi-task affective optimization (Valence/Arousal)
- Multi-branch encoder representations
- Subspace disentanglement and noise separation
- Cross-subject generalization and missing modality robustness
```

---

### PROMPT 19 — Executive Synthesis Summary (18-Point)

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook.

Perform TASK 19 — EXECUTIVE SYNTHESIS SUMMARY:
Produce a standardized 18-point executive summary strictly using the following structure:
1. Research Problem & Objective
2. Benchmark Dataset & Cohort Size
3. Physiological Modalities (CNS & ANS)
4. Affective Ground-Truth Model
5. Preprocessing & Artifact Cleaning
6. Feature Representation & Transforms
7. Encoder Architecture
8. Multimodal Fusion Mechanism
9. Multi-Task Learning Strategy
10. Multi-Branch Structure
11. Evaluation Protocol & Split
12. Benchmark Baselines
13. Quantitative Main Results
14. Ablation Findings
15. Generalization & LOSO Performance
16. Missing Modality & Robustness
17. Computational Efficiency & Latency
18. Key Limitations & Reproducibility
```

---

### PROMPT 20 — Research Relevance Matrix

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook.

Perform TASK 20 — RESEARCH RELEVANCE MATRIX:
Rate and justify relevance to the PhD Dissertation along 8 core dimensions using HIGH / MEDIUM / LOW:
1. Multimodal Biosignals (CNS + ANS Synergy): [HIGH/MEDIUM/LOW] — Justification:
2. Multi-Task Learning (Affective Joint Objectives): [HIGH/MEDIUM/LOW] — Justification:
3. Multi-Branch Deep Architectures: [HIGH/MEDIUM/LOW] — Justification:
4. Directional Cross-Modal Attention Fusion: [HIGH/MEDIUM/LOW] — Justification:
5. Shared-Private Subspace Disentanglement: [HIGH/MEDIUM/LOW] — Justification:
6. Cross-Subject LOSO Generalization: [HIGH/MEDIUM/LOW] — Justification:
7. Missing Modality Robustness: [HIGH/MEDIUM/LOW] — Justification:
8. Physiological / Explainable AI (XAI) Grounding: [HIGH/MEDIUM/LOW] — Justification:
```

---

### PROMPT 21 — Research Gap Extraction & Formulation (Phase P3)

```markdown
You are a senior scientific literature analysis assistant and doctoral auditor for the PhD research: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Read and analyze the uploaded research paper (source file) in this notebook.

Perform TASK 21 — RESEARCH GAP EXTRACTION & FORMULATION (PHASE P3):
Extract and formulate the scientific and technical gaps revealed by this paper:
1. Explicit Future Work & Open Questions:
   Extract what the authors explicitly stated as unresolved challenges, future directions, or unaddressed questions.
2. Theoretical & Methodological Gaps:
   Identify specific technical weaknesses or omissions in the paper's approach:
   - Modality Rate Asymmetry / Modality Collapse: Did one modality dominate during gradient updates?
   - Subspace Disentanglement: Did the paper mix sensor-private noise/artifacts with shared emotional semantics?
   - Multi-Task Objective Interference: Did the paper use naive/fixed loss weighting causing negative transfer?
   - Anti-Leakage & Generalization: Did the paper fail to evaluate strict Leave-One-Subject-Out (LOSO) protocols?
   - Missing Modality Robustness: Did the paper assume all sensor channels are always available without evaluating dropout?
   - Biological / XAI Grounding: Did the paper lack neurobiological grounding and topographic explainability?
3. Ph.D. Dissertation Contribution Opportunity:
   Synthesize how our proposed Multi-Task Multi-Branch Architecture (MMB-EmotionNet) directly addresses the gaps exposed by this paper.
```

---

### PROMPT 22 — Novelty & Prior Art Collision Check (Phase P7)

```markdown
You are a senior doctoral thesis reviewer specializing in Affective Computing and Multimodal Biosignals.

Read and analyze the uploaded research paper (source file) in this notebook.

Perform TASK 22 — NOVELTY & PRIOR ART COLLISION CHECK (PHASE P7):
Perform a rigorous novelty collision check against our proposed PhD framework:
1. Has this paper (or any cited work in this notebook) implemented the EXACT combination of:
   - Multimodal Biosignals (Scalp EEG + Autonomic ECG/EDA/PPG)?
   - Dedicated Physics-Informed Multi-Branch Encoders (GCN for EEG + Dilated TCN for ECG + CWT for EDA)?
   - Explicit Shared-Private Subspace Disentanglement (L_sim + L_diff)?
   - Directional Cross-Modal Attention (Q_EEG, K_Bio, V_Bio)?
   - Dynamically Balanced Multi-Task Loss (Homoscedastic Aleatoric Uncertainty Weighting)?
2. If similar architectures exist, identify the precise technical boundaries, differences, and limitations of prior art compared to our proposed MMB-EmotionNet framework. Categorize evidence strictly as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].
```

---

### PROMPT 23 — Research Directions & Architectural Taxonomy (Phases P2/P7)

```markdown
You are a senior doctoral thesis reviewer specializing in Affective Computing and Multimodal Biosignals.

Read and analyze the uploaded research paper (source file) in this notebook.

Perform TASK 23 — RESEARCH DIRECTIONS & ARCHITECTURAL TAXONOMY (PHASES P2/P7):
Map out and categorize the feasible technical avenues revealed across the literature:
1. Branching Paradigms: Unimodal vs Homogeneous CNN vs Physics-informed Spatial GCN + Dilated TCN + CWT.
2. Fusion & Cross-Modal Interaction: Early Concatenation vs Late Voting vs Cross-Attention QKV vs Multimodal Transformers.
3. Multi-Task Optimization: Single-task independent models vs Hard parameter sharing vs Uncertainty-weighted dynamic loss vs Adversarial subject decoupling.
4. Generalization & Adaptation: Standard empirical training vs Domain Adversarial Neural Networks (DANN) vs Maximum Mean Discrepancy (MMD) vs Orthogonal Disentanglement.
```

---

### PROMPT 24 — Research Questions & Testable Hypotheses Formulation (Phase P4)

```markdown
You are a senior doctoral thesis reviewer specializing in Affective Computing and Multimodal Biosignals.

Read and analyze the uploaded research paper (source file) in this notebook.

Perform TASK 24 — RESEARCH QUESTIONS & TESTABLE HYPOTHESES FORMULATION (PHASE P4):
Translate the identified research gaps and directions into formal, falsifiable scientific propositions:
1. Formulate 6 core Research Questions (RQ1 to RQ6):
   - RQ1: Physics-informed multi-branch representation vs Homogeneous encoders.
   - RQ2: Directional cross-modal attention synergy (Q_EEG ↔ K,V_Bio).
   - RQ3: Shared-private orthogonal subspace disentanglement for sensor noise isolation.
   - RQ4: Homoscedastic uncertainty multi-task loss balancing vs Static weighting.
   - RQ5: Subject-independent Leave-One-Subject-Out (LOSO) cross-subject generalization.
   - RQ6: Graceful performance degradation under sensor dropouts (Missing modality robustness).
2. State the corresponding Null (H0) and Alternative (H1) Hypotheses with formal statistical rejection criteria (α = 0.05).
```

---

### PROMPT 25 — Experimental Verification & Protocol Design (Phases P5/P6/P8)

```markdown
You are a senior doctoral thesis reviewer specializing in Affective Computing and Multimodal Biosignals.

Read and analyze the uploaded research paper (source file) in this notebook.

Perform TASK 25 — EXPERIMENTAL VERIFICATION & PROTOCOL DESIGN (PHASES P5/P6/P8):
Define the complete, reproducible experimental blueprint to validate the hypotheses:
1. Benchmark Datasets & Anti-Leakage Protocol: Selection of canonical datasets (DEAP, SEED, DREAMER, AMIGOS, WESAD) with strict Subject-wise LOSO splitting and pre-split isolated scaling.
2. Controlled 10-Configuration Ablation Suite (EXP-ABL-01 through EXP-ABL-10) isolating every individual module:
   - EXP-ABL-01: Full Proposed MMB-EmotionNet (Full SOTA benchmark)
   - EXP-ABL-02: Unimodal EEG Branch Only (CNS baseline)
   - EXP-ABL-03: Unimodal Peripheral Biosignals Only (ANS baseline: ECG+EDA)
   - EXP-ABL-04: Homogeneous Encoders (1D-CNN backbone across all signals)
   - EXP-ABL-05: Without Cross-Attention (Replaced by Feature Concatenation)
   - EXP-ABL-06: Without Subspace Disentanglement (Ablating L_diff and L_sim)
   - EXP-ABL-07: Fixed Loss Weights vs Uncertainty Loss Weighting
   - EXP-ABL-08: Single-Task Learning (STL) Baselines
   - EXP-ABL-09: Random Split vs Strict Subject-wise LOSO Protocol
   - EXP-ABL-10: Progressive Modality Dropout (25%, 50%, 75%, 100% missing sensors)
3. Missing Modality Stress-Testing Suite: Progressive sensor dropout comparing baseline models vs Teacher-Student Knowledge Distillation.
4. Statistical Rigor & Significance Testing: Wilcoxon Paired Signed-Rank Test, Holm-Bonferroni correction (α = 0.05), 95% Bootstrap BCa Confidence Intervals, and Cohen's d effect sizes.
```

---

### PROMPT 26 — Research Decision Map Synthesis (Phases P0/P13)

```markdown
You are a senior doctoral thesis reviewer specializing in Affective Computing and Multimodal Biosignals.

Read and analyze the uploaded research paper (source file) in this notebook.

Perform TASK 26 — RESEARCH DECISION MAP SYNTHESIS (PHASES P0/P13):
Synthesize all findings into an executive Research Decision Map according to Rule 23 of AGENTS.md:
1. Evidence Base: Summarize direct empirical evidence supporting the proposed design.
2. Technical Alternatives: List competing design choices evaluated in the literature.
3. Methodological Trade-offs: Detail trade-offs between model complexity, parameter footprint, and classification accuracy.
4. Experimental & Scientific Risks: Identify potential failure modes (e.g., negative transfer, sensor noise dominance, montage shift).
5. Concrete Action Plan: Provide the immediate experimental milestones for the PhD dissertation.
```

---

## 🚀 APPENDIX — All-in-One Master Deep Extraction Prompt

> **Usage Note**: When you want to perform a complete, end-to-end deep analysis of a paper in a single NotebookLM query, copy and paste this master prompt.

```markdown
You are a senior scientific literature analysis assistant and doctoral research auditor specializing in Affective Computing, Biomedical Signal Processing (EEG, ECG, EDA, PPG), and Multimodal Deep Learning.

Read and analyze the uploaded research paper (source file) in this notebook. Do NOT invent missing information. For every answer, distinguish [EXPLICIT], [SUPPORTED], [INFERRED], and [UNKNOWN]. Always preserve the scientific evaluation chain: METHOD → DATASET → PROTOCOL → METRIC → RESULT.

Provide a comprehensive, highly rigorous doctoral-level scientific audit covering all 26 dimensions:
1. Paper Identity: Title, Authors, Year, Venue, DOI, Problem, Claimed Contributions.
2. Dataset & Affective Ground-Truth: Dataset Name, Cohort N, Demographics, Ground-truth Affective Model, Rating Granularity & Reliability, CNS/ANS Modalities, Channels, Fs, Elicitation Paradigm, Trials/Windows.
3. Preprocessing & Signal Physiology: Filters, Physiological Artifact Removal (ICA/EEMD), Normalization, EEG Bands/Asymmetry, HRV/EDA Features, Augmentation.
4. Data Splitting Protocol: Subject-dependent vs LOSO Independent, Partitioning Ratios, Anti-Leakage Verification.
5. Model Architecture & Topology: Full End-to-End Pipeline, Spatial/Temporal/Spectral Encoders, Subspace Topography.
6. Multimodal Fusion & Dynamics: Fusion Category, Exact Mathematical Operators, Cross-Modal Interaction (Q_EEG ↔ K,V_Bio), Dominance Control.
7. Multi-Task Learning: Task Setup, Loss Equations, Static vs Kendall Uncertainty Dynamic Weighting, Negative Transfer Handling.
8. Multi-Branch Structure: Branch Count, Dedicated Inputs, Shared-Private Disentanglement, Explicit Justification.
9. Benchmark Baselines: Table of Baselines, Architecture Types, SOTA vs Naive.
10. Quantitative Results: Exact Acc, F1, MAE/RMSE, Standard Deviations, Statistical Hypothesis Tests (p-values).
11. Ablation Audit: Module Removed, ΔAcc/ΔF1, Isolated Contribution.
12. Generalization Capabilities: Cross-Subject LOSO, Cross-Session, Domain Adaptation.
13. Robustness & Sensor Dropout: Missing Modality Handling, Noise Sensitivity, Class Imbalance.
14. Computational Complexity: Parameters (M), FLOPs, Latency (ms), Hardware Specs.
15. Limitations Audit: Tier A Author-disclosed, Tier B Observable Flaws, Tier C Critical Concerns.
16. Reproducibility Assessment: Code URL, Benchmark Availability, Hyperparameters, Seed/Libraries.
17. Data Leakage Audit: Subject, Window, Scaling, Feature Selection, Hyperparameter Tuning Leakage Verdict ([CLEAN] / [POTENTIAL LEAKAGE] / [CONFIRMED LEAKAGE] / [INDETERMINABLE]).
18. Scientific Evidence Table: Markdown Table of Claims vs Evidence vs Source Location vs Epistemic Tag.
19. Standardized 18-Point Paper Summary: Formatted strictly using the 18 standard points.
20. Research Relevance Matrix: Rating 8 Dimensions (High/Medium/Low with Justifications).
21. Research Gap Extraction: Explicit Open Questions, Theoretical Gaps, PhD Contribution Opportunity.
22. Novelty & Prior Art Collision Check: Evaluate against the proposed MMB-EmotionNet framework.
23. Research Directions & Architectural Taxonomy: Branching, Fusion, MTL, Adaptation Paradigms.
24. Research Questions & Hypotheses Formulation: RQ1–RQ6, Null H0 & Alternative H1 Hypotheses.
25. Experimental Verification Protocol: Datasets, 10-Configuration Ablation Suite (EXP-ABL-01 to EXP-ABL-10), Missing Modality Stress-Testing, Statistical Rigor.
26. Research Decision Map: Evidence Base, Alternatives, Trade-offs, Risks, Immediate Action Plan.
```
