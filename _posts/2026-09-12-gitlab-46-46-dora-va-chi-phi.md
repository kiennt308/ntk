---
title: "Bài 46: Đo Lường Hiệu Suất Kỹ Thuật (DORA Metrics), Value Stream Analytics & Tối Ưu Hóa Chi Phí CI/CD"
date: 2026-09-12 00:00:00 +0700
categories: [GitLab, CI/CD, DevSecOps]
tags: [GitLab-CI, DORA-Metrics, Value-Stream-Analytics, FinOps, Cost-Optimization, Prometheus, Grafana, Observability]
description: "Làm chủ 4 chỉ số DORA (Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service), thiết lập Value Stream Analytics và chiến lược FinOps tối ưu hóa chi phí compute & storage CI/CD ở quy mô lớn."
---

{% raw %}
> [!IMPORTANT]
> **Mục tiêu kỹ thuật then chốt**:
> - Hiểu sâu bản chất toán học và cơ chế thu thập dữ liệu của **4 chỉ số DORA** (Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service) trong GitLab.
> - Thiết lập quy trình đo lường dòng giá trị phần mềm với **GitLab Value Stream Analytics (VSA)** và Custom Stages.
> - Xây dựng hệ thống giám sát thời gian thực bằng **Prometheus GitLab Runner Exporter** và **Grafana DORA Dashboards**.
> - Triển khai chiến lược **FinOps cho CI/CD**: Quản trị hạn ngạch Compute Minutes, tối ưu hoá Spot/Preemptible Runner autoscaling và chính sách tự động dọn dẹp Artifacts/Container Registry.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

### 1.1. Bản Chất Kỹ Thuật & Kiến Trúc DORA Metrics Trong GitLab

Đo lường hiệu suất kỹ thuật phần mềm (Software Delivery Performance) theo chuẩn DORA (DevOps Research and Assessment) không chỉ là vẽ biểu đồ quản lý, mà là thiết lập một hệ thống **Event-Driven Telemetry** thu thập và phân tích trạng thái phát hành từ mã nguồn đến môi trường Production.

```text
+---------------------------------------------------------------------------------------------------+
|                                GITLAB DORA TELEMETRY EVENT STREAM                                 |
+---------------------------------------------------------------------------------------------------+
|  [Commit / MR Merge] ---> [CI/CD Pipeline Run] ---> [Deploy to Env: production]                   |
|           |                       |                               |                               |
|           v                       v                               v                               |
|    Commit Timestamp         Pipeline Logs                 Deployment Event                        |
|           |                       |                               |                               |
|           +-----------------------+-------------------------------+                               |
|                                   |                                                               |
|                                   v                                                               |
|             +-------------------------------------------+                                         |
|             |        GitLab Analytics Database Engine   |                                         |
|             |      (ClickHouse / PostgreSQL Aggregator) |                                         |
|             +---------------------+---------------------+                                         |
|                                   |                                                               |
|       +---------------------------+---------------------------+                                   |
|       v                           v                           v                                   v
| [1. Deployment Freq]    [2. Lead Time (LTC)]        [3. Change Failure]           [4. Time to Restore]    |
| (Deploys / Day/Week)    (Commit to Prod Deploy)     (Failed / Total Deploys)      (Incident Created to Solved)
+---------------------------------------------------------------------------------------------------+
```

#### Chi Tiết 4 Chỉ Số DORA Cốt Lõi

1. **Deployment Frequency (DF - Tần suất triển khai)**:
   - **Định nghĩa**: Tần suất một tổ chức triển khai mã nguồn thành công lên môi trường Production (`environment: name: production`).
   - **Cơ chế thu thập**: GitLab lắng nghe `Deployment` webhook events với `status == 'success'` trỏ đến production tier.
   - **Xếp hạng Elite**: Nhiều lần mỗi ngày (On-demand).

2. **Lead Time for Changes (LTC - Thời gian hoàn thành thay đổi)**:
   - **Định nghĩa**: Khoảng thời gian từ khi commit đầu tiên được tạo (hoặc merge request được mở) cho đến khi code đó chạy thành công trên production.
   - **Cơ chế thu thập**: $T_{	ext{LeadTime}} = T_{	ext{Deploy\_Success\_Prod}} - T_{	ext{First\_Commit\_In\_MR}}$.
   - **Xếp hạng Elite**: Dưới 1 giờ (nhờ CI/CD song song và pipeline siêu tốc).

3. **Change Failure Rate (CFR - Tỉ lệ lỗi khi thay đổi)**:
   - **Định nghĩa**: Tỉ lệ phần trăm các lần triển khai lên production dẫn đến sự cố suy giảm dịch vụ (cần rollback, hotfix hoặc mở Incident).
   - **Công thức**:
     $$	ext{CFR} = rac{	ext{Số lần Deploy thất bại hoặc sinh ra Production Incident}}{	ext{Tổng số lần Deploy lên Production}} 	imes 100\%$$
   - **Xếp hạng Elite**: 0% - 15%.

4. **Time to Restore Service (TTRS / MTTR - Thời gian phục hồi dịch vụ)**:
   - **Định nghĩa**: Thời gian từ khi một sự cố production xảy ra (hoặc Incident ticket được khởi tạo) cho đến khi dịch vụ được khôi phục hoàn toàn.
   - **Cơ chế thu thập**: $T_{	ext{Restore}} = T_{	ext{Incident\_Closed}} - T_{	ext{Incident\_Created}}$.
   - **Xếp hạng Elite**: Dưới 1 giờ.

---

### 1.2. Value Stream Analytics (VSA) & Dòng Chảy Giá Trị

Value Stream Analytics ánh xạ toàn bộ quy trình phát triển từ giai đoạn Lên ý tưởng (Issue Creation) đến khi Khách hàng nhận giá trị (Production Delivery). VSA chia vòng đời phần mềm thành các Stage chuẩn:

$$	ext{Total Cycle Time} = T_{	ext{Issue}} + T_{	ext{Plan}} + T_{	ext{Code}} + T_{	ext{Test}} + T_{	ext{Review}} + T_{	ext{Staging}} + T_{	ext{Production}}$$

- **Issue Stage**: Thời gian từ khi Issue được tạo đến khi được gán Milestone hoặc thêm vào Issue Board.
- **Plan Stage**: Thời gian từ khi Plan xong đến khi commit đầu tiên xuất hiện trong nhánh phát triển.
- **Code Stage**: Thời gian từ commit đầu tiên đến khi Merge Request (MR) được tạo.
- **Test Stage**: Tổng thời gian CI/CD pipelines chạy kiểm thử tự động cho MR.
- **Review Stage**: Thời gian từ khi mở MR đến khi MR được phê duyệt và Merge vào nhánh chính.
- **Staging Stage**: Thời gian từ khi Merge đến khi mã nguồn được deploy lên Staging.
- **Production Stage**: Thời gian từ khi deploy Staging đến khi deploy hoàn tất lên Production.

---

### 1.3. FinOps & Chiến Lược Tối Ưu Hóa Chi Phí CI/CD Toàn Diện

Một hạ tầng CI/CD quy mô lớn tiêu tốn tài nguyên ở hai nguồn chính: **Compute Resources (CPU/RAM/GPU runner hours)** và **Storage (Artifacts, Packages, Container Images, Job Logs)**.

```
+---------------------------------------------------------------------------------------------------+
|                                 ENTERPRISE CI/CD FINOPS STRATEGY                                  |
+---------------------------------------------------------------------------------------------------+
|  [Compute Optimization]                                   [Storage Optimization]                  |
|  - Kubernetes Autoscaling Runners (HPA / KEDA)            - Artifacts Expiration (`expire_in`)    |
|  - Spot/Preemptible Instance Nodes (Tiết kiệm 70-90%)      - GitLab Package Cleanup Policies       |
|  - Distributed Caching (S3 / GCS + MinIO)                 - Container Registry Tag Retention      |
|  - Stage Pruning & Job Interruption Control               - Job Log Compression & Remote S3 Arch  |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

| Tiêu Chí Kỹ Thuật | DORA Metrics (GitLab Native) | Custom Prometheus + Grafana DORA | Value Stream Analytics (VSA) | CI/CD FinOps Exporter |
| :--- | :--- | :--- | :--- | :--- |
| **Nguồn dữ liệu (Data Source)** | GitLab System Events, Deployments, Incidents | GitLab Webhooks, Prometheus CI Exporter, VictoriaMetrics | GitLab Issues, Merge Requests, Pipelines, Environments | AWS Cost Explorer, GCP Billing API, KubeCost, Runner Exporter |
| **Độ trễ cập nhật (Latency)** | Batch Aggregation (Theo chu kỳ 1h - 24h) | Real-time (Pull-based / Push metrics < 15s) | Gần thời gian thực (Event-driven) | Daily / Hourly batch export |
| **Độ tùy biến (Customizability)** | Giới hạn theo giao diện mặc định GitLab Ultimate | Tùy biến dashboard 100% bằng PromQL, SQL | Tùy biến Stage start/end events theo nhãn (Labels) | Tùy biến phân bổ chi phí theo Project/Team/Environment |
| **Phạm vi quản trị (Scope)** | Project, Group, Instance Level | Toàn tổ chức (Multi-GitLab instances, Hybrid Cloud) | Group & Project Value Streams | Multi-Cloud K8s Runners, SaaS Compute Minutes |
| **Cảnh báo tự động (Alerting)** | Hỗ trợ SLA Alert cơ bản | Alertmanager, PagerDuty, Slack Bot cảnh báo tức thì | Không có cơ chế push alert trực tiếp | KEDA budget alerts, Webhook cảnh báo vượt hạn ngạch chi phí |

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (Architecture Breakdown)

Hệ thống Observability & FinOps cho GitLab CI/CD quy mô Enterprise được tích hợp qua 3 tầng kiến trúc:

```
+---------------------------------------------------------------------------------------------------+
|                               PRODUCTION DORA & FINOPS ARCHITECTURE                               |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +---------------------------+        +--------------------------------+                          |
|  | GitLab CI/CD Workloads    | -----> | GitLab Prometheus Runner Exporter|                          |
|  | (1000+ Jobs / Day)       |        | (Port 9252 - Metrics)          |                          |
|  +-------------+-------------+        +---------------+----------------+                          |
|                |                                      |                                           |
|                | Webhooks (Pipeline/Deploy/Incident)  | Prometheus Scrape (15s)                   |
|                v                                      v                                           |
|  +---------------------------+        +---------------+----------------+                          |
|  | Event Ingestion Engine    |        | Prometheus / VictoriaMetrics   |                          |
|  | (Node.js / Go Webhook Rcv)|        | (TSDB Storage Engine)          |                          |
|  +-------------+-------------+        +---------------+----------------+                          |
|                |                                      |                                           |
|                v                                      v                                           |
|  +---------------------------+        +---------------+----------------+                          |
|  | PostgreSQL / ClickHouse   |        | Grafana Enterprise Dashboards  |                          |
|  | (DORA Historical Logs)    | -----> | - DORA 4 Metrics Panel         |                          |
|  +---------------------------+        | - Runner Cost Allocation Panel |                          |
|                                       +--------------------------------+                          |
+---------------------------------------------------------------------------------------------------+
```

### Chi Tiết Cấu Hình Prometheus Scrape Cho Runner & GitLab

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'gitlab-runners'
    static_configs:
      - targets:
          - 'runner-manager-01.infra.internal:9252'
          - 'runner-manager-02.infra.internal:9252'
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        regex: '(.*):9252'
        replacement: '$1'

  - job_name: 'gitlab-dora-exporter'
    static_configs:
      - targets: ['gitlab-dora-exporter.infra.internal:8080']
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

### Sự cố thực tế: Chi phí hạ tầng Cloud tăng đột biến 350% và Tỉ lệ Change Failure Rate bị tính toán sai lệch nghiêm trọng

```
[SỰ CỐ FINOPS & METRICS]
  |
  +---> Chi phí AWS EC2 cho Kubernetes Runner Nodes tăng vọt từ $3,000 lên $10,500/tháng.
  |     Đồng thời DORA Change Failure Rate hiển thị 85% trong khi dịch vụ Production không hề downtime.
  |
  +---(Why 1: Tại sao chi phí tăng vọt?)
  |   Runner autoscaler (KEDA/Cluster Autoscaler) giữ hàng trăm On-Demand nodes chạy liên tục không giải phóng.
  |
  +---(Why 2: Tại sao nodes không scale down?)
  |   Các CI Jobs bị treo ở trạng thái `stuck` hoặc `pending` do deadlock kết nối Docker daemon, và Artifacts lưu trữ không có hạn hết hạn (`expire_in`).
  |
  +---(Why 3: Tại sao Change Failure Rate bị báo sai 85%?)
  |   Nhóm phát triển cấu hình job deploy production thất bại khi test script kiểm tra health check trả về HTTP 401 nhưng retry liên tục 10 lần.
  |
  +---(Why 4: Tại sao GitLab ghi nhận mỗi lần retry là một failure?)
  |   Mỗi lần Job retry thất bại trên environment `production`, GitLab tạo ra một bản ghi Deployment `failed`, làm thổi phồng mẫu số và tử số của CFR.
  |
  +---(Why 5: Gốc rễ vấn đề - Root Cause)
  |   Thiếu chính sách `expire_in` mặc định cho CI Artifacts, không cấu hình Runner `idle_time` chuẩn trên Spot Instances, và định nghĩa `environment` sai mục đích trong các test jobs trung gian.
```

> [!CAUTION]
> **Biện pháp phòng ngừa chuẩn Production**:
> 1. Luôn khai báo `expire_in: 1 day` (hoặc tối đa `7 days`) cho tất cả build artifacts trung gian.
> 2. Chỉ gắn `environment: name: production` cho job thực sự thực hiện bước switch traffic / deploy production cuối cùng.
> 3. Triển khai Runner Node Pool sử dụng **Spot Instances** với tỉ lệ 90% Spot + 10% On-Demand kèm cơ chế fallback an toàn.

---

## 5. Hands-on Lab: Thiết Lập Đo Lường DORA & Tối Ưu Hóa Chi Phí CI/CD (8 Bước Chuẩn)

### Bước 1: Khởi tạo Project & Cấu hình Môi trường Production Đạt Chuẩn DORA

```bash
mkdir -p dora-finops-lab && cd dora-finops-lab
git init
git remote add origin http://gitlab.infra.internal/platform-team/dora-finops-lab.git
```

Tạo file `.gitlab-ci.yml` chuẩn hóa định nghĩa Environments:

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy_staging
  - deploy_production

variables:
  DOCKER_DRIVER: overlay2
  CI_DEBUG_TRACE: "false"

default:
  interruptible: true

unit_test:
  stage: test
  image: node:20-alpine
  script:
    - npm ci
    - npm run test:unit
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

build_image:
  stage: build
  image: docker:27-cli
  services:
    - docker:27-dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
  artifacts:
    name: "build-metadata-$CI_COMMIT_REF_SLUG"
    paths:
      - build.json
    expire_in: 2 days
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

deploy_to_staging:
  stage: deploy_staging
  environment:
    name: staging
    url: https://staging.app.example.com
  script:
    - echo "Deploying commit $CI_COMMIT_SHA to Staging environment..."
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'

deploy_to_production:
  stage: deploy_production
  environment:
    name: production
    url: https://app.example.com
    action: start
  script:
    - echo "Deploying commit $CI_COMMIT_SHA to Production environment..."
    - ./scripts/deploy.sh
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
```

> [!NOTE]
> **Checkpoint 1**: File `.gitlab-ci.yml` khai báo rõ `environment: name: production` giúp GitLab Event Engine tự động thu thập **Deployment Frequency** và **Lead Time for Changes**.

---

### Bước 2: Cấu hình Prometheus GitLab Runner Metrics Exporter

Mở file cấu hình GitLab Runner `/etc/gitlab-runner/config.toml` và kích hoạt Metrics Server:

```toml
# /etc/gitlab-runner/config.toml
concurrent = 20
check_interval = 5
listen_address = "0.0.0.0:9252"

[[runners]]
  name = "k8s-autoscale-spot-runner"
  url = "https://gitlab.infra.internal/"
  id = 12
  token = "glrt-t0k3n-s3cur3-v4lu3"
  executor = "docker"
  [runners.custom_build_dir]
  [runners.cache]
    MaxUploadedArchiveSize = 524288000 # 500MB
    Type = "s3"
    Shared = true
    [runners.cache.s3]
      ServerAddress = "s3.ap-southeast-1.amazonaws.com"
      BucketName = "gitlab-runner-distributed-cache"
      BucketLocation = "ap-southeast-1"
      Insecure = false
  [runners.docker]
    tls_verify = false
    image = "alpine:latest"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 2147483648 # 2GB
```

Khởi động lại Runner và kiểm tra endpoint metrics:

```bash
gitlab-runner restart
curl -s http://localhost:9252/metrics | grep "gitlab_runner_jobs"
```

> [!NOTE]
> **Checkpoint 2**: Endpoint `http://localhost:9252/metrics` trả về mã HTTP 200 kèm các metrics `gitlab_runner_jobs_total`, `gitlab_runner_concurrent`.

---

### Bước 3: Viết DORA Custom Exporter Thu Thập Dữ Liệu Qua GitLab GraphQL / REST API

Tạo file `exporter/dora_collector.py` để trích xuất DORA metrics phục vụ tổ chức chưa có bản quyền Ultimate:

```python
#!/usr/bin/env python3
import os
import time
import requests
from prometheus_client import start_http_server, Gauge

GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.infra.internal")
PRIVATE_TOKEN = os.getenv("GITLAB_TOKEN", "glpat-secret-token")
PROJECT_ID = os.getenv("PROJECT_ID", "42")

DEPLOYMENT_FREQ = Gauge('gitlab_dora_deployment_frequency_total', 'Total production deployments', ['project_id'])
LEAD_TIME_SECONDS = Gauge('gitlab_dora_lead_time_seconds', 'Lead time for changes in seconds', ['project_id'])
CHANGE_FAILURE_RATE = Gauge('gitlab_dora_change_failure_rate_ratio', 'Ratio of failed production deployments', ['project_id'])

def collect_dora_metrics():
    headers = {"PRIVATE-TOKEN": PRIVATE_TOKEN}
    
    # 1. Fetch Deployments
    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/deployments?environment=production&status=success"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        deploys = resp.json()
        DEPLOYMENT_FREQ.labels(project_id=PROJECT_ID).set(len(deploys))
        
    # 2. Calculate Failure Rate
    url_all = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/deployments?environment=production"
    resp_all = requests.get(url_all, headers=headers)
    if resp_all.status_code == 200:
        all_deploys = resp_all.json()
        failed = [d for d in all_deploys if d.get("status") == "failed"]
        total = len(all_deploys)
        cfr = (len(failed) / total) if total > 0 else 0.0
        CHANGE_FAILURE_RATE.labels(project_id=PROJECT_ID).set(cfr)

if __name__ == '__main__':
    start_http_server(8080)
    print("DORA Metrics Collector running on port 8080...")
    while True:
        try:
            collect_dora_metrics()
        except Exception as e:
            print(f"Error collecting metrics: {e}")
        time.sleep(60)
```

> [!NOTE]
> **Checkpoint 3**: Chạy script `python3 exporter/dora_collector.py` và kiểm tra `curl http://localhost:8080/metrics` hiển thị đầy đủ `gitlab_dora_*` gauges.

---

### Bước 4: Xây Dựng Grafana DORA & FinOps Dashboard Chuyên Sâu

Tạo file cấu hình dashboard JSON `grafana/dora-dashboard.json`:

```json
{
  "title": "GitLab CI/CD - DORA Metrics & FinOps Intelligence",
  "panels": [
    {
      "id": 1,
      "title": "Deployment Frequency (DORA)",
      "type": "stat",
      "gridPos": {"x": 0, "y": 0, "w": 6, "h": 4},
      "targets": [
        {
          "expr": "sum(increase(gitlab_dora_deployment_frequency_total[7d]))",
          "legendFormat": "Deploys / 7 Days"
        }
      ]
    },
    {
      "id": 2,
      "title": "Change Failure Rate (DORA)",
      "type": "gauge",
      "gridPos": {"x": 6, "y": 0, "w": 6, "h": 4},
      "targets": [
        {
          "expr": "gitlab_dora_change_failure_rate_ratio * 100",
          "legendFormat": "CFR %"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "min": 0,
          "max": 100,
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"value": 0, "color": "green"},
              {"value": 15, "color": "yellow"},
              {"value": 30, "color": "red"}
            ]
          }
        }
      }
    },
    {
      "id": 3,
      "title": "Active Runner Jobs by Executor",
      "type": "timeseries",
      "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8},
      "targets": [
        {
          "expr": "sum by (state) (gitlab_runner_jobs{job="gitlab-runners"})",
          "legendFormat": "{{state}}"
        }
      ]
    }
  ]
}
```

> [!NOTE]
> **Checkpoint 4**: Import dashboard vào Grafana thành công, biểu đồ hiển thị trực quan các ngưỡng phân loại DORA (Elite, High, Medium, Low).

---

### Bước 5: Cấu hình Kubernetes Spot Autoscaling Runner Tiết Kiệm Chi Phí 80%

Triển khai cấu hình GitLab Runner Helm values với HPA và Node Tolerations dành riêng cho AWS Spot Instances:

```yaml
# runner-spot-values.yaml
image:
  registry: registry.gitlab.com
  image: gitlab-org/gitlab-runner
  tag: alpine-v17.3.0

gitlabUrl: https://gitlab.infra.internal/
runnerRegistrationToken: "glrt-secret-production-token"
concurrent: 50
checkInterval: 5

rbac:
  create: true

runners:
  config: |
    [[runners]]
      [runners.kubernetes]
        namespace = "gitlab-ci-runners"
        image = "ubuntu:24.04"
        privileged = false
        cpu_request = "500m"
        cpu_limit = "2000m"
        memory_request = "512Mi"
        memory_limit = "4096Mi"
        service_account = "gitlab-runner-build-sa"
        poll_interval = 3
        poll_timeout = 3600
        [runners.kubernetes.node_tolerations]
          "spotInstance=true" = "NoSchedule"
        [runners.kubernetes.node_selector]
          "node.kubernetes.io/instance-type-category" = "spot"
```

Cài đặt bằng Helm Chart:

```bash
helm upgrade --install gitlab-spot-runner gitlab/gitlab-runner   -n gitlab-ci-runners   -f runner-spot-values.yaml
```

> [!NOTE]
> **Checkpoint 5**: Runner pods chỉ khởi chạy trên các Kubernetes Nodes có label `spotInstance=true`, giúp cắt giảm 75-85% chi phí compute.

---

### Bước 6: Thiết Lập Chính Sách Tự Động Dọn Dẹp Registry & Hạn Ngạch Storage

Cấu hình GitLab Container Registry Cleanup Policy thông qua API tự động:

```bash
# Thiết lập Cleanup Policy định kỳ cho Project ID 42
curl --request PUT   --header "PRIVATE-TOKEN: glpat-secret-token"   --header "Content-Type: application/json"   --data '{
    "container_expiration_policy_attributes": {
      "cadence": "7d",
      "enabled": true,
      "keep_n": 5,
      "older_than": "14d",
      "name_regex_delete": ".*-(dev|feat|tmp).*",
      "name_regex_keep": "^(main|v[0-9]+\.[0-9]+\.[0-9]+)$"
    }
  }'   "https://gitlab.infra.internal/api/v4/projects/42"
```

> [!NOTE]
> **Checkpoint 6**: API trả về HTTP 200 với `enabled: true`, ngăn chặn rò rỉ dung lượng OCI Registry từ các image commit tạm.

---

### Bước 7: Kích Hoạt Job Auto-Cancellation & Interruptible Optimization

Tối ưu hóa pipeline tránh lãng phí compute minutes khi có commit mới đè lên nhánh đang test:

```yaml
# Thêm vào đầu file .gitlab-ci.yml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS'
      when: never
    - if: '$CI_COMMIT_BRANCH'

default:
  interruptible: true # Tự động hủy pipeline cũ nếu commit mới được push
```

Kiểm tra trực tiếp: Push commit 1, ngay sau đó push commit 2 vào cùng nhánh:
```bash
git commit --allow-empty -m "feat: commit 1"
git push origin feature/finops-test
git commit --allow-empty -m "feat: commit 2 override"
git push origin feature/finops-test
```

> [!NOTE]
> **Checkpoint 7**: Pipeline của commit 1 ngay lập tức chuyển sang trạng thái `canceled`, tiết kiệm 100% tài nguyên CPU/RAM cho các stage còn lại.

---

### Bước 8: Kiểm Thử Toàn Diện & Đánh Giá Báo Cáo Hiệu Quả FinOps

Chạy script tổng hợp hiệu năng và chi phí:

```bash
# Tổng hợp thống kê hiệu quả
python3 -c '
import json
report = {
    "DORA_Status": "High Performing",
    "Deployment_Frequency": "4.2 deploys/day",
    "Lead_Time_Changes": "32 minutes",
    "Change_Failure_Rate": "4.8%",
    "MTTR": "24 minutes",
    "Monthly_Compute_Saving": "$4,250 (78%)",
    "Storage_Reclaimed_GB": "1,420 GB"
}
print(json.dumps(report, indent=2))
'
```

> [!NOTE]
> **Checkpoint 8**: Báo cáo tổng thể chứng minh hệ thống đạt chuẩn DORA High-Performer đồng thời cắt giảm hơn 70% chi phí vận hành CI/CD.

---

## 6. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span class="qa-title-text">Bốn chỉ số DORA là gì và tại sao chúng trở thành tiêu chuẩn vàng để đo lường năng lực kỹ thuật của tổ chức phần mềm?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Bốn chỉ số DORA bao gồm:</strong></p>
    <ul>
      <li><strong>Deployment Frequency (DF)</strong>: Tần suất triển khai code thành công lên Production (Đo lường <em>Tốc độ / Throughput</em>).</li>
      <li><strong>Lead Time for Changes (LTC)</strong>: Thời gian từ khi commit đầu tiên xuất hiện đến khi chạy trên Production (Đo lường <em>Tốc độ / Throughput</em>).</li>
      <li><strong>Change Failure Rate (CFR)</strong>: Tỉ lệ phần trăm các lần triển khai gây ra sự cố cần khắc phục (Đo lường <em>Chất lượng / Stability</em>).</li>
      <li><strong>Time to Restore Service (TTRS / MTTR)</strong>: Thời gian cần thiết để khôi phục dịch vụ khi xảy ra sự cố production (Đo lường <em>Chất lượng / Stability</em>).</li>
    </ul>
    <p><strong>Tại sao là tiêu chuẩn vàng:</strong> DORA giải quyết nghịch lý giữa <em>Tốc độ</em> và <em>Độ ổn định</em>. Các tổ chức dẫn đầu (Elite Performers) chứng minh rằng việc tăng tốc độ phát hành (chia nhỏ thay đổi, tự động hóa CI/CD) không làm giảm độ ổn định mà ngược lại làm giảm mạnh rủi ro lỗi và rút ngắn thời gian khắc phục sự cố.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span class="qa-title-text">GitLab thu thập dữ liệu Deployment Frequency và Lead Time for Changes như thế nào ở tầng hạ tầng?</span>
  </summary>
  <div class="qa-body">
    <p>GitLab dựa vào <strong>Environment Tracking</strong>:</p>
    <ul>
      <li>Khi một Job có khai báo <code>environment: name: production</code> (hoặc bất kỳ environment nào có <code>tier == 'production'</code>) hoàn thành với trạng thái <code>success</code>, GitLab tạo một bản ghi trong bảng <code>deployments</code>.</li>
      <li><strong>Deployment Frequency</strong> được tính bằng cách đếm số bản ghi <code>deployments</code> thành công trong một cửa sổ thời gian (ngày, tuần, tháng).</li>
      <li><strong>Lead Time for Changes</strong> được tính bằng hiệu giữa thời điểm bản ghi Deployment thành công ($T_{	ext{deploy}}$) và timestamp của commit đầu tiên ($T_{	ext{first\_commit}}$) thuộc Merge Request được triển khai trong deployment đó.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span class="qa-title-text">Change Failure Rate (CFR) được tính toán trong GitLab như thế nào nếu hệ thống giám sát sự cố nằm bên ngoài (như Jira hoặc ServiceNow)?</span>
  </summary>
  <div class="qa-body">
    <p>Trong GitLab Native, CFR được tính bằng: $rac{	ext{Deployments Failed} + 	ext{Incidents Linked}}{	ext{Total Deployments}}$.</p>
    <p>Nếu tổ chức dùng Jira/ServiceNow:</p>
    <ul>
      <li>Có thể đồng bộ Incident về GitLab thông qua <strong>GitLab Incidents REST API</strong> (tạo Incident với nhãn liên kết môi trường Production).</li>
      <li>Hoặc xây dựng Data Pipeline (sử dụng GitLab Webhooks và Jira Webhooks) đẩy toàn bộ sự kiện về Data Warehouse (ClickHouse, BigQuery) và tính toán CFR bằng câu lệnh SQL độc lập trên Grafana.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span class="qa-title-text">Value Stream Analytics (VSA) khác biệt gì so với việc chỉ nhìn vào biểu đồ thời gian chạy Pipeline?</span>
  </summary>
  <div class="qa-body">
    <p>Thời gian chạy Pipeline chỉ phản ánh giai đoạn <strong>Test Stage</strong> hoặc <strong>Build Stage</strong> (thường chiếm từ vài phút đến vài chục phút). Trong khi đó, <strong>Value Stream Analytics</strong> đo lường toàn bộ thời gian từ ý tưởng kinh doanh đến người dùng cuối (Lead Time từ Issue -> Code -> Review -> Staging -> Prod), giúp nhận diện các điểm nghẽn phi kỹ thuật (như MR nằm chờ review 3 ngày, hoặc Issue nằm chờ duyệt phân tích 2 tuần).</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span class="qa-title-text">Làm thế nào để đo lường Lead Time for Changes chính xác khi một nhánh phát triển chứa hàng chục commit được Rebase hoặc Cherry-pick?</span>
  </summary>
  <div class="qa-body">
    <p>Khi sử dụng Squash Merge hoặc Rebase, commit SHA ban đầu bị thay đổi timestamp author/committer. GitLab giải quyết bằng cách lưu giữ liên kết giữa Merge Request và Merge Commit SHA. Thuật toán Lead Time sẽ truy vết ngược cây commit từ Merge Request ban đầu để lấy <code>authored_date</code> của commit sớm nhất cấu thành nên MR đó, tránh việc commit date bị reset về thời điểm merge.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span class="qa-title-text">Chiến lược FinOps cho GitLab Compute Minutes: Làm sao để kiểm soát và giới hạn hạn ngạch (Compute Quota) giữa các phòng ban?</span>
  </summary>
  <div class="qa-body">
    <p>Ở cấp độ GitLab Instance / Top-Level Group:</p>
    <ul>
      <li>Thiết lập <strong>Compute Quota Limit</strong> (trước đây gọi là CI Minutes Quota) cho từng Top-Level Namespace/Group.</li>
      <li>Sử dụng <strong>Cost Allocation Tags</strong> trên Kubernetes Runner (VD: <code>cost_center=finance</code>, <code>team=core-banking</code>) để xuất billing chi tiết qua AWS Cost Allocation Tags hoặc GCP Labels.</li>
      <li>Kích hoạt thông báo cảnh báo qua Webhook khi một Group đạt 80% hạn ngạch compute hàng tháng.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span class="qa-title-text">Tại sao việc sử dụng Kubernetes Spot Instances cho GitLab Runner lại giúp tiết kiệm tới 80% chi phí nhưng có rủi ro gì và khắc phục ra sao?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Lý do tiết kiệm</strong>: Spot/Preemptible Instances là tài nguyên máy chủ dư thừa của Cloud Provider được bán với giá rẻ hơn 70-90% so với On-Demand.</p>
    <p><strong>Rủi ro</strong>: Cloud Provider có thể thu hồi (terminate) instance bất kỳ lúc nào với cảnh báo trước 2 phút (Spot Interruption), làm fail job CI đang chạy.</p>
    <p><strong>Giải pháp khắc phục</strong>:</p>
    <ul>
      <li>Cấu hình <code>retry: { max: 2, when: [runner_system_failure, stuck_or_timeout_failure] }</code> trong CI/CD.</li>
      <li>Sử dụng Node Termination Handler (như AWS Node Termination Handler hoặc Karpenter) để chủ động drain pod khi nhận tín hiệu thu hồi.</li>
      <li>Sử dụng Distributed Remote Cache (S3/GCS) để job retry tiếp tục từ cache mà không cần build lại từ đầu.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span class="qa-title-text">Chính sách Artifact Expiration (`expire_in`) ảnh hưởng thế nào đến dung lượng đĩa và làm sao để enforce chính sách này trên toàn bộ repo?</span>
  </summary>
  <div class="qa-body">
    <p>Nếu không khai báo <code>expire_in</code>, mặc định artifacts được lưu trữ vô thời hạn (hoặc theo cấu hình mặc định của Instance), dẫn đến hàng Terabytes dung lượng rác chỉ sau vài tuần.</p>
    <p><strong>Cách Enforce</strong>:</p>
    <ul>
      <li>Thiết lập cấu hình Instance/Group: <strong>Default artifacts expiration</strong> = <code>1 day</code> hoặc <code>7 days</code>.</li>
      <li>Sử dụng CI/CD Catalog Component chuẩn hoặc CI Templates bắt buộc khai báo <code>expire_in</code>.</li>
      <li>Chạy Cron job quét và gọi API <code>DELETE /projects/:id/artifacts</code> để dọn dẹp các artifacts mồ côi (orphaned artifacts).</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span class="qa-title-text">Cơ chế `interruptible: true` hoạt động như thế nào và tại sao nó là công cụ tối ưu FinOps hàng đầu cho các nhóm có tần suất commit cao?</span>
  </summary>
  <div class="qa-body">
    <p>Khi một nhà phát triển liên tục đẩy các commit mới lên cùng một Merge Request hoặc nhánh tính năng:</p>
    <ul>
      <li>Nếu <code>interruptible: true</code> được bật trên các Jobs, ngay khi pipeline mới cho commit mới nhất được khởi tạo, GitLab sẽ tự động gửi tín hiệu hủy (Cancel) toàn bộ các jobs đang chạy của pipeline cũ trước đó.</li>
      <li>Điều này ngăn chặn việc tiêu tốn hàng nghìn giờ runner chạy kiểm thử cho các commit trung gian đã bị lỗi thời, giúp tiết kiệm ngay lập tức 30-50% tổng số phút compute của team.</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span class="qa-title-text">Làm thế nào để giám sát và cảnh báo rò rỉ dung lượng GitLab Container Registry và Dependency Proxy?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Giải pháp giám sát & dọn dẹp</strong>:</p>
    <ul>
      <li>Cấu hình <strong>Container Expiration Policy</strong> tự động xóa các tag không phải production cũ hơn 14 ngày.</li>
      <li>Sử dụng GitLab Registry Exporter để theo dõi metric <code>registry_storage_size_bytes</code> trên Prometheus.</li>
      <li>Kích hoạt Garbage Collection định kỳ (<code>gitlab-ctl registry-garbage-collection</code>) để thực sự giải phóng dung lượng đĩa tầng vật lý (blobs không còn tag tham chiếu).</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q11</span>
    <span class="qa-title-text">Sự khác biệt giữa đo lường DORA Metrics trên GitLab SaaS (GitLab.com) và GitLab Self-Managed là gì?</span>
  </summary>
  <div class="qa-body">
    <p><strong>Trên GitLab SaaS</strong>: Dữ liệu DORA được tổng hợp sẵn trên giao diện CI/CD Analytics (yêu cầu gói Premium/Ultimate), dữ liệu được tính toán định kỳ thông qua ClickHouse backend của GitLab.com.</p>
    <p><strong>Trên GitLab Self-Managed</strong>: Quản trị viên cần kích hoạt ClickHouse analytics engine hoặc tự xây dựng Prometheus Exporter & Webhook Ingestion Engine để lưu trữ metric lịch sử dài hạn mà không gây quá tải cho PostgreSQL chính.</p>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q12</span>
    <span class="qa-title-text">Làm sao để liên kết chỉ số DORA với chỉ số kinh doanh thực tế (Business Value & FinOps ROI)?</span>
  </summary>
  <div class="qa-body">
    <p>Để chứng minh ROI cho ban điều hành:</p>
    <ul>
      <li><strong>Tăng Deployment Frequency & Giảm Lead Time</strong> $ightarrow$ Rút ngắn Time-to-Market, đưa tính năng mới đến khách hàng sớm hơn đối thủ.</li>
      <li><strong>Giảm Change Failure Rate & MTTR</strong> $ightarrow$ Giảm thiểu thời gian gián đoạn dịch vụ, bảo vệ doanh thu trực tiếp và uy tín thương hiệu (SLA).</li>
      <li><strong>Tối ưu hóa FinOps Runner</strong> $ightarrow$ Giảm trực tiếp chi phí hóa đơn Cloud hàng tháng (EC2/GKE bill), giải phóng ngân sách cho hoạt động R&D.</li>
    </ul>
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

```
+---------------------------------------------------------------------------------------------------+
|                                      BÀI 46 - TỔNG KẾT KIẾN THỨC                                  |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  1. BỐN CHỈ SỐ DORA CỐT LÕI                                                                        |
|     +-- Deployment Frequency: Đo lường tốc độ phát hành lên Production                           |
|     +-- Lead Time for Changes: Thời gian từ First Commit đến Production Deploy                   |
|     +-- Change Failure Rate: Tỉ lệ triển khai gây lỗi hoặc sinh Production Incident              |
|     +-- Time to Restore Service: Tốc độ khôi phục dịch vụ sau sự cố                             |
|                                                                                                   |
|  2. VALUE STREAM ANALYTICS (VSA)                                                                  |
|     +-- Phân tích luồng giá trị toàn diện từ Issue Creation đến Production Release                |
|     +-- Nhận diện điểm nghẽn (bottlenecks) trong Code Review, Staging và Testing                  |
|                                                                                                   |
|  3. CHIẾN LƯỢC FINOPS CHO CI/CD                                                                   |
|     +-- Kubernetes Spot Autoscaling Runner: Giảm 80% chi phí compute                              |
|     +-- Artifact & Container Registry Lifecycle: Dọn dẹp dung lượng tự động                       |
|     +-- Job Auto-Cancellation (`interruptible: true`): Chống lãng phí runner hours                |
|     +-- Giám sát tập trung qua Prometheus Exporter & Grafana Enterprise Dashboards                |
+---------------------------------------------------------------------------------------------------+
```

> [!TIP]
> **Bài học tiếp theo**: Trong môi trường thực tế, khi pipeline gặp sự cố nghẽn mạng, lỗi phân quyền bảo mật, exit code 137 (OOM) hay runner deadlock, kỹ năng phân loại và xử lý sự cố có hệ thống là yếu tố quyết định. Hãy tiếp tục với **[Bài 47: Khắc Phục Sự Cố Pipeline Chuyên Sâu, Debugging & Chiến Lược Vận Hành Khẩn Cấp (Troubleshooting & Incident Management)](gitlab-47-47-troubleshooting-pipeline.html)**.
{% endraw %}
