import os
import sys
import csv
import json
import urllib.request
import urllib.parse
import ssl
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = r"d:\ntk\eeg_paper_research\literature\open_access_repository"

KEYWORDS = [
    {
        "id": "kw01_multimodal_eeg_biosignals",
        "name": "Multimodal EEG and Peripheral Biosignals for Emotion Recognition",
        "vietnamese_name": "Tín hiệu EEG và Sinh lý Đa phương thức cho Nhận diện Cảm xúc",
        "target_count": 50,
        "search_queries": [
            "EEG ECG EDA multimodal emotion recognition DEAP DREAMER",
            "multimodal physiological emotion recognition EEG peripheral biosignals",
            "EEG autonomic nervous system cardiac electrodermal emotion",
            "multimodal biosignal fusion emotion recognition affective computing"
        ]
    },
    {
        "id": "kw02_multitask_learning_affect",
        "name": "Multi-Task Learning for Affective Computing and Biosignals",
        "vietnamese_name": "Học Đa Nhiệm Vụ trong Tính toán Cảm xúc và Tín hiệu Sinh lý",
        "target_count": 50,
        "search_queries": [
            "multi-task learning emotion recognition EEG valence arousal",
            "multi-task deep learning physiological emotion classification regression",
            "joint valence arousal multi-task EEG biosignals",
            "multi-objective multi-task optimization affective computing biosignals"
        ]
    },
    {
        "id": "kw03_multibranch_crossmodal_attention",
        "name": "Multi-Branch Architectures and Cross-Modal Attention Fusion",
        "vietnamese_name": "Kiến trúc Đa nhánh và Cơ chế Chú ý Chéo Đa phương thức",
        "target_count": 50,
        "search_queries": [
            "multi-branch deep neural network EEG emotion recognition",
            "cross-modal attention EEG biosignal fusion emotion",
            "spatial temporal multi branch EEGNet fusion emotion",
            "cross-attention multimodal biosignal transformer emotion"
        ]
    },
    {
        "id": "kw04_subspace_disentanglement_domain_adaptation",
        "name": "Shared-Private Subspace Disentanglement and Domain Adaptation",
        "vietnamese_name": "Tách Không gian con Dùng chung - Riêng biệt và Thích ứng Miền",
        "target_count": 50,
        "search_queries": [
            "domain adaptation EEG emotion recognition cross-subject",
            "subspace disentanglement EEG emotion representation",
            "cross-subject transfer learning EEG affective biosignals",
            "unsupervised domain adaptation adversarial EEG emotion"
        ]
    },
    {
        "id": "kw05_missing_modality_wearable_robustness",
        "name": "Missing-Modality Robustness and Wearable Affective Biosensors",
        "vietnamese_name": "Độ bền vững khi Khuyết thiếu Cảm biến và Thiết bị Đeo Sinh lý",
        "target_count": 50,
        "search_queries": [
            "missing modality multimodal emotion recognition biosignals",
            "wearable EEG emotion recognition sensor noise robustness",
            "incomplete multimodal biosignals affective computing",
            "latent feature imputation missing modality EEG biosignals"
        ]
    },
    {
        "id": "kw06_foundation_models_self_supervised_biosignals",
        "name": "Foundation Models and Self-Supervised Learning for Biosignals",
        "vietnamese_name": "Mô hình Nền tảng và Học Tự Giám sát cho Tín hiệu Não & Y sinh",
        "target_count": 40,
        "search_queries": [
            "self-supervised learning EEG emotion recognition",
            "contrastive learning EEG biosignals representation",
            "masked autoencoder EEG physiological signal emotion",
            "foundation model EEG biosignal affective computing"
        ]
    },
    {
        "id": "kw07_graph_neural_networks_eeg_connectivity",
        "name": "Graph Neural Networks and Brain Connectivity for Emotion Recognition",
        "vietnamese_name": "Mạng Nơ-ron Đồ thị và Liên kết Não bộ cho Nhận diện Cảm xúc",
        "target_count": 40,
        "search_queries": [
            "dynamic graph convolutional network EEG emotion recognition DGCNN",
            "regularized graph neural network EEG emotion RGNN",
            "functional connectivity graph neural network EEG emotion",
            "spatial-temporal graph convolutional network EEG biosignals"
        ]
    },
    {
        "id": "kw08_transformers_crossmodal_affective_computing",
        "name": "Multimodal Transformers and Cross-Modal Interaction Networks",
        "vietnamese_name": "Kiến trúc Transformer Đa phương thức và Tương tác Chéo",
        "target_count": 40,
        "search_queries": [
            "multimodal transformer emotion recognition EEG",
            "cross-modal transformer physiological affective computing",
            "spatial temporal transformer EEG emotion recognition",
            "hierarchical transformer multimodal biosignal fusion"
        ]
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def is_pdf(data):
    return data.startswith(b"%PDF-") or b"%PDF-" in data[:1024]

def download_file(url, dest_path):
    if not url:
        return False
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=CTX, timeout=20) as resp:
            content = resp.read()
            if len(content) > 5000 and is_pdf(content[:1024]):
                with open(dest_path, "wb") as f:
                    f.write(content)
                return True
    except Exception:
        pass
    return False

def resolve_arxiv_pdf(title):
    try:
        clean_t = re.sub(r'[^a-zA-Z0-9 ]', '', title)
        encoded = urllib.parse.quote(clean_t)
        url = f"http://export.arxiv.org/api/query?search_query=ti:{encoded}&max_results=1"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=CTX, timeout=10) as resp:
            xml = resp.read().decode('utf-8')
            if "<id>http://arxiv.org/abs/" in xml:
                ar_id = xml.split("<id>http://arxiv.org/abs/")[1].split("</id>")[0].strip()
                return f"https://arxiv.org/pdf/{ar_id}.pdf"
    except Exception:
        pass
    return None

def resolve_europepmc(title):
    try:
        encoded = urllib.parse.quote(f'TITLE:"{title}"')
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={encoded}&format=json&resultType=core"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=CTX, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get("resultList", {}).get("result", [])
            for r in results:
                urls = r.get("fullTextUrlList", {}).get("fullTextUrl", [])
                for u in urls:
                    if u.get("documentStyle") == "pdf":
                        return u.get("url")
    except Exception:
        pass
    return None

def resolve_semanticscholar(title):
    try:
        encoded = urllib.parse.quote(title)
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded}&limit=1&fields=openAccessPdf,title"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=CTX, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get("data", [])
            if results and results[0].get("openAccessPdf"):
                return results[0]["openAccessPdf"].get("url")
    except Exception:
        pass
    return None

def fetch_and_download_paper_pdf(p, pdfs_dir):
    paper_id = p["ID"]
    dest_path = os.path.join(pdfs_dir, f"{paper_id}.pdf")
    
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
        return paper_id, True, "Already exists"
        
    title = p["Title"]
    oa_url = p.get("OA_URL", "")
    pdf_url = p.get("PDF_URL", "")
    
    # 1. Direct PDF URL
    if pdf_url and download_file(pdf_url, dest_path):
        return paper_id, True, "Direct PDF"
        
    # 2. OA URL
    if oa_url and download_file(oa_url, dest_path):
        return paper_id, True, "Direct OA"
        
    # 3. Frontiers / MDPI pattern
    if "frontiersin.org" in oa_url and download_file(oa_url.rstrip("/") + "/pdf", dest_path):
        return paper_id, True, "Frontiers PDF"
    if "mdpi.com" in oa_url and download_file(oa_url.rstrip("/") + "/pdf", dest_path):
        return paper_id, True, "MDPI PDF"
        
    # 4. arXiv
    ar_pdf = resolve_arxiv_pdf(title)
    if ar_pdf and download_file(ar_pdf, dest_path):
        return paper_id, True, "arXiv"
        
    # 5. Semantic Scholar
    ss_pdf = resolve_semanticscholar(title)
    if ss_pdf and download_file(ss_pdf, dest_path):
        return paper_id, True, "Semantic Scholar"
        
    # 6. Europe PMC
    pmc_pdf = resolve_europepmc(title)
    if pmc_pdf and download_file(pmc_pdf, dest_path):
        return paper_id, True, "Europe PMC"
        
    return paper_id, False, "Online Web Reader"

def is_relevant(title, abstract):
    text = (title + " " + abstract).lower()
    has_signal = any(k in text for k in ["eeg", "ecg", "eda", "gsr", "biosignal", "physiological", "brain", "cardiac", "electrodermal", "neuro", "wearable", "spatial-temporal"])
    has_affect = any(k in text for k in ["emotion", "affect", "valence", "arousal", "mood", "sentiment", "stress", "deap", "dreamer", "seed", "amigos", "cross-subject"])
    return has_signal and has_affect

def fetch_cluster_papers(kw):
    kw_dir = os.path.join(BASE_DIR, kw["id"])
    os.makedirs(kw_dir, exist_ok=True)
    notes_dir = os.path.join(kw_dir, "paper_notes")
    os.makedirs(notes_dir, exist_ok=True)
    pdfs_dir = os.path.join(kw_dir, "pdfs")
    os.makedirs(pdfs_dir, exist_ok=True)
    csv_file = os.path.join(kw_dir, "papers_index.csv")
    
    existing_papers = []
    seen_titles = set()
    
    if os.path.exists(csv_file):
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                existing_papers.append(r)
                seen_titles.add(r["Title"].strip().lower())
                
    target = kw["target_count"]
    print(f"\n=======================================================")
    print(f"Cluster: {kw['name']} ({kw['id']})")
    print(f"Current count: {len(existing_papers)} -> Target: {target}")
    print(f"=======================================================")
    
    new_papers = []
    headers = {"User-Agent": "PhDEEGResearch/1.0 (mailto:academic_researcher@university.edu)"}
    
    for q in kw["search_queries"]:
        if len(existing_papers) + len(new_papers) >= target:
            break
        encoded_q = urllib.parse.quote(q)
        url = f"https://api.openalex.org/works?search={encoded_q}&filter=is_oa:true,publication_year:>2022&per-page=50&sort=cited_by_count:desc"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for item in data.get("results", []):
                    title = item.get("title")
                    if not title:
                        continue
                    clean_t = title.strip().lower()
                    if clean_t in seen_titles:
                        continue
                        
                    abstract = ""
                    inv_abs = item.get("abstract_inverted_index")
                    if inv_abs:
                        word_pos = []
                        for word, positions in inv_abs.items():
                            for pos in positions:
                                word_pos.append((pos, word))
                        word_pos.sort(key=lambda x: x[0])
                        abstract = " ".join([w for _, w in word_pos])
                    else:
                        abstract = "Abstract available on open access publisher portal."
                        
                    if not is_relevant(title, abstract):
                        continue
                        
                    seen_titles.add(clean_t)
                    oa_info = item.get("open_access", {})
                    oa_url = oa_info.get("oa_url") or item.get("primary_location", {}).get("pdf_url") or item.get("primary_location", {}).get("landing_page_url") or item.get("doi", "")
                    pdf_url = item.get("primary_location", {}).get("pdf_url") or (oa_url if oa_url and oa_url.endswith(".pdf") else "")
                    authors = [a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])]
                    venue = item.get("primary_location", {}).get("source", {}).get("display_name", "Academic Venue") if item.get("primary_location", {}).get("source") else "Open Access Journal"
                    
                    paper_dict = {
                        "ID": f"OA_{kw['id'][:3].upper()}_{len(existing_papers)+len(new_papers)+1:03d}",
                        "Year": str(item.get("publication_year")),
                        "Title": title.strip(),
                        "Authors": ", ".join(authors[:5]) if authors else "Various Authors",
                        "Venue": venue,
                        "Citations": str(item.get("cited_by_count", 0)),
                        "DOI": item.get("doi", ""),
                        "OA_URL": oa_url,
                        "PDF_URL": pdf_url,
                        "Abstract": abstract
                    }
                    new_papers.append(paper_dict)
                    if len(existing_papers) + len(new_papers) >= target:
                        break
            time.sleep(1.0)
        except Exception as e:
            print(f"Query error: {e}")
            
    all_papers = existing_papers + new_papers
    print(f"Total papers in cluster: {len(all_papers)} (Added {len(new_papers)} new)")
    
    # Write CSV
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Year", "Title", "Authors", "Venue", "Citations", "DOI", "OA_URL", "PDF_URL"])
        writer.writeheader()
        for p in all_papers:
            writer.writerow({
                "ID": p["ID"],
                "Year": p["Year"],
                "Title": p["Title"],
                "Authors": p["Authors"],
                "Venue": p["Venue"],
                "Citations": p["Citations"],
                "DOI": p.get("DOI", ""),
                "OA_URL": p.get("OA_URL", ""),
                "PDF_URL": p.get("PDF_URL", "")
            })
            
    # Write Notes for new papers
    for p in new_papers:
        note_file = os.path.join(notes_dir, f"{p['ID']}.md")
        content = f"""# {p['ID']}: {p['Title']}

- **Title**: {p['Title']}
- **Authors**: {p['Authors']}
- **Year**: {p['Year']}
- **Venue / Source**: {p['Venue']}
- **Citations**: {p['Citations']}
- **DOI**: [{p.get('DOI', '')}]({p.get('DOI', '')})
- **Open Access URL**: [{p.get('OA_URL', '')}]({p.get('OA_URL', '')})
- **Keyword Category**: {kw['name']} ({kw['vietnamese_name']})

---

## Abstract
{p.get('Abstract', 'Abstract available on publisher portal.')}

---

## Relevance to Doctoral Research
- **Relevant Thesis Chapter**: Chapters 2, 3, 5
- **Research Theme**: {kw['vietnamese_name']}
"""
        with open(note_file, "w", encoding="utf-8") as f:
            f.write(content)
            
    # Concurrent Download of PDFs for all papers in cluster
    print(f"Downloading PDFs for {kw['id']}...")
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fetch_and_download_paper_pdf, p, pdfs_dir): p for p in all_papers}
        for future in as_completed(futures):
            p_id, success, msg = future.result()
            if success:
                if msg != "Already exists":
                    print(f"  [OK-NEW] {p_id}: {msg}")
            else:
                pass
                
    local_pdf_count = len([f for f in os.listdir(pdfs_dir) if f.endswith(".pdf") and os.path.getsize(os.path.join(pdfs_dir, f)) > 10000])
    recent_count = sum(1 for p in all_papers if int(p["Year"]) >= 2023)
    recent_pct = recent_count / len(all_papers) * 100 if all_papers else 0
    
    print(f"[{kw['id']}] PDF count: {local_pdf_count}/{len(all_papers)} | 2023+ pct: {recent_pct:.1f}%\n")
    
    return {
        "id": kw["id"],
        "name": kw["name"],
        "vn": kw["vietnamese_name"],
        "total": len(all_papers),
        "recent": recent_count,
        "recent_pct": recent_pct,
        "local_pdf": local_pdf_count
    }

def main():
    print("=================================================================")
    print("EXPANDING LITERATURE REPOSITORY ACROSS 8 SPECIALIZED KEYWORDS")
    print("=================================================================")
    
    summary_data = []
    for kw in KEYWORDS:
        stat = fetch_cluster_papers(kw)
        summary_data.append(stat)
        
    # Update All READMEs
    for kw_stat in summary_data:
        kw_id = kw_stat["id"]
        kw_dir = os.path.join(BASE_DIR, kw_id)
        csv_file = os.path.join(kw_dir, "papers_index.csv")
        readme_file = os.path.join(kw_dir, "README.md")
        pdfs_dir = os.path.join(kw_dir, "pdfs")
        
        papers = []
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                papers.append(r)
                
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(f"# Cụm Tài Liệu Mở: {kw_stat['vn']} (`{kw_id}`)\n\n")
            f.write(f"- **Tổng số bài báo khoa học**: {len(papers)} bài báo Open Access\n")
            f.write(f"- **Số file PDF đã tải về máy**: **{kw_stat['local_pdf']}/{len(papers)} bài** (Có thể đọc offline ngay)\n")
            f.write(f"- **Tỷ lệ bài báo từ 2023 đến 2026**: **{kw_stat['recent_pct']:.1f}%** ({kw_stat['recent']}/{len(papers)} bài)\n\n")
            f.write("---\n\n## Danh mục Toàn bộ Bài Báo Khoa học & Liên kết PDF\n\n")
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
        f.write("# KHO TÀI LIỆU MỞ MỞ RỘNG (EXPANDED OPEN ACCESS LITERATURE REPOSITORY)\n")
        f.write("## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH ĐA PHƯƠNG THỨC\n\n")
        f.write("Kho tài liệu mở rộng bao gồm **8 cụm từ khóa chuyên sâu**, cung cấp nguồn tư liệu toàn văn hiện đại giai đoạn **2023–2026** phục vụ cho nghiên cứu sinh.\n\n")
        f.write(f"- **Tổng số bài báo khoa học Open Access**: **{total_papers} bài**\n")
        f.write(f"- **Số file toàn văn PDF đã tải về máy**: **{total_local}/{total_papers} bài PDF offline** (lưu trữ trong các thư mục `pdfs/`)\n")
        f.write(f"- **Tỷ lệ công bố từ 2023 đến 2026**: **{overall_pct:.1f}%** ({total_recent}/{total_papers} bài)\n\n")
        f.write("---\n\n## 1. Bảng Chỉ Mục 8 Cụm Từ Khóa Chuyên Sâu\n\n")
        f.write("| Thư mục / Cụm từ khóa | Tên Tiếng Việt | Tổng bài | Bài 2023–2026 | Tỷ lệ 2023+ | File PDF Đã Tải | Thư mục chi tiết |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for s in summary_data:
            f.write(f"| **`{s['id']}`** | {s['vn']} | {s['total']} | {s['recent']} | **{s['recent_pct']:.1f}%** | **{s['local_pdf']} / {s['total']} PDF** | [`{s['id']}/README.md`]({s['id']}/README.md) |\n")
            
        f.write("\n---\n\n## 2. Các Nền Tảng Dữ Liệu Truy Cập Mở Được Tích Hợp\n\n")
        f.write("1. **OpenAlex Academic Graph** ([openalex.org](https://openalex.org))\n")
        f.write("2. **arXiv.org** ([arxiv.org](https://arxiv.org))\n")
        f.write("3. **IEEE Open Access / IEEE TAFFC OA** ([ieeexplore.ieee.org](https://ieeexplore.ieee.org))\n")
        f.write("4. **Frontiers in Neuroscience / Human Neuroscience Open** ([frontiersin.org](https://www.frontiersin.org))\n")
        f.write("5. **MDPI Sensors / Brain Sciences / Electronics** ([mdpi.com](https://www.mdpi.com))\n")
        f.write("6. **PubMed Central (PMC) & Europe PMC** ([europepmc.org](https://europepmc.org))\n")
        f.write("7. **Semantic Scholar Open Access Corpus** ([semanticscholar.org](https://www.semanticscholar.org))\n")

    print("\n=================================================================")
    print(f"EXPANSION COMPLETE: {total_local}/{total_papers} PDFs locally stored across 8 keywords!")
    print(f"Master index updated at: {master_readme}")
    print("=================================================================")

if __name__ == "__main__":
    main()
