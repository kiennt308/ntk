# Hướng Dẫn Kỹ Thuật Bộ Dữ Liệu DEAP (Database for Emotion Analysis using Physiological Signals)

## 1. Thông Tin Tổng Quan
- **Đơn vị phát triển**: Đại học Queen Mary London, Đại học Geneva, EPFL, Đại học Twente (Koelstra et al., IEEE TAFFC 2012).
- **Số lượng đối tượng**: 32 người tham gia (16 nam, 16 nữ).
- **Kích thích cảm xúc**: 40 video âm nhạc có độ dài 1 phút (60 giây), được chọn lọc kỹ lưỡng từ 120 video ứng viên.

## 2. Cấu Trúc Kênh Tín Hiệu (40 Kênh)
- **32 Kênh EEG**: Đặt theo chuẩn 10-20 quốc tế (Fp1, AF3, F3, F7, FC5, FC1, C3, T7, CP5, CP1, P3, P7, Pz, O1, Oz, O2, P4, P8, CP6, CP2, C4, T8, FC6, FC2, F4, F8, AF4, Fp2, Fz, Cz, Pz, Iz).
- **8 Kênh Sinh lý Ngoại vi (Peripheral Biosignals)**:
  - 2 kênh EOG (Horizontal & Vertical electrooculogram)
  - 2 kênh EMG (Zygomaticus major & Trapezius)
  - 1 kênh GSR / EDA (Galvanic Skin Response)
  - 1 kênh Hô hấp (Respiration belt)
  - 1 kênh Plethysmograph (PPG / Blood Volume Pulse)
  - 1 kênh Nhiệt độ da (Body Skin Temperature)

## 3. Định Dạng Dữ Liệu Cung Cấp
- **File tiền xử lý sẵn (`data_preprocessed_python.zip`)**:
  - Tần số lấy mẫu hạ xuống **128 Hz**.
  - Lọc dải tần EOG/EEG từ 4.0 – 45.0 Hz.
  - Dạng mảng NumPy: `data` shape `(40 trials, 40 channels, 8064 samples)` (3 giây baseline + 60 giây trial = 63s x 128Hz = 8064 samples).
  - Mảng nhãn: `labels` shape `(40 trials, 4)` ứng với [Valence, Arousal, Dominance, Liking] trên thang điểm 1–9.
