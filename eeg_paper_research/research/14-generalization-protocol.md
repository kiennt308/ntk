# Phase P9: Cross-Subject & Cross-Dataset Generalization Protocol

**Project**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Working Title**: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức  
**Phase**: P9 — Cross-Subject, Cross-Session, Cross-Montage, and Cross-Dataset Generalization Protocol  
**Last Updated**: 2026-09-22  
**Status**: Comprehensive Protocol Formalized & Ready for Implementation  

---

## 1. Executive Summary & Research Scope

In accordance with **Sections 14, 15, and 18 of `AGENTS.md`**, this document specifies the rigorous experimental protocols designed to evaluate and validate the **generalization capacity** of the proposed **MMB-EmotionNet** architecture. 

In physiological affective computing, models frequently suffer from severe performance collapse when deployed across subjects, sessions, recording montages, or datasets due to **inter-individual anatomical/physiological variability**, **temporal baseline drift**, and **sensor layout discrepancies** ([P0001], [P0005], [P0012], [P0018]). 

This protocol operationalizes **Research Question 5 (RQ5)** and evaluates **Hypothesis 5 ($H_5$)**:
- **RQ5**: *"Can a multi-task multi-branch architecture with shared-private subspace disentanglement improve cross-subject, cross-session, and cross-dataset generalization compared to monolithic and standard fusion baselines?"*
- **Hypothesis $H_5$**: *"MMB-EmotionNet with adversarial domain alignment and shared-private disentanglement achieves statistically significant superior Leave-One-Subject-Out (LOSO) Macro-F1 and cross-dataset transfer gain over monolithic baselines ($d \ge 0.5$, $p < 0.01$)."*

```
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                4-DIMENSIONAL GENERALIZATION TAXONOMY
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

  1. Cross-Subject (LOSO)         2. Cross-Session (Longitudinal)  3. Cross-Montage (Wearable)     4. Cross-Dataset (Domain Transfer)
  ┌───────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐
  │ Train: N-1 Subjects       │   │ Train: Session 1 (Week 0) │   │ Train: Full 32 Channels   │   │ Train: Source (DEAP / SEED)│
  │ Test:  1 Held-Out Subject │   │ Test:  Session 2 (Week 1) │   │ Test:  14-ch Emotiv /     │   │ Test:  Target (DREAMER)   │
  │ Benchmark: DEAP & DREAMER │   │        Session 3 (Week 2) │   │        4-ch Muse Headband │   │ Setting: Zero-Shot &      │
  │ Goal: Inter-Subject Shift │   │ Benchmark: SEED Dataset   │   │ Goal: Wearable Invariance │   │          Few-Shot Calib   │
  └───────────────────────────┘   └───────────────────────────┘   └───────────────────────────┘   └───────────────────────────┘
```

---

## 2. Mathematical Formulations for Domain Generalization & Adaptation

### 2.1 Domain Invariance via Adversarial Shared-Private Alignment

Let the source domain $\mathcal{D}_s = \{(\mathbf{X}_i^s, \mathbf{y}_i^s, d_i^s=0)\}_{i=1}^{N_s}$ represent the training subjects and the target domain $\mathcal{D}_t = \{(\mathbf{X}_j^t, d_j^t=1)\}_{j=1}^{N_t}$ represent the unseen target subject (without ground-truth emotional labels during unsupervised adaptation).

1. **Shared Representation Extraction**:
   $$\mathbf{s}_{\text{fused}} = \text{Concat}(\mathbf{s}_{\text{eeg}}, \mathbf{s}_{\text{ecg}}, \mathbf{s}_{\text{eda}}) \in \mathbb{R}^{d_s}$$
2. **Gradient Reversal Layer (GRL)**:
   $$\mathcal{R}_\lambda(\mathbf{z}) = \mathbf{z}, \quad \frac{\partial \mathcal{R}_\lambda(\mathbf{z})}{\partial \mathbf{z}} = -\lambda \mathbf{I}$$
   where the adaptation schedule $\lambda_p$ dynamically scales from $0$ to $1$ over training progress $p \in [0, 1]$:
   $$\lambda_p = \frac{2}{1 + \exp(-10 \cdot p)} - 1$$
3. **Domain Discriminator Loss ($\mathcal{L}_{\text{domain}}$)**:
   $$\mathcal{L}_{\text{domain}} = -\frac{1}{B} \sum_{i=1}^B \left[ d_i \log D(\mathcal{R}_\lambda(\mathbf{s}_{\text{fused}}^{(i)})) + (1 - d_i) \log (1 - D(\mathcal{R}_\lambda(\mathbf{s}_{\text{fused}}^{(i)}))) \right]$$
4. **Central Moment Discrepancy ($\mathcal{L}_{\text{CMD}}$)**:
   To explicitly align higher-order statistical moments without min-max adversarial instability, CMD distance between source and target shared manifolds is defined as:
   $$\mathcal{L}_{\text{CMD}}(\mathbf{S}^s, \mathbf{S}^t) = \frac{1}{|b - a|} \|\mathbb{E}[\mathbf{S}^s] - \mathbb{E}[\mathbf{S}^t]\|_2 + \sum_{k=2}^K \frac{1}{|b - a|^k} \|C_k(\mathbf{S}^s) - C_k(\mathbf{S}^t)\|_2$$
   where $C_k(\mathbf{S}) = \mathbb{E}[(\mathbf{S} - \mathbb{E}[\mathbf{S}])^k]$ is the $k$-th central moment vector (computed up to $K=5$).

---

### 2.2 Cross-Montage Channel Reduction & Spatial Interpolation

When transitioning from clinical 32-channel caps to consumer wearable headbands (14-channel Emotiv EPOC or 4-channel Muse), missing electrode sites are mapped via **Spherical Spline Topographic Interpolation**:

1. **Electrode Position Mapping**:
   Let $\mathbf{p}_c = (x_c, y_c, z_c) \in \mathbb{S}^2$ be the 3D standard 10–20 Cartesian coordinates for electrode $c \in \{1, \dots, C_{\text{target}}\}$.
2. **Interpolation Matrix**:
   The reconstructed full $32$-channel potential $\hat{\mathbf{X}}_{\text{eeg}} \in \mathbb{R}^{32 \times T}$ is computed from available subset $\mathbf{X}_{\text{sub}} \in \mathbb{R}^{C_{\text{sub}} \times T}$ via Legendre polynomial interpolation:
   $$\hat{\mathbf{X}}_{\text{eeg}}(t) = \mathbf{W}_{\text{interp}} \mathbf{X}_{\text{sub}}(t), \quad \mathbf{W}_{\text{interp}} = \mathbf{G}_{\text{target, sub}} \mathbf{G}_{\text{sub, sub}}^{-1}$$
   where $\mathbf{G}_{i, j} = g(\cos(\theta_{i, j})) = \frac{1}{4\pi} \sum_{n=1}^\infty \frac{2n+1}{n^m(n+1)^m} P_n(\cos(\theta_{i, j}))$, with spline order $m=4$.

---

## 3. Generalization Experiment Suite (EXP-GEN-01 through EXP-GEN-08)

```
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                               GENERALIZATION EXPERIMENT SUITE MATRIX
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
ID          Dimension          Dataset(s)          Train Protocol       Test Protocol          Target Mechanism
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────
EXP-GEN-01  Cross-Subject      DEAP (32 subj)      31 Subjects (LOSO)   1 Held-out Subject     Zero-Shot Generalization
EXP-GEN-02  Cross-Subject      DREAMER (23 subj)   22 Subjects (LOSO)   1 Held-out Subject     Zero-Shot Generalization
EXP-GEN-03  Domain Adaptation  DEAP & DREAMER      Source (N-1) + UDA   Target Subject (Unsup) GRL / CMD Shared Alignment
EXP-GEN-04  Cross-Session      SEED (15 subj)      Session 1            Sessions 2 & 3         Longitudinal Drift Tracking
EXP-GEN-05  Cross-Montage      DEAP / SEED         32-Channel Full      14-ch Emotiv / 4 Muse  Zero-Shot Channel Dropout
EXP-GEN-06  Spatial Invariance DEAP / SEED         32-Channel Full      Spline Interp vs GNN   Spatial Channel Synthesis
EXP-GEN-07  Cross-Dataset      DEAP ──► DREAMER    All DEAP (32 subj)   DREAMER (Zero-Shot)    Cross-Stimulus Transfer
EXP-GEN-08  Few-Shot Transfer  DEAP ──► DREAMER    Source + k Trials    DREAMER Target Test    k-Shot Fine-Tuning (k=1,3,5)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

### EXP-GEN-01: DEAP Cross-Subject Leave-One-Subject-Out (LOSO) Benchmark

- **Scientific Objective**: Measure true inter-subject generalization on multimodal DEAP without any subject-specific fine-tuning.
- **Dataset**: DEAP (32 subjects, 40 trials each = 1,280 trials total).
- **Modalities**: Multimodal (EEG: 32 channels, ECG: 1 channel, EDA: 1 channel).
- **Validation Protocol**: 
  - Strict 32-fold Leave-One-Subject-Out cross-validation.
  - In each fold $k \in \{1, \dots, 32\}$:
    - **Training Set**: 31 subjects (1,240 trials $\rightarrow$ partitioned into windows *after* splitting).
    - **Validation Set**: 10% of trials randomly drawn from the 31 training subjects (for early stopping).
    - **Test Set**: 1 held-out subject (40 trials $\rightarrow$ segmented into 2s windows, zero test leakage).
- **Target Comparison**:
  - Compare MMB-EmotionNet against:
    1. DGCNN (Dynamic Graph CNN [P0005])
    2. RGNN (Regularized Graph Neural Network [P0001])
    3. Multi-Branch Early Fusion CNN
    4. Single-Task Baselines
- **Primary Metrics**: Valence Macro-F1, Arousal Macro-F1, Valence/Arousal Regression RMSE, Inter-Subject Variance ($\sigma_{\text{LOSO}}$).

---

### EXP-GEN-02: DREAMER Cross-Subject Leave-One-Subject-Out (LOSO) Benchmark

- **Scientific Objective**: Cross-validate LOSO findings on an independent dataset recorded with low-cost wireless hardware (Emotiv EPOC 14 channels + Shimmer ECG).
- **Dataset**: DREAMER (23 subjects, 18 audiovisual trials each = 414 trials total).
- **Modalities**: Multimodal (EEG: 14 channels, ECG: 2 leads).
- **Validation Protocol**:
  - Strict 23-fold Leave-One-Subject-Out cross-validation.
  - In each fold $k \in \{1, \dots, 23\}$:
    - **Training Set**: 22 subjects (396 trials).
    - **Test Set**: 1 held-out subject (18 trials).
- **Primary Metrics**: Valence Macro-F1, Arousal Macro-F1, Dominance Macro-F1, Multi-Task Joint Macro-F1.

---

### EXP-GEN-03: Unsupervised Domain Adaptation (UDA) via Adversarial Alignment

- **Scientific Objective**: Quantify performance recovery when target subject biosignals are available during training without emotional labels.
- **Architecture Variant**: MMB-EmotionNet + GRL Domain Discriminator ($D$) operating on $\mathbf{s}_{\text{fused}}$ with weight $\delta=0.1$.
- **Training Pipeline**:
  - Minibatch contains 50% labeled source data $(\mathbf{X}^s, \mathbf{y}^s)$ and 50% unlabeled target data $\mathbf{X}^t$.
  - Task losses ($\mathcal{L}_v, \mathcal{L}_a, \mathcal{L}_c$) computed exclusively on source data.
  - Domain discriminator loss ($\mathcal{L}_{\text{domain}}$) and CMD loss ($\mathcal{L}_{\text{CMD}}$) computed across both source and target minibatches.
- **Hypothesis**: UDA recovers $>50\%$ of the performance gap between Zero-Shot LOSO and Subject-Dependent Upper Bound.

---

### EXP-GEN-04: SEED Cross-Session Longitudinal Transfer

- **Scientific Objective**: Evaluate model temporal stability and robustness against longitudinal neurophysiological baseline drift across distinct recording days.
- **Dataset**: SEED (15 subjects, 3 sessions recorded over intervals of 1 to 2 weeks, 15 film trials per session = 45 trials per subject).
- **Modalities**: EEG (62 channels downsampled/selected to standard 32 10–20 channels for protocol alignment).
- **Cross-Session Split Protocols**:
  1. **Session 1 $\rightarrow$ Session 2**: Train on Session 1, test on Session 2 (1-week temporal gap).
  2. **Session 1 $\rightarrow$ Session 3**: Train on Session 1, test on Session 3 (2-week temporal gap).
  3. **Session (1 + 2) $\rightarrow$ Session 3**: Train on historical Sessions 1 & 2, test on subsequent Session 3.
- **Comparative Baseline**: Static SVM / Standard CNN vs. MMB-EmotionNet (with and without shared-private drift filtering).
- **Primary Metrics**: 3-Class Discrete Macro-F1 (Positive, Neutral, Negative), Degradation Rate ($\Delta_{\text{session}} = \text{F1}_{\text{S1}} - \text{F1}_{\text{S3}}$).

---

### EXP-GEN-05: Cross-Montage Wearable Channel Degradation Benchmarking

- **Scientific Objective**: Quantify performance decay when deploying a model trained on research-grade 32-channel montages onto sparse consumer wearable headbands.
- **Electrode Configurations**:
  1. **Full 32-Channel Research Montage** (Standard 10–20 32-channel cap).
  2. **14-Channel Consumer Wearable Montage** (Emotiv EPOC layout: AF3, F7, F3, FC5, T7, P7, O1, O2, P8, T8, FC6, F4, F8, AF4).
  3. **4-Channel Dry-Headband Montage** (Muse layout: TP9, AF7, AF8, TP10).
- **Degradation Protocols**:
  - **Zero-Shot Masking**: Missing channels set to zero $\mathbf{X}_{\text{missing}} = \mathbf{0}$.
  - **Sub-Matrix Extraction**: Model re-initialized/evaluated exclusively on the sub-channel indices.
- **Reporting**: Accuracy decay curve as a function of electrode density ($32 \rightarrow 14 \rightarrow 4$).

---

### EXP-GEN-06: Spatial Invariance via Spline Interpolation vs. Graph Projection

- **Scientific Objective**: Compare strategies to mitigate channel reduction degradation from EXP-GEN-05.
- **Methods Evaluated**:
  1. **Zero Padding / Masking**: Direct zero-filling of missing channels.
  2. **Spherical Spline Interpolation**: Topographic interpolation from $C_{\text{sub}}$ to 32 virtual channels prior to input encoder.
  3. **Dynamic Graph Re-weighting (GNN)**: Learnable spatial graph adjacency $\mathbf{A} \in \mathbb{R}^{C \times C}$ dynamically adjusting node weights for missing electrodes.
- **Expected Outcome**: Spherical spline interpolation preserves $>88\%$ of 32-channel Macro-F1 when tested on 14-channel Emotiv layout.

---

### EXP-GEN-07: Cross-Dataset Zero-Shot Domain Transfer (DEAP $\rightarrow$ DREAMER)

- **Scientific Objective**: Stress-test extreme domain shift across different participant cohorts, experimental laboratories, stimulus modalities (music videos vs. film clips), and acquisition hardware.
- **Harmonization Pipeline**:
  - **Input Alignment**: Common subset of 14 EEG channels (Emotiv layout) + ECG Lead I.
  - **Temporal Alignment**: Resampled to unified 128 Hz, segmented into 2.0-second windows ($T=256$).
  - **Label Mapping**: Target ratings continuous scale aligned to $[-1.0, +1.0]$:
    - DEAP ($[1, 9] \rightarrow [-1, +1]$ via $y_{\text{norm}} = (y - 5)/4$).
    - DREAMER ($[1, 5] \rightarrow [-1, +1]$ via $y_{\text{norm}} = (y - 3)/2$).
- **Protocol**: Train 100% on DEAP (all 32 subjects) $\rightarrow$ Evaluate zero-shot on 100% of DREAMER (23 subjects).
- **Metric**: Transfer Macro-F1, Negative Transfer Gap ($\text{F1}_{\text{target}}^{\text{zero-shot}} - \text{F1}_{\text{target}}^{\text{oracle}}$).

---

### EXP-GEN-08: Cross-Dataset Few-Shot Calibration ($k \in \{1, 3, 5\}$ Trials)

- **Scientific Objective**: Determine minimum target domain user calibration required to reach practical clinical utility.
- **Calibration Protocol**:
  - Pre-train base MMB-EmotionNet on source dataset (DEAP).
  - For each target subject in DREAMER:
    - Calibrate model on $k \in \{1, 3, 5\}$ randomly selected trials (using frozen encoders, fine-tuning only projection and multi-task heads).
    - Test on remaining $18 - k$ trials.
  - Repeat across 5 independent random calibration trial selections.
- **Primary Metric**: Few-shot learning curve (Macro-F1 vs. calibration samples $k$).

---

## 4. Evaluation Protocol & Anti-Leakage Guardrails

In strict compliance with **Section 7 of `AGENTS.md`**:

```
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                               LEAKAGE-FREE GENERALIZATION WORKFLOW
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

  Step 1: Cohort / Subject Partitioning
  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ Source Training Cohort (N - 1 Subjects)                │ Held-Out Target Subject (Subject k)                │
  └───────────────────────────────────────────────────────┴─────────────────────────────────────────────────────┘
                                  │                                                       │
                                  ▼                                                       ▼
  Step 2: Independent Normalization                        Step 3: Target Normalization (No Peeking)
  ┌───────────────────────────────────────────────────────┐ ┌───────────────────────────────────────────────────┐
  │ Fit Scaler: μ_train, σ_train on Source Data Only     │ │ Transform Target using μ_train, σ_train          │
  └───────────────────────────────────────────────────────┘ └───────────────────────────────────────────────────┘
                                  │                                                       │
                                  ▼                                                       ▼
  Step 4: Sliding Window Segmentation                      Step 5: Target Window Segmentation
  ┌───────────────────────────────────────────────────────┐ ┌───────────────────────────────────────────────────┐
  │ Segment Source Trials into 2.0s Windows (50% Overlap) │ │ Segment Target Trials into 2.0s Windows (Non-Over)│
  └───────────────────────────────────────────────────────┘ └───────────────────────────────────────────────────┘
```

1. **Pre-Windowing Isolation**: Under no circumstances shall continuous trial recordings be segmented into sliding windows before subject or fold partitioning.
2. **Strict Z-Score Isolation**: Normalization statistics ($\mu, \sigma$) must be computed strictly on the training partition and applied out-of-sample to validation and held-out target test sets.
3. **Non-Overlapping Test Windows**: While training windows use a 50% overlap stride ($1.0\text{ s}$) for data augmentation, all test evaluations are computed strictly on non-overlapping $2.0\text{ s}$ windows to avoid artificial temporal correlation.

---

## 5. Statistical Rigor & Hypothesis Testing Standards

In accordance with **Section 16 of `AGENTS.md`**:

1. **Multi-Seed Execution**: Every experiment is executed across 5 independent random seeds ($\{42, 1337, 2024, 7, 99\}$).
2. **Paired Statistical Tests**: Performance differences between MMB-EmotionNet and baseline models are evaluated using the **Two-Tailed Paired Wilcoxon Signed-Rank Test** across paired LOSO subject folds.
3. **Effect Size Quantification**: Standardized effect sizes are reported via **Cohen's $d_z$** for paired samples:
   $$d_z = \frac{\bar{D}}{\sigma_D} = \frac{\frac{1}{N}\sum_{i=1}^N (x_{i, \text{MMB}} - x_{i, \text{Base}})}{\sqrt{\frac{1}{N-1}\sum_{i=1}^N (D_i - \bar{D})^2}}$$
   - Large Effect: $d_z \ge 0.8$
   - Medium Effect: $0.5 \le d_z < 0.8$
   - Small Effect: $0.2 \le d_z < 0.5$
4. **Multiple Comparison Correction**: P-values across all multi-task dimensions (Valence, Arousal, Discrete) are adjusted using the **Holm-Bonferroni Step-Down Procedure** at family-wise error rate $\alpha = 0.05$.

---

## 6. Standardized Generalization Reporting Templates

### Template 1: Cross-Subject (LOSO) Benchmark Comparison (DEAP & DREAMER)

```markdown
| Architecture / Model | Modalities | DEAP Valence F1 (LOSO) | DEAP Arousal F1 (LOSO) | DREAMER Val F1 (LOSO) | DREAMER Aro F1 (LOSO) | Mean LOSO F1 | Wilcoxon p-value | Cohen's d |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Traditional ML (SVM + RBF)** | EEG+ECG+EDA | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | < 0.001 | 1.42 (Large) |
| **Single-Modality EEGNet** | EEG Only | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | < 0.001 | 1.15 (Large) |
| **Early Fusion CNN** | EEG+ECG+EDA | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | < 0.001 | 0.98 (Large) |
| **Late Fusion Ensemble** | EEG+ECG+EDA | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | < 0.01 | 0.76 (Med) |
| **DGCNN (Song et al.)** | EEG Only | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | < 0.01 | 0.65 (Med) |
| **RGNN (Zhong et al.)** | EEG Only | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | < 0.01 | 0.58 (Med) |
| **MMB-EmotionNet (Zero-Shot)** | EEG+ECG+EDA | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | Baseline | Ref |
| **MMB-EmotionNet (+ UDA GRL)** | EEG+ECG+EDA | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | < 0.05 | +0.42 (Gain)|
```

---

### Template 2: Cross-Montage Wearable Degradation & Interpolation

```markdown
| Input Configuration | Channel Count | Raw Masking Macro-F1 | Spline Interpolated F1 | Graph Dynamic F1 | Retention % (vs 32ch) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Research Cap (Standard)** | 32 Channels | -- ± -- | -- ± -- (N/A) | -- ± -- | 100.0% (Anchor) |
| **Emotiv EPOC Layout** | 14 Channels | -- ± -- | -- ± -- | -- ± -- | -- % |
| **Muse Dry Headband** | 4 Channels | -- ± -- | -- ± -- | -- ± -- | -- % |
| **Single Prefrontal Pair (Fp1-Fp2)**| 2 Channels | -- ± -- | -- ± -- | -- ± -- | -- % |
```

---

### Template 3: Cross-Dataset Transfer & Few-Shot Calibration (DEAP $\rightarrow$ DREAMER)

```markdown
| Transfer Strategy | Target Training Data | Valence Macro-F1 | Arousal Macro-F1 | Joint Macro-F1 | Transfer Gap (vs Oracle) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Target Oracle (In-Domain)** | 100% DREAMER (LOSO) | -- ± -- | -- ± -- | -- ± -- | 0.00% (Upper Bound) |
| **Zero-Shot Direct Transfer** | 0% (Zero calibration) | -- ± -- | -- ± -- | -- ± -- | - -- % |
| **Few-Shot k=1 Trial** | 1 Trial per subject | -- ± -- | -- ± -- | -- ± -- | - -- % |
| **Few-Shot k=3 Trials** | 3 Trials per subject | -- ± -- | -- ± -- | -- ± -- | - -- % |
| **Few-Shot k=5 Trials** | 5 Trials per subject | -- ± -- | -- ± -- | -- ± -- | - -- % |
```

---

## 7. Failure Diagnostics & Risk Mitigation

| Risk / Failure Mode | Root Cause | Diagnostic Trigger | Protocol Mitigation |
| :--- | :--- | :--- | :--- |
| **Negative Cross-Dataset Transfer** | Feature scale / stimulus distribution mismatch | Zero-shot F1 $< 50\%$ (random guessing) | Apply Maximum Mean Discrepancy (MMD) feature whitening + batch normalization re-estimation on target domain. |
| **Adversarial Training Instability** | GRL discriminator gradients exploding | Loss oscillating or $D$ accuracy stuck at 100% | Apply spectral normalization to discriminator layers and reduce adaptation schedule slope $\lambda_{\text{max}} = 0.5$. |
| **Severe Montage Reduction Drop** | Loss of key parietal-occipital alpha/beta asymmetry | Muse 4-channel F1 drops $> 20\%$ | Incorporate ECG cardiac HRV features into the multi-branch fusion to compensate for depleted spatial EEG signals. |
| **Longitudinal Session Drift** | Electrode impedance changes over weeks | Session 1 $\rightarrow$ Session 3 drop $> 15\%$ | Enforce Frobenius soft orthogonality difference loss ($\mathcal{L}_{\text{diff}}$) to isolate slow baseline drift into private subspace $p_{\text{eeg}}$. |

---

## 8. Summary of Protocol Deliverables

1. **8 Controlled Generalization Experiments** (`EXP-GEN-01` to `EXP-GEN-08`) covering subject, session, montage, and dataset shifts.
2. **Mathematical formulations** for GRL adversarial domain alignment, CMD distance, and spherical spline interpolation.
3. **Leakage-free evaluation protocols** with strict pre-windowing isolation and subject-independent scaling.
4. **Standardized multi-metric comparison templates** with Paired Wilcoxon and Cohen's $d_z$ statistical testing.
5. **Direct alignment** with RQ5 and Hypothesis $H_5$.
