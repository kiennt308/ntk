---
layout: post
title: "[Bài 05] Thiết Kế Variables, Locals & Outputs Chuẩn Enterprise: Validation,"
date: 2026-09-09 08:00:00 +0700
categories: [Terraform]
tags:
  - Terraform
  - IaC
  - DevOps
  - CloudNative
  - Part-05
series: "Terraform Enterprise Architecture"
series_order: 5
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80"
summary: "Quy chuẩn thiết kế Input Variables có Custom Validation Rules bằng Regex,"
---

{% raw %}
# Thiết Kế Variables, Locals & Outputs Chuẩn Enterprise: Validation, Precedence & Sensitive Masking

Trong các dự án hạ tầng doanh nghiệp quy mô lớn với hàng chục môi trường phân tán (Dev, Staging, UAT, Production), việc quản lý các tham số đầu vào (**Input Variables**), tính toán các giá trị trung gian bất biến (**Locals**) và chia sẻ dữ liệu liên kết giữa các tầng hạ tầng (**Outputs**) đòi hỏi một tiêu chuẩn kiến trúc phần mềm nghiêm ngặt.

Nếu thiếu cơ chế kiểm định dữ liệu đầu vào (**Custom Validation Rules**) và kiểm soát quyền hiển thị dữ liệu nhạy cảm (**Sensitive Data Masking**), hệ thống của bạn sẽ đối mặt với những nguy cơ bảo mật nghiêm trọng: Rò rỉ mật khẩu quản trị cơ sở dữ liệu trên log công khai của hệ thống CI/CD (GitHub Actions / GitLab CI) hoặc gây sập toàn bộ chu trình triển khai do nhập sai định dạng dải mạng CIDR.

Bài viết này sẽ hướng dẫn bạn thiết lập toàn bộ quy chuẩn thiết kế **Variables, Locals và Outputs** chuyên nghiệp: Giải mã quy tắc phân tầng ưu tiên 5 cấp độ (**Variable Precedence**), viết biểu thức kiểm định nâng cao với Regex và `can()`, tối ưu hóa `locals` theo nguyên lý DRY và làm chủ kỹ thuật che giấu bí mật chuẩn SRE.

---

## 1. Thứ Tự Ưu Tiên Giá Trị Biến (Variable Precedence 5 Cấp Độ)

Khi cùng một biến được gán giá trị ở nhiều nguồn khác nhau, Terraform sẽ giải quyết xung đột dựa trên thứ tự ưu tiên nghiêm ngặt từ thấp đến cao (cấp sau ghi đè cấp trước):

```mermaid
graph TD
    V1["1. Giá trị mặc định (default trong variables.tf)<br/>[ƯU TIÊN THẤP NHẤT]"] --> V2["2. Biến môi trường hệ điều hành: TF_VAR_name"]
    V2 --> V3["3. Tệp cấu hình terraform.tfvars"]
    V3 --> V4["4. Tệp tự động *.auto.tfvars hoặc *.auto.tfvars.json"]
    V4 --> V5["5. Tham số dòng lệnh CLI: -var hoặc -var-file<br/>[ƯU TIÊN CAO NHẤT - GHI ĐÈ TẤT CẢ]"]


```

### Bảng Chi Tiết Cơ Chế Nạp & Ghi Đè Biến:

| Cấp Độ Ưu Tiên | Nguồn Nạp Biến | Cú Pháp Khai Báo / Thực Thi | Trường Hợp Sử Dụng Thực Tế |
| :---: | :--- | :--- | :--- |
| **1 (Thấp nhất)** | `default` attribute | `variable "region" { default = "ap-southeast-1" }` | Cung cấp giá trị an toàn khi người dùng không truyền |
| **2** | Environment Variables | `export TF_VAR_environment="staging"` | Nạp cấu hình động từ môi trường Runner trong CI/CD |
| **3** | `terraform.tfvars` | File text tĩnh `environment = "production"` | Cấu hình mặc định của một Workspace cụ thể |
| **4** | `*.auto.tfvars` | File `01-common.auto.tfvars`, `02-network.auto.tfvars` | Nạp tự động theo thứ tự từ điển chữ cái (Alphabet) |
| **5 (Cao nhất)** | CLI `-var` / `-var-file` | `terraform apply -var-file="env/prod.tfvars"` | Ghi đè tuyệt đối trong các đợt phát hành Release khẩn cấp |

---

## 2. Bảng So Sánh Kiến Trúc: Variables vs Locals vs Outputs

| Đặc Điểm Kỹ Thuật | Input Variables (`variable`) | Local Values (`locals`) | Output Values (`output`) |
| :--- | :--- | :--- | :--- |
| **Mục Đích Thiết Kế** | Nhận tham số cấu hình từ bên ngoài truyền vào Module | Biến trung gian tính toán nội bộ trong Module | Xuất dữ liệu ra ngoài cho người dùng hoặc Module khác |
| **Khả Năng Thay Đổi** | Có thể ghi đè bởi người gọi Module qua `.tfvars` | Bất biến (Immutable), không thể bị ghi đè từ bên ngoài | Được tính toán động từ tài nguyên sau khi apply |
| **Kiểm Định Dữ Liệu** | Hỗ trợ khối `validation` với biểu thức điều kiện | Không hỗ trợ khối validation riêng biệt | Hỗ trợ `precondition` và `postcondition` |
| **Bảo Mật Nhạy Cảm** | Hỗ trợ cờ `sensitive = true` | Tự động kế thừa tính chất sensitive | Hỗ trợ cờ `sensitive = true` để che giấu trên log |
| **Nguyên Tắc DRY** | Đóng vai trò là Interface API của Module | Triệt tiêu lặp code, tập trung logic tính toán | Đóng vai trò là Data Contract giữa các tầng hạ tầng |

---

## 3. Thiết Lập Custom Validation Rules Chuyên Sâu Cho Input Variables

Từ Terraform 0.13+, bạn có thể định nghĩa một hoặc nhiều khối `validation` trong từng biến để phát hiện sớm các lỗi sai cấu hình ngay tại bước `terraform plan`:

### 3.1. Kiểm Tra Giá Trị Thuộc Danh Sách Trắng (Whitelist with `contains`)
```hcl
variable "environment" {
  type        = string
  description = "Môi trường triển khai hạ tầng"
  nullable    = false # Cấm truyền giá trị null (Terraform 1.1+)

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Môi trường không hợp lệ! Giá trị bắt buộc phải là 'development', 'staging' hoặc 'production'."
  }
}
```

### 3.2. Kiểm Tra Định Dạng CIDR IPv4 Hợp Lệ (Network Validation with `can`)
```hcl
variable "vpc_cidr" {
  type        = string
  description = "Địa chỉ IPv4 CIDR Block của mạng VPC"

  validation {
    # Kiểm tra tính hợp lệ của IP và Subnet Mask tối thiểu /24
    condition = (
      can(cidrnetmask(var.vpc_cidr)) &&
      tonumber(split("/", var.vpc_cidr)[1]) >= 16 &&
      tonumber(split("/", var.vpc_cidr)[1]) <= 24
    )
    error_message = "VPC CIDR phải là dải IPv4 hợp lệ với độ dài Subnet Mask trong khoảng từ /16 đến /24."
  }
}
```

### 3.3. Kiểm Định Tên Tài Nguyên Theo Chuẩn Regex (Enterprise Naming Convention)
```hcl
variable "project_code" {
  type        = string
  description = "Mã định danh dự án (Chỉ chấp nhận chữ thường và số, độ dài 3-8 ký tự)"

  validation {
    condition     = can(regex("^[a-z0-9]{3,8}$", var.project_code))
    error_message = "Mã dự án phải từ 3 đến 8 ký tự, chỉ bao gồm chữ cái viết thường và số (Ví dụ: 'core01', 'payapi')."
  }
}
```

---

## 4. Tối Ưu Hóa Local Values (DRY & Logic Centralization)

`locals` là công cụ trung tâm để chuẩn hóa tên tài nguyên, thống nhất thẻ phân loại chi phí (Cost Tags) và xử lý các điều kiện rẽ nhánh theo môi trường:

```hcl
locals {
  # Chuẩn hóa tiền tố định danh tài nguyên (Naming Convention)
  name_prefix = "showtech-${var.project_code}-${var.environment}"

  # Logic cấu hình tự động co giãn theo môi trường
  is_production = var.environment == "production"

  db_instance_class = local.is_production ? "db.r6g.xlarge" : "db.t4g.medium"
  allocated_storage = local.is_production ? 200 : 20
  multi_az_enabled  = local.is_production ? true : false

  # Thống nhất hệ thống thẻ quản trị doanh nghiệp (FinOps & Compliance)
  common_tags = {
    Project     = var.project_code
    Environment = var.environment
    ManagedBy   = "Terraform"
    CostCenter  = local.is_production ? "Production-Core" : "Engineering-Dev"
    CreatedDate = "2026-09-05"
  }
}
```

---

## 5. Bảo Vệ Dữ Liệu Nhạy Cảm Với `sensitive = true`

> [!CAUTION]
> **RỦI RO RÒ RỈ SECRET TRÊN CI/CD LOGS:**
> Mọi chuỗi mật khẩu Database, Private Key TLS, hoặc OAuth Secret nếu không được đánh dấu `sensitive = true` sẽ bị in trực tiếp dưới dạng văn bản thô (Plain Text) trên màn hình Terminal và bản ghi log của GitHub Actions / GitLab CI, vi phạm nghiêm trọng tiêu chuẩn an ninh SOC 2 và PCI-DSS.

```mermaid
flowchart LR
    SECRET["Password Generator / RDS Master Password"] --> MASK{Cờ sensitive = true}
    MASK -->|BẬT (sensitive=true)| CLI_SAFE["Màn hình CLI / CI Logs: (sensitive value) [AN TOÀN]"]
    MASK -->|TẮT (sensitive=false)| CLI_DANGER["Màn hình CLI / CI Logs: 'SuperSecretPass123!' [NGUY HIỂM]"]


```

---

## 6. Kiến Trúc Mẫu Triển Khai RDS Database Với Variables & Outputs Bảo Mật

Dưới đây là một bộ mã nguồn HCL hoàn chỉnh tuân thủ 100% tiêu chuẩn thiết kế:

```hcl
# main.tf - Triển khai RDS Database Enterprise với Validation và Sensitive Masking
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
}

provider "aws" {
  region = var.aws_region
}

# 1. Tự động sinh mật khẩu ngẫu nhiên phức tạp cho Database
resource "random_password" "db_master_password" {
  length           = 24
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# 2. Khởi tạo Khóa KMS bảo vệ Database Storage
resource "aws_kms_key" "db_kms" {
  description             = "KMS Key ma hoa cho Database ${local.name_prefix}"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = local.common_tags
}

# 3. Khởi tạo Cơ sở dữ liệu AWS RDS Postgres
resource "aws_db_instance" "postgres" {
  identifier     = "${local.name_prefix}-postgres"
  engine         = "postgres"
  engine_version = "16.2"
  instance_class = local.db_instance_class

  allocated_storage     = local.allocated_storage
  max_allocated_storage = local.is_production ? 1000 : 100
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id            = aws_kms_key.db_kms.arn

  db_name  = "appdb"
  username = "dbadmin"
  password = random_password.db_master_password.result # Dữ liệu nhạy cảm

  multi_az            = local.multi_az_enabled
  publicly_accessible = false
  skip_final_snapshot = !local.is_production

  tags = local.common_tags
}
```

```hcl
# outputs.tf - Xuất các giá trị an toàn
output "db_endpoint" {
  value       = aws_db_instance.postgres.endpoint
  description = "Địa chỉ kết nối máy chủ Database (Host:Port)"
}

output "db_master_username" {
  value       = aws_db_instance.postgres.username
  description = "Tên tài khoản quản trị Database"
}

output "db_master_password" {
  value       = aws_db_instance.postgres.password
  description = "Mật khẩu quản trị Database (Được bảo vệ nghiêm ngặt)"
  sensitive   = true # BẮT BUỘC: Che giấu giá trị trên CLI và CI/CD Logs
}
```

---

## 7. Phân Tích Cạm Bẫy Thực Chiến: Lỗi Rò Rỉ Secret & Validation Failure

### Tình Huống Sự Cố Thực Tế:
Một nhóm kỹ sư phát triển triển khai hệ thống thông báo nội bộ. Kỹ sư đã xuất thông tin kết nối Database qua `output "connection_string"` mà quên không đánh dấu `sensitive = true`.

Khi pipeline CI/CD chạy lệnh `terraform apply`, toàn bộ chuỗi kết nối chứa mật khẩu rõ ràng:
```log
# Trích đoạn log nguy hiểm bị rò rỉ trên GitLab CI Runner công khai
Outputs:

db_endpoint = "showtech-payapi-prod-postgres.c9a1b2c3d4.ap-southeast-1.rds.amazonaws.com:5432"
db_master_username = "dbadmin"
connection_string = "postgresql://dbadmin:P%40ssw0rd99Enterprise%21@showtech-payapi-prod-postgres:5432/appdb"
```

### 5-Whys Root Cause Analysis:
1. **Tại sao mật khẩu quản trị bị lộ trên log CI/CD?** $\rightarrow$ Vì chuỗi `connection_string` được in ra màn hình ở phần Outputs sau khi apply.
2. **Tại sao Terraform lại in ra màn hình?** $\rightarrow$ Vì trong khối `output "connection_string"`, kỹ sư không khai báo thuộc tính `sensitive = true`.
3. **Tại sao Terraform không tự động phát hiện secret?** $\rightarrow$ Khi bạn ghép mật khẩu vào một chuỗi String mới (`"postgresql://${user}:${pass}@..."`), Terraform có thể mất dấu cờ sensitive nếu không gán cờ tường minh trên Output.
4. **Tại sao việc này lại qua được bước Code Review?** $\rightarrow$ Do nhóm chưa tích hợp công cụ kiểm tra tĩnh (Static Analysis Linter) như `tflint` hoặc `tfsec` để quét lỗi thiếu sensitive flag.
5. **Biện pháp khắc phục chuẩn SRE:**
   - **Gán `sensitive = true` cho mọi Output chứa secret.**
   - **Xoay vòng mật khẩu (Rotate Password) khẩn cấp** cho Database ngay lập tức.
   - **Tích hợp `tfsec` / `trivy` vào Pre-commit Hook** để tự động chặn các commit thiếu cờ sensitive.

---

## 8. Hands-on Lab: Thử Nghiệm Precedence, Validation & Sensitive Masking (8 Bước)

### Bước 1: Khởi tạo thư mục thực hành
```bash
mkdir -p /tmp/terraform-vars-lab && cd /tmp/terraform-vars-lab
terraform init
```

### Bước 2: Tạo tệp `variables.tf` có chứa Custom Validation
```bash
cat << 'EOF' > variables.tf
variable "environment" {
  type    = string
  default = "development"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Môi trường không hợp lệ! Chỉ chấp nhận: development, staging, production."
  }
}

variable "secret_token" {
  type      = string
  sensitive = true
}
EOF
```

### Bước 3: Tạo tệp `main.tf` và `outputs.tf`
```bash
cat << 'EOF' > main.tf
locals {
  app_name = "demo-app-${var.environment}"
}

output "application_name" {
  value = local.app_name
}

output "masked_secret" {
  value     = var.secret_token
  sensitive = true
}
EOF
```

### Bước 4: Thử nghiệm Validation Failure (Nhập sai môi trường)
```bash
# Cố tình truyền môi trường không hợp lệ
terraform plan -var="environment=testing" -var="secret_token=MySecret123"
```
Quan sát Terraform lập tức chặn lại và in ra thông báo: `Error: Invalid value for variable: Môi trường không hợp lệ!`.

### Bước 5: Thử nghiệm Variable Precedence Cấp Độ `TF_VAR_`
```bash
export TF_VAR_environment="staging"
export TF_VAR_secret_token="SecretFromEnvVar"

terraform plan
```
Quan sát `application_name` hiển thị giá trị `"demo-app-staging"`.

### Bước 6: Thử nghiệm Ghi Đè Cấp Cao Hơn Bằng CLI `-var`
```bash
terraform plan -var="environment=production"
```
Quan sát giá trị từ CLI (`production`) ghi đè thành công biến môi trường `TF_VAR_` (`staging`).

### Bước 7: Quan sát cơ chế che giấu Sensitive Output
```bash
terraform apply -auto-approve
```
Quan sát kết quả đầu ra:
```text
Outputs:

application_name = "demo-app-production"
masked_secret = <sensitive>
```

### Bước 8: Truy xuất an toàn giá trị Sensitive khi cần thiết
```bash
# Trích xuất giá trị thực tế của biến sensitive cho script tự động
terraform output -raw masked_secret
echo ""

# Dọn dẹp môi trường
cd .. && rm -rf /tmp/terraform-vars-lab
```

---

## 9. 10 Câu Hỏi Tự Kiểm Tra Chuyên Sâu (Self-Check Q&A)

### Câu 1: Thứ tự ưu tiên nạp biến trong Terraform được sắp xếp như thế nào từ thấp đến cao?
<details>
<summary><b>Xem lời giải chi tiết</b></summary>
Thứ tự ưu tiên từ thấp đến cao: (1) Giá trị <code>default</code> trong <code>variables.tf</code> $\rightarrow$ (2) Biến môi trường <code>TF_VAR_name</code> $\rightarrow$ (3) Tệp <code>terraform.tfvars</code> $\rightarrow$ (4) Tệp <code>*.auto.tfvars</code> $\rightarrow$ (5) Tham số CLI <code>-var</code> hoặc <code>-var-file</code>.
</details>

### Câu 2: Khối `validation` trong Input Variable được kích hoạt tại thời điểm nào?
<details>
<summary><b>Xem lời giải chi tiết</b></summary>
Được kích hoạt ngay trong <b>Pha Plan (hoặc khi chạy `terraform validate`)</b> trước khi Terraform gửi bất kỳ API request nào lên Cloud Provider, giúp tiết kiệm thời gian và ngăn chặn lỗi cấu hình sai từ sớm.
</details>

### Câu 3: Thuộc tính `nullable = false` trong khai báo `variable` có tác dụng gì từ Terraform 1.1+?
<details>
<summary><b>Xem lời giải chi tiết</b></summary>
Mặc định trong Terraform, nếu một biến có giá trị default nhưng người dùng cố tình truyền <code>null</code>, biến đó sẽ nhận giá trị <code>null</code>. Thiết lập <code>nullable = false</code> buộc Terraform phải từ chối giá trị null và tự động fallback về giá trị <code>default</code>.
</details>

### Câu 4: Sự khác nhau cơ bản giữa `variable` và `locals` là gì?
<details>
<summary><b>Xem lời giải chi tiết</b></summary>
- <code>variable</code> đóng vai trò là tham số đầu vào (Input Parameter) mà người gọi module có thể truyền vào và ghi đè.<br/>
- <code>locals</code> là biến nội bộ bất biến (Internal Constants), chỉ có thể được đọc và tính toán bên trong module đó, không thể bị ghi đè từ bên ngoài.
</details>

### Câu 5: Cờ `sensitive = true` trên Output có thực sự mã hóa dữ liệu trong State file không?
<details>
<summary><b>Xem lời giải chi tiết</b></summary>
<b>KHÔNG</b>. Cờ <code>sensitive = true</code> chỉ có tác dụng <b>che giấu giá trị hiển thị trên màn hình CLI, console và bản ghi log CI/CD</b> (hiển thị thành <code>(sensitive value)</code>). Dữ liệu này vẫn được lưu trữ dưới dạng văn bản thô (Plain Text) bên trong tệp <code>terraform.tfstate</code>. Do đó, State Backend bắt buộc phải được mã hóa tại chỗ (SSE-KMS/AES-256).
</details>

### Câu 6: Làm thế nào để lấy giá trị thực của một Sensitive Output trong Bash script tự động?
<details>
<summary><b>Xem lời giải chi tiết</b></summary>
Sử dụng cờ <code>-raw</code> trong lệnh output: <code>terraform output -raw <output_name></code> hoặc xuất định dạng JSON: <code>terraform output -json <output_name> | jq -r .</code>.
</details>

### Câu 7: Hàm `can(expression)` thường được dùng kết hợp với hàm nào trong khối validation?
<details>
<summary><b>Xem lời giải chi tiết</b></summary>
Thường được dùng kết hợp với các hàm phân tích chuỗi như <code>regex()</code>, <code>cidrnetmask()</code>, hoặc <code>tonumber()</code>. Nếu biểu thức bên trong gặp lỗi cú pháp (ví dụ regex không khớp), hàm <code>can()</code> sẽ bắt lỗi an toàn và trả về <code>false</code> thay vì làm sập toàn bộ tiến trình Terraform.
</details>

### Câu 8: Tại sao việc sử dụng `locals` để chuẩn hóa Resource Naming lại quan trọng trong doanh nghiệp?
<details>
<summary><b>Xem lời giải chi tiết</b></summary>
Giúp đảm bảo 100% tài nguyên hạ tầng tuân thủ đúng quy chuẩn đặt tên thống nhất (ví dụ <code>company-project-env-resource</code>). Khi cần thay đổi quy tắc đặt tên, kỹ sư chỉ cần chỉnh sửa tại 1 dòng duy nhất trong khối <code>locals</code> thay vì phải sửa hàng trăm tài nguyên phân tán.
</details>

### Câu 9: Điều gì xảy ra nếu bạn truyền một biến có cờ `sensitive = true` vào một resource tag?
<details>
<summary><b>Xem lời giải chi tiết</b></summary>
Toàn bộ resource tag và bất kỳ resource nào tham chiếu tới tag đó sẽ tự động bị Terraform đánh dấu là <b>Sensitive</b>, khiến các output liên quan cũng bị ẩn đi để tránh rò rỉ bắc cầu.
</details>

### Câu 10: Tệp `*.auto.tfvars.json` có ưu điểm gì so với tệp `*.auto.tfvars` thông thường?
<details>
<summary><b>Xem lời giải chi tiết</b></summary>
Định dạng JSON cho phép các công cụ tự động hóa hoặc script lập trình bên ngoài (Python, Go, Node.js) dễ dàng sinh ra (generate) các tệp biến cấu hình một cách có cấu trúc mà không cần phải viết parser định dạng HCL riêng.
</details>

---

## 10. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

Khép lại **Giai Đoạn 1: Nền Tảng Cốt Lõi**, bạn đã hoàn toàn làm chủ tư duy Declarative IaC, cơ chế Two-Phase DAG Engine, hệ thống kiểu dữ liệu HCL, nghệ thuật quản trị Dependency và thiết kế Variables/Outputs chuẩn Enterprise.

Trong **Giai Đoạn 2 (Quản Trị State & Modules)** mở đầu với **[Bài 06: Giải Mã Cấu Trúc Terraform State: JSON Schema v4, Serial Counter, Lineage & Cơ Chế Refresh-Only](06-giai-ma-terraform-state-cau-truc-json-v4-drift-detection-refresh-only.md)**, chúng ta sẽ bước vào "trái tim" của mọi hệ thống Terraform: Phẫu thuật từng trường dữ liệu trong tệp State JSON v4, giải mã các tham số bí mật `serial`, `lineage`, và cách giải cứu hạ tầng khi State File bị phân mảnh!
{% endraw %}
