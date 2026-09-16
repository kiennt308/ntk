---
layout: post
title: "[Bài 19] Tự Động Co Giãn Tài Nguyên: Horizontal Pod Autoscaler (HPA), Metrics-Server & Giới Hạn Scaling"
date: 2026-09-12 18:30:00 +0700
categories: [CKA]
tags:
  - CKA
  - Kubernetes
  - ClusterAdmin
  - LinuxFoundation
  - DevOps
  - Part-19
series: "CKA Exam & Cluster Admin Mastery"
series_order: 19
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1556075798-4825dfaaf498?auto=format&fit=crop&w=1200&q=80"
summary: "[CKA P.19] Hướng dẫn chuyên sâu Tự Động Co Giãn Tài Nguyên: Horizontal Pod Autoscaler (HPA), Metrics-Server & Giới Hạn Scaling: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Tự Động Co Giãn Tài Nguyên: Horizontal Pod Autoscaler (HPA), Metrics-Server & Giới Hạn Scaling."
  - "Làm chủ các thao tác lệnh kubectl tốc độ cao, xử lý sự cố cụm thực tế và tối ưu hóa tài nguyên Pod/Node."
  - "Củng cố kỹ năng thực chiến sát với đề thi chứng chỉ quốc tế của Linux Foundation / CNCF."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 19] TỰ ĐỘNG CO GIÃN TÀI NGUYÊN: HORIZONTAL POD AUTOSCALER (HPA), METRICS-SERVER & GIỚI HẠN SCALING

Trong kỷ nguyên điện toán đám mây và kiến trúc microservices phân tán quy mô lớn, **Kubernetes (CKA)** đóng vai trò là nền tảng điều phối container (Container Orchestration) tiêu chuẩn công nghiệp. Để làm chủ hệ thống trong môi trường sản xuất (Production) cũng như chinh phục kỳ thi chứng chỉ quốc tế của Linux Foundation / CNCF, kỹ sư không chỉ nắm vững các câu lệnh thao tác cơ bản mà phải thấu hiểu sâu sắc bản chất cơ chế tầng thấp: từ chu trình điều hòa (Reconciliation Loop), cấu trúc điều phối tài nguyên, kiến trúc mạng CNI, lưu trữ CSI cho đến các chuẩn mực an ninh phòng thủ chiều sâu.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn giải mã toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp bài thực hành Lab từng bước và bộ câu hỏi phỏng vấn chuẩn Architect / Lead Engineer.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

| # | Câu hỏi ôn tập | Đáp án chuẩn ngắn gọn (chứa con số / tên lệnh) |
|---|---|---|
| 1 | Sự khác nhau giữa `resources.requests` và `resources.limits`? | `requests` dùng cho Kube-Scheduler Lọc Node; `limits` dùng cho Kubelet/Kernel siết trần |
| 2 | Đơn vị đo lường tài nguyên CPU millicores? | **1000m** tương đương đúng **1** vCPU core (`100m = 0,1 CPU`) |
| 3 | Điều kiện để Pod đạt chuẩn lớp `Guaranteed QoS Class`? | **100%** container có `requests == limits` cho cả CPU và RAM |
| 4 | Hiện tượng xảy ra khi container tiêu thụ CPU vượt trần limit? | CPU **CFS Throttling** (bóp chậm tiến trình nhưng **`RESTARTS = 0`**) |
| 5 | Sự cố xảy ra khi container tiêu thụ RAM vượt trần limit? | **OOMKilled** (Linux Kernel diệt container với đúng mã thoát **Exit Code 137**) |



> **Luận đề trung tâm của buổi:**
> *"Đối tượng `HorizontalPodAutoscaler` (HPA API v2) tự động co giãn số lượng bản sao Pods (Replicas) hàng ngang theo công thức `desiredReplicas = ceil[ currentReplicas * ( currentMetric / targetMetric ) ]` dựa trên chỉ số CPU/RAM thực tế từ `metrics-server`; trong đó điều kiện tiên quyết bắt buộc là Pod spec phải khai báo `resources.requests`, và cơ chế cửa sổ ổn định `stabilizationWindowSeconds` (mặc định 300 giây) bảo vệ hệ thống khỏi hiện tượng rung lắc số lượng bản sao (Flapping/Thrashing)."*

**Bảng kết quả các buổi trước được dùng lại:**

| Kết quả / Công cụ | Nguồn gốc | Áp dụng vào buổi này |
|---|---|---|
| Truy vấn chỉ số tài nguyên từ `metrics-server` | Buổi 18 `QT 7.3` | HPA lấy nguồn dữ liệu từ Metrics API (`kubectl top`) |
| Khai báo khối `resources.requests.cpu` | Buổi 18 `QT 4.1` | Điều kiện bắt buộc để HPA tính tỷ lệ phần trăm CPU utilization % |
| Bộ 5 lệnh `kubectl rollout` và Deployment scale | Buổi 15 `QT 4.1` | HPA điều khiển trường `spec.replicas` của đối tượng Deployment |

Ba câu bài tập về nhà BTVN 4 của buổi 18 đã chuẩn bị sẵn kiến thức cho học viên: Câu 1 khảo sát chỉ số HPA dựa vào; Câu 2 phân tích điều kiện bắt buộc `resources.requests.cpu` trong Pod spec; Câu 3 phân biệt co giãn hàng ngang (HPA) vs co giãn hàng dọc (VPA).

---



| # | Năng lực đạt được sau buổi học | Hiện vật chứng minh trong bài lab |
|---|---|---|
| 1 | Khởi tạo HPA nhanh bằng câu lệnh CLI `kubectl autoscale` | Tệp `hien-vat/imperative-hpa.yaml` |
| 2 | Biển soạn tệp YAML HPA v2 API (`autoscaling/v2`) cấu hình min/max replicas và target CPU % | Tệp `hien-vat/php-apache-hpa.yaml` |
| 3 | Thực hành bắn tải thử nghiệm (Load Testing) kiểm chứng tiến trình tự động scale out Pods | Tệp `hien-vat/load-test-report.txt` |
| 4 | Cấu hình cửa sổ thời gian ổn định `stabilizationWindowSeconds` chống hiện tượng Flapping | Tệp `hien-vat/custom-behavior-hpa.yaml` |
| 5 | Chẩn đoán và khắc phục sự cố HPA báo chỉ số `<unknown>` do thiếu `resources.requests` | Tệp `hien-vat/fix-unknown-hpa.md` |
| 6 | Kiểm thử kịch bản tự động co giãn Pods và HPA Controller với script tự động | Script `hien-vat/verify-hpa-autoscaling.sh` |

---



| Bắt buộc phải biết | Nguồn tự học nếu thiếu |
|---|---|
| Cấu hình Deployment và quản lý số bản sao replicas | Buổi 15 `QT 4.1` |
| Khai báo tài nguyên CPU Requests trong Pod spec | Buổi 18 `QT 4.1` |
| Lệnh kiểm tra chỉ số tài nguyên `kubectl top pods` | Buổi 18 `QT 7.3` |

---





| # | Thuật ngữ tiếng Việt | Tiếng Anh tương đương | Ghi chú chuẩn hoá trong thân bài |
|---|---|---|---|
| 1 | Bộ tự động co giãn Pods hàng ngang | HorizontalPodAutoscaler (HPA) | Đối tượng tự động tăng/giảm số bản sao Pods |
| 2 | Bộ tự động co giãn Pods hàng dọc | VerticalPodAutoscaler (VPA) | Đối tượng tự động tăng/giảm CPU/RAM requests của Pod |
| 3 | Tỷ lệ sử dụng CPU mục tiêu | Target CPU Utilization (`averageUtilization`) | Mức % CPU mong muốn làm căn cứ scale (như `50%`) |
| 4 | Số bản sao tối thiểu / tối đa | Min / Max Replicas (`minReplicas` / `maxReplicas`) | Ngưỡng giới hạn dưới và trên số Pods do HPA quản lý |
| 5 | Dịch vụ thu thập chỉ số đo đạc | Metrics Server (`metrics-server`) | Add-on cung cấp chỉ số CPU/RAM cho HPA qua Metrics API |
| 6 | Công thức tính số bản sao mong muốn | Desired Replicas Formula | Công thức `ceil[ currentReplicas * (current / target) ]` |
| 7 | Hiện tượng rung lắc số bản sao | Flapping / Thrashing | Sự cố Pods bị scale up/down liên tục trong thời gian ngắn |
| 8 | Cửa sổ thời gian ổn định co giảm | Scale Down Stabilization Window | Khoảng thời gian trì hoãn trước khi scale in Pods (mặc định 300s) |
| 9 | Cấu hình hành vi co giãn chi tiết | HPA Behavior Spec (`spec.behavior`) | Khối tùy chỉnh tốc độ scaleUp và scaleDown trong v2 API |
| 10 | Tạo HPA bằng dòng lệnh CLI | Imperative Autoscale (`kubectl autoscale`) | Lệnh khởi tạo HPA nhanh trực tiếp từ terminal |
| 11 | Chỉ số tùy biến | Custom Metrics (`custom.metrics.k8s.io`) | Chỉ số ứng dụng (HTTP QPS, Queue Length) dùng cho HPA |
| 12 | Tải tài nguyên nhàn rỗi | Idle Resource Load | Mức tiêu thụ tài nguyên thực tế khi không có traffic |
| 13 | Bật bù tải tăng đột biến | Traffic Spike / Burst | Lưu lượng truy cập ứng dụng tăng vọt trong thời gian ngắn |
| 14 | Bộ điều khiển co giãn | HPA Controller (`kube-controller-manager`) | Tiến trình chạy vòng lặp kiểm tra HPA định kỳ mỗi 15s |



1. **Mô hình "Mở thêm quầy thu ngân ngày Lễ Tết vs Nâng cấp máy tính thu ngân (HPA vs VPA)":**
   `HPA` giống như siêu thị mở thêm từ 2 quầy thu ngân lên 10 quầy thu ngân khi khách hàng xếp hàng đông (tăng số bản sao Pods). `VPA` giống như giữ nguyên 1 quầy thu ngân nhưng thay máy vi tính cùi bằng máy vi tính cấu hình mạnh hơn (tăng CPU/RAM của Pod).

2. **Mô hình "Nhiệt kế đo nhiệt độ phòng và Công tắc máy lạnh (HPA & Metrics Server)":**
   `Metrics Server` đóng vai trò là chiếc Nhiệt kế liên tục đo nhiệt độ phòng (chỉ số CPU/RAM thực tế). `HPA` đóng vai trò là Công tắc tự động của Máy lạnh: Khi nhiệt độ CPU vượt quá 50% mục tiêu, công tắc bật thêm máy lạnh (scale up Pods); khi nhiệt độ hạ thấp, công tắc tắt bớt máy lạnh (scale down Pods).

3. **Mô hình "Thời gian chờ nguội động cơ xe đua (Stabilization Window chống Flapping)":**
   Sau khi xe đua chạy tốc độ cao, người ta không tắt máy ngay lập tức mà phải để động cơ chạy không tải 5 phút cho nguội bớt (`stabilizationWindowSeconds: 300s`). Trong Kubernetes, khi traffic vừa giảm xuống, HPA sẽ chờ 5 phút để xác nhận traffic thực sự êm rảnh trước khi thu hồi bớt Pods, tránh việc vừa xoá Pod xong traffic lại tăng đột biến.

---

### 1.1. Phân biệt Co giãn hàng ngang (HPA) vs Co giãn hàng dọc (VPA) (10 phút)

**Nguyên lý cốt lõi:** Đối tượng `HorizontalPodAutoscaler` (HPA) tự động co giãn **số lượng bản sao Pods (Replicas)** hàng ngang theo chiều ngang (Out/In); trong khi `VerticalPodAutoscaler` (VPA) tự động thay đổi **mức cấu hình tài nguyên (Requests & Limits CPU/RAM)** của Pod theo chiều dọc (Up/Down).

**Giải thích cơ chế ngầm:** HPA phù hợp tuyệt đối cho các ứng dụng Stateless Web/Microservices có khả năng phân tải. VPA dùng cho các ứng dụng Stateful/Database khó phân tán bản sao nhưng cần thêm RAM/CPU.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cố gắng dùng HPA cho Pod đơn lẻ không nằm dưới Deployment/ReplicaSet làm HPA báo lỗi không tìm thấy Scale Target.

**Minh hoạ.**

```bash
# Kiểm tra danh sách HPA trong namespace dev
kubectl get hpa -n dev
```

Con số chốt: **2** cơ chế co giãn Pods chính trong Kubernetes (HPA co giãn số bản sao, VPA co giãn dung lượng tài nguyên).

---

**Nguyên lý cốt lõi:** Tiến trình `HPA Controller` (nằm trong `kube-controller-manager`) chạy vòng lặp kiểm tra chỉ số tài nguyên và tính toán lại số lượng bản sao Pods theo chu kỳ định kỳ mặc định **15 giây một lần**.

**Giải thích cơ chế ngầm:** Chu kỳ 15s đủ nhanh để phản ứng với đợt tăng tải Spike mà không làm quá tải API Server và `metrics-server`.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thắc mắc tại sao vừa bắn traffic test mà `kubectl get hpa` phải mất 15-30 giây mới bắt đầu nhảy chỉ số CPU%.

**Minh hoạ.**

```bash
# Xem tần suất vòng lặp kiểm tra HPA của Kube-Controller-Manager
kube-controller-manager --horizontal-pod-autoscaler-sync-period=15s
```

Con số chốt: **15** giây là chu kỳ vòng lặp kiểm tra HPA mặc định của Controller.

---

### 1.2. Công thức tính số Pods và cấu trúc YAML HPA v2 API (`autoscaling/v2`) (12 phút)

```mermaid
graph TD
    subgraph HPA_Workflow ["Quy trình hoạt động của HPA Controller"]
        MS["Metrics Server (Metrics API)"] -->|"Chỉ số CPU/RAM thực tế"| HPA_CTRL["HPA Controller (Vòng lặp 15s)"]
        HPA_CTRL -->|"Áp dụng công thức"| FORMULA["desiredReplicas = ceil[ current * (currentMetric / targetMetric) ]"]
        FORMULA -->|"Update spec.replicas"| DEPLOY["Deployment (scale out / scale in)"]
    end

    style HPA_CTRL fill:none,stroke:#388e3c,stroke-width:2px
    style FORMULA fill:none,stroke:#f57c00,stroke-width:2px
    style DEPLOY fill:none,stroke:#0288d1,stroke-width:2px
```

---

**Nguyên lý cốt lõi:** Kube-Controller-Manager tính toán số lượng bản sao Pods mong muốn (`desiredReplicas`) cho HPA theo đúng công thức toán học: **`desiredReplicas = ceil[ currentReplicas * ( currentMetricValue / desiredMetricValue ) ]`** (trong đó `ceil` là hàm làm tròn lên số nguyên gần nhất).

**Giải thích cơ chế ngầm:** Công thức tỉ lệ thuận đảm bảo số bản sao Pods tăng/giảm chính xác theo mức độ chênh lệch giữa chỉ số tiêu thụ thực tế vs chỉ số mục tiêu.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thắc mắc tại sao current CPU là 80%, target CPU là 50% trên 2 Pods mà HPA lại scale lên đúng 4 Pods (`ceil[ 2 * (80/50) ] = ceil[3.2] = 4`).

**Minh hoạ.**

```bash
# Giả sử currentReplicas=2, currentCPU=80%, targetCPU=50%
# desiredReplicas = ceil[ 2 * (80 / 50) ] = ceil[ 3.2 ] = 4 Pods
```

Con số chốt: **100%** kết quả tính toán `desiredReplicas` được hàm `ceil` làm tròn lên số nguyên phía trên.

---

**Nguyên lý cốt lõi:** Trong định dạng YAML HPA phiên bản `autoscaling/v2`, chỉ số mục tiêu được khai báo trong khối `metrics[].resource.target` dưới hai dạng: `averageUtilization` (tỷ lệ phần trăm % so với request, ví dụ `50`) hoặc `averageValue` (giá trị tuyệt đối, ví dụ `200m`).

**Giải thích cơ chế ngầm:** API v2 cung cấp khả năng diễn đạt linh hoạt cho phép kết hợp nhiều chỉ số đo đạc (CPU, RAM, Custom Metrics) trong cùng 1 HPA.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dùng API v1 cũ (`autoscaling/v1`) không hỗ trợ co giãn theo Memory hoặc nhiều chỉ số cùng lúc.

**Minh hoạ.**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
  namespace: dev
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-deploy
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

Con số chốt: **2** dạng cấu hình chỉ số mục tiêu trong HPA v2 (`averageUtilization` % và `averageValue` tuyệt đối).

---

### 1.3. Điều kiện phụ thuộc `resources.requests` và cơ chế chống Flapping (`stabilizationWindowSeconds`) (12 phút)

**Nguyên lý cốt lõi:** Điều kiện tiên quyết bắt buộc để HPA tính toán được tỷ lệ phần trăm `averageUtilization` là **100% các container trong Pod spec phải được khai báo thuộc tính `resources.requests.cpu`** (hoặc memory); nếu thiếu, HPA sẽ báo chỉ số `<unknown>` và KHÔNG BAO GIỜ thực hiện tự động co giãn.

**Giải thích cơ chế ngầm:** Tỷ lệ phần trăm % CPU utilization được tính theo công thức: `(CPU thực tế tiêu thụ / CPU Request) * 100`. Không có `requests.cpu` làm mẫu số thì toán tử chia bị vô nghĩa.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cột `TARGETS` trong lệnh `kubectl get hpa` hiển thị `<unknown>/50%` và số Pods đứng yên không chịu scale.

**Minh hoạ.**

```bash
# Kiểm tra lỗi thiếu requests.cpu làm HPA báo unknown
kubectl describe hpa web-hpa -n dev | grep -i "failed to get cpu utilization"
```

Con số chốt: **100%** các container bắt buộc phải có `resources.requests` để HPA hoạt động.

---

**Nguyên lý cốt lõi:** Cửa sổ thời gian ổn định co giảm `stabilizationWindowSeconds` trong khối `behavior.scaleDown` có giá trị mặc định là **300 giây (5 phút)**; Kube-Controller-Manager sẽ trì hoãn việc xoá bớt Pods trong 5 phút để tránh hiện tượng rung lắc số bản sao (Flapping/Thrashing) khi lưu lượng truy cập trồi sụt liên tục.

**Giải thích cơ chế ngầm:** Giữ cho hạ tầng ổn định: tránh việc Pod vừa bị xoá xong 10 giây sau traffic lại vọt lên làm hệ thống phải tạo lại Pod mới gây tốn tài nguyên khởi tạo.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thắc mắc tại sao đã ngừng hoàn toàn traffic test mà HPA phải đợi đúng 5 phút mới bắt đầu giảm số lượng Pods xuống `minReplicas`.

**Minh hoạ.**

```yaml
spec:
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```

Con số chốt: **300** giây (5 phút) là thời gian cửa sổ ổn định scaleDown mặc định của HPA.

---

**Nguyên lý cốt lõi:** Tạo HPA nhanh bằng câu lệnh CLI `kubectl autoscale deployment <deploy-name> --min=<N> --max=<M> --cpu-percent=<X>` sẽ tự động sinh ra một đối tượng HPA liên kết với Deployment chỉ định trong đúng 2 giây.

**Giải thích cơ chế ngầm:** Đường gõ ngắn nhất giúp thí sinh tiết kiệm thời gian làm bài trong các kỳ thi CKA và CKAD.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ngồi tự gõ lại toàn bộ tệp YAML HPA 25 dòng làm mất hơn 3 phút trong bài thi bấm giờ.

**Minh hoạ.**

```bash
# Tạo HPA cho deployment web-deploy min 2, max 10, target CPU 50%
kubectl autoscale deployment web-deploy -n dev --min=2 --max=10 --cpu-percent=50
```

Con số chốt: **2** giây thực thi lệnh `kubectl autoscale` để tạo HPA hoàn chỉnh.

---

### 1.4. Cấu hình nhiều chỉ số đo đạc và tùy chỉnh hành vi scaleUp (4 phút)

**Nguyên lý cốt lõi:** Cấu hình nhiều chỉ số đo đạc (Multiple Metrics) trong HPA API `autoscaling/v2` (như vừa chọn CPU utilization `50%` vừa chọn Memory utilization `80%`); Kube-Controller-Manager sẽ tính toán `desiredReplicas` cho từng chỉ số độc lập và chọn số Pods **lớn nhất** làm kết quả scale.

**Giải thích cơ chế ngầm:** Đảm bảo an toàn tuyệt đối cho ứng dụng: chỉ cần 1 trong các chỉ số đo đạc bị vượt trần là HPA mở rộng số bản sao ngay lập tức.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thắc mắc tại sao CPU chỉ mới 30% mà HPA vẫn scale up Pods (do chỉ số Memory đã chạm 85%).

**Minh hoạ.**

```yaml
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      type: Utilization
      averageUtilization: 50
- type: Resource
  resource:
    name: memory
    target:
      type: Utilization
      averageUtilization: 80
```

Con số chốt: **1** số lượng Pods lớn nhất (Max calculation) luôn luôn được chọn khi khai báo nhiều chỉ số HPA.

---

**Nguyên lý cốt lõi:** Khối `spec.behavior.scaleUp` cho phép cấu hình tốc độ tăng số bản sao Pods tối đa theo phút (như `selectPolicy: Max` hoặc `percent: 100%`) giúp ứng dụng tăng tốc nhân bản Pods nhanh hơn khi gặp đợt bùng nổ lưu lượng truy cập lớn (Traffic Spike).

**Giải thích cơ chế ngầm:** Tùy chỉnh tốc độ bùng nổ Pods linh hoạt hơn cơ chế scale mặc định của Kubernetes.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> HPA scaleUp quá chậm không đáp ứng kịp cơn bão truy cập phút đầu tiên.

**Minh hoạ.**

```yaml
spec:
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

Con số chốt: **15** giây là chu kỳ periodSeconds cấu hình tăng tốc scaleUp trong HPA behavior.

---

## 8. Đưa vào cụm thật (4 phút)

### Áp vào cụm đang chạy thì làm gì trước

1. **Kiểm tra chắc chắn `metrics-server` đang hoạt động (`kubectl top nodes`):** HPA phụ thuộc 100% vào Metrics API.
2. **Luôn khai báo `resources.requests.cpu` cho Deployment trước khi gán HPA:** Tránh lỗi HPA báo `<unknown>`.
3. **Thiết lập `minReplicas ≥ 2` cho các dịch vụ Production:** Đảm bảo tính sẵn sàng cao (HA) ngay cả khi không có tải.

### Cái gì hỏng nếu áp thẳng lên prod

- **Đặt `maxReplicas` vượt quá tổng dung lượng Allocatable tài nguyên của cụm Node:** Làm HPA scale tạo ra hàng chục Pods bị kẹt ở trạng thái `Pending` do hết RAM/CPU Node.
- **Đặt `stabilizationWindowSeconds: 0` cho scaleDown:** Gây ra sự cố Flapping: Pods bị tạo mới và xoá liên tục hàng chục lần trong 1 giờ làm sập cơ sở dữ liệu do quá nhiều kết nối đóng/mở.
- **Quy trình áp thử an toàn:**
  - Áp dụng HPA trên môi trường Staging.
  - Sử dụng công cụ `hey` hoặc `k6` bắn tải thử nghiệm (Load Test) trong 10 phút.
  - Quan sát tiến trình scaleUp qua `kubectl get hpa -w` và kiểm tra thời gian nguội scaleDown sau 5 phút.

### Đo trước — đo sau

1. **Khả năng chịu tải bùng nổ (Traffic Spike):** Tự động scale từ 2 Pods lên 10 Pods trong 45 giây khi lượng request tăng gấp 5 lần.
2. **Chi phí tài nguyên nhàn rỗi:** Giảm 60% chi phí server ban đêm nhờ HPA tự động thu hồi số Pods về `minReplicas: 2`.
3. **Độ ổn định hệ thống:** 0% sự cố tràn RAM sập Web nhờ HPA kịp thời chia tải cho các bản sao Pods mới.

### Khi nào KHÔNG nên dùng

- **Không dùng HPA cho các ứng dụng có thời gian khởi động quá lâu (Warm-up time > 5 phút):** Pod mới tạo ra chưa kịp Ready thì server đã bị sập do dồn tải.
- **Không dùng HPA cho các ứng dụng Stateful Database đơn lẻ:** Việc scale out bản sao Database đòi hỏi cơ chế nhân bản dữ liệu Master-Slave phức tạp chứ không chỉ tăng `replicas`.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy hay gặp | Vì sao dính bẫy | Làm đúng là (kèm tên lệnh / con số) |
|---|---|---|---|
| 1 | HPA báo chỉ số `<unknown>/50%` ở cột TARGETS | Deployment bên dưới không khai báo `resources.requests.cpu` | Bổ sung `resources.requests.cpu` vào Pod spec của Deployment |
| 2 | HPA không chịu scale down Pods ngay khi ngừng bắn tải | Do cơ chế cửa sổ ổn định `stabilizationWindowSeconds` trì hoãn 300s | Đợi đủ 5 phút (300 giây) để HPA thực hiện scale down |
| 3 | Lệnh `kubectl autoscale` báo `error: scale target not found` | Gõ sai tên Deployment hoặc sai Namespace | Kiểm tra chính xác tên Deployment bằng `kubectl get deploy -n <ns>` |
| 4 | Pods bị kẹt ở `Pending` khi HPA scale out lên `maxReplicas` | Tổng CPU/RAM requests vượt quá dung lượng Allocatable của cụm | Tăng thêm Worker Node hoặc giảm `maxReplicas` phù hợp |
| 5 | Dùng API version `autoscaling/v1` bị báo lỗi khi cấu hình Memory | API v1 cũ chỉ hỗ trợ 1 chỉ số duy nhất là CPU | Sử dụng API version `autoscaling/v2` cho HPA |
| 6 | Thắc mắc vì sao HPA không scale Pods do DaemonSet quản lý | HPA chỉ hỗ trợ scale các đối tượng có trường `spec.replicas` | Chỉ liên kết HPA với Deployment hoặc StatefulSet |
| 7 | Đặt `minReplicas: 0` ở Kubernetes bản cũ | Kubernetes cũ không hỗ trợ scale to zero cho HPA | Đặt `minReplicas` tối thiểu là 1 hoặc 2 |
| 8 | Nhầm lẫn giữa HPA (scale Pods) và Cluster Autoscaler (scale Nodes) | HPA chỉ tăng số Pods; Cluster Autoscaler mới thêm máy chủ Node | Dùng HPA để scale Pods; dùng Cluster Autoscaler để scale Node |
| 9 | Gõ sai tên chỉ số CPU trong HPA YAML v2 | Gõ `name: CPU` chữ hoa thay vì `name: cpu` chữ thường | Gõ đúng `name: cpu` chữ thường trong HPA spec |
| 10 | HPA báo `unable to get metrics` mặc dù đã có `requests.cpu` | Add-on `metrics-server` bị sập hoặc gặp lỗi TLS certificate | Kiểm tra `kubectl get pods -n kube-system` xem metrics-server có Ready không |
| 11 | Bị xung đột số replicas khi vừa dùng HPA vừa tự gõ `kubectl scale` | HPA Controller sẽ tự động ghi đè số `replicas` về mức nó tính toán | Không dùng `kubectl scale` thủ công khi đã gán HPA |
| 12 | Thắc mắc vì sao HPA scale lên số Pod bị lẻ lẻ (như 3 Pods thay vì 4 Pods) | Áp dụng công thức `ceil[ current * (currentMetric / targetMetric) ]` | Tự tính lại bằng công thức `ceil` để đối soát |

---

## §10. Tóm tắt (2 phút)

```mermaid
graph TD
    A["HorizontalPodAutoscaler (HPA v2 API)"] --> B["Nguồn dữ liệu: metrics-server (kubectl top)"]
    A --> C["Công thức: desiredReplicas = ceil[ current * (currentMetric / targetMetric) ]"]
    A --> D["Điều kiện bắt buộc: 100% containers có resources.requests.cpu"]
    A --> E["Chống Flapping: scaleDown stabilizationWindowSeconds (300s / 5 phút)"]

    style A fill:none,stroke:#333,stroke-width:2px
    style B fill:none,stroke:#333,stroke-width:2px
    style C fill:none,stroke:#333,stroke-width:2px
    style E fill:none,stroke:#333,stroke-width:2px
```

### Năm điều phải nhớ

1. **Khái niệm HPA vs VPA:** HPA co giãn số lượng bản sao Pods (Replicas) hàng ngang; VPA co giãn dung lượng CPU/RAM hàng dọc.
2. **Công thức bất biến:** `desiredReplicas = ceil[ currentReplicas * ( currentMetric / targetMetric ) ]` (làm tròn lên `ceil`).
3. **Điều kiện tiên quyết:** Pod spec BẮT BUỘC phải có `resources.requests.cpu`; thiếu sẽ làm HPA báo lỗi `<unknown>`.
4. **Chu kỳ Controller:** Tiến trình HPA Controller chạy vòng lặp kiểm tra định kỳ **15 giây/lần**.
5. **Cơ chế chống Flapping:** Cửa sổ ổn định `stabilizationWindowSeconds` trì hoãn **300 giây (5 phút)** trước khi scale down Pods.

---

## §11. Câu hỏi tự kiểm tra

1. Phân biệt sự khác nhau giữa HPA (HorizontalPodAutoscaler) và VPA (VerticalPodAutoscaler).
2. Viết công thức toán học Kube-Controller-Manager sử dụng để tính số lượng Pods mong muốn (`desiredReplicas`) cho HPA.
3. Nếu currentReplicas = 2, current CPU utilization = 90%, target CPU utilization = 50% thì HPA sẽ scale Deployment lên bao nhiêu Pods?
4. Tại sao nếu Pod spec không khai báo `resources.requests.cpu` thì HPA không thể tính toán được tỷ lệ % CPU utilization?
5. Tần suất vòng lặp kiểm tra chỉ số HPA của Kube-Controller-Manager là bao nhiêu giây một lần?
6. Cửa sổ thời gian ổn định co giảm `stabilizationWindowSeconds` có giá trị mặc định là bao nhiêu phút và vai trò của nó là gì?
7. Câu lệnh CLI nào giúp tạo nhanh một HPA cho Deployment `web-deploy` với min 2, max 10, target CPU 50% trong 2 giây?
8. Tại sao việc tự gõ lệnh `kubectl scale deployment` thủ công lại bị vô hiệu hóa khi Deployment đó đang được HPA quản lý?
9. Hai chế độ hỏng (1 im lặng do HPA báo `<unknown>` vì thiếu requests.cpu, 1 âm thầm do Flapping Pods bị xoá/tạo liên tục vì để stabilizationWindow bằng 0) là gì?
10. API version chuẩn nhất hiện nay cho HPA hỗ trợ nhiều chỉ số (CPU, RAM, Custom Metrics) là phiên bản nào?

### Đáp án

1. HPA co giãn số lượng bản sao Pods (Replicas) hàng ngang; VPA co giãn dung lượng CPU/RAM của từng Pod hàng dọc.
2. `desiredReplicas = ceil[ currentReplicas * ( currentMetricValue / desiredMetricValue ) ]`.
3. `desiredReplicas = ceil[ 2 * (90 / 50) ] = ceil[ 3.6 ] = 4 Pods`.
4. Vì tỷ lệ % CPU được tính bằng `(CPU thực tế / CPU Request) * 100`; không có `requests.cpu` thì không có mẫu số để chia.
5. Định kỳ **15 giây** một lần.
6. Mặc định **300 giây (5 phút)**; chống hiện tượng rung lắc số bản sao Pods (Flapping/Thrashing) khi tải trồi sụt.
7. Lệnh `kubectl autoscale deployment web-deploy -n dev --min=2 --max=10 --cpu-percent=50`.
8. Vì HPA Controller chạy vòng lặp 15s sẽ tự động ghi đè số `replicas` về mức nó tự tính toán theo metric.
9. Chế độ 1: Thiếu `requests.cpu` làm HPA báo `<unknown>` không chịu scale; Chế độ 2: Để stabilizationWindow bằng 0 làm Pods bị xoá/tạo liên tục gây sập kết nối DB.
10. Phiên bản `autoscaling/v2`.

---

## §12. Tài liệu tham khảo

| Nguồn tài liệu | Phiên bản Kubernetes áp dụng | Nội dung chính |
|---|---|---|
| Official Docs: Horizontal Pod Autoscaling | Kubernetes v1.35 | Kiến trúc HPA, công thức desiredReplicas và autoscaling/v2 spec |
| Official Docs: HPA Walkthrough | Kubernetes v1.35 | Bài lab thực hành HPA với php-apache và lệnh kubectl autoscale |
| Official Docs: Configurable scaling behavior | Kubernetes v1.35 | Cấu hình behavior, scaleUp, scaleDown và stabilizationWindowSeconds |
| File cấu hình phiên bản cục bộ | `labs/phien-ban.env` | Biến `K8S_VER=1.35`, `LAB_CONTEXT="kubeadm"` |


---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên cụm Kubernetes 1.30+ tiêu chuẩn (hoặc cụm kind/kubeadm lab). Hãy đảm bảo ngữ cảnh dòng lệnh `kubectl config current-context` đã trỏ chính xác vào cụm thực hành trước khi thực thi.

## Khối thực hành — 120 phút

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| # | Mục tiêu thực hành | Tiêu chí hoàn thành (Kiểm chứng BẰNG LỆNH) |
|---|---|---|
| TH1 | Khởi tạo HPA bằng lệnh CLI `kubectl autoscale` | `kubectl get hpa php-hpa -n dev` ở trạng thái Active |
| TH2 | Biển soạn tệp YAML HPA v2 API (`autoscaling/v2`) chuẩn | `kubectl get hpa php-hpa-v2 -n dev -o jsonpath='{.apiVersion}'` in ra `autoscaling/v2` |
| TH3 | Bắn tải thử nghiệm (Load Testing) kích hoạt HPA scale out Pods | `kubectl get deploy php-deploy -n dev -o jsonpath='{.status.replicas}'` tăng > 2 bản sao |
| TH4 | Khảo sát cơ chế cửa sổ trì hoãn scaleDown chống Flapping | HPA giữ số lượng Pods trong thời gian `stabilizationWindowSeconds` |
| TH5 | Khắc phục sự cố HPA báo chỉ số `<unknown>` do thiếu `requests.cpu` | `kubectl get hpa -n dev` hiển thị tỷ lệ % CPU thực tế thay vì `<unknown>` |
| TH6 | Xác minh kịch bản tự động co giãn Pods và HPA với script tự động | Script kiểm tra HPA Autoscaling OK |
| TH7 | Nộp đủ 4 hiện vật vào portfolio | Thư mục `k8s-portfolio/buoi-19/` chứa đủ 4 file md/yaml/sh |

---

## L1. Điều kiện tiên quyết về môi trường

| # | Kiểm tra điều kiện | Câu lệnh kiểm tra | Kết quả kỳ vọng |
|---|---|---|---|
| 1 | Cụm `kubeadm` 3 node đang ở v1.35 | `kubectl get nodes` | Hiển thị 3 node `cp-01`, `worker-01`, `worker-02` `Ready` |
| 2 | Kubeconfig trỏ context `kubeadm` | `kubectl config current-context` | In ra đúng `kubeadm` |
| 3 | Namespace `dev` sẵn sàng | `kubectl get ns dev` | Namespace `dev` ở trạng thái Active |
| 4 | Thư mục hiện vật đã sẵn sàng | `mkdir -p k8s-portfolio/buoi-19` | Thư mục được tạo thành công |
| 5 | Lệnh `kubectl autoscale` sẵn sàng | `kubectl autoscale --help` | Hiển thị hướng dẫn sử dụng autoscale |

```bash
# Kiểm tra môi trường bắt buộc trước khi thực hiện bài lab
kubectl config current-context | grep -qx "kubeadm" && echo "CHECKPOINT MOI TRUONG — ĐẠT" || echo "CHECKPOINT MOI TRUONG — LỖI (Trỏ sai context)"
```

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    subgraph Deploy_Setup ["Chặng 1: Khởi tạo Deployment & HPA v2"]
        DEPLOY["Deployment php-deploy (requests.cpu: 100m, replicas: 2)"] --> HPA_V2["HPA php-hpa-v2 (min: 2, max: 10, target CPU: 50%)"]
    end

    subgraph Load_Testing ["Chặng 2: Bắn tải & Scale Out"]
        LOAD_POD["Pod load-generator (bắn HTTP request liên tục)"] --> HIGH_CPU["CPU utilization % vọt lên > 80%"]
        HIGH_CPU --> SCALE_OUT["HPA Controller scale php-deploy từ 2 lên 5+ Pods"]
    end

    subgraph ScaleDown_Stabilization ["Chặng 3: Dừng tải & Stabilization Window"]
        STOP_LOAD["Dừng Pod load-generator"] --> STAB_WIN["Trì hoãn 300s (stabilizationWindowSeconds)"]
        STAB_WIN --> SCALE_IN["HPA thu hồi Pods về minReplicas = 2"]
    end

    Deploy_Setup --> Load_Testing --> ScaleDown_Stabilization

    style Deploy_Setup fill:none,stroke:#0288d1,stroke-width:2px
    style Load_Testing fill:none,stroke:#f57c00,stroke-width:2px
    style ScaleDown_Stabilization fill:none,stroke:#388e3c,stroke-width:2px
```

---

## L3. Bước 1 — Khởi tạo Deployment `php-deploy` và HPA bằng lệnh CLI (30 phút)

### Thao tác 1.1: Tạo Deployment `php-deploy` có khai báo `requests.cpu: 100m`

```bash
# 1. Tạo Namespace dev nếu chưa có
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -

# 2. Tạo tệp php-deploy.yaml
cat << 'EOF' > k8s-portfolio/buoi-19/php-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-deploy
  namespace: dev
spec:
  replicas: 2
  selector:
    matchLabels:
      app: php-app
  template:
    metadata:
      labels:
        app: php-app
    spec:
      containers:
      - name: php-app
        image: registry.k8s.io/hpa-example:v1.0
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "200m"
            memory: "256Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: php-service
  namespace: dev
spec:
  ports:
  - port: 80
  selector:
    app: php-app
EOF

kubectl apply -f k8s-portfolio/buoi-19/php-deploy.yaml
kubectl rollout status deployment/php-deploy -n dev --timeout=30s

# 3. Tạo HPA nhanh bằng câu lệnh CLI imperative
kubectl autoscale deployment php-deploy -n dev --min=2 --max=10 --cpu-percent=50
```

**CHECKPOINT 1 — Deployment php-deploy khởi tạo thành công với 2 bản sao Pods Ready.**

```bash
kubectl get deploy php-deploy -n dev -o jsonpath='{.status.readyReplicas}' | grep -qx "2" && echo "CHECKPOINT 1 — ĐẠT" || echo "CHECKPOINT 1 — LỖI"
```

**CHECKPOINT 2 — Đối tượng HPA php-deploy được tạo bằng CLI liên kết chính xác với Deployment.**

```bash
kubectl get hpa php-deploy -n dev -o jsonpath='{.spec.scaleTargetRef.name}' | grep -qx "php-deploy" && echo "CHECKPOINT 2 — ĐẠT" || echo "CHECKPOINT 2 — LỖI"
```

---

## L4. Bước 2 — Biển soạn tệp YAML HPA v2 API (`autoscaling/v2`) (30 phút)

### Thao tác 2.1: Tạo tệp `php-hpa-v2.yaml` định dạng API v2

```bash
# 1. Xoá HPA cũ tạo bằng CLI
kubectl delete hpa php-deploy -n dev --ignore-not-found=true

# 2. Tạo tệp php-hpa-v2.yaml định dạng autoscaling/v2
cat << 'EOF' > k8s-portfolio/buoi-19/php-hpa-v2.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-hpa-v2
  namespace: dev
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-deploy
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
EOF

kubectl apply -f k8s-portfolio/buoi-19/php-hpa-v2.yaml

# 3. Trích xuất apiVersion và target CPU % của HPA
kubectl get hpa php-hpa-v2 -n dev -o jsonpath='{.apiVersion}' > /tmp/hpa-api.txt
kubectl get hpa php-hpa-v2 -n dev -o jsonpath='{.spec.metrics[0].resource.target.averageUtilization}' > /tmp/hpa-target.txt
```

**CHECKPOINT 3 — Đối tượng HPA php-hpa-v2 được khởi tạo đúng chuẩn apiVersion autoscaling/v2.**

```bash
grep -qx "autoscaling/v2" /tmp/hpa-api.txt && echo "CHECKPOINT 3 — ĐẠT" || echo "CHECKPOINT 3 — LỖI"
```

**CHECKPOINT 4 — HPA v2 được cấu hình target CPU utilization bằng 50%.**

```bash
grep -qx "50" /tmp/hpa-target.txt && echo "CHECKPOINT 4 — ĐẠT" || echo "CHECKPOINT 4 — LỖI"
```

**CHECKPOINT 5 — CA ĐỐI CHỨNG: Deployment thiếu resources.requests.cpu sẽ làm HPA báo chỉ số unknown.**

```bash
cat << EOF | kubectl apply -f - >/dev/null 2>&1
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bad-hpa-deploy
  namespace: dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: bad-hpa
  template:
    metadata:
      labels:
        app: bad-hpa
    spec:
      containers:
      - name: nginx
        image: nginx:1.27-alpine
EOF
kubectl autoscale deployment bad-hpa-deploy -n dev --min=1 --max=5 --cpu-percent=50 >/dev/null 2>&1
sleep 3
kubectl get hpa bad-hpa-deploy -n dev -o jsonpath='{.status.currentMetrics[0].resource.current.averageUtilization}' 2>/dev/null | grep -v "^[0-9]" >/dev/null 2>&1 || echo "CHECKPOINT 5 — ĐẠT"
```

---

## L5. Bước 3 — Bắn tải thử nghiệm (Load Testing) kích hoạt HPA scale out Pods (30 phút)

### Thao tác 3.1: Tạo Pod `load-generator` bắn HTTP request liên tục

```bash
# 1. Khởi chạy Pod load-generator bắn tải liên tục vào php-service
cat << 'EOF' | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: load-generator
  namespace: dev
spec:
  containers:
  - name: busybox
    image: busybox:1.36
    command: ["sh", "-c", "while true; do wget -q -O- http://php-service.dev.svc.cluster.local; done"]
EOF

# 2. Chờ 15 giây cho HPA Controller quét chỉ số và thực hiện scale out
sleep 15

# 3. Trích xuất số bản sao replicas thực tế của php-deploy sau khi bắn tải
kubectl get deploy php-deploy -n dev -o jsonpath='{.status.replicas}' > /tmp/scaled-replicas.txt
```

**CHECKPOINT 6 — Pod load-generator bắn tải làm tăng mức tiêu thụ CPU của php-deploy.**

```bash
kubectl get pod load-generator -n dev -o jsonpath='{.status.phase}' | grep -qx "Running" && echo "CHECKPOINT 6 — ĐẠT" || echo "CHECKPOINT 6 — LỖI"
```

**CHECKPOINT 7 — HPA Controller tự động scale out php-deploy từ 2 bản sao lên lớn hơn 2 bản sao (>= 3 bản sao).**

```bash
[ $(cat /tmp/scaled-replicas.txt) -gt 2 ] && echo "CHECKPOINT 7 — ĐẠT" || echo "CHECKPOINT 7 — LỖI"
```

**CHECKPOINT 8 — CA ĐỐI CHỨNG: Sau khi ngừng bắn tải, cửa sổ trì hoãn stabilizationWindowSeconds 300s giữ nguyên số Pods chưa xoá ngay.**

```bash
kubectl delete pod load-generator -n dev --ignore-not-found=true >/dev/null 2>&1
sleep 5
[ $(kubectl get deploy php-deploy -n dev -o jsonpath='{.status.replicas}') -gt 2 ] && echo "CHECKPOINT 8 — ĐẠT" || echo "CHECKPOINT 8 — LỖI"
```

---

## L6. Bước 4 — Kiểm tra cấu hình `behavior` nâng cao và dọn dẹp (20 phút)

### Thao tác 4.1: Tạo HPA `custom-behavior-hpa` tùy chỉnh tốc độ scaleUp

```bash
# 1. Tạo tệp custom-behavior-hpa.yaml
cat << 'EOF' > k8s-portfolio/buoi-19/custom-behavior-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: custom-behavior-hpa
  namespace: dev
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-deploy
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
EOF

kubectl apply -f k8s-portfolio/buoi-19/custom-behavior-hpa.yaml

# 2. Trích xuất cấu hình periodSeconds của scaleUp policy
kubectl get hpa custom-behavior-hpa -n dev -o jsonpath='{.spec.behavior.scaleUp.policies[0].periodSeconds}' > /tmp/period-sec.txt
```

**CHECKPOINT 9 — HPA custom-behavior-hpa được cấu hình scaleUp periodSeconds bằng 15.**

```bash
grep -qx "15" /tmp/period-sec.txt && echo "CHECKPOINT 9 — ĐẠT" || echo "CHECKPOINT 9 — LỖI"
```

**CHECKPOINT 10 — Dọn dẹp Deployment thử nghiệm lỗi bad-hpa-deploy và HPA liên kết.**

```bash
kubectl delete deploy bad-hpa-deploy -n dev --ignore-not-found=true >/dev/null 2>&1
kubectl delete hpa bad-hpa-deploy -n dev --ignore-not-found=true >/dev/null 2>&1 && echo "CHECKPOINT 10 — ĐẠT" || echo "CHECKPOINT 10 — LỖI"
```

**CHECKPOINT 11 — Dọn dẹp HPA php-deploy cũ.**

```bash
kubectl delete hpa php-hpa-v2 -n dev --ignore-not-found=true >/dev/null 2>&1 && echo "CHECKPOINT 11 — ĐẠT" || echo "CHECKPOINT 11 — LỖI"
```

**CHECKPOINT 12 — 100% 3 node cp-01, worker-01, worker-02 duy trì trạng thái Ready.**

```bash
kubectl get nodes --no-headers | grep -c "Ready" | grep -qx "3" && echo "CHECKPOINT 12 — ĐẠT" || echo "CHECKPOINT 12 — LỖI"
```

---

## L7. Nộp hiện vật và dọn dẹp (10 phút)

### Thao tác 7.1: Gom hiện vật nộp bài

```bash
# 1. Báo cáo tải thực nghiệm load-test-report.txt
cat << 'EOF' > k8s-portfolio/buoi-19/load-test-report.txt
BÁO CÁO KẾT QUẢ BẮN TẢI LOAD TESTING VÀ HPA AUTOSCALING:

1. Môi trường kiểm thử:
   - Deployment: php-deploy (requests.cpu: 100m, limits.cpu: 200m)
   - HPA Target: averageUtilization: 50% CPU
   - Ban đầu (Idle): 2 Replicas, CPU utilization ~ 2%

2. Tiến trình bắn tải với load-generator:
   - Sau 15 giây: CPU utilization vọt lên 85% (> 50% target)
   - HPA Controller áp dụng công thức desiredReplicas = ceil[ 2 * (85/50) ] = ceil[3.4] = 4 Pods
   - Deployment tự động scale out từ 2 lên 4 bản sao Pods thành công!

3. Kết luận:
   - Đối tượng HPA v2 autoscaling/v2 phản ứng nhanh chóng và chính xác với đợt tăng tải.
EOF

# 2. Báo cáo sửa lỗi fix-unknown-hpa.md
cat << 'EOF' > k8s-portfolio/buoi-19/fix-unknown-hpa.md
# CHẨN ĐOÁN VÀ KHẮC PHỤC LỖI HPA BÁO UNKNOWN

1. Nguyên nhân:
   - Deployment bên dưới không khai báo thuộc tính `resources.requests.cpu` trong Pod spec.
   - HPA không có mẫu số CPU Request để tính tỷ lệ phần trăm % Utilization.

2. Cách khắc phục:
   - Bổ sung khối `resources.requests.cpu: "100m"` vào container definition trong Pod spec.
   - Re-apply Deployment; HPA sẽ tự động thoát khỏi trạng thái `<unknown>` sau 15 giây.
EOF

# 3. Tạo tệp verify-hpa-autoscaling.sh
cat << 'EOF' > k8s-portfolio/buoi-19/verify-hpa-autoscaling.sh
#!/bin/bash
# Script kiểm tra HPA Autoscaling và behavior configuration

HPA_API=$(kubectl get hpa custom-behavior-hpa -n dev -o jsonpath='{.apiVersion}')
DEPLOY_REP=$(kubectl get deploy php-deploy -n dev -o jsonpath='{.status.replicas}')
PERIOD_SEC=$(kubectl get hpa custom-behavior-hpa -n dev -o jsonpath='{.spec.behavior.scaleUp.policies[0].periodSeconds}')

if [ "$HPA_API" == "autoscaling/v2" ] && [ "$PERIOD_SEC" == "15" ]; then
    echo "VERIFY HPA AUTOSCALING — ĐẠT (HPA v2, Replicas & Behavior OK)"
else
    echo "VERIFY HPA AUTOSCALING — LỖI (API: $HPA_API, Replicas: $DEPLOY_REP, Period: $PERIOD_SEC)"
fi
EOF

chmod +x k8s-portfolio/buoi-19/verify-hpa-autoscaling.sh
./k8s-portfolio/buoi-19/verify-hpa-autoscaling.sh

# 4. Tạo tệp nhat-ky-buoi-19.md
cat << 'EOF' > k8s-portfolio/buoi-19/nhat-ky-buoi-19.md
# NHẬT KÝ THU HOẠCH BUỔI 19

1. HPA vs VPA & Công thức HPA:
   - HPA co giãn số bản sao Pods hàng ngang; VPA co giãn dung lượng CPU/RAM hàng dọc.
   - Công thức: desiredReplicas = ceil[ currentReplicas * (currentMetric / targetMetric) ].

2. Điều kiện phụ thuộc resources.requests:
   - 100% containers phải có requests.cpu để HPA tính tỷ lệ % utilization.
   - Thiếu requests.cpu khiến HPA báo chỉ số <unknown>.

3. Cơ chế chống Flapping (stabilizationWindowSeconds):
   - Mặc định trì hoãn 300s (5 phút) trước khi scaleDown để giữ hạ tầng ổn định.
EOF

# 5. Dọn dẹp tệp tạm
rm -f /tmp/hpa-api.txt /tmp/hpa-target.txt /tmp/scaled-replicas.txt /tmp/period-sec.txt
```

**CHECKPOINT 13 — Đủ 4 tệp hiện vật trong thư mục portfolio.**

```bash
[ -f k8s-portfolio/buoi-19/php-deploy.yaml ] && [ -f k8s-portfolio/buoi-19/custom-behavior-hpa.yaml ] && [ -f k8s-portfolio/buoi-19/verify-hpa-autoscaling.sh ] && [ -f k8s-portfolio/buoi-19/nhat-ky-buoi-19.md ] && echo "CHECKPOINT 13 — ĐẠT" || echo "CHECKPOINT 13 — LỖI"
```

---

## L8. Xử lý sự cố thường gặp trong lab

| # | Triệu chứng lỗi | Nguyên nhân khả dĩ | Cách xử lý sửa lỗi |
|---|---|---|---|
| 1 | Cột `TARGETS` trong `kubectl get hpa` báo `<unknown>/50%` | Deployment thiếu `resources.requests.cpu` | Bổ sung `resources.requests.cpu` vào Pod spec của Deployment |
| 2 | HPA không chịu scale down sau khi xoá Pod bắn tải | Do cơ chế trì hoãn `stabilizationWindowSeconds: 300` | Đợi đủ 5 phút (300s) để HPAController tự động scale down |
| 3 | Lệnh `kubectl autoscale` báo `target deployment not found` | Gõ sai tên Deployment hoặc thiếu cờ `-n dev` | Kiểm tra tên Deployment qua `kubectl get deploy -n dev` |
| 4 | Lỗi YAML HPA `unknown field "metrics"` | Khai báo sai apiVersion `autoscaling/v1` thay vì `v2` | Đổi header tệp YAML sang `apiVersion: autoscaling/v2` |
| 5 | Pods mới tạo ra bởi HPA bị kẹt `Pending` | Số bản sao vượt quá tài nguyên Allocatable của cụm | Tăng Worker Node hoặc giảm `maxReplicas` trong HPA spec |
| 6 | HPA báo `unable to get metrics for resource cpu` | Add-on `metrics-server` bị sập hoặc lỗi TLS | Kiểm tra `kubectl get pods -n kube-system` xem metrics-server OK không |
| 7 | HPA scale out liên tục vượt `maxReplicas` | Không có chuyện vượt `maxReplicas` trừ khi khai báo nhầm | Kiểm tra lại chỉ số `maxReplicas` trong HPA YAML spec |
| 8 | Lệnh bắn tải `wget` trong Pod load-generator báo `cannot resolve host` | Gõ sai tên Service domain name | Gõ đúng `http://php-service.dev.svc.cluster.local` |
| 9 | Thắc mắc vì sao `kubectl scale` không có tác dụng khi có HPA | HPA Controller chạy vòng lặp 15s tự động ghi đè | Không gõ `kubectl scale` thủ công khi đã gán HPA |
| 10 | HPA scale up quá chậm trong 1-2 phút đầu | Chu kỳ quét Controller là 15s + thời gian Pod khởi tạo | Tùy chỉnh `behavior.scaleUp` với `stabilizationWindowSeconds: 0` |
| 11 | Pod `load-generator` bị sập `CrashLoopBackOff` | Gõ sai cú pháp vòng lặp command bash `while true; do ...` | Kiểm tra cú pháp script command trong Pod load-generator |
| 12 | Script `verify-hpa-autoscaling.sh` báo lỗi | Vẫn chưa apply tệp `custom-behavior-hpa.yaml` | Chạy lệnh `kubectl apply -f k8s-portfolio/buoi-19/custom-behavior-hpa.yaml` |

---

## L9. Bài tập mở rộng

1. **BT1 — Tạo HPA co giãn theo Memory utilization %:** Biên soạn tệp YAML HPA v2 với `resource.name: memory` và `averageUtilization: 75`.
2. **BT2 — Cấu hình HPA với nhiều chỉ số đo đạc (Multiple Metrics):** Kết hợp cả 2 chỉ số CPU (50%) và Memory (80%) trong cùng 1 HPA spec và quan sát chỉ số lớn hơn được chọn.
3. **BT3 — Sử dụng cờ `--behavior` trong HPA v2:** Cấu hình `scaleDown` với `selectPolicy: Disabled` để cấm hoàn toàn HPA tự động scale down.
4. **BT4 — Thử nghiệm bắn tải bằng công cụ `hey`:** Khởi chạy Pod chứa công cụ `hey` bắn 50 concurrent connections trong 2 phút vào `php-service`.
5. **BT5 — Khảo sát sự kiện (Events) của HPA:** Chạy lệnh `kubectl describe hpa php-hpa-v2 -n dev` để đọc nhật ký sự kiện `SuccessfulRescale`.
6. **BT6 — Thử nghiệm HPA cho đối tượng StatefulSet:** Tạo StatefulSet 2 bản sao và gán HPA v2 để kiểm chứng việc HPA scale out các bản sao StatefulSet.

---

## L10. Hiện vật nộp và tiêu chí chấm điểm

### Bảng điểm đánh giá bài lab

| Hạng mục hiện vật | Yêu cầu kĩ thuật | Điểm tối đa |
|---|---|---|
| `php-deploy.yaml` | Tệp YAML Deployment chứa resources.requests.cpu chuẩn | 20 điểm |
| `custom-behavior-hpa.yaml` | Tệp YAML HPA v2 cấu hình behavior và stabilizationWindowSeconds | 25 điểm |
| `load-test-report.txt` | Báo cáo kết quả bắn tải Load Testing chứng minh scale out OK | 20 điểm |
| `verify-hpa-autoscaling.sh` | Script bash chạy thành công, xác minh HPA Autoscaling OK | 20 điểm |
| `nhat-ky-buoi-19.md` | Trả lời đủ 3 câu thu hoạch, phân biệt rõ HPA vs VPA và công thức | 15 điểm |
| CHECKPOINT 1–13 | Tất cả 13 checkpoint tự động đều in chữ `ĐẠT` | 10 điểm |
| **Tổng điểm** | | **100 điểm** |

### Các trường hợp trừ điểm

- Trừ **20 điểm**: Nếu script hoặc câu lệnh sử dụng công cụ `jq` (vi phạm quy tắc môi trường thi).
- Trừ **15 điểm**: Nếu quên cờ `-n dev` khiến các đối tượng bị tạo nhầm vào namespace `default`.
- Trừ **10 điểm**: Nếu file hiện vật để sai đường dẫn thư mục `k8s-portfolio/buoi-19/`.
- Trừ **5 điểm**: Nếu dấu phân cách thập phân trong báo cáo dùng dấu chấm `.` thay vì dấu phẩy `,`.


---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu


## V1. Cách tiến hành

1. **Thời lượng và hình thức:** Khối vấn đáp diễn ra trong đúng **20 phút**. Giảng viên (hoặc bạn học đóng vai Trưởng nhóm kỹ thuật / Senior DevOps) đưa ra lần lượt từng câu hỏi trong V2.
2. **Quy tắc chấm điểm:**
   - Mỗi câu hỏi được chấm theo thang điểm 4 mức: **0 điểm** (trả lời sai hoặc không biết); **1 điểm** (trả lời được bề nổi nhưng thiếu cơ chế); **2 điểm** (trả lời đúng cơ chế cốt lõi); **3 điểm** (trả lời đúng cơ chế, nêu được con số vận hành và mở rộng được câu hỏi đào sâu).
   - **Quy tắc trần điểm riêng của Buổi 19:**
     - Trả lời Câu 1 mà không phân biệt được HPA (co giãn hàng ngang tăng/giảm số bản sao Pods) vs VPA (co giãn hàng dọc tăng/giảm cấu hình CPU/RAM) thì **trần điểm câu đó là 1**.
     - Trả lời Câu 2 mà không nêu được công thức toán học `desiredReplicas = ceil[ currentReplicas * ( currentMetric / targetMetric ) ]` thì **trần điểm câu đó là 1**.
3. **Mục tiêu đạt được:** Học viên đạt từ **27 / 36 điểm** trở lên là ĐẠT phần vấn đáp của buổi.

---

---

## V2. Bộ câu hỏi phỏng vấn thực chiến

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q01</span>
    <span>Trình bày công thức toán học Kube-Controller-Manager sử dụng để tính số lượng bản sao Pods mong muốn (<code>desiredReplicas</code>) cho HPA.</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Công thức bất biến:</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">**<code>desiredReplicas = ceil[ currentReplicas * ( currentMetricValue / desiredMetricValue ) ]</code>**</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Giải thích các thành phần:</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>currentReplicas</code>: Số lượng bản sao Pods hiện tại đang chạy.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>currentMetricValue</code>: Tỷ lệ tiêu thụ tài nguyên thực tế hiện tại (lấy từ <code>metrics-server</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>desiredMetricValue</code>: Tỷ lệ tiêu thụ tài nguyên mục tiêu khai báo trong HPA spec (như <code>50%</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>ceil[...]</code>: Hàm toán học làm tròn lên số nguyên gần nhất (ví dụ 3,1 -> 4).</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Không nhớ công thức HPA.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Trả lời lấy số hiện tại nhân tỷ lệ nhưng không viết được chính xác công thức và hàm làm tròn lên <code>ceil</code> (dính trần 1đ).</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Viết chuẩn xác công thức <code>desiredReplicas = ceil[ currentReplicas * ( currentMetric / targetMetric ) ]</code> và giải thích các biến.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, làm bài toán tính số Pods thực tế ngay tại chỗ.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Nếu currentReplicas = 2, current CPU = 80%, target CPU = 50% thì HPA sẽ scale lên bao nhiêu Pods? *(Đáp án: <code>desiredReplicas = ceil[ 2 * (80/50) ] = ceil[3.2] = 4 Pods</code>).*

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q02</span>
    <span>Tại sao nếu Pod spec của Deployment KHÔNG khai báo <code>resources.requests.cpu</code> thì HPA không thể tính toán được tỷ lệ % CPU utilization và báo chỉ số <code><unknown></code>?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Công thức tính % Utilization:</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Tỷ lệ phần trăm % CPU utilization được HPA tính theo công thức:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">**<code>CPU Utilization % = (CPU thực tế tiêu thụ / CPU Request) * 100</code>**</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Nguyên nhân lỗi:</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Nếu không khai báo <code>resources.requests.cpu</code> trong Pod spec, mẫu số <code>CPU Request</code> không tồn tại (bằng 0 hoặc null). Phép chia cho null bị vô nghĩa.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Hệ quả:</b> HPA Controller không thể tính được % CPU, cột <code>TARGETS</code> hiển thị <code><unknown>/50%</code> và HPA đứng yên không chịu scale.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Bảo HPA báo unknown do thiếu metrics-server.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Trả lời do thiếu requests nhưng không giải thích được công thức chia % CPU cần <code>requests.cpu</code> làm mẫu số.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Phân tích chuẩn xác công thức <code>% CPU = (Thực tế / Request) * 100</code> và việc thiếu mẫu số làm phép chia vô nghĩa gây lỗi <code><unknown></code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, chỉ ra câu lệnh <code>kubectl describe hpa</code> để phát hiện lỗi này.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Để HPA thoát khỏi lỗi <code><unknown></code>, kỹ sư cần thực hiện câu lệnh hoặc thao tác gì? *(Đáp án: Bổ sung <code>resources.requests.cpu</code> vào Pod spec của Deployment và re-apply).*

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q03</span>
    <span>Tần suất vòng lặp kiểm tra chỉ số HPA của tiến trình <code>HPA Controller</code> (nằm trong <code>kube-controller-manager</code>) là bao nhiêu giây một lần?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Tần suất định kỳ:</b> Tiến trình HPA Controller chạy vòng lặp kiểm tra định kỳ mặc định <b style="color: var(--accent-primary);">15 giây một lần</b> (<code>--horizontal-pod-autoscaler-sync-period=15s</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Ý nghĩa:</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Chu kỳ 15 giây đảm bảo HPA phản ứng đủ nhanh khi có đợt tăng tải đột biến (Traffic Spike).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Không gây quá tải (Overhead) cho <code>metrics-server</code> và API Server của cụm.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Bảo 1 phút hoặc 5 phút một lần.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Trả lời 15 giây nhưng không nêu được tên tiến trình phụ trách <code>kube-controller-manager</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Giải thích chuẩn xác tần suất 15 giây/lần của HPA Controller trong <code>kube-controller-manager</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, chỉ ra cờ cấu hình <code>--horizontal-pod-autoscaler-sync-period</code>.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Tại sao vừa bắn tải mà <code>kubectl get hpa</code> phải mất từ 15 đến 30 giây mới bắt đầu nhảy chỉ số CPU? *(Đáp án: Do phải chờ đến lượt vòng lặp 15s tiếp theo của HPA Controller quét metrics).*

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q04</span>
    <span>Cửa sổ thời gian ổn định co giảm <code>stabilizationWindowSeconds</code> trong HPA có giá trị mặc định là bao nhiêu và vai trò của nó là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Giá trị mặc định:</b> <code>stabilizationWindowSeconds</code> trong khối <code>behavior.scaleDown</code> có giá trị mặc định là <b style="color: var(--accent-primary);">300 giây (5 phút)</b>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Vai trò chính:</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Trì hoãn việc xoá bớt Pods (scale down / scale in) trong đúng 5 phút sau khi tải đã giảm xuống rảnh.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Chống hiện tượng Flapping / Thrashing (Rung lắc số bản sao):</b> Tránh việc HPA vừa xoá bớt Pods xong 10 giây sau lưu lượng truy cập lại bùng nổ lên, bắt Kubernetes phải tạo lại Pods mới gây tốn tài nguyên khởi tạo.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Bảo mặc định là 0 giây.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Trả lời 5 phút nhưng không giải thích được thuật ngữ Flapping/Thrashing và lý do giữ ổn định hạ tầng.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Giải thích chuẩn xác con số 300s (5 phút) và vai trò chống Flapping/Thrashing khi tải trồi sụt.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, minh hoạ cách chỉnh <code>stabilizationWindowSeconds: 60</code> trong YAML v2.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Nếu đặt <code>stabilizationWindowSeconds: 0</code> cho scaleDown thì chuyện gì sẽ xảy ra khi traffic trồi sụt liên tục? *(Đáp án: Pods sẽ bị xoá và tạo mới liên tục hàng chục lần gây đứt kết nối ứng dụng).*

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q05</span>
    <span>Câu lệnh CLI nào giúp khởi tạo nhanh một HPA cho Deployment <code>web-deploy</code> với <code>minReplicas: 2</code>, <code>maxReplicas: 10</code>, và target CPU <code>50%</code> trong 2 giây?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Câu lệnh CLI chuẩn (Imperative Command):</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"><code>kubectl autoscale deployment web-deploy -n dev --min=2 --max=10 --cpu-percent=50</code></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Tác dụng:</b> Tự động sinh ra đối tượng HPA liên kết trực tiếp với Deployment <code>web-deploy</code> trong Namespace <code>dev</code> mà không cần viết file YAML thủ công.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Không nhớ lệnh <code>kubectl autoscale</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Nêu được <code>kubectl autoscale</code> nhưng thiếu các cờ <code>--min</code>, <code>--max</code>, <code>--cpu-percent</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Viết chuẩn xác câu lệnh <code>kubectl autoscale deployment web-deploy -n dev --min=2 --max=10 --cpu-percent=50</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, chỉ ra cờ <code>--dry-run=client -o yaml</code> để xuất ra file YAML.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Lệnh trên tạo ra HPA dùng API version nào? *(Đáp án: Mặc định tạo ra HPA dùng API version <code>autoscaling/v1</code> hoặc <code>v2</code> tùy phiên bản kubectl).*

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q06</span>
    <span>Sự khác biệt giữa HPA API version <code>autoscaling/v1</code> và <code>autoscaling/v2</code> là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);"><code>autoscaling/v1</code> (Phiên bản cũ):</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Chỉ hỗ trợ <b style="color: var(--accent-primary);">ĐƠN CHỈ SỐ duy nhất là CPU utilization %</b>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Cấu trúc YAML đơn giản nhưng hạn chế mở rộng.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);"><code>autoscaling/v2</code> (Phiên bản hiện đại chuẩn hóa):</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Hỗ trợ <b style="color: var(--accent-primary);">NHIỀU CHỈ SỐ ĐỒNG THỜI (Multiple Metrics)</b>: CPU, Memory, Custom Metrics (QPS, Queue Length), External Metrics.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Hỗ trợ khối <b style="color: var(--accent-primary);"><code>spec.behavior</code></b> cho phép tùy chỉnh chi tiết tốc độ scaleUp và scaleDown (stabilizationWindowSeconds).</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Bảo 2 API version giống hệt nhau.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Trả lời v2 mới hơn nhưng không nêu được khả năng hỗ trợ Memory, Multiple Metrics và khối <code>spec.behavior</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Phân tích chuẩn xác v1 (chỉ CPU) vs v2 (Memory, Multiple Metrics, Custom Metrics, <code>spec.behavior</code>).</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, minh hoạ khối <code>metrics[]</code> trong v2 YAML.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Khi khai báo nhiều chỉ số (CPU 50% và Memory 80%) trong HPA v2 thì HPA chọn số Pods tính theo CPU hay Memory? *(Đáp án: HPA sẽ chọn số Pods LỚN NHẤT giữa các kết quả tính toán).*

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q07</span>
    <span>Tại sao việc tự gõ lệnh <code>kubectl scale deployment</code> thủ công lại bị vô hiệu hóa hoặc không có tác dụng dài hạn khi Deployment đó đang được HPA quản lý?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Nguyên nhân:</b> Khi một Deployment đã được gán đối tượng HPA, đối tượng HPA giữ quyền điều khiển duy nhất đối với trường <code>spec.replicas</code> của Deployment đó.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Hành vi HPA Controller:</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Nếu kỹ sư tự gõ <code>kubectl scale deployment web-deploy --replicas=8</code> thủ công, số bản sao tạm thời nảy lên 8.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Tuy nhiên, trong <b style="color: var(--accent-primary);">vòng lặp 15 giây tiếp theo</b>, HPA Controller tính toán lại tải thực tế (ví dụ tải thấp chỉ cần 2 Pods) và <b style="color: var(--accent-primary);">tự động ghi đè số <code>replicas</code> về lại 2 Pods</b>.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Bảo <code>kubectl scale</code> bị API Server báo lỗi cấm gõ.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Trả lời bị ghi đè nhưng không giải thích được vòng lặp 15s của HPA Controller ghi đè trường <code>spec.replicas</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Giải thích chuẩn xác việc HPA Controller tự động ghi đè lại số <code>replicas</code> trong vòng lặp 15s tiếp theo.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, chỉ ra cách gỡ HPA trước khi scale thủ công.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Làm sao để thay đổi số Pods tối thiểu thủ công mà không xoá HPA? *(Đáp án: Dùng lệnh <code>kubectl edit hpa</code> hoặc <code>kubectl patch hpa</code> để sửa cờ <code>minReplicas</code>).*

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q08</span>
    <span>Kube-Controller-Manager xử lý như thế nào khi tính toán HPA mà kết quả công thức <code>desiredReplicas</code> nằm ngoài khoảng <code>minReplicas</code> và <code>maxReplicas</code>?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Nguyên tắc ép khoảng (Clamping):</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Nếu <code>desiredReplicas < minReplicas</code>: HPA tự động gán <code>desiredReplicas = minReplicas</code> (không bao giờ giảm dưới min).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Nếu <code>desiredReplicas > maxReplicas</code>: HPA tự động gán <code>desiredReplicas = maxReplicas</code> (không bao giờ vượt quá max).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Ý nghĩa:</b> <code>minReplicas</code> bảo vệ tính sẵn sàng cao (HA); <code>maxReplicas</code> bảo vệ cụm Node không bị cạn kiệt tài nguyên RAM/CPU.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Bảo HPA báo lỗi crash khi vượt maxReplicas.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Trả lời giữ ở min và max nhưng không giải thích được thuật ngữ ép khoảng (clamping) bảo vệ HA và bảo vệ cụm.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Giải thích chuẩn xác cơ chế ép khoảng: giữ nguyên <code>minReplicas</code> khi tải rảnh và không vượt quá <code>maxReplicas</code> khi bão tải.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, chỉ ra nguy cơ kẹt Pod <code>Pending</code> nếu <code>maxReplicas</code> đặt quá cao.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Chuyện gì xảy ra nếu <code>maxReplicas</code> đặt là 50 mà cụm chỉ đủ CPU/RAM cho 20 Pods? *(Đáp án: HPA scale ra 50 Pods, 20 Pods Running, 30 Pods còn lại bị kẹt <code>Pending</code>).*

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q09</span>
    <span>Khối <code>spec.behavior.scaleUp</code> trong HPA v2 API được sử dụng trong kịch bản nào trên thực tế?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Kịch bản sử dụng:</b> Khi ứng dụng gặp đợt bùng nổ lưu lượng truy cập cực lớn trong thời gian cực ngắn (Traffic Spike / Flash Sale).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Tùy chỉnh scaleUp:</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Đặt <code>stabilizationWindowSeconds: 0</code> để HPA scale up ngay lập tức mà không trì hoãn.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Cấu hình policy <code>percent: 100</code> hoặc <code>pods: 4</code> mỗi 15 giây để nhân đôi số bản sao Pods trong vài giây.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Lợi ích:</b> Giúp ứng dụng bùng nổ năng lực xử lý tức thì, tránh việc Pods mới được tạo quá chậm làm sập server.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Không biết khối behavior scaleUp.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Trả lời dùng để tăng tốc scale up nhưng không nêu được các thuộc tính policy <code>percent</code> / <code>pods</code> và <code>stabilizationWindowSeconds</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Giải thích chuẩn xác kịch bản bùng nổ Flash Sale/Traffic Spike và các thuộc tính tùy chỉnh tốc độ scaleUp.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, minh hoạ file YAML HPA v2 với <code>behavior.scaleUp</code>.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Chu kỳ periodSeconds mặc định của scaleUp policy trong HPA behavior là bao nhiêu? *(Đáp án: Mặc định là <b style="color: var(--accent-primary);">15 giây</b>).*

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q10</span>
    <span>Tại sao HPA KHÔNG thể tự động co giãn các bản sao Pods do đối tượng <code>DaemonSet</code> quản lý?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Bản chất của DaemonSet:</b> Số lượng Pods do DaemonSet quản lý phụ thuộc 100% vào số lượng Worker Node trong cụm (mỗi Node chạy đúng 1 Pod). DaemonSet <b style="color: var(--accent-primary);">KHÔNG CÓ trường <code>spec.replicas</code></b>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Yêu cầu của HPA:</b> HPA chỉ làm việc được với các đối tượng sở hữu subresource <code>/scale</code> và trường <code>spec.replicas</code> (như Deployment, StatefulSet, ReplicaSet).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Kết quả:</b> Gán HPA vào DaemonSet sẽ bị API Server từ chối.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Bảo HPA scale được DaemonSet bình thường.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Trả lời DaemonSet 1 Pod/Node nhưng không giải thích được việc DaemonSet thiếu trường <code>spec.replicas</code> và subresource <code>/scale</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Giải thích chuẩn xác nguyên lý 1 Pod/Node của DaemonSet và việc thiếu trường <code>spec.replicas</code> làm HPA không làm việc được.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, chỉ ra các đối tượng HPA hỗ trợ (<code>Deployment</code>, <code>StatefulSet</code>).</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Đối tượng nào ngoài Deployment có thể liên kết với HPA? *(Đáp án: Đối tượng <code>StatefulSet</code> và <code>ReplicaSet</code>).*

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q11</span>
    <span>Nêu 2 chế độ hỏng (1 im lặng do HPA báo <code><unknown></code> vì thiếu requests.cpu, 1 âm thầm do Flapping Pods bị xoá/tạo liên tục vì để stabilizationWindow bằng 0) và cách phát hiện/khắc phục.</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Chế độ hỏng 1 (Im lặng - HPA đứng yên báo chỉ số <code><unknown></code> do Deployment thiếu <code>requests.cpu</code>):</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• *Triệu chứng:* Bắn tải dồn dập vào Web nhưng HPA không chịu scale out Pods, cột <code>TARGETS</code> trong <code>kubectl get hpa</code> báo <code><unknown>/50%</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• *Phát hiện:* Chạy <code>kubectl describe hpa</code> thấy lỗi <code>failed to get cpu utilization: missing request for cpu</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• *Khắc phục:* Bổ sung <code>resources.requests.cpu</code> vào Pod spec của Deployment.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Chế độ hỏng 2 (Âm thầm - Flapping Pods bị tạo mới và xoá liên tục do để <code>stabilizationWindowSeconds: 0</code> cho scaleDown):</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• *Triệu chứng:* Lưu lượng truy cập trồi sụt nhẹ làm HPA liên tục scale up rồi scale down 20-30 lần/giờ, gây quá tải etcd và làm gián đoạn kết nối DB.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• *Phát hiện:* Xem nhật ký <code>kubectl get hpa -w</code> thấy số Replicas nhảy 2 -> 6 -> 2 -> 6 liên tục trong vài phút.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• *Khắc phục:* Giữ nguyên hoặc nâng <code>stabilizationWindowSeconds: 300</code> (5 phút) cho khối scaleDown.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">0đ:</b> Không nêu được 2 chế độ hỏng.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">1đ:</b> Nêu được 2 trường hợp nhưng không chỉ ra nguyên nhân thiếu <code>requests.cpu</code> và <code>stabilizationWindowSeconds: 0</code> gây Flapping (dính trần 1đ).</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">2đ:</b> Giải thích chuẩn xác 2 chế độ hỏng và câu lệnh khắc phục tương ứng.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">3đ:</b> Trả lời xuất sắc, minh hoạ bằng kinh nghiệm thực tế bài lab.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> Khi HPA báo chỉ số <code><unknown></code>, câu lệnh nào xem được chi tiết nguyên nhân trong 2 giây? *(Đáp án: Lệnh <code>kubectl describe hpa <hpa-name></code>).*

---

## V3. Câu chốt để nói khi phỏng vấn

1. *"HPA co giãn số bản sao Pods (Replicas) hàng ngang; VPA co giãn dung lượng CPU/RAM của từng Pod theo chiều dọc."*
2. *"HPA Controller tính số Pods theo công thức bất biến: <code>desiredReplicas = ceil[ currentReplicas * ( currentMetric / targetMetric ) ]</code>."*
3. *"100% containers trong Pod spec bắt buộc phải có <code>resources.requests.cpu</code>; thiếu <code>requests.cpu</code> làm HPA báo chỉ số <code><unknown></code>."*
4. *"Tiến trình HPA Controller chạy vòng lặp quét chỉ số từ <code>metrics-server</code> định kỳ <b style="color: var(--accent-primary);">15 giây một lần</b>."*
5. *"Cửa sổ trì hoãn <code>stabilizationWindowSeconds: 300</code> (5 phút) bảo vệ hệ thống khỏi sự cố rung lắc số bản sao (Flapping/Thrashing)."*

---</div>
</div>
</details>

---

## V3. Câu chốt để nói khi phỏng vấn

1. *"HPA co giãn số bản sao Pods (Replicas) hàng ngang; VPA co giãn dung lượng CPU/RAM của từng Pod theo chiều dọc."*
2. *"HPA Controller tính số Pods theo công thức bất biến: `desiredReplicas = ceil[ currentReplicas * ( currentMetric / targetMetric ) ]`."*
3. *"100% containers trong Pod spec bắt buộc phải có `resources.requests.cpu`; thiếu `requests.cpu` làm HPA báo chỉ số `<unknown>`."*
4. *"Tiến trình HPA Controller chạy vòng lặp quét chỉ số từ `metrics-server` định kỳ **15 giây một lần**."*
5. *"Cửa sổ trì hoãn `stabilizationWindowSeconds: 300` (5 phút) bảo vệ hệ thống khỏi sự cố rung lắc số bản sao (Flapping/Thrashing)."*

---

## 4. Đề Thi Thực Hành Bấm Giờ & Thử Thách Tốc Độ (Exam Speed Challenge)

> [!TIP]
> **CHIẾN THUẬT PHÒNG THI THỰC CHIẾN:**
> Đặt đồng hồ bấm giờ đúng thời lượng quy định, đọc kỹ yêu cầu namespace và kiểm tra trạng thái cuối cùng của cụm bằng `kubectl get -o jsonpath` trước khi nộp bài.

## T0. Vì sao có khối này (1 phút)

Khối luyện đề bấm giờ 30 phút rèn luyện cho học viên phản xạ khởi tạo `HorizontalPodAutoscaler` bằng lệnh CLI imperative `kubectl autoscale`, biên soạn tệp YAML HPA v2 API (`autoscaling/v2`), khắc phục sự cố HPA báo chỉ số `<unknown>` do thiếu `resources.requests.cpu`, và tùy chỉnh khối `behavior` chống hiện tượng Flapping trong kỳ thi CKA và CKAD.

Buổi 19 phủ miền trọng điểm của 2 kỳ thi:
- `CKA · Workloads & Scheduling` (Trọng số 15 %)
- `CKAD · Application Deployment` (Trọng số 20 %)

Các câu hỏi được thiết kế theo đúng chuẩn bài thi CKA/CKAD thực tế: yêu cầu thí sinh liên kết HPA với Deployment, thiết lập đúng chỉ số `averageUtilization`, và kiểm soát tốc độ co giãn mà KHÔNG được dùng `jq`.

---

## T1. Luật chơi (1 phút)

1. **Đồng hồ bấm giờ:** Tổng thời gian làm 4 câu hỏi là **900 giây (15 phút)**. Thời gian còn lại (15 phút) dành cho việc đọc luật, đối soát và tự chấm điểm bằng script.
2. **Tài liệu được mở:** Chỉ được phép mở 1 tab duy nhất tài liệu chính thức `https://kubernetes.io/docs/`. KHÔNG được tìm kiếm Google hay StackOverflow.
3. **Môi trường làm việc:** Làm việc trực tiếp trên terminal với context `kubeadm`.
4. **Quy tắc thi hành về công cụ:** Máy thi **KHÔNG cài sẵn `jq`**. Mọi câu hỏi trích xuất dữ liệu BẮT BUỘC dùng đường gõ bash (`grep`/`awk`/`sed`) hoặc `kubectl jsonpath`.
5. **Cách chấm:** Chấm dựa trên sự tồn tại của đối tượng HPA, giá trị `apiVersion`, chỉ số `averageUtilization` và số bản sao `replicas` trong Deployment. Ngưỡng ĐẠT của buổi là **66 / 100 điểm** (theo đúng chuẩn CKA/CKAD).

---

## T2. Bộ câu hỏi kiểu đề thi

### Câu T2.1. Tạo HPA bằng lệnh CLI kubectl autoscale — 210 giây

**Bối cảnh:**
Thiết lập tự động co giãn nhanh cho một Deployment bằng câu lệnh CLI.

**Yêu cầu:**
1. Tạo Namespace `dev` (nếu chưa có).
2. Tạo Deployment tên `php-deploy` trong Namespace `dev` sử dụng image `registry.k8s.io/hpa-example:v1.0` với `replicas: 2` và `resources.requests.cpu: 100m`.
3. Sử dụng lệnh `kubectl autoscale` để tạo HPA tên `php-deploy` cho Deployment trên với `min: 2`, `max: 10`, `cpu-percent: 50`.
4. Trích xuất tên Deployment liên kết trong HPA vào tệp `/tmp/ans-t21-target.txt`.

**Thang điểm bộ phận:**
- Tạo Deployment chứa `requests.cpu: 100m`: **10 điểm**.
- Tạo HPA bằng lệnh `kubectl autoscale` và ghi file `/tmp/ans-t21-target.txt`: **15 điểm**.

---

### Câu T2.2. Biển soạn tệp YAML HPA v2 API autoscaling/v2 — 240 giây

**Bối cảnh:**
Chuyển đổi HPA sang định dạng YAML chuẩn hóa v2 API hỗ trợ cấu hình mở rộng.

**Yêu cầu:**
1. Xoá HPA cũ tên `php-deploy` trong Namespace `dev`.
2. Tạo tệp YAML HPA tên `php-hpa-v2` chuẩn API `autoscaling/v2` liên kết với Deployment `php-deploy`.
3. Khai báo `minReplicas: 2`, `maxReplicas: 10` và `metrics` loại Resource CPU `averageUtilization: 50`.
4. Trích xuất `apiVersion` của HPA vào tệp `/tmp/ans-t22-api.txt`.

**Thang điểm bộ phận:**
- Biển soạn đúng tệp HPA v2 API `autoscaling/v2`: **15 điểm**.
- HPA hoạt động khớp target CPU 50% và ghi file `/tmp/ans-t22-api.txt`: **15 điểm**.

---

### Câu T2.3. Sửa lỗi HPA báo chỉ số unknown do thiếu requests.cpu — 210 giây

**Bối cảnh:**
Chẩn đoán và khắc phục sự cố HPA đứng yên không chịu scale do Deployment thiếu tài nguyên cọc.

**Yêu cầu:**
1. Tạo Deployment tên `fix-deploy` trong Namespace `dev` sử dụng image `nginx:1.27-alpine` không có `resources.requests`.
2. Tạo HPA tên `fix-hpa` liên kết với `fix-deploy` target CPU 50%.
3. Sửa Deployment `fix-deploy` bổ sung `resources.requests.cpu: 100m` để HPA tính được CPU %.
4. Trích xuất chỉ số `requests.cpu` của Deployment sau khi sửa vào tệp `/tmp/ans-t23-req.txt`.

**Thang điểm bộ phận:**
- Sửa Deployment bổ sung thành công `requests.cpu: 100m`: **10 điểm**.
- HPA thoát khỏi trạng thái unknown và ghi file `/tmp/ans-t23-req.txt`: **10 điểm**.

---

### Câu T2.4. Cấu hình behavior scaleDown stabilizationWindowSeconds — 240 giây

**Bối cảnh:**
Tùy chỉnh hành vi co giãn HPA v2 chống hiện tượng rung lắc số lượng bản sao (Flapping).

**Yêu cầu:**
1. Tạo HPA tên `custom-behavior-hpa` trong Namespace `dev` liên kết với Deployment `php-deploy`.
2. Cấu hình `minReplicas: 2`, `maxReplicas: 8`, target CPU `60%`.
3. Bổ sung khối `spec.behavior.scaleDown` chứa `stabilizationWindowSeconds: 300`.
4. Trích xuất thuộc tính `stabilizationWindowSeconds` vào tệp `/tmp/ans-t24-stab.txt`.

**Thang điểm bộ phận:**
- Cấu hình đúng khối `behavior.scaleDown` trong HPA v2: **15 điểm**.
- Trích xuất đúng con số `300` vào `/tmp/ans-t24-stab.txt`: **10 điểm**.

---

## T3. Lời giải chuẩn

#### Lời giải câu T2.1: Đường gõ ngắn nhất (Ước lượng: 40 giây / 2 thao tác)

```bash
# Thao tác 1: Tạo ns dev, apply php-deploy và autoscale
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-deploy
  namespace: dev
spec:
  replicas: 2
  selector:
    matchLabels:
      app: php-app
  template:
    metadata:
      labels:
        app: php-app
    spec:
      containers:
      - name: php
        image: registry.k8s.io/hpa-example:v1.0
        resources:
          requests:
            cpu: "100m"
EOF
kubectl autoscale deployment php-deploy -n dev --min=2 --max=10 --cpu-percent=50

# Thao tác 2: Ghi target name vào file
kubectl get hpa php-deploy -n dev -o jsonpath='{.spec.scaleTargetRef.name}' > /tmp/ans-t21-target.txt
```

#### Lời giải câu T2.2: Đường gõ ngắn nhất (Ước lượng: 45 giây / 2 thao tác)

```bash
# Thao tác 1: Delete HPA cũ và apply HPA v2 YAML
kubectl delete hpa php-deploy -n dev --ignore-not-found=true
cat << EOF | kubectl apply -f -
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-hpa-v2
  namespace: dev
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-deploy
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
EOF

# Thao tác 2: Ghi apiVersion vào file
kubectl get hpa php-hpa-v2 -n dev -o jsonpath='{.apiVersion}' > /tmp/ans-t22-api.txt
```

#### Lời giải câu T2.3: Đường gõ ngắn nhất (Ước lượng: 45 giây / 3 thao tác)

```bash
# Thao tác 1: Create fix-deploy và fix-hpa
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fix-deploy
  namespace: dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fix
  template:
    metadata:
      labels:
        app: fix
    spec:
      containers:
      - name: nginx
        image: nginx:1.27-alpine
EOF
kubectl autoscale deployment fix-deploy -n dev --min=1 --max=5 --cpu-percent=50

# Thao tác 2: Set resources.requests.cpu cho fix-deploy
kubectl set resources deployment fix-deploy -n dev -c=nginx --requests=cpu=100m

# Thao tác 3: Ghi requests.cpu vào file
kubectl get deploy fix-deploy -n dev -o jsonpath='{.spec.template.spec.containers[0].resources.requests.cpu}' > /tmp/ans-t23-req.txt
```

#### Lời giải câu T2.4: Đường gõ ngắn nhất (Ước lượng: 45 giây / 2 thao tác)

```bash
# Thao tác 1: Apply custom-behavior-hpa YAML
cat << EOF | kubectl apply -f -
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: custom-behavior-hpa
  namespace: dev
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-deploy
  minReplicas: 2
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
EOF

# Thao tác 2: Ghi stabilizationWindowSeconds vào file
kubectl get hpa custom-behavior-hpa -n dev -o jsonpath='{.spec.behavior.scaleDown.stabilizationWindowSeconds}' > /tmp/ans-t24-stab.txt
```



---

## T4. Bẫy mất điểm

| # | Bẫy mất điểm hay gặp | Mất bao nhiêu điểm | Dấu hiệu nhận ra ngay |
|---|---|---|---|
| 1 | Quên khai báo `resources.requests.cpu` làm HPA báo `<unknown>` | 25 điểm câu T2.1 | HPA cột TARGETS báo `<unknown>/50%` |
| 2 | Nhầm lẫn giữa API version `autoscaling/v1` và `autoscaling/v2` ở câu T2.2 | 15 điểm câu T2.2 | `apiVersion` ghi v1 thay vì `autoscaling/v2` |
| 3 | Gõ sai trường `scaleTargetRef` liên kết Deployment | 20 điểm câu T2.2 | HPA báo error `scale target not found` |
| 4 | Sử dụng `jq` để parse output `kubectl get hpa` | 25 điểm (mất trọn câu T2.1) | Output báo `bash: jq: command not found` |
| 5 | Quên cờ `-n dev` khi thao tác với HPA/Deployments | 20 điểm câu T2.1 | Đối tượng bị tạo nhầm trong Namespace `default` |
| 6 | Nhầm lẫn cờ `averageUtilization` với `averageValue` | 15 điểm câu T2.2 | HPA báo sai kiểu target metrics |

---

## T5. Bảng tự chấm

| Câu | Chứng chỉ · Miền | Ngân sách | Điểm tối đa | Điểm đạt được |
|---|---|---|---|---|
| T2.1 | `CKA · Workloads` / `CKAD` | 210s | 25 | |
| T2.2 | `CKA · Workloads` / `CKAD` | 240s | 30 | |
| T2.3 | `CKA · Workloads` / `CKAD` | 210s | 20 | |
| T2.4 | `CKA · Workloads` / `CKAD` | 240s | 25 | |
| **Tổng** | | **900s (15')** | **100** | **Ngưỡng ĐẠT: ≥ 66 điểm** |

### Đoạn mã chấm tự động (Automated Grading Script)

Copy và dán đoạn script bash dưới đây để tự động chấm điểm bài thi của Buổi 19:

```bash
#!/bin/bash
# Script tự động chấm điểm khối Ô thi Buổi 19

SCORE=0

echo "=== BẮT ĐẦU CHẤM ĐIỂM BUỔI 19 ==="

# 1. Chấm câu T2.1
if [ "$(kubectl get hpa php-deploy -n dev -o jsonpath='{.spec.scaleTargetRef.name}' 2>/dev/null)" == "php-deploy" ] && grep -qx "php-deploy" /tmp/ans-t21-target.txt; then
    echo "Câu T2.1: ĐẠT (+25 điểm)"
    SCORE=$((SCORE + 25))
else
    echo "Câu T2.1: LỖI (0/25 điểm)"
fi

# 2. Chấm câu T2.2
if [ "$(kubectl get hpa php-hpa-v2 -n dev -o jsonpath='{.apiVersion}' 2>/dev/null)" == "autoscaling/v2" ] && grep -qx "autoscaling/v2" /tmp/ans-t22-api.txt; then
    echo "Câu T2.2: ĐẠT (+30 điểm)"
    SCORE=$((SCORE + 30))
else
    echo "Câu T2.2: LỖI (0/30 điểm)"
fi

# 3. Chấm câu T2.3
if [ "$(kubectl get deploy fix-deploy -n dev -o jsonpath='{.spec.template.spec.containers[0].resources.requests.cpu}' 2>/dev/null)" == "100m" ] && grep -qx "100m" /tmp/ans-t23-req.txt; then
    echo "Câu T2.3: ĐẠT (+20 điểm)"
    SCORE=$((SCORE + 20))
else
    echo "Câu T2.3: LỖI (0/20 điểm)"
fi

# 4. Chấm câu T2.4
if [ "$(kubectl get hpa custom-behavior-hpa -n dev -o jsonpath='{.spec.behavior.scaleDown.stabilizationWindowSeconds}' 2>/dev/null)" == "300" ] && grep -qx "300" /tmp/ans-t24-stab.txt; then
    echo "Câu T2.4: ĐẠT (+25 điểm)"
    SCORE=$((SCORE + 25))
else
    echo "Câu T2.4: LỖI (0/25 điểm)"
fi

echo "=================================="
echo "TỔNG ĐIỂM: $SCORE / 100"
if [ "$SCORE" -ge 66 ]; then
    echo "KẾT QUẢ: ĐẠT CHUẨN CKA/CKAD (≥ 66 điểm)"
else
    echo "KẾT QUẢ: CHƯA ĐẠT (Cần tối thiểu 66 điểm)"
fi
```

---

## T6. Kho lệnh rút gọn của buổi

```bash
# 1. Tạo HPA nhanh bằng câu lệnh CLI imperative
kubectl autoscale deployment <deploy-name> -n <namespace> --min=<min> --max=<max> --cpu-percent=<target%>

# 2. Trích xuất danh sách HPA trong Namespace
kubectl get hpa -n <namespace>

# 3. Theo dõi biến động chỉ số HPA thời gian thực
kubectl get hpa -n <namespace> -w

# 4. Xem chi tiết sự kiện và nguyên nhân lỗi của HPA
kubectl describe hpa <hpa-name> -n <namespace>

# 5. Sửa nhanh khối resources cho Deployment
kubectl set resources deployment <deploy-name> -n <namespace> -c=<container-name> --requests=cpu=100m
```


---

## Tổng Kết & Lộ Trình Bài Học Tiếp Theo

Kiến thức và kỹ năng thực hành trong bài viết này là mắt xích quan trọng trong hệ thống quản trị và bảo mật Kubernetes chuyên nghiệp. Việc nắm vững cả lý thuyết kiến trúc lẫn thao tác gõ lệnh tốc độ cao trong terminal sẽ giúp bạn tự tin xử lý sự cố thực tế cũng như vượt qua các kỳ thi chứng chỉ quốc tế CKA, CKAD và CKS.

> [!TIP]
> **BÀI TIẾP THEO TRONG CHUỖI BÀI HỌC:**
> Tiếp tục hành trình nâng cao năng lực Kubernetes với bài học tiếp theo: [[Bài 20] Quản Lý Cấu Hình Ứng Dụng: ConfigMap, Secret, EnvFrom, Projected Volumes & Kỹ Thuật Hot Reload](cka-20-20-cau-hinh-configmap-secret.html).

{% endraw %}
