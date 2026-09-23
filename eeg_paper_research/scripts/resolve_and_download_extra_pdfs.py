import os
import sys
import csv
import json
import urllib.request
import urllib.parse
import ssl
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = r"d:\ntk\eeg_paper_research\literature\open_access_repository"
KEYWORDS = [
    "kw01_multimodal_eeg_biosignals",
    "kw02_multitask_learning_affect",
    "kw03_multibranch_crossmodal_attention",
    "kw04_subspace_disentanglement_domain_adaptation",
    "kw05_missing_modality_wearable_robustness"
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

def resolve_by_semanticscholar_title(title):
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

def resolve_by_europepmc(title):
    try:
        encoded = urllib.parse.quote(f'TITLE:"{title}"')
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={encoded}&format=json&resultType=core"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=CTX, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get("resultList", {}).get("result", [])
            for r in results:
                # check fullTextUrlList
                urls = r.get("fullTextUrlList", {}).get("fullTextUrl", [])
                for u in urls:
                    if u.get("documentStyle") == "pdf":
                        return u.get("url")
    except Exception:
        pass
    return None

def resolve_by_arxiv_api(title):
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

def fetch_missing_paper_pdf(p, pdfs_dir):
    paper_id = p["ID"]
    dest_path = os.path.join(pdfs_dir, f"{paper_id}.pdf")
    
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
        return paper_id, True, "Already exists"
        
    title = p["Title"]
    doi = p.get("DOI", "")
    oa_url = p.get("OA_URL", "")
    
    # 1. Direct Pattern Transforms (Frontiers, MDPI, BioRxiv)
    if "frontiersin.org" in oa_url and not oa_url.endswith("/pdf"):
        if download_file(oa_url + "/pdf", dest_path):
            return paper_id, True, "Frontiers pattern"
    if "mdpi.com" in oa_url and not oa_url.endswith("/pdf"):
        if download_file(oa_url + "/pdf", dest_path):
            return paper_id, True, "MDPI pattern"
            
    # 2. Try Semantic Scholar Title Search
    ss_pdf = resolve_by_semanticscholar_title(title)
    if ss_pdf and download_file(ss_pdf, dest_path):
        return paper_id, True, "Semantic Scholar OA"
        
    # 3. Try Europe PMC Title Search
    epmc_pdf = resolve_by_europepmc(title)
    if epmc_pdf and download_file(epmc_pdf, dest_path):
        return paper_id, True, "Europe PMC OA"
        
    # 4. Try arXiv API Search
    arxiv_pdf = resolve_by_arxiv_api(title)
    if arxiv_pdf and download_file(arxiv_pdf, dest_path):
        return paper_id, True, "arXiv OA"
        
    return paper_id, False, "Requires browser portal / HTML reader"

def process_cluster_extra(kw_id):
    kw_dir = os.path.join(BASE_DIR, kw_id)
    csv_file = os.path.join(kw_dir, "papers_index.csv")
    pdfs_dir = os.path.join(kw_dir, "pdfs")
    os.makedirs(pdfs_dir, exist_ok=True)
    
    if not os.path.exists(csv_file):
        return 0, 0
        
    papers = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append(row)
            
    print(f"\n[{kw_id}] Deep resolving missing PDFs...")
    new_dl = 0
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_missing_paper_pdf, p, pdfs_dir): p for p in papers}
        for future in as_completed(futures):
            p_id, success, msg = future.result()
            if success:
                if msg != "Already exists":
                    new_dl += 1
                    print(f"  [OK-NEW] {p_id}: Downloaded ({msg})")
            else:
                print(f"  [--] {p_id}: {msg}")
                
    # Count total existing in folder
    total_local = len([f for f in os.listdir(pdfs_dir) if f.endswith(".pdf") and os.path.getsize(os.path.join(pdfs_dir, f)) > 10000])
    print(f"[{kw_id}] Total local PDFs now: {total_local}/{len(papers)}\n")
    return total_local, len(papers)

def main():
    print("=================================================================")
    print("DEEP RESOLUTION FOR OPEN ACCESS PAPERS (SEMANTIC SCHOLAR, PMC, ARXIV)")
    print("=================================================================")
    
    total_existing = 0
    total_all = 0
    
    for kw_id in KEYWORDS:
        t_loc, t_all = process_cluster_extra(kw_id)
        total_existing += t_loc
        total_all += t_all
        
    print("=================================================================")
    print(f"FINAL SUMMARY: {total_existing}/{total_all} Full-Text PDFs are locally stored in literature/open_access_repository!")
    print("=================================================================")

if __name__ == "__main__":
    main()
