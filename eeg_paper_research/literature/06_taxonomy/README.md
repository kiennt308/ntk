# HỆ THỐNG PHÂN LOẠI KIẾN TRÚC MÔ HÌNH HỌC ĐA NHIỆM ĐA NHÁNH (TECHNICAL TAXONOMY & MATHEMATICAL FRAMEWORK)
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH ĐA PHƯƠNG THỨC

Thư mục `06_taxonomy/` cung cấp khung phân loại cấu trúc kỹ thuật hoàn chỉnh và cơ sở toán học chặt chẽ cho toàn bộ các khối kiến trúc của mô hình đề xuất (**MMB-EmotionNet**).

---

## 🏛️ 1. Sơ Đồ Kiến Trúc Hệ Thống Tổng Thể (MMB-EmotionNet Architecture)

```
[Tín hiệu Y Sinh Đa Phương Thức]
 ├── EEG (62/32/14 ch) ──> [Nhánh EEG: Spatial-Temporal GCN / EEGNet] ─────> H_eeg ──┐
 ├── ECG (1/2/3 ch)    ──> [Nhánh ECG: Multi-Scale Dilated 1D-CNN]    ─────> H_ecg ──┼──> [Tầng Tách Không Gian Con]
 └── EDA (1 ch)        ──> [Nhánh EDA: Continuous Wavelet 1D-CNN]     ─────> H_eda ──┘     ├── Z_shared (Cảm xúc chung)
                                                                                           └── Z_private (Đặc thù cá nhân)
                                                                                                    │
                                                                                                    ▼
                                                                                   [Cơ Chế Chú Ý Chéo Đa Phương Thức]
                                                                                   (Cross-Modal QKV Attention Fusion)
                                                                                                    │
                                                                                                    ▼
                                                                                   [Tầng Học Đa Nhiệm Vụ Thích Ứng]
                                                                                   (Homoscedastic Uncertainty MTL)
                                                                                                    ├── Head 1: Valence (Reg/Cls)
                                                                                                    ├── Head 2: Arousal (Reg/Cls)
                                                                                                    ├── Head 3: Dominance (Reg/Cls)
                                                                                                    └── Head 4: Subject Invariance (GRL)
```

---

## 📐 2. Các Chuyên Đề Phân Tích Kỹ Thuật Chi Tiết

| Chuyên Đề Kiến Trúc | Nội Dung & Công Thức Toán Học Trọng Tâm | Tài Liệu Chi Tiết |
| :--- | :--- | :--- |
| **Khối 1: Bộ Mã Hóa Đa Nhánh** | Xử lý vật lý chuyên biệt: Spatial Depthwise Conv cho EEG, Dilated TCN cho HRV, CWT cho EDA. | [`01_multibranch_feature_extractors.md`](01_multibranch_feature_extractors.md) |
| **Khối 2: Chú Ý Chéo (Cross-Attention)** | Tương tác hai chiều $Attention(Q_{EEG}, K_{Bio}, V_{Bio})$ và dung hợp đa tầng QKV. | [`02_crossmodal_fusion_mechanisms.md`](02_crossmodal_fusion_mechanisms.md) |
| **Khối 3: Học Đa Nhiệm Vụ (MTL)** | Hàm mất mát tổng quát Kendall Loss $\mathcal{L}_{MTL} = \sum \frac{1}{2\sigma_i^2}\mathcal{L}_i + \log\sigma_i$ & cân bằng GradNorm. | [`03_multitask_learning_paradigms.md`](03_multitask_learning_paradigms.md) |
| **Khối 4: Tách Không Gian Con & Thích Ứng Miền** | Ràng buộc trực giao $\|Z_{shared}^T Z_{private}\|_F^2$ và thích ứng miền đối kháng DANN qua GRL. | [`04_disentanglement_domain_adaptation.md`](04_disentanglement_domain_adaptation.md) |
| **Khối 5: Bền Vững Khuyết Thiếu Cảm Biến** | Chưng cất tri thức đa phương thức (Cross-Modal KD), Teacher-Student và Masked Biosignal Modeling. | [`05_missing_modality_robustness.md`](05_missing_modality_robustness.md) |
