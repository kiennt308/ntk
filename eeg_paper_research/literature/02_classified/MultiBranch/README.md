# Phân Hệ Tài Liệu: Kiến Trúc Mạng Nơ-ron Đa Nhánh (Multi-Branch Networks)

## 1. Lý Do Khoa Học Cần Kiến Trúc Đa Nhánh
- **Tính không đồng nhất vật lý (Heterogeneous Signal Nature)**: EEG có đặc tính không gian đa kênh (Spatial Topology), trong khi ECG mang tính tuần hoàn chu kỳ nhịp tim (R-peak morphology), và EDA là tín hiệu biến thiên chậm (Tonic/Phasic response).
- **Hạn chế của Early Fusion**: Nếu ghép vector thô ngay từ đầu, sự chênh lệch lớn về biên độ, tần số lấy mẫu (128–512 Hz vs 4–64 Hz) và chiều không gian sẽ khiến tín hiệu EEG lấn át các tín hiệu khác, làm triệt tiêu thông tin ngoại vi.

## 2. Thiết Kế Bộ Mã Hóa Đa Nhánh Đề Xuất (Physics-Informed Encoders)
1. **Nhánh EEG**: Spatial-Temporal 2D-CNN hoặc Spatial GCN trích xuất đặc trưng liên kết bán cầu não.
2. **Nhánh ECG / PPG**: Multi-scale Dilated 1D-CNN nắm bắt biến thiên nhịp tim ngắn hạn và dài hạn (HRV).
3. **Nhánh EDA / Respiration**: Continuous Wavelet Transform (CWT) + 1D-CNN trích xuất biên độ phản ứng da tức thời.

## 3. Tài Liệu Nghiên Cứu Điển Hình
- [`kw03_multibranch_crossmodal_attention`](../open_access_repository/kw03_multibranch_crossmodal_attention/README.md): 46 bài báo chuyên sâu.
- Các bài báo nền tảng: `P0004`, `P0006`, `P0014`, `P0018` trong thư mục [`03_notes/`](../03_notes/).
