import os
import sys
import csv
import json
import urllib.request
import urllib.parse
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = r"d:\ntk\eeg_paper_research\literature\open_access_repository"

KEYWORDS = [
    "kw1_multimodal_eeg_biosignals",
    "kw2_multitask_learning_affect",
    "kw3_multibranch_crossmodal_attention",
    "kw4_subspace_disentanglement_domain_adaptation",
    "kw5_missing_modality_wearable_robustness"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

def is_pdf(data):
    return data.startswith(b"%PDF-") or b"%PDF-" in data[:1024]

def try_download_url(url, dest_path):
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

def resolve_alternative_pdf_urls(doi, oa_url):
    candidates = []
    if oa_url:
        candidates.append(oa_url)
        if not oa_url.endswith(".pdf") and "doi.org" not in oa_url:
            candidates.append(oa_url.rstrip("/") + ".pdf")
            
    # arXiv resolution
    if "arxiv.org" in (oa_url or "") or "arxiv" in (doi or "").lower():
        arxiv_id = ""
        if "arxiv.org/abs/" in oa_url:
            arxiv_id = oa_url.split("arxiv.org/abs/")[-1].split("?")[0].strip()
        elif "arxiv.org/pdf/" in oa_url:
            arxiv_id = oa_url.split("arxiv.org/pdf/")[-1].replace(".pdf", "").split("?")[0].strip()
        if arxiv_id:
            candidates.insert(0, f"https://arxiv.org/pdf/{arxiv_id}.pdf")
            
    # Semantic Scholar OA Resolver
    if doi:
        clean_doi = doi.replace("https://doi.org/", "").strip()
        ss_url = f"https://api.semanticscholar.org/graph/v1/paper/{clean_doi}?fields=openAccessPdf"
        try:
            req = urllib.request.Request(ss_url, headers=HEADERS)
            with urllib.request.urlopen(req, context=CTX, timeout=5) as resp:
                ss_data = json.loads(resp.read().decode("utf-8"))
                oa_pdf_info = ss_data.get("openAccessPdf")
                if oa_pdf_info and oa_pdf_info.get("url"):
                    candidates.insert(0, oa_pdf_info.get("url"))
        except Exception:
            pass
            
    # Unpaywall direct resolver
    if doi:
        clean_doi = doi.replace("https://doi.org/", "").strip()
        unpay_url = f"https://api.unpaywall.org/v2/{clean_doi}?email=academic_researcher@university.edu"
        try:
            req = urllib.request.Request(unpay_url, headers=HEADERS)
            with urllib.request.urlopen(req, context=CTX, timeout=5) as resp:
                un_data = json.loads(resp.read().decode("utf-8"))
                best_loc = un_data.get("best_oa_location", {})
                if best_loc and best_loc.get("url_for_pdf"):
                    candidates.insert(0, best_loc.get("url_for_pdf"))
        except Exception:
            pass
            
    return candidates

def process_single_paper(paper_info, pdfs_dir):
    paper_id = paper_info["ID"]
    dest_path = os.path.join(pdfs_dir, f"{paper_id}.pdf")
    
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
        return paper_id, True, dest_path, "Already exists"
        
    # 1. Try explicit PDF URL
    if paper_info.get("PDF_URL"):
        if try_download_url(paper_info["PDF_URL"], dest_path):
            return paper_id, True, dest_path, "Direct PDF URL"
            
    # 2. Try OA URL
    if paper_info.get("OA_URL"):
        if try_download_url(paper_info["OA_URL"], dest_path):
            return paper_id, True, dest_path, "Direct OA URL"
            
    # 3. Try alternative resolvers
    candidates = resolve_alternative_pdf_urls(paper_info.get("DOI"), paper_info.get("OA_URL"))
    for cand in candidates:
        if try_download_url(cand, dest_path):
            return paper_id, True, dest_path, f"Resolved via {cand[:40]}..."
            
    return paper_id, False, None, "Download unavailable / Paywalled / HTML only"

def download_keyword_cluster(kw_id):
    kw_dir = os.path.join(BASE_DIR, kw_id)
    csv_file = os.path.join(kw_dir, "papers_index.csv")
    pdfs_dir = os.path.join(kw_dir, "pdfs")
    os.makedirs(pdfs_dir, exist_ok=True)
    
    if not os.path.exists(csv_file):
        print(f"CSV not found: {csv_file}")
        return 0, 0
        
    papers = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)
            
    print(f"\n[{kw_id}] Starting download for {len(papers)} papers...")
    
    downloaded_count = 0
    results = {}
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(process_single_paper, p, pdfs_dir): p for p in papers}
        for future in as_completed(futures):
            p_id, success, path, msg = future.result()
            results[p_id] = (success, path, msg)
            if success:
                downloaded_count += 1
                print(f"  [OK] {p_id}: Downloaded ({msg})")
            else:
                print(f"  [--] {p_id}: {msg}")
                
    print(f"[{kw_id}] Finished: {downloaded_count}/{len(papers)} PDFs stored in {pdfs_dir}\n")
    return downloaded_count, len(papers)

def main():
    print("=================================================================")
    print("STARTING BULK OPEN ACCESS PDF DOWNLOADER ACROSS 5 KEYWORDS")
    print("=================================================================")
    
    total_dl = 0
    total_all = 0
    
    for kw_id in KEYWORDS:
        dl, all_p = download_keyword_cluster(kw_id)
        total_dl += dl
        total_all += all_p
        
    print("=================================================================")
    print(f"SUMMARY: Successfully downloaded {total_dl}/{total_all} full-text PDFs locally!")
    print("=================================================================")

if __name__ == "__main__":
    main()
