# Literature Taxonomy & Classification Dimensions

**Domain**: Multimodal Biosignal Emotion Recognition  
**Framework**: Multi-Task Multi-Branch Deep Learning  

---

## 1. Classification Categories (Levels A – L)

- **A — Foundational**: Fundamental neural, physiological, and mathematical principles.
- **B — Dataset / Benchmark**: Canonical corpora, annotation protocols, baseline datasets (e.g., AMIGOS `P0001`).
- **C — Unimodal Emotion Recognition**: Single-modality modeling (e.g., RGNN `P0002`, NGN-XGBoost `P0010`).
- **D — Multimodal Emotion Recognition**: Multimodal physiological modeling (e.g., BDAE `P0003`, Entropy-Assisted `P0006`).
- **E — Multitask Learning**: Joint task optimization & ambiguous label learning (e.g., Partial Label Learning `P0008`).
- **F — Multi-Branch Architecture**: Modality-specific and hemispheric dedicated streams (e.g., BiHDM `P0005`).
- **G — Multimodal Fusion**: Early, Intermediate, Late, and Cross-Attention fusion schemes.
- **H — Generalization / Domain Adaptation**: Cross-subject, cross-session, and cross-dataset transfer (e.g., Stable Patterns `P0004`).
- **I — Robustness / Missing Modality**: Handling missing biosensors, sensor failure, and noisy artifacts.
- **J — Efficient / Lightweight Models**: Knowledge distillation, compact CNNs, edge deployment (e.g., KD-DANN `P0007`).
- **K — Self-Supervised / Contrastive Learning**: Pretext task representation learning on unlabeled physiological data.
- **L — Review / Survey**: Comprehensive state-of-the-art surveys and methodological analyses (e.g., `P0009`).

---

## 2. Dimensional Tagging Matrix

| Tag Dimension | Available Tags | Description / Scope |
|---|---|---|
| **Modality** | `[EEG]`, `[ECG]`, `[EDA]`, `[GSR]`, `[EMG]`, `[PPG]`, `[RESP]`, `[MULTIMODAL]` | Specific sensor signals processed |
| **Architecture** | `[UNIMODAL]`, `[MULTIBRANCH]`, `[MULTISTREAM]`, `[SHARED_ENCODER]`, `[PRIVATE_SHARED]`, `[TRANSFORMER]`, `[CNN]`, `[GNN]`, `[ATTENTION]`, `[EFFICIENT]` | Neural encoder backbone structures |
| **Fusion** | `[EARLY_FUSION]`, `[INTERMEDIATE_FUSION]`, `[LATE_FUSION]`, `[CROSS_MODAL_ATTENTION]`, `[ADAPTIVE_FUSION]` | Level and mechanism of modality integration |
| **Learning** | `[SINGLE_TASK]`, `[MULTI_TASK]`, `[MULTI_LABEL]`, `[REGRESSION]`, `[CLASSIFICATION]`, `[PARTIAL_LABEL]` | Training objective and task formulation |
| **Evaluation** | `[SUBJECT_DEPENDENT]`, `[SUBJECT_INDEPENDENT]`, `[LOSO]`, `[CROSS_SESSION]`, `[CROSS_DATASET]`, `[MISSING_MODALITY]` | Validation protocol rigor |
| **Dataset** | `[DEAP]`, `[SEED]`, `[SEED_IV]`, `[SEED_V]`, `[AMIGOS]`, `[DREAMER]`, `[MAHNOB_HCI]`, `[WESAD]` | Benchmark corpus evaluated |
