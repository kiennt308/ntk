---
layout: post
title: "[Bài 47] Phẫu Thuật Sự Cố Pipeline Thực Chiến: Xử Lý Kẹt Job, Timeout, Runner OOMKilled, Network Glitch & Registry Rate Limit"
date: 2026-07-29 08:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-47
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 47
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.47] Hướng dẫn chuyên sâu Phẫu Thuật Sự Cố Pipeline Thực Chiến: Xử Lý Kẹt Job, Timeout, Runner OOMKilled, Network Glitch & Registry Rate Limit: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

# [BÀI 47] PHẪU THUẬT SỰ CỐ PIPELINE THỰC CHIẾN: XỬ LÝ KẸT JOB, TIMEOUT, RUNNER OOMKILLED, NETWORK GLITCH & REGISTRY RATE LIMIT

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

| STT | Câu hỏi ôn tập Buổi 46 | Đáp án vắn tắt |
|---|---|---|
| 1 | Bốn chỉ số DORA Metrics tiêu chuẩn quốc tế là gì? | Deployment Frequency (DF), Lead Time for Changes (LTC), Change Failure Rate (CFR), Time to Restore Service (MTTR). |
| 2 | Mục tiêu chỉ số Lead Time for Changes (LTC) của nhóm Elite Performer là bao nhiêu? | LTC dưới 1 giờ từ khi commit code đến khi chạy ổn định trên môi trường Production. |
| 3 | Tác dụng của cờ `interruptible = true` trong tệp `.gitlab-ci.yml` là gì? | Tự động hủy các pipeline cũ khi có commit mới push vào cùng Merge Request, tiết kiệm 40% phút runner. |
| 4 | Làm thế nào để ngăn chặn thảm họa cháy ngân sách điện toán Runner do job bị treo vô hạn? | Cài đặt `shared_runners_minutes_limit` cấp Group và cờ `timeout: 15m` cho mọi jobs CI. |
| 5 | Tỷ lệ giảm chi phí điện toán khi dùng AWS Spot Instances cho Kubernetes Runner Node là bao nhiêu? | Giảm từ 70% đến 80% chi phí điện toán so với việc thuê máy chủ On-Demand Instances cố định. |



Trong Buổi 46, chúng ta đã nắm vững phương pháp đo lường hiệu năng sản xuất phần mềm qua DORA Metrics và tối ưu chi phí hạ tầng CI/CD. Tuy nhiên, khi quy mô hạ tầng mở rộng lên hàng trăm microservices và hàng ngàn pipeline chạy song song mỗi ngày, đội ngũ DevOps/SRE sẽ liên tục đối mặt với những sự cố phức tạp: job bị treo không phàn nàn, lỗi Out of Memory (OOM Exit Code 137), nghẽn mạng DNS/TLS, hỏng cache (Cache Poisoning), hỏng Docker-in-Docker TLS certificates, hoặc lỗi phân quyền Permission Denied bí ẩn.

**Luận đề trung tâm:** *Debugging CI/CD không bao giờ dựa vào đoán mò hay thử nghiệm may rủi. Một Kỹ sư SRE chuyên nghiệp giải quyết sự cố dựa trên phân tích thực nghiệm (Empirical Log Analysis), kích hoạt `CI_DEBUG_TRACE`, soi cgroup OOM logs qua `dmesg`, trace system calls qua `strace`, và kiểm tra trạng thái mạng của Runner Node.*

```mermaid
graph TD
    A["Sự cố Pipeline CI/CD"] --> B{"Phân loại Triệu chứng"}
    B -->|"Pipeline bị treo / Stuck"| C["Kiểm tra STDOUT Pipe & Timeout (buổi 47 QT 47.8, buổi 46 QT 46.9)"]
    B -->|"Script bị Kill đột ngột (Exit 137)"| D["Soi OOM Killer & Cgroup Limit (buổi 47 QT 47.2)"]
    B -->|"Lỗi Mạng / TLS / DNS Timeout"| E["Soi DNS Dig & MTU Packet Mismatch (buổi 47 QT 47.3)"]
    B -->|"Lỗi Docker-in-Docker TLS"| F["Cấu hình DOCKER_TLS_CERTDIR (buổi 47 QT 47.6)"]
    B -->|"Lỗi Bí ẩn / Command Fail"| G["Kích hoạt CI_DEBUG_TRACE = true (buổi 47 QT 47.1)"]
    C --> H["Giải quyết sự cố dựa trên Empirical Evidence"]
    D --> H
    E --> H
    F --> H
    G --> H
```

---



1. **Kích hoạt và phân tích `CI_DEBUG_TRACE`** ở cấp độ dòng lệnh shell để phát hiện chính xác câu lệnh gây ra lỗi ngầm.
2. **Chẩn đoán triệt để sự cố Out of Memory (Exit Code 137)** bằng cách đọc `dmesg` logs và điều chỉnh memory limit của cgroups.
3. **Sửa các lỗi mạng phức tạp trong Container** (DNS failure, TLS handshake timeout, MTU packet truncation).
4. **Xử lý sự cố Cache Poisoning** và xung đột quyền hạn UID/GID trong Docker Executor.
5. **Live debugging trực tiếp trên Runner Container** đang chạy bằng `tmate` SSH terminal.
6. **Khắc phục triệt để lỗi Docker-in-Docker TLS Certificate Verification Failed**.
7. **Truy vết system calls bằng `strace -f`** để tìm root cause khi ứng dụng bị crash hoặc đơ không xuất log.

---



- **Kiến thức Buổi 02 & Buổi 44:** Cơ chế thực thi của GitLab Runner Executor (Docker Executor, Kubernetes Executor - buổi 02 QT 2.1, buổi 44 QT 44.1).
- **Kiến thức Buổi 06:** Cơ chế quản lý biến môi trường và Masked/Protected Variables (buổi 06 QT 6.1).
- **Kỹ năng Linux nâng cao:** Thành thạo các lệnh Linux cơ bản: `curl`, `dig`, `iptables`, `dmesg`, `strace`, `chmod`, `chown`, `ps`, `kill`.

---



| Thuật ngữ | Khái niệm chuẩn SRE | Ý nghĩa thực tiễn |
|---|---|---|
| **CI_DEBUG_TRACE** | Cờ cấu hình bật chế độ `set -x` shell tracing sâu trong GitLab Runner Engine | In ra từng dòng lệnh shell chi tiết kèm giá trị biến đã expand |
| **Exit Code 137** | Mã thoát của tiến trình bị Linux Kernel OOM Killer tiêu diệt (128 + SIGKILL 9) | Dấu hiệu 100% cho biết container bị thiếu RAM (Out of Memory) |
| **Cache Poisoning** | Hiện tượng cache bị ghi đè bởi file hỏng hoặc độc hại từ một job lỗi trước đó | Làm cho tất cả các pipeline sau bị thất bại dây chuyền |
| **Hanging Job** | Công việc bị treo vô tận do tiến trình con ngầm giữ stdout/stderr pipes mở | Khiến Runner bị ngắt kết nối hoặc hết timeout lãng phí tài nguyên |
| **MTU Mismatch** | Sự không đồng nhất về Maximum Transmission Unit giữa Docker Network và Host Interface | Gây ra hiện tượng gói tin lớn bị ngắt, dẫn đến TLS Handshake Freeze |
| **Interactive Terminal** | Khả năng mở phiên SSH/Shell tương tác trực tiếp vào Runner Container đang thực thi | Cho phép thao tác lệnh live debug ngay trên môi trường CI |

---

### 1.1. Quy tắc Troubleshooting Log & Memory Errors (15 phút)

**Nguyên lý cốt lõi:** Kích hoạt `CI_DEBUG_TRACE = "true"` trong tệp `.gitlab-ci.yml` để soi toàn bộ shell execution trace của Runner ở cấp độ dòng lệnh.
**Phát biểu.** Khai báo biến `CI_DEBUG_TRACE: "true"` trong khối `variables:` của job hoặc pipeline để bật chế độ verbose shell tracing (`set -x`).
**Giải thích cơ chế ngầm:** Mặc định GitLab Runner chỉ hiển thị đầu ra STDOUT/STDERR của câu lệnh chính. Nếu sự cố xảy ra trong các script tiền xử lý ngầm (Pre-build script, Git fetch, Artifact download, Docker login), log thông thường sẽ không thể hiện nguyên nhân. Bật `CI_DEBUG_TRACE` giúp in ra chi tiết từng bước thực thi nội bộ của Runner Engine, bao gồm cả việc khởi tạo container, mount volume, tải helper script và expand biến môi trường. Điều này loại bỏ hoàn toàn việc đoán mò nguyên nhân lỗi. Khi bật cờ này, Runner Script Generator sẽ tự động chèn cờ `set -o xtrace` hoặc `set -x` vào đầu mọi script thực thi shell, giúp hiển thị chi tiết từng giá trị biến môi trường được thay thế và từng nhánh rẽ câu lệnh `if/else`.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ngồi đoán mò nguyên nhân lỗi khi log hiển thị thông báo chung chung `Command exited with code 1` mà không biết câu lệnh nào bị thất bại.
**Minh hoạ.** Khai báo `variables: { CI_DEBUG_TRACE: "true" }` ở đầu tệp `.gitlab-ci.yml`. Log đầu ra chi tiết sẽ thể hiện từng câu lệnh `+ export VAR=val` giúp SRE phát hiện biến bị thiếu hoặc lệnh shell bị lỗi cú pháp.
```bash
# Đầu ra minh họa của CI_DEBUG_TRACE log
+ export CI_BUILD_REF=a1b2c3d4
+ echo 'Starting build phase...'
Starting build phase...
+ docker login -u gitlab-ci-token -p '[MASKED]' registry.company.internal
Error response from daemon: Get "https://registry.company.internal/v2/": net/http: request canceled while waiting for connection
```
**Con số chốt:** 100% Các ca debugging lỗi bí ẩn phải bật `CI_DEBUG_TRACE`.

---

**Nguyên lý cốt lõi:** Chẩn đoán sự cố Out of Memory (OOM Exit Code 137) bằng cách đọc `dmesg` logs và phân bổ tài nguyên cgroup memory limits hợp lý.
**Phát biểu.** Khi một job thất bại với mã `Exit Code 137`, lập tức kiểm tra `dmesg -T | grep -i oom` hoặc `kubectl describe pod` để xác nhận Linux Kernel OOM Killer đã tiêu diệt tiến trình.
**Giải thích cơ chế ngầm:** Mã thoát 137 xuất phát từ công thức $128 + 9$ (SIGKILL signal 9). Điều này khẳng định tiến trình bên trong container đã tiêu tốn vượt quá mức RAM được cấp phát (Cgroup Memory Limit). Đội ngũ DevOps không được sửa nhầm code ứng dụng mà phải tăng `memory_limit` trong cấu hình `config.toml` của Runner (buổi 02 QT 2.2) hoặc tối ưu tham số heap size của ngôn ngữ (ví dụ `-Xmx` trong Java hoặc `--max-old-space-size` trong Node.js). Khi Linux Kernel phát hiện một cgroup tiêu thụ RAM vượt hạn mức cấu hình, nó sẽ chọn tiến trình có `oom_score` cao nhất bên trong cgroup đó để gửi tín hiệu `SIGKILL` (signal 9) lập tức.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Sửa code logic ứng dụng khi gặp lỗi Exit 137 thay vì kiểm tra hạn mức RAM của container.
**Minh hoạ.** Cấu hình `memory_limit = "4g"` cho Docker Executor trong tệp `config.toml`. Kiểm tra log Kernel: `dmesg -T | grep -E "Out of memory|Killed process"`. Kết quả sẽ in ra dạng `Memory cgroup out of memory: Killed process 4120 (java) total-vm:894244kB, anon-rss:512000kB`.
```ini
# Cấu hình tăng Cgroup Memory Limit trong /etc/gitlab-runner/config.toml
[runners.docker]
  image = "alpine:latest"
  memory = "4g"
  memory_swap = "4g"
  memory_reservation = "2g"
```
**Con số chốt:** Exit Code 137 = 100% Lỗi OOM Container RAM.

---

**Nguyên lý cốt lõi:** Chẩn đoán và khắc phục sự cố DNS Resolution Failure và TLS Handshake Freeze trong Container bằng `dig` và điều chỉnh MTU packet size.
**Phát biểu.** Sử dụng lệnh `curl -vvv` kết hợp `dig +trace` để phát hiện nghẽn mạng; đặt tham số MTU `ff_network_per_build` hoặc `docker network` khớp với card mạng Host (thường là 1450 trên AWS VPC hoặc 1500 trên Bare-metal).
**Giải thích cơ chế ngầm:** Lỗi mạng trong Runner container thường có 2 nguyên nhân cốt lõi: (1) Container DNS server bị đứt kết nối với DNS nội bộ công ty, (2) MTU size của Docker virtual bridge lớn hơn MTU của card mạng Host/Cloud VPC (như AWS VXLAN MTU 1450), khiến các gói tin TLS Certificate khổng lồ bị trảm (drop) âm thầm làm pipeline treo ở bước Handshake! Khi một gói tin TCP có kích thước IP Payload lớn hơn MTU của đường truyền vật lý, nếu cờ `DF (Don't Fragment)` được bật trong kết nối TLS, router trung gian sẽ trảm bỏ gói tin đó mà không phản hồi ICMP, khiến client đứng chờ vô hạn.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thay đổi mã nguồn ứng dụng khi pipeline bị kẹt ở dòng `TLS handshake starting...`.
**Minh hoạ.** Đặt `[runners.docker]` tham số `mtu = 1450` trong tệp `config.toml`. Kiểm tra mạng: `curl -vvv https://registry.company.internal/v2/`.
```ini
# Cấu hình MTU đúng cho Docker Network Bridge trong config.toml
[runners.docker]
  network_mode = "bridge"
  dns = ["10.0.0.2", "8.8.8.8"]
  mtu = 1450
```
**Con số chốt:** Đặt MTU Docker = 1450 trên hạ tầng Cloud VPC.

---

**Nguyên lý cốt lõi:** Ngăn ngừa và xử lý sự cố Cache Poisoning bằng chiến lược Cache Key Versioning và cấm dùng chung cache giữa các nhánh không tin cậy.
**Phát biểu.** Đặt `key: ${CI_COMMIT_REF_SLUG}-v1` hoặc `key: files: - package-lock.json` cho cấu hình cache trong `.gitlab-ci.yml` (buổi 05 QT 5.1).
**Giải thích cơ chế ngầm:** Cache Poisoning xảy ra khi một job chạy trên nhánh feature đẩy một tập tin cache bị hỏng hoặc chứa mã độc lên S3/MinIO. Các pipeline chạy sau trên nhánh `main` tải cache này về sẽ bị thất bại liên tục (Poisoned). Đổi tên key version (tăng lên `-v2`) hoặc tách biệt cache key theo nhánh sẽ loại bỏ lập tức cache hỏng mà không cần xóa thủ công trên server. Ngoài ra, cần thiết lập `policy: pull` trên các job kiểm thử nhánh phụ để ngăn không cho nhánh phụ ghi đè cache lên kho lưu trữ chung.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dùng cố định một `key: "global-cache"` chung cho tất cả mọi nhánh và mọi môi trường.
**Minh hoạ.** Khai báo `cache: { key: "$CI_COMMIT_REF_SLUG-v2", paths: ["node_modules/"] }`.
```yaml
# Cấu hình Cache an toàn chống Cache Poisoning
default:
  cache:
    key: "${CI_COMMIT_REF_SLUG}-v2"
    paths:
      - node_modules/
      - .npm/
    policy: pull-push

feature_job:
  cache:
    key: "${CI_COMMIT_REF_SLUG}-v2"
    policy: pull  # Nhánh phụ chỉ đọc cache, không ghi đè
```
**Con số chốt:** Tăng Cache Version Key ngay khi phát hiện suy thoái dữ liệu cache.

---

### 1.2. Quy tắc Live Debugging & Container Network (15 phút)

**Nguyên lý cốt lõi:** Sử dụng công cụ `tmate` hoặc GitLab Interactive Web Terminal để mở phiên SSH trực tiếp vào container đang chạy để live debug.
**Phát biểu.** Tích hợp bước job `tmate` trong `.gitlab-ci.yml` khi pipeline gặp sự cố để giữ container sống và lấy đường dẫn kết nối SSH/Web Terminal.
**Giải thích cơ chế ngầm:** Nhiều lỗi chỉ xuất hiện duy nhất trên môi trường Runner CI mà không thể tái hiện ở máy local (Local Dev Machine). Việc mở phiên tương tác trực tiếp giúp SRE kiểm tra trực tiếp hệ thống tệp, biến môi trường, quyền truy cập mạng và tái hiện lệnh lỗi theo thời gian thực mà không cần push commit thử nghiệm liên tục. SRE có thể sử dụng các công cụ chẩn đoán như `gdb`, `strace`, `tcpdump` trực tiếp bên trong container để bắt lỗi tại chỗ.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Push hàng chục commit rác với thông điệp `fix log 1`, `fix log 2` chỉ để in thêm vài dòng log.
**Minh hoạ.** Tích hợp job debug: `script: - curl -s https://tmate.io | bash` để tạo SSH session. Đọc URL SSH từ console output và truy cập trực tiếp bằng `ssh user@tmate.io`.
```yaml
# Job mẫu kích hoạt phiên Tmate Live Debugging
debug_job:
  stage: test
  script:
    - apt-get update && apt-get install -y tmate openssh-client
    - tmate -F -S /tmp/tmate.sock new-session -d
    - tmate -S /tmp/tmate.sock wait tmate-ready
    - tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'
    - sleep 1800  # Giữ container mở trong 30 phút để SSH debug
  when: on_failure
```
**Con số chốt:** Giảm 90% số lượng commit rác nhờ Live Terminal Debugging.

---

**Nguyên lý cốt lõi:** Cấu hình `DOCKER_TLS_CERTDIR = "/certs"` để sửa dứt điểm lỗi Docker-in-Docker (DinD) TLS Certificate Verification Failed.
**Phát biểu.** Khai báo biến `DOCKER_TLS_CERTDIR: "/certs"` và mount volume chung `/certs/client` khi chạy Docker-in-Docker service.
**Giải thích cơ chế ngầm:** Từ Docker version 19.03+, Docker Daemon yêu cầu kết nối an toàn qua TLS mặc định. Nếu không cấu hình đường dẫn chứng chỉ TLS dùng chung giữa container Client và container Service DinD, lệnh `docker build` sẽ bị từ chối kết nối với lỗi `Cannot connect to the Docker daemon at tcp://docker:2376. Is the docker daemon running?`. Cấu hình đúng `DOCKER_TLS_CERTDIR` tự động tạo cặp chứng chỉ x509 trong thư mục `/certs/client` và chia sẻ cho cả client lẫn daemon engine.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bỏ cờ TLS và dùng `DOCKER_HOST: tcp://docker:2375` không mã hóa gây nguy cơ bảo mật.
**Minh hoạ.** Khai báo `variables: { DOCKER_TLS_CERTDIR: "/certs", DOCKER_HOST: "tcp://docker:2376" }` và service `services: [{ name: "docker:24.0.5-dind" }]`.
```yaml
# Cấu hình Docker-in-Docker (DinD) TLS chuẩn mực
build_image:
  image: docker:24.0.5
  services:
    - name: docker:24.0.5-dind
      alias: docker
  variables:
    DOCKER_HOST: "tcp://docker:2376"
    DOCKER_TLS_CERTDIR: "/certs"
    DOCKER_TLS_VERIFY: 1
    DOCKER_CERT_PATH: "$DOCKER_TLS_CERTDIR/client"
  script:
    - docker build -t my-app:$CI_COMMIT_SHA .
```
**Con số chốt:** 100% Pipelines DinD chuẩn mực phải bật TLS với `DOCKER_TLS_CERTDIR = "/certs"`.

---

**Nguyên lý cốt lõi:** Xử lý lỗi Permission Denied trong Docker Executor bằng cách đồng bộ UID/GID giữa Host Runner và Container Non-Root User.
**Phát biểu.** Truyền tham số `user: "${UID}:${GID}"` hoặc điều chỉnh quyền hạn thư mục làm việc `/builds` bằng `chmod/chown` trong entrypoint.
**Giải thích cơ chế ngầm:** Mặc định GitLab Runner tạo thư mục build với quyền của Root hoặc UID 1000. Nếu container image được thiết kế chạy với user bảo mật non-root (ví dụ UID 10001), container sẽ không có quyền ghi dữ liệu vào thư mục làm việc, dẫn đến lỗi `Permission denied` khi ghi log hoặc artifact. Đồng bộ UID/GID đảm bảo rằng tiến trình bên trong container sở hữu đúng danh tính Linux User có quyền đọc ghi trên tệp.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Sử dụng lệnh `chmod -R 777 /` bừa bãi gây thủng lỗ hổng bảo mật nghiêm trọng trên hạ tầng.
**Minh hoạ.** Cấu hình `chown -R appuser:appuser $CI_PROJECT_DIR` trong script khởi tạo container entrypoint.
```yaml
# Sửa lỗi Permission Denied an toàn bằng đồng bộ UID/GID
build_job:
  image: custom-python:3.11-nonroot
  before_script:
    - whoami && id
    - chown -R 10001:10001 $CI_PROJECT_DIR
  script:
    - python setup.py build
```
**Con số chốt:** Cấm dùng `chmod 777`, bắt buộc chẩn đoán đúng UID/GID.

---

**Nguyên lý cốt lõi:** Khắc phục sự cố Job bị treo vô tận (Hanging Job) do Daemon Process ngầm giữ STDOUT/STDERR pipe bằng chuyển hướng I/O.
**Phát biểu.** Chuyển hướng toàn bộ đầu ra của các tiến trình chạy ngầm: `nohup my-daemon > /dev/null 2>&1 &`.
**Giải thích cơ chế ngầm:** GitLab Runner theo dõi sự hoàn thành của một job bằng cách lắng nghe các ngõ ra STDOUT và STDERR của shell process. Nếu script khởi chạy một daemon ngầm (như web server thử nghiệm hay database ngầm) mà không chuyển hướng I/O, file descriptor của STDOUT sẽ bị giữ mở vô tận, khiến Runner đứng chờ mãi mãi cho đến khi chạm mốc timeout (buổi 46 QT 46.9). Khi chuyển hướng đầu ra vào `/dev/null`, file descriptor STDOUT/STDERR của shell chính sẽ đóng bình thường khi script chính kết thúc.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Khởi chạy tiến trình ngầm bằng `my-command &` mà không chuyển hướng `> /dev/null 2>&1`.
**Minh hoạ.** Thực thi daemon chuẩn: `./start-server.sh > /tmp/server.log 2>&1 &`.
```bash
# Thực thi daemon ngầm đúng chuẩn chuyển hướng File Descriptors
nohup ./redis-server --port 6379 > /tmp/redis.log 2>&1 &
echo $! > /tmp/redis.pid
# Kiểm tra daemon đã sẵn sàng
sleep 2 && nc -z localhost 6379
```
**Con số chốt:** 100% Tiến trình ngầm trong CI phải chuyển hướng STDOUT/STDERR.

---

### 1.3. Quy tắc Disk Pruning, System Calls & Incident Matrix (10 phút)

**Nguyên lý cốt lõi:** Tự động hóa dọn dẹp đĩa Runner bằng Cron Job `docker system prune -af --volumes` để ngăn lỗi "No space left on device".
**Phát biểu.** Cấu hình cronjob trên Runner Host định kỳ 3:00 AM tự động dọn dẹp Docker images, stopped containers và unused volumes.
**Giải thích cơ chế ngầm:** Mỗi job CI pull hàng trăm MB Docker images và sinh ra hàng GB build artifacts tạm. Sau vài ngày, ổ đĩa của Runner Node sẽ bị đầy 100%, dẫn đến sự cố hàng loạt pipeline thất bại đột ngột với lỗi `No space left on device`. Tự động hóa dọn dẹp đĩa giúp duy trì dung lượng trống liên tục mà không cần can thiệp thủ công.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chờ đĩa đầy sập Runner mới SSH vào xóa đĩa thủ công bằng tay.
**Minh hoạ.** Cronjob: `0 3 * * * docker system prune -af --filter "until=48h" --volumes`.
```bash
# Tệp cronjob đặt tại /etc/cron.d/runner-disk-cleanup
0 3 * * * root docker system prune -af --filter "until=48h" --volumes > /var/log/docker-prune.log 2>&1
```
**Con số chốt:** Giữ dung lượng ổ đĩa khả dụng của Runner luôn > 20%.

---

**Nguyên lý cốt lõi:** Phân tích root cause sự cố Flaky Artifact Pass-through do lệch thời gian đồng bộ NTP giữa các máy chủ Runner Nodes.
**Phát biểu.** Kích hoạt dịch vụ `chrony` hoặc `systemd-timesyncd` trên toàn bộ các máy chủ Runner Nodes để giữ độ lệch giờ $\Delta t < 100\text{ms}$.
**Giải thích cơ chế ngầm:** Khi Job A (build artifact) chạy trên Runner Node 1 có đồng hồ chạy nhanh hơn 5 phút so với Runner Node 2 (nơi Job B download artifact), GitLab Runner Engine sẽ từ chối hoặc bỏ qua artifact vì nghĩ rằng tệp artifact có `modification time` đến từ "tương lai", gây ra lỗi thất bại ngớ ngẩn `Artifacts file not found`.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bỏ qua kiểm tra NTP đồng hồ khi artifact truyền giữa các stages bị lỗi lạ.
**Minh hoạ.** Kiểm tra đồng bộ giờ: `timedatectl status | grep "NTP service: active"`.
```bash
# Kiểm tra và thiết lập đồng bộ thời gian NTP trên Ubuntu/Debian Runner Host
sudo systemctl enable --now chrony
sudo chronyc tracking | grep "System time"
```
**Con số chốt:** Độ lệch giờ giữa các Runner Nodes $\Delta t < 100\text{ms}$.

---

**Nguyên lý cốt lõi:** Truy vết System Calls bằng `strace -f` để tìm nguyên nhân gốc rễ khi ứng dụng bị Crash bí ẩn mà không xuất log.
**Phát biểu.** Thực thi lệnh lỗi dưới công cụ strace: `strace -f -e trace=file,network -o /tmp/trace.log ./my-binary`.
**Giải thích cơ chế ngầm:** Khi một binary compiled (như Go, C++, Rust) bị sập ngay khi khởi chạy (Segmentation Fault hoặc Silent Exit) mà không in ra bất kỳ log nào, `strace` sẽ ghi lại toàn bộ các system calls (như `openat`, `connect`, `read`, `access`). Điều này giúp SRE phát hiện ra tệp cấu hình bị thiếu, thư viện `.so` bị thiếu, hoặc địa chỉ mạng bị từ chối truy cập.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ngồi đoán nguyên nhân crash khi ứng dụng thoát không để lại log.
**Minh hoạ.** Phân tích vết system call: `grep -i "ENOENT" /tmp/trace.log` để tìm tệp bị thiếu.
```bash
# Lệnh thực thi strace chẩn đoán lỗi thiếu thư viện / file
strace -f -e trace=openat,access -o /tmp/strace.log ./app-binary
grep -E "ENOENT|EACCES" /tmp/strace.log
```
**Con số chốt:** 100% Ca binary crash im lặng được giải mã qua `strace`.

---

**Nguyên lý cốt lõi:** Xây dựng quy trình Troubleshooting Matrix 5 bước chuẩn hóa cho đội ngũ On-call SRE/DevOps Support.
**Phát biểu.** Áp dụng 5 bước chuẩn hóa: (1) Thu thập log thô & Exit Code, (2) Kiểm tra tài nguyên Host (RAM/CPU/Disk), (3) Bật `CI_DEBUG_TRACE`, (4) Reproduce trên Live Terminal, (5) Vá cấu hình và tạo Regression Test.
**Giải thích cơ chế ngầm:** Quy trình Troubleshooting Matrix chuẩn hóa giúp giảm thời gian phản ứng sự cố (MTTR) từ nhiều giờ xuống dưới 15 phút, ngăn ngừa tình trạng hoảng loạn và xử lý cảm tính của kỹ sư khi xảy ra sự cố nghiêm trọng trên quy trình phát hành.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Mỗi người một kiểu debugging ngẫu nhiên không có phương pháp luận chung.
**Minh hoạ.** Sơ đồ Incident Response Matrix dán tại phòng vận hành DevOps.
```markdown
# INCIDENT RESPONSE MATRIX (SRE ON-CALL)
Step 1: Check Exit Code (137 = OOM, 1 = App Error, 127 = Command Not Found)
Step 2: Check Host Resources (`df -h`, `free -m`, `dmesg -T | grep oom`)
Step 3: Enable `CI_DEBUG_TRACE: "true"`
Step 4: Launch `tmate` Live Debug Session
Step 5: Apply Fix & Add Automated Test
```
**Con số chốt:** Giảm 75% thời gian MTTR xử lý sự cố CI/CD nhờ Troubleshooting Matrix.

---

### 1.4. Đưa vào việc thật (4 phút)

### 7.1. Kịch bản áp dụng thực tế tại Tập đoàn Công nghệ Tài chính
Tại một tập đoàn Fintech với 400 microservices chạy trên hạ tầng Kubernetes GitLab Runner:
1. **Giải quyết sự cố OOM Exit Code 137:** Phát hiện 35% pipeline bị sập ngẫu nhiên khi build Java Spring Boot. Nhờ phân tích `dmesg` (QT 47.2), đội SRE phát hiện pod RAM limit cài 2GB nhưng JVM Heap chiếm 2.2GB. Tăng limit lên 4GB giúp giải quyết triệt me lỗi 137.
2. **Xử lý sự cố TLS Handshake Timeout:** Các container Runner trên AWS EKS bị kẹt khi pull dependencies từ Docker Hub. Kiểm tra MTU (QT 47.3) phát hiện MTU host là 1450 (AWS VXLAN) nhưng Docker bridge giữ 1500. Hạ MTU Docker xuống 1450 giúp pipeline chạy nhanh gấp 3 lần!
3. **Tiết kiệm 500GB ổ đĩa:** Triển khai Cronjob `docker system prune` (QT 47.9) giải phóng 500GB đĩa rác trên 50 Runner Nodes, triệt hạ hoàn toàn lỗi `No space left on device`.
4. **Phát hiện Flaky Artifact:** Xử lý sự cố lệch giờ NTP giữa 10 Runner Nodes (QT 47.10) giúp tỷ lệ artifact pass-through đạt 100%.

### 7.2. Case Study Thực tế: Sự cố Bí ẩn Lệch giờ NTP làm Hỏng Artifact Release
Một tập đoàn ngân hàng bị sự cố phát hành bản build khẩn cấp không thể deploy lên Production:
- **Nguyên nhân:** Runner Node A (chạy build) có đồng hồ NTP chạy nhanh hơn 3 phút so me với Runner Node B (chạy deploy). Khi Job Deploy tải artifact về, zip extractor phát hiện thời gian mtime của artifact ở "tương lai" nên tự động bỏ qua toàn bộ tệp binary!
- **Khắc phục chuẩn Buổi 47 (QT 47.10):** Kích hoạt `chrony` đồng bộ giờ trên toàn bộ máy chủ Runner. Sửa dứt điểm sự cố chỉ sau 5 phút!

### 7.3. Case Study 3: Phân Tích Lỗi Binary Crash của Microservice Go bằng `strace`
Một microservice viết bằng Golang bị sập ngẫu nhiên khi khởi chạy trên Kubernetes Runner Pod mà không in ra bất kỳ log lỗi nào:
- **Thực trạng:** Container exited với code 139 (Segmentation Fault). Không có log nào trong STDOUT.
- **Xử lý chuẩn Buổi 47 (QT 47.11):** Bật phiên `tmate` live debug (QT 47.5), thực thi `strace -f ./app-binary`. Phát hiện dòng `openat(AT_FDCWD, "/etc/ssl/certs/ca-certificates.crt", O_RDONLY) = -1 ENOENT (No such file or directory)`. Đơn giản là container base image Alpine bị thiếu gói `ca-certificates`! Thêm `apk add --no-cache ca-certificates` vào Dockerfile giúp ứng dụng chạy xanh mượt mà!

### 7.4. Case Study 4: Thảm Họa Dừng Toàn Bộ Hệ Thống CI/CD Do Trùng Khóa Cache Poisoning
Một lập trình viên thử nghiệm thư viện npm hỏng trên nhánh `feature/test-lib` và đẩy cache lên S3 MinIO:
- **Thảm họa:** Do đặt `key: "global-deps"` cố định, tệp `node_modules` hỏng bị ghi đè lên MinIO. Sau đó 50 dự án khác chạy trên nhánh `main` tải cache này về bị sập toàn bộ!
- **Khắc phục chuẩn Buổi 47 (QT 47.4):** Áp dụng Cache Key Versioning `key: "${CI_COMMIT_REF_SLUG}-v2"`. Loại bỏ ngay lập tức cache độc hại và cô lập môi trường cache của từng nhánh hoàn hảo!

### 7.5. Case Study 5: Sự cố Treo Job 3 Tiếng do Tiến trình Ghi Log Ngầm
Một dự án Node.js thực thi bài test integration có khởi chạy một instance Redis ngầm:
- **Nguyên nhân:** Script test gọi `redis-server &` mà không chuyển hướng STDOUT/STDERR. Tiến trình Redis ngầm giữ mở ngõ ra console làm GitLab Runner tưởng job đang in log và đứng chờ suốt 3 tiếng timeout.
- **Khắc phục chuẩn Buổi 47 (QT 47.8):** Đổi lệnh thành `redis-server > /dev/null 2>&1 &`. Job CI hoàn thành ngay lập tức trong 45 giây!

### 7.6. Case Study 6: Khắc phục sự cố Docker Executor không ghi được Artifact do Xung đột UID/GID
Một ứng dụng Python FastAPI chạy trong Docker Container với user `appuser` (UID 10001):
- **Thực trạng:** Khi kết thúc stage build, job báo lỗi `Uploading artifacts... FATAL: permission denied` và bị đỏ.
- **Phân tích:** GitLab Runner Helper container tạo thư mục `/builds` với quyền `root` (UID 0), khiến `appuser` (UID 10001) không thể tạo tệp artifact nén `.zip`.
- **Khắc phục chuẩn Buổi 47 (QT 47.7):** Thêm lệnh `before_script: - chown -R 10001:10001 $CI_PROJECT_DIR` vào `.gitlab-ci.yml` hoặc chạy container dưới quyền UID 1000. Artifact được tải lên S3 xanh 100%!

### 7.7. Case Study 7: Khôi Phục Hệ Thống CI/CD Sập 100% Do Đĩa Runner Bị Tràn
Một đợt release vào cuối quý khiến 1,000 pipelines chạy liên tục:
- **Thực trạng:** Sáng thứ Hai, toàn bộ 20 Runner Nodes báo đỏ với lỗi `No space left on device`. Mọi tiến trình phát hành phần mềm dừng hoạt động hoàn toàn.
- **Xử lý nhanh:** Đội On-call thực thi `docker system prune -af --volumes` trên cả 20 máy chủ, giải phóng 1.2 Terabytes dữ liệu rác.
- **Phòng ngừa lâu dài (QT 47.9):** Cài đặt Systemd Timer / Cronjob thực thi `docker system prune` tự động vào 3:00 AM mỗi ngày. Hệ thống CI/CD vận hành liên tục 365 ngày không bao giờ bị đĩa đầy!

### 7.8. Case Study 8: Xử lý sự cố TLS Verification Failure của Docker-in-Docker trong môi trường Air-Gapped Network
Tại một đơn vị bảo mật tài chính không có kết nối Internet trực tiếp (Air-gapped Network):
- **Triệu chứng:** Pipeline chạy `docker build` báo lỗi `Cannot connect to the Docker daemon at tcp://docker:2376. Is the docker daemon running?`. Log chi tiết báo lỗi `x509: certificate signed by unknown authority`.
- **Chẩn đoán:** Docker Client trong container chính không tin tưởng CA Certificate tự sinh của DinD Service khi khởi chạy trong mạng nội bộ.
- **Khắc phục chuẩn Buổi 47 (QT 47.6):** Cấu hình đúng `DOCKER_TLS_CERTDIR: "/certs"` và mount đường dẫn `/certs/client` shared volume giữa client và dind service. Docker client tự động đọc đúng CA cert và hoàn tất kết nối TLS 1.3 bảo mật 100%!

### 7.9. Case Study 9: Xử Lý Lỗi Phân Quyền Bí Ẩn Khi Ghi Volume Cache Trên Hạ Tầng Multi-Tenant Runner
Tại một đơn vị phát triển phần mềm dùng chung hạ tầng Runner cho 10 dự án độc lập:
- **Triệu chứng:** Khi job của Dự án A hoàn tất, nó tạo cache folder với quyền UID 0 (root). Khi job của Dự án B chạy lại trên cùng Runner Node đó, nó bị đỏ với lỗi `Permission Denied` không thể đọc ghi cache folder.
- **Chẩn đoán:** Docker executor không dọn dẹp quyền sở hữu thư mục volume cache chung giữa các lần chạy job của các người dùng khác nhau.
- **Khắc phục chuẩn Buổi 47 (QT 47.7):** Thiết lập `user = "1000:1000"` trong cấu hình `[runners.docker]` của `config.toml` và ép toàn bộ các job chạy dưới danh tính UID 1000 cố định. Mọi xung đột phân quyền bị dập tắt!

### 7.10. Case Study 10: Xử Lý Lỗi Pipeline Bị Treo Ở Bước Pull Image Do Docker Hub Rate Limit
Tại một startup công nghệ với 50 dự án CI/CD đẩy commit liên tục:
- **Triệu chứng:** Pipeline bị treo hàng giờ ở thông báo `Pulling docker image python:3.11...` rồi báo lỗi `429 Too Many Requests`.
- **Chẩn đoán:** Tất cả các Runner Node đều chia sẻ chung 1 địa chỉ IP NAT ngoài, khiến Docker Hub áp dụng hạn mức 100 pulls / 6 tiếng đối với anonymous users.
- **Khắc phục chuẩn SRE:** Cấu hình Dependency Proxy nội bộ trên GitLab Enterprise hoặc cài đặt Docker Hub Credentials qua `DOCKER_AUTH_CONFIG` trong variables cấp Group. Pipeline quay lại tốc độ tải image siêu tốc!

---

### 1.5. Khi nào KHÔNG nên dùng (2 phút)

1. **KHÔNG lạm dụng `CI_DEBUG_TRACE = "true"` trên môi trường Production bền vững:** Bật `CI_DEBUG_TRACE` sẽ in ra toàn bộ giá trị biến môi trường chưa mã hóa (nếu không được mask) và làm tăng dung lượng log lên 10-20 lần. Chỉ bật khi đang làm nhiệm vụ debugging và tắt ngay sau khi sửa lỗi xong.
2. **KHÔNG lạm dụng lệnh `chmod -R 777` để giải quyết lỗi Permission Denied:** Đây là hành vi cực kỳ nguy hiểm, làm vô hiệu hóa toàn bộ cơ sở bảo mật phân quyền của Linux và tạo ra lỗ hổng cho phép tiến trình độc hại chiếm đặc quyền host.
3. **KHÔNG tăng RAM container OOM vô hạn:** Khi gặp lỗi Exit Code 137, phải kiểm tra xem ứng dụng có bị Rò rỉ Bộ nhớ (Memory Leak) hay không trước khi quyết định nâng RAM limit cho Runner.
4. **KHÔNG áp dụng `docker system prune -f` trong giờ cao điểm làm việc:** Lệnh prune đĩa sẽ làm mất bớt các Docker layers base images cached, khiến các job CI chạy trong giờ làm việc phải pull lại image từ registry, làm tăng thời gian chờ của lập trình viên.

---

### 1.6. Bẫy hay gặp (2 phút)

1. **Bẫy 1: Nhầm lẫn giữa Exit Code 137 (OOM) và Exit Code 1 (App Code Failure).**
   - *Hậu quả:* Đi sửa code logic ứng dụng trong khi container bị trảm do thiếu RAM.
   - *Khắc phục:* Soi ngay `dmesg -T` hoặc `kubectl get pods` để xem lý do `OOMKilled`.

2. **Bẫy 2: Quên chuyển hướng STDOUT/STDERR cho tiến trình chạy ngầm khiến job bị treo vô hạn.**
   - *Hậu quả:* Job chạy hết timeout (vài tiếng) làm lãng phí phút runner và tắc nghẽn queue.
   - *Khắc phục:* Áp dụng đúng công thức `command > /dev/null 2>&1 &` (QT 47.8).

3. **Bẫy 3: Quên cấu hình `DOCKER_TLS_CERTDIR = "/certs"` khi dùng Docker-in-Docker.**
   - *Hậu quả:* Job build Docker image thất bại ngay lập tức với lỗi từ chối kết nối daemon.
   - *Khắc phục:* Đặt đầy đủ biến `DOCKER_TLS_CERTDIR` và mount volume `/certs/client` (QT 47.6).

4. **Bẫy 4: Để đĩa tràn 100% mới đi dọn rác Runner Node.**
   - *Hậu quả:* Máy chủ Runner bị khóa cứng, không thể tạo container mới, gây dừng toàn bộ pipeline công ty.
   - *Khắc phục:* Thiết lập Cronjob `docker system prune` tự động hàng đêm (QT 47.9).

5. **Bẫy 5: Để lệch giờ NTP giữa các máy chủ Runner.**
   - *Hậu quả:* Artifact tải về bị lỗi thời gian tương lai, khiến stage deploy thất bại ngớ ngẩn.
   - *Khắc phục:* Cài đặt `chrony` đồng bộ giờ tự động trên toàn bộ máy chủ (QT 47.10).

---

### 1.7. Tóm tắt (3 phút)

1. Debugging CI/CD phải dựa trên bằng chứng log thực nghiệm (Empirical Log Evidence), không đoán mò.
2. `CI_DEBUG_TRACE = "true"` là chìa khóa soi rõ mọi bước thực thi ngầm của Runner Shell.
3. Exit Code 137 khẳng định 100% lỗi thiếu RAM Container OOM.
4. Lỗi kẹt mạng TLS Handshake thường do lệch kích thước MTU giữa Docker Network và Cloud Host.
5. Luôn chuyển hướng STDOUT/STDERR cho các tiến trình ngầm để tránh Hanging Jobs.
6. Đồng bộ giờ NTP là điều kiện bắt buộc để truyền nhận Artifacts ổn định giữa các Runner Nodes.

---

### 1.8. Câu hỏi tự kiểm tra (5 phút)

1. Mã thoát (Exit Code) nào thể hiện container bị tiêu diệt do hết bộ nhớ RAM (OOM)?
   - A. Exit Code 1
   - B. Exit Code 127
   - C. Exit Code 137
   - D. Exit Code 255
   - *Đáp án đúng:* **C** (Exit Code 137 = 128 + SIGKILL 9).

2. Cờ biến nào trong GitLab CI/CD được dùng để bật chế độ verbose shell execution tracing?
   - A. `CI_VERBOSE = "true"`
   - B. `CI_DEBUG_TRACE = "true"`
   - C. `RUNNER_DEBUG = "1"`
   - D. `GIT_TRACE = "1"`
   - *Đáp án đúng:* **B** (`CI_DEBUG_TRACE = "true"`).

3. Nguyên nhân chính khiến tiến trình chạy ngầm `my-daemon &` làm job CI bị treo vô tận là gì?
   - A. Tiến trình ngầm chiếm 100% CPU.
   - B. Tiến trình ngầm không có quyền root.
   - C. Tiến trình ngầm giữ mở file descriptor của STDOUT/STDERR pipe.
   - D. GitLab Runner không hỗ trợ chạy ngầm.
   - *Đáp án đúng:* **C** (Giữ mở STDOUT/STDERR pipe làm Runner tưởng job chưa kết thúc).

4. Giải pháp triệt để cho lỗi Docker-in-Docker không kết nối được Docker Daemon từ phiên bản Docker 19.03+ là gì?
   - A. Đặt `DOCKER_HOST: tcp://localhost:2375`.
   - B. Đặt `DOCKER_TLS_CERTDIR: "/certs"` và dùng TLS port 2376.
   - C. Chạy lệnh `service docker start` trong container.
   - D. Tắt tường lửa ufw trên máy chủ.
   - *Đáp án đúng:* **B** (`DOCKER_TLS_CERTDIR: "/certs"`).

5. Lệnh Linux nào giúp truy vết các system calls của ứng dụng khi ứng dụng bị crash im lặng?
   - A. `top`
   - B. `netstat -tlpn`
   - C. `strace -f`
   - D. `systemctl status`
   - *Đáp án đúng:* **C** (`strace -f`).

---

## §12. Tài liệu tham khảo (2 phút)

| Nguồn tài liệu | Mô tả nội dung | Phiên bản áp dụng |
|---|---|---|
| GitLab Official Documentation — Troubleshooting GitLab Runner | Hướng dẫn chẩn đoán và khắc phục các sự cố thường gặp trên Runner và cài đặt `CI_DEBUG_TRACE` | GitLab Enterprise v15+ |
| Linux Kernel Documentation — Out of Memory Killer Mechanics | Chi tiết về cơ chế OOM Killer và cách tính điểm oom_score trong Cgroups Linux | Linux Kernel 5.x/6.x |
| Docker Official Guide — Docker-in-Docker TLS Security | Hướng dẫn cấu hình TLS bảo mật cho DinD Service trong CI/CD với `DOCKER_TLS_CERTDIR` | Docker Engine v20.10+ |
| AWS Knowledge Center — Troubleshooting MTU Packet Drops | Giải pháp sửa lỗi nghẽn gói tin TLS do lệch MTU trên Cloud VPC và Docker Network Bridge | AWS Networking |
| Systemd Documentation — System Clock Synchronization with Chrony | Hướng dẫn đồng bộ thời gian chuẩn NTP cho cụm máy chủ phân tán chống lỗi Artifacts | Linux Systemd |
| Linux Man Pages — `strace` System Call Tracer | Cẩm nang tra cứu và phân tích system calls cho SRE Troubleshooting và Binary Debugging | Linux General |
| CNCF Guide — Kubernetes Runner Troubleshooting & Pod Limits | Hướng dẫn chẩn đoán sự cố OOMKilled trên cụm Kubernetes Runner Executors | CNCF Standard |
| Google SRE Handbook — Incident Response & Root Cause Analysis | Phương pháp luận xử lý sự cố hệ thống và xây dựng Troubleshooting Matrix | Google SRE |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10 phút |
| §1 | Sau buổi này học viên LÀM ĐƯỢC gì | 1 phút |
| §2 | Cần biết trước | 1 phút |
| §3 | Thuật ngữ và mô hình tư duy | 8 phút |
| §4 | Quy tắc Troubleshooting Log & Memory Errors | 15 phút |
| §5 | Quy tắc Live Debugging & Container Network | 15 phút |
| §6 | Quy tắc Disk Pruning, System Calls & Incident Matrix | 10 phút |
| §7 | Đưa vào việc thật | 4 phút |
| §8 | Khi nào KHÔNG nên dùng | 2 phút |
| §9 | Bẫy hay gặp | 2 phút |
| §10 | Tóm tắt | 3 phút |
| §11 | Câu hỏi tự kiểm tra | 5 phút |
| §12 | Tài liệu tham khảo | 2 phút |
| **Tổng** | **Khối lý thuyết** | **60'** |

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên môi trường GitLab Community / Enterprise Edition cùng các GitLab Runner cô lập (Docker / Kubernetes Executor). Hãy đảm bảo bạn đã chuẩn bị môi trường thử nghiệm và cấu hình quyền truy cập cần thiết.

## Khối Thực hành — 150 phút

```mermaid
graph TD
    A["Bắt đầu Lab Troubleshooting 47"] --> B["Kịch bản 1: Debug LogVerbose & CI_DEBUG_TRACE (buổi 47 QT 47.1)"]
    B --> C["Kịch bản 2: Khắc phục lỗi Exit Code 137 OOM (buổi 47 QT 47.2)"]
    C --> D["Kịch bản 3: Sửa lỗi DNS & MTU Packet Drop (buổi 47 QT 47.3)"]
    D --> E["Kịch bản 4: Sửa lỗi DinD TLS Certificate Verification Failed (buổi 47 QT 47.6)"]
    E --> F["Kịch bản 5: Xử lý Hanging Jobs & Chuyển hướng Pipe (buổi 47 QT 47.8)"]
    F --> G["Kịch bản 6: Live Debug với Tmate & Terminal Session (buổi 47 QT 47.5)"]
    G --> H["Kịch bản 7: Tự động Prune đĩa & NTP Sync (buổi 47 QT 47.9, buổi 47 QT 47.10)"]
    H --> I["Kịch bản 8: Phân tích Binary Crash qua strace (buổi 47 QT 47.11)"]
    I --> J["Hoàn tất Lab Troubleshooting & Xóa môi trường Test"]
```

---

## 1. Yêu cầu môi trường & Thiết lập ban đầu (15 phút)

### 1.1. Chuẩn bị môi trường Lab
- 01 Máy chủ Linux (Ubuntu 22.04 LTS hoặc Rocky Linux 9) cài đặt sẵn GitLab Runner và Docker Engine.
- Quyền Root (`sudo`) để thao tác `dmesg`, `iptables`, `systemctl`, `strace`, `tmate`.
- Workspace làm việc tại thư mục `/tmp/lab-buoi-47/`.

```bash
# Lệnh khởi tạo môi trường làm việc Lab 47
sudo mkdir -p /tmp/lab-buoi-47/{app,logs,config,cache,scripts,dumps,trace_logs,dind_certs}
cd /tmp/lab-buoi-47/
sudo chmod -R 777 /tmp/lab-buoi-47/
echo "[INFO] Môi trường Lab Buổi 47 đã khởi tạo thành công tại /tmp/lab-buoi-47/"
```

---

## 2. Các kịch bản thực hành (120 phút)

### Kịch bản 1: Phân tích Shell Tracing ngầm với `CI_DEBUG_TRACE` (15 phút)

#### 1. Mạch tư duy (Mindset)
Khi job CI báo lỗi `Command exited with code 1` mà log chính không in ra bất kỳ chi tiết nào, ta cần áp dụng quy tắc buổi 47 QT 47.1 để bật `CI_DEBUG_TRACE: "true"`. Cờ này sẽ kích hoạt `set -x` trong shell execution script của Runner Engine, in ra mọi phép gán biến, lệnh rẽ nhánh `if/else`, và câu lệnh shell gây ra lỗi ngầm.

#### 2. Thao tác thực hành
Tạo file giả lập runner script `/tmp/lab-buoi-47/test-trace.sh` mô phỏng hành vi của Runner khi bật và chưa bật `CI_DEBUG_TRACE`.

```bash
cat << 'EOF' > /tmp/lab-buoi-47/test-trace.sh
#!/bin/bash
set -e

if [ "$CI_DEBUG_TRACE" = "true" ]; then
    set -x
fi

echo "=== MÔ PHỎNG GIẢI MÃ CI_DEBUG_TRACE ==="
export APP_ENV="production"
export DATABASE_URL="postgres://admin:pass@127.0.0.1:5432/db"
export REDIS_HOST="10.0.0.15"

echo "[DEBUG] Đang khởi tạo môi trường ứng dụng..."
echo "[DEBUG] APP_ENV=$APP_ENV"

if [ -z "$MISSING_SECRET_KEY" ]; then
    echo "LỖI BÍ ẨN: Không tìm thấy MISSING_SECRET_KEY!" >&2
    exit 1
fi
EOF

chmod +x /tmp/lab-buoi-47/test-trace.sh
```

Chạy script khi KHÔNG bật debug trace:
```bash
/tmp/lab-buoi-47/test-trace.sh || echo "Job thất bại không rõ lý do"
```

Chạy script KHI BẬT `CI_DEBUG_TRACE=true`:
```bash
CI_DEBUG_TRACE=true /tmp/lab-buoi-47/test-trace.sh || echo "Job thất bại có trace"
```

#### 3. Phân tích chi tiết Log đầu ra khi bật `CI_DEBUG_TRACE`
Khi bật cờ `CI_DEBUG_TRACE: "true"`, toàn bộ script runner generator sẽ hiển thị chi tiết từng dấu `+` biểu thị câu lệnh shell đang chạy:
```text
+ export APP_ENV=production
+ APP_ENV=production
+ export DATABASE_URL=postgres://admin:pass@127.0.0.1:5432/db
+ DATABASE_URL=postgres://admin:pass@127.0.0.1:5432/db
+ export REDIS_HOST=10.0.0.15
+ REDIS_HOST=10.0.0.15
+ echo '[DEBUG] Đang khởi tạo môi trường ứng dụng...'
[DEBUG] Đang khởi tạo môi trường ứng dụng...
+ echo '[DEBUG] APP_ENV=production'
[DEBUG] APP_ENV=production
+ '[' -z '' ']'
+ echo 'LỖI BÍ ẨN: Không tìm thấy MISSING_SECRET_KEY!'
LỖI BÍ ẨN: Không tìm thấy MISSING_SECRET_KEY!
+ exit 1
```

#### 4. Mẫu cấu hình `.gitlab-ci.yml` bật Debug Trace cho riêng job bị lỗi
```yaml
# Cấu hình khuyến nghị: Bật debug trace giới hạn ở job bị lỗi để bảo mật log
test_missing_variable_job:
  stage: test
  image: alpine:latest
  variables:
    CI_DEBUG_TRACE: "true" # Chỉ kích hoạt trace cho duy nhất job này
  script:
    - echo "Đang kiểm tra biến bí mật..."
    - sh /tmp/lab-buoi-47/test-trace.sh
```

### ### **CHECKPOINT 1**
Phân tích đầu ra log console để kiểm chứng sự khác biệt khi bật `CI_DEBUG_TRACE`:
```bash
CI_DEBUG_TRACE=true /tmp/lab-buoi-47/test-trace.sh 2>&1 | grep -q 'MISSING_SECRET_KEY' && echo "CHECKPOINT 1: ĐẠT - Đã chụp thành công verbose shell trace với CI_DEBUG_TRACE" || echo "CHECKPOINT 1: LỖI"
```

---

### Kịch bản 2: Chẩn đoán & Xử lý sự cố Out of Memory Exit Code 137 (15 phút)

#### 1. Mạch tư duy (Mindset)
Khi tiến trình bên trong container tiêu thụ bộ nhớ RAM vượt quá hạn mức cgroup limit được cấp phát, Linux Kernel OOM Killer sẽ gửi tín hiệu `SIGKILL` (signal 9) tiêu diệt tiến trình. Container sẽ thoát với mã `Exit Code 137` ($128 + 9$). Áp dụng quy tắc buổi 47 QT 47.2, ta kiểm tra `dmesg` để xác nhận lỗi OOM thay vì sửa code ứng dụng.

#### 2. Thao tác thực hành
Tạo container Docker thử nghiệm giới hạn RAM 64MB và chạy script tiêu tốn 128MB RAM để kích hoạt OOM Killer:

```bash
docker run --rm --name oom-test --memory="64m" python:3.11-slim python -c '
import time
print("Đang tiêu tốn RAM để kích hoạt OOM Killer...")
a = []
for i in range(100):
    a.append("X" * (10 * 1024 * 1024)) # Mỗi vòng lặp thêm 10MB
    time.sleep(0.1)
' || CODE=$?

echo "Exit code nhận được: $CODE"
```

#### 3. Bảng phân tích mã lỗi Exit Codes phổ biến trong CI/CD

| Exit Code | Tên Tín hiệu (Signal) | Ý nghĩa thực tiễn | Hành động khắc phục của SRE |
|---|---|---|---|
| **Exit Code 0** | SUCCESS | Tiến trình hoàn thành thành công không có lỗi | Không cần xử lý |
| **Exit Code 1** | General Error | Lỗi mã nguồn ứng dụng hoặc câu lệnh shell thất bại | Kiểm tra log ứng dụng, sửa lỗi code |
| **Exit Code 127** | Command Not Found | Câu lệnh không tồn tại trong môi trường PATH container | Cài bổ sung package hoặc kiểm tra tên lệnh |
| **Exit Code 137** | 128 + SIGKILL (9) | Tiến trình bị OOM Killer trảm do vượt RAM Cgroup Limit | Tăng `memory_limit` trong `config.toml` (buổi 47 QT 47.2) |
| **Exit Code 139** | 128 + SIGSEGV (11) | Segmentation fault, ứng dụng truy cập ô nhớ bất hợp lệ | Dùng `strace -f` để tìm thư viện hỏng (buổi 47 QT 47.11) |
| **Exit Code 143** | 128 + SIGTERM (15) | Tiến trình bị hủy bởi lệnh timeout hoặc hủy job thủ công | Kiểm tra timeout limit của pipeline |

#### 4. Phân tích chi tiết Kernel OOM Log từ `dmesg`
```text
[Mon Aug 22 09:15:22 2026] oom-kill:constraint=CONSTRAINT_MEMCG,nodemask=(null),cpuset=/,mems_allowed=0,oom_memcg=/docker/8f1e2a3b4c,task_memcg=/docker/8f1e2a3b4c,task=python,pid=4512,uid=0
[Mon Aug 22 09:15:22 2026] Memory cgroup out of memory: Killed process 4512 (python) total-vm:184512kB, anon-rss:65536kB, file-rss:1280kB, shmem-rss:0kB, uid:0
[Mon Aug 22 09:15:22 2026] oom_reaper: reaped process 4512 (python), now anon-rss:0kB, file-rss:0kB, shmem-rss:0kB
```

#### 5. Mẫu tệp cấu hình `config.toml` điều chỉnh RAM/Swap Limit
```ini
# Cấu hình khắc phục OOM Exit Code 137
[[runners]]
  name = "high-memory-runner"
  url = "https://gitlab.company.internal/"
  token = "GLRT-xxxx"
  executor = "docker"
  [runners.docker]
    image = "maven:3.8-openjdk-17"
    memory = "4g"              # Tăng hạn mức RAM cgroup lên 4GB
    memory_swap = "6g"         # Cấp thêm 2GB Swap bảo vệ
    memory_reservation = "2g"  # Đảm bảo giữ tối thiểu 2GB RAM thực
```

### ### **CHECKPOINT 2**
Kiểm tra Exit Code và đọc Kernel Logs qua `dmesg`:
```bash
[ "$CODE" -eq 137 ] && echo "CHECKPOINT 2: ĐẠT - Xác nhận chính xác lỗi Out of Memory với Exit Code 137" || echo "CHECKPOINT 2: LỖI"
```

---

### Kịch bản 3: Sửa lỗi DNS Failure & MTU Packet Truncation (15 phút)

#### 1. Mạch tư duy (Mindset)
Trên hạ tầng Cloud VPC (AWS EC2, Google Cloud Engine), card mạng host thường có kích thước MTU nhỏ hơn mặc định 1500 của Docker virtual bridge (như AWS VXLAN MTU 1450). Nếu gói tin TLS Certificate lớn truyền qua, kết nối TCP sẽ bị treo vô hạn ở bước Handshake. Áp dụng quy tắc buổi 47 QT 47.3, ta phải ép MTU của Docker Network về 1450.

#### 2. Thao tác thực hành
Kiểm tra MTU của card mạng Host và tạo Docker Network với MTU 1450:

```bash
# Đọc MTU hiện tại của card mạng mặc định
HOST_MTU=$(ip route show default | awk '{print $5}' | xargs ip link show | grep mtu | awk '{print $5}')
echo "MTU card mạng Host hiện tại: $HOST_MTU"

# Tạo mạng Docker tùy chỉnh với MTU 1450 chuẩn Cloud VPC
docker network create --driver bridge --opt com.docker.network.driver.mtu=1450 lab47-network || true
```

Chạy container thử nghiệm truy vấn DNS và kết nối HTTPS trên mạng `lab47-network`:
```bash
docker run --rm --net lab47-network alpine:latest sh -c "
apk add --no-cache bind-tools curl && \
dig +short registry.gitlab.com && \
curl -vvv https://registry.gitlab.com/v2/ > /dev/null 2>&1
"
```

#### 3. Mô phỏng cấu hình MTU trong `config.toml` của GitLab Runner
```ini
# Cấu hình chuẩn MTU 1450 cho Runner Docker Executor
[[runners]]
  name = "aws-cloud-runner-01"
  url = "https://gitlab.company.internal/"
  token = "GLRT-xxxxxxxxx"
  executor = "docker"
  [runners.custom_build_dir]
  [runners.cache]
    MaxUploadedArchiveSize = 0
  [runners.docker]
    tls_verify = false
    image = "alpine:latest"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 2147483648
    network_mode = "bridge"
    dns = ["10.0.0.2", "8.8.8.8"]
    mtu = 1450
```

### ### **CHECKPOINT 3**
Xác nhận MTU của Docker Network đã được thiết lập chính xác 1450:
```bash
docker network inspect lab47-network | grep -q '"com.docker.network.driver.mtu": "1450"' && echo "CHECKPOINT 3: ĐẠT - Cấu hình MTU Docker Network 1450 sửa dứt điểm lỗi kẹt TLS Handshake" || echo "CHECKPOINT 3: LỖI"
```

---

### Kịch bản 4: Khắc phục sự cố Docker-in-Docker (DinD) TLS Certificates (15 phút)

#### 1. Mạch tư duy (Mindset)
Từ Docker 19.03+, Docker-in-Docker daemon yêu cầu bật TLS mặc định. Nếu không khai báo `DOCKER_TLS_CERTDIR: "/certs"` và mount volume chứng chỉ, client sẽ không thể kết nối tới daemon qua port 2376. Áp dụng quy tắc buổi 47 QT 47.6 để thiết lập TLS chung.

#### 2. Thao tác thực hành
Tạo script mô phỏng khởi chạy container Docker-in-Docker Service với đường dẫn chứng chỉ TLS bảo mật:

```bash
# Tạo volume chứng chỉ dùng chung
docker volume create dind-certs-client || true

# Khởi chạy Docker Daemon Service với TLS
docker run -d --name lab47-dind-daemon \
  --privileged \
  -e DOCKER_TLS_CERTDIR=/certs \
  -v dind-certs-client:/certs/client \
  docker:24.0.5-dind || true

sleep 5

# Khởi chạy Docker Client container kết nối qua TLS port 2376
docker run --rm \
  -e DOCKER_HOST=tcp://lab47-dind-daemon:2376 \
  -e DOCKER_TLS_CERTDIR=/certs \
  -e DOCKER_TLS_VERIFY=1 \
  -e DOCKER_CERT_PATH=/certs/client \
  -v dind-certs-client:/certs/client \
  --link lab47-dind-daemon:docker \
  docker:24.0.5 docker info > /tmp/lab-buoi-47/dind-info.log 2>&1 || true

docker stop lab47-dind-daemon || true
docker rm lab47-dind-daemon || true
```

#### 3. Mẫu tệp cấu hình `.gitlab-ci.yml` chuẩn Docker-in-Docker (DinD)
```yaml
# Cấu hình mẫu sản xuất chống lỗi DinD TLS Certificate
build_docker_image:
  stage: build
  image: docker:24.0.5
  services:
    - name: docker:24.0.5-dind
      alias: docker
  variables:
    DOCKER_HOST: "tcp://docker:2376"
    DOCKER_TLS_CERTDIR: "/certs"
    DOCKER_TLS_VERIFY: 1
    DOCKER_CERT_PATH: "$DOCKER_TLS_CERTDIR/client"
  before_script:
    - until docker info > /dev/null 2>&1; do sleep 1; done
    - echo "Docker Daemon TLS đã sẵn sàng kết nối!"
  script:
    - docker build -t registry.company.internal/app:$CI_COMMIT_SHA .
    - docker push registry.company.internal/app:$CI_COMMIT_SHA
```

### ### **CHECKPOINT 4**
Kiểm tra kết quả kết nối Docker DinD qua TLS:
```bash
grep -q "Server Version" /tmp/lab-buoi-47/dind-info.log && echo "CHECKPOINT 4: ĐẠT - Đã kết nối Docker-in-Docker Daemon thành công qua TLS với DOCKER_TLS_CERTDIR" || echo "CHECKPOINT 4: LỖI"
```

---

### Kịch bản 5: Xử lý Hanging Job do Tiến trình Ngầm Giữ STDOUT Pipe (15 phút)

#### 1. Mạch tư duy (Mindset)
Khi một script CI khởi chạy một daemon ngầm (như web server thử nghiệm) mà không chuyển hướng ngõ ra STDOUT/STDERR (`> /dev/null 2>&1 &`), file descriptor ngõ ra sẽ bị giữ mở. GitLab Runner tưởng rằng job chưa hoàn tất và sẽ đứng chờ mãi mãi cho đến khi timeout. Áp dụng quy tắc buổi 47 QT 47.8 để giải phóng pipe.

#### 2. Thao tác thực hành
Viết script mô phỏng tiến trình ngầm đúng chuẩn chuyển hướng I/O:

```bash
cat << 'EOF' > /tmp/lab-buoi-47/run-daemon.sh
#!/bin/bash
echo "Bắt đầu khởi chạy daemon thử nghiệm..."

# Cách làm đúng: Chuyển hướng STDOUT và STDERR vào dev null
nohup python3 -m http.server 8088 > /dev/null 2>&1 &
DAEMON_PID=$!

echo "Daemon đã chạy với PID: $DAEMON_PID"
sleep 2

# Kiểm tra port đã lắng nghe
nc -z 127.0.0.1 8088 && echo "Daemon đang hoạt động trên port 8088"

# Dọn dẹp tiến trình
kill $DAEMON_PID
EOF

chmod +x /tmp/lab-buoi-47/run-daemon.sh
/tmp/lab-buoi-47/run-daemon.sh > /tmp/lab-buoi-47/daemon-output.log 2>&1
```

#### 3. Bảng so sánh 2 cách khởi chạy Daemon trong CI Script

| Tiêu chí so sánh | Cách sai (`my-daemon &`) | Cách đúng (`nohup my-daemon > /dev/null 2>&1 &`) |
|---|---|---|
| **File Descriptor STDOUT** | Giữ mở liên kết với Runner Engine Console | Đóng liên kết và chuyển hướng sang `/dev/null` |
| **File Descriptor STDERR** | Giữ mở liên kết với Runner Engine Console | Đóng liên kết và chuyển hướng sang `/dev/null` |
| **Trạng thái kết thúc Job** | Treo vô tận cho tới mốc Timeout (3 tiếng) | Kết thúc tức thì khi script chính hoàn thành |
| **Tiêu tốn phút Runner** | Lãng phí 100% hạn mức phút Runner | Tiết kiệm tối đa thời gian điện toán |

### ### **CHECKPOINT 5**
Xác nhận script kết thúc ngay lập tức mà không bị treo pipe:
```bash
grep -q "Daemon đang hoạt động" /tmp/lab-buoi-47/daemon-output.log && echo "CHECKPOINT 5: ĐẠT - Tiến trình ngầm chuyển hướng I/O thành công, không làm kẹt STDOUT pipe" || echo "CHECKPOINT 5: LỖI"
```

---

### Kịch bản 6: Live Debugging trực tiếp với `tmate` Interactive Session (15 phút)

#### 1. Mạch tư duy (Mindset)
Thay vì push hàng chục commit rác để in log thử nghiệm, SRE kích hoạt phiên SSH `tmate` trực tiếp trên Runner container để truy cập terminal live debug theo quy tắc buổi 47 QT 47.5.

#### 2. Thao tác thực hành
Giả lập script khởi tạo phiên Tmate background session và xuất URL kết nối:

```bash
cat << 'EOF' > /tmp/lab-buoi-47/test-tmate.sh
#!/bin/bash
echo "=== KÍCH HOẠT PHIÊN LIVE DEBUGGING TMATE ==="
echo "SSH Connection URL: ssh user_lab47@tmate.io:2222"
echo "Web Terminal URL: https://tmate.io/t/lab47-debug-session"
echo "Trạng thái: Container đang được giữ sống trong 1800 giây để SRE live debug."
EOF

chmod +x /tmp/lab-buoi-47/test-tmate.sh
/tmp/lab-buoi-47/test-tmate.sh > /tmp/lab-buoi-47/tmate-session.log
```

#### 3. Mẫu job `.gitlab-ci.yml` kích hoạt Tmate Debugging khi xảy ra lỗi (`when: on_failure`)
```yaml
# Job tự động mở SSH Session Debugging khi stage trước bị thất bại
debug_on_failure:
  stage: test
  image: ubuntu:22.04
  script:
    - apt-get update && apt-get install -y tmate openssh-client curl
    - tmate -F -S /tmp/tmate.sock new-session -d
    - tmate -S /tmp/tmate.sock wait tmate-ready
    - echo "===================================================="
    - echo "PHIÊN LIVE DEBUGGING ĐÃ SẴN SÀNG:"
    - tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'
    - echo "===================================================="
    - sleep 1800  # Giữ container sống 30 phút để SSH trực tiếp
  when: on_failure
```

### ### **CHECKPOINT 6**
Xác nhận đã trích xuất được thông tin kết nối SSH Tmate Live Debugging:
```bash
grep -q "ssh user_lab47@tmate.io" /tmp/lab-buoi-47/tmate-session.log && echo "CHECKPOINT 6: ĐẠT - Khởi tạo phiên Live Debugging Tmate thành công" || echo "CHECKPOINT 6: LỖI"
```

---

### Kịch bản 7: Tự động dọn dẹp đĩa & Kiểm tra đồng bộ giờ NTP (15 phút)

#### 1. Mạch tư duy (Mindset)
Ổ đĩa Runner bị tràn 100% sẽ gây sập toàn bộ CI/CD. Ta cần cấu hình Cronjob `docker system prune` tự động dọn rác đĩa (buổi 47 QT 47.9) và kiểm tra dịch vụ NTP để tránh lệch giờ artifact (buổi 47 QT 47.10).

#### 2. Thao tác thực hành
Tạo script kiểm tra dung lượng ổ đĩa và trạng thái đồng bộ giờ NTP trên máy chủ:

```bash
cat << 'EOF' > /tmp/lab-buoi-47/check-system.sh
#!/bin/bash
# 1. Kiểm tra dung lượng đĩa trống
DISK_FREE_PCT=$(df -k / | tail -1 | awk '{print 100-$5}' | tr -d '%')
echo "Dung lượng đĩa còn trống: ${DISK_FREE_PCT}%"

# 2. Giả lập lệnh dọn dẹp đĩa Docker Prune
docker system prune -f --filter "until=24h" > /dev/null 2>&1 || true

# 3. Kiểm tra trạng thái NTP
if command -v timedatectl > /dev/null 2>&1; then
    NTP_STATUS=$(timedatectl | grep "NTP service" | awk '{print $3}')
    echo "NTP Service: $NTP_STATUS"
else
    echo "NTP Service: active (simulated)"
fi
EOF

chmod +x /tmp/lab-buoi-47/check-system.sh
/tmp/lab-buoi-47/check-system.sh > /tmp/lab-buoi-47/system-check.log
```

#### 3. Cấu hình Cronjob dọn đĩa tự động tại `/etc/cron.d/runner-cleanup`
```bash
# Cấu hình Cronjob tự động dọn dẹp Docker images rác vào 3:00 AM hàng ngày
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

0 3 * * * root /usr/bin/docker system prune -af --filter "until=48h" --volumes > /var/log/docker-prune.log 2>&1
```

### ### **CHECKPOINT 7**
Xác nhận kiểm tra dung lượng đĩa và hệ thống đồng bộ thời gian NTP đạt yêu cầu:
```bash
grep -q "Dung lượng đĩa còn trống" /tmp/lab-buoi-47/system-check.log && echo "CHECKPOINT 7: ĐẠT - Kiểm tra dọn dẹp đĩa tự động và NTP Sync thành công" || echo "CHECKPOINT 7: LỖI"
```

---

### Kịch bản 8: Truy vết System Calls bằng `strace` khi Binary Crash im lặng (15 phút)

#### 1. Mạch tư duy (Mindset)
Khi một tệp binary bị crash im lặng mà không in log ra STDOUT, ta sử dụng công cụ `strace -f` để ghi lại các system call `openat`, `access` nhằm phát hiện tệp cấu hình hoặc thư viện `.so` bị thiếu theo quy tắc buổi 47 QT 47.11.

#### 2. Thao tác thực hành
Tạo một script shell giả lập binary crash do thiếu tệp cấu hình `/etc/missing-config.conf` và dùng `strace` để phát hiện tệp bị thiếu:

```bash
cat << 'EOF' > /tmp/lab-buoi-47/faulty-app.sh
#!/bin/bash
# Giả lập ứng dụng tìm tệp cấu hình và sập im lặng
if [ ! -f "/etc/missing-config.conf" ]; then
    # Cố tình truy cập tệp không tồn tại
    cat /etc/missing-config.conf 2>/dev/null
    exit 1
fi
EOF

chmod +x /tmp/lab-buoi-47/faulty-app.sh

# Chạy strace bắt vết system calls
strace -f -e trace=openat,access -o /tmp/lab-buoi-47/strace-output.log /tmp/lab-buoi-47/faulty-app.sh || true
```

#### 3. Đầu ra mẫu của lệnh `strace` giúp tìm tệp cấu hình bị thiếu
```text
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
access("/etc/missing-config.conf", F_OK) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/missing-config.conf", O_RDONLY) = -1 ENOENT (No such file or directory)
exit_group(1)                           = ?
+++ exited with 1 +++
```

### ### **CHECKPOINT 8**
Phân tích vết log `strace` để tìm ra tệp bị thiếu `ENOENT`:
```bash
grep -q "missing-config.conf" /tmp/lab-buoi-47/strace-output.log && echo "CHECKPOINT 8: ĐẠT - Phát hiện chính xác tệp bị thiếu gây crash ứng dụng bằng strace system calls" || echo "CHECKPOINT 8: LỖI"
```

---

## 3. Xử lý sự cố (15 phút)

### 3.1. Danh mục 120+ tình huống sự cố thực tế trong Debugging CI/CD

| STT | Triệu chứng lỗi (Symptoms) | Nguyên nhân gốc rễ (Root Cause) | Giải pháp xử lý chuẩn SRE |
|---|---|---|---|
| 1 | Job thất bại với `Exit Code 137` | Container RAM bị Linux OOM Killer tiêu diệt | Tăng `memory_limit` trong `config.toml` hoặc JVM `-Xmx` (buổi 47 QT 47.2) |
| 2 | Log job ngắt ngang không rõ câu lệnh lỗi | Mặc định shell script giấu chi tiết lệnh thực thi | Khai báo `CI_DEBUG_TRACE: "true"` trong `.gitlab-ci.yml` (buổi 47 QT 47.1) |
| 3 | Job build Docker kẹt ở TLS Handshake | Lệch MTU giữa Docker Network (1500) và AWS VPC (1450) | Đặt `mtu = 1450` trong `config.toml` `[runners.docker]` (buổi 47 QT 47.3) |
| 4 | DinD không kết nối được Docker Daemon | Thiếu chứng chỉ TLS chia sẻ giữa Client và Daemon | Khai báo `DOCKER_TLS_CERTDIR: "/certs"` và mount client certs (buổi 47 QT 47.6) |
| 5 | Job chạy ngầm bị treo vô tận đến timeout | Tiến trình ngầm giữ mở ngõ ra STDOUT/STDERR pipe | Chuyển hướng đầu ra `command > /dev/null 2>&1 &` (buổi 47 QT 47.8) |
| 6 | Lập trình viên push 20 commit rác để debug | Không có công cụ tương tác live debug trực tiếp | Kích hoạt phiên SSH `tmate` live terminal trong job (buổi 47 QT 47.5) |
| 7 | Runner sập đột ngột với `No space left on device` | Ổ đĩa bị đầy do tích tụ Docker images/volumes rác | Cài đặt Cronjob `docker system prune -af --volumes` hàng đêm (buổi 47 QT 47.9) |
| 8 | Artifact stage deploy báo không tìm thấy tệp | Lệch giờ NTP giữa Runner Node A và Node B | Bật dịch vụ `chrony` đồng bộ thời gian $\Delta t < 100\text{ms}$ (buổi 47 QT 47.10) |
| 9 | Application binary crash thoát im lặng | Thiếu tệp cấu hình hoặc thư viện `.so` phụ thuộc | Dùng `strace -f -e trace=file` để bắt tệp bị thiếu (buổi 47 QT 47.11) |
| 10 | Cache bị hỏng làm 50 pipeline đỏ dây chuyền | Đặt chung một cache key không phân biệt nhánh | Áp dụng Cache Key Versioning `${CI_COMMIT_REF_SLUG}-v2` (buổi 47 QT 47.4) |
| 11 | Job đỏ với lỗi `Permission denied` ghi file | Container user non-root khác UID với thư mục build | Cấu hình `chown -R UID:GID $CI_PROJECT_DIR` (buổi 47 QT 47.7) |
| 12 | Docker pull báo lỗi `429 Too Many Requests` | Đạt hạn mức rate limit của Docker Hub | Đăng ký Docker credentials hoặc dùng Dependency Proxy |
| 13 | Lỗi `Git clone failed` với SSL certificate error | Máy chủ Runner thiếu CA root certificates | Cập nhật gói `ca-certificates` trên Runner host |
| 14 | Job bị hủy đột ngột sau 1 tiếng | Vượt mốc max timeout cấu hình cấp Project | Tăng `timeout` trong `.gitlab-ci.yml` lên mức hợp lý |
| 15 | Lỗi `Cannot connect to server` khi gọi API nội bộ | Container không phân giải được tên miền DNS | Thêm cấu hình `dns = ["10.0.0.2"]` vào `config.toml` |
| 16 | Git submodule sync bị từ chối truy cập | Thiếu SSH Deploy Key hoặc CI_JOB_TOKEN permission | Cấp quyền read repository cho `CI_JOB_TOKEN` |
| 17 | Cache download bị timeout sập giữa chừng | File cache quá lớn (nhiều GB) qua đường truyền chậm | Tách nhỏ cache hoặc loại bỏ thư mục tạm rác |
| 18 | High CPU usage khiến Runner đứng máy | Thiếu giới hạn CPU limit trên container executor | Cài đặt `cpus = "2.0"` trong `config.toml` |
| 19 | Lỗi `Docker socket permission denied` | User `gitlab-runner` chưa nằm trong group `docker` | Chạy lệnh `usermod -aG docker gitlab-runner` |
| 20 | Docker image build bị chậm bất thường | Không tận dụng được Docker Build Cache | Sử dụng `--cache-from` hoặc `DOCKER_BUILDKIT=1` |
| 21 | Lỗi `Network bridge not found` khi khởi tạo job | Docker daemon bị mất cấu hình bridge network | Restart dịch vụ Docker: `systemctl restart docker` |
| 22 | NPM install bị lỗi EACCES trong container | NPM cache directory bị sở hữu bởi Root user | Đặt `npm config set cache /tmp/.npm` |
| 23 | Artifact upload bị lỗi 413 Payload Too Large | Kích thước artifact vượt hạn mức cấu hình GitLab | Tăng `Maximum artifact size` trong GitLab Admin Area |
| 24 | Shell script báo lỗi `\r: command not found` | File `.gitlab-ci.yml` bị dính ký tự CRLF từ Windows | Chuyển đổi định dạng mã hóa file sang LF |
| 25 | Lỗi `Host key verification failed` khi SSH | Máy chủ đích chưa có SSH Host Key trong known_hosts | Thêm lệnh `ssh-keyscan` vào `before_script` |
| 26 | Job kẹt ở trạng thái `Pending` không chạy | Không có Runner nào khớp với `tags` yêu cầu | Kiểm tra tag của Runner trong GitLab Admin UI |
| 27 | Lỗi `Killed` khi đang biên dịch C++/Rust | Compiler ngấu nghiến toàn bộ RAM của host | Giới hạn số luồng biên dịch bằng `make -j2` |
| 28 | Redis/Postgres service container không khởi động | Service container thiếu biến môi trường bắt buộc | Khai báo biến `POSTGRES_PASSWORD` trong job variables |
| 29 | Python pip install bị lỗi TLS cert expired | Đồng hồ hệ thống của Runner Node bị chạy sai | Cập nhật đồng bộ giờ bằng `chronyd -q` |
| 30 | Lỗi `Shared runner minutes limit exceeded` | Dự án dùng hết hạn mức phút runner miễn phí | Nâng hạn mức phút runner hoặc dùng Specific Runner |
| 31 | Shell execution báo `bash: line 12: jq: command not found` | Container base image thiếu công cụ `jq` | Thêm bước cài đặt `apk add --no-cache jq` |
| 32 | Terraform apply bị lỗi State Lock | Pipeline trước bị crash đột ngột chưa giải phóng lock | Chạy `terraform force-unlock` thủ công |
| 33 | Lỗi `Job canceled by newer pipeline` | Bật cờ `interruptible: true` khi có commit mới | Đây là tính năng tối ưu chi phí, không phải lỗi |
| 34 | Maven build báo `Out of Memory Metaspace` | Metaspace JVM bị tràn khi nạp quá nhiều class | Thêm `-XX:MaxMetaspaceSize=512m` vào `MAVEN_OPTS` |
| 35 | Lỗi `Container failed to start` trong Kubernetes Runner | Kubernetes Cluster bị cạn kiệt IP Pod Subnet | Dọn dẹp các Pod rác tồn đọng trong Namespace |
| 36 | File `.env` chứa mật khẩu bị lộ trên log console | Quên mask biến môi trường trong GitLab CI | Bật cờ `Mask variable` trong settings CI/CD |
| 37 | Lỗi `Read-only file system` trong container | Volume mount bị cấu hình cờ `:ro` | Đổi cờ volume mount thành `:rw` |
| 38 | Git push tag bị từ chối bởi GitLab | Nhánh hoặc Tag nằm trong danh sách Protected | Phân quyền Maintainer cho `CI_JOB_TOKEN` |
| 39 | Lỗi `cgroup memory limit reached` | Container bị rò rỉ RAM dần theo thời gian | Tối ưu ứng dụng và khởi động lại container định kỳ |
| 40 | Lỗi `Too many open files` khi chạy test | Hạn mức `ulimit` file descriptor của container quá nhỏ | Cài đặt `ulimits` `nofile=65535` trong `config.toml` |
| 41 | Curl connection reset by peer trong container | Tường lửa UFW/IPTables của Host chặn traffic | Mở port bridge interface trong iptables rules |
| 42 | Go build bị lỗi checksum mismatch | Go module proxy bị cache dữ liệu cũ | Xóa cache go proxy bằng `go clean -modcache` |
| 43 | Job deploy Helm chart báo lỗi RBAC unauthorized | ServiceAccount của Runner thiếu ClusterRoleBinding | Gán quyền `cluster-admin` cho ServiceAccount |
| 44 | Lỗi `No matching key exchange algorithm` khi SSH | Máy chủ SSH đích dùng thuật toán mã hóa cũ | Thêm `-o KexAlgorithms=+diffie-hellman-group1-sha1` |
| 45 | Container bị mất file log sau khi job kết thúc | Quên cấu hình Artifacts cho thư mục log | Khai báo `artifacts: paths: - logs/` |
| 46 | Pipeline bị sập do file YAML bị sai indent | Cú pháp file `.gitlab-ci.yml` bị lỗi indentation | Dùng công cụ GitLab CI Lint để kiểm tra cú pháp |
| 47 | Lỗi `ImagePullBackOff` trên Kubernetes Executor | Sai tên image hoặc registry secret không hợp lệ | Kiểm tra `imagePullSecrets` trong cấu hình Pod |
| 48 | Job build bị treo khi tải thư viện Gradle | Gradle Daemon bị treo ở background | Thêm tham số `--no-daemon` khi gọi lệnh build |
| 49 | Lỗi `Zstandard compression failed` khi nén cache | Phiên bản Runner Helper quá cũ không hỗ trợ zstd | Cập nhật GitLab Runner Helper image mới nhất |
| 50 | Cronjob dọn dẹp đĩa bị ngưng hoạt động | Dịch vụ `cron` hoặc `crond` trên máy chủ bị stopped | Khởi động lại dịch vụ `systemctl restart cron` |
| 51 | Lỗi `Fatal: empty ident name` trong git config | Git user name/email chưa được cài đặt trong job | Thêm `git config --global user.email "ci@company.com"` |
| 52 | AWS CLI error: `ExpiredToken` | Mật khẩu IAM temporary credentials bị hết hạn | Cập nhật cờ làm mới token AWS STS trước khi deploy |
| 53 | Lỗi `No space left on device` khi Docker build | Docker build context chứa quá nhiều file rác lớn | Thêm các thư mục rác vào tệp `.dockerignore` |
| 54 | Job kẹt ở `stuck` không gán cho Runner nào | Tag của job không trùng khớp với Tag của Runner | Điều chỉnh `tags:` trong `.gitlab-ci.yml` khớp với Runner |
| 55 | Lỗi `Invalid volume destination` | Đường dẫn volume mount chứa ký tự đặc biệt | Chuẩn hóa đường dẫn volume mount trong `config.toml` |
| 56 | Pod bị Status `CrashLoopBackOff` trên K8s Runner | Application entrypoint bị crash liên tục | Đọc log pod qua `kubectl logs <pod-name> -n gitlab-runner` |
| 57 | Lỗi `FATAL: Job failed: exit status 1` trên Windows Runner | PowerShell script bị dính lỗi Execution Policy | Thêm `Set-ExecutionPolicy Bypass -Scope Process` |
| 58 | Pip install bị lỗi `Could not find a version` | Private PyPI repository yêu cầu vpc endpoint | Thêm `--extra-index-url` trỏ về PyPI nội bộ |
| 59 | Docker container bị lặp restart liên tục | Container restart policy cài `always` khi script fail | Đổi cờ restart policy thành `on-failure:3` |
| 60 | Lỗi `Cannot connect to the Docker daemon at unix:///var/run/docker.sock` | File socket `/var/run/docker.sock` chưa mount vào container | Mount `/var/run/docker.sock:/var/run/docker.sock` |
| 61 | Lỗi `Resource temporarily unavailable` | Hạn mức `nproc` tiến trình tối đa của user bị vượt | Tăng `nproc` trong `/etc/security/limits.conf` |
| 62 | Node.js build bị lỗi `JavaScript heap out of memory` | Node process vượt quá hạn mức RAM 1.4GB mặc định | Khai báo `NODE_OPTIONS="--max-old-space-size=4096"` |
| 63 | Lỗi `Repository not found` khi Git fetch | Access token hết hạn hoặc sai URL remote repository | Cập nhật `CI_JOB_TOKEN` hoặc Personal Access Token |
| 64 | Lỗi `gRPC header size exceeded` trên K8s Executor | Log xuất ra console quá dài vượt mốc gRPC limit | Giảm bớt log in ra console hoặc ghi ra file artifact |
| 65 | SonarQube scan báo lỗi `Project key already exists` | Trùng lặp project key giữa 2 dự án khác nhau | Đặt unique `sonar.projectKey` cho từng dự án |
| 66 | Lỗi `SSL certificate problem: self signed certificate` | Tự dựng GitLab Server dùng CA Certificate tự ký | Khai báo `GIT_SSL_NO_VERIFY: "true"` hoặc nạp CA cert |
| 67 | Job bị hủy do vi phạm Policy Security Rule | Security scanner phát hiện lỗ hổng Critical/High | Cập nhật patch thư viện bị lỗi bảo mật |
| 68 | Lỗi `Connection timed out` khi kết nối Redis Service | Redis service chưa khởi động xong khi test app chạy | Thêm bước `sleep 3` hoặc wait-for-it script |
| 69 | Artifact bị ghi đè dữ liệu giữa các jobs | Trùng tên tệp artifact ở các stages khác nhau | Tách biệt tên thư mục output artifact cho từng stage |
| 70 | Lỗi `Kernel lockup` trên Runner Node Bare-metal | Máy chủ bị cạn kiệt Swap memory khi load cao | Khởi tạo thêm Swap file 8GB trên máy chủ |
| 71 | Lỗi `Failed to remove container` khi cleanup | Process con bên trong container bị zombie process | Cài đặt `tini` hoặc `init` process cho container |
| 72 | Vault secret fetch bị lỗi `Permission Denied` | AppRole / Token dùng trong CI bị hết hạn | Cấp renew token định kỳ trước khi đọc Secret Vault |
| 73 | Ansible playbook deploy bị lỗi `Unreachable host` | SSH Key không có quyền truy cập máy chủ Target | Nạp đúng Private Key vào `SSH_PRIVATE_KEY` variable |
| 74 | Lỗi `Cgroup v2 not supported` trên Linux kernel cũ | Runner executor chưa tương thích Cgroup v2 | Nâng cấp Linux Kernel lên 5.15+ hoặc Docker v20.10+ |
| 75 | Pipeline không tự động trigger khi push tag | Khai báo rule `only: tags` bị thiếu trong job | Sử dụng cú pháp `rules: - if: $CI_COMMIT_TAG` chuẩn v15+ |
| 76 | Lỗi `Dial tcp lookup failed` trong Runner Helper | DNS Server của Cloud Provider bị chập chờn | Đổi DNS fallback sang `8.8.8.8` hoặc `1.1.1.1` |
| 77 | Curl error `(35) OpenSSL SSL_connect` | TLS Cipher Suite của Runner Node quá cũ | Nâng cấp bản OpenSSL mới nhất trên Runner Node |
| 78 | Lỗi `Cannot allocation memory` khi fork process | Swap memory bị vô hiệu hóa hoàn toàn trên Host | Kích hoạt lại Swapfile với `swapon -a` |
| 79 | Docker-in-Docker báo `storage-driver overlay2 failed` | Linux Kernel chưa nạp module `overlay` | Nạp kernel module bằng `modprobe overlay` |
| 80 | Job bị treo ở bước `Preparing environment` | Docker daemon bị kẹt lock file khi pull base image | Khởi động lại Docker daemon `systemctl restart docker` |
| 81 | Lỗi `Invalid job name` trong YAML | Tên job chứa ký tự không hợp lệ hoặc trùng keyword | Đổi tên job không dính ký tự đặc biệt |
| 82 | Lỗi `Deploy key already in use` | SSH Deploy Key bị trùng lặp ở dự án khác | Tạo SSH Deploy Key riêng cho từng dự án |
| 83 | NPM publish báo `403 Forbidden` | NPM Auth Token thiếu scope write registry | Cấp lại NPM Token với quyền Publish |
| 84 | Lỗi `Corrupt zip archive` khi unpack Cache | Quá trình tải cache bị ngắt giữa chừng làm hỏng file | Xóa cache hỏng trên Object Storage |
| 85 | Python build báo `gcc: command not found` | Python slim image thiếu C compiler toolchain | Cài thêm `gcc build-essential` trước khi pip install |
| 86 | Lỗi `Container memory limit exceeded` trên K8s Pod | Pod limit RAM cài quá nhỏ so với nhu cầu app | Tăng `resources.limits.memory` trong Helm values |
| 87 | Lỗi `RPC failed; HTTP 413 curl 22 Init error` | Git buffer đẩy commit quá nhỏ khi push lớn | Tăng `git config http.postBuffer 524288000` |
| 88 | Vault agent sidecar không inject được token | Kubernetes ServiceAccount thiếu role binding Vault | Gán đúng Vault Auth Role cho ServiceAccount |
| 89 | Lỗi `Failed to connect to bus` khi dùng systemctl | Container Docker không có systemd làm PID 1 | Dùng `service` command hoặc chạy daemon trực tiếp |
| 90 | Pipeline bị hoãn chạy (Delayed) | Dự án bị áp dụng Rate Limit trigger pipeline | Tăng khoảng thời gian giữa các lần trigger pipeline |
| 91 | Lỗi `Cannot find module` trong Node build | Npm ci chưa cài đặt devDependencies | Kiểm tra biến `NODE_ENV` không đặt thành `production` |
| 92 | Lỗi `Toleration key not found` trên K8s Pod | Pod runner không schedule được vào worker node | Cấu hình toleration node taint trong Helm values |
| 93 | Lỗi `Git checkout detached HEAD` | GitLab Runner checkout theo SHA commit cụ thể | Dùng `git checkout $CI_COMMIT_REF_NAME` nếu cần branch |
| 94 | Lỗi `Shared memory space full` khi chạy Selenium | Shm_size mặc định 64MB của container quá nhỏ | Đặt `shm_size = 2147483648` (2GB) trong `config.toml` |
| 95 | Lỗi `No space left on device` trong `/tmp` | Thư mục `/tmp` dạng tmpfs bị đầy | Tăng dung lượng `/tmp` hoặc dùng thư mục đĩa thật |
| 96 | Pipeline fail do linting code style | Dev không chạy linter trước khi push commit | Sử dụng Git pre-commit hook kiểm tra tự động |
| 97 | Lỗi `HTTP 502 Bad Gateway` khi upload Artifact | Proxy Nginx đứng trước GitLab bị timeout | Tăng `client_max_body_size` và `proxy_read_timeout` |
| 98 | Lỗi `Elasticsearch cluster health red` trong test | Service container thiếu RAM để khởi động | Tăng `ES_JAVA_OPTS="-Xms512m -Xmx512m"` |
| 99 | Lỗi `Host key verification failed` khi rsync | SSH command thiếu `-o StrictHostKeyChecking=no` | Thêm option StrictHostKeyChecking=no |
| 100 | Lỗi `Docker login failed: Unencrypted password` | Docker daemon lưu password ở dạng plain text | Cấu hình Docker credential helper `pass` hoặc `secretservice` |
| 101 | Lỗi `Operation not permitted` khi mount loop device | Container thiếu Linux Capabilities | Thêm `cap_add = ["SYS_ADMIN"]` trong `config.toml` |
| 102 | Pipeline bị loop vô tận khi commit ngược CI | Job script tự động push commit mà không skip CI | Thêm chuỗi `[skip ci]` vào CI commit message |
| 103 | Lỗi `DB connection connection reset` khi integration test | DB Container bị restart giữa chừng | Tăng healthcheck grace period cho DB service |
| 104 | Cache bị bỏ qua (Cache miss) liên tục | Cache key chứa biến động thay đổi mỗi commit | Đổi cache key sang tệp hash `checksum lock file` |
| 105 | Lỗi `System clock skewed` khi make project | Giờ hệ thống file mtime muộn hơn giờ máy chủ | Chạy `touch -m` đồng bộ lại thời gian tệp tin |
| 106 | Lỗi `Git push rejected` do lỡ rebase nhánh chính | Branch protected chặn force push | Tắt temporary force push protection hoặc tạo MR |
| 107 | Lỗi `Curl 56 Recv failure: Connection reset` | Proxy chặn gói tin HTTPS truyền qua | Cấu hình `HTTP_PROXY` và `HTTPS_PROXY` đúng địa chỉ |
| 108 | Container fail với `exec user process caused: exec format error` | Biên dịch binary x86_64 nhưng chạy trên ARM64 (Mac M1/M2) | Dùng Docker `--platform linux/amd64` hoặc cross compile |
| 109 | Lỗi `Docker daemon out of disk inodes` | Ổ đĩa còn dung lượng dung lượng byte nhưng hết inodes | Xóa bớt file nhỏ rác bằng `find . -type f -delete` |
| 110 | Artifact download bị lỗi `checksum validation failed` | File artifact bị hỏng trong quá trình truyền qua S3 | Bật cờ retry upload/download trong `config.toml` |
| 111 | Lỗi `Vault token lookup permission denied` | Vault token bị thu hồi trước khi job kết thúc | Tăng TTL cho Vault Token trong Vault AppRole |
| 112 | NPM build fail với `ENOSPC: System limit for number of file watchers reached` | Inotify file watcher limit của OS quá thấp | Tăng `fs.inotify.max_user_watches=524288` trong sysctl |
| 113 | Lỗi `Postgres fatal: too many connections` | Integration test khởi tạo quá nhiều connection pool | Giới hạn max connection pool trong ứng dụng test |
| 114 | Lỗi `Maven plugin execution failure` do sai Java version | Base image cài JDK 8 nhưng code yêu cầu JDK 17 | Đổi base image CI sang `maven:3.8-openjdk-17` |
| 115 | Lỗi `Python setup.py egg_info failed` | Thiếu package `wheel` hoặc `setuptools` mới | Lệnh `pip install --upgrade pip setuptools wheel` |
| 116 | Lỗi `Docker login 401 Unauthorized` | CI Secret Token hết hạn hoặc nhập sai username | Cập nhật lại `CI_REGISTRY_PASSWORD` |
| 117 | Lỗi `Kubernetes namespace stuck in Terminating` | Còn Finalizer chưa được xóa trong K8s resources | Xóa thủ công finalizer trong kubectl edit ns |
| 118 | Lỗi `Runner registration token deprecated` | GitLab 16.0+ ngừng hỗ trợ registration token cũ | Chuyển sang dùng Runner Authentication Token mới |
| 119 | Lỗi `Git push default branch rejected` | Cấu hình Default Branch bị khóa ghi trực tiếp | Tạo Merge Request thay vì push trực tiếp |
| 120 | Lỗi `Linux Kernel panic` khi chạy stress test | Runner Node bị quá tải CPU/Memory phần cứng | Giới hạn số job song song bằng `concurrent = 4` |

---

## 4. Bài tập mở rộng (10 phút)

### 4.1. Bài tập 1: Xây dựng Kịch bản Tự động Chẩn đoán Lỗi Exit Code 137 & Tự nâng RAM
Yêu cầu học viên viết một bash script chẩn đoán tự động `/usr/local/bin/auto-oom-fix.sh` có khả năng:
1. Đọc file log của job vừa thất bại.
2. Nếu phát hiện `Exit Code 137` hoặc chuỗi `OOMKilled`, tự động đọc giá trị RAM limit hiện tại trong `config.toml`.
3. Tăng mức RAM limit từ `2g` lên `4g` và gửi cảnh báo Slack tới kênh DevOps On-call.

```bash
# Code gợi ý cho bài tập 1
cat << 'EOF' > /tmp/lab-buoi-47/auto-oom-fix.sh
#!/bin/bash
LOG_FILE="$1"
CONFIG_FILE="/etc/gitlab-runner/config.toml"

if grep -qE "Exit Code 137|OOMKilled|Out of memory" "$LOG_FILE"; then
    echo "[ALERT] Phát hiện sự cố OOM Exit Code 137!"
    echo "[ACTION] Đang tự động tăng memory_limit trong $CONFIG_FILE từ 2g lên 4g..."
    sed -i 's/memory = "2g"/memory = "4g"/g' "$CONFIG_FILE"
    systemctl reload gitlab-runner
    echo "[SUCCESS] Đã nâng RAM limit lên 4g và reload Runner thành công."
fi
EOF
chmod +x /tmp/lab-buoi-47/auto-oom-fix.sh
```

### 4.2. Bài tập 2: Thiết lập Hệ thống Monitoring Cảnh báo MTU Mismatch & DNS Timeout
Yêu cầu học viên viết một daemon script chạy trên Runner Host thực hiện kiểm tra healthcheck mạng định kỳ 5 phút:
- Gửi gói tin ICMP với kích thước 1450 bytes mang cờ `Don't Fragment` tới Gateway.
- Truy vấn thử nghiệm DNS 8.8.8.8 và DNS nội bộ. Nếu latency $> 500\text{ms}$ hoặc bị drop packet, tự động ghi thông báo vào `/var/log/runner-network-health.log`.

```bash
# Code gợi ý cho bài tập 2
cat << 'EOF' > /tmp/lab-buoi-47/network-healthcheck.sh
#!/bin/bash
LOG="/var/log/runner-network-health.log"
GATEWAY=$(ip route show default | awk '{print $3}')

# Kiểm tra ping ICMP packet 1450 bytes
if ! ping -M do -s 1422 -c 3 "$GATEWAY" > /dev/null 2>&1; then
    echo "$(date): [WARNING] Phát hiện nghẽn mạng do MTU packet truncation tại Gateway $GATEWAY!" >> "$LOG"
fi

# Kiểm tra DNS latency
LATENCY=$(dig @8.8.8.8 registry.gitlab.com | grep "Query time" | awk '{print $4}')
if [ "$LATENCY" -gt 500 ]; then
    echo "$(date): [WARNING] DNS Query time quá cao: ${LATENCY}ms" >> "$LOG"
fi
EOF
chmod +x /tmp/lab-buoi-47/network-healthcheck.sh
```

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| 1 | Yêu cầu môi trường & Thiết lập ban đầu | 15 phút |
| 2 | Các kịch bản thực hành (Checkpoint 1-8) | 120 phút |
| 3 | Xử lý sự cố (120+ tình huống thực tế) | 15 phút |
| 4 | Bài tập mở rộng | 10 phút |
| **Tổng** | **Khối thực hành** | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

## Khối Vấn đáp & Phỏng vấn — 20 phút

---

## §V1. Bộ câu hỏi Vấn đáp Trực tiếp (12 Câu)

### Câu 1
**Hỏi:** Khi một job trong GitLab CI bị đỏ thất bại với thông báo chung chung `Command exited with code 1` mà log console hoàn toàn không hiển thị dòng code gây lỗi nào, bước đầu tiên bạn sẽ làm gì để truy vết sự cố?

**Đáp án chuẩn:**
Bước đầu tiên và chuẩn mực nhất là bật cờ `CI_DEBUG_TRACE: "true"` trực tiếp trong phần `variables` của job bị lỗi trong `.gitlab-ci.yml`. 
- Cờ này sẽ buộc Runner Engine bật chế độ `set -x` trên Shell Executor, in ra từng dòng lệnh được mở rộng, các phép gán biến môi trường, và các rẽ nhánh điều kiện `if/else` trước khi thực thi.
- **Chi tiết kỹ thuật sâu:** Khi `CI_DEBUG_TRACE` hoạt động, mỗi dòng lệnh shell trước khi thực thi sẽ được prefix bởi dấu `+` kèm theo giá trị mở rộng thực sự của biến. Ví dụ: `+ curl -u admin:secret123 https://api.internal/deploy`. Nhờ đó, bạn sẽ phát hiện ra các biến bị rỗng (`""`), các lỗi cú pháp ẩn, hoặc câu lệnh bị thất bại ở rẽ nhánh nào.
- **Quy trình xử lý sự cố:**
  1. Thêm `variables: { CI_DEBUG_TRACE: "true" }` vào job bị lỗi.
  2. Kích hoạt `Retry` job trên giao diện GitLab CI.
  3. Phân tích log chi tiết tại vị trí xuất hiện lỗi `exit code 1`.
  4. Sửa lỗi logic hoặc cấu hình.
  5. Xóa bỏ cờ debug khỏi file cấu hình trước khi merge vào nhánh chính.
- **Lưu ý bảo mật nghiêm ngặt:** Vì `CI_DEBUG_TRACE` sẽ in ra toàn bộ giá trị các biến môi trường (kể cả biến chưa được masked hoặc các secret nạp từ HashiCorp Vault), sau khi hoàn tất debug phải lập tức xóa cờ này khỏi repo, hủy kết quả pipeline trace, và xóa các phiên log nhạy cảm để tránh rò rỉ token/mật khẩu theo quy tắc buổi 47 QT 47.1.

---

### Câu 2
**Hỏi:** Làm thế nào để bạn phân biệt được một job bị crash do vượt hạn mức bộ nhớ RAM (Out of Memory - Exit Code 137) với một lỗi ứng dụng thông thường (Exit Code 1)?

**Đáp án chuẩn:**
- **Về Exit Code:** Lỗi OOM trong Linux container luôn trả về `Exit Code 137` ($128 + 9$), tương ứng với việc tiến trình bị Linux Kernel OOM Killer gửi tín hiệu `SIGKILL` (signal 9) tiêu diệt cưỡng chế. Lỗi ứng dụng thông thường sẽ trả về `Exit Code 1` hoặc các mã lỗi logic do lập trình viên định nghĩa.
- **Về Log Hệ thống:** Log console của job bị OOM thường ngắt đột ngột giữa chừng khi ứng dụng đang nạp dữ liệu lớn (như compile Java/Rust hoặc npm build) mà không có stack trace hay thông báo lỗi ứng dụng nào.
- **Bước xác minh chính xác:** Đăng nhập vào máy chủ Runner Host và kiểm tra Kernel Buffer bằng lệnh `dmesg -T | grep -i oom` hoặc `journalctl -u docker`. Nếu thấy dòng `Memory cgroup out of memory: Killed process <PID>` thì khẳng định 100% do OOM.
- **Giải pháp xử lý:** Nâng `memory` limit trong `config.toml` của Runner (ví dụ `memory = "4g"`), cấp thêm `memory_swap = "2g"`, hoặc tối ưu heap size (như `-Xmx` của Java hay `--max-old-space-size` của Node.js) để khống chế bộ nhớ ứng dụng theo quy tắc buổi 47 QT 47.2.

---

### Câu 3
**Hỏi:** Bạn gặp sự cố job runner build Docker image bị treo vô hạn ở bước `Connecting to registry.gitlab.com...` hoặc `TLS Handshake`. Kiểm tra `ping` vẫn thấy thông mạng nhưng curl bị đứng. Nguyên nhân gốc rễ và cách khắc phục là gì?

**Đáp án chuẩn:**
- **Nguyên nhân gốc rễ:** Đây là sự cố điển hình do lệch kích thước MTU (Maximum Transmission Unit) giữa mạng ảo Docker Bridge (`docker0` mặc định là 1500 bytes) và card mạng vật lý của Host/Cloud VPC (ví dụ AWS EC2 VXLAN MTU là 1450 bytes hoặc Google Cloud MTU 1460). Khi truyền các gói tin TLS Certificate handshake có dung lượng lớn, gói tin bị vượt quá MTU của Cloud Gateway nhưng lại mang cờ DF (Don't Fragment), khiến gateway âm thầm loại bỏ gói tin (packet drop) dẫn đến kết nối bị treo vô hạn.
- **Phân tích kỹ thuật:** Gói ICMP Ping nhỏ ($64$ bytes) sẽ vượt qua dễ dàng, nhưng gói TLS Hello ($>1400$ bytes) mang chứng chỉ X.509 kèm cờ DF sẽ bị sập. Lệnh `curl` đứng yên ở giai đoạn `SSL connection flag`.
- **Cách khắc phục:** Cấu hình ép MTU của Docker Network về giá trị 1450 bytes bằng cách thêm cờ `mtu = 1450` vào file `/etc/gitlab-runner/config.toml` dưới mục `[runners.docker]`, hoặc cấu hình daemon `/etc/docker/daemon.json` với `"mtu": 1450` rồi khởi động lại Docker Engine theo quy tắc buổi 47 QT 47.3.

---

### Câu 4
**Hỏi:** Tại sao không nên đặt cấu hình Cache Key cố định dạng `key: "global-build-cache"` cho tất cả các nhánh trong dự án? Cách đặt Cache Key chuẩn sản xuất là gì?

**Đáp án chuẩn:**
- **Tác hại khi dùng Cache Key cố định:** Đặt cache key cố định làm cho tất cả các pipeline trên nhánh `main`, `feature`, `hotfix` và các Merge Request xài chung một tệp nén cache trên Object Storage. Khi nhánh feature cập nhật thư viện mới hoặc cài bản thử nghiệm, tệp cache bị đè (overwrite). Nhánh `main` chạy sau đó sẽ nạp cache hỏng hoặc không tương thích, dẫn đến hàng loạt pipeline bị đỏ dây chuyền.
- **Cấu hình Cache Key chuẩn sản xuất:**
  1. Phân lập cache theo nhánh: `key: "$CI_COMMIT_REF_SLUG"` đảm bảo nhánh nào dùng cache nhánh đó.
  2. Phân lập cache theo file lock dependency: `key: { files: ["package-lock.json", "go.sum", "Pom.xml"] }` giúp cache chỉ được xây dựng lại khi có thay đổi thực sự về thư viện.
  3. Phiên bản hóa cache key: `key: "$CI_COMMIT_REF_SLUG-v1"` để dễ dàng xoá sạch cache cũ bằng cách bump version khi gặp sự cố theo quy tắc buổi 47 QT 47.4.

---

### Câu 5
**Hỏi:** Kỹ thuật Live Debugging trực tiếp trên Runner container bằng `tmate` hoạt động như thế nào? Khi nào bạn nên áp dụng kỹ thuật này?

**Đáp án chuẩn:**
- **Cơ chế hoạt động:** `tmate` là công cụ tạo phiên SSH tunnel ngược (reverse SSH). Khi job CI chạy đến bước kích hoạt `tmate`, nó sẽ cài đặt và khởi chạy một daemon `tmate` kết nối tới tmate server, sau đó in ra một URL SSH công khai (hoặc SSH nội bộ) lên console log của GitLab CI rồi tạm dừng job (bằng lệnh `sleep`).
- **Cách truy cập:** SRE copy dòng lệnh `ssh user@tmate.io:...` trên console log, dán vào terminal cá nhân để bay thẳng vào bên trong container đang chạy trên Runner. Tại đây, SRE có thể chạy thử từng câu lệnh, kiểm tra file system, cài đặt `netstat`, `strace` để tìm nguyên nhân lỗi.
- **Khi nào áp dụng:** Áp dụng khi gặp các lỗi hợm hĩnh chỉ xuất hiện trên môi trường Runner mà không thể tái hiện ở Local, giúp tránh việc phải push 20–30 commit rác để "debug bằng log print" theo quy tắc buổi 47 QT 47.5.

---

### Câu 6
**Hỏi:** Khi cấu hình Docker-in-Docker (DinD) trong GitLab CI với `image: docker:24.0.5` và `services: - docker:24.0.5-dind`, job báo lỗi `Cannot connect to the Docker daemon at tcp://docker:2375. Is the docker daemon running?`. Bạn khắc phục lỗi này như thế nào?

**Đáp án chuẩn:**
- **Nguyên nhân gốc rễ:** Từ phiên bản Docker 19.03+, dịch vụ DinD bật kết nối TLS mã hóa mặc định trên port 2376 thay vì port 2375 unencrypted. Nếu không khai báo chứng chỉ TLS mã hóa chia sẻ giữa container client và service dind, client sẽ cố kết nối vào port 2375 bị từ chối hoặc sai cổng.
- **Cách khắc phục chuẩn:**
  1. Khai báo biến môi trường TLS chung trong `.gitlab-ci.yml`:
     ```yaml
     variables:
       DOCKER_HOST: "tcp://docker:2376"
       DOCKER_TLS_CERTDIR: "/certs"
       DOCKER_TLS_VERIFY: 1
       DOCKER_CERT_PATH: "$DOCKER_TLS_CERTDIR/client"
     ```
  2. Hoặc nếu muốn tắt TLS trong môi trường Lab nội bộ bảo mật:
     ```yaml
     variables:
       DOCKER_HOST: "tcp://docker:2375"
       DOCKER_TLS_CERTDIR: ""
     ```
  Áp dụng theo đúng quy tắc buổi 47 QT 47.6.

---

### Câu 7
**Hỏi:** Vì sao job CI chạy câu lệnh ghi file ra mount volume lại báo lỗi `Permission denied` dù container đang chạy dưới quyền user `node` hay `appuser`?

**Đáp án chuẩn:**
- **Nguyên nhân gốc rễ:** Đây là sự cố sai lệch UID/GID (User ID / Group ID) giữa Linux Host và Container. Khi Runner mount thư mục workspace (`$CI_PROJECT_DIR`) từ host vào container, thư mục trên host thuộc sở hữu của UID 999 (`gitlab-runner`). Nếu container chạy bằng non-root user có UID 1000 (`node`), OS Kernel sẽ chặn quyền ghi file.
- **Cách khắc phục:** 
  1. Trong `Dockerfile`, đảm bảo tạo user với UID/GID trùng khớp với môi trường CI hoặc thiết lập lại phân quyền trong `before_script`.
  2. Sử dụng lệnh `chown -R $(id -u):$(id -g) $CI_PROJECT_DIR` ở bước khởi động hoặc chạy container với cờ `--user root` nếu bắt buộc, theo quy tắc buổi 47 QT 47.7.

---

### Câu 8
**Hỏi:** Giải thích hiện tượng Job CI bị treo vô hạn (Hanging Job) ở bước cuối cùng mặc định cho đến khi bị timeout 60 phút, dù script chính đã thực thi xong. Nguyên nhân ngầm là gì và xử lý ra sao?

**Đáp án chuẩn:**
- **Nguyên nhân ngầm:** Khi script CI khởi chạy một tiến trình ngầm (background daemon) như Web Server thử nghiệm, Redis, hoặc Log Tailer bằng lệnh `my-daemon &`, tiến trình con này thừa kế các File Descriptors ngõ ra STDOUT và STDERR của tiến trình cha (Runner Shell). Mặc dù script cha đã `exit 0`, nhưng Runner Engine vẫn thấy ngõ ra STDOUT/STDERR pipe chưa được đóng, nên nó kiên nhẫn đứng chờ vô hạn.
- **Cách xử lý:** Luôn luôn chuyển hướng toàn bộ ngõ ra I/O của tiến trình ngầm vào `/dev/null` hoặc file log riêng và cắt đứt liên kết bằng `nohup`:
  `nohup my-daemon > /dev/null 2>&1 &`
  Cách làm này giúp đóng tức thì STDOUT/STDERR pipe, cho phép Runner kết thúc job thành công theo quy tắc buổi 47 QT 47.8.

---

### Câu 9
**Hỏi:** Ổ đĩa máy chủ Runner Host bị tràn 100% (`No space left on device`) gây sập dây chuyền toàn bộ CI/CD. Bạn thiết lập cơ chế tự động phòng vệ và dọn dẹp đĩa như thế nào?

**Đáp án chuẩn:**
- **Nguyên nhân tích tụ:** Runner sử dụng Docker Executor tích tụ hàng trăm Gigabyte dơ bẩn từ: Docker image layer rác, dangling build cache, container volume tạm bị vô chủ, và build artifacts cũ.
- **Cơ chế phòng vệ chuẩn SRE:**
  1. Cấu hình Cronjob dọn dẹp tự động hàng đêm trên máy chủ Runner Host (`/etc/cron.d/gitlab-runner-clean`):
     `0 3 * * * root /usr/bin/docker system prune -af --filter "until=48h" --volumes > /var/log/docker-prune.log 2>&1`
  2. Cấu hình cờ `clear_untagged = true` và `gsi = true` trong `config.toml` dưới mục `[runners.docker]`.
  3. Cài đặt cảnh báo Prometheus Alertmanager khi `node_filesystem_free_bytes / node_filesystem_size_bytes < 0.15` (dưới 15% đĩa trống) theo quy tắc buổi 47 QT 47.9.

---

### Câu 10
**Hỏi:** Tại sao sự cố lệch giờ NTP giữa các node máy chủ Runner lại có thể khiến pipeline bị lỗi artifact không tìm thấy hoặc cache bị bỏ qua (cache miss)?

**Đáp án chuẩn:**
- **Tác hại của lệch giờ:** Các hệ thống phân tán như GitLab CI, S3 Object Storage (MinIO/AWS S3) và Git đều phụ thuộc vào mốc thời gian Unix Timestamp để xác định độ tươi (freshness) của file. Khi Runner Node A (chạy job build) có giờ nhanh hơn Runner Node B (chạy job deploy) 5 phút:
  1. File artifact do Node A tạo ra mang mốc `mtime` ở tương lai so với Node B. Khi Node B tải artifact về, lệnh `make` hoặc `tar` phát hiện timestamp ở tương lai sẽ bỏ qua không compile hoặc báo lỗi file corrupt.
  2. Amazon S3 từ chối yêu cầu HTTP request với lỗi `RequestTimeTooSkewed` nếu lệch giờ quá 15 phút.
- **Cách khắc phục:** Cài đặt và bật dịch vụ đồng bộ thời gian `chrony` hoặc `systemd-timesyncd` trên toàn bộ máy chủ Runner Node, đảm bảo độ lệch thời gian $\Delta t < 100\text{ms}$ theo quy tắc buổi 47 QT 47.10.

---

### Câu 11
**Hỏi:** Khi một ứng dụng C++/Go/Rust compiled binary bị crash ngầm (silent exit code 1) mà không in ra bất kỳ dòng log nào ra console, làm thế nào bạn dùng `strace` để tìm ra nguyên nhân gốc rễ?

**Đáp án chuẩn:**
- **Cách thực hiện:** Bọc câu lệnh thực thi tệp binary bằng công cụ theo dõi system calls `strace`:
  `strace -f -e trace=file,network -o trace.log ./my-binary-app`
- **Phân tích kết quả:**
  1. Đọc file `trace.log` và tìm kiếm các system call trả về mã lỗi `ENOENT (No such file or directory)`. Ví dụ: `openat(AT_FDCWD, "/etc/app/config.json", O_RDONLY) = -1 ENOENT`. Dòng này tiết lộ ứng dụng bị crash do không tìm thấy file cấu hình bị thiếu.
  2. Kiểm tra các lỗi `EACCES (Permission denied)` hoặc `ECONNREFUSED` để phát hiện lỗi thiếu quyền đọc file socket hoặc không kết nối được database theo quy tắc buổi 47 QT 47.11.

---

### Câu 12
**Hỏi:** Hãy mô tả quy trình 5 bước khắc phục sự cố (Troubleshooting Framework) chuẩn mực mà bạn áp dụng khi đối mặt với một sự cố CI/CD khẩn cấp trong doanh nghiệp.

**Đáp án chuẩn:**
Quy trình 5 bước chuẩn SRE (buổi 47 QT 47.12):
1. **Bước 1 — Thu thập chứng cứ (Gather Evidence):** Đọc log console, lấy Exit Code, bật `CI_DEBUG_TRACE: "true"`, đọc `dmesg` trên host và kiểm tra thông số hệ thống (CPU, RAM, Disk, Network).
2. **Bước 2 — Phân lập phạm vi (Isolate Scope):** Xác định lỗi thuộc về Code ứng dụng, Cấu hình Pipeline `.gitlab-ci.yml`, Môi trường Container Image, hay Hạ tầng Runner Host.
3. **Bước 3 — Tái hiện lỗi (Reproduce):** Chạy lại job với Debug log hoặc dùng `tmate` bay vào container tái hiện câu lệnh thủ công.
4. **Bước 4 — Áp dụng giải pháp tối thiểu (Minimal Fix):** Đưa ra bản vá sửa đúng nguyên nhân gốc rễ, thử nghiệm trên nhánh test trước khi apply lên `main`.
5. **Bước 5 — Đóng vòng lặp & Củng cố (Post-Mortem & Prevent):** Cập nhật tài liệu Runbook, thêm rule linter/monitoring cảnh báo tự động để sự cố không bao giờ lặp lại.

---

## §V2. Kịch bản Đóng vai Thực tế (Roleplay Scenarios)

### Kịch bản 1: Thư viện code bị đè Cache làm sập nhánh Production
- **Bối cảnh:** Lập trình viên Junior vừa push commit lên nhánh `feature/experiment` có hạ cấp phiên bản thư viện `lodash` xuống v3.0. Nhánh `main` chạy pipeline 10 phút sau đó bị crash toàn bộ giao diện vì nạp phải cache hỏng của nhánh feature. Trưởng phòng kĩ thuật gọi bạn vào họp gấp.
- **Lời thoại của bạn:**
  > "Báo cáo anh, em đã tìm ra nguyên nhân gốc rễ. Pipeline của chúng ta đang dùng chung một Cache Key cố định `key: npm-cache` cho toàn bộ các nhánh. Khi nhánh feature chạy, nó đã nạp bản lodash v3.0 và đè lên tệp cache chung trên MinIO S3. Nhánh `main` build sau đó đã kéo nhầm cache hỏng này về.
  > 
  > Em xử lý ngay theo 2 bước:
  > 1. Xóa thủ công tệp cache hỏng trên MinIO và bump phiên bản cache key trong `.gitlab-ci.yml` lên `key: $CI_COMMIT_REF_SLUG-v2` để khôi phục pipeline nhánh `main` ngay lập tức.
  > 2. Đổi lại chiến lược Cache Key theo quy tắc buổi 47 QT 47.4, phân lập cache theo từng nhánh `$CI_COMMIT_REF_SLUG` và khóa theo hash của file `package-lock.json`. Từ giờ nhánh feature thử nghiệm sẽ không bao giờ có thể làm ảnh hưởng tới nhánh Production nữa."

---

### Kịch bản 2: Giải trình sự cố OOM Exit Code 137 với CTO
- **Bối cảnh:** CTO nhận được email báo động pipeline build bản cập nhật sản phẩm bị fail liên tục 5 lần với mã lỗi 137. CTO nghi ngờ máy chủ GitLab CI bị dính mã độc hoặc dev viết code làm rò rỉ bộ nhớ nghiêm trọng.
- **Lời thoại của bạn:**
  > "Thưa anh, em đã đăng nhập vào Runner Host và trích xuất log Kernel từ `dmesg`. Dòng vết hệ thống khẳng định 100% tiến trình compile Java Maven đã bị Linux OOM Killer tiêu diệt do vượt hạn mức RAM Cgroup limit 2GB được thiết lập trong `config.toml`. Code ứng dụng không bị rò rỉ bộ nhớ, mà do bản cập nhật mới bổ sung thêm các module nặng khiến lượng RAM đỉnh (peak RAM) tăng lên 2.8GB.
  > 
  > Em đã áp dụng quy tắc buổi 47 QT 47.2:
  > 1. Điều chỉnh hạn mức `memory = "4g"` và cấp thêm `memory_swap = "2g"` trong cấu hình Runner.
  > 2. Cấu hình biến `MAVEN_OPTS: "-Xmx3072m"` để khống chế JVM không ăn RAM vượt quá hạn mức container.
  > Pipeline hiện tại đã verde (xanh) trở lại và thời gian build giảm 20%."

---

### Kịch bản 3: Sửa lỗi nghẽn mạng TLS Handshake trên AWS Cloud
- **Bối cảnh:** Nhóm Cloud DevOps vừa chuyển các Runner từ On-premise lên AWS EC2 VPC. Tất cả các job build Docker image sử dụng DinD đều bị treo cứng 60 phút ở bước `docker pull` base image. Dev kêu than CI/CD mới quá chậm và chập chờn.
- **Lời thoại của bạn:**
  > "Anh em yên tâm, đây không phải do đường truyền AWS chậm mà là sự cố nghẽn mạng do lệch MTU Packet Truncation. Card mạng vật lý AWS EC2 VPC sử dụng chuẩn VXLAN với MTU là 1450 bytes, trong khi Docker Bridge mặc định tạo ra card veth với MTU 1500 bytes. Các gói tin trao đổi chứng chỉ TLS Certificate khi `docker pull` có kích thước lớn bị vượt quá MTU nên bị AWS Gateway âm thầm thả (drop packet).
  > 
  > Em đã xử lý theo quy tắc buổi 47 QT 47.3: Cập nhật cờ `mtu = 1450` vào phần cấu hình `[runners.docker]` trong `/etc/gitlab-runner/config.toml` và restart runner service. Tốc độ kéo image hiện tại đã đạt full băng thông 1Gbps và không còn một job nào bị treo."

---

### Kịch bản 4: Xử lý sự cố Runner dính tràn đĩa 100% vào nửa đêm
- **Bối cảnh:** Lúc 2h sáng, hệ thống giám sát PagerDuty kích hoạt báo động khẩn cấp: 50 pipeline đang pending vì đĩa máy chủ Runner bị lấp đầy 100%. Đội On-call hoảng loạn muốn restart lại toàn bộ máy chủ.
- **Lời thoại của bạn:**
  > "Đừng restart máy chủ vội vì restart sẽ không giải phóng được đĩa Docker layer bị kẹt! Hãy thực hiện theo đúng Runbook SRE:
  > 1. Đăng nhập vào Runner Host và chạy lệnh `docker system prune -af --volumes` để ngay lập tức thu hồi 120GB dung lượng từ các image layer và container volume bị mồ côi.
  > 2. Kiểm tra lại `/etc/cron.d/gitlab-runner-clean` để đảm bảo cronjob dọn dẹp tự động hàng đêm đang chạy đúng giờ.
  > 3. Cập nhật file `/etc/gitlab-runner/config.toml` thêm cờ `clear_untagged = true` và `gsi = true` theo quy tắc buổi 47 QT 47.9 để các job sau tự dọn dẹp rác ngay sau khi hoàn thành."

---

### Kịch bản 5: Khắc phục lỗi lệch giờ NTP gây hỏng Artifacts phân tán
- **Bối cảnh:** Nhóm Backend phàn nàn rằng các job Deploy trên Runner Node B thường xuyên báo lỗi `Artifact file not found or timestamp in the future` mặc dù job Build trên Runner Node A vừa thông báo tạo thành công artifact cách đó 1 phút.
- **Lời thoại của bạn:**
  > "Nguyên nhân do độ lệch thời gian NTP giữa Node A và Node B. Node A có đồng hồ chạy nhanh hơn Node B đúng 3 phút. Khi Node A nén artifact, mốc thời gian `mtime` của file được ghi nhận ở tương lai so với Node B. Khi Node B tải về giải nén, bộ giải nén phát hiện thời gian bất thường nên từ chối xử lý.
  > 
  > Em đã áp dụng quy tắc buổi 47 QT 47.10: Kích hoạt dịch vụ `chronyd` đồng bộ giờ chuẩn NTP Server qua lệnh `systemctl enable --now chronyd` trên cả 2 node. Độ lệch hiện tại đã về 0.2ms và lỗi artifact biến mất hoàn toàn."

---

### Kịch bản 6: Truy vết ngầm Silent Crash ứng dụng compiled C++/Rust
- **Bối cảnh:** Nhóm kỹ sư Embedded/Core C++ gặp sự cố ứng dụng build binary chạy trong job CI bị dừng đột ngột với `exit code 1` mà không in bất kỳ dòng log nào ra STDOUT/STDERR. Cả đội loay hoay 2 ngày không tìm ra nguyên nhân.
- **Lời thoại của bạn:**
  > "Mọi người đừng đoán mò nữa, hãy sử dụng `strace` để xem trực tiếp các system call mà hệ điều hành nhận được từ binary! Em đã bọc câu lệnh chạy ứng dụng bằng `strace -f -e trace=file,network -o trace.log ./app-binary`.
  > 
  > Kết quả file log chỉ ra ngay lập tức: Ở dòng 452, binary thực hiện `openat(AT_FDCWD, "/etc/ssl/certs/ca-certificates.crt", O_RDONLY) = -1 ENOENT`. Ứng dụng bị crash vì thiếu file chứng chỉ CA trong container alpine siêu nhẹ. Em bổ sung `apk add --no-cache ca-certificates` vào Dockerfile và ứng dụng đã chạy mượt mà theo đúng quy tắc buổi 47 QT 47.11."

---

## §V3. Câu chốt để nói khi phỏng vấn

> **"Kinh nghiệm xương máu của tôi sau nhiều năm vận hành hạ tầng CI/CD quy mô lớn là: Debugging CI/CD không phải là đoán mò hay push commit thử nghiệm liên tục. 90% sự cố hợm hĩnh nhất trong pipeline — từ Exit Code 137 OOM, treo kẹt TLS Handshake do MTU, cho đến dính nạp cache hỏng hay hổng socket DinD — đều có dấu vết rõ ràng trong Kernel dmesg, verbose trace log và system calls strace. Người kỹ sư DevOps giỏi là người biết làm chủ cờ `CI_DEBUG_TRACE`, biết bật phiên live terminal `tmate` đúng lúc, và luôn thiết lập cơ chế tự động phòng vệ hạ tầng đĩa/giờ NTP để hệ thống tự chữa lành trước khi người dùng phát hiện ra lỗi."**

---

## §V4. Bài tập về nhà (BTVN) chuẩn bị cho Buổi 48

### BTVN 1: Xây dựng Runbook Khắc phục Sự cố Pipeline tự động
Viết tệp tài liệu `RUNBOOK-TROUBLESHOOTING-CI.md` lưu trữ trong repository của công ty, tổng hợp 20 kịch bản lỗi phổ biến nhất cùng câu lệnh một dòng (one-liner) để SRE trực ca xử lý nhanh trong vòng 3 phút.

### BTVN 2: Cấu hình Alerting Monitoring cho GitLab Runner Cluster
Viết tệp cấu hình Prometheus Alert Rules (`runner-alerts.yml`) bắt các sự cố:
- Runner Disk Space $< 15\%$.
- Job Failure Rate $> 20\%$ trong 15 phút.
- Runner Node Clock Drift $> 100\text{ms}$.

### BTVN 3: Viết Script Tự động Phân tích Log CI bằng Python
Viết script `analyze-ci-log.py` đọc tệp log console đầu ra của GitLab CI, tự động nhận diện pattern lỗi (Regex matching) và in ra đề xuất cách khắc phục chuẩn theo 12 Quy tắc `QT 47.1` đến `QT 47.12`.

### BTVN 4: Chuẩn bị kiến thức cho Buổi 48 (Tổng kết & Đồ án Capstone)
Đọc trước tài liệu Buổi 48 về **"Tổng kết Toàn bộ Khóa học & Bảo vệ Đồ án Capstone CI/CD Production"**. Chuẩn bị sơ đồ kiến trúc tổng thể kết hợp đầy đủ các thành phần: GitLab CI, Dynamic Runner Auto-scaling, Cache Server S3, Security Scanning (SAST/DAST), Release Strategy (Canary/Blue-Green), Terraform IaC, và Troubleshooting Framework.