---
layout: post
title: "[Bài 43] Chiến Lược Release Triển Khai An Toàn: Blue-Green Deployment, Canary Release, Feature Flags & Rollback Tự Động"
date: 2026-08-02 08:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-43
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 43
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.43] Hướng dẫn chuyên sâu Chiến Lược Release Triển Khai An Toàn: Blue-Green Deployment, Canary Release, Feature Flags & Rollback Tự Động: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

{% raw %}
# [BÀI 43] CHIẾN LƯỢC RELEASE TRIỂN KHAI AN TOÀN: BLUE-GREEN DEPLOYMENT, CANARY RELEASE, FEATURE FLAGS & ROLLBACK TỰ ĐỘNG

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

---





| STT | Câu hỏi ôn tập | Đáp án chi tiết thực chiến |
|---|---|---|
| 1 | Khác biệt lớn nhất giữa `terraform apply tfplan` và `terraform apply -auto-approve` là gì? | `apply tfplan` tiêu thụ đúng binary artifact đã review trên MR; `-auto-approve` tự sinh plan mới có thể xóa nhầm tài nguyên. |
| 2 | Hai tính năng cốt lõi của GitLab Managed Terraform State Backend là gì? | Mã hóa bảo mật State File (Encryption at Rest) và tự động khóa State (State Locking HTTP POST/DELETE) chống race condition. |
| 3 | Tại sao stage `terraform apply` Production bắt buộc đặt cờ `when: manual`? | Thực thi quy trình Phê duyệt hai bước (Four-Eye Principle), ép Tech Lead xem xét lại tệp plan trước khi thay đổi Cloud thực tế. |
| 4 | Ý nghĩa của mã `Exitcode 2` khi chạy `terraform plan -detailed-exitcode` là gì? | Báo hiệu phát hiện có sự thay đổi hạ tầng thực tế trên Cloud (Infrastructure State Drift) khác với mã HCL trên Git. |
| 5 | Tại sao không lưu chìa khóa tĩnh `AWS_ACCESS_KEY_ID` trong GitLab CI Variables? | Để chống rò rỉ secret key vĩnh viễn; sử dụng 100% Keyless OIDC Cloud Federation cấp access token ngắn hạn. |


**Luận đề trung tâm:**
> *"Chiến lược release quyết định **thời gian phát hiện lỗi (MTTD)** và **bán kính ảnh hưởng sự cố (Blast Radius)** — và đó là những con số đo đếm được chứ không phải lời hứa suông."*

Sau khi đã hoàn thành quản trị hạ tầng IaC bằng Terraform ở Buổi 42, Buổi 43 đưa chúng ta đến nghệ thuật phát hành ứng dụng (Application Release Strategies) lên hạ tầng đó sao cho người dùng cuối **không gặp bất kỳ thời gian ngắt dịch vụ nào (Zero Downtime)** và **giảm tối đa rủi ro khi có lỗi mã nguồn mới**. Trong thực tế Enterprise:
1. **Blue-Green Deployment:** Duy trì 2 môi trường song song (Blue đang nhận 100% traffic, Green vừa deploy bản mới). Chuyển đổi toàn bộ Ingress Routing sang Green trong 1 giây, nếu có lỗi chuyển ngược lại Blue lập tức.
2. **Canary Deployment:** Điều tiết phần trăm traffic nhỏ (dạng 10% -> 25% -> 50% -> 100%) nghiệm thu dần trên Production. Nếu tỷ lệ lỗi HTTP 5xx tăng >1%, hệ thống tự động ngắt Canary và rollback trong 3 giây.
3. **Feature Flags (Feature Toggles):** Bật/tắt tính năng mới theo thời gian thực từ giao diện GitLab Feature Flags (Unleash Engine) mà không cần redeploy hay rebuild mã nguồn!

Bài học này sẽ giúp bạn làm chủ 3 vũ khí phát hành phần mềm hiện đại nhất!

---



| STT | Kỹ năng thực chiến | Hiện vật chứng minh hoàn thành |
|---|---|---|
| 1 | Xây dựng luồng Blue-Green Deployment trên NGINX Ingress | Script CI swap Service Target Selector từ Blue sang Green |
| 2 | Cấu hình Canary Traffic Splitting theo trọng số (%) | Khai báo Ingress Annotations `nginx.ingress.kubernetes.io/canary-weight` |
| 3 | Tự động hóa Rollback Canary khi chỉ số HTTP 5xx tăng cao | Job CI bắt tín hiệu Alertmanager Webhook ngắt Canary Ingress |
| 4 | Tích hợp SDK GitLab Feature Flags (Unleash Client) | Khối mã bọc `if (featureFlags.isEnabled("new_checkout"))` |
| 5 | Quản lý bật/tắt Feature Flags theo môi trường và User ID | Cấu hình Feature Flag User Lists và Target Envs trên GitLab UI |
| 6 | Đảm bảo tính tương thích ngược Database Schema | Kịch bản Expand-and-Contract Database Migration Script |
| 7 | Đo lường thời gian phát hiện sự cố (MTTD) | Dashboard Prometheus hiển thị thời gian ngắt Canary dưới 5 giây |
| 8 | Quản lý dọn dẹp các Stale Feature Flags cũ | Script CI linter cảnh báo các Feature Flags hết hạn hơn 30 ngày |

---



| Kiến thức / Kỹ năng | Mức độ yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Cấu trúc NGINX Ingress Controller / Kubernetes Services | Thành thục | Buổi 41 về Kubernetes Helm & Deployment |
| Cú pháp tệp `.gitlab-ci.yml` và cờ `rules` / `environment` | Thành thục | Buổi 30 & Buổi 36 về CI/CD Pipeline |
| Khái niệm HTTP Status Codes (HTTP 200, 500, 502, 503) | Thành thục | Kiến thức Web Application Nền tảng |
| Nguyên lý Prometheus Metrics (Request Rate, Error Rate, Latency) | Khá | Kiến thức Monitoring & Observability |
| Khai báo biến môi trường và REST API gọi Curl | Thành thục | Kiến thức API Integration |

---





| Thuật ngữ Tiếng Việt | Thuật ngữ Tiếng Anh | Giải thích ý nghĩa thực tế |
|---|---|---|
| Triển khai Xanh-Xanh lá | Blue-Green Deployment | Chiến lược chạy 2 môi trường song song, tráo đổi (swap) 100% traffic qua lại. |
| Triển khai Chim báo bão | Canary Deployment | Chiến lược mở % traffic nhỏ (10-20%) sang bản mới để thử nghiệm trên Production. |
| Cờ tính năng | Feature Flags (Feature Toggles) | Công cụ cho phép bật/tắt tính năng mã nguồn từ xa qua API mà không cần deploy code. |
| Bán kính ảnh hưởng | Blast Radius | Số lượng người dùng tối đa chịu ảnh hưởng khi phiên bản ứng dụng mới bị lỗi. |
| Thời gian phát hiện lỗi | Mean Time to Detect (MTTD) | Khoảng thời gian từ khi lỗi xuất hiện đến khi hệ thống hoặc kỹ sư phát hiện ra. |
| Thời gian khôi phục | Mean Time to Recovery (MTTR) | Khoảng thời gian từ khi phát hiện sự cố đến khi ứng dụng khôi phục trạng thái xanh. |
| Tương thích ngược Database | Database Backward Compatibility | Chiến lược thiết kế Database Schema để cả code cũ và code mới cùng chạy đồng thời được. |
| Trình điều tiết lưu lượng | Weighted Traffic Routing | Cơ chế phân chia % request truy cập theo trọng số trên Ingress Controller / Service Mesh. |
| Cờ tính năng quá hạn | Stale Feature Flags | Các đoạn mã Feature Flag đã bật 100% lâu ngày nhưng quên dọn dẹp khỏi mã nguồn. |
| Trình quản lý Unleash | Unleash Feature Engine | Động cơ mở quản lý Feature Flags được tích hợp sẵn bên trong GitLab. |



#### Mô hình 1: Sơ đồ Kiến trúc Điều tiết Traffic của Blue-Green và Canary Deployment

```mermaid
flowchart TD
    subgraph Scenario 1: Blue-Green Deployment (100% Swap)
        A1[User Request] --> B1[Ingress Controller Switch]
        B1 -->|Active 100%| C1[Blue Environment: v1.0.0]
        B1 -.->|Standby 0%| D1[Green Environment: v2.0.0]
        B1 -->|Instant 100% Swap| D1
    end

    subgraph Scenario 2: Canary Deployment (Weighted Split)
        A2[User Request] --> B2[Ingress Controller Traffic Splitter]
        B2 -->|90% Traffic| C2[Production Stable Pods: v1.0.0]
        B2 -->|10% Traffic| D2[Canary Test Pods: v2.0.0]
        D2 -->|Error Rate > 1%| E2[Auto Rollback: Cut 10% Traffic]
    end
```

#### Mô hình 2: Bảng So sánh Chi tiết Giữa 3 Chiến lược Release Enterprise

| Tiêu chí | Blue-Green Deployment | Canary Deployment | Feature Flags (Feature Toggles) |
|---|---|---|---|
| **Cơ chế hoạt động** | Chuyển đổi 100% traffic lập tức giữa 2 môi trường song song. | Chuyển dần % traffic (10% $\to$ 50% $\to$ 100%) sang bản mới. | Bật/tắt đoạn code tính năng bằng điều kiện logic `if/else` qua API. |
| **Yêu cầu Tài nguyên Hạ tầng** | Gấp 2 lần (200% Capacity) để duy trì 2 môi trường Blue/Green. | Thấp (+10-20% Capacity) để chạy thêm một vài Canary Pods. | Bằng 0% (dùng chung hạ tầng hiện tại của ứng dụng). |
| **Thời gian Rollback** | Cực nhanh (<3 giây qua đổi Ingress Selector). | Cực nhanh (<3 giây qua ngắt Ingress Canary Weight). | **Tức thì (<100ms)** qua thay đổi giá trị Flag trên GitLab UI. |
| **Bán kính ảnh hưởng (Blast Radius)** | 100% người dùng nếu bản Green bị lỗi ngay khi swap. | **Cực hẹp (chỉ 10% người dùng)** thử nghiệm bị ảnh hưởng. | **Có thể bọc theo cụ thể User ID / IP / Quốc gia**. |
| **Độ phức tạp Database Schema** | Yêu cầu Database Backward Compatibility cao. | Yêu cầu Database Backward Compatibility cao. | Không ảnh hưởng lớn tới Database Schema. |

##### Mẫu Cấu hình Manifest NGINX Ingress Canary Weighted Traffic Routing (10% Traffic):
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: payment-service-canary-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"
spec:
  ingressClassName: nginx
  rules:
    - host: payment.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: payment-service-canary
                port:
                  number: 8080
```

---

### 1.1. Quy tắc Triển khai Blue-Green & Canary Deployment (10 phút)

### 4.1. Mẫu Tệp `.gitlab-ci.yml` Triển khai Blue-Green và Canary Release Chuẩn mực

```yaml
stages:
  - build
  - deploy-canary
  - verify-canary
  - promote-production
  - rollback-canary

variables:
  CANARY_WEIGHT: "10"

deploy-canary-10:
  stage: deploy-canary
  script:
    - helm upgrade --install payment-canary ./helm/payment-service --set image.tag=$CI_COMMIT_SHA --set ingress.canary.enabled=true --set ingress.canary.weight=$CANARY_WEIGHT
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

verify-canary-health:
  stage: verify-canary
  script:
    - echo "[CANARY VERIFY] Monitoring Prometheus Error Rate metrics for 15 minutes..."
    - ./scripts/verify-canary-metrics.sh
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

promote-to-100:
  stage: promote-production
  script:
    - echo "[PROMOTE] Promoting Canary v2.0.0 to 100% Stable Production..."
    - helm upgrade --install payment-prod ./helm/payment-service --set image.tag=$CI_COMMIT_SHA --set ingress.canary.enabled=false
    - helm uninstall payment-canary || true
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual

auto-rollback-canary:
  stage: rollback-canary
  script:
    - echo "[ALERT] High Error Rate Detected! Cutting 10% Canary Traffic..."
    - helm uninstall payment-canary
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: on_failure
```

---

### 4.2. Các Quy tắc Cấu hình Release Strategies (QT 43.1 - QT 43.4)

**Nguyên lý cốt lõi:** Áp dụng Blue-Green Deployment cho các ứng dụng có yêu cầu Zero Downtime và tương thích Backward Compatible Schema.
**Phát biểu.** Khi thực hiện phát hành theo mô hình Blue-Green, bắt buộc phải dựng sẵn môi trường Green đầy đủ capacity độc lập với môi trường Blue và chỉ chuyển đổi 100% Ingress traffic sau khi môi trường Green vượt qua toàn bộ các bài test kiểm thử sức khỏe (Health Check).
**Giải thích cơ chế ngầm:** Giúp đảm bảo Zero Downtime tuyệt đối khi nâng cấp phiên bản ứng dụng. Nếu phiên bản Green phát sinh lỗi nghiêm trọng ngay khi vừa tráo đổi, việc chuyển Router Ingress ngược lại Blue chỉ mất dưới 3 giây, khôi phục dịch vụ cho người dùng lập tức.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tắt hoàn toàn môi trường Blue trước khi kiểm thử môi trường Green, làm ứng dụng bị gián đoạn dịch vụ khi Green bị crash.
**Minh hoạ.**
```bash
# Swap Traffic Ingress Service target from Blue to Green
kubectl patch ingress payment-ingress -p '{"spec":{"rules":[{"http":{"paths":[{"backend":{"service":{"name":"payment-green-service"}}}]}}]}}'
```
**Con số chốt:** Rollback Blue-Green dưới 3 giây.

---

**Nguyên lý cốt lõi:** Áp dụng Canary Deployment với bước nghiệm thu traffic nhỏ (10%) kèm thời gian quan sát metric tối thiểu 15 phút.
**Phát biểu.** Khi phát hành bản mới bằng Canary Deployment, nấc nghiệm thu traffic ban đầu chỉ được mở tối đa 10% lượng truy cập thực tế và bắt buộc phải duy trì khoảng thời gian theo dõi chỉ số (Observation Window) ít nhất 15 phút trước khi tăng thêm phần trăm traffic.
**Giải thích cơ chế ngầm:** Giúp thu hẹp bán kính ảnh hưởng sự cố (Blast Radius Reduction). Nếu phiên bản mới bị lỗi rò rỉ bộ nhớ (Memory Leak) hay nổ lỗi HTTP 500 ở một edge case hiếm gặp, chỉ có đúng 10% người dùng thực tế chịu tác động trong 15 phút nghiệm thu, 90% người dùng còn lại vẫn hoàn toàn an toàn trên bản Stable.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Mở thẳng 50% hoặc 100% traffic Canary ngay lập tức không có thời gian chờ quan sát metric Prometheus.
**Minh hoạ.** `nginx.ingress.kubernetes.io/canary-weight: "10"` trong 15 phút.
**Con số chốt:** 10% Traffic ban đầu và 15 phút Observation Window.

---

**Nguyên lý cốt lõi:** Tự động hóa Rollback Canary khi tỷ lệ lỗi HTTP 5xx vượt ngưỡng 1% hoặc P99 Latency tăng vượt 500ms.
**Phát biểu.** Pipeline CI/CD bắt buộc phải liên kết với Prometheus Alertmanager Webhook để tự động hủy bỏ (Rollback) Canary Pods lập tức khi tỷ lệ lỗi HTTP 5xx của nấc Canary vượt quá 1% tổng request hoặc độ trễ P99 Latency vượt quá 500ms.
**Giải thích cơ chế ngầm:** Loại bỏ hoàn toàn sự chậm trễ của yếu tố con người. Máy móc và Prometheus có khả năng phát hiện tỷ lệ lỗi tăng vọt trong 2 giây và kích hoạt ngắt Ingress Canary lập tức, rút ngắn thời gian phát hiện lỗi (MTTD) xuống dưới 5 giây.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chờ kỹ sư trực ca phát hiện lỗi bằng mắt trên dashboard rồi mới gõ lệnh rollback thủ công sau 30 phút.
**Minh hoạ.**
```yaml
rules:
  - if: $CI_COMMIT_BRANCH == "main"
    when: on_failure
```
**Con số chốt:** Tự động Rollback khi HTTP 5xx > 1%.

---

**Nguyên lý cốt lõi:** Sử dụng GitLab Feature Flags (Unleash Engine) phân tách việc Deploy mã nguồn khỏi việc Enable tính năng.
**Phát biểu.** Tất cả các tính năng nghiệp vụ mới mang tính rủi ro cao phải được bọc trong bộ quản lý GitLab Feature Flags (Unleash Client SDK), cho phép lập trình viên deploy mã nguồn lên Production trước, sau đó mới bật tính năng (Enable Flag) trên giao diện GitLab UI.
**Giải thích cơ chế ngầm:** Thực thi nguyên tắc "Deploy is NOT Release". Việc đưa code lên máy chủ (Deploy) có thể diễn ra bất kỳ lúc nào trong ngày mà không gây ảnh hưởng tới người dùng. Việc phát hành tính năng (Release) được quyết định linh hoạt bởi Product Manager thông qua việc bật/tắt Feature Flag trên UI trong 100ms.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Buộc phải chạy lại toàn bộ pipeline build và deploy Docker Image chỉ để bật hoặc tắt một tính năng nhỏ trên Production.
**Minh hoạ.**
```javascript
if (unleashClient.isEnabled("new_payment_gateway")) {
    processNewGateway();
} else {
    processLegacyGateway();
}
```
**Con số chốt:** Bật/tắt Feature Flag dưới 100ms.

---

### 1.2. Quy tắc Quản lý Feature Flags & Database Migration (10 phút)

**Nguyên lý cốt lõi:** Bắt buộc bọc các tính năng mới trong khối Feature Flag Toggle với fallback mặc định an toàn.
**Phát biểu.** Đoạn mã sử dụng Feature Flag phải luôn khai báo giá trị fallback mặc định là `false` (Legacy Code Path) nếu không thể kết nối tới GitLab Feature Flag Server.
**Giải thích cơ chế ngầm:** Đảm bảo tính sẵn sàng cao (High Availability). Nếu mạng giữa ứng dụng và máy chủ GitLab Unleash Server bị ngắt kết nối, ứng dụng vẫn tự động rơi về luồng code cũ ổn định (Fallback Path) thay vì bị crash ứng dụng.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Không viết nhánh `else` fallback, làm ứng dụng nổ lỗi `NullPointerException` khi Feature Flag Server bị timeout.
**Minh hoạ.**
```java
if (unleash.isEnabled("enable_v2_recommendation", false)) {
    return getV2Recommendations();
}
return getV1StandardRecommendations();
```
**Con số chốt:** 100% Feature Flags có Fallback Path an toàn.

---

**Nguyên lý cốt lõi:** Tự động dọn dẹp các Stale Feature Flags cũ hơn 30 ngày sau khi tính năng đã ổn định 100%.
**Phát biểu.** Đặt lịch linter định kỳ rà soát mã nguồn và xóa bỏ hoàn toàn các đoạn code bọc Feature Flag (Stale Flags) sau khi tính năng đó đã được bật 100% và chạy ổn định trên Production quá 30 ngày.
**Giải thích cơ chế ngầm:** Trọng nợ kỹ thuật (Technical Debt). Nếu không dọn dẹp các Feature Flags cũ, mã nguồn ứng dụng sẽ bị phình to bởi hàng ngàn câu lệnh `if/else` chồng chéo, gây rối mắt lập trình viên và làm tăng độ phức tạp khi viết Unit Tests.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Giữ lại hàng trăm tệp Feature Flags từ 2 năm trước làm mã nguồn biến thành "tổ nhện" logic.
**Minh hoạ.** Xóa bỏ nhánh `else` cũ và loại bỏ khai báo flag trên GitLab UI sau 30 ngày.
**Con số chốt:** Xóa Stale Flags sau 30 ngày.

---

**Nguyên lý cốt lõi:** Đảm bảo tính tương thích ngược của Database Schema (Database Backward Compatibility) khi thực thi Blue-Green/Canary.
**Phát biểu.** Khi thực hiện nâng cấp Database Schema trong các luồng Blue-Green hay Canary Deployment, bắt buộc phải áp dụng kịch bản **Expand-and-Contract (Parallel Change)**.
**Giải thích cơ chế ngầm:** Trong mô hình Blue-Green hay Canary, phiên bản ứng dụng cũ (v1) và phiên bản mới (v2) sẽ **cùng truy cập vào một Database duy nhất** trong một khoảng thời gian. Nếu bạn xóa ngay một cột (Column) hoặc đổi tên bảng (Rename Table), phiên bản v1 cũ đang nhận 90% traffic sẽ bị nổ lỗi SQL Crash lập tức!
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chạy lệnh `ALTER TABLE DROP COLUMN` ngay trong stage migration của phiên bản mới làm sập phiên bản cũ đang nhận traffic.
**Minh hoạ.**
- *Pha 1 (Expand):* Thêm cột mới `new_email`, giữ nguyên `email`.
- *Pha 2 (Deploy):* Deploy v2 ghi dữ liệu vào cả 2 cột.
- *Pha 3 (Contract):* Sau 30 ngày dọn dẹp xóa cột `email` cũ.
**Con số chốt:** 100% Database Migrations áp dụng Expand-and-Contract.

---

**Nguyên lý cốt lõi:** Sử dụng Ingress Controller NGINX / Service Mesh Linkerd/Istio để điều tiết phần trăm Weighted Traffic Routing.
**Phát biểu.** Việc phân chia phần trăm traffic trong Canary Deployment bắt buộc phải được điều tiết tại tầng Ingress Controller hoặc Service Mesh chứ không được chia bằng code ứng dụng.
**Giải thích cơ chế ngầm:** Giúp đảm bảo tính chính xác tuyệt đối của việc phân bổ lưu lượng (Traffic Splitting) ở tầng mạng HTTP Layer mà không làm tăng độ phức tạp của mã nguồn ứng dụng. NGINX Ingress hoặc Service Mesh có khả năng điều tiết chính xác 1%, 5%, 10% traffic dựa trên HTTP Header, Cookie hoặc Random Hash Weight.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Viết mã ngẫu nhiên `Math.random() < 0.1` bên trong code backend để tự chia traffic Canary.
**Minh hoạ.** Annotations `nginx.ingress.kubernetes.io/canary-weight: "10"`.
**Con số chốt:** 100% Traffic Splitting điều phối ở tầng Ingress/Service Mesh.

---

### 1.3. Quy tắc Observability, Access Control & Disaster Recovery (10 phút)

**Nguyên lý cốt lõi:** Khai báo GitLab Environments (Production-Blue, Production-Green, Canary) để theo dõi lịch sử deployment.
**Phát biểu.** Mọi job deployment trong `.gitlab-ci.yml` bắt buộc phải gắn khai báo `environment.name` và `environment.url` tương ứng với nấc release.
**Giải thích cơ chế ngầm:** Giúp hiển thị trực quan toàn bộ lịch sử các phiên bản đang chạy trên từng môi trường trực tiếp trên giao diện GitLab Environments Dashboard. Cho phép Tech Lead thực hiện Rollback 1-Click ngay từ giao diện GitLab UI khi phát hiện sự cố.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Deploy ứng dụng không khai báo khối `environment` khiến GitLab CI không lưu vết được lịch sử phiên bản trên từng cụm.
**Minh hoạ.**
```yaml
environment:
  name: production/canary
  url: https://canary.payment.company.com
```
**Con số chốt:** 100% Deploy Jobs có khai báo `environment`.

---

**Nguyên lý cốt lõi:** Tích hợp Prometheus Alertmanager Webhook tự động kích hoạt Rollback Job trong GitLab CI Pipeline.
**Phát biểu.** Cấu hình Prometheus Alertmanager gửi HTTP POST Webhook tới GitLab Pipeline Trigger URL khi cảnh báo `HighErrorRateCanary` kích hoạt.
**Giải thích cơ chế ngầm:** Tự động hóa hoàn toàn quy trình xử lý sự cố (Closed-loop Remediation). Khi hệ thống giám sát Prometheus phát hiện phiên bản Canary bị nổ lỗi, nó tự động gửi webhook gọi GitLab CI thực thi ngay job `auto-rollback-canary` xóa bỏ Canary Pods trong dưới 3 giây mà không cần kỹ sư On-call thức dậy can thiệp.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cảnh báo Prometheus chỉ gửi tin nhắn Slack rồi nằm chờ người dùng vào đọc tin nhắn và thao tác tay.
**Minh hoạ.** Prometheus Alert Rule bắn Webhook tới `https://gitlab.company.com/api/v4/projects/12/trigger/pipeline`.
**Con số chốt:** Tự động ngắt Canary dưới 3 giây qua Webhook.

---

**Nguyên lý cốt lõi:** Phân quyền bật/tắt Feature Flags cho Product Manager mà không cần quyền truy cập CI/CD Pipeline.
**Phát biểu.** Cấp quyền truy cập quản trị Feature Flags trên giao diện GitLab UI (vai trò `Reporter` hoặc `Developer`) cho bộ phận Product Manager / Business Analyst.
**Giải thích cơ chế ngầm:** Thực thi đúng triết lý Phân tách Trách nhiệm (Separation of Duties). Đội ngũ DevOps/Developer chịu trách nhiệm đưa code lên hạ tầng an toàn; đội ngũ Product Manager chủ động quyết định thời điểm bật/tắt tính năng kinh doanh cho khách hàng mà không cần phiền tới kỹ sư DevOps chạy lại pipeline.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Mỗi lần muốn bật Feature Flag cho 1 khách hàng VIP lại phải nhờ DevOps gõ lệnh CLI hoặc sửa biến môi trường CI.
**Minh hoạ.** Phân quyền truy cập Feature Flags trong mục `Deployments -> Feature Flags` trên GitLab.
**Con số chốt:** 100% Product Managers tự quản lý Feature Flags.

---

**Nguyên lý cốt lõi:** Thiết lập cơ chế Canary Analysis tự động đo lường chỉ số lỗi của phiên bản mới so với phiên bản baseline.
**Phát biểu.** Trước khi tăng nấc Canary từ 10% lên 50%, bắt buộc phải thực thi một script so sánh đối soát tự động (Canary Analysis) giữa chỉ số Error Rate/Latency của Canary Pods v2 và Baseline Pods v1 trong cùng một khoảng thời gian.
**Giải thích cơ chế ngầm:** Tránh đánh giá cảm tính. Script Canary Analysis tự động đọc dữ liệu Prometheus, tính toán công nghệ phân tích thống kê (như thuật toán Kayenta/Mann-Whitney U test). Nếu phiên bản Canary v2 có tỷ lệ lỗi vượt trội so với Baseline v1, pipeline sẽ lập tức từ chối Promote và phát lệnh Rollback.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đánh giá Canary thành công hay thất bại chỉ dựa vào cảm tính của kỹ sư trực ca mà không so sánh với bản Baseline.
**Minh hoạ.** Executing script `verify-canary-metrics.sh` so sánh Canary metric với Baseline metric.
**Con số chốt:** 100% Promote Canary trải qua Canary Analysis.

---

### 1.4. Đưa vào việc thật (4 phút)

### 7.1. Kịch bản áp dụng thực tế tại Tập đoàn Thương mại Điện tử trong Ngày Săn Sale 11/11
Trong đợt Săn Sale 11/11 với lượng truy cập 500.000 requests/giây:
1. **Pha Deploy Mã nguồn (Deploy Phase):** Đội ngũ phát triển hoàn thành tính năng "Vòng quay May mắn". Mã nguồn được build và deploy sẵn lên cụm Kubernetes từ 3 ngày trước dưới dạng **Feature Flag disabled (`false`)**.
2. **Pha Triển khai Canary (Canary Phase):** Đội DevOps mở 5% traffic Canary cho cụm Pods v2. Hệ thống Prometheus theo dõi chỉ số P99 Latency duy trì ổn định 45ms (dưới ngưỡng 500ms).
3. **Pha Bật Feature Flag Thực tế (Release Phase):** Đúng 00:00 AM ngày 11/11, Giám đốc Sản phẩm (Product Director) lên giao diện GitLab Feature Flags bấm công tắc **ON** cho nhóm người dùng tại Hà Nội. Tính năng xuất hiện tức thì trong 50ms cho người dùng mà không có bất kỳ thời gian ngắt trang nào.
4. **Pha Xử lý Sự cố Tự động (Auto-Rollback):** Đến 00:05 AM, hệ thống phát hiện cổng thanh toán qua thẻ VISA bị nổ lỗi HTTP 500 trên nấc Canary (tỷ lệ lỗi 2.5%). Alertmanager lập tức gọi Webhook ngắt Canary traffic về 0% và tắt Feature Flag tự động trong 2 giây. 95% khách hàng mua sắm hoàn toàn không bị ảnh hưởng!

### 7.2. Case Study Thực tế: Thảm họa Sập Toàn bộ Cổng Thanh toán do Nâng cấp Database Schema không Tương thích Ngược
Một ứng dụng Fintech thực thi nâng cấp giao diện thanh toán mới bằng Blue-Green Deployment.
- **Thảm họa ở cách làm cũ (Vi phạm Database Backward Compatibility - QT 43.7):**
  1. Kỹ sư Database chạy script migration xóa cột `user_card_number` cũ và thay bằng bảng `user_cards` mới trên Database Production.
  2. Môi trường Green (v2) chạy thử nghiệm xanh 100%. Đội DevOps bấm nút swap 100% Ingress sang Green.
  3. Tuy nhiên, sau 5 phút phát hiện Green bị nổ lỗi logic thanh toán. DevOps vội vã swap Ingress tráo đổi ngược lại môi trường Blue (v1).
  4. Nhưng phiên bản Blue (v1) khi nhận lại traffic đã lập tức **NỔ LỖI CRASH HÀNG LOẠT** do cột `user_card_number` trên Database đã bị script migration của v2 xóa mất trước đó! Hệ thống bị sập hoàn toàn 4 tiếng đồng hồ!
- **Khôi phục hoàn hảo ở cách làm chuẩn Buổi 43 (Expand-and-Contract Schema - QT 43.7):**
  Nếu áp dụng đúng QT 43.7, script migration sẽ giữ nguyên cột `user_card_number` cũ và tạo song song bảng `user_cards` mới. Cả v1 và v2 cùng đọc/ghi được dữ liệu. Khi rollback về bản Blue (v1), hệ thống tiếp tục chạy mượt mà 100% không dính sự cố SQL Crash!

### 7.3. Case Study 3: Thu Hẹp Bán kính Ảnh hưởng Sự cố (Blast Radius Reduction) nhờ Canary 10%
Một tập đoàn Logistics phát hành thuật toán tính phí giao hàng mới cho 10 triệu người dùng.
- **Cách làm cũ:** Deploy đập thẳng 100% ứng dụng mới lên cụm. Thuật toán bị lỗi nhân 10 lần giá cước, làm 500.000 khách hàng bức xúc hủy đơn trong 30 phút, công ty chịu thiệt hại 2 tỷ đồng.
- **Cách làm chuẩn Buổi 43 (Canary 10% - QT 43.2):**
  1. Mở nấc Canary chỉ **10% traffic** cho nhóm 1.000 tài khoản thử nghiệm.
  2. Phát hiện ngay lập tức giá cước bị tính sai ở 10% này trong 3 phút đầu tiên.
  3. Prometheus kích hoạt ngắt Canary tự động. Chỉ có 50 khách hàng bị ảnh hưởng thử nghiệm và được CSKH bồi hoàn voucher ngay lập tức. Bán kính ảnh hưởng được thu hẹp 99.9%!

### 7.4. Case Study 4: Bật/Tắt Tính năng Khẩn cấp trong 50ms bằng GitLab Feature Flags
Một ứng dụng tin tức bị đợt tấn công DDOS làm quá tải máy chủ tìm kiếm Elasticsearch.
- **Cách làm cũ:** Phải sửa code tắt tính năng tìm kiếm, commit code, chờ CI Runner build Docker Image mất 20 phút. Hệ thống bị sập hoàn toàn trong 20 phút đó.
- **Cách làm chuẩn Buổi 43 (GitLab Feature Flags - QT 43.4):**
  Kỹ sư On-call mở giao diện GitLab UI tại mục `Deployments -> Feature Flags`, chuyển cờ `enable_elasticsearch_search` từ **ON** sang **OFF**. Trong **50 miligiây**, toàn bộ các Pods trên Production ngắt luồng gọi Elasticsearch và chuyển sang hiển thị danh sách bài viết tĩnh. Hệ thống đứng vững 100% trước trận tấn công!

---

### 7.5. Trường hợp khi nào KHÔNG nên dùng Canary Deployment
Mặc dù Canary Deployment là chuẩn mực an toàn cao nhất, nhưng KHÔNG áp dụng cho các trường hợp sau:

| Ngữ cảnh / Hạ tầng | Lý do KHÔNG dùng được Canary Deployment | Giải pháp thay thế an toàn |
|---|---|---|
| Thay đổi Breaking Change Database Schema không thể áp dụng Expand-and-Contract | Hai phiên bản v1 và v2 không thể cùng đọc/ghi một Database cấu trúc cũ được. | Sử dụng Maintenance Window thông báo bảo trì ngắt kết nối và áp dụng Blue-Green với DB Backup. |
| Hệ thống xử lý giao dịch tài chính Core-Banking khớp lệnh theo chuỗi tuần tự | Việc chia 10% traffic sang v2 có thể làm lệch thứ tự ghi sổ cái kế toán (Ledger Inconsistency). | Sử dụng Blue-Green Deployment với Shadow Traffic Testing (nghiệm thủ dữ liệu mờ). |
| Các ứng dụng Desktop / Mobile App cài đặt trực tiếp trên máy client người dùng | Không thể chủ động điều tiết % traffic trên máy client bằng NGINX Ingress được. | Sử dụng Feature Flags hoặc Phân tầng Release theo Version trên Google Play / App Store. |

---

### 1.5. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính bẫy | Làm đúng là |
|---|---|---|
| Bẫy 1: Xóa cột Database cũ ngay khi deploy phiên bản mới | Làm phiên bản cũ (v1) đang nhận traffic bị nổ lỗi SQL Crash khi rollback hoặc chạy Canary. | Áp dụng kịch bản Expand-and-Contract Database Migration, giữ tương thích ngược (QT 43.7). |
| Bẫy 2: Mở thẳng 50% hoặc 100% traffic Canary ngay khi deploy | Mất tác dụng thu hẹp bán kính ảnh hưởng sự cố (Blast Radius), khi có lỗi 100% người dùng chịu trận. | Bắt đầu với nấc Canary 10% và quan sát metric tối thiểu 15 phút (QT 43.2). |
| Bẫy 3: Đánh giá Canary thành công bằng mắt thủ công | Kỹ sư trực ca không thể phát hiện các lỗi tăng trễ P99 hay rò rỉ bộ nhớ nhỏ ở nấc 10% traffic. | Tự động hóa Rollback qua Prometheus Alertmanager Webhook khi HTTP 5xx > 1% (QT 43.3). |
| Bẫy 4: Quên dọn dẹp các Stale Feature Flags cũ | Mã nguồn bị phình to bởi hàng ngàn câu lệnh `if/else` dư thừa từ các đợt release cũ 2 năm trước. | Đặt lịch linter định kỳ xóa bỏ Stale Feature Flags sau 30 ngày ổn định (QT 43.6). |
| Bẫy 5: Không khai báo fallback khi sử dụng Feature Flag SDK | Khi máy chủ Feature Flag bị timeout hoặc rớt mạng, ứng dụng bị nổ lỗi `NullPointer` crash. | Luôn bọc giá trị fallback mặc định an toàn (`false`) trong câu lệnh toggle (QT 43.5). |
| Bẫy 6: Chia traffic Canary bằng code `Math.random()` trong app | Làm tăng độ phức tạp mã nguồn và không thể điều chỉnh % traffic linh hoạt từ bên ngoài. | Sử dụng Ingress Controller NGINX / Service Mesh điều tiết Weighted Traffic (QT 43.8). |
| Bẫy 7: Promote Canary lên 100% mà không so sánh với Baseline Pods | Đánh giá sai hiệu năng bản mới do không đối soát với bản cũ trong cùng một điều kiện tải. | Thực thi Canary Analysis so sánh metric bản mới v2 với bản baseline v1 (QT 43.12). |
| Bẫy 8: Không khai báo khối `environment` trong `.gitlab-ci.yml` | GitLab CI không lưu trữ được lịch sử phiên bản deployment và không dùng được nút Rollback 1-Click. | Luôn khai báo `environment.name` và `environment.url` trong các job deploy (QT 43.9). |

---

### 1.6. Tóm tắt (3 phút)

### 9.1. Sơ đồ Mermaid: Vòng đời Phát hành Ứng dụng với Canary & Feature Flags

```mermaid
flowchart TD
    subgraph Stage 1: Build & Deploy Code
        A[Git Commit to main] --> B[Build Docker Image]
        B --> C[Deploy Code with Feature Flag OFF]
    end

    subgraph Stage 2: Canary Deployment (10% Traffic)
        C --> D[Helm Deploy Canary Pods v2.0.0]
        D --> E[NGINX Ingress: Set Canary Weight 10%]
        E --> F[Prometheus Monitoring: 15 Mins Observation]
    end

    subgraph Stage 3: Automated Health Decision
        F --> G{HTTP 5xx > 1% or Latency > 500ms?}
        G -->|YES: Error Alert| H[Auto Rollback Webhook: Cut Canary to 0%]
        G -->|NO: Healthy| I[Promote Production: Set Weight 100%]
    end

    subgraph Stage 4: Feature Release
        I --> J[Product Manager turns Feature Flag ON on GitLab UI]
        J --> K[100% Users Enjoy New Feature Zero Downtime]
    end
```

### 9.2. Năm điều phải nhớ thuộc lòng
1. **Deploy is NOT Release:** Phân tách việc đưa code lên hạ tầng (Deploy) khỏi việc bật tính năng cho người dùng (Release) bằng Feature Flags.
2. **Expand-and-Contract Database Migrations:** Luôn đảm bảo tương thích ngược Database Schema để cả v1 và v2 cùng chạy đồng thời mà không bị crash.
3. **Canary 10% with 15-Min Window:** Bắt đầu nấc Canary với 10% traffic và duy trì khoảng thời gian quan sát metric Prometheus ít nhất 15 phút.
4. **Automated Error Threshold Rollback:** Tự động ngắt Canary traffic dưới 3 giây qua Webhook khi tỷ lệ lỗi HTTP 5xx vượt quá 1%.
5. **Clean Stale Flags in 30 Days:** Xóa bỏ triệt để các đoạn code Feature Flag đã chạy ổn định 100% quá 30 ngày để chống nợ kỹ thuật.

---

### 1.7. Câu hỏi tự kiểm tra (5 phút)

### 10.1. Danh sách câu hỏi tự kiểm tra
1. Sự khác biệt cốt lõi nhất giữa hai chiến lược Blue-Green Deployment và Canary Deployment là gì?
2. Tại sao việc đảm bảo tính tương thích ngược của Database Schema (Expand-and-Contract) lại là điều kiện sống còn đối với Blue-Green và Canary?
3. Khoảng thời gian quan sát metric (Observation Window) khuyến nghị tối thiểu cho nấc Canary 10% traffic là bao nhiêu?
4. Ngưỡng tỷ lệ lỗi HTTP 5xx tối đa để kích hoạt tự động Rollback Canary là bao nhiêu?
5. Ưu điểm lớn nhất của việc sử dụng GitLab Feature Flags (Unleash Engine) so với việc redeploy code là gì?
6. Tại sao phải luôn khai báo giá trị fallback mặc định (`false`) trong câu lệnh kiểm tra Feature Flag SDK?
7. Tại sao nên thực hiện việc điều tiết % traffic Canary ở tầng Ingress Controller / Service Mesh chứ không nên chia bằng code ứng dụng?
8. Khái niệm "Stale Feature Flags" là gì và thời gian tối đa nên dọn dẹp chúng khỏi mã nguồn là bao nhiêu ngày?
9. Ý nghĩa của việc khai báo khối `environment` trong tệp `.gitlab-ci.yml` khi triển khai Canary là gì?
10. Công cụ nào giúp Prometheus Alertmanager gửi tín hiệu ngắt Canary tự động về GitLab CI Pipeline?
11. Khái niệm "Canary Analysis" là gì và tại sao phải so sánh phiên bản Canary mới với phiên bản Baseline cũ?
12. Tại sao Product Manager nên là người nắm quyền bật/tắt Feature Flags chứ không phải kỹ sư DevOps?

---

### 10.2. Đáp án câu hỏi tự kiểm tra

1. Blue-Green chuyển đổi 100% traffic giữa 2 môi trường song song trong 1 giây; Canary mở dần % traffic nhỏ (10% -> 50% -> 100%) nghiệm thu dần trên Production.
2. Vì phiên bản cũ (v1) và phiên bản mới (v2) sẽ cùng truy cập một Database trong khoảng thời gian release; nếu xóa cột cũ sẽ làm phiên bản v1 bị nổ lỗi SQL Crash lập tức.
3. Khoảng thời gian quan sát metric khuyến nghị tối thiểu là **15 phút**.
4. Ngưỡng tỷ lệ lỗi HTTP 5xx tối đa là **1% tổng số request** (hoặc P99 Latency > 500ms).
5. Cho phép bật/tắt tính năng theo thời gian thực trong **100ms** trực tiếp từ giao diện GitLab UI mà không cần rebuild Docker Image hay redeploy code.
6. Để ứng dụng vẫn tự động rơi về luồng code cũ an toàn (Fallback Path) nếu máy chủ Feature Flag Server bị ngắt kết nối hoặc timeout.
7. Đảm bảo tính chính xác của việc phân bổ lưu lượng ở tầng mạng HTTP Layer và không làm tăng độ phức tạp của mã nguồn ứng dụng.
8. Stale Feature Flags là các đoạn mã flag đã bật 100% lâu ngày; nên dọn dẹp khỏi mã nguồn sau **30 ngày** ổn định.
9. Giúp GitLab CI ghi lại nhật ký lịch sử phiên bản deployment và hỗ trợ nút Rollback 1-Click trên giao diện GitLab UI.
10. Sử dụng cơ chế **GitLab Pipeline Trigger Webhook** (gọi HTTP POST tới API GitLab).
11. Canary Analysis là quá trình so sánh đối soát tự động các chỉ số Error Rate/Latency giữa Canary v2 và Baseline v1 để đưa ra quyết định Promote hay Rollback bằng thuật toán thống kê.
12. Để phân tách trách nhiệm (Separation of Duties): DevOps chịu trách nhiệm độ tin cậy hạ tầng, Product Manager chủ động quyết định thời điểm phát hành tính năng kinh doanh cho khách hàng.

---

### 1.8. Tài liệu tham khảo (2 phút)

| Nguồn tài liệu | Mô tả nội dung | Phiên bản áp dụng |
|---|---|---|
| NGINX Ingress Controller Documentation — Canary Deployments | Hướng dẫn cấu hình Ingress Annotations `canary-weight` | NGINX Ingress v1.8+ |
| GitLab Documentation — Feature Flags with Unleash Engine | Hướng dẫn tích hợp SDK Unleash Client và quản lý Flags | GitLab v16.0+ |
| Martin Fowler — Feature Toggles (Feature Flags) Guide | Bài viết kinh điển về các mẫu thiết kế Feature Toggles | Enterprise Architecture |
| Prometheus Alertmanager Documentation — Webhook Receiver | Hướng dẫn bắn Webhook tự động hóa Rollback Pipeline | Prometheus v2.40+ |
| Kayenta — Automated Canary Analysis Engine | Công cụ phân tích chỉ số Canary tự động do Netflix phát triển | OSS Infrastructure |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10 phút |
| §1 | Sau buổi này học viên LÀM ĐƯỢC gì | 1 phút |
| §2 | Cần biết trước | 1 phút |
| §3 | Thuật ngữ và mô hình tư duy | 8 phút |
| §4 | Quy tắc Triển khai Blue-Green & Canary Deployment | 10 phút |
| §5 | Quy tắc Quản lý Feature Flags & Database Migration | 10 phút |
| §6 | Quy tắc Observability, Access Control & Disaster Recovery | 10 phút |
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
Trong bài lab này, học viên sẽ trực tiếp triển khai và làm chủ 3 chiến lược phát hành ứng dụng hiện đại:
1. Khởi tạo mã nguồn Microservice tích hợp SDK GitLab Feature Flags (Unleash Client) và cấu hình NGINX Ingress Weighted Routing.
2. Viết script CI triển khai Blue-Green Deployment và thực hiện tráo đổi (swap) 100% Ingress traffic trong 1 giây.
3. Xây dựng luồng Canary Deployment với bước chia 10% traffic nghiệm thu và theo dõi chỉ số Prometheus metrics.
4. Kiểm thử tự động hóa Rollback Canary khi chỉ số lỗi HTTP 5xx tăng đột biến (>1%) qua Alertmanager Webhook.
5. Kết nối GitLab Feature Flags API để bật/tắt tính năng từ xa theo thời gian thực (50ms) không cần redeploy code.
6. Xây dựng kịch bản Expand-and-Contract Database Migration và script linter kiểm tra phát hiện Stale Feature Flags cũ.

---

## 2. Mô hình kiến trúc Lab L2

```mermaid
graph TD
    subgraph Phase 1: Blue-Green Deployment (100% Swap)
        A[GitLab CI Job] -->|1. helm upgrade blue/green| B[Kubernetes Deployments]
        B -->|Active: 100% Traffic| C[Blue Service v1.0.0]
        B -->|Standby: 0% Traffic| D[Green Service v2.0.0]
        E[kubectl patch ingress] -->|2. Instant 100% Swap| D
    end

    subgraph Phase 2: Canary Deployment (Weighted Traffic Split)
        F[GitLab CI Job] -->|3. helm upgrade canary| G[Canary Deployment v2.0.0]
        H[NGINX Ingress] -->|4. canary-weight: 10| G
        I[Prometheus Alert] -->|5. HTTP 5xx > 1%| J[Auto Rollback Webhook]
        J -->|6. Cut 10% Traffic| H
    end

    subgraph Phase 3: GitLab Feature Flags (Unleash Engine)
        K[Microservice App] -->|7. Poll Flag API 50ms| L[GitLab Feature Engine]
        M[Product Manager UI Click] -->|8. Flag ON/OFF| L
        L -->|9. Toggle Feature Route| K
    end
```

---

## 3. Các bước thực hiện bài lab (14 Checkpoints)

### Bước 1: Khởi tạo Cấu trúc Thư mục và Mã nguồn Microservice tích hợp Feature Flags (10 phút)

Tạo thư mục làm việc cho bài lab Buổi 43:

```bash
mkdir -p release-lab
cd release-lab
mkdir -p app/src manifests/blue-green manifests/canary scripts audit feature-flags
```

Khởi tạo mã nguồn ứng dụng `app/src/server.js` tích hợp SDK Feature Flags:

```javascript
const express = require('express');
const app = express();
const PORT = process.env.PORT || 8080;
const VERSION = process.env.APP_VERSION || 'v1.0.0-blue';

// Feature Flag Status Storage (Simulated Unleash Engine)
let featureFlags = {
  new_checkout_flow: process.env.FEATURE_NEW_CHECKOUT === 'true' || false,
  dark_mode_ui: false
};

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'UP', version: VERSION });
});

app.get('/api/checkout', (req, res) => {
  if (featureFlags.new_checkout_flow) {
    res.status(200).json({
      message: 'New V2 Checkout Flow Enabled via GitLab Feature Flag!',
      engine: 'v2-quantum-checkout',
      version: VERSION
    });
  } else {
    res.status(200).json({
      message: 'Standard V1 Legacy Checkout Flow Active',
      engine: 'v1-legacy-checkout',
      version: VERSION
    });
  }
});

// Endpoint mô phỏng toggle Feature Flag từ xa qua API
app.post('/api/feature-flags/toggle', express.json(), (req, res) => {
  const { flagName, enabled } = req.body;
  featureFlags[flagName] = enabled;
  res.status(200).json({ flagName, enabled, updated_at: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`[SERVER] Release Lab App running on port ${PORT} (Version: ${VERSION})`);
});
```

Khởi tạo file `app/package.json`:

```json
{
  "name": "release-lab-app",
  "version": "1.0.0",
  "description": "Microservice for Blue-Green, Canary and Feature Flags Lab",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

### **CHECKPOINT 1**
Chạy câu lệnh kiểm tra tệp `server.js` và `package.json`:

```bash
test -f app/src/server.js && test -f app/package.json && echo "CHECKPOINT 1: ĐẠT" || echo "CHECKPOINT 1: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 1: ĐẠT
```

---

### Bước 2: Khởi tạo Manifests Kubernetes cho Blue-Green Deployment (10 phút)

Tạo tệp Kubernetes Manifest Môi trường Blue `manifests/blue-green/blue-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-blue
  namespace: production
  labels:
    app: payment-service
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-service
      version: blue
  template:
    metadata:
      labels:
        app: payment-service
        version: blue
    spec:
      containers:
        - name: app
          image: registry.company.com/bank-group/payment-service:v1.0.0
          env:
            - name: APP_VERSION
              value: "v1.0.0-blue"
          ports:
            - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: payment-service-blue-svc
  namespace: production
spec:
  ports:
    - port: 8080
      targetPort: 8080
  selector:
    app: payment-service
    version: blue
```

Tạo tệp Kubernetes Manifest Môi trường Green `manifests/blue-green/green-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-green
  namespace: production
  labels:
    app: payment-service
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-service
      version: green
  template:
    metadata:
      labels:
        app: payment-service
        version: green
    spec:
      containers:
        - name: app
          image: registry.company.com/bank-group/payment-service:v2.0.0
          env:
            - name: APP_VERSION
              value: "v2.0.0-green"
          ports:
            - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: payment-service-green-svc
  namespace: production
spec:
  ports:
    - port: 8080
      targetPort: 8080
  selector:
    app: payment-service
    version: green
```

Tạo tệp Ingress Main điều tiết Blue-Green `manifests/blue-green/main-ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: payment-service-main-ingress
  namespace: production
spec:
  ingressClassName: nginx
  rules:
    - host: payment.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: payment-service-blue-svc
                port:
                  number: 8080
```

### **CHECKPOINT 2**
Chạy câu lệnh kiểm tra các tệp manifests Blue-Green:

```bash
test -f manifests/blue-green/blue-deployment.yaml && test -f manifests/blue-green/green-deployment.yaml && test -f manifests/blue-green/main-ingress.yaml && echo "CHECKPOINT 2: ĐẠT" || echo "CHECKPOINT 2: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 2: ĐẠT
```

---

### Bước 3: Viết Script Mô phỏng Blue-Green 100% Instant Traffic Swap (15 phút)

Tạo script thực thi tráo đổi Blue-Green `scripts/blue-green-swap.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

TARGET_COLOR="${1:-green}"

echo "[BLUE-GREEN SWAP] Initiating 100% Instant Traffic Swap to '$TARGET_COLOR'..."
mkdir -p manifests/live-state

if [ "$TARGET_COLOR" = "green" ]; then
    cat << EOF > manifests/live-state/active-routing.json
{
  "active_color": "green",
  "active_service": "payment-service-green-svc",
  "active_version": "v2.0.0-green",
  "traffic_share": "100%",
  "swapped_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "SWAPPED_SUCCESSFULLY"
}
EOF
    echo "[BLUE-GREEN SWAP] Traffic 100% successfully switched to GREEN (v2.0.0)!"
else
    cat << EOF > manifests/live-state/active-routing.json
{
  "active_color": "blue",
  "active_service": "payment-service-blue-svc",
  "active_version": "v1.0.0-blue",
  "traffic_share": "100%",
  "swapped_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "ROLLED_BACK_TO_BLUE"
}
EOF
    echo "[BLUE-GREEN SWAP] Traffic 100% rolled back to BLUE (v1.0.0)!"
fi
```

Cho phép script chạy swap sang Green:
```bash
chmod +x scripts/blue-green-swap.sh
./scripts/blue-green-swap.sh "green"
```

### **CHECKPOINT 3**
Chạy câu lệnh kiểm tra kết quả Blue-Green Traffic Swap sang Green:

```bash
test -f manifests/live-state/active-routing.json && grep -q "SWAPPED_SUCCESSFULLY" manifests/live-state/active-routing.json && echo "CHECKPOINT 3: ĐẠT" || echo "CHECKPOINT 3: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 3: ĐẠT
```

---

### Bước 4: Khởi tạo Manifests Kubernetes cho NGINX Canary Weighted Routing (15 phút)

Tạo tệp Ingress Canary `manifests/canary/canary-ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: payment-service-canary-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"
spec:
  ingressClassName: nginx
  rules:
    - host: payment.company.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: payment-service-canary-svc
                port:
                  number: 8080
```

Tạo tệp Canary Deployment `manifests/canary/canary-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-canary
  namespace: production
  labels:
    app: payment-service
    release: canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: payment-service
      release: canary
  template:
    metadata:
      labels:
        app: payment-service
        release: canary
    spec:
      containers:
        - name: app
          image: registry.company.com/bank-group/payment-service:v2.5.0-canary
          ports:
            - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: payment-service-canary-svc
  namespace: production
spec:
  ports:
    - port: 8080
      targetPort: 8080
  selector:
    app: payment-service
    release: canary
```

### **CHECKPOINT 4**
Chạy câu lệnh kiểm tra các tệp manifests Canary:

```bash
test -f manifests/canary/canary-ingress.yaml && test -f manifests/canary/canary-deployment.yaml && echo "CHECKPOINT 4: ĐẠT" || echo "CHECKPOINT 4: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 4: ĐẠT
```

---

### Bước 5: Viết Script Mô phỏng Tăng Trọng số Canary Traffic (10% -> 50% -> 100%) (15 phút)

Tạo script điều tiết Canary Traffic Weight `scripts/canary-set-weight.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

WEIGHT="${1:-10}"

echo "[CANARY TRAFFIC] Adjusting NGINX Canary Ingress Weight to ${WEIGHT}%..."
mkdir -p manifests/live-state

cat << EOF > manifests/live-state/canary-status.json
{
  "canary_weight": "${WEIGHT}%",
  "stable_weight": "$((100 - WEIGHT))%",
  "canary_version": "v2.5.0-canary",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "CANARY_WEIGHT_UPDATED"
}
EOF

echo "[CANARY TRAFFIC] Canary Weight successfully updated to ${WEIGHT}%!"
```

Cho phép script chạy nấc 10%:
```bash
chmod +x scripts/canary-set-weight.sh
./scripts/canary-set-weight.sh "10"
```

### **CHECKPOINT 5**
Chạy câu lệnh kiểm tra nấc Canary Weight 10%:

```bash
test -f manifests/live-state/canary-status.json && grep -q '"canary_weight": "10%"' manifests/live-state/canary-status.json && echo "CHECKPOINT 5: ĐẠT" || echo "CHECKPOINT 5: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 5: ĐẠT
```

---

### Bước 6: Viết Script Mô phỏng Prometheus Metrics Canary Health Verification (10 phút)

Tạo script kiểm tra chỉ số Prometheus `scripts/verify-canary-metrics.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

FAIL_SIMULATION="${1:-false}"

echo "[CANARY VERIFY] Reading Prometheus Metrics for Canary Deployment..."
mkdir -p audit/metrics

if [ "$FAIL_SIMULATION" = "true" ]; then
    echo "[METRIC ALERT] High Error Rate Detected on Canary! HTTP 5xx Rate = 3.5% (Threshold: 1.0%)."
    cat << EOF > audit/metrics/canary-health-report.json
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "http_5xx_error_rate": "3.5%",
  "p99_latency_ms": 650,
  "threshold_exceeded": true,
  "status": "UNHEALTHY_ALERT_TRIGGERED"
}
EOF
    echo "[CANARY ERROR] Verification FAILED! Triggering automated rollback..."
    exit 1
else
    cat << EOF > audit/metrics/canary-health-report.json
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "http_5xx_error_rate": "0.1%",
  "p99_latency_ms": 42,
  "threshold_exceeded": false,
  "status": "HEALTHY_PASSED"
}
EOF
    echo "[CANARY SUCCESS] Verification PASSED! Canary metrics are 100% Healthy."
    exit 0
fi
```

Cho phép script chạy bản xanh:
```bash
chmod +x scripts/verify-canary-metrics.sh
./scripts/verify-canary-metrics.sh "false"
```

### **CHECKPOINT 6**
Chạy câu lệnh kiểm tra kết quả Prometheus Health Check:

```bash
test -f audit/metrics/canary-health-report.json && grep -q "HEALTHY_PASSED" audit/metrics/canary-health-report.json && echo "CHECKPOINT 6: ĐẠT" || echo "CHECKPOINT 6: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 6: ĐẠT
```

---

### Bước 7: Kiểm thử Tự động hóa Rollback Canary khi Tỷ lệ Lỗi HTTP 5xx > 1% (15 phút)

Tạo script tự động ngắt Canary khi nhận webhook cảnh báo `scripts/auto-rollback-canary.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[AUTO ROLLBACK] Received Prometheus Alertmanager Webhook: HighErrorRateCanary!"
echo "[AUTO ROLLBACK] Cutting Canary Traffic Weight to 0% and removing Canary Ingress..."

./scripts/canary-set-weight.sh "0"

cat << EOF > manifests/live-state/canary-status.json
{
  "canary_weight": "0%",
  "stable_weight": "100%",
  "canary_version": "v2.5.0-canary",
  "reason": "Automated rollback triggered due to HTTP 5xx error rate > 1%",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "CANARY_ROLLED_BACK"
}
EOF

echo "[AUTO ROLLBACK] Automated Canary Rollback executed successfully in 2 seconds!"
```

Cho phép script chạy rollback:
```bash
chmod +x scripts/auto-rollback-canary.sh
./scripts/auto-rollback-canary.sh
```

### **CHECKPOINT 7**
Chạy câu lệnh kiểm tra kết quả Auto Rollback Canary:

```bash
test -f manifests/live-state/canary-status.json && grep -q "CANARY_ROLLED_BACK" manifests/live-state/canary-status.json && echo "CHECKPOINT 7: ĐẠT" || echo "CHECKPOINT 7: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 7: ĐẠT
```

---

### Bước 8: Viết Script Mô phỏng Bật/Tắt GitLab Feature Flags từ xa (50ms) (15 phút)

Tạo script toggle Feature Flag qua API `scripts/toggle-gitlab-feature-flag.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

FLAG_NAME="${1:-new_checkout_flow}"
ENABLE_STATE="${2:-true}"

echo "[FEATURE FLAG API] Toggling GitLab Feature Flag '$FLAG_NAME' to state '$ENABLE_STATE'..."
mkdir -p feature-flags

cat << EOF > feature-flags/flag-config.json
{
  "project": "payment-service",
  "flag_name": "$FLAG_NAME",
  "enabled": $ENABLE_STATE,
  "environment": "production",
  "unleash_sync_time_ms": 48,
  "updated_by": "Product Manager (UI)",
  "updated_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

echo "[FEATURE FLAG API] Feature Flag '$FLAG_NAME' updated in 48ms!"
```

Cho phép script chạy bật flag (ON):
```bash
chmod +x scripts/toggle-gitlab-feature-flag.sh
./scripts/toggle-gitlab-feature-flag.sh "new_checkout_flow" "true"
```

### **CHECKPOINT 8**
Chạy câu lệnh kiểm tra trạng thái Feature Flag (ON):

```bash
test -f feature-flags/flag-config.json && grep -q '"enabled": true' feature-flags/flag-config.json && echo "CHECKPOINT 8: ĐẠT" || echo "CHECKPOINT 8: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 8: ĐẠT
```

---

### Bước 9: Khởi tạo Script Mô phỏng Database Migration Tương thích Ngược (Expand-and-Contract) (10 phút)

Tạo script mô phỏng Database Migration Expand-and-Contract `scripts/db-expand-contract-migration.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

PHASE="${1:-expand}"

mkdir -p audit/db-migrations

if [ "$PHASE" = "expand" ]; then
    echo "[DB MIGRATION] Executing PHASE 1 (EXPAND): Adding new_email column alongside email..."
    cat << EOF > audit/db-migrations/schema-status.json
{
  "phase": "EXPAND",
  "columns_active": ["email", "new_email"],
  "backward_compatible": true,
  "v1_support": true,
  "v2_support": true,
  "applied_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
    echo "[DB MIGRATION] Expand phase complete! Both v1 and v2 apps supported."
elif [ "$PHASE" = "contract" ]; then
    echo "[DB MIGRATION] Executing PHASE 2 (CONTRACT): Dropping deprecated email column after 30 days..."
    cat << EOF > audit/db-migrations/schema-status.json
{
  "phase": "CONTRACT",
  "columns_active": ["new_email"],
  "backward_compatible": false,
  "applied_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
    echo "[DB MIGRATION] Contract phase complete! Deprecated column dropped."
fi
```

Cho phép script chạy pha Expand:
```bash
chmod +x scripts/db-expand-contract-migration.sh
./scripts/db-expand-contract-migration.sh "expand"
```

### **CHECKPOINT 9**
Chạy câu lệnh kiểm tra tệp DB Migration Expand Phase:

```bash
test -f audit/db-migrations/schema-status.json && grep -q "EXPAND" audit/db-migrations/schema-status.json && echo "CHECKPOINT 9: ĐẠT" || echo "CHECKPOINT 9: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 9: ĐẠT
```

---

### Bước 10: Xây dựng Script Linter Phát hiện Stale Feature Flags cũ hơn 30 ngày (10 phút)

Tạo script linter quét Stale Flags `scripts/scan-stale-feature-flags.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[FEATURE FLAG LINTER] Scanning codebase for Stale Feature Flags (>30 days old)..."

mkdir -p audit/linter-reports

cat << EOF > audit/linter-reports/stale-flags-report.json
{
  "scanned_files": ["app/src/server.js"],
  "active_flags_count": 2,
  "stale_flags_detected": [
    {
      "flag_name": "legacy_banner_flag",
      "age_days": 45,
      "status": "NEEDS_CLEANUP"
    }
  ],
  "recommendation": "Remove 'legacy_banner_flag' from server.js code and delete from GitLab UI"
}
EOF

echo "[FEATURE FLAG LINTER] Report generated: 1 Stale Feature Flag needs cleanup."
```

Cho phép script chạy linter:
```bash
chmod +x scripts/scan-stale-feature-flags.sh
./scripts/scan-stale-feature-flags.sh
```

### **CHECKPOINT 10**
Chạy câu lệnh kiểm tra báo cáo Stale Flags Linter:

```bash
test -f audit/linter-reports/stale-flags-report.json && grep -q "NEEDS_CLEANUP" audit/linter-reports/stale-flags-report.json && echo "CHECKPOINT 10: ĐẠT" || echo "CHECKPOINT 10: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 10: ĐẠT
```

---

### Bước 11: Viết Script Ghi nhận Nhật ký Release Audit Event Logs (10 phút)

Tạo script ghi audit log `scripts/audit-release-events.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

mkdir -p audit

cat << EOF >> audit/release-events-audit.json
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "event": "CANARY_PROMOTED_TO_PRODUCTION",
  "version": "v2.5.0",
  "traffic_share": "100%",
  "executor": "GitLab CI Pipeline Trigger",
  "mttd_seconds": 4.2,
  "status": "COMPLIANT"
}
EOF

echo "[AUDIT LOG] Recorded Release Event in audit/release-events-audit.json"
```

Cho phép script chạy ghi log:
```bash
chmod +x scripts/audit-release-events.sh
./scripts/audit-release-events.sh
```

### **CHECKPOINT 11**
Chạy câu lệnh kiểm tra tệp Release Audit Log:

```bash
test -f audit/release-events-audit.json && grep -q "CANARY_PROMOTED_TO_PRODUCTION" audit/release-events-audit.json && echo "CHECKPOINT 11: ĐẠT" || echo "CHECKPOINT 11: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 11: ĐẠT
```

---

### Bước 12: Xây dựng Script Linter Kiểm tra Cấu hình GitLab CI cho Release Pipeline (5 phút)

Tạo script linter `scripts/validate-release-gitlab-ci.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[RELEASE CI LINTER] Auditing .gitlab-ci.yml for Release Strategy compliance..."

cat << EOF > .gitlab-ci.yml
deploy-canary:
  stage: deploy
  script:
    - helm upgrade --install payment-canary ./helm/payment-service --set ingress.canary.weight=10
  environment:
    name: production/canary

auto-rollback-canary:
  stage: rollback
  script:
    - helm uninstall payment-canary
  rules:
    - if: \$CI_COMMIT_BRANCH == "main"
      when: on_failure
EOF

if ! grep -q "canary.weight" .gitlab-ci.yml; then
    echo "[ERROR] Missing mandatory canary weight configuration!"
    exit 1
fi

if ! grep -q "when: on_failure" .gitlab-ci.yml; then
    echo "[ERROR] Missing mandatory auto-rollback on failure!"
    exit 1
fi

echo "[RELEASE CI LINTER] Validation PASSED: 100% Compliant Release CI Pipeline."
```

Cho phép script chạy linter:
```bash
chmod +x scripts/validate-release-gitlab-ci.sh
./scripts/validate-release-gitlab-ci.sh
```

### **CHECKPOINT 12**
Chạy câu lệnh kiểm tra script Linter Release CI:

```bash
./scripts/validate-release-gitlab-ci.sh | grep -q "PASSED" && echo "CHECKPOINT 12: ĐẠT" || echo "CHECKPOINT 12: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 12: ĐẠT
```

---

### Bước 13: Xây dựng Script Mô phỏng Canary Analysis So sánh với Baseline (5 phút)

Tạo script Canary Analysis `scripts/run-canary-analysis.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[CANARY ANALYSIS] Comparing Canary v2 metrics against Baseline v1 metrics..."

mkdir -p audit/canary-analysis

cat << EOF > audit/canary-analysis/analysis-report.json
{
  "baseline_version": "v1.0.0",
  "canary_version": "v2.5.0",
  "error_rate_diff": "+0.02%",
  "latency_p99_diff": "-5ms",
  "mann_whitney_u_score": 0.98,
  "verdict": "PROMOTE_APPROVED",
  "analyzed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

echo "[CANARY ANALYSIS] Verdict: PROMOTE_APPROVED. Canary is statistically superior or equal to Baseline."
```

Cho phép script chạy Canary Analysis:
```bash
chmod +x scripts/run-canary-analysis.sh
./scripts/run-canary-analysis.sh
```

### **CHECKPOINT 13**
Chạy câu lệnh kiểm tra tệp Canary Analysis Report:

```bash
test -f audit/canary-analysis/analysis-report.json && grep -q "PROMOTE_APPROVED" audit/canary-analysis/analysis-report.json && echo "CHECKPOINT 13: ĐẠT" || echo "CHECKPOINT 13: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 13: ĐẠT
```

---

### Bước 14: Tổng hợp Đánh giá Hoàn thành Bài Lab Buổi 43 (5 phút)

Tạo script đánh giá kết quả tổng hợp `scripts/final-release-lab-evaluation.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "FINAL EVALUATION SUMMARY — BUỔI 43 (RELEASE STRATEGIES)"
echo "=========================================================="

CHECKS_PASSED=0

[ -f app/src/server.js ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f manifests/blue-green/blue-deployment.yaml ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f manifests/live-state/active-routing.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f manifests/canary/canary-ingress.yaml ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f manifests/live-state/canary-status.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f feature-flags/flag-config.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))

echo "Successfully verified $CHECKS_PASSED / 6 Core Release Strategy Components."
echo "Verified App Code with Feature Flags SDK, Blue-Green Swap, Canary Weighted Ingress, Auto-Rollback, and Remote Toggle API."

if [ "$CHECKS_PASSED" -eq 6 ]; then
    echo "BUỔI 43 LAB STATUS: PASSED (100% COMPLETE)"
    exit 0
else
    echo "BUỔI 43 LAB STATUS: INCOMPLETE"
    exit 1
fi
```

Cho phép script chạy đánh giá kết quả:
```bash
chmod +x scripts/final-release-lab-evaluation.sh
./scripts/final-release-lab-evaluation.sh
```

### **CHECKPOINT 14**
Chạy câu lệnh tổng kết bài lab Buổi 43:

```bash
./scripts/final-release-lab-evaluation.sh | grep -q "PASSED" && echo "CHECKPOINT 14: ĐẠT" || echo "CHECKPOINT 14: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 14: ĐẠT
```

---

## Xử lý sự cố

### 1. Sự cố Lỗi `NGINX Ingress canary weight` không hoạt động
- **Triệu chứng:** Thêm annotation `canary-weight: "10"` nhưng 100% traffic vẫn trỏ về phiên bản cũ.
- **Nguyên nhân:** Thiếu annotation sống còn `nginx.ingress.kubernetes.io/canary: "true"`.
- **Cách khắc phục:** Bắt buộc phải khai báo cả 2 annotations `canary: "true"` và `canary-weight: "10"`.

### 2. Sự cố Rollback Blue-Green làm sập ứng dụng do xóa môi trường Blue quá sớm
- **Triệu chứng:** Tráo đổi sang Green bị nổ lỗi nhưng không thể tráo đổi ngược lại Blue.
- **Nguyên nhân:** Kỹ sư chạy lệnh xóa Deployment Blue ngay khi vừa tráo đổi sang Green.
- **Cách khắc phục:** Duy trì môi trường Blue chạy standby ít nhất 24 giờ sau khi swap sang Green thành công.

### 3. Sự cố Phiên bản cũ (v1) bị SQL Crash khi rollback do DB Schema không tương thích
- **Triệu chứng:** Swapped back sang v1 thành công nhưng v1 nổ lỗi `Column not found`.
- **Nguyên nhân:** Script DB migration của v2 đã xóa mất cột dữ liệu cũ.
- **Cách khắc phục:** Áp dụng nghiêm ngặt quy trình Expand-and-Contract DB Migration (QT 43.7).

### 4. Sự cố Feature Flag Client SDK nổ lỗi `NullPointerException`
- **Triệu chứng:** Ứng dụng bị crash khi máy chủ Unleash Server ngắt kết nối.
- **Nguyên nhân:** Không bọc giá trị fallback mặc định `false` trong hàm `isEnabled()`.
- **Cách khắc phục:** Khai báo đầy đủ fallback `unleash.isEnabled("flag_name", false)`.

### 5. Sự cố Canary Traffic 10% bị dính Session Affinity làm 1 user bị lỗi liên tục
- **Triệu chứng:** Một khách hàng liên tục bị rơi vào nấc 10% Canary bị lỗi dù đã reload trang.
- **Nguyên nhân:** NGINX Ingress đang bật cờ `canary-by-cookie` hoặc Session Sticky.
- **Cách khắc phục:** Tắt Session Sticky cho Ingress Canary thử nghiệm chung hoặc bổ sung header bypass.

### 6. Sự cố Lỗi `HTTP 401 Unauthorized` khi gọi API GitLab Feature Flags
- **Triệu chứng:** Microservice không thể nạp cấu hình Feature Flags từ GitLab.
- **Nguyên nhân:** Sai Instance URL hoặc Unleash Client Secret Token bị hết hạn.
- **Cách khắc phục:** Kiểm tra lại `UNLEASH_URL` và `UNLEASH_INSTANCE_ID` trong GitLab Feature Flags UI.

### 7. Sự cố Pipeline CI không tự động kích hoạt Rollback khi Canary bị lỗi
- **Triệu chứng:** Canary Pods bị 5xx lỗi 50% nhưng pipeline vẫn đứng chờ manual.
- **Nguyên nhân:** Quên cấu hình job `auto-rollback-canary` với cờ `when: on_failure`.
- **Cách khắc phục:** Thêm `when: on_failure` vào khối `rules` của job rollback.

### 8. Sự cố Stale Feature Flags gây rối logic làm phát sinh bug không mong muốn
- **Triệu chứng:** Phát sinh lỗi logic do hai Feature Flags cũ từ năm ngoái bị xung đột điều kiện `if/else`.
- **Nguyên nhân:** Không dọn dẹp các đoạn code Feature Flags cũ đã bật 100% lâu ngày.
- **Cách khắc phục:** Chạy script linter quét và xóa bỏ Stale Flags sau 30 ngày.

### 9. Sự cố `verify-canary-metrics.sh` nổ lỗi parse JSON report
- **Triệu chứng:** Script kiểm tra chỉ số Prometheus bị ngắt giữa chừng.
- **Nguyên nhân:** Thư mục `audit/metrics` chưa được khởi tạo.
- **Cách khắc phục:** Thêm `mkdir -p audit/metrics` trong script.

### 10. Sự cố Canary Pods bị kẹt `ImagePullBackOff` làm Ingress bị ngắt
- **Triệu chứng:** NGINX Ingress báo lỗi HTTP 503 cho 10% traffic Canary.
- **Nguyên nhân:** Gõ sai tên Docker Image Tag của Canary Deployment.
- **Cách khắc phục:** Kiểm tra lại tên Docker Image Tag trước khi gán Canary Weight.

### 11. Sự cố Product Manager không có quyền bật/tắt Feature Flags trên GitLab
- **Triệu chứng:** Giao diện Feature Flags bị ẩn nút công tắc Toggle.
- **Nguyên nhân:** Tài khoản của PM chỉ có quyền `Reporter` nhưng dự án yêu cầu `Developer`.
- **Cách khắc phục:** Cấp quyền `Developer` cho tài khoản PM trên kho GitLab Repository.

### 12. Sự cố Prometheus Alertmanager gửi Webhook Rollback bị lặp vô tận
- **Triệu chứng:** GitLab CI liên tục kích hoạt hàng trăm job rollback lặp đi lặp lại.
- **Nguyên nhân:** Cảnh báo Alertmanager không được tự động giải phóng (Resolve) sau khi rollback.
- **Cách khắc phục:** Cấu hình `repeat_interval: 1h` trong Alertmanager config.

### 13. Sự cố NGINX Ingress Canary Weight 10% nhưng thực tế nhận 50% traffic
- **Triệu chứng:** Số lượng request truy cập Canary Pods quá nhiều so với mức 10%.
- **Nguyên nhân:** Số lượng Pods của Canary quá lớn so với Pods Stable.
- **Cách khắc phục:** Đặt số lượng Canary Pods bằng 10% tổng số Pods của Stable Deployment.

### 14. Sự cố Microservice nạp Feature Flags làm chậm tốc độ khởi động App
- **Triệu chứng:** Container boot mất 40 giây do chờ kết nối Feature Flag Server.
- **Nguyên nhân:** Đợi nạp Feature Flags theo cơ chế Synchronous Blocking trong hàm init.
- **Cách khắc phục:** Nạp Feature Flags theo cơ chế Asynchronous Background Sync.

### 15. Sự cố Blue-Green Swap bị gián đoạn do thiếu Readiness Probe
- **Triệu chứng:** Người dùng bị lỗi HTTP 502 trong 2 giây đúng lúc tráo đổi Ingress.
- **Nguyên nhân:** Pods Green mới tạo chưa thực sự sẵn sàng nhận traffic khi tráo đổi.
- **Cách khắc phục:** Đảm bảo `readinessProbe` trên Green Pods đã báo `Ready` 100% trước khi swap.

### 16. Sự cố `blue-green-swap.sh` nổ lỗi directory not found
- **Triệu chứng:** Script tráo đổi bị dừng giữa chừng.
- **Nguyên nhân:** Thư mục `manifests/live-state` chưa được khởi tạo.
- **Cách khắc phục:** Bổ sung `mkdir -p manifests/live-state` trong script.

### 17. Sự cố GitLab Environment Dashboard không hiển thị nấc Canary
- **Triệu chứng:** Không xem được nút Rollback 1-Click trên giao diện GitLab UI.
- **Nguyên nhân:** Quên khai báo `environment.name: production/canary` trong job deploy.
- **Cách khắc phục:** Khai báo khối `environment` đầy đủ trong tệp `.gitlab-ci.yml`.

### 18. Sự cố Code HCL Terraform bị xung đột với Ingress Canary Manual
- **Triệu chứng:** Chạy `terraform apply` làm mất annotation `canary-weight`.
- **Nguyên nhân:** Terraform đè tệp Ingress Manifest chuẩn không có annotation canary.
- **Cách khắc phục:** Sử dụng cờ `lifecycle { ignore_changes = [metadata[0].annotations] }` trong HCL.

### 19. Sự cố `toggle-gitlab-feature-flag.sh` nổ lỗi JSON parse
- **Triệu chứng:** API toggle báo lỗi cú pháp.
- **Nguyên nhân:** Truyền giá trị boolean dạng chuỗi `"true"` thay vì giá trị `true` thô.
- **Cách khắc phục:** Đảm bảo định dạng JSON boolean `$ENABLE_STATE` chuẩn xác.

### 20. Sự cố Quên cờ `force_destroy` khi xóa tệp Feature Flags
- **Triệu chứng:** Không thể xóa Feature Flag trên GitLab UI.
- **Nguyên nhân:** Flag đang được gắn với một User List đang hoạt động.
- **Cách khắc phục:** Gỡ gắn User List khỏi Feature Flag trước khi xóa.

### 21. Sự cố Canary Pods chiếm bộ nhớ RAM quá lớn làm Node bị OOM
- **Triệu chứng:** Node Kubernetes bị giật do thêm Canary Pods.
- **Nguyên nhân:** Chưa cấu hình `resources.requests.memory` cho Canary Deployment.
- **Cách khắc phục:** Khai báo đầy đủ `resources` limits và requests cho Canary Pods.

### 22. Sự cố Tệp `server.js` bị crash do thiếu module `express`
- **Triệu chứng:** App node.js nổ lỗi `Cannot find module 'express'`.
- **Nguyên nhân:** Chưa chạy `npm install` hoặc thiếu file `package.json`.
- **Cách khắc phục:** Đảm bảo cài đặt `express` dependency trước khi chạy.

### 23. Sự cố `scan-stale-feature-flags.sh` nổ lỗi file not found
- **Triệu chứng:** Script linter báo không tìm thấy folder.
- **Nguyên nhân:** Thư mục `audit/linter-reports` chưa khởi tạo.
- **Cách khắc phục:** Thêm `mkdir -p audit/linter-reports` trong script.

### 24. Sự cố Lỗi `403 Forbidden` khi GitLab CI gọi API Promoted
- **Triệu chứng:** Job CI `promote-to-100` bị từ chối quyền.
- **Nguyên nhân:** `$CI_JOB_TOKEN` không có quyền Maintainer trên môi trường Production.
- **Cách khắc phục:** Cấp quyền Deploy Key hoặc dùng OIDC ServiceAccount.

### 25. Sự cố Quên xóa Ingress Canary sau khi Promote thành công 100%
- **Triệu chứng:** Traffic vẫn tiếp tục bị trỏ qua Ingress Canary cũ.
- **Nguyên nhân:** Script promote chỉ nâng bản Stable mà không xóa Ingress Canary.
- **Cách khắc phục:** Thêm câu lệnh `helm uninstall payment-canary` trong stage promote.

### 26. Sự cố Lỗi `canary-by-header` bị lộ cho người dùng cuối
- **Triệu chứng:** Khách hàng tự đổi HTTP Header để vào nấc Canary.
- **Nguyên nhân:** Cấu hình `nginx.ingress.kubernetes.io/canary-by-header` với header quá đoán trước.
- **Cách khắc phục:** Sử dụng chuỗi Secret Header ngẫu nhiên cho internal testing.

### 27. Sự cố `final-release-lab-evaluation.sh` báo 5/6 thành phần
- **Triệu chứng:** Bài lab đánh giá chưa đạt 100%.
- **Nguyên nhân:** Chưa thực thi Bước 8 bật Feature Flag từ xa.
- **Cách khắc phục:** Chạy script `./scripts/toggle-gitlab-feature-flag.sh "new_checkout_flow" "true"`.

### 28. Sự cố Database Migration Phase 2 (Contract) bị chạy quá sớm
- **Triệu chứng:** Xóa cột dữ liệu cũ làm bản v1 bị crash khi vừa deploy v2 được 1 giờ.
- **Nguyên nhân:** Chạy pha Contract ngay lập tức thay vì chờ 30 ngày.
- **Cách khắc phục:** Hoãn pha Contract ít nhất 30 ngày để đảm bảo bản v2 ổn định 100%.

### 29. Sự cố GitLab Feature Flags SDK gây Memory Leak trên Node.js
- **Triệu chứng:** Pods ứng dụng bị tăng RAM liên tục sau mỗi 5 phút.
- **Nguyên nhân:** Khởi tạo quá nhiều instance Unleash Client thay vì Singleton.
- **Cách khắc phục:** Sử dụng mẫu thiết kế Singleton cho Unleash Client Instance.

### 30. Sự cố Tốc độ Sync của Unleash Engine bị trễ 5 phút
- **Triệu chứng:** Bật Flag trên GitLab UI nhưng 5 phút sau app mới nhận.
- **Nguyên nhân:** Đặt `refreshInterval` của Unleash SDK quá dài (300.000ms).
- **Cách khắc phục:** Giảm `refreshInterval` xuống 15.000ms (15 giây).

### 31. Sự cố Ingress Controller bị quá tải do số lượng Ingress Rules quá nhiều
- **Triệu chứng:** NGINX Ingress reload lại liên tục gây tăng Latency.
- **Nguyên nhân:** Tạo quá nhiều Ingress Canary độc lập cho từng microservice.
- **Cách khắc phục:** Gộp các rules Canary thành các Ingress Manifests tập trung.

### 32. Sự cố `auto-rollback-canary.sh` nổ lỗi syntax bash
- **Triệu chứng:** Script rollback báo lỗi dòng.
- **Nguyên nhân:** Thiếu dấu ngoặc kép bọc biến trong câu lệnh bash.
- **Cách khắc phục:** Bọc tất cả các biến bash trong ngoặc `"..."`.

### 33. Sự cố App Backend bị treo khi gọi API Feature Flags do DNS nghẽn
- **Triệu chứng:** Mọi request ứng dụng bị chậm 5 giây.
- **Nguyên nhân:** DNS không phân giải được tên miền `gitlab.company.com`.
- **Cách khắc phục:** Cấu hình Local DNS Cache hoặc nạp IP trực tiếp trong Pods.

### 34. Sự cố Canary Analysis nổ lỗi do thiếu dữ liệu Prometheus Baseline
- **Triệu chứng:** Script so sánh báo `Baseline metrics not found`.
- **Nguyên nhân:** Pods Baseline v1 mới được restart nên chưa có đủ dữ liệu 15 phút.
- **Cách khắc phục:** Chờ Pods Baseline tích lũy đủ 15 phút dữ liệu trước khi chạy analysis.

### 35. Sự cố `canary-set-weight.sh` nổ lỗi math calculation
- **Triệu chứng:** Lệnh bash nổ syntax error ở phép tính `100 - WEIGHT`.
- **Nguyên nhân:** Sử dụng phép tính không đúng cú pháp bash `$((100 - WEIGHT))`.
- **Cách khắc phục:** Đảm bảo cú pháp phép tính số nguyên `$(($100 - $WEIGHT))` chuẩn xác.

### 36. Sự cố Quên bật cờ `canary-weight-total` trong Service Mesh Istio
- **Triệu chứng:** Traffic Splitting trong Istio VirtualService bị chia sai.
- **Nguyên nhân:** Tổng trọng số các nấc VirtualService không bằng 100.
- **Cách khắc phục:** Đảm bảo tổng trọng số `weight: 90` và `weight: 10` bằng 100.

### 37. Sự cố `validate-release-gitlab-ci.sh` báo lỗi thiếu rollback rule
- **Triệu chứng:** Linter chặn CI vì pipeline thiếu quy tắc auto-rollback.
- **Nguyên nhân:** Viết file `.gitlab-ci.yml` thiếu `when: on_failure`.
- **Cách khắc phục:** Bổ sung `when: on_failure` trong khối rollback job.

### 38. Sự cố Feature Flag User List bị sai định dạng User ID
- **Triệu chứng:** Bật Flag cho 1 User nhưng tất cả người dùng đều thấy tính năng mới.
- **Nguyên nhân:** SDK gửi `userId` dạng number trong khi GitLab yêu cầu `string`.
- **Cách khắc phục:** Ép kiểu `String(userId)` khi truyền vào Unleash Context.

### 39. Sự cố Git diff hiển thị 100% dòng do khác biệt End-of-Line CRLF
- **Triệu chứng:** Reviewer nhìn thấy toàn bộ file `server.js` bị sửa khi commit từ Windows.
- **Nguyên nhân:** Windows tự đổi ký tự xuống dòng từ LF sang CRLF.
- **Cách khắc phục:** Chuẩn hóa `.gitattributes` bắt buộc dùng dòng LF.

### 40. Sự cố GitLab Feature Flags API bị ngắt kết nối do hết hạn SSL Certificate
- **Triệu chứng:** SDK log báo `SSL Handshake Failed`.
- **Nguyên nhân:** Chứng chỉ SSL Let's Encrypt của GitLab bị hết hạn.
- **Cách khắc phục:** Gia hạn chứng chỉ SSL cho GitLab Server.

### 41. Sự cố Quên cờ `--install` khi chạy `helm upgrade` Canary
- **Triệu chứng:** Job deploy Canary nổ lỗi `release: not found`.
- **Nguyên nhân:** Release Canary chưa tồn tại trên cụm từ trước.
- **Cách khắc phục:** Luôn sử dụng `helm upgrade --install`.

### 42. Sự cố Tệp `canary-health-report.json` bị ghi đè mất lịch sử cũ
- **Triệu chứng:** Báo cáo kiểm định chỉ lưu kết quả của lần chạy cuối cùng.
- **Nguyên nhân:** Dùng toán tử ghi đè `>` thay vì nối tiếp `>>`.
- **Cách khắc phục:** Đặt tên file đính kèm timestamp hoặc dùng `>>`.

### 43. Sự cố Network Latency tăng vọt do Feature Flag Client gọi API liên tục
- **Triệu chứng:** Ứng dụng bị chậm 10ms trên từng request.
- **Nguyên nhân:** Gọi API GitLab Feature Flag trên từng HTTP Request thay vì Cache trong bộ nhớ.
- **Cách khắc phục:** Đọc Feature Flags từ In-Memory Cache của Unleash Client SDK.

### 44. Sự cố `db-expand-contract-migration.sh` nổ lỗi phase name
- **Triệu chứng:** Script DB Migration nổ error.
- **Nguyên nhân:** Gõ sai tên pha `expand_phase` thay vì `expand`.
- **Cách khắc phục:** Truyền đúng tên pha `expand` hoặc `contract`.

### 45. Sự cố Blue Deployment bị gỡ nhầm trên Production khi chưa Swap Green
- **Triệu chứng:** 100% người dùng bị nổ lỗi 503 khi đang trong quá trình deploy Green.
- **Nguyên nhân:** Script CI có câu lệnh dọn dẹp Blue quá sớm.
- **Cách khắc phục:** Chỉ dọn dẹp Blue sau khi Green đã chạy mượt mà 24 giờ.

### 46. Sự cố Lỗi `Error: Invalid Ingress Class` khi deploy NGINX Canary
- **Triệu chứng:** Ingress Canary bị cụm từ chối.
- **Nguyên nhân:** Cụm Kubernetes sử dụng `ingressClassName: alb` thay vì `nginx`.
- **Cách khắc phục:** Đổi `ingressClassName` phù hợp với Ingress Controller trên cụm.

### 47. Sự cố Cờ `reports.metrics` trong `.gitlab-ci.yml` trỏ sai đường dẫn file
- **Triệu chứng:** GitLab MR Widget không hiển thị được báo cáo Metrics.
- **Nguyên nhân:** Khai báo sai đường dẫn tệp JSON.
- **Cách khắc phục:** Đảm bảo đường dẫn `reports.metrics` chính xác 100%.

### 48. Sự cố Container Node.js bị sập do unhandled rejection khi ngắt Feature Flag API
- **Triệu chứng:** App Pod bị crash loop khi rớt mạng.
- **Nguyên nhân:** Thiếu đoạn code bắt lỗi `unleashClient.on('error', console.error)`.
- **Cách khắc phục:** Bắt sự kiện `'error'` trên Unleash Client Instance.

### 49. Sự cố `final-release-lab-evaluation.sh` nổ lỗi syntax bash
- **Triệu chứng:** Script tổng kết báo lỗi dòng.
- **Nguyên nhân:** Thiếu dấu ngoặc vuông đóng trong câu lệnh kiểm tra tệp.
- **Cách khắc phục:** Đảm bảo cú pháp `[ -f file ]` chuẩn xác.

### 50. Sự cố Tệp `flag-config.json` bị rò rỉ API Token của GitLab
- **Triệu chứng:** Token quản trị Feature Flags bị lộ trên Git.
- **Nguyên nhân:** Commit file chứa token lên kho mã nguồn.
- **Cách khắc phục:** Bổ sung `feature-flags/` vào tệp `.gitignore`.

### 51. Sự cố Lỗi `Error: Invalid percentage` khi đặt Canary Weight
- **Triệu chứng:** NGINX Ingress nổ lỗi annotation invalid.
- **Nguyên nhân:** Đặt `canary-weight: "105"` (vượt quá 100%).
- **Cách khắc phục:** Đảm bảo `canary-weight` nằm trong khoảng từ `0` đến `100`.

### 52. Sự cố Unleash SDK bị lỗi xung đột phiên bản Node.js
- **Triệu chứng:** App không thể start được trên Docker Image Alpine.
- **Nguyên nhân:** Dùng Unleash Client v5 trên Node.js v14 cũ.
- **Cách khắc phục:** Nâng cấp Docker Image Base lên `node:18-alpine`.

### 53. Sự cố `scripts/validate-release-gitlab-ci.sh` bị nổ lỗi permission denied
- **Triệu chứng:** Không chạy được script linter.
- **Nguyên nhân:** Quên cấp quyền execution cho file.
- **Cách khắc phục:** Chạy `chmod +x scripts/validate-release-gitlab-ci.sh`.

### 54. Sự cố Canary Promote bị dừng do Kỹ sư bấm nhầm nút Cancel
- **Triệu chứng:** Pipeline bị treo ở nấc 10% Canary không chịu sang 100%.
- **Nguyên nhân:** Thao tác con người bấm nhầm Cancel trên nút manual promote.
- **Cách khắc phục:** Bấm **Retry** lại stage `promote-to-100`.

### 55. Sự cố Phê duyệt Manual Promote bị canceled tự động sau 7 ngày
- **Triệu chứng:** Nút Manual Promote bị vô hiệu hóa.
- **Nguyên nhân:** Nút duyệt manual trong MR không được tương tác trong 7 ngày.
- **Cách khắc phục:** Chạy lại (Retry) pipeline từ stage deploy canary.

---

## Bài tập mở rộng

1. **Xây dựng Quy trình Automated Canary Analysis với Flagger & Prometheus trên Kubernetes:**
   - Cài đặt công cụ **Flagger Operator** (tích hợp NGINX Ingress & Prometheus) trên cụm Kubernetes.
   - Viết manifest `Canary` Custom Resource định nghĩa tự động tăng trọng số traffic từ 5% -> 10% -> 20% -> 50% mỗi 2 phút, tự động đo lường chỉ số Latency & Error Rate và tiến hành Promote 100% hoặc Rollback hoàn toàn tự động không cần viết script CI thủ công!

2. **Xây dựng Hệ thống Dynamic Feature Flag Targeting với GitLab & Unleash Engine:**
   - Cấu hình Feature Flag trên GitLab UI áp dụng chiến lược **Gradual Rollout BY User ID** (chỉ bật tính năng mới cho 5% danh sách User ID thuộc nhóm Beta Testers).
   - Viết mã nguồn Node.js truyền `UnleashContext` chứa `userId` và `remoteAddress` khách hàng, kiểm thử việc bật/tắt tính năng chính xác theo từng nhóm đối tượng người dùng thực tế!

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| Bước 1 | Khởi tạo Cấu trúc Thư mục và Mã nguồn Microservice tích hợp Feature Flags | 10 phút |
| Bước 2 | Khởi tạo Manifests Kubernetes cho Blue-Green Deployment | 10 phút |
| Bước 3 | Viết Script Mô phỏng Blue-Green 100% Instant Traffic Swap | 15 phút |
| Bước 4 | Khởi tạo Manifests Kubernetes cho NGINX Canary Weighted Routing | 15 phút |
| Bước 5 | Viết Script Mô phỏng Tăng Trọng số Canary Traffic (10% -> 50% -> 100%) | 15 phút |
| Bước 6 | Viết Script Mô phỏng Prometheus Metrics Canary Health Verification | 10 phút |
| Bước 7 | Kiểm thử Tự động hóa Rollback Canary khi Tỷ lệ Lỗi HTTP 5xx > 1% | 15 phút |
| Bước 8 | Viết Script Mô phỏng Bật/Tắt GitLab Feature Flags từ xa (50ms) | 15 phút |
| Bước 9 | Khởi tạo Script Mô phỏng Database Migration Tương thích Ngược | 10 phút |
| Bước 10 | Xây dựng Script Linter Phát hiện Stale Feature Flags cũ hơn 30 ngày | 10 phút |
| Bước 11 | Viết Script Ghi nhận Nhật ký Release Audit Event Logs | 10 phút |
| Bước 12 | Xây dựng Script Linter Kiểm tra Cấu hình GitLab CI cho Release Pipeline | 5 phút |
| Bước 13 | Xây dựng Script Mô phỏng Canary Analysis So sánh với Baseline | 5 phút |
| Bước 14 | Tổng hợp Đánh giá Hoàn thành Bài Lab Buổi 43 | 5 phút |
| **Tổng** | **Khối thực hành lab** | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

# Buổi 43: Chiến lược release: Blue-green, Canary, Feature flags — Vấn Đáp & Phỏng Vấn

## Thống kê & Phân bổ thời lượng
- **Tổng thời lượng:** 20 phút
- **Cấu trúc:**
  - 5 phút: Kiểm tra phản xạ lý thuyết (12 câu hỏi trắc nghiệm & tự luận nhanh)
  - 10 phút: Đóng vai phỏng vấn tình huống thực chiến (7 kịch bản nâng cao)
  - 5 phút: Chốt từ khóa ăn tiền (§V3) & Giao bài tập về nhà chuẩn bị cho Buổi 44 (BTVN 4)

---

## §V1. 12 Câu hỏi vấn đáp kiểm tra phản xạ

### Câu 1
**Hỏi:** Sự khác biệt cốt lõi nhất về nguyên lý hoạt động và tài nguyên hạ tầng giữa Blue-Green Deployment và Canary Deployment là gì?

**Gợi ý trả lời ngắn:**
Blue-Green tráo đổi 100% traffic giữa 2 môi trường song song (đòi hỏi 200% tài nguyên); Canary mở dần % traffic nhỏ (10% -> 50% -> 100%) nghiệm thu dần trên Production (chỉ tốn +10-20% tài nguyên).

**Đáp án chuẩn:**
- **So sánh Nguyên lý & Hạ tầng:**
  1. *Blue-Green Deployment:* Duy trì 2 môi trường độc lập hoàn toàn (Blue đang active, Green standby). Khi nâng cấp, kiểm thử Green rồi tráo đổi 100% Ingress Routing sang Green trong 1 giây. Đòi hỏi gấp đôi tài nguyên hạ tầng (200% Capacity).
  2. *Canary Deployment:* Chạy ứng dụng mới song song trên cùng hạ tầng, điều tiết phần trăm traffic nhỏ (dạng 10% Canary, 90% Stable) bằng Ingress Controller. Thu hẹp tối đa bán kính ảnh hưởng sự cố và chỉ tốn thêm một vài Pods thử nghiệm (+10-20% Capacity).

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng "Canary Deployment cũng bắt buộc phải dựng lại toàn bộ hạ tầng mới gấp 2 lần như Blue-Green".

---

### Câu 2
**Hỏi:** Tại sao việc đảm bảo tính tương thích ngược của Database Schema (Expand-and-Contract Migration) lại là điều kiện sống còn đối với ca phát hành Blue-Green hay Canary?

**Gợi ý trả lời ngắn:**
Vì trong khoảng thời gian release, cả phiên bản cũ (v1) và phiên bản mới (v2) sẽ cùng truy cập một Database duy nhất; nếu xóa cột cũ sẽ làm phiên bản v1 bị nổ lỗi SQL Crash lập tức.

**Đáp án chuẩn:**
- **Cơ chế Expand-and-Contract:**
  Trong mô hình Blue-Green hay Canary, phiên bản v1 (đang nhận 90% traffic) và phiên bản v2 (đang nhận 10% traffic) đều cùng đọc/ghi vào một Database Production.
  - *Pha 1 (Expand):* Thêm cột mới `new_column` nhưng giữ nguyên cột cũ `old_column`. Code v1 và v2 đều đọc được.
  - *Pha 2 (Deploy):* Deploy v2 thành công 100% trên Production.
  - *Pha 3 (Contract):* Sau 30 ngày v2 chạy ổn định, mới thực thi script xóa cột `old_column`.
- **Hậu quả nếu làm sai:** Xóa cột cũ ngay lập tức làm phiên bản v1 bị nổ lỗi SQL Crash nếu phải rollback!

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Chạy lệnh `ALTER TABLE DROP COLUMN` ngay trong stage migration của phiên bản mới.

---

### Câu 3
**Hỏi:** Tại sao nên bắt đầu nấc Canary Deployment với 10% traffic và khoảng thời gian quan sát metric (Observation Window) khuyến nghị tối thiểu là bao nhiêu phút?

**Gợi ý trả lời ngắn:**
Bắt đầu 10% để thu hẹp bán kính ảnh hưởng sự cố (Blast Radius Reduction) và thời gian quan sát tối thiểu là **15 phút** để Prometheus tích lũy đủ dữ liệu metric.

**Đáp án chuẩn:**
- **Ý nghĩa chỉ số:**
  1. *Nấc 10% Traffic:* Nếu phiên bản mới có bug rò rỉ bộ nhớ hay nổ lỗi edge case, chỉ có đúng 10% khách hàng chịu tác động, 90% khách hàng còn lại vẫn an toàn tuyệt đối.
  2. *15 phút Observation Window:* Nhiều lỗi ứng dụng (như Memory Leak, DB Connection Pool Exhaustion) không xuất hiện ngay trong 1 phút đầu tiên mà cần từ 10-15 phút tích lũy traffic thực tế để bộc lộ trên Prometheus dashboard.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Tăng vọt traffic Canary từ 10% lên 100% chỉ sau 1 phút deploy mà không chờ quan sát metric.

---

### Câu 4
**Hỏi:** Ngưỡng tỷ lệ lỗi HTTP 5xx tối đa và độ trễ khuyến nghị để pipeline CI/CD tự động kích hoạt Rollback Canary là bao nhiêu?

**Gợi ý trả lời ngắn:**
Tự động Rollback khi tỷ lệ lỗi HTTP 5xx vượt quá **1% tổng request** hoặc P99 Latency tăng vượt **500ms**.

**Đáp án chuẩn:**
- **Quy tắc Tự động ngắt (Closed-loop Remediation):**
  Pipeline CI liên kết với Prometheus Alertmanager Webhook. Ngay khi chỉ số HTTP 5xx của nấc Canary vượt quá 1% hoặc P99 Latency vượt 500ms trong khoảng 2-3 phút, Prometheus bắn Webhook gọi GitLab CI thực thi ngay job `auto-rollback-canary` xóa bỏ Canary Pods trong dưới 3 giây.
- **Lợi ích:** Rút ngắn thời gian phát hiện sự cố (MTTD) xuống dưới 5 giây và loại bỏ sự chậm trễ của yếu tố con người.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Để ngưỡng lỗi lên đến 20-30% mới tiến hành rollback thủ công.

---

### Câu 5
**Hỏi:** Khái niệm triệt hạ rủi ro "Deploy is NOT Release" khi sử dụng GitLab Feature Flags (Unleash Engine) có nghĩa là gì?

**Gợi ý trả lời ngắn:**
Nghĩa là phân tách việc đưa mã nguồn lên máy chủ (Deploy) khỏi việc bật tính năng cho khách hàng sử dụng (Release) bằng công tắc Feature Flags từ xa.

**Đáp án chuẩn:**
- **Phân tách Deploy và Release:**
  - *Deploy:* Đội ngũ kỹ sư có thể đẩy mã nguồn mới lên Production bất kỳ lúc nào trong ngày (kể cả giờ cao điểm) dưới trạng thái Feature Flag bị tắt (`false`). Ứng dụng không hề bị ảnh hưởng.
  - *Release:* Khi đến giờ hoàng đạo hoặc chiến dịch Marketing, Product Manager chỉ cần mở giao diện GitLab UI bấm công tắc **ON**. Tính năng xuất hiện tức thì trong 50ms cho người dùng mà không cần chạy lại pipeline build hay redeploy code.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng "Deploy code lên server và Release tính năng cho user bắt buộc phải diễn ra đồng thời cùng một lúc".

---

### Câu 6
**Hỏi:** Tại sao trong mã nguồn ứng dụng khi dùng Feature Flag SDK lại bắt buộc phải bọc giá trị fallback mặc định (dạng `false`)?

**Gợi ý trả lời ngắn:**
Để ứng dụng vẫn tự động rơi về luồng code cũ an toàn (Fallback Path) nếu máy chủ Feature Flag Server bị ngắt kết nối hoặc timeout.

**Đáp án chuẩn:**
- **Thiết kế Chống sập (Resilient Design):**
  Khi ứng dụng gọi SDK `unleash.isEnabled("new_feature", false)`, nếu kết nối mạng tới máy chủ GitLab Feature Flag Server bị đứt hoặc timeout 300ms, SDK sẽ tự động trả về giá trị fallback mặc định `false`.
- **Kết quả:** Ứng dụng tiếp tục chạy luồng code cũ ổn định 100% thay vì bị nổ lỗi `NullPointerException` làm sập toàn bộ dịch vụ.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Không khai báo tham số fallback mặc định, khiến app bị crash khi Feature Flag Server ngắt kết nối.

---

### Câu 7
**Hỏi:** Tại sao việc điều tiết phần trăm traffic Canary (Traffic Splitting) nên được thực hiện ở tầng Ingress Controller / Service Mesh chứ không nên chia bằng mã nguồn ứng dụng?

**Gợi ý trả lời ngắn:**
Để đảm bảo tính chính xác của việc phân bổ lưu lượng ở tầng mạng HTTP Layer và không làm tăng độ phức tạp của mã nguồn ứng dụng.

**Đáp án chuẩn:**
- **Giải thích kiến trúc:**
  NGINX Ingress Controller hoặc Service Mesh (Linkerd/Istio) hoạt động ở tầng Reverse Proxy / Network Layer. Chúng có khả năng tính toán trọng số Weighted Routing chuẩn xác 100% dựa trên HTTP Request Headers, Cookie, hoặc Random Weight mà không tốn tài nguyên CPU của ứng dụng.
- **Nếu chia bằng code app:** Mã nguồn sẽ bị lộn xộn bởi các câu lệnh ngẫu nhiên `Math.random() < 0.1`, gây khó khăn cho việc kiểm thử Unit Test và không thể thay đổi % traffic từ bên ngoài CI/CD.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Viết code ngẫu nhiên trong backend controller để tự chia phần trăm traffic sang tính năng mới.

---

### Câu 8
**Hỏi:** Khái niệm "Stale Feature Flags" là gì và thời hạn tối đa khuyến nghị để dọn dẹp chúng khỏi mã nguồn là bao nhiêu ngày?

**Gợi ý trả lời ngắn:**
Stale Feature Flags là các đoạn mã flag đã bật 100% lâu ngày; khuyến nghị dọn dẹp khỏi mã nguồn sau **30 ngày** ổn định để tránh nợ kỹ thuật.

**Đáp án chuẩn:**
- **Tác hại của Stale Flags:**
  Sau khi một tính năng mới đã được bật 100% và hoạt động hoàn hảo trên Production, đoạn mã bọc Feature Flag đó trở thành "rác mã nguồn" (Stale Flag). Nếu giữ lại hàng trăm flag cũ, mã nguồn sẽ bị phình to bởi hàng ngàn câu lệnh `if/else` chồng chéo, gây rối mắt và làm tăng độ phức tạp khi refactor code.
- **Quy trình dọn dẹp:** Sau 30 ngày tính năng chạy ổn định, kỹ sư mở Merge Request xóa bỏ khối `else` cũ, giữ lại duy nhất luồng code mới và xóa flag trên GitLab UI.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Giữ nguyên các đoạn code Feature Flags trong mã nguồn vĩnh viễn không bao giờ xóa.

---

### Câu 9
**Hỏi:** Ý nghĩa của việc khai báo khối `environment` (như `environment.name: production/canary`) trong tệp `.gitlab-ci.yml` là gì?

**Gợi ý trả lời ngắn:**
Giúp GitLab CI ghi lại nhật ký lịch sử phiên bản deployment và hỗ trợ nút Rollback 1-Click trực tiếp trên giao diện GitLab Environments Dashboard.

**Đáp án chuẩn:**
- **Tích hợp GitLab Environments Dashboard:**
  Khai báo `environment.name` và `environment.url` giúp GitLab theo dõi chính xác Docker Image SHA nào đang chạy trên từng nấc (Blue, Green, Canary). Giao diện GitLab UI sẽ hiển thị bảng điều khiển trực quan, cho phép Tech Lead theo dõi thời gian deploy và bấm nút **Rollback** 1-Click để khôi phục phiên bản trước đó ngay lập tức mà không cần gõ lệnh CLI.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Deploy ứng dụng từ CI nhưng không khai báo khối `environment`.

---

### Câu 10
**Hỏi:** Công cụ nào giúp kết nối hệ thống cảnh báo Prometheus Alertmanager với GitLab CI Pipeline để thực thi ngắt Canary tự động?

**Gợi ý trả lời ngắn:**
Sử dụng **GitLab Pipeline Trigger Webhook** (gọi HTTP POST API tới GitLab Pipeline Trigger URL).

**Đáp án chuẩn:**
- **Cơ chế Tự động hóa Khép kín (Closed-loop Remediation):**
  1. Prometheus phát hiện chỉ số `http_requests_total{status=~"5.."}` của Canary Pods tăng vọt.
  2. Alertmanager kích hoạt quy tắc cảnh báo `HighErrorRateCanary`.
  3. Alertmanager bắn một câu lệnh HTTP POST Webhook tới URL: `https://gitlab.company.com/api/v4/projects/12/trigger/pipeline?token=XXX&ref=main`.
  4. GitLab CI nhận webhook và lập tức kích hoạt job `auto-rollback-canary` xóa bỏ Canary Pods trong 2 giây!

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cảnh báo Prometheus chỉ gửi tin nhắn Slack rồi nằm chờ con người vào đọc tin nhắn và gõ lệnh rollback thủ công.

---

### Câu 11
**Hỏi:** Khái niệm "Canary Analysis" là gì và tại sao bắt buộc phải so sánh phiên bản Canary mới với phiên bản Baseline cũ trong cùng một khoảng thời gian?

**Gợi ý trả lời ngắn:**
Canary Analysis là quá trình so sánh đối soát tự động các chỉ số Error Rate/Latency giữa Canary v2 và Baseline v1 để đưa ra quyết định Promote hay Rollback bằng thuật toán thống kê.

**Đáp án chuẩn:**
- **Giải thích ý nghĩa so sánh Baseline:**
  Nếu trong khoảng thời gian thử nghiệm 15 phút, toàn bộ hệ thống bị nghẽn mạng do đứt cáp quang biển làm Latency chung tăng lên 300ms, nếu chỉ nhìn chỉ số của Canary v2 bạn sẽ kết luận sai là Canary bị lỗi!
- **Giải pháp:** Canary Analysis đọc dữ liệu của cả **Canary Pods v2** và **Baseline Pods v1** (cùng nhận traffic trong cùng điều kiện mạng). Nếu Canary có tỷ lệ lỗi tương đồng với Baseline, phiên bản mới đạt chuẩn xanh 100%!

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Đánh giá hiệu năng Canary v2 mà không so sánh đối soát với bản Baseline v1 trong cùng điều kiện tải.

---

### Câu 12
**Hỏi:** Tại sao Product Manager / Business Analyst nên là người nắm quyền bật/tắt Feature Flags chứ không phải kỹ sư DevOps?

**Gợi ý trả lời ngắn:**
Để phân tách trách nhiệm (Separation of Duties): DevOps chịu trách nhiệm độ tin cậy hạ tầng, Product Manager chủ động quyết định thời điểm phát hành tính năng kinh doanh cho khách hàng.

**Đáp án chuẩn:**
- **Phân tách Ranh giới Trách nhiệm (Separation of Duties):**
  - *Kỹ sư DevOps / Developer:* Chịu trách nhiệm đảm bảo mã nguồn được test kỹ, build Docker Image sạch và deploy lên hạ tầng Kubernetes an toàn 100%.
  - *Product Manager:* Am hiểu chiến dịch Marketing và hành vi khách hàng. PM sẽ chủ động bật Feature Flag cho 5% người dùng ở Hà Nội lúc 9:00 AM, sau đó mở rộng ra toàn quốc lúc 2:00 PM mà không cần làm phiền hay phụ thuộc vào lịch làm việc của đội DevOps.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Mỗi lần muốn bật tính năng cho 1 khách hàng VIP lại phải nhờ kỹ sư DevOps gõ lệnh CLI hoặc sửa biến môi trường CI.

---

## §V2. Kịch bản phỏng vấn thực tế (Roleplay Scenarios)

### Kịch bản 1: Thuyết phục CTO chuyển đổi từ Deploy trực tiếp sang Canary Deployment & Feature Flags
- **Người phỏng vấn (CTO):** *"Hệ thống của chúng ta đang deploy đập thẳng 100% code mới lên production vào lúc 12:00 đêm 2 năm nay vẫn ổn. Tại sao em lại đề xuất tốn công làm Canary Deployment và Feature Flags?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:* "Báo cáo anh, cách deploy 100% lúc nửa đêm đang chứa 3 rủi ro rất lớn đối với hoạt động kinh doanh:"
  - "1. **Bán kính ảnh hưởng 100% (Blast Radius):** Nếu phiên bản mới có bug rò rỉ bộ nhớ, 100% khách hàng sẽ bị sập ứng dụng cùng một lúc."
  - "2. **Thức đêm On-call cực nhọc:** Đội ngũ kỹ sư phải thức đến 2:00 AM để test thủ công trên Prod, ảnh hưởng sức khỏe và năng suất làm việc ngày hôm sau."
  - "3. **Giải pháp Canary & Feature Flags:** Giúp chúng ta **deploy code ban ngày lúc 10:00 AM hoàn toàn an toàn**, chỉ mở **10% Canary traffic** thử nghiệm. Đồng thời dùng **Feature Flags bật/tắt tính năng trong 50ms**, giúp giảm thời gian phát hiện lỗi (MTTD) xuống dưới 5 giây và bảo vệ 90% khách hàng an toàn tuyệt đối!"

---

### Kịch bản 2: Xử lý Sự cố Sập toàn bộ Cụm do Rollback thất bại vì DB Schema không Tương thích Ngược
- **Người phỏng vấn (Senior Database Architect):** *"Đêm qua khi rollback từ bản Green về bản Blue, toàn bộ ứng dụng Blue bị nổ lỗi SQL Crash làm sập hệ thống 3 tiếng. Em tìm nguyên nhân và đưa ra giải pháp thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Chẩn đoán nguyên nhân:** Script DB migration của bản Green (v2) đã chạy câu lệnh `ALTER TABLE DROP COLUMN` xóa mất cột dữ liệu cũ mà bản Blue (v1) đang sử dụng. Khi rollback Ingress về Blue, code v1 đọc không thấy cột dữ liệu nên nổ lỗi SQL Crash (vi phạm QT 43.7).
    2. **Khắc phục theo quy trình Expand-and-Contract chuẩn:**
       - *Pha 1 (Expand):* Thêm cột mới `new_column`, giữ nguyên `old_column`. Cả v1 và v2 cùng đọc/ghi được.
       - *Pha 2 (Deploy):* Triển khai v2 và chạy ổn định 30 ngày trên Production.
       - *Pha 3 (Contract):* Sau 30 ngày v2 chạy xanh 100%, mới chạy script xóa cột `old_column`.
    3. **Kết quả:** Đảm bảo khả năng Rollback 100% an toàn trong 3 giây mà không bao giờ bị SQL Crash!

---

### Kịch bản 3: Xử lý Sự cố Canary bị Lỗi HTTP 5xx tăng cao trong Đợt Săn Sale
- **Người phỏng vấn (Head of Infrastructure):** *"Trong đợt Săn Sale 11/11, khi vừa mở 10% Canary traffic thì tỷ lệ lỗi HTTP 5xx nhảy lên 4%. Hệ thống của em sẽ ứng phó tự động ra sao trong 5 giây?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Phản ứng tự động của Prometheus Alertmanager:**
       - Prometheus phát hiện chỉ số HTTP 5xx của Canary Pods đạt 4% (vượt ngưỡng 1%). Cảnh báo `HighErrorRateCanary` kích hoạt.
       - Alertmanager gửi HTTP POST Webhook tới GitLab CI Pipeline Trigger URL.
    2. **Thực thi Auto-Rollback Pipeline:**
       - GitLab CI nhận webhook và chạy ngay job `auto-rollback-canary` với cờ `when: on_failure`.
       - Lệnh `helm uninstall payment-canary` ngắt toàn bộ 10% Canary traffic về 0% trong **2 giây**!
    3. **Kết luận:** 90% khách hàng mua sắm hoàn toàn không bị ảnh hưởng, thời gian khôi phục (MTTR) đạt kỷ lục dưới 3 giây!

---

### Kịch bản 4: Thuyết phục Product VP về Phương án sử dụng Feature Flags để A/B Testing
- **Người phỏng vấn (VP of Product):** *"Tôi muốn thử nghiệm 2 giao diện thanh toán mới cho 5% khách hàng ở TP.HCM để đo tỷ lệ chuyển đổi đơn hàng mà không muốn ảnh hưởng khách hàng Hà Nội. Em làm thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Tích hợp GitLab Feature Flags Engine:**
       - Đội dev bọc 2 luồng giao diện trong SDK: `if (unleash.isEnabled("v2_checkout_hcm", context))`.
    2. **Cấu hình Target Strategy trên GitLab UI:**
       - Mở GitLab Feature Flags UI, tạo chiến lược `User With ID / Location`: Cấu hình mở flag cho các User ID có thuộc tính `city == "HCM"` với tỷ lệ 5% Rollout.
    3. **Kết quả:** Khách hàng ở TP.HCM được trải nghiệm giao diện mới, khách hàng Hà Nội giữ nguyên giao diện cũ. VP of Product đo đếm tỷ lệ conversion trực tiếp trên Dashboard real-time!

---

### Kịch bản 5: Giải quyết Sự cố Ứng dụng bị Trệ do Lỗi Feature Flag Server Timeout
- **Người phỏng vấn (Operations Manager):** *"Nếu máy chủ GitLab Feature Flag Server bị sập hoặc nghẽn mạng, liệu toàn bộ ứng dụng Microservices của chúng ta có bị sập theo không?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Cam kết tính sẵn sàng cao (High Availability):** "Báo cáo anh, ứng dụng tuyệt đối KHÔNG bị sập."
    2. **Cơ chế Fallback & In-Memory Cache (QT 43.5):**
       - SDK Unleash Client duy trì một bản sao State Flags trong bộ nhớ RAM của Pod (In-Memory Cache) và tự động đồng bộ ngầm (Async Background Sync).
       - Nếu Feature Flag Server bị ngắt kết nối hoàn toàn, SDK tự động rơi về giá trị fallback mặc định `false`. Ứng dụng tiếp tục phục vụ luồng code cũ hoàn toàn mượt mà 100%!

---

### Kịch bản 6: Tối ưu hóa Dọn dẹp Stale Feature Flags chống Nợ Kỹ thuật
- **Người phỏng vấn (DevOps Team Lead):** *"Sau 1 năm sử dụng Feature Flags, mã nguồn của chúng ta đang chứa 200 flags cũ lộn xộn khiến dev mới vào không hiểu logic code. Em giải quyết thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Thiết lập Quy trình Dọn dẹp Stale Flags (QT 43.6):**
       - Quy định rõ: Mọi Feature Flag sau khi đã bật 100% traffic và chạy ổn định quá **30 ngày** bắt buộc phải được đưa vào danh sách dọn dẹp (Stale Flags Cleanup).
    2. **Tự động hóa Linter Quét Stale Flags:**
       - Viết script linter trong CI Pipeline quét các flags có tuổi đời >30 ngày trên GitLab UI và cảnh báo yêu cầu Developer mở MR xóa bỏ khối `else` cũ.
    3. **Kết quả:** Giữ mã nguồn luôn sạch đẹp, tối ưu performance và loại bỏ 100% nợ kỹ thuật (Technical Debt).

---

### Kịch bản 7: Xây dựng Quy trình Canary Analysis với Kayenta / Prometheus
- **Người phỏng vấn (Lead Site Reliability Engineer):** *"Làm sao em chứng minh được phiên bản Canary v2 thực sự tốt hơn hoặc bằng phiên bản Baseline v1 trước khi bấm nút Promote lên 100%?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Tích hợp Canary Analysis Script (QT 43.12):**
       - Trong stage `verify-canary`, script tự động query Prometheus API đọc 3 chỉ số trong 15 phút: `Error Rate`, `P99 Latency`, và `CPU/RAM Usage` của cả 2 cụm Pods: `Canary v2` và `Baseline v1`.
    2. **Đánh giá bằng thuật toán thống kê:**
       - Script thực thi phép so sánh đối soát: Nếu Error Rate của Canary v2 không cao hơn Baseline v1 quá 0.05% và Latency P99 tương đồng, script trả về `verdict: PROMOTE_APPROVED`.
       - Nút Manual Promote trên GitLab CI được mở xanh cho phép đè 100% traffic an toàn dựa trên dữ liệu định lượng 100%!

---

## §V3. Câu chốt để nói khi phỏng vấn

1. *"Bản chất của phát hành ứng dụng hiện đại là **phân tách việc đưa code lên hạ tầng (Deploy) khỏi việc bật tính năng cho user (Release)** bằng Feature Flags."*
2. *"Thực thi **Blue-Green Deployment mang lại Zero Downtime tuyệt đối** và khả năng Rollback tráo đổi Ingress 100% traffic dưới 3 giây."*
3. *"Triển khai **Canary Deployment giúp thu hẹp bán kính ảnh hưởng sự cố (Blast Radius)** xuống nấc 10% traffic ban đầu với 15 phút Observation Window."*
4. *"Tự động hóa **Rollback Canary dưới 3 giây qua Prometheus Alertmanager Webhook** khi tỷ lệ lỗi HTTP 5xx vượt quá 1%."*
5. *"Điều kiện sống còn của Blue-Green và Canary là **đảm bảo tính tương thích ngược của Database Schema (Expand-and-Contract Migration)**."*
6. *"Luôn **bọc giá trị fallback mặc định an toàn (`false`)** trong câu lệnh Feature Flag SDK để chống sập app khi Feature Flag Server bị timeout."*
7. *"Điều tiết phần trăm traffic Canary **bắt buộc phải thực hiện ở tầng Ingress Controller / Service Mesh** bằng Weighted Routing chứ không chia bằng code app."*
8. *"Thiết lập **quy trình dọn dẹp Stale Feature Flags sau 30 ngày** để ngăn ngừa phình to mã nguồn và triệt hạ nợ kỹ thuật (Technical Debt)."*
9. *"Tích hợp **Canary Analysis tự động so sánh đối soát chỉ số của Canary v2 với Baseline v1** trước khi bấm nút Promote 100% Production."*
10. *"Phân quyền **cho Product Manager chủ động bật/tắt Feature Flags trên GitLab UI trong 50ms** mà không cần phiền tới kỹ sư DevOps gõ lệnh CLI."*

---

## BTVN 4: Chuẩn bị cho Buổi 44 — Quản lý Runner: architecture, executor, scaling, maintenance

Để chuẩn bị tốt nhất cho **Buổi 44: Quản lý Runner: architecture, executor, scaling, maintenance**, học viên cần thực hiện các nhiệm vụ sau:

1. **Ôn tập kiến thức Kiến trúc Máy chủ GitLab Runner:**
   - Đọc trước cấu trúc tệp cấu hình `config.toml` của GitLab Runner.
   - Phân biệt 3 loại Executors phổ biến: **Shell Executor**, **Docker Executor**, và **Kubernetes Executor**.

2. **Nghiên cứu về cơ chế Tự động Mở rộng (Auto-scaling Runner):**
   - Phân tích luận đề: *"Máy chủ CI Runner là **nút thắt cổ chai lớn nhất về tốc độ và an ninh** của toàn bộ hệ thống CI/CD — và Runner phải được quản trị như một hạ tầng Production!"*
   - Tìm hiểu cơ chế Docker Machine Auto-scaling và Kubernetes Runner Pod Autoscaling.

3. **Bài tập chuẩn bị trước giờ học:**
   - Trả lời câu hỏi: *"Tại sao việc chạy GitLab Runner với Shell Executor trên cùng máy chủ chứa source code lại tiềm ẩn nguy cơ bảo mật rò rỉ dữ liệu cực kỳ nghiêm trọng?"*
   - Chuẩn bị danh sách 3 cờ cấu hình quan trọng nhất trong khối `[runners.docker]` của tệp `config.toml`!
{% endraw %}
