# Dataset Index: Multimodal Biosignal Emotion Recognition

This index tracks all benchmark datasets identified and utilized in the literature base (Batch 1: P0001–P0010, Batch 2: P0011–P0020, Batch 3: P0021–P0030).

| Dataset ID | Dataset Name | Modalities Available | Subjects | Stimuli | Target Tasks & Labels | Standard Protocols | References in Literature Base |
|---|---|---|---|---|---|---|---|
| **D01** | **DEAP** | EEG (32), ECG, GSR, EMG, RSP, PPG, Temp | 32 | 40 Music Videos (60s) | Valence, Arousal, Dominance (1–9) | 10-Fold CV, LOSO | P0005, P0006, P0007, P0009, P0010, P0011, P0013, P0014, P0016, P0017, P0018, P0019, P0020, P0025, P0030 |
| **D02** | **SEED** | EEG (62 ch) | 15 (3 sessions) | 15 Film Clips (~4m) | 3 Discrete (Positive, Neutral, Negative) | Subject-Dependent, Cross-Session, LOSO | P0002, P0003, P0004, P0005, P0007, P0009, P0011, P0012, P0020, P0025, P0030 |
| **D03** | **SEED-IV** | EEG (62 ch), Eye Tracking | 15 (3 sessions) | 24 Film Clips (~2m) | 4 Discrete (Happy, Sad, Fear, Neutral) | Subject-Dependent, LOSO | P0002, P0008, P0025, P0030 |
| **D04** | **SEED-V** | EEG (62 ch), Eye Tracking | 16 (3 sessions) | 45 Film Clips (~2-4m) | 5 Discrete (Happy, Sad, Fear, Disgust, Neutral) | Subject-Dependent, LOSO | P0008, P0025, P0030 |
| **D05** | **AMIGOS** | EEG (14), ECG (2), GSR (1), RGB/Depth Video | 40 | 16 Short + 4 Long Clips | Valence, Arousal, Dominance, Basic 7 | LOSO, 10-Fold CV | P0001, P0006, P0014, P0030 |
| **D06** | **DREAMER** | EEG (14), ECG (2) | 23 | 18 Film Clips (65–393s) | Valence, Arousal, Dominance (1–5) | LOSO, Within-subject | P0009, P0019, P0020, P0030 |
| **D07** | **MAHNOB-HCI** | EEG (32), ECG, GSR, RSP, Temp, Eye, Face | 27 | 20 Film Clips | Valence, Arousal, Dominance (1–9), Discrete | 10-Fold CV, LOSO | P0009, P0016 |
| **D08** | **Wearable Mobility** | EEG (14), ECG, GSR | 12 | Real-world outdoor routes | 3-Class Environmental Stress | Strict LOSO | P0015 |
| **D09** | **Custom Muse** | EEG (4 dry channels: TP9, AF7, AF8, TP10) | 18 | Audio-Visual clips | Valence, Arousal Binary | LOSO | P0019 |
| **D10** | **PhysioNet Sleep-EDF** | Single/Dual-channel EEG (Fpz-Cz, Pz-Oz) | 60+ | Continuous sleep epochs | Vigilance / Sleep Staging | Cross-Subject Transfer (LOSO) | P0021, P0025 |
| **D11** | **High-Density Affective Imagery** | 64-channel HydroCel EEG | 30 | Autobiographical emotional recall | Valence Microstates A, B, C, D | Subject-Independent Statistical ANOVA | P0022 |
| **D12** | **OpenBHB Simultaneous EEG-fMRI** | Scalp EEG (64 ch) + 3T BOLD fMRI | 80 | Multimodal resting & emotional tasks | Continuous BOLD ROI Regression | Cross-Subject LOSO & Unseen Cohort | P0023 |
| **D13** | **IERQ Emotion Regulation Cohort** | Psychophysiological & Behavioral Metrics | 640 | Standardized emotional scenario prompts | 4 Core Regulation Strategies | Multi-Group Invariance Testing | P0024 |
| **D14** | **Cowen-Keltner 2185 Video Corpus** | Rich Multimedia Emotional Responses | 853 | 2,185 emotionally rich video clips | 27 Continuous Affective Categories | Split-Sample Cross-Validation | P0029 |

---

## Dataset Leakage & Protocol Guidance

1. **Windowing Leakage**:
   - In DEAP, AMIGOS, and continuous series datasets (P0018), overlapping temporal sliding windows must never be partitioned into train/test sets before grouping by trial or subject.
2. **Subject Leakage**:
   - In cross-subject evaluation (P0001, P0007, P0012, P0015, P0016, P0019, P0020, P0021, P0023, P0030), all trials from the test subject must be completely withheld from the training folds (strict LOSO).
3. **Temporal Filtering Leakage**:
   - Linear Dynamic System (LDS) or temporal smoothing filters must be fitted only on training segments and applied independently to test segments.
4. **Sensor Configuration & Referencing Shift**:
   - As demonstrated in P0020 and P0027, transferring models across datasets with different electrode montages requires geometric coordinate embeddings and standardized reference transformations (REST / CAR) to prevent spatial distortion.
