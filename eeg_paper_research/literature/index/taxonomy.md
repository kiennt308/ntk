# Literature Taxonomy & Classification Dimensions (2023–2026 Modernized)
## Multi-Task Multi-Branch Deep Learning for Biosignal Emotion Recognition

---

## 1. Classification Categories (Levels A – N)

- **A — Foundational**: Fundamental neural, physiological, autonomic (CNS vs. ANS), and mathematical principles.
- **B — Dataset / Benchmark**: Canonical corpora, annotation protocols, baseline datasets (e.g., DEAP, SEED, DREAMER, AMIGOS, WESAD, K-EmoCon).
- **C — Unimodal Emotion Recognition**: Single-modality modeling (e.g., Spatial-Temporal EEG, 1D-CNN ECG, CWT-EDA).
- **D — Multimodal Emotion Recognition**: Multimodal physiological modeling integrating Central (EEG) and Peripheral (ECG, EDA, PPG, Respiration, EMG) signals.
- **E — Multitask Learning (MTL)**: Joint Valence-Arousal-Dominance optimization, Kendall uncertainty loss balancing, GradNorm gradient conflict resolution.
- **F — Multi-Branch Architecture**: Dedicated physics-informed encoders preserving modality-specific spatial/temporal properties.
- **G — Multimodal Fusion**: Early, Intermediate, Late, Bidirectional Cross-Modal QKV Attention, and Bilinear Tensor Fusion.
- **H — Subspace Disentanglement & Domain Adaptation**: Shared-Private representation decomposition ($Z_{shared}, Z_{private}$), Orthogonality constraints, DANN, MMD, CORAL.
- **I — Robustness & Missing Modalities**: Handling missing biosensors, sensor dropouts, cross-modal knowledge distillation, and generative imputation.
- **J — Efficient & Edge BCI Models**: Model compression, INT8/FP16 quantization, latency-constrained edge deployment on wearables/embedded NPUs.
- **K — Self-Supervised & Foundation Models**: Large-scale pretext task pretraining (Masked Autoencoding, Contrastive Learning) on massive unlabeled biosignals.
- **L — Graph Neural Networks (GNNs)**: Dynamic brain connectivity, Phase Locking Value (PLV), hemisphere asymmetry topologies.
- **M — Explainable AI (XAI)**: SHAP, Integrated Gradients, Grad-CAM topographic scalp maps, biological validity verification.
- **N — Review / Survey**: Comprehensive state-of-the-art PRISMA surveys and methodological benchmarks.

---

## 2. Dimensional Tagging Matrix

| Tag Dimension | Available Tags | Description / Scope |
|---|---|---|
| **Modality** | `[EEG]`, `[ECG]`, `[EDA]`, `[GSR]`, `[EMG]`, `[PPG]`, `[RESP]`, `[EYE]`, `[MULTIMODAL]` | Specific sensor signals processed |
| **Architecture** | `[MULTIBRANCH]`, `[SHARED_PRIVATE]`, `[DISENTANGLEMENT]`, `[TRANSFORMER]`, `[GNN]`, `[GAT]`, `[DGCNN]`, `[CNN]`, `[TCN]`, `[FOUNDATION_MODEL]` | Neural encoder backbone structures |
| **Fusion** | `[EARLY_FUSION]`, `[INTERMEDIATE_FUSION]`, `[LATE_FUSION]`, `[CROSS_MODAL_ATTENTION]`, `[BILINEAR_POOLING]` | Level and mechanism of modality integration |
| **Learning** | `[SINGLE_TASK]`, `[MULTI_TASK]`, `[UNCERTAINTY_WEIGHTING]`, `[GRADNORM]`, `[SELF_SUPERVISED]`, `[MASKED_AUTOENCODING]` | Training objective and task formulation |
| **Adaptation** | `[DISENTANGLEMENT]`, `[DANN]`, `[ADVERSARIAL_ALIGNMENT]`, `[ORTHOGONALITY]`, `[MMD]` | Domain alignment and invariance mechanisms |
| **Evaluation** | `[SUBJECT_INDEPENDENT]`, `[LOSO]`, `[CROSS_SESSION]`, `[CROSS_DATASET]`, `[MISSING_MODALITY_STRESS]` | Validation protocol rigor |
| **Explainability** | `[SHAP]`, `[GRAD_CAM]`, `[TOPOPLOT]`, `[INTEGRATED_GRADIENTS]`, `[NEURO_VALIDATION]` | Interpretable decision visualization |
| **Dataset** | `[DEAP]`, `[SEED]`, `[SEED_IV]`, `[SEED_V]`, `[AMIGOS]`, `[DREAMER]`, `[MAHNOB_HCI]`, `[WESAD]`, `[K_EMOCON]` | Benchmark corpus evaluated |
