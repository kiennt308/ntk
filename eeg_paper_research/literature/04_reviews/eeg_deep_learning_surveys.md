# Tổng Hợp Khảo Sát: Các Kiến Trúc Deep Learning Cho Tín Hiệu Não (EEG)

## 1. Xu Hướng Chuyển Dịch Kiến Trúc (2023–2026)

1. **Từ CNN truyền thống sang Spatial-Temporal GNN & Transformer**:
   - Các mô hình như **LGGNet** (Ding et al., IEEE TNNLS 2023) và **EEGformer** (Wan et al., 2023) khai thác cấu trúc đồ thị động (Dynamic Brain Connectivity) giữa các điện cực não bộ trên mạng 10-20.
2. **Học Đa Nhiệm Vụ (Multi-Task Learning - MTL)**:
   - Thay vì huấn luyện các mô hình phân loại nhị phân riêng rẽ cho Valence và Arousal, mạng đa nhiệm sử dụng Shared Encoder + Task-Specific Heads giúp chia sẻ biểu diễn ngữ nghĩa và giảm hiện tượng Overfitting.
3. **Tách Biểu Diễn (Subspace Disentanglement)**:
   - Tách không gian biểu diễn thành 2 phần: $Z_{shared}$ (biểu diễn cảm xúc dùng chung giữa các đối tượng) và $Z_{private}$ (đặc tính sinh lý đặc thù của từng cá nhân / miền).
