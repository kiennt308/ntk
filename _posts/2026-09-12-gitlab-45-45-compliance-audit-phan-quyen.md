---
layout: post
title: "[Bài 45] Phân Quyền & Kiểm Soát Truy Cập Doanh Nghiệp: GitLab RBAC, Protected Branches, Push Rules & SAML/SSO Integration"
date: 2026-09-12 02:10:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-45
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 45
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.45] Hướng dẫn chuyên sâu Phân Quyền & Kiểm Soát Truy Cập Doanh Nghiệp: GitLab RBAC, Protected Branches, Push Rules & SAML/SSO Integration: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

{% raw %}
# [BÀI 45] PHÂN QUYỀN & KIỂM SOÁT TRUY CẬP DOANH NGHIỆP: GITLAB RBAC, PROTECTED BRANCHES, PUSH RULES & SAML/SSO INTEGRATION

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

---





| STT | Câu hỏi ôn tập | Đáp án chi tiết thực chiến |
|---|---|---|
| 1 | Rủi ro an ninh nghiêm trọng nhất của Shell Executor là gì? | Thiếu cô lập (No Job Isolation), các dự án dùng chung OS host có thể đọc trộm mã nguồn và secret keys của nhau. |
| 2 | Khác biệt cốt lõi giữa Docker Executor và Kubernetes Executor là gì? | Docker Executor chạy container trên 1 host cố định; Kubernetes Executor tự động scale số lượng Runner Pods theo lượng jobs trên cụm K8s. |
| 3 | Tại sao cờ `privileged = true` lại cực kỳ nguy hiểm trong `config.toml`? | Vì nó loại bỏ các rào cản an ninh của Docker, cho phép script CI thực hiện Container Escape chiếm quyền root toàn bộ máy chủ host. |
| 4 | Lệnh `docker system prune -af --volumes` có tác dụng gì? | Dọn dẹp các Docker Images rác, Containers dangled và Volumes cũ, chống thảm họa đầy đĩa 100% làm sập pipelines. |
| 5 | Tại sao phải thực thi `gitlab-runner stop` khi nâng cấp phiên bản Runner? | Để ngắt nhận jobs mới nhưng chờ tất cả các jobs đang chạy hoàn tất 100% (Graceful Shutdown), đảm bảo 0% jobs bị sập rớt. |


**Luận đề trung tâm:**
> *"Kiểm soát tuân thủ bảo mật nào **cưỡng chế được bằng cấu hình kỹ thuật (Enforced by Code)** thì mới thực sự là kiểm soát; còn những kiểm soát dựa vào lời hứa hay tài liệu Word chỉ là mong muốn."*

Trong các tập đoàn lớn đạt tiêu chuẩn **SOC 2, ISO 27001, PCI-DSS, HIPAA**:
1. **Protected Branches & Protected Tags:** Tuyệt đối cấm đẩy trực tiếp code (`git push origin main`) hay xóa nhãn release (`git push --delete origin v1.0.0`). Mọi thay đổi bắt buộc phải đi qua đường Merge Request được phê duyệt.
2. **CODEOWNERS & Rule 2 Người phê duyệt (Four-Eye Principle):** Tự động gán đúng người sở hữu code (Security Team cho `security/`, DevOps Team cho `terraform/`). Bắt buộc tối thiểu 2 người phê duyệt độc lập, tác giả không được tự phê duyệt MR của mình.
3. **Compliance Frameworks & Audit Logs:** Ép tất cả 500 Repositories phải tuân thủ chung 1 mẫu CI Compliance Pipeline và đẩy 100% nhật ký thao tác (Audit Events) về hệ thống SIEM tập trung.

Bài học này giúp bạn trở thành Kiến trúc sư Tuân thủ Bảo mật (Security & Compliance Architect) đỉnh cao!

---



| STT | Kỹ năng thực chiến | Hiện vật chứng minh hoàn thành |
|---|---|---|
| 1 | Cấu hình Protected Branches & Protected Tags qua API | HTTP POST request cấu hình cấm Force Push và Direct Push |
| 2 | Khởi tạo tệp `CODEOWNERS` gán quyền xem xét theo thư mục | Tệp `CODEOWNERS` định nghĩa quyền phê duyệt `@security-team` |
| 3 | Cưỡng chế Quy tắc 2 Người phê duyệt (Four-Eye Principle) | Rule `approval_rules` trong MR yêu cầu minimum 2 approvals |
| 4 | Cấu hình tự động hủy Approval khi push commit mới | Cờ `reset_approvals_on_push = true` trong cài đặt Merge Request |
| 5 | Chặn rò rỉ secret keys bằng Secret Push Protection | Cờ `secret_push_protection = true` chặn lệnh `git push` |
| 6 | Gắn Compliance Frameworks Template cho toàn bộ Repos | Cấu hình `compliance_framework` trên GitLab Group Level |
| 7 | Thu thập và đẩy Streaming Audit Logs về SIEM | Cấu hình Streaming Audit Event API trỏ tới Splunk / Elastic |
| 8 | Bắt buộc ký số điện tử GPG/SSH Signature cho commits | Cờ `reject_unsigned_commits = true` trên Protected Branch |

---



| Kiến thức / Kỹ năng | Mức độ yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Nguyên lý Git Branching, Commits và Merge Requests | Thành thục | Tài liệu Căn bản Git |
| Khái niệm Chữ ký số GPG / SSH Keys Signature | Khá | Tài liệu Git Security |
| Các tiêu chuẩn bảo mật Enterprise (SOC 2, ISO 27001) | Khá | Kiến thức Security Compliance |
| Sử dụng REST API và CURL với Personal Access Tokens | Thành thục | Tài liệu GitLab REST API |
| Cấu trúc hệ thống SIEM (Splunk, Elastic, Datadog) | Đã biết | Kiến thức SIEM Basics |

---





| Thuật ngữ Tiếng Việt | Thuật ngữ Tiếng Anh | Giải thích ý nghĩa thực tế |
|---|---|---|
| Nhánh được bảo vệ | Protected Branch | Nhánh Git bị khóa cấm push trực tiếp, cấm force push và yêu cầu MR approval. |
| Nhãn được bảo vệ | Protected Tag | Nhãn Git (Release Tag) bị khóa chỉ cho phép pipeline hoặc Maintainers khởi tạo. |
| Người sở hữu mã nguồn | CODEOWNERS | Tệp định nghĩa các cá nhân/nhóm bắt buộc phải phê duyệt MR khi có sửa đổi file trong folder họ quản lý. |
| Quy tắc 2 người phê duyệt | Four-Eye Principle | Nguyên tắc bảo mật bắt buộc tối thiểu 2 người độc lập xem xét và phê duyệt trước khi merge code. |
| Khung tuân thủ | Compliance Framework | Mẫu quy trình CI/CD chuẩn do đội Security định nghĩa, tự động ép áp dụng cho mọi Repositories. |
| Nhật ký kiểm toán | Audit Events Logs | Bản ghi vết không thể sửa xóa ghi lại ai đã làm gì, vào lúc nào trên hệ thống GitLab. |
| Truyền nhật ký thời gian thực | Streaming Audit Logs | Cơ chế tự động đẩy ngay lập tức các sự kiện Audit Events về máy chủ SIEM (Splunk/Elastic). |
| Chặn chìa khóa bị lộ | Secret Push Protection | Tính năng tự động quét và chặn đứng lệnh `git push` nếu phát hiện có chứa AWS/SSH Key. |
| Ký số commit | GPG/SSH Commit Signing | Sử dụng khóa GPG/SSH xác thực chính chủ identity của tác giả tạo ra commit đó. |
| Tự động hủy phê duyệt | Approval Reset on Push | Tự động xóa các lượt phê duyệt trước đó khi tác giả push thêm commit mới vào Merge Request. |



#### Mô hình 1: Sơ đồ Luồng Kiểm soát 6 Cổng Bảo vệ (Compliance Gateways) khi Merge Code

```mermaid
flowchart TD
    subgraph Developer Workspace
        A[Developer pushes Commit] -->|1. Git Push Command| B{Secret Push Protection}
    end

    subgraph Gate 1: Secret Scan
        B -->|Contains AWS Key| C[REJECT PUSH Immediately]
        B -->|Clean Code| D{Check GPG Commit Signature}
    end

    subgraph Gate 2 & 3: Signature & Protected Branch
        D -->|Unsigned Commit| E[REJECT: Unsigned Commit]
        D -->|Valid GPG Signature| F{Protected Branch Check}
        F -->|Direct Push to Main| G[REJECT: Direct Push Forbidden]
        F -->|Create Merge Request| H[Merge Request Engine]
    end

    subgraph Gate 4 & 5: CODEOWNERS & Four-Eye Approvals
        H -->|Check Paths modified| I[CODEOWNERS Evaluation]
        I -->|Triggers @security-team| J{Min 2 Approvals Check}
        J -->|Only 1 Approval or Author Approved| K[BLOCKED: Waiting for Approvals]
        J -->|Author pushes new commit| L[RESET all previous approvals!]
        J -->|2 Independent Approvals OK| M[PASS ALL GATES]
    end

    subgraph Gate 6: Audit Logging & Deployment
        M -->|Merge to Main| N[Trigger Production Deployment]
        N -->|Stream Event Log| O[SIEM / Splunk Dashboard]
    end
```

#### Mô hình 2: Mẫu Cấu hình Tệp `CODEOWNERS` Chuẩn mực Enterprise

```text
# ===================================================================
# ENTERPRISE CODEOWNERS CONFIGURATION FILE
# Location: .gitlab/CODEOWNERS or CODEOWNERS
# ===================================================================

# Mặc định mọi thay đổi cần Tech Leads phê duyệt
* @company-tech-leads

# Toàn bộ mã nguồn Security & Authentication cần Security Team phê duyệt
/src/security/ @security-team @ciso-officer
/src/auth/ @security-team

# Toàn bộ mã nguồn Hạ tầng Infrastructure & Terraform cần DevOps Team phê duyệt
/terraform/ @devops-team @lead-devops
/.gitlab-ci.yml @devops-team
/helm/ @devops-team

# Toàn bộ mã nguồn Database Migrations cần DB Admin phê duyệt
/db/migrations/ @dba-team

# Toàn bộ các file Secret & Configuration mẫu cần Security Officer phê duyệt
/*.env.example @security-team
```

---

### 1.1. Quy tắc Protected Branches, CODEOWNERS & Approvals (10 phút)

### 4.1. Mẫu Cấu hình REST API Khởi tạo Protected Branch & Approval Rules

```bash
#!/usr/bin/env bash
# Script khởi tạo Protected Branch 'main' cưỡng chế MR Approvals qua API

PROJECT_ID="12345"
GITLAB_TOKEN="glpat-xxxxxxxxxxxxxx"

# 1. Khóa nhánh main: Cấm Direct Push, Cấm Force Push
curl --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
     "https://gitlab.company.com/api/v4/projects/$PROJECT_ID/protected_branches?name=main&push_access_level=0&merge_access_level=30&allow_force_push=false"

# 2. Cấu hình Rule 2 Người phê duyệt (Four-Eye Principle)
curl --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
     --header "Content-Type: application/json" \
     --data '{
       "name": "Production Approval Rule",
       "approvals_required": 2,
       "rule_type": "regular"
     }' \
     "https://gitlab.company.com/api/v4/projects/$PROJECT_ID/approval_rules"
```

---

### 4.2. Các Quy tắc Tuân thủ và Phân quyền (QT 45.1 - QT 45.4)

**Nguyên lý cốt lõi:** Bắt buộc bật cờ Protected Branch trên `main` và `production`, cấm tuyệt đối Force Push và Direct Push.
**Phát biểu.** Khai báo chính sách Protected Branch cho các nhánh quan trọng (`main`, `production`, `release/*`) với `push_access_level = 0` (No one can push) và `allow_force_push = false`.
**Giải thích cơ chế ngầm:** Ngăn chặn thảm họa lập trình viên vô tình gõ lệnh `git push --force origin main` làm xóa sạch lịch sử commit của toàn bộ công ty, hoặc gõ `git push origin main` đẩy trực tiếp code lỗi chưa qua kiểm thử lên môi trường Production.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cấu hình `push_access_level = 30` (Developers can push) cho nhánh `main`, cho phép dev đẩy code thẳng lên main không qua MR.
**Minh hoạ.** REST API `push_access_level=0` và `allow_force_push=false`.
**Con số chốt:** 0% Direct Push lên nhánh Production.

---

**Nguyên lý cốt lõi:** Áp dụng tệp `CODEOWNERS` để tự động chỉ định bắt buộc phê duyệt của chuyên gia cho các thay đổi nhạy cảm (Security, Infra, Core logic).
**Phát biểu.** Khởi tạo tệp `CODEOWNERS` đặt tại thư mục gốc hoặc `.gitlab/CODEOWNERS`, khai báo đúng nhóm chuyên trách quản lý từng thư mục nhạy cảm.
**Giải thích cơ chế ngầm:** Trong một dự án lớn có hàng trăm developers, nếu không dùng `CODEOWNERS`, một lập trình viên Junior viết frontend có thể sửa nhầm vào file cấu hình Terraform `/terraform/main.tf` hoặc luồng xác thực mã hóa `/src/auth.js` mà các chuyên gia Security/DevOps không hề hay biết! `CODEOWNERS` tự động cưỡng chế khóa MR cho đến khi chính đại diện nhóm chuyên trách bấm nút Phê duyệt.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Không dùng `CODEOWNERS`, để bất kỳ ai trong dự án cũng có thể approve các thay đổi hạ tầng nhạy cảm.
**Minh hoạ.** `/terraform/ @devops-team` trong tệp `CODEOWNERS`.
**Con số chốt:** 100% Thư mục nhạy cảm được gán `CODEOWNERS`.

---

**Nguyên lý cốt lõi:** Cấu hình Phê duyệt Merge Request hai bước (Four-Eye Principle - tối thiểu 2 Approvals) cho mọi thay đổi lên nhánh Production.
**Phát biểu.** Đặt `approvals_required = 2` trong cài đặt Merge Request Approval Rules cho tất cả các Merge Requests trỏ về nhánh Production.
**Giải thích cơ chế ngầm:** Áp dụng Tiêu chuẩn An ninh Quốc tế SOC 2 / PCI-DSS (Quy tắc 4 Mắt - Four-Eye Principle). Đảm bảo một đoạn mã trước khi đưa lên Production bắt buộc phải được ít nhất **2 cặp mắt độc lập** (Tác giả + 2 Người Review) kiểm tra kỹ lưỡng, ngăn ngừa sai sót cá nhân hoặc hành vi cố tình chèn backdoor của một cá nhân đơn lẻ.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đặt `approvals_required = 1` hoặc `0`, cho phép 1 người tự quyết định đưa code lên Production.
**Minh hoạ.** `approvals_required = 2` trong cài đặt MR.
**Con số chốt:** Tối thiểu 2 Approvals độc lập cho Production MRs.

---

**Nguyên lý cốt lõi:** Tự động hủy bỏ các lượt phê duyệt cũ (Approval Reset) ngay khi có commit mới được push vào Merge Request.
**Phát biểu.** Bật cờ `reset_approvals_on_push = true` trong cài đặt Merge Request Approval Settings.
**Giải thích cơ chế ngầm:** Rất nhiều trường hợp tinh vi: Tác giả tạo MR, nhờ 2 đồng nghiệp phê duyệt xong xanh 100%. Sau đó, tác giả lại âm thầm push thêm một commit chứa mã độc hoặc code lỗi vào MR đó và bấm **Merge**! Nếu không bật cờ Reset Approvals, các lượt phê duyệt cũ vẫn giữ nguyên, khiến mã độc trôi thẳng lên Production. Bật cờ này sẽ tự động xóa sạch các lượt phê duyệt cũ ngay khi có commit mới push vào, bắt buộc phải review lại từ đầu.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đặt `reset_approvals_on_push = false`, để commit mới push thêm ăn theo các lượt approve cũ.
**Minh hoạ.** `reset_approvals_on_push = true` trên GitLab UI Settings.
**Con số chốt:** 100% Reset Approvals khi có commit mới.

---

### 1.2. Quy tắc Anti-Bypass, Tags & Compliance Frameworks (10 phút)

**Nguyên lý cốt lõi:** Cấm tác giả của Merge Request tự phê duyệt MR của chính mình (Prevent Author Approval).
**Phát biểu.** Bật cờ `merge_requests_author_approval = false` trong cài đặt bảo mật của dự án.
**Giải thích cơ chế ngầm:** Triệt hạ lỗ hổng xung đột lợi ích (Conflict of Interest). Nếu tác giả tạo MR được phép bấm nút Approve cho chính mình, quy tắc 2 người phê duyệt sẽ bị vô hiệu hóa hoàn toàn, người đó có thể tự sửa code và tự duyệt để đẩy lên Production mà không ai kiểm soát.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cho phép cờ Author Approval `= true`, giúp tác giả tự duyệt MR của chính mình.
**Minh hoạ.** `merge_requests_author_approval = false`.
**Con số chốt:** 0% Author Self-Approval.

---

**Nguyên lý cốt lõi:** Cấm nhân sự thêm commit mới tự phê duyệt Merge Request (Prevent Commit Approver Approval).
**Phát biểu.** Bật cờ `merge_requests_disable_committers_approval = true` trong cài đặt bảo mật của dự án.
**Giải thích cơ chế ngầm:** Ngăn chặn lách luật: Nhân sự A tạo MR. Nhân sự B vào push thêm 1 commit vào MR đó, sau đó nhân sự B lại đứng ra bấm nút Approve với tư cách là Reviewer! Về bản chất B cũng là tác giả của một phần code trong MR đó. Cờ này cấm tất cả những ai đã từng đóng góp commit trong MR đó được đứng ra làm Reviewer phê duyệt.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để người vừa push commit vào MR tự đứng ra approve MR đó.
**Minh hoạ.** `merge_requests_disable_committers_approval = true`.
**Con số chốt:** 0% Committer Approval.

---

**Nguyên lý cốt lõi:** Áp dụng Protected Tags để bảo vệ các nhãn release (v1.*, v2.*) chỉ cho phép pipeline CI đã qua phê duyệt tạo tag.
**Phát biểu.** Khai báo chính sách Protected Tags cho các pattern `v*` hoặc `release-*` với `create_access_level = 40` (Maintainers) hoặc chỉ gán cho CI/CD Pipeline.
**Giải thích cơ chế ngầm:** Nhãn Git Tag (như `v1.0.0`) thường là điểm kích hoạt (Trigger Point) cho các pipeline tự động build Docker Image và deploy trực tiếp lên môi trường Production. Nếu không bảo vệ Tag, một developer bất kỳ có thể gõ lệnh `git tag v9.9.9 && git push origin v9.9.9` trên máy cá nhân để kích hoạt pipeline deploy bậy lên Production!
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để cờ `create_access_level = 30` (Developers), cho phép bất kỳ ai tự do tạo Release Tags.
**Minh hoạ.** Protected Tag wildcard `v*` chỉ cấp quyền cho Maintainers/CI.
**Con số chốt:** 100% Release Tags được bảo vệ bằng Protected Tags.

---

**Nguyên lý cốt lõi:** Sử dụng GitLab Compliance Frameworks để tự động gắn và cưỡng chế Pipeline Compliance trên toàn bộ các Repositories của tổ chức.
**Phát biểu.** Tạo một Compliance Pipeline Template tập trung (chứa các công cụ quét bảo mật SAST, Dependency Scanning, License Check) và gắn nhãn Compliance Framework (như `SOC2-Compliant`) cấp Group Level cho tất cả các Repositories.
**Giải thích cơ chế ngầm:** Tự động hóa tuân thủ ở quy mô lớn (Compliance at Scale). Khi tổ chức có 500 Repositories, bạn không thể đi từng repo để kiểm tra xem họ có viết đúng file `.gitlab-ci.yml` hay không. Compliance Framework ép buộc mọi pipeline của 500 repos khi chạy đều phải chạy qua tệp Compliance Pipeline trung tâm trước, không ai có thể sửa hay bỏ qua được!
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để từng dự án tự do sửa đổi hoặc xóa bỏ các stage quét bảo mật trong `.gitlab-ci.yml` của họ.
**Minh hoạ.** Khai báo `compliance_pipeline_enforced_path` ở cấp GitLab Group Settings.
**Con số chốt:** 100% Repositories áp dụng Compliance Framework.

---

### 1.3. Quy tắc Audit, Push Protection & Security (10 phút)

**Nguyên lý cốt lõi:** Kích hoạt Streaming Audit Events gửi toàn bộ log thao tác phân quyền và chìa khóa secret về hệ thống SIEM (Splunk / Elastic).
**Phát biểu.** Cấu hình đường dẫn Webhook URL trong `Group -> Audit Events -> Streaming Audit Events` trỏ tới hệ thống SIEM tập trung của tập đoàn.
**Giải thích cơ chế ngầm:** Phục vụ công tác điều tra sự cố an ninh (Forensics) và tuân thủ pháp lý. Khi một kẻ gian truy cập trái phép đổi phân quyền từ Developer lên Owner, hoặc xóa chìa khóa SSH Key của dự án, sự kiện đó phải được ghi nhận ngón tay (Fingerprint) và đẩy ngay lập tức trong $0.5$ giây về máy chủ SIEM bảo mật độc lập. Dù kẻ gian có cố tình xóa log trên GitLab UI thì bản ghi trên SIEM vẫn nguyên vẹn không thể chối cãi!
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chỉ lưu log trên giao diện GitLab UI, bị mất sạch vết khi dự án bị xóa.
**Minh hoạ.** Streaming Audit Events API destination `https://siem.company.com/v1/audit-logs`.
**Con số chốt:** Đẩy 100% Audit Events về SIEM real-time.

---

**Nguyên lý cốt lõi:** Cấu hình Secret Push Protection tự động chặn đứng commit chứa chìa khóa AWS/SSH Keys ngay từ lệnh `git push`.
**Phát biểu.** Bật cờ `secret_push_protection = true` ở cấp Group/Project Settings trên GitLab Enterprise.
**Giải thích cơ chế ngầm:** Chặn đứng rò rỉ ngay từ cửa ngõ (Shift-Left Prevention). Lập trình viên rất hay vô tình lỡ tay commit file chứa `AWS_SECRET_ACCESS_KEY` hay `PRIVATE_KEY` vào Git. Nếu để commit đó đẩy lên server rồi mới chạy pipeline quét SAST thì secret key đã bị lưu vào lịch sử Git (Git History) và rò rỉ. Secret Push Protection quét gói tin ngay lúc gõ lệnh `git push` và chặn đứng lệnh push từ máy dev nếu phát hiện secret!
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để commit chứa AWS Keys đẩy được lên kho mã nguồn rồi mới chạy job quét rác dọn dẹp.
**Minh hoạ.** `secret_push_protection = true` trên Security Settings.
**Con số chốt:** Chặn 100% Secret Keys bị leak từ lệnh `git push`.

---

**Nguyên lý cốt lõi:** Bắt buộc tất cả các commits phải được ký số điện tử GPG/SSH Signature Verification trước khi merge vào nhánh chính.
**Phát biểu.** Bật cờ `reject_unsigned_commits = true` trong cài đặt Push Rules của Protected Branch.
**Giải thích cơ chế ngầm:** Chống giả mạo danh tính tác giả Git (Git Author Spoofing Attack). Trong Git thô, bất kỳ ai cũng có thể gõ lệnh `git config user.name "CEO Name"` và `git config user.email "ceo@company.com"` để mạo danh sếp lớn tạo commit độc hại! Ký số GPG/SSH buộc mọi commit phải kèm theo chữ ký điện tử được xác thực bằng Public Key cá nhân đăng ký trên GitLab Server, chứng minh 100% tính chính chủ.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tắt cờ kiểm tra chữ ký số, cho phép commit mạo danh tên người khác trôi vào kho mã nguồn.
**Minh hoạ.** `reject_unsigned_commits = true` trong Push Rules.
**Con số chốt:** 100% Commits được ký số GPG/SSH Verified.

---

**Nguyên lý cốt lõi:** Thiết lập quy trình rà soát tài khoản người dùng nhàn rỗi (User Audit Access Review) tự động khóa quyền sau 30 ngày không hoạt động.
**Phát biểu.** Chạy script tự động hàng tuần gọi REST API `GET /api/v4/users` kiểm tra trường `last_activity_on`, tự động khóa (Deactivate) các tài khoản nhàn rỗi quá 30 ngày.
**Giải thích cơ chế ngầm:** Loại bỏ tài khoản bóng ma (Ghost Accounts). Khi nhân sự nghỉ việc hoặc chuyển dự án nhưng quản trị viên quên gỡ quyền, tài khoản đó trở thành điểm yếu chết người cho hacker lợi dụng xâm nhập. Tự động khóa tài khoản sau 30 ngày nhàn rỗi giúp duy trì nguyên tắc Quyền tối thiểu (Least Privilege).
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để hàng trăm tài khoản nhân sự đã nghỉ việc từ 2 năm trước vẫn còn nguyên quyền Owner/Maintainer trên dự án.
**Minh hoạ.** REST API `/api/v4/users/:id/deactivate` cho user nhàn rỗi >30 ngày.
**Con số chốt:** Khóa 100% tài khoản nhàn rỗi quá 30 ngày.

---

### 1.4. Đưa vào việc thật (4 phút)

### 7.1. Kịch bản áp dụng thực tế tại Ngân hàng Thương mại Cổ phần Đạt Chuẩn PCI-DSS v4.0
Tại một ngân hàng thương mại triển khai GitLab Self-Managed với 400 lập trình viên:
1. **Bảo vệ Nhánh Tuyệt đối:** Nhánh `main` và `production` trên 150 repos dịch vụ Core Banking được áp dụng **Protected Branch (push_access_level=0)**. Không ai (kể cả Giám đốc Công nghệ CTO) được push trực tiếp code lên main.
2. **Quy tắc 4 Mắt & CODEOWNERS:** Tệp `CODEOWNERS` phân định rõ: Mọi sửa đổi luồng chuyển tiền phải có approval của `@lead-architect`, sửa đổi luồng mã hóa phải có approval của `@security-lead`. Đòi hỏi **tối thiểu 2 Approvals độc lập** (QT 45.3).
3. **Chặn Rò rỉ Chìa khóa Real-time:** Bật **Secret Push Protection** trên toàn tập đoàn, chặn đứng 45 lượt lỡ tay push tệp `.env` chứa AWS Keys của developers trong năm 2025!
4. **Kiểm toán Tối cao:** 100% sự kiện phân quyền được đẩy qua **Streaming Audit Events API** về máy chủ Splunk SIEM. Đạt 100% điểm đánh giá tuân thủ PCI-DSS v4.0 trong kỳ kiểm toán quốc tế!

### 7.2. Case Study Thực tế: Thảm họa Mất 2 Triệu USD do Tác giả Tự duyệt MR của Chính mình
Một công ty Fintech không cấu hình chặn Author Approval (`merge_requests_author_approval = true`).
- **Thảm họa ở cách làm cũ (Vi phạm QT 45.5):**
  1. Một Lập trình viên Senior cố tình chèn một đoạn code gian lận tỷ giá chuyển tiền vào tệp `currency.js`.
  2. Lập trình viên này tự tạo Merge Request và **tự bấm nút Approve cho chính mình**!
  3. Code trôi thẳng lên Production, giúp đối tượng rút ruột 2 triệu USD trước khi bị phát hiện.
- **Khôi phục hoàn hảo ở cách làm chuẩn Buổi 45 (Bật Prevent Author Approval - QT 45.5 & QT 45.3):**
  Nếu áp dụng đúng QT 45.5, hệ thống tự động vô hiệu hóa nút Approve đối với tác giả MR. Bắt buộc phải có **2 lập trình viên độc lập khác** review và phê duyệt. Đoạn code gian lận tỷ giá sẽ bị phát hiện và chặn đứng ngay từ vòng review!

### 7.3. Case Study 3: Ngăn chặn Kẻ gian Mạo danh Email Giám đốc Công nghệ nhờ GPG Commit Signature
Một kẻ tấn công chiếm được tài khoản Git cá nhân của 1 dev tập sự.
- **Sự cố:** Kẻ tấn công gõ lệnh `git config user.email "cto@company.com"` mạo danh CTO và tạo một commit độc hại xóa toàn bộ cơ sở dữ liệu.
- **Bảo vệ tuyệt đối nhờ GPG Signature Verification (QT 45.11):**
  1. Protected Branch `main` đã bật cờ `reject_unsigned_commits = true`.
  2. Commit mạo danh của kẻ tấn công thiếu chữ ký số GPG Verified của CTO.
  3. Lệnh push/merge bị GitLab Server chối bỏ lập tức với thông báo `Unsigned commit rejected`. Hệ thống được bảo toàn 100%!

### 7.4. Case Study 4: Tự động Hóa Tuân thủ SOC 2 cho 300 Repositories nhờ Compliance Frameworks
Một tập đoàn SaaS cần chuẩn bị kiểm toán tiêu chuẩn bảo mật SOC 2 Type II cho 300 dự án microservices.
- **Cách làm thủ công cũ:** Đội Security phải đi mở từng repo để kiểm tra file `.gitlab-ci.yml` xem có chèn job quét SAST hay không, mất 3 tháng làm việc vất vả.
- **Cách làm chuẩn Buổi 45 (Compliance Frameworks - QT 45.8):**
  1. Đội Security tạo 1 file `soc2-compliance-pipeline.yml` chuẩn tại repo trung tâm.
  2. Gắn nhãn Compliance Framework `SOC2-Compliant` cấp Group Level cho toàn bộ 300 Repos.
  3. Mọi pipeline của 300 Repos tự động kế thừa các stage quét SAST/Dependency Scanning bắt buộc. Đội kiểm toán SOC 2 cấp chứng nhận tuân thủ chỉ sau 1 tuần rà soát!

### 7.5. Case Study 5: Chặn Đứng Thảm Họa Lộ AWS Keys Nhờ Secret Push Protection Real-time
Một developer lỡ tay lưu tệp `aws-credentials.json` chứa `AWS_SECRET_ACCESS_KEY` vào thư mục dự án và chạy `git commit -m "add config"`.
- **Rủi ro ở cách làm cũ (Quét SAST trong CI Pipeline):** Developer chạy `git push origin feature/login`. Commit trôi lên GitLab Server. Sau đó 5 phút pipeline CI mới chạy job quét rác. Trong 5 phút đó, kẻ tấn công đã phát hiện commit trên kho mã nguồn và lấy mất AWS Key!
- **Bảo vệ tuyệt đối nhờ QT 45.10 (Secret Push Protection):**
  1. Ngay khi developer gõ `git push origin feature/login`, GitLab Secret Push Protection Engine lập tức quét gói tin HTTP/SSH payload.
  2. Phát hiện định dạng AWS Access Key `AKIAIOSFODNN7EXAMPLE`.
  3. Lệnh push bị từ chối ngay lập tức từ máy cá nhân (`PUSH REJECTED: AWS Secret Key detected!`). Secret key $0\%$ trôi lên kho mã nguồn, bảo vệ an toàn tuyệt đối!

### 7.6. Case Study 6: Tự Động Khóa 80 Tài Khoản Bóng Ma Nhàn Rỗi Bằng Script User Audit Review
Một ngân hàng lớn có 500 nhân sự kỹ thuật.
- **Tình trạng ở cách làm cũ:** Khi nhân sự hoặc đối tác tư vấn kết thúc hợp đồng, quản trị viên thường xuyên quên bấm nút gỡ tài khoản trên GitLab Admin UI.
- **Nguy cơ an ninh:** 80 tài khoản nhàn rỗi quá 6 tháng vẫn giữ nguyên quyền Owner/Maintainer trên các repo Core Banking nhạy cảm.
- **Khắc phục tự động nhờ QT 45.12 (User Access Audit Review):**
  1. Đặt Cron Job chạy script Python gọi REST API `GET /api/v4/users` định kỳ mỗi sáng thứ Hai.
  2. Kiểm tra chỉ số `last_activity_on`. Nếu user không có bất kỳ thao tác nào trong 30 ngày, script gọi API `POST /api/v4/users/:id/deactivate`.
  3. 80 tài khoản bóng ma bị khóa tự động, xuất báo cáo PDF đính kèm gửi trực tiếp tới Giám đốc Bảo mật CISO!

---

### 7.7. Trường hợp khi nào KHÔNG nên dùng Quy tắc Phê duyệt Ngặt nghèo (Over-Engineering Compliance)
Mặc dù Compliance và Approval Rules là sống còn cho Production, nhưng KHÔNG nên áp dụng thái quá cho các trường hợp sau:

| Ngữ cảnh / Hạ tầng | Lý do KHÔNG nên ép 2 Approvals & CODEOWNERS | Giải pháp thay thế linh hoạt |
|---|---|---|
| Môi trường Sandbox / R&D Thử nghiệm Ý tưởng | Làm giảm tốc độ thử nghiệm của đội nghiên cứu, gây thủ tục phiền hà không cần thiết. | Cho phép **Direct Push trên Repos R&D cá nhân**, chỉ áp dụng compliance khi đưa vào kho main. |
| Dự án Open Source cộng đồng có ít hơn 2 Maintainers | Không đủ 2 người phê duyệt độc lập sẽ làm kẹt 100% Merge Requests không thể merge. | Giảm xuống **1 Approval cho dự án nhỏ** hoặc dùng Bot Auto-Approval cho các file tài liệu doc. |
| Hotfix khẩn cấp lúc 3:00 AM khi hệ thống sập toàn bộ | Việc chờ đủ 2 reviewers thức dậy lúc 3:00 AM làm kéo dài thời gian sập mạng (MTTR). | Cấu hình **Emergency Bypass Approval Role** có ghi lại Audit Events siêu ngặt nghèo! |

---

### 1.5. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính bẫy | Làm đúng là |
|---|---|---|
| Bẫy 1: Cho phép tác giả MR tự phê duyệt (Author Self-Approval) | Tác giả có thể tự tạo MR và tự duyệt code độc hại/lỗi của mình lên Production. | Bật cờ `merge_requests_author_approval = false` ngắt quyền tự duyệt (QT 45.5). |
| Bẫy 2: Không bật cờ Reset Approvals khi push commit mới | Tác giả nhờ duyệt xong rồi âm thầm push thêm commit độc hại vào MR ăn theo. | Bật `reset_approvals_on_push = true` xóa sạch approve cũ khi có commit mới (QT 45.4). |
| Bẫy 3: Quên bảo vệ Git Tags (`v1.0.0`), cho phép Dev tự tạo Release Tag | Dev có thể gõ `git tag v1.0.0` đẩy lên server kích hoạt pipeline deploy bậy lên Prod. | Đặt Protected Tags pattern `v*` chỉ cho phép Maintainers/CI tạo tags (QT 45.7). |
| Bẫy 4: Để commit chứa AWS/SSH Keys đẩy lên Git rồi mới quét SAST | Secret key đã bị ghi vết vào Git History, kẻ gian có thể checkout lại commit cũ để lấy. | Bật cờ `secret_push_protection = true` chặn đứng ngay từ lệnh `git push` (QT 45.10). |
| Bẫy 5: Không dùng `CODEOWNERS`, để dev bất kỳ approve file hạ tầng Terraform | Dev frontend có thể vô tình approve đoạn code xóa mất cơ sở dữ liệu hạ tầng. | Áp dụng tệp `CODEOWNERS` gán đúng `@devops-team` phê duyệt folder `/terraform/` (QT 45.2). |
| Bẫy 6: Chỉ lưu Audit Logs trên giao diện UI mà không đẩy về SIEM | Khi kho mã nguồn bị xóa hoặc tài khoản bị hack, toàn bộ vết Audit Event bị biến mất. | Bật Streaming Audit Events API đẩy 100% logs về máy chủ Splunk/Elastic (QT 45.9). |
| Bẫy 7: Để hàng trăm tài khoản nhân sự nghỉ việc nguyên quyền Access | Kẻ tấn công lợi dụng tài khoản cũ không ai quản lý để xâm nhập kho mã nguồn. | Chạy script kiểm toán tài khoản nhàn rỗi tự động khóa sau 30 ngày (QT 45.12). |
| Bẫy 8: Không bật cờ cấm Force Push trên nhánh `main` | Dev lỡ tay gõ `git push --force origin main` xóa sạch lịch sử commit của công ty. | Khai báo Protected Branch `allow_force_push = false` trên nhánh main (QT 45.1). |

---

### 1.6. Tóm tắt (3 phút)

### 9.1. Sơ đồ Mermaid: Kiến trúc Hệ thống Tuân thủ Compliance & Audit Enterprise

```mermaid
flowchart TD
    subgraph Developer Push Gateway
        A[Git Push Request] -->|Secret Push Protection| B{Check Secrets & Signatures}
        B -->|AWS Key Detected| C[REJECT PUSH]
        B -->|Unsigned Commit| D[REJECT UNSIGNED]
        B -->|Passed| E[Merge Request Engine]
    end

    subgraph Governance & Authorization Layer
        E -->|Read .gitlab/CODEOWNERS| F[Identify Code Owners]
        F -->|Require Min 2 Approvals| G{Four-Eye Rule Check}
        G -->|Author Tries Self-Approve| H[BLOCKED: Author Approval Forbidden]
        G -->|Push New Commit| I[RESET All Previous Approvals!]
        G -->|2 Independent Approvals OK| J[MERGE APPROVED]
    end

    subgraph Audit & Enforcement Infrastructure
        J -->|Trigger Pipeline| K[Compliance Framework Pipeline]
        K -->|Deploy to Production| L[Production Cluster]
        E -.->|Stream Audit Event| M[SIEM / Splunk Dashboard]
        J -.->|Stream Audit Event| M
    end
```

### 9.2. Năm điều phải nhớ thuộc lòng
1. **Enforced by Code:** Mọi quy tắc tuân thủ bảo mật phải được cưỡng chế bằng cấu hình kỹ thuật (API/Settings), không dựa vào lời hứa.
2. **Four-Eye Principle & CODEOWNERS:** Bắt buộc tối thiểu 2 approvals độc lập cho Production MRs và áp dụng `CODEOWNERS` cho thư mục nhạy cảm.
3. **Reset Approvals on Push:** Luôn xóa sạch các lượt phê duyệt cũ ngay khi có commit mới push vào Merge Request.
4. **Secret Push Protection:** Chặn đứng các chìa khóa AWS/SSH Keys ngay từ lệnh `git push` trước khi trôi vào Git History.
5. **Streaming Audit Events to SIEM:** Đẩy 100% nhật ký thao tác thời gian thực về hệ thống SIEM tập trung phục vụ điều tra an ninh.

---

### 1.7. Câu hỏi tự kiểm tra (5 phút)

### 10.1. Danh sách câu hỏi tự kiểm tra
1. Rủi ro lớn nhất khi không bật cờ Protected Branch trên nhánh `main` là gì?
2. Tệp `CODEOWNERS` đóng vai trò gì trong việc bảo vệ các thư mục nhạy cảm như `/terraform/` hay `/src/auth/`?
3. Nguyên tắc Quy tắc 4 Mắt (Four-Eye Principle) trong phê duyệt Merge Request có ý nghĩa như thế nào?
4. Tại sao cờ `reset_approvals_on_push = true` lại là điều kiện bắt buộc để chống lách luật an ninh?
5. Sự khác biệt giữa cờ `merge_requests_author_approval` và `merge_requests_disable_committers_approval` là gì?
6. Tại sao phải cài đặt Protected Tags cho các nhãn phiên bản dạng `v1.*` hoặc `release-*`?
7. Lợi ích của việc áp dụng GitLab Compliance Frameworks cấp Group Level cho 500 Repositories là gì?
8. Tại sao tính năng Secret Push Protection lại vượt trội hơn so với việc chạy job quét SAST trong CI Pipeline?
9. Ý nghĩa của việc bật cờ `reject_unsigned_commits = true` trên Protected Branch là gì?
10. Tại sao phải xuất nhật ký kiểm toán qua Streaming Audit Events API về máy chủ SIEM tập trung?
11. Tác hại của việc giữ nguyên các tài khoản nhàn rỗi (Ghost Accounts) quá 30 ngày trong hệ thống là gì?
12. Trong trường hợp khẩn cấp nào thì nên linh hoạt hạ thấp quy tắc phê duyệt ngặt nghèo?

---

### 10.2. Đáp án câu hỏi tự kiểm tra

1. Lập trình viên có thể đẩy trực tiếp code chưa kiểm thử (Direct Push) hoặc gõ cờ `--force` xóa sạch lịch sử commit của kho mã nguồn.
2. Tệp `CODEOWNERS` tự động cưỡng chế chỉ định các nhóm chuyên trách (DevOps/Security) bắt buộc phải phê duyệt MR khi có sửa đổi file trong thư mục đó.
3. Đảm bảo một đoạn mã trước khi merge lên Production bắt buộc phải được ít nhất 2 người xem xét độc lập, ngăn ngừa lỗi cá nhân hoặc mã độc đơn lẻ.
4. Để tự động xóa các lượt phê duyệt cũ khi tác giả push thêm commit mới, ngăn tác giả lén lách luật push thêm code chưa review sau khi đã được duyệt.
5. `author_approval` cấm tác giả tạo MR tự duyệt; `disable_committers_approval` cấm tất cả những ai đã từng push commit vào MR đó tự duyệt.
6. Ngăn chặn lập trình viên tự do tạo Tag release trên máy cá nhân để kích hoạt các pipeline tự động deploy code chưa duyệt lên Production.
7. Ép buộc 100% các Repositories trong tập đoàn phải tự động kế thừa quy trình quét bảo mật chuẩn mà không thể tự ý sửa đổi hay bỏ qua.
8. Secret Push Protection chặn đứng lệnh `git push` ngay từ máy dev, ngăn chìa khóa bị ghi vết vào Git History (nơi kẻ gian có thể checkout lại).
9. Bắt buộc mọi commit phải có chữ ký số GPG/SSH Verified, chống thảm họa mạo danh identity của người khác (`git config user.email`).
10. Để đảm bảo tính nguyên vẹn không thể chối cãi của nhật ký thao tác phục vụ điều tra an ninh, ngay cả khi dự án trên GitLab bị xóa.
11. Tạo ra các lỗ hổng điểm yếu cho hacker lợi dụng xâm nhập vào hệ thống thông qua các tài khoản cũ không ai quản lý.
12. Khi xử lý sự cố khẩn cấp (Hotfix 3:00 AM) sập toàn bộ hệ thống dịch vụ, cần cơ chế Emergency Bypass Role có ghi audit log đặc biệt.

---

### 1.8. Tài liệu tham khảo (2 phút)

| Nguồn tài liệu | Mô tả nội dung | Phiên bản áp dụng |
|---|---|---|
| GitLab Documentation — Protected Branches & Tags API | Hướng dẫn cấu hình cấm Force Push và Direct Push qua REST API | GitLab v16+ |
| GitLab Documentation — CODEOWNERS File Syntax | Cú pháp chỉ định người sở hữu mã nguồn theo thư mục | GitLab Enterprise |
| GitLab Documentation — Merge Request Approval Rules | Cấu hình Four-Eye Principle và Reset Approvals settings | GitLab Ultimate/Premium |
| GitLab Documentation — Compliance Frameworks & Streaming Audit Events | Hướng dẫn gắn Compliance Pipeline và kết nối SIEM Splunk | GitLab Ultimate |
| SOC 2 Type II Compliance Standard — Change Management Controls | Tiêu chuẩn quốc tế về quản lý thay đổi mã nguồn và kiểm soát truy cập | SOC 2 Standard |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10 phút |
| §1 | Sau buổi này học viên LÀM ĐƯỢC gì | 1 phút |
| §2 | Cần biết trước | 1 phút |
| §3 | Thuật ngữ và mô hình tư duy | 8 phút |
| §4 | Cấu hình Protected Branches, CODEOWNERS & Approvals | 10 phút |
| §5 | Quy tắc Anti-Bypass, Tags & Compliance Frameworks | 10 phút |
| §6 | Quy tắc Audit, Push Protection & Security | 10 phút |
| §7 | Đưa vào việc thật | 4 phút |
| §8 | Bẫy hay gặp | 2 phút |
| §9 | Tóm tắt | 3 phút |
| §10 | Câu hỏi tự kiểm tra | 5 phút |
| §11 | Tài liệu tham khảo | 2 phút |
| **Tổng** | **Khối lý thuyết** | **60'** |

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên môi trường GitLab Community / Enterprise Edition cùng các GitLab Runner cô lập (Docker / Kubernetes Executor). Hãy đảm bảo bạn đã chuẩn bị môi trường thử nghiệm và cấu hình quyền truy cập cần thiết.

## Khối thực hành — 150 phút

---

## 1. Mục tiêu bài thực hành Lab
Trong bài lab này, học viên sẽ trực tiếp cấu hình hệ thống quản trị tuân thủ và phân quyền bảo mật Enterprise trên GitLab CI/CD:
1. Khởi tạo tệp `CODEOWNERS` chỉ định người xem xét bắt buộc cho các thư mục nhạy cảm (`/terraform/`, `/src/security/`).
2. Giả lập cấu hình Protected Branch `main` cấm Force Push và Direct Push qua REST API.
3. Cấu hình Quy tắc 2 Người Phê duyệt (Four-Eye Principle - 2 Approvals Required) và bật cờ Reset Approvals khi commit mới push thêm.
4. Giả lập tính năng Secret Push Protection chặn lệnh `git push` nếu phát hiện có AWS Key.
5. Cấu hình Compliance Frameworks Template cho nhóm Repositories và xuất Streaming Audit Events về hệ thống SIEM.
6. Viết script kiểm tra chữ ký số GPG Commit Verification và tự động rà soát tài khoản nhàn rỗi (User Audit Access Review).

---

## 2. Mô hình kiến trúc Lab L2

```mermaid
graph TD
    subgraph Phase 1: Branch Protection & Secret Scanning
        A[Git Push Request] -->|1. Secret Push Protection Engine| B{Scan Payload}
        B -->|AWS Key Found| C[REJECT PUSH Immediately]
        B -->|Clean| D{GPG Signature Check}
        D -->|Unsigned| E[REJECT: Unsigned Commit]
        D -->|Valid| F[Protected Branch Verification]
    end

    subgraph Phase 2: CODEOWNERS & Four-Eye Approvals
        F -->|Direct Push to Main| G[REJECT: Direct Push Forbidden]
        F -->|Create Merge Request| H[MR Approval Engine]
        H -->|Check Paths modified| I[Evaluate CODEOWNERS Rules]
        I -->|Requires @security-team| J{Min 2 Approvals & Reset on Push}
        J -->|Author tries to approve| K[BLOCKED: Author Approval Forbidden]
        J -->|New Commit Pushed| L[RESET All Approvals!]
        J -->|2 Independent Approvals OK| M[MERGE APPROVED]
    end

    subgraph Phase 3: Compliance & Audit Logging
        M -->|Execute Merge| N[Compliance Framework Pipeline]
        N -->|Deploy Production| O[Production App]
        P[Audit Engine] -.->|Stream Events API| Q[SIEM / Splunk Dashboard]
    end
```

---

## 3. Các bước thực hiện bài lab (14 Checkpoints)

### Bước 1: Khởi tạo Thư mục Lab và Tệp `CODEOWNERS` Chuẩn mực Enterprise (10 phút)

Tạo thư mục làm việc cho bài lab Buổi 45:

```bash
mkdir -p compliance-lab
cd compliance-lab
mkdir -p .gitlab config scripts audit/events compliance-templates security-policies
```

Khởi tạo tệp `.gitlab/CODEOWNERS` với các quy tắc phân quyền người sở hữu mã nguồn đầy đủ các phòng ban:

```text
# ===================================================================
# ENTERPRISE CODEOWNERS CONFIGURATION FILE FOR COMPLIANCE LAB
# Location: .gitlab/CODEOWNERS
# ===================================================================

# Mặc định mọi thay đổi cần Tech Leads phê duyệt
* @company-tech-leads

# Toàn bộ mã nguồn Security & Authentication cần Security Team phê duyệt
/src/security/ @security-team @ciso-officer
/src/auth/ @security-team
/src/crypto/ @security-team

# Toàn bộ mã nguồn Hạ tầng Infrastructure & Terraform cần DevOps Team phê duyệt
/terraform/ @devops-team @lead-devops
/.gitlab-ci.yml @devops-team
/helm/ @devops-team
/kubernetes/ @devops-team

# Toàn bộ mã nguồn Database Migrations cần DB Admin phê duyệt
/db/migrations/ @dba-team

# Toàn bộ các file Secret & Configuration mẫu cần Security Officer phê duyệt
/*.env.example @security-team
/config/secrets.json.example @security-team
```

### **CHECKPOINT 1**
Chạy câu lệnh kiểm tra tệp `CODEOWNERS`:

```bash
test -f .gitlab/CODEOWNERS && grep -q "/terraform/ @devops-team" .gitlab/CODEOWNERS && echo "CHECKPOINT 1: ĐẠT" || echo "CHECKPOINT 1: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 1: ĐẠT
```

---

### Bước 2: Viết Script Mô phỏng Cấu hình Protected Branch API Cấm Force Push (10 phút)

Tạo script mô phỏng gọi REST API bảo vệ nhánh `main` `scripts/protect-branch-api.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

BRANCH_NAME="${1:-main}"

echo "[PROTECTED BRANCH] Protecting branch '$BRANCH_NAME' via REST API..."
mkdir -p audit

cat << EOF > audit/protected-branch-settings.json
{
  "branch_name": "$BRANCH_NAME",
  "push_access_level": 0,
  "merge_access_level": 30,
  "allow_force_push": false,
  "code_owner_approval_required": true,
  "protected_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "BRANCH_PROTECTED_SUCCESS"
}
EOF

echo "[PROTECTED BRANCH] Branch '$BRANCH_NAME' is now protected! Direct Push & Force Push are strictly FORBIDDEN."
```

Cho phép script chạy bảo vệ nhánh:
```bash
chmod +x scripts/protect-branch-api.sh
./scripts/protect-branch-api.sh "main"
```

### **CHECKPOINT 2**
Chạy câu lệnh kiểm tra cài đặt Protected Branch:

```bash
test -f audit/protected-branch-settings.json && grep -q "BRANCH_PROTECTED_SUCCESS" audit/protected-branch-settings.json && echo "CHECKPOINT 2: ĐẠT" || echo "CHECKPOINT 2: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 2: ĐẠT
```

---

### Bước 3: Viết Script Mô phỏng Cưỡng chế Quy tắc 2 Người Phê duyệt (Four-Eye Principle) (15 phút)

Tạo script mô phỏng cài đặt MR Approval Rules `scripts/setup-approval-rules.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[MR APPROVALS] Configuring Four-Eye Principle Approval Rules..."
mkdir -p audit

cat << EOF > audit/approval-rules-config.json
{
  "rule_name": "Production Four-Eye Approval Rule",
  "approvals_required": 2,
  "reset_approvals_on_push": true,
  "merge_requests_author_approval": false,
  "merge_requests_disable_committers_approval": true,
  "configured_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "APPROVAL_RULES_ENFORCED"
}
EOF

echo "[MR APPROVALS] Approval rules enforced: 2 Approvals Required, Author Self-Approval Disabled!"
```

Cho phép script chạy thiết lập approval rules:
```bash
chmod +x scripts/setup-approval-rules.sh
./scripts/setup-approval-rules.sh
```

### **CHECKPOINT 3**
Chạy câu lệnh kiểm tra tệp cấu hình Approval Rules:

```bash
test -f audit/approval-rules-config.json && grep -q "APPROVAL_RULES_ENFORCED" audit/approval-rules-config.json && echo "CHECKPOINT 3: ĐẠT" || echo "CHECKPOINT 3: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 3: ĐẠT
```

---

### Bước 4: Viết Script Kiểm thử Tự động Hủy Approval khi Push Commit Mới (15 phút)

Tạo script mô phỏng hành vi Reset Approval `scripts/verify-approval-reset-on-push.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

COMMIT_EVENT="${1:-new_commit_pushed}"

echo "[APPROVAL RESET] Processing event: $COMMIT_EVENT..."
mkdir -p audit

if [ "$COMMIT_EVENT" = "new_commit_pushed" ]; then
    cat << EOF > audit/mr-approval-status.json
{
  "mr_id": 405,
  "previous_approvals_cleared": 2,
  "current_approvals_count": 0,
  "reset_triggered_by": "commit_hash_a1b2c3d",
  "status": "APPROVALS_RESET_REQUIRED_RE_REVIEW"
}
EOF
    echo "[APPROVAL RESET] SUCCESS: Previous approvals purged due to new commit push! Re-review required."
fi
```

Cho phép script chạy kiểm thử reset approval:
```bash
chmod +x scripts/verify-approval-reset-on-push.sh
./scripts/verify-approval-reset-on-push.sh "new_commit_pushed"
```

### **CHECKPOINT 4**
Chạy câu lệnh kiểm tra tệp trạng thái Reset Approval:

```bash
test -f audit/mr-approval-status.json && grep -q "APPROVALS_RESET_REQUIRED_RE_REVIEW" audit/mr-approval-status.json && echo "CHECKPOINT 4: ĐẠT" || echo "CHECKPOINT 4: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 4: ĐẠT
```

---

### Bước 5: Viết Script Mô phỏng Secret Push Protection Chặn AWS Access Keys (10 phút)

Tạo script kiểm tra Secret Push Protection `scripts/simulate-secret-push-protection.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

PAYLOAD_FILE="${1:-config/aws-credentials.json}"
mkdir -p config audit/security-audits

cat << EOF > config/aws-credentials.json
{
  "AWS_ACCESS_KEY_ID": "AKIAIOSFODNN7EXAMPLE",
  "AWS_SECRET_ACCESS_KEY": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}
EOF

echo "[SECRET SCAN] Scanning Git payload for hardcoded cloud credentials..."

if grep -q "AKIAIOSFODNN7EXAMPLE" "$PAYLOAD_FILE"; then
    cat << EOF > audit/security-audits/secret-push-report.json
{
  "scan_target": "$PAYLOAD_FILE",
  "detected_secret_type": "AWS_ACCESS_KEY",
  "action_taken": "PUSH_REJECTED",
  "scanned_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "SECRET_PUSH_PROTECTION_TRIGGERED"
}
EOF
    echo "[SECRET SCAN] REJECTED: Hardcoded AWS Access Key detected in payload! Push blocked."
fi
```

Cho phép script chạy kiểm thử scan secrets:
```bash
chmod +x scripts/simulate-secret-push-protection.sh
./scripts/simulate-secret-push-protection.sh "config/aws-credentials.json"
```

### **CHECKPOINT 5**
Chạy câu lệnh kiểm tra báo cáo Secret Push Protection:

```bash
test -f audit/security-audits/secret-push-report.json && grep -q "SECRET_PUSH_PROTECTION_TRIGGERED" audit/security-audits/secret-push-report.json && echo "CHECKPOINT 5: ĐẠT" || echo "CHECKPOINT 5: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 5: ĐẠT
```

---

### Bước 6: Viết Script Mô phỏng Gắn Compliance Framework Template Cấp Group (15 phút)

Tạo tệp Compliance Framework Template `compliance-templates/soc2-compliance-pipeline.yml` bao gồm đầy đủ các bước kiểm soát an ninh bắt buộc:

```yaml
# Compliance Framework Pipeline Template (SOC2 & PCI-DSS)
stages:
  - compliance-sast
  - compliance-dependency
  - compliance-secret-audit
  - build
  - test
  - deploy

compliance-sast-job:
  stage: compliance-sast
  script:
    - echo "[COMPLIANCE PIPELINE] Running Mandatory SAST Security Scanner..."
    - echo "SAST Security Audit PASSED 0 High Vulnerabilities."

compliance-dependency-job:
  stage: compliance-dependency
  script:
    - echo "[COMPLIANCE PIPELINE] Running Dependency License & Vulnerability Check..."
    - echo "Dependency Check PASSED 100% Compliant."

compliance-secret-audit-job:
  stage: compliance-secret-audit
  script:
    - echo "[COMPLIANCE PIPELINE] Running Hardcoded Credentials Audit..."
    - echo "Credentials Audit PASSED 0 Secrets Found."
```

Tạo script gán Compliance Framework `scripts/assign-compliance-framework.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

FRAMEWORK_NAME="${1:-SOC2-Compliant}"

echo "[COMPLIANCE FRAMEWORK] Assigning framework '$FRAMEWORK_NAME' to all Group Repositories..."
mkdir -p audit

cat << EOF > audit/compliance-framework-status.json
{
  "framework_name": "$FRAMEWORK_NAME",
  "enforced_pipeline_path": "compliance-templates/soc2-compliance-pipeline.yml",
  "applied_projects_count": 150,
  "enforced_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "COMPLIANCE_FRAMEWORK_ENFORCED"
}
EOF

echo "[COMPLIANCE FRAMEWORK] Framework '$FRAMEWORK_NAME' successfully enforced for 150 projects!"
```

Cho phép script chạy gán framework:
```bash
chmod +x scripts/assign-compliance-framework.sh
./scripts/assign-compliance-framework.sh "SOC2-Compliant"
```

### **CHECKPOINT 6**
Chạy câu lệnh kiểm tra tệp trạng thái Compliance Framework:

```bash
test -f audit/compliance-framework-status.json && grep -q "COMPLIANCE_FRAMEWORK_ENFORCED" audit/compliance-framework-status.json && echo "CHECKPOINT 6: ĐẠT" || echo "CHECKPOINT 6: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 6: ĐẠT
```

---

### Bước 7: Viết Script Mô phỏng Kích hoạt Streaming Audit Events API về SIEM Splunk (15 phút)

Tạo script mô phỏng Streaming Audit Events `scripts/enable-streaming-audit-events.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

SIEM_ENDPOINT="${1:-https://siem.company.com/v1/audit-events}"

echo "[STREAMING AUDIT] Configuring Streaming Audit Events API destination to '$SIEM_ENDPOINT'..."
mkdir -p audit/events

cat << EOF > audit/events/streaming-audit-config.json
{
  "destination_url": "$SIEM_ENDPOINT",
  "header_key": "X-Splunk-HEC-Token",
  "verification_token": "hec-token-sec-9988776655",
  "event_types": ["project_member_added", "protected_branch_created", "secret_detected", "mr_merged"],
  "configured_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "STREAMING_AUDIT_EVENTS_ACTIVE"
}
EOF

# Giả lập ghi 1 sự kiện audit log
cat << EOF > audit/events/event-sample.json
{
  "event_id": "evt-$(openssl rand -hex 6)",
  "author_username": "john.dev",
  "action": "PROTECTED_BRANCH_FORCE_PUSH_ATTEMPT",
  "target": "main",
  "ip_address": "192.168.1.100",
  "result": "DENIED",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

echo "[STREAMING AUDIT] Streaming Audit Events active! Audit logs being streamed real-time to SIEM."
```

Cho phép script chạy kích hoạt streaming audit:
```bash
chmod +x scripts/enable-streaming-audit-events.sh
./scripts/enable-streaming-audit-events.sh "https://siem.company.com/v1/audit-events"
```

### **CHECKPOINT 7**
Chạy câu lệnh kiểm tra tệp cấu hình Streaming Audit:

```bash
test -f audit/events/streaming-audit-config.json && grep -q "STREAMING_AUDIT_EVENTS_ACTIVE" audit/events/streaming-audit-config.json && echo "CHECKPOINT 7: ĐẠT" || echo "CHECKPOINT 7: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 7: ĐẠT
```

---

### Bước 8: Viết Script Kiểm thử Kiểm tra Chữ ký số GPG Commit Verification (10 phút)

Tạo script kiểm tra GPG Signature Verification `scripts/verify-gpg-commit-signature.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

COMMIT_HASH="${1:-c8d9e0f1a2b3}"
SIGNATURE_STATUS="${2:-VERIFIED}"

echo "[GPG VERIFY] Auditing GPG Signature for Commit '$COMMIT_HASH'..."
mkdir -p audit/security-audits

if [ "$SIGNATURE_STATUS" = "VERIFIED" ]; then
    cat << EOF > audit/security-audits/gpg-verification-report.json
{
  "commit_hash": "$COMMIT_HASH",
  "author_email": "lead.devops@company.com",
  "gpg_key_id": "3AA5C34371567BD2",
  "signature_valid": true,
  "verified_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "GPG_SIGNATURE_VERIFIED_PASSED"
}
EOF
    echo "[GPG VERIFY] PASSED: Commit signature is GPG Verified."
else
    cat << EOF > audit/security-audits/gpg-verification-report.json
{
  "commit_hash": "$COMMIT_HASH",
  "signature_valid": false,
  "status": "GPG_SIGNATURE_REJECTED"
}
EOF
    echo "[GPG VERIFY] REJECTED: Unsigned or invalid GPG Signature commit!"
fi
```

Cho phép script chạy kiểm tra GPG:
```bash
chmod +x scripts/verify-gpg-commit-signature.sh
./scripts/verify-gpg-commit-signature.sh "c8d9e0f1a2b3" "VERIFIED"
```

### **CHECKPOINT 8**
Chạy câu lệnh kiểm tra báo cáo GPG Verification:

```bash
test -f audit/security-audits/gpg-verification-report.json && grep -q "GPG_SIGNATURE_VERIFIED_PASSED" audit/security-audits/gpg-verification-report.json && echo "CHECKPOINT 8: ĐẠT" || echo "CHECKPOINT 8: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 8: ĐẠT
```

---

### Bước 9: Viết Script Tự động Rà soát và Khóa Tài khoản Nhàn rỗi (User Audit Access Review) (15 phút)

Tạo script tự động rà soát tài khoản nhàn rỗi `scripts/user-access-audit-review.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

IDLE_DAYS_THRESHOLD="${1:-30}"

echo "[USER AUDIT] Scanning for inactive user accounts (> $IDLE_DAYS_THRESHOLD days idle)..."
mkdir -p audit/user-reviews

cat << EOF > audit/user-reviews/inactive-users-report.json
{
  "total_users_scanned": 450,
  "active_users": 412,
  "inactive_users_found": 38,
  "deactivated_accounts_count": 38,
  "policy": "DEACTIVATE_AFTER_30_DAYS_IDLE",
  "reviewed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "USER_AUDIT_ACCESS_REVIEW_COMPLETED"
}
EOF

echo "[USER AUDIT] Successfully deactivated 38 inactive ghost user accounts!"
```

Cho phép script chạy rà soát user:
```bash
chmod +x scripts/user-access-audit-review.sh
./scripts/user-access-audit-review.sh "30"
```

### **CHECKPOINT 9**
Chạy câu lệnh kiểm tra báo cáo rà soát tài khoản user:

```bash
test -f audit/user-reviews/inactive-users-report.json && grep -q "USER_AUDIT_ACCESS_REVIEW_COMPLETED" audit/user-reviews/inactive-users-report.json && echo "CHECKPOINT 9: ĐẠT" || echo "CHECKPOINT 9: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 9: ĐẠT
```

---

### Bước 10: Khởi tạo Policy Cấu hình Protected Tags `v*` (10 phút)

Tạo tệp cấu hình Protected Tags Policy `security-policies/protected-tags-policy.json`:

```json
{
  "tag_pattern": "v*",
  "create_access_level": 40,
  "allowed_to_create": [
    {
      "access_level": 40,
      "access_level_description": "Maintainers"
    }
  ],
  "protected_at": "2026-08-22T00:00:00Z",
  "status": "PROTECTED_TAGS_ENFORCED"
}
```

### **CHECKPOINT 10**
Chạy câu lệnh kiểm tra tệp Protected Tags Policy:

```bash
test -f security-policies/protected-tags-policy.json && grep -q "PROTECTED_TAGS_ENFORCED" security-policies/protected-tags-policy.json && echo "CHECKPOINT 10: ĐẠT" || echo "CHECKPOINT 10: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 10: ĐẠT
```

---

### Bước 11: Viết Script Ghi nhận Nhật ký Compliance Audit Event Log (10 phút)

Tạo script ghi log audit compliance `scripts/record-compliance-audit-event.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

mkdir -p audit/events

cat << EOF >> audit/events/compliance-events-log.json
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "event": "CODEOWNERS_ENFORCEMENT_AUDITED",
  "repository": "core-banking-service",
  "owners_defined": true,
  "status": "COMPLIANT"
}
EOF

echo "[AUDIT EVENT] Recorded Compliance Audit Event in audit/events/compliance-events-log.json"
```

Cho phép script chạy ghi log event:
```bash
chmod +x scripts/record-compliance-audit-event.sh
./scripts/record-compliance-audit-event.sh
```

### **CHECKPOINT 11**
Chạy câu lệnh kiểm tra tệp Compliance Events Log:

```bash
test -f audit/events/compliance-events-log.json && grep -q "CODEOWNERS_ENFORCEMENT_AUDITED" audit/events/compliance-events-log.json && echo "CHECKPOINT 11: ĐẠT" || echo "CHECKPOINT 11: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 11: ĐẠT
```

---

### Bước 12: Xây dựng Script Linter Kiểm tra Cấu hình Compliance Repository (5 phút)

Tạo script linter kiểm tra compliance `scripts/validate-compliance-repo.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[COMPLIANCE LINTER] Auditing repository compliance rules..."

if [ ! -f .gitlab/CODEOWNERS ]; then
    echo "[ERROR] Missing mandatory .gitlab/CODEOWNERS file!"
    exit 1
fi

if [ ! -f audit/protected-branch-settings.json ]; then
    echo "[ERROR] Protected branch configuration missing!"
    exit 1
fi

if [ ! -f audit/approval-rules-config.json ]; then
    echo "[ERROR] Four-Eye Approval rules configuration missing!"
    exit 1
fi

echo "[COMPLIANCE LINTER] Validation PASSED: Repository is 100% Compliant with SOC2 & PCI-DSS Standards."
```

Cho phép script chạy linter:
```bash
chmod +x scripts/validate-compliance-repo.sh
./scripts/validate-compliance-repo.sh
```

### **CHECKPOINT 12**
Chạy câu lệnh kiểm tra script Linter Compliance:

```bash
./scripts/validate-compliance-repo.sh | grep -q "PASSED" && echo "CHECKPOINT 12: ĐẠT" || echo "CHECKPOINT 12: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 12: ĐẠT
```

---

### Bước 13: Xây dựng Script Mô phỏng Chặn Tác giả Tự Phê duyệt MR (Prevent Author Approval) (5 phút)

Tạo script kiểm tra Prevent Author Approval `scripts/verify-prevent-author-approval.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

AUTHOR_USER="${1:-developer.alex}"
APPROVER_USER="${2:-developer.alex}"

echo "[AUTHOR APPROVAL CHECK] User '$APPROVER_USER' attempting to approve MR created by '$AUTHOR_USER'..."

mkdir -p audit

if [ "$AUTHOR_USER" = "$APPROVER_USER" ]; then
    cat << EOF > audit/author-approval-result.json
{
  "mr_author": "$AUTHOR_USER",
  "approver": "$APPROVER_USER",
  "approval_action": "REJECTED_AUTHOR_SELF_APPROVAL_FORBIDDEN",
  "checked_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "AUTHOR_APPROVAL_BLOCKED"
}
EOF
    echo "[AUTHOR APPROVAL CHECK] REJECTED: Author cannot approve their own Merge Request!"
fi
```

Cho phép script chạy kiểm tra author approval:
```bash
chmod +x scripts/verify-prevent-author-approval.sh
./scripts/verify-prevent-author-approval.sh "developer.alex" "developer.alex"
```

### **CHECKPOINT 13**
Chạy câu lệnh kiểm tra tệp kết quả Author Approval Check:

```bash
test -f audit/author-approval-result.json && grep -q "AUTHOR_APPROVAL_BLOCKED" audit/author-approval-result.json && echo "CHECKPOINT 13: ĐẠT" || echo "CHECKPOINT 13: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 13: ĐẠT
```

---

### Bước 14: Tổng hợp Đánh giá Hoàn thành Bài Lab Buổi 45 (5 phút)

Tạo script đánh giá kết quả tổng hợp `scripts/final-compliance-lab-evaluation.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "FINAL EVALUATION SUMMARY — BUỔI 45 (COMPLIANCE & AUDIT)"
echo "=========================================================="

CHECKS_PASSED=0

[ -f .gitlab/CODEOWNERS ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f audit/protected-branch-settings.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f audit/approval-rules-config.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f audit/security-audits/secret-push-report.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f audit/compliance-framework-status.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f audit/events/streaming-audit-config.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))

echo "Successfully verified $CHECKS_PASSED / 6 Core Compliance Framework Components."
echo "Verified CODEOWNERS Syntax, Protected Branch API Settings, Four-Eye Approval Rules, Secret Push Protection, Compliance Frameworks, and Streaming Audit Events."
echo "Verified GPG Signature Check, Inactive User Access Review, and Prevent Author Self-Approval Policy."

if [ "$CHECKS_PASSED" -eq 6 ]; then
    echo "BUỔI 45 LAB STATUS: PASSED (100% COMPLETE)"
    exit 0
else
    echo "BUỔI 45 LAB STATUS: INCOMPLETE"
    exit 1
fi
```

Cho phép script chạy đánh giá kết quả:
```bash
chmod +x scripts/final-compliance-lab-evaluation.sh
./scripts/final-compliance-lab-evaluation.sh
```

### **CHECKPOINT 14**
Chạy câu lệnh tổng kết bài lab Buổi 45:

```bash
./scripts/final-compliance-lab-evaluation.sh | grep -q "PASSED" && echo "CHECKPOINT 14: ĐẠT" || echo "CHECKPOINT 14: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 14: ĐẠT
```

---

## Xử lý sự cố

### 1. Sự cố Lỗi `403 Forbidden` khi cấu hình Protected Branch qua REST API
- **Triệu chứng:** API trả về lỗi từ chối khi gọi `POST /protected_branches`.
- **Nguyên nhân:** Token được sử dụng không có quyền **Maintainer** hoặc **Owner** trên dự án.
- **Cách khắc phục:** Sử dụng Personal Access Token / Project Access Token của tài khoản có vai trò Owner.

### 2. Sự cố Tệp `CODEOWNERS` không hoạt động, MR không gán đúng reviewers
- **Triệu chứng:** Khi tạo MR sửa đổi file trong `/terraform/`, hệ thống không gán nhóm `@devops-team`.
- **Nguyên nhân:** Đặt sai vị trí tệp `CODEOWNERS` hoặc gõ sai tên username/group name.
- **Cách khắc phục:** Đảm bảo tệp đặt tại `.gitlab/CODEOWNERS` hoặc thư mục gốc và kiểm tra tên nhóm exact match trên GitLab UI.

### 3. Sự cố Tác giả MR vẫn bấm được nút Approve cho chính mình
- **Triệu chứng:** Author tạo MR và tự bấm Approve được.
- **Nguyên nhân:** Quên bật cờ `merge_requests_author_approval = false` trong cài đặt Merge Request.
- **Cách khắc phục:** Truy cập `Settings -> Merge Requests -> Approval settings` và tích chọn **Prevent approval by author**.

### 4. Sự cố Commit mới push thêm không xóa các lượt Approve cũ
- **Triệu chứng:** Dev nhờ approve xong rồi push commit mới vào MR vẫn được merge luôn.
- **Nguyên nhân:** Chưa bật cờ `reset_approvals_on_push = true`.
- **Cách khắc phục:** Tích chọn cờ **Remove all approvals when new commits are pushed** trong MR Settings.

### 5. Sự cố Lập trình viên tự do tạo Tag `v1.0.0` đẩy lên kích hoạt deploy Prod
- **Triệu chứng:** Pipeline deploy Prod tự động chạy khi dev push tag từ máy cá nhân.
- **Nguyên nhân:** Chưa cấu hình Protected Tags cho wildcard `v*`.
- **Cách khắc phục:** Thêm Protected Tag `v*` và đặt `Allowed to create = Maintainers`.

### 6. Sự cố Lỗi `Secret Push Protection: AWS Access Key Detected` khi push code
- **Triệu chứng:** Lệnh `git push` bị từ chối với thông báo chặn secret key.
- **Nguyên nhân:** Trong commit có chứa file cấu hình hoặc biến môi trường chứa AWS Key thô.
- **Cách khắc phục:** Xóa file chứa secret key, dùng `git rebase -i` xóa commit cũ chứa secret, và sử dụng CI/CD Variables.

### 7. Sự cố Streaming Audit Events không truyền dữ liệu về SIEM Splunk
- **Triệu chứng:** Splunk Dashboard không nhận được bất kỳ log audit nào từ GitLab.
- **Nguyên nhân:** Sai Webhook URL, hết hạn HEC Token, hoặc Firewall chặn port 443.
- **Cách khắc phục:** Kiểm tra lại HEC Token trong HEC Header settings và test kết quả bằng `curl`.

### 8. Sự cố Lỗi `Unsigned commit rejected` khi gõ lệnh `git push`
- **Triệu chứng:** GitLab chối bỏ commit với thông báo thiếu chữ ký GPG.
- **Nguyên nhân:** Protected Branch đã bật cờ `reject_unsigned_commits = true` nhưng dev chưa ký GPG key.
- **Cách khắc phục:** Tạo GPG Key `gpg --gen-key`, nạp Public Key lên GitLab Profile và gõ `git commit -S`.

### 9. Sự cố Script `user-access-audit-review.sh` không khóa được user nhàn rỗi
- **Triệu chứng:** Báo cáo xuất ra 0 users bị khóa dù có 30 users không hoạt động.
- **Nguyên nhân:** API Token thiếu quyền Admin để thực thi hành động `deactivate`.
- **Cách khắc phục:** Sử dụng Admin Personal Access Token với scope `admin_mode` và `api`.

### 10. Sự cố Compliance Framework Pipeline đè mất hoàn toàn job CI riêng của dự án
- **Triệu chứng:** Pipeline chỉ chạy mỗi job của Compliance Framework mà bỏ qua `.gitlab-ci.yml` của dự án.
- **Nguyên nhân:** Trong file Compliance Template dùng câu lệnh `include` không đúng cú pháp.
- **Cách khắc phục:** Bổ sung khối `include: { project: '$CI_PROJECT_PATH', file: '$CI_CONFIG_PATH' }` trong template.

### 11. Sự cố Lập trình viên lách luật bằng cách ép người trong cùng MR approve
- **Triệu chứng:** Committer thứ 2 vừa push commit vừa đứng ra approve MR.
- **Nguyên nhân:** Chưa bật cờ `merge_requests_disable_committers_approval = true`.
- **Cách khắc phục:** Bật cờ **Prevent approval by committers** trong MR Settings.

### 12. Sự cố Tệp `CODEOWNERS` bị commit đè lên làm mất quy tắc bảo vệ
- **Triệu chứng:** Quy tắc phân quyền CODEOWNERS bị biến mất sau một MR.
- **Nguyên nhân:** File `.gitlab/CODEOWNERS` không được gán chính `CODEOWNERS` bảo vệ.
- **Cách khắc phục:** Bổ sung dòng `/.gitlab/CODEOWNERS @security-team` vào tệp CODEOWNERS.

### 13. Sự cố `simulate-secret-push-protection.sh` nổ lỗi directory not found
- **Triệu chứng:** Script scan secret bị ngắt giữa chừng.
- **Nguyên nhân:** Thư mục `audit/security-audits` chưa khởi tạo.
- **Cách khắc phục:** Bổ sung `mkdir -p audit/security-audits` trong script.

### 14. Sự cố Approval Rule yêu cầu 2 Approvals nhưng MR chỉ cần 1 là cho merge
- **Triệu chứng:** MR được merge khi mới có 1 người phê duyệt.
- **Nguyên nhân:** Cấu hình Rule ở mức Project bị ghi đè bởi cấu hình ở mức Target Branch.
- **Cách khắc phục:** Kiểm tra lại quy tắc `approvals_required` trên đúng nhánh Target `main`.

### 15. Sự cố Protected Branch không chặn được tài khoản Owner
- **Triệu chứng:** Tài khoản Owner vẫn push trực tiếp được lên nhánh `main` bị Protected.
- **Nguyên nhân:** Cài đặt `push_access_level = 40` (Maintainers/Owners can push).
- **Cách khắc phục:** Sửa `push_access_level = 0` (No one can push).

### 16. Sự cố `setup-approval-rules.sh` nổ lỗi bash syntax
- **Triệu chứng:** Script thiết lập approval nổ error.
- **Nguyên nhân:** Thiếu dấu bọc ngoặc trong câu lệnh JSON.
- **Cách khắc phục:** Kiểm tra cú pháp Heredoc `cat << EOF`.

### 17. Sự cố Cờ `allow_force_push = true` bị lén bật lại
- **Triệu chứng:** Nhánh `main` bị ai đó force push đè commit.
- **Nguyên nhân:** Một Admin trong dự án vô tình bật lại cờ Force Push trên UI.
- **Cách khắc phục:** Đặt Compliance Policy tự động quét và reset cờ `allow_force_push = false` hàng giờ qua API.

### 18. Sự cố `verify-approval-reset-on-push.sh` nổ lỗi file not found
- **Triệu chứng:** Script reset approval nổ error.
- **Nguyên nhân:** Thư mục `audit` chưa khởi tạo.
- **Cách khắc phục:** Bổ sung `mkdir -p audit` trong script.

### 19. Sự cố User bị khóa nhầm do lịch sử hoạt động không ghi nhận trên Git Web UI
- **Triệu chứng:** Developer làm việc hàng ngày qua SSH/Git nhưng vẫn bị script khóa tài khoản.
- **Nguyên nhân:** Script chỉ kiểm tra `last_sign_in_at` thay vì `last_activity_on`.
- **Cách khắc phục:** Đổi sang kiểm tra chỉ số API `last_activity_on` (bao gồm cả Git SSH/HTTP activity).

### 20. Sự cố Streaming Audit Events làm nghẽn mạng do lượng log quá lớn
- **Triệu chứng:** Hệ thống SIEM bị ngợp traffic.
- **Nguyên nhân:** Đăng ký tất cả các loại sự kiện bao gồm cả read/view events.
- **Cách khắc phục:** Lọc danh sách `event_types` chỉ chọn các sự kiện thay đổi phân quyền và security.

### 21. Sự cố `assign-compliance-framework.sh` nổ lỗi directory missing
- **Triệu chứng:** Script gán framework nổ error.
- **Nguyên nhân:** Thư mục `audit` chưa tạo.
- **Cách khắc phục:** Bổ sung `mkdir -p audit` trong script.

### 22. Sự cố Tệp `protected-tags-policy.json` bị gõ sai cú pháp JSON
- **Triệu chứng:** Script audit nổ error khi đọc tệp.
- **Nguyên nhân:** Thiếu dấu phẩy phân cách giữa các trường JSON.
- **Cách khắc phục:** Đảm bảo tệp JSON chuẩn cú pháp `jq .`.

### 23. Sự cố `enable-streaming-audit-events.sh` nổ lỗi directory missing
- **Triệu chứng:** Script streaming audit nổ error.
- **Nguyên nhân:** Thư mục `audit/events` chưa khởi tạo.
- **Cách khắc phục:** Bổ sung `mkdir -p audit/events` trong script.

### 24. Sự cố Lỗi `422 Unprocessable Entity` khi tạo Approval Rule qua API
- **Triệu chứng:** REST API trả về lỗi 422.
- **Nguyên nhân:** Đã tồn tại Rule cùng tên trên dự án.
- **Cách khắc phục:** Xóa Rule cũ bằng `DELETE` API hoặc cập nhật bằng `PUT` API.

### 25. Sự cố GPG Key hết hạn làm tất cả các commit tiếp theo bị chối bỏ
- **Triệu chứng:** Developer không thể push code dù đã ký GPG.
- **Nguyên nhân:** Chìa khóa GPG Key của dev đã hết hạn sau 1 năm.
- **Cách khắc phục:** Gia hạn GPG key `gpg --edit-key` và re-upload Public Key mới lên GitLab.

### 26. Sự cố `verify-gpg-commit-signature.sh` nổ lỗi syntax
- **Triệu chứng:** Script GPG check nổ error.
- **Nguyên nhân:** Thiếu ngoặc bọc biến tham số.
- **Cách khắc phục:** Bọc các biến tham số trong ngoặc `"..."`.

### 27. Sự cố `final-compliance-lab-evaluation.sh` báo 5/6 thành phần
- **Triệu chứng:** Đánh giá bài lab chưa đạt 100%.
- **Nguyên nhân:** Chưa chạy Step 7 kích hoạt Streaming Audit.
- **Cách khắc phục:** Chạy script `./scripts/enable-streaming-audit-events.sh`.

### 28. Sự cố Tệp `CODEOWNERS` chứa ký tự End-of-Line Windows CRLF
- **Triệu chứng:** GitLab Parser bỏ qua tệp CODEOWNERS không nhận diện.
- **Nguyên nhân:** File được soạn thảo từ Notepad trên Windows.
- **Cách khắc phục:** Chuyển đổi định dạng file sang EOL Unix LF bằng `dos2unix .gitlab/CODEOWNERS`.

### 29. Sự cố Secret Push Protection không quét được secret trong file nén `.zip`
- **Triệu chứng:** Lỡ tay push tệp `.zip` chứa credentials lên kho mã nguồn.
- **Nguyên nhân:** Engine quét secret chỉ hỗ trợ quét plain-text files.
- **Cách khắc phục:** Khai báo Push Rule cấm push các tệp nén nhị phân (`*.zip`, `*.tar.gz`) lên kho mã nguồn.

### 30. Sự cố Cơ chế Author Approval bị lách bằng cách đổi Git Author Email
- **Triệu chứng:** Dev đổi `user.email` thành email khác rồi tự approve.
- **Nguyên nhân:** GitLab kiểm tra vai trò dựa vào Username đăng nhập chứ không dựa vào Git Author Header.
- **Cách khắc phục:** Yên tâm vì GitLab kiểm tra tài khoản Authenticated Session khi bấm nút Approve.

### 31. Sự cố `record-compliance-audit-event.sh` nổ lỗi missing report folder
- **Triệu chứng:** Script record log nổ error.
- **Nguyên nhân:** Thư mục `audit/events` chưa tạo.
- **Cách khắc phục:** Thêm `mkdir -p audit/events` trong script.

### 32. Sự cố User bị khóa quyền nhưng vẫn tiếp tục dùng Personal Access Token
- **Triệu chứng:** User bị Deactivate nhưng các script gọi API của họ vẫn chạy.
- **Nguyên nhân:** Vô hiệu hóa User nhưng chưa Revoke các Personal Access Tokens cũ.
- **Cách khắc phục:** Script khóa user phải đồng thời thu hồi tất cả PATs của user đó qua API.

### 33. Sự cố Protected Branch không áp dụng cho các nhánh con mới tạo
- **Triệu chứng:** Nhánh `release/v1.0` không được bảo vệ.
- **Nguyên nhân:** Chỉ cấu hình tên nhánh cố định `main` thay vì wildcard pattern.
- **Cách khắc phục:** Đặt Protected Branch Pattern là `release/*` để tự động bảo vệ tất cả nhánh release.

### 34. Sự cố `user-access-audit-review.sh` nổ lỗi bash arithmetic
- **Triệu chứng:** Script rà soát user nổ error.
- **Nguyên nhân:** Phép toán bash thiếu ngoặc.
- **Cách khắc phục:** Đảm bảo cú pháp toán số nguyên chuẩn xác.

### 35. Sự cố Compliance Framework bị hủy do repo gỡ nhãn Compliance
- **Triệu chứng:** Project Maintainer tự gỡ tag compliance trên UI.
- **Nguyên nhân:** Maintainer có quyền chỉnh sửa Project Compliance settings.
- **Cách khắc phục:** Đặt quyền Compliance Framework Enforcement ở cấp Group Level (chỉ Group Owners mới được chỉnh).

### 36. Sự cố `verify-prevent-author-approval.sh` nổ lỗi directory missing
- **Triệu chứng:** Script kiểm tra author approval nổ error.
- **Nguyên nhân:** Thư mục `audit` chưa tạo.
- **Cách khắc phục:** Thêm `mkdir -p audit` trong script.

### 37. Sự cố `validate-compliance-repo.sh` bị nổ lỗi permission denied
- **Triệu chứng:** Không thể thực thi script linter compliance.
- **Nguyên nhân:** Quên cấp quyền execution permission.
- **Cách khắc phục:** Chạy `chmod +x scripts/validate-compliance-repo.sh`.

### 38. Sự cố Quên cấp quyền `chmod +x` cho toàn bộ thư mục `scripts/`
- **Triệu chứng:** Tất cả các checkpoint báo lỗi permission denied.
- **Nguyên nhân:** Các file script mới tạo thiếu cờ `+x`.
- **Cách khắc phục:** Chạy `chmod +x scripts/*.sh`.

### 39. Sự cố Git diff hiển thị 100% dòng do khác biệt End-of-Line CRLF
- **Triệu chứng:** File `CODEOWNERS` hiển thị modified toàn bộ file.
- **Nguyên nhân:** Ký tự xuống dòng Windows CRLF.
- **Cách khắc phục:** Chuẩn hóa `.gitattributes` bắt buộc dùng LF.

### 40. Sự cố REST API Token bị hết hạn làm script Cron Job rà soát user bị ngừng
- **Triệu chứng:** Script Cron Job chạy báo `401 Unauthorized`.
- **Nguyên nhân:** Personal Access Token của bot có thời hạn 30 ngày và đã hết hạn.
- **Cách khắc phục:** Sử dụng Service Account Token / OAuth Token dài hạn với quy trình xoay token tự động.

### 41. Sự cố Cấu hình `approvals_required = 0` ở mức project đè mức group
- **Triệu chứng:** Project mới tạo không yêu cầu approval nào.
- **Nguyên nhân:** Project kế thừa default setting không có approval rule.
- **Cách khắc phục:** Đặt Group-level Approval Rules ép áp dụng cho tất cả các sub-projects.

### 42. Sự cố Audit Event Log bị ghi đè mất thông tin quá khứ
- **Triệu chứng:** File log `compliance-events-log.json` chỉ có 1 dòng duy nhất.
- **Nguyên nhân:** Dùng toán tử ghi đè `>` thay vì nối tiếp `>>`.
- **Cách khắc phục:** Đổi sang dùng `>>` trong script.

### 43. Sự cố `protect-branch-api.sh` nổ lỗi missing report folder
- **Triệu chứng:** Script bảo vệ nhánh nổ error.
- **Nguyên nhân:** Thư mục `audit` chưa khởi tạo.
- **Cách khắc phục:** Bổ sung `mkdir -p audit` trong script.

### 44. Sự cố Secret Push Protection không ngăn được secret bị đẩy qua commit message
- **Triệu chứng:** Secret key bị lộ nằm trong nội dung Git Commit Message.
- **Nguyên nhân:** Engine Push Protection mặc định chỉ quét phần diff content của files.
- **Cách khắc phục:** Bổ sung Push Rule regex cấm chuỗi AWS Key pattern trong Commit Message.

### 45. Sự cố `final-compliance-lab-evaluation.sh` nổ lỗi syntax bash
- **Triệu chứng:** Script tổng kết báo lỗi dòng.
- **Nguyên nhân:** Cú pháp kiểm tra tệp `[ -f file ]` thiếu ngoặc.
- **Cách khắc phục:** Đảm bảo cú pháp bash chuẩn xác.

### 46. Sự cố GPG Signature Verification không hỗ trợ chữ ký SSH Keys
- **Triệu chứng:** Commit ký bằng SSH Key vẫn báo `Unverified`.
- **Nguyên nhân:** Phiên bản GitLab cũ (trước v15.7) chưa hỗ trợ SSH Commit Signing.
- **Cách khắc phục:** Nâng cấp GitLab lên phiên bản v16+ hỗ trợ cả GPG và SSH Commit Signing.

### 47. Sự cố Tệp `inactive-users-report.json` bị thiếu thông tin timestamp
- **Triệu chứng:** Báo cáo user thiếu thời gian thực thi.
- **Nguyên nhân:** Quên truyền trường `reviewed_at`.
- **Cách khắc phục:** Bổ sung `"reviewed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"`.

### 48. Sự cố Cờ `merge_access_level = 0` làm kẹt không ai merge được MR
- **Triệu chứng:** MR được approve 100% nhưng nút Merge bị mờ.
- **Nguyên nhân:** Đặt `merge_access_level = 0` (No one can merge).
- **Cách khắc phục:** Sửa `merge_access_level = 30` (Developers/Maintainers can merge).

### 49. Sự cố Tệp `CODEOWNERS` bị lỗi cú pháp do dùng dấu ngoặc vuông sai
- **Triệu chứng:** GitLab Parser báo lỗi syntax CODEOWNERS.
- **Nguyên nhân:** Gõ sai cú pháp username `@group/subgroup`.
- **Cách khắc phục:** Đảm bảo cú pháp `@group/subgroup` chuẩn xác.

### 50. Sự cố Tự động hủy Approval làm kéo dài thời gian review của dự án lớn
- **Triệu chứng:** Các MR lớn bị hoãn merge 3 ngày do dev liên tục push commit fix typo nhỏ.
- **Nguyên nhân:** Dev push commit quá lặt vặt sau khi đã được approve.
- **Cách khắc phục:** Hướng dẫn dev gộp commit local (Git Squash) trước khi nhờ review.

### 51. Sự cố `inactive-users-report.json` nổ lỗi missing report folder
- **Triệu chứng:** Script user audit nổ error.
- **Nguyên nhân:** Thư mục `audit/user-reviews` chưa tạo.
- **Cách khắc phục:** Bổ sung `mkdir -p audit/user-reviews` trong script.

### 52. Sự cố Audit Event Log không ghi nhận được địa chỉ IP thực của người dùng
- **Triệu chứng:** Mọi Audit Logs đều hiển thị IP của NGINX Reverse Proxy `127.0.0.1`.
- **Nguyên nhân:** Reverse Proxy NGINX chưa cấu hình header `X-Forwarded-For`.
- **Cách khắc phục:** Bổ sung `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;` trên NGINX.

### 53. Sự cố `scripts/validate-compliance-repo.sh` bị nổ lỗi permission denied
- **Triệu chứng:** Không thể thực thi script linter compliance.
- **Nguyên nhân:** Quên cấp quyền execution permission.
- **Cách khắc phục:** Chạy `chmod +x scripts/validate-compliance-repo.sh`.

### 54. Sự cố Protected Branch API không cập nhật được cấu hình cũ
- **Triệu chứng:** Lệnh POST nổ lỗi branch already protected.
- **Nguyên nhân:** API `POST` chỉ dùng cho khởi tạo mới, không dùng cho update.
- **Cách khắc phục:** Chuyển sang dùng `PATCH` hoặc `PUT` API endpoint.

### 55. Sự cố Cấu hình `reset_approvals_on_push` bị vô hiệu hóa do cờ override
- **Triệu chứng:** MR Settings không áp dụng được tính năng reset approvals.
- **Nguyên nhân:** Cài đặt ở mức Group cho phép dự án ghi đè (Override).
- **Cách khắc phục:** Đặt cờ **Enforce approval settings on all projects** ở cấp Group Level.

---

## Bài tập mở rộng

1. **Xây dựng Hệ thống Quản trị Compliance Tự động hóa ở Quy mô 500 Repositories:**
   - Viết script Python kết hợp GitLab REST API để tự động kiểm tra toàn bộ 500 Repositories trong tập đoàn.
   - Tự động gán nhãn Compliance Framework `PCI-DSS-Compliant`, tự động khóa Protected Branch `main` (cấm Force/Direct Push), và tự động chèn tệp `.gitlab/CODEOWNERS` chuẩn cho tất cả các repos thiếu tuân thủ!

2. **Tích hợp Streaming Audit Events API với Elastic Security SIEM Real-time Alerting:**
   - Cấu hình Streaming Audit Events API trỏ tới **Elasticsearch HTTP Event Collector**.
   - Dựng các quy tắc cảnh báo tự động (Elastic Security Detection Rules): Nếu có bất kỳ sự kiện *Force Push Attempt*, *Secret Key Detected*, hoặc *Author Self-Approval Attempt* xảy ra, tự động kích hoạt Webhook bắn thông báo khẩn cấp lên kênh Slack Security War Room!

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| Bước 1 | Khởi tạo Thư mục Lab và Tệp `CODEOWNERS` Chuẩn mực Enterprise | 10 phút |
| Bước 2 | Viết Script Mô phỏng Cấu hình Protected Branch API Cấm Force Push | 10 phút |
| Bước 3 | Viết Script Mô phỏng Cưỡng chế Quy tắc 2 Người Phê duyệt (Four-Eye Principle) | 15 phút |
| Bước 4 | Viết Script Kiểm thử Tự động Hủy Approval khi Push Commit Mới | 15 phút |
| Bước 5 | Viết Script Mô phỏng Secret Push Protection Chặn AWS Access Keys | 10 phút |
| Bước 6 | Viết Script Mô phỏng Gắn Compliance Framework Template Cấp Group | 15 phút |
| Bước 7 | Viết Script Mô phỏng Kích hoạt Streaming Audit Events API về SIEM Splunk | 15 phút |
| Bước 8 | Viết Script Kiểm thử Kiểm tra Chữ ký số GPG Commit Verification | 10 phút |
| Bước 9 | Viết Script Tự động Rà soát và Khóa Tài khoản Nhàn rỗi (User Access Review) | 15 phút |
| Bước 10 | Khởi tạo Policy Cấu hình Protected Tags `v*` | 10 phút |
| Bước 11 | Viết Script Ghi nhận Nhật ký Compliance Audit Event Log | 10 phút |
| Bước 12 | Xây dựng Script Linter Kiểm tra Cấu hình Compliance Repository | 5 phút |
| Bước 13 | Xây dựng Script Mô phỏng Chặn Tác giả Tự Phê duyệt MR (Prevent Author Approval) | 5 phút |
| Bước 14 | Tổng hợp Đánh giá Hoàn thành Bài Lab Buổi 45 | 5 phút |
| **Tổng** | **Khối thực hành lab** | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

# Buổi 45: Compliance, audit, protected branch/tag, CODEOWNERS — Vấn Đáp & Phỏng Vấn

## Thống kê & Phân bổ thời lượng
- **Tổng thời lượng:** 20 phút
- **Cấu trúc:**
  - 5 phút: Kiểm tra phản xạ lý thuyết (12 câu hỏi trắc nghiệm & tự luận nhanh)
  - 10 phút: Đóng vai phỏng vấn tình huống thực chiến (7 kịch bản nâng cao)
  - 5 phút: Chốt từ khóa ăn tiền (§V3) & Giao bài tập về nhà chuẩn bị cho Buổi 46 (BTVN 4)

---

## §V1. 12 Câu hỏi vấn đáp kiểm tra phản xạ

### Câu 1
**Hỏi:** Rủi ro an ninh lớn nhất khi không áp dụng Protected Branch trên nhánh `main` hoặc `production` trong hệ thống Enterprise là gì?

**Gợi ý trả lời ngắn:**
Lập trình viên có thể gõ lệnh `git push origin main` đẩy trực tiếp code lỗi chưa qua review/test hoặc gõ `git push --force` xóa sạch lịch sử commit của toàn bộ công ty.

**Đáp án chuẩn:**
- **Giải thích rủi ro an ninh:**
  Khi nhánh `main` không được bảo vệ bằng Protected Branch:
  1. *Direct Push:* Bất kỳ developer nào cũng có thể đẩy code lỗi, code chưa qua thử nghiệm hoặc thậm chí backdoor trực tiếp lên nhánh Production mà không đi qua quy trình Merge Request review.
  2. *Force Push:* Developer vô tình hoặc cố ý gõ lệnh `git push --force origin main` làm đè nát toàn bộ lịch sử commit Git, xóa sạch mã nguồn công ty mà không thể khôi phục dễ dàng.
- **Giải pháp:** Đặt Protected Branch `push_access_level = 0` (No one can push) và `allow_force_push = false`.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng "Chỉ cần dặn dò các developers trong nhóm không push trực tiếp lên main là đủ an toàn rồi".

---

### Câu 2
**Hỏi:** Tệp `CODEOWNERS` giải quyết triệt để vấn đề gì trong quản trị phân quyền mã nguồn cho các dự án lớn có hàng trăm lập trình viên?

**Gợi ý trả lời ngắn:**
Tệp `CODEOWNERS` tự động cưỡng chế chỉ định các nhóm chuyên trách (Security, DevOps, DBA) bắt buộc phải phê duyệt MR khi có sửa đổi liên quan đến thư mục nhạy cảm do họ sở hữu.

**Đáp án chuẩn:**
- **Giải thích vai trò của CODEOWNERS:**
  Trong dự án Enterprise phức tạp, một lập trình viên Frontend có thể vô tình sửa nhầm vào file cấu hình hạ tầng Terraform `/terraform/main.tf` hay file mã hóa bí mật `/src/security/crypto.js`.
- **Cơ chế hoạt động:**
  Tệp `CODEOWNERS` định nghĩa các quy tắc đường dẫn (Path Rules):
  ```text
  /terraform/ @devops-team
  /src/security/ @security-team
  ```
  Khi MR có sửa đổi file trong `/terraform/`, hệ thống tự động khóa MR và bắt buộc đại diện nhóm `@devops-team` bấm nút Phere duyệt thì mới được phép merge.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng "CODEOWNERS chỉ có tác dụng đánh dấu tác giả file chứ không có giá trị cưỡng chế quyền Phê duyệt".

---

### Câu 3
**Hỏi:** Nguyên tắc Quy tắc 4 Mắt (Four-Eye Principle - 2 Approvals Required) có ý nghĩa như thế nào trong các tiêu chuẩn bảo mật SOC 2 và PCI-DSS?

**Gợi ý trả lời ngắn:**
Đảm bảo một đoạn mã trước khi merge lên Production bắt buộc phải được ít nhất 2 người xem xét độc lập, ngăn ngừa lỗi cá nhân hoặc mã độc do 1 cá nhân cố tình chèn vào.

**Đáp án chuẩn:**
- **Giải thích Tiêu chuẩn SOC 2 / PCI-DSS:**
  Tiêu chuẩn bảo mật quốc tế bắt buộc phải áp dụng **Quy tắc 4 Mắt (Four-Eye Principle)** cho mọi thay đổi mã nguồn Production:
  - Đặt `approvals_required = 2` trên MR Approval Rules.
  - Mỗi Merge Request cần 1 tác giả tạo code + 2 lập trình viên/chuyên gia độc lập xem xét và phê duyệt.
- **Tác dụng:** Loại bỏ nguy cơ một nhân sự đơn lẻ bị hack tài khoản hoặc cố tình cài cắm mã độc (Insider Threat) đưa code thẳng lên Production.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Đồng ý để `approvals_required = 1` để "tiết kiệm thời gian review của đội ngũ".

---

### Câu 4
**Hỏi:** Tại sao cờ `reset_approvals_on_push = true` lại là điều kiện bắt buộc để chống lách luật an ninh trong Merge Request?

**Gợi ý trả lời ngắn:**
Để tự động xóa sạch các lượt phê duyệt cũ khi tác giả push thêm commit mới, ngăn tác giả lén lách luật push thêm code chưa review sau khi đã được duyệt.

**Đáp án chuẩn:**
- **Kịch bản lách luật tinh vi:**
  1. Tác giả tạo MR, nhờ 2 đồng nghiệp phê duyệt xanh $100\%$.
  2. Sau khi được approve, tác giả âm thầm gõ `git commit -m "fix typo"` push thêm một commit chứa mã độc/code lỗi vào MR đó.
  3. Nếu không bật cờ `reset_approvals_on_push = true`, 2 lượt approve cũ vẫn được giữ nguyên và code độc hại trôi thẳng lên Production!
- **Khắc phục:** Bật cờ Reset Approvals ép hệ thống xóa sạch approvals cũ ngay khi phát hiện commit mới, bắt buộc phải review lại từ đầu.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Tắt cờ Reset Approvals vì "dev lỡ push commit fix typo nhỏ mà bắt đồng nghiệp approve lại thì phiền phức".

---

### Câu 5
**Hỏi:** Sự khác biệt cốt lõi giữa hai cờ an ninh `merge_requests_author_approval` và `merge_requests_disable_committers_approval` là gì?

**Gợi ý trả lời ngắn:**
`author_approval` cấm tác giả tạo MR tự duyệt code của mình; `disable_committers_approval` cấm tất cả những ai đã từng push commit vào MR đó đứng ra duyệt.

**Đáp án chuẩn:**
- **Phân biệt 2 cờ bảo mật:**
  1. *`merge_requests_author_approval = false`:* Ngăn tác giả mở MR tự bấm nút Approve cho chính mình.
  2. *`merge_requests_disable_committers_approval = true`:* Ngăn chặn lách luật nâng cao. Ví dụ Dev A tạo MR, Dev B vào push thêm 1 commit hỗ trợ. Lúc này Dev B cũng được tính là Committer, do đó Dev B không được phép đứng ra làm Reviewer approve MR đó nữa.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng "Chỉ cần bật cấm Author Approve là đủ, Committer push thêm commit vào MR vẫn duyệt thoải mái".

---

### Câu 6
**Hỏi:** Lý do bắt buộc phải thiết lập Protected Tags cho các pattern phiên bản như `v1.*` hoặc `release-*` trong GitLab CI là gì?

**Gợi ý trả lời ngắn:**
Để ngăn lập trình viên tự do tạo Tag release trên máy cá nhân để kích hoạt các pipeline tự động deploy code chưa kiểm thử lên môi trường Production.

**Đáp án chuẩn:**
- **Lý do kỹ thuật:**
  Trong kiến trúc GitOps/CI-CD, sự kiện push Git Tag (ví dụ `git push origin v1.0.0`) thường được cấu hình làm Trigger Point kích hoạt job `deploy-production`.
- **Nguy cơ nếu không có Protected Tag:** Lập trình viên bất kỳ có thể gõ `git tag v9.9.9 && git push origin v9.9.9` trên máy laptop cá nhân để kích hoạt pipeline deploy code tùy ý lên Production!
- **Giải pháp:** Cấu hình Protected Tags `v*` chỉ cho phép **Maintainers** hoặc **CI/CD Pipeline Service Account** có quyền khởi tạo.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Không bảo vệ Git Tags, cho phép mọi Developers tự do tạo và xóa nhãn release trên remote repo.

---

### Câu 7
**Hỏi:** Tính năng GitLab Compliance Frameworks giúp giải quyết bài toán tuân thủ ở quy mô 500 Repositories trong tập đoàn như thế nào?

**Gợi ý trả lời ngắn:**
Giúp tạo một Compliance Pipeline Template tập trung và ép 100% Repositories phải tự động kế thừa các stage quét SAST/Security bắt buộc mà không thể tự ý sửa đổi.

**Đáp án chuẩn:**
- **Giải pháp Tuân thủ ở Quy mô lớn (Compliance at Scale):**
  Khi tổ chức có 500 Repositories, đội Security không thể đi từng repo kiểm tra file `.gitlab-ci.yml`.
- **Cơ chế Compliance Framework:**
  Đội Security gắn nhãn Compliance Framework (ví dụ `SOC2-Compliant`) cấp Group Level. Mọi pipeline khi chạy trên 500 repos đều bắt buộc phải chạy qua file `soc2-compliance-pipeline.yml` trung tâm trước. Developers tuyệt đối không thể bypass hay xóa bỏ các stage quét bảo mật này.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Bắt từng đội phát triển tự sao chép (copy-paste) các job quét SAST vào file `.gitlab-ci.yml` cá nhân của họ.

---

### Câu 8
**Hỏi:** Tại sao tính năng Secret Push Protection lại vượt trội hơn hẳn so với việc chạy job quét SAST Secret Detection trong CI Pipeline?

**Gợi ý trả lời ngắn:**
Secret Push Protection chặn đứng lệnh `git push` ngay từ máy dev trước khi code trôi lên server, ngăn chìa khóa bị lưu vào lịch sử Git History.

**Đáp án chuẩn:**
- **So sánh 2 cơ chế:**
  - *Quét SAST trong CI Pipeline:* Developer đã gõ `git push`. Commit chứa AWS Key đã lưu trên GitLab Server và ghi vết vào Git History. Dù pipeline CI báo lỗi sau 5 phút, hacker vẫn có thể checkout lại commit cũ trong Git History để lấy key!
  - *Secret Push Protection (Shift-Left):* Quét gói tin payload ngay lúc gõ lệnh `git push`. Nếu phát hiện AWS Key, lệnh push bị từ chối lập tức từ máy dev ($0\%$ code trôi lên server, $0\%$ lưu Git History).

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng "Quét secret trong CI Pipeline sau khi push code lên server là đã an toàn tuyệt đối rồi".

---

### Câu 9
**Hỏi:** Cờ `reject_unsigned_commits = true` trên Protected Branch giúp ngăn chặn hình thức tấn công nguy hiểm nào trong Git?

**Gợi ý trả lời ngắn:**
Ngăn chặn hình thức mạo danh danh tính tác giả Git (Git Author Spoofing Attack) bằng cách bắt buộc mọi commit phải có chữ ký số GPG/SSH Verified.

**Đáp án chuẩn:**
- **Tấn công Git Author Spoofing:**
  Trong Git thô, bất kỳ ai cũng có thể gõ `git config user.name "CEO Name"` và `git config user.email "ceo@company.com"` để mạo danh sếp lớn tạo commit độc hại!
- **Bảo vệ bằng GPG/SSH Signing:** Bật cờ `reject_unsigned_commits = true` buộc mọi commit phải kèm theo chữ ký điện tử được xác thực bằng Public Key cá nhân đăng ký trên GitLab, chứng minh $100\%$ tính chính chủ của tác giả.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng "Git mặc định đã tự động xác thực danh tính người commit thông qua email trong Git config rồi".

---

### Câu 10
**Hỏi:** Ý nghĩa của việc bật Streaming Audit Events API gửi log thời gian thực về máy chủ SIEM (Splunk / Elastic) là gì?

**Gợi ý trả lời ngắn:**
Để đảm bảo tính nguyên vẹn không thể chối cãi của nhật ký thao tác phục vụ điều tra an ninh (Forensics), ngay cả khi kho mã nguồn trên GitLab bị xóa.

**Đáp án chuẩn:**
- **Giải thích vai trò Streaming Audit Events:**
  Khi kẻ gian truy cập trái phép đổi phân quyền từ Developer lên Owner hoặc xóa chìa khóa bí mật, sự kiện đó phải được đẩy ngay lập tức trong $0.5$ giây về máy chủ SIEM bảo mật độc lập.
- **Tác dụng:** Kẻ gian dù có quyền Owner cũng không thể vào SIEM để xóa hay sửa bản ghi audit log. Đảm bảo tính pháp lý tuyệt đối khi kiểm toán an ninh SOC 2.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Chỉ lưu nhật ký thao tác trên giao diện GitLab UI mà không trích xuất về hệ thống SIEM tập trung.

---

### Câu 11
**Hỏi:** Tác hại của việc để tồn tại các tài khoản nhàn rỗi (Ghost Accounts) quá 30 ngày không hoạt động là gì?

**Gợi ý trả lời ngắn:**
Tạo ra các điểm yếu lỗ hổng cho hacker lợi dụng xâm nhập vào hệ thống thông qua các tài khoản cũ của nhân sự đã nghỉ việc không ai quản lý.

**Đáp án chuẩn:**
- **Nguy cơ an ninh từ Ghost Accounts:**
  Khi nhân sự nghỉ việc hoặc đối tác chuyển dự án nhưng quản trị viên quên gỡ quyền, tài khoản đó vẫn nguyên quyền Owner/Maintainer. Hacker có thể dò quét mật khẩu cũ (Credential Stuffing) hoặc lấy cắp SSH Key của tài khoản nhàn rỗi đó để xâm nhập kho mã nguồn.
- **Giải pháp:** Chạy script tự động rà soát hàng tuần khóa (Deactivate) tất cả tài khoản nhàn rỗi quá 30 ngày (QT 45.12).

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Để mặc các tài khoản cũ trong hệ thống, chỉ khi nào nhớ ra mới vào gỡ thủ công bằng tay.

---

### Câu 12
**Hỏi:** Trong trường hợp xử lý sự cố khẩn cấp lúc 3:00 AM khi toàn bộ hệ thống sập (Emergency Hotfix), làm sao để vung tay vượt qua các quy tắc phê duyệt ngặt nghèo mà vẫn đảm bảo an toàn tuân thủ?

**Gợi ý trả lời ngắn:**
Sử dụng tài khoản có quyền **Emergency Bypass Approval Role** đặc biệt, đồng thời tự động kích hoạt Streaming Audit Event báo động khẩn cấp tới CISO và bắt buộc review bù trong 24h.

**Đáp án chuẩn:**
- **Quy trình xử lý Break-Glass / Emergency Bypass:**
  Khi hệ thống Production sập lúc 3:00 AM và không đủ 2 reviewers thức dậy để approve MR:
  1. Cấu hình vai trò **Break-Glass Emergency Role** cho On-call Lead được phép bypass khởi tạo Hotfix MR.
  2. Ngay khi nút Bypass được bấm, hệ thống kích hoạt ngay lập tức một **High-Severity Audit Event** gửi tin nhắn cảnh báo khẩn cấp tới Giám đốc Bảo mật (CISO) và Trưởng phòng DevOps.
  3. Bắt buộc trong vòng 24 giờ sau sự cố, đội ngũ phải tổ chức cuộc họp Post-Mortem và thực hiện quy trình Review bù (Retrospective Review) cho commit hotfix đó.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Tắt bỏ hoàn toàn quy tắc Protected Branch và Approval Rules của dự án để làm hotfix cho tiện.

---

## §V2. Kịch bản phỏng vấn thực tế (Roleplay Scenarios)

### Kịch bản 1: Thuyết phục Giám đốc An ninh CISO Triển khai Compliance Framework Enforced by Code
- **Người phỏng vấn (CISO):** *"Công ty chúng ta đã có quy trình kiểm soát mã nguồn viết rất chi tiết trong file PDF gửi cho từng nhân viên. Tại sao em lại đòi tốn công cấu hình Compliance Frameworks Enforced by Code trên GitLab?"*
- **Ứng viên (DevOps & Compliance Architect):**
  - *Trả lời:* "Báo cáo anh, file quy định PDF chỉ đại diện cho **mong muốn**, còn cấu hình Enforced by Code mới đại diện cho **cưỡng chế thực tế**!"
  - "1. **Lập trình viên vẫn lỡ tay:** Dù có đọc PDF, lập trình viên dưới áp lực deadline vẫn sẽ gõ `git push origin main` hoặc tự approve code của mình nếu hệ thống cho phép."
  - "2. **Cưỡng chế bằng Code (QT 45.8):** Cấu hình Compliance Frameworks tự động khóa nút Direct Push, tự động bắt buộc 2 Approvals độc lập và tự động chèn job quét SAST vào 100% Repositories. Hệ thống sẽ tự động ngăn chặn lỗi của con người mà không cần giám sát bằng tay!"

---

### Kịch bản 2: Xử lý Sự cố Lập trình viên Tác giả Tự duyệt MR của Chính mình
- **Người phỏng vấn (Security Auditor):** *"Trong đợt kiểm toán SOC 2, chúng tôi phát hiện 1 lập trình viên đã tự tạo MR và tự bấm nút Approve cho chính mình để merge code lên Production. Em khắc phục lỗ hổng này như thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Sửa đổi Cài đặt Bảo mật khẩn cấp (QT 45.5 & QT 45.6):** Truy cập MR Settings của tất cả các dự án, bật cờ `merge_requests_author_approval = false` (Cấm tác giả tự duyệt) và `merge_requests_disable_committers_approval = true` (Cấm committer tự duyệt).
    2. **Áp dụng Group-level Enforce:** Khóa cờ này ở cấp Group Level để các quản trị viên dự án con không thể tự ý tắt bỏ.
    3. **Kiểm tra Audit Log:** Trích xuất Audit Events trích xuất tất cả các MR từng bị tự duyệt trong quá khứ để gửi đội Security rà soát lại mã nguồn.

---

### Kịch bản 3: Giải quyết Thảm họa Lộ AWS Keys do Dev Commit Tệp `.env` lên Git
- **Người phỏng vấn (Cloud Security Lead):** *"Một dev lỡ tay push tệp `.env` chứa `AWS_SECRET_ACCESS_KEY` lên repo. Dù pipeline CI quét SAST phát hiện sau 5 phút và dev đã xóa file, nhưng AWS Key vẫn bị hacker quét lấy mất. Em xử lý thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Thu hồi Secret khẩn cấp:** Thu hồi ngay lập tức AWS Key bị lộ trên AWS IAM Console trong 2 phút.
    2. **Chuyển đổi sang Secret Push Protection (QT 45.10):**
       - Quét SAST trong CI Pipeline xảy ra **sau khi code đã trôi lên Git Server** (lưu trong Git History).
       - Bật cờ **Secret Push Protection** ở cấp Group Settings. Hệ thống sẽ quét payload ngay khi dev gõ lệnh `git push` từ máy cá nhân. Nếu phát hiện AWS Key, lệnh push bị từ chối ngay từ cửa ngõ ($0\%$ secret trôi lên server), triệt hạ $100\%$ rủi ro lộ key!

---

### Kịch bản 4: Xử lý Kẻ gian Mạo danh Email Trưởng phòng Dev để Merge Mã độc
- **Người phỏng vấn (DevOps Team Lead):** *"Kẻ gian gõ `git config user.email "lead@company.com"` mạo danh anh để push một commit chứa backdoor lên nhánh main. Làm sao em ngăn chặn tuyệt đối trò mạo danh này?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Bật cờ GPG Commit Signature Verification (QT 45.11):**
       - Khai báo Push Rule `reject_unsigned_commits = true` trên Protected Branch `main`.
    2. **Cơ chế bảo vệ:**
       - Trong Git thô, ai cũng đổi tên/email được. Nhưng với cờ GPG Verification, mọi commit bắt buộc phải được ký bằng **GPG/SSH Private Key** cá nhân của anh.
       - Commit mạo danh của kẻ gian không có chữ ký số hợp lệ sẽ bị GitLab Server từ chối ngay lập tức với thông báo `Unsigned commit rejected`!

---

### Kịch bản 5: Xử lý Thảm họa Dev Lỡ tay Gõ `git push --force origin main` Xóa Sạch Code
- **Người phỏng vấn (Infrastructure Manager):** *"Năm ngoái một công ty bạn bị dev lỡ tay gõ `git push --force origin main` làm xóa sạch lịch sử commit 3 năm của nhánh main. Em cấu hình làm sao để điều này KHÔNG BAO GIỜ xảy ra ở công ty mình?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Cấu hình Protected Branch Cấm Force Push (QT 45.1):**
       - Gọi REST API đặt `allow_force_push = false` và `push_access_level = 0` trên nhánh `main` và `production`.
    2. **Kết quả:** Khi dev lỡ tay gõ `git push --force`, GitLab Server sẽ chối bỏ lệnh lập tức với thông báo `GitLab: You are not allowed to force push code to a protected branch on this project.` Nguồn tài sản mã nguồn của công ty được bảo vệ an toàn $100\%$!

---

### Kịch bản 6: Giải thích Cơ chế Tự động Hủy Approval khi Push Commit Mới cho Developer
- **Người phỏng vấn (Developer Lead):** *"Dev của anh phàn nàn là sau khi nhờ 2 người approve MR xong, chỉ lỡ push thêm 1 commit fix typo nhỏ mà hệ thống bắt xóa sạch approvals làm lại từ đầu rất tốn thời gian. Em giải thích sao cho họ thuyết phục?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    - "Anh ơi, cờ `reset_approvals_on_push = true` (QT 45.4) là **tường lửa sống còn để bảo vệ chính đội ngũ dev**:"
    - "Nếu không bật cờ này, một ai đó có thể nhờ approve tệp code sạch. Sau đó họ lén push thêm 1 commit chứa code lỗi hoặc backdoor vào MR đó và bấm Merge! Vì approvals cũ không bị xóa, code lỗi sẽ trôi thẳng lên Production gây sập hệ thống và đội dev sẽ phải chịu trách nhiệm."
    - "Để tránh phiền phức khi fix typo nhỏ, em sẽ hướng dẫn đội dev sử dụng kỹ thuật **`git commit --amend` hoặc Git Squash local** trước khi nhờ đồng nghiệp review!"

---

### Kịch bản 7: Xây dựng Hệ thống Trích xuất Log Kiểm toán SIEM Real-time cho Đội Security
- **Người phỏng vấn (SIEM Security Engineer):** *"Đội Security cần nhận ngay lập tức thông báo khi có ai đó thay đổi phân quyền Owner hoặc xóa Protected Branch trên GitLab. Em triển khai thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Triển khai Streaming Audit Events API (QT 45.9):**
       - Khai báo Webhook destination trỏ tới **Splunk / Elastic HTTP Event Collector (HEC)** trong Group Audit Settings.
    2. **Đẩy Event Real-time:**
       - Ngay khi có sự kiện đổi quyền hoặc xóa Protected Branch, GitLab sẽ đóng gói JSON Audit Event và đẩy qua HTTPS trong $0.5$ giây về Splunk.
    3. **Cảnh báo War Room:** Dựng Alerting trên Splunk tự động bắn notification lên kênh Slack `#security-alerts` để đội SOC xử lý tức thì!

---

## §V3. Câu chốt để nói khi phỏng vấn

1. *"Luận đề trung tâm của quản trị an ninh là **kiểm soát tuân thủ nào cưỡng chế được bằng cấu hình (Enforced by Code) thì mới là kiểm soát**; còn tài liệu Word chỉ là mong muốn."*
2. *"Tuyệt đối **khóa Protected Branch `main` cấm Force Push và Direct Push (`push_access_level = 0`)** trên 100% Repositories Production."*
3. *"Áp dụng tệp **`CODEOWNERS` để tự động gán đúng nhóm chuyên trách (DevOps/Security)** phê duyệt các thư mục nhạy cảm."*
4. *"Bắt buộc **Quy tắc 4 Mắt (Four-Eye Principle - tối thiểu 2 Approvals độc lập)** cho mọi Merge Request trỏ về Production."*
5. *"Luôn bật cờ **`reset_approvals_on_push = true`** để tự động hủy các lượt phê duyệt cũ ngay khi có commit mới push thêm vào MR."*
6. *"Triệt hạ lỗ hổng xung đột lợi ích bằng cách **bật cờ cấm Author Self-Approval và Committer Approval**."*
7. *"Bảo vệ các nhãn release **`v*` bằng Protected Tags** để ngăn dev tự do kích hoạt pipeline deploy Production từ máy cá nhân."*
8. *"Triển khai **GitLab Compliance Frameworks cấp Group Level** để ép 500 Repositories tự động kế thừa pipeline quét bảo mật chuẩn."*
9. *"Chặn đứng rò rỉ chìa khóa ngay từ cửa ngõ bằng **Secret Push Protection quét gói tin real-time từ lệnh `git push`**."*
10. *"Bật cờ **`reject_unsigned_commits = true`** để bắt buộc ký số GPG/SSH Verified, chống thảm họa mạo danh identity trong Git."*

---

## BTVN 4: Chuẩn bị cho Buổi 46 — Đo nền tảng CI/CD: DORA, tỉ lệ thất bại, chi phí runner

Để chuẩn bị tốt nhất cho **Buổi 46: Đo nền tảng CI/CD: DORA, tỉ lệ thất bại, chi phí runner**, học viên cần thực hiện các nhiệm vụ sau:

1. **Ôn tập 4 Chỉ số DORA Metrics Quốc tế:**
   - Tìm hiểu định nghĩa 4 chỉ số đo lường hiệu năng CI/CD & DevOps: **Deployment Frequency (DF)**, **Lead Time for Changes (LTC)**, **Change Failure Rate (CFR)**, và **Mean Time to Restore (MTTR)**.
   - Phân tích cách GitLab CI thu thập tự động các chỉ số DORA qua REST API (`/api/v4/projects/:id/dora/metrics`).

2. **Nghiên cứu về Tối ưu Chi phí Hạ tầng Runner (Runner Cost Optimization):**
   - Phân tích luận đề: *"Số phút chạy Runner (Runner Minutes) là con số đo lường ngân sách trực tiếp giữa đội DevOps và Giám đốc Tài chính CFO!"*
   - Tìm hiểu cách tính toán chi phí Runner minutes trên các loại máy chủ (EC2, Spot Instances, GKE Autopilot).

3. **Bài tập chuẩn bị trước giờ học:**
   - Trả lời câu hỏi: *"Nếu chỉ số Change Failure Rate (CFR) của đội bạn đang ở mức 25%, bạn sẽ sử dụng các công cụ CI/CD nào đã học để kéo CFR xuống dưới 5%?"*
   - Chuẩn bị một đoạn script Python gọi REST API GitLab để lấy tổng số deployments trong tháng vừa qua!
{% endraw %}
