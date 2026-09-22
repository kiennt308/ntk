# Phase P8: Ablation Study Protocol

**Project**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Working Title**: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức  
**Phase**: P8 — Component-Level, Loss-Level, and Modality Ablation Protocol  
**Last Updated**: 2026-09-22  
**Status**: Formal Specification of 10 Controlled Ablation Experiments Complete  

---

## 1. Ablation Policy & Methodological Principles

In strict compliance with **Section 10 and 18 of `AGENTS.md`**, every architectural component in the proposed **MMB-EmotionNet** must have an empirical and scientific justification:
1. **Isolated Variable Manipulation**: Exactly one architectural module, loss term, or modality subset is modified per ablation experiment while holding all other parameters, random seeds ($N_{seeds} = 5$), and preprocessing pipelines strictly constant.
2. **Statistical Rigor**: Performance deltas are evaluated via two-tailed paired Wilcoxon signed-rank tests with Holm-Bonferroni correction ($p < 0.05$, Cohen's $d$) across all test folds.
3. **Negative Result Documentation**: If an ablation reveals that removing a component improves performance or has no significant effect, the hypothesis for that component is formally rejected in accordance with Section 19 of `AGENTS.md`.

---

## 2. Master Ablation Matrix

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                           MASTER ABLATION EXPERIMENTS MATRIX                                     │
├────────────┬───────────────────────────────┬───────────────────────────────┬─────────────────────────────────────┤
│ Exp ID     │ Target Component Tested       │ Architectural Modification    │ Scientific Question Addressed       │
├────────────┼───────────────────────────────┼───────────────────────────────┼─────────────────────────────────────┤
│ EXP-ABL-00 │ Full MMB-EmotionNet (Anchor)  │ Unmodified Complete Model     │ Benchmark upper-bound performance   │
│ EXP-ABL-01 │ Shared-Private Disentangle    │ Set α = 0, β = 0, γ = 0       │ Does disentanglement prevent noise? │
│ EXP-ABL-02 │ Difference/Orthogonality Loss │ Set β = 0 (No orthogonality)  │ Does orthogonality isolate sensors? │
│ EXP-ABL-03 │ Similarity Loss (CMD/MMD)     │ Set α = 0 (No shared align)   │ Does shared alignment aid fusion?   │
│ EXP-ABL-04 │ Reconstruction Loss (L_recon) │ Set γ = 0 (No decoder recon)  │ Does recon prevent latent collapse? │
│ EXP-ABL-05 │ Cross-Modal Attention (MulT)  │ Replaced by Flat Concatenation│ Does attention beat concatenation?  │
│ EXP-ABL-06 │ Dynamic Uncertainty MTL       │ Fixed static weights (λ=1.0)  │ Does uncertainty prevent conflict?  │
│ EXP-ABL-07 │ Multi-Branch Dedicated Struct │ Monolithic Multi-Channel CNN  │ Do dedicated branches beat mono?    │
│ EXP-ABL-08 │ Adversarial Domain Head (GRL) │ Set δ = 0 (No GRL domain loss)│ Does GRL improve LOSO adaptation?   │
│ EXP-ABL-09 │ Sensor Modality Subsets       │ Single & Dual Modality Runs   │ What is the marginal contribution?  │
│ EXP-ABL-10 │ Missing Modality Imputation   │ Zero-Padding vs. Recon Impute │ Is cross-modal routing robust?      │
└────────────┴───────────────────────────────┴───────────────────────────────┴─────────────────────────────────────┤
```

---

## 3. Detailed Controlled Ablation Experiment Specifications

---

### Experiment ABL-01: Contribution of Full Shared-Private Disentanglement
- **Experiment ID**: `EXP-ABL-01`
- **Component Tested**: Subspace Disentanglement Module (Stage 2).
- **Modification**: Remove similarity, difference, and reconstruction losses by setting $\alpha = 0, \beta = 0, \gamma = 0$. Latent branch representations $\mathbf{h}_m$ are fed directly into the cross-modal attention block without shared-private separation.
- **Scientific Rationale**: Tests **RQ3** ($H_1^{(3)}$). Determines whether explicitly decomposing representations into shared emotion and private sensor spaces outperforms unconstrained latent feature learning.
- **Expected Outcome**: Test Macro-F1 is expected to drop by $\approx 2.5\%–4.0\%$ due to private sensor noise (sweat baseline drift, ocular potentials) leaking into the fused classifier.
- **Diagnostic Metric**: Subspace cross-correlation redundancy and test Macro-F1.

---

### Experiment ABL-02: Contribution of Soft Orthogonality Difference Loss ($\mathcal{L}_{diff}$)
- **Experiment ID**: `EXP-ABL-02`
- **Component Tested**: Orthogonality constraint between shared and private spaces.
- **Modification**: Set $\beta = 0$ while retaining $\alpha = 0.05, \gamma = 0.1$.
- **Scientific Rationale**: Determines whether the soft Frobenius orthogonality penalty $\|\mathbf{S}_m^T \mathbf{P}_m\|_F^2$ is necessary to prevent the shared subspace from redundantly encoding private sensor dynamics.
- **Expected Outcome**: Without $\mathcal{L}_{diff}$, the shared space $\mathbf{s}_m$ and private space $\mathbf{p}_m$ will exhibit high cross-correlation ($r > 0.60$), diminishing the benefits of separate private routing.
- **Diagnostic Metric**: Frobenius norm of cross-subspace correlation matrix $\|\mathbf{S}_m^T \mathbf{P}_m\|_F$.

---

### Experiment ABL-03: Contribution of Shared Distribution Similarity Loss ($\mathcal{L}_{sim}$)
- **Experiment ID**: `EXP-ABL-03`
- **Component Tested**: Central Moment Discrepancy (CMD) alignment across modalities.
- **Modification**: Set $\alpha = 0$ while retaining $\beta = 0.01, \gamma = 0.1$.
- **Scientific Rationale**: Verifies whether explicitly penalizing statistical moment discrepancies between $\mathbf{s}_{eeg}, \mathbf{s}_{ecg}, \mathbf{s}_{eda}$ aligns the cross-modal emotional manifold into a unified metric space.
- **Expected Outcome**: Cross-modal attention efficiency degrades, dropping continuous Valence/Arousal Pearson correlation $r$.

---

### Experiment ABL-04: Contribution of Latent Reconstruction Loss ($\mathcal{L}_{recon}$)
- **Experiment ID**: `EXP-ABL-04`
- **Component Tested**: Modality Decoders $D_m([\mathbf{s}_m; \mathbf{p}_m])$.
- **Modification**: Set $\gamma = 0$, removing decoders during training.
- **Scientific Rationale**: Verifies that the information bottleneck preserves complete physiological signal content and prevents trivial constant representations.
- **Expected Outcome**: Slight decrease in classification accuracy under complete cases; severe failure during missing-modality imputation.

---

### Experiment ABL-05: Contribution of Directional Cross-Modal Attention (MulT)
- **Experiment ID**: `EXP-ABL-05`
- **Component Tested**: Directional Query-Key-Value Attention Blocks (Stage 3).
- **Modification**: Replace cross-modal attention blocks $\mathbf{z}_{eeg \leftarrow eda}$ and $\mathbf{z}_{ecg \leftarrow eeg}$ with simple element-wise concatenation $[\mathbf{s}_{eeg}; \mathbf{s}_{ecg}; \mathbf{s}_{eda}]$ followed by a linear projection.
- **Scientific Rationale**: Tests **RQ1 & RQ2**. Determines whether non-linear directional attention (where autonomic EDA/ECG modulates cortical EEG attention) is superior to static feature concatenation.
- **Expected Outcome**: Performance drops significantly on Arousal decoding (where autonomic modulation is critical), dropping Macro-F1 by $\approx 3.0\%–5.0\%$.

---

### Experiment ABL-06: Contribution of Dynamic Homoscedastic Uncertainty Loss Balancing
- **Experiment ID**: `EXP-ABL-06`
- **Component Tested**: Multi-Task Loss Balancing (Stage 5).
- **Modification**: Replace learnable homoscedastic parameters $(\sigma_v, \sigma_a, \sigma_c)$ with:
  1. Static Equal Weights: $\lambda_1 = 1.0, \lambda_2 = 1.0, \lambda_3 = 1.0$.
  2. Static Grid-Searched Weights: $\lambda_1 = 0.5, \lambda_2 = 0.5, \lambda_3 = 1.0$.
- **Scientific Rationale**: Tests **RQ4** ($H_1^{(4)}$). Evaluates whether dynamic gradient scale balancing eliminates destructive gradient interference (negative transfer) between continuous regression (MSE) and discrete classification (Cross-Entropy).
- **Expected Outcome**: Fixed static weights result in negative transfer ($\Delta_{MTL} < 0$), with discrete classification gradients dominating and increasing Valence/Arousal RMSE by $>15\%$.

---

### Experiment ABL-07: Contribution of Dedicated Multi-Branch Encoders vs. Monolithic Encoder
- **Experiment ID**: `EXP-ABL-07`
- **Component Tested**: Modality-Specific Encoders (Stage 1).
- **Modification**: Replace dedicated EEGNet and Dilated 1D-CNN branches with a single parameter-matched Monolithic 2D-CNN processing all 35 stacked channels uniformly.
- **Scientific Rationale**: Tests **RQ2** ($H_1^{(2)}$). Separates architectural inductive bias from parameter volume.
- **Expected Outcome**: Monolithic network exhibits slower convergence, higher training loss variance, and lower test F1 ($\approx 4.0\%–6.0\%$ drop).

---

### Experiment ABL-08: Contribution of Adversarial Domain Alignment (GRL)
- **Experiment ID**: `EXP-ABL-08`
- **Component Tested**: Adversarial Domain Discriminator with Gradient Reversal Layer.
- **Modification**: Set $\delta = 0$, training without domain loss $\mathcal{L}_{domain}$.
- **Scientific Rationale**: Tests **RQ5** ($H_1^{(5)}$). Measures the exact cross-subject generalization gain attributable to domain-invariant representation learning under strict Leave-One-Subject-Out (LOSO) evaluation.
- **Expected Outcome**: Within-subject accuracy remains high, but LOSO cross-subject accuracy drops by $+6.0\%–10.0\%$, validating the necessity of GRL for unseen subject transfer.

---

### Experiment ABL-09: Modality Subset Contribution & Sensitivity Analysis
- **Experiment ID**: `EXP-ABL-09`
- **Component Tested**: Modality branches in isolation and pair-wise combinations.
- **Sub-Experiments**:
  - `EXP-ABL-09a`: EEG-Only Branch (ECG and EDA zeroed out)
  - `EXP-ABL-09b`: ECG-Only Branch
  - `EXP-ABL-09c`: EDA-Only Branch
  - `EXP-ABL-09d`: EEG + ECG Dual-Branch
  - `EXP-ABL-09e`: EEG + EDA Dual-Branch
  - `EXP-ABL-09f`: ECG + EDA Dual-Branch (Peripheral-Only)
- **Scientific Rationale**: Quantifies the marginal contribution of each biological sensory channel to Valence, Arousal, and Categorical emotion recognition.
- **Expected Outcome**: EEG provides the primary basis for Valence and Discrete classification, while EDA/ECG provide critical complementary boost for Arousal ($+8.0\%–12.0\%$).

---

### Experiment ABL-10: Missing-Modality Robustness & Imputation Routing
- **Experiment ID**: `EXP-ABL-10`
- **Component Tested**: Modality Dropout ($p_{drop} = 0.2$) and dynamic cross-modal latent imputation.
- **Modification**: Compare against a model trained without Modality Dropout ($p_{drop} = 0$) when evaluating under 100% missing EEG or 100% missing peripheral signals at inference time.
- **Scientific Rationale**: Tests **RQ6** ($H_1^{(6)}$). Verifies whether training with stochastic modality dropping forces the network to learn robust cross-modal reconstruction paths.
- **Expected Outcome**: The proposed model retains $>85\%$ of full multimodal accuracy when EEG drops out, whereas the naive model collapses to near-chance ($<55\%$).

---

## 4. Standardized Reporting Template for Ablation Results

Every ablation experiment will record its results in the following standardized comparative table across all benchmark datasets:

| Experiment ID | Architectural Variant | Valence RMSE ($\downarrow$) | Valence $r$ ($\uparrow$) | Arousal RMSE ($\downarrow$) | Arousal $r$ ($\uparrow$) | Emotion Macro-F1 ($\uparrow$) | LOSO Acc ($\uparrow$) | $\Delta_{MTL}$ | $p$-value vs Anchor |
|---|---|---|---|---|---|---|---|---|---|
| `EXP-ABL-00` | **Full MMB-EmotionNet (Anchor)** | **Target** | **Target** | **Target** | **Target** | **Target** | **Target** | **$> 0$** | — |
| `EXP-ABL-01` | − Shared-Private Disentangle | | | | | | | | |
| `EXP-ABL-02` | − Difference Orthogonality | | | | | | | | |
| `EXP-ABL-03` | − Similarity Loss (CMD) | | | | | | | | |
| `EXP-ABL-04` | − Reconstruction Loss | | | | | | | | |
| `EXP-ABL-05` | − Cross-Modal Attention | | | | | | | | |
| `EXP-ABL-06` | − Dynamic Uncertainty (Static) | | | | | | | | |
| `EXP-ABL-07` | − Dedicated Branches (Mono) | | | | | | | | |
| `EXP-ABL-08` | − Domain Alignment (No GRL) | | | | | | | | |
| `EXP-ABL-09a`| EEG-Only Unimodal | | | | | | | | |
| `EXP-ABL-09f`| Peripheral-Only (ECG+EDA) | | | | | | | | |
| `EXP-ABL-10` | Zero-Shot Missing EEG (100%) | | | | | | | | |

---

## 5. Synthesis & Transition to Phase P9

With the 10 controlled ablation experiments fully specified and mapped to hypotheses $H_1$ through $H_6$, the project is ready to proceed to **Phase P9: Cross-Subject & Cross-Dataset Generalization Protocol** to define the domain transfer validation suites.
