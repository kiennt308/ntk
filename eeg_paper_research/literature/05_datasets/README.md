# TỔNG HỢP CÁC BỘ DỮ LIỆU BENCHMARK ĐA PHƯƠNG THỨC (BENCHMARK DATASETS)
## ĐỀ TÀI TIẾN SĨ: NHẬN DIỆN CẢM XÚC ĐA PHƯƠNG THỨC TỪ TÍN HIỆU Y SINH

Thư mục `05_datasets/` cung cấp tài liệu hướng dẫn kỹ thuật chi tiết, cấu trúc dữ liệu, giao thức tiền xử lý và liên kết tải/đăng ký quyền truy cập cho tất cả các bộ dữ liệu chuẩn quốc tế phục vụ thử nghiệm mô hình.

---

## 1. Bảng Tổng Hợp Các Bộ Dữ Liệu Benchmark Quốc Tế

| Tên Dataset | Số Đối Tượng | Tín hiệu / Phương thức thu thập | Kích thích (Stimuli) | Nhãn Cảm Xúc & Thang Đo | Tài liệu chi tiết |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **DEAP** | 32 | EEG (32 kênh), ECG, GSR, EMG, PPG, Nhiệt độ | 40 Video Âm nhạc (60s) | Valence, Arousal, Dominance (1–9) | [`DEAP_dataset_guide.md`](DEAP_dataset_guide.md) |
| **SEED Family** | 15–16 | EEG (62 kênh ESI NeuroScan), Theo dõi Mắt (Eye-tracking) | Phim điện ảnh cảm xúc (2–4 phút) | 3 đến 5 cảm xúc rời rạc (Vui, Buồn, Sợ, Ghê tởm, Bình thường) | [`SEED_family_guide.md`](SEED_family_guide.md) |
| **DREAMER** | 23 | EEG (14 kênh Emotiv), ECG (2 kênh Shimmer) | 18 Đoạn phim âm thanh-hình ảnh | Valence, Arousal, Dominance (1–5) | [`DREAMER_dataset_guide.md`](DREAMER_dataset_guide.md) |
| **AMIGOS** | 40 | EEG (14 kênh), ECG (2 kênh), GSR, Video khuôn mặt | Video ngắn (16 clip) & Video dài (4 clip) | Valence, Arousal, Dominance, 7 Cảm xúc cơ bản | [`AMIGOS_dataset_guide.md`](AMIGOS_dataset_guide.md) |
| **MAHNOB-HCI**| 27 | EEG (32 kênh Biosemi), ECG, GSR, RSP, Temp, Eye-gaze | 20 Đoạn phim cảm xúc | Valence, Arousal, Dominance, Nhãn rời rạc | [`MAHNOB_HCI_guide.md`](MAHNOB_HCI_guide.md) |
| **WESAD** | 15 | RespiBAN (Ngực: ECG, EDA, EMG, Resp, Temp) + Empatica E4 (Cổ tay: BVP, EDA, Temp) | Kịch bản gây stress, thư giãn, giải trí | Stress (3 lớp) & Affect (Valence, Arousal) | [`WESAD_dataset_guide.md`](WESAD_dataset_guide.md) |
| **K-EmoCon** | 32 (16 cặp)| EEG (Emotiv), BVP, EDA, SKT, Audio, Video (Đàm thoại tự nhiên) | Hội thoại tranh luận tự nhiên theo cặp | Continuous Valence & Arousal (Self & Observer) | [`K_EmoCon_guide.md`](K_EmoCon_guide.md) |

---

## 2. Quy Chuẩn Tiền Xử Lý & Đánh Giá Không Rò Rỉ (Leakage-Free Protocols)

- **Chia tập dữ liệu (Cross-Subject Validation)**: Bắt buộc áp dụng Leave-One-Subject-Out (LOSO) hoặc K-Fold theo Subject ID để kiểm tra tính tổng quát hóa trên người dùng mới.
- **Tránh rò rỉ cửa sổ trượt (Windowing Leakage)**: Tuyệt đối không xáo trộn (shuffle) các sliding windows trước khi chia tập Train/Test.
- **Chuẩn hóa tín hiệu (Feature Scaling)**: Áp dụng Z-score / Min-Max fit trên tập Train và transform sang tập Test độc lập.
