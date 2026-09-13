---
layout: post
title: "[Bài 29] Tổng Ôn & Bí Kíp Chinh Phục Chứng Chỉ Terraform Associate (003)"
date: 2026-09-13 07:20:00 +0700
categories: [Terraform]
tags:
  - Terraform
  - IaC
  - DevOps
  - CloudNative
  - Part-29
series: "Terraform Enterprise Architecture"
series_order: 29
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=1200&q=80"
summary: "Cẩm nang tổng ôn toàn diện kỳ thi chứng chỉ HashiCorp Certified: Terraform Associate (003): Tổng hợp 9 chuyên đề trọng tâm, phân tích cạm bẫy câu hỏi trắc nghiệm và chiến thuật làm bài đạt điểm tối đa."
tldr:
  - "9 Chuyên đề cốt lõi: Nắm vững IaC Concepts, Terraform CLI Workflow, State Management, Modules, Core Syntax và HCP Terraform Cloud."
  - "Phân tích dạng câu hỏi: Làm chủ các câu hỏi trắc nghiệm một/nhiều đáp án, câu hỏi điền từ và các tình huống xử lý lệnh CLI thực tế."
  - "Cạm bẫy thường gặp: Phân biệt rõ sự khác nhau giữa local-exec vs remote-exec, count vs for_each, taint vs replace và các mức độ Policy enforcement."
  - "Chiến thuật làm bài: Quản lý thời gian 60 phút cho 57 câu hỏi, kỹ thuật loại trừ đáp án và đọc kỹ từ khóa điều kiện trong đề bài."
---
{% raw %}
# Tổng Ôn và Bí Kíp Chinh Phục Chứng Chỉ Terraform Associate (003)

Chứng chỉ **HashiCorp Certified: Terraform Associate (003)** là một trong những chứng chỉ nghề nghiệp danh giá và được săn đón hàng đầu trong ngành công nghiệp Cloud & DevOps toàn cầu. Sở hữu chứng chỉ này không chỉ là bằng chứng khẳng định năng lực chuyên môn của bạn về Infrastructure as Code (IaC), mà còn mở ra những cơ hội thăng tiến vượt bậc với mức đãi ngộ hấp dẫn tại các tập đoàn công nghệ lớn.

Tuy nhiên, kỳ thi phiên bản **003** đã được HashiCorp nâng cấp toàn diện với nhiều câu hỏi tình huống thực tế hóc búa, tập trung sâu vào các tính năng hiện đại (như Terraform 1.3+ structural types, khối `moved`, `import` khai báo, `terraform test`, HCP Terraform Workspaces, và các câu hỏi bẫy về thứ tự ưu tiên của biến số).

Bài viết này được thiết kế như một **Khóa Huấn Luyện Cấp Tốc (Crash Course)**: hệ thống hóa trọn vẹn 9 chuyên đề thi cốt lõi, mổ xẻ các cạm bẫy thường gặp trong đề thi thật, hướng dẫn chiến lược làm bài thi trực tuyến và cung cấp **Bộ đề thi mô phỏng 25 câu hỏi độc quyền** sát đề thi 100% kèm phân tích đáp án chi tiết.

---

## 1. Cấu Trúc Đề Thi & 9 Chuyên Đề Cốt Lõi (Exam Objectives)

```mermaid
pie title Tỷ Trọng 9 Chuyên Đề Trong Kỳ Thi Terraform Associate (003)
    "1. Understand IaC concepts" : 10
    "2. Understand Terraform's purpose" : 10
    "3. Understand Terraform basics" : 15
    "4. Use Terraform CLI" : 15
    "5. Interact with Terraform modules" : 12
    "6. Navigate Terraform workflow" : 15
    "7. Implement and maintain state" : 15
    "8. Read, generate, and modify config" : 13
    "9. Understand HCP Terraform capabilities" : 10


```

### 1.1. Thông Tin Tổng Quan Về Kỳ Thi
- **Mã kỳ thi**: `TA-003` (Terraform Associate 003).
- **Hình thức thi**: Trắc nghiệm trực tuyến có giám thị (Online Proctored qua PSI / Webassessor).
- **Thời gian làm bài**: **60 phút**.
- **Số lượng câu hỏi**: **45 - 57 câu** (Bao gồm Multiple Choice, Multiple Select, và Fill-in-the-blank điền từ vào chỗ trống).
- **Điểm đạt (Passing Score)**: Thường khoảng **70% - 75%** trở lên.
- **Thời hạn hiệu lực**: **2 năm**.

---

## 2. Hệ Thống Hóa 9 Trụ Cột Kiến Thức Trọng Tâm

```mermaid
mindmap
  root((Terraform Associate 003))
    ["Trụ Cột 1 & 2: IaC & Architecture"]
      ["Declarative vs Imperative"]
      ["Idempotency: Ap dung nhieu lan cung 1 ket qua"]
      ["Plugin Architecture: Core vs Provider qua gRPC"]
    ["Trụ Cột 3 & 4: CLI & Workflow"]
      ["init -&gt; plan -&gt; apply -&gt; destroy"]
      ["terraform fmt -check -recursive"]
      ["terraform validate: Chi kiem tra syntax & schema"]
      ["terraform state: list, show, mv, rm, pull, push"]
    ["Trụ Cột 5 & 6: Modules & Lifecycle"]
      ["Module inputs, outputs, source, version"]
      ["lifecycle: create_before_destroy, prevent_destroy, ignore_changes"]
      ["replace_triggered_by (TF 1.2+)"]
    ["Trụ Cột 7 & 8: State & HCL Deep Dive"]
      ["Remote State: S3 + DynamoDB Locking"]
      ["Thu tu uu tien bien so: -var &gt; tfvars &gt; env &gt; default"]
      ["Functions, Type constraints, Dynamic blocks"]
      ["moved va import blocks"]
    ["Trụ Cột 9: HCP Terraform"]
      ["Workspaces: VCS, CLI, API"]
      ["Variable Sets, Private Registry, Cost Estimation"]


```

---

## 3. Bảng Thứ Tự Ưu Tiên Biến Số (Variable Precedence) - Câu Hỏi Chắc Chắn Xuất Hiện!

Một trong những câu hỏi bẫy kinh điển nhất trong phòng thi là xác định giá trị cuối cùng của biến số khi được khai báo ở nhiều nơi.

```mermaid
flowchart TD
    P1["1. Cờ Dòng Lệnh CLI: -var hoặc -var-file (ƯU TIÊN CAO NHẤT)"]
    P2["2. Tệp *.auto.tfvars hoặc *.auto.tfvars.json (Theo thứ tự từ điển)"]
    P3["3. Tệp terraform.tfvars.json"]
    P4["4. Tệp terraform.tfvars"]
    P5["5. Biến Môi Trường Hệ Điều Hành: TF_VAR_[variable_name]"]
    P6["6. Giá Trị Mặc Định Trong Code: default = ... (ƯU TIÊN THẤP NHẤT)"]

    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> P6

    style P1 fill:none,stroke:#28a745,stroke-width:2px
    style P5 fill:none,stroke:#f57c00,stroke-width:2px
    style P6 fill:none,stroke:#c62828,stroke-width:2px


```

> [!IMPORTANT]
> **Quy Tắc Vàng Cần Nhớ**:
> **CLI Flag `-var` > `*.auto.tfvars` > `terraform.tfvars` > `TF_VAR_*` > `default`**.
> Nếu đề thi hỏi biến môi trường `TF_VAR_region="us-west-1"` có ghi đè được file `terraform.tfvars` có giá trị `"ap-southeast-1"` không? Câu trả lời dứt khoát là **KHÔNG**! File `terraform.tfvars` luôn có độ ưu tiên cao hơn biến môi trường!

---

## 4. Phân Tích 5 Cạm Bẫy Đề Thi Kinh Điển (Trap Analysis)

### Bẫy 1: Sự Khác Biệt Giữa `terraform fmt` và `terraform validate`
- **Đề bài thường hỏi**: *"Lệnh nào dùng để kiểm tra xem cấu hình có đúng cú pháp HCL và schema thuộc tính không?"*
- **Bẫy**: Nhiều thí sinh chọn `terraform fmt`.
- **Sự thật**: 
  - `terraform fmt`: Chỉ định dạng lại code (thụt lề khoảng trắng, căn lề dấu bằng `=`). Nó **không kiểm tra tính đúng đắn của logic**.
  - `terraform validate`: Kiểm tra cú pháp HCL và đối chiếu với Provider Schema (xem thuộc tính có tồn tại không). Nó **yêu cầu phải chạy `terraform init` trước**.

### Bẫy 2: `terraform refresh` có làm thay đổi hạ tầng thực tế trên Cloud không?
- **Đề bài thường hỏi**: *"Lệnh `terraform refresh` sẽ cập nhật Cloud theo State hay cập nhật State theo Cloud?"*
- **Sự thật**: `terraform refresh` (hoặc `terraform apply -refresh-only`) **CHỈ ĐỌC DỮ LIỆU TỪ CLOUD ĐỂ CẬP NHẬT VÀO STATE FILE**. Nó **tuyệt đối không làm thay đổi hay tạo/xóa bất kỳ tài nguyên nào trên Cloud**!

### Bẫy 3: Biến Môi Trường Bật Debug Log
- **Câu hỏi điền từ (Fill-in-the-blank)**: *"Biến môi trường nào được sử dụng để thiết lập mức độ chi tiết của nhật ký ghi log trong Terraform?"*
- **Đáp án chính xác**: **`TF_LOG`** (Các giá trị hợp lệ: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `OFF`).
- **Biến chỉ định đường dẫn file log**: **`TF_LOG_PATH`**.

### Bẫy 4: Module Source và Tự Động Tải Plugin
- **Đề bài thường hỏi**: *"Khi bạn thêm một module mới vào file `main.tf`, bạn cần chạy lệnh nào để Terraform tải module đó về?"*
- **Sự thật**: Bắt buộc phải chạy **`terraform init`** (hoặc `terraform get`). Lệnh `terraform plan` sẽ bị lỗi nếu module mới chưa được khởi tạo.

### Bẫy 5: `prevent_destroy` có bảo vệ tài nguyên khi chạy `terraform destroy` không?
- **Sự thật**: **CÓ**. Nếu bất kỳ tài nguyên nào trong State có `lifecycle { prevent_destroy = true }`, lệnh `terraform destroy` sẽ bị chặn đứng ngay lập tức và ném ra lỗi Fatal Error.

---

## 5. Bộ Đề Thi Thử Nghiệm 25 Câu Sát Đề Thi Thật (kèm Lời Giải Chi Tiết)

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q01</span>
    <span>**: Bạn vừa sửa đổi mã nguồn Terraform để thêm một biến số mới và muốn kiểm tra nhanh xem cú pháp có hợp lệ hay không mà không cần kết nối tới Cloud Provider API. Bạn nên chạy lệnh nào?
- A. `terraform plan -refresh=false`
- B. `terraform validate`
- C. `terraform fmt`
- D. `terraform show</span>
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
  **Đáp án đúng: B**
**Giải thích**: `terraform validate` kiểm tra cú pháp HCL và tính hợp lệ của các thuộc tính schema cục bộ dựa trên các plugin provider đã tải về trong thư mục `.terraform/`, không cần gửi yêu cầu mạng đến Cloud API.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q02</span>
    <span>**: Cho các cấu hình sau cho biến `instance_count`:
1. `default = 2` trong `variables.tf`
2. `instance_count = 4` trong `terraform.tfvars`
3. `instance_count = 6` trong `prod.auto.tfvars`
4. Biến môi trường `TF_VAR_instance_count = 8`
5. Lệnh CLI: `terraform apply -var="instance_count=10"`

Giá trị nào sẽ được Terraform áp dụng khi chạy lệnh trên?
- A. 2
- B. 4
- C. 6
- D. 10</span>
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
  **Đáp án đúng: D**
**Giải thích**: Cờ dòng lệnh `-var` có mức độ ưu tiên cao nhất trong toàn bộ hệ thống phân cấp biến số của Terraform.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q03</span>
    <span>**: Đội ngũ của bạn đang cấu hình S3 Backend cho Terraform State. Dịch vụ AWS nào bắt buộc phải được kết hợp để cung cấp tính năng State Locking (Khóa trạng thái chống xung đột)?
- A. AWS Secrets Manager
- B. AWS DynamoDB
- C. AWS KMS
- D. AWS CloudWatch</span>
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
  **Đáp án đúng: B**
**Giải thích**: S3 Remote Backend sử dụng bảng DynamoDB (với Partition Key là `LockID`) để thực hiện cơ chế Distributed State Locking.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q04</span>
    <span>**: Điền vào chỗ trống: Để chỉ định mức độ ghi log chi tiết nhất phục vụ việc điều tra lỗi sâu của Terraform Core và Provider, bạn cần thiết lập biến môi trường `TF_LOG` có giá trị là `_______`.</span>
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
  **Đáp án đúng: TRACE** (hoặc `trace`)
**Giải thích**: `TRACE` là mức độ log chi tiết nhất của Terraform, ghi nhận toàn bộ payload HTTP request/response và các bước phân tích đồ thị DAG.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q05</span>
    <span>**: Bạn muốn đổi tên một tài nguyên trong State từ `aws_instance.web` thành `aws_instance.app_server` mà **không làm phá hủy và tạo lại** máy chủ EC2 thực tế trên AWS. Bạn có thể sử dụng giải pháp nào? (Chọn 2 đáp án)
- A. Sửa tên trong code và chạy `terraform apply -replace=aws_instance.web`
- B. Thêm khối `moved { from = aws_instance.web to = aws_instance.app_server }` vào code
- C. Chạy lệnh CLI: `terraform state mv aws_instance.web aws_instance.app_server`
- D. Chạy lệnh CLI: `terraform refresh -target=aws_instance.web</span>
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
  **Đáp án đúng: B và C**
**Giải thích**: Cả khối khai báo `moved` (Terraform 1.1+) và lệnh CLI `terraform state mv` đều thực hiện việc cập nhật lại địa chỉ định danh của tài nguyên trong State file mà không gửi lệnh hủy tài nguyên lên Cloud.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q06</span>
    <span>**: Tính chất nào sau đây của Infrastructure as Code đảm bảo rằng khi bạn áp dụng cùng một cấu hình Terraform nhiều lần liên tiếp, kết quả trạng thái hạ tầng trên Cloud luôn không đổi?
- A. Immutability
- B. Idempotency (Tính bất biến)
- C. Declarative
- D. Scalability</span>
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
  **Đáp án đúng: B**
**Giải thích**: `Idempotency` (Tính bất biến / Tính lũy đẳng) là nguyên lý cốt lõi: Áp dụng một cấu hình N lần sẽ tạo ra kết quả giống hệt như áp dụng 1 lần duy nhất nếu không có sự thay đổi trong code.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q07</span>
    <span>**: Tại sao HashiCorp khuyến cáo coi Provisioners (`local-exec`, `remote-exec`) là giải pháp cuối cùng (Last Resort)?
- A. Vì Provisioners làm chậm quá trình biên dịch HCL
- B. Vì Provisioners phá vỡ tính Declarative, không thể phát hiện Drift và dễ khiến tài nguyên bị đánh dấu Tainted khi gặp lỗi mạng
- C. Vì Provisioners không hỗ trợ hệ điều hành Linux
- D. Vì Provisioners yêu cầu bản quyền HCP Terraform Enterprise</span>
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
  **Đáp án đúng: B**
**Giải thích**: Provisioners chạy shell script mệnh lệnh (Imperative), Terraform không thể theo dõi trạng thái thay đổi bên trong máy chủ, và nếu script lỗi thì máy chủ bị taint, buộc phải tạo lại ở lần apply sau.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q08</span>
    <span>**: Trong HCP Terraform (Terraform Cloud), tính năng nào cho phép bạn định nghĩa một tập hợp các biến số (Variables) hoặc Secrets dùng chung và tự động gán cho hàng chục Workspaces khác nhau?
- A. Run Triggers
- B. Variable Sets
- C. Private Registry
- D. Agent Pools</span>
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
  **Đáp án đúng: B**
**Giải thích**: Variable Sets cho phép quản lý tập trung các biến số môi trường và bí mật, sau đó áp dụng cho toàn bộ Organization hoặc các Workspaces được chỉ định.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q09</span>
    <span>**: Chuỗi Module Source nào sau đây thể hiện việc tải một Child Module từ Terraform Public Registry chính thức?
- A. `source = "git::https://github.com/terraform-aws-modules/terraform-aws-vpc.git"`
- B. `source = "terraform-aws-modules/vpc/aws"`
- C. `source = "./modules/vpc"`
- D. `source = "s3::https://s3.amazonaws.com/my-bucket/vpc.zip"</span>
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
  **Đáp án đúng: B**
**Giải thích**: Cấu trúc `<NAMESPACE>/<NAME>/<PROVIDER>` là định dạng chuẩn để kéo module trực tiếp từ Terraform Public Registry.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q10</span>
    <span>**: Khi nào bạn **bắt buộc** phải sử dụng meta-argument `depends_on` trong một resource?
- A. Khi một resource sử dụng thuộc tính ID của resource khác (ví dụ: `vpc_id = aws_vpc.main.id`)
- B. Khi tồn tại một sự phụ thuộc ngầm định (Hidden/Implicit dependency) giữa hai tài nguyên mà Terraform không thể tự phát hiện thông qua tham chiếu thuộc tính HCL (ví dụ: EC2 cần IAM Role Policy gắn xong trước)
- C. Luôn luôn bắt buộc cho mọi resource để tăng tốc độ apply
- D. Khi muốn kích hoạt tính năng Zero-Downtime</span>
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
  **Đáp án đúng: B**
**Giải thích**: Với các phụ thuộc tường minh qua biến (`aws_vpc.main.id`), Terraform tự động dựng DAG. `depends_on` chỉ được dùng cho các phụ thuộc ẩn (Implicit/Hidden dependencies) mà HCL không thể tự suy diễn.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q11</span>
    <span>**: Bạn muốn ngăn chặn việc một kỹ sư vô tình xóa nhầm Production Database khi chạy `terraform destroy`. Meta-argument nào trong khối `lifecycle` phải được cấu hình?
- A. `create_before_destroy = true`
- B. `ignore_changes = all`
- C. `prevent_destroy = true`
- D. `replace_triggered_by = []</span>
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
  **Đáp án đúng: C**
**Giải thích**: `prevent_destroy = true` sẽ từ chối bất kỳ kế hoạch nào có chứa hành động hủy tài nguyên.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q12</span>
    <span>**: Lệnh nào sau đây dùng để xem toàn bộ danh sách các tài nguyên đang được theo dõi bên trong tệp State hiện tại?
- A. `terraform state show`
- B. `terraform state list`
- C. `terraform state pull`
- D. `terraform state inspect</span>
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
  **Đáp án đúng: B**
**Giải thích**: `terraform state list` in ra danh sách đầy đủ địa chỉ của tất cả các resources và data sources trong State.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q13</span>
    <span>**: Để tạo tài nguyên trên 2 AWS Region khác nhau trong cùng một tệp cấu hình, bạn cần sử dụng thuộc tính nào trong khối `provider`?
- A. `alias`
- B. `label`
- C. `name`
- D. `region_id</span>
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
  **Đáp án đúng: A**
**Giải thích**: `alias` cho phép khởi tạo nhiều thực thể Provider khác nhau của cùng một Cloud Provider.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q14</span>
    <span>**: Điểm khác biệt mấu chốt giữa `resource` và `data` source trong Terraform là gì?
- A. `resource` chỉ dùng để đọc thông tin, `data` dùng để tạo tài nguyên
- B. `resource` quản lý vòng đời tạo/sửa/xóa tài nguyên, `data` chỉ thực hiện thao tác Đọc (Read-only) dữ liệu đã tồn tại sẵn ngoài Cloud
- C. `data` source không lưu thông tin vào State file
- D. `resource` chỉ hỗ trợ Cloud AWS</span>
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
  **Đáp án đúng: B**
**Giải thích**: Data sources là các khối truy vấn dữ liệu chỉ đọc (Read-only), không tạo ra hay quản lý vòng đời tài nguyên.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q15</span>
    <span>**: Biểu thức điều kiện (Ternary operator) nào sau đây có cú pháp HCL hợp lệ?
- A. `instance_type = var.env == "prod" ? "t3.large" : "t3.micro"`
- B. `instance_type = if var.env == "prod" then "t3.large" else "t3.micro"`
- C. `instance_type = var.env == "prod" -> "t3.large" | "t3.micro"`
- D. `instance_type = switch(var.env) { "prod": "t3.large", default: "t3.micro" }</span>
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
  **Đáp án đúng: A**
**Giải thích**: HCL sử dụng cú pháp toán tử 3 ngôi chuẩn: `condition ? true_val : false_val`.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q16</span>
    <span>**: Điền vào chỗ trống: Khi cấu hình Remote Backend trên AWS S3, tên tệp lưu trữ trạng thái bên trong bucket được chỉ định thông qua tham số `_______`.</span>
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
  **Đáp án đúng: key**
**Giải thích**: Tham số `key` trong khối cấu hình `backend "s3"` định nghĩa đường dẫn S3 Object Key (ví dụ: `key = "prod/network/terraform.tfstate"`).

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q17</span>
    <span>**: Kể từ Terraform 1.3+, hàm meta-type nào cho phép bạn định nghĩa một thuộc tính tùy chọn kèm giá trị mặc định bên trong một `object` type constraint?
- A. `default()`
- B. `optional()`
- C. `nullable()`
- D. `coalesce()</span>
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
  **Đáp án đúng: B**
**Giải thích**: Cú pháp `optional(type, default_value)` cho phép tạo thuộc tính tùy chọn với giá trị mặc định bên trong structural object types.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q18</span>
    <span>**: Framework kiểm thử bản địa `terraform test` (kể từ Terraform 1.6+) lưu trữ các kịch bản kiểm thử trong các tệp có phần mở rộng là gì?
- A. `.tfspec`
- B. `.tftest.hcl` (hoặc `.tftest.json`)
- C. `.test.tf`
- D. `.spec.hcl</span>
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
  **Đáp án đúng: B**
**Giải thích**: Terraform test engine tự động tìm kiếm các tệp có đuôi `.tftest.hcl` hoặc `.tftest.json` trong thư mục `tests/`.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q19</span>
    <span>**: Trong HCP Terraform, loại Workspace nào sẽ tự động kích hoạt một lượt chạy Plan mỗi khi có Pull Request được tạo trên GitHub?
- A. CLI-driven Workspace
- B. VCS-driven Workspace
- C. API-driven Workspace
- D. Manual Workspace</span>
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
  **Đáp án đúng: B**
**Giải thích**: VCS-driven Workspace tích hợp trực tiếp qua Webhooks với các hệ thống Git (GitHub, GitLab) để tự động hóa kiểm tra PR.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q20</span>
    <span>**: Lệnh nào sau đây được sử dụng để giải phóng một khóa trạng thái bị kẹt khi tiến trình trước đó đã bị crash đột ngột?
- A. `terraform unlock`
- B. `terraform force-unlock <LOCK_ID>`
- C. `terraform state unlock`
- D. `terraform reset-lock</span>
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
  **Đáp án đúng: B**
**Giải thích**: `terraform force-unlock <LOCK_ID>` là lệnh chuẩn để gỡ bỏ Distributed State Lock bị kẹt.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q21</span>
    <span>**: Trong HCP Terraform, mức độ thực thi chính sách Sentinel nào cho phép người có thẩm quyền bấm nút Override bỏ qua cảnh báo để tiếp tục apply?
- A. `advisory`
- B. `soft-mandatory`
- C. `hard-mandatory`
- D. `optional</span>
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
  **Đáp án đúng: B**
**Giải thích**: `soft-mandatory` sẽ chặn pipeline nhưng cho phép người có quyền quản trị (Admin/Lead) thực hiện hành động Override để tiếp tục apply.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q22</span>
    <span>**: Ràng buộc phiên bản `version = "~> 2.1.0"` trong khối `required_providers` sẽ chấp nhận phiên bản nào sau đây?
- A. `2.2.0`
- B. `2.1.4`
- C. `3.0.0`
- D. `2.0.9</span>
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
  **Đáp án đúng: B**
**Giải thích**: Toán tử Pessimistic constraint `~> 2.1.0` chỉ cho phép cập nhật chữ số cuối cùng bên phải (Patch version: `>= 2.1.0` và `< 2.2.0`).

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q23</span>
    <span>**: Khai báo `sensitive = true` trên một output có tác dụng gì?
- A. Tự động mã hóa giá trị đó trong file `terraform.tfstate`
- B. Ẩn giá trị đó khi hiển thị trên màn hình CLI console hoặc logs CI/CD
- C. Xóa giá trị đó khỏi bộ nhớ RAM
- D. Yêu cầu nhập mật khẩu mỗi khi chạy apply</span>
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
  **Đáp án đúng: B**
**Giải thích**: `sensitive = true` chỉ có tác dụng ở tầng giao diện hiển thị CLI/Logs, dữ liệu vẫn được lưu trữ nguyên vẹn dưới dạng plaintext trong State file.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q24</span>
    <span>**: Khối `moved` được HashiCorp giới thiệu chính thức từ phiên bản Terraform nào?
- A. Terraform 0.12
- B. Terraform 0.14
- C. Terraform 1.1
- D. Terraform 1.5</span>
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
  **Đáp án đúng: C**
**Giải thích**: Khối `moved` chính thức ra mắt từ phiên bản **Terraform 1.1+**.

---
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q25</span>
    <span>**: Khối cấu hình nào sau đây được khuyến nghị sử dụng kể từ Terraform 1.1+ để kết nối trực tiếp với HCP Terraform thay thế cho `backend "remote"`?
- A. `cloud` block
- B. `hcp` block
- C. `enterprise` block
- D. `remote_state` block</span>
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
  **Đáp án đúng: A**
**Giải thích**: Khối `cloud { organization = ... workspaces { ... } }` là tiêu chuẩn hiện đại để tích hợp với HCP Terraform.

---
</div>
</details>

## 6. Chiến Lược Làm Bài Thi Trực Tuyến Đạt Điểm Cao

```mermaid
graph TD
    S1["Vòng 1: Làm Hết Các Câu Dễ & Chắc Chắn \n Mục tiêu: 35 câu trong 25 phút"] --> S2["Vòng 2: Xử Lý Các Câu Tình Huống & Phân Vân \n Đánh dấu Flag for Review - 20 phút"]
    S2 --> S3["Vòng 3: Rà Soát Toàn Bộ & Kiểm Tra Điền Từ \n 15 phút cuối cùng"]
    S3 --> SUBMIT["Bấm Nộp Bài: PASS VỚI ĐIỂM SỐ 90%+"]

    style S1 fill:none,stroke:#2e7d32,stroke-width:2px
    style S2 fill:none,stroke:#f57c00,stroke-width:2px
    style S3 fill:none,stroke:#0288d1,stroke-width:2px
    style SUBMIT fill:none,stroke:#28a745,stroke-width:2px


```

### 3 Lời Khuyên Vàng Trong Phòng Thi:
1. **Quản trị thời gian (Time Management)**: Bạn có 60 phút cho ~50 câu hỏi, tương đương **khoảng 1 phút 10 giây cho mỗi câu**. Đừng bao giờ dừng lại quá 2 phút ở một câu hỏi khó. Hãy chọn tạm một đáp án khả dĩ nhất, bấm nút **"Flag for Review"** và đi tiếp!
2. **Kỹ thuật loại trừ (Elimination Technique)**: Mỗi câu hỏi trắc nghiệm thường có 2 đáp án sai ngớ ngẩn (chứa các lệnh hoặc cú pháp không hề tồn tại trong Terraform, ví dụ: `terraform update` hay `terraform state delete`). Hãy gạch bỏ chúng trước để tăng tỷ lệ chọn đúng lên 50%.
3. **Cẩn thận với câu hỏi điền từ**: Kiểm tra kỹ lỗi chính tả (Spelling). Viết đúng chữ thường/chữ hoa theo quy ước CLI (ví dụ: `terraform.tfstate`, `TF_LOG`, `local-exec`).

---

## 7. Tổng Kết & Lộ Trình Về Đích

- **Bản lĩnh phòng thi**: Tự tin vào nền tảng thực chiến đã tích lũy qua 28 bài học chuyên sâu trước đó.
- **Tài liệu ôn tập cốt lõi**: Xem lại bảng thứ tự ưu tiên biến số, các câu lệnh State CLI (`mv`, `rm`, `pull`, `push`), và các meta-arguments trong khối `lifecycle`.
- **Bước tiếp theo**: Trong [Bài 30: Capstone Project: Xây Dựng Nền Tảng Hạ Tầng Enterprise Đa Tầng End-to-End](./30-capstone-xay-dung-nen-tang-ha-tang-enterprise-da-tang-end-to-end.md), chúng ta sẽ bước vào trận đánh lớn cuối cùng: Tự tay hiện thực hóa toàn bộ các kỹ thuật đã học vào một đồ án tốt nghiệp Capstone Project quy mô lớn chuẩn Production!
{% endraw %}
