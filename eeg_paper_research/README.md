# 🧠 HỆ THỐNG TẢI & KHAI THÁC BÀI BÁO Y SINH CHO ĐỀ TÀI TIẾN SĨ (PhD)

---

> ### 🎓 **ĐỀ TÀI TIẾN SĨ (PhD THESIS TOPIC):**
> **“Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức”**
> *(Multi-task Multi-branch Architecture for Emotion Recognition from Multimodal Biosignals)*

---

```text
                    ĐỀ TÀI CỦA BẠN
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
   Multimodal         Multi-task       Multi-branch
   Biosignals         Learning         Architecture
        │                 │                 │
   EEG + ECG          Emotion          CNN/Transformer
   EDA/GSR            Valence          Attention
   EMG                Arousal          Fusion
   etc.               Discrete         Experts
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                  Emotion Recognition
```

---

## ⚡ HƯỚNG DẪN NHANH (QUICK START)

### 1. Tự Động Phân Loại Toàn Bộ Bài Báo Vào 5 Track Workspace:
```powershell
cd d:\ntk\eeg_paper_downloader
python filter_and_packager.py --max-per-track 35
```

### 2. Tải Bài Báo Bổ Sung Chuyên Sâu Từng Trục:
```powershell
# Track 3: Multi-Task Learning trong Biosignals
python oa_paper_fetcher.py --track 3 --limit 20

# Track 4: Multi-Branch & Cross-Modal Attention
python oa_paper_fetcher.py --track 4 --limit 20

# Track 5: Missing Modality & Robustness
python oa_paper_fetcher.py --track 5 --limit 20
```

### 3. Nạp Vào 5 Thư Mục NotebookLM Tương Ứng:
* `notebooklm_workspace/notebook_01_Biosignal_Emotion_Recognition`
* `notebooklm_workspace/notebook_02_Multimodal_Emotion_Recognition`
* `notebooklm_workspace/notebook_03_Multi_Task_Learning_Emotion`
* `notebooklm_workspace/notebook_04_Multi_Branch_Fusion_Architecture`
* `notebooklm_workspace/notebook_05_Generalization_Robustness_Missing_Modality`

---

## 📖 TÀI LIỆU HƯỚNG DẪN CHI TIẾT

Toàn bộ nội dung phân tích đề tài, bộ Prompt Master Class 20 tiêu chí, ma trận nghiên cứu (Research Matrix), hệ thống giả thuyết H1–H6 và câu hỏi nghiên cứu RQ1–RQ6 được cập nhật đầy đủ tại:

👉 **[HUONG_DAN_TRIEN_KHAI_PHD_NOTEBOOKLM.md](./HUONG_DAN_TRIEN_KHAI_PHD_NOTEBOOKLM.md)**
