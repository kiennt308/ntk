---
title: "Bài 47: Khắc Phục Sự Cố Pipeline Chuyên Sâu, Debugging & Chiến Lược Vận Hành Khẩn Cấp (Troubleshooting & Incident Management)"
date: 2026-09-12 00:00:00 +0700
categories: [GitLab, CI/CD, DevSecOps]
tags: [GitLab-CI, Troubleshooting, Debugging, Exit-Codes, Runner-Logs, Interactive-Terminal, Incident-Management, Observability]
description: "Cẩm nang khắc phục sự cố CI/CD toàn diện: Phương pháp luận 5 bước phân tích root cause, giải mã toàn bộ mã lỗi exit code (137, 143, 127...), gỡ rối SSL/TLS, Job Token và kỹ thuật Interactive Web Terminal debug."
---

{% raw %}
> [!IMPORTANT]
> **Mục tiêu kỹ thuật then chốt**:
> - Làm chủ phương pháp luận chẩn đoán sự cố CI/CD 5 bước (Observe $ightarrow$ Isolate $ightarrow$ Reproduce $ightarrow$ Remediate $ightarrow$ Automate).
> - Giải mã bản chất tầng thấp của các mã lỗi phổ biến: **Exit code 137 (OOM Killer)**, **Exit code 143 (SIGTERM / Timeout)**, **Exit code 127 (Command Not Found)**, **Exit code 1 (Application Error)**.
> - Xử lý triệt để các lỗi hạ tầng phức tạp: SSL/TLS x509 Certificate verification, Docker daemon socket permissions, CI_JOB_TOKEN permissions denied và distributed cache corruption.
> - Vận hành công cụ gỡ rối nâng cao: Kích hoạt `CI_DEBUG_TRACE`, sử dụng **GitLab Interactive Web Terminal** và khai thác hệ thống Runner System Logs.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

### 1.1. Vòng Đời Thực Thi Job & Ma Trận Phân Vùng Lỗi (Failure Isolation Matrix)

Khi một GitLab Runner nhận một Job từ GitLab Server (qua giao thức gRPC / HTTP long-polling), quá trình thực thi trải qua 6 giai đoạn nghiêm ngặt. Việc xác định chính xác **giai đoạn xảy ra lỗi** là chìa khóa để cô lập nguyên nhân:

```
+---------------------------------------------------------------------------------------------------+
|                                  GITLAB JOB EXECUTION LIFECYCLE                                   |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [1. PREPARE]         [2. PRE-CLONE]       [3. GET SOURCES]   [4. RESTORE CACHE]   [5. USER SCRIPT]  [6. ARTIFACTS] |
|  - Create Container   - Pull helper image  - Git clone/fetch  - Download cache     - `before_script`  - Zip & upload |
|  - Mount volumes      - Auth Docker reg    - Checkout SHA     - Extract tarball    - `script`         - Upload logs  |
|  - Check limits       - Net setup          - Init submodules  - Perms check        - `after_script`   - Clean space  |
|         |                   |                    |                   |                   |               |        |
|         v                   v                    v                   v                   v               v        |
|    [Runner Host /      [Network / DNS /     [GitLab Server /    [S3 / MinIO /        [App Code / Dev   [GitLab S3 /   |
|     Docker Engine]      Auth Registry]       Disk Space]         Network I/O]         Dependencies]     Object Store] |
+---------------------------------------------------------------------------------------------------+
```

#### Ma Trận Phân Loại Điểm Lỗi (Failure Domain Matrix)

| Giai Đoạn (Phase) | Triệu Chứng Lỗi Điển Hình | Nguyên Nhân Gốc (Root Cause) | Trách Nhiệm (Owner) |
| :--- | :--- | :--- | :--- |
| **1. Prepare / Pod Init** | `API error: cannot create container`, `Pod stuck in Pending` | Hết tài nguyên Node (CPU/RAM), Image Pull Backoff, Storage limit | Platform / Infra Team |
| **2. Pre-Clone & Auth** | `x509: certificate signed by unknown authority` | Thiếu CA Root Certificates, lỗi mTLS, proxy chặn | Security / Infra Team |
| **3. Get Sources** | `fatal: unable to access: The requested URL returned error: 403` | `CI_JOB_TOKEN` không có quyền truy cập repo phụ (Inbound/Outbound rules) | GitLab Project Admin |
| **4. Restore Cache** | `WARNING: file extraction failed: no space left on device` | Runner disk bị đầy, phân quyền thư mục `/builds` không khớp UID | Infra / Runner Team |
| **5. User Script** | `Command terminated with exit code 137 / 143 / 127` | OOM Killer, Job Timeout, binary thiếu dependencies (glibc/musl) | Dev / Application Team |
| **6. Artifact Upload** | `FATAL: Uploading artifacts to coordinator... too large` | Vượt quá `max_artifacts_size` của GitLab Instance | Project / GitLab Admin |

---

### 1.2. Bản Chất Các Mã Lỗi Hệ Thống (Linux Exit Codes) Trong CI/CD

Linux Process Exit Code tuân theo chuẩn POSIX. Khi một tiến trình bị terminated bởi tín hiệu hệ điều hành (Signal), mã thoát được tính bằng công thức:

$$	ext{Exit Code} = 128 + 	ext{Signal Number}$$

```
+---------------------------------------------------------------------------------------------------+
|                                  POSIX PROCESS EXIT CODE TAXONOMY                                 |
+---------------------------------------------------------------------------------------------------+
|  Exit Code 0   : Thành công hoàn toàn (SUCCESS)                                                   |
|  Exit Code 1   : Lỗi ứng dụng chung (General catchall error / Unhandled Exception)                |
|  Exit Code 2   : Sai cú pháp lệnh Shell (Misuse of shell builtins)                                |
|  Exit Code 126 : Lệnh tìm thấy nhưng không có quyền thực thi (Permission denied)                  |
|  Exit Code 127 : Lệnh không tồn tại trong PATH (Command not found)                                |
|  Exit Code 128 : Tham số thoát không hợp lệ cho lệnh exit                                         |
|  Exit Code 130 : Tiến trình bị hủy bởi Ctrl+C (128 + SIGINT = 128 + 2)                            |
|  Exit Code 137 : Tiến trình bị hủy cưỡng chế bởi OOM Killer (128 + SIGKILL = 128 + 9)              |
|  Exit Code 143 : Tiến trình bị hủy do Timeout hoặc Runner hủy (128 + SIGTERM = 128 + 15)          |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

| Phương Pháp Gỡ Rối | Kích Hoạt `CI_DEBUG_TRACE` | Interactive Web Terminal | Runner System Debug Logs | Local Execution (`gitlab-runner exec`) |
| :--- | :--- | :--- | :--- | :--- |
| **Cơ chế hoạt động** | `set -o xtrace` (in từng dòng lệnh và giá trị biến trước khi chạy) | Mở phiên WebSocket Web TTY kết nối trực tiếp vào Container | Giám sát `journalctl -u gitlab-runner` hoặc Docker Daemon events | Chạy giả lập Runner trực tiếp trên máy trạm lập trình viên |
| **Mức độ thâm nhập** | Xem chi tiết giá trị biến và lệnh shell | Thao tác tương tác trực tiếp (inspect filesystem, memory, network) | Quan sát hoạt động quản lý pod, spawn container, API call | Chạy thử nghiệm offline không cần push commit |
| **Rủi ro bảo mật** | **CỰC KỲ CAO**: Có thể để lộ Private Keys, Token, Passwords ra Job Log | **CAO**: Cần quyền Maintainer/Owner, cho phép truy cập shell container | **THẤP**: Chỉ lưu trữ trên máy chủ Runner Host | **AN TOÀN**: Mọi dữ liệu chỉ nằm trên máy trạm local |
| **Trường hợp áp dụng tốt nhất** | Debug logic shell script, kiểm tra biến môi trường bị rỗng | Debug lỗi build phức tạp không tái hiện được ở local | Debug lỗi kết nối Coordinator, lỗi disk full, lỗi Docker socket | Kiểm tra cú pháp YAML và logic build cơ bản |

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (Architecture Breakdown)

Mô hình kiến trúc giám sát và xử lý sự cố khẩn cấp cho hệ thống GitLab CI/CD:

```
+---------------------------------------------------------------------------------------------------+
|                            PRODUCTION TROUBLESHOOTING ARCHITECTURE                                |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +---------------------------+        +--------------------------------+                          |
|  | GitLab Web UI / Webhook   | -----> | Incident Response Bot (OpsGenie|                          |
|  | (Job Failed Event)        |        | / PagerDuty / Slack Webhook)   |                          |
|  +-------------+-------------+        +---------------+----------------+                          |
|                |                                      |                                           |
|                v                                      v                                           |
|  +---------------------------+        +--------------------------------+                          |
|  | Runner Manager            |        | Automated Diagnostic Script    |                          |
|  | - Metrics (Port 9252)     | -----> | - Check Node Memory / OOM Log  |                          |
|  | - Systemd Logs            |        | - Validate DNS / Proxy Egress  |                          |
|  +-------------+-------------+        | - Verify Job Token Whitelist   |                          |
|                |                      +--------------------------------+                          |
|                v                                                                                  |
|  +---------------------------+                                                                    |
|  | Target Job Container      | <===== [Developer / SRE via Interactive Web Terminal]             |
|  | (Live Debug Session)      |                                                                    |
|  +---------------------------+                                                                    |
+---------------------------------------------------------------------------------------------------+
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

### Sự cố thực tế: Toàn bộ pipeline triển khai Microservices đồng loạt tê liệt do lỗi "Job Token Permission Denied" và "Docker Daemon Out of Space"

```
[SỰ CỐ PIPELINE OUTAGE]
  |
  +---> 100% CI/CD Pipelines của 35 Microservices thất bại ở stage "Build & Security Scan".
  |
  +---(Why 1: Tại sao các jobs đồng loạt thất bại?)
  |   Một số jobs báo lỗi `x509: certificate signed by unknown authority`, một số khác báo `403 Forbidden` khi tải Shared CI Template, và runner báo `No space left on device`.
  |
  +---(Why 2: Tại sao tải Shared CI Template bị 403 Forbidden?)
  |   GitLab vừa nâng cấp phiên bản bảo mật, kích hoạt mặc định "Limit CI_JOB_TOKEN access", chặn các repo ngoài danh sách trắng.
  |
  +---(Why 3: Tại sao Runner bị No space left on device?)
  |   Hàng trăm container cũ và dangling docker images không được dọn dẹp sau khi build, làm đầy phân vùng `/var/lib/docker`.
  |
  +---(Why 4: Tại sao x509 Certificate verification failed?)
  |   Runner container sử dụng base image `alpine:latest` mới không chứa Corporate Root CA Certificate để kết nối internal Harbor Registry.
  |
  +---(Why 5: Gốc rễ vấn đề - Root Cause)
  |   Thiếu quy trình chuẩn hóa Base Runner Images (chưa nhúng Enterprise Root CA), không cấu hình Docker System Prune định kỳ trên Runner Node, và không cấu hình CI_JOB_TOKEN Allowlist cho Shared Templates Repo.
```

> [!CAUTION]
> **Biện pháp phòng ngừa chuẩn Production**:
> 1. Thiết lập Job Token Scope (Allowlist) rõ ràng cho tất cả Shared Infrastructure Repositories.
> 2. Triển khai DaemonSet / CronJob chạy `docker system prune -af --filter "until=24h"` mỗi 6 giờ trên tất cả Runner Hosts.
> 3. Chuẩn hóa Golden Runner Images chứa sẵn Corporate CA Certificates tại `/usr/local/share/ca-certificates/`.

---

## 5. Hands-on Lab: Khắc Phục Toàn Diện Các Kịch Bản Sự Cố CI/CD (8 Bước Chuẩn)

### Bước 1: Khởi Tạo Dự Án Mô Phỏng Môi Trường Lỗi

```bash
mkdir -p gitlab-troubleshooting-lab && cd gitlab-troubleshooting-lab
git init
git remote add origin http://gitlab.infra.internal/platform-team/troubleshooting-lab.git
```

Tạo file `.gitlab-ci.yml` chứa các kịch bản lỗi thực tế:

```yaml
# .gitlab-ci.yml
stages:
  - syntax_check
  - memory_heavy
  - network_test
  - auth_test

variables:
  DOCKER_DRIVER: overlay2

test_exit_code_127:
  stage: syntax_check
  image: alpine:3.20
  script:
    - echo "Testing missing binary..."
    - non_existing_command --flag
  allow_failure: true

test_oom_exit_137:
  stage: memory_heavy
  image: python:3.11-slim
  script:
    - python3 -c 'a = [0] * (1024 * 1024 * 500); print("Allocated 500M elements")'
  allow_failure: true

test_job_token_scope:
  stage: auth_test
  image: curlimages/curl:latest
  script:
    - 'curl --fail --header "JOB-TOKEN: $CI_JOB_TOKEN" "https://gitlab.infra.internal/api/v4/projects/platform%2Fshared-templates/repository/files/.gitlab-ci-base.yml/raw?ref=main"'
  allow_failure: true
```

> [!NOTE]
> **Checkpoint 1**: File `.gitlab-ci.yml` được cấu hình để kiểm thử có kiểm soát các kịch bản lỗi phổ biến.

---

### Bước 2: Kích Hoạt `CI_DEBUG_TRACE` & Kỹ Thuật Masking Bí Mật An Toàn

Để quan sát từng câu lệnh shell được thực thi mà không làm lộ Secret Keys:

```yaml
# Cập nhật job trong .gitlab-ci.yml
debug_inspection_job:
  stage: syntax_check
  image: alpine:3.20
  variables:
    CI_DEBUG_TRACE: "true"
    # MASK SECRET VARIABLES:
    SECRET_API_KEY: "super-confidential-token"
  script:
    - set +x # Tắt echo trước khi in biến nhạy cảm
    - echo "Masked secret length: ${#SECRET_API_KEY}"
    - set -x # Bật lại debug trace
    - ls -la /tmp
    - cat /etc/os-release
```

> [!NOTE]
> **Checkpoint 2**: Chạy pipeline và quan sát log. Mọi câu lệnh được tiền tố `+` hiển thị rõ ràng tham số, trong khi biến nhạy cảm được bảo vệ an toàn.

---

### Bước 3: Chẩn Đoán & Khắc Phục Lỗi Exit Code 137 (OOM Killer)

Khi Job chạy tác vụ tốn nhiều bộ nhớ và bị dừng đột ngột với thông báo:
`ERROR: Job failed: command terminated with exit code 137`

Kiểm tra Kernel OOM Messages trên Runner Host:
```bash
dmesg -T | grep -E -i "oom_reaper|out of memory|killed process"
```

Khắc phục bằng cách cấu hình giới hạn RAM và tối ưu hóa Node.js / Python memory flags:

```yaml
# Sửa lại job memory_heavy
test_oom_fixed:
  stage: memory_heavy
  image: node:20-alpine
  variables:
    # Tối ưu hóa V8 Heap Memory để không vượt quá giới hạn Container
    NODE_OPTIONS: "--max-old-space-size=1536"
  script:
    - echo "Running memory safe node process..."
    - node -e 'console.log("Memory limit configured:", process.env.NODE_OPTIONS)'
```

> [!NOTE]
> **Checkpoint 3**: Job chạy thành công với Exit code 0 mà không kích hoạt Linux OOM Killer.

---

### Bước 4: Xử Lý Triệt Để Lỗi SSL/TLS x509 Unknown Authority

Khi Runner tương tác với Internal Services và gặp lỗi:
`fatal: unable to access: SSL certificate problem: unable to get local issuer certificate`

Tạo script tự động cập nhật CA Certificate trong Job:

```yaml
# Cấu hình job kết nối HTTPS an toàn
secure_internal_fetch:
  stage: network_test
  image: alpine:3.20
  variables:
    INTERNAL_CA_PEM: "$CORPORATE_CA_CERT" # CI/CD Masked Variable
  before_script:
    - apk add --no-cache ca-certificates curl
    - echo "$INTERNAL_CA_PEM" > /usr/local/share/ca-certificates/corporate-ca.crt
    - update-ca-certificates
  script:
    - curl -s https://registry.infra.internal/v2/
```

> [!NOTE]
> **Checkpoint 4**: Lệnh `curl` xác thực TLS thành công qua Internal Root CA mà không cần sử dụng cờ không an toàn `--insecure` / `-k`.

---

### Bước 5: Cấu Hình CI_JOB_TOKEN Access Control (Inbound / Outbound Allowlist)

Khắc phục lỗi `403 Forbidden` khi truy cập Cross-Project Artifacts hoặc API.

Sử dụng GitLab REST API để thêm project gọi vào Allowlist của Target Project:

```bash
# Thêm Source Project ID (42) vào Allowlist của Target Template Project (100)
curl --request POST   --header "PRIVATE-TOKEN: glpat-admin-secret"   --header "Content-Type: application/json"   --data '{"target_project_id": 42}'   "https://gitlab.infra.internal/api/v4/projects/100/job_token_scope/allowlist"
```

Kiểm tra trạng thái Allowlist:
```bash
curl --header "PRIVATE-TOKEN: glpat-admin-secret"   "https://gitlab.infra.internal/api/v4/projects/100/job_token_scope/allowlist"
```

> [!NOTE]
> **Checkpoint 5**: API trả về danh sách liên kết thành công. Job sử dụng `$CI_JOB_TOKEN` có thể kéo template mượt mà.

---

### Bước 6: Kích Hoạt & Sử Dụng GitLab Interactive Web Terminal Để Debug Live

Mở file cấu hình Runner `/etc/gitlab-runner/config.toml` và kích hoạt Session Server:

```toml
# /etc/gitlab-runner/config.toml
[session_server]
  listen_address = "0.0.0.0:8093"
  advertise_address = "runner-host.infra.internal:8093"
  session_timeout = 1800
```

Khởi động lại Runner:
```bash
sudo systemctl restart gitlab-runner
```

Tạo job cho phép debug terminal:
```yaml
debug_live_session:
  stage: syntax_check
  image: ubuntu:24.04
  script:
    - echo "Waiting for engineer to inspect..."
    - sleep 600 # Giữ job để kỹ sư bấm nút "Debug" trên giao diện Web UI
  rules:
    - if: '$CI_COMMIT_BRANCH == "debug-fix"'
```

> [!NOTE]
> **Checkpoint 6**: Trên giao diện GitLab Job Log, xuất hiện nút **"Debug"** (Terminal icon). Bấm vào mở ra live bash shell bên trong container đang chạy.

---

### Bước 7: Tự Động Hóa Dọn Dẹp Đĩa Runner & Ngăn Ngừa Lỗi "No Space Left on Device"

Tạo script bảo trì tự động `runner-maintenance.sh` và thiết lập CronJob:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Starting Runner Maintenance ==="
# 1. Kiểm tra dung lượng phân vùng /var/lib/docker
DISK_USAGE=$(df /var/lib/docker | awk 'NR==2 {print $5}' | tr -d '%')
echo "Current Docker Disk Usage: ${DISK_USAGE}%"

if [ "$DISK_USAGE" -gt 80 ]; then
    echo "[WARNING] Disk usage above 80%! Pruning unused docker objects..."
    docker system prune -af --volumes --filter "until=12h"
    docker builder prune -af --filter "until=12h"
fi

# 2. Dọn dẹp Runner Build Directories mồ côi
find /home/gitlab-runner/builds -maxdepth 2 -type d -mtime +7 -exec rm -rf {} + 2>/dev/null || true

echo "=== Maintenance Completed Successfully ==="
```

Cấp quyền thực thi và test thử nghiệm:
```bash
chmod +x runner-maintenance.sh && ./runner-maintenance.sh
```

> [!NOTE]
> **Checkpoint 7**: Script dọn dẹp toàn bộ dangling images và temporary build directories, giải phóng ngay lập tức hàng chục GB dung lượng đĩa.

---

### Bước 8: Kiểm Thử Toàn Diện Bộ Kịch Bản Tự Phục Hồi (Self-Healing Validation)

Tạo test script tổng hợp để xác nhận toàn bộ hệ sinh thái CI/CD đã ổn định:

```bash
# test-health.sh
#!/usr/bin/env bash
set -e

echo "1. Checking GitLab Runner Status..."
gitlab-runner status

echo "2. Checking Docker Daemon Socket Permissions..."
docker info >/dev/null && echo "[OK] Docker socket accessible"

echo "3. Validating DNS & Egress Connectivity..."
curl -s --connect-timeout 5 https://gitlab.infra.internal/ >/dev/null && echo "[OK] GitLab Coordinator reachable"

echo "=== ALL CHECKS PASSED: RUNNER READY FOR PRODUCTION ==="
```

Chạy script kiểm tra:
```bash
./test-health.sh
```

> [!NOTE]
> **Checkpoint 8**: Tất cả 3 tiêu chí kiểm tra cốt lõi đều trả về `[OK]`, xác nhận hạ tầng Runner vận hành ở trạng thái tối ưu.

---

## 6. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span class="qa-title-text">Khi một CI Job thất bại với mã lỗi "Exit Code 137", nguyên nhân gốc rễ là gì và bạn tiến hành xử lý như thế nào?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Nguyên nhân gốc rễ</strong>: Exit code 137 = $128 + 9$ (Signal 9 - <code>SIGKILL</code>). Điều này có nghĩa tiến trình bị hệ điều hành (Linux Kernel OOM Killer) tiêu diệt cưỡng chế do sử dụng vượt quá giới hạn RAM được cấp phát cho Container (hoặc máy chủ hết RAM vật lý).</p>
    <p><strong>Quy trình xử lý</strong>:</p>
    <ul>
      <li>Kiểm tra log kernel: <code>dmesg -T | grep -i oom</code> trên máy chủ Runner.</li>
      <li>Tăng giới hạn <code>memory_limit</code> trong cấu hình Runner hoặc Kubernetes Pod limits.</li>
      <li>Tối ưu hóa ứng dụng: Cấu hình giới hạn bộ nhớ runtime (như <code>NODE_OPTIONS="--max-old-space-size=..."</code> hoặc Maven <code>-Xmx</code>), tránh memory leak trong unit test.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span class="qa-title-text">Exit code 143 khác gì so với Exit code 137 và những tình huống nào kích hoạt lỗi này?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Exit code 143</strong> = $128 + 15$ (Signal 15 - <code>SIGTERM</code>). Khác với SIGKILL (cưỡng chế chết ngay lập tức), SIGTERM là tín hiệu yêu cầu dừng tiến trình một cách êm thuận (graceful shutdown).</p>
    <p><strong>Tình huống kích hoạt</strong>:</p>
    <ul>
      <li>Job vượt quá giới hạn thời gian chạy cho phép (Job Timeout configured trong <code>.gitlab-ci.yml</code> hoặc Project Settings).</li>
      <li>Người dùng bấm nút "Cancel" hủy Pipeline trên giao diện GitLab.</li>
      <li>Cơ chế <code>interruptible: true</code> tự động hủy job cũ khi có commit mới được đẩy lên.</li>
      <li>Kubernetes Node drain / Spot Instance termination notification.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span class="qa-title-text">Lỗi "x509: certificate signed by unknown authority" xảy ra ở giai đoạn nào và phương án khắc phục an toàn nhất là gì?</span>
  </summary>
  <div class="qa-body">
    <p>Lỗi này xảy ra ở giai đoạn <strong>Pre-Clone</strong> hoặc <strong>Helper Image</strong> khi Runner cố gắng kết nối HTTPS với GitLab Server hoặc Container Registry nội bộ sử dụng chứng chỉ SSL tự ký (Self-signed) hoặc Corporate Private CA.</p>
    <p><strong>Phương án khắc phục an toàn</strong>: Mount Root CA Certificate của tổ chức vào Runner Container qua file cấu hình <code>config.toml</code> (mục <code>tls-ca-file</code>) hoặc cập nhật vào <code>/etc/ssl/certs/ca-certificates.crt</code> trong Base Image. <strong>Tuyệt đối không</strong> sử dụng các cờ bỏ qua kiểm tra SSL (<code>tls_verify = false</code> hoặc <code>git config --global http.sslVerify false</code>) trong môi trường Production.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span class="qa-title-text">Khi nào nên bật `CI_DEBUG_TRACE: "true"` và rủi ro bảo mật tiềm ẩn của biến này là gì?</span>
  </summary>
  <div class="qa-body">
    <p><code>CI_DEBUG_TRACE</code> kích hoạt chế độ shell tracing (<code>set -o xtrace</code>), in ra chi tiết từng dòng script và giá trị của tất cả các biến môi trường trước khi thực thi lệnh.</p>
    <p><strong>Rủi ro bảo mật</strong>: Các giá trị Secret Variables (như Database Passwords, Private Deploy Keys, API Tokens) có thể bị giải phóng thành văn bản thuần (plaintext) và in trực tiếp vào Job Log công khai, tạo nguy cơ lộ lọt dữ liệu nghiêm trọng.</p>
    <p><strong>Khuyến nghị</strong>: Chỉ bật trên nhánh phát triển cá nhân (debug branch) và lập tức tắt đi sau khi xác định xong nguyên nhân lỗi.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span class="qa-title-text">Interactive Web Terminal trong GitLab CI/CD hoạt động ra sao và cần những điều kiện gì để kích hoạt?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Cơ chế</strong>: GitLab Runner mở một WebSocket Server (gọi là Session Server). Khi kỹ sư bấm nút "Debug" trên Web UI, trình duyệt kết nối qua WebSocket tới Session Server, mở ra phiên interactive shell trực tiếp bên trong Container của Job đang chạy.</p>
    <p><strong>Điều kiện cần thiết</strong>:</p>
    <ul>
      <li>Cấu hình <code>[session_server]</code> trong <code>config.toml</code> của Runner với địa chỉ mạng hợp lệ và mở port (mặc định 8093).</li>
      <li>Job phải đang ở trạng thái chạy (running) và chưa kết thúc.</li>
      <li>Kỹ sư thực hiện phải có quyền Maintainer hoặc Owner trên dự án.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span class="qa-title-text">Giải thích cơ chế bảo mật "CI_JOB_TOKEN Scope" và cách xử lý lỗi HTTP 403 khi kéo Package/Template từ dự án khác?</span>
  </summary>
  <div class="qa-body">
    <p>Mặc định từ các phiên bản GitLab hiện đại, tính năng <strong>Limit CI_JOB_TOKEN access</strong> được kích hoạt để ngăn chặn rò rỉ token truy cập chéo dự án bất hợp pháp. Một Job Token chỉ có thể gọi API của dự án sở hữu nó.</p>
    <p><strong>Cách xử lý lỗi 403</strong>: Trên dự án đích (Target Project chứa Template hoặc Package), truy cập <em>Settings $ightarrow$ CI/CD $ightarrow$ Token Access</em>, sau đó thêm đường dẫn của Dự án nguồn (Source Project) vào <strong>Allowlist</strong> (hoặc gọi API <code>/projects/:id/job_token_scope/allowlist</code>).</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span class="qa-title-text">Lỗi "No space left on device" trên Runner Host thường do những thành phần nào gây ra và giải pháp tự động dọn dẹp là gì?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Các thủ phạm chính</strong>:</p>
    <ul>
      <li>Dangling Docker Images và unused build cache trong <code>/var/lib/docker</code>.</li>
      <li>Thư mục build tạm của Runner <code>/home/gitlab-runner/builds/</code> chứa source code của các job cũ.</li>
      <li>Dung lượng Job Logs và Cache lưu trữ cục bộ.</li>
    </ul>
    <p><strong>Giải pháp</strong>: Thiết lập CronJob chạy <code>docker system prune -af --filter "until=24h"</code>, cấu hình <code>clear-docker-cache</code> utility của GitLab Runner, và định kỳ kiểm tra cảnh báo dung lượng đĩa qua Prometheus Node Exporter.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span class="qa-title-text">Tại sao một Job bị kẹt vô tận ở trạng thái "Pending" và những bước đầu tiên bạn sẽ kiểm tra là gì?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Các bước kiểm tra đầu tiên</strong>:</p>
    <ol>
      <li><strong>Tags Matching</strong>: Kiểm tra xem Job có yêu cầu <code>tags: [docker, gpu]</code> mà không có bất kỳ Runner nào mang tag tương ứng đang online hay không.</li>
      <li><strong>Untagged Runners Setting</strong>: Nếu job không có tag, kiểm tra xem các Runner có bật tùy chọn <em>"Run untagged jobs"</em> hay không.</li>
      <li><strong>Runner Status & Connectivity</strong>: Kiểm tra trên trang Admin/CI Settings xem Runner có trạng thái màu xanh (Online) hay đỏ (Contacted X hours ago).</li>
      <li><strong>Runner Concurrency</strong>: Kiểm tra xem Runner đã đạt ngưỡng <code>concurrent</code> tối đa và tất cả slot đang bị chiếm giữ bởi các jobs khác hay không.</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span class="qa-title-text">Sự khác biệt giữa lỗi "Command not found (Exit code 127)" và lỗi "Permission denied (Exit code 126)" trong môi trường Docker Container?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Exit code 127 (Command not found)</strong>: Hệ điều hành không thể tìm thấy file thực thi trong các đường dẫn của biến <code>$PATH</code> (hoặc file thực thi phụ thuộc vào dynamic linker không tương thích, ví dụ: chạy binary biên dịch với <code>glibc</code> trên image Alpine dùng <code>musl</code>).</p>
    <p><strong>Exit code 126 (Permission denied)</strong>: File thực thi tồn tại trong đường dẫn nhưng tiến trình (User UID hiện tại trong Container) không có quyền thực thi (<code>chmod +x</code>) hoặc hệ thống file được mount với cờ <code>noexec</code>.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span class="qa-title-text">Làm thế nào để xử lý sự cố Cache Corrupted khiến Job liên tục build thất bại dù mã nguồn không thay đổi?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Cách xử lý nhanh</strong>:</p>
    <ul>
      <li>Thay đổi giá trị <code>key</code> của cache trong <code>.gitlab-ci.yml</code> (ví dụ: thêm version suffix <code>cache-key-v2</code> hoặc sử dụng <code>key: { files: [package-lock.json] }</code>).</li>
      <li>Bấm nút <strong>"Clear runner caches"</strong> trên giao diện GitLab Pipelines UI.</li>
      <li>Nếu dùng S3/MinIO Distributed Cache, xóa trực tiếp file nén <code>.zip</code> của key bị lỗi trên bucket lưu trữ.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q11</span>
    <span class="qa-title-text">Khi nào nên sử dụng `gitlab-runner exec` để kiểm tra lỗi local và hạn chế của công cụ này là gì?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Khi nên dùng</strong>: Dùng để nhanh chóng kiểm tra cú pháp lệnh <code>script</code>, kiểm tra sự tương thích của base docker image mà không cần thực hiện commit/push lên máy chủ GitLab.</p>
    <p><strong>Hạn chế lớn</strong>:</p>
    <ul>
      <li>Không hỗ trợ tải/lưu Artifacts hoặc tương tác với GitLab Server API.</li>
      <li>Không hỗ trợ tính năng DAG (<code>needs:</code>), child/parent pipelines, hoặc các biến môi trường được quản lý tập trung trên GitLab UI.</li>
      <li>Tính năng <code>exec</code> đã bị GitLab thông báo deprecated và dần thay thế bởi các công cụ kiểm thử cục bộ hiện đại.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q12</span>
    <span class="qa-title-text">Xây dựng quy trình phản ứng sự cố (Incident Response Protocol) chuẩn khi toàn bộ hệ thống CI/CD ngừng hoạt động?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Quy trình 5 bước phản ứng sự cố SRE/DevOps</strong>:</p>
    <ol>
      <li><strong>Triage & Cảnh báo (Triage & Alert)</strong>: Gửi thông báo sự cố lên kênh Slack/Teams nội bộ, mở Incident ticket trên PagerDuty.</li>
      <li><strong>Cô lập sự cố (Containment)</strong>: Xác định phạm vi ảnh hưởng (do GitLab Coordinator, Runner Network hay Storage S3). Tạm dừng các Scheduled pipelines không quan trọng.</li>
      <li><strong>Khôi phục khẩn cấp (Remediation)</strong>: Khởi động lại Runner Service, dọn dẹp dung lượng đĩa, hoặc chuyển hướng lưu lượng sang Backup Runner Pool.</li>
      <li><strong>Kiểm tra xác nhận (Verification)</strong>: Chạy Canary Pipeline kiểm thử toàn bộ các stage từ build đến deploy.</li>
      <li><strong>Hậu kiểm sự cố (Post-Mortem / PIR)</strong>: Phân tích 5-Whys tìm nguyên nhân gốc rễ, bổ sung cảnh báo Prometheus và cập nhật tài liệu Runbook.</li>
    </ol>
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

```
+---------------------------------------------------------------------------------------------------+
|                                      BÀI 47 - TỔNG KẾT KIẾN THỨC                                  |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  1. PHƯƠNG PHÁP LUẬN CHẨN ĐOÁN SỰ CỐ                                                              |
|     +-- 6 Giai đoạn vòng đời Job: Cô lập chính xác Failure Domain                                 |
|     +-- Phân tích Root Cause bằng ma trận 5-Whys                                                  |
|                                                                                                   |
|  2. GIẢI MÃ TOÀN BỘ LINUX EXIT CODES                                                              |
|     +-- Exit 137 (OOM Killer): Kiểm soát memory limit & kernel logs                               |
|     +-- Exit 143 (SIGTERM): Xử lý Timeout, Cancellation & Spot Drain                              |
|     +-- Exit 127/126: Phân giải PATH, glibc/musl binary & phân quyền thực thi                     |
|                                                                                                   |
|  3. CÔNG CỤ GỠ RỐI CHUYÊN SÂU                                                                     |
|     +-- CI_DEBUG_TRACE: Quan sát execution trace với quy tắc Masking Secret                       |
|     +-- Interactive Web Terminal: Thâm nhập trực tiếp vào Container bằng Live TTY                 |
|     +-- Quản trị Job Token Scope Allowlist & Corporate CA Certificates                           |
+---------------------------------------------------------------------------------------------------+
```

> [!TIP]
> **Bài học tiếp theo**: Bạn đã tích lũy đầy đủ toàn bộ kiến thức từ nền tảng cú pháp, tối ưu hóa đa ngôn ngữ, đóng gói container, an ninh DevSecOps đến phân phối đa đám mây và khắc phục sự cố. Giờ là lúc ghép nối tất cả thành một kiệt tác kỹ thuật hoàn chỉnh trong **[Bài 48: Đồ Án Tốt Nghiệp: Xây Dựng Hệ Thống CI/CD & DevSecOps Toàn Diện Cho Doanh Nghiệp (Capstone Enterprise Production Pipeline)](gitlab-48-48-capstone-project.html)**.
{% endraw %}
