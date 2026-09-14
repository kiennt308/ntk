---
layout: post
title: "[Bài 02] GitLab Runner & Các Loại Executor: Shell, Docker, Kubernetes Executor & Cơ Chế Đăng Ký Token Mới"
date: 2026-09-12 09:20:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-02
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 2
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.02] Phân tích chuyên sâu kiến trúc GitLab Runner & các loại Executor: Shell, Docker, Kubernetes, giải mã cơ chế phân chia trách nhiệm giữa .gitlab-ci.yml và config.toml, tối ưu hóa concurrent/limit và cơ chế xác thực Authentication Token mới."
tldr:
  - "Nắm vững nguyên lý hai tệp cấu hình: .gitlab-ci.yml (Job làm gì) và config.toml (Job chạy ở đâu và với quyền gì)."
  - "Phân loại 4 loại Executor trên trục cô lập: Shell (0 cô lập), Docker (cô lập hệ tệp), Kubernetes (cô lập tài nguyên) và Custom."
  - "Nhận diện rủi ro bảo mật nghiêm trọng khi mount Docker Socket (/var/run/docker.sock) vào Runner Container."
  - "Kiểm soát 3 điều kiện độc lập để Runner nhận Job và phương pháp đo đạc chống nghẽn hàng đợi (Queue Latency vs Execution Duration)."
---
{% raw %}
# [BÀI 02] GITLAB RUNNER & CÁC LOẠI EXECUTOR: SHELL, DOCKER, KUBERNETES EXECUTOR & CƠ CHẾ ĐĂNG KÝ TOKEN MỚI

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

### 1.1. Luận Đề Hai Tệp Cấu Hình: Ranh Giới Giữa Pipeline & Hạ Tầng
Một Job CI/CD trong thực tế luôn được chi phối bởi **HAI TỆP CẤU HÌNH** do hai vai trò kỹ thuật khác nhau đảm nhiệm:
1. **`.gitlab-ci.yml` (Người viết Pipeline):** Xác định Job *LÀM GÌ* (câu lệnh `script`, image yêu cầu, artifacts cần giữ lại, điều kiện `rules`).
2. **`config.toml` (Người vận hành Runner / Platform Engineer):** Xác định Job *CHẠY Ở ĐÂU VÀ VỚI QUYỀN GÌ* (loại Executor, thư mục volume mount, phân bổ CPU/RAM, hạn mức `concurrent`, cấu hình mạng).

```yaml
  NGƯỜI VIẾT PIPELINE                          NGƯỜI VẬN HÀNH RUNNER
  .gitlab-ci.yml                               config.toml
  ├── job làm gì (script)                      ├── executor nào (shell/docker/k8s)
  ├── chạy trên image nào (image:)             ├── image mặc định, image được phép
  ├── cần artifact của ai                      ├── concurrent, limit, request_concurrency
  ├── chạy khi nào (rules)                     ├── tags runner phục vụ
  └── đòi runner có tag gì (tags)              ├── volume được mount (Docker Socket!)
                                               └── mạng nội bộ job nằm trong
          │                                            │
          └──────────────┬─────────────────────────────┘
                         ▼
               TÁM PHA THỰC THI
     Pha 1, 2  ← 100% config.toml           ("Lỗi hạ tầng Runner")
     Pha 3     ← config.toml + biến GIT_*  (Ranh giới, hay tranh luận)
     Pha 4–8   ← Chủ yếu .gitlab-ci.yml    ("Lỗi mã nguồn / Logic")
```

Khoảng **37.5% (3 trên 8 pha)** các điểm có thể gây lỗi của một Job nằm hoàn toàn ở phía hạ tầng Runner (`config.toml`), nằm ngoài khả năng can thiệp trực tiếp của tệp `.gitlab-ci.yml`.

### 1.2. Trục Đánh Đổi Cô Lập Của 4 Loại Executor
Các loại Executor không khác nhau ở tốc độ chạy lệnh CPU (vì cùng chung nhân Linux Kernel), mà khác nhau ở **MỨC ĐỘ CÔ LẬP (Isolation Level)** và **CHI PHÍ KHỞI TẠO (Startup Overhead)**:

```mermaid
flowchart LR
    E1["Shell Executor<br/>(0% Cô lập, 0s Startup)"] -->|"Tăng mức cô lập hệ tệp"| E2["Docker Executor<br/>(Cô lập Filesystem, ~2s Startup)"]
    E2 -->|"Tăng mức cô lập tài nguyên"| E3["Kubernetes Executor<br/>(Cô lập Pod/Resource Limit, ~12s Startup)"]
    E3 -->|"Tùy biến môi trường cô lập"| E4["Custom / VM Autoscaling<br/>(Cô lập ảo hóa toàn phần, ~30s Startup)"]

    classDef exec fill:none,stroke:#3b82f6,stroke-width:1.5px,color:#f8fafc;
    class E1,E2,E3,E4 exec;
```

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

### 2.1. So Sánh Toàn Diện Các Loại Executor
| Tiêu Chí So Sánh | Shell Executor | Docker Executor | Kubernetes Executor |
| :--- | :--- | :--- | :--- |
| **Cơ chế môi trường** | Chạy trực tiếp trên Host OS | Container mới tạo qua Docker socket | Pod mới sinh trên K8s Cluster |
| **Mức độ cô lập** | <span class="badge badge--rose">0% (Rất nguy hiểm)</span> | <span class="badge badge--primary">Hệ tệp (0 byte tồn lưu)</span> | <span class="badge badge--emerald">Hệ tệp + CPU/RAM Quota</span> |
| **Chi phí khởi tạo** | ~0.01 giây | ~1–3 giây | ~10–15 giây |
| **Rò rỉ giữa các Job** | Rò rỉ file, process, secret profile | Tuyệt đối không | Tuyệt đối không |
| **Khuyến nghị sử dụng** | Task gắn với phần cứng đặc thù | Standard CI/CD Jobs, Unit Tests | Cloud Native Scaling, Enterprise Build |

### 2.2. So Sánh Ba Thông Số Điều Phối Tải Trong `config.toml`
| Thông Số | Vị Trí Cấu Hình | Ý Nghĩa Kỹ Thuật | Khuyến Nghị Thực Tế |
| :--- | :--- | :--- | :--- |
| **`concurrent`** | Cấp cao nhất (Global) | Tổng số Job tối đa mà **toàn bộ tiến trình Runner** được phép chạy song song | Bằng `nproc * 2` cho build job, hoặc giới hạn theo RAM |
| **`limit`** | Trong từng `[[runners]]` | Số Job tối đa của **riêng mục Runner đó** | Phải $\le$ `concurrent` |
| **`request_concurrency`** | Trong từng `[[runners]]` | Số request **hỏi việc (Long-polling)** gửi song song tới GitLab Server | Mặc định 1, tăng khi có độ trễ mạng lớn |

### 2.3. Ma Trận Ba Mức Phạm Vi Runner (Runner Scopes)
| Mức Phạm Vi | Đối Tượng Được Giao Việc | Rủi Ro Bảo Mật | Use Case Chuẩn |
| :--- | :--- | :--- | :--- |
| **Instance (Shared)** | Toàn bộ Project trên toàn GitLab | Cao (Bất kỳ ai tạo project đều gọi được) | Lint, Unit Test, Public Build |
| **Group** | Tất cả Project trong Group | Trung bình (Giới hạn trong đội ngũ) | Build service nội bộ, Integration Test |
| **Project (Specific)** | Duy nhất 1 Project được chỉ định | Thấp nhất (Kiểm soát chặt) | Deploy Production, Protected Environments |

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (Architecture Breakdown)

### 3.1. Tệp Cấu Hình Runner Chuẩn Enterprise (`config.toml`)
Dưới đây là kiến trúc tệp `config.toml` hoàn chỉnh cho Docker Executor chạy trên môi trường cô lập, tối ưu cache và bảo mật:

```toml
# ==============================================================================
# File: /etc/gitlab-runner/config.toml - Production Docker Runner Configuration
# ==============================================================================
concurrent = 8
check_interval = 5
shutdown_timeout = 30

[session_server]
  session_timeout = 1800

[[runners]]
  name = "prod-docker-runner-01"
  url = "https://gitlab.enterprise.internal"
  id = 101
  token = "glrt-t1_PRODUCTION_AUTHENTICATION_TOKEN_SECRET"
  token_obtained_at = 2026-09-12T08:00:00Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  limit = 8
  request_concurrency = 2
  
  [runners.custom_build_dir]
  [runners.cache]
    MaxUploadedArchiveSize = 1073741824 # 1 GB
    Type = "s3"
    Shared = true
    [runners.cache.s3]
      ServerAddress = "minio.internal:9000"
      AccessKey = "minio-cache-user"
      SecretKey = "minio-cache-secret"
      BucketName = "gitlab-runner-cache"
      Insecure = false
  
  [runners.docker]
    tls_verify = false
    image = "alpine:3.20"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    # TUYỆT ĐỐI KHÔNG MOUNT /var/run/docker.sock VÌ LÝ DO BẢO MẬT
    shm_size = 2147483648 # 2 GB Shared Memory
    pull_policy = ["if-not-present", "always"]
    network_mode = "bridge"
    extra_hosts = ["gitlab.enterprise.internal:10.0.10.15"]
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

### Tình Huống Sự Cố Thực Tế:
<span class="badge badge--rose">🕒 10:30 AM</span> Một thực tập sinh tạo một Merge Request từ fork cá nhân để thêm tính năng. Trong tệp `.gitlab-ci.yml`, người này chèn một lệnh khai thác đơn giản: `docker run -v /:/host-root alpine cat /host-root/etc/shadow`. Job chạy thành công và in toàn bộ mật khẩu mã hóa của máy chủ vật lý host Runner ra log công khai.

### Hậu Quả & Log Lỗi Thực Tế:
Kẻ tấn công chiếm được toàn bộ quyền kiểm soát máy chủ Runner Host và các thông tin xác thực AWS IAM:

```text
Executing "step_script" stage of the job script
$ docker run --rm -v /:/host-root alpine cat /host-root/root/.aws/credentials
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Job succeeded
```

```mermaid
flowchart TD
    A["Job chạy trên Runner mount Docker Socket<br/>(/var/run/docker.sock)"] -->|"Gọi Docker API trực tiếp từ trong Job"| B["Tạo Container con với mount /:/host-root"]
    B -->|"Docker Daemon chạy với quyền Root Host"| C["Bỏ qua 100% ranh giới Namespace & Cgroup"]
    C -->|"Đọc toàn bộ file nhạy cảm trên Host"| D["💥 RÒ RỈ SECRET AWS & ROOT PASSWORD"]

    classDef danger fill:none,stroke:#f43f5e,stroke-width:1.5px,color:#f8fafc;
    class A,B,C,D danger;
```

### 5-Whys Root Cause Analysis:
1. <span class="badge badge--primary">Why 1</span> **Tại sao Job đọc được file nhạy cảm trên máy chủ host?** $ightarrow$ Vì Job đã khởi tạo một container mới và mount toàn bộ thư mục gốc `/` của host.
2. <span class="badge badge--primary">Why 2</span> **Tại sao Job lại có quyền ra lệnh cho Docker Engine của host?** $ightarrow$ Vì trong `config.toml`, kỹ sư hạ tầng đã cấu hình `volumes = ["/var/run/docker.sock:/var/run/docker.sock"]`.
3. <span class="badge badge--primary">Why 3</span> **Tại sao kỹ sư lại mount Docker Socket vào Runner?** $ightarrow$ Để tiện cho việc chạy lệnh `docker build` (Docker-in-Docker) mà không cần cài đặt phức tạp.
4. <span class="badge badge--primary">Why 4</span> **Tại sao MR của người ngoài lại được chạy trên Runner này?** $ightarrow$ Vì Runner này được đăng ký ở cấp **Instance (Shared Runner)** mở cho mọi repository.
5. <span class="badge badge--emerald">Root Cause Remedy</span> **Biện pháp khắc phục chuẩn SRE:**
   - Xóa bỏ ngay lập tức việc mount `/var/run/docker.sock` trên Shared Runners.
   - Chuyển sang sử dụng **Kaniko** hoặc **Buildah (Rootless)** để build Docker image mà không cần Docker daemon.
   - Phân tách riêng biệt Runner cho Protected Branches và Untrusted MRs.

---

## 5. Hands-on Lab: Triển Khai & Kiểm Thử Runner & Executors (8 Bước Chuẩn)

### Bước 1: Khởi Tạo GitLab Runner Với Docker Executor
Đăng ký Runner mới sử dụng cú pháp Authentication Token (`glrt-...`):

```bash
docker run -d --name gitlab-runner-lab   --restart always   -v /var/run/docker.sock:/var/run/docker.sock   -v /etc/gitlab-runner:/etc/gitlab-runner   gitlab/gitlab-runner:v17.7.0

# Đăng ký Runner tương tác không mật khẩu cũ
docker exec -it gitlab-runner-lab gitlab-runner register   --non-interactive   --url "http://gitlab.lab:8929"   --token "$RUNNER_AUTH_TOKEN"   --executor "docker"   --docker-image "alpine:3.20"   --description "lab-docker-runner"   --docker-network-mode "bridge"   --docker-extra-hosts "gitlab.lab:172.28.0.10"
```

### Bước 2: Khảo Sát & Giải Mã Tệp `config.toml`
Kiểm tra tệp cấu hình sinh ra và thiết lập hạn mức thực thi đồng thời:

```bash
cat /etc/gitlab-runner/config.toml
```

Chỉnh sửa thông số `concurrent = 4` ở đầu tệp để cho phép 4 job chạy song song.

### Bước 3: Kiểm Chứng 3 Điều Kiện Độc Lập Để Runner Nhận Job
Chạy script kiểm tra trạng thái Online, Paused và Tag Routing qua API:

```bash
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/1"   | jq '{id, description, online, paused, run_untagged, tag_list}'
```

### Bước 4: Kiểm Chứng Rò Rỉ Môi Trường Giữa Shell vs Docker Executor
Thực thi 2 job liên tiếp trên Shell Runner để ghi nhận hiện tượng file rác tồn lưu:

```yaml
# Test trên Shell Executor
test-shell-leak-1:
  tags: [shell-runner]
  script:
    - touch /tmp/leaked_by_job1.txt
    - echo "Leaked from Job 1" > /tmp/leaked_by_job1.txt

test-shell-leak-2:
  tags: [shell-runner]
  script:
    - cat /tmp/leaked_by_job1.txt # VẪN ĐỌC ĐƯỢC -> Rò rỉ trạng thái!
```

### Bước 5: Kiểm Chứng 0-Byte State Retention Trên Docker Executor
Thực thi cùng kịch bản trên Docker Runner để chứng minh tính cô lập 0 byte:

```yaml
test-docker-isolation:
  tags: [docker-runner]
  image: alpine:3.20
  script:
    - ls /tmp/leaked_by_job1.txt # Báo lỗi No such file -> 100% Cô lập!
```

### Bước 6: Đo Lường & Phân Biệt `concurrent` vs `limit`
Thực nghiệm gửi 6 job đồng thời vào Runner cấu hình `concurrent = 4` và `limit = 2` để quan sát hiện tượng hàng đợi xếp tầng (Queued Duration).

### Bước 7: Phân Tích Hiện Tượng Nghẽn CPU Khi Tăng Quá Mức `concurrent`
Chạy lệnh `docker stats` song song với pipeline stress test CPU để đo lường điểm bão hòa phần cứng (`Duration` trung bình bắt đầu tăng vọt).

### Bước 8: Áp Dụng Best Practice Bảo Mật & Dọn Dẹp
Cấu hình thu hồi quyền truy cập Docker socket và thiết lập chính sách xóa container tự động:

```bash
docker exec -it gitlab-runner-lab gitlab-runner unregister --all-runners
```

---

## 6. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span class="qa-question-text">Hai tệp .gitlab-ci.yml và config.toml do ai viết và phân chia trách nhiệm thế nào? Pha nào trong 8 pha thuộc về hạ tầng?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b></div>
    <div>• <b><code>.gitlab-ci.yml</code>:</b> Do Kỹ sư phần mềm / DevOps viết mã pipeline quản lý. Tệp này định nghĩa Job <i>LÀM GÌ</i> (script, image mong muốn, artifacts, rules).</div>
    <div>• <b><code>config.toml</code>:</b> Do Quản trị viên hệ thống / Platform Engineer quản lý. Tệp này cấu hình Job <i>CHẠY Ở ĐÂU VÀ QUYỀN GÌ</i> (loại executor, volume mount, giới hạn CPU/RAM, concurrent, tag routing).</div>
    <div>• <b>Phân chia 8 pha:</b> Ba pha đầu (<code>prepare_executor</code>, <code>prepare_script</code>, và phần lớn <code>get_sources</code>) thuộc 100% trách nhiệm hạ tầng của <code>config.toml</code>. Tức <b>3/8 pha (~37.5%)</b> các vị trí lỗi xảy ra nằm ngoài tầm kiểm soát của người viết <code>.gitlab-ci.yml</code>.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Không biết có file config.toml &bull; 1: Kể được 2 file nhưng không rõ ranh giới &bull; 2: Phân tích đúng làm gì vs chạy ở đâu &bull; 3: Nêu đúng ranh giới + chỉ ra 3/8 pha thuộc hạ tầng và ý nghĩa "đề nghị đúng người khi sửa lỗi".</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Khi pipeline đỏ ở pha <code>prepare_executor</code> thì sửa file nào? <i>(Sửa <code>config.toml</code> hoặc cấu hình Docker/K8s trên máy chủ Runner, không sửa <code>.gitlab-ci.yml</code>.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span class="qa-question-text">Bốn loại Executor (Shell, Docker, Kubernetes, Custom) khác nhau ở trục cốt lõi nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b> Khác nhau ở <b>MỨC ĐỘ CÔ LẬP (Isolation Level)</b> và <b>CHI PHÍ KHỞI TẠO (Startup Overhead)</b>, hoàn toàn không khác biệt về hiệu năng thực thi CPU thuần túy:</div>
    <div>• <b>Shell Executor:</b> 0% cô lập (chạy trực tiếp trên host OS, 0s startup).</div>
    <div>• <b>Docker Executor:</b> Cô lập hệ tệp (mỗi job là 1 container mới, 0-byte state retention, ~2s startup).</div>
    <div>• <b>Kubernetes Executor:</b> Cô lập cả hệ tệp và hạn mức tài nguyên CPU/RAM quota cấp Pod (~12s startup).</div>
    <div>• <b>Custom / Autoscaling VM:</b> Cô lập toàn diện cấp độ máy ảo ảo hóa (~30s startup).</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Nói khác về tốc độ &bull; 1: Nói được Docker sạch hơn Shell &bull; 2: Nêu đúng trục cô lập vs chi phí khởi tạo &bull; 3: Phân tích xuất sắc cả 4 loại kèm số liệu startup overhead thực tế.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Với job lint chạy 5 giây thì chọn Docker hay Shell? <i>(Vẫn chọn Docker vì an toàn bảo mật; startup 2s hoàn toàn chấp nhận được để đổi lấy sự cô lập.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span class="qa-question-text">Tại sao mount Docker Socket (/var/run/docker.sock) vào container runner lại làm vô hiệu hóa 100% cơ chế cô lập bảo mật?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b> Docker Socket là giao diện IPC điều khiển toàn quyền Docker Daemon của máy chủ host. Docker Daemon mặc định chạy dưới quyền <code>root</code> và không có cơ chế phân quyền chi tiết bên trong API.</div>
    <div>Khi mount socket vào job container, bất kỳ câu lệnh nào trong job (kể cả script từ MR của người ngoài) đều có thể chạy <code>docker run -v /:/host-root alpine</code> để đọc và ghi đè toàn bộ hệ thống file của máy chủ host, đánh cắp SSH key, AWS credentials và chiếm quyền root host.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Không biết socket là gì &bull; 1: Biết có nguy cơ bảo mật &bull; 2: Phân tích đúng cơ chế giao tiếp daemon root &bull; 3: Nêu đúng kịch bản khai thác mount root host <code>-v /:/host</code> và giải pháp thay thế bằng Kaniko.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Giải pháp build image nào không cần Docker Socket? <i>(Sử dụng Kaniko, Buildah rootless, hoặc BuildKit container.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span class="qa-question-text">Cơ chế đăng ký Runner mới bằng Authentication Tokens (từ GitLab 16.0+) thay thế Registration Token cũ như thế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b></div>
    <div>• <b>Cơ chế cũ (Registration Token):</b> Dùng 1 token tĩnh chia sẻ cho nhiều Runner. Runner tự khai báo tag khi register &rarr; Rủi ro bảo mật nghiêm trọng: Ai có token đều có thể đăng ký runner giả mạo chiếm tag nhạy cảm (như <code>production-deploy</code>) để cướp job.</div>
    <div>• <b>Cơ chế mới (Authentication Token `glrt-...`):</b> Quản trị viên phải tạo cấu hình Runner trên GitLab trước (chỉ định sẵn tag, mô tả, quyền hạn), GitLab sinh ra một token xác thực duy nhất bắt đầu bằng <code>glrt-</code>. Runner chỉ dùng token này để nhận dạng, không thể tự ý thay đổi tag.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Không biết sự thay đổi &bull; 1: Biết token có tiền tố glrt- &bull; 2: Phân tích đúng lỗ hổng cướp tag của token cũ &bull; 3: Phân tích xuất sắc cơ chế kiểm soát tag từ phía máy chủ và quy trình đăng ký token mới.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Token <code>glrt-</code> có hạn sử dụng không? <i>(Có thể cấu hình xoay vòng token tự động theo chính sách bảo mật doanh nghiệp.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span class="qa-question-text">Cơ chế sao chép dự án của pha 3 (get_sources) gồm những chiến lược nào (GIT_STRATEGY)? Khi nào dùng fetch vs clone?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b> Có 3 chiến lược chính trong <code>GIT_STRATEGY</code>:</div>
    <div>1. <b>`clone` (Mặc định khi thư mục rỗng):</b> Tạo mới toàn bộ kho từ số 0, an toàn tuyệt đối nhưng tốn băng thông và thời gian với repo lớn.</div>
    <div>2. <b>`fetch` (Mặc định tối ưu):</b> Tái sử dụng thư mục làm việc cũ của runner, chỉ kéo các commit mới (incremental fetch), nhanh hơn đáng kể.</div>
    <div>3. <b>`none`:</b> Bỏ qua hoàn toàn việc tải code Git, dùng cho các job chỉ xử lý tải artifact hoặc trigger pipeline khác.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Không biết &bull; 1: Kể được clone vs fetch &bull; 2: Phân tích đúng sự khác nhau &bull; 3: Nêu đủ cả 3 chiến lược (clone, fetch, none) kèm cờ <code>GIT_DEPTH</code> để tối ưu shallow clone.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Khi nào <code>GIT_STRATEGY: clone</code> là bắt buộc? <i>(Khi cần đảm bảo workspace 100% sạch trên Shell runner, hoặc khi build đòi hỏi git log đầy đủ không shallow.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span class="qa-question-text">Phân biệt sự khác nhau giữa 3 thông số định lượng: concurrent, limit và request_concurrency trong config.toml?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b></div>
    <div>• <b>`concurrent` (Global):</b> Hạn mức tối đa tổng số job mà <b>toàn bộ daemon runner</b> được phép thực thi đồng thời.</div>
    <div>• <b>`limit` (Mục runner con):</b> Hạn mức số job tối đa của <b>riêng khối `[[runners]]` đó</b>. Số job thực tế chạy là <code>min(concurrent, limit)</code>.</div>
    <div>• <b>`request_concurrency`:</b> Số lượng request hỏi việc (long-poll requests) gửi đồng thời tới GitLab Server, không phải số job thực thi.</div>
    <div>Lưu ý: Mặc định <code>concurrent = 1</code> khi cài mới, khiến job thứ hai luôn phải chờ job thứ nhất hoàn thành.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Không phân biệt được &bull; 1: Biết concurrent là số job &bull; 2: Phân biệt đúng cả 3 và cơ chế lấy min &bull; 3: Phân tích sâu cơ chế hàng đợi và cách nhận biết nghẽn polling vs nghẽn concurrent.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Nếu đặt <code>limit = 10</code> và <code>concurrent = 2</code> thì runner chạy được mấy job? <i>(Tối đa đúng 2 job vì bị chặn bởi trần global concurrent.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span class="qa-question-text">Khi pipeline bị nghẽn (pending lâu), việc tăng concurrent hay thêm runner có phải luôn là giải pháp đúng không? Cần đo gì trước?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b> Chưa chắc — đây là bài toán lý thuyết hàng đợi (Queueing Theory):</div>
    <div>Tổng thời gian hoàn thành một Job = Thời gian chờ hàng đợi (Queue Duration) + Thời gian thực thi (Execution Duration).</div>
    <div>Nếu máy chủ Runner đã bão hòa CPU/Disk I/O (CPU utilization $pprox 100\%$), việc tăng concurrent chỉ chia nhỏ tài nguyên khiến <b>Execution Duration tăng vọt</b>, làm tổng thời gian hoàn thành thậm chí còn lâu hơn.</div>
    <div>2 Phép đo bắt buộc phải làm trước:</div>
    <div>1. Đo mức tải phần cứng hiện tại qua <code>docker stats</code> hoặc monitoring metrics.</div>
    <div>2. Đo thời lượng trung vị (Median Duration) của job khi tăng dần concurrent. Quy tắc dừng: Chỉ tăng concurrent khi Duration trung vị chưa bị đội lên đáng kể.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Khẳng định cứ thêm runner là nhanh &bull; 1: Nói được cần xem tài nguyên &bull; 2: Phân tích đúng Queue time vs Execution time &bull; 3: Nêu xuất sắc quy tắc dừng tối ưu và giải thích vì sao dùng Median thay vì Average.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Vì sao đo thời gian chờ phải dùng Trung vị (Median) thay vì Trung bình (Mean)? <i>(Vì vài job bị pending timeout 60 phút do sai tag sẽ làm sai lệch hoàn toàn giá trị trung bình.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span class="qa-question-text">Runner có mấy mức phạm vi (Instance, Group, Project) và nguyên tắc phân bổ quyền hạn bảo mật Enterprise là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b> Có 3 mức phạm vi:</div>
    <div>1. <b>Instance (Shared Runner):</b> Phục vụ mọi project trên hệ thống. Dành cho các tác vụ công khai, không có secret nhạy cảm (Linting, Unit Testing).</div>
    <div>2. <b>Group Runner:</b> Phục vụ tất cả project con trong một Group. Dành cho build nội bộ và integration test.</div>
    <div>3. <b>Project (Specific Runner):</b> Chỉ phục vụ duy nhất 1 project được gán. Dành cho tác vụ Deploy Production, có gắn với Protected Environment và chứa Cloud Credentials.</div>
    <div>Nguyên tắc vàng: <b>Tuyệt đối không dùng Shared Runner để chạy các job deploy production</b> vì nguy cơ bị tấn công chéo từ các project untrusted.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Không biết 3 mức &bull; 1: Kể được 3 mức &bull; 2: Phân tích đúng rủi ro bảo mật của Instance runner &bull; 3: Nêu xuất sắc kiến trúc phân tách runner cho build vs deploy production.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Merge Request từ một fork bên ngoài sẽ chạy trên Runner nào? <i>(Mặc định chạy trên Runner của repo gốc, do đó phải cấm mount docker socket trên runner này.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span class="qa-question-text">Tại sao Runner hiển thị chấm xanh (Online) trên Web UI nhưng Job vẫn bị kẹt Pending? Ba điều kiện độc lập là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b> Chấm xanh chỉ chứng minh Runner đang gửi Heartbeat (Online). Để Runner thực sự nhận Job cần thỏa mãn đồng thời <b>3 ĐIỀU KIỆN ĐỘC LẬP</b>:</div>
    <div>1. <b>`online == true`</b>: Runner daemon đang chạy và kết nối được với GitLab.</div>
    <div>2. <b>`paused == false`</b>: Runner không bị tạm dừng thủ công trên giao diện.</div>
    <div>3. <b>Khớp định tuyến (Routing Match)</b>: Tập <code>tags</code> của Job phải là tập con của <code>tags</code> trên Runner, HOẶC Job không khai báo tag và Runner có bật cờ <code>run_untagged: true</code>.</div>
    <div>Thiếu 1 trong 3 điều kiện trên đều cho ra cùng một triệu chứng: <b>Job Pending vô hạn, không có trace log</b>. Kiểm tra nhanh bằng 1 lệnh API: <code>GET /api/v4/runners/:id</code>.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Cho rằng chấm xanh là runner tốt &bull; 1: Đoán do tag &bull; 2: Nêu đủ 3 điều kiện &bull; 3: Phân tích sâu 3 nguyên nhân 1 triệu chứng + giải pháp kiểm tra API tổng thể.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Thuộc ô nào trong ma trận lỗi? <i>(Im lặng, có chặn. Gây timeout sau 60 phút mặc định.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span class="qa-question-text">Trên Kubernetes Executor, làm sao chẩn đoán được Job bị Pending do thiếu Runner hay do Pod không được Cluster xếp lịch (Scheduling)?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b> Phải truy vấn đồng thời <b>HAI NGUỒN DỮ LIỆU</b>:</div>
    <div>• <b>Nguồn 1 (GitLab API):</b> Kiểm tra 3 điều kiện của Runner xem Runner Manager đã nhận Job hay chưa.</div>
    <div>• <b>Nguồn 2 (Kubernetes API):</b> Kiểm tra trạng thái Pod bằng lệnh:</div>
    <div><code>kubectl get pods -n gitlab-runner --field-selector=status.phase=Pending</code> và <code>kubectl get events -n gitlab-runner</code>.</div>
    <div>Nếu sự kiện báo <code>0/N nodes available: Insufficient cpu/memory</code> thì lỗi do Cluster hết tài nguyên, việc thêm GitLab Runner sẽ không giải quyết được vấn đề.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Nói giống docker &bull; 1: Biết liên quan tới k8s &bull; 2: Nêu đúng 2 nguồn dữ liệu &bull; 3: Phân tích xuất sắc các sự kiện K8s scheduling + thông số <code>poll_timeout</code> trong config.toml.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Thông số <code>poll_timeout</code> có vai trò gì? <i>(Thời gian tối đa Runner chờ Pod K8s khởi chạy thành công trước khi hủy Job và báo FAILED.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q11</span>
    <span class="qa-question-text">Lựa chọn Executor và phạm vi Runner tối ưu cho 3 tình huống: Lint trên MR public, Build Docker Image, và Deploy Production có Secret?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b></div>
    <div>• <b>(a) Lint trên MR public:</b> Docker Executor, Shared/Instance Runner, <b>không</b> mount Docker socket, image nhẹ (Alpine/Node).</div>
    <div>• <b>(b) Build Docker Image:</b> Docker/K8s Executor, Group Runner, sử dụng <b>Kaniko</b> (không socket) hoặc Docker-in-Docker an toàn có TLS certs.</div>
    <div>• <b>(c) Deploy Production:</b> Docker/K8s Executor, <b>Project-Specific Runner</b>, gán nhãn <code>protected: true</code> cho Protected Environments, thiết lập <code>concurrent = 1-2</code> để tránh deploy đồng thời xung đột.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Chọn bừa cùng 1 loại &bull; 1: Chọn đúng nhưng giải thích theo tốc độ &bull; 2: Chọn đúng với lập luận theo mức cô lập &bull; 3: Phân tích xuất sắc cả 3 ca kèm lập luận về mức phạm vi Runner và cơ chế chống xung đột deploy.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Vì sao ở ca (c) nên đặt <code>concurrent</code> thấp? <i>(Để ngăn chặn hai pipeline deploy chạy đè lên nhau gây race condition trên hạ tầng.)</i></div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q12</span>
    <span class="qa-question-text">Quy trình 3 nhịp phân loại sự cố để xác định chính xác lỗi thuộc về người viết Pipeline (.gitlab-ci.yml) hay đội Hạ tầng (config.toml)?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div><b>Đáp án chuẩn:</b> Quy trình 3 nhịp chuẩn hóa:</div>
    <div>• <b>Nhịp 1 — Xác định Pha trong Log (10 giây):</b> Tìm dòng tiêu đề pha cuối cùng trước khi lỗi. Nếu không có dòng <code>Executing "step_script"</code> &rarr; Lệnh chưa từng chạy, lỗi 100% thuộc về hạ tầng Runner.</div>
    <div>• <b>Nhịp 2 — Ánh xạ sang Tệp:</b> Pha 1 (`prepare_executor`), Pha 2 (`prepare_script`), và phần lớn Pha 3 (`get_sources`) thuộc quyền quản lý của <code>config.toml</code>. Các pha từ 4 đến 8 thuộc về <code>.gitlab-ci.yml</code>.</div>
    <div>• <b>Nhịp 3 — Kiểm tra Job Pending không có log:</b> Kiểm tra 3 điều kiện Runner (Online, Not Paused, Tag Match) qua API và kiểm tra sự kiện K8s cluster nếu dùng K8s executor.</div>
    <div>Ý nghĩa: Tiết kiệm 80% thời gian debug và luôn liên hệ đúng đầu mối kỹ thuật phụ trách.</div>
    <div style="margin-top: 0.5rem;"><b style="color: var(--accent-cyan);">&bull; Tiêu chí chấm điểm:</b> 0: Đọc log tìm chữ ERROR &bull; 1: Biết phân loại pha &bull; 2: Nêu đúng 3 nhịp &bull; 3: Trình bày xuất sắc quy trình 3 nhịp kèm số liệu 3/8 pha và kỹ năng xử lý job pending.</div>
    <div><b style="color: var(--accent-rose);">&bull; Câu hỏi đào sâu:</b> Khi pipeline của cả công ty đột nhiên đỏ đồng loạt mà không ai sửa code, nguyên nhân đầu tiên cần kiểm tra là gì? <i>(Có ai vừa thay đổi hoặc khởi động lại <code>config.toml</code> của runner cluster hay không.)</i></div>
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

### Tóm Tắt Các Điểm Cốt Lõi:
1. **Ranh Giới 2 Tệp:** `.gitlab-ci.yml` kiểm soát logic hành động; `config.toml` kiểm soát hạ tầng và mức độ an toàn.
2. **Nguyên Tắc Cô Lập:** Lựa chọn Executor dựa trên yêu cầu cô lập và bảo mật, không dựa thuần túy vào tốc độ.
3. **Tuyệt Đối Tránh Docker Socket:** Không mount `/var/run/docker.sock` trên các Shared Runner cấp Enterprise.
4. **Ba Điều Kiện Runner:** Luôn kiểm tra đủ 3 điều kiện (Online, Unpaused, Tag Match) khi Job bị Pending.

```mermaid
mindmap
  root((GitLab Runner Architecture))
    Config Ranh Giới
      .gitlab-ci.yml: Logic Job
      config.toml: Ha Tang & Quyen
      3/8 Pha Thuoc Ha Tang
    4 Loai Executor
      Shell: 0% Co Lap
      Docker: Co Lap Filesystem
      Kubernetes: Co Lap Resource
    Dieu Phoi & Hieu Nang
      concurrent: Tran Global
      limit: Tran Runner Con
      request_concurrency: Long-polling
    An Toan Enterprise
      Cam Mount Docker Socket
      Phan Tach Shared vs Specific
      Token Moi: glrt- Authentication
```

---

> [!TIP]
> **BÀI HỌC TIẾP THEO:**
> Trong **[[Bài 03] Cú Pháp YAML & Thiết Kế Stages Trong GitLab CI: Cấu Trúc Pipeline, Default Settings & Biến Toàn Cục](gitlab-03-03-cu-phap-yaml-va-stage.html)**, chúng ta sẽ đi sâu vào kỹ thuật thiết kế tệp `.gitlab-ci.yml` chuẩn Enterprise, phân cấp `stages`, kiểm soát thứ tự thực thi và cơ chế nạp biến toàn cục.

{% endraw %}
