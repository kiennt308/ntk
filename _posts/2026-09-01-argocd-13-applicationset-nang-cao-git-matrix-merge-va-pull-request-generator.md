---
layout: post
title: "[Bài 13] ApplicationSet Nâng Cao: Git Matrix, Merge & Pull Request Preview Generator"
date: 2026-09-01 08:00:00 +0700
categories: [ArgoCD]
tags:
  - ArgoCD
  - GitOps
  - Kubernetes
  - CICD
  - CloudNative
  - Part-13
series: "ArgoCD & GitOps Mastery"
series_order: 13
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1556075798-4825dfaaf498?auto=format&fit=crop&w=1200&q=80"
summary: "Khai phóng toàn bộ sức mạnh của Argo CD ApplicationSet: Tự động hóa Zero-Touch với Git Directory/File Generator, nhân ma trận đa dịch vụ đa cụm với Matrix & Merge Generator, và thiết lập môi trường thử nghiệm tạm thời Ephemeral Preview Environments cho từng Pull Request."
---

{% raw %}
# ApplicationSet Nâng Cao: Git Matrix, Merge & Pull Request Preview Generator

Trong bài viết trước, chúng ta đã làm quen với List và Cluster Generator. Tuy nhiên, trong các doanh nghiệp công nghệ quy mô hàng đầu (như Intuit, Google, Red Hat), quy trình phân phối phần mềm đòi hỏi sự linh hoạt và tự động hóa cao hơn gấp nhiều lần:

1. **Zero-Touch GitOps:** Khi một kỹ sư tạo một thư mục microservice mới trên Git, hệ thống phải **tự động phát hiện và triển khai ngay lập tức** mà không cần sửa bất kỳ tệp manifest cấu hình nào!
2. **Multi-Cluster Matrix Scaling:** Bạn có 20 microservices cần triển khai trên 5 cụm Kubernetes khác nhau với cấu hình phân tầng.
3. **Ephemeral Preview Environments (Môi trường tạm thời theo Pull Request):** Mỗi khi một lập trình viên mở một Pull Request (PR) trên GitHub/GitLab, Argo CD phải tự động dựng một môi trường hoàn chỉnh (bao gồm Backend, Frontend, Ingress riêng) để QA và Product Owner kiểm thử tính năng; và **tự động xóa sạch toàn bộ môi trường khi PR được merge hoặc đóng**!

> [!IMPORTANT]
> **ZERO-TOUCH GITOPS VÀ MA TRẬN PHÂN PHỐI:**
> Sử dụng ApplicationSet nâng cao giúp loại bỏ 100% việc cấu hình thủ công khi thêm mới dịch vụ hoặc mở rộng sang cụm Kubernetes mới. Toàn bộ chu trình sinh và hủy tài nguyên đều tuân thủ chặt chẽ nguyên lý Khai báo GitOps.

> [!TIP]
> **TIẾT KIỆM CHI PHÍ VỚI EPHEMERAL PREVIEW ENVIRONMENTS:**
> Pull Request Generator kết hợp với TTL Controller giúp tự động hủy các môi trường tạm sau khi Pull Request được merge hoặc đóng, tiết kiệm tới 60% chi phí hạ tầng Cloud cho môi trường Non-Production.

---

## 1. Zero-Touch Git Directory & File Generator

**Git Generator** giải phóng hoàn toàn kỹ sư khỏi việc khai báo danh sách dịch vụ. Controller sẽ tự động duyệt qua cây thư mục của kho GitOps để tìm kiếm các tệp hoặc thư mục thỏa mãn điều kiện.

```mermaid
flowchart TD
    subgraph GIT_TREE["KHO MÃ NGUỒN GITOPS (GitHub Repo)"]
        D1["Thư mục: services/payment-api/"]
        D2["Thư mục: services/order-api/"]
        D3["Thư mục mới tạo: services/notification-api/"]
    end

    APPSET_GIT["ApplicationSet (Git Directory Generator)<br/>directories: [services/*]"]

    GIT_TREE -->|Tự động quét cây thư mục| APPSET_GIT

    subgraph AUTO_APPS["TỰ ĐỘNG SINH ỨNG DỤNG TỨC THÌ (Zero-Touch)"]
        A1["App: payment-api"]
        A2["App: order-api"]
        A3["App: notification-api (Tự động sinh sau 3s khi commit!)"]
    end

    APPSET_GIT --> A1
    APPSET_GIT --> A2
    APPSET_GIT --> A3


```

### 1.1. Các Biến Hữu Ích Của Git Directory Generator
- **`{{path}}`:** Đường dẫn đầy đủ của thư mục (ví dụ: `services/payment-api`).
- **`{{path.basename}}`:** Tên của thư mục cuối cùng (ví dụ: `payment-api`).
- **`{{path[0]}}`, `{{path[1]}}`:** Phân tách từng phần tử trong đường dẫn.

---

## 2. Matrix Generator: Nhân Ma Trận Tích Đa Chiều (Cartesian Product)

Khi bạn muốn triển khai một danh sách $N$ Microservices lên một danh mục $M$ Cụm Kubernetes, bạn không cần phải viết $N \times M$ cấu hình. **Matrix Generator** sẽ thực hiện phép nhân tích Descartes giữa 2 Generators độc lập.

```mermaid
flowchart LR
    GEN_1["Generator 1: Git Directory<br/>[payment, order, catalog]<br/>(3 Dịch vụ)"]
    GEN_2["Generator 2: Cluster Generator<br/>[cluster-staging, cluster-prod]<br/>(2 Cụm)"]

    MATRIX["MATRIX GENERATOR (Tích Descartes 3 x 2)"]

    GEN_1 --> MATRIX
    GEN_2 --> MATRIX

    subgraph SIX_APPS["TỰ ĐỘNG SINH RA 6 ỨNG DỤNG ĐỘC LẬP"]
        P1["payment - staging"]
        P2["payment - prod"]
        O1["order - staging"]
        O2["order - prod"]
        C1["catalog - staging"]
        C2["catalog - prod"]
    end

    MATRIX ==> SIX_APPS


```

### 2.1. Phân Tích Cấu Hình Chi Tiết Matrix Generator (Line-by-Line Breakdown)

```yaml
# appset-matrix-ecommerce.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: ecommerce-matrix-deployer
  namespace: argocd
spec:
  generators:
    - matrix:
        generators:
          # 1. GENERATOR THỨ NHẤT: Quét danh mục các Cụm mục tiêu
          - clusters:
              selector:
                matchLabels:
                  tier: production
          # 2. GENERATOR THỨ HAI: Quét toàn bộ các Microservices trong kho Git
          - git:
              repoURL: "https://github.com/company/ecommerce-gitops.git"
              revision: "main"
              directories:
                - path: "services/*"
  template:
    metadata:
      # Sinh tên: payment-api-cluster-us-east
      name: "{{path.basename}}-{{name}}"
      labels:
        service: "{{path.basename}}"
        cluster: "{{name}}"
        environment: "{{metadata.labels.env}}"
    spec:
      project: default
      source:
        repoURL: "https://github.com/company/ecommerce-gitops.git"
        targetRevision: "main"
        path: "{{path}}/overlays/{{metadata.labels.env}}"
      destination:
        server: "{{server}}"
        namespace: "{{path.basename}}-{{metadata.labels.env}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
          - ServerSideApply=true
```

---

## 3. Merge Generator: Hợp Nhất & Ghi Đè Cấu Hình Có Điều Kiện

Trong khi Matrix Generator nhân chéo toàn bộ dữ liệu, **Merge Generator** cho phép bạn gộp nhiều generator lại và ghi đè tham số cho các trường hợp ngoại lệ dựa trên khóa định danh `mergeKeys`:

```mermaid
flowchart TD
    BASE_GEN["Base Generator: Cluster Generator<br/>(Sinh cấu hình mặc định: replicas=3 cho 10 cụm)"]
    OVERRIDE_GEN["Override Generator: List Generator<br/>(Chỉ định riêng cho cluster-prod-us: replicas=10)"]
    MERGE["MERGE GENERATOR (mergeKeys: [server])"]

    BASE_GEN --> MERGE
    OVERRIDE_GEN --> MERGE
    MERGE --> RESULT["10 Cụm được tạo:<br/>- 9 cụm chạy replicas=3<br/>- Riêng cụm US chạy replicas=10!"]


```

### 3.1. Manifest Minh Họa Merge Generator
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: global-ingress-merge
  namespace: argocd
spec:
  generators:
    - merge:
        mergeKeys:
          - server
        generators:
          - clusters:
              values:
                replicas: "3"
          - list:
              elements:
                - server: "https://k8s-prod-us.company.com:6443"
                  replicas: "10"
  template:
    metadata:
      name: "ingress-{{name}}"
    spec:
      project: default
      source:
        repoURL: "https://charts.bitnami.com/bitnami"
        chart: "nginx-ingress-controller"
        targetRevision: "9.3.0"
        helm:
          parameters:
            - name: "replicaCount"
              value: "{{values.replicas}}"
      destination:
        server: "{{server}}"
        namespace: "kube-ingress"
```

---

## 4. Pull Request Generator: Tự Động Dựng Môi Trường Xem Trước (Ephemeral Preview Environments)

Trong quy trình phát triển hiện đại, việc lập trình viên mở một Pull Request và phải chờ đến khi code được merge vào nhánh chính mới được kiểm thử là một sự lãng phí thời gian lớn.

**Pull Request Generator** cho phép Argo CD kết nối trực tiếp với GitHub/GitLab API, liên tục quét các PR đang mở và tự động tạo ra một Application riêng biệt cho từng PR.

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Lập trình viên
    participant GitHub as GitHub / GitLab (Repo)
    participant AppSet as ApplicationSet PR Controller
    participant K8s as Kubernetes Cluster
    participant Ingress as Ingress Router

    Dev->>GitHub: Mở Pull Request #142 (Nhánh: feat-new-payment)
    AppSet->>GitHub: Quét danh sách PRs qua GitHub API
    Note over AppSet: Phát hiện PR #142 đang MỞ (Open)!
    AppSet->>K8s: Tự động tạo Namespace: preview-pr-142
    AppSet->>K8s: Triển khai toàn bộ Workloads cho PR #142
    AppSet->>Ingress: Cấp phát URL: https://pr-142.preview.company.com
    Note over Dev,Ingress: QA & Product Owner truy cập URL kiểm thử tính năng độc lập!

    Dev->>GitHub: Merge hoặc Close Pull Request #142
    AppSet->>GitHub: Quét lại danh sách PRs
    Note over AppSet: PR #142 đã ĐÓNG (Closed)!
    AppSet->>K8s: TỰ ĐỘNG XÓA SẠCH SẼ Namespace preview-pr-142!<br/>(Giải phóng 100% RAM/CPU)


```

---

## 5. Phân Tích Cấu Hình Chi Tiết Pull Request Generator (Line-by-Line Breakdown)

```yaml
# appset-pull-request-preview.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: frontend-pr-preview-environments
  namespace: argocd
spec:
  generators:
    - pullRequest:
        # Khai báo nhà cung cấp Git (github, gitlab, gitea, bitbucket)
        github:
          owner: company-org
          repo: frontend-app
          # Token GitHub để tăng giới hạn API Rate Limit
          tokenRef:
            secretName: github-token-secret
            key: token
        # Bộ lọc chỉ dựng môi trường cho các PR có gắn nhãn 'preview' hoặc target vào 'main'
        filters:
          - branchMatch: ".*"
            targetBranchMatch: "main"
  template:
    metadata:
      # Sinh tên duy nhất theo số PR: frontend-preview-pr-142
      name: "frontend-preview-pr-{{number}}"
      labels:
        pr-number: "{{number}}"
        branch: "{{branch_slug}}"
    spec:
      project: preview-environments
      source:
        repoURL: "https://github.com/company-org/frontend-app.git"
        # Trỏ chính xác vào Commit SHA hoặc Head Branch của PR
        targetRevision: "{{head_sha}}"
        path: "manifests/preview"
        kustomize:
          namePrefix: "pr-{{number}}-"
      destination:
        server: "https://kubernetes.default.svc"
        namespace: "preview-pr-{{number}}"
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

### Các Biến Có Sẵn Trong Pull Request Generator:
- **`{{number}}`:** Số thứ tự của Pull Request (ví dụ `142`).
- **`{{branch}}`:** Tên nhánh nguồn của PR (ví dụ `feature/payment-v2`).
- **`{{branch_slug}}`:** Tên nhánh đã được chuẩn hóa an toàn cho DNS (ví dụ `feature-payment-v2`).
- **`{{head_sha}}`:** Mã Commit SHA mới nhất của PR.

---

## 6. Cấu Hình Webhook Bắn Sự Kiện Trực Tiếp Cho ApplicationSet

Thay vì dựa vào Polling định kỳ làm tốn quota API, bạn có thể thiết lập GitHub Webhook gửi payload trực tiếp tới endpoint `/api/webhook` của Argo CD:

```bash
# Cấu hình Webhook Secret trong Argo CD
kubectl patch secret argocd-secret -n argocd \
  -p '{"stringData":{"webhook.github.secret":"my-github-webhook-secret-token"}}'
```

Khi có sự kiện `Pull Request` mở, cập nhật hoặc đóng, GitHub sẽ kích hoạt webhook và Argo CD ApplicationSet Controller sẽ khởi tạo hoặc dọn dẹp môi trường chỉ sau **2 giây**!

---

## 7. Cạm Bẫy Thực Chiến: "GitHub API Rate Limit Làm Đóng Băng Toàn Bộ Hệ Thống ApplicationSet"

### Hiện Tượng Sự Cố & Log Trace
- Toàn bộ các ApplicationSet sử dụng Pull Request Generator hoặc Git Generator bất ngờ **ngừng hoạt động hoàn toàn**.
- Các PR mới mở không được tạo môi trường xem trước, các PR đã đóng không được dọn dẹp, gây lãng phí tài nguyên máy chủ.
- Khi kiểm tra log của `argocd-applicationset-controller`, xuất hiện hàng ngàn dòng lỗi `HTTP 403 Forbidden: API rate limit exceeded`:

```json
{
  "timestamp": "2026-04-02T14:05:11Z",
  "level": "error",
  "component": "applicationset-controller",
  "msg": "failed to list pull requests for repository company-org/frontend-app",
  "error": "GET https://api.github.com/repos/company-org/frontend-app/pulls: 403 API rate limit exceeded for IP 35.201.12.4. (But here's the good news: Authenticated requests get a higher rate limit.)"
}
```

```mermaid
flowchart TD
    APPSET["ApplicationSet PR Controller (Không gắn Token GitHub)"] -->|Gọi API liên tục mỗi 3 phút| GITHUB["GitHub Public API Server"]
    GITHUB -->|Vượt quá ngưỡng 60 requests/giờ!| RATE_LIMIT["HTTP 403 API RATE LIMIT EXCEEDED!"]
    RATE_LIMIT ==> TRAP["HẬU QUẢ: Toàn bộ Preview Environments bị TÊ LIỆT HOÀN TOÀN!"]


```

### 7.1. Phân Tích Nguyên Nhân Gốc Rễ (5-Whys)
1. **Tại sao Preview Environments không được tạo?** $\rightarrow$ Vì ApplicationSet Controller bị GitHub chặn truy vấn.
2. **Tại sao bị GitHub chặn?** $\rightarrow$ Do mã phản hồi HTTP 403 Rate Limit Exceeded.
3. **Tại sao lại vượt ngưỡng Rate Limit?** $\rightarrow$ Vì Controller sử dụng truy vấn nặc danh (Unauthenticated) chỉ có hạn mức 60 requests/giờ trong khi có 10 PRs được quét liên tục.
4. **Tại sao không có token xác thực?** $\rightarrow$ Do kỹ sư quên khai báo khối `tokenRef` trong ApplicationSet manifest.
5. **Giải pháp chuẩn hóa là gì?** $\rightarrow$ Cấu hình GitHub App Token hoặc Personal Access Token với quyền hạn tối thiểu (Read-Only PRs) để nâng hạn mức lên 5,000 requests/giờ.

---

## 8. Hướng Dẫn Thực Hành CLI: Quản Trị Matrix & PR Applications (Step-by-Step Lab)

Dưới đây là quy trình thực hành từ dòng lệnh để triển khai và quản trị Matrix & PR Generators:

```bash
# Bước 1: Tạo Secret chứa GitHub Personal Access Token để xác thực PR Generator
kubectl create secret generic github-token-secret -n argocd \
  --from-literal=token=ghp_YourSecretGitHubPersonalAccessToken998877

# Bước 2: Triển khai ApplicationSet Matrix Generator
kubectl apply -f appset-matrix-ecommerce.yaml

# Bước 3: Kiểm tra danh sách các Application được tạo bởi Matrix Generator
argocd app list -l "app.kubernetes.io/managed-by=applicationset-controller"

# Bước 4: Triển khai ApplicationSet Pull Request Preview
kubectl apply -f appset-pull-request-preview.yaml

# Bước 5: Xem các biến đã được gán vào một Application Preview cụ thể
argocd app get frontend-preview-pr-142

# Bước 6: Ép buộc ApplicationSet quét lại toàn bộ kho Git và PRs ngay lập tức
kubectl annotate applicationset frontend-pr-preview-environments -n argocd \
  argocd.argoproj.io/refresh=now --overwrite
```

---

## 9. Bộ Câu Hỏi Tự Kiểm Tra Chuyên Sâu (Self-Check Q&A)

Dưới đây là 10 câu hỏi sát hạch chuyên sâu về Matrix, Merge & PR Generators:

### Câu 1: Phép tính toán nào được thực hiện bên trong Matrix Generator?
- **Đáp án:** Phép **nhân tích Descartes (Cartesian Product)**. Nếu Generator A sinh ra 4 phần tử và Generator B sinh ra 3 phần tử, Matrix Generator sẽ kết hợp từng phần tử của A với từng phần tử của B để tạo ra tổng cộng $4 \times 3 = 12$ bộ tham số cho Template.

### Câu 2: Biến `{{branch_slug}}` khác gì so với biến `{{branch}}` trong Pull Request Generator?
- **Đáp án:** Biến `{{branch}}` giữ nguyên tên nhánh gốc (có thể chứa ký tự `/`, `_` hoặc chữ hoa, ví dụ `feat/Fix_Bug_#1`). Biến `{{branch_slug}}` tự động chuẩn hóa chuỗi này thành định dạng an toàn cho Kubernetes DNS (đổi chữ hoa thành chữ thường, đổi `/` và `_` thành dấu `-`, ví dụ `feat-fix-bug-1`).

### Câu 3: Khi nào nên sử dụng Merge Generator thay vì Matrix Generator?
- **Đáp án:** Sử dụng **Merge Generator** khi bạn muốn gộp 2 generator lại với nhau và cho phép **ghi đè (Override) các tham số cấu hình cục bộ theo điều kiện**. Ví dụ: Áp dụng cấu hình chung cho 10 cụm, nhưng riêng cụm `prod-us` cần ghi đè số lượng `replicas: 10`.

### Câu 4: Làm thế nào để ngăn chặn Pull Request Generator tự động tạo môi trường cho các PR của người lạ (tránh bị đào Bitcoin trái phép)?
- **Đáp án:** Sử dụng bộ lọc bảo mật trong `pullRequest.github.filters`:
  - `labels`: Chỉ tạo môi trường khi PR được gắn nhãn `safe-to-test` bởi Maintainer.
  - `forkMatch`: Cấm hoặc giới hạn các PR xuất phát từ các kho fork bên ngoài.

### Câu 5: Cần làm gì để đảm bảo toàn bộ tài nguyên của PR Preview bị xóa sạch khi PR đóng lại?
- **Đáp án:** (1) Đảm bảo `spec.syncPolicy.preserveResourcesOnDeletion` là `false`, (2) Gắn `finalizers: [resources-finalizer.argocd.argoproj.io]` vào `template.metadata.finalizers`, và (3) Khai báo `destination.namespace: "preview-pr-{{number}}"` kèm `syncPolicy.automated.prune: true`.

### Câu 6: Làm thế nào để kết hợp Git File Generator với Matrix Generator?
- **Đáp án:** Đặt Git File Generator vào một nhánh của Matrix Generator để đọc cấu hình từ các tệp `config.json` nằm trong từng thư mục dịch vụ, sau đó nhân chéo với Cluster Generator để áp dụng các tham số riêng biệt cho từng cụm.

### Câu 7: `requeueAfterSeconds` trong Pull Request Generator có tác dụng gì?
- **Đáp án:** Chỉ định chu kỳ thời gian (tính bằng giây) mà Controller sẽ chủ động gửi request lên GitHub API để kiểm tra danh sách PRs mới hoặc trạng thái đóng/mở PR (mặc định là 1800 giây - 30 phút).

### Câu 8: Tại sao nên sử dụng GitHub App thay vì Personal Access Token (PAT) cho Pull Request Generator?
- **Đáp án:** GitHub App có cơ chế cấp quyền theo tổ chức và repo cụ thể (Least Privilege), hỗ trợ hạn mức API lớn hơn (lên tới 15,000 requests/giờ) và không bị phụ thuộc vào tài khoản cá nhân của kỹ sư (tránh lỗi khi nhân viên nghỉ việc).

### Câu 9: Trong Git Directory Generator, cú pháp `path: "services/*"` khác gì với `path: "services/**"`?
- **Đáp án:** `services/*` chỉ quét các thư mục con cấp 1 trực tiếp bên trong `services/`. Cú pháp `services/**` quét đệ quy toàn bộ mọi cấp thư mục lồng nhau bên trong.

### Câu 10: Làm thế nào để loại trừ một thư mục cụ thể (như thư mục `services/archive`) khỏi Git Directory Generator?
- **Đáp án:** Sử dụng trường `exclude: true` trong danh sách `directories`:
  ```yaml
  directories:
    - path: "services/*"
    - path: "services/archive"
      exclude: true
  ```

---

## Tổng Kết

Các Generator nâng cao của `ApplicationSet` là đỉnh cao của tự động hóa GitOps hiện đại, mang lại trải nghiệm phát triển phần mềm mượt mà, tối ưu hóa chi phí hạ tầng và mở rộng quy mô không giới hạn.

Ở bài tiếp theo, chúng ta sẽ đi sâu vào **Quản Trị Đa Cụm: Multi-Cluster GitOps & Kỹ Thuật Triển Khai Chéo Hạ Tầng Chuẩn Enterprise**!
{% endraw %}
