---
layout: post
title: "[Bài 33] Pipeline Compliance & Security Policies Toàn Doanh Nghiệp Trong GitLab CI"
date: 2026-09-12 07:10:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Compliance
  - Governance
  - SecurityPolicies
  - Audit
  - Part-33
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 33
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.33] Quản trị tuân thủ quy chuẩn doanh nghiệp: Thiết lập Scan Execution Policies, Scan Result Policies, bắt buộc Pipeline bảo mật cấp Group và đáp ứng các tiêu chuẩn kiểm toán quốc tế SOC 2, PCI-DSS, ISO 27001."
tldr:
  - "Nắm vững nguyên lý quản trị tuân thủ cấp Enterprise (Enterprise Compliance & Security Governance)."
  - "Làm chủ cơ chế Scan Execution Policies (SEP) ép buộc chạy job quét bảo mật mà lập trình viên không thể ghi đè."
  - "Cấu hình Scan Result Policies tự động yêu cầu phê duyệt bảo mật (Security Approval Gates) khi có lỗ hổng mới."
  - "Thiết lập cơ chế tách biệt quyền hạn (Separation of Duties - SoD) và lưu trữ nhật ký kiểm toán bất biến."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 12 câu hỏi phỏng vấn phân tích tình huống thực tế."
description: "Xây dựng và thực thi chính sách tuân thủ bắt buộc với GitLab Compliance Pipelines: Đảm bảo 100% dự án áp dụng Security Gates và lưu vết bằng chứng kiểm toán Audit Trails."
keywords:
  - gitlab compliance framework
  - gitlab compliance pipeline
  - gitlab audit events
  - gitlab soc2 iso27001
---

{% raw %}
> [!IMPORTANT]
> **Mục tiêu kỹ thuật bài học**:
> - Nắm vững nguyên lý quản trị tuân thủ cấp Enterprise (Enterprise Compliance & Security Governance).
> - Làm chủ cơ chế Scan Execution Policies (SEP) ép buộc chạy job quét bảo mật mà lập trình viên không thể ghi đè.
> - Cấu hình Scan Result Policies tự động yêu cầu phê duyệt bảo mật (Security Approval Gates) khi có lỗ hổng mới.
> - Thiết lập cơ chế tách biệt quyền hạn (Separation of Duties - SoD) và lưu trữ nhật ký kiểm toán bất biến.

---

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

### 1.1. Luận Đề Trung Tâm: Sự Xung Đột Giữa Quyền Tự Quyết Của Developer & Yêu Cầu Tuân Thủ Của Doanh Nghiệp

Trong các tổ chức quy mô hàng trăm hoặc hàng ngàn lập trình viên, mỗi nhóm dự án thường có toàn quyền chỉnh sửa tệp `.gitlab-ci.yml` của riêng mình. Điều này dẫn đến những rủi ro tuân thủ (Compliance Risks) nghiêm trọng:
1. **Lập trình viên tự ý xóa Job bảo mật**: Để hoàn thành deadline gấp, developer có thể xóa hoặc chú thích (comment out) các job SAST, Secret Detection hoặc SCA để pipeline chạy nhanh hơn.
2. **Thiếu tính đồng bộ toàn công ty**: 100 dự án sử dụng 100 phiên bản scanner khác nhau, không tuân theo một tiêu chuẩn thống nhất.
3. **Thất bại trong các kỳ kiểm toán quốc tế**: Các chứng chỉ kiểm toán khắt khe như **SOC 2 Type II, PCI-DSS v4.0, ISO/IEC 27001, HIPAA** đòi hỏi tổ chức phải chứng minh bằng văn bản và logs kỹ thuật rằng: **"100% mã nguồn khi release lên Production BẮT BUỘC phải chạy qua kiểm thử bảo mật và không có ngoại lệ nào có thể bypass."**

> **Giải pháp là kiến trúc "Centralized Security Policy Management" của GitLab: Đội ngũ Security thiết lập các chính sách Scan Execution Policies và Compliance Frameworks tại cấp Group cha cao nhất. Các chính sách này sẽ được ép ngầm (Injected) vào pipeline của mọi repository con mà lập trình viên không có quyền chỉnh sửa, vô hiệu hóa hay bỏ qua.**

```text
       CƠ CHẾ ÉP BUỘC CHÍNH SÁCH BẢO MẬT TẬP TRUNG (GitLab Security Policies)

      [ Group Level: Security Policy Project ] (Chỉ Security Team có quyền sửa)
                         │
                         ▼
        ┌─────────────────────────────────────────────────┐
        │  Scan Execution Policy:                         │
        │  - Bắt buộc chạy Semgrep SAST trên mọi MR       │
        │  - Bắt buộc quét Secret Detection trên mọi Tag   │
        └──────────────┬───────────────────┬──────────────┘
                       │                   │
         (Tự động chèn ngầm)       (Tự động chèn ngầm)
                       │                   │
                       ▼                   ▼
      [ Project A: .gitlab-ci.yml ]  [ Project B: .gitlab-ci.yml ]
      (Chỉ viết test/build của Dev)  (Chỉ viết test/build của Dev)
                       │                   │
                       ▼                   ▼
       [ PIPELINE THỰC THI HOÀN CHỈNH ] [ PIPELINE THỰC THI HOÀN CHỈNH ]
       - Job: App Unit Tests (Dev)      - Job: App Unit Tests (Dev)
       - Job: Semgrep SAST (Enforced)   - Job: Semgrep SAST (Enforced)
       - Job: Secret Scan (Enforced)    - Job: Secret Scan (Enforced)
```

```mermaid
graph TD
    subgraph GROUP_GOVERNANCE["1. Quản Trị Cấp Group (Security Team)"]
        SEC_POLICY_REPO["Security Policy Project (.gitlab/security-policies/policy.yml)"]
        COMPLIANCE_LABEL["Compliance Framework Label: 'SOC2-Regulated'"]
        SEC_POLICY_REPO --> SEP["Scan Execution Policy (SEP)"]
        SEC_POLICY_REPO --> SRP["Scan Result Policy (Approval Rules)"]
    end

    subgraph PROJECT_INHERITANCE["2. Thừa Kế Tự Động Tại Project Con"]
        PROJECT_CI["Project: .gitlab-ci.yml (Do Developer quản lý)"]
        SEP -->|"Chèn ngầm không thể xóa"| MERGED_PIPELINE["Merged Runtime Pipeline"]
        PROJECT_CI --> MERGED_PIPELINE
    end

    subgraph AUDIT_AND_GATE["3. Kiểm Soát Cổng Merge & Kiểm Toán"]
        MERGED_PIPELINE --> SCAN_OUT["Kết quả quét bảo mật"]
        SCAN_OUT --> SRP
        SRP --> CHECK_VULN{"Có lỗ hổng Critical mới?"}
        CHECK_VULN -->|"Có"| REQUIRE_SEC_APPROVAL["Khóa Merge -> Bắt buộc Security Lead Approve"]
        CHECK_VULN -->|"Không"| ALLOW_MERGE["Cho phép Merge"]
        MERGED_PIPELINE --> AUDIT_LOGS["Immutable Audit Events Store (SOC2 / ISO 27001)"]
    end
```

### 1.2. Phân Biệt Scan Execution Policies vs Scan Result Policies

1. **Scan Execution Policies (SEP - Chính sách thực thi quét)**:
   - Quy định **KHI NÀO** và **CÔNG CỤ NÀO** phải được kích hoạt.
   - Ví dụ: "Ép buộc chạy Secret Detection và Trivy Container Scan trên tất cả các commit nhánh `main` và `release/*`".
   - Hoàn toàn độc lập với tệp `.gitlab-ci.yml` của dự án.
2. **Scan Result Policies (SRP / Security Approval Policies - Chính sách phê duyệt kết quả)**:
   - Quy định **HÀNH ĐỘNG GÌ XẢY RA** dựa trên kết quả quét.
   - Ví dụ: "Nếu phát hiện bất kỳ lỗ hổng mức độ **CRITICAL** hoặc **HIGH** mới, hệ thống tự động khóa nút Merge và yêu cầu ít nhất 2 thành viên thuộc nhóm `@security-team` phê duyệt bằng chữ ký số".

### 1.3. Nguyên Tắc Tách Biệt Quyền Hạn (Separation of Duties - SoD)

Để đạt chứng chỉ kiểm toán SOC 2, hệ thống phải đảm bảo nguyên tắc:
- **Người viết mã (Developer)**: Không được quyền tự phê duyệt Merge Request của chính mình.
- **Người triển khai Production**: Không được quyền chỉnh sửa trực tiếp các chính sách kiểm thử an ninh.
- **Dự án Policy**: Được lưu trữ tại một repository riêng biệt có quyền truy cập chỉ dành cho Security Officers.

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

| Tiêu Chí Kỹ Thuật | Manual CI Templates (`include:`) | Compliance Pipelines (Legacy) | Scan Execution Policies (Hiện Đại) | Scan Result Policies (Approval) |
| :--- | :--- | :--- | :--- | :--- |
| **Vị Trí Cấu Hình** | Trong tệp `.gitlab-ci.yml` | Gán nhãn Project Settings | **Security Policy Project riêng biệt** | **Security Policy Project riêng biệt** |
| **Khả Năng Bypass Của Dev** | **Có (Dev có thể xóa dòng include)** | Khó (Gán cứng template) | **Tuyệt đối không thể bypass** | **Tuyệt đối không thể bypass** |
| **Quyền Quản Lý Tách Biệt** | Dev & Sec chung quyền | Admin / Maintainer | **Chỉ Security Team có quyền sửa** | **Chỉ Security Team có quyền sửa** |
| **Ghi Đè Biến Môi Trường** | Dev có thể ghi đè biến | Có thể xung đột | **Policy variables có độ ưu tiên cao** | Khóa cấu hình merge |
| **Tự Động Khóa Merge Request**| Không (Cần script custom) | Không | Không | **Tự động thêm Security Approvers** |
| **Hỗ Trợ Lên Lịch (Schedules)**| Phải tạo schedule thủ công | Theo pipeline chạy | **Lên lịch quét định kỳ toàn Group** | Theo sự kiện Merge Request |
| **Mức Độ Tuân Thủ Kiểm Toán** | Không đạt chuẩn SOC 2 | Đạt một phần | **Chuẩn mực cao nhất SOC 2 / PCI-DSS** | **Chuẩn mực cao nhất SOC 2 / PCI-DSS** |

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (Architecture Breakdown)

### 3.1. Cấu Trúc Dự Án Security Policy Toàn Doanh Nghiệp

```text
security-policy-management/ (Repository riêng biệt cấp Group)
├── .gitlab/
│   └── security-policies/
│       └── policy.yml       # Tệp định nghĩa toàn bộ Scan Execution & Approval Policies
└── README.md
```

### 3.2. Nội Dung Tệp `policy.yml` Chuẩn Enterprise Governance

```yaml
---
# -------------------------------------------------------------
# 1. Scan Execution Policy: Ép buộc chạy SAST và Secret Detection
# -------------------------------------------------------------
scan_execution_policy:
  - name: Enforce Enterprise SAST on All Branches
    description: "Bắt buộc chạy phân tích tĩnh Semgrep SAST trên mọi commit và MR của toàn bộ các dự án con"
    enabled: true
    rules:
      - type: pipeline
        branches:
          - "*"
    actions:
      - scan: sast
      - scan: secret_detection

  - name: Nightly Container Security Audit
    description: "Tự động chạy quét toàn bộ Container Images vào 01:00 AM hàng ngày"
    enabled: true
    rules:
      - type: schedule
        cadence: "0 1 * * *"
        branches:
          - "main"
    actions:
      - scan: container_scanning

# -------------------------------------------------------------
# 2. Scan Result Policy: Khóa Merge khi có lỗ hổng Critical
# -------------------------------------------------------------
scan_result_policy:
  - name: Block Unapproved Critical Vulnerabilities
    description: "Tự động khóa Merge Request nếu phát hiện lỗ hổng Critical mới chưa được Security Lead phê duyệt"
    enabled: true
    rules:
      - type: scan_finding
        branches:
          - "main"
          - "release/*"
        scanners:
          - sast
          - dependency_scanning
          - container_scanning
        vulnerabilities_allowed: 0
        severity_levels:
          - critical
        vulnerability_states:
          - newly_detected
    actions:
      - type: require_approval
        approvals_required: 2
        user_approvers:
          - security_lead_user
        group_approvers:
          - enterprise-security-officers
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

### 4.1. Sự Cố Thực Tế: Thất Bại Kiểm Toán SOC 2 Do Lập Trình Viên Tự Merge Code Không Qua Scan

> **Bối Cảnh**: Trong đợt kiểm toán độc lập thường niên để đạt chứng chỉ **SOC 2 Type II**, đơn vị kiểm toán phát hiện hơn 30 Merge Requests của dịch vụ thanh toán được merge thẳng vào nhánh `main` mà không hề chạy bất kỳ bài kiểm tra an ninh nào. Lý do là các kỹ sư đã tạm thời thêm cờ `[skip ci]` hoặc xóa dòng `include` bảo mật để kịp giờ phát hành tính năng khuyến mãi.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    PHÂN TÍCH NGUYÊN NHÂN GỐC RỄ (5-WHYS)                 │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. Tại sao có 30 Merge Requests được merge mà không qua Security Scan?  │
│    -> Tệp .gitlab-ci.yml trong các MR đó bị xóa khối kiểm tra bảo mật.  │
│                                                                         │
│ 2. Tại sao lập trình viên có thể xóa được khối kiểm tra bảo mật?       │
│    -> Khối bảo mật được nhúng bằng lệnh include truyền thống trong repo.│
│                                                                         │
│ 3. Tại sao doanh nghiệp lại áp dụng cơ chế include tự nguyện?          │
│    -> Chưa chuyển dịch sang mô hình Scan Execution Policies cấp Group.  │
│                                                                         │
│ 4. Tại sao không có ai phát hiện việc bị xóa trong lúc review MR?       │
│    -> Nhóm phát triển tự review lẫn nhau mà không có Security Gate.     │
│                                                                         │
│ 5. NGUYÊN NHÂN CỐT LÕI (Root Cause):                                   │
│    -> Thiếu chính sách thực thi bảo mật bất biến (Immutable Policy)     │
│       và vi phạm nguyên tắc tách biệt quyền hạn (Separation of Duties). │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2. Giải Pháp Khắc Phục Triệt Để

1. **Chuyển toàn bộ quy tắc sang Scan Execution Policies**: Không cấu hình scanner trong `.gitlab-ci.yml` của dự án nữa; chuyển sang dự án Policy tập trung cấp Group.
2. **Kích hoạt tính năng Merge Request Approval Rules**: Khóa cứng quyền merge, bắt buộc phải có ít nhất 1 thành viên độc lập (Code Owner / Security Lead) phê duyệt và tất cả Security Policies phải ở trạng thái Passed.

---

## 5. Hands-on Lab: Thiết Lập Quản Trị Tuân Thủ Toàn Doanh Nghiệp (8 Bước Chuẩn)

### 5.1. Mục Tiêu Lab
- Khởi tạo một Group mẹ và một dự án Security Policy Project.
- Định nghĩa chính sách Scan Execution Policy (SEP) ép buộc chạy Secret Detection.
- Định nghĩa chính sách Scan Result Policy (SRP) yêu cầu phê duyệt khi có lỗ hổng.
- Tạo một dự án con, cố tình commit hardcoded secret và quan sát hệ thống tự động chèn job bảo mật và khóa nút Merge.

```text
       MÔ HÌNH THỰC HÀNH LAB QUẢN TRỊ TUÂN THỦ TRÊN GITLAB CI

     [ Group: enterprise-fintech ]
            │
            ├──► [ Security Policy Project: security-governance ]
            │      └── .gitlab/security-policies/policy.yml
            │
            └──► [ Project Con: payment-gateway ]
                   └── .gitlab-ci.yml (Chỉ có job npm test)
                             │
                             ▼
     [ Developer commit chứa Secret ] ──► [ Pipeline tự động Injected Secret Scan ]
                                                │
                                                ▼
                                   [ Khóa Nút Merge Bắt Buộc ]
                                   (Chờ Security Team Phê Duyệt)
```

### 5.2. Các Bước Thực Hiện Chi Tiết

#### Bước 1: Khởi Tạo Dự Án Quản Trị Chính Sách `security-governance`
Tạo một repository mới tên `security-governance` tại Group cấp cao nhất.

#### Bước 2: Tạo Thư Mục Cấu Hình Chính Sách
```bash
mkdir -p .gitlab/security-policies
```

#### Bước 3: Định Nghĩa Tệp `.gitlab/security-policies/policy.yml`
```yaml
---
scan_execution_policy:
  - name: Enforce Secret Detection Everywhere
    description: "Ép buộc quét phát hiện bí mật rò rỉ trên mọi pipeline của Group"
    enabled: true
    rules:
      - type: pipeline
        branches:
          - "*"
    actions:
      - scan: secret_detection

scan_result_policy:
  - name: Require Security Approval for Leaked Secrets
    description: "Chặn merge khi phát hiện rò rỉ Secret mới"
    enabled: true
    rules:
      - type: scan_finding
        branches:
          - "main"
        scanners:
          - secret_detection
        vulnerabilities_allowed: 0
        severity_levels:
          - critical
          - high
        vulnerability_states:
          - newly_detected
    actions:
      - type: require_approval
        approvals_required: 1
        group_approvers:
          - enterprise-sec-leads
```

#### Bước 4: Liên Kết Chính Sách Vào Cài Đặt Của Group
- Truy cập Group **Security -> Policies** trên thanh điều hướng GitLab.
- Nhấn **Edit policy configuration** và chọn dự án `security-governance`.

#### Bước 5: Tạo Dự Án Con `payment-gateway` Với Tệp CI Tối Giản
Tạo dự án con `payment-gateway`. Trong `.gitlab-ci.yml`, chỉ khai báo các job thông thường của developer:
```yaml
stages:
  - test

run_unit_tests:
  stage: test
  image: node:20-alpine
  script:
    - echo "Running application unit tests... PASS"
```

#### Bước 6: Cố Tình Commit Một Tệp Chứa Mật Khẩu Thô (Vulnerable Code)
Tạo tệp `config.js` cố tình để lộ AWS Access Key:
```javascript
// Hardcoded AWS Key
const AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE";
const AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";

module.exports = { AWS_ACCESS_KEY, AWS_SECRET_KEY };
```

#### Bước 7: Mở Merge Request Và Quan Sát Pipeline Tự Động
- Đẩy branch `feature/payment-integration` và mở Merge Request vào `main`.
- Quan sát giao diện Pipeline: Xuất hiện thêm job **`secret-detection`** được hệ thống tự động chèn vào mặc dù file `.gitlab-ci.yml` của dự án không hề khai báo!
- Job `secret-detection` hoàn tất và phát hiện `AWS API Key` bị lộ.

#### Bước 8: Kiểm Tra Trạng Thái Khóa Nút Merge
- Trên giao diện Merge Request: Nút **Merge** bị khóa hoàn toàn.
- Dòng thông báo hiển thị: `Approval required from Security Policy: Require Security Approval for Leaked Secrets (Requires 1 approval from enterprise-sec-leads)`.

> [!NOTE]
> **Check-point Lab 33**: Chính sách bảo mật được thực thi độc lập từ cấp Group cha, ngăn chặn hoàn toàn việc developer bypass quy trình an ninh.

---

## 6. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span>Tại sao các kỳ kiểm toán SOC 2 và PCI-DSS lại yêu cầu sử dụng Scan Execution Policies thay vì lệnh `include` truyền thống?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Yêu cầu kiểm toán:</strong></p>
    <p>Kiểm toán viên yêu cầu bằng chứng về <strong>Tính bất biến của quy trình kiểm soát (Control Immutability)</strong>. Lệnh <code>include</code> trong tệp <code>.gitlab-ci.yml</code> nằm trong quyền kiểm soát của developer (họ có thể xóa hoặc sửa đổi bất cứ lúc nào). Scan Execution Policies được cấu hình tại một dự án riêng biệt mà developer hoàn toàn không có quyền truy cập, đảm bảo tính khách quan và tuân thủ tuyệt đối 100% không có ngoại lệ.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span>Làm thế nào để áp dụng các chính sách tuân thủ khác nhau cho các dự án có mức độ rủi ro khác nhau trong cùng một Group?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Giải pháp Compliance Frameworks:</strong></p>
    <p>Tạo các nhãn <strong>Compliance Framework Labels</strong> tại cấp Group (ví dụ: nhãn <code>PCI-Regulated</code> cho các dự án thanh toán và nhãn <code>Standard</code> cho các dự án nội bộ). Sau đó trong <code>policy.yml</code>, sử dụng bộ lọc <code>compliance_frameworks</code> để chỉ áp dụng các quy tắc quét khắt khe nhất cho các repository được gắn nhãn tương ứng.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span>Sự khác biệt giữa `vulnerability_states: [newly_detected]` và `[previously_existing]` trong Scan Result Policy là gì?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Ý nghĩa thực chiến:</strong></p>
    <ul>
      <li><code>newly_detected</code>: Chỉ kích hoạt khóa Merge nếu commit trong MR <strong>tạo ra thêm lỗ hổng mới</strong> chưa từng có trước đó trên nhánh đích. Giúp developer không bị chặn oan bởi các khoản nợ kỹ thuật (Technical Debt) cũ của dự án.</li>
      <li><code>previously_existing</code>: Khóa Merge nếu dự án vẫn còn tồn tại bất kỳ lỗ hổng cũ nào chưa được xử lý, dùng cho các chiến dịch thanh lọc nợ bảo mật bắt buộc.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span>Làm thế nào để đảm bảo tính bất biến của nhật ký kiểm toán (Audit Logs) trong GitLab?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Giải pháp Enterprise:</strong></p>
    <ul>
      <li>Sử dụng tính năng <strong>Audit Events Streaming</strong> của GitLab để truyền trực tiếp toàn bộ log sự kiện (ai đổi quyền, ai sửa biến, ai merge code) sang hệ thống SIEM tập trung bên ngoài (như Splunk, Datadog, AWS S3 Immutable Vault với Object Lock WORM).</li>
      <li>Kể cả khi quản trị viên GitLab có ý đồ xấu cũng không thể sửa đổi hay xóa nhật ký đã được ghi vào SIEM ngoài.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span>Tại sao cần cấm sử dụng cờ `--skip-ci` hoặc `[ci skip]` trên các Protected Branches?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Ngăn chặn bypass:</strong></p>
    <p>Nếu cho phép dùng <code>[skip ci]</code> trên nhánh chính, một kỹ sư có quyền push có thể chèn mã độc vào commit và thêm chỉ thị skip CI để bỏ qua toàn bộ các bài quét bảo mật và tự động deploy. Cần cấu hình cài đặt dự án để vô hiệu hóa việc bỏ qua CI trên các nhánh được bảo vệ.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span>Khái niệm "Two-Person Rule" (Quy tắc 4 mắt) trong kiểm soát phát hành là gì?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Nguyên tắc:</strong></p>
    <p>Bất kỳ thay đổi mã nguồn nào đưa lên môi trường Production bắt buộc phải có <strong>ít nhất hai cá nhân độc lập tham gia</strong>: Một người viết mã (Author) và ít nhất một người duyệt độc lập (Peer Reviewer / Security Lead). GitLab hỗ trợ thiết lập chính sách <em>"Prevent author approval"</em> và <em>"Prevent committers approval"</em> để thực thi nghiêm ngặt quy tắc này.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span>Làm thế nào để kiểm soát các Runner của bên thứ ba không làm rò rỉ dữ liệu của Group được kiểm toán?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Chính sách cách ly Runner:</strong></p>
    <ol>
      <li>Vô hiệu hóa tính năng <strong>Shared Runners</strong> trên toàn bộ các Group nhạy cảm.</li>
      <li>Bắt buộc sử dụng <strong>Dedicated Group Runners</strong> chạy trên hạ tầng mạng riêng biệt có chứng nhận PCI-DSS.</li>
      <li>Bật cờ <strong>Protected Runner</strong> (chỉ tiếp nhận các jobs chạy trên Protected Branches).</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span>Làm cách nào để xử lý tình huống khẩn cấp (Hotfix Release) khi Security Policy đang chặn Merge?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Quy trình Break-Glass Emergency:</strong></p>
    <ul>
      <li>Không bao giờ tắt chính sách bảo mật của hệ thống.</li>
      <li>Sử dụng tài khoản **Security Officer On-Call** có thẩm quyền cao nhất để thực hiện quyền phê duyệt ngoại lệ khẩn cấp (Emergency Approval) trực tiếp trên Merge Request.</li>
      <li>Hệ thống tự động mở một bản ghi kiểm toán đặc biệt và gửi thông báo khẩn tới CISO để rà soát lại lý do trong vòng 24 giờ sau sự cố.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span>Cơ chế quản lý biến môi trường trong Scan Execution Policy có mức độ ưu tiên như thế nào so với biến của Project?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Thứ tự ưu tiên:</strong></p>
    <p>Các biến được định nghĩa bên trong tệp <code>policy.yml</code> của Scan Execution Policy có <strong>mức độ ưu tiên cao nhất</strong> và không thể bị ghi đè bởi các biến trùng tên được khai báo trong <code>.gitlab-ci.yml</code> của dự án hay cài đặt biến của developer, đảm bảo cấu hình bảo mật luôn chạy đúng ý đồ của Security Team.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span>Làm thế nào để lập lịch quét định kỳ (Nightly Scans) toàn bộ 200 repositories mà không cần tạo pipeline schedule thủ công trên từng repo?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Giải pháp:</strong></p>
    <p>Trong <code>policy.yml</code> của Security Policy Project cấp Group, định nghĩa một quy tắc có <code>type: schedule</code> và đặt biểu thức Cron <code>cadence: "0 2 * * *"</code>. GitLab sẽ tự động kích hoạt job quét bảo mật vào 02:00 AM mỗi đêm trên toàn bộ 200 repositories con trong Group mà không cần can thiệp thủ công.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q11</span>
    <span>Sự cố: Pipeline của developer bị lỗi xung đột stage do Scan Execution Policy tự động chèn job có stage không tồn tại. Xử lý thế nào?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Nguyên nhân & Khắc phục:</strong></p>
    <ul>
      <li><strong>Nguyên nhân</strong>: Tệp `.gitlab-ci.yml` của developer chỉ định nghĩa <code>stages: [build, deploy]</code>, trong khi scanner mặc định yêu cầu stage <code>test</code>.</li>
      <li><strong>Khắc phục</strong>: Các phiên bản GitLab hiện đại tự động quản lý Execution Order ngầm cho policy jobs, hoặc cấu hình rõ ràng thuộc tính <code>scan: sast</code> để GitLab tự động inject stage ẩn mà không cần developer phải sửa danh sách stages.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q12</span>
    <span>Làm cách nào để xuất báo cáo chứng minh tính tuân thủ (Compliance Report) cho đơn vị kiểm toán bên ngoài?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Trích xuất báo cáo:</strong></p>
    <p>Truy cập <strong>Security -> Compliance Center</strong> cấp Group trong GitLab. Xuất báo cáo <strong>Compliance Violations Report</strong> và <strong>Standards Adherence Report</strong> (đánh giá tỷ lệ tuân thủ các tiêu chuẩn SOC 2, ISO 27001) dưới dạng file CSV/PDF chính thức cung cấp cho kiểm toán viên.</p>
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

### 7.1. Tóm Tắt Các Điểm Cốt Lõi (Architectural Key Takeaways)
- **Centralized Security Policies**: Quản lý chính sách an ninh tập trung tại Group level, loại bỏ nguy cơ developer bypass quy trình.
- **Scan Execution Policies (SEP)**: Ép buộc thực thi các công cụ phân tích bảo mật trên toàn bộ repositories con một cách bất biến.
- **Scan Result Policies (SRP)**: Tự động hóa rào chắn phê duyệt (Approval Gates) khi phát hiện lỗ hổng Critical mới.
- **Audit Readiness**: Đảm bảo nguyên tắc tách biệt quyền hạn (SoD) và streaming nhật ký kiểm toán đáp ứng chuẩn SOC 2 / PCI-DSS.

### 7.2. Sơ Đồ Tư Duy Quản Trị Tuân Thủ Doanh Nghiệp (Mindmap)

```text
                    QUẢN TRỊ TUÂN THỦ DOANH NGHIỆP TRONG GITLAB
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
  [ Policy Architecture ]     [ Automated Enforcement ]      [ Compliance & Audit ]
  - Security Policy Project   - Scan Execution Policies      - SOC 2 & PCI-DSS Proof
  - Group-Level Governance    - Scan Result Approval Rules   - Immutable Audit Streaming
  - Separation of Duties      - Immutable Injected Jobs      - Compliance Dashboard
```

> [!TIP]
> **Bước tiếp theo trong lộ trình**: Hoàn thiện bộ tiêu chuẩn kiểm soát chất lượng và thiết lập rào chắn tự động trong [Bài 34: Quality & Security Gates Toàn Diện: Định Nghĩa, Đo Lường & Tự Động Hóa Chặn Release](gitlab-34-34-gate-va-chinh-sach.html).
{% endraw %}
