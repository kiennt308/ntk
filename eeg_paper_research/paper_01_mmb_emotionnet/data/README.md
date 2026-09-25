# Dataset Setup & Preparation Guide: DEAP & DREAMER

This document details the exact dataset characteristics, channel indexing, and anti-leakage loading protocols for **MMB-EmotionNet**.

---

## 1. Primary Benchmark: DEAP (Database for Emotion Analysis using Physiological Signals)

- **Official Citation**: Koelstra, S. et al., "DEAP: A Database for Emotion Analysis Using Physiological Signals," *IEEE Transactions on Affective Computing*, vol. 3, no. 1, pp. 18–31, 2012.
- **Access URL**: https://www.eecs.qmul.ac.uk/mmv/datasets/deap/
- **Official Format Used**: `data_preprocessed_python.zip` (contains 32 Python pickle `.dat` files from `s01.dat` to `s32.dat`).

### A. Data Layout per File (`sXX.dat`):
Each `.dat` file is a dictionary containing two arrays:
1. **`data`**: Array of shape `(40, 40, 8064)`
   - `40` video trials (each 63 seconds total = 3s pre-trial fixation baseline + 60s stimulus).
   - `40` channels sampled at $128\text{ Hz}$ ($63 \times 128 = 8,064$ time points).
   - **Channel Index Mapping (0-indexed)**:
     - **Channels 0 – 31 (32 channels)**: Scalp EEG (10–20 system: Fp1, AF3, F3, F7, FC5, FC1, C3, T7, CP5, CP1, P3, P7, Pz, O1, Oz, O2, P4, P8, CP6, CP2, Cz, C4, T8, FC6, FC2, F4, F8, AF4, Fp2, Fz, Pz, Cz).
     - **Channels 32 – 33**: EOG (Horizontal, Vertical).
     - **Channels 34 – 35**: EMG (Zygomaticus Major, Trapezius).
     - **Channel 36**: **GSR / EDA** (Electrodermal Activity, Skin Conductance).
     - **Channel 37**: **Respiration** (Chest belt expansion).
     - **Channel 38**: **PPG / BVP** (Plethysmograph, Blood Volume Pulse / Heart Rate).
     - **Channel 39**: **Temperature** (Skin temperature in Celsius).
2. **`labels`**: Array of shape `(40, 4)`
   - Column 0: **Valence** (Continuous rating from 1.0 to 9.0).
   - Column 1: **Arousal** (Continuous rating from 1.0 to 9.0).
   - Column 2: **Dominance** (Continuous rating from 1.0 to 9.0).
   - Column 3: **Liking** (Continuous rating from 1.0 to 9.0).

### B. MMB-EmotionNet Input Tensor Construction:
- **EEG Tensor**: Channels `0:32` $\rightarrow$ Shape: `(Batch, 32, Time)`
- **ECG / PPG Tensor**: Channel `38` (BVP/PPG) $\rightarrow$ Shape: `(Batch, 1, Time)`
- **EDA Tensor**: Channel `36` (GSR/EDA) $\rightarrow$ Shape: `(Batch, 1, Time)`
- **Target Multi-Task Labels**:
  - Continuous Regression Head: $(y_V, y_A) \in [1, 9]^2$
  - Binary Threshold Split: High ($\ge 5.0$) vs Low ($< 5.0$)

---

## 2. Secondary Dual-Benchmark: DREAMER

- **Official Citation**: Katsigiannis, S. & Ramzan, N., "DREAMER: A Database for Emotion Recognition Through EEG and ECG Signals from Wireless Low-cost Off-the-Shelf Devices," *IEEE Journal of Biomedical and Health Informatics*, vol. 22, no. 1, pp. 98–107, 2018.
- **Subject Count**: 23 healthy participants.
- **Modalities**:
  - **14-channel EEG** (Emotiv EPOC wireless headset, $128\text{ Hz}$).
  - **2-channel ECG** (Shimmer wireless sensor, $256\text{ Hz}$).
- **Target Labels**: Continuous Valence, Arousal, Dominance (1 to 5 scale).

---

## 3. Forensic Anti-Leakage Execution Protocol

To eliminate the methodological flaws identified in prior literature (such as Paper 4 reporting >99% via random sample splitting):

1. **Pre-Windowing Subject Isolation**:
   - The dataset must be split **by subject ID** BEFORE any sliding window segmentation.
   - For 32-fold Leave-One-Subject-Out (LOSO): In fold $k$, all 40 trials of subject $k$ form the test set; all trials of the remaining 31 subjects form the train/val set.
2. **Pre-Split Isolated Standardization**:
   - Z-score normalization parameters ($\mu, \sigma$) must be computed strictly on the training folds.
   - Never apply global dataset-wide scaling across all subjects.
3. **Zero Window Overlap Leakage**:
   - Overlapping segments from the same continuous trial must never be distributed across both training and test partitions.
