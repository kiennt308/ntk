---
layout: post
title: "[Bài 01] Tư Duy Declarative IaC & So Sánh Thực Chiến: Terraform vs Ansible vs Pulumi vs CloudFormation"
date: 2026-09-13 12:00:00 +0700
categories: [Terraform]
tags:
  - Terraform
  - IaC
  - DevOps
  - CloudNative
  - Part-01
series: "Terraform Enterprise Architecture"
series_order: 1
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80"
summary: "Phân tích chuyên sâu tư duy Declarative Desired State, cơ chế toán học của Reconcile Loop, bảng so sánh thực chiến 10 tiêu chí (Terraform vs Ansible vs Pulumi vs CloudFormation), mổ xẻ mã nguồn HCL 1.7+ chuẩn Enterprise và bài học xương máu chống ClickOps Drift."
tldr:
  - "Declarative (Khai báo trạng thái mong muốn) giúp hệ thống tự phục hồi và loại bỏ hoàn toàn các rủi ro Partial State so với Imperative (Mệnh lệnh)."
  - "Chu trình Reconcile Loop so khớp 3 ngôi giữa Code HCL, State File và Cloud Actual State để tự động đưa hạ tầng về trạng thái mong muốn."
  - "Bộ tứ công cụ: Terraform (hạ tầng nền móng đa đám mây) + Ansible (cấu hình OS/phần mềm) + Pulumi (hạ tầng bằng code lập trình đa năng) + CloudFormation (AWS Native)."
  - "Triển khai Production an toàn bắt buộc có: State Locking (DynamoDB), Server-Side Encryption (KMS CMK), prevent_destroy và cấm cờ -auto-approve."
---

{% raw %}
# Tư Duy Declarative IaC & So Sánh Thực Chiến: Terraform vs Ansible vs Pulumi vs CloudFormation

Khi hạ tầng đám mây (**Cloud Infrastructure**) mở rộng từ vài chục lên hàng ngàn máy chủ ảo, cụm Kubernetes phân tán, mạng VPC đa vùng và cơ sở dữ liệu quy mô Petabyte, việc cấu hình thủ công qua giao diện đồ họa (**ClickOps**) hoặc các kịch bản Shell/Python tuần tự trở thành nguyên nhân hàng đầu gây ra hiện tượng **Configuration Drift** (lệch cấu hình ngầm) cùng các sự cố gián đoạn dịch vụ nghiêm trọng.

Để giải quyết triệt để bài toán này, **Infrastructure as Code (IaC)** ra đời như một tiêu chuẩn bắt buộc cho mọi kỹ sư Cloud Native, DevOps và Platform SRE hiện đại. Tuy nhiên, việc nắm vững tư duy cốt lõi **Declarative (Khai báo trạng thái mong muốn)** thay vì **Imperative (Chỉ định từng bước thực thi)** chính là ranh giới sống còn giữa một hệ thống tự phục hồi vững chắc và một đống mã nguồn bảo trì đầy rủi ro.

---

## 1. Tư Duy Cốt Lõi: Declarative vs Imperative trong Quản Trị Hạ Tầng

```mermaid
flowchart TB
    subgraph IMP["⚠️ MÔ HÌNH IMPERATIVE (MỆNH LỆNH - Ansible / Bash)"]
        direction TB
        I1["1. Gửi API kiểm tra S3 Bucket"] --> I2{"Đã tồn tại?"}
        I2 -- "Chưa có" --> I3["2. Gửi API tạo mới S3 Bucket"]
        I2 -- "Đã có" --> I4["3. Cấu hình mã hóa KMS & Policy"]
        I3 --> I4
        I4 --> I5{"Đứt mạng / OOM Crash?"}
        I5 -- "Có" --> I_ERR["❌ Rơi vào Partial State (Treo tài nguyên rác)"]
        I5 -- "Không" --> I_OK["Hoàn tất tuần tự"]
    end

    subgraph DEC["✨ MÔ HÌNH DECLARATIVE (KHAI BÁO - Terraform Desired State)"]
        direction TB
        D1["📄 <b>Khai báo Desired State trong HCL</b><br/><code>resource 'aws_s3_bucket' 'prod'</code>"]
        D2["⚙️ <b>Terraform Core Reconcile Loop</b><br/>So khớp tự động: <code>Δ = S_desired ∖ S_actual</code>"]
        D3["☁️ <b>Cloud Provider API</b><br/>Tự động bù đắp khác biệt để hội tụ chuẩn"]
        D4["🎯 <b>Đạt Chuẩn Tuyệt Đối & Tự Phục Hồi</b><br/>Không phụ thuộc vào trạng thái chạy trước"]

        D1 --> D2
        D2 --> D3
        D3 --> D4
    end

    classDef impNode fill:#fff1f2,stroke:#e11d48,stroke-width:1.5px,color:#9f1239
    classDef decNode fill:#f0fdf4,stroke:#16a34a,stroke-width:1.5px,color:#14532d
    classDef coreNode fill:#eff6ff,stroke:#2563eb,stroke-width:1.5px,color:#1e3a8a

    class I1,I2,I3,I4,I5,I_ERR,I_OK impNode
    class D1,D3,D4 decNode
    class D2 coreNode
```

### 1.1. Bản Chất của Phương Pháp Imperative (Mệnh Lệnh)
Trong mô hình **Imperative** (điển hình như Bash Script, Python SDK Boto3, hoặc Ansible khi không thiết kế chặt chẽ tính Idempotency), kỹ sư phải mô tả **từng bước tuần tự** để đạt được kết quả:
* **Bước 1:** Gửi API kiểm tra xem S3 Bucket `enterprise-prod-data` đã tồn tại trên AWS hay chưa.
* **Bước 2:** Nếu chưa có, gửi API tạo Bucket với region `ap-southeast-1`.
* **Bước 3:** Nếu đã có, kiểm tra cấu hình Encryption và gán KMS Key.
* **Bước 4:** Nếu quá trình tạo bị lỗi giữa chừng, lập trình viên phải tự viết hàm Rollback thủ công để dọn dẹp tài nguyên rác.

> [!WARNING]
> **RỦI RO LỚN NHẤT CỦA IMPERATIVE:**
> Script mệnh lệnh không có bộ nhớ trạng thái hệ thống. Nếu script bị gián đoạn giữa chừng do đứt kết nối mạng (**Network Timeout**) hoặc hết bộ nhớ (**OOM**), hạ tầng sẽ rơi vào trạng thái dở dang (**Partial State**). Khi chạy lại script lần 2, hệ thống thường báo lỗi xung đột `ResourceAlreadyExists` hoặc sinh ra các tài nguyên mồ côi (**Orphaned Resources**) làm tăng vọt chi phí vận hành.

---

### 1.2. Tư Duy Declarative của Terraform (Khai Báo Trạng Thái Mong Muốn)
Với mô hình **Declarative** của Terraform, kỹ sư **chỉ cần mô tả trạng thái cuối cùng mong muốn ($S_{desired}$)** trong các tệp mã nguồn HCL.

Terraform Engine sẽ tự động thực hiện phép so sánh 3 ngôi giữa:
1. **$S_{desired}$ (Desired State):** Trạng thái khai báo trong code `.tf`.
2. **$S_{recorded}$ (Last Known State):** Trạng thái được lưu trong tệp `terraform.tfstate`.
3. **$S_{actual}$ (Actual State):** Trạng thái thực tế đang chạy trên Cloud API (AWS/GCP/Azure).

```mermaid
flowchart TD
    subgraph INPUTS["1. ĐẦU VÀO HỆ THỐNG (3 NGUỒN DỮ LIỆU)"]
        HCL["📄 <b>Mã Nguồn HCL (.tf)</b><br/>Trạng thái mong muốn: <code>S_desired</code>"]
        STATE["📦 <b>State Backend (S3/GCS)</b><br/>Trạng thái đã ghi nhận: <code>S_recorded</code>"]
        CLOUD["☁️ <b>Hạ Tầng Đám Mây (Cloud API)</b><br/>Trạng thái thực tế: <code>S_actual</code>"]
    end

    subgraph CORE["2. CƠ CHẾ TÍNH TOÁN (TERRAFORM CORE ENGINE)"]
        REFRESH["🔄 <b>Refresh Step</b><br/>Truy vấn Cloud API để cập nhật State mới nhất"]
        DIFF["⚖️ <b>Diff Engine</b><br/>Tính toán độ lệch: <code>Δ = S_desired ∖ S_actual</code>"]
        DAG["🕸️ <b>Đồ Thị Phụ Thuộc (DAG)</b><br/>Xác định thứ tự Create / Update / Destroy"]
    end

    subgraph ACTIONS["3. KẾ HOẠCH & THỰC THI (EXECUTION)"]
        PLAN["📋 <b>Execution Plan</b><br/>(+ Thêm mới &nbsp;|&nbsp; ~ Sửa đổi &nbsp;|&nbsp; - Xóa bỏ)"]
        APPLY["🚀 <b>Terraform Apply</b><br/>Phát lệnh song song tới AWS/GCP/Azure API"]
        NEW_STATE["💾 <b>State Backend Lock & Save</b><br/>Ghi đè trạng thái mới an toàn"]
    end

    CLOUD -->|1. Đọc thực tế| REFRESH
    STATE -->|2. Đọc bản lưu| REFRESH
    REFRESH --> DIFF
    HCL -->|3. Đọc mã HCL| DIFF
    DIFF --> DAG
    DAG --> PLAN
    PLAN --> APPLY
    APPLY --> CLOUD
    APPLY --> NEW_STATE

    classDef inputStyle fill:#f8fafc,stroke:#64748b,stroke-width:1.5px,color:#0f172a
    classDef coreStyle fill:#eff6ff,stroke:#3b82f6,stroke-width:1.5px,color:#1e3a8a
    classDef actionStyle fill:#f0fdf4,stroke:#22c55e,stroke-width:1.5px,color:#14532d

    class HCL,STATE,CLOUD inputStyle
    class REFRESH,DIFF,DAG coreStyle
    class PLAN,APPLY,NEW_STATE actionStyle
```

---

### 1.3. Mô Hình Toán Học Của Chu Trình Điều Hòa (Reconcile Loop)

Chu trình tính toán của Terraform tuân theo công thức tập hợp:

$$\Delta = S_{desired} \setminus S_{actual}$$

* **Hành động: CREATE (+)** $\Longleftrightarrow$ Thuộc tính $x \in S_{desired}$ nhưng $x \notin S_{actual}$.
* **Hành động: UPDATE (~)** $\Longleftrightarrow$ Thuộc tính $x \in S_{desired}$ và $x \in S_{actual}$ nhưng $Value_{desired}(x) \neq Value_{actual}(x)$.
* **Hành động: DESTROY (-)** $\Longleftrightarrow$ Thuộc tính $x \in S_{actual}$ nhưng $x \notin S_{desired}$ (đối với tài nguyên được Terraform quản lý).

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

Dưới đây là ma trận so sánh chi tiết giữa 4 giải pháp quản trị hạ tầng phổ biến nhất hiện nay dựa trên 10 tiêu chí kiểm định thực tế tại các môi trường chịu tải cao:

<div class="table-responsive">

| Tiêu Chí Kỹ Thuật | HashiCorp Terraform | Ansible (Red Hat) | Pulumi | AWS CloudFormation |
| :--- | :--- | :--- | :--- | :--- |
| **Triết Lý Thiết Kế** | **Declarative IaC** (Thuần Hạ Tầng) | **Config Management** (Cấu Hình OS) | **Declarative** (General Programming) | **Declarative** (Hạ Tầng AWS Native) |
| **Ngôn Ngữ Định Nghĩa** | `HCL` (HashiCorp Config Lang) | `YAML` (Playbooks & Tasks) | `TypeScript`, `Python`, `Go`, `C#` | `JSON` / `YAML` Templates |
| **Quản Lý Trạng Thái (State)** | **Explicit State File** (S3, GCS, HCP) | **Stateless** (Không có State File) | **Pulumi SaaS** / S3 Backend | Engine nội bộ AWS quản lý ngầm |
| **Phát Hiện Lệch Cấu Hình (Drift)** | Cực mạnh (`plan -refresh-only`) | Hạn chế (Dựa trên `--check` mode) | Rất mạnh (`pulumi refresh`) | Hỗ trợ qua AWS Drift Detection |
| **Tính Độc Lập Nền Tảng (Multi-Cloud)** | **Tuyệt đối** (Hơn 3.500+ Providers) | Rất tốt (OS, Docker, K8s, Cloud) | Rất tốt (Pulumi Packages) | Khóa chặt vào hệ sinh thái AWS |
| **Khả Năng Xem Trước (Preview)** | Trực quan, chính xác 100% (`plan`) | Tương đối (`--check` mode dễ sót) | Trực quan, chi tiết (`preview`) | Xem trước qua Change Sets |
| **Kiểm Soát Vòng Đời Tài Nguyên** | Lifecycle (`create_before_destroy`) | Quản lý theo Task tuần tự | Custom Resource Options | `DeletionPolicy` / `UpdateReplace` |
| **Hệ Sinh Thái Module & Registry** | **15.000+ Modules** trên Registry | Ansible Galaxy Roles | Pulumi Registry & NPM/PyPI | AWS Serverless Application Repo |
| **Khả Năng Khi Có Sự Cố Mạng** | **Khóa State an toàn** (State Locking) | Dễ gây Partial State nếu đứt mạng | Quản lý qua State Lock Backend | Rollback tự động cấp CloudFormation |
| **Trường Hợp Ứng Dụng Lý Tưởng** | Khởi tạo VPC, EKS, RDS, IAM Đa Cloud | Cài đặt Package, Nginx, Patching OS | Dev quen dùng TypeScript/Go | Dự án thuần 100% AWS |

</div>

> [!IMPORTANT]
> **QUY TẮC PHỐI HỢP VÀNG TRONG DOANH NGHIỆP:**
> Không có công cụ "vạn năng". Kiến trúc hiện đại thường sử dụng **Terraform** để khởi tạo hạ tầng nền móng (VPC, Subnet, EKS Cluster, RDS Database, IAM Roles), sau đó bàn giao thông tin cho **Ansible** để cấu hình máy chủ hoặc **Argo CD** để triển khai các ứng dụng GitOps lên Kubernetes.

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (HCL 1.7+ Breakdown)

Dưới đây là một bộ mã nguồn HCL hoàn chỉnh tuân thủ tiêu chuẩn bảo mật doanh nghiệp: Khởi tạo S3 Secure Bucket với mã hóa KMS tùy chỉnh, chặn hoàn toàn truy cập công khai và bật tính năng Object Locking chống xóa nhầm:

```hcl
# ==============================================================================
# File: versions.tf - Định nghĩa phiên bản Terraform và Remote Backend
# ==============================================================================
terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.45.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6.0"
    }
  }

  backend "s3" {
    bucket         = "showtech-prod-tfstate-ap-southeast-1"
    key            = "core/storage/s3-secure.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "showtech-prod-tflocks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = "ShowTech-Enterprise"
      CostCenter  = "Infrastructure-Core"
    }
  }
}
```

```hcl
# ==============================================================================
# File: main.tf - Tài nguyên S3 Bucket được bảo vệ nghiêm ngặt
# ==============================================================================
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# 1. Khởi tạo Khóa Mã Hóa AWS KMS Customer Managed Key (CMK)
resource "aws_kms_key" "s3_encryption_key" {
  description             = "KMS Key ma hoa du lieu cho S3 Bucket Enterprise"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Name = "s3-kms-key-${var.environment}"
  }
}

# 2. Khởi tạo S3 Bucket cốt lõi
resource "aws_s3_bucket" "secure_storage" {
  bucket        = "showtech-enterprise-data-${var.environment}-${random_string.suffix.result}"
  force_destroy = false # Ngăn chặn việc xóa nhầm bucket khi còn chứa dữ liệu

  lifecycle {
    prevent_destroy = true # Rào chắn an ninh cấp HCL cấm lệnh destroy
  }
}

# 3. Kích hoạt Versioning để lưu vết lịch sử tệp tin
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.secure_storage.id

  versioning_configuration {
    status = "Enabled"
  }
}

# 4. Ép buộc mã hóa Server-Side Encryption với KMS Key vừa tạo
resource "aws_s3_bucket_server_side_encryption_configuration" "kms_encryption" {
  bucket = aws_s3_bucket.secure_storage.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.s3_encryption_key.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true # Tiết kiệm tới 99% chi phí KMS API calls
  }
}

# 5. Chặn toàn bộ mọi hình thức Public Access (Bảo mật tuyệt đối)
resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.secure_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

```hcl
# ==============================================================================
# File: variables.tf & outputs.tf - Định nghĩa biến & Đầu ra
# ==============================================================================
variable "aws_region" {
  type        = string
  default     = "ap-southeast-1"
  description = "Khu vực AWS triển khai tài nguyên"
}

variable "environment" {
  type        = string
  default     = "production"
  description = "Môi trường triển khai (production, staging, development)"

  validation {
    condition     = contains(["production", "staging", "development"], var.environment)
    error_message = "Môi trường chỉ được phép là production, staging, hoặc development."
  }
}

output "bucket_id" {
  value       = aws_s3_bucket.secure_storage.id
  description = "Tên định danh duy nhất của S3 Bucket"
}

output "bucket_arn" {
  value       = aws_s3_bucket.secure_storage.arn
  description = "ARN của S3 Bucket phục vụ phân quyền IAM"
}

output "kms_key_arn" {
  value       = aws_kms_key.s3_encryption_key.arn
  description = "ARN của KMS Key dùng để mã hóa dữ liệu"
}
```

### Phân Tích Kỹ Thuật Từng Dòng (Line-by-Line Breakdown):
* **`prevent_destroy = true`**: Rào chắn sinh tử trong khối `lifecycle`. Khi kỹ sư vô tình chạy `terraform destroy`, Terraform sẽ lập tức dừng thực thi và báo lỗi, bảo vệ an toàn cho dữ liệu Production.
* **`bucket_key_enabled = true`**: Giảm số lượng request gửi tới dịch vụ AWS KMS bằng cách sử dụng Bucket Key ở cấp độ S3, giúp tiết kiệm hàng ngàn USD chi phí vận hành cho các bucket có hàng triệu lượt đọc/ghi mỗi ngày.
* **`default_tags`**: Tự động gắn tag đồng bộ cho 100% tài nguyên được sinh ra từ AWS Provider, phục vụ việc phân bổ chi phí (**Cost Allocation**) và kiểm toán tuân thủ (**Audit Compliance**).

---

## 4. Phân Tích Cạm Bẫy Thực Chiến: Thảm Họa "ClickOps Drift" & Mất Dữ Liệu

### Tình Huống Sự Cố Thực Tế Tại Doanh Nghiệp:
Vào lúc **02:00 sáng**, trong một đợt khắc phục sự cố khẩn cấp, một kỹ sư vận hành đã đăng nhập vào AWS Management Console và trực tiếp sửa tham số `Instance Type` của một máy chủ cơ sở dữ liệu RDS từ `db.r6g.xlarge` lên `db.r6g.2xlarge`.

Sáng hôm sau, một kỹ sư DevOps khác thực hiện việc cập nhật mã nguồn Terraform (thêm một tag giám sát) và chạy lệnh:
```bash
terraform apply -auto-approve
```

### Hậu Quả & Log Lỗi Thực Tế:

```diff
aws_db_instance.primary: Refreshing state... [id=rds-prod-postgres]

Terraform will perform the following actions:

  # aws_db_instance.primary will be updated in-place
  ~ resource "aws_db_instance" "primary" {
        id                   = "rds-prod-postgres"
-       instance_class       = "db.r6g.2xlarge"
+       instance_class       = "db.r6g.xlarge"
      ~ tags                 = {
          + "CostCenter"     = "DataPlatform"
        }
    }

Plan: 0 to add, 1 to change, 0 to destroy.

aws_db_instance.primary: Modifying... [id=rds-prod-postgres]
! [CRITICAL OUTAGE] RDS PostgreSQL Instance bị ép Restart để hạ cấu hình CPU/RAM, làm gián đoạn toàn bộ dịch vụ thanh toán trong 15 phút!
```

```mermaid
flowchart TD
    A["🕒 <b>02:00 AM: Sửa Khẩn Cấp Bằng ClickOps</b><br/>Kỹ sư trực tiếp sửa trên AWS Console: <code>r6g.xlarge ➔ r6g.2xlarge</code>"]
    B["☁️ <b>Hạ Tầng Thực Tế Bị Lệch Cấu Hình (Drift)</b><br/>S_actual = <code>r6g.2xlarge</code> | Code & State = <code>r6g.xlarge</code>"]
    C["🕘 <b>09:00 AM: CI/CD Pipeline Thực Thi Tự Động</b><br/>Kỹ sư khác chạy lệnh nguy hiểm: <code>terraform apply -auto-approve</code>"]
    D["⚙️ <b>Terraform So Khớp & Ép Về Code HCL</b><br/>Engine thấy Code ghi <code>r6g.xlarge</code> ➔ Phát lệnh hạ cấu hình RDS"]
    E["💥 <b>HẬU QUẢ SỰ CỐ NGHIÊM TRỌNG</b><br/>RDS Database bị Restart lập tức ➔ Gián đoạn thanh toán 15 phút!"]

    A --> B
    B --> C
    C --> D
    D --> E

    classDef stepNode fill:#f8fafc,stroke:#94a3b8,stroke-width:1.5px,color:#1e293b
    classDef driftNode fill:#fffbeb,stroke:#f59e0b,stroke-width:1.5px,color:#92400e
    classDef disasterNode fill:#fef2f2,stroke:#ef4444,stroke-width:2px,color:#991b1b

    class A,C stepNode
    class B,D driftNode
    class E disasterNode
```

### 5-Whys Root Cause Analysis:
1. **Tại sao cơ sở dữ liệu bị hạ cấu hình và restart?** $\rightarrow$ Vì Terraform thực thi kế hoạch đưa `instance_class` từ `db.r6g.2xlarge` về lại `db.r6g.xlarge`.
2. **Tại sao Terraform lại đưa về giá trị cũ?** $\rightarrow$ Vì trong tệp HCL, biến `instance_class` vẫn đang khai báo là `db.r6g.xlarge` (chưa được cập nhật sau sự cố đêm qua).
3. **Tại sao kỹ sư không nhìn thấy cảnh báo này trước khi apply?** $\rightarrow$ Vì lệnh áp dụng được chạy kèm cờ nguy hiểm `-auto-approve` trong pipeline mà không qua bước kiểm duyệt Execution Plan.
4. **Tại sao có sự sai lệch giữa Cloud và HCL?** $\rightarrow$ Do quy trình quản trị cho phép kỹ sư chỉnh sửa trực tiếp trên AWS Console (ClickOps) mà không đồng bộ ngược lại vào Git.
5. **Biện pháp khắc phục tận gốc (Root Cause Remedy):**
   * **Cấm hoàn toàn quyền ghi trực tiếp trên AWS Console (Enforce IaC-Only):** Thu hồi quyền chỉnh sửa thủ công của kỹ sư trên môi trường Staging/Production, chỉ cho phép thực thi thông qua CI/CD Pipeline.
   * **Chạy định kỳ kiểm tra Drift:** Sử dụng lệnh `terraform plan -refresh-only` trên pipeline tự động mỗi 30 phút để phát hiện sớm các thay đổi trái phép.
   * **Loại bỏ cờ `-auto-approve` trên Production:** Bắt buộc phải có bước kiểm duyệt Plan Review từ Tech Lead trước khi Apply.

---

## 5. Hands-on Lab: Khởi Tạo & Vận Hành Hạ Tầng Chuẩn SRE (8 Bước)

| Bước | Lệnh CLI | Mục Đích Thực Thi |
| :---: | :--- | :--- |
| **01** | `tfswitch 1.7.5` | Quản lý và kích hoạt chính xác phiên bản Terraform yêu cầu |
| **02** | `aws sts get-caller-identity` | Xác thực thông tin danh tính IAM với AWS Cloud |
| **03** | `terraform init` | Tải Provider Plugins và khởi tạo kết nối S3 Remote Backend |
| **04** | `terraform fmt -recursive && terraform validate` | Chuẩn hóa cú pháp và kiểm tra tính hợp lệ của biến/khối lệnh |
| **05** | `terraform plan -out=tfplan.binary` | Tạo bản kế hoạch thay đổi nhị phân độc lập an toàn |
| **06** | `terraform show -json tfplan.binary \| jq` | Phân tích tệp Plan dưới dạng JSON để kiểm thử an ninh tự động |
| **07** | `terraform apply tfplan.binary` | Áp dụng chính xác bản kế hoạch đã qua phê duyệt |
| **08** | `terraform state list && terraform output` | Kiểm tra danh mục tài nguyên và truy xuất các giá trị đầu ra |

```bash
# 1. Kích hoạt phiên bản Terraform và kiểm tra danh tính
tfswitch 1.7.5
terraform version
aws sts get-caller-identity

# 2. Khởi tạo, định dạng và kiểm tra cú pháp
terraform init
terraform fmt -recursive
terraform validate

# 3. Tạo kế hoạch thực thi nhị phân và xuất JSON kiểm toán
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary | jq '.resource_changes[] | {type: .type, change: .change.actions}'

# 4. Áp dụng kế hoạch chính xác & Xem output
terraform apply tfplan.binary
terraform state list
terraform output
```

---

## 6. 10 Câu Hỏi Tự Kiểm Tra Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q01</span>
    <span>Bản chất khác biệt lớn nhất giữa Declarative IaC (Terraform) và Imperative IaC (Ansible/Bash) là gì?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích & Lời Giải Kỹ Thuật</span>
  </div>
  Declarative tập trung vào <b>"Cái gì" (Desired State)</b> — kỹ sư chỉ khai báo trạng thái mong muốn cuối cùng và engine tự tính toán hành động để đạt được trạng thái đó. Trong khi Imperative tập trung vào <b>"Làm như thế nào" (Step-by-Step)</b> — kỹ sư phải tự lập trình từng bước tuần tự và tự xử lý các trường hợp lỗi hoặc điều kiện rẽ nhánh.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q02</span>
    <span>Trạng thái (State) trong Terraform đóng vai trò gì trong chu trình Reconcile Loop?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích & Lời Giải Kỹ Thuật</span>
  </div>
  State file đóng vai trò là <b>"Bản đồ ánh xạ" (Mapping Metadata)</b> giữa các tài nguyên được khai báo trong code HCL với các tài nguyên thực tế trên Cloud (Resource ID, ARN, Attributes). Không có State, Terraform không thể biết tài nguyên nào đã được tạo trước đó để thực hiện update hay destroy, dẫn đến việc tạo trùng lặp.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q03</span>
    <span>Vì sao việc chạy <code>terraform apply -auto-approve</code> trên môi trường Production bị coi là phản mẫu (Anti-Pattern)?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích & Lời Giải Kỹ Thuật</span>
  </div>
  Cờ <code>-auto-approve</code> bỏ qua bước xem xét Execution Plan của con người. Nếu trên hạ tầng thực tế đã có ai đó sửa đổi thủ công (Drift) hoặc việc đổi tên resource làm kích hoạt hành vi <b>Destroy and Recreate</b>, lệnh apply tự động có thể xóa sạch cơ sở dữ liệu hoặc cụm máy chủ quan trọng mà không có cơ hội ngăn chặn.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q04</span>
    <span>Tham số <code>prevent_destroy = true</code> trong khối <code>lifecycle</code> hoạt động như thế nào?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích & Lời Giải Kỹ Thuật</span>
  </div>
  Đây là một cơ chế an toàn cấp độ engine. Nếu một kế hoạch thực thi (Plan) dẫn tới việc xóa tài nguyên có khai báo <code>prevent_destroy = true</code> (dù là do lệnh <code>terraform destroy</code> trực tiếp hay do thay đổi một thuộc tính bắt buộc phải Re-create), Terraform sẽ lập tức dừng lại và báo lỗi, từ chối tạo Plan.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q05</span>
    <span>Lệnh <code>terraform plan -refresh-only</code> khác gì so với <code>terraform plan</code> thông thường?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích & Lời Giải Kỹ Thuật</span>
  </div>
  <code>terraform plan -refresh-only</code> chỉ thực hiện việc truy vấn Cloud API để cập nhật trạng thái thực tế vào State mà <b>không đề xuất bất kỳ thay đổi nào lên hạ tầng thực tế</b>. Lệnh này được dùng chuyên biệt để phát hiện và đồng bộ Drift do ClickOps gây ra.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q06</span>
    <span>Thuộc tính <code>bucket_key_enabled = true</code> trong cấu hình mã hóa S3 mang lại lợi ích gì?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích & Lời Giải Kỹ Thuật</span>
  </div>
  Thuộc tính này giảm tần suất gọi API tới AWS KMS bằng cách sử dụng một khóa cấp bucket ngắn hạn thay vì gọi KMS cho từng đối tượng riêng lẻ. Điều này giúp giảm chi phí dịch vụ KMS tới <b>99%</b> đối với các hệ thống có khối lượng đọc/ghi tệp lớn.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q07</span>
    <span>Khi nào nên sử dụng Pulumi thay vì Terraform trong các dự án Cloud Native?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích & Lời Giải Kỹ Thuật</span>
  </div>
  Nên cân nhắc Pulumi khi hạ tầng đòi hỏi các thuật toán điều kiện phức tạp, xử lý chuỗi dữ liệu động nâng cao, tích hợp sâu vào mã nguồn ứng dụng (viết bằng TypeScript/Python/Go), hoặc khi đội ngũ kỹ sư phần mềm muốn sử dụng chung ngôn ngữ và bộ công cụ kiểm thử đơn vị (Unit Test) của ngôn ngữ lập trình đa năng.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q08</span>
    <span>Hiện tượng "Index Shifting" trong Terraform là gì và công cụ nào giải quyết triệt để?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích & Lời Giải Kỹ Thuật</span>
  </div>
  Index Shifting xảy ra khi sử dụng <code>count</code> để tạo danh sách tài nguyên dựa trên chỉ số mảng <code>[0, 1, 2]</code>. Khi xóa một phần tử ở giữa danh sách, toàn bộ các phần tử phía sau bị dịch chuyển index, khiến Terraform hiểu nhầm là phải destroy và recreate lại hàng loạt tài nguyên. Giải pháp là chuyển sang dùng <code>for_each</code> với cấu trúc Map/Set.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q09</span>
    <span>Lệnh <code>terraform validate</code> kiểm tra những gì và nó có gọi tới Cloud API hay không?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích & Lời Giải Kỹ Thuật</span>
  </div>
  <code>terraform validate</code> chỉ kiểm tra tính hợp lệ về mặt cú pháp HCL, tính nhất quán của các khối khai báo, các kiểu dữ liệu biến và tham số nội bộ. Lệnh này <b>hoàn toàn không gọi tới Cloud API</b> và không kiểm tra xem tài nguyên thực tế có tồn tại hay không.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q10</span>
    <span>State Locking (Khóa trạng thái) hoạt động như thế nào khi nhiều kỹ sư cùng chạy Terraform?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích & Lời Giải Kỹ Thuật</span>
  </div>
  Khi một kỹ sư phát lệnh <code>plan</code> hoặc <code>apply</code>, Terraform sẽ tạo một bản ghi khóa (Lock Record) trên cơ chế khóa của Backend (ví dụ DynamoDB Lock Table hoặc GCS Lock). Mọi lệnh khác chạy đồng thời sẽ bị chặn lại với thông báo <code>Error acquiring the state lock</code> cho đến khi tiến trình đầu tiên hoàn tất và nhả khóa, ngăn chặn nguy cơ làm hỏng (Corrupt) State File.
</div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

Tư duy **Declarative Desired State** là nền móng tư tưởng quan trọng nhất giúp bạn làm chủ toàn bộ hệ sinh thái Terraform. Hiểu rõ chu trình Reconcile Loop và mối liên hệ giữa Code HCL, State File và Cloud Actual State sẽ giúp bạn luôn tự tin trước mọi thay đổi hạ tầng phức tạp.

> [!TIP]
> **BÀI HỌC TIẾP THEO:**
> Trong **[Bài 02] Giải Mã Workflow Init, Plan, Apply - Cơ Chế Two-Phase Execution & Đồ Thị DAG Chuyên Sâu**, chúng ta sẽ mở nắp "cỗ máy bên trong" của Terraform Core: Khám phá cách đồ thị có hướng không chu trình (**DAG**) được xây dựng, cơ chế Provider Plugin RPC qua gRPC và cách tối ưu hóa hiệu năng song song với `-parallelism`.
{% endraw %}
