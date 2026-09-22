# Phase P4: Research Questions & Hypotheses Formulation

**Project**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Working Title**: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức  
**Phase**: P4 — Research Questions & Hypotheses Formulation  
**Last Updated**: 2026-09-22  
**Status**: Formal Statistical Hypotheses & Falsification Protocols Grounded in P1–P3 Evidence  

---

## 1. Methodological Principles & Statistical Rigor

In accordance with **Section 4, 15, and 16 of `AGENTS.md`**, every research question in this doctoral project must satisfy three formal scientific criteria:
1. **Literature-Grounded**: Emerge directly from empirical evidence and identified literature gaps ([`research/08-research-gaps.md`](file:///d:/ntk/eeg_paper_research/research/08-research-gaps.md)).
2. **Statistically Testable & Falsifiable**: Defined through formal paired Null ($H_0$) and Alternative ($H_1$) hypotheses with predefined statistical rejection thresholds ($p < 0.05$ with False Discovery Rate [FDR] / Bonferroni correction, Cohen's $d \ge 0.5$).
3. **Reproducible & Controlled**: Evaluated under identical, leak-free benchmarking protocols with fixed random seeds ($N_{seeds} \ge 5$) across multiple subjects and folds.

---

## 2. Research Questions & Hypotheses Formulation

---

### Research Question 1 (RQ1): Multimodal Complementarity
> **RQ1**: *Does the joint fusion of central nervous system signals (EEG) and autonomic peripheral biosignals (ECG, EDA, Respiration) improve emotion recognition performance compared with single-modality baseline models under strict, leak-free evaluation?*

- **Literature Grounding**: Addresses **Gap 1**. Biological emotion evokes both cortical cognitive appraisal (EEG) and autonomic physiological arousal (ECG/EDA) ([`P0001`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0001.md), [`P0014`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0014.md), [`P0030`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0030.md)).
- **Formal Hypotheses**:
  - **Null Hypothesis ($H_0^{(1)}$)**: Multimodal biosignal models yield equal or lower classification performance compared to the best unimodal baseline:
    $$H_0^{(1)}: \mu(\text{Macro-F1}_{\text{multimodal}}) \le \mu(\text{Macro-F1}_{\text{best\_unimodal}})$$
  - **Alternative Hypothesis ($H_1^{(1)}$)**: Multimodal biosignal fusion yields a statistically significant increase in classification performance over any single modality:
    $$H_1^{(1)}: \mu(\text{Macro-F1}_{\text{multimodal}}) > \mu(\text{Macro-F1}_{\text{best\_unimodal}})$$
- **Falsification Criteria**: Reject $H_1^{(1)}$ if paired Wilcoxon signed-rank test yields $p \ge 0.05$ or Cohen's $d < 0.3$ across subject test folds.
- **Evaluation Settings & Metrics**:
  - Datasets: DEAP (32 subjects), DREAMER (23 subjects), AMIGOS (40 subjects).
  - Metrics: Macro-F1 score, Balanced Accuracy, Confusion Matrices.
  - Statistical Test: Two-sided paired Wilcoxon signed-rank test across participants.

---

### Research Question 2 (RQ2): Multi-Branch Dedicated Encoding vs. Monolithic Encoding
> **RQ2**: *Does a multi-branch architecture with dedicated modality-specific encoders tailored to signal physics improve latent representation quality and affective decoding compared with a monolithic multi-channel encoder?*

- **Literature Grounding**: Addresses **Gap 1 & Gap 2**. EEG signals (microvolt potential oscillations across 3D scalp coordinates) and peripheral signals (slow tonic/phasic sweat and cardiac intervals) possess distinct temporal frequencies and physical scales ([`P0005`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0005.md), [`P0007`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0007.md), [`P0015`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0015.md)).
- **Formal Hypotheses**:
  - **Null Hypothesis ($H_0^{(2)}$)**: A dedicated multi-branch encoder architecture achieves equivalent or inferior performance compared to a parameter-matched monolithic encoder:
    $$H_0^{(2)}: \mu(\text{Acc}_{\text{multi\_branch}}) \le \mu(\text{Acc}_{\text{monolithic}})$$
  - **Alternative Hypothesis ($H_1^{(2)}$)**: Dedicated multi-branch encoders achieve statistically superior decoding accuracy and faster optimization convergence:
    $$H_1^{(2)}: \mu(\text{Acc}_{\text{multi\_branch}}) > \mu(\text{Acc}_{\text{monolithic}})$$
- **Falsification Criteria**: Reject $H_1^{(2)}$ if the performance difference between multi-branch and monolithic networks is statistically insignificant ($p \ge 0.05$) under identical parameter budgets.
- **Evaluation Settings & Metrics**:
  - Datasets: DEAP, DREAMER.
  - Baselines: Monolithic 1D-CNN, Monolithic MLP, Parameter-Matched Multi-Branch Network.
  - Metrics: Accuracy, Macro-F1, Training Epochs to Convergence.

---

### Research Question 3 (RQ3): Shared-Private Subspace Disentanglement
> **RQ3**: *Does explicit orthogonal shared-private subspace disentanglement prevent modality sensor noise from corrupting the shared emotion manifold and outperform standard intermediate feature concatenation?*

- **Literature Grounding**: Addresses **Gap 2**. Biosignal modalities contain both emotion-invariant shared semantics (sympathetic arousal, hedonic valence) and sensor-private artifacts (ocular blinks, sweat drift, electrode impedance shifts) ([`P0003`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0003.md), [`P0022`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0022.md), [`P0027`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0027.md)).
- **Formal Hypotheses**:
  - **Null Hypothesis ($H_0^{(3)}$)**: Incorporating shared-private similarity ($\mathcal{L}_{sim}$) and orthogonality difference ($\mathcal{L}_{diff}$) losses does not improve emotion recognition accuracy over unconstrained latent concatenation ($\mathcal{L}_{task}$ only):
    $$H_0^{(3)}: \mu(\text{F1}_{\text{disentangled}}) \le \mu(\text{F1}_{\text{unconstrained\_concat}})$$
  - **Alternative Hypothesis ($H_1^{(3)}$)**: Orthogonal shared-private disentanglement yields a statistically significant increase in classification performance and reduces latent cross-modal correlation redundancy:
    $$H_1^{(3)}: \mu(\text{F1}_{\text{disentangled}}) > \mu(\text{F1}_{\text{unconstrained\_concat}})$$
- **Falsification Criteria**: Reject $H_1^{(3)}$ if ablation of $\mathcal{L}_{sim}$ and $\mathcal{L}_{diff}$ causes no statistically significant drop in test F1 ($p \ge 0.05$) or if the measured Frobenius orthogonality $\|\mathbf{S}_m^T \mathbf{P}_m\|_F$ does not decrease.
- **Evaluation Settings & Metrics**:
  - Datasets: DEAP, DREAMER, SEED-IV.
  - Metrics: Macro-F1, Reconstruction Error, Subspace Orthogonality Metric $\|\mathbf{S}_m^T \mathbf{P}_m\|_F^2$.

---

### Research Question 4 (RQ4): Multi-Task Uncertainty Loss Balancing
> **RQ4**: *Does dynamic homoscedastic uncertainty loss balancing resolve gradient conflict and mitigate negative transfer when jointly optimizing continuous regression (Valence, Arousal) and discrete emotion classification?*

- **Literature Grounding**: Addresses **Gap 3**. Emotion consists of continuous dimensional activation and discrete categorical states ([`P0028`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0028.md), [`P0029`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0029.md)). Fixed loss weighting causes gradient magnitude mismatch between MSE and Cross-Entropy ([`P0008`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0008.md)).
- **Formal Hypotheses**:
  - **Null Hypothesis ($H_0^{(4)}$)**: Multi-task training with dynamic uncertainty loss weighting achieves equivalent or higher total error (or lower joint F1) compared to separate single-task models:
    $$H_0^{(4)}: \mu(\text{Joint\_Score}_{\text{dynamic\_MTL}}) \le \mu(\text{Joint\_Score}_{\text{single\_tasks}})$$
  - **Alternative Hypothesis ($H_1^{(4)}$)**: Dynamic uncertainty loss weighting outperforms both isolated single-task models and fixed-weight multi-task models by eliminating negative transfer:
    $$H_1^{(4)}: \mu(\text{Joint\_Score}_{\text{dynamic\_MTL}}) > \mu(\text{Joint\_Score}_{\text{fixed\_MTL}})$$
- **Falsification Criteria**: Reject $H_1^{(4)}$ if dynamic loss balancing produces lower joint accuracy than fixed hyperparameter grid search or fails to achieve negative transfer ratios $< 0$.
- **Evaluation Settings & Metrics**:
  - Datasets: DEAP (Valence Reg + Arousal Reg + Dominance Reg), AMIGOS (Continuous V/A + 7 Discrete Categories).
  - Metrics: Root Mean Square Error (RMSE), Pearson's $r$, Classification Macro-F1, Negative Transfer Ratio $\Delta_{MTL} = \frac{1}{T}\sum_{t=1}^T \frac{M_{MTL, t} - M_{STL, t}}{M_{STL, t}}$.

---

### Research Question 5 (RQ5): Cross-Subject Generalization & Domain Adaptation
> **RQ5**: *Can domain-invariant representation learning (via adversarial domain alignment) significantly narrow the performance gap between subject-dependent and subject-independent (LOSO) benchmarks?*

- **Literature Grounding**: Addresses **Gap 5**. High inter-subject physiological variability causes severe performance drops under Leave-One-Subject-Out (LOSO) validation ([`P0001`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0001.md), [`P0007`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0007.md), [`P0021`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0021.md), [`P0030`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0030.md)).
- **Formal Hypotheses**:
  - **Null Hypothesis ($H_0^{(5)}$)**: Incorporating adversarial domain adaptation (GRL) yields no statistically significant improvement in target subject decoding accuracy under LOSO validation:
    $$H_0^{(5)}: \mu(\text{Acc}_{\text{LOSO\_adapted}}) \le \mu(\text{Acc}_{\text{LOSO\_unadapted}})$$
  - **Alternative Hypothesis ($H_1^{(5)}$)**: Adversarial domain alignment achieves a statistically significant accuracy increase on unseen target subjects in LOSO:
    $$H_1^{(5)}: \mu(\text{Acc}_{\text{LOSO\_adapted}}) > \mu(\text{Acc}_{\text{LOSO\_unadapted}})$$
- **Falsification Criteria**: Reject $H_1^{(5)}$ if domain adaptation produces an accuracy increase of $< 3.0\%$ or if the gain is not statistically significant ($p \ge 0.05$) across the participant cohort.
- **Evaluation Settings & Metrics**:
  - Datasets: SEED (15 subjects), DEAP (32 subjects).
  - Protocol: Strict Leave-One-Subject-Out (LOSO) Cross-Validation.
  - Metrics: LOSO Accuracy, Balanced Accuracy, Target Domain Maximum Mean Discrepancy (MMD).

---

### Research Question 6 (RQ6): Graceful Degradation Under Missing Modalities
> **RQ6**: *Does the integration of modality dropout during training and cross-modal latent reconstruction enable the architecture to maintain robust inference when primary biosignals (e.g. EEG) are completely missing or detached?*

- **Literature Grounding**: Addresses **Gap 4**. Wearable sensors frequently detach or drop channels in real-world scenarios ([`P0015`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0015.md), [`P0019`](file:///d:/ntk/eeg_paper_research/literature/03_notes/P0019.md)).
- **Formal Hypotheses**:
  - **Null Hypothesis ($H_0^{(6)}$)**: Under complete omission of the EEG modality at inference time, the proposed reconstruction architecture performs no better than a model evaluated on raw zero-padded inputs:
    $$H_0^{(6)}: \mu(\text{Acc}_{\text{missing\_EEG\_reconstructed}}) \le \mu(\text{Acc}_{\text{missing\_EEG\_zero\_padded}})$$
  - **Alternative Hypothesis ($H_1^{(6)}$)**: The latent reconstruction mechanism preserves a statistically significant portion of full multimodal performance ($>85\%$ accuracy retention) when EEG is missing:
    $$H_1^{(6)}: \mu(\text{Acc}_{\text{missing\_EEG\_reconstructed}}) > \mu(\text{Acc}_{\text{missing\_EEG\_zero\_padded}})$$
- **Falsification Criteria**: Reject $H_1^{(6)}$ if zero-shot modality dropping results in catastrophic performance drop to chance level without significant difference from zero-padding baseline.
- **Evaluation Settings & Metrics**:
  - Datasets: DEAP, DREAMER.
  - Missingness Stress-Testing Scenarios: (1) EEG dropped 100%, (2) ECG dropped 100%, (3) EDA dropped 100%, (4) Random modality dropout $p \in \{0.2, 0.4, 0.6, 0.8\}$.
  - Metrics: Relative Accuracy Retention Rate $\frac{\text{Acc}_{\text{missing}}}{\text{Acc}_{\text{full}}}$, Macro-F1.

---

## 3. Summary Mapping of Hypotheses to Research Lifecycle

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 DOCTORAL HYPOTHESIS MAP                                │
├────────────┬─────────────────────────────┬───────────────────────────┬─────────────────┤
│ Hypothesis │ Primary Research Focus      │ Proposed Mechanism        │ Benchmark Target│
├────────────┼─────────────────────────────┼───────────────────────────┼─────────────────┤
│ H1 (RQ1)   │ Multimodal Complementarity  │ Cross-Modal Attention QKV │ DEAP / DREAMER  │
│ H2 (RQ2)   │ Multi-Branch Architecture   │ EEGNet + 1D-CNN Encoders  │ DEAP / DREAMER  │
│ H3 (RQ3)   │ Shared-Private Disentangle  │ CMD (Sim) + Orthog (Diff) │ DEAP / SEED-IV  │
│ H4 (RQ4)   │ Multi-Task Loss Balancing   │ Homoscedastic Uncertainty │ DEAP / AMIGOS   │
│ H5 (RQ5)   │ Cross-Subject Generalization│ Adversarial GRL Alignment │ SEED / DEAP     │
│ H6 (RQ6)   │ Missing Modality Robustness │ Modality Dropout + Recon  │ DEAP / DREAMER  │
└────────────┴─────────────────────────────┴───────────────────────────┴─────────────────┘
```

---

## 4. Synthesis & Transition to Phase P5

All six research questions are now grounded in empirical literature and formal mathematical hypotheses. The project is ready to proceed to **Phase P5: Dataset Selection & Preprocessing Protocol** to formalize the exact data pipelines, signal filtering, electrode montages, and data leakage audits.
