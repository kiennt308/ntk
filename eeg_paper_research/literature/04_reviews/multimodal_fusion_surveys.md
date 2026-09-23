# Tổng Hợp Khảo Sát: Cơ Chế Dung Hợp Đa Phương Thức (Multimodal Fusion)

## 1. Phân Loại Cơ Chế Dung Hợp Trong Tài Liệu Mới (2023–2026)

### A. Early Fusion (Data / Low-Level Feature Level)
- **Ưu điểm**: Giữ được tương quan thô trực tiếp giữa các kênh tín hiệu đồng thời (ví dụ: ghép ma trận EEG + GSR + ECG sau khi chuẩn hóa tần số lấy mẫu).
- **Hạn chế**: Chênh lệch lớn về chiều không gian và đặc tính vật lý khiến đặc trưng EEG bị áp đảo hoặc gây bùng nổ chiều đặc trưng (curse of dimensionality).

### B. Intermediate / Multibranch Fusion (Feature-Level & Cross-Modal Attention)
- **Kiến trúc tiêu biểu**: Kiến trúc đa nhánh độc lập (Multi-branch Subnetworks) trích xuất biểu diễn đặc trưng riêng cho từng tín hiệu (1D-CNN cho ECG/PPG, GCN/Spatial-CNN cho EEG, BiLSTM/TCN cho EDA/GSR).
- **Cơ chế Chú ý Chéo (Cross-Modal Attention)**: Sử dụng ma trận tương quan chú ý giữa Query ($Q_{EEG}$) và Key/Value ($K_{Bio}, V_{Bio}$) để định hướng mức độ đóng góp của từng phương thức theo thời gian thực.
- **Tài liệu tham khảo**: `OA_KW3_001` đến `OA_KW3_046` trong kho tài liệu.

### C. Late Fusion & Decision Fusion
- **Ưu điểm**: Cho phép mỗi nhánh mô hình tối ưu độc lập phân phối xác suất phân loại (Valence, Arousal, Dominance). Bền vững tốt hơn khi một nhánh cảm biến bị mất tín hiệu đột ngột.
- **Hạn chế**: Bỏ qua các tương tác phi tuyến tính cấp độ cao (high-order non-linear cross-modal correlations) giữa não bộ và hệ thần kinh tự chủ.
