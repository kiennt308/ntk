# Hướng Dẫn Kỹ Thuật Bộ Dữ Liệu SEED Family (SEED, SEED-IV, SEED-V)

## 1. Hệ Sinh Thái Dữ Liệu SEED (Đại học Giao thông Thượng Hải - SJTU BCMI Lab)

### A. SEED (SJTU Emotion EEG Dataset - 3 Lớp Cảm Xúc)
- **15 đối tượng**, tham gia **3 phiên thử nghiệm (sessions)** cách nhau một khoảng thời gian.
- **62 Kênh EEG** chuẩn ESI NeuroScan, lấy mẫu 1000 Hz, downsample 200 Hz.
- **Nhãn**: 3 lớp cảm xúc (Positive, Neutral, Negative) kích thích qua 15 đoạn phim.
- **Đặc trưng chuẩn**: Cung cấp sẵn Differential Entropy (DE), Power Spectral Density (PSD), Differential Asymmetry (DASM), Rational Asymmetry (RASM) trên 5 dải tần ($\delta, 	heta, lpha, eta, \gamma$).

### B. SEED-IV (4 Lớp Cảm Xúc + Eye Tracking)
- **15 đối tượng**, 3 sessions, 24 video clip mỗi session.
- **Nhãn**: 4 lớp cảm xúc (Happy, Sad, Fear, Neutral).
- **Phương thức bổ sung**: Tín hiệu theo dõi chuyển động mắt đa kênh từ SMI Eye-Tracking Glasses (đường kính đồng tử, tần số chớp mắt, thời gian định thị - fixation duration).

### C. SEED-V (5 Lớp Cảm Xúc + Eye Tracking)
- **16 đối tượng**, 3 sessions, 45 video clip.
- **Nhãn**: 5 lớp cảm xúc (Happy, Sad, Fear, Disgust, Neutral).
