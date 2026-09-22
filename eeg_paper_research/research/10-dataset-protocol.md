# Phase P5: Dataset Selection & Preprocessing Protocol

**Project**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Working Title**: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức  
**Phase**: P5 — Dataset Selection & Preprocessing Protocol  
**Last Updated**: 2026-09-22  
**Status**: Formal Dataset Selection, Signal Pipelines, and Anti-Leakage Protocol Complete  

---

## 1. Benchmark Dataset Selection Strategy

In accordance with **Section 8 of `AGENTS.md`** and the hypotheses established in **Phase P4**, datasets are selected to rigorously test:
1. Multimodal central-autonomic interactions (EEG + ECG + EDA/GSR).
2. Multi-task continuous-discrete emotion targets (Valence, Arousal, Dominance, Discrete emotion classes).
3. Cross-subject (LOSO), cross-session, and missing-modality robustness.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   BENCHMARK DATASET TIER MATRIX                                   │
├───────────────────┬─────────────┬──────────┬──────────────────────┬───────────────────────────────┤
│ Tier              │ Dataset     │ Subjects │ Primary Modalities   │ Evaluated Research Hypotheses │
├───────────────────┼─────────────┼──────────┼──────────────────────┼───────────────────────────────┤
│ Tier 1 (Primary)  │ DEAP        │ 32       │ EEG (32), ECG, EDA,  │ H1 (Multimodal), H2 (Branch), │
│                   │             │          │ EMG, RSP, PPG, Temp  │ H3 (Disentang), H4 (MTL), H6  │
├───────────────────┼─────────────┼──────────┼──────────────────────┼───────────────────────────────┤
│ Tier 1 (Primary)  │ DREAMER     │ 23       │ EEG (14), ECG (2)    │ H1 (Dual-branch CNS-ANS),     │
│                   │             │          │                      │ H2 (Branch), H5 (LOSO), H6    │
├───────────────────┼─────────────┼──────────┼──────────────────────┼───────────────────────────────┤
│ Tier 2 (Secondary)│ SEED /      │ 15 / 15  │ EEG (62 ch),         │ H2 (Graph/Spatial), H3,       │
│                   │ SEED-IV     │          │ Eye Tracking         │ H5 (Cross-Subject/Session)    │
├───────────────────┼─────────────┼──────────┼──────────────────────┼───────────────────────────────┤
│ Tier 2 (Generaliz)│ AMIGOS      │ 40       │ EEG (14), ECG, EDA,  │ H1 (Multimodal), H4 (MTL      │
│                   │             │          │ Video (Short/Long)   │ Continuous + Discrete Basic 7)│
└───────────────────┴─────────────┴──────────┴──────────────────────┴───────────────────────────────┘
```

---

## 2. Modality Preprocessing Pipelines

---

### 2.1 EEG Signal Preprocessing Pipeline

```
Raw Scalp EEG (32 / 62 ch)
     │
     ▼
[Step 1: Referencing Standardization] ──► Common Average Reference (CAR) or REST Neutral Surface ([P0027])
     │
     ▼
[Step 2: Bandpass & Notch Filtering] ──► Zero-phase 4th-order Butterworth Filter (0.5 – 45.0 Hz) + 50/60 Hz Notch
     │
     ▼
[Step 3: Artifact Cleaning] ──────────► ICA / Blind Source Separation removing Ocular (EOG) & Muscle (EMG) peaks
     │
     ▼
[Step 4: Temporal Segmentation] ──────► Non-overlapping 2-second or 4-second windows (256 / 512 samples at 128 Hz)
     │
     ▼
[Step 5: Fold-Isolated Z-Score] ──────► Standardized using Training Fold Mean (μ_train) & Std (σ_train) ONLY
```

- **Referencing Standard**: Common Average Reference (CAR) is enforced across all EEG channels:
  $$V_i^{CAR}(t) = V_i(t) - \frac{1}{C}\sum_{j=1}^C V_j(t)$$
  to eliminate localized monopolar reference bias ([`P0027`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0027.md)).
- **Sampling Rate Alignment**: All EEG streams are resampled to $f_s = 128\text{ Hz}$ via polyphase anti-aliasing interpolation.
- **Frequency Sub-band Decomposition** (for feature-based baselines):
  - Delta ($\delta$): $0.5 - 4\text{ Hz}$
  - Theta ($\theta$): $4.0 - 8.0\text{ Hz}$
  - Alpha ($\alpha$): $8.0 - 13.0\text{ Hz}$
  - Beta ($\beta$): $14.0 - 30.0\text{ Hz}$
  - Gamma ($\gamma$): $31.0 - 45.0\text{ Hz}$

---

### 2.2 Peripheral Biosignal Preprocessing Pipelines

#### A. Electrocardiogram (ECG) / Photoplethysmography (PPG)
- **Filtering**: Bandpass filtered between $0.5\text{ Hz}$ and $40.0\text{ Hz}$ (removes baseline respiratory wander and high-frequency EMG tremor).
- **R-Peak Detection & HRV**: Pan-Tompkins QRS detection algorithm identifying $R$-$R$ intervals ($NN$ series).
- **Extracted Feature Tensor**:
  - Time-Domain: Mean Heart Rate (HR), SDNN (Standard deviation of NN intervals), RMSSD (Root mean square of successive differences), pNN50.
  - Frequency-Domain: Low Frequency power (LF: 0.04–0.15 Hz), High Frequency power (HF: 0.15–0.40 Hz), Sympathovagal balance ratio ($\text{LF}/\text{HF}$).
  - Raw Waveform: 1D normalized time-series segment synchronized with the EEG window.

#### B. Electrodermal Activity (EDA / GSR)
- **Decomposition**: Continuous Deconvolution Analysis (CDA) decomposing EDA into:
  - **Tonic Component (Skin Conductance Level - SCL)**: Low-pass filtered ($< 0.05\text{ Hz}$) reflecting baseline autonomic tone.
  - **Phasic Component (Skin Conductance Response - SCR)**: High-pass filtered ($0.05 - 1.0\text{ Hz}$) capturing event-related sympathetic arousal spikes.
- **Metrics Extracted**: Mean SCL, SCR peak count, mean peak amplitude, cumulative response energy.

#### C. Respiration (RSP)
- **Filtering**: Low-pass filtered at $1.0\text{ Hz}$ to smooth chest expansion waveforms.
- **Metrics Extracted**: Breathing rate (breaths per minute), breath duration variability, inhale/exhale ratio.

---

## 3. Label Processing & Multi-Task Formulation

---

### 3.1 Continuous Regression Tasks
- **Valence ($y_v \in [1.0, 9.0]$)**: Normalized to $[-1.0, 1.0]$ via affine transform: $\tilde{y}_v = \frac{y_v - 5.0}{4.0}$.
- **Arousal ($y_a \in [1.0, 9.0]$)**: Normalized to $[-1.0, 1.0]$: $\tilde{y}_a = \frac{y_a - 5.0}{4.0}$.
- **Dominance ($y_d \in [1.0, 9.0]$)**: Normalized to $[-1.0, 1.0]$: $\tilde{y}_d = \frac{y_d - 5.0}{4.0}$.
- **Loss Metric**: Mean Squared Error (MSE) / Huber Loss with Pearson correlation $r$.

---

### 3.2 Discrete Classification Tasks
- **Binary High vs. Low Valence/Arousal**:
  - High ($1$) if $y \ge 5.0$; Low ($0$) if $y < 5.0$.
  - Thresholding performed on raw ratings per subject.
- **Categorical Discrete Emotion (SEED / AMIGOS)**:
  - SEED: 3 classes (Positive, Neutral, Negative) encoded as one-hot vectors $\mathbf{y}_c \in \{0, 1\}^3$.
  - SEED-IV: 4 classes (Happy, Sad, Fear, Neutral) $\mathbf{y}_c \in \{0, 1\}^4$.
  - AMIGOS: 7 discrete emotion categories (Happiness, Sadness, Anger, Fear, Disgust, Surprise, Neutral).
- **Loss Metric**: Categorical Cross-Entropy Loss with Softmax activation.

---

## 4. Strict Data Leakage Audit & Safeguards

In compliance with **Section 7 of `AGENTS.md`** and the findings from [`P0030`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0030.md), the experimental pipeline enforces six mandatory anti-leakage safeguards:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               STRICT ANTI-LEAKAGE PARTITIONING FLOW                               │
└───────────────────────────────────────────────────┬───────────────────────────────────────────────┘
                                                    │
                 ┌──────────────────────────────────┴──────────────────────────────────┐
                 ▼                                                                     ▼
┌─────────────────────────────────────────────────┐                 ┌─────────────────────────────────────┐
│  PROTOCOL A: Subject-Independent (LOSO)         │                 │  PROTOCOL B: Subject-Dependent (CV) │
├─────────────────────────────────────────────────┤                 ├─────────────────────────────────────┤
│ 1. Group by Subject ID                          │                 │ 1. Group by Trial ID (60s videos)   │
│ 2. Split: Train on N-1 Subjects, Test on 1 Subj │                 │ 2. Split: 80% Train Trials / 20% Test│
│ 3. Compute (μ_train, σ_train) strictly on Train │                 │ 3. Compute (μ_train, σ_train)       │
│ 4. Windowing applied AFTER subject isolation    │                 │ 4. Windowing applied AFTER trial iso│
│ 5. NO test subject data in training pipeline    │                 │ 5. NO window from same trial in test│
└─────────────────────────────────────────────────┘                 └─────────────────────────────────────┘
```

| Leakage Dimension | Potential Flaw Identified in Literature | Enforced Anti-Leakage Safeguard in this Project | Verification Check |
|---|---|---|---|
| **1. Windowing Leakage** | Segmenting 60s trial into overlapping windows *before* splitting (inflates accuracy $>95\%$) | **Partitioning strictly precedes windowing**: Whole trials or whole subjects are partitioned first; windowing occurs independently inside folds. | Check that no two overlapping windows share the same Trial ID across train and test sets. |
| **2. Subject Contamination** | Random cross-validation mixing samples from the same subject across train and test | **Strict Subject-Grouping in LOSO**: In subject-independent evaluation, all trials from test subject $k$ are strictly isolated. | Verify $\text{Subjects}(\mathcal{D}_{train}) \cap \text{Subjects}(\mathcal{D}_{test}) = \emptyset$. |
| **3. Normalization Leakage** | Computing global z-score mean ($\mu$) and standard deviation ($\sigma$) over the entire dataset | **Fold-Isolated Normalization**: Mean ($\mu_{train}$) and standard deviation ($\sigma_{train}$) are computed strictly on training folds and applied to validation/test folds. | Verify test statistics are never used during feature scaling. |
| **4. Temporal Smoothing Leakage** | Applying Linear Dynamic System (LDS) or Kalman filter smoothing across trial boundaries | **Intra-Trial Smoothing Only**: Temporal filtering is fitted strictly within single trial blocks and never smoothed across split boundaries. | Verify filter state resets at every trial boundary. |
| **5. Hyperparameter Leakage** | Selecting model hyperparameters or early stopping on the test set | **Nested Cross-Validation**: Hyperparameter tuning and model checkpointing use an internal validation split ($\mathcal{D}_{val}$) extracted solely from $\mathcal{D}_{train}$. | Test set is evaluated exactly once after all training is finalized. |
| **6. Augmentation Leakage** | Applying data augmentations before splitting folds | **Train-Set Only Augmentation**: Augmentations (e.g. Gaussian jitter, electrode dropout) are applied exclusively to training folds. | Verify test fold contains only raw un-augmented physiological windows. |

---

## 5. Standardized Train/Val/Test Split Configurations

### Configuration 1: Leave-One-Subject-Out (LOSO) — Primary Benchmark
- For a dataset with $N$ participants:
  - Iteration $k \in \{1, \dots, N\}$:
    - **Test Set ($\mathcal{D}_{test}$)**: All trials from Subject $k$ (100% held-out unseen subject).
    - **Validation Set ($\mathcal{D}_{val}$)**: Random $10\%$ of trials from the remaining $N-1$ training subjects (for early stopping).
    - **Training Set ($\mathcal{D}_{train}$)**: Remaining $90\%$ of trials from $N-1$ training subjects.
  - Final Metric: Mean $\pm$ Standard Deviation across all $N$ folds.

### Configuration 2: Subject-Dependent 10-Fold Cross-Validation — Secondary Benchmark
- For each subject independently:
  - 40 trials grouped into 10 folds (4 distinct trials per fold).
  - Train on 9 folds (36 trials), test on 1 fold (4 trials), repeated 10 times.
  - No sliding windows from the same 60s trial ever appear simultaneously in train and test sets.

---

## 6. Synthesis & Transition to Phase P6

With the primary benchmark datasets selected, preprocessing filtering and referencing mathematically formalized, and strict anti-leakage partitioning pipelines established, the project is ready to proceed to **Phase P6: Baseline Architecture & Benchmark Implementation Protocol** to specify the complete baseline suite.
