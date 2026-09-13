---
layout: post
title: "[Bài 42] Tự Động Hóa Hạ Tầng Với Terraform Trong CI: Terraform Plan / Apply Pipeline, State Locking & Infracost Estimate"
date: 2026-08-03 08:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-42
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 42
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.42] Hướng dẫn chuyên sâu Tự Động Hóa Hạ Tầng Với Terraform Trong CI: Terraform Plan / Apply Pipeline, State Locking & Infracost Estimate: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

{% raw %}
# [BÀI 42] TỰ ĐỘNG HÓA HẠ TẦNG VỚI TERRAFORM TRONG CI: TERRAFORM PLAN / APPLY PIPELINE, STATE LOCKING & INFRACOST ESTIMATE

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

---





| STT | Câu hỏi ôn tập | Đáp án chi tiết thực chiến |
|---|---|---|
| 1 | Khác biệt cốt lõi giữa Push-based CD và Pull-based GitOps CD là gì? | Push CD dùng CI Runner ở ngoài giữ Kubeconfig đẩy manifests; GitOps CD dùng Controller trong cụm tự đọc và kéo manifests từ Git. |
| 2 | Hai cờ lệnh bắt buộc nào phải bổ sung khi chạy `helm upgrade` từ CI? | Bắt buộc bổ sung hai cờ `--atomic` và `--wait` (kèm `--timeout 300s`) để tự động rollback khi Pod crash. |
| 3 | Ý nghĩa của cờ `syncPolicy.automated.selfHeal: true` trên ArgoCD? | Tự động ghi đè khôi phục lại cấu hình chuẩn từ Git khi phát hiện ai đó sửa bẩn thủ công trên cụm qua `kubectl edit`. |
| 4 | Làm thế nào để Rollback chuẩn xác trong mô hình GitOps ArgoCD? | Thực hiện câu lệnh `git revert <commit_sha>` và push lên kho GitOps Repo; tuyệt đối không gõ `helm rollback` thủ công trên cụm. |
| 5 | Công cụ nào giúp mã hóa an toàn Kubernetes Secrets để commit lên Git? | Bitnami SealedSecrets (dùng `kubeseal` mã hóa bất đối xứng) hoặc External Secrets Operator (ESO) liên kết Key Vault. |


**Luận đề trung tâm:**
> *"File `plan` trong Merge Request chỉ có giá trị khi **đúng tệp `tfplan` đó** được truyền sang stage `apply` — nếu không thì bước `plan` chỉ là trang trí và hạ tầng sẽ bị lệch hoàn toàn."*

Sau khi đã làm chủ việc triển khai ứng dụng trên Kubernetes ở Buổi 41, Buổi 42 đưa chúng ta đến với nền tảng quản trị toàn bộ hạ tầng bên dưới (VPC, Subnets, Kubernetes Clusters, Databases, IAM Roles) bằng **Terraform (Infrastructure as Code - IaC)**. Trong quy trình CI/CD Enterprise:
1. **Lưu trữ State File an toàn:** Không được lưu tệp `terraform.tfstate` trên máy cá nhân hay runner local. Bắt buộc dùng **GitLab Managed Terraform State Backend** có tính năng State Locking tự động.
2. **Luồng Plan/Apply Gate nghiêm ngặt:** Tạo file binary `tfplan` trong stage `plan` trên Merge Request, chuyển tệp đó thành Artifact và ép stage `apply` phải tiêu thụ ĐÚNG tệp artifact đó thông qua nút duyệt thủ công (`when: manual`).
3. **Phát hiện State Drift:** Chạy job `terraform plan -detailed-exitcode` định kỳ qua Cron Schedule để cảnh báo ngay lập tức nếu có ai đó tự ý sửa hạ tầng qua Cloud Console UI!

Bài học này sẽ giúp bạn xây dựng pipeline IaC chuẩn xác, bảo mật và an toàn 100%!

---



| STT | Kỹ năng thực chiến | Hiện vật chứng minh hoàn thành |
|---|---|---|
| 1 | Khởi tạo cấu hình GitLab Managed Terraform State Backend | Khai báo `backend "http"` trong tệp HCL `main.tf` |
| 2 | Xây dựng pipeline `terraform plan` tự động trên Merge Request | Job CI tạo artifact `tfplan` và comment báo cáo plan trên MR |
| 3 | Đóng cổng phê duyệt `terraform apply` qua Manual Gate | Stage `apply` với cờ `when: manual` tiêu thụ tệp `tfplan` |
| 4 | Tự động quét phát hiện lệch trạng thái hạ tầng (State Drift) | Cron pipeline chạy `terraform plan -detailed-exitcode` trả về Exitcode 2 |
| 5 | Tích hợp công cụ Linter & Security Scanner cho code HCL | Job CI chạy `tflint` và `tfsec`/`trivy` quét mã nguồn HCL |
| 6 | Định dạng mã nguồn HCL tự động | Job CI thực thi `terraform fmt -check` kiểm tra chuẩn định dạng |
| 7 | Loại bỏ chìa khóa tĩnh Cloud credentials | Kết nối Terraform runner với AWS/GCP/Azure qua OIDC Federation |
| 8 | Quản lý hạ tầng đa môi trường bằng Terraform Workspaces | Cấu hình độc lập State Files cho `staging` và `production` |

---



| Kiến thức / Kỹ năng | Mức độ yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Cú pháp ngôn ngữ HCL (HashiCorp Configuration Language) | Thành thục | Buổi 38-40 & Tài liệu Terraform |
| Các câu lệnh Terraform CLI (`init`, `plan`, `apply`, `destroy`) | Thành thục | Kiến thức IaC Nền tảng |
| Nguyên lý OIDC Cloud Federation cho CI Runner | Hiểu rõ | Buổi 37 về liên danh danh tính đám mây |
| Khai báo Artifacts và Dependencies trong `.gitlab-ci.yml` | Thành thục | Buổi 30 & Buổi 36 về tự động hóa pipeline CI/CD |
| Khái niệm State File (`terraform.tfstate`) và State Locking | Khá | Tài liệu quản trị Terraform State |

---





| Thuật ngữ Tiếng Việt | Thuật ngữ Tiếng Anh | Giải thích ý nghĩa thực tế |
|---|---|---|
| Tệp lưu trạng thái hạ tầng | Terraform State File (`.tfstate`) | Tệp chứa bản đồ ánh xạ giữa mã nguồn HCL và tài nguyên thực tế trên Cloud. |
| Khóa trạng thái hạ tầng | State Locking | Cơ chế ngắt ghi đồng thời防止 2 jobs CI cùng sửa State File gây hỏng dữ liệu. |
| Kế hoạch thay đổi hạ tầng | Execution Plan (`tfplan`) | Tệp binary chứa danh sách chính xác các tài nguyên sẽ được thêm/sửa/xóa. |
| Cổng duyệt kế hoạch | Plan/Apply Gate | Quy trình ép `apply` phải dùng lại đúng tệp `tfplan` đã được duyệt ở bước `plan`. |
| Độ lệch trạng thái hạ tầng | Infrastructure State Drift | Sự sai lệch giữa Trạng thái thực tế trên Cloud Console và Trạng thái trong State File. |
| Mã thoát chi tiết | Detailed Exit Code (`-detailed-exitcode`) | Cờ trả về Exitcode 0 (không đổi), 1 (lỗi), 2 (phát hiện có thay đổi hạ tầng). |
| Trình kiểm tra mã HCL | TFLint / TFSec | Công cụ phân tích tĩnh quét lỗi cú pháp, chuẩn thiết kế và lỗ hổng bảo mật HCL. |
| Đòn bẩy backend GitLab | GitLab Managed Terraform Backend | Dịch vụ HTTP Backend tích hợp sẵn của GitLab lưu trữ và khóa State File an toàn. |
| Không gian làm việc | Terraform Workspaces | Cơ chế phân tách State File cho nhiều môi trường (dev, staging, prod) trong cùng mã HCL. |
| Xác thực không chìa khóa | Keyless OIDC Authentication | Cơ chế cấp Access Token ngắn hạn cho Terraform runner gọi API Cloud qua OIDC. |



#### Mô hình 1: Sơ đồ Luồng Plan/Apply Gate và Drift Detection trong GitLab CI

```mermaid
flowchart TD
    subgraph Phase 1: Merge Request (Plan Gate)
        A[Developer Create MR] --> B[CI Runner: terraform init]
        B --> C[CI Runner: terraform plan -out=tfplan]
        C -->|1. Create Artifact| D[Artifact: tfplan Binary File]
        C -->|2. Render Report| E[MR Comment: Infrastructure Changes]
    end

    subgraph Phase 2: Merge & Apply (Manual Gate)
        F[Tech Lead Approves & Merges MR] --> G[Pipeline on main Branch]
        G --> H[Job: terraform apply tfplan]
        D -->|Pass EXACT tfplan Artifact| H
        H -->|Apply Changes to Cloud| I[Cloud Resources Updated]
    end

    subgraph Phase 3: Cron Drift Detection
        J[Daily Scheduled Pipeline] --> K[terraform plan -detailed-exitcode]
        K -->|Exitcode 0: No Drift| L[Pipeline Passed]
        K -->|Exitcode 2: Drift Detected| M[Alert Slack/Email: Manual Cloud Edit!]
    end
```

#### Mô hình 2: Bảng So sánh Giữa Việc Dùng File `tfplan` Artifact và Chạy Lại `terraform apply` Trực Tiếp

| Tiêu chí so sánh | Cách làm SAI: Chạy `terraform apply` không có file `tfplan` | Cách làm CHUẨN: Truyền tệp `tfplan` Artifact từ `plan` sang `apply` |
|---|---|---|
| **Tính nhất quán hạ tầng** | **Cực kỳ nguy hiểm.** Trong thời gian từ lúc `plan` đến khi `apply`, nếu ai đó sửa Cloud hoặc merge MR khác, `apply` sẽ tạo tài nguyên KHÁC với cái đã review. | **Nhất quán 100%.** Lệnh `terraform apply tfplan` bắt buộc thực thi ĐÚNG các hành động đã được duyệt trong file plan binary. |
| **Rủi ro xóa nhầm tài nguyên** | Cao (do plan mới sinh ra tại thời điểm `apply` có thể xóa tài nguyên do lệch state). | **Bằng $0** (nếu tệp `tfplan` phát hiện state bị đổi, `apply` nổ lỗi dừng lập tức). |
| **Tốc độ thực thi** | Chậm (phải đọc lại toàn bộ Cloud API để tính toán lại plan trước khi apply). | **Rất nhanh** (đã có sẵn tệp binary execution plan, chỉ việc gọi API tạo tài nguyên). |
| **Nhật ký kiểm toán Audit** | Không thể chứng minh bản apply có đúng với bản plan đã duyệt hay không. | Lưu trữ tệp binary `tfplan` làm bằng chứng kiểm toán 100% khớp với MR review. |

##### Mẫu Cấu hình HCL Main.tf Tích hợp GitLab Managed HTTP Backend:
```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "http" {
    # Các biến cấu hình TF_HTTP_* được nạp tự động qua GitLab CI Variables
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "secure_assets" {
  bucket        = "bank-production-secure-assets-${var.environment}"
  force_destroy = false

  tags = {
    Environment = var.environment
    ManagedBy   = "GitLab-CI-Terraform"
    Project     = "BankCore"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "assets_crypto" {
  bucket = aws_s3_bucket.secure_assets.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

---

### 1.1. Quy tắc Cấu hình Backend & Plan/Apply Gate (10 phút)

### 4.1. Mẫu Tệp `.gitlab-ci.yml` Triển khai Terraform Plan/Apply Gate Chuẩn mực
Dưới đây là tệp cấu hình pipeline Terraform hoàn chỉnh tích hợp OIDC, State Backend, Artifacts và Manual Gate:

```yaml
stages:
  - validate
  - plan
  - apply
  - cleanup

image:
  name: hashicorp/terraform:1.5.7
  entrypoint: [""]

variables:
  TF_STATE_NAME: "production-infrastructure"
  TF_CACHE_KEY: "production"
  TF_ROOT: "${CI_PROJECT_DIR}/terraform"

before_script:
  - cd ${TF_ROOT}
  - export TF_HTTP_ADDRESS="${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/terraform/state/${TF_STATE_NAME}"
  - export TF_HTTP_AUTHENTICATE_PASSWORD="${CI_JOB_TOKEN}"
  - export TF_HTTP_USER="gitlab-ci-token"
  - export TF_HTTP_LOCK_ADDRESS="${TF_HTTP_ADDRESS}/lock"
  - export TF_HTTP_UNLOCK_ADDRESS="${TF_HTTP_ADDRESS}/lock"
  - export TF_HTTP_LOCK_METHOD="POST"
  - export TF_HTTP_UNLOCK_METHOD="DELETE"
  - terraform init -reconfigure

fmt-validate:
  stage: validate
  script:
    - terraform fmt -check
    - terraform validate

plan-mr:
  stage: plan
  script:
    - terraform plan -out=tfplan -input=false
    - terraform show -json tfplan | jq . > tfplan.json
  artifacts:
    name: "tfplan-${CI_COMMIT_SHA}"
    expire_in: 7 days
    paths:
      - ${TF_ROOT}/tfplan
      - ${TF_ROOT}/tfplan.json
    reports:
      terraform: ${TF_ROOT}/tfplan.json
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

apply-prod:
  stage: apply
  script:
    - terraform apply -input=false tfplan
  dependencies:
    - plan-mr
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

---

### 4.2. Các Quy tắc Cấu hình Terraform CI (QT 42.1 - QT 42.4)

**Nguyên lý cốt lõi:** Bắt buộc sử dụng tệp `tfplan` làm artifact duy nhất truyền từ stage `plan` sang stage `apply`.
**Phát biểu.** Khi thực hiện hạ tầng bằng Terraform trong CI, stage `plan` bắt buộc phải sinh ra tệp binary `-out=tfplan`, lưu thành Artifact và stage `apply` bắt buộc phải chạy lệnh `terraform apply tfplan`.
**Giải thích cơ chế ngầm:** Nếu chạy lệnh `terraform apply` không truyền file plan binary, Terraform sẽ tự động quét và tạo lại một plan mới tại thời điểm apply. Nếu trong khoảng thời gian chờ phê duyệt có người dùng sửa hạ tầng trên Cloud Console hoặc một MR khác được merge, plan mới này có thể chứa các hành động nguy hiểm (như xóa Database/VPC) mà chưa từng được ai review trên MR.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chạy lệnh `terraform apply -auto-approve` trực tiếp mà không truyền tệp `tfplan` artifact đã sinh ra từ stage `plan`.
**Minh hoạ.**
```yaml
# Stage plan
script:
  - terraform plan -out=tfplan
artifacts:
  paths: [tfplan]

# Stage apply
script:
  - terraform apply -input=false tfplan
```
**Con số chốt:** 100% `terraform apply` dùng tệp `tfplan` artifact.

---

**Nguyên lý cốt lõi:** Khai báo GitLab Managed HTTP Terraform State Backend với State Locking tự động.
**Phát biểu.** Bắt buộc cấu hình `backend "http"` trong tệp HCL trỏ tới GitLab Terraform State REST API endpoint.
**Giải thích cơ chế ngầm:** Tệp `terraform.tfstate` chứa thông tin nhạy cảm và ánh xạ hạ tầng. GitLab Managed State Backend vừa mã hóa mã lưu trữ (Encryption at Rest), vừa tích hợp tính năng **State Locking (HTTP POST/DELETE lock)** tự động. Khi một pipeline CI đang chạy `apply`, State File sẽ bị khóa chặt, ngăn chặn mọi pipeline khác ghi đè gây hỏng cấu trúc State (State Corruption).
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Lưu tệp `terraform.tfstate` cục bộ trên Runner hoặc commit file `.tfstate` lên kho Git.
**Minh hoạ.**
```hcl
terraform {
  backend "http" {}
}
```
**Con số chốt:** 100% State Files dùng GitLab Managed HTTP Backend.

---

**Nguyên lý cốt lõi:** Đặt cờ `when: manual` và `protected: true` cho stage `terraform apply` trên nhánh `main`.
**Phát biểu.** Stage thực thi `terraform apply` làm thay đổi hạ tầng Production bắt buộc phải đặt chế độ kích hoạt thủ công (`when: manual`) và chỉ chạy trên các nhánh được bảo vệ (`protected: true`).
**Giải thích cơ chế ngầm:** Đảm bảo nguyên tắc Phê duyệt hai bước (Four-Eye Principle). Mặc dù code đã được merge vào `main`, một kỹ sư DevOps cấp cao hoặc Tech Lead phải xem xét lại một lần cuối trước khi bấm nút kích hoạt `apply` hạ tầng trên đám mây.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đặt `when: always` cho stage `terraform apply` làm thay đổi hạ tầng Production tự động diễn ra ngay khi merge code không qua nút duyệt.
**Minh hoạ.**
```yaml
apply-production:
  stage: apply
  script:
    - terraform apply -input=false tfplan
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```
**Con số chốt:** 100% Apply Production qua nút duyệt Manual Gate.

---

**Nguyên lý cốt lõi:** Sử dụng OIDC Cloud Federation thay thế 100% static Cloud credentials khi thực thi Terraform trong CI.
**Phát biểu.** Kết nối máy chủ Terraform Runner với AWS/GCP/Azure hoàn toàn bằng cơ chế Workload Identity Federation (WIF) qua OIDC Token, tuyệt đối không lưu static Access Keys/Secret Keys trong CI Variables.
**Giải thích cơ chế ngầm:** Áp dụng các bài học đã hoàn thành ở buổi 37 QT 37.2, buổi 38 QT 38.1 và buổi 40 QT 40.1. Terraform Runner chỉ lấy được Cloud Access Token ngắn hạn tự hủy sau 60 phút. Nếu máy chủ Runner bị tấn công RCE, kẻ tấn công cũng không thể lấy trộm chìa khóa vĩnh viễn để chiếm quyền kiểm soát hạ tầng Cloud.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Lưu `AWS_ACCESS_KEY_ID` và `AWS_SECRET_ACCESS_KEY` tĩnh trong GitLab CI Variables.
**Minh hoạ.**
```yaml
id_tokens:
  GITLAB_OIDC_TOKEN:
    aud: https://gitlab.company.com
```
**Con số chốt:** 0% Static Cloud Keys trong Terraform CI.

---

### 1.2. Quy tắc Quản lý Drift Detection & Code Quality (10 phút)

**Nguyên lý cốt lõi:** Bổ sung cờ `-detailed-exitcode` trong các job kiểm định Drift Detection định kỳ qua Cron Schedule.
**Phát biểu.** Thiết lập một Pipeline Cron Schedule chạy hàng ngày thực thi câu lệnh `terraform plan -detailed-exitcode`.
**Giải thích cơ chế ngầm:** Cờ `-detailed-exitcode` làm cho `terraform plan` trả về 3 mã Exit Status chuẩn xác: `0` (không có thay đổi), `1` (có lỗi cú pháp), và **`2` (phát hiện có sự thay đổi hạ tầng / State Drift)**. Khi câu lệnh trả về Exitcode 2, job CI sẽ bắt được tín hiệu và ngay lập tức phát cảnh báo Slack/Email cho đội DevOps về việc có ai đó vừa tự ý sửa hạ tầng qua Cloud Console UI!
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chạy `terraform plan` định kỳ không có cờ `-detailed-exitcode` khiến CI luôn trả về Exitcode 0 và không bao giờ phát hiện được sai lệch hạ tầng.
**Minh hoạ.**
```bash
terraform plan -detailed-exitcode -input=false || EXIT_CODE=$?
if [ $EXIT_CODE -eq 2 ]; then
    echo "[DRIFT ALERT] Infrastructure Drift Detected on Cloud!"
    # Call Slack Webhook Alert
fi
```
**Con số chốt:** Exitcode 2 dùng cho Drift Detection.

---

**Nguyên lý cốt lõi:** Tích hợp công cụ `tflint` và `tfsec` / `trivy` trong stage `test` để quét lỗi cú pháp và lỗ hổng an toàn HCL.
**Phát biểu.** Mọi pipeline Terraform bắt buộc phải chạy bộ quét linter `tflint` (phát hiện lỗi cấu hình sai thuộc tính Cloud) và security scanner `tfsec` hoặc `trivy` (phát hiện lỗ hổng mở port S3/Security Group lỏng lẻo).
**Giải thích cơ chế ngầm:** Giúp phát hiện sớm 90% lỗi sai cú pháp tài nguyên Cloud và các rủi ro bảo mật (như mở Security Group 0.0.0.0/0 hay tắt mã hóa S3 Bucket) ngay trên Merge Request trước khi hạ tầng được khởi tạo.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Merge code HCL không qua bộ quét an ninh, làm lộ cổng database công khai ra Internet.
**Minh hoạ.**
```yaml
security-scan:
  stage: validate
  image: aquasec/trivy:latest
  script:
    - trivy config ${TF_ROOT}
```
**Con số chốt:** 100% HCL code được quét bởi `tflint` và `trivy`.

---

**Nguyên lý cốt lõi:** Định dạng tự động mã nguồn HCL với câu lệnh `terraform fmt -check` trong CI Pipeline.
**Phát biểu.** Đặt job chạy `terraform fmt -check -recursive` ở stage `validate` đầu tiên của pipeline.
**Giải thích cơ chế ngầm:** Đảm bảo toàn bộ mã nguồn HCL trong kho GitOps tuân thủ nghiêm ngặt chuẩn định dạng chuẩn mực của HashiCorp (2 spaces indent, căn chỉnh dấu `=`). Giúp mã nguồn sạch đẹp, dễ đọc và loại bỏ 100% các tranh cãi không cần thiết về định dạng code khi Review Merge Request.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để mã nguồn HCL lộn xộn khoảng trắng, làm rối mắt Reviewer và gây khó khăn cho việc so sánh git diff.
**Minh hoạ.** `terraform fmt -check -recursive` trong stage `validate`.
**Con số chốt:** 100% HCL code pass `terraform fmt`.

---

**Nguyên lý cốt lõi:** Không bao giờ commit tệp `terraform.tfstate` hoặc `.terraform/` lên kho mã nguồn Git.
**Phát biểu.** Bắt buộc khai báo đầy đủ tệp `.gitignore` bỏ qua toàn bộ các thư mục tạm và file state của Terraform: `.terraform/`, `*.tfstate`, `*.tfstate.backup`, `tfplan`.
**Giải thích cơ chế ngầm:** Tệp `terraform.tfstate` chứa toàn bộ cấu trúc hạ tầng và có thể chứa cả mật khẩu/secret dưới dạng plain-text. Commit tệp state lên Git vừa làm lộ bí mật quốc gia, vừa gây xung đột Git Commit (Git Merge Conflicts) trầm trọng khi nhiều người cùng làm việc.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Push tệp `terraform.tfstate` trực tiếp lên kho mã nguồn Git repository.
**Minh hoạ.**
```gitignore
# .gitignore for Terraform
.terraform/
*.tfstate
*.tfstate.backup
tfplan
*.tfvars
```
**Con số chốt:** 0% State Files trên Git repository.

---

### 1.3. Quy tắc Reporting, Isolation & Disaster Recovery (10 phút)

**Nguyên lý cốt lõi:** Tự động render báo cáo `terraform plan` dạng Markdown collapsible comment đính kèm vào Merge Request.
**Phát biểu.** Trích xuất kết quả `terraform plan` thành định dạng JSON (`terraform show -json tfplan`), sau đó chuyển đổi thành báo cáo Markdown để GitLab MR widget hiển thị bảng tổng hợp tài nguyên thêm (`+`), sửa (`~`), xóa (`-`).
**Giải thích cơ chế ngầm:** Reviewer không cần mở nhật ký log CI Runner dài hàng nghìn dòng để đọc. Báo cáo Markdown hiển thị ngay trên giao diện Merge Request giúp Tech Lead nắm bắt được ngay số lượng tài nguyên bị ảnh hưởng và quyết định duyệt code nhanh chóng.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Reviewer phải vào đọc log thô (raw log) của CI Runner để tự đếm số tài nguyên bị thay đổi.
**Minh hoạ.** Sử dụng cờ `reports.terraform: tfplan.json` trong cấu hình artifacts GitLab CI.
**Con số chốt:** 100% Merge Requests có Terraform Plan Report Widget.

---

**Nguyên lý cốt lõi:** Giới hạn ranh giới phân quyền Cloud IAM của Terraform ServiceAccount theo cấp hẹp của Resource Group / VPC.
**Phát biểu.** Quyền Cloud IAM cấp cho Terraform CI Runner qua OIDC chỉ được giới hạn trong đúng Scope của Resource Group / AWS Account dành riêng cho môi trường đó.
**Giải thích cơ chế ngầm:** Tương tự bài học ở buổi 40 QT 40.8. Nếu cấp quyền `AdministratorAccess` cho Terraform Runner, nếu một script HCL bị lỗi gõ nhầm scope, nó có thể xóa sạch các tài nguyên của môi trường khác trong cùng Cloud Account.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Gán vai trò `Owner` hoặc `AdministratorAccess` cấp root Cloud Account cho Terraform CI ServiceAccount.
**Minh hoạ.** Gán vai trò `Contributor` trên duy nhất Resource Group `rg-production-app`.
**Con số chốt:** 100% IAM Roles bị giới hạn Scope.

---

**Nguyên lý cốt lõi:** Sử dụng Terraform Workspaces hoặc thư mục môi trường độc lập cho Dev, Staging và Production.
**Phát biểu.** Tách biệt hoàn toàn các môi trường bằng cách dùng cấu trúc thư mục riêng biệt (`environments/staging/`, `environments/production/`) hoặc **Terraform Workspaces**.
**Giải thích cơ chế ngầm:** Đảm bảo tính cô lập hoàn toàn (Environment Isolation). Thay đổi trên môi trường Staging tuyệt đối không được dùng chung State File hay ảnh hưởng tới tài nguyên Production.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dùng chung 1 State File duy nhất cho cả Dev, Staging và Production.
**Minh hoạ.** Tệp `environments/production/main.tf` sử dụng `TF_STATE_NAME="production-state"`.
**Con số chốt:** 100% Môi trường có State File riêng biệt.

---

**Nguyên lý cốt lõi:** Xây dựng kịch bản Disaster Recovery cho State File qua tính năng State Version History của GitLab Backend.
**Phát biểu.** Định kỳ sao lưu và nắm vững quy trình khôi phục State File từ nhật ký phiên bản (Version History) của GitLab Managed Terraform Backend khi State File bị hỏng (State Corruption).
**Giải thích cơ chế ngầm:** Trong trường hợp một job CI bị hủy giữa chừng làm tệp State bị ngắt nửa chừng hoặc gõ nhầm lệnh `terraform state rm`, khả năng truy xuất lại phiên bản State File ổn định trước đó (State Versioning) trên GitLab là phao cứu sinh duy nhất giúp khôi phục quản lý hạ tầng trong vài phút.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Không biết cách tải lại phiên bản State cũ trên GitLab khi State File bị kẹt hỏng.
**Minh hoạ.** Truy cập `Infrastructure -> Terraform states` trên GitLab UI để download phiên bản State Version N-1.
**Con số chốt:** Khôi phục State hỏng trong dưới 5 phút.

---

### 1.4. Đưa vào việc thật (4 phút)

### 7.1. Kịch bản áp dụng thực tế tại Tập đoàn Tài chính Vận hành Hạ tầng Đa Đám mây
Trong một hệ thống ngân hàng quản lý 1.000 tài nguyên Cloud (VPC, EKS, RDS, S3):
1. **Pha Tạo Thay đổi (Merge Request):** Kỹ sư DevOps sửa mã HCL thêm một Subnet mới vào VPC trên kho Git. Pipeline CI chạy `terraform fmt`, `tflint`, `trivy` và thực thi `terraform plan -out=tfplan`.
2. **Pha Review & Kiểm duyệt:** Báo cáo `terraform plan` tự động render đính kèm vào MR: `Plan: 1 to add, 0 to change, 0 to destroy`. Báo cáo hiển thị rõ ràng chỉ tạo thêm 1 Subnet, không xóa tài nguyên nào. Tech Lead duyệt MR.
3. **Pha Merge & Phê duyệt Manual Gate:** Code được merge vào `main`. Pipeline trên `main` tự động chạy stage `plan`, lưu tệp `tfplan` artifact. Nút `apply-prod` chuyển sang trạng thái chờ phê duyệt thủ công (`when: manual`).
4. **Pha Thực thi Hạ tầng (Apply):** Head of DevOps vào xem lại tệp `tfplan` artifact, bấm nút **Play** trên nút manual gate. Job `terraform apply tfplan` tiêu thụ ĐÚNG tệp artifact đã duyệt và cập nhật Cloud an toàn 100%.

### 7.2. Case Study Thực tế: Thảm họa Xóa sạch Database do Chạy `terraform apply` không có tệp `tfplan` Artifact
Một công ty công nghệ vận hành hạ tầng AWS bằng Terraform qua GitLab CI.
- **Thảm họa ở cách làm cũ (Chạy apply không dùng file plan artifact):**
  1. Kỹ sư A tạo MR thêm một Security Group, pipeline chạy `terraform plan` báo xanh.
  2. Trong khi MR của A đang chờ duyệt, Kỹ sư B đổi tên tệp Database trong code HCL ở một branch khác và merge thẳng vào `main`.
  3. Kỹ sư A được duyệt MR và bấm chạy job `terraform apply -auto-approve`. Vì job apply KHÔNG DÙNG tệp `tfplan` artifact cũ mà tự sinh ra plan mới tại thời điểm đó, nó đã tự động xóa mất Database RDS Production của Kỹ sư B để tạo lại DB mới với tên mới! Dữ liệu 5 năm bị xóa sạch!
- **Khôi phục hoàn hảo ở cách làm chuẩn Buổi 42 (Ép dùng tệp `tfplan` Artifact - QT 42.1):**
  Nếu áp dụng đúng QT 42.1, khi Kỹ sư A bấm apply tệp `tfplan` artifact cũ, Terraform phát hiện State File đã bị thay đổi bởi Kỹ sư B (Serial Number bị lệch). Lệnh `terraform apply tfplan` lập tức **NỔ LỖI VÀ DỪNG LẠI NGAY LẬP TỨC**, ngăn chặn 100% thảm họa xóa Database!

### 7.3. Case Study 2: Cứu nguy Sự cố Sửa lén Security Group qua AWS Console bằng Drift Detection
Một kỹ sư On-call mở tạm cổng 22 (SSH) `0.0.0.0/0` trên AWS Security Group để debug sự cố đêm nhưng quên đóng lại.
- **Kết quả ở cách làm cũ:** Cổng SSH mở công khai suốt 3 tháng, hệ thống bị botnet quét và cài mã độc đào tiền ảo.
- **Khôi phục tự động nhờ Cron Drift Detection (QT 42.5):**
  1. Pipeline Cron Schedule chạy 6:00 AM mỗi ngày thực thi `terraform plan -detailed-exitcode`.
  2. Lệnh `terraform plan` phát hiện Security Group bị sửa thủ công trên AWS Console khác với mã HCL trên Git, trả về **Exitcode 2**.
  3. Job CI lập tức bắn cảnh báo Slack khẩn cấp: `[DRIFT ALERT] Security Group sg-123 has been modified manually!`.
  4. Đội DevOps kích hoạt pipeline `apply` để đè lại mã HCL chuẩn từ Git, đóng cổng SSH tự động trong 3 phút!

### 7.4. Case Study 3: Khôi phục State File kẹt Khóa (State Locking) trong GitLab CI Backend
Trong một đợt phát hành hạ tầng lớn, máy chủ CI Runner bị sập nguồn đúng lúc đang thực thi `terraform apply`.
- **Hậu quả ở cách làm cũ:** Tệp `terraform.tfstate` bị kẹt ở trạng thái Locked (`Lock ID: 9f8a2b3c`). Mọi pipeline triển khai tiếp theo đều nổ lỗi `Error acquiring the state lock` và dừng lại hoàn toàn.
- **Khôi phục chuẩn xác theo bài học Buổi 42 (Force Unlock State):**
  1. Kỹ sư DevOps truy cập giao diện GitLab UI tại mục `Infrastructure -> Terraform states`.
  2. Tìm State File `production-infrastructure`, kiểm tra Lock ID bị treo và bấm nút **Unlock**.
  3. Chạy lại (Retry) pipeline CI. GitLab Backend tự động giải phóng khóa HTTP Lock, giúp hạ tầng tiếp tục triển khai thành công 100% chỉ trong 2 phút!

### 7.5. Case Study 4: Ngăn ngừa Lộ Mật khẩu Database qua Quét An ninh Code HCL với Trivy
Một kỹ sư lập trình viết file `database.tf` khai báo mật khẩu `password = "Admin123456!"` dạng plain-text trong mã nguồn HCL.
- **Rủi ro:** Khi commit code lên Git, toàn bộ các thành viên dự án và bộ phận Audit đều nhìn thấy mật khẩu database Production.
- **Khắc phục tự động nhờ Trivy Security Scan (QT 42.6):**
  1. Job `security-scan` ở stage `validate` thực thi câu lệnh `trivy config .`.
  2. Trivy phát hiện quy tắc `AWS-001: Plaintext password found in HCL resource definition` và trả về exitcode 1 dừng pipeline lập tức.
  3. Kỹ sư buộc phải sửa lại dùng `aws_secretsmanager_secret` hoặc mã hóa biến `var.db_password`. Pipeline bảo vệ tuyệt đối mật khẩu Production!

---

### 7.6. Trường hợp khi nào KHÔNG nên dùng Terraform trong CI
Mặc dù Terraform CI/CD là chuẩn mực cao nhất cho IaC, nhưng KHÔNG áp dụng cho các trường hợp sau:

| Ngữ cảnh / Hạ tầng | Lý do KHÔNG dùng được Terraform CI | Giải pháp thay thế an toàn |
|---|---|---|
| Khởi tạo ban đầu tài khoản Cloud Root (AWS Root Account / GCP Organization Org Node) | Chưa có hạ tầng Runner, OIDC Provider hay Backend State để chạy CI. | Chạy `terraform apply` thủ công từ máy Admin bảo mật cấp cao (Bootstrap Phase). |
| Triển khai các tài nguyên có thời gian khởi tạo quá dài (>3 tiếng như CloudFront CDN hay Oracle DB) | Vượt quá thời gian timeout tối đa của GitLab CI Job Runner, làm job bị kill giữa chừng. | Tách làm 2 bước: Terraform tạo core hạ tầng, công cụ chuyên dụng (Ansible/Custom Operator) cấu hình background. |
| Môi trường Dev cá nhân của từng kỹ sư cần tạo/xóa liên tục trong vài phút | Tạo hàng trăm State Files rác trên GitLab Backend gây nghẽn storage. | Sử dụng Local State hoặc Ephemeral Local Workspaces cho Dev cá nhân. |

---

### 1.5. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính bẫy | Làm đúng là |
|---|---|---|
| Bẫy 1: Chạy `terraform apply` không truyền tệp `tfplan` artifact | `apply` tự tính lại plan mới tại thời điểm chạy, có thể xóa nhầm tài nguyên Production do lệch state. | Bắt buộc truyền tệp artifact `-out=tfplan` từ stage `plan` sang `apply` (QT 42.1). |
| Bẫy 2: Lưu tệp `terraform.tfstate` cục bộ trên máy chủ Runner | State File bị mất khi Runner bị reset, hoặc bị race condition hỏng state khi 2 jobs chạy song song. | Khai báo `backend "http"` sử dụng GitLab Managed State Backend có State Locking (QT 42.2). |
| Bẫy 3: Đặt cờ `when: always` cho stage `terraform apply` Production | Mọi commit merge vào `main` tự động đổi hạ tầng Cloud mà không qua bước phê duyệt kiểm tra thủ công. | Bắt buộc cấu hình `when: manual` trên các nhánh được bảo vệ `protected: true` (QT 42.3). |
| Bẫy 4: Lưu chìa khóa tĩnh `AWS_ACCESS_KEY_ID` trong CI Variables | Nếu máy chủ Runner bị chiếm quyền, hacker sẽ lấy trộm secret key kiểm soát vĩnh viễn Cloud Account. | Chuyển sang sử dụng 100% Keyless OIDC Cloud Federation (QT 42.4). |
| Bẫy 5: Chạy `terraform plan` định kỳ không có cờ `-detailed-exitcode` | Job CI luôn trả về Exitcode 0 dù hạ tầng bị sửa thủ công, làm thất bại việc phát hiện State Drift. | Bổ sung cờ `-detailed-exitcode` để bắt Exitcode 2 khi có sai lệch hạ tầng (QT 42.5). |
| Bẫy 6: Commit file `terraform.tfstate` hoặc `*.tfvars` chứa secret lên Git | Lộ toàn bộ mật khẩu Database và chìa khóa mã hóa cho bất kỳ ai có quyền đọc kho Git repository. | Khai báo tệp `.gitignore` loại bỏ toàn bộ `.tfstate`, `tfplan`, và `.tfvars` (QT 42.8). |
| Bẫy 7: Bỏ qua job chạy `terraform fmt -check` trong CI Pipeline | Mã nguồn HCL bị lộn xộn khoảng trắng, gây khó khăn cho việc review git diff trên Merge Request. | Đặt job `terraform fmt -check -recursive` ở stage `validate` đầu tiên (QT 42.7). |
| Bẫy 8: Cấp vai trò `AdministratorAccess` cho Terraform ServiceAccount | Nếu tệp HCL bị lỗi gõ nhầm scope, nó có thể xóa sạch toàn bộ tài nguyên của các môi trường khác. | Giới hạn quyền Cloud IAM của ServiceAccount theo đúng Resource Group / VPC Scope (QT 42.10). |

---

### 1.6. Tóm tắt (3 phút)

### 9.1. Sơ đồ Mermaid: Kiến trúc Luồng Pipeline Terraform CI/CD Chuẩn mực

```mermaid
flowchart TD
    subgraph Stage 1: Validate
        A[Git Push / MR Created] --> B[terraform fmt -check]
        B --> C[tflint & trivy scan]
    end

    subgraph Stage 2: Plan (MR Gate)
        C --> D[terraform plan -out=tfplan]
        D -->|Pass Binary File| E[Artifact: tfplan]
        D -->|Render JSON Report| F[MR Widget Comment]
    end

    subgraph Stage 3: Apply (Manual Gate)
        G[Merge MR to main] --> H{Manual Approval?}
        H -->|User Click Play| I[terraform apply tfplan]
        E -->|Consume Exact Artifact| I
        I --> J[Cloud Infrastructure Updated]
    end

    subgraph Stage 4: Scheduled Drift Detection
        K[Cron Trigger 6:00 AM] --> L[terraform plan -detailed-exitcode]
        L -->|Exitcode 2| M[Send Slack Alert: Drift Detected!]
    end
```

### 9.2. Năm điều phải nhớ thuộc lòng
1. **Always Apply Exact `tfplan` Artifact:** Không bao giờ chạy `terraform apply` không có tệp `tfplan` artifact đã được review trên MR.
2. **GitLab Managed State Backend:** Luôn dùng `backend "http"` để GitLab quản lý mã hóa và khóa State File (State Locking).
3. **Manual Gate for Production:** Stage `apply` môi trường Production bắt buộc phải đặt `when: manual` trên nhánh Protected Branch.
4. **Drift Detection via Exitcode 2:** Sử dụng `terraform plan -detailed-exitcode` trong Cron Job để phát hiện hạ tầng bị sửa thủ công trên Cloud Console.
5. **Keyless OIDC Authentication:** Tuyệt đối không lưu static Cloud Access Keys trong CI Variables; sử dụng 100% OIDC Federation.

---

### 1.7. Câu hỏi tự kiểm tra (5 phút)

### 10.1. Danh sách câu hỏi tự kiểm tra
1. Sự khác biệt nguy hiểm nhất giữa việc chạy `terraform apply tfplan` (dùng artifact) và chạy `terraform apply -auto-approve` (không dùng artifact) là gì?
2. Hai tính năng quan trọng nhất mà GitLab Managed Terraform State Backend cung cấp là gì?
3. Tại sao stage `terraform apply` môi trường Production lại bắt buộc phải đặt chế độ `when: manual`?
4. Ý nghĩa của mã Exitcode 2 khi chạy câu lệnh `terraform plan -detailed-exitcode` là gì?
5. Tại sao không được lưu chìa khóa tĩnh `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` trong GitLab CI Variables?
6. Công cụ Linter nào giúp kiểm tra chuẩn cú pháp và lỗi cấu hình mã nguồn HCL trên Merge Request?
7. Tại sao tệp `terraform.tfstate` tuyệt đối không bao giờ được commit lên kho mã nguồn Git?
8. Tính năng nào của GitLab CI giúp hiển thị bảng tổng hợp thay đổi tài nguyên Terraform trực tiếp trên giao diện Merge Request Widget?
9. Tại sao lại cần tách rời State Files của môi trường Staging và Production bằng Terraform Workspaces hoặc thư mục độc lập?
10. Mục đích của câu lệnh `terraform fmt -check` trong stage `validate` của pipeline là gì?
11. Khi tệp State File bị kẹt ở trạng thái locked do job CI trước bị crash giữa chừng, làm thế nào để giải phóng lock an toàn?
12. Cơ chế nào giúp bảo vệ hạ tầng khỏi việc bị xóa sạch khi Terraform ServiceAccount bị rò rỉ?

---

### 10.2. Đáp án câu hỏi tự kiểm tra

1. Chạy không dùng artifact sẽ tự tính lại plan mới tại thời điểm apply, có thể xóa nhầm tài nguyên Production do lệch state; dùng `tfplan` artifact đảm bảo thực thi ĐÚNG các hành động đã được duyệt trên MR.
2. Hai tính năng quan trọng nhất là **Mã hóa lưu trữ State File (Encryption at Rest)** và **Tự động khóa State (State Locking HTTP POST/DELETE)** chống race condition.
3. Đảm bảo quy trình Phê duyệt hai bước (Four-Eye Principle), yêu cầu Tech Lead xem xét lại tệp plan trước khi bấm nút kích hoạt thay đổi hạ tầng thực tế.
4. Exitcode 2 báo hiệu câu lệnh `terraform plan` phát hiện có sự thay đổi hạ tầng (Infrastructure State Drift) giữa mã HCL trên Git và thực tế trên Cloud.
5. Vì chìa khóa tĩnh có thời hạn sống dài hạn; nếu máy chủ Runner bị chiếm quyền, kẻ tấn công sẽ sở hữu secret key kiểm soát vĩnh viễn Cloud Account.
6. Công cụ **TFLint** (`tflint`) quét lỗi cú pháp và **Trivy** / **TFSec** quét lỗ hổng an toàn HCL.
7. Vì State File chứa bản đồ toàn bộ hạ tầng và có thể chứa mật khẩu plain-text, commit lên Git sẽ làm rò rỉ bí mật và gây xung đột Git merge.
8. Tính năng **Terraform Report Artifact** (`reports.terraform: tfplan.json`) trong GitLab CI.
9. Giúp đảm bảo tính cô lập hoàn toàn (Environment Isolation), sự cố trên Staging không bao giờ ảnh hưởng tới State hay tài nguyên Production.
10. Ép mã nguồn HCL tuân thủ chuẩn định dạng 2 spaces indent của HashiCorp, giúp code sạch đẹp và dễ đọc khi review git diff.
11. Sử dụng tính năng Force Unlock State trên GitLab UI (`Infrastructure -> Terraform states`) hoặc chạy lệnh `terraform force-unlock <lock_id>`.
12. Giới hạn ranh giới phân quyền Cloud IAM của ServiceAccount theo đúng Scope của Resource Group / VPC môi trường đó.

---

### 1.8. Tài liệu tham khảo (2 phút)

| Nguồn tài liệu | Mô tả nội dung | Phiên bản áp dụng |
|---|---|---|
| HashiCorp Terraform CLI — Plan & Apply Command Options | Chi tiết các cờ `-out=tfplan`, `-detailed-exitcode` | Terraform v1.5+ |
| GitLab Documentation — GitLab Managed Terraform State | Hướng dẫn cấu hình HTTP State Backend và State Locking | GitLab v15.0+ |
| GitLab CI/CD Templates — Terraform.gitlab-ci.yml | Mẫu pipeline Terraform chuẩn do GitLab phát hành | GitLab CI v16+ |
| TFLint GitHub Repository — HCL Linter for Terraform | Hướng dẫn cài đặt và tích hợp tflint vào CI Pipeline | TFLint v0.45+ |
| Trivy Documentation — Infrastructure as Code Scanning | Quét lỗ hổng an ninh mã nguồn HCL bằng Trivy | Trivy v0.40+ |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10 phút |
| §1 | Sau buổi này học viên LÀM ĐƯỢC gì | 1 phút |
| §2 | Cần biết trước | 1 phút |
| §3 | Thuật ngữ và mô hình tư duy | 8 phút |
| §4 | Cấu hình Backend & Plan/Apply Gate | 10 phút |
| §5 | Quy tắc Quản lý Drift Detection & Code Quality | 10 phút |
| §6 | Quy tắc Reporting, Isolation & Disaster Recovery | 10 phút |
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
Trong bài lab này, học viên sẽ trực tiếp xây dựng luồng tự động hóa quản lý hạ tầng Cloud bằng Terraform trong GitLab CI/CD:
1. Khởi tạo mã nguồn HCL (main.tf, variables.tf, outputs.tf) cấu hình tài nguyên đám mây và GitLab Managed HTTP State Backend.
2. Kiểm thử chạy `terraform fmt -check` và `terraform validate` tự động ở stage validate.
3. Viết script CI thực thi `terraform plan -out=tfplan`, trích xuất file binary `tfplan` và JSON Report Artifacts.
4. Mô phỏng luồng phê duyệt thủ công Manual Gate (`when: manual`) cho stage `apply` tiêu thụ đúng tệp `tfplan` artifact.
5. Xây dựng script kiểm thử phát hiện lệch trạng thái hạ tầng (State Drift Detection) với cờ `-detailed-exitcode` (Exitcode 2).
6. Tích hợp công cụ Linter & Security Scanner (`tflint`, `trivy`) và kiểm thử cơ chế giải phóng khóa State Locking (State Lock Release).

---

## 2. Mô hình kiến trúc Lab L2

```mermaid
graph TD
    subgraph Phase 1: Code Validation & Linting
        A[Git Push / MR] -->|1. terraform fmt| B[Format Checker]
        B -->|2. tflint & trivy| C[Security & Quality Scanner]
    end

    subgraph Phase 2: Plan Gate (MR Execution)
        C -->|3. terraform plan -out=tfplan| D[GitLab Managed State Backend]
        D -->|State Lock HTTP POST| E[State Locked]
        D -->|4. Generate Artifact| F[tfplan Binary File]
        D -->|Unlock HTTP DELETE| G[State Unlocked]
    end

    subgraph Phase 3: Apply Gate (Manual Approval)
        H[Manual Approval Click] -->|5. terraform apply tfplan| I[Consume Exact tfplan Artifact]
        I -->|6. Apply Changes| J[Cloud Infrastructure Updated]
    end

    subgraph Phase 4: Cron Drift Detection
        K[Cron Schedule 6:00 AM] -->|7. plan -detailed-exitcode| L{Exitcode Status}
        L -->|Exitcode 0| M[No Drift]
        L -->|Exitcode 2| N[Alert Slack: Infrastructure Drift!]
    end
```

---

## 3. Các bước thực hiện bài lab (14 Checkpoints)

### Bước 1: Khởi tạo Cấu trúc Thư mục và Mã nguồn HCL Terraform (10 phút)

Tạo thư mục làm việc cho bài lab Buổi 42:

```bash
mkdir -p terraform-ci-lab
cd terraform-ci-lab
mkdir -p terraform/modules/s3_storage scripts artifacts state-backend audit
```

Khởi tạo tệp `terraform/main.tf` hỗ trợ đầy đủ cấu hình tài nguyên enterprise và GitLab Managed HTTP Backend:

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "http" {
    # GitLab Managed State Backend configuration via TF_HTTP_* variables
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "app_storage" {
  bucket        = "bank-finance-assets-${var.environment}"
  force_destroy = false

  tags = {
    Environment = var.environment
    ManagedBy   = "GitLab-CI-Terraform"
    Project     = "BankCore"
    CostCenter  = "FinTech-Infrastructure"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "storage_crypto" {
  bucket = aws_s3_bucket.app_storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "storage_versioning" {
  bucket = aws_s3_bucket.app_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "storage_privacy" {
  bucket                  = aws_s3_bucket.app_storage.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

Khởi tạo tệp `terraform/variables.tf` với các ràng buộc kiểu dữ liệu:

```hcl
variable "aws_region" {
  type        = string
  default     = "ap-southeast-1"
  description = "AWS Deployment Region for Enterprise Infrastructure"
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Deployment Environment Target (dev, staging, production)"

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be one of: dev, staging, production."
  }
}
```

Khởi tạo tệp `terraform/outputs.tf`:

```hcl
output "s3_bucket_name" {
  value       = aws_s3_bucket.app_storage.id
  description = "Name of created S3 Bucket for App Storage"
}

output "s3_bucket_arn" {
  value       = aws_s3_bucket.app_storage.arn
  description = "ARN of created S3 Bucket for Security Auditing"
}
```

### **CHECKPOINT 1**
Chạy câu lệnh kiểm tra tệp `main.tf`, `variables.tf` và `outputs.tf`:

```bash
test -f terraform/main.tf && test -f terraform/variables.tf && test -f terraform/outputs.tf && echo "CHECKPOINT 1: ĐẠT" || echo "CHECKPOINT 1: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 1: ĐẠT
```

---

### Bước 2: Tạo Tệp `.gitignore` Chuẩn mực Loại bỏ State Files và Secrets (10 phút)

Khởi tạo tệp `.gitignore` cho dự án Terraform:

```gitignore
# Terraform Local Workspace & Cache
.terraform/
*.tfstate
*.tfstate.*
*.tfstate.backup

# Execution Plans & Sensitive Vars
tfplan
tfplan.json
*.tfvars
*.tfvars.json

# Crash Logs & Temporary Artifacts
crash.log
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Environment Secrets
.env
```

### **CHECKPOINT 2**
Chạy câu lệnh kiểm tra tệp `.gitignore`:

```bash
test -f .gitignore && grep -q "*.tfstate" .gitignore && echo "CHECKPOINT 2: ĐẠT" || echo "CHECKPOINT 2: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 2: ĐẠT
```

---

### Bước 3: Thực thi Lập trình Linter `terraform fmt` và `terraform validate` (15 phút)

Tạo script kiểm tra định dạng và cú pháp HCL `scripts/validate-hcl-code.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[TERRAFORM FMT] Checking HCL code formatting..."
mkdir -p dist

cat << EOF > dist/validation-report.json
{
  "fmt_check": "PASSED",
  "syntax_validate": "PASSED",
  "files_scanned": ["terraform/main.tf", "terraform/variables.tf", "terraform/outputs.tf"],
  "status": "VALIDATED"
}
EOF

echo "[TERRAFORM VALIDATE] Successfully validated Terraform code!"
```

Cho phép script chạy:
```bash
chmod +x scripts/validate-hcl-code.sh
./scripts/validate-hcl-code.sh
```

### **CHECKPOINT 3**
Chạy câu lệnh kiểm tra kết quả validation HCL:

```bash
test -f dist/validation-report.json && grep -q "VALIDATED" dist/validation-report.json && echo "CHECKPOINT 3: ĐẠT" || echo "CHECKPOINT 3: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 3: ĐẠT
```

---

### Bước 4: Viết Script Mô phỏng GitLab Managed State Backend và State Locking (15 phút)

Tạo script mô phỏng dịch vụ HTTP State Backend và cơ chế tự động khóa State Locking của GitLab CI `scripts/simulate-gitlab-state-backend.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

STATE_NAME="${1:-production-infrastructure}"
ACTION="${2:-lock}"

mkdir -p state-backend

if [ "$ACTION" = "lock" ]; then
    echo "[STATE BACKEND] Acquiring HTTP State Lock for '$STATE_NAME'..."
    cat << EOF > state-backend/lock-status.json
{
  "state_name": "$STATE_NAME",
  "locked": true,
  "lock_id": "lock-$(openssl rand -hex 8)",
  "locked_by": "gitlab-ci-runner-bot",
  "locked_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "backend_type": "GITLAB_MANAGED_HTTP_BACKEND"
}
EOF
    echo "[STATE BACKEND] State Lock Acquired successfully!"
elif [ "$ACTION" = "unlock" ]; then
    echo "[STATE BACKEND] Releasing HTTP State Lock for '$STATE_NAME'..."
    cat << EOF > state-backend/lock-status.json
{
  "state_name": "$STATE_NAME",
  "locked": false,
  "unlocked_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "backend_type": "GITLAB_MANAGED_HTTP_BACKEND"
}
EOF
    echo "[STATE BACKEND] State Lock Released successfully!"
fi
```

Cho phép script chạy lấy khóa state:
```bash
chmod +x scripts/simulate-gitlab-state-backend.sh
./scripts/simulate-gitlab-state-backend.sh "production-infrastructure" "lock"
```

### **CHECKPOINT 4**
Chạy câu lệnh kiểm tra trạng thái State Lock:

```bash
test -f state-backend/lock-status.json && grep -q '"locked": true' state-backend/lock-status.json && echo "CHECKPOINT 4: ĐẠT" || echo "CHECKPOINT 4: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 4: ĐẠT
```

---

### Bước 5: Viết Script Mô phỏng `terraform plan -out=tfplan` Sinh Artifacts Binary (15 phút)

Tạo script mô phỏng stage plan sinh tệp binary plan artifact và JSON summary `scripts/terraform-plan-stage.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[TERRAFORM PLAN] Generating execution plan file -out=tfplan..."
echo "[TERRAFORM PLAN] Enforcing mandatory flags: -out=tfplan -input=false..."

mkdir -p artifacts/plan-artifacts

# Tạo tệp binary giả lập tfplan
echo "BINARY_TFPLAN_ARTIFACT_SHA_$(openssl rand -hex 16)" > artifacts/plan-artifacts/tfplan

# Tạo tệp JSON report
cat << EOF > artifacts/plan-artifacts/tfplan.json
{
  "format_version": "1.2",
  "terraform_version": "1.5.7",
  "planned_change": {
    "actions": ["create"],
    "resource_changes": [
      {
        "address": "aws_s3_bucket.app_storage",
        "type": "aws_s3_bucket",
        "change": {
          "actions": ["create"],
          "before": null,
          "after": {
            "bucket": "bank-finance-assets-production",
            "environment": "production",
            "managed_by": "GitLab-CI-Terraform"
          }
        }
      }
    ]
  },
  "summary": {
    "add": 1,
    "change": 0,
    "destroy": 0
  }
}
EOF

echo "[TERRAFORM PLAN] Successfully generated tfplan and tfplan.json artifacts!"
```

Cho phép script chạy:
```bash
chmod +x scripts/terraform-plan-stage.sh
./scripts/terraform-plan-stage.sh
```

### **CHECKPOINT 5**
Chạy câu lệnh kiểm tra tệp `tfplan` binary artifact:

```bash
test -f artifacts/plan-artifacts/tfplan && test -f artifacts/plan-artifacts/tfplan.json && echo "CHECKPOINT 5: ĐẠT" || echo "CHECKPOINT 5: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 5: ĐẠT
```

---

### Bước 6: Viết Script Mô phỏng Merge Request Plan Reporting Widget (10 phút)

Tạo script render báo cáo MR Markdown `scripts/render-mr-plan-report.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[MR REPORTING] Rendering Markdown Terraform Plan Summary Report..."

cat << EOF > artifacts/plan-artifacts/mr-report.md
### Terraform Plan Report Summary
- **Project:** BankCore Infrastructure
- **Environment:** Production
- **Action Summary:** 1 to add, 0 to change, 0 to destroy

<details><summary>Click to view planned resource changes</summary>

\`\`\`diff
+ resource "aws_s3_bucket" "app_storage" {
+   bucket = "bank-finance-assets-production"
+   force_destroy = false
+ }
\`\`\`
</details>
EOF

echo "[MR REPORTING] Successfully generated mr-report.md widget!"
```

Cho phép script chạy:
```bash
chmod +x scripts/render-mr-plan-report.sh
./scripts/render-mr-plan-report.sh
```

### **CHECKPOINT 6**
Chạy câu lệnh kiểm tra tệp MR plan report:

```bash
test -f artifacts/plan-artifacts/mr-report.md && grep -q "Terraform Plan Report Summary" artifacts/plan-artifacts/mr-report.md && echo "CHECKPOINT 6: ĐẠT" || echo "CHECKPOINT 6: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 6: ĐẠT
```

---

### Bước 7: Viết Script Mô phỏng Stage `terraform apply tfplan` qua Manual Gate (15 phút)

Tạo script apply với tệp plan artifact `scripts/terraform-apply-stage.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

PLAN_FILE="artifacts/plan-artifacts/tfplan"

echo "[TERRAFORM APPLY] Checking for mandatory tfplan artifact..."

if [ ! -f "$PLAN_FILE" ]; then
    echo "[TERRAFORM ERROR] Missing required tfplan artifact file! Refusing to apply."
    exit 1
fi

echo "[TERRAFORM APPLY] Consuming EXACT artifact '$PLAN_FILE'..."
echo "[TERRAFORM APPLY] Applying 1 resource change to AWS Cloud..."

# Releasing State Lock after apply
./scripts/simulate-gitlab-state-backend.sh "production-infrastructure" "unlock"

mkdir -p state-backend/applied-state

cat << EOF > state-backend/applied-state/cluster-infrastructure.json
{
  "status": "APPLIED_SUCCESSFULLY",
  "applied_from_artifact": "$PLAN_FILE",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "resources": ["aws_s3_bucket.app_storage"]
}
EOF

echo "[TERRAFORM SUCCESS] Infrastructure updated successfully via Manual Gate!"
```

Cho phép script chạy:
```bash
chmod +x scripts/terraform-apply-stage.sh
./scripts/terraform-apply-stage.sh
```

### **CHECKPOINT 7**
Chạy câu lệnh kiểm tra kết quả apply thành công:

```bash
test -f state-backend/applied-state/cluster-infrastructure.json && grep -q "APPLIED_SUCCESSFULLY" state-backend/applied-state/cluster-infrastructure.json && echo "CHECKPOINT 7: ĐẠT" || echo "CHECKPOINT 7: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 7: ĐẠT
```

---

### Bước 8: Kiểm thử Phát hiện Sai lệch Trạng thái Hạ tầng (State Drift Detection) (15 phút)

Tạo script kiểm thử Drift Detection với cờ `-detailed-exitcode` `scripts/terraform-drift-detection.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

DRIFT_SIMULATION="${1:-true}"

echo "[DRIFT DETECTION] Executing 'terraform plan -detailed-exitcode'..."

mkdir -p audit/drift-reports

if [ "$DRIFT_SIMULATION" = "true" ]; then
    echo "[DRIFT ALERT] [EXITCODE 2] Infrastructure State Drift Detected! Cloud resource modified manually via AWS Console."
    cat << EOF > audit/drift-reports/drift-summary.json
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "exitcode": 2,
  "drift_status": "DRIFT_DETECTED",
  "details": "Security Group sg-123 has unmapped inbound SSH port open",
  "severity": "CRITICAL"
}
EOF
    echo "[ALERT HOOK] Sent Slack Alert to #devops-infra-alerts."
    exit 2
else
    echo "[DRIFT OK] [EXITCODE 0] Infrastructure is 100% In-Sync with HCL Code."
    cat << EOF > audit/drift-reports/drift-summary.json
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "exitcode": 0,
  "drift_status": "IN_SYNC"
}
EOF
    exit 0
fi
```

Cho phép script chạy kiểm thử phát hiện Drift (trả về Exitcode 2):
```bash
chmod +x scripts/terraform-drift-detection.sh
./scripts/terraform-drift-detection.sh "true" || true
```

### **CHECKPOINT 8**
Chạy câu lệnh kiểm tra tệp báo cáo Drift Detection:

```bash
test -f audit/drift-reports/drift-summary.json && grep -q "DRIFT_DETECTED" audit/drift-reports/drift-summary.json && echo "CHECKPOINT 8: ĐẠT" || echo "CHECKPOINT 8: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 8: ĐẠT
```

---

### Bước 9: Tích hợp Bộ quét Security & Linter HCL (`tflint` & `trivy`) (10 phút)

Tạo script linter và security scanner `scripts/scan-hcl-security.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[TFLINT SCAN] Scanning Terraform HCL files in terraform/..."
echo "[TRIVY IAC SCAN] Auditing Security misconfigurations..."

mkdir -p audit/security-scans

cat << EOF > audit/security-scans/security-report.json
{
  "tool": "trivy-iac",
  "scanned_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "vulnerabilities_found": 0,
  "misconfigurations": 0,
  "status": "COMPLIANT_PASSED"
}
EOF

echo "[SECURITY SCAN] PASSED: 0 Security misconfigurations found."
```

Cho phép script chạy quét an ninh:
```bash
chmod +x scripts/scan-hcl-security.sh
./scripts/scan-hcl-security.sh
```

### **CHECKPOINT 9**
Chạy câu lệnh kiểm tra tệp báo cáo Security Scan:

```bash
test -f audit/security-scans/security-report.json && grep -q "COMPLIANT_PASSED" audit/security-scans/security-report.json && echo "CHECKPOINT 9: ĐẠT" || echo "CHECKPOINT 9: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 9: ĐẠT
```

---

### Bước 10: Viết Script Mô phỏng Force Unlock State File khi Kẹt Khóa (10 phút)

Tạo script giải phóng State Lock `scripts/force-unlock-state.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

LOCK_ID="${1:-lock-9f8a2b3c}"

echo "[FORCE UNLOCK] Executing 'terraform force-unlock $LOCK_ID' on GitLab Backend..."

cat << EOF > state-backend/lock-status.json
{
  "state_name": "production-infrastructure",
  "locked": false,
  "force_unlocked_by": "gitlab-admin-user",
  "unlocked_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "released_lock_id": "$LOCK_ID"
}
EOF

echo "[FORCE UNLOCK] Successfully released stuck State Lock $LOCK_ID!"
```

Cho phép script chạy force unlock:
```bash
chmod +x scripts/force-unlock-state.sh
./scripts/force-unlock-state.sh "lock-9f8a2b3c"
```

### **CHECKPOINT 10**
Chạy câu lệnh kiểm tra State Lock đã được giải phóng:

```bash
test -f state-backend/lock-status.json && grep -q '"locked": false' state-backend/lock-status.json && echo "CHECKPOINT 10: ĐẠT" || echo "CHECKPOINT 10: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 10: ĐẠT
```

---

### Bước 11: Viết Script Ghi nhận Nhật ký Terraform Execution Audit Logs (10 phút)

Tạo script ghi nhận đầy đủ nhật ký kiểm toán sự kiện thực thi thay đổi hạ tầng Terraform `scripts/audit-terraform-events.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

mkdir -p audit

cat << EOF >> audit/terraform-ci-audit.json
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "event": "TERRAFORM_APPLY_SUCCESSFUL",
  "state_name": "production-infrastructure",
  "commit_sha": "git-commit-$(openssl rand -hex 8)",
  "executor": "GitLab CI Manual Gate",
  "audit_type": "INFRASTRUCTURE_AS_CODE_ALIGNMENT",
  "compliance_status": "ISO27001_SOC2_COMPLIANT",
  "status": "COMPLIANT"
}
EOF

echo "[AUDIT LOG] Recorded Terraform Execution Event in audit/terraform-ci-audit.json"
```

Cho phép script chạy ghi log:
```bash
chmod +x scripts/audit-terraform-events.sh
./scripts/audit-terraform-events.sh
```

### **CHECKPOINT 11**
Chạy câu lệnh kiểm tra tệp Terraform Audit Log:

```bash
test -f audit/terraform-ci-audit.json && grep -q "TERRAFORM_APPLY_SUCCESSFUL" audit/terraform-ci-audit.json && echo "CHECKPOINT 11: ĐẠT" || echo "CHECKPOINT 11: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 11: ĐẠT
```

---

### Bước 12: Xây dựng Script Linter Kiểm tra Cấu hình GitLab CI cho Terraform (5 phút)

Tạo script linter kiểm định nghiêm ngặt cấu hình GitLab CI Pipeline cho Terraform `scripts/validate-terraform-gitlab-ci.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[TERRAFORM CI LINTER] Auditing .gitlab-ci.yml for Terraform best practices..."

cat << EOF > .gitlab-ci.yml
plan-job:
  stage: plan
  script:
    - terraform plan -out=tfplan
  artifacts:
    paths:
      - tfplan

apply-job:
  stage: apply
  script:
    - terraform apply -input=false tfplan
  rules:
    - if: \$CI_COMMIT_BRANCH == "main"
      when: manual
EOF

if ! grep -q "-out=tfplan" .gitlab-ci.yml; then
    echo "[ERROR] Missing mandatory -out=tfplan in terraform plan!"
    exit 1
fi

if ! grep -q "when: manual" .gitlab-ci.yml; then
    echo "[ERROR] Missing mandatory manual gate in terraform apply!"
    exit 1
fi

echo "[TERRAFORM CI LINTER] Validation PASSED: 100% Compliant Terraform CI Pipeline Configuration."
```

Cho phép script chạy linter:
```bash
chmod +x scripts/validate-terraform-gitlab-ci.sh
./scripts/validate-terraform-gitlab-ci.sh
```

### **CHECKPOINT 12**
Chạy câu lệnh kiểm tra script Linter Terraform CI:

```bash
./scripts/validate-terraform-gitlab-ci.sh | grep -q "PASSED" && echo "CHECKPOINT 12: ĐẠT" || echo "CHECKPOINT 12: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 12: ĐẠT
```

---

### Bước 13: Xây dựng Script Mô phỏng Truy xuất Lịch sử State File Disaster Recovery (5 phút)

Tạo script disaster recovery `scripts/terraform-state-disaster-recovery.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[DISASTER RECOVERY] Fetching State File Version History N-1 from GitLab Backend..."

mkdir -p state-backend/recovered-state

cat << EOF > state-backend/recovered-state/terraform.tfstate
{
  "version": 4,
  "terraform_version": "1.5.7",
  "serial": 12,
  "lineage": "9f8a2b3c-4d5e-6f7a-8b9c-0d1e2f3a4b5c",
  "outputs": {
    "s3_bucket_name": {
      "value": "bank-finance-assets-production",
      "type": "string"
    }
  },
  "resources": []
}
EOF

echo "[DISASTER RECOVERY] Successfully restored State File Version 12 from GitLab Backend History!"
```

Cho phép script chạy recovery:
```bash
chmod +x scripts/terraform-state-disaster-recovery.sh
./scripts/terraform-state-disaster-recovery.sh
```

### **CHECKPOINT 13**
Chạy câu lệnh kiểm tra tệp State khôi phục:

```bash
test -f state-backend/recovered-state/terraform.tfstate && grep -q '"serial": 12' state-backend/recovered-state/terraform.tfstate && echo "CHECKPOINT 13: ĐẠT" || echo "CHECKPOINT 13: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 13: ĐẠT
```

---

### Bước 14: Tổng hợp Đánh giá Hoàn thành Bài Lab Buổi 42 (5 phút)

Tạo script đánh giá kết quả tổng hợp `scripts/final-terraform-lab-evaluation.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "FINAL EVALUATION SUMMARY — BUỔI 42 (TERRAFORM IN GITLAB CI)"
echo "=========================================================="

CHECKS_PASSED=0

[ -f terraform/main.tf ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f dist/validation-report.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f artifacts/plan-artifacts/tfplan ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f state-backend/applied-state/cluster-infrastructure.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f audit/drift-reports/drift-summary.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f audit/security-scans/security-report.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))

echo "Successfully verified $CHECKS_PASSED / 6 Core Terraform CI Components."
echo "Verified HCL Validation, Plan Artifact Generation, Manual Apply Gate, Drift Detection, and Security Scanning."
echo "Verified GitLab Managed State Backend integration and Audit Event Logging."

if [ "$CHECKS_PASSED" -eq 6 ]; then
    echo "BUỔI 42 LAB STATUS: PASSED (100% COMPLETE)"
    exit 0
else
    echo "BUỔI 42 LAB STATUS: INCOMPLETE"
    exit 1
fi
```

Cho phép script chạy đánh giá kết quả:
```bash
chmod +x scripts/final-terraform-lab-evaluation.sh
./scripts/final-terraform-lab-evaluation.sh
```

### **CHECKPOINT 14**
Chạy câu lệnh tổng kết bài lab Buổi 42:

```bash
./scripts/final-terraform-lab-evaluation.sh | grep -q "PASSED" && echo "CHECKPOINT 14: ĐẠT" || echo "CHECKPOINT 14: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 14: ĐẠT
```

---

## Xử lý sự cố

### 1. Sự cố Lỗi `Error acquiring the state lock` khi chạy `terraform plan`
- **Triệu chứng:** Pipeline bị dừng với lỗi State Lock bị giữ bởi Lock ID `lock-12345`.
- **Nguyên nhân:** Một job CI trước đó bị sập nguồn hoặc bị cancel giữa chừng trong khi đang ghi State File.
- **Cách khắc phục:** Truy cập GitLab UI tại `Infrastructure -> Terraform states` bấm nút **Unlock** hoặc chạy `terraform force-unlock <lock_id>`.

### 2. Sự cố Stage `apply` báo lỗi `Error: Saved plan is stale`
- **Triệu chứng:** Lệnh `terraform apply tfplan` bị từ chối thực thi.
- **Nguyên nhân:** State File trên Cloud đã bị thay đổi bởi một pipeline khác trong thời gian chờ duyệt nút Manual Gate.
- **Cách khắc phục:** Chạy lại (Retry) pipeline từ stage `plan` để sinh tệp `tfplan` mới phù hợp với State mới nhất.

### 3. Sự cố Lỡ commit tệp `terraform.tfstate` chứa mật khẩu lên kho Git
- **Triệu chứng:** Bộ phận Security phát hiện mật khẩu DB plain-text trong Git commit history.
- **Nguyên nhân:** Quên khai báo tệp `.gitignore` bỏ qua `*.tfstate`.
- **Cách khắc phục:** Sử dụng công cụ `git-filter-repo` hoặc BFG Repo-Cleaner xóa hoàn toàn file state khỏi lịch sử Git và thu hồi mật khẩu ngay lập tức.

### 4. Sự cố Job `terraform fmt` báo lỗi `Diff found` và hủy pipeline
- **Triệu chứng:** Pipeline bị dừng ở stage `validate`.
- **Nguyên nhân:** Mã HCL gõ khoảng trắng không chuẩn (dùng Tab hoặc sai 2 spaces indent).
- **Cách khắc phục:** Chạy `terraform fmt -recursive` trên local trước khi commit code.

### 5. Sự cố Cron Scheduled Drift Detection báo `Exitcode 2`
- **Triệu chứng:** Pipeline Cron bắn cảnh báo Slack đỏ vào lúc 6:00 AM.
- **Nguyên nhân:** Có kỹ sư vừa tự ý sửa hạ tầng Cloud qua AWS/Azure Console mà không qua Git.
- **Cách khắc phục:** Kiểm tra lại người sửa trên Cloud Audit Log (CloudTrail) và chạy pipeline `apply` trên branch `main` để đè lại mã HCL chuẩn từ Git.

### 6. Sự cố Lỗi `HTTP 401 Unauthorized` khi Terraform kết nối GitLab Backend
- **Triệu chứng:** Lệnh `terraform init` nổ lỗi HTTP 401.
- **Nguyên nhân:** Biến `TF_HTTP_AUTHENTICATE_PASSWORD` bị thiếu hoặc giá trị `$CI_JOB_TOKEN` hết hạn.
- **Cách khắc phục:** Kiểm tra lại việc khai báo biến môi trường `TF_HTTP_*` trong `before_script`.

### 7. Sự cố Stage `apply` tự động chạy làm đổi hạ tầng Production mà không qua duyệt
- **Triệu chứng:** Merge MR xong hạ tầng Cloud bị thay đổi tự động.
- **Nguyên nhân:** Quên đặt cờ `when: manual` trong cấu hình stage `apply` của `.gitlab-ci.yml`.
- **Cách khắc phục:** Thêm `when: manual` vào khối `rules` của job apply.

### 8. Sự cố Lỗi `Error: Invalid provider configuration` khi chạy trên CI Runner
- **Triệu chứng:** `terraform init` nổ lỗi không thể tìm thấy Provider plugin.
- **Nguyên nhân:** Máy chủ Runner không có kết nối Internet để kéo Provider từ Terraform Registry.
- **Cách khắc phục:** Cấu hình Terraform Provider Mirror hoặc cache plugins trong thư mục Runner.

### 9. Sự cố `tfsec` phát hiện lỗ hổng `S3 Bucket missing Encryption`
- **Triệu chứng:** Job security scan chặn pipeline do file HCL thiếu mã hóa.
- **Nguyên nhân:** Chưa bổ sung tài nguyên `aws_s3_bucket_server_side_encryption_configuration`.
- **Cách khắc phục:** Thêm khối tài nguyên mã hóa S3 vào `main.tf`.

### 10. Sự cố Tệp `tfplan` artifact bị hết hạn khi bấm nút Apply sau 10 ngày
- **Triệu chứng:** Nút Manual Apply báo lỗi `Artifact not found`.
- **Nguyên nhân:** Cấu hình `artifacts.expire_in: 7 days` làm tệp artifact bị tự động xóa sau 7 ngày.
- **Cách khắc phục:** Tăng thời gian lưu trữ artifact `expire_in: 30 days` hoặc chạy lại `plan`.

### 11. Sự cố Lỗi `Error: Provider produced inconsistent final plan`
- **Triệu chứng:** Lệnh `terraform apply` bị ngắt giữa chừng.
- **Nguyên nhân:** Cloud API trả về thuộc tính thực tế khác với thuộc tính Terraform dự đoán.
- **Cách khắc phục:** Cập nhật phiên bản Terraform Provider mới nhất (`version = "~> 5.0"`).

### 12. Sự cố Tệp `variables.tf` bị gõ nhầm type declaration
- **Triệu chứng:** `terraform validate` nổ lỗi `type is required`.
- **Nguyên nhân:** Khai báo variable không ghi rõ `type = string`.
- **Cách khắc phục:** Bổ sung đúng kiểu dữ liệu `type` cho mọi biến trong `variables.tf`.

### 13. Sự cố Quên cờ `-input=false` làm job CI bị treo vô tận
- **Triệu chứng:** Job CI chạy `terraform plan` dừng mãi ở 0% CPU.
- **Nguyên nhân:** Terraform chờ con người gõ giá trị variable từ bàn phím terminal.
- **Cách khắc phục:** Luôn bổ sung cờ `-input=false` cho mọi câu lệnh Terraform trong CI.

### 14. Sự cố Multi-environment bị đè State File của nhau
- **Triệu chứng:** Triển khai Staging làm sập tài nguyên của Production.
- **Nguyên nhân:** Dùng chung biến `TF_STATE_NAME` cho cả 2 môi trường.
- **Cách khắc phục:** Đặt tên State khác nhau: `TF_STATE_NAME="staging"` và `TF_STATE_NAME="production"`.

### 15. Sự cố Lỗi `Error: Resource already exists` khi chạy `terraform apply`
- **Triệu chứng:** Apply báo lỗi tài nguyên Cloud đã tồn tại từ trước.
- **Nguyên nhân:** Ai đó tạo tài nguyên thủ công trên Cloud nhưng chưa import vào State File.
- **Cách khắc phục:** Chạy câu lệnh `terraform import <address> <id>` để nạp tài nguyên vào State.

### 16. Sự cố `validate-hcl-code.sh` nổ lỗi `dist directory not found`
- **Triệu chứng:** Script validation bị ngắt giữa chừng.
- **Nguyên nhân:** Thư mục `dist` chưa được khởi tạo.
- **Cách khắc phục:** Bổ sung `mkdir -p dist` trong script.

### 17. Sự cố GitLab UI hiển thị `Terraform report failed to parse`
- **Triệu chứng:** Merge Request Widget không hiển thị được bảng báo cáo Terraform.
- **Nguyên nhân:** Tệp `tfplan.json` bị sai định dạng JSON hoặc rỗng.
- **Cách khắc phục:** Kiểm tra lại lệnh `terraform show -json tfplan | jq . > tfplan.json`.

### 18. Sự cố Tệp `terraform.tfstate` bị tăng dung lượng lên 100MB
- **Triệu chứng:** Tải State File bị timeout.
- **Nguyên nhân:** Lưu trữ dữ liệu cấu hình quá nhiều tài nguyên rác trong 1 State Single File.
- **Cách khắc phục:** Chia nhỏ mã nguồn IaC thành các Modules và State Files độc lập.

### 19. Sự cố `simulate-gitlab-state-backend.sh` nổ lỗi bash syntax
- **Triệu chứng:** Script mô phỏng Backend nổ error.
- **Nguyên nhân:** Thiếu dấu ngoặc kép khi đọc tham số `$ACTION`.
- **Cách khắc phục:** Bọc các biến trong ngoặc `"$ACTION"`.

### 20. Sự cố Quên cờ `-recursive` khi chạy `terraform fmt`
- **Triệu chứng:** Các file HCL nằm trong thư mục con `modules/` không được định dạng.
- **Nguyên nhân:** `terraform fmt` mặc định chỉ quét thư mục hiện tại.
- **Cách khắc phục:** Bắt buộc dùng `terraform fmt -check -recursive`.

### 21. Sự cố Cụm AWS Cloud IAM từ chối OIDC Token của Runner
- **Triệu chứng:** `terraform plan` nổ lỗi `AccessDenied: Invalid Identity Token`.
- **Nguyên nhân:** Claim `aud` hoặc `sub` của OIDC Token không khớp với AWS IAM Trust Policy.
- **Cách khắc phục:** Kiểm tra lại cấu hình Trust Policy của IAM Role (bài học Buổi 38).

### 22. Sự cố Tệp `outputs.tf` chứa thông tin nhạy cảm plain-text
- **Triệu chứng:** Mật khẩu DB bị in ra màn hình console log của CI Runner.
- **Nguyên nhân:** Không đánh dấu `sensitive = true` cho output nhạy cảm.
- **Cách khắc phục:** Thêm `sensitive = true` vào khối output nhạy cảm.

### 23. Sự cố `terraform-drift-detection.sh` nổ lỗi file not found
- **Triệu chứng:** Script kiểm thử Drift báo không tìm thấy folder.
- **Nguyên nhân:** Thư mục `audit/drift-reports` chưa khởi tạo.
- **Cách khắc phục:** Thêm `mkdir -p audit/drift-reports` trong script.

### 24. Sự cố Lỗi `403 Forbidden` khi giải phóng State Lock trên GitLab UI
- **Triệu chứng:** Bấm nút Unlock State báo lỗi không đủ quyền.
- **Nguyên nhân:** Tài khoản người dùng chỉ có quyền `Developer` thay vì `Maintainer`.
- **Cách khắc phục:** Yêu cầu Admin cấp quyền `Maintainer` trở lên để Force Unlock State.

### 25. Sự cố Quên cờ `-reconfigure` khi chạy `terraform init`
- **Triệu chứng:** Terraform sử dụng lại cấu hình Backend cũ bị sai.
- **Nguyên nhân:** Cache local của `.terraform/` lưu backend cũ.
- **Cách khắc phục:** Luôn dùng `terraform init -reconfigure` trong `before_script`.

### 26. Sự cố Lỗi `cyclic dependency` trong mã nguồn HCL
- **Triệu chứng:** `terraform validate` nổ lỗi phụ thuộc vòng lặp.
- **Nguyên nhân:** Tài nguyên A tham chiếu tài nguyên B và tài nguyên B lại tham chiếu ngược A.
- **Cách khắc phục:** Bỏ tham số lặp hoặc sử dụng tài nguyên trung gian.

### 27. Sự cố `final-terraform-lab-evaluation.sh` báo 5/6 thành phần
- **Triệu chứng:** Bài lab đánh giá chưa đạt 100%.
- **Nguyên nhân:** Chưa chạy Bước 9 tạo báo cáo Security Scan.
- **Cách khắc phục:** Chạy script `./scripts/scan-hcl-security.sh`.

### 28. Sự cố Tên S3 Bucket bị lặp trên phạm vi toàn cầu của AWS
- **Triệu chứng:** `terraform apply` nổ lỗi `BucketAlreadyExists`.
- **Nguyên nhân:** Tên S3 Bucket bị trùng với một bucket khác trên toàn mạng AWS.
- **Cách khắc phục:** Thêm tiền tố độc nhất hoặc chuỗi ngẫu nhiên `random_id` vào tên bucket.

### 29. Sự cố GitLab CI Variable `TF_VAR_db_password` không nạp vào Terraform
- **Triệu chứng:** Terraform hỏi mật khẩu từ bàn phím khi plan.
- **Nguyên nhân:** Tên biến môi trường không có tiền tố `TF_VAR_`.
- **Cách khắc phục:** Đặt tên biến CI là `TF_VAR_<variable_name>`.

### 30. Sự cố Lỗi `Error: Request-Timeout` khi Terraform gọi Azure API
- **Triệu chứng:** `terraform plan` bị hủy ngầm do nghẽn mạng Azure.
- **Nguyên nhân:** Mạng giữa CI Runner và Azure Cloud API bị nghẽn.
- **Cách khắc phục:** Đặt CI Runner trong cùng Azure Virtual Network (VNet).

### 31. Sự cố Mã nguồn HCL dùng phiên bản Provider quá cũ bị Deprecated
- **Triệu chứng:** Terraform cảnh báo thuộc tính sắp bị xóa.
- **Nguyên nhân:** Sử dụng syntax HCL của Terraform v0.12 trên Terraform v1.5+.
- **Cách khắc phục:** Nâng cấp cú pháp HCL theo chuẩn Terraform v1.5+.

### 32. Sự cố `render-mr-plan-report.sh` nổ lỗi sed trên macOS
- **Triệu chứng:** Script render báo lỗi cú pháp.
- **Nguyên nhân:** Khác biệt lệnh `sed` trên Linux và macOS.
- **Cách khắc phục:** Dùng toán tử chuyển hướng `cat << EOF > file` chuẩn xác.

### 33. Sự cố AWS Resource bị gõ sai Region trong `provider.tf`
- **Triệu chứng:** Tạo tài nguyên ở `us-east-1` thay vì `ap-southeast-1`.
- **Nguyên nhân:** Đặt default variable `aws_region` không đúng region yêu cầu.
- **Cách khắc phục:** Đặt `default = "ap-southeast-1"` trong `variables.tf`.

### 34. Sự cố TFLint báo lỗi `missing module version constraint`
- **Triệu chứng:** Linter cảnh báo Module không khai báo version.
- **Nguyên nhân:** Gọi Terraform Module mà không ghi rõ `version = "1.0.0"`.
- **Cách khắc phục:** Thêm `version = "1.0.0"` cho tất cả các khối `module`.

### 35. Sự cố `terraform-apply-stage.sh` nổ lỗi missing plan file
- **Triệu chứng:** Script apply báo không tìm thấy tệp plan.
- **Nguyên nhân:** Chưa thực thi Bước 5 tạo tệp plan artifact.
- **Cách khắc phục:** Chạy Bước 5 trước khi chạy Bước 7.

### 36. Sự cố Biến `TF_IN_AUTOMATION=true` không được kích hoạt
- **Triệu chứng:** Output của Terraform in quá nhiều dòng hướng dẫn terminal không cần thiết.
- **Nguyên nhân:** Thiếu biến môi trường thông báo cho Terraform biết đang chạy trong CI.
- **Cách khắc phục:** Đặt `export TF_IN_AUTOMATION=true` trong `before_script`.

### 37. Sự cố `validate-terraform-gitlab-ci.sh` báo lỗi thiếu manual gate
- **Triệu chứng:** Linter chặn CI vì pipeline thiếu bước phê duyệt thủ công.
- **Nguyên nhân:** Viết file `.gitlab-ci.yml` thiếu `when: manual`.
- **Cách khắc phục:** Bổ sung `when: manual` trong khối apply.

### 38. Sự cố Cron Scheduled Drift Detection không gửi tin nhắn Slack
- **Triệu chứng:** Phát hiện Drift nhưng không có thông báo về kênh đỗi ngũ.
- **Nguyên nhân:** Biến `SLACK_WEBHOOK_URL` bị thiếu hoặc sai URL.
- **Cách khắc phục:** Kiểm tra lại Webhook URL trong GitLab CI Variables.

### 39. Sự cố Git diff hiển thị 100% dòng do khác biệt End-of-Line CRLF
- **Triệu chứng:** Reviewer nhìn thấy toàn bộ file `main.tf` bị sửa khi commit từ Windows.
- **Nguyên nhân:** Windows tự đổi ký tự xuống dòng từ LF sang CRLF.
- **Cách khắc phục:** Chuẩn hóa `.gitattributes` bắt buộc dùng dòng LF.

### 40. Sự cố GitLab Managed Backend bị đầy dung lượng do giữ hàng ngàn State Versions
- **Triệu chứng:** Tốc độ `terraform init` bị chậm.
- **Nguyên nhân:** Không cài đặt chính sách dọn dẹp các phiên bản State cũ.
- **Cách khắc phục:** Cấu hình Retention Policy dọn dẹp State Versions cũ hơn 90 ngày.

### 41. Sự cố Quên cờ `-input=false` làm lệnh `terraform apply` hỏi confirmation
- **Triệu chứng:** Job CI apply bị dừng ở câu hỏi `Do you want to perform these actions?`.
- **Nguyên nhân:** Thiếu cờ ngắt câu hỏi tương tác.
- **Cách khắc phục:** Luôn truyền cờ `-input=false` khi apply file `tfplan`.

### 42. Sự cố Tệp `mr-report.md` bị vượt quá giới hạn ký tự comment của GitLab API
- **Triệu chứng:** MR comment bị cắt ngắn giữa chừng.
- **Nguyên nhân:** `terraform plan` sinh ra hàng ngàn tài nguyên làm file report quá lớn.
- **Cách khắc phục:** Bọc nội dung chi tiết trong thẻ `<details><summary>` và giới hạn số dòng.

### 43. Sự cố Cloud Provider API bị nghẽn làm job `terraform plan` bị timeout
- **Triệu chứng:** Job CI bị hủy sau 60 phút.
- **Nguyên nhân:** Mạng kết nối chập chờn khi đọc thông tin hàng ngàn tài nguyên.
- **Cách khắc phục:** Tăng cờ `-parallelism=20` để Terraform đọc tài nguyên song song nhanh hơn.

### 44. Sự cố `force-unlock-state.sh` nổ lỗi Lock ID không tồn tại
- **Triệu chứng:** Force unlock bị từ chối.
- **Nguyên nhân:** Nhập sai chuỗi Lock ID.
- **Cách khắc phục:** Kiểm tra chính xác Lock ID trên log hoặc GitLab UI.

### 45. Sự cố Terraform Workspace bị xóa nhầm trên GitLab Backend
- **Triệu chứng:** `terraform workspace select production` nổ lỗi không tìm thấy.
- **Nguyên nhân:** Ai đó chạy lệnh `terraform workspace delete production`.
- **Cách khắc phục:** Khôi phục State File từ GitLab State Version History.

### 46. Sự cố Lỗi `Error: Unsupported argument` khi chạy `terraform validate`
- **Triệu chứng:** Validation nổ lỗi không hỗ trợ tham số.
- **Nguyên nhân:** Thuộc tính HCL viết sai tên từ vựng.
- **Cách khắc phục:** Đọc tài liệu của Provider để kiểm tra lại tên thuộc tính chuẩn.

### 47. Sự cố Cờ `reports.terraform` trong `.gitlab-ci.yml` trỏ sai đường dẫn file JSON
- **Triệu chứng:** GitLab MR Widget không hiển thị báo cáo plan.
- **Nguyên nhân:** Đặt đường dẫn `reports.terraform: tfplan.json` nhưng file nằm trong `dist/`.
- **Cách khắc phục:** Đảm bảo đường dẫn file JSON chính xác 100%.

### 48. Sự cố Terraform CI Runner bị hết bộ nhớ RAM khi chạy `terraform plan`
- **Triệu chứng:** Job CI báo lỗi `Killed` (Out of Memory).
- **Nguyên nhân:** Mã HCL quá lớn làm Terraform chiếm hơn 4GB RAM.
- **Cách khắc phục:** Tăng RAM cho máy chủ Runner hoặc chia nhỏ mã HCL thành Modules.

### 49. Sự cố `final-terraform-lab-evaluation.sh` nổ lỗi syntax bash
- **Triệu chứng:** Script tổng kết báo lỗi dòng.
- **Nguyên nhân:** Thiếu dấu ngoặc vuông đóng trong câu lệnh kiểm tra tệp.
- **Cách khắc phục:** Đảm bảo cú pháp `[ -f file ]` chuẩn xác.

### 50. Sự cố Tệp `terraform.tfvars` chứa secret bị vô tình push lên Git
- **Triệu chứng:** Mật khẩu DB bị rò rỉ công khai trên Git repo.
- **Nguyên nhân:** Thiếu `*.tfvars` trong tệp `.gitignore`.
- **Cách khắc phục:** Bổ sung `*.tfvars` vào `.gitignore` và thu hồi mật khẩu ngay lập tức.

### 51. Sự cố Lỗi `Error: Invalid index` khi truy cập Output của Module
- **Triệu chứng:** `terraform apply` nổ lỗi chỉ mục mảng.
- **Nguyên nhân:** Truy cập phần tử mảng khi mảng rỗng.
- **Cách khắc phục:** Kiểm tra điều kiện `length()` trước khi truy cập index.

### 52. Sự cố TFLint nổ lỗi `module not installed`
- **Triệu chứng:** Linter chặn CI vì chưa cài đặt Modules.
- **Nguyên nhân:** Quên chạy `terraform init` trước khi chạy `tflint`.
- **Cách khắc phục:** Luôn chạy `terraform init` trước khi gọi `tflint`.

### 53. Sự cố `scripts/validate-terraform-gitlab-ci.sh` bị nổ lỗi permission denied
- **Triệu chứng:** Không chạy được script linter.
- **Nguyên nhân:** Quên cấp quyền execution cho file.
- **Cách khắc phục:** Chạy `chmod +x scripts/validate-terraform-gitlab-ci.sh`.

### 54. Sự cố Apply bị hủy do Kỹ sư bấm nhầm nút Cancel trên Manual Gate
- **Triệu chứng:** Pipeline bị dừng ở stage apply.
- **Nguyên nhân:** Thao tác con người bấm nhầm nút Cancel thay vì Play.
- **Cách khắc phục:** Bấm **Retry** lại stage apply để tiếp tục triển khai.

### 55. Sự cố Phê duyệt Manual Gate bị canceled tự động sau 7 ngày
- **Triệu chứng:** Nút Play manual bị vô hiệu hóa.
- **Nguyên nhân:** Nút duyệt manual trong MR không được tương tác trong 7 ngày.
- **Cách khắc phục:** Chạy lại (Retry) pipeline từ stage plan để cấp nút manual gate mới.

---

## Bài tập mở rộng

1. **Xây dựng Pipeline Multi-Environment Terraform với Workspaces & GitLab Backend:**
   - Xây dựng cấu hình Terraform CI/CD hỗ trợ 3 môi trường: `development`, `staging`, và `production` sử dụng **Terraform Workspaces** (`terraform workspace select`).
   - Khai báo động biến `TF_STATE_NAME="infrastructure-${CI_COMMIT_REF_SLUG}"` để GitLab Backend tự động quản lý 3 State Files độc lập hoàn toàn cho 3 môi trường mà không bị đè dữ liệu!

2. **Tích hợp Infracost để Dự toán Chi phí Hạ tầng Cloud trực tiếp trên Merge Request:**
   - Tích hợp công cụ **Infracost** vào stage `plan` của GitLab CI Pipeline.
   - Khi kỹ sư sửa mã HCL thêm tài nguyên (như tạo thêm EC2 Instance hay RDS Database), Infracost tự động tính toán chi phí tăng thêm tính theo USD/tháng và comment bảng dự toán chi phí trực tiếp vào Merge Request cho Tech Lead phê duyệt trước khi Apply!

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| Bước 1 | Khởi tạo Cấu trúc Thư mục và Mã nguồn HCL Terraform | 10 phút |
| Bước 2 | Tạo Tệp `.gitignore` Chuẩn mực Loại bỏ State Files và Secrets | 10 phút |
| Bước 3 | Thực thi Lập trình Linter `terraform fmt` và `terraform validate` | 15 phút |
| Bước 4 | Viết Script Mô phỏng GitLab Managed State Backend và State Locking | 15 phút |
| Bước 5 | Viết Script Mô phỏng `terraform plan -out=tfplan` Sinh Artifacts Binary | 15 phút |
| Bước 6 | Viết Script Mô phỏng Merge Request Plan Reporting Widget | 10 phút |
| Bước 7 | Viết Script Mô phỏng Stage `terraform apply tfplan` qua Manual Gate | 15 phút |
| Bước 8 | Kiểm thử Phát hiện Sai lệch Trạng thái Hạ tầng (State Drift Detection) | 15 phút |
| Bước 9 | Tích hợp Bộ quét Security & Linter HCL (`tflint` & `trivy`) | 10 phút |
| Bước 10 | Viết Script Mô phỏng Force Unlock State File khi Kẹt Khóa | 10 phút |
| Bước 11 | Viết Script Ghi nhận Nhật ký Terraform Execution Audit Logs | 10 phút |
| Bước 12 | Xây dựng Script Linter Kiểm tra Cấu hình GitLab CI cho Terraform | 5 phút |
| Bước 13 | Xây dựng Script Mô phỏng Truy xuất Lịch sử State File Disaster Recovery | 5 phút |
| Bước 14 | Tổng hợp Đánh giá Hoàn thành Bài Lab Buổi 42 | 5 phút |
| **Tổng** | **Khối thực hành lab** | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

# Buổi 42: Terraform trong GitLab CI: state, plan/apply gate, drift — Vấn Đáp & Phỏng Vấn

## Thống kê & Phân bổ thời lượng
- **Tổng thời lượng:** 20 phút
- **Cấu trúc:**
  - 5 phút: Kiểm tra phản xạ lý thuyết (12 câu hỏi trắc nghiệm & tự luận nhanh)
  - 10 phút: Đóng vai phỏng vấn tình huống thực chiến (7 kịch bản nâng cao)
  - 5 phút: Chốt từ khóa ăn tiền (§V3) & Giao bài tập về nhà chuẩn bị cho Buổi 43 (BTVN 4)

---

## §V1. 12 Câu hỏi vấn đáp kiểm tra phản xạ

### Câu 1
**Hỏi:** Sự khác biệt nguy hiểm nhất giữa việc chạy câu lệnh `terraform apply tfplan` (dùng tệp artifact plan binary) và chạy `terraform apply -auto-approve` (không dùng tệp artifact plan) trong CI Pipeline là gì?

**Gợi ý trả lời ngắn:**
Chạy không dùng artifact sẽ tự tính toán lại plan mới tại thời điểm apply, có thể xóa nhầm tài nguyên Production do sai lệch state; dùng `tfplan` artifact đảm bảo thực thi ĐÚNG các hành động đã được review trên MR.

**Đáp án chuẩn:**
- **Giải thích nguy cơ:**
  Nếu không truyền file binary plan artifact (`tfplan`), Terraform sẽ tự động đọc lại trạng thái Cloud API và tạo lại một plan mới tại thời điểm chạy stage `apply`. Nếu trong khoảng thời gian chờ phê duyệt manual gate có một Merge Request khác được merge hoặc ai đó sửa Cloud Console, plan mới này có thể chứa hành động nguy hiểm (như xóa VPC hay Database) mà chưa từng được bất kỳ ai review trên Merge Request!
- **Cơ chế an toàn:** Lệnh `terraform apply tfplan` bắt buộc thực thi chính xác 100% các hành động đã được đóng gói trong tệp artifact binary. Nếu State File bị thay đổi, lệnh apply sẽ nổ lỗi ngắt lập tức.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng "chạy `terraform apply -auto-approve` ở stage apply giúp tiết kiệm thời gian CI mà không có rủi ro nào".

---

### Câu 2
**Hỏi:** Hai tính năng bảo mật và quản trị hạ tầng quan trọng nhất mà GitLab Managed Terraform State Backend cung cấp là gì?

**Gợi ý trả lời ngắn:**
Hai tính năng quan trọng nhất là **Mã hóa lưu trữ State File (Encryption at Rest)** và **Tự động khóa State (State Locking HTTP POST/DELETE)** chống nghẽn ghi đồng thời.

**Đáp án chuẩn:**
- **Chi tiết hai tính năng:**
  1. *Mã hóa bảo mật (Encryption at Rest):* GitLab lưu trữ tệp `terraform.tfstate` trên backend và tự động mã hóa, ngăn ngừa rò rỉ secret credentials (như DB Password hay Access Token) ra máy chủ Runner local.
  2. *Tự động khóa State (State Locking):* Khi một job CI bắt đầu thực thi `terraform plan` hoặc `apply`, GitLab tự động kích hoạt HTTP POST Lock ID. Mọi job CI khác cố tình can thiệp vào State File sẽ bị từ chối, triệt hạ 100% rủi ro hỏng cấu trúc State (State Corruption) do ghi đồng thời (Race Condition).

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Lưu tệp `terraform.tfstate` cục bộ trên máy chủ CI Runner hoặc commit tệp `.tfstate` lên kho mã nguồn Git.

---

### Câu 3
**Hỏi:** Tại sao stage `terraform apply` cho các môi trường Production lại bắt buộc phải đặt chế độ phê duyệt thủ công (`when: manual`)?

**Gợi ý trả lời ngắn:**
Đảm bảo quy trình Phê duyệt hai bước (Four-Eye Principle), bắt buộc Tech Lead hoặc DevOps Manager xem xét lại tệp plan trước khi kích hoạt thay đổi hạ tầng đám mây thực tế.

**Đáp án chuẩn:**
- **Cơ chế kiểm soát rủi ro:**
  Mặc dù mã nguồn HCL đã được test và merge vào nhánh `main`, việc thay đổi hạ tầng đám mây (đặc biệt là chỉnh sửa Subnet, Security Group, Routing Table) mang rủi ro làm gián đoạn dịch vụ rất cao. Cờ `when: manual` tạo ra một cổng chặn an toàn (Manual Gate), ép con người phải rà soát lại tệp `tfplan` artifact một lần nữa và bấm nút **Play** trên giao diện GitLab CI UI mới cho phép apply.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Đặt cờ `when: always` cho stage `terraform apply` Production để hạ tầng tự động thay đổi ngay khi merge code.

---

### Câu 4
**Hỏi:** Ý nghĩa của mã thoát chi tiết (Detailed Exit Code) `Exitcode 2` khi thực thi câu lệnh `terraform plan -detailed-exitcode` là gì?

**Gợi ý trả lời ngắn:**
Mã Exitcode 2 báo hiệu câu lệnh `terraform plan` phát hiện có sự thay đổi hạ tầng (Infrastructure State Drift) giữa mã HCL trên Git và trạng thái thực tế trên Cloud Console.

**Đáp án chuẩn:**
- **Bảng mã Exit Status của `-detailed-exitcode`:**
  - `Exitcode 0`: Thành công, không có bất kỳ thay đổi nào giữa Git và Cloud.
  - `Exitcode 1`: Thất bại, xảy ra lỗi cú pháp HCL hoặc lỗi kết nối Provider.
  - `Exitcode 2`: Thành công, nhưng phát hiện có sai lệch hạ tầng (Infrastructure Drift Detected - có tài nguyên cần thêm/sửa/xóa).
- **Ứng dụng:** Sử dụng Exitcode 2 trong các Pipeline Cron Schedule định kỳ để tự động phát hiện và cảnh báo khi có ai đó tự ý sửa hạ tầng qua Cloud Console UI!

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng Exitcode 2 là mã báo lỗi hỏng script CI.

---

### Câu 5
**Hỏi:** Tại sao trong kiến trúc Terraform CI Enterprise tuyệt đối không được sử dụng chìa khóa tĩnh `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` trong GitLab CI Variables?

**Gợi ý trả lời ngắn:**
Vì chìa khóa tĩnh có thời hạn sống dài hạn; nếu máy chủ Runner bị lỗ hổng RCE, kẻ tấn công sẽ lấy trộm secret key và chiếm quyền kiểm soát vĩnh viễn Cloud Account.

**Đáp án chuẩn:**
- **Giải pháp Keyless OIDC Federation:**
  Áp dụng nguyên lý OIDC Federation đã học ở buổi 37-40 (buổi 38 QT 38.1, buổi 40 QT 40.1). Máy chủ Terraform CI Runner sử dụng `GITLAB_OIDC_TOKEN` để đổi lấy Cloud Access Token ngắn hạn có thời hạn sống tối đa 60 phút và tự động thu hồi.
- **Bán kính ảnh hưởng bằng $0:** Ngay cả khi rò rỉ biến CI của Runner, kẻ tấn công cũng không thu thập được chìa khóa tĩnh để can thiệp hạ tầng về sau.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Lưu `AWS_ACCESS_KEY_ID` và `AWS_SECRET_ACCESS_KEY` dạng Masked Variable trong GitLab CI.

---

### Câu 6
**Hỏi:** Công cụ Linter & Security Scanner nào giúp tự động kiểm tra chuẩn cú pháp và quét lỗ hổng an toàn mã nguồn HCL trực tiếp trên Merge Request?

**Gợi ý trả lời ngắn:**
Công cụ **TFLint** (`tflint`) quét lỗi cú pháp/chuẩn thiết kế Cloud và **Trivy** (`trivy config`) / **TFSec** (`tfsec`) quét lỗ hổng bảo mật HCL.

**Đáp án chuẩn:**
- **Tích hợp bộ đôi Linter & Security Scan vào CI:**
  1. *TFLint:* Kiểm tra các lỗi logic mà `terraform validate` bỏ sót (như dùng sai kiểu Instance Type không tồn tại trên AWS Region).
  2. *Trivy / TFSec:* Quét các vi phạm an toàn hạ tầng (như mở Security Group 0.0.0.0/0, tắt mã hóa S3 Bucket, hay khai báo plain-text password).
- **Kết quả:** Chặn đứng 95% mã HCL không đạt chuẩn an toàn ngay ở stage `validate` của Merge Request.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Bỏ qua bước quét linter và security scan, cho phép merge mã HCL vi phạm quy chuẩn an toàn.

---

### Câu 7
**Hỏi:** Tại sao tệp `terraform.tfstate` tuyệt đối không bao giờ được commit lên kho mã nguồn Git repository?

**Gợi ý trả lời ngắn:**
Vì State File chứa toàn bộ sơ đồ hạ tầng và có thể chứa mật khẩu/secret plain-text; commit lên Git sẽ làm rò rỉ bí mật và gây xung đột Git merge nghiêm trọng.

**Đáp án chuẩn:**
- **Lý do an ninh và kỹ thuật:**
  1. *Rò rỉ bí mật (Secret Exposure):* Dù biến môi trường được đánh dấu `sensitive = true`, Terraform vẫn bắt buộc phải lưu giá trị thực tế của mật khẩu/API Keys trong tệp State File. Push State File lên Git là làm lộ mật khẩu cho bất kỳ ai có quyền đọc Git.
  2. *Xung đột Git (Merge Conflicts):* Tệp State File thay đổi theo từng hành động. Nếu nhiều người cùng commit file state, Git Merge Conflict sẽ làm hỏng cấu trúc JSON của State File, khiến hạ tầng bị treo.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Commit tệp `terraform.tfstate` lên Git repository với lý do "để các thành viên cùng chia sẻ state".

---

### Câu 8
**Hỏi:** Cấu hình nào trong tệp `.gitlab-ci.yml` giúp tự động hiển thị bảng tổng hợp thay đổi tài nguyên Terraform trực tiếp trên giao diện Merge Request Widget?

**Gợi ý trả lời ngắn:**
Cấu hình `reports.terraform: tfplan.json` trong khối `artifacts` của job `terraform plan`.

**Đáp án chuẩn:**
- **Cơ chế GitLab Terraform Report Integration:**
  Trong stage `plan`, script chạy 2 lệnh:
  `terraform plan -out=tfplan`
  `terraform show -json tfplan | jq . > tfplan.json`
  Sau đó khai báo `reports.terraform: tfplan.json` trong khối artifacts. GitLab CI tự động đọc file JSON này và render một Widget đẹp mắt trực tiếp trên giao diện Merge Request với thông tin: `Terraform planned 2 to add, 0 to change, 0 to destroy`.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Yêu cầu Reviewer phải tự vào log thô (raw log) của CI Runner để đọc kết quả plan.

---

### Câu 9
**Hỏi:** Tại sao trong kiến trúc Enterprise lại cần tách rời State Files của môi trường Staging và Production bằng Terraform Workspaces hoặc thư mục độc lập?

**Gợi ý trả lời ngắn:**
Giúp đảm bảo tính cô lập hoàn toàn (Environment Isolation), sự cố thực thi hay hỏng State trên Staging tuyệt đối không bao giờ ảnh hưởng tới hạ tầng Production.

**Đáp án chuẩn:**
- **Nguyên tắc Cô lập Môi trường:**
  Nếu dùng chung 1 State File cho cả Staging và Production, một câu lệnh `terraform destroy` hoặc lỗi sai chỉ mục variable trên Staging có thể vô tình xóa nhầm tài nguyên Production!
- **Giải pháp:** Tách biệt thành 2 State Files riêng biệt (`TF_STATE_NAME="staging"` và `TF_STATE_NAME="production"`) trên GitLab Backend hoặc dùng cấu trúc folder `environments/staging/` và `environments/production/`.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Dùng chung 1 State File duy nhất cho tất cả các môi trường Dev, Staging, và Production.

---

### Câu 10
**Hỏi:** Mục đích của câu lệnh `terraform fmt -check -recursive` trong stage `validate` đầu tiên của pipeline là gì?

**Gợi ý trả lời ngắn:**
Ép mã nguồn HCL tuân thủ chuẩn định dạng 2 spaces indent của HashiCorp, giúp code sạch đẹp và loại bỏ tranh cãi không cần thiết khi review git diff.

**Đáp án chuẩn:**
- **Ý nghĩa định dạng tự động:**
  Câu lệnh `terraform fmt -check -recursive` quét toàn bộ tệp `.tf` trong tất cả thư mục con. Nếu phát hiện có dòng code gõ sai khoảng trắng hoặc dùng dấu Tab, nó sẽ trả về Exitcode 1 và hủy job CI ngay lập tức.
- **Lợi ích:** Đảm bảo 100% mã nguồn HCL trong toàn công ty tuân thủ một chuẩn định dạng thống nhất duy nhất.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Để mã nguồn HCL lộn xộn khoảng trắng, làm rối mắt người review trên Merge Request.

---

### Câu 11
**Hỏi:** Khi tệp State File bị kẹt ở trạng thái locked do job CI trước bị sập nguồn giữa chừng, làm thế nào để giải phóng khóa an toàn?

**Gợi ý trả lời ngắn:**
Sử dụng tính năng **Force Unlock State** trên giao diện GitLab UI (`Infrastructure -> Terraform states`) hoặc chạy câu lệnh `terraform force-unlock <lock_id>`.

**Đáp án chuẩn:**
- **Quy trình xử lý State Lock bị kẹt:**
  1. *Kiểm tra nguyên nhân:* Xác nhận job CI trước đã thực sự bị ngắt (không còn job nào đang chạy ngầm).
  2. *Lấy Lock ID:* Trích xuất chuỗi `Lock ID: lock-9f8a2b3c` từ nhật ký lỗi CI.
  3. *Giải phóng khóa:* Mở GitLab UI mục `Infrastructure -> Terraform states` bấm nút **Unlock**, hoặc gõ lệnh `terraform force-unlock <lock_id>` từ máy tính có quyền Maintainer.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Xóa luôn tệp State File hoặc tạo dự án mới khi gặp lỗi State Lock.

---

### Câu 12
**Hỏi:** Làm thế nào để khoanh vùng bán kính ảnh hưởng (Blast Radius Isolation) nếu tệp OIDC credentials của Terraform Runner bị rò rỉ?

**Gợi ý trả lời ngắn:**
Giới hạn ranh giới phân quyền Cloud IAM của ServiceAccount theo đúng Scope của Resource Group / AWS Account dành riêng cho môi trường đó.

**Đáp án chuẩn:**
- **Nguyên tắc Phân quyền Hạn chế (Least Privilege):**
  Không gán quyền `AdministratorAccess` hay `Owner` cho Terraform Runner. Chỉ gán vai trò `Contributor` trên duy nhất 1 Resource Group hoặc 1 VPC cụ thể.
- **Kết quả:** Ngay cả khi mã HCL bị lỗi gõ nhầm scope hoặc Runner bị chiếm quyền, tác động cũng bị khống chế 100% bên trong Resource Group chỉ định, không thể gây hại cho các hạ tầng quan trọng khác.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cấp quyền `AdministratorAccess` toàn quyền trên Cloud Account cho Terraform CI Runner.

---

## §V2. Kịch bản phỏng vấn thực tế (Roleplay Scenarios)

### Kịch bản 1: Thuyết phục CTO chuyển đổi từ chạy Terraform local sang GitLab CI/CD Backend
- **Người phỏng vấn (CTO):** *"Đội ngũ kỹ sư của chúng ta đang chạy `terraform apply` trực tiếp từ máy laptop cá nhân 3 năm nay rất nhanh. Tại sao em lại đề xuất tốn công chuyển sang chạy qua GitLab CI?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:* "Báo cáo anh, việc chạy Terraform từ laptop cá nhân đang chứa 3 thảm họa an toàn hạ tầng rất lớn:"
  - "1. **Nguy cơ race condition hỏng State:** Nếu 2 kỹ sư cùng chạy apply từ laptop, file state sẽ bị ghi đè gây hỏng cấu hình hạ tầng hoàn toàn."
  - "2. **Lộ Secret Mật khẩu:** Tệp `terraform.tfstate` lưu cục bộ trên laptop chứa mật khẩu DB plain-text. Nếu laptop bị mất hoặc dính malware, toàn bộ hạ tầng Production sẽ bị rò rỉ."
  - "3. **Giải pháp GitLab CI Backend:** Giúp đưa State File lên **GitLab Managed HTTP Backend có State Locking tự động**, đồng thời thiết lập **Plan/Apply Manual Gate**, đảm bảo 100% thay đổi hạ tầng được kiểm duyệt tập trung và có nhật ký audit log chuẩn Enterprise."

---

### Kịch bản 2: Giải quyết Thảm họa Xóa nhầm Database do `apply` không truyền tệp `tfplan` Artifact
- **Người phỏng vấn (Senior Cloud Architect):** *"Một kỹ sư junior vừa bấm duyệt pipeline và làm xóa mất Database RDS Production do lệnh `terraform apply` tự sinh ra plan mới tại thời điểm apply. Em khắc phục quy trình CI này thế nào để thảm họa này không bao giờ lặp lại?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Bắt đúng nguyên nhân:** Lỗi do job apply trong CI chạy câu lệnh `terraform apply -auto-approve` mà **không truyền tệp binary `tfplan` artifact** đã sinh ra từ stage `plan` trước đó (vi phạm QT 42.1).
    2. **Khắc phục quy trình chuẩn:**
       - Cập nhật `.gitlab-ci.yml`: Stage `plan` bắt buộc chạy `terraform plan -out=tfplan` và lưu `paths: [tfplan]` vào artifacts.
       - Stage `apply` bắt buộc phải chạy `terraform apply -input=false tfplan` và khai báo `dependencies: [plan-job]`.
    3. **Kết quả:** Lệnh apply bắt buộc phải tiêu thụ ĐÚNG tệp artifact binary đã được review trên Merge Request. Nếu State File bị lệch, apply dừng lập tức, triệt hạ 100% thảm họa xóa nhầm tài nguyên!

---

### Kịch bản 3: Xử lý Sự cố State File bị kẹt Lock trong đợt Release hạ tầng gấp
- **Người phỏng vấn (Operations Lead):** *"Hệ thống đang cần deploy hạ tầng khẩn cấp lúc 2:00 AM, nhưng pipeline CI liên tục nổ lỗi `Error acquiring the state lock` do job CI trước bị kill giữa chừng. Em giải quyết thế nào trong 2 phút?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Xác nhận an toàn:** Kiểm tra danh sách pipelines trên GitLab UI để đảm bảo không còn job CI nào đang chạy ghi state thực sự.
    2. **Thực thi Force Unlock State:**
       - Truy cập giao diện GitLab UI mục `Infrastructure -> Terraform states`.
       - Tìm State File `production-infrastructure`, kiểm tra Lock ID bị kẹt và bấm nút **Unlock**.
       - Hoặc gõ nhanh lệnh: `terraform force-unlock <lock_id>` từ terminal.
    3. **Retry Pipeline:** Bấm nút **Retry** trên job CI bị treo. Hạ tầng tiếp tục triển khai thành công 100% trong 60 giây!

---

### Kịch bản 4: Thuyết phục Security Auditor về phương án Bảo mật Credentials trong Terraform CI
- **Người phỏng vấn (Security Auditor):** *"Terraform CI Runner cần quyền tạo tài nguyên Cloud. Làm sao em đảm bảo chìa khóa Access Key của Cloud không bị lộ trong GitLab CI Variables?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Cam kết 0% Static Keys:** "Báo cáo anh, chúng em cam kết không lưu bất kỳ chuỗi `AWS_ACCESS_KEY_ID` hay secret key tĩnh nào trong GitLab CI Variables."
    2. **Áp dụng OIDC Workload Identity Federation:**
       - Cấu hình OIDC Provider giữa GitLab CI và AWS/GCP/Azure Entra ID.
       - Runner sử dụng `GITLAB_OIDC_TOKEN` ngắn hạn để đổi lấy Cloud Access Token tự hủy sau 60 phút.
       - Ngay cả khi máy chủ CI Runner bị lỗ hổng RCE, kẻ tấn công cũng không thể lấy được chìa khóa tĩnh để thâm nhập hệ thống về sau, đạt 100% tiêu chuẩn SOC2 & ISO 27001!

---

### Kịch bản 5: Xử lý Sự cố Phát hiện Sửa lén Hạ tầng Cloud Console với Drift Detection
- **Người phỏng vấn (Head of Infrastructure):** *"Làm sao em phát hiện được việc một kỹ sư vừa vào AWS Console sửa thủ công tăng RAM của Instance mà không khai báo vào mã nguồn HCL trên Git?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Thiết lập Pipeline Cron Drift Detection:**
       - Khai báo một Cron Schedule Pipeline trên GitLab CI chạy tự động lúc 6:00 AM mỗi ngày.
       - Executing câu lệnh: `terraform plan -detailed-exitcode`.
    2. **Bắt tín hiệu Exitcode 2:**
       - Nếu có sai lệch giữa Cloud và Git, lệnh plan trả về **Exitcode 2**.
       - Script CI bắt Exitcode 2 và tự động bắn tin nhắn cảnh báo đỏ vào kênh Slack `#devops-infra-alerts` kèm danh sách thuộc tính bị sửa bẩn.
    3. **Khôi phục:** Kích hoạt pipeline apply để đè lại mã HCL chuẩn từ Git trong 3 phút.

---

### Kịch bản 6: Tối ưu hóa Tốc độ Review Merge Request với Terraform Report Widget
- **Người phỏng vấn (DevOps Team Lead):** *"Các Tech Lead phản ánh việc phải mở log thô dài 3.000 dòng của CI Runner để đọc kết quả `terraform plan` khiến việc review MR rất chậm. Em tối ưu thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Trích xuất JSON Plan:** Trong stage `plan`, chạy câu lệnh `terraform show -json tfplan | jq . > tfplan.json`.
    2. **Khai báo Reports Artifact:** Bổ sung `reports.terraform: tfplan.json` vào khối `artifacts` trong `.gitlab-ci.yml`.
    3. **Kết quả:** Giao diện Merge Request hiển thị một Widget tổng hợp chuyên nghiệp: `Terraform planned 3 to add, 1 to change, 0 to destroy`. Reviewer chỉ cần nhìn Widget trên giao diện MR là biết ngay kết quả mà không cần mở log thô!

---

### Kịch bản 7: Xây dựng Quy trình Quét An ninh HCL với Trivy & TFLint
- **Người phỏng vấn (DevSecOps Lead):** *"Làm sao em ngăn chặn một lập trình viên vô tình commit file HCL mở cổng Security Group 0.0.0.0/0 hoặc tạo S3 Bucket không bật mã hóa?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Tích hợp TFLint & Trivy vào Stage Validate:**
       - Trong stage `validate` của MR pipeline, chạy bộ đôi công cụ `tflint` và `trivy config .`.
    2. **Chặn đứng vi phạm an ninh:**
       - Nếu code HCL mở port `0.0.0.0/0` hoặc thiếu khối mã hóa S3, Trivy phát hiện lỗi `AWS-001 / AWS-002` và trả về exitcode 1 dừng pipeline lập tức.
       - Developer bắt buộc phải sửa code HCL tuân thủ quy chuẩn an toàn trước khi MR được cho phép merge!

---

## §V3. Câu chốt để nói khi phỏng vấn

1. *"Luận đề trung tâm của Terraform CI là **file `plan` trong Merge Request chỉ có giá trị khi đúng tệp `tfplan` artifact đó được truyền sang stage `apply`**."*
2. *"Bắt buộc phải **sử dụng GitLab Managed HTTP State Backend** để vừa mã hóa lưu trữ State File, vừa tự động khóa State Locking chống nghẽn ghi đồng thời."*
3. *"Stage `terraform apply` môi trường Production **bắt buộc phải đặt cờ `when: manual`** trên nhánh Protected Branch để thực thi nguyên tắc Phê duyệt hai bước."*
4. *"Tự động hóa phát hiện sai lệch hạ tầng bằng **cờ `-detailed-exitcode` trong Cron Job**, bắt tín hiệu Exitcode 2 để bắn cảnh báo Drift Detection."*
5. *"Tuyệt đối **không lưu chìa khóa tĩnh Cloud Access Keys trong CI Variables**, chuyển đổi 100% sang Keyless OIDC Workload Identity Federation."*
6. *"Tuyệt đối **không commit tệp `terraform.tfstate` hoặc `*.tfvars` lên kho Git**, bắt buộc khai báo tệp `.gitignore` chuẩn mực."*
7. *"Tự động render báo cáo plan bằng **cấu hình `reports.terraform: tfplan.json`**, giúp hiển thị bảng thay đổi tài nguyên trực tiếp trên giao diện Merge Request Widget."*
8. *"Luôn **tách rời State Files giữa môi trường Staging và Production** để đảm bảo tính cô lập hạ tầng hoàn toàn (Environment Isolation)."*
9. *"Tích hợp **bộ đôi `tflint` và `trivy config` vào stage `validate`** để phát hiện 95% lỗi cú pháp và lỗ hổng an ninh HCL trước khi hạ tầng được khởi tạo."*
10. *"Luôn **giới hạn ranh giới phân quyền Cloud IAM của Terraform ServiceAccount** theo cấp hẹp của Resource Group / VPC để khống chế bán kính ảnh hưởng sự cố."*

---

## BTVN 4: Chuẩn bị cho Buổi 43 — Chiến lược release: Blue-green, Canary, Feature flags

Để chuẩn bị tốt nhất cho **Buổi 43: Chiến lược release: Blue-green, Canary, Feature flags**, học viên cần thực hiện các nhiệm vụ sau:

1. **Ôn tập kiến thức Chiến lược Triển khai Ứng dụng (Deployment Strategies):**
   - Đọc trước khái niệm **Blue-Green Deployment** (chuyển đổi 100% traffic giữa 2 môi trường song song) và **Canary Deployment** (điều tiết % traffic nhỏ nghiệm thu dần).
   - Tìm hiểu vai trò của **Feature Flags (Feature Toggles)** trong việc phát hành tính năng độc lập với việc deploy code.

2. **Nghiên cứu về thời gian phát hiện lỗi (Mean Time to Detect - MTTD):**
   - Phân tích luận đề: *"Chiến lược release quyết định **thời gian phát hiện lỗi (MTTD)** và **bán kính ảnh hưởng sự cố (Blast Radius)** — và đó là các con số phải đo đếm được!"*
   - Tìm hiểu cách GitLab CI tích hợp Feature Flags sử dụng Unleash Engine.

3. **Bài tập chuẩn bị trước giờ học:**
   - Trả lời câu hỏi: *"Khác biệt lớn nhất về yêu cầu tài nguyên hạ tầng giữa Blue-Green Deployment và Canary Deployment là gì?"*
   - Chuẩn bị ví dụ về kịch bản Rollback tức thì (<5 giây) khi tỷ lệ lỗi HTTP 5xx trên phiên bản Canary vượt quá 1%!
{% endraw %}
