# HỆ THỐNG TỔNG KHO TÀI LIỆU NGHIÊN CỨU (LITERATURE REPOSITORY)
## ĐỀ TÀI TIẾN SĨ: NHẬN DIỆN CẢM XÚC ĐA PHƯƠNG THỨC TỪ TÍN HIỆU Y SINH (EEG & BIOSIGNALS)

Thư mục `literature/` là trung tâm lưu trữ toàn bộ các nguồn tài liệu khoa học, bài báo, tóm tắt trích dẫn và các chỉ mục nghiên cứu phục vụ đề tài.

---

## 1. Cấu Trúc Chi Tiết Thư Mục `literature/`

```
eeg_paper_research/literature/
│
├── open_access_repository/          ⭐ [KHO TRỌNG TÂM] 375 bài báo OA & 240 file PDF phân theo 10 Cụm Từ Khóa
│   ├── README.md                    -> Bảng chỉ mục liên kết toàn bộ 10 cụm chủ đề
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
├── 01_verified/                     📄 30 bài báo PDF trọng tâm giai đoạn 1 (Core Papers)
├── 03_notes/                        📝 30 bản phân tích chuyên sâu chi tiết (Detailed Paper Notes)
├── index/                           📊 Hệ thống chỉ mục dữ liệu, bài báo và bảng phân loại (Taxonomy)
│   ├── paper-index.csv              -> Cơ sở dữ liệu metadata các bài báo cốt lõi
│   ├── dataset-index.md             -> Tổng hợp danh mục các bộ dữ liệu (DEAP, SEED, DREAMER, MAHNOB,...)
│   └── taxonomy.md                  -> Hệ thống phân loại kiến trúc đa nhiệm, đa phương thức
│
└── [Thư mục quy trình SLR]:
    ├── 00_inbox/                    -> Hộp thư tiếp nhận tài liệu thô mới thu thập
    ├── 02_classified/               -> Phân loại bài báo theo phân hệ
    ├── 04_reviews/                  -> Tổng hợp các bài Systematic Review / Survey
    ├── 05_datasets/                 -> Dữ liệu trích xuất từ các dataset
    ├── 06_taxonomy/                 -> Cây phả hệ nghiên cứu
    ├── 07_duplicates/               -> Lọc bài trùng lặp
    └── 08_unavailable/              -> Danh sách bài chưa có bản full text
```

---

## 2. Các Kho Tài Liệu Chính Bạn Có Thể Truy Cập Ngay

### 🌟 A. Kho Tài Liệu Mở 10 Cụm Chuyên Sâu (`open_access_repository/`)
* **Tổng số bài**: 375 bài báo Open Access giai đoạn 2023–2026.
* **Số lượng PDF offline**: 240 file toàn văn lưu trong các thư mục con `pdfs/`.
* **Ghi chú tóm tắt**: 375 file tóm tắt chi tiết trong các thư mục `paper_notes/`.
* 🔗 Xem chi tiết tại: [`open_access_repository/README.md`](open_access_repository/README.md)

### 📄 B. Bộ 30 Bài Báo Nền Tảng Giai Đoạn 1 (`01_verified/` & `03_notes/`)
* Chứa 30 file PDF toàn văn và 30 bài phân tích chi tiết về kiến trúc học đa nhiệm, đa phương thức cho EEG & tín hiệu sinh lý.
* 🔗 Xem danh mục tại: [`index/paper-index.csv`](index/paper-index.csv) và [`03_notes/`](03_notes/)

### 📊 C. Danh Mục Dữ Liệu & Phân Loại (`index/`)
* [`index/dataset-index.md`](index/dataset-index.md): Bảng phân tích chi tiết các Dataset EEG chuẩn quốc tế (SEED, SEED-IV, SEED-V, DEAP, DREAMER, AMIGOS, K-EmoCon,...).
* [`index/taxonomy.md`](index/taxonomy.md): Khung phân loại kiến trúc kỹ thuật (Feature Fusion, Cross-Attention, Multi-task Loss, Disentanglement).
