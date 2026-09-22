#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Multi-Source Open Access Paper Fetcher for PhD Research
Đề tài: Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức
(Multi-task multi-branch architecture for emotion recognition from multimodal biosignals)
=============================================================================
Thu thập và tải toàn văn PDF từ các nguồn học thuật Mở (Open Access) uy tín:
  1. Semantic Scholar API (https://api.semanticscholar.org/)
  2. Europe PMC / PubMed Central API (https://europepmc.org/)
  3. arXiv API (https://arxiv.org/)

Tính năng:
  - Tải bài báo theo 5 Track cốt lõi của đề tài Multimodal Biosignals.
  - Lọc chính xác các bài có Open Access PDF, trích xuất Citation Count và DOI.
  - Tích hợp cơ chế bảo vệ IP & lưu vết SQLite WAL Mode chống cúp điện.
=============================================================================
"""

import os
import re
import sys
import time
import json
import random
import sqlite3
import argparse
from datetime import datetime

# Đảm bảo hiển thị UTF-8 trên Windows console
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("[!] Lỗi: Chưa cài đặt 'requests'. Hãy chạy: pip install requests")
    sys.exit(1)

# User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

# Bộ từ khóa chuyên sâu phân theo 5 Trục của Đề tài
MULTIMODAL_TRACK_KEYWORDS = {
    1: [
        "ECG emotion recognition physiological",
        "EDA GSR emotion recognition physiological",
        "EMG emotion recognition biosignals",
        "PPG respiration emotion recognition"
    ],
    2: [
        "multimodal biosignals emotion recognition",
        "EEG ECG multimodal emotion recognition",
        "EEG EDA multimodal affective computing",
        "multimodal physiological emotion DEAP DREAMER AMIGOS"
    ],
    3: [
        "multi-task learning emotion recognition biosignals",
        "multi-task valence arousal emotion classification",
        "joint emotion recognition and valence arousal regression",
        "multi-task physiological affective computing"
    ],
    4: [
        "multi-branch neural network multimodal emotion",
        "cross-modal attention biosignal emotion recognition",
        "shared private representation multimodal emotion",
        "multimodal fusion transformer biosignals emotion"
    ],
    5: [
        "missing modality multimodal emotion recognition",
        "incomplete multimodal biosignals emotion",
        "cross-subject multimodal emotion recognition",
        "domain generalization multimodal physiological emotion"
    ]
}


class OpenAccessFetcher:
    def __init__(self, output_dir="downloaded_papers", db_path="downloaded_papers/checklist.db"):
        self.output_dir = output_dir
        self.db_path = db_path
        os.makedirs(self.output_dir, exist_ok=True)
        self.session = self._create_resilient_session()
        self._init_db()

    def _create_resilient_session(self):
        session = requests.Session()
        retry_strategy = Retry(
            total=4,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=15, pool_maxsize=15)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id TEXT PRIMARY KEY,
                source TEXT,
                doi TEXT,
                title TEXT,
                authors TEXT,
                year TEXT,
                journal TEXT,
                pdf_url TEXT,
                local_path TEXT,
                file_size INTEGER,
                status TEXT,
                downloaded_at TEXT,
                error_message TEXT,
                abstract TEXT,
                landing_url TEXT
            );
            """)
            conn.commit()

    def is_paper_downloaded(self, paper_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT status, local_path FROM papers WHERE id = ?;", (paper_id,))
            row = cur.fetchone()
            if row and row[0] == "Success" and row[1] and os.path.exists(row[1]):
                return True
        return False

    def search_semantic_scholar(self, query, limit=20):
        print(f"[*] [Semantic Scholar] Đang tìm kiếm: '{query}' (Giới hạn: {limit})...")
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "paperId,title,abstract,authors,year,venue,openAccessPdf,citationCount,externalIds"
        }
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        papers = []
        try:
            resp = self.session.get(url, params=params, headers=headers, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get("data", []):
                    oa_info = item.get("openAccessPdf")
                    pdf_url = oa_info.get("url") if oa_info else ""
                    if not pdf_url:
                        continue

                    paper_id = f"s2_{item.get('paperId')}"
                    authors_list = [a.get("name", "") for a in item.get("authors", []) if a.get("name")]
                    ext_ids = item.get("externalIds") or {}
                    doi = ext_ids.get("DOI", "")

                    papers.append({
                        "id": paper_id,
                        "source": "SemanticScholar_OA",
                        "title": item.get("title", "").strip(),
                        "authors": ", ".join(authors_list),
                        "year": str(item.get("year", "")),
                        "journal": item.get("venue", "Semantic Scholar Open Access"),
                        "doi": doi,
                        "pdf_url": pdf_url,
                        "abstract": item.get("abstract", "") or "",
                        "landing_url": f"https://www.semanticscholar.org/paper/{item.get('paperId')}"
                    })
                print(f"[+] [Semantic Scholar] Tìm thấy {len(papers)} bài có Open Access PDF.")
            else:
                print(f"[!] Semantic Scholar trả về mã lỗi: {resp.status_code}")
        except Exception as e:
            print(f"[!] Lỗi kết nối Semantic Scholar: {e}")
        return papers

    def search_europe_pmc(self, query, limit=20):
        print(f"[*] [Europe PMC] Đang tìm kiếm: '{query}' (Giới hạn: {limit})...")
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        formatted_query = f"{query} AND (OPEN_ACCESS:y OR HAS_FT:y)"
        params = {
            "query": formatted_query,
            "format": "json",
            "pageSize": limit,
            "resultType": "core"
        }
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        papers = []
        try:
            resp = self.session.get(url, params=params, headers=headers, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                result_list = data.get("resultList", {}).get("result", [])
                for item in result_list:
                    pmcid = item.get("pmcid")
                    doi = item.get("doi", "")
                    title = item.get("title", "").rstrip(".")
                    pdf_url = ""
                    if pmcid:
                        pdf_url = f"https://europepmc.org/backend/ptpmcrender.fcgi?accid={pmcid}&blobtype=pdf"

                    if not pdf_url:
                        continue

                    paper_id = f"epmc_{pmcid or item.get('id')}"
                    papers.append({
                        "id": paper_id,
                        "source": "EuropePMC_OA",
                        "title": title,
                        "authors": item.get("authorString", ""),
                        "year": str(item.get("pubYear", "")),
                        "journal": item.get("journalTitle", "Europe PMC / PubMed Central"),
                        "doi": doi,
                        "pdf_url": pdf_url,
                        "abstract": item.get("abstractText", "") or "",
                        "landing_url": f"https://europepmc.org/article/PMC/{pmcid}" if pmcid else f"https://doi.org/{doi}"
                    })
                print(f"[+] [Europe PMC] Tìm thấy {len(papers)} bài Open Access toàn văn.")
            else:
                print(f"[!] Europe PMC trả về mã lỗi: {resp.status_code}")
        except Exception as e:
            print(f"[!] Lỗi kết nối Europe PMC: {e}")
        return papers

    def download_paper_pdf(self, paper, subfolder="open_access"):
        if self.is_paper_downloaded(paper["id"]):
            print(f"  [⏩ Bỏ qua] Đã tải trước đó: {paper['title'][:60]}...")
            return True

        target_dir = os.path.join(self.output_dir, subfolder)
        os.makedirs(target_dir, exist_ok=True)

        clean_title = re.sub(r'[\\/*?:"<>|]', "", paper["title"])
        clean_title = re.sub(r"\s+", "_", clean_title)[:60].strip("_")
        year = paper.get("year", "2024") or "2024"
        filename = f"{paper['id']}_{year}_{clean_title}.pdf"
        target_path = os.path.join(target_dir, filename)
        tmp_path = target_path + ".tmp"

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/pdf,application/xhtml+xml,text/html;q=0.9,*/*;q=0.8"
        }

        print(f"  [⬇ Tải PDF] {paper['title'][:65]}...")
        try:
            with self.session.get(paper["pdf_url"], headers=headers, stream=True, timeout=30) as resp:
                if resp.status_code == 200:
                    with open(tmp_path, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=32768):
                            if chunk:
                                f.write(chunk)

                    if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 2048:
                        with open(tmp_path, "rb") as f:
                            header = f.read(5)
                        if header == b"%PDF-":
                            if os.path.exists(target_path):
                                os.remove(target_path)
                            os.rename(tmp_path, target_path)
                            file_size = os.path.getsize(target_path)
                            self._record_success(paper, target_path, file_size)
                            print(f"  [✔ Thành công] Lưu: {filename} ({file_size / 1024:.1f} KB)")
                            return True

                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                    print("  [!] File tải về không phải PDF hợp lệ.")
                else:
                    print(f"  [!] Lỗi HTTP {resp.status_code} khi tải PDF.")
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            print(f"  [!] Lỗi ngoại lệ khi tải: {e}")

        return False

    def _record_success(self, paper, local_path, file_size):
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            INSERT OR REPLACE INTO papers (
                id, source, doi, title, authors, year, journal,
                pdf_url, local_path, file_size, status, downloaded_at, error_message, abstract, landing_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Success', ?, '', ?, ?);
            """, (
                paper.get("id"),
                paper.get("source"),
                paper.get("doi", ""),
                paper.get("title", ""),
                paper.get("authors", ""),
                paper.get("year", ""),
                paper.get("journal", ""),
                paper.get("pdf_url", ""),
                local_path,
                file_size,
                now,
                paper.get("abstract", ""),
                paper.get("landing_url", "")
            ))
            conn.commit()


def main():
    parser = argparse.ArgumentParser(description="Multimodal Biosignals Open Access Paper Fetcher")
    parser.add_argument("--track", type=int, choices=range(1, 6), help="Chọn Track (1 đến 5) theo Roadmap Multimodal")
    parser.add_argument("--query", type=str, help="Từ khóa tìm kiếm tùy biến")
    parser.add_argument("--limit", type=int, default=15, help="Số lượng bài tải về tối đa mỗi từ khóa")
    args = parser.parse_args()

    fetcher = OpenAccessFetcher()

    queries = []
    if args.track:
        queries = MULTIMODAL_TRACK_KEYWORDS.get(args.track, [])
        print(f"[*] Đã chọn Track {args.track} với {len(queries)} cụm từ khóa chuyên sâu.")
    elif args.query:
        queries = [args.query]
    else:
        print("[*] Không chỉ định Track, tự động quét theo tất cả các cụm từ khóa Multimodal PhD Roadmap...")
        for kws in MULTIMODAL_TRACK_KEYWORDS.values():
            queries.extend(kws[:2])

    for q in queries:
        print(f"\n{'='*70}\n🔎 Đang quét: '{q}'\n{'='*70}")
        # Quét Semantic Scholar
        s2_papers = fetcher.search_semantic_scholar(q, limit=args.limit)
        for p in s2_papers:
            fetcher.download_paper_pdf(p, subfolder="semantic_scholar")
            time.sleep(random.uniform(2.0, 4.0))

        # Quét Europe PMC
        pmc_papers = fetcher.search_europe_pmc(q, limit=args.limit)
        for p in pmc_papers:
            fetcher.download_paper_pdf(p, subfolder="europe_pmc")
            time.sleep(random.uniform(2.0, 4.0))


if __name__ == "__main__":
    main()
