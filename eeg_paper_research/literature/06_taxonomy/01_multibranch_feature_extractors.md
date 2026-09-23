# Khối 1: Mạng Trích Xuất Đặc Trưng Đa Nhánh Độc Lập

## 1. Nhánh Tín Hiệu Não Bộ (EEG Branch)
- **Đặc thù**: Độ phân giải không gian đa kênh (14–62 kênh) và tần số cao ($\delta, 	heta, lpha, eta, \gamma$).
- **Kiến trúc tối ưu**: 
  - **Spatial Filtering + Temporal Convolutions**: Khối Spatial Depthwise Conv (như EEGNet) học cách kết hợp các kênh đối xứng bán cầu não (F3-F4, T7-T8).
  - **Graph Attention Networks (GAT)**: Xây dựng ma trận kề động dựa trên Phase Locking Value (PLV) hoặc Pearson Correlation giữa các điện cực.

## 2. Nhánh Tín Hiệu Tim Mạch (ECG / PPG Branch)
- **Đặc thù**: Tính chu kỳ mạnh, R-peaks, biến thiên nhịp tim (HRV).
- **Kiến trúc tối ưu**: Temporal Convolutional Networks (TCN) với dilated convolutions để nắm bắt biến thiên HRV ngắn hạn và dài hạn.

## 3. Nhánh Phản Xạ Da & Hô Hấp (EDA/GSR & Respiration)
- **Đặc thù**: Phản ứng chậm (tonic component) và các gai kích thích cảm xúc tức thì (phasic component).
- **Kiến trúc tối ưu**: Continuous Wavelet Transform (CWT) + 1D-CNN trích xuất đặc trưng biên độ và thời gian phục hồi đỉnh.
