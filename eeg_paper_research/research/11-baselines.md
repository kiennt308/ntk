# Phase P6: Baseline Architecture & Benchmark Protocol

**Project**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Working Title**: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức  
**Phase**: P6 — Baseline Architecture & Benchmark Implementation Protocol  
**Last Updated**: 2026-09-22  
**Status**: Formal Specification of 9 Baseline Families & Unified Benchmarking Suite  

---

## 1. Baseline Policy & Methodological Control

In strict compliance with **Section 9 of `AGENTS.md`**, the proposed multi-task multi-branch architecture must NOT be compared only against weak or naive baselines. To ensure rigorous scientific attribution, all comparisons must satisfy three strict experimental controls:
1. **Identical Preprocessing & Data Splits**: Every baseline is trained and evaluated on the exact same fold partitions generated in **Phase P5** ([`research/10-dataset-protocol.md`](file:///d:/ntk/eeg_paper_research/research/10-dataset-protocol.md)) with zero test-set leakage.
2. **Controlled Parameter & Computational Budgets**: Baseline models are parameter-matched where applicable to separate architectural inductive bias from sheer parameter capacity.
3. **Multi-Faceted Evaluation Metrics**: Evaluated across both classification metrics (Macro-F1, Balanced Accuracy) and regression metrics (RMSE, Pearson's $r$) alongside computational complexity (FLOPs, latency, parameters).

---

## 2. Specification of the 9 Baseline Model Families

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       9 BASELINE MODEL FAMILIES                                         │
├────────────────────────────────┬────────────────────────────────────────────────────────────────────────┤
│ Family                         │ Representative Architectural Baselines                                 │
├────────────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 1. Traditional ML              │ SVM (RBF Kernel), Random Forest (100 trees), XGBoost (PSO-tuned [P0010])│
│ 2. Single-Modality DL          │ EEGNet-8,2 ([P0007]), ShallowConvNet, 1D-CNN (ECG/EDA branches)         │
│ 3. Multimodal Early Fusion     │ Feature Concatenation + 3-Layer Deep MLP                               │
│ 4. Multimodal Late Fusion      │ Decision Stacking & Posterior Probability Averaging ([P0001], [P0014]) │
│ 5. Monolithic Shared Encoder   │ Single Multi-Channel 2D-CNN processing stacked heterogeneous channels  │
│ 6. Multi-Branch Intermediate   │ Unconstrained Multi-Branch Encoders + Feature Concatenation ([P0003])   │
│ 7. Single-Task Deep Models     │ Isolated single-task models for Valence, Arousal, and Discrete Emotion │
│ 8. Fixed-Weight Multi-Task     │ Multi-Task Network with static fixed loss weights (λ1=1.0, λ2=1.0, λ3=1)│
│ 9. Literature SOTA Baselines   │ DGCNN ([P0012]), RGNN ([P0002]), STRNN ([P0011]), MISA adaptation     │
└────────────────────────────────┴────────────────────────────────────────────────────────────────────────┘
```

---

### Family 1: Traditional Machine Learning Baselines

Applied to standard handcrafted features (Differential Entropy across 5 frequency bands for EEG; HRV time/frequency stats for ECG; Tonic/Phasic SCR stats for EDA).

1. **Baseline 1.1 — Support Vector Machine (SVM-RBF)**:
   - Kernel: Radial Basis Function (RBF) $K(\mathbf{x}_i, \mathbf{x}_j) = \exp(-\gamma \|\mathbf{x}_i - \mathbf{x}_j\|^2)$.
   - Hyperparameter Grid: Regularization $C \in \{0.1, 1.0, 10.0, 100.0\}$, $\gamma \in \{10^{-4}, 10^{-3}, 10^{-2}, \text{'scale'}\}$.
   - Multi-class: One-vs-Rest (OvR).
2. **Baseline 1.2 — Random Forest Classifier / Regressor**:
   - Estimators: 100 decision trees, maximum depth $d_{max} \in \{10, 20, \text{None}\}$, minimum samples split = 2.
   - Criterion: Gini Impurity (classification) / Mean Squared Error (regression).
3. **Baseline 1.3 — Extreme Gradient Boosting (XGBoost)** ([`P0010`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0010.md)):
   - Parameters: Max depth = 6, learning rate $\eta = 0.05$, subsample = 0.8, colsample_bytree = 0.8, n_estimators = 200.

---

### Family 2: Single-Modality Deep Learning Baselines

Evaluated on individual sensor streams to establish unimodal lower bounds (testing **RQ1**).

1. **Baseline 2.1 — EEG-Only: EEGNet (Lawhern et al. 2018; [`P0007`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0007.md))**:
   - **Architecture**:
     - Block 1: 2D Temporal Conv ($1 \times 64$, $F_1=8$) $\rightarrow$ BatchNorm $\rightarrow$ Depthwise Spatial Conv ($C \times 1$, $D=2$) $\rightarrow$ BatchNorm $\rightarrow$ ELU $\rightarrow$ AvgPool ($1 \times 4$) $\rightarrow$ Dropout ($p=0.25$).
     - Block 2: Separable Conv ($1 \times 16$, $F_2=16$) $\rightarrow$ BatchNorm $\rightarrow$ ELU $\rightarrow$ AvgPool ($1 \times 8$) $\rightarrow$ Dropout ($p=0.25$).
     - Dense Classification / Regression Head ($16 \times 16 \rightarrow \text{Output}$).
   - **Parameters**: $\approx 2,500$ parameters ($C=32$ channels).
2. **Baseline 2.2 — EEG-Only: ShallowConvNet (Schirrmeister et al. 2017)**:
   - Temporal Conv ($1 \times 25$) $\rightarrow$ Spatial Conv ($C \times 1$, 40 filters) $\rightarrow$ Square Activation $\rightarrow$ MeanPool ($1 \times 75$, stride 15) $\rightarrow$ Log Activation $\rightarrow$ Dropout ($p=0.5$).
   - **Parameters**: $\approx 45,000$ parameters.
3. **Baseline 2.3 — Peripheral-Only: 1D Multi-Scale Dilated CNN (ECG + EDA)** ([`P0001`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0001.md), [`P0015`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0015.md)):
   - 3-Layer 1D-CNN with dilation rates $d \in \{1, 2, 4\}$, kernel size $k=7$, filters = 32, 64, 128 $\rightarrow$ Global Average Pooling $\rightarrow$ Dense Head.
   - **Parameters**: $\approx 65,000$ parameters.

---

### Family 3: Multimodal Early Fusion Baseline

1. **Baseline 3.1 — Early Feature Concatenation + Deep MLP**:
   - All preprocessed features from EEG (32 channels $\times$ 5 bands = 160), ECG (12 HRV features), and EDA (8 SCL/SCR features) are concatenated into a single input vector $\mathbf{x}_{early} \in \mathbb{R}^{180}$.
   - **Encoder**: 4-Layer Dense Network ($180 \rightarrow 256 \rightarrow 128 \rightarrow 64 \rightarrow \text{Output}$) with BatchNorm, LeakyReLU ($\alpha=0.1$), and Dropout ($p=0.3$).
   - **Parameters**: $\approx 115,000$ parameters.

---

### Family 4: Multimodal Late Decision Fusion Baseline

1. **Baseline 4.1 — Posterior Probability Averaging & Meta-Learner Stacking** ([`P0001`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0001.md), [`P0014`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0014.md)):
   - Unimodal networks (EEGNet for EEG, 1D-CNN for ECG, 1D-CNN for EDA) are trained independently.
   - Predicted class posterior probabilities $\mathbf{p}_{eeg}, \mathbf{p}_{ecg}, \mathbf{p}_{eda} \in \mathbb{R}^K$ are fused via:
     - Scheme A (Weighted Linear Sum): $\mathbf{p}_{fused} = w_1 \mathbf{p}_{eeg} + w_2 \mathbf{p}_{ecg} + w_3 \mathbf{p}_{eda}$, with $\sum w_i = 1$.
     - Scheme B (Meta-Classifier Stacking): Logistic Regression / Linear SVM trained on concatenated posterior vectors $[\mathbf{p}_{eeg}; \mathbf{p}_{ecg}; \mathbf{p}_{eda}]$.

---

### Family 5: Monolithic Shared Encoder Baseline

1. **Baseline 5.1 — Monolithic Multi-Channel 2D-CNN** (testing **RQ2**):
   - All heterogeneous biosignal channels (32 EEG + 2 ECG + 1 EDA = 35 channels) are stacked into a single multi-channel 2D matrix $\mathbf{X} \in \mathbb{R}^{35 \times T}$.
   - **Architecture**: Monolithic 4-layer 2D-CNN treating all channels uniformly without modality-specific spatial or temporal branching.
   - **Parameters**: Matched to $\approx 180,000$ parameters (identical to the total parameter budget of the multi-branch model).

---

### Family 6: Multi-Branch Intermediate Fusion Baseline

1. **Baseline 6.1 — Multi-Branch Intermediate Concatenation (Without Disentanglement)** ([`P0003`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0003.md), testing **RQ2 & RQ3**):
   - Branch 1: EEGNet encoder producing latent embedding $\mathbf{h}_{eeg} \in \mathbb{R}^{64}$.
   - Branch 2: ECG 1D-CNN encoder producing latent embedding $\mathbf{h}_{ecg} \in \mathbb{R}^{32}$.
   - Branch 3: EDA 1D-CNN encoder producing latent embedding $\mathbf{h}_{eda} \in \mathbb{R}^{32}$.
   - **Fusion**: Simple intermediate concatenation $\mathbf{h}_{joint} = [\mathbf{h}_{eeg}; \mathbf{h}_{ecg}; \mathbf{h}_{eda}] \in \mathbb{R}^{128}$ fed directly to the classification head without shared-private separation ($\mathcal{L}_{sim} = 0, \mathcal{L}_{diff} = 0$).

---

### Family 7: Single-Task Deep Learning Baselines

1. **Baseline 7.1 — Isolated Single-Task Multi-Branch Models** (testing **RQ4**):
   - Model 7.1a (Valence-Only): Multi-branch encoder trained strictly on Valence loss $\mathcal{L}_v$.
   - Model 7.1b (Arousal-Only): Multi-branch encoder trained strictly on Arousal loss $\mathcal{L}_a$.
   - Model 7.1c (Emotion-Only): Multi-branch encoder trained strictly on Discrete Emotion classification loss $\mathcal{L}_c$.

---

### Family 8: Fixed-Weight Multi-Task Learning Baseline

1. **Baseline 8.1 — Multi-Task Network with Static Loss Weighting** (testing **RQ4**):
   - Multi-branch encoder with 3 task heads (Valence, Arousal, Emotion).
   - Joint Loss:
     $$\mathcal{L}_{fixed} = \lambda_1 \mathcal{L}_{valence}(W) + \lambda_2 \mathcal{L}_{arousal}(W) + \lambda_3 \mathcal{L}_{emotion}(W)$$
   - Static hyperparameter weights: $\lambda_1 = 1.0, \lambda_2 = 1.0, \lambda_3 = 1.0$ (and grid-searched optimal static weights $\lambda_1=0.5, \lambda_2=0.5, \lambda_3=1.0$).

---

### Family 9: Literature SOTA Baselines

Exact re-implementations of top published peer-reviewed models from our verified literature base:

1. **Baseline 9.1 — Dynamic Graph Convolutional Neural Network (DGCNN; Song et al. 2020; [`P0012`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0012.md))**:
   - 2-Layer Dynamic Graph Convolution with learnable adjacency matrix $\mathbf{W} \in \mathbb{R}^{C \times C}$, Chebyshev polynomial degree $K=2$.
   - **Parameters**: $\approx 85,000$ parameters.
2. **Baseline 9.2 — Regularized Graph Neural Network (RGNN; Zhong et al. 2020; [`P0002`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0002.md))**:
   - Graph convolution with node-level $L_1$ sparsity regularizer ($\|\mathbf{A}\|_1$) and topological inter-channel distance matrix penalty ($\sum D_{ij} A_{ij}$).
   - **Parameters**: $\approx 120,000$ parameters.
3. **Baseline 9.3 — Spatial-Temporal Recurrent Neural Network (STRNN; Zhang et al. 2017; [`P0011`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0011.md))**:
   - Spatial multidirectional RNN layer + Temporal LSTM units ($64$ hidden units).
   - **Parameters**: $\approx 320,000$ parameters.
4. **Baseline 9.4 — MISA Multimodal Subspace Adaptation (Hazarika et al. 2020; [`P0003`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0003.md) adaptation)**:
   - Shared-private disentanglement with Central Moment Discrepancy (CMD) and soft Frobenius orthogonality, adapted to biosignal time-series.
   - **Parameters**: $\approx 210,000$ parameters.

---

## 3. Unified Training & Optimization Protocol

To eliminate confounding experimental variables, all deep neural baselines and proposed models share identical optimization hyperparameter environments:

| Parameter | Configuration / Value | Rationale |
|---|---|---|
| **Optimizer** | AdamW ($\beta_1 = 0.9, \beta_2 = 0.999$) | Stable convergence with decoupled weight decay |
| **Weight Decay** | $1 \times 10^{-4}$ | Prevents small-sample overfitting on biosignal epochs |
| **Initial Learning Rate** | $1 \times 10^{-3}$ (with Cosine Annealing to $1 \times 10^{-6}$) | Smooth learning rate schedule |
| **Batch Size** | 32 (DEAP / DREAMER), 16 (SEED) | Balanced gradient variance across trial lengths |
| **Maximum Epochs** | 150 epochs (with Early Stopping patience = 20) | Terminated based on validation set ($\mathcal{D}_{val}$) loss |
| **Random Seeds** | $N_{seeds} = 5$ fixed seeds (`[42, 123, 456, 789, 2026]`) | Mitigates initialization luck; mean ± std reported |
| **Hardware Environment** | Single NVIDIA GPU, PyTorch 2.x, deterministic cuDNN | Guaranteed mathematical reproducibility |

---

## 4. Evaluation Metrics Suite

In compliance with **Section 15 of `AGENTS.md`**, models are evaluated across 4 dimensional tiers:

1. **Classification Metrics**:
   - **Macro-F1 Score**: $\text{Macro-F1} = \frac{1}{K}\sum_{k=1}^K \frac{2 \times \text{Precision}_k \times \text{Recall}_k}{\text{Precision}_k + \text{Recall}_k}$ (Primary metric for class-imbalanced emotion bins).
   - **Balanced Accuracy**: $\text{Balanced Acc} = \frac{1}{K}\sum_{k=1}^K \frac{\text{TP}_k}{\text{TP}_k + \text{FN}_k}$.
   - **Confusion Matrix**: Full normalized matrix across classes.
2. **Regression Metrics**:
   - **Root Mean Squared Error (RMSE)**: $\text{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2}$.
   - **Pearson's Correlation Coefficient ($r$)**: Measures linear tracking dynamics of continuous affective trajectories.
3. **Multi-Task Balance Metric**:
   - **Negative Transfer Index ($\Delta_{MTL}$)**: $\Delta_{MTL} = \frac{1}{T}\sum_{t=1}^T \frac{M_{MTL, t} - M_{STL, t}}{M_{STL, t}}$ (Positive value indicates successful synergy).
4. **Computational Efficiency Metrics**:
   - Total Trainable Parameter Count ($N_{params}$).
   - Floating-Point Operations per Sample (FLOPs).
   - GPU / CPU Inference Latency per 2-second Window (milliseconds).

---

## 5. Synthesis & Transition to Phase P7

With the full suite of 9 baseline families formally specified, unified training settings fixed, and evaluation protocols calibrated, the project is ready to proceed to **Phase P7: Proposed Multi-Task Multi-Branch Architecture Design & Implementation**.
