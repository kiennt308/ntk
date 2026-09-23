# HỆ THỐNG PHÂN LOẠI KIẾN TRÚC MÔ HÌNH HỌC ĐA NHIỆM ĐA NHÁNH (TECHNICAL TAXONOMY)
## ĐỀ TÀI TIẾN SĨ: NHẬN DIỆN CẢM XÚC ĐA PHƯƠNG THỨC TỪ TÍN HIỆU Y SINH

Thư mục `06_taxonomy/` cung cấp khung phân loại cấu trúc hoàn chỉnh của các phương pháp học sâu, cơ chế dung hợp và kỹ thuật thích ứng miền được chuẩn hóa cho đề tài.

---

## 1. Cây Phân Loại Cấu Trúc (Hierarchical Taxonomy)

```
Phân Loại Kiến Trúc Nhận Diện Cảm Xúc Y Sinh
│
├── 1. Mạng Trích Xuất Đặc Trưng Đa Nhánh (Multibranch Encoders)
│   ├── Nhánh EEG Không-Thời Gian: 1D/2D-CNN, Spatial GCN / GAT, EEG-Conformer
│   ├── Nhánh Tim Mạch (ECG/PPG): Multi-scale TCN, Wavelet ResNet, HRV-BiLSTM
│   └── Nhánh Da Liễu & Hô Hấp (EDA/GSR/RSP): Continuous Decomposition, Temporal Attention
│
├── 2. Cơ Chế Dung Hợp & Chú Ý Chéo (Cross-Modal Attention & Fusion)
│   ├── Sơ cấp (Early / Feature Concatenation)
│   ├── Tương tác chéo: Multi-Head Cross-Attention (Q_eeg, K_bio, V_bio)
│   ├── Dung hợp đồ thị đa phương thức: Multimodal Heterogeneous Graph
│   └── Dung hợp cấp quyết định (Decision-level & Uncertainty Fusion)
│
├── 3. Học Đa Nhiệm Vụ (Multi-Task Learning Heads)
│   ├── Tối ưu liên hợp Valence - Arousal - Dominance
│   ├── Nhiệm vụ chính (Emotion Classification) + Nhiệm vụ phụ (Subject / Stress / Denoising)
│   └── Động lực chia sẻ tham số: Hard vs Soft Parameter Sharing & Dynamic Task Weighting
│
├── 4. Tách Không Gian Con & Thích Ứng Miền (Disentanglement & Domain Adaptation)
│   ├── Tách không gian biểu diễn: Shared Content (Emotion) vs Private Style (Subject Identity)
│   ├── Thích ứng miền đối kháng: DANN, Multi-Adversarial Domain Adaptation
│   └── Tương thích phân phối: Maximum Mean Discrepancy (MMD), Coral Loss
│
└── 5. Độ Bền Vững Khuyết Thiếu Cảm Biến (Robustness & Missing Modalities)
    ├── Chuyển giao tri thức chéo (Cross-Modal Knowledge Distillation)
    └── Tái tạo tín hiệu khuyết: Masked Autoencoder, Variational Autoencoder (VAE)
```

---

## 2. Các Tài Liệu Phân Tích Chuyên Sâu Từng Khối Kiến Trúc

1. [`01_multibranch_feature_extractors.md`](01_multibranch_feature_extractors.md): Thiết kế các nhánh trích xuất đặc trưng cho từng loại tín hiệu sinh lý.
2. [`02_crossmodal_fusion_mechanisms.md`](02_crossmodal_fusion_mechanisms.md): Cơ chế chú ý chéo và tích hợp thông tin đa giác quan.
3. [`03_multitask_learning_paradigms.md`](03_multitask_learning_paradigms.md): Khung tối ưu đa nhiệm vụ (Multi-task Loss Weighting, Gradient Normalization).
4. [`04_disentanglement_domain_adaptation.md`](04_disentanglement_domain_adaptation.md): Tách biểu diễn và khử phương sai cá nhân (Cross-Subject Generalization).
5. [`05_missing_modality_robustness.md`](05_missing_modality_robustness.md): Chiến lược bảo toàn độ chính xác khi cảm biến bị tháo rời hoặc gián đoạn.
