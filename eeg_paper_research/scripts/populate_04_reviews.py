import os

base_dir = r"d:\ntk\eeg_paper_research\literature"

# -------------------------------------------------------------
# 1. 04_reviews
# -------------------------------------------------------------
reviews_dir = os.path.join(base_dir, "04_reviews")
os.makedirs(reviews_dir, exist_ok=True)

reviews_readme = """# TỔNG HỢP CÁC BÀI BÁO TỔNG QUAN & KHẢO SÁT CHUYÊN SÂU (SYSTEMATIC REVIEWS & SURVEYS)
## ĐỀ TÀI TIẾN SĨ: NHẬN DIỆN CẢM XÚC ĐA PHƯƠNG THỨC TỪ TÍN HIỆU Y SINH

Thư mục `04_reviews/` tập hợp và phân tích có hệ thống các bài báo tổng quan (Surveys / Systematic Literature Reviews - SLR) hàng đầu thế giới từ các tạp chí uy tín (Information Fusion, IEEE TAFFC, AI Review, Proceedings of the IEEE, Sensors, Frontiers) về tính toán cảm xúc, EEG và tín hiệu sinh lý.

---

## 1. Danh Mục Các Khảo Sát Nền Tảng (Core Benchmark Reviews)

| Mã ID | Tác giả & Năm | Tiêu đề bài báo | Nguồn / Tạp chí | Trích dẫn | Liên kết file |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **REV_01** | *Khare et al. (2023)* | **Emotion recognition and artificial intelligence: A systematic review (2014–2023) and research recommendations** | *Information Fusion* | 462 | [`OA_KW2_001.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_001.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_001.pdf) |
| **REV_02** | *Samal & Hashmi (2024)* | **Role of machine learning and deep learning techniques in EEG-based BCI emotion recognition system: a review** | *Artificial Intelligence Review* | 147 | [`OA_KW2_003.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_003.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_003.pdf) |
| **REV_03** | *Abibullaev et al. (2023)* | **Deep Learning in EEG-Based BCIs: A Comprehensive Review of Transformer Models, Advantages, Challenges, and Applications** | *IEEE Access* | 136 | [`OA_KW2_004.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_004.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_004.pdf) |
| **REV_04** | *Cai et al. (2023)* | **Emotion Recognition Using Different Sensors, Emotion Models, Methods and Datasets: A Comprehensive Review** | *Sensors* | 133 | [`OA_KW2_006.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_006.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_006.pdf) |
| **REV_05** | *Pei et al. (2023)* | **Affective Computing: Recent Advances, Challenges, and Future Trends** | *Intelligent Computing* | 132 | [`OA_KW2_007.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_007.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_007.pdf) |
| **REV_06** | *Pillalamarri & Udhayakumar (2025)* | **A review on EEG-based multimodal learning for emotion recognition** | *Artificial Intelligence Review* | 117 | [`OA_KW2_011.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_011.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_011.pdf) |
| **REV_07** | *Can et al. (2023)* | **Approaches, Applications, and Challenges in Physiological Emotion Recognition—A Tutorial Overview** | *Proceedings of the IEEE* | 73 | [`OA_KW2_031.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_031.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_031.pdf) |
| **REV_08** | *Ma et al. (2024)* | **A comprehensive review of deep learning in EEG-based emotion recognition: classifications, trends, and practical implications** | *PeerJ Computer Science* | 87 | [`OA_KW2_023.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_023.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_023.pdf) |
| **REV_09** | *Udahemuka et al. (2024)* | **Multimodal Emotion Recognition Using Visual, Vocal and Physiological Signals: A Review** | *Applied Sciences* | 74 | [`OA_KW2_030.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_030.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_030.pdf) |
| **REV_10** | *Vos et al. (2023)* | **Generalizable machine learning for stress monitoring from wearable devices: A systematic literature review** | *Int. J. Medical Informatics* | 160 | [`OA_KW2_026.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_026.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_026.pdf) |

---

## 2. Báo Cáo Tổng Hợp Chuyên Đề (Thematic Synthesis)

1. [`multimodal_fusion_surveys.md`](multimodal_fusion_surveys.md): Khảo sát các cơ chế dung hợp đa phương thức (Early, Late, Cross-Attention, Multi-Branch).
2. [`eeg_deep_learning_surveys.md`](eeg_deep_learning_surveys.md): Tổng quan các kiến trúc Deep Learning cho EEG (CNN, Transformer, GNN, Disentanglement).
3. [`wearable_stress_affect_surveys.md`](wearable_stress_affect_surveys.md): Khảo sát ứng dụng cảm biến đeo, thiết bị y tế IoT và tính toán biên trong nhận diện cảm xúc.
"""

with open(os.path.join(reviews_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(reviews_readme)

fusion_synthesis = """# Tổng Hợp Khảo Sát: Cơ Chế Dung Hợp Đa Phương Thức (Multimodal Fusion)

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
"""

with open(os.path.join(reviews_dir, "multimodal_fusion_surveys.md"), "w", encoding="utf-8") as f:
    f.write(fusion_synthesis)

eeg_synthesis = """# Tổng Hợp Khảo Sát: Các Kiến Trúc Deep Learning Cho Tín Hiệu Não (EEG)

## 1. Xu Hướng Chuyển Dịch Kiến Trúc (2023–2026)

1. **Từ CNN truyền thống sang Spatial-Temporal GNN & Transformer**:
   - Các mô hình như **LGGNet** (Ding et al., IEEE TNNLS 2023) và **EEGformer** (Wan et al., 2023) khai thác cấu trúc đồ thị động (Dynamic Brain Connectivity) giữa các điện cực não bộ trên mạng 10-20.
2. **Học Đa Nhiệm Vụ (Multi-Task Learning - MTL)**:
   - Thay vì huấn luyện các mô hình phân loại nhị phân riêng rẽ cho Valence và Arousal, mạng đa nhiệm sử dụng Shared Encoder + Task-Specific Heads giúp chia sẻ biểu diễn ngữ nghĩa và giảm hiện tượng Overfitting.
3. **Tách Biểu Diễn (Subspace Disentanglement)**:
   - Tách không gian biểu diễn thành 2 phần: $Z_{shared}$ (biểu diễn cảm xúc dùng chung giữa các đối tượng) và $Z_{private}$ (đặc tính sinh lý đặc thù của từng cá nhân / miền).
"""

with open(os.path.join(reviews_dir, "eeg_deep_learning_surveys.md"), "w", encoding="utf-8") as f:
    f.write(eeg_synthesis)

wearable_synthesis = """# Tổng Hợp Khảo Sát: Cảm Biến Đeo & Tính Bền Vững (Wearables & Missing Modalities)

## 1. Thách Thức Trong Môi Trường Thực Tế (In-the-wild Affective Computing)

- **Suy hao và Khuyết thiếu Cảm biến (Missing Modalities)**: Trong môi trường đeo thực tế, các cảm biến như PPG, EDA hoặc điện cực EEG có thể bị rơi, ngắt kết nối hoặc nhiễu do vận động (motion artifacts).
- **Giải pháp hiện đại**:
  - Học chuyển giao tri thức chéo (Cross-Modal Knowledge Distillation): Sử dụng mô hình giáo viên (Teacher) đầy đủ phương thức để dạy mô hình học sinh (Student) hoạt động khi chỉ có 1 hoặc 2 cảm biến đeo.
  - Tái tạo dữ liệu khuyết bằng Masked Autoencoder / GAN.
- **Tài liệu tham khảo**: Xem cụm [`kw05_missing_modality_wearable_robustness`](../open_access_repository/kw05_missing_modality_wearable_robustness/README.md).
"""

with open(os.path.join(reviews_dir, "wearable_stress_affect_surveys.md"), "w", encoding="utf-8") as f:
    f.write(wearable_synthesis)

print("04_reviews populated successfully.")
