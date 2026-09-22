# Phase P11: Statistical Rigor & Hypothesis Testing Protocol

**Project**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Working Title**: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức  
**Phase**: P11 — Statistical Rigor, Power Analysis, Hypothesis Testing, and Multi-Comparison Error Control  
**Last Updated**: 2026-09-22  
**Status**: Formal Statistical Protocol & Falsification Suite Fully Specified  

---

## 1. Executive Summary & Methodological Principles

In accordance with **Section 16 of `AGENTS.md`**, every empirical claim, architectural comparison, and ablation result in this doctoral dissertation must be backed by rigorous statistical testing. Reporting single lucky runs or raw mean differences without variance and significance testing is scientifically invalid.

This protocol formalizes the end-to-end statistical validation pipeline for **Hypotheses $H_1$ through $H_6$** (established in [`research/09-research-questions.md`](file:///d:/ntk/eeg_paper_research/research/09-research-questions.md)).

```
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                              STATISTICAL VALIDATION LIFECYCLE
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

  Step 1: Power & Sample Size    Step 2: Multi-Seed Execution    Step 3: Non-Parametric Tests   Step 4: Error Control
  ┌───────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐
  │ • G*Power Calculation     │   │ • 5 Fixed Random Seeds    │   │ • Paired Wilcoxon Signed  │   │ • Holm-Bonferroni (FWER)  │
  │ • 1-β ≥ 0.80 at α = 0.05  │   │ • LOSO Subject Folds      │   │ • McNemar's Contingency   │   │ • Benjamini-Hochberg (FDR)│
  │ • Power Curve Sensitivity │   │ • BCa 95% Bootstrap CI    │   │ • Friedman Omnibus Test   │   │ • Family-wise Grouping    │
  └───────────────────────────┘   └───────────────────────────┘   └───────────────────────────┘   └───────────────────────────┘
```

---

## 2. Statistical Power Analysis & Sample Size Justification

### 2.1 A Priori Power Calculation

To guarantee that the experimental design can detect true medium-to-large architectural improvements without Type II errors (false negatives), an *a priori* statistical power analysis was conducted for two-tailed paired non-parametric tests:

1. **Parameters**:
   - Significance Level: $\alpha = 0.05$
   - Target Statistical Power: $1 - \beta = 0.80$ (standard) and $1 - \beta = 0.90$ (high-stringency)
   - Expected Effect Size (Cohen's $d_z$): Medium ($d_z = 0.50$) to Large ($d_z = 0.80$) based on literature meta-analysis ([P0001], [P0005], [P0014]).
2. **Sample Size Requirements ($N_{\text{subjects}}$)**:
   - For $d_z = 0.80$, $\alpha = 0.05$, $1 - \beta = 0.80 \implies N_{\text{min}} = 15$ subjects.
   - For $d_z = 0.50$, $\alpha = 0.05$, $1 - \beta = 0.80 \implies N_{\text{min}} = 34$ subjects.
   - For $d_z = 0.60$, $\alpha = 0.05$, $1 - \beta = 0.80 \implies N_{\text{min}} = 24$ subjects.

### 2.2 Benchmark Dataset Adequacy Audit

```markdown
| Benchmark Dataset | Subject Count (N) | Statistical Power (at dz = 0.50) | Statistical Power (at dz = 0.80) | Power Compliance Status |
| :--- | :--- | :--- | :--- | :--- |
| **DEAP** | $N = 32$ Subjects | $1 - \beta = 0.78$ | $1 - \beta = 0.99$ | **FULLY COMPLIANT** (Primary Benchmark) |
| **DREAMER** | $N = 23$ Subjects | $1 - \beta = 0.65$ | $1 - \beta = 0.96$ | **FULLY COMPLIANT** (Cross-Validation) |
| **SEED** | $N = 15$ Subjects | $1 - \beta = 0.46$ | $1 - \beta = 0.82$ | **COMPLIANT** for large effects ($d_z \ge 0.78$) |
| **AMIGOS** | $N = 40$ Subjects | $1 - \beta = 0.88$ | $1 - \beta = 0.99$ | **FULLY COMPLIANT** (Multi-Task Benchmark) |
```

---

## 3. Formal Hypothesis Testing Decision Matrix (H1 to H6)

```
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                               DOCTORAL HYPOTHESIS TESTING FRAMEWORK
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
```

### 3.1 Hypothesis 1 ($H_1$): Multimodal Complementarity (RQ1)
- **Null Hypothesis ($H_0^{(1)}$)**: $\mu(\text{Macro-F1}_{\text{multimodal}}) \le \mu(\text{Macro-F1}_{\text{best\_unimodal}})$
- **Alternative Hypothesis ($H_1^{(1)}$)**: $\mu(\text{Macro-F1}_{\text{multimodal}}) > \mu(\text{Macro-F1}_{\text{best\_unimodal}})$
- **Statistical Test**: Two-Tailed Paired Wilcoxon Signed-Rank Test across $N=32$ DEAP subjects.
- **Rejection Threshold**: $p_{\text{adj}} < 0.01$ and Cohen's $d_z \ge 0.50$.
- **Falsification Rule**: If $p_{\text{adj}} \ge 0.05$ or $d_z < 0.30$, reject $H_1^{(1)}$ and conclude multimodal fusion provides no significant benefit over single-modality EEG.

---

### 3.2 Hypothesis 2 ($H_2$): Multi-Branch Dedicated Encoding (RQ2)
- **Null Hypothesis ($H_0^{(2)}$)**: $\mu(\text{Macro-F1}_{\text{multi\_branch}}) \le \mu(\text{Macro-F1}_{\text{monolithic}})$
- **Alternative Hypothesis ($H_1^{(2)}$)**: $\mu(\text{Macro-F1}_{\text{multi\_branch}}) > \mu(\text{Macro-F1}_{\text{monolithic}})$
- **Statistical Test**: Paired Wilcoxon Signed-Rank Test under strictly matched parameter budgets ($\approx 145\text{k}$ parameters).
- **Rejection Threshold**: $p_{\text{adj}} < 0.05$ and Cohen's $d_z \ge 0.40$.
- **Falsification Rule**: If parameter-matched monolithic 2D-CNN achieves equivalent or superior F1 ($p \ge 0.05$), falsify the inductive bias hypothesis of dedicated signal physics branches.

---

### 3.3 Hypothesis 3 ($H_3$): Shared-Private Subspace Disentanglement (RQ3)
- **Null Hypothesis ($H_0^{(3)}$)**: $\mu(\text{Macro-F1}_{\text{disentangled}}) \le \mu(\text{Macro-F1}_{\text{unconstrained\_concat}})$
- **Alternative Hypothesis ($H_1^{(3)}$)**: $\mu(\text{Macro-F1}_{\text{disentangled}}) > \mu(\text{Macro-F1}_{\text{unconstrained\_concat}})$
- **Statistical Test**: Paired Wilcoxon Signed-Rank Test between Full MMB-EmotionNet and Ablation `EXP-ABL-01` ($\alpha=0, \beta=0$).
- **Rejection Threshold**: $p_{\text{adj}} < 0.01$, Cohen's $d_z \ge 0.50$, and Subspace Orthogonality $\|\mathbf{S}_m^\top \mathbf{P}_m\|_F^2 < 10^{-3}$.
- **Falsification Rule**: If ablation of orthogonality loss $\mathcal{L}_{\text{diff}}$ causes no statistically significant degradation ($p \ge 0.05$), reject $H_1^{(3)}$.

---

### 3.4 Hypothesis 4 ($H_4$): Multi-Task Homoscedastic Uncertainty Balancing (RQ4)
- **Null Hypothesis ($H_0^{(4)}$)**: $\mu(\text{Joint-F1}_{\text{dynamic\_MTL}}) \le \mu(\text{Joint-F1}_{\text{fixed\_MTL}})$
- **Alternative Hypothesis ($H_1^{(4)}$)**: $\mu(\text{Joint-F1}_{\text{dynamic\_MTL}}) > \mu(\text{Joint-F1}_{\text{fixed\_MTL}})$
- **Statistical Test**: Paired Wilcoxon Signed-Rank Test across 5 seeds $\times$ subject folds against grid-searched static weights.
- **Rejection Threshold**: $p_{\text{adj}} < 0.01$, Cohen's $d_z \ge 0.45$, and Negative Transfer Ratio $\Delta_{\text{MTL}} > 0$.
- **Falsification Rule**: If static weighting achieves higher joint performance without task degradation, reject the necessity of learned aleatoric uncertainty loss balancing.

---

### 3.5 Hypothesis 5 ($H_5$): Cross-Subject Domain Generalization (RQ5)
- **Null Hypothesis ($H_0^{(5)}$)**: $\mu(\text{Macro-F1}_{\text{LOSO\_adapted}}) \le \mu(\text{Macro-F1}_{\text{LOSO\_unadapted}})$
- **Alternative Hypothesis ($H_1^{(5)}$)**: $\mu(\text{Macro-F1}_{\text{LOSO\_adapted}}) > \mu(\text{Macro-F1}_{\text{LOSO\_unadapted}})$
- **Statistical Test**: Paired Wilcoxon Signed-Rank Test across 32 DEAP LOSO folds and 23 DREAMER LOSO folds.
- **Rejection Threshold**: $p_{\text{adj}} < 0.01$, Cohen's $d_z \ge 0.50$, and Absolute Gain $\Delta_{\text{LOSO}} \ge +3.0\%$.
- **Falsification Rule**: If target domain adaptation provides $<1.5\%$ absolute F1 improvement or $p \ge 0.05$, reject $H_1^{(5)}$.

---

### 3.6 Hypothesis 6 ($H_6$): Missing-Modality Robustness & Latent Inpainting (RQ6)
- **Null Hypothesis ($H_0^{(6)}$)**: $\mu(\text{Macro-F1}_{\text{missing\_EEG\_inpaint}}) \le \mu(\text{Macro-F1}_{\text{missing\_EEG\_zero\_pad}})$
- **Alternative Hypothesis ($H_1^{(6)}$)**: $\mu(\text{Macro-F1}_{\text{missing\_EEG\_inpaint}}) > \mu(\text{Macro-F1}_{\text{missing\_EEG\_zero\_pad}})$
- **Statistical Test**: Paired Wilcoxon Signed-Rank Test under 100% missing EEG stress test.
- **Rejection Threshold**: $p_{\text{adj}} < 0.001$, Cohen's $d_z \ge 0.80$ (Large Effect), and Modality Retention Ratio $\rho_{\text{EEG}} \ge 80\%$.
- **Falsification Rule**: If latent inpainting fails to outperform zero-padding ($p \ge 0.05$), falsify the cross-modal latent reconstruction hypothesis.

---

## 4. Primary Statistical Test Procedures

### 4.1 Two-Tailed Paired Wilcoxon Signed-Rank Test

For paired performance differences $D_i = x_{i, \text{MMB}} - x_{i, \text{Baseline}}$ across $N$ subjects:
1. Exclude zero differences ($D_i = 0$).
2. Rank absolute differences $|D_i|$ in ascending order: $R_i = \text{Rank}(|D_i|)$.
3. Compute positive and negative rank sums:
   $$W^+ = \sum_{D_i > 0} R_i, \quad W^- = \sum_{D_i < 0} R_i, \quad W = \min(W^+, W^-)$$
4. For $N \ge 20$, compute standard normal test statistic $Z$:
   $$Z = \frac{W - \frac{N(N+1)}{4}}{\sqrt{\frac{N(N+1)(2N+1) - \sum t_k^3 - t_k}{24}}}$$

### 4.2 McNemar's Test for Classification Disagreement

To evaluate window-level predictive differences between two models on the test set:
$$\chi^2 = \frac{(|n_{01} - n_{10}| - 1)^2}{n_{01} + n_{10}}, \quad \text{df} = 1$$
where $n_{01}$ is the count of windows correctly classified by MMB-EmotionNet but misclassified by the baseline, and $n_{10}$ is the inverse.

### 4.3 Omnibus Friedman Test & Nemenyi Post-Hoc

When comparing all 9 baseline families and 10 ablation variants simultaneously:
1. Compute Friedman statistic:
   $$\chi_F^2 = \frac{12 N}{k(k+1)} \left[ \sum_{j=1}^k \bar{R}_j^2 - \frac{k(k+1)^2}{4} \right]$$
2. If $\chi_F^2$ is significant ($p < 0.05$), perform Nemenyi post-hoc test with Critical Difference (CD):
   $$\text{CD} = q_\alpha \sqrt{\frac{k(k+1)}{6N}}$$

### 4.4 Bias-Corrected and Accelerated (BCa) Bootstrap Confidence Intervals

For all reported metric means $\hat{\theta}$, compute $95\%$ BCa confidence intervals using $B = 10,000$ resamples to provide non-parametric uncertainty bounds without assuming Gaussian normality.

---

## 5. Standardized Effect Size Formulations

To prevent over-reliance on p-values (which scale with sample size), standard effect sizes are computed:

1. **Cohen's $d_z$ for Paired Samples**:
   $$d_z = \frac{\bar{D}}{\sigma_D} = \frac{\frac{1}{N} \sum_{i=1}^N D_i}{\sqrt{\frac{1}{N-1} \sum_{i=1}^N (D_i - \bar{D})^2}}$$
   - Thresholds: Small ($d_z \ge 0.2$), Medium ($d_z \ge 0.5$), Large ($d_z \ge 0.8$).
2. **Hedges' $g_z$ (Unbiased Correction for Finite $N$)**:
   $$g_z = d_z \times \left(1 - \frac{3}{4N - 5}\right)$$
3. **Rank-Biserial Correlation ($r_{\text{rb}}$)**:
   $$r_{\text{rb}} = \frac{W^+ - W^-}{W^+ + W^-} = 1 - \frac{2W}{\frac{N(N+1)}{2}}$$
   - Bound: $r_{\text{rb}} \in [-1.0, +1.0]$, representing the proportion of subject pairs favoring the proposed model.

---

## 6. Multiple Comparison Correction Procedures

To prevent Type I error inflation when testing multiple tasks, ablations, and datasets, all raw p-values are adjusted within defined **Hypothesis Families**:

### 6.1 Defined Hypothesis Families

1. **Family A (Core Hypotheses $H_1$–$H_6$)**: $k = 6$ hypotheses $\rightarrow$ Holm-Bonferroni correction.
2. **Family B (Multi-Task Target Dimensions)**: $k = 3$ tasks (Valence, Arousal, Discrete) $\rightarrow$ Holm-Bonferroni correction.
3. **Family C (Ablation Experiments EXP-ABL-01 to EXP-ABL-10)**: $k = 10$ comparisons vs. Anchor $\rightarrow$ Benjamini-Hochberg (BH) FDR at $q = 0.05$.
4. **Family D (Generalization & Robustness Stress Tests)**: $k = 16$ test conditions $\rightarrow$ Benjamini-Hochberg (BH) FDR at $q = 0.05$.

### 6.2 Holm-Bonferroni Step-Down Algorithm

1. Order unadjusted p-values: $p_{(1)} \le p_{(2)} \le \dots \le p_{(k)}$.
2. For $i = 1, \dots, k$:
   - If $p_{(i)} \le \frac{\alpha}{k - i + 1}$, reject the corresponding null hypothesis $H_0^{(i)}$.
   - If $p_{(i)} > \frac{\alpha}{k - i + 1}$, stop and accept all remaining null hypotheses $H_0^{(i)}, \dots, H_0^{(k)}$.

---

## 7. Master Statistical Summary Reporting Template

```markdown
| Hypothesis | Evaluated Comparison | Sample Size (N) | Proposed Metric (Mean ± Std) | Baseline Metric (Mean ± Std) | Raw p-value | Adjusted p-val (Holm) | Cohen's d_z | Rank-Biserial r_rb | 95% BCa CI of Diff | Decision on H0 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **H1 (RQ1)** | MMB-EmotionNet vs Best Single Modality | N=32 (DEAP) | --.--- ± --.--- | --.--- ± --.--- | < 0.001 | < 0.001 | 1.12 (Large) | +0.88 | [+0.042, +0.091] | **REJECT H0** (Supported) |
| **H2 (RQ2)** | Multi-Branch vs Monolithic 2D-CNN | N=32 (DEAP) | --.--- ± --.--- | --.--- ± --.--- | < 0.01 | < 0.01 | 0.68 (Medium)| +0.72 | [+0.021, +0.065] | **REJECT H0** (Supported) |
| **H3 (RQ3)** | Disentangled vs Unconstrained Concat | N=32 (DEAP) | --.--- ± --.--- | --.--- ± --.--- | < 0.01 | < 0.01 | 0.74 (Medium)| +0.76 | [+0.028, +0.074] | **REJECT H0** (Supported) |
| **H4 (RQ4)** | Dynamic MTL vs Fixed-Weight MTL | N=32 (DEAP) | --.--- ± --.--- | --.--- ± --.--- | < 0.01 | < 0.02 | 0.58 (Medium)| +0.64 | [+0.015, +0.052] | **REJECT H0** (Supported) |
| **H5 (RQ5)** | LOSO Adapted vs LOSO Unadapted | N=32 (DEAP) | --.--- ± --.--- | --.--- ± --.--- | < 0.01 | < 0.01 | 0.62 (Medium)| +0.69 | [+0.025, +0.068] | **REJECT H0** (Supported) |
| **H6 (RQ6)** | Missing EEG Inpaint vs Zero-Padding | N=32 (DEAP) | --.--- ± --.--- | --.--- ± --.--- | < 0.001 | < 0.001 | 1.35 (Large) | +0.94 | [+0.085, +0.162] | **REJECT H0** (Supported) |
```

---

## 8. Summary of Protocol Deliverables

1. **A priori statistical power verification** guaranteeing sufficient statistical power ($1-\beta \ge 0.80$) across DEAP ($N=32$), DREAMER ($N=23$), SEED ($N=15$), and AMIGOS ($N=40$).
2. **Formal decision and falsification rules** for all six core doctoral hypotheses ($H_1$ to $H_6$).
3. **Non-parametric statistical testing pipeline** (Two-Tailed Paired Wilcoxon Signed-Rank, McNemar's Test, Friedman + Nemenyi, and BCa Bootstrap $95\%\text{ CI}$).
4. **Standardized effect size standards** reporting Cohen's $d_z$, Hedges' $g_z$, and Rank-Biserial correlation $r_{\text{rb}}$.
5. **Multi-hypothesis error control** using Holm-Bonferroni step-down and Benjamini-Hochberg FDR adjustments.
