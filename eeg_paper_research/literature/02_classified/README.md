# HỆ THỐNG PHÂN LOẠI TÀI LIỆU THEO PHÂN HỆ KỸ THUẬT & TÍN HIỆU (`02_classified/`)
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH

Thư mục `02_classified/` tổ chức toàn bộ cơ sở dữ liệu bài báo khoa học thành 14 phân hệ chuyên đề, bao gồm cả đặc tính vật lý tín hiệu y sinh và các đột phá kiến trúc học sâu giai đoạn **2023–2026**.

---

## 🧭 Danh Mục 14 Phân Hệ Chuyên Đề

### Nhóm 1: Tín Hiệu Y Sinh & Sinh Lý Thần Kinh (Modality Foundations)
1. **[`EEG/`](EEG/README.md)**: Xử lý tín hiệu Điện não đồ (EEG), dải tần ($\delta, \theta, \alpha, \beta, \gamma$), liên kết chức năng vỏ não và mạng nơ-ron đồ thị (GNNs).
2. **[`ECG/`](ECG/README.md)**: Điện tim (ECG), biến thiên nhịp tim (HRV) miền thời gian/tần số và điều hòa thần kinh tự chủ (ANS).
3. **[`EDA_GSR/`](EDA_GSR/README.md)**: Hoạt tính điện da (EDA / GSR), phân rã thành phần Tonic (SCL) và Phasic (SCR) phản ánh mức độ kích động cảm xúc (Arousal).
4. **[`PPG/`](PPG/README.md)**: Quang thể tích đồ (PPG) từ thiết bị đeo thông minh (Smartwatch, Wristband) và ước lượng nhịp tim gián tiếp.
5. **[`EMG/`](EMG/README.md)**: Điện cơ (EMG) cơ mặt (Zygomaticus major, Corrugator supercilii) và cơ thang nhận diện biểu cảm vi mô.
6. **[`Respiration/`](Respiration/README.md)**: Tín hiệu nhịp thở (Respiration Rate / Amplitude) phản ánh trạng thái thư giãn và căng thẳng cấp tính.

### Nhóm 2: Kiến Trúc Học Sâu & Dung Hợp Đa Phương Thức (Architectural Innovations)
7. **[`Multimodal/`](Multimodal/README.md)**: Tích hợp đồng thời đa tín hiệu thần kinh trung ương và ngoại vi.
8. **[`MultiBranch/`](MultiBranch/README.md)**: Kiến trúc mạng nơ-ron đa nhánh (Multi-Branch) trích xuất đặc trưng độc lập theo đặc thù vật lý của từng tín hiệu.
9. **[`MultiTask/`](MultiTask/README.md)**: Học đa nhiệm vụ (MTL) tối ưu hóa liên hợp Valence, Arousal, Dominance và cân bằng gradient động (GradNorm, Uncertainty Weighting).
10. **[`Fusion/`](Fusion/README.md)**: Cơ chế dung hợp: Early, Late, Hybrid, Cross-Modal Attention ($Q_{EEG}, K_{Bio}, V_{Bio}$), Bilinear Pooling.
11. **[`Generalization/`](Generalization/README.md)**: Khả năng tổng quát hóa liên đối tượng (Cross-Subject / LOSO), Thích ứng miền (Domain Adaptation), và Tách không gian con (Disentanglement).

### Nhóm 3: Xu Hướng Mới & Tối Ưu Hóa Biên (Emerging Trends 2023–2026)
12. **[`SelfSupervised/`](SelfSupervised/README.md)**: Học tự giám sát (SSL), Mô hình nền tảng y sinh (Foundation Models) và Masked Autoencoding.
13. **[`EfficientModels/`](EfficientModels/README.md)**: Nén mô hình, Lượng tử hóa, Tính toán biên thời gian thực (Edge BCI / IoT Wearables).
14. **[`Reviews/`](Reviews/README.md)**: Các bài báo tổng quan, khảo sát hệ thống (Systematic Literature Reviews & Surveys).

---

## 🔗 Liên Kết Tra Cứu Toàn Văn
- Toàn bộ danh mục bài báo chi tiết, tóm tắt và file PDF có thể tra cứu theo [Kho 10 Cụm Tài Liệu Mở](../open_access_repository/README.md) và [30 Bài Báo Cốt Lõi](../03_notes/).
