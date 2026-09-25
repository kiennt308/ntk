"""
Leak-Free 32-Fold Leave-One-Subject-Out (LOSO) DataLoader for DEAP Dataset.

Enhanced Features for SOTA Generalization:
1. Baseline Subtraction (Trừ điện thế nền 3s đầu): Neutralizes subject-specific DC offsets and impedance drift.
2. Subject-Median Thresholding: Calculates balanced High vs. Low binary targets per subject.
3. Pre-Split Isolated Standardization: Mean and standard deviation are computed strictly on training folds.
4. Zero Window Overlap Leakage across partitions.
"""

import os
import pickle
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader


class DEAPSubjectFoldDataset(Dataset):
    """
    In-memory PyTorch Dataset for DEAP segments.
    Provides both continuous ratings (for Kendall multi-task regression)
    and binary class labels (for Accuracy/Macro-F1 evaluation).
    """
    def __init__(self, eeg_data, ecg_data, eda_data, labels_v, labels_a, bin_v, bin_a):
        self.eeg = torch.tensor(eeg_data, dtype=torch.float32)
        self.ecg = torch.tensor(ecg_data, dtype=torch.float32)
        self.eda = torch.tensor(eda_data, dtype=torch.float32)
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
            'eda': self.eda[idx],
            'valence': self.val[idx],
            'arousal': self.aro[idx],
            'valence_bin': self.bin_v[idx],
            'arousal_bin': self.bin_a[idx]
        }


class DEAPLOSOGenerator:
    """
    Generates 32 leak-free cross-validation folds from preprocessed DEAP pickle files.
    """
    def __init__(self, data_dir, window_size_sec=4, step_size_sec=2, sampling_rate=128,
                 subtract_baseline=True, use_median_split=True):
        self.data_dir = data_dir
        self.window_size = window_size_sec * sampling_rate  # 4s * 128 = 512 points
        self.step_size = step_size_sec * sampling_rate      # 2s * 128 = 256 points
        self.fs = sampling_rate
        self.num_subjects = 32
        self.subtract_baseline = subtract_baseline
        self.use_median_split = use_median_split

    def load_single_subject(self, subject_id):
        """
        Loads sXX.dat (subject_id from 1 to 32).
        Returns segmented tensors and continuous + binary labels for all 40 trials of this subject.
        """
        file_name = f"s{subject_id:02d}.dat"
        file_path = os.path.join(self.data_dir, file_name)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"DEAP file not found: {file_path}")

        with open(file_path, 'rb') as f:
            content = pickle.load(f, encoding='latin1')

        # raw data: (40 trials, 40 channels, 8064 points)
        # 0:384 (3s baseline @ 128Hz), 384:8064 (60s stimulus @ 128Hz)
        raw_stimulus = content['data'][:, :, 384:]  # (40, 40, 7680)
        labels = content['labels']                  # (40, 4) -> [Valence, Arousal, Dominance, Liking]

        # Đòn bẩy kỹ thuật 1: Baseline Subtraction (Trừ điện thế nền cá nhân)
        if self.subtract_baseline:
            baseline_mean = content['data'][:, :, :384].mean(axis=-1, keepdims=True)  # (40, 40, 1)
            raw_stimulus = raw_stimulus - baseline_mean

        # Đòn bẩy kỹ thuật 3: Phân ngưỡng nhãn cân bằng
        if self.use_median_split:
            thresh_v = np.median(labels[:, 0])
            thresh_a = np.median(labels[:, 1])
        else:
            thresh_v = 5.0
            thresh_a = 5.0

        eeg_segments = []
        ecg_segments = []
        eda_segments = []
        v_labels = []
        a_labels = []
        v_binary = []
        a_binary = []

        total_points = raw_stimulus.shape[2]
        
        for trial_idx in range(40):
            trial_signal = raw_stimulus[trial_idx]
            v = labels[trial_idx, 0]
            a = labels[trial_idx, 1]
            bin_v = 1 if v >= thresh_v else 0
            bin_a = 1 if a >= thresh_a else 0

            # Slide window across 60 seconds
            for start in range(0, total_points - self.window_size + 1, self.step_size):
                end = start + self.window_size
                
                # Channels 0:32 -> EEG (Cortical 10-20 system)
                eeg_segments.append(trial_signal[0:32, start:end])
                # Channel 38 -> BVP/PPG (Cardiac peripheral pulse)
                ecg_segments.append(trial_signal[38:39, start:end])
                # Channel 36 -> GSR/EDA (Electrodermal response)
                eda_segments.append(trial_signal[36:37, start:end])
                
                v_labels.append(v)
                a_labels.append(a)
                v_binary.append(bin_v)
                a_binary.append(bin_a)

        return (
            np.array(eeg_segments, dtype=np.float32),
            np.array(ecg_segments, dtype=np.float32),
            np.array(eda_segments, dtype=np.float32),
            np.array(v_labels, dtype=np.float32),
            np.array(a_labels, dtype=np.float32),
            np.array(v_binary, dtype=np.int64),
            np.array(a_binary, dtype=np.int64)
        )

    def get_loso_fold(self, test_subject_id, total_subjects=32, batch_size=64):
        """
        Builds Fold where test_subject_id is the test set, and all remaining subjects are train.
        Normalizes strictly using train statistics (Pre-split Isolated Standardization).
        """
        print(f"\n[LOSO Setup] Preparing Fold: Test Subject = s{test_subject_id:02d} (Baseline Subtraction={self.subtract_baseline}) ...")
        
        train_eeg, train_ecg, train_eda = [], [], []
        train_v, train_a = [], []
        train_bv, train_ba = [], []
        test_data = None

        for sid in range(1, total_subjects + 1):
            if not os.path.exists(os.path.join(self.data_dir, f"s{sid:02d}.dat")):
                continue
            eeg, ecg, eda, v, a, bv, ba = self.load_single_subject(sid)
            if sid == test_subject_id:
                test_data = (eeg, ecg, eda, v, a, bv, ba)
            else:
                train_eeg.append(eeg)
                train_ecg.append(ecg)
                train_eda.append(eda)
                train_v.append(v)
                train_a.append(a)
                train_bv.append(bv)
                train_ba.append(ba)

        if test_data is None:
            raise ValueError(f"Test subject s{test_subject_id:02d}.dat not found in {self.data_dir}")

        train_eeg = np.concatenate(train_eeg, axis=0)
        train_ecg = np.concatenate(train_ecg, axis=0)
        train_eda = np.concatenate(train_eda, axis=0)
        train_v = np.concatenate(train_v, axis=0)
        train_a = np.concatenate(train_a, axis=0)
        train_bv = np.concatenate(train_bv, axis=0)
        train_ba = np.concatenate(train_ba, axis=0)

        test_eeg, test_ecg, test_eda, test_v, test_a, test_bv, test_ba = test_data

        # Pre-Split Isolated Standardization (Zero Leakage)
        eeg_mean, eeg_std = train_eeg.mean(), train_eeg.std() + 1e-8
        ecg_mean, ecg_std = train_ecg.mean(), train_ecg.std() + 1e-8
        eda_mean, eda_std = train_eda.mean(), train_eda.std() + 1e-8

        train_eeg = (train_eeg - eeg_mean) / eeg_std
        test_eeg = (test_eeg - eeg_mean) / eeg_std

        train_ecg = (train_ecg - ecg_mean) / ecg_std
        test_ecg = (test_ecg - ecg_mean) / ecg_std

        train_eda = (train_eda - eda_mean) / eda_std
        test_eda = (test_eda - eda_mean) / eda_std

        train_dataset = DEAPSubjectFoldDataset(train_eeg, train_ecg, train_eda, train_v, train_a, train_bv, train_ba)
        test_dataset = DEAPSubjectFoldDataset(test_eeg, test_ecg, test_eda, test_v, test_a, test_bv, test_ba)

        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

        print(f"  Train samples: {len(train_dataset):,} windows")
        print(f"  Test samples (Subject s{test_subject_id:02d}): {len(test_dataset):,} windows")
        
        return train_loader, test_loader
