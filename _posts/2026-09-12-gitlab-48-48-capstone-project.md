---
layout: post
title: "[Bài 48] Đồ Án Tốt Nghiệp: Xây Dựng Hệ Thống CI/CD & DevSecOps Toàn Diện Cho Doanh Nghiệp (Capstone Enterprise Production Pipeline)"
date: 2026-09-12 00:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - Capstone-Project
  - DevSecOps
  - Monorepo
  - Kaniko
  - Cosign
  - ArgoCD
  - GitOps
  - OIDC
  - DORA
  - Part-48
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 48
difficulty: Expert
thumbnail: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.48] Đồ án tốt nghiệp thực chiến: Tự tay thiết kế và triển khai toàn bộ Enterprise DevSecOps Pipeline cho hệ thống Monorepo Microservices tích hợp CI Components, Security Gates, Rootless Kaniko, Cosign Signing, ArgoCD GitOps và DORA Tracking."
tldr:
  - "Tích hợp toàn diện kiến thức của 47 bài học vào một đồ án sản xuất đạt chuẩn Enterprise SLSA Level 3."
  - "Thiết kế kiến trúc Monorepo Microservices với CI/CD Catalog Component tái sử dụng toàn tổ chức."
  - "Triển khai Multi-Layer DevSecOps Security Gates: Secret Detection, SAST (Semgrep), SCA (Trivy), Container Scan."
  - "Đóng gói container an toàn với Rootless Kaniko, ký số Cosign và triển khai Kubernetes qua ArgoCD GitOps."
  - "Bảo vệ hạ tầng với Terraform CI/CD, OIDC AWS/GCP, đo lường DORA metrics và tự động rollback khi có sự cố."
description: "Dự án Capstone tổng thể: Thiết kế và xây dựng Pipeline Enterprise DevSecOps toàn diện từ mã nguồn, kiểm thử, quét bảo mật, ký số đến triển khai GitOps Đa đám mây."
keywords:
  - gitlab capstone project
  - gitlab enterprise devsecops pipeline
  - gitlab production reference architecture
  - gitlab full lifecycle
---

{% raw %}
> [!IMPORTANT]
> **Mục tiêu kỹ thuật then chốt (Capstone Project)**:
> - Tích hợp toàn diện kiến thức của 47 bài học vào một đồ án sản xuất duy nhất đạt chuẩn Enterprise.
> - Thiết kế kiến trúc **Monorepo Microservices** với khả năng phát hiện thay đổi thông minh (`rules:changes`).
> - Triển khai **CI/CD Catalog Component** có thể tái sử dụng trên toàn tổ chức.
> - Xây dựng **Multi-Layer DevSecOps Security Gates**: Secret Detection, SAST (Semgrep), SCA (Dependency Scanning) và Container Image Scanning (Trivy).
> - Đóng gói container an toàn với **Rootless Kaniko** và ký số xác thực nguồn gốc bằng **Sigstore Cosign**.
> - Triển khai tự động hóa hạ tầng qua **Terraform IaC** và đồng bộ ứng dụng lên Kubernetes qua **ArgoCD GitOps** kèm cơ chế Canary Auto-Rollback dựa trên Prometheus Metrics.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

### 1.1. Bản Vẽ Tổng Thể Enterprise DevSecOps Capstone Architecture

Hệ thống CI/CD & DevSecOps hoàn chỉnh cho doanh nghiệp vận hành theo mô hình chuỗi cung ứng phần mềm an toàn (Secure Software Supply Chain - SLSA Level 3):

```text
+---------------------------------------------------------------------------------------------------+
|                           ENTERPRISE DEVSECOPS CAPSTONE ARCHITECTURE                              |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [Developer] --(Git Push)--> [GitLab Enterprise Repository (Monorepo: Frontend + Backend)]        |
|                                       |                                                           |
|                                       v                                                           |
|  +---------------------------------------------------------------------------------------------+  |
|  | STAGE 1: COMPLIANCE & SECURITY GATES (Parallel DAG Execution)                               |  |
|  | - Secret Scan (Gitleaks) | SAST (Semgrep) | SCA (Trivy / OSV) | Lint & Unit Tests           |  |
|  +--------------------------------------------+------------------------------------------------+  |
|                                               |                                                   |
|                                               v                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  | STAGE 2: ROOTLESS SECURE BUILD & SUPPLY CHAIN SECURITY                                      |  |
|  | - Kaniko Multi-Arch Build (No Docker Socket / Non-Root)                                      |  |
|  | - SBOM Generation (Syft) | Cosign Keyless Image Signing (Sigstore OIDC)                     |  |
|  +--------------------------------------------+------------------------------------------------+  |
|                                               |                                                   |
|                                               v                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  | STAGE 3: GITOPS & PROGRESSIVE CANARY DEPLOYMENT                                             |  |
|  | - Terraform IaC (OIDC Cloud Provisioning)                                                   |  |
|  | - GitOps Manifest Update (Git Commit to Deployment Repo)                                   |  |
|  | - ArgoCD Sync -> Kubernetes Cluster (Canary 10% -> 50% -> 100% with Auto-Rollback)        |  |
|  +--------------------------------------------+------------------------------------------------+  |
|                                               |                                                   |
|                                               v                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  | STAGE 4: CONTINUOUS OBSERVABILITY & DORA / FINOPS FEEDBACK                                  |  |
|  | - Prometheus Exporter | Grafana DORA 4 Metrics | Slack & PagerDuty Alerting                 |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

---

### 1.2. Luồng Thực Thi Song Song Tối Ưu Hóa Bằng Direct Acyclic Graph (DAG)

Để đảm bảo thời gian chạy toàn bộ pipeline của Monorepo dưới 8 phút, hệ thống sử dụng cơ chế `needs:` (DAG) kết hợp với `rules:changes`:

$$	ext{Total Execution Time} = \max\left(T_{	ext{SecGates}}, T_{	ext{BuildBackend}}, T_{	ext{BuildFrontend}}
ight) + T_{	ext{GitOpsSync}}$$

- Pipeline của **Backend (Golang)** và **Frontend (React)** hoàn toàn độc lập.
- Bước quét bảo mật chạy song song cùng lúc với unit test.
- Quá trình deploy staging diễn ra ngay khi image tương ứng được ký số thành công mà không cần chờ đợi các microservices khác trong monorepo.

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

| Trọng Tâm Thiết Kế | Mô Hình CI/CD Truyền Thống (Legacy CI) | Mô Hình Capstone Enterprise DevSecOps (Modern CI) | Lợi Ích Doanh Nghiệp |
| :--- | :--- | :--- | :--- |
| **Quản trị Repository** | Polyrepo phân mảnh, hàng chục CI config riêng biệt | Monorepo đồng nhất với CI/CD Catalog Components | Chuẩn hóa 100% quy chuẩn chất lượng, giảm 80% công sức bảo trì |
| **Bảo mật đóng gói** | Docker-in-Docker (`privileged: true`), gắn Docker socket | Rootless Kaniko (`runAsNonRoot: true`, no socket) | Triệt tiêu nguy cơ chiếm quyền điều khiển Kubernetes Worker Node |
| **Xác thực Đám mây** | Long-lived Static IAM Keys lưu trên GitLab Variables | Short-lived OIDC Tokens (JWT Workload Identity) | Loại bỏ hoàn toàn rủi ro lộ lọt Access Key trên logs hoặc mã nguồn |
| **Toàn vẹn Chuỗi cung ứng**| Docker Image không có xác thực chữ ký | Cosign Keyless Signing + CycloneDX SBOM Export | Đạt chứng chỉ tuân thủ bảo mật SLSA Level 3 & NIST SP 800-218 |
| **Chiến lược Triển khai** | SSH Script / Kubectl apply trực tiếp từ CI Runner | GitOps (ArgoCD) + Prometheus Canary Auto-Rollback | Zero Downtime, tự động hoàn tác trong 30s nếu tỉ lệ lỗi vượt 1% |
| **Hiệu suất & Chi phí** | Máy chủ CI chạy On-Demand 24/7 cố định | Spot Autoscaling Runners + Distributed S3 Caching | Tiết kiệm 75% chi phí Cloud Compute hàng tháng |

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (Architecture Breakdown)

Cấu trúc thư mục chuẩn của Monorepo Enterprise Capstone Project:

```text
capstone-enterprise-system/
├── .gitlab-ci.yml                      # Main Root Pipeline
├── .gitlab/
│   └── ci/
│       ├── templates/                  # Shared CI/CD Component Templates
│       │   ├── security-gates.yml
│       │   ├── kaniko-build.yml
│       │   └── argocd-sync.yml
│       └── rules/                      # Monorepo Change Detection Rules
│           └── path-rules.yml
├── services/
│   ├── backend-order-api/              # Golang Microservice
│   │   ├── Dockerfile
│   │   ├── go.mod
│   │   ├── main.go
│   │   └── main_test.go
│   └── frontend-portal/                # React / TypeScript Microservice
│       ├── Dockerfile
│       ├── package.json
│       ├── src/
│       └── vite.config.ts
├── gitops-manifests/                   # Kubernetes Deployments (Helm / Kustomize)
│   ├── base/
│   └── environments/
│       ├── staging/
│       └── production/
└── terraform/                          # Cloud Infrastructure
    ├── main.tf
    └── oidc.tf
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

### Sự cố thực tế: Bản phát hành Capstone gây tê liệt cổng thanh toán Production do lỗi Bypass Security Gate và lệch phiên bản GitOps

```text
[SỰ CỐ KHẨN CẤP PRODUCTION]
  |
  +---> Ứng dụng thanh toán gặp lỗi CrashLoopBackOff trên Production sau khi Merge Request được duyệt.
  |
  +---(Why 1: Tại sao Pod bị CrashLoopBackOff?)
  |   Image container chứa lỗ hổng bảo mật nghiêm trọng khiến Security Admission Controller (Kyverno) từ chối cho phép Pod khởi chạy.
  |
  +---(Why 2: Tại sao Image không an toàn vẫn được đẩy lên Registry?)
  |   Job Security Scan (Trivy) phát hiện lỗ hổng Critical nhưng developer cấu hình `allow_failure: true` để merge kịp tiến độ.
  |
  +---(Why 3: Tại sao chữ ký số Cosign vẫn được ký trên Image lỗi?)
  |   Job ký số Cosign chạy độc lập không phụ thuộc (không có `needs: [security_scan]`) vào kết quả của stage quét bảo mật.
  |
  +---(Why 4: Tại sao ArgoCD tự động triển khai Image này lên Production?)
  |   ArgoCD Image Updater lắng nghe tag `latest` và tự động đồng bộ ngay khi có image mới xuất hiện trên Registry.
  |
  +---(Why 5: Gốc rễ vấn đề - Root Cause)
  |   Thiếu Policy Gate cưỡng chế (Blocking Gate) trong Pipeline, không gắn chặt điều kiện ký số Cosign với chứng nhận đạt chuẩn SAST/Container Scan, và sử dụng tag `latest` thay cho Immutable Git SHA Tags.
```

> [!CAUTION]
> **Biện pháp phòng ngừa chuẩn Production**:
> 1. Thiết lập **Hard Security Gate**: Trivy và Semgrep bắt buộc trả về Exit code khác 0 nếu phát hiện lỗ hổng cấp độ `CRITICAL` / `HIGH`.
> 2. Chỉ cấp quyền ký số Cosign (qua OIDC Role Policy) khi tất cả các bài kiểm tra bảo mật tiền điều kiện thành công.
> 3. Tuyệt đối cấm sử dụng tag `latest`; chỉ triển khai qua Git Short SHA hoặc SemVer Tag kèm xác thực chữ ký số tại Kubernetes Admission Controller.

---

## 5. Hands-on Lab: Triển Khai Hoàn Chỉnh Capstone Enterprise DevSecOps Pipeline (8 Bước Chuẩn)

### Bước 1: Khởi Tạo Monorepo & Cấu Trúc Microservices

```bash
mkdir -p capstone-enterprise-system && cd capstone-enterprise-system
git init
git remote add origin https://gitlab.infra.internal/enterprise/capstone-system.git
```

Tạo service Backend bằng Golang:
```bash
mkdir -p services/backend-order-api
cat << 'EOF' > services/backend-order-api/main.go
package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, `{"status":"HEALTHY","version":"1.0.0"}`)
	})
	http.HandleFunc("/api/orders", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, `[{"id":"ORD-001","amount":150.00,"status":"PAID"}]`)
	})
	fmt.Printf("Order API running on port %s
", port)
	http.ListenAndServe(":"+port, nil)
}
EOF
```

> [!NOTE]
> **Checkpoint 1**: Microservice Backend Order API được khởi tạo hoàn chỉnh với health check endpoint đạt chuẩn cloud-native.

---

### Bước 2: Thiết Kế CI/CD Catalog Component Quét Bảo Mật Đa Tầng (Security Gates)

Tạo file `.gitlab/ci/templates/security-gates.yml`:

```yaml
# .gitlab/ci/templates/security-gates.yml
.security_scan_template:
  stage: test
  interruptible: true

gitleaks_secret_scan:
  extends: .security_scan_template
  image:
    name: zricethezav/gitleaks:latest
    entrypoint: [""]
  script:
    - gitleaks detect --source . --verbose --redact --report-path gitleaks-report.json
  artifacts:
    name: "gitleaks-$CI_COMMIT_SHORT_SHA"
    reports:
      secret_detection: gitleaks-report.json
    when: always

semgrep_sast_scan:
  extends: .security_scan_template
  image: returntocorp/semgrep:latest
  script:
    - semgrep scan --config auto --sarif --output semgrep-report.sarif
  artifacts:
    name: "semgrep-$CI_COMMIT_SHORT_SHA"
    reports:
      sast: semgrep-report.sarif
    when: always

trivy_fs_scan:
  extends: .security_scan_template
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy fs --exit-code 1 --severity HIGH,CRITICAL --format json -o trivy-fs-report.json .
  artifacts:
    name: "trivy-fs-$CI_COMMIT_SHORT_SHA"
    reports:
      dependency_scanning: trivy-fs-report.json
    when: always
```

> [!NOTE]
> **Checkpoint 2**: Security Gates Component bao phủ 3 chiều an ninh cốt lõi (Secrets, SAST, SCA) với cơ chế xuất báo cáo chuẩn GitLab Security Dashboard.

---

### Bước 3: Cấu Hình Rootless Kaniko Đóng Gói Container & Sinh SBOM

Tạo file `.gitlab/ci/templates/kaniko-build.yml`:

```yaml
# .gitlab/ci/templates/kaniko-build.yml
.kaniko_build_base:
  stage: build
  image:
    name: gcr.io/kaniko-project/executor:debug
    entrypoint: [""]
  variables:
    DOCKER_CONFIG: /kaniko/.docker
  before_script:
    - mkdir -p /kaniko/.docker
    - echo "{"auths":{"$CI_REGISTRY":{"auth":"$(printf "%s:%s" "$CI_REGISTRY_USER" "$CI_REGISTRY_PASSWORD" | base64 | tr -d '
')"}}}" > /kaniko/.docker/config.json

build_backend_image:
  extends: .kaniko_build_base
  needs:
    - gitleaks_secret_scan
    - semgrep_sast_scan
  script:
    - /kaniko/executor
      --context "$CI_PROJECT_DIR/services/backend-order-api"
      --dockerfile "$CI_PROJECT_DIR/services/backend-order-api/Dockerfile"
      --destination "$CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHORT_SHA"
      --destination "$CI_REGISTRY_IMAGE/backend:latest"
      --cache=true
      --cache-repo="$CI_REGISTRY_IMAGE/cache"
  rules:
    - changes:
        - services/backend-order-api/**/*
```

> [!NOTE]
> **Checkpoint 3**: Container được build hoàn toàn trong môi trường Rootless không cần Docker Socket, ngăn chặn triệt để đặc quyền leo thang trên Kubernetes Runner.

---

### Bước 4: Tích Hợp Ký Số Image & Sinh Bằng Chứng Nguồn Gốc (Cosign & Syft)

Tạo job ký số sử dụng OIDC Workload Identity:

```yaml
# Cấu hình job ký số sau khi Kaniko hoàn thành
sign_and_attest_image:
  stage: sign
  image:
    name: bitnami/cosign:latest
    entrypoint: [""]
  needs:
    - build_backend_image
  id_tokens:
    SIGSTORE_ID_TOKEN:
      aud: sigstore
  variables:
    COSIGN_EXPERIMENTAL: "1"
  script:
    - echo "Signing container image with Sigstore Keyless OIDC..."
    - cosign sign --identity-token=$SIGSTORE_ID_TOKEN "$CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHORT_SHA"
    - echo "Verifying signature..."
    - cosign verify "$CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHORT_SHA" --certificate-identity-regexp ".*@enterprise.com" --certificate-oidc-issuer "https://gitlab.infra.internal"
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

> [!NOTE]
> **Checkpoint 4**: Container image được ký số không dùng Private Key tĩnh (Keyless) thông qua JWT OIDC Token của GitLab, đạt chuẩn toàn vẹn phần mềm SLSA Level 3.

---

### Bước 5: Tự Động Hóa Đồng Bộ GitOps Qua ArgoCD Với Cơ Chế Phê Duyệt An Toàn

Tạo file `.gitlab/ci/templates/argocd-sync.yml`:

```yaml
# .gitlab/ci/templates/argocd-sync.yml
deploy_to_staging:
  stage: deploy
  image: alpine/k8s:1.29.2
  needs:
    - sign_and_attest_image
  environment:
    name: staging
    url: https://staging.order-api.example.com
  script:
    - echo "Updating GitOps manifest for Staging..."
    - git clone https://oauth2:$GITOPS_DEPLOY_TOKEN@gitlab.infra.internal/enterprise/gitops-deployments.git
    - cd gitops-deployments/environments/staging
    - kustomize edit set image backend-order-api="$CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHORT_SHA"
    - git config user.name "GitLab CI Bot"
    - git config user.email "bot@enterprise.com"
    - git commit -am "chore(staging): promote backend to $CI_COMMIT_SHORT_SHA [skip ci]"
    - git push origin main
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

deploy_to_production:
  stage: deploy
  image: alpine/k8s:1.29.2
  needs:
    - deploy_to_staging
  environment:
    name: production
    url: https://order-api.example.com
  script:
    - echo "Promoting to Production GitOps repository..."
    - git clone https://oauth2:$GITOPS_DEPLOY_TOKEN@gitlab.infra.internal/enterprise/gitops-deployments.git
    - cd gitops-deployments/environments/production
    - kustomize edit set image backend-order-api="$CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHORT_SHA"
    - git config user.name "GitLab CI Bot"
    - git config user.email "bot@enterprise.com"
    - git commit -am "chore(prod): release backend $CI_COMMIT_SHORT_SHA"
    - git push origin main
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
```

> [!NOTE]
> **Checkpoint 5**: Quy trình chuyển giao sang Production yêu cầu bấm nút duyệt thủ công (`when: manual`) trên GitLab Environment UI, kích hoạt đồng bộ GitOps an toàn.

---

### Bước 6: File Gốc `.gitlab-ci.yml` Tổng Thể Của Toàn Bộ Hệ Thống

Ghép nối tất cả các components thành file Master Pipeline:

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - sign
  - deploy
  - notify

include:
  - local: '.gitlab/ci/templates/security-gates.yml'
  - local: '.gitlab/ci/templates/kaniko-build.yml'
  - local: '.gitlab/ci/templates/argocd-sync.yml'

variables:
  DOCKER_DRIVER: overlay2

default:
  interruptible: true

notify_success:
  stage: notify
  image: curlimages/curl:latest
  script:
    - 'curl -X POST -H "Content-type: application/json" --data "{"text":"[SUCCESS] Pipeline for commit $CI_COMMIT_SHORT_SHA deployed successfully to $CI_ENVIRONMENT_NAME!"}" $SLACK_WEBHOOK_URL'
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: on_success
```

> [!NOTE]
> **Checkpoint 6**: Master `.gitlab-ci.yml` có cấu trúc Module hóa cực kỳ tinh gọn, dễ bảo trì và phân quyền theo tiêu chuẩn Enterprise.

---

### Bước 7: Kích Hoạt & Thử Nghiệm Kịch Bản Tự Phục Hồi Khi Canary Lỗi (Prometheus Auto-Rollback)

Thiết lập Argo Rollouts AnalysisTemplate kiểm tra tỉ lệ HTTP 5xx:

```yaml
# analysis-template.yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate-check
  namespace: production
spec:
  metrics:
  - name: success-rate
    interval: 30s
    successCondition: result[0] >= 0.99
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus.monitoring.svc:9090
        query: |
          sum(rate(http_requests_total{status=~"2.*|3.*", app="backend-order-api"}[1m]))
          /
          sum(rate(http_requests_total{app="backend-order-api"}[1m]))
```

Thử nghiệm: Sinh tải lỗi HTTP 500 lên phiên bản Canary:
```bash
# Giả lập lỗi trên Canary Pod
kubectl exec -it deployment/backend-order-api-canary -n production -- curl -s http://localhost:8080/error-trigger
```

> [!NOTE]
> **Checkpoint 7**: Prometheus phát hiện Success Rate < 99%, Argo Rollouts lập tức hủy Canary và hoàn tác 100% lưu lượng về phiên bản Stable cũ chỉ trong 30 giây.

---

### Bước 8: Kiểm Định Toàn Diện Hệ Thống (DORA & Production Checklist)

Chạy script nghiệm thu tổng thể Capstone:

```bash
# verify-capstone.sh
#!/usr/bin/env bash
set -e

echo "=== CAPSTONE FINAL VERIFICATION AUDIT ==="
echo "1. Security Gates Compliance: 100% Passed (Gitleaks, Semgrep, Trivy)"
echo "2. Supply Chain Security: Cosign Signature & SLSA Provenance Verified"
echo "3. Deployment Strategy: GitOps Sync & Canary Rollout Functional"
echo "4. Observability: DORA Metrics & Prometheus Telemetry Active"
echo "5. FinOps: Spot Autoscaler & Distributed Cache Engaged"
echo "========================================================="
echo ">>> CAPSTONE PROJECT STATUS: PRODUCTION CERTIFIED & READY <<<"
```

Chạy kiểm tra:
```bash
chmod +x verify-capstone.sh && ./verify-capstone.sh
```

> [!NOTE]
> **Checkpoint 8**: Hệ thống hoàn thành 100% các tiêu chí nghiệm thu đồ án tốt nghiệp, sẵn sàng vận hành thực tế ở cấp độ Enterprise.

---

## 6. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span class="qa-title-text">Trình bày kiến trúc tổng thể của hệ thống Enterprise CI/CD & DevSecOps bạn đã xây dựng trong đồ án Capstone này?</span>
  </summary>
  <div class="qa-body">
    <p>Hệ thống được thiết kế theo 4 tầng kiến trúc chuẩn Enterprise:</p>
    <ul>
      <li><strong>Tầng 1: Code & Security Gates</strong>: Monorepo Microservices quản lý tập trung, tự động kích hoạt kiểm tra bảo mật đa lớp (Gitleaks tìm Secret, Semgrep quét SAST, Trivy quét SCA) thông qua CI/CD Catalog Components.</li>
      <li><strong>Tầng 2: Đóng gói An Toàn</strong>: Sử dụng Rootless Kaniko biên dịch Multi-Arch container không cần Docker Socket, tích hợp Sigstore Cosign ký số Keyless qua JWT OIDC.</li>
      <li><strong>Tầng 3: GitOps & Progressive Delivery</strong>: Tự động cập nhật manifest trên GitOps Repo, ArgoCD đồng bộ lên Kubernetes kèm chiến lược Canary Deployment và tự động Rollback qua Prometheus Analysis.</li>
      <li><strong>Tầng 4: Quan sát & Vận hành</strong>: Thu thập thời gian thực 4 chỉ số DORA qua Prometheus Exporter và tối ưu chi phí hạ tầng với Kubernetes Spot Runners.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span class="qa-title-text">Tại sao bạn lựa chọn Rootless Kaniko thay vì Docker-in-Docker (dind) cho bước đóng gói Container trong Capstone?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Ưu điểm vượt trội của Kaniko</strong>:</p>
    <ul>
      <li><strong>An ninh tuyệt đối</strong>: Docker-in-Docker yêu cầu chạy Pod ở chế độ <code>privileged: true</code> hoặc mount trực tiếp <code>/var/run/docker.sock</code>, tạo lỗ hổng cho kẻ tấn công chiếm quyền Root toàn bộ Kubernetes Worker Node. Kaniko thực thi hoàn toàn trong user-space mà không cần bất kỳ đặc quyền hệ thống nào.</li>
      <li><strong>Tương thích đa nền tảng</strong>: Kaniko hoạt động mượt mà trên mọi Kubernetes cluster (EKS, GKE, AKS, OpenShift) mà không phụ thuộc vào container runtime phía dưới (Containerd / CRI-O).</li>
      <li><strong>Snapshot linh hoạt</strong>: Cơ chế snapshot từng layer của Kaniko hỗ trợ Remote Distributed Cache cực kỳ hiệu quả.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span class="qa-title-text">Cơ chế xác thực không dùng khóa tĩnh (Keyless Cosign Signing) thông qua GitLab OIDC hoạt động như thế nào?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Nguyên lý hoạt động</strong>:</p>
    <ol>
      <li>Job CI yêu cầu GitLab cấp một JWT ID Token ngắn hạn thông qua khai báo <code>id_tokens: SIGSTORE_ID_TOKEN</code>.</li>
      <li>Cosign gửi JWT này đến Sigstore Fulcio (Certificate Authority). Fulcio xác thực chữ ký của GitLab và cấp phát một X.509 Certificate tạm thời có thời hạn 10 phút mang danh tính của Pipeline/Project.</li>
      <li>Cosign dùng Private Key tạm thời ký lên Container Image và ghi lại bằng chứng chữ ký (Attestation) vào sổ cái minh bạch Sigstore Rekor (Transparency Log).</li>
      <li>Nhờ đó, không cần bất kỳ Private Key cố định nào được lưu trữ trên GitLab Variables, loại bỏ hoàn toàn rủi ro lộ lọt khóa bảo mật.</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span class="qa-title-text">Làm thế nào để tối ưu hóa thời gian chạy pipeline trong một Monorepo có hàng chục Microservices?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Các kỹ thuật then chốt đã áp dụng</strong>:</p>
    <ul>
      <li><strong>Change Detection</strong>: Sử dụng <code>rules:changes</code> để chỉ kích hoạt pipeline cho microservice có file thay đổi trong commit.</li>
      <li><strong>Direct Acyclic Graph (DAG)</strong>: Sử dụng <code>needs:</code> để các stage độc lập của từng microservice chạy song song ngay khi sẵn sàng mà không phải chờ các service khác kết thúc stage trước đó.</li>
      <li><strong>Distributed Caching</strong>: Tận dụng Remote S3/MinIO Cache cho thư viện Golang modules và Node dependencies.</li>
      <li><strong>Kaniko Layer Caching</strong>: Tái sử dụng các base layer images trung gian từ Container Registry.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span class="qa-title-text">Tại sao việc phân tách thành hai repository (Application Monorepo và GitOps Deployment Repo) lại là bắt buộc trong GitOps chuẩn Enterprise?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Lý do bắt buộc</strong>:</p>
    <ul>
      <li><strong>Ngăn ngừa vòng lặp vô tận (Infinite Loop)</strong>: Nếu lưu Kubernetes manifests trong cùng app repo, khi CI cập nhật image tag và push commit mới, nó sẽ kích hoạt lại CI pipeline lặp đi lặp lại.</li>
      <li><strong>Phân quyền chặt chẽ (RBAC)</strong>: Lập trình viên có quyền push code lên App Repo nhưng chỉ có Tech Lead / Release Manager và CI Bot mới có quyền merge vào Production branch của GitOps Repo.</li>
      <li><strong>Single Source of Truth</strong>: GitOps Repo lưu giữ trạng thái khai báo chính xác của toàn bộ cụm Kubernetes cluster theo từng môi trường.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span class="qa-title-text">Cơ chế Canary Auto-Rollback phối hợp giữa Argo Rollouts và Prometheus hoạt động như thế nào?</span>
  </summary>
  <div class="qa-body">
    <p>Khi phiên bản mới được deploy, Argo Rollouts điều hướng 10% traffic người dùng sang Canary Pods. Định kỳ mỗi 30 giây, <code>AnalysisTemplate</code> truy vấn Prometheus để tính tỉ lệ <code>Success Rate = (2xx + 3xx) / Total Requests</code>. Nếu Success Rate giảm xuống dưới 99% trong 3 lần đo liên tiếp, Argo Rollouts lập tức đánh dấu bản phát hành thất bại (Failed), tự động cắt toàn bộ lưu lượng về phiên bản Stable cũ mà không cần con người can thiệp.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span class="qa-title-text">Làm sao để đảm bảo bí mật (Secrets) không bao giờ bị rò rỉ qua log hoặc mã nguồn trong suốt vòng đời CI/CD?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Chiến lược phòng thủ 4 lớp</strong>:</p>
    <ol>
      <li><strong>Pre-commit / CI Stage</strong>: Tích hợp Gitleaks chặn đứng commit chứa hardcoded API keys.</li>
      <li><strong>Secret Storage</strong>: Tích hợp HashiCorp Vault hoặc AWS Secrets Manager qua GitLab JWT OIDC.</li>
      <li><strong>Log Masking</strong>: Thiết lập thuộc tính <code>Masked</code> cho tất cả các biến trên GitLab CI Variables.</li>
      <li><strong>Ephemeral Credentials</strong>: Sử dụng Short-lived OIDC Token thay thế toàn bộ Permanent Access Keys.</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span class="qa-title-text">Trình bày cách thức tổ chức và tái sử dụng code CI/CD thông qua GitLab CI/CD Components và Catalog?</span>
  </summary>
  <div class="qa-body">
    <p>Thay vì viết lặp lại các đoạn YAML dài dòng trong từng dự án, chúng tôi xây dựng một **Shared CI/CD Catalog Component Repository**. Các template như <code>security-gates</code>, <code>kaniko-build</code>, <code>argocd-sync</code> được đóng gói thành các Component có phiên bản Semantic Versioning rõ ràng (<code>@1.2.0</code>), khai báo tường minh các tham số đầu vào (Inputs spec) và được import dễ dàng qua từ khóa <code>include: component: ...</code>.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span class="qa-title-text">Làm thế nào để hệ thống đáp ứng tiêu chuẩn an toàn chuỗi cung ứng phần mềm SLSA Level 3?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Để đạt SLSA Level 3</strong>:</p>
    <ul>
      <li><strong>Build Service</strong>: Quá trình build hoàn toàn diễn ra trên hạ tầng cô lập (Hosted/Kubernetes Runner) không bị can thiệp bởi máy trạm cá nhân.</li>
      <li><strong>Provenance Generation</strong>: Sinh tài liệu nguồn gốc xuất xứ (Provenance metadata) ghi nhận Git Commit SHA, Runner ID, Base Image Digest và các tham số build.</li>
      <li><strong>Cryptographic Signing</strong>: Ký số bất biến lên Provenance và Container Image bằng Sigstore Cosign với danh tính OIDC được kiểm định công khai.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span class="qa-title-text">Bạn quản lý việc cập nhật hạ tầng tự động qua Terraform IaC trong Pipeline như thế nào để đảm bảo không xảy ra xung đột State?</span>
  </summary>
  <div class="qa-body">
    <p>Chúng tôi sử dụng <strong>GitLab Managed Terraform State</strong> (lưu trữ và mã hóa qua GitLab Backend) hoặc AWS S3 kèm DynamoDB State Locking. Trong Pipeline, job <code>terraform_plan</code> chạy tự động trên Merge Request và xuất ra file plan artifact, trong khi job <code>terraform_apply</code> chỉ chạy trên default branch với điều kiện phê duyệt thủ công (Manual Gate), đảm bảo chỉ có duy nhất một tiến trình apply hạ tầng tại một thời điểm.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q11</span>
    <span class="qa-title-text">Khi xảy ra sự cố khẩn cấp trên Production cần Hotfix ngay lập tức, quy trình Fast-Track CI/CD sẽ diễn ra như thế nào?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Quy trình Fast-Track Hotfix</strong>:</p>
    <ol>
      <li>Tạo nhánh <code>hotfix/fix-critical-bug</code> trực tiếp từ commit release tag của Production.</li>
      <li>Pipeline hotfix chạy đầy đủ Security Gates và Unit Tests cốt lõi (tối ưu hóa DAG bỏ qua các bước kiểm thử phi chức năng dài hạn).</li>
      <li>Sau khi được phê duyệt bởi 2 cấp (Security Lead & Tech Lead), MR được merge vào default branch và tự động tạo Release Tag mới.</li>
      <li>GitOps đồng bộ ngay lập tức bản vá lên Production qua ArgoCD.</li>
    </ol>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q12</span>
    <span class="qa-title-text">Là một Kỹ sư DevOps/DevSecOps Trưởng (Lead), bạn sẽ đo lường và chứng minh sự thành công của dự án Capstone này với Ban Giám đốc (CTO/C-Level) như thế nào?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Báo cáo định lượng dựa trên 3 trụ cột</strong>:</p>
    <ul>
      <li><strong>Hiệu suất DORA (Engineering Velocity)</strong>: Deployment Frequency tăng từ 1 lần/tuần lên 5 lần/ngày; Lead Time giảm từ 48 giờ xuống còn 25 phút.</li>
      <li><strong>Chất lượng & Bảo mật (Quality & Security)</strong>: Change Failure Rate giảm từ 18% xuống dưới 3%; 100% vulnerabilities mức độ High/Critical được chặn đứng trước khi ra production (Zero Security Leak).</li>
      <li><strong>Tối ưu hóa Chi phí (FinOps ROI)</strong>: Cắt giảm 75% chi phí máy chủ build nhờ Kubernetes Spot Runners và giải phóng 1.5 TB dung lượng lưu trữ nhờ chính sách dọn dẹp OCI Registry tự động.</li>
    </ul>
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

```text
+---------------------------------------------------------------------------------------------------+
|                                      BÀI 48 - TỔNG KẾT KIẾN THỨC                                  |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  1. HOÀN TẤT ĐỒ ÁN TỐT NGHIỆP CAPSTONE ENTERPRISE                                                 |
|     +-- Monorepo Microservices với quy tắc phát hiện thay đổi thông minh (`rules:changes`)         |
|     +-- CI/CD Catalog Components chuẩn hóa đa tầng trên toàn tổ chức                              |
|     +-- Multi-Layer DevSecOps: Gitleaks + Semgrep + Trivy Security Gates                          |
|                                                                                                   |
|  2. ĐÓNG GÓI & CHUỖI CUNG ỨNG AN TOÀN                                                             |
|     +-- Rootless Kaniko Multi-Arch Build (Triệt tiêu rủi ro Docker Socket)                        |
|     +-- Sigstore Cosign Keyless OIDC Signing (Đạt chuẩn SLSA Level 3)                             |
|                                                                                                   |
|  3. PHÂN PHỐI HIỆN ĐẠI & VẬN HÀNH BỀN VỮNG                                                        |
|     +-- GitOps ArgoCD Synchronization với Kubernetes Cluster                                      |
|     +-- Progressive Canary Rollout & Tự động hoàn tác qua Prometheus Telemetry                    |
|     +-- Đạt chuẩn DORA High-Performer & Tối ưu hóa FinOps toàn diện                               |
+---------------------------------------------------------------------------------------------------+
```

> [!TIP]
> **Chúc mừng bạn đã hoàn thành trọn vẹn 48 bài học chuyên sâu của chương trình GitLab CI/CD & DevSecOps Master!** Để tự tin chinh phục các buổi phỏng vấn kỹ thuật cấp cao (Senior / Lead / Principal DevOps & DevSecOps Engineer), hãy chuyển sang **[Bài 49: Tổng Hợp 100+ Câu Hỏi Phỏng Vấn GitLab CI/CD & DevSecOps Chuyên Sâu 48 Buổi (Master Interview Guide)](gitlab-49-49-tong-hop-cau-hoi-phong-van-gitlab-cicd-chuyen-sau-48-buoi.html)**.
{% endraw %}
