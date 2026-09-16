---
layout: post
title: "[Bài 07] Cơ Chế Probes Toàn Diện: StartupProbe, ReadinessProbe, LivenessProbe & 3 Kịch Bản Sập Ứng Dụng"
date: 2026-09-12 14:40:00 +0700
categories: [CKAD]
tags:
  - CKAD
  - Kubernetes
  - AppDeveloper
  - Microservices
  - Containers
  - Part-07
series: "CKAD Exam & App Developer Mastery"
series_order: 7
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1577563908411-5077b6dc7624?auto=format&fit=crop&w=1200&q=80"
summary: "[CKAD P.07] Hướng dẫn chuyên sâu Cơ Chế Probes Toàn Diện: StartupProbe, ReadinessProbe, LivenessProbe & 3 Kịch Bản Sập Ứng Dụng: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Cơ Chế Probes Toàn Diện: StartupProbe, ReadinessProbe, LivenessProbe & 3 Kịch Bản Sập Ứng Dụng."
  - "Làm chủ các thao tác lệnh kubectl tốc độ cao, xử lý sự cố cụm thực tế và tối ưu hóa tài nguyên Pod/Node."
  - "Củng cố kỹ năng thực chiến sát với đề thi chứng chỉ quốc tế của Linux Foundation / CNCF."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 07] CƠ CHẾ PROBES TOÀN DIỆN: STARTUPPROBE, READINESSPROBE, LIVENESSPROBE & 3 KỊCH BẢN SẬP ỨNG DỤNG

Trong kỷ nguyên điện toán đám mây và kiến trúc microservices phân tán quy mô lớn, **Kubernetes (CKAD)** đóng vai trò là nền tảng điều phối container (Container Orchestration) tiêu chuẩn công nghiệp. Để làm chủ hệ thống trong môi trường sản xuất (Production) cũng như chinh phục kỳ thi chứng chỉ quốc tế của Linux Foundation / CNCF, kỹ sư không chỉ nắm vững các câu lệnh thao tác cơ bản mà phải thấu hiểu sâu sắc bản chất cơ chế tầng thấp: từ chu trình điều hòa (Reconciliation Loop), cấu trúc điều phối tài nguyên, kiến trúc mạng CNI, lưu trữ CSI cho đến các chuẩn mực an ninh phòng thủ chiều sâu.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn giải mã toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp bài thực hành Lab từng bước và bộ câu hỏi phỏng vấn chuẩn Architect / Lead Engineer.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

| # | Câu hỏi ôn tập | Đáp án chuẩn ngắn gọn |
|---|---|---|
| 1 | Ba khái niệm cốt lõi của Helm Package Manager là gì? | **Chart**, **Values** (`values.yaml`), và **Release** |
| 2 | Thư mục nào trong Helm Chart chứa tất cả các tệp bản kê khai YAML mẫu? | Thư mục **`templates/`** |
| 3 | Cú pháp thế biến Go Template lấy giá trị từ `values.yaml`? | **`{{ .Values.key }}`** |
| 4 | Cờ CLI ghi đè trực tiếp từng biến từ terminal khi install/upgrade? | Cờ **`--set key=value`** |
| 5 | Câu lệnh CLI khôi phục Helm Release về phiên bản Revision cũ? | **`helm rollback <release> <revision>`** |



> **"Cấu hình chính xác ba loại cơ chế kiểm tra sức khỏe ứng dụng (Health Check Probes) là nội dung thuộc miền Application Observability and Maintenance trong CKAD, yêu cầu lập trình viên phân biệt rõ mục đích vận hành của `startupProbe` (che chắn cho các ứng dụng khởi động chậm), `readinessProbe` (quyết định Pod có sẵn sàng nhận traffic từ Service hay không), và `livenessProbe` (quyết định Kubelet có tiêu diệt và tái tạo lại container bị treo hay không); đồng thời làm chủ 3 phương thức kiểm tra (`httpGet`, `exec`, `tcpSocket`) và các tham số cấu hình thời gian (`initialDelaySeconds`, `periodSeconds`, `failureThreshold`) để xử lý triệt để ba ca hỏng hóc ứng dụng kinh điển trong môi trường Cloud Native."**

**Kết quả từ các buổi trước được sử dụng lại:**

| Kết quả / Công cụ | Buổi + số hiệu `QT` | Dùng ở đâu trong buổi này |
|---|---|---|
| Định nghĩa container spec và lệnh CLI | Buổi 32 `QT 4.1` | Nhúng khối cấu hình Probes dưới định nghĩa container |
| Cơ chế kết nối Service và Endpoints | Buổi 22 `QT 4.1` | Quan sát `readinessProbe` gỡ IP Pod khỏi Service Endpoints |
| Chiến lược cập nhật RollingUpdate Deployment | Buổi 35 `QT 7.1` | Kết hợp `readinessProbe` với RollingUpdate để không rớt 502 |

---



| # | Kỹ năng thực hiện được | Hiện vật chứng minh |
|---|---|---|
| 1 | Phân biệt chính xác bản chất và hành vi của 3 loại Probe (`startupProbe`, `readinessProbe`, `livenessProbe`) | Bảng so sánh hành vi xử lý của Kubelet khi từng loại Probe bị fail |
| 2 | Cấu hình thành thục 3 phương thức kiểm tra (`httpGet`, `exec`, `tcpSocket`) | Tệp YAML Pod spec chứa đủ 3 phương thức kiểm tra sức khỏe |
| 3 | Khắc phục ca hỏng 1: Pod boot chậm bị Kubelet restart liên tục | Cấu hình `startupProbe` mở rộng hạn ngạch thời gian boot |
| 4 | Khắc phục ca hỏng 2: Pod ngắt kết nối DB vẫn nhận traffic | Cấu hình `readinessProbe` kiểm tra kết nối DB trên endpoint `/ready` |
| 5 | Khắc phục ca hỏng 3: Container dính Deadlock treo luồng | Cấu hình `livenessProbe` tự động tái tạo container treo |

---



| Kiến thức tiên quyết | Nguồn tự học nếu thiếu |
|---|---|
| Định nghĩa container spec trong Pod manifest | Buổi 32 (`QT 4.1`) |
| Định tuyến Service qua cờ selector nhãn Pod | Buổi 22 (`QT 4.1`) |
| Quản lý vòng đời Pod và chính sách restartPolicy | Buổi 14 (`QT 4.1`) |

---



### 3.1. Thuật ngữ Việt–Anh

| # | Thuật ngữ tiếng Việt | Tiếng Anh tương đương | Ghi chú chuẩn hoá trong thân bài |
|---|---|---|---|
| 1 | Cơ chế kiểm tra sức khỏe | Health Check Probe | Đoạn mã Kubelet dùng để kiểm tra trạng thái container |
| 2 | Kiểm tra khởi chạy | `startupProbe` | Probe kiểm tra xem container đã khởi chạy xong chưa |
| 3 | Kiểm tra sẵn sàng | `readinessProbe` | Probe quyết định Pod có được nhận traffic từ Service không |
| 4 | Kiểm tra sự sống | `livenessProbe` | Probe quyết định Kubelet có tiêu diệt và restart container không |
| 5 | Kiểm tra qua yêu cầu HTTP | `httpGet` Action | Gửi yêu cầu HTTP GET tới đường dẫn endpoint (ví dụ `/healthz`) |
| 6 | Kiểm tra qua lệnh shell | `exec` Action | Thực thi một câu lệnh bên trong container (exit 0 = OK) |
| 7 | Kiểm tra qua cổng TCP | `tcpSocket` Action | Thử mở kết nối tới cổng TCP cụ thể trên container |
| 8 | Thời gian chờ ban đầu | `initialDelaySeconds` | Số giây Kubelet chờ trước khi bắt đầu thực hiện probe lần đầu |
| 9 | Tần suất kiểm tra định kỳ | `periodSeconds` | Khoảng thời gian giữa các lần thực hiện probe nối tiếp nhau |
| 10 | Hạn ngạch thời gian phản hồi | `timeoutSeconds` | Thời gian tối đa cho phép probe chờ câu trả lời |
| 11 | Ngưỡng thất bại | `failureThreshold` | Số lần probe dính lỗi liên tiếp để bị tính là thất bại |
| 12 | Ngưỡng thành công | `successThreshold` | Số lần probe thành công liên tiếp để được tính là khôi phục |
| 13 | Điểm cuối dịch vụ | Service Endpoints | Danh sách IP Pod sẵn sàng phục vụ traffic của Service |
| 14 | Vòng lặp tiêu diệt vĩnh viễn | Restart Loop (`CrashLoopBackOff`) | Trạng thái Pod bị Kubelet diệt và bật lại liên tục do liveness fail |



Mô hình Bác sĩ Khám Bệnh cho Vận động viên: `startupProbe` giống như Bác sĩ khám thể lực ban đầu trước khi vận động viên ra sân (nếu chưa qua thì không cho đá). `readinessProbe` giống như Cờ hiệu của Trọng tài (nếu vận động viên bị đau chân nhói nhẹ, trọng tài ra hiệu cho tạm nghỉ nhận bóng). `livenessProbe` giống như Xe cấp cứu (nếu vận động viên bị ngất xỉu ngưng tim, chở đi cấp cứu tiêu diệt và hồi sinh ngay).

---

### 1.1. Phân biệt ba loại Probe: startupProbe, readinessProbe, và livenessProbe (12 phút)

**Nguyên lý cốt lõi:** `startupProbe` được Kubelet chạy trước tiên; khi `startupProbe` chưa thành công thì mọi `livenessProbe` và `readinessProbe` đều bị vô hiệu hóa, giúp che chắn cho ứng dụng khởi động chậm không bị diệt nhầm.

**Giải thích cơ chế ngầm:** Các ứng dụng cũ (như Java Spring Boot hay Legacy ERP) có thể mất từ 2 đến 5 phút để nạp xong cache và nạp framework. Nếu không có `startupProbe`, Kubelet sẽ cho `livenessProbe` chạy ngay; do app chưa boot xong nên `livenessProbe` fail và Kubelet lại kill container, tạo ra vòng lặp diệt nhầm vĩnh viễn.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ứng dụng Java khởi động mất 3 phút liên tục bị Kubelet tiêu diệt ở phút thứ 1 và đứng ở trạng thái `CrashLoopBackOff`.

**Minh hoạ.**

```mermaid
graph TD
    Start[Khởi động Container] --> Startup{"startupProbe thành công?"}
    Startup -->|"Chưa/Đang thử"| DisableProbes[Vô hiệu hóa livenessProbe & readinessProbe]
    DisableProbes --> Startup
    Startup -->|"Thành công 100%"| EnableProbes[Kích hoạt livenessProbe & readinessProbe chạy định kỳ]
```

**Nguyên lý cốt lõi:** Khi `readinessProbe` thất bại, Kubelet KHÔNG tiêu diệt container mà chỉ gỡ IP của Pod ra khỏi danh sách Service Endpoints để ngừng chuyển traffic; khi `livenessProbe` thất bại, Kubelet sẽ tiêu diệt và khởi động lại container theo `restartPolicy`.

**Giải thích cơ chế ngầm:** Thất bại sẵn sàng (`readinessProbe`) có nghĩa là Pod đang bận hoặc tạm thời rớt kết nối DB, chỉ cần ngắt traffic người dùng và đợi Pod tự phục hồi. Thất bại sự sống (`livenessProbe`) có nghĩa là tiến trình container bị ngất/deadlock không thể tự phục hồi, bắt buộc Kubelet phải can thiệp tiêu diệt và khởi tạo lại.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cấu hình `livenessProbe` kiểm tra kết nối DB bên ngoài làm toàn bộ các Pod bị Kubelet tiêu diệt đồng loạt khi DB bị gián đoạn mạng tạm thời.

**Minh hoạ.**

```yaml
# Bảng phân biệt hành vi xử lý của Kubelet
# readinessProbe FAIL -> Gỡ IP khỏi Service Endpoints (Hành vi êm dịu)
# livenessProbe FAIL   -> Send SIGKILL diệt & restart container (Hành vi mạnh tay)
```

---

### 1.2. Ba phương thức kiểm tra (httpGet, exec, tcpSocket) và các cờ tham số mốc thời gian (12 phút)

**Nguyên lý cốt lõi:** Phương thức `httpGet` trả về mã trạng thái HTTP từ 200 đến 399 được coi là thành công; mã 4xx hoặc 5xx được tính là thất bại.

**Giải thích cơ chế ngầm:** Phù hợp cho 90% các ứng dụng Web API. Kubelet tự động gửi yêu cầu HTTP GET tới địa chỉ IP của Pod trên cổng và đường dẫn endpoint được chỉ định (như `/healthz` hoặc `/ready`).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cấu hình `httpGet` trỏ tới đường dẫn `/login` yêu cầu mã token xác thực (bị trả về 401 Unauthorized), làm Kubelet đánh giá Probe bị thất bại.

**Minh hoạ.**

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

**Nguyên lý cốt lõi:** Phương thức `exec` thực thi lệnh shell bên trong container; nếu câu lệnh trả về Exit Code 0 được coi là thành công, khác 0 là thất bại.

**Giải thích cơ chế ngầm:** Phù hợp cho các ứng dụng không có giao thức Web (như Batch Worker, Queue Processor, Database daemon). Kubelet sẽ chui vào container và gõ câu lệnh kiểm tra (như `cat /tmp/healthy` hoặc `redis-cli ping`).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Câu lệnh `exec` chứa ký tự pipe `|` hoặc redirect `>` mà không bọc qua `sh -c`, khiến lệnh shell bị lỗi syntax parser trả về exit code khác 0.

**Minh hoạ.**

```yaml
livenessProbe:
  exec:
    command:
      - cat
      - /tmp/healthy
  initialDelaySeconds: 5
  periodSeconds: 5
```

**Nguyên lý cốt lõi:** Phương thức `tcpSocket` cố gắng mở kết nối TCP tới cổng container chỉ định; nếu mở được socket kết nối thành công thì probe đạt, ngược lại bị tính là thất bại.

**Giải thích cơ chế ngầm:** Phù hợp cho các ứng dụng chạy dịch vụ giao thức TCP thuần (như MySQL cổng 3306, Memcached cổng 11211, SSH cổng 22) mà không có sẵn HTTP endpoint.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cấu hình `tcpSocket` trỏ nhầm cổng container chưa bind socket, làm Probe báo lỗi connection refused.

**Minh hoạ.**

```yaml
startupProbe:
  tcpSocket:
    port: 3306
  failureThreshold: 30
  periodSeconds: 10
```

---

### 1.3. Ba ca hỏng ứng dụng kinh điển liên quan đến Probe và cách khắc phục triệt để (10 phút)

**Nguyên lý cốt lõi:** Ca hỏng 1 (Pod khởi động chậm bị Kubelet restart liên tục): Xử lý bằng cách bổ sung `startupProbe` với `failureThreshold: 30` và `periodSeconds: 10` (cho phép tối đa 300s để app boot).

**Giải thích cơ chế ngầm:** Cho phép ứng dụng có tối đa `30 x 10 = 300` giây để khởi động xong mà không bị `livenessProbe` diệt nhầm giữa chừng.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tăng `initialDelaySeconds` của `livenessProbe` lên quá lớn (như 300s), làm mất khả năng phát hiện container bị sập trong 5 phút đầu tiên sau khi đã boot xong.

**Minh hoạ.**

```yaml
startupProbe:
  httpGet:
    path: /healthz
    port: 8080
  failureThreshold: 30 # Thử tối đa 30 lần
  periodSeconds: 10    # Mỗi lần cách nhau 10s -> Tổng 300s
```

**Nguyên lý cốt lõi:** Ca hỏng 2 (Ứng dụng ngắt kết nối DB vẫn nhận traffic gây lỗi 500): Xử lý bằng cách bổ sung `readinessProbe` kiểm tra endpoint `/ready` có query DB thật.

**Giải thích cơ chế ngầm:** Khi kết nối DB bị đứt, endpoint `/ready` trả về HTTP 503, `readinessProbe` lập tức báo fail và Kubelet lập tức gỡ IP Pod khỏi Service Endpoints, bảo vệ người dùng không bị nhận lỗi 500.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Không có `readinessProbe`, Service vẫn tiếp tục đẩy traffic người dùng vào Pod bị đứt kết nối DB.

**Minh hoạ.**

```yaml
readinessProbe:
  httpGet:
    path: /ready # Endpoint này thực hiện kiểm tra ping DB thật
    port: 8080
```

**Nguyên lý cốt lõi:** Ca hỏng 3 (Ứng dụng dính Deadlock treo luồng không tự thoát): Xử lý bằng cách bổ sung `livenessProbe` để Kubelet tự động diệt và tái tạo lại container khi không phản hồi.

**Giải thích cơ chế ngầm:** Tiến trình bên trong container bị kẹt vĩnh viễn (Deadlock/Infinite Loop), không tự dừng nhưng cũng không trả về dữ liệu. `livenessProbe` timeout liên tục sẽ kích hoạt Kubelet gửi `SIGKILL` để hồi sinh container.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ứng dụng bị treo 3 ngày nhưng Pod vẫn báo `Running 1/1` do thiếu `livenessProbe`.

**Minh hoạ.**

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  timeoutSeconds: 2
  failureThreshold: 3
```

---

### 1.4. Đưa vào cụm thật (4 phút)

**Nguyên lý cốt lõi:** Bắt buộc phân tách rõ ràng hai đường dẫn endpoint: `/healthz` (cho livenessProbe chỉ kiểm tra nội bộ container) và `/ready` (cho readinessProbe kiểm tra kết nối dịch vụ phụ thuộc như DB/Redis).

**Giải thích cơ chế ngầm:** Nếu cấu hình `livenessProbe` trỏ vào `/ready` (có kiểm tra kết nối DB), khi cụm Database bị sập hoặc bảo trì, TOÀN BỘ các Pod trên cụm Kubernetes sẽ bị Kubelet tiêu diệt đồng loạt, gây ra thảm họa gãy sập dây chuyền (Cascading Failure).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Toàn bộ 50 Microservices đồng loạt bị Kubelet diệt và restart liên tục khi cơ sở dữ liệu trung tâm bị gián đoạn mạng 10 giây.

**Minh hoạ.**

```yaml
# Cấu hình chuẩn phân tách 2 Endpoint:
containers:
  - name: app
    livenessProbe:
      httpGet:
        path: /healthz # CHỈ KIỂM TRA NỘI BỘ APP
        port: 8080
    readinessProbe:
      httpGet:
        path: /ready   # KIỂM TRA KẾT NỐI DB KHÁC
        port: 8080
```

**Áp vào cụm đang chạy thì làm gì trước:**
1. Kiểm tra tất cả tệp YAML Pod/Deployment và tách biệt 2 endpoint `/healthz` và `/ready`.
2. Bổ sung `startupProbe` cho các ứng dụng có thời gian khởi động lâu hơn 15 giây.
3. Đặt `periodSeconds: 10` và `timeoutSeconds: 2` làm chuẩn mặc định Production.

**Cái gì hỏng nếu áp thẳng lên prod:**
- Đặt `periodSeconds` quá ngắn (ví dụ 1s) sẽ làm Kubelet gửi liên tục hàng nghìn request probe gây quá tải CPU container.

**Đo trước — đo sau:**
- Quan sát danh sách Endpoints của Service qua lệnh `kubectl get endpoints` trong lúc diễn ra sự cố.
- Kiểm tra nhật ký sự kiện `kubectl get events` để xem mốc thời gian Probe fail.

**Khi nào KHÔNG nên dùng:**
- Không dùng `livenessProbe` cho các Job hay CronJob ngắn hạn chỉ chạy vài giây rồi thoát.

---

### 1.5. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính | Làm đúng là |
|---|---|---|
| 1. Cấu hình `livenessProbe` trỏ vào endpoint có check DB | Nhầm lẫn giữa livenessProbe và readinessProbe | `livenessProbe` chỉ check nội bộ app `/healthz` |
| 2. App boot chậm bị diệt do thiếu `startupProbe` | `livenessProbe` chạy ngay khi container start | Bổ sung `startupProbe` mở rộng hạn ngạch boot |
| 3. Đặt `initialDelaySeconds` quá ngắn | Container chưa kịp mở port đã bị probe check | Đặt `initialDelaySeconds` vừa đủ thời gian mở port |
| 4. Đặt `periodSeconds: 1` gây quá tải CPU Pod | Kubelet gửi request probe liên tục từng giây | Đặt `periodSeconds: 10` hoặc `5` |
| 5. Cấu hình `httpGet` trỏ tới path yêu cầu Auth 401 | Kubelet nhận mã HTTP 401 Unauthorized tính là fail | Tạo endpoint public không cần Auth cho probe |
| 6. Lệnh `exec` chứa ký tự pipe không dùng `sh -c` | Syntax shell bị lỗi trả về exit code 1 | Bọc câu lệnh: `command: ["sh", "-c", "lệnh | grep ok"]` |
| 7. Quên khai báo `port` trong khối probe | Kubelet không biết gửi probe tới cổng nào | Luôn khai báo `port:` cụ thể trong probe spec |
| 8. Tưởng `readinessProbe` fail sẽ restart container | Không phân biệt được hành vi readiness vs liveness | Readiness fail chỉ gỡ IP khỏi Service Endpoints |
| 9. Đặt `timeoutSeconds` quá ngắn làm probe fail nhầm | Mạng nội bộ gián đoạn nhẹ 1 giây | Đặt `timeoutSeconds: 2` hoặc `3` |
| 10. `tcpSocket` trỏ nhầm cổng container chưa listen | Khai báo nhầm cổng 80 thay vì 8080 | Kiểm tra chính xác cổng container bind socket |
| 11. Thừa cờ `successThreshold` > 1 ở livenessProbe | K8s quy định liveness successThreshold bắt buộc = 1 | Giữ mặc định `successThreshold: 1` cho liveness |
| 12. Quên cờ `-n <namespace>` khi describe event | Kiểm tra sự kiện Probe ở Namespace default | Thêm cờ `-n <namespace>` khi dùng `kubectl describe` |

---

### 1.6. Tóm tắt (2 phút)

```mermaid
graph TD
    Probes[Health Check Probes] --> Startup[1. startupProbe: Bảo vệ app boot chậm]
    Probes --> Readiness[2. readinessProbe: Quyết định nhận traffic Service]
    Probes --> Liveness[3. livenessProbe: Quyết định diệt & restart container]
    
    Probes --> Actions[3 Phương thức kiểm tra]
    Actions --> HTTP[httpGet: HTTP 200-399]
    Actions --> Exec[exec: Exit code 0]
    Actions --> TCP[tcpSocket: Connect Port OK]
    
    Readiness -->|"FAIL"| CutTraffic[Gỡ IP khỏi Service Endpoints]
    Liveness -->|"FAIL"| RestartPod[Kubelet Send SIGKILL & Restart]
```

**Năm điều phải nhớ:**
1. **Ba loại Probe**: `startupProbe` (bảo vệ boot), `readinessProbe` (nhận traffic), `livenessProbe` (diệt/hồi sinh).
2. **Cơ chế xử lý fail**: Readiness fail gỡ IP khỏi Endpoints; Liveness fail tiêu diệt và restart container.
3. **Ba phương thức**: `httpGet` (mã HTTP 200-399), `exec` (exit code 0), `tcpSocket` (mở port OK).
4. **Phân tách Endpoint**: `/healthz` cho liveness nội bộ, `/ready` cho readiness phụ thuộc DB.
5. **Tránh diệt nhầm**: Dùng `startupProbe` cho các ứng dụng boot chậm thay vì tăng liveness delay.

---

## §10. Câu hỏi tự kiểm tra (5 phút)


<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<code>startupProbe</code>, <code>readinessProbe</code>, và <code>livenessProbe</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Tất cả các <code>livenessProbe</code> và <code>readinessProbe</code> đều bị vô hiệu hóa cho tới khi <code>startupProbe</code> thành công.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<code>readinessProbe</code> fail chỉ gỡ IP Pod khỏi Service Endpoints; <code>livenessProbe</code> fail sẽ tiêu diệt và khởi động lại container.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<code>httpGet</code>, <code>exec</code>, và <code>tcpSocket</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Trong khoảng từ 200 đến 399 (mã 2xx và 3xx).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Trả về Exit Code 0.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Định nghĩa số giây Kubelet chờ trước khi thực hiện lượt kiểm tra Probe đầu tiên.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Định nghĩa khoảng thời gian giữa các lần thực hiện Probe định kỳ nối tiếp nhau.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Định nghĩa số lần Probe dính lỗi liên tiếp tối đa (3 lần) trước khi bị tính là thất bại hoàn toàn.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Vì khi DB bị gián đoạn mạng, toàn bộ các Pod trên cụm sẽ bị Kubelet diệt đồng loạt, gây thảm họa sập hệ thống dây chuyền.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Cần bổ sung <code>startupProbe</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Lệnh <code>kubectl describe pod <pod-name></code>.
</div>
</details>

---

## §11. Tài liệu tham khảo

| Nguồn | Địa chỉ URL | Ghi chú |
|---|---|---|
| Kubernetes Probes Documentation | `https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/` | Tài liệu chuẩn K8s Health Check Probes |
| K8s Pod Lifecycle and Probes | `https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes` | Tài liệu vòng đời Pod và Probes |


---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên cụm Kubernetes 1.30+ tiêu chuẩn (hoặc cụm kind/kubeadm lab). Hãy đảm bảo ngữ cảnh dòng lệnh `kubectl config current-context` đã trỏ chính xác vào cụm thực hành trước khi thực thi.

## Khối thực hành — 120 phút

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| Mã tiêu chí | Nội dung tiêu chí | Lệnh kiểm chứng | Kết quả kỳ vọng |
|---|---|---|---|
| TH1 | Tạo Namespace `lab37` phục vụ thực hành Health Check Probes | `kubectl get ns lab37 -o jsonpath='{.status.phase}'` | In ra `Active` |
| TH2 | Triển khai Pod `pod-http-probe` chứa `readinessProbe` và `livenessProbe` dùng `httpGet` | `kubectl get pod pod-http-probe -n lab37 -o jsonpath='{.spec.containers[0].livenessProbe.httpGet.path}'` | In ra `/healthz` |
| TH3 | Pod `pod-http-probe` ở trạng thái `READY 1/1` | `kubectl get pod pod-http-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].ready}'` | In ra `true` |
| TH4 | Giả lập lỗi trên path `/healthz` và kiểm tra cột Restarts tăng lên | `kubectl get pod pod-http-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].restartCount}'` | In ra con số `>= 1` |
| TH5 | Triển khai Pod `pod-exec-probe` sử dụng `exec` với `cat /tmp/healthy` | `kubectl get pod pod-exec-probe -n lab37 -o jsonpath='{.spec.containers[0].livenessProbe.exec.command[1]}'` | In ra `/tmp/healthy` |
| TH6 | Pod `pod-exec-probe` ở trạng thái `READY 1/1` | `kubectl get pod pod-exec-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].ready}'` | In ra `true` |
| TH7 | Xóa file `/tmp/healthy` và kiểm tra Kubelet tự động restart container | `kubectl get pod pod-exec-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].restartCount}'` | In ra con số `>= 1` |
| TH8 | Triển khai Pod `pod-tcp-probe` sử dụng `tcpSocket` cổng 80 | `kubectl get pod pod-tcp-probe -n lab37 -o jsonpath='{.spec.containers[0].readinessProbe.tcpSocket.port}'` | In ra `80` |
| TH9 | Pod `pod-tcp-probe` đạt trạng thái `READY 1/1` | `kubectl get pod pod-tcp-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].ready}'` | In ra `true` |
| TH10 | Triển khai Pod `pod-startup-probe` chứa `startupProbe` | `kubectl get pod pod-startup-probe -n lab37 -o jsonpath='{.spec.containers[0].startupProbe.failureThreshold}'` | In ra `30` |
| TH11 | Kiểm tra `startupProbe` hoạt động bảo vệ Pod không bị diệt nhầm | `kubectl get pod pod-startup-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].ready}'` | In ra `true` |
| TH12 | Tạo Service `svc-probe` và kiểm tra IP Pod bị rút khỏi Endpoints khi readiness fail | `kubectl get ep svc-probe -n lab37 -o jsonpath='{.subsets}'` | Kiểm tra biến động subsets |
| TH13 | Dọn dẹp sạch sẽ tài nguyên lab37 | `test ! -f /tmp/lab37-probe.yaml && echo "CLEAN"` | In ra `CLEAN` |

---

## L1. Điều kiện tiên quyết về môi trường

| Kiểm tra | Lệnh thực hiện | Kết quả kỳ vọng |
|---|---|---|
| Cụm Kubernetes ba node | `kubectl get nodes` | `cp-01`, `worker-01`, `worker-02` ở trạng thái `Ready` |
| Context đúng môi trường lab | `kubectl config current-context` | Đúng context cụm `kubeadm` |
| Quyền tạo tài nguyên | `kubectl auth can-i create pod -n default` | In ra `yes` |

---

## L2. Kiến trúc bài lab Health Check Probes và ba ca hỏng

```mermaid
graph TD
    subgraph Namespace lab37
        PodHTTP[Pod pod-http-probe: httpGet /healthz & /ready]
        PodExec[Pod pod-exec-probe: exec cat /tmp/healthy]
        PodTCP[Pod pod-tcp-probe: tcpSocket Port 80]
        PodStartup[Pod pod-startup-probe: startupProbe failureThreshold 30]
        SvcProbe[Service svc-probe -> Endpoints Dynamic Update]
    end
    
    PodHTTP --> Checkpoint1
    PodExec --> Checkpoint2
    PodTCP --> Checkpoint3
    PodStartup --> Checkpoint4
```

---

## L3. Bước 1: Khởi tạo Namespace `lab37` (10 phút)

### Thao tác 1.1: Tạo Namespace

```bash
kubectl create namespace lab37
```

**CHECKPOINT 1 — Kiểm tra Namespace `lab37`.**

```bash
kubectl get ns lab37 -o jsonpath='{.status.phase}' | grep -qx Active && echo "CHECKPOINT 1 — ĐẠT" || echo "CHECKPOINT 1 — LỖI"
```

---

## L4. Bước 2: Triển khai Probes phương thức `httpGet` và thử nghiệm Liveness Fail (25 phút)

### Thao tác 2.1: Biên soạn Pod `pod-http-probe` có readinessProbe và livenessProbe

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-http-probe
  namespace: lab37
  labels:
    app: http-app
spec:
  containers:
    - name: web
      image: nginx:alpine
      command: ["sh", "-c", "echo 'OK' > /usr/share/nginx/html/healthz; echo 'OK' > /usr/share/nginx/html/ready; nginx -g 'daemon off;'"]
      ports:
        - containerPort: 80
      livenessProbe:
        httpGet:
          path: /healthz
          port: 80
        initialDelaySeconds: 3
        periodSeconds: 3
      readinessProbe:
        httpGet:
          path: /ready
          port: 80
        initialDelaySeconds: 3
        periodSeconds: 3
EOF
```

**CHECKPOINT 2 — Kiểm tra thuộc tính `livenessProbe.httpGet.path`.**

```bash
kubectl get pod pod-http-probe -n lab37 -o jsonpath='{.spec.containers[0].livenessProbe.httpGet.path}' | grep -qx "/healthz" && echo "CHECKPOINT 2 — ĐẠT" || echo "CHECKPOINT 2 — LỖI"
```

**CHECKPOINT 3 — Kiểm tra Pod `pod-http-probe` ở trạng thái `READY 1/1`.**

```bash
sleep 5
kubectl get pod pod-http-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].ready}' | grep -qx true && echo "CHECKPOINT 3 — ĐẠT" || echo "CHECKPOINT 3 — LỖI"
```

### Thao tác 2.2: Giả lập lỗi xóa file `/healthz` làm Liveness Fail để Kubelet restart

```bash
kubectl exec pod-http-probe -n lab37 -- rm -f /usr/share/nginx/html/healthz
```

**CHECKPOINT 4 — Kiểm tra số lần Restarts tăng lên `>= 1`.**

```bash
sleep 12
[ $(kubectl get pod pod-http-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].restartCount}') -ge 1 ] && echo "CHECKPOINT 4 — ĐẠT" || echo "CHECKPOINT 4 — LỖI"
```

---

## L5. Bước 3: Triển khai Probes phương thức `exec` (25 phút)

### Thao tác 3.1: Biên soạn Pod `pod-exec-probe` với lệnh `cat /tmp/healthy`

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-exec-probe
  namespace: lab37
spec:
  containers:
    - name: worker
      image: busybox:1.36
      command: ["sh", "-c", "touch /tmp/healthy; sleep 3600"]
      livenessProbe:
        exec:
          command:
            - cat
            - /tmp/healthy
        initialDelaySeconds: 2
        periodSeconds: 3
EOF
```

**CHECKPOINT 5 — Kiểm tra lệnh `exec` trong Pod spec.**

```bash
kubectl get pod pod-exec-probe -n lab37 -o jsonpath='{.spec.containers[0].livenessProbe.exec.command[1]}' | grep -qx "/tmp/healthy" && echo "CHECKPOINT 5 — ĐẠT" || echo "CHECKPOINT 5 — LỖI"
```

**CHECKPOINT 6 — Kiểm tra Pod `pod-exec-probe` ở trạng thái `READY 1/1`.**

```bash
sleep 4
kubectl get pod pod-exec-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].ready}' | grep -qx true && echo "CHECKPOINT 6 — ĐẠT" || echo "CHECKPOINT 6 — LỖI"
```

### Thao tác 3.2: Giả lập lỗi xóa file `/tmp/healthy` làm `exec` fail

```bash
kubectl exec pod-exec-probe -n lab37 -- rm -f /tmp/healthy
```

**CHECKPOINT 7 — Kiểm tra Kubelet tự động restart container.**

```bash
sleep 12
[ $(kubectl get pod pod-exec-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].restartCount}') -ge 1 ] && echo "CHECKPOINT 7 — ĐẠT" || echo "CHECKPOINT 7 — LỖI"
```

---

## L6. Bước 4: Triển khai Probes phương thức `tcpSocket` và `startupProbe` (25 phút)

### Thao tác 4.1: Biên soạn Pod `pod-tcp-probe` mở socket cổng 80

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-tcp-probe
  namespace: lab37
spec:
  containers:
    - name: web
      image: nginx:alpine
      ports:
        - containerPort: 80
      readinessProbe:
        tcpSocket:
          port: 80
        initialDelaySeconds: 2
        periodSeconds: 3
EOF
```

**CHECKPOINT 8 — Kiểm tra thuộc tính `tcpSocket.port: 80`.**

```bash
kubectl get pod pod-tcp-probe -n lab37 -o jsonpath='{.spec.containers[0].readinessProbe.tcpSocket.port}' | grep -qx 80 && echo "CHECKPOINT 8 — ĐẠT" || echo "CHECKPOINT 8 — LỖI"
```

**CHECKPOINT 9 — Kiểm tra Pod `pod-tcp-probe` ở trạng thái `READY 1/1`.**

```bash
sleep 4
kubectl get pod pod-tcp-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].ready}' | grep -qx true && echo "CHECKPOINT 9 — ĐẠT" || echo "CHECKPOINT 9 — LỖI"
```

### Thao tác 4.2: Triển khai Pod `pod-startup-probe` cho ứng dụng boot chậm

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: pod-startup-probe
  namespace: lab37
spec:
  containers:
    - name: slow-app
      image: busybox:1.36
      command: ["sh", "-c", "sleep 10; touch /tmp/started; touch /tmp/healthy; sleep 3600"]
      startupProbe:
        exec:
          command:
            - cat
            - /tmp/started
        failureThreshold: 30
        periodSeconds: 2
      livenessProbe:
        exec:
          command:
            - cat
            - /tmp/healthy
        periodSeconds: 3
EOF
```

**CHECKPOINT 10 — Kiểm tra `startupProbe.failureThreshold: 30`.**

```bash
kubectl get pod pod-startup-probe -n lab37 -o jsonpath='{.spec.containers[0].startupProbe.failureThreshold}' | grep -qx 30 && echo "CHECKPOINT 10 — ĐẠT" || echo "CHECKPOINT 10 — LỖI"
```

**CHECKPOINT 11 — Kiểm tra Pod boot xong đạt trạng thái `READY 1/1`.**

```bash
sleep 14
kubectl get pod pod-startup-probe -n lab37 -o jsonpath='{.status.containerStatuses[0].ready}' | grep -qx true && echo "CHECKPOINT 11 — ĐẠT" || echo "CHECKPOINT 11 — LỖI"
```

---

## L7. Bước 5: Thử nghiệm biến động Service Endpoints khi Readiness Fail (25 phút)

### Thao tác 5.1: Tạo Service `svc-probe` trỏ vào `pod-http-probe`

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: svc-probe
  namespace: lab37
spec:
  selector:
    app: http-app
  ports:
    - port: 80
      targetPort: 80
EOF
```

**CHECKPOINT 12 — Kiểm tra Service Endpoints nhặt được IP Pod.**

```bash
sleep 3
kubectl get ep svc-probe -n lab37 -o jsonpath='{.subsets[0].addresses[0].ip}' | grep -q "\." && echo "CHECKPOINT 12 — ĐẠT" || echo "CHECKPOINT 12 — LỖI"
```

---

## L8. Dọn dẹp môi trường (10 phút)

### Thao tác 8.1: Dọn dẹp tài nguyên lab37

```bash
kubectl delete namespace lab37
rm -f /tmp/lab37-probe.yaml
```

**CHECKPOINT 13 — Kiểm tra dọn dẹp sạch sẽ.**

```bash
test ! -f /tmp/lab37-probe.yaml && echo "CHECKPOINT 13 — ĐẠT" || echo "CHECKPOINT 13 — LỖI"
```

---

## L9. Xử lý sự cố thường gặp trong lab

| Triệu chứng lỗi | Nguyên nhân gốc rễ | Cách sửa triệt để |
|---|---|---|
| 1. Pod bị Kubelet diệt liên tục (`CrashLoopBackOff`) | `livenessProbe` bị fail do sai path hoặc sai port | Kiểm tra lại path/port trong livenessProbe spec |
| 2. App boot chậm bị liveness kill giữa chừng | Thiếu `startupProbe` che chắn cho thời gian khởi động | Bổ sung `startupProbe` với `failureThreshold: 30` |
| 3. Service không chuyển traffic vào Pod | `readinessProbe` bị fail khiến IP Pod bị gỡ khỏi Endpoints | Chạy `kubectl describe pod` kiểm tra lý do readiness fail |
| 4. Lỗi `exec` probe báo command exit status 1 | Lệnh `exec` trong container không tìm thấy tệp hoặc sai syntax | Test lệnh shell trực tiếp trong terminal container trước |
| 5. Lỗi `httpGet` probe báo status code 404 | Khai báo sai path URL của endpoint healthcheck | Đảm bảo web server trả về 200 OK trên path chỉ định |
| 6. Lỗi `tcpSocket` probe báo connection refused | Container chưa bind cổng socket thành công | Kiểm tra cờ `ports` và cổng ứng dụng lắng nghe |
| 7. Quá tải CPU do Probe check liên tục | Đặt `periodSeconds: 1` quá ngắn | Tăng `periodSeconds` lên 5s hoặc 10s |
| 8. Liveness fail liên tục khi DB bên ngoài bị đứt | Cấu hình `livenessProbe` trỏ nhầm vào endpoint check DB | Tách biệt `/healthz` cho liveness và `/ready` cho readiness |
| 9. ReadinessProbe pass nhưng Pod vẫn bị restart | `livenessProbe` bị fail độc lập | Kiểm tra riêng cấu hình livenessProbe |
| 10. `initialDelaySeconds` quá dài làm chậm readiness | Đặt delay 60s không cần thiết cho ứng dụng nhẹ | Giảm `initialDelaySeconds` xuống 3s cho app mỏng |
| 11. Pod kẹt trạng thái `0/1 READY` | `readinessProbe` fail liên tục nhưng `livenessProbe` vẫn pass | Kiểm tra endpoint readiness trả về mã status gì |
| 12. Quên cờ `-n lab37` khi xem describe pod | Describe Pod ở Namespace `default` không thấy | Luôn thêm `-n lab37` khi chạy `kubectl describe pod` |
| 13. Tệp YAML dry-run bị lỗi indentation | Copy/paste thủ công bị dính tab | Sử dụng `vim` thiết lập `:set expandtab tabstop=2 shiftwidth=2` |
| 14. `successThreshold` > 1 ở livenessProbe bị báo lỗi | API Server quy định livenessProbe successThreshold bắt buộc = 1 | Xóa cờ `successThreshold` ở livenessProbe |

---

## L10. Bài tập mở rộng

- **BT1:** Viết bản kê khai Pod chạy ứng dụng Python Flask có `readinessProbe` kiểm tra kết nối Redis qua `tcpSocket:6379`.
- **BT2:** Viết script Bash tự động giả lập đứt mạng DB để kiểm tra IP Pod tự động biến mất khỏi Service Endpoints.
- **BT3:** Thử nghiệm tác động của `timeoutSeconds: 1` khi giả lập endpoint `/healthz` trả về phản hồi sau 2 giây.
- **BT4:** Cấu hình `startupProbe` loại `httpGet` cho 1 ứng dụng Java Spring Boot giả lập mất 45 giây để boot.
- **BT5:** Sử dụng lệnh `kubectl describe pod` để phân tích mốc thời gian từ lúc Probe fail đến lúc Kubelet gửi `SIGKILL`.
- **BT6:** So sánh lượng request log ghi lại trên Web Server giữa `periodSeconds: 2` và `periodSeconds: 10`.

---

## L11. Hiện vật nộp và tiêu chí chấm điểm

| Hạng mục hiện vật | Tiêu chí chấm điểm đạt | Thang điểm |
|---|---|---|
| Nhật ký 13 Checkpoint | Thực thi thành công 100 % các checkpoint in ra `ĐẠT` | 50 điểm |
| Bản kê khai 3 phương thức Probe | Cấu hình đúng `httpGet`, `exec`, `tcpSocket` và `startupProbe` | 20 điểm |
| Thử nghiệm Giả lập Lỗi & Endpoints | Giả lập thành công liveness fail và readiness fail | 20 điểm |
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
    <span>Sự khác biệt về hành vi xử lý của Kubelet khi <code>readinessProbe</code> bị thất bại so với khi <code>livenessProbe</code> bị thất bại là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Khi <code>readinessProbe</code> fail, Kubelet KHÔNG diệt container mà chỉ gỡ IP của Pod ra khỏi danh sách Service Endpoints để dừng nhận traffic. Khi <code>livenessProbe</code> fail, Kubelet sẽ gửi <code>SIGKILL</code> tiêu diệt và khởi động lại container theo <code>restartPolicy</code>.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Cho rằng cả 2 probe fail đều bị diệt container.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được liveness fail bị restart nhưng không giải thích được việc readiness fail gỡ IP khỏi Endpoints.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chuẩn xác hành vi êm dịu (gỡ Endpoints) vs hành vi mạnh tay (diệt container).</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Nếu Pod không có <code>readinessProbe</code> mà chỉ có <code>livenessProbe</code> thì khi container chưa sẵn sàng, Kubelet sẽ làm gì? — Kubelet vẫn coi Pod sẵn sàng và Service vẫn đẩy traffic vào gây lỗi 502).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q02</span>
    <span>Tại sao các ứng dụng khởi động chậm (như Java Spring Boot) bắt buộc phải cấu hình <code>startupProbe</code>?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Vì nếu không có <code>startupProbe</code>, Kubelet sẽ kích hoạt <code>livenessProbe</code> ngay từ đầu. Do ứng dụng mất 3 phút mới boot xong nên <code>livenessProbe</code> sẽ báo fail và Kubelet lại kill container, tạo ra vòng lặp diệt nhầm vĩnh viễn (<code>CrashLoopBackOff</code>). <code>startupProbe</code> cho phép ứng dụng mở rộng hạn ngạch thời gian boot an toàn.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không giải thích được lý do diệt nhầm của livenessProbe.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được cho ứng dụng boot chậm nhưng không rõ cơ chế vô hiệu hóa livenessProbe của startupProbe.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích chính xác bài toán diệt nhầm và cách giải quyết bằng <code>startupProbe</code>.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Có nên giải quyết bài toán app boot chậm bằng cách tăng <code>initialDelaySeconds</code> của <code>livenessProbe</code> lên 300s không? — KHÔNG nên, vì sẽ làm mất khả năng phát hiện app bị crash trong 5 phút đầu tiên sau khi đã boot xong).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q03</span>
    <span>Ba phương thức hành động (Actions) được dùng để cấu hình Probe là gì và ứng dụng trong những trường hợp nào?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">3 phương thức gồm: <code>httpGet</code> (gửi request HTTP GET tới path/port, dùng cho Web API), <code>exec</code> (chạy câu lệnh shell trong container exit code 0, dùng cho Batch Worker/Script), và <code>tcpSocket</code> (thử mở kết nối cổng TCP, dùng cho Database/Cache daemon).</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không nêu đúng 3 phương thức.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được tên nhưng không làm rõ bối cảnh ứng dụng thực tế của từng loại.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày chính xác cả 3 phương thức và trường hợp ứng dụng thực tiễn.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Phương thức <code>httpGet</code> đánh giá Probe thành công khi mã HTTP trả về nằm trong khoảng nào? — Trong dải từ 200 đến 399).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q04</span>
    <span>Tại sao KHÔNG nên cấu hình <code>livenessProbe</code> trỏ vào đường dẫn endpoint có thực hiện query kiểm tra cơ sở dữ liệu?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Vì nếu DB bị gián đoạn mạng hoặc quá tải tạm thời 10 giây, endpoint đó sẽ trả về fail. Nếu <code>livenessProbe</code> check endpoint này, Kubelet sẽ tiêu diệt và restart ĐỒNG LOẠT tất cả các Pod trên cụm, gây thảm họa sập hệ thống dây chuyền (Cascading Failure).</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Cho rằng liveness check DB là tốt.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được không nên check DB nhưng không giải thích được thảm họa diệt đồng loạt các Pod.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích thấu đáo lý do phân tách <code>/healthz</code> (liveness nội bộ) và <code>/ready</code> (readiness phụ thuộc DB).</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Đường dẫn <code>/ready</code> của <code>readinessProbe</code> có được phép check DB không? — ĐƯỢC phép, vì readiness fail chỉ gỡ IP khỏi Endpoints chứ không làm diệt Pod).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q05</span>
    <span>Ý nghĩa của các tham số <code>initialDelaySeconds</code>, <code>periodSeconds</code>, <code>timeoutSeconds</code> và <code>failureThreshold</code> là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"><code>initialDelaySeconds</code>: số giây chờ trước khi probe lần đầu; <code>periodSeconds</code>: khoảng thời gian giữa các lần probe định kỳ; <code>timeoutSeconds</code>: thời gian chờ phản hồi tối đa của 1 lượt probe; <code>failureThreshold</code>: số lần fail liên tiếp tối đa trước khi công nhận fail toàn bộ.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không giải thích được các tham số.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Giải thích được 2-3 tham số.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày chính xác tuyệt đối định nghĩa và vai trò của cả 4 tham số mốc thời gian.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Nếu <code>periodSeconds: 10</code> và <code>failureThreshold: 3</code> thì Probe sẽ mất bao nhiêu giây fail liên tiếp để bị tính là thất bại? — Mất khoảng 30 giây).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q06</span>
    <span>Ca hỏng "Ứng dụng dính Deadlock treo luồng không tự thoát" được phát hiện và xử lý thế nào bởi Probe?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Khi app dính Deadlock, tiến trình container vẫn chạy (<code>Running</code>) nhưng không trả lời bất kỳ request nào. <code>livenessProbe</code> gửi request HTTP/TCP nhưng bị <code>timeoutSeconds</code> quá hạn ngạch liên tiếp 3 lần (<code>failureThreshold: 3</code>), Kubelet lập tức phát hiện liveness fail và gửi <code>SIGKILL</code> để diệt và khởi động lại container hồi sinh ứng dụng.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không giải thích được cơ chế phát hiện Deadlock.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được diệt container nhưng chưa làm rõ cơ chế timeout và failureThreshold liên tiếp.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích thấu đáo luồng xử lý từ timeout đến <code>SIGKILL</code> của Kubelet.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Nếu không có <code>livenessProbe</code> thì Pod dính Deadlock sẽ hiển thị trạng thái gì trên <code>kubectl get pods</code>? — Vẫn hiển thị <code>Running 1/1</code> giả tạo dù app đã chết hoàn toàn).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q07</span>
    <span>Câu lệnh CLI nào dùng để xem nhật ký các sự kiện cảnh báo Probe fail của một Pod từ terminal?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"><code>kubectl describe pod <pod-name> -n <namespace></code>. Sự kiện Probe fail sẽ được ghi lại trong mục <code>Events</code> ở dưới cùng (ví dụ: <code>Liveness probe failed: HTTP probe failed with statuscode 500</code>).</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Nhầm với lệnh <code>kubectl logs</code>.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu đúng describe pod nhưng không rõ vị trí xem mục Events.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày chuẩn xác câu lệnh CLI và thông điệp event mẫu của Probe fail.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Xem thông tin số lần Pod đã bị Kubelet restart do liveness fail ở cột nào trong <code>kubectl get pods</code>? — Ở cột <code>RESTARTS</code>).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q08</span>
    <span>Tại sao cờ <code>successThreshold</code> trong khối <code>livenessProbe</code> lại BẮT BUỘC phải luôn bằng 1?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Vì đối với <code>livenessProbe</code>, chỉ cần 1 lần kiểm tra thành công là container được tính là đang sống bình thường. Kubernetes API Server quy định cứng <code>successThreshold: 1</code> cho livenessProbe và sẽ trả về lỗi validation nếu đặt con số khác 1.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết quy định này.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được bằng 1 nhưng không rõ lỗi validation của API Server.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày chính xác quy tắc validation cứng của Kubernetes API Server đối với livenessProbe.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Trường <code>successThreshold</code> trong <code>readinessProbe</code> có được phép đặt lớn hơn 1 không? — ĐƯỢC phép, ví dụ đặt bằng 2 để yêu cầu 2 lần tháo gỡ lỗi liên tiếp mới cho Pod nhận traffic trở lại).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q09</span>
    <span>Cú pháp YAML chuẩn để định nghĩa một <code>readinessProbe</code> loại <code>httpGet</code> cổng 8080 đường dẫn <code>/ready</code> là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">readinessProbe:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">httpGet:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">path: /ready</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">port: 8080</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">initialDelaySeconds: 5</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">periodSeconds: 10</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">```</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Cấu hình sai thụt lề hoặc sai từ khóa.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được httpGet nhưng thiếu mốc thời gian.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Viết chuẩn xác tuyệt đối cú pháp YAML spec của readinessProbe.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Nếu cổng container lắng nghe được đặt tên nhãn là <code>http-web</code> thì có thể điền <code>port: http-web</code> thay vì số 8080 được không? — ĐƯỢC phép, Kubelet tự động ánh xạ tên cổng).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q10</span>
    <span>Điểm khác biệt khi sử dụng <code>exec</code> probe với câu lệnh chứa cờ pipe <code>|</code> cần lưu ý điều gì về cú pháp?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">Lệnh <code>exec</code> mặc định không chạy qua shell interpreter. Nếu câu lệnh chứa cờ pipe <code>|</code> hoặc redirect <code>></code>, bắt buộc phải khai báo dạng: <code>command: ["sh", "-c", "lệnh 1 | lệnh 2"]</code> để shell tự phân tích cú pháp pipe.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết lưu ý về sh -c.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được dùng sh -c nhưng không giải thích được lý do thiếu shell interpreter.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích thấu đáo cú pháp bọc <code>sh -c</code> cho các câu lệnh shell phức tạp trong <code>exec</code> probe.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Nếu gõ <code>command: ["cat", "/tmp/a", "|", "grep", "ok"]</code> mà không có <code>sh -c</code> thì chuyện gì xảy ra? — Lệnh <code>cat</code> sẽ tìm tệp tên là <code>|</code> và báo lỗi exit code 1 làm Probe fail).

---</div>
</div>
</details>

<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q11</span>
    <span>Tổng kết quy trình 3 bước vàng để thiết kế Health Check Probes chuẩn Production cho một Microservice là gì?</span>
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
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Thêm <code>startupProbe</code> nếu app boot lâu hơn 15s.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Thêm <code>livenessProbe</code> trỏ vào <code>/healthz</code> (chỉ check nội bộ container) để hồi sinh khi deadlock.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Thêm <code>readinessProbe</code> trỏ vào <code>/ready</code> (check kết nối DB/dịch vụ ngoài) để tạm ngắt traffic khi bận.</div>
  <div style="margin-top: 0.75rem;"><b style="color: var(--accent-primary);">Tiêu chí chấm điểm &amp; Phân tầng năng lực:</b></div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không nêu đúng quy trình.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được 2/3 bước.</div>
  <div style="margin: 0.25rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Trình bày mạch lạc, tự tin bộ 3 bước vàng thiết kế Probes Production.</div>
  <div style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(var(--accent-primary-rgb, 59, 130, 246), 0.08); border-radius: 4px;"><b style="color: var(--accent-primary);">Câu hỏi mở rộng / Đào sâu:</b> (Mục tiêu tiếp theo của bạn trong Buổi 38 là gì? — Học về Log, sự kiện và debug container với <code>kubectl logs</code>, <code>events</code>, <code>describe</code>, <code>exec</code> và <code>ephemeral containers</code>).

---

## V3. Câu chốt để nói khi phỏng vấn

1. <b style="color: var(--accent-primary);">"Phân biệt đúng mục đích của 3 loại Probe là chìa khóa xây dựng hệ thống tự chữa lành (Self-healing) trên Kubernetes."</b>
2. <b style="color: var(--accent-primary);">"Luôn nhớ: Readiness fail chỉ gỡ IP khỏi Service Endpoints để ngừng nhận traffic; Liveness fail mới làm Kubelet diệt và restart container."</b>
3. <b style="color: var(--accent-primary);">"Áp dụng <code>startupProbe</code> là giải pháp chuẩn nhất để che chắn cho các ứng dụng khởi động chậm mà không làm mất khả năng phát hiện lỗi của <code>livenessProbe</code>."</b>
4. <b style="color: var(--accent-primary);">"Tuyệt đối phân tách hai endpoint <code>/healthz</code> (liveness nội bộ) và <code>/ready</code> (readiness phụ thuộc DB) để tránh thảm họa sập cụm dây chuyền."</b>

---</div>
</div>
</details>

---

## V3. Câu chốt để nói khi phỏng vấn

1. **"Phân biệt đúng mục đích của 3 loại Probe là chìa khóa xây dựng hệ thống tự chữa lành (Self-healing) trên Kubernetes."**
2. **"Luôn nhớ: Readiness fail chỉ gỡ IP khỏi Service Endpoints để ngừng nhận traffic; Liveness fail mới làm Kubelet diệt và restart container."**
3. **"Áp dụng `startupProbe` là giải pháp chuẩn nhất để che chắn cho các ứng dụng khởi động chậm mà không làm mất khả năng phát hiện lỗi của `livenessProbe`."**
4. **"Tuyệt đối phân tách hai endpoint `/healthz` (liveness nội bộ) và `/ready` (readiness phụ thuộc DB) để tránh thảm họa sập cụm dây chuyền."**

---

## 4. Đề Thi Thực Hành Bấm Giờ & Thử Thách Tốc Độ (Exam Speed Challenge)

> [!TIP]
> **CHIẾN THUẬT PHÒNG THI THỰC CHIẾN:**
> Đặt đồng hồ bấm giờ đúng thời lượng quy định, đọc kỹ yêu cầu namespace và kiểm tra trạng thái cuối cùng của cụm bằng `kubectl get -o jsonpath` trước khi nộp bài.

## T0. Vì sao có khối này

Khối luyện đề giúp học viên rèn luyện phản xạ gõ lệnh tốc độ cao cho các câu hỏi thuộc miền **`Application Observability and Maintenance` (15 %)** trong kỳ thi CKAD. Trọng tâm bài luyện là kỹ năng biên soạn và bổ sung 3 loại Probe (`startupProbe`, `readinessProbe`, `livenessProbe`) vào bản kê khai Pod/Deployment từ terminal CLI. Tổng thời gian làm bài và tự chấm là đúng 30 phút (1.800 giây).

---

## T1. Luật chơi

1. Mở duy nhất 1 cửa sổ Terminal và 1 tab trình duyệt truy cập tài liệu chính thức `https://kubernetes.io/docs/`.
2. Không sử dụng công cụ AI, không copy/paste các mẫu YAML sẵn từ ngoài tài liệu chính thức.
3. Sử dụng tối đa các alias rút gọn (`k` cho `kubectl`, `$do` cho `--dry-run=client -o yaml`).
4. Tổng thời gian thực hiện 4 câu: **21 phút** (1.260 giây). Thời gian tự chấm bằng script: **9 phút** (540 giây).

---

## T2. Bốn câu kiểu đề thi

### Câu T2.1 — CKAD · Observability — 300 giây
Tạo Pod tên là `liveness-pod` trong Namespace `prod`:
- Ảnh container: `nginx:alpine`
- Thêm `livenessProbe` kiểu `httpGet` cổng `80`, path `/`
- Cấu hình mốc thời gian: `initialDelaySeconds: 5`, `periodSeconds: 10`

### Câu T2.2 — CKAD · Observability — 300 giây
Tạo Pod tên là `readiness-pod` trong Namespace `prod`:
- Ảnh container: `busybox:1.36`, lệnh `sh -c "touch /tmp/ready; sleep 3600"`
- Thêm `readinessProbe` kiểu `exec` với lệnh `cat /tmp/ready`
- Cấu hình mốc thời gian: `periodSeconds: 5`, `failureThreshold: 2`

### Câu T2.3 — CKAD · Observability — 300 giây
Tạo Pod tên là `tcp-startup-pod` trong Namespace `prod`:
- Ảnh container: `nginx:alpine`
- Thêm `startupProbe` kiểu `tcpSocket` cổng `80`
- Cấu hình mốc thời gian: `failureThreshold: 30`, `periodSeconds: 5`

### Câu T2.4 — CKAD · Observability — 360 giây
Tạo Deployment tên là `probe-deploy` trong Namespace `prod`:
- Số bản sao (`replicas`): `2`, ảnh container `nginx:alpine`
- Cấu hình đầy đủ cả 3 loại Probe:
  - `startupProbe`: `tcpSocket` port 80, `failureThreshold: 30`, `periodSeconds: 5`
  - `readinessProbe`: `httpGet` port 80, path `/`, `periodSeconds: 5`
  - `livenessProbe`: `httpGet` port 80, path `/`, `periodSeconds: 10`

---

## T3. Lời giải chuẩn (Đường gõ ngắn nhất)

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
kubectl create ns prod --dry-run=client -o yaml | kubectl apply -f -

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: liveness-pod
  namespace: prod
spec:
  containers:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• name: web</div>
      image: nginx:alpine
      ports:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• containerPort: 80</div>
      livenessProbe:
        httpGet:
          path: /
          port: 80
        initialDelaySeconds: 5
        periodSeconds: 10
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
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: readiness-pod
  namespace: prod
spec:
  containers:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• name: worker</div>
      image: busybox:1.36
      command: ["sh", "-c", "touch /tmp/ready; sleep 3600"]
      readinessProbe:
        exec:
          command:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• cat</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• /tmp/ready</div>
        periodSeconds: 5
        failureThreshold: 2
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
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: tcp-startup-pod
  namespace: prod
spec:
  containers:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• name: web</div>
      image: nginx:alpine
      ports:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• containerPort: 80</div>
      startupProbe:
        tcpSocket:
          port: 80
        failureThreshold: 30
        periodSeconds: 5
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
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: probe-deploy
  namespace: prod
spec:
  replicas: 2
  selector:
    matchLabels:
      app: probe-app
  template:
    metadata:
      labels:
        app: probe-app
    spec:
      containers:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• name: web</div>
          image: nginx:alpine
          ports:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• containerPort: 80</div>
          startupProbe:
            tcpSocket:
              port: 80
            failureThreshold: 30
            periodSeconds: 5
          readinessProbe:
            httpGet:
              path: /
              port: 80
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /
              port: 80
            periodSeconds: 10
EOF
```

---
</div>
</details>

## T4. Bẫy hay gặp

| Bẫy hay gặp | Mất bao nhiêu điểm | Dấu hiệu nhận ra ngay |
|---|---|---|
| 1. Khai báo `successThreshold` > 1 trong livenessProbe | Mất 25 điểm (Câu 1) | API Server báo lỗi validation `Unsupported value` |
| 2. Gõ sai từ khóa `tcpSocket` thành `tcp` hoặc `socket` | Mất 25 điểm (Câu 3) | API Server báo lỗi unknown field |
| 3. Quên cờ `port` trong cấu hình Probe | Mất 25 điểm (Câu 1) | Pod kẹt lỗi missing required field port |
| 4. Khai báo câu lệnh `exec` dạng chuỗi không tách mảng | Mất 25 điểm (Câu 2) | Lệnh exec bị fail do sai định dạng command |
| 5. Quên cờ `-n prod` khi apply Pod spec | Mất 25 điểm (Câu 4) | Tài nguyên bị tạo ở Namespace default |

---

## T5. Bảng tự chấm và Script chấm điểm tự động

### Đoạn script tự kiểm tra và in điểm (Không phụ thuộc vào `jq`)

```bash
#!/bin/bash
SCORE=0

echo "=== KẾT QUẢ TỰ CHẤM BÀI Ô THI BUỔI 37 ==="

# Kiểm câu 1
LIVENESS_PATH=$(kubectl get pod liveness-pod -n prod -o jsonpath='{.spec.containers[0].livenessProbe.httpGet.path}' 2>/dev/null)
if [ "$LIVENESS_PATH" == "/" ]; then
    echo "Câu 1: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 1: THẤT BẠI (0đ)"
fi

# Kiểm câu 2
READINESS_CMD=$(kubectl get pod readiness-pod -n prod -o jsonpath='{.spec.containers[0].readinessProbe.exec.command[1]}' 2>/dev/null)
if [ "$READINESS_CMD" == "/tmp/ready" ]; then
    echo "Câu 2: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 2: THẤT BẠI (0đ)"
fi

# Kiểm câu 3
STARTUP_PORT=$(kubectl get pod tcp-startup-pod -n prod -o jsonpath='{.spec.containers[0].startupProbe.tcpSocket.port}' 2>/dev/null)
if [ "$STARTUP_PORT" == "80" ]; then
    echo "Câu 3: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 3: THẤT BẠI (0đ)"
fi

# Kiểm câu 4
DEPLOY_PROBES=$(kubectl get deploy probe-deploy -n prod -o jsonpath='{.spec.template.spec.containers[0].startupProbe.tcpSocket.port}' 2>/dev/null)
if [ "$DEPLOY_PROBES" == "80" ]; then
    echo "Câu 4: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 4: THẤT BẠI (0đ)"
fi

echo "=========================================="
echo "TỔNG ĐIỂM: $SCORE / 100"
if [ $SCORE -ge 75 ]; then
    echo "ĐÁNH GIÁ: ĐẠT NGƯỠNG AN TOÀN KỲ THI CKAD"
else
    echo "ĐÁNH GIÁ: CHƯA ĐẠT - CẦN LUYỆN LẠI"
fi
```

---

## T6. Kho lệnh rút gọn của buổi

```bash
# Xem sự kiện Probe fail của Pod
kubectl describe pod <pod-name> -n <ns>

# Kiểm tra trường livenessProbe bằng jsonpath
kubectl get pod <pod-name> -n <ns> -o jsonpath='{.spec.containers[0].livenessProbe}'

# Khung YAML Probe httpGet
livenessProbe:
  httpGet: {path: /healthz, port: 8080}
  initialDelaySeconds: 5
  periodSeconds: 10

# Khung YAML Probe exec
readinessProbe:
  exec:
    command: ["cat", "/tmp/ready"]
  periodSeconds: 5
```


---

## Tổng Kết & Lộ Trình Bài Học Tiếp Theo

Kiến thức và kỹ năng thực hành trong bài viết này là mắt xích quan trọng trong hệ thống quản trị và bảo mật Kubernetes chuyên nghiệp. Việc nắm vững cả lý thuyết kiến trúc lẫn thao tác gõ lệnh tốc độ cao trong terminal sẽ giúp bạn tự tin xử lý sự cố thực tế cũng như vượt qua các kỳ thi chứng chỉ quốc tế CKA, CKAD và CKS.

> [!TIP]
> **BÀI TIẾP THEO TRONG CHUỖI BÀI HỌC:**
> Tiếp tục hành trình nâng cao năng lực Kubernetes với bài học tiếp theo: [[Bài 08] Giám Sát Log, Truy Vết Sự Kiện & Debug Container: Logs, Events, Describe, Exec & Ephemeral Debug Container](ckad-08-08-log-su-kien-va-debug-container.html).

{% endraw %}
