---
layout: post
title: "[Bài 05] Quản Trị Dữ Liệu Tạm Thời: Phân Biệt Artifacts vs Caching, S3 MinIO Backend & Tối Ưu Tốc Độ Build"
date: 2026-09-12 08:50:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-05
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 5
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.05] Hướng dẫn chuyên sâu Quản Trị Dữ Liệu Tạm Thời: Phân Biệt Artifacts vs Caching, S3 MinIO Backend & Tối Ưu Tốc Độ Build: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Quản Trị Dữ Liệu Tạm Thời: Phân Biệt Artifacts vs Caching, S3 MinIO Backend & Tối Ưu Tốc Độ Build."
  - "Thiết kế CI/CD Pipeline chuẩn Enterprise với kiến trúc DAG, tối ưu hóa thời gian build và caching hiệu quả."
  - "Bảo mật chuỗi cung ứng phần mềm với SAST/DAST, Container Scanning và OIDC Authentication."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 12 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 05] QUẢN TRỊ DỮ LIỆU TẠM THỜI: PHÂN BIỆT ARTIFACTS VS CACHING, S3 MINIO BACKEND & TỐI ƯU TỐC ĐỘ BUILD

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

### 1.1. Luận Đề Trung Tâm: Artifacts Là Hợp Đồng, Caching Là Tối Ưu

Trong thiết kế hệ thống CI/CD, sai lầm gây tốn kém thời gian gỡ lỗi nhất là sự nhầm lẫn giữa hai cơ chế luân chuyển dữ liệu: **Job Artifacts** và **Distributed Caching**.

> **`artifacts` là HỢP ĐỒNG BẮT BUỘC: Dữ liệu được đẩy lên Server GitLab, có cam kết bảo toàn, kiểm chứng được qua API và tính vào dung lượng dự án. `cache` là KHOẢN ĐẦU TƯ TỐI ƯU: Dữ liệu lưu tại Runner/S3, KHÔNG có cam kết bảo toàn, và Runner không bao giờ báo lỗi khi trượt cache.**

```text
   Server GitLab ──┐  artifacts: Upload ở cuối Job A ──▶ Download ở đầu Job B
                   │  ĐƯỢC ĐẢM BẢO · Có Metadata DB · Kiểm chứng qua API HTTP 200/404
                   │
   Job A ──────────┼─────────────────────────────────────────────────────────────► Job B
                   │
   Runner Disk / ──┘  cache: Nén ở cuối Job A ──▶ Giải nén ở đầu Job B (Cùng key)
   S3 MinIO           KHÔNG ĐẢM BẢO · Không có API đọc · Runner im lặng khi Miss
```

1. **Chủ thể lưu trữ quyết định mức độ đảm bảo**:
   - `artifacts` được Runner nén và gửi qua HTTP REST API lên Coordinator (GitLab Server/Object Storage) ở Pha 8. GitLab tạo bản ghi trong bảng `ci_job_artifacts` của PostgreSQL, gắn thời hạn `expire_in` và cấp endpoint `GET /projects/:id/jobs/:id/artifacts`.
   - `cache` được lưu trực tiếp trên đĩa cục bộ của Runner hoặc S3 bucket thông qua Runner Cache Driver. Server GitLab hoàn toàn không quản lý nội dung cache.
2. **Hành vi khi thiếu dữ liệu**:
   - Nếu Job B cần artifact từ Job A mà Job A fail &rarr; Job B bị block hoặc fail ở Pha 5.
   - Nếu Job B trượt cache &rarr; Runner in 1 dòng `No URL provided, cache will not be downloaded` và tiếp tục chạy `script` bình thường với **0 dòng error**.

```mermaid
graph TD
    subgraph ARTIFACTS_PIPELINE["Cơ Chế Artifacts (Contractual Delivery)"]
        JA["Job A (Compiler)"] -->|Upload qua HTTP| GLS["GitLab Server / S3 Artifacts Storage<br/>(Metadata DB + Audit Trail)"]
        GLS -->|Download tự động| JB["Job B (Tester / Deployer)"]
    end

    subgraph CACHE_PIPELINE["Cơ Chế Distributed Cache (Best-Effort Optimization)"]
        JC["Job C (Build)"] -->|Push tar.gz| MINIO["MinIO / AWS S3 Cache Bucket<br/>(Key-Value Store)"]
        MINIO -.->|Pull nếu Hit| JD["Job D (Test)"]
        MINIO -.->|Miss: Bỏ qua im lặng| JD
    end
```

### 1.2. Vòng Đời Phục Hồi Dữ Liệu: 4 Bước Khởi Động Job

Khi một Runner tiếp nhận job từ hàng đợi, thứ tự thực thi chuẩn xác tại workspace diễn ra như sau:

```text
  ┌────────────────────────────────────────────────────────────────────────┐
  │                   RUNNER WORKSPACE RESTORATION ORDER                   │
  ├────────────────────────────────────────────────────────────────────────┤
  │                                                                        │
  │  [ Bước 1: Pha clone ]                                                 │
  │  Git clone / fetch commit SHA mục tiêu vào $CI_PROJECT_DIR             │
  │                         │                                              │
  │                         ▼                                              │
  │  [ Bước 2: Pha restore_cache ]                                         │
  │  Tìm kiếm cache theo key/fallback_keys và giải nén đè lên workspace   │
  │                         │                                              │
  │                         ▼                                              │
  │  [ Bước 3: Pha download_artifacts ]                                    │
  │  Tải artifacts từ các upstream jobs và GIẢI NÉN ĐÈ LÊN CACHE           │
  │                         │                                              │
  │                         ▼                                              │
  │  [ Bước 4: Pha step_script ]                                           │
  │  Bắt đầu thực thi before_script và script trong Shell Session          │
  │                                                                        │
  └────────────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **Quy tắc ghi đè**: Do `download_artifacts` (Bước 3) chạy sau `restore_cache` (Bước 2), nếu một đường dẫn thư mục (ví dụ `dist/`) được khai báo trùng trong cả 2 khối `cache:paths` và `artifacts:paths`, **dữ liệu từ Artifacts sẽ luôn ghi đè lên dữ liệu từ Cache**.

### 1.3. Thời Điểm Tính Toán `cache:key` vs `rules`

- `rules` được Parser tính toán tại $t_0$ (thời điểm nhận webhook tạo pipeline).
- `cache:key` (đặc biệt là `cache:key:files`) được tính toán **trên chính Runner sau Bước 1 (clone)**. Runner cần có lockfile vật lý trên đĩa để băm hàm SHA/MD5 nội dung.
- Do đó, `cache:key` có thể sử dụng các biến môi trường runtime hoặc tính toán theo hash lockfile (`package-lock.json`, `go.sum`, `pom.xml`), trong khi `rules` thì không thể.

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

### 2.1. Ma Trận So Sánh Kỹ Thuật: Artifacts vs Caching

| Tiêu chí Kỹ thuật | Job Artifacts (`artifacts`) | Distributed Caching (`cache`) |
|---|---|---|
| **Mục đích thiết kế** | Chuyển giao kết quả build/test giữa các stage | Tăng tốc độ cài đặt dependencies giữa các pipeline |
| **Vị trí lưu trữ** | GitLab Coordinator Server / S3 Storage | Runner Local Disk / S3 MinIO Cache Bucket |
| **Bản ghi Cơ sở dữ liệu** | Có (`ci_job_artifacts` trong PostgreSQL) | **Không** (Lưu trữ Key-Value phi cấu trúc) |
| **Kiểm chứng qua API** | **Có** (`GET /jobs/:id/artifacts` trả HTTP 200/404) | **Không có API truy vấn trạng thái** |
| **Chính sách dọn dẹp** | Tự động theo `expire_in` (Default: 30 ngày) | Tự động theo S3 Lifecycle Policy / Runner LRU |
| **Hành vi khi vắng mặt** | Báo lỗi hoặc khiến job sau thất bại | **Im lặng tuyệt đối (0 dòng error, job vẫn chạy)** |
| **Mức độ phụ thuộc mạng** | Truyền qua GitLab HTTP API | Truyền qua S3 Protocol / Direct Disk I/O |
| **Trường hợp áp dụng chuẩn** | `dist/`, `.jar`, báo cáo `junit.xml`, SBOM, binary | `node_modules/`, `~/.m2`, `.gradle/`, `GOMODCACHE` |

### 2.2. Ma Trận Thu Hẹp Tải Artifacts Giữa Các Job

| Cú pháp khai báo | Nguồn tải Artifacts | Ảnh hưởng Thứ tự DAG | Byte truyền tải | Thời gian tải ước tính |
|---|---|---|---|---|
| *Mặc định (Không khai báo)* | **Toàn bộ job ở mọi stage trước đó** | Giữ nguyên Stage Barrier | $\sum \text{Tất cả Artifacts}$ | Rất chậm (Tải dư thừa) |
| `dependencies: [job_a]` | **Chỉ tải duy nhất từ `job_a`** | Giữ nguyên Stage Barrier | Chỉ dung lượng `job_a` | Nhanh |
| `dependencies: []` | **Tắt hoàn toàn việc tải (0 job)** | Giữ nguyên Stage Barrier | **Chính xác 0 byte** | **0 giây** |
| `needs: [job_a]` | **Chỉ tải từ `job_a`** | **Phá vỡ Stage, chạy ngay khi `job_a` xong** | Chỉ dung lượng `job_a` | Tối ưu tuyệt đối |
| `needs: [{job: job_a, artifacts: false}]` | **Không tải artifact từ `job_a`** | **Chạy ngay khi `job_a` xong** | **Chính xác 0 byte** | **0 giây** |

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (Architecture Breakdown)

### 3.1. Sơ Đồ Kiến Trúc Distributed Cache Với MinIO S3 Backend

Trong môi trường Autoscaling Runners (Kubernetes/Docker Machine), mỗi job chạy trên một node/pod tạm thời (ephemeral). Nếu không có Distributed Cache, tỷ lệ trúng cache rơi về $1/N$ ($N$ là số node). Kiến trúc chuẩn Enterprise sử dụng MinIO S3 làm bộ nhớ đệm dùng chung:

```text
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │                       ENTERPRISE DISTRIBUTED CACHING ARCHITECTURE                      │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                        │
  │   [ Runner Pod 1 ] ──(Pull Cache)──┐                                                   │
  │                                    ▼                                                   │
  │   [ Runner Pod 2 ] ──(Push Cache)──▶ [ MinIO Distributed Cluster ] ◀──(S3 Lifecycle)   │
  │                                    ▲   (Bucket: gitlab-runner-cache)  (Auto-expire 7d) │
  │   [ Runner Pod 3 ] ──(Pull Cache)──┘                                                   │
  │                                                                                        │
  └────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2. Cấu Hình Production Chuẩn Mực `.gitlab-ci.yml`

```yaml
# ==============================================================================
# PIPELINE DATA MANAGEMENT: ENTERPRISE ARTIFACTS & DISTRIBUTED CACHE
# ==============================================================================

stages:
  - prepare
  - build
  - test
  - package
  - release

default:
  image: node:20-alpine

# ------------------------------------------------------------------------------
# 1. Global Cache Strategy: Khóa theo Lockfile với Fallback đa tầng
# ------------------------------------------------------------------------------
.node_cache_template:
  cache:
    key:
      files:
        - package-lock.json
      prefix: "node-20-${CI_RUNNER_EXECUTOR}"
    paths:
      - .npm/
    policy: pull
    fallback_keys:
      - "node-20-${CI_RUNNER_EXECUTOR}-${CI_DEFAULT_BRANCH}"
      - "node-20-${CI_RUNNER_EXECUTOR}-default"

# ------------------------------------------------------------------------------
# 2. Stage Prepare: Cache Warming Job (Chỉ chạy khi Lockfile thay đổi)
# ------------------------------------------------------------------------------
warm-cache-dependencies:
  extends: .node_cache_template
  stage: prepare
  rules:
    - changes:
        paths:
          - package-lock.json
  cache:
    policy: push # Job duy nhất đẩy cache mới lên S3
  script:
    - echo "Lockfile changed. Warming up distributed S3 cache..."
    - npm ci --cache .npm --prefer-offline
    - test -d .npm || { echo "Cache directory missing!"; exit 1; }

# ------------------------------------------------------------------------------
# 3. Stage Build: Sinh Intermediate Artifacts
# ------------------------------------------------------------------------------
compile-frontend:
  extends: .node_cache_template
  stage: build
  cache:
    policy: pull-push
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run build
    # ASSERTION BẮT BUỘC: Ngăn chặn Silent Empty Artifacts
    - test -s dist/index.html || { echo "CRITICAL: dist/index.html missing!"; exit 1; }
    - test -s dist/assets/app.js || { echo "CRITICAL: bundle JS empty!"; exit 1; }
  artifacts:
    name: "frontend-build-${CI_COMMIT_SHORT_SHA}"
    paths:
      - dist/
    expire_in: 2 hours # Hiện vật trung gian dọn dẹp sau 2h

# ------------------------------------------------------------------------------
# 4. Stage Test: Đọc Cache và Tải Báo Cáo Khi Thất Bại (when: always)
# ------------------------------------------------------------------------------
unit-tests:
  extends: .node_cache_template
  stage: test
  dependencies: [] # Tắt download artifacts để tiết kiệm băng thông
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run test:unit -- --reporters=default --reporters=jest-junit
  artifacts:
    when: always # Luôn tải báo cáo kể cả khi test fail
    paths:
      - junit.xml
      - coverage/
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    expire_in: 7 days

# ------------------------------------------------------------------------------
# 5. Stage Package & Release: Release Artifacts (Lưu trữ dài hạn)
# ------------------------------------------------------------------------------
package-release-bundle:
  stage: release
  image: alpine:3.20
  dependencies:
    - compile-frontend # Chỉ tải duy nhất artifacts từ compile-frontend
  script:
    - mkdir -p release-payload
    - cp -r dist/ release-payload/
    - sha256sum release-payload/dist/assets/app.js > release-payload/SHA256SUMS
    - test -s release-payload/SHA256SUMS || exit 1
  artifacts:
    name: "release-${CI_COMMIT_TAG}"
    paths:
      - release-payload/
    expire_in: 90 days # Hiện vật release lưu trữ dài hạn
  rules:
    - if: $CI_COMMIT_TAG
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

### 4.1. Incident 1: Sự Cố Triển Khai Bundle Cũ Lên Production Do Xung Đột Cache và Artifacts

```text
                      SỰ CỐ STALE BUNDLE DEPLOYMENT
  ┌────────────────────────────────────────────────────────────────────────┐
  │ Job Build: Khai báo `cache: paths: [dist/]` VÀ `artifacts: paths: [dist/]` │
  │ Lần chạy 1: Build thành công dist/ (Version 1.0) -> Đẩy vào S3 Cache   │
  │ Lần chạy 2: Sửa file src/app.js, nhưng do lỗi webpack, build sinh rỗng │
  │ Job Deploy: Download Artifacts rỗng, nhưng giải nén đè Cache cũ (v1.0) │
  ├────────────────────────────────────────────────────────────────────────┤
  │ Kết quả: Job Deploy deploy nhầm Bundle cũ Version 1.0 lên Production!  │
  │ Pipeline: Báo SUCCESS (Xanh mượt) -> Khách hàng dùng code cũ 2 tuần!   │
  └────────────────────────────────────────────────────────────────────────┘
```

- **Hiện tượng**: Đội ngũ Frontend sửa đổi giao diện thanh toán và commit mã nguồn, pipeline CI/CD báo xanh toàn bộ, nhưng khách hàng vẫn thấy giao diện cũ. Kiểm tra container trên Production cho thấy bundle JS chứa mã nguồn của 2 tuần trước.
- **Phân tích 5-Whys**:
  1. *Tại sao container lại chứa mã nguồn 2 tuần trước?* Vì thư mục `dist/` nạp vào Dockerfile chứa tệp JS cũ.
  2. *Tại sao tệp JS cũ lại xuất hiện khi commit mới đã push?* Vì job `build` khai báo cả `cache: paths: [dist/]` và `artifacts: paths: [dist/]`. Khi build mới bị lỗi silent rỗng, bước restore cache đã lôi lại `dist/` của lần build thành công 2 tuần trước.
  3. *Tại sao job build không bị fail khi sinh rỗng?* Webpack exit code 0 do không có fatal syntax error, và script không có lệnh `test -s dist/app.js` để kiểm tra dung lượng output.
  4. *Tại sao lại cấu hình `dist/` vào trong khối `cache`?* Vì kỹ sư tưởng nhầm việc cache `dist/` sẽ giúp job `build` chạy nhanh hơn nếu mã nguồn không đổi.
  5. *Nguyên nhân gốc rễ (Root Cause)*: Vi phạm nguyên lý phân loại dữ liệu: Đưa sản phẩm đầu ra (Build Output - thuộc về Artifacts) vào kho đệm tạm thời (Cache), kết hợp với việc thiếu assertion kiểm tra tệp tin trước khi kết thúc job.
- **Giải pháp triệt để**:
  1. Xóa bỏ hoàn toàn `dist/` khỏi mảng `cache:paths`. Chỉ cache thư mục phụ thuộc (`.npm/`, `node_modules/`).
  2. Bổ sung assertion bắt buộc: `test -s dist/app.js || { echo "ASSERTION FAILED"; exit 1; }`.

### 4.2. Incident 2: Đĩa Cứng Runner Bị Đầy (Disk Exhaustion) Do `cache:key: $CI_COMMIT_SHA`

- **Hiện tượng**: Cụm GitLab Runner đồng loạt báo lỗi `No space left on device` sau 3 ngày hoạt động, hàng loạt job bị pending và failed.
- **Phân tích 5-Whys**:
  1. *Tại sao đĩa cứng Runner bị đầy 100%?* Thư mục `/cache` trên host chứa hơn 4,000 file nén `.tar.gz` dung lượng 350MB mỗi file.
  2. *Tại sao lại có 4,000 file cache không tái sử dụng?* Vì cấu hình `.gitlab-ci.yml` sử dụng `cache: key: "$CI_COMMIT_SHA"`.
  3. *Tại sao key theo commit SHA lại sinh nhiều file?* Mỗi lần push commit tạo ra một SHA mới, Runner nén 350MB và đẩy vào một key mới, không bao giờ hit lại key cũ.
  4. *Tại sao Runner không tự xóa cache cũ?* Docker executor trên local disk không có cơ chế tự động eviction cache theo thời gian thực nếu không có cronjob dọn dẹp bên ngoài.
  5. *Nguyên nhân gốc rễ (Root Cause)*: Sử dụng "Phản-cache" (Anti-pattern `key: $CI_COMMIT_SHA`), biến cơ chế cache thành một cỗ máy đốt đĩa cứng với tỷ lệ trúng 0%.
- **Giải pháp triệt để**: Chuyển đổi `cache:key` sang dạng `files: [package-lock.json]` và chuyển backend sang MinIO S3 có cấu hình Lifecycle Policy tự động xóa sau 7 ngày.

---

## 5. Hands-on Lab: Quản Lý Artifacts, Distributed Caching & Tối Ưu Tốc Độ Truyền Tải (8 Bước Chuẩn)

### 5.1. Bước 1: Khởi Tạo Môi Trường & Đo Lường Hành Vi Mặc Định Của Artifacts

Thiết lập project thử nghiệm trên GitLab và đo lường số lượng artifacts tải về mặc định:

```bash
export GITLAB="http://gitlab.lab:8929"
export GITLAB_TOKEN="glpat-StandardLabTokenAdmin2026"
export HAU_TO="devops-storage"

# Tạo Project Lab 05
PID5=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN"   --header "Content-Type: application/json"   --data "{"name":"lab05-artifacts-cache-${HAU_TO}","visibility":"internal"}"   "$GITLAB/api/v4/projects" | jq -r .id)

echo "Lab Project ID: $PID5"

mkdir -p ~/lab05 && cd ~/lab05
git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/root/lab05-artifacts-cache-${HAU_TO}.git"
git config user.email "lab@internal.corp"
git config user.name "Lab Storage Engineer"

cat > .gitlab-ci.yml <<'EOF'
stages:
  - stage_a
  - stage_b
  - stage_c

build_module_1:
  stage: stage_a
  image: alpine:3.20
  script:
    - mkdir -p mod1 && echo "MOD1_PAYLOAD" > mod1/file1.bin
  artifacts:
    paths: [mod1/]

build_module_2:
  stage: stage_b
  image: alpine:3.20
  script:
    - mkdir -p mod2 && echo "MOD2_PAYLOAD" > mod2/file2.bin
  artifacts:
    paths: [mod2/]

verify_default_download:
  stage: stage_c
  image: alpine:3.20
  script:
    - echo "=== Checking files in workspace ==="
    - ls -la mod1/file1.bin
    - ls -la mod2/file2.bin
EOF

git add .gitlab-ci.yml && git commit -m "lab: test default artifacts propagation" && git push -u origin main
sleep 25

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines?per_page=1" | jq -r '.[0].id')
JOB_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines/$PIPE_ID/jobs" | jq -r '.[] | select(.name=="verify_default_download") | .id')

curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/jobs/$JOB_ID/trace"   | grep -aE '(Downloading artifacts|MOD[12]_PAYLOAD)'
```

> **CHECKPOINT 1**: Job `verify_default_download` tự động tải artifacts của cả 2 stage trước đó (`mod1/` và `mod2/`) dù không hề khai báo bất kỳ từ khóa dependencies nào.

### 5.2. Bước 2: Tái Hiện Sự Cố Artifact Rỗng Nhưng Job Vẫn Xanh & Khắc Phục

Tạo 2 job kiểm thử để đo lường mã trạng thái HTTP API:

```yaml
# Thêm vào .gitlab-ci.yml
stages:
  - test_silent_fail

build_silent_empty:
  stage: test_silent_fail
  image: alpine:3.20
  script:
    - mkdir -p actual_dist && echo "data" > actual_dist/app.js
    - echo "Build completed with exit code 0"
  artifacts:
    paths:
      - wrong_dist/ # ĐƯỜNG DẪN SAI -> Artifact rỗng

build_with_assertion:
  stage: test_silent_fail
  image: alpine:3.20
  script:
    - mkdir -p actual_dist && echo "data" > actual_dist/app.js
    - test -d wrong_dist || { echo "ASSERTION ERROR: wrong_dist missing!"; exit 1; }
  artifacts:
    paths:
      - wrong_dist/
```

Đẩy pipeline và kiểm tra kết quả qua API:

```bash
cd ~/lab05
git add .gitlab-ci.yml && git commit -m "lab: test silent empty artifacts" && git push origin main
sleep 20

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines?per_page=1" | jq -r '.[0].id')
JOB_SILENT=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines/$PIPE_ID/jobs" | jq -r '.[] | select(.name=="build_silent_empty") | .id')

STATUS_SILENT=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/jobs/$JOB_SILENT" | jq -r .status)
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/jobs/$JOB_SILENT/artifacts")

echo "Job status: $STATUS_SILENT, Artifact API Download Code: HTTP $HTTP_CODE"
```

> **CHECKPOINT 2**: `build_silent_empty` có `status: success` (Xanh) nhưng API download trả về `HTTP 404`. Ngược lại, `build_with_assertion` báo đỏ ngay lập tức (`exit code 1`).

### 5.3. Bước 3: Đo Lường & So Sánh `dependencies: []` vs `needs`

Kiểm chứng tốc độ và tính cô lập khi thu hẹp artifacts:

```yaml
# ~/lab05/.gitlab-ci.yml
stages:
  - generate
  - consume

producer_heavy:
  stage: generate
  image: alpine:3.20
  script:
    - mkdir -p big_payload
    - dd if=/dev/urandom of=big_payload/data.bin bs=1M count=10 2>/dev/null
  artifacts:
    paths: [big_payload/]

consumer_isolated:
  stage: consume
  image: alpine:3.20
  dependencies: [] # Tắt download
  script:
    - ls -la big_payload/data.bin 2>/dev/null || echo "WORKSPACE IS CLEAN (0 Byte Downloaded)"
```

```bash
cd ~/lab05
git add .gitlab-ci.yml && git commit -m "lab: verify dependencies isolation" && git push origin main
sleep 25

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines?per_page=1" | jq -r '.[0].id')
JOB_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines/$PIPE_ID/jobs" | jq -r '.[] | select(.name=="consumer_isolated") | .id')

curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/jobs/$JOB_ID/trace"   | grep -a "WORKSPACE IS CLEAN"
```

> **CHECKPOINT 3**: Job `consumer_isolated` hoàn thành trong 2 giây mà không tốn bất kỳ thời gian tải 10MB payload nào từ stage trước.

### 5.4. Bước 4: Thực Nghiệm `artifacts:when: always` Khi Job Bị Thất Bại

Chứng minh việc giữ lại file báo cáo kiểm thử khi test suite bị fail:

```yaml
# ~/lab05/.gitlab-ci.yml
stages:
  - test_reports

test_fail_with_reports:
  stage: test_reports
  image: alpine:3.20
  script:
    - mkdir -p reports
    - echo "<testsuite failures='1'><testcase name='auth_test'><failure>Invalid Token</failure></testcase></testsuite>" > reports/junit.xml
    - echo "Simulating test failure..."
    - exit 1
  artifacts:
    when: always # BẮT BUỘC
    paths:
      - reports/
    reports:
      junit: reports/junit.xml
```

```bash
cd ~/lab05
git add .gitlab-ci.yml && git commit -m "lab: test when always reports on failure" && git push origin main
sleep 20

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines?per_page=1" | jq -r '.[0].id')
JOB_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines/$PIPE_ID/jobs" | jq -r '.[] | select(.name=="test_fail_with_reports") | .id')

HTTP_REPORT=$(curl -s -o /dev/null -w '%{http_code}' --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/jobs/$JOB_ID/artifacts")
echo "Job Failed but Artifact Download HTTP Code: $HTTP_REPORT"
```

> **CHECKPOINT 4**: Dù job bị failed (`status: failed`), mã phản hồi tải artifact vẫn đạt `HTTP 200` thành công.

### 5.5. Bước 5: Đo Đạc Sổ Thu Chi Caching (Break-Even Measurement)

Tạo kịch bản đo đạc chính xác thời gian nén, giải nén và tải thư mục cache:

```yaml
# ~/lab05/.gitlab-ci.yml
stages:
  - benchmark_cache

cache_benchmark_job:
  stage: benchmark_cache
  image: alpine:3.20
  cache:
    key: "benchmark-v1"
    paths:
      - mock_cache/
    policy: pull-push
  script:
    - mkdir -p mock_cache
    - if [ ! -f mock_cache/payload.dat ]; then
        echo "Cache Miss: Generating 20MB mock dependencies...";
        dd if=/dev/urandom of=mock_cache/payload.dat bs=1M count=20 2>/dev/null;
      else
        echo "Cache Hit: Dependencies restored successfully!";
      fi
```

Chạy pipeline 2 lần liên tiếp để đo Hit/Miss:

```bash
cd ~/lab05
git add .gitlab-ci.yml && git commit -m "lab: benchmark cache break even" && git push origin main
sleep 25
# Lần 1: Cache Miss & Upload
PIPE_1=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines?per_page=1" | jq -r '.[0].id')
JOB_1=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines/$PIPE_1/jobs" | jq -r '.[0].id')

# Kích hoạt lần 2: Cache Hit
curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipeline?ref=main" >/dev/null
sleep 25
PIPE_2=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines?per_page=1" | jq -r '.[0].id')
JOB_2=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines/$PIPE_2/jobs" | jq -r '.[0].id')

echo "=== PIPELINE 1 (MISS & PUSH) TRACE ==="
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/jobs/$JOB_1/trace" | grep -aE '(Restoring cache|Creating cache)'

echo "=== PIPELINE 2 (HIT & RESTORE) TRACE ==="
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/jobs/$JOB_2/trace" | grep -aE '(Restoring cache|Successfully extracted cache)'
```

> **CHECKPOINT 5**: Pipeline 2 hiển thị `Successfully extracted cache in X.XX seconds`, chứng minh chu trình Hit cache thành công.

### 5.6. Bước 6: Tối Ưu Hóa Bằng `cache:policy: pull` Cho Các Job Song Song

Chứng minh việc tiết kiệm thời gian bằng cách loại bỏ pha `Creating cache` ở các job test song song:

```yaml
# ~/lab05/.gitlab-ci.yml
stages:
  - test_parallel

.test_pull_template:
  stage: test_parallel
  image: alpine:3.20
  cache:
    key: "benchmark-v1"
    paths: [mock_cache/]
    policy: pull # CHỈ ĐỌC

test_worker_1:
  extends: .test_pull_template
  script: [ls -la mock_cache/payload.dat]

test_worker_2:
  extends: .test_pull_template
  script: [ls -la mock_cache/payload.dat]
```

```bash
cd ~/lab05
git add .gitlab-ci.yml && git commit -m "lab: test pull policy" && git push origin main
sleep 20

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines?per_page=1" | jq -r '.[0].id')
JOB_W1=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines/$PIPE_ID/jobs" | jq -r '.[] | select(.name=="test_worker_1") | .id')

echo "Worker 1 Trace Check (Should NOT have Creating cache):"
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/jobs/$JOB_W1/trace" | grep -a "Creating cache" || echo "VERIFIED: Creating cache skipped successfully!"
```

> **CHECKPOINT 6**: Log của worker không xuất hiện pha `Creating cache`, tiết kiệm 100% thời gian nén và upload lại trên S3 backend.

### 5.7. Bước 7: Thực Nghiệm Thứ Tự Phục Hồi Dữ Liệu & Xung Đột Trùng Đường Dẫn

Chứng minh Artifacts ghi đè Cache khi trùng đường dẫn:

```yaml
# ~/lab05/.gitlab-ci.yml
stages:
  - populate
  - verify_override

producer_both:
  stage: populate
  image: alpine:3.20
  cache:
    key: "conflict-key"
    paths: [shared_folder/]
  artifacts:
    paths: [shared_folder/]
  script:
    - mkdir -p shared_folder
    - echo "VERSION_FROM_CACHE" > shared_folder/target.txt
    - cp shared_folder/target.txt /tmp/cached_copy.txt
    - echo "VERSION_FROM_ARTIFACTS" > shared_folder/target.txt

consumer_both:
  stage: verify_override
  image: alpine:3.20
  cache:
    key: "conflict-key"
    paths: [shared_folder/]
    policy: pull
  script:
    - echo "Reading content of shared_folder/target.txt:"
    - cat shared_folder/target.txt
```

```bash
cd ~/lab05
git add .gitlab-ci.yml && git commit -m "lab: verify artifact overrides cache" && git push origin main
sleep 25

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines?per_page=1" | jq -r '.[0].id')
JOB_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/pipelines/$PIPE_ID/jobs" | jq -r '.[] | select(.name=="consumer_both") | .id')

curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5/jobs/$JOB_ID/trace"   | grep -a "VERSION_FROM_"
```

> **CHECKPOINT 7**: File in ra chính xác `VERSION_FROM_ARTIFACTS`. Khẳng định: Pha tải Artifacts diễn ra sau và ghi đè hoàn toàn nội dung Cache.

### 5.8. Bước 8: Kiểm Tra Dung Lượng Project Artifacts & Dọn Dẹp Tài Nguyên

Truy vấn chỉ số thống kê dung lượng lưu trữ của project và dọn dẹp môi trường lab:

```bash
# Truy vấn dung lượng lưu trữ Job Artifacts của dự án
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5?statistics=true"   | jq '{name: .name, artifacts_size_bytes: .statistics.job_artifacts_size, storage_size_bytes: .statistics.storage_size}'

# Dọn dẹp Project Lab 05
curl -sf --request DELETE --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID5"
echo "Lab 05 storage resources cleaned up successfully."
```

> **CHECKPOINT 8**: Endpoint trả về `statistics.job_artifacts_size` chi tiết và project lab được xóa sạch khỏi cụm.

---

## 6. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span>Bản chất khác biệt cốt lõi giữa `artifacts` và `cache` trong GitLab CI là gì? Khi nào dùng cái nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Bản chất cốt lõi nằm ở "Chủ thể lưu trữ" và "Mức độ cam kết"</b>:</p>
    <ul>
      <li><code>artifacts</code>: Do <b>GitLab Server Coordinator</b> lưu trữ. Là <b>Hợp đồng bắt buộc</b> (Contract). Dữ liệu có bản ghi cơ sở dữ liệu, kiểm chứng được qua API HTTP 200/404, có vòng đời <code>expire_in</code> rõ ràng và được bảo đảm chuyển giao giữa các stage.</li>
      <li><code>cache</code>: Do <b>Runner / S3 Storage</b> lưu trữ. Là <b>Khoản đầu tư tối ưu hóa</b> (Best-effort). Hoàn toàn không có cam kết bảo toàn dữ liệu, không có API kiểm tra, và Runner sẽ im lặng bỏ qua nếu trượt cache (Cache miss).</li>
    </ul>
    <p><b>Quy tắc 1 câu hỏi để lựa chọn</b>: <i>"Job phía sau sẽ <b>SAI</b> (Fail) nếu thiếu nó, hay chỉ chạy <b>CHẬM</b> hơn?"</i></p>
    <ul>
      <li>Nếu thiếu mà SAI &rarr; Dùng <code>artifacts</code> (Ví dụ: <code>dist/</code>, binary, test report).</li>
      <li>Nếu thiếu mà chỉ CHẬM (có thể tự tải/cài lại từ lockfile) &rarr; Dùng <code>cache</code> (Ví dụ: <code>node_modules/</code>, <code>~/.m2</code>).</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span>Thời điểm tính toán `cache:key` diễn ra lúc nào? Tại sao nó không thể được tính toán tại $t_0$ như `rules`?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Thời điểm tính toán</b>: <code>cache:key</code> được tính toán <b>trên Runner sau khi hoàn thành pha clone mã nguồn (Pha get_sources)</b>, hoàn toàn không phải tại $t_0$ lúc khởi tạo pipeline.</p>
    <p><b>Lý do kỹ thuật</b>: Đối với dạng khóa chuẩn mực nhất là <code>cache:key:files</code> (ví dụ: <code>files: [package-lock.json]</code>), Runner bắt buộc phải băm (hash) <b>nội dung nhị phân thực tế của tệp tin</b> trên đĩa. Do đó, Runner bắt buộc phải checkout mã nguồn về workspace trước rồi mới có dữ liệu để tính toán ra mã băm của Cache Key.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span>Tại sao một job khai báo sai đường dẫn `artifacts:paths` vẫn kết thúc với trạng thái Xanh (Passed)? Làm thế nào để phát hiện và ngăn chặn?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Cơ chế gây lỗi</b>: Bước thu thập và nén artifacts (Pha 8) diễn ra <b>sau khi khối lệnh script đã thực thi xong</b>. Mã thoát (Exit Code) của job được chốt bởi lệnh cuối cùng trong <code>script</code>. Nếu <code>artifacts:paths</code> không tìm thấy tệp khớp mẫu, Runner chỉ in một cảnh báo <code>WARNING: No matching files</code> vào trace log và tạo một file zip rỗng rồi thoát với mã 0.</p>
    <p><b>Cách phát hiện và phòng ngừa</b>:</p>
    <ul>
      <li><b>Phát hiện qua API</b>: Job có <code>status == "success"</code> nhưng gọi <code>GET /projects/:id/jobs/:id/artifacts</code> trả về mã <code>HTTP 404</code>.</li>
      <li><b>Phòng ngừa bằng Assertion</b>: Đặt lệnh kiểm tra bắt buộc trước khi kết thúc <code>script</code>:
        <pre><code class="language-bash">test -s dist/app.js || { echo "ERROR: Output dist/app.js is empty or missing"; exit 1; }</code></pre>
      </li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span>Mặc định một job sẽ tải artifacts từ những job nào? Tác động tiêu cực của hành vi mặc định này đến hiệu năng pipeline?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Hành vi mặc định</b>: Mặc định một job sẽ <b>tự động tải toàn bộ artifacts từ TẤT CẢ các job thuộc TẤT CẢ các stage phía trước nó</b> (không chỉ stage liền trước).</p>
    <p><b>Tác động tiêu cực</b>:</p>
    <ul>
      <li>Gây lãng phí băng thông mạng và thời gian I/O đĩa cục bộ. Ví dụ: Một job <code>lint</code> nhẹ nhàng ở Stage 3 vẫn phải chờ tải 500MB artifacts từ các job build Docker/JAR ở Stage 1 và Stage 2 dù nó hoàn toàn không sử dụng.</li>
      <li>Làm tăng thời gian tổng thể của pipeline thêm hàng chục giây cho mỗi job downstream.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span>Phân biệt sự khác nhau giữa 3 chỉ thị: `dependencies: []`, `dependencies: [build_app]` và `needs: [{job: build_app, artifacts: false}]`?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Bảng phân tích kỹ thuật</b>:</p>
    <ul>
      <li><code>dependencies: []</code>: <b>Tắt hoàn toàn việc tải artifacts (0 Byte)</b>, nhưng <b>vẫn giữ nguyên thứ tự đồng bộ của Stage</b> (Phải chờ toàn bộ job ở stage trước hoàn thành).</li>
      <li><code>dependencies: [build_app]</code>: <b>Chỉ tải duy nhất artifacts từ `build_app`</b>, nhưng <b>vẫn phải chờ toàn bộ stage trước kết thúc</b>.</li>
      <li><code>needs: [{job: build_app, artifacts: false}]</code>: <b>Phá vỡ rào cản Stage (Chạy ngay lập tức khi `build_app` xong)</b> và <b>hoàn toàn không tải artifacts (0 Byte)</b>.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span>Khi một job test bị thất bại (Exit code != 0), tại sao mặc định kỹ sư không xem được file log hoặc JUnit XML? Cách khắc phục?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Nguyên nhân</b>: Thuộc tính <code>artifacts:when</code> có giá trị mặc định là <code>on_success</code>. Khi job bị fail, Runner hủy bỏ toàn bộ bước upload artifacts, dẫn đến việc các báo cáo kiểm thử và log chi tiết bị xóa sạch cùng workspace của Runner.</p>
    <p><b>Cách khắc phục chuẩn</b>: Luôn khai báo tường minh <code>when: always</code> cho các khối artifacts chứa báo cáo test, security scan và debug logs:
    <pre><code class="language-yaml">artifacts:
  when: always
  paths:
    - reports/junit.xml
  reports:
    junit: reports/junit.xml
  expire_in: 7 days</code></pre>
    </p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span>Phân tích Sổ thu chi của Cache (Break-even Analysis). Tại sao một thư mục cache nặng 380MB vẫn có thể mang lại hiệu quả tối ưu vượt trội?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Phương trình sổ thu chi</b>:</p>
    $$\text{Lợi nhuận mỗi lần chạy} = p \times (T_{\text{rebuild}} - T_{\text{restore}}) - T_{\text{archive}}$$
    <p>Với cache 380MB thực nghiệm: $T_{\text{rebuild}} = 95s$, $T_{\text{archive}} = 61s$, $T_{\text{restore}} = 44s$.</p>
    <ul>
      <li>Lợi nhuận mỗi lần Hit: $95s - 44s = \mathbf{+51s}$.</li>
      <li>Số lần Hit để hòa vốn: $\text{Break-even} = \frac{T_{\text{archive}}}{\text{Lợi nhuận Hit}} = \frac{61}{51} \approx \mathbf{2 \ lần}$.</li>
    </ul>
    <p><i>Kết luận</i>: Nếu khóa cache bám theo `package-lock.json` (tỷ lệ trúng 95%), chỉ sau 2 lần chạy pipeline, hệ thống đã hoàn vốn chi phí nén 61s và bắt đầu tiết kiệm 51s cho mỗi pipeline tiếp theo trong ngày.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span>Chính sách `cache:policy: pull` giải quyết vấn đề gì trong các job chạy song song (Parallel Jobs)? Tiết kiệm bao nhiêu thời gian?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Hai vấn đề được giải quyết</b>:</p>
    <ol>
      <li><b>Triệt tiêu lãng phí thời gian nén</b>: Mặc định (<code>pull-push</code>), mọi job đều nén và upload lại cache ở cuối job. Khi có 3 job test chạy song song, <code>policy: pull</code> loại bỏ hoàn toàn pha nén 61s ở cả 3 job &rarr; <b>Tiết kiệm $3 \times 61s = \mathbf{183s}$ thời gian máy</b>.</li>
      <li><b>Ngăn ngừa Race Condition ghi đè</b>: Khi 3 job song song cùng đẩy cache lên S3, job nào kết thúc sau cùng sẽ ghi đè lên các job trước. <code>policy: pull</code> đảm bảo chỉ có duy nhất job `build` có quyền ghi đè cache.</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span>Tại sao khi chạy pipeline trên cụm nhiều Runner không có S3 MinIO backend, tỷ lệ trúng cache bị trần ở mức $1/N$? Giải pháp kiến trúc là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Nguyên nhân</b>: Mặc định Runner lưu cache trên đĩa cứng cục bộ của chính máy đó. Khi hệ thống có $N$ Runner, một job bất kỳ chỉ có xác suất $1/N$ được điều phối đúng vào Runner đang giữ file cache trên đĩa. $N-1$ lần còn lại sẽ bị Cache Miss.</p>
    <p><b>Giải pháp kiến trúc</b>: Cấu hình <b>Distributed Cache</b> trong <code>config.toml</code> của toàn bộ cụm Runner, trỏ về một S3-compatible Object Storage chung (như MinIO, AWS S3, Google Cloud Storage):
    <pre><code class="language-toml">[runners.cache]
  Type = "s3"
  Shared = true
  [runners.cache.s3]
    ServerAddress = "minio.internal:9000"
    BucketName = "gitlab-runner-cache"</code></pre>
    </p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span>Trình bày thứ tự phục hồi dữ liệu 4 bước ở đầu job. Nếu một thư mục xuất hiện trong cả `cache:paths` và `artifacts:paths`, kết quả cuối cùng ra sao?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Thứ tự 4 bước khởi tạo workspace</b>:</p>
    <ol>
      <li><b>Pha 1 (clone)</b>: Checkout Git commit SHA.</li>
      <li><b>Pha 2 (restore_cache)</b>: Tải và giải nén Cache.</li>
      <li><b>Pha 3 (download_artifacts)</b>: Tải và giải nén Artifacts (Ghi đè lên bước 2).</li>
      <li><b>Pha 4 (step_script)</b>: Bắt đầu chạy script người dùng.</li>
    </ol>
    <p><b>Kết quả khi trùng đường dẫn</b>: <b>Artifacts sẽ luôn chiến thắng và ghi đè lên Cache</b>. Tuy nhiên, đây là cạm bẫy thiết kế tồi, có thể gây sự cố deploy code cũ nếu job build upstream sinh rỗng và bước 3 không có file để ghi đè.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q11</span>
    <span>Trình bày cây quyết định 3 câu hỏi để phân loại các thư mục: `dist/`, `node_modules/`, `~/.m2/repository`, `junit.xml`, và `sbom.cdx.json`?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Cây quyết định 3 câu hỏi theo thứ tự</b>:</p>
    <ol>
      <li><i>Câu 1: Job sau SAI nếu thiếu nó, hay chỉ CHẬM hơn?</i> &rarr; SAI: <code>artifacts</code>.</li>
      <li><i>Câu 2: Có thể tái tạo từ lockfile trong Git không?</i> &rarr; CÓ: <code>cache</code>.</li>
      <li><i>Câu 3: Có người/hệ thống ngoài pipeline cần đọc không?</i> &rarr; CÓ: <code>artifacts</code> (Ghi đè câu 2).</li>
    </ol>
    <p><b>Phân loại chi tiết</b>:</p>
    <ul>
      <li><code>node_modules/</code> & <code>~/.m2/repository</code>: Dừng ở Câu 2 $
ightarrow$ <b>Cache</b> (Tái tạo được từ lockfile).</li>
      <li><code>junit.xml</code> & <code>sbom.cdx.json</code>: Dừng ở Câu 3 $
ightarrow$ <b>Artifacts</b> (Reviewer và Security Auditor cần kiểm chứng qua API).</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q12</span>
    <span>Xây dựng quy trình 5 nhịp chuẩn đoán khi gặp sự cố: "Pipeline báo xanh toàn bộ nhưng Production lại chạy bản build cũ hoặc rỗng"?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Quy trình 5 nhịp chuẩn hóa</b>:</p>
    <ol>
      <li><b>Nhịp 1: Đo lường kích thước Artifacts qua API</b>: Gọi <code>GET /projects/:id/jobs/:id/artifacts</code>. Nếu trả về <code>HTTP 404</code> hoặc dung lượng chỉ vài trăm bytes $
ightarrow$ Hợp đồng Artifacts bị rỗng.</li>
      <li><b>Nhịp 2: Kiểm tra sự tồn tại của Upstream Job</b>: Kiểm tra xem job build có bị <code>rules</code> loại bỏ khỏi DAG tại $t_0$ hay không.</li>
      <li><b>Nhịp 3: Đối soát Trace Log tìm cảnh báo</b>: Tìm dòng <code>WARNING: No matching files</code> trong job trace của bước build.</li>
      <li><b>Nhịp 4: Kiểm tra xung đột Cache</b>: Kiểm tra xem job deploy có đang vô tình restore lại <code>dist/</code> cũ từ cache thông qua <code>cache:paths</code> hay không.</li>
      <li><b>Nhịp 5: Khắc phục và cô lập vĩnh viễn</b>:
        <ul>
          <li>Bổ sung <code>test -s dist/app.js || exit 1</code> vào cuối job build.</li>
          <li>Thêm mã hash commit vào file bundle và kiểm tra tại đầu job deploy: <code>grep -q "$CI_COMMIT_SHORT_SHA" dist/app.js</code>.</li>
          <li>Xóa bỏ hoàn toàn output build ra khỏi khối <code>cache</code>.</li>
        </ul>
      </li>
    </ol>
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

```mermaid
mindmap
  root((Quản Trị Dữ Liệu Tạm Thời))
    Bản chất Phân biệt
      Artifacts là Hợp đồng Server
      Cache là Khoản đầu tư Tối ưu
      4 bước phục hồi đầu job
    Chiến lược Artifacts
      Tắt tải bằng dependencies rỗng
      when always cho file báo cáo
      expire_in phân tầng ngắn hạn và dài hạn
      Assertion test ngăn ngừa rỗng
    Chiến lược Caching
      Khóa bám theo Hash Lockfile
      S3 MinIO Distributed Backend
      policy pull loại bỏ chi phí ghi
      Phân tích điểm hòa vốn Break-even
```

> [!TIP]
> **Bài học tiếp theo**: Trong bài học kế tiếp [Bài 06: Quản Trị Biến Môi Trường & Bí Mật: Phân Cấp 9 Nấc Ưu Tiên, Masked/Protected Variables & Tích Hợp HashiCorp Vault](gitlab-06-06-bien-va-bi-mat.html), chúng ta sẽ mổ xẻ toàn diện cây phân cấp 9 nấc ưu tiên biến môi trường, cơ chế bảo vệ bí mật chống rò rỉ log và kiến trúc xác thực Keyless OIDC với HashiCorp Vault.
{% endraw %}
