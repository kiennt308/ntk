"""
MMB-EmotionNet: Physiologically-Informed Multimodal Representation and Directional Fusion
for EEG–Peripheral Biosignal Emotion Recognition

Core Modules:
1. Physics-Informed Heterogeneous Encoders (ST-GCN/2D-CNN for EEG, 1D-TCN for ECG, CWT/1D-CNN for EDA)
2. Shared-Private Subspace Disentanglement Module (L_sim, L_diff, L_recon)
3. Directional Cross-Modal Attention Module (Q_EEG -> K,V_Bio)
4. Multi-Task Homoscedastic Uncertainty Head (Valence & Arousal)

Multi-Benchmark Adaptability:
- Supports DEAP (32 EEG + 1 ECG/PPG + 1 EDA/GSR)
- Supports DREAMER (14 EEG + 2 ECG, with EDA bypassed gracefully)
- Loss Scheduling: Orthogonality weight annealing (beta warm-up)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class EEGEncoder(nn.Module):
    """
    Spatial-temporal encoder tailored for multi-channel scalp EEG montages (10-20 system).
    Input shape: (Batch, in_channels, Time)
    Output shape: (Batch, d_latent)
    """
    def __init__(self, in_channels=32, d_latent=128):
        super().__init__()
        # Temporal convolution across sampling points
        self.conv_time = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(1, 31), padding=(0, 15), bias=False),
            nn.BatchNorm2d(16),
            nn.ELU()
        )
        # Spatial convolution across electrode locations
        self.conv_spatial = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=(in_channels, 1), bias=False),
            nn.BatchNorm2d(32),
            nn.ELU(),
            nn.AvgPool2d(kernel_size=(1, 4))
        )
        # Spatio-temporal summary
        self.temporal_summary = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=(1, 15), padding=(0, 7), bias=False),
            nn.BatchNorm2d(64),
            nn.ELU(),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        self.fc = nn.Linear(64, d_latent)

    def forward(self, x):
        # x: (Batch, Channels, Time) -> (Batch, 1, Channels, Time)
        x = x.unsqueeze(1)
        x = self.conv_time(x)
        x = self.conv_spatial(x)
        x = self.temporal_summary(x)
        x = torch.flatten(x, 1)
        return self.fc(x)


class ECGEncoder(nn.Module):
    """
    Dilated 1D Temporal Convolutional Network (TCN) capturing cardiac cycles and R-peaks.
    Input shape: (Batch, in_channels, Time) (1 channel in DEAP, 2 channels in DREAMER)
    Output shape: (Batch, d_latent)
    """
    def __init__(self, in_channels=1, d_latent=128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(in_channels, 32, kernel_size=15, stride=2, padding=7),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Conv1d(32, 64, kernel_size=9, stride=2, padding=4, dilation=2),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Conv1d(64, 128, kernel_size=5, stride=2, padding=2, dilation=4),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )
        self.fc = nn.Linear(128, d_latent)

    def forward(self, x):
        feat = self.net(x).squeeze(-1)
        return self.fc(feat)


class EDAEncoder(nn.Module):
    """
    Multi-scale convolutional encoder decomposing slow tonic baseline from phasic SCR bursts.
    Input shape: (Batch, 1, Time)
    Output shape: (Batch, d_latent)
    """
    def __init__(self, in_channels=1, d_latent=128):
        super().__init__()
        # Parallel multi-scale temporal kernels
        self.branch_tonic = nn.Sequential(
            nn.Conv1d(in_channels, 32, kernel_size=31, stride=2, padding=15),
            nn.BatchNorm1d(32),
            nn.ReLU()
        )
        self.branch_phasic = nn.Sequential(
            nn.Conv1d(in_channels, 32, kernel_size=9, stride=2, padding=4),
            nn.BatchNorm1d(32),
            nn.ReLU()
        )
        self.merge = nn.Sequential(
            nn.Conv1d(64, 128, kernel_size=5, stride=2, padding=2),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )
        self.fc = nn.Linear(128, d_latent)

    def forward(self, x):
        h_tonic = self.branch_tonic(x)
        h_phasic = self.branch_phasic(x)
        merged = torch.cat([h_tonic, h_phasic], dim=1)
        feat = self.merge(merged).squeeze(-1)
        return self.fc(feat)


class SubspaceDisentangler(nn.Module):
    """
    Shared-Private Subspace Disentanglement Module.
    Decomposes each modality's latent feature E_m into:
      - Z_m^s: Shared Subspace (modality-invariant emotional semantics)
      - Z_m^p: Private Subspace (sensor artifacts and individual baseline noise)
    Constrained by Similarity, Orthogonal Difference, and Reconstruction losses.
    Gracefully handles absence of EDA (e.g. on DREAMER).
    """
    def __init__(self, d_latent=128, d_subspace=64, has_eda=True):
        super().__init__()
        self.d_subspace = d_subspace
        self.has_eda = has_eda
        
        # Shared Projection Heads
        self.proj_shared_eeg = nn.Linear(d_latent, d_subspace)
        self.proj_shared_ecg = nn.Linear(d_latent, d_subspace)
        
        # Private Projection Heads
        self.proj_private_eeg = nn.Linear(d_latent, d_subspace)
        self.proj_private_ecg = nn.Linear(d_latent, d_subspace)
        
        # Reconstruction Decoders
        self.decoder_eeg = nn.Linear(d_subspace * 2, d_latent)
        self.decoder_ecg = nn.Linear(d_subspace * 2, d_latent)

        if has_eda:
            self.proj_shared_eda = nn.Linear(d_latent, d_subspace)
            self.proj_private_eda = nn.Linear(d_latent, d_subspace)
            self.decoder_eda = nn.Linear(d_subspace * 2, d_latent)

    def forward(self, e_eeg, e_ecg, e_eda=None):
        # Project EEG & ECG to Shared & Private
        z_s_eeg = F.normalize(self.proj_shared_eeg(e_eeg), p=2, dim=-1)
        z_s_ecg = F.normalize(self.proj_shared_ecg(e_ecg), p=2, dim=-1)
        z_p_eeg = F.normalize(self.proj_private_eeg(e_eeg), p=2, dim=-1)
        z_p_ecg = F.normalize(self.proj_private_ecg(e_ecg), p=2, dim=-1)
        
        rec_eeg = self.decoder_eeg(torch.cat([z_s_eeg, z_p_eeg], dim=-1))
        rec_ecg = self.decoder_ecg(torch.cat([z_s_ecg, z_p_ecg], dim=-1))

        if self.has_eda and e_eda is not None:
            z_s_eda = F.normalize(self.proj_shared_eda(e_eda), p=2, dim=-1)
            z_p_eda = F.normalize(self.proj_private_eda(e_eda), p=2, dim=-1)
            rec_eda = self.decoder_eda(torch.cat([z_s_eda, z_p_eda], dim=-1))

            # 1. Difference Loss (Frobenius-norm soft orthogonality)
            l_diff = (
                torch.norm(torch.mm(z_s_eeg.t(), z_p_eeg), p='fro')**2 +
                torch.norm(torch.mm(z_s_ecg.t(), z_p_ecg), p='fro')**2 +
                torch.norm(torch.mm(z_s_eda.t(), z_p_eda), p='fro')**2
            ) / (self.d_subspace**2)

            # 2. Similarity Loss
            l_sim = (
                F.mse_loss(z_s_eeg, z_s_ecg) +
                F.mse_loss(z_s_eeg, z_s_eda) +
                F.mse_loss(z_s_ecg, z_s_eda)
            ) / 3.0

            # 3. Reconstruction Loss
            l_recon = (
                F.mse_loss(rec_eeg, e_eeg) +
                F.mse_loss(rec_ecg, e_ecg) +
                F.mse_loss(rec_eda, e_eda)
            ) / 3.0

            return (z_s_eeg, z_s_ecg, z_s_eda), (z_p_eeg, z_p_ecg, z_p_eda), (l_sim, l_diff, l_recon)
        else:
            # 2 Modalities (EEG + ECG) for DREAMER
            l_diff = (
                torch.norm(torch.mm(z_s_eeg.t(), z_p_eeg), p='fro')**2 +
                torch.norm(torch.mm(z_s_ecg.t(), z_p_ecg), p='fro')**2
            ) / (self.d_subspace**2)

            l_sim = F.mse_loss(z_s_eeg, z_s_ecg)
            l_recon = (F.mse_loss(rec_eeg, e_eeg) + F.mse_loss(rec_ecg, e_ecg)) / 2.0

            return (z_s_eeg, z_s_ecg, None), (z_p_eeg, z_p_ecg, None), (l_sim, l_diff, l_recon)


class DirectionalCrossAttention(nn.Module):
    """
    Directional Cross-Modal Attention Module.
    Neurobiologically grounded: Central Nervous System (EEG) acts as the Query (Q_EEG) anchor,
    directing attention over Key & Value of Autonomic Peripheral signals (K_Bio, V_Bio).
    """
    def __init__(self, d_subspace=64, n_heads=4):
        super().__init__()
        self.n_heads = n_heads
        self.d_head = d_subspace // n_heads
        
        self.w_q = nn.Linear(d_subspace, d_subspace)
        self.w_k = nn.Linear(d_subspace, d_subspace)
        self.w_v = nn.Linear(d_subspace, d_subspace)
        
        self.out_proj = nn.Linear(d_subspace, d_subspace)
        self.norm = nn.LayerNorm(d_subspace)

    def forward(self, z_s_eeg, z_s_ecg, z_s_eda=None):
        if z_s_eda is not None:
            bio_seq = torch.stack([z_s_ecg, z_s_eda], dim=1) # (B, 2, d)
        else:
            bio_seq = z_s_ecg.unsqueeze(1)                   # (B, 1, d)
        
        # Q from EEG: (Batch, 1, d_subspace)
        q = self.w_q(z_s_eeg.unsqueeze(1))
        # K, V from Peripheral: (Batch, K_len, d_subspace)
        k = self.w_k(bio_seq)
        v = self.w_v(bio_seq)
        
        scores = torch.bmm(q, k.transpose(1, 2)) / (self.d_head ** 0.5)
        attn_weights = F.softmax(scores, dim=-1)
        
        attended_bio = torch.bmm(attn_weights, v).squeeze(1)
        fused = self.norm(z_s_eeg + self.out_proj(attended_bio))
        return fused, attn_weights


class HomoscedasticMultiTaskHead(nn.Module):
    """
    Multi-Task Learning Head with Kendall Homoscedastic Aleatoric Uncertainty Loss Balancing.
    Eliminates negative gradient competition between Valence and Arousal.
    """
    def __init__(self, d_in=64):
        super().__init__()
        self.valence_head = nn.Sequential(
            nn.Linear(d_in, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
        self.arousal_head = nn.Sequential(
            nn.Linear(d_in, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
        
        # Learnable log-variance parameters log(sigma^2)
        self.log_var_v = nn.Parameter(torch.zeros(1))
        self.log_var_a = nn.Parameter(torch.zeros(1))

    def forward(self, fused_rep):
        pred_v = self.valence_head(fused_rep).squeeze(-1)
        pred_a = self.arousal_head(fused_rep).squeeze(-1)
        return pred_v, pred_a

    def compute_mtl_loss(self, pred_v, target_v, pred_a, target_a):
        l_v = F.mse_loss(pred_v, target_v)
        l_a = F.mse_loss(pred_a, target_a)
        
        precision_v = torch.exp(-self.log_var_v)
        precision_a = torch.exp(-self.log_var_a)
        
        loss_mtl = (
            0.5 * precision_v * l_v + 0.5 * self.log_var_v +
            0.5 * precision_a * l_a + 0.5 * self.log_var_a
        )
        return loss_mtl, l_v.item(), l_a.item()


class MMBEmotionNet(nn.Module):
    """
    Unified MMB-EmotionNet End-to-End Pipeline.
    Supports both 3-modality (DEAP) and 2-modality (DREAMER).
    """
    def __init__(self, eeg_channels=32, ecg_channels=1, eda_channels=1,
                 d_latent=128, d_subspace=64, has_eda=True):
        super().__init__()
        self.has_eda = has_eda
        
        # 1. Physics-Informed Encoders
        self.enc_eeg = EEGEncoder(in_channels=eeg_channels, d_latent=d_latent)
        self.enc_ecg = ECGEncoder(in_channels=ecg_channels, d_latent=d_latent)
        if has_eda and eda_channels > 0:
            self.enc_eda = EDAEncoder(in_channels=eda_channels, d_latent=d_latent)
        else:
            self.enc_eda = None
            self.has_eda = False
        
        # 2. Shared-Private Subspace Disentangler
        self.disentangler = SubspaceDisentangler(d_latent=d_latent, d_subspace=d_subspace, has_eda=self.has_eda)
        
        # 3. Directional Cross-Modal Attention
        self.cross_attn = DirectionalCrossAttention(d_subspace=d_subspace)
        
        # 4. Multi-Task Uncertainty Head
        self.mtl_head = HomoscedasticMultiTaskHead(d_in=d_subspace)

    def forward(self, x_eeg, x_ecg, x_eda=None):
        e_eeg = self.enc_eeg(x_eeg)
        e_ecg = self.enc_ecg(x_ecg)
        e_eda = self.enc_eda(x_eda) if (self.has_eda and x_eda is not None) else None
        
        (z_s_eeg, z_s_ecg, z_s_eda), (z_p_eeg, z_p_ecg, z_p_eda), (l_sim, l_diff, l_recon) = \
            self.disentangler(e_eeg, e_ecg, e_eda)
        
        fused_rep, attn_weights = self.cross_attn(z_s_eeg, z_s_ecg, z_s_eda)
        pred_v, pred_a = self.mtl_head(fused_rep)
        
        return {
            'pred_v': pred_v,
            'pred_a': pred_a,
            'fused_rep': fused_rep,
            'attn_weights': attn_weights,
            'l_sim': l_sim,
            'l_diff': l_diff,
            'l_recon': l_recon
        }

    @staticmethod
    def get_beta_weight(epoch, max_epochs=20, warmup_epochs=5, beta_target=0.1):
        """
        Đòn bẩy 4: Lịch trình khởi động trực giao (Orthogonality Annealing Schedule).
        Giữ beta = 0 trong giai đoạn đầu, sau đó tăng dần đến beta_target.
        """
        if epoch < warmup_epochs:
            return 0.0
        elif epoch >= warmup_epochs and epoch < (warmup_epochs + 5):
            progress = (epoch - warmup_epochs) / 5.0
            return progress * beta_target
        else:
            return beta_target

    def compute_loss(self, outputs, target_v, target_a, beta_weight=0.1, alpha=0.5, gamma=1.0):
        """
        Computes joint objective:
        L_total = L_Kendall(Valence, Arousal) + alpha * L_sim + beta * L_diff + gamma * L_recon
        """
        l_mtl, l_v_mse, l_a_mse = self.mtl_head.compute_mtl_loss(
            outputs['pred_v'], target_v, outputs['pred_a'], target_a
        )
        l_disentangle = alpha * outputs['l_sim'] + beta_weight * outputs['l_diff'] + gamma * outputs['l_recon']
        total_loss = l_mtl + l_disentangle
        
        return {
            'total_loss': total_loss,
            'loss_mtl': l_mtl,
            'l_v_mse': l_v_mse,
            'l_a_mse': l_a_mse,
            'l_sim': outputs['l_sim'],
            'l_diff': outputs['l_diff'],
            'l_recon': outputs['l_recon'],
            'sigma_v': torch.exp(0.5 * self.mtl_head.log_var_v).item(),
            'sigma_a': torch.exp(0.5 * self.mtl_head.log_var_a).item()
        }
