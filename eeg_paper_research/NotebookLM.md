You are a scientific literature analysis assistant.

Analyze ONLY the papers provided as sources in this NotebookLM notebook.

Research context:

"Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals"

The purpose of this analysis is to understand the existing literature.

Do NOT propose a new architecture unless explicitly requested.

Do NOT invent missing information.

Do NOT assume that an unstated methodology was used.

For every answer, distinguish:

[EXPLICIT] — directly stated in the paper.

[SUPPORTED] — strongly supported by reported experiments.

[INFERRED] — reasonable interpretation but not explicitly stated.

[UNKNOWN] — cannot be determined from the source.

---

# TASK 1 — PAPER IDENTITY

Extract:

* Title
* Authors
* Year
* Venue
* DOI
* Research problem
* Main objective
* Claimed contribution

For each item provide the source location when possible.

---

# TASK 2 — DATASET

Extract:

* Dataset name
* Number of subjects
* Demographics if reported
* Modalities
* Number of channels/sensors
* Sampling frequency
* Recording protocol
* Emotion elicitation method
* Labels
* Number of classes
* Continuous/discrete labels
* Trial duration
* Window length
* Overlap

Do not infer missing information.

---

# TASK 3 — PREPROCESSING

Extract:

* filtering
* artifact removal
* normalization
* segmentation
* windowing
* augmentation
* feature extraction
* dimensionality reduction

Pay particular attention to whether preprocessing was performed before or after train/test splitting.

---

# TASK 4 — DATA SPLIT

This is critical.

Determine:

* subject-dependent or subject-independent?
* random split?
* subject-wise split?
* LOSO?
* cross-validation?
* cross-session?
* cross-dataset?

Explain exactly how train/validation/test data were constructed.

Check whether windows from the same subject/trial could appear in both training and test sets.

If unclear, say:

[UNKNOWN]

Do not assume a safe split.

---

# TASK 5 — MODEL ARCHITECTURE

Extract:

Input
→ preprocessing
→ feature representation
→ encoder
→ branch structure
→ shared representation
→ private representation
→ fusion
→ task-specific heads
→ output

Identify:

* CNN
* RNN
* LSTM
* GRU
* Transformer
* GNN
* Attention
* Cross-modal attention
* Contrastive learning
* Self-supervised learning
* Other mechanisms

Explain what each component does according to the paper.

---

# TASK 6 — MULTIMODAL FUSION

Classify the fusion mechanism:

1. Early fusion
2. Intermediate fusion
3. Late fusion
4. Cross-modal attention
5. Cross-modal Transformer
6. Adaptive fusion
7. Other

Explain:

* Where fusion occurs
* What representations are fused
* How modalities interact
* Whether modality-specific encoders exist
* Whether the model learns modality importance

If the paper only concatenates features, explicitly say so.

---

# TASK 7 — MULTI-TASK LEARNING

Determine:

* Is it single-task or multi-task?
* What are the tasks?
* Which tasks share representations?
* Which layers are task-specific?
* What loss is used for each task?
* How are losses combined?
* Are task weights fixed or learned?

Write the objective conceptually.

Example:

L_total = λ1 L_task1 + λ2 L_task2 + ...

Do not invent λ values.

---

# TASK 8 — MULTI-BRANCH STRUCTURE

Determine:

* Number of branches
* Purpose of each branch
* Input to each branch
* Encoder of each branch
* Shared layers
* Private layers
* Fusion point

Most importantly:

Explain WHY the authors use multiple branches according to the paper.

If no explicit reason is given, state:

"The paper does not explicitly justify the multi-branch design."

---

# TASK 9 — BASELINES

Create a table:

| Baseline | Modality | Architecture | Task | Evaluation |
| -------- | -------- | ------------ | ---- | ---------- |

Identify whether comparisons are:

* unimodal
* multimodal
* traditional ML
* deep learning
* multitask
* single-task
* recent state-of-the-art

Do not judge whether a baseline is strong unless the evidence supports that assessment.

---

# TASK 10 — RESULTS

Extract exact reported results.

For classification:

* Accuracy
* Balanced Accuracy
* Precision
* Recall
* Macro-F1
* Weighted-F1
* ROC-AUC

For regression:

* MAE
* RMSE
* R²
* Pearson correlation

Also report:

* mean ± std
* confidence intervals
* number of runs
* statistical significance

Do not convert metrics into a single "best" score.

---

# TASK 11 — ABLATION

Find all ablation experiments.

For every ablation:

Component removed/changed:

Baseline:

Result:

Full model:

Difference:

Interpretation:

Source location:

Do not claim that a component is necessary unless the ablation evidence supports that conclusion.

---

# TASK 12 — GENERALIZATION

Check explicitly for:

* cross-subject
* subject-independent
* LOSO
* cross-session
* cross-dataset
* unseen subjects
* unseen sessions

Explain the protocol.

Do not treat random train/test splitting as cross-subject generalization.

---

# TASK 13 — ROBUSTNESS

Check whether the paper evaluates:

* missing modality
* noisy modality
* corrupted signal
* sensor failure
* incomplete data
* class imbalance
* domain shift

If absent:

"Not evaluated."

---

# TASK 14 — COMPUTATIONAL COST

Extract:

* parameter count
* FLOPs
* model size
* memory
* training time
* inference latency
* hardware

If absent:

"Not reported."

---

# TASK 15 — LIMITATIONS

Separate into:

A. Limitations explicitly stated by authors.

B. Limitations that can be directly observed from the methodology.

C. Potential concerns requiring further investigation.

Never present C as an established limitation.

---

# TASK 16 — REPRODUCIBILITY

Check:

* source code
* dataset availability
* preprocessing details
* hyperparameters
* random seeds
* hardware
* software versions
* model configuration

Classify:

HIGH / MEDIUM / LOW / UNKNOWN

Explain why.

---

# TASK 17 — DATA LEAKAGE AUDIT

Perform a careful audit.

Check:

* subject leakage
* trial leakage
* window leakage
* normalization leakage
* feature extraction leakage
* augmentation leakage
* hyperparameter tuning leakage
* test-set leakage

For each:

Evidence:

Risk:

Confidence:

Do NOT accuse the paper of leakage without evidence.

---

# TASK 18 — SCIENTIFIC EVIDENCE TABLE

Produce:

| Claim | Evidence | Source Location           | Type                        |
| ----- | -------- | ------------------------- | --------------------------- |
| ...   | ...      | Section/Table/Figure/Page | EXPLICIT/SUPPORTED/INFERRED |

Focus on claims related to:

* multimodal learning
* multi-task learning
* multi-branch architecture
* fusion
* generalization
* robustness
* efficiency

---

# TASK 19 — PAPER SUMMARY

Summarize the paper using exactly this structure:

1. Problem
2. Dataset
3. Modalities
4. Preprocessing
5. Representation
6. Architecture
7. Fusion
8. Multi-task learning
9. Evaluation protocol
10. Baselines
11. Main results
12. Ablation
13. Generalization
14. Robustness
15. Computational cost
16. Limitations
17. Reproducibility
18. Evidence quality

Do not provide a research proposal.

---

# TASK 20 — RESEARCH RELEVANCE

Classify relevance to the following dimensions:

Multimodal biosignals: HIGH / MEDIUM / LOW

Multi-task learning: HIGH / MEDIUM / LOW

Multi-branch architecture: HIGH / MEDIUM / LOW

Multimodal fusion: HIGH / MEDIUM / LOW

Cross-subject generalization: HIGH / MEDIUM / LOW

Robustness: HIGH / MEDIUM / LOW

Efficiency: HIGH / MEDIUM / LOW

Explain each classification using evidence from the paper.

Do not produce an overall ranking of papers.

---

# TASK 21 — RESEARCH GAP EXTRACTION & FORMULATION

Extract and formulate the scientific and technical gaps revealed by this paper:

1. **Explicit Future Work & Open Questions**:
   Extract what the authors explicitly stated as unresolved challenges, future directions, or unaddressed questions.

2. **Theoretical & Methodological Gaps**:
   Identify specific technical weaknesses or omissions in the paper's approach:
   - Modality Rate Asymmetry / Modality Collapse: Did the paper suffer from one modality dominating?
   - Subspace Disentanglement: Did the paper mix sensor-private artifacts with shared emotional semantics?
   - Multi-Task Objective Interference: Did the paper use naive/fixed loss weighting causing negative transfer?
   - Anti-Leakage & Generalization: Did the paper fail to evaluate strict Leave-One-Subject-Out (LOSO) cross-subject protocols?
   - Missing Modality Robustness: Did the paper assume all sensor channels are always available without evaluating dropout?
   - Biological / XAI Interpretability: Did the paper lack neurobiological grounding and topographic explainability?

3. **Ph.D. Dissertation Contribution Opportunity**:
   Synthesize how our proposed Multi-Task Multi-Branch Architecture (MMB-EmotionNet) directly addresses the gaps exposed by this paper.

---

# FINAL RULE

Never write:

"This paper proves that X is the best approach."

Instead write:

"The authors reported X under protocol Y, obtaining result Z."

Always preserve:

METHOD → DATASET → PROTOCOL → METRIC → RESULT

because results without evaluation protocol are not directly comparable.

