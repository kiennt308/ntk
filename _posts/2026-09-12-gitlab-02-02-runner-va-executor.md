---
layout: post
title: "[Bài 02] GitLab Runner & Các Loại Executor: Shell, Docker, Kubernetes Executor & Cơ Chế Đăng Ký Token Mới"
date: 2026-09-12 09:20:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-02
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 2
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.02] Hướng dẫn chuyên sâu GitLab Runner & Các Loại Executor: Shell, Docker, Kubernetes Executor & Cơ Chế Đăng Ký Token Mới: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về GitLab Runner & Các Loại Executor: Shell, Docker, Kubernetes Executor & Cơ Chế Đăng Ký Token Mới."
  - "Thiết kế CI/CD Pipeline chuẩn Enterprise với kiến trúc DAG, tối ưu hóa thời gian build và caching hiệu quả."
  - "Bảo mật chuỗi cung ứng phần mềm với SAST/DAST, Container Scanning và OIDC Authentication."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 02] GITLAB RUNNER & CÁC LOẠI EXECUTOR: SHELL, DOCKER, KUBERNETES EXECUTOR & CƠ CHẾ ĐĂNG KÝ TOKEN MỚI

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · Docker Engine 27.x.
> Mọi đoạn cấu hình trong tệp này dán được vào `config.toml` hoặc `.gitlab-ci.yml` và chạy được.

---





| # | Câu hỏi | Đáp án vắn tắt |
|---|---|---|
| 1 | Một job lấy dữ liệu vào từ đâu và đưa ra bằng cách nào | **Bốn** đường vào — git, cache, artifact, biến — và **hai** đường ra: `artifacts` và **mã thoát**. Log **không** phải đường ra; ngoại lệ duy nhất là `artifacts:reports:dotenv`, và nó là một dạng artifact |
| 2 | Kể tám pha; pha nào chứa lệnh của mình | `prepare_executor` → `prepare_script` → `get_sources` → `restore_cache` → `download_artifacts` → **`step_script`** → `after_script` → `archive_cache`/`upload_artifacts`. Không có dòng `Executing "step_script"` trong log nghĩa là **lệnh chưa chạy lần nào** |
| 3 | Cache khác artifact ở đâu | Ở **sự đảm bảo**. Artifact là hợp đồng, thiếu thì job đỏ ở pha 5. Cache là tối ưu, thiếu thì runner ghi một dòng log rồi chạy tiếp — **cache miss làm job chậm, không làm job hỏng** (QT 5.2 buổi 01) |
| 4 | Job `pending` không có log — chẩn đoán thế nào | Log chỉ tồn tại **sau khi runner nhận job**, nên `pending` thì không có gì để đọc. Hỏi API `runners/all` và so `tags`. Với mặc định, phải **60 phút** job mới đổi màu (QT 6.3 buổi 01) |
| 5 | Ô nào của bảng hai thuộc tính nguy hiểm nhất | **Im lặng + không chặn** — job xanh, sản phẩm sai. Thời gian phát hiện tính bằng **tuần**, và người phát hiện thường là người dùng (QT 7.1 buổi 01) |



Buổi 01 dựng mô hình *bên trong* một job và để lại một câu hỏi chưa trả lời. BTVN 4 câu 3 hỏi thẳng nó:

> *Trong tám pha, pha nào **không** phụ thuộc vào `.gitlab-ci.yml` mà phụ thuộc vào cấu hình runner?*

Trả lời câu đó là bước ra khỏi tệp YAML và nhìn thấy **tệp thứ hai**. Đó là bước chuyển từ "người viết pipeline" sang "người hiểu nền tảng CI", và nó quyết định người ta gỡ được loại lỗi nào.

**Luận đề trung tâm.**

> **Một job được cấu hình bởi HAI tệp do HAI người viết, và hai người ấy thường không nói chuyện với nhau: `.gitlab-ci.yml` nói job LÀM GÌ, `config.toml` nói job CHẠY Ở ĐÂU VÀ VỚI QUYỀN GÌ. Ranh giới giữa hai tệp chính là ranh giới giữa "lỗi của tôi" và "lỗi của hạ tầng" — và phần lớn thời gian gỡ lỗi CI bị mất vì người ta đi tìm ở nhầm tệp.**

```
  NGƯỜI VIẾT PIPELINE                          NGƯỜI VẬN HÀNH RUNNER
  .gitlab-ci.yml                               config.toml
  ├── job làm gì (script)                      ├── executor nào
  ├── chạy trên image nào (image:)             ├── image mặc định, image được phép
  ├── cần artifact của ai                      ├── concurrent, limit, request_concurrency
  ├── chạy khi nào (rules)                     ├── tags runner phục vụ
  └── đòi runner có tag gì (tags)              ├── volume được mount (socket!)
                                               └── mạng job nằm trong
          │                                            │
          └──────────────┬─────────────────────────────┘
                         ▼
              TÁM PHA CỦA BUỔI 01
     pha 1,2  ← CHỈ config.toml           ("lỗi hạ tầng")
     pha 3    ← config.toml + biến GIT_*  (ranh giới, hay cãi nhau nhất)
     pha 4–8  ← chủ yếu .gitlab-ci.yml    ("lỗi của tôi")
```

| Kết quả buổi 01 | Nguồn | Dùng ở đâu hôm nay |
|---|---|---|
| Tám pha | buổi 01 QT 4.2 | **Toàn bộ §4** — hôm nay tách tám pha thành hai nhóm theo tệp cấu hình |
| Executor quyết định cái gì tồn tại giữa hai job | buổi 01 QT 6.1 | §5 — buổi 01 **phát biểu**, hôm nay **đo ba kênh rò rỉ** |
| Job không nằm trong mạng runner | buổi 01 QT 6.2 | §5 và §6 — hôm nay thấy **dòng cấu hình** sinh ra hành vi đó |
| `tags` là định tuyến duy nhất | buổi 01 QT 6.3 | §7 — hôm nay thêm **hai điều kiện độc lập nữa** ngoài tag |
| Bảng hai thuộc tính hỏng | buổi 01 QT 7.1 | §5, §6, §7 — đây là **lần thứ HAI** khoá học dùng bảng này |

Cũng là **lần thứ HAI** khoá học áp quy tắc *hành vi phụ thuộc phiên bản thì phải ĐO, không tra tài liệu* — lần đầu ở lab buổi 01 bước 4 khi đo mã thoát trong ống dẫn. Hôm nay có bốn đại lượng phải đo, liệt kê ở §5 và §6.

**Ba câu hỏi trung tâm của buổi:**

1. Khi pipeline hỏng, làm sao biết phải sửa `.gitlab-ci.yml` hay phải đi gọi người vận hành runner?
2. Bốn executor khác nhau ở **một trục duy nhất** nào, và trục đó quyết định lớp lỗi nào biến mất?
3. Job đang xếp hàng chờ — thêm runner có giúp không, và làm sao biết **trước** khi thêm?

---



| # | Làm được gì | Hiện vật chứng minh |
|---|---|---|
| LĐ1 | Nhìn một lỗi CI và nói được nó thuộc `.gitlab-ci.yml` hay `config.toml` | Bảng phân loại 6 sự cố ở lab bước 1 |
| LĐ2 | Tìm, đọc và giải thích được `config.toml` của một runner bất kỳ | Lab bước 1, CHECKPOINT 2 |
| LĐ3 | Đo được ba kênh rò rỉ trạng thái của executor `shell` | Ba bằng chứng ở lab bước 2 |
| LĐ4 | Đo được chi phí khởi tạo của từng executor và nói ra con số | `chi-phi-khoi-tao.tsv` ở lab bước 3 |
| LĐ5 | Đo được `concurrent` thật bằng hàng đợi, không bằng đọc tệp | `do-concurrent.tsv` ở lab bước 3 |
| LĐ6 | Chẩn đoán được job `pending` theo **ba** điều kiện độc lập | Lab bước 4, CHECKPOINT 9 |
| LĐ7 | Chỉ ra được rủi ro của Docker socket trong job và nêu đường thay thế | Lab bước 4, CHECKPOINT 10 |
| LĐ8 | Thiết kế được đội hình runner cho một tổ chức nhiều đội, có lập luận | `doi-hinh-runner.md` ở lab bước 5 |

---



| Cần biết | Mức yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Tám pha của một job | **Vận dụng** | Buổi 01 QT 4.2 — **tiền đề của toàn bộ §4** |
| Executor quyết định cái gì tồn tại giữa hai job | Vận dụng | Buổi 01 QT 6.1 |
| Job không nằm trong mạng runner | Nhớ | Buổi 01 QT 6.2 |
| `tags` là cơ chế định tuyến | Vận dụng | Buổi 01 QT 6.3 — §7 mở rộng nó |
| Bảng hai thuộc tính hỏng | Vận dụng | Buổi 01 QT 7.1 |
| Đọc được TOML ở mức bảng và khoá | Nhớ | TOML có ba cấu trúc: khoá-giá trị, `[bảng]`, `[[mảng bảng]]`. Học 10 phút là đủ |
| `docker exec`, `docker stats` | Nhớ | Lab dùng để đọc `config.toml` và đo nút cổ chai |

---



### 3.1. Đối chiếu thuật ngữ

| Tiếng Việt | Tiếng Anh | Trong bài dùng gì | Ghi chú |
|---|---|---|---|
| bộ chạy | runner | `runner` | Tiến trình nhận job từ GitLab |
| bộ thực thi | executor | `executor` | Cơ chế runner dùng để tạo môi trường chạy |
| mục runner | runner entry | tiếng Việt | Một khối `[[runners]]` trong `config.toml` |
| tệp cấu hình runner | — | `config.toml` | Tệp thứ hai của luận đề hôm nay |
| mã xác thực runner | runner authentication token | tiếng Việt | Dạng `glrt-…`, thay cho registration token từ GitLab 16.0 |
| nhịp tim | heartbeat | tiếng Việt | Trường `contacted_at` trong API |
| số job chạy đồng thời | concurrency | `concurrent`, `limit` | Hai khoá khác nhau, xem QT 6.1 |
| số yêu cầu hỏi việc đồng thời | request concurrency | `request_concurrency` | **Không** phải số job, xem QT 6.3 |
| mức cô lập | isolation level | tiếng Việt | Trục duy nhất để chọn executor |
| rò rỉ trạng thái | state leakage | tiếng Việt | Ba kênh, xem QT 5.2 |
| chi phí khởi tạo | startup overhead | tiếng Việt | Cái giá của mức cô lập |
| tự co giãn | autoscaling | tiếng Việt | Buổi 13 xử lý đầy đủ |
| ổ cắm Docker | Docker socket | `/var/run/docker.sock` | Một dòng cấu hình phá hết cô lập |
| đặc quyền | privileged | `privileged` | Cờ trong `config.toml` |
| tạm dừng | paused | `paused` | Trạng thái riêng, khác `offline` |
| runner cấp instance/group/project | instance/group/project runner | tiếng Anh | Ba mức phạm vi, xem QT 7.1 |
| bề mặt tấn công | attack surface | tiếng Việt | Buổi 28 xử lý đầy đủ |
| runner ma | zombie runner | tiếng Việt | Runner `online` nhưng không nhận job nào trong nhiều ngày |



Mọi câu hỏi "sửa ở đâu" trong CI/CD quy về một câu hỏi nhỏ hơn: **thứ này thuộc `.gitlab-ci.yml` hay `config.toml`?**

Giá trị thực dụng: hai tệp thuộc hai người và thường thuộc hai đội. Người viết pipeline sửa được tệp thứ nhất bất cứ lúc nào, một mình, và thay đổi chỉ ảnh hưởng project của họ. Tệp thứ hai thì ngược lại: sửa nó là hành động vận hành, ảnh hưởng mọi project dùng runner đó, và thường phải qua người khác. Nhầm tệp không chỉ tốn thời gian gỡ lỗi — nó còn làm người ta đề nghị sai người.

Mô hình này quay lại ở buổi 07 (gỡ rối có hệ thống), buổi 44 (pipeline tập trung, nơi xuất hiện tệp thứ ba là template dùng chung), và buổi 47 (sự cố runner, nơi gần như mọi sự cố nằm ở tệp thứ hai).

### 3.3. Mô hình tư duy 2: một trục duy nhất là mức cô lập

Bốn executor thường được trình bày như một danh sách tính năng. Cách nhìn ấy không giúp chọn. Cách nhìn giúp chọn là xếp chúng trên **một trục**: mức cô lập giữa job và mọi thứ khác.

```
   thấp ◄───────────────── MỨC CÔ LẬP ─────────────────► cao
   shell        docker        docker-autoscaler      kubernetes
   ▲                                                       ▲
   chi phí khởi tạo ≈ 0                    chi phí khởi tạo lớn nhất
   lớp lỗi "chạy máy tôi thì được" còn nguyên   lớp lỗi ấy biến mất
```

Giá trị thực dụng: khi ai đó hỏi "nên dùng executor nào", câu trả lời không phải "cái nào nhanh hơn" mà là **"job này cần cô lập tới mức nào, và ta chịu được bao nhiêu giây khởi tạo"**. Câu hỏi thứ hai có số; câu hỏi đầu có tiêu chí. Cả hai trả lời được trong một cuộc họp.

Mô hình này quay lại ở buổi 13 (chọn executor ở quy mô), buổi 23 (build image, nơi mức cô lập là **tiêu chí chọn duy nhất**), buổi 28 (mô hình đe doạ).

### 3.4. Mô hình tư duy 3: hàng đợi, không phải số máy

Job xếp hàng chờ là một bài toán hàng đợi: có tỉ lệ job đến, có tỉ lệ phục vụ, và thời gian chờ là hàm của **tỉ số** giữa hai cái. Số runner chỉ là một trong các yếu tố quyết định tỉ lệ phục vụ — CPU, đĩa và mạng của máy chủ cũng vậy.

Giá trị thực dụng: khi hàng đợi dài, phản xạ thông thường là thêm runner. Phản xạ đúng là **đo xem tỉ lệ phục vụ bị chặn bởi cái gì**. Nếu nút cổ chai là CPU máy chủ thì thêm runner làm mỗi job chậm hơn, và tổng thời gian **tăng** — đây là QT 6.2, và bài lab đo hiện tượng ấy.

Mô hình này quay lại ở buổi 13 (autoscaling), buổi 14 (đường găng), buổi 46 (chi phí runner tính bằng tiền).

---

### 1.1. Hai tệp cấu hình và ranh giới giữa chúng (9 phút)

### 4.1. Tệp thứ hai nằm ở đâu

**Nguyên lý cốt lõi:** Mỗi job được cấu hình bởi **hai** tệp: `.gitlab-ci.yml` nói job **làm gì**, `config.toml` nói job **chạy ở đâu và với quyền gì**.

**Giải thích cơ chế ngầm:** Runner là một tiến trình chạy độc lập với GitLab. Khi nó hỏi GitLab "có việc gì cho tôi không", GitLab trả về nội dung job đã được phân giải từ `.gitlab-ci.yml`. Nhưng **cách** thực thi nội dung ấy — dựng container nào, mount volume gì, dùng mạng nào, cho phép bao nhiêu job chạy song song — hoàn toàn do runner tự quyết theo `config.toml` của nó. GitLab không biết và không kiểm soát được phần đó.

Đây là lý do hai người khác nhau viết hai tệp: người viết pipeline không cần quyền trên máy runner, và người vận hành runner không cần biết project làm gì.

| Thứ này | Thuộc tệp nào |
|---|---|
| Job chạy lệnh gì | `.gitlab-ci.yml` |
| Job chạy trên image nào | **Cả hai** — `image:` trong job thắng, `config.toml` cho mặc định |
| Job chạy song song bao nhiêu cái | `config.toml` |
| Job đòi runner có tag gì | `.gitlab-ci.yml` |
| Runner phục vụ tag gì | `config.toml` (và giao diện GitLab) |
| Job có Docker socket không | `config.toml` |
| Job nằm trong mạng nào | `config.toml` |
| Job lấy artifact của ai | `.gitlab-ci.yml` |
| Cache lưu ở đâu | `config.toml` |
| Cache gồm thư mục nào | `.gitlab-ci.yml` |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hai người tranh luận về một lỗi: một người mở `.gitlab-ci.yml`, một người mở log runner, và cả hai đều đúng một nửa. Cuộc tranh luận ấy kéo dài vì không ai đặt câu hỏi phân loại trước: *lỗi này xuất hiện ở pha nào?*

**Minh hoạ.**

```bash
# Tìm config.toml của runner đang chạy trong container
docker exec lab-runner cat /etc/gitlab-runner/config.toml

# Ba dòng đáng đọc trước tiên
docker exec lab-runner sh -c \
  'grep -E "^concurrent|executor|volumes" /etc/gitlab-runner/config.toml'
```

Vị trí chuẩn của tệp: `/etc/gitlab-runner/config.toml` khi runner chạy như dịch vụ hệ thống hoặc trong container; `~/.gitlab-runner/config.toml` khi chạy dưới người dùng thường. Với runner cài bằng Helm trên Kubernetes, nội dung tệp nằm trong ConfigMap sinh từ `values.yaml` — xem `labs/k8s/values.yaml` của khoá.

### 4.2. Ba trong tám pha không đọc YAML

Đây là câu trả lời cho BTVN 4 câu 3 của buổi 01, và nó là phần có giá trị thực dụng cao nhất của §4.

**Nguyên lý cốt lõi:** Trong tám pha của buổi 01, **ba pha đầu** gần như không đọc `.gitlab-ci.yml`: chúng do `config.toml` và hạ tầng quyết định. Lỗi ở ba pha ấy thì sửa YAML **không giúp gì**.

**Giải thích cơ chế ngầm:** Pha `prepare_executor` chạy **trước khi** runner biết gì về nội dung job ngoài `image` — nó dựng môi trường theo `executor` và các tuỳ chọn trong `config.toml`. Pha `prepare_script` nạp biến và chuẩn bị shell, cũng theo cấu hình runner. Pha `get_sources` là ranh giới: nó đọc vài biến `GIT_*` từ YAML nhưng phần lớn hành vi — xác thực, mạng, thư mục build, chiến lược dọn — đến từ runner.

| Pha | Ai quyết định | Lỗi điển hình | Ai sửa |
|---|---|---|---|
| 1. `prepare_executor` | **`config.toml`** | Không kéo được image, thiếu quyền Docker, executor cấu hình sai | Người vận hành runner |
| 2. `prepare_script` | **`config.toml`** | Image không có shell, không ghi được biến dạng tệp | Người vận hành runner |
| 3. `get_sources` | **Ranh giới** | Không phân giải được tên GitLab, xác thực hỏng, hết đĩa | Thường là người vận hành; đôi khi là biến `GIT_*` trong YAML |
| 4. `restore_cache` | `.gitlab-ci.yml` + vị trí kho cache trong `config.toml` | Cache miss (không làm đỏ) | — |
| 5. `download_artifacts` | `.gitlab-ci.yml` | Thiếu artifact, `needs` sai | Người viết pipeline |
| 6. `step_script` | `.gitlab-ci.yml` | Lỗi lệnh, lỗi code | Người viết pipeline |
| 7. `after_script` | `.gitlab-ci.yml` | Xem buổi 01 QT 4.3 | Người viết pipeline |
| 8. `archive_cache` / `upload_artifacts` | `.gitlab-ci.yml` + hạn mức | Mẫu không khớp, vượt hạn mức | Người viết pipeline |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Học viên sửa `script` năm lần mà lỗi không đổi — vì lỗi ở pha 1 hoặc pha 3. Buổi 01 đã cho mẹo nhận ra trong 5 giây: nếu log **không có** dòng `Executing "step_script" stage of the job script` thì lệnh chưa chạy lần nào, tức lỗi nằm ở phía hạ tầng.

**Minh hoạ.**

```bash
# Phân loại một job hỏng: thuộc phía nào?
JOB_ID=123
LOG=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        "$GITLAB/api/v4/projects/$PID/jobs/$JOB_ID/trace" \
      | sed 's/\x1b\[[0-9;K]*[a-zA-Z]//g')

if echo "$LOG" | grep -q 'Executing "step_script"'; then
  echo "PHÍA PIPELINE — lệnh đã chạy, sửa .gitlab-ci.yml hoặc sửa code"
else
  echo "PHÍA HẠ TẦNG — lệnh chưa chạy lần nào, xem config.toml và log runner"
  echo "$LOG" | grep -E 'Preparing the|Preparing environment|Getting source' | tail -1
fi
```

**Con số cần nhớ: 3 trên 8 pha thuộc phía hạ tầng.** Nói cách khác, khoảng 37% các chỗ một job có thể hỏng nằm ngoài tầm với của người viết pipeline. Đó là lý do câu hỏi phân loại phải đặt **trước** mọi việc sửa.

### 4.3. Sửa tệp thứ hai là hành động vận hành

**Nguyên lý cốt lõi:** Sửa `config.toml` là **hành động vận hành** ảnh hưởng tới **mọi project** dùng runner đó, không phải thay đổi cục bộ như sửa `.gitlab-ci.yml`.

**Giải thích cơ chế ngầm:** Một runner phục vụ nhiều project. Đổi `concurrent`, đổi `volumes`, đổi image mặc định — mọi project đang dùng runner ấy nhận thay đổi ngay, không qua merge request, không có ai review, và không có lịch sử git để đối chiếu. So sánh: đổi `.gitlab-ci.yml` là một commit, có tác giả, có review, và chỉ ảnh hưởng một project.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline của một đội gãy mà đội đó không đổi gì. Câu hỏi đầu tiên phải hỏi là *"có ai đổi `config.toml` của runner không"*, và câu hỏi ấy thường không hỏi được vì không có ai ghi lại.

**Minh hoạ.**

```bash
# Quy trình tối thiểu trước khi sửa config.toml — ba bước, không bỏ bước nào
# 1. Sao lưu, có mốc thời gian
docker exec lab-runner sh -c \
  'cp /etc/gitlab-runner/config.toml /etc/gitlab-runner/config.toml.bak.$(date +%Y%m%d-%H%M%S)'

# 2. Đo phạm vi ảnh hưởng: runner này đang phục vụ bao nhiêu project
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/runners/$RUNNER_ID/jobs?per_page=100" \
| jq -r '[.[].pipeline.project_id] | unique | length' \
| xargs -I{} echo "runner này đã chạy job cho {} project khác nhau"

# 3. Sửa, rồi kiểm ngay bằng một pipeline thử — đừng chờ người khác phát hiện hộ
```

> **Đây là đại lượng phải ĐO, không tra tài liệu.** Việc runner có **tự nạp lại** `config.toml` khi tệp đổi hay phải khởi động lại tiến trình là hành vi **phụ thuộc phiên bản**. Bài lab bước 1 đo trực tiếp: sửa `concurrent`, không khởi động lại, đẩy 6 job, đếm số job chạy song song. Đây là **lần thứ HAI** khoá học áp quy tắc này — lần đầu ở buổi 01 lab bước 4.

---

### 1.2. Bốn executor và một trục duy nhất: mức cô lập (11 phút)

### 5.1. Trục để chọn không phải tốc độ

**Nguyên lý cốt lõi:** Bốn executor xếp theo **một trục duy nhất — mức cô lập**. Cô lập càng cao thì lớp lỗi "chạy máy tôi thì được" càng biến mất, và **chi phí khởi tạo** càng lớn. Tốc độ chạy job **không** phải trục để chọn.

**Giải thích cơ chế ngầm:** Cái mà một executor cung cấp là **một môi trường**. Sự khác nhau giữa bốn executor nằm ở việc môi trường ấy được cô lập tới đâu khỏi (a) máy chủ, (b) các job khác, (c) các job trước đó. Tốc độ **chạy** một lệnh thì gần như giống nhau trên cả bốn — cùng nhân, cùng CPU. Cái khác nhau là **chi phí dựng và dỡ môi trường**, và đó là cái giá phải trả cho cô lập.

| Executor | Môi trường job là gì | Cô lập khỏi máy chủ | Cô lập khỏi job trước | Chi phí khởi tạo |
|---|---|---|---|---|
| `shell` | Chính máy cài runner | **Không** | **Không** | ≈ 0 giây |
| `docker` | Container mới từ `image` | Một phần — trừ khi mount socket | **Có** | bậc 1–5 giây (image có sẵn) |
| `docker-autoscaler` | Container trên máy ảo **dựng riêng** | **Có** | Có | bậc 30–120 giây (dựng máy) |
| `kubernetes` | Pod mới trong cụm | Có | Có | bậc 5–20 giây (chờ xếp lịch) |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Một đội chọn `shell` "cho nhanh" rồi sáu tháng sau không ai dám dựng lại máy runner, vì không ai biết trên đó đã cài những gì. Chi phí thật của lựa chọn ấy không nằm ở tốc độ mà ở chỗ nó biến máy runner thành một thứ không tái lập được.

**Minh hoạ.**

```yaml
# Job đo chi phí khởi tạo — chạy trên cả hai runner rồi so
# Chạy trên runner docker
do-khoi-tao-docker:
  tags: [docker]
  image: alpine:3.20
  script:
    - echo "bat dau $(date +%s.%N)"
    - true
# Chạy trên runner shell
do-khoi-tao-shell:
  tags: [shell-lab]
  script:
    - echo "bat dau $(date +%s.%N)"
    - true
```

Chi phí khởi tạo suy ra bằng `duration` của job trừ đi thời gian `script` thật (ở đây gần bằng 0). Lab bước 3 làm chính xác phép trừ này.

**Ba con số 0 giây / 1–5 giây / 5–20 giây là đại lượng loại (c) — phải đo.** Chúng phụ thuộc tốc độ đĩa, image đã có sẵn hay chưa, và tải của cụm. Đặc biệt, chi phí kéo một image 800 MB lần đầu là **bậc phút**, không phải bậc giây — bài lab đo cả hai ca.

### 5.2. Ba kênh rò rỉ của executor `shell`

Đây là câu trả lời cho BTVN 4 câu 1 của buổi 01.

**Nguyên lý cốt lõi:** Executor `shell` rò rỉ trạng thái qua **ba kênh**: (a) hệ tệp ngoài thư mục dự án; (b) tiến trình nền còn sống sau khi job kết thúc; (c) trạng thái công cụ toàn cục — biến trong profile, cấu hình git, gói đã cài.

**Giải thích cơ chế ngầm:** Với `shell`, môi trường job **là chính máy chủ**. Runner chỉ tạo một thư mục build rồi chạy script trong đó; nó không có cơ chế nào hoàn tác những gì script đã làm ở ngoài thư mục ấy. Ba kênh trên là ba loại "ở ngoài thư mục ấy" mà một script bình thường hay đụng tới.

| Kênh | Ví dụ cụ thể | Hậu quả |
|---|---|---|
| (a) Hệ tệp ngoài thư mục dự án | `echo x > /tmp/token`, `~/.aws/credentials`, `~/.npmrc` | Job sau đọc được **secret** của job trước — đây cũng là lối vào số 3 trong mô hình đe doạ buổi 28 |
| (b) Tiến trình nền còn sống | `npm start &`, `docker run -d`, một server test không được tắt | Job sau thấy cổng bị chiếm, hoặc tệ hơn: **kết nối nhầm vào service của job trước** và test qua một cách sai |
| (c) Trạng thái công cụ toàn cục | `npm i -g`, `pip install --user`, `git config --global`, sửa `~/.bashrc` | Pipeline xanh nhờ gói do job khác cài **tuần trước**; ngày dựng lại máy thì đỏ hàng loạt |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ba dấu hiệu, xếp theo mức khó chịu tăng dần: pipeline xanh trên runner cũ và đỏ trên runner mới; `which <công-cụ>` trong job trả về `/usr/local/bin` thay vì đường dẫn trong image; và dấu hiệu tệ nhất — **không có dấu hiệu nào**, cho tới ngày máy runner được dựng lại.

Ô của bảng hai thuộc tính: **im lặng, không chặn**. Đây là ô nguy hiểm nhất, và đây là **lần thứ HAI** khoá học gặp một ca rơi vào ô đó.

**Minh hoạ.**

```yaml
# Ba job chứng minh ba kênh rò rỉ. Chạy trên runner shell, theo thứ tự.
stages: [ghi, doc]

ro-ri-a-he-tep:
  stage: ghi
  tags: [shell-lab]
  script:
    - echo "bi-mat-cua-job-truoc" > /tmp/ro-ri-a.txt

ro-ri-b-tien-trinh:
  stage: ghi
  tags: [shell-lab]
  script:
    - (sleep 600 & echo "$!" > /tmp/pid-ro-ri.txt) # tiến trình nền sống 10 phút

ro-ri-c-cong-cu:
  stage: ghi
  tags: [shell-lab]
  script:
    - git config --global user.email "ro-ri-c@lab.local"

doc-ba-kenh:
  stage: doc
  tags: [shell-lab]
  script:
    - echo "kenh a: $(cat /tmp/ro-ri-a.txt 2>/dev/null || echo KHONG)"
    - echo "kenh b: $(ps -p "$(cat /tmp/pid-ro-ri.txt 2>/dev/null)" >/dev/null 2>&1 && echo CON-SONG || echo DA-CHET)"
    - echo "kenh c: $(git config --global user.email 2>/dev/null || echo KHONG)"
    # Trên runner shell: cả ba đều rò rỉ. Trên runner docker: cả ba đều KHÔNG.
```

### 5.3. Một dòng cấu hình phá hết cô lập

**Nguyên lý cốt lõi:** Executor `docker` cô lập hệ tệp nhưng **không** cô lập Docker socket khi socket được mount. Job có socket là job có quyền **tương đương root trên máy chủ**.

**Giải thích cơ chế ngầm:** Docker socket là giao diện điều khiển đầy đủ của Docker daemon, và daemon chạy dưới quyền root. Tiến trình nào gọi được socket ấy thì tạo được container bất kỳ với tuỳ chọn bất kỳ — kể cả container mount thẳng `/` của máy chủ. Không có phân quyền bên trong socket: có socket là có tất cả.

Hệ quả: mức cô lập mà `docker` mang lại bị vô hiệu hoá bởi **một dòng** trong `config.toml`.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dòng này trong `config.toml`:

```toml
[runners.docker]
  volumes = ["/cache", "/var/run/docker.sock:/var/run/docker.sock"]
```

Hoặc dòng này, tệ tương đương:

```toml
[runners.docker]
  privileged = true
```

**Minh hoạ.** Chứng minh trong ba lệnh:

```yaml
chung-minh-socket-la-root:
  image: docker:27-cli
  script:
    - docker version --format '{{.Server.Version}}'   # job nói chuyện được với daemon máy chủ
    # Ba dòng dưới đây đọc được /etc/shadow của MÁY CHỦ từ bên trong job.
    # Chạy trong lab để thấy tận mắt; đừng chạy ở nơi làm việc.
    - docker run --rm -v /:/host alpine:3.20 head -3 /host/etc/hostname
    - echo "job vua doc duoc he tep MAY CHU — cach ly da bi vo hieu hoa"
```

**Con số cần nhớ: 1 dòng.** Một dòng cấu hình đủ để vô hiệu hoá toàn bộ mức cô lập của executor. Đây là lý do buổi 23 dành trọn cho ba đường build image **không cần** socket (kaniko, buildah, BuildKit rootless), và buổi 28 xếp socket là **lối vào số 1** trong mô hình đe doạ của pipeline.

### 5.4. `kubernetes` đổi bài toán, không xoá bài toán

**Nguyên lý cốt lõi:** Executor `kubernetes` đổi bài toán từ "máy có đủ tài nguyên không" sang "pod có được xếp lịch không". Job `pending` vì thiếu tài nguyên cụm **trông giống hệt** job `pending` vì không có runner khớp tag.

**Giải thích cơ chế ngầm:** Với `kubernetes`, runner không tự chạy job — nó tạo một pod và chờ cụm xếp lịch pod ấy. Nếu cụm hết CPU, hết bộ nhớ, hoặc không node nào thoả `nodeSelector`, pod nằm `Pending` và job nằm chờ. Từ phía GitLab, trạng thái job trông y hệt ca không có runner: `pending`, không log. Nhưng nguyên nhân, người phải sửa, và cách sửa đều khác hẳn.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chẩn đoán chỉ bằng API GitLab và kết luận "thiếu runner", rồi đăng ký thêm runner — mà cụm vẫn hết tài nguyên, nên không có gì thay đổi. Phân biệt bằng cách hỏi **hai** nguồn:

```bash
# Nguồn 1 — phía GitLab: có runner khớp không?
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/all" \
| jq -r '.[] | "\(.id) online=\(.online) paused=\(.paused)"'

# Nguồn 2 — phía cụm: pod có được xếp lịch không?
kubectl get pods -n gitlab-runner --field-selector=status.phase=Pending
kubectl get events -n gitlab-runner --sort-by=.lastTimestamp | tail -20
# Dòng "0/3 nodes are available: Insufficient cpu" là câu trả lời, và nó KHÔNG có ở phía GitLab
```

**Minh hoạ.** Đặt giới hạn tài nguyên trong cấu hình runner Kubernetes để thấy ranh giới:

```toml
# mảnh — dán vào phần runners.kubernetes của config.toml
[runners.kubernetes]
  cpu_request    = "200m"
  memory_request = "256Mi"
  cpu_limit      = "1"
  memory_limit   = "1Gi"
  poll_timeout   = 600     # sau 600 giây chờ pod, runner bỏ cuộc và job ĐỎ
```

`poll_timeout` là chỗ ca im lặng này **cuối cùng cũng trở thành ồn ào** — nhưng phải chờ hết hạn giờ đó. Ô của bảng hai thuộc tính: **im lặng, có chặn**.

---

### 1.3. `config.toml`: hàng đợi, `concurrent`, `limit` (9 phút)

### 6.1. Hai trần, và trần thật là min của hai

Đây là câu trả lời cho BTVN 4 câu 2 của buổi 01.

**Nguyên lý cốt lõi:** `concurrent` là trần **toàn cục** của một tiến trình runner; `limit` là trần của **một mục runner** trong tệp đó. Số job thật sự chạy đồng thời là **min của hai cái**, không phải tổng.

**Giải thích cơ chế ngầm:** Một tiến trình `gitlab-runner` có thể phục vụ nhiều mục `[[runners]]` — nhiều token, nhiều executor, nhiều tag khác nhau. `concurrent` nằm ở **cấp cao nhất** của tệp và chặn tổng số job của cả tiến trình. `limit` nằm **trong** từng mục và chặn riêng mục đó. Vì `concurrent` chặn tổng, nên đặt `limit` cao hơn `concurrent` không có tác dụng gì.

```toml
concurrent = 4              # ← TRẦN TOÀN CỤC: cả tiến trình tối đa 4 job
check_interval = 3

[[runners]]
  name = "docker-chung"
  limit = 10                # ← vô nghĩa: concurrent = 4 đã chặn ở 4
  executor = "docker"

[[runners]]
  name = "shell-rieng"
  limit = 1                 # ← có tác dụng: mục này tối đa 1 job
  executor = "shell"
```

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đặt `limit = 10` cho một mục nhưng chỉ thấy 4 job chạy, rồi kết luận runner hỏng. Cách kiểm trong 10 giây: đọc dòng `concurrent` ở **đầu** tệp — nó nằm ngoài mọi khối `[[runners]]` nên rất hay bị bỏ sót khi đọc lướt.

**Minh hoạ.**

```bash
# Đọc cả hai trần cùng lúc
docker exec lab-runner sh -c '
  echo "== TRẦN TOÀN CỤC =="
  grep -E "^concurrent" /etc/gitlab-runner/config.toml
  echo "== TRẦN TỪNG MỤC =="
  grep -E "^\s*(name|limit|executor)\s*=" /etc/gitlab-runner/config.toml
'
```

**Con số cần nhớ, và giới hạn của nó.** Mặc định `concurrent = 1` khi cài mới. Con số này làm rất nhiều lab tưởng runner hỏng, vì job thứ hai luôn phải chờ job thứ nhất xong. Con số **không phổ quát**: bản cài qua Helm hoặc qua image dựng sẵn thường đặt khác — nên bài lab **đọc giá trị thật** thay vì giả định.

### 6.2. Thêm runner không phải lúc nào cũng giúp

**Nguyên lý cốt lõi:** Thêm runner **không** giảm thời gian chờ nếu nút cổ chai là CPU, đĩa, hoặc mạng của máy chủ. Phải đo nút cổ chai **trước** khi thêm.

**Giải thích cơ chế ngầm:** Đây là mô hình tư duy 3 áp vào một con số cụ thể. Thời gian một job hoàn thành gồm hai phần: thời gian **chờ trong hàng đợi** và thời gian **được phục vụ**. Tăng `concurrent` giảm phần thứ nhất nhưng có thể **tăng** phần thứ hai, vì các job tranh cùng một lượng CPU và cùng một đĩa. Khi phần tăng vượt phần giảm, tổng thời gian đi lên.

Có một cách phát biểu gọn: `concurrent` chỉ nên tăng tới mức mà **thời lượng trung bình của một job chưa đổi đáng kể**. Vượt mức đó là đang chia nhỏ cùng một lượng tài nguyên cho nhiều job hơn.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tăng `concurrent` từ 4 lên 12 và tổng thời gian pipeline **tăng**. Bằng chứng xác nhận: `duration` trung bình của từng job tăng theo, và `docker stats` cho thấy CPU của máy chủ bão hoà.

**Minh hoạ.**

```bash
# Đo nút cổ chai TRONG LÚC pipeline chạy — chạy ở một terminal khác
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.BlockIO}}'

# Nếu tổng CPUPerc đã gần số lõi × 100% → nút cổ chai là CPU, thêm runner không giúp
nproc
```

**Đại lượng loại (c) — phải đo.** Mốc so sánh của bài lab: tổng thời gian đồng hồ của **cùng một tải 12 job** ở `concurrent` = 2, 4, 8. Ba điểm cho thấy **hình dạng** đường cong, và chỗ đường cong ngừng đi xuống chính là điểm dừng của việc tăng `concurrent` trên máy đó.

### 6.3. Hỏi việc khác chạy việc

**Nguyên lý cốt lõi:** `request_concurrency` điều khiển số **yêu cầu hỏi việc** gửi tới GitLab đồng thời, không điều khiển số **job chạy**. Nhầm hai cái là lý do phổ biến của câu "tôi đặt `concurrent` cao rồi mà vẫn chậm".

**Giải thích cơ chế ngầm:** Runner lấy job theo cơ chế hỏi: cứ mỗi `check_interval` giây, nó gửi yêu cầu tới GitLab hỏi có việc không. `request_concurrency` là số yêu cầu **hỏi** như vậy được gửi song song. Nếu nó bằng 1 và độ trễ mạng tới GitLab là 200 ms, thì tốc độ **nhận** job bị chặn ở khoảng 5 job mỗi giây — bất kể `concurrent` bằng bao nhiêu. Với lab một máy thì con số ấy không bao giờ thành nút cổ chai; với runner ở xa GitLab và nhiều mục runner thì có.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> `concurrent` đặt cao, máy chủ còn rỗi, nhưng job vẫn được nhận rời rạc từng cái một với khoảng cách đều đặn bằng `check_interval`. Bằng chứng: so `created_at` với `started_at` của một loạt job — nếu chênh lệch tăng dần đều theo thứ tự job thì đó là hàng đợi ở phía **hỏi việc**, không phải ở phía chạy việc.

**Minh hoạ.**

```toml
concurrent = 20
check_interval = 3          # giây giữa hai lần hỏi

[[runners]]
  name = "docker-chung"
  executor = "docker"
  request_concurrency = 4   # số yêu cầu HỎI VIỆC song song — không phải số job
```

```bash
# Phân biệt hai loại hàng đợi bằng số liệu
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?per_page=100" \
| jq -r '.[] | [.name, .created_at, .started_at, .queued_duration] | @tsv' | sort
# queued_duration tăng dần đều theo thứ tự  → nghẽn ở khâu hỏi việc
# queued_duration nhảy bậc theo nhóm        → nghẽn ở concurrent
```

**Con số cần nhớ, và giới hạn.** Mặc định `request_concurrency = 1`. Nó **chỉ** thành nút cổ chai khi số mục runner lớn hoặc độ trễ mạng tới GitLab cao — nên đừng tăng nó theo phản xạ; tăng khi đã có bằng chứng bằng số như trên.

---

### 1.4. Ba mức runner và ba điều kiện nhận job (5 phút)

### 7.1. Ba mức phạm vi

**Nguyên lý cốt lõi:** Runner có **ba mức phạm vi**: instance, group, project. Chúng khác nhau ở **project nào nhìn thấy runner**, và runner cấp instance thấy **mọi** project — nên nó vừa tiện nhất vừa là **bề mặt tấn công lớn nhất**.

**Giải thích cơ chế ngầm:** Phạm vi quyết định ai được giao việc cho runner. Runner instance nhận job từ mọi project trên GitLab đó, kể cả project mà đội vận hành runner chưa từng nghe tên. Vì job chạy **mã tuỳ ý** do người viết pipeline quyết định, một runner instance thực chất là một máy cho phép mọi người trong tổ chức chạy mã trên đó.

| Mức | Ai giao việc được | Dùng khi | Rủi ro |
|---|---|---|---|
| Instance | **Mọi project** | Job chung, không đụng secret nhạy cảm | Một runner bị chiếm là **mọi** project bị ảnh hưởng |
| Group | Project trong group | Đội hoặc phòng ban dùng chung | Giới hạn trong group |
| Project | Đúng một project | Job cần secret riêng, deploy prod | Thấp nhất, nhưng tốn công quản lý nhất |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Một runner instance có mount Docker socket và có sẵn thông tin xác thực cloud trong biến môi trường máy chủ. Bất kỳ ai tạo được một project trên GitLab đó đều lấy được cả hai. Buổi 28 xây mô hình đe doạ đầy đủ cho ca này; buổi 45 đưa cách tách bằng protected environment và runner riêng.

**Minh hoạ.**

```bash
# Liệt kê runner theo mức phạm vi
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/all" \
| jq -r '.[] | "\(.id)\t\(.runner_type)\t\(.description)"'
# runner_type: instance_type | group_type | project_type
```

**Con số cần nhớ: 1 runner instance bị chiếm là toàn bộ project của GitLab đó bị ảnh hưởng.** Đây là lý do quy tắc thực hành của khoá: runner instance dùng cho job build và test; job deploy dùng runner project hoặc group, gắn với protected environment.

### 7.2. Ba điều kiện độc lập, một triệu chứng

**Nguyên lý cốt lõi:** Runner `online` chỉ nghĩa là nó còn gửi nhịp tim. Để runner thật sự nhận được một job cụ thể cần **ba điều kiện độc lập**: `online` **và** không `paused` **và** khớp định tuyến. Thiếu bất kỳ điều nào cũng cho cùng một triệu chứng: job `pending`, không log.

**Giải thích cơ chế ngầm:** Ba điều kiện được quản lý ở ba chỗ khác nhau và hỏng vì ba lý do khác nhau. `online` phản ánh việc tiến trình runner có còn sống và còn kết nối được không — nó là trường `contacted_at` được cập nhật định kỳ. `paused` là một công tắc thủ công trên GitLab, hoàn toàn độc lập với việc tiến trình có sống hay không: **một runner đang chạy tốt vẫn có thể `paused`**. Định tuyến là phép so khớp tag cộng cờ `run_untagged`, quản lý một phần ở GitLab và một phần ở `config.toml`.

Vì cả ba cho cùng một triệu chứng, chẩn đoán bằng cách nhìn giao diện là không đủ — chấm xanh chỉ nói về điều kiện thứ nhất.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Kết luận "runner ổn, chấm xanh mà" rồi đi tìm nguyên nhân ở `.gitlab-ci.yml` trong nửa giờ. Cách kiểm cả ba trong một lệnh:

**Minh hoạ.**

```bash
# Kiểm BA điều kiện cho mọi runner, in ra cái nào thiếu điều kiện nào
for id in $(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/all" | jq -r '.[].id'); do
  curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/$id" | jq -r '
    "runner \(.id) [\(.description)]"
    + "\n  1. online       : \(.online)"
    + "\n  2. khong paused : \(.paused | not)"
    + "\n  3. dinh tuyen   : run_untagged=\(.run_untagged) tags=[\(.tag_list | join(","))]"
    + "\n  => nhan duoc job KHONG TAG: \(.online and (.paused | not) and .run_untagged)"'
done
```

**Con số cần nhớ: 3 điều kiện, 1 triệu chứng.** Đó là toàn bộ lý do phải kiểm bằng API thay vì nhìn chấm xanh, và là lý do §8 đề xuất biến phép kiểm này thành một job chạy theo lịch.

---

### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước

**Việc 1 — 10 phút, rủi ro bằng 0.** Lấy `config.toml` của runner đội mình và đọc đúng **ba** dòng: `concurrent`, `executor`, `volumes`. Ba dòng đó trả lời ba câu quan trọng nhất: bao nhiêu job chạy song song, mức cô lập là gì, và job có Docker socket không.

**Việc 2 — 20 phút, rủi ro bằng 0.** Chạy đoạn kiểm ba điều kiện của QT 7.2 cho mọi runner, lưu kết quả. Việc này thường phát hiện ra **runner ma**: runner `online` nhưng không nhận job nào trong nhiều ngày vì tag không còn ai dùng.

**Việc 3 — 30 phút, rủi ro bằng 0 và có giá trị thuyết phục cao nhất.** Lấy 5 sự cố CI gần nhất của đội và phân loại từng cái: thuộc `.gitlab-ci.yml` hay `config.toml`? Bảng ấy thường cho một kết quả bất ngờ — phần lớn thời gian gỡ lỗi đã đổ vào tệp thứ nhất trong khi nguyên nhân nằm ở tệp thứ hai.

### Cái gì hỏng nếu áp thẳng lên prod

Đổi `concurrent` trên một runner dùng chung ảnh hưởng **mọi project** ngay lập tức (QT 4.3), và không có cơ chế hoàn tác tự động. Ba nguyên tắc tối thiểu:

1. **Sao lưu tệp có mốc thời gian** trước khi sửa, và giữ bản sao ít nhất một tuần.
2. **Đổi ngoài giờ cao điểm**, và đo `queued_duration` trung vị trước và sau.
3. **Báo trước cho các đội dùng runner đó** — danh sách lấy được bằng API `runners/:id/jobs` như ở QT 4.3.

Thay đổi nguy hiểm nhất là **bỏ** dòng mount Docker socket: nó đúng về mặt bảo mật nhưng làm mọi job build image gãy ngay. Đường đi an toàn là dựng **runner mới** không có socket, chuyển từng project sang bằng tag, rồi mới tắt runner cũ — buổi 23 và buổi 44 xử lý đầy đủ.

### Đo trước — đo sau

| Chỉ số | Đo bằng | Vì sao chỉ số này |
|---|---|---|
| `concurrent` hiện tại và số job trung bình trong hàng đợi | Đọc `config.toml`; đếm job `pending` theo thời gian qua API | Hai con số này quyết định có nên tăng `concurrent` không |
| `queued_duration` **trung vị** của 100 job gần nhất | API `jobs`, lấy trường `queued_duration` | Trung vị chứ không phải trung bình — vài job pending 60 phút làm hỏng trung bình |
| Số runner `online` mà không nhận job nào trong 7 ngày | Đối chiếu `runners/all` với `runners/:id/jobs` | Đây là số runner ma; mỗi cái tốn tài nguyên và mở rộng bề mặt tấn công |

### Khi nào KHÔNG nên dùng

**Đừng chuyển hết sang `kubernetes` chỉ vì nó cô lập tốt nhất.** Với job ngắn dưới 30 giây, chi phí xếp lịch pod bậc 5–20 giây chiếm tỉ lệ lớn trong tổng thời gian. Một pipeline gồm nhiều job lint ngắn chạy trên `kubernetes` có thể chậm hơn hẳn cùng pipeline đó trên `docker`, và phần chậm thêm ấy **không mua được thêm chút cô lập nào có ý nghĩa** nếu các job lint không đụng gì nhạy cảm.

**Đừng tăng `concurrent` khi chưa đo nút cổ chai.** QT 6.2 nói rõ nó có thể làm chậm hơn. Phép đo tốn 15 phút; việc tăng nhầm rồi tìm nguyên nhân tốn cả buổi và làm chậm cả đội trong lúc đó.

**Đừng dùng runner `shell` cho job chạy mã từ merge request của người ngoài.** Ba kênh rò rỉ của QT 5.2 trở thành ba lối tấn công khi mã được chạy là mã người lạ gửi tới. Buổi 28 nói vì sao và nói cách chặn; hôm nay chỉ cần nhớ quy tắc.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy | Vì sao dính | Làm đúng là |
|---|---|---|---|
| 1 | Sửa YAML để chữa lỗi ở pha `prepare_executor` | `.gitlab-ci.yml` là tệp duy nhất người viết pipeline nhìn thấy | **3/8** pha thuộc `config.toml`. Kiểm dòng `Executing "step_script"` trước (QT 4.2) |
| 2 | Chọn executor theo tốc độ | Tốc độ là thứ đo được dễ nhất | Trục là **mức cô lập**; tốc độ chỉ khác ở chi phí khởi tạo (QT 5.1) |
| 3 | Tưởng `docker` là cô lập hoàn toàn | Tên gọi gợi ý như vậy | Socket mount phá hết. Kiểm dòng `volumes` (QT 5.3) |
| 4 | Đặt `limit = 10` mà quên `concurrent` | `concurrent` nằm ngoài mọi khối `[[runners]]`, dễ đọc lướt qua | Trần thật là **min** của hai (QT 6.1) |
| 5 | Tăng `concurrent` không đo nút cổ chai | Phản xạ "chậm thì thêm máy" | Đo bằng `docker stats` trước; có thể chậm hơn (QT 6.2) |
| 6 | Nhầm `request_concurrency` với `concurrent` | Tên giống nhau | Một cái là **hỏi việc**, một cái là **chạy việc** (QT 6.3) |
| 7 | Nhìn chấm xanh kết luận runner nhận được job | Chấm xanh chỉ nói về điều kiện thứ nhất | **3** điều kiện độc lập, kiểm cả ba bằng API (QT 7.2) |
| 8 | Quên `paused` là trạng thái độc lập với `online` | Runner đang chạy tốt vẫn có thể `paused` | Kiểm trường `paused` trong API |
| 9 | Dùng runner instance cho mọi thứ, kể cả deploy prod | Tiện nhất | Job deploy dùng runner project/group (QT 7.1); buổi 45 xử lý |
| 10 | Cài phụ thuộc bằng một job trên runner `shell` | Nó chạy được ngay | Rò rỉ kênh (c). Dùng `image` có sẵn phụ thuộc (QT 5.2) |
| 11 | Job `shell` để lại tiến trình nền | Không ai kiểm | Rò rỉ kênh (b). Dọn trong `after_script` — nhớ nó là shell khác (buổi 01 QT 4.3) |
| 12 | Sửa `config.toml` giờ cao điểm | Tưởng là thay đổi nhỏ | Ảnh hưởng **mọi** project ngay lập tức (QT 4.3) |
| 13 | Kết luận `kubernetes` chậm hơn `docker` | Chỉ đo job ngắn | Chỉ chậm hơn ở **chi phí khởi tạo**; với job dài, chênh lệch nằm dưới nhiễu đo |
| 14 | Job pending trên K8s mà chỉ hỏi API GitLab | Quen chẩn đoán từ buổi 01 | Phải hỏi **hai** nguồn: API GitLab **và** `kubectl get events` (QT 5.4) |

---

### 1.7. Tóm tắt

```mermaid
graph TD
    LD["LUẬN ĐỀ: hai tệp, hai người<br/>.gitlab-ci.yml nói LÀM GÌ · config.toml nói CHẠY Ở ĐÂU VÀ VỚI QUYỀN GÌ"]

    LD --> A["§4 RANH GIỚI HAI TỆP<br/>QT 4.1 hai tệp, hai người<br/>QT 4.2 3/8 pha thuộc hạ tầng<br/>QT 4.3 sửa config.toml là hành động vận hành"]
    LD --> B["§5 MỘT TRỤC: MỨC CÔ LẬP<br/>QT 5.1 cô lập, không phải tốc độ<br/>QT 5.2 shell rò rỉ BA kênh<br/>QT 5.3 socket = root máy chủ<br/>QT 5.4 k8s đổi bài toán, không xoá"]
    LD --> C["§6 HÀNG ĐỢI<br/>QT 6.1 trần thật = min(concurrent, limit)<br/>QT 6.2 thêm runner không phải lúc nào cũng giúp<br/>QT 6.3 hỏi việc khác chạy việc"]
    LD --> D["§7 ĐỊNH TUYẾN<br/>QT 7.1 ba mức phạm vi, instance = bề mặt lớn nhất<br/>QT 7.2 BA điều kiện độc lập, MỘT triệu chứng"]

    A --> KQ["BỐN CA HỎNG:<br/>rò rỉ shell (im lặng, KHÔNG chặn)<br/>paused · concurrent thấp (im lặng, có chặn)<br/>socket mount (im lặng, KHÔNG chặn)"]
    B --> KQ
    C --> KQ
    D --> KQ

    KQ --> VT["§8 ĐƯA VÀO VIỆC THẬT<br/>đọc 3 dòng config.toml · kiểm 3 điều kiện theo lịch<br/>phân loại 5 sự cố gần nhất theo tệp"]

    A -.dùng lại.-> B07["buổi 07 gỡ rối · 44 pipeline tập trung · 47 sự cố runner"]
    B -.dùng lại.-> B23["buổi 13 quy mô · 23 build image · 28 mô hình đe doạ"]
    C -.dùng lại.-> B14["buổi 13 · 14 đường găng · 46 chi phí"]
    D -.dùng lại.-> B45["buổi 28 · 45 compliance"]
```

**Năm điều phải nhớ sau buổi học:**

1. **Hai tệp, hai người.** `.gitlab-ci.yml` nói làm gì; `config.toml` nói chạy ở đâu và với quyền gì.
2. **3 trên 8 pha thuộc phía hạ tầng.** Không có dòng `Executing "step_script"` nghĩa là đừng sửa YAML nữa.
3. **Trục chọn executor là mức cô lập, không phải tốc độ.** Chi phí khởi tạo là cái giá phải trả cho cô lập.
4. **Một dòng `volumes` mount socket phá hết cô lập.** Job có socket là job có quyền root trên máy chủ.
5. **Ba điều kiện độc lập, một triệu chứng.** `online` + không `paused` + khớp định tuyến. Chấm xanh chỉ nói về điều kiện thứ nhất.

---

### 1.8. Câu hỏi tự kiểm tra

1. Kể tên hai tệp cấu hình một job và nói mỗi tệp quyết định điều gì.
2. Trong tám pha, ba pha nào thuộc phía hạ tầng? Lỗi ở đó thì ai sửa?
3. Trong log job không có dòng `Executing "step_script" stage of the job script`. Kết luận gì, và bước tiếp theo là gì?
4. Bốn executor xếp theo trục nào? Cái giá của việc đi lên trên trục ấy là gì?
5. Kể ba kênh rò rỉ trạng thái của executor `shell`, mỗi kênh một ví dụ cụ thể.
6. Rò rỉ ở executor `shell` thuộc ô nào của bảng hai thuộc tính? Vì sao đó là ô tệ nhất?
7. `config.toml` có dòng `volumes = ["/var/run/docker.sock:/var/run/docker.sock"]`. Chuyện gì có thể xảy ra?
8. `concurrent = 4` ở đầu tệp và `limit = 10` trong một mục runner. Bao nhiêu job chạy đồng thời được?
9. Job đang xếp hàng dài. Nêu **hai** phép đo phải làm **trước khi** tăng `concurrent`.
10. Phân biệt `concurrent`, `limit`, `request_concurrency` bằng một câu mỗi cái.
11. `queued_duration` của một loạt job tăng dần đều theo thứ tự job. Nghẽn ở đâu? Còn nếu nó nhảy bậc theo nhóm thì nghẽn ở đâu?
12. Kể ba điều kiện để một runner nhận được một job cụ thể. Thiếu điều nào thì triệu chứng khác nhau thế nào?
13. Trên executor `kubernetes`, job nằm `pending`. Nêu hai giả thuyết và hai nguồn dữ liệu phân biệt chúng.
14. Vì sao runner cấp instance vừa tiện nhất vừa rủi ro nhất? Nêu một quy tắc thực hành để giảm rủi ro.
15. Nêu một tình huống mà chuyển sang `kubernetes` là quyết định **sai**, kèm lập luận bằng số.

### Đáp án

1. `.gitlab-ci.yml` — job **làm gì**: lệnh, image mong muốn, artifact cần, khi nào chạy, đòi tag gì. `config.toml` — job **chạy ở đâu và với quyền gì**: executor, image mặc định, `concurrent`/`limit`, volume được mount, mạng, vị trí kho cache (QT 4.1).
2. `prepare_executor`, `prepare_script`, và phần lớn `get_sources`. Người vận hành runner sửa. Riêng `get_sources` là ranh giới — đôi khi sửa được bằng biến `GIT_*` trong YAML (QT 4.2).
3. Kết luận: lệnh của mình **chưa chạy lần nào**, lỗi thuộc phía hạ tầng. Bước tiếp theo: đọc dòng tiêu đề pha cuối cùng trong log, rồi mở `config.toml` và log runner — không sửa `script`.
4. Trục **mức cô lập**. Cái giá là **chi phí khởi tạo**: `shell` ≈ 0 giây, `docker` bậc 1–5 giây, `kubernetes` bậc 5–20 giây, `docker-autoscaler` bậc 30–120 giây (QT 5.1). Ba con số đầu là đại lượng phải đo.
5. (a) Hệ tệp ngoài thư mục dự án — `~/.aws/credentials`, `/tmp/token`. (b) Tiến trình nền còn sống — `npm start &` không được tắt. (c) Trạng thái công cụ toàn cục — `npm i -g`, `git config --global` (QT 5.2).
6. **Im lặng, không chặn.** Tệ nhất vì pipeline vẫn xanh — nó xanh **nhờ** trạng thái rò rỉ — nên không có tín hiệu nào cho tới ngày máy runner được dựng lại, và khi đó đỏ hàng loạt cùng lúc.
7. Job gọi được Docker daemon của máy chủ, mà daemon chạy dưới quyền root và không có phân quyền bên trong socket. Job tạo được container mount `/` của máy chủ, tức đọc ghi được toàn bộ hệ tệp máy chủ. Mức cô lập của executor `docker` bị vô hiệu hoá bởi **một dòng** (QT 5.3).
8. **4.** `concurrent` là trần toàn cục và nó nhỏ hơn; trần thật là min của hai (QT 6.1).
9. (a) Đo nút cổ chai bằng `docker stats` trong lúc pipeline chạy — nếu tổng CPU đã gần `nproc × 100%` thì thêm runner không giúp. (b) Đo `queued_duration` trung vị và `duration` trung bình của job; nếu `duration` đã tăng khi tải cao thì đang tranh tài nguyên (QT 6.2).
10. `concurrent` — trần số job của **cả tiến trình runner**. `limit` — trần số job của **một mục runner**. `request_concurrency` — số yêu cầu **hỏi việc** gửi song song tới GitLab, không liên quan số job chạy (QT 6.1, 6.3).
11. Tăng dần đều theo thứ tự → nghẽn ở khâu **hỏi việc** (`request_concurrency`, `check_interval`). Nhảy bậc theo nhóm → nghẽn ở **`concurrent`**: mỗi nhóm là một lứa job chạy cùng lúc, nhóm sau chờ nhóm trước xong.
12. `online` (còn gửi nhịp tim) **và** không `paused` **và** khớp định tuyến (tag hoặc `run_untagged`). Triệu chứng **không** khác nhau — cả ba đều cho job `pending`, không log. Đó chính là lý do phải kiểm cả ba bằng API (QT 7.2).
13. Giả thuyết A: không runner nào khớp hoặc runner không thoả ba điều kiện. Giả thuyết B: cụm không xếp lịch được pod (hết CPU/bộ nhớ, `nodeSelector` không khớp). Hai nguồn: API GitLab `runners/all`, và `kubectl get events -n <namespace>` — dòng `Insufficient cpu` chỉ có ở nguồn thứ hai (QT 5.4).
14. Vì nó nhận job từ **mọi** project, mà job chạy mã tuỳ ý do người viết pipeline quyết định. Quy tắc thực hành: runner instance dùng cho build và test; job deploy dùng runner project hoặc group gắn với protected environment (QT 7.1).
15. Pipeline gồm 10 job lint, mỗi job chạy 8 giây. Trên `docker` chi phí khởi tạo khoảng 2 giây/job → tổng khoảng 100 giây. Trên `kubernetes` chi phí khoảng 12 giây/job → tổng khoảng 200 giây. Chậm gấp đôi, mà các job lint không đụng secret nên phần cô lập thêm không mua được giá trị nào.

---

## §12. Tài liệu tham khảo

| Nguồn | Loại | Phiên bản |
|---|---|---|
| GitLab Runner Docs — *Executors* (`shell`, `docker`, `docker-autoscaler`, `kubernetes`) | (a) tài liệu chính thức | 17.7 |
| GitLab Runner Docs — *Advanced configuration* (`config.toml`: `concurrent`, `limit`, `request_concurrency`, `check_interval`) | (a) | 17.7 |
| GitLab Runner Docs — *The Docker executor* (`volumes`, `privileged`, `network_mode`, `extra_hosts`) | (a) | 17.7 |
| GitLab Docs — *Runner scope*: instance, group, project | (a) | 17.7 |
| GitLab API — `GET /runners/all`, `GET /runners/:id`, `GET /runners/:id/jobs` | (a) | v4 |
| Chi phí khởi tạo từng executor; hành vi nạp lại `config.toml`; hình dạng đường cong `concurrent` | (c) **phải đo** | Lab bước 1 và bước 3 |
| Quy trình ba bước trước khi sửa `config.toml`; quy tắc runner deploy tách khỏi runner build | (c) kinh nghiệm thực tế | — |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10' |
| §1 | Sau buổi này học viên làm được gì | 1' |
| §2 | Cần biết trước | 1' |
| §3 | Thuật ngữ và mô hình tư duy | 8' |
| §4 | Hai tệp cấu hình và ranh giới giữa chúng | 9' |
| §5 | Bốn executor và một trục duy nhất: mức cô lập | 11' |
| §6 | `config.toml`: hàng đợi, `concurrent`, `limit` | 9' |
| §7 | Ba mức runner và ba điều kiện nhận job | 5' |
| §8 | Đưa vào việc thật | 4' |
| §9 | Bẫy hay gặp | 2' |
| §10–§12 | Tóm tắt · tự kiểm tra · tham khảo (đọc ngoài giờ) | — |
| **Tổng** | | **60'** |

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên môi trường GitLab Community / Enterprise Edition cùng các GitLab Runner cô lập (Docker / Kubernetes Executor). Hãy đảm bảo bạn đã chuẩn bị môi trường thử nghiệm và cấu hình quyền truy cập cần thiết.

## Khối thực hành — 150 phút

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · Docker Engine 27.x.
> **Buổi này đụng vào `config.toml` — hạ tầng dùng chung.** §L1 bắt buộc sao lưu, §L8 bắt buộc khôi phục.

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| # | Mục tiêu | Tiêu chí hoàn thành (kiểm chứng được bằng lệnh) |
|---|---|---|
| TH1 | Tìm và đọc `config.toml` của runner lab | `config-doc-duoc.toml` chứa cả `concurrent` lẫn `executor` |
| TH2 | Đăng ký thêm một runner `shell` bên cạnh runner `docker` | API `runners/all` trả về **≥ 2** runner online, một cái có tag `shell-lab` |
| TH3 | **Đo QT 4.3** — runner có tự nạp lại `config.toml` không | `nap-lai-config.txt` ghi kết quả đo **kèm phiên bản runner** |
| TH4 | Kiểm chứng QT 5.2 kênh (a) — hệ tệp ngoài thư mục dự án | Job `doc-ba-kenh` trên `shell` in `CO`, trên `docker` in `KHONG` |
| TH5 | Kiểm chứng QT 5.2 kênh (b) và (c) — tiến trình nền và công cụ toàn cục | Cùng job, hai kết quả trái ngược trên hai executor |
| TH6 | **Đo QT 5.1** — chi phí khởi tạo `shell` so `docker`, và chi phí kéo image lần đầu | `chi-phi-khoi-tao.tsv` có ≥ 3 dòng đo |
| TH7 | **Đo QT 6.1** — `concurrent` thật bằng hàng đợi, không bằng đọc tệp | Số job chồng lấn đo được khớp `concurrent` đã đặt |
| TH8 | **Đo QT 6.2** — hình dạng đường cong tổng thời gian theo `concurrent` | `do-concurrent.tsv` có 3 điểm: `concurrent` = 2, 4, 8 |
| TH9 | Kiểm chứng QT 7.2 — ba điều kiện độc lập, một triệu chứng | Ba lần job `pending` vì ba nguyên nhân khác nhau, đều log rỗng |
| TH10 | Kiểm chứng QT 5.3 — Docker socket là quyền root máy chủ | Job đọc được tệp của **máy chủ** từ bên trong container |
| TH11 | Thiết kế đội hình runner cho tổ chức giả định | `doi-hinh-runner.md` có bảng 4 nhóm job kèm lập luận |
| TH12 | Nộp hiện vật và **khôi phục `config.toml`** | `kiem-hien-vat.sh` in ĐẠT; `config.toml` khớp bản sao lưu |

**Sản phẩm cuối buổi:** `gitlab-portfolio/02-runner-va-executor/` gồm `config-doc-duoc.toml`, `phan-loai-su-co.md` (6 sự cố phân loại theo tệp), `nap-lai-config.txt`, `ba-kenh-ro-ri.md`, `chi-phi-khoi-tao.tsv`, `do-concurrent.tsv`, `ba-dieu-kien.md`, `socket-la-root.md`, `doi-hinh-runner.md`, `checkpoint.log`.

---

## L1. Điều kiện tiên quyết về môi trường

| # | Kiểm tra | Lệnh | Kết quả kỳ vọng |
|---|---|---|---|
| 1 | Đã nạp biến môi trường lab | `echo "$GITLAB" "$GITLAB_TOKEN" \| wc -w` | `2` |
| 2 | GitLab sẵn sàng | `curl -sf -o /dev/null -w '%{http_code}\n' "$GITLAB/-/readiness"` | `200` |
| 3 | Container runner đang chạy | `docker ps --format '{{.Names}}' \| grep -cx lab-runner` | `1` |
| 4 | **Có quyền `docker exec` vào runner** | `docker exec lab-runner gitlab-runner --version \| head -1` | in ra phiên bản |
| 5 | Runner docker cũ vẫn online | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/all" \| jq '[.[]\|select(.online)]\|length'` | `>= 1` |
| 6 | Đã học buổi 01 | (tự kiểm) phát biểu được tám pha và bốn đường vào | Bắt buộc — §4 dựng thẳng lên đó |
| 7 | Bộ nhớ trống | `free -g \| awk '/Mem:/{print $7}'` | `>= 4` (bước 3 chạy 12 job) |
| 8 | Số lõi CPU — **ghi lại, dùng ở bước 3** | `nproc` | ghi vào hiện vật |
| 9 | Có `jq`, `curl`, `git` | `command -v jq curl git \| wc -l` | `3` |
| 10 | Chưa có project lab 02 | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects?search=lab02-runner" \| jq length` | `0` |

### Sao lưu bắt buộc — làm trước mọi thứ khác

Bài lab **sẽ sửa** `config.toml`. Đây là hạ tầng dùng chung theo QT 4.3, nên sao lưu là bắt buộc, không phải khuyến nghị.

```bash
source ~/.gitlab-lab.env
docker exec lab-runner sh -c \
  'cp /etc/gitlab-runner/config.toml /etc/gitlab-runner/config.toml.buoi02.bak'
docker exec lab-runner sh -c 'ls -la /etc/gitlab-runner/config.toml*'
```

**Cảnh báo về mức độ tác động.** Bài lab tạo project `lab02-runner`, đăng ký thêm **một** runner `shell`, và sửa `concurrent` trong `config.toml` **ba lần** ở bước 3. Trên lớp đông người dùng chung một GitLab và một runner, **chỉ giảng viên làm bước 3 trước lớp**; học viên quan sát và ghi số. Nếu mỗi học viên có runner riêng thì làm độc lập được. §L8 khôi phục `config.toml` về bản sao lưu — bỏ bước đó là để lại hạ tầng ở trạng thái khác lúc đầu.

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    HV["Học viên"]
    HV -->|"docker exec"| CFG["config.toml<br/>trong container lab-runner<br/>TỆP THỨ HAI của luận đề"]
    HV -->|"git push"| PRJ["Project lab02-runner"]
    HV -->|"curl + jq"| API["API GitLab v4<br/>runners/all · runners/:id · jobs"]

    CFG --> RN["Tiến trình gitlab-runner<br/>concurrent = trần TOÀN CỤC"]
    RN --> E1["Mục runner 1: executor docker<br/>tag: docker<br/>job chạy trong container ANH EM"]
    RN --> E2["Mục runner 2: executor shell<br/>tag: shell-lab<br/>job chạy TRONG container lab-runner<br/>→ rò rỉ THẬT, phạm vi giới hạn"]

    PRJ --> RN

    E1 --> B2A["Bước 2: docker → KHÔNG rò rỉ"]
    E2 --> B2B["Bước 2: shell → rò rỉ BA kênh"]

    API --> B1["Bước 1: đọc config.toml<br/>+ đo có tự nạp lại không"]
    API --> B3["Bước 3: đo chi phí khởi tạo<br/>+ concurrent = 2, 4, 8 với 12 job"]
    API --> B4["Bước 4: tắt LẦN LƯỢT ba điều kiện<br/>→ ba nguyên nhân, MỘT triệu chứng<br/>+ socket = root máy chủ"]
    API --> B5["Bước 5: thiết kế đội hình runner"]
```

**Bốn quyết định thiết kế:**

1. **Runner `shell` đăng ký bên trong chính container `lab-runner`**, không đăng ký trên máy chủ. Nó vẫn là executor `shell` thật và rò rỉ thật qua đủ ba kênh, nhưng phạm vi rò rỉ giới hạn trong container — nhờ đó bài lab an toàn mà vẫn đo được đủ hiện tượng. Phương án hiển nhiên là cài runner shell trên máy chủ; nó cho kết quả giống hệt nhưng làm bẩn máy học viên và không dọn sạch được.

2. **Đo `concurrent` bằng hàng đợi thật, không bằng đọc tệp.** Bài lab đẩy 12 job cùng lúc và đếm số job có khoảng `[started_at, finished_at]` **chồng lấn** nhau. Đọc tệp chỉ cho biết cấu hình; đo cho biết **hành vi** — và hai thứ lệch nhau khi `limit` hoặc `request_concurrency` chen vào. Đây cũng là kỹ thuật buổi 13 và buổi 14 dùng lại để đo song song thật.

3. **Ba giá trị `concurrent` (2, 4, 8) chạy cùng một tải 12 job.** Một điểm chỉ cho một con số; ba điểm cho thấy **hình dạng** đường cong. Hình dạng ấy là bằng chứng của QT 6.2 — chỗ đường cong ngừng đi xuống là điểm dừng của việc tăng `concurrent` trên máy đó. Nếu chỉ đo một giá trị, học viên nhớ một con số vô nghĩa vì nó chỉ đúng với máy lab.

4. **Ba điều kiện của QT 7.2 được tắt LẦN LƯỢT, mỗi lần đúng một điều kiện.** Cả ba lần cho **cùng một triệu chứng**: job `pending`, log rỗng. Đó là bài học của bước 4, và nó chỉ hiện ra khi làm tuần tự. Làm gộp thì học viên thấy một lỗi và nhớ một nguyên nhân.

**Ca đối chứng PHẢI THẤT BẠI — báo trước cho lớp.** Bước 4 có **ba lần** job nằm `pending` và không chạy. Cả ba là kết quả đúng. Ai gọi giảng viên ở bước 4 vì "job không chạy" là đã bỏ qua đoạn này.

---

## L3. Bước 1 — Tìm và đọc `config.toml`; đăng ký runner `shell` (30 phút)

### 3.1. Tạo project và bộ công cụ (6 phút)

```bash
source ~/.gitlab-lab.env
export HAU_TO="${USER}"
export TEN_PRJ="lab02-runner-${HAU_TO}"
mkdir -p ~/lab02 && cd ~/lab02

PID2=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{\"name\":\"$TEN_PRJ\",\"visibility\":\"internal\"}" \
  "$GITLAB/api/v4/projects" | jq -r .id)
echo "PID2=$PID2"
```

Bộ công cụ buổi 02 — mở rộng bộ của buổi 01, thêm hai hàm đo hàng đợi:

```bash
cat > ~/lab02/cong-cu.sh <<'SH'
#!/usr/bin/env bash
# Bộ công cụ lab buổi 02. Nạp bằng: source ~/lab02/cong-cu.sh
: "${GITLAB:?}"; : "${GITLAB_TOKEN:?}"; : "${PID2:?}"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")

day() {
  git add -A >/dev/null; git commit -q -m "${1:-cap nhat}" --allow-empty
  git push -q origin HEAD 2>/dev/null; sleep 4
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/pipelines?per_page=1" | jq -r '.[0].id'
}

cho_pipeline() {
  local pipe="$1" han="${2:-420}" t=0 st
  while [ "$t" -lt "$han" ]; do
    st=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/pipelines/$pipe" | jq -r .status)
    case "$st" in success|failed|canceled|skipped) echo "$st"; return 0 ;; esac
    sleep 5; t=$((t+5))
  done
  echo "$st"
}

job_bang() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/pipelines/$1/jobs?per_page=100" \
  | jq -r '.[] | [.name, .status, (.duration//0), (.queued_duration//0)] | @tsv'
}

job_id() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/pipelines/$1/jobs?per_page=100" \
  | jq -r --arg n "$2" '.[] | select(.name==$n) | .id' | head -1
}

job_log() { curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/jobs/$1/trace" \
            | sed 's/\x1b\[[0-9;K]*[a-zA-Z]//g'; }

# ĐO SONG SONG THẬT: số job nhiều nhất cùng chạy tại một thời điểm bất kỳ
# Nguyên lý: quét mọi mốc bắt đầu, đếm bao nhiêu khoảng [started, finished] phủ mốc đó.
song_song_toi_da() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/pipelines/$1/jobs?per_page=100" \
  | jq -r '[ .[] | select(.started_at != null and .finished_at != null)
             | {s: (.started_at|fromdateiso8601), f: (.finished_at|fromdateiso8601)} ] as $j
           | [ $j[].s ] | map( . as $t | [ $j[] | select(.s <= $t and .f > $t) ] | length ) | max // 0'
}

# Tổng thời gian đồng hồ của cả pipeline, tính bằng giây
tong_dong_ho() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/pipelines/$1/jobs?per_page=100" \
  | jq -r '[ .[] | select(.started_at != null and .finished_at != null) ] as $j
           | if ($j|length) == 0 then 0
             else (([$j[].finished_at|fromdateiso8601]|max) - ([$j[].started_at|fromdateiso8601]|min))
             end'
}
SH
source ~/lab02/cong-cu.sh

git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2" | jq -r .path_with_namespace).git"
git config user.email "hocvien@lab.local"; git config user.name "hoc vien"
```

### 3.2. Đọc tệp thứ hai (8 phút)

Kiểm chứng QT 4.1. Đây là lần đầu học viên nhìn thấy tệp thứ hai của luận đề.

```bash
# Toàn bộ tệp
docker exec lab-runner cat /etc/gitlab-runner/config.toml | tee ~/lab02/config-doc-duoc.toml

echo "=== BA DÒNG ĐÁNG ĐỌC TRƯỚC TIÊN ==="
docker exec lab-runner sh -c \
  'grep -nE "^concurrent|executor|volumes|privileged|network_mode|extra_hosts" /etc/gitlab-runner/config.toml'
```

Trả lời ba câu, ghi vào `config-doc-duoc.toml` dạng bình luận `#` ở đầu tệp:

1. `concurrent` bằng bao nhiêu? Nó nằm **trong** hay **ngoài** khối `[[runners]]`?
2. Có dòng `volumes` chứa `docker.sock` không? Nếu có, theo QT 5.3 điều đó nghĩa là gì?
3. Có dòng `extra_hosts` hoặc `network_mode` không? Đối chiếu với buổi 01 QT 6.2 — chúng giải quyết vấn đề nào?

**CHECKPOINT 1 — đọc được `config.toml` và trích được cả `concurrent` lẫn `executor`.**

```bash
c=$(grep -cE '^concurrent' ~/lab02/config-doc-duoc.toml || true)
e=$(grep -cE 'executor' ~/lab02/config-doc-duoc.toml || true)
{ [ "$c" -ge 1 ] && [ "$e" -ge 1 ]; } \
  && echo "CHECKPOINT 1 — ĐẠT (concurrent=$(grep -E '^concurrent' ~/lab02/config-doc-duoc.toml | head -1))" \
  || echo "CHECKPOINT 1 — LỖI (concurrent=$c dòng, executor=$e dòng)"
```

### 3.3. Đăng ký runner `shell` (8 phút)

Lấy token mới ở Admin → CI/CD → Runners → New instance runner. Đặt tag `shell-lab`, **bỏ tick** "Run untagged jobs" — runner này chỉ phục vụ job có tag đó.

```bash
read -r -p "Dán token glrt- của runner shell: " TOKEN_SHELL
docker exec lab-runner gitlab-runner register \
  --non-interactive \
  --url "$GITLAB" \
  --token "$TOKEN_SHELL" \
  --executor shell \
  --description "lab-shell"
```

```bash
# Xem tệp đã đổi: giờ có HAI mục [[runners]]
docker exec lab-runner sh -c 'grep -cE "^\[\[runners\]\]" /etc/gitlab-runner/config.toml'
docker exec lab-runner sh -c 'grep -E "^\s*(name|executor)\s*=" /etc/gitlab-runner/config.toml'
```

**CHECKPOINT 2 — có hai runner online, một `docker` nhận job không tag và một `shell` có tag `shell-lab`.**

```bash
res=$(for id in $(curl -sf "${H[@]}" "$GITLAB/api/v4/runners/all" | jq -r '.[].id'); do
        curl -sf "${H[@]}" "$GITLAB/api/v4/runners/$id" \
        | jq -r 'select(.online==true) | "\(.id)|\(.run_untagged)|\(.tag_list|join(","))"'
      done)
n_all=$(echo "$res" | grep -c . || true)
n_shell=$(echo "$res" | grep -c 'shell-lab' || true)
n_untag=$(echo "$res" | grep -c '|true|' || true)
{ [ "$n_all" -ge 2 ] && [ "$n_shell" -ge 1 ] && [ "$n_untag" -ge 1 ]; } \
  && echo "CHECKPOINT 2 — ĐẠT ($n_all runner online, $n_shell có tag shell-lab)" \
  || echo "CHECKPOINT 2 — LỖI (online=$n_all shell=$n_shell untagged=$n_untag)"
echo "$res"
```

### 3.4. Đo QT 4.3 — runner có tự nạp lại `config.toml` không (8 phút)

Đại lượng loại (c), **lần thứ HAI** khoá học áp quy tắc "phải đo". Đo bằng hành vi, không bằng tài liệu.

```bash
# Ghi lại giá trị hiện tại
CU=$(docker exec lab-runner sh -c 'grep -E "^concurrent" /etc/gitlab-runner/config.toml' | tr -dc '0-9')
echo "concurrent hiện tại = $CU"

# Đặt về 2 mà KHÔNG khởi động lại runner
docker exec lab-runner sh -c \
  "sed -i 's/^concurrent.*/concurrent = 2/' /etc/gitlab-runner/config.toml"
docker exec lab-runner sh -c 'grep -E "^concurrent" /etc/gitlab-runner/config.toml'
sleep 15   # cho runner thời gian nạp lại nếu nó có cơ chế đó
```

Đẩy 6 job cùng lúc và đo song song thật:

```yaml
# ~/lab02/.gitlab-ci.yml
stages: [do]
.mau:
  stage: do
  image: alpine:3.20
  script: [sleep 20]

j1: {extends: .mau}
j2: {extends: .mau}
j3: {extends: .mau}
j4: {extends: .mau}
j5: {extends: .mau}
j6: {extends: .mau}
```

```bash
cd ~/lab02
P=$(day "do nap lai config"); cho_pipeline "$P"
SS=$(song_song_toi_da "$P")

{
  echo "# QT 4.3 — runner có tự nạp lại config.toml không? ĐO, không tra tài liệu"
  echo "# $(docker exec lab-runner gitlab-runner --version | head -1)"
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
  echo "# Ngày đo: $(date -Iseconds)"
  echo "concurrent_trong_tep = 2"
  echo "song_song_do_duoc    = $SS"
  echo "khoi_dong_lai_runner = KHONG"
  echo "ket_luan             = $([ "$SS" -le 2 ] && echo 'CO TU NAP LAI' || echo 'PHAI KHOI DONG LAI')"
} | tee ~/lab02/nap-lai-config.txt
```

**CHECKPOINT 3 — đo xong và hiện vật ghi đủ phiên bản runner.**

```bash
k=$(grep -c 'ket_luan' ~/lab02/nap-lai-config.txt || true)
v=$(grep -c 'gitlab-runner' ~/lab02/nap-lai-config.txt || true)
{ [ "$k" -ge 1 ] && [ "$v" -ge 1 ]; } \
  && echo "CHECKPOINT 3 — ĐẠT ($(grep ket_luan ~/lab02/nap-lai-config.txt))" \
  || echo "CHECKPOINT 3 — LỖI (ket_luan=$k, phiên bản=$v)"
```

Nếu kết luận là `PHAI KHOI DONG LAI` thì chạy `docker restart lab-runner` và chờ 20 giây trước khi sang bước sau. Ghi rõ điều đó vào hiện vật — đó là một phát hiện, không phải một sự cố.

---

## L4. Bước 2 — Đo ba kênh rò rỉ của executor `shell` (30 phút)

Kiểm chứng QT 5.2. Cùng một pipeline chạy trên **hai** executor cho **hai** kết quả trái ngược — đó là toàn bộ nội dung của bước này.

### 4.1. Pipeline ghi và đọc ba kênh (12 phút)

```yaml
# ~/lab02/.gitlab-ci.yml — thay toàn bộ
stages: [ghi, doc]

# ============ CHẠY TRÊN RUNNER SHELL ============
ghi-shell:
  stage: ghi
  tags: [shell-lab]
  script:
    # kênh (a) — hệ tệp ngoài thư mục dự án
    - echo "bi-mat-cua-job-truoc" > /tmp/ro-ri-a.txt
    # kênh (b) — tiến trình nền còn sống sau khi job kết thúc
    - sh -c 'sleep 600 >/dev/null 2>&1 & echo $! > /tmp/ro-ri-b-pid.txt'
    # kênh (c) — trạng thái công cụ toàn cục
    - git config --global user.email "ro-ri-c@lab.local"
    - echo "da ghi ca ba kenh"

doc-shell:
  stage: doc
  tags: [shell-lab]
  script:
    - echo "KENH_A=$(cat /tmp/ro-ri-a.txt 2>/dev/null || echo KHONG)"
    - echo "KENH_B=$(ps -p "$(cat /tmp/ro-ri-b-pid.txt 2>/dev/null || echo 0)" >/dev/null 2>&1 && echo CON-SONG || echo DA-CHET)"
    - echo "KENH_C=$(git config --global user.email 2>/dev/null || echo KHONG)"

# ============ CHẠY TRÊN RUNNER DOCKER — ĐỐI CHỨNG ============
ghi-docker:
  stage: ghi
  image: alpine:3.20
  script:
    - echo "bi-mat-cua-job-truoc" > /tmp/ro-ri-a.txt
    - sh -c 'sleep 600 >/dev/null 2>&1 & echo $! > /tmp/ro-ri-b-pid.txt'
    - apk add --no-cache git >/dev/null 2>&1 || true
    - git config --global user.email "ro-ri-c@lab.local"
    - echo "da ghi ca ba kenh"

doc-docker:
  stage: doc
  image: alpine:3.20
  script:
    - echo "KENH_A=$(cat /tmp/ro-ri-a.txt 2>/dev/null || echo KHONG)"
    - echo "KENH_B=$(ps -p "$(cat /tmp/ro-ri-b-pid.txt 2>/dev/null || echo 0)" >/dev/null 2>&1 && echo CON-SONG || echo DA-CHET)"
    - echo "KENH_C=$(apk add --no-cache git >/dev/null 2>&1; git config --global user.email 2>/dev/null || echo KHONG)"
```

```bash
cd ~/lab02
P2=$(day "ba kenh ro ri"); cho_pipeline "$P2"
job_bang "$P2"
echo "=== SHELL ===";  job_log "$(job_id "$P2" doc-shell)"  | grep -E '^KENH_'
echo "=== DOCKER ==="; job_log "$(job_id "$P2" doc-docker)" | grep -E '^KENH_'
```

**CHECKPOINT 4 — runner `shell` rò rỉ cả ba kênh.**

```bash
LS=$(job_log "$(job_id "$P2" doc-shell)")
a=$(echo "$LS" | grep -c 'KENH_A=bi-mat-cua-job-truoc' || true)
b=$(echo "$LS" | grep -c 'KENH_B=CON-SONG' || true)
c=$(echo "$LS" | grep -c 'KENH_C=ro-ri-c@lab.local' || true)
{ [ "$a" -ge 1 ] && [ "$b" -ge 1 ] && [ "$c" -ge 1 ]; } \
  && echo "CHECKPOINT 4 — ĐẠT (shell rò rỉ 3/3 kênh)" \
  || echo "CHECKPOINT 4 — LỖI (a=$a b=$b c=$c)"
```

**CHECKPOINT 5 — runner `docker` KHÔNG rò rỉ kênh nào.**

```bash
LD=$(job_log "$(job_id "$P2" doc-docker)")
a2=$(echo "$LD" | grep -c 'KENH_A=KHONG' || true)
b2=$(echo "$LD" | grep -c 'KENH_B=DA-CHET' || true)
c2=$(echo "$LD" | grep -c 'KENH_C=KHONG' || true)
{ [ "$a2" -ge 1 ] && [ "$b2" -ge 1 ] && [ "$c2" -ge 1 ]; } \
  && echo "CHECKPOINT 5 — ĐẠT (docker rò rỉ 0/3 kênh)" \
  || echo "CHECKPOINT 5 — LỖI (a=$a2 b=$b2 c=$c2)"
```

### 4.2. Ghi hiện vật và trả lời (18 phút)

Ghi `ba-kenh-ro-ri.md` theo mẫu — bảng này là hiện vật chấm điểm cao nhất của bước 2:

| Kênh | Cơ chế | Kết quả trên `shell` | Kết quả trên `docker` | Hậu quả thật ở nơi làm việc |
|---|---|---|---|---|
| (a) Hệ tệp ngoài thư mục dự án | | | | |
| (b) Tiến trình nền còn sống | | | | |
| (c) Trạng thái công cụ toàn cục | | | | |

**Bốn câu hỏi phải trả lời trong hiện vật:**

1. Kênh nào nguy hiểm nhất về mặt **bảo mật**, và vì sao? (Gợi ý: nghĩ về `~/.aws/credentials`, `~/.npmrc`, `~/.docker/config.json`.)
2. Kênh (b) gây ra một ca hỏng đặc biệt khó chịu: job sau **kết nối nhầm** vào service của job trước và test **qua**. Đó là ô nào của bảng hai thuộc tính buổi 01 QT 7.1?
3. Rò rỉ ở executor `shell` thuộc ô nào của bảng hai thuộc tính? Vì sao nó tệ hơn một job đỏ?
4. Dọn xong ba kênh này bằng `after_script` được không? Nhớ buổi 01 QT 4.3 — `after_script` là shell khác. Cái gì dọn được, cái gì không?

Dọn phần rò rỉ do bài lab tạo ra:

```bash
docker exec lab-runner sh -c \
  'rm -f /tmp/ro-ri-a.txt; kill "$(cat /tmp/ro-ri-b-pid.txt 2>/dev/null)" 2>/dev/null; rm -f /tmp/ro-ri-b-pid.txt; git config --global --unset user.email 2>/dev/null; true'
echo "đã dọn ba kênh rò rỉ trong container runner"
```

---

## L5. Bước 3 — Đo chi phí khởi tạo và đo `concurrent` bằng hàng đợi (30 phút)

### 5.1. Đo chi phí khởi tạo (10 phút)

Kiểm chứng và định lượng QT 5.1. Ba phép đo: `shell`, `docker` với image đã có sẵn, `docker` với image lạ.

```yaml
# ~/lab02/.gitlab-ci.yml — thay toàn bộ
stages: [do-khoi-tao]

kt-shell:
  stage: do-khoi-tao
  tags: [shell-lab]
  script: [true]

kt-docker-image-co-san:
  stage: do-khoi-tao
  image: alpine:3.20          # đã kéo ở các bước trước
  script: [true]

kt-docker-image-la:
  stage: do-khoi-tao
  image: python:3.12-slim     # chưa từng kéo trên runner này
  script: [true]
```

```bash
cd ~/lab02
P3=$(day "do chi phi khoi tao"); cho_pipeline "$P3"

{
  echo "# QT 5.1 — chi phí khởi tạo theo executor. ĐO trên máy này."
  echo "# $(docker exec lab-runner gitlab-runner --version | head -1)"
  echo "# nproc = $(nproc)"
  printf "%-30s %-10s %-10s\n" "job" "duration_s" "queued_s"
  for j in kt-shell kt-docker-image-co-san kt-docker-image-la; do
    id=$(job_id "$P3" "$j")
    curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/jobs/$id" \
    | jq -r --arg n "$j" '[$n, (.duration|tostring), (.queued_duration|tostring)] | @tsv' \
    | awk '{printf "%-30s %-10s %-10s\n", $1, $2, $3}'
  done
  echo "# script của cả ba job đều là 'true', tức ~0 giây."
  echo "# Do đó duration ≈ CHI PHÍ KHỞI TẠO."
} | tee ~/lab02/chi-phi-khoi-tao.tsv
```

**CHECKPOINT 6 — đo được ba mức chi phí khởi tạo, và `shell` là thấp nhất.**

```bash
n=$(grep -cE '^kt-' ~/lab02/chi-phi-khoi-tao.tsv || true)
ds=$(awk '/^kt-shell/{print int($2)}' ~/lab02/chi-phi-khoi-tao.tsv)
dl=$(awk '/^kt-docker-image-la/{print int($2)}' ~/lab02/chi-phi-khoi-tao.tsv)
{ [ "$n" -eq 3 ] && [ "${ds:-99}" -le "${dl:-0}" ]; } \
  && echo "CHECKPOINT 6 — ĐẠT (3 phép đo; shell ${ds}s ≤ docker-image-lạ ${dl}s)" \
  || echo "CHECKPOINT 6 — LỖI (n=$n shell=${ds}s image-lạ=${dl}s)"
```

**Câu hỏi phải trả lời:** chênh lệch giữa `kt-docker-image-co-san` và `kt-docker-image-la` là bao nhiêu giây, và nó nói gì về con số "1–5 giây" ở QT 5.1? Con số ấy có phổ quát không?

### 5.2. Đo `concurrent` thật ở ba mức (20 phút)

Kiểm chứng QT 6.1 và QT 6.2. Cùng một tải 12 job, ba giá trị `concurrent`.

```yaml
# ~/lab02/.gitlab-ci.yml — thay toàn bộ
stages: [tai]
.mau:
  stage: tai
  image: alpine:3.20
  script:
    # Tải vừa có chờ vừa có tính, để nút cổ chai CPU lộ ra khi concurrent cao
    - sleep 5
    - awk 'BEGIN{s=0; for(i=0;i<3000000;i++) s+=sqrt(i); print s}' >/dev/null

t01: {extends: .mau}
t02: {extends: .mau}
t03: {extends: .mau}
t04: {extends: .mau}
t05: {extends: .mau}
t06: {extends: .mau}
t07: {extends: .mau}
t08: {extends: .mau}
t09: {extends: .mau}
t10: {extends: .mau}
t11: {extends: .mau}
t12: {extends: .mau}
```

```bash
cd ~/lab02
git add -A && git commit -q -m "tai 12 job" --allow-empty && git push -q origin HEAD

echo -e "concurrent\tsong_song_do_duoc\ttong_dong_ho_s\tduration_tb_s" > ~/lab02/do-concurrent.tsv

for C in 2 4 8; do
  docker exec lab-runner sh -c "sed -i 's/^concurrent.*/concurrent = $C/' /etc/gitlab-runner/config.toml"
  # Nếu bước 1 kết luận PHẢI KHỞI ĐỘNG LẠI thì bỏ comment dòng dưới
  # docker restart lab-runner >/dev/null && sleep 20
  sleep 15

  P=$(day "tai 12 job voi concurrent=$C")
  cho_pipeline "$P" 600 >/dev/null
  SS=$(song_song_toi_da "$P")
  TT=$(tong_dong_ho "$P")
  TB=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/pipelines/$P/jobs?per_page=100" \
       | jq -r '[.[].duration] | add / length | floor')
  echo -e "$C\t$SS\t$TT\t$TB" | tee -a ~/lab02/do-concurrent.tsv
done

echo "# nproc = $(nproc)" >> ~/lab02/do-concurrent.tsv
cat ~/lab02/do-concurrent.tsv
```

Trong lúc lần chạy `concurrent = 8` đang diễn ra, mở terminal khác và đo nút cổ chai:

```bash
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}' | tee -a ~/lab02/do-concurrent.tsv
```

**CHECKPOINT 7 — song song đo được khớp `concurrent` đã đặt ở cả ba mức.**

```bash
loi=0
while IFS=$'\t' read -r c ss _ _; do
  case "$c" in [0-9]*) [ "${ss:-0}" -le "$c" ] || loi=$((loi+1)) ;; esac
done < <(tail -n +2 ~/lab02/do-concurrent.tsv | grep -E '^[0-9]')
[ "$loi" -eq 0 ] \
  && echo "CHECKPOINT 7 — ĐẠT (song song đo được ≤ concurrent ở cả 3 mức)" \
  || echo "CHECKPOINT 7 — LỖI ($loi mức có song song vượt concurrent)"
```

**CHECKPOINT 8 — có đủ ba điểm đo và ghi số lõi CPU.**

```bash
n=$(grep -cE '^[0-9]+\s' ~/lab02/do-concurrent.tsv || true)
p=$(grep -c 'nproc' ~/lab02/do-concurrent.tsv || true)
{ [ "$n" -eq 3 ] && [ "$p" -ge 1 ]; } \
  && echo "CHECKPOINT 8 — ĐẠT (3 điểm đo, có ghi nproc)" \
  || echo "CHECKPOINT 8 — LỖI (điểm đo=$n, nproc=$p)"
```

**Ba câu hỏi phải trả lời, ghi vào `do-concurrent.tsv`:**

1. Tổng thời gian đồng hồ giảm bao nhiêu khi đi từ `concurrent = 2` sang `4`? Từ `4` sang `8`?
2. `duration` trung bình của **một** job có tăng khi `concurrent` tăng không? Nếu có, đó là bằng chứng của điều gì trong QT 6.2?
3. Trên máy có `nproc` lõi này, giá trị `concurrent` nào là điểm dừng hợp lý? Nêu lập luận bằng **hai** con số ở trên.

---

## L6. Bước 4 — Ba điều kiện nhận job; và Docker socket là quyền root (30 phút)

### 6.1. Ba điều kiện, một triệu chứng (18 phút)

Kiểm chứng QT 7.2. Tắt **lần lượt** từng điều kiện. **Cả ba lần job sẽ nằm `pending` — đó là kết quả đúng.**

Trước hết, đặt `concurrent` về giá trị làm việc và dựng pipeline dùng chung cho ba lần:

```bash
docker exec lab-runner sh -c "sed -i 's/^concurrent.*/concurrent = 4/' /etc/gitlab-runner/config.toml"
sleep 15
```

```yaml
# ~/lab02/.gitlab-ci.yml — thay toàn bộ
stages: [chay]
job-shell:
  stage: chay
  tags: [shell-lab]
  script: [echo "job nay can runner shell-lab"]
```

**Lần 1 — thiếu điều kiện 3 (định tuyến).** Đổi tag của job sang một tag không ai có:

```bash
cd ~/lab02
sed -i 's/tags: \[shell-lab\]/tags: [tag-khong-ton-tai]/' .gitlab-ci.yml
PA=$(day "lan 1: thieu dinh tuyen"); cho_pipeline "$PA" 120
JA=$(job_id "$PA" job-shell)
echo "lần 1: status=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/jobs/$JA" | jq -r .status), log $(job_log "$JA" | wc -c) byte"
```

**Lần 2 — thiếu điều kiện 2 (`paused`).** Trả tag về đúng, nhưng tạm dừng runner `shell`:

```bash
sed -i 's/tags: \[tag-khong-ton-tai\]/tags: [shell-lab]/' .gitlab-ci.yml
RID_SHELL=$(for id in $(curl -sf "${H[@]}" "$GITLAB/api/v4/runners/all" | jq -r '.[].id'); do
              curl -sf "${H[@]}" "$GITLAB/api/v4/runners/$id" | jq -r 'select(.tag_list|index("shell-lab")) | .id'
            done | head -1)
curl -sf --request PUT "${H[@]}" "$GITLAB/api/v4/runners/$RID_SHELL" --data "paused=true" | jq '{id, paused, online}'

PB=$(day "lan 2: runner paused"); cho_pipeline "$PB" 120
JB=$(job_id "$PB" job-shell)
echo "lần 2: status=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/jobs/$JB" | jq -r .status), log $(job_log "$JB" | wc -c) byte"
```

**Lần 3 — thiếu điều kiện 1 (`online`).** Bỏ tạm dừng, nhưng dừng tiến trình runner:

```bash
curl -sf --request PUT "${H[@]}" "$GITLAB/api/v4/runners/$RID_SHELL" --data "paused=false" >/dev/null
docker stop lab-runner >/dev/null
sleep 20

PC=$(day "lan 3: runner offline"); cho_pipeline "$PC" 120
JC=$(job_id "$PC" job-shell)
echo "lần 3: status=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/jobs/$JC" | jq -r .status), log $(job_log "$JC" | wc -c) byte"

docker start lab-runner >/dev/null && sleep 20
```

**CHECKPOINT 9 — ba nguyên nhân khác nhau cho cùng một triệu chứng: `pending`, log rỗng.**

```bash
ok=0
for pair in "$JA:dinh-tuyen" "$JB:paused" "$JC:offline"; do
  j="${pair%%:*}"; ten="${pair##*:}"
  st=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/jobs/$j" | jq -r .status)
  len=$(job_log "$j" | wc -c)
  echo "  $ten: status=$st, log=${len}B"
  { [ "$st" = "pending" ] && [ "$len" -lt 50 ]; } && ok=$((ok+1))
done
[ "$ok" -eq 3 ] \
  && echo "CHECKPOINT 9 — ĐẠT (3 nguyên nhân, 1 triệu chứng: pending + log rỗng)" \
  || echo "CHECKPOINT 9 — LỖI (chỉ $ok/3 lần cho đúng triệu chứng)"
```

Huỷ ba job đang chờ:

```bash
for j in "$JA" "$JB" "$JC"; do
  curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects/$PID2/jobs/$j/cancel" >/dev/null
done
echo "đã huỷ 3 job pending"
```

Ghi `ba-dieu-kien.md` — bảng này là hiện vật của bước 4:

| Lần | Điều kiện bị thiếu | Cách tái hiện | Trạng thái job | Log | Lệnh **duy nhất** phát hiện được |
|---|---|---|---|---|---|
| 1 | Định tuyến | | | | |
| 2 | `paused` | | | | |
| 3 | `online` | | | | |

Cột cuối là cột quan trọng nhất: với mỗi lần, viết **lệnh API cụ thể** phân biệt được nguyên nhân đó với hai nguyên nhân kia.

### 6.2. Docker socket là quyền root máy chủ (12 phút)

Kiểm chứng QT 5.3. Chạy trong lab để thấy tận mắt; **đừng chạy đoạn này ở nơi làm việc**.

```bash
# Kiểm xem runner lab có mount socket không
docker exec lab-runner sh -c 'grep -n "docker.sock" /etc/gitlab-runner/config.toml || echo "KHONG CO SOCKET"'
```

```yaml
# ~/lab02/.gitlab-ci.yml — thay toàn bộ
stages: [chung-minh]

socket-la-root:
  stage: chung-minh
  image: docker:27-cli
  script:
    - echo "== job co noi chuyen duoc voi daemon may chu khong =="
    - docker version --format 'server={{.Server.Version}}' || { echo "KHONG CO SOCKET — bo qua buoc nay"; exit 0; }
    - echo "== doc he tep MAY CHU tu ben trong job =="
    - docker run --rm -v /:/host alpine:3.20 sh -c 'echo "hostname may chu: $(cat /host/etc/hostname)"; ls /host/etc/gitlab-runner 2>/dev/null | head -3'
    - echo "KET LUAN: cach ly cua executor docker da bi vo hieu hoa boi MOT dong volumes"
```

```bash
cd ~/lab02
P4=$(day "socket la root"); cho_pipeline "$P4"
JS=$(job_id "$P4" socket-la-root)
job_log "$JS" | grep -E 'server=|hostname may chu|KET LUAN|KHONG CO SOCKET'
```

**CHECKPOINT 10 — job đọc được tệp của máy chủ, hoặc chứng minh được runner không mount socket.**

```bash
L=$(job_log "$JS")
co_socket=$(echo "$L" | grep -c 'hostname may chu' || true)
khong_socket=$(echo "$L" | grep -c 'KHONG CO SOCKET' || true)
{ [ "$co_socket" -ge 1 ] || [ "$khong_socket" -ge 1 ]; } \
  && echo "CHECKPOINT 10 — ĐẠT ($([ "$co_socket" -ge 1 ] && echo 'socket CÓ mount → job đọc được máy chủ' || echo 'runner KHÔNG mount socket → cô lập còn nguyên'))" \
  || echo "CHECKPOINT 10 — LỖI (không kết luận được)"
```

Ghi `socket-la-root.md` và trả lời **ba** câu:

1. Runner lab có mount socket không? Dòng cấu hình nào chứng minh?
2. Nếu có, một người tạo được project trên GitLab này lấy được những gì? Liệt kê ba thứ cụ thể trên máy chủ lab.
3. Ô nào của bảng hai thuộc tính? (Gợi ý: không có ai bị chặn, không có gì báo — cho tới khi sự cố xảy ra.)

---

## L7. Bước 5 — Thiết kế đội hình runner cho một tổ chức giả định (20 phút)

Đây là bước tổng hợp: dùng QT 5.1, 5.3, 6.2, 7.1 cùng lúc.

**Đề bài.** Một công ty có GitLab self-managed, 40 lập trình viên, 12 project. Bốn nhóm job:

| Nhóm | Đặc điểm | Số lần chạy/ngày | Thời lượng điển hình |
|---|---|---|---|
| A. Lint và unit test | Không đụng secret, chạy trên MR của cả người ngoài | 300 | 40 giây |
| B. Build image | Cần build Docker image, đẩy lên registry nội bộ | 60 | 4 phút |
| C. Integration test | Cần chạy database và message queue bên cạnh | 40 | 8 phút |
| D. Deploy production | Cần thông tin xác thực cloud, chạy trên tag protected | 5 | 3 phút |

Điền bảng vào `doi-hinh-runner.md` — **mỗi ô phải có lập luận, không được để trống**:

| Nhóm | Executor | Mức phạm vi | Có socket? | `concurrent` đề xuất | Lập luận (dẫn QT nào) |
|---|---|---|---|---|---|
| A | | | | | |
| B | | | | | |
| C | | | | | |
| D | | | | | |

**Bốn câu phải trả lời trong hiện vật:**

1. Nhóm nào **tuyệt đối không** được dùng executor `shell`, và vì sao? (Dẫn QT 5.2 và nói rõ kênh nào là lối tấn công.)
2. Nhóm B cần build image. Nêu **hai** phương án: một dùng socket, một không. Nêu đánh đổi của từng cái. (Buổi 23 sẽ giải đầy đủ; hôm nay chỉ cần nêu đúng trục đánh đổi.)
3. Nhóm D chạy 5 lần một ngày nhưng có secret cloud. Vì sao nó **không** nên dùng chung runner với nhóm A? Dẫn QT 7.1 và tính: nhóm A chạy 300 lần/ngày trên MR của người ngoài — điều đó nghĩa là gì với runner đó?
4. Tổng `concurrent` đề xuất cho cả bốn nhóm là bao nhiêu? Cần biết thêm **thông tin gì về máy chủ** trước khi chốt con số đó? (Dẫn QT 6.2.)

**CHECKPOINT 11 — hiện vật thiết kế đầy đủ 4 nhóm, mỗi nhóm có dẫn chiếu ít nhất một QT.**

```bash
n=$(grep -cE '^\| *[ABCD] *\|' ~/lab02/doi-hinh-runner.md 2>/dev/null || true)
q=$(grep -coE 'QT [0-9]+\.[0-9]+' ~/lab02/doi-hinh-runner.md 2>/dev/null || true)
c=$(grep -cE '^[0-9]\.' ~/lab02/doi-hinh-runner.md 2>/dev/null || true)
{ [ "$n" -ge 4 ] && [ "$q" -ge 4 ] && [ "$c" -ge 4 ]; } \
  && echo "CHECKPOINT 11 — ĐẠT ($n nhóm, $q dẫn chiếu QT, $c câu trả lời)" \
  || echo "CHECKPOINT 11 — LỖI (nhóm=$n, dẫn chiếu QT=$q, câu trả lời=$c)"
```

---

## L8. Nộp sản phẩm và dọn dẹp (10 phút)

### 8.1. Khôi phục `config.toml` — làm trước tiên

Đây là bước **bắt buộc** vì buổi này đụng hạ tầng dùng chung (QT 4.3).

```bash
docker exec lab-runner sh -c \
  'cp /etc/gitlab-runner/config.toml.buoi02.bak /etc/gitlab-runner/config.toml'
docker restart lab-runner >/dev/null && sleep 20
docker exec lab-runner sh -c 'grep -E "^concurrent" /etc/gitlab-runner/config.toml'
```

> Runner `shell` đăng ký ở bước 1 bị **xoá theo** khi khôi phục tệp, vì bản sao lưu chưa có nó. Nếu muốn giữ để dùng ở buổi 13, khôi phục xong thì đăng ký lại — và ghi vào hiện vật rằng mình đã chọn giữ.

### 8.2. Gom hiện vật

```bash
DICH="$PORTFOLIO/02-runner-va-executor"
mkdir -p "$DICH"
cp ~/lab02/config-doc-duoc.toml   "$DICH/"
cp ~/lab02/nap-lai-config.txt     "$DICH/"
cp ~/lab02/chi-phi-khoi-tao.tsv   "$DICH/"
cp ~/lab02/do-concurrent.tsv      "$DICH/"
# ba-kenh-ro-ri.md · ba-dieu-kien.md · socket-la-root.md · doi-hinh-runner.md
# · phan-loai-su-co.md  do học viên tự viết
ls -la "$DICH"
```

`phan-loai-su-co.md` là việc 3 của mục "Đưa vào việc thật" và cũng là hiện vật nộp: lấy **6** sự cố CI gần nhất (của đội mình, hoặc 6 ca dựng sẵn của giảng viên) và phân loại từng cái.

| # | Triệu chứng | Pha nào | Thuộc tệp nào | Ai sửa |
|---|---|---|---|---|
| 1 | | | | |

### 8.3. Script kiểm hiện vật

```bash
cat > "$DICH/kiem-hien-vat.sh" <<'SH'
#!/usr/bin/env bash
cd "$(dirname "$0")"
P=0; F=0
kiem() { if eval "$2" >/dev/null 2>&1; then echo "ĐẠT   $1"; P=$((P+1)); else echo "LỖI   $1"; F=$((F+1)); fi; }

kiem "config-doc-duoc.toml có concurrent"        "grep -qE '^concurrent' config-doc-duoc.toml"
kiem "nap-lai-config.txt có kết luận"            "grep -q 'ket_luan' nap-lai-config.txt"
kiem "nap-lai-config.txt ghi phiên bản runner"   "grep -q 'gitlab-runner' nap-lai-config.txt"
kiem "chi-phi-khoi-tao.tsv có 3 phép đo"         "[ \$(grep -cE '^kt-' chi-phi-khoi-tao.tsv) -eq 3 ]"
kiem "do-concurrent.tsv có 3 điểm"               "[ \$(grep -cE '^[0-9]+\s' do-concurrent.tsv) -eq 3 ]"
kiem "do-concurrent.tsv ghi nproc"               "grep -q 'nproc' do-concurrent.tsv"
kiem "ba-kenh-ro-ri.md có bảng 3 kênh"           "[ \$(grep -cE '^\| *\(?[abc]\)?' ba-kenh-ro-ri.md) -ge 3 ]"
kiem "ba-dieu-kien.md có 3 lần"                  "[ \$(grep -cE '^\| *[123] *\|' ba-dieu-kien.md) -ge 3 ]"
kiem "socket-la-root.md khác rỗng"               "[ -s socket-la-root.md ]"
kiem "doi-hinh-runner.md có 4 nhóm"              "[ \$(grep -cE '^\| *[ABCD] *\|' doi-hinh-runner.md) -ge 4 ]"
kiem "doi-hinh-runner.md dẫn chiếu QT"           "[ \$(grep -coE 'QT [0-9]+\.[0-9]+' doi-hinh-runner.md) -ge 4 ]"
kiem "phan-loai-su-co.md có 6 sự cố"             "[ \$(grep -cE '^\| *[1-6] *\|' phan-loai-su-co.md) -ge 6 ]"
kiem "checkpoint.log có 11 dòng CHECKPOINT"      "[ \$(grep -c 'CHECKPOINT' checkpoint.log) -ge 11 ]"
kiem "checkpoint.log không có LỖI"               "! grep -q 'LỖI' checkpoint.log"

echo "=== $P đạt, $F lỗi ==="
[ "$F" -eq 0 ]
SH
chmod +x "$DICH/kiem-hien-vat.sh"
```

**CHECKPOINT 12 — hiện vật đầy đủ và `config.toml` đã khôi phục.**

```bash
hv=$(bash "$DICH/kiem-hien-vat.sh" >/dev/null 2>&1 && echo 1 || echo 0)
same=$(docker exec lab-runner sh -c \
  'cmp -s /etc/gitlab-runner/config.toml /etc/gitlab-runner/config.toml.buoi02.bak && echo 1 || echo 0')
{ [ "$hv" -eq 1 ] && [ "$same" = "1" ]; } \
  && echo "CHECKPOINT 12 — ĐẠT (hiện vật đủ, config.toml đã khôi phục)" \
  || echo "CHECKPOINT 12 — LỖI (hiện vật=$hv, config khớp bản sao lưu=$same)"
```

```bash
cd "$PORTFOLIO"
git add 02-runner-va-executor
git commit -q -m "buoi 02: runner va executor — hai tep, ba kenh ro ri, do concurrent"
git push -q 2>/dev/null || echo "chưa cấu hình remote cho portfolio"
```

### 8.4. Dọn dẹp

```bash
source ~/lab02/cong-cu.sh
for j in $(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID2/jobs?scope[]=pending&scope[]=running&per_page=100" | jq -r '.[].id'); do
  curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects/$PID2/jobs/$j/cancel" >/dev/null
done
curl -sf --request DELETE "${H[@]}" "$GITLAB/api/v4/projects/$PID2/artifacts" >/dev/null
# Giữ project để buổi 03 dùng lại. Xoá khi hết giai đoạn 1:
# curl -sf --request DELETE "${H[@]}" "$GITLAB/api/v4/projects/$PID2"
```

---

## L9. Xử lý sự cố thường gặp trong lab

| Triệu chứng | Nguyên nhân | Cách khắc phục |
|---|---|---|
| `docker exec lab-runner` báo `permission denied` | Người dùng chưa vào nhóm `docker` | `sudo usermod -aG docker "$USER"`, đăng xuất rồi vào lại |
| `gitlab-runner register` báo token không hợp lệ | Dùng registration token cũ thay vì authentication token `glrt-` | Từ GitLab 16.0 chỉ dùng `glrt-`; lấy ở Admin → CI/CD → Runners → New instance runner |
| Job có tag `shell-lab` nằm `pending` ở bước 2 | Runner shell chưa online, hoặc tag gõ sai | Kiểm bằng CHECKPOINT 2; so từng ký tự tag |
| `song_song_toi_da` trả về `0` | Job chưa có `finished_at` — pipeline chưa xong | Chờ `cho_pipeline` trả về `success` rồi mới đo |
| `song_song_toi_da` trả về `1` ở mọi mức `concurrent` | Runner chưa nạp lại `config.toml` | Xem kết luận CHECKPOINT 3; nếu `PHAI KHOI DONG LAI` thì `docker restart lab-runner` giữa các mức |
| Tổng thời gian ở `concurrent = 8` **lớn hơn** ở `4` | Đây **là** kết quả của QT 6.2 — nút cổ chai CPU | Không phải lỗi. Ghi vào hiện vật kèm số liệu `docker stats` |
| `kt-docker-image-la` mất hơn 120 giây | Mạng chậm hoặc Docker Hub giới hạn tốc độ | Đổi sang một image nhỏ khác chưa kéo; **ghi lại image đã dùng** |
| CHECKPOINT 4 báo `docker` cũng rò rỉ kênh (a) | Runner docker có mount `/tmp` của máy chủ | Kiểm dòng `volumes`; đây là một phát hiện đáng ghi, không phải lỗi bài lab |
| Job trên `shell` báo `git: not found` | Container `lab-runner` không có git | `docker exec lab-runner apk add --no-cache git`; và ghi lại — đây là ví dụ trực tiếp của rò rỉ kênh (c) |
| Bước 4 lần 3: sau `docker start`, runner không online lại | Runner cần thời gian kết nối | Chờ 30 giây, kiểm bằng API `runners/:id` trường `online` |
| Sau bước 4, mọi job đều `pending` | Quên bỏ `paused`, hoặc quên `docker start lab-runner` | `curl -X PUT ... --data "paused=false"`; `docker start lab-runner` |
| `socket-la-root` job báo `KHONG CO SOCKET` | Runner lab không mount socket | Đây là **kết quả hợp lệ**. Ghi vào hiện vật rằng cô lập còn nguyên, và trả lời câu 2 theo hướng giả định |
| Sau khi khôi phục `config.toml`, runner shell biến mất | Bản sao lưu tạo **trước** khi đăng ký nó | Đúng như dự kiến; đăng ký lại nếu muốn giữ cho buổi 13 |
| Lớp đông, số đo bước 3 nhiễu nặng | Nhiều học viên chạy tải cùng lúc trên một máy | **Chỉ giảng viên chạy bước 3 trước lớp**; học viên ghi số chung. Đây là quyết định vận hành, ghi vào hiện vật |
| Muốn làm lại từ đầu | — | Khôi phục `config.toml`, xoá project, chạy lại §L3.1 |

---

## L10. Bài tập mở rộng

### BT1. Đo `check_interval`

Đặt `check_interval = 30` rồi đẩy một job và đo `queued_duration`.

**Câu hỏi phải trả lời:** `queued_duration` thay đổi thế nào? Con số đó thuộc pha nào trong tám pha của buổi 01 — hay không thuộc pha nào?

### BT2. `limit` so `concurrent`

Đặt `concurrent = 8` nhưng `limit = 2` cho mục runner docker, rồi đẩy 6 job.

**Câu hỏi phải trả lời:** đo được bao nhiêu job song song? Kết quả có khớp QT 6.1 không?

### BT3. Runner ma

Viết script tìm mọi runner `online` nhưng không chạy job nào trong 7 ngày.

**Câu hỏi phải trả lời:** trên GitLab lab có bao nhiêu runner ma? Mỗi runner ma gây ra rủi ro gì theo QT 7.1?

### BT4. Đo chi phí khởi tạo theo kích thước image

Chạy cùng một job `true` với `alpine:3.20` (~8 MB), `python:3.12-slim` (~130 MB), `node:22` (~1,1 GB), lần đầu và lần thứ hai.

**Câu hỏi phải trả lời:** vẽ quan hệ giữa kích thước image và chi phí khởi tạo lần đầu. Điều đó nói gì về buổi 25 (image mỏng)?

### BT5. `network_mode` và `extra_hosts`

Đăng ký một runner docker **không có** hai tuỳ chọn ấy, rồi chạy job `curl http://gitlab.lab:8929/-/readiness`.

**Câu hỏi phải trả lời:** thông báo lỗi là gì? Đối chiếu với buổi 01 QT 6.2 — nó ứng với nguyên nhân nào trong hai nguyên nhân đã học?

### BT6. Phân loại 10 sự cố

Lấy 10 sự cố CI thật của đội mình (hoặc 10 ca giảng viên cung cấp) và phân loại theo pha và theo tệp.

**Câu hỏi phải trả lời:** tỉ lệ sự cố thuộc `config.toml` là bao nhiêu? So với con số 3/8 pha của QT 4.2 — cao hơn hay thấp hơn, và vì sao?

### BT7. Job giám sát ba điều kiện

Viết một job chạy theo lịch kiểm ba điều kiện của QT 7.2 cho mọi runner và **đỏ** khi có runner thiếu điều kiện.

**Câu hỏi phải trả lời:** job này biến hỏng im lặng thành ô nào của bảng hai thuộc tính? (Dẫn buổi 01 QT 7.3.)

### BT8. Executor `kubernetes`

Nếu đã dựng cụm kind, cài runner Kubernetes theo `labs/k8s/values.yaml` và chạy cùng job `true`.

**Câu hỏi phải trả lời:** chi phí khởi tạo bao nhiêu giây? Với job 40 giây thì phần trăm phụ trội là bao nhiêu, và với job 8 phút thì bao nhiêu? Kết luận gì về QT 5.1?

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| Hạng mục | Điểm | Tiêu chí |
|---|---|---|
| `config-doc-duoc.toml` kèm 3 câu trả lời | 2 | Có `concurrent`, có nhận xét về `volumes` và `extra_hosts` |
| `phan-loai-su-co.md` — 6 sự cố phân loại theo pha và theo tệp | 3 | Đủ 6 dòng, mỗi dòng có cột "pha" và cột "thuộc tệp nào" |
| `nap-lai-config.txt` — kết quả đo + phiên bản runner | 2 | Thiếu phiên bản runner thì hạng mục này **0 điểm** |
| `ba-kenh-ro-ri.md` — bảng 3 kênh × 2 executor + 4 câu trả lời | 4 | Phải có cột "hậu quả thật ở nơi làm việc" và trả lời được câu 3 về ô của bảng hai thuộc tính |
| `chi-phi-khoi-tao.tsv` — 3 phép đo | 2 | Có cả ca image lạ; và trả lời được câu hỏi về tính phổ quát của "1–5 giây" |
| `do-concurrent.tsv` — 3 điểm đo + `nproc` + 3 câu trả lời | 4 | Thiếu `nproc` thì trừ 2; thiếu câu trả lời về `duration` trung bình thì trừ 2 |
| `ba-dieu-kien.md` — 3 lần, mỗi lần có **lệnh phân biệt** | 3 | Cột "lệnh duy nhất phát hiện được" là cột chấm chính |
| `doi-hinh-runner.md` — 4 nhóm + 4 câu trả lời | 4 | Mỗi ô phải có lập luận dẫn QT; ô trống thì trừ 1 mỗi ô |
| `checkpoint.log` — 12 dòng, không có `LỖI` | 2 | Chạy lại một checkpoint bất kỳ phải ra `ĐẠT` |
| **Tổng** | **26** | Đạt ≥ 16, đạt tốt ≥ 21 |

**Điểm trừ** — dẫn chiếu mục Bẫy hay gặp của `01-ly-thuyet.md` §9:

| Lỗi | Trừ |
|---|---|
| **Không khôi phục `config.toml`** ở §L8.1 | **Trần điểm 1 cho cả bài** — đây là để lại hạ tầng dùng chung ở trạng thái khác lúc đầu |
| `checkpoint.log` ghi ĐẠT nhưng chạy lại ra LỖI | **Trần điểm 1 cho cả bài** |
| Kết luận "chọn executor theo tốc độ" — bẫy 2 | −4 |
| `nap-lai-config.txt` chép đáp án thay vì đo (dấu hiệu: thiếu phiên bản runner) | −3 |
| Kết luận `concurrent` càng cao càng nhanh mà không nhìn `duration` trung bình — bẫy 5 | −3 |
| `ba-dieu-kien.md` thiếu cột lệnh phân biệt | −2 |
| Quên bỏ `paused` hoặc quên khởi động lại runner sau bước 4 | −2 |
| Nộp ảnh chụp màn hình thay kết quả API | **Trần điểm 1** cho hạng mục đó |

**Mức 3 của rubric buổi** đạt được khi làm thêm **một** trong ba việc: hoàn thành ≥ 3 bài BT của §L10 kèm câu trả lời; hoặc đo thêm executor `kubernetes` (BT8) và bổ sung nó vào bảng QT 5.1; hoặc áp `phan-loai-su-co.md` vào 10 sự cố thật của đội và nộp tỉ lệ theo tệp.

---

## Bảng đối soát thời lượng

| Bước | Nội dung | Thời lượng |
|---|---|---|
| L3 | Bước 1 — Tìm và đọc `config.toml`; đăng ký runner `shell`; đo tự nạp lại | 30' |
| L4 | Bước 2 — Đo ba kênh rò rỉ của executor `shell` | 30' |
| L5 | Bước 3 — Đo chi phí khởi tạo và đo `concurrent` ở ba mức | 30' |
| L6 | Bước 4 — Ba điều kiện nhận job; Docker socket là quyền root | 30' |
| L7 | Bước 5 — Thiết kế đội hình runner cho tổ chức giả định | 20' |
| L8 | Nộp sản phẩm, khôi phục `config.toml`, dọn dẹp | 10' |
| **Tổng** | | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---



**Quy tắc cho giảng viên:**

- Chọn **5–7 câu** trong 12, ưu tiên câu đánh dấu 🔥.
- **Gọi ngẫu nhiên.** Người trả lời sai thì người kế tiếp bổ sung; giảng viên không trả lời thay.
- Trả lời **bằng miệng, không nhìn tài liệu**.
- Khi học viên nói khẳng định định lượng, **luôn** hỏi lại "bao nhiêu". Từ buổi 02 trở đi đây là phản xạ bắt buộc, không phải nhắc nhở.
- Buổi này có một câu hỏi đặc thù giảng viên nên chen vào bất kỳ lúc nào học viên đề xuất sửa gì đó: **"sửa ở tệp nào?"** Câu ấy đo đúng luận đề của buổi.

**Thang điểm mỗi câu:**

| Điểm | Nghĩa |
|---|---|
| 0 | Không trả lời được, hoặc trả lời sai cơ chế |
| 1 | Nhắc được tên khái niệm nhưng không nêu được cơ chế |
| 2 | Nêu đúng cơ chế |
| 3 | Nêu đúng cơ chế **và** một con số, hoặc **và** một ca mà nó không đúng |

**Hai lỗi làm trần điểm cả buổi là 1:**

1. **Trả lời rằng chọn executor là chọn theo tốc độ.** Đây là hiểu sai trục, và nó dẫn tới quyết định hạ tầng sai ở mọi quy mô. Buổi 23 dựng thẳng lên trục đúng — người nhầm trục ở buổi 02 sẽ chọn sai cách build image ở buổi 23.
2. **Khẳng định rằng runner hiện chấm xanh nghĩa là nó nhận được job.** Chấm xanh chỉ nói về **một** trong ba điều kiện độc lập.

**Bốn câu phân loại thật của buổi này:**

| Câu | Phân loại điều gì |
|---|---|
| 4 | Phân loại người **đã vận hành runner `shell` thật**. Người chỉ đọc tài liệu kể được một kênh, hiếm khi kể đủ ba |
| 5 | Phân loại người **có ý thức bảo mật pipeline**. Người chưa nghĩ tới sẽ nói "socket để build image thôi mà" |
| 7 | Phân loại **tư duy hàng đợi** với tư duy số máy. Đây là câu phân biệt mạnh nhất cho vị trí platform |
| 12 | Phân loại **tư duy ranh giới trách nhiệm**. Câu này không có đáp án duy nhất; nó đo cách người ta chia bài toán |

---

## V2. Bộ câu hỏi


<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q01</span>
    <span>Một job GitLab CI được cấu hình bởi những tệp nào? Mỗi tệp quyết định điều gì?</span>
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
  **Hai** tệp, do **hai** người thường thuộc hai đội khác nhau viết.

`.gitlab-ci.yml` nói job **làm gì**: lệnh chạy, image mong muốn, artifact cần, khi nào chạy (`rules`), đòi runner có tag gì. Nó nằm trong repo, sửa bằng merge request, có tác giả và có lịch sử git, và chỉ ảnh hưởng một project.

`config.toml` nói job **chạy ở đâu và với quyền gì**: executor nào, image mặc định, `concurrent` và `limit`, volume nào được mount, mạng nào, kho cache ở đâu. Nó nằm trên máy runner tại `/etc/gitlab-runner/config.toml`, sửa trực tiếp, không qua review, và ảnh hưởng **mọi** project dùng runner đó.

Ranh giới ấy chính là ranh giới giữa "lỗi của tôi" và "lỗi của hạ tầng". Con số để đạt 3 điểm: **3 trên 8 pha** của một job thuộc phía hạ tầng — `prepare_executor`, `prepare_script`, và phần lớn `get_sources`. Lỗi ở ba pha đó thì sửa YAML không giúp gì.

**Tiêu chí chấm:**
- 0đ: Chỉ biết `.gitlab-ci.yml`.
- 1đ: Biết có `config.toml` nhưng không nói được nó quyết định gì.
- 2đ: Nêu đúng phân công giữa hai tệp.
- 3đ: Như trên, **và** nêu con số 3/8 pha, **và** nêu được khác biệt về **phạm vi ảnh hưởng** khi sửa hai tệp.

**Câu hỏi đào sâu:** Có thứ nào cả hai tệp cùng nói tới không? *(Có — `image`. `config.toml` cho mặc định, `image:` trong job ghi đè. Đây cũng là câu BTVN 4 chuẩn bị cho buổi 03 về thứ tự ưu tiên.)*
</div>
</details>

---

### Câu 2 — ★★

**Hỏi:** `config.toml` nằm ở đâu, và ai được sửa nó?

**Đáp án chuẩn:** `/etc/gitlab-runner/config.toml` khi runner chạy như dịch vụ hệ thống hoặc trong container; `~/.gitlab-runner/config.toml` khi chạy dưới người dùng thường. Với runner cài bằng Helm trên Kubernetes, nội dung nằm trong ConfigMap sinh từ `values.yaml`.

Ai sửa: người có quyền trên **máy runner**, không phải người có quyền trên project. Đó là một nhóm người khác hẳn, và thường là một đội khác.

Điểm cần nói để đạt 3 điểm: sửa `config.toml` là **hành động vận hành** — không qua merge request, không có review, không có lịch sử git, và có hiệu lực ngay với mọi project dùng runner đó. Quy trình tối thiểu là ba bước: sao lưu có mốc thời gian; đo phạm vi ảnh hưởng bằng API `runners/:id/jobs` xem runner đang phục vụ bao nhiêu project; sửa rồi kiểm ngay bằng một pipeline thử.

**Tiêu chí chấm:**
- 0đ: Không biết tệp nằm ở đâu.
- 1đ: Biết đường dẫn.
- 2đ: Biết đường dẫn và biết nó thuộc người vận hành runner.
- 3đ: Như trên, **và** nêu được ba bước quy trình, **và** nói rõ vì sao nó khác sửa `.gitlab-ci.yml` về phạm vi ảnh hưởng.

**Câu hỏi đào sâu:** Runner có tự nạp lại tệp khi nó đổi không? *(Đây là hành vi **phụ thuộc phiên bản** — phải đo, không tra. Cách đo: sửa `concurrent`, không khởi động lại, đẩy 6 job, đếm số job chạy song song. Trả lời "chắc chắn có" hoặc "chắc chắn không" mà không nói đã đo thì chỉ được 2 điểm ở câu này.)*

---

### Câu 3 — 🔥

**Hỏi:** Có bốn executor. Bạn chọn theo tiêu chí gì?

**Đáp án chuẩn:** Theo **một trục duy nhất: mức cô lập**. Không phải theo tốc độ.

```
   thấp ◄────────────── MỨC CÔ LẬP ──────────────► cao
   shell        docker        docker-autoscaler      kubernetes
```

Cái mà executor cung cấp là **một môi trường**, và chúng khác nhau ở việc môi trường ấy cô lập tới đâu khỏi máy chủ, khỏi các job khác, và khỏi các job trước đó. Tốc độ **chạy** một lệnh gần như giống nhau trên cả bốn — cùng nhân, cùng CPU. Cái khác nhau là **chi phí dựng và dỡ môi trường**, và đó chính là cái giá phải trả cho cô lập.

Con số để đạt 3 điểm — và phải nói rõ đây là số **đo được trên một máy cụ thể**, không phải hằng số: `shell` ≈ 0 giây; `docker` bậc 1–5 giây khi image đã có sẵn; `kubernetes` bậc 5–20 giây vì phải chờ xếp lịch pod; `docker-autoscaler` bậc 30–120 giây vì phải dựng máy ảo. Riêng `docker` với image chưa kéo là **bậc phút**, không phải bậc giây.

Câu hỏi thực hành để chọn: *"job này cần cô lập tới mức nào, và ta chịu được bao nhiêu giây khởi tạo?"*

**Tiêu chí chấm:**
- 0đ: "Cái nào nhanh hơn thì chọn." **Trần điểm cả buổi là 1.**
- 1đ: Kể được tên bốn executor.
- 2đ: Nêu đúng trục là mức cô lập và nêu được cái giá là chi phí khởi tạo.
- 3đ: Như trên, **và** nêu các con số kèm cảnh báo rằng chúng phụ thuộc máy, **và** nêu ca image chưa kéo là bậc phút.

**Câu hỏi đào sâu:** Kể một tình huống chọn `kubernetes` là **sai**. *(Pipeline gồm 10 job lint mỗi job 8 giây: trên `docker` khoảng 2 giây phụ trội mỗi job → tổng ~100 giây; trên `kubernetes` khoảng 12 giây → tổng ~200 giây. Chậm gấp đôi, mà job lint không đụng secret nên phần cô lập thêm không mua được giá trị nào.)*

---

### Câu 4 — ★★★

**Hỏi:** Executor `shell` rò rỉ trạng thái giữa các job. Rò rỉ qua đường nào?

**Đáp án chuẩn:** **Ba kênh**, và cả ba đều là "ở ngoài thư mục dự án":

| Kênh | Ví dụ cụ thể | Hậu quả nguy hiểm nhất |
|---|---|---|
| (a) Hệ tệp ngoài thư mục dự án | `/tmp/token`, `~/.aws/credentials`, `~/.npmrc`, `~/.docker/config.json` | Job sau đọc được **secret** của job trước |
| (b) Tiến trình nền còn sống | `npm start &`, `docker run -d`, server test không được tắt | Job sau **kết nối nhầm** vào service của job trước và test **qua** một cách sai |
| (c) Trạng thái công cụ toàn cục | `npm i -g`, `pip install --user`, `git config --global`, sửa `~/.bashrc` | Pipeline xanh nhờ gói do job khác cài **tuần trước**; ngày dựng lại máy thì đỏ hàng loạt |

Vì sao có ba kênh này: với `shell`, môi trường job **là chính máy chủ**. Runner chỉ tạo thư mục build rồi chạy script trong đó; nó không có cơ chế nào hoàn tác những gì script đã làm ở ngoài thư mục ấy.

Điểm quan trọng nhất để đạt 3 điểm: rò rỉ thuộc ô **im lặng, không chặn** — ô nguy hiểm nhất của bảng hai thuộc tính. Nó tệ hơn một job đỏ vì pipeline **vẫn xanh**, và nó xanh **nhờ** trạng thái rò rỉ. Không có tín hiệu nào cho tới ngày máy runner được dựng lại.

**Tiêu chí chấm:**
- 0đ: "Nó dùng chung máy nên có thể lẫn."
- 1đ: Kể được một kênh, thường là kênh (a).
- 2đ: Kể đủ ba kênh với ví dụ cụ thể.
- 3đ: Như trên, **và** xếp được nó vào ô im lặng + không chặn, **và** nêu được ca (b) job sau kết nối nhầm và test qua sai.

**Câu hỏi đào sâu:** Dọn ba kênh này bằng `after_script` được không? *(Kênh (a) và (b) dọn được nếu nhớ đường dẫn và PID. Kênh (c) rất khó, vì không biết job đã đổi gì trong trạng thái toàn cục. Và nhớ buổi 01 QT 4.3: `after_script` là shell khác, nên phải truyền PID qua tệp trong thư mục dự án chứ không qua biến.)*

---

### Câu 5 — ★★★

**Hỏi:** Trong `config.toml` có dòng `volumes = ["/var/run/docker.sock:/var/run/docker.sock"]`. Điều đó nghĩa là gì?

**Đáp án chuẩn:** Nghĩa là **mức cô lập của executor `docker` đã bị vô hiệu hoá**, và mọi job chạy trên runner đó có quyền **tương đương root trên máy chủ**.

Cơ chế: Docker socket là giao diện điều khiển đầy đủ của Docker daemon, và daemon chạy dưới quyền root. Không có phân quyền bên trong socket — có socket là có tất cả. Tiến trình nào gọi được nó thì tạo được container bất kỳ với tuỳ chọn bất kỳ, kể cả container mount thẳng `/` của máy chủ:

```bash
docker run --rm -v /:/host alpine cat /host/etc/shadow
```

Ba dòng đó chạy được **từ bên trong job**, và job đọc được toàn bộ hệ tệp máy chủ — kể cả `config.toml`, kể cả thông tin xác thực của các runner khác.

Con số để đạt 3 điểm: **một dòng** cấu hình đủ để phá toàn bộ cô lập. Và nếu runner đó là runner cấp **instance** thì mọi người tạo được project trên GitLab ấy đều có đường tới đó — đây là kết hợp của QT 5.3 với QT 7.1, và là lối vào số 1 trong mô hình đe doạ ở buổi 28.

**Tiêu chí chấm:**
- 0đ: "Để job build được image."
- 1đ: Biết là có rủi ro nhưng không nêu được cơ chế.
- 2đ: Nêu đúng cơ chế socket là root và cho được ví dụ lệnh.
- 3đ: Như trên, **và** kết hợp với mức phạm vi runner (instance thì ai cũng tới được), **và** nêu được hướng thay thế.

**Câu hỏi đào sâu:** Vậy build image thế nào cho đúng? *(Ba đường không cần socket: kaniko, buildah, BuildKit rootless. Buổi 23 dành trọn cho việc so ba đường ấy — và tiêu chí so là **đặc quyền cần có**, đúng theo trục của QT 5.1.)*

---

### Câu 6 — ★★

**Hỏi:** Phân biệt `concurrent`, `limit`, `request_concurrency`.

**Đáp án chuẩn:**

| Khoá | Ở đâu trong tệp | Điều khiển gì |
|---|---|---|
| `concurrent` | Cấp cao nhất, **ngoài** mọi khối `[[runners]]` | Trần số job của **cả tiến trình runner** |
| `limit` | **Trong** một khối `[[runners]]` | Trần số job của **riêng mục runner đó** |
| `request_concurrency` | Trong một khối `[[runners]]` | Số yêu cầu **hỏi việc** gửi song song tới GitLab — **không** phải số job chạy |

Số job thật sự chạy đồng thời là **min của `concurrent` và `limit`**, không phải tổng. Đặt `limit = 10` khi `concurrent = 4` thì `limit` vô nghĩa.

Con số để đạt 3 điểm: mặc định `concurrent = 1` khi cài mới. Đây là con số làm rất nhiều người tưởng runner hỏng, vì job thứ hai luôn phải chờ job thứ nhất. Kèm cảnh báo: con số **không phổ quát** — bản cài qua Helm hoặc qua image dựng sẵn thường đặt khác, nên phải **đọc giá trị thật** thay vì giả định.

**Tiêu chí chấm:**
- 0đ: Không phân biệt được.
- 1đ: Biết `concurrent` là số job song song.
- 2đ: Phân biệt đúng cả ba, và biết trần thật là min.
- 3đ: Như trên, **và** nêu mặc định `concurrent = 1` kèm cảnh báo nó không phổ quát.

**Câu hỏi đào sâu:** Làm sao biết đang nghẽn ở `concurrent` hay ở `request_concurrency`? *(Nhìn `queued_duration` của một loạt job: tăng dần đều theo thứ tự → nghẽn ở khâu hỏi việc; nhảy bậc theo nhóm → nghẽn ở `concurrent`, vì mỗi nhóm là một lứa job chạy cùng lúc.)*

---

### Câu 7 — ★★★

**Hỏi:** Đội bạn phàn nàn pipeline chờ lâu. Bạn có nên thêm runner không?

**Đáp án chuẩn:** Chưa biết — phải **đo trước**. Đây là bài toán hàng đợi, không phải bài toán số máy.

Thời gian một job hoàn thành gồm hai phần: thời gian **chờ trong hàng đợi** và thời gian **được phục vụ**. Tăng `concurrent` hoặc thêm runner giảm phần thứ nhất nhưng có thể **tăng** phần thứ hai, vì các job tranh cùng một lượng CPU và cùng một đĩa. Khi phần tăng vượt phần giảm, **tổng thời gian đi lên**.

Hai phép đo phải làm trước:

1. **Nút cổ chai.** `docker stats` trong lúc pipeline chạy, cộng `nproc`. Nếu tổng CPU đã gần `nproc × 100%` thì thêm runner không giúp gì — nó chỉ chia nhỏ cùng một lượng tài nguyên.
2. **`duration` trung bình của một job theo mức tải.** Chạy cùng một tải ở `concurrent` = 2, 4, 8 và xem `duration` trung bình có tăng không. Nếu có, đó là bằng chứng đang tranh tài nguyên.

Phát biểu gọn để đạt 3 điểm: **`concurrent` chỉ nên tăng tới mức mà thời lượng trung bình của một job chưa đổi đáng kể.** Vượt mức đó là đang chia nhỏ cùng một lượng tài nguyên cho nhiều job hơn.

Nếu nút cổ chai **không** phải máy chủ mà là số slot, thì thêm runner đúng là giải pháp — và khi ấy câu hỏi tiếp theo là autoscaling, tức buổi 13.

**Tiêu chí chấm:**
- 0đ: "Có, thêm runner cho nhanh."
- 1đ: Nói được là còn tuỳ, không nêu được đo gì.
- 2đ: Nêu đúng hai phép đo và giải thích cơ chế tranh tài nguyên.
- 3đ: Như trên, **và** phát biểu được quy tắc dừng bằng `duration` trung bình, **và** nêu được ca thêm runner đúng là giải pháp.

**Câu hỏi đào sâu:** Đo `queued_duration` trung bình hay trung vị? *(**Trung vị.** Vài job nằm `pending` 60 phút vì lỗi định tuyến sẽ làm hỏng trung bình hoàn toàn, và khi đó con số không phản ánh trải nghiệm của đa số job.)*

---

### Câu 8 — ★★

**Hỏi:** Runner có mấy mức phạm vi, và điều đó ảnh hưởng gì tới bảo mật?

**Đáp án chuẩn:** Ba mức: **instance**, **group**, **project**. Chúng khác nhau ở **project nào giao việc được cho runner**.

| Mức | Ai giao việc được | Rủi ro |
|---|---|---|
| Instance | **Mọi project** trên GitLab đó | Một runner bị chiếm là **mọi** project bị ảnh hưởng |
| Group | Project trong group | Giới hạn trong group |
| Project | Đúng một project | Thấp nhất, tốn công quản lý nhất |

Vì sao đây là chuyện bảo mật: job chạy **mã tuỳ ý** do người viết pipeline quyết định. Một runner instance thực chất là một máy cho phép **mọi người trong tổ chức** chạy mã trên đó. Nếu runner ấy còn mount Docker socket hoặc có sẵn thông tin xác thực cloud trong biến môi trường, thì bất kỳ ai tạo được một project đều lấy được cả hai.

Quy tắc thực hành để đạt 3 điểm: **runner instance dùng cho job build và test; job deploy dùng runner project hoặc group, gắn với protected environment.** Buổi 45 xử lý đầy đủ cơ chế cưỡng chế.

**Tiêu chí chấm:**
- 0đ: Không biết có ba mức.
- 1đ: Kể được ba mức.
- 2đ: Nêu đúng khác biệt và nêu được rủi ro của mức instance.
- 3đ: Như trên, **và** nêu quy tắc tách runner deploy, **và** kết hợp được với QT 5.3 (socket trên runner instance).

**Câu hỏi đào sâu:** Merge request từ một fork chạy trên runner nào? *(Mặc định chạy trên runner của project gốc — đó chính là chỗ mã của người ngoài chạy trên hạ tầng của mình. Buổi 28 gọi đây là một trong bảy lối vào và nêu cách chặn.)*

---

### Câu 9 — 🔥

**Hỏi:** Runner hiện chấm xanh trên giao diện, nhưng job vẫn nằm `pending`. Chuyện gì đang xảy ra?

**Đáp án chuẩn:** Chấm xanh chỉ nói về **một** trong **ba** điều kiện độc lập. Để runner nhận được một job cụ thể cần cả ba:

| # | Điều kiện | Nghĩa là gì | Hỏng vì lý do gì |
|---|---|---|---|
| 1 | `online` | Runner còn gửi nhịp tim (`contacted_at` được cập nhật) | Tiến trình chết, mất mạng |
| 2 | Không `paused` | Công tắc thủ công trên GitLab đang bật | Ai đó tạm dừng, và **runner đang chạy tốt vẫn có thể `paused`** |
| 3 | Khớp định tuyến | Tag của job là tập con của tag runner, hoặc job không tag và runner có `run_untagged` | Tag gõ sai, ai đó bỏ tick "Run untagged jobs" |

Điểm cốt lõi: **thiếu bất kỳ điều nào cũng cho cùng một triệu chứng** — job `pending`, log rỗng. Log rỗng vì log chỉ tồn tại sau khi runner nhận job (buổi 01 QT 6.3).

Vì cả ba cho cùng triệu chứng, chẩn đoán bằng cách nhìn giao diện là không đủ. Kiểm cả ba bằng một lệnh:

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/runners/$ID" \
| jq '{online, paused, run_untagged, tag_list}'
```

Con số để đạt 3 điểm: **3 điều kiện, 1 triệu chứng**. Và với mặc định, job chờ **60 phút** mới đổi màu — tức 60 phút im lặng hoàn toàn.

**Tiêu chí chấm:**
- 0đ: "Chắc GitLab lag." Hoặc: "Chấm xanh thì runner ổn rồi." **Trần điểm cả buổi là 1.**
- 1đ: Đoán được là do tag.
- 2đ: Nêu đủ ba điều kiện.
- 3đ: Như trên, **và** nhấn được điểm "ba nguyên nhân một triệu chứng", **và** đưa được lệnh API kiểm cả ba.

**Câu hỏi đào sâu:** Ô nào của bảng hai thuộc tính? *(Im lặng, **có chặn**. Không phải ô tệ nhất — vì có chặn nên sớm muộn cũng có người thắc mắc sao pipeline lâu thế. Ô tệ nhất là im lặng + không chặn, ví dụ rò rỉ trạng thái ở executor `shell`.)*

---

### Câu 10 — ★★★

**Hỏi:** Trên executor `kubernetes`, job nằm `pending`. Bạn chẩn đoán thế nào?

**Đáp án chuẩn:** `kubernetes` **đổi bài toán**, không xoá bài toán: từ "máy có đủ tài nguyên không" sang "pod có được xếp lịch không".

Runner không tự chạy job — nó tạo một pod và chờ cụm xếp lịch. Nếu cụm hết CPU, hết bộ nhớ, hoặc không node nào thoả `nodeSelector`, pod nằm `Pending` và job nằm chờ. **Từ phía GitLab, trạng thái job trông y hệt ca không có runner.** Nhưng nguyên nhân, người phải sửa, và cách sửa đều khác hẳn.

Phải hỏi **hai** nguồn, và đây là điểm chính của câu:

```bash
# Nguồn 1 — phía GitLab: ba điều kiện của QT 7.2
curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/runners/all" | jq '.[] | {id, online, paused}'

# Nguồn 2 — phía cụm: pod có được xếp lịch không
kubectl get pods -n gitlab-runner --field-selector=status.phase=Pending
kubectl get events -n gitlab-runner --sort-by=.lastTimestamp | tail -20
```

Dòng `0/3 nodes are available: Insufficient cpu` chỉ có ở **nguồn thứ hai**, và nó là câu trả lời. Người chỉ hỏi nguồn thứ nhất sẽ kết luận "thiếu runner" rồi đăng ký thêm runner — mà cụm vẫn hết tài nguyên, nên không có gì thay đổi.

Chi tiết để đạt 3 điểm: `poll_timeout` trong `config.toml` là chỗ ca im lặng này cuối cùng trở thành ồn ào — sau khoảng thời gian đó runner bỏ cuộc và job **đỏ**. Nghĩa là ô của bảng hai thuộc tính là **im lặng, có chặn**, với thời gian phát hiện bằng `poll_timeout`.

**Tiêu chí chấm:**
- 0đ: "Giống như trên `docker` thôi."
- 1đ: Biết là liên quan tới cụm nhưng không nêu được cách kiểm.
- 2đ: Nêu đúng hai giả thuyết và hai nguồn dữ liệu.
- 3đ: Như trên, **và** nêu `poll_timeout` là chỗ nó chuyển thành ồn ào, **và** nói rõ vì sao chỉ hỏi API GitLab là chưa đủ.

**Câu hỏi đào sâu:** Đặt `cpu_request` cao hay thấp thì tốt hơn? *(Đánh đổi: cao thì pod khó được xếp lịch nhưng job chạy nhanh và ổn định; thấp thì dễ được xếp lịch nhưng job có thể bị bóp CPU và chậm bất thường. Không có đáp án chung — phải đo `duration` ở hai mức. Buổi 13 làm phép đo ấy.)*

---

### Câu 11 — ★★★

**Hỏi:** Ba tình huống. Chọn executor cho mỗi cái và nói vì sao: (a) job lint chạy trên merge request của người ngoài; (b) job build Docker image; (c) job deploy production có thông tin xác thực cloud.

**Đáp án chuẩn:**

**(a) Job lint trên MR của người ngoài** — `docker` (hoặc `kubernetes` nếu đã có cụm). **Tuyệt đối không** `shell`: mã được chạy là mã người lạ gửi tới, và ba kênh rò rỉ của QT 5.2 trở thành ba lối tấn công. Kênh (a) đặc biệt nguy hiểm — người lạ đọc được `~/.aws/credentials` hoặc `~/.docker/config.json` mà job trước để lại. Runner cấp instance chấp nhận được vì job lint không đụng secret, nhưng phải chắc nó **không** mount Docker socket.

**(b) Job build Docker image** — vẫn `docker`, nhưng câu hỏi thật nằm ở chỗ khác: **có mount socket hay không**. Hai phương án, và đây là trục đánh đổi:

| Phương án | Được | Mất |
|---|---|---|
| Mount socket (dind hoặc socket máy chủ) | Đơn giản, cache layer tốt | Job có quyền root máy chủ (QT 5.3) |
| Không socket (kaniko / buildah / BuildKit rootless) | Giữ nguyên cô lập | Cấu hình phức tạp hơn, cache layer khác cách |

Buổi 23 so đầy đủ ba đường không cần socket.

**(c) Job deploy production** — `docker`, nhưng điều quyết định **không phải** executor mà là **mức phạm vi runner**: phải là runner **project hoặc group**, gắn với protected environment, và **tách hẳn** khỏi runner chạy job của MR người ngoài. Lý do: nếu dùng chung runner instance với tình huống (a), thì mã của người lạ chạy trên cùng máy có thông tin xác thực cloud — và với executor `shell` thì kênh (a) của QT 5.2 đưa thẳng secret ra ngoài.

**Tiêu chí chấm:**
- 0đ: Chọn cùng một executor cho cả ba mà không lập luận.
- 1đ: Chọn đúng nhưng lập luận theo tốc độ.
- 2đ: Chọn đúng cả ba với lập luận theo mức cô lập.
- 3đ: Như trên, **và** nhận ra rằng ở (c) yếu tố quyết định là **mức phạm vi runner** chứ không phải executor, **và** nêu được trục đánh đổi ở (b).

**Câu hỏi đào sâu:** Ở (c), `concurrent` nên đặt bao nhiêu? *(Rất thấp, thường 1–2. Job deploy chạy 5 lần một ngày nên hàng đợi không phải vấn đề, còn `concurrent` thấp làm giảm khả năng hai lần deploy chồng nhau. Buổi 36 dùng `resource_group` để cưỡng chế điều đó ở tầng pipeline thay vì tầng runner.)*

---

### Câu 12 — 🔥

**Hỏi:** Một pipeline hỏng. Làm sao bạn biết đây là việc của bạn hay việc của đội hạ tầng?

**Đáp án chuẩn:** Đây là câu tổng hợp của cả buổi, và đáp án tốt đi theo ba nhịp.

**Nhịp 1 — xác định pha, mất 10 giây.** Tìm dòng tiêu đề pha cuối cùng xuất hiện **trước** thông báo lỗi. Mẹo nhanh nhất: nếu log **không có** dòng `Executing "step_script" stage of the job script` thì lệnh của mình **chưa chạy lần nào** — chuyện này thuộc phía hạ tầng, và sửa `.gitlab-ci.yml` là vô ích.

**Nhịp 2 — ánh xạ pha sang tệp.** Ba pha đầu — `prepare_executor`, `prepare_script`, phần lớn `get_sources` — thuộc `config.toml`. Năm pha còn lại thuộc `.gitlab-ci.yml`. `get_sources` là ranh giới: nó đọc vài biến `GIT_*` từ YAML nhưng phần lớn hành vi đến từ runner.

**Nhịp 3 — nếu không có log gì cả**, tức job `pending`, thì không có pha nào để đọc. Chuyển sang kiểm **ba điều kiện** của QT 7.2 bằng API: `online`, không `paused`, khớp định tuyến. Nếu executor là `kubernetes` thì hỏi thêm nguồn thứ hai: `kubectl get events`.

Điểm cần nói để đạt 3 điểm: việc phân loại này không chỉ tiết kiệm thời gian gỡ lỗi — nó còn quyết định **đề nghị đúng người**. Đề nghị người vận hành runner sửa một lỗi thuộc `.gitlab-ci.yml` làm mất thời gian của cả hai bên và làm hỏng quan hệ giữa hai đội.

Con số: **3 trên 8 pha** thuộc phía hạ tầng — khoảng 37% các chỗ một job có thể hỏng nằm ngoài tầm với của người viết pipeline.

**Tiêu chí chấm:**
- 0đ: "Chạy lại xem sao."
- 1đ: Đọc log tìm chữ `ERROR`.
- 2đ: Xác định pha trước, rồi ánh xạ sang tệp.
- 3đ: Đủ ba nhịp, **và** nêu con số 3/8, **và** nêu được lý do "đề nghị đúng người" chứ không chỉ "gỡ nhanh hơn".

**Câu hỏi đào sâu:** Pipeline của một đội gãy mà đội đó không đổi gì. Câu hỏi đầu tiên bạn hỏi là gì? *("Có ai đổi `config.toml` của runner không?" Và câu hỏi ấy thường không trả lời được, vì sửa `config.toml` không qua merge request và không có lịch sử git. Đó chính là lý do QT 4.3 đòi sao lưu có mốc thời gian.)*

---

## V3. Câu chốt để nói khi phỏng vấn

> Bốn câu viết **nguyên văn, đúng ngữ điệu nói**. Tập nói to tới khi trôi chảy mà không phải nghĩ.
> Mỗi câu chứa một con số hoặc một cơ chế.

**Câu 1 — khi được hỏi "bạn phân biệt lỗi CI thế nào":**

> "Việc đầu tiên tôi làm là phân loại xem lỗi thuộc tệp nào. Một job được cấu hình bởi hai tệp: `.gitlab-ci.yml` nói job làm gì, `config.toml` nói job chạy ở đâu và với quyền gì. Ba trong tám pha của một job — chuẩn bị executor, chuẩn bị môi trường, và phần lớn việc lấy mã nguồn — hoàn toàn thuộc phía hạ tầng. Nghĩa là khoảng ba mươi bảy phần trăm số chỗ một job có thể hỏng nằm ngoài tầm với của tôi với tư cách người viết pipeline. Phân loại được điều đó không chỉ gỡ nhanh hơn — nó còn giúp tôi đề nghị đúng người."

**Câu 2 — khi được hỏi "chọn executor thế nào":**

> "Tôi không chọn theo tốc độ, tôi chọn theo mức cô lập. Bốn executor xếp trên đúng một trục: shell không cô lập gì, docker cô lập hệ tệp, kubernetes cô lập cả tài nguyên. Tốc độ chạy lệnh thì gần như nhau vì cùng nhân, cùng CPU — cái khác nhau là chi phí khởi tạo, và đó chính là cái giá phải trả cho cô lập. Trên máy tôi đo được shell gần như bằng không, docker khoảng hai giây khi image có sẵn, kubernetes khoảng mười hai giây. Với job build tám phút thì chênh lệch ấy nằm dưới nhiễu; với job lint tám giây thì nó gấp đôi thời gian."

**Câu 3 — khi được hỏi về bảo mật pipeline:**

> "Thứ tôi kiểm đầu tiên trong `config.toml` là dòng `volumes`. Nếu có mount Docker socket thì toàn bộ mức cô lập của executor docker bị vô hiệu hoá bằng đúng một dòng — vì socket là giao diện điều khiển đầy đủ của daemon, mà daemon chạy dưới root, và bên trong socket không có phân quyền. Job nào gọi được nó thì `docker run -v /:/host` là đọc được cả máy chủ. Nếu runner đó lại là runner cấp instance thì mọi người tạo được project trên GitLab ấy đều có đường tới đó."

**Câu 4 — khi được hỏi "pipeline chờ lâu thì làm gì":**

> "Tôi không thêm runner trước, tôi đo trước. Đây là bài toán hàng đợi chứ không phải bài toán số máy: tăng số job song song thì giảm thời gian chờ nhưng có thể tăng thời gian phục vụ, vì các job tranh cùng một lượng CPU. Tôi chạy cùng một tải ở ba mức concurrent và nhìn hai con số: tổng thời gian đồng hồ, và thời lượng trung bình của một job. Quy tắc dừng của tôi là tăng concurrent tới mức mà thời lượng trung bình của một job chưa đổi đáng kể — vượt mức đó là đang chia nhỏ cùng một lượng tài nguyên cho nhiều job hơn."

---

## V4. Bảng ghi điểm

| Học viên | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | Tổng | Trần điểm? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | |

**Quy đổi** (tính trên số câu thực hỏi, mỗi câu tối đa 3 điểm):

| Tỉ lệ điểm | Kết luận |
|---|---|
| ≥ 80% | Nắm vững. Giao BT8 của §L10 (executor `kubernetes`) làm trước buổi 13 |
| 60–79% | Đạt. Đọc lại quy tắc bị mất điểm trước buổi 03 |
| 40–59% | Chưa đạt. Làm lại bước lab tương ứng ở nhà |
| < 40% | Chưa đạt. Học lại cả buổi — buổi 13 và buổi 23 dựng thẳng lên mô hình này |

**Bảng lỗi làm trần điểm là 1:**

| Lỗi | Vì sao nghiêm trọng đến mức trần điểm |
|---|---|
| "Chọn executor theo tốc độ" | Hiểu sai trục; dẫn tới quyết định hạ tầng sai ở mọi quy mô, và sẽ chọn sai cách build image ở buổi 23 |
| "Runner chấm xanh nghĩa là nó nhận được job" | Chấm xanh chỉ nói về **một** trong ba điều kiện độc lập; hiểu sai này làm mất hàng giờ ở mỗi ca job `pending` |
| Nói "nhanh hơn nhiều", "tốn lắm" và khi hỏi lại vẫn không có số | Vi phạm nguyên tắc của khoá; ở phỏng vấn thật đây là dấu hiệu người chưa đo bao giờ |

---

## V5. Bài tập về nhà

### BTVN 1. Đọc ba dòng `config.toml` của đội mình

Lấy `config.toml` của runner đội mình (hoặc hỏi người vận hành) và đọc đúng ba dòng: `concurrent`, `executor`, `volumes`.

**Nộp:** ba giá trị, và trả lời: (a) runner có mount Docker socket không; (b) nếu có, ai trong tổ chức giao việc được cho runner ấy — tức mức phạm vi của nó là gì.

### BTVN 2. Kiểm ba điều kiện cho mọi runner

Chạy đoạn kiểm ba điều kiện của QT 7.2 cho mọi runner mà đội mình dùng.

**Nộp:** bảng kết quả, và danh sách **runner ma** — runner `online` nhưng không nhận job nào trong 7 ngày. Với mỗi runner ma, nêu một lý do nên tắt nó.

### BTVN 3. Đo `concurrent` của đội mình

Không đổi cấu hình. Chỉ lấy 100 job gần nhất qua API và tính: `queued_duration` **trung vị**, và số job nhiều nhất chạy song song tại một thời điểm.

**Nộp:** hai con số, và trả lời: theo QT 6.2, hai con số ấy có đủ để kết luận nên tăng `concurrent` không? Còn thiếu phép đo nào?

### BTVN 4. Chuẩn bị cho buổi 03

Trả lời ba câu sau bằng viết, mỗi câu 3–5 dòng. Mang theo vào buổi 03.

1. Mở `.gitlab-ci.yml` của một project bất kỳ. Những khoá nào nằm ở **cấp trên cùng** — tức không nằm trong bất kỳ job nào? Liệt kê ít nhất **bốn** và đoán mỗi cái làm gì.
2. Buổi 01 nói `stage` nhóm các job lại. Hãy đoán: hai job **cùng `stage`** có **chắc chắn** chạy **cùng lúc** không? Điều gì quyết định chuyện đó — và gợi ý: câu trả lời có liên quan tới một quy tắc bạn vừa học hôm nay.
3. Nếu `image` được khai trong `config.toml` (làm mặc định) **và** cũng được khai trong một job, cái nào thắng? Ghi phỏng đoán của bạn cùng lập luận; buổi 03 sẽ **đo** thay vì tra tài liệu.

**Ba câu này dẫn vào đâu:** câu 1 dẫn vào §4 buổi 03 về cấu trúc tệp `.gitlab-ci.yml` và khối `default`; câu 2 dẫn vào §5 buổi 03 với luận đề *`stage` là ràng buộc **thứ tự**, không phải ràng buộc **dữ liệu*** — và câu trả lời đúng cần `concurrent` của hôm nay, tức hai job cùng stage chỉ chạy cùng lúc khi có đủ slot; câu 3 dẫn vào §6 buổi 03 về thứ tự ưu tiên giữa `config.toml`, `default`, và khai báo trong job — nối thẳng vào QT 4.1 hôm nay.
{% endraw %}
