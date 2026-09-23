# HỆ THỐNG KHO TÀI LIỆU KHOA HỌC CHUYÊN SÂU (ADVANCED LITERATURE REPOSITORY)
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH ĐA PHƯƠNG THỨC
*(Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals)*

---

## 🧭 1. Tổng Quan & Kiến Trúc Kho Tri Thức

Kho tài liệu `literature/` là trung tâm lưu trữ, xử lý và phân tích hệ thống tài liệu khoa học toàn văn (Full-text Literature Corpus) phục vụ nghiên cứu sinh. Hệ thống được tổ chức theo tiêu chuẩn quy trình **Systematic Literature Review (PRISMA-2020)** kết hợp với phân loại chuyên sâu cho kỷ nguyên **2023–2026** (Foundation Models, Dynamic GNN, Subspace Disentanglement, và Wearable Edge BCI).

```
eeg_paper_research/literature/
│
├── 🌟 open_access_repository/         [KHO TRỌNG TÂM 2023–2026] 375 bài báo OA & 240 PDF phân theo 10 Cụm Từ Khóa
│   ├── README.md                      -> Bảng chỉ mục liên kết toàn diện 10 cụm chủ đề
│   ├── kw01_multimodal_eeg_biosignals/
│   ├── kw02_multitask_learning_affect/
│   ├── kw03_multibranch_crossmodal_attention/
│   ├── kw04_subspace_disentanglement_domain_adaptation/
│   ├── kw05_missing_modality_wearable_robustness/
│   ├── kw06_foundation_models_self_supervised_biosignals/
│   ├── kw07_graph_neural_networks_eeg_connectivity/
│   ├── kw08_transformers_crossmodal_affective_computing/
│   ├── kw09_explainable_ai_interpretable_biosignals/
│   └── kw10_closed_loop_bci_realtime_affective_systems/
│
├── 📥 00_inbox/                        [Tiếp nhận] Hộp thư nạp tài liệu thô mới & quy trình tiền xử lý
├── 📄 01_verified/                     [Cốt lõi GĐ 1] 30 file PDF bài báo nền tảng kiểm định nghiêm ngặt (P0001–P0030)
├── 🏷️ 02_classified/                   [Phân hệ Chuyên đề] Phân loại 14 nhánh kỹ thuật & đặc tính vật lý tín hiệu
├── 📝 03_notes/                        [Bản phân tích Sâu] 30 bài phân tích chi tiết (Mathematical Deep Dives)
├── 📚 04_reviews/                      [Khảo sát Hệ thống] Tổng quan SLR, xu hướng dung hợp, deep learning & thiết bị đeo
├── 📊 05_datasets/                     [Benchmark Chuẩn] Hướng dẫn giao thức DEAP, SEED, DREAMER, AMIGOS, WESAD, K-EmoCon
├── 🌲 06_taxonomy/                     [Cây Phân loại Kỹ thuật] Kiến trúc đa nhánh, chú ý chéo, MTL, tách không gian & XAI
├── 🔍 07_duplicates/                   [Kiểm toán Trùng lặp] Quy trình khử trùng lặp PRISMA & định danh số DOI/arXiv
├── 🔒 08_unavailable/                  [Quản lý Bài Trả phí] Theo dõi các bài Paywalled, phương án Preprint & ILL
└── 📑 index/                           [Chỉ mục Cơ sở Dữ liệu] Master CSV Metadata, Taxonomy Framework & Dataset Mapping
```

---

## 📊 2. Bản Đồ Điều Hướng Nhanh & Thống Kê Dữ Liệu

| Thư mục | Chức năng chính | Quy mô dữ liệu | Trọng tâm công nghệ / Xu hướng 2023–2026 |
| :--- | :--- | :---: | :--- |
| [`open_access_repository/`](open_access_repository/README.md) | Kho 10 Cụm Từ Khóa Toàn diện | **375 bài (240 PDF)** | Foundation Models, SSL, Dynamic Graph, Transformer QKV |
| [`01_verified/`](01_verified/) & [`03_notes/`](03_notes/) | 30 Bài báo Cốt lõi & Phân tích Sâu | **30 PDF + 30 Notes** | Toàn văn trích xuất công thức toán, hàm mất mát & tham số |
| [`02_classified/`](02_classified/README.md) | Phân loại 14 Phân hệ Tín hiệu & Mô hình | **15 Danh mục** | Tách riêng EEG, ECG, EDA, PPG, MTL, Fusion, Generalization |
| [`04_reviews/`](04_reviews/README.md) | Tổng hợp Systematic Reviews & Surveys | **4 Báo cáo tổng hợp** | Tổng quan công nghệ 2023-2026 từ IEEE, Info Fusion, AI Review |
| [`05_datasets/`](05_datasets/README.md) | Cẩm nang Kỹ thuật Benchmark Datasets | **5 Tài liệu kỹ thuật** | Giao thức LOSO, chống rò rỉ cửa sổ trượt (Anti-Leakage) |
| [`06_taxonomy/`](06_taxonomy/README.md) | Cây Phân loại Kiến trúc Đa nhánh Đa nhiệm | **6 Chuyên đề kiến trúc**| Công thức toán học Cross-Attention, Disentanglement, MTL Loss |
| [`07_duplicates/`](07_duplicates/README.md) | Báo cáo Khử Trùng lặp Học thuật | **1 Báo cáo PRISMA** | Chuẩn hóa định danh DOI, OpenAlex ID và arXiv Preprints |
| [`08_unavailable/`](08_unavailable/README.md) | Theo dõi Bài báo Paywalled & Open Access | **1 Báo cáo quản trị** | Hướng dẫn khai thác bản mở hợp pháp (Green OA, Author Copy) |
| [`index/`](index/) | Master CSV Database & Metadata Indices | **3 File CSDL Chỉ mục** | CSV Paper Database, Dataset Matrix & Taxonomy Mapping |

---

## 🎯 3. Quy Chuẩn Đọc & Trích Dẫn Dành Cho Nghiên Cứu Sinh

1. **Khi viết Chương 2 (Tổng quan & Lý thuyết nền tảng)**:
   - Tham khảo [`04_reviews/`](04_reviews/README.md) và [`06_taxonomy/`](06_taxonomy/README.md) để xây dựng cây phả hệ công nghệ.
   - Trích dẫn các bài báo mới nhất trong [`open_access_repository/kw06_foundation_models_self_supervised_biosignals/`](open_access_repository/kw06_foundation_models_self_supervised_biosignals/README.md) và [`open_access_repository/kw07_graph_neural_networks_eeg_connectivity/`](open_access_repository/kw07_graph_neural_networks_eeg_connectivity/README.md).

2. **Khi viết Chương 3 (Thiết kế Kiến trúc MMB-EmotionNet)**:
   - Tham khảo công thức toán trong [`06_taxonomy/02_crossmodal_fusion_mechanisms.md`](06_taxonomy/02_crossmodal_fusion_mechanisms.md), [`06_taxonomy/03_multitask_learning_paradigms.md`](06_taxonomy/03_multitask_learning_paradigms.md), và [`06_taxonomy/04_disentanglement_domain_adaptation.md`](06_taxonomy/04_disentanglement_domain_adaptation.md).

3. **Khi thiết kế Thực nghiệm Chương 4 & Chương 5 (Datasets & Experiments)**:
   - Áp dụng các quy tắc chia tập và chống rò rỉ dữ liệu trong [`05_datasets/README.md`](05_datasets/README.md) và các hướng dẫn chi tiết từng bộ dữ liệu.
