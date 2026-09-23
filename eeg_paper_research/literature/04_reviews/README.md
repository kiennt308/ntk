# TỔNG HỢP CÁC BÀI BÁO TỔNG QUAN & KHẢO SÁT HỆ THỐNG (SYSTEMATIC REVIEWS & SOTA BENCHMARKS)
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH

Thư mục `04_reviews/` tập hợp, phân loại và phân tích có hệ thống các bài báo tổng quan (Surveys / Systematic Literature Reviews - SLR) xuất bản trên các tạp chí quốc tế hàng đầu (Information Fusion, IEEE TAFFC, AI Review, Proceedings of the IEEE, Sensors, Frontiers) về tính toán cảm xúc, EEG và tín hiệu sinh lý.

---

## 📊 1. Ma Trận So Sánh Các Bài Báo Tổng Quan Nền Tảng (2023–2026)

| Mã ID | Tác giả & Năm | Tạp chí | Trích dẫn | Trọng tâm Phân tích & Đóng góp | Liên kết Tài liệu |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **REV_01** | *Khare et al. (2023)* | *Information Fusion* | 462 | Khảo sát toàn diện AI trong nhận diện cảm xúc (2014–2023), phân tích 180+ bài báo, chỉ ra xu hướng dung hợp đa phương thức và đề xuất khuyến nghị chuẩn hóa dữ liệu. | [`OA_KW2_001.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_001.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_001.pdf) |
| **REV_02** | *Samal & Hashmi (2024)* | *Artificial Intelligence Review* | 147 | Đánh giá vai trò của ML/DL trong hệ thống BCI nhận diện cảm xúc, phân tích các họ kiến trúc CNN, LSTM, GCN và độ chính xác trên SEED/DEAP. | [`OA_KW2_003.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_003.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_003.pdf) |
| **REV_03** | *Abibullaev et al. (2023)* | *IEEE Access* | 136 | Khảo sát chi tiết ứng dụng Transformer trong EEG BCI, phân tích cơ chế Self-Attention và Cross-Attention trong trích xuất biểu diễn chuỗi thời gian. | [`OA_KW2_004.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_004.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_004.pdf) |
| **REV_04** | *Cai et al. (2023)* | *Sensors* | 133 | Tổng quan cảm biến đa dạng (EEG, ECG, GSR, Video), mô hình cảm xúc (Circumplex vs Discrete), phương pháp xử lý và 25 bộ dữ liệu benchmark quốc tế. | [`OA_KW2_006.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_006.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_006.pdf) |
| **REV_05** | *Pei et al. (2023)* | *Intelligent Computing* | 132 | Xu hướng mới trong Affective Computing: Tính toán biên, mô hình nền tảng y sinh, khả năng diễn giải mô hình (XAI) và các rào cản đạo đức AI. | [`OA_KW2_007.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_007.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_007.pdf) |
| **REV_06** | *Pillalamarri et al. (2025)* | *Artificial Intelligence Review* | 117 | Khảo sát học đa phương thức dựa trên EEG, phân loại các chiến lược dung hợp (Early, Late, Multi-Branch, Attention) và thách thức rò rỉ dữ liệu. | [`OA_KW2_011.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_011.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_011.pdf) |
| **REV_07** | *Can et al. (2023)* | *Proc. IEEE* | 73 | Cẩm nang hướng dẫn toàn diện (Tutorial Overview) về nhận diện cảm xúc từ tín hiệu sinh lý ngoại vi (EDA, HRV, PPG) và các bài toán thực tiễn. | [`OA_KW2_031.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_031.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_031.pdf) |
| **REV_08** | *Vos et al. (2023)* | *Int. J. Med. Informatics* | 160 | Tổng quan có hệ thống về khả năng tổng quát hóa (Generalizability) của các mô hình học máy theo dõi stress trên thiết bị đeo thương mại. | [`OA_KW2_026.md`](../open_access_repository/kw02_multitask_learning_affect/paper_notes/OA_KW2_026.md) / [PDF](../open_access_repository/kw02_multitask_learning_affect/pdfs/OA_KW2_026.pdf) |

---

## 📚 2. Báo Cáo Tổng Hợp Chuyên Đề Phục Vụ Viết Luận Án (Synthesis Reports)

1. [`multimodal_fusion_surveys.md`](multimodal_fusion_surveys.md): Khảo sát và so sánh định lượng các cơ chế dung hợp (Early, Late, Multi-Branch, Cross-Modal QKV Attention).
2. [`eeg_deep_learning_surveys.md`](eeg_deep_learning_surveys.md): Lộ trình tiến hóa kiến trúc Deep Learning cho EEG (từ CNN 1D/2D $\rightarrow$ Dynamic GNN $\rightarrow$ Transformer $\rightarrow$ Disentanglement).
3. [`wearable_stress_affect_surveys.md`](wearable_stress_affect_surveys.md): Đánh giá tính ứng dụng trên thiết bị đeo IoT, độ trễ biên (Edge Latency) và độ bền vững khi khuyết thiếu cảm biến (Missing Modalities).
