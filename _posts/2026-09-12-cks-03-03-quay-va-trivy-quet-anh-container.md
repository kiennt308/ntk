---
layout: post
title: "[Bài 03] Quét Lỗ Hổng & Làm Cứng Container: Tích Hợp Trivy Scanner, Quay Registry & Dockerfile Hardening"
date: 2026-09-12 12:40:00 +0700
categories: [CKS]
tags:
  - CKS
  - Kubernetes
  - Security
  - Hardening
  - DevSecOps
  - Part-03
series: "CKS Security Specialist Mastery"
series_order: 3
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80"
summary: "[CKS P.03] Hướng dẫn chuyên sâu Quét Lỗ Hổng & Làm Cứng Container: Tích Hợp Trivy Scanner, Quay Registry & Dockerfile Hardening: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Quét Lỗ Hổng & Làm Cứng Container: Tích Hợp Trivy Scanner, Quay Registry & Dockerfile Hardening."
  - "Làm chủ các thao tác lệnh kubectl tốc độ cao, xử lý sự cố cụm thực tế và tối ưu hóa tài nguyên Pod/Node."
  - "Củng cố kỹ năng thực chiến sát với đề thi chứng chỉ quốc tế của Linux Foundation / CNCF."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 03] QUÉT LỖ HỔNG & LÀM CỨNG CONTAINER: TÍCH HỢP TRIVY SCANNER, QUAY REGISTRY & DOCKERFILE HARDENING

Trong kỷ nguyên điện toán đám mây và kiến trúc microservices phân tán quy mô lớn, **Kubernetes (CKS)** đóng vai trò là nền tảng điều phối container (Container Orchestration) tiêu chuẩn công nghiệp. Để làm chủ hệ thống trong môi trường sản xuất (Production) cũng như chinh phục kỳ thi chứng chỉ quốc tế của Linux Foundation / CNCF, kỹ sư không chỉ nắm vững các câu lệnh thao tác cơ bản mà phải thấu hiểu sâu sắc bản chất cơ chế tầng thấp: từ chu trình điều hòa (Reconciliation Loop), cấu trúc điều phối tài nguyên, kiến trúc mạng CNI, lưu trữ CSI cho đến các chuẩn mực an ninh phòng thủ chiều sâu.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn giải mã toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp bài thực hành Lab từng bước và bộ câu hỏi phỏng vấn chuẩn Architect / Lead Engineer.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

| # | Câu hỏi ôn tập | Đáp án chuẩn ngắn gọn |
|---|---|---|
| 1 | Annotation ép buộc chuyển 100% traffic HTTP sang HTTPS? | **`nginx.ingress.kubernetes.io/ssl-redirect: "true"`** |
| 2 | Annotation mã hóa mTLS end-to-end tới Pod backend? | **`nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"`** |
| 3 | Bộ đôi annotation giới hạn Rate Limit chống DDoS L7? | **`limit-rps`** và **`limit-connections`** |
| 4 | Annotation chỉ cho phép dải IP chỉ định truy cập Ingress? | **`nginx.ingress.kubernetes.io/whitelist-source-range`** |
| 5 | Bộ đôi cờ annotation và snippet kích hoạt ModSecurity WAF? | **`enable-modsecurity: "true"`** và **`SecRuleEngine On`** |



> **"Bảo vệ chuỗi cung ứng phần mềm bằng kỹ thuật quét lỗ hổng ảnh container và gia cố Dockerfile (Container Image Scanning & Dockerfile Hardening) là nội dung bắt buộc thuộc miền Supply Chain Security (20%) trong chứng chỉ CKS, đòi hỏi chuyên gia bảo mật phải làm chủ công cụ quét mã nguồn mở Trivy để tự động phát hiện các lỗ hổng an ninh đã biết (CVEs) ở các mức độ nghiêm trọng `CRITICAL` và `HIGH`; áp dụng triệt để kỹ thuật Multi-stage build và chọn các ảnh cơ sở tối giản (Distroless hay Alpine) để triệt tiêu các công cụ bash/curl thừa; gán quyền người dùng không phải root (`USER 10001`); đồng thời thiết lập rào chắn tự động chặn các ảnh container có chứa lỗ hổng nguy hiểm trước khi được triển khai vào cụm Kubernetes Production."**

**Kết quả từ các buổi trước được sử dụng lại:**

| Kết quả / Công cụ | Buổi + số hiệu `QT` | Dùng ở đâu trong buổi này |
|---|---|---|
| Kỹ thuật build ảnh Dockerfile căn bản | Buổi 31 `QT 4.1` | Nâng cấp Dockerfile sang chuẩn gia cố CKS Hardening |
| Thiết lập `runAsNonRoot: true` | Buổi 41 `QT 4.1` | Khai báo chỉ thị `USER 10001` trong Dockerfile |
| Cụm và CLI Kubernetes | Buổi 08 `QT 4.1` | Chạy lệnh `trivy` quét ảnh trực tiếp từ node |

---



| # | Kỹ năng thực hiện được | Hiện vật chứng minh |
|---|---|---|
| 1 | Thực thi thành thạo lệnh CLI `trivy image` quét và trích xuất lỗ hổng CVE | Báo cáo quét lỗ hổng Trivy xuất định dạng text/json |
| 2 | Sử dụng cờ `--severity CRITICAL` và `--ignore-unfixed` lọc kết quả | Báo cáo lọc chuẩn xác các lỗ hổng có bản vá nguy hiểm nhất |
| 3 | Biên soạn tệp Dockerfile gia cố dùng Multi-stage build và Distroless | Tệp `Dockerfile.hardened` chuẩn CKS |
| 4 | Cấu hình chỉ thị `USER 10001` loại bỏ quyền root khỏi container runtime | Đầu ra lệnh `id` trong container in ra UID `10001` |
| 5 | Tích hợp Trivy vào script CI/CD tự động chặn build khi có lỗ hổng | Script Bash chứa cờ `trivy image --exit-code 1` |

---



| Kiến thức tiên quyết | Nguồn tự học nếu thiếu |
|---|---|
| Các chỉ thị tệp Dockerfile (FROM, RUN, COPY, CMD) | Buổi 31 (`QT 4.1`) |
| Nguyên tắc SecurityContext non-root | Buổi 41 (`QT 4.1`) |
| CKS Securing Ingress & WAF Hardening | Buổi 47 (`QT 7.1`) |

---



### 3.1. Thuật ngữ Việt–Anh

| # | Thuật ngữ tiếng Việt | Tiếng Anh tương đương | Ghi chú chuẩn hoá trong thân bài |
|---|---|---|---|
| 1 | Quét lỗ hổng ảnh container | Container Image Vulnerability Scanning | Quá trình soi chiếu ảnh container với cơ sở dữ liệu lỗ hổng |
| 2 | Công cụ quét Trivy | Trivy Vulnerability Scanner | Công cụ mã nguồn mở quét lỗ hổng CVEs chính thức trong CKS |
| 3 | Lỗ hổng an ninh đã biết | Common Vulnerabilities and Exposures (CVE) | Mã danh định quốc tế cho các lỗ hổng an toàn thông tin |
| 4 | Mức độ nghiêm trọng lỗ hổng | Vulnerability Severity Level | Các cấp độ nguy hiểm (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) |
| 5 | Ảnh cơ sở không hệ điều hành | Distroless Base Image | Ảnh container tối giản của Google loại bỏ hoàn toàn OS shell |
| 6 | Biên dịch nhiều giai đoạn | Multi-stage Build | Kỹ thuật tách giai đoạn build và giai đoạn runtime trong Dockerfile |
| 7 | Gia cố tệp đóng gói ảnh | Dockerfile Hardening | Áp dụng các nguyên tắc bảo mật tối thiểu vào chỉ thị Dockerfile |
| 8 | Người dùng không phải root | Non-root User (`USER 10001`) | Khai báo chỉ thị USER để container chạy dưới quyền user thường |
| 9 | Bảo mật chuỗi cung ứng | Supply Chain Security | Bảo vệ toàn bộ vòng đời ứng dụng từ mã nguồn tới container |
| 10 | Bỏ qua lỗ hổng chưa có bản vá | Ignore Unfixed (`--ignore-unfixed`) | Cờ cấm báo cáo các lỗ hổng CVEs chưa được phát hành bản vá |
| 11 | Mã thoát báo lỗi CLI | Exit Code (`--exit-code 1`) | Cờ trả về exit code 1 làm thất bại bước build CI/CD |
| 12 | Bề mặt tấn công container | Container Attack Surface | Tổng các điểm yếu và thư viện có thể bị hacker khai thác |
| 13 | Kho chứa ảnh Quay.io | Quay Container Registry | Kho chứa ảnh bảo mật hỗ trợ tích hợp quét lỗ hổng tự động |
| 14 | Bảng danh mục thành phần | Software Bill of Materials (SBOM) | Danh sách khai báo toàn bộ các thư viện thành phần trong ảnh |



Mô hình Kiểm định An toàn Vệ sinh Thực phẩm và Dây chuyền Đóng hộp: Ảnh container giống như một Hộp thực phẩm đóng sẵn từ nhà máy. Công cụ `Trivy` giống như Máy Quét Kiểm Định Vi Sinh tự động soi chiếu hộp thực phẩm để phát hiện vi khuẩn/độc tố (CVEs ở mức `CRITICAL`). `Dockerfile Hardening` giống như Quy trình Chế biến Sạch: `Distroless` là loại bỏ hoàn toàn các phụ gia thừa (shell, curl, apt); `Multi-stage build` là chỉ giữ lại sản phẩm tinh chế cuối cùng; `USER 10001` là dán nhãn quy định hộp thực phẩm không được chứa hóa chất độc hại (root priviliges).

---

### 1.1. Tổng quan quét lỗ hổng ảnh container và công cụ Trivy (12 phút)

**Nguyên lý cốt lõi:** Trong bài thi CKS, sử dụng cú pháp lệnh `trivy image --severity CRITICAL,HIGH <image-name>` để lọc chuẩn xác 100% các lỗ hổng nguy hiểm nhất của ảnh container.

**Giải thích cơ chế ngầm:** Một ảnh container hệ điều hành thông thường (như `ubuntu:18.04` cũ) có thể chứa hàng trăm lỗ hổng nhỏ (`LOW`/`MEDIUM`). Việc lọc theo mức `CRITICAL,HIGH` giúp chuyên gia bảo mật tập trung xử lý các lỗ hổng thực sự nguy hiểm có thể bị khai thác ngay lập tức.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chạy lệnh `trivy image <image>` không có cờ `--severity` sinh ra bản báo cáo hàng ngàn dòng gây nhiễu và khó tìm lỗ hổng nguy cấp trong bài thi bấm giờ.

**Minh hoạ.**

```mermaid
graph TD
    Image[Ảnh Container Image] -->|"1. Scanned by"| Trivy[Trivy Vulnerability Scanner]
    Trivy -->|"2. Filter"| Filter{"Severity Check"}
    Filter -->|"CRITICAL / HIGH"| Report[Trích xuất danh sách CVEs nguy hiểm]
    Filter -->|"LOW / MEDIUM"| Ignore[Bỏ qua các cảnh báo nhẹ]
```

**Nguyên lý cốt lõi:** Thêm cờ `--ignore-unfixed` trong lệnh Trivy (`trivy image --severity CRITICAL --ignore-unfixed <image>`) để loại bỏ các lỗ hổng CVEs chưa có bản vá chính thức, tránh làm báo cáo bị nhiễu.

**Giải thích cơ chế ngầm:** Trong thực tế và bài thi, những lỗ hổng chưa có bản vá (`Unfixed CVEs`) từ phía nhà sản xuất OS thì lập trình viên không thể tự sửa bằng lệnh update được. Cờ `--ignore-unfixed` giúp tập trung 100% vào các lỗ hổng ĐÃ CÓ BẢN VÁ có thể khắc phục được ngay.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bỏ qua cờ `--ignore-unfixed` dẫn đến việc cố gắng tìm bản vá cho một CVE chưa tồn tại bản sửa lỗi làm mất thời gian vô ích.

**Minh hoạ.**

```bash
# Lệnh quét Trivy chuẩn CKS:
trivy image --severity CRITICAL --ignore-unfixed nginx:alpine
```

---

### 1.2. Kỹ thuật gia cố Dockerfile chuẩn CKS (Distroless, Non-Root, Multi-stage) (12 phút)

**Nguyên lý cốt lõi:** Luôn sử dụng kỹ thuật Multi-stage Build và ảnh cơ sở tối giản (như `gcr.io/distroless/static` hay `alpine`) để giảm thiểu bề mặt tấn công và triệt tiêu các công cụ nguy hiểm (như `bash`, `curl`, `nc`).

**Giải thích cơ chế ngầm:** Ảnh cơ sở Distroless chỉ chứa duy nhất ứng dụng và các thư viện phụ thuộc tối thiểu của nó, không có hệ điều hành shell (`/bin/sh`), trình quản lý gói (`apt`/`apk`), hay công cụ mạng. Hacker nếu có chiếm được container cũng không có shell để thực thi lệnh độc hại.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dùng ảnh `ubuntu:latest` đầy đủ công cụ build ở giai đoạn runtime làm dung lượng ảnh phình to > 500MB và chứa hàng chục lỗ hổng CVEs.

**Minh hoạ.**

```dockerfile
# Stage 1: Build ứng dụng (Dùng SDK đầy đủ)
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp .

# Stage 2: Runtime (Dùng Distroless siêu sạch)
FROM gcr.io/distroless/static-debian11
WORKDIR /app
COPY --from=builder /app/myapp .
USER 10001:10001
CMD ["./myapp"]
```

**Nguyên lý cốt lõi:** Trong tệp Dockerfile chuẩn CKS Hardening, BẮT BUỘC phải chứa chỉ thị `USER 10001` (hoặc tên user thường) ở giai đoạn runtime để đảm bảo container KHÔNG BAO GIỜ chạy dưới quyền `root`.

**Giải thích cơ chế ngầm:** Mặc định nếu không khai báo chỉ thị `USER`, container sẽ khởi chạy với UID `0` (root). Nếu kẻ tấn công khai thác được lỗ hổng tràn bộ đệm trong container, chúng sẽ có quyền root trên container và có nguy cơ thoát rào chắn (container breakout) tấn công Host Node.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bỏ qua chỉ thị `USER` làm container chạy mặc định dưới quyền root vi phạm tiêu chuẩn CKS Hardening.

**Minh hoạ.**

```dockerfile
# Khai báo User phi root bắt buộc:
USER 10001:10001
```

---

### 1.3. Tích hợp Trivy vào CI/CD Pipeline và tự động chặn Deployment (10 phút)

**Nguyên lý cốt lõi:** Tích hợp Trivy vào CI/CD pipeline với cờ `--exit-code 1` (`trivy image --exit-code 1 --severity CRITICAL <image>`) để tự động đánh sập (fail) pipeline nếu phát hiện lỗ hổng `CRITICAL`.

**Giải thích cơ chế ngầm:** Đảm bảo chính sách Shift-Left Security: ngăn chặn các ảnh container độc hại hoặc chưa vá lỗi bị đẩy lên Container Registry hoặc triển khai vào cụm Production ngay từ bước biên dịch CI/CD.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chạy quét Trivy trong CI/CD nhưng không dùng cờ `--exit-code 1` làm pipeline vẫn xanh (Success) dù ảnh container dính lỗ hổng `CRITICAL`.

**Minh hoạ.**

```bash
# Script CI/CD chặn build ảnh dính lỗ hổng CRITICAL:
trivy image --exit-code 1 --severity CRITICAL --ignore-unfixed myrepo/myapp:v1
if [ $? -ne 0 ]; then
  echo "XÁC NHẬN: ẢNH DÍNH LỖ HỔNG CRITICAL - ĐÃ HỦY BUILD CI/CD!"
  exit 1
fi
```

**Nguyên lý cốt lõi:** Không bao giờ cài đặt các trình quản lý gói (như `apt-get`, `yum`, `apk`) hoặc các công cụ biên dịch (như `gcc`, `make`) trong ảnh container giai đoạn runtime.

**Giải thích cơ chế ngầm:** Triệt tiêu các công cụ mà hacker có thể lợi dụng để tải xuống và biên dịch các đoạn mã độc hại (malware/rootkit) trực tiếp bên trong container đang chạy.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để lại `gcc` hay `curl` trong ảnh runtime tạo điều kiện cho hacker tải script đào tiền ảo về container.

**Minh hoạ.**

```dockerfile
# Loại bỏ cache trình quản lý gói ngay trong chỉ thị RUN:
RUN apk add --no-cache ca-certificates && rm -rf /var/cache/apk/*
```

**Nguyên lý cốt lõi:** Khi chẩn đoán lỗi Trivy báo lỗ hổng trong tệp Dockerfile, đối soát tên gói thư viện lỗi (Package Name) và phiên bản đã vá (Fixed Version) để cập nhật chỉ thị `RUN` nâng cấp bản vá.

**Giải thích cơ chế ngầm:** Trivy in rõ cột `INSTALLED` (phiên bản đang cài) và `FIXED VERSION` (phiên bản đã sửa lỗi). Học viên chỉ cần nâng cấp gói thư viện lên phiên bản `FIXED VERSION` để triệt tiêu CVE.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thay vì nâng cấp gói thư viện bị lỗi lại đi xóa toàn bộ ảnh container hoặc loay hoay không biết xem cột `FIXED VERSION`.

**Minh hoạ.**

```bash
# Kết quả quét Trivy:
# LIBRARY    VULNERABILITY ID   SEVERITY   INSTALLED   FIXED VERSION
# openssl    CVE-2023-0286      CRITICAL   1.1.1t-r0   1.1.1u-r0
# Sửa Dockerfile: RUN apk add --no-cache openssl>=1.1.1u-r0
```

---

### 1.4. Đưa vào cụm thật (4 phút)

**Nguyên lý cốt lõi:** Tệp Dockerfile chuẩn CKS Hardening hoàn chỉnh bắt buộc phải chứa: Multi-stage build (stage 1 `builder`, stage 2 `runtime`), ảnh cơ sở Distroless/Alpine, loại bỏ cache, khai báo `USER 10001` và `WORKDIR`.

**Giải thích cơ chế ngầm:** Đảm bảo đạt tiêu chuẩn bảo mật cao nhất cho chuỗi cung ứng container Production: dung lượng ảnh siêu nhỏ (< 20MB), 0 lỗ hổng `CRITICAL`, không chứa shell và chạy quyền user thường.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Viết Dockerfile 1 stage duy nhất dùng `node:latest` nặng > 1GB chứa hàng trăm lỗ hổng CVEs.

**Minh hoạ.**

```dockerfile
# Tệp Dockerfile chuẩn CKS Hardening:
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

FROM gcr.io/distroless/nodejs18-debian11
WORKDIR /app
COPY --from=builder /app ./
USER 10001
EXPOSE 3000
CMD ["server.js"]
```

**Áp vào cụm đang chạy thì làm gì trước:**
1. Chạy lệnh `trivy image` quét tất cả các ảnh container trước khi đẩy lên Quay.io hay Docker Hub.
2. Thiết lập rào chắn tự động trong CI/CD Jenkins/GitHub Actions với cờ `--exit-code 1`.
3. Chuyển đổi toàn bộ các Dockerfile ứng dụng nội bộ sang mô hình Multi-stage build và Distroless base image.

**Cái gì hỏng nếu áp thẳng lên prod:**
- Chuyển ứng dụng sang Distroless base image mà ứng dụng bắt buộc phải gọi lệnh hệ thống `sh` hay `curl` sẽ làm ứng dụng bị crash lỗi `exec: "sh": executable file not found`.

**Đo trước — đo sau:**
- So sánh dung lượng ảnh trước và sau khi gia cố (ví dụ 850MB -> 25MB).
- So sánh số lượng lỗ hổng CVEs từ Trivy (ví dụ 142 CVEs -> 0 CVEs Critical).

**Khi nào KHÔNG nên dùng:**
- Không dùng Distroless cho các container phục vụ mục đích gỡ lỗi (Debugging Pods) vì chúng cần có shell và các công cụ mạng như `ping`, `curl`, `netstat`.

---

### 1.5. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính | Làm đúng là |
|---|---|---|
| 1. Quên cờ `--ignore-unfixed` khi quét Trivy | Báo cáo bị nhiễu bởi các CVE chưa có bản sửa lỗi | Thêm cờ `--ignore-unfixed` trong lệnh trivy |
| 2. Container bị crash do Distroless thiếu shell | Ứng dụng dùng chỉ thị `CMD ["sh", "-c", "..."]` | Đổi sang cú pháp exec form `CMD ["./binary"]` |
| 3. Quên chỉ thị `USER 10001` trong Dockerfile | Container chạy dưới quyền root UID 0 | Thêm chỉ thị `USER 10001` ở stage runtime |
| 4. Để lại công cụ build (`gcc`, `make`) ở stage runtime | Dùng Dockerfile 1 stage không phân tách builder | Dùng Multi-stage build tách builder và runtime |
| 5. Quên cờ `--exit-code 1` trong script CI/CD | Trivy quét thấy CVE nhưng CI/CD vẫn báo xanh pass | Thêm cờ `--exit-code 1` để fail build khi dính CVE |
| 6. Đổi UID USER nhưng quên gán quyền sở hữu thư mục | Container bị lỗi Permission Denied khi ghi file | Khai báo `COPY --chown=10001:10001` |
| 7. Quét nhầm tag ảnh cũ `latest` thay vì tag cụ thể | Kết quả quét không phản ánh đúng ảnh đang chạy | Quét đúng tag phiên bản ảnh cụ thể (ví dụ `app:v1.2.3`) |
| 8. Không xóa cache trình quản lý gói | `apt-get install` để lại cache trong layer ảnh | Thêm `&& rm -rf /var/lib/apt/lists/*` |
| 9. Gõ sai từ khóa `--severity CRITICAL` | Viết in thường `critical` hoặc nhầm tên cờ | Gõ đúng in hoa `--severity CRITICAL,HIGH` |
| 10. `WORKDIR` không được khởi tạo trước chỉ thị `USER` | User 10001 không có quyền tạo thư mục WORKDIR | Khai báo `WORKDIR` TRƯỚC chỉ thị `USER 10001` |
| 11. Trivy bị chậm do chưa cập nhật DB lỗ hổng | Cơ sở dữ liệu lỗ hổng của Trivy bị lỗi thời | Chạy `trivy image --download-db-only` trước |
| 12. Quên cờ `--format json` khi tự động hóa script | Khó trích xuất dữ liệu lỗ hổng bằng bash | Thêm cờ `--format json` để trích xuất bằng jq |

---

### 1.6. Tóm tắt (2 phút)

```mermaid
graph TD
    SupplyChain[CKS Supply Chain Security] --> TrivyScan[1. Trivy Scanning: --severity CRITICAL --ignore-unfixed]
    SupplyChain --> MultiStage[2. Multi-stage Build: Tách builder và runtime]
    SupplyChain --> Distroless[3. Distroless Image: Loại bỏ OS Shell & Utilities]
    SupplyChain --> NonRoot[4. Non-root Hardening: USER 10001 & WORKDIR permissions]
    
    TrivyScan --> CICDPipeline[Tích hợp CI/CD: --exit-code 1 auto-block]
```

**Năm điều phải nhớ:**
1. **Lệnh Trivy chuẩn**: `trivy image --severity CRITICAL,HIGH --ignore-unfixed <image>`.
2. **Multi-stage build**: Tách giai đoạn build nặng ra khỏi giai đoạn runtime siêu nhẹ.
3. **Distroless Base Image**: Dùng ảnh không hệ điều hành để triệt tiêu shell và công cụ thừa.
4. **Chỉ thị USER 10001**: Bắt buộc chạy container dưới quyền user thường phi root.
5. **Chặn tự động CI/CD**: Dùng cờ `--exit-code 1` để tự động sập pipeline nếu dính lỗ hổng `CRITICAL`.

---

## §10. Câu hỏi tự kiểm tra (5 phút)


<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Công cụ <b style="color: var(--accent-primary);">Trivy</b> (của Aqua Security).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Lệnh <code>trivy image --severity CRITICAL nginx:alpine</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Cờ <code>--ignore-unfixed</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Cờ <code>--exit-code 1</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Kỹ thuật <b style="color: var(--accent-primary);">Multi-stage Build</b> (Biên dịch nhiều giai đoạn).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Vì Distroless chỉ chứa ứng dụng và thư viện phụ thuộc tối thiểu, loại bỏ hoàn toàn hệ điều hành shell (<code>/bin/sh</code>), trình quản lý gói và công cụ mạng.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Chỉ thị <code>USER 10001</code> (hoặc UID của một user phi root).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Cột <code>FIXED VERSION</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Để tránh việc hacker lợi dụng các công cụ này để tải xuống và biên dịch mã độc hại (malware) trực tiếp trong container.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Lệnh thất bại với lỗi <code>OCI runtime exec failed: exec: "sh": executable file not found in $PATH</code> (vì Distroless không có shell).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Để đảm bảo Docker daemon khởi tạo thư mục làm việc với quyền root trước, tránh lỗi <code>Permission Denied</code> khi user thường không có quyền tạo thư mục.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Cú pháp <code>COPY --chown=10001:10001 --from=builder /app /app</code>.
</div>
</details>

---

## §11. Tài liệu tham khảo

| Nguồn | Địa chỉ URL | Ghi chú |
|---|---|---|
| Trivy Documentation | `https://aquasecurity.github.io/trivy/latest/` | Tài liệu chuẩn công cụ quét Trivy |
| Google Distroless Images | `https://github.com/GoogleContainerTools/distroless` | Tài liệu chuẩn ảnh cơ sở Distroless |


---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên cụm Kubernetes 1.30+ tiêu chuẩn (hoặc cụm kind/kubeadm lab). Hãy đảm bảo ngữ cảnh dòng lệnh `kubectl config current-context` đã trỏ chính xác vào cụm thực hành trước khi thực thi.

## Khối thực hành — 120 phút

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| Mã tiêu chí | Nội dung tiêu chí | Lệnh kiểm chứng | Kết quả kỳ vọng |
|---|---|---|---|
| TH1 | Tạo Namespace `lab48` phục vụ thực hành Container Image Scanning CKS | `kubectl get ns lab48 -o jsonpath='{.status.phase}'` | In ra `Active` |
| TH2 | Cài đặt hoặc xác minh công cụ `trivy` sẵn sàng hoạt động từ CLI | `trivy --version 2>&1 \| grep -q "Version"` | In phiên bản Trivy |
| TH3 | Thực thi quét ảnh `python:3.8-slim` bằng Trivy CLI | `trivy image --severity CRITICAL python:3.8-slim 2>&1 \| grep -q "Total:"` | Trích xuất báo cáo |
| TH4 | Lọc danh sách lỗ hổng `CRITICAL` và lưu vào tệp `/tmp/lab48-cve.txt` | `test -s /tmp/lab48-cve.txt && echo "EXISTS"` | In ra `EXISTS` |
| TH5 | Sử dụng cờ `--ignore-unfixed` lọc các lỗ hổng đã có bản vá | `trivy image --severity CRITICAL --ignore-unfixed python:3.8-slim 2>&1 \| grep -q "Total:"` | Lọc thành công |
| TH6 | Tạo tệp `Dockerfile.vulnerable` chứa nhiều lỗ hổng (dùng ubuntu:18.04, root) | `grep -q "FROM ubuntu:18.04" /tmp/Dockerfile.vulnerable` | Tệp tồn tại |
| TH7 | Build ảnh `vulnerable-app:v1` từ Dockerfile lỗi và thực thi quét | `docker image inspect vulnerable-app:v1 >/dev/null 2>&1 \|\| echo "BUILT"` | Xóa/Build thành công |
| TH8 | Tạo tệp `Dockerfile.hardened` chuẩn CKS (Multi-stage, Distroless, USER 10001) | `grep -q "USER 10001" /tmp/Dockerfile.hardened` | Tệp chứa USER 10001 |
| TH9 | Build ảnh `hardened-app:v1` từ Dockerfile gia cố | `docker image inspect hardened-app:v1 >/dev/null 2>&1 \|\| echo "BUILT"` | Build thành công |
| TH10 | Quét Trivy ảnh `hardened-app:v1` xác nhận 0 lỗ hổng `CRITICAL` | `trivy image --severity CRITICAL hardened-app:v1 2>&1 \| grep -q "Total: 0"` | In `Total: 0` |
| TH11 | Triển khai Pod `hardened-pod` từ ảnh `hardened-app:v1` trong `lab48` | `kubectl get pod hardened-pod -n lab48 -o jsonpath='{.status.phase}'` | In ra `Running` |
| TH12 | Xác minh Pod `hardened-pod` đang chạy dưới ID người dùng `10001` | `kubectl get pod hardened-pod -n lab48 -o jsonpath='{.spec.securityContext.runAsUser}'` | In ra `10001` |
| TH13 | Dọn dẹp sạch sẽ tài nguyên lab48 | `test ! -f /tmp/Dockerfile.vulnerable && echo "CLEAN"` | In ra `CLEAN` |

---

## L1. Điều kiện tiên quyết về môi trường

| Kiểm tra | Lệnh thực hiện | Kết quả kỳ vọng |
|---|---|---|
| Cụm Kubernetes ba node | `kubectl get nodes` | `cp-01`, `worker-01`, `worker-02` ở trạng thái `Ready` |
| Context đúng môi trường lab | `kubectl config current-context` | Đúng context cụm `kubeadm` |
| Công cụ Trivy và Docker/Containerd | `trivy --version` | Trivy CLI sẵn sàng |

---

## L2. Kiến trúc bài lab Image Scanning & Hardening

```mermaid
graph TD
    Vulnerable[Dockerfile.vulnerable: Ubuntu 18.04 + Root] -->|"Build & Scan"| TrivyBad[Trivy Scan: Dính N lỗ hổng CRITICAL]
    TrivyBad -->|"Refactor Dockerfile"| Hardened[Dockerfile.hardened: Multi-stage + Distroless + USER 10001]
    Hardened -->|"Build & Scan"| TrivyGood[Trivy Scan: Total 0 CRITICAL CVEs]
    TrivyGood -->|"Deploy"| PodHardened[Pod hardened-pod in Namespace lab48]
```

---

## L3. Bước 1: Khởi tạo Namespace `lab48` và kiểm tra Trivy CLI (15 phút)

### Thao tác 1.1: Tạo Namespace và xác minh Trivy CLI

```bash
kubectl create namespace lab48

# Cài đặt Trivy nếu chưa có:
which trivy >/dev/null || (curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin)
```

**CHECKPOINT 1 — Kiểm tra Namespace `lab48`.**

```bash
kubectl get ns lab48 -o jsonpath='{.status.phase}' | grep -qx Active && echo "CHECKPOINT 1 — ĐẠT" || echo "CHECKPOINT 1 — LỖI"
```

**CHECKPOINT 2 — Kiểm tra Trivy CLI.**

```bash
trivy --version 2>&1 | grep -q "Version" && echo "CHECKPOINT 2 — ĐẠT" || echo "CHECKPOINT 2 — LỖI"
```

---

## L4. Bước 2: Thực thi quét lỗ hổng ảnh container bằng Trivy CLI (25 phút)

### Thao tác 2.1: Quét ảnh `python:3.8-slim` và lọc lỗ hổng `CRITICAL`

```bash
trivy image --severity CRITICAL python:3.8-slim > /tmp/lab48-cve.txt
```

**CHECKPOINT 3 — Thực thi lệnh `trivy image`.**

```bash
test -f /tmp/lab48-cve.txt && echo "CHECKPOINT 3 — ĐẠT" || echo "CHECKPOINT 3 — LỖI"
```

**CHECKPOINT 4 — Trích xuất tệp kết quả `/tmp/lab48-cve.txt`.**

```bash
test -s /tmp/lab48-cve.txt && echo "CHECKPOINT 4 — ĐẠT" || echo "CHECKPOINT 4 — LỖI"
```

### Thao tác 2.2: Sử dụng cờ `--ignore-unfixed` lọc kết quả đã có bản vá

**CHECKPOINT 5 — Kiểm tra lệnh Trivy có cờ `--ignore-unfixed`.**

```bash
trivy image --severity CRITICAL --ignore-unfixed python:3.8-slim >/dev/null 2>&1 && echo "CHECKPOINT 5 — ĐẠT" || echo "CHECKPOINT 5 — LỖI"
```

---

## L5. Bước 3: Tạo Dockerfile lỗi và thực thi quét phát hiện lỗ hổng (25 phút)

### Thao tác 3.1: Tạo tệp `Dockerfile.vulnerable` không an toàn

```bash
cat <<EOF > /tmp/Dockerfile.vulnerable
FROM ubuntu:18.04
RUN apt-get update && apt-get install -y python3 curl netcat
WORKDIR /app
COPY . .
CMD ["python3", "-m", "http.server", "8080"]
EOF
```

**CHECKPOINT 6 — Kiểm tra tệp `Dockerfile.vulnerable`.**

```bash
grep -q "FROM ubuntu:18.04" /tmp/Dockerfile.vulnerable && echo "CHECKPOINT 6 — ĐẠT" || echo "CHECKPOINT 6 — LỖI"
```

### Thao tác 3.2: Build ảnh `vulnerable-app:v1` (nếu có Docker) hoặc quét trực tiếp

```bash
docker build -t vulnerable-app:v1 -f /tmp/Dockerfile.vulnerable /tmp 2>/dev/null || true
```

**CHECKPOINT 7 — Xác minh build/kiểm tra ảnh `vulnerable-app:v1`.**

```bash
test -f /tmp/Dockerfile.vulnerable && echo "CHECKPOINT 7 — ĐẠT" || echo "CHECKPOINT 7 — LỖI"
```

---

## L6. Bước 4: Biên soạn `Dockerfile.hardened` chuẩn CKS và build ảnh sạch (25 phút)

### Thao tác 4.1: Biên soạn `Dockerfile.hardened` (Multi-stage, Distroless, USER 10001)

```bash
cat <<EOF > /tmp/Dockerfile.hardened
# Stage 1: Build stage
FROM python:3.11-alpine AS builder
WORKDIR /app
RUN pip install --no-cache-dir --user redis

# Stage 2: Runtime stage
FROM gcr.io/distroless/python3-debian11
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
USER 10001
EXPOSE 8080
CMD ["-m", "http.server", "8080"]
EOF
```

**CHECKPOINT 8 — Kiểm tra chỉ thị `USER 10001` trong `Dockerfile.hardened`.**

```bash
grep -q "USER 10001" /tmp/Dockerfile.hardened && echo "CHECKPOINT 8 — ĐẠT" || echo "CHECKPOINT 8 — LỖI"
```

### Thao tác 4.2: Build ảnh `hardened-app:v1`

```bash
docker build -t hardened-app:v1 -f /tmp/Dockerfile.hardened /tmp 2>/dev/null || true
```

**CHECKPOINT 9 — Xác minh tệp `Dockerfile.hardened` sẵn sàng.**

```bash
test -f /tmp/Dockerfile.hardened && echo "CHECKPOINT 9 — ĐẠT" || echo "CHECKPOINT 9 — LỖI"
```

**CHECKPOINT 10 — Xác minh ảnh tối giản chuẩn CKS.**

```bash
grep -q "distroless" /tmp/Dockerfile.hardened && echo "CHECKPOINT 10 — ĐẠT" || echo "CHECKPOINT 10 — LỖI"
```

---

## L7. Bước 5: Triển khai Pod gia cố trong Namespace `lab48` (10 phút)

### Thao tác 5.1: Triển khai Pod `hardened-pod` có `runAsUser: 10001`

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: hardened-pod
  namespace: lab48
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
  containers:
    - name: app
      image: python:3.11-alpine
      command: ["python3", "-m", "http.server", "8080"]
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
      volumeMounts:
        - name: tmp-vol
          mountPath: /tmp
  volumes:
    - name: tmp-vol
      emptyDir: {}
EOF
```

**CHECKPOINT 11 — Kiểm tra Pod `hardened-pod` ở trạng thái `Running`.**

```bash
sleep 4
kubectl get pod hardened-pod -n lab48 -o jsonpath='{.status.phase}' | grep -qx Running && echo "CHECKPOINT 11 — ĐẠT" || echo "CHECKPOINT 11 — LỖI"
```

**CHECKPOINT 12 — Xác minh `runAsUser: 10001` của Pod `hardened-pod`.**

```bash
kubectl get pod hardened-pod -n lab48 -o jsonpath='{.spec.securityContext.runAsUser}' | grep -qx 10001 && echo "CHECKPOINT 12 — ĐẠT" || echo "CHECKPOINT 12 — LỖI"
```

---

## L8. Dọn dẹp môi trường (10 phút)

### Thao tác 8.1: Dọn dẹp tài nguyên lab48

```bash
kubectl delete namespace lab48
rm -f /tmp/Dockerfile.vulnerable /tmp/Dockerfile.hardened /tmp/lab48-cve.txt
```

**CHECKPOINT 13 — Kiểm tra dọn dẹp sạch sẽ.**

```bash
test ! -f /tmp/Dockerfile.vulnerable && echo "CHECKPOINT 13 — ĐẠT" || echo "CHECKPOINT 13 — LỖI"
```

---

## L9. Xử lý sự cố thường gặp trong lab

| Triệu chứng lỗi | Nguyên nhân gốc rễ | Cách sửa triệt để |
|---|---|---|
| 1. Lệnh `trivy` bị kẹt lâu khi tải database | Cơ sở dữ liệu Trivy DB bị nghẽn mạng | Thêm cờ `--download-db-only` hoặc dùng proxy |
| 2. Báo cáo Trivy chứa quá nhiều CVEs phụ | Quên cờ `--severity CRITICAL` và `--ignore-unfixed` | Thêm cờ `--severity CRITICAL --ignore-unfixed` |
| 3. Pod `hardened-pod` kẹt `CreateContainerConfigError` | Bật `readOnlyRootFilesystem: true` nhưng thiếu `emptyDir` mount | Mount `emptyDir` volume vào các thư mục ghi tạm |
| 4. Distroless image bị lỗi `executable not found` | Dùng cú pháp shell form `CMD python server.py` | Đổi sang cú pháp exec form `CMD ["python", "server.py"]` |
| 5. Lỗi `Permission Denied` khi container ghi file | User 10001 không có quyền ghi thư mục WORKDIR | Khai báo `WORKDIR` trước chỉ thị `USER 10001` |
| 6. Script CI/CD không dừng khi có lỗ hổng | Quên cờ `--exit-code 1` trong lệnh trivy | Thêm cờ `--exit-code 1` vào lệnh trivy image |
| 7. Quên loại bỏ cache trình quản lý gói | `apt-get install` để lại cache trong layer ảnh | Thêm `&& rm -rf /var/lib/apt/lists/*` |
| 8. Quét nhầm tag ảnh `latest` cũ | Kết quả không phản ánh đúng phiên bản ảnh build | Chỉ định đúng tag phiên bản cụ thể (như `app:v1`) |
| 9. Gõ sai từ khóa `USER 10001` thành `USER root` | Dockerfile vẫn khởi chạy với quyền root | Đổi chỉ thị thành `USER 10001` |
| 10. `trivy` báo lỗi `Need write permission to /root/.cache` | User chạy lệnh Trivy không có quyền ghi thư mục cache | Chạy lệnh Trivy với cờ `--cache-dir /tmp/trivy` |
| 11. Pod bị chặn do `runAsNonRoot: true` | Container khởi chạy với UID 0 | Thêm chỉ thị `USER 10001` trong Dockerfile |
| 12. Multi-stage build quên copy file từ stage builder | Stage 2 runtime thiếu file thực thi binary | Thêm chỉ thị `COPY --from=builder /app/binary .` |
| 13. Tệp YAML dry-run bị lỗi indentation | Copy/paste thủ công bị dính tab | Sử dụng `vim` thiết lập `:set expandtab tabstop=2 shiftwidth=2` |
| 14. Docker build bị lỗi không tìm thấy file | Quên copy mã nguồn ở chỉ thị `COPY . .` | Đảm bảo context build chứa đầy đủ mã nguồn |

---

## L10. Bài tập mở rộng

- **BT1:** Viết script Bash quét tự động tất cả các ảnh container đang chạy trong cụm và xuất báo cáo HTML.
- **BT2:** Biên soạn Dockerfile gia cố cho ứng dụng NodeJS sử dụng `gcr.io/distroless/nodejs18-debian11`.
- **BT3:** Cấu hình Trivy plugin tích hợp trực tiếp vào VS Code để cảnh báo CVEs khi mở Dockerfile.
- **BT4:** Thử nghiệm sử dụng công cụ `Grype` (của Anchore) và so sánh kết quả quét với Trivy.
- **BT5:** Cấu hình Quay.io Container Registry tự động chặn push ảnh dính lỗ hổng `CRITICAL`.
- **BT6:** Thực hành viết SBOM (Software Bill of Materials) xuất dạng SPDX bằng Trivy (`trivy image --format spdx-json`).

---

## L11. Hiện vật nộp và tiêu chí chấm điểm

| Hạng mục hiện vật | Tiêu chí chấm điểm đạt | Thang điểm |
|---|---|---|
| Nhật ký 13 Checkpoint | Thực thi thành công 100 % các checkpoint in ra `ĐẠT` | 50 điểm |
| Thao tác Trivy Image Scanning | Quét ảnh và xuất báo cáo CVEs lọc --ignore-unfixed | 20 điểm |
| Thao tác Dockerfile Hardening | Biên soạn Dockerfile Multi-stage Distroless USER 10001 | 20 điểm |
| Báo cáo bài tập mở rộng | Trả lời đầy đủ câu hỏi BT1 và BT2 | 10 điểm |
| **Tổng điểm** | | **100 điểm** |


---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu


## V1. Cách tiến hành

Giảng viên hoặc bạn học chọn ngẫu nhiên các câu hỏi trong bộ 12 câu dưới đây. Người trả lời phải trình bày mạch lạc trong 60–90 giây mỗi câu, đi thẳng vào cơ chế kỹ thuật và viện dẫn các lệnh CLI thực tế.

---

---

## V2. Bộ câu hỏi phỏng vấn thực chiến

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q01</span>
    <span>Cú pháp lệnh CLI Trivy chuẩn để quét ảnh <code>nginx:1.19</code> và chỉ hiển thị các lỗ hổng mức <code>CRITICAL</code> đã có bản vá sửa lỗi là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"><code>trivy image --severity CRITICAL --ignore-unfixed nginx:1.19</code>.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Cấu hình sai cú pháp lệnh trivy image.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu đúng severity nhưng quên cờ <code>--ignore-unfixed</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày chính xác 100% cú pháp lệnh Trivy lọc <code>--severity CRITICAL</code> và <code>--ignore-unfixed</code>.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Cờ <code>--ignore-unfixed</code> đóng vai trò gì? — Bỏ qua các lỗ hổng CVEs chưa có bản sửa lỗi từ phía nhà sản xuất OS để tránh làm báo cáo bị nhiễu).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q02</span>
    <span>Cờ thuộc tính nào trong lệnh Trivy giúp tự động trả về lỗi (exit code 1) để đánh sập CI/CD pipeline khi phát hiện lỗ hổng <code>CRITICAL</code>?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Cờ <code>--exit-code 1</code> (ví dụ <code>trivy image --exit-code 1 --severity CRITICAL <image></code>). Nếu phát hiện lỗ hổng mức <code>CRITICAL</code>, Trivy sẽ dừng với exit code 1 làm bước build CI/CD bị thất bại.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết cờ exit-code trong CI/CD.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được sập build nhưng thiếu cờ <code>--exit-code 1</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chuẩn xác vai trò cờ <code>--exit-code 1</code> tự động hóa rào chắn an ninh trong CI/CD pipeline.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Nếu muốn Trivy xuất kết quả định dạng JSON cho script CI/CD trích xuất thì dùng cờ gì? — Thêm cờ <code>--format json</code>).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q03</span>
    <span>Tại sao việc sử dụng ảnh cơ sở Distroless (<code>gcr.io/distroless/*</code>) lại giúp giảm đến 90% số lượng lỗ hổng CVEs so với ảnh cơ sở Ubuntu hay Debian?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Vì ảnh Distroless được thiết kế tối giản tuyệt đối, chỉ chứa duy nhất ứng dụng và các thư viện phụ thuộc của nó; hoàn toàn loại bỏ hệ điều hành shell (<code>/bin/sh</code>), trình quản lý gói (<code>apt</code>/<code>dpkg</code>) và các tiện ích hệ thống thừa, từ đó triệt tiêu hầu hết các lỗ hổng CVEs hệ điều hành.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết đặc điểm ảnh Distroless.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được ảnh nhẹ hơn nhưng chưa làm rõ việc loại bỏ OS shell và utilities.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích thấu đáo lý do Distroless triệt tiêu 90% lỗ hổng CVEs.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Nếu kẻ tấn công chiếm được container chạy Distroless thì chúng có dùng được lệnh <code>sh</code> hay <code>bash</code> không? — Không được, vì Distroless hoàn toàn không chứa file nhị phân <code>sh</code> hay <code>bash</code>).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q04</span>
    <span>Kỹ thuật Multi-stage Build trong Dockerfile hoạt động ra sao và mang lại lợi ích bảo mật gì cho ảnh container?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Multi-stage Build sử dụng nhiều chỉ thị <code>FROM</code> trong cùng một Dockerfile: Stage 1 (Builder) dùng ảnh đầy đủ công cụ để biên dịch mã nguồn; Stage 2 (Runtime) chỉ copy sản phẩm binary đã biên dịch sang một ảnh cơ sở siêu sạch (như Distroless hay Alpine). Lợi ích: Loại bỏ toàn bộ công cụ biên dịch (<code>gcc</code>, <code>make</code>) khỏi ảnh chạy Production.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết Multi-stage build.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được tách 2 stage nhưng chưa rõ lợi ích gỡ bỏ compiler ở runtime.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích thấu đáo cơ chế Multi-stage build và lợi ích bảo mật triệt tiêu bề mặt tấn công.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Cú pháp copy file binary từ stage <code>builder</code> sang stage <code>runtime</code> là gì? — <code>COPY --from=builder /app/myapp /app/myapp</code>).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q05</span>
    <span>Tại sao chỉ thị <code>USER 10001</code> lại là yêu cầu bắt buộc trong tệp Dockerfile chuẩn CKS Hardening?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Mặc định nếu không khai báo <code>USER</code>, container sẽ chạy dưới quyền <code>root</code> (UID 0). Khai báo <code>USER 10001</code> ép buộc container vận hành dưới quyền người dùng phi root thường, ngăn chặn nguy cơ kẻ tấn công thực hiện kỹ thuật thoát rào chắn container (Container Breakout) chiếm quyền root của Host Node.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết tác dụng chỉ thị USER.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được cấm root nhưng chưa rõ nguy cơ Container Breakout chiếm Host Node.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày chuẩn xác vai trò chỉ thị <code>USER 10001</code> triệt tiêu nguy cơ chiếm Host Node.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Tại sao chỉ thị <code>WORKDIR</code> nên được khai báo TRƯỚC chỉ thị <code>USER 10001</code> trong Dockerfile? — Để Docker daemon tạo thư mục WORKDIR với quyền root trước, tránh lỗi Permission Denied cho user thường).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q06</span>
    <span>Cách đối soát kết quả quét lỗ hổng Trivy để tìm đúng phiên bản gói thư viện chứa bản vá để nâng cấp là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Quan sát bảng kết quả Trivy tại hai cột: <code>INSTALLED</code> (phiên bản gói thư viện hiện tại đang dính lỗi) và <code>FIXED VERSION</code> (phiên bản đã được sửa lỗi). Sau đó cập nhật chỉ thị trong Dockerfile hoặc <code>package.json</code> nâng cấp gói thư viện lên phiên bản <code>>= FIXED VERSION</code>.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết cách đọc bảng kết quả Trivy.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được xem phiên bản nhưng chưa rõ 2 cột INSTALLED và FIXED VERSION.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chuẩn xác quy trình đọc cột FIXED VERSION để nâng cấp bản vá.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Nếu cột <code>FIXED VERSION</code> bị bỏ trống thì nghĩa là gì? — Nghĩa là lỗ hổng đó chưa có bản vá chính thức từ nhà sản xuất).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q07</span>
    <span>Cú pháp Dockerfile chuẩn CKS Hardening hoàn chỉnh cho một ứng dụng viết bằng Go/NodeJS gồm các thành phần cốt lõi nào?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">```dockerfile</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"># Stage 1: Build</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">FROM golang:1.21-alpine AS builder</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">WORKDIR /app</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">COPY . .</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">RUN CGO_ENABLED=0 go build -o app .</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"># Stage 2: Runtime</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">FROM gcr.io/distroless/static-debian11</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">WORKDIR /app</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">COPY --chown=10001:10001 --from=builder /app/app .</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">USER 10001</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">CMD ["./app"]</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">```</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Viết Dockerfile 1 stage không có USER hay Distroless.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được Multi-stage nhưng thiếu USER 10001 hoặc COPY --chown.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Viết chuẩn xác 100% bản kê khai Dockerfile CKS Hardening.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Cờ <code>--chown=10001:10001</code> trong chỉ thị COPY đóng vai trò gì? — Gán quyền sở hữu file cho user 10001 để tránh lỗi Permission Denied).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q08</span>
    <span>Khái niệm SBOM (Software Bill of Materials) trong bảo mật chuỗi cung ứng CKS là gì và Trivy hỗ trợ xuất SBOM thế nào?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">SBOM là bản danh mục thống kê toàn bộ các thành phần phần mềm, thư viện và phụ thuộc có trong ảnh container. Trivy hỗ trợ xuất SBOM theo chuẩn quốc tế SPDX/CycloneDX qua lệnh <code>trivy image --format spdx-json <image></code>.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết khái niệm SBOM.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được danh mục thư viện nhưng chưa rõ lệnh Trivy xuất SPDX/CycloneDX.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chuẩn xác khái niệm SBOM và lệnh Trivy xuất SBOM.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Lợi ích của SBOM trong quản lý an ninh doanh nghiệp là gì? — Cho phép nhanh chóng tra cứu xem doanh nghiệp có bị ảnh hưởng khi xuất hiện 1 lỗ hổng CVE mới công bố không).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q09</span>
    <span>Sự khác nhau giữa việc quét ảnh container tĩnh (Static Image Scanning) vs Giám sát thời gian thực (Runtime Security) là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Quét ảnh tĩnh (Trivy, Quay) thực hiện trước khi triển khai (CI/CD) để phát hiện lỗ hổng đính kèm trong file ảnh. Giám sát thời gian thực (Falco, Sysdig) thực hiện khi container ĐANG CHẠY trên cụm để phát hiện các hành vi bất thường (như gọi bash shell, sửa file hệ thống).</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Nhầm lẫn giữa Static Scanning và Runtime Security.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được trước và sau nhưng chưa rõ công cụ Trivy vs Falco.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chuẩn xác ranh giới nhiệm vụ giữa Static Image Scanning vs Runtime Security.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Công cụ nào nổi tiếng nhất trong CKS về giám sát hành vi thời gian thực at Runtime? — Công cụ Falco của Sysdig).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q10</span>
    <span>Tại sao không nên cài đặt trình quản lý gói (<code>apt-get</code>, <code>apk</code>) hoặc công cụ <code>curl</code>/<code>wget</code> trong ảnh container ở môi trường Production?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Vì nếu hacker chiếm được container qua lỗ hổng ứng dụng, chúng sẽ dùng <code>curl</code>/<code>wget</code> để tải mã độc (malware/rootkit) từ bên ngoài về và dùng <code>apt</code>/<code>apk</code> để cài đặt các công cụ tấn công leo thang ngay trên container.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Cho rằng cài curl trong container Production là vô hại.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được hacker tải mã độc nhưng thiếu việc triệt tiêu công cụ tải/biên dịch.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích thấu đáo lý do loại bỏ apt/curl ở môi trường Production.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Nếu ứng dụng bắt buộc phải tải dữ liệu từ ngoài thì làm thế nào mà không cần curl? — Sử dụng trực tiếp thư viện HTTP Client có sẵn trong mã nguồn ngôn ngữ lập trình).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q11</span>
    <span>Bộ 4 quy tắc vàng để gia cố tệp Dockerfile chuẩn CKS Hardening là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Áp dụng Multi-stage Build tách biệt giai đoạn build và runtime.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Dùng ảnh cơ sở tối giản (Distroless hay Alpine) loại bỏ OS shell.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Bắt buộc khai báo <code>USER 10001</code> chạy dưới quyền phi root.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Quét kiểm tra bằng <code>trivy image --severity CRITICAL --ignore-unfixed</code> đảm bảo 0 CVE Critical.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không nêu đủ 4 quy tắc.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được 2 quy tắc.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày tự tin, mạch lạc bộ 4 quy tắc vàng Dockerfile Hardening CKS.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Mục tiêu tiếp theo của bạn trong Buổi 49 là gì? — Học về <code>Sysdig và Falco Phát hiện Đe dọa CKS: Runtime Security & System Call Auditing</code>).

---

## V3. Câu chốt để nói khi phỏng vấn

1. <b style="color: var(--accent-primary);">"Thực thi nguyên tắc Shift-Left Security bằng cách quét lỗ hổng ảnh container qua Trivy CLI ngay trong CI/CD pipeline."</b>
2. <b style="color: var(--accent-primary);">"Sử dụng cờ <code>--exit-code 1 --severity CRITICAL</code> để tự động đánh sập pipeline nếu phát hiện ảnh dính lỗ hổng nguy cấp."</b>
3. <b style="color: var(--accent-primary);">"Gia cố Dockerfile bằng Multi-stage build kết hợp Distroless base image để giảm 90% dung lượng và bề mặt tấn công."</b>
4. <b style="color: var(--accent-primary);">"Luôn khai báo chỉ thị <code>USER 10001</code> ở giai đoạn runtime để đảm bảo container KHÔNG BAO GIỜ chạy dưới quyền root."</b>

---</div>
</div>
</details>

---

## V3. Câu chốt để nói khi phỏng vấn

1. **"Thực thi nguyên tắc Shift-Left Security bằng cách quét lỗ hổng ảnh container qua Trivy CLI ngay trong CI/CD pipeline."**
2. **"Sử dụng cờ `--exit-code 1 --severity CRITICAL` để tự động đánh sập pipeline nếu phát hiện ảnh dính lỗ hổng nguy cấp."**
3. **"Gia cố Dockerfile bằng Multi-stage build kết hợp Distroless base image để giảm 90% dung lượng và bề mặt tấn công."**
4. **"Luôn khai báo chỉ thị `USER 10001` ở giai đoạn runtime để đảm bảo container KHÔNG BAO GIỜ chạy dưới quyền root."**

---

## 4. Đề Thi Thực Hành Bấm Giờ & Thử Thách Tốc Độ (Exam Speed Challenge)

> [!TIP]
> **CHIẾN THUẬT PHÒNG THI THỰC CHIẾN:**
> Đặt đồng hồ bấm giờ đúng thời lượng quy định, đọc kỹ yêu cầu namespace và kiểm tra trạng thái cuối cùng của cụm bằng `kubectl get -o jsonpath` trước khi nộp bài.

## T0. Vì sao có khối này

Khối luyện đề giúp học viên rèn luyện phản xạ gõ lệnh tốc độ cao cho các câu hỏi thuộc miền **`Supply Chain Security` (20 %)** trong kỳ thi CKS. Trọng tâm bài luyện là kỹ năng thực thi quét ảnh bằng Trivy CLI (`--severity CRITICAL`, `--ignore-unfixed`), trích xuất báo cáo CVEs và gia cố tệp Dockerfile chuẩn CKS (Multi-stage build, Distroless, USER 10001) từ terminal CLI. Tổng thời gian làm bài và tự chấm là đúng 30 phút (1.800 giây).

---

## T1. Luật chơi

1. Mở duy nhất 1 cửa sổ Terminal và 1 tab trình duyệt truy cập tài liệu chính thức `https://kubernetes.io/docs/`.
2. Không sử dụng công cụ AI, không copy/paste các mẫu YAML sẵn từ ngoài tài liệu chính thức.
3. Sử dụng tối đa các alias rút gọn (`k` cho `kubectl`).
4. Tổng thời gian thực hiện 4 câu: **21 phút** (1.260 giây). Thời gian tự chấm bằng script: **9 phút** (540 giây).

---

## T2. Bốn câu kiểu đề thi

### Câu T2.1 — CKS · Supply Chain Security — 300 giây
Quét ảnh `nginx:1.18` bằng công cụ Trivy:
- Chỉ trích xuất các lỗ hổng ở mức độ nghiêm trọng `CRITICAL`
- Loại bỏ các lỗ hổng chưa có bản vá bằng cờ `--ignore-unfixed`
- Lưu danh sách kết quả quét vào tệp `/tmp/nginx-cve.txt`

### Câu T2.2 — CKS · Supply Chain Security — 300 giây
Biên soạn tệp Dockerfile gia cố cho ứng dụng Go tại tệp `/tmp/Dockerfile.hardened`:
- Stage 1 (`builder`): dùng ảnh `golang:1.21-alpine`, build binary `/app/myapp`
- Stage 2 (`runtime`): dùng ảnh `gcr.io/distroless/static-debian11`
- Copy binary từ `builder` sang `runtime` và khai báo `USER 10001`

### Câu T2.3 — CKS · Supply Chain Security — 300 giây
Thực thi lệnh Trivy quét ảnh `app:v1` giả lập kiểm tra điều kiện sập build CI/CD:
- Sử dụng cờ `--exit-code 1` và `--severity CRITICAL`
- Nếu phát hiện lỗ hổng `CRITICAL`, lệnh trả về exit code 1
- Lưu câu lệnh CLI chuẩn vào tệp `/tmp/trivy-cicd.sh`

### Câu T2.4 — CKS · Supply Chain Security — 360 giây
Sửa tệp `/tmp/Dockerfile.buggy` bị dính lỗi bảo mật:
- Tệp cũ dùng `FROM ubuntu:16.04` và chạy dưới quyền `root`
- Sửa lại tệp tại `/tmp/Dockerfile.fixed` dùng `FROM alpine:3.18`, cài `python3` loại bỏ cache, khai báo `USER 10001`
- Xác minh ảnh mới không còn chứa lỗ hổng `CRITICAL`

---

## T3. Lời giải chuẩn (Đường gõ ngắn nhất)

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
trivy image --severity CRITICAL --ignore-unfixed nginx:1.18 > /tmp/nginx-cve.txt
```
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
cat <<EOF > /tmp/Dockerfile.hardened
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o myapp .

FROM gcr.io/distroless/static-debian11
WORKDIR /app
COPY --chown=10001:10001 --from=builder /app/myapp .
USER 10001
CMD ["./myapp"]
EOF
```
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
cat <<EOF > /tmp/trivy-cicd.sh
#!/bin/bash
trivy image --exit-code 1 --severity CRITICAL --ignore-unfixed app:v1
EOF

chmod +x /tmp/trivy-cicd.sh
```
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
cat <<EOF > /tmp/Dockerfile.fixed
FROM alpine:3.18
RUN apk add --no-cache python3 && rm -rf /var/cache/apk/*
WORKDIR /app
COPY . .
USER 10001
CMD ["python3", "-m", "http.server", "8080"]
EOF
```

---
</div>
</details>

## T4. Bẫy hay gặp

| Bẫy hay gặp | Mất bao nhiêu điểm | Dấu hiệu nhận ra ngay |
|---|---|---|
| 1. Quên cờ `--ignore-unfixed` khi quét Trivy | Mất 25 điểm (Câu 1) | Kết quả chứa các CVE chưa có bản vá |
| 2. Quên chỉ thị `USER 10001` ở stage runtime | Mất 25 điểm (Câu 2 & 4) | Container khởi chạy dưới quyền root |
| 3. Quên cờ `--exit-code 1` trong script CI/CD | Mất 25 điểm (Câu 3) | Lệnh Trivy không trả về exit code 1 khi dính lỗi |
| 4. Để lại cache package manager trong `RUN` | Mất 25 điểm (Câu 4) | Tệp Dockerfile không có `--no-cache` |
| 5. Quên cờ `--from=builder` khi COPY ở stage 2 | Mất 25 điểm (Câu 2) | Image runtime bị thiếu file nhị phân binary |

---

## T5. Bảng tự chấm và Script chấm điểm tự động

### Đoạn script tự kiểm tra và in điểm (Không phụ thuộc vào `jq`)

```bash
#!/bin/bash
SCORE=0

echo "=== KẾT QUẢ TỰ CHẤM BÀI Ô THI BUỔI 48 ==="

# Kiểm câu 1
if [ -s /tmp/nginx-cve.txt ]; then
    echo "Câu 1: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 1: THẤT BẠI (0đ)"
fi

# Kiểm câu 2
DISTRO_CHECK=$(grep "distroless" /tmp/Dockerfile.hardened 2>/dev/null)
USER_CHECK=$(grep "USER 10001" /tmp/Dockerfile.hardened 2>/dev/null)
if [ -n "$DISTRO_CHECK" ] && [ -n "$USER_CHECK" ]; then
    echo "Câu 2: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 2: THẤT BẠI (0đ)"
fi

# Kiểm câu 3
EXIT_CHECK=$(grep "exit-code 1" /tmp/trivy-cicd.sh 2>/dev/null)
if [ -n "$EXIT_CHECK" ]; then
    echo "Câu 3: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 3: THẤT BẠI (0đ)"
fi

# Kiểm câu 4
ALPINE_CHECK=$(grep "alpine" /tmp/Dockerfile.fixed 2>/dev/null)
FIXED_USER=$(grep "USER 10001" /tmp/Dockerfile.fixed 2>/dev/null)
if [ -n "$ALPINE_CHECK" ] && [ -n "$FIXED_USER" ]; then
    echo "Câu 4: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 4: THẤT BẠI (0đ)"
fi

echo "=========================================="
echo "TỔNG ĐIỂM: $SCORE / 100"
if [ $SCORE -ge 75 ]; then
    echo "ĐÁNH GIÁ: ĐẠT NGƯỠNG AN TOÀN KỲ THI CKS"
else
    echo "ĐÁNH GIÁ: CHƯA ĐẠT - CẦN LUYỆN LẠI"
fi
```

---

## T6. Kho lệnh rút gọn của buổi

```bash
# Trivy Scanning Filtered
trivy image --severity CRITICAL,HIGH --ignore-unfixed <image>

# Trivy CI/CD Fail Gate
trivy image --exit-code 1 --severity CRITICAL <image>

# Dockerfile Hardening Snippet
FROM gcr.io/distroless/static-debian11
WORKDIR /app
COPY --chown=10001:10001 --from=builder /app/binary .
USER 10001
CMD ["./binary"]
```


---

## Tổng Kết & Lộ Trình Bài Học Tiếp Theo

Kiến thức và kỹ năng thực hành trong bài viết này là mắt xích quan trọng trong hệ thống quản trị và bảo mật Kubernetes chuyên nghiệp. Việc nắm vững cả lý thuyết kiến trúc lẫn thao tác gõ lệnh tốc độ cao trong terminal sẽ giúp bạn tự tin xử lý sự cố thực tế cũng như vượt qua các kỳ thi chứng chỉ quốc tế CKA, CKAD và CKS.

> [!TIP]
> **BÀI TIẾP THEO TRONG CHUỖI BÀI HỌC:**
> Tiếp tục hành trình nâng cao năng lực Kubernetes với bài học tiếp theo: [[Bài 04] Giám Sát & Phát Hiện Mối Đe Dọa Thời Gian Chạy: Sysdig, Falco Engine & System Call Auditing](cks-04-04-sysdig-falco-phat-hien-de-doa.html).

{% endraw %}
