# Phase P2: Literature Classification & Deep Synthesis

**Project**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Working Title**: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức  
**Phase**: P2 — Literature Classification & Architectural Synthesis  
**Last Updated**: 2026-09-22  
**Status**: Formal Mathematical & Structural Classification Complete  

---

## 1. Executive Synthesis & Architectural Landscape

Based on the 30 verified peer-reviewed publications and benchmark corpora ([`P0001`–`P0030`](file:///d:/ntk/eeg_paper_research/literature/index/paper-index.csv)), existing literature in affective computing from biosignals can be systematically classified into four major architectural paradigms:

```
PARADIGM 1: Monolithic Early Fusion
┌─────────────┐
│ EEG Signals │──┐
└─────────────┘  │
┌─────────────┐  ├──► [Raw Concatenation] ──► [Heavy Monolithic Encoder] ──► [Single Task Head]
│ Periph Bios │──┘                                 (CNN / MLP)
└─────────────┘
Drawbacks: Rate mismatch, noise propagation, EEG gradient dominance.

─────────────────────────────────────────────────────────────────────────────────────────────

PARADIGM 2: Uncoupled Late Decision Fusion
┌─────────────┐     ┌────────────────┐     ┌───────────────┐
│ EEG Signals │────►│ EEG Classifier │────►│ Prob. Vectors │──┐
└─────────────┘     └────────────────┘     └───────────────┘  │
┌─────────────┐     ┌────────────────┐     ┌───────────────┐  ├──► [Weighted Sum / Voting] ──► [Output]
│ Periph Bios │────►│ Periph Classif │────►│ Prob. Vectors │──┘
└─────────────┘     └────────────────┘     └───────────────┘
Drawbacks: Zero latent cross-modal interaction; fails to capture non-linear cortical-autonomic synchrony.

─────────────────────────────────────────────────────────────────────────────────────────────

PARADIGM 3: Multi-Branch Intermediate Fusion (Standard Deep Learning)
┌─────────────┐     ┌─────────────┐
│ EEG Stream  │────►│ EEG Encoder │──┐
└─────────────┘     └─────────────┘  │
┌─────────────┐     ┌─────────────┐  ├──► [Latent Concatenation / Tensor Fusion] ──► [Task Head]
│ ECG / EDA   │────►│ 1D-CNN Encod│──┘
└─────────────┘     └─────────────┘
Drawbacks: Fails to disentangle shared emotion from private sensor artifacts; redundant representation.

─────────────────────────────────────────────────────────────────────────────────────────────

PARADIGM 4: Multi-Task Multi-Branch Disentangled Attention Architecture (Proposed Target Scope)
┌─────────────┐     ┌─────────────────┐     ┌──► Shared Latent Subspace (cmd/mmd) ──┐     ┌────────────────────┐     ┌──► Task 1: Valence
│ EEG Stream  │────►│ EEGNet/TSception│─────┤                                       ├────►│ Cross-Modal Attn   │────►┼──► Task 2: Arousal
└─────────────┘     └─────────────────┘     └──► Private EEG Subspace (orthog) ─────┤     │ (QKV Projection)   │     └──► Task 3: Emotion
┌─────────────┐     ┌─────────────────┐     ┌──► Shared Latent Subspace (cmd/mmd) ──┤     │                    │          (Uncertainty Loss)
│ ECG/EDA/PPG │────►│ 1D-CNN Branch   │─────┤                                       ├────►│ Dynamic Robustness │
└─────────────┘     └─────────────────┘     └──► Private Periph Subspace (orthog) ──┘     └────────────────────┘
Advantages: Preserves unique sensor dynamics, aligns shared emotional manifold, balances multi-task gradients.
```

---

## 2. Modality Encoder Architectures & Physics

Biosignals originate from fundamentally different biological systems with heterogeneous temporal scales, channel topologies, and physical generation mechanisms:

### 2.1 Central Nervous System (CNS): EEG Branch
- **Physical Nature**: Microvolt-level ($\mu\text{V}$) postsynaptic potentials reflecting cortical pyramidal neuronal population activity.
- **Properties**: High temporal resolution (100–1000 Hz), non-Euclidean 3D scalp channel geometry, low signal-to-noise ratio (SNR), sensitive to ocular and myogenic noise ([`P0026`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0026.md), [`P0027`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0027.md)).
- **Verified Optimal Encoder Architectures in Literature**:
  1. **Compact Spatial-Temporal Convolutions (EEGNet / TSception)** ([`P0007`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0007.md), [`P0019`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0019.md)):
     - Layer 1 (Temporal Filtering): 1D Convolutions across time ($1 \times K_t$) learning frequency bandpass filters ($\theta, \alpha, \beta, \gamma$).
     - Layer 2 (Spatial Filtering): Depthwise Convolutions ($C \times 1$) across electrodes learning spatial projection filters.
     - Layer 3 (Separable Pointwise Convolutions): Compressing cross-channel representations with $< 5\text{k}$ parameters.
  2. **Dynamic Graph Convolutional Networks (DGCNN / RGNN)** ([`P0002`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0002.md), [`P0012`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0012.md)):
     - Modeling electrode connectivity via learnable adjacency matrices $\mathbf{A} \in \mathbb{R}^{C \times C}$:
       $$\mathbf{H}^{(l+1)} = \sigma\left(\mathbf{\tilde{D}}^{-\frac{1}{2}} \mathbf{\tilde{A}} \mathbf{\tilde{D}}^{-\frac{1}{2}} \mathbf{H}^{(l)} \mathbf{W}^{(l)}\right)$$
  3. **Bi-hemispheric Asymmetric Streams (BiHDM)** ([`P0005`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0005.md)):
     - Dual sub-networks for Left ($\mathcal{N}_L$) and Right ($\mathcal{N}_R$) hemispheres calculating differential activation $\mathbf{h}_{diff} = \mathbf{h}_L - \mathbf{h}_R$.

### 2.2 Autonomic Nervous System (ANS): Peripheral Biosignal Branches
- **Physical Nature**: Sympathetic (SNS) and Parasympathetic (PNS) nervous system innervation of cardiovascular, electrodermal, and respiratory systems.
- **Properties**: Slower temporal dynamics (seconds vs. milliseconds), lower channel count (1–4 sensors), large amplitude differences.
- **Sub-Modality Characteristics & Encoders**:
  1. **Electrocardiogram (ECG) / Photoplethysmography (PPG)**:
     - Captures heart rate variability (HRV), sympathetic-parasympathetic balance (LF/HF ratio, RMSSD).
     - Encoder: 1D-CNN with dilated convolutions or multi-resolution patch embedding capturing R-peak intervals and pulse morphology ([`P0001`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0001.md), [`P0015`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0015.md)).
  2. **Electrodermal Activity (EDA / GSR)**:
     - Decomposed into slow baseline tonic Skin Conductance Level (SCL, 0.05–0.2 Hz) and rapid phasic Skin Conductance Responses (SCR, 0.2–1.0 Hz) driven by sweat gland sympathetic activation.
     - Encoder: Dual-branch filter or multi-scale 1D convolutional smoothing network.
  3. **Respiration (RSP)**:
     - Measures breathing rate and depth (thoracic expansion). Slower deep breathing correlates with relaxation/positive valence; rapid irregular breathing correlates with high arousal/stress.

---

## 3. Mathematical Formalisms of Target Subsystems

---

### 3.1 Shared-Private Subspace Disentanglement Formulation

To prevent one dominant modality (e.g., EEG) from overpowering weaker peripheral streams (e.g., EDA) and to isolate sensor-specific artifacts from underlying emotional states, latent representations are decomposed into **Shared** ($\mathbf{s}_m$) and **Private** ($\mathbf{p}_m$) subspaces ([`P0003`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0003.md), MISA / DSN framework):

Let $M$ be the set of modalities ($m \in \{\text{EEG}, \text{ECG}, \text{EDA}, \dots\}$). For each input $\mathbf{x}_m$:
$$\mathbf{s}_m = E_{m}^{shared}(\mathbf{x}_m) \in \mathbb{R}^{d_s}, \quad \mathbf{p}_m = E_{m}^{private}(\mathbf{x}_m) \in \mathbb{R}^{d_p}$$

The learning objective consists of four joint terms:

```
                        ┌────────────────────────────────────────────────────────┐
                        │      Total Disentanglement Loss Formulation            │
                        │  L_rep = L_task + α L_sim + β L_diff + γ L_recon       │
                        └──────────────────────────┬─────────────────────────────┘
                                                   │
         ┌────────────────────────┬────────────────┴────────────────┬────────────────────────┐
         ▼                        ▼                                 ▼                        ▼
┌──────────────────┐    ┌──────────────────┐              ┌──────────────────┐     ┌──────────────────┐
│ Task Prediction  │    │ Similarity Loss  │              │ Difference Loss  │     │ Reconstruction   │
│     L_task       │    │     L_sim        │              │     L_diff       │     │     L_recon      │
├──────────────────┤    ├──────────────────┤              ├──────────────────┤     ├──────────────────┤
│ Task heads on    │    │ Minimizes MMD or │              │ Enforces soft    │     │ Decoders rebuild │
│ concatenated     │    │ CMD discrepancy  │              │ orthogonality    │     │ original x_m from│
│ [s_all, p_m]     │    │ between shared   │              │ between s_m and  │     │ (s_m, p_m)       │
│ representations  │    │ s_i and s_j      │              │ p_m subspaces    │     │                  │
└──────────────────┘    └──────────────────┘              └──────────────────┘     └──────────────────┘
```

1. **Similarity Loss ($\mathcal{L}_{sim}$)**:
   Forces shared representations from different modalities into a common distribution using Central Moment Discrepancy (CMD) or Maximum Mean Discrepancy (MMD):
   $$\mathcal{L}_{sim} = \sum_{i \neq j} \text{CMD}(\mathbf{S}_i, \mathbf{S}_j) = \sum_{i \neq j} \left( \frac{1}{|c_i - c_j|} \|\mathbb{E}(\mathbf{S}_i) - \mathbb{E}(\mathbf{S}_j)\|_2 + \sum_{k=2}^K \frac{1}{|c_i - c_j|^k} \|C_k(\mathbf{S}_i) - C_k(\mathbf{S}_j)\|_F \right)$$

2. **Difference Loss ($\mathcal{L}_{diff}$)**:
   Enforces orthogonality between shared and private subspaces of the same modality, preventing private sensor noise from contaminating the shared emotion manifold:
   $$\mathcal{L}_{diff} = \sum_{m \in M} \|\mathbf{S}_m^T \mathbf{P}_m\|_F^2$$

3. **Reconstruction Loss ($\mathcal{L}_{recon}$)**:
   Guarantees that $(\mathbf{s}_m, \mathbf{p}_m)$ retain complete modality information without trivial information collapse:
   $$\mathcal{L}_{recon} = \sum_{m \in M} \|\mathbf{x}_m - D_m(\mathbf{s}_m, \mathbf{p}_m)\|_2^2$$

---

### 3.2 Cross-Modal Attention & Temporal Alignment Formulation

To model directional cross-modal interactions between unaligned sampling rates (e.g., 128 Hz EEG vs. 4 Hz EDA), Cross-Modal Attention projects Query from target modality $m_1$ and Key/Value from source modality $m_2$ ([`P0003`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0003.md), MulT):

$$\mathbf{Q}_{m_1} = \mathbf{H}_{m_1} \mathbf{W}_Q, \quad \mathbf{K}_{m_2} = \mathbf{H}_{m_2} \mathbf{W}_K, \quad \mathbf{V}_{m_2} = \mathbf{H}_{m_2} \mathbf{W}_V$$
$$\mathbf{Z}_{m_1 \leftarrow m_2} = \text{Softmax}\left( \frac{\mathbf{Q}_{m_1} \mathbf{K}_{m_2}^T}{\sqrt{d_k}} \right) \mathbf{V}_{m_2}$$

- **Directional Physics**:
  - $\text{EEG} \leftarrow \text{EDA}$: Modulates cortical oscillation attention weights based on sympathetic sweat gland arousal spikes.
  - $\text{ECG} \leftarrow \text{EEG}$: Conditions heart-rate variability features on rapid frontal cortical cognitive appraisal changes.

---

### 3.3 Multi-Task Formulation & Dynamic Uncertainty Weighting

Emotions in biological organisms are multi-faceted ([`P0028`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0028.md), [`P0029`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0029.md)), spanning:
- Task 1: Continuous/Binary **Valence** (Pleasantness / Hedonic tone)
- Task 2: Continuous/Binary **Arousal** (Activation / Autonomic intensity)
- Task 3: Continuous/Binary **Dominance** (Control / Agency)
- Task 4: Discrete **Emotion Categories** (e.g. 3-class on SEED, 4-class on SEED-IV, 7-class on AMIGOS)

**Homoscedastic Aleatoric Uncertainty Loss Balancing** (Kendall et al. 2018):
When optimizing regression tasks ($\mathcal{L}_v, \mathcal{L}_a$) alongside classification tasks ($\mathcal{L}_c$), fixed loss weights $\lambda_i$ cause gradients of one task to dominate optimization. Deriving the joint loss from Gaussian and Softmax likelihoods with learnable observation noise parameters $\sigma_i$:

$$\mathcal{L}_{total}(W, \sigma_v, \sigma_a, \sigma_c) = \frac{1}{2\sigma_v^2}\mathcal{L}_v(W) + \frac{1}{2\sigma_a^2}\mathcal{L}_a(W) + \frac{1}{\sigma_c^2}\mathcal{L}_c(W) + \log \sigma_v + \log \sigma_a + \log \sigma_c$$

- **Automatic Gradient Dynamics**: If task $i$ has high label noise or high gradient scale, the network adaptively increases $\sigma_i$, attenuating $\frac{1}{2\sigma_i^2}\mathcal{L}_i$, while the regularizer $\log \sigma_i$ prevents unbounded divergence.

---

## 4. Cross-Subject Generalization & Missing-Modality Robustness

---

### 4.1 Cross-Subject Domain Alignment
- **Problem**: Inter-subject variance (skull thickness, electrode placement, baseline autonomic arousal) causes $>15–20\%$ accuracy drops between within-subject and cross-subject benchmarks ([`P0001`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0001.md), [`P0004`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0004.md), [`P0007`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0007.md), [`P0021`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0021.md), [`P0030`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0030.md)).
- **Mechanism**: Adversarial Domain Adaptation via Gradient Reversal Layer (GRL):
  $$\mathcal{L}_{adv} = \mathcal{L}_{task}(\hat{\mathbf{y}}, \mathbf{y}) - \lambda_{GRL} \mathcal{L}_{domain}(\hat{\mathbf{d}}, \mathbf{d})$$
  forces the shared encoder to learn features that maximize emotion discriminability while minimizing subject domain discriminability.

---

### 4.2 Missing-Modality Robustness & Dynamic Masking
- **Problem**: In wearable scenarios, electrodes or wristbands may disconnect, causing missing input streams at inference time ([`P0015`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0015.md), [`P0019`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0019.md)).
- **Mechanism**: Modality Dropout during training with residual cross-modal feature imputation. When modality $m$ is missing:
  $$\mathbf{h}_m = \mathbf{0}, \quad \text{Mask } \mathbf{m} \sim \text{Bernoulli}(1 - p_{drop})$$
  The shared-private decoder reconstructs the missing latent representation from the remaining present modalities via cross-modal attention routing.

---

## 5. Taxonomical Classification Matrix of Literature Base

| Paper ID | Architecture Paradigm | Modality Branches | Shared-Private / Disentanglement | Fusion Strategy | Multi-Task Setup | Generalization Protocol |
|---|---|---|---|---|---|---|
| [`P0001`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0001.md) | Multi-Branch Classical | EEG, ECG, GSR, Video | Monolithic / None | Early / Late Decision | Valence + Arousal (Single-task runs) | LOSO & 10-Fold CV |
| [`P0002`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0002.md) | GNN Spatial-Spectral | EEG (62 ch) | Node / Edge Regularized | Spatial Graph Convolution | Discrete Emotion (3/4-Class) | Subject-Dep & LOSO |
| [`P0003`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0003.md) | Bimodal Autoencoder | EEG + Eye Tracking | Shared Latent Bottleneck | Intermediate Latent Fusion | Discrete 3-Class | Subject-Dependent |
| [`P0004`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0004.md) | Deep Belief Network | EEG (62 ch) | Latent RBM Space | Sub-band Concatenation | Discrete 3-Class | Cross-Session & LOSO |
| [`P0005`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0005.md) | Bi-hemispheric Dual-Branch | EEG (Left / Right) | Discrepancy Subspace | Pairwise Subtraction Layer | 3-Class & Valence/Arousal | Subject-Dependent |
| [`P0006`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0006.md) | Multi-Scale Entropy | EEG, ECG, GSR | Multi-Scale Feature Bank | Early Feature Concatenation | Valence + Arousal | Subject-Dependent |
| [`P0007`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0007.md) | Lightweight KD-DANN | EEG (Teacher/Student) | Domain-Invariant Latent | Adversarial + Distillation | Emotion + Domain Classifier | LOSO Cross-Subject |
| [`P0008`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0008.md) | Partial Label Learning | EEG (62 ch) | Disambiguation Matrix | Candidate Probability Weighting | Multi-Candidate Disambiguation | Subject-Dep & LOSO |
| [`P0009`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0009.md) | SOTA Review | EEG + Peripheral | Taxonomy Review | Early, Intermediate, Late | Multi-Task & Single-Task | Dep vs. LOSO Review |
| [`P0010`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0010.md) | Neural Gas + Fuzzy XGB | EEG (32 ch) | Prototype Manifold | Topological Prototype Map | Binary Valence / Arousal | 10-Fold CV |
| [`P0011`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0011.md) | Spatial-Temporal RNN | EEG (62/32 ch) | Multidirectional State | Hierarchical Spatial-to-Temporal | 3-Class & Valence/Arousal | Subject-Dependent |
| [`P0012`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0012.md) | Dynamic Graph CNN | EEG (62 ch) | Learnable Graph Topology | Dynamic Graph Convolution | Discrete 3-Class | Subject-Dep & LOSO |
| [`P0013`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0013.md) | Phase Synchrony 2D-CNN | EEG (32 ch) | Multi-band PLV Matrix | 2D Tensor Stacking | Binary Valence / Arousal | Subject-Dependent |
| [`P0014`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0014.md) | Multi-Stream Deep Pipeline | EEG, ECG, GSR, Video | Unimodal Feature Trunks | Decision-Level ELM / SVM | Binary Valence / Arousal | Subject-Dependent |
| [`P0015`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0015.md) | Wearable Mobility HMM | EEG (14 ch), ECG, GSR | Multi-Sensor Branches | Early & Late HMM Fusion | 3-Class Stress Detection | Strict Outdoor LOSO |
| [`P0016`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0016.md) | Inter-Subject Correlation | EEG (32 ch) | Stimuli-Aligned Covariance | Maximized Synchrony Projection | Valence + Arousal Reg. | LOSO Cross-Subject |
| [`P0017`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0017.md) | Deep Echo State Reservoir | EEG (Raw waveforms) | High-Dim Non-linear Reservoir | Multi-Reservoir Concatenation | Binary Valence / Arousal | 10-Fold CV |
| [`P0018`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0018.md) | Bimodal Kalman Filter | EEG + Acoustic Music | Continuous Affect Trajectory | Kalman State Smoothing | Continuous V-A Time-Series | Continuous 10-Fold CV |
| [`P0019`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0019.md) | Channel-Pruned Wearable | EEG (4–14 ch) | Sparse Spatial Subspace | Channel Concatenation | Binary Valence / Arousal | Subject-Dep & LOSO |
| [`P0020`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0020.md) | Sensor Configuration SCANet | EEG (Variable Montages) | Coordinate-Invariant Surface | 3D Spatial Spline Embedding | Cross-Montage Emotion | Cross-Dataset Transfer |
| [`P0021`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0021.md) | Transfer Support Vector Machine | 2-ch EEG | RKHS Domain Invariance | MMD Regularization Kernel | Sleep / Vigilance Binary | Cross-Subject LOSO |
| [`P0022`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0022.md) | Spatial Microstates Clustering | 64-ch Scalp EEG | Sub-second Quasi-stable States | Global Field Power Peaks | Positive vs. Negative Valence | Subject-Independent |
| [`P0023`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0023.md) | Foundation Transformer Model | EEG (64 ch) + fMRI | Cross-Modal Latent Manifold | Cross-Modal Attention + HRF | 116 ROI BOLD Regression | LOSO Cross-Subject |
| [`P0024`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0024.md) | Structural Equation Model | Psychometric Cohort | Metric-Invariant Factors | Multi-Group SEM Invariance | 4 Regulation Strategies | Cross-Population |
| [`P0025`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0025.md) | 2025 Deep Learning Survey | Multimodal Biosignals | Survey of Architectures | GNN vs Transformer vs SSL | Multi-Task Clinical/Affect | Within vs LOSO Audit |
| [`P0026`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0026.md) | Wavelet-EMD Time-Frequency | Single-channel EEG | Time-Frequency Planes | Wavelet Coefficient Reconstruction | ERP Denoising / SNR | Monte Carlo Simulation |
| [`P0027`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0027.md) | Standardized Referencing (REST)| 64-ch Scalp EEG | Reference-Free Surface | Lead-Field Matrix Inverse | Spatial Potential Fidelity | Physics-Based Solution |
| [`P0028`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0028.md) | Hierarchical Linear Model | Longitudinal EMA | Emotion Granularity Structure | Multi-Emotion Covariance | Discrete Emotion NED | Prospective Prediction |
| [`P0029`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0029.md) | Semantic Manifold Analysis | Video Responses | High-Dim Semantic Space | 27 Continuous Gradients | Multi-Dimensional Semantic | Split-Sample CV |
| [`P0030`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0030.md) | 2024 Methodological Review | Multimodal Biosignals | Audit of Deep Models | Early, Tensor, Cross-Attention | Multi-Task vs Single-Task | Data Leakage Audit |

---

## 6. Synthesis Summary & Transition to Phase P3

1. **Established Scientific Facts [FACT]**:
   - Monolithic concatenation fails to account for sampling rate and amplitude asymmetry between EEG and peripheral streams ([`P0001`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0001.md), [`P0030`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0030.md)).
   - Shared-Private Subspace Disentanglement with similarity and difference losses preserves modality-specific features while removing redundancy ([`P0003`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0003.md)).
   - Multi-Task learning without adaptive loss balancing leads to negative transfer and gradient collapse when combining continuous regression (Valence/Arousal) with discrete classification ([`P0008`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0008.md), [`P0028`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0028.md)).
2. **Transition to P3**:
   - Proceed directly to **Phase P3: Research Gap Analysis** to formulate precise, evidence-backed literature gaps.
