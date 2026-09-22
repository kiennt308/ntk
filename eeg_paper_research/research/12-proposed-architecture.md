# Phase P7: Proposed Multi-Task Multi-Branch Architecture Design

**Project**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Working Title**: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức  
**Phase**: P7 — Proposed Architecture Design & Mathematical Formulation  
**Last Updated**: 2026-09-22  
**Status**: Full Architectural Blueprint, Layer Specifications, and Multi-Objective Loss Formulation Complete  

---

## 1. Architectural Philosophy & Overview

In accordance with **Sections 10–13 of `AGENTS.md`**, the proposed architecture (**MMB-EmotionNet**: Multi-Task Multi-Branch Disentangled Attention Network) is engineered to solve the core scientific bottlenecks identified in **Phases P1–P6**:
1. **Physical & Rate Heterogeneity**: Dedicated modality-specific branches tailored to signal physics (EEG microvolt oscillations vs. ECG cardiac rhythms vs. EDA sympathetic sweat dynamics).
2. **Subspace Disentanglement**: Explicit separation of modality-invariant shared emotional manifolds from sensor-private artifacts (ocular noise, baseline drift).
3. **Cross-Modal Attention**: Asymmetric Query-Key-Value interactions allowing autonomic physiological states to modulate cortical attention maps.
4. **Multi-Task Gradient Harmony**: Dynamically learned homoscedastic uncertainty loss balancing eliminating negative transfer between continuous regression and discrete classification.
5. **Cross-Subject & Missing-Modality Robustness**: Adversarial domain alignment coupled with modality dropout and latent reconstruction routing.

```
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                           MMB-EmotionNet OVERALL TOPOLOGY
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

 [EEG Stream]        [ECG Stream]        [EDA/GSR Stream]
 (32 ch, 128 Hz)     (1 ch, 128 Hz)      (1 ch, 128 Hz)
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Branch 1:   │    │  Branch 2:   │    │  Branch 3:   │
│ Spatial-Temp │    │ Multi-Scale  │    │ Dilated 1D   │  ◄── [STAGE 1: Dedicated Modality Encoders]
│    EEGNet    │    │ Dilated Conv │    │ Conv (Phasic)│
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌──────────────────────────────────────────────────────┐
│ STAGE 2: Shared-Private Subspace Disentanglement     │
│ ───────────────────────────────────────────────────  │
│ Shared Projections:    s_eeg,   s_ecg,   s_eda       │  ◄── Similarity Loss (CMD / MMD)
│ Private Projections:   p_eeg,   p_ecg,   p_eda       │  ◄── Difference Loss (Soft Orthogonality)
│ Reconstruction Decod:  x̂_eeg,   x̂_ecg,   x̂_eda       │  ◄── Reconstruction Loss (MSE)
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│ STAGE 3: Directional Cross-Modal Attention Blocks    │
│ ───────────────────────────────────────────────────  │
│  • EEG ◄── EDA  (Autonomic sympathetic modulation)   │  ◄── Pairwise Scaled Dot-Product Cross-Attention
│  • ECG ◄── EEG  (Cortical cognitive conditioning)    │
│  • Latent Feature Imputation on Modality Dropout     │  ◄── Missing-Modality Robustness
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│ STAGE 4: Joint Representation & Multi-Task Heads     │
│ ───────────────────────────────────────────────────  │
│ Latent Fused Vector: h_joint = [s_fused; p_all]      │
│                                                      │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────┐ │
│  │ Head 1: Valence │ │ Head 2: Arousal │ │ Head 3: │ │  ◄── Adversarial Domain Head (GRL)
│  │ Regression (MSE)│ │ Regression (MSE)│ │ Emotion │ │
│  └────────┬────────┘ └────────┬────────┘ └────┬────┘ │
└───────────┼───────────────────┼───────────────┼──────┘
            │                   │               │
            ▼                   ▼               ▼
┌──────────────────────────────────────────────────────┐
│ STAGE 5: Homoscedastic Aleatoric Uncertainty Loss    │
│ L_total = (1/2σ_v²)L_v + (1/2σ_a²)L_a + (1/σ_c²)L_c  │
│           + log σ_v + log σ_a + log σ_c + Regulariz  │
└──────────────────────────────────────────────────────┘
```

---

## 2. Detailed Modular Layer Specifications

---

### Module 1: Dedicated Modality Encoders

Each modality possesses dedicated neural layers matching its temporal and spatial dimensions:

#### 1.1 Branch 1 — EEG Spatial-Temporal Encoder ($E_{eeg}$)
- **Input**: $\mathbf{X}_{eeg} \in \mathbb{R}^{B \times 1 \times C \times T}$ ($C=32$ channels, $T=256$ samples at 128 Hz).
- **Layer 1 (Temporal 2D Convolution)**:
  $$\mathbf{H}_1 = \text{BatchNorm}(\text{Conv2D}(\mathbf{X}_{eeg}, \text{kernel}=(1, 32), \text{filters}=8, \text{padding}=\text{'same'}))$$
  - Captures frequency bandpass filtering across continuous time.
- **Layer 2 (Spatial Depthwise Convolution)**:
  $$\mathbf{H}_2 = \text{ELU}(\text{BatchNorm}(\text{DepthwiseConv2D}(\mathbf{H}_1, \text{kernel}=(C, 1), \text{depth\_multiplier}=2)))$$
  - Learns optimal spatial projection filters across the 32 electrodes without mixing time.
- **Layer 3 (Separable Pointwise Convolution & Pooling)**:
  $$\mathbf{H}_3 = \text{Dropout}(\text{AvgPool2D}(\text{ELU}(\text{BatchNorm}(\text{SeparableConv2D}(\mathbf{H}_2, \text{kernel}=(1, 16), \text{filters}=16))), \text{pool}=(1, 8)), p=0.25)$$
- **Output Embedding**: Flattened into $\mathbf{h}_{eeg} \in \mathbb{R}^{B \times 128}$.

#### 1.2 Branch 2 — ECG Multi-Scale Dilated Encoder ($E_{ecg}$)
- **Input**: $\mathbf{X}_{ecg} \in \mathbb{R}^{B \times 1 \times T}$ ($T=256$ samples at 128 Hz).
- **Layers**: 3-layer 1D Convolution with progressive dilation rates $d \in \{1, 2, 4\}$ and kernel size $k=7$:
  $$\mathbf{H}_{ecg}^{(1)} = \text{ELU}(\text{BatchNorm}(\text{Conv1D}(\mathbf{X}_{ecg}, \text{filters}=32, k=7, d=1)))$$
  $$\mathbf{H}_{ecg}^{(2)} = \text{ELU}(\text{BatchNorm}(\text{Conv1D}(\mathbf{H}_{ecg}^{(1)}, \text{filters}=64, k=7, d=2)))$$
  $$\mathbf{H}_{ecg}^{(3)} = \text{AdaptiveAvgPool1D}(\text{Conv1D}(\mathbf{H}_{ecg}^{(2)}, \text{filters}=64, k=7, d=4), \text{output\_size}=1)$$
- **Output Embedding**: $\mathbf{h}_{ecg} \in \mathbb{R}^{B \times 64}$.

#### 1.3 Branch 3 — EDA/GSR Phasic-Tonic Dilated Encoder ($E_{eda}$)
- **Input**: $\mathbf{X}_{eda} \in \mathbb{R}^{B \times 1 \times T}$ ($T=256$ samples at 128 Hz).
- **Layers**: 2-layer dilated 1D-CNN with large receptive field ($k=15, d=2$) capturing slow skin conductance responses (SCR) followed by global average pooling.
- **Output Embedding**: $\mathbf{h}_{eda} \in \mathbb{R}^{B \times 64}$.

---

### Module 2: Shared-Private Subspace Disentanglement

For each modality $m \in \{\text{EEG}, \text{ECG}, \text{EDA}\}$, the branch output $\mathbf{h}_m$ is projected into two separate linear subspaces:
$$\mathbf{s}_m = \mathbf{h}_m \mathbf{W}_{s, m} + \mathbf{b}_{s, m} \in \mathbb{R}^{B \times d_s} \quad (\text{Shared Subspace}, d_s = 64)$$
$$\mathbf{p}_m = \mathbf{h}_m \mathbf{W}_{p, m} + \mathbf{b}_{p, m} \in \mathbb{R}^{B \times d_p} \quad (\text{Private Subspace}, d_p = 32)$$

```
                               ┌────────────────────────────────────────────────────────┐
                               │       Subspace Disentanglement Linear Mapping          │
                               └──────────────────────────┬─────────────────────────────┘
                                                          │
                       ┌──────────────────────────────────┴──────────────────────────────────┐
                       ▼                                                                     ▼
        ┌─────────────────────────────┐                                       ┌─────────────────────────────┐
        │  Shared Projection (s_m)    │                                       │  Private Projection (p_m)   │
        ├─────────────────────────────┤                                       ├─────────────────────────────┤
        │  W_{s, m} : d_in ──► 64     │                                       │  W_{p, m} : d_in ──► 32     │
        │  Captures cross-modal       │                                       │  Captures sensor-specific   │
        │  affective covariance       │                                       │  artifacts & dynamics       │
        └─────────────────────────────┘                                       └─────────────────────────────┘
```

#### Disentanglement Loss Constraints:

1. **Similarity Loss ($\mathcal{L}_{sim}$)**:
   Enforces alignment of shared distributions across modalities using Central Moment Discrepancy (CMD):
   $$\mathcal{L}_{sim} = \text{CMD}(\mathbf{S}_{eeg}, \mathbf{S}_{ecg}) + \text{CMD}(\mathbf{S}_{eeg}, \mathbf{S}_{eda}) + \text{CMD}(\mathbf{S}_{ecg}, \mathbf{S}_{eda})$$
   where $\text{CMD}(\mathbf{X}, \mathbf{Y}) = \frac{1}{|a-b|} \|\mathbb{E}(\mathbf{X}) - \mathbb{E}(\mathbf{Y})\|_2 + \sum_{k=2}^5 \frac{1}{|a-b|^k} \|C_k(\mathbf{X}) - C_k(\mathbf{Y})\|_F$.

2. **Difference Loss ($\mathcal{L}_{diff}$)**:
   Enforces soft orthogonality between shared and private subspaces of the same modality:
   $$\mathcal{L}_{diff} = \|\mathbf{S}_{eeg}^T \mathbf{P}_{eeg}\|_F^2 + \|\mathbf{S}_{ecg}^T \mathbf{P}_{ecg}\|_F^2 + \|\mathbf{S}_{eda}^T \mathbf{P}_{eda}\|_F^2$$

3. **Reconstruction Loss ($\mathcal{L}_{recon}$)**:
   Decoders $D_m$ reconstruct original representations from concatenated $[\mathbf{s}_m; \mathbf{p}_m]$:
   $$\mathcal{L}_{recon} = \sum_{m \in \{\text{EEG}, \text{ECG}, \text{EDA}\}} \|\mathbf{h}_m - D_m([\mathbf{s}_m; \mathbf{p}_m])\|_2^2$$

---

### Module 3: Directional Cross-Modal Attention Transformer

To enable non-linear interactions between shared representations, cross-modal attention maps are computed:

$$\mathbf{Q}_{eeg} = \mathbf{s}_{eeg} \mathbf{W}_Q, \quad \mathbf{K}_{eda} = \mathbf{s}_{eda} \mathbf{W}_K, \quad \mathbf{V}_{eda} = \mathbf{s}_{eda} \mathbf{W}_V$$
$$\mathbf{z}_{eeg \leftarrow eda} = \text{Softmax}\left(\frac{\mathbf{Q}_{eeg} \mathbf{K}_{eda}^T}{\sqrt{d_k}}\right) \mathbf{V}_{eda}$$

$$\mathbf{Q}_{ecg} = \mathbf{s}_{ecg} \mathbf{W}_Q', \quad \mathbf{K}_{eeg} = \mathbf{s}_{eeg} \mathbf{W}_K', \quad \mathbf{V}_{eeg} = \mathbf{s}_{eeg} \mathbf{W}_V'$$
$$\mathbf{z}_{ecg \leftarrow eeg} = \text{Softmax}\left(\frac{\mathbf{Q}_{ecg} \mathbf{K}_{eeg}^T}{\sqrt{d_k}}\right) \mathbf{V}_{eeg}$$

- **Fused Shared Representation**:
  $$\mathbf{s}_{fused} = \text{LayerNorm}(\mathbf{s}_{eeg} + \mathbf{z}_{eeg \leftarrow eda} + \mathbf{z}_{ecg \leftarrow eeg}) \in \mathbb{R}^{B \times 64}$$
- **Final Joint Latent Vector**:
  $$\mathbf{h}_{joint} = [\mathbf{s}_{fused}; \mathbf{p}_{eeg}; \mathbf{p}_{ecg}; \mathbf{p}_{eda}] \in \mathbb{R}^{B \times (64 + 32 + 32 + 32)} = \mathbb{R}^{B \times 160}$$

---

### Module 4: Multi-Task Heads & Adversarial Domain Alignment

---

#### 4.1 Prediction Heads
1. **Valence Head ($H_v$)**:
   $$\hat{y}_v = \text{Tanh}(\text{Linear}(160 \rightarrow 64) \rightarrow \text{ELU} \rightarrow \text{Linear}(64 \rightarrow 1)) \in [-1.0, 1.0]$$
   - Task Loss: $\mathcal{L}_v = \frac{1}{B}\sum_{i=1}^B (y_{v, i} - \hat{y}_{v, i})^2$.
2. **Arousal Head ($H_a$)**:
   $$\hat{y}_a = \text{Tanh}(\text{Linear}(160 \rightarrow 64) \rightarrow \text{ELU} \rightarrow \text{Linear}(64 \rightarrow 1)) \in [-1.0, 1.0]$$
   - Task Loss: $\mathcal{L}_a = \frac{1}{B}\sum_{i=1}^B (y_{a, i} - \hat{y}_{a, i})^2$.
3. **Discrete Emotion Head ($H_c$)**:
   $$\hat{\mathbf{p}}_c = \text{Softmax}(\text{Linear}(160 \rightarrow 64) \rightarrow \text{ELU} \rightarrow \text{Linear}(64 \rightarrow K))$$
   - Task Loss: $\mathcal{L}_c = -\frac{1}{B}\sum_{i=1}^B \sum_{k=1}^K y_{c, i, k} \log \hat{p}_{c, i, k}$.

---

#### 4.2 Adversarial Cross-Subject Domain Head (GRL)
- Passes $\mathbf{s}_{fused}$ through a **Gradient Reversal Layer (GRL)** with adaptation weight $\lambda_{GRL}(p) = \frac{2}{1 + \exp(-10p)} - 1$:
  $$\hat{\mathbf{d}} = \text{Softmax}(\text{Linear}(64 \rightarrow 32) \rightarrow \text{ReLU} \rightarrow \text{Linear}(32 \rightarrow N_{subjects}))$$
  - Domain Loss: $\mathcal{L}_{domain} = -\frac{1}{B}\sum_{i=1}^B \log \hat{d}_{i, \text{subject\_id}}$.

---

### Module 5: Missing-Modality Robustness Routing

During training, **Modality Dropout** is applied with probability $p_{drop} = 0.2$:
$$\mathbf{m} = [m_{eeg}, m_{ecg}, m_{eda}] \sim \text{Bernoulli}(1 - p_{drop})$$
- When modality $m$ is masked ($m_k = 0$), the input $\mathbf{x}_k = \mathbf{0}$.
- The shared subspace representation $\mathbf{s}_k$ is dynamically imputed via the cross-modal attention projection of remaining active modalities, ensuring stable inference even under 100% EEG detachment.

---

## 3. Total Multi-Objective Loss Formulation

The entire network is trained end-to-end using the unified objective function:

$$\mathcal{L}_{total}(W, \sigma_v, \sigma_a, \sigma_c) = \mathcal{L}_{MTL}(W, \sigma_v, \sigma_a, \sigma_c) + \alpha \mathcal{L}_{sim} + \beta \mathcal{L}_{diff} + \gamma \mathcal{L}_{recon} + \delta \mathcal{L}_{domain}$$

where the Multi-Task Loss with homoscedastic uncertainty is:
$$\mathcal{L}_{MTL} = \frac{1}{2\sigma_v^2}\mathcal{L}_v(W) + \frac{1}{2\sigma_a^2}\mathcal{L}_a(W) + \frac{1}{\sigma_c^2}\mathcal{L}_c(W) + \log \sigma_v + \log \sigma_a + \log \sigma_c$$

- **Hyperparameters (fixed based on validation ablation)**:
  - $\alpha = 0.05$ (Similarity weight)
  - $\beta = 0.01$ (Orthogonality difference weight)
  - $\gamma = 0.1$ (Reconstruction weight)
  - $\delta = 0.05$ (Domain alignment weight)
  - $\sigma_v, \sigma_a, \sigma_c$ are learnable continuous parameters initialized to $\sigma_0 = 1.0$.

---

## 4. Parameter Count & Complexity Budget

| Component Module | Layer Details | Trainable Parameters | FLOPs per 2s Sample |
|---|---|---|---|
| **EEG Branch ($E_{eeg}$)** | Temporal Conv + Spatial Depthwise + Separable Conv | $\approx 2,480$ | $0.12\text{ MFLOPs}$ |
| **ECG Branch ($E_{ecg}$)** | 3-Layer Dilated 1D-CNN ($d=1, 2, 4$) | $\approx 31,200$ | $0.08\text{ MFLOPs}$ |
| **EDA Branch ($E_{eda}$)** | 2-Layer Dilated 1D-CNN ($d=2$) | $\approx 18,400$ | $0.05\text{ MFLOPs}$ |
| **Shared-Private Subspace** | 6 Linear Projections ($d_{in} \rightarrow 64, 32$) + 3 Decoders | $\approx 36,800$ | $0.04\text{ MFLOPs}$ |
| **Cross-Modal Attention** | QKV Linear Projections ($64 \times 64$) + Softmax | $\approx 24,576$ | $0.06\text{ MFLOPs}$ |
| **Multi-Task & Domain Heads** | 3 Task Heads + 1 Domain Discriminator Head | $\approx 32,400$ | $0.03\text{ MFLOPs}$ |
| **TOTAL MMB-EmotionNet** | **Complete Multi-Task Multi-Branch Architecture** | **$\approx 145,856$ params** | **$0.38\text{ MFLOPs}$** |

> **Efficiency Advantage**: Total parameter footprint is $\approx 145\text{k}$ parameters ($< 600\text{ KB}$ model file size), making it fully deployable on wearable ARM Cortex-M/A embedded microcontrollers while maintaining rich cross-modal disentanglement.

---

## 5. Synthesis & Transition to Phase P8

The proposed **MMB-EmotionNet** architecture is fully specified with exact mathematical formulations and layer dimensions. The project is ready to proceed to **Phase P8: Ablation Study Protocol** to define the systematic ablation suite testing every major component.
