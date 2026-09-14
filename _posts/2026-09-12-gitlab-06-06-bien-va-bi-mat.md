---
layout: post
title: "[Bài 06] Quản Lý Biến & Bảo Mật Secrets: CI/CD Variables, Masked / Protected Variables & File-type Variables"
date: 2026-09-12 08:40:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-06
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 6
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.06] Hướng dẫn chuyên sâu Quản Lý Biến & Bảo Mật Secrets: CI/CD Variables, Masked / Protected Variables & File-type Variables: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Quản Lý Biến & Bảo Mật Secrets: CI/CD Variables, Masked / Protected Variables & File-type Variables."
  - "Làm chủ thứ tự ưu tiên 9 nấc biến, cơ chế Masked/Protected, File-type variables và mở rộng biến an toàn."
  - "Bảo mật chuỗi cung ứng phần mềm với SAST/DAST, Container Scanning và OIDC Authentication."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 12 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 06] QUẢN LÝ BIẾN & BẢO MẬT SECRETS: CI/CD VARIABLES, MASKED / PROTECTED VARIABLES & FILE-TYPE VARIABLES

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

### 1.1. Luận Đề Trung Tâm: Biến Đến Từ 9 Nguồn Và Có Thứ Tự Ưu Tiên Nền Tảng

Trong thiết kế hệ thống CI/CD, biến môi trường (Environment Variables) là con đường duy nhất đưa cấu hình động và bí mật (secrets) từ bên ngoài vào trong quá trình thực thi mà không làm bẩn mã nguồn repository. Tuy nhiên, sự cố phổ biến nhất trong các dự án enterprise là tình trạng: *"Kỹ sư sửa biến trong YAML ba lần nhưng job vẫn lấy giá trị cũ"* hoặc *"Job deploy trên branch staging chạy thành công nhưng không thực sự deploy gì vì biến secret bị rỗng"*.

> **Biến trong GitLab CI đến từ CHÍN nguồn khác nhau, và thứ tự ưu tiên giữa chúng là thuộc tính của NỀN TẢNG (Platform Rule), không phải của tệp `.gitlab-ci.yml`. Do đó, không ai có thể xác định giá trị thực tế của một biến chỉ bằng cách đọc mã nguồn YAML — mọi xung đột giá trị đều phải được phân giải qua hệ thống phân cấp 9 nấc.**

```text
   NẤC CAO GHI ĐÈ NẤC THẤP (Highest Precedence Overrides Lowest):
   
   ┌─── [ Nấc 1: Pipeline Variables ] ───────────────────────────────────────────┐
   │    Trigger token, Scheduled pipelines, Manual run (Web UI), Trigger API     │
   └───┬─────────────────────────────────────────────────────────────────────────┘
       │ Ghi đè
       ▼
   ┌─── [ Nấc 2: Project Variables ] ────────────────────────────────────────────┐
   │    Settings > CI/CD > Variables (Cấp dự án)                                 │
   └───┬─────────────────────────────────────────────────────────────────────────┘
       │ Ghi đè
       ▼
   ┌─── [ Nấc 3: Group Variables ] ──────────────────────────────────────────────┐
   │    Settings > CI/CD > Variables (Kế thừa từ Group / Subgroup)               │
   └───┬─────────────────────────────────────────────────────────────────────────┘
       │ Ghi đè
       ▼
   ┌─── [ Nấc 4: Instance Variables ] ───────────────────────────────────────────┐
   │    Admin Area > CI/CD > Variables (Cấp toàn cụm GitLab Instance)            │
   └───┬─────────────────────────────────────────────────────────────────────────┘
       │ Ghi đè
       ▼
   ┌─── [ Nấc 5: Dotenv Variables ] ─────────────────────────────────────────────┐
   │    artifacts:reports:dotenv từ job trước (Truyền sang job sau qua DAG/needs) │
   └───┬─────────────────────────────────────────────────────────────────────────┘
       │ Ghi đè
       ▼
   ┌─── [ Nấc 6: Job-level Variables ] ──────────────────────────────────────────┐
   │    Khai báo trong khối `variables:` của từng Job trong .gitlab-ci.yml       │
   └───┬─────────────────────────────────────────────────────────────────────────┘
       │ Ghi đè
       ▼
   ┌─── [ Nấc 7: Root-level Variables ] ─────────────────────────────────────────┐
   │    Khai báo trong khối `variables:` toàn cục ở đầu .gitlab-ci.yml           │
   └───┬─────────────────────────────────────────────────────────────────────────┘
       │ Ghi đè
       ▼
   ┌─── [ Nấc 8: Deployment Variables ] ─────────────────────────────────────────┐
   │    Biến sinh ra từ Kubernetes cluster integration hoặc Environment config   │
   └───┬─────────────────────────────────────────────────────────────────────────┘
       │ Ghi đè
       ▼
   ┌─── [ Nấc 9: Predefined Variables ] ─────────────────────────────────────────┐
   │    Hệ thống biến định sẵn: CI_COMMIT_SHA, CI_JOB_ID, CI_PROJECT_DIR...      │
   └─────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TD
    subgraph UI_API_INJECTION["1. Nguồn Bên Ngoài (External Injections)"]
        P1["1. Pipeline Variables<br/>(Manual / API / Web / Schedule)"]
        P2["2. Project CI/CD Variables<br/>(Masked / Protected)"]
        P3["3. Group CI/CD Variables"]
        P4["4. Instance CI/CD Variables"]
    end

    subgraph ARTIFACT_INJECTION["2. Nguồn Động (Dynamic Inter-job)"]
        P5["5. artifacts:reports:dotenv<br/>(Dynamic outputs)"]
    end

    subgraph REPO_INJECTION["3. Nguồn Khai Báo Repo (Static Code)"]
        P6["6. Job-level variables:"]
        P7["7. Top-level variables:"]
    end

    subgraph SYSTEM_INJECTION["4. Nguồn Hệ Thống (Platform / Cluster)"]
        P8["8. Deployment variables<br/>(Kube / Env Integrations)"]
        P9["9. Predefined variables<br/>(CI_COMMIT_SHA, CI_JOB_ID)"]
    end

    P1 -->|"Ghi đè"| P2
    P2 -->|"Ghi đè"| P3
    P3 -->|"Ghi đè"| P4
    P4 -->|"Ghi đè"| P5
    P5 -->|"Ghi đè"| P6
    P6 -->|"Ghi đè"| P7
    P7 -->|"Ghi đè"| P8
    P8 -->|"Ghi đè"| P9
    P9 --> RUNNER_ENV["Runner Execution Environment<br/>(/bin/sh export ENV)"]
```

### 1.2. Cơ Chế Masked vs Protected Variables: Hai Trục Bảo Vệ Hoàn Toàn Tách Biệt

Nhiều kỹ sư nhầm lẫn giữa tính chất `Masked` (che giấu) và `Protected` (bảo vệ phạm vi). Đây là hai cơ chế hoàn toàn độc lập giải quyết hai mối đe dọa bảo mật khác nhau:

1. **`Masked Variables` (Bảo Vệ Luồng Output / Log Stream)**:
   - **Mục đích**: Chống rò rỉ vô ý giá trị nhạy cảm (API token, password) hiển thị ra giao diện màn hình Job Trace (Web UI Logs).
   - **Cơ chế**: GitLab Runner nhận danh sách giá trị cần mask từ GitLab Server. Trong suốt quá trình thực thi, Runner stream từng byte log qua bộ lọc regex. Bất kỳ chuỗi con nào khớp chính xác với giá trị biến masked sẽ bị thay thế bằng chuỗi `[MASKED]`.
   - **Giới hạn kỹ thuật**:
     - Độ dài tối thiểu: **8 ký tự**.
     - Bộ ký tự hợp lệ: Base64 chuẩn `[a-zA-Z0-9_+=/@:~.-]`. Nếu chứa dấu cách, tab hoặc ký tự đặc biệt ngoài chuẩn, GitLab Server từ chối bật cờ `masked` với mã `HTTP 400`.
     - **KHÔNG BẢO VỆ ĐƯỢC**: Nếu biến bị nén thành base64, url-encode, ghi vào file artifact hoặc gửi qua HTTP payload ra bên ngoài, giá trị thật sẽ bị lộ hoàn toàn.
2. **`Protected Variables` (Bảo Vệ Phạm Vi Thực Thi / Execution Boundary)**:
   - **Mục đích**: Đảm bảo secret chỉ được truyền vào các job chạy trên Protected Branches (như `main`, `production`) hoặc Protected Tags.
   - **Cơ chế**: Khi pipeline khởi tạo trên một nhánh tính năng thông thường (`feature/*`), GitLab Server **hoàn toàn loại bỏ biến Protected khỏi payload gửi cho Runner**.
   - **Hậu quả nếu cấu hình sai**: Khi job deploy chạy trên feature branch, biến password/token mang giá trị rỗng (`""`), dẫn đến câu lệnh deploy không xác thực được hoặc fail âm thầm nếu script không kiểm tra biến rỗng.

```text
   PROTECTED BRANCH (main / tag v1.0.0) ───► GitLab Server GỬI biến Protected ───► Job nhận đủ Secrets
   
   FEATURE BRANCH (feat/login)         ───► GitLab Server CẮT BỎ biến Protected ──► Job nhận giá trị RỖNG
```

### 1.3. Phân Biệt Biến Dạng `Variable` (String) và `File` (File-type Variable)

GitLab CI hỗ trợ hai kiểu biến:
- **Kiểu `Variable`**: Runner export trực tiếp vào môi trường shell: `export API_KEY="my-secret-token"`. Truy cập qua `$API_KEY`.
- **Kiểu `File`**: Runner ghi nội dung của biến vào một tệp tạm trên đĩa (thường nằm tại `/tmp/builds/...` hoặc `$CI_PROJECT_DIR.tmp/`) và gán **đường dẫn tuyệt đối của tệp** vào tên biến: `export KUBECONFIG="/builds/org/repo.tmp/KUBECONFIG"`.
  - Nếu gọi `echo $KUBECONFIG` &rarr; Kết quả in ra đường dẫn `/builds/org/repo.tmp/KUBECONFIG`.
  - Nếu muốn đọc nội dung &rarr; Bắt buộc dùng `cat "$KUBECONFIG"` hoặc truyền trực tiếp đường dẫn vào cờ CLI: `kubectl --kubeconfig "$KUBECONFIG" get nodes`.

### 1.4. Mở Rộng Biến (Variable Expansion) & Cờ `expand: false`

Mặc định, GitLab CI sẽ tự động mở rộng (evaluate) các ký tự `$` trong giá trị biến:
- Nếu bạn khai báo `DATABASE_URL="postgres://$DB_USER:$DB_PASS@$DB_HOST:5432/$DB_NAME"`, GitLab sẽ thế giá trị của `$DB_USER`, `$DB_PASS` vào trước khi truyền cho Runner.
- **Rủi ro**: Nếu mật khẩu của bạn vô tình chứa ký tự `$`, ví dụ `p@ss$word123`, GitLab sẽ cố gắng tìm biến tên là `$word123` (vốn rỗng) và biến mật khẩu thành `p@ss123` &rarr; Đăng nhập thất bại (401 Unauthorized) dù bạn nhìn chuỗi secret gốc hoàn toàn đúng!
- **Giải pháp**: Bật thuộc tính `expand: false` trong Settings > CI/CD Variables hoặc trong file YAML để vô hiệu hóa tính năng tự thế ký tự `$`.

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

| Tiêu chí phân tích | Plain CI/CD Variable | Masked Variable | Protected Variable | File-type Variable | HashiCorp Vault / OIDC Token |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Vị trí lưu trữ** | GitLab PostgreSQL DB | GitLab PostgreSQL DB | GitLab PostgreSQL DB | Runner Temp Disk (`.tmp/`) | External Vault / Keyless JWT |
| **Cách truyền vào Job** | Env var (`export VAR=...`) | Env var (`export VAR=...`) | Env var (chỉ trên protected ref) | Env var chứa File Path | ID Token OIDC &rarr; Đổi STS token ngắn hạn |
| **Bảo vệ Log Stream** | ❌ Hiển thị thô trong log | ✅ Tự thế bằng `[MASKED]` | ❌ Không bảo vệ log | ✅ Masked nếu đường dẫn hợp lệ | ✅ Secret ngắn hạn tự hủy |
| **Bảo vệ Nhánh Rẽ (Branches)** | ❌ Có mặt ở mọi branch | ❌ Có mặt ở mọi branch | ✅ Chỉ xuất hiện trên Protected | Tùy chọn (Protected File) | ✅ Policy ràng buộc theo `sub` claim |
| **Hỗ trợ định dạng dài/Multi-line** | ⚠️ Dễ lỗi xuống dòng | ❌ Giới hạn format (no spaces) | ⚠️ Dễ lỗi xuống dòng | ✅ Chuyên dụng cho RSA key, Kubeconfig, JSON | ✅ Quản lý secret dạng JSON payload |
| **Xử lý ký tự `$`** | Bị expand nếu không tắt | Bị expand nếu không tắt | Bị expand nếu không tắt | Không bị biến dạng nội dung file | Xử lý an toàn qua CLI / API |
| **Thời hạn sống (TTL)** | Vĩnh viễn tới khi xóa | Vĩnh viễn tới khi xóa | Vĩnh viễn tới khi xóa | Xóa theo vòng đời Job | Ngắn hạn (5 phút – 1 giờ) |
| **Mức độ sẵn sàng Enterprise** | Thấp (chỉ cho config chung) | Trung bình (API Key đơn giản) | Khá (Deploy Token production) | Tốt (Certificate, Cloud Creds) | Xuất sắc (Chuẩn Zero Trust DevSecOps) |

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (Architecture Breakdown)

Dưới đây là kiến trúc pipeline mẫu kết hợp toàn diện các chuẩn biến: Root variables, Job variables, Masked & Protected variables, File-type variables, Mở rộng biến an toàn `expand: false`, và truyền biến động qua `dotenv`:

```yaml
# ==============================================================================
# PIPELINE KIẾN TRÚC QUẢN TRỊ BIẾN & BẢO MẬT SECRETS CHUẨN ENTERPRISE
# ==============================================================================
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS'
      when: never
    - if: '$CI_COMMIT_BRANCH'

stages:
  - prepare
  - validate
  - build
  - deploy

# ------------------------------------------------------------------------------
# 1. ROOT LEVEL VARIABLES (Nấc 7 - Ưu tiên mặc định)
# ------------------------------------------------------------------------------
variables:
  APP_ENV: "staging"
  REGISTRY_ENDPOINT: "harbor.internal.corp/app"
  DOCKER_DRIVER: "overlay2"
  # Tắt expand toàn cục nếu có biến chứa ký tự $
  FF_DISABLE_UMASK_FOR_DOCKER_EXECUTOR: "true"

# ------------------------------------------------------------------------------
# 2. JOB PREPARE: Sinh biến động qua Dotenv (Nấc 5)
# ------------------------------------------------------------------------------
generate_dynamic_version:
  stage: prepare
  image: alpine:3.20
  script:
    - echo "=== [Pha 1] Khởi tạo dynamic metadata ==="
    - APP_BUILD_TIME=$(date -u +'%Y%m%d-%H%M%S')
    - DYNAMIC_VERSION="v2.4.0-${CI_COMMIT_SHORT_SHA}-${APP_BUILD_TIME}"
    - echo "DYNAMIC_APP_VERSION=${DYNAMIC_VERSION}" > build.env
    - echo "DEPLOY_RELEASE_ID=REL-${CI_PIPELINE_ID}" >> build.env
    - cat build.env
  artifacts:
    reports:
      dotenv: build.env
    expire_in: 1 hour

# ------------------------------------------------------------------------------
# 3. JOB VALIDATE: Kiểm tra fail-fast các biến môi trường bắt buộc
# ------------------------------------------------------------------------------
validate_environment:
  stage: validate
  image: alpine:3.20
  script:
    - echo "=== [Pha 2] Khẳng định tính toàn vẹn của biến ==="
    # Chốt chặn Fail-fast: Nếu thiếu biến critical lập tức kết thúc pipeline ngay
    - : "${APP_ENV:?Error - Variable APP_ENV must be defined}"
    - echo "Current Environment: ${APP_ENV}"
    # Kiểm tra biến file-type kubeconfig nếu là nhánh production
    - |
      if [ "$CI_COMMIT_REF_PROTECTED" = "true" ]; then
        echo "Validating Protected Release Credentials..."
        if [ -z "${PROD_KUBECONFIG:-}" ]; then
          echo "FATAL: PROD_KUBECONFIG is empty on protected ref!" >&2
          exit 1
        fi
        test -f "${PROD_KUBECONFIG}" || (echo "FATAL: Kubeconfig path invalid" >&2 && exit 1)
        echo "Kubeconfig path confirmed: ${PROD_KUBECONFIG}"
      fi

# ------------------------------------------------------------------------------
# 4. JOB BUILD: Tiêu thụ biến Dotenv từ Job prepare
# ------------------------------------------------------------------------------
compile_artifact:
  stage: build
  image: alpine:3.20
  needs:
    - job: generate_dynamic_version
      artifacts: true
  script:
    - echo "=== [Pha 3] Build với Dynamic Version ==="
    # DYNAMIC_APP_VERSION được nạp tự động từ dotenv (Nấc 5)
    - echo "Building package for version: ${DYNAMIC_APP_VERSION}"
    - echo "Release ID: ${DEPLOY_RELEASE_ID}"
    - mkdir -p dist/
    - echo "Application Binary ${DYNAMIC_APP_VERSION}" > dist/app.bin
  artifacts:
    paths:
      - dist/
    expire_in: 1 day

# ------------------------------------------------------------------------------
# 5. JOB DEPLOY: Sử dụng File-type Variables & Protected Variables
# ------------------------------------------------------------------------------
deploy_production:
  stage: deploy
  image: bitnami/kubectl:1.30
  needs:
    - job: compile_artifact
      artifacts: true
    - job: generate_dynamic_version
      artifacts: true
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
  script:
    - echo "=== [Pha 4] Deploy Production với Protected Secrets ==="
    # Chốt chặn bảo vệ biến nhạy cảm
    - : "${PROD_DEPLOY_TOKEN:?Error - Missing PROD_DEPLOY_TOKEN}"
    - : "${PROD_KUBECONFIG:?Error - Missing PROD_KUBECONFIG}"
    # Kiểm tra độ dài biến để phát hiện ký tự tàng hình / trailing newline
    - TOKEN_LEN=${#PROD_DEPLOY_TOKEN}
    - echo "Deploy Token length verified: ${TOKEN_LEN} chars"
    - echo "Deploying version ${DYNAMIC_APP_VERSION} to Kubernetes Cluster..."
    # Đọc Kubeconfig từ File-type Variable đường dẫn
    - kubectl --kubeconfig "${PROD_KUBECONFIG}" version --client=true
    - echo "Deploy success for Release ${DEPLOY_RELEASE_ID}"
  environment:
    name: production
    url: https://app.internal.corp
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

```mermaid
graph TD
    INC1["Sự Cố: Token chính xác 100% nhưng API Gateway luôn trả về HTTP 401"]
    W11["Tại sao API báo 401? &rarr; Token xác thực bị Server từ chối"]
    W12["Tại sao Token bị từ chối? &rarr; Chuỗi hash SHA-256 gửi đi trong Header không khớp"]
    W13["Tại sao không khớp? &rarr; Token chứa 1 byte xuống dòng tàng hình \n ở cuối"]
    W14["Tại sao có byte \n? &rarr; Kỹ sư copy từ terminal/web và nhấn Enter khi dán vào Web UI"]
    W15["Biện pháp: Dùng od -c kiểm tra, tr -d '\r\n' làm sạch và assert ${#TOKEN}"]
    
    INC1 --> W11 --> W12 --> W13 --> W14 --> W15
```

### 4.1. Incident 1: Token Xác Thực Bị Lỗi 401 Unauthorized Do Ký Tự Tàng Hình (Invisible Bytes)

### Tình Huống Sự Cố Thực Tế:
<span class="badge badge--rose">🕒 02:15 AM</span> — Kỹ sư trực On-call nhận cảnh báo pipeline deploy khẩn cấp lên Kubernetes staging bị fail liên tục ở bước xác thực API Gateway, dù biến `PROD_DEPLOY_TOKEN` vừa được cập nhật lại chính xác từ hệ thống quản lý mật khẩu nội bộ.

### Hậu Quả & Log Lỗi Thực Tế:
```text
$ curl -s -f -X POST "https://api.internal.corp/v1/deploy" \
    -H "Authorization: Bearer ${PROD_DEPLOY_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"release": "'"${DYNAMIC_APP_VERSION}"'"}'
HTTP/1.1 401 Unauthorized
Date: Mon, 12 Sep 2026 19:15:22 GMT
Content-Type: application/json
{"error": "invalid_token", "error_description": "The access token signature is invalid or malformed"}
ERROR: Job failed: exit code 22
```

### 5-Whys Root Cause Analysis:
1. <span class="badge badge--primary">Why 1</span> **Tại sao API Gateway từ chối xác thực với mã 401?** &rarr; Chữ ký băm HMAC của access token không khớp với bản ghi trên Identity Provider.
2. <span class="badge badge--primary">Why 2</span> **Tại sao chuỗi băm không khớp dù token được copy chính xác?** &rarr; Chuỗi token truyền trong header HTTP có độ dài 41 ký tự thay vì 40 ký tự chuẩn.
3. <span class="badge badge--primary">Why 3</span> **Tại sao token lại bị dư 1 ký tự?** &rarr; Ký tự thứ 41 là byte xuống dòng tàng hình `\n` (0x0A) nằm ở cuối chuỗi.
4. <span class="badge badge--primary">Why 4</span> **Tại sao ký tự xuống dòng lại lọt vào biến GitLab?** &rarr; Khi kỹ sư copy từ terminal bằng phím chuột hoặc ấn Enter khi dán vào form **Settings > CI/CD > Variables**, ký tự newline bị lưu nguyên vẹn vào database. Lệnh `echo $TOKEN` thông thường không hiển thị được byte này.
5. <span class="badge badge--emerald">Root Cause Remedy</span> **Biện pháp khắc phục chuẩn SRE:**
   - <span class="badge badge--emerald">Input Sanitization</span>: Luôn khử sạch ký tự xuống dòng trước khi sử dụng: `CLEAN_TOKEN=$(printf "%s" "$PROD_DEPLOY_TOKEN" | tr -d '\r\n')`.
   - <span class="badge badge--cyan">Byte Audit</span>: Sử dụng `printf "%s" "$VAR" | od -c` để soi rõ từng byte nhị phân thô khi gỡ rối.
   - <span class="badge badge--amber">Length Assertion</span>: Kiểm tra độ dài chuỗi bằng `${#PROD_DEPLOY_TOKEN}` ngay trong `before_script`.

### 4.2. Incident 2: Rò Rỉ Secret Ra Ngoài Do Hiểu Nhầm Về Cơ Chế Masked Variables

### Tình Huống Sự Cố Thực Tế:
<span class="badge badge--rose">🕒 10:45 AM</span> — Bộ phận Security phát hiện Private API Token cấp Production bị gửi kèm trong tệp artifact log `debug-info.tar.gz` được công khai cho toàn bộ thành viên dự án tải về, dù biến này đã được bật cờ `Masked`.

### Hậu Quả & Log Lỗi Thực Tế:
```text
$ tar -ztvf debug-info.tar.gz
-rw-r--r-- root/root        1024 2026-09-12 10:40 payload.json
-rw-r--r-- root/root        2048 2026-09-12 10:40 auth_headers.txt

$ cat auth_headers.txt
Authorization: Bearer glpat-SecretLiveProdMasterKey999888
X-Vault-Token: s.vJ8x999332110022AAABBB
```

### 5-Whys Root Cause Analysis:
1. <span class="badge badge--primary">Why 1</span> **Tại sao token xuất hiện rõ ràng trong artifact dù đã bật Masked?** &rarr; Cơ chế `Masked` của GitLab Runner chỉ can thiệp vào luồng STDOUT/STDERR của Job Trace, hoàn toàn không quét hay che giấu nội dung tệp lưu trong `artifacts:paths`.
2. <span class="badge badge--primary">Why 2</span> **Tại sao script lại ghi token vào tệp artifact?** &rarr; Job chạy một shell script debug trung gian xuất toàn bộ HTTP request headers ra file `auth_headers.txt` để phục vụ audit downstream.
3. <span class="badge badge--primary">Why 3</span> **Tại sao quá trình review MR không phát hiện ra?** &rarr; Lập trình viên nhầm tưởng rằng "đã bật Masked thì biến sẽ an toàn ở mọi nơi".
4. <span class="badge badge--primary">Why 4</span> **Có trường hợp nào khác Masked bị vô hiệu hóa?** &rarr; Khi token được mã hóa Base64 (`echo -n $TOKEN | base64`) hoặc đưa vào URL query params bị encode `urlencode($TOKEN)`, chuỗi băm thay đổi khiến bộ lọc regex của Runner bỏ qua và in thẳng ra log.
5. <span class="badge badge--emerald">Root Cause Remedy</span> **Biện pháp khắc phục chuẩn SRE:**
   - <span class="badge badge--rose">Zero Secret in Artifacts</span>: Nghiêm cấm ghi bất kỳ file nào chứa secret vào đường dẫn gom artifact.
   - <span class="badge badge--emerald">OIDC Keyless Identity</span>: Chuyển đổi sang Vault OIDC hoặc Cloud IAM Role để sử dụng short-lived tokens thay vì lưu static token vĩnh viễn trong CI/CD Variables.

---

## 5. Hands-on Lab: Quản Lý Biến & Bảo Mật Secrets Toàn Diện (8 Bước Chuẩn)

```text
   ┌────────────────────────────────────────────────────────────────────────┐
   │                     LAB ARCHITECTURE: SECRETS & VARS                   │
   ├────────────────────────────────────────────────────────────────────────┤
   │                                                                        │
   │  [ Bước 1: Khởi tạo Repo & Biến 9 Nấc ]                                │
   │  Thiết lập project và đo lường 9 nấc ưu tiên biến qua API              │
   │                         │                                              │
   │                         ▼                                              │
   │  [ Bước 2: Thử nghiệm xung đột Project Variable vs YAML ]             │
   │  Tái hiện và xử lý ca sửa YAML không tác dụng                          │
   │                         │                                              │
   │                         ▼                                              │
   │  [ Bước 3: Kiểm chứng Masked Variables & Lỗ Hổng Rò Rỉ ]               │
   │  Thực nghiệm cơ chế mask log, rò rỉ qua artifact & encode              │
   │                         │                                              │
   │                         ▼                                              │
   │  [ Bước 4: Khởi tạo và sử dụng File-type Variables ]                   │
   │  Xử lý Private Key / Kubeconfig qua File variable an toàn             │
   │                         │                                              │
   │                         ▼                                              │
   │  [ Bước 5: Bắt bẫy Ký Tự Tàng Hình & Variable Expansion ]             │
   │  Debug lỗi 401 bằng od -c và khắc phục với expand: false               │
   │                         │                                              │
   │                         ▼                                              │
   │  [ Bước 6: Truyền Biến Động Đa Tầng qua Dotenv Report ]                │
   │  Kết nối biến từ upstream job sang downstream DAG jobs                 │
   │                         │                                              │
   │                         ▼                                              │
   │  [ Bước 7: Thiết lập Chốt Chặn An Toàn Fail-Fast ]                     │
   │  Cài đặt assertion bắt buộc biến không được rỗng                       │
   │                         │                                              │
   │                         ▼                                              │
   │  [ Bước 8: Dọn Dẹp Tài Nguyên & Audit Báo Cáo ]                        │
   │  Xóa biến tạm, revoke token và kiểm tra audit log                      │
   │                                                                        │
   └────────────────────────────────────────────────────────────────────────┘
```

### Bước 1: Khởi tạo Repo & Xác thực Thứ tự Ưu tiên 9 Nấc
Tạo repository kiểm thử và tạo biến Project qua REST API để đối chiếu với YAML.

```bash
# Khởi tạo biến Project qua API
curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/variables" \
  --form "key=TEST_OVERRIDE" \
  --form "value=PROJECT_LEVEL_VALUE"
```

Tạo `.gitlab-ci.yml` kiểm chứng độ ưu tiên:

```yaml
variables:
  TEST_OVERRIDE: "ROOT_YAML_VALUE"

stages:
  - test_precedence

check_precedence:
  stage: test_precedence
  image: alpine:3.20
  variables:
    TEST_OVERRIDE: "JOB_YAML_VALUE"
  script:
    - echo "Value of TEST_OVERRIDE is: ${TEST_OVERRIDE}"
```

> **Checkpoint 1**: Chạy pipeline và xem log của `check_precedence`. Kết quả in ra là `PROJECT_LEVEL_VALUE` vì Project Variable (Nấc 2) ghi đè toàn bộ Job-level (Nấc 6) và Root-level (Nấc 7).

### Bước 2: Xử lý Tình huống "Sửa YAML không tác dụng" & Protected Branch Traps
Cấu hình một biến Protected và kiểm tra hành vi khi chạy trên feature branch.

```bash
# Tạo biến PROTECTED qua API
curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/variables" \
  --form "key=PROD_SECRET_KEY" \
  --form "value=super-secret-key-12345" \
  --form "protected=true"
```

Tạo branch `feat/test-secret` và đẩy pipeline:

```yaml
test_protected_variable:
  stage: test_precedence
  image: alpine:3.20
  script:
    - echo "Ref is: ${CI_COMMIT_REF_NAME}, Protected: ${CI_COMMIT_REF_PROTECTED}"
    - |
      if [ -z "${PROD_SECRET_KEY}" ]; then
        echo "WARNING: PROD_SECRET_KEY is EMPTY on non-protected branch!"
      else
        echo "SUCCESS: PROD_SECRET_KEY is present."
      fi
```

> **Checkpoint 2**: Khi chạy trên branch `feat/test-secret`, log hiển thị `WARNING: PROD_SECRET_KEY is EMPTY`. Khi merge vào `main` (Protected), log hiển thị `SUCCESS: PROD_SECRET_KEY is present`.

### Bước 3: Kiểm chứng Masked Variables & Giới Hạn Bộ Lọc
Thực nghiệm khả năng che giấu của `masked` trong các tình huống output khác nhau.

```bash
# Tạo biến MASKED
curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/variables" \
  --form "key=MY_API_TOKEN" \
  --form "value=glpat-abcdef1234567890" \
  --form "masked=true"
```

Thực thi kiểm tra trong YAML:

```yaml
test_masking_mechanics:
  stage: test_precedence
  image: alpine:3.20
  script:
    - echo "Direct output: ${MY_API_TOKEN}"
    - echo "Base64 output: $(echo -n "${MY_API_TOKEN}" | base64)"
    - echo "${MY_API_TOKEN}" > leak.txt
  artifacts:
    paths:
      - leak.txt
    expire_in: 10 mins
```

> **Checkpoint 3**: 
> - Dòng 1 in ra: `Direct output: [MASKED]` (Che thành công).
> - Dòng 2 in ra chuỗi Base64 nguyên vẹn (Không che được vì giá trị hash không khớp chuỗi gốc).
> - Tải artifact `leak.txt` về máy mở ra xem: Chứa token nguyên vẹn (Artifact không bị mask).

### Bước 4: Cấu hình và Sử dụng File-type Variables
Tạo File-type variable chứa cấu hình SSH Private Key và kiểm tra cách runner xử lý.

```bash
# Tạo biến dạng File qua API
curl --request POST --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/variables" \
  --form "key=SSH_PRIVATE_KEY" \
  --form "value=-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
-----END OPENSSH PRIVATE KEY-----" \
  --form "variable_type=file"
```

Kiểm tra trong YAML:

```yaml
test_file_variable:
  stage: test_precedence
  image: alpine:3.20
  script:
    - echo "Variable value is a PATH: ${SSH_PRIVATE_KEY}"
    - test -f "${SSH_PRIVATE_KEY}" && echo "File exists on runner filesystem"
    - chmod 600 "${SSH_PRIVATE_KEY}"
    - head -n 1 "${SSH_PRIVATE_KEY}"
```

> **Checkpoint 4**: `echo ${SSH_PRIVATE_KEY}` in ra đường dẫn `/builds/group/project.tmp/SSH_PRIVATE_KEY`. Lệnh `test -f` xác nhận tệp tồn tại trên đĩa của container.

### Bước 5: Bắt bẫy Ký Tự Tàng Hình (Invisible Bytes) & Variable Expansion
Viết script tự động phát hiện ký tự xuống dòng `\n` và `\r\n` và xử lý biến chứa dấu `$`.

```yaml
test_special_characters:
  stage: test_precedence
  image: alpine:3.20
  variables:
    RAW_PASSWORD:
      value: 'MySecret$Password#2026'
      expand: false
  script:
    - echo "=== Checking for invisible trailing characters ==="
    - printf "%s" "${RAW_PASSWORD}" | od -c
    - LEN=${#RAW_PASSWORD}
    - echo "Total characters length: ${LEN}"
    - |
      if [ "${RAW_PASSWORD}" = 'MySecret$Password#2026' ]; then
        echo "SUCCESS: Password accurately preserved with expand: false"
      else
        echo "FAIL: Password corrupted by variable expansion" >&2
        exit 1
      fi
```

> **Checkpoint 5**: Job chạy thành công, chuỗi `MySecret$Password#2026` được giữ nguyên vẹn 22 ký tự, không bị rụng mất `$Password`.

### Bước 6: Truyền Biến Động Đa Tầng qua `dotenv` Report
Tạo pipeline 2 job truyền metadata động cho nhau mà không cần cấu hình UI variable.

```yaml
producer_job:
  stage: test_precedence
  image: alpine:3.20
  script:
    - BUILD_TIMESTAMP=$(date +%s)
    - echo "GENERATED_BUILD_ID=BLD-${BUILD_TIMESTAMP}" > dynamic.env
    - echo "TARGET_CLUSTER=k8s-prod-sea" >> dynamic.env
  artifacts:
    reports:
      dotenv: dynamic.env

consumer_job:
  stage: test_precedence
  image: alpine:3.20
  needs:
    - job: producer_job
      artifacts: true
  script:
    - echo "Received BUILD_ID from upstream: ${GENERATED_BUILD_ID}"
    - echo "Target Cluster is: ${TARGET_CLUSTER}"
    - test -n "${GENERATED_BUILD_ID}" || exit 1
```

> **Checkpoint 6**: `consumer_job` nhận chính xác biến `GENERATED_BUILD_ID` từ `producer_job` thông qua cơ chế nạp biến Dotenv (Nấc 5).

### Bước 7: Cài Đặt Chốt Chặn An Toàn Fail-Fast (Shell Assertions)
Tích hợp các pattern kiểm tra biến bắt buộc giúp pipeline fail ngay lập tức trong 0.01s nếu thiếu biến.

```yaml
test_fail_fast_assertion:
  stage: test_precedence
  image: alpine:3.20
  script:
    - echo "Testing fail-fast validation..."
    # Pattern 1: Kiểm tra biến bắt buộc bằng cú pháp Bash Parameter Expansion
    - : "${CRITICAL_VAR:?FATAL ERROR: Variable CRITICAL_VAR has not been configured!}"
    - echo "This line will not run if CRITICAL_VAR is empty"
```

> **Checkpoint 7**: Khi `CRITICAL_VAR` chưa được gán, job lập tức chuyển màu ĐỎ ở mili-giây đầu tiên với thông báo rõ ràng: `CRITICAL_VAR: FATAL ERROR: Variable CRITICAL_VAR has not been configured!`.

### Bước 8: Dọn Dẹp Tài Nguyên và Kiểm Tra Audit Log
Xóa toàn bộ các biến kiểm thử khỏi GitLab Project qua API.

```bash
# Xóa các biến test sau khi hoàn thành lab
for VAR_NAME in "TEST_OVERRIDE" "PROD_SECRET_KEY" "MY_API_TOKEN" "SSH_PRIVATE_KEY"; do
  curl --request DELETE --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
    "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/variables/${VAR_NAME}"
  echo "Deleted test variable: ${VAR_NAME}"
done
```

> **Checkpoint 8**: Truy cập **Settings > CI/CD > Variables** trên giao diện Web xác nhận danh sách biến đã được dọn sạch sẽ.

---

## 6. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q01</span>
      <span>Trình bày chính xác thứ tự ưu tiên 9 nấc biến trong GitLab CI/CD và nêu một tình huống thực tế giải quyết bằng bảng này.</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Thứ tự ưu tiên từ cao nhất xuống thấp nhất:</b></p>
    <ol>
      <li><b>Pipeline Variables</b> (Trigger API, Web UI Run Pipeline, Scheduled Pipeline).</li>
      <li><b>Project CI/CD Variables</b> (Settings &gt; CI/CD &gt; Variables của Project).</li>
      <li><b>Group CI/CD Variables</b> (Kế thừa từ Group cha / Subgroup).</li>
      <li><b>Instance CI/CD Variables</b> (Admin Area của cụm GitLab).</li>
      <li><b>Dotenv Variables</b> (Sinh từ <code>artifacts:reports:dotenv</code> của job trước qua DAG/needs).</li>
      <li><b>Job-level Variables</b> (Khai báo trong khối <code>variables:</code> của Job trong YAML).</li>
      <li><b>Root-level Variables</b> (Khai báo trong khối <code>variables:</code> toàn cục ở đầu YAML).</li>
      <li><b>Deployment Variables</b> (Biến tự sinh từ Kubernetes integration hoặc Environment settings).</li>
      <li><b>Predefined Variables</b> (Hệ thống biến định sẵn như <code>CI_COMMIT_SHA</code>, <code>CI_JOB_ID</code>).</li>
    </ol>
    <p><b>Tình huống thực tế:</b> Kỹ sư sửa URL database trong <code>.gitlab-ci.yml</code> nhưng job chạy vẫn trỏ về database cũ. Tra cứu bảng cho thấy một biến cùng tên đã được set trong Project Variables (Nấc 2), do Nấc 2 cao hơn Nấc 6/7 trong YAML nên giá trị trong YAML bị bỏ qua hoàn toàn.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q02</span>
      <span>Phân biệt bản chất kỹ thuật giữa Masked Variables và Protected Variables.</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p>Hai cơ chế giải quyết hai bài toán hoàn toàn độc lập:</p>
    <ul>
      <li><b>Masked Variables</b>: Bảo vệ <i>luồng hiển thị log (Job Trace)</i>. Runner stream log qua bộ lọc regex để thay thế chuỗi ký tự secret bằng <code>[MASKED]</code>. Biến vẫn được truyền vào mọi branch/job.</li>
      <li><b>Protected Variables</b>: Bảo vệ <i>phạm vi thực thi (Execution Scope)</i>. GitLab Server chỉ nạp biến này vào payload gửi cho Runner khi pipeline chạy trên Protected Branch (ví dụ <code>main</code>) hoặc Protected Tag. Trên feature branch, biến hoàn toàn không tồn tại (mang giá trị rỗng).</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q03</span>
      <span>Tại sao biến được đánh dấu Masked vẫn có thể bị lộ ra ngoài? Nêu 3 con đường rò rỉ điển hình.</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p>Runner chỉ áp dụng bộ lọc regex đối với chuỗi STDOUT/STDERR thô. Biến Masked sẽ bị lộ qua:</p>
    <ol>
      <li><b>Job Artifacts</b>: Nếu script thực hiện <code>echo $MASKED_SECRET &gt; output.txt</code> và đưa vào <code>artifacts:paths</code>, file này được upload nguyên vẹn lên server và bất kỳ ai có quyền Developer đều tải về đọc được.</li>
      <li><b>Encoding / Hashing</b>: Nếu script encode chuỗi thành Base64 (<code>echo -n $SECRET | base64</code>) hoặc URL-encode, chuỗi sau khi encode có hash khác chuỗi gốc nên bộ lọc Runner bỏ qua và in thẳng ra log.</li>
      <li><b>Gửi qua Network Payload</b>: Nếu dùng <code>curl -X POST -d "$SECRET" https://external-api.com</code> với cờ verbose <code>curl -v</code> hoặc log proxy bên ngoài, secret sẽ bị ghi nhận ở server đích.</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q04</span>
      <span>Khi nào bắt buộc phải dùng biến dạng File-type thay vì String Variable thông thường? Cho ví dụ.</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p>Nên và bắt buộc dùng <b>File-type Variable</b> khi:</p>
    <ul>
      <li>Dữ liệu nhạy cảm có cấu trúc nhiều dòng (multi-line), chứa ký tự ngắt dòng đặc biệt hoặc ký tự nhạy cảm shell như: <b>SSH Private Key (RSA/Ed25519)</b>, <b>SSL Certificates</b>, <b>Kubeconfig YAML</b>, hoặc <b>GCP Service Account JSON Key</b>.</li>
      <li>Các công cụ CLI yêu cầu truyền cờ trỏ tới đường dẫn file thay vì chuỗi text (ví dụ <code>kubectl --kubeconfig "$KUBECONFIG"</code> hoặc <code>docker login --password-stdin</code>).</li>
      <li>Tránh lỗi shell quoting và escape ký tự đặc biệt khi truyền nội dung dài qua lệnh <code>export</code>.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q05</span>
      <span>Giải thích nguyên nhân một Personal Access Token hoặc API Key dù copy chính xác 100% vẫn gây lỗi 401 Unauthorized trong CI/CD.</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p>Nguyên nhân phổ biến nhất là <b>Ký tự tàng hình (Trailing Invisible Bytes)</b>: Khi copy token từ web UI hoặc terminal, thao tác bôi đen hoặc nhấn phím Enter vô tình chèn thêm ký tự xuống dòng <code>\n</code> (0x0A) hoặc Carriage Return <code>\r\n</code> (0x0D 0x0A) vào cuối chuỗi trong ô cấu hình Variable của GitLab.</p>
    <p>Khi gửi HTTP Request qua <code>curl -H "Authorization: Bearer $TOKEN"</code>, ký tự xuống dòng làm hỏng HTTP Header hoặc bị Server xác thực từ chối vì chuỗi hash token không khớp.</p>
    <p><b>Khắc phục</b>: Dùng <code>printf "%s" "$TOKEN" | od -c</code> để kiểm tra và dùng <code>tr -d '\r\n'</code> để khử sạch ký tự thừa trước khi gọi API.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q06</span>
      <span>Biến sinh ra từ <code>artifacts:reports:dotenv</code> có thể dùng trong mệnh đề <code>rules:</code> của job sau không? Tại sao?</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>KHÔNG THỂ</b>. Bởi vì:</p>
    <ul>
      <li>Mệnh đề <code>rules:</code> được GitLab Server tính toán và đánh giá tại <b>thời điểm tạo pipeline (Pipeline Creation Time - t0)</b> để quyết định đưa những job nào vào đồ thị thực thi.</li>
      <li>Trong khi đó, biến trong <code>dotenv</code> chỉ được sinh ra tại <b>thời điểm Job trước chạy xong trên Runner (Runtime)</b>. Tại t0, Job trước chưa hề chạy nên Server không thể biết giá trị của biến dotenv để đánh giá <code>rules:</code>.</li>
      <li>Biến Dotenv chỉ có giá trị bên trong <code>before_script</code>, <code>script</code>, và <code>after_script</code> của các downstream jobs có phụ thuộc (<code>needs</code>/<code>dependencies</code>).</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q07</span>
      <span>Thuộc tính <code>expand: false</code> có ý nghĩa gì và trong trường hợp nào bắt buộc phải kích hoạt?</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Ý nghĩa</b>: <code>expand: false</code> chỉ thị cho GitLab CI không tự động phân tích và thế (expand) các ký tự <code>$</code> xuất hiện trong giá trị của biến.</p>
    <p><b>Trường hợp bắt buộc dùng</b>: Khi giá trị biến chứa mật khẩu phức tạp hoặc chuỗi regex có chứa ký tự <code>$</code> (ví dụ: <code>P@ssw$rd!2026</code> hoặc token mã hóa). Nếu không tắt expand, GitLab sẽ coi <code>$rd</code> là tên của một biến môi trường khác, tự động thay thế bằng chuỗi rỗng khiến mật khẩu bị biến dạng thành <code>P@ssw!2026</code> dẫn đến lỗi xác thực.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q08</span>
      <span>Bật biến <code>CI_DEBUG_TRACE=true</code> mang lại lợi ích gì và tiềm ẩn nguy cơ an ninh nghiêm trọng nào?</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Lợi ích</b>: Kích hoạt chế độ debug chi tiết tầng Shell execution (tương đương <code>set -x</code> trong bash), in toàn bộ từng dòng lệnh shell cùng giá trị biến đã được phân giải ra console log giúp kỹ sư gỡ rối pipeline cực nhanh.</p>
    <p><b>Nguy cơ an ninh</b>: <code>CI_DEBUG_TRACE</code> sẽ in toàn bộ giá trị biến môi trường trong quá trình gán lệnh. Mặc dù Runner cố gắng mask các biến đã đánh dấu, nhưng các biến không được mask (hoặc các biến bị encode/cắt chuỗi trong script) sẽ bị lộ 100% dạng clear-text trên Web UI log, bất kỳ ai có quyền xem pipeline đều thấy được secrets.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q09</span>
      <span>Làm thế nào để truyền biến từ Parent Pipeline sang Downstream / Child Pipeline một cách bảo mật?</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p>Có 3 cách chính:</p>
    <ol>
      <li><b>Dùng <code>trigger:include:</code> kết hợp <code>variables:</code></b>: Khai báo tường minh danh sách biến trong job trigger.</li>
      <li><b>Sử dụng <code>inherit:variables: true/false</code></b>: Mặc định child pipeline kế thừa toàn bộ biến từ parent. Có thể giới hạn bằng <code>inherit:variables: [VAR1, VAR2]</code> để tránh lộ secrets không cần thiết.</li>
      <li><b>Truyền qua <code>artifacts:reports:dotenv</code></b>: Job tạo dotenv file, sau đó job trigger dùng <code>needs: [job_dotenv]</code> để nạp toàn bộ biến động sang child pipeline.</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q10</span>
      <span>Tại sao hệ thống Predefined Variables (CI_*) lại được xếp ở nấc ưu tiên THẤP NHẤT (Nấc 9)? Ý đồ thiết kế của GitLab là gì?</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p>Việc xếp Predefined Variables ở nấc thấp nhất là một <b>chủ đích thiết kế linh hoạt (Design by Intent)</b> của GitLab:</p>
    <ul>
      <li>Cho phép kỹ sư và hệ thống CI có thể <b>Mock hoặc Override</b> các biến hệ thống khi cần thiết (ví dụ: ghi đè <code>CI_ENVIRONMENT_NAME</code> hoặc <code>CI_APPLICATION_TAG</code> trong các kịch bản test đặc biệt, giả lập pipeline môi trường khác).</li>
      <li>Đảm bảo các cấu hình tường minh của lập trình viên trong YAML hoặc Project Settings luôn có quyền quyết định cao hơn các giá trị tự động suy diễn của hệ thống.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q11</span>
      <span>Viết một đoạn script Shell chuẩn Enterprise để áp dụng cơ chế Fail-fast Assertion kiểm tra biến rỗng trước khi chạy lệnh phá hủy.</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p>Đoạn script chuẩn sử dụng cú pháp <b>POSIX Parameter Expansion</b>:</p>
    <div class="language-bash highlighter-rouge"><pre class="highlight"><code><span class="c"># Kiểm tra biến bắt buộc - Dừng ngay lập tức nếu biến chưa khai báo hoặc rỗng</span>
: <span class="s2">"${DEPLOY_ENVIRONMENT:?FATAL: DEPLOY_ENVIRONMENT is not set}"</span>
: <span class="s2">"${DATABASE_PASSWORD:?FATAL: DATABASE_PASSWORD is not set}"</span>

<span class="c"># Khẳng định biến File tồn tại và có dung lượng &gt; 0 byte</span>
: <span class="s2">"${KUBECONFIG:?FATAL: KUBECONFIG variable is missing}"</span>
<span class="nb">test</span> -s <span class="s2">"${KUBECONFIG}"</span> <span class="o">||</span> <span class="o">(</span><span class="nb">echo</span> <span class="s2">"FATAL: Kubeconfig file is empty or missing"</span> <span class="o">&gt;&amp;</span>2 <span class="o">&amp;&amp;</span> <span class="nb">exit </span>1<span class="o">)</span>

<span class="nb">echo</span> <span class="s2">"All assertions passed. Starting safe execution..."</span>
</code></pre></div>
    <p>Cú pháp <code>: "${VAR:?message}"</code> tận dụng lệnh no-op <code>:</code> trong POSIX shell, tốn 0.00 giây thực thi nhưng chặn đứng hoàn toàn rủi ro chạy lệnh khi biến rỗng.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <div class="qa-summary-left">
      <span class="qa-num-badge">Q12</span>
      <span>So sánh việc lưu trữ Secret trong GitLab CI Variables với giải pháp HashiCorp Vault / AWS Secrets Manager kết hợp OIDC.</span>
    </div>
    <span class="qa-chevron">
      <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>GitLab CI Variables (Static Secrets)</b>:</p>
    <ul>
      <li><i>Ưu điểm</i>: Dễ cấu hình, không cần hạ tầng phụ trợ, sẵn có trên giao diện web.</li>
      <li><i>Nhược điểm</i>: Secret tĩnh (Static Long-lived Credentials), khó xoay vòng (rotation), có nguy cơ rò rỉ qua log/artifacts, phân quyền thô theo mức độ Project/Group.</li>
    </ul>
    <p><b>HashiCorp Vault / Cloud Secrets qua OIDC (Dynamic Keyless Secrets)</b>:</p>
    <ul>
      <li><i>Ưu điểm</i>: Chuẩn Zero Trust Enterprise. Không lưu trữ bất kỳ secret tĩnh nào trên GitLab. Job sử dụng <code>CI_JOB_JWT_V2</code> (ID Token OIDC) để xác thực với Vault/AWS STS và nhận về <b>Temporary Credentials có thời hạn 15-60 phút</b>. Tự động thu hồi, phân quyền chi tiết theo từng commit SHA, branch, project path.</li>
      <li><i>Nhược điểm</i>: Cần thiết lập hạ tầng OIDC Trust và quản trị cụm Vault / IAM Roles.</li>
    </ul>
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

### 7.1. Tóm Tắt Các Điểm Cốt Lõi (Key Takeaways)

```text
                              QUẢN TRỊ BIẾN & SECRETS
                                         │
     ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
     ▼                   ▼                               ▼                   ▼
[ 9 NẤC ƯU TIÊN ]   [ MASKED vs PROTECTED ]       [ FILE VARIABLES ]   [ FAIL-FAST DEFENSE ]
Pipeline > Project  Masked: Lọc STDOUT log        Chuyên dụng cho      : "${VAR:?Error}"
> Group > Instance  Protected: Chỉ nạp cho        RSA key, Kubeconfig  Kiểm tra od -c
> Dotenv > Job YAML Protected branches/tags       Tránh lỗi escape     Tắt expand: false
```

- **Quy tắc 9 nấc ưu tiên**: Biến Project và Pipeline Variables luôn ghi đè cấu hình trong `.gitlab-ci.yml`. Luôn kiểm tra API nếu thấy cấu hình YAML không có tác dụng.
- **Bảo vệ Secrets đúng cách**: `Masked` chỉ bảo vệ log stream; `Protected` bảo vệ phạm vi branch; kết hợp `File-type` và `expand: false` để bảo toàn tính toàn vẹn của khóa bảo mật.
- **Chốt chặn an toàn**: Mọi script triển khai bắt buộc cài đặt Assertion `: "${SECRET:?}"` để loại bỏ 100% rủi ro thực thi khi biến mang giá trị rỗng.

### 7.2. Lộ Trình Bài Học Tiếp Theo

Ở bài học tiếp theo, chúng ta sẽ chuyển sang làm chủ toàn diện các kỹ thuật gỡ rối pipeline khi gặp sự cố phức tạp: phương pháp đọc log tầng thấp, kích hoạt Interactive Web Terminal để debug trực tiếp bên trong Runner container và tối ưu hóa chu trình fix bug CI/CD.

> [!TIP]
> **Khám phá bài học tiếp theo**: [Bài 07: Kỹ Thuật Gỡ Rối Pipeline (Troubleshooting & Debugging) — doc-pha.sh, CI_DEBUG_TRACE, Interactive Web Terminal](gitlab-07-07-go-roi-pipeline.html)
{% endraw %}
