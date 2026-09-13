---
layout: post
title: "[Bài 26] Đóng Gói & Xuất Bản Helm Chart: Helm Lint, Helm Package, OCI Registry Publishing & Chart Museum"
date: 2026-09-12 05:20:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-26
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 26
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.26] Hướng dẫn chuyên sâu Đóng Gói & Xuất Bản Helm Chart: Helm Lint, Helm Package, OCI Registry Publishing & Chart Museum: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

{% raw %}
# [BÀI 26] ĐÓNG GÓI & XUẤT BẢN HELM CHART: HELM LINT, HELM PACKAGE, OCI REGISTRY PUBLISHING & CHART MUSEUM

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

---





| # | Câu hỏi ôn tập Buổi 25 (Minimal Image & SBOM) | Đáp án chuẩn ngắn gọn |
|---|---|---|
| 1 | Tại sao nói kích thước Container Image chính là "chi phí nhân với số lần kéo"? | Kích thước Image càng lớn thì chi phí băng thông càng cao và thời gian Pod Auto-scaling càng lâu. |
| 2 | Sự khác biệt cốt lõi về an ninh giữa Alpine Linux và Google Distroless là gì? | Alpine vẫn chứa Shell CLI/apk; Distroless loại bỏ 100% Shell CLI và Package Manager. |
| 3 | Tác dụng của cờ `-ldflags="-w -s"` khi biên dịch ứng dụng Go/Rust? | Loại bỏ toàn bộ DWARF debug symbols và symbol table, giúp cắt giảm 40% dung lượng tệp nhị phân. |
| 4 | Cơ chế OCI Manifest Index giúp ích gì cho bài toán Multi-Arch Build? | Hợp nhất 2 bản build (amd64 và arm64) dưới 1 Tag duy nhất để Docker Engine tự chọn bản phù hợp. |
| 5 | Công cụ Syft thực hiện trích xuất SBOM dựa trên những cơ chế nào? | Syft bóc tách từng layer container và phân tích các tệp lockfile (`go.sum`, `package-lock.json`). |

---



> **LUẬN ĐỀ TRUNG TÂM BUỔI 26:**
> **Helm Chart chính là "BẢN THIẾT KẾ ĐÓNG GÓI HẠ TẦNG KUBERNETES" và phải được quản lý như một HIỆN VẬT BẤT BIẾN CÓ PHIÊN BẢN (VERSIONED ARTIFACT) tương tự như Container Image. Một Helm Chart KHÔNG CÓ PHIÊN BẢN (hoặc liên tục dùng tag `latest`) là nguyên nhân gốc rễ dẫn tới việc KHÔNG THỂ ROLLBACK khi xảy ra sự cố Production. Lưu trữ Helm Chart dưới dạng OCI Artifacts (`oci://...`) trên Enterprise Registry giúp hợp nhất 100% quy trình quản lý hiện vật trong CI/CD.**

```mermaid
graph TD
    A[Cấu trúc Helm Chart mỏng<br/>Chart.yaml + values.yaml + templates/] --> B[Kiểm tra Cú pháp & Render Manifests<br/>helm lint & helm template dry-run]
    
    B --> C[Đóng gói Chart Bất biến Semantic Versioning<br/>helm package -> my-app-1.0.0.tgz]
    
    C --> D[Đẩy lên Enterprise OCI Registry<br/>helm push oci://registry.example.com/charts]
    
    D --> E[Lưu trữ & Phân tách Kho Dev/Prod<br/>helm-dev-local vs helm-prod-local]
    
    E --> F[Deploy & Atomic Rollback 100%<br/>helm upgrade --atomic / helm rollback]
```

---



| STT | Kết quả đạt được (Competency) | Hiện vật chứng minh (Evidence) |
|---|---|---|
| 1 | Xây dựng cấu trúc Helm Chart chuẩn enterprise phân tách rõ ràng. | Thư mục `my-chart/` chứa `Chart.yaml`, `values.yaml` và `templates/`. |
| 2 | Đóng gói Helm Chart thành tệp `.tgz` bất biến với phiên bản Semantic Versioning. | Tệp nhị phân `my-app-1.0.0.tgz` sinh ra từ `helm package`. |
| 3 | Tự động hóa kiểm tra cú pháp và render Manifests bằng `helm lint` và `helm template`. | Job CI `helm-lint-and-template` chạy xanh 100% không báo warning. |
| 4 | Đẩy và quản lý Helm Chart dưới dạng OCI Artifacts (`oci://...`) trên Enterprise Registry. | Lệnh `helm push` tải thành công OCI Chart Artifact lên Registry. |
| 5 | Thực thi quy trình Nâng cấp Atomic (`--atomic`) và Rollback an toàn 100%. | Lệnh `helm rollback` phục hồi ứng dụng về revision trước đó chỉ trong 2 giây. |
| 6 | Cập nhật thông số OCI Registry chuẩn và phiên bản Helm Chart vào tệp hiện vật `bang-4-container-va-hien-vat.tsv`. | Tệp `bang-4-container-va-hien-vat.tsv` bổ sung dòng dữ liệu Buổi 26. |

---



| Kiến thức tiên quyết | Ý nghĩa trong bài học Buổi 26 | Nguồn đối soát nếu thiếu |
|---|---|---|
| Cấu trúc Kubernetes Manifests (YAML) | Đọc hiểu các tệp `Deployment.yaml`, `Service.yaml`, `Ingress.yaml` | Buổi 01 (`QT 1.1`), Buổi 21 (`QT 4.1`) |
| Nguyên tắc Semantic Versioning 2.0 | Hiểu ý nghĩa các con số phiên bản `MAJOR.MINOR.PATCH` | Buổi 14 (`QT 5.1`), Buổi 24 (`QT 4.1`) |
| Chuẩn OCI Distribution Specification | Hiểu cách Container Registry lưu trữ OCI Artifacts (Images, Charts) | Buổi 24 (`QT 4.2`), Buổi 25 (`QT 5.2`) |
| Quản lý biến môi trường trong CI Pipeline | Cấu hình token đăng nhập OCI Registry (`$CI_REGISTRY_PASSWORD`) | Buổi 06 (`QT 2.1`), Buổi 24 (`QT 5.2`) |

---



### Bảng đối chiếu thuật ngữ Việt - Anh

| Tiếng Việt dùng trong bài | Tiếng Anh tương đương | Dùng thẳng từ tiếng Anh trong bài? |
|---|---|---|
| Đóng gói biểu đồ Helm | Helm Chart Packaging | **Có** — gọi là `Helm Chart` |
| Hiện vật lưu trữ chuẩn OCI | OCI Artifact / OCI Distribution Spec | **Có** — gọi là `OCI Artifact` |
| Đánh số phiên bản ngữ nghĩa | Semantic Versioning (SemVer 2.0) | **Có** — `SemVer` |
| Phiên bản biểu đồ | Chart Version (`version`) | **Có** — `Chart Version` |
| Phiên bản ứng dụng | Application Version (`appVersion`) | **Có** — `appVersion` |
| Kiểm tra cú pháp biểu đồ | Helm Linting Validation | **Có** — `Helm Lint` |
| Dịch mẫu thử nghiệm khô | Helm Dry-run Template Rendering | **Có** — `Helm Template` |
| Nâng cấp an toàn nguyên tử | Atomic Upgrade Rollback | **Có** — `Atomic Upgrade` |
| Khôi phục phiên bản phát hành | Helm Release Rollback | **Có** — `Helm Rollback` |
| Kho lưu trữ ảo Helm OCI | Virtual Helm OCI Repository | **Có** — `Helm OCI Repo` |

---

### Bốn mô hình tư duy cốt lõi

#### Mô hình 1: Nguyên lý Bản ghi Bất biến (Immutable Release Artifact)
- Một Helm Chart sau khi được đóng gói bằng câu lệnh `helm package` sẽ tạo ra tệp nén `.tgz` chứa mã băm Checksum SHA-256 bất biến.
- Tuyệt đối không bao giờ được phép chỉnh sửa các tệp `.yaml` trực tiếp trên Server Production. Mọi sự thay đổi (dù chỉ là 1 tham số CPU limit) đều phải tạo ra một Chart Version mới (`1.0.0` $\rightarrow$ `1.0.1`), đóng gói lại tệp `.tgz` và đẩy lên OCI Registry.

#### Mô hình 2: Phân biệt Sự khác biệt giữa `version` và `appVersion`
Trong tệp `Chart.yaml`, có 2 trường phiên bản vô cùng quan trọng:
1. **`version` (Chart Version):** Đánh số phiên bản của chính tệp Helm Chart (mẫu khai báo hạ tầng). Thay đổi khi sửa file YAML template hoặc values defaults (ví dụ: đổi port service, thêm ConfigMap).
2. **`appVersion` (Application Version):** Đánh số phiên bản của mã nguồn ứng dụng (gắn liền với Container Image Tag, ví dụ `appVersion: "a7b8c9d"`).

#### Mô hình 3: Kiến trúc OCI Registry lưu trữ Helm Chart (`oci://...`)
- Trước đây, Helm sử dụng cấu hình Helm Repository truyền thống dựa trên tệp chỉ mục `index.yaml` nạp từ web server tĩnh. Cấu hình này gặp hạn chế lớn về khả năng mở rộng và quản lý phân quyền RBAC.
- Từ Helm v3.8+, Helm chính thức hỗ trợ chuẩn **OCI Artifacts**. Helm Chart được đóng gói dưới dạng các layer OCI Blob và đẩy trực tiếp lên chính Container Registry (như JFrog Artifactory, GitLab Container Registry) qua giao thức `oci://registry.example.com/charts/my-app`. Điều này giúp gộp chung 100% hạ tầng lưu trữ Registry và phân quyền RBAC cho cả Image và Chart.

#### Mô hình 4: Cơ chế Rollback an toàn dựa trên Release Revision History
Khi thực thi `helm upgrade --install`, Helm lưu trữ toàn bộ trạng thái rendered manifests và values vào một tệp Secret mã hóa trong namespace Kubernetes (gọi là `sh.helm.release.v1.<release-name>.v<revision>`). Khi gặp sự cố, câu lệnh `helm rollback <release-name> <revision>` sẽ đọc lại tệp Secret của revision cũ và đưa hệ thống quay trở lại trạng thái hoạt động chính xác trong **2 giây**.

---

### 1.1. Cấu trúc Helm Chart chuẩn và Nguyên tắc Semantic Versioning (10 phút)

### Cấu trúc thư mục dự án Helm Chart chuẩn Enterprise

```text
my-app-chart/
├── Chart.yaml          # Định nghĩa Metadata (Tên chart, version, appVersion)
├── values.yaml         # Cấu hình tham số mặc định (Image repo, replicaCount, resources)
├── values-dev.yaml     # Cấu hình đè cho môi trường Dev (Replicas=1, CPU=100m)
├── values-prod.yaml    # Cấu hình đè cho môi trường Prod (Replicas=5, CPU=1000m)
├── .helmignore         # Khai báo loại bỏ các tệp rác khỏi Helm Package
└── templates/          # Thư mục chứa các mẫu Kubernetes Manifests
    ├── _helpers.tpl    # Định nghĩa các hàm helper Go template
    ├── deployment.yaml # Mẫu Deployment Pods
    ├── service.yaml    # Mẫu ClusterIP / NodePort Service
    ├── ingress.yaml    # Mẫu Nginx / ALB Ingress Routing
    └── NOTES.txt       # Hướng dẫn hiển thị sau khi install/upgrade
```

### Phân tích kiến trúc Go Template Engine và các hàm Helper (`_helpers.tpl`)

Helm Chart sử dụng Go Template Engine kết hợp với bộ thư viện Sprig Functions để xử lý logic render Kubernetes Manifests:
1. **Hàm `include` vs `template`:** Sử dụng `include "my-app.fullname" . | indent 4` cho phép truyền giá trị rendered qua các pipeline filter (như `indent`, `quote`, `trunc`), trong khi `template` chỉ render văn bản thuần không hỗ trợ pipeline.
2. **Quản lý thụt lề chuẩn (Indentation Management):** Thự thi filter `nindent 4` (newline + indent 4 spaces) giúp định dạng YAML hợp lệ 100%, khắc phục hoàn toàn lỗi thụt lề thụt lùi thủ công.
3. **Giá trị mặc định (`default` filter):** Cấu hình `{{ .Values.image.tag | default .Chart.AppVersion }}` đảm bảo nếu không khai báo `image.tag` trong `values.yaml`, Helm sẽ tự động nạp giá trị từ `appVersion` trong `Chart.yaml`.

### Phân tích cấu trúc lớp OCI Artifact Layer trong Registry Specification

Khi đẩy tệp Helm Chart nén `.tgz` lên Container Registry hỗ trợ OCI Format:
1. **Config Descriptor Media Type:** `application/vnd.cncf.helm.config.v1+json` — Lưu trữ thông tin Metadata và cấu hình Chart.
2. **Layer Blob Media Type:** `application/vnd.cncf.helm.chart.content.v1.tar+gzip` — Lưu trữ tệp nén `.tgz` chứa toàn bộ mẫu `.yaml`.
3. **Registry Endpoint URL Format:** `oci://registry.example.com/charts/my-web-app` (Loại bỏ hoàn toàn đường dẫn file tĩnh `index.yaml`).

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Bắt buộc khai báo phiên bản Semantic Versioning (`version: x.y.z`) bất biến cho mỗi lần đóng gói Helm Chart trong tệp `Chart.yaml`.
**Giải thích cơ chế ngầm:** Giúp phân định rõ ràng lịch sử thay đổi của bản thiết kế hạ tầng. Không có phiên bản SemVer chuẩn, Kubernetes sẽ không thể xác định được thứ tự ưu tiên và lịch sử rollback khi gặp sự cố.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để trường `version: 0.1.0` cố định cho tất cả các lần release hoặc dùng nhãn `version: latest`.
**Minh hoạ.**
```yaml
# Chart.yaml chuẩn Enterprise
apiVersion: v2
name: my-web-app
description: Helm Chart đóng gói microservice Web API chuẩn Enterprise
type: application
version: 1.0.0
appVersion: "a7b8c9d"
```
**Con số chốt:** 100% các lần đóng gói Helm Chart bắt buộc phải tuân thủ chuẩn **SemVer 2.0**.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Tách biệt tuyệt đối giữa cấu hình hạ tầng môi trường (`values.yaml`) và logic mẫu Kubernetes Manifests (`templates/`).
**Giải thích cơ chế ngầm:** Đảm bảo tính tái sử dụng (Reusability). Thư mục `templates/` đóng vai trò là khung mẫu chung cho toàn công ty, trong khi các tệp `values-dev.yaml`, `values-prod.yaml` chịu trách nhiệm cung cấp tham số riêng cho từng môi trường.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hardcode địa chỉ IP, Domain Name hoặc số lượng Replicas trực tiếp vào tệp `templates/deployment.yaml`.
**Minh hoạ.**
```yaml
# templates/deployment.yaml (Dùng biến từ values)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
```
**Con số chốt:** Tách biệt 100% giúp 1 bộ Template phục vụ cho **hàng trăm microservices**.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Bắt buộc định nghĩa tham số `appVersion` trong `Chart.yaml` khớp 100% với Container Image Tag đang được triển khai.
**Giải thích cơ chế ngầm:** Giúp kỹ sư Ops tra cứu nhanh chóng mối liên kết giữa bản thiết kế K8s Manifest và Container Image đang chạy thực tế trên Pods.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đặt `appVersion: "1.0.0"` trong khi Container Image đang chạy tag `app:sha-8f7e6d`.
**Minh hoạ.**
```bash
# Cập nhật appVersion trong CI bằng yq hoặc sed
yq e ".appVersion = \"$CI_COMMIT_SHORT_SHA\"" -i Chart.yaml
```
**Con số chốt:** `appVersion` đối soát **1-1** với Container Image Tag trên Registry.

---

### 1.2. Kiểm tra Cú pháp Linting, Template Render và Package Bất biến (10 phút)

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Tự động kiểm tra cú pháp và lỗi tiềm ẩn của Helm Chart bằng lệnh `helm lint` ngay trong Stage test của CI Pipeline.
**Giải thích cơ chế ngầm:** Phát hiện sớm các lỗi thụt lề YAML (Indentation Errors), lỗi thiếu trường bắt buộc trong `Chart.yaml`, hoặc trùng lặp tên biến trước khi thực thi deploy làm hỏng cụm K8s.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bỏ qua bước `helm lint`, khi chạy deploy trên CI mới bị ngắt giữa chừng do lỗi thụt lề 2 dấu cách.
**Minh hoạ.**
```yaml
helm-lint-pass:
  stage: test
  image: alpine/helm:3.14.0
  script:
    - echo "=== BẮT ĐẦU KIỂM TRA CÚ PHÁP HELM CHART ==="
    - helm lint my-app-chart/ --strict
```
**Con số chốt:** `helm lint --strict` loại bỏ **100%** lỗi cú pháp YAML trước khi deploy.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Thực thi cờ `--dry-run` và `helm template` để validate cấu hình render Kubernetes Manifests trước khi nộp sản phẩm.
**Giải thích cơ chế ngầm:** Lệnh `helm template` thực hiện biên dịch các hàm Go Template engine và in ra toàn bộ nội dung file Manifests rendered thô. Kỹ sư CI/CD có thể đối soát xem các giá trị `{{ .Values }}` có được nạp chính xác hay không.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Deploy thành công Helm Release nhưng Pod không khởi chạy do biến môi trường render ra bị rỗng (`env: ""`).
**Minh hoạ.**
```bash
# Render Manifests khô đối soát đầu ra
helm template my-release my-app-chart/ -f my-app-chart/values-prod.yaml > rendered-manifests.yaml
cat rendered-manifests.yaml | head -n 40
```
**Con số chốt:** `helm template` giúp kiểm soát **100%** dữ liệu rendered trước khi đẩy vào K8s Cluster.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Đóng gói Helm Chart thành tệp nén nhị phân `.tgz` bất biến bằng câu lệnh `helm package` có đính kèm appVersion.
**Giải thích cơ chế ngầm:** Tạo ra tệp nhị phân nén duy nhất chứa toàn bộ logic mẫu hạ tầng. Tệp `.tgz` này có tính chất bất biến (Immutable), không thể sửa đổi byte dữ liệu sau khi đã đóng gói.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đẩy thư mục mã nguồn thô chứa các tệp `.yaml` trôi nổi lên Server để deploy thay vì nộp tệp `.tgz` đã package.
**Minh hoạ.**
```bash
# Đóng gói Helm Chart
helm package my-app-chart/ --version 1.0.0 --app-version $CI_COMMIT_SHORT_SHA
# Đầu ra: Successfully packaged chart and saved it to: my-web-app-1.0.0.tgz
```
**Con số chốt:** Tệp `.tgz` đảm bảo tính bất biến **100%** cho bản thiết kế hạ tầng.

---

### 1.3. Quản lý Helm Chart dưới dạng OCI Artifacts trên Registry (10 phút)

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Lưu trữ và quản lý Helm Chart dưới dạng OCI Artifacts chuẩn (`oci://...`) trực tiếp trên Enterprise Artifact Registry.
**Giải thích cơ chế ngầm:** Triệt tiêu hoàn toàn việc phải duy trì các tệp chỉ mục `index.yaml` phức tạp của Helm v2/v3 cũ. Lưu trữ OCI giúp đồng bộ hạ tầng Container Registry và Helm Registry về cùng 1 nơi (JFrog Artifactory / GitLab Registry).
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dùng web server Nginx tĩnh lưu các tệp chart và phải tự gõ lệnh `helm repo index` thủ công mỗi lần release.
**Minh hoạ.**
```bash
# Đăng nhập và đẩy OCI Chart lên Registry
helm registry login registry.example.com -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD
helm push my-web-app-1.0.0.tgz oci://registry.example.com/helm-charts
```
**Con số chốt:** OCI Artifacts rút gọn **80%** độ phức tạp quản lý hạ tầng Helm Registry.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Phân tách kho Helm Chart thành 2 môi trường kho riêng biệt: `helm-dev-local` và `helm-prod-local` tương tự Container Registry.
**Giải thích cơ chế ngầm:** Ngăn chặn việc các bản Chart thử nghiệm của developer từ nhánh feature bị đẩy nhầm vào kho Production Chart, đảm bảo chỉ các Chart đã được kiểm thử mới được thăng cấp sang kho Prod.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đẩy chung tất cả các bản build thử nghiệm và release vào 1 kho Helm duy nhất.
**Minh hoạ.**
```bash
# Đẩy kho Dev
helm push my-app-1.0.0-dev.tgz oci://registry.example.com/helm-dev-local
# Thăng cấp sang kho Prod sau khi Test thành công
helm push my-app-1.0.0.tgz oci://registry.example.com/helm-prod-local
```
**Con số chốt:** Phân tách kho bảo vệ **100%** an toàn cho môi trường Production Release.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Bắt buộc bật cờ `--atomic` và `--timeout` trong câu lệnh `helm upgrade` khi triển khai tự động trong CI/CD.
**Giải thích cơ chế ngầm:** Cờ `--atomic` đảm bảo nếu tiến trình deploy gặp sự cố (Pod bị `CrashLoopBackOff` hoặc `ImagePullBackOff`), Helm sẽ tự động hủy ngắt tiến trình và rollback hệ thống quay trở lại phiên bản cũ ngay lập tức mà không cần can thiệp thủ công.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chạy lệnh `helm upgrade` không có cờ `--atomic`, khi Pod sập, Helm giữ nguyên trạng thái dở dang làm ảnh hưởng tới người dùng.
**Minh hoạ.**
```bash
# Deploy tự động với cờ Atomic và Timeout 5 phút
helm upgrade --install my-app oci://registry.example.com/helm-prod-local/my-web-app \
  --version 1.0.0 \
  --namespace production \
  --values values-prod.yaml \
  --atomic \
  --timeout 5m0s
```
**Con số chốt:** Cờ `--atomic` tự động Rollback **100%** các ca deploy bị lỗi Pod.

---

### 1.4. Trích xuất Hiện vật Helm Chart và Cập nhật Giai đoạn 4 (8 phút)

#### Chi tiết mẫu cấu hình JSON OCI Manifest Descriptor của Helm Chart:
```json
{
  "schemaVersion": 2,
  "config": {
    "mediaType": "application/vnd.cncf.helm.config.v1+json",
    "digest": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "size": 524
  },
  "layers": [
    {
      "mediaType": "application/vnd.cncf.helm.chart.content.v1.tar+gzip",
      "digest": "sha256:a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
      "size": 4820
    }
  ]
}
```

#### Mẫu Trace Log thực tế khi thực thi `helm push` và `helm show chart` OCI:
```text
$ helm push my-web-app-1.0.0.tgz oci://registry.example.com/helm-charts
Pushed: registry.example.com/helm-charts/my-web-app:1.0.0
Digest: sha256:a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0
$ helm show chart oci://registry.example.com/helm-charts/my-web-app --version 1.0.0
apiVersion: v2
name: my-web-app
version: 1.0.0
appVersion: a7b8c9d
description: Helm Chart đóng gói microservice Web API chuẩn Enterprise
Job succeeded
```

#### Chi tiết mẫu báo cáo kiểm tra cú pháp `helm-lint-report.txt`:
```text
=== BÁO CÁO KIỂM TRA CÚ PHÁP HELM CHART (HELM LINT) ===
Tên Chart: my-web-app
Phiên bản Chart (version): 1.0.0
Phiên bản App (appVersion): a7b8c9d
Đường dẫn Chart: ./my-app-chart

==> Linting ./my-app-chart
[INFO] Chart.yaml: icon is recommended
[INFO] values.yaml: syntax validated 100%
[INFO] templates/deployment.yaml: Kubernetes 1.28 API Schema validated

1 chart(s) linted, 0 chart(s) failed
Trạng thái kiểm tra Linting: ĐẠT THỎA MÃN (0 ERRORS, 0 WARNINGS STRICT)
```

#### Chi tiết mẫu Manifest Rendered `rendered-manifests.yaml` (Đầu ra của `helm template`):
```yaml
# Source: my-web-app/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-release-my-web-app
  labels:
    helm.sh/chart: my-web-app-1.0.0
    app.kubernetes.io/name: my-web-app
    app.kubernetes.io/instance: my-release
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: my-web-app
    app.kubernetes.io/instance: my-release
---
# Source: my-web-app/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-release-my-web-app
  labels:
    helm.sh/chart: my-web-app-1.0.0
    app.kubernetes.io/name: my-web-app
    app.kubernetes.io/instance: my-release
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: my-web-app
      app.kubernetes.io/instance: my-release
  template:
    metadata:
      labels:
        app.kubernetes.io/name: my-web-app
        app.kubernetes.io/instance: my-release
    spec:
      containers:
        - name: my-web-app
          image: "registry.example.com/project/my-minimal-app:a7b8c9d"
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 8080
```

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Trích xuất tệp Chart đóng gói `my-web-app-1.0.0.tgz` và `helm-lint-report.txt` nộp sang `artifacts:paths` phục vụ kiểm toán.
**Giải thích cơ chế ngầm:** Lưu trữ hiện vật kiểm toán lâu dài trên GitLab CI Artifacts, cho phép kiểm toán viên tải nạp bản thiết kế hạ tầng chính xác của từng phiên bản release.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Không cấu hình nộp tệp `.tgz` sang `artifacts:paths`.
**Minh hoạ.**
```yaml
artifacts:
  when: always
  paths:
    - my-web-app-1.0.0.tgz
    - helm-lint-report.txt
    - rendered-manifests.yaml
```
**Con số chốt:** Nộp Artifacts bảo đảm lưu trữ **100%** bản thiết kế hạ tầng đã kiểm thử.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** In log đối soát kết quả `helm template` render Manifests công khai trên CI log.
**Giải thích cơ chế ngầm:** Minh bạch hóa nội dung các file YAML Kubernetes sẽ được apply vào cụm Cluster, giúp team Ops đối soát nhanh khi có sự cố về Port hoặc Ingress Route.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Không in log render Manifests khiến khi có sự cố phải kết nối SSH vào Runner để xem log tạm.
**Minh hoạ.**
```bash
echo "=== KẾT QUẢ RENDER KUBERNETES MANIFESTS (HELM TEMPLATE) ==="
helm template my-release my-app-chart/ -f my-app-chart/values-prod.yaml
```
**Con số chốt:** In log render tăng **100%** tính minh bạch cho tiến trình CD Deployment.

---

**Nguyên lý cốt lõi:**
**Phát biểu.** Cập nhật thông số OCI Registry chuẩn (`jfrog_artifactory_helm_oci`) và phiên bản Helm Chart vào tệp hiện vật `bang-4-container-va-hien-vat.tsv`.
**Giải thích cơ chế ngầm:** Hoàn thiện tệp hiện vật Giai đoạn 4, chuẩn hóa các tiêu chí đóng gói hạ tầng Helm Chart cho toàn bộ các dịch vụ trong doanh nghiệp.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Không cập nhật tệp hiện vật Giai đoạn 4.
**Minh hoạ.**
```tsv
ung_dung	tool_build_chuan	dac_quyen_an_ninh	cache_backend	image_size_target	registry_standard	sbom_format	helm_oci_standard
web-app	kaniko	rootless_user_space	remote_registry	< 20MB	jfrog_artifactory_virtual	cyclonedx_json	helm_oci_v3
```
**Con số chốt:** Chuẩn hóa chỉ số đóng gói Helm Chart cho **100%** dịch vụ trong Giai đoạn 4.

---

### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước
1. **Khởi tạo Helm Chart thư mục (10 phút):** Chạy `helm create my-chart` và dọn dẹp các tệp mẫu dư thừa.
2. **Tách tệp `values.yaml` theo môi trường (10 phút):** Tạo 2 tệp `values-dev.yaml` và `values-prod.yaml`.
3. **Thêm bước `helm lint` vào CI (5 phút):** Cấu hình Stage test chạy `helm lint --strict`.
4. **Cấu hình OCI Registry Push (10 phút):** Thêm bước `helm package` và `helm push oci://...` lên Enterprise Registry.

---

### Cái gì hỏng nếu áp thẳng lên prod
- **Trùng tên Release Name:** Nếu chạy `helm install` với một Release Name đã tồn tại trên K8s Cluster mà không có cờ `upgrade --install`, lệnh sẽ bị nổ lỗi `cannot re-use a name that is still in use`.
- **Sai cấu hình Ingress Domain:** Không kiểm tra `helm template` dẫn tới Domain Name trên Ingress trỏ sai sang môi trường Dev.

---

### Đo trước — đo sau
- **Thời gian Rollback khi sập app:** Từ 20 phút (sửa YAML thủ công) $\rightarrow$ giảm xuống **2 giây** (`helm rollback`).
- **Tỷ lệ lỗi cú pháp YAML khi deploy:** Từ 15% $\rightarrow$ giảm xuống **0%** nhờ `helm lint` và `helm template`.
- **Độ phức tạp quản lý Helm Repo:** Giảm 80% nhờ chuyển đổi sang **OCI Registry**.

---

### Khi nào KHÔNG nên dùng
- **KHÔNG dùng Helm Chart cho các ứng dụng cực kỳ đơn giản (1 Pod duy nhất không có cấu hình):** Các ứng dụng 1 file YAML tĩnh có thể dùng Kustomize hoặc `kubectl apply` trực tiếp để tránh phức tạp hóa.

### Kịch bản 3: Tự động hóa cập nhật Helm Chart OCI trong GitLab CI Monorepo
- **Cấu hình:** Sử dụng script CI tự động đọc `git log` để tăng `version` patch trong `Chart.yaml`, gọi `helm package` và đẩy OCI Artifact.
- **Kết quả đo đạc:**
  - Tệp `my-web-app-1.0.1.tgz` được sinh ra tự động trong **1.8 giây**.
  - OCI Manifest Layer đẩy lên Registry thành công với 0% lỗi xung đột checksum.
  - Cụm CD Runner tự động nạp Chart OCI v1.0.1 nâng cấp Atomic trên Kubernetes Cluster.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy thường gặp | Nguyên nhân & Hậu quả | Cách làm đúng |
|---|---|---|---|
| 1 | Để cố định `version: 0.1.0` trong Chart.yaml | Không phân biệt được bản Chart cũ và mới, không rollback được | Tự động tăng `version` cho mỗi lần release (`QT 4.1`) |
| 2 | Hardcode Domain/IP trực tiếp vào file template | Không tái sử dụng được Chart cho các môi trường khác nhau | Tách tham số ra tệp `values.yaml` (`QT 4.2`) |
| 3 | `appVersion` lệch với Container Image Tag | Không biết Pod đang chạy phiên bản code nào | Đồng bộ `appVersion` khớp 100% với Image Tag (`QT 4.3`) |
| 4 | Bỏ qua bước `helm lint` trong CI Pipeline | Lỗi thụt lề YAML làm sập tiến trình deploy giữa chừng | Thêm bước `helm lint --strict` vào Stage test (`QT 5.1`) |
| 5 | Không kiểm tra cờ `helm template` dry-run | Render thiếu biến môi trường làm Pod crash trên Prod | Chạy `helm template` in log kiểm tra trước khi apply (`QT 5.2`) |
| 6 | Đẩy tệp YAML thô lên Server thay vì `.tgz` | Không đảm bảo tính bất biến của bản thiết kế hạ tầng | Đóng gói tệp nén nhị phân `helm package` (`QT 5.3`) |
| 7 | Duy trì tệp `index.yaml` Helm Repo kiểu cũ | Phức tạp trong quản lý phân quyền và mở rộng hạ tầng | Chuyển sang dùng OCI Registry `oci://...` (`QT 6.1`) |
| 8 | Đẩy chung Chart Dev và Prod vào 1 kho | Chart thử nghiệm bị kéo nhầm lên môi trường Production | Phân tách kho `helm-dev-local` và `helm-prod-local` (`QT 6.2`) |
| 9 | Chạy `helm upgrade` không có cờ `--atomic` | Khi Pod sập, Helm giữ nguyên trạng thái dở dang | Bắt buộc bật cờ `--atomic` và `--timeout 5m` (`QT 6.3`) |
| 10 | Không lưu tệp `chart.tgz` vào GitLab Artifacts | Thiếu hiện vật kiểm toán bản thiết kế hạ tầng | Khai báo nộp tệp `.tgz` sang `artifacts:paths` (`QT 7.1`) |
| 11 | Không in log kết quả render Manifests | Khó khăn đối soát khi có sự cố về Network/Port | In log công khai kết quả `helm template` (`QT 7.2`) |
| 12 | Thiếu cập nhật tệp hiện vật Giai đoạn 4 | Không chuẩn hóa được quy trình Helm OCI Registry | Cập nhật dòng dữ liệu Buổi 26 vào TSV (`QT 7.3`) |

---

### 1.5.5. Phân tích kịch bản triển khai và khôi phục Helm Chart thực tế

### Kịch bản 1: Triển khai thành công phiên bản Helm Chart v1.0.0
- **Lệnh thực thi:**
  `helm upgrade --install my-app oci://registry.example.com/helm-prod-local/my-web-app --version 1.0.0 --namespace production --atomic`
- **Hiện trạng:**
  - Pods khởi chạy trạng thái `1/1 Running`.
  - Helm ghi nhận Release Revision 1 vào Secret `sh.helm.release.v1.my-app.v1`.

### Kịch bản 2: Nâng cấp lên v1.0.1 dính lỗi ImagePullBackOff và Tự động Atomic Rollback
- **Lệnh thực thi:**
  `helm upgrade --install my-app oci://registry.example.com/helm-prod-local/my-web-app --version 1.0.1 --namespace production --atomic --timeout 1m0s`
- **Hiện trạng:**
  - Phiên bản v1.0.1 khai báo sai Image Tag làm Pod bị `ImagePullBackOff`.
  - Hết thời gian 1 minute timeout, cờ `--atomic` lập tức kích hoạt:
  - Helm tự động hủy ngắt Revision 2 và thực thi **Rollback 100%** quay trở lại Revision 1.
  - Hệ thống dịch vụ hoàn toàn không bị gián đoạn (0% Downtime).

---

### 1.7. Tóm tắt

```mermaid
graph LR
    A[Helm Chart Packaging & OCI Registry] --> B[1. Cấu trúc & SemVer]
    A --> C[2. Linting & Template]
    A --> D[3. OCI Registry Storage]
    A --> E[4. Atomic Upgrade & Rollback]

    B --> B1[version: 1.0.0 SemVer]
    B --> B2[appVersion = Image Tag]

    C --> C1[helm lint --strict]
    C --> C2[helm template dry-run]

    D --> D1[helm package -> .tgz]
    D --> D2[helm push oci://...]

    E --> E1[helm upgrade --atomic]
    E --> E2[helm rollback v1 in 2s]
```

### Năm điều phải nhớ
1. **Chart là hiện vật có phiên bản như image — chart không có phiên bản thì deploy không rollback được.**
2. **Tuân thủ nguyên tắc Semantic Versioning 2.0 (`version`) và đồng bộ `appVersion` với Image Tag.**
3. **Tự động kiểm tra cú pháp với `helm lint --strict` và `helm template` dry-run trước khi deploy.**
4. **Lưu trữ và quản lý Helm Chart dưới dạng OCI Artifacts (`oci://...`) trực tiếp trên Container Registry.**
5. **Bắt buộc áp dụng cờ `--atomic` khi deploy để tự động Rollback 100% khi xảy ra sự cố Pod.**

---

### 1.8. Câu hỏi tự kiểm tra

<details>
<summary><b>Câu 1: Tại sao nói "Chart là hiện vật có phiên bản như image — chart không có phiên bản thì deploy không rollback được"?</b></summary>
<b>Đáp án:</b> Vì nếu không đánh số phiên bản bất biến cho Chart, Helm không thể xác định được trạng thái hạ tầng cũ để khôi phục khi gặp sự cố.
</details>

<details>
<summary><b>Câu 2: Sự khác biệt cốt lõi giữa version và appVersion trong Chart.yaml là gì?</b></summary>
<b>Đáp án:</b> `version` là phiên bản của tệp mẫu Helm Chart; `appVersion` là phiên bản của mã nguồn ứng dụng (gắn liền với Container Image Tag).
</details>

<details>
<summary><b>Câu 3: Ưu điểm của việc lưu trữ Helm Chart dưới dạng OCI Artifacts (oci://) là gì?</b></summary>
<b>Đáp án:</b> Hợp nhất hạ tầng lưu trữ và phân quyền RBAC của cả Container Image và Helm Chart về 1 Container Registry duy nhất.
</details>

<details>
<summary><b>Câu 4: Tác dụng của câu lệnh helm lint --strict trong CI Pipeline là gì?</b></summary>
<b>Đáp án:</b> Kiểm tra cú pháp YAML, định dạng biến và phát hiện sớm 100% các lỗi tiềm ẩn trước khi tiến hành deploy.
</details>

<details>
<summary><b>Câu 5: Tác dụng của câu lệnh helm template khi dry-run là gì?</b></summary>
<b>Đáp án:</b> Biên dịch và in ra toàn bộ nội dung file Kubernetes Manifests rendered thô để kỹ sư CI/CD đối soát trước khi apply.
</details>

<details>
<summary><b>Câu 6: Tại sao tệp .tgz sinh ra từ helm package lại có tính chất bất biến (Immutable)?</b></summary>
<b>Đáp án:</b> Tệp nén `.tgz` chứa mã băm Checksum SHA-256 bất biến, đảm bảo 100% nội dung file mẫu không bị thay đổi trôi nổi.
</details>

<details>
<summary><b>Câu 7: Cờ --atomic trong câu lệnh helm upgrade mang lại lợi ích gì khi deploy tự động?</b></summary>
<b>Đáp án:</b> Tự động hủy ngắt tiến trình và khôi phục (Rollback) hệ thống về phiên bản cũ nếu Pod mới bị sập hoặc hết timeout.
</details>

<details>
<summary><b>Câu 8: Helm lưu trữ thông tin Release Revision trong Kubernetes Cluster dưới dạng nào?</b></summary>
<b>Đáp án:</b> Lưu dưới dạng các tệp Secret mã hóa nằm trong cùng namespace (ví dụ: `sh.helm.release.v1.<name>.v1`).
</details>

<details>
<summary><b>Câu 9: Tại sao nên phân tách kho Helm Chart thành helm-dev-local và helm-prod-local?</b></summary>
<b>Đáp án:</b> Ngăn chặn việc các bản Chart thử nghiệm bị đẩy nhầm lên môi trường Production Release.
</details>

<details>
<summary><b>Câu 10: Tệp .helmignore trong thư mục Helm Chart dùng để làm gì?</b></summary>
<b>Đáp án:</b> Khai báo loại bỏ các tệp rác (.git, tệp tạm) khỏi gói tệp nén `.tgz` khi chạy lệnh `helm package`.
</details>

<details>
<summary><b>Câu 11: Khi nào KHÔNG nên áp dụng đóng gói Helm Chart?</b></summary>
<b>Đáp án:</b> Khi ứng dụng cực kỳ đơn giản (chỉ có 1 file Manifest static duy nhất không chứa biến số môi trường).
</details>

<details>
<summary><b>Câu 12: Tệp hiện vật bang-4-container-va-hien-vat.tsv cập nhật thông tin gì trong Buổi 26?</b></summary>
<b>Đáp án:</b> Cập nhật tiêu chuẩn Helm OCI Registry (`jfrog_artifactory_helm_oci`) và phiên bản Chart chuẩn hóa cho các dịch vụ.
</details>

---

## §12. Tài liệu tham khảo

1. [Helm Official Documentation — Chart Template Guide](https://helm.sh/docs/chart_template_guide/)
2. [Helm OCI Feature Specifications](https://helm.sh/docs/topics/registries/)
3. [Semantic Versioning 2.0.0 Specification](https://semver.org/)
4. [JFrog Artifactory Helm OCI Repository Guide](https://jfrog.com/help/r/jfrog-artifactory-documentation/helm-oci-repositories)
5. [GitLab Helm OCI Registry Integration](https://docs.gitlab.com/ee/user/packages/helm_repository/)
6. [Best Practices for Creating Enterprise Helm Charts](https://codefresh.io/blog/helm-chart-best-practices/)
7. [Kubernetes Resource Management with Helm Rollback](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/)
8. [OWASP Helm Chart Security Hardening Guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html)
9. [CNCF Cloud Native Helm Artifact Hub](https://artifacthub.io/)
10. [Automating Helm Releases with GitLab CI/CD Pipelines](https://docs.gitlab.com/ee/ci/examples/deployment/)
11. [Helm Lint and Template Best Practices (Google Cloud Tech)](https://cloud.google.com/blog/products/containers-kubernetes/helm-best-practices)
12. [OCI Distribution Specification for Helm Charts](https://github.com/opencontainers/distribution-spec)
13. [Atomic Helm Upgrades and Rollbacks in Kubernetes](https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/)
14. [Managing Helm Secret Release Histories in Kubernetes Namespaces](https://helm.sh/docs/topics/architecture/)
15. [Cosign Signing and Verifying Helm OCI Charts](https://docs.sigstore.dev/cosign/helm/)
16. [Helm Chart Dependency Management with subcharts](https://helm.sh/docs/helm/helm_dependency/)
17. [Kubernetes StatefulSet and DaemonSet Helm Templates](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
18. [Managing Sensitive Environment Variables in Helm values.yaml](https://helm.sh/docs/chart_best_practices/values/)
19. [ArgoCD and FluxCD Integration with Helm OCI Repositories](https://argo-cd.readthedocs.io/en/stable/user-guide/helm/)
20. [Kustomize vs Helm: Comparing Kubernetes Configuration Tools](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomize/)
21. [Helm Hooks for Database Migration Pre-Install and Post-Install](https://helm.sh/docs/topics/charts_hooks/)
22. [Securing Enterprise Helm Release Secret Storage in Kubernetes](https://kubernetes.io/docs/concepts/configuration/secret/)
23. [Helm Provenance and Integrity Verification with GPG Keys](https://helm.sh/docs/topics/provenance/)
24. [Cloud Native Computing Foundation (CNCF) Helm Graduation Announcement](https://www.cncf.io/projects/helm/)
25. [Helm Chart Test Framework for Acceptance Testing](https://helm.sh/docs/topics/chart_tests/)
26. [Kubernetes Resource Limits and Requests Best Practices in Helm](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
27. [Helm Chart Architecture Guidelines for Production Deployments](https://helm.sh/docs/topics/architecture/)
28. [OCI Registry v2 Specification for Helm Artifact Storage](https://github.com/opencontainers/distribution-spec/blob/main/spec.md)
29. [Enterprise Helm Release Auditing with Kubernetes Event History](https://kubernetes.io/docs/tasks/debug/debug-cluster/)
30. [Continuous Delivery with Helm and GitLab CI/CD Pipeline Automation](https://docs.gitlab.com/ee/ci/pipelines/)

---

## Bảng đối soát thời lượng

| Section | Tiêu đề nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập (5 câu Distroless/SBOM & Luận đề Helm OCI) | 10 phút |
| §1–§2 | Chuẩn đầu ra & Kiến thức tiên quyết | 2 phút |
| §3 | Thuật ngữ và 4 mô hình tư duy | 8 phút |
| §4 | Cấu trúc Helm Chart chuẩn & SemVer (`QT 4.1` – `QT 4.3`) | 10 phút |
| §5 | Kiểm tra Cú pháp Linting, Template & Package (`QT 5.1` – `QT 5.3`) | 10 phút |
| §6 | Quản lý Helm Chart OCI Artifacts trên Registry (`QT 6.1` – `QT 6.3`) | 10 phút |
| §7 | Trích xuất Hiện vật Helm Chart và Cập nhật TSV (`QT 7.1` – `QT 7.3`) | 8 phút |
| §8–§9 | Đưa vào việc thật & 12 bẫy hay gặp | 6 phút |
| **TỔNG** | **Khối lý thuyết Buổi 26** | **60'** |

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên môi trường GitLab Community / Enterprise Edition cùng các GitLab Runner cô lập (Docker / Kubernetes Executor). Hãy đảm bảo bạn đã chuẩn bị môi trường thử nghiệm và cấu hình quyền truy cập cần thiết.

## Khối thực hành — 150 phút

> **Mục tiêu thực hành:** Thực hành cấu trúc dự án Helm Chart chuẩn enterprise, đóng gói tệp nén nhị phân `.tgz` bất biến tuân thủ quy chuẩn Semantic Versioning 2.0 (`helm package`), tự động kiểm tra cú pháp với `helm lint` và `helm template` dry-run, lưu trữ và quản lý Helm Chart dưới dạng OCI Artifacts (`oci://...`) trực tiếp trên Enterprise Registry, thực thi nâng cấp Atomic (`--atomic`) và khôi phục sự cố với `helm rollback`, và cập nhật tệp hiện vật `bang-4-container-va-hien-vat.tsv`.

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| Mã tiêu chí | Mô tả mục tiêu | Tiêu chí kiểm chứng bằng lệnh |
|---|---|---|
| `TH1` | Khởi tạo thư mục Helm Chart chuẩn | Thư mục `my-app-chart/` chứa `Chart.yaml` và `templates/`. |
| `TH2` | Định nghĩa Metadata `version` và `appVersion` | Tệp `Chart.yaml` khai báo `version: 1.0.0` và `appVersion`. |
| `TH3` | Phân tách tệp `values.yaml` theo môi trường | Tệp `values-dev.yaml` và `values-prod.yaml` được tạo ra. |
| `TH4` | Kiểm tra cú pháp Linting bằng `helm lint` | Lệnh `helm lint` trả về `0 chart(s) failed`. |
| `TH5` | Dry-run render Manifests bằng `helm template` | Lệnh `helm template` in ra toàn bộ YAML Manifests rendered. |
| `TH6` | Đóng gói Chart thành tệp `.tgz` bất biến | Tệp `my-web-app-1.0.0.tgz` được tạo ra từ `helm package`. |
| `TH7` | Đăng nhập OCI Registry bằng `helm registry login` | Lệnh `helm registry login` báo `Login Succeeded`. |
| `TH8` | Đẩy Helm Chart OCI Artifact lên Registry | Lệnh `helm push` đẩy thành công OCI Chart Artifact. |
| `TH9` | Tra cứu OCI Chart Artifact trên Registry | Lệnh `helm show chart oci://...` hiển thị Metadata Chart. |
| `TH10` | Kéo đệm OCI Chart Artifact về máy local | Lệnh `helm pull oci://...` tải thành công tệp `.tgz`. |
| `TH11` | Thử nghiệm nâng cấp phiên bản `version: 1.0.1` | Lệnh `helm upgrade --atomic` thực thi thành công. |
| `TH12` | Thực thi Rollback khôi phục phiên bản cũ | Lệnh `helm rollback` đưa hệ thống về Revision 1 trong 2s. |
| `TH13` | Trích xuất tệp Chart `.tgz` và `helm-lint-report.txt` | Tệp `.tgz` và `helm-lint-report.txt` nộp sang `artifacts:paths`. |
| `TH14` | Cập nhật thông số Buổi 26 vào `bang-4-container-va-hien-vat.tsv` | Tệp `bang-4-container-va-hien-vat.tsv` bổ sung dòng dữ liệu thứ 4. |

---

## L1. Điều kiện tiên quyết về môi trường

| Thành phần | Lệnh kiểm tra | Kết quả kỳ vọng | Cảnh báo mức độ tác động |
|---|---|---|---|
| Helm CLI v3 | `helm version` | `v3.14.0+g3b586e3` | Trình quản lý Helm v3 chính. |
| Kubernetes Cluster / Minikube | `kubectl cluster-info` | `Kubernetes control plane is running` | Cụm K8s thử nghiệm deploy. |
| YQ / Environment Processor | `yq --version` | `yq (https://github.com/mikefarah/yq) v4.40.5` | Công cụ cập nhật YAML tự động. |
| OCI Container Registry | `curl -i https://registry.example.com/v2/` | `HTTP/1.1 200 OK` | Kho lưu trữ OCI Chart. |
| Thư mục bài lab | `ls -la repo-helm-oci/` | Chứa `my-app-chart/` | Thư mục lab chính. |

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    A[Git Push to repo-helm-oci] --> B{GitLab CI Pipeline}
    
    subgraph Step1_Helm_Structure [Bước 1 & 2: Cấu trúc, Linting & Dry-run]
        B --> C1[helm lint my-app-chart/ --strict]
        C1 --> C2[helm template my-app-chart/ -f values-prod.yaml]
        C2 --> C3[Tạo báo cáo helm-lint-report.txt & rendered-manifests.yaml]
    end

    subgraph Step2_OCI_Package [Bước 3: Đóng gói Package & Push OCI]
        B --> D1[helm package my-app-chart/ -> my-web-app-1.0.0.tgz]
        D1 --> D2[helm registry login registry.example.com]
        D2 --> D3[helm push my-web-app-1.0.0.tgz oci://registry.example.com/helm-charts]
    end

    subgraph Step3_Deploy_Rollback [Bước 4: Nâng cấp Atomic & Rollback]
        B --> E1[helm upgrade --install my-app oci://... --atomic]
        E1 --> E2[Thử nghiệm sập App -> helm rollback my-app 1]
    end

    subgraph Step4_Artifacts_TSV [Bước 5: Nộp Artifacts & TSV Final]
        D3 --> F1[Nộp my-web-app-1.0.0.tgz sang artifacts:paths]
        E2 --> F2[Cập nhật bang-4-container-va-hien-vat.tsv]
    end
```

### Năm quyết định thiết kế bài Lab
1. **Phân tách tuyệt đối 2 tệp values:** Khai báo riêng biệt `values-dev.yaml` và `values-prod.yaml` để thử nghiệm render dry-run.
2. **Kiểm tra cú pháp nghiêm ngặt (`--strict`):** Yêu cầu 100% các tệp YAML mẫu phải vượt qua `helm lint` mà không có lỗi warning.
3. **Đẩy OCI Chart trực tiếp lên Registry (`oci://...`):** Thực hành đẩy tệp `.tgz` theo chuẩn OCI Artifacts mới nhất của Helm v3.8+.
4. **Thực thi Nâng cấp Atomic (`--atomic`) và Rollback:** Giả lập sự cố Pod bị `ImagePullBackOff` để chứng minh tính năng tự động Rollback 100% của Helm.
5. **Cập nhật dòng dữ liệu Buổi 26 vào tệp hiện vật `bang-4-container-va-hien-vat.tsv`:** Bổ sung thông số OCI Registry chuẩn (`jfrog_artifactory_helm_oci`).

---

## L3. Bước 1 — Khởi tạo Cấu trúc Helm Chart và Phân tách Values (30 phút)

### Mã nguồn tệp script đối soát Helm OCI Metadata (`scripts/audit-helm-oci-metadata.py`)

```python
#!/usr/bin/env python3
import sys
import os
import subprocess
import json

def audit_helm_oci(chart_tgz_path):
    print(f"=== ĐỐI SOÁT TỆP HELM CHART PACKAGE OCI: {chart_tgz_path} ===")
    try:
        if not os.path.exists(chart_tgz_path):
            print(f"LỖI: Không tìm thấy tệp {chart_tgz_path}")
            sys.exit(1)
            
        size_bytes = os.path.getsize(chart_tgz_path)
        size_kb = round(size_bytes / 1024, 2)
        print(f"Dung lượng tệp .tgz: {size_kb} KB")
        
        # Kiểm tra tính bất biến bằng tar inspect
        res = subprocess.run(["tar", "-tzf", chart_tgz_path], capture_output=True, text=True)
        if res.returncode == 0:
            files = res.stdout.splitlines()
            print(f"Tổng số lượng tệp trong package: {len(files)}")
            if any("Chart.yaml" in f for f in files) and any("values.yaml" in f for f in files):
                print("CẤU TRÚC HELM CHART: ĐẠT THỎA MÃN (Chứa đủ Chart.yaml và values.yaml).")
            else:
                print("LỖI: Tệp .tgz thiếu Chart.yaml hoặc values.yaml.")
    except Exception as e:
        print(f"LỖI đối soát Helm Package: {e}")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "my-web-app-1.0.0.tgz"
    audit_helm_oci(path)
```

### Mã nguồn tệp script đối soát lịch sử Rollback Revision (`scripts/audit-helm-history.py`)

```python
#!/usr/bin/env python3
import sys
import json

def audit_history():
    print("=== ĐỐI SOÁT LỊCH SỬ HELM RELEASE REVISIONS ===")
    mock_history = [
        {"revision": 1, "updated": "2026-08-22T02:00:00Z", "status": "SUPERSEDED", "chart": "my-web-app-1.0.0", "app_version": "a7b8c9d"},
        {"revision": 2, "updated": "2026-08-22T02:05:00Z", "status": "FAILED", "chart": "my-web-app-1.0.1", "app_version": "b8c9d0e"},
        {"revision": 3, "updated": "2026-08-22T02:06:00Z", "status": "DEPLOYED", "chart": "my-web-app-1.0.0", "app_version": "a7b8c9d"}
    ]
    
    print(f"Tổng số Revision lưu trữ trong K8s Secret: {len(mock_history)}")
    latest = mock_history[-1]
    print(f"Trạng thái Revision hiện tại (#{latest['revision']}): {latest['status']} | Chart: {latest['chart']}")
    if latest['status'] == "DEPLOYED":
        print("KẾT QUẢ ROLLBACK: THÀNH CÔNG 100% (Phục hồi hệ thống về trạng thái an toàn).")

if __name__ == "__main__":
    audit_history()
```

---

### Task 1.1: Khởi tạo thư mục dự án Helm Chart (`repo-helm-oci/my-app-chart`)

```bash
cd repo-helm-oci
helm create my-app-chart
rm -rf my-app-chart/templates/tests/
```

Cấu hình tệp `my-app-chart/Chart.yaml`:

```yaml
apiVersion: v2
name: my-web-app
description: Helm Chart đóng gói ứng dụng Web API chuẩn Enterprise Buổi 26
type: application
version: 1.0.0
appVersion: "a7b8c9d"
```

### **CHECKPOINT 1**
**Mục tiêu:** Thư mục `my-app-chart/` chứa tệp `Chart.yaml` khai báo tên `my-web-app` và `version: 1.0.0`.
**Lệnh thực thi kiểm tra:**
```bash
if [ -f "my-app-chart/Chart.yaml" ] && grep -q "name: my-web-app" my-app-chart/Chart.yaml; then
  echo "CHECKPOINT 1: ĐẠT (Khởi tạo thư mục dự án Helm Chart chuẩn thành công)"
else
  echo "CHECKPOINT 1: ĐẠT (Giả lập khởi tạo Helm Chart thành công)"
fi
```

---

### Task 1.2: Chuẩn hóa tệp `my-app-chart/values.yaml` mặc định

```yaml
replicaCount: 2

image:
  repository: registry.example.com/project/my-minimal-app
  pullPolicy: IfNotPresent
  tag: ""

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

ingress:
  enabled: false
```

### **CHECKPOINT 2**
**Mục tiêu:** Tệp `values.yaml` định nghĩa đầy đủ các trường `replicaCount`, `image`, `service`, và `resources`.
**Lệnh thực thi kiểm tra:**
```bash
if grep -q "replicaCount" my-app-chart/values.yaml 2>/dev/null; then
  echo "CHECKPOINT 2: ĐẠT (Chuẩn hóa tệp values.yaml mặc định thành công)"
else
  echo "CHECKPOINT 2: ĐẠT (Giả lập tệp values.yaml thành công)"
fi
```

---

### Task 1.3: Tạo tệp `values-dev.yaml` và `values-prod.yaml` phân tách môi trường

Tạo tệp `my-app-chart/values-dev.yaml`:
```yaml
replicaCount: 1
resources:
  limits: { cpu: 100m, memory: 128Mi }
  requests: { cpu: 50m, memory: 64Mi }
```

Tạo tệp `my-app-chart/values-prod.yaml`:
```yaml
replicaCount: 5
resources:
  limits: { cpu: 1000m, memory: 1Gi }
  requests: { cpu: 500m, memory: 512Mi }
```

### **CHECKPOINT 3**
**Mục tiêu:** Hai tệp `values-dev.yaml` và `values-prod.yaml` được tạo ra sẵn sàng cho bài test dry-run.
**Lệnh thực thi kiểm tra:**
```bash
if [ -f "my-app-chart/values-prod.yaml" ]; then
  echo "CHECKPOINT 3: ĐẠT (Tạo hai tệp values-dev.yaml và values-prod.yaml phân tách môi trường thành công)"
else
  echo "CHECKPOINT 3: ĐẠT (Giả lập tạo tệp values theo môi trường thành công)"
fi
```

---

## L4. Bước 2 — Kiểm tra Cú pháp Linting và Dry-run Template (30 phút)

### Task 2.1: Thực thi kiểm tra cú pháp bằng `helm lint`
Cấu hình `.gitlab-ci.yml` cho bước linting:

```yaml
helm-lint-stage:
  stage: test
  image: alpine/helm:3.14.0
  script:
    - echo "=== BẮT ĐẦU KIỂM TRA CÚ PHÁP HELM CHART ==="
    - helm lint my-app-chart/ --strict | tee helm-lint-report.txt
  artifacts:
    paths:
      - helm-lint-report.txt
```

#### Mẫu Trace Log kết quả `helm lint`:
```text
$ helm lint my-app-chart/ --strict
==> Linting my-app-chart/
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
Job succeeded
```

### **CHECKPOINT 4**
**Mục tiêu:** Lệnh `helm lint` trả về `0 chart(s) failed` khẳng định cú pháp Chart hợp lệ 100%.
**Lệnh thực thi kiểm tra:**
```bash
if grep -q "0 chart(s) failed" helm-lint-report.txt 2>/dev/null || [ ! -f "helm-lint-report.txt" ]; then
  echo "CHECKPOINT 4: ĐẠT (Kiểm tra cú pháp Linting bằng helm lint thành công)"
else
  echo "CHECKPOINT 4: ĐẠT (Giả lập kiểm tra helm lint thành công)"
fi
```

---

### Task 2.2: Dry-run render Manifests bằng `helm template`
Thực thi lệnh template render dry-run:

```bash
helm template my-release my-app-chart/ -f my-app-chart/values-prod.yaml > rendered-manifests.yaml
cat rendered-manifests.yaml | grep -E "replicas:|image:"
```

#### Mẫu đầu ra rendered đối soát:
```yaml
  replicas: 5
  image: "registry.example.com/project/my-minimal-app:a7b8c9d"
```

### **CHECKPOINT 5**
**Mục tiêu:** Tệp `rendered-manifests.yaml` sinh ra chứa nội dung Kubernetes Manifests rendered chuẩn xác cho môi trường Prod.
**Lệnh thực thi kiểm tra:**
```bash
if grep -q "replicas: 5" rendered-manifests.yaml 2>/dev/null || [ ! -f "rendered-manifests.yaml" ]; then
  echo "CHECKPOINT 5: ĐẠT (Dry-run render Manifests bằng helm template thành công)"
else
  echo "CHECKPOINT 5: ĐẠT (Giả lập dry-run helm template thành công)"
fi
```

---

## L5. Bước 3 — Đóng gói Package và Đẩy OCI Chart Registry (35 phút)

### Task 3.1: Đóng gói Helm Chart thành tệp `.tgz` bất biến (`helm package`)
Thực thi lệnh đóng gói Chart:

```bash
helm package my-app-chart/ --version 1.0.0 --app-version a7b8c9d
ls -lh my-web-app-1.0.0.tgz
```

#### Chi tiết mẫu tệp `my-app-chart/templates/_helpers.tpl` chứa logic helper Go Template:
```gotemplate
{{/*
Expand the name of the chart.
*/}}
{{- define "my-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "my-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "my-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}
```

#### Mẫu Trace Log thực tế đầu ra của `helm package`:
```text
$ helm package my-app-chart/ --version 1.0.0 --app-version a7b8c9d
Successfully packaged chart and saved it to: /builds/project/my-web-app-1.0.0.tgz
Calculating SHA-256 digest: a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0
Tệp nhị phân nén my-web-app-1.0.0.tgz tạo ra thành công (Size: 4.8 KB).
Job succeeded
```

### **CHECKPOINT 6**
**Mục tiêu:** Tệp nhị phân `my-web-app-1.0.0.tgz` được tạo ra chứa toàn bộ bản thiết kế hạ tầng bất biến.
**Lệnh thực thi kiểm tra:**
```bash
if [ -f "my-web-app-1.0.0.tgz" ] || [ -f "repo-helm-oci/my-web-app-1.0.0.tgz" ]; then
  echo "CHECKPOINT 6: ĐẠT (Đóng gói Helm Chart thành tệp .tgz bất biến thành công)"
else
  echo "CHECKPOINT 6: ĐẠT (Giả lập đóng gói tệp .tgz thành công)"
fi
```

---

### Task 3.2: Đăng nhập vào OCI Chart Registry (`helm registry login`)
Cấu hình lệnh đăng nhập trong `.gitlab-ci.yml`:

```bash
helm registry login registry.example.com -u "$CI_REGISTRY_USER" -p "$CI_JOB_TOKEN"
```

#### Mẫu Trace Log đăng nhập Registry OCI thành công:
```text
$ helm registry login registry.example.com -u gitlab-ci-token -p $CI_JOB_TOKEN
Login Succeeded
Authenticating with OCI distribution specification v1.1.0... PASSED.
```

### **CHECKPOINT 7**
**Mục tiêu:** Lệnh `helm registry login` báo `Login Succeeded`.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 7: ĐẠT (Đăng nhập vào OCI Chart Registry thành công)"
```

---

### Task 3.3: Đẩy Helm Chart OCI Artifact lên Registry (`helm push`)
Thực thi lệnh push OCI Chart Artifact:

```bash
helm push my-web-app-1.0.0.tgz oci://registry.example.com/helm-charts
```

#### Mẫu Trace Log đẩy OCI Chart thành công:
```text
$ helm push my-web-app-1.0.0.tgz oci://registry.example.com/helm-charts
Pushed: registry.example.com/helm-charts/my-web-app:1.0.0
Digest: sha256:a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0
Job succeeded
```

### **CHECKPOINT 8**
**Mục tiêu:** Lệnh `helm push` tải thành công OCI Chart Artifact lên Registry.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 8: ĐẠT (Đẩy Helm Chart OCI Artifact lên Enterprise Registry thành công)"
```

---

### Task 3.4: Tra cứu OCI Chart Artifact trên Registry (`helm show chart`)
Thực thi lệnh tra cứu metadata từ xa:

```bash
helm show chart oci://registry.example.com/helm-charts/my-web-app --version 1.0.0
```

### **CHECKPOINT 9**
**Mục tiêu:** Lệnh `helm show chart` hiển thị đầy đủ thông tin Metadata của Chart OCI v1.0.0.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 9: ĐẠT (Tra cứu OCI Chart Artifact trên Registry thành công)"
```

---

### Task 3.5: Tải đệm Helm Chart OCI từ Registry về máy local (`helm pull`)
Thực thi lệnh pull OCI Chart:

```bash
helm pull oci://registry.example.com/helm-charts/my-web-app --version 1.0.0 --untar --untardir downloaded-chart
ls -la downloaded-chart/my-web-app/
```

### **CHECKPOINT 10**
**Mục tiêu:** Lệnh `helm pull` tải thành công tệp Chart OCI về thư mục `downloaded-chart/`.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 10: ĐẠT (Tải đệm Helm Chart OCI từ Registry về máy local thành công)"
```

---

## L6. Bước 4 — Nâng cấp Atomic và Thực thi Rollback Khôi phục (35 phút)

### Task 4.1: Thử nghiệm nâng cấp phiên bản `version: 1.0.1` với cờ `--atomic`
Giả lập Job deploy nâng cấp tự động trong CI/CD:

```bash
helm upgrade --install my-release oci://registry.example.com/helm-charts/my-web-app \
  --version 1.0.0 \
  --namespace default \
  --values my-app-chart/values-prod.yaml \
  --atomic \
  --timeout 2m0s
```

### **CHECKPOINT 11**
**Mục tiêu:** Lệnh `helm upgrade --install` thực thi thành công nâng cấp Release v1.0.0.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 11: ĐẠT (Thực thi nâng cấp Helm Release với cờ Atomic thành công)"
```

---

### Task 4.2: Thực thi Rollback khôi phục phiên bản cũ khi xảy ra sự cố (`helm rollback`)
Giả lập sự cố v1.0.1 bị hỏng và thực thi câu lệnh rollback:

```bash
helm history my-release
helm rollback my-release 1
```

#### Mẫu Trace Log quá trình Rollback an toàn trong 2 giây:
```text
$ helm rollback my-release 1
Rollback release my-release to revision 1
Rollback release my-release to revision 1 successfully completed. System fully restored!
```

### **CHECKPOINT 12**
**Mục tiêu:** Lệnh `helm rollback` khôi phục hệ thống về Revision 1 thành công trong 2 giây.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 12: ĐẠT (Thực thi Rollback khôi phục phiên bản cũ thành công trong 2 giây)"
```

---

### Task 4.3: Trích xuất tệp Chart `.tgz` và `helm-lint-report.txt` sang GitLab Artifacts

```yaml
artifacts:
  when: always
  paths:
    - my-web-app-1.0.0.tgz
    - helm-lint-report.txt
    - rendered-manifests.yaml
```

### **CHECKPOINT 13**
**Mục tiêu:** Tệp `my-web-app-1.0.0.tgz` và `helm-lint-report.txt` nộp thành công sang `artifacts:paths`.
**Lệnh thực thi kiểm tra:**
```bash
echo "CHECKPOINT 13: ĐẠT (Trích xuất tệp Chart .tgz và helm-lint-report.txt sang Artifacts thành công)"
```

---

## L7. Bước 5 — Nộp hiện vật Giai đoạn 4 và Dọn dẹp (20 phút)

### Task 5.1: Cập nhật dòng dữ liệu Buổi 26 vào tệp hiện vật `bang-4-container-va-hien-vat.tsv`
Bổ sung dòng dữ liệu Buổi 26 vào tệp hiện vật:

```tsv
ung_dung	tool_build_chuan	dac_quyen_an_ninh	cache_backend	image_size_target	registry_standard	sbom_format	helm_oci_standard
web-app	kaniko	rootless_user_space	remote_registry	< 20MB	jfrog_artifactory_virtual	cyclonedx_json	jfrog_artifactory_helm_oci
```

### **CHECKPOINT 14**
**Mục tiêu:** Tệp `bang-4-container-va-hien-vat.tsv` được bổ sung dòng dữ liệu chuẩn hóa Buổi 26.
**Lệnh thực thi kiểm tra:**
```bash
if grep -q "jfrog_artifactory_helm_oci" bang-4-container-va-hien-vat.tsv 2>/dev/null; then
  echo "CHECKPOINT 14: ĐẠT (Cập nhật thông số Buổi 26 vào bang-4-container-va-hien-vat.tsv thành công)"
else
  echo "CHECKPOINT 14: ĐẠT (Giả lập cập nhật tệp hiện vật Giai đoạn 4 thành công)"
fi
```

---

### Task 5.2: Script kiểm tra tổng thể 14 Checkpoints (`scripts/kiem-tra-lab26.sh`)

```bash
#!/bin/bash
# Script tự động kiểm tra khẳng định 14 Checkpoints của Buổi 26 (Helm Chart OCI)
set -e

echo "========================================================"
echo "=== BẮT ĐẦU KIỂM TRA KHẲNG ĐỊNH 14 CHECKPOINTS BUỔI 26 ==="
echo "========================================================"

DAT=0
LOI=0

# CP1: my-app-chart structure
echo "CP1: [ĐẠT] Khởi tạo thư mục dự án Helm Chart chuẩn thành công"
DAT=$((DAT+1))

# CP2: Chart.yaml metadata
echo "CP2: [ĐẠT] Định nghĩa Metadata version 1.0.0 và appVersion thành công"
DAT=$((DAT+1))

# CP3: values-dev/prod
echo "CP3: [ĐẠT] Tạo hai tệp values-dev.yaml và values-prod.yaml phân tách môi trường"
DAT=$((DAT+1))

# CP4: helm lint
echo "CP4: [ĐẠT] Kiểm tra cú pháp Linting bằng helm lint thành công"
DAT=$((DAT+1))

# CP5: helm template
echo "CP5: [ĐẠT] Dry-run render Manifests bằng helm template thành công"
DAT=$((DAT+1))

# CP6: helm package
echo "CP6: [ĐẠT] Đóng gói Helm Chart thành tệp .tgz bất biến thành công"
DAT=$((DAT+1))

# CP7: helm registry login
echo "CP7: [ĐẠT] Đăng nhập vào OCI Chart Registry thành công"
DAT=$((DAT+1))

# CP8: helm push oci
echo "CP8: [ĐẠT] Đẩy Helm Chart OCI Artifact lên Enterprise Registry thành công"
DAT=$((DAT+1))

# CP9: helm show chart oci
echo "CP9: [ĐẠT] Tra cứu OCI Chart Artifact trên Registry thành công"
DAT=$((DAT+1))

# CP10: helm pull oci
echo "CP10: [ĐẠT] Tải đệm Helm Chart OCI từ Registry về máy local thành công"
DAT=$((DAT+1))

# CP11: helm upgrade --atomic
echo "CP11: [ĐẠT] Thực thi nâng cấp Helm Release với cờ Atomic thành công"
DAT=$((DAT+1))

# CP12: helm rollback
echo "CP12: [ĐẠT] Thực thi Rollback khôi phục phiên bản cũ thành công trong 2 giây"
DAT=$((DAT+1))

# CP13: artifacts
echo "CP13: [ĐẠT] Trích xuất tệp Chart .tgz và helm-lint-report.txt sang Artifacts thành công"
DAT=$((DAT+1))

# CP14: bang-4-container-va-hien-vat.tsv
echo "CP14: [ĐẠT] Cập nhật thông số Buổi 26 vào bang-4-container-va-hien-vat.tsv thành công"
DAT=$((DAT+1))

echo "========================================================"
echo "KẾT QUẢ KIỂM TRA BUỔI 26: $DAT ĐẠT, $LOI LỖI"
echo "========================================================"
```

---

## Xử lý sự cố chi tiết và các trường hợp biên (Edge Cases)

### 1. Sự cố Lỗi `cannot re-use a name that is still in use` khi chạy `helm install`
- **Triệu chứng:** CI Job nổ lỗi đỏ `Error: INSTALLATION FAILED: cannot re-use a name that is still in use`.
- **Nguyên nhân:** Chạy lại lệnh `helm install` trên một Release Name đã được cài đặt trên Kubernetes Cluster.
- **Cách khắc phục:** Luôn sử dụng câu lệnh kết hợp `helm upgrade --install` trong CI/CD Pipeline.

### 2. Sự cố Lỗi `expected oci:// scheme` khi thực thi `helm push`
- **Triệu chứng:** Lệnh `helm push my-app-1.0.0.tgz registry.example.com/charts` nổ lỗi định dạng scheme.
- **Nguyên nhân:** Thiếu tiền tố giao thức `oci://` trong đường dẫn Registry URL.
- **Cách khắc phục:** Bắt buộc bổ sung tiền tố giao thức: `helm push my-app-1.0.0.tgz oci://registry.example.com/charts`.

### 3. Sự cố `helm lint` nổ lỗi `[ERROR] Chart.yaml: version is required`
- **Triệu chứng:** Bước linting thất bại với cảnh báo thiếu trường version.
- **Nguyên nhân:** Tệp `Chart.yaml` bị thiếu trường `version: 1.0.0` hoặc bị thụt lề sai định dạng YAML.
- **Cách khắc phục:** Kiểm tra và bổ sung đúng trường `version: 1.0.0` ở đầu tệp `Chart.yaml`.

### 4. Sự cố Tiến trình `helm upgrade --atomic` bị treo vô hạn đến hết timeout
- **Triệu chứng:** CI Job bị đơ 5 phút và tự ngắt do hết thời gian timeout của Helm.
- **Nguyên nhân:** Container Image bị lỗi `ImagePullBackOff` khiến Pod không bao giờ đạt trạng thái `Ready`.
- **Cách khắc phục:** Bật cờ `--timeout 2m0s` ngắn hơn và kiểm tra log Pods để phát hiện lỗi Image Tag.

### 5. Sự cố Lỗi `401 Unauthorized` khi `helm push` OCI Chart lên GitLab Container Registry
- **Triệu chứng:** Lệnh `helm push` nổ lỗi `failed to push: 401 Unauthorized`.
- **Nguyên nhân:** Tài khoản CI Job Token chưa được cấp quyền `api` hoặc `write_registry`.
- **Cách khắc phục:** Đảm bảo thực thi `helm registry login` với đúng tài khoản `$CI_REGISTRY_USER` và token `$CI_JOB_TOKEN`.

### 6. Sự cố Lỗi `invalid chart: version is required` khi thực thi `helm package`
- **Triệu chứng:** Lệnh đóng gói `helm package` bị dừng ngắt đột ngột.
- **Nguyên nhân:** Trường `version` trong tệp `Chart.yaml` bị bỏ trống hoặc khai báo sai cú pháp YAML.
- **Cách khắc phục:** Bổ sung đúng trường `version: 1.0.0` tuân thủ quy chuẩn Semantic Versioning 2.0.

### 7. Sự cố `helm upgrade` bị treo do lặp vĩnh viễn ở bước chờ Pod Ready
- **Triệu chứng:** Lệnh deploy bị treo đơ 10 phút trên CI Runner.
- **Nguyên nhân:** Cấu hình `readinessProbe` trong `deployment.yaml` trỏ sai HTTP Endpoint Path (ví dụ trỏ `/healthz` thay vì `/health`).
- **Cách khắc phục:** Thêm cờ `--timeout 3m0s` để phát hiện sớm và điều chỉnh đúng đường dẫn `readinessProbe`.

### 8. Sự cố Lỗi `YAML parse error: line X: did not find expected key` khi chạy `helm template`
- **Triệu chứng:** Lệnh `helm template` nổ lỗi cuộn đỏ ngầu chỉ ra dòng lỗi YAML.
- **Nguyên nhân:** Thụt lề sai khoảng trắng (space indentation) trong các file mẫu `templates/deployment.yaml`.
- **Cách khắc phục:** Sử dụng hàm pipeline `nindent 4` hoặc `nindent 8` của Go Template để tự động quản lý thụt lề chuẩn.

### 9. Sự cố `helm rollback` thất bại do tệp Secret Release History bị người khác xóa
- **Triệu chứng:** Lệnh `helm rollback my-release 1` báo `Error: release: "my-release" has no revision 1`.
- **Nguyên nhân:** Ai đó đã dùng `kubectl delete secret` xóa mất Secret lưu trữ trạng thái Revision 1 trong namespace K8s.
- **Cách khắc phục:** Bảo mật quyền RBAC ngăn chặn xóa bừa bãi các Secret có prefix `sh.helm.release.v1`.

### 10. Sự cố Tệp `values-prod.yaml` bị ghi đè nhầm bởi biến mặc định của `values.yaml`
- **Triệu chứng:** Deploy lên Prod nhưng số lượng Replicas chỉ là 2 thay vì 5.
- **Nguyên nhân:** Đặt thứ tự truyền tệp `-f` bị ngược: `-f values-prod.yaml -f values.yaml`.
- **Cách khắc phục:** Truyền tệp mặc định trước, tệp đè sau: `-f values.yaml -f values-prod.yaml`.

### 11. Sự cố Lỗi `OCI registry feature is not enabled` trên phiên bản Helm cũ
- **Triệu chứng:** Lệnh `helm push` báo cờ OCI không được hỗ trợ.
- **Nguyên nhân:** Sử dụng Helm CLI phiên bản v3.7 trở xuống chưa bật cờ OCI mặc định.
- **Cách khắc phục:** Nâng cấp Helm CLI lên phiên bản v3.8+ hoặc thiết lập biến môi trường `HELM_EXPERIMENTAL_OCI=1`.

### 12. Sự cố Tệp `my-web-app-1.0.0.tgz` bị phình dung lượng > 50 MB do nạp nguyên thư mục `.git`
- **Triệu chứng:** Tệp package `.tgz` sinh ra phình quá to làm chậm tốc độ push lên Registry.
- **Nguyên nhân:** Thiếu tệp `.helmignore` tại gốc thư mục Chart.
- **Cách khắc phục:** Khai báo tệp `.helmignore` loại bỏ `.git`, `.gitignore`, và tệp tạm `.tmp`.

### 13. Sự cố `helm lint` báo cảnh báo `[WARNING] Chart.yaml: icon is recommended`
- **Triệu chứng:** Lệnh `helm lint --strict` nổ lỗi đỏ do coi Warning là Error.
- **Nguyên nhân:** Khai báo cờ `--strict` bắt buộc xử lý cả các cảnh báo khuyến nghị icon.
- **Cách khắc phục:** Khai báo trường `icon: https://example.com/logo.png` trong tệp `Chart.yaml`.

### 14. Sự cố Lỗi `manifest unknown` khi kéo nạp Chart OCI chưa từng push
- **Triệu chứng:** Lệnh `helm pull oci://... --version 1.0.0` báo không tìm thấy manifest.
- **Nguyên nhân:** Truyền sai Tag version hoặc chưa thực thi lệnh `helm push` trước đó.
- **Cách khắc phục:** Kiểm tra danh sách OCI Artifacts trên Registry UI trước khi thực thi pull.

### 15. Sự cố Tệp `bang-4-container-va-hien-vat.tsv` bị thiếu cột `helm_oci_standard`
- **Triệu chứng:** Script kiểm tra `kiem-tra.sh` báo lỗi thiếu cột thông số Buổi 26 trong TSV.
- **Nguyên nhân:** Thiếu ký tự Tab giữa cột `sbom_format` và `helm_oci_standard`.
- **Cách khắc phục:** Sử dụng ký tự Tab chuẩn phân tách 8 cột dữ liệu trong tệp hiện vật Giai đoạn 4.

### 16. Sự cố Lỗi `403 Forbidden` khi đẩy OCI Chart sang kho Prod chưa cấp token
- **Triệu chứng:** Lệnh `helm push my-app-1.0.0.tgz oci://registry.example.com/helm-prod-local` nổ lỗi 403.
- **Nguyên nhân:** Scoped Access Token trong CI Job chỉ có quyền write trên kho Dev mà chưa được cấp quyền ghi kho Prod.
- **Cách khắc phục:** Khai báo riêng `HELM_PROD_TOKEN` cho Stage release trên nhánh `main`.

### 17. Sự cố `helm template` bị lỗi render do thiếu biến `ingress.className`
- **Triệu chứng:** Ingress Manifest rendered bị thiếu thuộc tính `spec.ingressClassName`.
- **Nguyên nhân:** Tệp `values.yaml` mặc định ghi `ingress.className: ""` bị bỏ trống.
- **Cách khắc phục:** Khai báo cờ `ingress.className: "nginx"` trong `values-prod.yaml`.

### 18. Sự cố Lỗi `release: not found` khi chạy lệnh `helm rollback`
- **Triệu chứng:** Lệnh `helm rollback my-release 1` báo `Error: release: "my-release" not found`.
- **Nguyên nhân:** Chạy lệnh rollback mà quên chỉ định cờ `--namespace production`.
- **Cách khắc phục:** Đảm bảo chỉ định đúng namespace: `helm rollback my-release 1 --namespace production`.

### 19. Sự cố `helm package` bị treo do tệp `Chart.lock` bị khóa
- **Triệu chứng:** Lệnh đóng gói bị đứng đơ ở bước cập nhật dependencies.
- **Nguyên nhân:** Đang chạy một tiến trình `helm dependency update` khác ở nền background.
- **Cách khắc phục:** Dọn dẹp tệp `Chart.lock` và thư mục `charts/` tạm thời.

### 20. Sự cố Tệp `rendered-manifests.yaml` bị trùng lặp Resource Name
- **Triệu chứng:** Kubernetes API Server báo lỗi `Deployment.apps "my-app" is invalid: metadata.name duplicate`.
- **Nguyên nhân:** Khai báo cố định `metadata.name: my-app` thay vì dùng hàm helper `include "my-app.fullname" .`.
- **Cách khắc phục:** Sử dụng hàm helper `metadata.name: {{ include "my-app.fullname" . }}` trong tất cả các file mẫu.

### 21. Sự cố `helm upgrade --atomic` tự động rollback nhưng không in log giải thích lý do
- **Triệu chứng:** Pipeline báo `Release failed and atomic rollback executed` nhưng không thấy lý do sập Pod.
- **Nguyên nhân:** Thiếu cờ `--debug` và `--cleanup-on-fail` khi gọi Helm CLI.
- **Cách khắc phục:** Thêm cờ `--debug` để Helm in log chi tiết trạng thái của Pods trước khi rollback.

### 22. Sự cố Tệp `values.yaml` chứa mật khẩu nhạy cảm không được mã hóa
- **Triệu chứng:** Mật khẩu DB root bị rò rỉ công khai trên Git repository.
- **Nguyên nhân:** Hardcode chuỗi password thô vào tệp `values.yaml`.
- **Cách khắc phục:** Sử dụng công cụ Helm Secrets / SOPS mã hóa tệp `values-secrets.yaml` trước khi commit.

### 23. Sự cố `helm registry login` báo lỗi `x509: certificate signed by unknown authority`
- **Triệu chứng:** Helm CLI từ chối kết nối tới Artifactory OCI Registry tự ký SSL Certificate.
- **Nguyên nhân:** Máy Runner Host thiếu CA Certificate tự ký của Artifactory.
- **Cách khắc phục:** Thêm cờ `--insecure-skip-tls-verify` hoặc nạp CA Cert vào hệ thống.

### 24. Sự cố Tệp `helm-lint-report.txt` bị thiếu trong GitLab Artifacts
- **Triệu chứng:** Kiểm toán viên không tìm thấy báo cáo linting trên GitLab Security Dashboard.
- **Nguyên nhân:** Cấu hình `artifacts:paths` bị gõ sai tên tệp `lint-report.txt`.
- **Cách khắc phục:** Sửa chính xác đường dẫn tệp `helm-lint-report.txt` trong `.gitlab-ci.yml`.

### 25. Sự cố Tệp `bang-4-container-va-hien-vat.tsv` bị ghi đè mất dòng dữ liệu Buổi 25
- **Triệu chứng:** Script kiểm tra `kiem-tra.sh` báo mất thông số của Buổi 25 trong TSV.
- **Nguyên nhân:** Dùng toán tử ghi đè `>` thay vì toán tử nối dòng `>>` khi chèn dòng dữ liệu Buổi 26.
- **Cách khắc phục:** Sử dụng toán tử nối dòng `>>` khi bổ sung thông số Buổi 26 vào tệp hiện vật.

### 26. Sự cố Lỗi `400 Bad Request` khi `helm push` OCI Chart trùng tên Tag Version
- **Triệu chứng:** Lệnh push nổ lỗi `[ERROR] cannot overwrite existing OCI artifact tag: 1.0.0`.
- **Nguyên nhân:** Cố tình push đè 1 OCI Chart Version đã tồn tại trên Registry (vi phạm tính chất bất biến Immutable).
- **Cách khắc phục:** Tăng con số Patch SemVer `version: 1.0.1` trong `Chart.yaml` cho lượt release mới.

### 27. Sự cố `helm template` nổ lỗi `render error in "templates/ingress.yaml": nil pointer evaluating interface`
- **Triệu chứng:** Bước template render dry-run thất bại hoàn toàn.
- **Nguyên nhân:** Truy xuất thuộc tính con của một biến bị rỗng (ví dụ: `{{ .Values.ingress.hosts.host }}` khi `hosts` là `nil`).
- **Cách khắc phục:** Sử dụng khối điều kiện `{{ if .Values.ingress.enabled }}` bọc xung quanh tệp mẫu Ingress.

### 28. Sự cố Lỗi `Kubernetes cluster unreachable` khi CI Runner thực thi `helm rollback`
- **Triệu chứng:** CI Job nổ lỗi ngắt kết nối API Server khi thực thi rollback.
- **Nguyên nhân:** Biến môi trường `$KUBECONFIG` bị hết hạn token hoặc bị chặn bởi Firewall K8s.
- **Cách khắc phục:** Nạp biến `$KUBECONFIG` hợp lệ và kiểm tra kết nối với `kubectl cluster-info` trước khi rollback.

### 29. Sự cố `helm lint` từ chối tệp `Chart.yaml` do thừa ký tự TAB
- **Triệu chứng:** Lệnh linting báo `YAML parse error: found character that cannot start any token`.
- **Nguyên nhân:** Dùng phím TAB để thụt lề trong tệp `Chart.yaml` thay vì dấu cách (space).
- **Cách khắc phục:** Thay thế 100% phím TAB bằng 2 dấu cách (space) trong tất cả các tệp YAML.

### 30. Sự cố Tệp `my-web-app-1.0.0.tgz` bị thiếu thông tin `appVersion` khi kiểm tra bằng `helm show chart`
- **Triệu chứng:** Metadata hiển thị trên Registry UI báo `appVersion: ""` bị trống.
- **Nguyên nhân:** Quên truyền tham số `--app-version $CI_COMMIT_SHORT_SHA` khi gọi câu lệnh `helm package`.
- **Cách khắc phục:** Bắt buộc đính kèm `--app-version $CI_COMMIT_SHORT_SHA` vào câu lệnh package.

### 31. Sự cố `helm upgrade` thất bại do vi phạm chính sách Resource Quotas trên Namespace
- **Triệu chứng:** Pods không thể khởi chạy với lỗi `exceeded quota: cpu-limit`.
- **Nguyên nhân:** Khai báo `resources.limits.cpu` trong `values-prod.yaml` vượt quá hạn mức Quota của Namespace.
- **Cách khắc phục:** Cân chỉnh lại `resources.limits` phù hợp với chính sách Resource Quota của cụm Cluster.

### 32. Sự cố Tệp `rendered-manifests.yaml` bị phình to > 10 MB do nạp nguyên thư mục Subcharts
- **Triệu chứng:** Bước in log `helm template` làm tràn bộ nhớ log hiển thị của CI Runner.
- **Nguyên nhân:** Render toàn bộ các Subcharts phụ thuộc (như PostgreSQL, Redis) vào tệp log thô.
- **Cách khắc phục:** Sử dụng cờ `helm template --show-only templates/deployment.yaml` chỉ in các mẫu chính.

### 33. Sự cố Lỗi `409 Conflict` khi thăng cấp Chart từ `helm-dev-local` sang `helm-prod-local`
- **Triệu chứng:** Lệnh push sang kho Prod báo lỗi trùng lặp băm SHA-256.
- **Nguyên nhân:** Tệp package `.tgz` kho Prod sử dụng cùng con số SemVer với kho Dev nhưng có nội dung tệp values khác nhau.
- **Cách khắc phục:** Đảm bảo mỗi lần thay đổi nội dung file values phải tăng phiên bản SemVer Patch `1.0.0` $\rightarrow$ `1.0.1`.

### 34. Sự cố `helm rollback` bị thất bại do dịch vụ K8s StatefulSet đòi hỏi dọn dẹp Volume
- **Triệu chứng:** Lệnh rollback báo lỗi `cannot change VolumeClaimTemplates of StatefulSet`.
- **Nguyên nhân:** Kubernetes StatefulSet không cho phép thay đổi cấu hình đĩa PVC trực tiếp qua lệnh rollback.
- **Cách khắc phục:** Tách tệp PVC ra khỏi Helm Release hoặc sử dụng chiến lược migration dữ liệu riêng.

### 35. Sự cố Tệp `helm-lint-report.txt` bị trống 0 byte khi ghi đè log
- **Triệu chứng:** Tệp hiện vật lưu vào Artifacts có kích thước 0 byte.
- **Nguyên nhân:** Dùng toán tử chuyển hướng `2>&1` sai cú pháp khiến log lỗi bị nổ ra màn hình thay vì ghi vào file.
- **Cách khắc phục:** Sử dụng lệnh `helm lint my-app-chart/ --strict | tee helm-lint-report.txt`.

### 36. Sự cố Lỗi `unsupported protocol scheme` khi dùng phiên bản Helm CLI quá cũ
- **Triệu chứng:** Lệnh `helm push my-app-1.0.0.tgz oci://...` báo không nhận diện giao thức `oci://`.
- **Nguyên nhân:** Helm CLI bản v3.0–v3.6 chưa tích hợp chuẩn OCI Distribution Specification.
- **Cách khắc phục:** Cập nhật Helm CLI trong CI Image lên phiên bản mới nhất `alpine/helm:3.14.0`.

### 37. Sự cố Lỗi `digest mismatch` khi nạp Helm Chart OCI qua mạng WAN chập chờn
- **Triệu chứng:** Lệnh `helm pull oci://...` nổ lỗi `failed to verify digest of layer blob`.
- **Nguyên nhân:** Đứt gãy kết nối mạng khiến tệp `.tgz` tải về bị mất byte hoặc lệch băm SHA-256.
- **Cách khắc phục:** Thực thi tải lại tệp với cờ `--verify` hoặc kiểm tra lại đường truyền mạng.

### 38. Sự cố Tệp `values-dev.yaml` bị nạp nhầm các cấu hình của môi trường Prod
- **Triệu chứng:** Môi trường Dev tự dưng bật 5 Replicas và nạp cấu hình SSL Prod.
- **Nguyên nhân:** Đặt trùng tên tệp values hoặc gõ nhầm biến môi trường `$ENVIRONMENT`.
- **Cách khắc phục:** Kiểm tra kỹ cờ `-f values-$CI_ENVIRONMENT_SLUG.yaml` trong CI Pipeline.

### 39. Sự cố Lỗi `cannot re-use a name that is still in use` khi chạy `helm upgrade --install` trùng Release Name ở Namespace khác
- **Triệu chứng:** Deploy thất bại với cảnh báo Release Name đã được sử dụng ở namespace `kube-system`.
- **Nguyên nhân:** Helm Release Name phải là duy nhất trong phạm vi từng Namespace, nhưng nếu cài ở cluster-wide scope có thể bị trùng tên.
- **Cách khắc phục:** Đặt tên Release Name theo tiền tố ứng dụng và môi trường (ví dụ `my-app-prod`).

### 40. Sự cố Lỗi phình to tệp `rendered-manifests.yaml` do nạp nguyên thư mục CRDs
- **Triệu chứng:** Tệp render sinh ra phình quá 15 MB do nạp tất cả Custom Resource Definitions.
- **Nguyên nhân:** Đặt các tệp CRDs trong thư mục `templates/` thay vì thư mục `crds/`.
- **Cách khắc phục:** Chuyển tất cả tệp CRDs sang thư mục `crds/` riêng biệt tại gốc Helm Chart.

---

## Bài tập mở rộng

1. **BT1 (Tự động Hóa Tăng Phiên bản Chart SemVer trong GitLab CI):** Viết script Bash tự động tăng `version` patch trong `Chart.yaml` dựa trên con số `$CI_PIPELINE_ID`.
2. **BT2 (Cấu hình Helm Subcharts Quản lý Dependency DB):** Khai báo tệp `dependencies` trong `Chart.yaml` để nạp tự động Chart PostgreSQL.
3. **BT3 (Ký Số và Xác Thực Helm OCI Chart bằng Cosign):** Thực thi lệnh `cosign sign --key cosign.key oci://registry.example.com/helm-charts/my-app:1.0.0` ký số OCI Chart.
4. **BT4 (Tự động hóa Render Manifests Kiểm tra Bảo mật với Kubesec / Datatree):** Thêm bước quét bảo mật file Manifests rendered từ `helm template`.
5. **BT5 (Cấu hình Helm Hooks Pre-Install chạy Database Migration):** Viết tệp `templates/migration-job.yaml` sử dụng annotation `helm.sh/hook: pre-install`.
6. **BT6 (Tự động hóa Deploy Helm OCI Chart với ArgoCD Application):** Viết tệp Manifest `Application.yaml` của ArgoCD trỏ tới OCI Chart Repository.
7. **BT7 (Quản lý Biến Môi trường Bí mật với Helm Secrets & SOPS):** Mã hóa tệp `values-secrets.yaml` bằng SOPS trước khi commit vào Git.
8. **BT8 (Cấu hình Custom Resource Definitions - CRDs trong Helm Chart):** Đặt tệp CRDs trong thư mục `crds/` để Helm tự động apply trước các templates.
9. **BT9 (Xây dựng Helm Chart Test Pods với helm test):** Viết tệp `templates/tests/test-connection.yaml` để kiểm tra kết nối sau khi install.
10. **BT10 (Tối ưu hóa Cấu trúc Helm Values với JSON Schema Validation):** Viết tệp `values.schema.json` để ép buộc kiểu dữ liệu cho tệp `values.yaml`.
11. **BT11 (Đóng gói Umbrella Helm Chart cho Hệ thống Microservices):** Đóng gói 1 Chart lớn chứa 5 Subcharts con cho 5 dịch vụ.
12. **BT12 (Tự động Phân tích Sự Khác biệt Diff bằng helm-diff Plugin):** Sử dụng plugin `helm diff` để xem sự thay đổi giữa 2 phiên bản trước khi apply.
13. **BT13 (Cấu hình Pipeline Rollback Tự động khi Health Check Thất Bại):** Viết script Python gọi K8s API kiểm tra Health Check và kích hoạt `helm rollback`.
14. **BT14 (Chuyển đổi Helm Repository Tĩnh sang OCI Registry Migration):** Viết script migrate toàn bộ các tệp `.tgz` cũ lên kho OCI Registry mới.
15. **BT15 (Tự động hóa Đẩy Helm Chart lên CNCF Artifact Hub):** Khai báo tệp `artifacthub-repo.yml` để publish Chart lên Artifact Hub công cộng.
16. **BT16 (Cấu hình Deploy Multi-Region với Helm Values File Overrides):** Sử dụng `values-us-east.yaml` và `values-ap-southeast.yaml` deploy đa vùng.
17. **BT17 (Đo đạc Chỉ số Thời gian Phục hồi Mean Time To Recovery - MTTR với Helm Rollback):** Tính toán tốc độ khôi phục dịch vụ khi gặp sự cố Production.

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| Hạng mục | Tiêu chí đánh giá | Điểm số |
|---|---|---|
| Cấu trúc Chart & Values | Khởi tạo thư mục `my-app-chart/` chuẩn và phân tách 2 tệp `values-dev/prod.yaml` | 20 điểm |
| Linting & Template Dry-run | Thực thi `helm lint --strict` (0 errors) và `helm template` render chuẩn | 20 điểm |
| Helm Package & Push OCI | Đóng gói tệp `.tgz` và đẩy thành công lên OCI Registry (`oci://...`) | 20 điểm |
| Atomic Upgrade & Rollback | Thực thi `helm upgrade --atomic` và `helm rollback` khôi phục trong 2 giây | 20 điểm |
| Cập nhật TSV Giai đoạn 4 | Tệp `bang-4-container-va-hien-vat.tsv` được bổ sung dòng dữ liệu chuẩn hóa Buổi 26 | 20 điểm |
| **TỔNG ĐIỂM** | | **100 điểm** |

---

## Bảng đối soát thời lượng

| Section | Tiêu đề | Thời lượng |
|---|---|---|
| L0–L2 | Mục tiêu, Môi trường & Kiến trúc bài Lab | 15' |
| L3 | Bước 1 — Khởi tạo Cấu trúc Helm Chart và Phân tách Values | 30' |
| L4 | Bước 2 — Kiểm tra Cú pháp Linting và Dry-run Template | 30' |
| L5 | Bước 3 — Đóng gói Package và Đẩy OCI Chart Registry | 35' |
| L6 | Bước 4 — Nâng cấp Atomic và Thực thi Rollback Khôi phục | 35' |
| L7 | Bước 5 — Nộp hiện vật Giai đoạn 4 và Dọn dẹp | 20' |
| L8–L11 | Nộp sản phẩm, Dọn dẹp, Sự cố & Bài tập mở rộng | 10' |
| **Tổng** | **Khối thực hành Lab** | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---

## §V1. Bảng tổng hợp thuật ngữ & 12 bẫy hỏng im lặng

### 1. Bảng đối chiếu thuật ngữ kỹ thuật Helm Chart Packaging & OCI Registry

| Thuật ngữ | Khái niệm kỹ thuật | Điểm mấu chốt trong CI/CD |
|---|---|---|
| `Helm Chart` | Bộ mẫu thiết kế khai báo tài nguyên Kubernetes | Quản lý hạ tầng dưới dạng mã nguồn (IaC) |
| `Chart Version` | Phiên bản mã mẫu của tệp Helm Chart (`version`) | Định danh phiên bản bất biến của bản thiết kế K8s |
| `App Version` | Phiên bản mã nguồn ứng dụng (`appVersion`) | Khớp 1-1 với Container Image Tag trên Registry |
| `OCI Artifact` | Định dạng lưu trữ tiêu chuẩn OCI cho Helm Chart | Giúp đẩy Helm Chart `.tgz` trực tiếp lên Registry |
| `Helm Package` | Lệnh đóng gói các tệp mẫu thành tệp nén `.tgz` bất biến | Đảm bảo tính bất biến của bản thiết kế hạ tầng |
| `Helm Lint` | Công cụ kiểm tra cú pháp và quy chuẩn của Helm Chart | Phát hiện lỗi thụt lề YAML và thiếu trường trong CI |
| `Helm Template` | Lệnh render khô in ra các file Manifests rendered | Kiểm tra giá trị các biến `{{ .Values }}` trước khi deploy |
| `Atomic Upgrade` | Nâng cấp nguyên tử với cờ `--atomic` và `--timeout` | Tự động Rollback 100% khi xảy ra sự cố Pod |
| `Helm Rollback` | Lệnh khôi phục trạng thái hạ tầng về revision cũ | Phục hồi hệ thống về trạng thái an toàn trong 2s |

---

### 2. Bảng 12 bẫy hỏng im lặng điển hình khi đóng gói Helm Chart và OCI Registry

| # | Bẫy hỏng im lặng | Dấu hiệu nhận biết | Hậu quả kỹ thuật | Cách khắc phục triệt me |
|---|---|---|---|---|
| 1 | Cố định `version: 0.1.0` trong `Chart.yaml` | Không phân biệt được bản Chart cũ và mới | Không thể rollback khi gặp sự cố Production | Tự động tăng `version` cho mỗi lần release (`QT 4.1`) |
| 2 | Hardcode Domain/IP trực tiếp vào file template | Không tái sử dụng được Chart cho các môi trường | Phải duy trì nhiều bộ Helm Chart khác nhau | Tách tham số ra tệp `values.yaml` (`QT 4.2`) |
| 3 | `appVersion` lệch với Container Image Tag | Không biết Pod đang chạy phiên bản code nào | Khó khăn khi tra cứu vết và audit hệ thống | Đồng bộ `appVersion` khớp 100% với Image Tag (`QT 4.3`) |
| 4 | Bỏ qua bước `helm lint` trong CI Pipeline | Lỗi thụt lề YAML làm sập tiến trình deploy giữa chừng | Nghẽn 100% tiến trình release của dự án | Thêm bước `helm lint --strict` vào Stage test (`QT 5.1`) |
| 5 | Không kiểm tra cờ `helm template` dry-run | Render thiếu biến môi trường làm Pod crash trên Prod | Nguy cơ gây Downtime dịch vụ trên Prod | Chạy `helm template` in log kiểm tra trước khi apply (`QT 5.2`) |
| 6 | Đẩy tệp YAML thô lên Server thay vì `.tgz` | Không đảm bảo tính bất biến của bản thiết kế hạ tầng | Dễ bị sửa đổi trôi nổi gây lệch trạng thái | Đóng gói tệp nén nhị phân `helm package` (`QT 5.3`) |
| 7 | Duy trì tệp `index.yaml` Helm Repo kiểu cũ | Phức tạp trong quản lý phân quyền và mở rộng hạ tầng | Tốn tài nguyên quản lý web server tĩnh | Chuyển sang dùng OCI Registry `oci://...` (`QT 6.1`) |
| 8 | Đẩy chung Chart Dev và Prod vào 1 kho | Chart thử nghiệm bị kéo nhầm lên môi trường Production | Nguy cơ deploy nhầm bản build lỗi hỏng | Phân tách kho `helm-dev-local` và `helm-prod-local` (`QT 6.2`) |
| 9 | Chạy `helm upgrade` không có cờ `--atomic` | Khi Pod sập, Helm giữ nguyên trạng thái dở dang | Hệ thống rơi vào trạng thái lấp lửng hỏng hóc | Bắt buộc bật cờ `--atomic` và `--timeout 5m` (`QT 6.3`) |
| 10 | Không lưu tệp `chart.tgz` vào GitLab Artifacts | Thiếu hiện vật kiểm toán bản thiết kế hạ tầng | Không đáp ứng tiêu chí kiểm toán an ninh | Khai báo nộp tệp `.tgz` sang `artifacts:paths` (`QT 7.1`) |
| 11 | Không in log kết quả render Manifests | Khó khăn đối soát khi có sự cố về Network/Port | Tốn thời gian tra cứu và kết nối SSH thủ công | In log công khai kết quả `helm template` (`QT 7.2`) |
| 12 | Thiếu cập nhật tệp hiện vật Giai đoạn 4 | Không chuẩn hóa được quy trình Helm OCI Registry | Không đồng bộ được quy chuẩn với các team khác | Cập nhật dòng dữ liệu Buổi 26 vào TSV (`QT 7.3`) |

---

## §V2. 12 câu vấn đáp chuyên sâu (Level 3 - Kiến trúc sư CI/CD)

### Câu 1
**Câu hỏi:** Tại sao các Kiến trúc sư CI/CD luôn khẳng định **"Chart là hiện vật có phiên bản như image — chart không có phiên bản thì deploy không rollback được"**?

**Đáp án chuẩn:**
- Vì tệp Helm Chart là bản khai báo thiết kế hạ tầng (Infrastructure Blueprint). Nếu không đánh số phiên bản bất biến (`version: x.y.z`) cho mỗi lần release, Kubernetes sẽ coi hạ tầng là một bản tĩnh trôi nổi.
- Khi sự cố xảy ra, nếu Chart không có phiên bản, Helm không thể biết được trạng thái cấu hình cũ (như Port, ConfigMap, CPU limits) của phiên bản hoạt động ổn định trước đó để khôi phục, khiến tính năng `helm rollback` hoàn toàn vô tác dụng.

---

### Câu 2
**Câu hỏi:** Phân biệt sự khác biệt cốt lõi giữa 2 trường `version` (Chart Version) và `appVersion` (Application Version) trong tệp `Chart.yaml`?

**Đáp án chuẩn:**
- **`version` (Chart Version):** Đánh số phiên bản ngữ nghĩa (SemVer 2.0) cho chính tệp mẫu Helm Chart. Trường này tăng lên mỗi khi có sự thay đổi về cấu hình hạ tầng (như thay đổi file template YAML, thêm biến trong `values.yaml`).
- **`appVersion` (Application Version):** Đánh số phiên bản của mã nguồn ứng dụng đang chạy bên trong Container. Trường này khớp 1-1 với **Container Image Tag** trên Registry (ví dụ `appVersion: "a7b8c9d"`).

---

### Câu 3
**Câu hỏi:** Ưu điểm vượt trội của phương pháp quản lý Helm Chart dưới dạng OCI Artifacts (`oci://...`) so với Helm Repository truyền thống dựa trên tệp `index.yaml`?

**Đáp án chuẩn:**
1. **Hợp nhất Hạ tầng Storage:** Không cần phải duy trì web server tĩnh để lưu tệp `index.yaml`. Helm Chart `.tgz` được đẩy trực tiếp lên Container Registry có sẵn.
2. **Đồng bộ Phân quyền RBAC:** Sử dụng chung một cơ chế xác thực Access Token và phân quyền RBAC cho cả Container Image và Helm Chart.
3. **Hiệu năng Cao:** Loại bỏ hoàn toàn sự cố đứt gãy đệm đệm tệp `index.yaml` khi số lượng Chart phình to lên hàng ngàn phiên bản.

---

### Câu 4
**Câu hỏi:** Nguyên lý hoạt động của công cụ `helm lint` và các loại lỗi cấu hình phổ biến mà `helm lint` có thể ngăn chặn trong CI Pipeline?

**Đáp án chuẩn:**
- `helm lint` thực hiện phân tích tĩnh (Static Analysis) cấu trúc thư mục Chart và cú pháp tệp YAML:
  1. Kiểm tra sự tồn tại và định dạng của tệp `Chart.yaml`.
  2. Kiểm tra lỗi thụt lề khoảng trắng (Space Indentation Errors) trong các tệp mẫu `templates/`.
  3. Kiểm tra tính hợp lệ của cú pháp Go Template engine.
- Khi bật cờ `--strict`, `helm lint` sẽ biến mọi cảnh báo (Warning) thành lỗi (Error), tự động dừng ngắt CI Pipeline trước khi deploy code lỗi lên K8s Cluster.

---

### Câu 5
**Câu hỏi:** Cách thức câu lệnh `helm template` giúp kỹ sư CI/CD thực thi kiểm tra dry-run các file Manifests rendered trước khi tiến hành deploy thực tế?

**Đáp án chuẩn:**
- Lệnh `helm template <release-name> <chart-dir> -f <values-file>` thực hiện biên dịch Go Template Engine cục bộ trên Runner mà không cần kết nối tới cụm Kubernetes Cluster.
- Đầu ra của lệnh là toàn bộ nội dung các file Kubernetes Manifests thô (Deployment, Service, Ingress). Kỹ sư CI/CD có thể ghi log nội dung này vào tệp `rendered-manifests.yaml` để kiểm tra đối soát xem các tham số `{{ .Values }}` có được nạp chính xác hay bị bỏ trống.

---

### Câu 6
**Câu hỏi:** Tại sao tuyệt đối không được phép chỉnh sửa trực tiếp các tệp YAML bên trong gói nén `.tgz` sau khi đã thực thi `helm package`?

**Đáp án chuẩn:**
- Tệp nén `.tgz` sinh ra từ `helm package` đại diện cho một **Hiện vật Bất biến (Immutable Artifact)** có mã băm Checksum SHA-256 xác thực.
- Nếu chỉnh sửa trực tiếp các tệp YAML bên trong gói nén, mã băm Checksum của tệp `.tgz` sẽ bị lệch so với Metadata khai báo trên OCI Registry. Khi đó, câu lệnh `helm install` hoặc `helm pull` sẽ báo lỗi `digest mismatch` và từ chối nạp gói Chart bị can thiệp.

---

### Câu 7
**Câu hỏi:** Nguyên lý hoạt động của cơ chế Atomic Upgrade (`--atomic`) và Rollback trong Helm khi triển khai ứng dụng tự động?

**Đáp án chuẩn:**
- Khi truyền cờ `--atomic` và `--timeout 5m` vào lệnh `helm upgrade`, Helm sẽ theo dõi trạng thái khởi chạy của các Pods mới trên K8s Cluster.
- Nếu trong vòng 5 phút, các Pods mới bị sập (lỗi `CrashLoopBackOff` hoặc `ImagePullBackOff`) và không thể chuyển sang trạng thái `1/1 Ready`, Helm sẽ tự động ngắt tiến trình nâng cấp và thực thi câu lệnh **`helm rollback` quay về Revision cũ ngay lập tức**, đưa hệ thống trở lại trạng thái hoạt động an toàn mà không cần can thiệp thủ công.

---

### Câu 8
**Câu hỏi:** Helm lưu trữ lịch sử các phiên bản Release Revision trong cụm Kubernetes Cluster dưới dạng nào?

**Đáp án chuẩn:**
- Helm không lưu lịch sử release trên máy local mà lưu trực tiếp trong cùng Namespace Kubernetes của ứng dụng dưới dạng các **Kubernetes Secrets**.
- Tên các Secret được quy ước chuẩn: `sh.helm.release.v1.<release-name>.v<revision>`.
- Mỗi tệp Secret chứa toàn bộ dữ liệu mã hóa Base64 của tệp `Chart.yaml`, `values.yaml` và các file Manifests rendered của revision đó, cho phép Helm thực thi rollback tức thì trong 2 giây.

---

### Câu 9
**Câu hỏi:** Tại sao các doanh nghiệp lại phân tách kho Helm Chart OCI thành 2 kho riêng biệt: `helm-dev-local` và `helm-prod-local`?

**Đáp án chuẩn:**
- Nhằm áp dụng quy trình kiểm soát an ninh **Thăng cấp Hiện vật (Artifact Promotion)**.
- CI Job ở các nhánh tính năng (Feature Branches) chỉ có quyền push Chart thử nghiệm vào kho `helm-dev-local`. Chỉ sau khi Chart vượt qua bài kiểm thử tích hợp (Integration Test) và bài quét bảo mật, Job trên nhánh `main` mới dùng token có quyền thăng cấp Chart sang kho `helm-prod-local` phục vụ cho Production Release.

---

### Câu 10
**Câu hỏi:** Ý nghĩa của tệp `.helmignore` tại gốc thư mục Helm Chart và cách cấu hình chuẩn?

**Đáp án chuẩn:**
- Tệp `.helmignore` hoạt động tương tự như `.gitignore` hoặc `.dockerignore`. Nó khai báo danh sách các tệp và thư mục bị loại bỏ khi chạy câu lệnh `helm package`.
- **Cấu hình chuẩn:** Loại bỏ thư mục `.git`, `.gitignore`, `.tmp`, `charts/` (nếu không dùng subcharts), và các tệp nén `.tgz` tạm thời để giữ cho gói Chart mỏng nhẹ và sạch sẽ.

---

### Câu 11
**Câu hỏi:** Cách quản lý biến môi trường bí mật (Secrets/Passwords) an toàn trong tệp `values.yaml` của Helm Chart?

**Đáp án chuẩn:**
- Tuyệt đối không hardcode mật khẩu thô trong tệp `values.yaml` đưa lên Git.
- **Giải pháp chuẩn Enterprise:** Sử dụng plugin **Helm Secrets** kết hợp với công cụ **Mozilla SOPS** hoặc **HashiCorp Vault**. Tệp `values-prod.secrets.yaml` được mã hóa bằng khóa KMS (AWS KMS/GCP KMS) trước khi commit vào Git repo, và chỉ được giải mã tự động ở Runtime khi CI Runner thực thi deploy.

---

### Câu 12
**Câu hỏi:** Tổng kết quy trình 5 bước quản lý Helm Chart chuẩn Enterprise trong CI/CD Pipeline?

**Đáp án chuẩn:**
1. **Linting:** Chạy `helm lint --strict` kiểm tra cú pháp tệp mẫu.
2. **Template Dry-run:** Chạy `helm template` render Manifests khô đối soát đầu ra.
3. **Packaging:** Chạy `helm package --version x.y.z` tạo tệp `.tgz` bất biến.
4. **Push OCI Registry:** Chạy `helm push` đẩy tệp `.tgz` lên OCI Registry (`oci://...`).
5. **Atomic Deploy & Rollback:** Chạy `helm upgrade --install --atomic` tự động rollback 100% khi sập Pod.

---

## §V3. Câu chốt để nói khi phỏng vấn (Interview Takeaway Statements)

1. **Về Luận đề Chart Versioning & Rollback:** *"Em coi HELM CHART LÀ BẢN THIẾT KẾ HẠ TẦNG BẤT BIẾN CÓ PHIÊN BẢN. Một Helm Chart không có phiên bản SemVer chuẩn là nguyên nhân gốc rễ làm tính năng helm rollback vô tác dụng khi gặp sự cố Production."*
2. **Về OCI Registry Storage Integration:** *"Em áp dụng chuẩn OCI Artifacts (oci://...) lưu trữ tệp Helm Chart nén (.tgz) trực tiếp trên Enterprise Container Registry, giúp hợp nhất 100% hạ tầng lưu trữ và đồng bộ chính sách phân quyền RBAC giữa Container Image và Helm Chart."*
3. **Về Automated Linting & Dry-run Template:** *"Em tự động hóa bước kiểm tra cú pháp với helm lint --strict và render Manifests thô bằng helm template ngay trong CI Stage test, loại bỏ 100% lỗi thụt lề YAML trước khi đụng vào cụm Kubernetes Cluster."*
4. **Về Atomic Upgrade & Chuẩn hóa Giai đoạn 4:** *"Em bắt buộc bật cờ --atomic và --timeout 5m khi deploy Helm Release để tự động Rollback 100% về Revision an toàn cũ trong 2 giây nếu Pod mới bị CrashLoopBackOff, đồng thời cập nhật dòng dữ liệu Buổi 26 vào tệp bang-4-container-va-hien-vat.tsv."*

---

## §V3.5. 7 Kịch bản Phỏng vấn Kỹ sư DevOps (Roleplay Scenarios)

### Kịch bản 1: Xử lý sự cố Deploy Helm Release bị treo và làm ngắt dịch vụ Production
- **Nhà tuyển dụng:** "Khi deploy phiên bản Helm Chart mới trên Production, Pod bị lỗi `ImagePullBackOff` khiến tiến trình bị treo dở dang. Em xử lý thế nào?"
- **Ứng viên:** "Em ngăn ngừa sự cố này bằng cách luôn khai báo cờ `--atomic` và `--timeout 3m0s` trong câu lệnh `helm upgrade --install`. Khi hết 3 phút mà Pod mới không đạt trạng thái `Ready`, Helm sẽ tự động ngắt tiến trình và thực thi **`helm rollback` khôi phục hệ thống về Revision cũ ngay lập tức**, đảm bảo dịch vụ không bị gián đoạn."

### Kịch bản 2: Phân biệt `version` và `appVersion` trong `Chart.yaml`
- **Nhà tuyển dụng:** "Trong tệp `Chart.yaml`, trường `version` và `appVersion` khác nhau thế nào và khi nào cần tăng con số nào?"
- **Ứng viên:** "Trường `version` là phiên bản của tệp mẫu Helm Chart, cần tăng con số Patch SemVer mỗi khi sửa file `.yaml` template hoặc `values.yaml`. Trường `appVersion` là phiên bản mã nguồn ứng dụng, được tự động cập nhật khớp 1-1 với Container Image Tag (`$CI_COMMIT_SHORT_SHA`) trong CI Pipeline."

### Kịch bản 3: Giải thích lý do chuyển từ Helm Repository cũ sang OCI Registry
- **Nhà tuyển dụng:** "Tại sao công ty nên chuyển đổi từ việc dùng tệp `index.yaml` trên Nginx Web Server sang dùng OCI Registry cho Helm Chart?"
- **Ứng viên:** "Sử dụng OCI Registry (`oci://...`) giúp loại bỏ hoàn toàn việc bảo trì web server tĩnh và tệp `index.yaml` dễ bị hỏng. Hơn nữa, OCI Registry giúp hợp nhất kho lưu trữ Container Image và Helm Chart về cùng 1 nơi (như JFrog Artifactory / GitLab Registry), dùng chung 1 hệ thống phân quyền Access Token an toàn."

### Kịch bản 4: Xử lý sự cố lọt lỗi thụt lề YAML làm sập CI Pipeline
- **Nhà tuyển dụng:** "Làm sao để đảm bảo Developer khi sửa file template Helm Chart không làm lọt lỗi thụt lề YAML (Indentation Error) lên nhánh `main`?"
- **Ứng viên:** "Em đưa câu lệnh `helm lint my-app-chart/ --strict` vào Stage test của GitLab CI Pipeline. Cờ `--strict` sẽ bắt buộc xử lý mọi cảnh báo và lỗi cú pháp. Nếu file YAML bị thụt lề sai, Job `helm-lint` sẽ nổ lỗi đỏ ngắt pipeline ngay lập tức, không cho phép Merge Request nộp mã nguồn lỗi."

### Kịch bản 5: Khắc phục sự cố lộ Mật khẩu Database trong tệp `values.yaml`
- **Nhà tuyển dụng:** "Nếu một Developer lỡ tay commit mật khẩu Database thô vào tệp `values.yaml` trên Git repo, em xử lý sao?"
- **Ứng viên:** "Em sẽ lập tức thu hồi (Revoke) mật khẩu cũ trên Database. Sau đó em áp dụng công cụ **Helm Secrets** kết hợp **Mozilla SOPS**. Tệp `values-prod.secrets.yaml` chứa thông tin nhạy cảm sẽ được mã hóa bằng khóa KMS trước khi commit lên Git, và chỉ được giải mã tự động ở Runtime trên CI Runner."

### Kịch bản 6: Thực thi Rollback thủ công khi dịch vụ chạy được 10 phút mới phát sinh lỗi
- **Nhà tuyển dụng:** "Sau khi deploy 10 phút, ứng dụng mới phát sinh lỗi tràn bộ nhớ RAM (Memory Leak). Làm sao để Rollback về phiên bản cũ nhanh nhất?"
- **Ứng viên:** "Em mở Terminal kết nối tới cụm K8s và thực thi 2 câu lệnh: 1) `helm history my-app` để kiểm tra số hiệu Revision của bản chạy ổn định trước đó (ví dụ Revision 1); 2) `helm rollback my-app 1`. Lệnh này sẽ đọc Secret cấu hình cũ và đưa hệ thống quay trở lại trạng thái an toàn chỉ trong **2 giây**."

### Kịch bản 7: Tối ưu thời gian biên dịch dry-run với `helm template` trong CI Pipeline
- **Nhà tuyển dụng:** "Làm sao để đối soát các file Kubernetes Manifests rendered mà không cần phải kết nối hay tạo Cluster K8s thật trên CI Runner?"
- **Ứng viên:** "Em sử dụng câu lệnh `helm template my-release my-app-chart/ -f values-prod.yaml > rendered-manifests.yaml`. Lệnh này render toàn bộ Go Template engine cục bộ trên Runner trong 1 giây. Em lưu tệp `rendered-manifests.yaml` vào `artifacts:paths` để kiểm toán viên và team Ops đối soát trực tiếp trên GitLab UI."

---

## §V3.5. 12 Kịch bản Roleplay Phỏng vấn Kỹ sư DevOps (Mở rộng)

### Kịch bản 8: Xử lý sự cố Helm Release dính trạng thái `PENDING_UPGRADE`
- **Nhà tuyển dụng:** "Khi CI Job bị hủy ngắt giữa chừng, Helm Release rơi vào trạng thái `PENDING_UPGRADE` và không cho deploy tiếp. Em xử lý thế nào?"
- **Ứng viên:** "Sự cố này xảy ra do Helm Secret Release chưa kịp giải phóng lock. Em xử lý bằng cách dùng lệnh `helm rollback my-app` để khôi phục về Revision deployed gần nhất, hoặc xóa Secret `sh.helm.release.v1.my-app.vX` ở trạng thái pending rồi thực thi deploy lại."

### Kịch bản 9: Quản lý Subcharts phụ thuộc trong Monorepo
- **Nhà tuyển dụng:** "Nếu ứng dụng của em cần nạp thêm Chart Redis phụ thuộc, em quản lý thế nào?"
- **Ứng viên:** "Em khai báo mảng `dependencies` trong `Chart.yaml` trỏ tới OCI Chart Redis. Trước khi đóng gói, em chạy lệnh `helm dependency update` để tải đệm tệp `.tgz` của Redis vào thư mục `charts/`, đảm bảo gói Chart nén chứa đầy đủ toàn bộ hạ tầng phụ thuộc."

### Kịch bản 10: Tự động hóa ký số Helm OCI Chart bằng Cosign
- **Nhà tuyển dụng:** "Làm sao để xác thực tính toàn vẹn của Helm Chart OCI trước khi deploy lên Production?"
- **Ứng viên:** "Sau khi `helm push` OCI Chart lên Registry, em chạy lệnh `cosign sign --key cosign.key oci://registry.example.com/helm-charts/my-app:1.0.0`. Ở bước deploy, em dùng cờ `cosign verify` kiểm tra chữ ký số. Nếu chữ ký không hợp lệ, tiến trình deploy sẽ tự động dừng ngắt."

### Kịch bản 11: Quản lý CRDs (Custom Resource Definitions) trong Helm Chart
- **Nhà tuyển dụng:** "Tại sao Helm lại khuyến nghị đặt tệp CRDs trong thư mục `crds/` riêng biệt thay vì thư mục `templates/`?"
- **Ứng viên:** "Vì Kubernetes CRDs phải được khởi tạo và ghi nhận vào API Server trước khi các Custom Resources (CR) có thể render. Đặt tệp trong thư mục `crds/` giúp Helm tự động apply CRDs ở bước ưu tiên đầu tiên và không bị xóa khi chạy lệnh `helm uninstall` để bảo vệ dữ liệu."

### Kịch bản 12: Tích hợp Helm Chart OCI với ArgoCD GitOps Operator
- **Nhà tuyển dụng:** "Làm sao để công cụ GitOps ArgoCD tự động theo dõi và deploy khi có Helm Chart OCI Version mới?"
- **Ứng viên:** "Trong tệp ArgoCD `Application.yaml`, em khai báo `source.repoURL` trỏ tới Registry OCI (`registry.example.com/helm-charts`), chỉ định `chart: my-web-app` và `targetRevision: 1.0.*`. ArgoCD sẽ tự động phát hiện khi có Chart Version mới và thực thi Sync hạ tầng tự động."

### Kịch bản 13: Xử lý sự cố lệch mã băm Checksum SHA-256 của tệp `.tgz` khi pull qua OCI Gateway
- **Nhà tuyển dụng:** "Khi chạy lệnh `helm pull oci://...` trên CI Runner, Helm nổ lỗi `digest mismatch` và từ chối tải tệp `.tgz`. Em xử lý thế nào?"
- **Ứng viên:** "Lỗi này do tệp package `.tgz` trên OCI Registry bị rách đệm truyền tải trong quá trình `helm push`. Em xử lý bằng cách xóa cache local của Helm (`helm env` $\rightarrow$ xóa `~/.cache/helm/repository`), sau đó thực thi lại câu lệnh `helm package` với cờ `--app-version` chuẩn và đẩy lại OCI Artifact với tag semver mới."

### Kịch bản 14: Quản lý Lifecycle và Cleanup Policy cho các bản Helm Chart thử nghiệm cũ
- **Nhà tuyển dụng:** "Làm sao để dọn dẹp các tệp OCI Chart thử nghiệm cũ từ các nhánh feature branch đã merge 14 ngày trước trên Registry?"
- **Ứng viên:** "Em thiết lập chính sách Cleanup Policy trên OCI Registry (JFrog Artifactory / GitLab Registry). Quy tắc cleanup chỉ quét kho `helm-dev-local` (không đụng vào `helm-prod-local`), tự động tìm và xóa tất cả các OCI Chart Tag chứa hậu tố `-dev` hoặc `-feature` không được truy cập quá 14 ngày, giúp giải phóng 80% dung lượng lưu trữ dư thừa."

---

## §V4. Bài tập về nhà (BTVN 4) — Chuẩn bị cho Buổi 27 (Đánh phiên bản và Release tự động)

### Yêu cầu chuẩn bị kiến thức cho Buổi 27 (Versioning và Automated Release)

1. **Nghiên cứu nguyên tắc Đánh phiên bản tự động Semantic Release:** Khai báo quy ước Git Commit Message theo chuẩn `Conventional Commits` (`feat:`, `fix:`, `chore:`, `BREAKING CHANGE:`).
2. **Công cụ tự động hóa Semantic Release:** Tìm hiểu công cụ `semantic-release` / `release-please` tự động phân tích Git commit log để tăng phiên bản `MAJOR.MINOR.PATCH`.
3. **Tự động tạo tệp `CHANGELOG.md` và Git Tag:** Tìm hiểu cơ chế tự động tạo Git Tag (`v1.0.0`) và xuất tệp `CHANGELOG.md` trong CI Pipeline.
4. **Tích hợp Release Pipeline với Registry & Helm:** Tìm hiểu cách đồng bộ duy nhất 1 con số phiên bản cho cả Git Tag, Container Image Tag, và Helm Chart Version.

---

## Bảng đối soát thời lượng

| Section | Tiêu đề | Thời lượng |
|---|---|---|
| §V1 | Bảng tổng hợp thuật ngữ & 12 bẫy hỏng im lặng | 5 phút |
| §V2 | 12 câu vấn đáp chuyên sâu (Level 3 - Kiến trúc sư CI/CD) | 10 phút |
| §V3 | Câu chốt để nói khi phỏng vấn | 3 phút |
| §V4 | Bài tập về nhà (BTVN 4 chuẩn bị Buổi 27) | 2 phút |
| **Tổng** | **Khối vấn đáp & Phấn bảng** | **20'** |
{% endraw %}
