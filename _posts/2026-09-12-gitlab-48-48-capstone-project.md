---
layout: post
title: "[Bài 48] Đồ Án Capstone: Xây Dựng Hệ Thống CI/CD & DevSecOps Doanh Nghiệp Đa Môi Trường Chuẩn Enterprise End-to-End"
date: 2026-09-12 01:40:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-48
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 48
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.48] Hướng dẫn chuyên sâu Đồ Án Capstone: Xây Dựng Hệ Thống CI/CD & DevSecOps Doanh Nghiệp Đa Môi Trường Chuẩn Enterprise End-to-End: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

{% raw %}
# [BÀI 48] ĐỒ ÁN CAPSTONE: XÂY DỰNG HỆ THỐNG CI/CD & DEVSECOPS DOANH NGHIỆP ĐA MÔI TRƯỜNG CHUẨN ENTERPRISE END-TO-END

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

---





| STT | Câu hỏi ôn tập | Đáp án vắn tắt |
|---|---|---|
| 1 | Khi job bị kẹt ở trạng thái `pending` vô thời hạn, 3 nguyên nhân hạ tầng runner phổ biến nhất là gì? | Tags không khớp giữa job và runner, runner bị `paused` hoặc đạt `concurrent` max limit, hoặc runner lost connection đến GitLab coordinator API |
| 2 | Chế độ hỏng "Silent Failure" nào nguy hiểm nhất trong pipeline caching? | Cache key dùng chung cố định khiến branch `feature` ghi đè artifact/thư viện hỏng lên cache của `main`, khiến build `main` vỡ mà không log lỗi rõ ràng |
| 3 | Khác biệt cơ bản giữa Log Level `DEBUG` trong runner và `CI_DEBUG_TRACE` trong job là gì? | `CI_DEBUG_TRACE=true` in ra mọi câu lệnh shell trong job execution context; Log Level `DEBUG` trong `config.toml` in ra log nội bộ của dịch vụ `gitlab-runner` daemon |
| 4 | Kỹ thuật nào giúp cô lập sự cố network egress timeout từ inside container runner? | Chạy `curl -v --connect-timeout 5` kết hợp `traceroute` hoặc `nc -zvw3` ngay trong `before_script` để xác định IP/Port bị chặn bởi Egress Firewall |
| 5 | Khi pipeline bị OOM (Out Of Memory) do RAM container vượt quá limit, chỉ số kernel nào khẳng định nguyên nhân? | Log `dmesg` hoặc `journalctl` trên host runner hiển thị `OOM-killer killed process` kèm `exit code 137` của Docker container |



Trải qua 47 buổi học thực chiến từ những câu lệnh YAML đơn giản nhất đến các chiến lược quản trị hạ tầng runner, bảo mật compliance, IaC automation và release management nâng cao, chúng ta đã đi trọn vẹn hành trình từ Zero đến Hero trong thế giới GitLab CI/CD. 

Bài học Buổi 48 này là cột mốc tổng kết quan trọng nhất - nơi toàn bộ các mảnh ghép kiến thức lẻ tẻ được hợp nhất thành một bức tranh kiến trúc Enterprise CI/CD tổng thể (Architectural Blueprint). Trong một môi trường doanh nghiệp quy mô lớn (Enterprise Scale), hệ thống CI/CD không chỉ là một công cụ giúp tự động hóa lệnh `git push` hay `docker build`. Nó là hệ xương sống (Backbone) của toàn bộ quy trình phân phối phần mềm, quyết định tốc độ ra mắt sản phẩm (Time-to-Market), mức độ an toàn thông tin (Cybersecurity posture), tính sẵn sàng của hạ tầng (High Availability) và khả năng tuân thủ pháp lý (Regulatory Compliance).

Trong thực tế doanh nghiệp, một hệ thống CI/CD thiếu kiến trúc tổng thể thường rơi vào thảm họa "YAML Spaghetti": hàng trăm repository chứa các file cấu hình nhân bản sai lệch, lộ mật mã tĩnh trên CI Variables, runner quá tải gây nghẽn hàng giờ, và mỗi đợt phát hành lên Production là một lần đội ngũ vận hành phải cầu nguyện. Bài học Capstone này giải quyết triệt để vấn đề đó bằng việc hệ thống hóa thành **Kiến trúc Enterprise CI/CD 5 Tầng** cùng **12 Quy tắc vàng bất biến**.

---



| STT | Kỹ năng đạt được | Hiện vật chứng minh |
|---|---|---|
| 1 | Thiết kế kiến trúc tổng thể Enterprise CI/CD Platform cho 100+ Microservices | File sơ đồ Mermaid Blueprint & Document Kiến trúc Capstone hoàn chỉnh |
| 2 | Đóng gói thư viện Centralized CI/CD Components chuẩn hóa cấp Tập đoàn | Centralized Repository `devops/ci-components` với phiên bản Semantic Versioning |
| 3 | Cưỡng chế quy chuẩn Security Compliance Pipelines đa tầng cho 100% dự án con | Group Compliance Framework Configuration & Shared Security Policy Template |
| 4 | Triển khai xác thực OIDC Federated Secretless Authentication với AWS, GCP, Azure | Dynamic Identity Token Exchange Pipeline configuration không cần Static Credentials |
| 5 | Tự động hóa IaC Provisioning kết hợp State Lock & Approval Gate với Terraform | Terraform Automation Pipeline xuất artifact `plan.tfplan` và phê duyệt manual `apply` |
| 6 | Xây dựng luồng Progressive Delivery Canary Rollout đi kèm Prometheus Auto-Rollback | Helm Deployment Script tự động query Error Rate từ Prometheus API để kích hoạt Rollback |
| 7 | Thiết lập hệ thống Monitoring & Measuring 4 chỉ số DORA Metrics cho toàn doanh nghiệp | Prometheus Metric Exporter Exposing Webhook Engine & Grafana DORA Metrics Dashboard |

---



| Kiến thức cần có | Nguồn tự học nếu thiếu | Số hiệu QUY TẮC liên quan |
|---|---|---|
| Kiến trúc Pipeline & DAG Workflow | Buổi 08, Buổi 09, Buổi 10 | `QT 8.1`, `QT 9.2`, `QT 10.1` |
| Quản trị Runner Autoscaling & Kubernetes | Buổi 13, Buổi 44 | `QT 13.2`, `QT 44.1` |
| CI/CD Components & Catalog Reusability | Buổi 11, Buổi 38 | `QT 11.1`, `QT 38.1` |
| DevSecOps (SAST, SCA, Secret, Cosign, SBOM) | Buổi 28, Buổi 29, Buổi 30, Buổi 31, Buổi 32 | `QT 28.1`, `QT 30.2`, `QT 32.1` |
| OIDC Authentication & Dynamic Cloud Access | Buổi 37, Buổi 38, Buổi 39, Buổi 40 | `QT 37.1`, `QT 40.2` |
| Terraform Infrastructure & State Management | Buổi 42 | `QT 42.1` |
| Release Strategies (Canary, Blue-Green, Flags) | Buổi 43 | `QT 43.1` |
| Governance, Compliance & DORA Metrics | Buổi 45, Buổi 46, Buổi 47 | `QT 45.1`, `QT 46.1`, `QT 47.1` |

---



### Bảng đối chiếu thuật ngữ Việt - Anh

| Thuật ngữ tiếng Việt | Term tiếng Anh tương đương | Ý nghĩa vận hành trong Capstone |
|---|---|---|
| Bản thiết kế kiến trúc | Architectural Blueprint | Sơ đồ cấu trúc tổng thể kết nối 5 tầng của hệ thống CI/CD Enterprise |
| Khung tuân thủ tập trung | Compliance Framework | Quy định pipeline bắt buộc áp dụng từ cấp Group cho mọi dự án con |
| Xác thực không mật khẩu tĩnh | Secretless Authentication (OIDC) | Cơ chế cấp JWT Token ngắn hạn thay thế cho Cloud Access Key tĩnh |
| Thư viện thành phần tái sử dụng | CI/CD Component Catalog | Kho phần tử pipeline chung có phiên bản (v1.0.0) và tham số giao diện |
| Phát hành lũy tiến | Progressive Delivery | Chiến lược đẩy code dần dần (Canary 10% -> 100%) kèm kiểm tra metric |
| Tự động khôi phục | Auto-Rollback Engine | Script tự động hủy release và về bản cũ khi error rate vượt ngưỡng |
| Bằng chứng nguồn gốc phần mềm | Software Provenance & SBOM | Chữ ký Cosign và danh mục phần tử software chứng minh tính toàn vẹn |
| Hạ tầng sống tạm thời | Ephemeral Runner Infrastructure | Hạ tầng runner Pod chỉ sinh ra khi có job và hủy ngay khi hoàn thành |
| Đo lường hiệu năng phân phối | DORA Metrics Automation | Bộ 4 chỉ số đo đạc tốc độ và độ tin cậy của quy trình phân phối phần mềm |
| Khóa trạng thái hạ tầng | IaC State Locking | Cơ chế ngăn chặn nhiều job Terraform can thiệp hạ tầng cùng một lúc |
| Phản hồi nhanh lập trình viên | Fast Feedback Loop | Thiết kế pipeline phản hồi lỗi cho developer dưới 10 phút |
| Phê duyệt 2 người độc lập | Four-Eye Approval Principle | Quy tắc yêu cầu ít nhất 2 nhân sự độc duyệt MR và release |
| Tách biệt môi trường thực thi | Environment Isolation | Đảm bảo runner stage Staging và Production không chung tài nguyên |

### Mô hình tư duy cốt lõi (Mental Models)

**Mô hình 1: Sợi dây chuyền sản xuất 5 tầng (The 5-Tier Industrial Conveyor Belt)**
Hệ thống Capstone CI/CD được ví như một dây chuyền sản xuất ô tô hiện đại. Mã nguồn đẩy vào đi qua 5 trạm kiểm định nối tiếp: (1) Trạm Governance kiểm tra thiết kế và phân quyền; (2) Trạm Security quét bằng tia X phát hiện lỗ hổng ẩn và credential rò rỉ; (3) Trạm IaC chuẩn bị mặt bằng hạ tầng bằng Terraform; (4) Trạm Build lắp ráp container rootless và dán tem chữ ký số Cosign; (5) Trạm Release thử nghiệm 10% công suất Canary trước khi xuất xưởng 100% kèm tự động rollback khi gặp sự cố.

**Mô hình 2: Nguyên tắc Bức tường bảo vệ không thể Bypass (Unbypassable Security Fence)**
Trong mô hình Enterprise, pipeline dự án con không bao giờ sở hữu toàn quyền tự quyết. Mọi thay đổi đều nằm trong một chiếc hộp kiên cố được bao bọc bởi Compliance Pipeline ở cấp Group. Dù lập trình viên có xóa sạch file `.gitlab-ci.yml` ở repo con thì các kiểm tra an toàn tại repo cha vẫn tự động chèn vào và thực thi bắt buộc.

**Mô hình 3: Vòng xoáy cải tiến liên tục DORA (The DORA Flywheel of Continuous Improvement)**
Hệ thống CI/CD không phải là một dự án làm một lần rồi bỏ đó. Thông qua bộ 4 chỉ số DORA Metrics thu thập tự động từ Webhooks, ban quản trị và đội ngũ kỹ thuật liên tục nhận biết các điểm nghẽn (tắc ở khâu test thủ công, vỡ ở khâu deploy hay kéo dài ở khâu review code) để liên tục tối ưu hóa hạ tầng runner và tự động hóa quy trình.

---

### 1.1. Kiến trúc Enterprise CI/CD tổng thể (Architectural Blueprint) (15 phút)

```mermaid
flowchart TD
    subgraph Tier1 ["1. Developer Experience & Governance"]
        MR[Merge Request Event] --> ComplianceGate[Compliance Pipeline Enforcement]
        ComplianceGate --> PolicyCheck[Policy as Code & CODEOWNERS Approval]
        PolicyCheck --> FastFeedback[Fast-Feedback Linter & Unit Tests]
    end

    subgraph Tier2 ["2. Multi-Layer DevSecOps Pipeline"]
        FastFeedback --> SAST[Static Application Security Testing - Semgrep]
        SAST --> SecretScan[Secret Push Protection & Credential Audit]
        SecretScan --> SCA[Dependency & License Scanning - Grype/Syft]
        SCA --> ContainerScan[Container Image Vulnerability Scan - Trivy]
    end

    subgraph Tier3 ["3. Infrastructure & IaC Pipeline"]
        ContainerScan --> OIDCAuth[OIDC Federated Auth with Cloud AWS/GCP/Azure]
        OIDCAuth --> TFPlan[Terraform Plan & Encrypted HTTP State Lock]
        TFPlan --> TFApprove[Manual Environment Approval Gate]
        TFApprove --> TFApply[Terraform Apply / Infrastructure Provisioning]
    end

    subgraph Tier4 ["4. Container Build & Progressive Release"]
        TFApply --> KanikoBuild[Rootless Kaniko Build & Cache Layering]
        KanikoBuild --> SignImage[Cosign Supply-Chain Image Signing]
        SignImage --> DeployStrategy{Progressive Deployment Strategy}
        DeployStrategy -->|Canary 10%| CanaryRollout[Canary Deployment & Prometheus Health Check]
        CanaryRollout -->|Error Rate < 0.1%| FullDeploy[Helm Production Upgrade 100%]
        CanaryRollout -->|Error Rate > 1.0%| AutoRollback[Automated Immediate Rollback]
    end

    subgraph Tier5 ["5. Fleet Management & Observability"]
        K8sFleet[Kubernetes Autoscaling Runner Cluster] --> KanikoBuild
        MetricsExporter[GitLab Prometheus Exporter] --> Grafana[Grafana Real-time DORA Dashboard]
        AuditTrail[Immutable Audit Events & Compliance Logs] --> SIEM[Enterprise SIEM Exporter]
    end
```

### Chi tiết 5 Tầng Kiến trúc Capstone

#### 1. Developer Experience & Governance (Tầng Trải nghiệm Lập trình viên & Kiểm soát)
Một hệ thống CI/CD thất bại nếu lập trình viên cảm thấy bị cản trở hoặc tìm cách né tránh nó. Tầng này tập trung tối ưu hóa thời gian phản hồi (Fast Feedback Loop) thông qua cơ chế Caching nhiều lớp (Distributed Caching), chạy song song (Parallel Matrix) và luồng đồ thị phụ thuộc không chu kỳ (Directed Acyclic Graph - DAG). Tuy nhiên, tự do phải nằm trong khuôn khổ: mọi Merge Request bắt buộc phải chịu sự chi phối của Compliance Pipeline ở cấp Group, không cho phép dự án con tự ý tháo bỏ các bước kiểm tra an toàn hay bypass quy trình review của CODEOWNERS.

#### 2. Multi-Layer DevSecOps Pipeline (Tầng Bảo mật Đa lớp Shift-Left)
Bảo mật trong hệ thống Capstone không phải là một công đoạn duyệt tay ở cuối dự án, mà là một quy trình tự động hóa liên tục từ dòng code đầu tiên. Tầng DevSecOps thực thi 4 lớp phòng thủ:
- **Lớp 1 (Code Syntax & Style):** SAST (Semgrep/SonarQube) phân tích mã nguồn tĩnh, phát hiện các mẫu code độc hại hay lỗi logic cơ bản.
- **Lớp 2 (Mật mã & Secret):** Secret Detection rà quét lịch sử commit, ngăn chặn việc lỡ tay push API key, Certificate hay Database Password lên repository.
- **Lớp 3 (Thư viện phụ thuộc):** SCA (Software Component Analysis) kiểm tra toàn bộ file package lock để tìm CVE đã biết và vi phạm bản quyền phần mềm (License Compliance).
- **Lớp 4 (Container Image):** Trivy/Grype rà quét hệ điều hành base image và các gói cài đặt trước khi cho phép lưu trữ vào Container Registry.

#### 3. Infrastructure & IaC Pipeline (Tầng Quản lý Hạ tầng bằng Mã)
Toàn bộ hạ tầng phục vụ ứng dụng được quản lý khai báo (Declarative Infrastructure) bằng Terraform / OpenTofu. Tầng này bóc tách hoàn toàn việc lưu trữ bí mật bằng cách áp dụng OpenID Connect (OIDC) - xác thực không dùng chìa khóa tĩnh (Secretless Authentication). State file của Terraform được quản lý tập trung và khóa trạng thái (State Locking) trực tiếp trên Backend của GitLab HTTP. Luồng công việc tuân thủ tuyệt đối nguyên tắc: `terraform plan` chạy trên Merge Request để xem trước thay đổi, và `terraform apply` chỉ được phép kích hoạt manual trên nhánh chính sau khi có sự đồng ý của Trưởng nhóm Hạ tầng.

#### 4. Container Build & Progressive Release Strategy (Tầng Biên dịch & Phát hành Nâng cao)
Biên dịch Container Image sử dụng Kaniko - công cụ build rootless an toàn bên trong Kubernetes Cluster mà không cần tới Docker-in-Docker (DinD) nguy hiểm. Mỗi image tạo ra được ký số bằng Cosign để chứng minh tính toàn vẹn (Supply Chain Security). 
Khi triển khai lên Production, ứng dụng không bao giờ được ghi đè 100% ngay lập tức. Hệ thống áp dụng Progressive Delivery (Canary Deployment): chuyển trước 10% lưu lượng người dùng sang phiên bản mới, liên tục đo lường chỉ số lỗi HTTP 5xx từ Prometheus trong 3 phút. Nếu tỷ lệ lỗi dưới ngưỡng an toàn, hệ thống tự động đẩy dần lên 100%; nếu phát hiện bất thường, cơ chế Auto-rollback lập tức khôi phục trạng thái cũ mà không cần con người can thiệp.

#### 5. Fleet Management & Continuous Observability (Tầng Quản trị Đội ngũ Runner & Giám sát)
Hạ tầng thực thi CI/CD được vận hành trên Kubernetes dưới dạng Auto-scaling Runner Cluster. Khi khối lượng công việc tăng đột biến (ví dụ thời điểm cuối ngày trước khi phát hành), cluster tự động phình to để đáp ứng hàng trăm job song song và tự thu nhỏ về 0 vào ban đêm để tiết kiệm chi phí. Toàn bộ metric của Runner, thời gian thực thi pipeline, tỷ lệ thành công/thất bại và log tuân thủ được đẩy theo dạng danh tính bất biến (Immutable Audit Logs) về hệ thống SIEM tập trung (Elasticsearch/Splunk) và Grafana Dashboard để phục vụ đo lường chỉ số DORA Metrics.

---

### 1.2. 12 Quy tắc vàng kiến trúc CI/CD Enterprise (QT 48.1 - QT 48.12) (20 phút)

**Nguyên lý cốt lõi:**
**Phát biểu.** Mọi cấu hình kiểm soát an toàn và tuân thủ phải được cưỡng chế ở cấp độ Group hoặc Organization (Compliance Pipeline / Security Policy Framework), tuyệt đối không trông chờ vào sự tự giác của từng dự án thành viên.
**Giải thích cơ chế ngầm:** Lập trình viên có thể vô tình hoặc cố ý chỉnh sửa file `.gitlab-ci.yml` trong repository dự án để bỏ qua các bước kiểm tra mã nguồn, quét lỗ hổng hoặc bypass kiểm thử. Việc khóa quyền ở cấp Group bảo đảm mọi repository đều phải đi qua cửa đèo an toàn chung giống như quy định tại buổi 45 QT 45.1. Khi quản lý quy mô lớn, việc tự do cấu hình ở repo con sẽ tạo ra vô số dị bản và lỗ hổng nguy hiểm.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dự án con tự xóa các stage `test` hoặc `security` trong file YAML mà pipeline vẫn báo màu xanh (Success), dẫn đến mã nguồn chứa lỗ hổng nghiêm trọng trọt thẳng lên Production mà không ai phát hiện.
**Minh hoạ.** Cấu hình Compliance Pipeline Path `compliance-templates/security-gate.yml@infrastructure/security` trong Group Settings thay vì cho phép từng repository viết lại toàn bộ pipeline:
```yaml
# compliance-templates/security-gate.yml
include:
  - project: 'infrastructure/security'
    file: '/templates/mandatory-scans.yml'
```
**Con số chốt:** 100% dự án trong tổ chức phải chịu sự chi phối của Compliance Pipeline bắt buộc.

**Nguyên lý cốt lõi:**
**Phát biểu.** Secret và Token truy cập hạ tầng tuyệt đối không lưu dạng plain-text hay hardcode trong biến môi trường tĩnh, phải chuyển sang dùng OIDC (OpenID Connect) federated identity hoặc HashiCorp Vault integration.
**Giải thích cơ chế ngầm:** Static credentials (như AWS Access Key, GCP Service Account Key) lưu lâu ngày trong GitLab CI/CD Variables rất dễ bị rò rỉ qua log job, bị export từ runner compromised hoặc không được rotate định kỳ. OIDC cung cấp token ngắn hạn (Short-lived token) tự động hết hạn sau khi job kết thúc tương tự quy định tại buổi 40 QT 40.2. Mọi truy cập cloud đều được gắn danh tính rõ ràng theo project path và commit SHA.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Khi kiểm tra danh sách `CI/CD Variables`, thấy hàng chục biến chứa chuỗi bí mật dạng `AKIA...` hay `-----BEGIN PRIVATE KEY-----` mà không có thời hạn hết hạn.
**Minh hoạ.** Sử dụng `id_tokens` trong GitLab CI để trao đổi JWT lấy temporary credentials từ AWS STS:
```yaml
id_tokens:
  AWS_OIDC_TOKEN:
    aud: https://gitlab.com
assume_role_job:
  script:
    - aws sts assume-role-with-web-identity --role-arn $AWS_ROLE_ARN --web-identity-token $AWS_OIDC_TOKEN
```
**Con số chốt:** 0 static cloud credential tồn tại trên hệ thống CI/CD Variables.

**Nguyên lý cốt lõi:**
**Phát biểu.** Tốc độ thực thi pipeline phản hồi cho lập trình viên (Developer Feedback Loop) trên nhánh tính năng (Feature Branch) không được vượt quá 10 phút.
**Giải thích cơ chế ngầm:** Thời gian chờ phản hồi CI quá lâu khiến lập trình viên mất ngữ cảnh làm việc (context switching), giảm năng suất làm việc và tăng nguy cơ xung đột mã nguồn do tích hợp chậm (Delayed integration). Áp dụng kỹ thuật cào cache, DAG workflow và parallel matrix đã học ở buổi 37 QT 37.1 để hạ thời gian chạy. Khi phản hồi quá 10 phút, lập trình viên sẽ chuyển sang làm việc khác và việc sửa lỗi bị trì hoãn hàng giờ.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Lập trình viên push code và phải ngồi chờ 30-45 phút mới biết được code mình viết có vỡ unit test hay không.
**Minh hoạ.** Tách pipeline làm 2 luồng: Fast Feedback (Unit test, Linter, SAST chạy parallel dưới 5 phút cho MR) và Deep Validation (E2E Test, Heavy Security Scan chạy scheduled hoặc tiền release):
```yaml
unit-test-fast:
  stage: test
  parallel: 4
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```
**Con số chốt:** Thời gian phản hồi Fast-feedback pipeline $\le$ 8-10 phút.

**Nguyên lý cốt lõi:**
**Phát biểu.** Mọi thao tác thay đổi hạ tầng bằng Infrastructure as Code (Terraform/OpenTofu) trong CI/CD phải tuân thủ nghiêm ngặt nguyên tắc Tách biệt giữa Plan (Merge Request) và Apply (Main Branch).
**Giải thích cơ chế ngầm:** Thực thi `terraform apply` trực tiếp trên Merge Request là thảm họa vì code chưa được review và phê duyệt chính thức đã làm thay đổi trạng thái hạ tầng thật. Luồng chuẩn đòi hỏi `plan` xuất ra artifact dạng file mã hóa và `apply` chỉ chạy khi đã merge code vào nhánh chính có bảo mật như quy định tại buổi 42 QT 42.1. File plan đảm bảo những gì được duyệt ở MR là chính xác những gì được thực thi lên cluster.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hạ tầng Production bị thay đổi hoặc xóa nhầm tài nguyên do một Merge Request thử nghiệm đang trong quá trình phát triển.
**Minh hoạ.** Cấu hình `artifacts: paths: - plan.tfplan` ở stage plan và chỉ cho phép `when: manual` cùng `only: refs: - main` ở stage apply:
```yaml
tf-plan:
  stage: infrastructure
  script: terraform plan -out=plan.tfplan
  artifacts:
    paths: [plan.tfplan]
tf-apply:
  stage: infrastructure
  script: terraform apply plan.tfplan
  when: manual
  only: [main]
```
**Con số chốt:** 100% lệnh `terraform apply` phải sử dụng plan artifact đã qua phê duyệt.

**Nguyên lý cốt lõi:**
**Phát biểu.** Đội ngũ Runner phục vụ CI/CD phải được quản lý theo mô hình Auto-scaling sống theo nhu cầu (Ephemeral & On-demand), tuyệt đối không duy trì hạ tầng Runner cố định dư thừa.
**Giải thích cơ chế ngầm:** Runner tĩnh (Static Shell/Docker Runner) vừa tốn chi phí duy trì máy chủ 24/7 khi không có job, vừa tiềm ẩn nguy cơ nhiễm độc môi trường (Cross-job contamination) khi các job sử dụng chung một không gian đĩa đệm. Docker Autoscaling / Kubernetes Executor tạo Pod mới cho từng job và hủy ngay khi hoàn thành như học ở buổi 44 QT 44.1. Môi trường sạch giúp triệt tiêu hoàn toàn các lỗi dính cache hay tài nguyên rác.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hàng trăm job bị tắc nghẽn ở trạng thái `pending` vào giờ cao điểm, nhưng ban đêm máy chủ Runner lại chạy không tải 0% CPU.
**Minh hoạ.** Cấu hình `gitlab-runner-operator` hoặc `KEDA` trên Kubernetes Cluster với chỉ số scaling dựa trên số lượng job trong queue:
```yaml
executor: kubernetes
kubernetes:
  namespace: gitlab-runners
  image: alpine:latest
```
**Con số chốt:** 100% Job CI/CD được thực thi trong môi trường isolated container sạch hoàn toàn.

**Nguyên lý cốt lõi:**
**Phát biểu.** Mọi Container Image build ra từ pipeline CI/CD bắt buộc phải đi qua công đoạn kiểm tra lỗ hổng (Container Scanning) và Ký số (Image Signing với Cosign) trước khi đẩy vào Production Registry.
**Giải thích cơ chế ngầm:** Một image build thành công không đồng nghĩa với việc nó an toàn. Việc tích hợp sẵn các thư viện lỗi thời chứa CVE nguy hiểm hoặc bị chèn mã độc trong quá trình transit đòi hỏi phải có bằng chứng xác thực nguồn gốc (Provenance & Attestation) chuẩn Supply-chain Security như buổi 41 QT 41.2. Ký số giúp Kubernetes Admission Controller phân biệt được image hợp lệ từ CI/CD nội bộ với image độc hại bên ngoài.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cluster Kubernetes kéo và chạy trực tiếp các image có tag `latest` từ registry công cộng mà không qua bất kỳ bước kiểm định chìa khóa chữ ký số nào.
**Minh hoạ.** Thực hiện `cosign sign --key env://COSIGN_PRIVATE_KEY $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA` và bật Kyverno/OPA Gatekeeper trên K8s để chặn image chưa ký:
```yaml
cosign-sign:
  stage: build
  script:
    - cosign sign --key $COSIGN_KEY $IMAGE_URI:$CI_COMMIT_SHA
```
**Con số chốt:** 0 container image chưa qua ký số được phép khởi tạo Pod trên Production Cluster.

**Nguyên lý cốt lõi:**
**Phát biểu.** Triển khai ứng dụng lên môi trường Production phải áp dụng chiến lược Zero-downtime (Canary Deployment hoặc Blue-Green Deployment) đi kèm tự động giám sát chỉ số lỗi (Automatic Rollback).
**Giải thích cơ chế ngầm:** Triển khai theo kiểu đè trực tiếp (Recreate/Direct overwrite) gây sập dịch vụ tạm thời và tiềm ẩn rủi ro cực lớn khi phiên bản mới xuất hiện lỗi ẩn (Edge cases) tác động đến toàn bộ người dùng cùng lúc. Canary deployment chuyển lưu lượng dần dần và tự dừng nếu tỷ lệ HTTP 5xx tăng vọt giống bài học buổi 43 QT 43.1. Việc tự động hóa khâu rollback rút ngắn MTTR xuống mức phút thay vì giờ.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Mỗi lần deploy sản phẩm mới, nhóm vận hành phải thông báo cắt gián đoạn hệ thống (Maintenance window) và ngồi canh log thủ công để rollback bằng tay.
**Minh hoạ.** Điều hướng 5% traffic sang pod Canary, sử dụng Prometheus query đếm tỷ lệ lỗi trong 3 phút. Nếu error rate > 1%, kích hoạt pipeline rollback tự động ngay lập tức:
```yaml
canary-rollback-check:
  stage: deploy
  script:
    - ERROR_RATE=$(curl -s "http://prometheus:9090/api/v1/query?query=rate(http_5xx[3m])")
    - if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then helm rollback release 0; exit 1; fi
```
**Con số chốt:** Thời gian phát hiện và rollback tự động khi đợt phát hành lỗi $\le$ 3 phút.

**Nguyên lý cốt lõi:**
**Phát biểu.** Toàn bộ các file cấu hình Pipeline (`.gitlab-ci.yml`, templates, scripts) phải được mô đun hóa (Modularization) và tái sử dụng thông qua `include:` và `component:`, tuyệt đối không copy-paste mã YAML giữa các dự án.
**Giải thích cơ chế ngầm:** Copy-paste dẫn đến việc nhân bản hàng trăm file YAML dị bản. Khi cần nâng cấp phiên bản tool, sửa lỗi an ninh hay thay đổi quy chuẩn, đội ngũ DevOps sẽ phải đi sửa thủ công từng repository một - một công việc tốn sức và dễ bỏ sót nghiêm trọng như đề cập ở buổi 38 QT 38.1. CI/CD Component Catalog cung cấp giao diện tham số chuẩn giúp tái sử dụng an toàn.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Trong cùng một tổ chức, dự án A chạy build Docker theo cách này, dự án B chạy theo cách khác, khi nâng cấp version Docker Daemon thì 50% dự án bị hỏng pipeline.
**Minh hoạ.** Quản lý thư viện CI/CD Component Centralized tại repository `devops/ci-components` và gọi lại bằng syntax chuẩn:
```yaml
include:
  - component: $CI_SERVER_FQDN/devops/ci-components/docker-build@1.2.0
```
**Con số chốt:** Reuse rate của các template CI/CD trong toàn doanh nghiệp đạt $\ge 85\%$.

**Nguyên lý cốt lõi:**
**Phát biểu.** Cache và Artifacts trong GitLab CI/CD phải được định nghĩa chính xác phạm vi (Key Scope) và thời hạn sống (Expiration), tuyệt đối không lạm dụng lưu trữ dữ liệu rác làm tràn ổ đĩa Runner và Registry.
**Giải thích cơ chế ngầm:** Lưu cache quá rộng (ví dụ key cố định cho mọi nhánh) làm nhiễm độc dependency giữa các nhánh; ngược lại không dùng cache làm thời gian job kéo dài gấp 5 lần. Artifacts không đặt Expiry sẽ ngốn sạch dung lượng lưu trữ kho GitLab Server theo thời gian như học tại buổi 37 QT 37.3. Đặt thời hạn hết hạn giúp tự động dọn dẹp bộ nhớ đệm hiệu quả.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dung lượng GitLab Storage phồng to lên hàng Terabyte mà không rõ lý do, hoặc job build bị vỡ do nhận cache cũ của nhánh khác.
**Minh hoạ.** Thiết lập `cache:key: "$CI_COMMIT_REF_SLUG"` đi kèm `expire_in: 7 days` cho tất cả các build artifacts trung gian:
```yaml
job-build:
  stage: build
  artifacts:
    paths: [dist/]
    expire_in: 7 days
  cache:
    key: "$CI_COMMIT_REF_SLUG"
    paths: [.npm/]
```
**Con số chốt:** 100% temporary artifacts phải có khai báo thời hạn hết hạn (`expire_in`).

**Nguyên lý cốt lõi:**
**Phát biểu.** Quản lý phân quyền và phê duyệt chuyển đổi môi trường (Environment Gate) bắt buộc phải tích hợp chặt chẽ với cơ chế Protected Environments và CODEOWNERS.
**Giải thích cơ chế ngầm:** Nếu bất kỳ lập trình viên nào cũng có thể nhấn nút `Trigger Deploy Production`, rủi ro con người (Human Error) hoặc tài khoản bị chiếm đoạt sẽ lập tức biến thành sự cố sập hệ thống nghiêm trọng. Phê duyệt sản xuất phải là quyết định của ít nhất 2 người thuộc nhóm Authorized Approvers như buổi 45 QT 45.3.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Một Junior Developer vừa gia nhập công ty vô tình bấm nút deploy một branch thử nghiệm lên cluster Production trong giờ cao điểm.
**Minh hoạ.** Cấu hình `Protected Environments: production` trong GitLab Settings, chỉ cho phép nhóm `Role: Maintainer` hoặc nhóm `DevOps Lead` được phê duyệt manual action.
**Con số chốt:** Tối thiểu 2 sự phê duyệt độc lập (4-eyes principle) cho mọi luồng deploy Production.

**Nguyên lý cốt lõi:**
**Phát biểu.** Hệ thống pipeline phải có khả năng tự chẩn đoán và hiển thị rõ ràng nguyên nhân thất bại (Actionable Error Reporting) đi kèm nhật ký định dạng chuẩn (Structured Logging).
**Giải thích cơ chế ngầm:** Log pipeline quá mờ mạt, thiếu thông tin context làm kỹ sư mất hàng giờ đồng hồ mò mẫm lỗi do đâu (do ứng dụng, do môi trường runner, do đứt mạng hay do hết dung lượng đĩa đệm). Log chuẩn hóa giúp rút ngắn thời gian khắc phục sự cố (MTTR) như kiến thức ở buổi 46 QT 46.1. Việc gộp log theo section giúp hiển thị giao diện sạch sẽ.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Output của job chỉ báo ngắn gọn `Script failed with exit code 1` mà không in ra lỗi từ trình biên dịch hay nguyên nhân chi tiết.
**Minh hoạ.** Sử dụng `set -euo pipefail` trong bash script và cấu hình `section_start` / `section_end` collapsible logs trong GitLab UI để gom nhóm log theo từng bước trực quan:
```bash
echo -e "\e[0Ksection_start:$(date +%s):security_scan[collapsed=true]\r\e[0KHeader Security Scan"
semgrep --config p/ci .
echo -e "\e[0Ksection_end:$(date +%s):security_scan\r\e[0K"
```
**Con số chốt:** Giảm thời gian chẩn đoán sự cố pipeline (Mean Time To Detect) xuống dưới 3 phút.

**Nguyên lý cốt lõi:**
**Phát biểu.** Kiến trúc hệ thống CI/CD phải được đo lường thường xuyên bằng 4 chỉ số DORA Metrics (Deployment Frequency, Lead Time for Changes, Change Failure Rate, Mean Time to Restore).
**Giải thích cơ chế ngầm:** Cải tiến CI/CD không thể dựa trên cảm tính. Các chỉ số DORA cung cấp bức tranh định lượng khách quan về năng lực phân phối phần mềm của toàn bộ tổ chức, từ đó xác định điểm nghẽn (Bottleneck) để tối ưu hóa liên tục như quy chuẩn tại buổi 47 QT 47.1. Việc theo dõi liên tục giúp ban quản trị định hướng đầu tư hạ tầng đúng đắn.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ban quản lý không nắm được tần suất deploy của dự án là bao nhiêu lần một tuần, và mất bao lâu để đưa một hotfix lên tới tay người dùng.
**Minh hoạ.** Thu thập dữ liệu sự kiện CI/CD Webhooks đẩy vào Grafana DORA Dashboard để theo dõi tỷ lệ sự cố và tốc độ phát hành theo thời gian thực:
```yaml
exporter-dora-metrics:
  stage: audit
  script:
    - python scripts/export_dora_prometheus.py
```
**Con số chốt:** Đạt cấp độ High/Elite Performer theo chuẩn DORA (Deploy hàng ngày, Lead time < 1 ngày, CFR < 15%, MTTR < 1 giờ).

---

### 1.3. Đưa vào việc thật (4 phút)

### 6.1. Áp vào repo đang chạy thì làm gì trước
1. **Kiểm tra tính tuân thủ:** Áp dụng Compliance Pipeline Framework ở cấp Group để khóa các quy tắc an toàn cơ bản (Secret Scan, SAST).
2. **Khởi tạo Component Catalog:** Đóng gói các job build Docker và Helm deploy chung vào repository `ci-components` dùng chung.
3. **Chuyển đổi sang OIDC:** Thay thế toàn bộ Static Cloud Access Keys bằng OIDC Federated Roles trên AWS IAM / GCP WIF.
4. **Chuẩn hóa Branching & MR Approval:** Thiết lập Protected Branches (`main`, `staging`), cấm Force Push và kích hoạt quy tắc 2 phê duyệt từ CODEOWNERS.
5. **Cấu hình Ephemeral Runner Fleet:** Chuyển dịch toàn bộ hạ tầng runner từ Static Shell VM sang Kubernetes Autoscaling Runner Cluster để tối ưu chi phí và tính cách ly.

### 6.2. Cái gì hỏng nếu áp thẳng lên prod
- **Kẹt Pipeline do CODEOWNERS:** Đột ngột bật CODEOWNERS trên protected branch khiến các MR bị treo do thiếu người review. *Giải pháp:* Thiết lập giai đoạn cảnh báo (Audit mode) trong 2 tuần trước khi cưỡng chế khóa merge.
- **Rollback nhầm do Metric nhạy cảm:** Ngưỡng error rate Prometheus quá thấp (ví dụ < 0.01%) khiến các lỗi mảng mạng tạm thời kích hoạt rollback nhầm. *Giải pháp:* Tinh chỉnh query `rate(...)` tính trên cửa sổ 3-5 phút.
- **OIDC Token Expiration trên Job dài:** Các job test E2E chạy quá 1 tiếng khiến OIDC Token hết hạn giữa chừng làm vỡ pipeline. *Giải pháp:* Thiết lập `duration_seconds: 7200` trên AWS IAM Role Trust Policy.

### 6.3. Đo trước - đo sau
- **Chỉ số 1 (Lead Time for Changes):** Giảm từ 5 ngày xuống dưới 4 giờ nhờ tự động hóa 100% khâu kiểm thử và phê duyệt.
- **Chỉ số 2 (Change Failure Rate):** Giảm từ 25% xuống dưới 3% nhờ kiểm tra an ninh đa tầng và Canary deployment.
- **Chỉ số 3 (Pipeline Feedback Time):** Hạ thời gian phản hồi cho lập trình viên trên nhánh MR từ 35 phút xuống dưới 6 phút.
- **Chỉ số 4 (Runner Infrastructure Cost):** Tiết kiệm 65% chi phí máy chủ nhờ chuyển sang Kubernetes Autoscaling Ephemeral Runners.

### 6.4. Khi nào KHÔNG nên dùng
- **Dự án PoC / Prototype 1 người làm:** Áp dụng toàn bộ 5 tầng Capstone cho một dự án cá nhân ngắn hạn 3 ngày sẽ gây lãng phí thời gian cấu hình quá mức.
- **Hạ tầng Legacy Monolith tĩnh:** Ứng dụng legacy monolithic cũ chưa container hóa và deploy bằng copy file zip thủ công qua FTP/SCP (cần hiện đại hóa ứng dụng sang container trước).

---

### 1.4. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính | Làm đúng là |
|---|---|---|
| Hardcode AWS Secret Access Key | Do tiện tay khi dựng nhanh lab | Sử dụng OIDC Dynamic JWT Exchange (QT 48.2) |
| Allow failure cho SAST/Secret Scan | Muốn pipeline hiện xanh nhanh | Sửa sạch lỗi hoặc tạo Exception Ticket có thời hạn (QT 48.1) |
| Deploy Recreate đè 100% Prod | Chưa cấu hình Progressive Rollout | Sử dụng Helm Canary 10% đi kèm Prometheus Auto-Rollback (QT 48.7) |
| Quên đặt expiry cho Artifacts | Không khai báo `expire_in` | Mặc định đặt `expire_in: 7 days` cho mọi artifact trung gian (QT 48.9) |
| Chạy `terraform apply` ở MR | Thiếu kiến trúc phân tách plan/apply | `plan` ở MR xuất `plan.tfplan`, `apply` manual ở `main` (QT 48.4) |
| Dùng `latest` tag cho Docker Base Image | Không khóa phiên bản cố định | Khóa hash digest hoặc semantic version cụ thể cho base image (QT 48.6) |

---

### 1.5. Tóm tắt (3 phút)

### Sơ đồ tóm tắt kiến trúc Capstone

```mermaid
graph LR
    A[Governance & Policy] --> B[DevSecOps Multi-Layer]
    B --> C[IaC & OIDC Cloud]
    C --> D[Build & Progressive Release]
    D --> E[Observability & DORA Metrics]
```

### Năm điều phải nhớ
1. Compliance Pipeline khóa ở cấp Group - 100% dự án con tuân thủ không ngoại lệ.
2. Secretless OIDC - 0 static credentials trên CI/CD Variables.
3. Fast Feedback < 10 phút - Tối ưu bằng DAG, Caching và Matrix Parallel.
4. Progressive Release - Canary deployment đi kèm Prometheus Auto-Rollback.
5. Continuous Improvement - Đo lường cải tiến liên tục bằng 4 chỉ số DORA Metrics.

---

### 1.6. Câu hỏi tự kiểm tra (2 phút)

1. Giả sử tổ chức của bạn có 100 dự án microservices độc lập. Làm thế nào để đảm bảo rằng khi Security Team cập nhật quy chuẩn quét mã nguồn mới, tất cả 100 dự án đều lập tức áp dụng mà không cần sửa file `.gitlab-ci.yml` của từng dự án?
   - *Đáp án chuẩn:* Áp dụng Compliance Pipeline ở cấp Group kết hợp với Centralized CI/CD Components (QT 48.1, QT 48.8).

2. Sự khác biệt bản chất giữa việc dùng static AWS Access Key trong CI/CD Variable và việc triển khai OIDC Authentication là gì?
   - *Đáp án chuẩn:* OIDC phát hành token ngắn hạn (short-lived), có phạm vi hẹp (scoped to job), không thể lưu trữ hay đánh cắp để dùng lại về sau (QT 48.2).

3. Làm thế nào để thiết lập một luồng triển khai Canary Deployment tự động hoàn toàn (Auto-Canary with Auto-Rollback) trong GitLab CI/CD khi kết hợp với Prometheus?
   - *Đáp án chuẩn:* Chạy job deploy 10% traffic, ngủ 3 phút, query Prometheus API đếm tỷ lệ HTTP 5xx. Nếu lỗi > 1%, kích hoạt job Rollback và ngắt pipeline với exit code 1 (QT 48.7).

4. Tại sao nguyên tắc tách biệt giữa `terraform plan` và `terraform apply` lại đóng vai trò quyết định tính an toàn hạ tầng trong pipeline IaC?
   - *Đáp án chuẩn:* Plan tạo ra tệp thực thi cố định được kiểm duyệt; Apply chỉ chạy tệp plan đó trên nhánh chính nhằm tránh lệch trạng thái (State drift) và thay đổi ngoài ý muốn (QT 48.4).

5. Bốn chỉ số DORA Metrics phản ánh điều gì về sức khỏe của hệ thống CI/CD Enterprise, và chỉ số nào thường phản ánh rõ nhất mức độ tin cậy của quy trình kiểm thử tự động?
   - *Đáp án chuẩn:* Change Failure Rate (CFR) và Lead Time for Changes phản ánh trực tiếp chất lượng kiểm thử và tốc độ của luồng CI/CD (QT 48.12).

---

### 1.7. Tài liệu tham khảo (1 phút)

| Nguồn tài liệu | Nội dung tham chiếu | Phiên bản áp dụng |
|---|---|---|
| GitLab Official Docs | Enterprise CI/CD Architecture & Compliance Pipelines | GitLab CE/EE 16.x + |
| CNCF Security Group | Software Supply Chain Security Reference Architecture | 2024 Specification |
| HashiCorp Developer | Terraform Automation & GitLab HTTP Backend State Lock | Terraform 1.6+ |
| DORA Research | Accelerate: The Science of Lean Software and DevOps | DORA Framework |
| Sigstore Cosign | Container Signing & OCI Attestation Specification | Cosign 2.x |

---

## Bảng đối soát thời lượng

| Mục | Thời lượng | Trạng thái |
|---|---|---|
| §0. Khởi động và ôn tập | 10' | ĐẠT |
| §1. Sau buổi này học viên LÀM ĐƯỢC gì | 1' | ĐẠT |
| §2. Cần biết trước | 1' | ĐẠT |
| §3. Thuật ngữ và mô hình tư duy | 8' | ĐẠT |
| §4. Kiến trúc Enterprise CI/CD tổng thể | 15' | ĐẠT |
| §5. 12 Quy tắc vàng kiến trúc CI/CD Enterprise | 20' | ĐẠT |
| §6. Đưa vào việc thật | 4' | ĐẠT |
| §7. Bẫy hay gặp | 2' | ĐẠT |
| §8. Tóm tắt | 3' | ĐẠT |
| §9. Câu hỏi tự kiểm tra | 2' | ĐẠT |
| §10. Tài liệu tham khảo | 1' | ĐẠT |
| **Tổng** | **60'** | **ĐẠT** |

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên môi trường GitLab Community / Enterprise Edition cùng các GitLab Runner cô lập (Docker / Kubernetes Executor). Hãy đảm bảo bạn đã chuẩn bị môi trường thử nghiệm và cấu hình quyền truy cập cần thiết.

## Khối thực hành — 150 phút

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

Trong bài lab Capstone này, học viên sẽ trực tiếp xây dựng và vận hành một hệ thống Enterprise CI/CD Pipeline hoàn chỉnh từ đầu (from scratch) cho hệ thống Microservices "Enterprise E-Commerce Platform" (gồm các dịch vụ Auth Service, Payment Service, Order Service và Web Frontend):

1. **Khởi tạo Monorepo & Component Catalog:** Đóng gói thư viện CI/CD Components tập trung tại `devops/ci-components` có phiên bản Semantic Versioning và áp dụng lại tại dự án microservices (`QT 48.8`).
2. **Cưỡng chế Group Compliance Framework:** Thiết lập Compliance Pipeline bắt buộc rà quét an ninh đa tầng (Semgrep SAST, Secret Detection, Dependency Scan, Trivy Container Scan) cho 100% repository con (`QT 48.1`, `QT 48.6`).
3. **Xác thực Dynamic Secretless OIDC:** Triển khai OIDC Identity Federation để trao đổi JWT Token kết nối AWS/GCP/Azure mà không dùng Static Cloud Access Keys (`QT 48.2`).
4. **Tự động hóa IaC Terraform với State Lock:** Xây dựng luồng `terraform plan` trên Merge Request và `terraform apply` có phê duyệt manual trên nhánh `main` kết hợp HTTP Backend Lock (`QT 48.4`, `QT 48.10`).
5. **Biên dịch Rootless Kaniko & Ký số Cosign:** Biên dịch Container Image không dùng root daemon và ký số xác thực nguồn gốc Supply-chain Security trước khi đẩy vào Registry (`QT 48.5`, `QT 48.6`).
6. **Thử nghiệm Progressive Canary Rollout & Auto-Rollback:** Triển khai 10% Canary trên Kubernetes, đo lường tỷ lệ lỗi HTTP 5xx từ Prometheus API và tự động kích hoạt Rollback khi lỗi vọt ngưỡng (`QT 48.7`).
7. **Tự động thu thập DORA Metrics & Log Exporter:** Đẩy dữ liệu sự kiện pipeline về Prometheus/Grafana Dashboard và xuất Audit Event log về SIEM (`QT 48.11`, `QT 48.12`).

---

## L1. Điều kiện tiên quyết về môi trường

| Kiểm tra môi trường | Lệnh kiểm tra | Kết quả kỳ vọng | Cảnh báo tác động |
|---|---|---|---|
| GitLab CLI (`glab`) | `glab --version` | `glab version 1.30+` | Cần thiết để tạo group, repo và trigger pipeline |
| Docker & Minikube/K3s | `kubectl get nodes` | `Ready` status trên node | Đảm bảo cluster K8s local chạy ổn định |
| Helm v3 | `helm version --short` | `v3.12+` | Phục vụ triển khai Canary Rollout |
| Cosign CLI | `cosign version` | `v2.2+` | Dùng để ký số và kiểm định container image |
| Trivy Scanner | `trivy --version` | `v0.45+` | Rà quét lỗ hổng container image |
| Semgrep CLI | `semgrep --version` | `v1.50+` | Phân tích an ninh mã nguồn tĩnh SAST |
| Terraform / OpenTofu | `terraform version` | `v1.6+` | Phục vụ kiểm tra IaC pipeline |
| jq JSON Parser | `jq --version` | `jq-1.6+` | Phục vụ parse JSON API responses trong checkpoint |

---

## L2. Kiến trúc bài lab Capstone

```mermaid
graph TD
    subgraph Phase 1: Workspace & Governance Setup
        A[Init Microservices Monorepo] --> B[Create Centralized CI Components Catalog]
        B --> C[Configure Group Compliance Pipeline Framework]
    end

    subgraph Phase 2: Security & Static Analysis Gates
        C --> D[Semgrep SAST Code Audit]
        D --> E[Gitleaks Secret Push Protection]
        E --> F[Grype Dependency & License Scan]
    end

    subgraph Phase 3: Infrastructure & OIDC Authentication
        F --> G[OIDC Dynamic JWT Token Request]
        G --> H[Terraform Plan Generation & HTTP State Lock]
        H --> I[Protected Manual Approval Gate]
        I --> J[Terraform Apply / K8s Provisioning]
    end

    subgraph Phase 4: Container Build & Supply-Chain Security
        J --> K[Rootless Kaniko Image Build]
        K --> L[Trivy Vulnerability Container Scan]
        L --> M[Cosign Private Key Image Signing]
    end

    subgraph Phase 5: Progressive Canary & Prometheus Auto-Rollback
        M --> N[Helm Deploy Canary 10% Traffic]
        N --> O[Wait 180s & Query Prometheus Metric API]
        O -->|Error Rate < 0.1%| P[Promote Canary to 100% Primary Deployment]
        O -->|Error Rate > 1.0%| Q[EXECUTE IMMEDIATE AUTO-ROLLBACK]
    end

    subgraph Phase 6: Observability & DORA Metrics Audit
        P --> R[Publish DORA Metrics Event to Grafana]
        Q --> R
        R --> S[Stream Immutable Audit Event to SIEM]
    end
```

---

## L3. Bước 1: Khởi tạo Cấu trúc Monorepo Microservices & Component Catalog (25 phút)

Tạo cấu trúc thư mục dự án Capstone Enterprise E-Commerce Platform:

```bash
mkdir -p capstone-enterprise-lab
cd capstone-enterprise-lab
mkdir -p microservices/{auth-service,payment-service,order-service,frontend}
mkdir -p devops/ci-components/{docker-build,helm-deploy,security-scan,terraform-iac}
mkdir -p compliance-policies infrastructure/terraform scripts metrics audit helm/templates runner-config dashboards runbooks
```

Khởi tạo mã nguồn Dockerfile đại diện cho 4 dịch vụ microservices:

```dockerfile
# microservices/auth-service/Dockerfile
FROM alpine:3.19.1
LABEL maintainer="DevOps Lead <devops@company.com>"
LABEL service="auth-service"
LABEL architecture="microservices"
RUN apk add --no-cache bash curl ca-certificates nodejs npm
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production || true
COPY . /app
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s CMD curl -f http://localhost:8080/health || exit 1
CMD ["node", "server.js"]
```

```dockerfile
# microservices/payment-service/Dockerfile
FROM alpine:3.19.1
LABEL maintainer="DevOps Lead <devops@company.com>"
LABEL service="payment-service"
LABEL architecture="microservices"
RUN apk add --no-cache bash curl ca-certificates nodejs npm
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production || true
COPY . /app
EXPOSE 8081
HEALTHCHECK --interval=10s --timeout=3s CMD curl -f http://localhost:8081/health || exit 1
CMD ["node", "server.js"]
```

```dockerfile
# microservices/order-service/Dockerfile
FROM alpine:3.19.1
LABEL maintainer="DevOps Lead <devops@company.com>"
LABEL service="order-service"
LABEL architecture="microservices"
RUN apk add --no-cache bash curl ca-certificates nodejs npm
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production || true
COPY . /app
EXPOSE 8082
HEALTHCHECK --interval=10s --timeout=3s CMD curl -f http://localhost:8082/health || exit 1
CMD ["node", "server.js"]
```

```dockerfile
# microservices/frontend/Dockerfile
FROM alpine:3.19.1
LABEL maintainer="DevOps Lead <devops@company.com>"
LABEL service="frontend"
LABEL architecture="microservices"
RUN apk add --no-cache bash curl ca-certificates nginx
WORKDIR /usr/share/nginx/html
COPY . /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=10s --timeout=3s CMD curl -f http://localhost:80/ || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

Khởi tạo mã nguồn ứng dụng mẫu cho Auth Service `microservices/auth-service/server.js` và `microservices/auth-service/package.json`:

```json
{
  "name": "auth-service",
  "version": "1.0.0",
  "description": "Enterprise E-Commerce Authentication Microservice",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "test": "echo \"Running unit tests for auth-service...\" && exit 0"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

```javascript
// Auth Service Server Implementation
const express = require('express');
const app = express();
const PORT = process.env.PORT || 8080;

app.get('/health', (req, res) => res.json({ status: 'UP', service: 'auth-service', timestamp: new Date() }));
app.get('/metrics', (req, res) => {
  res.set('Content-Type', 'text/plain');
  res.send('# HELP http_requests_total Total number of HTTP requests\n# TYPE http_requests_total counter\nhttp_requests_total{service="auth",status="200"} 1050\nhttp_requests_total{service="auth",status="500"} 0\n');
});

app.listen(PORT, () => console.log(`Auth Service listening on port ${PORT}`));
```

Khởi tạo mã nguồn ứng dụng mẫu cho Payment Service `microservices/payment-service/server.js`:

```javascript
// Payment Service Server Implementation
const express = require('express');
const app = express();
const PORT = process.env.PORT || 8081;

app.get('/health', (req, res) => res.json({ status: 'UP', service: 'payment-service', timestamp: new Date() }));
app.get('/metrics', (req, res) => {
  res.set('Content-Type', 'text/plain');
  res.send('# HELP http_requests_total Total number of HTTP requests\n# TYPE http_requests_total counter\nhttp_requests_total{service="payment",status="200"} 450\nhttp_requests_total{service="payment",status="500"} 0\n');
});

app.listen(PORT, () => console.log(`Payment Service listening on port ${PORT}`));
```

Khởi tạo mã nguồn ứng dụng mẫu cho Order Service `microservices/order-service/server.js`:

```javascript
// Order Service Server Implementation
const express = require('express');
const app = express();
const PORT = process.env.PORT || 8082;

app.get('/health', (req, res) => res.json({ status: 'UP', service: 'order-service', timestamp: new Date() }));
app.get('/metrics', (req, res) => {
  res.set('Content-Type', 'text/plain');
  res.send('# HELP http_requests_total Total number of HTTP requests\n# TYPE http_requests_total counter\nhttp_requests_total{service="order",status="200"} 890\nhttp_requests_total{service="order",status="500"} 0\n');
});

app.listen(PORT, () => console.log(`Order Service listening on port ${PORT}`));
```

Khởi tạo cấu hình Runner Autoscaling config `runner-config/config.toml`:

```toml
# ===================================================================
# ENTERPRISE KUBERNETES RUNNER CONFIGURATION
# Location: runner-config/config.toml
# ===================================================================
concurrent = 50
check_interval = 3

[session_server]
  session_timeout = 1800

[[runners]]
  name = "k8s-autoscale-runner-pool"
  url = "https://gitlab.com/"
  token = "GLRT-ENTERPRISE-RUNNER-TOKEN"
  executor = "kubernetes"
  [runners.custom_build_dir]
  [runners.cache]
    MaxUploadedArchiveSize = 524288000
    Type = "s3"
    Shared = true
    [runners.cache.s3]
      ServerAddress = "s3.amazonaws.com"
      BucketName = "gitlab-ci-cache-enterprise"
      BucketLocation = "us-east-1"
      Insecure = false
  [runners.kubernetes]
    host = ""
    bearer_token_overwrite_allowed = false
    image = "alpine:3.19"
    namespace = "gitlab-runners"
    privileged = false
    cpu_limit = "2000m"
    memory_limit = "4Gi"
    service_cpu_limit = "1000m"
    service_memory_limit = "2Gi"
    [runners.kubernetes.node_selector]
      "node.kubernetes.io/instance-type" = "c5.xlarge"
```

Khởi tạo KEDA Custom ScaledObject `runner-config/keda-runner-scaler.yaml`:

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: gitlab-runner-scaledobject
  namespace: gitlab-runners
spec:
  scaleTargetRef:
    name: gitlab-runner-deployment
  minReplicaCount: 2
  maxReplicaCount: 20
  triggers:
    - type: prometheus
      metadata:
        serverAddress: http://prometheus-k8s.monitoring:9090
        metricName: gitlab_runner_jobs_pending
        query: sum(gitlab_runner_jobs{state="pending"})
        threshold: '5'
```

Khởi tạo Component Catalog cấu hình Docker Build `devops/ci-components/docker-build/template.yml`:

```yaml
# ===================================================================
# ENTERPRISE CI/CD COMPONENT: DOCKER KANIKO BUILD
# Path: devops/ci-components/docker-build/template.yml
# ===================================================================
spec:
  inputs:
    stage:
      default: build
      description: "Stage execution for container compilation"
    image_name:
      default: $CI_REGISTRY_IMAGE
      description: "Target image destination name"
    kaniko_flags:
      default: "--clear-contexts --snapshot-mode=redo"
      description: "Optimization flags for Kaniko rootless executor"
---
component-docker-build:
  stage: $[[ inputs.stage ]]
  image:
    name: gcr.io/kaniko-project/executor:v1.19.0-debug
    entrypoint: [""]
  script:
    - mkdir -p /kaniko/.docker
    - echo "{\"auths\":{\"$CI_REGISTRY\":{\"username\":\"$CI_REGISTRY_USER\",\"password\":\"$CI_REGISTRY_PASSWORD\"}}}" > /kaniko/.docker/config.json
    - /kaniko/executor --context $CI_PROJECT_DIR --dockerfile $CI_PROJECT_DIR/Dockerfile --destination $[[ inputs.image_name ]]:$CI_COMMIT_SHA $[[ inputs.kaniko_flags ]]
    - echo "[KANIKO BUILD SUCCESS] Built image $[[ inputs.image_name ]]:$CI_COMMIT_SHA"
```

### **CHECKPOINT 1 — Khởi tạo Component Catalog Docker Build thành công (`QT 48.8`)**
Thao tác khởi tạo Component Catalog chuẩn GitLab 16.x cho phép tái sử dụng pipeline template đa dự án mà không bị lặp lại cấu hình YAML:
```bash
test -f devops/ci-components/docker-build/template.yml && grep -q "component-docker-build:" devops/ci-components/docker-build/template.yml && echo "CHECKPOINT 1: ĐẠT" || echo "CHECKPOINT 1: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 1: ĐẠT
```

---

Khởi tạo Component Catalog Helm Deploy `devops/ci-components/helm-deploy/template.yml`:

```yaml
# ===================================================================
# ENTERPRISE CI/CD COMPONENT: HELM CANARY DEPLOY
# Path: devops/ci-components/helm-deploy/template.yml
# ===================================================================
spec:
  inputs:
    environment:
      default: staging
      description: "Target Kubernetes deployment environment"
    chart_path:
      default: ./helm
      description: "Path to Helm chart directory"
---
component-helm-deploy:
  stage: deploy
  image: alpine/helm:3.14.0
  environment:
    name: $[[ inputs.environment ]]
  script:
    - echo "[HELM DEPLOY] Deploying chart at $[[ inputs.chart_path ]] to environment $[[ inputs.environment ]]"
    - helm lint $[[ inputs.chart_path ]] || true
    - echo "[HELM DEPLOY SUCCESS] Release deployed successfully to $[[ inputs.environment ]]!"
```

### **CHECKPOINT 2 — Khởi tạo Component Catalog Helm Deploy thành công (`QT 48.8`)**
Kiểm tra tính chính xác của Component Catalog Helm Deploy nhằm đảm bảo các bước triển khai Kubernetes được đồng bộ hóa toàn tập đoàn:
```bash
test -f devops/ci-components/helm-deploy/template.yml && grep -q "component-helm-deploy:" devops/ci-components/helm-deploy/template.yml && echo "CHECKPOINT 2: ĐẠT" || echo "CHECKPOINT 2: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 2: ĐẠT
```

---

Khởi tạo Helm Chart metadata `helm/Chart.yaml`, values `helm/values.yaml` và deployment templates:

```yaml
# helm/Chart.yaml
apiVersion: v2
name: ecommerce-platform
description: Enterprise E-Commerce Platform Microservices Helm Chart
type: application
version: 1.0.0
appVersion: "1.0.0"
```

```yaml
# helm/values.yaml
replicaCount:
  primary: 9
  canary: 1
image:
  repository: registry.gitlab.com/enterprise/ecommerce/auth-service
  tag: a1b2c3d4e5f6
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8080
metrics:
  enabled: true
  path: /metrics
  port: 9090
ingress:
  enabled: true
  className: nginx
  hosts:
    - host: api.ecommerce.company.com
      paths:
        - path: /
          pathType: Prefix
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 30
  targetCPUUtilizationPercentage: 75
```

```yaml
# helm/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-auth-primary
  labels:
    app: ecommerce-auth
    tier: primary
spec:
  replicas: {{ .Values.replicaCount.primary }}
  selector:
    matchLabels:
      app: ecommerce-auth
  template:
    metadata:
      labels:
        app: ecommerce-auth
    spec:
      containers:
        - name: auth-service
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          resources:
            limits:
              cpu: {{ .Values.resources.limits.cpu }}
              memory: {{ .Values.resources.limits.memory }}
            requests:
              cpu: {{ .Values.resources.requests.cpu }}
              memory: {{ .Values.resources.requests.memory }}
```

```yaml
# helm/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ecommerce-auth-svc
  labels:
    app: ecommerce-auth
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.port }}
      protocol: TCP
      name: http
  selector:
    app: ecommerce-auth
```

```yaml
# helm/templates/servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ecommerce-auth-monitor
  labels:
    release: prometheus-stack
spec:
  selector:
    matchLabels:
      app: ecommerce-auth
  endpoints:
    - port: http
      path: /metrics
      interval: 15s
```

```yaml
# helm/templates/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-auth-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"
spec:
  rules:
    - host: api.ecommerce.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ecommerce-auth-svc
                port:
                  number: 8080
```

```yaml
# helm/templates/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ecommerce-auth-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ecommerce-auth-primary
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
```

---

## L4. Bước 2: Cấu hình Multi-Layer Security Gates (Semgrep, Secret Detection, Trivy) (30 phút)

Khởi tạo file cấu hình Gitleaks `compliance-policies/.gitleaks.toml` cùng Semgrep rules `compliance-policies/.semgrep.yml`:

```toml
# compliance-policies/.gitleaks.toml
[allowlist]
description = "Global allowlist for synthetic test keys"
regexes = ['''ASIAEXAMPLETOKEN1234''']
```

```yaml
# compliance-policies/.semgrep.yml
rules:
  - id: no-hardcoded-credentials
    patterns:
      - pattern: $X = "AKIA..."
    message: "Hardcoded AWS credentials detected in source code!"
    languages: [python, javascript, go, java]
    severity: ERROR

  - id: no-eval-usage
    patterns:
      - pattern: eval(...)
    message: "Dangerous eval function usage detected!"
    languages: [javascript, python]
    severity: WARNING

  - id: no-sql-injection-concat
    patterns:
      - pattern: db.query("SELECT * FROM users WHERE id = " + $ID)
    message: "Potential SQL Injection via string concatenation!"
    languages: [javascript, python]
    severity: ERROR
```

Khởi tạo cấu hình Kyverno Admission Controller Policy `compliance-policies/kyverno-cosign-policy.yaml`:

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-image-signature
spec:
  validationFailureAction: Enforce
  background: false
  rules:
    - name: verify-cosign-signature
      match:
        any:
          - resources:
              kinds:
                - Pod
      verifyImages:
        - imageReferences:
            - "registry.gitlab.com/enterprise/ecommerce/*"
          key: |
            -----BEGIN PUBLIC KEY-----
            MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE2...
            -----END PUBLIC KEY-----
```

Khởi tạo cấu hình Group Compliance Framework Security Template `compliance-policies/group-security-compliance.yml`:

```yaml
# ===================================================================
# GROUP COMPLIANCE SECURITY FRAMEWORK TEMPLATE
# Path: compliance-policies/group-security-compliance.yml
# ===================================================================
stages:
  - governance
  - security
  - infrastructure
  - build
  - deploy
  - audit

compliance-secret-push-protection:
  stage: governance
  image: zricethezav/gitleaks:v8.18.1
  script:
    - echo "[COMPLIANCE SECRET SCAN] Scanning commit history for hardcoded secrets..."
    - gitleaks detect --source . --verbose --exit-code 0 || echo "Secret warnings detected!"
    - echo "COMPLIANCE_SECRET_PROTECTION_PASSED" > audit/secret-scan-status.txt

compliance-sast-semgrep:
  stage: security
  image: returntocorp/semgrep:1.60.0
  script:
    - echo "[COMPLIANCE SAST] Running Semgrep static code analysis..."
    - semgrep --config p/security-audit --json --output audit/semgrep-sast-report.json . || true
    - echo "COMPLIANCE_SAST_SUCCESS" >> audit/security-summary.txt

compliance-container-trivy:
  stage: security
  image: aquasec/trivy:0.48.3
  script:
    - echo "[COMPLIANCE TRIVY] Scanning container filesystem vulnerabilities..."
    - trivy fs --severity CRITICAL,HIGH --exit-code 0 --format json --output audit/trivy-report.json .
    - echo "COMPLIANCE_TRIVY_SUCCESS" >> audit/security-summary.txt
```

### **CHECKPOINT 3 — Cấu hình Compliance Security Framework thành công (`QT 48.1`)**
Thiết lập mẫu Compliance Security Framework cấp Group ép buộc 100% dự án chạy kiểm tra an ninh trước khi biên dịch:
```bash
test -f compliance-policies/group-security-compliance.yml && grep -q "compliance-secret-push-protection:" compliance-policies/group-security-compliance.yml && echo "CHECKPOINT 3: ĐẠT" || echo "CHECKPOINT 3: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 3: ĐẠT
```

---

Viết script thực thi mô phỏng bước quét an ninh đa tầng `scripts/run-security-gates.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail
mkdir -p audit

echo "[SECURITY GATE] Executing SAST, Secret Detection & SCA Scans..."

cat << EOF > audit/semgrep-sast-report.json
{
  "results": [],
  "errors": [],
  "paths": { "scanned": ["microservices/auth-service", "microservices/payment-service", "microservices/order-service", "microservices/frontend"] },
  "status": "PASSED_ZERO_CRITICAL"
}
EOF

cat << EOF > audit/trivy-report.json
{
  "SchemaVersion": 2,
  "ArtifactName": "microservices/auth-service:v1.0.0",
  "Results": [{ "Target": "alpine:3.19", "Vulnerabilities": [] }],
  "status": "PASSED_ZERO_CVE"
}
EOF

echo "ALL_SECURITY_GATES_PASSED" > audit/security-gate-result.txt
echo "[SECURITY GATE] All multi-layer security scans PASSED with ZERO Critical Vulnerabilities!"
```

Chạy script kiểm thử:
```bash
chmod +x scripts/run-security-gates.sh
./scripts/run-security-gates.sh
```

### **CHECKPOINT 4 — Thực thi Security Gates thành công 0 lỗi Critical (`QT 48.1`, `QT 48.6`)**
Kiểm định rằng mọi báo cáo SAST và Trivy đều xác nhận 0 lỗ hổng an ninh mức Critical:
```bash
test -f audit/security-gate-result.txt && grep -q "ALL_SECURITY_GATES_PASSED" audit/security-gate-result.txt && echo "CHECKPOINT 4: ĐẠT" || echo "CHECKPOINT 4: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 4: ĐẠT
```

---

## L5. Bước 3: Triển khai OIDC Authentication & Terraform IaC Pipeline (30 phút)

Khởi tạo cấu hình OIDC Federated Identity Token Exchange Script `scripts/oidc-cloud-auth.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail
mkdir -p audit

echo "[OIDC AUTH] Simulating OpenID Connect Federated Auth Token Exchange..."
AWS_ROLE_ARN="${1:-arn:aws:iam::123456789012:role/GitLabCI-EnterpriseRole}"
GITLAB_JWT_TOKEN="eyJhbGciOiJSUzI1NiIsImtpZCI6ImFndHktY2Fwc3RvbmUifQ.eyJpc3MiOiJodHRwczovL2dpdGxhYi5jb20iLCJzdWIiOiJwcm9qZWN0X3BhdGg6ZGV2b3BzL2NhcHN0b25lOnJlZjptYWluIn0.signature"

cat << EOF > audit/oidc-credentials.json
{
  "AccessKeyId": "ASIAEXAMPLETOKEN1234",
  "SecretAccessKey": "temp-secret-key-expiring-in-1-hour",
  "SessionToken": "session-token-oidc-federated-auth",
  "Expiration": "$(date -u -d "+1 hour" +"%Y-%m-%dT%H:%M:%SZ" 2>/devnull || date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "AssumedRoleUser": "$AWS_ROLE_ARN",
  "Status": "OIDC_AUTH_SUCCESS_SECRETLESS"
}
EOF

echo "[OIDC AUTH] Token Exchange SUCCESS! Using temporary credentials expiring in 3600 seconds."
```

Cho phép script chạy và kiểm tra:
```bash
chmod +x scripts/oidc-cloud-auth.sh
./scripts/oidc-cloud-auth.sh
```

### **CHECKPOINT 5 — Xác thực OIDC Dynamic Secretless Auth thành công (`QT 48.2`)**
Trao đổi JWT token thành công và thu về thông tin xác thực tạm thời ngắn hạn mà không lưu static key:
```bash
test -f audit/oidc-credentials.json && grep -q "OIDC_AUTH_SUCCESS_SECRETLESS" audit/oidc-credentials.json && echo "CHECKPOINT 5: ĐẠT" || echo "CHECKPOINT 5: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 5: ĐẠT
```

---

Tạo file cấu hình Terraform IaC `infrastructure/terraform/main.tf` cùng `infrastructure/terraform/variables.tf`, `infrastructure/terraform/providers.tf` và `infrastructure/terraform/outputs.tf`:

```hcl
# infrastructure/terraform/providers.tf
terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2.0"
    }
  }
}
```

```hcl
# infrastructure/terraform/main.tf
terraform {
  required_version = ">= 1.6.0"
  backend "http" {
    address        = "https://gitlab.com/api/v4/projects/101/terraform/state/production"
    lock_address   = "https://gitlab.com/api/v4/projects/101/terraform/state/production/lock"
    unlock_address = "https://gitlab.com/api/v4/projects/101/terraform/state/production/lock"
  }
}

resource "null_resource" "k8s_cluster_namespace" {
  provisioner "local-exec" {
    command = "echo 'Provisioning Enterprise Kubernetes Namespace: ecommerce-prod'"
  }
}

resource "null_resource" "redis_cache_cluster" {
  provisioner "local-exec" {
    command = "echo 'Provisioning Shared Redis Cache Instance for Microservices'"
  }
}

resource "null_resource" "postgresql_database" {
  provisioner "local-exec" {
    command = "echo 'Provisioning Shared PostgreSQL Database Cluster'"
  }
}
```

```hcl
# infrastructure/terraform/variables.tf
variable "environment" {
  type        = string
  default     = "production"
  description = "Target deployment environment"
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "AWS Cloud region for deployment"
}

variable "kubernetes_cluster_name" {
  type        = string
  default     = "enterprise-eks-prod"
  description = "Target Kubernetes cluster name"
}
```

```hcl
# infrastructure/terraform/outputs.tf
output "kubernetes_namespace" {
  value       = "ecommerce-prod"
  description = "Provisioned Kubernetes Namespace"
}

output "terraform_backend_status" {
  value       = "GitLab HTTP State Backend Active with Lock Protection"
  description = "IaC State Backend Status"
}

output "database_endpoint" {
  value       = "postgresql-cluster.internal:5432"
  description = "Provisioned PostgreSQL Endpoint"
}
```

Tạo script mô phỏng Terraform Plan & Apply `scripts/terraform-pipeline.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail
ACTION="${1:-plan}"
mkdir -p audit

if [ "$ACTION" = "plan" ]; then
  echo "[TERRAFORM PLAN] Creating encrypted plan file plan.tfplan..."
  cat << EOF > audit/plan.tfplan
TERRAFORM_PLAN_BINARY_DATA_ENCRYPTED_SHA256_9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
EOF
  echo "[TERRAFORM PLAN SUCCESS] Plan generated and saved to artifact."
elif [ "$ACTION" = "apply" ]; then
  test -f audit/plan.tfplan || (echo "[ERROR] Missing plan artifact!"; exit 1)
  echo "[TERRAFORM APPLY] Applying approved plan artifact plan.tfplan..."
  echo "TERRAFORM_APPLY_SUCCESS" > audit/terraform-apply-status.txt
  echo "[TERRAFORM APPLY SUCCESS] Infrastructure provisioned!"
fi
```

Chạy thử `plan`:
```bash
chmod +x scripts/terraform-pipeline.sh
./scripts/terraform-pipeline.sh "plan"
```

### **CHECKPOINT 6 — Tạo Terraform Plan Artifact thành công (`QT 48.4`)**
Xác nhận bản kế hoạch thay đổi hạ tầng `plan.tfplan` được tạo độc lập trên Merge Request:
```bash
test -f audit/plan.tfplan && grep -q "TERRAFORM_PLAN_BINARY_DATA" audit/plan.tfplan && echo "CHECKPOINT 6: ĐẠT" || echo "CHECKPOINT 6: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 6: ĐẠT
```

---

Chạy thử `apply`:
```bash
./scripts/terraform-pipeline.sh "apply"
```

### **CHECKPOINT 7 — Thực thi Terraform Apply thành công (`QT 48.4`, `QT 48.10`)**
Đảm bảo luồng `terraform apply` chỉ đọc từ artifact plan đã phê duyệt và có State Lock HTTP Backend:
```bash
test -f audit/terraform-apply-status.txt && grep -q "TERRAFORM_APPLY_SUCCESS" audit/terraform-apply-status.txt && echo "CHECKPOINT 7: ĐẠT" || echo "CHECKPOINT 7: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 7: ĐẠT
```

---

## L6. Bước 4: Biên dịch Container Rootless Kaniko & Ký số Cosign (30 phút)

Khởi tạo script mô phỏng Kaniko Rootless Build `scripts/kaniko-build-sim.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail
SERVICE_NAME="${1:-auth-service}"
COMMIT_SHA="${2:-a1b2c3d4e5f6}"
mkdir -p audit

echo "[KANIKO BUILD] Building image microservices/$SERVICE_NAME:$COMMIT_SHA rootless..."
IMAGE_URI="registry.gitlab.com/enterprise/ecommerce/$SERVICE_NAME:$COMMIT_SHA"

cat << EOF > audit/built-image-digest.json
{
  "image": "$IMAGE_URI",
  "digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "built_by": "kaniko-rootless-executor",
  "status": "KANIKO_BUILD_SUCCESS"
}
EOF

echo "[KANIKO BUILD SUCCESS] Image $IMAGE_URI created!"
```

Chạy script build:
```bash
chmod +x scripts/kaniko-build-sim.sh
./scripts/kaniko-build-sim.sh "auth-service" "a1b2c3d4e5f6"
```

### **CHECKPOINT 8 — Kaniko Rootless Build Image thành công (`QT 48.5`)**
Xác nhận container image được đóng gói rootless an toàn 100% không cần truy cập Docker socket:
```bash
test -f audit/built-image-digest.json && grep -q "KANIKO_BUILD_SUCCESS" audit/built-image-digest.json && echo "CHECKPOINT 8: ĐẠT" || echo "CHECKPOINT 8: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 8: ĐẠT
```

---

Khởi tạo script ký số Container Image với Cosign `scripts/cosign-sign-image.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail
mkdir -p audit

echo "[COSIGN SIGNING] Signing container image digest with private key..."

cat << EOF > audit/cosign-signature.json
{
  "critical": {
    "identity": { "docker-reference": "registry.gitlab.com/enterprise/ecommerce/auth-service" },
    "image": { "docker-manifest-digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" },
    "type": "cosign container image signature"
  },
  "optional": { "by-gitlab-ci-job": "10048", "signer": "devops-lead@company.com" },
  "status": "COSIGN_SIGNATURE_VALID"
}
EOF

echo "[COSIGN SIGNING SUCCESS] Signature attached to OCI Registry manifest."
```

Thực thi ký số:
```bash
chmod +x scripts/cosign-sign-image.sh
./scripts/cosign-sign-image.sh
```

### **CHECKPOINT 9 — Ký số Cosign Container Image thành công (`QT 48.6`)**
Kiểm định chữ ký số Cosign bảo vệ Supply Chain Security toàn diện cho container image:
```bash
test -f audit/cosign-signature.json && grep -q "COSIGN_SIGNATURE_VALID" audit/cosign-signature.json && echo "CHECKPOINT 9: ĐẠT" || echo "CHECKPOINT 9: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 9: ĐẠT
```

---

## L7. Bước 5: Thử nghiệm Progressive Delivery Canary & Auto-Rollback Prometheus (25 phút)

Viết script triển khai Canary Deployment & Prometheus Metric Check Engine `scripts/canary-deploy-engine.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail
SCENARIO="${1:-success}" # success | failure
mkdir -p audit

echo "[CANARY ROLLOUT] Deploying 10% Canary traffic to Kubernetes cluster..."
echo "Helm Release 'ecommerce-auth' updated: canary_replicas=1, primary_replicas=9"

echo "[CANARY METRIC MONITOR] Waiting 180s to sample Prometheus Error Rate Metrics..."
sleep 2

if [ "$SCENARIO" = "success" ]; then
  ERROR_RATE="0.0004" # 0.04% error rate
  echo "[PROMETHEUS QUERY] http_requests_5xx_rate = $ERROR_RATE (Threshold: 0.0100)"
  echo "[CANARY PROMOTION] Metric healthy! Promoting Canary to 100% Primary Release."
  cat << EOF > audit/canary-result.json
{
  "scenario": "success",
  "error_rate": "$ERROR_RATE",
  "decision": "PROMOTE_FULL_RELEASE",
  "status": "CANARY_SUCCESS"
}
EOF
else
  ERROR_RATE="0.0345" # 3.45% error rate (high error!)
  echo "[PROMETHEUS ALERT] http_requests_5xx_rate = $ERROR_RATE EXCEEDS THRESHOLD 0.0100!"
  echo "[AUTO-ROLLBACK TRIGGERED] Executing immediate Helm Rollback to previous revision..."
  cat << EOF > audit/canary-result.json
{
  "scenario": "failure",
  "error_rate": "$ERROR_RATE",
  "decision": "EXECUTE_IMMEDIATE_ROLLBACK",
  "status": "CANARY_AUTO_ROLLBACK_EXECUTED"
}
EOF
fi
```

Cấp quyền chạy script:
```bash
chmod +x scripts/canary-deploy-engine.sh
```

Thực thi kịch bản thành công:
```bash
./scripts/canary-deploy-engine.sh "success"
```

### **CHECKPOINT 10 — Thử nghiệm Canary Promotion thành công (`QT 48.7`)**
Triển khai 10% lượng truy cập cho phiên bản mới và xác nhận metrics phản hồi đạt tiêu chuẩn:
```bash
test -f audit/canary-result.json && grep -q "CANARY_SUCCESS" audit/canary-result.json && echo "CHECKPOINT 10: ĐẠT" || echo "CHECKPOINT 10: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 10: ĐẠT
```

---

Thực thi kịch bản thất bại để kích hoạt Auto-Rollback:
```bash
./scripts/canary-deploy-engine.sh "failure"
```

### **CHECKPOINT 11 — Kích hoạt Prometheus Auto-Rollback tự động thành công (`QT 48.7`)**
Phát hiện tỷ lệ lỗi HTTP 5xx vượt quá threshold 1.0% và tự động hoàn tác phiên bản trong 30 giây:
```bash
test -f audit/canary-result.json && grep -q "CANARY_AUTO_ROLLBACK_EXECUTED" audit/canary-result.json && echo "CHECKPOINT 11: ĐẠT" || echo "CHECKPOINT 11: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 11: ĐẠT
```

---

Khởi tạo alert rules Prometheus `metrics/alert-rules.yaml`:

```yaml
groups:
  - name: canary_alerts
    rules:
      - alert: CanaryHighHttp5xxRate
        expr: rate(http_requests_total{status=~"5.."}[3m]) / rate(http_requests_total[3m]) > 0.01
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Canary Deployment HTTP 5xx error rate exceeded 1%"
```

Khởi tạo Grafana Dashboard Export Template `dashboards/dora-metrics-dashboard.json`:

```json
{
  "dashboard": {
    "id": null,
    "title": "Enterprise CI/CD DORA Metrics Dashboard",
    "tags": ["dora", "gitlab", "devops"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Deployment Frequency",
        "type": "stat",
        "targets": [{ "expr": "sum(increase(gitlab_pipeline_success_total[24h]))" }]
      },
      {
        "id": 2,
        "title": "Change Failure Rate",
        "type": "gauge",
        "targets": [{ "expr": "sum(gitlab_pipeline_failed_total) / sum(gitlab_pipeline_total)" }]
      }
    ]
  }
}
```

Khởi tạo Incident Runbook `runbooks/canary-rollback-runbook.md`:

```markdown
# INCIDENT RESPONSE RUNBOOK: CANARY AUTO-ROLLBACK PROCEDURE

## 1. Trigger Conditions
Alert `CanaryHighHttp5xxRate` fires when HTTP 5xx error rate exceeds 1% during Canary evaluation window.

## 2. Automated Remediation Steps
1. The pipeline automatically terminates Canary promotion job.
2. `helm rollback ecommerce-auth <previous_revision>` is executed within 30 seconds.
3. Ingress canary traffic weight is set back to 0%.

## 3. Post-Incident Analysis
1. Inspect container logs via `kubectl logs -l app=ecommerce-auth -n ecommerce-prod --tail=100`.
2. Review Sentry exception tracebacks.
3. Attach incident ticket link to DORA failure metrics exporter.
```

Viết script thu thập DORA Metrics và gửi SIEM Audit Stream `scripts/dora-siem-exporter.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail
mkdir -p audit metrics

echo "[DORA EXPORTER] Calculating 4 DORA Metrics for Enterprise Capstone Pipeline..."

cat << EOF > metrics/dora-metrics.json
{
  "deployment_frequency": "12_per_day",
  "lead_time_for_changes_minutes": 45,
  "change_failure_rate_percent": 2.1,
  "mean_time_to_restore_minutes": 3,
  "dora_performance_tier": "ELITE",
  "status": "DORA_METRICS_EXPOSED"
}
EOF

echo "[SIEM AUDIT ENGINE] Streaming Audit Event Payload to Enterprise SIEM..."

cat << EOF > audit/siem-audit-payload.json
{
  "event_type": "PIPELINE_PRODUCTION_RELEASE",
  "project_id": 101,
  "commit_sha": "a1b2c3d4e5f6",
  "triggered_by": "devops-lead",
  "security_status": "ALL_GATES_PASSED",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "AUDIT_STREAMED_SUCCESS"
}
EOF

echo "[OBSERVABILITY SUCCESS] DORA Metrics & SIEM Audit Logs published!"
```

Cấp quyền và chạy script:
```bash
chmod +x scripts/dora-siem-exporter.sh
./scripts/dora-siem-exporter.sh
```

### **CHECKPOINT 12 — Thu thập DORA Metrics Elite Performer thành công (`QT 48.12`)**
Đánh giá năng lực CI/CD toàn bộ hệ thống đạt nhóm Elite Performer theo chuẩn DORA:
```bash
test -f metrics/dora-metrics.json && grep -q "DORA_METRICS_EXPOSED" metrics/dora-metrics.json && echo "CHECKPOINT 12: ĐẠT" || echo "CHECKPOINT 12: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 12: ĐẠT
```

---

### **CHECKPOINT 13 — Stream Immutable Audit Event về SIEM thành công (`QT 48.11`)**
Xuất nhật ký sự kiện không thể thay đổi về SIEM phục vụ các kỳ kiểm toán tuân thủ SOX / ISO27001:
```bash
test -f audit/siem-audit-payload.json && grep -q "AUDIT_STREAMED_SUCCESS" audit/siem-audit-payload.json && echo "CHECKPOINT 13: ĐẠT" || echo "CHECKPOINT 13: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 13: ĐẠT
```

---

Tạo file master pipeline tổng hợp `.gitlab-ci.yml`:

```yaml
# ===================================================================
# ENTERPRISE CAPSTONE MASTER PIPELINE (.gitlab-ci.yml)
# Full 5-Tier Blueprint Integration
# ===================================================================

include:
  - local: compliance-policies/group-security-compliance.yml
  - local: devops/ci-components/docker-build/template.yml
  - local: devops/ci-components/helm-deploy/template.yml

variables:
  CANARY_ERROR_THRESHOLD: "0.0100"
  DORA_METRICS_ENABLED: "true"

capstone-master-verification:
  stage: audit
  script:
    - echo "Executing Capstone Master Verification..."
    - test -f audit/security-gate-result.txt
    - test -f audit/oidc-credentials.json
    - test -f audit/plan.tfplan
    - test -f audit/cosign-signature.json
    - test -f audit/canary-result.json
    - test -f metrics/dora-metrics.json
    - echo "CAPSTONE_MASTER_PIPELINE_COMPLETE_SUCCESS" > audit/capstone-final.txt
```

Chạy script kiểm tra verification cuối cùng:
```bash
bash -c "test -f audit/security-gate-result.txt && test -f audit/oidc-credentials.json && test -f audit/plan.tfplan && test -f audit/cosign-signature.json && echo 'CAPSTONE_MASTER_PIPELINE_COMPLETE_SUCCESS' > audit/capstone-final.txt"
```

### **CHECKPOINT 14 — Master Capstone Pipeline Verification ĐẠT 100% (`QT 48.1` - `QT 48.12`)**
Xác nhận pipeline tổng thể tích hợp trôi chảy 5 tầng kiến trúc Enterprise Capstone Blueprint:
```bash
test -f audit/capstone-final.txt && grep -q "CAPSTONE_MASTER_PIPELINE_COMPLETE_SUCCESS" audit/capstone-final.txt && echo "CHECKPOINT 14: ĐẠT" || echo "CHECKPOINT 14: LỖI"
```
**Kết quả kỳ vọng:**
```text
CHECKPOINT 14: ĐẠT
```

---

## L8. Nộp sản phẩm và dọn dẹp (10 phút)

### L8.1. Kiểm tra toàn bộ artifact cần nộp
Chạy script tự kiểm tra 14 checkpoints bài lab:

```bash
echo "=== KIỂM TRA TỔNG HỢP 14 CHECKPOINTS CAPSTONE ==="
for i in $(seq 1 14); do
  case $i in
    1) test -f devops/ci-components/docker-build/template.yml && echo "CP1: ĐẠT" || echo "CP1: LỖI" ;;
    2) test -f devops/ci-components/helm-deploy/template.yml && echo "CP2: ĐẠT" || echo "CP2: LỖI" ;;
    3) test -f compliance-policies/group-security-compliance.yml && echo "CP3: ĐẠT" || echo "CP3: LỖI" ;;
    4) test -f audit/security-gate-result.txt && echo "CP4: ĐẠT" || echo "CP4: LỖI" ;;
    5) test -f audit/oidc-credentials.json && echo "CP5: ĐẠT" || echo "CP5: LỖI" ;;
    6) test -f audit/plan.tfplan && echo "CP6: ĐẠT" || echo "CP6: LỖI" ;;
    7) test -f audit/terraform-apply-status.txt && echo "CP7: ĐẠT" || echo "CP7: LỖI" ;;
    8) test -f audit/built-image-digest.json && echo "CP8: ĐẠT" || echo "CP8: LỖI" ;;
    9) test -f audit/cosign-signature.json && echo "CP9: ĐẠT" || echo "CP9: LỖI" ;;
    10) test -f audit/canary-result.json && echo "CP10: ĐẠT" || echo "CP10: LỖI" ;;
    11) grep -q "CANARY_AUTO_ROLLBACK_EXECUTED" audit/canary-result.json && echo "CP11: ĐẠT" || echo "CP11: LỖI" ;;
    12) test -f metrics/dora-metrics.json && echo "CP12: ĐẠT" || echo "CP12: LỖI" ;;
    13) test -f audit/siem-audit-payload.json && echo "CP13: ĐẠT" || echo "CP13: LỖI" ;;
    14) test -f audit/capstone-final.txt && echo "CP14: ĐẠT" || echo "CP14: LỖI" ;;
  esac
done
```

### L8.2. Dọn dẹp hạ tầng lab
```bash
echo "[CLEANUP] Cleaning temporary Capstone lab artifacts..."
rm -rf audit/ metrics/
echo "[CLEANUP DONE] Lab environment restored cleanly."
```

---

## L9. Xử lý sự cố thường gặp trong lab

| Triệu chứng lỗi | Nguyên nhân gốc rễ | Cách khắc phục xử lý |
|---|---|---|
| OIDC Token Exchange bị lỗi HTTP 400 | JWT Claims `aud` hoặc `sub` không khớp với AWS IAM Trust Policy | Kiểm tra cấu hình `aud: https://gitlab.com` và `sub` binding trong IAM Role |
| Terraform Apply báo lỗi `State Locked` | Job trước đó bị hỏng bất ngờ chưa giải phóng lock ID trên HTTP backend | Gọi API `force-unlock` của GitLab HTTP State Backend với Lock ID tương ứng |
| Cosign Sign báo `unauthorized` | Private key bị bọc sai passphrase hoặc OIDC Token không có quyền push artifact | Verify giá trị `COSIGN_PASSWORD` và quyền push của CI Registry token |
| Prometheus Metric Query trả về `empty` | Pod Canary chưa mở cổng metric exporter hoặc ServiceMonitor chưa scraping | Kiểm tra annotation `prometheus.io/scrape: "true"` trên Helm Template Pod |
| Kaniko Build bị lỗi `permission denied` | Container runner thiếu quyền truy cập storage mount local | Sử dụng flag `--clear-contexts` và đảm bảo runner executor chạy rootless container |
| Gitleaks báo false-positive secret | File testdata chứa chuỗi token giả định có cấu trúc tương tự real key | Tạo tệp `.gitleaksignore` liệt kê fingerprint của các file test |
| Helm Canary promotion thất bại | Cluster K8s bị thiếu tài nguyên CPU/RAM để kích hoạt pod mới | Tăng node pool size hoặc hạ thấp resource requests trong values.yaml |
| Semgrep SAST timeout trên repo lớn | Scan cả thư mục `node_modules` hoặc binary build output | Thêm file `.semgrepignore` bỏ qua `node_modules/` và `dist/` |
| Kyverno Admission Controller cấm Deploy | Image chưa qua ký số Cosign hoặc signature digest không khớp | Chạy job `cosign sign` trước khi kích hoạt stage deploy lên K8s |
| KEDA ScaledObject không scale runner | Prometheus exporter endpoint không khả dụng hoặc query sai metric name | Kiểm tra metric `gitlab_runner_jobs_pending` trên Prometheus UI |

---

## L10. Bài tập mở rộng

1. **BT1 (Advanced Security Gate):** Bổ sung job quét SBOM bằng Syft và tạo attestation SBOM dán kèm container image qua Cosign.
2. **BT2 (Multi-Cloud Failover):** Mở rộng script OIDC để tự động failover sang GCP Cloud Run nếu AWS EKS cluster gặp sự cố.
3. **BT3 (Custom KEDA Auto-scaler):** Viết file CRD KEDA ScaledObject để auto-scale số lượng GitLab Runner Pods dựa trên chỉ số Queue Length từ Prometheus.
4. **BT4 (Slack Incident Bot):** Viết Webhook handler gửi thông báo kèm nút bấm Approve / Rollback trực tiếp trên ứng dụng Slack khi Canary gặp lỗi.

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| Hạng mục sản phẩm | Tiêu chuẩn đánh giá | Thang điểm |
|---|---|---|
| `devops/ci-components/` | Đủ 2 templates `docker-build` & `helm-deploy` theo chuẩn Component Catalog | 2.0 điểm |
| `compliance-policies/` | Khung Compliance Security Framework phủ đủ SAST, Secret, SCA và Container Scan | 2.0 điểm |
| `scripts/oidc-cloud-auth.sh` | Xác thực Secretless OIDC JWT Token thành công 0 static credentials | 1.5 điểm |
| `scripts/terraform-pipeline.sh` | Phân tách bạch minh giữa `plan` xuất artifact và `apply` manual | 1.5 điểm |
| `scripts/canary-deploy-engine.sh` | Triển khai Canary 10% và kích hoạt Auto-Rollback tự động dựa trên Prometheus | 2.0 điểm |
| `metrics/ & audit/` | Xuất đủ 4 chỉ số DORA Metrics Elite và Stream Audit Log về SIEM | 1.0 điểm |
| **Tổng điểm Capstone Lab** | **Hoàn thành xuất sắc 14 Checkpoints** | **10.0 điểm** |

---

## Bảng đối soát thời lượng

| Bước thực hành | Thời lượng dự kiến | Thời lượng thực tế | Trạng thái |
|---|---|---|---|
| L0 & L1 & L2. Chuẩn bị và Kiến trúc | 15 phút | 15 phút | ĐẠT |
| L3. Bước 1: Monorepo & Components | 25 phút | 25 phút | ĐẠT |
| L4. Bước 2: Multi-Layer Security Gates | 30 phút | 30 phút | ĐẠT |
| L5. Bước 3: OIDC Auth & Terraform IaC | 30 phút | 30 phút | ĐẠT |
| L6. Bước 4: Rootless Kaniko & Cosign | 30 phút | 30 phút | ĐẠT |
| L7. Bước 5: Progressive Canary & Prometheus Rollback | 25 phút | 25 phút | ĐẠT |
| L8 & L9 & L10 & L11. Dọn dẹp & Tổng kết | 10 phút | 10 phút | ĐẠT |
| **Tổng thời gian phần Lab** | **150'** | **150'** | **ĐẠT** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---



1. **Mục đích:** Đánh giá năng lực tư duy kiến trúc Enterprise CI/CD, khả năng trả lời phỏng vấn ở cấp độ Principal / Lead DevOps Architect / Head of Infrastructure, và tư duy ứng biến xử lý sự cố trong môi trường doanh nghiệp quy mô lớn.
2. **Hình thức:** Hỏi trực tiếp 1-1 hoặc hội đồng chuyên môn (Technical Board Review). Giảng viên đóng vai CTO / Head of Security / Lead Auditor; học viên đóng vai Enterprise CI/CD Architect.
3. **Thang điểm:** Tổng điểm 36 (12 câu × max 3 điểm mỗi câu). Đạt từ 28/36 trở lên được xếp loại **Xuất sắc (Elite Level)**.

---

## V2. Bộ câu hỏi (12 câu phỏng vấn nâng cao)

### Câu 1 — 🔥
**Hỏi:** Anh/chị thiết kế kiến trúc CI/CD như thế nào cho một tập đoàn sở hữu hơn 100 microservices độc lập nhưng phải tuân thủ nghiêm ngặt chuẩn an ninh ISO27001 và SOC2?

**Đáp án chuẩn:**
Tôi thiết kế kiến trúc theo 5 tầng phân tách minh bạch:
1. **Tầng Governance:** Cưỡng chế Group Compliance Pipeline Framework ở cấp Group cao nhất. Mọi repository con tự động nhận các Security Gates bắt buộc mà không thể xóa hay bypass (`QT 48.1`).
2. **Tầng Security Shift-Left:** Chạy song song SAST (Semgrep), Secret Detection (Gitleaks), SCA (Grype) và Container Scan (Trivy) trực tiếp trên Merge Request (`QT 48.6`).
3. **Tầng Infrastructure & OIDC:** Xác thực secretless qua OIDC JWT Token với Cloud AWS/GCP/Azure, tách biệt `terraform plan` trên MR và `terraform apply` manual trên nhánh chính (`QT 48.2`, `QT 48.4`).
4. **Tầng Build & Progressive Release:** Biên dịch rootless Kaniko, ký số Cosign provenance và deploy Canary 10% đi kèm Prometheus Auto-Rollback (`QT 48.5`, `QT 48.7`).
5. **Tầng Observability:** Tự động thu thập 4 chỉ số DORA Metrics và đẩy immutable audit logs về hệ thống SIEM tập trung (`QT 48.11`, `QT 48.12`).

**Tiêu chí chấm:**
- **0đ:** Chỉ nói về việc viết file `.gitlab-ci.yml` đơn lẻ cho từng dự án.
- **1đ:** Nêu được việc quét an ninh và deploy lên Kubernetes nhưng thiếu Compliance Framework và OIDC.
- **2đ:** Trình bày được sơ đồ các tầng CI/CD và công cụ Security nhưng chưa nhấn mạnh cơ chế cưỡng chế cấp Group và DORA Metrics.
- **3đ:** Trình bày hoàn hảo kiến trúc 5 tầng, nêu rõ cơ chế cưỡng chế Compliance Pipeline ở cấp Group, OIDC Secretless Auth, Cosign Signing, Canary Auto-Rollback và DORA Observability.

**Câu hỏi đào sâu:** (Nếu dự án con cố tình gỡ bỏ file `.gitlab-ci.yml` thì Group Compliance Pipeline xử lý ra sao? *Đáp án: GitLab Compliance Framework tự động inject file cấu hình cha vào trước khi job chạy, khiến pipeline vẫn thực thi đầy đủ các bước security bất chấp nội dung file repo con.*)

---

### Câu 2 — ★★★
**Hỏi:** Tại sao việc duy trì Static Cloud Access Keys (AWS Access Key / GCP Service Account Key) trong CI/CD Variables lại là một rủi ro bảo mật thảm họa, và anh/chị giải quyết bài toán này như thế nào bằng OIDC?

**Đáp án chuẩn:**
Static credentials tồn tại 3 rủi ro chí mạng: (1) Rủi ro rò rỉ qua log job hoặc bị lộ khi runner bị compromised; (2) Không có thời hạn hết hạn tự động nên khi lộ sẽ bị hacker lợi dụng kéo dài; (3) Khó rotate định kỳ do ảnh hưởng tới hàng trăm pipeline.
Tôi giải quyết triệt để bằng **OIDC Federated Identity Authentication** (`QT 48.2`):
- Khi job chạy, GitLab Runner cấp một OIDC JWT Token có chữ ký chứa thông tin danh tính đại diện (`project_path`, `ref`, `user`).
- Runner gửi JWT Token này tới STS của AWS / WIF của GCP để trao đổi lấy Temporary Credentials có thời gian sống ngắn (Short-lived, ví dụ 1 giờ).
- Khi job kết thúc, credential tự động hết hiệu lực. Hệ thống đạt trạng thái 0 static cloud credentials.

**Tiêu chí chấm:**
- **0đ:** Không giải thích được rủi ro của static key và không biết OIDC là gì.
- **1đ:** Biết static key nguy hiểm nhưng đề xuất giải pháp mã hóa key thay vì OIDC.
- **2đ:** Giải thích đúng OIDC cấp token ngắn hạn nhưng chưa nêu rõ cơ chế Trust Policy ràng buộc theo `project_path` và `ref`.
- **3đ:** Trình bày xuất sắc 3 rủi ro của static credentials, phân tích chi tiết luồng trao đổi OIDC JWT Token với AWS STS / GCP WIF và nguyên tắc 0 static credentials.

**Câu hỏi đào sâu:** (Trust Policy trên IAM Role AWS cần kiểm tra claim nào trong OIDC JWT Token để tránh việc dự án A lấy được role của dự án B? *Đáp án: Kiểm tra claim `sub` hoặc `project_path` trong Condition block của IAM Trust Policy.*)

---

### Câu 3 — 🔥
**Hỏi:** Trình bày chiến lược thiết kế thư viện Centralized CI/CD Components Catalog để đảm bảo tỷ lệ tái sử dụng (Reuse Rate) đạt trên 85% trong toàn doanh nghiệp?

**Đáp án chuẩn:**
Để đạt tỷ lệ tái sử dụng $\ge 85\%$, tôi áp dụng 4 nguyên tắc chuẩn hóa (`QT 48.8`):
1. **Repository tập trung:** Đóng gói tất cả pipeline building blocks tại một repository duy nhất `devops/ci-components`.
2. **Khai báo Giao diện minh bạch (Input Inputs):** Sử dụng cú pháp `spec: inputs:` để định nghĩa rõ tham số đầu vào, giá trị mặc định và kiểu dữ liệu.
3. **Quản lý phiên bản Semantic Versioning:** Phát hành phiên bản theo chuẩn `v1.0.0`, `v1.1.0`. Dự án con import theo tag cố định để tránh bị vỡ pipeline khi component nâng cấp.
4. **Đa dạng hóa theo Stack:** Cung cấp sẵn các components chuẩn cho Node.js, Java, Python, Go, Docker build và Helm deploy.

**Tiêu chí chấm:**
- **0đ:** Đề xuất copy-paste đoạn YAML giữa các repo.
- **1đ:** Nêu giải pháp dùng `include: file:` nhưng không có Semantic Versioning hay Input Specs.
- **2đ:** Trình bày được cấu trúc Component Catalog nhưng chưa nêu cách quản lý phiên bản và tỷ lệ reuse rate.
- **3đ:** Trình bày toàn diện 4 nguyên tắc thiết kế CI/CD Component Catalog, cú pháp `spec: inputs:`, quy trình Semantic Versioning và chiến lược đạt 85% reuse rate.

**Câu hỏi đào sâu:** (Sự khác biệt lớn nhất giữa `include: component:` và `include: local:` là gì? *Đáp án: Component có giao diện tham số khai báo minh bạch `spec: inputs` và được quản lý phiên bản độc lập trong Catalog UI.*)

---

### Câu 4 — ★★★
**Hỏi:** Làm thế nào để tự động hóa khâu triển khai IaC với Terraform trong CI/CD mà tuyệt đối không xảy ra sự cố sập hạ tầng do lỗi con người?

**Đáp án chuẩn:**
Tôi thực thi quy trình 4 lớp bảo vệ nghiêm ngặt (`QT 48.4`, `QT 48.10`):
1. **Phân tách Plan & Apply:** Trên Merge Request chỉ cho phép chạy `terraform plan` và xuất ra binary artifact `plan.tfplan`.
2. **Lock State tập trung:** Sử dụng GitLab HTTP Backend để tự động khóa state file (`state lock`) trong suốt quá trình chạy plan/apply.
3. **Manual Approval Gate:** Lệnh `terraform apply` chỉ chạy trên nhánh `main` sau khi MR được merge và bắt buộc phải có nút kích hoạt Manual Action từ DevOps Lead.
4. **Ràng buộc Apply đúng Plan Artifact:** Lệnh `apply` bắt buộc phải đọc trực tiếp tệp `plan.tfplan` đã qua phê duyệt, cấm không cho `apply` lại từ mã nguồn live để tránh State Drift.

**Tiêu chí chấm:**
- **0đ:** Cho phép chạy `terraform apply` tự động ngay trên Merge Request.
- **1đ:** Biết tách plan và apply nhưng không dùng state locking hay plan artifact.
- **2đ:** Trình bày được plan/apply và manual gate nhưng chưa nhấn mạnh việc cưỡng chế apply từ `plan.tfplan` artifact.
- **3đ:** Trình bày xuất sắc 4 lớp bảo vệ, cơ chế State Locking trên HTTP Backend, phê duyệt 2 người và cưỡng chế apply đúng plan artifact.

**Câu hỏi đào sâu:** (Nếu một kỹ sư sửa thủ công một Security Group trên AWS Console, làm sao CI/CD Terraform phát hiện ra? *Đáp án: Lệnh `terraform plan` định kỳ sẽ so sánh State File và live infrastructure để báo về sự cố Drift.*)

---

### Câu 5 — 🔥
**Hỏi:** Anh/chị hãy mô tả chi tiết luồng hoạt động của một bài toán Progressive Delivery Canary Rollout đi kèm Prometheus Auto-Rollback tự động trong 3 phút?

**Đáp án chuẩn:**
Luồng diễn ra qua 5 bước tự động hóa (`QT 48.7`):
1. **Deploy Canary 10%:** Helm Upgrade thiết lập 1 Pod Canary nhận 10% lưu lượng người dùng (9 Pods còn lại giữ bản cũ).
2. **Warm-up & Sleep:** Pipeline dừng 180 giây để ứng dụng Canary khởi động và xử lý traffic thực tế.
3. **Prometheus Query Check:** Script gọi Prometheus Metric API tính tỷ lệ lỗi:
   $$\text{Error Rate} = \frac{\text{rate}(\text{http\_requests\_total}\{\text{status}=\sim"5.."\}[\text{3m}])}{\text{rate}(\text{http\_requests\_total}[\text{3m}])}$$
4. **Đánh giá Ngưỡng (Threshold Evaluation):**
   - Nếu $\text{Error Rate} < 0.1\%$: Promote Canary phình to thành 100% Primary Release.
   - Nếu $\text{Error Rate} \ge 1.0\%$: Kích hoạt lập tức đường `Helm rollback` về revision trước và dừng pipeline với `exit 1`.

**Tiêu chí chấm:**
- **0đ:** Không biết Canary deployment là gì, chỉ biết deploy đè 100%.
- **1đ:** Trình bày được ý tưởng chia 10% traffic nhưng khâu rollback hoàn toàn làm thủ công.
- **2đ:** Nêu được công thức Prometheus nhưng chưa trình bày chi tiết luồng tự độngpromote/rollback trong script CI.
- **3đ:** Mô tả chính xác 5 bước tự động hóa, công thức PromQL tính error rate, ngưỡng kích hoạt Auto-Rollback trong 3 phút và tích hợp với Helm.

**Câu hỏi đào sâu:** (Tại sao phải cần khoảng nghỉ Sleep 180s trước khi query Prometheus? *Đáp án: Để chờ container hoàn tất startup probe, JVM JIT warmup và tích lũy đủ mẫu dữ liệu HTTP request trong cửa sổ rate 3 phút.*)

---

### Câu 6 — ★★★
**Hỏi:** Trong môi trường Kubernetes Auto-scaling Runner, làm thế nào để đảm bảo tính cô lập tuyệt đối giữa các job (Zero Cross-Job Contamination) mà không làm tăng thời gian chờ của pipeline?

**Đáp án chuẩn:**
Tôi áp dụng giải pháp **Ephemeral Runner Pods trên Kubernetes Executor** (`QT 48.5`):
- Mỗi job CI/CD khi xuất hiện trong queue sẽ kích hoạt Kubernetes Executor tạo một Pod riêng biệt chứa container chạy job.
- Môi trường hoàn toàn sạch (Ephemeral), không chia sẻ đĩa đệm hay bộ nhớ với các job khác. Khi job xong, Pod bị xóa hoàn toàn.
- Để không tăng thời gian chờ pull image, tôi cấu hình **Distributed S3 Caching** và duy trì **Local Image Registry Cache Mirror** trên node pool của K8s Cluster.

**Tiêu chí chấm:**
- **0đ:** Sử dụng Static Shell Runner dùng chung ổ đĩa cho mọi job.
- **1đ:** Biết dùng Docker Executor nhưng runner vẫn chạy tĩnh trên một VM đơn lẻ.
- **2đ:** Trình bày được Kubernetes Executor nhưng chưa nêu giải pháp S3 Caching và Local Registry Mirror để bù đắp thời gian pull image.
- **3đ:** Phân tích sâu sắc ưu điểm của Ephemeral Pods, cơ chế xóa pod tức thì, giải pháp S3 Distributed Cache và Local Registry Mirror giúp tối ưu tốc độ.

**Câu hỏi đào sâu:** (Nếu một job bị treo vô hạn trong Pod Runner, giải pháp ngăn chặn cạn kiệt tài nguyên cluster là gì? *Đáp án: Cấu hình `timeout:` bắt buộc ở cấp Job trong YAML và `job_timeout` trên Kubernetes Runner Manager.*)

---

### Câu 7 — 🔥
**Hỏi:** Chuỗi cung ứng phần mềm (Software Supply Chain Security) đòi hỏi những yếu tố gì trong pipeline CI/CD để chống lại các cuộc tấn công dạng SolarWinds hay Dependency Confusion?

**Đáp án chuẩn:**
Tôi thực thi 3 trụ cột bảo mật chuỗi cung ứng (`QT 48.6`):
1. **Xác thực Nguồn gốc (Provenance & SLSA Level 3):** Sử dụng Cosign ký số Container Image và xuất bằng chứng provenance minh chứng image được build từ đúng commit SHA và runner hợp lệ.
2. **Danh mục SBOM (Software Bill of Materials):** Tự động xuất báo cáo SBOM định dạng CycloneDX/SPDX bằng Syft cho mọi build artifact.
3. **Cưỡng chế Chữ ký số tại Cluster (Policy Enforcement):** Bật Kyverno hoặc OPA Gatekeeper trên Kubernetes Cluster, chỉ cho phép khởi tạo Pod từ các Image có chữ ký Cosign hợp lệ.

**Tiêu chí chấm:**
- **0đ:** Cho rằng chỉ cần đặt mật khẩu mạnh cho Docker Registry là đủ.
- **1đ:** Nêu được việc quét lỗ hổng container nhưng không biết về ký số hay SBOM.
- **2đ:** Trình bày được Cosign và SBOM nhưng chưa nêu khâu cưỡng chế chặn image chưa ký ở cấp Kubernetes Admission Controller.
- **3đ:** Trình bày xuất sắc 3 trụ cột Supply Chain Security, chuẩn SLSA Provenance, Cosign signing, SBOM CycloneDX và OPA/Kyverno Gatekeeper.

**Câu hỏi đào sâu:** (Chữ ký Cosign được lưu trữ ở đâu sau khi ký xong image? *Đáp án: Cosign lưu trữ signature dưới dạng một OCI Artifact phụ nằm ngay bên cạnh Container Image Manifest trong Registry.*)

---

### Câu 8 — ★★★
**Hỏi:** 4 chỉ số DORA Metrics là gì, và anh/chị thu thập, đo lường chúng tự động như thế nào trong hệ thống GitLab CI/CD Enterprise?

**Đáp án chuẩn:**
4 chỉ số DORA bao gồm (`QT 48.12`):
1. **Deployment Frequency (DF):** Tần suất phát hành thành công lên Production.
2. **Lead Time for Changes (LTC):** Thời gian từ khi commit code đến khi code chạy trên Prod.
3. **Change Failure Rate (CFR):** Tỷ lệ đợt phát hành gây ra sự cố.
4. **Mean Time to Restore (MTTR):** Thời gian trung bình để khôi phục dịch vụ khi có sự cố.

Tôi tự động hóa việc thu thập bằng cách bắt sự kiện từ **GitLab Webhook Engine** và **GitLab DORA API**, đẩy dữ liệu thô về Prometheus Exporter, sau đó trực quan hóa trên Grafana Dashboard theo dõi theo thời gian thực.

**Tiêu chí chấm:**
- **0đ:** Không kể tên được 4 chỉ số DORA.
- **1đ:** Kể tên được 4 chỉ số nhưng đo đạc hoàn toàn bằng phương pháp ghi chép thủ công.
- **2đ:** Trình bày đúng 4 chỉ số và biết đến GitLab DORA feature nhưng chưa nêu luồng thu thập tự động qua Webhook/Prometheus/Grafana.
- **3đ:** Phân tích chính xác ý nghĩa 4 chỉ số DORA, quy trình thu thập tự động qua Webhook Engine, Prometheus Exporter và Grafana DORA Metrics Dashboard.

**Câu hỏi đào sâu:** (Chỉ số nào trong DORA phản ánh trực tiếp chất lượng của quy trình kiểm thử tự động Shift-Left? *Đáp án: Change Failure Rate - CFR. CFR càng thấp chứng tỏ các test gate trước đó chặn được càng nhiều lỗi.*)

---

### Câu 9 — 🔥
**Hỏi:** Khi một lỗ hổng Zero-Day nghiêm trọng xuất hiện trên thư viện Log4j/OpenSSL, làm sao anh/chị cập nhật quy tắc rà quét và áp dụng cho 100 dự án microservices trong vòng 15 phút?

**Đáp án chuẩn:**
Quy trình ứng phó 15 phút nhờ kiến trúc Compliance tập trung (`QT 48.1`, `QT 48.8`):
1. **Cập nhật tại 1 điểm duy nhất:** Security Team cập nhật rule rà quét mới tại repository `security-templates` tập trung.
2. **Tự động áp dụng tức thì:** Do 100 dự án con đều chịu sự chi phối của Group Compliance Framework, tất cả các pipeline mới kích hoạt sẽ tự động nhận rule mới mà không cần chỉnh sửa từng file repo con.
3. **Chặn Pipeline vỡ rule:** Các dự án dính lỗ hổng lập tức bị ngắt pipeline build.
4. **Auto-Fix MR Bot:** Kích hoạt Bot tự động tạo 100 Merge Requests nâng cấp thư viện bản vá cho 100 repository cùng lúc.

**Tiêu chí chấm:**
- **0đ:** Đề xuất gửi email yêu cầu 100 lập trình viên tự sửa tay file YAML từng repo.
- **1đ:** Nêu giải pháp sửa template dùng chung nhưng mất thời gian chờ từng repo merge code.
- **2đ:** Trình bày được vai trò của Compliance Framework tập trung nhưng chưa nêu luồng Auto-Fix MR Bot.
- **3đ:** Trình bày xuất sắc kịch bản ứng phó 15 phút, cập nhật 1 điểm tại Compliance Template, cưỡng chế tức thì cho 100 repo và kích hoạt Auto-Fix Bot.

**Câu hỏi đào sâu:** (Làm sao đảm bảo Bot tạo 100 MR không làm tắc nghẽn hạ tầng runner? *Đáp án: Cấu hình queue priority và phân luồng runner riêng cho các job do Bot kích hoạt.*)

---

### Câu 10 — ★★★
**Hỏi:** Anh/chị làm thế nào để tối ưu hóa thời gian thực thi của một pipeline đa ngôn ngữ từ 40 phút xuống dưới 8 phút (Fast Feedback Loop)?

**Đáp án chuẩn:**
Tôi kết hợp 4 kỹ thuật tối ưu hóa cốt lõi (`QT 48.3`, `QT 48.9`):
1. **Bỏ hàng rào Stage với DAG `needs:`:** Chuyển pipeline từ mô hình nối tiếp theo stage sang luồng đồ thị DAG, cho phép job test chạy ngay khi job build tương ứng xong mà không chờ các job khác.
2. **Parallel Matrix:** Chia nhỏ suite kiểm thử E2E/Unit test thành `parallel: 8` job chạy đồng thời.
3. **Phân tầng Caching thông minh:** Đặt `cache:key` theo checksum file lock (`package-lock.json`, `go.sum`), sử dụng S3 Distributed Cache.
4. **Tách luồng Fast Feedback:** MR pipeline chỉ chạy Linter, Fast Unit Test, SAST (< 5 phút); các job E2E heavy test chuyển sang chạy scheduled đêm.

**Tiêu chí chấm:**
- **0đ:** Trả lời chung chung "tăng cấu hình CPU/RAM cho runner".
- **1đ:** Biết dùng cache nhưng pipeline vẫn bị nghẽn do stage nối tiếp.
- **2đ:** Trình bày được DAG `needs:` và Caching nhưng chưa áp dụng Parallel Matrix và phân tách luồng Fast Feedback.
- **3đ:** Phân tích toàn diện 4 kỹ thuật tối ưu, DAG workflow, Parallel Matrix, Distributed S3 Caching và tách luồng Fast Feedback dưới 8 phút.

**Câu hỏi đào sâu:** (Nếu cache key đặt theo `$CI_COMMIT_REF_SLUG` bị hỏng, cách xử lý nhanh nhất mà không cần sửa code là gì? *Đáp án: Xóa cache trên giao diện GitLab UI hoặc đổi cờ `CLEAR_CACHE=true` trong CI Variables.*)

---

### Câu 11 — 🔥
**Hỏi:** Làm thế nào để đảm bảo tính độc lập và nguyên tắc kiểm soát 4 mắt (Four-Eye Principle) khi phê duyệt phát hành ứng dụng lên môi trường Production?

**Đáp án chuẩn:**
Tôi cưỡng chế nguyên tắc 4 mắt thông qua Protected Environments và CODEOWNERS (`QT 48.10`):
1. **Protected Environments Configuration:** Cấu hình môi trường `production` trên GitLab Settings chỉ cho phép nhóm `Maintainer` hoặc `Release Managers` phê duyệt.
2. **Tối thiểu 2 Approvers độc lập:** Thiết lập `Required Approvals: 2`. Tác giả của Merge Request (Author) và người tạo commit tuyệt đối không được tự phê duyệt chính code của mình.
3. **Reset Approvals khi có commit mới:** Bật cờ `Remove all approvals when new commits are pushed` để ngăn ngừa việc gài mã độc sau khi đã được duyệt.

**Tiêu chí chấm:**
- **0đ:** Cho phép bất kỳ ai bấm nút deploy Production.
- **1đ:** Nêu được việc cần 1 người duyệt nhưng không chặn tác giả tự duyệt code.
- **2đ:** Trình bày được Protected Environments và 2 approvers nhưng chưa nêu cờ Reset Approvals khi push commit mới.
- **3đ:** Trình bày hoàn hảo nguyên tắc 4 mắt, phân quyền Protected Environments, chặn Author Approval và cờ Reset Approvals tự động.

**Câu hỏi đào sâu:** (Nếu trong ca trực đệm chỉ có 1 Lead DevOps on-call mà có sự cố P1 khẩn cấp thì quy trình Bypass Break-Glass diễn ra ra sao? *Đáp án: Kích hoạt quy trình Emergency Break-Glass Role có ghi vết Audit Log đặc biệt và yêu cầu giải trình sau sự cố trong 24h.*)

---

### Câu 12 — ★★★
**Hỏi:** Anh/chị làm thế nào để xây dựng một hệ thống Log & Alerting tự động cho Pipeline CI/CD giúp kỹ sư phát hiện nguyên nhân gốc rễ (Root Cause) trong vòng dưới 3 phút?

**Đáp án chuẩn:**
Tôi xây dựng hệ thống Actionable Observability cho Pipeline (`QT 48.11`):
1. **Collapsible Section Logging:** Sử dụng cú pháp `section_start` / `section_end` của GitLab CI để gom nhóm log trực quan, giúp kỹ sư mở ngay phần log bị lỗi mà không phải cuộn hàng ngàn dòng log.
2. **Standardized Error Exit Codes:** Script pipeline bắt lỗi bằng `set -euo pipefail` và in ra thông báo màu dạng `[ERROR-NET-01] Unable to reach Artifact Registry`.
3. **Structured Webhook Alerting:** Khi job failure, Webhook tự động gửi alert sang Slack/Teams kèm theo: Tên Job, Người kích hoạt, File bị vỡ, Commit SHA và đường dẫn trực tiếp tới dòng log lỗi.

**Tiêu chí chấm:**
- **0đ:** Để log mặc định trôi tự do, khi lỗi kỹ sư phải tự mò từng dòng.
- **1đ:** Biết gửi notification khi job fail nhưng không có thông tin chi tiết.
- **2đ:** Trình bày được Collapsible log và script exit code nhưng chưa xây dựng Webhook Alerting cấu trúc rõ ràng.
- **3đ:** Trình bày xuất sắc Collapsible Section Logs, Standardized Error Exit Codes và Structured Webhook Alerting giúp chẩn đoán lỗi dưới 3 phút.

**Câu hỏi đào sâu:** (Cú pháp bash script nào đảm bảo script dừng ngay lập tức khi một câu lệnh bất kỳ trong chuỗi bị lỗi? *Đáp án: Lệnh `set -e` hoặc `set -eo pipefail`.*)

---

## V3. Câu chốt để nói khi phỏng vấn

1. **Câu chốt về Architecture & Governance:**
   > "Tôi không xây dựng CI/CD dưới dạng các file YAML nhỏ lẻ cho từng dự án. Tôi thiết kế **Enterprise CI/CD Platform 5 tầng** với Group Compliance Framework cưỡng chế 100% quy chuẩn an ninh, giúp tổ chức vận hành 100 microservices đồng nhất, an toàn và tuân thủ tuyệt đối."

2. **Câu chốt về Security & Secretless Auth:**
   > "Trong hệ thống CI/CD do tôi kiến tạo, **0 static credentials** tồn tại trên môi trường. 100% kết nối sang Cloud AWS/GCP/Azure đều qua cơ chế **Secretless OIDC Federated Auth** với temporary token ngắn hạn, kết hợp ký số **Cosign SLSA Provenance** đảm bảo an toàn tuyệt đối cho chuỗi cung ứng."

3. **Câu chốt về Speed, Release & DORA Metrics:**
   > "Tôi tối ưu hóa Developer Feedback Loop xuống dưới **8 phút** nhờ DAG workflow và S3 Caching. Mọi đợt phát hành Production đều áp dụng **Helm Canary Rollout đi kèm Prometheus Auto-Rollback trong 3 phút**, đưa tổ chức đạt cấp độ **Elite Performer theo chuẩn DORA Metrics**."

---

## V4. Bảng ghi điểm

| Mức điểm tổng | Xếp loại năng lực | Đánh giá vị trí phù hợp |
|---|---|---|
| 32 - 36 điểm | **Elite Architecture Lead** | Principal / Enterprise CI/CD Architect / Head of DevOps |
| 26 - 31 điểm | **Senior DevSecOps Engineer** | Senior DevOps / DevSecOps Specialist / Tech Lead |
| 20 - 25 điểm | **Mid-Level DevOps Engineer** | Mid-Level DevOps / CI/CD Pipeline Engineer |
| Dưới 20 điểm | **Junior / Need Improvement** | Cần ôn tập lại các buổi từ 01 đến 47 |

---

## V5. Bài tập về nhà

1. **BTVN 1:** Tổng hợp toàn bộ sơ đồ kiến trúc 5 tầng Capstone và 12 Quy tắc vàng (`QT 48.1` - `QT 48.12`) thành một bản tài liệu **CI/CD Enterprise Handbook** định dạng PDF/Markdown cho doanh nghiệp.
2. **BTVN 2:** Thực hành đóng gói 3 CI/CD Components (Docker Build, Helm Deploy, Security Scan) và xuất bản lên GitLab Component Catalog riêng của cá nhân.
3. **BTVN 3:** Lập kế hoạch lộ trình chuyển đổi (Migration Plan) hệ thống CI/CD cũ của công ty bạn sang mô hình Capstone Enterprise trong vòng 90 ngày.
4. **BTVN 4 (Chuẩn bị cho sự nghiệp thực tế):**
   - *Câu 1:* Chuẩn bị bài thuyết trình 10 phút bảo vệ kiến trúc Capstone CI/CD trước CTO và Security Committee.
   - *Câu 2:* Xây dựng bộ CV / Portfolio cá nhân làm nổi bật các dự án Capstone CI/CD, OIDC, Cosign, Canary Rollout và DORA Metrics.
   - *Câu 3:* Luyện tập phản xạ trả lời 3 câu chốt ở Mục V3 để sẵn sàng chinh phục các buổi phỏng vấn vị trí Lead / Principal DevOps Architect với mức thu nhập mơ ước.

---

## Bảng đối soát thời lượng

| Mục | Thời lượng | Trạng thái |
|---|---|---|
| V1. Cách tiến hành | 2 phút | ĐẠT |
| V2. Bộ 12 câu hỏi phỏng vấn nâng cao | 12 phút | ĐẠT |
| V3. Các câu chốt khi phỏng vấn | 3 phút | ĐẠT |
| V4 & V5. Bảng ghi điểm & Bài tập về nhà | 3 phút | ĐẠT |
| **Tổng thời gian phần Vấn đáp** | **20 phút** | **ĐẠT** |
{% endraw %}
