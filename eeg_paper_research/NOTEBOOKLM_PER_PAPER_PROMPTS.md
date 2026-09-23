# 📑 NotebookLM Individual Task Prompts per Paper (English Suite)
## Doctoral Research: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals

This document provides dedicated, task-by-task **English Prompts** for **Google NotebookLM** to analyze any individual research paper based on the 26 rigorous tasks defined in [`NotebookLM.md`](NotebookLM.md).

---

## 🎯 Global Instructions & Evidentiary Rules (Applied to All Prompts)

When using any prompt below:
1. Replace `[INSERT PAPER TITLE OR PAPER ID]` with the target paper title or citation ID (e.g., `OA_KW1_001` or `LGGNet`).
2. NotebookLM must evaluate **ONLY** the sources uploaded in the notebook.
3. NotebookLM must label every piece of extracted information with:
   - **`[EXPLICIT]`**: Directly stated in the paper text (with section/table/page citation).
   - **`[SUPPORTED]`**: Strongly supported by reported experimental figures or tables.
   - **`[INFERRED]`**: Reasonable interpretation but not explicitly stated.
   - **`[UNKNOWN]`**: Cannot be determined from the source text (never hallucinate or guess).
4. Strict evaluation chain rule:
   $$\text{METHOD} \longrightarrow \text{DATASET} \longrightarrow \text{PROTOCOL} \longrightarrow \text{METRIC} \longrightarrow \text{RESULT}$$

---

## 📑 Table of Contents (26 Discrete Task Prompts)

- [PROMPT 1 — Paper Identity](#prompt-1--paper-identity)
- [PROMPT 2 — Dataset Specification](#prompt-2--dataset-specification)
- [PROMPT 3 — Preprocessing Protocol](#prompt-3--preprocessing-protocol)
- [PROMPT 4 — Data Split & Partitioning](#prompt-4--data-split--partitioning)
- [PROMPT 5 — Model Architecture](#prompt-5--model-architecture)
- [PROMPT 6 — Multimodal Fusion Mechanism](#prompt-6--multimodal-fusion-mechanism)
- [PROMPT 7 — Multi-Task Learning Formulation](#prompt-7--multi-task-learning-formulation)
- [PROMPT 8 — Multi-Branch Structure](#prompt-8--multi-branch-structure)
- [PROMPT 9 — Baseline Comparisons](#prompt-9--baseline-comparisons)
- [PROMPT 10 — Experimental Results](#prompt-10--experimental-results)
- [PROMPT 11 — Ablation Experiments](#prompt-11--ablation-experiments)
- [PROMPT 12 — Generalization Capabilities](#prompt-12--generalization-capabilities)
- [PROMPT 13 — Robustness & Missing Modalities](#prompt-13--robustness--missing-modalities)
- [PROMPT 14 — Computational Cost & Efficiency](#prompt-14--computational-cost--efficiency)
- [PROMPT 15 — Stated & Observed Limitations](#prompt-15--stated--observed-limitations)
- [PROMPT 16 — Reproducibility Assessment](#prompt-16--reproducibility-assessment)
- [PROMPT 17 — Data Leakage Audit](#prompt-17--data-leakage-audit)
- [PROMPT 18 — Scientific Evidence Table](#prompt-18--scientific-evidence-table)
- [PROMPT 19 — Standardized 18-Point Paper Summary](#prompt-19--standardized-18-point-paper-summary)
- [PROMPT 20 — Research Relevance to PhD Thesis](#prompt-20--research-relevance-to-phd-thesis)
- [PROMPT 21 — Research Gap Extraction & Formulation](#prompt-21--research-gap-extraction--formulation)
- [PROMPT 22 — Novelty & Prior Art Collision Check (P4)](#prompt-22--novelty--prior-art-collision-check-p4)
- [PROMPT 23 — Research Directions & Architectural Taxonomy (P5)](#prompt-23--research-directions--architectural-taxonomy-p5)
- [PROMPT 24 — Research Questions & Hypotheses Formulation (P6)](#prompt-24--research-questions--hypotheses-formulation-p6)
- [PROMPT 25 — Experimental Verification & Protocol Design (P7)](#prompt-25--experimental-verification--protocol-design-p7)
- [PROMPT 26 — Research Decision Map Synthesis (P8)](#prompt-26--research-decision-map-synthesis-p8)
- [APPENDIX — All-in-One Master Deep Extraction Prompt](#appendix--all-in-one-master-deep-extraction-prompt)

---

### PROMPT 1 — Paper Identity

```markdown
You are a scientific literature analysis assistant for the PhD research project: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources in this notebook. Do not invent missing information. For each item, provide source locations (section/page) and categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 1 — PAPER IDENTITY:
Extract:
1. Exact Title
2. Authors and Affiliations
3. Publication Year
4. Venue / Journal / Conference
5. DOI and Official URL
6. Core Research Problem addressed
7. Main Objective of the study
8. Primary Claimed Scientific Contributions
```

---

### PROMPT 2 — Dataset Specification

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Do not invent missing information. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 2 — DATASET SPECIFICATION:
Extract:
1. Dataset Name (e.g., DEAP, SEED, SEED-IV, SEED-V, DREAMER, AMIGOS, MAHNOB-HCI, WESAD, or Custom)
2. Number of Subjects and Demographics (age, gender distribution if reported)
3. Modalities recorded (EEG, ECG, EDA/GSR, PPG, EMG, Respiration, Eye-tracking, etc.)
4. Number of Channels/Sensors for each modality and sensor placement montage (e.g., 10-20 international system)
5. Sampling Frequency (Hz) for each recorded signal stream
6. Emotion Elicitation Method (video clips, music videos, acoustic stimuli, standardized recall)
7. Emotional Labels and Label Space (Valence, Arousal, Dominance / Discrete categories)
8. Number of Classes and Rating Scale (e.g., continuous 1–9 SAM scale, binary thresholding)
9. Trial Duration (seconds)
10. Segmentation and Windowing: Window Length (seconds/samples) and Overlap / Step Size
```

---

### PROMPT 3 — Preprocessing Protocol

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 3 — PREPROCESSING PROTOCOL:
Extract:
1. Bandpass Filtering (cutoff frequencies, filter types, orders for each modality)
2. Notch Filtering (50 Hz / 60 Hz powerline interference removal)
3. Artifact Removal methods (ICA, EOG/EMG regression, thresholding, wavelet denoising, CAR/REST reference transformation)
4. Normalization and Scaling (Z-score, Min-Max, baseline subtraction, per-subject vs. global)
5. Segmentation and Windowing parameters
6. Data Augmentation techniques applied (jittering, masking, GANs, mixup, crop)
7. Handcrafted Feature Extraction (e.g., DE, PSD, CWT, HRV time/frequency metrics, EDA tonic/phasic CDA)
8. Dimensionality Reduction (PCA, t-SNE, feature selection algorithms)
9. CRITICAL AUDIT: State explicitly whether normalization, filtering, and feature extraction were performed BEFORE or AFTER the train/test splitting.
```

---

### PROMPT 4 — Data Split & Partitioning

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Do not assume a safe split. If unclear, explicitly state [UNKNOWN].

Perform TASK 4 — DATA SPLIT & PARTITIONING:
Determine and explain:
1. Is the evaluation Subject-Dependent (within-subject) or Subject-Independent (cross-subject)?
2. Exact Splitting Strategy: Random split, Subject-wise K-Fold, Leave-One-Subject-Out (LOSO), Cross-Session, or Cross-Dataset?
3. Exact Ratio/Fold Partitioning: Training %, Validation %, and Testing %
4. Construction Details: Explain exactly how train/validation/test sets were assembled.
5. Window Overlap Leakage Check: Could overlapping sliding windows from the same trial or subject appear simultaneously in both training and testing folds?
```

---

### PROMPT 5 — Model Architecture

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Explain what each component does according to the paper.

Perform TASK 5 — MODEL ARCHITECTURE:
Extract and trace the full computational flow:
Input → Preprocessing → Feature Representation → Backbone Encoder → Branch Structure → Shared Representation → Private Representation → Fusion Layer → Task-Specific Heads → Output.

Identify and detail:
1. Deep Learning Architectures used (CNN 1D/2D, RNN/LSTM/GRU, Transformer, GNN/GAT/DGCNN, Spiking Neural Networks, Conformer)
2. Latent dimensions, hidden layer configurations, activation functions, and dropout rates
3. Shared Representation vs. Modality-Private Representation mechanisms (if any)
4. Alignment, self-supervised, or contrastive learning modules embedded in the architecture.
```

---

### PROMPT 6 — Multimodal Fusion Mechanism

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 6 — MULTIMODAL FUSION:
Classify the fusion mechanism into one of the following:
1. Early Fusion (Data/Feature level concatenation)
2. Intermediate / Feature-level Fusion
3. Late / Decision-level Fusion
4. Cross-Modal Attention (e.g., Query-Key-Value interactions across modalities)
5. Multimodal Transformer (e.g., MulT, cross-attention encoders)
6. Adaptive / Bilinear / Tensor Fusion
7. Other (specify)

Explain:
- Exactly WHERE fusion occurs in the computational pipeline
- What latent representations are fused
- How modalities interact mathematically
- Whether dedicated modality-specific encoders exist prior to fusion
- Whether the model dynamically learns modality importance weights (adaptive gating).
- If the paper only concatenates raw features, state so explicitly.
```

---

### PROMPT 7 — Multi-Task Learning Formulation

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Do not invent loss weighting values.

Perform TASK 7 — MULTI-TASK LEARNING FORMULATION:
Determine:
1. Is the model Single-Task or Multi-Task?
2. What are the specific co-optimized tasks (e.g., Valence classification, Arousal regression, Dominance prediction, Subject identification, Signal reconstruction)?
3. Which layers share representations across tasks, and which layers/heads are task-specific?
4. What individual loss functions are used for each task (e.g., Cross-Entropy, MSE, CCC, Triplet Loss)?
5. Write out the total conceptual multi-task loss objective:
   Example: L_total = λ1 * L_task1 + λ2 * L_task2 + ...
6. Are task weighting coefficients (λ) fixed constants or dynamically learned (e.g., Kendall homoscedastic uncertainty weighting, GradNorm, Dynamic Weight Average)?
```

---

### PROMPT 8 — Multi-Branch Structure

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources.

Perform TASK 8 — MULTI-BRANCH STRUCTURE:
Determine:
1. Total number of independent parallel branches in the network
2. Input signal assigned to each branch (e.g., Branch 1: Scalp EEG, Branch 2: ECG/HRV, Branch 3: EDA)
3. Specialized encoder architecture of each branch (e.g., Spatial-Temporal GCN for EEG vs. Dilated 1D-TCN for cardiac dynamics)
4. Shared layers vs. Private branch-specific layers
5. Convergence and fusion junction point
6. Physics-Informed Justification: Explain WHY the authors chose a multi-branch design according to the paper. If no explicit reason is given, state: "The paper does not explicitly justify the multi-branch design."
```

---

### PROMPT 9 — Baseline Comparisons

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources.

Perform TASK 9 — BASELINES COMPARISON MATRIX:
Create a comprehensive comparative table:
| Baseline Model | Modality | Architecture Family | Task Formulation | Evaluation Protocol | Reported Performance | Source / Reference |
| -------------- | -------- | ------------------- | ---------------- | ------------------- | -------------------- | ------------------ |

Identify whether the comparative baselines include:
- Unimodal vs. Multimodal baselines
- Traditional Machine Learning (SVM, Random Forest, XGBoost) vs. Deep Learning models
- Standard SOTA architectures (EEGNet, DGCNN, BiHDM, MulT, Conformer)
- Multi-Task vs. Single-Task configurations.
```

---

### PROMPT 10 — Experimental Results

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Preserve the exact formulation: METHOD → DATASET → PROTOCOL → METRIC → RESULT.

Perform TASK 10 — EXPERIMENTAL RESULTS EXTRACTION:
Extract exact quantitative results reported in the paper:
1. For Classification Tasks:
   - Accuracy (%) and Balanced Accuracy (%)
   - Macro-F1, Weighted-F1, Precision, Recall, ROC-AUC
2. For Continuous Regression Tasks:
   - Mean Absolute Error (MAE), Root Mean Squared Error (RMSE)
   - Coefficient of Determination (R²), Pearson Correlation Coefficient (r), Concordance Correlation Coefficient (CCC)
3. Statistical Rigor:
   - Mean ± Standard Deviation (Std) across subjects/runs
   - 95% Confidence Intervals (CI)
   - Number of experimental repetitions / seeds
   - Statistical significance tests and reported p-values (e.g., paired t-test, Wilcoxon signed-rank test with Bonferroni correction).
```

---

### PROMPT 11 — Ablation Experiments

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Do not claim a component is necessary unless ablation evidence supports that conclusion.

Perform TASK 11 — ABLATION STUDIES:
Identify all ablation configurations reported in the paper.
For every ablation experiment, structure the output as follows:
- Component Removed / Modified:
- Baseline / Variant Name:
- Ablated Model Metric:
- Full Model Metric:
- Absolute Difference (Δ Performance):
- Author's Interpretation:
- Source Location (Table/Figure/Page):
```

---

### PROMPT 12 — Generalization Capabilities

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Do not treat random train/test splitting as cross-subject generalization.

Perform TASK 12 — GENERALIZATION EVALUATION:
Check and extract evidence for:
1. Cross-Subject / Subject-Independent Generalization (Leave-One-Subject-Out / LOSO performance)
2. Cross-Session Generalization (evaluation across different days/sessions for the same subject)
3. Cross-Dataset Generalization (models trained on Dataset A and tested on unseen Dataset B)
4. Domain Adaptation / Alignment Techniques used (DANN, Gradient Reversal Layer, MMD, Coral Loss, Adversarial Alignment)
5. Generalization Degradation: Report the performance drop (Δ) when moving from Subject-Dependent to Subject-Independent protocols.
```

---

### PROMPT 13 — Robustness & Missing Modalities

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. If absent, explicitly write: "Not evaluated".

Perform TASK 13 — ROBUSTNESS & MISSING MODALITIES:
Check whether the paper evaluates:
1. Missing Modality Scenarios (e.g., performance degradation when EEG is dropped and only wearable ECG/EDA is available)
2. Modality Dropout / Noise Injection during training
3. Sensor Artifacts & Signal Corruption (motion artifacts, loose electrode impedance noise)
4. Class Imbalance Handling
5. Cross-Modal Knowledge Distillation or Latent Inpainting for missing sensor imputation.
```

---

### PROMPT 14 — Computational Cost & Efficiency

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. If absent, explicitly write: "Not reported".

Perform TASK 14 — COMPUTATIONAL COST & EFFICIENCY:
Extract:
1. Parameter Count (Total trainable parameters / Millions of weights)
2. Computational Complexity (FLOPs / MACs)
3. Model Storage Footprint (Size in MB)
4. GPU/CPU Memory Consumption (VRAM during training and inference)
5. Training Time (hours/epochs)
6. Inference Latency (milliseconds per window/sample)
7. Hardware Environment (GPU model, CPU, Embedded/Edge platform like Jetson or Raspberry Pi).
```

---

### PROMPT 15 — Stated & Observed Limitations

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources.

Perform TASK 15 — RESEARCH LIMITATIONS:
Categorize into three distinct groups:
Group A — Limitations explicitly acknowledged by the authors in the paper text.
Group B — Methodological limitations directly observable from the experimental design (e.g., small sample size, absence of LOSO evaluation, lack of statistical testing).
Group C — Potential validity concerns requiring further experimental verification (clearly marked as speculative).
```

---

### PROMPT 16 — Reproducibility Assessment

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources.

Perform TASK 16 — REPRODUCIBILITY AUDIT:
Evaluate:
1. Source Code Availability (GitHub/Zenodo URL provided? Open source vs. proprietary)
2. Dataset Accessibility (Publicly available benchmarks vs. private closed cohorts)
3. Detailed Preprocessing Instructions (Exact filter cutoff frequencies, windowing parameters specified?)
4. Hyperparameter Transparency (Learning rate, batch size, optimizer, weight decay, epochs reported?)
5. Random Seed and Initialization details
6. Software Library Versions (PyTorch, TensorFlow, MNE, Scikit-learn).

Assign an overall Reproducibility Rating: HIGH / MEDIUM / LOW / UNKNOWN, and justify with evidence.
```

---

### PROMPT 17 — Data Leakage Audit

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Perform a rigorous, evidence-grounded audit. Do NOT accuse the paper of leakage without concrete textual evidence.

Perform TASK 17 — DATA LEAKAGE AUDIT:
Audit the paper across 8 dimensions and present as a table:
| Leakage Dimension | Evidence in Paper | Risk Level (High/Med/Low/None) | Confidence ([EXPLICIT]/[INFERRED]) |
| ----------------- | ----------------- | ------------------------------ | ---------------------------------- |
| 1. Subject Leakage (Same subject in train & test) | ... | ... | ... |
| 2. Trial Leakage (Same trial segments mixed) | ... | ... | ... |
| 3. Windowing Leakage (Overlapping windows shuffled prior to split) | ... | ... | ... |
| 4. Normalization Leakage (Global Z-score fit before split) | ... | ... | ... |
| 5. Temporal Filtering Leakage (LDS smoothing across split boundaries) | ... | ... | ... |
| 6. Augmentation Leakage (Synthetic samples created from test set) | ... | ... | ... |
| 7. Hyperparameter Tuning Leakage (Tuned on test set) | ... | ... | ... |
| 8. Montage / Sensor Configuration Shift | ... | ... | ... |
```

---

### PROMPT 18 — Scientific Evidence Table

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources.

Perform TASK 18 — SCIENTIFIC EVIDENCE TABLE:
Produce a comprehensive claims-and-evidence table:
| Claim Made by Authors | Experimental Evidence | Source Location (Section/Table/Figure/Page) | Evidence Type ([EXPLICIT]/[SUPPORTED]/[INFERRED]) |
| --------------------- | --------------------- | ------------------------------------------- | -------------------------------------------------- |

Focus specifically on claims regarding:
- Multimodal biosignal synergy
- Multi-task learning advantage
- Multi-branch architectural superiority
- Cross-modal attention mechanisms
- Generalization and robustness.
```

---

### PROMPT 19 — Standardized 18-Point Paper Summary

```markdown
You are a scientific literature analysis assistant. Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Do not provide a research proposal; synthesize the paper objectively.

Perform TASK 19 — STANDARDIZED 18-POINT SUMMARY:
Summarize the paper following EXACTLY this 18-point numbered structure:
1. Research Problem:
2. Dataset Evaluated:
3. Modalities Used:
4. Preprocessing Protocol:
5. Feature Representation:
6. Model Architecture:
7. Multimodal Fusion Mechanism:
8. Multi-Task Formulation:
9. Evaluation Protocol:
10. Comparative Baselines:
11. Main Quantitative Results:
12. Ablation Study Findings:
13. Generalization Performance:
14. Robustness & Missing Modalities:
15. Computational Cost:
16. Stated & Observed Limitations:
17. Reproducibility Assessment:
18. Scientific Evidence Quality:
```

---

### PROMPT 20 — Research Relevance to PhD Thesis

```markdown
You are a scientific literature analysis assistant for the PhD research topic: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Analyze the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources.

Perform TASK 20 — RESEARCH RELEVANCE SCORING:
Classify and justify the relevance of this paper across 7 core dissertation dimensions:

1. Multimodal Biosignals (EEG + Autonomic ECG/EDA): [HIGH / MEDIUM / LOW]
   - Justification: ...
2. Multi-Task Learning (Joint Valence-Arousal-Dominance): [HIGH / MEDIUM / LOW]
   - Justification: ...
3. Multi-Branch Architecture (Physics-informed dedicated encoders): [HIGH / MEDIUM / LOW]
   - Justification: ...
4. Multimodal Fusion (Cross-Modal Attention QKV): [HIGH / MEDIUM / LOW]
   - Justification: ...
5. Cross-Subject Generalization (LOSO / Disentangled representations): [HIGH / MEDIUM / LOW]
   - Justification: ...
6. Missing Modality Robustness (Wearable sensor dropouts): [HIGH / MEDIUM / LOW]
   - Justification: ...
7. Computational Efficiency & Edge BCI Feasibility: [HIGH / MEDIUM / LOW]
   - Justification: ...

Conclude with 3 concrete takeaways or technical ideas from this paper that can directly strengthen the PhD dissertation chapters.
```

---

### PROMPT 21 — Research Gap Extraction & Formulation

```markdown
You are a scientific literature analysis assistant for the PhD research project: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" using the provided sources. Do not invent missing information. For each item, provide concrete textual evidence and label findings as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 21 — RESEARCH GAP EXTRACTION & FORMULATION:
Extract and formulate the scientific and technical gaps revealed by this paper across 3 critical areas:

1. EXPLICIT OPEN QUESTIONS & AUTHOR-STATED GAPS:
   - What unresolved theoretical, experimental, or engineering challenges do the authors explicitly acknowledge as future work?
   - What scenarios did the authors fail to address or declare out-of-scope?

2. METHODOLOGICAL & THEORETICAL GAPS (Cross-checked against SOTA):
   Evaluate whether the paper leaves any of the following foundational gaps unaddressed:
   - Modality Asymmetry & Dominance: Did the model use naive concatenation causing high-dimensional EEG to suppress subtle autonomic ECG/EDA signals?
   - Subspace Disentanglement: Did the architecture fail to isolate subject-specific artifacts/style from shared emotion content?
   - Multi-Task Objective Interference: Did the model use fixed, manual loss weights leading to gradient conflict between Valence and Arousal?
   - Evaluation & Generalization Rigor: Did the study evaluate only subject-dependent protocols without strict Leave-One-Subject-Out (LOSO) cross-subject or cross-dataset validation?
   - Sensor Dropout & Real-World Robustness: Did the paper assume all sensor channels are continuously available, ignoring missing modality scenarios in wearable settings?
   - Neurobiological Grounding & Explainability: Did the model act as a black box without providing topographic scalp activation or physiological interpretability (XAI)?

3. GROUNDED CONTRIBUTION OPPORTUNITY FOR THE PHD DISSERTATION:
   - Formulate a precise, publication-ready research gap statement summarizing how our proposed MMB-EmotionNet architecture (Physics-informed Multi-Branch + Shared-Private Disentanglement + Directional Cross-Attention + Homoscedastic Uncertainty MTL) directly overcomes the weaknesses of this paper.
```

---

### PROMPT 22 — Novelty & Prior Art Collision Check (P4)

```markdown
You are a scientific literature analysis assistant for the PhD research project: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Analyze ONLY the target paper: "[INSERT PAPER TITLE OR PAPER ID]" (and any related work cited in this notebook). Do not assume novelty without textual evidence. Categorize evidence as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN].

Perform TASK 22 — NOVELTY & PRIOR ART COLLISION CHECK:
Investigate whether the core ideas of our PhD dissertation have already been executed by this paper or prior art:

1. COMBINATORIAL COLLISION ANALYSIS:
   Has this paper implemented the EXACT combination of:
   - Multimodal Trinity (Central EEG + Autonomic ECG + Sympathetic EDA)? [YES / PARTIAL / NO]
   - Physics-Informed Dedicated Multi-Branch Encoders (Spatial GCN for EEG, Dilated 1D-TCN for ECG, CWT for EDA)? [YES / PARTIAL / NO]
   - Explicit Shared-Private Subspace Disentanglement (Orthogonality loss separating subject identity from shared emotion manifold)? [YES / PARTIAL / NO]
   - Directional Cross-Modal Attention ($Q_{EEG}, K_{Bio}, V_{Bio}$)? [YES / PARTIAL / NO]
   - Dynamically Balanced Multi-Task Loss (Homoscedastic uncertainty weighting / GradNorm)? [YES / PARTIAL / NO]

2. SIMILARITY & BOUNDARY DELINEATION:
   - What is the exact degree of architectural overlap between this paper and our proposed MMB-EmotionNet framework?
   - Where does this paper stop, and what specific novel territory remains exclusively open for our dissertation?
```

---

### PROMPT 23 — Research Directions & Architectural Taxonomy (P5)

```markdown
You are a scientific literature analysis assistant for the PhD research project: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Analyze the target paper: "[INSERT PAPER TITLE OR PAPER ID]" across the broad literature base in this notebook.

Perform TASK 23 — RESEARCH DIRECTIONS & ARCHITECTURAL TAXONOMY:
Map out and categorize the feasible technical avenues and paradigms represented in this work:

1. BRANCHING PARADIGMS:
   - Classify: Unimodal vs. Homogeneous Multichannel CNN vs. Heterogeneous Physics-Informed Encoders (GNN + TCN + CWT).
   - What are the strengths and trade-offs of this paper's branching approach?

2. FUSION & MODALITY INTERACTION PARADIGMS:
   - Classify: Early Concatenation vs. Intermediate Feature Fusion vs. Late Decision Fusion vs. Bidirectional Cross-Modal QKV Attention vs. Multimodal Transformer (MulT).

3. MULTI-TASK & OPTIMIZATION PARADIGMS:
   - Classify: Single-task independent models vs. Hard parameter sharing vs. Soft parameter sharing vs. Uncertainty-weighted dynamic loss vs. Adversarial subject decoupling.

4. REPRESENTATION ALIGNMENT & GENERALIZATION:
   - Classify: Monolithic latent space vs. Domain Adversarial Alignment (DANN) vs. Maximum Mean Discrepancy (MMD) vs. Explicit Orthogonal Subspace Disentanglement.
```

---

### PROMPT 24 — Research Questions & Hypotheses Formulation (P6)

```markdown
You are a scientific literature analysis assistant for the PhD research project: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Analyze the methodology and empirical gaps of the paper: "[INSERT PAPER TITLE OR PAPER ID]".

Perform TASK 24 — RESEARCH QUESTIONS & TESTABLE HYPOTHESES FORMULATION:
Translate the weaknesses and open directions of this paper into formal, testable PhD research questions and falsifiable hypotheses:

1. FORMULATION OF FORMAL RESEARCH QUESTIONS (RQs):
   - Formulate applicable RQs among $RQ_1$–$RQ_6$ directly motivated by this paper:
     * $RQ_1$ (Physics-Informed Multi-Branch vs. Monolithic/Early Concatenation)
     * $RQ_2$ (Directional Cross-Modal Attention vs. Flat Concatenation)
     * $RQ_3$ (Shared-Private Disentanglement vs. Entangled Latent Representation)
     * $RQ_4$ (Homoscedastic Uncertainty MTL vs. Fixed Loss Weighting)
     * $RQ_5$ (Subject-Independent LOSO Generalization vs. Subject-Dependent Splits)
     * $RQ_6$ (Missing-Modality Knowledge Distillation vs. Standard Sensor Dependency)

2. FORMAL STATISTICAL HYPOTHESES ($H_0$ and $H_1$):
   - State the Null Hypothesis ($H_0$) and Alternative Hypothesis ($H_1$) corresponding to the chosen RQ.
   - Define the quantitative metric and statistical threshold for rejecting $H_0$ (e.g., Wilcoxon signed-rank test, $p < 0.05$, Cohen's $d > 0.5$).
```

---

### PROMPT 25 — Experimental Verification & Protocol Design (P7)

```markdown
You are a scientific literature analysis assistant for the PhD research project: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Analyze the experimental design of the paper: "[INSERT PAPER TITLE OR PAPER ID]".

Perform TASK 25 — EXPERIMENTAL VERIFICATION & PROTOCOL DESIGN:
Design an end-to-end, rigorous experimental protocol to empirically validate our proposed hypotheses against the benchmarks in this paper:

1. BENCHMARK DATASET & ANTI-LEAKAGE SELECTION:
   - Target Datasets: DEAP, SEED, DREAMER, AMIGOS, or WESAD.
   - Exact Splitting Protocol: Strict Leave-One-Subject-Out (LOSO) cross-subject cross-validation.
   - Anti-Leakage Rules: Preprocessing and Z-score normalization strictly fit on training folds only; trial-level windowing without temporal shuffling.

2. CONTROLLED ABLATION SUITE DESIGN:
   - Specify the ablation configurations required to isolate individual mechanisms (e.g., Unimodal EEG, Unimodal ECG/EDA, Early Fusion, Without Disentanglement, Without Cross-Attention, Without Uncertainty Loss).

3. MISSING MODALITY & STRESS-TESTING PROTOCOL:
   - Progressive sensor dropout evaluation (Drop 25%, 50%, 75%, 100% of peripheral or EEG channels) comparing baseline vs Teacher-Student Knowledge Distillation.

4. STATISTICAL VALIDATION PROTOCOL:
   - Metric definitions: Balanced Accuracy, Macro-F1, Pearson $r$, Concordance Correlation Coefficient (CCC).
   - Statistical Tests: 1000-iteration Bootstrap 95% BCa Confidence Intervals, Wilcoxon Paired Signed-Rank Test with Holm-Bonferroni correction ($\alpha = 0.05$).
```

---

### PROMPT 26 — Research Decision Map Synthesis (P8)

```markdown
You are a scientific literature analysis assistant for the PhD research project: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Analyze the paper: "[INSERT PAPER TITLE OR PAPER ID]" and synthesize findings into an executive Research Decision Map complying with Rule 23 of `AGENTS.md`.

Perform TASK 26 — RESEARCH DECISION MAP SYNTHESIS:
Synthesize an executive decision matrix structured exactly as follows:

1. EVIDENCE BASE:
   - What concrete empirical results from this paper justify our architectural choices (Multi-Branch, Disentanglement, Cross-Attention, MTL)?

2. TECHNICAL ALTERNATIVES:
   - What competing baseline algorithms or fusion mechanisms exist as valid alternatives?

3. METHODOLOGICAL TRADE-OFFS:
   - Model complexity vs. Classification accuracy.
   - Parameter count vs. Real-time edge latency.
   - Training stability of Disentanglement vs. Standard cross-entropy.

4. SCIENTIFIC & EXPERIMENTAL RISKS:
   - What potential failure modes (e.g., negative transfer, gradient explosion, sensor artifact dominance) must be mitigated?

5. CONCRETE EXPERIMENTAL ACTION PLAN:
   - What is the immediate next experimental step for the PhD dissertation based on this analysis?
```

---

## ⚡ APPENDIX — All-in-One Master Deep Extraction Prompt

*(Use this prompt if you want NotebookLM to extract all 26 dimensions in a single comprehensive pass)*

```markdown
You are a scientific literature analysis assistant for the PhD research project: "Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals".

Analyze the paper: "[INSERT PAPER TITLE OR PAPER ID]" using ONLY the uploaded sources. Do not hallucinate. Label all findings as [EXPLICIT], [SUPPORTED], [INFERRED], or [UNKNOWN], and adhere to the evaluation chain: METHOD → DATASET → PROTOCOL → METRIC → RESULT.

Generate a comprehensive academic extraction report following this structured template:

# SCIENTIFIC ANALYSIS REPORT: [INSERT PAPER TITLE OR PAPER ID]

## 1. IDENTITY & RESEARCH PROBLEM (Tasks 1 & 2)
- Title, Authors, Year, Venue, DOI.
- Core research problem, claimed scientific contributions, and dataset specification.

## 2. PREPROCESSING & DATA LEAKAGE AUDIT (Tasks 3, 4, 17)
- Preprocessing protocol, filter parameters, and feature representations.
- Data partitioning (Subject-Dependent vs LOSO) and 8-Dimensional Anti-Leakage Audit.

## 3. ARCHITECTURE, MULTI-BRANCH & FUSION (Tasks 5, 6, 7, 8)
- End-to-end tensor flow, dedicated multi-branch structure, and physics-informed justification.
- Multimodal fusion mechanism (Cross-Modal QKV Attention) and Multi-Task loss formulation.

## 4. EXPERIMENTAL RESULTS, ABLATION & EFFICIENCY (Tasks 9, 10, 11, 12, 13, 14)
- Comparative Baselines Matrix and exact quantitative metrics (Mean ± Std, p-values, CI).
- Ablation study findings (Component removed, Full vs Ablated, Δ difference).
- Generalization (LOSO), Robustness (Missing Modalities), and Computational Cost (Params, Latency).

## 5. RESEARCH GAPS, NOVELTY & LIMITATIONS (Tasks 15, 16, 18, 21, 22)
- Explicit author-stated future directions and methodological gaps.
- Novelty Collision Check (Has Multi-Task + Multi-Branch + Multimodal been done?).
- Scientific Evidence Table and Reproducibility rating (HIGH/MED/LOW).

## 6. PHD DISSERTATION ROADMAP & DECISION MAP (Tasks 19, 20, 23, 24, 25, 26)
- 18-point standardized summary and 7-dimensional relevance scoring.
- Translation into Formal Research Questions ($RQ_1$–$RQ_6$) and Hypotheses ($H_1$–$H_6$).
- Experimental validation blueprint (LOSO, 10 Ablation configurations, Wilcoxon + Holm-Bonferroni).
- Executive Research Decision Map (Evidence, Alternatives, Trade-offs, Risks, and Action Plan).
```
