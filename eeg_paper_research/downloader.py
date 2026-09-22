#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
EEG Paper Downloader (arXiv & Frontiers in...) - CONTINUOUS & RESILIENT EDITION
Tự động tìm kiếm và tải các bài báo khoa học về EEG & Nhận diện cảm xúc
Trang hỗ trợ:
  1. arXiv (https://arxiv.org/)
  2. Frontiers (https://www.frontiersin.org/)

Tính năng đặc biệt:
  - CHẠY LIÊN TỤC (Continuous Mode): Lặp tuần hoàn, tự động quét sâu dần qua
    từng trang kết quả, nghỉ giãn cách giữa các chu kỳ để bảo vệ IP.
  - CHECKLIST BẢO VỆ DỮ LIỆU KHI CÚP ĐIỆN (Crash-Proof SQLite WAL):
    Lưu vết từng bài báo ngay khi tải xong bằng SQLite chế độ Write-Ahead-Logging (WAL).
    Nếu máy tính tắt đột ngột, cúp điện, không bao giờ mất checklist, không tải trùng,
    và tự động tiếp tục (resume) đúng vị trí trang trước đó.
  - GIÃN CÁCH NHIỀU CẤP ĐỘ (Multi-Tier Anti-Bot Delays):
    + Giãn cách giữa 2 bài báo (3s - 7s ngẫu nhiên)
    + Nghỉ giải lao mô phỏng người thật (15s - 25s sau mỗi 8-12 bài)
    + Giãn cách giữa các chu kỳ quét (5 - 15 phút đếm ngược hiển thị sinh động)
  - XUẤT BẢNG METADATA EXCEL (CSV UTF-8 BOM) & JSON
=============================================================================
"""

import os
import re
import sys
import time
import json
import random
import csv
import signal
import sqlite3
import argparse
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
from datetime import datetime

# Đảm bảo in tiếng Việt và ký tự đặc biệt mượt mà trên Windows console (cmd/powershell)
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
    print("[!] Lỗi: Chưa cài đặt thư viện 'requests'. Hãy chạy: pip install requests")
    sys.exit(1)

try:
    from tqdm import tqdm
except ImportError:
    class tqdm:
        def __init__(self, iterable=None, total=None, desc="", unit="", unit_scale=False, leave=True):
            self.iterable = iterable
            self.total = total
            self.desc = desc
            self.n = 0

        def update(self, n=1):
            self.n += n

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass


# =============================================================================
# CẤU HÌNH USER-AGENTS & BROWSER HEADERS (ANTI-BOT)
# =============================================================================
REALISTIC_USER_AGENTS = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    # Chrome on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # Safari on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
]

# Danh mục từ khóa tìm kiếm phong phú về EEG + Nhận diện cảm xúc
DEFAULT_KEYWORD_GROUPS = [
    "EEG emotion recognition",
    "EEG emotion classification",
    "EEG affective computing",
    "electroencephalogram emotion recognition",
    "EEG emotional state estimation",
    "EEG valence arousal emotion",
    "EEG sentiment analysis deep learning"
]


# =============================================================================
# CHECKLIST DATABASE (SQLITE WITH WAL MODE - CHỐNG CÚP ĐIỆN)
# =============================================================================
class ChecklistDB:
    """
    Checklist lưu trữ bằng SQLite với chế độ Write-Ahead Logging (WAL).
    Đảm bảo 100% tính toàn vẹn dữ liệu khi máy tính bị cúp điện, khởi động lại
    hoặc tắt ngang đột ngột.
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            # WAL mode giúp chống hỏng database khi tắt nguồn đột ngột
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA synchronous = NORMAL;")

            # Bảng lưu trữ checklist bài báo
            conn.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                doi TEXT,
                title TEXT,
                authors TEXT,
                year TEXT,
                journal TEXT,
                pdf_url TEXT,
                local_path TEXT,
                file_size INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                downloaded_at TEXT,
                error_message TEXT,
                abstract TEXT,
                landing_url TEXT
            );
            """)

            # Bảng lưu trữ vị trí offset quét (cursor) để khi bật lại tiếp tục quét sâu hơn
            conn.execute("""
            CREATE TABLE IF NOT EXISTS crawl_state (
                source TEXT PRIMARY KEY,
                keyword_index INTEGER DEFAULT 0,
                offset INTEGER DEFAULT 0,
                total_downloaded INTEGER DEFAULT 0,
                last_updated TEXT
            );
            """)
            conn.commit()

    def is_downloaded(self, paper_id):
        """Kiểm tra bài báo đã có trong checklist thành công chưa."""
        if not paper_id:
            return False
        with self._get_connection() as conn:
            cur = conn.execute(
                "SELECT 1 FROM papers WHERE id = ? AND status = 'Success' LIMIT 1;",
                (paper_id,)
            )
            return cur.fetchone() is not None

    def record_success(self, paper, local_path, file_size):
        """Ghi nhận bài báo tải thành công vào SQLite ngay lập tức (Commit tức thì)."""
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
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

    def record_failure(self, paper, error_msg):
        """Ghi nhận bài báo bị lỗi."""
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO papers (
                id, source, doi, title, authors, year, journal,
                pdf_url, local_path, file_size, status, downloaded_at, error_message, abstract, landing_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, '', 0, 'Failed', ?, ?, ?, ?);
            """, (
                paper.get("id"),
                paper.get("source"),
                paper.get("doi", ""),
                paper.get("title", ""),
                paper.get("authors", ""),
                paper.get("year", ""),
                paper.get("journal", ""),
                paper.get("pdf_url", ""),
                now,
                error_msg,
                paper.get("abstract", ""),
                paper.get("landing_url", "")
            ))
            conn.commit()

    def get_crawl_state(self, source):
        """Lấy vị trí quét trang gần nhất để tiếp tục sau cúp điện."""
        with self._get_connection() as conn:
            cur = conn.execute(
                "SELECT keyword_index, offset, total_downloaded FROM crawl_state WHERE source = ?;",
                (source,)
            )
            row = cur.fetchone()
            if row:
                return dict(row)
            return {"keyword_index": 0, "offset": 0, "total_downloaded": 0}

    def update_crawl_state(self, source, keyword_index, offset, downloaded_delta=0):
        """Cập nhật vị trí trang quét đã duyệt tới."""
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            state = self.get_crawl_state(source)
            new_total = state["total_downloaded"] + downloaded_delta
            conn.execute("""
            INSERT OR REPLACE INTO crawl_state (source, keyword_index, offset, total_downloaded, last_updated)
            VALUES (?, ?, ?, ?, ?);
            """, (source, keyword_index, offset, new_total, now))
            conn.commit()

    def get_all_success_papers(self):
        """Lấy tất cả các bài thành công để đồng bộ ra CSV/JSON."""
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM papers WHERE status = 'Success' ORDER BY downloaded_at DESC;")
            return [dict(row) for row in cur.fetchall()]

    def get_stats(self):
        """Thống kê số lượng bài trong checklist."""
        with self._get_connection() as conn:
            cur1 = conn.execute("SELECT COUNT(*) FROM papers WHERE status = 'Success';")
            success_count = cur1.fetchone()[0]
            cur2 = conn.execute("SELECT COUNT(*) FROM papers WHERE status = 'Failed';")
            failed_count = cur2.fetchone()[0]
            cur3 = conn.execute("SELECT source, COUNT(*) FROM papers WHERE status = 'Success' GROUP BY source;")
            by_source = dict(cur3.fetchall())
            return {
                "success": success_count,
                "failed": failed_count,
                "by_source": by_source
            }


# =============================================================================
# HTTP SESSION QUẢN LÝ CHỐNG CHẶN (ANTI-BOT)
# =============================================================================
class AntiBotSession:
    """Quản lý HTTP session thông minh với hành vi giả lập người dùng thật."""

    def __init__(self, min_delay=3.0, max_delay=6.5):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.session = requests.Session()
        self.request_count = 0
        self.next_rest_at = random.randint(8, 14)

        # Cấu hình retry adapter cho lỗi mạng tạm thời
        retries = Retry(
            total=3,
            backoff_factor=1.5,
            status_forcelist=[500, 502, 503, 504],
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get_realistic_headers(self, referer=None):
        ua = random.choice(REALISTIC_USER_AGENTS)
        headers = {
            "User-Agent": ua,
            "Accept": "application/pdf,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
        }
        if referer:
            headers["Referer"] = referer
        return headers

    def random_sleep(self, custom_min=None, custom_max=None):
        """Tạo khoảng nghỉ ngẫu nhiên tránh tần suất robot đều đặn."""
        low = custom_min if custom_min is not None else self.min_delay
        high = custom_max if custom_max is not None else self.max_delay
        sleep_time = random.uniform(low, high)
        time.sleep(sleep_time)

    def check_rest_break(self):
        """Cứ sau một số bài, tạm nghỉ lâu hơn (15-25s) giống con người đọc bài."""
        self.request_count += 1
        if self.request_count >= self.next_rest_at:
            pause_time = random.uniform(15.0, 25.0)
            print(f"\n[*] [Human Simulation] Tạm nghỉ {pause_time:.1f}s để mô phỏng hành vi đọc tài liệu...")
            time.sleep(pause_time)
            self.next_rest_at = self.request_count + random.randint(8, 14)

    def safe_get(self, url, headers=None, stream=False, timeout=30, referer=None, max_attempts=4):
        """Gửi GET request với cơ chế thử lại lũy thừa (exponential backoff) nếu dính 429."""
        attempt = 0
        while attempt < max_attempts:
            req_headers = self.get_realistic_headers(referer=referer)
            if headers:
                req_headers.update(headers)

            try:
                self.check_rest_break()
                response = self.session.get(url, headers=req_headers, stream=stream, timeout=timeout)

                # Trường hợp bị rate limit 429
                if response.status_code == 429:
                    attempt += 1
                    retry_after = response.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        wait_seconds = int(retry_after) + random.uniform(3, 8)
                    else:
                        wait_seconds = (2 ** attempt) * 20 + random.uniform(5, 12)
                    print(f"\n[!] Gặp mã 429 (Rate Limit). Tạm dừng {wait_seconds:.1f}s trước khi thử lại ({attempt}/{max_attempts})...")
                    time.sleep(wait_seconds)
                    continue

                return response

            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                attempt += 1
                wait_seconds = (2 ** attempt) * 4 + random.uniform(2, 5)
                print(f"\n[!] Lỗi kết nối ({e}). Chờ {wait_seconds:.1f}s trước khi thử lại ({attempt}/{max_attempts})...")
                time.sleep(wait_seconds)

        return None


# =============================================================================
# CRAWLER: ARXIV (HỖ TRỢ OFFSET PHÂN TRANG)
# =============================================================================
class ArxivCrawler:
    """Thu thập thông tin bài báo từ arXiv qua Atom API chính thức."""

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self, session: AntiBotSession):
        self.session = session

    def fetch_batch(self, keywords, start=0, count=15):
        """Tìm nạp một đợt bài báo từ vị trí start."""
        papers = []
        if isinstance(keywords, list) and keywords:
            clean_terms = [f'all:"{k.replace("EEG", "").strip()}"' for k in keywords if k.strip()]
            query_str = f'all:EEG AND ({" OR ".join(clean_terms)})'
        elif isinstance(keywords, str) and keywords.strip():
            query_str = f'all:"{keywords.strip()}"'
        else:
            query_str = 'all:EEG AND (all:"emotion recognition" OR all:"emotion classification" OR all:"affective computing")'

        params = f"?search_query={quote_plus(query_str)}&start={start}&max_results={count}&sortBy=relevance&sortOrder=descending"
        req_url = self.BASE_URL + params

        resp = self.session.safe_get(req_url, timeout=25)
        if not resp or resp.status_code != 200:
            print(f"[!] Lỗi truy vấn arXiv (Status: {resp.status_code if resp else 'None'})")
            return papers, 0

        try:
            root = ET.fromstring(resp.content)
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "arxiv": "http://arxiv.org/schemas/atom"
            }

            entries = root.findall("atom:entry", ns)
            for entry in entries:
                paper_id = entry.find("atom:id", ns).text.strip().split("/abs/")[-1]
                title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
                title = re.sub(r"\s+", " ", title)

                summary = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
                summary = re.sub(r"\s+", " ", summary)

                published = entry.find("atom:published", ns).text.strip()
                year = published[:4] if published else "Unknown"

                authors = []
                for author in entry.findall("atom:author", ns):
                    name_elem = author.find("atom:name", ns)
                    if name_elem is not None and name_elem.text:
                        authors.append(name_elem.text.strip())

                pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
                for link in entry.findall("atom:link", ns):
                    if link.attrib.get("title") == "pdf":
                        pdf_url = link.attrib.get("href")
                        break

                paper_info = {
                    "source": "arXiv",
                    "id": paper_id,
                    "doi": f"10.48550/arXiv.{paper_id}",
                    "title": title,
                    "authors": "; ".join(authors),
                    "year": year,
                    "journal": "arXiv",
                    "abstract": summary,
                    "pdf_url": pdf_url,
                    "landing_url": f"https://arxiv.org/abs/{paper_id}"
                }
                papers.append(paper_info)

            return papers, len(entries)

        except Exception as e:
            print(f"[!] Lỗi khi parse dữ liệu arXiv XML: {e}")
            return papers, 0


# =============================================================================
# CRAWLER: FRONTIERS (HỖ TRỢ OFFSET PHÂN TRANG)
# =============================================================================
class FrontiersCrawler:
    """Thu thập thông tin bài báo từ Frontiers qua Crossref Open Access API."""

    CROSSREF_BASE = "https://api.crossref.org/prefixes/10.3389/works"

    def __init__(self, session: AntiBotSession):
        self.session = session

    def fetch_batch(self, query="EEG emotion recognition", offset=0, count=15):
        """Tìm nạp một đợt bài báo từ vị trí offset."""
        papers = []
        url = f"{self.CROSSREF_BASE}?query={quote_plus(query)}&rows={count}&offset={offset}"

        custom_header = {"User-Agent": "AcademicResearcherBot/2.0 (mailto:academic.research@frontiers-reader.org)"}
        resp = self.session.safe_get(url, headers=custom_header, timeout=25)

        if not resp or resp.status_code != 200:
            print(f"[!] Lỗi truy vấn Frontiers qua Crossref (Status: {resp.status_code if resp else 'None'})")
            return papers, 0

        try:
            data = resp.json()
            items = data.get("message", {}).get("items", [])
            for it in items:
                doi = it.get("DOI")
                if not doi or not doi.startswith("10.3389/"):
                    continue

                title_list = it.get("title", [])
                title = title_list[0].strip() if title_list else "Untitled Article"
                title = re.sub(r"\s+", " ", title)

                authors = []
                for a in it.get("author", []):
                    given = a.get("given", "")
                    family = a.get("family", "")
                    name = f"{given} {family}".strip()
                    if name:
                        authors.append(name)

                year = "Unknown"
                date_parts = it.get("created", {}).get("date-parts", [[]])[0]
                if date_parts:
                    year = str(date_parts[0])

                container_title = it.get("container-title", ["Frontiers"])[0] if it.get("container-title") else "Frontiers"

                abstract = it.get("abstract", "")
                if abstract:
                    abstract = re.sub(r"<[^>]+>", "", abstract).strip()

                pdf_url = f"https://www.frontiersin.org/articles/{doi}/pdf"
                landing_url = f"https://doi.org/{doi}"

                paper_info = {
                    "source": "Frontiers",
                    "id": doi,
                    "doi": doi,
                    "journal": container_title,
                    "title": title,
                    "authors": "; ".join(authors),
                    "year": year,
                    "abstract": abstract,
                    "pdf_url": pdf_url,
                    "landing_url": landing_url
                }
                papers.append(paper_info)

            return papers, len(items)

        except Exception as e:
            print(f"[!] Lỗi khi parse dữ liệu Frontiers: {e}")
            return papers, 0


# =============================================================================
# QUẢN LÝ TẢI FILE & ĐỒNG BỘ CHECKLIST
# =============================================================================
class PaperDownloader:
    """Điều phối tải file PDF, chống cúp điện, đồng bộ checklist SQLite & Excel CSV."""

    def __init__(self, output_dir="./downloaded_papers", min_delay=3.0, max_delay=6.5):
        self.output_dir = os.path.abspath(output_dir)
        self.arxiv_dir = os.path.join(self.output_dir, "arxiv")
        self.frontiers_dir = os.path.join(self.output_dir, "frontiers")
        self.csv_path = os.path.join(self.output_dir, "papers_metadata.csv")
        self.json_path = os.path.join(self.output_dir, "papers_metadata.json")
        self.db_path = os.path.join(self.output_dir, "checklist.db")

        os.makedirs(self.arxiv_dir, exist_ok=True)
        os.makedirs(self.frontiers_dir, exist_ok=True)

        self.db = ChecklistDB(self.db_path)
        self.session = AntiBotSession(min_delay=min_delay, max_delay=max_delay)

        # 1. Dọn dẹp các file .tmp dở dang do cúp điện từ phiên trước
        self.cleanup_leftover_tmp()

        # 2. Quét thư mục đĩa và đồng bộ toàn bộ file đã tải vào SQLite Checklist
        self.sync_existing_files_to_db()

    def cleanup_leftover_tmp(self):
        """Xóa các file .tmp bị bỏ dở khi máy tính bị mất điện đột ngột."""
        cleaned = 0
        for folder in [self.arxiv_dir, self.frontiers_dir]:
            if not os.path.exists(folder):
                continue
            for fname in os.listdir(folder):
                if fname.endswith(".tmp"):
                    try:
                        os.remove(os.path.join(folder, fname))
                        cleaned += 1
                    except Exception:
                        pass
        if cleaned > 0:
            print(f"[*] [Recovery] Đã dọn dẹp {cleaned} file tạm (.tmp) bị dở dang từ phiên trước.")

    def sync_existing_files_to_db(self):
        """
        Đọc các file PDF đã tồn tại trên đĩa hoặc từ papers_metadata.json cũ
        để nạp vào SQLite Checklist, đảm bảo không bao giờ tải lại.
        """
        synced = 0
        # Nạp từ JSON cũ nếu có
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    old_items = json.load(f)
                    for item in old_items:
                        pid = item.get("id") or item.get("doi")
                        if pid and not self.db.is_downloaded(pid):
                            lpath = item.get("local_path", "")
                            if lpath and self.is_valid_pdf(lpath):
                                fsize = os.path.getsize(lpath)
                                self.db.record_success(item, lpath, fsize)
                                synced += 1
            except Exception:
                pass

        # Quét trực tiếp các file PDF trong thư mục
        for folder, source in [(self.arxiv_dir, "arXiv"), (self.frontiers_dir, "Frontiers")]:
            for fname in os.listdir(folder):
                if fname.endswith(".pdf"):
                    fpath = os.path.join(folder, fname)
                    if self.is_valid_pdf(fpath):
                        # Lấy ID từ tên file
                        # [Source]_Year_Title_ID.pdf
                        parts = fname[:-4].split("_")
                        extracted_id = parts[-1] if parts else fname
                        if not self.db.is_downloaded(extracted_id):
                            item = {
                                "id": extracted_id,
                                "source": source,
                                "doi": extracted_id if "/" in extracted_id else "",
                                "title": fname[:-4],
                                "authors": "",
                                "year": "",
                                "journal": source,
                                "pdf_url": "",
                                "abstract": "",
                                "landing_url": ""
                            }
                            self.db.record_success(item, fpath, os.path.getsize(fpath))
                            synced += 1

        if synced > 0:
            print(f"[*] [Checklist] Đã đồng bộ {synced} bài báo có sẵn vào SQLite Checklist an toàn.")
            self.export_csv_and_json()

    @staticmethod
    def sanitize_filename(name, max_length=110):
        """Làm sạch tên file, loại bỏ ký tự cấm trên Windows/Linux/Mac."""
        clean = re.sub(r'[\\/*?:"<>|]', "", name)
        clean = re.sub(r"\s+", "_", clean).strip("._-")
        if len(clean) > max_length:
            clean = clean[:max_length]
        return clean

    def is_valid_pdf(self, filepath):
        """Kiểm tra file có phải PDF hợp lệ hay không (phát hiện byte %PDF-)."""
        if not os.path.exists(filepath):
            return False
        if os.path.getsize(filepath) < 10240:  # Nhỏ hơn 10KB thường là trang lỗi HTML
            return False
        try:
            with open(filepath, "rb") as f:
                header = f.read(1024)
                return b"%PDF-" in header
        except Exception:
            return False

    def export_csv_and_json(self):
        """Xuất danh mục bài báo ra CSV (mở Excel không lỗi font) và JSON."""
        papers = self.db.get_all_success_papers()

        # Ghi JSON
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)

        # Ghi CSV UTF-8 BOM
        fieldnames = [
            "source", "id", "doi", "year", "title", "authors",
            "journal", "file_size", "downloaded_at", "local_path", "pdf_url", "abstract"
        ]
        with open(self.csv_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for p in papers:
                writer.writerow(p)

    def download_one_paper(self, paper):
        """Tải một bài báo, ghi nhận checklist SQLite và xử lý chống cúp điện."""
        paper_id = paper.get("id")
        source = paper.get("source", "").lower()
        target_dir = self.arxiv_dir if source == "arxiv" else self.frontiers_dir

        safe_title = self.sanitize_filename(paper.get("title", "paper"))
        paper_id_clean = self.sanitize_filename(paper_id)
        year = paper.get("year", "XXXX")
        filename = f"[{paper['source']}]_{year}_{safe_title}_{paper_id_clean}.pdf"
        local_path = os.path.join(target_dir, filename)

        # 1. Kiểm tra trong SQLite Checklist
        if self.db.is_downloaded(paper_id):
            # Nếu trong DB đã có và file trên đĩa vẫn còn nguyên -> Bỏ qua ngay
            if self.is_valid_pdf(local_path):
                return "EXISTING"

        # 2. Kiểm tra trên đĩa
        if self.is_valid_pdf(local_path):
            self.db.record_success(paper, local_path, os.path.getsize(local_path))
            return "EXISTING"

        pdf_url = paper.get("pdf_url")
        referer = paper.get("landing_url")

        print(f"\n[↓] Đang tải: {paper.get('title')[:68]}...")
        print(f"    Nguồn: {paper['source']} | ID: {paper_id}")

        resp = self.session.safe_get(pdf_url, stream=True, timeout=45, referer=referer)
        if not resp or resp.status_code != 200:
            status_code = resp.status_code if resp else "Connection Error"
            print(f"[!] Thất bại khi tải PDF (HTTP {status_code})")
            self.db.record_failure(paper, f"HTTP {status_code}")
            return "FAILED"

        # Kiểm tra content-type
        content_type = resp.headers.get("Content-Type", "").lower()
        if "text/html" in content_type:
            print(f"[!] Máy chủ trả về HTML thay vì PDF (có thể dính trang xác minh bot).")
            self.db.record_failure(paper, "HTML Response")
            return "FAILED"

        total_size = int(resp.headers.get("content-length", 0))
        temp_path = local_path + ".tmp"

        try:
            with open(temp_path, "wb") as f, tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc=filename[:30],
                leave=False
            ) as bar:
                for chunk in resp.iter_content(chunk_size=16384):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

            # Xác thực file PDF
            if self.is_valid_pdf(temp_path):
                if os.path.exists(local_path):
                    os.remove(local_path)
                os.rename(temp_path, local_path)
                file_size = os.path.getsize(local_path)
                file_size_mb = file_size / (1024 * 1024)

                # CẬP NHẬT NGAY VÀO SQLITE CHECKLIST (Bảo vệ cúp điện)
                self.db.record_success(paper, local_path, file_size)
                print(f"[✓] Tải thành công: {filename} ({file_size_mb:.2f} MB)")
                return "SUCCESS"
            else:
                print(f"[!] File không hợp lệ (không chứa header %PDF-). Đã dọn dẹp file tạm.")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                self.db.record_failure(paper, "Corrupted PDF Header")
                return "FAILED"

        except Exception as e:
            print(f"[!] Lỗi trong quá trình lưu file: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            self.db.record_failure(paper, str(e))
            return "FAILED"
        finally:
            self.session.random_sleep()


# =============================================================================
# BỘ ĐIỀU KHIỂN VÒNG LẶP LIÊN TỤC (CONTINUOUS LOOP ORCHESTRATOR)
# =============================================================================
class ContinuousOrchestrator:
    """Quản lý các chu kỳ cào liên tục, tự động tăng offset, giãn cách và bắt Ctrl+C."""

    def __init__(self, downloader: PaperDownloader, sources="all", keywords=None,
                 batch_size=15, cycle_interval=600, dry_run=False):
        self.downloader = downloader
        self.sources = sources
        self.keywords = keywords or DEFAULT_KEYWORD_GROUPS
        self.batch_size = batch_size
        self.cycle_interval = cycle_interval
        self.dry_run = dry_run
        self.stop_requested = False

        # Bắt tín hiệu Ctrl+C để dừng nhẹ nhàng, lưu checkpoint an toàn
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        print("\n\n[!] Nhận tín hiệu dừng từ người dùng (Ctrl+C). Đang lưu lại Checklist an toàn...")
        self.stop_requested = True

    def countdown_timer(self, seconds):
        """Đếm ngược thời gian giãn cách giữa các chu kỳ với giao diện trực quan."""
        print(f"\n[*] [Chu kỳ Giãn Cách] Sẽ nghỉ {seconds // 60} phút {seconds % 60}s trước khi quét chu kỳ tiếp theo...")
        end_time = time.time() + seconds
        try:
            while time.time() < end_time:
                if self.stop_requested:
                    break
                remaining = int(end_time - time.time())
                mins, secs = divmod(remaining, 60)
                sys.stdout.write(f"\r[⏳] Chu kỳ tiếp theo sau: {mins:02d}:{secs:02d} (Nhấn Ctrl+C để dừng an toàn)... ")
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write("\r" + " " * 80 + "\r")
        except KeyboardInterrupt:
            self.stop_requested = True

    def run_one_cycle(self, cycle_num):
        """Thực hiện một chu kỳ cào (fetch batch arXiv + Frontiers)."""
        print(f"\n{'='*75}")
        print(f"         CHU KỲ CÀO THỨ #{cycle_num} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*75}")

        new_downloads = 0
        total_examined = 0

        # 1. Quét arXiv
        if self.sources in ["arxiv", "all"] and not self.stop_requested:
            arxiv_state = self.downloader.db.get_crawl_state("arXiv")
            arxiv_offset = arxiv_state["offset"]
            print(f"\n>>> [1/2] Quét arXiv từ vị trí offset = {arxiv_offset} (Số lượng cần nạp: {self.batch_size})...")

            arxiv_crawler = ArxivCrawler(self.downloader.session)
            papers, fetched_count = arxiv_crawler.fetch_batch(
                keywords=self.keywords,
                start=arxiv_offset,
                count=self.batch_size
            )

            print(f"    Tìm thấy {len(papers)} bài báo từ arXiv.")
            total_examined += len(papers)

            for p in papers:
                if self.stop_requested:
                    break
                if self.dry_run:
                    print(f"    [DRY-RUN arXiv] {p['title'][:60]} ({p['id']})")
                else:
                    res = self.downloader.download_one_paper(p)
                    if res == "SUCCESS":
                        new_downloads += 1
                    elif res == "EXISTING":
                        print(f"    [=] Đã có trong checklist: {p['title'][:55]}...")

            # Cập nhật offset mới vào SQLite checkpoint
            new_offset = arxiv_offset + fetched_count
            self.downloader.db.update_crawl_state("arXiv", 0, new_offset, downloaded_delta=new_downloads)
            self.downloader.session.random_sleep(4.0, 7.0)

        # 2. Quét Frontiers
        if self.sources in ["frontiers", "all"] and not self.stop_requested:
            frontiers_state = self.downloader.db.get_crawl_state("Frontiers")
            frontiers_offset = frontiers_state["offset"]
            print(f"\n>>> [2/2] Quét Frontiers từ vị trí offset = {frontiers_offset} (Số lượng cần nạp: {self.batch_size})...")

            frontiers_crawler = FrontiersCrawler(self.downloader.session)
            papers, fetched_count = frontiers_crawler.fetch_batch(
                query="EEG emotion recognition",
                offset=frontiers_offset,
                count=self.batch_size
            )

            print(f"    Tìm thấy {len(papers)} bài báo từ Frontiers.")
            total_examined += len(papers)

            frontiers_new = 0
            for p in papers:
                if self.stop_requested:
                    break
                if self.dry_run:
                    print(f"    [DRY-RUN Frontiers] {p['title'][:60]} ({p['id']})")
                else:
                    res = self.downloader.download_one_paper(p)
                    if res == "SUCCESS":
                        new_downloads += 1
                        frontiers_new += 1
                    elif res == "EXISTING":
                        print(f"    [=] Đã có trong checklist: {p['title'][:55]}...")

            # Cập nhật offset mới vào SQLite checkpoint
            new_offset = frontiers_offset + fetched_count
            self.downloader.db.update_crawl_state("Frontiers", 0, new_offset, downloaded_delta=frontiers_new)

        # Đồng bộ ra file CSV & JSON sau mỗi chu kỳ
        self.downloader.export_csv_and_json()

        # In thống kê chu kỳ
        stats = self.downloader.db.get_stats()
        print(f"\n[+] Kết thúc Chu kỳ #{cycle_num}:")
        print(f"    - Bài mới tải được trong chu kỳ: {new_downloads}")
        print(f"    - Tổng số bài trong Checklist hiện tại: {stats['success']} bài (arXiv: {stats['by_source'].get('arXiv', 0)}, Frontiers: {stats['by_source'].get('Frontiers', 0)})")
        print(f"    - Danh mục Excel đã lưu tại: {self.downloader.csv_path}")

        return new_downloads, total_examined

    def start_loop(self):
        """Bắt đầu chạy liên tục với thời gian giãn cách bảo vệ máy chủ."""
        cycle_num = 1
        while not self.stop_requested:
            new_downloads, total_examined = self.run_one_cycle(cycle_num)

            if self.stop_requested:
                break

            # Nếu không tìm thấy thêm bài nào từ cả 2 nguồn
            if total_examined == 0:
                print("\n[*] Cả hai nguồn tạm thời không còn bài báo mới phù hợp.")
                print(f"[*] Sẽ tạm nghỉ {self.cycle_interval}s trước khi thử kiểm tra lại các bài mới xuất bản...")

            # Đếm ngược thời gian nghỉ giữa các chu kỳ
            self.countdown_timer(self.cycle_interval)
            cycle_num += 1

        print("\n" + "=" * 75)
        print("          ĐÃ DỪNG CHƯƠNG TRÌNH AN TOÀN THEO YÊU CẦU")
        print("=" * 75)
        stats = self.downloader.db.get_stats()
        print(f"[✓] Tổng số bài báo đã tải thành công : {stats['success']} bài")
        print(f"[📁] Thư mục chứa PDF                 : {self.downloader.output_dir}")
        print(f"[📊] File Checklist Excel (CSV UTF-8) : {self.downloader.csv_path}")
        print(f"[🛡️] File SQLite Database an toàn      : {self.downloader.db_path}")
        print("=" * 75)


# =============================================================================
# HÀM MAIN VÀ XỬ LÝ DÒNG LỆNH (CLI)
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Tool tự động chạy liên tục, tải bài báo EEG + Cảm xúc, trang bị Checklist chống cúp điện."
    )
    parser.add_argument(
        "--continuous", "-c",
        action="store_true",
        help="Chế độ chạy liên tục tuần hoàn theo chu kỳ (mặc định lặp lại vô tận với thời gian nghỉ giãn cách)."
    )
    parser.add_argument(
        "--cycle-interval",
        type=int,
        default=600,
        help="Thời gian nghỉ giữa các chu kỳ chạy liên tục (giây, mặc định: 600s = 10 phút)."
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=15,
        help="Số lượng bài báo nạp cho mỗi nguồn trong mỗi chu kỳ (Mặc định: 15)."
    )
    parser.add_argument(
        "--sources",
        choices=["arxiv", "frontiers", "all"],
        default="all",
        help="Nguồn cần tải: 'arxiv', 'frontiers', hoặc 'all' (Mặc định: all)."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Giới hạn tải tối đa nếu chạy 1 lần (0 = dùng batch-size và chạy theo chu kỳ)."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./downloaded_papers",
        help="Thư mục lưu bài báo, SQLite checklist và metadata CSV (Mặc định: ./downloaded_papers)."
    )
    parser.add_argument(
        "--min-delay",
        type=float,
        default=3.0,
        help="Thời gian nghỉ tối thiểu giữa 2 bài báo (giây, mặc định: 3.0s)."
    )
    parser.add_argument(
        "--max-delay",
        type=float,
        default=7.0,
        help="Thời gian nghỉ tối đa giữa 2 bài báo (giây, mặc định: 7.0s)."
    )
    parser.add_argument(
        "--keywords",
        type=str,
        default="",
        help="Từ khóa tùy chỉnh (phân cách bằng dấu phẩy). Bỏ trống để dùng bộ từ khóa tối ưu."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Chỉ kiểm tra và xuất danh sách, không tải file PDF."
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Chỉ hiển thị thống kê checklist hiện tại và vị trí con trỏ (offset) rồi thoát."
    )

    args = parser.parse_args()

    # Khởi tạo Downloader và Checklist
    downloader = PaperDownloader(
        output_dir=args.output,
        min_delay=args.min_delay,
        max_delay=args.max_delay
    )

    # Chế độ xem trạng thái Checklist
    if args.status:
        stats = downloader.db.get_stats()
        arxiv_state = downloader.db.get_crawl_state("arXiv")
        frontiers_state = downloader.db.get_crawl_state("Frontiers")
        print("=" * 65)
        print("          THỐNG KÊ CHECKLIST HIỆN TẠI (SQLITE WAL)")
        print("=" * 65)
        print(f"[✓] Tổng bài đã tải thành công : {stats['success']}")
        print(f"    - arXiv                    : {stats['by_source'].get('arXiv', 0)}")
        print(f"    - Frontiers                : {stats['by_source'].get('Frontiers', 0)}")
        print(f"[!] Bài gặp lỗi                : {stats['failed']}")
        print(f"[📍] Vị trí quét arXiv (Offset): {arxiv_state['offset']}")
        print(f"[📍] Vị trí quét Frontiers     : {frontiers_state['offset']}")
        print(f"[📁] Thư mục lưu trữ           : {downloader.output_dir}")
        print("=" * 65)
        return

    # Xử lý danh sách từ khóa
    if args.keywords.strip():
        search_keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    else:
        search_keywords = DEFAULT_KEYWORD_GROUPS

    batch_size = args.limit if args.limit > 0 else args.batch_size

    print("=" * 75)
    print("      EEG & EMOTION RECOGNITION RESEARCH PAPER DOWNLOADER")
    print("           (CONTINUOUS & CRASH-PROOF CHECKLIST EDITION)   ")
    print("=" * 75)
    print(f"[*] Chế độ hoạt động : {'CHẠY LIÊN TỤC (Continuous Loop)' if args.continuous else 'CHẠY MỘT LẦN (Single Run)'}")
    print(f"[*] Nguồn mục tiêu   : {args.sources.upper()}")
    print(f"[*] Lô tải mỗi chu kỳ: {batch_size} bài/nguồn")
    if args.continuous:
        print(f"[*] Nghỉ giữa chu kỳ : {args.cycle_interval}s ({args.cycle_interval // 60} phút)")
    print(f"[*] Giãn cách bài    : {args.min_delay}s - {args.max_delay}s (Random Jitter Anti-bot)")
    print(f"[*] Thư mục xuất     : {downloader.output_dir}")
    print(f"[*] Checklist DB     : {downloader.db_path} (SQLite WAL Chống Cúp Điện)")
    print("=" * 75)

    orchestrator = ContinuousOrchestrator(
        downloader=downloader,
        sources=args.sources,
        keywords=search_keywords,
        batch_size=batch_size,
        cycle_interval=args.cycle_interval,
        dry_run=args.dry_run
    )

    if args.continuous:
        orchestrator.start_loop()
    else:
        orchestrator.run_one_cycle(1)


if __name__ == "__main__":
    main()
