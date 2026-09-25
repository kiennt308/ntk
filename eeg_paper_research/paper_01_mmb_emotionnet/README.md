# MMB-EmotionNet: Physiologically-Informed Multimodal Representation and Directional Fusion for EEG–Peripheral Biosignal Emotion Recognition

**Target Venue:** *IEEE Transactions on Affective Computing (IEEE TAC)* / *Elsevier Information Fusion*  
**Primary Benchmark Dataset:** **DEAP** (Database for Emotion Analysis using Physiological Signals)  
**Secondary Dual-Benchmark Dataset:** **DREAMER** (Database for Emotion Recognition through EEG and ECG)  
**Evaluation Protocol:** Strict Subject-Independent **Leave-One-Subject-Out (LOSO) Cross-Validation**  

---

## 1. Directory Structure

```
paper_01_mmb_emotionnet/
├── README.md                           # This overview and execution guide
├── data/
│   ├── README.md                       # Dataset specifications, download URLs, and directory layout
│   ├── deap/                           # Storage for DEAP preprocessed .dat files (s01.dat - s32.dat)
│   └── dreamer/                        # Storage for DREAMER.mat
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── encoders.py                 # Physics-informed encoders (ST-GCN for EEG, TCN for ECG, CWT for EDA)
│   │   ├── disentanglement.py          # Shared-Private Subspace Disentanglement (L_sim, L_diff, L_recon)
│   │   ├── directional_attention.py    # Directional Cross-Attention (Q_EEG -> K,V_Bio)
│   │   ├── uncertainty_loss.py         # Kendall Homoscedastic Aleatoric Uncertainty Loss Balancing
│   │   └── mmb_emotionnet.py           # Complete end-to-end MMB-EmotionNet PyTorch model
│   ├── dataset/
│   │   ├── __init__.py
│   │   └── deap_loso_loader.py         # Anti-leakage LOSO data generator & pre-split isolated standardizer
│   └── utils/
│       ├── __init__.py
│       └── metrics.py                  # Macro F1, Accuracy, and Wilcoxon signed-rank test
└── manuscript/
    ├── draft.md                        # Complete research paper manuscript
    ├── tables/                         # SOTA comparison & 8-config ablation tables
    └── figures/                        # Architecture flowcharts & t-SNE visualizations
```

---

## 2. Core Methodological Contributions

1. **Physics-Informed Modality Encoders**:
   - **EEG Branch**: Dynamic Spatial-Temporal Graph Convolutional Network (ST-GCN) respecting 10–20 electrode topology.
   - **ECG Branch**: Dilated 1D Temporal Convolutional Network (TCN) capturing cardiac cycles and inter-beat intervals.
   - **EDA Branch**: Continuous Wavelet Transform (CWT) multi-scale decomposition separating tonic skin conductance level (SCL) from phasic responses (SCR).

2. **Shared-Private Subspace Disentanglement**:
   - Explicitly factorizes latent features into $\mathcal{Z}_{\text{Shared}}$ (emotion-invariant semantics) and $\mathcal{Z}_{\text{Private}}$ (wearable sensor noise and subject-specific baselines).
   - Constrained by Central Moment Discrepancy ($\mathcal{L}_{\text{sim}}$), Frobenius-norm orthogonality ($\mathcal{L}_{\text{diff}} = 0$), and reconstructive fidelity ($\mathcal{L}_{\text{recon}}$) to prevent representation collapse.

3. **Directional Cross-Modal Attention ($Q_{\text{EEG}} \rightarrow K,V_{\text{Bio}}$)**:
   - Grounded in affective neuroscience: Cortical cognitive appraisal (CNS) acts as the Query anchor guiding autonomic physiological arousal (ANS) feature selection, eliminating modality dominance and noise contamination.

4. **Multi-Task Homoscedastic Uncertainty Balancing**:
   - Resolves inter-task gradient competition between continuous Valence and Arousal dimensions via learnable task variance parameters $(\sigma_V, \sigma_A)$.

5. **Leak-Free Subject-Independent LOSO Validation**:
   - Zero sample-level or trial-level leakage. Pre-split isolated standard scaling.
