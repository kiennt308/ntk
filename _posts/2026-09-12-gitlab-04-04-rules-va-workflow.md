---
layout: post
title: "[Bài 04] Điều Khiển Luồng Thực Thi Nâng Cao Với Rules & Workflow: rules:if, changes, exists & workflow:rules"
date: 2026-09-12 09:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-04
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 4
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.04] Hướng dẫn chuyên sâu Điều Khiển Luồng Thực Thi Nâng Cao Với Rules & Workflow: rules:if, changes, exists & workflow:rules: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Điều Khiển Luồng Thực Thi Nâng Cao Với Rules & Workflow: rules:if, changes, exists & workflow:rules."
  - "Thiết kế CI/CD Pipeline chuẩn Enterprise với kiến trúc DAG, tối ưu hóa thời gian build và caching hiệu quả."
  - "Bảo mật chuỗi cung ứng phần mềm với SAST/DAST, Container Scanning và OIDC Authentication."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 04] ĐIỀU KHIỂN LUỒNG THỰC THI NÂNG CAO VỚI RULES & WORKFLOW: RULES:IF, CHANGES, EXISTS & WORKFLOW:RULES

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7.
> Mọi đoạn YAML dán được vào `.gitlab-ci.yml` và kiểm được bằng `ci/lint` trong 1 giây.

---





| # | Câu hỏi | Đáp án vắn tắt |
|---|---|---|
| 1 | `stage` cho gì và không cho gì | Cho **ràng buộc thứ tự**. Không chuyển dữ liệu — **0 byte**; không đảm bảo song song (`concurrent` mới quyết định) |
| 2 | Khoá cấp trên cùng không dành riêng là gì | **Một job.** Gõ sai `variables` thành `variabels` thì GitLab tạo job rác, và `ci/lint` vẫn trả `valid: true` — phải so **danh sách job** |
| 3 | Lãng phí hàng rào tính thế nào | **Tổng thời gian pipeline − đường găng dữ liệu thật** |
| 4 | Ba khối lệnh chạy trong mấy shell | **3 khối, 2 shell.** `before_script` và `script` chung; `after_script` riêng — để nó chạy được kể cả khi `script` đã chết |
| 5 | Ba nấc ưu tiên | `config.toml` → `default:` → trong job. **Gần job nhất thắng, và nó THAY THẾ chứ không hợp nhất** |



Buổi 03 để lại một câu hỏi và BTVN 4 đã hỏi thẳng: *"kể ba cách làm một job không chạy"*. Ba cách ấy khác nhau **không** ở cú pháp mà ở **thời điểm quyết định**:

| Cách | Quyết định lúc nào |
|---|---|
| `rules` không khớp | Lúc pipeline được **tạo** |
| `when: manual` không ai bấm | Lúc pipeline đang **chạy** |
| Job trước đỏ nên job sau `skipped` | Lúc job trước **thực thi xong** |

Hiểu trục thời gian ấy giải thích được toàn bộ phần còn lại của buổi, kể cả những chỗ trông như lỗi của GitLab.

**Luận đề trung tâm.**

> **`rules` được đánh giá ĐÚNG MỘT LẦN — lúc pipeline được TẠO, không phải lúc job sắp chạy. Danh sách job của một pipeline được chốt tại thời điểm ấy và không gì đổi được nó sau đó. Mọi thứ khó hiểu về `rules` đều là hệ quả trực tiếp của một câu đó.**

```
   t0: git push / MR / tag / schedule / API / trigger
        │
        ├─► workflow:rules đánh giá  →  KHÔNG khớp → KHÔNG CÓ PIPELINE (im lặng)
        │
        ├─► rules của TỪNG job đánh giá  →  không khớp → job KHÔNG CÓ MẶT
        │
        └─► DANH SÁCH JOB CHỐT TẠI ĐÂY ◄── không gì đổi được nữa
             │
   t1..tn:  ├─ job chạy · job đỏ · job manual bấm hay không bấm
             └─ biến do dotenv sinh ra ← KHÔNG dùng được trong rules (đã quá muộn)
```

| Kết quả buổi trước | Nguồn | Dùng ở đâu hôm nay |
|---|---|---|
| `ci/lint` cho tệp sau phân giải | buổi 03 QT 4.3 | **Toàn bộ bước 1 lab** — đọc `rules` sau phân giải, không đoán |
| Khoá cấp trên cùng | buổi 03 QT 4.1 | §5 — `workflow` là một trong 13 từ khoá đó |
| Hàng rào stage | buổi 03 QT 5.3 | §7 — job biến mất nhưng **hàng rào vẫn còn** |
| Bốn đường vào; `dotenv` là đường thứ tư | buổi 01 QT 5.1, 5.4 | §4 QT 4.2 — nó tới **quá muộn** cho `rules` |
| Ba nấc ưu tiên | buổi 03 QT 7.1 | §6 — `rules` **không** theo quy tắc đó; nó dừng ở **khớp đầu tiên** |

Đây là **lần thứ TƯ** khoá học dùng bảng hai thuộc tính hỏng của buổi 01 QT 7.1, và cũng là **lần thứ TƯ** áp quy tắc *hành vi phụ thuộc phiên bản thì phải ĐO*.

**Ba câu hỏi trung tâm của buổi:**

1. `rules` được đánh giá **lúc nào**, và điều đó **cấm** ta làm gì?
2. Ba cách làm một job không chạy cho **ba trạng thái** nào, và hệ quả lên job phụ thuộc khác nhau ra sao?
3. Vì sao mở một merge request lại sinh **hai** pipeline, và chặn nó ở đâu?

---



| # | Làm được gì | Hiện vật chứng minh |
|---|---|---|
| LĐ1 | Trả lời được câu "sao job này không chạy" bằng **một bảng**, không đoán | `bang-chan-tri.tsv`, lab bước 1 |
| LĐ2 | Nói được `rules` đánh giá lúc nào và điều đó cấm gì | Lab bước 5, CHECKPOINT 11 |
| LĐ3 | Phân biệt được ba trạng thái "không chạy" và hệ quả từng cái | `ba-trang-thai.md`, lab bước 4 |
| LĐ4 | **Đo được** số pipeline trùng và phút runner lãng phí | `pipeline-trung.tsv`, lab bước 2 |
| LĐ5 | Viết được `workflow` chuẩn cho một repo, kiểm đủ 6 nguồn kích hoạt | `workflow-chuan.yml`, lab bước 5 |
| LĐ6 | Chỉ ra được ca `rules:changes` âm thầm sai | Lab bước 3, CHECKPOINT 8 |
| LĐ7 | Chẩn đoán được ca "pipeline không được tạo" | Lab bước 5, CHECKPOINT 11 |

---



| Cần biết | Mức | Nguồn nếu thiếu |
|---|---|---|
| `ci/lint` đọc tệp sau phân giải | **Vận dụng** | Buổi 03 QT 4.3 — dùng suốt buổi |
| `stage` là hàng rào thời gian | Vận dụng | Buổi 03 QT 5.1, 5.3 |
| Bốn đường vào; `dotenv` là cơ chế duy nhất truyền biến | **Vận dụng** | Buổi 01 QT 5.1, 5.4 — **tiền đề của QT 4.2** |
| Bảng hai thuộc tính hỏng | Vận dụng | Buổi 01 QT 7.1 |
| Tạo được nhánh, tag, merge request trên GitLab | Vận dụng | Lab bước 1 cần cả sáu nguồn kích hoạt |

---



### 3.1. Đối chiếu thuật ngữ

| Tiếng Việt | Tiếng Anh | Trong bài dùng gì | Ghi chú |
|---|---|---|---|
| nguồn kích hoạt | pipeline source | `CI_PIPELINE_SOURCE` | Sáu giá trị hay gặp, xem §6.1 |
| điều kiện chạy | rule | `rules` | Danh sách, xét theo thứ tự |
| cổng pipeline | workflow rules | `workflow` | Tầng lọc trên `rules` |
| thời điểm đánh giá | evaluation time | tiếng Việt | Khái niệm trung tâm của buổi |
| khớp đầu tiên thắng | first-match-wins | tiếng Việt | Quy tắc xét `rules` |
| bảng chân trị | truth table | tiếng Việt | Công cụ chính, thay cho đoán |
| pipeline trùng | duplicate pipeline | tiếng Việt | Hai pipeline cho một commit |
| bị bỏ qua | skipped | `skipped` | Trạng thái, **khác** biến mất |
| thủ công | manual | `manual` | Job chờ người bấm |
| cho phép hỏng | allow failure | `allow_failure` | Đổi màu pipeline, không đổi việc chạy |
| mốc so sánh | compare base | tiếng Việt | `changes` cần nó |
| tệp thay đổi | changed files | tiếng Việt | Tập tệp `changes` xét |
| phụ thuộc tuỳ chọn | optional dependency | `needs:optional` | Đổi ô của bảng hai thuộc tính |



Mọi câu hỏi khó về `rules` quy về một câu hỏi dễ: **"cái này quyết định ở `t0` hay sau `t0`?"**

`t0` là thời điểm GitLab nhận sự kiện — push, mở MR, tạo tag, tới giờ lịch, gọi API — và **dựng danh sách job**. Tại `t0`, GitLab biết: nhánh nào, commit nào, nguồn kích hoạt gì, biến project/group/instance là gì, và tệp nào thay đổi. Nó **không** biết: job nào sẽ đỏ, biến nào sẽ được sinh ra, ai sẽ bấm nút manual.

Giá trị thực dụng: mọi thứ `rules` **không thể** làm đều nằm ở cột thứ hai. Khi ai đó hỏi "làm sao cho job này chạy nếu job kia sinh ra biến X", câu trả lời là *"không được — X sinh sau `t0`"*, và câu trả lời tiếp theo là pipeline động (buổi 09).

Mô hình này quay lại ở buổi 09, 12, 22.

### 3.3. Mô hình tư duy 2: bảng chân trị, không đoán

`rules` có vẻ nhiều biến thể, nhưng thực ra chỉ có hai chiều: **nguồn kích hoạt** (khoảng sáu giá trị hay gặp) và **điều kiện ta viết**. Sáu nhân năm là ba mươi ô — một bảng điền được trong một buổi lab.

Giá trị thực dụng: khi có bảng, câu hỏi "sao job này không chạy" trả lời trong 10 giây bằng cách tra ô. Không có bảng thì mỗi lần lại là một vòng thử sai 4 phút.

Đây là bảng cần nhất của giai đoạn 1, và bài lab bước 1 dành trọn để đo nó bằng **kích hoạt thật**, không bằng đọc tài liệu.

### 3.4. Mô hình tư duy 3: ba trạng thái "không chạy"

"Job không chạy" là ba tình huống khác nhau, và chúng khác nhau ở hai điều: **có xuất hiện trong pipeline không**, và **có chặn job sau không**.

| Trạng thái | Có trong danh sách job | Bấm chạy được | Chặn job sau |
|---|---|---|---|
| **Không có mặt** — `rules` không khớp | **Không** | Không | **Không** |
| **`manual`** | Có | **Có** | Tuỳ `allow_failure` |
| **`skipped`** — job trước đỏ | Có | Không | Có |

Một câu hỏi phân biệt cả ba: *"nó có trong danh sách job không?"* Không có → `rules`. Có mà chờ người bấm → `manual`. Có mà xám → `skipped`.

Mô hình này quay lại ở buổi 07 (gỡ rối), 12 (MR pipeline), 36 (environment và phê duyệt).

---

### 1.1. Thời điểm đánh giá: pipeline chốt lúc tạo (9 phút)

### 4.1. Một lần, ở `t0`

**Nguyên lý cốt lõi:** `rules` được đánh giá **đúng một lần, lúc pipeline được tạo**. Danh sách job chốt tại đó và không gì đổi được nó sau đó.

**Giải thích cơ chế ngầm:** GitLab dựng pipeline như một **đối tượng tĩnh**: nó phân giải tệp, đánh giá `workflow`, đánh giá `rules` của từng job, rồi ghi vào cơ sở dữ liệu một danh sách job cố định cùng quan hệ giữa chúng. Runner sau đó chỉ lấy job từ danh sách ấy. Không có bước nào đánh giá lại `rules`.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ba dấu hiệu, đều là cùng một hiểu nhầm:

1. Sửa một biến ở giao diện project rồi bấm **retry** một job — job vẫn chạy như cũ, vì `rules` của nó đã được đánh giá xong từ lâu.
2. Bấm **retry cả pipeline** và mong job đã biến mất xuất hiện lại — nó không xuất hiện; phải tạo **pipeline mới**.
3. Sửa `.gitlab-ci.yml` rồi retry pipeline cũ — pipeline cũ vẫn dùng tệp của commit cũ.

**Minh hoạ.**

```yaml
# Job này chạy hay không được quyết định ở t0 và không đổi được nữa
chi-chay-tren-nhanh-chinh:
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script: [echo "chay tren nhanh chinh"]
```

```bash
# Bằng chứng: đọc danh sách job của một pipeline đã tạo.
# Danh sách này KHÔNG đổi dù có retry bao nhiêu lần.
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?per_page=100" \
| jq -r '.[] | "\(.name)\t\(.status)"'
```

**Con số cần nhớ: 1 lần đánh giá, tại `t0`.** Muốn đổi danh sách job thì phải tạo pipeline mới — retry không đủ.

### 4.2. Hệ quả: `dotenv` tới quá muộn

**Nguyên lý cốt lõi:** Hệ quả trực tiếp: biến do job khác sinh ra qua `artifacts:reports:dotenv` **không dùng được** trong `rules` — lúc `rules` chạy thì job kia còn chưa tồn tại.

**Giải thích cơ chế ngầm:** Buổi 01 QT 5.4 nói `dotenv` là **cơ chế duy nhất** truyền một giá trị từ job này sang job sau. Nhưng cơ chế ấy hoạt động ở `t1..tn`, tức **sau** `t0`. `rules` chạy ở `t0`. Không có cách nào để một thứ sinh sau `t0` ảnh hưởng một quyết định đã ra ở `t0`.

Chỉ **hai** loại biến dùng được trong `rules`:

| Dùng được | Ví dụ |
|---|---|
| Biến hệ thống của GitLab | `$CI_COMMIT_BRANCH`, `$CI_PIPELINE_SOURCE`, `$CI_COMMIT_TAG`, `$CI_MERGE_REQUEST_TARGET_BRANCH_NAME` |
| Biến khai **trước** `t0` | Biến instance/group/project, `variables:` trong tệp, biến nhập tay khi chạy pipeline thủ công |

| **Không** dùng được | Vì sao |
|---|---|
| Biến từ `artifacts:reports:dotenv` | Sinh sau `t0` |
| Kết quả của một job | Sinh sau `t0` |
| Nội dung một tệp trong repo | GitLab không đọc tệp lúc đánh giá `rules` (trừ `rules:exists`) |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> `rules:if: '$PHIEN_BAN =~ /^v/'` **luôn** không khớp, dù job trước rõ ràng đã sinh `PHIEN_BAN` và log của nó in ra giá trị đúng. Job biến mất khỏi pipeline **im lặng** — và đây là ô nguy hiểm nhất của bảng hai thuộc tính.

**Minh hoạ.**

```yaml
# SAI — PHIEN_BAN chưa tồn tại ở t0, rule không bao giờ khớp
tinh-phien-ban:
  script:
    - echo "PHIEN_BAN=v1.2.3" > bien.env
  artifacts:
    reports:
      dotenv: bien.env

deploy-sai:
  needs: [tinh-phien-ban]
  rules:
    - if: '$PHIEN_BAN =~ /^v/'      # LUÔN không khớp → job BIẾN MẤT
  script: [echo "deploy $PHIEN_BAN"]

# ĐÚNG — dùng biến có sẵn ở t0 để quyết định chạy hay không,
# rồi dùng biến dotenv BÊN TRONG script
deploy-dung:
  needs: [tinh-phien-ban]
  rules:
    - if: $CI_COMMIT_TAG            # biến hệ thống, có ở t0
  script:
    - test -n "$PHIEN_BAN" || { echo "PHIEN_BAN rong"; exit 1; }
    - echo "deploy $PHIEN_BAN"
```

**Con số cần nhớ: chỉ 2 loại biến dùng được trong `rules`.** Nếu cần quyết định dựa trên thứ sinh lúc chạy, câu trả lời là **pipeline động** — buổi 09.

### 4.3. Không job nào thì không có pipeline

**Nguyên lý cốt lõi:** Pipeline không còn job nào sau khi lọc `rules` thì **không được tạo**, và GitLab báo bằng một thông báo dễ bị bỏ qua.

**Giải thích cơ chế ngầm:** GitLab không tạo pipeline rỗng. Nếu mọi job đều bị `rules` loại, kết quả là **không có gì** — không có pipeline để mở, không có log để đọc.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Push code lên và **không thấy pipeline nào xuất hiện**. Người mới thường nghĩ GitLab hỏng hoặc runner chết. Thông báo thật nằm ở API hoặc ở một dòng nhỏ trong giao diện, dạng *"No stages / jobs for this pipeline"* hoặc `filtered out by workflow rules`.

Ô của bảng hai thuộc tính: **im lặng, có chặn** — không có gì chạy, và cũng không có gì báo rõ ràng.

**Minh hoạ.**

```bash
# Chẩn đoán: dùng ci/lint để xem tệp có sinh ra job nào không,
# rồi hỏi API xem commit này có pipeline không
curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "$(jq -Rs '{content: ., ref: "main"}' < .gitlab-ci.yml)" \
  "$GITLAB/api/v4/projects/$PID/ci/lint" \
| jq -r '"valid=\(.valid)  so_job=\(.jobs | length)"'

# Nếu so_job = 0 thì không có pipeline nào được tạo, và đó là lý do
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/repository/commits/$SHA" | jq -r '.last_pipeline // "KHONG CO PIPELINE"'
```

**Con số cần nhớ: 0 job → 0 pipeline.**

---

### 1.2. `workflow`: pipeline có được tạo không (8 phút)

### 5.1. Hai tầng lọc độc lập

**Nguyên lý cốt lõi:** `workflow:rules` chặn ở tầng **pipeline**; `rules` của job chặn ở tầng **job**. Hai tầng độc lập và **cả hai** phải cho qua.

**Giải thích cơ chế ngầm:** GitLab đánh giá `workflow` **trước**: nếu nó không cho qua thì không có pipeline nào được tạo, và `rules` của các job không được đánh giá lần nào. Nếu `workflow` cho qua thì mới tới lượt `rules` của từng job lọc tiếp.

| Tầng | Từ khoá | Quyết định | Hỏng thì |
|---|---|---|---|
| 1 | `workflow:rules` | **Cả pipeline** có được tạo không | Không có pipeline — im lặng |
| 2 | `rules` của job | **Từng job** có mặt không | Job biến mất — im lặng |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Sửa `rules` của một job mãi mà nó không chạy — vì `workflow` đã chặn cả pipeline từ trước. Cách kiểm trong 5 giây: **có pipeline nào được tạo không?** Không có → vấn đề ở tầng 1, sửa `rules` của job là vô ích.

**Minh hoạ.**

```yaml
workflow:
  rules:
    # Tầng 1: chỉ tạo pipeline cho MR, nhánh chính, và tag
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG
    - when: never                    # mọi ca khác: KHÔNG tạo pipeline

test:
  rules:
    # Tầng 2: trong số pipeline đã được tạo, job này chỉ chạy ở MR
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  script: [echo "test"]
```

**Con số cần nhớ: 2 tầng lọc, `workflow` đánh giá trước.**

### 5.2. Pipeline trùng, và nó tốn bao nhiêu

**Nguyên lý cốt lõi:** Không có `workflow`, một merge request mở trên nhánh đang được push sẽ sinh **hai** pipeline cho cùng một commit: một `push`, một `merge_request_event`.

**Giải thích cơ chế ngầm:** Hai sự kiện khác nhau cùng xảy ra: git nhận một push (nguồn `push`), và merge request thấy nhánh nguồn đổi (nguồn `merge_request_event`). Nếu không có gì loại bớt, GitLab tạo pipeline cho **cả hai**. Cả hai chạy cùng tập job, trên cùng commit, cho cùng kết quả.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Mở tab Pipelines và thấy hai dòng liền nhau cùng một SHA ngắn. Hoặc đo bằng số:

```bash
# Đếm pipeline theo commit trong 20 commit gần nhất
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines?per_page=100" \
| jq -r 'group_by(.sha) | map({sha: .[0].sha[0:8], so_pipeline: length})
         | map(select(.so_pipeline > 1)) | .[] | "\(.sha)\t\(.so_pipeline)"'
```

Ô của bảng hai thuộc tính: **im lặng, không chặn** — mọi thứ xanh, chỉ là tốn gấp đôi.

**Minh hoạ.** `workflow` chuẩn của khoá này, dùng lại ở mọi buổi sau:

```yaml
workflow:
  rules:
    # 1. Pipeline của merge request
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    # 2. Bỏ pipeline push khi nhánh đó ĐANG có merge request mở
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    # 3. Nhánh chính luôn chạy
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    # 4. Tag luôn chạy
    - if: $CI_COMMIT_TAG
    # 5. Nhánh khác chưa có MR: vẫn chạy
    - if: $CI_COMMIT_BRANCH
```

Điểm cần chú ý ở đoạn trên: **thứ tự quyết định kết quả** — quy tắc 2 phải nằm **sau** quy tắc 1, nếu không thì pipeline MR cũng bị chặn. Đây chính là QT 6.1.

**Con số cần nhớ, và giới hạn.** **2 pipeline cho 1 commit** — gấp đôi phút runner. Con số này **không phổ quát**: nó chỉ đúng khi không có `workflow` **và** nhánh đó đang có MR mở **và** nhánh vẫn còn được push. Bài lab đo con số thật trên repo lab.

---

### 1.3. `rules`: bốn loại điều kiện, dừng ở khớp đầu tiên (11 phút)

### 6.1. Khớp đầu tiên thắng

**Nguyên lý cốt lõi:** `rules` dừng ở **điều kiện khớp đầu tiên** và dùng `when` của điều kiện đó; các điều kiện sau **không** được xét. Thứ tự quyết định kết quả.

**Giải thích cơ chế ngầm:** `rules` là một **danh sách có thứ tự**, không phải một tập hợp điều kiện. GitLab duyệt từ trên xuống, gặp điều kiện đầu tiên đúng thì lấy `when` (mặc định `on_success`), `allow_failure`, `variables` của điều kiện đó rồi **dừng**. Nếu duyệt hết mà không điều kiện nào đúng thì job **không được thêm vào pipeline** (QT 6.2).

Bốn loại điều kiện, và chúng kết hợp được trong một mục:

| Loại | Cú pháp | Xét cái gì |
|---|---|---|
| `if` | `- if: $CI_COMMIT_BRANCH == "main"` | Biểu thức trên biến có ở `t0` |
| `changes` | `- changes: [src/**/*]` | Tệp nào thay đổi so với **mốc so sánh** |
| `exists` | `- exists: [Dockerfile]` | Tệp có tồn tại trong repo không |
| `when` | `- when: manual` | Không phải điều kiện — nó là **kết quả** |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đảo thứ tự hai rule làm job đổi hành vi mà không ai sửa điều kiện nào. Ca kinh điển: viết rule **chung** trước rule **riêng**, và rule riêng không bao giờ được xét.

**Minh hoạ.**

```yaml
# SAI — rule chung nằm trước, rule manual KHÔNG BAO GIỜ được xét
deploy-sai:
  rules:
    - if: $CI_COMMIT_BRANCH                    # khớp với MỌI nhánh, kể cả main
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual                              # không bao giờ tới đây

# ĐÚNG — riêng trước, chung sau
deploy-dung:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
    - if: $CI_COMMIT_BRANCH
```

Kiểm bằng `ci/lint` thay vì đoán — buổi 03 QT 4.3 áp vào đây:

```bash
lint | jq -r '.jobs[] | select(.name=="deploy-dung") | {name, when, rules}'
```

**Con số cần nhớ: 1 rule khớp là dừng.** Quy tắc thực hành: **viết điều kiện riêng trước, điều kiện chung sau** — giống thứ tự trong một khối `case`.

### 6.2. Không khớp thì biến mất, không phải `skipped`

**Nguyên lý cốt lõi:** Không rule nào khớp → job **không được thêm vào pipeline**. Nó **biến mất**, không phải `skipped`.

**Giải thích cơ chế ngầm:** `skipped` là một **trạng thái** của một job **đang có trong pipeline** — nó có id, có trang riêng, và nó chặn job sau. Job bị `rules` loại thì không được tạo ra: nó không có id, không có trang, và **không chặn gì cả**.

Phân biệt này quan trọng vì nó quyết định hệ quả lên job phụ thuộc, và đó là §7.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hỏi "job đó ở đâu, sao tôi không thấy nó xám" — vì nó không xám, nó không có ở đó. Cách kiểm: đếm số job của pipeline và so với số job trong tệp.

**Minh hoạ.**

```yaml
# Ba cách viết cho CÙNG một kết quả: job không có mặt
khong-khop-rule-nao:
  rules:
    - if: $BIEN_KHONG_BAO_GIO_DUNG == "x"
  script: [echo "khong bao gio chay"]

when-never-tuong-minh:
  rules:
    - if: $CI_COMMIT_BRANCH
      when: never
  script: [echo "khong bao gio chay"]
```

```bash
# Bằng chứng: hai job trên KHÔNG có trong danh sách job của pipeline
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs" | jq -r '.[].name'
```

**Con số cần nhớ:** `when: never` và "không khớp rule nào" cho **cùng** kết quả — nên rule cuối dạng `- when: never` thường là thừa.

**Đây là chế độ hỏng im lặng quan trọng nhất của buổi.** Nếu job biến mất là một job **gate security**, thì gate ấy biến mất **im lặng và không chặn gì** — pipeline xanh, không có cảnh báo, và không ai biết bước quét đã không chạy. Buổi 35 xử lý cách chống, và cách chống dựa trên buổi 01 QT 7.3: một job riêng **khẳng định** rằng các gate đã có mặt.

### 6.3. `changes` cần mốc so sánh, và mốc đó âm thầm sai

**Nguyên lý cốt lõi:** `rules:changes` cần một **mốc so sánh**, và mốc mặc định âm thầm sai ở ba ca: nhánh mới, pipeline theo lịch, và push nhiều commit một lần.

**Giải thích cơ chế ngầm:** `changes` trả lời câu "tệp nào đã đổi", và câu ấy chỉ có nghĩa khi có **hai** điểm để so. Với pipeline merge request, GitLab so với nhánh đích — đúng. Với pipeline nhánh, nó so với **commit trước đó trên cùng nhánh** — và ba ca dưới đây làm phép so ấy sai:

| Ca | Chuyện gì xảy ra | Hệ quả |
|---|---|---|
| **Nhánh mới tạo** | Không có commit trước trên nhánh này | GitLab coi **mọi tệp đều đổi** → job chạy hết, kể cả job không cần |
| **Pipeline theo lịch** | Không có commit mới nào | Không tệp nào "đổi" → job `changes` **không chạy lần nào** |
| **Push nhiều commit một lần** | So với commit trước push, không phải từng commit | Đúng về tổng thể nhưng sai nếu ta muốn xét từng commit |

Ô của bảng hai thuộc tính: **im lặng, không chặn** ở cả ba ca — job chạy thừa hoặc không chạy, và không có gì báo.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job build của một service trong monorepo chạy trên mọi nhánh mới dù không ai đụng service đó. Hoặc ngược lại: pipeline theo lịch hằng đêm không chạy job nào.

**Minh hoạ.**

```yaml
# Sửa được 2 trong 3 ca bằng compare_to
build-service-a:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes: [services/a/**/*]
    # Với pipeline nhánh, chỉ định rõ mốc so sánh
    - if: $CI_COMMIT_BRANCH
      changes:
        paths: [services/a/**/*]
        compare_to: refs/heads/main
    # Pipeline theo lịch: KHÔNG dùng changes, chạy đầy đủ
    - if: $CI_PIPELINE_SOURCE == "schedule"
  script: [echo "build service a"]
```

**Con số cần nhớ: 3 ca sai; `compare_to` sửa được 2**, ca thứ ba — muốn xét từng commit riêng — cần pipeline động, và buổi 22 giải đầy đủ.

**Kết luận thực hành quan trọng:** **đừng dùng `rules:changes` cho job security.** Một gate chạy thừa chỉ tốn vài chục giây; một gate biến mất im lặng thì không ai biết. Đây là một trong hai mục "khi nào KHÔNG nên dùng" ở §8.

### 6.4. `rules` và `only` loại trừ nhau

**Nguyên lý cốt lõi:** `rules` và `only`/`except` **không dùng chung được trong một job**. GitLab báo lỗi ở tầng tạo pipeline.

**Giải thích cơ chế ngầm:** `only`/`except` là cú pháp cũ với mô hình đánh giá khác; `rules` thay thế nó. Cho phép dùng chung sẽ tạo ra hành vi mơ hồ, nên GitLab từ chối thẳng.

Ô của bảng hai thuộc tính: **ồn ào, có chặn** — đây là một trong ít ca GitLab báo lỗi rõ ràng, và bài lab đưa nó vào để học viên thấy **đối chứng** với ba ca im lặng còn lại.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline không được tạo, thông báo dạng `jobs:<ten> config key may not be used with 'rules': only`.

**Minh hoạ.**

```yaml
# SAI — GitLab từ chối tạo pipeline
job-sai:
  only: [main]
  rules:
    - if: $CI_COMMIT_TAG
  script: [echo x]

# ĐÚNG — chuyển hết sang rules
job-dung:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG
  script: [echo x]
```

Quy tắc thực hành của khoá: **dùng `rules`, không dùng `only`/`except`** — kể cả khi repo cũ đang dùng. Chuyển dần từng job, và kiểm bằng `ci/lint`.

---

### 1.4. Ba trạng thái "không chạy" và hệ quả (6 phút)

### 7.1. Ba trạng thái, một câu hỏi phân biệt

Đây là câu trả lời cho BTVN 4 câu 1 của buổi 03.

**Nguyên lý cốt lõi:** Có **ba** trạng thái "job không chạy", khác nhau ở hai điều: có xuất hiện trong pipeline không, và có chặn job sau không.

| Trạng thái | Nguyên nhân | Có trong pipeline | Bấm chạy được | Chặn job sau | Ô của bảng hai thuộc tính |
|---|---|---|---|---|---|
| **Không có mặt** | `rules` không khớp | **Không** | Không | **Không** | Im lặng, không chặn |
| **`manual`** | `when: manual` | Có | **Có** | Tuỳ `allow_failure` | Ồn ào, tuỳ |
| **`skipped`** | Job trước đỏ | Có | Không | Có | Ồn ào, có chặn |

**Giải thích cơ chế ngầm:** Ba trạng thái khác nhau về hệ quả vì lý do sau: Hàng rào stage của buổi 03 QT 5.3 vẫn còn nguyên khi một job biến mất — nó chỉ bớt đi một job phải chờ. Nhưng `skipped` thì khác: nó là một job **đang có** ở trạng thái không thành công, nên nó chặn theo quy tắc thông thường.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Câu hỏi "sao job đó không xám" — vì nó không xám, nó không có ở đó. Câu hỏi phân biệt duy nhất cần hỏi: ***"nó có trong danh sách job không?"***

**Minh hoạ.**

```bash
# Ba trạng thái nhìn từ API
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?per_page=100" \
| jq -r '.[] | "\(.name)\t\(.status)\tallow_failure=\(.allow_failure)"'
# Job "không có mặt" KHÔNG xuất hiện trong kết quả này — đó chính là bằng chứng
```

**Con số cần nhớ: 3 trạng thái, 1 câu hỏi phân biệt.**

### 7.2. `manual` có hai mặc định khác nhau

**Nguyên lý cốt lõi:** `when: manual` mặc định có `allow_failure: true` **khi ở trong `rules`**, và mặc định `false` khi khai trực tiếp. Đây là chỗ hành vi khác nhau giữa hai cách viết.

**Giải thích cơ chế ngầm:** Hai cú pháp có lịch sử khác nhau. Khi `when: manual` nằm trong một mục `rules`, GitLab coi nó là "một lựa chọn, không bắt buộc" nên mặc định cho phép bỏ qua. Khi khai trực tiếp ở cấp job, nó giữ ngữ nghĩa cũ: job này là một bước bắt buộc, chờ người bấm.

Hệ quả thực tế: cùng một job "deploy thủ công", hai cách viết cho hai kết quả khác nhau về **màu pipeline** khi không ai bấm.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline hiển thị **blocked** thay vì **success** khi không ai bấm nút deploy — hoặc ngược lại, pipeline xanh dù bước deploy chưa chạy. Cả hai đều là hệ quả của mặc định mà không ai để ý.

**Minh hoạ.**

```yaml
# Cách 1 — manual trong rules
deploy-trong-rules:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  script: [echo "deploy"]

# Cách 2 — manual khai trực tiếp
deploy-truc-tiep:
  when: manual
  script: [echo "deploy"]
```

```bash
# ĐO, không tra: đọc trường allow_failure của hai job
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs" \
| jq -r '.[] | select(.name | startswith("deploy-")) | "\(.name)\tallow_failure=\(.allow_failure)"'
```

**Con số cần nhớ: 2 cách viết, 2 giá trị mặc định.** Đây là **đại lượng loại (c)** — hành vi đã đổi giữa các phiên bản, nên bài lab bước 4 đo trực tiếp và ghi kèm phiên bản GitLab. Quy tắc thực hành: **luôn khai `allow_failure` tường minh** cho job manual, đừng dựa vào mặc định.

### 7.3. `needs` trỏ vào job không có mặt

**Nguyên lý cốt lõi:** Job có `needs` trỏ tới một job **không có mặt** trong pipeline gây lỗi ở tầng tạo pipeline; `needs:optional: true` làm nó im lặng bỏ qua.

**Giải thích cơ chế ngầm:** `needs` khai báo một phụ thuộc cứng. Nếu job được trỏ tới đã bị `rules` loại, GitLab không dựng được đồ thị phụ thuộc và từ chối tạo pipeline. Cờ `optional: true` nói với GitLab: "nếu job kia không có thì bỏ qua ràng buộc này".

Đây là ca hiếm mà **một cờ đổi ô của bảng hai thuộc tính**:

| Cấu hình | Ô |
|---|---|
| `needs: [job-a]` khi `job-a` không có mặt | **Ồn ào, có chặn** — pipeline không tạo được, lỗi rõ ràng |
| `needs: [{job: job-a, optional: true}]` | **Im lặng, không chặn** — job chạy mà không có artifact của `job-a` |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Với `optional: true`: job chạy nhưng thiếu artifact, và vì shell không báo lỗi khi tệp thiếu ở nhiều ca, job có thể **vẫn xanh** với hiện vật rỗng — đúng ca hỏng của buổi 01 QT 7.2.

**Minh hoạ.**

```yaml
build-chi-tren-tag:
  rules:
    - if: $CI_COMMIT_TAG
  script: [mkdir -p dist && echo x > dist/app.js]
  artifacts: {paths: [dist/]}

# Không có optional: trên nhánh thường, pipeline KHÔNG TẠO ĐƯỢC — ồn ào
dong-goi-cung:
  needs: [build-chi-tren-tag]
  script: [ls dist/]

# Có optional: pipeline tạo được, nhưng job chạy mà không có dist/ — im lặng
dong-goi-mem:
  needs:
    - job: build-chi-tren-tag
      optional: true
  script:
    # BẮT BUỘC có khẳng định khi dùng optional — buổi 01 QT 7.3
    - test -s dist/app.js || { echo "KHANG DINH HONG: thieu artifact cua build"; exit 1; }
    - ls dist/
```

**Con số cần nhớ: 1 cờ `optional` đổi ô của bảng hai thuộc tính.** Quy tắc: chỉ dùng `optional: true` khi đã có **khẳng định** riêng kiểm hiện vật.

---

### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước

**Việc 1 — 10 phút, rủi ro bằng 0.** Đếm pipeline trùng: với 20 commit gần nhất, có bao nhiêu commit có **hơn một** pipeline?

```bash
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines?per_page=100" \
| jq -r 'group_by(.sha) | map(select(length > 1)) | length as $n
         | "\($n) commit có pipeline trùng"'
```

**Việc 2 — 30 phút, rủi ro bằng 0.** Lập **bảng chân trị** cho repo mình: sáu nguồn kích hoạt × job quan trọng nhất. Điền bằng đo, không bằng đoán.

**Việc 3 — 20 phút, rủi ro bằng 0, và là việc quan trọng nhất về mặt an toàn.** Kiểm mọi job **security/gate**: `rules` của nó có ca nào làm nó **biến mất** không? Đặc biệt tìm `rules:changes` trong các job ấy — theo QT 6.3, nó âm thầm sai ở ba ca.

### Cái gì hỏng nếu áp thẳng lên prod

Thêm `workflow` chặn pipeline `push` khi có MR sẽ làm **mất** pipeline trên nhánh chính nếu viết thiếu ca `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`. Hậu quả: merge vào main mà không có pipeline nào chạy — và không có gì báo, vì "không có pipeline" là ô im lặng.

Cách áp an toàn: đặt `workflow` trên nhánh riêng, rồi **kiểm đủ sáu nguồn kích hoạt** trước khi merge — push nhánh thường, push nhánh chính, mở MR, đẩy tag, chạy lịch, gọi API. Bảng chân trị ở việc 2 chính là danh sách kiểm ấy.

### Đo trước — đo sau

| Chỉ số | Đo bằng | Vì sao |
|---|---|---|
| Số pipeline / số commit trong 7 ngày | API `pipelines`, nhóm theo `sha` | Tỉ số > 1 là bằng chứng có pipeline trùng |
| Tổng phút runner 7 ngày | Cộng `duration` mọi job | Con số quy ra tiền được ở buổi 46 |
| Số job gate có `rules` chứa ca biến mất | Đọc `ci/lint`, lọc job có `rules:changes` | Đây là số gate đang có nguy cơ biến mất im lặng |

### Khi nào KHÔNG nên dùng

**Đừng dùng `rules:changes` cho job security.** QT 6.3 nói nó âm thầm sai ở ba ca, và hậu quả không đối xứng: một gate chạy thừa tốn vài chục giây; một gate **biến mất im lặng** thì không ai biết bước quét đã không chạy, và pipeline vẫn xanh. Với job security, chấp nhận chạy thừa.

**Đừng dùng `needs:optional: true` để "cho tiện".** Nó đổi ô của bảng hai thuộc tính từ **ồn ào có chặn** sang **im lặng không chặn** — tức từ ô rẻ nhất sang ô đắt nhất. Chỉ dùng khi job tiêu thụ đã có **khẳng định** riêng kiểm hiện vật, theo buổi 01 QT 7.3.

**Đừng viết `workflow` phức tạp hơn năm quy tắc.** Mỗi quy tắc thêm vào là một ô mới trong bảng chân trị phải kiểm. `workflow` chuẩn ở §5.2 có năm quy tắc và phủ đủ sáu nguồn kích hoạt; nhiều hơn thế thì thường là dấu hiệu cần chuyển sang pipeline động (buổi 09) thay vì nhồi thêm điều kiện.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy | Vì sao dính | Làm đúng là |
|---|---|---|---|
| 1 | Tưởng `rules` được đánh giá lại khi retry | Trực giác nói "chạy lại thì tính lại" | **1 lần** ở `t0`; muốn đổi thì tạo pipeline mới (QT 4.1) |
| 2 | Dùng biến `dotenv` trong `rules` | Nó là biến, trông như dùng được | Nó sinh sau `t0` — quá muộn (QT 4.2). Dùng biến hệ thống |
| 3 | Nghĩ job không khớp rule là `skipped` | Cả hai đều "không chạy" | Nó **biến mất** — không có id, không chặn gì (QT 6.2, 7.1) |
| 4 | Viết rule chung trước rule riêng | Đọc từ tổng quát tới cụ thể | Dừng ở khớp đầu tiên (QT 6.1). Riêng trước, chung sau |
| 5 | Không có `workflow` | Không biết pipeline trùng tồn tại | **2** pipeline cho **1** commit (QT 5.2) |
| 6 | `workflow` chặn cả nhánh chính | Viết thiếu một ca | Phải có `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH` |
| 7 | `rules:changes` cho job security | Muốn tiết kiệm thời gian | Sai ở 3 ca; gate biến mất im lặng (QT 6.3) |
| 8 | Quên `changes:compare_to` | Mặc định trông có vẻ hợp lý | Mốc mặc định sai ở nhánh mới (QT 6.3) |
| 9 | Dùng chung `rules` với `only` | Chuyển đổi dở dang | GitLab báo lỗi (QT 6.4). Chuyển hết sang `rules` |
| 10 | Tưởng `allow_failure` của `manual` luôn giống nhau | Cùng chữ `manual` | **2** cách viết, **2** mặc định (QT 7.2). Khai tường minh |
| 11 | `needs:optional: true` cho tiện | Nó làm hết lỗi ngay | Nó đổi ô bảng hai thuộc tính (QT 7.3). Phải có khẳng định kèm |
| 12 | Push xong không thấy pipeline, nghĩ GitLab hỏng | Không có gì để mở | **0** job → **0** pipeline (QT 4.3). Kiểm bằng `ci/lint` |
| 13 | Đoán `CI_PIPELINE_SOURCE` nhận giá trị gì | Tài liệu dài | Lập **bảng chân trị** bằng kích hoạt thật (lab bước 1) |
| 14 | Thêm `- when: never` ở cuối để "tắt" job | Trông tường minh hơn | Không khớp rule nào đã đủ (QT 6.2); dòng đó thường thừa |

---

### 1.7. Tóm tắt

```mermaid
graph TD
    LD["LUẬN ĐỀ: rules đánh giá ĐÚNG MỘT LẦN ở t0<br/>danh sách job chốt tại đó"]

    LD --> A["§4 THỜI ĐIỂM<br/>QT 4.1 một lần, ở t0<br/>QT 4.2 dotenv tới QUÁ MUỘN<br/>QT 4.3 0 job → 0 pipeline"]
    LD --> B["§5 WORKFLOW<br/>QT 5.1 hai tầng lọc độc lập<br/>QT 5.2 pipeline trùng = gấp đôi phút runner"]
    LD --> C["§6 RULES<br/>QT 6.1 dừng ở KHỚP ĐẦU TIÊN<br/>QT 6.2 không khớp → BIẾN MẤT<br/>QT 6.3 changes sai ở BA ca<br/>QT 6.4 rules và only loại trừ nhau"]
    LD --> D["§7 BA TRẠNG THÁI<br/>QT 7.1 không có mặt / manual / skipped<br/>QT 7.2 manual có HAI mặc định<br/>QT 7.3 needs:optional đổi ô"]

    C --> KQ["CHẾ ĐỘ HỎNG NGUY HIỂM NHẤT:<br/>job GATE biến mất im lặng<br/>pipeline xanh, không ai biết quét đã không chạy"]
    D --> KQ
    KQ --> VT["§8 ĐƯA VÀO VIỆC THẬT<br/>đếm pipeline trùng · lập bảng chân trị<br/>kiểm rules của MỌI job gate"]

    A -.dùng lại.-> B09["buổi 09 pipeline động · 12 MR · 22 monorepo"]
    B -.dùng lại.-> B12["buổi 12 merge train · 44 template"]
    C -.dùng lại.-> B22["buổi 22 monorepo (giải đầy đủ changes) · 35 gate"]
    D -.dùng lại.-> B36["buổi 07 gỡ rối · 36 environment · 43 canary"]
```

**Năm điều phải nhớ sau buổi học:**

1. **`rules` đánh giá một lần, ở `t0`.** Retry không đánh giá lại; muốn đổi danh sách job phải tạo pipeline mới.
2. **Biến `dotenv` không dùng được trong `rules`** — nó sinh sau `t0`. Chỉ biến hệ thống và biến khai trước `t0` dùng được.
3. **`rules` dừng ở khớp đầu tiên.** Riêng trước, chung sau.
4. **Không khớp rule nào → job BIẾN MẤT**, không phải `skipped`. Và nếu đó là gate security thì gate biến mất im lặng.
5. **Không có `workflow` → 2 pipeline cho 1 commit.** Gấp đôi phút runner, và mọi thứ vẫn xanh.

---

### 1.8. Câu hỏi tự kiểm tra

1. `rules` được đánh giá lúc nào? Nêu **hai** hệ quả của câu trả lời đó.
2. Job A sinh `PHIEN_BAN` qua `dotenv`. Job B có `rules:if: '$PHIEN_BAN =~ /^v/'`. Job B chạy không? Vì sao?
3. Kể **hai** loại biến dùng được trong `rules` và **ba** thứ không dùng được.
4. Push code lên nhưng không thấy pipeline nào. Nêu hai giả thuyết và cách phân biệt.
5. `workflow:rules` khác `rules` của job ở chỗ nào? Cái nào được đánh giá trước?
6. Vì sao mở một MR lại sinh hai pipeline? Chặn ở đâu, và bằng quy tắc nào?
7. Trong `workflow` chuẩn ở §5.2, vì sao quy tắc "bỏ pipeline push khi có MR" phải nằm **sau** quy tắc MR?
8. `rules` xét theo thứ tự nào? Điều gì xảy ra sau khi một điều kiện khớp?
9. Job không khớp rule nào — nó có trong danh sách job không? Nó có chặn job sau không?
10. Kể **ba** ca `rules:changes` âm thầm sai. `compare_to` sửa được mấy ca?
11. Kể ba trạng thái "job không chạy" và **một câu hỏi** phân biệt cả ba.
12. `when: manual` viết trong `rules` và viết trực tiếp — khác nhau ở đâu?
13. `needs` trỏ tới job đã bị `rules` loại. Chuyện gì xảy ra? Thêm `optional: true` thì sao?
14. Vì sao không nên dùng `rules:changes` cho job security?
15. Repo có 40 commit/tuần và mỗi commit sinh 2 pipeline, mỗi pipeline 6 phút runner. Bỏ pipeline trùng tiết kiệm bao nhiêu phút runner một tháng?

### Đáp án

1. **Đúng một lần, lúc pipeline được tạo (`t0`).** Hệ quả 1: retry không đánh giá lại `rules`. Hệ quả 2: thứ sinh sau `t0` — biến `dotenv`, kết quả job — không dùng được trong `rules` (QT 4.1, 4.2).
2. **Không chạy** — job B **biến mất** khỏi pipeline. Ở `t0`, `PHIEN_BAN` chưa tồn tại nên biểu thức không khớp. Đây là ô im lặng + không chặn (QT 4.2, 6.2).
3. Dùng được: biến hệ thống của GitLab (`$CI_COMMIT_BRANCH`, `$CI_PIPELINE_SOURCE`, `$CI_COMMIT_TAG`…) và biến khai trước `t0` (instance/group/project, `variables:` trong tệp, biến nhập tay). Không dùng được: biến `dotenv`, kết quả của một job, nội dung tệp trong repo (trừ `rules:exists`).
4. Giả thuyết A: `workflow` chặn cả pipeline. Giả thuyết B: mọi job đều bị `rules` loại nên **0 job → 0 pipeline**. Phân biệt bằng `ci/lint`: nếu `.jobs | length == 0` thì là B; nếu có job mà vẫn không tạo pipeline thì là A (QT 4.3, 5.1).
5. `workflow` chặn ở tầng **pipeline** — không qua thì không có pipeline nào và `rules` của job không được đánh giá lần nào. `rules` chặn ở tầng **job**. `workflow` được đánh giá **trước** (QT 5.1).
6. Vì hai sự kiện cùng xảy ra: git nhận push (nguồn `push`) và MR thấy nhánh nguồn đổi (nguồn `merge_request_event`). Chặn bằng `workflow` với quy tắc `- if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS` kèm `when: never` (QT 5.2).
7. Vì `rules` **dừng ở khớp đầu tiên** (QT 6.1). Nếu quy tắc `when: never` nằm trước, nó cũng khớp với pipeline MR trong một số ca và sẽ chặn luôn cái ta muốn giữ.
8. Xét **theo thứ tự từ trên xuống**, dừng ở **điều kiện khớp đầu tiên**, lấy `when`/`allow_failure`/`variables` của điều kiện đó. Các điều kiện sau **không** được xét (QT 6.1).
9. **Không** có trong danh sách job — nó biến mất, không có id, không có trang riêng. Và nó **không chặn** job sau (QT 6.2, 7.1).
10. Ba ca: (a) **nhánh mới tạo** — không có commit trước nên GitLab coi mọi tệp đều đổi, job chạy hết; (b) **pipeline theo lịch** — không có commit mới nên không tệp nào "đổi", job không chạy lần nào; (c) **push nhiều commit một lần** — so với commit trước push chứ không xét từng commit. `compare_to` sửa được **2** ca đầu; ca thứ ba cần pipeline động, buổi 22 (QT 6.3).
11. **Không có mặt** (`rules` không khớp) · **`manual`** · **`skipped`** (job trước đỏ). Câu hỏi phân biệt: ***"nó có trong danh sách job không?"*** — không có → `rules`; có mà chờ bấm → `manual`; có mà xám → `skipped` (QT 7.1).
12. Khác ở **mặc định của `allow_failure`**: trong `rules` mặc định `true`, khai trực tiếp mặc định `false`. Hệ quả: pipeline hiển thị `blocked` hay `success` khi không ai bấm. Đây là hành vi **phải đo**, và quy tắc thực hành là **luôn khai `allow_failure` tường minh** (QT 7.2).
13. Không có `optional`: GitLab **không dựng được đồ thị phụ thuộc** và từ chối tạo pipeline — ồn ào, có chặn. Thêm `optional: true`: pipeline tạo được, job chạy nhưng **không có artifact** — im lặng, không chặn. Một cờ đổi ô của bảng hai thuộc tính (QT 7.3).
14. Vì hậu quả **không đối xứng**: gate chạy thừa tốn vài chục giây; gate **biến mất im lặng** thì không ai biết bước quét đã không chạy, và pipeline vẫn xanh. Cộng với việc `changes` âm thầm sai ở ba ca (QT 6.3), rủi ro không đáng đổi.
15. 40 commit/tuần × 1 pipeline thừa × 6 phút = 240 phút/tuần ≈ **960–1.000 phút runner một tháng** cho một repo. Buổi 46 quy con số này ra tiền.

---

## §12. Tài liệu tham khảo

| Nguồn | Loại | Phiên bản |
|---|---|---|
| GitLab Docs — *`rules`*, *`rules:if`*, *`rules:changes`*, *`rules:exists`* | (a) tài liệu chính thức | 17.7 |
| GitLab Docs — *`workflow`* và *`workflow:rules` templates* | (a) | 17.7 |
| GitLab Docs — *Predefined variables* (`CI_PIPELINE_SOURCE`, `CI_OPEN_MERGE_REQUESTS`…) | (a) | 17.7 |
| GitLab Docs — *`when`*, *`allow_failure`*, *`needs:optional`* | (a) | 17.7 |
| GitLab API — `POST /projects/:id/ci/lint`, `GET /projects/:id/pipelines` | (a) | v4 |
| Bảng chân trị 6 nguồn × rules; `allow_failure` mặc định của `manual`; hành vi `changes` ở nhánh mới | (c) **phải đo** | Lab bước 1, 3, 4 |
| Quy tắc "riêng trước, chung sau"; "đừng dùng `changes` cho job security" | (c) kinh nghiệm thực tế | — |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10' |
| §1 | Sau buổi này học viên làm được gì | 1' |
| §2 | Cần biết trước | 1' |
| §3 | Thuật ngữ và mô hình tư duy | 8' |
| §4 | Thời điểm đánh giá: pipeline chốt lúc tạo | 9' |
| §5 | `workflow`: pipeline có được tạo không | 8' |
| §6 | `rules`: bốn loại điều kiện, dừng ở khớp đầu tiên | 11' |
| §7 | Ba trạng thái "không chạy" và hệ quả | 6' |
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

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7.
> **Buổi này KHÔNG đụng `config.toml`** — nhẹ hơn buổi 02 và 03 về hạ tầng.

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| # | Mục tiêu | Tiêu chí hoàn thành (kiểm chứng được bằng lệnh) |
|---|---|---|
| TH1 | Kích hoạt được **sáu** nguồn pipeline khác nhau | `bang-chan-tri.tsv` có 6 dòng nguồn, mỗi dòng có `CI_PIPELINE_SOURCE` đo được |
| TH2 | **Đo QT 6.2** — job không khớp rule thì biến mất, không `skipped` | Job không xuất hiện trong `pipelines/:id/jobs` |
| TH3 | Điền đủ bảng chân trị 6 nguồn × 5 rule | 30 ô, mỗi ô `CO` hoặc `KHONG`, đo bằng API |
| TH4 | **Đo QT 5.2** — pipeline trùng khi mở MR | `pipeline-trung.tsv` ghi số pipeline cho cùng một SHA |
| TH5 | Kiểm chứng QT 5.1 — `workflow` bỏ được pipeline trùng | Sau khi thêm `workflow`, mỗi SHA có đúng **1** pipeline |
| TH6 | **Đo QT 6.1** — đảo thứ tự rule đổi hành vi | Cùng job, hai thứ tự, hai giá trị `when` khác nhau |
| TH7 | Kiểm chứng QT 6.4 — `rules` và `only` loại trừ nhau | `ci/lint` trả `valid: false` với thông báo cụ thể |
| TH8 | **Đo QT 6.3** — `changes` sai ở nhánh mới tạo | Job `changes` chạy dù không đụng thư mục nó theo dõi |
| TH9 | Kiểm chứng QT 7.1 — ba trạng thái "không chạy" | `ba-trang-thai.md` có bằng chứng API cho cả ba |
| TH10 | **Đo QT 7.2** — `allow_failure` mặc định của `manual` ở hai cách viết | Hai job, hai giá trị `allow_failure` đo được |
| TH11 | Kiểm chứng QT 4.1, 4.3 — retry không đánh giá lại; 0 job → 0 pipeline | Bằng chứng API cho cả hai |
| TH12 | Nộp hiện vật | `kiem-hien-vat.sh` in ĐẠT |

**Sản phẩm cuối buổi:** `gitlab-portfolio/04-rules-va-workflow/` gồm `bang-chan-tri.tsv` (bảng 6 × 5 — **hiện vật quan trọng nhất**), `pipeline-trung.tsv`, `thu-tu-rule.md`, `changes-sai.md`, `ba-trang-thai.md`, `manual-allow-failure.tsv`, `t0-bat-bien.md`, `workflow-chuan.yml`, `checkpoint.log`.

---

## L1. Điều kiện tiên quyết về môi trường

| # | Kiểm tra | Lệnh | Kết quả kỳ vọng |
|---|---|---|---|
| 1 | Đã nạp biến môi trường lab | `echo "$GITLAB" "$GITLAB_TOKEN" \| wc -w` | `2` |
| 2 | GitLab sẵn sàng | `curl -sf -o /dev/null -w '%{http_code}\n' "$GITLAB/-/readiness"` | `200` |
| 3 | Runner online, nhận job không tag | (đoạn kiểm ba điều kiện buổi 02 §L1) | ≥ 1 runner đạt cả ba |
| 4 | Token có quyền tạo **merge request** | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/user" \| jq -r .username` | in ra tên; token scope `api` |
| 5 | Token có quyền tạo **pipeline schedule** | (kiểm ở bước 1; nếu thiếu thì dùng đường B ở §L9) | — |
| 6 | Đã học buổi 03 | (tự kiểm) gọi được `ci/lint` và giải thích được `stage` | Bắt buộc |
| 7 | `git` cấu hình xong tên và email | `git config --get user.email` | khác rỗng |
| 8 | Chưa có project lab 04 | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects?search=lab04-rules" \| jq length` | `0` |

**Cảnh báo về mức độ tác động.** Bài lab tạo project `lab04-rules`, tạo **nhiều nhánh, một tag, một merge request và một pipeline schedule** trong project đó. Nó **không** sửa `config.toml`, **không** đụng project khác. Bước 1 tạo tổng cộng khoảng 10–14 pipeline — trên lớp đông, con số này nhân với sĩ số, nên §L1 dòng 3 phải đạt trước khi bắt đầu.

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    HV["Học viên"]
    HV -->|"6 cách kích hoạt khác nhau"| SRC["push nhánh thường · push nhánh chính<br/>merge_request_event · tag<br/>schedule · api"]
    SRC --> PRJ["Project lab04-rules"]
    HV -->|"POST ci/lint"| LINT["ci/lint — đọc rules SAU phân giải<br/>dùng cho QT 6.1, 6.4"]
    HV -->|"curl + jq"| API["API GitLab v4<br/>pipelines · jobs · merge_requests"]

    PRJ --> API
    API --> B1["Bước 1: BẢNG CHÂN TRỊ 6 × 5<br/>đo bằng KÍCH HOẠT THẬT<br/>job không khớp rule → BIẾN MẤT"]
    API --> B2["Bước 2: pipeline TRÙNG<br/>đếm theo SHA, trước và sau workflow"]
    LINT --> B3["Bước 3: đảo thứ tự rule → đổi when<br/>rules + only → valid=false"]
    API --> B3B["Bước 3: changes SAI ở NHÁNH MỚI"]
    API --> B4["Bước 4: ba trạng thái không chạy<br/>manual: hai cách viết, hai allow_failure"]
    API --> B5["Bước 5: t0 bất biến — retry KHÔNG đánh giá lại<br/>0 job → 0 pipeline"]

    B2 --> WF["workflow thêm ở bước 2 và GIỮ tới hết buổi<br/>→ bước 3,4,5 không bị nhiễu bởi pipeline trùng"]
```

**Bốn quyết định thiết kế:**

1. **Bảng chân trị đo bằng kích hoạt thật, không đọc tài liệu.** Sáu nguồn × năm rule = 30 ô. Đây là bảng cần nhất của giai đoạn 1 và nó chỉ có giá trị khi tự tay đo — đọc tài liệu cho ra một bảng người khác đo, và nó sai ngay khi phiên bản GitLab đổi. Phương án hiển nhiên — chép bảng từ tài liệu — nhanh hơn 25 phút nhưng không dạy được gì.

2. **`workflow` được thêm vào ở bước 2 rồi giữ tới hết buổi.** Nhờ đó bước 3, 4, 5 không bị nhiễu bởi pipeline trùng, và học viên thấy tác dụng của nó suốt phần còn lại thay vì chỉ ở một bước. Đây cũng là cách bài lab mô phỏng đúng thứ tự áp dụng ở nơi làm việc: đặt `workflow` trước, rồi mới tinh chỉnh `rules` từng job.

3. **Ca `changes` sai được tái hiện trên nhánh MỚI TẠO.** Đó là ca hay gặp nhất và cũng khó tin nhất khi chỉ đọc tài liệu — học viên phải thấy job `changes: [thu-muc-khong-dung/**]` chạy trên một nhánh mà họ không đụng thư mục đó.

4. **Bước 4 đo `allow_failure` bằng API chứ không nhìn giao diện.** Giao diện vẽ job manual **giống hệt nhau** ở cả hai cách viết, trong khi trường `allow_failure` khác nhau — và chính sự khác nhau ấy quyết định pipeline hiển thị `blocked` hay `success`.

**Ca đối chứng PHẢI THẤT BẠI — báo trước cho lớp.** Bước 1 có job **biến mất khỏi pipeline** (không phải `skipped`). Bước 3 có `ci/lint` trả `valid: false`. Bước 5 có một push **không tạo pipeline nào**. Cả ba là kết quả đúng.

---

## L3. Bước 1 — Bảng chân trị: sáu nguồn kích hoạt × rules (30 phút)

### 3.1. Tạo project và bộ công cụ (6 phút)

```bash
source ~/.gitlab-lab.env
export HAU_TO="${USER}"
mkdir -p ~/lab04 && cd ~/lab04

PID4=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{\"name\":\"lab04-rules-${HAU_TO}\",\"visibility\":\"internal\"}" \
  "$GITLAB/api/v4/projects" | jq -r .id)
echo "PID4=$PID4"
```

```bash
cat > ~/lab04/cong-cu.sh <<'SH'
#!/usr/bin/env bash
# Bộ công cụ lab buổi 04. Nạp: source ~/lab04/cong-cu.sh
: "${GITLAB:?}"; : "${GITLAB_TOKEN:?}"; : "${PID4:?}"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")
A="$GITLAB/api/v4/projects/$PID4"

lint() {
  curl -sf --request POST "${H[@]}" --header "Content-Type: application/json" \
    --data "$(jq -Rs '{content: ., include_merged_yaml: true}' < "${1:-.gitlab-ci.yml}")" \
    "$A/ci/lint"
}

# Đẩy lên MỘT nhánh cụ thể và trả về id pipeline mới nhất của nhánh đó
day_nhanh() {
  local nhanh="$1" msg="${2:-cap nhat}"
  git add -A >/dev/null; git commit -q -m "$msg" --allow-empty
  git push -q -f origin "HEAD:refs/heads/$nhanh" 2>/dev/null
  sleep 6
  curl -sf "${H[@]}" "$A/pipelines?ref=$nhanh&per_page=1" | jq -r '.[0].id // "KHONG-CO"'
}

cho_pipeline() {
  local pipe="$1" han="${2:-300}" t=0 st
  [ "$pipe" = "KHONG-CO" ] && { echo "KHONG-CO"; return 0; }
  while [ "$t" -lt "$han" ]; do
    st=$(curl -sf "${H[@]}" "$A/pipelines/$pipe" | jq -r .status)
    case "$st" in success|failed|canceled|skipped) echo "$st"; return 0 ;; esac
    sleep 5; t=$((t+5))
  done
  echo "$st"
}

# DANH SÁCH JOB của một pipeline — công cụ trung tâm của buổi
job_ten() {
  [ "$1" = "KHONG-CO" ] && return 0
  curl -sf "${H[@]}" "$A/pipelines/$1/jobs?per_page=100" | jq -r '.[].name' | sort
}
job_bang() {
  [ "$1" = "KHONG-CO" ] && { echo "(khong co pipeline)"; return 0; }
  curl -sf "${H[@]}" "$A/pipelines/$1/jobs?per_page=100" \
  | jq -r '.[] | [.name, .status, (.allow_failure|tostring)] | @tsv'
}
# job CÓ trong pipeline hay KHÔNG — trả về CO / KHONG
co_job() {
  local pipe="$1" ten="$2"
  [ "$pipe" = "KHONG-CO" ] && { echo "KHONG-PIPELINE"; return 0; }
  if job_ten "$pipe" | grep -qx "$ten"; then echo "CO"; else echo "KHONG"; fi
}
nguon_cua() {
  [ "$1" = "KHONG-CO" ] && { echo "-"; return 0; }
  curl -sf "${H[@]}" "$A/pipelines/$1" | jq -r .source
}
SH
source ~/lab04/cong-cu.sh

git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$A" | jq -r .path_with_namespace).git"
git config user.email "hocvien@lab.local"; git config user.name "hoc vien"
mkdir -p src docs
echo "x" > src/a.txt; echo "y" > docs/b.txt
```

### 3.2. Pipeline đo bảng chân trị (8 phút)

Năm job, năm rule khác nhau. Job nào **có mặt** trong pipeline là câu trả lời của một ô.

```yaml
# ~/lab04/.gitlab-ci.yml
stages: [do]

.mau:
  stage: do
  image: alpine:3.20
  script:
    - echo "nguon = $CI_PIPELINE_SOURCE"
    - echo "nhanh = ${CI_COMMIT_BRANCH:-khong-co}"
    - echo "tag   = ${CI_COMMIT_TAG:-khong-co}"

r1-luon-chay:
  extends: .mau
  rules:
    - when: always

r2-chi-nhanh-chinh:
  extends: .mau
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

r3-chi-merge-request:
  extends: .mau
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

r4-chi-tag:
  extends: .mau
  rules:
    - if: $CI_COMMIT_TAG

r5-changes-src:
  extends: .mau
  rules:
    - changes: [src/**/*]
```

### 3.3. Kích hoạt sáu nguồn và điền bảng (16 phút)

```bash
cd ~/lab04
JOBS="r1-luon-chay r2-chi-nhanh-chinh r3-chi-merge-request r4-chi-tag r5-changes-src"
echo -e "nguon\tCI_PIPELINE_SOURCE\t$(echo $JOBS | tr ' ' '\t')" > ~/lab04/bang-chan-tri.tsv

dien_dong() {   # $1 = tên nguồn, $2 = pipeline id
  local ten="$1" pipe="$2" src dong
  src=$(nguon_cua "$pipe")
  dong="$ten\t$src"
  for j in $JOBS; do dong="$dong\t$(co_job "$pipe" "$j")"; done
  echo -e "$dong" | tee -a ~/lab04/bang-chan-tri.tsv
}
```

**Nguồn 1 — push nhánh chính.**

```bash
P_MAIN=$(day_nhanh main "nguon 1: push nhanh chinh")
cho_pipeline "$P_MAIN" >/dev/null
dien_dong "push-nhanh-chinh" "$P_MAIN"
```

**Nguồn 2 — push nhánh thường, có sửa `src/`.**

```bash
git checkout -q -b tinh-nang-a
echo "doi src" >> src/a.txt
P_NHANH=$(day_nhanh tinh-nang-a "nguon 2: push nhanh thuong, sua src")
cho_pipeline "$P_NHANH" >/dev/null
dien_dong "push-nhanh-thuong" "$P_NHANH"
```

**Nguồn 3 — merge request.**

```bash
MR_IID=$(curl -sf --request POST "${H[@]}" --header "Content-Type: application/json" \
  --data '{"source_branch":"tinh-nang-a","target_branch":"main","title":"MR do bang chan tri"}' \
  "$A/merge_requests" | jq -r .iid)
echo "MR !$MR_IID"
sleep 8
P_MR=$(curl -sf "${H[@]}" "$A/merge_requests/$MR_IID/pipelines" | jq -r '.[0].id // "KHONG-CO"')
cho_pipeline "$P_MR" >/dev/null
dien_dong "merge-request" "$P_MR"
```

**Nguồn 4 — tag.**

```bash
git checkout -q main
git tag -f v0.1.0 >/dev/null && git push -q -f origin v0.1.0
sleep 8
P_TAG=$(curl -sf "${H[@]}" "$A/pipelines?ref=v0.1.0&per_page=1" | jq -r '.[0].id // "KHONG-CO"')
cho_pipeline "$P_TAG" >/dev/null
dien_dong "tag" "$P_TAG"
```

**Nguồn 5 — gọi API (`trigger`/`api`).**

```bash
P_API=$(curl -sf --request POST "${H[@]}" \
  "$A/pipeline?ref=main" | jq -r '.id // "KHONG-CO"')
cho_pipeline "$P_API" >/dev/null
dien_dong "api" "$P_API"
```

**Nguồn 6 — pipeline theo lịch.**

```bash
SCH_ID=$(curl -sf --request POST "${H[@]}" --header "Content-Type: application/json" \
  --data '{"description":"lab04","ref":"main","cron":"0 1 * * *"}' \
  "$A/pipeline_schedules" | jq -r .id)
P_SCH=$(curl -sf --request POST "${H[@]}" "$A/pipeline_schedules/$SCH_ID/play" >/dev/null 2>&1; \
        sleep 10; curl -sf "${H[@]}" "$A/pipelines?source=schedule&per_page=1" | jq -r '.[0].id // "KHONG-CO"')
cho_pipeline "$P_SCH" >/dev/null
dien_dong "schedule" "$P_SCH"

echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)" >> ~/lab04/bang-chan-tri.tsv
echo "# Ngày đo: $(date -Iseconds)" >> ~/lab04/bang-chan-tri.tsv
column -t -s$'\t' ~/lab04/bang-chan-tri.tsv
```

**CHECKPOINT 1 — kích hoạt được ít nhất 5 trong 6 nguồn.**

```bash
n=$(grep -cE '^(push-nhanh-chinh|push-nhanh-thuong|merge-request|tag|api|schedule)' ~/lab04/bang-chan-tri.tsv || true)
[ "$n" -ge 5 ] \
  && echo "CHECKPOINT 1 — ĐẠT ($n/6 nguồn kích hoạt được)" \
  || echo "CHECKPOINT 1 — LỖI (chỉ $n/6 nguồn; xem §L9 đường B cho schedule)"
```

**CHECKPOINT 2 — bảng chân trị có đủ 30 ô (6 nguồn × 5 job).**

```bash
o=$(tail -n +2 ~/lab04/bang-chan-tri.tsv | grep -E '^[a-z]' | awk -F'\t' '{c+=NF-2} END{print c+0}')
[ "$o" -ge 25 ] \
  && echo "CHECKPOINT 2 — ĐẠT ($o ô đã điền)" \
  || echo "CHECKPOINT 2 — LỖI ($o ô, cần ≥25)"
```

**CHECKPOINT 3 — job không khớp rule BIẾN MẤT, không phải `skipped`.**

```bash
# Trên nhánh thường, r2 (chỉ nhánh chính) và r4 (chỉ tag) phải KHÔNG có mặt
co_r2=$(co_job "$P_NHANH" r2-chi-nhanh-chinh)
co_r4=$(co_job "$P_NHANH" r4-chi-tag)
skipped=$(job_bang "$P_NHANH" | grep -c 'skipped' || true)
{ [ "$co_r2" = "KHONG" ] && [ "$co_r4" = "KHONG" ] && [ "$skipped" -eq 0 ]; } \
  && echo "CHECKPOINT 3 — ĐẠT (r2=$co_r2, r4=$co_r4, 0 job skipped → chúng BIẾN MẤT)" \
  || echo "CHECKPOINT 3 — LỖI (r2=$co_r2 r4=$co_r4 skipped=$skipped)"
```

**Bốn câu hỏi phải trả lời, ghi vào `bang-chan-tri.tsv`:**

1. Ô nào trong bảng làm bạn **bất ngờ nhất** so với phỏng đoán ở BTVN 4 buổi 03?
2. Job `r5-changes-src` chạy ở nguồn nào, **không** chạy ở nguồn nào? Kết quả có khớp QT 6.3 không?
3. Ở nguồn `schedule`, job `r5-changes-src` có chạy không? Điều đó ứng với ca nào trong ba ca của QT 6.3?
4. Job `r1-luon-chay` có mặt ở **cả sáu** nguồn không? Nếu có, điều đó nói gì về `- when: always`?

---

## L4. Bước 2 — Pipeline trùng và `workflow` (30 phút)

### 4.1. Đo pipeline trùng (12 phút)

Kiểm chứng QT 5.2. Merge request `!$MR_IID` từ bước 1 vẫn đang mở — đẩy thêm commit lên nhánh nguồn.

```bash
cd ~/lab04
git checkout -q tinh-nang-a
for i in 1 2 3; do
  echo "commit $i" >> src/a.txt
  git add -A >/dev/null && git commit -q -m "commit trung $i"
done
git push -q origin tinh-nang-a
sleep 12

# Đếm pipeline theo SHA
curl -sf "${H[@]}" "$A/pipelines?per_page=100" \
| jq -r 'group_by(.sha) | map({sha: .[0].sha[0:8], so: length, nguon: [.[].source]})
         | .[] | "\(.sha)\t\(.so)\t\(.nguon | join(","))"' | tee ~/lab04/trung-truoc.txt
```

```bash
TRUNG=$(awk -F'\t' '$2>1' ~/lab04/trung-truoc.txt | wc -l)
TONG_PHUT=$(curl -sf "${H[@]}" "$A/pipelines?per_page=100" | jq -r '[.[].id]|.[]' \
  | while read -r p; do curl -sf "${H[@]}" "$A/pipelines/$p" | jq -r '.duration // 0'; done \
  | awk '{s+=$1} END{printf "%.1f", s/60}')

{
  echo "# QT 5.2 — pipeline trùng. GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
  echo -e "giai_doan\tso_sha_co_pipeline_trung\ttong_phut_runner"
  echo -e "truoc_workflow\t$TRUNG\t$TONG_PHUT"
} | tee ~/lab04/pipeline-trung.tsv
```

**CHECKPOINT 4 — có ít nhất một SHA sinh hơn một pipeline.**

```bash
[ "$TRUNG" -ge 1 ] \
  && echo "CHECKPOINT 4 — ĐẠT ($TRUNG SHA có pipeline trùng — gấp đôi phút runner)" \
  || echo "CHECKPOINT 4 — LỖI (không thấy trùng; kiểm MR còn mở không)"
```

### 4.2. Thêm `workflow` chuẩn và đo lại (18 phút)

```yaml
# ~/lab04/.gitlab-ci.yml — thêm khối workflow vào ĐẦU tệp, giữ nguyên 5 job
workflow:
  rules:
    # 1. Pipeline của merge request
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    # 2. Bỏ pipeline push khi nhánh đó ĐANG có merge request mở
    #    QUY TẮC NÀY PHẢI NẰM SAU quy tắc 1 — xem QT 6.1
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    # 3. Nhánh chính luôn chạy
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    # 4. Tag luôn chạy
    - if: $CI_COMMIT_TAG
    # 5. Nhánh khác chưa có MR: vẫn chạy
    - if: $CI_COMMIT_BRANCH
```

```bash
cd ~/lab04
cp .gitlab-ci.yml ~/lab04/workflow-chuan.yml
lint | jq -r '.valid, (.errors[]?)'

for i in 4 5 6; do
  echo "commit $i" >> src/a.txt
  git add -A >/dev/null && git commit -q -m "commit sau workflow $i"
done
git push -q origin tinh-nang-a
sleep 12

curl -sf "${H[@]}" "$A/pipelines?per_page=100" \
| jq -r 'group_by(.sha) | map({sha: .[0].sha[0:8], so: length, nguon: [.[].source]})
         | .[] | "\(.sha)\t\(.so)\t\(.nguon | join(","))"' | tee ~/lab04/trung-sau.txt

TRUNG2=$(awk -F'\t' '$2>1' ~/lab04/trung-sau.txt | wc -l)
echo -e "sau_workflow\t$TRUNG2\t(do lai sau)" >> ~/lab04/pipeline-trung.tsv
```

**CHECKPOINT 5 — sau khi thêm `workflow`, ba commit mới KHÔNG sinh pipeline trùng.**

```bash
# Ba SHA mới nhất phải mỗi cái đúng 1 pipeline
MOI=$(git rev-parse HEAD | cut -c1-8)
SO_MOI=$(awk -F'\t' -v s="$MOI" '$1==s {print $2}' ~/lab04/trung-sau.txt)
{ [ "${SO_MOI:-9}" -eq 1 ]; } \
  && echo "CHECKPOINT 5 — ĐẠT (SHA $MOI có đúng 1 pipeline; trước workflow có $TRUNG SHA trùng)" \
  || echo "CHECKPOINT 5 — LỖI (SHA $MOI có ${SO_MOI:-?} pipeline)"
```

**Ba câu hỏi phải trả lời, ghi vào `pipeline-trung.tsv`:**

1. Trước `workflow`, mỗi commit trên nhánh có MR sinh mấy pipeline? Nguồn của chúng là gì?
2. Nếu repo của bạn có 40 commit một tuần trên các nhánh có MR, và mỗi pipeline 6 phút runner, thì `workflow` tiết kiệm bao nhiêu **phút runner một tháng**?
3. Trong `workflow` chuẩn, thử **đảo** quy tắc 1 và quy tắc 2 rồi gọi `lint`. Pipeline MR còn được tạo không? Vì sao? (Dẫn QT 6.1.)

---

## L5. Bước 3 — Thứ tự rule; `changes` sai ở nhánh mới (30 phút)

### 5.1. Đảo thứ tự rule đổi hành vi (10 phút)

Kiểm chứng QT 6.1 bằng `ci/lint`, **không đẩy commit**.

```bash
cd ~/lab04
cat > /tmp/thu-tu-sai.yml <<'EOF'
deploy:
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_BRANCH                       # CHUNG — khớp mọi nhánh
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH # RIÊNG — không bao giờ tới
      when: manual
  script: [echo deploy]
EOF
cat > /tmp/thu-tu-dung.yml <<'EOF'
deploy:
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH # RIÊNG trước
      when: manual
    - if: $CI_COMMIT_BRANCH                       # CHUNG sau
  script: [echo deploy]
EOF

echo "=== THỨ TỰ SAI ==="; lint /tmp/thu-tu-sai.yml | jq -r '.jobs[] | {name, when}'
echo "=== THỨ TỰ ĐÚNG ==="; lint /tmp/thu-tu-dung.yml | jq -r '.jobs[] | {name, when}'
```

Xác nhận bằng chạy thật trên nhánh chính:

```bash
git checkout -q main
cp /tmp/thu-tu-sai.yml /tmp/gi.yml
python3 - <<'PY'
import re,io
p='/home/'+__import__('os').environ['USER']+'/lab04/.gitlab-ci.yml'
s=open(p).read()
s+= "\n" + open('/tmp/thu-tu-sai.yml').read().replace('deploy:','deploy-thu-tu-sai:')
s+= "\n" + open('/tmp/thu-tu-dung.yml').read().replace('deploy:','deploy-thu-tu-dung:')
open(p,'w').write(s)
PY
P_TT=$(day_nhanh main "buoc 3: thu tu rule"); cho_pipeline "$P_TT" >/dev/null
job_bang "$P_TT" | grep deploy-
```

**CHECKPOINT 6 — hai job cùng điều kiện, khác thứ tự, cho hai trạng thái khác nhau.**

```bash
S_SAI=$(curl -sf "${H[@]}" "$A/pipelines/$P_TT/jobs?per_page=100" | jq -r '.[]|select(.name=="deploy-thu-tu-sai")|.status')
S_DUNG=$(curl -sf "${H[@]}" "$A/pipelines/$P_TT/jobs?per_page=100" | jq -r '.[]|select(.name=="deploy-thu-tu-dung")|.status')
{ [ -n "$S_SAI" ] && [ -n "$S_DUNG" ] && [ "$S_SAI" != "$S_DUNG" ]; } \
  && echo "CHECKPOINT 6 — ĐẠT (thu-tu-sai=$S_SAI, thu-tu-dung=$S_DUNG → thứ tự QUYẾT ĐỊNH kết quả)" \
  || echo "CHECKPOINT 6 — LỖI (sai=$S_SAI, dung=$S_DUNG)"
```

Ghi `thu-tu-rule.md` với bảng hai cột: thứ tự viết · `when` kết quả · giải thích theo QT 6.1.

### 5.2. `rules` và `only` loại trừ nhau (5 phút)

Kiểm chứng QT 6.4 — **đây là ca ĐỐI CHỨNG ồn ào** giữa ba ca im lặng của buổi.

```bash
cat > /tmp/rules-va-only.yml <<'EOF'
job-sai:
  image: alpine:3.20
  only: [main]
  rules:
    - if: $CI_COMMIT_TAG
  script: [echo x]
EOF
lint /tmp/rules-va-only.yml | jq -r '.valid, (.errors[]?)'
```

**CHECKPOINT 7 — `ci/lint` trả `valid: false` với thông báo về `rules` và `only`.**

```bash
V=$(lint /tmp/rules-va-only.yml | jq -r .valid)
E=$(lint /tmp/rules-va-only.yml | jq -r '[.errors[]?] | join(" ")')
{ [ "$V" = "false" ] && echo "$E" | grep -qi 'rules'; } \
  && echo "CHECKPOINT 7 — ĐẠT (valid=$V, lỗi: $E → ồn ào, có chặn)" \
  || echo "CHECKPOINT 7 — LỖI (valid=$V, lỗi=$E)"
```

### 5.3. `changes` âm thầm sai ở nhánh mới tạo (15 phút)

Kiểm chứng QT 6.3 ca 1 — ca hay gặp nhất và khó tin nhất khi chỉ đọc tài liệu.

```bash
cd ~/lab04
git checkout -q main
# Nhánh HOÀN TOÀN MỚI, và ta chỉ đụng docs/ — KHÔNG đụng src/
git checkout -q -b nhanh-moi-tinh
echo "chi sua docs, khong dung src" >> docs/b.txt
P_MOI=$(day_nhanh nhanh-moi-tinh "buoc 3: nhanh moi, chi sua docs")
cho_pipeline "$P_MOI" >/dev/null
job_bang "$P_MOI"
```

```bash
CO_R5=$(co_job "$P_MOI" r5-changes-src)
{
  echo "# QT 6.3 ca 1 — changes SAI ở nhánh mới tạo"
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
  echo "nhanh              = nhanh-moi-tinh (mới tạo từ main)"
  echo "tep_da_sua         = docs/b.txt  (KHONG dung src/)"
  echo "rule_cua_job       = changes: [src/**/*]"
  echo "job_co_chay_khong  = $CO_R5"
  echo "ky_vong_hop_ly     = KHONG (vi khong ai dung src/)"
  echo "ket_luan           = $([ "$CO_R5" = "CO" ] && echo 'CHANGES SAI — chay du khong can' || echo 'dung nhu mong doi')"
} | tee ~/lab04/changes-sai.md
```

**CHECKPOINT 8 — ghi được kết quả đo của ca `changes` trên nhánh mới, kèm phiên bản GitLab.**

```bash
k=$(grep -c 'ket_luan' ~/lab04/changes-sai.md || true)
v=$(grep -c 'GitLab' ~/lab04/changes-sai.md || true)
{ [ "$k" -ge 1 ] && [ "$v" -ge 1 ]; } \
  && echo "CHECKPOINT 8 — ĐẠT ($(grep ket_luan ~/lab04/changes-sai.md))" \
  || echo "CHECKPOINT 8 — LỖI (kết luận=$k, phiên bản=$v)"
```

**Ba câu hỏi phải trả lời, ghi vào `changes-sai.md`:**

1. Job `r5-changes-src` có chạy trên nhánh mới không, dù bạn chỉ sửa `docs/`? Đó là ca nào trong ba ca của QT 6.3?
2. Thêm `compare_to: refs/heads/main` vào rule đó rồi đẩy lại. Kết quả đổi không?
3. Nếu `r5-changes-src` là một job **quét bảo mật**, ca sai này rơi vào ô nào của bảng hai thuộc tính, và vì sao §8 lý thuyết nói **đừng dùng `changes` cho job security**?

---

## L6. Bước 4 — Ba trạng thái "không chạy"; `manual` (30 phút)

### 6.1. Ba trạng thái trong một pipeline (16 phút)

Kiểm chứng QT 7.1.

```yaml
# ~/lab04/.gitlab-ci.yml — thay phần job (GIỮ NGUYÊN khối workflow ở đầu tệp)
stages: [truoc, sau]

# Trạng thái 1: KHÔNG CÓ MẶT — rules không khớp
tt1-khong-co-mat:
  stage: truoc
  image: alpine:3.20
  rules:
    - if: $BIEN_KHONG_BAO_GIO_DUNG == "x"
  script: [echo "khong bao gio chay"]

# Trạng thái 2: MANUAL — có mặt, chờ người bấm
tt2-manual-trong-rules:
  stage: truoc
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_BRANCH
      when: manual
  script: [echo "cho bam"]

tt2-manual-truc-tiep:
  stage: truoc
  image: alpine:3.20
  when: manual
  script: [echo "cho bam"]

# Job đỏ để sinh trạng thái 3
job-do:
  stage: truoc
  image: alpine:3.20
  script: [exit 1]

# Trạng thái 3: SKIPPED — có mặt, bị bỏ qua vì job trước đỏ
tt3-skipped:
  stage: sau
  image: alpine:3.20
  script: [echo "se bi skipped"]
```

```bash
cd ~/lab04
git checkout -q main
P_TT3=$(day_nhanh main "buoc 4: ba trang thai"); cho_pipeline "$P_TT3" 300 >/dev/null
job_bang "$P_TT3"
```

**CHECKPOINT 9 — ba trạng thái phân biệt được bằng API.**

```bash
J=$(curl -sf "${H[@]}" "$A/pipelines/$P_TT3/jobs?per_page=100")
co1=$(echo "$J" | jq -r '[.[]|select(.name=="tt1-khong-co-mat")]|length')
st2=$(echo "$J" | jq -r '.[]|select(.name=="tt2-manual-trong-rules")|.status')
st3=$(echo "$J" | jq -r '.[]|select(.name=="tt3-skipped")|.status')
{ [ "$co1" -eq 0 ] && [ "$st2" = "manual" ] && [ "$st3" = "skipped" ]; } \
  && echo "CHECKPOINT 9 — ĐẠT (tt1 KHÔNG CÓ MẶT, tt2=$st2, tt3=$st3 → ba trạng thái khác nhau)" \
  || echo "CHECKPOINT 9 — LỖI (tt1 có mặt=$co1, tt2=$st2, tt3=$st3)"
```

Ghi `ba-trang-thai.md` — bảng này là hiện vật của bước 4:

| Trạng thái | Cách tạo ra | Có trong `pipelines/:id/jobs` | `status` | Chặn job sau | Ô của bảng hai thuộc tính |
|---|---|---|---|---|---|
| Không có mặt | | | | | |
| `manual` | | | | | |
| `skipped` | | | | | |

### 6.2. `manual` có hai mặc định khác nhau (14 phút)

Kiểm chứng QT 7.2 — đại lượng loại (c), **đo bằng API chứ không nhìn giao diện**.

```bash
{
  echo "# QT 7.2 — allow_failure mặc định của manual, ĐO bằng API"
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
  echo "# Ngày đo: $(date -Iseconds)"
  echo -e "cach_viet\tjob\tstatus\tallow_failure"
  echo "$J" | jq -r '.[] | select(.name|startswith("tt2-")) |
    [(if (.name|test("trong-rules")) then "manual-TRONG-rules" else "manual-TRUC-TIEP" end),
     .name, .status, (.allow_failure|tostring)] | @tsv'
} | tee ~/lab04/manual-allow-failure.tsv
```

**CHECKPOINT 10 — hai cách viết `manual` cho hai giá trị `allow_failure` khác nhau.**

```bash
AF_R=$(echo "$J" | jq -r '.[]|select(.name=="tt2-manual-trong-rules")|.allow_failure')
AF_T=$(echo "$J" | jq -r '.[]|select(.name=="tt2-manual-truc-tiep")|.allow_failure')
{ [ -n "$AF_R" ] && [ -n "$AF_T" ] && [ "$AF_R" != "$AF_T" ]; } \
  && echo "CHECKPOINT 10 — ĐẠT (trong rules: allow_failure=$AF_R; trực tiếp: $AF_T → HAI mặc định)" \
  || echo "CHECKPOINT 10 — LỖI (trong rules=$AF_R, trực tiếp=$AF_T — nếu bằng nhau thì phiên bản này đã hợp nhất; GHI LẠI, đó là dữ liệu)"
```

**Ba câu hỏi phải trả lời, ghi vào `manual-allow-failure.tsv`:**

1. Hai giá trị `allow_failure` đo được là gì? Chúng có khác nhau trên phiên bản GitLab của bạn không?
2. Nếu không ai bấm nút, pipeline hiển thị trạng thái gì? Hai job cho kết quả khác nhau ra sao?
3. Vì sao §7 lý thuyết khuyên **luôn khai `allow_failure` tường minh** cho job manual?

---

## L7. Bước 5 — `t0` bất biến: retry và pipeline rỗng (20 phút)

### 7.1. Retry không đánh giá lại `rules` (10 phút)

Kiểm chứng QT 4.1.

```bash
cd ~/lab04
# Đặt một biến ở cấp PROJECT, giá trị làm job KHÔNG chạy
curl -sf --request POST "${H[@]}" --header "Content-Type: application/json" \
  --data '{"key":"CHE_DO","value":"tat"}' "$A/variables" >/dev/null 2>&1 || \
curl -sf --request PUT "${H[@]}" --header "Content-Type: application/json" \
  --data '{"value":"tat"}' "$A/variables/CHE_DO" >/dev/null
```

```yaml
# ~/lab04/.gitlab-ci.yml — thay phần job, GIỮ workflow
stages: [do]

job-phu-thuoc-bien:
  stage: do
  image: alpine:3.20
  rules:
    - if: $CHE_DO == "bat"
  script: [echo "chay khi CHE_DO=bat"]

job-luon-co:
  stage: do
  image: alpine:3.20
  script: [echo "luon co mat"]
```

```bash
P_T0=$(day_nhanh main "buoc 5: t0 bat bien"); cho_pipeline "$P_T0" >/dev/null
CO_TRUOC=$(co_job "$P_T0" job-phu-thuoc-bien)
echo "trước khi đổi biến: job-phu-thuoc-bien = $CO_TRUOC"

# Đổi biến ở cấp project rồi RETRY pipeline cũ
curl -sf --request PUT "${H[@]}" --header "Content-Type: application/json" \
  --data '{"value":"bat"}' "$A/variables/CHE_DO" | jq -r '"CHE_DO = \(.value)"'
curl -sf --request POST "${H[@]}" "$A/pipelines/$P_T0/retry" >/dev/null
sleep 10
CO_SAU=$(co_job "$P_T0" job-phu-thuoc-bien)
echo "sau retry (biến đã đổi): job-phu-thuoc-bien = $CO_SAU"

# Tạo PIPELINE MỚI với cùng biến ấy
P_MOI2=$(curl -sf --request POST "${H[@]}" "$A/pipeline?ref=main" | jq -r .id)
cho_pipeline "$P_MOI2" >/dev/null
CO_MOI=$(co_job "$P_MOI2" job-phu-thuoc-bien)
echo "pipeline MỚI (biến đã đổi): job-phu-thuoc-bien = $CO_MOI"
```

### 7.2. Không job nào thì không có pipeline (10 phút)

Kiểm chứng QT 4.3. **Push này sẽ KHÔNG tạo pipeline — đó là kết quả đúng.**

```bash
cd ~/lab04
cat > .gitlab-ci.yml <<'EOF'
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH

moi-job-deu-bi-loai:
  image: alpine:3.20
  rules:
    - if: $BIEN_KHONG_BAO_GIO_DUNG == "x"
  script: [echo "khong bao gio"]
EOF

echo "=== ci/lint nói gì ==="
lint | jq -r '"valid=\(.valid)  so_job=\((.jobs//[])|length)"'

SHA_TRUOC=$(git rev-parse HEAD)
P_RONG=$(day_nhanh main "buoc 5: moi job bi loai")
echo "pipeline sinh ra: $P_RONG"
SHA_SAU=$(git rev-parse HEAD)
curl -sf "${H[@]}" "$A/repository/commits/$SHA_SAU" | jq -r '.last_pipeline.id // "KHONG CO PIPELINE"'
```

```bash
SO_JOB_LINT=$(lint | jq -r '(.jobs//[])|length')
{
  echo "# QT 4.1 và 4.3 — t0 BẤT BIẾN"
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
  echo "## QT 4.1 — retry KHÔNG đánh giá lại rules"
  echo "job_truoc_khi_doi_bien   = $CO_TRUOC"
  echo "job_sau_RETRY            = $CO_SAU     (biến đã đổi thành bat)"
  echo "job_o_PIPELINE_MOI       = $CO_MOI     (cùng biến đó)"
  echo "ket_luan_4_1             = $([ "$CO_SAU" = "KHONG" ] && [ "$CO_MOI" = "CO" ] && echo 'XAC NHAN: retry khong danh gia lai, pipeline moi thi co' || echo 'CAN XEM LAI')"
  echo "## QT 4.3 — 0 job → 0 pipeline"
  echo "so_job_theo_ci_lint      = $SO_JOB_LINT"
  echo "pipeline_sinh_ra         = $P_RONG"
  echo "ket_luan_4_3             = $([ "$SO_JOB_LINT" -eq 0 ] && echo '0 job -> khong co pipeline' || echo 'con job, co pipeline')"
} | tee ~/lab04/t0-bat-bien.md
```

**CHECKPOINT 11 — retry không đánh giá lại `rules`, nhưng pipeline mới thì có.**

```bash
{ [ "$CO_TRUOC" = "KHONG" ] && [ "$CO_SAU" = "KHONG" ] && [ "$CO_MOI" = "CO" ]; } \
  && echo "CHECKPOINT 11 — ĐẠT (retry: $CO_SAU · pipeline mới: $CO_MOI → t0 BẤT BIẾN)" \
  || echo "CHECKPOINT 11 — LỖI (trước=$CO_TRUOC retry=$CO_SAU mới=$CO_MOI)"
```

### 7.3. `dotenv` tới quá muộn — đo trực tiếp (bổ sung, làm nếu còn giờ)

Kiểm chứng QT 4.2 **bằng đo** thay vì bằng lập luận. Đây là hệ quả trực tiếp của QT 4.1 và là ca sai tốn thời gian nhất ở nơi làm việc, nên đáng đo một lần cho nhớ.

```yaml
# ~/lab04/.gitlab-ci.yml — thay toàn bộ, GIỮ khối workflow
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH

stages: [sinh, dung]

tinh-phien-ban:
  stage: sinh
  image: alpine:3.20
  script:
    - echo "PHIEN_BAN=v1.2.3" > bien.env
    - echo "job nay DA sinh ra PHIEN_BAN=v1.2.3"
    - cat bien.env
  artifacts:
    reports:
      dotenv: bien.env

# SAI — rules dùng biến sinh ở t1, không tồn tại ở t0
deploy-rules-dung-dotenv:
  stage: dung
  image: alpine:3.20
  needs: [tinh-phien-ban]
  rules:
    - if: '$PHIEN_BAN =~ /^v/'
  script: [echo "deploy $PHIEN_BAN"]

# ĐÚNG — rules dùng biến có ở t0; dotenv dùng BÊN TRONG script
deploy-rules-dung-bien-he-thong:
  stage: dung
  image: alpine:3.20
  needs: [tinh-phien-ban]
  rules:
    - if: $CI_COMMIT_BRANCH
  script:
    - test -n "$PHIEN_BAN" || { echo "KHANG DINH HONG: PHIEN_BAN rong"; exit 1; }
    - echo "deploy $PHIEN_BAN"
```

```bash
cd ~/lab04
P_DOT=$(day_nhanh main "buoc 5c: dotenv toi qua muon"); cho_pipeline "$P_DOT" >/dev/null
job_bang "$P_DOT"

CO_SAI=$(co_job "$P_DOT" deploy-rules-dung-dotenv)
CO_DUNG=$(co_job "$P_DOT" deploy-rules-dung-bien-he-thong)
LOG_SINH=$(job_log "$(curl -sf "${H[@]}" "$A/pipelines/$P_DOT/jobs?per_page=100" \
           | jq -r '.[]|select(.name=="tinh-phien-ban")|.id')" | grep -c 'DA sinh ra' || true)

{
  echo
  echo "## QT 4.2 — dotenv tới QUÁ MUỘN cho rules"
  echo "job_sinh_bien_da_chay        = $([ "$LOG_SINH" -ge 1 ] && echo CO || echo KHONG)"
  echo "rules_dung_bien_dotenv       = $CO_SAI      (ky vong: KHONG — bien chua ton tai o t0)"
  echo "rules_dung_bien_he_thong     = $CO_DUNG     (ky vong: CO)"
  echo "ket_luan_4_2                 = $([ "$CO_SAI" = "KHONG" ] && [ "$CO_DUNG" = "CO" ] \
        && echo 'XAC NHAN: bien dotenv KHONG dung duoc trong rules' || echo 'CAN XEM LAI')"
} | tee -a ~/lab04/t0-bat-bien.md
```

**Hai câu hỏi phải trả lời, ghi ngay dưới:**

1. Job `tinh-phien-ban` **rõ ràng đã chạy** và log của nó in ra `PHIEN_BAN=v1.2.3`. Vậy vì sao `deploy-rules-dung-dotenv` vẫn không có mặt? Trả lời bằng trục thời gian `t0`.
2. Job sai ấy **biến mất** hay **`skipped`**? Nếu nó là job deploy production, ai sẽ phát hiện ra rằng deploy đã không chạy, và sau bao lâu?

---

## L8. Nộp sản phẩm và dọn dẹp (10 phút)

```bash
DICH="$PORTFOLIO/04-rules-va-workflow"
mkdir -p "$DICH"
cp ~/lab04/bang-chan-tri.tsv        "$DICH/"
cp ~/lab04/pipeline-trung.tsv       "$DICH/"
cp ~/lab04/changes-sai.md           "$DICH/"
cp ~/lab04/manual-allow-failure.tsv "$DICH/"
cp ~/lab04/t0-bat-bien.md           "$DICH/"
cp ~/lab04/workflow-chuan.yml       "$DICH/"
# thu-tu-rule.md và ba-trang-thai.md do học viên tự viết

cat > "$DICH/kiem-hien-vat.sh" <<'SH'
#!/usr/bin/env bash
cd "$(dirname "$0")"
P=0; F=0
kiem() { if eval "$2" >/dev/null 2>&1; then echo "ĐẠT   $1"; P=$((P+1)); else echo "LỖI   $1"; F=$((F+1)); fi; }

kiem "bang-chan-tri.tsv có ≥5 nguồn"          "[ \$(grep -cE '^(push-|merge-|tag|api|schedule)' bang-chan-tri.tsv) -ge 5 ]"
kiem "bang-chan-tri.tsv ghi phiên bản GitLab" "grep -q 'GitLab' bang-chan-tri.tsv"
kiem "pipeline-trung.tsv có trước và sau"      "[ \$(grep -cE '^(truoc_workflow|sau_workflow)' pipeline-trung.tsv) -eq 2 ]"
kiem "thu-tu-rule.md có bảng 2 thứ tự"         "[ \$(grep -cE '^\| ' thu-tu-rule.md) -ge 3 ]"
kiem "changes-sai.md có kết luận"              "grep -q 'ket_luan' changes-sai.md"
kiem "ba-trang-thai.md có 3 trạng thái"        "[ \$(grep -cE 'khong co mat|manual|skipped' ba-trang-thai.md) -ge 3 ]"
kiem "manual-allow-failure.tsv có 2 cách viết" "[ \$(grep -cE 'manual-(TRONG|TRUC)' manual-allow-failure.tsv) -eq 2 ]"
kiem "t0-bat-bien.md có kết luận 4.1 và 4.3"   "[ \$(grep -cE '^ket_luan_4_[13]') -eq 2 ] || [ \$(grep -cE 'ket_luan_4_' t0-bat-bien.md) -ge 2 ]"
kiem "workflow-chuan.yml có khối workflow"     "grep -q '^workflow:' workflow-chuan.yml"
kiem "checkpoint.log có 11 dòng CHECKPOINT"    "[ \$(grep -c 'CHECKPOINT' checkpoint.log) -ge 11 ]"
kiem "checkpoint.log không có LỖI"             "! grep -q 'LỖI' checkpoint.log"

echo "=== $P đạt, $F lỗi ==="
[ "$F" -eq 0 ]
SH
chmod +x "$DICH/kiem-hien-vat.sh"
```

**CHECKPOINT 12 — hiện vật đầy đủ.**

```bash
bash "$DICH/kiem-hien-vat.sh" && echo "CHECKPOINT 12 — ĐẠT" || echo "CHECKPOINT 12 — LỖI"
cd "$PORTFOLIO"
git add 04-rules-va-workflow
git commit -q -m "buoi 04: rules va workflow — bang chan tri, pipeline trung, t0 bat bien"
git push -q 2>/dev/null || echo "chưa cấu hình remote cho portfolio"
```

**Dọn dẹp:**

```bash
source ~/lab04/cong-cu.sh
# Đóng MR, xoá schedule, xoá biến project, huỷ job đang chờ
curl -sf --request PUT "${H[@]}" "$A/merge_requests/$MR_IID?state_event=close" >/dev/null 2>&1
for s in $(curl -sf "${H[@]}" "$A/pipeline_schedules" | jq -r '.[].id'); do
  curl -sf --request DELETE "${H[@]}" "$A/pipeline_schedules/$s" >/dev/null
done
curl -sf --request DELETE "${H[@]}" "$A/variables/CHE_DO" >/dev/null 2>&1
for j in $(curl -sf "${H[@]}" "$A/jobs?scope[]=pending&scope[]=running&scope[]=manual&per_page=100" | jq -r '.[].id'); do
  curl -sf --request POST "${H[@]}" "$A/jobs/$j/cancel" >/dev/null
done
curl -sf --request DELETE "${H[@]}" "$A/artifacts" >/dev/null
rm -f /tmp/thu-tu-sai.yml /tmp/thu-tu-dung.yml /tmp/rules-va-only.yml /tmp/gi.yml
echo "đã dọn"
```

---

## L9. Xử lý sự cố thường gặp trong lab

| Triệu chứng | Nguyên nhân | Cách khắc phục |
|---|---|---|
| Tạo `pipeline_schedules` báo 403 | Token thiếu quyền, hoặc vai trò dưới Maintainer | **Đường B**: bỏ nguồn `schedule`, điền `-` vào dòng đó và ghi rõ lý do; CHECKPOINT 1 chỉ cần 5/6 |
| `day_nhanh` trả `KHONG-CO` | Pipeline chưa kịp tạo trong 6 giây, hoặc `workflow` chặn | Tăng `sleep` lên 10; nếu là `workflow` chặn thì đó là **kết quả đúng** ở bước 5 |
| Tạo MR báo `branch not found` | Chưa push nhánh nguồn lên trước | Push nhánh rồi mới tạo MR; thứ tự trong §L3.3 đã đúng |
| Không thấy pipeline trùng ở bước 2 | MR đã đóng, hoặc GitLab đã cấu hình sẵn `workflow` mặc định | Kiểm MR còn `opened`; và đảm bảo chưa thêm `workflow` vào tệp |
| CHECKPOINT 5 vẫn thấy trùng | Khối `workflow` bị đặt **trong** một job thay vì cấp trên cùng | `workflow` là **khoá cấp trên cùng** (buổi 03 QT 4.1); kiểm bằng `lint` |
| CHECKPOINT 6: hai job cùng trạng thái | Nhánh đang chạy không phải nhánh chính | Bước 3 phải chạy trên `main`; kiểm `git branch --show-current` |
| CHECKPOINT 7 trả `valid: true` | Phiên bản này đã đổi hành vi | **Ghi lại kèm phiên bản** — đó là dữ liệu, không phải lỗi bài lab |
| Job `r5-changes-src` **không** chạy trên nhánh mới | Phiên bản này xử lý mốc so sánh khác | Ghi vào `changes-sai.md` kèm phiên bản; kết luận đảo lại và nêu rõ |
| CHECKPOINT 10 hai giá trị bằng nhau | Phiên bản này đã hợp nhất hai mặc định | Ghi lại — đây là **phát hiện**, và nó củng cố lời khuyên "khai tường minh" |
| CHECKPOINT 11 `job_sau_RETRY` = `CO` | Retry đã tạo pipeline mới thay vì chạy lại pipeline cũ | Kiểm id pipeline sau retry; nếu id đổi thì đó là pipeline mới, không phải retry |
| Bước 5 vẫn tạo pipeline dù `so_job = 0` | Còn job khác sót lại trong tệp | Kiểm `lint | jq '.jobs[].name'`; tệp ở §L7.2 phải thay **toàn bộ** |
| Đoạn `python3` ở §L5.1 báo lỗi | Không có `python3`, hoặc đường dẫn `$USER` khác | Nối tệp bằng tay: `cat /tmp/thu-tu-sai.yml >> .gitlab-ci.yml` rồi sửa tên job |
| Quá nhiều pipeline làm chậm GitLab lab | Bước 1 và 2 sinh 15–20 pipeline | Bình thường. Dọn artifact ở §L8; nếu chậm thì `docker restart lab-gitlab` |
| Muốn làm lại từ đầu | — | `curl -X DELETE "${H[@]}" "$A"` rồi chạy lại §L3.1 |

---

## L10. Bài tập mở rộng

### BT1. Mở rộng bảng chân trị lên 6 × 8

Thêm ba rule nữa: `exists: [Dockerfile]`, `if: $CI_MERGE_REQUEST_TARGET_BRANCH_NAME == "main"`, và một rule kết hợp `if` + `changes`.

**Câu hỏi:** ô nào của ba rule mới làm bạn bất ngờ? Rule kết hợp `if` + `changes` khớp khi nào — cả hai đúng hay chỉ một?

### BT2. `workflow` cho repo có nhánh release

Viết `workflow` cho repo có `main`, các nhánh `release/*`, nhánh tính năng, và tag.

**Câu hỏi:** bạn cần mấy quy tắc? Thứ tự nào? Kiểm bằng bảng chân trị 6 nguồn — có ô nào bị bỏ sót không?

### BT3. `changes:compare_to` sửa được ca nào

Thêm `compare_to: refs/heads/main` vào `r5-changes-src` và đo lại cả ba ca của QT 6.3.

**Câu hỏi:** nó sửa được mấy ca? Ca còn lại cần gì? (Buổi 22 trả lời.)

### BT4. Gate biến mất im lặng

Viết một job "quét bảo mật" giả (chỉ `echo`) với `rules:changes: [src/**/*]`, rồi đẩy một commit chỉ sửa `docs/`.

**Câu hỏi:** gate có chạy không? Pipeline màu gì? Viết một job **khẳng định** (buổi 01 QT 7.3) làm pipeline **đỏ** khi gate vắng mặt.

### BT5. `needs:optional` đổi ô

Dựng ca của QT 7.3: job build chỉ chạy trên tag, job đóng gói `needs` nó — thử cả hai bản có và không có `optional: true`.

**Câu hỏi:** bản nào không tạo được pipeline? Bản nào tạo được nhưng nguy hiểm hơn, và vì sao?

### BT6. Đếm pipeline trùng trên repo thật

Chạy đoạn đếm pipeline theo SHA trên một repo thật của đội mình.

**Câu hỏi:** bao nhiêu phần trăm commit có pipeline trùng? Quy ra phút runner một tháng là bao nhiêu?

### BT7. `variables` trong `rules`

Một mục `rules` có thể mang theo `variables`. Viết một job đặt `MOI_TRUONG` khác nhau tuỳ nhánh.

**Câu hỏi:** biến ấy được đặt ở `t0` hay lúc job chạy? Nó có ghi đè biến cấp project không? (Buổi 06 trả lời đầy đủ.)

### BT8. Bảng chân trị thành công cụ

Viết một script nhận `.gitlab-ci.yml` và in ra bảng "job nào có mặt ở nguồn nào", dùng `ci/lint` với tham số `ref`.

**Câu hỏi:** `ci/lint` có mô phỏng được mọi nguồn kích hoạt không? Nguồn nào nó **không** mô phỏng được, và vì sao?

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| Hạng mục | Điểm | Tiêu chí |
|---|---|---|
| `bang-chan-tri.tsv` — ≥5 nguồn × 5 rule + 4 câu trả lời | **6** | Đây là hiện vật chính. Thiếu cột `CI_PIPELINE_SOURCE` đo được thì trừ 2 |
| `pipeline-trung.tsv` — trước/sau `workflow` + 3 câu trả lời | 4 | Phải có phép quy đổi ra **phút runner một tháng** (câu 2) |
| `thu-tu-rule.md` — hai thứ tự, hai kết quả | 3 | Phải giải thích bằng QT 6.1, không chỉ ghi kết quả |
| `changes-sai.md` — kết quả đo + 3 câu trả lời | 4 | Câu 3 (ô của bảng hai thuộc tính cho job security) là câu chấm chính |
| `ba-trang-thai.md` — bảng 3 trạng thái, 6 cột | 4 | Phải có cột "có trong `pipelines/:id/jobs` không" và cột "chặn job sau" |
| `manual-allow-failure.tsv` — 2 cách viết + phiên bản + 3 câu trả lời | 3 | Thiếu phiên bản GitLab thì hạng mục này **0 điểm** |
| `t0-bat-bien.md` — kết luận QT 4.1 và QT 4.3 | 3 | Phải có cả ba giá trị: trước / sau retry / pipeline mới |
| `checkpoint.log` — 12 dòng, không có `LỖI` | 2 | Chạy lại một checkpoint bất kỳ phải ra `ĐẠT` |
| **Tổng** | **29** | Đạt ≥ 18, đạt tốt ≥ 23 |

**Điểm trừ** — dẫn chiếu Bẫy hay gặp của `01-ly-thuyet.md` §9:

| Lỗi | Trừ |
|---|---|
| `checkpoint.log` ghi ĐẠT nhưng chạy lại ra LỖI | **Trần điểm 1 cho cả bài** |
| Kết luận "job không khớp rule thì nó `skipped`" — bẫy 3 | −5 |
| Kết luận "`rules` được đánh giá lại khi retry" — bẫy 1 | −5 |
| `bang-chan-tri.tsv` chép từ tài liệu thay vì đo (dấu hiệu: thiếu cột `CI_PIPELINE_SOURCE` thật) | −4 |
| `manual-allow-failure.tsv` thiếu phiên bản GitLab | −3 |
| Không dọn MR, schedule, biến project ở §L8 | −2 |
| Nộp ảnh chụp màn hình thay kết quả API | **Trần điểm 1** cho hạng mục đó |

**Mức 3 của rubric buổi** đạt được khi: hoàn thành ≥ 3 bài BT của §L10 kèm câu trả lời; **hoặc** làm BT4 (gate biến mất im lặng) và nộp job khẳng định chạy được; **hoặc** làm BT6 trên repo thật và nộp phần trăm commit có pipeline trùng kèm quy đổi phút runner.

---

## Bảng đối soát thời lượng

| Bước | Nội dung | Thời lượng |
|---|---|---|
| L3 | Bước 1 — Bảng chân trị: 6 nguồn kích hoạt × 5 rule | 30' |
| L4 | Bước 2 — Pipeline trùng và `workflow` chuẩn | 30' |
| L5 | Bước 3 — Thứ tự rule; `rules` so `only`; `changes` sai ở nhánh mới | 30' |
| L6 | Bước 4 — Ba trạng thái "không chạy"; `manual` hai mặc định | 30' |
| L7 | Bước 5 — `t0` bất biến: retry và pipeline rỗng | 20' |
| L8 | Nộp sản phẩm và dọn dẹp | 10' |
| **Tổng** | | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---



**Quy tắc cho giảng viên:**

- Chọn **5–7 câu** trong 12, ưu tiên câu 🔥.
- **Gọi ngẫu nhiên.** Trả lời **bằng miệng, không nhìn tài liệu**.
- Ba câu hỏi chen vào, đã thành phản xạ của khoá: **"bao nhiêu?"** (buổi 01), **"sửa ở tệp nào?"** (buổi 02), **"cái đó đi qua đường nào trong bốn đường?"** (buổi 03).
- Buổi này thêm câu thứ tư, và nó là câu quan trọng nhất của giai đoạn 1: **"cái đó quyết định ở `t0` hay sau `t0`?"**

**Thang điểm mỗi câu:**

| Điểm | Nghĩa |
|---|---|
| 0 | Không trả lời được, hoặc sai cơ chế |
| 1 | Nhắc được tên khái niệm, không nêu cơ chế |
| 2 | Nêu đúng cơ chế |
| 3 | Đúng cơ chế **và** một con số, hoặc **và** một ca nó không đúng |

**Hai lỗi làm trần điểm cả buổi là 1:**

1. **Nói `rules` được đánh giá lại mỗi lần job sắp chạy.** Đây là hiểu sai luận đề của cả buổi, và nó dẫn tới hàng loạt quyết định thiết kế sai — đặc biệt là dùng biến `dotenv` trong `rules`.
2. **Nói job không khớp rule thì nó `skipped`.** Hai trạng thái này khác nhau ở việc **có chặn job sau không**, nên nhầm chúng làm chẩn đoán sai hoàn toàn.

**Bốn câu phân loại thật:**

| Câu | Phân loại điều gì |
|---|---|
| 2 | Phân loại người **hiểu trục thời gian**. Người chưa hiểu sẽ đề xuất "thì đặt biến sớm hơn" |
| 6 | Phân loại người **phân biệt biến mất với `skipped`**. Đây là chỗ tách người đã đọc API với người chỉ nhìn giao diện |
| 7 | Phân loại người **từng bị `changes` cắn**. Người chưa gặp sẽ nói "`changes` tiện lắm, tiết kiệm thời gian" |
| 12 | Phân loại **tư duy hệ thống**: có quy trình trả lời hay đoán từng ca |

---

## V2. Bộ câu hỏi


<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q01</span>
    <span>rules` được đánh giá lúc nào?</span>
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
  **Đúng một lần, lúc pipeline được tạo** — gọi thời điểm ấy là `t0`. Danh sách job của pipeline chốt tại đó và **không gì đổi được nó sau đó**.

Cơ chế: GitLab dựng pipeline như một **đối tượng tĩnh**. Nó phân giải tệp, đánh giá `workflow`, đánh giá `rules` của từng job, rồi ghi vào cơ sở dữ liệu một danh sách job cố định cùng quan hệ giữa chúng. Runner sau đó chỉ **lấy job từ danh sách ấy**. Không có bước nào đánh giá lại `rules`.

Ba hệ quả kiểm chứng được:

1. Sửa một biến ở giao diện rồi bấm **retry** một job — `rules` **không** được đánh giá lại, job vẫn như cũ.
2. Retry cả pipeline cũng không làm job đã biến mất xuất hiện lại; phải tạo **pipeline mới**.
3. Sửa `.gitlab-ci.yml` rồi retry pipeline cũ — nó vẫn dùng tệp của commit cũ.

Ở lab tôi đo bằng ba giá trị: job vắng mặt trước khi đổi biến, vắng mặt **sau retry**, và **có mặt** ở pipeline mới tạo với cùng biến ấy.

**Tiêu chí chấm:**
- 0đ: "Mỗi lần job sắp chạy." **Trần điểm cả buổi là 1.**
- 1đ: Biết là lúc tạo pipeline, không nêu hệ quả.
- 2đ: Nêu đúng `t0` và ít nhất một hệ quả.
- 3đ: Như trên, **và** nêu được phép đo ba giá trị (trước / sau retry / pipeline mới).

**Câu hỏi đào sâu:** Vậy muốn đổi danh sách job thì làm gì? *(Tạo pipeline mới — push commit mới, hoặc gọi API `POST /projects/:id/pipeline`. Retry không đủ.)*
</div>
</details>

---

### Câu 2 — ★★★

**Hỏi:** Job A sinh biến `PHIEN_BAN` qua `artifacts:reports:dotenv`. Job B có `rules:if: '$PHIEN_BAN =~ /^v/'`. Job B chạy không?

**Đáp án chuẩn:** **Không chạy** — và tệ hơn, nó **biến mất khỏi pipeline** chứ không phải bị `skipped`.

Lý do là hệ quả trực tiếp của câu 1: `rules` chạy ở `t0`; `dotenv` sinh giá trị ở `t1..tn`, tức **sau** `t0`. Lúc GitLab đánh giá `rules` của job B thì job A còn chưa tồn tại, `PHIEN_BAN` là chuỗi rỗng, biểu thức không khớp, job B không được thêm vào pipeline.

Buổi 01 QT 5.4 nói `dotenv` là **cơ chế duy nhất** truyền một giá trị từ job này sang job sau — điều đó vẫn đúng, nhưng nó hoạt động **trong** pipeline, không **trước** khi pipeline tồn tại.

Chỉ **hai** loại biến dùng được trong `rules`:

| Dùng được | Ví dụ |
|---|---|
| Biến hệ thống của GitLab | `$CI_COMMIT_BRANCH`, `$CI_PIPELINE_SOURCE`, `$CI_COMMIT_TAG` |
| Biến khai **trước** `t0` | Biến instance/group/project, `variables:` trong tệp, biến nhập tay |

Cách làm đúng: dùng biến có ở `t0` để quyết định **chạy hay không**, rồi dùng biến `dotenv` **bên trong `script`** — kèm một khẳng định `test -n "$PHIEN_BAN" || exit 1` theo buổi 01 QT 7.3.

**Tiêu chí chấm:**
- 0đ: "Có, vì job A chạy trước."
- 1đ: Đoán đúng là không chạy, không giải thích được.
- 2đ: Nêu đúng cơ chế `t0` so `t1`.
- 3đ: Như trên, **và** nêu hai loại biến dùng được, **và** đưa được cách làm đúng kèm khẳng định.

**Câu hỏi đào sâu:** Nếu thật sự cần quyết định dựa trên thứ sinh lúc chạy thì làm sao? *(Pipeline động — job đầu **sinh ra** một tệp `.gitlab-ci.yml` con rồi `trigger` nó. Khi ấy `t0` của pipeline con nằm sau khi job đầu chạy xong. Buổi 09 xử lý.)*

---

### Câu 3 — 🔥

**Hỏi:** Kể ba cách làm một job không chạy. Chúng khác nhau thế nào?

**Đáp án chuẩn:** Ba cách cho **ba trạng thái khác nhau**, và chúng khác nhau ở hai điều: có xuất hiện trong pipeline không, và có chặn job sau không.

| Trạng thái | Nguyên nhân | Có trong danh sách job | Bấm chạy được | Chặn job sau |
|---|---|---|---|---|
| **Không có mặt** | `rules` không khớp | **Không** | Không | **Không** |
| **`manual`** | `when: manual` | Có | **Có** | Tuỳ `allow_failure` |
| **`skipped`** | Job trước đỏ | Có | Không | Có |

Một câu hỏi phân biệt cả ba: ***"nó có trong danh sách job không?"*** Không có → `rules`. Có mà chờ người bấm → `manual`. Có mà xám → `skipped`.

Chỗ khác nhau về **thời điểm quyết định** cũng đáng nói: `rules` quyết định ở `t0`; `manual` quyết định lúc pipeline đang chạy; `skipped` quyết định khi job trước thực thi xong.

Cách kiểm bằng API — và điểm quan trọng là job "không có mặt" **không xuất hiện** trong kết quả, chính sự vắng mặt ấy là bằng chứng:

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs" \
| jq -r '.[] | "\(.name)\t\(.status)"'
```

**Tiêu chí chấm:**
- 0đ: Chỉ kể được một cách.
- 1đ: Kể được ba cách, không phân biệt được hệ quả.
- 2đ: Nêu đủ ba trạng thái và bảng khác biệt.
- 3đ: Như trên, **và** nêu câu hỏi phân biệt duy nhất, **và** nói thêm về trục thời gian của ba cách.

**Câu hỏi đào sâu:** Trạng thái nào nguy hiểm nhất và vì sao? *(**Không có mặt** — vì nó không chặn gì và không có gì báo. Nếu job biến mất là một **gate security** thì gate ấy biến mất im lặng, pipeline xanh, và không ai biết bước quét đã không chạy.)*

---

### Câu 4 — ★★★

**Hỏi:** Mở một merge request và thấy hai pipeline chạy cho cùng một commit. Vì sao, và chặn ở đâu?

**Đáp án chuẩn:** Vì **hai sự kiện khác nhau cùng xảy ra**: git nhận một push (nguồn `push`) và merge request thấy nhánh nguồn đổi (nguồn `merge_request_event`). Nếu không có gì loại bớt, GitLab tạo pipeline cho **cả hai** — cùng tập job, cùng commit, cùng kết quả.

Chặn ở tầng **`workflow`**, không phải ở `rules` của từng job. Đây là hai tầng lọc độc lập:

| Tầng | Từ khoá | Quyết định |
|---|---|---|
| 1 | `workflow:rules` | **Cả pipeline** có được tạo không |
| 2 | `rules` của job | **Từng job** có mặt không |

`workflow` được đánh giá **trước**; nếu nó không cho qua thì `rules` của các job không được đánh giá lần nào.

Quy tắc chặn:

```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH
```

Điểm để đạt 3 điểm — thứ tự: quy tắc `when: never` phải nằm **sau** quy tắc MR, vì `rules` dừng ở khớp đầu tiên (QT 6.1). Đảo lại thì nó chặn luôn cái ta muốn giữ.

Con số: **2 pipeline cho 1 commit** = gấp đôi phút runner. Với 40 commit/tuần trên nhánh có MR và mỗi pipeline 6 phút, đó là khoảng **960 phút runner một tháng** cho một repo.

**Tiêu chí chấm:**
- 0đ: "Chắc GitLab lỗi."
- 1đ: Biết là do hai nguồn khác nhau.
- 2đ: Nêu đúng cơ chế và biết chặn bằng `workflow`.
- 3đ: Như trên, **và** giải thích được **thứ tự** quy tắc, **và** quy đổi ra phút runner.

**Câu hỏi đào sâu:** Kiểm bằng số thế nào? *(Nhóm pipeline theo `sha` qua API và đếm: `jq 'group_by(.sha) | map(select(length > 1)) | length'`. Tỉ số pipeline/commit lớn hơn 1 là bằng chứng.)*

---

### Câu 5 — ★★

**Hỏi:** `rules` là một danh sách. GitLab xét nó thế nào?

**Đáp án chuẩn:** Duyệt **từ trên xuống**, dừng ở **điều kiện khớp đầu tiên**, lấy `when`, `allow_failure`, `variables` của điều kiện đó rồi **dừng hẳn**. Các điều kiện sau **không** được xét. Nếu duyệt hết mà không điều kiện nào khớp thì job **không được thêm vào pipeline**.

Đây là mô hình `case`, không phải mô hình "tập hợp điều kiện" — nên **thứ tự quyết định kết quả**.

Bốn loại điều kiện, kết hợp được trong một mục:

| Loại | Xét cái gì |
|---|---|
| `if` | Biểu thức trên biến có ở `t0` |
| `changes` | Tệp nào thay đổi so với **mốc so sánh** |
| `exists` | Tệp có tồn tại trong repo không |
| `when` | Không phải điều kiện — nó là **kết quả** |

Quy tắc thực hành: **viết điều kiện riêng trước, điều kiện chung sau**. Ca kinh điển làm sai:

```yaml
# SAI — rule chung nằm trước, rule manual KHÔNG BAO GIỜ được xét
rules:
  - if: $CI_COMMIT_BRANCH
  - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    when: manual
```

**Tiêu chí chấm:**
- 0đ: "Nó xét hết rồi lấy kết quả tổng hợp."
- 1đ: Biết là xét theo thứ tự.
- 2đ: Nêu đúng "dừng ở khớp đầu tiên" và biết không khớp gì thì job biến mất.
- 3đ: Như trên, **và** nêu quy tắc "riêng trước chung sau" kèm ví dụ sai.

**Câu hỏi đào sâu:** Kiểm thứ tự có đúng không mà không cần đẩy commit? *(Gọi `ci/lint` rồi đọc `when` của job sau phân giải — buổi 03 QT 4.3. 1 giây thay cho một vòng đẩy-chờ 3–5 phút.)*

---

### Câu 6 — ★★★

**Hỏi:** Job không khớp rule nào. Nó có trong pipeline không? Nó có chặn job sau không?

**Đáp án chuẩn:** **Không có trong pipeline**, và **không chặn** gì cả.

Phân biệt quan trọng: `skipped` là một **trạng thái** của một job **đang có** trong pipeline — nó có id, có trang riêng, hiện màu xám, và nó chặn job sau theo quy tắc thông thường. Job bị `rules` loại thì **không được tạo ra**: không có id, không có trang, không xuất hiện trong `GET /pipelines/:id/jobs`.

Bằng chứng đo được: đếm số job trong `pipelines/:id/jobs` và so với số job trong tệp — chênh lệch chính là số job đã biến mất. Và kiểm thêm rằng **không có job nào ở trạng thái `skipped`** trong pipeline đó.

Hệ quả thực hành, và đây là phần đạt 3 điểm: nếu job biến mất là một **gate security**, thì gate ấy biến mất **im lặng và không chặn gì** — pipeline xanh, không có cảnh báo, không ai biết bước quét đã không chạy. Đây là ô nguy hiểm nhất của bảng hai thuộc tính.

Cách chống: một job riêng **khẳng định** rằng các gate bắt buộc đã có mặt trong pipeline, theo buổi 01 QT 7.3. Buổi 35 xử lý đầy đủ.

Ghi chú thêm: `when: never` và "không khớp rule nào" cho **cùng** kết quả — nên dòng `- when: never` ở cuối danh sách rules thường là thừa.

**Tiêu chí chấm:**
- 0đ: "Nó `skipped`." **Trần điểm cả buổi là 1.**
- 1đ: Biết nó không chạy nhưng không phân biệt được với `skipped`.
- 2đ: Nêu đúng "biến mất, không chặn" và cách kiểm bằng API.
- 3đ: Như trên, **và** nêu hệ quả với job gate security, **và** nêu cách chống bằng job khẳng định.

**Câu hỏi đào sâu:** Job sau nó có `needs` trỏ vào nó thì sao? *(Không có `optional`: pipeline **không tạo được** — ồn ào, có chặn. Có `optional: true`: pipeline tạo được nhưng job chạy mà **thiếu artifact** — im lặng, không chặn. Một cờ đổi ô của bảng hai thuộc tính.)*

---

### Câu 7 — ★★★

**Hỏi:** `rules:changes` có vẻ tiện: chỉ chạy job khi thư mục liên quan thay đổi. Nó sai ở đâu?

**Đáp án chuẩn:** `changes` cần một **mốc so sánh**, và câu "tệp nào đã đổi" chỉ có nghĩa khi có hai điểm để so. Với pipeline merge request, GitLab so với nhánh đích — đúng. Với pipeline nhánh, nó so với commit trước trên cùng nhánh — và **ba ca** làm phép so ấy sai:

| Ca | Chuyện gì | Hệ quả |
|---|---|---|
| **Nhánh mới tạo** | Không có commit trước trên nhánh này | GitLab coi **mọi tệp đều đổi** → job chạy hết, kể cả job không cần |
| **Pipeline theo lịch** | Không có commit mới | Không tệp nào "đổi" → job `changes` **không chạy lần nào** |
| **Push nhiều commit một lần** | So với commit trước push, không xét từng commit | Đúng về tổng thể, sai nếu muốn xét từng commit |

`changes:compare_to: refs/heads/main` sửa được **2** ca đầu. Ca thứ ba cần **pipeline động** — buổi 22.

Ô của bảng hai thuộc tính: **im lặng, không chặn** ở cả ba ca.

Kết luận thực hành để đạt 3 điểm: **đừng dùng `rules:changes` cho job security.** Hậu quả không đối xứng — một gate chạy thừa tốn vài chục giây; một gate **biến mất im lặng** thì không ai biết, và pipeline vẫn xanh. Với job security, chấp nhận chạy thừa.

**Tiêu chí chấm:**
- 0đ: "Nó ổn mà, tôi vẫn dùng."
- 1đ: Biết là có vấn đề với mốc so sánh.
- 2đ: Kể được ít nhất hai ca và biết `compare_to`.
- 3đ: Kể đủ ba ca, **và** nói `compare_to` sửa được 2, **và** nêu kết luận về job security kèm lập luận bất đối xứng.

**Câu hỏi đào sâu:** Ca "nhánh mới tạo" hay xảy ra tới mức nào? *(Rất hay — mỗi tính năng mới là một nhánh mới. Trong monorepo, nó nghĩa là commit đầu tiên của mọi nhánh đều build **toàn bộ** service. Buổi 22 đo con số đó.)*

---

### Câu 8 — ★★

**Hỏi:** `workflow` khác `rules` ở chỗ nào?

**Đáp án chuẩn:** Khác ở **tầng** mà chúng chặn.

| | `workflow:rules` | `rules` của job |
|---|---|---|
| Chặn ở tầng | **Pipeline** | **Job** |
| Không qua thì | Không có pipeline nào được tạo | Job không có mặt |
| Đánh giá lúc nào | **Trước** | Sau |
| Khai ở đâu | Khoá cấp trên cùng | Trong từng job |

Hai tầng **độc lập** và **cả hai** phải cho qua thì job mới chạy.

Giá trị chẩn đoán, và đây là phần đạt 3 điểm: khi một job không chạy, câu hỏi đầu tiên là ***"có pipeline nào được tạo không?"***. Không có pipeline → vấn đề ở tầng 1, sửa `rules` của job là vô ích, có thể mất nửa giờ. Có pipeline mà thiếu job → vấn đề ở tầng 2.

**Tiêu chí chấm:**
- 0đ: "Giống nhau, chỉ khác chỗ đặt."
- 1đ: Biết `workflow` ở cấp trên cùng.
- 2đ: Nêu đúng hai tầng và thứ tự đánh giá.
- 3đ: Như trên, **và** nêu giá trị chẩn đoán "có pipeline nào không" như câu hỏi đầu tiên.

**Câu hỏi đào sâu:** `workflow` nên có bao nhiêu quy tắc? *(Khoảng năm — đủ phủ sáu nguồn kích hoạt. Nhiều hơn thường là dấu hiệu nên chuyển sang pipeline động (buổi 09) thay vì nhồi thêm điều kiện, vì mỗi quy tắc thêm vào là một ô mới trong bảng chân trị phải kiểm.)*

---

### Câu 9 — ★★★

**Hỏi:** `when: manual` viết trong `rules` và viết trực tiếp ở cấp job — có khác nhau không?

**Đáp án chuẩn:** **Có** — khác ở **mặc định của `allow_failure`**. Trong `rules`, `when: manual` mặc định `allow_failure: true`; khai trực tiếp thì mặc định `false`.

Lý do lịch sử: trong `rules`, GitLab coi `manual` là "một lựa chọn, không bắt buộc" nên mặc định cho phép bỏ qua. Khai trực tiếp thì giữ ngữ nghĩa cũ — job này là một bước bắt buộc, chờ người bấm.

Hệ quả thực tế nhìn thấy được: khi **không ai bấm nút**, pipeline hiển thị `success` với cách viết thứ nhất, và `blocked` với cách viết thứ hai. Cùng một job deploy, hai cách viết, hai màu pipeline khác nhau — và người ta thường không để ý cho tới khi có ai hỏi "sao pipeline này chưa xong".

Cách kiểm — **đo bằng API, không nhìn giao diện**, vì giao diện vẽ hai job giống hệt nhau:

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs" \
| jq -r '.[] | "\(.name)\tallow_failure=\(.allow_failure)"'
```

Điểm để đạt 3 điểm: đây là **đại lượng phải đo**, không tra tài liệu — hành vi đã đổi giữa các phiên bản. Và quy tắc thực hành rút ra là **luôn khai `allow_failure` tường minh** cho job manual, đừng dựa vào mặc định.

**Tiêu chí chấm:**
- 0đ: "Giống nhau."
- 1đ: Biết có khác nhau, không nêu được khác gì.
- 2đ: Nêu đúng khác biệt về `allow_failure` và hệ quả lên màu pipeline.
- 3đ: Như trên, **và** nói rõ đây là thứ phải đo kèm ghi phiên bản, **và** nêu quy tắc khai tường minh.

**Câu hỏi đào sâu:** Vì sao không nhìn giao diện được? *(Giao diện vẽ job manual giống hệt nhau ở cả hai cách viết — cùng biểu tượng, cùng nút bấm. Chỉ trường `allow_failure` trong API mới phân biệt được, và nó là thứ quyết định màu pipeline.)*

---

### Câu 10 — ★★★

**Hỏi:** Job B có `needs: [job-a]`, nhưng `job-a` bị `rules` loại. Chuyện gì xảy ra?

**Đáp án chuẩn:** **Pipeline không tạo được.** GitLab không dựng được đồ thị phụ thuộc khi một `needs` trỏ vào job không tồn tại, nên nó từ chối tạo pipeline và báo lỗi rõ ràng.

Ô của bảng hai thuộc tính: **ồn ào, có chặn** — đây là ô **rẻ nhất**, phát hiện trong vài giây.

Thêm `needs: [{job: job-a, optional: true}]` thì GitLab bỏ qua ràng buộc khi `job-a` vắng mặt. Pipeline tạo được, job B chạy — **nhưng không có artifact của `job-a`**. Và vì nhiều lệnh không báo lỗi khi tệp thiếu, job B có thể **vẫn xanh** với hiện vật rỗng.

Đây là ca hiếm mà **một cờ đổi ô của bảng hai thuộc tính**:

| Cấu hình | Ô |
|---|---|
| `needs: [job-a]` | **Ồn ào, có chặn** — pipeline không tạo được |
| `needs: [{job: job-a, optional: true}]` | **Im lặng, không chặn** — job chạy thiếu artifact |

Tức là cờ `optional: true` chuyển lỗi từ ô rẻ nhất sang ô đắt nhất. Nó không phải "sửa lỗi" — nó là **ẩn lỗi**.

Kết luận thực hành để đạt 3 điểm: chỉ dùng `optional: true` khi job tiêu thụ đã có **khẳng định** riêng kiểm hiện vật, theo buổi 01 QT 7.3:

```yaml
script:
  - test -s dist/app.js || { echo "KHANG DINH HONG: thieu artifact"; exit 1; }
```

**Tiêu chí chấm:**
- 0đ: "Job B chạy bình thường."
- 1đ: Biết là có vấn đề.
- 2đ: Nêu đúng cả hai ca — có và không có `optional`.
- 3đ: Như trên, **và** nói rõ `optional` **đổi ô** của bảng hai thuộc tính từ rẻ sang đắt, **và** nêu điều kiện dùng nó kèm khẳng định.

**Câu hỏi đào sâu:** Vậy khi nào `optional: true` là đúng? *(Khi phụ thuộc thật sự là tuỳ chọn — ví dụ một job tải artifact **nếu có** để tăng tốc, nhưng vẫn chạy được nếu không có. Và ngay cả khi đó, phải có khẳng định phân biệt hai đường đi.)*

---

### Câu 11 — ★★★

**Hỏi:** Bạn push code lên nhưng không thấy pipeline nào xuất hiện. Chẩn đoán thế nào?

**Đáp án chuẩn:** Hai giả thuyết, và cả hai đều là ô **im lặng, có chặn**:

**Giả thuyết A — `workflow` chặn cả pipeline.** Không quy tắc nào của `workflow` khớp với nguồn kích hoạt này.

**Giả thuyết B — mọi job đều bị `rules` loại.** Pipeline không còn job nào, và GitLab **không tạo pipeline rỗng**: **0 job → 0 pipeline**.

Phân biệt bằng `ci/lint`:

```bash
curl -sf --request POST --header "PRIVATE-TOKEN: $TOKEN" \
  --header "Content-Type: application/json" \
  --data "$(jq -Rs '{content: ., ref: "main"}' < .gitlab-ci.yml)" \
  "$GITLAB/api/v4/projects/$PID/ci/lint" \
| jq -r '"valid=\(.valid)  so_job=\((.jobs//[])|length)"'
```

Nếu `so_job == 0` → giả thuyết B. Nếu có job mà vẫn không có pipeline → giả thuyết A.

Giả thuyết thứ ba cần loại trừ trước cả hai: **tệp `.gitlab-ci.yml` có lỗi cú pháp** — khi đó `valid: false` và GitLab tạo một pipeline **failed** ngay lập tức, chứ không phải không tạo gì.

Điểm để đạt 3 điểm: nói rõ đây là ca **im lặng** — không có pipeline nghĩa là không có gì để mở, không có log để đọc, và thông báo thật nằm ở một dòng nhỏ trong giao diện hoặc ở API. Người mới thường nghĩ GitLab hỏng hoặc runner chết, và đi tìm ở chỗ hoàn toàn khác.

**Tiêu chí chấm:**
- 0đ: "Chắc runner chết."
- 1đ: Đoán được là do `rules` hoặc `workflow`.
- 2đ: Nêu đúng hai giả thuyết và cách phân biệt bằng `ci/lint`.
- 3đ: Như trên, **và** loại trừ được giả thuyết thứ ba (lỗi cú pháp cho ra pipeline failed, không phải không có pipeline), **và** nêu vì sao ca này im lặng.

**Câu hỏi đào sâu:** Vì sao GitLab không tạo pipeline rỗng? *(Vì một pipeline không có job nào thì không có gì để báo cáo — nó sẽ luôn "thành công" mà không làm gì, và đó là tín hiệu sai. Nhưng cái giá là ca này im lặng, và đó là đánh đổi mà người dùng phải biết.)*

---

### Câu 12 — 🔥

**Hỏi:** Đồng nghiệp hỏi "sao job này không chạy?". Bạn trả lời thế nào?

**Đáp án chuẩn:** Có **quy trình bốn bước**, không đoán từng ca.

**Bước 1 — có pipeline nào được tạo không?** Không có → vấn đề ở tầng `workflow` hoặc **0 job → 0 pipeline**; sửa `rules` của job là vô ích. Đây là câu hỏi đầu tiên vì nó loại được một nửa không gian giả thuyết trong 5 giây.

**Bước 2 — job có trong danh sách job không?**

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" ".../pipelines/$PIPE/jobs" | jq -r '.[].name'
```

Không có → `rules` không khớp, job **biến mất**. Có → sang bước 3.

**Bước 3 — nó ở trạng thái nào?** `manual` (chờ người bấm) hay `skipped` (job trước đỏ)? Ba trạng thái, ba nguyên nhân, ba cách sửa.

**Bước 4 — nếu là `rules` không khớp, tra bảng chân trị.** Nguồn kích hoạt là gì, và ô tương ứng trong bảng nói gì? Có bảng thì trả lời trong 10 giây; không có bảng thì mỗi lần lại là một vòng thử sai 4 phút.

Hai điều cần nói thêm để đạt 3 điểm:

- **Kiểm bằng `ci/lint` trước khi đẩy commit** — nó cho tệp sau phân giải và cho biết job nào tồn tại, mất 1 giây.
- **Nhớ `t0`**: nếu `rules` của job đó dùng một biến sinh bởi job khác thì nó **không bao giờ** khớp, và không có cách sửa nào trong `rules` — phải chuyển sang pipeline động.

**Tiêu chí chấm:**
- 0đ: "Xem lại `rules` thôi."
- 1đ: Biết đọc `rules`.
- 2đ: Nêu được quy trình có thứ tự, ít nhất ba bước.
- 3đ: Đủ bốn bước, **và** nêu `ci/lint` như bước phòng ngừa, **và** nêu ca `t0` không sửa được trong `rules`.

**Câu hỏi đào sâu:** Nếu job đó là gate security thì câu hỏi của bạn đổi thế nào? *(Đổi từ "sao nó không chạy" sang **"nó đã không chạy bao nhiêu lần rồi mà không ai biết"** — vì gate biến mất là ô im lặng không chặn. Và câu trả lời phải kèm một job khẳng định để lần sau nó ồn ào.)*

---

## V3. Câu chốt để nói khi phỏng vấn

> Bốn câu viết **nguyên văn, đúng ngữ điệu nói**. Mỗi câu chứa một con số hoặc một cơ chế.

**Câu 1 — khi được hỏi "bạn hiểu `rules` thế nào":**

> "Điều quan trọng nhất về `rules` là nó được đánh giá đúng một lần, lúc pipeline được tạo — không phải lúc job sắp chạy. Danh sách job chốt tại thời điểm đó và không gì đổi được nữa. Hệ quả trực tiếp là biến sinh bởi một job khác, kiểu `dotenv`, không dùng được trong `rules` — lúc `rules` chạy thì job kia còn chưa tồn tại. Tôi đã đo chuyện này: đổi một biến cấp project rồi retry, job vẫn vắng mặt; tạo pipeline mới với đúng biến đó thì job xuất hiện."

**Câu 2 — khi được hỏi "job không chạy thì bạn làm gì":**

> "Tôi hỏi hai câu theo thứ tự. Thứ nhất: có pipeline nào được tạo không — nếu không thì vấn đề ở `workflow` hoặc mọi job đều bị loại, và sửa `rules` của job là vô ích. Thứ hai: job đó có trong danh sách job không — nếu không có thì nó **biến mất**, chứ không phải `skipped`. Hai trạng thái đó khác nhau ở chỗ `skipped` chặn job sau còn biến mất thì không, nên nhầm chúng là chẩn đoán sai hoàn toàn."

**Câu 3 — khi được hỏi về tối ưu chi phí CI:**

> "Việc rẻ nhất tôi làm là thêm khối `workflow`. Không có nó, một commit trên nhánh đang có merge request sinh hai pipeline — một từ nguồn push, một từ nguồn merge request — cho cùng một commit và cùng kết quả. Với bốn mươi commit một tuần và pipeline sáu phút, đó là gần một nghìn phút runner một tháng cho một repo, mà mọi thứ vẫn xanh nên không ai để ý. Tôi đo bằng cách nhóm pipeline theo SHA và đếm."

**Câu 4 — khi được hỏi về `rules:changes`:**

> "Tôi không dùng `changes` cho job security. Lý do là nó cần một mốc so sánh, và mốc mặc định sai ở ba ca: nhánh mới tạo thì GitLab coi mọi tệp đều đổi nên job chạy hết; pipeline theo lịch thì không tệp nào đổi nên job không chạy lần nào; và push nhiều commit một lần thì nó so với trước push chứ không xét từng commit. `compare_to` sửa được hai ca đầu. Nhưng với gate bảo mật thì hậu quả không đối xứng: chạy thừa tốn vài chục giây, còn biến mất im lặng thì pipeline vẫn xanh và không ai biết bước quét đã không chạy."

---

## V4. Bảng ghi điểm

| Học viên | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | Tổng | Trần điểm? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | |

**Quy đổi:**

| Tỉ lệ điểm | Kết luận |
|---|---|
| ≥ 80% | Nắm vững. Giao BT4 (gate biến mất im lặng) làm trước buổi 35 |
| 60–79% | Đạt. Đọc lại quy tắc bị mất điểm trước buổi 05 |
| 40–59% | Chưa đạt. Làm lại bước lab tương ứng ở nhà |
| < 40% | Chưa đạt. Học lại cả buổi — buổi 12 và 22 dựng thẳng lên bảng chân trị này |

**Bảng lỗi làm trần điểm là 1:**

| Lỗi | Vì sao nghiêm trọng |
|---|---|
| "`rules` được đánh giá lại mỗi lần job sắp chạy" | Hiểu sai luận đề cả buổi; dẫn tới thiết kế dùng biến `dotenv` trong `rules`, vốn không bao giờ chạy |
| "Job không khớp rule thì nó `skipped`" | Hai trạng thái khác nhau ở việc **có chặn job sau không**; nhầm chúng là chẩn đoán sai hoàn toàn |
| Nói định lượng mà khi hỏi lại vẫn không có số | Vi phạm nguyên tắc của khoá |

---

## V5. Bài tập về nhà

### BTVN 1. Đếm pipeline trùng trên repo thật

Chạy đoạn đếm pipeline theo SHA trên một repo thật của đội mình:

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/projects/$PID/pipelines?per_page=100" \
| jq -r 'group_by(.sha) | map(select(length > 1)) | length as $n | "\($n) commit có pipeline trùng"'
```

**Nộp:** con số, tỉ lệ phần trăm trên tổng commit, và quy đổi ra **phút runner một tháng**.

### BTVN 2. Bảng chân trị cho repo thật

Lập bảng chân trị cho repo của mình: sáu nguồn kích hoạt × ba job quan trọng nhất.

**Nộp:** bảng 18 ô, điền bằng **đo** chứ không đoán. Ghi rõ ô nào bạn chưa kích hoạt được và vì sao.

### BTVN 3. Kiểm gate security

Với mọi job security/gate trong repo của mình, kiểm `rules` của nó: có ca nào làm nó **biến mất** không? Đặc biệt tìm `rules:changes`.

**Nộp:** danh sách job gate kèm cột "có nguy cơ biến mất ở nguồn nào". Với mỗi job có nguy cơ, viết một dòng đề xuất sửa.

### BTVN 4. Chuẩn bị cho buổi 05

Trả lời ba câu sau bằng viết, mỗi câu 3–5 dòng. Mang theo vào buổi 05.

1. Buổi 01 QT 5.2 nói `cache` **không** được đảm bảo tồn tại. Hãy đoán: `cache:key` được **tính** lúc nào — ở `t0` như `rules`, hay lúc job chạy? Ghi phỏng đoán kèm lập luận.
2. Nếu một job sinh artifact **biến mất** vì `rules` không khớp, job sau cần artifact đó sẽ ra sao? Trả lời cho **cả hai** ca: có `needs` và không có `needs`. (Gợi ý: hôm nay QT 7.3 đã trả lời một nửa.)
3. Liệt kê **ba** thư mục trong dự án của bạn nên đi bằng `cache` và **ba** thư mục nên đi bằng `artifacts`. Với mỗi thư mục, ghi một câu lý do dựa trên buổi 01 QT 5.2.

**Ba câu này dẫn vào đâu:** câu 1 dẫn vào §4 buổi 05 về **thời điểm tính `cache:key`** — và câu trả lời nối thẳng vào trục `t0` của hôm nay; câu 2 dẫn vào §5 buổi 05 về `dependencies` so `needs` khi job nguồn vắng mặt; câu 3 dẫn vào §6 buổi 05, nơi khoá học chốt **bảng phân loại thư mục** dùng lại ở toàn bộ giai đoạn 3 (buổi 15–22, mỗi ngôn ngữ một chiến lược cache).
{% endraw %}
