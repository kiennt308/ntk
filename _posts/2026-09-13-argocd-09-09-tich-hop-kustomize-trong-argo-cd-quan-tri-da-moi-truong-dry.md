---
layout: post
title: "[Bài 09] Tích Hợp Kustomize Trong Argo CD: Quản Trị Đa Môi Trường DRY Chuẩn Enterprise"
date: 2026-09-13 00:20:00 +0700
categories: [ArgoCD]
tags:
  - ArgoCD
  - GitOps
  - Kubernetes
  - CICD
  - CloudNative
  - Part-09
series: "ArgoCD & GitOps Mastery"
series_order: 9
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80"
summary: "Hướng dẫn tích hợp Kustomize trong Argo CD: Quản trị đa môi trường Dev/Staging/Prod theo triết lý DRY (Don't Repeat Yourself) với Base & Overlays Pattern, Kustomize Components, khai thác sức mạnh của ConfigMapGenerator Content Hash kích hoạt Zero-Downtime Rolling Updates và xử lý bẫy Pod không reload cấu hình."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Tích Hợp Kustomize Trong Argo CD: Quản Trị Đa Môi Trường DRY Chuẩn Enterprise."
  - "Ứng dụng triết lý GitOps với Git làm nguồn chân lý duy nhất (Single Source of Truth), đồng bộ tự động 24/7."
  - "Kiểm soát chặt chẽ quy trình triển khai đa cụm Kubernetes, phát hiện và triệt tiêu Configuration Drift."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# Tích Hợp Kustomize Trong Argo CD: Quản Trị Đa Môi Trường DRY Chuẩn Enterprise

Trong thực tế phát triển phần mềm, một ứng dụng microservice không bao giờ chỉ chạy trên một môi trường duy nhất. Hệ thống bắt buộc phải đi qua chuỗi các môi trường: **Dev** (cho lập trình viên thử nghiệm), **Staging / UAT** (cho QA kiểm thử tải) và **Production** (phục vụ khách hàng thực tế).

Vấn đề đặt ra là: Làm thế nào để quản lý cấu hình cho hàng chục microservices chạy trên nhiều môi trường và cụm đám mây khác nhau mà không phải sao chép (Copy-Paste) tệp `deployment.yaml` thành hàng chục bản khác nhau? Nếu copy-paste, khi cần sửa một biến môi trường hoặc cập nhật security context chung, bạn sẽ phải sửa ở hàng chục nơi — tạo ra nguy cơ sai sót con người cực kỳ lớn!

**Kustomize** ra đời như một giải pháp cứu tinh với triết lý quản trị không dùng mẫu (**Template-Free Declarative Management**), cho phép tái sử dụng tối đa cấu hình gốc thông qua mô hình **Base & Overlays Pattern (DRY - Don't Repeat Yourself)**.

Bài viết này sẽ hướng dẫn bạn tích hợp Kustomize vào Argo CD, làm chủ các kỹ thuật vá cấu hình (Strategic Merge vs JSON 6902 Patch), khai thác tính năng tự động kích hoạt Rolling Update bằng **ConfigMapGenerator Content Hash**, kiến trúc Kustomize Components và vạch trần cạm bẫy *"ConfigMap đã Synced nhưng Pod vẫn chạy cấu hình cũ"*.

---

## 1. Kiến Trúc Base & Overlays Pattern (DRY Triệt Để)

Kustomize chia cấu hình thành 2 tầng phân tách trách nhiệm rõ rệt:
1. **Base (Tầng Nền Tảng):** Chứa 80-90% các khai báo chuẩn mực dùng chung cho mọi môi trường (cấu trúc Pod, Port, Liveness/Readiness Probes, Service, NetworkPolicy).
2. **Overlays (Tầng Chuyên Biệt):** Chỉ chứa các bản vá (Patches) đè lên Base để tinh chỉnh riêng cho từng môi trường (CPU/RAM, số Replicas, Ingress Hostname, Secrets, biến môi trường).

```mermaid
flowchart TD
    subgraph BASE["TẦNG GỐC: BASE (DÙNG CHUNG 100%)"]
        B_DEPLOY["deployment.yaml<br/>(Cấu trúc Pod, Port 8080, Probes)"]
        B_SVC["service.yaml<br/>(ClusterIP Service)"]
        B_KUST["kustomization.yaml<br/>(resources: [deployment, service])"]
    end

    subgraph OVERLAYS["TẦNG CHUYÊN BIỆT: OVERLAYS (PATCHES)"]
        subgraph DEV["Overlay: Dev"]
            DEV_KUST["kustomization.yaml<br/>- replicas: 1<br/>- CPU: 100m, RAM: 128Mi<br/>- env: dev"]
        end
        
        subgraph STAGING["Overlay: Staging"]
            STG_KUST["kustomization.yaml<br/>- replicas: 2<br/>- CPU: 250m, RAM: 256Mi<br/>- env: staging"]
        end

        subgraph PROD["Overlay: Production"]
            PRD_KUST["kustomization.yaml<br/>- replicas: 5<br/>- CPU: 1000m, RAM: 1Gi<br/>- Ingress: api.company.com"]
        end
    end

    BASE -->|"Tái sử dụng gốc"| DEV
    BASE -->|"Tái sử dụng gốc"| STAGING
    BASE -->|"Tái sử dụng gốc"| PROD

    PROD ==>|"Argo CD biên dịch kustomize build"| PROD_RENDERED["Manifest Hoàn Chỉnh Triển Khai Lên Production"]


```

---

## 2. Kiến Trúc Đa Tầng Phân Cấp (Multi-Tier Hierarchy) & Kustomize Components

Trong các hệ thống Enterprise triển khai trên nhiều khu vực (Multi-Region) và nhiều nhà cung cấp đám mây (Multi-Cloud), mô hình 2 tầng đơn giản không đủ đáp ứng. Ta sử dụng mô hình **Đa Tầng Phân Cấp (Multi-Tier Overlays)** kết hợp **Kustomize Components**:

```mermaid
flowchart TD
    BASE["1. Base (Core App Manifests)"]
    
    subgraph CLOUD["2. Cloud Provider Layer (Overlays)"]
        AWS["aws-overlay<br/>(IRSA Annotations, ALB Ingress)"]
        GCP["gcp-overlay<br/>(Workload Identity, GKE Ingress)"]
    end
    
    subgraph COMP["Kustomize Components (Plug-and-Play Modules)"]
        C_TRACE["components/opentelemetry-tracing"]
        C_AUTH["components/oauth2-proxy-sidecar"]
        C_HPA["components/horizontal-autoscaler"]
    end

    subgraph REGION["3. Regional Production Overlays"]
        US_PROD["overlays/prod-us-east-1<br/>- Replicas: 10<br/>- Ingress: us-api.domain.com"]
        EU_PROD["overlays/prod-eu-west-1<br/>- Replicas: 8<br/>- Ingress: eu-api.domain.com"]
    end

    BASE --> AWS
    BASE --> GCP
    AWS --> US_PROD
    GCP --> EU_PROD
    C_TRACE -.->|"components: [...]"| US_PROD
    C_HPA -.->|"components: [...]"| US_PROD
    C_AUTH -.->|"components: [...]"| EU_PROD


```

- **Kustomize Components (`components:`):** Cho phép đóng gói các tính năng có thể tái sử dụng (như thêm sidecar log, cấu hình distributed tracing, hoặc cấu hình WAF rules) thành từng module độc lập và chỉ "cắm" (plug-in) vào môi trường nào thực sự cần thiết.

---

## 3. Phân Tích Cấu Trúc Thư Mục & Manifest Kustomize Chuẩn

Dưới đây là cấu trúc cây thư mục chuẩn mực trong kho GitOps quản trị microservice:

```bash
services/payment-service/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
├── components/
│   └── tracing/
│       ├── kustomization.yaml
│       └── otel-agent-patch.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── dev-patches.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   └── staging-patches.yaml
    └── production/
        ├── kustomization.yaml
        ├── replica-patch.yaml
        └── config.env
```

### 3.1. Cấu Hình Tệp `base/kustomization.yaml`

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml

commonLabels:
  app.kubernetes.io/name: payment-api
  app.kubernetes.io/part-of: ecommerce
```

### 3.2. Cấu Hình Tệp `overlays/production/kustomization.yaml` (Line-by-Line Breakdown)

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# 1. Kế thừa toàn bộ tài nguyên từ thư mục base
resources:
  - ../../base

# 2. Nhúng thêm module Kustomize Component (Tracing OpenTelemetry)
components:
  - ../../components/tracing

# 3. Tự động thêm tiền tố cho toàn bộ tài nguyên (ví dụ: prod-payment-api)
namePrefix: prod-

# 4. Tự động thêm Namespace cho toàn bộ tài nguyên
namespace: payment-production

# 5. Gắn thêm nhãn định danh môi trường
commonLabels:
  environment: production
  tier: backend

# 6. Tự động cập nhật Image Tag mà không cần sửa file deployment.yaml
images:
  - name: company-registry.io/payment-api
    newTag: "v2.5.0"

# 7. Tự động băm nội dung ConfigMap kích hoạt Zero-Downtime Rolling Update
configMapGenerator:
  - name: payment-config
    envs:
      - config.env
    options:
      disableNameSuffixHash: false

# 8. Áp dụng các bản vá (Patches) đè lên cấu hình Base
patches:
  - target:
      kind: Deployment
      name: payment-api
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
      - op: add
        path: /spec/template/spec/containers/0/resources
        value:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 2000m
            memory: 2Gi
```

### 3.3. So Sánh Các Kỹ Thuật Patch Trong Kustomize

| Kỹ Thuật Patch | Cú Pháp Khai Báo | Trường Hợp Sử Dụng | Ưu Điểm | Nhược Điểm |
| :--- | :--- | :--- | :--- | :--- |
| **Strategic Merge Patch** | File YAML con chứa cấu trúc merge | Thêm biến môi trường, sửa label, đổi image | Dễ đọc, cú pháp tương tự Kubernetes manifest thông thường | Không thể xóa phần tử khỏi mảng một cách tường minh |
| **JSON Patch (RFC 6902)** | Mảng các operations: `add`, `remove`, `replace` | Xóa một container, sửa chính xác vị trí index trong mảng | Linh hoạt tuyệt đối, hỗ trợ xóa và thay thế chính xác | Khó đọc hơn, dễ sai nếu index mảng bị lệch |
| **Inline Patches (Kustomize v5)** | Khối `patches: [{target, patch}]` | Gộp chung cấu hình vá vào ngay trong `kustomization.yaml` | Gọn gàng, không cần tạo thêm nhiều file patch rác | File `kustomization.yaml` có thể bị dài nếu vá quá nhiều |

---

## 4. Sức Mạnh Của `configMapGenerator` & Tự Động Kích Hoạt Rolling Update

Một vấn đề "nhức nhối" trong Kubernetes là: **Khi bạn sửa nội dung một ConfigMap hoặc Secret, các Pods đang chạy sẽ KHÔNG tự động khởi động lại để nạp cấu hình mới**. Nếu kỹ sư không biết, ứng dụng sẽ tiếp tục chạy với cấu hình cũ lỗi thời dù manifest đã được đồng bộ.

### 4.1. Cơ Chế Băm Nội Dung (Content Hash Suffix) Của Kustomize

Khi sử dụng `configMapGenerator`, Kustomize tự động tính toán mã băm SHA256 của nội dung tệp `config.env` và gắn vào đuôi của tên ConfigMap:

```bash
Lần 1: payment-config-7b8f9g4k2m  (Nội dung: DB_TIMEOUT=30)
Lần 2: Sửa DB_TIMEOUT=60
  -> Kustomize tự sinh tên mới: payment-config-9h3k8d1w5p
  -> Deployment tự động đổi tham số trỏ sang ConfigMap mới
  -> Kubernetes PHÁT HIỆN THAY ĐỔI TRÊN POD TEMPLATE VÀ KÍCH HOẠT ROLLING UPDATE TỨC THÌ!
```

```mermaid
flowchart LR
    ENV_EDIT["1. Sửa DB_TIMEOUT=60 trong config.env"] --> KUST_BUILD["2. Kustomize tính toán Hash SHA256"]
    KUST_BUILD --> CM_NEW["3. Sinh ConfigMap mới: config-9h3k8d1w5p"]
    CM_NEW --> DEPLOY_PATCH["4. Deployment cập nhật name: config-9h3k8d1w5p"]
    DEPLOY_PATCH ==> K8S_ROLLING["5. Kubernetes tự động Rolling Update Pods mới 100%!"]


```

> [!IMPORTANT]
> **TỰ ĐỘNG ROLLING UPDATE VỚI CONFIGMAP:**
> Sửa ConfigMap tĩnh không làm Pod restart. Luôn sử dụng `configMapGenerator` của Kustomize để tự động băm mã Hash vào tên ConfigMap, ép Kubernetes kích hoạt Zero-Downtime Rolling Update.

---

## 5. Tùy Biến Cờ Kustomize Build Trong Argo CD (`argocd-cm`)

Mặc định, Kustomize chạy bên trong `argocd-repo-server` với các thiết lập bảo mật nghiêm ngặt. Khi cần kích hoạt các tính năng nâng cao như nhúng Helm Chart trong Kustomize hoặc nạp file ngoài thư mục gốc (`--load-restrictor LoadRestrictionsNone`), bạn có thể cấu hình thông qua ConfigMap `argocd-cm`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  # Cấu hình tùy chọn tham số build cho Kustomize engine
  kustomize.buildOptions: "--enable-helm --load-restrictor LoadRestrictionsNone"
```

---

## 6. Khai Báo Kustomize Trong Argo CD Application CRD

Argo CD tự động nhận diện Kustomize khi trong thư mục `spec.source.path` có chứa tệp `kustomization.yaml`:

```yaml
# application-kustomize-prod.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-prod-kustomize
  namespace: argocd
spec:
  project: default
  source:
    repoURL: "https://github.com/company/ecommerce-gitops.git"
    targetRevision: "main"
    path: "services/payment-service/overlays/production"
    
    # Có thể override tham số trực tiếp từ Argo CD Application
    kustomize:
      namePrefix: "prod-"
      images:
        - "company-registry.io/payment-api:v2.5.0"
      commonLabels:
        managed-by: "argocd"
  destination:
    server: "https://kubernetes.default.svc"
    namespace: "payment-production"
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
```

---

## 7. Cạm Bẫy Thực Chiến: "ConfigMap Đã Synced Nhưng Pods Vẫn Chạy Cấu Hình Cũ Do Không Dùng Hash Generator"

### Hiện Tượng Sự Cố & Log Trace
- Kỹ sư DevOps sửa một biến môi trường quan trọng `FEATURE_FLAG_PAYMENT=true` trong một ConfigMap tĩnh `configmap.yaml` trên Git.
- Argo CD phát hiện commit mới, thực hiện Sync thành công và báo **`Sync Status: Synced`** màu xanh lá.
- Tuy nhiên, người dùng trên Production vẫn không sử dụng được tính năng mới. Khách hàng phàn nàn và hệ thống vẫn xử lý theo logic cũ!

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Kỹ sư DevOps
    participant Git as Git Repo (ConfigMap tĩnh)
    participant Argo as Argo CD Controller
    participant K8s as Kubernetes API Server
    participant Pod as Live Pods

    Dev->>Git: Sửa FEATURE_FLAG_PAYMENT=true trong configmap.yaml
    Argo->>K8s: Apply ConfigMap mới đè lên ConfigMap cũ
    Note over K8s: ConfigMap trên cụm đã đổi giá trị mới!
    Argo-->>Dev: Báo App SYNCED MÀU XANH LÁ!
    Note over Pod: Pods KHÔNG HỀ BIẾT CÓ THAY ĐỔI!<br/>Vì Pod Template trong Deployment không hề đổi!
    Note over Dev,Pod: BẪY NGUY HIỂM: UI báo xanh nhưng Pods vẫn chạy code cũ!


```

### 7.1. Phân Tích Nguyên Nhân Gốc Rễ (5-Whys)
1. **Tại sao người dùng không thấy tính năng mới?** $\rightarrow$ Vì Pods chưa nạp biến môi trường mới.
2. **Tại sao Pods không nạp?** $\rightarrow$ Vì Kubernetes không tự động restart Pod khi ConfigMap tĩnh bị sửa.
3. **Tại sao Kubernetes không restart Pod?** $\rightarrow$ Vì trường `spec.template` của Deployment không hề có bất kỳ thay đổi nào (generation không tăng).
4. **Tại sao kỹ sư dùng ConfigMap tĩnh thay vì Kustomize Generator?** $\rightarrow$ Do thói quen viết manifest Kubernetes thủ công trước đây mà chưa tận dụng tính năng hash của Kustomize.
5. **Giải pháp chuẩn hóa là gì?** $\rightarrow$ Quy định 100% ConfigMaps/Secrets phải được sinh qua `configMapGenerator` hoặc `secretGenerator` trong `kustomization.yaml`.

---

## 8. Hướng Dẫn Thực Hành CLI: Kiểm Thử Biên Dịch Kustomize Cục Bộ (Step-by-Step Lab)

| Bước | Lệnh / Thao Tác | Mục Đích Kỹ Thuật |
|---|---|---|
| **1. Di Chuyển Thư Mục** | `cd services/payment-service/overlays/production` | Truy cập vào thư mục overlay cấu hình của môi trường đích |
| **2. Biên Dịch Thử Nghiệm** | `kustomize build .` | Xem trước toàn bộ Kubernetes manifest hoàn chỉnh sau khi vá |
| **3. Kiểm Tra Hash Suffix** | `kustomize build . \| grep -A 8 "kind: ConfigMap"` | Xác minh ConfigMap đã được gắn mã băm SHA256 tự động |
| **4. Xác Minh Bản Vá** | `kustomize build . \| grep -A 20 "kind: Deployment"` | Kiểm tra các thông số CPU/RAM và Replicas đã được ghi đè |
| **5. Kiểm Tra Tính Hợp Lệ** | `kustomize build . \| kubeconform -strict -summary` | Kiểm thử schema validation đảm bảo manifest chuẩn K8s |
| **6. So Sánh Đa Môi Trường** | `diff <(kustomize build ../staging) <(kustomize build .)` | So sánh sự khác biệt cấu hình giữa Production và Staging |

```bash
# Bước 1: Di chuyển vào thư mục overlay production
cd services/payment-service/overlays/production

# Bước 2: Thực thi lệnh biên dịch để xem trước toàn bộ Kubernetes manifests đầu ra
kustomize build .

# Bước 3: Kiểm tra xem ConfigMap có được tự động gắn mã băm Hash Suffix không
kustomize build . | grep -A 8 "kind: ConfigMap"

# Bước 4: Kiểm tra xem các bản vá Patches (CPU/RAM/Replicas) đã được áp dụng đúng chưa
kustomize build . | grep -A 20 "kind: Deployment"

# Bước 5: Validate tính hợp lệ của manifest với kubeconform
kustomize build . | kubeconform -strict -summary

# Bước 6: So sánh sự khác biệt của Overlay Production so với Overlay Staging
diff <(kustomize build ../staging) <(kustomize build .)
```

---

## 9. Bộ Câu Hỏi Tự Kiểm Tra Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span class="qa-question-text">Tại sao Kustomize lại được gọi là công cụ quản lý cấu hình "Template-Free"?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Vì Kustomize không sử dụng cú pháp chèn mẫu như <code>{{ .Values.name }}</code> (như Helm). Toàn bộ các file trong Base và Overlays đều là các tệp <b style="color: var(--accent-primary);">Kubernetes YAML hợp lệ 100%</b> và có thể <code>kubectl apply</code> độc lập. Kustomize chỉ thực hiện thao tác sáp nhập và vá cấu trúc JSON/YAML (Patching).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span class="qa-question-text">Lợi ích cốt lõi của việc sử dụng configMapGenerator thay vì khai báo ConfigMap tĩnh là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Là tính năng <b style="color: var(--accent-primary);">Content Hash Suffix</b>. Mỗi khi nội dung cấu hình thay đổi, Kustomize tự động sinh ra một ConfigMap có tên mới (ví dụ <code>app-config-8f7d9a</code>) và cập nhật Deployment trỏ tới tên mới đó, giúp Kubernetes tự động kích hoạt Zero-Downtime Rolling Update mà không cần can thiệp thủ công.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span class="qa-question-text">Làm thế nào để tự động cập nhật Image Tag cho toàn bộ ứng dụng trong một môi trường mà không cần sửa file deployment.yaml?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Sử dụng khối <code>images:</code> trong <code>kustomization.yaml</code>:
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"><code>images:</code><br/><code>  - name: company/app</code><br/><code>    newTag: "v2.0.0"</code></div>
    Kustomize sẽ tự động quét toàn bộ các Deployment/StatefulSet có chứa image <code>company/app</code> và thay thế tag thành <code>v2.0.0</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span class="qa-question-text">Có thể xếp chồng (nest) nhiều tầng Overlays lên nhau trong Kustomize không?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <b style="color: var(--accent-primary);">Hoàn toàn được!</b> Kustomize hỗ trợ mô hình đa tầng phân cấp không giới hạn. Một thư mục <code>kustomization.yaml</code> có thể tham chiếu đến một thư mục cha khác thông qua trường <code>resources: [../path]</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span class="qa-question-text">Trong kiến trúc GitOps của Argo CD, trường spec.source.path nên trỏ vào thư mục Base hay thư mục Overlay?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Bắt buộc phải trỏ vào <b style="color: var(--accent-primary);">thư mục Overlay tương ứng của môi trường đó</b> (ví dụ: <code>services/payment/overlays/production</code>). Thư mục Overlay sẽ tự động kéo thư mục Base về biên dịch thành bản manifest hoàn chỉnh cho môi trường đó.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span class="qa-question-text">Kustomize Components khác biệt thế nào so với việc kế thừa Base thông thường?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Kế thừa Base là quan hệ "IS-A" (môi trường này là phiên bản mở rộng của Base). Trong khi đó, <code>Components</code> là quan hệ "HAS-A" (mô hình Plug-and-Play), cho phép nhiều Overlays khác nhau tùy ý nhúng hoặc không nhúng một module tính năng (như Tracing, Prometheus Exporter, TLS Ingress) mà không làm ô nhiễm cấu hình Base.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span class="qa-question-text">Khi nào kỹ sư bắt buộc phải sử dụng JSON 6902 Patch thay vì Strategic Merge Patch?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Khi cần thực hiện các thao tác phức tạp trên mảng (Array) mà Strategic Merge không hỗ trợ, chẳng hạn như xóa hoàn toàn một phần tử cụ thể khỏi mảng, thay thế chính xác một biến môi trường ở vị trí index xác định, hoặc sửa trường trong CRD không có strategic merge schema.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span class="qa-question-text">Làm thế nào để vô hiệu hóa mã băm (Disable Hash Suffix) trong configMapGenerator nếu hệ thống yêu cầu tên cố định?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Thêm tùy chọn <code>options: { disableNameSuffixHash: true }</code> vào khối khai báo trong <code>kustomization.yaml</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span class="qa-question-text">Lệnh nào giúp kiểm tra kết quả biên dịch Kustomize mà không cần cài đặt binary kustomize riêng biệt?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Sử dụng lệnh tích hợp sẵn trong Kubectl: <code>kubectl kustomize &lt;đường_dẫn_thư_mục&gt;</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span class="qa-question-text">Tác dụng của trường commonLabels trong tệp kustomization.yaml là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <code>commonLabels</code> sẽ được Kustomize gắn tự động vào cả hai nơi: <code>metadata.labels</code> của toàn bộ tài nguyên (Deployment, Service, Ingress) VÀ <code>spec.template.metadata.labels</code> cùng với <code>spec.selector.matchLabels</code> của Deployment/StatefulSet.
  </div>
</details>

---

## Tổng Kết

Kustomize là chuẩn mực vàng để hiện thực hóa triết lý DRY trong quản trị cấu hình Kubernetes đa môi trường. Bằng việc kết hợp Base & Overlays, Kustomize Components và ConfigMapGenerator, đội ngũ kỹ thuật có thể quản lý hàng trăm ứng dụng một cách nhất quán, giảm thiểu sai sót và đảm bảo các bản cập nhật cấu hình luôn được kích hoạt mượt mà trên Production.

> [!TIP]
> **Khám phá bài học tiếp theo:**  
> Đọc tiếp bài [Bài 10: Quản Lý Helm Charts Với Argo CD & Kỹ Thuật Multiple Sources $values Nâng Cao](argocd-10-10-quan-ly-helm-charts-voi-argo-cd-va-ky-thuat-multiple-sources.html) để làm chủ kỹ thuật quản trị Helm Chart kết hợp kho Git values đa tầng.
{% endraw %}
