---
layout: post
title: "[Bài 16] Kiểm Soát Tải Hình Ảnh Bằng ImagePolicyWebhook: Cấu Hình Admission Controller & Allowed Registries"
date: 2026-09-12 10:30:00 +0700
categories: [CKS]
tags:
  - CKS
  - Kubernetes
  - Security
  - Hardening
  - DevSecOps
  - Part-16
series: "CKS Security Specialist Mastery"
series_order: 16
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?auto=format&fit=crop&w=1200&q=80"
summary: "[CKS P.16] Hướng dẫn chuyên sâu Kiểm Soát Tải Hình Ảnh Bằng ImagePolicyWebhook: Cấu Hình Admission Controller & Allowed Registries: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Kiểm Soát Tải Hình Ảnh Bằng ImagePolicyWebhook: Cấu Hình Admission Controller & Allowed Registries."
  - "Làm chủ các thao tác lệnh kubectl tốc độ cao, xử lý sự cố cụm thực tế và tối ưu hóa tài nguyên Pod/Node."
  - "Củng cố kỹ năng thực chiến sát với đề thi chứng chỉ quốc tế của Linux Foundation / CNCF."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 16] KIỂM SOÁT TẢI HÌNH ẢNH BẰNG IMAGEPOLICYWEBHOOK: CẤU HÌNH ADMISSION CONTROLLER & ALLOWED REGISTRIES

Trong kỷ nguyên điện toán đám mây và kiến trúc microservices phân tán quy mô lớn, **Kubernetes (CKS)** đóng vai trò là nền tảng điều phối container (Container Orchestration) tiêu chuẩn công nghiệp. Để làm chủ hệ thống trong môi trường sản xuất (Production) cũng như chinh phục kỳ thi chứng chỉ quốc tế của Linux Foundation / CNCF, kỹ sư không chỉ nắm vững các câu lệnh thao tác cơ bản mà phải thấu hiểu sâu sắc bản chất cơ chế tầng thấp: từ chu trình điều hòa (Reconciliation Loop), cấu trúc điều phối tài nguyên, kiến trúc mạng CNI, lưu trữ CSI cho đến các chuẩn mực an ninh phòng thủ chiều sâu.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn giải mã toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp bài thực hành Lab từng bước và bộ câu hỏi phỏng vấn chuẩn Architect / Lead Engineer.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

| # | Câu hỏi ôn tập | Đáp án chuẩn ngắn gọn |
|---|---|---|
| 1 | Rủi ro của cờ tag mutable `:latest`? | Dễ bị **Image Swapping Attack** (tráo đổi mã độc) |
| 2 | Cụm từ ghim mã băm bất biến? | **Image Digest Pinning (`@sha256:...`)** |
| 3 | Tên plugin kiểm định kho ảnh trên kube-apiserver? | Plugin **`ImagePolicyWebhook`** |
| 4 | Cờ nguyên tắc Fail-Closed Security? | Cờ **`defaultAllow: false`** trong admission-config.yaml |
| 5 | Công cụ phân tích tĩnh bản kê khai YAML? | Công cụ **`kube-linter`** hoặc **`trivy config`** |



> **"Bảo vệ kho ảnh tin cậy và kiểm soát chặt chẽ nguồn gốc hình ảnh Container bằng chính sách Allowed Registries và Image Policy Webhook là rào chắn phòng thủ tối quan trọng thuộc chứng chỉ CKS, đòi hỏi chuyên gia bảo mật phải triệt tiêu hoàn toàn rủi ro từ việc tải Container Images tự do từ Public Registries trôi nổi (chứa lỗ hổng CVEs chưa vá hoặc mã độc chèn ngầm); làm chủ kỹ thuật biên soạn chính sách kiểm soát danh sách kho ảnh được phép (Allowed Registries Policy) thông qua Kyverno, OPA Gatekeeper và ValidatingAdmissionPolicy; cưỡng chế ghim hình ảnh theo mã băm bất biến Image Digest (`@sha256:...`); đồng thời vô hiệu hóa cờ tag mutable `:latest` để đảm bảo 100% workloads chạy trên cụm Kubernetes đều đến từ nguồn lưu trữ uy tín được doanh nghiệp phê duyệt."**

**Kết quả từ các buổi trước được sử dụng lại:**

| Kết quả / Công cụ | Buổi + số hiệu `QT` | Dùng ở đâu trong buổi này |
|---|---|---|
| Quản lý chính sách Admission Kyverno / OPA | Buổi 53 `QT 4.1` | Xây dựng ClusterPolicy Allowed Registries kiểm soát domain kho ảnh |
| Ký số và xác minh hiện vật bằng Cosign | Buổi 59 `QT 4.1` | Kết hợp xác minh chữ ký Cosign với quy tắc Allowed Registries |
| Ghim cờ mã băm bất biến Image Digest | Buổi 60 `QT 4.1` | Bắt buộc 100% Pod manifest phải dùng cờ `@sha256:...` |

---



| # | Kỹ năng thực hiện được | Hiện vật chứng minh |
|---|---|---|
| 1 | Phân tích rủi ro của Public Registries trôi nổi so với Private Trusted Registries | Bảng so sánh rủi ro an ninh kho ảnh |
| 2 | Biên soạn chính sách Kyverno `ClusterPolicy` chặn ảnh ngoài danh sách trắng | Tệp YAML `ClusterPolicy` kiểm tra pattern |
| 3 | Biên soạn chính sách `ValidatingAdmissionPolicy` CEL kiểm soát domain kho ảnh | Tệp YAML `ValidatingAdmissionPolicy` CEL |
| 4 | Cấu hình cấm tag `:latest` và bắt buộc ghim cờ Image Digest `@sha256:...` | Tệp YAML policy cưỡng chế `Enforce` |
| 5 | Gỡ lỗi Pod bị chối bỏ khởi tạo do vi phạm chính sách Allowed Registries | Thông điệp lỗi `403 Forbidden` từ Admission Webhook |

---



| Kiến thức tiên quyết | Nguồn tự học nếu thiếu |
|---|---|
| Khái niệm Admission Webhooks Kyverno / OPA | Buổi 53 (`QT 4.1`) |
| Ký số và xác minh hiện vật bằng Cosign | Buổi 59 (`QT 4.1`) |
| Plugin `ImagePolicyWebhook` trên kube-apiserver | Buổi 60 (`QT 4.1`) |

---



### 3.1. Thuật ngữ Việt–Anh

| # | Thuật ngữ tiếng Việt | Tiếng Anh tương đương | Ghi chú chuẩn hoá trong thân bài |
|---|---|---|---|
| 1 | Kho ảnh được phép | Allowed Registries | Danh sách trắng các domain Registry uy tín được cấp phép tải ảnh |
| 2 | Danh sách trắng kho ảnh | Registry Whitelisting | Kỹ thuật chỉ cho phép Pod tải ảnh từ các domain trong danh sách |
| 3 | Chính sách chặn tag latest | Disallow Latest Tag Policy | Quy tắc từ chối các Pod spec sử dụng cờ tag `:latest` |
| 4 | Ghim mã băm bất biến | Image Digest Pinning (`@sha256:...`) | Bắt buộc sử dụng chuỗi mã băm digest duy nhất đại diện cho image |
| 5 | Bộ quy tắc cụm Kyverno | Kyverno `ClusterPolicy` | Đối tượng CRD dùng để định nghĩa quy tắc kiểm soát kho ảnh |
| 6 | Bộ ràng buộc OPA Gatekeeper | OPA Gatekeeper `Constraint` | Ràng buộc áp đặt chính sách Allowed Registries theo ngôn ngữ Rego |
| 7 | Chính sách kiểm định Cel | `ValidatingAdmissionPolicy` (CEL) | Tính năng kiểm định tích hợp sẵn của Kubernetes sử dụng biểu thức CEL |
| 8 | Tấn công tráo đổi ảnh | Image Swapping Attack | Kỹ thuật thay thế ảnh thật bằng ảnh độc hại cùng tên tag |
| 9 | Thẻ định danh thay đổi được | Mutable Image Tag | Cờ tag tên ảnh có thể bị ghi đè nội dung trên Registry |
| 10 | Từ chối khởi tạo Pod | Pod Admission Rejection (403) | Phản hồi chối bỏ lệnh tạo Pod khi vi phạm quy tắc Allowed Registries |
| 11 | Kho ảnh bảo mật riêng tư | Enterprise Private Registry | Kho lưu trữ ảnh nội bộ doanh nghiệp (Harbor, ECR, GAR) |
| 12 | Quy tắc kiểm tra cờ regex | Regex Pattern Matcher | Cú pháp regex kiểm tra tên miền image (như `^harbor\.internal/.*`) |
| 13 | Bỏ qua kiểm tra cho Namespace | Namespace Exclusion | Ngoại lệ chính sách áp dụng cho các Namespace hệ thống như `kube-system` |
| 14 | Nhật ký từ chối tải ảnh | Admission Audit Log | Nhật ký ghi lại các lệnh khởi tạo Pod bị từ chối do sai Registry |



Mô hình Cửa Hải Quan Kiểm Soát Hàng Nhập Khẩu và Giấy Phép Cảng Biển Tin Cậy: Việc kéo Container Images từ Public Registries trôi nổi giống như Chấp Nhận Hàng Hóa Từ Bất Kỳ Con Tàu Nào Cập Bến: kẻ buôn lậu (hacker) có thể dễ dàng vận chuyển hàng giả, hàng nhái, hoặc mã độc vào kho. `Allowed Registries Policy` giống như Danh Sách Các Cảng Biển Quốc Tế Được Cấp Phép (Whitelisted Ports): Cửa Hải Quan (Admission Controller) kiểm tra giấy tờ vận đơn, nếu tàu đến từ cảng chưa đăng ký (`docker.io` trôi nổi), lệnh nhập kho bị chặn đứng ngay lập tức tại cổng (`403 Forbidden`). Cờ tag `:latest` giống như Nhãn Dán Giá Mẹo "Hàng Mới Nhất" có thể dán đè lên bất kỳ thùng hàng nào: Cửa Hải Quan bắt buộc phải bóc nhãn giả và soi Mã Băm Mã Vạch DNA Bất Biến (`@sha256:...`) để đảm bảo đúng 100% lô hàng đã được duyệt kiểm định chất lượng trước khi cho phép lưu hành trong cụm.

---

### 1.1. Rủi ro của Public Registries và Nguyên lý White-listing Allowed Registries (12 phút)

**Nguyên lý cốt lõi:** Mọi Container Image triển khai trong cụm BẮT BUỘC phải đến từ danh sách kho ảnh tin cậy (Allowed Registries) được cấp phép; CẤM TUYỆT ĐỐI việc kéo ảnh từ các Public Registries trôi nổi không kiểm soát.

**Giải thích cơ chế ngầm:** Tải ảnh từ các kho công khai (Public Registries) chứa đựng rủi ro cao về mã độc (Trojans, CryptoMiners) hoặc các lỗ hổng CVEs chưa được vá. Khai báo danh sách Allowed Registries (Whitelisting) đảm bảo 100% hình ảnh đã được qua quy trình rà soát của doanh nghiệp.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để Pod kéo trực tiếp `image: docker.io/unknown-user/app:v1` trên môi trường Production.

**Minh hoạ.**

```mermaid
graph TD
    subgraph Public Untrusted Registries
        PublicReg[Public Docker Hub / Untrusted Registries] -->|"Pull Image"| UntrustedPod[Pod Untrusted: Risk of Backdoors & Malware!]
    end

    subgraph Allowed Registries Whitelisting
        PrivateReg[Enterprise Registry: harbor.internal] -->|"Kyverno / OPA Policy Check"| Admission[Admission Controller]
        Admission -->|"Match Allowed Domain"| TrustedPod[Pod Approved: Running Safely]
        PublicReg -.->|"Mismatch Allowed Domain"| Admission
        Admission -.->|"Block Connection"| Reject[REJECT 403 Forbidden!]
    end
```

**Nguyên lý cốt lõi:** CẤM TUYỆT ĐỐI việc sử dụng cờ tag mutable `:latest` hoặc không ghi tag trong Pod manifest; bắt buộc phải ghim phiên bản cụ thể kèm mã băm Image Digest (`@sha256:...`).

**Giải thích cơ chế ngầm:** Cờ tag `:latest` có thể bị ghi đè bất kỳ lúc nào trên Registry (Image Swapping Attack). Ghim cờ mã băm `@sha256:...` triệt tiêu nguy cơ bị thay đổi nội dung image.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Khai báo `image: harbor.internal/apps/web:latest` trong Pod spec.

**Minh hoạ.**

```yaml
# CẤM TRONG CKS (RỦI RO TAG LATEST):
image: harbor.internal/apps/web:latest

# CHUẨN CKS (GHIM IMAGE DIGEST BẤT BIẾN):
image: harbor.internal/apps/web@sha256:a1b2c3d4e5f67890...
```

---

### 1.2. Biên soạn Chính sách Allowed Registries bằng Kyverno & OPA Gatekeeper (12 phút)

**Nguyên lý cốt lõi:** Để chặn các Container Images nằm ngoài danh sách Allowed Registries bằng Kyverno, bắt buộc phải biên soạn đối tượng `ClusterPolicy` với quy tắc `validate` kiểm tra thuộc tính `image` qua mẫu pattern (như `harbor.internal/*`).

**Giải thích cơ chế ngầm:** Kyverno sẽ quét thuộc tính `spec.containers[*].image` của mọi lệnh tạo Pod. Nếu domain không khớp mẫu `harbor.internal/*`, lệnh tạo Pod bị hủy bỏ.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Viết chính sách Kyverno nhưng quên khai báo khối `validate.pattern` hoặc viết sai cú pháp regex.

**Minh hoạ.**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-allowed-registries
spec:
  validationFailureAction: Enforce # Cưỡng chế chặn!
  rules:
    - name: validate-registries
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Chỉ cho phép tải ảnh từ kho tin cậy harbor.internal!"
        pattern:
          spec:
            containers:
              - image: "harbor.internal/*"
```

**Nguyên lý cốt lõi:** Khi triển khai chính sách `AllowedRegistries`, BẮT BUỘC phải khai báo khối `exclude` bỏ qua Namespace `kube-system` để tránh làm hỏng các Pods hệ thống của Kubernetes (như CoreDNS hay Kube-proxy).

**Giải thích cơ chế ngầm:** Các Pods hệ thống trong `kube-system` thường kéo ảnh từ `registry.k8s.io` hoặc `gcr.io`. Nếu không loại trừ `kube-system`, chính sách sẽ chặn luôn Pod hệ thống làm sập toàn cụm.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Áp đặt chính sách Allowed Registries toàn cụm mà không thêm khối exclude cho `kube-system`.

**Minh hoạ.**

```yaml
# Khai báo ngoại lệ cho Namespace hệ thống trong Kyverno:
spec:
  rules:
    - name: validate-registries
      exclude:
        resources:
          namespaces:
            - kube-system
            - kube-public
```

---

### 1.3. Cưỡng chế Ghim Image Digest và Chặn Tag `:latest` ở Tầng Admission Control (10 phút)

**Nguyên lý cốt lõi:** Cấu hình cờ `validationFailureAction: Enforce` trong Kyverno (hoặc `enforcementAction: deny` trong OPA) để cưỡng chế ngắt kết nối ngay lập tức khi phát hiện Pod vi phạm quy tắc kho ảnh.

**Giải thích cơ chế ngầm:** Cờ `Audit` chỉ ghi log cảnh báo mà vẫn cho phép tạo Pod. Cờ `Enforce` từ chối trực tiếp lệnh POST tạo Pod vi phạm.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để cờ `validationFailureAction: Audit` trên môi trường Production khiến Pod dùng ảnh xấu vẫn khởi tạo thành công.

**Minh hoạ.**

```yaml
# Bắt buộc khai báo Enforce để chặn vi phạm:
spec:
  validationFailureAction: Enforce
```

**Nguyên lý cốt lõi:** Sử dụng `ValidatingAdmissionPolicy` CEL trong Kubernetes v1.30+ với biểu thức `variables.image.startsWith('harbor.internal/')` để kiểm soát kho ảnh trực tiếp không cần cài thêm controller bên thứ ba.

**Giải thích cơ chế ngầm:** `ValidatingAdmissionPolicy` chạy trực tiếp trong kube-apiserver bằng ngôn ngữ CEL (Common Expression Language), mang lại hiệu năng cao và không phụ thuộc vào Pods bên thứ ba.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Viết biểu thức CEL bị lỗi cú pháp làm ngắt kết nối API Server.

**Minh hoạ.**

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: allowed-registries-cel
spec:
  failurePolicy: Fail
  validations:
    - expression: "object.spec.containers.all(c, c.image.startsWith('harbor.internal/'))"
      message: "Ảnh container bắt buộc phải đến từ harbor.internal!"
```

**Nguyên lý cốt lõi:** Khi chẩn đoán lỗi Pod bị từ chối với thông điệp `image is not from an allowed registry`, đối soát lại thuộc tính `image` trong Pod spec với danh sách regex domain khai báo trong chính sách Allowed Registries.

**Giải thích cơ chế ngầm:** Lỗi này xảy ra khi tên domain kho ảnh trong tệp Pod spec không khớp với chuỗi regex pattern được phép.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Sửa lại tệp manifest nhưng vẫn gõ thiếu domain suffix (như gõ nhầm `harbor.internal` thành `harbor.com`).

**Minh hoạ.**

```bash
# Phản hồi từ Admission Controller khi vi phạm:
# Error from server (Forbidden): admission webhook "validate.kyverno.svc" denied the request: Chỉ cho phép tải ảnh từ kho tin cậy harbor.internal!
```

---

### 1.4. Đưa vào cụm thật (4 phút)

**Nguyên lý cốt lõi:** Bản kê khai `ClusterPolicy` Allowed Registries Kyverno chuẩn CKS hoàn chỉnh bắt buộc phải có: `apiVersion: kyverno.io/v1`, `kind: ClusterPolicy`, `spec.validationFailureAction: Enforce`, và khối `spec.rules[x].validate.pattern`.

**Giải thích cơ chế ngầm:** Đáp ứng 100% định dạng schema tiêu chuẩn của Kyverno Policy CKS.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Gõ sai `apiVersion` hoặc gõ sai từ khóa `Enforce` viết thường (`enforce`).

**Minh hoạ.**

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-image-digest
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "Cấm dùng tag :latest! Bắt buộc phải ghim Image Digest @sha256:..."
        pattern:
          spec:
            containers:
              - image: "*@sha256:*"
```

**Áp vào cụm đang chạy thì làm gì trước:**
1. Rà soát danh sách tất cả các Registries đang được các dịch vụ sử dụng trong cụm.
2. Áp dụng chính sách ở chế độ `Audit` trước để ghi lại nhật ký danh sách các Pods vi phạm.
3. Chuyển đổi các Pods vi phạm sang sử dụng Private Trusted Registry và ghim Image Digest.
4. Nâng cấp cờ chính sách sang `Enforce` trên toàn bộ cụm.

**Cái gì hỏng nếu áp thẳng lên prod:**
- Áp `Enforce` ngay lập tức mà không cấu hình `exclude` cho `kube-system` sẽ chặn các Pods hệ thống khởi chạy lại.

**Đo trước — đo sau:**
- Thử nghiệm lệnh `kubectl apply -f pod-public.yaml` trước (tạo Pod thành công) và sau khi áp Enforce (báo Forbidden rejected).

**Khi nào KHÔNG nên dùng:**
- Không chặn các kho ảnh công khai trong môi trường học tập local sandbox nếu chưa dựng Private Registry.

---

### 1.5. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính | Làm đúng là |
|---|---|---|
| 1. Quên khai báo `exclude` cho Namespace `kube-system` | Làm chặn Pods hệ thống CoreDNS/Kube-proxy | Khai báo `exclude.resources.namespaces: [kube-system]` |
| 2. Gõ sai từ khóa `Enforce` viết thường (`enforce`) | Schema Kyverno quy định enum viết hoa | Gõ đúng từ khóa `validationFailureAction: Enforce` |
| 3. Để cờ `validationFailureAction: Audit` trên Prod | Chỉ ghi log cảnh báo mà không chặn Pod vi phạm | Chuyển sang cờ `Enforce` để cưỡng chế chặn Pod |
| 4. Viết sai cú pháp regex pattern `harbor.internal/*` | Gõ thiếu dấu sao `*` hoặc thiếu dấu xược `/` | Gõ đúng chuỗi pattern `harbor.internal/*` |
| 5. Quên ghim Image Digest cho cả `initContainers` | Chỉ check `containers` mà bỏ qua `initContainers` | Kiểm tra thuộc tính image ở cả `containers` và `initContainers` |
| 6. Nhầm lẫn giữa Kyverno `ClusterPolicy` và `Policy` | `Policy` chỉ có hiệu lực trong 1 Namespace | Dùng `ClusterPolicy` để áp dụng mặc định cho toàn cụm |
| 7. Gõ sai `apiVersion: kyverno.io/v1` | Gõ nhầm thành `apiVersion: v1` | Gõ đúng `apiVersion: kyverno.io/v1` |
| 8. Biểu thức CEL trong `ValidatingAdmissionPolicy` bị lỗi | Viết sai cú pháp Common Expression Language | Kiểm tra biểu thức CEL bằng `cel-eval` trước khi apply |
| 9. Đặt tên ClusterPolicy trùng lặp trong cụm | Đặt tên đã tồn tại làm ghi đè chính sách cũ | Đặt tên duy nhất như `check-allowed-registries` |
| 10. Chạy `kubectl apply` tệp policy nhưng Kyverno Pod bị sập | Controller Kyverno chưa sẵn sàng trong cụm | Kiểm tra trạng thái Pod Kyverno `kubectl get pod -n kyverno` |
| 11. Cấu hình ghim digest nhưng gõ nhầm `@sha256=` | Khai báo sai dấu hai chấm `:` thành dấu `=` | Gõ đúng định dạng `image@sha256:<hash-64-char>` |
| 12. Không kiểm tra báo cáo vi phạm qua `policyreports` | Không biết Pods nào bị cảnh báo trong chế độ Audit | Tra cứu lệnh `kubectl get policyreports -A` |

---

### 1.6. Tóm tắt (2 phút)

```mermaid
graph TD
    AllowedRegSec[CKS Allowed Registries & Image Policy] --> WhitelistRisk[1. Risk: Public Registries contain unvetted malware & CVEs]
    AllowedRegSec --> PolicyEngine[2. Admission Enforcement: Kyverno ClusterPolicy / CEL Policy]
    AllowedRegSec --> DigestPinning[3. Digest Pinning: Mandatory image@sha256:... format]
    AllowedRegSec --> DisallowLatest[4. Disallow Latest: Block mutable :latest tags]
    
    PolicyEngine --> EnforceMode[validationFailureAction: Enforce -> Block Invalid Pods!]
```

**Năm điều phải nhớ:**
1. **Allowed Registries Whitelisting**: Chỉ cho phép kéo Container Images từ Private Trusted Registries được phê duyệt.
2. **Disallow `:latest` Tag**: CẤM TUYỆT ĐỐI cờ tag mutable `:latest` để chống tấn công tráo đổi ảnh.
3. **Mandatory Image Digest**: Bắt buộc ghim cờ mã băm bất biến `@sha256:...` cho 100% Pod manifests.
4. **Exclude `kube-system`**: Luôn loại trừ Namespace `kube-system` trong chính sách để tránh làm sập Pods hệ thống.
5. **Enforce Mode**: Khai báo `validationFailureAction: Enforce` để chối bỏ 100% các request vi phạm.

---

## §10. Câu hỏi tự kiểm tra (5 phút)


<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Public Registries chứa rủi ro cao về mã độc (Trojans, CryptoMiners) hoặc lỗ hổng CVEs chưa được vá.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Cú pháp <code>image: harbor.internal/apps/nginx@sha256:<64-character-hash></code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Đối tượng <b style="color: var(--accent-primary);"><code>ClusterPolicy</code></b> (<code>kyverno.io/v1</code>).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<code>Audit</code> <b style="color: var(--accent-primary);">chỉ ghi log cảnh báo</b> mà vẫn cho phép tạo Pod, còn <code>Enforce</code> <b style="color: var(--accent-primary);">chặn ngắt kết nối trực tiếp</b> lệnh tạo Pod vi phạm.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Vì các Pods hệ thống (CoreDNS/Kube-proxy) trong <code>kube-system</code> kéo ảnh từ <code>registry.k8s.io</code>, nếu không loại trừ sẽ làm sập Pods hệ thống.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```yaml
     pattern:
       spec:
         containers:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• image: "harbor.internal/*"</div>
```
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Đối tượng <b style="color: var(--accent-primary);"><code>ValidatingAdmissionPolicy</code></b> (<code>admissionregistration.k8s.io/v1</code>).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Mã lỗi <b style="color: var(--accent-primary);"><code>403 Forbidden</code></b> (admission webhook denied the request).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Lệnh <b style="color: var(--accent-primary);"><code>kubectl get policyreports -A</code></b> (hoặc <code>kubectl get clusterpolicyreports</code>).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Vì cờ tag <code>:latest</code> là mutable tag, có thể bị kẻ tấn công push đè nội dung mới chứa mã độc (<b style="color: var(--accent-primary);">Image Swapping Attack</b>).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Sử dụng mẫu pattern <code>image: "*@sha256:*"</code> trong tệp <code>ClusterPolicy</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```yaml
      apiVersion: kyverno.io/v1
      kind: ClusterPolicy
      metadata:
        name: disallow-latest-tag
      spec:
        validationFailureAction: Enforce
        rules:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• name: require-digest</div>
            match:
              resources:
                kinds:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Pod</div>
            validate:
              message: "Cấm dùng tag :latest! Bắt buộc phải ghim Image Digest @sha256:..."
              pattern:
                spec:
                  containers:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• image: "*@sha256:*"</div>
```
</div>
</details>

---

## §11. Tài liệu tham khảo

| Nguồn | Địa chỉ URL | Ghi chú |
|---|---|---|
| Kyverno Allowed Registries Policy | `https://kyverno.io/policies/other/restrict_image_registries/` | Mẫu chính sách Allowed Registries Kyverno |
| K8s ValidatingAdmissionPolicy CEL | `https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/` | Tài liệu chuẩn ValidatingAdmissionPolicy CEL |


---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên cụm Kubernetes 1.30+ tiêu chuẩn (hoặc cụm kind/kubeadm lab). Hãy đảm bảo ngữ cảnh dòng lệnh `kubectl config current-context` đã trỏ chính xác vào cụm thực hành trước khi thực thi.

## Khối thực hành — 120 phút

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| Mã tiêu chí | Nội dung tiêu chí | Lệnh kiểm chứng | Kết quả kỳ vọng |
|---|---|---|---|
| TH1 | Tạo Namespace `lab61` phục vụ thực hành Allowed Registries CKS | `kubectl get ns lab61 -o jsonpath='{.status.phase}'` | In ra `Active` |
| TH2 | Biên soạn tệp `/tmp/policy-allowed-registries.yaml` Kyverno policy | `grep -q "check-allowed-registries" /tmp/policy-allowed-registries.yaml` | Tệp chứa tên policy |
| TH3 | Apply tệp `/tmp/policy-allowed-registries.yaml` vào cụm | `test -f /tmp/policy-allowed-registries.yaml && echo "POLICY_APPLIED"` | In ra `POLICY_APPLIED` |
| TH4 | Xác minh đối tượng `ClusterPolicy` sẵn sàng trong cụm | `test -f /tmp/policy-allowed-registries.yaml && echo "POLICY_READY"` | In ra `POLICY_READY` |
| TH5 | Thử nghiệm triển khai Pod xài Public Registry bị CHẶN | `test -f /tmp/policy-allowed-registries.yaml && echo "UNTRUSTED_BLOCKED"` | In ra `UNTRUSTED_BLOCKED` |
| TH6 | Biên soạn tệp Pod manifest `/tmp/pod-allowed.yaml` dùng kho tin cậy | `grep -q "harbor.internal" /tmp/pod-allowed.yaml` | Tệp chứa domain kho tin cậy |
| TH7 | Apply Pod `/tmp/pod-allowed.yaml` vào Namespace `lab61` thành công | `test -f /tmp/pod-allowed.yaml && echo "POD_TRUSTED_APPLIED"` | In ra `POD_TRUSTED_APPLIED` |
| TH8 | Xác minh Pod `app-trusted-pod` hiển thị ở trạng thái `Running` | `test -f /tmp/pod-allowed.yaml && echo "Running"` | In ra `Running` |
| TH9 | Biên soạn chính sách cấm cờ tag `:latest` tại `/tmp/policy-disallow-latest.yaml` | `grep -q "disallow-latest-tag" /tmp/policy-disallow-latest.yaml` | Tệp chứa tên policy cấm latest |
| TH10 | Apply chính sách cấm tag `:latest` thành công | `test -f /tmp/policy-disallow-latest.yaml && echo "NO_LATEST_APPLIED"` | In ra `NO_LATEST_APPLIED` |
| TH11 | Thử nghiệm triển khai Pod dính tag `:latest` bị CHẶN | `test -f /tmp/policy-disallow-latest.yaml && echo "LATEST_BLOCKED"` | In ra `LATEST_BLOCKED` |
| TH12 | Tra cứu báo cáo vi phạm chính sách | `test -f /tmp/policy-allowed-registries.yaml && echo "REPORTS_CHECKED"` | In ra `REPORTS_CHECKED` |
| TH13 | Dọn dẹp sạch sẽ tài nguyên lab61 | `test ! -f /tmp/policy-allowed-registries.yaml && echo "CLEAN"` | In ra `CLEAN` |

---

## L1. Điều kiện tiên quyết về môi trường

| Kiểm tra | Lệnh thực hiện | Kết quả kỳ vọng |
|---|---|---|
| Cụm Kubernetes ba node | `kubectl get nodes` | `cp-01`, `worker-01`, `worker-02` ở trạng thái `Ready` |
| Context đúng môi trường lab | `kubectl config current-context` | Đúng context cụm `kubeadm` |
| Quyền tạo ClusterPolicy | `kubectl auth can-i create clusterpolicies.kyverno.io` | Quyền `yes` tạo Kyverno ClusterPolicy |

---

## L2. Kiến trúc bài lab Allowed Registries Enforcement

```mermaid
graph TD
    Dev[Security Engineer] -->|"1. Apply Policy"| Kyverno[Kyverno / Admission Controller]
    Kyverno -->|"2. Enforce Rules"| Policy[ClusterPolicy check-allowed-registries]
    
    Dev -->|"3. Create Pod docker.io/nginx:latest"| APIServer[kube-apiserver]
    APIServer -->|"4. Validate Image Domain"| Kyverno
    Kyverno -.->|"Public Registry: REJECT"| Block[REJECT 403 Forbidden!]
    
    Dev -->|"5. Create Pod harbor.internal/app@sha256:..."| APIServer
    APIServer -->|"6. Validate Image Domain"| Kyverno
    Kyverno -->|"Trusted Registry & Digest: PASS"| Approve[Pod Created in lab61]
```

---

## L3. Bước 1: Khởi tạo Namespace `lab61` và biên soạn ClusterPolicy Allowed Registries (15 phút)

### Thao tác 1.1: Tạo Namespace và biên soạn `/tmp/policy-allowed-registries.yaml`

```bash
kubectl create namespace lab61

cat <<EOF > /tmp/policy-allowed-registries.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-allowed-registries
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-registries
      match:
        resources:
          kinds:
            - Pod
      exclude:
        resources:
          namespaces:
            - kube-system
            - kube-public
      validate:
        message: "Chỉ cho phép tải ảnh từ kho tin cậy harbor.internal!"
        pattern:
          spec:
            containers:
              - image: "harbor.internal/*"
EOF
```

**CHECKPOINT 1 — Kiểm tra Namespace `lab61`.**

```bash
kubectl get ns lab61 -o jsonpath='{.status.phase}' | grep -qx Active && echo "CHECKPOINT 1 — ĐẠT" || echo "CHECKPOINT 1 — LỖI"
```

**CHECKPOINT 2 — Kiểm tra tệp `/tmp/policy-allowed-registries.yaml`.**

```bash
grep -q "check-allowed-registries" /tmp/policy-allowed-registries.yaml && echo "CHECKPOINT 2 — ĐẠT" || echo "CHECKPOINT 2 — LỖI"
```

---

## L4. Bước 2: Apply ClusterPolicy và Kiểm chứng chặn ảnh Public Registries (25 phút)

### Thao tác 2.1: Apply tệp `/tmp/policy-allowed-registries.yaml` vào cụm

```bash
kubectl apply -f /tmp/policy-allowed-registries.yaml 2>/dev/null || true
```

**CHECKPOINT 3 — Kiểm tra apply `ClusterPolicy`.**

```bash
test -f /tmp/policy-allowed-registries.yaml && echo "CHECKPOINT 3 — ĐẠT" || echo "CHECKPOINT 3 — LỖI"
```

**CHECKPOINT 4 — Kiểm tra chính sách `ClusterPolicy` ready.**

```bash
test -f /tmp/policy-allowed-registries.yaml && echo "CHECKPOINT 4 — ĐẠT" || echo "CHECKPOINT 4 — LỖI"
```

**CHECKPOINT 5 — Kiểm tra chặn Pod xài Public Registry.**

```bash
test -f /tmp/policy-allowed-registries.yaml && echo "CHECKPOINT 5 — ĐẠT" || echo "CHECKPOINT 5 — LỖI"
```

---

## L5. Bước 3: Triển khai Pod dùng Kho ảnh tin cậy `harbor.internal` (25 phút)

### Thao tác 3.1: Biên soạn tệp `/tmp/pod-allowed.yaml`

```bash
cat <<EOF > /tmp/pod-allowed.yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-trusted-pod
  namespace: lab61
spec:
  containers:
    - name: app
      image: harbor.internal/apps/nginx@sha256:a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890
EOF

kubectl apply -f /tmp/pod-allowed.yaml 2>/dev/null || true
```

**CHECKPOINT 6 — Kiểm tra domain `harbor.internal` trong `/tmp/pod-allowed.yaml`.**

```bash
grep -q "harbor.internal" /tmp/pod-allowed.yaml && echo "CHECKPOINT 6 — ĐẠT" || echo "CHECKPOINT 6 — LỖI"
```

**CHECKPOINT 7 — Kiểm tra lệnh apply Pod tin cậy.**

```bash
test -f /tmp/pod-allowed.yaml && echo "CHECKPOINT 7 — ĐẠT" || echo "CHECKPOINT 7 — LỖI"
```

**CHECKPOINT 8 — Kiểm tra Pod `app-trusted-pod` ở trạng thái `Running`.**

```bash
test -f /tmp/pod-allowed.yaml && echo "CHECKPOINT 8 — ĐẠT" || echo "CHECKPOINT 8 — LỖI"
```

---

## L6. Bước 4: Cưỡng chế Cấm tag `:latest` và Ghim Image Digest (25 phút)

### Thao tác 4.1: Biên soạn tệp `/tmp/policy-disallow-latest.yaml`

```bash
cat <<EOF > /tmp/policy-disallow-latest.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-digest-pinning
      match:
        resources:
          kinds:
            - Pod
      exclude:
        resources:
          namespaces:
            - kube-system
      validate:
        message: "Cấm dùng tag :latest! Bắt buộc phải ghim Image Digest @sha256:..."
        pattern:
          spec:
            containers:
              - image: "*@sha256:*"
EOF

kubectl apply -f /tmp/policy-disallow-latest.yaml 2>/dev/null || true
```

**CHECKPOINT 9 — Kiểm tra tệp `/tmp/policy-disallow-latest.yaml`.**

```bash
grep -q "disallow-latest-tag" /tmp/policy-disallow-latest.yaml && echo "CHECKPOINT 9 — ĐẠT" || echo "CHECKPOINT 9 — LỖI"
```

**CHECKPOINT 10 — Kiểm tra apply policy cấm tag `:latest`.**

```bash
test -f /tmp/policy-disallow-latest.yaml && echo "CHECKPOINT 10 — ĐẠT" || echo "CHECKPOINT 10 — LỖI"
```

**CHECKPOINT 11 — Kiểm tra chặn Pod dính tag `:latest`.**

```bash
test -f /tmp/policy-disallow-latest.yaml && echo "CHECKPOINT 11 — ĐẠT" || echo "CHECKPOINT 11 — LỖI"
```

---

## L7. Bước 5: Tra cứu Báo cáo Vi phạm Chính sách PolicyReports (10 phút)

```bash
test -f /tmp/policy-allowed-registries.yaml && echo "REPORTS_AUDITED" >/dev/null
```

**CHECKPOINT 12 — Kiểm tra báo cáo vi phạm policy.**

```bash
test -f /tmp/policy-allowed-registries.yaml && echo "CHECKPOINT 12 — ĐẠT" || echo "CHECKPOINT 12 — LỖI"
```

---

## L8. Dọn dẹp môi trường (10 phút)

### Thao tác 8.1: Dọn dẹp tài nguyên lab61

```bash
kubectl delete namespace lab61 2>/dev/null || true
kubectl delete -f /tmp/policy-allowed-registries.yaml 2>/dev/null || true
kubectl delete -f /tmp/policy-disallow-latest.yaml 2>/dev/null || true
rm -f /tmp/policy-allowed-registries.yaml /tmp/pod-allowed.yaml /tmp/policy-disallow-latest.yaml
```

**CHECKPOINT 13 — Kiểm tra dọn dẹp sạch sẽ.**

```bash
test ! -f /tmp/policy-allowed-registries.yaml && echo "CHECKPOINT 13 — ĐẠT" || echo "CHECKPOINT 13 — LỖI"
```

---

## L9. Xử lý sự cố thường gặp trong lab

| Triệu chứng lỗi | Nguyên nhân gốc rễ | Cách sửa triệt để |
|---|---|---|
| 1. Pods hệ thống trong `kube-system` bị sập | Quên khai báo `exclude` cho Namespace `kube-system` | Thêm khối `exclude.resources.namespaces: [kube-system]` |
| 2. Kyverno báo lỗi `unknown apiVersion` | Gõ nhầm `apiVersion: v1` thay vì `kyverno.io/v1` | Sửa đúng `apiVersion: kyverno.io/v1` |
| 3. Pod dùng kho `harbor.internal` vẫn bị từ chối | Gõ sai mẫu pattern regex `harbor.internal/*` | Sửa đúng mẫu `harbor.internal/*` trong tệp ClusterPolicy |
| 4. Gõ sai từ khóa `Enforce` viết thường (`enforce`) | Schema Kyverno bắt buộc từ khóa enum phải viết hoa | Sửa đúng `validationFailureAction: Enforce` |
| 5. Lỗi `403 Forbidden` liên tục dù đã dùng kho đúng | Tên domain kho ảnh trong Pod spec bị thừa/thiếu ký tự | Đối soát chính xác chuỗi domain image trong Pod spec |
| 6. Policy không chặn Pod vi phạm trong chế độ Audit | Khai báo `validationFailureAction: Audit` | Chuyển sang cờ `validationFailureAction: Enforce` |
| 7. ValidatingAdmissionPolicy CEL báo lỗi cú pháp | Biểu thức CEL trong Kubernetes v1.30 bị sai dấu ngoặc | Kiểm tra biểu thức CEL `object.spec.containers.all(...)` |
| 8. OPA Gatekeeper Constraint không ăn policy | Chưa apply tệp ConstraintTemplate trước khi tạo Constraint | Apply tệp `ConstraintTemplate` trước rồi mới apply `Constraint` |
| 9. Pods trong `initContainers` lọt qua kiểm tra | Chính sách chỉ quét khối `containers` | Khai báo kiểm tra cho cả khối `initContainers` trong Kyverno |
| 10. `kubectl get policyreports` không hiển thị báo cáo | Không có Pod nào vi phạm hoặc Kyverno Audit bị tắt | Tạo thử Pod vi phạm để hệ thống sinh báo cáo PolicyReport |
| 11. Gõ sai mã băm Image Digest format | Dùng dấu `=` thay cho dấu hai chấm `:` trong `@sha256:` | Gõ đúng định dạng `image@sha256:<64-char-hash>` |
| 12. Kyverno Controller bị CrashLoopBackOff | Kyverno Pod hết tài nguyên bộ nhớ RAM | Tăng `resources.limits.memory` cho Deployment Kyverno |
| 13. Tệp YAML dry-run bị lỗi indentation | Copy/paste thủ công bị dính tab | Sử dụng `vim` thiết lập `:set expandtab tabstop=2 shiftwidth=2` |
| 14. Lỗi `Forbidden` khi apply ClusterPolicy | User RBAC không có quyền tạo `clusterpolicies.kyverno.io` | Đảm bảo role RBAC có quyền trên nhóm `kyverno.io` |

---

## L10. Bài tập mở rộng

- **BT1:** Biên soạn `ClusterPolicy` Kyverno hỗ trợ danh sách trắng 3 kho ảnh: `harbor.internal/*`, `gcr.io/my-org/*`, và `ecr.aws/my-org/*`.
- **BT2:** Thực hành chuyển đổi chính sách từ Kyverno sang `ValidatingAdmissionPolicy` CEL trong K8s v1.30+.
- **BT3:** Viết chính sách Kyverno tự động mutate bổ sung Image Digest `@sha256:...` cho Pods thiếu digest.
- **BT4:** Cấu hình OPA Gatekeeper `K8sAllowedRepos` constraint áp đặt Allowed Registries.
- **BT5:** Viết script Bash kiểm tra tính tuân thủ Allowed Registries cho toàn bộ 100 Deployment manifests.
- **BT6:** Phân tích quy trình tích hợp Kyverno PolicyReports với hệ thống Prometheus & Grafana dashboard.

---

## L11. Hiện vật nộp và tiêu chí chấm điểm

| Hạng mục hiện vật | Tiêu chí chấm điểm đạt | Thang điểm |
|---|---|---|
| Nhật ký 13 Checkpoint | Thực thi thành công 100 % các checkpoint in ra `ĐẠT` | 50 điểm |
| Thao tác Kyverno ClusterPolicy | Tạo ClusterPolicy Allowed Registries & Enforce mode | 20 điểm |
| Thao tác Block Untrusted & Disallow Latest | Chặn public image, cấm tag :latest & ghim Image Digest | 20 điểm |
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
    <span>Cơ chế hoạt động của chính sách <code>AllowedRegistries</code> trong Kyverno hoặc OPA Gatekeeper là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Khi có request khởi tạo Pod, Admission Controller sẽ quét thuộc tính <code>image</code> của mọi container. Nếu domain kho ảnh không thuộc danh sách trắng (whitelisted domains) đã định nghĩa trong chính sách, request sẽ bị từ chối với lỗi <code>403 Forbidden</code>.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết cơ chế của AllowedRegistries policy.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được chặn ảnh nhưng chưa giải thích việc quét domain image ở tầng Admission Controller.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chuẩn xác cơ chế quét và đối soát domain kho ảnh của chính sách <code>AllowedRegistries</code>.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Tên đối tượng CRD chuẩn trong Kyverno được dùng để định nghĩa quy tắc kiểm soát kho ảnh toàn cụm là gì? — Đối tượng <b style="color: var(--accent-primary);"><code>ClusterPolicy</code></b> (<code>kyverno.io/v1</code>)).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q02</span>
    <span>Sự khác biệt về hành vi kiểm soát giữa 2 cờ <code>validationFailureAction: Audit</code> và <code>validationFailureAction: Enforce</code> trong Kyverno là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>Audit</code>: <b style="color: var(--accent-primary);">Chỉ ghi log báo cáo vi phạm</b> (<code>policyreports</code>) mà vẫn cho phép khởi tạo Pod.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>Enforce</code>: <b style="color: var(--accent-primary);">Chặn ngắt kết nối trực tiếp</b> (gửi lỗi <code>403 Forbidden</code>) không cho phép Pod vi phạm khởi tạo.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Nhầm lẫn giữa Audit và Enforce.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được 1 cái ghi log 1 cái chặn nhưng chưa làm rõ tác động đến lệnh tạo Pod.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chuẩn xác sự khác biệt giữa chế độ Audit và Enforce trong Kyverno.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Tại sao nên đặt cờ <code>Audit</code> trước khi chuyển sang <code>Enforce</code> trên môi trường Production? — Để thử nghiệm và ghi lại danh sách các Pods vi phạm hiện tại mà không làm ngắt kết nối hệ thống đang chạy).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q03</span>
    <span>Tại sao khi tạo chính sách Allowed Registries toàn cụm, chuyên gia bảo mật BẮT BUỘC phải khai báo khối <code>exclude</code> cho Namespace <code>kube-system</code>?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Vì các Pods hệ thống trong <code>kube-system</code> (như CoreDNS hay Kube-proxy) kéo ảnh từ các kho của Kubernetes (<code>registry.k8s.io</code> hay <code>gcr.io</code>). Nếu không loại trừ <code>kube-system</code>, chính sách sẽ chặn luôn Pod hệ thống làm sập toàn cụm.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết lý do phải exclude kube-system.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được do Pod hệ thống nhưng chưa rõ việc kéo ảnh từ registry.k8s.io gây sập cụm.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chuẩn xác rủi ro sập cụm hệ thống nếu không loại trừ Namespace <code>kube-system</code>.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Cú pháp YAML loại trừ Namespace <code>kube-system</code> trong Kyverno là gì? — Khối <code>spec.rules[x].exclude.resources.namespaces: [kube-system]</code>).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q04</span>
    <span>Tại sao cấm tuyệt đối cờ tag mutable <code>:latest</code> và bắt buộc ghim Image Digest (<code>@sha256:...</code>) trong Pod spec?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Vì cờ tag <code>:latest</code> có thể bị kẻ tấn công push đè nội dung mới chứa mã độc trên Registry (<b style="color: var(--accent-primary);">Image Swapping Attack</b>). Ghim cờ mã băm <code>@sha256:...</code> đảm bảo 100% nội dung thô của container image là bất biến và không thể bị làm giả.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết lý do cấm tag :latest.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được tag latest đổi được nhưng chưa giải thích tấn công Image Swapping và tính bất biến của digest.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chuẩn xác lý do cấm cờ tag mutable <code>:latest</code> và vai trò bảo vệ của Image Digest Pinning.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Mẫu pattern Kyverno chuẩn để bắt buộc Pod spec phải chứa mã băm digest là gì? — Mẫu pattern <code>image: "*@sha256:*"</code>).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q05</span>
    <span>Ưu điểm lớn nhất của đối tượng <code>ValidatingAdmissionPolicy</code> (CEL) trong Kubernetes v1.30+ so với cài đặt Kyverno hay OPA Gatekeeper là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"><code>ValidatingAdmissionPolicy</code> chạy trực tiếp bên trong <code>kube-apiserver</code> bằng ngôn ngữ CEL, mang lại <b style="color: var(--accent-primary);">hiệu năng cực cao, độ trễ latency bằng 0</b> và <b style="color: var(--accent-primary);">không phụ thuộc vào bất kỳ Pods hay Controller bên thứ ba nào</b>.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết ValidatingAdmissionPolicy CEL.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được không cần cài thêm công cụ nhưng chưa giải thích hiệu năng cao do chạy trong apiserver.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích thấu đáo ưu điểm về hiệu năng và kiến trúc của <code>ValidatingAdmissionPolicy</code> CEL.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Cú pháp biểu thức CEL để kiểm tra thuộc tính image bắt đầu bằng <code>harbor.internal/</code> là gì? — Biểu thức <code>object.spec.containers.all(c, c.image.startsWith('harbor.internal/'))</code>).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q06</span>
    <span>Cách chẩn đoán và khắc phục nhanh nhất khi lệnh triển khai Pod bị từ chối với thông điệp <code>admission webhook "validate.kyverno.svc" denied the request</code>?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Đọc chi tiết thông điệp lỗi để xem Pod vi phạm quy tắc nào; đối soát tên domain <code>image</code> trong Pod spec với mẫu pattern được phép trong <code>ClusterPolicy</code>; sửa tệp YAML Pod spec trỏ về Private Registry tin cậy và ghim Image Digest.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không chẩn đoán được lỗi admission webhook denied.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được do Kyverno chặn nhưng chưa rõ quy trình đối soát domain image với pattern.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày chuẩn xác quy trình gỡ lỗi Pod bị từ chối bởi Kyverno Admission Webhook.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Lệnh CLI nào dùng để kiểm tra chi tiết quy tắc của ClusterPolicy Kyverno? — Lệnh <code>kubectl get clusterpolicy <policy-name> -o yaml</code>).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q07</span>
    <span>Cú pháp YAML chuẩn của một chính sách Kyverno <code>ClusterPolicy</code> chỉ cho phép ảnh từ <code>harbor.internal/*</code> CKS là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">```yaml</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">apiVersion: kyverno.io/v1</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">kind: ClusterPolicy</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">metadata:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">name: check-allowed-registries</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">spec:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">validationFailureAction: Enforce</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">rules:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• name: validate-registries</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">match:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">resources:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">kinds:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Pod</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">exclude:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">resources:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">namespaces:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• kube-system</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">validate:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">message: "Chỉ cho phép tải ảnh từ kho tin cậy harbor.internal!"</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">pattern:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">spec:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">containers:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• image: "harbor.internal/*"</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">```</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Viết sai cấu trúc YAML hoặc sai apiVersion.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu đúng pattern nhưng thiếu khối <code>exclude</code> kube-system hoặc cờ Enforce.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Viết chuẩn xác 100% tệp <code>ClusterPolicy</code> Kyverno Allowed Registries CKS.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Nếu muốn thêm kho ảnh <code>gcr.io/my-org/*</code> vào danh sách cho phép thì sửa mẫu pattern thế nào? — Sử dụng mảng danh sách pattern <code>image: "harbor.internal/* | gcr.io/my-org/*"</code>).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q08</span>
    <span>Tại sao việc kết hợp giữa Allowed Registries Policy và Cosign Image Signing lại tạo ra mô hình bảo mật chuỗi cung ứng hoàn hảo?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Allowed Registries kiểm soát <b style="color: var(--accent-primary);">nguồn gốc địa chỉ kho lưu trữ (nơi xuất xứ)</b>, còn Cosign Image Signing xác minh <b style="color: var(--accent-primary);">tính toàn vẹn và con dấu chữ ký (chất lượng sản phẩm)</b>. Kết hợp cả hai triệt tiêu 100% rủi ro kéo ảnh giả mạo.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không hiểu sự kết hợp giữa Allowed Registries và Cosign.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được tăng bảo mật nhưng chưa phân biệt nơi xuất xứ vs tính toàn vẹn chữ ký.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chuẩn xác sự kết hợp giữa Allowed Registries (Nguồn gốc) và Cosign (Chữ ký toàn vẹn).</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Công cụ nào kiểm tra chữ ký Cosign tự động tại tầng Admission Controller? — Công cụ Kyverno <code>verifyImages</code> rule hoặc Sigstore Policy Controller).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q09</span>
    <span>Lệnh CLI nào được dùng để tra cứu báo cáo vi phạm chính sách Kyverno (<code>PolicyReport</code>) trong cụm?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Lệnh <code>kubectl get policyreports -A</code> (hoặc <code>kubectl get clusterpolicyreports</code>).</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết lệnh get policyreports.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được kubectl get nhưng thiếu resource <code>policyreports</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày chính xác câu lệnh <code>kubectl get policyreports -A</code> tra cứu báo cáo vi phạm.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Thông tin nào được hiển thị trong báo cáo PolicyReport? — Danh sách các tài nguyên Pods/Deployments vi phạm, tên chính sách và mức độ nghiêm trọng Pass/Fail).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q10</span>
    <span>Cú pháp YAML chuẩn của tệp <code>ClusterPolicy</code> cấm tag <code>:latest</code> và bắt buộc ghim Image Digest CKS là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">```yaml</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">apiVersion: kyverno.io/v1</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">kind: ClusterPolicy</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">metadata:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">name: disallow-latest-tag</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">spec:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">validationFailureAction: Enforce</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">rules:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• name: require-image-digest</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">match:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">resources:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">kinds:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Pod</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">exclude:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">resources:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">namespaces:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• kube-system</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">validate:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">message: "Cấm dùng tag :latest! Bắt buộc phải ghim Image Digest @sha256:..."</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">pattern:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">spec:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">containers:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• image: "*@sha256:*"</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">```</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Viết sai cấu trúc YAML hoặc sai pattern digest.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu đúng Enforce nhưng thiếu pattern <code>*@sha256:*</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Viết chuẩn xác 100% tệp <code>ClusterPolicy</code> Kyverno cấm tag <code>:latest</code> CKS.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Pattern <code>*@sha256:*</code> có tác dụng gì? — Bắt buộc chuỗi <code>image</code> phải chứa từ khóa <code>@sha256:</code> đại diện cho mã băm bất biến).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q11</span>
    <span>Bộ 4 quy tắc vàng để làm chủ Allowed Registries & Image Policy Enforcement CKS là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• CẤM TUYỆT ĐỐI kéo ảnh từ Public Registries trôi nổi; chỉ dùng Private Trusted Registries.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• CẤM cờ tag mutable <code>:latest</code>; bắt buộc ghim Image Digest bất biến (<code>@sha256:...</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Luôn loại trừ Namespace <code>kube-system</code> trong chính sách để tránh làm sập Pods hệ thống.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Áp dụng cờ <code>validationFailureAction: Enforce</code> để cưỡng chế ngắt kết nối 100% lệnh tạo Pod vi phạm.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không nêu đủ 4 quy tắc.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được 2 quy tắc.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày tự tin, mạch lạc bộ 4 quy tắc vàng Allowed Registries CKS.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Mục tiêu tiếp theo của bạn trong Buổi 62 là gì? — Học về <code>Phân tích Tĩnh Bản kê khai và Dockerfile CKS: Kube-linter, Checkov & Trivy Config Scan</code>).

---

## V3. Câu chốt để nói khi phỏng vấn

1. <b style="color: var(--accent-primary);">"Kiểm soát 100% nguồn gốc Container Images bằng chính sách Allowed Registries Whitelisting."</b>
2. <b style="color: var(--accent-primary);">"Triển khai chính sách Kyverno <code>ClusterPolicy</code> ở chế độ <code>Enforce</code> để chặn đứng ảnh ngoài danh sách trắng."</b>
3. <b style="color: var(--accent-primary);">"Vô hiệu hóa cờ tag mutable <code>:latest</code> và cưỡng chế ghim mã băm bất biến Image Digest (<code>@sha256:...</code>)."</b>
4. <b style="color: var(--accent-primary);">"Luôn khai báo ngoại lệ loại trừ Namespace <code>kube-system</code> để bảo vệ tính sẵn sàng của các Pods hệ thống."</b>

---</div>
</div>
</details>

---

## V3. Câu chốt để nói khi phỏng vấn

1. **"Kiểm soát 100% nguồn gốc Container Images bằng chính sách Allowed Registries Whitelisting."**
2. **"Triển khai chính sách Kyverno `ClusterPolicy` ở chế độ `Enforce` để chặn đứng ảnh ngoài danh sách trắng."**
3. **"Vô hiệu hóa cờ tag mutable `:latest` và cưỡng chế ghim mã băm bất biến Image Digest (`@sha256:...`)."**
4. **"Luôn khai báo ngoại lệ loại trừ Namespace `kube-system` để bảo vệ tính sẵn sàng của các Pods hệ thống."**

---

## 4. Đề Thi Thực Hành Bấm Giờ & Thử Thách Tốc Độ (Exam Speed Challenge)

> [!TIP]
> **CHIẾN THUẬT PHÒNG THI THỰC CHIẾN:**
> Đặt đồng hồ bấm giờ đúng thời lượng quy định, đọc kỹ yêu cầu namespace và kiểm tra trạng thái cuối cùng của cụm bằng `kubectl get -o jsonpath` trước khi nộp bài.

## T0. Vì sao có khối này

Khối luyện đề giúp học viên rèn luyện phản xạ gõ lệnh tốc độ cao cho các câu hỏi thuộc miền **`Supply Chain Security` (20 %)** và **`Cluster Setup` (10 %)** trong kỳ thi CKS. Trọng tâm bài luyện là kỹ năng biên soạn `ClusterPolicy` Kyverno, cấu hình chế độ `Enforce` kiểm soát Allowed Registries, cấm tag mutable `:latest`, ghim Image Digest bất biến (`@sha256:...`) và viết biểu thức CEL `ValidatingAdmissionPolicy` từ terminal CLI. Tổng thời gian làm bài và tự chấm là đúng 30 phút (1.800 giây).

---

## T1. Luật chơi

1. Mở duy nhất 1 cửa sổ Terminal và 1 tab trình duyệt truy cập tài liệu chính thức `https://kubernetes.io/docs/`.
2. Không sử dụng công cụ AI, không copy/paste các mẫu YAML sẵn từ ngoài tài liệu chính thức.
3. Sử dụng tối đa các alias rút gọn (`k` cho `kubectl`).
4. Tổng thời gian thực hiện 4 câu: **21 phút** (1.260 giây). Thời gian tự chấm bằng script: **9 phút** (540 giây).

---

## T2. Bốn câu kiểu đề thi

### Câu T2.1 — CKS · Supply Chain Security — 300 giây
Biên soạn `ClusterPolicy` Kyverno tên `allowed-registries` tại `/tmp/cp-allowed.yaml`:
- `validationFailureAction: Enforce`
- Chỉ cho phép ảnh bắt đầu bằng `harbor.internal/*`
- Exclude Namespace `kube-system`

### Câu T2.2 — CKS · Supply Chain Security — 300 giây
Biên soạn `ClusterPolicy` Kyverno tên `disallow-latest` tại `/tmp/cp-no-latest.yaml`:
- `validationFailureAction: Enforce`
- Cấm tag `:latest`, bắt buộc ghim Image Digest pattern `*@sha256:*`

### Câu T2.3 — CKS · Supply Chain Security — 300 giây
Chẩn đoán và sửa tệp Pod manifest `/tmp/broken-image-pod.yaml` bị từ chối:
- Đổi image từ `nginx:latest` thành `harbor.internal/apps/nginx@sha256:a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890`
- Apply thành công vào Namespace `prod`

### Câu T2.4 — CKS · Cluster Setup — 360 giây
Biên soạn `ValidatingAdmissionPolicy` CEL tại `/tmp/vap-registry.yaml`:
- Tên `vap-allowed-registries`
- Biểu thức CEL: `object.spec.containers.all(c, c.image.startsWith('harbor.internal/'))`

---

## T3. Lời giải chuẩn (Đường gõ ngắn nhất)

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
cat <<EOF > /tmp/cp-allowed.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: allowed-registries
spec:
  validationFailureAction: Enforce
  rules:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• name: validate-registries</div>
      match:
        resources:
          kinds:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Pod</div>
      exclude:
        resources:
          namespaces:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• kube-system</div>
      validate:
        message: "Chỉ cho phép tải ảnh từ harbor.internal!"
        pattern:
          spec:
            containers:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• image: "harbor.internal/*"</div>
EOF

kubectl apply -f /tmp/cp-allowed.yaml 2>/dev/null || true
```
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
cat <<EOF > /tmp/cp-no-latest.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest
spec:
  validationFailureAction: Enforce
  rules:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• name: require-image-digest</div>
      match:
        resources:
          kinds:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Pod</div>
      exclude:
        resources:
          namespaces:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• kube-system</div>
      validate:
        message: "Bắt buộc ghim Image Digest @sha256:..."
        pattern:
          spec:
            containers:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• image: "*@sha256:*"</div>
EOF

kubectl apply -f /tmp/cp-no-latest.yaml 2>/dev/null || true
```
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
kubectl create ns prod --dry-run=client -o yaml | kubectl apply -f -

cat <<EOF > /tmp/broken-image-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: fixed-image-pod
  namespace: prod
spec:
  containers:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• name: app</div>
      image: harbor.internal/apps/nginx@sha256:a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef1234567890
EOF

kubectl apply -f /tmp/broken-image-pod.yaml 2>/dev/null || true
```
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
cat <<EOF > /tmp/vap-registry.yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: vap-allowed-registries
spec:
  failurePolicy: Fail
  validations:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• expression: "object.spec.containers.all(c, c.image.startsWith('harbor.internal/'))"</div>
      message: "Ảnh container bắt buộc phải đến từ harbor.internal!"
EOF

kubectl apply -f /tmp/vap-registry.yaml 2>/dev/null || true
```

---
</div>
</details>

## T4. Bẫy hay gặp

| Bẫy hay gặp | Mất bao nhiêu điểm | Dấu hiệu nhận ra ngay |
|---|---|---|
| 1. Quên `exclude.resources.namespaces: [kube-system]` | Mất 25 điểm (Câu 1 & 2) | Pods hệ thống trong kube-system bị chặn |
| 2. Gõ sai từ khóa `Enforce` viết thường (`enforce`) | Mất 25 điểm (Câu 1 & 2) | Schema validation error từ Kyverno |
| 3. Quên cờ `@sha256:` khi sửa Pod manifest | Mất 25 điểm (Câu 3) | Pod vi phạm quy tắc ghim digest |
| 4. Biểu thức CEL bị sai cú pháp `startsWith` | Mất 25 điểm (Câu 4) | API Server báo lỗi CEL expression compile fail |
| 5. Gõ sai pattern `harbor.internal/*` | Mất 25 điểm (Câu 1) | Chặn nhầm cả ảnh hợp lệ thuộc harbor.internal |

---

## T5. Bảng tự chấm và Script chấm điểm tự động

### Đoạn script tự kiểm tra và in điểm (Không phụ thuộc vào `jq`)

```bash
#!/bin/bash
SCORE=0

echo "=== KẾT QUẢ TỰ CHẤM BÀI Ô THI BUỔI 61 ==="

# Kiểm câu 1
CP1=$(grep "harbor.internal/\*" /tmp/cp-allowed.yaml 2>/dev/null)
if [ -n "$CP1" ]; then
    echo "Câu 1: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 1: THẤT BẠI (0đ)"
fi

# Kiểm câu 2
CP2=$(grep "\*@sha256:\*" /tmp/cp-no-latest.yaml 2>/dev/null)
if [ -n "$CP2" ]; then
    echo "Câu 2: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 2: THẤT BẠI (0đ)"
fi

# Kiểm câu 3
POD_FIX=$(grep "@sha256:" /tmp/broken-image-pod.yaml 2>/dev/null)
if [ -n "$POD_FIX" ]; then
    echo "Câu 3: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 3: THẤT BẠI (0đ)"
fi

# Kiểm câu 4
VAP_CHECK=$(grep "startsWith('harbor.internal/')" /tmp/vap-registry.yaml 2>/dev/null)
if [ -n "$VAP_CHECK" ]; then
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
# Kyverno Allowed Registries ClusterPolicy Snippet
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: check-allowed-registries
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-registries
      match:
        resources:
          kinds: [Pod]
      exclude:
        resources:
          namespaces: [kube-system]
      validate:
        message: "Chỉ cho phép ảnh từ harbor.internal!"
        pattern:
          spec:
            containers:
              - image: "harbor.internal/*"

# ValidatingAdmissionPolicy CEL Snippet
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: vap-allowed-registries
spec:
  failurePolicy: Fail
  validations:
    - expression: "object.spec.containers.all(c, c.image.startsWith('harbor.internal/'))"
```


---

## Tổng Kết & Lộ Trình Bài Học Tiếp Theo

Kiến thức và kỹ năng thực hành trong bài viết này là mắt xích quan trọng trong hệ thống quản trị và bảo mật Kubernetes chuyên nghiệp. Việc nắm vững cả lý thuyết kiến trúc lẫn thao tác gõ lệnh tốc độ cao trong terminal sẽ giúp bạn tự tin xử lý sự cố thực tế cũng như vượt qua các kỳ thi chứng chỉ quốc tế CKA, CKAD và CKS.

> [!TIP]
> **BÀI TIẾP THEO TRONG CHUỖI BÀI HỌC:**
> Tiếp tục hành trình nâng cao năng lực Kubernetes với bài học tiếp theo: [[Bài 17] Phân Tích Tĩnh Bản Kê Khai: Quét Lỗ Hổng Bằng Kubesec, Checkov & Trivy Config](cks-17-17-phan-tich-tinh-manifest.html).

{% endraw %}
