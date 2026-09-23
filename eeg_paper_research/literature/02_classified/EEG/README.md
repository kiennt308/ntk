# Phân Hệ Tài Liệu: EEG & Liên Kết Chức Năng Não Bộ (Brain Connectivity)

## 1. Đặc Tính Vật Lý & Sinh Lý Thần Kinh
- **Độ phân giải**: Độ phân giải thời gian cực cao (mili-giây), ghi nhận trực tiếp hoạt động điện thế sau synap của hàng triệu nơ-ron vỏ não.
- **Dải tần số chức năng (Frequency Bands)**:
  - $\delta$ (0.5 – 4 Hz): Giấc ngủ sâu, trạng thái vô thức.
  - $\theta$ (4 – 8 Hz): Trạng thái thiền, buồn ngủ, xử lý cảm xúc cảm thụ.
  - $\alpha$ (8 – 13 Hz): Thư giãn tỉnh táo; Sự bất đối xứng alpha trán (**Frontal Alpha Asymmetry - FAA**) là chỉ dấu kinh điển cho Valence (tiếp cận vs tránh né).
  - $\beta$ (13 – 30 Hz): Căng thẳng, tập trung cao độ, kích thích cảm xúc (Arousal).
  - $\gamma$ (> 30 Hz): Tích hợp nhận thức cao cấp, gắn kết cảm xúc đa giác quan.

## 2. Các Kiến Trúc Deep Learning Đột Phá (2023–2026)
1. **Dynamic Graph Convolutional Networks (DGCNN / RGNN)**: Học ma trận kề động dựa trên Phase Locking Value (PLV) hoặc Pearson Correlation giữa 62 điện cực.
2. **EEG-Conformer / Transformer Encoders**: Kết hợp Spatial Depthwise Convolution với Multi-Head Self-Attention để mô hình hóa chuỗi thời gian dài.
3. **Mô hình tham khảo**:
   - `OA_KW7_001` đến `OA_KW7_050` trong [Cụm Graph Neural Networks](../open_access_repository/kw07_graph_neural_networks_eeg_connectivity/README.md).
   - `P0002`, `P0003`, `P0008` trong [30 Bài Báo Cốt Lõi](../03_notes/).
