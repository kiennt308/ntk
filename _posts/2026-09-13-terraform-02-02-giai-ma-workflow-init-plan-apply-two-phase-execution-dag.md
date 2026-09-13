---
layout: post
title: "[Bài 02] Giải Mã Workflow Init, Plan, Apply - Cơ Chế Two-Phase Execution & Đồ Thị DAG Chuyên Sâu"
date: 2026-09-13 11:50:00 +0700
categories: [Terraform]
tags:
  - Terraform
  - IaC
  - DevOps
  - CloudNative
  - Part-02
series: "Terraform Enterprise Architecture"
series_order: 2
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80"
summary: "Phân tích sâu cơ chế thực thi 2 pha (Two-Phase Execution), giao thức gRPC Plugin RPC, thuật toán sắp xếp Topo trên đồ thị DAG và tối ưu hóa luồng song song với -parallelism."
tldr:
  - "Workflow cốt lõi: Init (tải Provider & khóa SHA-256) -> Plan (đọc Live State & dựng đồ thị DAG) -> Apply (thực thi đa luồng theo topo)."
  - "Giao thức gRPC Plugin RPC tách biệt Terraform Core (Go Engine) và Provider Plugins qua Local Domain Sockets / Named Pipes."
  - "Đồ thị DAG xác định thứ tự xuôi khi tạo (+) và thứ tự ngược khi hủy (-), ngăn chặn triệt để Circular Dependencies."
  - "Kiểm soát an toàn với -parallelism, -lock-timeout=120s và chỉ chạy terraform force-unlock khi chắc chắn tiến trình cũ đã dừng."
---

{% raw %}
# Giải Mã Workflow Terraform: Cơ Chế Hoạt Động Ngầm Của Init, Plan, Apply & Đồ Thị DAG

Hầu hết các kỹ sư khi bắt đầu làm quen với Terraform đều thuộc lòng bộ ba câu lệnh quen thuộc: `terraform init`, `terraform plan` và `terraform apply`. Tuy nhiên, khi vận hành hệ thống quy mô lớn với hàng trăm tài nguyên phân tán trên nhiều tài khoản đám mây, việc hiểu rõ **cơ chế ngầm (under-the-hood)** của từng giai đoạn thực thi là yếu tố sống còn giúp bạn tối ưu hóa thời gian chạy pipeline từ <span class="badge badge--rose">45 phút</span> xuống dưới <span class="badge badge--emerald">3 phút</span>, gỡ rối các vòng lặp phụ thuộc (<strong style="color: var(--accent-rose);">Circular Dependency</strong>) và ngăn chặn thảm họa xóa nhầm cơ sở dữ liệu Production.

Trong bài viết chuyên sâu này, chúng ta sẽ mở nắp "bộ máy cơ học" bên trong Terraform Core: Khám phá giao thức giao tiếp <strong style="color: var(--accent-primary);">gRPC Plugin RPC</strong>, cơ chế phân tích cú pháp <strong style="color: var(--accent-cyan);">Two-Phase Execution</strong>, thuật toán sắp xếp topo trên <strong style="color: var(--accent-amber);">Đồ thị không tuần hoàn có hướng (Directed Acyclic Graph - DAG)</strong> và phương pháp điều phối luồng song song với tham số `<code style="color: var(--accent-primary); font-weight: 700;">-parallelism</code>`.

---

## 1. Toàn Cảnh Chu Trình Vòng Đời Terraform Core Workflow

Kiến trúc nội tại của Terraform được chia thành 2 phần tách biệt hoàn toàn: **Terraform Core** (chịu trách nhiệm phân tích HCL, dựng đồ thị DAG, quản lý State) và **Provider Plugins** (chịu trách nhiệm giao tiếp trực tiếp với Cloud API). Hai thành phần này giao tiếp với nhau qua giao thức **HashiCorp go-plugin** dựa trên **gRPC over Local Unix Sockets / Named Pipes**:

```mermaid
sequenceDiagram
    autonumber
    actor Dev as DevOps Engineer / CI-CD
    participant Core as Terraform Core (Go Engine)
    participant Reg as HashiCorp Registry
    participant State as State Backend (S3 + DynamoDB Lock)
    participant Prov as AWS Provider Plugin (gRPC Process)
    participant API as AWS Cloud APIs (HTTPS REST)

    Note over Dev,Reg: GIAI ĐOẠN 1: TERRAFORM INIT
    Dev->>Core: terraform init
    Core->>Reg: Tra cứu Provider & Module Versions
    Reg-->>Core: Tải Binary Plugins về .terraform/providers/
    Core->>Core: Xác thực mã băm SHA-256 (.terraform.lock.hcl)
    Core->>State: Khởi tạo kết nối Backend & Thử nghiệm State Lock

    Note over Dev,API: GIAI ĐOẠN 2: TERRAFORM PLAN (TWO-PHASE)
    Dev->>Core: terraform plan
    Core->>State: Acquire Lock & Tải State hiện tại
    Core->>Prov: gRPC ReadResource (Yêu cầu Refresh trạng thái)
    Prov->>API: Gọi Describe/Get API (DescribeVpcs, DescribeSubnets)
    API-->>Prov: Phản hồi Live Attributes
    Prov-->>Core: Trả về trạng thái Actual State
    Core->>Core: Xây dựng đồ thị DAG & Topological Sort
    Core->>Core: So sánh S_desired vs S_actual -> Tính Diff
    Core-->>Dev: Xuất bản Execution Plan (+ Add / ~ Change / - Destroy)

    Note over Dev,API: GIAI ĐOẠN 3: TERRAFORM APPLY
    Dev->>Core: terraform apply (approve)
    Core->>Prov: gRPC ApplyResourceChange theo thứ tự DAG Topo
    Prov->>API: Gửi POST/PUT/DELETE API Calls lên Cloud
    API-->>Prov: Xác nhận tài nguyên đã tạo/sửa xong
    Prov-->>Core: Trả về Resource ID, ARN, Public IP
    Core->>State: Ghi đè State mới vào S3 & Release Lock
    Core-->>Dev: Báo cáo Apply Complete! Resources: 5 added, 0 changed.
```

---

## 2. Giải Phẫu Chi Tiết Ba Giai Đoạn Cốt Lõi

### 2.1. `terraform init` — Quản Trị Dependency & Cấu Trúc Khóa Lock File
Khi phát lệnh `init`, Terraform chuẩn bị toàn bộ không gian làm việc với 3 bước nền tảng:
1. <span class="badge badge--primary">Bước 1</span> **Provider Discovery & Checksum Verification**: Quét các khối `required_providers`, tải binary tương thích với OS/Arch về `.terraform/providers/`.
2. <span class="badge badge--amber">Bước 2</span> **Khóa Phiên Bản Bất Biến (`.terraform.lock.hcl`)**: Ghi lại mã băm SHA-256 của từng Provider binary (cả mã hash nền tảng `h1:` và mã hash đa nền tảng `zh:`). Tệp này phải luôn được commit vào Git để tránh lỗi lệch phiên bản trong CI/CD.
3. <span class="badge badge--emerald">Bước 3</span> **Remote Backend & State Lock Binding**: Thiết lập kênh truyền dữ liệu an toàn tới S3 Bucket và xác thực quyền ghi vào DynamoDB Lock Table.

> [!TIP]
> **TỐI ƯU HIỆU NĂNG CI/CD VỚI PLUGIN CACHE:**
> Thiết lập biến môi trường `export TF_PLUGIN_CACHE_DIR="$HOME/.terraform.d/plugin-cache"` trong máy chủ CI/CD (GitLab Runner / GitHub Action Runner). Lệnh này giúp tái sử dụng lại các binary provider đã tải, giảm thời gian chạy `terraform init` từ <b style="color: var(--accent-rose);">40 giây</b> xuống dưới <b style="color: var(--accent-emerald);">2 giây</b>!

---

### 2.2. `terraform plan` — Two-Phase Execution & Thuật Toán Xây Dựng DAG
Lệnh `plan` thực hiện chu trình phân tích 2 pha nghiêm ngặt:

#### Pha 1: Refresh State (Đối Soát Trạng Thái Thực Tế)
Terraform đọc State file hiện hành, gửi các lệnh RPC `ReadResource` tới Provider để truy vấn trực tiếp Cloud API, phát hiện các thay đổi ngoài luồng (<strong style="color: var(--accent-rose);">State Drift</strong>) do ai đó can thiệp thủ công trên giao diện Web.

#### Pha 2: Xây Dựng Đồ Thị DAG & Thuật Toán Sắp Xếp Topo (Topological Sort)
Terraform Engine phân tích toàn bộ mã nguồn HCL, xác định các tham chiếu ngầm định (`aws_subnet.public.id` tham chiếu `aws_vpc.main.id`) và tham chiếu tường minh (`depends_on`). Toàn bộ hệ thống được mô hình hóa thành một **Đồ thị không tuần hoàn có hướng (Directed Acyclic Graph - DAG)**:

```mermaid
flowchart TD
    VPC["aws_vpc.main<br/>(Node Gốc - Root)"] --> IGW["aws_internet_gateway.gw"]
    VPC --> SUB_PUB["aws_subnet.public_a"]
    VPC --> SUB_PRI["aws_subnet.private_a"]
    
    IGW --> RT_PUB["aws_route_table.public_rt"]
    SUB_PUB --> RT_PUB_ASSOC["aws_route_table_association.pub_assoc"]
    RT_PUB --> RT_PUB_ASSOC
    
    SUB_PUB --> NAT["aws_nat_gateway.nat_gw"]
    NAT --> RT_PRI["aws_route_table.private_rt"]
    SUB_PRI --> RT_PRI_ASSOC["aws_route_table_association.pri_assoc"]
    RT_PRI --> RT_PRI_ASSOC

    RT_PRI_ASSOC --> EKS["aws_eks_cluster.main_cluster<br/>(Node Lá - Leaf)"]

    style VPC fill:none,stroke:#3b82f6,stroke-width:2px
    style IGW fill:none,stroke:#6366f1,stroke-width:2px
    style SUB_PUB fill:none,stroke:#0ea5e9,stroke-width:2px
    style SUB_PRI fill:none,stroke:#0ea5e9,stroke-width:2px
    style RT_PUB fill:none,stroke:#f59e0b,stroke-width:1.5px
    style RT_PUB_ASSOC fill:none,stroke:#f59e0b,stroke-width:1.5px
    style NAT fill:none,stroke:#ec4899,stroke-width:2px
    style RT_PRI fill:none,stroke:#f59e0b,stroke-width:1.5px
    style RT_PRI_ASSOC fill:none,stroke:#f59e0b,stroke-width:1.5px
    style EKS fill:none,stroke:#10b981,stroke-width:2px
```

Dựa trên thuật toán sắp xếp Topo (Topological Sorting - Kahn's Algorithm), Terraform xác định:
- <b style="color: var(--accent-emerald);">Thứ tự xuôi khi Tạo mới (+):</b> Đi từ Node gốc (VPC) $\rightarrow$ Subnet $\rightarrow$ Route Table $\rightarrow$ EKS Cluster.
- <b style="color: var(--accent-rose);">Thứ tự ngược khi Xóa bỏ (-):</b> Đi từ Node lá (EKS Cluster) $\rightarrow$ Route Table Association $\rightarrow$ Subnet $\rightarrow$ VPC (LIFO - Last In First Out).
- <b style="color: var(--accent-amber);">Phát hiện Vòng lặp bế tắc (Circular Dependency):</b> Nếu tài nguyên $A$ phụ thuộc $B$ và $B$ lại phụ thuộc ngược lại $A$, thuật toán sẽ phát hiện chu trình (Cycle) và lập tức dừng lại báo lỗi `Cycle: aws_security_group_rule.a, aws_security_group_rule.b`.

---

### 2.3. `terraform apply` — Cơ Chế Điều Phối Đa Luồng Với Tham Số `-parallelism`
Trong giai đoạn `apply`, Terraform Core duyệt qua đồ thị DAG theo thứ tự topo và phân bổ công việc vào một **Worker Pool đa luồng** (Goroutines trong Go).

Mặc định, Terraform sử dụng tham số `-parallelism=10` (đồng thời gửi tối đa 10 API requests lên Cloud Provider).

| Tham Số CLI | Giá Trị Mặc Định | Hành Vi Kỹ Thuật | Khuyến Nghị Thực Chiến |
| :--- | :--- | :--- | :--- |
| **`-parallelism=N`** | `10` | Số lượng Node độc lập trên DAG được thực thi song song | Giảm xuống `3` - `5` khi bị Rate Limit / Throttling; Tăng lên `30` khi khởi tạo hàng trăm DNS records |
| **`-refresh=false`** | `true` | Bỏ qua bước gọi API kiểm tra Live State trong pha 1 | Dùng khi cần apply khẩn cấp các tài nguyên độc lập mà Cloud API đang chậm |
| **`-lock-timeout=Xs`**| `0s` | Thời gian chờ nếu State đang bị khóa bởi tiến trình khác | Luôn đặt `-lock-timeout=120s` trong CI/CD để xếp hàng chờ thay vì fail ngay lập tức |
| **`-target=resource`**| N/A | Chỉ áp dụng một nhánh cụ thể trên đồ thị DAG | Chỉ dùng để cứu hộ sự cố, không lạm dụng trong quy trình chuẩn |

---

## 3. Kiến Trúc Mẫu Triển Khai Mạng VPC Chuẩn Đồ Thị DAG (HCL Breakdown)

Dưới đây là cấu hình một hệ sinh thái mạng VPC hoàn chỉnh, thể hiện rõ ràng cây phân nhánh của đồ thị DAG từ gốc tới lá:

```hcl
# ==============================================================================
# File: main.tf - Kiến trúc hạ tầng mạng VPC chuẩn Enterprise
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

# 1. ROOT NODE: Mạng VPC cốt lõi
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "showtech-enterprise-vpc"
  }
}

# 2. CHILD NODE: Internet Gateway (Phụ thuộc ngầm định vào VPC)
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "showtech-igw"
  }
}

# 3. CHILD NODES: Public Subnet và Private Subnet (Độc lập, tạo song song)
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 4, 0) # 10.0.0.0/20
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "showtech-public-subnet-a"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, 1) # 10.0.16.0/20
  availability_zone = "${var.aws_region}a"

  tags = {
    Name = "showtech-private-subnet-a"
  }
}

# 4. INTERMEDIATE NODE: Elastic IP & NAT Gateway (Nằm trong Public Subnet)
resource "aws_eip" "nat" {
  domain     = "vpc"
  depends_on = [aws_internet_gateway.gw] # Bắt buộc IGW phải có trước EIP

  tags = {
    Name = "showtech-nat-eip"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public.id

  tags = {
    Name = "showtech-nat-gw"
  }
}

# 5. LEAF NODES: Route Tables và Route Associations
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "showtech-public-rt"
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public_rt.id
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

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}
```

### Phân Tích Kỹ Thuật Chi Tiết:
- <span class="badge badge--primary"><code>Implicit Dependency</code></span> **Tham chiếu ngầm định:** Dòng `vpc_id = aws_vpc.main.id` tự động thông báo cho Terraform DAG rằng tài nguyên `aws_subnet.public` không thể được tạo trước khi `aws_vpc.main` trả về thuộc tính `id`.
- <span class="badge badge--emerald"><code>Explicit Dependency</code></span> **Tham chiếu tường minh:** Dòng `depends_on = [aws_internet_gateway.gw]` ép buộc Terraform phải đợi Internet Gateway gắn thành công vào VPC thì mới xin cấp Elastic IP, loại bỏ lỗi gián đoạn định tuyến của AWS.

---

## 4. Phân Tích Cạm Bẫy Thực Chiến: Thảm Họa "API Throttling & Deadlock Lock State"

### Tình Huống Sự Cố Thực Tế:
Vào lúc <span class="badge badge--rose">🕒 10:14 AM</span>, tại một công ty thương mại điện tử, một kỹ sư thực hiện triển khai cụm 150 DNS Records và 80 Security Group Rules bằng một tệp cấu hình Terraform duy nhất. Để tăng tốc độ apply, kỹ sư đã thiết lập tham số:
```bash
terraform apply -parallelism=50 -auto-approve
```

### Hậu Quả & Log Lỗi Thực Tế:
```diff
# Trích đoạn log lỗi từ AWS Provider Plugin
2026-09-05T10:14:02.120Z [ERROR] provider.aws: RequestError: send request failed
caused by: ThrottlingException: Rate exceeded
	status code: 400, request id: 89ab32cd-1234-5678-90ab-cdef12345678
aws_route53_record.app_record[42]: Creating...
aws_route53_record.app_record[43]: Creating...
aws_security_group_rule.ingress[18]: Creating...

! [CRITICAL ERROR] Error creating Route53 Record: ThrottlingException: Rate exceeded
! [CRITICAL ERROR] Error creating Security Group Rule: RequestLimitExceeded: Request limit exceeded.

# Tiến trình apply bị crash giữa chừng, State Lock trong DynamoDB không kịp giải phóng!
# Khi kỹ sư chạy lại lệnh apply lần 2:
! Error: Error acquiring the state lock
Lock Info:
  ID:        e2b9c031-41fa-4f2a-b731-92fa0912384a
  Path:      showtech-prod-tfstate-ap-southeast-1/core/network.tfstate
  Operation: OperationTypeApply
  Who:       jenkins@ci-runner-04
  Created:   2026-09-05 10:14:00.1023 UTC
```

```mermaid
flowchart TD
    A["⚙️ Thiết lập -parallelism=50<br/>(Quá nhiều luồng gọi đồng thời)"]
    B["💥 Bắn dồn dập 50 requests/giây tới AWS Route53 / EC2 API"]
    C["🛑 AWS Kích hoạt Throttling: Rate exceeded (HTTP 400)"]
    D["⚡ Terraform Plugin gặp Exception và Crash đột ngột"]
    E["🔒 Tiến trình chết trước khi gửi lệnh Release Lock tới DynamoDB"]
    F["💥 HỆ THỐNG RƠI VÀO TRẠNG THÁI DEADLOCK STATE LOCK!"]

    A --> B --> C --> D --> E --> F

    style A fill:none,stroke:#f59e0b,stroke-width:2px
    style B fill:none,stroke:#f43f5e,stroke-width:2px
    style C fill:none,stroke:#dc2626,stroke-width:2.5px
    style D fill:none,stroke:#8b5cf6,stroke-width:2px
    style E fill:none,stroke:#d97706,stroke-width:2px
    style F fill:none,stroke:#dc2626,stroke-width:2.5px
```

### 5-Whys Root Cause Analysis:
1. <span class="badge badge--primary">Why 1</span> **Tại sao hệ thống bị khóa không cho deploy tiếp?** $\rightarrow$ Vì DynamoDB Lock Table vẫn đang giữ bản ghi Lock ID `e2b9c031...` của tiến trình trước.
2. <span class="badge badge--primary">Why 2</span> **Tại sao tiến trình trước không nhả khóa?** $\rightarrow$ Vì tiến trình bị crash đột ngột do gặp lỗi `ThrottlingException` từ AWS API.
3. <span class="badge badge--primary">Why 3</span> **Tại sao AWS API trả về lỗi Throttling?** $\rightarrow$ Vì Terraform gửi đồng thời 50 requests/giây, vượt quá ngưỡng Token Bucket Rate Limit của tài khoản AWS.
4. <span class="badge badge--primary">Why 4</span> **Tại sao lại gửi 50 requests cùng lúc?** $\rightarrow$ Vì kỹ sư tùy tiện cấu hình `-parallelism=50` mà không nắm rõ hạn mức API của dịch vụ Route53 và EC2.
5. <span class="badge badge--emerald">Root Cause Remedy</span> **Biện pháp khắc phục chuẩn SRE:**
   - <span class="badge badge--rose">Force Unlock</span> **Mở khóa khẩn cấp an toàn:** Chạy `<code style="color: var(--accent-rose); font-weight: 700;">terraform force-unlock &lt;Lock-ID&gt;</code>` sau khi đã xác minh không còn tiến trình nào đang chạy ngầm trên CI/CD runner.
   - <span class="badge badge--amber">Tune Parallelism</span> **Điều chỉnh `-parallelism` hợp lý:** Đặt `-parallelism=10` (mặc định) hoặc `-parallelism=5` cho các dịch vụ nhạy cảm về API rate limit.
   - <span class="badge badge--cyan">Lock Timeout Gate</span> **Thêm tham số `-lock-timeout` trong CI/CD:** Luôn truyền cờ `<code style="color: var(--accent-cyan); font-weight: 700;">-lock-timeout=120s</code>` để pipeline tự động đợi khóa được nhả thay vì báo fail tức thì.

---

## 5. Hands-on Lab: Khám Phá & Xuất Bản Đồ Thị DAG (8 Bước)

| Bước | Lệnh CLI | Mục Đích Thực Thi |
| :---: | :--- | :--- |
| <span class="badge badge--primary">01</span> | `sudo apt-get install -y graphviz && terraform init` | Cài đặt công cụ phân tích đồ thị và khởi tạo Terraform |
| <span class="badge badge--cyan">02</span> | `export TF_LOG=DEBUG && export TF_LOG_PATH=...` | Kích hoạt log chi tiết để quan sát các lệnh gRPC và API calls |
| <span class="badge badge--indigo">03</span> | `terraform graph > graph.dot` | Xuất đồ thị phụ thuộc của toàn bộ tài nguyên ra định dạng DOT |
| <span class="badge badge--amber">04</span> | `dot -Tpng graph.dot -o terraform_dag.png` | Chuyển đổi đồ thị DOT sang hình ảnh trực quan PNG |
| <span class="badge badge--emerald">05</span> | `terraform plan -parallelism=5 -out=tfplan.binary` | Tạo kế hoạch thực thi với mức độ song song kiểm soát an toàn |
| <span class="badge badge--primary">06</span> | `terraform plan -replace="aws_nat_gateway.nat"` | Đánh dấu buộc hủy và tạo lại tài nguyên cụ thể có chủ đích |
| <span class="badge badge--rose">07</span> | `terraform apply -lock-timeout=60s tfplan.binary` | Áp dụng kế hoạch với thời gian chờ nhả khóa 60 giây an toàn |
| <span class="badge badge--emerald">08</span> | `terraform state list && terraform destroy` | Kiểm tra danh mục tài nguyên và thu dọn theo thứ tự ngược DAG |

```bash
# 1. Cài đặt công cụ vẽ đồ thị Graphviz và khởi tạo
sudo apt-get install -y graphviz || brew install graphviz
terraform init

# 2. Bật chế độ Debug Logging chi tiết
export TF_LOG=DEBUG
export TF_LOG_PATH="./terraform_debug.log"

# 3. Xuất bản dữ liệu đồ thị DAG dưới định dạng DOT
terraform graph > graph.dot

# 4. Chuyển đổi đồ thị DOT sang hình ảnh trực quan PNG
dot -Tpng graph.dot -o terraform_dag_architecture.png
ls -lh terraform_dag_architecture.png

# 5. Thực hiện Plan với tham số giới hạn luồng song song
terraform plan -parallelism=5 -out=tfplan.binary

# 6. Kiểm tra cơ chế thay thế tài nguyên có chủ đích (-replace)
terraform plan -replace="aws_nat_gateway.nat"

# 7. Áp dụng kế hoạch thực thi với cấu hình State Lock Timeout
terraform apply -lock-timeout=60s tfplan.binary

# 8. Kiểm tra trạng thái và thu dọn tài nguyên có kiểm soát
terraform state list
terraform destroy -auto-approve
```

---

## 6. 10 Câu Hỏi Tự Kiểm Tra Chuyên Sâu (Self-Check Q&A)

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Tệp này lưu trữ chính xác phiên bản và mã băm SHA-256 (Checksum) của các Provider Plugins đã được sử dụng. <b style="color: var(--accent-emerald);">BẮT BUỘC</b> phải đưa tệp này vào Git để đảm bảo tính bất biến (Reproducibility), ngăn chặn việc các môi trường CI/CD khác nhau vô tình tải về phiên bản Provider mới hơn có chứa breaking changes.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Terraform Core và Provider Plugins là các tiến trình (OS Processes) riêng biệt. Chúng giao tiếp với nhau thông qua cơ chế <b style="color: var(--accent-primary);">gRPC over Local Sockets (Unix Domain Socket trên Linux/Mac hoặc Named Pipes trên Windows)</b> sử dụng thư viện mã nguồn mở <code>hashicorp/go-plugin</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
DAG là đồ thị có hướng và <b style="color: var(--accent-rose);">không chứa bất kỳ vòng lặp khép kín nào</b>. Terraform bắt buộc phải dùng DAG vì nếu tồn tại chu trình tuần hoàn (tài nguyên A phụ thuộc B và B phụ thuộc A), thuật toán sẽ không thể xác định điểm bắt đầu và rơi vào bế tắc vô tận (<b style="color: var(--accent-rose);">Deadlock</b>).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Implicit Dependency:</b> Được tạo tự động khi một tài nguyên sử dụng trực tiếp thuộc tính đầu ra của tài nguyên khác (ví dụ <code>subnet_id = aws_subnet.public.id</code>).<br/></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-emerald);">Explicit Dependency:</b> Được kỹ sư khai báo thủ công thông qua thuộc tính <code style="color: var(--accent-emerald); font-weight: 700;">depends_on = [...]</code> khi không có sự ràng buộc dữ liệu trực tiếp nhưng bắt buộc phải có thứ tự khởi tạo trước sau.</div>
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Terraform Core sẽ gửi các yêu cầu <code>ReadResource</code> tới Provider để gọi các API đọc (Describe/Get) từ Cloud, sau đó cập nhật dữ liệu mới nhất vào bộ nhớ đệm State nhằm phát hiện xem có sự sai lệch nào giữa thực tế và State (<b style="color: var(--accent-amber);">Drift Detection</b>) trước khi tính toán Diff.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Nên dùng khi hạ tầng có số lượng tài nguyên quá lớn (hàng ngàn resources) khiến bước Refresh mất hàng chục phút, hoặc khi Cloud API đang bị chậm/nghẽn mà bạn chỉ cần thực hiện một thay đổi nhỏ đã biết chắc chắn trạng thái. Tuy nhiên cần thận trọng vì nó bỏ qua việc kiểm tra Drift.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Chỉ sử dụng khi một tiến trình Terraform trước đó bị crash/kill bất ngờ khiến bản ghi Lock vẫn còn kẹt trong Backend (DynamoDB). <b style="color: var(--accent-rose);">Rủi ro lớn nhất:</b> Nếu tiến trình cũ thực tế vẫn đang âm thầm chạy và ghi dữ liệu, việc force-unlock sẽ cho phép tiến trình thứ hai nhảy vào ghi đè, gây hỏng hoàn toàn tệp State (<b style="color: var(--accent-rose);">State Corruption</b>).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Kiểm soát số lượng tác vụ (Goroutines) độc lập trên đồ thị DAG có thể được thực thi đồng thời. Giảm tham số này giúp tránh lỗi <b style="color: var(--accent-amber);">API Throttling</b> của Cloud Provider; tăng tham số này giúp rút ngắn thời gian triển khai khi có nhiều tài nguyên độc lập (như DNS records, S3 buckets).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Lệnh <code>terraform graph</code> xuất ra dữ liệu mô tả đồ thị dưới định dạng ngôn ngữ <b style="color: var(--accent-primary);">DOT</b>. Ta sử dụng công cụ mã nguồn mở <b style="color: var(--accent-primary);">Graphviz</b> (lệnh <code>dot -Tpng graph.dot -o graph.png</code>) để chuyển đổi sang hình ảnh SVG/PNG.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Dùng để thay thế lệnh cũ <code>terraform taint</code>. Nó yêu cầu Terraform trong đợt apply tiếp theo phải hủy bỏ (destroy) và tạo mới lại (recreate) chính xác tài nguyên được chỉ định mà không cần chỉnh sửa bất kỳ dòng mã nguồn HCL nào.
</div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

Hiểu rõ cơ chế <b style="color: var(--accent-primary);">Two-Phase Execution</b>, giao thức <b style="color: var(--accent-cyan);">gRPC Plugin RPC</b> và thuật toán <b style="color: var(--accent-amber);">DAG</b> giúp bạn nắm trong tay chìa khóa để điều khiển, tối ưu hóa và gỡ lỗi mọi hệ thống IaC phức tạp nhất.

> [!TIP]
> **BÀI HỌC TIẾP THEO:**
> Trong **[Bài 03: Tối Ưu Cú Pháp HCL: Xử Lý Dynamic Types, Expressions, Built-in Functions & Meta-Arguments Chuẩn Enterprise](./03-toi-uu-cu-phap-hcl-xu-ly-dynamic-type-expressions.md)**, chúng ta sẽ đi sâu vào nghệ thuật lập trình HCL: Làm chủ hệ thống kiểu dữ liệu động, biểu thức điều kiện tam nguyên, các hàm tích hợp sẵn (Built-in Functions) và siêu tham số vòng lặp meta-arguments.
{% endraw %}
