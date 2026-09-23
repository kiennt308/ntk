import os
import glob
import json
import csv

ws_dir = r"d:\ntk\eeg_paper_research\notebooklm_workspace"
oa_dir = r"d:\ntk\eeg_paper_research\literature\open_access_repository"

notebook_definitions = [
    {
        "id": "NB01",
        "folder": "notebook_01_Multimodal_EEG_Biosignals",
        "oa_folder": "kw01_multimodal_eeg_biosignals",
        "title_en": "Multimodal EEG & Peripheral Biosignals (EEG, ECG, EDA, PPG, Respiration)",
        "title_vi": "Nền tảng Tín hiệu Não (EEG) và Tín hiệu Sinh lý Tự chủ (ECG, EDA)",
        "chapter_mapping": "Chương 2 & Chương 4 (Tổng quan Sinh học Thần kinh & Giao thức Dữ liệu)",
        "research_focus": "Cortical cognitive appraisal vs. Autonomic physiological arousal, DEAP/DREAMER benchmarks, signal filtering, CAR, and HRV/CDA feature extraction.",
        "key_questions": [
            "Các dải tần số EEG (Theta, Alpha, Beta, Gamma) tương quan thế nào với Valence và Arousal?",
            "Làm thế nào để đồng bộ hóa (synchronization) tần số lấy mẫu giữa EEG (128-512 Hz) và EDA/ECG (4-64 Hz)?",
            "Đặc trưng sinh lý ngoại vi nào (HRV time/frequency domain, GSR Phasic tonic) bổ trợ mạnh nhất cho EEG?"
        ]
    },
    {
        "id": "NB02",
        "folder": "notebook_02_Multi_Task_Learning_Affect",
        "oa_folder": "kw02_multitask_learning_affect",
        "title_en": "Multi-Task Learning in Affective Computing & Biosignals",
        "title_vi": "Học Đa Nhiệm Vụ trong Tính toán Cảm xúc & Tín hiệu Sinh lý",
        "chapter_mapping": "Chương 3 & Chương 6 (Kiến trúc Đề xuất MMB-EmotionNet & Kiểm định Đa nhiệm vụ)",
        "research_focus": "Joint Valence-Arousal-Dominance optimization, Kendall uncertainty loss weighting, GradNorm gradient balancing, and task synergy vs. negative transfer.",
        "key_questions": [
            "Làm sao để cân bằng hàm mất mát đa nhiệm giữa phân loại Valence, Arousal và Dominance mà không bị Overfitting?",
            "Cơ chế chia sẻ tham số (Hard vs Soft Parameter Sharing) nào tối ưu nhất cho tín hiệu y sinh?",
            "Làm thế nào để đo lường Negative Transfer giữa các nhiệm vụ cảm xúc?"
        ]
    },
    {
        "id": "NB03",
        "folder": "notebook_03_Multi_Branch_Cross_Modal_Attention",
        "oa_folder": "kw03_multibranch_crossmodal_attention",
        "title_en": "Multi-Branch Architectures & Cross-Modal Attention Mechanisms",
        "title_vi": "Kiến trúc Đa nhánh & Cơ chế Chú ý Chéo Đa phương thức",
        "chapter_mapping": "Chương 3 & Chương 5 (Tầng mã hóa chuyên biệt & Thực nghiệm Triệt tiêu Attention)",
        "research_focus": "Signal-specific deep feature encoders (Spatial-GCN for EEG, TCN for ECG, CWT-CNN for EDA), and bidirectional QKV cross-modal attention fusion.",
        "key_questions": [
            "Tại sao kiến trúc đa nhánh (Multi-branch) vượt trội hơn việc nối vector thô (Early Concatenation)?",
            "Cơ chế Cross-Attention Query-Key-Value giữa EEG và Biosignals hoạt động ra sao về mặt toán học?",
            "Kết quả thử nghiệm Ablation Study chứng minh vai trò của từng nhánh tín hiệu như thế nào?"
        ]
    },
    {
        "id": "NB04",
        "folder": "notebook_04_Subspace_Disentanglement_Domain_Adaptation",
        "oa_folder": "kw04_subspace_disentanglement_domain_adaptation",
        "title_en": "Shared-Private Subspace Disentanglement & Domain Adaptation",
        "title_vi": "Tách Không gian con Dùng chung - Riêng biệt & Thích ứng Miền",
        "chapter_mapping": "Chương 3 & Chương 5 (Phân tách Biểu diễn & Thử nghiệm Tổng quát hóa LOSO)",
        "research_focus": "Decomposing representations into subject-invariant emotion content (Z_shared) and subject-specific physiological style (Z_private) with orthogonality constraints.",
        "key_questions": [
            "Làm thế nào để ràng buộc trực giao (Orthogonality Constraint) giữa Z_shared và Z_private?",
            "Hiệu quả cải thiện độ chính xác phân loại cảm xúc Cross-Subject (LOSO) đạt được bao nhiêu %?",
            "Domain Adversarial Neural Networks (DANN) kết hợp với Disentanglement như thế nào?"
        ]
    },
    {
        "id": "NB05",
        "folder": "notebook_05_Missing_Modality_Wearable_Robustness",
        "oa_folder": "kw05_missing_modality_wearable_robustness",
        "title_en": "Missing Modality Robustness & Physiological Wearables",
        "title_vi": "Độ bền vững khi Khuyết thiếu Cảm biến & Thiết bị Đeo Sinh lý",
        "chapter_mapping": "Chương 5 (Thực nghiệm Bền vững, Rớt cảm biến & Đo kiểm Độ trễ Biên)",
        "research_focus": "Handling missing sensor streams in wild environments via cross-modal knowledge distillation, generative imputation (GAN/VAE), and masked biosignal modeling.",
        "key_questions": [
            "Mô hình hoạt động như thế nào khi mất hoàn toàn tín hiệu EEG (chỉ còn ECG/GSR từ đồng hồ đeo tay)?",
            "Chiến lược Teacher-Student Knowledge Distillation giúp bảo toàn bao nhiêu % hiệu năng?",
            "Độ trễ suy luận (Inference Latency) và mức tiêu thụ tài nguyên trên thiết bị biên (Edge Hardware) là bao nhiêu?"
        ]
    },
    {
        "id": "NB06",
        "folder": "notebook_06_Foundation_Models_Self_Supervised_Biosignals",
        "oa_folder": "kw06_foundation_models_self_supervised_biosignals",
        "title_en": "Foundation Models & Self-Supervised Learning for Biosignals",
        "title_vi": "Mô hình Nền tảng & Học Tự Giám sát cho Tín hiệu Não & Y sinh",
        "chapter_mapping": "Chương 2 & Chương 7 (Xu hướng Công nghệ Mới 2023–2026 & Hướng Phát triển)",
        "research_focus": "Large-scale self-supervised pre-training (Masked Autoencoding, Contrastive Learning) on massive unlabeled EEG/Physiological corpora.",
        "key_questions": [
            "Các Foundation Models cho EEG (như BIOT, BrainBERT, Neuro-GPT) có cấu trúc ra sao?",
            "Lợi ích của việc Pre-training tự giám sát trên tập dữ liệu lớn đối với downstream task cảm xúc?",
            "Fine-tuning chiến lược Parameter-Efficient (LoRA, Adapter) cho mô hình y sinh."
        ]
    },
    {
        "id": "NB07",
        "folder": "notebook_07_Graph_Neural_Networks_Brain_Connectivity",
        "oa_folder": "kw07_graph_neural_networks_eeg_connectivity",
        "title_en": "Graph Neural Networks & Brain Functional Connectivity for Emotion",
        "title_vi": "Mạng Nơ-ron Đồ thị & Liên kết Não bộ cho Nhận diện Cảm xúc",
        "chapter_mapping": "Chương 2, 4 & 5 (Các Mô hình Đối sánh SOTA Đồ thị)",
        "research_focus": "Dynamic Graph Convolutional Networks (DGCNN), Regularized Graph Neural Networks (RGNN), Phase Locking Value (PLV), and hemisphere asymmetry graph topologies.",
        "key_questions": [
            "Cách xây dựng ma trận kề động (Dynamic Adjacency Matrix) từ tín hiệu EEG đa kênh?",
            "Sự bất đối xứng bán cầu não (Frontal Alpha Asymmetry) được mô hình hóa qua đồ thị như thế nào?",
            "So sánh hiệu năng giữa GCN, GAT và Spatio-Temporal Graph Networks trên SEED/DEAP."
        ]
    },
    {
        "id": "NB08",
        "folder": "notebook_08_Transformers_Crossmodal_Affective_Computing",
        "oa_folder": "kw08_transformers_crossmodal_affective_computing",
        "title_en": "Transformer Architectures in Crossmodal Affective Computing",
        "title_vi": "Kiến trúc Transformer Đa phương thức và Tương tác Chéo",
        "chapter_mapping": "Chương 2 & Chương 3 (So sánh Đối sánh Transformer & MulT / MISA)",
        "research_focus": "Multimodal Transformers (MulT), Cross-attention encoders, spatio-temporal self-attention, and long-range dependencies in continuous affective dynamics.",
        "key_questions": [
            "Kiến trúc Multimodal Transformer giải quyết độ trễ pha (phase shift) giữa các tín hiệu như thế nào?",
            "Cơ chế Positional Encoding thích ứng với chuỗi thời gian sinh lý phi đều đặn.",
            "So sánh độ phức tạp tính toán giữa Self-Attention và Cross-Attention trong dung hợp đa tín hiệu."
        ]
    },
    {
        "id": "NB09",
        "folder": "notebook_09_Explainable_AI_Interpretable_Biosignals",
        "oa_folder": "kw09_explainable_ai_interpretable_biosignals",
        "title_en": "Explainable AI (XAI) & Interpretable Biosignal Modeling",
        "title_vi": "Trí tuệ Nhân tạo Giải thích được (XAI) & Minh bạch Mô hình Cảm xúc",
        "chapter_mapping": "Chương 5 & Chương 7 (Phân tích Trực quan hóa Bản đồ Não & Ý nghĩa Sinh học)",
        "research_focus": "SHAP, Integrated Gradients, Grad-CAM topographic scalp maps, and neuroscience validation of learned multi-branch feature representations.",
        "key_questions": [
            "Cách trực quan hóa trọng số đóng góp của các vùng vỏ não (Frontal, Temporal, Parietal, Occipital) lên bản đồ địa hình não (Topoplot)?",
            "Làm sao để chứng minh mô hình học được đặc trưng sinh học thực tế thay vì học nhiễu artifact?",
            "Giải thích sự tương tác giữa nhịp tim (HRV) và điện não (EEG) qua Grad-CAM/SHAP."
        ]
    },
    {
        "id": "NB10",
        "folder": "notebook_10_Closed_Loop_BCI_RealTime_Affective_Systems",
        "oa_folder": "kw10_closed_loop_bci_realtime_affective_systems",
        "title_en": "Closed-Loop BCI, Edge Computing & Real-Time Affective Systems",
        "title_vi": "Hệ thống BCI Vòng lặp Khép kín, Tính toán Biên Thời gian thực",
        "chapter_mapping": "Chương 7 (Ứng dụng Thực tiễn Y tế, BCI Thiết bị đeo & Định hướng Tương lai)",
        "research_focus": "Closed-loop neurofeedback, real-time edge deployment, quantization, model pruning, and clinical interventions for affective disorders.",
        "key_questions": [
            "Kiến trúc hệ thống vòng lặp khép kín (Closed-loop Affective BCI) từ thu thập, lọc thời gian thực đến điều khiển phản hồi sinh học (Biofeedback)?",
            "Phương pháp lượng tử hóa (Quantization INT8/FP16) và nén mô hình để chạy trên Raspberry Pi / NVIDIA Jetson / Mobile NPU.",
            "Tiêu chuẩn an toàn và bảo mật dữ liệu y sinh cá nhân (Federated Learning & Privacy)."
        ]
    }
]

for nb in notebook_definitions:
    nb_dir = os.path.join(ws_dir, nb["folder"])
    oa_path = os.path.join(oa_dir, nb["oa_folder"])
    os.makedirs(nb_dir, exist_ok=True)
    
    # Read paper index from CSV if available
    csv_file = os.path.join(oa_path, "papers_index.csv")
    papers_list = []
    if os.path.exists(csv_file):
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                papers_list.append({
                    "id": row.get("id", ""),
                    "year": row.get("year", ""),
                    "title": row.get("title", ""),
                    "authors": row.get("authors", ""),
                    "venue": row.get("venue", ""),
                    "citations": row.get("citations", ""),
                    "doi": row.get("doi", ""),
                    "pdf_url": row.get("pdf_url", "")
                })
    
    # Check PDF count
    pdf_dir = os.path.join(nb_dir, "pdfs")
    pdf_files = [os.path.basename(p) for p in glob.glob(os.path.join(pdf_dir, "*.pdf"))] if os.path.exists(pdf_dir) else []
    
    # Write metadata JSON
    metadata = {
        "notebook_id": nb["id"],
        "folder_name": nb["folder"],
        "title_en": nb["title_en"],
        "title_vi": nb["title_vi"],
        "phd_chapter_mapping": nb["chapter_mapping"],
        "research_focus": nb["research_focus"],
        "key_research_questions": nb["key_questions"],
        "total_papers_indexed": len(papers_list),
        "total_pdfs_available": len(pdf_files),
        "pdf_filenames": pdf_files,
        "papers": papers_list
    }
    
    with open(os.path.join(nb_dir, "notebook_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    # Write standardized README.md for the notebook
    nb_readme = f"""# {nb['id']} - {nb['title_en']}
## Chủ đề Tiếng Việt: {nb['title_vi']}

- **Ánh xạ Chương Luận Án**: **{nb['chapter_mapping']}**
- **Trọng tâm Nghiên cứu**: {nb['research_focus']}
- **Tổng số bài báo khoa học chỉ mục**: **{len(papers_list)} bài** (Giai đoạn 2023–2026)
- **Số lượng file PDF toàn văn sẵn có**: **{len(pdf_files)} file PDF** (trong thư mục [`pdfs/`](pdfs/))

---

## 🎯 Các Câu Hỏi Nghiên Cứu Trọng Tâm
"""
    for idx, q in enumerate(nb["key_questions"], 1):
        nb_readme += f"{idx}. {q}\n"
    
    nb_readme += f"""
---

## 🚀 Bộ Prompt Master Class Dành Cho NotebookLM
Mở file [`00_NOTEBOOKLM_PROMPTS_AND_INDEX.md`](00_NOTEBOOKLM_PROMPTS_AND_INDEX.md) để sử dụng toàn bộ **6 Prompts trích xuất chuyên sâu**:
- **Prompt 1**: Khảo sát & Phân tích Đột phá Công nghệ (2023–2026).
- **Prompt 2**: Bóc tách Kỹ thuật, Hàm mất mát & Chi tiết Toán học.
- **Prompt 3**: Kiểm toán Dữ liệu, Giao thức Đánh giá & Ngăn ngừa Rò rỉ (Leakage).
- **Prompt 4**: Phân tích Ma trận So sánh & Trích xuất Khoảng trống Nghiên cứu (Research Gaps).
- **Prompt 5**: Đề xuất Giải pháp Cải tiến & Đóng góp Mới cho Luận án Tiến sĩ.
- **Prompt 6**: Trích xuất Toàn văn Trích dẫn Học thuật Chuẩn IEEE / APA.

---

## 📂 Danh Mục Bài Báo Trong Notebook
Chi tiết toàn văn và tóm tắt từng bài báo có thể xem tại:
- [Tài liệu tóm tắt mở rộng](../../literature/open_access_repository/{nb['oa_folder']}/README.md)
- [Bảng dữ liệu thô `papers_index.csv`](../../literature/open_access_repository/{nb['oa_folder']}/papers_index.csv)
"""
    with open(os.path.join(nb_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(nb_readme)

print("Standardized all 10 notebook workspaces.")
