import os

classified_dir = r"d:\ntk\eeg_paper_research\literature\02_classified"

cats = {
    "EEG": "Các bài báo và phương pháp xử lý tín hiệu điện não (EEG) đa kênh, Spatial-Temporal Filtering, GNNs.",
    "ECG": "Tín hiệu điện tim (ECG), biến thiên nhịp tim (HRV) và trích xuất đặc trưng hình thái sóng.",
    "EDA_GSR": "Phản xạ da (Electrodermal Activity / GSR), thành phần Tonic và Phasic đáp ứng cảm xúc.",
    "PPG": "Quang thể tích đồ (PPG) từ thiết bị đeo thông minh (Smartwatch / Wristband).",
    "EMG": "Điện cơ (EMG) cơ mặt và cơ thang nhận diện biểu cảm vi mô.",
    "Respiration": "Tín hiệu nhịp thở (Respiration Rate / Amplitude) phản ánh mức độ thư giãn và kích động.",
    "Multimodal": "Tích hợp đồng thời đa phương thức tín hiệu sinh lý và hành vi.",
    "MultiBranch": "Kiến trúc mạng nơ-ron đa nhánh xử lý song song từng kênh tín hiệu độc lập.",
    "MultiTask": "Học đa nhiệm vụ tối ưu hóa liên hợp Valence, Arousal, Dominance và Subject Invariance.",
    "Fusion": "Cơ chế dung hợp đặc trưng: Early, Late, Hybrid, Cross-Modal Attention, Bilinear Pooling.",
    "Generalization": "Khả năng tổng quát hóa qua đối tượng mới (Cross-subject), Thích ứng miền (Domain Adaptation).",
    "SelfSupervised": "Học tự giám sát (Self-Supervised Learning / SSL) và Mô hình nền tảng (Foundation Models) cho tín hiệu Y sinh.",
    "EfficientModels": "Mô hình nén nhẹ, tối ưu hóa tính toán biên (Edge Computing / Real-time BCI).",
    "Reviews": "Các bài báo tổng quan, khảo sát hệ thống (Systematic Literature Reviews & Surveys)."
}

classified_readme = """# HỆ THỐNG PHÂN LOẠI TÀI LIỆU THEO PHÂN HỆ NGHIÊN CỨU (`02_classified/`)

Thư mục này tổ chức và liên kết các bài báo trong kho dữ liệu theo từng phân hệ kỹ thuật và loại tín hiệu sinh lý chuyên biệt:

"""

for cat, desc in cats.items():
    classified_readme += f"- **[`{cat}/`]({cat}/README.md)**: {desc}\n"
    cat_dir = os.path.join(classified_dir, cat)
    os.makedirs(cat_dir, exist_ok=True)
    with open(os.path.join(cat_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# Phân Hệ Tài Liệu: {cat}\n\n**Mô tả**: {desc}\n\nXem thêm danh mục bài báo chi tiết tại [Kho 10 Cụm Tài Liệu Mở](../../open_access_repository/README.md) và [30 Bài Báo Cốt Lõi](../../03_notes/).\n")

with open(os.path.join(classified_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(classified_readme)

print("02_classified populated successfully.")
