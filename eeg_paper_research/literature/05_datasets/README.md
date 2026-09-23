# TỔNG HỢP CÁC BỘ DỮ LIỆU BENCHMARK ĐA PHƯƠNG THỨC & GIAO THỨC CHUẨN (BENCHMARK DATASETS & ANTI-LEAKAGE PROTOCOLS)
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH

Thư mục `05_datasets/` cung cấp tài liệu hướng dẫn kỹ thuật chi tiết, kích thước mảng Tensor thô và tiền xử lý, cấu trúc kênh, giao thức chia tập dữ liệu nghiêm ngặt và cẩm nang ngăn chặn rò rỉ dữ liệu (Anti-Leakage Audit) cho tất cả các bộ dữ liệu benchmark quốc tế.

---

## 📊 1. Bảng Thông Số Kỹ Thuật Chi Tiết Các Bộ Dữ Liệu Benchmark

| Tên Dataset | Số Đối Tượng | Kênh Tín Hiệu & Tần Số Lấy Mẫu | Kích Thích (Stimuli) | Nhãn Cảm Xúc & Thang Đo | Shape Dữ Liệu Sau Tiền Xử Lý | Tài Liệu Kỹ Thuật |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| **DEAP** | 32 (16N/16N) | **32 EEG** (128 Hz) + **8 Peripheral** (ECG, GSR, EMG, PPG, Temp, Resp) | 40 Music Videos (60s) | Valence, Arousal, Dominance, Liking (1–9 continuous SAM) | `(40 trials, 40 channels, 8064 samples)` | [`DEAP_dataset_guide.md`](DEAP_dataset_guide.md) |
| **SEED** | 15 (3 sessions) | **62 EEG** chuẩn ESI NeuroScan (downsample 200 Hz) | 15 Film Clips (~4m) | 3 Cảm xúc rời rạc (Positive, Neutral, Negative) | DE/PSD features `(15 trials, 62 channels, 5 bands)` | [`SEED_family_guide.md`](SEED_family_guide.md) |
| **SEED-IV** | 15 (3 sessions) | **62 EEG** + **12 Eye-tracking metrics** (SMI Glasses) | 24 Film Clips (~2m) | 4 Cảm xúc (Happy, Sad, Fear, Neutral) | DE + Eye features per segment | [`SEED_family_guide.md`](SEED_family_guide.md) |
| **SEED-V** | 16 (3 sessions) | **62 EEG** + **Eye-tracking** (Pupil diameter, Fixation) | 45 Film Clips (~2-4m) | 5 Cảm xúc (Happy, Sad, Fear, Disgust, Neutral) | Multimodal EEG-Eye aligned features | [`SEED_family_guide.md`](SEED_family_guide.md) |
| **DREAMER** | 23 | **14 EEG** Emotiv (128 Hz) + **2 ECG** Shimmer (256 Hz) | 18 Audio-Visual Clips | Valence, Arousal, Dominance (1–5 continuous SAM) | Raw & baseline-subtracted epochs | [`DREAMER_dataset_guide.md`](DREAMER_dataset_guide.md) |
| **AMIGOS** | 40 | **14 EEG** + **2 ECG** + **1 GSR** + Video RGB/Depth | 16 Short (60s) + 4 Long Clips (15m) | Valence, Arousal, Dominance + Basic Emotions | Individual & Group Setting arrays | [`AMIGOS_dataset_guide.md`](AMIGOS_dataset_guide.md) |
| **WESAD** | 15 | **RespiBAN (Ngực)**: ECG, EDA, EMG, Resp (700 Hz)<br>**Empatica E4 (Cổ tay)**: BVP (64 Hz), EDA (4 Hz) | Social Stress Test (TSST), Amusement, Meditation | 3-Class (Stress, Amusement, Baseline) & Valence/Arousal | Synchronized Chest + Wrist biosignals | [`AMIGOS_dataset_guide.md`](AMIGOS_dataset_guide.md) |

---

## 🛡️ 2. Quy Chuẩn Kiểm Toán Rò Rỉ Dữ Liệu 6 Chiều (Anti-Leakage Audit Checklist)

Khi tiến hành thử nghiệm mô hình cho luận án Tiến sĩ, bắt buộc phải tuân thủ nghiêm ngặt 6 nguyên tắc chống rò rỉ:

1. **Rò rỉ Cửa sổ Trượt (Windowing Temporal Leakage)**:
   - *Nguy cơ*: Cắt các cửa sổ trượt có độ gối nhau (overlapping sliding windows, ví dụ: cửa sổ 4s, bước nhảy 1s) rồi xáo trộn ngẫu nhiên (random shuffle) trước khi chia Train/Test.
   - *Giải pháp*: Bắt buộc phân chia tập dữ liệu theo **Subject ID** hoặc theo **Trial ID** trước khi áp dụng cửa sổ trượt.
2. **Rò rỉ Thông tin Đối tượng (Subject Identity Leakage)**:
   - *Nguy cơ*: Dữ liệu của cùng một đối tượng xuất hiện ở cả tập Train và Test trong bài toán liên đối tượng (Cross-Subject).
   - *Giải pháp*: Bắt buộc sử dụng **Leave-One-Subject-Out (LOSO)**: huấn luyện trên $N-1$ đối tượng và kiểm thử độc lập hoàn toàn trên đối tượng thứ $N$.
3. **Rò rỉ Chuẩn hóa Đặc trưng (Feature Scaling Leakage)**:
   - *Nguy cơ*: Áp dụng Z-score chuẩn hóa hoặc Min-Max trên toàn bộ dataset trước khi chia tập Train/Test.
   - *Giải pháp*: Chỉ tính toán trung bình $\mu_{train}$ và độ lệch chuẩn $\sigma_{train}$ trên tập huấn luyện, sau đó áp dụng phép biến đổi lên tập kiểm thử.
4. **Rò rỉ Bộ lọc Làm mượt Thời gian (Temporal Smoothing Leakage)**:
   - *Nguy cơ*: Sử dụng Linear Dynamic System (LDS) hoặc bộ lọc Moving Average xuyên suốt toàn bộ phiên đo.
   - *Giải pháp*: Fit bộ lọc độc lập cho từng trial riêng biệt sau khi đã chia tập.
5. **Rò rỉ Tối ưu Siêu tham số (Hyperparameter Tuning Leakage)**:
   - *Nguy cơ*: Tinh chỉnh tham số (Learning rate, Dropout, Hidden dim) dựa trên kết quả của tập Test.
   - *Giải pháp*: Sử dụng cơ chế Nested Cross-Validation (Outer loop cho Test, Inner loop cho Validation).
6. **Rò rỉ Cấu hình Điện cực (Montage Mapping Shift)**:
   - *Nguy cơ*: Trộn lẫn các bộ dữ liệu có vị trí đặt điện cực khác nhau (62 kênh 10-20 vs 14 kênh Emotiv) mà không đồng bộ hóa không gian.
   - *Giải pháp*: Sử dụng phép biến đổi tọa độ không gian 3D (Spherical Spline Interpolation hoặc Geometric GCN Node Projection).
