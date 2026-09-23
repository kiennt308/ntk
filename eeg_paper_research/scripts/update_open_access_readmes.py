import os
import csv

BASE_DIR = r"d:\ntk\eeg_paper_research\literature\open_access_repository"
KEYWORDS = [
    ("kw01_multimodal_eeg_biosignals", "Tín hiệu EEG và Sinh lý Đa phương thức cho Nhận diện Cảm xúc"),
    ("kw02_multitask_learning_affect", "Học Đa Nhiệm Vụ trong Tính toán Cảm xúc và Tín hiệu Sinh lý"),
    ("kw03_multibranch_crossmodal_attention", "Kiến trúc Đa nhánh và Cơ chế Chú ý Chéo Đa phương thức"),
    ("kw04_subspace_disentanglement_domain_adaptation", "Tách Không gian con Dùng chung - Riêng biệt và Thích ứng Miền"),
    ("kw05_missing_modality_wearable_robustness", "Độ bền vững khi Khuyết thiếu Cảm biến và Thiết bị Đeo Sinh lý")
]

def update_readmes():
    summary_data = []
    
    for kw_id, kw_vn in KEYWORDS:
        kw_dir = os.path.join(BASE_DIR, kw_id)
        csv_file = os.path.join(kw_dir, "papers_index.csv")
        readme_file = os.path.join(kw_dir, "README.md")
        pdfs_dir = os.path.join(kw_dir, "pdfs")
        
        if not os.path.exists(csv_file):
            continue
            
        papers = []
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                papers.append(r)
                
        recent_count = sum(1 for p in papers if int(p["Year"]) >= 2023)
        recent_pct = recent_count / len(papers) * 100 if papers else 0
        local_pdf_count = len([f for f in os.listdir(pdfs_dir) if f.endswith(".pdf") and os.path.getsize(os.path.join(pdfs_dir, f)) > 10000]) if os.path.exists(pdfs_dir) else 0
        
        summary_data.append({
            "id": kw_id,
            "vn": kw_vn,
            "total": len(papers),
            "recent": recent_count,
            "recent_pct": recent_pct,
            "local_pdf": local_pdf_count
        })
        
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(f"# Cụm Tài Liệu Mở: {kw_vn} (`{kw_id}`)\n\n")
            f.write(f"- **Tổng số bài báo khoa học**: {len(papers)} bài báo Open Access\n")
            f.write(f"- **Số bài đã tải File PDF về máy**: **{local_pdf_count}/{len(papers)} bài** (Có thể mở đọc toàn văn offline ngay lập tức)\n")
            f.write(f"- **Tỷ lệ bài báo từ 2023 đến 2026**: **{recent_pct:.1f}%** ({recent_count}/{len(papers)} bài)\n\n")
            f.write("---\n\n## Danh mục Toàn bộ 35 Bài Báo Khoa học & Liên kết PDF\n\n")
            f.write("| ID | Năm | Tiêu đề bài báo | Nguồn / Tạp chí | Trích dẫn | File PDF Cục Bộ / Link Truy Cập |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
            
            for p in papers:
                p_id = p["ID"]
                pdf_path = os.path.join(pdfs_dir, f"{p_id}.pdf")
                has_local = os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 10000
                
                local_btn = f"[📄 **Đọc PDF cục bộ**](pdfs/{p_id}.pdf)" if has_local else "[🌐 Đọc trực tuyến]"
                oa_url = p.get("OA_URL", "")
                oa_link = f" ([Link gốc]({oa_url}))" if oa_url else ""
                
                authors = p.get("Authors", "")
                authors_short = authors[:40] + ("..." if len(authors) > 40 else "")
                
                f.write(f"| [`{p_id}`](paper_notes/{p_id}.md) | **{p['Year']}** | **{p['Title']}**<br>*{authors_short}* | {p['Venue']} | {p['Citations']} | {local_btn}{oa_link} |\n")

    # Update Master README
    master_readme = os.path.join(BASE_DIR, "README.md")
    total_papers = sum(s["total"] for s in summary_data)
    total_recent = sum(s["recent"] for s in summary_data)
    total_local = sum(s["local_pdf"] for s in summary_data)
    overall_pct = total_recent / total_papers * 100 if total_papers else 0
    
    with open(master_readme, "w", encoding="utf-8") as f:
        f.write("# KHO TÀI LIỆU MỞ (OPEN ACCESS LITERATURE REPOSITORY)\n")
        f.write("## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH ĐA PHƯƠNG THỨC\n\n")
        f.write("Kho tài liệu này được cấu trúc thành **5 cụm từ khóa chuyên sâu**, phục vụ trực tiếp cho nghiên cứu sinh phân tích bối cảnh công nghệ mới nhất giai đoạn **2023–2026**.\n\n")
        f.write(f"- **Tổng số bài báo Open Access**: **{total_papers} bài** (35 bài / thư mục)\n")
        f.write(f"- **Số file toàn văn PDF đã tải về máy**: **{total_local}/{total_papers} bài PDF offline** (sẵn sàng đọc trong thư mục `pdfs/`)\n")
        f.write(f"- **Tỷ lệ công bố từ 2023 đến 2026**: **{overall_pct:.1f}%** ({total_recent}/{total_papers} bài)\n\n")
        f.write("---\n\n## 1. Bảng Chỉ Mục 5 Cụm Từ Khóa & Tình Trạng File PDF Cục Bộ\n\n")
        f.write("| Thư mục / Cụm từ khóa | Tên Tiếng Việt | Tổng bài | Bài 2023–2026 | Tỷ lệ 2023+ | File PDF Đã Tải | Thư mục chi tiết |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for s in summary_data:
            f.write(f"| **`{s['id']}`** | {s['vn']} | {s['total']} | {s['recent']} | **{s['recent_pct']:.1f}%** | **{s['local_pdf']} / 35 PDF** | [`{s['id']}/README.md`]({s['id']}/README.md) |\n")
            
        f.write("\n---\n\n## 2. Các Nguồn Dữ Liệu Truy Cập Mở Đã Sử Dụng\n\n")
        f.write("1. **OpenAlex Academic Graph** ([openalex.org](https://openalex.org))\n")
        f.write("2. **arXiv.org** ([arxiv.org](https://arxiv.org))\n")
        f.write("3. **IEEE Open Access / IEEE TAFFC OA** ([ieeexplore.ieee.org](https://ieeexplore.ieee.org))\n")
        f.write("4. **Frontiers in Neuroscience Open** ([frontiersin.org](https://www.frontiersin.org))\n")
        f.write("5. **MDPI Sensors / Brain Sciences** ([mdpi.com](https://www.mdpi.com))\n")
        f.write("6. **PubMed Central (PMC) & Europe PMC** ([europepmc.org](https://europepmc.org))\n")
        f.write("7. **Semantic Scholar Open Access Corpus** ([semanticscholar.org](https://www.semanticscholar.org))\n")

    print("Master and keyword READMEs updated successfully!")

if __name__ == "__main__":
    update_readmes()
