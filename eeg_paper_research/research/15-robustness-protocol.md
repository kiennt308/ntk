# Phase P10: Missing-Modality Robustness & Stress-Testing Protocol

**Project**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Working Title**: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức  
**Phase**: P10 — Missing-Modality Robustness, Noise Perturbation, and Computational Efficiency Stress-Testing  
**Last Updated**: 2026-09-22  
**Status**: Comprehensive Robustness Protocol Formalized & Ready for Implementation  

---

## 1. Executive Summary & Research Scope

In accordance with **Sections 14, 15, and 18 of `AGENTS.md`**, this document formalizes the stress-testing and robustness evaluation protocol for the proposed **MMB-EmotionNet** architecture.

In real-world ubiquitous affective computing and healthcare applications, wearable biosensors suffer from frequent signal corruption, electrode detachment, motion artifacts, battery depletion, or wireless packet loss ([P0004], [P0012], [P0020]). Standard multimodal architectures catastrophically fail when one or more input streams are missing or corrupted.

This protocol operationalizes **Research Question 6 (RQ6)** and evaluates **Hypothesis 6 ($H_6$)**:
- **RQ6**: *"How robust is the proposed multi-branch shared-private architecture under complete modality dropout, sensor noise corruption, and severe computational constraints compared to monolithic and standard fusion models?"*
- **Hypothesis $H_6$**: *"MMB-EmotionNet with shared-private latent imputation and training-time modality dropout maintains statistically significantly higher Macro-F1 under single and multi-modality loss ($d \ge 0.5$, $p < 0.01$) and maintains $<15\text{ ms}$ inference latency on edge compute devices."*

```
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                              5-DIMENSIONAL ROBUSTNESS TAXONOMY
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

  1. Complete Modality Loss       2. Partial Channel Dropout      3. Noise & Artifact Injection
  ┌───────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐
  │ • Zero-shot Missing EEG   │   │ • Random Channel Drop     │   │ • Gaussian Noise (SNR)    │
  │ • Zero-shot Missing ECG   │   │ • Frontal Electrode Loss  │   │ • Motion / EMG Bursts     │
  │ • Zero-shot Missing EDA   │   │ • Dual Sensor Detach      │   │ • Low-Freq Baseline Drift │
  │ • Dual Modality Loss      │   │                           │   │ • 50/60 Hz Powerline Hum  │
  └───────────────────────────┘   └───────────────────────────┘   └───────────────────────────┘
                │                               │                               │
                ▼                               ▼                               ▼
  4. Latent Imputation & Routing  5. Computational & Latency Profiling
  ┌───────────────────────────┐   ┌───────────────────────────┐
  │ • Shared Subspace Routing │   │ • FLOPs per 2s window     │
  │ • Cross-Attention Inpaint │   │ • Peak VRAM / Memory      │
  │ • Learnable Default Token │   │ • Server GPU vs Edge CPU  │
  │ • Zero-Padding Baseline   │   │ • Jetson / Mobile Latency │
  └───────────────────────────┘   └───────────────────────────┘
```

---

## 2. Mathematical Formulations of Degradation & Imputation

### 2.1 Modality Masking & Stochastic Training-Time Dropout

Let $\mathcal{M} = \{m_1, m_2, m_3\} = \{\text{EEG}, \text{ECG}, \text{EDA}\}$ denote the set of biosignal modalities.
During training, a stochastic modality presence mask $\mathbf{r} = [r_{\text{eeg}}, r_{\text{ecg}}, r_{\text{eda}}] \in \{0, 1\}^3$ is sampled from a Bernoulli distribution with retention probability $(1 - p_{\text{drop}})$:
$$r_m \sim \text{Bernoulli}(1 - p_{\text{drop}}), \quad \text{s.t.} \quad \sum_{m \in \mathcal{M}} r_m \ge 1$$
where at least one modality is guaranteed to remain active in every training minibatch.

### 2.2 Latent Subspace Reconstruction & Cross-Modal Imputation

When modality $m$ is missing ($r_m = 0$), its input is replaced by a learnable neutral prior token $\mathbf{e}_m^{\text{null}} \in \mathbb{R}^{d_m}$.
The missing private and shared latent representations are imputed via the **Cross-Modal Attention Inpainting Module**:

1. **Available Modality Projection**:
   For all active modalities $j \in \{k \in \mathcal{M} \mid r_k = 1\}$, extract shared projections $\mathbf{s}_j = E_{\text{shared}}^{(j)}(\mathbf{h}_j)$.
2. **Imputed Shared Representation**:
   $$\hat{\mathbf{s}}_m = \sum_{j \neq m, r_j = 1} \text{Softmax}\left(\frac{\mathbf{Q}_m^{\text{impute}} (\mathbf{K}_j^{\text{impute}})^\top}{\sqrt{d_k}}\right) \mathbf{V}_j^{\text{impute}}$$
3. **Private Latent Zero-Gating**:
   Since sensor-specific private artifacts cannot be inferred from other modalities, private embeddings are clamped to zero: $\mathbf{p}_m = \mathbf{0}$.
4. **Imputation Consistency Loss ($\mathcal{L}_{\text{impute}}$)**:
   During multi-modal complete training passes, the imputation projector is supervised to reconstruct the true shared representation:
   $$\mathcal{L}_{\text{impute}} = \sum_{m \in \mathcal{M}} \|\hat{\mathbf{s}}_m - \mathbf{s}_m\|_2^2$$

---

### 2.3 Sensor Noise & Artifact Perturbation Models

To evaluate robustness against degradation encountered in ambulatory recordings, inputs $\mathbf{X}_m(t)$ are perturbed by four distinct noise regimes:

1. **Additive Gaussian White Noise (AGWN)**:
   $$\tilde{\mathbf{X}}_m(t) = \mathbf{X}_m(t) + \mathbf{\eta}(t), \quad \mathbf{\eta} \sim \mathcal{N}\left(0, \frac{\sigma_{\mathbf{X}_m}^2}{10^{\text{SNR}_{\text{dB}}/10}}\right)$$
   evaluated across $\text{SNR} \in \{20\text{ dB}, 10\text{ dB}, 5\text{ dB}, 0\text{ dB}, -5\text{ dB}\}$.
2. **Electrode Motion & EMG Burst Artifacts**:
   $$\tilde{\mathbf{X}}_{\text{eeg}}(t) = \mathbf{X}_{\text{eeg}}(t) + \alpha_{\text{EMG}} \cdot \mathbf{N}_{\text{EMG}}(t)$$
   where $\mathbf{N}_{\text{EMG}}$ represents high-frequency bandpassed noise ($30–100\text{ Hz}$) occurring in stochastic $0.5\text{s}$ bursts at Signal-to-Artifact Ratio $\text{SAR} \in \{10\text{ dB}, 0\text{ dB}\}$.
3. **Low-Frequency Baseline Drift (Respiration & Sweating Artifact)**:
   $$\tilde{\mathbf{X}}_m(t) = \mathbf{X}_m(t) + A_{\text{drift}} \sin(2\pi f_{\text{drift}} t + \phi), \quad f_{\text{drift}} \in [0.05, 0.2]\text{ Hz}$$
4. **Powerline Interference**:
   $$\tilde{\mathbf{X}}_m(t) = \mathbf{X}_m(t) + A_{50} \sin(2\pi \cdot 50 \cdot t)$$

---

## 3. Robustness Experiment Suite (EXP-ROB-01 through EXP-ROB-08)

```
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                               ROBUSTNESS EXPERIMENT SUITE MATRIX
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
ID          Stress Dimension      Target Scenario          Evaluated Modalities      Imputation / Defense
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────
EXP-ROB-01  Single Dropout        Zero-Shot Modality Loss  Missing EEG / ECG / EDA   Cross-Modal Latent Inpainting
EXP-ROB-02  Dual Dropout          Extreme Sensor Depletion Only EEG / ECG / EDA Left Zero-Gated Shared Routing
EXP-ROB-03  Dropout Probability   Training-Time Regulariz  $p_{\text{drop}} \in [0.0, 0.5]$ Dynamic Mask Scheduling
EXP-ROB-04  Noise Perturbation    Additive Gaussian Noise  SNR = 20, 10, 5, 0, -5 dB Shared Subspace Denoising
EXP-ROB-05  Electrode Artifacts   Motion & EMG Bursts      High-Freq Burst on EEG    Spatial Depthwise Filtering
EXP-ROB-06  Baseline Drift        Slow Sensor Wander       $0.1\text{ Hz}$ Drift on EDA/ECG Soft Orthogonality Filtering
EXP-ROB-07  Channel Dropout       Electrode Detachment     $25\%, 50\%, 75\%$ EEG Ch  Spherical Spline Interp
EXP-ROB-08  Hardware Efficiency   Edge & Server Profiling  Full Architecture         Latency, FLOPs, Memory Audit
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
```

---

### EXP-ROB-01: Zero-Shot Single Modality Dropout

- **Objective**: Quantify model resilience when exactly one physiological sensor fails or is disconnected at test time.
- **Test Conditions**:
  1. **Condition A (Missing EEG)**: Inputs: $\mathbf{X}_{\text{eeg}} = \text{Null}$, Active: ECG + EDA.
  2. **Condition B (Missing ECG)**: Inputs: $\mathbf{X}_{\text{ecg}} = \text{Null}$, Active: EEG + EDA.
  3. **Condition C (Missing EDA)**: Inputs: $\mathbf{X}_{\text{eda}} = \text{Null}$, Active: EEG + ECG.
- **Architectures Compared**:
  - Monolithic Early Fusion CNN (zero-padded).
  - Late Fusion Ensemble (sub-model average).
  - MMB-EmotionNet (Vanilla without imputation).
  - MMB-EmotionNet (Full + Cross-Modal Latent Inpainting).
- **Primary Metric**: Modality Retention Ratio $\rho_m = \frac{\text{Macro-F1}_{\text{missing } m}}{\text{Macro-F1}_{\text{full}}}$.

---

### EXP-ROB-02: Dual Modality Dropout (Extreme Sensor Depletion)

- **Objective**: Stress-test extreme edge scenarios where two out of three modalities fail, leaving only a single active sensor stream.
- **Test Conditions**:
  1. **EEG Only** (Missing ECG + EDA).
  2. **ECG Only** (Missing EEG + EDA).
  3. **EDA Only** (Missing EEG + ECG).
- **Expected Outcome**: MMB-EmotionNet recovers $>75\%$ of full multimodal performance when only EEG is preserved, and $>60\%$ when only peripheral signals (ECG or EDA) are preserved.

---

### EXP-ROB-03: Training-Time Modality Dropout Sensitivity ($p_{\text{drop}}$)

- **Objective**: Determine the optimal training-time modality dropout probability $p_{\text{drop}} \in \{0.0, 0.1, 0.2, 0.3, 0.4, 0.5\}$ that maximizes missing-modality robustness without degrading clean multimodal accuracy.
- **Protocol**: Train 6 separate MMB-EmotionNet instances with varying $p_{\text{drop}}$ values under unified hyperparameters (AdamW, 100 epochs, 5 seeds).
- **Evaluation**: Evaluate each instance across all 7 possible modality test combinations ($2^3 - 1$).
- **Deliverable**: Robustness vs. Peak Accuracy Pareto frontier curve.

---

### EXP-ROB-04: Gaussian Noise Degradation Curve

- **Objective**: Quantify affective classification decay under increasing sensor transmission noise.
- **Noise Sweep**: Gaussian White Noise injected into all channels at $\text{SNR} \in \{20\text{ dB}, 10\text{ dB}, 5\text{ dB}, 0\text{ dB}, -5\text{ dB}\}$.
- **Evaluation Metric**: Area Under Degradation Curve ($\text{AUDC}_{\text{SNR}}$) and SNR Breakpoint ($\text{SNR}_{50\%}$ where Macro-F1 drops below $50\%$).

---

### EXP-ROB-05: Real-World Motion & EMG Artifact Burst Stress-Test

- **Objective**: Benchmark robustness against sudden non-stationary physiological artifacts (facial grimacing, swallowing, eye squints).
- **Perturbation**: Inject high-frequency EMG bursts ($30–100\text{ Hz}$) covering $20\%$ of total trial duration into frontal EEG channels (Fp1, Fp2, AF3, AF4, F7, F8).
- **Hypothesis**: The dedicated spatial depthwise convolution in Branch 1 combined with private subspace projection filters out EMG bursts, preserving $>90\%$ of clean Macro-F1.

---

### EXP-ROB-06: Autonomic Sensor Baseline Drift Stress-Test

- **Objective**: Measure stability against slow sweating and electrode gel drying on peripheral EDA and ECG sensors.
- **Perturbation**: Inject low-frequency sinusoidal wander ($0.1\text{ Hz}$, amplitude equal to $2\times$ signal standard deviation) into EDA and ECG channels.
- **Expected Outcome**: MMB-EmotionNet private subspace encoder absorbs drift energy, leaving shared emotional embeddings $\mathbf{s}_{\text{ecg}}, \mathbf{s}_{\text{eda}}$ unaffected.

---

### EXP-ROB-07: Random Electrode Detachment Stress-Test

- **Objective**: Measure degradation under progressive EEG channel loss ($25\% \rightarrow 50\% \rightarrow 75\%$ random electrode disconnection).
- **Interpolation Defense**: Evaluate Spherical Spline Reconstruction vs. Zero Masking under varying channel loss percentages.

---

### EXP-ROB-08: Computational Complexity & Real-Time Edge Profiling

- **Objective**: Formally audit computational requirements, parameter efficiency, memory footprint, and inference latency across diverse deployment targets.
- **Hardware Benchmarks**:
  1. **Server GPU**: NVIDIA RTX 4090 / A100 (TensorRT & PyTorch FP32/FP16).
  2. **Edge GPU**: NVIDIA Jetson Orin Nano / Xavier NX.
  3. **Consumer CPU**: Intel Core i7 / AMD Ryzen (ONNX Runtime 4 threads).
  4. **Mobile/Embedded CPU**: ARM Cortex-A78 / Raspberry Pi 5.
- **Audited Metrics**:
  - Model Parameter Count ($M_{\text{params}}$).
  - Theoretical FLOPs per 2.0-second multimodal window ($T=256$).
  - Peak Memory Footprint during Inference (MB VRAM / RAM).
  - Batch=1 Inference Latency (Mean $\pm$ 95th percentile in milliseconds).
  - Real-Time Throughput (Windows processed per second).

---

## 4. Standardized Reporting Templates

### Template 1: Missing-Modality Degradation Matrix (DEAP & DREAMER)

```markdown
| Active Modalities | Input State | Early Fusion CNN F1 | Late Fusion F1 | DGCNN / RGNN F1 | MMB-EmotionNet (Vanilla) | MMB-EmotionNet (+ Impute) | Retention % (vs Full) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EEG + ECG + EDA** | Full Modality (Clean) | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | 100.0% (Anchor) |
| **ECG + EDA** | Missing EEG (100%) | -- ± -- | -- ± -- | N/A (EEG-only) | -- ± -- | -- ± -- | -- % |
| **EEG + EDA** | Missing ECG (100%) | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- % |
| **EEG + ECG** | Missing EDA (100%) | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- % |
| **EEG Only** | Missing ECG + EDA | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- ± -- | -- % |
| **ECG Only** | Missing EEG + EDA | -- ± -- | -- ± -- | N/A | -- ± -- | -- ± -- | -- % |
| **EDA Only** | Missing EEG + ECG | -- ± -- | -- ± -- | N/A | -- ± -- | -- ± -- | -- % |
```

---

### Template 2: Noise Degradation & Artifact Robustness

```markdown
| Perturbation Regime | Noise Parameter | Early Fusion F1 | Late Fusion F1 | MMB-EmotionNet F1 | Performance Drop (Δ F1) | Statistical Sig (p-val) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Clean Baseline** | No Noise | -- ± -- | -- ± -- | -- ± -- | 0.00 (Anchor) | -- |
| **Gaussian Noise** | SNR = 20 dB | -- ± -- | -- ± -- | -- ± -- | - -- | < 0.05 |
| **Gaussian Noise** | SNR = 10 dB | -- ± -- | -- ± -- | -- ± -- | - -- | < 0.01 |
| **Gaussian Noise** | SNR = 0 dB | -- ± -- | -- ± -- | -- ± -- | - -- | < 0.001 |
| **EMG Burst Artifact**| SAR = 0 dB (Frontal) | -- ± -- | -- ± -- | -- ± -- | - -- | < 0.01 |
| **Baseline Drift** | 0.1 Hz Sinusoid | -- ± -- | -- ± -- | -- ± -- | - -- | < 0.05 |
```

---

### Template 3: Hardware Deployment & Latency Benchmark

```markdown
| Target Platform | Runtime Engine | Precision | Batch Size | Inference Latency (Mean ± p95) | Peak RAM/VRAM | Max Throughput (Hz) | Real-Time Capable (<50ms)? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NVIDIA RTX 4090** | PyTorch (CUDA) | FP32 | 1 | -- ± -- ms | -- MB | -- windows/s | YES (Ultra-Fast) |
| **NVIDIA RTX 4090** | TensorRT | FP16 | 1 | -- ± -- ms | -- MB | -- windows/s | YES (Ultra-Fast) |
| **Jetson Orin Nano**| TensorRT | FP16 | 1 | -- ± -- ms | -- MB | -- windows/s | YES |
| **Intel Core i7** | ONNX Runtime | FP32 | 1 | -- ± -- ms | -- MB | -- windows/s | YES |
| **Raspberry Pi 5** | ONNX Runtime | INT8 / FP32 | 1 | -- ± -- ms | -- MB | -- windows/s | YES / NO |
```

---

## 5. Failure Diagnostics & Risk Mitigation

| Failure Mode | Root Cause | Diagnostic Trigger | Protocol Mitigation |
| :--- | :--- | :--- | :--- |
| **Imputation Collapse** | Null token causes gradient saturation | Missing-modality F1 $< 40\%$ | Apply LayerNorm after neutral null embedding $\mathbf{e}_m^{\text{null}}$ and scale imputation learning rate by $0.5$. |
| **Dropout Over-Regularization** | High $p_{\text{drop}}$ degrades clean full-modality F1 | Clean multimodal F1 drops $> 3\%$ when $p_{\text{drop}}=0.5$ | Enforce adaptive curriculum dropout scheduling ($p_{\text{drop}}$ increases linearly from $0.0$ to $0.25$ over epochs 1–50). |
| **Severe High-Noise Breakdown** | Noise overwhelms low-amplitude EEG microvolts | F1 drops $> 25\%$ at SNR $= 10\text{ dB}$ | Prepend spatial Laplacian surface filtering or adaptive bandpass filtering ($4–45\text{ Hz}$) before Branch 1 convolution. |
| **Edge Latency Overrun** | Cross-modal attention scales quadratically | Latency $> 50\text{ ms}$ on Raspberry Pi | Prune cross-modal attention key-value dimensions from $d_k=64 \rightarrow 32$ or utilize linear cross-attention approximation. |

---

## 6. Summary of Protocol Deliverables

1. **8 Controlled Robustness Experiments** (`EXP-ROB-01` to `EXP-ROB-08`) covering single/dual dropout, noise regimes, and hardware profiling.
2. **Mathematical formulations** for stochastic modality dropout, latent cross-modal inpainting, and physiological artifact models.
3. **Hardware benchmarking specifications** across 4 computing tiers (Server GPU, Edge GPU, Desktop CPU, Embedded ARM).
4. **Standardized multi-metric comparison templates** reporting Retention Ratio ($\rho_m$), AUDC, and latency percentiles.
5. **Direct alignment** with RQ6 and Hypothesis $H_6$.
