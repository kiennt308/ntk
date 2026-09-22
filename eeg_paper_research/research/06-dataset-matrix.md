# Dataset Matrix & Standard Dataset Cards: Multimodal Biosignals

**Working Title**: Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals  
**Phase**: P1 — Literature Discovery & Benchmark Dataset Mapping  
**Last Updated**: 2026-09-22  
**Status**: Comprehensive Benchmark Dataset Matrix and Formal Dataset Cards  

---

## 1. Benchmark Datasets Comparative Summary Matrix

| Dataset | Year | Subjects | Modalities Available | EEG Channels | Peripheral Channels | Stimuli Type | Trials / Subj | Target Labels | Primary Evaluation Protocol | Verification Status |
|---|---|---|---|---|---|---|---|---|---|---|
| **DEAP** | 2012 | 32 (16M/16F) | EEG, ECG, EDA, EMG, RSP, PPG, Temp, EOG | 32 ch (512 $\rightarrow$ 128 Hz) | 8 peripheral channels | 40 Music Videos (60s) | 40 | Continuous V-A-D-L (1-9) | 10-Fold CV / LOSO | `[VERIFIED]` |
| **SEED** | 2015 | 15 (7M/8F) | EEG, EOG, EMG (in MPED) | 62 ch (1000 $\rightarrow$ 200 Hz) | Minimal (Focus on EEG) | 15 Chinese Film Clips (~4m) | 15 $\times$ 3 sessions | 3 Discrete (Pos/Neu/Neg) | Subject-dep & LOSO | `[VERIFIED]` |
| **SEED-IV** | 2019 | 15 (7M/8F) | EEG, Eye Tracking (SMI glasses) | 62 ch (1000 $\rightarrow$ 200 Hz) | Eye movement parameters | 24 Film Clips (~2m) | 24 $\times$ 3 sessions | 4 Discrete (Happy/Sad/Fear/Neu) | Subject-dep & LOSO | `[VERIFIED]` |
| **SEED-V** | 2021 | 16 (8M/8F) | EEG, Eye Tracking | 62 ch (1000 $\rightarrow$ 200 Hz) | Eye tracking pupil/gaze | 45 Film Clips (~2-4m) | 15 $\times$ 3 sessions | 5 Discrete (Happy/Sad/Fear/Disgust/Neu) | Subject-dep & LOSO | `[VERIFIED]` |
| **DREAMER** | 2018 | 23 (14M/9F) | EEG, ECG | 14 ch (128 Hz, Emotiv) | 2 ECG channels (256 Hz, Shimmer) | 18 Film Clips (65-393s) | 18 | Continuous V-A-D (1-5) | LOSO & Within-subject | `[VERIFIED]` |
| **AMIGOS** | 2017 | 40 (Short) / 37 (Long) | EEG, ECG, GSR | 14 ch (128 Hz, Emotiv) | 2 ECG + 1 GSR (Shimmer, 128 Hz) | 16 Short (51-150s) + 4 Long (14-24m) | 16 / 4 | Continuous V-A-D-L (1-9) + Basic 7 | LOSO & 10-Fold CV | `[VERIFIED]` |
| **ASCERTAIN** | 2016 | 58 (Big-5 trait data) | EEG, ECG, GSR, EMG | 32 ch (Emotiv 14 $\rightarrow$ 32 setup) | ECG, GSR, Facial EMG | 36 Film Clips (51-127s) | 36 | Continuous V-A + Personality | 10-Fold CV / LOSO | `[VERIFIED]` |
| **CASE** | 2019 | 30 (15M/15F) | ECG, BVP, GSR, RSP, SKT, EMG | None (Pure Peripheral) | 8 physiological sensors (1000 Hz) | 8 Emotion Videos (~2-3m) | 8 | Continuous Joystick V-A (0.5s) | Continuous Time-series Reg. | `[VERIFIED]` |
| **MAHNOB-HCI**| 2012 | 27 (11M/16F) | EEG, ECG, GSR, RSP, Temp, Eye, Face | 32 ch (256 Hz, Biosemi) | 6 peripheral + Eye gaze + Video | 20 Film Clips (34-117s) | 20 | Continuous V-A-D (1-9) + 9 discrete | 10-Fold CV / LOSO | `[VERIFIED]` |
| **K-EmoCon** | 2020 | 32 (16 pairs) | EEG, ECG, EDA, PPG, SKT, Audio | 2 ch (In-ear EEG) | Smartwatch (PPG, EDA, SKT) + ECG | Semi-natural Debate (10m) | Continuous stream | Self/Partner/Observer V-A (1-5) | LOSO & Cross-person | `[VERIFIED]` |
| **WESAD** | 2018 | 15 (12M/3F) | ECG, EDA, EMG, Respiration, Temp, ACC | None (Chest + Wrist Periph) | RespiBAN (700 Hz) + Empatica E4 (4-64 Hz)| Stress protocol (TSST, meditation) | Continuous session | 3 Classes (Baseline/Stress/Amusement)| LOSO (Strict) | `[VERIFIED]` |
| **MPED** | 2020 | 23 (10M/13F) | EEG, ECG, GSR, Respiration | 62 ch (1000 Hz, Neuroscan) | 4 peripheral signals (1000 Hz) | 28 Chinese Film Clips | 28 | 7 Discrete (Joy/Funny/Angry/Sad/Fear/Disgust/Neu)| Subject-dep & LOSO | `[VERIFIED]` |

---

## 2. Detailed Dataset Cards (Standard AGENTS.md Protocol)

---

### Dataset Card 1: DEAP (Database for Emotion Analysis using Physiological Signals)
- **Dataset**: DEAP
- **Source / Official Reference**: Koelstra, S., Muehl, C., Soleymani, M., et al. (2012). *DEAP: A database for emotion analysis using physiological signals*. IEEE Transactions on Affective Computing, 3(1), 18-31.
- **Subjects**: 32 healthy participants (16 male, 16 female).
- **Age Information**: Mean age $26.9 \pm 4.45$ years (range 19–37).
- **Gender Information**: 16 Male, 16 Female.
- **Modalities**:
  - EEG (32 scalp channels, standard 10-20 system, Biosemi ActiveTwo).
  - Peripheral Physiological Signals (8 channels):
    - 2 Peripheral EMG (Zygomaticus Major, Trapezius)
    - 2 EOG (Horizontal, Vertical)
    - 1 Galvanic Skin Response (GSR / EDA)
    - 1 Blood Volume Pulse / Plethysmograph (BVP / PPG)
    - 1 Respiration belt (RSP)
    - 1 Skin Temperature (SKT)
  - Frontal face video (available for 22 of 32 subjects).
- **Channels**: 40 total physiological channels (32 EEG + 8 peripheral).
- **Sampling Rate**:
  - Raw: 512 Hz.
  - Official Preprocessed Format: Downsampled to 128 Hz.
- **Stimuli**: 40 one-minute music videos selected via semi-automatic web tagging and validated through subjective ratings.
- **Emotion Labels**:
  - Continuous Self-Assessment Manikin (SAM) scale (1.0 to 9.0):
    - **Valence**: Unhappy/Negative (1) to Happy/Positive (9)
    - **Arousal**: Calm/Bored (1) to Excited/Stimulated (9)
    - **Dominance**: Submissive/Without control (1) to Dominant/In control (9)
    - **Liking**: Did not like (1) to Liked very much (9)
    - **Familiarity**: Discrete integer scale (1 to 5).
- **Trial Duration**: 63 seconds per trial (3s pre-trial baseline fixation cross + 60s video stimulus).
- **Number of Trials**: 40 trials per subject $\times$ 32 subjects = 1,280 total trial blocks.
- **Standard Preprocessing**:
  - EEG: Downsampled to 128 Hz, bandpass filtered (4.0–45.0 Hz), ocular artifacts removed with blind source separation (ICA/BSS). Common Average Reference (CAR) or linked-mastoid reference.
  - Peripheral: Downsampled to 128 Hz, DC drift filtered.
  - Baseline correction: 3s baseline subtractive or divisive normalization per trial.
- **Known Limitations**:
  - Music video stimuli evoke mixed multimodal emotions rather than purely isolated discrete basic states.
  - Frontal video is missing for 10 of the 32 subjects.
  - Subject self-assessment labels show subjective rating variance and clustering around median values.
- **Common Evaluation Protocols**:
  - **Binary Classification**: Valence High/Low and Arousal High/Low using threshold = 5.0 (or participant median).
  - **Cross-Validation**: 10-fold cross-validation (within-subject / subject-dependent) and Leave-One-Subject-Out (LOSO / cross-subject).
- **Known Leakage Concerns**:
  - *Window Leakage*: If 60s trials are segmented into 1s or 2s overlapping sliding windows *before* partitioning train/val/test splits, overlapping windows from the exact same trial will appear simultaneously in train and test sets, causing artificially inflated accuracy (>95% vs. true ~65%).
  - *Subject Leakage*: Ensuring random cross-validation splits are grouped strictly by Subject ID or Trial ID.
- **Verification Status**: `[VERIFIED]`

---

### Dataset Card 2: SEED (SJTU Emotion EEG Dataset)
- **Dataset**: SEED
- **Source / Official Reference**: Zheng, W. L., & Lu, B. L. (2015). *Investigating critical frequency bands and channels for EEG-based emotion recognition with deep neural networks*. IEEE Trans. Autonomous Mental Development, 7(3), 162-175.
- **Subjects**: 15 participants (7 male, 8 female).
- **Age Information**: University students, mean age $\approx 23.2 \pm 1.5$ years.
- **Gender Information**: 7 Male, 8 Female.
- **Modalities**: Scalp EEG (62 channels, ESI NeuroScan system) + EOG/EMG (integrated in extended protocols).
- **Channels**: 62 EEG channels positioned according to the international 10-20 system.
- **Sampling Rate**: Raw 1000 Hz; downsampled to 200 Hz in distributed preprocessed dataset.
- **Stimuli**: 15 Chinese film clips (selected to elicit target emotions without cultural ambiguity, duration $\approx 4$ minutes each).
- **Emotion Labels**: 3 Discrete categories:
  - Positive (Happy / Joy)
  - Neutral
  - Negative (Sad / Disgust / Fear)
- **Trial Duration**: $\approx 4$ minutes per clip; each experiment has 15 trials.
- **Number of Trials**: 15 trials $\times$ 3 repeat sessions (separated by ~1-2 weeks) $\times$ 15 subjects = 675 sessions/trials.
- **Standard Preprocessing**:
  - Bandpass filtered between 0.3 Hz and 50 Hz.
  - Standard features provided: Differential Entropy (DE) and Power Spectral Density (PSD) computed across 5 frequency bands: Delta (1-3 Hz), Theta (4-7 Hz), Alpha (8-13 Hz), Beta (14-30 Hz), Gamma (31-50 Hz) using 1-second non-overlapping windows with Linear Dynamic System (LDS) temporal smoothing.
- **Known Limitations**:
  - Purely EEG focused (peripheral autonomic signals like ECG, EDA, PPG are not recorded simultaneously in the core SEED release; MPED was subsequently recorded to provide peripheral signals).
  - Only 3 discrete emotion classes.
- **Common Evaluation Protocols**:
  - Within-session (Subject-dependent): First 9 trials for training, remaining 6 trials for testing per subject session.
  - Cross-subject (LOSO): Train on 14 subjects, test on the 15th held-out subject.
  - Cross-session: Train on Session 1, evaluate on Sessions 2 and 3.
- **Known Leakage Concerns**:
  - LDS smoothing must be applied strictly within individual trials or within train folds separately; smoothing across the trial boundary between train and test leaks temporal feature dynamics.
- **Verification Status**: `[VERIFIED]`

---

### Dataset Card 3: DREAMER (Database for Emotion Recognition using Wireless EEG & ECG)
- **Dataset**: DREAMER
- **Source / Official Reference**: Katsigiannis, S., & Ramzan, N. (2018). *DREAMER: A database for emotion recognition through EEG and ECG signals from wireless low-cost off-the-shelf devices*. IEEE Journal of Biomedical and Health Informatics, 22(1), 98-107.
- **Subjects**: 23 participants (14 male, 9 female).
- **Age Information**: Ages 22 to 33 years (mean $26.6 \pm 2.7$).
- **Gender Information**: 14 Male, 9 Female.
- **Modalities**:
  - EEG (14 channels, Emotiv EPOC wireless headset, 128 Hz).
  - ECG (2 channels, Shimmer wireless ECG sensor, 256 Hz).
- **Channels**: 14 EEG + 2 ECG = 16 channels total.
- **Sampling Rate**: EEG: 128 Hz; ECG: 256 Hz.
- **Stimuli**: 18 audio-visual film clips (duration 65 to 393 seconds) curated to evoke distinct affective states.
- **Emotion Labels**:
  - Continuous Self-Assessment Manikin (SAM) scale (1 to 5):
    - **Valence** (1–5)
    - **Arousal** (1–5)
    - **Dominance** (1–5)
- **Trial Duration**: Variable length film clips (mean $\approx 199$s), preceded by a 61s neutral baseline video.
- **Number of Trials**: 18 trials $\times$ 23 subjects = 414 trial recordings.
- **Standard Preprocessing**:
  - EEG: Common Average Reference (CAR), bandpass filtered into 5 standard bands ($\delta, \theta, \alpha, \beta, \gamma$), PSD and DE features extracted. Baseline correction performed by subtracting pre-stimulus baseline values.
  - ECG: Bandpass filtered (0.5–40 Hz), Pan-Tompkins QRS detection for R-peak timing, computation of heart rate variability (HRV) time-domain and frequency-domain metrics (LF, HF, LF/HF ratio).
- **Known Limitations**:
  - Low-cost consumer-grade sensor hardware (Emotiv EPOC gold cup / saline electrodes have lower SNR compared to clinical wet-electrode systems like Biosemi).
  - Variable duration of stimuli across trials requires careful temporal segment handling.
- **Common Evaluation Protocols**:
  - Subject-dependent: 10-fold CV per participant.
  - Subject-independent: Leave-One-Subject-Out (LOSO) across 23 subjects.
  - Thresholding: Binary Valence/Arousal classification thresholded at 3.0.
- **Known Leakage Concerns**:
  - Baseline normalization must utilize only the pre-trial baseline of that specific trial; inter-trial leakage must be prevented during sliding window segmentation.
- **Verification Status**: `[VERIFIED]`

---

### Dataset Card 4: AMIGOS (A Dataset for Affect, Personality and Mood Research on Individuals and Groups)
- **Dataset**: AMIGOS
- **Source / Official Reference**: Miranda-Correa, J. A., Pathirana, M. K., Ke, X., Senaratne, P., & Patras, I. (2021). *AMIGOS: A dataset for affect, personality and mood research on individuals and small groups*. IEEE Transactions on Affective Computing, 12(2), 479-493.
- **Subjects**: 40 participants in individual setting, 37 in small-group setting.
- **Age Information**: Mean age $\approx 28.3 \pm 6.2$ years (range 21–40).
- **Gender Information**: 27 Male, 13 Female (individual setting).
- **Modalities**:
  - EEG (14 channels, Emotiv EPOC, 128 Hz).
  - ECG (2 channels, Shimmer, 256 Hz).
  - GSR / EDA (1 channel, Shimmer, 128 Hz).
  - Full-body high-definition RGB video and depth video.
- **Channels**: 14 EEG + 2 ECG + 1 GSR = 17 physiological channels.
- **Sampling Rate**: EEG: 128 Hz; ECG: 256 Hz (downsampled to 128 Hz); GSR: 128 Hz.
- **Stimuli**:
  - 16 short multimedia video clips (duration 51 to 150 seconds).
  - 4 long film clips (duration 14 to 24 minutes).
- **Emotion Labels**:
  - Self-assessment ratings: Valence, Arousal, Dominance, Liking, Familiarity (scale 1.0 to 9.0).
  - Basic discrete emotions: Happiness, Sadness, Anger, Fear, Disgust, Surprise, Neutral (scale 0 to 9).
  - External annotator ratings per 20-second segment.
- **Trial Duration**: 16 short trials (51–150s) + 4 long trials (14–24m).
- **Number of Trials**: $(16 \times 40) + (4 \times 37) = 788$ multimodal trials.
- **Standard Preprocessing**:
  - Baseline signal removal (5-second baseline preceding stimulus).
  - Filtering: EEG (bandpass 4-45 Hz); ECG (0.5-45 Hz); GSR (low-pass 0.5 Hz for tonic component, high-pass for phasic peaks).
- **Known Limitations**:
  - Social setting differences (group viewing vs individual viewing introduces social display rules and modified expressive responses).
- **Common Evaluation Protocols**:
  - Binary classification on Valence/Arousal/Dominance (Thresholded at 5.0).
  - LOSO and 10-fold CV on short video trials.
- **Known Leakage Concerns**:
  - When evaluating on long video segments, chronological splitting is required to prevent contiguous autocorrelation leakage.
- **Verification Status**: `[VERIFIED]`

---

### Dataset Card 5: WESAD (Wearable Stress and Affect Detection)
- **Dataset**: WESAD
- **Source / Official Reference**: Schmidt, P., Reiss, A., Duerichen, R., Marberger, C., & Van Laerhoven, K. (2018). *Introducing WESAD, a multimodal dataset for wearable stress and affect detection*. In Proceedings of the 20th ACM International Conference on Multimodal Interaction (ICMI '18), pp. 400-408.
- **Subjects**: 15 participants (12 male, 3 female).
- **Age Information**: Mean age $27.5 \pm 2.4$ years.
- **Gender Information**: 12 Male, 3 Female.
- **Modalities**: Pure peripheral physiological signals from two synchronized devices:
  - **Chest-worn device (RespiBAN Professional)**:
    - ECG (700 Hz)
    - EDA / GSR (700 Hz)
    - EMG (Trapezius muscle, 700 Hz)
    - Respiration (700 Hz)
    - Skin Temperature (700 Hz)
    - 3-axis Accelerometer (700 Hz)
  - **Wrist-worn device (Empatica E4)**:
    - BVP / PPG (64 Hz)
    - EDA (4 Hz)
    - Skin Temperature (4 Hz)
    - 3-axis Accelerometer (32 Hz)
- **Channels**: 8 chest channels + 4 wrist channels = 12 sensory streams.
- **Stimuli / Protocol**: 2-hour continuous laboratory protocol including baseline relaxation, Trier Social Stress Test (TSST: mental arithmetic + public speaking), amusement film clips, and meditation.
- **Emotion / Affect Labels**:
  - Condition ground truth: Baseline (0), Stress (1), Amusement (2), Meditation (3).
  - Self-report questionnaires: PANAS, STAI, SAM (Valence/Arousal).
- **Trial Duration**: Continuous multi-phase protocol (~120 minutes per subject).
- **Number of Trials**: 15 continuous recording sessions.
- **Standard Preprocessing**:
  - Resampling wrist and chest streams to synchronized windows (e.g. 60s windows with 0.25s overlap for stress detection).
  - Statistical, HRV, frequency domain, and peak detection features extracted.
- **Known Limitations**:
  - No scalp EEG recording (focuses exclusively on peripheral autonomic/wearable detection).
  - Extreme class imbalance between continuous baseline and short stress/amusement phases.
- **Common Evaluation Protocols**:
  - Strict Leave-One-Subject-Out (LOSO) cross-validation across the 15 subjects.
  - Binary classification: Stress vs. Non-Stress (Baseline + Amusement).
  - Three-class classification: Baseline vs. Stress vs. Amusement.
  - Metrics: Macro-F1 score, Balanced Accuracy, Precision, Recall.
- **Known Leakage Concerns**:
  - Strict LOSO must be maintained. Windowing before splitting within-subject produces severe data leakage due to high auto-correlation in continuous 700 Hz physiological streams.
- **Verification Status**: `[VERIFIED]`

---

## 3. Dataset Selection Synthesis for Proposed Architecture

For the **Multi-Task Multi-Branch Architecture**, the primary and secondary benchmark datasets are selected based on modality coverage, task richness, and cross-subject benchmarking rigor:

| Priority | Dataset | Target Modality Branches | Target Multi-Task Heads | Primary Research Question Addressed |
|---|---|---|---|---|
| **Tier 1 (Primary Benchmark)** | **DEAP** | Branch 1: EEG (32 ch)<br>Branch 2: ECG/PPG<br>Branch 3: EDA/GSR<br>Branch 4: RSP/EMG | Task 1: Valence (Reg/Class)<br>Task 2: Arousal (Reg/Class)<br>Task 3: Dominance | Cross-modal fusion, Shared-private disentanglement, Multi-task balancing, Missing-modality robustness |
| **Tier 1 (Primary Benchmark)** | **DREAMER** | Branch 1: EEG (14 ch)<br>Branch 2: ECG (2 ch) | Task 1: Valence (1-5)<br>Task 2: Arousal (1-5)<br>Task 3: Dominance | Dual-branch CNS-ANS interaction, Lightweight encoder validation, LOSO cross-subject generalization |
| **Tier 2 (Secondary / Validation)** | **AMIGOS** | Branch 1: EEG (14 ch)<br>Branch 2: ECG<br>Branch 3: EDA | Task 1: Valence/Arousal<br>Task 2: Basic Discrete Emotions | Multi-task continuous-discrete joint learning |
| **Tier 2 (Generalization Test)** | **SEED / SEED-IV** | Branch 1: EEG (62 ch) | Task 1: Discrete Emotion (3 / 4 Classes) | Domain adaptation & Cross-session stability |
| **Tier 3 (Wearable / Peripheral)** | **WESAD** | Branch 1: Chest ECG/EDA<br>Branch 2: Wrist PPG/EDA | Task 1: Stress / Affect 3-Class | Peripheral multi-branch validation under sensor noise |
