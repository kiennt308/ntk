import os
import sys
import json
import urllib.request
import urllib.parse
import csv
import re
import hashlib
import ssl

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

BASE_DIR = r"d:\ntk\eeg_paper_research"
NB01_DIR = os.path.join(BASE_DIR, "notebooklm_workspace", "notebook_01_Multimodal_EEG_Biosignals")
PDF_DIR = os.path.join(NB01_DIR, "pdfs")
NOTES_DIR = os.path.join(NB01_DIR, "paper_notes")
CSV_PATH = os.path.join(NB01_DIR, "papers_index.csv")
META_PATH = os.path.join(NB01_DIR, "notebook_metadata.json")
INDEX_MD_PATH = os.path.join(NB01_DIR, "00_NOTEBOOKLM_PROMPTS_AND_INDEX.md")
README_PATH = os.path.join(NB01_DIR, "README.md")

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def normalize_title(t):
    return re.sub(r'[^a-z0-9]', '', (t or '').lower())

def is_valid_pdf(data):
    if not data or len(data) < 25000:
        return False
    return data.startswith(b"%PDF-") or b"%PDF-" in data[:1024]

def download_url_content(url):
    if not url:
        return None
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=CTX, timeout=25) as resp:
            content = resp.read()
            if is_valid_pdf(content):
                return content
    except Exception:
        pass
    return None

def collect_benchmark_existing():
    existing_titles = set()
    existing_dois = set()
    import glob
    # Notebook 01 original 50
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, encoding='utf-8', errors='ignore') as f:
            for i, r in enumerate(csv.DictReader(f)):
                if i < 50:
                    nt = normalize_title(r.get('title', ''))
                    if nt: existing_titles.add(nt)
                    doi = r.get('doi', '').strip().lower()
                    if doi: existing_dois.add(doi)
    # Other notebooks
    for nb in glob.glob(os.path.join(BASE_DIR, 'notebooklm_workspace', 'notebook_*')):
        if os.path.basename(nb) == "notebook_01_Multimodal_EEG_Biosignals":
            continue
        csv_file = os.path.join(nb, 'papers_index.csv')
        if os.path.exists(csv_file):
            with open(csv_file, encoding='utf-8', errors='ignore') as f:
                for r in csv.DictReader(f):
                    nt = normalize_title(r.get('title', ''))
                    if nt: existing_titles.add(nt)
                    doi = r.get('doi', '').strip().lower()
                    if doi: existing_dois.add(doi)
    return existing_titles, existing_dois

print("Loaded existing set...")
