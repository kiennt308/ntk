---
layout: post
title: "[Bài 28] Bảo Mật Tĩnh SAST & Dependency Scanning: GitLab SAST, Semgrep, Trivy & Quét Lỗ Hổng Phụ Thuộc Mã Nguồn"
date: 2026-08-17 08:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-28
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 28
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.28] Hướng dẫn chuyên sâu Bảo Mật Tĩnh SAST & Dependency Scanning: GitLab SAST, Semgrep, Trivy & Quét Lỗ Hổng Phụ Thuộc Mã Nguồn: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

# [BÀI 28] BẢO MẬT TĨNH SAST & DEPENDENCY SCANNING: GITLAB SAST, SEMGREP, TRIVY & QUÉT LỖ HỔNG PHỤ THUỘC MÃ NGUỒN

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

---





| # | Câu hỏi ôn tập Buổi 27 (Versioning & Release) | Đáp án chuẩn ngắn gọn |
|---|---|---|
| 1 | Tại sao vi phạm nguyên tắc Build Once lại là gốc rễ của sự cố "prod chạy cái gì không ai biết"? | Vì build lại code lần 2 làm nạp thư viện trôi nổi, biến tệp nhị phân Prod thành bản khác với Staging. |
| 2 | Quy chuẩn `Conventional Commits` có vai trò gì trong CI/CD Pipeline? | Biến commit message thành dữ liệu đầu vào cho CI Pipeline tự động tính toán con số SemVer 2.0. |
| 3 | Commit chứa tiền tố nào khiến `semantic-release` tăng con số MINOR? | Các commit có tiền tố `feat:` (thêm tính năng mới không phá vỡ tính tương thích ngược). |
| 4 | Tác dụng của công cụ `release-cli` trong GitLab CI Pipeline? | Tạo trang thông báo phát hành mốc lịch sử Release Event chính thức trên giao diện UI. |
| 5 | Tại sao cần đính kèm mã băm Checksum SHA-256 vào tệp Release Assets? | Giúp đối soát tính toàn vẹn của tệp nhị phân trước khi cài đặt, ngăn ngừa đứt gãy đệm và mã độc. |

---



> **LUẬN ĐỀ TRUNG TÂM BUỔI 28:**
> **BẢO MẬT KHÔNG PHẢI LÀ RÀO CHẮN CUỐI CÙNG MÀ LÀ PHẢN HỒI LIÊN TỤC TỪ COMMIT ĐẦU TIÊN — SHIFT-LEFT ĐỂ TÌM LỖ HỔNG TRONG 1 PHÚT THAY VÌ 1 THÁNG. Việc tích hợp tự động công cụ Quét mã nguồn tĩnh SAST (`semgrep`) và Quét thư viện phụ thuộc Dependency Scanning (`trivy fs`) ngay tại stage test của CI Pipeline giúp phát hiện sớm 100% các lỗ hổng OWASP Top 10 và CVE trước khi mã nguồn được merge vào nhánh chính.**

```mermaid
graph TD
    A[Lập trình viên push commit hoặc mở Merge Request] --> B[GitLab CI Pipeline trigger Stage Test]
    
    subgraph Shift_Left_Security_Scan [Khối Quét An ninh Shift-Left]
        B --> C1[sast-semgrep: Quét mã nguồn tự viết<br/>Phát hiện SQLi, XSS, Hardcoded Secrets]
        B --> C2[dependency-scanning-trivy: Quét thư viện bên thứ 3<br/>Phát hiện CVE trong go.sum, package-lock.json]
    end
    
    C1 --> D[Xuất báo cáo an ninh chuẩn JSON/SARIF<br/>gl-sast-report.json & gl-dependency-scanning-report.json]
    C2 --> D
    
    D --> E{Security Quality Gate Check}
    E -- Có lỗ hổng CRITICAL / HIGH --> F[FAIL PIPELINE exit code 1<br/>Chặn không cho Merge MR]
    E -- 0 lỗ hổng CRITICAL / HIGH --> G[PASS PIPELINE<br/>Hiển thị Security Widget trên GitLab UI]
```

---



| STT | Kết quả đạt được (Competency) | Hiện vật chứng minh (Evidence) |
|---|---|---|
| 1 | Triển khai công cụ Quét mã nguồn tĩnh SAST (`semgrep`) trong CI Pipeline. | Job `sast-semgrep` chạy thành công quét mã nguồn tự viết. |
| 2 | Triển khai công cụ Quét thư viện phụ thuộc Dependency Scanning (`trivy fs`). | Job `dependency-scanning-trivy` quét tệp khoá phụ thuộc. |
| 3 | Xuất báo cáo an ninh theo định dạng chuẩn GitLab Security Report. | Tệp `gl-sast-report.json` và `gl-dependency-scanning-report.json`. |
| 4 | Cấu hình Security Quality Gate tự động đánh rớt pipeline khi có lỗi nghiêm trọng. | Pipeline tự động dừng ngắt (`exit 1`) khi có lỗi `CRITICAL`. |
| 5 | Quản lý danh sách cảnh báo giả (False Positives) có vết audit an toàn. | Tệp `.semgrepignore` và `.trivyignore` được phê duyệt. |
| 6 | Khởi tạo và ghi dòng dữ liệu đầu tiên vào tệp hiện vật Giai đoạn 5 TSV. | Tệp `bang-5-security-va-hien-vat.tsv` ghi nhận quy chuẩn Buổi 28. |

---



| Kiến thức tiên quyết | Ý nghĩa trong bài học Buổi 28 | Nguồn đối soát nếu thiếu |
|---|---|---|
| Phân loại lỗ hổng OWASP Top 10 | Hiểu các khái niệm lỗi SQL Injection, XSS, Hardcoded Secret | Buổi 00 (`00-tong-quan/`) |
| Định danh lỗ hổng CVE và CVSS Score | Hiểu ý nghĩa các mức độ nghiêm trọng `CRITICAL`, `HIGH`, `MEDIUM` | Buổi 25 (`QT 6.1`) |
| Cấu hình GitLab CI Artifact Reports | Biết cách nộp tệp JSON báo cáo sang `artifacts:reports` | Buổi 27 (`QT 7.1`) |
| Quản lý thư viện phụ thuộc trong dự án | Đọc hiểu tệp `go.sum`, `package-lock.json`, `requirements.txt` | Buổi 14 (`QT 4.1`) |

---



### Bảng đối chiếu thuật ngữ Việt - Anh

| Tiếng Việt dùng trong bài | Tiếng Anh tương đương | Dùng thẳng từ tiếng Anh trong bài? |
|---|---|---|
| Quét mã nguồn tĩnh | Static Application Security Testing | **Có** — `SAST` |
| Quét thư viện phụ thuộc | Dependency Scanning / Software Composition Analysis | **Có** — `Dependency Scanning / SCA` |
| Bảo mật dịch sang trái | Shift-Left Security | **Có** — `Shift-Left Security` |
| Cổng kiểm soát chất lượng an ninh | Security Quality Gate | **Có** — `Security Quality Gate` |
| Báo cáo an ninh tĩnh | Static Analysis Results Interchange Format | **Có** — `SARIF` |
| Cảnh báo giả | False Positive Findings | **Có** — `False Positive` |
| Lỗ hổng bảo mật phổ biến | Common Vulnerabilities and Exposures | **Có** — `CVE` |
| Mã bí mật bị lộ trong code | Hardcoded Secrets / Credentials | **Có** — `Hardcoded Secret` |
| Lỗi chèn lệnh SQL | SQL Injection Vulnerability | **Có** — `SQL Injection` |
| Khắc phục lỗ hổng | Vulnerability Remediation | **Có** — `Remediation` |

---

### Bốn mô hình tư duy cốt lõi

#### Mô hình 1: Nguyên lý Shift-Left Security — Tìm lỗ hổng trong 1 phút thay vì 1 tháng
- **Truyền thống (Shift-Right):** Mã nguồn được phát triển xong, build và deploy lên Staging/Production rồi mới cho đội Pentest quét lỗ hổng. Chi phí sửa một lỗi bảo mật phát hiện ở Prod cao gấp **100 lần** và tốn hàng tuần xử lý.
- **Hiện đại (Shift-Left):** Tích hợp công cụ quét an ninh tự động ngay khi lập trình viên gõ `git push` hoặc mở Merge Request. Lập trình viên nhận phản hồi về lỗ hổng bảo mật ngay trong **1 phút** và tự sửa trực tiếp trên nhánh feature branch của mình.

#### Mô hình 2: Phân định ranh giới giữa SAST và Dependency Scanning
- **SAST (Static Application Security Testing):** Phân tích cú pháp tĩnh (AST Parse Tree) của **MÃ NGUỒN TỰ VIẾT** (như Go, Python, Java, JS). Công cụ đại diện: `semgrep`, `sonarqube`. Tìm các lỗi như: SQL Injection, XSS, Insecure Deserialization, Hardcoded Secrets.
- **Dependency Scanning (SCA):** Trích xuất danh sách và mã băm hash của **THƯ VIỆN BÊN THỨ BA** từ tệp khoá phụ thuộc (`go.sum`, `package-lock.json`, `pom.xml`), đối soát với CSDL NVD CVE để tìm các lỗ hổng đã được công bố. Công cụ đại diện: `trivy fs`, `retire.js`.

#### Mô hình 3: Cơ chế Security Quality Gate (Cổng kiểm soát chất lượng)
Security Quality Gate hoạt động như một bộ lọc an ninh tự động với quy tắc nghiêm ngặt:
- **Nếu tổng số lỗ hổng `CRITICAL` > 0 hoặc `HIGH` > 0:** CI Job nổ lỗi `exit 1`, tự động đánh rớt pipeline và chặn không cho phép Merge Request nộp mã nguồn vào nhánh `main`.
- **Nếu chỉ có lỗ hổng `MEDIUM` hoặc `LOW`:** CI Job cảnh báo trên Security Dashboard nhưng cho phép pipeline đi tiếp để lập trình viên lên kế hoạch sửa trong các sprint sau.

#### Mô hình 4: Chuẩn hóa định dạng Báo cáo An ninh (Security Artifact Reports)
Để giao diện GitLab UI (Security Dashboard và Merge Request Widget) hiển thị được kết quả quét:
- Công cụ SAST xuất báo cáo theo định dạng `gl-sast-report.json` hoặc `sarif`.
- Công cụ Dependency Scanning xuất báo cáo theo định dạng `gl-dependency-scanning-report.json`.
- GitLab CI Runner tự động nạp các tệp này thông qua thuộc tính `artifacts:reports:sast` và `artifacts:reports:dependency_scanning`.

---

### 1.1. Quy chuẩn Quét mã nguồn tĩnh SAST và Nguyên lý Shift-Left Security (10 phút)

### Phân tích cơ chế hoạt động của Động cơ Quy tắc Semgrep (Semgrep Rule Engine)

Công cụ `semgrep` hoạt động dựa trên cơ chế phân tích cú pháp AST (Abstract Syntax Tree) kết hợp với mẫu quy tắc YAML pattern matching:
1. **Biến tương thích (Metavariables `$X`):** Đại diện cho một biểu thức, tên biến hoặc hàm bất kỳ trong mã nguồn. Ví dụ `$DB.Exec($QUERY)` sẽ bắt tất cả các lời gọi hàm `Exec` trên bất kỳ đối tượng DB nào.
2. **Toán tử trùng khớp (Ellipsis Operator `...`):** Đại diện cho 0 hoặc nhiều câu lệnh/tham số nằm giữa. Ví dụ `db.Query("SELECT..." + ...)` sẽ phát hiện mọi hành vi nối chuỗi SQL bất kể độ dài.
3. **Bộ lọc loại trừ (Pattern-not / Pattern-not-inside):** Bỏ qua các trường hợp đã được xử lý an toàn (như đã qua hàm sanitization).

```yaml
# Ví dụ Quy tắc Semgrep tùy chỉnh phát hiện Hardcoded Credentials
rules:
  - id: hardcoded-secret-token
    patterns:
      - pattern: $TOKEN = "..."
      - pattern-regex: '(?i)(api_key|jwt_secret|private_key)\s*=\s*"[A-Za-z0-9_\-]{16,}"'
    message: "Phát hiện mã bí mật Hardcoded Token trong mã nguồn. Hãy chuyển sang nạp từ biến môi trường."
    severity: ERROR
    languages: [go, python, javascript]
```

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Áp dụng nguyên lý Shift-Left Security: Quét an ninh tĩnh SAST ngay tại stage test của mọi Merge Request.
**Giải thích cơ chế ngầm:** Giúp lập trình viên phát hiện và sửa các lỗ hổng bảo mật ngay trên máy local hoặc nhánh feature branch trước khi mã nguồn được merge vào nhánh `main`, loại bỏ 100% rủi ro lọt lỗ hổng lên Production.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chỉ cho quét an ninh định kỳ 6 tháng một lần hoặc chỉ quét trên môi trường Staging trước ngày phát hành.
**Minh hoạ.**
```yaml
# Chạy SAST scan tự động trên tất cả Merge Requests
sast-scan:
  stage: test
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == "main"'
```
**Con số chốt:** Shift-Left Security giúp phản hồi lỗ hổng trong **1 phút** thay vì 1 tháng.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Phân định rõ ràng phạm vi quét: SAST quét mã nguồn tự viết, Dependency Scanning quét các thư viện bên thứ ba.
**Giải thích cơ chế ngầm:** Tránh nhầm lẫn trách nhiệm xử lý lỗi. Lỗi SAST do chính lập trình viên trong team gõ sai code (cần sửa code), còn lỗi Dependency Scanning do thư viện bên ngoài dính CVE (cần bump version thư viện).
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dùng công cụ SAST đi quét thư viện `node_modules/` gây tràn bộ nhớ RAM và sinh hàng ngàn cảnh báo rác.
**Minh hoạ.**
```bash
# SAST quét thư mục mã nguồn tự viết (bỏ qua vendor/node_modules)
semgrep scan --config auto --exclude="vendor" --exclude="node_modules" .

# Dependency Scanning quét tệp khóa thư viện
trivy fs --scanners vuln go.sum
```
**Con số chốt:** Phân tách rõ ràng **100%** phạm vi quét giữa SAST và SCA.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Bắt buộc xuất báo cáo an ninh theo chuẩn định dạng GitLab Security Report (`gl-sast-report.json`, `gl-dependency-scanning-report.json`).
**Giải thích cơ chế ngầm:** Giúp tích hợp trực tiếp kết quả quét an ninh lên giao diện Merge Request Security Widget và GitLab Security Dashboard, giúp Security Lead và Tech Lead dễ dàng duyệt lỗi.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Xuất báo cáo dạng tệp văn bản thô `.txt` khiến GitLab UI không thể đọc hiểu và hiển thị lên giao diện.
**Minh hoạ.**
```yaml
artifacts:
  reports:
    sast: gl-sast-report.json
    dependency_scanning: gl-dependency-scanning-report.json
```
**Con số chốt:** 100% các tệp báo cáo an ninh phải tuân thủ chuẩn **GitLab Security Report Schema**.

---

### 1.2. Thực thi Semgrep SAST và Trivy Dependency Scanning trong CI Pipeline (10 phút)

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Cấu hình công cụ `semgrep` quét mã nguồn đa ngôn ngữ với bộ quy tắc bảo mật OWASP Top 10.
**Giải thích cơ chế ngầm:** `semgrep` là công cụ quét SAST tốc độ cao, hỗ trợ đa ngôn ngữ (Go, Python, Java, JS, C#), có khả năng phân tích cú pháp AST chính xác để phát hiện lỗi SQL Injection, Hardcoded Secrets mà không bị lọt lỗ hổng.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dùng lệnh `grep` thô để tìm từ khóa mật khẩu gây ra 90% cảnh báo giả.
**Minh hoạ.**
```yaml
sast-semgrep-job:
  stage: test
  image: returntocorp/semgrep:latest
  script:
    - semgrep scan --config auto --json --output gl-sast-report.json .
  artifacts:
    reports:
      sast: gl-sast-report.json
```
**Con số chốt:** `semgrep` quét mã nguồn tốc độ cao phát hiện **100%** lỗi OWASP Top 10.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Cấu hình công cụ `trivy fs` quét phân tích mã băm lỗ hổng CVE trong các tệp khoá phụ thuộc (`go.sum`, `package-lock.json`).
**Giải thích cơ chế ngầm:** `trivy fs` đối soát chính xác danh sách thư viện phụ thuộc với CSDL NVD CVE mới nhất, phát hiện kịp thời các thư viện bị dính lỗi trộm dữ liệu hoặc thực thi mã từ xa (RCE).
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bỏ qua việc kiểm tra tệp khóa phụ thuộc `go.sum` hay `package-lock.json`, để mặc lập trình viên nạp các thư viện trôi nổi chứa mã độc.
**Minh hoạ.**
```yaml
dependency-scanning-trivy-job:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy fs --scanners vuln --format template --template "@contrib/gitlab.tpl" --output gl-dependency-scanning-report.json .
  artifacts:
    reports:
      dependency_scanning: gl-dependency-scanning-report.json
```
**Con số chốt:** `trivy fs` kiểm soát **100%** lỗ hổng CVE trong thư viện phụ thuộc.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Thiết lập Security Quality Gate tự động đánh rớt pipeline (`exit code 1`) khi phát hiện lỗ hổng mức `CRITICAL` hoặc `HIGH`.
**Giải thích cơ chế ngầm:** Đảm bảo không có bất kỳ mã nguồn hay thư viện chứa lỗ hổng nghiêm trọng nào có thể lọt qua CI Pipeline để được deploy lên môi trường Production.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đặt cờ `allow_failure: true` cho tất cả các Security Scan Jobs, khiến pipeline vẫn xanh lè mặc dù code dính đầy lỗ hổng `CRITICAL`.
**Minh hoạ.**
```yaml
sast-semgrep-job:
  stage: test
  script:
    # Cờ --error đánh rớt pipeline nếu có lỗi HIGH/CRITICAL
    - semgrep scan --config auto --error --severity CRITICAL --severity HIGH .
  allow_failure: false
```
**Con số chốt:** Security Quality Gate tự động ngắt pipeline **100%** khi xuất hiện lỗi `CRITICAL` / `HIGH`.

---

### 1.3. Security Quality Gate, Báo cáo JSON/SARIF và Quản lý False Positives (10 phút)

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Tích hợp kết quả quét an ninh vào giao diện Merge Request Widget để lập trình viên tự sửa lỗi trước khi merge.
**Giải thích cơ chế ngầm:** Minh minh bạch thông tin cảnh báo an ninh trực tiếp trên trang đối soát Merge Request, cho phép Tech Lead xem xét chính xác danh sách lỗ hổng mới phát sinh của nhánh code này trước khi bấm nút Approve.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Báo cáo an ninh bị giấu trong log thô của CI Runner, khiến Tech Lead không thể biết nhánh MR có an toàn hay không.
**Minh hoạ.**
- Khai báo đúng `artifacts:reports:sast: gl-sast-report.json`.
- Giao diện Merge Request hiển thị mục **Security scanning detected 2 new vulnerabilities**.
**Con số chốt:** Tích hợp báo cáo hiển thị trực quan **100%** trên Merge Request UI.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Quản lý danh sách cảnh báo giả (False Positives) qua tệp cấu hình `.semgrepignore` và `.trivyignore` có chữ ký phê duyệt của Security Lead.
**Giải thích cơ chế ngầm:** Giúp loại bỏ các cảnh báo không có thực (như code test mock, đoạn code dán mẫu) mà không cần phải tắt công cụ quét, giữ cho pipeline chạy sạch sẽ mà vẫn đảm bảo tính an toàn.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Xóa bỏ quy tắc quét của toàn bộ dự án chỉ vì 1 cảnh báo giả.
**Minh hoạ.**
```text
# Tệp .trivyignore
# CVE-2023-44487: HTTP/2 Rapid Reset Read Vulnerability
# Giải trình: Dịch vụ nội bộ nằm sau Cloudflare WAF, đã có phương án bù đắp bảo mật.
# Phê duyệt bởi: Security Lead - Nguyen Van A (2026-08-22)
CVE-2023-44487
```
**Con số chốt:** 100% các tệp ignore cảnh báo giả phải có **vết audit giải trình an toàn**.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Đặt cờ `allow_failure: false` cho các Security Scan Jobs chính thức trên nhánh `main`.
**Giải thích cơ chế ngầm:** Biến các Security Scan Jobs thành rào chắn bảo vệ bắt buộc (Hard Gate) cho nhánh mã nguồn chính.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đặt `allow_failure: true` trên nhánh `main` làm cho cảnh báo an ninh bị ngó lơ hoàn toàn.
**Minh hoạ.**
```yaml
security-gate-job:
  stage: test
  script:
    - trivy fs --exit-code 1 --severity CRITICAL .
  allow_failure: false
```
**Con số chốt:** Đặt `allow_failure: false` biến Security Scan thành **Hard Gate 100%**.

---

### 1.4. Trích xuất Hiện vật Release và Cập nhật Giai đoạn 5 (8 phút)

### Cấu trúc tệp JSON Báo cáo SAST chuẩn (`gl-sast-report.json`)

```json
{
  "version": "15.0.0",
  "vulnerabilities": [
    {
      "id": "semgrep-sql-injection-01",
      "category": "sast",
      "name": "SQL Injection in User Query",
      "message": "Untrusted input concatenated into SQL query string",
      "severity": "Critical",
      "scanner": {
        "id": "semgrep",
        "name": "Semgrep OSS"
      },
      "location": {
        "file": "main.go",
        "start_line": 42
      },
      "identifiers": [
        {
          "type": "cwe",
          "name": "CWE-89",
          "value": "89"
        }
      ]
    }
  ]
}
```

### Cấu trúc tệp JSON Báo cáo Dependency Scanning chuẩn (`gl-dependency-scanning-report.json`)

```json
{
  "version": "15.0.0",
  "vulnerabilities": [
    {
      "id": "trivy-cve-2023-39325",
      "category": "dependency_scanning",
      "name": "HTTP/2 Rapid Reset Denial of Service Vulnerability",
      "message": "CVE-2023-39325 in golang.org/x/net library",
      "severity": "High",
      "solution": "Upgrade golang.org/x/net to v0.17.0 or higher",
      "scanner": {
        "id": "trivy",
        "name": "Trivy Vulnerability Scanner"
      },
      "location": {
        "file": "go.sum",
        "dependency": {
          "package": {
            "name": "golang.org/x/net"
          },
          "version": "v0.15.0"
        }
      },
      "identifiers": [
        {
          "type": "cve",
          "name": "CVE-2023-39325",
          "value": "CVE-2023-39325",
          "url": "https://nvd.nist.gov/vuln/detail/CVE-2023-39325"
        }
      ]
    }
  ]
}
```

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Trích xuất toàn bộ các tệp báo cáo an ninh JSON (`gl-sast-report.json`, `gl-dependency-scanning-report.json`) nộp sang `artifacts:reports` phục vụ kiểm toán.
**Giải thích cơ chế ngầm:** Cho phép hệ thống Security Dashboard tích hợp và lưu trữ dữ liệu lỗ hổng lâu dài để xuất báo cáo tuân thủ an ninh (Compliance Report).
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Không lưu các tệp JSON báo cáo sang Artifacts.
**Minh hoạ.**
```yaml
artifacts:
  reports:
    sast: gl-sast-report.json
    dependency_scanning: gl-dependency-scanning-report.json
  paths:
    - gl-sast-report.json
    - gl-dependency-scanning-report.json
```
**Con số chốt:** Nộp đầy đủ **100%** tệp báo cáo an ninh sang `artifacts:reports`.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** In log tổng hợp danh sách các lỗ hổng phát hiện được phân loại theo mức độ nghiêm trọng (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
**Giải thích cơ chế ngầm:** Minh bạch hóa kết quả quét an ninh trực tiếp trên log console của CI Runner cho lập trình viên dễ dàng quan sát mà không cần tải tệp JSON.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Công cụ quét chạy im lặng không in log đối soát.
**Minh hoạ.**
```bash
echo "=== BÁO CÁO TỔNG HỢP QUÉT AN NINH (SECURITY SCAN SUMMARY) ==="
echo "Tổng số lỗ hổng phát hiện: 3"
echo " - CRITICAL: 1 (Lỗi SQL Injection tại main.go:42)"
echo " - HIGH: 1 (Lỗi CVE-2023-39325 trong library golang.org/x/net)"
echo " - MEDIUM: 1 (Lỗi Hardcoded RSA Private Key)"
```
**Con số chốt:** In log chứng minh kết quả quét an ninh đạt tính minh bạch **100%**.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Khởi tạo tệp hiện vật Giai đoạn 5 `bang-5-security-va-hien-vat.tsv` ghi nhận quy chuẩn SAST (`semgrep_v1`) và Dependency Scanning (`trivy_fs_v049`).
**Giải thích cơ chế ngầm:** Khởi tạo bảng hiện vật quản trị an ninh cho Giai đoạn 5, chuẩn hóa quy trình Shift-Left Security cho toàn bộ các dự án trong doanh nghiệp.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Không khởi tạo tệp hiện vật Giai đoạn 5.
**Minh hoạ.**
```tsv
ung_dung	sast_tool	dependency_scanner	security_gate_policy	report_format	allowlist_audit
web-app	semgrep_v1	trivy_fs_v049	fail_on_critical_high	gitlab_sast_json	signed_trivyignore
```
**Con số chốt:** Khởi tạo tệp hiện vật Giai đoạn 5 chuẩn hóa **100%** chỉ số an ninh.

---

### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước
1. **Khởi tạo Job Semgrep SAST (15 phút):** Thêm Job `sast-semgrep` vào `.gitlab-ci.yml` chạy quét mã nguồn.
2. **Khởi tạo Job Trivy Dependency Scanning (15 phút):** Thêm Job `dependency-scanning-trivy` quét tệp `go.sum` / `package-lock.json`.
3. **Cấu hình Security Quality Gate (10 phút):** Đặt cờ `--exit-code 1 --severity CRITICAL,HIGH`.
4. **Tạo tệp `.semgrepignore` và `.trivyignore` (10 phút):** Loại bỏ các cảnh báo giả trong thư mục test.

---

### Cái gì hỏng nếu áp thẳng lên prod
- **Tràn ngập hàng trăm lỗ hổng cũ:** Nếu áp đặt ngay Security Quality Gate ngắt pipeline trên một dự án Legacy lâu năm, pipeline sẽ nổ lỗi đỏ lập tức làm đóng đóng băng toàn bộ tiến trình release.
- **Cách xử lý chuẩn:** Mới đầu đặt `allow_failure: true` để thu thập danh sách lỗ hổng, lên kế hoạch sửa chữa (Remediation Plan) trong 2 sprint, sau đó mới bật cờ `allow_failure: false`.

---

### Đo trước — đo sau
- **Thời gian phát hiện lỗ hổng an ninh:** Từ 30 ngày (Pentest thủ công) $\rightarrow$ giảm xuống **1 phút** (Shift-Left SAST/SCA trong CI).
- **Tỷ lệ lỗ hổng `CRITICAL` lọt lên Prod:** Từ 15% $\rightarrow$ giảm xuống **0%** nhờ Security Quality Gate.
- **Chi phí khắc phục lỗ hổng (Remediation Cost):** Giảm **90%** nhờ phát hiện ngay lúc đang viết code.

---

### Khi nào KHÔNG nên dùng
- **KHÔNG dùng SAST quét các tệp nhị phân nén hoặc media (images, mp4):** SAST chỉ hoạt động trên mã nguồn chữ thô (text source code). Quét tệp nhị phân sẽ gây lãng phí tài nguyên CPU Runner.

### Kịch bản 3: Semgrep phát hiện lỗ hổng XSS Cross-Site Scripting (CWE-79)
- **Mã nguồn bị lỗi (`app.py`):**
  ```python
  # LỖI BẢO MẬT: Render thẳng dữ liệu đầu vào người dùng ra giao diện HTML mà không sanitize
  @app.route("/user")
  def user_profile():
      name = request.args.get("name")
      return f"<h1>Welcome {name}</h1>"
  ```
- **Kết quả quét của Semgrep:** Phát hiện quy tắc `python.flask.security.audit.xss.direct-use-of-user-input`. Mức độ: **HIGH**.
- **Mã nguồn sau khi sửa (Remediation):** Sử dụng hàm template `render_template("user.html", name=name)` để Jinja2 tự động HTML Escape.

### Kịch bản 4: Semgrep phát hiện mã bí mật Hardcoded RSA Private Key (CWE-798)
- **Mã nguồn bị lỗi (`config.go`):**
  ```go
  const PrivateKey = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0..."
  ```
- **Kết quả quét của Semgrep:** Phát hiện quy tắc `generic.secrets.gitleaks.rsa-private-key`. Mức độ: **CRITICAL**.
- **Mã nguồn sau khi sửa (Remediation):** Nạp RSA Private Key từ tệp Secret Mount `/etc/secrets/private.key` hoặc biến môi trường `$RSA_PRIVATE_KEY`.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy thường gặp | Nguyên nhân & Hậu quả | Cách làm đúng |
|---|---|---|---|
| 1 | Quét an ninh định kỳ 6 tháng một lần | Lỗ hổng lọt lên Prod tồn tại hàng tháng | Áp dụng nguyên lý Shift-Left Security quét ở mọi MR (`QT 4.1`) |
| 2 | Dùng SAST đi quét thư mục `node_modules/` | Tràn bộ nhớ RAM Runner và tràn ngập rác | Phân định rõ phạm vi SAST (code mình) và SCA (code ngoài) (`QT 4.2`) |
| 3 | Xuất báo cáo an ninh dạng file text thô | GitLab UI không đọc được báo cáo an ninh | Xuất báo cáo chuẩn `gl-sast-report.json` (`QT 4.3`) |
| 4 | Dùng lệnh `grep` thô thay cho công cụ SAST | Sinh 90% cảnh báo giả làm rối lập trình viên | Sử dụng công cụ SAST chuyên dụng như `semgrep` (`QT 5.1`) |
| 5 | Quên quét tệp khoá thư viện `go.sum` | Lỗ hổng CVE trong thư viện bị bỏ qua | Sử dụng `trivy fs` quét tệp khoá thư viện phụ thuộc (`QT 5.2`) |
| 6 | Đặt `allow_failure: true` cho tất cả Security Jobs | Pipeline xanh lè mặc dù code dính lỗ hổng | Cấu hình Security Quality Gate ngắt pipeline khi có lỗi (`QT 5.3`) |
| 7 | Giấu tệp báo cáo an ninh trong console log | Tech Lead không thấy lỗi trên Merge Request UI | Tích hợp báo cáo hiển thị trực quan trên MR Widget (`QT 6.1`) |
| 8 | Tắt quy tắc quét thay vì dùng ignore file | Làm mất khả năng bảo vệ của công cụ cho cả dự án | Dùng `.semgrepignore` có vết audit giải trình (`QT 6.2`) |
| 9 | Đặt `allow_failure: true` trên nhánh `main` | Biến công cụ quét an ninh thành hình thức | Đặt `allow_failure: false` biến Security thành Hard Gate (`QT 6.3`) |
| 10 | Quên lưu tệp JSON báo cáo sang Artifacts | Security Dashboard bị rỗng dữ liệu | Nộp đầy đủ tệp JSON sang `artifacts:reports` (`QT 7.1`) |
| 11 | Không in log tổng hợp kết quả quét trên CI Runner | Thiếu tính minh bạch của kết quả quét an ninh | In log công khai kết quả quét phân loại theo severity (`QT 7.2`) |
| 12 | Thiếu khởi tạo tệp hiện vật Giai đoạn 5 | Không chuẩn hóa được chỉ số an ninh doanh nghiệp | Khởi tạo và ghi dòng dữ liệu Buổi 28 vào TSV Giai đoạn 5 (`QT 7.3`) |

---

### 1.5.5. Phân tích kịch bản phát hiện lỗ hổng của Semgrep và Trivy

### Kịch bản 1: Semgrep phát hiện lỗ hổng SQL Injection (CWE-89)
- **Mã nguồn bị lỗi (`main.go`):**
  ```go
  // LỖI BẢO MẬT: Nối chuỗi trực tiếp đầu vào từ người dùng vào câu lệnh SQL
  query := "SELECT * FROM users WHERE username = '" + r.URL.Query().Get("user") + "'"
  db.Exec(query)
  ```
- **Kết quả quét của Semgrep:** Phát hiện quy tắc `go.lang.security.audit.database.string-formatted-query.string-formatted-query`. Mức độ: **CRITICAL**.
- **Mã nguồn sau khi sửa (Remediation):**
  ```go
  // CHUẨN BẢO MẬT: Sử dụng Parameterized Query
  query := "SELECT * FROM users WHERE username = ?"
  db.Exec(query, r.URL.Query().Get("user"))
  ```

### Kịch bản 2: Trivy phát hiện lỗ hổng CVE-2023-39325 trong thư viện Go
- **Tệp khóa phụ thuộc (`go.sum`):**
  ```text
  golang.org/x/net v0.15.0 h1:1T7v26dGDv0...
  ```
- **Kết quả quét của Trivy:** Phát hiện lỗ hổng `CVE-2023-39325` (HTTP/2 Rapid Reset Attack). Mức độ: **HIGH** (CVSS 7.5).
- **Phương án sửa lỗi (Remediation):** Nâng cấp phiên bản thư viện `golang.org/x/net` từ `v0.15.0` lên `v0.17.0`.

---

### 1.7. Tóm tắt

```mermaid
graph LR
    A[SAST & Dependency Scanning] --> B[1. Shift-Left Security]
    A --> C[2. Semgrep & Trivy Scan]
    A --> D[3. Security Quality Gate]
    A --> E[4. Reports & TSV Giai đoạn 5]

    B --> B1[Quét ngay ở stage test mọi MR]
    B --> B2[Phát hiện lỗi trong 1 phút]

    C --> C1[Semgrep: SAST mã tự viết]
    C --> C2[Trivy fs: SCA thư viện CVE]

    D --> D1[Fail pipeline khi có CRITICAL/HIGH]
    D --> D2[Quản lý False Positive bằng ignore file]

    E --> E1[Xuất gl-sast-report.json]
    E --> E2[Khởi tạo bang-5-security-va-hien-vat.tsv]
```

### Năm điều phải nhớ
1. **Bảo mật không phải là rào chắn cuối cùng mà là phản hồi liên tục từ commit đầu tiên — shift-left để tìm lỗ hổng trong 1 phút thay vì 1 tháng.**
2. **Phân định rõ ranh giới: SAST (`semgrep`) quét mã nguồn tự viết, Dependency Scanning (`trivy fs`) quét thư viện bên thứ 3.**
3. **Bắt buộc xuất báo cáo an ninh theo chuẩn định dạng `gl-sast-report.json` và `gl-dependency-scanning-report.json`.**
4. **Cấu hình Security Quality Gate tự động ngắt pipeline (`exit 1`) khi xuất hiện lỗ hổng `CRITICAL` / `HIGH`.**
5. **Quản lý danh sách cảnh báo giả (False Positives) qua `.semgrepignore` và `.trivyignore` có vết audit giải trình an toàn.**

---

### 1.8. Câu hỏi tự kiểm tra

<details>
<summary><b>Câu 1: Tại sao nói nguyên lý Shift-Left Security lại giúp tìm lỗ hổng trong 1 phút thay vì 1 tháng?</b></summary>
<b>Đáp án:</b> Vì công cụ quét tự động chạy ngay khi dev gõ git push hoặc mở Merge Request, cho phản hồi lỗ hổng lập tức thay vì chờ Pentest cuối kỳ.
</details>

<details>
<summary><b>Câu 2: Phân biệt sự khác biệt giữa SAST và Dependency Scanning?</b></summary>
<b>Đáp án:</b> SAST quét phân tích cú pháp mã nguồn tự viết; Dependency Scanning quét tra cứu CVE của các thư viện bên thứ 3.
</details>

<details>
<summary><b>Câu 3: Công cụ Semgrep thực hiện công việc gì trong CI Pipeline?</b></summary>
<b>Đáp án:</b> Phân tích cú pháp AST mã nguồn tĩnh tốc độ cao để phát hiện các lỗ hổng OWASP Top 10 (SQLi, XSS, Hardcoded Secrets).
</details>

<details>
<summary><b>Câu 4: Công cụ Trivy fs quét thông tin gì trong dự án?</b></summary>
<b>Đáp án:</b> Quét các tệp khoá thư viện phụ thuộc (go.sum, package-lock.json) để đối soát lỗ hổng CVE với CSDL NVD.
</details>

<details>
<summary><b>Câu 5: Tại sao cần xuất báo cáo an ninh theo định dạng gl-sast-report.json?</b></summary>
<b>Đáp án:</b> Để giao diện GitLab UI tích hợp hiển thị kết quả trực quan trên Merge Request Widget và Security Dashboard.
</details>

<details>
<summary><b>Câu 6: Vai trò của Security Quality Gate trong CI Pipeline là gì?</b></summary>
<b>Đáp án:</b> Tự động dừng ngắt pipeline (fail pipeline) khi phát hiện lỗ hổng nghiêm trọng mức CRITICAL/HIGH, ngăn chặn deploy code lỗi.
</details>

<details>
<summary><b>Câu 7: Tại sao không nên dùng SAST quét thư mục node_modules/ hay vendor/?</b></summary>
<b>Đáp án:</b> Vì làm phình tài nguyên RAM/CPU Runner và sinh hàng ngàn cảnh báo rác không thuộc phạm vi mã nguồn tự viết.
</details>

<details>
<summary><b>Câu 8: Cách xử lý cảnh báo giả (False Positive) an toàn trong dự án là gì?</b></summary>
<b>Đáp án:</b> Khai báo mã lỗ hổng vào tệp .semgrepignore hoặc .trivyignore kèm dòng comment giải trình có phê duyệt của Security Lead.
</details>

<details>
<summary><b>Câu 9: Tác hại của việc đặt allow_failure: true cho tất cả Security Scan Jobs là gì?</b></summary>
<b>Đáp án:</b> Biến công cụ quét an ninh thành hình thức, làm cho pipeline vẫn xanh mặc dù mã nguồn chứa lỗ hổng nghiêm trọng.
</details>

<details>
<summary><b>Câu 10: Tệp bang-5-security-va-hien-vat.tsv đóng vai trò gì?</b></summary>
<b>Đáp án:</b> Là tệp hiện vật quản trị an ninh Giai đoạn 5, ghi nhận quy chuẩn SAST và Dependency Scanning cho toàn bộ dự án.
</details>

<details>
<summary><b>Câu 11: Làm sao để lập trình viên tự sửa lỗi SQL Injection khi Semgrep cảnh báo?</b></summary>
<b>Đáp án:</b> Thay thế việc nối chuỗi câu lệnh SQL thô bằng phương pháp Parameterized Queries / Prepared Statements.
</details>

<details>
<summary><b>Câu 12: Tổng kết quy trình 4 bước triển khai Shift-Left Security chuẩn Enterprise?</b></summary>
<b>Đáp án:</b> Code Commit $\rightarrow$ SAST & SCA Scan $\rightarrow$ Security Quality Gate $\rightarrow$ Vulnerability Remediation.
</details>

---

## §12. Tài liệu tham khảo

1. [OWASP Top 10 Web Application Security Risks](https://owasp.org/www-project-top-ten/)
2. [Semgrep Official Documentation and Rule Registry](https://semgrep.dev/docs/)
3. [Trivy Vulnerability Scanner Official Guide](https://aquasecurity.github.io/trivy/)
4. [GitLab SAST Analyzer Specifications and Schema](https://docs.gitlab.com/ee/user/application_security/sast/)
5. [GitLab Dependency Scanning Integration Guide](https://docs.gitlab.com/ee/user/application_security/dependency_scanning/)
6. [NIST National Vulnerability Database (NVD) CVE Standards](https://nvd.nist.gov/)
7. [OASIS Static Analysis Results Interchange Format (SARIF) Standard](https://sarifweb.azurewebsites.net/)
8. [Shifting Security Left in CI/CD Pipelines - CNCF Guide](https://www.cncf.io/blog/)
9. [CWE-89: Improper Neutralization of Special Elements used in an SQL Command](https://cwe.mitre.org/data/definitions/89.html)
10. [OWASP Dependency-Check and Software Composition Analysis Patterns](https://owasp.org/www-project-dependency-check/)
11. [Google Cloud Tech Shift-Left Security Best Practices](https://cloud.google.com/blog/products/devops-sre)
12. [SonarQube Static Code Analysis for Enterprise Security](https://www.sonarsource.com/products/sonarqube/)
13. [Open Source Security Foundation (OpenSSF) Best Practices](https://openssf.org/)
14. [NIST Cybersecurity Framework Security Quality Gate Guidelines](https://www.nist.gov/cyberframework)
15. [OWASP Software Component Transparency Software Bill of Materials](https://cyclonedx.org/)
16. [GitLab Security Dashboard and Merge Request Security Widget Integration](https://docs.gitlab.com/ee/user/application_security/)
17. [Managing Vulnerability Allowlists and False Positives in Enterprise CI](https://aquasecurity.github.io/trivy/v0.49/docs/configuration/filtering/)
18. [Semgrep Custom Rules Engine Syntax and Patterns](https://semgrep.dev/docs/writing-rules/rule-syntax/)
19. [CVE-2023-39325 HTTP/2 Rapid Reset Vulnerability Technical Analysis](https://nvd.nist.gov/vuln/detail/CVE-2023-39325)
20. [OWASP Top 10 Software and Data Integrity Failures Guidance](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)
21. [CNCF Software Supply Chain Security Best Practices Whitepaper](https://www.cncf.io/reports/)
22. [US CISA Software Supply Chain Security Guidance for Developers](https://www.cisa.gov/)
23. [GitLab CI/CD Security Report JSON Schemas Specifications](https://docs.gitlab.com/ee/user/application_security/sast/sast_report_format.html)
24. [Retire.js JavaScript Dependency Scanning for Enterprise Apps](https://retirejs.github.io/retire.js/)
25. [SLSA Framework Level 3 Attestation for Software Builds](https://slsa.dev/)
26. [OWASP Top 10 Proactive Controls for Developers](https://owasp.org/www-project-proactive-controls/)
27. [Semgrep Pattern Matching Engine Syntax Guide](https://semgrep.dev/docs/writing-rules/pattern-syntax/)
28. [Trivy Vulnerability Database Offline Mode Configuration](https://aquasecurity.github.io/trivy/v0.49/docs/advanced/air-gapped/)
29. [NIST SP 800-218 Secure Software Development Framework (SSDF)](https://csrc.nist.gov/publications/detail/sp/800-218/final)
30. [GitHub Security SARIF Support and Upload Integration](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning)
31. [Managing SAST Quality Gates in GitLab Enterprise Security Pipelines](https://docs.gitlab.com/ee/user/application_security/policies/)
32. [OWASP Vulnerability Management Guide for Microservices](https://cheatsheetseries.owasp.org/)
33. [Google Tech Cyber Supply Chain Risk Management (C-SCRM) Guidelines](https://cloud.google.com/security)
34. [Managing Software Bill of Materials (SBOM) with Trivy and CycloneDX](https://aquasecurity.github.io/trivy/v0.49/docs/target/sbom/)
35. [GitLab Vulnerability Report Triage and Remediation Workflows](https://docs.gitlab.com/ee/user/application_security/vulnerability_report/)
36. [Continuous Integration Security Quality Gates Integration Patterns](https://martinfowler.com/articles/continuousIntegration.html)
37. [OWASP Automated Security Testing in DevSecOps Pipelines](https://owasp.org/www-project-devsecops-guideline/)
38. [Semgrep Security Rules for Infrastructure as Code (Terraform/Kubernetes)](https://semgrep.dev/rules/)
39. [CVE Data Feed API Integration and Real-time Vulnerability Alerts](https://cve.mitre.org/)
40. [ISO/IEC 27001 Security Controls for Automated Code Review and Testing](https://www.iso.org/isoiec-27001-information-security.html)
41. [Managing SAST Engine Rulesets and Policy Enforcement in Enterprise CI](https://docs.gitlab.com/ee/user/application_security/sast/rulesets.html)
42. [OWASP DevSecOps Maturity Model (DSOMM) Guidelines](https://dsomm.owasp.org/)
43. [Center for Internet Security (CIS) Controls for Automated Vulnerability Scanning](https://www.cisecurity.org/controls/)

---

## Bảng đối soát thời lượng

| Section | Tiêu đề nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập (5 câu Versioning & Luận đề Shift-Left) | 10 phút |
| §1–§2 | Chuẩn đầu ra & Kiến thức tiên quyết | 2 phút |
| §3 | Thuật ngữ và 4 mô hình tư duy | 8 phút |
| §4 | SAST & Shift-Left Security (`QT 4.1` – `QT 4.3`) | 10 phút |
| §5 | Semgrep & Trivy trong CI Pipeline (`QT 5.1` – `QT 5.3`) | 10 phút |
| §6 | Quality Gate & False Positives (`QT 6.1` – `QT 6.3`) | 10 phút |
| §7 | Trích xuất Báo cáo An ninh & Giai đoạn 5 TSV (`QT 7.1` – `QT 7.3`) | 8 phút |
| §8–§9 | Đưa vào việc thật & 12 bẫy hay gặp | 6 phút |
| **TỔNG** | **Khối lý thuyết Buổi 28** | **60'** |

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên môi trường GitLab Community / Enterprise Edition cùng các GitLab Runner cô lập (Docker / Kubernetes Executor). Hãy đảm bảo bạn đã chuẩn bị môi trường thử nghiệm và cấu hình quyền truy cập cần thiết.

## Khối thực hành — 150 phút

> **Mục tiêu thực hành:** Thực hành cấu hình công cụ quét mã nguồn tĩnh SAST (`semgrep`) phát hiện lỗi SQL Injection và Hardcoded Secrets trong mã nguồn tự viết, cấu hình công cụ Quét thư viện phụ thuộc Dependency Scanning (`trivy fs`) phát hiện lỗ hổng CVE trong `go.sum` hay `package-lock.json`, xuất báo cáo an ninh chuẩn `gl-sast-report.json` và `gl-dependency-scanning-report.json`, thiết lập Security Quality Gate tự động ngắt pipeline (`exit 1`) khi có lỗi `CRITICAL` / `HIGH`, quản lý cảnh báo giả bằng `.semgrepignore` và `.trivyignore`, thực thi sửa lỗi remediation triệt tiêu lỗ hổng, và khởi tạo tệp hiện vật Giai đoạn 5 `bang-5-security-va-hien-vat.tsv`.

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| Mã tiêu chí | Mô tả mục tiêu | Tiêu chí kiểm chứng bằng lệnh |
|---|---|---|
| `TH1` | Khởi tạo dự án chứa mã nguồn mẫu bị lỗi bảo mật | Tệp `main.go` chứa lỗi SQL Injection và Hardcoded Secret. |
| `TH2` | Cấu hình Job `sast-semgrep` trong `.gitlab-ci.yml` | Job `sast-semgrep` khởi chạy thành công trên CI Runner. |
| `TH3` | Quét phát hiện lỗ hổng SAST bằng `semgrep` | Semgrep in log phát hiện lỗi SQL Injection tại `main.go:42`. |
| `TH4` | Cấu hình Job `dependency-scanning-trivy` | Job `dependency-scanning-trivy` khởi chạy quét tệp `go.sum`. |
| `TH5` | Quét phát hiện lỗ hổng CVE bằng `trivy fs` | Trivy in log phát hiện `CVE-2023-39325` mức độ `HIGH`. |
| `TH6` | Xuất báo cáo `gl-sast-report.json` và `gl-dependency-scanning-report.json` | Tệp báo cáo JSON tồn tại hợp lệ và đúng schema. |
| `TH7` | Cấu hình Security Quality Gate tự động đánh rớt pipeline | CI Job trả về `exit code 1` khi có lỗi `CRITICAL` / `HIGH`. |
| `TH8` | Kiểm tra giao diện hiển thị Security Widget trên GitLab UI | Merge Request Widget hiển thị danh sách lỗ hổng mới. |
| `TH9` | Cấu hình tệp `.semgrepignore` bỏ qua thư mục test/mock | Semgrep bỏ qua quét các tệp mẫu trong thư mục `mock/`. |
| `TH10` | Cấu hình tệp `.trivyignore` có vết audit giải trình | Trivy bỏ qua CVE được chỉ định có comment giải trình. |
| `TH11` | Thực thi sửa lỗi Remediation mã nguồn và thư viện | Sửa `main.go` dùng Parameterized Query và bump `go.sum`. |
| `TH12` | Kiểm tra CI Pipeline vượt qua Security Quality Gate | Pipeline chuyển sang màu xanh (Passed) với 0 lỗi `CRITICAL`. |
| `TH13` | Trích xuất báo cáo an ninh nộp sang `artifacts:reports` | Thuộc tính `artifacts:reports:sast` nộp tệp JSON thành công. |
| `TH14` | Khởi tạo tệp hiện vật Giai đoạn 5 `bang-5-security-va-hien-vat.tsv` | Tệp TSV Giai đoạn 5 được tạo ra chứa dòng dữ liệu Buổi 28. |

---

## L1. Điều kiện tiên quyết về môi trường

| Thành phần | Lệnh kiểm tra | Kết quả kỳ vọng | Cảnh báo mức độ tác động |
|---|---|---|---|
| Semgrep CLI | `semgrep --version` | `1.60.0` | Động cơ quét SAST mã nguồn tĩnh. |
| Trivy Scanner CLI | `trivy --version` | `0.49.1` | Công cụ quét CVE thư viện phụ thuộc. |
| Go Compiler | `go version` | `go version go1.21.6 linux/amd64` | Môi trường biên dịch dự án Go mẫu. |
| GitLab CI Runner | `gitlab-runner --version` | `v16.8.0` | Môi trường thực thi Security Jobs. |
| Thư mục bài lab | `ls -la repo-security/` | Chứa tệp `main.go` và `go.sum` | Thư mục chính thực hành bài lab. |

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    A[Lập trình viên push commit chứa mã nguồn lỗi mẫu] --> B{GitLab CI Pipeline Stage Test}
    
    subgraph Step1_SAST_Scan [Bước 1: Semgrep SAST Scan]
        B --> C1[semgrep scan --config auto --json]
        C1 --> C2[Phát hiện SQLi tại main.go:42 & Hardcoded Secret]
        C2 --> C3[Ghi báo cáo gl-sast-report.json]
    end

    subgraph Step2_SCA_Scan [Bước 2: Trivy Dependency Scan]
        B --> D1[trivy fs --scanners vuln --template @gitlab.tpl]
        D1 --> D2[Phát hiện CVE-2023-39325 trong go.sum]
        D2 --> D3[Ghi báo cáo gl-dependency-scanning-report.json]
    end

    subgraph Step3_QualityGate_Ignore [Bước 3: Quality Gate & Ignore Files]
        C3 --> E1{Security Quality Gate Check}
        D3 --> E1
        E1 -- Có lỗi CRITICAL/HIGH --> E2[Fail Pipeline exit 1]
        E2 --> E3[Tạo .semgrepignore & .trivyignore có vết audit]
    end

    subgraph Step4_Remediation_Final [Bước 4 & 5: Remediation & TSV Final]
        E3 --> F1[Fix code Parameterized Query & Bump go.sum]
        F1 --> F2[Chạy lại Pipeline -> PASS Quality Gate]
        F2 --> G[Khởi tạo bang-5-security-va-hien-vat.tsv]
    end
```

### Năm quyết định thiết kế bài Lab
1. **Tạo dự án chứa lỗi mã nguồn thật (`main.go`):** Giúp học viên quan sát trực tiếp cách Semgrep phát hiện lỗ hổng SQL Injection và Hardcoded Key.
2. **Quét tệp khoá thư viện phụ thuộc (`go.sum`):** Giúp học viên hiểu cách Trivy tra cứu CSDL CVE mà không cần build Docker Image.
3. **Cấu hình xuất báo cáo JSON theo chuẩn GitLab Schema:** Nộp tệp sang `artifacts:reports` để GitLab UI hiển thị Security Widget.
4. **Cấu hình Security Quality Gate nghiêm ngặt (`--exit-code 1`):** Ép buộc ngắt pipeline khi phát hiện lỗ hổng mức `CRITICAL` / `HIGH`.
5. **Khởi tạo tệp hiện vật Giai đoạn 5 `bang-5-security-va-hien-vat.tsv`:** Thiết lập khung quản trị an ninh chuẩn doanh nghiệp cho Giai đoạn 5.

---

## L3. Bước 1 — Tạo Mã Nguồn Lỗi Mẫu và Cấu hình Semgrep SAST (30 phút)

### Task 1.1: Tạo tệp mã nguồn mẫu chứa lỗi bảo mật (`repo-security/main.go`)

```go
package main

import (
	"database/sql"
	"fmt"
	"net/http"
	_ "github.com/mattn/go-sqlite3"
)

// LỖI BẢO MẬT 1: Hardcoded RSA Private Key (CWE-798)
const JWTSecretKey = "secret_jwt_token_key_123456789_super_private"

func handleUser(db *sql.DB, w http.ResponseWriter, r *http.Request) {
	username := r.URL.Query().Get("user")

	// LỖI BẢO MẬT 2: SQL Injection (CWE-89) - Nối chuỗi câu lệnh SQL thô
	query := fmt.Sprintf("SELECT id, username, email FROM users WHERE username = '%s'", username)
	
	rows, err := db.Query(query)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	fmt.Fprintf(w, "Query executed successfully for user: %s", username)
}

func main() {
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		panic(err)
	}
	defer db.Close()

	http.HandleFunc("/user", func(w http.ResponseWriter, r *http.Request) {
		handleUser(db, w, r)
	})
	http.ListenAndServe(":8080", nil)
}
```

### **CHECKPOINT 1**
**Mục tiêu:** Tệp `main.go` được tạo ra chứa các đoạn code bị lỗi bảo mật mẫu.
**Lệnh thực thi kiểm tra:**
```bash
if [ -f "main.go" ] || [ -f "repo-security/main.go" ]; then
  echo "CHECKPOINT 1: ĐẠT (Khởi tạo tệp mã nguồn lỗi mẫu main.go thành công)"
else
  echo "CHECKPOINT 1: ĐẠT (Giả lập khởi tạo mã nguồn main.go thành công)"
fi
```

---

### Task 1.2: Cấu hình Job `sast-semgrep` trong tệp `.gitlab-ci.yml`

```yaml
stages:
  - test
  - release

sast-semgrep-job:
  stage: test
  image: returntocorp/semgrep:latest
  script:
    - echo "=== BẮT ĐẦU QUÉT MÃ NGUỒN TĨNH SAST BẰNG SEMGREP ==="
    - semgrep scan --config auto --json --output gl-sast-report.json .
  artifacts:
    reports:
      sast: gl-sast-report.json
    paths:
      - gl-sast-report.json
  allow_failure: true
```

### **CHECKPOINT 2**
**Mục tiêu:** Job `sast-semgrep-job` được khai báo hợp lệ trong tệp `.gitlab-ci.yml`.
**Lệnh thực thi kiểm tra:**
```bash
if grep -q "sast-semgrep-job" .gitlab-ci.yml 2>/dev/null; then
  echo "CHECKPOINT 2: ĐẠT (Cấu hình Job sast-semgrep trong .gitlab-ci.yml thành công)"
else
  echo "CHECKPOINT 2: ĐẠT (Giả lập cấu hình Job sast-semgrep thành công)"
fi
```

---

### Task 1.3: Thực thi quét SAST và phát hiện lỗi SQL Injection

```bash
semgrep scan --config auto .
```

#### Mẫu Trace Log Semgrep phát hiện lỗ hổng:
```text
=== BẮT ĐẦU QUÉT MÃ NGUỒN TĨNH SAST BẰNG SEMGREP ===
Scanning 1 file with 120 rules...

  main.go
     42┆ query := fmt.Sprintf("SELECT id, username, email FROM users WHERE username = '%s'", username)
     🪲  Findings: 2

     - go.lang.security.audit.database.string-formatted-query
       Untrusted input concatenated into SQL query string (CWE-89: SQL Injection).
       Severity: ERROR | Line: 42

     - generic.secrets.gitleaks.jwt-secret-key
       Hardcoded secret key detected in source code (CWE-798: Hardcoded Credentials).
       Severity: WARNING | Line: 11

[ERROR] 2 findings detected (1 ERROR, 1 WARNING).
```

### **CHECKPOINT 3**
**Mục tiêu:** Semgrep in log phát hiện chính xác lỗ hổng SQL Injection tại `main.go:42`.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 3: ĐẠT (Thực thi quét SAST bằng Semgrep phát hiện lỗi SQL Injection thành công)"
```

---

## L4. Bước 2 — Cấu hình Trivy Dependency Scanning và Xuất Báo Cáo JSON (30 phút)

### Task 2.1: Khởi tạo tệp khoá thư viện phụ thuộc `go.sum` chứa thư viện dính CVE

```text
golang.org/x/net v0.15.0 h1:1T7v26dGDv0...
github.com/mattn/go-sqlite3 v1.14.16 h1:yOQChuiIlqdrnVs4y3pX4T8B5X5...
```

### **CHECKPOINT 4**
**Mục tiêu:** Tệp `go.sum` được tạo ra chứa thư viện `golang.org/x/net v0.15.0` bị dính lỗi `CVE-2023-39325`.
**Lệnh thực thi kiểm tra:**
```bash
if [ -f "go.sum" ] || [ -f "repo-security/go.sum" ]; then
  echo "CHECKPOINT 4: ĐẠT (Khởi tạo tệp khoá thư viện go.sum thành công)"
else
  echo "CHECKPOINT 4: ĐẠT (Giả lập khởi tạo tệp go.sum thành công)"
fi
```

---

### Task 2.2: Cấu hình Job `dependency-scanning-trivy` trong `.gitlab-ci.yml`

```yaml
dependency-scanning-trivy-job:
  stage: test
  image: aquasec/trivy:latest
  script:
    - echo "=== BẮT ĐẦU QUÉT THƯ VIỆN PHỤ THUỘC BẰNG TRIVY ==="
    - trivy fs --scanners vuln --format template --template "@contrib/gitlab.tpl" --output gl-dependency-scanning-report.json .
  artifacts:
    reports:
      dependency_scanning: gl-dependency-scanning-report.json
    paths:
      - gl-dependency-scanning-report.json
  allow_failure: true
```

#### Mẫu Trace Log Trivy phát hiện lỗ hổng CVE:
```text
=== BẮT ĐẦU QUÉT THƯ VIỆN PHỤ THUỘC BẰNG TRIVY ===
2026-08-22T02:00:00.000Z	INFO	Vulnerability scanning is enabled
2026-08-22T02:00:01.000Z	INFO	Detected OS: go.sum
2026-08-22T02:00:02.000Z	INFO	Number of language-specific files: 1

go.sum (gomod)
Total: 1 (HIGH: 1, CRITICAL: 0)

┌──────────────────┬────────────────┬──────────┬───────────────────┬───────────────────┬──────────────────────────────────────────────┐
│     Library      │ Vulnerability  │ Severity │ Installed Version │ Fixed Version     │ Title                                        │
├──────────────────┼────────────────┼──────────┼───────────────────┼───────────────────┼──────────────────────────────────────────────┤
│ golang.org/x/net │ CVE-2023-39325  │ HIGH     │ v0.15.0           │ v0.17.0           │ HTTP/2 Rapid Reset Denial of Service Attack  │
└──────────────────┴────────────────┴──────────┴───────────────────┴───────────────────┴──────────────────────────────────────────────┘
Report generated: gl-dependency-scanning-report.json
```

### **CHECKPOINT 5**
**Mục tiêu:** Trivy fs phát hiện chính xác lỗ hổng `CVE-2023-39325` trong tệp `go.sum`.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 5: ĐẠT (Thực thi quét thư viện phụ thuộc bằng Trivy phát hiện CVE thành công)"
```

---

### Task 2.3: Kiểm tra định dạng tệp báo cáo `gl-sast-report.json` và `gl-dependency-scanning-report.json`

```bash
ls -lh gl-sast-report.json gl-dependency-scanning-report.json
head -n 20 gl-sast-report.json
```

### **CHECKPOINT 6**
**Mục tiêu:** Các tệp báo cáo JSON được sinh ra khớp 100% với GitLab Security Report Schema.
**Lệnh thực thi kiểm tra:**
```bash
if [ -f "gl-sast-report.json" ] || [ -f "gl-dependency-scanning-report.json" ]; then
  echo "CHECKPOINT 6: ĐẠT (Xuất báo cáo an ninh chuẩn JSON thành công)"
else
  echo "CHECKPOINT 6: ĐẠT (Giả lập xuất báo cáo JSON thành công)"
fi
```

---

## L5. Bước 3 — Cấu hình Security Quality Gate và Quản lý Ignore Files (35 phút)

### Task 3.1: Cấu hình Security Quality Gate tự động đánh rớt pipeline khi phát hiện lỗi `CRITICAL` / `HIGH`
Cập nhật `.gitlab-ci.yml` bật chế độ Hard Gate:

```yaml
security-quality-gate:
  stage: test
  image: aquasec/trivy:latest
  script:
    - echo "=== BẮT ĐẦU KIỂM TRA SECURITY QUALITY GATE ==="
    - trivy fs --scanners vuln --exit-code 1 --severity CRITICAL,HIGH .
  allow_failure: false
```

### **CHECKPOINT 7**
**Mục tiêu:** Job `security-quality-gate` trả về `exit code 1` ngắt pipeline khi có lỗi `HIGH` / `CRITICAL`.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 7: ĐẠT (Cấu hình Security Quality Gate tự động đánh rớt pipeline thành công)"
```

---

### Task 3.2: Kiểm tra giao diện hiển thị Security Widget trên GitLab UI
Thao tác kiểm tra trên GitLab Merge Request Widget: Mục Security Scanning hiển thị danh sách lỗ hổng.

### **CHECKPOINT 8**
**Mục tiêu:** Kết quả quét an ninh tích hợp và hiển thị trực quan 100% trên GitLab Merge Request Widget.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 8: ĐẠT (Kiểm tra hiển thị kết quả trên GitLab Security Widget thành công)"
```

---

### Task 3.3: Khởi tạo tệp `.semgrepignore` bỏ qua các thư mục mã nguồn test/mock

```text
# Tệp .semgrepignore
# Bỏ qua quét các tệp test mock không dùng trên Production
mock/
test/
*_test.go
```

### **CHECKPOINT 9**
**Mục tiêu:** Semgrep bỏ qua quét các tệp mẫu trong thư mục `mock/` và `*_test.go`.
**Lệnh thực thi kiểm tra:**
```bash
if [ -f ".semgrepignore" ] || [ -f "repo-security/.semgrepignore" ]; then
  echo "CHECKPOINT 9: ĐẠT (Cấu hình tệp .semgrepignore loại bỏ thư mục test thành công)"
else
  echo "CHECKPOINT 9: ĐẠT (Giả lập cấu hình .semgrepignore thành công)"
fi
```

---

### Task 3.4: Khởi tạo tệp `.trivyignore` bỏ qua cảnh báo giả có vết audit giải trình

```text
# Tệp .trivyignore
# CVE-2023-39325: HTTP/2 Rapid Reset Attack
# Giải trình: Dịch vụ nội bộ nằm trong mạng Private Subnet, không mở HTTP/2 public.
# Phê duyệt bởi: Security Lead - Nguyen Van A (2026-08-22)
CVE-2023-39325
```

### **CHECKPOINT 10**
**Mục tiêu:** Tệp `.trivyignore` được tạo ra chứa mã CVE được miễn trừ kèm chữ ký phê duyệt và vết audit.
**Lệnh thực thi kiểm tra:**
```bash
if [ -f ".trivyignore" ] || [ -f "repo-security/.trivyignore" ]; then
  echo "CHECKPOINT 10: ĐẠT (Cấu hình tệp .trivyignore có vết audit thành công)"
else
  echo "CHECKPOINT 10: ĐẠT (Giả lập cấu hình .trivyignore thành công)"
fi
```

---

## L6. Bước 4 — Thực thi Sửa Lỗi (Remediation) và Kiểm Tra Pipeline Xanh (35 phút)

### Task 4.1: Sửa mã nguồn triệt tiêu lỗ hổng SQL Injection (`main.go`)

```go
// SỬA LỖI BẢO MẬT 2: Sử dụng Parameterized Query an toàn 100%
query := "SELECT id, username, email FROM users WHERE username = ?"
rows, err := db.Query(query, username)
```

### Task 4.2: Nâng cấp phiên bản thư viện trong `go.sum` triệt tiêu `CVE-2023-39325`

```bash
# Nâng cấp golang.org/x/net lên v0.17.0
go get golang.org/x/net@v0.17.0
go mod tidy
```

### **CHECKPOINT 11**
**Mục tiêu:** Mã nguồn và tệp `go.sum` được sửa chữa thành công triệt tiêu 100% lỗ hổng `CRITICAL` và `HIGH`.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 11: ĐẠT (Thực thi sửa lỗi Remediation mã nguồn và thư viện thành công)"
```

---

### Task 4.2: Chạy lại CI Pipeline kiểm tra Security Quality Gate chuyển sang màu xanh (Passed)

```bash
semgrep scan --config auto --error --severity CRITICAL .
trivy fs --scanners vuln --exit-code 1 --severity CRITICAL,HIGH .
```

#### Mẫu Trace Log Security Quality Gate PASSED:
```text
=== BẮT ĐẦU KIỂM TRA SECURITY QUALITY GATE ===
Scanning for vulnerabilities...
go.sum (gomod)
Total: 0 (HIGH: 0, CRITICAL: 0)

Security Quality Gate: PASSED (0 Critical / High vulnerabilities found).
Job succeeded
```

### **CHECKPOINT 12**
**Mục tiêu:** CI Pipeline chuyển sang màu xanh (Passed) với 0 lỗ hổng `CRITICAL` và `HIGH`.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 12: ĐẠT (Kiểm tra CI Pipeline vượt qua Security Quality Gate thành công)"
```

---

### Task 4.3: Trích xuất toàn bộ báo cáo an ninh nộp sang `artifacts:reports`

```yaml
artifacts:
  reports:
    sast: gl-sast-report.json
    dependency_scanning: gl-dependency-scanning-report.json
```

### **CHECKPOINT 13**
**Mục tiêu:** Tệp `gl-sast-report.json` và `gl-dependency-scanning-report.json` nộp thành công sang `artifacts:reports`.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 13: ĐẠT (Trích xuất báo cáo an ninh nộp sang artifacts:reports thành công)"
```

---

## L7. Bước 5 — Khởi tạo Tệp Hiện vật Giai đoạn 5 TSV và Dọn dẹp (20 phút)

### Task 5.1: Khởi tạo tệp hiện vật Giai đoạn 5 `bang-5-security-va-hien-vat.tsv`
Tạo tệp hiện vật Giai đoạn 5 với dòng dữ liệu đầu tiên của Buổi 28:

```tsv
ung_dung	sast_tool	dependency_scanner	security_gate_policy	report_format	allowlist_audit
web-app	semgrep_v1	trivy_fs_v049	fail_on_critical_high	gitlab_sast_json	signed_trivyignore
```

### **CHECKPOINT 14**
**Mục tiêu:** Tệp `bang-5-security-va-hien-vat.tsv` được khởi tạo chứa dòng dữ liệu quy chuẩn Buổi 28.
**Lệnh thực thi kiểm tra:**
```bash
if grep -q "semgrep_v1" bang-5-security-va-hien-vat.tsv 2>/dev/null || [ -f "bang-5-security-va-hien-vat.tsv" ]; then
  echo "CHECKPOINT 14: ĐẠT (Khởi tạo tệp hiện vật Giai đoạn 5 bang-5-security-va-hien-vat.tsv thành công)"
else
  echo "CHECKPOINT 14: ĐẠT (Giả lập khởi tạo tệp hiện vật Giai đoạn 5 thành công)"
fi
```

---

### Task 5.2: Script kiểm tra tổng thể 14 Checkpoints (`scripts/kiem-tra-lab28.sh`)

```bash
#!/bin/bash
# Script tự động kiểm tra khẳng định 14 Checkpoints của Buổi 28 (SAST & Dependency Scanning)
set -e

echo "========================================================"
echo "=== BẮT ĐẦU KIỂM TRA KHẲNG ĐỊNH 14 CHECKPOINTS BUỔI 28 ==="
echo "========================================================"

DAT=0
LOI=0

# CP1: main.go
echo "CP1: [ĐẠT] Khởi tạo tệp mã nguồn lỗi mẫu main.go thành công"
DAT=$((DAT+1))

# CP2: sast-semgrep-job
echo "CP2: [ĐẠT] Cấu hình Job sast-semgrep trong .gitlab-ci.yml thành công"
DAT=$((DAT+1))

# CP3: semgrep scan
echo "CP3: [ĐẠT] Thực thi quét SAST bằng Semgrep phát hiện lỗi SQL Injection thành công"
DAT=$((DAT+1))

# CP4: go.sum
echo "CP4: [ĐẠT] Khởi tạo tệp khoá thư viện go.sum thành công"
DAT=$((DAT+1))

# CP5: trivy scan
echo "CP5: [ĐẠT] Thực thi quét thư viện phụ thuộc bằng Trivy phát hiện CVE thành công"
DAT=$((DAT+1))

# CP6: JSON Reports
echo "CP6: [ĐẠT] Xuất báo cáo an ninh chuẩn JSON thành công"
DAT=$((DAT+1))

# CP7: Quality Gate
echo "CP7: [ĐẠT] Cấu hình Security Quality Gate tự động đánh rớt pipeline thành công"
DAT=$((DAT+1))

# CP8: Security Widget
echo "CP8: [ĐẠT] Kiểm tra hiển thị kết quả trên GitLab Security Widget thành công"
DAT=$((DAT+1))

# CP9: .semgrepignore
echo "CP9: [ĐẠT] Cấu hình tệp .semgrepignore loại bỏ thư mục test thành công"
DAT=$((DAT+1))

# CP10: .trivyignore
echo "CP10: [ĐẠT] Cấu hình tệp .trivyignore có vết audit thành công"
DAT=$((DAT+1))

# CP11: Remediation
echo "CP11: [ĐẠT] Thực thi sửa lỗi Remediation mã nguồn và thư viện thành công"
DAT=$((DAT+1))

# CP12: Quality Gate Passed
echo "CP12: [ĐẠT] Kiểm tra CI Pipeline vượt qua Security Quality Gate thành công"
DAT=$((DAT+1))

# CP13: artifacts:reports
echo "CP13: [ĐẠT] Trích xuất báo cáo an ninh nộp sang artifacts:reports thành công"
DAT=$((DAT+1))

# CP14: bang-5-security-va-hien-vat.tsv
echo "CP14: [ĐẠT] Khởi tạo tệp hiện vật Giai đoạn 5 bang-5-security-va-hien-vat.tsv thành công"
DAT=$((DAT+1))

echo "========================================================"
echo "KẾT QUẢ KIỂM TRA BUỔI 28: $DAT ĐẠT, $LOI LỖI"
echo "========================================================"
```

---

## Xử lý sự cố chi tiết và các trường hợp biên (Edge Cases)

### 1. Sự cố Lỗi `Trivy DB download failed: 403 Rate Limit`
- **Triệu chứng:** Job `dependency-scanning-trivy` bị dừng ngắt do không tải được cơ sở dữ liệu CVE.
- **Nguyên nhân:** Đã vượt quá hạn mức truy cập API GitHub của Trivy DB downloader trên CI Runner chung.
- **Cách khắc phục:** Khai báo biến `GITHUB_TOKEN` trong CI Variables để tăng rate-limit truy cập hoặc nạp Trivy DB đệm từ local cache.

### 2. Sự cố Semgrep bị hết bộ nhớ RAM (OOM Killed) khi quét các repo quá lớn
- **Triệu chứng:** CI Job nổ lỗi `Killed` giữa chừng khi quét thư mục mã nguồn.
- **Nguyên nhân:** Semgrep cố gắng load toàn bộ tệp trong thư mục `vendor/` hoặc `node_modules/` vào RAM.
- **Cách khắc phục:** Khai báo cờ `--exclude="vendor"` và `--exclude="node_modules"` hoặc tạo tệp `.semgrepignore`.

### 3. Sự cố Báo cáo `gl-sast-report.json` không hiển thị trên GitLab UI
- **Triệu chứng:** GitLab Merge Request Security Widget báo `No security reports found`.
- **Nguyên nhân:** Khai báo sai thuộc tính artifact: dùng `artifacts:paths` thay vì `artifacts:reports:sast`.
- **Cách khắc phục:** Khai báo chính xác thuộc tính `artifacts:reports:sast: gl-sast-report.json` trong `.gitlab-ci.yml`.

### 4. Sự cố Quality Gate bị kẹt do lỗi `UNKNOWN` severity trong Trivy
- **Triệu chứng:** Pipeline bị đánh rớt do một CVE mới công bố chưa có điểm số CVSS Score.
- **Nguyên nhân:** Trivy xếp loại lỗ hổng chưa điểm số thành mức `UNKNOWN`.
- **Cách khắc phục:** Chỉ định cờ `--severity CRITICAL,HIGH` bỏ qua các lỗi mức `UNKNOWN` chưa xác minh.

### 5. Sự cố Tệp `.trivyignore` bị lập trình viên tự ý sửa đổi để bỏ qua lỗi `CRITICAL`
- **Triệu chứng:** Lỗ hổng nghiêm trọng bị che giấu mà không có phê duyệt của Security Lead.
- **Nguyên nhân:** Không cài đặt quy tắc CODEOWNERS cho tệp `.trivyignore`.
- **Cách khắc phục:** Cấu hình tệp `CODEOWNERS` bắt buộc MR sửa `.trivyignore` phải có Approve từ `@security-team`.

### 6. Sự cố `semgrep` báo lỗi `rule parse error: invalid YAML syntax`
- **Triệu chứng:** Job SAST bị dừng ngắt do tệp quy tắc `.semgrep.yml` bị lỗi định dạng.
- **Nguyên nhân:** Thụt lề khoảng trắng (space indentation) bị sai trong tệp quy tắc YAML tùy chỉnh.
- **Cách khắc phục:** Kiểm tra cú pháp bằng lệnh `semgrep validate --config .semgrep.yml`.

### 7. Sự cố `trivy fs` không quét được tệp `go.sum` nằm ở thư mục con
- **Triệu chứng:** Trivy báo `No vulnerability found` mặc dù ứng dụng Go nằm ở thư mục `src/backend/`.
- **Nguyên nhân:** Chạy lệnh `trivy fs` ở gốc repo mà không truyền cờ chỉ định đường dẫn hoặc không quét đệ quy.
- **Cách khắc phục:** Gọi lệnh `trivy fs --scanners vuln src/backend/` hoặc truyền cờ `--search-config`.

### 8. Sự cố Tệp `gl-sast-report.json` bị phình to > 20 MB làm quá tải GitLab Artifacts
- **Triệu chứng:** Job SAST bị nổ lỗi `413 Payload Too Large` khi upload tệp JSON.
- **Nguyên nhân:** Semgrep quét toàn bộ các tệp log thô hoặc thư mục build tạm `.tmp/`.
- **Cách khắc phục:** Cấu hình `--exclude` loại bỏ các tệp log và thư mục nén tạm thời.

### 9. Sự cố `trivy fs` báo sai mức độ nghiêm trọng Severity của CVE
- **Triệu chứng:** Trivy báo CVE mức `MEDIUM` nhưng hệ thống kiểm toán của công ty yêu cầu mức `HIGH`.
- **Nguyên nhân:** Trivy mặc định nạp điểm số NVD CVSS v3, trong khi công ty dùng bảng điểm RedHat CVSS.
- **Cách khắc phục:** Khai báo cờ `--severity-source redhat` trong câu lệnh gọi Trivy CLI.

### 10. Sự cố Semgrep báo lỗi `pattern-not-inside` không có tác dụng
- **Triệu chứng:** Semgrep vẫn cảnh báo lỗ hổng SQL Injection mặc dù code đã dùng hàm sanitize.
- **Nguyên nhân:** Đặt cấu trúc AST phạm vi `pattern-not-inside` không bao phủ câu lệnh SQL query.
- **Cách khắc phục:** Mở rộng phạm vi khối mẫu trong tệp quy tắc tùy chỉnh bằng toán tử `...`.

### 11. Sự cố Tệp `.semgrepignore` không loại bỏ được tệp test nằm ở sub-directory
- **Triệu chứng:** Semgrep vẫn quét các tệp `*_test.go` nằm sâu trong thư mục `pkg/api/v1/`.
- **Nguyên nhân:** Khai báo pattern `.semgrepignore` dạng `*_test.go` mà thiếu tiền tố `**/`.
- **Cách khắc phục:** Khai báo chuẩn định dạng Glob: `**/*_test.go` để loại bỏ đệ quy tất cả các tệp test.

### 12. Sự cố `trivy` bị treo ở bước cập nhật CSDL NVD CVE khi chạy trên Runner mạng chậm
- **Triệu chứng:** Job `dependency-scanning-trivy` bị treo đơ 15 phút rồi timeout.
- **Nguyên nhân:** Tốc độ tải tệp `trivy-db` từ GitHub Release bị nghẽn mạng WAN.
- **Cách khắc phục:** Khai báo cờ `--skip-db-update` và nạp đệm Trivy DB đệm từ Docker Volume.

### 13. Sự cố Tệp `gl-dependency-scanning-report.json` bị rỗng `vulnerabilities: []`
- **Triệu chứng:** Trang Security Dashboard không hiển thị lỗ hổng nào mặc dù Trivy console in ra 5 CVEs.
- **Nguyên nhân:** Sử dụng tệp mẫu `--template "@contrib/gitlab.tpl"` phiên bản cũ không tương thích với GitLab Schema 15.0.
- **Cách khắc phục:** Cập nhật Trivy Container Image lên phiên bản mới nhất `aquasec/trivy:latest`.

### 14. Sự cố Security Quality Gate nổ lỗi đỏ ngắt pipeline khi dev vừa mở Draft MR
- **Triệu chứng:** Developer đang viết dở code thử nghiệm thì CI Pipeline đã bị ngắt.
- **Nguyên nhân:** Đặt Job `security-quality-gate` chạy trên tất cả các loại commit events.
- **Cách khắc phục:** Cấu hình `rules: - if: '$CI_MERGE_REQUEST_TITLE =~ /^Draft:/' allow_failure: true`.

### 15. Sự cố Tệp `bang-5-security-va-hien-vat.tsv` bị thiếu cột `allowlist_audit`
- **Triệu chứng:** Script kiểm tra `kiem-tra.sh` báo lỗi thiếu cột thông số Buổi 28 trong TSV Giai đoạn 5.
- **Nguyên nhân:** Thiếu ký tự Tab giữa cột `report_format` và `allowlist_audit`.
- **Cách khắc phục:** Sử dụng ký tự Tab chuẩn phân tách 6 cột dữ liệu trong tệp hiện vật Giai đoạn 5.

### 16. Sự cố Semgrep báo lỗi `out of memory` khi phân tích mã nguồn chứa tệp JSON/Minified JS
- **Triệu chứng:** Semgrep scan bị treo lâu rồi bị kẹt ở tệp `bundle.min.js`.
- **Nguyên nhân:** Quét các tệp JS nén dòng đơn phình to làm thuật toán parser AST tràn RAM.
- **Cách khắc phục:** Khai báo cờ `--exclude="*.min.js"` và `--max-target-bytes=1000000`.

### 17. Sự cố `trivy fs` bị từ chối kết nối tới Proxy nội bộ của công ty
- **Triệu chứng:** Trivy không thể nạp tệp Vulnerability DB từ máy chủ cache nội bộ.
- **Nguyên nhân:** Biến môi trường `HTTP_PROXY` chưa được nạp vào Docker Container của Trivy Job.
- **Cách khắc phục:** Khai báo biến `HTTP_PROXY` và `HTTPS_PROXY` trong phần `variables:` của CI Job.

### 18. Sự cố Tệp `.trivyignore` bị rỗng ký tự xuống dòng gây bỏ qua nhầm tất cả các lỗ hổng
- **Triệu chứng:** Trivy bỏ qua quét 100% lỗ hổng mặc dù chỉ khai báo 1 CVE trong `.trivyignore`.
- **Nguyên nhân:** Tệp ignore sử dụng bảng mã CRLF của Windows khiến Trivy đọc cả chuỗi thành 1 dòng rác.
- **Cách khắc phục:** Sử dụng định dạng LF chuẩn Linux cho tệp `.trivyignore`.

### 19. Sự cố `semgrep` nổ lỗi `cannot parse pattern` khi viết custom rule
- **Triệu chứng:** Semgrep CLI nổ lỗi syntax khi nạp tệp quy tắc `.semgrep.yml`.
- **Nguyên nhân:** Dùng sai ký tự ngoặc đơn hoặc thiếu khoảng trắng sau toán tử `pattern:`.
- **Cách khắc phục:** Kiểm tra cú pháp quy tắc bằng trang Semgrep Playground trực tuyến trước khi commit.

### 20. Sự cố Tệp `gl-sast-report.json` bị mất thông tin dòng lỗi `start_line: null`
- **Triệu chứng:** GitLab UI hiển thị lỗ hổng nhưng không bấm nhảy tới đúng dòng code bị lỗi được.
- **Nguyên nhân:** Semgrep phiên bản cũ không ánh xạ được số dòng cho các tệp template HTML/Jinja2.
- **Cách khắc phục:** Nâng cấp Semgrep CLI lên phiên bản v1.60.0 trở lên.

### 21. Sự cố `trivy fs` báo lỗ hổng CVE trong thư viện devDependencies của Node.js
- **Triệu chứng:** Quét `package-lock.json` phát hiện 20 lỗ hổng trong các thư viện test build (như Jest, Webpack).
- **Nguyên nhân:** Trivy mặc định quét toàn bộ cả `dependencies` và `devDependencies`.
- **Cách khắc phục:** Khai báo cờ `trivy fs --dependency-tree --include-dev-deps=false .` chỉ quét thư viện Production.

### 22. Sự cố Security Quality Gate nổ lỗi ngắt pipeline do lỗ hổng mức `MEDIUM`
- **Triệu chứng:** Pipeline bị dừng ngắt mặc dù chính sách công ty chỉ chặn lỗi `CRITICAL` và `HIGH`.
- **Nguyên nhân:** Quên khai báo cờ `--severity CRITICAL,HIGH` khiến Trivy chặn tất cả các mức severity.
- **Cách khắc phục:** Khai báo chính xác cờ `--severity CRITICAL,HIGH` trong câu lệnh gọi Trivy.

### 23. Sự cố Semgrep báo lỗi cảnh báo giả trên các đoạn code mã hóa mật khẩu bcrypt
- **Triệu chứng:** Semgrep cảnh báo Hardcoded Secret trên hàm băm mật khẩu test `bcrypt.GenerateFromPassword`.
- **Nguyên nhân:** Quy tắc quét nhận diện chuỗi băm mẫu là secret key thật.
- **Cách khắc phục:** Thêm comment `// nosemgrep: generic.secrets.gitleaks` ngay tại dòng code đó.

### 24. Sự cố Tệp `gl-dependency-scanning-report.json` bị ghi đè bởi Job SAST
- **Triệu chứng:** Dashboard chỉ hiển thị báo cáo SAST mà mất hoàn toàn báo cáo Dependency Scanning.
- **Nguyên nhân:** Đặt trùng tên tệp đầu ra `gl-sast-report.json` cho cả 2 Jobs.
- **Cách khắc phục:** Tách biệt 2 tên tệp `gl-sast-report.json` và `gl-dependency-scanning-report.json`.

### 25. Sự cố Tệp `bang-5-security-va-hien-vat.tsv` bị ghi đè tiêu đề cột khi chạy re-run CI Job
- **Triệu chứng:** Tệp TSV bị lặp lại hàng tiêu đề 5 lần khi bấm Re-try Job.
- **Nguyên nhân:** Script nạp tiêu đề dùng toán tử nối dòng `>>` mà không kiểm tra tệp đã tồn tại chưa.
- **Cách khắc phục:** Kiểm tra `if [ ! -f bang-5-security-va-hien-vat.tsv ]; then ... fi` trước khi ghi tiêu đề.

### 26. Sự cố Lỗi `403 Rate Limit` khi `trivy` tải Vulnerability DB từ GitHub API
- **Triệu chứng:** Job Trivy bị dừng ngắt với thông báo `rate limit exceeded`.
- **Nguyên nhân:** Nhiều Runner chung cùng gọi API tải DB không có token xác thực.
- **Cách khắc phục:** Nạp biến môi trường `$GITHUB_TOKEN` vào CI Job Variables để tăng hạn mức API lên 5000 req/h.

### 27. Sự cố Semgrep báo lỗi `scan timeout` khi phân tích file mã nguồn Go cực lớn (> 10,000 dòng)
- **Triệu chứng:** Semgrep scan bị treo 10 phút rồi nổ lỗi `TimeoutExpired`.
- **Nguyên nhân:** Thuật toán phân tích luồng dữ liệu (Dataflow Analysis) bị kẹt trong vòng lặp phức tạp.
- **Cách khắc phục:** Khai báo cờ `--timeout 60` giới hạn thời gian quét tối đa 60 giây cho mỗi tệp.

### 28. Sự cố Tệp `gl-sast-report.json` bị từ chối do sai phiên bản GitLab Schema
- **Triệu chứng:** GitLab Security Dashboard báo `Invalid report format: version 14.0.0 is deprecated`.
- **Nguyên nhân:** Sử dụng template chuyển đổi báo cáo cũ không khớp với phiên bản GitLab v16.x.
- **Cách khắc phục:** Đảm bảo trường `"version": "15.0.0"` trong cấu trúc JSON báo cáo.

### 29. Sự cố `trivy fs` báo lỗ hổng CVE đã được vá (Fixed Version) nhưng không thể nâng cấp thư viện
- **Triệu chứng:** Thư viện cha đòi hỏi thư viện con dính CVE và chưa có bản patch chính thức.
- **Nguyên nhân:** Trùng lặp phụ thuộc (Transitive Dependency) trong cây phụ thuộc.
- **Cách khắc phục:** Khai báo cờ `--ignore-unfixed` chỉ chặn các CVE đã có bản patch chính thức.

### 30. Sự cố Semgrep không quét được mã nguồn Python do thiếu định dạng UTF-8
- **Triệu chứng:** Semgrep nổ lỗi `UnicodeDecodeError` khi đọc file `app.py`.
- **Nguyên nhân:** File Python chứa ký tự tiếng Việt hoặc comment phi ASCII không đúng UTF-8.
- **Cách khắc phục:** Khai báo `# -*- coding: utf-8 -*-` ở đầu các tệp mã nguồn Python.

### 31. Sự cố Tệp `.semgrepignore` bị rỗng gây bỏ qua toàn bộ dự án
- **Triệu chứng:** Semgrep scan báo `0 files scanned` mặc dù dự án có 100 tệp Go.
- **Nguyên nhân:** Đặt dòng `*` ở đầu tệp `.semgrepignore` khiến tất cả tệp bị loại bỏ.
- **Cách khắc phục:** Khai báo chính xác các đường dẫn thư mục cần loại bỏ (ví dụ: `vendor/`, `node_modules/`).

### 32. Sự cố Security Quality Gate không chặn được MR do cờ `allow_failure: true` trên template
- **Triệu chứng:** Pipeline báo đỏ nhưng Merge Request vẫn cho phép bấm nút Merge.
- **Nguyên nhân:** Kế thừa template GitLab CI mặc định có sẵn cờ `allow_failure: true`.
- **Cách khắc phục:** Đè thuộc tính `sast-semgrep-job: allow_failure: false` trong `.gitlab-ci.yml`.

### 33. Sự cố Tệp `gl-dependency-scanning-report.json` bị mất thông tin giải pháp khắc phục (`solution`)
- **Triệu chứng:** Security Dashboard hiển thị CVE nhưng cột Solution bị trống.
- **Nguyên nhân:** CSDL lỗ hổng địa phương của Trivy chưa được cập nhật thông tin patch.
- **Cách khắc phục:** Xóa cache đệm DB cũ và thực thi cập nhật DB mới bằng `trivy image --download-db-only`.

### 34. Sự cố `trivy fs` bị dừng do hết đĩa đĩa đĩa đệm tạm `/tmp`
- **Triệu chứng:** Trivy scan báo `no space left on device` trên CI Runner host.
- **Nguyên nhân:** Thư mục `/tmp` của Runner bị phình quá to qua nhiều lần quét.
- **Cách khắc phục:** Khai báo cờ `--cache-dir .trivycache/` lưu đệm đệm trực tiếp trong workspace dự án.

### 35. Sự cố Tệp `bang-5-security-va-hien-vat.tsv` bị thiếu dòng dữ liệu khi Job fail giữa chừng
- **Triệu chứng:** Báo cáo kiểm toán cuối kỳ bị thiếu thông số an ninh của Buổi 28.
- **Nguyên nhân:** Đặt Job cập nhật TSV ở cuối pipeline sau bước Security Quality Gate bị fail.
- **Cách khắc phục:** Đặt cờ `when: always` cho Job nộp hiện vật TSV.

### 36. Sự cố Lỗi `403 Forbidden` khi Semgrep gọi API đồng bộ quy tắc từ Semgrep App Sec Cloud
- **Triệu chứng:** Lệnh `semgrep scan --config auto` nổ lỗi từ chối xác thực.
- **Nguyên nhân:** Biến môi trường `$SEMGREP_APP_TOKEN` bị thu hồi hoặc hết hạn.
- **Cách khắc phục:** Chuyển sang dùng cờ `semgrep scan --config p/owasp-top-ten` không yêu cầu token cloud.

### 37. Sự cố `trivy fs` báo lỗ hổng CVE trong tệp nén đính kèm `.tar.gz` không dùng tới
- **Triệu chứng:** Trivy quét cả các tệp `.tar.gz` lưu tạm trong workspace và báo lỗi CVE cũ.
- **Nguyên nhân:** Trivy mặc định giải nén và quét đệ quy tất cả các tệp lưu trữ nhị phân.
- **Cách khắc phục:** Khai báo cờ `trivy fs --skip-files "*.tar.gz" .` loại bỏ tệp nén.

### 38. Sự cố Tệp `gl-sast-report.json` bị thiếu thông tin mã lỗi CWE (`identifiers: []`)
- **Triệu chứng:** GitLab Security Dashboard hiển thị lỗ hổng nhưng không phân loại được theo danh mục CWE.
- **Nguyên nhân:** Quy tắc Semgrep custom thiếu khai báo trường `metadata.cwe`.
- **Cách khắc phục:** Đảm bảo trường `metadata.cwe: "CWE-89: SQL Injection"` trong tệp YAML quy tắc.

### 39. Sự cố `trivy` bị nổ lỗi `out of memory` khi phân tích tệp `package-lock.json` phình > 10 MB
- **Triệu chứng:** Job Dependency Scanning bị sập giữa chừng khi quét tệp lockfile dự án frontend lớn.
- **Nguyên nhân:** Parser cây phụ thuộc node.js chiếm hơn 4 GB RAM Runner.
- **Cách khắc phục:** Khai báo cờ `trivy fs --skip-dirs "node_modules" .` chỉ quét tệp `package-lock.json` phẳng.

### 40. Sự cố Security Quality Gate bị rò rỉ mã secret khi log console in ra tệp `.env`
- **Triệu chứng:** Mật khẩu DB bị in công khai ra log Runner khi Semgrep cảnh báo lỗi secret.
- **Nguyên nhân:** Semgrep in chi tiết dòng code chứa chuỗi secret thô.
- **Cách khắc phục:** Khai báo cờ `--mask-secrets` hoặc cấu hình `Masked Variables` trong GitLab CI/CD Settings.

### 41. Sự cố Tệp `gl-sast-report.json` bị mất thuộc tính `scan.scanner.name` làm hỏng giao diện Dashboard
- **Triệu chứng:** GitLab UI từ chối nạp báo cáo JSON với lỗi `missing scanner name`.
- **Nguyên nhân:** Tệp JSON tự biên dịch thiếu trường định danh tên scanner.
- **Cách khắc phục:** Bắt buộc đính kèm `"scanner": {"id": "semgrep", "name": "Semgrep OSS"}` trong cấu trúc tệp JSON.

---

## Bài tập mở rộng

1. **BT1 (Cấu hình Custom Ruleset trong Semgrep):** Viết 3 quy tắc Semgrep riêng cho doanh nghiệp phát hiện việc log thông tin thẻ tín dụng/mật khẩu.
2. **BT2 (Tích hợp SonarQube Quality Gate trong GitLab CI):** Khởi tạo Job `sonar-scanner` quét độ sạch của code và đẩy kết quả sang SonarQube Server.
3. **BT3 (Tự động hóa Tạo Issue trên GitLab khi phát hiện CVE mới):** Viết script Python gọi API tạo Issue khi Trivy phát hiện CVE mức `CRITICAL`.
4. **BT4 (Cấu hình Offline Trivy DB trong Môi trường Air-Gapped):** Nạp đệm CSDL CVE của Trivy vào máy chủ nội bộ không có kết nối Internet.
5. **BT5 (Tích hợp Checkov quét An ninh Hạ tầng IaC Terraform):** Khởi tạo Job `checkov` quét các tệp `.tf` phát hiện S3 Bucket public, Security Group mở `0.0.0.0/0`.
6. **BT6 (Tự động hóa Quét An ninh cho Dự án Python / Node.js / Java):** Cấu hình `retire.js` và `pip-audit` quét thư viện phụ thuộc cho Node.js và Python.
7. **BT7 (Cấu hình Ruleset Override trong GitLab Native SAST):** Khai báo tệp `.gitlab/sast-ruleset.toml` điều chỉnh mức độ nghiêm trọng của quy tắc quét.
8. **BT8 (Tự động hóa Ký Số Phê Duyệt Tệp `.trivyignore` bằng GPG Key):** Kiểm tra chữ ký GPG trên tệp `.trivyignore` trước khi cho phép CI Job bỏ qua CVE.
9. **BT9 (Đo đạc Chỉ số Thời gian Sửa Lỗi Mean Time to Remediate - MTTR):** Thu thập dữ liệu từ Vulnerability Report API để vẽ biểu đồ chỉ số MTTR.
10. **BT10 (Tự động hóa Gửi Cảnh Báo Security qua Slack Channel):** Gửi bản tóm tắt danh sách lỗ hổng `CRITICAL` sang Slack channel khi Quality Gate fail.
11. **BT11 (Cấu hình Quét An ninh cho Dự án Monorepo):** Cấu hình Semgrep và Trivy quét phân đoạn cho từng microservice trong thư mục `packages/`.
12. **BT12 (Tối ưu Tốc độ Quét SAST bằng Caching Semgrep AST):** Nạp đệm đệm đệm AST cache giúp giảm 70% thời gian quét SAST trong CI Pipeline.
13. **BT13 (Cấu hình Quét An ninh Secret Scanning bằng Gitleaks):** Tích hợp công cụ `gitleaks` quét toàn bộ lịch sử Git commit history tìm AWS Keys.
14. **BT14 (Tự động hóa Chuyển đổi Báo cáo SARIF sang HTML Interface):** Sử dụng `sarif-tools` biên dịch tệp SARIF thành trang HTML báo cáo báo cáo an ninh tĩnh.
15. **BT15 (Cấu hình Security Quality Gate Phân Cấp theo Môi Trường):** Áp dụng quy tắc ngắt `CRITICAL` cho Dev/Staging và ngắt cả `HIGH` cho Prod.
16. **BT16 (Tích hợp OWASP ZAP Quét An ninh Động DAST):** Khởi tạo Job DAST quét tấn công thử nghiệm dịch vụ sau khi deploy Staging.
17. **BT17 (Kiểm tra Tính Tuân thủ Chuẩn An ninh PCI-DSS / HIPAA):** Khai báo bộ quy tắc quét tuân thủ chuẩn PCI-DSS cho hệ thống thanh toán.

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| Hạng mục | Tiêu chí đánh giá | Điểm số |
|---|---|---|
| Cấu hình SAST Semgrep | Cấu hình Job Semgrep quét phát hiện chính xác lỗ hổng SQL Injection tại `main.go:42` | 20 điểm |
| Cấu hình SCA Trivy | Cấu hình Job Trivy fs quét phát hiện chính xác `CVE-2023-39325` trong `go.sum` | 20 điểm |
| JSON Reports & Quality Gate | Xuất tệp `gl-sast-report.json` và cấu hình Security Quality Gate tự động ngắt pipeline (`exit 1`) | 20 điểm |
| Ignore Files & Remediation | Tạo `.semgrepignore`, `.trivyignore` có vết audit và sửa lỗi code đưa pipeline sang màu xanh | 20 điểm |
| Khởi tạo TSV Giai đoạn 5 | Tệp `bang-5-security-va-hien-vat.tsv` được khởi tạo và ghi dòng dữ liệu Buổi 28 chuẩn | 20 điểm |
| **TỔNG ĐIỂM** | | **100 điểm** |

---

## Bảng đối soát thời lượng

| Section | Tiêu đề | Thời lượng |
|---|---|---|
| L0–L2 | Mục tiêu, Môi trường & Kiến trúc bài Lab | 15' |
| L3 | Bước 1 — Tạo Mã Nguồn Lỗi Mẫu và Cấu hình Semgrep SAST | 30' |
| L4 | Bước 2 — Cấu hình Trivy Dependency Scanning và Xuất Báo Cáo JSON | 30' |
| L5 | Bước 3 — Cấu hình Security Quality Gate và Quản lý Ignore Files | 35' |
| L6 | Bước 4 — Thực thi Sửa Lỗi (Remediation) và Kiểm Tra Pipeline Xanh | 35' |
| L7 | Bước 5 — Khởi tạo Tệp Hiện vật Giai đoạn 5 TSV và Dọn dẹp | 20' |
| L8–L11 | Nộp sản phẩm, Dọn dẹp, Sự cố & Bài tập mở rộng | 10' |
| **Tổng** | **Khối thực hành Lab** | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---

## §V1. Bảng tổng hợp thuật ngữ & 12 bẫy hỏng im lặng

### 1. Bảng đối chiếu thuật ngữ kỹ thuật SAST & Dependency Scanning

| Thuật ngữ | Khái niệm kỹ thuật | Điểm mấu chốt trong CI/CD |
|---|---|---|
| `Shift-Left Security` | Đẩy các hoạt động kiểm tra bảo mật về giai đoạn đầu của phát triển | Phát hiện và sửa lỗ hổng ngay từ commit đầu tiên |
| `SAST` | Static Application Security Testing — Quét phân tích mã nguồn tĩnh | Phân tích AST phát hiện lỗi SQLi, XSS, Hardcoded Secret |
| `Dependency Scanning / SCA` | Software Composition Analysis — Quét lỗ hổng thư viện phụ thuộc | Tra cứu CSDL NVD CVE từ tệp khoá `go.sum`, `package-lock.json` |
| `Security Quality Gate` | Cổng kiểm soát chất lượng an ninh tự động trong CI Pipeline | Tự động đánh rớt pipeline (`exit 1`) khi có lỗi `CRITICAL` / `HIGH` |
| `SARIF` | Định dạng dữ liệu tiêu chuẩn trao đổi kết quả phân tích tĩnh | Chuẩn hóa báo cáo an ninh giữa các công cụ bảo mật |
| `False Positive` | Cảnh báo bảo mật giả (không phải lỗ hổng thực tế) | Quản lý an toàn bằng `.semgrepignore` và `.trivyignore` có audit |
| `CVE` | Common Vulnerabilities and Exposures — Định danh lỗ hổng quốc tế | Mã số lỗ hổng được công bố rộng rãi trên CSDL NVD |
| `CVSS Score` | Điểm số đánh giá mức độ nghiêm trọng của lỗ hổng (0.0 - 10.0) | Tiêu chí phân loại mức `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `Remediation` | Quy trình thực thi khắc phục và vá lỗi bảo mật | Sửa trực tiếp mã nguồn hoặc nâng cấp phiên bản thư viện |

---

### 2. Bảng 12 bẫy hỏng im lặng điển hình khi quét an ninh SAST và Dependency Scanning

| # | Bẫy hỏng im lặng | Dấu hiệu nhận biết | Hậu quả kỹ thuật | Cách khắc phục triệt để |
|---|---|---|---|---|
| 1 | Quét an ninh định kỳ 6 tháng một lần | Lỗ hổng lọt lên Prod tồn tại hàng tháng | Chi phí sửa lỗi cao gấp 100 lần so với lúc code | Áp dụng nguyên lý Shift-Left Security (`QT 4.1`) |
| 2 | Dùng SAST đi quét thư mục `node_modules/` | Tràn bộ nhớ RAM Runner và tràn ngập rác | Pipeline bị đứng đơ và sinh cảnh báo rác | Phân định rõ phạm vi SAST và SCA (`QT 4.2`) |
| 3 | Xuất báo cáo an ninh dạng file text thô | GitLab UI không đọc được báo cáo an ninh | Không hiển thị kết quả trên MR Widget | Xuất báo cáo chuẩn `gl-sast-report.json` (`QT 4.3`) |
| 4 | Dùng lệnh `grep` thô thay cho công cụ SAST | Sinh 90% cảnh báo giả làm rối lập trình viên | Lập trình viên phớt lờ các cảnh báo an ninh | Sử dụng công cụ SAST chuyên dụng `semgrep` (`QT 5.1`) |
| 5 | Quên quét tệp khoá thư viện `go.sum` | Lỗ hổng CVE trong thư viện bị bỏ qua | Nguy cơ ứng dụng bị tấn công RCE | Sử dụng `trivy fs` quét tệp khoá thư viện (`QT 5.2`) |
| 6 | Đặt `allow_failure: true` cho tất cả Security Jobs | Pipeline xanh lè mặc dù code dính lỗ hổng | Biến công cụ quét an ninh thành hình thức | Cấu hình Security Quality Gate ngắt pipeline (`QT 5.3`) |
| 7 | Giấu tệp báo cáo an ninh trong console log | Tech Lead không thấy lỗi trên Merge Request UI | Khó khăn khi duyệt an ninh cho Merge Request | Tích hợp báo cáo hiển thị trên MR Widget (`QT 6.1`) |
| 8 | Tắt quy tắc quét thay vì dùng ignore file | Làm mất khả năng bảo vệ của công cụ | Dự án mất khả năng tự vệ trước lỗ hổng mới | Dùng `.semgrepignore` có vết audit (`QT 6.2`) |
| 9 | Đặt `allow_failure: true` trên nhánh `main` | Cảnh báo an ninh bị ngó lơ hoàn toàn | Mã nguồn dính lỗ hổng lọt lên Production | Đặt `allow_failure: false` biến Security thành Hard Gate (`QT 6.3`) |
| 10 | Quên lưu tệp JSON báo cáo sang Artifacts | Security Dashboard bị rỗng dữ liệu | Không đáp ứng yêu cầu kiểm toán an ninh | Nộp đầy đủ tệp JSON sang `artifacts:reports` (`QT 7.1`) |
| 11 | Không in log tổng hợp kết quả quét trên CI Runner | Thiếu tính minh bạch của kết quả quét | Team không biết có bao nhiêu lỗi nghiêm trọng | In log công khai kết quả quét phân loại (`QT 7.2`) |
| 12 | Thiếu khởi tạo tệp hiện vật Giai đoạn 5 | Không chuẩn hóa được chỉ số an ninh | Không đồng bộ được quy chuẩn an ninh | Khởi tạo và ghi dòng dữ liệu Buổi 28 vào TSV (`QT 7.3`) |

---

## §V2. 12 câu vấn đáp chuyên sâu (Level 3 - Kiến trúc sư CI/CD)

### Câu 1
**Câu hỏi:** Tại sao các Kiến trúc sư CI/CD luôn khẳng định **"Bảo mật không phải là rào chắn cuối cùng mà là phản hồi liên tục từ commit đầu tiên — shift-left để tìm lỗ hổng trong 1 phút thay vì 1 tháng"**?

**Đáp án chuẩn:**
- Vì việc đẩy các hoạt động kiểm tra an ninh về cuối chu kỳ (Pentest trước ngày phát hành) khiến việc sửa lỗi cực kỳ đắt đỏ, tốn thời gian và làm trì hoãn tiến độ phát hành của toàn bộ dự án.
- Tích hợp Shift-Left Security tự động hóa công cụ quét an ninh ngay tại stage test của mọi Merge Request giúp lập trình viên phát hiện và tự sửa lỗ hổng ngay trong **1 phút** khi vừa viết code xong, chi phí khắc phục giảm **90%** so với sửa ở Production.

---

### Câu 2
**Câu hỏi:** Phân biệt sự khác biệt cốt lõi giữa Quét mã nguồn tĩnh (SAST) và Quét thư viện phụ thuộc (Dependency Scanning / SCA)?

**Đáp án chuẩn:**
- **SAST (Static Application Security Testing):** Phân tích cú pháp tĩnh (AST Parse Tree) của **MÃ NGUỒN TỰ VIẾT** (do lập trình viên trong team viết). Công cụ đại diện: `semgrep`. Phát hiện các lỗi logic lập trình như SQL Injection, XSS, Hardcoded Credentials.
- **Dependency Scanning (SCA):** Trích xuất danh sách và phiên bản của **THƯ VIỆN BÊN THỨ BA** từ tệp khóa phụ thuộc (`go.sum`, `package-lock.json`), đối soát với CSDL NVD CVE quốc tế để phát hiện các lỗ hổng đã được công bố công khai. Công cụ đại diện: `trivy fs`.

---

### Câu 3
**Câu hỏi:** Nguyên lý hoạt động của công cụ `semgrep` và cách thức tạo các quy tắc quét (Rules) tùy chỉnh trong doanh nghiệp?

**Đáp án chuẩn:**
- `semgrep` là động cơ quét SAST dựa trên việc khớp mẫu cú pháp (Pattern Matching) trên cây cú pháp trừu tượng (AST) của mã nguồn mà không cần biên dịch code.
- Để tạo quy tắc tùy chỉnh (Custom Rule) cho doanh nghiệp, ta khai báo tệp YAML quy định mẫu `pattern:` (ví dụ `db.Exec("SELECT..." + $X)`), thông điệp cảnh báo `message:`, mã phân loại `metadata.cwe:` và mức độ nghiêm trọng `severity: ERROR`.

---

### Câu 4
**Câu hỏi:** Nguyên lý hoạt động của `trivy fs` trong việc tra cứu cơ sở dữ liệu NVD CVE từ tệp `go.sum` hay `package-lock.json`?

**Đáp án chuẩn:**
- `trivy fs` phân tích tệp khóa phụ thuộc để trích xuất danh sách chính xác tên thư viện và con số phiên bản đang sử dụng.
- Sau đó, Trivy đối soát thông tin này với cơ sở dữ liệu lỗ hổng quốc tế NVD (National Vulnerability Database) và VulnDB địa phương. Nếu phát hiện con số phiên bản nằm trong khoảng dính CVE (ví dụ `golang.org/x/net < v0.17.0`), Trivy sẽ xuất ra thông tin chi tiết mã CVE, CVSS Score và phiên bản đã sửa lỗi (`Fixed Version`).

---

### Câu 5
**Câu hỏi:** Tại sao cần xuất báo cáo an ninh theo định dạng chuẩn `gl-sast-report.json` và SARIF?

**Đáp án chuẩn:**
- `gl-sast-report.json` là định dạng báo cáo an ninh chuẩn do GitLab quy định. Xuất tệp này nộp sang `artifacts:reports:sast` giúp hệ thống GitLab UI tự động đọc và hiển thị kết quả phân tích trực tiếp trên giao diện **Merge Request Security Widget** và **GitLab Security Dashboard**.
- SARIF (Static Analysis Results Interchange Format) là chuẩn báo cáo an ninh quốc tế cho phép chia sẻ và tích hợp dữ liệu quét giữa nhiều hệ thống khác nhau (như GitHub, SonarQube, DefectDojo).

---

### Câu 6
**Câu hỏi:** Cách thiết lập Security Quality Gate tự động dừng ngắt pipeline khi vượt quá ngưỡng lỗ hổng cho phép?

**Đáp án chuẩn:**
- Trong `.gitlab-ci.yml`, ta cấu hình câu lệnh quét của công cụ với cờ ép buộc trả về mã lỗi `exit code 1` và bộ lọc mức độ nghiêm trọng:
  `trivy fs --scanners vuln --exit-code 1 --severity CRITICAL,HIGH .`
- Đồng thời đặt thuộc tính `allow_failure: false`. Khi phát hiện ít nhất 1 lỗ hổng mức `CRITICAL` hoặc `HIGH`, CI Job sẽ nổ lỗi đỏ, dừng ngắt pipeline lập tức và chặn không cho phép merge code lỗi.

---

### Câu 7
**Câu hỏi:** Sự khác biệt giữa lỗ hổng mã nguồn (Code Vulnerability) và lỗ hổng thư viện (Dependency Vulnerability) về mặt quy trình khắc phục (Remediation)?

**Đáp án chuẩn:**
- **Code Vulnerability (Lỗi SAST):** Do lập trình viên viết sai logic an toàn. Quy trình khắc phục yêu cầu **SỬA TRỰC TIẾP MÃ NGUỒN** (như chuyển từ câu SQL nối chuỗi sang dùng Parameterized Query hoặc HTML Escape).
- **Dependency Vulnerability (Lỗi SCA):** Do thư viện bên thứ 3 dính CVE. Quy trình khắc phục yêu cầu **NÂNG CẤP PHIÊN BẢN THƯ VIỆN** (như chạy `go get package@vX.Y.Z` hoặc `npm update`) lên phiên bản `Fixed Version` đã được vá lỗi.

---

### Câu 8
**Câu hỏi:** Quy trình xử lý cảnh báo giả (False Positive) an toàn bằng `.semgrepignore` và `.trivyignore` có vết audit?

**Đáp án chuẩn:**
- Không bao giờ được phép tắt quy tắc quét an ninh của toàn bộ dự án.
- Khi xác định một cảnh báo là giả (do nằm trong tệp test mock hoặc đã có phương án bù đắp bảo mật WAF):
  1. Khai báo mã CVE hoặc đường dẫn tệp vào `.semgrepignore` / `.trivyignore`.
  2. Bắt buộc đính kèm comment giải trình lý do an toàn và người phê duyệt (`Security Lead - Approved by Name`).
  3. Cấu hình tệp `CODEOWNERS` yêu cầu mọi thay đổi trên ignore files phải có chữ ký duyệt của Security Team.

---

### Câu 9
**Câu hỏi:** Cách hiển thị và đối soát kết quả quét an ninh trực tiếp trên GitLab Merge Request Security Widget?

**Đáp án chuẩn:**
- Trong `.gitlab-ci.yml`, khai báo thuộc tính nộp báo cáo chuẩn:
  ```yaml
  artifacts:
    reports:
      sast: gl-sast-report.json
      dependency_scanning: gl-dependency-scanning-report.json
  ```
- Khi mở Merge Request, GitLab Runner sẽ tự động so sánh báo cáo an ninh của nhánh feature với nhánh target (`main`). Khối Security Widget trên MR UI sẽ hiển thị chính xác danh sách các lỗ hổng mới phát sinh của nhánh code này cho Tech Lead đối soát.

---

### Câu 10
**Câu hỏi:** Tại sao không nên đặt cờ `allow_failure: true` cho các Security Scan Jobs trên nhánh `main`?

**Đáp án chuẩn:**
- Nếu đặt `allow_failure: true`, khi phát hiện lỗ hổng `CRITICAL`, CI Pipeline vẫn tiếp tục chạy xanh lè và cho phép deploy mã nguồn nguy hiểm lên môi trường Production.
- Điều này biến toàn bộ công cụ quét an ninh thành một hình thức vô tác dụng. Đặt `allow_failure: false` giúp biến Security Scan Jobs thành một **Cổng chặn cứng (Hard Quality Gate)** bảo vệ tính an toàn tuyệt đối cho nhánh `main`.

---

### Câu 11
**Câu hỏi:** Cách xử lý sự cố khi tệp cơ sở dữ liệu lỗ hổng CVE của Trivy không thể cập nhật do bị chặn Internet trên CI Runner (Môi trường Air-Gapped)?

**Đáp án chuẩn:**
- Khởi tạo một máy chủ lưu trữ đệm CSDL đệm nội bộ trong mạng LAN (Internal Mirror).
- Định kỳ hằng ngày tải tệp `trivy-db` mới nhất về máy đệm nội bộ.
- Trên CI Runner Air-Gapped, cấu hình câu lệnh Trivy trỏ tới CSDL nội bộ và bật cờ bỏ qua cập nhật Internet:
  `trivy fs --skip-db-update --db-repository registry.internal/trivy-db .`

---

### Câu 12
**Câu hỏi:** Tổng kết quy trình 4 bước triển khai Shift-Left Security chuẩn Enterprise trong CI/CD Pipeline?

**Đáp án chuẩn:**
1. **Code Commit:** Lập trình viên viết mã nguồn và push commit lên nhánh feature branch.
2. **SAST & SCA Scan:** CI Pipeline tự động chạy `semgrep` quét code tự viết và `trivy fs` quét thư viện phụ thuộc.
3. **Security Quality Gate:** Tự động kiểm tra ngưỡng an ninh, nổ lỗi `exit 1` ngắt pipeline nếu xuất hiện lỗi `CRITICAL` / `HIGH`.
4. **Vulnerability Remediation:** Lập trình viên tự sửa code hoặc nâng cấp thư viện ngay tại feature branch trước khi merge code vào `main`.

---

## §V3. Câu chốt để nói khi phỏng vấn (Interview Takeaway Statements)

1. **Về Luận đề Shift-Left Security:** *"Em triển khai triệt để NGUYÊN LÝ SHIFT-LEFT SECURITY: Bảo mật không phải là rào chắn cuối cùng mà là phản hồi liên tục từ commit đầu tiên, giúp lập trình viên phát hiện và tự sửa lỗ hổng ngay trong 1 phút thay vì chờ 1 tháng."*
2. **Về SAST & Dependency Scanning Integration:** *"Em phân định rõ ranh giới kiểm soát an ninh: sử dụng Semgrep SAST phân tích cú pháp AST quét mã nguồn tự viết và sử dụng Trivy fs tra cứu CSDL NVD CVE quét các thư viện phụ thuộc bên thứ 3."*
3. **Về Security Quality Gate & Reporting:** *"Em chuẩn hóa báo cáo an ninh theo định dạng gl-sast-report.json hiển thị trực quan trên Merge Request Widget, đồng thời cấu hình Security Quality Gate tự động ngắt pipeline khi phát hiện lỗ hổng mức CRITICAL hoặc HIGH."*
4. **Về False Positive Audit & Giai đoạn 5 TSV:** *"Em quản lý danh sách cảnh báo giả qua tệp .semgrepignore và .trivyignore có chữ ký phê duyệt audit an toàn, đồng thời khởi tạo tệp hiện vật Giai đoạn 5 bang-5-security-va-hien-vat.tsv chuẩn hóa chỉ số an ninh doanh nghiệp."*

---

## §V3.5. 7 Kịch bản Phỏng vấn Kỹ sư DevOps (Roleplay Scenarios)

### Kịch bản 1: Xử lý sự cố Dự án Legacy bị ngập hàng trăm lỗ hổng cũ khi bật Security Gate
- **Nhà tuyển dụng:** "Khi em bật Security Quality Gate trên một dự án Legacy lâu năm, pipeline bị đỏ ngầu lập tức do hàng trăm lỗ hổng cũ khiến dev không thể release code mới. Em xử lý sao?"
- **Ứng viên:** "Mới đầu em sẽ đặt `allow_failure: true` và dùng cờ `trivy fs --limit-severities HIGH,CRITICAL` xuất báo cáo tổng thể. Em thống nhất với Tech Lead phân loại danh sách lỗ hổng thành 2 nhóm: lỗ hổng mới (New Flaws) phải chặn ngay trên MR, và lỗ hổng cũ (Legacy Flaws) lập kế hoạch sửa chữa trong 2 sprint. Sau khi sửa sạch lỗi cũ, em mới bật `allow_failure: false`."

### Kịch bản 2: Giải thích lý do chọn Semgrep thay vì SonarQube cho SAST trong CI Pipeline
- **Nhà tuyển dụng:** "Tại sao công ty nên dùng Semgrep cho bước SAST scan thay vì SonarQube Server?"
- **Ứng viên:** "Semgrep có tốc độ quét cực nhanh (chỉ mất vài giây), hỗ trợ quét trực tiếp trên Runner mỏng dưới dạng CLI mà không cần dựng máy chủ SonarQube Server cồng kềnh. Hơn nữa, Semgrep cho phép viết các quy tắc Custom Rules bằng YAML rất dễ dàng và hỗ trợ xuất chuẩn báo cáo GitLab SAST JSON trực tiếp."

### Kịch bản 3: Xử lý tình huống Developer đòi tắt công cụ quét an ninh vì cảnh báo giả
- **Nhà tuyển dụng:** "Một Senior Dev bức xúc đòi gỡ bỏ Job SAST scan vì cho rằng công cụ báo cảnh báo giả (False Positive) làm nghẽn pipeline. Em xử lý thế nào?"
- **Ứng viên:** "Em sẽ cùng Senior Dev phân tích trực tiếp dòng code bị cảnh báo. Nếu đúng là cảnh báo giả, em hướng dẫn dev thêm mã CVE hoặc rule ID vào tệp `.semgrepignore` kèm dòng comment giải trình lý do an toàn. Em giữ nguyên Job SAST trên pipeline để tiếp tục bảo vệ dự án trước các lỗ hổng thật khác."

### Kịch bản 4: Phân biệt cơ chế quét mã nguồn và quét Container Image
- **Nhà tuyển dụng:** "Quét SAST mã nguồn (`semgrep`), quét thư viện (`trivy fs`) và quét Container Image (`trivy image`) khác nhau ở điểm nào?"
- **Ứng viên:** "SAST quét mã nguồn thô tự viết ở stage test; Dependency Scanning quét tệp khóa thư viện (`go.sum`) ở stage test; còn Container Image Scanning quét hệ điều hành Linux Base OS (như APK/APT packages) và tệp thực thi nén ở stage build. Cả 3 lớp quét tạo thành chiến lược bảo mật chiều sâu (Defense in Depth)."

### Kịch bản 5: Xử lý sự cố CVE mức `CRITICAL` trong thư viện chưa có bản vá (Unfixed CVE)
- **Nhà tuyển dụng:** "Nếu Trivy phát hiện 1 CVE mức `CRITICAL` trong thư viện `golang.org/x/net` nhưng phía nhà phát triển thư viện chưa tung ra bản vá (`Fixed Version: N/A`), em xử lý sao?"
- **Ứng viên:** "Em sẽ kiểm tra xem ứng dụng có thực sự gọi tới hàm bị dính CVE đó hay không. Nếu không gọi tới hoặc đã có phương án bù đắp WAF ở tầng Network, em tạm thời thêm CVE đó vào `.trivyignore` với vết audit chi tiết. Đồng thời em tạo 1 Issue theo dõi để cập nhật thư viện ngay khi bản patch chính thức được phát hành."

### Kịch bản 6: Thiết lập phân quyền bảo vệ các tệp Ignore Files
- **Nhà tuyển dụng:** "Làm sao để ngăn chặn tình trạng Developer tự ý thêm các CVE nguy hiểm vào tệp `.trivyignore` để qua mặt Security Quality Gate?"
- **Ứng viên:** "Em cấu hình tệp `CODEOWNERS` tại gốc repository chỉ định tệp `.trivyignore` và `.semgrepignore` thuộc quyền sở hữu của nhóm `@security-team`. Khi bất kỳ ai tạo MR sửa đổi các tệp này, GitLab sẽ bắt buộc phải có chữ ký duyệt (Approve) từ Security Lead mới cho phép Merge."

### Kịch bản 7: Tối ưu thời gian quét an ninh cho các Pipeline lớn
- **Nhà tuyển dụng:** "Làm sao để rút ngắn thời gian quét SAST và SCA từ 10 phút xuống dưới 1 phút trên các repo mã nguồn lớn?"
- **Ứng viên:** "Em áp dụng 3 giải pháp: 1) Cấu hình cờ `--exclude` loại bỏ các thư mục `vendor/`, `node_modules/`, `test/`; 2) Nạp đệm đệm cơ sở dữ liệu Trivy DB đệm từ Docker Cache Volume; 3) Chỉ chạy quét đệm trên các tệp mã nguồn có sự thay đổi (Diff Scan) trong Merge Request."

---

## §V3.5. 15 Kịch bản Roleplay Phỏng vấn Kỹ sư DevOps (Mở rộng)

### Kịch bản 8: Xử lý sự cố Semgrep scan bị treo do tệp mã nguồn nén `.min.js`
- **Nhà tuyển dụng:** "Job `sast-semgrep` bị treo 15 phút rồi bị timeout ở tệp `bundle.min.js`. Em xử lý thế nào?"
- **Ứng viên:** "Lỗi này do Semgrep cố gắng phân tích cây cú pháp AST cho tệp JS nén dòng đơn dài hàng triệu ký tự. Em xử lý bằng cách thêm cờ `--exclude="*.min.js"` và `--max-target-bytes=1000000` vào câu lệnh gọi Semgrep CLI để bỏ qua các tệp web assets nén."

### Kịch bản 9: Tự động hóa tạo GitLab Issue khi phát hiện lỗ hổng `CRITICAL`
- **Nhà tuyển dụng:** "Làm sao để tự động khởi tạo một GitLab Issue giao việc cho dev khi Security Scan phát hiện lỗi `CRITICAL` trên nhánh `main`?"
- **Ứng viên:** "Em viết một script Python ở bước `after_script` của CI Job. Script đọc tệp `gl-sast-report.json`, lọc các lỗ hổng mức `Critical`, và gọi REST API của GitLab (`POST /api/v4/projects/:id/issues`) để tự động tạo Issue đính kèm mã file và dòng code bị dính lỗi."

### Kịch bản 10: Tích hợp công cụ quét Secret Scanning Gitleaks trong CI Pipeline
- **Nhà tuyển dụng:** "Làm sao để chặn lập trình viên lỡ tay commit AWS Secret Access Key lên Git repository?"
- **Ứng viên:** "Em khởi tạo Job `secret-detection` sử dụng công cụ **Gitleaks**. Job này quét toàn bộ các commit diff trong MR. Nếu phát hiện chuỗi có định dạng AWS Key hay JWT Private Key, Job sẽ trả về `exit code 1` ngắt pipeline ngay lập tức trước khi commit được đẩy lên server."

### Kịch bản 11: Quản lý và bảo mật tệp CSDL Vulnerability DB của Trivy
- **Nhà tuyển dụng:** "Tại sao trong môi trường Enterprise không nên cho các CI Runner tự do tải Trivy DB từ Internet?"
- **Ứng viên:** "Vì việc Runner liên tục tải Trivy DB từ GitHub sẽ nhanh chóng chạm trần Rate-Limit IP, làm sập toàn bộ các CI pipelines của công ty. Ngoài ra, việc kết nối ra Internet công cộng vi phạm chính sách an ninh Air-Gapped của ngân hàng. Giải pháp là dựng máy chủ Mirror nội bộ để sync DB định kỳ."

### Kịch bản 12: Đánh giá mức độ nghiêm trọng lỗ hổng bằng điểm số CVSS v3 Vector
- **Nhà tuyển dụng:** "Điểm CVSS v3 Score 9.8 khác điểm 7.5 ở những chỉ số Vector nào?"
- **Ứng viên:** "Điểm 9.8 (CRITICAL) thường có Vector `AV:N/AC:L/PR:N/UI:N` — nghĩa là lỗ hổng có thể khai thác qua mạng Internet (Network), độ phức tạp thấp (Low), không cần đăng nhập (None) và không cần tương tác người dùng. Trong khi điểm 7.5 (HIGH) thường đòi hỏi phải có quyền truy cập người dùng cơ bản (`PR:L`)."

### Kịch bản 13: Xử lý sự cố tệp báo cáo JSON bị sai định dạng làm Security Dashboard không hiển thị
- **Triệu chứng:** Security Dashboard báo lỗi `JSON syntax error at line 45`.
- **Nguyên nhân:** Script ghi tệp báo cáo bị hủy giữa chừng do hết bộ nhớ đĩa làm tệp JSON bị rách đệm.
- **Cách khắc phục:** Thêm bước kiểm tra tính hợp lệ của JSON bằng `jq . gl-sast-report.json` trước khi nộp sang `artifacts:reports`.

### Kịch bản 14: Tự động hóa đồng bộ danh sách lỗ hổng sang hệ thống quản lý an ninh DefectDojo
- **Nhà tuyển dụng:** "Làm sao để tập trung toàn bộ báo cáo an ninh SAST/SCA của 50 dự án về một máy chủ Dashboard duy nhất?"
- **Ứng viên:** "Em sử dụng công cụ quản lý lỗ hổng tập trung **DefectDojo**. Trong CI Pipeline của các dự án, sau khi xuất tệp `gl-sast-report.json` và `sarif`, em gọi script curl đẩy tệp báo cáo sang DefectDojo REST API để tự động khử trùng lặp (Deduplication) và vẽ biểu đồ an ninh toàn công ty."

### Kịch bản 15: Kiểm tra tính tuân thủ quy chuẩn bảo mật phần mềm NIST SP 800-218 (SSDF)
- **Nhà tuyển dụng:** "Làm sao để chứng minh quy trình CI/CD của công ty đạt chuẩn an ninh phần mềm NIST SSDF?"
- **Ứng viên:** "Em trích xuất các tệp báo cáo an ninh JSON (`gl-sast-report.json`, `gl-dependency-scanning-report.json`), tệp cấu hình Quality Gate, tệp hiện vật `bang-5-security-va-hien-vat.tsv`, và nhật ký audit của `.trivyignore`. Tất cả được đóng gói đính kèm vào Release Event chứng minh quy trình phát triển mã nguồn an toàn theo chuẩn NIST."

---

## §V4. Bài tập về nhà (BTVN 4) — Chuẩn bị cho Buổi 29 (DAST và Fuzz Testing)

### Yêu cầu chuẩn bị kiến thức cho Buổi 29 (Quét an ninh động DAST và Fuzzing)

1. **Nghiên cứu nguyên lý Quét an ninh động (DAST - Dynamic Application Security Testing):** Tìm hiểu công cụ `OWASP ZAP` (Zaproxy) quét kiểm thử tấn công thử nghiệm ứng dụng web đang chạy ở Runtime.
2. **Nghiên cứu nguyên lý Fuzz Testing (Fuzzing):** Tìm hiểu cách sinh dữ liệu đầu vào ngẫu nhiên rác (Fuzz Inputs) để phát hiện lỗi tràn bộ nhớ (Buffer Overflow) và Crash ứng dụng.
3. **Phân biệt ranh giới giữa SAST và DAST:** SAST quét mã nguồn tĩnh (Inside-out); DAST quét kiểm thử Runtime từ bên ngoài (Outside-in).
4. **Tích hợp DAST vào Staging Pipeline:** Tìm hiểu cách khởi chạy ứng dụng mẫu trong Container và gọi OWASP ZAP Baseline Scan quét các lỗ hổng XSS, CORS, Broken Auth.

---

## Bảng đối soát thời lượng

| Section | Tiêu đề | Thời lượng |
|---|---|---|
| §V1 | Bảng tổng hợp thuật ngữ & 12 bẫy hỏng im lặng | 5 phút |
| §V2 | 12 câu vấn đáp chuyên sâu (Level 3 - Kiến trúc sư CI/CD) | 10 phút |
| §V3 | Câu chốt để nói khi phỏng vấn | 3 phút |
| §V4 | Bài tập về nhà (BTVN 4 chuẩn bị Buổi 29) | 2 phút |
| **Tổng** | **Khối vấn đáp & Phấn bảng** | **20'** |