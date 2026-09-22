# Phase P3: Research Gap Analysis

**Project**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Working Title**: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức  
**Phase**: P3 — Research Gap Analysis  
**Last Updated**: 2026-09-22  
**Status**: Formal Literature Gaps Formulated & Backed by Evidence  

---

## 1. Research Gap Policy & Compliance

In strict compliance with **Section 5 of `AGENTS.md`**, this document avoids unsubstantiated claims of absolute novelty (e.g., *"this has never been studied"*). Instead, all identified research gaps are formulated using evidence-calibrated language (e.g., *"The literature reviewed suggests..."*, *"Few studies were identified that..."*) and are substantiated by multiple verified peer-reviewed publications from the repository ([`P0001`–`P0030`](file:///d:/ntk/eeg_paper_research/literature/index/paper-index.csv)).

Every statement is tagged with its epistemological status:
- `[FACT]`: Directly reported or measured in peer-reviewed literature.
- `[SUPPORTED]`: Strongly corroborated by comparative experimental findings.
- `[INFERENCE]`: Methodological synthesis derived across multiple studies.
- `[HYPOTHESIS]`: Testable proposition requiring experimental validation in subsequent phases.

---

## 2. Identified Research Gaps

---

### Research Gap 1: Modality Rate Asymmetry and Gradient Dominance in Biosignal Fusion

- **Description**:
  Existing multimodal biosignal emotion recognition systems predominantly rely on either naive feature concatenation (Early Fusion) or uncoupled score averaging (Late Fusion). The literature reviewed suggests that naive concatenation causes high-dimensional, high-frequency Central Nervous System signals (EEG: 32–62 channels at 128–500 Hz) to dominate gradient updates during backpropagation, suppressing subtle but critical Autonomic Nervous System cues (ECG, EDA, Respiration at 1–128 Hz).
- **Supporting Literature Evidence**:
  - `[FACT]` In the DEAP benchmark paper ([`P0001`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0001.md), [`P0006`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0006.md)), early feature concatenation often performed worse than or yielded only marginal gains over single-modality EEG due to feature dimension disparity.
  - `[FACT]` In the multi-stream study by Siddharth et al. ([`P0014`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0014.md)), late decision fusion outperformed early concatenation by $+4.1\%$, because concatenation failed to learn inter-modality cross-correlations without overpowering peripheral branches.
  - `[SUPPORTED]` In recent comprehensive reviews ([`P0025`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0025.md), [`P0030`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0030.md)), standard deep architectures were observed to suffer from "modality collapse", where the network relies almost exclusively on the easiest-to-fit modality during training.
- **Epistemological Classification**: `[SUPPORTED]`
- **Research Implication for Proposed Architecture**:
  Requires dedicated modality-specific encoder branches (e.g., compact EEGNet for EEG, dilated 1D-CNN for ECG/EDA) paired with directional Cross-Modal Attention (Query-Key-Value projections) rather than flat feature concatenation.

---

### Research Gap 2: Lack of Explicit Shared-Private Subspace Disentanglement in Biosignals

- **Description**:
  While shared-private representation learning (e.g., MISA, DSN) has been successfully applied to text-audio-visual multimodal sentiment analysis, few studies have formalized explicit orthogonal shared-private subspace disentanglement for combined EEG and autonomic peripheral biosignals. Existing biosignal models mix modality-unique sensor dynamics (e.g., ocular artifacts in EEG, movement/sweat drift in EDA) with shared underlying affective states.
- **Supporting Literature Evidence**:
  - `[FACT]` In Zheng et al.'s bimodal autoencoder ([`P0003`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0003.md)), learning a shared middle layer improved bimodal classification to $91.01\%$, but did not explicitly constrain or isolate modality-private residual spaces.
  - `[SUPPORTED]` Biological affective neuroscience ([`P0022`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0022.md), [`P0027`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0027.md)) confirms that EEG scalp potentials contain substantial non-emotional electrophysiological components (e.g. baseline cortical rhythms, reference artifacts) that do not share covariance with sympathetic EDA or cardiac HRV.
  - `[INFERENCE]` Monolithic intermediate fusion forces all latent features into a single joint space, causing modality-specific sensor noise to corrupt the shared affective representation.
- **Epistemological Classification**: `[SUPPORTED]`
- **Research Implication for Proposed Architecture**:
  Requires formulating explicit **Similarity Losses** ($\mathcal{L}_{sim}$ via Central Moment Discrepancy or MMD) to align shared emotion distributions and **Difference Losses** ($\mathcal{L}_{diff}$ via soft Frobenius orthogonality) to ensure private sensor dynamics remain strictly orthogonal to the shared emotion manifold.

---

### Research Gap 3: Negative Transfer and Gradient Conflict in Multi-Task Emotion Learning

- **Description**:
  Human emotional experience involves multiple interrelated facets: continuous Valence (hedonic tone), continuous Arousal (physiological activation), and discrete categorical states (e.g., Joy, Sadness, Anger). Existing affective computing literature often trains isolated single-task models for each axis or uses fixed, hand-tuned loss weighting ($\mathcal{L} = \lambda_1 \mathcal{L}_v + \lambda_2 \mathcal{L}_a$). The literature reviewed suggests that fixed weighting causes destructive gradient interference (negative transfer) between continuous regression and discrete classification objectives.
- **Supporting Literature Evidence**:
  - `[FACT]` Large-scale semantic manifold analysis by Cowen & Keltner ([`P0029`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0029.md)) demonstrated that a 2D Valence-Arousal space explains only $38.5\%$ of emotional variance, whereas discrete continuous semantic categories account for $>89\%$, proving that Valence and Arousal alone are insufficient to capture complete affect.
  - `[FACT]` Emotion differentiation research ([`P0028`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0028.md)) proves that differentiating discrete negative emotions provides distinct predictive power beyond global valence extremity.
  - `[FACT]` In partial label learning ([`P0008`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0008.md)), ambiguous candidate labels degrade performance unless dynamic disambiguation loss weighting is employed.
  - `[SUPPORTED]` In multi-task deep learning literature (Kendall et al., CVPR 2018; [`P0025`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0025.md)), tasks with different loss scales (e.g., MSE for regression vs. Cross-Entropy for classification) have gradients that point in conflicting directions, degrading the shared representation unless dynamic balancing is applied.
- **Epistemological Classification**: `[SUPPORTED]`
- **Research Implication for Proposed Architecture**:
  Requires integrating multi-task prediction heads (Valence regression, Arousal regression, Discrete classification) regularized by **Homoscedastic Aleatoric Uncertainty Loss Balancing**, where task loss weights $\frac{1}{2\sigma_i^2}$ are learned dynamically during training.

---

### Research Gap 4: Fragility of Multimodal Architectures Under Missing or Corrupted Modalities

- **Description**:
  In real-world wearable affective computing and ambulatory monitoring, sensors frequently detach, experience contact impedance failure, or are omitted due to battery constraints. Existing multimodal biosignal deep models are almost exclusively trained and evaluated on complete-case datasets; few studies evaluate graceful performance degradation when primary modalities (e.g., EEG) drop out during inference.
- **Supporting Literature Evidence**:
  - `[FACT]` In consumer-grade brain sensing experiments ([`P0019`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0019.md)), reducing channels from 32 to 4 channels drops Leave-One-Subject-Out (LOSO) accuracy to $\approx 61–63\%$, demonstrating extreme vulnerability to channel loss.
  - `[FACT]` Wearable mobility trials in real outdoor environments ([`P0015`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0015.md)) report frequent transient sensor detachment and high motion artifacts on scalp electrodes.
  - `[SUPPORTED]` In 2024–2025 literature reviews ([`P0025`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0025.md), [`P0030`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0030.md)), missing-modality robustness in deep multimodal biosignals is identified as an urgent, underexplored operational challenge.
- **Epistemological Classification**: `[SUPPORTED]`
- **Research Implication for Proposed Architecture**:
  Requires introducing **Modality Dropout** during training alongside cross-modal latent reconstruction decoders ($\mathcal{L}_{recon}$) that allow available peripheral signals to impute missing central neural representations during inference.

---

### Research Gap 5: Severe Cross-Subject Generalization Collapse in LOSO Protocols

- **Description**:
  A pervasive gap exists between within-subject (subject-dependent) and cross-subject (subject-independent) evaluation. The literature reviewed reveals that within-subject models frequently report 80–94% accuracy, but performance drops sharply to 55–75% under strict Leave-One-Subject-Out (LOSO) cross-validation due to individual physiological baseline differences, skull conductivity variation, and emotional expressivity disparities.
- **Supporting Literature Evidence**:
  - `[FACT]` On the AMIGOS benchmark ([`P0001`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0001.md)), unimodal LOSO F1-scores were only $0.528–0.540$, rising to $0.575$ under multimodal fusion.
  - `[FACT]` On SEED, SVM accuracy drops from $83.99\%$ (within-subject) to $72.45\%$ in LOSO ([`P0002`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0002.md), [`P0012`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0012.md)).
  - `[FACT]` Domain adaptation methods (e.g. KD-DANN in [`P0007`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0007.md), T-SVM in [`P0021`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0021.md)) demonstrate that explicitly aligning source and target subject distributions recovers $+8\%$ to $+12\%$ in cross-subject accuracy.
  - `[FACT]` In incompatible headset transfer ([`P0020`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0020.md)), cross-dataset zero-shot transfer without coordinate embedding drops to near chance ($52.4\%$).
- **Epistemological Classification**: `[FACT]`
- **Research Implication for Proposed Architecture**:
  Cross-subject generalization must be treated as a primary evaluation dimension. The architecture should incorporate domain-invariant feature alignment (e.g. Gradient Reversal Layers or MMD regularization).

---

### Research Gap 6: Methodological Flaws and Windowing Data Leakage in Prior Literature

- **Description**:
  A significant portion of published literature in affective computing suffers from hidden data leakage caused by windowing before cross-validation splitting or improper baseline normalization, creating over-optimistic, non-reproducible performance claims.
- **Supporting Literature Evidence**:
  - `[FACT]` The 2024 critical review ([`P0030`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0030.md)) audited published studies and found that over $35\%$ of early papers partitioned overlapping temporal sliding windows *before* train/test splitting, producing artificially inflated accuracies ($>95\%$) that collapsed to near-chance upon proper subject-isolated re-evaluation.
  - `[FACT]` Studies on referencing effects ([`P0027`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0027.md)) proved that non-neutral reference choices (e.g., vertex or mastoid references) distort spatial potential gradients by $>28\%$, invalidating spatial assumptions if uncorrected.
- **Epistemological Classification**: `[FACT]`
- **Research Implication for Proposed Architecture**:
  All experiments in this PhD project must enforce strict, leak-free pipelines: subject-isolated partitioning *prior* to temporal windowing, independent fold normalization, and standardized reference transformations (REST / CAR).

---

## 3. Gap-to-Solution Mapping Matrix

| Research Gap | Root Cause in Literature | Epistemological Status | Proposed Architectural Countermeasure | Primary Benchmark Datasets |
|---|---|---|---|---|
| **Gap 1: Modality Rate & Gradient Asymmetry** | Naive early feature concatenation; EEG gradient dominance | `[SUPPORTED]` | Dedicated multi-branch encoders (EEGNet + 1D-CNN) + Cross-Modal Attention QKV | DEAP, DREAMER, AMIGOS |
| **Gap 2: Lack of Shared-Private Disentanglement** | Entanglement of modality sensor artifacts with shared affect | `[SUPPORTED]` | Orthogonal shared-private subspaces via similarity ($\mathcal{L}_{sim}$) and difference ($\mathcal{L}_{diff}$) losses | DEAP, DREAMER, SEED-IV |
| **Gap 3: Multi-Task Gradient Conflict** | Fixed loss weighting between regression and classification | `[SUPPORTED]` | Dynamic homoscedastic uncertainty loss balancing ($\sigma_v, \sigma_a, \sigma_c$) | DEAP, AMIGOS, SEED-V |
| **Gap 4: Missing-Modality Fragility** | Complete-case assumption; no graceful degradation mechanism | `[SUPPORTED]` | Modality Dropout during training + Cross-modal reconstruction decoders ($\mathcal{L}_{recon}$) | DEAP, DREAMER, CASE |
| **Gap 5: Cross-Subject Generalization Drop** | Inter-subject baseline shifts and high physiological variance | `[FACT]` | Adversarial domain adaptation (GRL) & geometric coordinate embeddings (SCANet) | DEAP (32 subj), SEED (15 subj) |
| **Gap 6: Data Leakage Vulnerabilities** | Overlapping windowing before splitting; unstandardized referencing | `[FACT]` | Strict subject-isolated partitioning prior to windowing; REST/CAR referencing | All benchmark protocols |

---

## 4. Synthesis & Transition to Phase P4

Having established and substantiated the six core research gaps from peer-reviewed evidence, the project is ready to transition to **Phase P4: Research Questions & Hypotheses Formulation** to define formal, testable statistical hypotheses ($H_1$ to $H_6$) mapped to candidate research questions.
