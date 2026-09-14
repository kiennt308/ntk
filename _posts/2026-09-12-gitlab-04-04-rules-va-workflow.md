---
layout: post
title: "[Bài 04] Điều Khiển Luồng Thực Thi Nâng Cao Với Rules & Workflow: rules:if, changes, exists & workflow:rules"
date: 2026-09-12 09:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-04
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 4
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.04] Hướng dẫn chuyên sâu Điều Khiển Luồng Thực Thi Nâng Cao Với Rules & Workflow: rules:if, changes, exists & workflow:rules: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Điều Khiển Luồng Thực Thi Nâng Cao Với Rules & Workflow: rules:if, changes, exists & workflow:rules."
  - "Thiết kế CI/CD Pipeline chuẩn Enterprise với kiến trúc DAG, tối ưu hóa thời gian build và caching hiệu quả."
  - "Bảo mật chuỗi cung ứng phần mềm với SAST/DAST, Container Scanning và OIDC Authentication."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 12 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 04] ĐIỀU KHIỂN LUỒNG THỰC THI NÂNG CAO VỚI RULES & WORKFLOW: RULES:IF, CHANGES, EXISTS & WORKFLOW:RULES

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

### 1.1. Luận Đề Trung Tâm: Thời Điểm Đánh Giá $t_0$ & Tính Bất Biến Của Danh Sách Job

Khác biệt bản chất giữa hệ thống CI/CD khai báo tĩnh (Declarative CI) và các hệ thống kịch bản động nằm ở **thời điểm chốt danh sách thực thi (Execution Plan Binding Time)**:

> **`rules` được GitLab CI Parser đánh giá ĐÚNG MỘT LẦN duy nhất tại thời điểm pipeline được khởi tạo ($t_0$), hoàn toàn không phải lúc job sắp sửa được Runner bốc chạy.**

```
   t0: SỰ KIỆN KÍCH HOẠT (git push / MR / tag / schedule / API / Webhook)
        │
        ├─► [TẦNG 1] workflow:rules đánh giá
        │    └── KHÔNG khớp ──▶ HỦY TOÀN BỘ PIPELINE (Silent Dropped - Không có pipeline)
        │
        ├─► [TẦNG 2] rules của TỪNG JOB đánh giá
        │    └── KHÔNG khớp ──▶ LOẠI BỎ KHỎI DANH SÁCH (Job biến mất hoàn toàn)
        │
        └─► DANH SÁCH JOB ĐƯỢC CHỐT CỐ ĐỊNH (Static DAG Ingestion vào PostgreSQL)
             │
   t1..tn:   ├── Runner nhận job từ Queue tĩnh
             ├── Job fail / pass / skipped do upstream fail
             └── Biến do dotenv artifacts sinh ra ──▶ QUÁ MUỘN để ảnh hưởng rules!
```

1. **Tính bất biến (Immutability)**: Khi GitLab ghi nhận danh sách job vào cơ sở dữ liệu tại $t_0$, việc kỹ sư bấm nút **Retry Pipeline** hoặc chỉnh sửa biến môi trường trên giao diện Web UI sau đó sẽ **không làm tính toán lại `rules`**. Để áp dụng rules mới, bắt buộc phải khởi tạo một Pipeline ID hoàn toàn mới.
2. **Hệ quả đối với biến môi trường động**: Các biến môi trường được sinh ra trong quá trình chạy của job trước thông qua `artifacts:reports:dotenv` sinh ra ở thời điểm $t > t_0$. Do đó, chúng **hoàn toàn vô hình** đối với bộ thẩm định `rules:if`.

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Git Client / Webhook
    participant GL as GitLab CI Engine (t0)
    participant DB as Pipeline Database
    participant R as Runner Worker (t1..tn)

    Dev->>GL: Push Event (commit SHA / branch / MR)
    Note over GL: Đánh giá workflow:rules (Tầng 1)
    Note over GL: Đánh giá rules của từng Job (Tầng 2)
    GL->>DB: Persist Execution Plan (Danh sách Job cố định)
    GL-->>Dev: Pipeline Created (ID: #1042)
    
    loop Polling Execution
        R->>DB: Request Next Job
        DB-->>R: Dispatch Job Payload
        R->>R: Execute Scripts & Generate Dotenv
        Note over R: Biến sinh ra ở t1 không thể sửa DB tại t0!
    end
```

### 1.2. Hai Tầng Lọc Độc Lập: `workflow:rules` vs `rules`

Hệ thống điều phối của GitLab chia thành 2 tầng lọc phân cấp nghiêm ngặt:
- **Tầng 1: `workflow:rules` (Pipeline-level Gate)**: Quyết định *toàn bộ pipeline có được cấp phép khởi tạo hay không*. Nếu `workflow:rules` đánh giá ra `when: never` (hoặc không khớp rule nào), GitLab sẽ không tạo pipeline, không tốn bất kỳ bản ghi cơ sở dữ liệu hay tài nguyên Runner nào.
- **Tầng 2: `rules:` của từng Job (Job-level Gate)**: Chỉ được đánh giá khi Tầng 1 đã cho phép tạo pipeline. Tầng này quyết định *job cụ thể có xuất hiện trong danh sách thực thi của pipeline hay không*.

### 1.3. Cơ Chế First-Match-Wins & Bốn Loại Điều Kiện

Danh sách `rules` hoạt động theo nguyên lý **Khớp đầu tiên thì thắng (First-match-wins)**. GitLab duyệt mảng `rules` tuần tự từ trên xuống dưới; ngay khi gặp điều kiện đầu tiên thỏa mãn logic, nó áp dụng ngay các thuộc tính (`when`, `allow_failure`, `variables`) của mục đó và **dừng duyệt toàn bộ các rule phía sau**.

Bốn loại biểu thức điều kiện trong một rule:
1. `if`: Biểu thức so sánh chuỗi, regex hoặc kiểm tra sự tồn tại của biến môi trường hệ thống có sẵn tại $t_0$ (ví dụ: `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`).
2. `changes`: Kiểm tra sự thay đổi của tập tin/thư mục dựa trên **mốc so sánh (compare base)**.
3. `exists`: Kiểm tra sự tồn tại vật lý của tập tin trong cây mã nguồn tại commit mục tiêu (ví dụ: `exists: [Dockerfile]`).
4. `when`: Chỉ thị kết quả điều phối (`on_success`, `manual`, `always`, `never`, `delayed`).

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

### 2.1. Ma Trận Ba Trạng Thái "Job Không Chạy"

| Tiêu chí Kỹ thuật | Trạng thái 1: Không có mặt (Omitted) | Trạng thái 2: Manual Trigger (`manual`) | Trạng thái 3: Bị bỏ qua (`skipped`) |
|---|---|---|---|
| **Nguyên nhân cốt lõi** | `rules:` không khớp hoặc rơi vào `when: never` | `when: manual` trong rules hoặc khai báo job | Job trước đó bị lỗi (Non-zero exit code) |
| **Thời điểm quyết định** | Tại $t_0$ (Lúc tạo pipeline) | Tại $t > t_0$ (Chờ người dùng/API kích hoạt) | Tại $t > t_0$ (Khi upstream job kết thúc thất bại) |
| **Xuất hiện trong Pipeline API** | **Hoàn toàn KHÔNG** (0 byte metadata) | **CÓ** (`status: manual`) | **CÓ** (`status: skipped`) |
| **Giao diện trực quan** | Biến mất không dấu vết | Nút Play chờ bấm | Khối xám có biểu tượng Skip |
| **Tác động lên Downstream** | **Không chặn** (DAG tự động co gọn) | Phụ thuộc vào `allow_failure` | **Chặn hoàn toàn** các job phụ thuộc |
| **Phân loại rủi ro sự cố** | **Silent Drop** (Cực kỳ nguy hiểm nếu là Gate) | Chờ phê duyệt nghiệp vụ | Thất bại chuẩn mực (Fast fail) |

### 2.2. Ma Trận Bảng Chân Trị 6 Nguồn Kích Hoạt $	imes$ Điều Kiện Rules

Bảng chân trị thực nghiệm đo đạc hành vi thực tế của các biểu thức rules phổ biến trên 6 nguồn kích hoạt pipeline:

| Biểu thức Rule (`rules:if`) | 1. Push Branch Thường | 2. Push Default Branch | 3. Merge Request Event | 4. Git Tag Push | 5. Pipeline Schedule | 6. Trigger / API Call |
|---|---|---|---|---|---|---|
| `if: $CI_PIPELINE_SOURCE == "merge_request_event"` | ❌ KHÔNG | ❌ KHÔNG | ✅ **CÓ** | ❌ KHÔNG | ❌ KHÔNG | ❌ KHÔNG |
| `if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH` | ❌ KHÔNG | ✅ **CÓ** | ❌ KHÔNG ($CI_COMMIT_BRANCH null trong detached MR) | ❌ KHÔNG | ✅ CÓ (Nếu schedule trỏ default) | ✅ CÓ (Nếu ref=default) |
| `if: $CI_COMMIT_TAG` | ❌ KHÔNG | ❌ KHÔNG | ❌ KHÔNG | ✅ **CÓ** | ❌ KHÔNG | ❌ KHÔNG |
| `if: $CI_PIPELINE_SOURCE == "schedule"` | ❌ KHÔNG | ❌ KHÔNG | ❌ KHÔNG | ❌ KHÔNG | ✅ **CÓ** | ❌ KHÔNG |
| `changes: [src/**/*]` (Không compare_to) | ✅ CÓ (So commit trước) | ✅ CÓ (So commit trước) | ✅ CÓ (So target branch) | ❌ KHÔNG | ❌ **KHÔNG (Không có diff commit)** | ❌ **KHÔNG** |
| `when: always` | ✅ CÓ | ✅ CÓ | ✅ CÓ | ✅ CÓ | ✅ CÓ | ✅ CÓ |

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (Architecture Breakdown)

### 3.1. Sơ Đồ Điều Phối Workflow Tránh Pipeline Trùng Lặp (Duplicate Pipelines)

Khi một nhánh tính năng đang mở Merge Request và tiếp tục được push commit, nếu không cấu hình `workflow:rules` chuẩn, GitLab sẽ tự động kích hoạt **2 pipeline chạy song song cho cùng 1 commit SHA**:
1. Pipeline nguồn `push`: Chạy trên context của branch.
2. Pipeline nguồn `merge_request_event`: Chạy trên context của MR (có các biến `$CI_MERGE_REQUEST_*`).

```
                    SỰ KIỆN: GIT PUSH LÊN NHÁNH ĐANG CÓ MR MỞ
                                       │
                ┌──────────────────────┴──────────────────────┐
                │                                             │
    [KHÔNG CÓ WORKFLOW:RULES]                       [CÓ WORKFLOW:RULES CHUẨN]
                │                                             │
    ┌───────────┴───────────┐                     ┌───────────┴───────────┐
    ▼                       ▼                     ▼                       ▼
Pipeline 1 (push)    Pipeline 2 (MR)        Pipeline Push          Pipeline MR
(Chạy lãng phí 6m)   (Chạy lãng phí 6m)     (Bị NEVER chặn)       (Chạy duy nhất)
    │                       │                     │                       │
    └───────────┬───────────┘                     └───▶ TIẾT KIỆM 50% ◀───┘
                ▼                                       RUNNER MINUTES
      LÃNG PHÍ 100% RUNNER
```

### 3.2. Cấu Hình Production Chuẩn Mực `.gitlab-ci.yml`

```yaml
# ==============================================================================
# ENTERPRISE WORKFLOW & DYNAMIC RULES GOVERNANCE TEMPLATE
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Pipeline-level Gate: Triệt tiêu hoàn toàn Duplicate Pipelines
# ------------------------------------------------------------------------------
workflow:
  rules:
    # Rule 1: Ưu tiên tối cao cho Merge Request Pipeline
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    # Rule 2: Chặn pipeline push nếu nhánh đó ĐANG có MR mở
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    # Rule 3: Luôn cho phép chạy trên nhánh mặc định (main/master)
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    # Rule 4: Luôn cho phép chạy khi gắn Git Tag (Release build)
    - if: $CI_COMMIT_TAG
    # Rule 5: Chạy pipeline theo lịch định kỳ
    - if: $CI_PIPELINE_SOURCE == "schedule"
    # Rule 6: Cho phép push trên các nhánh tính năng chưa tạo MR
    - if: $CI_COMMIT_BRANCH

stages:
  - .pre
  - test
  - build
  - deploy

default:
  image: alpine:3.20

# ------------------------------------------------------------------------------
# 2. Pre-flight Security: Chặn hoàn toàn rủi ro biến mất im lặng
# ------------------------------------------------------------------------------
security-gatekeeper:
  stage: .pre
  image: zricethezav/gitleaks:latest
  rules:
    # Rule security PHẢI chạy trên mọi pipeline được tạo ra
    - when: always
  script:
    - gitleaks git --verbose --redact

# ------------------------------------------------------------------------------
# 3. Job-level Conditional Rules: Áp dụng First-match-wins
# ------------------------------------------------------------------------------
unit-tests:
  stage: test
  rules:
    # Chạy khi có thay đổi trong src/ hoặc khi chạy trên default branch / MR
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        paths:
          - src/**/*
          - package.json
    - if: $CI_PIPELINE_SOURCE == "schedule" # Luôn chạy khi quét định kỳ
  script:
    - echo "Executing comprehensive unit test suites..."

build-artifacts:
  stage: build
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script:
    - mkdir -p dist && echo "PACKAGE_PROD_v2026" > dist/app.bundle
    - test -s dist/app.bundle || { echo "Build output invalid!"; exit 1; }
  artifacts:
    paths:
      - dist/
    expire_in: 1 day

# ------------------------------------------------------------------------------
# 4. Production Manual Deploy: Khai báo allow_failure tường minh
# ------------------------------------------------------------------------------
deploy-to-production:
  stage: deploy
  rules:
    # Điều kiện riêng: Chỉ deploy manual trên Tag hoặc Default branch
    - if: $CI_COMMIT_TAG
      when: manual
      allow_failure: false # Bắt buộc phê duyệt để hoàn thành pipeline
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
      allow_failure: true  # Cho phép pipeline xanh dù chưa bấm deploy
  script:
    - echo "Deploying release payload to Kubernetes Cluster..."
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

### 4.1. Incident 1: Security Gate Biến Mất Im Lặng Do Sử Dụng `rules:changes` Trên Lịch Trình

```
                        SỰ CỐ SILENT SECURITY DROP
  ┌────────────────────────────────────────────────────────────────────────┐
  │ Job SAST Security Scanner: Cấu hình `rules:changes: [src/**]`          │
  │ Pipeline Schedule hàng đêm (02:00 AM) được kích hoạt                   │
  ├────────────────────────────────────────────────────────────────────────┤
  │ Schedule Engine: Không có commit diff nào được tạo ra                   │
  │ GitLab Rules Parser: `changes` đánh giá FALSE                          │
  │ Scheduler: Loại bỏ SAST Scanner khỏi pipeline (Omitted)                 │
  │ Pipeline Report: Báo SUCCESS (Xanh 100%) -> Lỗ hổng 0-day lọt qua!     │
  └────────────────────────────────────────────────────────────────────────┘
```

- **Hiện tượng**: Pipeline quét mã độc và lỗ hổng bảo mật hàng đêm (Nightly Security Audit) liên tục báo trạng thái `Passed` (màu xanh), nhưng khi chuyên gia an ninh rà soát thì phát hiện mã nguồn chứa thư viện có lỗ hổng Critical CVE-2026-8812 đã tồn tại 3 tuần.
- **Phân tích 5-Whys**:
  1. *Tại sao lỗ hổng Critical không bị phát hiện?* Vì job `sast-container-scan` không hề chạy trong các pipeline hàng đêm.
  2. *Tại sao job không chạy khi lịch schedule vẫn kích hoạt đều đặn?* Vì job được cấu hình `rules: - changes: [src/**/*, Dockerfile]`.
  3. *Tại sao `changes` lại không kích hoạt trên schedule?* Trong pipeline theo lịch (`CI_PIPELINE_SOURCE == "schedule"`), không có commit mới được đẩy lên, mốc so sánh commit diff trả về rỗng, dẫn đến `changes` luôn trả về `false`.
  4. *Tại sao hệ thống không báo lỗi khi job bị bỏ qua?* Khi `rules` đánh giá không khớp, job bị **loại bỏ hoàn toàn (Omitted)** chứ không phải `failed` hay `skipped`. Pipeline không còn job nào bị lỗi nên GitLab đánh dấu toàn bộ pipeline là `success`.
  5. *Nguyên nhân gốc rễ (Root Cause)*: Kỹ sư áp dụng cẩu thả từ khóa `rules:changes` vào các job thuộc danh mục An ninh / Compliance mà không nhận thức được 3 trường hợp sai lệch kinh điển của `changes`.
- **Giải pháp triệt để**: Tuyệt đối **không sử dụng `rules:changes` độc lập cho các chốt kiểm soát an ninh (Security Gates)**. Luôn bổ sung rule chạy bắt buộc:
  ```yaml
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule" # Luôn chạy khi quét định kỳ
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - changes: [src/**/*]
  ```

### 4.2. Incident 2: Sử Dụng Biến `dotenv` Trong `rules:if` Khiến Pipeline Mất Job Deploy

- **Hiện tượng**: Job tính toán phiên bản động `calculate-semver` sinh ra biến `RELEASE_TAG=v2.1.0` ghi vào `reports:dotenv`, nhưng job `deploy-package` downstream có điều kiện `rules: - if: '$RELEASE_TAG =~ /^v/'` không bao giờ được kích hoạt.
- **Phân tích 5-Whys**:
  1. *Tại sao job deploy không được kích hoạt?* Vì biểu thức regex trong `rules:if` đánh giá biến `$RELEASE_TAG` là chuỗi rỗng (`null`).
  2. *Tại sao biến lại rỗng trong khi log của job `calculate-semver` đã xuất file `.env` thành công?* Vì `reports:dotenv` chỉ nạp biến vào môi trường thực thi khi job bắt đầu chạy (thời điểm $t_1$).
  3. *Tại sao `rules:if` không đọc được biến đó?* Vì toàn bộ `rules:if` của pipeline được tính toán tại thời điểm khởi tạo pipeline ($t_0$), trước khi bất kỳ Runner nào nhận job đầu tiên.
  4. *Tại sao kỹ sư lại thiết kế như vậy?* Do nhầm lẫn giữa phạm vi của biến môi trường runtime và metadata lập lịch của pipeline engine.
  5. *Nguyên nhân gốc rễ (Root Cause)*: Vi phạm nguyên lý cơ bản: `dotenv` là cơ chế runtime sau $t_0$, không thể can thiệp vào bộ lập lịch tĩnh.
- **Giải pháp triệt để**: Sử dụng các biến hệ thống sẵn có tại $t_0$ (như `$CI_COMMIT_TAG`, `$CI_COMMIT_BRANCH`) để điều khiển `rules`, và xử lý logic kiểm tra biến `dotenv` trực tiếp bên trong khối `script: [...]`.

---

## 5. Hands-on Lab: Điều Khiển Luồng Thực Thi với Rules & Workflow (8 Bước Chuẩn)

### 5.1. Bước 1: Khởi Tạo Môi Trường Lab & Bộ Đo Đạc API `ci/lint`

Thiết lập project cô lập trên GitLab và tạo các công cụ đo kiểm qua API:

```bash
export GITLAB="http://gitlab.lab:8929"
export GITLAB_TOKEN="glpat-StandardLabTokenAdmin2026"
export HAU_TO="devops-rules"

# Tạo Project Lab 04
PID4=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN"   --header "Content-Type: application/json"   --data "{"name":"lab04-rules-workflow-${HAU_TO}","visibility":"internal"}"   "$GITLAB/api/v4/projects" | jq -r .id)

echo "Lab Project ID: $PID4"

mkdir -p ~/lab04 && cd ~/lab04
git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/root/lab04-rules-workflow-${HAU_TO}.git"
git config user.email "lab@internal.corp"
git config user.name "Lab Engineer"

mkdir -p src docs
echo "initial app source" > src/app.js
echo "initial doc content" > docs/readme.md

cat > cong-cu.sh <<'SH'
#!/usr/bin/env bash
A="$GITLAB/api/v4/projects/$PID4"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")

lint_eval() {
  curl -sf --request POST "${H[@]}" --header "Content-Type: application/json"     --data "$(jq -Rs '{content: ., include_merged_yaml: true}' < "${1:-.gitlab-ci.yml}")"     "$A/ci/lint"
}
list_pipeline_jobs() {
  curl -sf "${H[@]}" "$A/pipelines/$1/jobs?per_page=100" | jq -r '.[] | [.name, .stage, .status] | @tsv'
}
check_job_exists() {
  curl -sf "${H[@]}" "$A/pipelines/$1/jobs?per_page=100" | jq -r --arg n "$2" '[.[] | select(.name==$n)] | length'
}
SH
source cong-cu.sh
```

### 5.2. Bước 2: Đo Lường Thực Nghiệm Bảng Chân Trị (Truth Table Verification)

Xây dựng pipeline thử nghiệm 5 loại rules để đo đạc ma trận kích hoạt:

```yaml
# ~/lab04/.gitlab-ci.yml
stages:
  - verify

.base_checker:
  stage: verify
  image: alpine:3.20
  script:
    - echo "Trigger Source: ${CI_PIPELINE_SOURCE}, Branch: ${CI_COMMIT_BRANCH}, Tag: ${CI_COMMIT_TAG}"

rule_always:
  extends: .base_checker
  rules:
    - when: always

rule_branch_main_only:
  extends: .base_checker
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

rule_mr_only:
  extends: .base_checker
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

rule_tag_only:
  extends: .base_checker
  rules:
    - if: $CI_COMMIT_TAG

rule_changes_src:
  extends: .base_checker
  rules:
    - changes: [src/**/*]
```

Đẩy lên nhánh `main` và kiểm tra danh sách job:

```bash
cd ~/lab04
git add . && git commit -m "lab: initialize truth table testing" && git push -u origin main
sleep 20

PIPE_MAIN=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipelines?ref=main&per_page=1" | jq -r '.[0].id')
echo "=== DANH SÁCH JOB TRÊN NHÁNH MAIN (PIPE: $PIPE_MAIN) ==="
list_pipeline_jobs "$PIPE_MAIN"
```

> **CHECKPOINT 1**: Trên nhánh `main`, `rule_always`, `rule_branch_main_only`, và `rule_changes_src` xuất hiện; `rule_mr_only` và `rule_tag_only` **hoàn toàn biến mất** khỏi danh sách job (Omitted).

### 5.3. Bước 3: Tái Hiện Hiện Tượng Duplicate Pipelines Khi Mở Merge Request

Tạo nhánh tính năng, đẩy commit và mở Merge Request để quan sát số lượng pipeline sinh ra:

```bash
cd ~/lab04
git checkout -b feature/user-auth
echo "function auth() { return true; }" >> src/app.js
git add src/app.js && git commit -m "feat: implement user auth logic"
git push -u origin feature/user-auth

# Mở Merge Request qua API
MR_IID=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN"   --header "Content-Type: application/json"   --data '{"source_branch":"feature/user-auth","target_branch":"main","title":"Feat: User Authentication"}'   "$A/merge_requests" | jq -r .iid)

echo "Created Merge Request !${MR_IID}"

# Tiếp tục push commit thứ 2 vào nhánh khi MR đang mở
echo "// additional patch" >> src/app.js
git add src/app.js && git commit -m "fix: minor security patch"
git push origin feature/user-auth
sleep 25

# Đếm số pipeline sinh ra theo SHA
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipelines?per_page=10"   | jq -r 'group_by(.sha) | .[] | {sha: .[0].sha[0:8], count: length, sources: [.[].source]}'
```

> **CHECKPOINT 2**: Commit SHA mới nhất ghi nhận `count: 2` với 2 nguồn kích hoạt đồng thời: `push` và `merge_request_event`. Tỷ lệ lãng phí tài nguyên là 100%.

### 5.4. Bước 4: Khắc Phục Triệt Để Bằng Khối `workflow:rules` Chuẩn Hóa

Bổ sung khối `workflow:rules` vào đầu tệp `.gitlab-ci.yml`:

```yaml
# ~/lab04/.gitlab-ci.yml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH

stages:
  - verify

.base_checker:
  stage: verify
  image: alpine:3.20
  script:
    - echo "Verified on pipeline source ${CI_PIPELINE_SOURCE}"

test_execution:
  extends: .base_checker
  rules:
    - when: always
```

Cập nhật mã nguồn và đẩy lên nhánh `feature/user-auth`:

```bash
cd ~/lab04
git add .gitlab-ci.yml && git commit -m "ci: enforce workflow rules to deduplicate"
git push origin feature/user-auth
sleep 20

curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipelines?per_page=5"   | jq -r 'group_by(.sha) | .[] | {sha: .[0].sha[0:8], count: length, sources: [.[].source]}'
```

> **CHECKPOINT 3**: Commit SHA mới nhất chỉ tạo đúng **1 pipeline duy nhất** thuộc nguồn `merge_request_event`. Rule `when: never` đã loại bỏ thành công pipeline nguồn `push`.

### 5.5. Bước 5: Thực Nghiệm Nguyên Tắc First-Match-Wins & Cạm Bẫy Đảo Thứ Tự

Chứng minh thứ tự khai báo rule quyết định trực tiếp đến thuộc tính `when`:

```yaml
# ~/lab04/.gitlab-ci.yml
stages:
  - deploy_test

# Cấu hình SAI: Rule chung đứng trước rule riêng
deploy_wrong_order:
  stage: deploy_test
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_BRANCH # Khớp MỌI branch -> when mặc định là on_success
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual # Không bao giờ được duyệt tới!
  script:
    - echo "Deploying..."

# Cấu hình ĐÚNG: Rule riêng đứng trước rule chung
deploy_correct_order:
  stage: deploy_test
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual # Duyệt trúng trước khi xét rule chung
    - if: $CI_COMMIT_BRANCH
  script:
    - echo "Deploying..."
```

Kiểm tra trạng thái qua CI Lint API:

```bash
cd ~/lab04
git checkout main
git add .gitlab-ci.yml && git commit -m "lab: test first match wins precedence" && git push origin main
sleep 20

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipelines?ref=main&per_page=1" | jq -r '.[0].id')
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipelines/$PIPE_ID/jobs"   | jq -r '.[] | [.name, .status, .when] | @tsv'
```

> **CHECKPOINT 4**: `deploy_wrong_order` tự động thực thi ngay (`status: running/success`), trong khi `deploy_correct_order` dừng lại ở trạng thái `status: manual`.

### 5.6. Bước 6: Phân Tích Thực Nghiệm 3 Trường Hợp Sai Của `rules:changes`

Tạo một nhánh hoàn toàn mới `feature/docs-only` và chỉ sửa đổi tệp trong thư mục `docs/`:

```bash
cd ~/lab04
git checkout main
git checkout -b feature/docs-only
echo "Updated documentation" >> docs/readme.md

# Pipeline chứa job theo dõi src/
cat > .gitlab-ci.yml <<'EOF'
stages:
  - test

service_src_build:
  stage: test
  image: alpine:3.20
  rules:
    - changes: [src/**/*]
  script:
    - echo "Building service src..."
EOF

git add . && git commit -m "docs: update readmes without touching src"
git push -u origin feature/docs-only
sleep 20

PIPE_DOCS=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipelines?ref=feature/docs-only&per_page=1" | jq -r '.[0].id')
echo "Job count for docs-only commit on NEW branch:"
check_job_exists "$PIPE_DOCS" "service_src_build"
```

> **CHECKPOINT 5**: Kết quả trả về `1` (Job vẫn chạy!). Vì trên nhánh mới tạo chưa có commit cơ sở trước đó, GitLab Runner coi như *mọi tệp tin đều thay đổi*.

Khắc phục bằng `compare_to`:

```yaml
service_src_build:
  stage: test
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_BRANCH
      changes:
        paths: [src/**/*]
        compare_to: refs/heads/main
  script:
    - echo "Building service src..."
```

### 5.7. Bước 7: Đo Lường 3 Trạng Thái "Job Không Chạy" & Cơ Chế `allow_failure`

Thực nghiệm đo đạc sự khác biệt giữa `omitted`, `manual` và `skipped`:

```yaml
# ~/lab04/.gitlab-ci.yml
stages:
  - stage_one
  - stage_two

job_omitted_by_rule:
  stage: stage_one
  image: alpine:3.20
  rules:
    - if: $NON_EXISTENT_VARIABLE == "active"
  script: [echo "never runs"]

job_manual_in_rules:
  stage: stage_one
  image: alpine:3.20
  rules:
    - when: manual
  script: [echo "manual triggered"]

job_manual_direct:
  stage: stage_one
  image: alpine:3.20
  when: manual
  script: [echo "manual triggered direct"]

job_trigger_fail:
  stage: stage_one
  image: alpine:3.20
  script: [exit 1]

job_downstream_skipped:
  stage: stage_two
  image: alpine:3.20
  script: [echo "will be skipped"]
```

```bash
cd ~/lab04
git checkout main
git add .gitlab-ci.yml && git commit -m "lab: verify 3 non-running states" && git push origin main
sleep 25

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipelines?ref=main&per_page=1" | jq -r '.[0].id')
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipelines/$PIPE_ID/jobs"   | jq -r '.[] | [.name, .status, (.allow_failure|tostring)] | @tsv'
```

> **CHECKPOINT 6**: 
> - `job_omitted_by_rule`: Không xuất hiện trong danh sách trả về của API.
> - `job_manual_in_rules`: Có trạng thái `manual` và `allow_failure: true`.
> - `job_manual_direct`: Có trạng thái `manual` và `allow_failure: false`.
> - `job_downstream_skipped`: Có trạng thái `skipped`.

### 5.8. Bước 8: Kiểm Chứng Tính Bất Biến Tại $t_0$ & Dọn Dẹp Tài Nguyên

Chứng minh rằng retry không tính toán lại `rules`:

```bash
# 1. Đặt biến project làm job không đủ điều kiện chạy
curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" --header "Content-Type: application/json"   --data '{"key":"FEATURE_FLAG","value":"disabled"}' "$A/variables"

cat > .gitlab-ci.yml <<'EOF'
stages: [test]
feature_job:
  stage: test
  image: alpine:3.20
  rules:
    - if: $FEATURE_FLAG == "enabled"
  script: [echo "Feature Active"]
EOF

git add .gitlab-ci.yml && git commit -m "test: verify immutability at t0" && git push origin main
sleep 20
PIPE_T0=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipelines?ref=main&per_page=1" | jq -r '.[0].id')
echo "Số lượng job tại t0 (Flag disabled): $(check_job_exists "$PIPE_T0" "feature_job")"

# 2. Đổi biến thành enabled và thực hiện Retry pipeline cũ
curl -sf --request PUT --header "PRIVATE-TOKEN: $GITLAB_TOKEN" --header "Content-Type: application/json"   --data '{"value":"enabled"}' "$A/variables/FEATURE_FLAG"

curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipelines/$PIPE_T0/retry"
sleep 15
echo "Số lượng job sau RETRY (Flag enabled): $(check_job_exists "$PIPE_T0" "feature_job")"

# 3. Tạo pipeline MỚI với biến mới
PIPE_NEW=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A/pipeline?ref=main" | jq -r .id)
sleep 20
echo "Số lượng job trên PIPELINE MỚI: $(check_job_exists "$PIPE_NEW" "feature_job")"

# Dọn dẹp Project Lab 04
curl -sf --request DELETE --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$A"
echo "Lab 04 cleaned up successfully."
```

> **CHECKPOINT 7 & 8**: `feature_job` vẫn trả về `0` sau khi Retry pipeline cũ, nhưng trả về `1` trên Pipeline Mới tạo. Toàn bộ môi trường lab được dọn dẹp an toàn.

---

## 6. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span>Thời điểm đánh giá (Evaluation Time) của từ khóa `rules` diễn ra khi nào? Nêu 2 hệ quả kiến trúc then chốt của nguyên lý này?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Thời điểm đánh giá</b>: <code>rules</code> được đánh giá <b>đúng một lần duy nhất tại thời điểm khởi tạo pipeline ($t_0$)</b>, trước khi pipeline được lưu vào cơ sở dữ liệu và trước khi bất kỳ Runner nào tiếp nhận job.</p>
    <p><b>Hai hệ quả kiến trúc then chốt</b>:</p>
    <ol>
      <li><b>Tính bất biến khi Retry</b>: Thao tác Retry một job hoặc Retry toàn bộ pipeline không làm Parser tính toán lại <code>rules</code>. Nếu biến môi trường bị đổi sau $t_0$, job bị loại bỏ vẫn sẽ không xuất hiện lại.</li>
      <li><b>Biến động (Dynamic Variables) không thể dùng trong rules</b>: Các biến môi trường sinh ra trong runtime từ các job trước (như <code>reports:dotenv</code>) không thể dùng làm điều kiện cho <code>rules:if</code> của job sau vì chúng chưa tồn tại tại $t_0$.</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span>Tại sao biến môi trường xuất ra từ `artifacts:reports:dotenv` không thể sử dụng trong biểu thức `rules:if` của job phía sau? Cách giải quyết chuẩn là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Nguyên nhân</b>: Lệch pha thời gian giữa $t_0$ và $t_1$. <code>rules:if</code> thẩm định tại $t_0$, trong khi file dotenv chỉ được tạo ra và nạp vào Runner tại $t_1$ (khi job phía trước chạy xong). Tại $t_0$, Parser thấy biến đó có giá trị rỗng (<code>null</code>) nên rule đánh giá ra <code>false</code> $ightarrow$ Job biến mất trong im lặng.</p>
    <p><b>Giải pháp chuẩn</b>:</p>
    <ul>
      <li>Sử dụng các biến tĩnh có sẵn tại $t_0$ (như <code>$CI_COMMIT_TAG</code>, <code>$CI_PIPELINE_SOURCE</code>) để điều khiển <code>rules</code> của job.</li>
      <li>Kiểm tra biến dotenv bên trong khối lệnh <code>script: [...]</code> kèm lệnh assertion:
        <pre><code class="language-bash">test -n "$DYNAMIC_VAR" || { echo "ERROR: Dynamic variable missing"; exit 1; }</code></pre>
      </li>
      <li>Nếu bắt buộc phải quyết định cấu trúc DAG động dựa trên dữ liệu runtime, sử dụng giải pháp <b>Dynamic Child Pipeline</b> (Tạo tệp YAML con rồi kích hoạt qua <code>trigger:include:artifact</code>).</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span>Phân biệt chi tiết 3 trạng thái "Job không chạy": Omitted (Không có mặt), Manual Trigger (`manual`), và Skipped (`skipped`). Trạng thái nào nguy hiểm nhất?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Bảng phân biệt kỹ thuật</b>:</p>
    <ul>
      <li><b>Omitted (Không có mặt)</b>: Xảy ra do <code>rules</code> không khớp tại $t_0$. Job không hề được tạo ra trong DB, không có Job ID, API trả về rỗng, và <b>không chặn</b> các job phía sau.</li>
      <li><b>Manual</b>: Job có tồn tại trong DB nhưng ở trạng thái chờ người dùng hoặc API bấm nút kích hoạt.</li>
      <li><b>Skipped</b>: Job có tồn tại trong DB nhưng bị bỏ qua vì một job ở stage trước đó bị failed. Trạng thái này sẽ <b>chặn toàn bộ downstream</b>.</li>
    </ul>
    <p><b>Trạng thái nguy hiểm nhất</b>: <b>Omitted (Không có mặt)</b>. Nếu một chốt kiểm soát an ninh (Security Gate) bị rơi vào trạng thái này, toàn bộ pipeline vẫn xanh mượt mà không ai biết rằng bước quét lỗ hổng đã bị bỏ qua hoàn toàn.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span>Hiện tượng Duplicate Pipelines (Pipeline trùng lặp) là gì? Tại sao nó xảy ra và làm thế nào để loại bỏ triệt để bằng `workflow:rules`?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Nguyên nhân</b>: Khi một commit được push lên một branch đang có Merge Request mở, GitLab nhận được 2 sự kiện riêng biệt: sự kiện <code>push</code> và sự kiện <code>merge_request_event</code>. Mặc định, GitLab tạo 2 pipeline song song cho cùng 1 commit SHA, gây lãng phí 100% thời gian Runner.</p>
    <p><b>Giải pháp chuẩn hóa với `workflow:rules`</b>:</p>
    <pre><code class="language-yaml">workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH</code></pre>
    <p><i>Lưu ý quan trọng</i>: Rule <code>when: never</code> bắt buộc phải đặt <b>sau</b> rule <code>merge_request_event</code> để chỉ triệt tiêu pipeline push mà vẫn giữ lại pipeline Merge Request.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span>Nguyên tắc "First-match-wins" trong `rules` hoạt động như thế nào? Nêu ví dụ về lỗi logic nghiêm trọng khi đảo thứ tự rule?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Cơ chế</b>: GitLab Parser duyệt mảng <code>rules</code> từ trên xuống dưới. Ngay khi một rule trả về <code>true</code>, nó lấy ngay cấu hình của rule đó và <b>dừng thẩm định</b> toàn bộ mảng còn lại.</p>
    <p><b>Ví dụ lỗi logic kinh điển</b>:</p>
    <pre><code class="language-yaml"># LỖI: Đặt điều kiện tổng quát trước điều kiện đặc thù
rules:
  - if: $CI_COMMIT_BRANCH # Khớp MỌI branch (bao gồm main) -> when: on_success
  - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    when: manual          # KHÔNG BAO GIỜ ĐƯỢC DUYỆT TỚI!</code></pre>
    <p><i>Hậu quả</i>: Job deploy tự động chạy trên nhánh <code>main</code> thay vì dừng lại chờ kích hoạt thủ công, dẫn đến rủi ro release ngoài tầm kiểm soát.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span>Khi một job không khớp bất kỳ điều kiện nào trong mảng `rules`, hành vi mặc định của GitLab là gì? Thêm `- when: never` ở cuối có thực sự cần thiết?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Hành vi mặc định</b>: Nếu duyệt hết mảng <code>rules</code> mà không có điều kiện nào trả về <code>true</code>, GitLab mặc định coi kết quả là <code>when: never</code> và <b>loại bỏ job hoàn toàn khỏi pipeline</b>.</p>
    <p><b>Tính cần thiết của `- when: never`</b>: Về mặt kỹ thuật là <b>dư thừa</b> (Redundant) vì hành vi mặc định đã là loại bỏ. Tuy nhiên, trong một số tiêu chuẩn coding của doanh nghiệp, việc ghi rõ <code>- when: never</code> ở cuối được khuyến khích để thể hiện tính tường minh (Explicit default fallback).</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span>Phân tích 3 trường hợp `rules:changes` hoạt động âm thầm sai hoặc không như kỳ vọng. Tại sao không nên dùng `changes` cho Security Gate?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>3 trường hợp sai lệch kinh điển của `changes`</b>:</p>
    <ol>
      <li><b>Nhánh mới tạo (New branch)</b>: Do chưa có commit trước đó trên branch, GitLab Runner coi <i>toàn bộ tệp tin trong repository đều bị thay đổi</i> $ightarrow$ Chạy thừa toàn bộ các job.</li>
      <li><b>Pipeline theo lịch (Schedule)</b>: Không có commit diff nào được tạo ra tại thời điểm schedule chạy $ightarrow$ <code>changes</code> trả về <code>false</code> $ightarrow$ Bỏ qua toàn bộ các job.</li>
      <li><b>Push nhiều commit cùng lúc</b>: Diff chỉ so sánh giữa HEAD và commit trước đợt push, có thể bỏ sót các trạng thái trung gian.</li>
    </ol>
    <p><b>Tại sao không dùng cho Security Gate</b>: Tính bất đối xứng của rủi ro. Job build chạy thừa chỉ tốn 30s Runner, nhưng Security Gate bị biến mất im lặng sẽ tạo ra lỗ hổng bảo mật nghiêm trọng trên Production mà không ai hay biết.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span>So sánh sự khác biệt cốt lõi giữa hai tầng lọc `workflow:rules` (Pipeline level) và `rules` (Job level)?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Bảng so sánh 2 tầng lọc</b>:</p>
    <ul>
      <li><b>Phạm vi kiểm soát</b>: <code>workflow:rules</code> kiểm soát sự tồn tại của <i>toàn bộ Pipeline instance</i>; <code>rules</code> kiểm soát sự xuất hiện của <i>từng Job đơn lẻ</i>.</li>
      <li><b>Thứ tự thực thi</b>: <code>workflow:rules</code> luôn được đánh giá <b>trước</b>. Nếu tầng này không cho phép, Parser hủy ngay lập tức và không bao giờ đọc đến <code>rules</code> của từng job.</li>
      <li><b>Giá trị chẩn đoán</b>: Khi job không chạy, bước 1 là kiểm tra xem có pipeline nào được tạo không. Nếu không có pipeline $ightarrow$ Lỗi tại tầng <code>workflow:rules</code>; nếu có pipeline nhưng thiếu job $ightarrow$ Lỗi tại <code>rules</code> của job đó.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span>Giá trị mặc định của `allow_failure` khác nhau như thế nào khi `when: manual` được đặt trong `rules` so với khi khai báo trực tiếp ở cấp Job?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Sự khác biệt về giá trị mặc định</b>:</p>
    <ul>
      <li>Khi khai báo <b>bên trong `rules:`</b> (<code>rules: - when: manual</code>): Mặc định là <code>allow_failure: true</code>. Pipeline sẽ hiển thị trạng thái <b>Passed (Xanh)</b> ngay cả khi người dùng không bấm nút manual.</li>
      <li>Khi khai báo <b>trực tiếp ở cấp Job</b> (<code>when: manual</code>): Mặc định là <code>allow_failure: false</code>. Pipeline sẽ bị giữ ở trạng thái <b>Blocked</b> cho đến khi có người bấm nút hoặc hủy bỏ.</li>
    </ul>
    <p><i>Quy tắc thực hành</i>: Luôn khai báo tường minh <code>allow_failure: true/false</code> bất cứ khi nào sử dụng <code>when: manual</code> để tránh hành vi mập mờ.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span>Khi một job sử dụng `needs: [job_a]` nhưng `job_a` bị loại bỏ bởi `rules`, pipeline sẽ xử lý ra sao? Cờ `optional: true` thay đổi hành vi này thế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Hành vi mặc định</b>: GitLab không thể dựng cây đồ thị DAG hợp lệ khi một dependency trỏ vào một job không tồn tại. Kết quả: <b>Pipeline bị từ chối khởi tạo (Pipeline creation failed)</b> với thông báo lỗi cú pháp rõ ràng (Lỗi ồn ào có chặn - Loud failure).</p>
    <p><b>Khi thêm `optional: true`</b>:</p>
    <pre><code class="language-yaml">needs:
  - job: job_a
    optional: true</code></pre>
    <p>GitLab cho phép pipeline khởi tạo. Nếu <code>job_a</code> không có mặt, job phía sau vẫn chạy bình thường nhưng <b>hoàn toàn không nhận được artifact từ `job_a`</b>. Cờ này chuyển lỗi từ "ồn ào có chặn" sang "im lặng không chặn" (Silent drop), do đó bắt buộc phải có câu lệnh assert kiểm tra tệp tin trong script.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q11</span>
    <span>Khi kỹ sư push code nhưng hoàn toàn không thấy bất kỳ pipeline nào xuất hiện trong tab CI/CD, quy trình chẩn đoán 2 giả thuyết chính là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Hai giả thuyết chính</b>:</p>
    <ol>
      <li><b>Giả thuyết A (Bị chặn ở Tầng 1)</b>: Khối <code>workflow:rules</code> không có rule nào khớp với sự kiện push hiện tại, hoặc rơi vào <code>when: never</code>.</li>
      <li><b>Giả thuyết B (0 Job $ightarrow$ 0 Pipeline)</b>: <code>workflow:rules</code> cho qua, nhưng toàn bộ các job trong file đều bị <code>rules</code> riêng lẻ từ chối. GitLab không tạo pipeline rỗng.</li>
    </ol>
    <p><b>Cách phân biệt bằng API</b>: Gọi endpoint <code>POST /api/v4/projects/:id/ci/lint</code>. Nếu mảng <code>.jobs</code> rỗng $ightarrow$ Giả thuyết B. Nếu mảng <code>.jobs</code> có phần tử nhưng pipeline thực tế không sinh ra $ightarrow$ Giả thuyết A.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q12</span>
    <span>Trình bày quy trình 4 bước chuẩn mực để trả lời câu hỏi: "Tại sao Job X không chạy trong Pipeline vừa kích hoạt?"</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Quy trình 4 bước chuẩn đoán chuyên sâu</b>:</p>
    <ol>
      <li><b>Bước 1: Kiểm tra sự tồn tại của Pipeline Instance</b>: Có pipeline nào được sinh ra cho commit SHA đó không? Nếu không có $ightarrow$ Rà soát ngay khối <code>workflow:rules</code>.</li>
      <li><b>Bước 2: Kiểm tra sự hiện diện trong Job List API</b>: Gọi <code>GET /pipelines/:id/jobs</code>. Nếu Job X không có tên trong danh sách $ightarrow$ Job đã bị <code>rules</code> loại bỏ (Omitted) tại $t_0$.</li>
      <li><b>Bước 3: Xác định trạng thái Runtime</b>: Nếu Job X có trong danh sách nhưng không chạy, kiểm tra xem nó đang ở trạng thái <code>manual</code> (chờ bấm) hay <code>skipped</code> (do job upstream bị failed).</li>
      <li><b>Bước 4: Đối soát Bảng chân trị</b>: Nếu bị Omitted, xác định giá trị <code>CI_PIPELINE_SOURCE</code> của pipeline và duyệt từng dòng trong mảng <code>rules</code> của Job X từ trên xuống dưới để tìm ra rule đầu tiên bị fail hoặc bị che khuất bởi nguyên tắc First-match-wins.</li>
    </ol>
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

```mermaid
mindmap
  root((Điều Khiển Luồng Rules & Workflow))
    Thời điểm Đánh giá
      Chốt tại t0 lúc tạo pipeline
      Bất biến khi Retry
      Biến dotenv không dùng được trong rules
      0 Job dẫn tới 0 Pipeline
    Hai Tầng Lọc
      workflow rules chặn cấp Pipeline
      rules chặn cấp Job
      Loại bỏ Duplicate Pipelines khi có MR
    Nguyên tắc Rules
      First-match-wins duyệt từ trên xuống
      Omitted biến mất hoàn toàn
      Cạm bẫy mốc so sánh của changes
      allow_failure khác biệt trong manual
```

> [!TIP]
> **Bài học tiếp theo**: Trong bài học kế tiếp [Bài 05: Quản Lý Dữ Liệu: Artifacts, Caching Nâng Cao & Tối Ưu Tốc Độ Truyền Tải Giữa Các Job](gitlab-05-05-artifact-va-cache.html), chúng ta sẽ phân tích toàn diện cơ chế lưu trữ và luân chuyển dữ liệu: phân biệt ranh giới giữa Artifacts và Distributed Cache, xây dựng chiến lược Cache Key thông minh và tối ưu hóa thời gian nạp phụ thuộc đa tầng.
{% endraw %}
