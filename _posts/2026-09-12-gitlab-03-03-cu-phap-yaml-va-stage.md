---
layout: post
title: "[Bài 03] Cú Pháp YAML Cốt Lõi & Thiết Kế Stages: .gitlab-ci.yml, Pipeline Execution Order & Điều Phối Tuyến Tính"
date: 2026-09-12 09:10:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-03
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 3
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.03] Hướng dẫn chuyên sâu Cú Pháp YAML Cốt Lõi & Thiết Kế Stages: .gitlab-ci.yml, Pipeline Execution Order & Điều Phối Tuyến Tính: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Cú Pháp YAML Cốt Lõi & Thiết Kế Stages: .gitlab-ci.yml, Pipeline Execution Order & Điều Phối Tuyến Tính."
  - "Thiết kế CI/CD Pipeline chuẩn Enterprise với kiến trúc DAG, tối ưu hóa thời gian build và caching hiệu quả."
  - "Bảo mật chuỗi cung ứng phần mềm với SAST/DAST, Container Scanning và OIDC Authentication."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 12 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 03] CÚ PHÁP YAML CỐT LÕI & THIẾT KẾ STAGES: .GITLAB-CI.YML, PIPELINE EXECUTION ORDER & ĐIỀU PHỐI TUYẾN TÍNH

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

### 1.1. Luận Đề Trung Tâm: Stage Là Ràng Buộc Thứ Tự, Không Phải Ràng Buộc Dữ Liệu

Trong thiết kế hệ thống CI/CD với GitLab, sai lầm phổ biến nhất của các kỹ sư là coi `stage` như một đường ống dẫn truyền dữ liệu tự động hoặc một bộ cấp phát tài nguyên song song. Trên thực tế:

> **`stage` là một hàng rào thời gian (synchronization barrier), hoàn toàn không phải là kênh vận chuyển dữ liệu và không tự động cấp phát tài nguyên song song.**

```text
   HIỂU SAI (Rất phổ biến)               HIỂU ĐÚNG (Chuẩn kiến trúc)
   stage: build ──dữ liệu──▶ stage: test    stage chỉ là HÀNG RÀO ĐỒNG BỘ THỜI GIAN
        │                                    ├── Dữ liệu luân chuyển qua Artifacts / S3 Cache
        └── "test tự động có thư mục dist/"  └── Độ song song do Runner Concurrent quyết định

   Hai hệ quả nghiêm trọng khi hiểu sai:
   (1) CHẬM: Dựng hàng rào ở nơi không có phụ thuộc dữ liệu → Block tài nguyên vô ích.
   (2) SAI:  Bỏ quên khai báo artifacts vì nghĩ stage tự chuyển → Job xanh ảo, hiện vật rỗng.
```

1. **`stage` chuyển chính xác 0 byte dữ liệu**: Dữ liệu đi qua 4 kênh độc lập (Git clone, Cache, Artifacts, Variables). Stage không nằm trong các kênh này.
2. **`stage` không đảm bảo tính song song**: `stage` chỉ gỡ bỏ ràng buộc tuần tự giữa các job bên trong nó; việc các job có thực sự chạy đồng thời hay không hoàn toàn phụ thuộc vào tham số `concurrent` và `limit` của GitLab Runner trong `config.toml`.
3. **Cái giá của hàng rào thời gian**: Toàn bộ các job ở stage kế tiếp buộc phải chờ job chậm nhất của stage trước hoàn tất, ngay cả khi chúng không hề có bất kỳ quan hệ phụ thuộc dữ liệu nào.

```mermaid
graph TD
    subgraph STAGE_BUILD["Stage: Build"]
        B1["Job: Build Frontend<br/>(10s - sinh dist/)"]
    end

    subgraph STAGE_TEST["Stage: Test (Hàng rào chặn toàn bộ)"]
        T1["Job: Unit Test<br/>(5s - độc lập)"]
        T2["Job: Integration Test<br/>(60s - không sinh artifact)"]
    end

    subgraph STAGE_PACKAGE["Stage: Package"]
        P1["Job: Docker Build<br/>(Chỉ cần dist/ của Build Frontend)"]
    end

    B1 -->|Chờ hoàn thành| T1
    B1 -->|Chờ hoàn thành| T2
    T1 -->|Hàng rào Stage chặn| P1
    T2 -->|Hàng rào Stage chặn 60s| P1

    classDef barrier fill:#f96,stroke:#333,stroke-width:2px;
    class T1,T2 barrier;
```

### 1.2. Nguyên Tắc Loại Trừ Trong Phân Tích Cú Pháp YAML Cấp Trên Cùng

GitLab CI Parser xử lý tệp `.gitlab-ci.yml` dựa trên **nguyên tắc loại trừ** (Exclusion Principle). GitLab định nghĩa sẵn một danh sách các từ khóa dành riêng cấp trên cùng (Top-level Reserved Keywords). **Mọi khóa không nằm trong danh sách từ khóa dành riêng đều được coi là định nghĩa của một Job.**

Danh sách 13 từ khóa dành riêng cấp trên cùng trên GitLab 17.x:
- `stages`: Khai báo danh sách các stage và thứ tự thực thi tuyến tính.
- `default`: Khối tham số mặc định áp dụng chung cho mọi job (`image`, `before_script`, `after_script`, `cache`, `artifacts`, `services`, `tags`, `retry`, `timeout`, `interruptible`).
- `variables`: Khai báo biến môi trường cấp pipeline.
- `include`: Nhúng các tệp cấu hình bên ngoài (local, project, remote, template, component).
- `workflow`: Điều kiện quyết định toàn bộ pipeline có được khởi tạo hay không.
- `image`: Image mặc định cho toàn bộ pipeline (tương đương `default.image`).
- `services`: Container phụ trợ mặc định.
- `cache`: Cấu hình cache mặc định.
- `before_script`: Script mặc định chạy trước mỗi job.
- `after_script`: Script mặc định chạy sau mỗi job.
- `pages`: Job dành riêng để triển khai GitLab Pages static site.
- `hooks`: Hook thực thi tại các giai đoạn vòng đời đặc thù.
- `spec`: Khai báo định nghĩa input/spec cho CI/CD Components.

> [!WARNING]
> **Cạm bẫy Silent Failure do lỗi chính tả**: Nếu kỹ sư gõ sai từ khóa cấp trên cùng (ví dụ `variabels:`, `stgaes:`, `scripts:`), GitLab **không báo lỗi cú pháp**. Parser coi đó là một job mang tên `variabels` hoặc `stgaes`. Kết quả là cấu hình thật bị mất hoàn toàn và một job rác được tạo ra trong trạng thái "xanh ảo".

### 1.3. Cơ Chế Job Ẩn (Hidden Jobs)

Bất kỳ khóa cấp trên cùng nào có tên bắt đầu bằng ký tự dấu chấm (`.`) đều được GitLab CI coi là một **Job Ẩn (Hidden Job)**:
- Không bao giờ được scheduler đưa vào danh sách thực thi.
- Nội dung YAML vẫn được phân giải đầy đủ, phục vụ làm khuôn mẫu (template) cho từ khóa `extends` hoặc YAML Anchors (`&` và `*`).
- Việc bỏ quên dấu chấm khiến template chạy như job thật và thường bị lỗi (do thiếu `script`); ngược lại, thêm nhầm dấu chấm vào job thật khiến job biến mất trong im lặng mà không có cảnh báo.

### 1.4. Vòng Đời Script: 3 Khối Lệnh, 2 Shell Riêng Biệt

Một trong những cơ chế dễ gây hiểu lầm nhất ở tầng thấp là cách GitLab Runner thực thi các khối script trong một job:

```text
  ┌─────────────────────────────────────────────────────────────┐
  │                    SHELL SESSION A                          │
  │  ┌───────────────────────┐     ┌─────────────────────────┐  │
  │  │     before_script     │ ──▶ │         script          │  │
  │  │ (export VAR, cd path) │     │ (Thấy biến & pwd của A) │  │
  │  └───────────────────────┘     └─────────────────────────┘  │
  └─────────────────────────────────────────────────────────────┘
                                 │
                     [script hoàn thành / thất bại]
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                    SHELL SESSION B                          │
  │  ┌───────────────────────────────────────────────────────┐  │
  │  │                    after_script                       │  │
  │  │ (Shell mới: KHÔNG thấy biến export & pwd của shell A) │  │
  │  │ (Vẫn chạy kể cả khi script ở Shell A bị exit code !=0)│  │
  │  └───────────────────────────────────────────────────────┘  │
  └─────────────────────────────────────────────────────────────┘
```

- `before_script` và `script` được Runner nối thành một script duy nhất và thực thi trong **cùng một subshell (Shell A)**. Do đó, các lệnh `cd`, biến môi trường `export`, hoặc hàm shell được định nghĩa ở `before_script` đều có hiệu lực xuyên suốt trong `script`.
- `after_script` được khởi tạo trong một **tiến trình shell hoàn toàn độc lập (Shell B)**. Nó không kế thừa bất kỳ biến môi trường nào được `export` trong `script` và thư mục làm việc quay trở về gốc `$CI_PROJECT_DIR`.
- Để truyền dữ liệu hoặc trạng thái từ `script` sang `after_script`, phương thức duy nhất là ghi ra tệp trong thư mục dự án (shared filesystem).

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

### 2.1. Ma Trận So Sánh Các Cơ Chế Cấu Hình & Điều Phối

| Tiêu chí Kỹ thuật | Sequential Stages | DAG (`needs`) | Hidden Jobs (`.job`) | YAML Anchors (`&/*`) | Multi-project Trigger |
|---|---|---|---|---|---|
| **Cơ chế điều phối** | Đồng bộ theo hàng rào tuyến tính | Đồ thị phi chu trình có hướng | Template cấu hình tĩnh | Tham chiếu cây AST nội bộ | API call bất đồng bộ/đồng bộ |
| **Phạm vi tác động** | Nội bộ pipeline (Linear) | Nội bộ pipeline (Graph) | Khai báo trong hoặc ngoài tệp | Chỉ trong một tệp đơn lẻ | Xuyên project / repository |
| **Độ trễ pipeline** | Cao (chờ job chậm nhất) | Tối ưu tuyệt đối (đường găng) | 0s (không thực thi) | 0s (phân giải compile-time) | Phụ thuộc queue runner ngoài |
| **Chia sẻ biến môi trường** | Qua `.gitlab-ci.yml` / UI | Qua dotenv artifacts | Kế thừa tĩnh qua `extends` | Ghi đè khóa YAML thô | Qua `trigger:forward:pipeline_variables` |
| **Khả năng kế thừa đa tầng** | Không | Không | Rất mạnh (`extends: [...]`) | Kém (dễ xung đột khóa) | Không |
| **Tính tương thích CI Lint** | 100% | Yêu cầu GitLab >= 12.2 | 100% | 100% | Yêu cầu GitLab Premium/Ultimate cho visual |
| **Trường hợp áp dụng tối ưu** | Pipeline đơn giản, ít job | Monorepo, Microservices phức tạp | Chuẩn hóa template doanh nghiệp | Đoạn cấu hình ngắn cục bộ | Triển khai microservice liên repo |

### 2.2. Ma Trận Thứ Tự Ưu Tiên 3 Nấc Cấu Hình (Precedence Rules)

Khi cùng một thuộc tính được khai báo ở nhiều nơi, quy tắc bất biến là: **Gần Job nhất thì thắng (Most specific wins)**, và cơ chế áp dụng là **Thay thế hoàn toàn (Replacement)** chứ không hợp nhất (Merge).

| Thuộc tính | Nấc 1: `config.toml` (Runner) | Nấc 2: `default:` (Pipeline Level) | Nấc 3: Khai báo trong `Job` | Kết quả thực thi | Cơ chế ghi đè |
|---|---|---|---|---|---|
| `image` | `docker.image = "alpine:3.18"` | `image: node:20` | `image: golang:1.22` | `golang:1.22` | Thay thế toàn bộ |
| `before_script` | Không hỗ trợ | `echo "Setup global tools"` | `echo "Setup job specifics"` | Chỉ chạy `Setup job specifics` | Thay thế toàn bộ (Bỏ default) |
| `after_script` | Không hỗ trợ | `echo "Cleanup global"` | `echo "Cleanup job"` | Chỉ chạy `Cleanup job` | Thay thế toàn bộ |
| `tags` | Tags của runner đăng ký | `tags: [shared-docker]` | `tags: [high-cpu, gpu]` | Định tuyến theo `[high-cpu, gpu]` | Thay thế toàn bộ |
| `variables` | `environment = [...]` | `variables: {ENV: "dev", LOG: "info"}` | `variables: {LOG: "debug"}` | `ENV="dev"`, `LOG="debug"` | **Ghi đè từng khóa (Deep merge)** |

> [!IMPORTANT]
> **Ngoại lệ đặc biệt của `variables`**: Trong khi `before_script` hoặc `image` bị thay thế hoàn toàn khi khai báo tại job, từ khóa `variables` lại áp dụng cơ chế **hợp nhất khóa (key-by-key merge)**. Các biến không bị trùng tên ở cấp pipeline vẫn được giữ nguyên trong job.

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (Architecture Breakdown)

### 3.1. Kiến Trúc Pipeline Enterprise Phân Tầng

Một pipeline đạt chuẩn Enterprise cần tách bạch rõ ràng giữa các giai đoạn kiểm soát an ninh đầu vào (`.pre`), các luồng build/test song song, và cổng tổng hợp số liệu an ninh (`.post`).

```text
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │                            PIPELINE EXECUTION ARCHITECTURE                             │
  ├────────────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                        │
  │   [ .pre ] ────────▶ [ Build ] ───────────▶ [ Test & Security ] ───────▶ [ .post ]     │
  │      │                   │                         │                         │         │
  │      ▼                   ▼                         ▼                         ▼         │
  │  gitleaks-scan      compile-app             unit-test-matrix          dora-metrics     │
  │  (Chặn commit có    (Sinh artifacts         (Parallel test chunks)    (Ghi log & audit)│
  │   hardcoded secret)   cho downstream)       sast-semgrep                               │
  │                                             container-trivy-scan                       │
  │                                                                                        │
  └────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2. Mẫu Khung Cấu Hình Production `.gitlab-ci.yml`

```yaml
# ==============================================================================
# PIPELINE ARCHITECTURE TEMPLATE: STANDARDIZED LINEAR & DAG WORKFLOW
# ==============================================================================

stages:
  - build
  - test
  - package
  - deploy

# ------------------------------------------------------------------------------
# 1. Pipeline Variables & Global Defaults
# ------------------------------------------------------------------------------
variables:
  DOCKER_DRIVER: overlay2
  APP_VERSION: "1.4.2"
  DEPLOY_ENV:
    description: "Môi trường triển khai mục tiêu"
    value: "staging"
    options:
      - "staging"
      - "production"

default:
  image: alpine:3.20
  before_script:
    - echo "=== [PIPELINE INIT] Job ${CI_JOB_NAME} started on Runner ${CI_RUNNER_DESCRIPTION} ==="
  after_script:
    - echo "=== [PIPELINE CLEANUP] Job ${CI_JOB_NAME} finished with status ${CI_JOB_STATUS} ==="
  retry:
    max: 1
    when:
      - runner_system_failure
      - stuck_or_timeout_failure

# ------------------------------------------------------------------------------
# 2. Pre-stage Security Gate (Giai đoạn .pre luôn chạy đầu tiên)
# ------------------------------------------------------------------------------
secret-detection-gate:
  stage: .pre
  image: zricethezav/gitleaks:latest
  before_script: [] # Override default before_script
  script:
    - echo "Running GitLeaks secret scan against git commit history..."
    - gitleaks git --verbose --redact
  allow_failure: false

# ------------------------------------------------------------------------------
# 3. Base Templates (Hidden Jobs)
# ------------------------------------------------------------------------------
.node-job-base:
  image: node:20-alpine
  before_script:
    - node -v && npm -v
    - npm ci --cache .npm --prefer-offline
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
    policy: pull

# ------------------------------------------------------------------------------
# 4. Pipeline Execution Jobs
# ------------------------------------------------------------------------------
build-application:
  extends: .node-job-base
  stage: build
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
    policy: pull-push
  script:
    - npm run build
    - test -s dist/index.html || { echo "CRITICAL: Build output missing!"; exit 1; }
  artifacts:
    name: "dist-${CI_COMMIT_SHORT_SHA}"
    paths:
      - dist/
    expire_in: 2 hours

unit-test-chunk-1:
  extends: .node-job-base
  stage: test
  dependencies:
    - build-application
  script:
    - npm run test:unit -- --shard=1/2

unit-test-chunk-2:
  extends: .node-job-base
  stage: test
  dependencies:
    - build-application
  script:
    - npm run test:unit -- --shard=2/2

package-oci-image:
  stage: package
  image: docker:27-cli
  dependencies:
    - build-application
  before_script:
    - docker info
  script:
    - >
      docker build
      --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
      --build-arg COMMIT_SHA="${CI_COMMIT_SHA}"
      --tag "registry.example.com/apps/core:${CI_COMMIT_SHORT_SHA}" .
    - echo "Container image packaged successfully."

# ------------------------------------------------------------------------------
# 5. Post-stage Telemetry (Giai đoạn .post luôn chạy sau cùng)
# ------------------------------------------------------------------------------
telemetry-dora-collection:
  stage: .post
  image: curlimages/curl:8.10.0
  before_script: []
  script:
    - >
      curl -sf -X POST "https://metrics.internal.corp/api/v1/dora/events"
      -H "Content-Type: application/json"
      -d '{"pipeline_id": "'"$CI_PIPELINE_ID"'", "status": "'"$CI_PIPELINE_SOURCE"'", "duration": "'"$CI_PIPELINE_CREATED_AT"'"}'
      || echo "Warning: Telemetry endpoint unreachable."
  when: always
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

### 4.1. Incident 1: Pipeline Xanh Ảo Nhưng Gói Deployment Rỗng (Silent Artifact Loss)

```text
                       SỰ CỐ SILENT ARTIFACT LOSS
  ┌────────────────────────────────────────────────────────────────────────┐
  │ Dòng 3 script: cd services/payment                                     │
  │ Dòng 4 script: npm run build (Sinh bundle tại services/payment/dist/)   │
  │ YAML Artifacts: paths: [dist/] (Runner tìm tại $CI_PROJECT_DIR/dist/)  │
  ├────────────────────────────────────────────────────────────────────────┤
  │ Kết quả: $CI_PROJECT_DIR/dist/ không tồn tại                           │
  │ Runner: Tạo zip archive 148 bytes (chỉ chứa metadata rỗng)             │
  │ Pipeline: Báo SUCCESS (Xanh) -> Deploy container rỗng lên Production!  │
  └────────────────────────────────────────────────────────────────────────┘
```

- **Hiện tượng**: Pipeline build và packaging kết thúc với trạng thái `passed` (màu xanh), nhưng container triển khai lên môi trường Staging bị lỗi `404 Not Found` do thư mục assets rỗng.
- **Phân tích 5-Whys**:
  1. *Tại sao container lại rỗng?* Vì gói artifact `dist.zip` từ job `build` chỉ có kích thước 148 byte, không chứa bất kỳ tệp JavaScript nào.
  2. *Tại sao artifact lại rỗng khi log cho thấy webpack build thành công?* Vì job `build` có lệnh `cd client-app` ở đầu script, file được sinh ra tại `$CI_PROJECT_DIR/client-app/dist`.
  3. *Tại sao runner không báo lỗi khi tìm kiếm artifact?* Vì khai báo `artifacts.paths: [dist/]` trỏ vào thư mục gốc dự án `$CI_PROJECT_DIR/dist`. Bộ thu thập artifact của GitLab Runner không tìm thấy tệp khớp mẫu thì mặc định tạo zip rỗng và xem đó là thành công.
  4. *Tại sao kỹ sư lại dùng `cd client-app` ở dòng đầu?* Vì kỹ sư nhầm tưởng mỗi dòng trong mảng `script: [...]` chạy trong một subshell tách biệt, không ảnh hưởng đến vị trí tệp của runner.
  5. *Nguyên nhân gốc rễ (Root Cause)*: Cơ chế nối chuỗi của GitLab Runner thực thi toàn bộ mảng `script` trong cùng một shell session, khiến lệnh `cd` làm dịch chuyển vĩnh viễn context của cả job mà không có bước assert xác thực tệp trước khi kết thúc.
- **Giải pháp triệt để**:
  1. Luôn sử dụng subshell cho các lệnh chuyển thư mục: `(cd client-app && npm run build)`.
  2. Đặt assertion bắt buộc trước khi kết thúc job: `test -s client-app/dist/index.html || { echo "ASSERTION FAILED"; exit 1; }`.
  3. Khai báo đường dẫn artifacts chính xác từ gốc dự án: `paths: [client-app/dist/]`.

### 4.2. Incident 2: Job Rác Sinh Ra Từ Lỗi Chính Tả Biến Pipeline Thành Lỗ Hổng Bảo Mật

- **Hiện tượng**: Biến môi trường bảo mật `NEXUS_PASSWORD` không được nạp vào job `publish-artifact`, khiến job publish ẩn danh bị thất bại, nhưng hệ thống lại không xuất hiện bất kỳ cảnh báo lỗi cú pháp nào khi chạy `ci/lint`.
- **Phân tích 5-Whys**:
  1. *Tại sao biến không được nạp?* Trong `.gitlab-ci.yml`, biến được khai báo dưới khóa `variabels:`.
  2. *Tại sao GitLab không báo lỗi cú pháp từ khóa sai?* Parser áp dụng nguyên tắc loại trừ: `variabels` không thuộc danh sách từ khóa hệ thống, nên GitLab tự động chuyển nó thành một job độc lập có tên là `variabels`.
  3. *Tại sao job rác đó lại pass?* Job `variabels` không có mảng `script`, nên runner coi như job rỗng và đánh dấu `success` ngay lập tức.
  4. *Tại sao CI Lint không chặn được lỗi này?* Endpoint `ci/lint` chỉ kiểm tra tính hợp lệ về cấu trúc JSON/YAML Schema (tức tệp có phân tích được hay không), chứ không thể đoán định được ý đồ nghiệp vụ của kỹ sư.
  5. *Nguyên nhân gốc rễ (Root Cause)*: Sự thiếu vắng của bước kiểm tra đối soát danh sách Job ID sau phân giải (`resolved jobs`) thông qua API trước khi commit mã nguồn vào nhánh chính.
- **Giải pháp triệt để**: Tích hợp pre-commit hook hoặc pipeline linter gọi API `POST /api/v4/projects/:id/ci/lint` và parse danh sách `.jobs[].name` để so khớp với danh sách job được phê duyệt.

---

## 5. Hands-on Lab: Triển Khai & Phân Tích Cú Pháp YAML & Stages (8 Bước Chuẩn)

### 5.1. Bước 1: Khởi Tạo Project Lab & Thiết Lập Bộ Công Cụ API `ci/lint`

Thiết lập môi trường làm việc và khai báo hàm tiện ích kiểm thử API trực tiếp:

```bash
# Khai báo môi trường kết nối
export GITLAB="http://gitlab.lab:8929"
export GITLAB_TOKEN="glpat-StandardLabTokenAdmin2026"
export HAU_TO="devops-engineer"

# Tạo project kiểm thử trên GitLab
PID3=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN"   --header "Content-Type: application/json"   --data "{"name":"lab03-cu-phap-stages-${HAU_TO}","visibility":"internal"}"   "$GITLAB/api/v4/projects" | jq -r .id)

echo "Created Lab Project ID: $PID3"

# Thiết lập thư mục làm việc và hàm kiểm thử API
mkdir -p ~/lab03 && cd ~/lab03
git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/root/lab03-cu-phap-stages-${HAU_TO}.git"
git config user.email "lab@internal.corp"
git config user.name "Lab Engineer"

cat > cong-cu.sh <<'SH'
#!/usr/bin/env bash
lint_check() {
  curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN"     --header "Content-Type: application/json"     --data "$(jq -Rs '{content: ., include_merged_yaml: true}' < "${1:-.gitlab-ci.yml}")"     "$GITLAB/api/v4/projects/$PID3/ci/lint"
}
lint_jobs() { lint_check "${1:-.gitlab-ci.yml}" | jq -r '.jobs[]?.name'; }
lint_valid() { lint_check "${1:-.gitlab-ci.yml}" | jq -r '.valid'; }
SH
source cong-cu.sh
```

### 5.2. Bước 2: Kiểm Chứng Nguyên Tắc Loại Trừ & Cơ Chế Sinh Job Rác

Tạo tệp `.gitlab-ci.yml` chứa các lỗi chính tả phổ biến để đo lường hành vi của GitLab CI Parser:

```yaml
# ~/lab03/.gitlab-ci.yml
stages:
  - build
  - test

variabels:                 # GÕ SAI: biến thành job rác tên "variabels"
  DATABASE_URL: "postgres://prod.internal"

stgaes:                    # GÕ SAI: biến thành job rác tên "stgaes"
  - compile
  - verify

build:
  stage: build
  image: alpine:3.20
  script:
    - echo "Executing production build..."

test:
  stage: test
  image: alpine:3.20
  script:
    - echo "Database connection string is: [${DATABASE_URL}]"
```

Thực thi kiểm tra qua CI Lint:

```bash
cd ~/lab03
echo "=== TRẠNG THÁI HỢP LỆ CỦA TỆP CÚ PHÁP ==="
lint_valid
echo "=== DANH SÁCH JOB SAU PHÂN GIẢI (RESOLVED JOBS) ==="
lint_jobs
```

> **CHECKPOINT 1**: Kết quả `lint_valid` trả về `true` dù có 2 lỗi chính tả nghiêm trọng. Danh sách job sau phân giải xuất hiện thêm `variabels` và `stgaes`.

### 5.3. Bước 3: Cấu Hình Job Ẩn (`.hidden_job`) & Template Inheritance

Hiệu chỉnh lại cấu hình, áp dụng Job Ẩn làm template chuẩn hóa:

```yaml
# ~/lab03/.gitlab-ci.yml
stages:
  - build
  - test

variables:
  APP_ENV: "staging"

.base_node_template:
  image: node:20-alpine
  before_script:
    - echo "=== Standard Node Environment Setup ==="
    - node -v

build_app:
  extends: .base_node_template
  stage: build
  script:
    - echo "Compiling Node.js assets in environment ${APP_ENV}..."

unit_test:
  extends: .base_node_template
  stage: test
  script:
    - echo "Running test suite against environment ${APP_ENV}..."
```

Kiểm tra danh sách job qua API:

```bash
cd ~/lab03
lint_jobs
```

> **CHECKPOINT 2**: Parser chỉ ghi nhận 2 job thực thi là `build_app` và `unit_test`. Job template `.base_node_template` được giữ dưới dạng AST template và hoàn toàn không nằm trong scheduler queue.

### 5.4. Bước 4: Đo Đạc Thực Nghiệm: `stage` Chuyển 0 Byte Dữ Liệu

Chứng minh việc job ở stage sau không thể đọc file của stage trước nếu không khai báo `artifacts`:

```yaml
# ~/lab03/.gitlab-ci.yml
stages:
  - build
  - test

build_without_artifacts:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p build_output
    - echo "PAYLOAD_DATA_2026" > build_output/app.bin
    - echo "Build artifact created at $(pwd)/build_output/app.bin"

test_data_transfer:
  stage: test
  image: alpine:3.20
  script:
    - echo "Verifying data transfer from previous stage..."
    - ls -la build_output/app.bin
```

Đẩy mã nguồn và theo dõi pipeline:

```bash
cd ~/lab03
git add .gitlab-ci.yml && git commit -m "lab: test data transfer across stages" && git push origin main

# Chờ pipeline thực thi
sleep 25
PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines?per_page=1" | jq -r '.[0].id')
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines/$PIPE_ID/jobs" | jq -r '.[] | [.name, .stage, .status] | @tsv'
```

> **CHECKPOINT 3**: Job `test_data_transfer` thất bại với mã lỗi `exit code 1` do `ls: build_output/app.bin: No such file or directory`. Khẳng định: `stage` không chuyển bất kỳ byte dữ liệu nào.

### 5.5. Bước 5: Đo Lường Định Lượng Lãng Phí Hàng Rào (Barrier Waste)

Triển khai pipeline có sự phân hóa về thời gian thực thi giữa các job trong cùng stage để đo lường lãng phí hàng rào:

```yaml
# ~/lab03/.gitlab-ci.yml
stages:
  - .pre
  - build
  - test
  - deploy

security_gate:
  stage: .pre
  image: alpine:3.20
  script:
    - echo "Pre-flight security check..."

build_job:
  stage: build
  image: alpine:3.20
  script:
    - sleep 10
    - mkdir -p dist && echo "bundle_v1" > dist/bundle.js
  artifacts:
    paths: [dist/]

test_fast:
  stage: test
  image: alpine:3.20
  dependencies: []
  script:
    - sleep 5

test_slow:
  stage: test
  image: alpine:3.20
  dependencies: []
  script:
    - sleep 45 # Job chậm làm giữ chân hàng rào

deploy_job:
  stage: deploy
  image: alpine:3.20
  script:
    - test -s dist/bundle.js || exit 1
    - echo "Deployed successfully in 2 seconds"
```

Thực thi và tính toán chỉ số:

```bash
cd ~/lab03
git add .gitlab-ci.yml && git commit -m "lab: measure barrier waste" && git push origin main
sleep 70

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines?per_page=1" | jq -r '.[0].id')

# Lấy tổng thời gian pipeline và thời gian từng job
TOTAL_DURATION=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines/$PIPE_ID" | jq -r '.duration')
BUILD_DUR=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines/$PIPE_ID/jobs" | jq -r '.[] | select(.name=="build_job") | .duration')
DEPLOY_DUR=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines/$PIPE_ID/jobs" | jq -r '.[] | select(.name=="deploy_job") | .duration')

CRITICAL_PATH=$((BUILD_DUR + DEPLOY_DUR))
BARRIER_WASTE=$((TOTAL_DURATION - CRITICAL_PATH))

echo "Total Pipeline Duration: ${TOTAL_DURATION}s"
echo "Data Critical Path (Build -> Deploy): ${CRITICAL_PATH}s"
echo "Barrier Waste (Lãng phí hàng rào): ${BARRIER_WASTE}s"
```

> **CHECKPOINT 4**: Chỉ số `BARRIER_WASTE` đạt ~45 giây. `deploy_job` bị chặn hoàn toàn bởi `test_slow` dù nó chỉ cần artifact của `build_job`.

### 5.6. Bước 6: Phân Tích Song Song Trong Stage Phụ Thuộc `concurrent`

Cấu hình 4 job chạy trong cùng một stage và thay đổi `concurrent` trong Runner daemon để quan sát hành vi:

```yaml
# ~/lab03/.gitlab-ci.yml
stages:
  - parallel_stage

.parallel_base:
  stage: parallel_stage
  image: alpine:3.20
  script:
    - echo "Job ${CI_JOB_NAME} running on thread..."
    - sleep 15

p1: {extends: .parallel_base}
p2: {extends: .parallel_base}
p3: {extends: .parallel_base}
p4: {extends: .parallel_base}
```

Thực nghiệm đo đạc:

```bash
cd ~/lab03
git add .gitlab-ci.yml && git commit -m "lab: concurrency verification" && git push origin main
sleep 30

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines?per_page=1" | jq -r '.[0].id')
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines/$PIPE_ID/jobs"   | jq -r '.[] | [.name, .started_at, .finished_at, .duration] | @tsv'
```

> **CHECKPOINT 5**: Nếu Runner cấu hình `concurrent = 1`, 4 job mất tổng cộng 60s (chạy nối đuôi nhau). Nếu Runner cấu hình `concurrent = 4`, toàn bộ stage hoàn thành trong ~16s.

### 5.7. Bước 7: Thực Nghiệm 3 Khối Lệnh, 2 Shell & Khắc Phục Lỗi `cd` Xuyên Dòng

Kiểm chứng phạm vi biến môi trường và thư mục làm việc qua 3 khối script:

```yaml
# ~/lab03/.gitlab-ci.yml
stages:
  - shell_test

shell_execution_analysis:
  stage: shell_test
  image: alpine:3.20
  before_script:
    - export SHARED_VAR="CREATED_IN_BEFORE_SCRIPT"
    - echo "[BEFORE] Current Directory: $(pwd)"
  script:
    - echo "[SCRIPT] Shared Variable in Shell A: [${SHARED_VAR}]"
    - mkdir -p sub_dir && cd sub_dir
    - echo "[SCRIPT] Changed Directory: $(pwd)"
    - export SCRIPT_VAR="CREATED_IN_SCRIPT"
  after_script:
    - echo "[AFTER] Current Directory in Shell B: $(pwd)"
    - echo "[AFTER] Shared Variable: [${SHARED_VAR:-NOT_FOUND}]"
    - echo "[AFTER] Script Variable: [${SCRIPT_VAR:-NOT_FOUND}]"
```

Đẩy pipeline và phân tích job trace:

```bash
cd ~/lab03
git add .gitlab-ci.yml && git commit -m "lab: verify shell scoping" && git push origin main
sleep 20

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines?per_page=1" | jq -r '.[0].id')
JOB_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines/$PIPE_ID/jobs" | jq -r '.[0].id')

curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/jobs/$JOB_ID/trace"   | grep -E '\[(BEFORE|SCRIPT|AFTER)\]'
```

> **CHECKPOINT 6**: Log hiển thị:
> - `[SCRIPT]` thấy `$SHARED_VAR`.
> - `[AFTER]` in ra `NOT_FOUND` cho cả `$SHARED_VAR` và `$SCRIPT_VAR`.
> - `[AFTER]` có current directory quay về thư mục gốc dự án `$CI_PROJECT_DIR`.

### 5.8. Bước 8: Kiểm Chứng Thứ Tự Ưu Tiên 3 Nấc Cấu Hình & Dọn Dẹp

Kiểm tra quy tắc ghi đè cấu hình:

```yaml
# ~/lab03/.gitlab-ci.yml
stages:
  - precedence_check

default:
  image: alpine:3.20
  before_script:
    - echo "GLOBAL_DEFAULT_BEFORE_SCRIPT"

job_default_inheritance:
  stage: precedence_check
  script:
    - echo "Executing with default image & before_script"

job_custom_override:
  stage: precedence_check
  image: debian:12-slim
  before_script:
    - echo "OVERRIDDEN_JOB_SPECIFIC_BEFORE_SCRIPT"
  script:
    - cat /etc/os-release | grep '^PRETTY_NAME'
```

```bash
cd ~/lab03
git add .gitlab-ci.yml && git commit -m "lab: verify configuration precedence" && git push origin main
sleep 25

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines?per_page=1" | jq -r '.[0].id')
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3/pipelines/$PIPE_ID/jobs" | jq -r '.[] | [.name, .status] | @tsv'

# Dọn dẹp tài nguyên lab
curl -sf --request DELETE --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID3"
echo "Lab 03 resources cleaned up successfully."
```

> **CHECKPOINT 7 & 8**: `job_custom_override` chạy trên OS Debian và chỉ xuất hiện log `OVERRIDDEN_JOB_SPECIFIC_BEFORE_SCRIPT` (log của default bị loại bỏ hoàn toàn, không có cơ chế nối chuỗi). Toàn bộ project lab được dọn dẹp sạch sẽ.

---

## 6. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span>Bản chất của từ khóa `stage` trong GitLab CI là gì? Nó cho ta điều gì và KHÔNG cho ta những điều gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Bản chất kỹ thuật</b>: <code>stage</code> là một <b>ràng buộc đồng bộ thời gian (synchronization barrier)</b>. Nó xác định thứ tự thực thi tuyến tính: các job thuộc stage $N$ chỉ được cấp phát vào hàng đợi sau khi toàn bộ các job thuộc stage $N-1$ đã hoàn thành thành công (hoặc thỏa mãn <code>allow_failure</code>).</p>
    <p><b>Hai điều `stage` KHÔNG cung cấp</b>:</p>
    <ul>
      <li><b>Không chuyển dữ liệu</b>: <code>stage</code> chuyển chính xác <b>0 byte</b> dữ liệu giữa các job. Dữ liệu chỉ luân chuyển khi có khai báo tường minh qua <code>artifacts</code> hoặc <code>cache</code>. Mặc định GitLab tự động download artifacts của các stage trước đó dễ gây ngộ nhận rằng stage tự chuyển dữ liệu.</li>
      <li><b>Không đảm bảo tính song song</b>: Việc gom 10 job vào cùng một stage chỉ có nghĩa là chúng <i>đủ điều kiện chạy đồng thời</i>. Việc chúng có chạy song song hay không phụ thuộc hoàn toàn vào tham số <code>concurrent</code> trong <code>config.toml</code> của Runner daemon.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span>Làm thế nào GitLab CI Parser phân biệt giữa một Job thật và một từ khóa cấu hình cấp trên cùng (Top-level Keyword)?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p>GitLab CI Parser xử lý tệp cấu hình dựa trên <b>Nguyên tắc loại trừ (Exclusion Principle)</b>:</p>
    <ul>
      <li>Parser duy trì một danh sách các từ khóa dành riêng cấp trên cùng cố định (13 từ khóa trên GitLab 17.x: <code>stages</code>, <code>default</code>, <code>variables</code>, <code>include</code>, <code>workflow</code>, <code>image</code>, <code>services</code>, <code>cache</code>, <code>before_script</code>, <code>after_script</code>, <code>pages</code>, <code>hooks</code>, <code>spec</code>).</li>
      <li>Mọi khóa không nằm trong danh sách trên đều được coi là một <b>Job Definition</b>.</li>
      <li>Ngoại lệ: Các khóa bắt đầu bằng dấu chấm (<code>.</code>) được xếp loại là <b>Hidden Jobs</b> và bị bỏ qua trong quá trình lập lịch thực thi.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span>Khi kỹ sư gõ sai từ khóa cấp trên cùng (ví dụ `variabels:` thay vì `variables:`), hệ thống phản ứng thế nào? Tại sao đây là lỗi nguy hiểm?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Phản ứng hệ thống</b>: GitLab <b>không báo lỗi cú pháp</b> và CI Lint vẫn trả về <code>valid: true</code>. Theo nguyên tắc loại trừ, GitLab tạo một job thực thi có tên là <code>variabels</code>.</p>
    <p><b>Độ nguy hiểm thực chiến</b>: Thuộc nhóm cạm bẫy <b>Silent Failure (Hỏng hóc trong im lặng)</b>:</p>
    <ol>
      <li>Job rác <code>variabels</code> không có script nên thường pass ngay lập tức (xanh ảo).</li>
      <li>Toàn bộ các biến môi trường cấu hình bên trong khối đó bị mất hoàn toàn. Các job downstream tham chiếu đến biến sẽ nhận chuỗi rỗng (<code>""</code>). Shell script không crash nếu không bật <code>set -u</code>, dẫn đến việc ứng dụng build/deploy sai cấu hình lên production mà không ai hay biết.</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span>Nếu một stage chứa 6 job, mỗi job chạy mất 30 giây. Tổng thời gian hoàn thành stage đó là bao lâu? Yếu tố nào quyết định?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="6 9 12 15 18 9"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p>Thời gian hoàn thành stage dao động từ <b>30 giây đến 180 giây</b>, hoàn toàn phụ thuộc vào năng lực xử lý đồng thời của hạ tầng Runner:</p>
    <ul>
      <li><b>Trường hợp tối ưu (Song song hoàn toàn)</b>: Nếu Runner có <code>concurrent &gt;= 6</code> và đủ tài nguyên CPU/RAM, 6 job chạy đồng thời &rarr; Thời gian stage = $\max(t_1, \dots, t_6) \approx \mathbf{30s}$.</li>
      <li><b>Trường hợp xấu nhất (Tuần tự hóa)</b>: Nếu Runner có <code>concurrent = 1</code>, 6 job phải xếp hàng nối đuôi nhau &rarr; Thời gian stage = $\sum_{i=1}^{6} t_i = 6 \times 30 = \mathbf{180s}$.</li>
    </ul>
    <p><i>Kết luận</i>: <code>stage</code> chỉ cấp phép chạy song song, <code>config.toml</code> của Runner mới quyết định mức độ song song thực tế.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span>Khái niệm "Lãng phí hàng rào" (Barrier Waste) và "Đường găng dữ liệu" (Data Critical Path) được định nghĩa và tính toán như thế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="6 9 12 15 18 9"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Định nghĩa toán học</b>:</p>
    $$\text{Barrier Waste} = \text{Tổng thời gian Pipeline} - \text{Đường găng dữ liệu thật (Critical Path)}$$
    <ul>
      <li><b>Đường găng dữ liệu thật</b>: Chuỗi phụ thuộc artifacts dài nhất từ job khởi tạo đến job kết thúc. Đây là giới hạn vật lý tối thiểu mà pipeline không thể chạy nhanh hơn.</li>
      <li><b>Lãng phí hàng rào</b>: Tổng thời gian các job hạ nguồn phải chờ đợi vô ích các job khác trong cùng stage hoàn thành, mặc dù giữa chúng không hề có quan hệ phụ thuộc dữ liệu.</li>
    </ul>
    <p><i>Ý nghĩa tối ưu</i>: Con số Barrier Waste chính là lượng thời gian tối đa có thể cắt giảm khi chuyển dịch từ mô hình Sequential Stages sang đồ thị DAG (<code>needs: [...]</code>).</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span>Hai stage ngầm định `.pre` và `.post` có đặc tính gì và được sử dụng trong các tình huống thực tế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="6 9 12 15 18 9"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Đặc tính kỹ thuật</b>: <code>.pre</code> và <code>.post</code> là hai stage dựng sẵn luôn tồn tại mà không cần khai báo trong mảng <code>stages:</code>. Job thuộc <code>.pre</code> luôn chạy trước mọi stage; Job thuộc <code>.post</code> luôn chạy sau cùng.</p>
    <p><b>Ứng dụng thực tế trong Enterprise</b>:</p>
    <ul>
      <li><code>.pre</code>: Dùng cho các tác vụ kiểm soát an ninh tiên quyết (Pre-flight Security Gate) như quét hardcoded secrets (GitLeaks, TruffleHog), kiểm tra cấu trúc branch, xác thực policy Open Policy Agent. Giúp fail pipeline ngay từ giây thứ 5 trước khi tốn tài nguyên build/test nặng.</li>
      <li><code>.post</code>: Dùng cho các tác vụ đo đạc viễn trắc (Telemetry), gửi số liệu DORA metrics, giải phóng môi trường tạm thời hoặc gửi thông báo tổng hợp trạng thái pipeline với <code>when: always</code>.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span>Phân tích vòng đời thực thi của 3 khối lệnh `before_script`, `script`, `after_script`. Chúng chia sẻ bao nhiêu phiên shell? Làm thế nào để truyền dữ liệu sang `after_script`?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="6 9 12 15 18 9"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Cơ chế phân tách Shell</b>: 3 khối lệnh chạy trong đúng <b>2 phiên shell độc lập</b>:</p>
    <ul>
      <li><b>Shell Session 1</b>: Nối chung <code>before_script</code> và <code>script</code>. Các biến môi trường <code>export</code>, alias, hàm shell và thay đổi thư mục (<code>cd</code>) ở <code>before_script</code> đều được giữ nguyên trong <code>script</code>.</li>
      <li><b>Shell Session 2</b>: Dành riêng cho <code>after_script</code>. Chạy trong một process mới hoàn toàn, không thừa hưởng biến môi trường trong Session 1 và working directory luôn reset về <code>$CI_PROJECT_DIR</code>. Khối này luôn được kích hoạt kể cả khi Session 1 bị fail (non-zero exit code).</li>
    </ul>
    <p><b>Phương pháp truyền dữ liệu</b>: Để truyền trạng thái hoặc biến từ <code>script</code> sang <code>after_script</code>, bắt buộc phải <b>ghi ra tệp vật lý</b> trên workspace (ví dụ: <code>echo "STATUS=FAIL" &gt; /tmp/status.txt</code> hoặc ghi vào tệp trong <code>$CI_PROJECT_DIR</code>) để <code>after_script</code> đọc lại.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span>Tại sao lệnh `cd` trong mảng `script` có thể dẫn đến sự cố artifact rỗng nhưng job vẫn xanh? Nêu 3 giải pháp phòng ngừa chuẩn?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="6 9 12 15 18 9"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Cơ chế gây lỗi</b>: Toàn bộ mảng <code>script: [...]</code> được runner ghép thành một tệp shell script liên tục. Lệnh <code>cd subfolder</code> ở dòng $k$ làm thay đổi current working directory cho toàn bộ các dòng $k+1, \dots$. Khi job kết thúc, bước <code>upload_artifacts</code> tìm kiếm đường dẫn từ gốc <code>$CI_PROJECT_DIR</code>, không tìm thấy file và mặc định tạo file zip rỗng &rarr; Job xanh nhưng artifact không có dữ liệu.</p>
    <p><b>3 Giải pháp phòng ngừa chuẩn</b>:</p>
    <ol>
      <li><b>Sử dụng Subshell</b>: Cô lập lệnh thay đổi thư mục trong ngoặc đơn: <code>(cd subfolder &amp;&amp; npm run build)</code> để không làm ảnh hưởng context ngoài.</li>
      <li><b>Sử dụng biến gốc tuyệt đối</b>: Luôn tham chiếu đường dẫn với biến hệ thống <code>$CI_PROJECT_DIR/subfolder/dist</code> hoặc <code>cd "$CI_PROJECT_DIR"</code> trước khi kết thúc job.</li>
      <li><b>Assertion bắt buộc</b>: Đặt lệnh kiểm tra sự tồn tại và dung lượng file trước khi thoát: <code>test -s dist/app.js || { echo "ASSERTION FAILED"; exit 1; }</code>.</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span>Những ký tự đặc biệt nào khiến YAML parser hiểu sai dòng lệnh script? Phân biệt chuỗi khối `|` (Literal) và `>` (Folded)?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>8 ký tự đặc biệt cần chú ý</b>: Dấu hai chấm theo sau bởi khoảng trắng (<code>: </code>), và các ký tự mở đầu dòng <code>*</code>, <code>&</code>, <code>{</code>, <code>[</code>, <code>|</code>, <code>></code>, <code>%</code>, <code>@</code> khiến YAML hiểu nhầm là Mapping, Anchor, Reference, hoặc Inline Array.</p>
    <p><b>Phân biệt Block Scalar Styles</b>:</p>
    <ul>
      <li><b>Toán tử <code>|</code> (Literal Block Scalar)</b>: <b>Giữ nguyên các ký tự xuống dòng</b>. Thích hợp cho các đoạn script nhiều dòng, cấu trúc điều kiện <code>if / else</code>, vòng lặp <code>for</code>.</li>
      <li><b>Toán tử <code>></code> (Folded Block Scalar)</b>: <b>Gộp các dòng liên tiếp thành một dòng duy nhất</b> (thay thế ký tự xuống dòng bằng dấu cách). Thích hợp cho các câu lệnh CLI dài có nhiều tham số như <code>docker build ...</code> hoặc <code>helm upgrade ...</code>.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span>Khi một thuộc tính (ví dụ `image` hoặc `before_script`) được khai báo ở cả 3 nơi: `config.toml`, `default:`, và trong `Job`, giá trị nào sẽ thắng? Cơ chế ghi đè diễn ra như thế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Quy tắc ưu tiên</b>: Giá trị khai báo <b>trong chính Job (Nấc 3) sẽ thắng</b> theo nguyên tắc "Gần Job nhất thì thắng". Thứ tự từ thấp đến cao: <code>config.toml</code> (Runner) &rarr; <code>default:</code> (Pipeline) &rarr; Khai báo trong <code>Job</code>.</p>
    <p><b>Cơ chế ghi đè</b>: Áp dụng cơ chế <b>Thay thế toàn bộ (Full Replacement)</b>, hoàn toàn không có sự kế thừa hay nối chuỗi (Merge):</p>
    <ul>
      <li>Nếu <code>default:</code> khai báo <code>before_script: [echo "A"]</code> và Job khai báo <code>before_script: [echo "B"]</code>, job sẽ chỉ chạy duy nhất lệnh <code>echo "B"</code>.</li>
      <li><i>Ngoại lệ duy nhất</i>: Khối <code>variables</code> áp dụng cơ chế <b>Deep Merge theo khóa</b> (Job ghi đè các khóa trùng tên và giữ nguyên các khóa không trùng tên từ cấp pipeline).</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q11</span>
    <span>Job Ẩn (Hidden Job) là gì? Khi nào NÊN và KHÔNG NÊN sử dụng Job Ẩn trong thiết kế CI/CD?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Định nghĩa</b>: Job Ẩn là job có tiền tố dấu chấm (ví dụ <code>.deploy_template:</code>). GitLab Parser phân tích cấu trúc nhưng loại bỏ khỏi hàng đợi thực thi.</p>
    <p><b>Khi nào NÊN sử dụng</b>: Khi có từ 2 job trở lên chia sẻ chung logic phức tạp (cùng <code>image</code>, <code>cache</code>, <code>retry</code>, <code>before_script</code>) để tái sử dụng qua từ khóa <code>extends: .deploy_template</code>, giúp giảm lặp mã (DRY).</p>
    <p><b>Khi nào KHÔNG NÊN sử dụng</b>:</p>
    <ul>
      <li>Khi chỉ có duy nhất 1 job sử dụng template đó (tạo ra sự phức tạp gián tiếp không cần thiết).</li>
      <li>Khi template chứa logic thay đổi liên tục giữa các job con dẫn đến việc phải ghi đè quá nhiều khóa trong job kế thừa.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q12</span>
    <span>Khi một đội ngũ phản ánh pipeline CI/CD chạy quá chậm, quy trình 3 nhịp chẩn đoán và xử lý tối ưu của bạn là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <p><b>Quy trình 3 nhịp chuẩn hóa (Data-Driven Optimization)</b>:</p>
    <ol>
      <li><b>Nhịp 1: Lập bản đồ phụ thuộc dữ liệu (Data Dependency Mapping)</b>: Trả lời câu hỏi <i>"Job này thực sự cần artifact từ những job nào?"</i> để vẽ ra <b>Đường găng dữ liệu thật (Critical Path)</b>.</li>
      <li><b>Nhịp 2: Định lượng Lãng phí hàng rào (Barrier Waste Calculation)</b>:
      $$\text{Barrier Waste} = \text{Tổng thời gian Pipeline} - \text{Thời gian Critical Path}$$
      Nếu lãng phí lớn &rarr; Chuyển dịch ngay sang mô hình DAG với từ khóa <code>needs: [...]</code>.</li>
      <li><b>Nhịp 3: Phân loại và tối ưu tầng hạ tầng/cấu hình</b>:
        <ul>
          <li>Nếu <code>queued_duration</code> cao &rarr; Runner thiếu slot, cần tăng <code>concurrent</code> hoặc cấu hình Autoscaling Runner.</li>
          <li>Nếu pha <code>download_artifacts</code> tốn thời gian &rarr; Thêm <code>dependencies: []</code> cho các job độc lập.</li>
          <li>Nếu pha tải package dependency chậm &rarr; Tối ưu phân tầng Distributed Cache (S3/MinIO) và fallback key.</li>
        </ul>
      </li>
    </ol>
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

```mermaid
mindmap
  root((GitLab CI Cú Pháp & Stages))
    Bản chất Stage
      Hàng rào thời gian tuyến tính
      Chuyển đúng 0 byte dữ liệu
      Độ song song do Runner concurrent
      Hai stage ngầm định .pre và .post
    Cú pháp Tầng thấp
      Nguyên tắc loại trừ Top-level
      Job ẩn template với dấu chấm
      3 khối lệnh chia 2 shell session
      Cạm bẫy cd xuyên dòng & YAML nuốt ký tự
    Tối ưu Hóa
      Đường găng dữ liệu Critical Path
      Chỉ số Lãng phí Hàng rào Barrier Waste
      Quy tắc ưu tiên 3 nấc ghi đè
```

> [!TIP]
> **Bài học tiếp theo**: Trong bài học kế tiếp [Bài 04: Điều Kiện Thực Thi Nâng Cao: Rules, Workflow, Dynamic Conditions & Bảng Chân Trị 12 Kịch Bản Kích Hoạt](gitlab-04-04-rules-va-workflow.html), chúng ta sẽ phân tích toàn diện cơ chế kiểm soát vòng đời pipeline với `rules:`, `workflow:rules`, và xây dựng ma trận chân trị điều phối kích hoạt chuẩn Enterprise.
{% endraw %}
