"""
Leak-Free 23-Fold Leave-One-Subject-Out (LOSO) DataLoader for DREAMER Dataset.

DREAMER Dataset Specifications:
- 23 Subjects (Aged 22-33)
- 18 Film Clip Trials per subject
- Modalities:
    * EEG: 14 channels @ 128 Hz (Emotiv EPOC wireless headset)
    * ECG: 2 channels @ 256 Hz (SHIMMER wireless sensor, resampled to 128 Hz)
- Affect Dimensions: Valence (1-5), Arousal (1-5), Dominance (1-5)
- Baseline: 61s pre-trial baseline per stimulus.

Guarantees:
1. Baseline Subtraction: Mean of 61s baseline subtracted per channel to remove DC shift.
2. Subject-Median Thresholding: Balanced High vs. Low binary targets per subject.
3. Pre-Split Isolated Standardization: Training fold statistics isolated from test fold.
4. Auto-Mock Generator: Creates synthetic DREAMER.mat for smoke tests if file is absent.
"""

import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
try:
    import scipy.io as sio
except ImportError:
    sio = None


class DREAMERSubjectDataset(Dataset):
    """
    In-memory PyTorch Dataset for DREAMER segments.
    DREAMER provides EEG (14 ch) + ECG (2 ch).
    """
    def __init__(self, eeg_data, ecg_data, labels_v, labels_a, bin_v, bin_a):
        self.eeg = torch.tensor(eeg_data, dtype=torch.float32)
        self.ecg = torch.tensor(ecg_data, dtype=torch.float32)
        self.val = torch.tensor(labels_v, dtype=torch.float32)
        self.aro = torch.tensor(labels_a, dtype=torch.float32)
        self.bin_v = torch.tensor(bin_v, dtype=torch.long)
        self.bin_a = torch.tensor(bin_a, dtype=torch.long)

    def __len__(self):
        return len(self.val)

    def __getitem__(self, idx):
        return {
            'eeg': self.eeg[idx],
            'ecg': self.ecg[idx],
            'valence': self.val[idx],
            'arousal': self.aro[idx],
            'valence_bin': self.bin_v[idx],
            'arousal_bin': self.bin_a[idx]
        }


class DREAMERLOSOGenerator:
    """
    Manages 23-Fold Leave-One-Subject-Out evaluation on DREAMER.mat
    """
    def __init__(self, mat_path, window_sec=4, step_sec=2, fs=128,
                 subtract_baseline=True, use_median_split=True):
        self.mat_path = mat_path
        self.win_len = window_sec * fs   # 4s * 128 = 512 points
        self.step_len = step_sec * fs    # 2s * 128 = 256 points
        self.fs = fs
        self.num_subjects = 23
        self.subtract_baseline = subtract_baseline
        self.use_median_split = use_median_split

    def ensure_data_exists(self):
        """
        Creates synthetic DREAMER.mat if not found, allowing immediate smoke-testing.
        """
        if os.path.exists(self.mat_path):
            return
        
        print(f"⚠️ DREAMER file not found at: {self.mat_path}")
        print("🚀 Generating synthetic DREAMER.mat for smoke-testing (23 subjects, 18 trials)...")
        os.makedirs(os.path.dirname(os.path.abspath(self.mat_path)), exist_ok=True)
        
        # Build mock MATLAB struct
        dreamer_dict = {'DREAMER': {'Data': np.empty((1, 23), dtype=object)}}
        for s in range(23):
            subj_data = {}
            # 18 trials
            eeg_trials = np.empty((18, 1), dtype=object)
            ecg_trials = np.empty((18, 1), dtype=object)
            val_scores = np.random.uniform(1.0, 5.0, size=(18, 1))
            aro_scores = np.random.uniform(1.0, 5.0, size=(18, 1))
            
            for t in range(18):
                # Stimulus: 65s (8320 samples @ 128Hz)
                stim_len = 8320
                base_len = 7808 # 61s
                eeg_trials[t, 0] = {
                    'baseline': np.random.randn(base_len, 14).astype(np.float32),
                    'stimuli': np.random.randn(stim_len, 14).astype(np.float32)
                }
                # ECG 256 Hz -> stimulus 16640, baseline 15616
                ecg_trials[t, 0] = {
                    'baseline': np.random.randn(base_len * 2, 2).astype(np.float32),
                    'stimuli': np.random.randn(stim_len * 2, 2).astype(np.float32)
                }
            
            subj_data['EEG'] = eeg_trials
            subj_data['ECG'] = ecg_trials
            subj_data['ScoreValence'] = val_scores
            subj_data['ScoreArousal'] = aro_scores
            dreamer_dict['DREAMER']['Data'][0, s] = subj_data

        if sio is not None:
            sio.savemat(self.mat_path, dreamer_dict)
            print(f"✅ Created synthetic DREAMER file at: {self.mat_path}")

    def load_single_subject(self, subject_idx):
        """
        Loads data for a single subject (0-indexed: 0 to 22).
        Returns segmented tensors and continuous + binary labels.
        """
        self.ensure_data_exists()
        mat = sio.loadmat(self.mat_path, squeeze_me=True, struct_as_record=False)
        dreamer = mat['DREAMER']
        subj = dreamer.Data[subject_idx]

        val_scores = np.array(subj.ScoreValence, dtype=np.float32)
        aro_scores = np.array(subj.ScoreArousal, dtype=np.float32)

        if self.use_median_split:
            thresh_v = np.median(val_scores)
            thresh_a = np.median(aro_scores)
        else:
            thresh_v = 3.0  # Midpoint of 1-5 scale
            thresh_a = 3.0

        eeg_segments = []
        ecg_segments = []
        v_labels = []
        a_labels = []
        v_binary = []
        a_binary = []

        for trial_idx in range(18):
            eeg_obj = subj.EEG[trial_idx]
            ecg_obj = subj.ECG[trial_idx]

            # Raw signals: (time, channels)
            eeg_stim = eeg_obj.stimuli.astype(np.float32)    # (T, 14)
            eeg_base = eeg_obj.baseline.astype(np.float32)   # (T_b, 14)
            ecg_stim = ecg_obj.stimuli.astype(np.float32)    # (T*2, 2) @ 256Hz
            ecg_base = ecg_obj.baseline.astype(np.float32)   # (T_b*2, 2) @ 256Hz

            # Downsample ECG from 256Hz to 128Hz (factor 2)
            ecg_stim = ecg_stim[::2, :]
            ecg_base = ecg_base[::2, :]

            # Baseline Subtraction (Trừ điện thế nền)
            if self.subtract_baseline:
                eeg_stim = eeg_stim - np.mean(eeg_base, axis=0, keepdims=True)
                ecg_stim = ecg_stim - np.mean(ecg_base, axis=0, keepdims=True)

            # Transpose to (channels, time)
            eeg_stim = eeg_stim.T  # (14, T)
            ecg_stim = ecg_stim.T  # (2, T)

            min_len = min(eeg_stim.shape[1], ecg_stim.shape[1])
            v = val_scores[trial_idx]
            a = aro_scores[trial_idx]
            bin_v = 1 if v >= thresh_v else 0
            bin_a = 1 if a >= thresh_a else 0

            # Window slicing
            for start in range(0, min_len - self.win_len + 1, self.step_len):
                end = start + self.win_len
                eeg_segments.append(eeg_stim[:, start:end])
                ecg_segments.append(ecg_stim[:, start:end])
                v_labels.append(v)
                a_labels.append(a)
                v_binary.append(bin_v)
                a_binary.append(bin_a)

        return (
            np.array(eeg_segments, dtype=np.float32),
            np.array(ecg_segments, dtype=np.float32),
            np.array(v_labels, dtype=np.float32),
            np.array(a_labels, dtype=np.float32),
            np.array(v_binary, dtype=np.int64),
            np.array(a_binary, dtype=np.int64)
        )

    def get_loso_fold(self, test_subject_idx, total_subjects=23, batch_size=64):
        """
        Builds Fold where test_subject_idx is test, remaining 22 subjects are train.
        Strict Pre-split Isolated Standardization.
        """
        print(f"\n[DREAMER LOSO] Preparing Fold: Test Subject = #{test_subject_idx + 1:02d} ...")
        train_eeg, train_ecg = [], []
        train_v, train_a = [], []
        train_bv, train_ba = [], []
        test_data = None

        for s_idx in range(total_subjects):
            eeg, ecg, v, a, bv, ba = self.load_single_subject(s_idx)
            if s_idx == test_subject_idx:
                test_data = (eeg, ecg, v, a, bv, ba)
            else:
                train_eeg.append(eeg)
                train_ecg.append(ecg)
                train_v.append(v)
                train_a.append(a)
                train_bv.append(bv)
                train_ba.append(ba)

        train_eeg = np.concatenate(train_eeg, axis=0)
        train_ecg = np.concatenate(train_ecg, axis=0)
        train_v = np.concatenate(train_v, axis=0)
        train_a = np.concatenate(train_a, axis=0)
        train_bv = np.concatenate(train_bv, axis=0)
        train_ba = np.concatenate(train_ba, axis=0)

        test_eeg, test_ecg, test_v, test_a, test_bv, test_ba = test_data

        # Isolated Normalization
        eeg_mean, eeg_std = train_eeg.mean(), train_eeg.std() + 1e-8
        ecg_mean, ecg_std = train_ecg.mean(), train_ecg.std() + 1e-8

        train_eeg = (train_eeg - eeg_mean) / eeg_std
        test_eeg = (test_eeg - eeg_mean) / eeg_std

        train_ecg = (train_ecg - ecg_mean) / ecg_std
        test_ecg = (test_ecg - ecg_mean) / ecg_std

        train_dataset = DREAMERSubjectDataset(train_eeg, train_ecg, train_v, train_a, train_bv, train_ba)
        test_dataset = DREAMERSubjectDataset(test_eeg, test_ecg, test_v, test_a, test_bv, test_ba)

        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

        print(f"  Train windows: {len(train_dataset):,}")
        print(f"  Test windows (Subject #{test_subject_idx + 1:02d}): {len(test_dataset):,}")

        return train_loader, test_loader
