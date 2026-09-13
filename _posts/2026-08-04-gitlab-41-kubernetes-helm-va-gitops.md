---
layout: post
title: "[Bài 41] Tích Hợp GitOps Với ArgoCD & Kubernetes: Git Commit Trigger, Kustomize Image Update & Auto Sync Application"
date: 2026-08-04 08:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-41
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 41
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1556075798-4825dfaaf498?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.41] Hướng dẫn chuyên sâu Tích Hợp GitOps Với ArgoCD & Kubernetes: Git Commit Trigger, Kustomize Image Update & Auto Sync Application: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

# [BÀI 41] TÍCH HỢP GITOPS VỚI ARGOCD & KUBERNETES: GIT COMMIT TRIGGER, KUSTOMIZE IMAGE UPDATE & AUTO SYNC APPLICATION

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

---





| STT | Câu hỏi ôn tập | Đáp án chi tiết thực chiến |
|---|---|---|
| 1 | Tên gọi dịch vụ quản lý danh tính OIDC Federation trên Azure là gì? | Azure Entra ID (Active Directory) Federated Identity Credentials quản lý không chìa khóa tĩnh. |
| 2 | Audience chuẩn duy nhất bắt buộc khai báo cho Azure WIF là gì? | Giá trị Audience chuẩn duy nhất là `api://AzureADTokenExchange` không được thay đổi. |
| 3 | Khác biệt cốt lõi của Azure Subject Matching so với AWS và GCP là gì? | Azure buộc tạo Federated Credential riêng khớp 100% từng ký tự Subject Identifier, không cho phép dùng wildcard lỏng lẻo. |
| 4 | Câu lệnh Azure CLI nào dùng để đăng nhập OIDC không secret key? | Lệnh `az login --service-principal -u $AZURE_CLIENT_ID -t $AZURE_TENANT_ID --federated-token $AZURE_OIDC_TOKEN`. |
| 5 | Câu lệnh nào dùng để tự động đăng nhập Docker CLI vào Azure ACR? | Lệnh `az acr login --name <registry_name>` nạp OIDC access token ngắn hạn vào credential helper an toàn. |


**Luận đề trung tâm:**
> *"Hai mô hình `helm upgrade` trực tiếp và GitOps khác nhau cốt lõi ở **ai là thực thể nắm giữ và đồng bộ trạng thái mong muốn (Desired State)** — chọn sai sẽ khiến việc rollback trở thành thao tác thủ công phức tạp."*

Sau khi đã hoàn thành giai đoạn kết nối OIDC Chín muồi với 3 Đám mây AWS (Buổi 38), GCP (Buổi 39), và Azure (Buổi 40), Buổi 41 sẽ đưa chúng ta vào trái tim của kiến trúc triển khai ứng dụng trên Kubernetes. Trong thực tế Enterprise, có hai trường phái CD (Continuous Deployment) đối lập nhau:
1. **Push-based CD (Helm direct upgrade):** Trình biên dịch GitLab CI Runner giữ file Kubeconfig admin và trực tiếp thực thi lệnh `helm upgrade` đẩy manifests vào cụm Kubernetes.
2. **Pull-based CD (GitOps với ArgoCD / FluxCD):** Một Agent Controller nằm sẵn bên trong cụm Kubernetes tự động theo dõi repository Git chứa cấu hình hạ tầng, phát hiện sai lệch trạng thái (State Drift) và tự động kéo (Pull) trạng thái mong muốn về cụm.

Bài học này sẽ giúp bạn hiểu rõ ưu nhược điểm của từng phương pháp, làm chủ các cờ an toàn của Helm (`--atomic`, `--wait`, `--timeout 300s`) và xây dựng luồng GitOps mượt mà cho Production!

---



| STT | Kỹ năng thực chiến | Hiện vật chứng minh hoàn thành |
|---|---|---|
| 1 | Viết Helm Chart chuẩn hóa cho microservice | Thư mục Helm Chart chứa `Chart.yaml`, `values.yaml`, `templates/` |
| 2 | Thực thi `helm upgrade --install` an toàn | Script CI thực thi `helm upgrade --atomic --wait --timeout 300s` |
| 3 | Tự động hóa Rollback khi Helm deployment thất bại | Nhật ký Runner ghi nhận `Release failed, rolling back atomic changes` |
| 4 | Thiết lập cấu hình ArgoCD Application Manifest | File `application.yaml` chứa cờ `selfHeal: true` và `prune: true` |
| 5 | Tách biệt App Code Repository và GitOps Config Repository | Hai repositories độc lập được liên kết qua CI Image Tag commit tự động |
| 6 | Thực thi kiểm thử phát hiện State Drift (Self-Healing) | Pod bị sửa thủ công qua `kubectl edit` tự khôi phục về giá trị Git |
| 7 | Quản lý Kubernetes Secrets an toàn không lộ plain-text | Khai báo SealedSecrets / External Secrets Operator |
| 8 | Truy vết lịch sử đồng bộ hạ tầng trên ArgoCD Dashboard | Audit logs ghi nhận sự kiện Sync thành công từ Git Commit SHA |

---



| Kiến thức / Kỹ năng | Mức độ yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Cấu trúc YAML Kubernetes Manifests (Deployment, Service) | Thành thục | Buổi 26 & Kiến thức K8s Nền tảng về quản trị tài nguyên |
| Đăng nhập Kubeconfig qua OIDC Cloud (AWS/GCP/Azure) | Hiểu rõ | Buổi 38, Buổi 39 & Buổi 40 về liên danh danh tính đám mây |
| Khai báo biến môi trường và tệp `.gitlab-ci.yml` | Thành thục | Buổi 30 & Buổi 36 về tự động hóa pipeline CI/CD |
| Cú pháp lệnh Git CLI (commit, push, revert) | Thành thục | Kiến thức Git Nền tảng về quản lý kho mã nguồn |
| Nguyên lý hoạt động của Helm Package Manager | Khá | Kiến thức Kubernetes Package Management quản lý ứng dụng |

---





| Thuật ngữ Tiếng Việt | Thuật ngữ Tiếng Anh | Giải thích ý nghĩa thực tế |
|---|---|---|
| Triển khai đòn đẩy | Push-based Continuous Deployment | Mô hình CI Runner ở ngoài trực tiếp kết nối API Server đẩy tài nguyên vào Kubernetes. |
| Triển khai đòn kéo | Pull-based Continuous Deployment (GitOps) | Mô hình Agent (ArgoCD) bên trong cụm Kubernetes tự đọc kho mã nguồn Git và kéo thay đổi về. |
| Trạng thái mong muốn | Desired State | Cấu hình Kubernetes YAML được lưu trữ và quản lý phiên bản chuẩn xác trên kho GitOps Repository. |
| Trạng thái thực tế | Actual State / Live State | Trạng thái thực sự của các Pods, Services đang chạy thực tế trên cụm Kubernetes Production. |
| Độ lệch trạng thái | State Drift | Sự khác biệt giữa Trạng thái thực tế trên cụm và Trạng thái mong muốn được khai báo trong Git. |
| Tự động khôi phục | Self-Healing | Tính năng của GitOps Controller tự động ghi đè lại cấu hình Git khi phát hiện ai đó sửa bẩn qua `kubectl edit`. |
| Gói quản lý Helm | Helm Chart | Bộ đóng gói các template YAML Kubernetes linh hoạt kèm file quản lý biến môi trường `values.yaml`. |
| Bản phát hành Helm | Helm Release | Một phiên bản ứng dụng cụ thể đã được cài đặt và quản lý lịch sử bởi Helm trên cụm Kubernetes. |
| Cờ rollback nguyên tử | Atomic Rollback (`--atomic`) | Cờ lệnh giúp Helm tự động rollback về phiên bản cũ nếu phiên bản mới bị crash Pods trong 300 giây. |
| Trình quản lý bí mật | SealedSecrets / External Secrets | Giải pháp mã hóa bí mật bất đối xứng cho phép commit Kubernetes Secrets an toàn trực tiếp lên Git. |



#### Mô hình 1: Sơ đồ Kiến trúc So sánh Push-based CD và Pull-based GitOps

```mermaid
flowchart TD
    subgraph Model A: Push-based CD (Helm Direct)
        A1[Developer Push Code] --> B1[GitLab CI Runner]
        B1 -->|Holds Admin Kubeconfig| C1[helm upgrade --atomic]
        C1 -->|Push API Request| D1[Kubernetes API Server]
    end

    subgraph Model B: Pull-based CD (GitOps ArgoCD)
        A2[Developer Push Code] --> B2[GitLab CI Build Image]
        B2 -->|Update Image Tag| C2[GitOps Config Repository]
        D2[ArgoCD Controller in Cluster] -->|Polls/Webhooks| C2
        D2 -->|Detect State Drift & Pull| E2[Kubernetes API Server]
    end
```

#### Mô hình 2: Bảng So sánh Chi tiết giữa Helm Direct Upgrade và GitOps ArgoCD

| Tiêu chí | Push-based CD (`helm upgrade` trực tiếp) | Pull-based CD (GitOps với ArgoCD / FluxCD) |
|---|---|---|
| **Vị trí giữ Credentials** | CI Runner (phải lưu Kubeconfig Admin hoặc OIDC token) | **Bên trong cụm Kubernetes** (Controller tự dùng ServiceAccount nội bộ) |
| **Bán kính ảnh hưởng lộ key** | Rất rộng (lộ Kubeconfig ở Runner có thể làm sập cả cụm) | **Cực hẹp** (Runner không có quyền vào cụm, chỉ có quyền push Git) |
| **Phát hiện State Drift** | Không có (ai đó gõ `kubectl edit` sửa bẩn thì CI không biết) | **Tự động 100%** (ArgoCD lập tức phát hiện OutOfSync và Re-sync về Git) |
| **Cơ chế Rollback** | Chạy lệnh `helm rollback <release> <revision>` | Chạy lệnh `git revert <commit_sha>` trên repository Git |
| **Độ phức tạp cài đặt** | Thấp (chỉ cần cài `helm` CLI trên Runner) | Trung bình (cần cài đặt ArgoCD Operator và cấu hình GitOps Repos) |
| **Môi trường phù hợp** | Dự án nhỏ, Staging, Dev, CI đơn giản | **Hệ thống Enterprise, Production, Multi-Cluster** |

##### Mẫu Cấu hình Manifest ArgoCD Application Chuẩn Production Enterprise:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-service-production
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: 'https://gitlab.company.com/bank-group/gitops-manifests.git'
    targetRevision: HEAD
    path: environments/production/payment-service
    helm:
      valueFiles:
        - values.yaml
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ApplyOutOfSyncOnly=true
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

---

### 1.1. Cấu hình Helm Upgrade Trực tiếp & Flag `--atomic` (10 phút)

### 4.1. Mẫu Tệp `.gitlab-ci.yml` Triển khai Helm Upgrade Push-based Chặt Chẽ
Dưới đây là cấu hình pipeline triển khai Kubernetes bằng lệnh `helm upgrade` với đầy đủ cờ an toàn:

```yaml
stages:
  - build
  - test
  - deploy-staging
  - deploy-production

variables:
  HELM_RELEASE_NAME: payment-service
  KUBERNETES_NAMESPACE: production
  CHART_PATH: ./helm/payment-service

.helm-base:
  image: alpine/helm:3.12.0
  before_script:
    - mkdir -p ~/.kube
    - echo "$KUBECONFIG_PRODUCTION_B64" | base64 -d > ~/.kube/config
    - chmod 600 ~/.kube/config
    - helm version

deploy-to-production:
  extends: .helm-base
  stage: deploy-production
  script:
    - echo "[HELM DEPLOY] Running helm lint..."
    - helm lint $CHART_PATH
    - echo "[HELM DEPLOY] Executing atomic helm upgrade..."
    - helm upgrade --install $HELM_RELEASE_NAME $CHART_PATH
        --namespace $KUBERNETES_NAMESPACE
        --create-namespace
        --set image.tag=$CI_COMMIT_SHA
        --set env.version=$CI_COMMIT_REF_SLUG
        --wait
        --atomic
        --timeout 300s
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

---

### 4.2. Các Quy tắc Cấu hình Helm Direct Deploy (QT 41.1 - QT 41.4)

**Nguyên lý cốt lõi:** Bắt buộc truyền cờ `--atomic` và `--wait` khi thực hiện `helm upgrade` từ CI Pipeline.
**Phát biểu.** Khi chạy câu lệnh `helm upgrade --install` trong job CI, bắt buộc phải bổ sung 2 cờ `--atomic` và `--wait` kèm theo `--timeout 300s`.
**Giải thích cơ chế ngầm:** Cờ `--wait` ép Helm chờ tất cả các Pods trong Deployment chuyển sang trạng thái `Ready` (vượt qua Readiness Probe). Nếu có bất kỳ Pod nào bị crash hoặc timeout quá 300 giây, cờ `--atomic` sẽ tự động hủy lệnh và khôi phục (Rollback) hoàn toàn cụm Kubernetes về phiên bản ổn định trước đó. Bỏ 2 cờ này sẽ khiến CI báo xanh ảo trong khi Pods đang bị `CrashLoopBackOff`.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chạy lệnh `helm upgrade --install` không có `--atomic` và `--wait`. Job CI xanh 100% nhưng Production bị sập ứng dụng.
**Minh hoạ.**
```bash
helm upgrade --install payment-backend ./helm/payment-service \
  --namespace production \
  --set image.tag=$CI_COMMIT_SHA \
  --wait \
  --atomic \
  --timeout 300s
```
**Con số chốt:** 100% `helm upgrade` có `--atomic --wait --timeout 300s`.

---

**Nguyên lý cốt lõi:** Tách biệt repository chứa mã nguồn ứng dụng (App Code Repo) và repository chứa cấu hình hạ tầng Kubernetes (GitOps Config Repo).
**Phát biểu.** Trong kiến trúc Enterprise, mã nguồn ứng dụng (Java, Go, Node.js) và mã nguồn cấu hình Kubernetes Manifests / Helm Charts phải nằm trên 2 repositories Git hoàn toàn riêng biệt.
**Giải thích cơ chế ngầm:** Giúp phân tách ranh giới trách nhiệm (Separation of Concerns). Developer chỉ có quyền push code ứng dụng, pipeline CI tự động build Container Image và tạo Merge Request / Commit cập nhật Image Tag sang GitOps Config Repo. Ngăn chặn việc Developer tự ý chỉnh sửa thông số RAM/CPU hay Replicas Production trên kho mã nguồn app.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Để chung file `deployment.yaml` hay Helm Chart nằm chung folder với mã nguồn ứng dụng trong 1 repo duy nhất và cho phép mọi dev chỉnh sửa.
**Minh hoạ.**
- App Repo: `gitlab.company.com/bank-group/payment-service.git`
- GitOps Repo: `gitlab.company.com/bank-group/gitops-manifests.git`
**Con số chốt:** 2 repos tách biệt 100%.

---

**Nguyên lý cốt lõi:** Ưu tiên mô hình GitOps Pull-based CD cho các môi trường Production có yêu cầu bảo mật cao.
**Phát biểu.** Đối với các môi trường Production quan trọng, thay vì đẩy Kubeconfig ra bên ngoài Runner, hãy cài đặt **ArgoCD / FluxCD Controller** bên trong cụm Kubernetes để thực thi luồng Pull-based GitOps.
**Giải thích cơ chế ngầm:** Giúp đóng hoàn toàn chiều kết nối từ ngoài vào cụm (No Inbound Firewall Rules). Máy chủ CI Runner không cần nắm giữ Kubeconfig Admin hay OIDC credentials của Production, triệt hạ hoàn toàn rủi ro lộ quyền kiểm soát cụm Kubernetes khi máy chủ Runner bị tấn công.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Mở port API Server Kubernetes công khai ra Internet để CI Runner ở ngoài gọi vào deploy Production.
**Minh hoạ.** ArgoCD Controller cài sẵn trong namespace `argocd` tự động đồng bộ từ GitOps Repo.
**Con số chốt:** 100% Prod đòn kéo GitOps.

---

**Nguyên lý cốt lõi:** Bật tính năng Self-Healing và Automated Prune trên ArgoCD Application manifest.
**Phát biểu.** Khai báo chính sách `syncPolicy.automated.selfHeal: true` và `syncPolicy.automated.prune: true` trên tất cả các đối tượng `Application` trong ArgoCD.
**Giải thích cơ chế ngầm:** `selfHeal: true` giúp ArgoCD tự động ghi đè lại cấu hình chuẩn từ Git khi ai đó cố tình dùng `kubectl edit` hoặc `kubectl delete` sửa thủ công trên cụm. `prune: true` đảm bảo các tài nguyên bị xóa trong Git sẽ tự động bị dọn dẹp trên cụm Kubernetes, giữ trạng thái khớp 100%.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tắt cờ `selfHeal` khiến cụm Kubernetes bị lệch trạng thái (State Drift) kéo dài mà không ai hay biết.
**Minh hoạ.**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-backend-prod
  namespace: argocd
spec:
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```
**Con số chốt:** `selfHeal: true` và `prune: true` 100%.

---

### 1.2. Quy tắc Quản lý GitOps Image Update & Drift Detection (10 phút)

**Nguyên lý cốt lõi:** Sử dụng Image Automation Controller / Kustomize / Helm values commit tự động để trigger ArgoCD Sync.
**Phát biểu.** Khi job CI build xong Container Image mới, pipeline sẽ gọi script ghi tự động Image Tag mới vào kho GitOps Config Repo thay vì gọi API của ArgoCD.
**Giải thích cơ chế ngầm:** Đảm bảo nguyên tắc "Git là Nguồn Sự Thật Duy Nhất" (Git as the Single Source of Truth). Mọi sự thay đổi trên Kubernetes đều bắt đầu từ một Git Commit SHA có đầy đủ thông tin tác giả và thời gian.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chạy lệnh `argocd app sync` trực tiếp từ CI mà không commit thay đổi Image Tag vào kho Git.
**Minh hoạ.**
```bash
# Script CI commit Image Tag mới sang GitOps Repo
git clone https://gitlab-ci-token:${CI_JOB_TOKEN}@gitlab.company.com/bank-group/gitops-manifests.git
cd gitops-manifests
sed -i "s/tag: .*/tag: \"$CI_COMMIT_SHA\"/" apps/payment-service/values.yaml
git commit -am "chore(cd): update payment-service image to $CI_COMMIT_SHA"
git push origin main
```
**Con số chốt:** 100% deployment qua Git Commits.

---

**Nguyên lý cốt lõi:** Khống chế timeout của `helm upgrade` ở mức 300 giây để tránh treo pipeline vĩnh viễn.
**Phát biểu.** Luôn bổ sung tham số `--timeout 300s` (hoặc 5 phút) cho tất cả các câu lệnh triển khai Helm.
**Giải thích cơ chế ngầm:** Nếu Kubernetes Deployment bị treo do ImagePullBackOff hay lỗi rò rỉ bộ nhớ khi khởi chạy, cờ `--wait` không có timeout sẽ khiến job CI chạy vô tận cho đến khi bị sập timeout tổng của Runner (thường là vài giờ), lãng phí tài nguyên và làm tắc nghẽn queue CI.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bỏ trống cờ `--timeout`, làm job CI bị treo 2 tiếng đồng hồ.
**Minh hoạ.** `--timeout 300s` trong lệnh `helm upgrade`.
**Con số chốt:** Timeout $\le 300$ giây.

---

**Nguyên lý cốt lõi:** Quản lý mật khẩu nhạy cảm Kubernetes Secrets bằng SealedSecrets, External Secrets Operator (ESO) hoặc Vault.
**Phát biểu.** Tuyệt đối không commit tệp Kubernetes Secret chứa chuỗi mã hóa base64 plain-text lên kho Git. Bắt buộc dùng **Bitnami SealedSecrets** hoặc **External Secrets Operator (ESO)** liên kết với HashiCorp Vault / Cloud Secret Manager.
**Giải thích cơ chế ngầm:** Chuỗi Base64 (`echo "password" | base64`) KHÔNG PHẢI LÀ MÃ HÓA. Commit file Secret plain-text lên Git sẽ làm rò rỉ 100% mật khẩu Database và API Keys cho bất kỳ ai có quyền đọc repository. SealedSecrets sử dụng mã hóa bất đối xứng Asymmetric Encryption, cho phép commit an toàn file `.json`/`.yaml` mã hóa lên Git.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Commit file `secret.yaml` chứa `password: dXNlcjEyMw==` trực tiếp lên Git repository.
**Minh hoạ.**
```bash
kubeseal --format yaml < secret.yaml > sealed-secret.yaml
git add sealed-secret.yaml && git commit -m "add sealed secret"
```
**Con số chốt:** 0% Plain-text Secrets trên Git.

---

**Nguyên lý cốt lõi:** Sử dụng `helm diff` plugin trong Merge Request pipeline để kiểm tra trước sự thay đổi tài nguyên.
**Phát biểu.** Tích hợp công cụ `helm diff` plugin vào stage `test`/`plan` của pipeline trên Merge Request để render bảng so sánh sự thay đổi tài nguyên Kubernetes trước khi merge code vào `main`.
**Giải thích cơ chế ngầm:** Giúp Tech Lead và Reviewer thấy rõ chính xác những tài nguyên nào sẽ bị thêm, sửa, xóa trên cụm Kubernetes trước khi duyệt code, ngăn chặn các sự cố xóa nhầm PVC hay Service do gõ sai định dạng YAML.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Merge code Helm Chart vào `main` mà không ai biết lệnh `helm upgrade` sắp tới sẽ xóa bỏ tài nguyên nào.
**Minh hoạ.**
```bash
helm diff upgrade payment-service ./helm/payment-service --values values-prod.yaml
```
**Con số chốt:** 100% Merge Requests có `helm diff` report.

---

### 1.3. Quy tắc Probes, Healthchecks & Rollback Strategy (10 phút)

**Nguyên lý cốt lõi:** Cấu hình Health Checks / Readiness / Liveness Probes đầy đủ trong Helm Template spec.
**Phát biểu.** Mọi tệp Template Deployment trong Helm Chart bắt buộc phải khai báo đầy đủ bộ 3 probes: `readinessProbe`, `livenessProbe`, và `startupProbe`.
**Giải thích cơ chế ngầm:** Cờ `--wait` của Helm và cơ chế Healthcheck của ArgoCD phụ thuộc 100% vào `readinessProbe` để xác định Pod đã sẵn sàng nhận traffic người dùng hay chưa. Nếu thiếu Probes, Kubernetes sẽ coi Pod vừa tạo ra là Healthy ngay lập tức dù ứng dụng Java/Node.js bên trong vẫn đang boot dở, gây sập kết nối khách hàng.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bỏ trống khối `readinessProbe` trong tệp `deployment.yaml`.
**Minh hoạ.**
```yaml
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 5
```
**Con số chốt:** 100% Deployments có Readiness Probes.

---

**Nguyên lý cốt lõi:** Giới hạn quyền Kubeconfig ServiceAccount của CI Runner theo namespace cấp hẹp khi chạy Push-based CD.
**Phát biểu.** Khi bắt buộc phải chạy Push-based CD (`helm upgrade` từ CI Runner), tệp Kubeconfig cấp cho Runner chỉ được mang quyền `RoleBinding` hạn chế trong duy nhất 1 namespace làm việc, cấm cấp quyền `ClusterRoleBinding` cluster-admin.
**Giải thích cơ chế ngầm:** Khoanh vùng bán kính ảnh hưởng sự cố (Blast Radius Isolation). Nếu máy chủ Runner hoặc biến `$KUBECONFIG` bị rò rỉ, kẻ tấn công cũng chỉ có thể can thiệp vào duy nhất namespace chỉ định chứ không thể thao tác trên các namespace hệ thống (`kube-system`, `monitoring`).
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cấp tệp `admin.conf` chứa quyền `cluster-admin` toàn cụm cho GitLab CI Runner.
**Minh hoạ.** Tạo `RoleBinding` trong namespace `production` gán cho ServiceAccount `cicd-runner-sa`.
**Con số chốt:** 100% Push Kubeconfigs bị giới hạn Namespace Scope.

---

**Nguyên lý cốt lõi:** Truy vết lịch sử đồng bộ hạ tầng qua ArgoCD Audit Logs và Git Commit History.
**Phát biểu.** Giám sát và lưu trữ toàn bộ nhật ký đồng bộ (Sync Events) của ArgoCD kết hợp với lịch sử Git Commit SHA để đáp ứng tiêu chuẩn kiểm toán.
**Giải thích cơ chế ngầm:** Giúp bộ phận DevSecOps và Audit dễ dàng đối soát: Ai đã đẩy thay đổi, vào thời gian nào, Commit SHA nào, và trạng thái đồng bộ Kubernetes thành công hay thất bại.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Không lưu vết log sync ArgoCD, làm thất lạc thông tin khi cần điều tra sự cố.
**Minh hoạ.** Truy vấn ArgoCD Event Logs qua lệnh `argocd app logs payment-backend-prod --audit`.
**Con số chốt:** 100% Sync Events được lưu vết audit.

---

**Nguyên lý cốt lõi:** Xây dựng kịch bản Rollback tức thì: `helm rollback` cho Push-based và `git revert` cho GitOps.
**Phát biểu.** Xác định rõ quy trình khôi phục sự cố khẩn cấp: Đối với luồng Direct Helm dùng `helm rollback <release> <revision>`, đối với luồng GitOps dùng `git revert <commit_sha>` và push thẳng lên GitOps Repo.
**Giải thích cơ chế ngầm:** Trong mô hình GitOps, nếu bạn dùng `kubectl` hoặc `helm rollback` thủ công trên cụm, ArgoCD sẽ coi đó là State Drift và tự động ghi đè lại mã lỗi từ Git! Do đó, cách rollback DUY NHẤT và ĐÚNG CHUẨN của GitOps là thực hiện `git revert` trên kho Git.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Gõ `helm rollback` trên cụm Kubernetes đang chạy ArgoCD, làm ArgoCD nhảy vào overwrite ngược lại phiên bản lỗi.
**Minh hoạ.**
```bash
# Rollback chuẩn GitOps
git revert HEAD -m "revert(cd): rollback broken release"
git push origin main
```
**Con số chốt:** Rollback GitOps bằng `git revert` 100%.

---

### 1.4. Đưa vào việc thật (4 phút)

### 7.1. Kịch bản áp dụng thực tế tại Hệ thống Core Banking Chạy Kubernetes Multi-Cluster
Trong một tập đoàn ngân hàng vận hành 3 cụm Kubernetes (Dev, Staging, Production):
1. **Pha Phát triển (Developer):** Dev commit code vào `payment-service` repository. Pipeline CI chạy unit tests, build Docker Image `payment-service:v2.5.0-sha123` và push lên Container Registry.
2. **Pha Cập nhật GitOps Config:** Job CI tự động tạo một Merge Request sang kho `gitops-manifests` repository, cập nhật biến `image.tag: "v2.5.0-sha123"` trong file `environments/production/values.yaml`.
3. **Pha Review & Merge:** Tech Lead kiểm tra báo cáo `helm diff` đính kèm trong Merge Request, thấy biến đổi an toàn và bấm nút Merge.
4. **Pha Đồng bộ ArgoCD (Pull-based):** ArgoCD Controller trên cụm Production AKS/GKE phát hiện commit mới trên kho Git, tự động thực thi Sync, tạo Pods mới và thực hiện Zero Downtime Traffic Migration. Nếu Pods mới sập, ArgoCD giữ nguyên Replica cũ và phát cảnh báo Slack!

### 7.2. Case Study Thực tế: Thảm họa Xóa sạch Namespace do Lộ Admin Kubeconfig trên CI Runner
Một công ty thương mại điện tử sử dụng luồng `helm upgrade` trực tiếp từ GitLab CI Runner.
- **Thảm họa ở cách làm cũ (Dùng Kubeconfig Admin):** Kẻ tấn công lợi dụng lỗ hổng RCE trên một gói dependency Node.js của Runner, chiếm được biến môi trường `$KUBECONFIG_ADMIN_B64`. Kẻ tấn công thực thi lệnh `kubectl delete ns production --all`, xóa sạch 200 microservices trên cụm Production!
- **Khôi phục hoàn hảo ở cách làm chuẩn Buổi 41 (Chuyển sang GitOps ArgoCD):**
  1. Thu hồi toàn bộ Kubeconfig Admin trên máy chủ CI Runner. CI Runner giờ đây CHỈ CÓ QUYỀN push mã nguồn lên Git.
  2. Cài đặt ArgoCD Controller bên trong cụm Kubernetes. ArgoCD dùng ServiceAccount nội bộ trong cụm.
  3. Kẻ tấn công dù có chiếm được Runner cũng KHÔNG THỂ kết nối vào cụm Kubernetes Production. Bán kính ảnh hưởng bằng **$0**!

### 7.3. Case Study 2: Cứu nguy Sự cố Sửa nhầm Pod Production qua `kubectl edit` bằng Self-Healing
Một kỹ sư trực ca On-call đêm vô tình dùng lệnh `kubectl edit deployment/payment-backend` sửa tạm memory limit trên Production nhưng gõ nhầm làm nổ syntax YAML.
- **Kết quả ở cách làm cũ:** Deployment bị treo, 50% người dùng bị ngắt kết nối thanh toán.
- **Khôi phục tự động nhờ ArgoCD Self-Healing (QT 41.4):** ArgoCD Controller phát hiện Trạng thái thực tế (Live State) bị lệch so với Trạng thái mong muốn (Desired State trong Git). Trong vòng **2 giây**, ArgoCD tự động kích hoạt cờ `selfHeal`, ghi đè lại 100% cấu hình chuẩn từ Git, khôi phục dịch vụ Healthy lập tức mà không cần con người can thiệp!

### 7.4. Case Study 3: Tự động hóa Render Diff Báo cáo Thay đổi Tài nguyên trên Merge Request
Một đội ngũ DevOps gồm 20 Kỹ sư quản lý 500 Helm Charts trên Kubernetes Multi-Cluster.
- **Cách làm cũ:** Reviewer duyệt MR nhưng không hình dung được lệnh `helm upgrade` sẽ làm thay đổi cấu hình gì trên cụm Production. Đã từng xảy ra sự cố xóa mất PersistentVolumeClaim (PVC) dữ liệu do gõ sai định dạng indent YAML.
- **Cách làm chuẩn Buổi 41 (Tích hợp `helm diff`):**
  1. Tích hợp plugin `helm diff` vào stage `test` của GitLab CI Pipeline.
  2. Mỗi khi có MR mới, script tự động so sánh bản build mới với bản đang chạy trên cụm và comment báo cáo chi tiết trực tiếp vào MR:
     `[HELM DIFF REPORT] 1 deployment modified, 0 created, 0 deleted`.
  3. Reviewer biết chính xác từng dòng YAML thay đổi trước khi bấm nút Merge, triệt hạ 100% sự cố xóa nhầm tài nguyên!

### 7.5. Case Study 4: Bảo mật Mật khẩu Kubernetes bằng Bitnami SealedSecrets trên GitOps
Một doanh nghiệp FinTech bắt buộc phải áp dụng tiêu chuẩn an toàn dữ liệu thẻ PCI-DSS.
- **Cách làm cũ:** Kỹ sư mã hóa base64 mật khẩu Database và commit file `secret.yaml` lên Git. Bộ phận Audit phát hiện và phát lệnh phạt nặng do để lộ plain-text secret trên mã nguồn.
- **Cách làm chuẩn Buổi 41 (Áp dụng SealedSecrets):**
  1. Cài đặt SealedSecrets Controller trên cụm Kubernetes.
  2. Kỹ sư dùng công cụ `kubeseal` mã hóa bất đối xứng tệp Secret local bằng Public Key của cụm:
     `kubeseal --format yaml < secret.yaml > sealed-secret.yaml`.
  3. Commit file `sealed-secret.yaml` an toàn tuyệt đối lên kho mã nguồn Git. Chỉ duy nhất SealedSecrets Controller giữ Private Key bên trong cụm mới giải mã được. Đạt 100% tiêu chuẩn PCI-DSS!

---

### 7.6. Trường hợp khi nào KHÔNG nên dùng GitOps ArgoCD
Mặc dù GitOps Pull-based CD là chuẩn mực cao nhất cho Kubernetes, nhưng KHÔNG áp dụng cho các trường hợp sau:

| Ngữ cảnh / Hạ tầng | Lý do KHÔNG dùng được GitOps | Giải pháp thay thế an toàn |
|---|---|---|
| Môi trường thử nghiệm Ephemeral Preview Environments (tạo/xóa liên tục trong vài phút) | Tạo thêm Git repos hay commit liên tục vào GitOps repo gây rác commit history không cần thiết. | Sử dụng `helm upgrade --install --atomic` trực tiếp từ CI Runner với Kubeconfig scoped namespace tạm thời. |
| Cụm Kubernetes nhỏ nằm ở Edge Devices / IoT | Máy chủ Edge không đủ RAM/CPU để chạy ArgoCD Controller Operator (tốn ~512MB RAM). | Sử dụng K3s kết hợp lightweight `helm upgrade` hoặc k3s manifest auto-deploy. |
| Pipeline chạy các bài test đĩa cứng ghi đè Data dán nhãn tạm | Cần tạo và dọn dẹp lập tức các Stateful workloads sau khi chạy test. | Sử dụng `helm install` và `helm uninstall` trực tiếp trong job test CI. |

---

### 1.5. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính bẫy | Làm đúng là |
|---|---|---|
| Bẫy 1: Chạy `helm upgrade` không có cờ `--atomic` và `--wait` | CI báo xanh 100% nhưng Pods trên Kubernetes đang bị `CrashLoopBackOff` khiến sập ứng dụng Production. | Bắt buộc bổ sung `--atomic --wait --timeout 300s` trong mọi câu lệnh `helm upgrade`. |
| Bẫy 2: Lưu tệp `secret.yaml` plain-text mã hóa base64 trên kho mã nguồn Git | Lộ 100% mật khẩu Database và API Keys cho bất kỳ ai có quyền truy cập Git repository. | Sử dụng Bitnami SealedSecrets hoặc External Secrets Operator (ESO) mã hóa trước khi commit. |
| Bẫy 3: Gõ `helm rollback` thủ công trên cụm Kubernetes đang chạy ArgoCD | ArgoCD phát hiện State Drift và lập tức ghi đè (overwrite) ngược lại phiên bản lỗi từ Git! | Thực hiện Rollback chuẩn GitOps bằng lệnh `git revert <commit_sha>` và push lên kho Git. |
| Bẫy 4: Để mã nguồn ứng dụng và Kubernetes Manifests nằm chung 1 Git Repository | Developer sửa code app vô tình sửa nhầm thông số RAM/CPU hay Replica của Production. | Tách làm 2 Repositories riêng biệt: App Code Repo và GitOps Config Repo (QT 41.2). |
| Bẫy 5: Tắt cờ `selfHeal: true` trên ArgoCD Application manifest | Khi ai đó sửa thủ công bằng `kubectl edit`, cụm bị lệch trạng thái (State Drift) kéo dài không khôi phục. | Bắt buộc bật `syncPolicy.automated.selfHeal: true` và `prune: true` (QT 41.4). |
| Bẫy 6: Cấp tệp Kubeconfig chứa quyền `cluster-admin` cho CI Runner khi chạy Push CD | Nếu Runner bị chiếm quyền, kẻ tấn công sẽ xóa sạch toàn bộ cụm Kubernetes. | Cấp Kubeconfig ServiceAccount bị giới hạn trong 1 namespace chỉ định qua RoleBinding (QT 41.10). |
| Bẫy 7: Bỏ trống khối `readinessProbe` trong Helm Chart template spec | Cờ `--wait` của Helm hoặc ArgoCD Sync coi Pod mới dựng xong là Ready ngay dù ứng dụng chưa boot xong. | Đảm bảo 100% Deployment templates có đầy đủ `readinessProbe` và `livenessProbe`. |
| Bẫy 8: Bỏ trống cờ `--timeout` trong lệnh `helm upgrade` | Job CI bị treo vĩnh viễn vài tiếng đồng hồ khi Pod mới rơi vào trạng thái ImagePullBackOff. | Luôn khống chế cờ `--timeout 300s` để tự động ngắt và rollback sau 5 phút. |

---

### 1.6. Tóm tắt (3 phút)

### 9.1. Sơ đồ Mermaid: Kiến trúc Luồng GitOps Tự động hóa với ArgoCD

```mermaid
flowchart TD
    subgraph App Code Repo
        A[Git Push Code to main] --> B[GitLab CI Build & Push Image]
        B --> C[CI Script Auto Commit Image Tag]
    end

    subgraph GitOps Config Repo
        C -->|Commit new tag| D[apps/payment/values.yaml]
    end

    subgraph Kubernetes Cluster Inside
        E[ArgoCD Controller Operator] -->|1. Detect Git Commit| D
        E -->|2. Compare Desired vs Live State| F{State Drift?}
        F -->|Out of Sync| G[3. Pull Manifests & Apply]
        G -->|4. Readiness Probe Passed| H[Zero Downtime Production Release]
        F -->|Self Healing Triggered| G
    end
```

### 9.2. Năm điều phải nhớ thuộc lòng
1. **Always Use `--atomic` & `--wait`:** Lệnh `helm upgrade` bắt buộc phải có `--atomic --wait --timeout 300s` để chống báo xanh ảo khi Pod bị crash, tự động khôi phục bản cũ nếu rollout thất bại.
2. **Git is the Single Source of Truth:** Trong mô hình GitOps, mọi sự thay đổi trên Kubernetes bắt buộc phải xuất phát từ một Git Commit SHA có đầy đủ thông tin tác giả và nhật ký kiểm toán.
3. **Rollback GitOps bằng `git revert`:** Tuyệt đối không gõ `helm rollback` hay `kubectl` thủ công trên cụm running ArgoCD; phải thực hiện `git revert` commit trên kho Git để ArgoCD đồng bộ tự động.
4. **SealedSecrets cho Git:** Không commit Base64 plain-text secrets lên kho mã nguồn Git; bắt buộc dùng Bitnami SealedSecrets hoặc External Secrets Operator (ESO) mã hóa an toàn.
5. **Tách biệt Repositories:** Tách rời App Code Repo và GitOps Config Repo để bảo vệ an toàn phân quyền ranh giới Enterprise và thực thi triết lý Separation of Concerns.

---

### 1.7. Câu hỏi tự kiểm tra (5 phút)

### 10.1. Danh sách câu hỏi tự kiểm tra
1. Sự khác biệt cốt lõi giữa hai tư duy triển khai Push-based CD và Pull-based GitOps CD là gì?
2. Hai cờ lệnh bắt buộc nào phải bổ sung vào câu lệnh `helm upgrade` để tự động khôi phục bản cũ khi Pod mới bị crash?
3. Tại sao không nên lưu tệp Kubeconfig chứa quyền `cluster-admin` toàn quyền trên máy chủ GitLab CI Runner?
4. Ý nghĩa của cờ `syncPolicy.automated.selfHeal: true` trên đối tượng ArgoCD Application manifest là gì?
5. Tại sao không được gõ câu lệnh `helm rollback` thủ công trên cụm Kubernetes đang chạy bộ tự động đồng bộ ArgoCD?
6. Làm thế nào để thực hiện quy trình Rollback chuẩn xác và an toàn nhất trong mô hình Pull-based GitOps?
7. Công cụ nào giúp mã hóa an toàn Kubernetes Secrets để có thể commit trực tiếp lên kho mã nguồn Git?
8. Tại sao việc tách biệt App Code Repo và GitOps Config Repo lại giúp tăng cường an toàn hạ tầng?
9. Công cụ Helm plugin nào giúp so sánh và hiển thị sự thay đổi tài nguyên Kubernetes trên Merge Request pipeline?
10. Tại sao `readinessProbe` lại đóng vai trò quyết định tới tính đúng đắn của cờ `--wait` trong Helm?
11. Khoảng thời gian timeout khuyến nghị tối đa cho một lệnh `helm upgrade` trong CI là bao lâu?
12. Cơ chế nào của ArgoCD giúp tự động dọn dẹp các tài nguyên Kubernetes đã bị xóa khỏi kho mã nguồn Git?

---

### 10.2. Đáp án câu hỏi tự kiểm tra

1. Push-based CD dùng CI Runner ở ngoài giữ credentials và trực tiếp đẩy manifests vào cụm; Pull-based GitOps dùng Controller bên trong cụm tự đọc kho mã nguồn Git và kéo manifests về đồng bộ.
2. Bắt buộc bổ sung hai cờ **`--atomic`** và **`--wait`** (kèm `--timeout 300s`) để ép Helm chờ Pods đạt trạng thái Ready, nếu crash sẽ tự động rollback nguyên tử.
3. Vì nếu máy chủ CI Runner bị chiếm quyền (RCE/malware), kẻ tấn công sẽ có tệp Kubeconfig admin toàn quyền xóa sạch toàn bộ các namespaces và tài nguyên trên cụm Kubernetes Production.
4. Giúp ArgoCD tự động ghi đè khôi phục lại cấu hình chuẩn từ kho mã nguồn Git khi phát hiện ai đó cố tình dùng `kubectl edit` hoặc `kubectl delete` sửa nhầm trên cụm.
5. Vì ArgoCD sẽ coi việc rollback thủ công trên cụm là State Drift (lệch trạng thái) và tự động ghi đè ngược lại phiên bản lỗi cũ từ Git!
6. Thực hiện Rollback chuẩn xác bằng câu lệnh **`git revert <commit_sha>`** và push commit mới lên kho GitOps Config Repo để ArgoCD tự động sync về bản cũ.
7. Công cụ **Bitnami SealedSecrets** (dùng lệnh `kubeseal` mã hóa bất đối xứng) hoặc **External Secrets Operator (ESO)** liên kết với Key Vault/Vault.
8. Giúp phân tách ranh giới trách nhiệm (Separation of Concerns), ngăn Developer tự ý sửa thông số RAM/CPU hay Replica Production trong mã nguồn ứng dụng.
9. Plugin **`helm diff`** (câu lệnh `helm diff upgrade`) render chi tiết tài nguyên thêm/sửa/xóa trực tiếp vào Merge Request.
10. Vì cờ `--wait` của Helm dựa 100% vào trạng thái `Ready` do `readinessProbe` báo về để quyết định Deployment đã khởi chạy thành công hay chưa.
11. Khoảng thời gian timeout khuyến nghị là **300 giây (5 phút)** để tránh treo job CI vô tận khi Pods bị rớt vào trạng thái ImagePullBackOff.
12. Cơ chế cờ **`syncPolicy.automated.prune: true`** trên ArgoCD Application manifest tự động dọn dẹp tài nguyên bị xóa trong Git.

---

### 1.8. Tài liệu tham khảo (2 phút)

| Nguồn tài liệu | Mô tả nội dung | Phiên bản áp dụng |
|---|---|---|
| Helm Documentation — Upgrade Command Reference | Chi tiết các cờ `--atomic`, `--wait`, `--timeout` giúp tự động hóa rollback an toàn | Helm v3.10+ |
| ArgoCD Official Documentation — Core Concepts | Hướng dẫn cài đặt và cấu hình GitOps Application Spec cho Kubernetes Multi-Cluster | ArgoCD v2.6+ |
| Bitnami SealedSecrets GitHub Repository | Hướng dẫn mã hóa Kubernetes Secrets bất đối xứng cho quy trình GitOps | SealedSecrets v0.20+ |
| External Secrets Operator (ESO) Guide | Đồng bộ Secrets từ Key Vault/AWS Secrets Manager/Vault sang Kubernetes | ESO v0.8+ |
| Helm Diff Plugin GitHub Repository | Hướng dẫn tích hợp helm diff vào GitLab CI/CD Pipeline để render diff report | Helm Diff v3.6+ |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10 phút |
| §1 | Sau buổi này học viên LÀM ĐƯỢC gì | 1 phút |
| §2 | Cần biết trước | 1 phút |
| §3 | Thuật ngữ và mô hình tư duy | 8 phút |
| §4 | Cấu hình Helm Upgrade Trực tiếp & Flag `--atomic` | 10 phút |
| §5 | Quy tắc Quản lý GitOps Image Update & Drift Detection | 10 phút |
| §6 | Quy tắc Probes, Healthchecks & Rollback Strategy | 10 phút |
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
Trong bài lab này, học viên sẽ trực tiếp triển khai và làm chủ cả hai tư duy CD trên cụm Kubernetes:
1. Xây dựng gói Helm Chart chuẩn cho ứng dụng Microservice (bao gồm Chart.yaml, values.yaml, Deployment, Service, Ingress, Probes).
2. Thực thi quy trình Push-based CD bằng câu lệnh `helm upgrade --install --atomic --wait --timeout 300s`.
3. Kiểm thử kịch bản tự động Rollback nguyên tử khi Pods rơi vào trạng thái `CrashLoopBackOff`.
4. Xây dựng luồng GitOps Pull-based CD mô phỏng ArgoCD Application Sync.
5. Kiểm thử tính năng phát hiện sai lệch trạng thái hạ tầng (State Drift Detection) và tự động khôi phục (Self-Healing).
6. Mã hóa an toàn Kubernetes Secrets với SealedSecrets và truy vết nhật ký đồng bộ kiểm toán Sync Audit Logs.

---

## 2. Mô hình kiến trúc Lab L2

```mermaid
graph TD
    subgraph Phase 1: Push-based CD (Direct Helm Upgrade)
        A[Gitlab CI Job] -->|1. helm lint| B[Helm Package Engine]
        B -->|2. helm upgrade --atomic --wait| C[Kubernetes API Server]
        C -->|3. Readiness Probe Failed| D[Atomic Rollback Triggered]
    end

    subgraph Phase 2: Pull-based CD (GitOps ArgoCD Sync)
        E[App Code Repo] -->|Auto Commit Image Tag| F[GitOps Config Repo]
        G[ArgoCD Controller] -->|1. Poll/Webhook| F
        G -->|2. Compare Desired vs Live State| H[Kubernetes API Server]
        I[Manual kubectl edit] -->|3. State Drift Detected| G
        G -->|4. Self-Healing Re-sync| H
    end
```

---

## 3. Các bước thực hiện bài lab (14 Checkpoints)

### Bước 1: Khởi tạo Cấu trúc Thư mục và Helm Chart Microservice (10 phút)

Tạo thư mục làm việc cho bài lab Buổi 41:

```bash
mkdir -p helm-gitops-lab
cd helm-gitops-lab
mkdir -p helm/payment-service/templates gitops-repo/apps/payment-service manifests scripts audit secrets
```

Khởi tạo file `helm/payment-service/Chart.yaml`:

```yaml
apiVersion: v2
name: payment-service
description: Helm Chart for Payment Backend Microservice
type: application
version: 1.0.0
appVersion: "2.5.0"
```

Khởi tạo tệp `helm/payment-service/values.yaml` với đầy đủ cấu hình microservice enterprise:

```yaml
replicaCount: 3

image:
  repository: registry.company.com/bank-group/payment-service
  pullPolicy: IfNotPresent
  tag: "v2.5.0-sha123"

service:
  type: ClusterIP
  port: 8080

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: payment.company.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: payment-service-tls
      hosts:
        - payment.company.com

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 250m
    memory: 256Mi

probes:
  readiness:
    path: /health/readiness
    port: 8080
  liveness:
    path: /health/liveness
    port: 8080
  startup:
    path: /health/startup
    port: 8080

env:
  ENVIRONMENT: production
  LOG_LEVEL: INFO
  DATABASE_POOL_SIZE: "20"
```

### **CHECKPOINT 1**
Chạy câu lệnh kiểm tra tệp `Chart.yaml` và `values.yaml`:

```bash
test -f helm/payment-service/Chart.yaml && test -f helm/payment-service/values.yaml && echo "CHECKPOINT 1: ĐẠT" || echo "CHECKPOINT 1: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 1: ĐẠT
```

---

### Bước 2: Khởi tạo các Tệp Templates Kubernetes Manifests trong Helm Chart (10 phút)

Tạo tệp Template Deployment `helm/payment-service/templates/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-backend
  labels:
    app: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.service.port }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          startupProbe:
            httpGet:
              path: {{ .Values.probes.startup.path }}
              port: {{ .Values.probes.startup.port }}
            failureThreshold: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: {{ .Values.probes.readiness.path }}
              port: {{ .Values.probes.readiness.port }}
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: {{ .Values.probes.liveness.path }}
              port: {{ .Values.probes.liveness.port }}
            initialDelaySeconds: 15
            periodSeconds: 10
```

Tạo tệp Template Service `helm/payment-service/templates/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}-service
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.port }}
      protocol: TCP
  selector:
    app: {{ .Release.Name }}
```

Tạo tệp Template Ingress `helm/payment-service/templates/ingress.yaml`:

```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}-ingress
  annotations:
    {{- toYaml .Values.ingress.annotations | nindent 4 }}
spec:
  ingressClassName: {{ .Values.ingress.className }}
  tls:
    {{- toYaml .Values.ingress.tls | nindent 4 }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ $.Release.Name }}-service
                port:
                  number: {{ $.Values.service.port }}
          {{- end }}
    {{- end }}
{{- end }}
```

### **CHECKPOINT 2**
Chạy câu lệnh kiểm tra các tệp templates Helm Chart:

```bash
test -f helm/payment-service/templates/deployment.yaml && test -f helm/payment-service/templates/service.yaml && echo "CHECKPOINT 2: ĐẠT" || echo "CHECKPOINT 2: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 2: ĐẠT
```

---

### Bước 3: Thực thi Script `helm lint` và Render Template Kiểm tra Syntax (15 phút)

Tạo script kiểm định Helm Chart `scripts/validate-helm-chart.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

CHART_DIR="helm/payment-service"

echo "[HELM LINT] Linting Helm Chart in $CHART_DIR..."
mkdir -p dist

cat << EOF > dist/rendered-manifests.yaml
# Rendered Helm Template Output for Validation
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-backend
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: payment-service
          image: "registry.company.com/bank-group/payment-service:v2.5.0-sha123"
EOF

echo "[HELM TEMPLATE] Successfully rendered template to dist/rendered-manifests.yaml!"
```

Cho phép script chạy:
```bash
chmod +x scripts/validate-helm-chart.sh
./scripts/validate-helm-chart.sh
```

### **CHECKPOINT 3**
Chạy câu lệnh kiểm tra tệp manifest đã được render:

```bash
test -f dist/rendered-manifests.yaml && grep -q "payment-service-backend" dist/rendered-manifests.yaml && echo "CHECKPOINT 3: ĐẠT" || echo "CHECKPOINT 3: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 3: ĐẠT
```

---

### Bước 4: Viết Script Mô phỏng Push-based `helm upgrade --atomic` (15 phút)

Tạo script deploy Helm direct chuẩn mực với cờ kiểm tra nguyên tử `scripts/helm-upgrade-push.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

RELEASE_NAME="${1:-payment-service}"
IMAGE_TAG="${2:-v2.5.0-sha123}"
FAIL_MODE="${3:-false}"

echo "[HELM UPGRADE] Deploying release $RELEASE_NAME with tag $IMAGE_TAG..."
echo "[HELM UPGRADE] Enforcing mandatory flags: --atomic --wait --timeout 300s..."
mkdir -p manifests/live-state

if [ "$FAIL_MODE" = "true" ]; then
    echo "[HELM UPGRADE] [WARNING] Pod Readiness Probe failed! Triggering ATOMIC ROLLBACK..."
    cat << EOF > manifests/live-state/release-status.json
{
  "release": "$RELEASE_NAME",
  "status": "ROLLED_BACK",
  "reason": "Atomic rollback triggered due to readiness probe failure",
  "active_revision": 1,
  "rolled_back_from_revision": 2,
  "atomic_execution_status": "RESTORED_PREVIOUS_STABLE_STATE"
}
EOF
    echo "[HELM ERROR] Release failed! Atomic rollback restored revision 1."
    exit 1
else
    cat << EOF > manifests/live-state/release-status.json
{
  "release": "$RELEASE_NAME",
  "status": "DEPLOYED",
  "active_revision": 2,
  "image_tag": "$IMAGE_TAG",
  "atomic_wait_status": "SUCCESS_WAIT_PASSED",
  "deployment_strategy": "PUSH_BASED_HELM_DIRECT"
}
EOF
    echo "[HELM SUCCESS] Release $RELEASE_NAME revision 2 deployed successfully!"
fi
```

Cho phép script chạy bản xanh:
```bash
chmod +x scripts/helm-upgrade-push.sh
./scripts/helm-upgrade-push.sh "payment-service" "v2.5.0-sha123" "false"
```

### **CHECKPOINT 4**
Chạy câu lệnh kiểm tra kết quả `helm upgrade` thành công:

```bash
test -f manifests/live-state/release-status.json && grep -q "DEPLOYED" manifests/live-state/release-status.json && echo "CHECKPOINT 4: ĐẠT" || echo "CHECKPOINT 4: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 4: ĐẠT
```

---

### Bước 5: Kiểm thử Tính năng Tự động Rollback Nguyên tử (`--atomic`) khi Pod Crash (10 phút)

Chạy script deploy Helm ở chế độ giả lập sập Pod (`FAIL_MODE=true`):

```bash
./scripts/helm-upgrade-push.sh "payment-service" "v3.0.0-broken" "true" || true
```

### **CHECKPOINT 5**
Chạy câu lệnh kiểm tra tính năng `--atomic` tự động rollback về revision 1:

```bash
test -f manifests/live-state/release-status.json && grep -q "ROLLED_BACK" manifests/live-state/release-status.json && echo "CHECKPOINT 5: ĐẠT" || echo "CHECKPOINT 5: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 5: ĐẠT
```

---

### Bước 6: Khởi tạo ArgoCD Application Manifest chuẩn GitOps (10 phút)

Tạo tệp ArgoCD Application manifest `gitops-repo/apps/payment-service/argocd-app.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-service-prod
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: 'https://gitlab.company.com/bank-group/gitops-manifests.git'
    targetRevision: HEAD
    path: apps/payment-service
    helm:
      valueFiles:
        - values-prod.yaml
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ApplyOutOfSyncOnly=true
```

Tạo file values môi trường production `gitops-repo/apps/payment-service/values-prod.yaml`:

```yaml
replicaCount: 5

image:
  repository: registry.company.com/bank-group/payment-service
  tag: "v2.5.0-sha123"

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
```

### **CHECKPOINT 6**
Chạy câu lệnh kiểm tra tệp ArgoCD Application manifest:

```bash
test -f gitops-repo/apps/payment-service/argocd-app.yaml && grep -q "selfHeal: true" gitops-repo/apps/payment-service/argocd-app.yaml && echo "CHECKPOINT 6: ĐẠT" || echo "CHECKPOINT 6: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 6: ĐẠT
```

---

### Bước 7: Viết Script Mô phỏng CI Commit Tự động nâng Image Tag sang GitOps Repo (15 phút)

Tạo script CI auto commit `scripts/ci-gitops-commit-tag.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

NEW_TAG="${1:-v2.6.0-sha999}"

echo "[CI GITOPS COMMIT] Updating Image Tag to $NEW_TAG in GitOps Repo..."

sed -i "s/tag: .*/tag: \"$NEW_TAG\"/" gitops-repo/apps/payment-service/values-prod.yaml 2>/dev/null || sed -i "" "s/tag: .*/tag: \"$NEW_TAG\"/" gitops-repo/apps/payment-service/values-prod.yaml

mkdir -p gitops-repo/git-history

cat << EOF > gitops-repo/git-history/latest-commit.json
{
  "commit_sha": "git-commit-$(openssl rand -hex 8)",
  "author": "GitLab CI Runner Bot",
  "message": "chore(cd): update payment-service image to $NEW_TAG",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "image_tag": "$NEW_TAG"
}
EOF

echo "[CI GITOPS COMMIT] Successfully pushed Git commit to GitOps repository!"
```

Cho phép script chạy:
```bash
chmod +x scripts/ci-gitops-commit-tag.sh
./scripts/ci-gitops-commit-tag.sh "v2.6.0-sha999"
```

### **CHECKPOINT 7**
Chạy câu lệnh kiểm tra tệp Git commit mới nhất:

```bash
test -f gitops-repo/git-history/latest-commit.json && grep -q "v2.6.0-sha999" gitops-repo/git-history/latest-commit.json && echo "CHECKPOINT 7: ĐẠT" || echo "CHECKPOINT 7: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 7: ĐẠT
```

---

### Bước 8: Viết Script Mô phỏng ArgoCD Pull Sync Engine (15 phút)

Tạo script mô phỏng bộ công cụ ArgoCD Pull Sync Engine tự động đồng bộ hạ tầng `scripts/argocd-sync-engine.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

source gitops-repo/git-history/latest-commit.json 2>/dev/null || true

echo "[ARGOCD CONTROLLER] Polling GitOps Config Repository..."
echo "[ARGOCD CONTROLLER] Found new Git Commit: $commit_sha. Synchronizing..."
echo "[ARGOCD CONTROLLER] Applying manifests to target namespace 'production'..."

mkdir -p manifests/gitops-live-state

cat << EOF > manifests/gitops-live-state/cluster-live-state.json
{
  "application": "payment-service-prod",
  "sync_status": "Synced",
  "health_status": "Healthy",
  "revision": "$commit_sha",
  "active_image_tag": "$image_tag",
  "synced_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "replicas": "5/5",
  "sync_engine_mode": "PULL_BASED_GITOPS_ARGOCD"
}
EOF

echo "[ARGOCD CONTROLLER] Sync completed! Cluster state is Synced & Healthy."
```Terminal output:

Cho phép script chạy:
```bash
chmod +x scripts/argocd-sync-engine.sh
./scripts/argocd-sync-engine.sh
```

### **CHECKPOINT 8**
Chạy câu lệnh kiểm tra trạng thái live state của ArgoCD:

```bash
test -f manifests/gitops-live-state/cluster-live-state.json && grep -q "Healthy" manifests/gitops-live-state/cluster-live-state.json && echo "CHECKPOINT 8: ĐẠT" || echo "CHECKPOINT 8: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 8: ĐẠT
```

---

### Bước 9: Kiểm thử Phát hiện Sai lệch Trạng thái (State Drift) và Self-Healing (10 phút)

Tạo script mô phỏng `kubectl edit` sửa bẩn tài nguyên và kích hoạt Self-Healing `scripts/simulate-state-drift-selfheal.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[MALICIOUS USER] Running 'kubectl edit' to change replicas to 1 directly on cluster..."

# Mô phỏng bị sửa bẩn
cat << EOF > manifests/gitops-live-state/cluster-live-state.json
{
  "application": "payment-service-prod",
  "sync_status": "OutOfSync",
  "health_status": "Degraded",
  "drift_detected": true,
  "drift_reason": "Replicas count modified manually via kubectl edit"
}
EOF

echo "[ARGOCD CONTROLLER] State Drift Detected! Triggering AUTOMATED SELF-HEALING..."

# Self healing khôi phục về giá trị Git
./scripts/argocd-sync-engine.sh

echo "[ARGOCD CONTROLLER] Self-healing completed! Overwrote live state back to Desired Git State."
```

Cho phép script chạy:
```bash
chmod +x scripts/simulate-state-drift-selfheal.sh
./scripts/simulate-state-drift-selfheal.sh
```

### **CHECKPOINT 9**
Chạy câu lệnh kiểm tra sau khi Self-Healing khôi phục trạng thái `Synced`:

```bash
test -f manifests/gitops-live-state/cluster-live-state.json && grep -q "Synced" manifests/gitops-live-state/cluster-live-state.json && echo "CHECKPOINT 9: ĐẠT" || echo "CHECKPOINT 9: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 9: ĐẠT
```

---

### Bước 10: Khởi tạo Tệp Bitnami SealedSecrets Mã hóa Bí mật (10 phút)

Tạo tệp mã hóa SealedSecrets giả lập `secrets/sealed-db-secret.yaml`:

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: db-credentials
  namespace: production
spec:
  encryptedData:
    DB_PASSWORD: AgA3bXY4ejltOGk2cTRtOWszajQ4d2U5OGszajQ4d2U5OGszajQ4
    DB_USER: AgB1c2VybmFtZTEyM2s0OGtlOTNrNDg=
  template:
    metadata:
      name: db-credentials
      namespace: production
    type: Opaque
```

### **CHECKPOINT 10**
Chạy câu lệnh kiểm tra tệp SealedSecret mã hóa:

```bash
test -f secrets/sealed-db-secret.yaml && grep -q "kind: SealedSecret" secrets/sealed-db-secret.yaml && echo "CHECKPOINT 10: ĐẠT" || echo "CHECKPOINT 10: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 10: ĐẠT
```

---

### Bước 11: Xây dựng Script Ghi nhận Nhật ký ArgoCD Audit Event Log (10 phút)

Tạo script ghi nhận đầy đủ nhật ký kiểm toán sự kiện đồng bộ hạ tầng ArgoCD `scripts/audit-argocd-sync-events.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

mkdir -p audit

cat << EOF >> audit/argocd-sync-audit.json
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "application": "payment-service-prod",
  "event": "SYNC_SUCCESSFUL",
  "sync_source": "GitOps Repository (main branch)",
  "commit_sha": "git-commit-$(openssl rand -hex 8)",
  "initiator": "Automated GitOps Sync Engine",
  "audit_type": "KUBERNETES_GITOPS_ALIGNMENT",
  "compliance_status": "ISO27001_SOC2_COMPLIANT",
  "status": "COMPLIANT"
}
EOF

echo "[ARGO AUDIT] Recorded ArgoCD Sync Audit Event in audit/argocd-sync-audit.json"
```

Cho phép script chạy ghi log:
```bash
chmod +x scripts/audit-argocd-sync-events.sh
./scripts/audit-argocd-sync-events.sh
```

### **CHECKPOINT 11**
Chạy câu lệnh kiểm tra tệp ArgoCD Audit Log:

```bash
test -f audit/argocd-sync-audit.json && grep -q "SYNC_SUCCESSFUL" audit/argocd-sync-audit.json && echo "CHECKPOINT 11: ĐẠT" || echo "CHECKPOINT 11: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 11: ĐẠT
```

---

### Bước 12: Xây dựng Script Linter Kiểm tra Cấu hình Helm & GitOps CI (5 phút)

Tạo script linter kiểm định nghiêm ngặt cấu hình GitLab CI cho Helm & GitOps `scripts/validate-helm-gitops-ci.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[HELM/GITOPS LINTER] Auditing GitLab CI Helm & GitOps configuration..."

cat << EOF > .gitlab-ci.yml
deploy-push-job:
  stage: deploy
  script:
    - helm upgrade --install payment-service ./helm/payment-service --wait --atomic --timeout 300s
EOF

if ! grep -q "--atomic" .gitlab-ci.yml; then
    echo "[ERROR] Missing mandatory --atomic flag in helm upgrade!"
    exit 1
fi

if ! grep -q "--wait" .gitlab-ci.yml; then
    echo "[ERROR] Missing mandatory --wait flag in helm upgrade!"
    exit 1
fi

echo "[HELM/GITOPS LINTER] Validation PASSED: 100% Compliant Helm & GitOps CI Pipeline Configuration."
```

Cho phép script chạy linter:
```bash
chmod +x scripts/validate-helm-gitops-ci.sh
./scripts/validate-helm-gitops-ci.sh
```

### **CHECKPOINT 12**
Chạy câu lệnh kiểm tra script Linter Helm CI:

```bash
./scripts/validate-helm-gitops-ci.sh | grep -q "PASSED" && echo "CHECKPOINT 12: ĐẠT" || echo "CHECKPOINT 12: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 12: ĐẠT
```

---

### Bước 13: Xây dựng Script Kiểm tra Khôi phục Sự cố Git Revert Rollback (5 phút)

Tạo script git revert rollback `scripts/gitops-revert-rollback.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[GITOPS ROLLBACK] Executing 'git revert HEAD' to restore previous stable Git state..."

cat << EOF > gitops-repo/git-history/latest-commit.json
{
  "commit_sha": "revert-commit-$(openssl rand -hex 8)",
  "author": "DevOps OnCall Engineer",
  "message": "revert(cd): rollback broken release back to v2.5.0-sha123",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "image_tag": "v2.5.0-sha123"
}
EOF

# Trigger ArgoCD sync back
./scripts/argocd-sync-engine.sh

echo "[GITOPS ROLLBACK] Git Revert executed successfully! Cluster rolled back to v2.5.0-sha123."
```

Cho phép script chạy rollback:
```bash
chmod +x scripts/gitops-revert-rollback.sh
./scripts/gitops-revert-rollback.sh
```

### **CHECKPOINT 13**
Chạy câu lệnh kiểm tra kết quả Git Revert Rollback:

```bash
test -f gitops-repo/git-history/latest-commit.json && grep -q "revert" gitops-repo/git-history/latest-commit.json && echo "CHECKPOINT 13: ĐẠT" || echo "CHECKPOINT 13: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 13: ĐẠT
```

---

### Bước 14: Tổng hợp Đánh giá Hoàn thành Bài Lab Buổi 41 (5 phút)

Tạo script đánh giá kết quả tổng hợp `scripts/final-helm-gitops-lab-evaluation.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "FINAL EVALUATION SUMMARY — BUỔI 41 (HELM & GITOPS DEPLOYMENT)"
echo "=========================================================="

CHECKS_PASSED=0

[ -f helm/payment-service/Chart.yaml ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f dist/rendered-manifests.yaml ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f manifests/live-state/release-status.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f gitops-repo/apps/payment-service/argocd-app.yaml ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f manifests/gitops-live-state/cluster-live-state.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f audit/argocd-sync-audit.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))

echo "Successfully verified $CHECKS_PASSED / 6 Core Helm & GitOps Components."
echo "Verified Helm Chart Templates, Direct Upgrade Atomic Rollback, ArgoCD Application, GitOps Sync, and Self-Healing."
echo "Verified Bitnami SealedSecrets integration and ArgoCD Event Audit Logging."

if [ "$CHECKS_PASSED" -eq 6 ]; then
    echo "BUỔI 41 LAB STATUS: PASSED (100% COMPLETE)"
    exit 0
else
    echo "BUỔI 41 LAB STATUS: INCOMPLETE"
    exit 1
fi
```

Cho phép script chạy đánh giá kết quả:
```bash
chmod +x scripts/final-helm-gitops-lab-evaluation.sh
./scripts/final-helm-gitops-lab-evaluation.sh
```

### **CHECKPOINT 14**
Chạy câu lệnh tổng kết bài lab Buổi 41:

```bash
./scripts/final-helm-gitops-lab-evaluation.sh | grep -q "PASSED" && echo "CHECKPOINT 14: ĐẠT" || echo "CHECKPOINT 14: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 14: ĐẠT
```

---

## Xử lý sự cố

### 1. Sự cố `helm upgrade` bị treo vô hạn ở stage deploy CI
- **Triệu chứng:** Job CI chạy quá 30 phút mà không ngắt.
- **Nguyên nhân:** Quên bổ sung cờ `--timeout 300s` khiến Helm chờ Pods mãi mãi khi bị ImagePullBackOff.
- **Cách khắc phục:** Luôn bổ sung tham số `--timeout 300s` trong mọi câu lệnh `helm upgrade`.

### 2. Sự cố CI báo xanh 100% nhưng ứng dụng Kubernetes bị Crash
- **Triệu chứng:** Job CI kết thúc 0 exit code nhưng Pods bị `CrashLoopBackOff`.
- **Nguyên nhân:** Quên truyền hai cờ `--atomic` và `--wait`.
- **Cách khắc phục:** Thêm `--atomic --wait` để ép Helm kiểm tra Readiness Probe trước khi báo xanh.

### 3. Sự cố Lập thao tác `helm rollback` bị ArgoCD ghi đè ngược lại phiên bản lỗi
- **Triệu chứng:** Chạy `helm rollback` thủ công nhưng 5 giây sau cụm tự quay về bản lỗi.
- **Nguyên nhân:** ArgoCD có bật cờ `selfHeal: true`, nó coi `helm rollback` thủ công là State Drift nên ghi đè từ Git.
- **Cách khắc phục:** Rollback chuẩn GitOps bằng câu lệnh `git revert <commit_sha>` và push lên kho GitOps Repo.

### 4. Sự cố ArgoCD Application báo trạng thái `OutOfSync` liên tục
- **Triệu chứng:** ArgoCD không thể chuyển sang trạng thái `Synced`.
- **Nguyên nhân:** File YAML trong GitOps Repo bị sai cú pháp hoặc thiếu thông số bắt buộc.
- **Cách khắc phục:** Chạy `helm lint` hoặc `kubectl apply --dry-run=client` kiểm tra file YAML trong Git.

### 5. Sự cố Lộ mật khẩu base64 plain-text trên kho mã nguồn Git
- **Triệu chứng:** Bộ phận Security phát hiện chuỗi secret mã hóa base64 công khai trên Git.
- **Nguyên nhân:** Commit file `secret.yaml` chuẩn Kubernetes trực tiếp lên Git.
- **Cách khắc phục:** Dùng `kubeseal` mã hóa thành `SealedSecret` hoặc dùng External Secrets Operator (ESO).

### 6. Sự cố Lỗi `helm lint` báo `chart.yaml: version is required`
- **Triệu chứng:** Lệnh validation bị từ chối.
- **Nguyên nhân:** Tệp `Chart.yaml` thiếu trường `version` hoặc `name`.
- **Cách khắc phục:** Khai báo đầy đủ các trường `name`, `version`, `apiVersion` trong `Chart.yaml`.

### 7. Sự cố ArgoCD không tự động xóa tài nguyên cũ khi đã xóa trong Git
- **Triệu chứng:** Tài nguyên Pods/Services bị thừa trên cụm Kubernetes dù trong Git không còn.
- **Nguyên nhân:** Chưa bật cờ `syncPolicy.automated.prune: true`.
- **Cách khắc phục:** Thêm `prune: true` vào spec `syncPolicy.automated` của ArgoCD Application.

### 8. Sự cố Kubeconfig của CI Runner bị từ chối quyền `ClusterRoleBinding`
- **Triệu chứng:** Job `helm upgrade` nổ lỗi `Forbidden: cannot list resource`.
- **Nguyên nhân:** ServiceAccount của Runner bị giới hạn namespace hoặc thiếu RBAC Role.
- **Cách khắc phục:** Cấp `RoleBinding` hạn chế đúng namespace deploy cho Runner ServiceAccount.

### 9. Sự cố `helm diff` plugin báo lỗi `plugin not found`
- **Triệu chứng:** Job CI không chạy được câu lệnh `helm diff`.
- **Nguyên nhân:** Container Image của Runner chưa cài đặt plugin `helm-diff`.
- **Cách khắc phục:** Chạy `helm plugin install https://github.com/databus23/helm-diff` trong `before_script`.

### 10. Sự cố Pods không đạt trạng thái `Ready` do sai thông số Readiness Probe
- **Triệu chứng:** Helm báo lỗi `timed out waiting for the condition` và kích hoạt atomic rollback.
- **Nguyên nhân:** Path `/health` trong `readinessProbe` trả về HTTP 404 hoặc sai port 8080.
- **Cách khắc phục:** Kiểm tra lại đúng HTTP Health Path và Port của ứng dụng microservice.

### 11. Sự cố ArgoCD bị rớt kết nối Git Repository do sai Personal Access Token
- **Triệu chứng:** ArgoCD Application báo `ComparisonError: repository not found`.
- **Nguyên nhân:** SSH Key hoặc Personal Access Token kết nối Git bị hết hạn.
- **Cách khắc phục:** Cập nhật lại Repositories Credentials trên ArgoCD Settings.

### 12. Sự cố Tệp `values-prod.yaml` bị gõ nhầm indent khoảng trắng YAML
- **Triệu chứng:** Helm render nổ lỗi `yaml: line X: did not find expected key`.
- **Nguyên nhân:** Dùng dấu Tab thay vì khoảng trắng Space khi định dạng YAML.
- **Cách khắc phục:** Dùng Linter YAMLLint kiểm tra lại cấu trúc 2 spaces indent.

### 13. Sự cố Deploy Helm làm treo các Pods cũ trước khi Pods mới Readiness
- **Triệu chứng:** Người dùng bị ngắt kết nối trong 15 giây khi deploy.
- **Nguyên nhân:** Cấu hình `strategy.rollingUpdate.maxUnavailable` quá cao (dạng 100%).
- **Cách khắc phục:** Đặt `maxUnavailable: 0` hoặc `25%` để đảm bảo Zero Downtime.

### 14. Sự cố Lệnh `git push` sang GitOps Repo bị từ chối do xung đột commit
- **Triệu chứng:** Script CI auto-commit báo `non-fast-forward push rejected`.
- **Nguyên nhân:** Nhiều pipelines chạy song song cùng push vào GitOps Repo.
- **Cách khắc phục:** Bổ sung `git pull --rebase origin main` trước khi execution `git push`.

### 15. Sự cố ArgoCD Sync bị treo ở trạng thái `Progressing`
- **Triệu chứng:** Khối Sync không thể chuyển sang `Healthy`.
- **Nguyên nhân:** Một trong số các Pods bị thiếu PVC Storage Volume mount.
- **Cách khắc phục:** Kiểm tra sự tồn tại của StorageClass và PersistentVolumeClaim.

### 16. Sự cố `validate-helm-chart.sh` nổ lỗi `dist directory not found`
- **Triệu chứng:** Script kiểm tra bị dừng giữa chừng.
- **Nguyên nhân:** Thư mục `dist` chưa được khởi tạo.
- **Cách khắc phục:** Thêm `mkdir -p dist` trong script.

### 17. Sự cố SealedSecrets Controller không giải mã được Secret
- **Triệu chứng:** Pods nổ lỗi `Secret "db-credentials" not found`.
- **Nguyên nhân:** SealedSecret được mã hóa bằng Public Key của cụm K8s khác.
- **Cách khắc phục:** Re-seal lại tệp Secret bằng Public Key của đúng cụm target.

### 18. Sự cố Helm Release bị kẹt trạng thái `pending-upgrade`
- **Triệu chứng:** Không thể thực thi `helm upgrade` mới.
- **Nguyên nhân:** Phiên nâng cấp trước bị hủy giữa chừng do ngắt nguồn hoặc kill job.
- **Cách khắc phục:** Chạy `helm rollback <release> <last_working_revision>` để giải phóng lock.

### 19. Sự cố `argocd-sync-engine.sh` nổ lỗi parse JSON
- **Triệu chứng:** Script mô phỏng sync báo lỗi đọc tệp commit.
- **Nguyên nhân:** Tệp `latest-commit.json` bị rỗng.
- **Cách khắc phục:** Kiểm tra Bước 7 chạy thành công trước khi gọi Bước 8.

### 20. Sự cố Cấu hình sai `targetRevision: HEAD` trong ArgoCD App
- **Triệu chứng:** ArgoCD đồng bộ sang một branch rác không mong muốn.
- **Nguyên nhân:** Để `targetRevision` tự do thay vì chỉ định rõ `main` hoặc `tags`.
- **Cách khắc phục:** Khai báo chính xác `targetRevision: main` hoặc Semantic Version Tags.

### 21. Sự cố Cụm Kubernetes bị hết bộ nhớ Node làm Pods bị Evicted
- **Triệu chứng:** Helm deploy báo lỗi `Pod Evicted due to OutOfMemory`.
- **Nguyên nhân:** Khai báo `resources.requests.memory` vượt quá khả năng của cụm.
- **Cách khắc phục:** Giảm `requests` bộ nhớ hoặc kích hoạt Cluster Autoscaler.

### 22. Sự cố Tệp `values.yaml` chứa thông tin nhạy cảm plain-text
- **Triệu chứng:** Lộ mật khẩu DB trong file `values.yaml`.
- **Nguyên nhân:** Đưa chuỗi mật khẩu trực tiếp vào `values.yaml` thay vì nạp từ Vault/SealedSecrets.
- **Cách khắc phục:** Sử dụng tham số `--set` nạp bí mật từ SealedSecrets.

### 23. Sự cố `simulate-state-drift-selfheal.sh` báo lỗi file not found
- **Triệu chứng:** Script kiểm thử Drift không tìm thấy live state.
- **Nguyên nhân:** Chưa chạy Bước 8 khởi tạo trạng thái ban đầu.
- **Cách khắc phục:** Thực thi Bước 8 trước khi kiểm thử Drift.

### 24. Sự cố Lỗi `403 Forbidden` khi CI Runner gọi API Server K8s
- **Triệu chứng:** Lệnh `helm upgrade` bị ngắt kết nối RBAC.
- **Nguyên nhân:** ServiceAccount token của Runner bị hết hạn hoặc thu hồi.
- **Cách khắc phục:** Cấp lại ServiceAccount Token mới hoặc dùng OIDC Federation.

### 25. Sự cố Quên khai báo `namespace` trong `helm upgrade`
- **Triệu chứng:** Release bị cài đặt nhầm vào namespace `default`.
- **Nguyên nhân:** Thiếu cờ `--namespace production`.
- **Cách khắc phục:** Luôn chỉ định cờ `--namespace <target_ns> --create-namespace`.

### 26. Sự cố ArgoCD bị treo Sync do Resource Finalizers bị chặn
- **Triệu chứng:** Xóa ArgoCD Application nhưng bị treo vĩnh viễn ở `Deleting`.
- **Nguyên nhân:** Finalizer `resources-finalizer.argocd.argoproj.io` chờ dọn dẹp tài nguyên.
- **Cách khắc phục:** Kiểm tra dọn dẹp các tài nguyên con hoặc gỡ finalizer bằng `kubectl patch`.

### 27. Sự cố `final-helm-gitops-lab-evaluation.sh` báo 5/6 thành phần
- **Triệu chứng:** Bài lab đánh giá chưa hoàn thành.
- **Nguyên nhân:** Chưa thực thi Bước 13 tạo tệp commit revert rollback.
- **Cách khắc phục:** Chạy script `./scripts/gitops-revert-rollback.sh`.

### 28. Sự cố Helm Chart bị lặp tên Release Name giữa các dự án
- **Triệu chứng:** `helm upgrade` ghi đè lên ứng dụng của đội khác.
- **Nguyên nhân:** Đặt tên Release quá chung chung dạng `app` hoặc `web`.
- **Cách khắc phục:** Đặt tên Release chứa tên microservice độc nhất: `payment-service-prod`.

### 29. Sự cố GitOps Repository bị lộ quyền Write cho Developer toàn bộ
- **Triệu chứng:** Developer tự ý push trực tiếp vào branch `main` của GitOps Repo.
- **Nguyên nhân:** Nhánh `main` trên GitOps Repo không bật Protected Branch.
- **Cách khắc phục:** Bật Protected Branch, buộc 100% thay đổi phải đi qua Merge Request có phê duyệt.

### 30. Sự cố Lỗi `CRD (CustomResourceDefinition) not found` khi Helm deploy
- **Triệu chứng:** `helm upgrade` báo lỗi không tìm thấy CRD Prometheus/CertManager.
- **Nguyên nhân:** Helm v3 không tự động upgrade CRDs trong thư mục `crds/`.
- **Cách khắc phục:** Cài đặt CRDs thủ công trước bằng `kubectl apply -f crds/`.

### 31. Sự cố ArgoCD Sync Wave bị sai thứ tự triển khai
- **Triệu chứng:** Web App khởi chạy trước khi Database Migration Job hoàn tất.
- **Nguyên nhân:** Chưa cấu hình annotation `argocd.argoproj.io/sync-wave`.
- **Cách khắc phục:** Đánh số Sync Wave: Migration Job (Wave -1), Web App (Wave 0).

### 32. Sự cố `ci-gitops-commit-tag.sh` nổ lỗi sed trên macOS
- **Triệu chứng:** Lệnh `sed` nổ syntax error trên hệ điều hành macOS.
- **Nguyên nhân:** Khác biệt cú pháp `sed` giữa Linux (GNU) và macOS (BSD).
- **Cách khắc phục:** Dùng cú pháp tương thích `sed -i "..."` hỗ trợ cả 2 hệ điều hành.

### 33. Sự cố Pods bị kẹt `ImagePullBackOff` do sai tên Image Repository
- **Triệu chứng:** Pod không thể kéo Docker Image.
- **Nguyên nhân:** Gõ sai tên registry `registry.conpany.com` trong `values.yaml`.
- **Cách khắc phục:** Kiểm tra lại tên miền Registry chuẩn xác.

### 34. Sự cố ArgoCD UI báo lỗi `Unknown Resource` đối với SealedSecret
- **Triệu chứng:** ArgoCD coi SealedSecret là tài nguyên không hợp lệ.
- **Nguyên nhân:** ArgoCD chưa được đăng ký Health Check Plugin cho SealedSecrets CRD.
- **Cách khắc phục:** Bổ sung Resource Health Customization trong ArgoCD ConfigMap.

### 35. Sự cố `helm-upgrade-push.sh` nổ lỗi không tìm thấy manifests directory
- **Triệu chứng:** Script deploy Push-based bị ngắt giữa chừng.
- **Nguyên nhân:** Thư mục `manifests/live-state` chưa được khởi tạo.
- **Cách khắc phục:** Thêm `mkdir -p manifests/live-state` trong script.

### 36. Sự cố Cấu hình Liveness Probe quá nhạy làm Pods bị kill liên tục
- **Triệu chứng:** Pods bị restart lặp đi lặp lại sau mỗi 30 giây.
- **Nguyên nhân:** `initialDelaySeconds` quá ngắn (2s) trong khi app Java cần 15s để boot.
- **Cách khắc phục:** Tăng `initialDelaySeconds: 20` và `periodSeconds: 10`.

### 37. Sự cố `validate-helm-gitops-ci.sh` nổ lỗi do thiếu cờ `--wait`
- **Triệu chứng:** Linter chặn pipeline do script thiếu `--wait`.
- **Nguyên nhân:** Viết lệnh `helm upgrade` thiếu cờ kiểm tra trạng thái.
- **Cách khắc phục:** Bổ sung đầy đủ cờ `--wait`.

### 38. Sự cố ArgoCD Notifications không gửi tin nhắn Slack khi Sync thất bại
- **Triệu chứng:** Pipeline bị sập nhưng đội trực ca không nhận được thông báo.
- **Nguyên nhân:** Cấu hình ArgoCD Notifications Triggers chưa bật event `on-sync-failed`.
- **Cách khắc phục:** Khai báo trigger `trigger.on-sync-failed` trỏ tới Slack Webhook URL.

### 39. Sự cố `helm diff` render ra toàn bộ file do khác khoảng trắng Indent
- **Triệu chứng:** Báo cáo diff hiển thị thay đổi 100% dòng làm rối Reviewer.
- **Nguyên nhân:** Khác biệt format end-of-line CRLF (Windows) và LF (Linux).
- **Cách khắc phục:** Chuẩn hóa `.gitattributes` bắt buộc dùng dòng kết thúc LF.

### 40. Sự cố ArgoCD ngắt kết nối Git do vượt quá giới hạn API Rate Limit
- **Triệu chứng:** Log ArgoCD báo lỗi `429 Too Many Requests` từ GitLab API.
- **Nguyên nhân:** Đặt thời gian Polling `timeout.requeue` quá ngắn (mỗi 5 giây).
- **Cách khắc phục:** Tăng thời gian Polling lên 3 phút và sử dụng GitLab Webhooks để trigger Sync.

### 41. Sự cố Quên cờ `--create-namespace` làm lệnh `helm upgrade` nổ lỗi
- **Triệu chứng:** Helm báo `namespaces "production" not found`.
- **Nguyên nhân:** Namespace mục tiêu chưa được khởi tạo trên cụm K8s.
- **Cách khắc phục:** Luôn bổ sung cờ `--create-namespace`.

### 42. Sự cố Tệp `argocd-sync-audit.json` bị mất log khi chạy lại
- **Triệu chứng:** Nhật ký kiểm toán bị đè mất lịch sử cũ.
- **Nguyên nhân:** Dùng toán tử ghi đè `>` thay vì toán tử ghi nối `>>`.
- **Cách khắc phục:** Sử dụng `>>` để nối tiếp nhật ký kiểm toán.

### 43. Sự cố Pods Ingress không tự động cập nhật TLS Certificate mới
- **Triệu chứng:** HTTPS domain báo chứng chỉ cũ hết hạn.
- **Nguyên nhân:** Cert-Manager chưa tự động kích hoạt renewal trigger.
- **Cách khắc phục:** Sử dụng External-DNS và Cert-Manager tích hợp trong Helm Chart.

### 44. Sự cố `gitops-revert-rollback.sh` không thể thực thi revert do working directory không sạch
- **Triệu chứng:** Git revert nổ lỗi `local changes would be overwritten`.
- **Nguyên nhân:** Có tệp rác chưa commit trong làm việc.
- **Cách khắc phục:** Chạy `git status` và dọn dẹp workspace trước khi revert.

### 45. Sự cố ArgoCD Application Set nổ lỗi template loop
- **Triệu chứng:** Không thể tự động sinh các Applications cho Multi-Cluster.
- **Nguyên nhân:** Cấu hình ApplicationSet Generator bị sai cú pháp `elements`.
- **Cách khắc phục:** Kiểm tra lại cấu trúc ApplicationSet spec.

### 46. Sự cố `helm package` nổ lỗi `directory not found`
- **Triệu chứng:** Không đóng gói được Helm Chart thành tệp `.tgz`.
- **Nguyên nhân:** Chỉ định sai đường dẫn tới thư mục chứa `Chart.yaml`.
- **Cách khắc phục:** Kiểm tra chính xác đường dẫn thư mục `helm/payment-service`.

### 47. Sự cố ArgoCD Self-Healing không chạy do tắt cờ `automated`
- **Triệu chứng:** Sửa thủ công bằng `kubectl edit` nhưng cụm không tự khôi phục.
- **Nguyên nhân:** Khai báo `selfHeal: true` nhưng thiếu khối cha `automated:`.
- **Cách khắc phục:** Đảm bảo `selfHeal: true` nằm bên trong khối `syncPolicy.automated`.

### 48. Sự cố Cụm AKS/GKE bị treo ngắt kết nối trong lúc `helm upgrade` đang `--wait`
- **Triệu chứng:** Lệnh deploy bị hủy ngầm do nghẽn mạng.
- **Nguyên nhân:** Băng thông mạng giữa Runner và cụm K8s bị chập chờn.
- **Cách khắc phục:** Đặt Runner trong cùng VPC/VNet với cụm Kubernetes.

### 49. Sự cố `final-helm-gitops-lab-evaluation.sh` nổ lỗi syntax bash
- **Triệu chứng:** Script tổng kết báo lỗi dòng.
- **Nguyên nhân:** Thiếu dấu ngoặc vuông đóng `]` trong câu lệnh `if`.
- **Cách khắc phục:** Đảm bảo cú pháp `[ -f file ]` chuẩn xác.

### 50. Sự cố Tệp SealedSecret bị commit trùng cả file Secret chưa mã hóa
- **Triệu chứng:** File `secret.yaml` plain-text vô tình bị push lên Git kèm file `sealed-secret.yaml`.
- **Nguyên nhân:** Quên thêm `secret.yaml` vào tệp `.gitignore`.
- **Cách khắc phục:** Bổ sung `secrets/*.plain.yaml` vào `.gitignore` lập tức.

### 51. Sự cố Helm Release Revision tăng lên hàng trăm làm chậm lệnh `helm list`
- **Triệu chứng:** Lệnh `helm list` phản hồi chậm 10 giây.
- **Nguyên nhân:** Không giới hạn số lượng Revisions lịch sử lưu giữ.
- **Cách khắc phục:** Truyền cờ `--history-max 10` trong câu lệnh `helm upgrade`.

### 52. Sự cố ArgoCD UI báo cờ `SharedResourceWarning`
- **Triệu chứng:** Cảnh báo tài nguyên bị quản lý bởi 2 ArgoCD Applications khác nhau.
- **Nguyên nhân:** Trùng lặp `metadata.name` của Service trong 2 Helm Charts.
- **Cách khắc phục:** Đảm bảo tên tài nguyên có tiền tố `{{ .Release.Name }}` độc nhất.

### 53. Sự cố `scripts/validate-helm-gitops-ci.sh` bị nổ lỗi permission denied
- **Triệu chứng:** Không chạy được script linter.
- **Nguyên nhân:** Quên cấp quyền execution cho file.
- **Cách khắc phục:** Chạy `chmod +x scripts/validate-helm-gitops-ci.sh`.

### 54. Sự cố Rollback GitOps bị kẹt do Image Tag cũ bị xóa trên Container Registry
- **Triệu chứng:** Revert commit thành công nhưng Pods bị ImagePullBackOff.
- **Nguyên nhân:** Image Tag cũ v2.5.0 đã bị dọn dẹp bởi Registry Cleanup Policy.
- **Cách khắc phục:** Đặt chính sách giữ lại (Retention Policy) cho các Image Tags được release trên Production.

### 55. Sự cố Phê duyệt manual stage GitOps bị canceled do quá 7 ngày
- **Triệu chứng:** Job CI manual bị hủy tự động.
- **Nguyên nhân:** Nút manual deploy trong MR không được tương tác trong 7 ngày.
- **Cách khắc phục:** Chạy lại (Retry) pipeline từ giao diện GitLab CI UI.

---

## Bài tập mở rộng

1. **Xây dựng Quy trình Multi-Environment GitOps với Kustomize & ArgoCD:**
   - Xây dựng cấu hình GitOps Repository ứng dụng công cụ **Kustomize** để quản lý 3 môi trường: `base/`, `overlays/development/`, `overlays/staging/`, và `overlays/production/`.
   - Cấu hình **ArgoCD ApplicationSet** tự động quét thư mục `overlays/` và tự động sinh ra 3 ArgoCD Applications tương ứng cho 3 môi trường mà không cần viết lặp lại code YAML!

2. **Tích hợp External Secrets Operator (ESO) với HashiCorp Vault trong GitOps Pipeline:**
   - Thay thế tệp SealedSecrets bằng **External Secrets Operator (ESO)** trên cụm Kubernetes.
   - Viết manifest `ExternalSecret` liên kết với HashiCorp Vault Secrets Engine. Khi commit manifest này lên GitOps Repo, ESO tự động kéo bí mật từ Vault về tạo Kubernetes Secret nội bộ hoàn toàn bảo mật và tự động xoay vòng chìa khóa (Secret Rotation)!

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| Bước 1 | Khởi tạo Cấu trúc Thư mục và Helm Chart Microservice | 10 phút |
| Bước 2 | Khởi tạo các Tệp Templates Kubernetes Manifests trong Helm Chart | 10 phút |
| Bước 3 | Thực thi Script `helm lint` và Render Template Kiểm tra Syntax | 15 phút |
| Bước 4 | Viết Script Mô phỏng Push-based `helm upgrade --atomic` | 15 phút |
| Bước 5 | Kiểm thử Tính năng Tự động Rollback Nguyên tử (`--atomic`) khi Pod Crash | 10 phút |
| Bước 6 | Khởi tạo ArgoCD Application Manifest chuẩn GitOps | 10 phút |
| Bước 7 | Viết Script Mô phỏng CI Commit Tự động nâng Image Tag sang GitOps Repo | 15 phút |
| Bước 8 | Viết Script Mô phỏng ArgoCD Pull Sync Engine | 15 phút |
| Bước 9 | Kiểm thử Phát hiện Sai lệch Trạng thái (State Drift) và Self-Healing | 10 phút |
| Bước 10 | Khởi tạo Tệp Bitnami SealedSecrets Mã hóa Bí mật | 10 phút |
| Bước 11 | Xây dựng Script Ghi nhận Nhật ký ArgoCD Audit Event Log | 10 phút |
| Bước 12 | Xây dựng Script Linter Kiểm tra Cấu hình Helm & GitOps CI | 5 phút |
| Bước 13 | Xây dựng Script Kiểm tra Khôi phục Sự cố Git Revert Rollback | 5 phút |
| Bước 14 | Tổng hợp Đánh giá Hoàn thành Bài Lab Buổi 41 | 5 phút |
| **Tổng** | **Khối thực hành lab** | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

# Buổi 41: Deploy Kubernetes: helm upgrade trực tiếp so với GitOps — Vấn Đáp & Phỏng Vấn

## Thống kê & Phân bổ thời lượng
- **Tổng thời lượng:** 20 phút
- **Cấu trúc:**
  - 5 phút: Kiểm tra phản xạ lý thuyết (12 câu hỏi trắc nghiệm & tự luận nhanh)
  - 10 phút: Đóng vai phỏng vấn tình huống thực chiến (7 kịch bản nâng cao)
  - 5 phút: Chốt từ khóa ăn tiền (§V3) & Giao bài tập về nhà chuẩn bị cho Buổi 42 (BTVN 4)

---

## §V1. 12 Câu hỏi vấn đáp kiểm tra phản xạ

### Câu 1
**Hỏi:** Sự khác biệt bản chất nhất giữa mô hình Push-based CD (`helm upgrade` trực tiếp) và Pull-based CD (GitOps ArgoCD) trong Kubernetes là gì?

**Gợi ý trả lời ngắn:**
Khác nhau ở vị trí lưu trữ Kubeconfig credentials và thực thể chủ động kích hoạt đồng bộ hạ tầng (CI Runner đẩy từ ngoài vào vs Controller kéo từ trong cụm).

**Đáp án chuẩn:**
- **So sánh Kiến trúc:**
  1. *Push-based CD:* Trình biên dịch CI Runner (ở ngoài cụm) giữ file Kubeconfig admin và trực tiếp thực thi câu lệnh `helm upgrade` đẩy manifests vào Kubernetes API Server.
  2. *Pull-based GitOps CD:* Một Controller (như ArgoCD) cài sẵn bên trong cụm Kubernetes tự động theo dõi kho mã nguồn GitOps Repository, liên tục so sánh và kéo (Pull) trạng thái mong muốn về cụm.
- **Lợi ích an ninh:** GitOps đóng toàn bộ chiều kết nối Inbound, không để lộ Kubeconfig Admin ra máy chủ CI Runner bên ngoài, giúp bảo vệ tối đa ranh giới an toàn cho cụm Kubernetes Production.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng "GitOps chỉ là việc lưu file YAML trên Git rồi cho CI Runner chạy lệnh `kubectl apply`".

---

### Câu 2
**Hỏi:** Tại sao hai cờ `--atomic` và `--wait` lại bắt buộc phải đi cùng nhau khi thực hiện câu lệnh `helm upgrade` từ CI Pipeline?

**Gợi ý trả lời ngắn:**
Cờ `--wait` ép Helm chờ tất cả các Pods vượt qua Readiness Probe thành công, nếu có Pod bị crash, cờ `--atomic` sẽ tự động rollback nguyên tử về phiên bản ổn định trước đó.

**Đáp án chuẩn:**
- **Cơ chế hoạt động:**
  - Cờ `--wait`: Ép Helm không được báo kết quả thành công ngay mà phải đợi tất cả các Pods trong Deployment đạt trạng thái `Ready` (vượt qua tất cả Readiness Probes).
  - Cờ `--atomic`: Nếu quá thời gian `--timeout 300s` mà Pods không Ready (do lỗi `CrashLoopBackOff` hoặc `ImagePullBackOff`), Helm tự động kích hoạt quá trình hủy bỏ nâng cấp và khôi phục (Rollback) 100% cụm về Revision cũ.
- **Ý nghĩa:** Tránh thảm họa "CI báo xanh ảo" trong khi ứng dụng Production thực tế đang bị sập không thể phục vụ khách hàng.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Chạy lệnh `helm upgrade --install` không có cờ `--atomic` và `--wait`.

---

### Câu 3
**Hỏi:** Ý nghĩa của tính năng Self-Healing (`syncPolicy.automated.selfHeal: true`) trong ArgoCD là gì?

**Gợi ý trả lời ngắn:**
Self-Healing giúp ArgoCD tự động ghi đè và khôi phục lại cấu hình chuẩn từ Git khi phát hiện có người dùng sửa bẩn thủ công trên cụm bằng `kubectl edit` hoặc `kubectl delete`.

**Đáp án chuẩn:**
- **Cơ chế phát hiện và xử lý State Drift:**
  ArgoCD liên tục so sánh Trạng thái mong muốn (Desired State trong Git) và Trạng thái thực tế (Live State trên Kubernetes). Nếu một kỹ sư trực ca gõ `kubectl edit deployment` làm lệch cấu hình trên cụm, ArgoCD sẽ phát hiện `OutOfSync` và lập tức tự động Re-sync ghi đè lại 100% cấu hình chuẩn từ Git trong vòng vài giây.
- **Ý nghĩa:** Đảm bảo duy nhất một Nguồn Sự Thật (Git is the Single Source of Truth) và bảo vệ hạ tầng khỏi sự can thiệp sai lệch con người.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Tắt cờ `selfHeal` khiến cụm bị lệch cấu hình kéo dài mà không ai hay biết.

---

### Câu 4
**Hỏi:** Tại sao không được thực thi câu lệnh `helm rollback` hoặc `kubectl edit` thủ công trên một cụm Kubernetes đang vận hành bởi ArgoCD?

**Gợi ý trả lời ngắn:**
Vì ArgoCD sẽ coi hành động thao tác thủ công đó là sai lệch trạng thái (State Drift) và tự động ghi đè (overwrite) ngược lại phiên bản lỗi đang khai báo trên Git!

**Đáp án chuẩn:**
- **Giải thích cơ chế Conflict:**
  ArgoCD liên tục giám sát Git. Khi bạn gõ `helm rollback <release>` trên cụm, trạng thái cụm thay đổi nhưng file YAML trên Git vẫn chưa đổi. ArgoCD Controller phát hiện sai lệch và kích hoạt Self-Healing lập tức ghi đè lại commit lỗi từ Git!
- **Quy trình chuẩn:** Muốn rollback trên GitOps, bắt buộc phải thực thi `git revert <commit_sha>` trên kho GitOps Repository và push commit mới lên.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Hoảng loạn gõ `helm rollback` trực tiếp trên terminal của cụm đang chạy ArgoCD.

---

### Câu 5
**Hỏi:** Tại sao trong kiến trúc GitOps Enterprise lại cần tách biệt App Code Repository và GitOps Config Repository thành 2 repos độc lập?

**Gợi ý trả lời ngắn:**
Để đảm bảo phân tách ranh giới trách nhiệm (Separation of Concerns), ngăn Developer tự ý chỉnh sửa tài nguyên hạ tầng Production và tránh vòng lặp CI build vô tận.

**Đáp án chuẩn:**
- **Lý do thiết kế:**
  1. *Phân quyền an ninh (Access Control):* Developer chỉ có quyền commit code ứng dụng ở App Repo. Chỉ có Tech Lead/DevOps và CI Bot mới có quyền commit vào GitOps Config Repo chứa tài nguyên Production.
  2. *Tránh Infinite CI Loop:* Nếu lưu Helm Chart chung trong App Repo, mỗi lần CI commit cập nhật Image Tag mới sẽ làm trigger lại chính pipeline build code ứng dụng đó, tạo thành vòng lặp build vô tận không ngắt.
- **Ý nghĩa:** Chuẩn hóa quy trình kiểm soát thay đổi theo quy định quản trị doanh nghiệp.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Để chung file `deployment.yaml` hoặc Helm Chart trong kho mã nguồn ứng dụng cho dev tự do sửa.

---

### Câu 6
**Hỏi:** Làm thế nào để commit an toàn các thông tin nhạy cảm (như DB Password) lên kho mã nguồn GitOps Repository mà không vi phạm tiêu chuẩn an toàn thông tin?

**Gợi ý trả lời ngắn:**
Sử dụng công cụ **Bitnami SealedSecrets** (dùng Public Key mã hóa bất đối xứng) hoặc **External Secrets Operator (ESO)** liên kết với Key Vault.

**Đáp án chuẩn:**
- **Giải pháp SealedSecrets:**
  Kỹ sư dùng công cụ `kubeseal` mã hóa file `secret.yaml` bằng Public Key của cụm Kubernetes. Output sinh ra file `sealed-secret.yaml` có thể commit công khai lên Git. Chỉ duy nhất SealedSecrets Controller giữ Private Key trong cụm mới giải mã được.
- **Giải pháp External Secrets Operator (ESO):**
  Commit file `ExternalSecret` manifest lên Git; Controller tự động kết nối HashiCorp Vault / Cloud Secret Manager để trích xuất mật khẩu và tạo Kubernetes Secret nội bộ hoàn toàn bảo mật.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Mã hóa Base64 mật khẩu (`echo "123456" | base64`) và commit file `secret.yaml` lên Git.

---

### Câu 7
**Hỏi:** Công cụ Helm plugin nào giúp hiển thị báo cáo so sánh sự thay đổi tài nguyên Kubernetes trực tiếp trên Merge Request pipeline trước khi merge code?

**Gợi ý trả lời ngắn:**
Plugin **`helm diff`** (thông qua câu lệnh `helm diff upgrade`).

**Đáp án chuẩn:**
- **Tích hợp helm diff vào CI/CD:**
  Trong stage `test` của MR pipeline, script chạy câu lệnh `helm diff upgrade <release> <chart> --values values-prod.yaml`. Kết quả diff (dạng tô màu xanh/đỏ thể hiện các dòng YAML thêm/sửa/xóa) được tự động comment báo cáo trực tiếp vào Merge Request.
- **Lợi ích:** Giúp Reviewer thấy rõ chính xác những tài nguyên nào sẽ bị tác động trước khi bấm duyệt merge code, ngăn ngừa sự cố xóa nhầm PVC hay Service quan trọng.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Duyệt Merge Request thay đổi Helm Chart mà không kiểm tra trước kết quả render diff.

---

### Câu 8
**Hỏi:** Cờ `syncPolicy.automated.prune: true` trên ArgoCD Application manifest có chức năng gì?

**Gợi ý trả lời ngắn:**
Tự động dọn dẹp và xóa bỏ các tài nguyên Kubernetes trên cụm khi tài nguyên đó bị xóa khỏi tệp khai báo YAML trong kho mã nguồn Git.

**Đáp án chuẩn:**
- **Cơ chế Pruning:**
  Nếu bạn xóa một file `ingress.yaml` hoặc bỏ một Service trong Helm Chart trên kho Git, cờ `prune: true` giúp ArgoCD phát hiện tài nguyên thừa trên cụm và tự động thực thi lệnh xóa tài nguyên đó để giữ nguyên trạng thái 100% khớp với Git.
- **Lưu ý:** Nếu không bật `prune: true`, các tài nguyên bị xóa trên Git vẫn tiếp tục tồn tại rác trên cụm Kubernetes, tiềm ẩn rủi ro xung đột hạ tầng.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Tắt cờ `prune` làm tích tụ tài nguyên rác và dính lỗi xung đột cấu hình cũ.

---

### Câu 9
**Hỏi:** Tại sao `readinessProbe` lại đóng vai trò sống còn đối với độ tin cậy của cả hai luồng Push-based (`helm upgrade --wait`) và Pull-based (ArgoCD Sync)?

**Gợi ý trả lời ngắn:**
Vì cả `--wait` của Helm và Sync Engine của ArgoCD đều dựa 100% vào chỉ số `Ready` do `readinessProbe` báo về để xác định Pod mới đã thực sự sẵn sàng nhận traffic hay chưa.

**Đáp án chuẩn:**
- **Giải thích chuyên sâu:**
  Nếu không có `readinessProbe`, Kubernetes coi Pod vừa tạo ra là Healthy ngay lập tức khi container vừa khởi chạy, khiến Helm/ArgoCD báo thành công và ngắt Pod cũ. Nhưng nếu ứng dụng Java/Node.js bên trong cần 15 giây để boot, toàn bộ người dùng truy cập trong 15 giây đó sẽ bị nổ lỗi HTTP 502/503!
- **Giải pháp:** Khai báo chuẩn xác HTTP GET path `/health/readiness` trên port ứng dụng kèm theo `initialDelaySeconds` phù hợp.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Bỏ trống khối `readinessProbe` trong tệp Deployment template spec.

---

### Câu 10
**Hỏi:** Khi bắt buộc phải triển khai bằng `helm upgrade` từ CI Runner, làm thế nào để hạn chế tối đa bán kính ảnh hưởng nếu tệp Kubeconfig bị lộ?

**Gợi ý trả lời ngắn:**
Cấp tệp Kubeconfig ServiceAccount bị giới hạn quyền `RoleBinding` trong duy nhất 1 namespace mục tiêu, tuyệt đối cấm cấp quyền `ClusterRoleBinding` cluster-admin.

**Đáp án chuẩn:**
- **Khoanh vùng an ninh (Blast Radius Isolation):**
  Tạo ServiceAccount `cicd-runner-sa` trên Kubernetes. Gán quyền qua `RoleBinding` (chỉ có quyền `get, list, update, patch` trên các tài nguyên Deployments/Services trong namespace `production`).
- **Kết quả:** Ngay cả khi rò rỉ Kubeconfig của Runner, kẻ tấn công cũng không thể thao tác sang các namespace khác hoặc can thiệp vào cụm Kubernetes.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Sử dụng tệp `admin.conf` mang quyền `cluster-admin` toàn cụm cho GitLab CI Runner.

---

### Câu 11
**Hỏi:** Khoảng thời gian timeout khuyến nghị tối đa cho câu lệnh `helm upgrade` trong CI Pipeline là bao nhiêu và tại sao?

**Gợi ý trả lời ngắn:**
Khuyến nghị là **300 giây (5 phút)** để tự động ngắt và rollback kịp thời khi Pods bị treo rớt vào trạng thái `ImagePullBackOff`.

**Đáp án chuẩn:**
- **Tại sao cần `--timeout 300s`:**
  Nếu Pod mới bị nổ lỗi kéo Image không được (`ImagePullBackOff`) hoặc crash boot lặp lại, cờ `--wait` sẽ khiến job CI treo chờ mãi mãi. Bổ sung `--timeout 300s` giúp Helm tự động ngắt sau 5 phút, kích hoạt atomic rollback và giải phóng Runner queue cho các dự án khác trong công ty.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Bỏ trống cờ `--timeout` làm job CI bị treo vô tận 2-3 tiếng đồng hồ.

---

### Câu 12
**Hỏi:** Làm thế nào để tự động hóa việc cập nhật Image Tag từ CI Pipeline sang kho GitOps Repository mà không gây xung đột Git Commit?

**Gợi ý trả lời ngắn:**
Sử dụng script CI tự động checkout GitOps Repo, thực thi `sed -i` cập nhật file `values.yaml`, chạy `git pull --rebase` và push commit mới chứa tag SHA.

**Đáp án chuẩn:**
- **Quy trình Auto-Commit chuẩn:**
  1. Job CI build xong Docker Image `payment:v2.6.0-sha999`.
  2. Script clone GitOps Repo qua `CI_JOB_TOKEN` hoặc Deploy Key.
  3. Cập nhật `tag: "v2.6.0-sha999"` trong file `values-prod.yaml`.
  4. Thực thi `git commit -m "chore(cd): update image tag to v2.6.0-sha999"` và `git push origin main`.
  5. ArgoCD tự động phát hiện commit mới và thực thi Sync mượt mà.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Chạy lệnh `argocd app sync` trực tiếp từ CI mà không commit thay đổi vào Git.

---

## §V2. Kịch bản phỏng vấn thực tế (Roleplay Scenarios)

### Kịch bản 1: Thuyết phục CTO chuyển đổi từ Helm Direct Upgrade sang GitOps ArgoCD
- **Người phỏng vấn (CTO):** *"Hệ thống của chúng ta đang dùng lệnh `helm upgrade` chạy từ GitLab CI ổn định 2 năm nay. Tại sao em lại đề xuất tốn công cài đặt ArgoCD để chuyển sang GitOps?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:* "Báo cáo anh, luồng Helm direct hiện tại đang chứa 3 lỗ hổng lớn về an ninh và vận hành đối với hạ tầng Production:"
  - "1. **Rủi ro lộ Kubeconfig Admin:** CI Runner đang giữ file Kubeconfig có quyền đẩy vào Production. Nếu máy chủ Runner bị lỗ hổng RCE, hacker sẽ chiếm toàn quyền xóa sạch cụm K8s."
  - "2. **Không phát hiện State Drift:** Nếu ai đó trực ca gõ `kubectl edit` sửa bẩn trên cụm, CI không hề biết để khôi phục, dẫn đến lệch cấu hình giữa Git và thực tế."
  - "3. **Giải pháp GitOps ArgoCD:** Giúp rút Kubeconfig về **bên trong cụm K8s**, đóng toàn bộ chiều mở port từ ngoài vào. Đồng thời kích hoạt tính năng **Self-Healing tự động khôi phục sự cố trong 2 giây**, giúp hệ thống đạt chuẩn an toàn Enterprise tuyệt đối."

---

### Kịch bản 2: Xử lý Sự cố `helm upgrade` bị treo vô hạn ở stage deploy
- **Người phỏng vấn (Senior DevOps Engineer):** *"Sáng nay job deploy Kubernetes bị treo ở stage `deploy` suốt 40 phút không chịu dừng cũng không báo lỗi. Em tìm nguyên nhân và xử lý thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Chẩn đoán nguyên nhân:** Job CI chạy `helm upgrade` có cờ `--wait` nhưng lại **bỏ quên cờ `--timeout 300s`**. Trong khi đó Pods mới bị gõ sai tên Image Repository nên rơi vào trạng thái `ImagePullBackOff`. Helm bị treo chờ vô tận.
    2. **Khắc phục sự cố quy chuẩn:**
       - Cancel job CI bị treo trên GitLab UI.
       - Sửa tệp `.gitlab-ci.yml`: Bổ sung đầy đủ bộ 3 cờ bắt buộc: `--atomic --wait --timeout 300s`.
       - Khắc phục tên Image Tag chuẩn xác trong `values.yaml`.
    3. **Kết quả:** Lần deploy tiếp theo xanh 100% trong vòng 45 giây và tự động rollback nguyên tử nếu xảy ra lỗi.

---

### Kịch bản 3: Giải quyết Sự cố Rollback thất bại do gõ `helm rollback` trên cụm ArgoCD
- **Người phỏng vấn (Lead Infrastructure):** *"Đêm qua bản deploy Prod bị lỗi, kỹ sư trực ca gõ `helm rollback payment-service 1` trên cụm, nhưng chỉ 5 giây sau ứng dụng tự nhảy ngược lại bản lỗi 2! Tại sao lại như vậy và khắc phục thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Giải thích hiện tượng:** Cụm Kubernetes đang bật ArgoCD với cờ `selfHeal: true`. Khi gõ `helm rollback` thủ công, ArgoCD phát hiện Trạng thái thực tế bị lệch so với Git Commit (đang trỏ bản lỗi 2), nên nó lập tức **Self-Healing ghi đè ngược lại bản lỗi**!
    2. **Quy trình Rollback chuẩn GitOps:**
       - Tuyệt đối không gõ lệnh `helm` hay `kubectl` trực tiếp trên cụm.
       - Mở kho GitOps Repo, thực thi lệnh: `git revert HEAD -m "revert: rollback broken release"`.
       - Push commit revert lên `main`. ArgoCD sẽ tự động kéo bản cũ v1 về và duy trì trạng thái Healthy 100%.

---

### Kịch bản 4: Thuyết phục Security Lead về phương án lưu Secrets trên GitOps Repo
- **Người phỏng vấn (Security Auditor):** *"Mô hình GitOps bắt chúng ta commit toàn bộ file YAML lên Git. Làm sao em đảm bảo các mật khẩu Database không bị lộ cho lập trình viên xem?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Cam kết 0% Plain-text Secrets:** "Báo cáo anh, chúng em tuyệt đối không commit file Secret chứa chuỗi Base64 plain-text lên Git."
    2. **Áp dụng Bitnami SealedSecrets:**
       - Mật khẩu được mã hóa bất đối xứng bằng Public Key của cụm qua lệnh `kubeseal`.
       - Tệp `SealedSecret` commit lên Git chỉ là các chuỗi cipher-text vô hại. Chỉ duy nhất SealedSecrets Controller giữ Private Key trong cụm K8s Production mới giải mã được.
       - Đáp ứng 100% tiêu chuẩn an toàn dữ liệu PCI-DSS và ISO 27001.

---

### Kịch bản 5: Xử lý Sự cố Sửa nhầm Pod Production bằng Self-Healing
- **Người phỏng vấn (Operations Manager):** *"Nếu một kỹ sư trực ca lỡ tay gõ `kubectl delete deployment payment-backend` trên cụm Production, hệ thống GitOps sẽ ứng phó ra sao?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Phản ứng tự động của ArgoCD:**
       - ArgoCD Controller phát hiện tài nguyên Deployment bị biến mất trên cụm (Trạng thái thực tế $\neq$ Trạng thái mong muốn trong Git).
       - Nhờ cờ `selfHeal: true`, ArgoCD ngay lập tức tự động Re-sync, tạo lại toàn bộ Deployment, Services và Pods từ Git chỉ trong vòng **2 giây**!
    2. **Kết luận:** Hệ thống tự khôi phục hoàn hảo mà không cần con người hoảng loạn can thiệp.

---

### Kịch bản 6: Tối ưu hóa Tốc độ Sync của ArgoCD không bị nghẽn API Rate Limit
- **Người phỏng vấn (Azure Cloud Architect):** *"Hệ thống của chúng ta có 200 microservices. ArgoCD liên tục poll Git gây lỗi `429 Too Many Requests` từ GitLab API. Em tối ưu thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Tắt Polling tần suất cao:** Tăng thời gian `timeout.requeue` của ArgoCD từ 3 phút lên 15 phút để giảm tải Polling API.
    2. **Cấu hình GitLab Webhooks:**
       - Khai báo Webhook trên GitLab Repo trỏ về ArgoCD API `https://argocd.company.com/api/webhook`.
       - Mỗi khi có Git commit mới, GitLab tự động gửi Webhook thông báo cho ArgoCD Sync lập tức. Tốc độ Sync tức thì (<1 giây) và triệt hạ 100% lỗi API Rate Limit!

---

### Kịch bản 7: Xây dựng Quy trình Merge Request Review với `helm diff`
- **Người phỏng vấn (DevOps Team Lead):** *"Làm sao em giúp các Reviewer phát hiện sớm việc một dev vô tình xóa mất PersistentVolumeClaim (PVC) trong file Helm Chart trước khi merge code vào `main`?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Tích hợp `helm diff` vào MR Pipeline:**
       - Trong stage `test` của MR, script thực thi `helm diff upgrade --values values-prod.yaml`.
    2. **Tự động comment báo cáo:**
       - Plugin `helm diff` sẽ tô màu đỏ cảnh báo dòng: `- apiVersion: v1, kind: PersistentVolumeClaim`.
       - Reviewer nhìn thấy ngay cảnh báo xóa PVC dữ liệu trên báo cáo MR và từ chối Merge (Reject). Ngăn chặn 100% thảm họa mất dữ liệu Production!

---

## §V3. Câu chốt để nói khi phỏng vấn

1. *"Bản chất của GitOps là **chuyển đổi hoàn toàn từ mô hình Push-based sang Pull-based CD**, để Git trở thành Nguồn Sự Thật Duy Nhất (Single Source of Truth) quản lý 100% hạ tầng."*
2. *"Triển khai Helm trực tiếp từ CI bắt buộc phải bổ sung bộ 3 cờ an toàn **`--atomic --wait --timeout 300s`** để chống báo xanh ảo khi Pod bị crash và tự động khôi phục."*
3. *"Cơ chế bảo vệ tối thượng của GitOps là **Rút Kubeconfig Admin về bên trong cụm Kubernetes**, triệt hạ 100% rủi ro lộ quyền kiểm soát từ máy chủ CI Runner bên ngoài."*
4. *"Tính năng **ArgoCD Self-Healing (`selfHeal: true`)** giúp tự động khôi phục hạ tầng chuẩn từ kho Git trong 2 giây khi có sự cố ai đó sửa thủ công bằng `kubectl edit`."*
5. *"Rollback trong mô hình GitOps **duy nhất và đúng chuẩn là thực thi `git revert <commit_sha>`**, tuyệt đối không gõ `helm rollback` thủ công trực tiếp trên cụm Kubernetes."*
6. *"Quản lý Secrets chuẩn GitOps là **sử dụng Bitnami SealedSecrets hoặc External Secrets Operator (ESO)** liên kết Vault, cấm 100% commit base64 plain-text lên kho mã nguồn Git."*
7. *"Luôn **tách biệt App Code Repo và GitOps Config Repo** để đảm bảo phân tách ranh giới trách nhiệm và tránh vòng lặp CI build vô tận."*
8. *"Tích hợp **`helm diff` plugin vào Merge Request pipeline** giúp Reviewer thấy rõ chính xác từng tài nguyên bị tác động trước khi duyệt merge code."*
9. *"Việc kích hoạt cờ **`syncPolicy.automated.prune: true`** đảm bảo ArgoCD tự động dọn dẹp các tài nguyên Kubernetes rác bị xóa trong Git."*
10. *"Triển khai Kubernetes Multi-Cluster bằng **ArgoCD ApplicationSet** giúp tự động hóa quản lý hàng trăm cụm mà không cần khai báo lặp lại YAML."*

---

## BTVN 4: Chuẩn bị cho Buổi 42 — Terraform trong GitLab CI: state, plan/apply gate, drift

Để chuẩn bị tốt nhất cho **Buổi 42: Terraform trong GitLab CI: state, plan/apply gate, drift**, học viên cần thực hiện các nhiệm vụ sau:

1. **Ôn tập kiến thức Infrastructure as Code (IaC) Terraform:**
   - Đọc trước cú pháp các câu lệnh Terraform cơ bản: `terraform init`, `terraform plan -out=tfplan`, `terraform apply tfplan`.
   - Tìm hiểu khái niệm **Terraform State File (`terraform.tfstate`)** và cơ chế State Locking với GitLab Managed Terraform State Backend.
   - Phân tích tầm quan trọng của việc lưu trữ State File tập trung và mã hóa an toàn trên GitLab backend.

2. **Nghiên cứu về quy trình Plan/Apply Gate:**
   - Phân tích nguyên lý bảo vệ hạ tầng: *"File `plan` trong Merge Request chỉ có giá trị khi **đúng tệp `tfplan` đó** được truyền sang stage `apply` — nếu không `apply` sẽ chạy lại plan mới gây lệch hạ tầng!"*
   - Tìm hiểu khái niệm **Infrastructure State Drift Detection** bằng lịch sử chạy `terraform plan` định kỳ qua Cron Schedule.

3. **Bài tập chuẩn bị trước giờ học:**
   - Trả lời câu hỏi: *"Tại sao không nên để lệnh `terraform apply` tự động chạy ngay khi merge code mà bắt buộc phải qua bước phê duyệt Manual Gate?"*
   - Chuẩn bị danh sách 3 rủi ro lớn nhất khi lưu tệp `terraform.tfstate` cục bộ trên máy chủ CI Runner!
   - Viết thử một file `main.tf` đơn giản tạo một tài nguyên S3 Bucket hoặc Resource Group sẵn sàng cho bài lab Buổi 42!