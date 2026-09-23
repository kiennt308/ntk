# Khối 5: Độ Bền Vững Khi Khuyết Thiếu Cảm Biến (Missing Modality Robustness)

## 1. Chưng Cất Tri Thức Đa Phương Thức (Cross-Modal Knowledge Distillation)
- **Giai đoạn Offline**: Huấn luyện Mạng Giáo Viên (Full Modalities: EEG + ECG + EDA).
- **Giai đoạn Online / Deployment**: Mạng Học Sinh chỉ nhận 1 hoặc 2 cảm biến đeo khả dụng, được giám sát bởi hàm mất mát Kullback-Leibler (KL-Divergence) ép khớp biểu diễn với Mạng Giáo Viên.

## 2. Tái Tạo Đặc Trưng Ẩn Bằng Masked Modeling
Áp dụng cơ chế ngẫu nhiên che bớt (masking) một phương thức trong quá trình huấn luyện để mô hình tự học cách bù đắp thông tin qua các phương thức còn lại.
