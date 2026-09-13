---
layout: post
title: "[Bài 04] Làm Chủ Dependency Graph (DAG): Quản Lý Phụ Thuộc Tường Minh vs Ngầm Định & Data Sources"
date: 2026-09-13 11:30:00 +0700
categories: [Terraform]
tags:
  - Terraform
  - IaC
  - DevOps
  - CloudNative
  - Part-04
series: "Terraform Enterprise Architecture"
series_order: 4
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80"
summary: "Phân tích sâu cơ chế tự động xây dựng đồ thị DAG trong Terraform Core, phân biệt Implicit vs Explicit Dependencies, quản lý Data Sources an toàn và kỹ thuật bẻ gãy vòng lặp phụ thuộc 2 chiều."
tldr:
  - "Cơ chế đồ thị DAG: Terraform Core mô hình hóa tài nguyên thành các Node và quan hệ thành Edges, xác định thứ tự tạo (+) xuôi và thứ tự hủy (-) ngược theo LIFO."
  - "Implicit vs Explicit: Luôn ưu tiên Implicit References (truyền ID trực tiếp) để tối đa hóa luồng song song; chỉ dùng depends_on cho các side-effects logic."
  - "Phá vỡ Cyclic Dependency: Tách rời các inline rules trong Security Groups thành các resource aws_security_group_rule độc lập để triệt tiêu quan hệ phụ thuộc chéo 2 chiều."
  - "Cạm bẫy Data Sources: Tuyệt đối không dùng Data Source để truy vấn lại tài nguyên vừa tạo trong cùng một State tại pha Plan để tránh lỗi Deferred/Unknown."
---
{% raw %}
# Làm Chủ Dependency Graph (DAG): Quản Lý Phụ Thuộc Tường Minh vs Ngầm Định & Data Sources

Trong một hệ thống hạ tầng đám mây đa tầng (Multi-Tier Enterprise Infrastructure), mối quan hệ phụ thuộc giữa các thành phần là vô cùng chằng chịt: *EC2 Instance bắt buộc phải đặt trong Subnet, Subnet phải gắn vào VPC, Security Group Rule cần ID của Security Group, và Kubernetes EKS Node Group chỉ có thể khởi động sau khi IAM Policy Attachment đã hoàn tất trên AWS IAM Service*.

Terraform Core xử lý mạng lưới phụ thuộc phức tạp này một cách tự động và chuẩn xác thông qua cấu trúc dữ liệu **Đồ thị không tuần hoàn có hướng (Directed Acyclic Graph - DAG)**. Tuy nhiên, việc hiểu sai cơ chế dựng đồ thị (đặc biệt là lạm dụng từ khóa `<code style="color: var(--accent-rose); font-weight: 700;">depends_on</code>`, khai báo quan hệ phụ thuộc chéo hoặc sử dụng Data Sources phụ thuộc vào giá trị động chưa xác định tại pha Plan) là nguyên nhân hàng đầu phá hủy khả năng thực thi song song (`parallelism`), gây kéo dài thời gian deploy hoặc dẫn tới lỗi nghiêm trọng <strong style="color: var(--accent-rose);">Cyclic Dependency</strong>.

Bài viết này sẽ hướng dẫn bạn giải phẫu cấu trúc DAG trong Terraform Core, phân biệt rạch ròi giữa <strong style="color: var(--accent-primary);">Phụ thuộc ngầm định (Implicit)</strong> và <strong style="color: var(--accent-amber);">Phụ thuộc tường minh (Explicit)</strong>, làm chủ cơ chế nạp dữ liệu của <strong style="color: var(--accent-cyan);">Data Sources</strong> và kỹ thuật phá vỡ vòng lặp phụ thuộc 2 chiều.

---

## 1. Cơ Chế Xây Dựng Đồ Thị DAG Trong Terraform Core

Mỗi tài nguyên khai báo trong mã nguồn HCL được biểu diễn như một **Node (Đỉnh)** trên đồ thị, và các mối quan hệ phụ thuộc giữa chúng được biểu diễn bằng các **Directed Edges (Cạnh có hướng)**:

```mermaid
graph TD
    subgraph IMPLICIT["1. PHỤ THUỘC NGẦM ĐỊNH (Implicit Reference)"]
        VPC["aws_vpc.main"] -->|"vpc_id = aws_vpc.main.id"| SUB["aws_subnet.public"]
        SUB -->|"subnet_id = aws_subnet.public.id"| EC2["aws_instance.app_server"]
    end

    subgraph EXPLICIT["2. PHỤ THUỘC TƯỜNG MINH (Explicit depends_on)"]
        S3["aws_s3_bucket.audit_logs"] -.->|"depends_on = [aws_s3_bucket.audit_logs]"| ROLE["aws_iam_role.app_role"]
        POLICY["aws_iam_policy_attachment.attach"] -.->|"depends_on = [aws_iam_policy_attachment.attach]"| EKS_NODES["aws_eks_node_group.workers"]
    end

    subgraph DATA_SRC["3. TRUY VẤN DỮ LIỆU ĐỘNG (Data Sources)"]
        AWS_AMI["data.aws_ami.ubuntu"] -->|"ami = data.aws_ami.ubuntu.id"| EC2
        AWS_VPC["data.aws_vpc.existing_vpc"] -->|"vpc_id = data.aws_vpc.existing_vpc.id"| SG["aws_security_group.db_sg"]
    end

    style VPC fill:none,stroke:#3b82f6,stroke-width:2px
    style SUB fill:none,stroke:#0ea5e9,stroke-width:2px
    style EC2 fill:none,stroke:#10b981,stroke-width:2px
    style S3 fill:none,stroke:#f59e0b,stroke-width:2px
    style ROLE fill:none,stroke:#8b5cf6,stroke-width:2px
    style POLICY fill:none,stroke:#ec4899,stroke-width:2px
    style EKS_NODES fill:none,stroke:#10b981,stroke-width:2px
    style AWS_AMI fill:none,stroke:#06b6d4,stroke-width:2px
    style AWS_VPC fill:none,stroke:#06b6d4,stroke-width:2px
    style SG fill:none,stroke:#f59e0b,stroke-width:2px
```

---

## 2. Bảng So Sánh Ba Phương Thức Quản Lý Phụ Thuộc

| Tiêu Chí Kỹ Thuật | Phụ Thuộc Ngầm Định (Implicit) | Phụ Thuộc Tường Minh (`depends_on`) | Data Source References |
| :--- | :--- | :--- | :--- |
| **Cơ Chế Nhận Diện** | Tự động phân tích từ cú pháp `${resource.name.attr}` | Kỹ sư khai báo thủ công trong khối `depends_on = [...]` | Truy vấn API đám mây thông qua khối `data "type" "name"` |
| **Tối Ưu Thực Thi Song Song** | <b style="color: var(--accent-emerald);">Tối đa</b> (Chỉ khóa chính xác thuộc tính cần thiết) | <b style="color: var(--accent-rose);">Kém</b> (Khóa toàn bộ Node, làm tuần tự hóa DAG) | <b style="color: var(--accent-cyan);">Tối ưu</b> nếu Data Source không phụ thuộc giá trị động |
| **Thứ Tự Hủy Tài Nguyên (`destroy`)** | Tự động đảo ngược 100% theo thứ tự LIFO | Tự động đảo ngược theo danh sách khai báo | Không bị ảnh hưởng (Data Source là Read-Only) |
| **Nguy Cơ Gây Lỗi Cycle** | Thấp (Dễ phát hiện khi code) | <b style="color: var(--accent-amber);">Cao</b> (Dễ vô tình tạo quan hệ chéo đa module) | <b style="color: var(--accent-rose);">Rất cao</b> nếu Data Source phụ thuộc Resource mới tạo |
| **Khuyến Nghị Thiết Kế** | <span class="badge badge--emerald">Khuyến nghị 95%</span> Ưu tiên hàng đầu | <span class="badge badge--amber">Cân nhắc kỹ</span> Chỉ dùng cho Side-effects | <span class="badge badge--cyan">Tích hợp sẵn</span> Dùng cho hạ tầng chia sẻ có sẵn |

> [!IMPORTANT]
> **NGUYÊN TẮC THIẾT KẾ DAG TINH GỌN:**
> Luôn ưu tiên sử dụng **Implicit Dependency** thông qua việc truyền tham chiếu trực tiếp `resource_type.name.id`. Tuyệt đối không lạm dụng `depends_on` cho toàn bộ Module cha nếu chỉ có 1 tài nguyên con bên trong cần đồng bộ.

---

## 3. Nghệ Thuật Phá Vỡ Vòng Lặp Phụ Thuộc Hai Chiều (Bidirectional Cyclic Dependency)

Một trong những bài toán kinh điển trong quản trị mạng AWS là: **Security Group của Web Server cần cho phép Ingress từ Security Group của Database Server, và Security Group của Database Server chỉ cho phép Ingress từ Web Server**.

Nếu bạn khai báo Ingress Rules trực tiếp lồng bên trong khối `aws_security_group`, Terraform sẽ gặp lỗi <strong style="color: var(--accent-rose);">Cyclic Dependency</strong> ngay lập tức vì không thể xác định cái nào phải tạo trước:

```mermaid
flowchart LR
    subgraph WRONG["SAI: Khai Báo Ingress Lồng Nhau (Tạo Lỗi Cycle)"]
        SG_A["aws_security_group.web<br/>(Cần ID của sg.db)"] --- SG_B["aws_security_group.db<br/>(Cần ID của sg.web)"]
    end

    subgraph CORRECT["ĐÚNG: Tách Rời Bằng Resource Độc Lập"]
        SG_WEB["aws_security_group.web<br/>(Tạo trước, không có rule)"]
        SG_DB["aws_security_group.db<br/>(Tạo trước, không có rule)"]
        
        RULE_WEB["aws_security_group_rule.web_ingress"]
        RULE_DB["aws_security_group_rule.db_ingress"]

        SG_WEB --> RULE_WEB
        SG_DB --> RULE_WEB
        SG_WEB --> RULE_DB
        SG_DB --> RULE_DB
    end

    style SG_A fill:none,stroke:#f43f5e,stroke-width:2px
    style SG_B fill:none,stroke:#f43f5e,stroke-width:2px
    style SG_WEB fill:none,stroke:#3b82f6,stroke-width:2px
    style SG_DB fill:none,stroke:#3b82f6,stroke-width:2px
    style RULE_WEB fill:none,stroke:#10b981,stroke-width:2px
    style RULE_DB fill:none,stroke:#10b981,stroke-width:2px
```

---

## 4. Kiến Trúc Mẫu Triển Khai Multi-Tier Với Dependency Graph Chuẩn Mực

Dưới đây là bộ mã nguồn HCL giải quyết triệt để bài toán phụ thuộc đa tầng, tích hợp Data Sources và tách rời Security Group Rules độc lập:

```hcl
# ==============================================================================
# File: main.tf - Kiến trúc 3-Tier Enterprise tách rời phụ thuộc
# ==============================================================================
terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.45.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. DATA SOURCES: Truy vấn thông tin hạ tầng chia sẻ có sẵn
data "aws_vpc" "default_vpc" {
  default = true
}

data "aws_ami" "ubuntu_lts" {
  most_recent = true
  owners      = ["099720109477"] # Canonical Official Owner ID

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# 2. KHỞI TẠO CÁC SECURITY GROUPS CỐT LÕI (Không chứa inline rules)
resource "aws_security_group" "web_tier" {
  name        = "showtech-web-sg-${var.environment}"
  description = "Security Group cho Web Frontend Tier"
  vpc_id      = data.aws_vpc.default_vpc.id

  tags = {
    Name = "sg-web-${var.environment}"
  }
}

resource "aws_security_group" "db_tier" {
  name        = "showtech-db-sg-${var.environment}"
  description = "Security Group cho Database Backend Tier"
  vpc_id      = data.aws_vpc.default_vpc.id

  tags = {
    Name = "sg-db-${var.environment}"
  }
}

# 3. PHÁ VỠ CYCLE BẰNG SECURITY GROUP RULES ĐỘC LẬP
resource "aws_security_group_rule" "web_allow_https" {
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.web_tier.id
  description       = "Cho phep truy cap Web HTTPS tu Internet"
}

# DB chỉ nhận kết nối Port 5432 từ Web SG
resource "aws_security_group_rule" "db_allow_web" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.web_tier.id
  security_group_id        = aws_security_group.db_tier.id
  description              = "Cho phep Postgres connection tu Web Tier"
}

# 4. KHỞI TẠO IAM ROLE & EXPLICIT DEPENDENCY VỚI EKS NODE GROUP
resource "aws_iam_role" "node_role" {
  name = "showtech-eks-node-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "worker_node" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "cni_policy" {
  role       = aws_iam_role.node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

# 5. EC2 INSTANCE: Tích hợp Implicit Dependency và Data Source AMI
resource "aws_instance" "web_server" {
  ami                    = data.aws_ami.ubuntu_lts.id # Implicit tu Data Source
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.web_tier.id] # Implicit tu SG

  # Phụ thuộc tường minh: Đảm bảo Policy đã gắn xong vào IAM Role
  depends_on = [
    aws_iam_role_policy_attachment.worker_node,
    aws_iam_role_policy_attachment.cni_policy
  ]

  tags = {
    Name = "web-server-${var.environment}"
  }
}
```

```hcl
# ==============================================================================
# File: variables.tf
# ==============================================================================
variable "aws_region" {
  type    = string
  default = "ap-southeast-1"
}

variable "environment" {
  type    = string
  default = "production"
}

variable "instance_type" {
  type    = string
  default = "t3.medium"
}
```

---

## 5. Phân Tích Cạm Bẫy Thực Chiến: Lỗi "Data Source Deferral & Cycle Error"

### Tình Huống Sự Cố Thực Tế:
Vào lúc <span class="badge badge--rose">🕒 14:20 PM</span>, một nhóm kỹ sư muốn cấu hình Security Group dựa trên thông tin trả về từ một Data Source VPC Subnet. Tuy nhiên, Data Source này lại được truyền vào một biến `vpc_id` lấy từ tài nguyên `aws_vpc` được tạo trong cùng một đợt Apply:

```hcl
# CODE GÂY LỖI: Data Source phụ thuộc thuộc tính chưa xác định tại Pha Plan
resource "aws_vpc" "new_vpc" {
  cidr_block = "10.100.0.0/16"
}

data "aws_subnets" "created_subnets" {
  filter {
    name   = "vpc-id"
    values = [aws_vpc.new_vpc.id] # aws_vpc.new_vpc.id CHƯA TỒN TẠI tại pha Plan!
  }
}
```

### Log Lỗi Trả Về Khi Chạy `terraform plan`:
```diff
# Trích đoạn log lỗi từ Terraform Core Engine
! [CRITICAL ERROR] Error: Invalid data source query during plan
!   on main.tf line 6, in data "aws_subnets" "created_subnets":
!    6:   values = [aws_vpc.new_vpc.id]
! 
! The argument "values" depends on a resource attribute that cannot be determined 
! until apply. Data sources must be readable during the plan phase to build the 
! dependency graph.
```

### 5-Whys Root Cause Analysis:
1. <span class="badge badge--primary">Why 1</span> **Tại sao Data Source bị lỗi không đọc được?** $\rightarrow$ Vì Data Source cố gắng gửi API query lên AWS trong pha `plan`, nhưng tham số `vpc_id` lại là `(known after apply)`.
2. <span class="badge badge--primary">Why 2</span> **Tại sao `vpc_id` chưa có giá trị?** $\rightarrow$ Vì tài nguyên `aws_vpc.new_vpc` mới chỉ được khai báo, chưa hề được tạo trên AWS.
3. <span class="badge badge--primary">Why 3</span> **Tại sao Data Source lại chạy ở pha Plan?** $\rightarrow$ Vì Terraform cần toàn bộ kết quả của Data Source để tính toán số lượng phần tử cho các khối vòng lặp và dựng đồ thị DAG.
4. <span class="badge badge--primary">Why 4</span> **Tại sao kỹ sư lại dùng Data Source cho tài nguyên vừa tạo?** $\rightarrow$ Do thói quen thiết kế sai lầm; thay vì tham chiếu trực tiếp tài nguyên con qua mã HCL, kỹ sư lại cố gắng query ngược lại từ Cloud.
5. <span class="badge badge--emerald">Root Cause Remedy</span> **Biện pháp khắc phục chuẩn SRE:**
   - <span class="badge badge--emerald">Direct Reference</span> **Tuyệt đối không dùng Data Source để đọc lại tài nguyên vừa tạo trong cùng một Terraform State:** Hãy sử dụng trực tiếp tham chiếu tài nguyên (`aws_subnet.my_subnet.id`).
   - <span class="badge badge--cyan">State Decoupling</span> **Tách Workspace/Module độc lập:** Nếu bắt buộc phải query, hãy tách tầng Network (VPC/Subnet) thành một State riêng biệt được apply trước, sau đó tầng App mới dùng Data Source để đọc.

---

## 6. Hands-on Lab: Tái Hiện & Phá Vỡ Lỗi Cyclic Dependency (8 Bước)

| Bước | Lệnh CLI | Mục Đích Thực Thi |
| :---: | :--- | :--- |
| <span class="badge badge--primary">01</span> | `mkdir -p /tmp/terraform-dag-lab && cd /tmp/terraform-dag-lab` | Khởi tạo thư mục thực hành thử nghiệm môi trường cô lập |
| <span class="badge badge--cyan">02</span> | `cat << 'EOF' > cycle_test.tf ...` | Cố tình tạo mã nguồn có chứa lỗi Cycle phụ thuộc 2 chiều |
| <span class="badge badge--rose">03</span> | `terraform plan` | Chạy lệnh kiểm tra và quan sát thông báo lỗi Cycle bế tắc |
| <span class="badge badge--indigo">04</span> | `terraform graph \| grep -E "service_a\|service_b"` | Xuất bản cấu trúc đồ thị DOT thể hiện vòng lặp phụ thuộc |
| <span class="badge badge--amber">05</span> | `cat << 'EOF' > cycle_test.tf ... (Refactor)` | Tách rời Ingress Rules thành các tài nguyên độc lập để phá vỡ Cycle |
| <span class="badge badge--primary">06</span> | `terraform validate` | Chạy kiểm tra cú pháp và cấu trúc tham chiếu HCL sau khi sửa |
| <span class="badge badge--emerald">07</span> | `terraform plan` | Xác nhận đồ thị DAG hợp lệ và kế hoạch tạo 4 tài nguyên thành công |
| <span class="badge badge--emerald">08</span> | `cd .. && rm -rf /tmp/terraform-dag-lab` | Thu dọn sạch sẽ thư mục thử nghiệm sau khi hoàn tất |

```bash
# 1. Khởi tạo thư mục thực hành thử nghiệm
mkdir -p /tmp/terraform-dag-lab && cd /tmp/terraform-dag-lab
terraform init

# 2. Cố tình tạo mã nguồn có chứa lỗi Cycle phụ thuộc 2 chiều
cat << 'EOF' > cycle_test.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.45.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_security_group" "service_a" {
  name        = "sg-service-a"
  description = "Service A Security Group"
  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.service_b.id]
  }
}

resource "aws_security_group" "service_b" {
  name        = "sg-service-b"
  description = "Service B Security Group"
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.service_a.id]
  }
}
EOF

# 3. Chạy terraform plan để quan sát thông báo lỗi Cycle
terraform plan

# 4. Xuất bản đồ thị thể hiện vòng lặp bế tắc
terraform graph | grep -E "service_a|service_b"

# 5. Refactor mã nguồn — Tách rời Ingress Rules độc lập
cat << 'EOF' > cycle_test.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.45.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-1"
}

# 1. Khởi tạo 2 Security Group rỗng không chứa inline rules
resource "aws_security_group" "service_a" {
  name = "sg-service-a"
}

resource "aws_security_group" "service_b" {
  name = "sg-service-b"
}

# 2. Định nghĩa Rules độc lập để phá vỡ Cycle
resource "aws_security_group_rule" "a_from_b" {
  type                     = "ingress"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.service_b.id
  security_group_id        = aws_security_group.service_a.id
}

resource "aws_security_group_rule" "b_from_a" {
  type                     = "ingress"
  from_port                = 8080
  to_port                  = 8080
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.service_a.id
  security_group_id        = aws_security_group.service_b.id
}
EOF

# 6. Chạy kiểm tra lại với terraform validate
terraform validate

# 7. Thực hiện terraform plan kiểm tra tính hợp lệ của DAG
terraform plan

# 8. Dọn dẹp thư mục thử nghiệm
cd .. && rm -rf /tmp/terraform-dag-lab
```

---

## 7. 10 Câu Hỏi Tự Kiểm Tra Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q01</span>
    <span>Tại sao phụ thuộc ngầm định (Implicit Dependency) luôn được ưu tiên hơn phụ thuộc tường minh (<code>depends_on</code>)?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Vì phụ thuộc ngầm định cho phép Terraform biết chính xác <b style="color: var(--accent-primary);">thuộc tính nào</b> đang được truyền đi giữa 2 Node trên DAG, giúp đồ thị tối ưu hóa tối đa các nhánh thực thi song song. Trong khi <code>depends_on</code> khóa toàn bộ Node cha, ép buộc tất cả tài nguyên con phải chờ đợi tuần tự dù không cần thiết.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q02</span>
    <span>Lỗi "Cyclic Dependency" (Vòng lặp phụ thuộc) xảy ra khi nào trong Terraform?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Xảy ra khi đồ thị tồn tại một chu trình khép kín: Node A phụ thuộc Node B, và Node B (trực tiếp hoặc gián tiếp) lại phụ thuộc ngược lại Node A. Thuật toán sắp xếp Topo không thể tìm thấy đỉnh bắt đầu hợp lệ và dừng lại báo lỗi.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q03</span>
    <span>Làm thế nào để giải quyết triệt để lỗi Cyclic Dependency giữa 2 Security Groups trên AWS?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Không khai báo khối <code>ingress</code> hoặc <code>egress</code> lồng bên trong tài nguyên <code>aws_security_group</code>. Thay vào đó, hãy khởi tạo 2 Security Group rỗng, sau đó sử dụng các tài nguyên độc lập <code>aws_security_group_rule</code> để gắn quan hệ sau.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q04</span>
    <span>Data Sources trong Terraform được thực thi ở giai đoạn nào (Plan hay Apply)?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Phần lớn Data Sources được thực thi ngay trong <b style="color: var(--accent-primary);">pha Plan</b> để nạp dữ liệu và kiểm tra kiểu. Tuy nhiên, nếu một tham số của Data Source phụ thuộc vào giá trị của một tài nguyên chỉ được xác định sau pha Apply (<code>known after apply</code>), việc đọc Data Source sẽ bị hoãn (Deferred) sang pha Apply.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q05</span>
    <span>Khi nào bắt buộc phải dùng từ khóa <code>depends_on</code>? Cho ví dụ thực tế?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Khi có mối quan hệ phụ thuộc ngầm về mặt logic hoặc quyền hạn nhưng <b style="color: var(--accent-primary);">không có tham chiếu dữ liệu trực tiếp trong code</b>. Ví dụ: EKS Node Group cần IAM Policy đã gắn xong vào Role trước khi khởi tạo, hoặc EC2 instance cần S3 Bucket Policy cấu hình xong mới được gọi API đọc dữ liệu.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q06</span>
    <span>Điều gì xảy ra khi bạn đặt <code>depends_on</code> ở cấp độ Module (<code>module "vpc"</code>)?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Toàn bộ mọi tài nguyên bên trong module con đó sẽ bị hoãn thực thi cho đến khi mọi tài nguyên trong danh sách <code>depends_on</code> hoàn tất 100%. Điều này làm tê liệt hoàn toàn tính năng chạy song song giữa các module.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q07</span>
    <span>Tại sao không nên dùng Data Source để truy vấn lại tài nguyên vừa được tạo trong cùng một State?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Vì trong lần chạy đầu tiên (khi tài nguyên chưa được tạo), Data Source sẽ gửi query lên Cloud và báo lỗi <code>ResourceNotFound</code> ở pha Plan, khiến toàn bộ tiến trình Apply bị sập. Hãy luôn tham chiếu trực tiếp qua thuộc tính của Resource.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q08</span>
    <span>Thuật toán sắp xếp Topo (Topological Sort) duyệt qua đồ thị DAG theo thứ tự nào khi hủy tài nguyên (<code>terraform destroy</code>)?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Terraform tự động đảo ngược hướng của toàn bộ các cạnh trên đồ thị DAG, thực hiện hủy các Node lá (Leaf Nodes) trước, sau đó mới đi ngược về Node gốc (Root Nodes) theo nguyên lý <b style="color: var(--accent-primary);">LIFO (Last In, First Out)</b>.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q09</span>
    <span>Data Source <code>aws_ami</code> với tham số <code>most_recent = true</code> có rủi ro tiềm ẩn nào khi vận hành?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Mỗi khi nhà cung cấp (Canonical/AWS) phát hành một bản vá AMI mới, lệnh <code>terraform plan</code> tiếp theo sẽ phát hiện ID của AMI đã thay đổi và đề xuất <b style="color: var(--accent-primary);">hủy và tạo lại (Destroy and Recreate)</b> toàn bộ các EC2 Instances đang chạy, có thể gây gián đoạn dịch vụ ngoài ý muốn nếu không dùng Launch Template / ASG.
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q10</span>
    <span>Làm thế nào để trực quan hóa đồ thị DAG của một dự án lớn một cách nhanh nhất?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Sử dụng lệnh <code>terraform graph | dot -Tsvg -o graph.svg</code> kết hợp với trình duyệt Web hoặc công cụ trực quan hóa trực tuyến Graphviz để xem cấu trúc phân nhánh và mối quan hệ phụ thuộc.
</div>
</details>

---

## 8. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

Làm chủ **Dependency Graph (DAG)**, phân biệt rõ ràng **Implicit vs Explicit Dependencies** và nắm vững quy tắc vận hành của **Data Sources** giúp bạn tự tin thiết kế những hệ sinh thái hạ tầng khổng lồ mà không bao giờ gặp phải các lỗi bế tắc vòng lặp.

> [!TIP]
> **BÀI HỌC TIẾP THEO:**
> Trong **[Bài 05: Thiết Kế Variables, Locals & Outputs Chuẩn Enterprise: Type Constraints, Validation Rules & Sensitive Data Masking](./05-thiet-ke-variables-locals-outputs-chuan-enterprise.md)**, chúng ta sẽ hoàn thiện chặng 1 với nghệ thuật thiết kế giao diện hạ tầng: Tùy biến biến đầu vào với các quy tắc kiểm tra biểu thức chính quy (Regex Validation), quản lý biến nội bộ bất biến `locals` và che giấu dữ liệu nhạy cảm với cờ `sensitive = true`.
{% endraw %}
