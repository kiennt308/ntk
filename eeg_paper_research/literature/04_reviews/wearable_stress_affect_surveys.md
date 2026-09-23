# Tổng Hợp Khảo Sát: Cảm Biến Đeo & Tính Bền Vững (Wearables & Missing Modalities)

## 1. Thách Thức Trong Môi Trường Thực Tế (In-the-wild Affective Computing)

- **Suy hao và Khuyết thiếu Cảm biến (Missing Modalities)**: Trong môi trường đeo thực tế, các cảm biến như PPG, EDA hoặc điện cực EEG có thể bị rơi, ngắt kết nối hoặc nhiễu do vận động (motion artifacts).
- **Giải pháp hiện đại**:
  - Học chuyển giao tri thức chéo (Cross-Modal Knowledge Distillation): Sử dụng mô hình giáo viên (Teacher) đầy đủ phương thức để dạy mô hình học sinh (Student) hoạt động khi chỉ có 1 hoặc 2 cảm biến đeo.
  - Tái tạo dữ liệu khuyết bằng Masked Autoencoder / GAN.
- **Tài liệu tham khảo**: Xem cụm [`kw5_missing_modality_wearable_robustness`](../open_access_repository/kw5_missing_modality_wearable_robustness/README.md).
