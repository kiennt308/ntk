---
layout: post
title: "[Bài 07] Kỹ Thuật Gỡ Rối & Chẩn Đoán Pipeline: CI_DEBUG_TRACE, Log Analysis, Runner Interactive Debug & SSH Debug"
date: 2026-09-07 08:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-07
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 7
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.07] Hướng dẫn chuyên sâu Kỹ Thuật Gỡ Rối & Chẩn Đoán Pipeline: CI_DEBUG_TRACE, Log Analysis, Runner Interactive Debug & SSH Debug: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

{% raw %}
# [BÀI 07] KỸ THUẬT GỠ RỐI & CHẨN ĐOÁN PIPELINE: CI_DEBUG_TRACE, LOG ANALYSIS, RUNNER INTERACTIVE DEBUG & SSH DEBUG

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · executor `docker`.
> Mọi đoạn YAML dán được vào `.gitlab-ci.yml` và chạy trong dưới 60 giây, trừ hai đoạn cố ý vượt hạn giờ ở §6.
> Lệnh `curl` dùng bốn biến đã có từ buổi 01: `$GITLAB`, `$GITLAB_TOKEN`, `$PID`, `$PIPE`.
> **Buổi này khép lại giai đoạn 1.** Nó không thêm khái niệm lớn nào mới — nó gom sáu buổi trước thành một quy trình dùng được lúc 2 giờ sáng.

---





Gọi ngẫu nhiên, mỗi câu 1 phút. Ai sai câu 4 sẽ tắc ở lab ca 2; ai sai câu 3 sẽ bật `CI_DEBUG_TRACE` sai chỗ ở §8.

| # | Câu hỏi | Đáp án vắn tắt | Dẫn vào đâu hôm nay |
|---|---|---|---|
| 1 | Có mấy nguồn biến, mấy nguồn nằm ngoài repo | **9** nấc; **4** nấc cao nhất nằm ngoài repo (buổi 06 QT 4.1) | §4 — hàng "biến" của bảng thu hẹp: bốn nấc ngoài repo là lý do phải **đo** chứ không đọc YAML |
| 2 | "Sửa YAML không có tác dụng" là ca gì | Nấc **2** (project) thắng nấc **7** (YAML cấp trên cùng) (buổi 06 QT 4.2) | §4 QT 4.3 — cùng một trạng thái `failed` có thể là lỗi của hai đội khác nhau, y như vậy |
| 3 | `masked` che gì, không che gì | Che **log**; **3** đường lộ: artifact, giá trị bị biến đổi, giao diện (buổi 06 QT 5.1) | §8 phần "KHÔNG nên dùng" — vì sao `CI_DEBUG_TRACE` là bước **cuối**, không phải bước đầu |
| 4 | Biến `protected` thiếu thì job ra sao | Độ dài **0**, **không** lỗi; chặn bằng `: "${VAR:?}"` (buổi 06 QT 5.2) | Lab ca 2 — ca "xanh mà không triển khai gì", ô *biến × pha 4–5* |
| 5 | `$VAR` của biến kiểu file là gì | Là **đường dẫn**; nội dung ở `$(cat $VAR)` (buổi 06 QT 6.1) | §4 QT 4.2 — bằng chứng phải là lệnh in ra được, `${#VAR}` và `cat` là hai lệnh đó |



Sáu buổi vừa qua học viên đã dựng đủ đồ nghề nhưng chưa có **quy trình**. Buổi 01 cho tám pha và bốn đường vào; buổi 02 cho biên giới `config.toml`; buổi 03 cho stage và ba khối lệnh; buổi 04 cho `t0`; buổi 05 cho artifact và cache; buổi 06 cho chín nấc biến. Mỗi buổi giải một lớp lỗi. Chưa buổi nào trả lời câu hỏi thật của người trực ca: *"pipeline đỏ, tôi làm gì trong ba mươi giây đầu?"*

Hôm nay trả lời câu đó, và trả lời bằng cách nối hai trục **đã có sẵn từ buổi 01** thành một mặt phẳng.

**Luận đề trung tâm.**

> **Gỡ rối CI không phải thử lại cho tới khi xanh. Nó là THU HẸP VÙNG NGHI NGỜ trên hai trục đã có sẵn từ buổi 01: BỐN đường dữ liệu vào job, và TÁM pha của một job. Bốn nhân tám là ba mươi hai ô; mỗi bằng chứng đọc được bằng một lệnh sẽ loại bỏ hàng loạt ô cùng lúc, và một pipeline hỏng bất kỳ quy về đúng một ô.**

**Bảng thu hẹp — ba mươi hai ô.** Trục ngang là **tám pha** của buổi 01 QT 4.2, gộp thành bốn cột cho vừa trang; trục dọc là **bốn đường vào** của buổi 01 QT 5.1. Bốn hàng nhân tám pha là **32 ô**. Không ô nào mới: cả ba mươi hai ô đều đã đi qua trong sáu buổi trước.

```
   BẢNG THU HẸP — mọi pipeline hỏng nằm ở một ô

                    │ pha 1–3      │ pha 4–5      │ pha 6        │ pha 7–8
                    │ chuẩn bị     │ nguồn+dữ liệu│ script       │ dọn+tải lên
   ─────────────────┼──────────────┼──────────────┼──────────────┼──────────────
   mã nguồn (git)   │ clone hỏng   │ ref sai      │ —            │ —
   cache            │ —            │ trượt, im    │ —            │ nén hỏng
   artifacts        │ —            │ 404 / rỗng   │ —            │ upload rỗng
   biến             │ runner thiếu │ rỗng, im     │ mở rộng sai  │ —

   Bằng chứng nào cũng phải là MỘT LỆNH in ra được:
     failure_reason → loại bỏ theo cột · trace theo pha → loại bỏ theo cột
     ${#VAR} · artifacts 404 · dòng trượt cache → loại bỏ theo hàng
```

Điểm phải nêu rõ với lớp: bảng này **không** phải danh sách mọi cách hỏng. Nó là khung phân loại để thu hẹp — mỗi ô còn nhiều nguyên nhân con, và có một lớp sự cố nằm hẳn ngoài bảng (§8 phần cuối).

**Kết quả buổi trước được dùng lại.** Đây là buổi thu hoạch, nên bảng này dài hơn mọi buổi trước: **mọi công cụ của sáu buổi đều tụ vào đây**.

| Kết quả | Nguồn | Dùng ở đâu hôm nay |
|---|---|---|
| Tám pha của một job | buổi 01 QT 4.2 | §4 — **trục dọc** của bảng thu hẹp; đây là **lần thứ 4** |
| Bốn đường dữ liệu vào job | buổi 01 QT 5.1 | §4 — **trục ngang** của bảng thu hẹp; **lần thứ 4** |
| `after_script` chạy trong shell mới, có hạn giờ riêng | buổi 01 QT 4.3 | §6 QT 6.3 — **lần thứ 2** |
| Job `pending` vô hạn vì `tags` không khớp, không ai báo | buổi 02 QT 6.3 | §6 QT 6.2 và lab ca 3 — **lần thứ 2** |
| Ranh giới `.gitlab-ci.yml` / `config.toml` | buổi 02 QT 4.1, 4.3 | §6 QT 6.1 — timeout đến từ **cả hai** tệp |
| Ba khối lệnh, hai shell | buổi 03 QT 6.1 | §4 — pha 6 chia làm ba đoạn con trong log |
| Job biến mất vì `rules`; `needs` trỏ job vắng mặt | buổi 04 QT 6.2, 7.3 | Lab ca 4 |
| Artifact rỗng mà job xanh; artifact thắng cache | buổi 05 QT 5.3, 7.2 | Lab ca 1 và ca 5 |
| `doc-pha.sh` đọc `trace` qua API | buổi 05 lab B4 | §4 QT 4.2 — hôm nay mở rộng thành `go-roi.sh` |
| Biến `protected` rỗng, `${VAR:?}` | buổi 06 QT 5.2 | Lab ca 2 |
| `CI_DEBUG_TRACE` và cái giá của nó | buổi 06 QT 7.2 | §4 — công cụ cuối cùng, không phải công cụ đầu tiên |
| Bảng hai thuộc tính hỏng | buổi 01 QT 7.1 | §4, §5, §7 — **lần thứ 7**, và hôm nay nó thành **cột của báo cáo gỡ rối** |

**Nguyên lý xuất hiện lần thứ mấy.** Giảng viên **nói ra con số** để lớp thấy đây là đồ nghề dùng lại, không phải khẩu hiệu:

- **Bảng hai thuộc tính hỏng** — **lần thứ 7**. Hôm nay nó đổi vai: từ bảng phân loại thành **một cột trong báo cáo gỡ rối**, vì câu "hỏng này im lặng hay ồn ào" quyết định việc tiếp theo là sửa code hay dựng cảnh báo.
- **Tám pha** — **lần thứ 4**. Lần này chúng là **trục** của một bảng, không còn là danh sách phải học thuộc.
- **Bốn đường vào** — **lần thứ 4**. Cũng vậy: từ danh sách thành trục.
- **"Phụ thuộc phiên bản thì phải ĐO, không tra"** — **lần thứ 7**. Hôm nay đại lượng phải đo là **hạn giờ riêng của `after_script`** (§6 QT 6.3).
- **"Job xanh không chứng minh gì"** — **lần thứ 5**. Ca lab số 5 là ca **không có gì đỏ** mà bản triển khai vẫn sai.

**Ba câu hỏi trung tâm của buổi:**

1. Trước khi đọc một dòng log nào, tôi trả lời được câu "hỏng ở ô nào trong ba mươi hai ô" bằng mấy lệnh?
2. `retry` sửa được nhóm lỗi nào — và với nhóm nào thì nó chỉ nhân chi phí lên ba lần?
3. Vì sao hai pipeline deploy cùng lúc là một lỗi **im lặng**, và một dòng cấu hình nào chặn nó?

**Ba câu BTVN 4 của buổi 06 dẫn thẳng vào ba mục.** Gọi ba học viên đọc phỏng đoán đã ghi, **không sửa ngay**, ghi lên bảng để đối chiếu cuối buổi: câu 1 (chia log theo tám pha) → §4 QT 4.1; câu 2 (`retry` có sửa được biến rỗng không) → §5 QT 5.1; câu 3 (một pipeline hỏng viết theo mẫu bốn dòng) → §7 QT 7.3 và sáu báo cáo của lab.

---



| # | Làm được gì | Hiện vật chứng minh |
|---|---|---|
| LĐ1 | Chỉ ra một job hỏng ở **pha nào** trong tám pha, kèm số giây từng pha, bằng **1** lệnh | `go-roi.sh` chạy trên job thật — lab bước 1 CHECKPOINT 1 |
| LĐ2 | Đọc `failure_reason` cho **cả** pipeline và quy nó về **4** nhóm quy trách nhiệm | Bảng một trang, lab bước 1 CHECKPOINT 2 |
| LĐ3 | So hai lần chạy (một xanh, một đỏ) và chỉ ra **dòng thứ mấy** log bắt đầu khác | `diff lan-xanh.txt lan-do.txt`, lab bước 3 |
| LĐ4 | Viết được **báo cáo bốn dòng** cho một sự cố, dòng thứ hai là một lệnh | `bao-cao-go-roi.md` — **6** báo cáo, lab bước 2 và 3 |
| LĐ5 | Nói ra job 90 giây với `retry: 2` tốn bao nhiêu giây và thêm mấy phần trăm cơ hội | Đo qua API, lab bước 4 CHECKPOINT 9 |
| LĐ6 | Tính được hạn giờ **thật** đang áp cho một job từ **3** nguồn | So `GET /runners/:id` · `timeout` job · cấu hình project, lab bước 4 |
| LĐ7 | Phân biệt job `pending` với job treo bằng **1** trường JSON | `jq '.runner'`, lab bước 2 ca 3 |
| LĐ8 | Chặn deploy chồng nhau bằng **1** dòng và chứng minh hai job không chồng thời gian | So `started_at`/`finished_at`, lab bước 5 CHECKPOINT 11 |

---



| Cần biết | Mức yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Tám pha của một job và dòng tiêu đề từng pha trong log | **Vận dụng** | buổi 01 QT 4.2 — trục dọc của cả buổi |
| Bốn đường vào một job | **Vận dụng** | buổi 01 QT 5.1 — trục ngang của cả buổi |
| Bảng hai thuộc tính hỏng: im lặng/ồn ào × chặn/không chặn | **Vận dụng** | buổi 01 QT 7.1 |
| `after_script` là shell khác, có hạn giờ riêng | Vận dụng | buổi 01 QT 4.3 |
| `tags` là cơ chế định tuyến duy nhất; job không khớp thì `pending` | **Vận dụng** | buổi 02 QT 6.3 |
| Ranh giới `.gitlab-ci.yml` với `config.toml` | Vận dụng | buổi 02 QT 4.1, 4.3 |
| Artifact rỗng mà job vẫn xanh; artifact thắng cache | Vận dụng | buổi 05 QT 5.3, 7.2 |
| Biến rỗng không phải lỗi; `: "${VAR:?}"` | Vận dụng | buổi 06 QT 5.2 |
| `curl` + `jq`, đọc `trace` qua API, viết script bash ngắn | **Bắt buộc** | buổi 05 lab B4 (`doc-pha.sh`) — hôm nay mở rộng nó |

---



### 3.1. Đối chiếu thuật ngữ

Từ khoá YAML và tên trường API **giữ nguyên tiếng Anh**, vì học viên gõ đúng chữ đó vào tệp cấu hình hoặc vào `jq`. Khái niệm khác dùng tiếng Việt, kèm tiếng Anh để đi phỏng vấn.

| Tiếng Việt dùng trong bài | Tiếng Anh | Dùng thẳng tiếng Anh trong thân bài? |
|---|---|---|
| log job dạng văn bản | job trace | **Có** — `trace` |
| lý do thất bại | failure reason | **Có** — `failure_reason` |
| chạy lại tự động | retry | **Có** — `retry` |
| chạy lại bằng tay | manual retry | Việt |
| hạn giờ | timeout | **Có** — `timeout` |
| job treo | stuck job | Việt |
| job chờ runner | pending job | **Có** — `pending` |
| huỷ được giữa đường | interruptible | **Có** — `interruptible` |
| huỷ pipeline dư | auto-cancel redundant pipeline | Việt |
| nhóm tài nguyên loại trừ | resource group | **Có** — `resource_group` |
| loại trừ lẫn nhau | mutual exclusion | Việt |
| thu hẹp vùng nghi ngờ | narrowing the search | Việt |
| bằng chứng | evidence | Việt |
| lỗi xác định | deterministic failure | Việt |
| lỗi chập chờn | flaky failure | Việt |
| mã thoát | exit code | Việt |
| dấu vết gỡ rối | debug trace | **Có** — `CI_DEBUG_TRACE` |



Bốn đường vào nhân tám pha bằng **32 ô**. Giá trị thực dụng không nằm ở con số 32 mà ở cách nó bị chia: **mỗi bằng chứng loại bỏ một hàng hoặc một cột, không loại bỏ từng ô một**. Đọc `failure_reason` loại bỏ theo cột; đo `${#VAR}` loại bỏ theo hàng. Hai lệnh là còn lại vài ô.

Đây là lý do người có mô hình gỡ nhanh hơn người thử-và-sai không phải chút ít mà một bậc: thử-và-sai đi từng ô, mỗi vòng mất một lần đẩy commit cộng thời gian pipeline. Mô hình này quay lại ở buổi **13**, **14**, **22** và **47**.

### 3.3. Mô hình tư duy 2: lỗi xác định so với lỗi chập chờn

Phép thử gọn nhất của cả buổi: **chạy lại hai lần**. Hai kết quả khác nhau thì là lỗi chập chờn — mạng, tài nguyên máy, thời điểm. Hai kết quả giống nhau thì là lỗi xác định, và mọi thứ dựa trên việc chạy lại đều vô nghĩa với nó.

Giá trị đo được: phép thử này tốn hai lần chạy job, thường 2–4 phút, và nó quyết định thẳng việc `retry` là công cụ đúng hay là cái làm ta trả tiền ba lần cho cùng một tin xấu. Quay lại ở buổi **14**, **30**, **33**, **47**.

### 3.4. Mô hình tư duy 3: chờ khác treo

`pending` nghĩa là **chưa runner nào nhận** job (buổi 02 QT 6.3). Hết hạn giờ nghĩa là **đã có runner nhận rồi mà không tiến triển**. Hai chuyện này ở hai phía đối diện của pha 1, và hai cách sửa không có điểm nào chung: một bên sửa `tags`/thêm runner, một bên đi tìm việc gì đang treo trong `script`.

Trên giao diện chúng trông giống nhau — cùng là "pipeline chạy mãi không xong". Trường phân biệt là `runner`: `null` hay có id. Quay lại ở buổi **13** và **47**.

### 3.5. Mô hình tư duy 4: báo cáo bốn dòng

Một cuộc gỡ rối xong khi viết được bốn dòng: **triệu chứng → bằng chứng (một lệnh) → nguyên nhân → cách sửa**. Dòng thứ hai là dòng duy nhất không được viết bằng văn xuôi.

Vì sao ép đúng bốn dòng: dài hơn thì không ai đọc lại, ngắn hơn thì mất dòng bằng chứng — và mất dòng bằng chứng nghĩa là ba tháng sau người khác phải điều tra lại từ đầu. Mẫu này là hiện vật nộp của rất nhiều buổi sau: **28**, **35**, **46**, **47**, **48**.

---

### 1.1. Đọc log có phương pháp: ba mươi hai ô (10 phút)

Bốn lệnh đầu tiên của mọi cuộc gỡ rối, theo đúng thứ tự: (1) `failure_reason` của mọi job trong pipeline; (2) `trace` của job hỏng tải về tệp; (3) chia `trace` theo tám pha; (4) `diff` với lần xanh gần nhất. Ba quy tắc dưới đây là ba lệnh 1–3; lệnh 4 nằm trong QT 4.2.

**Nguyên lý cốt lõi:** Log job **có cấu trúc**: nó chia theo tám pha của buổi 01 QT 4.2 (lần thứ 4), và mỗi pha có một dòng tiêu đề nhận dạng được. Định vị đúng pha hỏng loại bỏ **bảy trong tám** nhóm nguyên nhân trước khi đọc bất kỳ dòng lỗi nào.

**Giải thích cơ chế ngầm:** Runner in tên pha ra `trace` ngay khi bắt đầu pha đó. Vì thứ tự tám pha là cố định, **vị trí của dòng lỗi so với các dòng tiêu đề** là dữ liệu chứ không phải cảm nhận: dòng tiêu đề cuối cùng xuất hiện *trước* dòng lỗi cho biết chính xác lỗi thuộc pha nào. Từ pha suy ra nhóm nguyên nhân là phép tra bảng — bảng tám dòng ở buổi 01 §4.1. Đây là phát biểu loại (a), lấy từ tài liệu Runner 17.x; tên pha **đã đổi giữa các bản runner**, nên lab đo lại trên log thật.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Người gỡ rối dán dòng lỗi cuối cùng vào ô tìm kiếm mà không biết dòng đó thuộc pha nào, rồi sửa `script` cho một lỗi thuộc pha 2. Dấu hiệu nhận ra trong 5 giây: log **không có** dòng `Executing "step_script" stage of the job script` thì `script` chưa chạy lần nào, và mọi phút bỏ vào sửa `script` là phút bỏ đi.

**Minh hoạ.**

```bash
# go-roi.sh, phần 1 — bảng ba cột: pha · dòng bắt đầu · số giây của pha.
# Mở rộng từ doc-pha.sh của buổi 05 lab B4. Chạy: ./go-roi.sh <JOB_ID>
JOB_ID="$1"
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB_ID/trace" > /tmp/trace-$JOB_ID.txt

grep -anE 'Preparing the|Preparing environment|Getting source|Restoring cache|Downloading artifacts|Executing "step_script"|Running after_script|Saving cache|Uploading artifacts|Cleaning up|Job succeeded|Job failed' \
  /tmp/trace-$JOB_ID.txt \
| awk -F: 'NR>1{printf "%-6s %-6s %s\n", p, $1-pl, t} {pl=$1; p=$1; t=substr($0, index($0,$2))}
           END{printf "%-6s %-6s %s\n", p, "-", t}' \
| sed '1i DONG   SO_DONG PHA'
```

**Con số chốt.** **8** pha; **1** pha hỏng; **7/8** giả thuyết bị loại bỏ bằng một lệnh. Chi phí lệnh này khoảng **2 giây** một lần gọi API, thay cho 10–20 phút đọc log bằng mắt.

**Nguyên lý cốt lõi:** `trace` lấy qua API là **văn bản thuần**: `grep` được, `wc` được, so sánh hai lần chạy được. Giao diện web không cho ta cả ba việc đó. Vì vậy công cụ đầu tiên của buổi này là một lệnh `curl`, không phải một cú nhấp chuột.

**Giải thích cơ chế ngầm:** Giao diện làm ba việc cùng lúc: thu gọn phần dài, tô màu bằng mã ANSI, và tải lười phần cuối log. Cả ba đều phá việc so sánh cơ học giữa lần xanh và lần đỏ — thứ duy nhất trả lời được câu "cái gì đã đổi". Endpoint `GET /projects/:id/jobs/:job_id/trace` trả về đúng byte mà runner đã gửi lên, nên `diff` trên nó là phép so sánh có thật. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hai người nhìn cùng một job và kể lại log khác nhau. Hoặc: không ai chỉ ra được **dòng thứ mấy** log bắt đầu khác nhau giữa lần xanh và lần đỏ, nên cuộc thảo luận chuyển sang "chắc là do..." trong 20 phút.

**Minh hoạ.**

```bash
# Hai lệnh thay cho việc đọc 400 dòng bằng mắt.
for pair in "do:$JOB_DO" "xanh:$JOB_XANH"; do
  ten="${pair%%:*}"; id="${pair##*:}"
  curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/jobs/$id/trace" \
  | sed 's/\x1b\[[0-9;]*[a-zA-Z]//g' > "lan-$ten.txt"     # bỏ mã màu ANSI
done
diff lan-xanh.txt lan-do.txt | head -20
echo "dòng đầu tiên khác nhau: $(diff lan-xanh.txt lan-do.txt | grep -m1 -oE '^[0-9]+')"
```

**Con số chốt.** **1** lệnh `curl` + **1** lệnh `diff` thay cho việc đọc **400** dòng bằng mắt. Một `trace` điển hình của job build 5 phút nằm ở bậc 300–800 dòng; `wc -l` trên hai tệp là phép kiểm rẻ nhất xem lần đỏ có đi được xa bằng lần xanh không.

**Nguyên lý cốt lõi:** Bước 0 của mọi cuộc gỡ rối là đọc `failure_reason` của job qua API, vì nó phân loại nguyên nhân theo **nền tảng** trước khi ta phán xét theo mã nguồn: lỗi `script`, lỗi hạ tầng runner, hết hạn giờ, và mất artifact là **bốn nhóm khác nhau** cần bốn người khác nhau xử lý.

**Giải thích cơ chế ngầm:** Trên giao diện, cả bốn nhóm đều hiện đúng một chữ `failed`. `failure_reason` là trường duy nhất phân biệt được chúng mà **không** phải đọc log, và nó do runner báo về chứ không do ai suy đoán. Bốn nhóm ứng với bốn người: `script_failure` → tác giả commit; `runner_system_failure` và `runner_unsupported` → đội hạ tầng; `job_execution_timeout` và `stuck_or_timeout_failure` → chủ pipeline (§6); `missing_dependency_failure` và `archived_failure` → chủ job sinh artifact (buổi 05). Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Một vé được chuyển qua lại giữa hai đội hai ngày, trong khi `failure_reason` đã ghi `runner_system_failure` ngay từ đầu. Dạng nhẹ hơn, gặp hằng tuần: người ta sửa `script` cho một job mà `failure_reason` là `stuck_or_timeout_failure` — job đó không hỏng vì code, nó hỏng vì chưa kịp xong.

**Minh hoạ.**

```bash
# Bảng một trang cho CẢ pipeline — lệnh đầu tiên của mọi cuộc gỡ rối
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?per_page=100" \
| jq -r '.[] | [.name, .status, (.failure_reason // "-"), (.duration // 0 | floor),
                (.queued_duration // 0 | floor), (.runner.id // "chua-nhan")]
         | @tsv' \
| sed '1i JOB\tTRANG_THAI\tFAILURE_REASON\tGIAY\tCHO_GIAY\tRUNNER' | column -t
```

**Con số chốt.** **4** nhóm quy trách nhiệm; **1** lệnh `jq` cho cả pipeline. Trong lab, sáu ca hỏng cho ra sáu giá trị `failure_reason` khác nhau — riêng ca 4 cho ra **không có gì**, vì pipeline không được tạo (buổi 04 QT 6.2).

---

### 1.2. `retry`: sửa được nhóm nào, che mất nhóm nào (9 phút)

**Nguyên lý cốt lõi:** `retry` chỉ có giá trị với **lỗi chập chờn**. Với lỗi xác định — mã sai, biến rỗng, artifact rỗng — nó không thêm một phần trăm cơ hội nào và nhân thời gian cùng phút runner lên **`retry` + 1** lần. Phép thử phân biệt: chạy lại hai lần, nếu hai kết quả giống nhau thì đừng đặt `retry`.

**Giải thích cơ chế ngầm:** Cùng một đầu vào, cùng một `image`, cùng một `script`, cùng một môi trường dùng một lần (buổi 01 QT 4.1) thì cho cùng một kết quả. `retry` chỉ đổi được những thứ **không** giống nhau giữa hai lần chạy: mạng, tài nguyên máy chủ runner, và thời điểm. Biến `protected` rỗng thì lần chạy thứ ba vẫn rỗng; `artifacts:paths` trỏ sai thư mục thì lần thứ ba vẫn trỏ sai. Loại (b) — suy ra từ cơ chế môi trường dùng một lần.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job hỏng ba lần liên tiếp với **đúng cùng một** dòng lỗi, và cả đội chờ 4,5 phút thay vì 1,5 phút để nhận cùng một tin. Dấu hiệu trên tệp: `retry: 2` nằm ở một job mà lần hỏng gần nhất có `failure_reason` là `script_failure`.

**Minh hoạ.**

```yaml
# Ca đối chứng của lab bước 4 — job này PHẢI đỏ ba lần, đó là kết quả đúng
loi-xac-dinh:
  image: alpine:3.20
  retry: 2                      # SAI chỗ: lỗi dưới đây hoàn toàn xác định
  script:
    - echo "bắt đầu $(date +%s)"
    - sleep 90
    - exit 1
# Đo tổng chi phí thật của ba lần chạy:
#   curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
#     "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?include_retried=true" \
#   | jq '[.[] | select(.name=="loi-xac-dinh") | .duration] | add | floor'
```

**Con số chốt.** Job 90 giây với `retry: 2` → **270 giây** và **0%** cơ hội thêm. Chênh lệch là **+180 giây** mỗi lần hỏng, trả bằng phút runner và bằng thời gian chờ của người đang đợi kết quả.

**Nguyên lý cốt lõi:** `retry:when` gắn việc chạy lại với **`failure_reason` cụ thể**, và đó là cách duy nhất để `retry` không che mất lỗi thật. `retry` trần trụi không có `when` là một quyết định gần như luôn sai.

**Giải thích cơ chế ngầm:** `when` để nền tảng làm việc phân loại thay ta, ngay tại chỗ, bằng đúng trường của QT 4.3. Mặc định của `retry: 2` là `when: always` — tức mọi giá trị `failure_reason` đều được chạy lại, kể cả `script_failure`. Khai `when` là chuyển từ "chạy lại mọi thứ" sang "chỉ chạy lại nhóm mà chạy lại có nghĩa", và nhóm đó đúng bằng nhóm hạ tầng cộng nhóm hạn giờ. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Biểu đồ "tỉ lệ job phải chạy lại" phẳng ở mức cao trong nhiều tuần mà không ai mở vé hạ tầng, vì mọi lỗi đều bị `retry` nuốt như nhau. Dạng cụ thể hơn: một lỗi test chập chờn thật bị lẫn với một lỗi biên dịch thật, và không ai tách được hai loại vì cả hai đều "xanh ở lần thứ hai".

**Minh hoạ.**

```yaml
# mảnh — dán vào default: để áp cho mọi job, hoặc vào một job cụ thể
default:
  retry:
    max: 2                              # trần của GitLab 17.7
    when:
      - runner_system_failure           # runner chết giữa job — chạy lại có nghĩa
      - stuck_or_timeout_failure        # job bị treo, không tiến triển
      - scheduler_failure               # nền tảng không xếp được job
      - api_failure
      - unknown_failure
    # KHÔNG có script_failure trong danh sách: lỗi code phải đỏ ngay lần đầu
```

**Con số chốt.** `max` tối đa **2** ở GitLab 17.7 — đây là giới hạn của phiên bản, không phải quy luật, và nó đã đổi trong quá khứ. Danh sách `when` có khoảng **12** giá trị; chỉ nhóm hạ tầng và hạn giờ nên có mặt, tức khoảng **5** giá trị.

**Nguyên lý cốt lõi:** `retry` là một cơ chế **che hỏng im lặng**: nó biến sự cố hạ tầng lặp lại thành vô hình vì kết quả cuối cùng vẫn xanh. Vì vậy dùng `retry` thì **bắt buộc** đo tỉ lệ job cần chạy lại, nếu không ta đang trả tiền cho một sự cố mà không ai biết nó tồn tại.

**Giải thích cơ chế ngầm:** Trạng thái **cuối cùng** của job là thứ duy nhất mọi người nhìn: giao diện pipeline, thông báo, huy hiệu trên README. Các lần thất bại trung gian chỉ tồn tại trong dữ liệu API, sau tham số `include_retried=true`, và không nằm trên bảng điều khiển nào. Đây đúng là ô *im lặng + không chặn* của buổi 01 QT 7.1 — **lần thứ 7** ta dùng bảng đó, và lần này nó là cột của báo cáo. Loại (b).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hoá đơn phút runner tăng **30%** trong một tháng mà số pipeline không đổi và không ai giải thích được. Dấu hiệu sớm hơn: thời gian trung vị của một pipeline tăng thêm đúng bậc thời lượng của một job, mà không job nào chậm đi.

**Minh hoạ.**

```bash
# dem-retry.sh — tỉ lệ job phải chạy lại trong N pipeline gần nhất
N="${1:-100}"
for p in $(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
      "$GITLAB/api/v4/projects/$PID/pipelines?per_page=$N" | jq -r '.[].id'); do
  curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/pipelines/$p/jobs?include_retried=true&per_page=100" \
  | jq -r '.[] | "\(.name)"'
done | sort | uniq -c \
| awk '{tong+=$1; if($1>1) lai+=$1-1} END{printf "job chạy: %d · lần chạy lại: %d · tỉ lệ: %.2f%%\n", tong, lai, 100*lai/tong}'
```

**Con số chốt.** Ngưỡng đáng mở vé hạ tầng, **theo kinh nghiệm thực tế**: tỉ lệ job phải chạy lại vượt **2%**. Con số này **không** có nguồn chính thức và không phổ quát — đội có 500 pipeline mỗi ngày và đội có 20 pipeline mỗi ngày không dùng cùng một ngưỡng.

> **Nếu có Ultimate:** Value Streams Dashboard và bộ chỉ số DORA cho sẵn biểu đồ xu hướng theo tuần, nên tỉ lệ chạy lại đọc được mà không cần script. Trên CE thì `dem-retry.sh` cho đúng con số ấy bằng **1** lệnh; bài lab **không** phụ thuộc vào bản có license.

---

### 1.3. `timeout`: ba nguồn, và job treo khác job chờ (8 phút)

**Nguyên lý cốt lõi:** Hạn giờ của một job đến từ **ba** nguồn: cấu hình project, khoá `timeout` của job, và hạn giờ khai trong `config.toml` của runner. Giá trị **nhỏ nhất** thắng, và nguồn thứ ba nằm ngoài repo nên nó là nguồn khó tìm nhất (buổi 02 QT 4.1 — ranh giới hai tệp).

**Giải thích cơ chế ngầm:** Hạn giờ là một hợp đồng giữa hai bên: project nói "tôi cho job này nhiều nhất bao lâu", runner nói "tôi cho job của bất kỳ ai nhiều nhất bao lâu". Bên nào cũng có quyền đặt giới hạn thấp hơn, nên kết quả là **min**. Cụ thể ở Runner 17.7, khoá `[[runners]] output_limit` không liên quan; khoá quyết định là hạn giờ cấu hình cho runner trong giao diện GitLab, và runner còn cắt xuống theo `--timeout`/biến môi trường của tiến trình runner. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job khai `timeout: 3h` mà bị cắt ở phút thứ 60, và trong `.gitlab-ci.yml` không có gì giải thích được. Người sửa đọc lại YAML mười lần rồi kết luận "GitLab bỏ qua `timeout`" — trong khi con số 60 phút nằm ở nơi họ không có quyền đọc.

**Minh hoạ.**

```bash
# Tính hạn giờ THẬT: min của ba nguồn. Đây là lệnh của lab bước 4.
JOB_ID="$1"
JOB_TO=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB_ID" \
  | jq -r '"job=\(.name) runner_id=\(.runner.id // "chua-nhan")"')
PRJ_TO=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID" | jq -r '.build_timeout')   # giây, mặc định 3600
RUN_ID=$(echo "$JOB_TO" | sed 's/.*runner_id=//')
RUN_TO=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/runners/$RUN_ID" | jq -r '.maximum_timeout // "khong-dat"')
echo "$JOB_TO · project=${PRJ_TO}s · runner=${RUN_TO}s → hạn giờ thật = min của ba nguồn"
```

**Con số chốt.** **3** nguồn, thắng theo **min**; mặc định cấp project là **60 phút** (`build_timeout` = 3.600 giây). Con số 60 phút cấu hình được ở Settings → CI/CD → General pipelines, và bị `config.toml` cắt xuống — nên nó là mặc định, không phải sự thật về hệ thống đang chạy.

**Nguyên lý cốt lõi:** `pending` và `stuck` là **hai** trạng thái khác nhau tuy trông giống nhau: `pending` nghĩa là **chưa runner nào nhận** (buổi 02 QT 6.3 — lần thứ 2, nguyên nhân thường là `tags`), còn hết hạn giờ nghĩa là **đã nhận rồi mà không tiến triển**. Câu hỏi phân biệt: job đã có `runner` gán chưa.

**Giải thích cơ chế ngầm:** Hai trạng thái này ở hai phía đối diện của pha 1. Trước pha 1, job nằm trong hàng đợi và chưa có `trace` — vì `trace` chỉ tồn tại sau khi runner nhận job. Sau pha 1, job có `runner.id`, có `trace`, và đồng hồ hạn giờ bắt đầu chạy. Sửa `tags` cho một job đang treo giữa `script` là vô ích, và tăng `timeout` cho một job chưa bao giờ được nhận cũng vô ích. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Người ta thêm runner mới để sửa một job đang treo ở `docker pull`, hoặc nâng `timeout` cho một job chưa runner nào nhận. Dấu hiệu trên dữ liệu: `queued_duration` lớn mà `duration` là `null` — đó là chờ, không phải treo.

**Minh hoạ.**

```bash
# Một lệnh phân biệt chờ với treo cho hai job bất kỳ
for id in "$JOB_A" "$JOB_B"; do
  curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/jobs/$id" \
  | jq -r '"\(.name)\tstatus=\(.status)\trunner=\(.runner.id // "null → CHỜ, sửa tags")" +
           "\tqueued=\(.queued_duration // 0)s\tduration=\(.duration // "null")"'
done
```

**Con số chốt.** **1** trường `runner` phân biệt hai trạng thái. Job `pending` có `duration` = **null**. Với mặc định 60 phút, một job định tuyến sai gây **60 phút im lặng** trước khi có tín hiệu nào — ô *im lặng + có chặn* của buổi 01 QT 7.1.

**Nguyên lý cốt lõi:** `after_script` có hạn giờ **riêng** và ngắn (buổi 01 QT 4.3 — lần thứ 2), nên job hết hạn giờ ở `script` vẫn còn cơ hội chạy `after_script`, còn job hết hạn giờ **trong** `after_script` thì mất bước dọn dẹp, và cái mất đó **im lặng**.

**Giải thích cơ chế ngầm:** Nền tảng cố ý cho `after_script` một đồng hồ riêng, để bước dọn dẹp không bị cắt cùng lúc với `script` — nếu dùng chung đồng hồ thì mọi job hết hạn giờ đều bỏ dở việc dọn, và đó là thiết kế tệ. Nhưng "riêng" cũng có nghĩa là "có thể hết trước khi dọn xong". Đây là phát biểu **loại (c) — phải ĐO** (lần thứ 7 của nguyên lý này trong khoá): giá trị và cả hành vi đã đổi giữa các bản runner, và biến điều khiển nó có ở bản này mà không có ở bản khác. **Tuyệt đối không kết luận từ tài liệu.**

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Container phụ, tệp tạm, hoặc lock còn sót lại sau một job hết hạn giờ, và trong log **không có dòng nào** nói `after_script` bị cắt. Không có thông báo, không có `failure_reason` riêng — chỉ có rác còn lại mà lần chạy sau vấp phải.

**Minh hoạ.**

```yaml
# Hai ca của lab bước 4 — chỉ khác nhau chỗ đặt sleep. PHẢI đo, không tra.
ca-a-script-het-han:
  image: alpine:3.20
  timeout: 2m                    # hạn giờ nhỏ để đo trong 2 phút
  script:
    - echo "MOC-script-bat-dau $(date +%s)"
    - sleep 300                  # vượt hạn giờ → job bị cắt ở đây
  after_script:
    - echo "MOC-after-script-CO-CHAY $(date +%s)"   # dòng này CÓ in ra không?

ca-b-after-script-het-han:
  image: alpine:3.20
  timeout: 10m
  script: [echo "script xong nhanh"]
  after_script:
    - echo "MOC-after-bat-dau $(date +%s)"
    - sleep 400                  # vượt hạn giờ RIÊNG của after_script
    - echo "MOC-after-KET-THUC $(date +%s)"         # dòng này gần như chắc chắn MẤT
```

**Con số chốt.** Giá trị tham chiếu của hạn giờ `after_script` ở Runner 17.7 là **5 phút** — bài lab **phải đo lại**, không được tra. Kết luận đo được ghi vào hiện vật nộp kèm số phiên bản runner; nếu số đo khác 5 phút thì số đo thắng.

---

### 1.4. `interruptible`, `resource_group`, và mẫu báo cáo bốn dòng (7 phút)

**Nguyên lý cốt lõi:** `interruptible: true` cho phép nền tảng huỷ job của pipeline đã lỗi thời khi có commit mới, nhưng **một** job không `interruptible` đang chạy là đủ để phần còn lại của pipeline **không** bị huỷ. Vì vậy giá trị của tính năng này là **nhị phân theo cả pipeline**, không cộng dồn theo từng job.

**Giải thích cơ chế ngầm:** Nền tảng chỉ huỷ một pipeline khi nó chắc rằng mọi việc còn dở đều huỷ được **an toàn**. Job không đánh dấu bị coi là không huỷ được — đó là mặc định bảo toàn, và là mặc định đúng, vì một job deploy bị huỷ giữa đường để lại trạng thái nửa vời. Vì vậy bật cho 9 trong 10 job cho ra **0 giây** tiết kiệm, y như không bật gì. Điều kiện thứ hai, thường bị quên: phải bật tuỳ chọn huỷ pipeline dư trong cấu hình project, nếu không `interruptible` chỉ là một khoá không ai đọc. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bật `interruptible` cho 9 trong 10 job mà phút runner không giảm chút nào, và không ai tìm ra vì sao — vì cái sai không nằm ở 9 job đã bật, nó nằm ở 1 job chưa bật.

**Minh hoạ.**

```yaml
# Khai ở default: cho MỌI job, rồi trừ đúng job deploy — đó là cách duy nhất đúng
default:
  interruptible: true

trien-khai-staging:
  stage: trien-khai
  interruptible: false           # BẮT BUỘC false: huỷ giữa đường để lại trạng thái nửa vời
  resource_group: staging        # xem QT 7.2
  script: [./trien-khai.sh staging]
# Đo: push 3 commit trong 2 phút, rồi đếm job bị huỷ của hai pipeline cũ
#   curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
#     "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?scope=canceled" | jq 'length'
```

**Con số chốt.** Push **3** commit trong 2 phút, pipeline **6** job × **90** giây: tiết kiệm khoảng **2 × 6 × 90 = 1.080 giây** phút runner khi mọi job đều `interruptible`, và **0 giây** khi còn một job không đánh dấu. Con số 1.080 tính cho đúng ca ấy — đổi bất kỳ số nào trong ba số đó thì kết quả đổi theo.

**Nguyên lý cốt lõi:** `resource_group` là **cơ chế loại trừ lẫn nhau duy nhất** của GitLab CI: cùng một tên nhóm thì các job xếp hàng chạy lần lượt thay vì song song. Thiếu nó, hai pipeline deploy cùng lúc và bản thắng là bản **kết thúc sau** — một kết quả không xác định và **im lặng**.

**Giải thích cơ chế ngầm:** Không có gì khác trong `.gitlab-ci.yml` biểu đạt được câu "hai job này không được chạy cùng lúc". `stage` chỉ nói thứ tự **trong** một pipeline (buổi 03 QT 5.1), `needs` cũng vậy — cả hai không nói gì về quan hệ giữa hai pipeline khác nhau. `resource_group` là khoá duy nhất tạo một hàng đợi có tên, ở phạm vi project, cắt ngang mọi pipeline. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Môi trường staging chạy phiên bản của commit **cũ hơn** commit mới nhất đã deploy xong, và lịch sử deploy cho thấy hai lần deploy chồng nhau về thời gian. Không có job nào đỏ, không có cảnh báo nào — đây là **ô nguy hiểm nhất** của bảng hai thuộc tính: im lặng và không chặn.

**Minh hoạ.**

```bash
# Chứng minh hai job cùng resource_group KHÔNG chồng thời gian
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/resource_groups/staging/upcoming_jobs" \
| jq -r '.[] | "dang-cho: \(.name) pipeline=\(.pipeline.id)"'

for id in "$JOB_P1" "$JOB_P2"; do
  curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/jobs/$id" \
  | jq -r '"\(.name)\tbat-dau=\(.started_at)\tket-thuc=\(.finished_at)"'
done
# ĐẠT khi: ket-thuc của job thứ nhất <= bat-dau của job thứ hai
```

**Con số chốt.** **1** dòng cấu hình; **2** pipeline song song thành **1** hàng đợi. Cái giá phải nói ra: thời gian chờ tăng đúng bằng thời lượng của job kia — hai job deploy 30 phút thành 60 phút từ lúc push tới lúc xong.

> **Nếu có Ultimate:** protected environments và deployment approvals cho thêm một lớp kiểm soát ai được deploy vào đâu. Chúng **không** thay `resource_group`: phê duyệt giải bài toán quyền, `resource_group` giải bài toán hai việc chạy cùng lúc. Bài lab dùng CE và không phụ thuộc bản có license.

**Nguyên lý cốt lõi:** Một cuộc gỡ rối chỉ được coi là xong khi viết được **bốn** dòng: triệu chứng · **bằng chứng** · nguyên nhân · cách sửa — trong đó **bằng chứng phải là một lệnh in ra được**, không phải một câu mô tả. Thiếu dòng bằng chứng thì kết luận là phỏng đoán, và nó sẽ được lặp lại bởi người sau.

**Giải thích cơ chế ngầm:** Bằng chứng dạng lệnh là thứ duy nhất người khác **kiểm lại** được sau ba tháng, khi cả pipeline đã đổi. Một câu như "artifact bị rỗng" không kiểm lại được: không biết đo ở đâu, không biết ngưỡng nào là rỗng. Một dòng `curl … | jq '.status'` in ra `404` thì kiểm lại được trong 2 giây, và nếu nó không còn in ra `404` thì ta biết chuyện đã khác. Đây là phát biểu loại (b), và nó cưỡng chế được bằng máy: checkpoint của lab đếm số dòng bắt đầu bằng `$ ` trong báo cáo, không đọc câu văn.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cùng một sự cố xuất hiện lần thứ ba trong sáu tháng và mỗi lần lại được điều tra từ đầu. Dấu hiệu trên văn bản: mọi dòng của báo cáo đều là câu tiếng Việt, không dòng nào là lệnh dán chạy được.

**Minh hoạ.**

```markdown
### Ca 1 — job dong-goi đỏ: không tìm thấy tệp

1. **Triệu chứng.** Job `dong-goi` đỏ ở pha 5, `failure_reason` = `missing_dependency_failure`;
   job `bien-dich` ngay trước đó **xanh**.
2. **Bằng chứng.**
   $ curl -sf -H "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID/jobs/$J_BD" | jq -r .status
   success
   $ curl -s -o /dev/null -w '%{http_code}\n' -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
       "$GITLAB/api/v4/projects/$PID/jobs/$J_BD/artifacts"
   404
3. **Nguyên nhân.** `artifacts:paths` của `bien-dich` trỏ `build/` còn `script` ghi vào `dist/`;
   mẫu không khớp gì nên gói rỗng, pha 8 vẫn thành công (buổi 05 QT 5.3). Ô: *artifacts × pha 4–5*.
4. **Cách sửa.** Sửa `paths` thành `dist/`, và thêm `- test -s dist/app.js || exit 1` ở cuối
   `script` để lần sau lỗi này **ồn ào + có chặn** thay vì im lặng.
```

**Con số chốt.** **4** dòng; **1** lệnh bắt buộc ở dòng thứ hai; **6** báo cáo là hiện vật nộp của buổi. Chi phí viết một báo cáo là 3–5 phút, đổi lấy việc lần sau ai gặp lại ca đó mất 2 phút thay vì 40 phút.

---

### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước

Bốn việc, tổng **40 phút**, xếp theo rủi ro tăng dần. Việc 1 và 2 làm được ngay hôm nay mà không đụng tới ai.

**Việc 1 — 10 phút, rủi ro bằng 0.** Chép `go-roi.sh` vào máy và chạy nó cho **job đỏ gần nhất** của repo mình. Ghi lại đúng hai thứ: pha hỏng và `failure_reason`. Việc này không sửa một dòng nào trong repo.

**Việc 2 — 15 phút, rủi ro thấp.** `grep -n 'retry' .gitlab-ci.yml`. Mọi `retry` **không** có `when` là một chỗ đang che lỗi (QT 5.2). Thêm `when` giới hạn vào nhóm hạ tầng. Thay đổi này chỉ làm pipeline **đỏ sớm hơn**, không làm nó đỏ nhiều hơn.

**Việc 3 — 10 phút, rủi ro trung bình.** Thêm `interruptible: true` vào `default:` và bật huỷ pipeline dư trong cấu hình project; đặt `interruptible: false` cho mọi job deploy **trước khi** bật. Đo phút runner tuần trước và tuần sau.

**Việc 4 — 5 phút, giá trị cao nhất trên mỗi dòng.** Mọi job deploy vào cùng một môi trường phải có `resource_group` cùng tên. Đây là dòng cấu hình rẻ nhất trong cả khoá so với thiệt hại nó chặn.

### Cái gì hỏng nếu áp thẳng lên prod

`interruptible: true` cho một job **đã bắt đầu deploy** làm nó bị huỷ giữa đường và để lại trạng thái nửa vời: một nửa số pod đã đổi image, migration chạy được một nửa. Job deploy phải là job **không** đánh dấu `interruptible` — và điều đó khiến QT 7.1 không cho ta tiết kiệm gì trên pipeline có deploy. Đó là cái giá đúng phải trả, không phải lỗi cấu hình.

Thêm `resource_group` cho một job đang chạy 30 phút biến hai lần deploy song song thành **60 phút** chờ. Đo `duration` của job deploy **trước khi** thêm, để biết mình đang mua gì bằng bao nhiêu phút.

Siết `timeout` xuống thấp làm job build lớn nhất hỏng đúng vào ngày phát hành. Cách an toàn: đo `duration` **lớn nhất trong 30 ngày** rồi cộng 50% biên, đừng lấy trung vị.

```yaml
# mảnh — áp thử trên nhánh riêng trước, không chặn ai
retry-nghiem-ngat:
  extends: test
  allow_failure: true                    # ồn ào nhưng KHÔNG chặn — buổi 01 QT 7.1
  retry: {max: 2, when: [runner_system_failure, stuck_or_timeout_failure]}
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

### Đo trước — đo sau

| # | Chỉ số | Đo bằng | Mục tiêu |
|---|---|---|---|
| 1 | Thời gian trung vị từ lúc job đỏ tới lúc có kết luận nguyên nhân | Ghi tay trong 2 tuần, hoặc dấu thời gian bình luận trên vé | Dưới **10 phút** nhờ bốn lệnh của §4 |
| 2 | Tỉ lệ job phải chạy lại trong 100 pipeline gần nhất | `dem-retry.sh 100` | Dưới **2%** (QT 5.3) |
| 3 | Tổng phút runner mỗi tuần, trước và sau khi bật `interruptible` | Trang usage quota của project | Giảm, bậc **1.080 giây** cho mỗi ca 3 commit liên tiếp |

### Khi nào KHÔNG nên dùng

**Đừng** dùng `retry` như một cách "cho pipeline ổn định hơn". QT 5.3 nói nó ổn định bằng cách làm ta không thấy sự cố. Chưa đo được tỉ lệ chạy lại thì chưa được đặt `retry` — thứ tự đúng là đo trước, đặt sau.

**Đừng** dùng `CI_DEBUG_TRACE` làm bước đầu tiên. Nó là bước **cuối**, sau khi bảng ba mươi hai ô đã thu hẹp còn một hàng, vì nó in cả secret ra log cho bất cứ ai đọc được job (buổi 06 QT 7.2). Bốn lệnh của §4 rẻ hơn và không để lại rác.

**Đừng** dùng `resource_group` cho job test hay job build chỉ vì "để cho chắc". Nó biến việc chạy song song thành hàng đợi và làm đường găng dài ra — đúng thứ buổi **14** sẽ phải đi rút ngắn.

**Bảng ba mươi hai ô không giải được** lớp sự cố nằm ngoài một job: hạ tầng GitLab, quota, và hàng đợi runner ở quy mô. Ba thứ đó không thuộc ô nào trong bảng, vì bảng lấy đơn vị là **một job**. Đó là buổi **13** và buổi **47**.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy | Vì sao dính | Làm đúng là |
|---|---|---|---|
| 1 | Dán dòng lỗi cuối vào ô tìm kiếm, không biết nó thuộc pha nào | Bản năng: lỗi ở cuối log thì nguyên nhân cũng ở cuối | Định vị pha trước, loại bỏ **7/8** giả thuyết (QT 4.1) |
| 2 | Đọc log bằng mắt trên giao diện | Giao diện là thứ mở ra đầu tiên | `trace` qua API rồi `diff` — **2** lệnh (QT 4.2) |
| 3 | Không đọc `failure_reason` trước | Trên giao diện chỉ thấy chữ `failed`, tưởng không có gì hơn | **4** nhóm quy trách nhiệm, **1** lệnh `jq` (QT 4.3) |
| 4 | `retry` cho lỗi xác định | Chạy lại là hành động rẻ nhất về mặt thao tác | **270 giây** cho job 90 giây, **0%** cơ hội thêm (QT 5.1) |
| 5 | `retry` không có `when` | Mặc định `when: always` không ai đọc | Giới hạn vào nhóm hạ tầng; `max` tối đa **2** (QT 5.2) |
| 6 | Dùng `retry` mà không đo tỉ lệ chạy lại | Kết quả cuối cùng xanh nên không ai thắc mắc | Ngưỡng **2%** thì mở vé hạ tầng (QT 5.3) |
| 7 | Tin `timeout` trong YAML là hạn giờ thật | YAML là tệp duy nhất người viết pipeline đọc được | **3** nguồn, thắng theo **min** (QT 6.1) |
| 8 | Thêm runner để sửa job đang treo giữa `script` | Cả hai ca đều hiện là "pipeline chạy mãi" | Trường `runner` phân biệt `pending` với treo (QT 6.2) |
| 9 | Tin `after_script` luôn chạy đủ | Tài liệu nói nó chạy cả khi `script` hỏng, dừng đọc ở đó | Hạn giờ **riêng**, tham chiếu 5 phút, **phải đo** (QT 6.3) |
| 10 | Bật `interruptible` cho gần hết job | Tưởng lợi ích cộng dồn theo từng job | Giá trị **nhị phân theo pipeline**: còn 1 job là **0 giây** (QT 7.1) |
| 11 | Đánh dấu job deploy là `interruptible` | Làm cho đủ bộ, `default:` áp cả lượt | Job deploy phải **không** đánh dấu — bị huỷ giữa đường để lại trạng thái nửa vời (QT 7.1) |
| 12 | Không có `resource_group` cho deploy | Hai lần deploy cùng lúc là ca hiếm, cho tới hôm nó xảy ra | **2** pipeline chồng nhau, bản **kết thúc sau** thắng (QT 7.2) |
| 13 | `resource_group` cho job test "cho chắc" | Nghe như một lớp an toàn miễn phí | Biến song song thành hàng đợi, đường găng dài ra (QT 7.2) |
| 14 | Kết luận nguyên nhân mà không có lệnh chứng minh | Đã hiểu rồi thì viết lệnh ra thấy như việc dư | **4** dòng, dòng thứ hai là **một lệnh** (QT 7.3) |

---

### 1.7. Tóm tắt

```mermaid
graph TD
    LD["LUẬN ĐỀ: gỡ rối là THU HẸP, không phải thử lại<br/>4 đường vào × 8 pha = 32 ô — cả hai trục đến từ BUỔI 01"]

    G1["GIAI ĐOẠN 1 TỤ VÀO ĐÂY<br/>b01 tám pha + bốn đường · b02 config.toml<br/>b03 stage · b04 t0 · b05 artifact/cache · b06 chín nấc biến"] --> LD

    LD --> S4["§4 BA MƯƠI HAI Ô<br/>QT 4.1 log có cấu trúc, loại 7/8<br/>QT 4.2 trace là văn bản, diff được<br/>QT 4.3 failure_reason = 4 nhóm trách nhiệm"]
    LD --> S5["§5 retry<br/>QT 5.1 chỉ sửa lỗi chập chờn, 90s→270s<br/>QT 5.2 when gắn với failure_reason<br/>QT 5.3 retry là cơ chế CHE, phải đo 2%"]
    LD --> S6["§6 timeout<br/>QT 6.1 ba nguồn, min thắng<br/>QT 6.2 pending khác treo: trường runner<br/>QT 6.3 after_script có hạn giờ riêng — PHẢI ĐO"]

    S4 --> S7["§7 CHẶN VÀ KẾT LUẬN<br/>QT 7.1 interruptible nhị phân theo pipeline<br/>QT 7.2 resource_group: loại trừ duy nhất<br/>QT 7.3 báo cáo bốn dòng, dòng 2 là MỘT LỆNH"]
    S5 --> S7
    S6 --> S7

    S7 --> KQ["Ô NGUY HIỂM NHẤT vẫn là im lặng + không chặn<br/>hôm nay góp 6 chế độ hỏng, 5 nằm ở ô đó<br/>bảng hai thuộc tính — LẦN THỨ 7"]
    KQ --> VT["§8 ĐƯA VÀO VIỆC THẬT<br/>go-roi.sh · retry:when · interruptible ở default<br/>resource_group cho deploy — 4 việc, 40 phút"]

    S4 -.dùng lại.-> B1["buổi 13 · 14 · 22 · 47 · 48"]
    S5 -.dùng lại.-> B2["buổi 14 · 30 · 33 · 46 DORA"]
    S7 -.dùng lại.-> B3["buổi 36 environment · 41 GitOps · 43 canary"]
    KQ -.mở giai đoạn 2.-> B4["buổi 08 needs, DAG, parallel, matrix"]
```

**Năm điều phải nhớ sau buổi học:**

1. **Ba mươi hai ô, và cả hai trục đã có từ buổi 01.** 4 đường vào × 8 pha. Buổi này không thêm trục mới — nó chỉ nối hai trục cũ lại, nên mọi công cụ của sáu buổi trước đều dùng được ngay tại đây.
2. **Bốn lệnh trước một dòng suy đoán.** `failure_reason` cho cả pipeline → `trace` tải về tệp → chia theo tám pha → `diff` với lần xanh. Một lệnh loại bỏ **7/8** giả thuyết.
3. **`retry` là cơ chế che, không phải cơ chế sửa.** Job 90 giây với `retry: 2` cho **270 giây** và **0%** cơ hội thêm. Chưa đo được tỉ lệ chạy lại thì chưa được đặt `retry`.
4. **Hạn giờ đến từ ba nơi và min thắng.** Nguồn khó tìm nhất nằm trong `config.toml`, ngoài repo. Còn `pending` khác treo: trường `runner` là `null` hay không.
5. **Bằng chứng là một lệnh, không phải một câu.** Bốn dòng: triệu chứng · bằng chứng · nguyên nhân · cách sửa. Thiếu dòng thứ hai thì ba tháng sau có người điều tra lại từ đầu.

---

### 1.8. Câu hỏi tự kiểm tra

1. Bảng thu hẹp có bao nhiêu ô? Hai trục của nó đến từ buổi nào và quy tắc nào?
2. Một dòng lỗi `Could not resolve host` xuất hiện trong log. Nó thuộc pha nào, và vì sao sửa `script` không giúp gì?
3. Vì sao lấy `trace` qua API rồi `diff` tốt hơn đọc log trên giao diện? Nêu ba lý do cơ chế.
4. `failure_reason` phân loại nguyên nhân thành mấy nhóm quy trách nhiệm? Kể tên các nhóm và người xử lý tương ứng.
5. Một job 90 giây đặt `retry: 2` và lỗi là `exit 1` do sai chính tả tên tệp. Tổng thời gian là bao nhiêu, và cơ hội thành công tăng thêm mấy phần trăm?
6. Nêu **phép thử một câu** để biết một lỗi là xác định hay chập chờn.
7. Vì sao `retry` không có `when` là quyết định gần như luôn sai? `max` tối đa là bao nhiêu ở GitLab 17.7?
8. Một đội bật `retry` cho mọi job và hoá đơn phút runner tăng 30% mà số pipeline không đổi. Viết **một lệnh** chứng minh nguyên nhân.
9. Job khai `timeout: 3h` bị cắt ở phút thứ 60. Nêu ba nguồn hạn giờ và cách tìm ra nguồn nào đang thắng.
10. Hai job đều "chạy mãi không xong": một `pending`, một treo giữa `script`. Trường JSON nào phân biệt, và hai cách sửa khác nhau ra sao?
11. `after_script` có chạy khi `script` hết hạn giờ không? Vì sao câu trả lời này không được tra tài liệu?
12. Bật `interruptible: true` cho 9 trong 10 job mà phút runner không giảm. Vì sao? Job thứ 10 nên là job gì?
13. Staging đang chạy bản cũ hơn bản vừa deploy xong. Nêu nguyên nhân và **một dòng** cấu hình chặn nó. Đây là ô nào của bảng hai thuộc tính?
14. Viết báo cáo bốn dòng cho ca: job `trien-khai` **xanh** mà không có gì được triển khai, trên nhánh feature.

### Đáp án

1. **32 ô** = **4** đường vào × **8** pha. Trục ngang (tám pha) từ buổi 01 QT 4.2; trục dọc (bốn đường vào) từ buổi 01 QT 5.1. Buổi 07 không thêm trục mới.
2. Pha **3** (`get_sources`) nếu nó xuất hiện sau dòng `Getting source from Git repository` và trước dòng tiêu đề pha kế tiếp. Sửa `script` vô ích vì pha 6 chưa hề chạy — kiểm bằng việc log **không có** dòng `Executing "step_script"` (QT 4.1).
3. Giao diện (a) thu gọn phần dài, (b) tô màu bằng mã ANSI, (c) tải lười phần cuối. Cả ba phá phép so sánh cơ học. API trả về đúng byte runner đã gửi, nên `diff` là phép so có thật (QT 4.2).
4. **4** nhóm: `script_failure` → tác giả commit; `runner_system_failure`/`runner_unsupported` → đội hạ tầng; `job_execution_timeout`/`stuck_or_timeout_failure` → chủ pipeline; `missing_dependency_failure`/`archived_failure` → chủ job sinh artifact (QT 4.3).
5. **270 giây** (3 × 90) và **0%**. Lỗi hoàn toàn xác định: cùng đầu vào, cùng `image`, cùng `script`, cùng môi trường dùng một lần thì cùng kết quả (QT 5.1).
6. Chạy lại **hai** lần: hai kết quả khác nhau thì chập chờn, giống nhau thì xác định và `retry` vô nghĩa.
7. Vì mặc định là `when: always`, tức mọi `failure_reason` đều được chạy lại — kể cả `script_failure`, nên `retry` nuốt luôn lỗi code thật và làm tỉ lệ chạy lại mất ý nghĩa chẩn đoán. `max` tối đa **2** ở 17.7, và đó là giới hạn phiên bản, không phải quy luật (QT 5.2).
8. `dem-retry.sh 100` — hoặc gọi trực tiếp: `curl … "/pipelines/$p/jobs?include_retried=true" | jq -r '.[].name' | sort | uniq -c | awk '$1>1'`. Tỉ lệ vượt **2%** là ngưỡng đáng mở vé, theo kinh nghiệm thực tế (QT 5.3).
9. Ba nguồn: cấu hình project (`build_timeout`, mặc định **3.600** giây), khoá `timeout` của job, và hạn giờ của runner. **Min thắng.** Tìm bằng `GET /projects/:id` lấy `build_timeout`, `GET /runners/:id` lấy `maximum_timeout`, so với `timeout` trong YAML; nguồn khó tìm nhất là `config.toml`, ngoài repo (QT 6.1).
10. Trường `runner`: `null` là **chờ** — chưa ai nhận, thường do `tags` không khớp (buổi 02 QT 6.3), sửa bằng `tags`/thêm runner; có id là **treo** — đã nhận rồi, sửa bằng cách tìm việc đang treo trong `script` hoặc điều chỉnh hạn giờ. Job `pending` có `duration` = `null` (QT 6.2).
11. Có, vì `after_script` có đồng hồ **riêng**. Nhưng con số và cả hành vi phụ thuộc phiên bản runner và đã đổi trong quá khứ, nên đây là đại lượng **loại (c) phải đo** — giá trị tham chiếu ở Runner 17.7 là **5 phút**, và số đo thắng tài liệu (QT 6.3).
12. Vì nền tảng chỉ huỷ pipeline khi **mọi** job còn dở đều huỷ được an toàn; một job không đánh dấu là đủ để không huỷ gì, nên kết quả là **0 giây**. Job thứ 10 nên là job **deploy** — nó phải `interruptible: false` để không bị cắt giữa đường, và đó là cái giá đúng phải trả (QT 7.1).
13. Hai pipeline deploy chồng nhau, bản **kết thúc sau** thắng — không xác định và **im lặng**. Một dòng sửa: `resource_group: staging` cho job deploy. Ô **im lặng + không chặn**, ô nguy hiểm nhất (QT 7.2, buổi 01 QT 7.1).
14. Ví dụ: (1) *Triệu chứng:* `trien-khai` xanh trên nhánh `feature/x`, không tài nguyên nào đổi. (2) *Bằng chứng:* `$ curl … /jobs/$ID/trace | grep -n 'DEPLOY_TOKEN'` in ra `${#DEPLOY_TOKEN}` bằng **0**. (3) *Nguyên nhân:* biến `protected` không tồn tại trên nhánh không được bảo vệ, cho chuỗi rỗng chứ không cho lỗi (buổi 06 QT 5.2); ô *biến × pha 4–5*. (4) *Cách sửa:* thêm `: "${DEPLOY_TOKEN:?thiếu token}"` ở dòng đầu `script`, và giới hạn job bằng `rules` chỉ chạy trên nhánh được bảo vệ.

---

## §12. Tài liệu tham khảo

| Nguồn | Loại | Phiên bản |
|---|---|---|
| GitLab Docs — *CI/CD YAML syntax reference*: `retry`, `retry:when`, `timeout`, `interruptible`, `resource_group` | (a) tài liệu chính thức | **17.7** |
| GitLab Docs — *Job timeouts* và *Auto-cancel redundant pipelines* | (a) | **17.7** |
| GitLab Docs — *Resource group* và *Deployment safety* | (a) | **17.7** |
| GitLab Runner Docs — *Advanced configuration* (`config.toml`), biến hạn giờ của `after_script` | (a) | Runner **17.7** |
| GitLab API v4 — `GET /projects/:id/jobs/:job_id/trace`, `/pipelines/:id/jobs?include_retried=true`, `GET /runners/:id`, `/resource_groups/:key/upcoming_jobs` | (a) | v4 trên CE **17.7** |
| Hạn giờ riêng của `after_script`; `after_script` có chạy khi `script` hết hạn giờ không | **(c) phải ĐO** | Lab bước 4 |
| Dòng bắt đầu và số giây của tám pha; `failure_reason` của sáu ca hỏng | **(c) phải ĐO** | Lab bước 1 |
| Ngưỡng **2%** job phải chạy lại; ngưỡng "kết luận trong dưới 10 phút" | (c) kinh nghiệm thực tế | — |

> **Về việc trích dẫn.** Năm dòng loại (a) là chỗ nên tra tài liệu khi cần con số chính xác cho phiên bản đang chạy. Ba dòng loại (c) là chỗ **không được** tra — chúng phụ thuộc phiên bản runner và `config.toml` của chính hệ thống mình, và đây là **lần thứ 7** khoá học nhắc nguyên tắc đó.

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10' |
| §1 | Sau buổi này học viên làm được gì | 1' |
| §2 | Cần biết trước | 1' |
| §3 | Thuật ngữ và mô hình tư duy | 8' |
| §4 | Đọc log có phương pháp: ba mươi hai ô | 10' |
| §5 | `retry`: sửa được nhóm nào, che mất nhóm nào | 9' |
| §6 | `timeout`: ba nguồn, và job treo khác job chờ | 8' |
| §7 | `interruptible`, `resource_group`, và mẫu báo cáo bốn dòng | 7' |
| §8 | Đưa vào việc thật | 4' |
| §9 | Bẫy hay gặp | 2' |
| §10–§12 | Tóm tắt · tự kiểm tra · tham khảo (học viên đọc ngoài giờ) | — |
| **Tổng** | | **60'** |

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên môi trường GitLab Community / Enterprise Edition cùng các GitLab Runner cô lập (Docker / Kubernetes Executor). Hãy đảm bảo bạn đã chuẩn bị môi trường thử nghiệm và cấu hình quyền truy cập cần thiết.

## Khối thực hành — 150 phút

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · executor `docker`.
> Mọi checkpoint gọi **API GitLab**, không xem giao diện. Lý do ở §L2 quyết định 2 và ở QT 4.2.
> Buổi này là buổi **thu hoạch** của sáu buổi trước: sáu ca hỏng dựng sẵn, mỗi ca một nguyên nhân, mỗi ca dựng trên một buổi từ 01 tới 06. Học viên **chỉ nhận triệu chứng** — bảng nguyên nhân nằm trong phần của giảng viên ở cuối tệp và không được đọc trước khi làm xong bước 3.
> Buổi này đụng **hạ tầng dùng chung** ở hai chỗ: hạn giờ tối đa của runner bị hạ xuống **600 giây** trong suốt buổi, và phần **tuỳ chọn** sửa `config.toml` để cắt hạn giờ `after_script`. Cả hai đều sao lưu ở §L1, khôi phục ở §L8, và CHECKPOINT 12 kiểm bằng lệnh.
> Hiện vật nộp chính là `bao-cao-go-roi.md` gồm **6** báo cáo bốn dòng. Dòng thứ hai của mỗi báo cáo phải là **một lệnh** in ra được (QT 7.3) — checkpoint đếm đúng dòng đó bằng `grep -c`, không đọc câu văn.

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| # | Mục tiêu | Tiêu chí hoàn thành (kiểm chứng được bằng lệnh) |
|---|---|---|
| TH1 | Viết `go-roi.sh` — mở rộng `doc-pha.sh` buổi 05 thành công cụ gỡ rối | `bash -n go-roi.sh` không lỗi; chạy cho một job thật in **≥ 5** dòng pha có cột `dong_bat_dau` và `giay`, kèm `failure_reason`, `runner`, `queued_duration` |
| TH2 | Dựng bảng ba mươi hai ô của **chính mình**, mỗi ô một lệnh | `bang-32-o.md` có **4** hàng nhãn đường vào và **≥ 12** dòng bắt đầu bằng `$ ` |
| TH3 | **Đo QT 4.3** — `failure_reason` của sáu ca là sáu giá trị | `bang-6-ca.tsv` có **6** dòng, cột `failure_reason` có **≥ 4** giá trị khác nhau, kể cả ô `-` của ca không tạo được pipeline |
| TH4 | Gỡ ca 1, 2, 3 và viết ba báo cáo bốn dòng | `bao-cao-go-roi.md`: mỗi ca có **4** nhãn dòng và **≥ 1** dòng `$ ` — CHECKPOINT 3, 4, 5 |
| TH5 | Gỡ ca 4, 5, 6 — trong đó ca 5 **không có gì đỏ** | Ba báo cáo nữa, tổng **6**; ca 5 có bằng chứng hai giá trị khác nhau trong **một** tệp JSON của artifact |
| TH6 | Kiểm chứng QT 4.2 — so hai `trace` bằng máy, không bằng mắt | `diff lan-do.txt lan-xanh.txt` chỉ ra **dòng đầu tiên** khác nhau; số dòng ghi vào báo cáo ca 5 |
| TH7 | **Đo QT 5.1** — job `exit 1` với `retry: 2` tốn bao nhiêu giây | `include_retried=true` cho **3** lần chạy; tổng `duration` ≈ **270** giây cho job 90 giây |
| TH8 | Kiểm chứng QT 5.2 — `retry:when` giới hạn vào nhóm hạ tầng | Job `script_failure` có `retry:when` hạ tầng chạy **đúng 1** lần |
| TH9 | Viết `dem-retry.sh` — tỉ lệ job phải chạy lại trong N pipeline | `bash dem-retry.sh 20` in một dòng có `%`; đối chiếu với ngưỡng **2%** của QT 5.3 |
| TH10 | **Đo QT 6.1 và QT 6.3** — ba nguồn hạn giờ, và hạn giờ riêng của `after_script` | `bang-han-gio.tsv` có **3** con số nguồn + con số **min**; pha `after_script` của ca 6 đo được ≈ **300** giây và không có dòng `DON DEP XONG` |
| TH11 | **Đo QT 7.1 và QT 7.2** — giây tiết kiệm và chặn deploy chồng | Số job `canceled` sau **3** commit; quy ra giây; hai job cùng `resource_group` **không** chồng `started_at`/`finished_at` |
| TH12 | Nộp hiện vật và trả hạ tầng về nguyên trạng | `kiem-hien-vat.sh` in `ĐẠT`; `maximum_timeout` của runner bằng giá trị trong tệp sao lưu; nếu đã sửa `config.toml` thì `diff` với bản sao lưu **rỗng** |

**Sản phẩm cuối buổi:** `gitlab-portfolio/07-go-roi-pipeline/` gồm **`bao-cao-go-roi.md`** (6 báo cáo bốn dòng — hiện vật chính), **`go-roi.sh`**, `dem-retry.sh`, `bang-32-o.md`, `bang-6-ca.tsv`, `bang-han-gio.tsv`, `bang-huy.tsv`, `.gitlab-ci.yml` bản cuối của nhánh `do-luong`, `checkpoint.log`.

Hai hiện vật **cốt lõi** — thiếu một trong hai là chưa nộp bài — là `bao-cao-go-roi.md` và `go-roi.sh`. Ai đi **đường B** ở §L9 (không đọc được `GET /runners/:id`, không sửa được `config.toml`) vẫn có đủ cả hai, với `bang-han-gio.tsv` ghi **2** nguồn thay vì 3 và một dòng ghi rõ lý do.

---

## L1. Điều kiện tiên quyết về môi trường

| # | Kiểm tra | Lệnh | Kết quả kỳ vọng |
|---|---|---|---|
| 1 | Đã nạp biến môi trường lab | `echo "$GITLAB" "$GITLAB_TOKEN" \| wc -w` | `2` |
| 2 | GitLab sẵn sàng | `curl -sf -o /dev/null -w '%{http_code}\n' "$GITLAB/-/readiness"` | `200` |
| 3 | Token gọi được API | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/user" \| jq -r .username` | tên đăng nhập, khác rỗng |
| 4 | **Còn bộ công cụ buổi 05** — buổi này nạp lại, không viết lại | `grep -cE '^(day\|day_nhanh\|cho_pipeline\|job_bang\|job_id\|job_tt\|job_log\|job_log_sach\|art_http\|art_tep\|art_zip)\(\)' ~/lab05/cong-cu.sh` | `11` — thiếu thì §L9 dòng 1 |
| 5 | **Còn `doc-pha.sh` buổi 05** — `go-roi.sh` mở rộng từ nó | `bash -n ~/lab05/doc-pha.sh && grep -c 'section_start' ~/lab05/doc-pha.sh` | `≥ 1` |
| 6 | **Còn `dat-bien.sh` buổi 06** — ca 2 cần một biến `protected` | `bash -n ~/lab06/dat-bien.sh && echo co` | `co` — thiếu thì §L9 dòng 2 |
| 7 | Runner online và nhận job **không** tag | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners?status=online" \| jq -r '.[] \| "\(.id)\t\(.description)"'` | ≥ 1 dòng; lấy `id` làm `$RID` |
| 8 | **Không** runner nào có tag `gpu-lon` — ca 3 phụ thuộc điều này | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners?tag_list=gpu-lon" \| jq length` | `0` — khác `0` thì đổi tag của ca 3 sang một chuỗi không ai dùng |
| 9 | Đọc được **hạn giờ tối đa của runner** — nguồn thứ ba của QT 6.1 | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/$RID" \| jq .maximum_timeout` | một số hoặc `null`; `403` thì đi **đường B** §L9 dòng 3 |
| 10 | **Sao lưu hạn giờ runner trước khi hạ xuống 600 giây** | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/$RID" \| jq '{id, maximum_timeout}' > ~/lab07/han-gio-runner.bak; cat ~/lab07/han-gio-runner.bak` | tệp khác rỗng — §L8.1 khôi phục từ đây |
| 11 | **Tuỳ chọn — sao lưu `config.toml`** trước phần đo hạn giờ `after_script` | `docker exec lab-runner sh -c 'cp /etc/gitlab-runner/config.toml /etc/gitlab-runner/config.toml.buoi07.bak && ls -la /etc/gitlab-runner/config.toml*'` | thấy cả hai tệp; không làm được thì bỏ phần tuỳ chọn |
| 12 | Có `jq`, `curl`, `git`, `awk`, `sed`, `date` | `command -v jq curl git awk sed date \| wc -l` | `6` |
| 13 | Chưa có project lab 07 | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects?search=lab07-go-roi" \| jq length` | `0` — khác `0` thì §L9 dòng cuối |
| 14 | Đĩa trống — bài lab sinh khoảng **8 MB** artifact và **2 MB** log | `df -BG --output=avail "$HOME" \| tail -1` | `> 5G` |
| 15 | Ghi lại phiên bản để dán vào hiện vật | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/version" \| jq -r '.version'; docker exec lab-runner gitlab-runner --version \| head -2` | hai chuỗi phiên bản |

**Cảnh báo về mức độ tác động.** Bài lab tạo **một** project `lab07-go-roi` với sáu nhánh `ca-1` … `ca-6` cộng ba nhánh đo (`khoi-dong`, `do-luong`, `do-huy`, `do-hang-doi`). Bốn thứ **tồn tại sau khi buổi học kết thúc** nếu không dọn, xếp theo mức tác động giảm dần:

1. **`maximum_timeout` của runner bị hạ xuống 600 giây.** Đây là hạ tầng dùng chung: mọi job của **mọi project** dùng runner đó sẽ bị cắt ở phút thứ 10 trong suốt buổi. Đó là nguồn thứ ba của QT 6.1 và là nửa đầu của ca 6, nên không tránh được — nhưng **phải** sao lưu (dòng 10 của bảng) và khôi phục ở §L8.1. Trên lớp đông người dùng chung một runner, **chỉ giảng viên** hạ hạn giờ, một lần, trước lớp; học viên đọc số. Ai có runner riêng thì tự làm. GitLab 17.7 **không nhận** `maximum_timeout` nhỏ hơn **600** giây — đó là lý do ca 6 bị cắt ở phút thứ 10 chứ không phải phút thứ 2.
2. **Phần tuỳ chọn sửa `config.toml`.** Nó thêm một dòng `environment` vào khối `[[runners]]` để cắt hạn giờ `after_script` xuống **30 giây**, và dòng đó ảnh hưởng mọi job của runner. Sao lưu ở dòng 11, khôi phục **bắt buộc** ở §L8.2, và CHECKPOINT 12 đòi `diff` với bản sao lưu **rỗng**. Bỏ phần này vẫn đo được hạn giờ riêng của `after_script` bằng ca 6 (giá trị mặc định, tham chiếu 5 phút) — chỉ mất phần chứng minh **nguồn** của con số đó nằm ngoài repo. Đường B ở §L9 dòng 3.
3. **Một biến `protected` mức project** tên `DEPLOY_TOKEN` cho ca 2 (dựng lại buổi 06 QT 5.2). §L8.3 xoá và CHECKPOINT 12 kiểm `GET /variables` trả mảng rỗng.
4. **Một job `pending` vĩnh viễn** của ca 3. Nó không chiếm chỗ nào trong hàng đợi vì không runner nào nhận, nhưng nó cũng **không tự chết**: đó chính là chế độ hỏng im lặng số 6 — im lặng mà **có chặn**. §L8.3 huỷ pipeline đó bằng API.

Chi phí phút runner của buổi: ca 6 tốn **~15 phút** một mình (600 giây `script` bị cắt cộng ~300 giây `after_script` bị cắt), phép đo `retry` tốn **270 giây**, phép đo hạn giờ job tốn **120 giây**, bước 5 tốn **~4 phút**, phần còn lại dưới 3 phút — tổng khoảng **28–32 phút runner**. Vì ca 6 tốn 15 phút, giảng viên **phải chạy script dựng ca trước giờ ít nhất 20 phút**; nếu chạy đúng giờ thì bước 3 sẽ phải chờ.

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    GV["Giảng viên<br/>dung-sau-ca.sh — chạy TRƯỚC giờ 20 phút"]
    GV -->|"6 nhánh, 1 biến protected,<br/>maximum_timeout = 600"| PRJ["Project lab07-go-roi<br/>ca-1 … ca-6"]
    GV -->|"chỉ phát PHIẾU TRIỆU CHỨNG"| HV["Học viên"]

    HV -->|"go-roi.sh — 1 lệnh cho 1 job"| API["API GitLab v4<br/>jobs · trace · artifacts<br/>runners · pipelines"]
    HV -->|"POST /pipeline · git push"| PRJ
    PRJ -->|"giao job"| RN["Runner lab-runner<br/>executor docker<br/>maximum_timeout = 600 giây"]
    RN --> TR["trace THÔ<br/>section_start / section_end"]
    RN --> ART["artifact<br/>404 = rỗng · 200 = có"]
    TR --> API
    ART --> API

    API --> B1["Bước 1 — go-roi.sh<br/>failure_reason · bảng 32 ô"]
    API --> B2["Bước 2 — ca 1, 2, 3<br/>artifact rỗng · biến rỗng · pending"]
    API --> B3["Bước 3 — ca 4, 5, 6<br/>không tạo pipeline · XANH MÀ SAI · bị cắt"]
    API --> B4["Bước 4 — retry 270 giây<br/>timeout min của 3 nguồn"]
    API --> B5["Bước 5 — interruptible<br/>resource_group"]

    B2 --> BC["bao-cao-go-roi.md<br/>6 báo cáo bốn dòng<br/>dòng 2 = MỘT LỆNH"]
    B3 --> BC
    CC["cong-cu.sh buổi 05 — 11 hàm<br/>doc-pha.sh buổi 05<br/>dat-bien.sh buổi 06"] --> B1
    CC --> B2
```

**Năm quyết định thiết kế:**

1. **Sáu ca đặt trên sáu nhánh riêng của MỘT project, không trên sáu project.** Cùng một project nghĩa là cùng một runner, cùng một bộ biến, cùng một cấu hình hạn giờ. Nhờ đó biến số duy nhất giữa sáu ca là **nguyên nhân hỏng** — đúng tinh thần thu hẹp vùng nghi ngờ. Nếu mỗi ca một project thì mỗi lần kết luận sai học viên lại có một lối thoát rẻ tiền ("chắc project kia cấu hình khác"), và bảng ba mươi hai ô mất giá trị vì hai trục của nó không còn cố định. Cái giá phải trả: sáu nhánh dùng chung một biến `DEPLOY_TOKEN` và một `maximum_timeout`, nên ai sửa hai thứ đó giữa buổi sẽ làm nhiễu ca của người khác — §L8 dọn một lần cho cả sáu.

2. **Học viên không được xem trước bảng nguyên nhân.** Giảng viên giữ bảng sáu ca ở phần cuối tệp; học viên chỉ nhận **PHIẾU TRIỆU CHỨNG** sáu dòng. Một bài lab gỡ rối mà biết trước đáp án thì không đo được điều cần đo: cái ta muốn đo là **thời gian từ lúc thấy đỏ tới lúc có kết luận có bằng chứng**, và con số đó vô nghĩa nếu đáp án đã nằm trong đầu. Ai tự học một mình thì chép khối `dung-sau-ca.sh` ở phần giảng viên vào tệp rồi chạy **mà không đọc nội dung**; đọc rồi thì tự ghi vào hiện vật là đã đọc, và bỏ phần điểm thời gian ở §L11.

3. **Mỗi báo cáo bắt buộc có dòng bằng chứng dạng lệnh, và checkpoint kiểm chính dòng đó bằng `grep -c '^\$ '`, không kiểm câu văn.** QT 7.3 chỉ có giá trị khi được cưỡng chế bằng máy. Một câu như "artifact bị rỗng" không kiểm lại được sau ba tháng; một dòng `$ curl … /artifacts` in ra `404` thì kiểm lại được kể cả khi cả pipeline đã đổi. Vì thế CHECKPOINT 3 tới 8 **không** kiểm học viên có sửa được ca hay không — sửa được là phần thưởng, viết được bằng chứng là yêu cầu.

4. **Ca 5 là ca "xanh mà sai" và nó được đặt ở giữa, không đặt cuối.** Học viên phải gặp một ca mà **không có gì đỏ** ngay khi còn đang tin rằng gỡ rối là đi tìm màu đỏ. Đặt nó ở cuối thì lớp đã đoán được "chắc ca cuối là ca xanh mà sai" và mất hiệu ứng. Đây là lần thứ **5** của khoá cho nguyên lý "job xanh không chứng minh gì".

5. **Phần đo `retry` dùng job `exit 1` cố ý, không dùng ca chập chờn giả lập.** Mục đích của phép đo là cho thấy `retry` **không** giúp gì với lỗi xác định, và điều đó chỉ hiển nhiên khi lỗi hoàn toàn xác định: ba lần chạy cho **đúng cùng một** dòng lỗi và tổng **270 giây** cho một job 90 giây. Nếu dùng ca chập chờn thì có lần nó xanh, và cả bài học biến thành "retry đôi khi cứu được" — đúng cái kết luận sai mà QT 5.1 đi phá.

**Ca đối chứng PHẢI THẤT BẠI — báo trước cho lớp.** Ca 4 làm **pipeline không được tạo**: không có gì để mở ra xem, không có job nào, không có `failure_reason` nào — và đó chính là bài học của ô "pha 0" trong bảng ba mươi hai ô. Job `hong-xac-dinh` ở bước 4 **phải đỏ ba lần** với cùng một dòng lỗi. Job `qua-han-gio` ở bước 4 **phải bị cắt** ở phút thứ 2. Job `sao-luu-du-lieu` của ca 6 **phải bị cắt** ở phút thứ 10 dù YAML ghi `timeout: 1h`, và dòng `DON DEP XONG` trong `after_script` **phải không xuất hiện**. Bốn kết quả đó là đáp án đúng, không phải sự cố của bài lab.

---

## L3. Bước 1 — Dựng bộ công cụ: `go-roi.sh`, `failure_reason`, bảng ba mươi hai ô (25 phút)

Kiểm chứng QT 4.1, QT 4.2, QT 4.3.

### 3.1. Nạp lại bộ công cụ buổi 05 và buổi 06, bổ sung sáu hàm (5 phút)

Buổi này **không** viết lại `cong-cu.sh`. Mười một hàm của buổi 05 — `day`, `day_nhanh`, `cho_pipeline`, `job_bang`, `job_id`, `job_tt`, `job_log`, `job_log_sach`, `art_http`, `art_tep`, `art_zip` — dùng nguyên. Ta thêm sáu hàm, tất cả đều là hàm **đọc**: một hàm đọc JSON của job, một hàm in bảng job **rộng** có `failure_reason`, một hàm tạo pipeline in cả thông báo lỗi khi pipeline **không** được tạo, một hàm đọc hạn giờ runner, một hàm đọc trace đã chuẩn hoá, một hàm đếm số lần chạy của một job.

```bash
source ~/.gitlab-lab.env
mkdir -p ~/lab07 && cd ~/lab07
export PID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects?search=lab07-go-roi" | jq -r '.[0].id')
export RID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/runners?status=online" | jq -r '.[0].id')
echo "PID=$PID  RID=$RID"
{ echo "export PID=$PID"; echo "export RID=$RID"; } >> ~/.gitlab-lab.env
```

```bash
cat > ~/lab07/cong-cu07.sh <<'SH'
#!/usr/bin/env bash
# Bộ công cụ lab buổi 07 — nạp LẠI buổi 05 rồi bổ sung sáu hàm ĐỌC.
# Dùng: source ~/lab07/cong-cu07.sh
. "$HOME/lab05/cong-cu.sh"

# JSON đầy đủ của một job — nguồn của failure_reason, runner, queued_duration
job_json()  { curl -sf "${H[@]}" "$A/jobs/$1"; }

# bảng job RỘNG: cái này thay job_bang trong mọi cuộc gỡ rối (QT 4.3)
job_bang_rong() {
  curl -sf "${H[@]}" "$A/pipelines/$1/jobs?per_page=100&include_retried=true" \
  | jq -r '["id","ten","tt","ly_do","runner","cho_giay","chay_giay"],
           (.[] | [.id, .name, .status, (.failure_reason // "-"),
                   (.runner.id // "null"), ((.queued_duration // 0) | floor),
                   ((.duration // 0) | floor)]) | @tsv' | column -t -s $'\t'
}

# tạo pipeline và in CẢ thông báo lỗi khi pipeline KHÔNG được tạo (ca 4)
tao_pipe() {
  local nhanh="$1"; shift
  local vars='[]' kv
  for kv in "$@"; do
    vars=$(printf '%s' "$vars" | jq -c --arg k "${kv%%=*}" --arg v "${kv#*=}" \
           '. + [{key:$k, value:$v, variable_type:"env_var"}]')
  done
  curl -s "${H[@]}" --request POST --header 'Content-Type: application/json' \
    --data "$(jq -n --arg r "$nhanh" --argjson v "$vars" '{ref:$r, variables:$v}')" \
    "$A/pipeline" | jq -r 'if .id then (.id|tostring)
                           else "KHONG-TAO-DUOC\t" + ((.message // .error) | tostring) end'
}

# hạn giờ tối đa của runner — nguồn THỨ BA của QT 6.1, nằm NGOÀI repo
runner_han() {
  curl -s "${H[@]}" "$GITLAB/api/v4/runners/${1:-$RID}" \
  | jq -r 'if .maximum_timeout != null then .maximum_timeout
           elif .message then "KHONG-DOC-DUOC" else "null" end'
}

# trace đã CHUẨN HOÁ: \r thành \n. Số dòng của go-roi.sh tính trên bản này.
trace_chuan() { job_log "$1" | tr '\r' '\n'; }

# số lần một job đã chạy (kể cả các lần bị retry) — dùng ở bước 4
so_lan_chay() {
  curl -sf "${H[@]}" "$A/pipelines/$1/jobs?per_page=100&include_retried=true" \
  | jq --arg n "$2" '[.[] | select(.name==$n)] | length'
}
SH
source ~/lab07/cong-cu07.sh
type job_bang_rong >/dev/null && type art_http >/dev/null && echo "nap du 11 + 6 ham"
```

Nhánh `khoi-dong` để có ngay hai job thật cho `go-roi.sh` đọc: một job xanh có cả cache lẫn artifact (đủ tám pha), một job đỏ ở `script`.

```bash
cd ~/lab07
git init -q -b main 2>/dev/null
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$A" | jq -r .path_with_namespace).git" 2>/dev/null
git config user.email "hocvien@lab.local"; git config user.name "hoc vien"
```

```yaml
# ~/lab07/.gitlab-ci.yml — nhánh khoi-dong
stages: [xay, kiem]

default:
  image: alpine:3.20

mau-xanh:
  stage: xay
  cache:
    key: khoi-dong
    paths: [.bo-dem/]
  script:
    - mkdir -p .bo-dem ket-qua
    - echo "$CI_COMMIT_SHORT_SHA" > ket-qua/phien-ban.txt
    - sleep 3
  artifacts:
    paths: [ket-qua/]
    expire_in: 1 day

mau-do:
  stage: kiem
  script:
    - echo "sap hong o day"
    - ls /khong-co-thu-muc-nay
```

```bash
cd ~/lab07
echo "# lab07 go roi pipeline" > README.md
git add -A && git commit -q -m "khoi dong" --allow-empty
git push -q -f origin HEAD:refs/heads/khoi-dong 2>/dev/null
sleep 6
P_KD=$(curl -sf "${H[@]}" "$A/pipelines?ref=khoi-dong&per_page=1" | jq -r '.[0].id')
cho_pipeline "$P_KD" 420
job_bang_rong "$P_KD"
```

Bảng vừa in ra là **bước 0 của mọi cuộc gỡ rối** (QT 4.3): một lệnh, cả pipeline, và cột `ly_do` đã phân loại nguyên nhân theo nền tảng trước khi ta đọc một dòng log nào. Bốn nhóm quy trách nhiệm: `script_failure` là việc của người viết code; `runner_system_failure` là việc của đội hạ tầng; `job_execution_timeout` là việc của người đặt hạn giờ; `missing_dependency_failure` là việc của người khai `needs`/`artifacts`.

### 3.2. `go-roi.sh` — mở rộng `doc-pha.sh` buổi 05 (10 phút)

`doc-pha.sh` của buổi 05 trả lời **một** câu: ba pha cache/artifact tốn bao nhiêu giây. `go-roi.sh` trả lời câu của buổi 07: **hỏng ở ô nào trong ba mươi hai ô**. Nó giữ nguyên cơ chế đọc mốc `section_start:<epoch>:<tên>` / `section_end:<epoch>:<tên>` trong `trace` **thô** — vì đó là dữ liệu duy nhất không phụ thuộc việc runner có bật dấu thời gian từng dòng — và thêm ba thứ: cột **dòng bắt đầu** của mỗi pha, số hiệu **pha 1–8** của buổi 01 QT 4.2, và một khối tiêu đề đọc từ JSON của job gồm `failure_reason`, `runner`, `queued_duration`.

```bash
cat > ~/lab07/go-roi.sh <<'SH'
#!/usr/bin/env bash
# go-roi.sh — công cụ gỡ rối MỘT job: in bảng PHA · DÒNG BẮT ĐẦU · GIÂY,
# kèm failure_reason, runner, queued_duration. Mở rộng doc-pha.sh của buổi 05.
#
# Dùng:
#   bash go-roi.sh <PID> <JOB_ID>            # mặc định --bang (tiêu đề + bảng pha)
#   bash go-roi.sh <PID> <JOB_ID> --pha      # chỉ bảng pha, dạng TSV, dễ awk
#   bash go-roi.sh <PID> <JOB_ID> --json     # một đối tượng JSON một dòng
#
# Cần: GITLAB, GITLAB_TOKEN, curl, jq, awk.
#
# CƠ CHẾ. Runner ghi vào trace các cặp điều khiển:
#     section_start:1738000000:step_script\r<esc>[0KExecuting "step_script" stage
#     section_end:1738000041:step_script\r<esc>[0K
# Hiệu hai mốc epoch là số giây của pha, chính xác tới 1 giây.
# Cột dong_bat_dau tính trên trace ĐÃ CHUẨN HOÁ bằng `tr '\r' '\n'` — muốn xem
# đúng dòng đó thì dùng:  job_log <id> | tr '\r' '\n' | sed -n '<dong>p'
#
# TÁM PHA của buổi 01 QT 4.2 được đánh số ở cột pha; section lạ ghi pha 0.
# MÃ THOÁT: 0 bình thường · 2 thiếu tham số · 3 không đọc được job
#           · 4 trace rỗng (job pending — xem QT 6.2) · 5 trace không có section nào
set -uo pipefail
PID_IN="${1:-}"; JOB_IN="${2:-}"; DANG="${3:---bang}"
if [ -z "$PID_IN" ] || [ -z "$JOB_IN" ]; then
  echo "Dùng: bash go-roi.sh <PID> <JOB_ID> [--bang|--pha|--json]" >&2; exit 2
fi
: "${GITLAB:?chưa đặt GITLAB}"
: "${GITLAB_TOKEN:?chưa đặt GITLAB_TOKEN}"
HH=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")
AA="$GITLAB/api/v4/projects/$PID_IN"

JJ=$(curl -sf "${HH[@]}" "$AA/jobs/$JOB_IN") \
  || { echo "khong doc duoc job $JOB_IN (kiem PID, JOB_ID, token)" >&2; exit 3; }

TEN=$(printf '%s' "$JJ" | jq -r '.name')
TT=$(printf  '%s' "$JJ" | jq -r '.status')
LY_DO=$(printf '%s' "$JJ" | jq -r '.failure_reason // "-"')
RN=$(printf  '%s' "$JJ" | jq -r '.runner.id // "null"')
RN_TEN=$(printf '%s' "$JJ" | jq -r '.runner.description // "-"')
CHO=$(printf '%s' "$JJ" | jq -r '(.queued_duration // 0) | floor')
CHAY=$(printf '%s' "$JJ" | jq -r '(.duration // 0) | floor')
REF=$(printf '%s' "$JJ" | jq -r '.ref')
# hạn giờ của runner đã nhận job — nguồn thứ ba của QT 6.1
HAN="-"
if [ "$RN" != "null" ]; then
  HAN=$(curl -s "${HH[@]}" "$GITLAB/api/v4/runners/$RN" \
        | jq -r 'if .maximum_timeout != null then .maximum_timeout
                 elif .message then "khong-doc-duoc" else "null" end')
fi

TRACE=$(curl -sf "${HH[@]}" "$AA/jobs/$JOB_IN/trace" || true)
if [ -z "$TRACE" ]; then
  echo "job $TEN ($JOB_IN): trace RONG · tt=$TT · runner=$RN · cho=${CHO}s" >&2
  echo "  trace rong + runner=null = PENDING, khong phai treo (QT 6.2)" >&2
  exit 4
fi

BANG=$(printf '%s' "$TRACE" | tr '\r' '\n' | awk '
  {
    if (match($0, /section_(start|end):[0-9]+:[A-Za-z0-9_]+/)) {
      s = substr($0, RSTART, RLENGTH); split(s, p, ":")
      if (p[1] == "section_start") {
        if (!(p[3] in bd)) { bd[p[3]] = p[2]; dong[p[3]] = NR; thu_tu[++n] = p[3] }
      } else { kt[p[3]] = p[2] }
    }
    if (loi_dong == 0 && $0 ~ /ERROR|error:|No such file|not found|command not found/) loi_dong = NR
  }
  END {
    if (n == 0) { print "KHONG-CO-SECTION" > "/dev/stderr"; exit 5 }
    pha["prepare_executor"]=1; pha["resolve_secrets"]=1; pha["prepare_script"]=2
    pha["get_sources"]=3; pha["restore_cache"]=4; pha["download_artifacts"]=5
    pha["step_script"]=6; pha["build_script"]=6; pha["after_script"]=7
    pha["archive_cache"]=8; pha["archive_cache_on_failure"]=8
    pha["upload_artifacts_on_success"]=8; pha["upload_artifacts_on_failure"]=8
    pha["cleanup_file_variables"]=8
    for (i = 1; i <= n; i++) {
      s = thu_tu[i]
      g = (s in kt) ? kt[s] - bd[s] : -1
      p = (s in pha) ? pha[s] : 0
      printf "%d\t%s\t%d\t%d\n", p, s, dong[s], g
      tong += (g > 0 ? g : 0)
      if (g >= 0) cuoi = s
    }
    printf "9\tTONG_CAC_PHA\t0\t%d\n", tong
    printf "9\tPHA_CUOI_HOAN_TAT\t0\t0\t%s\n", cuoi
    printf "9\tDONG_LOI_DAU_TIEN\t%d\t0\n", loi_dong
  }') || exit 5

if [ "$DANG" = "--pha" ]; then
  printf 'pha\tsection\tdong_bat_dau\tgiay\n'
  printf '%s\n' "$BANG"
  exit 0
fi

if [ "$DANG" = "--json" ]; then
  printf '%s\n' "$BANG" | awk -F'\t' -v t="$TEN" -v s="$TT" -v l="$LY_DO" \
    -v r="$RN" -v c="$CHO" -v d="$CHAY" -v h="$HAN" -v j="$JOB_IN" '
    BEGIN { printf "{\"job\":%s,\"ten\":\"%s\",\"tt\":\"%s\",\"failure_reason\":\"%s\"", j, t, s, l
            printf ",\"runner\":\"%s\",\"queued_duration\":%s,\"duration\":%s,\"runner_maximum_timeout\":\"%s\",\"pha\":{", r, c, d, h }
    $1 < 9 { printf "%s\"%s\":{\"pha\":%s,\"dong\":%s,\"giay\":%s}", (k++ ? "," : ""), $2, $1, $3, $4 }
    END { print "}}" }'
  exit 0
fi

printf '===== go-roi.sh · job %s (id %s) · ref %s =====\n' "$TEN" "$JOB_IN" "$REF"
printf 'trang thai      : %s\n' "$TT"
printf 'failure_reason  : %s   <- BUOC 0 cua moi cuoc go roi (QT 4.3)\n' "$LY_DO"
printf 'runner          : %s (%s)   maximum_timeout=%s giay\n' "$RN" "$RN_TEN" "$HAN"
printf 'queued_duration : %s giay   duration: %s giay\n' "$CHO" "$CHAY"
printf 'trace           : %s dong (da chuan hoa \\r -> \\n)\n' \
  "$(printf '%s' "$TRACE" | tr '\r' '\n' | wc -l | tr -d ' ')"
echo
printf 'pha\tsection\tdong_bat_dau\tgiay\n'
printf '%s\n' "$BANG" | awk -F'\t' '$1 < 9'
echo
printf '%s\n' "$BANG" | awk -F'\t' '$1 == 9 { printf "%-22s %s %s\n", $2, $3 + $4, $5 }'
SH
chmod +x ~/lab07/go-roi.sh
bash -n ~/lab07/go-roi.sh && echo "cu phap OK"
```

Thử ngay trên hai job của nhánh `khoi-dong` — nếu nó chạy được ở đây thì mọi kết luận của bốn bước sau mới có nền:

```bash
bash ~/lab07/go-roi.sh "$PID" "$(job_id "$P_KD" mau-xanh)"
bash ~/lab07/go-roi.sh "$PID" "$(job_id "$P_KD" mau-do)"
bash ~/lab07/go-roi.sh "$PID" "$(job_id "$P_KD" mau-do)" --pha
bash ~/lab07/go-roi.sh "$PID" "$(job_id "$P_KD" mau-do)" --json | jq .
```

Đọc hai bảng cạnh nhau và trả lời ngay: job `mau-do` có pha **6** (`step_script`) trong bảng không? Có nghĩa là lệnh của ta đã chạy. Nếu một job đỏ mà **không** có pha 6, thì mọi phút bỏ ra sửa `script` là phút bỏ đi — đó là toàn bộ giá trị của QT 4.1, và nó loại bỏ **bảy trong tám** nhóm nguyên nhân bằng một lệnh.

**CHECKPOINT 1 — `go-roi.sh` chạy được, đọc mốc `section_*`, in ≥ 5 pha có cột dòng bắt đầu và giây, kèm `failure_reason`, `runner`, `queued_duration`.**

```bash
J_DO=$(job_id "$P_KD" mau-do)
bash -n ~/lab07/go-roi.sh 2>/dev/null \
  && grep -q 'section_start' ~/lab07/go-roi.sh \
  && so_pha=$(bash ~/lab07/go-roi.sh "$PID" "$J_DO" --pha | awk -F'\t' 'NR>1 && $1>=1 && $1<=8' | wc -l | tr -d ' ') \
  && co_dong=$(bash ~/lab07/go-roi.sh "$PID" "$J_DO" --pha | awk -F'\t' 'NR>1 && $3+0>0' | wc -l | tr -d ' ') \
  && j=$(bash ~/lab07/go-roi.sh "$PID" "$J_DO" --json) \
  && echo "$j" | jq -e '.failure_reason != "-" and .runner != "null" and (.queued_duration|type=="number")' >/dev/null \
  && [ "$so_pha" -ge 5 ] && [ "$co_dong" -ge 5 ] \
  && echo "CHECKPOINT 1 — ĐẠT ($so_pha pha, $co_dong pha có dòng bắt đầu, failure_reason=$(echo "$j" | jq -r .failure_reason))" \
  || echo "CHECKPOINT 1 — LỖI (so_pha=${so_pha:-0}, co_dong=${co_dong:-0} — cần ≥5; xem §L9 dòng 4, 5)"
```

### 3.3. Bảng ba mươi hai ô của chính mình — bốn hàng, mỗi ô một lệnh (10 phút)

Bảng ba mươi hai ô là **4** đường dữ liệu vào job (buổi 01 QT 5.1, lần thứ 4) nhân **8** pha (buổi 01 QT 4.2, lần thứ 4), gom cột thành bốn nhóm pha để bảng vừa một trang. Giá trị của nó không nằm ở việc chép lại — nó nằm ở chỗ **mỗi ô ghi một lệnh chạy được trên hạ tầng của chính mình**. Bảng dưới là bộ khung; học viên điền lệnh, chạy thử từng lệnh trên hai job của nhánh `khoi-dong`, và chỉ ghi vào hiện vật những lệnh **đã in ra được cái gì đó**.

```bash
cd ~/lab07
cat > bang-32-o.md <<'MD'
# Bảng ba mươi hai ô — bản của tôi
Đo trên GitLab CE 17.7 · Runner 17.7 · executor docker. Máy đo: DIEN-VAO-DAY.
4 đường vào (buổi 01 QT 5.1) × 8 pha (buổi 01 QT 4.2), gom cột thành 4 nhóm pha.
Mọi dòng bắt đầu bằng `$ ` là một lệnh ĐÃ CHẠY ĐƯỢC trên hạ tầng của tôi.

## Bước 0 — bốn lệnh loại bỏ theo CỘT, chạy trước khi đọc log
$ job_bang_rong "$PIPE"
$ bash ~/lab07/go-roi.sh "$PID" "$JOB" --pha
$ bash ~/lab07/go-roi.sh "$PID" "$JOB" --json | jq -r '.failure_reason, .runner'
$ job_log_sach "$JOB" | tr '\r' '\n' | sed -n "$(bash ~/lab07/go-roi.sh "$PID" "$JOB" --pha | awk -F'\t' '$2=="step_script"{print $3}'),\$p" | head -20

## Hàng 1 — mã nguồn (git)
$ bash ~/lab07/go-roi.sh "$PID" "$JOB" --pha | awk -F'\t' '$2=="get_sources"{print "pha 3 ton", $4, "giay"}'
$ job_log_sach "$JOB" | grep -E 'Getting source|Checking out|fatal:'

## Hàng 2 — cache
$ bash ~/lab07/go-roi.sh "$PID" "$JOB" --pha | awk -F'\t' '$2=="restore_cache"{print "pha 4 ton", $4, "giay"}'
$ job_log_sach "$JOB" | grep -iE 'Restoring cache|Successfully extracted cache|Failed to extract cache|No URL provided'

## Hàng 3 — artifacts
$ art_http "$JOB_NGUON"
$ art_tep "$JOB_NGUON" "duong/dan/trong/artifact" | head -3
$ job_log_sach "$JOB" | grep -iE 'Downloading artifacts|WARNING: .*no matching files|Uploading artifacts'

## Hàng 4 — biến
$ job_log_sach "$JOB" | grep -E 'DO_DAI_[A-Z_]+='
$ curl -sf "${H[@]}" "$A/variables" | jq -r '.[] | "\(.key)\tprotected=\(.protected)\tlen=\(.value|length)"'

## Ô đặc biệt — pha 0, trước khi job tồn tại (t0 của buổi 04)
$ tao_pipe ca-4
$ curl -sf "${H[@]}" "$A/ci/lint?dry_run=true&ref=ca-4" -X POST --header 'Content-Type: application/json' --data '{"content":"..."}' | jq '{valid, errors}'
MD
sed -i "s/DIEN-VAO-DAY/$(hostname)/" bang-32-o.md
grep -c '^\$ ' bang-32-o.md
```

Chạy thử **từng** lệnh của bảng trên job `mau-do` và `mau-xanh` để chắc chúng in ra được cái gì đó. Ô nào lệnh không chạy được thì sửa lệnh, đừng để lại một ô "để đó cho đủ" — bảng có một ô giả là bảng không dùng được lúc 2 giờ sáng:

```bash
export PIPE="$P_KD" JOB="$J_DO" JOB_NGUON=$(job_id "$P_KD" mau-xanh)
job_bang_rong "$PIPE"
art_http "$JOB_NGUON"; echo
art_tep "$JOB_NGUON" "ket-qua/phien-ban.txt"
job_log_sach "$JOB" | grep -E 'Getting source|Restoring cache|Downloading artifacts' || echo "(khong co dong nao)"
```

Bây giờ QT 4.2 — so hai `trace` bằng máy, không bằng mắt. Đây là **1** lệnh `curl` cộng **1** lệnh `diff` thay cho việc đọc 400 dòng:

```bash
cd ~/lab07
trace_chuan "$(job_id "$P_KD" mau-xanh)" > lan-xanh.txt
trace_chuan "$J_DO"                      > lan-do.txt
wc -l lan-xanh.txt lan-do.txt
diff lan-xanh.txt lan-do.txt | head -12
diff lan-xanh.txt lan-do.txt | grep -m1 -E '^[0-9]+' 
```

Số dòng đầu tiên mà `diff` in ra là **vị trí phân kỳ** — con số đó là thứ hai người nhìn cùng một job vẫn nói ra giống nhau, còn "log nó khác khác" thì không. Ghi con số của mình vào `bang-32-o.md`.

**CHECKPOINT 2 — bảng ba mươi hai ô có 4 hàng nhãn đường vào, ≥ 12 dòng lệnh chạy được, và có ô pha 0.**

```bash
so_lenh=$(grep -c '^\$ ' ~/lab07/bang-32-o.md)
so_hang=$(grep -cE '^## Hàng [1-4] —' ~/lab07/bang-32-o.md)
co_pha0=$(grep -c 'pha 0' ~/lab07/bang-32-o.md)
co_may=$(grep -c 'DIEN-VAO-DAY' ~/lab07/bang-32-o.md)
echo "so_lenh=$so_lenh  so_hang=$so_hang  co_pha0=$co_pha0  con_cho_trong=$co_may"
{ [ "$so_lenh" -ge 12 ] && [ "$so_hang" -eq 4 ] && [ "$co_pha0" -ge 1 ] && [ "$co_may" -eq 0 ] \
  && [ -s ~/lab07/lan-do.txt ] && [ -s ~/lab07/lan-xanh.txt ]; } \
  && echo "CHECKPOINT 2 — ĐẠT ($so_lenh lệnh, 4 hàng đường vào, có ô pha 0, có hai trace để diff)" \
  || echo "CHECKPOINT 2 — LỖI (cần ≥12 lệnh, đúng 4 hàng, ô pha 0, đã thay DIEN-VAO-DAY, và hai tệp trace)"
```

---

## L4. Bước 2 — Gỡ ca 1, 2, 3 và viết ba báo cáo bốn dòng (35 phút)

Kiểm chứng QT 4.1, QT 4.3, QT 7.3.

Từ đây trở đi mọi checkpoint đều ghi vào `checkpoint.log` — hiện vật nộp số 8 đòi đủ **12** dòng `ĐẠT`. Chạy lại hai đoạn kiểm của bước 1 một lần nữa qua `tee`, rồi thêm `| tee -a ~/lab07/checkpoint.log` vào **mọi** đoạn checkpoint còn lại:

```bash
touch ~/lab07/checkpoint.log
# chạy lại đoạn kiểm CHECKPOINT 1 và CHECKPOINT 2 với: ... | tee -a ~/lab07/checkpoint.log
grep -c 'CHECKPOINT' ~/lab07/checkpoint.log
```

### 4.1. Phiếu triệu chứng, quy trình bốn lệnh, và mẫu báo cáo (3 phút)

Đây là tất cả những gì học viên được biết về ba ca đầu. Không có thêm gợi ý nào, và **không** mở phần phụ lục giảng viên ở cuối tệp trước khi xong bước 3:

| Ca | Nhánh | Triệu chứng học viên thấy | Ngân sách |
|---|---|---|---|
| 1 | `ca-1` | Job `dong-goi` **đỏ**: không tìm thấy tệp | 10' |
| 2 | `ca-2` | Job `trien-khai` **xanh** mà không có gì được triển khai | 10' |
| 3 | `ca-3` | Pipeline đứng ở `pending` hơn 20 phút, **không ai báo** gì | 8' |

**Quy trình bốn lệnh — chạy đúng thứ tự này cho mọi ca, trước khi đọc một dòng log nào.** Ba lệnh đầu loại bỏ theo **cột** của bảng ba mươi hai ô, lệnh thứ tư loại bỏ theo **hàng**:

```bash
# mảnh — dán vào shell, đặt PIPE và JOB trước
job_bang_rong "$PIPE"                                    # 1. failure_reason cả pipeline (QT 4.3)
bash ~/lab07/go-roi.sh "$PID" "$JOB"                     # 2. pha nào hỏng (QT 4.1)
bash ~/lab07/go-roi.sh "$PID" "$JOB" --pha | awk -F'\t' '$4 < 0 || $1 == 6'   # 3. pha nào chưa đóng
job_log_sach "$JOB" | tr '\r' '\n' | sed -n "$(bash ~/lab07/go-roi.sh "$PID" "$JOB" --pha \
  | awk -F'\t' '$1==6{print $3}'),\$p" | head -20        # 4. đọc TỪ pha hỏng, không đọc từ đầu
```

Lệnh thứ hai là lệnh đắt giá nhất của buổi: nếu bảng pha **không có** dòng pha 6 thì lỗi nằm trước `script`, và mọi phút bỏ ra sửa `script` là phút bỏ đi — một lệnh loại bỏ **7/8** nhóm nguyên nhân (QT 4.1).

Mẫu báo cáo bốn dòng của QT 7.3, cộng một dòng thứ năm ghi ô trong bảng và hai thuộc tính hỏng của buổi 01 QT 7.1 (lần thứ 7 của nguyên lý đó). Dòng `BANG CHUNG` **phải** là một lệnh bắt đầu bằng `$ ` kèm đầu ra rút gọn — máy sẽ đếm đúng dòng đó:

```bash
cd ~/lab07
cat > bao-cao-go-roi.md <<'MD'
# Sáu báo cáo gỡ rối — buổi 07
Đo trên GitLab CE 17.7 · Runner 17.7 · executor docker. Người gỡ: DIEN-TEN-VAO-DAY.
Mẫu bốn dòng của QT 7.3. Dòng BANG CHUNG luôn là MỘT LỆNH đã in ra được, ghi kèm đầu ra.

MD
sed -i "s/DIEN-TEN-VAO-DAY/$(whoami)@$(hostname)/" bao-cao-go-roi.md

cat > mau-bao-cao.txt <<'MD'
## Ca N — <triệu chứng một dòng>
- TRIEU CHUNG: <người dùng thấy gì, ở job nào, trạng thái gì>
- BANG CHUNG:
$ <lệnh>
<đầu ra rút gọn, giữ đúng con số>
- NGUYEN NHAN: <cơ chế, không phải phỏng đoán>
- CACH SUA: <sửa gì, và dòng khẳng định nào chặn nó tái diễn>
- O: <hàng> × <nhóm pha> · <im lặng|ồn ào> · <có chặn|không chặn>
MD
cat mau-bao-cao.txt
```

Máy kiểm báo cáo — dùng lại ở cả sáu checkpoint từ 3 tới 8, nên viết một lần:

```bash
cat > ~/lab07/kiem-bao-cao.sh <<'SH'
#!/usr/bin/env bash
# kiem-bao-cao.sh <so_ca_toi_thieu> [tep]
# Mỗi khối "## Ca N" phải có đủ BỐN nhãn của QT 7.3 và ÍT NHẤT MỘT dòng lệnh "$ ".
# In một dòng cho từng ca, dòng cuối TONG_CA_DAT=<n>. Mã thoát 0 khi đủ số ca yêu cầu.
N="${1:-1}"; F="${2:-$HOME/lab07/bao-cao-go-roi.md}"
[ -s "$F" ] || { echo "khong co $F"; echo "TONG_CA_DAT=0"; exit 1; }
awk -v need="$N" '
  function xong() {
    if (ca == "") return
    nhan = t + b + n + s
    ok = (nhan == 4 && lenh >= 1)
    printf "  ca %s: %s (nhan=%d/4, dong_lenh=%d, o=%s)\n", ca, (ok ? "hop le" : "THIEU"), nhan, lenh, (o ? "co" : "khong")
    if (ok) dat++
  }
  /^## Ca /            { xong(); ca = $3; gsub(/[^0-9]/, "", ca); t = b = n = s = o = lenh = 0; next }
  /^- TRIEU CHUNG:/    { t = 1 }
  /^- BANG CHUNG:/     { b = 1 }
  /^- NGUYEN NHAN:/    { n = 1 }
  /^- CACH SUA:/       { s = 1 }
  /^- O:/              { o = 1 }
  /^\$ /               { lenh++ }
  END { xong(); printf "TONG_CA_DAT=%d\n", dat; exit !(dat >= need) }
' "$F"
SH
bash ~/lab07/kiem-bao-cao.sh 0
```

### 4.2. Ca 1 — job `dong-goi` đỏ vì không tìm thấy tệp (10 phút)

```bash
source ~/lab07/cong-cu07.sh
P1=$(tao_pipe ca-1); echo "pipeline ca-1 = $P1"
cho_pipeline "$P1" 300
job_bang_rong "$P1"
```

Bảng bước 0 cho hai dữ kiện trước khi ta mở log: `dong-goi` có `ly_do` là `script_failure` — lỗi thuộc **nhóm người viết code** — và job `chuan-bi` ở stage trước **xanh**. Hai dữ kiện đó cùng lúc là một nghịch lý, và nghịch lý là chỗ để đào:

```bash
J_CB=$(job_id "$P1" chuan-bi); J_DG=$(job_id "$P1" dong-goi)
bash ~/lab07/go-roi.sh "$PID" "$J_DG"
bash ~/lab07/go-roi.sh "$PID" "$J_DG" --pha
```

Bảng pha **có** pha 5 `download_artifacts` và **có** pha 6 `step_script`: job đã tải artifact và đã chạy lệnh, nên chỉ còn hai cột sống. Bây giờ đi theo **hàng** — hàng `artifacts`, với đúng cặp khẳng định của buổi 05 QT 5.3:

```bash
job_tt "$J_CB"          # success  <- job nguồn XANH
art_http "$J_CB"        # 404      <- mà artifact KHÔNG TỒN TẠI
echo
job_log_sach "$J_CB" | grep -iE 'Uploading artifacts|no matching files|WARNING'
job_log_sach "$J_DG" | grep -iE 'Downloading artifacts|no such file|tar:'
git show origin/ca-1:.gitlab-ci.yml | grep -nA3 'artifacts:'
```

Cặp `success` + `404` là bằng chứng đủ để kết luận, và nó là **hai lệnh**, không phải một câu văn. Dòng `WARNING: ... no matching files` là nơi nền tảng đã nói ra sự thật ngay từ đầu — nó chỉ không làm job đỏ, và đó là định nghĩa của hỏng **im lặng**. So `artifacts:paths` với đường dẫn `script` thật sự tạo ra: khác một ký tự là đủ.

Viết báo cáo ca 1, giữ nguyên năm nhãn:

```bash
cat >> ~/lab07/bao-cao-go-roi.md <<MD

## Ca 1 — job dong-goi do: khong tim thay tep
- TRIEU CHUNG: dong-goi (stage goi) do voi failure_reason=script_failure, dong loi "tar: ket-qua: no such file". Job chuan-bi o stage truoc XANH.
- BANG CHUNG:
\$ job_tt $J_CB; art_http $J_CB
success
404
- NGUYEN NHAN: artifacts:paths cua chuan-bi tro duong dan KHONG ton tai (khac mot ky tu) -> archive rong; runner chi ghi WARNING chu khong doi ma thoat nen job xanh. dong-goi tai artifact rong roi hong o pha 6.
- CACH SUA: sua artifacts:paths cho khop; khang dinh cuoi script job nguon: test -s ket-qua/goi.txt || exit 1
- O: artifacts x pha 4-5 · im lang o job nguon, on ao o job sau · khong chan
MD
bash ~/lab07/kiem-bao-cao.sh 1
```

**CHECKPOINT 3 — ca 1: job nguồn `success` mà artifact trả `404`, và báo cáo ca 1 có đủ bốn nhãn cùng ít nhất một dòng lệnh.**

```bash
tt=$(job_tt "$J_CB"); ma=$(art_http "$J_CB")
so_ca=$(bash ~/lab07/kiem-bao-cao.sh 1 | awk -F= '/^TONG_CA_DAT/{print $2}')
canh=$(job_log_sach "$J_CB" | grep -ci 'no matching files')
{ [ "$tt" = success ] && [ "$ma" = 404 ] && [ "$so_ca" -ge 1 ] && [ "$canh" -ge 1 ]; } \
  && echo "CHECKPOINT 3 — ĐẠT (chuan-bi=$tt, artifact HTTP=$ma, canh bao no-matching-files=$canh, bao cao hop le=$so_ca)" \
  || echo "CHECKPOINT 3 — LỖI (tt=$tt cần success, ma=$ma cần 404, bao_cao=$so_ca cần ≥1 — xem §L9 dòng 6, 7)" \
  | tee -a ~/lab07/checkpoint.log
```

### 4.3. Ca 2 — job `trien-khai` xanh mà không có gì được triển khai (10 phút)

```bash
P2=$(tao_pipe ca-2); echo "pipeline ca-2 = $P2"
cho_pipeline "$P2" 300
job_bang_rong "$P2"
```

Bảng bước 0 lần này **không** cho gì cả: mọi job `success`, mọi ô `ly_do` là `-`. Cột `failure_reason` rỗng nghĩa là nền tảng không phát hiện gì, nên bằng chứng phải tìm trong **nội dung** job làm ra, không tìm trong trạng thái job — lần thứ **5** của khoá cho nguyên lý "job xanh không chứng minh gì":

```bash
J_TK=$(job_id "$P2" trien-khai)
bash ~/lab07/go-roi.sh "$PID" "$J_TK"
job_log_sach "$J_TK" | grep -E 'DO_DAI_TOKEN|MA_HTTP|trien khai'
art_tep "$J_TK" "ket-qua/ma-http.txt"
```

`DO_DAI_TOKEN=0` là con số của buổi 06 QT 5.2 quay lại nguyên vẹn: biến `protected` không được cấp cho nhánh không bảo vệ, job gọi API với token rỗng, nhận `401`, và `curl` trả mã thoát 0 nên `script` xanh. Hai lệnh đọc phía cấu hình khẳng định nốt cơ chế:

```bash
curl -sf "${H[@]}" "$A/variables" | jq -r '.[] | "\(.key)\tprotected=\(.protected)\tmasked=\(.masked)"'
curl -sf "${H[@]}" "$A/repository/branches/ca-2" | jq '{name, protected}'
```

Biến `DEPLOY_TOKEN` có `protected=true`, nhánh `ca-2` có `protected=false` — hai dòng đó ghép lại là nguyên nhân, và cả hai đều nằm **ngoài** repo nên đọc YAML bao lâu cũng không thấy (buổi 02 QT 4.1 — ranh giới hai tệp).

```bash
cat >> ~/lab07/bao-cao-go-roi.md <<MD

## Ca 2 — trien-khai XANH ma khong co gi duoc trien khai
- TRIEU CHUNG: trien-khai (nhanh ca-2) status=success, failure_reason="-", nhung moi truong dich khong doi. Khong co dong do nao trong ca pipeline.
- BANG CHUNG:
\$ job_log_sach $J_TK | grep -E 'DO_DAI_TOKEN|MA_HTTP'
DO_DAI_TOKEN=0
MA_HTTP=401
- NGUYEN NHAN: DEPLOY_TOKEN la bien protected muc project, nhanh ca-2 KHONG protected -> runner khong nhan bien, do dai 0. curl voi token rong nhan 401 nhung tra ma thoat 0 nen job xanh.
- CACH SUA: : "\${DEPLOY_TOKEN:?thieu DEPLOY_TOKEN}" o dong dau script, va [ "\$(cat ket-qua/ma-http.txt)" = 200 ] || exit 1. Nhanh feature can token thi bao ve nhanh, hoac dung bien khong protected rieng cho phi-prod.
- O: bien x pha 4-5 · im lang · khong chan
MD
bash ~/lab07/kiem-bao-cao.sh 2
```

**CHECKPOINT 4 — ca 2: job `success` với `failure_reason` rỗng, log in `DO_DAI_TOKEN=0`, biến `protected` trên nhánh không `protected`, và báo cáo ca 2 hợp lệ.**

```bash
tt2=$(job_tt "$J_TK")
do_dai=$(job_log_sach "$J_TK" | grep -oE 'DO_DAI_TOKEN=[0-9]+' | head -1 | cut -d= -f2)
bv=$(curl -sf "${H[@]}" "$A/variables" | jq -r '[.[] | select(.key=="DEPLOY_TOKEN") | .protected] | first // "khong-co"')
nh=$(curl -sf "${H[@]}" "$A/repository/branches/ca-2" | jq -r .protected)
so_ca=$(bash ~/lab07/kiem-bao-cao.sh 2 | awk -F= '/^TONG_CA_DAT/{print $2}')
{ [ "$tt2" = success ] && [ "${do_dai:-x}" = 0 ] && [ "$bv" = true ] && [ "$nh" = false ] && [ "$so_ca" -ge 2 ]; } \
  && echo "CHECKPOINT 4 — ĐẠT (job=$tt2, DO_DAI_TOKEN=$do_dai, bien protected=$bv, nhanh protected=$nh, bao cao=$so_ca)" \
  || echo "CHECKPOINT 4 — LỖI (tt=$tt2, do_dai=${do_dai:-trong}, bien=$bv, nhanh=$nh, bao_cao=$so_ca — xem §L9 dòng 8)" \
  | tee -a ~/lab07/checkpoint.log
```

### 4.4. Ca 3 — pipeline đứng ở `pending` và không ai báo (8 phút)

Pipeline ca 3 do giảng viên tạo trước giờ, nên nó đã `pending` sẵn vài chục phút — đúng hình dạng của sự cố thật:

```bash
P3=$(curl -sf "${H[@]}" "$A/pipelines?ref=ca-3&per_page=1" | jq -r '.[0].id')
job_bang_rong "$P3"
J_GPU=$(job_id "$P3" kiem-gpu)
job_json "$J_GPU" | jq '{status, runner, queued_duration, duration, started_at}'
```

Ba trường trả lời xong câu hỏi của QT 6.2: `runner` là `null`, `duration` là `null`, `queued_duration` lớn dần. **Chưa runner nào nhận job** — đây là `pending`, không phải treo; ai định tăng `timeout` hay sửa `script` đã đi sai hướng từ phút đầu. `go-roi.sh` nói ra điều đó bằng mã thoát riêng, vì job chưa được nhận thì **không có** `trace` để phân pha:

```bash
bash ~/lab07/go-roi.sh "$PID" "$J_GPU"; echo "ma thoat = $?"     # 4 = trace rong
git show origin/ca-3:.gitlab-ci.yml | grep -n -A2 'tags:'
curl -sf "${H[@]}" "$GITLAB/api/v4/runners/all?tag_list=gpu-lon" | jq 'length'
curl -sf "${H[@]}" "$GITLAB/api/v4/runners/all?status=online" | jq -r '.[] | "\(.id)\t\(.description)\ttags=\(.tag_list|join(","))\trun_untagged=\(.run_untagged // "?")"'
```

`tags: [gpu-lon]` trong YAML, **không** runner nào mang tag đó (`jq length` = 0) — hai lệnh, xong. Đây là buổi 02 QT 6.3 lần thứ **2**, và điều tệ nhất của nó không phải cách sửa mà là **không ai được báo**: GitLab không gửi thông báo cho một job chỉ vì nó chờ lâu. Chế độ hỏng số 6 của buổi: **im lặng** mà **có chặn**.

```bash
cat >> ~/lab07/bao-cao-go-roi.md <<MD

## Ca 3 — pipeline dung o pending hon 20 phut, khong ai bao
- TRIEU CHUNG: pipeline nhanh ca-3 o trang thai pending; job kiem-gpu khong bat dau, khong co log, khong co thong bao nao gui di.
- BANG CHUNG:
\$ job_json $J_GPU | jq -c '{status, runner, duration}'; curl -sf "\${H[@]}" "\$GITLAB/api/v4/runners/all?tag_list=gpu-lon" | jq length
{"status":"pending","runner":null,"duration":null}
0
- NGUYEN NHAN: job khai tags: [gpu-lon], khong runner nao mang tag do -> job khong duoc GIAO, nam trong hang doi vo han. runner=null phan biet ca nay voi ca treo giua script (QT 6.2).
- CACH SUA: bo tag hoac dang ky runner mang tag gpu-lon. Chan tai dien: job dinh ky doc GET /jobs?scope=pending, bao dong khi queued_duration > 600 giay.
- O: ha tang x pha 1 · im lang · CO chan (pipeline dung)
MD
bash ~/lab07/kiem-bao-cao.sh 3
```

**CHECKPOINT 5 — ca 3: job `pending` với `runner` rỗng và `duration` rỗng, `go-roi.sh` trả mã thoát 4, không runner nào mang tag của job, và đã có đủ ba báo cáo hợp lệ.**

```bash
jj=$(job_json "$J_GPU")
st=$(echo "$jj" | jq -r .status); rn=$(echo "$jj" | jq -r '.runner // "null"'); du=$(echo "$jj" | jq -r '.duration // "null"')
cho=$(echo "$jj" | jq -r '(.queued_duration // 0) | floor')
bash ~/lab07/go-roi.sh "$PID" "$J_GPU" >/dev/null 2>&1; mt=$?
sr=$(curl -sf "${H[@]}" "$GITLAB/api/v4/runners/all?tag_list=gpu-lon" | jq 'length')
so_ca=$(bash ~/lab07/kiem-bao-cao.sh 3 | awk -F= '/^TONG_CA_DAT/{print $2}')
{ [ "$st" = pending ] && [ "$rn" = null ] && [ "$du" = null ] && [ "$mt" -eq 4 ] \
  && [ "$sr" -eq 0 ] && [ "$so_ca" -ge 3 ]; } \
  && echo "CHECKPOINT 5 — ĐẠT (status=$st, runner=$rn, duration=$du, cho=${cho}s, go-roi ma thoat=$mt, runner co tag=$sr, bao cao=$so_ca/3)" \
  || echo "CHECKPOINT 5 — LỖI (status=$st, runner=$rn, ma_thoat=$mt cần 4, runner_co_tag=$sr cần 0, bao_cao=$so_ca cần 3 — xem §L9 dòng 9)" \
  | tee -a ~/lab07/checkpoint.log
```

### 4.5. Ba ô đã đóng — ghi vào bảng ba mươi hai ô (4 phút)

Ba ca vừa rồi đóng ba ô khác nhau, và **cả ba** đều được định vị bằng lệnh trước khi đọc log. Ghi lại vào `bang-32-o.md` để bảng của mình có dữ liệu thật, không chỉ có khung:

```bash
cd ~/lab07
cat >> bang-32-o.md <<MD

## Ba o da dong trong buoi (buoc 2)
| Ca | O | Lenh dinh vi o | Ket qua |
|---|---|---|---|
| 1 | artifacts x pha 4-5 | \`job_tt \$J; art_http \$J\` | success + 404 |
| 2 | bien x pha 4-5 | \`job_log_sach \$J \| grep DO_DAI_TOKEN\` | DO_DAI_TOKEN=0 |
| 3 | ha tang x pha 1 | \`job_json \$J \| jq .runner\` | null |
MD
grep -c '^| [123] |' bang-32-o.md
```

Ba lệnh trong bảng dài dưới 60 ký tự, và mỗi lệnh loại bỏ trọn một cột hoặc một hàng. Đó là toàn bộ nội dung của §4 tệp lý thuyết, đo bằng ba ca thật.

---

## L5. Bước 3 — Gỡ ca 4, 5, 6 (ca 5 là "xanh mà sai") (35 phút)

Kiểm chứng QT 4.2, QT 7.3.

| Ca | Nhánh | Triệu chứng học viên thấy | Ngân sách |
|---|---|---|---|
| 4 | `ca-4` | Push xong mà **pipeline không được tạo** — không có gì để mở ra xem | 8' |
| 5 | `ca-5` | Job xanh, pipeline xanh, nhưng nội dung triển khai là bản **cũ** | 15' |
| 6 | `ca-6` | Job bị cắt ở phút thứ 10 dù YAML ghi `timeout: 1h`; tệp tạm còn sót lại | 12' |

### 5.1. Ca 4 — pipeline không được tạo (8 phút)

Ca này không có job, không có `trace`, không có `failure_reason`. Ba lệnh đầu của quy trình bốn lệnh **đều không dùng được** — và đó chính là bài học: có một ô nằm **trước** cả tám pha, ô "pha 0" ở thời điểm `t0` của buổi 04, nơi nền tảng quyết định danh sách job. Bằng chứng ở ô đó không lấy từ job mà lấy từ **thông báo trả về lúc tạo pipeline**:

```bash
tao_pipe ca-4
curl -sf "${H[@]}" "$A/pipelines?ref=ca-4" | jq 'length'
```

`tao_pipe` in `KHONG-TAO-DUOC` kèm nguyên văn `message` của API, và số pipeline của nhánh `ca-4` là `0`. Ai push bằng `git push` thì thông báo tương đương xuất hiện ngay trên stderr của lệnh push — đọc nó, đừng bỏ qua. Lệnh thứ hai kiểm chứng độc lập, không cần tạo pipeline thật, bằng `ci/lint` với `dry_run` — đây là phép mô phỏng đúng bước `t0`:

```bash
NOI_DUNG=$(git fetch -q origin ca-4 && git show origin/ca-4:.gitlab-ci.yml)
curl -s "${H[@]}" --request POST --header 'Content-Type: application/json' \
  --data "$(jq -n --arg c "$NOI_DUNG" '{content:$c, dry_run:true, ref:"ca-4"}')" \
  "$A/ci/lint" | jq '{valid, errors, merged_yaml: (.merged_yaml != null)}'
```

`valid` là `false` và `errors` nói rõ job nào cần job nào không có mặt. Đối chứng bằng cách lint **cùng** nội dung với `ref` là `main`:

```bash
curl -s "${H[@]}" --request POST --header 'Content-Type: application/json' \
  --data "$(jq -n --arg c "$NOI_DUNG" '{content:$c, dry_run:true, ref:"main"}')" \
  "$A/ci/lint" | jq '{ref: "main", valid, errors}'
git show origin/ca-4:.gitlab-ci.yml | grep -nE 'rules:|needs:|if:'
```

Cùng một tệp YAML, `valid=false` trên `ca-4` và `valid=true` trên `main`. Vậy lỗi **không** nằm trong cú pháp YAML mà nằm ở việc `rules` làm một job biến mất trên nhánh này (buổi 04 QT 6.2) trong khi một job khác vẫn khai `needs` trỏ tới nó (buổi 04 QT 7.3). Con số `dry_run` và cặp `ca-4`/`main` là bằng chứng; "chắc do rules" không phải bằng chứng.

```bash
cat >> ~/lab07/bao-cao-go-roi.md <<'MD'

## Ca 4 — pipeline KHONG duoc tao
- TRIEU CHUNG: push len nhanh ca-4 xong khong co pipeline nao xuat hien; GET /pipelines?ref=ca-4 tra ve mang rong; khong co job, khong co trace, khong co failure_reason.
- BANG CHUNG:
$ curl -s "${H[@]}" -X POST -H 'Content-Type: application/json' --data "$(jq -n --arg c "$NOI_DUNG" '{content:$c,dry_run:true,ref:"ca-4"}')" "$A/ci/lint" | jq -c '{valid,errors}'
{"valid":false,"errors":["'kiem' job needs 'xay' job, but it was not added to the pipeline"]}
$ curl -s ... same content, ref:"main" ... | jq -c '{valid}'
{"valid":true}
- NGUYEN NHAN: rules cua job xay chi cho main nen tren ca-4 no bien mat tai t0; job kiem van khai needs: [xay] -> do thi phu thuoc khong dong, nen tang TU CHOI TAO pipeline thay vi tao roi bao loi.
- CACH SUA: needs: [{job: xay, optional: true}], hoac cho hai job dung CUNG khoi rules. Chan tai dien: POST /ci/lint?dry_run=true voi dung ref, chay trong job kiem YAML truoc khi merge.
- O: pha 0 (t0, truoc tam pha) · on ao voi nguoi push, im lang voi nguoi doc giao dien pipeline · CO chan
MD
bash ~/lab07/kiem-bao-cao.sh 4
```

**CHECKPOINT 6 — ca 4: nhánh `ca-4` không có pipeline nào, `ci/lint --dry_run` cho `valid=false` trên `ca-4` và `valid=true` trên `main`, và báo cáo ca 4 hợp lệ.**

```bash
so_pipe=$(curl -sf "${H[@]}" "$A/pipelines?ref=ca-4" | jq 'length')
lint() { curl -s "${H[@]}" --request POST --header 'Content-Type: application/json' \
  --data "$(jq -n --arg c "$NOI_DUNG" --arg r "$1" '{content:$c, dry_run:true, ref:$r}')" "$A/ci/lint"; }
v4=$(lint ca-4 | jq -r .valid); vm=$(lint main | jq -r .valid)
loi4=$(lint ca-4 | jq -r '.errors | join(" ")')
co_needs=$(printf '%s' "$loi4" | grep -ci 'needs')
so_ca=$(bash ~/lab07/kiem-bao-cao.sh 4 | awk -F= '/^TONG_CA_DAT/{print $2}')
{ [ "$so_pipe" -eq 0 ] && [ "$v4" = false ] && [ "$vm" = true ] && [ "$co_needs" -ge 1 ] && [ "$so_ca" -ge 4 ]; } \
  && echo "CHECKPOINT 6 — ĐẠT (pipeline tren ca-4=$so_pipe, valid[ca-4]=$v4, valid[main]=$vm, loi noi ve needs=$co_needs, bao cao=$so_ca/4)" \
  || echo "CHECKPOINT 6 — LỖI (so_pipe=$so_pipe cần 0, valid ca-4=$v4 cần false, valid main=$vm cần true, bao_cao=$so_ca — xem §L9 dòng 10)" \
  | tee -a ~/lab07/checkpoint.log
```

### 5.2. Ca 5 — không có gì đỏ, và bản triển khai là bản cũ (15 phút)

Đây là ca đặt ở **giữa** buổi có chủ ý (§L2 quyết định 4). Pipeline lần thứ nhất do giảng viên chạy trước giờ:

```bash
P5=$(curl -sf "${H[@]}" "$A/pipelines?ref=ca-5&per_page=5" | jq -r '.[0].id')
job_bang_rong "$P5"
J_X1=$(job_id "$P5" xay)
art_tep "$J_X1" "dist/phien-ban.json" | jq .
```

Mọi job `success`, mọi `ly_do` là `-`. Lần chạy đầu tiên **không** sai gì cả: hai trường trong `dist/phien-ban.json` bằng nhau. Cái ta cần là lần chạy thứ **hai** trên một commit khác — đó là phản xạ đúng khi có nghi vấn "bản triển khai là bản cũ", vì nó biến một lời kể thành một phép so:

```bash
cd ~/lab07
git fetch -q origin ca-5 && git checkout -qB ca-5 origin/ca-5
git commit -q --allow-empty -m "chay lai lan 2 de so sanh"
git push -q origin ca-5
sleep 8
P5B=$(curl -sf "${H[@]}" "$A/pipelines?ref=ca-5&per_page=1" | jq -r '.[0].id')
cho_pipeline "$P5B" 300
job_bang_rong "$P5B"
J_X2=$(job_id "$P5B" xay)
art_tep "$J_X2" "dist/phien-ban.json" | jq -r '"sha_trong_goi=\(.sha_trong_goi)  sha_dang_build=\(.sha_dang_build)"'
```

Hai giá trị **khác nhau** trong **một** tệp JSON của artifact, và cả pipeline vẫn xanh. Đó là bằng chứng: gói đem đi triển khai mang sha của lần build **trước**. Bây giờ tới QT 4.2 — tìm xem hai lần chạy khác nhau ở **dòng thứ mấy**, bằng máy chứ không bằng mắt:

```bash
trace_chuan "$J_X1" > ca5-lan1.txt
trace_chuan "$J_X2" > ca5-lan2.txt
wc -l ca5-lan1.txt ca5-lan2.txt
diff ca5-lan1.txt ca5-lan2.txt | head -20
diff ca5-lan1.txt ca5-lan2.txt | grep -m1 -E '^[0-9]+'
grep -n -iE 'Checking cache|Successfully extracted cache|Created cache|Restoring cache' ca5-lan2.txt
```

Dòng đầu tiên `diff` in ra là **vị trí phân kỳ** — con số đó nói vào việc, còn "log lần hai nó khác khác" thì không. Ngay tại vị trí đó có dòng `Successfully extracted cache`, thứ **không** có ở lần một. Đọc nốt YAML để thấy cơ chế:

```bash
git show origin/ca-5:.gitlab-ci.yml | grep -nE 'cache:|artifacts:|paths:|policy:|key:'
```

Cùng đường dẫn `dist/` xuất hiện ở **cả** `cache:paths` **và** `artifacts:paths`. Cache phục hồi `dist/` từ lần chạy trước ở pha 4, `script` chỉ tạo tệp mốc khi nó **chưa có** (`test -f ... ||`), rồi pha 8 đóng gói cả `dist/` thành artifact. Cache đã đi vào hợp đồng — đúng ranh giới buổi 05 QT 7.2 bị xoá, và không có một dòng đỏ nào để báo.

```bash
cat >> ~/lab07/bao-cao-go-roi.md <<MD

## Ca 5 — job XANH ma noi dung trien khai la ban CU
- TRIEU CHUNG: toan bo pipeline nhanh ca-5 success, failure_reason "-" o moi job, nhung goi trien khai mang sha cua lan build TRUOC.
- BANG CHUNG:
\$ art_tep $J_X2 "dist/phien-ban.json" | jq -r '.sha_trong_goi + " " + .sha_dang_build'
$(art_tep "$J_X2" "dist/phien-ban.json" | jq -r '.sha_trong_goi + " " + .sha_dang_build')
\$ diff ca5-lan1.txt ca5-lan2.txt | grep -m1 -E '^[0-9]+'
$(diff ca5-lan1.txt ca5-lan2.txt | grep -m1 -E '^[0-9]+')
- NGUYEN NHAN: dist/ nam o CA cache:paths VA artifacts:paths. Pha 4 phuc hoi dist/ tu cache lan truoc, script chi sinh tep moc khi chua ton tai, pha 8 dong goi ca dist/ thanh artifact -> cache (co che TOI UU) di vao HOP DONG giua hai job.
- CACH SUA: tach duong dan (cache giu .cache/, artifacts giu dist/), them "rm -rf dist" dong dau script, va khang dinh: jq -e --arg s "\$CI_COMMIT_SHORT_SHA" '.sha_trong_goi == \$s' dist/phien-ban.json
- O: cache x pha 4-5 · im lang · khong chan
MD
bash ~/lab07/kiem-bao-cao.sh 5
```

**CHECKPOINT 7 — ca 5: job `xay` `success` mà hai trường trong một tệp JSON của artifact khác nhau, `diff` hai `trace` chỉ ra dòng phân kỳ, và lần hai có dòng phục hồi cache mà lần một không có.**

```bash
tt5=$(job_tt "$J_X2")
cap=$(art_tep "$J_X2" "dist/phien-ban.json")
khac=$(printf '%s' "$cap" | jq -r 'if .sha_trong_goi != .sha_dang_build then "khac" else "giong" end')
dong=$(diff ~/lab07/ca5-lan1.txt ~/lab07/ca5-lan2.txt | grep -m1 -oE '^[0-9]+' || true)
c1=$(grep -ci 'Successfully extracted cache' ~/lab07/ca5-lan1.txt || true)
c2=$(grep -ci 'Successfully extracted cache' ~/lab07/ca5-lan2.txt || true)
so_ca=$(bash ~/lab07/kiem-bao-cao.sh 5 | awk -F= '/^TONG_CA_DAT/{print $2}')
{ [ "$tt5" = success ] && [ "$khac" = khac ] && [ -n "${dong:-}" ] \
  && [ "$c1" -eq 0 ] && [ "$c2" -ge 1 ] && [ "$so_ca" -ge 5 ]; } \
  && echo "CHECKPOINT 7 — ĐẠT (job=$tt5, hai truong JSON=$khac, dong phan ky dau tien=$dong, extracted-cache lan1=$c1 lan2=$c2, bao cao=$so_ca/5)" \
  || echo "CHECKPOINT 7 — LỖI (job=$tt5, JSON=$khac cần khac, dong_phan_ky=${dong:-trong}, cache lan1=$c1 lan2=$c2, bao_cao=$so_ca — xem §L9 dòng 11, 12)" \
  | tee -a ~/lab07/checkpoint.log
```

### 5.3. Ca 6 — bị cắt ở phút thứ 10 dù YAML ghi `timeout: 1h` (12 phút)

Pipeline ca 6 do giảng viên chạy trước giờ vì nó tốn **~15 phút** một mình:

```bash
P6=$(curl -sf "${H[@]}" "$A/pipelines?ref=ca-6&per_page=1" | jq -r '.[0].id')
job_bang_rong "$P6"
J_SL=$(job_id "$P6" sao-luu-du-lieu)
bash ~/lab07/go-roi.sh "$PID" "$J_SL"
```

Bước 0 cho ngay `ly_do` là `job_execution_timeout` — nhóm thứ ba trong bốn nhóm quy trách nhiệm của QT 4.3, tức việc của **người đặt hạn giờ**, không phải của người viết `script`. Khối tiêu đề của `go-roi.sh` in luôn `maximum_timeout` của runner đã nhận job, và đó là nửa còn lại của câu trả lời:

```bash
git show origin/ca-6:.gitlab-ci.yml | grep -nE 'timeout:|after_script:|sleep'
runner_han "$RID"
bash ~/lab07/go-roi.sh "$PID" "$J_SL" --json | jq -r '{duration, failure_reason, runner_maximum_timeout}'
```

YAML ghi `timeout: 1h` = 3.600 giây; runner ghi `maximum_timeout` = 600 giây; `duration` đo được ~600 giây cộng phần `after_script`. **Min thắng** (QT 6.1), và nguồn thắng nằm **ngoài** repo. Đây là con số 60 phút của tệp lý thuyết bị hạ xuống 10 phút cho vừa buổi học — cơ chế không đổi.

Nửa thứ hai của ca 6 là phần **im lặng**, và nó là phần đắt hơn:

```bash
bash ~/lab07/go-roi.sh "$PID" "$J_SL" --pha
bash ~/lab07/go-roi.sh "$PID" "$J_SL" --pha | awk -F'\t' '$2=="after_script"{print "after_script:", $4, "giay"}'
job_log_sach "$J_SL" | grep -c 'DON DEP XONG'
job_log_sach "$J_SL" | tail -12
```

`after_script` **có** chạy — nó có mặt trong bảng pha, tức nền tảng đã cho bước dọn dẹp một cơ hội sau khi `script` bị cắt (buổi 01 QT 4.3, lần thứ 2). Nhưng dòng `DON DEP XONG` **không** xuất hiện: `after_script` cũng bị cắt, bởi một hạn giờ **riêng** của nó. Số giây đo được là đại lượng loại (c) — **phải đo, không tra**. Nếu pha `after_script` không có `section_end` thì `go-roi.sh` in `-1`; lúc đó lấy `duration − 600` làm số đo và ghi rõ cách suy ra:

```bash
GIAY_AS=$(bash ~/lab07/go-roi.sh "$PID" "$J_SL" --pha | awk -F'\t' '$2=="after_script"{print $4}')
DUR6=$(bash ~/lab07/go-roi.sh "$PID" "$J_SL" --json | jq -r .duration)
[ "${GIAY_AS:-0}" -lt 0 ] && GIAY_AS=$(( DUR6 - 600 )) && echo "(suy tu duration - 600)"
echo "after_script bi cat sau $GIAY_AS giay — gia tri tham chieu cua Runner 17.7 la 300 giay"
```

Ghi ngay vào bảng hạn giờ, bước 4 sẽ dùng lại con số này:

```bash
cd ~/lab07
{ printf 'nguon\tgia_tri_giay\tlenh_doc\n'
  printf 'ca6.job.timeout (YAML)\t3600\tgit show origin/ca-6:.gitlab-ci.yml | grep timeout\n'
  printf 'ca6.runner.maximum_timeout\t%s\trunner_han $RID\n' "$(runner_han "$RID")"
  printf 'ca6.do_duoc_duration\t%s\tgo-roi.sh --json | jq .duration\n' "$DUR6"
  printf 'ca6.after_script_bi_cat\t%s\tgo-roi.sh --pha | awk $2=="after_script"\n' "$GIAY_AS"
} > bang-han-gio.tsv
column -t -s $'\t' bang-han-gio.tsv
```

```bash
cat >> ~/lab07/bao-cao-go-roi.md <<MD

## Ca 6 — job bi cat o phut thu 10 du YAML ghi timeout 1h, tep tam con sot
- TRIEU CHUNG: sao-luu-du-lieu do voi failure_reason=job_execution_timeout sau ~600 giay, trong khi YAML khai timeout: 1h. Log khong co dong DON DEP XONG, tep tam cua job con lai.
- BANG CHUNG:
\$ bash ~/lab07/go-roi.sh \$PID $J_SL --json | jq -c '{duration,failure_reason,runner_maximum_timeout}'; job_log_sach $J_SL | grep -c 'DON DEP XONG'
$(bash ~/lab07/go-roi.sh "$PID" "$J_SL" --json | jq -c '{duration,failure_reason,runner_maximum_timeout}')
0
- NGUYEN NHAN: han gio thuc te la MIN cua ba nguon (QT 6.1): project 3600, job 3600, runner.maximum_timeout 600 -> 600 thang, va nguon thang nam trong config.toml, NGOAI repo. Phan hai: after_script co han gio RIENG (do duoc $GIAY_AS giay) nen buoc don dep bi cat giua duong ma khong co dong log nao noi ra.
- CACH SUA: doc runner_han truoc khi tin timeout trong YAML; chia job sao luu thanh nhieu job ngan hon 600 giay hoac nang maximum_timeout; KHONG dat viec don dep quan trong vao after_script — dua vao mot job rieng.
- O: pha 6 (bi cat) va pha 7 (after_script) · nua dau on ao, nua sau IM LANG · co chan
MD
bash ~/lab07/kiem-bao-cao.sh 6
```

**CHECKPOINT 8 — ca 6: `failure_reason` là `job_execution_timeout`, hạn giờ thắng là 600 giây của runner chứ không phải 3.600 giây của YAML, `after_script` có chạy mà `DON DEP XONG` không in ra, và đã đủ **sáu** báo cáo hợp lệ với ít nhất sáu dòng lệnh.**

```bash
j6=$(bash ~/lab07/go-roi.sh "$PID" "$J_SL" --json)
ly_do6=$(echo "$j6" | jq -r .failure_reason)
han6=$(echo "$j6" | jq -r .runner_maximum_timeout)
dur6=$(echo "$j6" | jq -r .duration)
yaml6=$(git show origin/ca-6:.gitlab-ci.yml | grep -c 'timeout: 1h')
as_co=$(bash ~/lab07/go-roi.sh "$PID" "$J_SL" --pha | awk -F'\t' '$2=="after_script"' | wc -l | tr -d ' ')
don=$(job_log_sach "$J_SL" | grep -c 'DON DEP XONG' || true)
so_ca=$(bash ~/lab07/kiem-bao-cao.sh 6 | awk -F= '/^TONG_CA_DAT/{print $2}')
so_lenh=$(grep -c '^\$ ' ~/lab07/bao-cao-go-roi.md)
{ [ "$ly_do6" = job_execution_timeout ] && [ "$han6" = 600 ] && [ "$yaml6" -ge 1 ] \
  && [ "$dur6" -ge 570 ] && [ "$as_co" -ge 1 ] && [ "$don" -eq 0 ] \
  && [ "$so_ca" -ge 6 ] && [ "$so_lenh" -ge 6 ]; } \
  && echo "CHECKPOINT 8 — ĐẠT (ly_do=$ly_do6, runner=600s thang YAML=3600s, duration=${dur6}s, after_script co mat=$as_co pha, DON DEP XONG=$don lan, bao cao=$so_ca/6, dong lenh=$so_lenh)" \
  || echo "CHECKPOINT 8 — LỖI (ly_do=$ly_do6, han_runner=$han6 cần 600, duration=$dur6 cần ≥570, after_script=$as_co cần ≥1, DON DEP XONG=$don cần 0, bao_cao=$so_ca cần 6 — xem §L9 dòng 13, 14)" \
  | tee -a ~/lab07/checkpoint.log
```

Sáu báo cáo đã xong. Đọc lại cột `O` của cả sáu: sáu ô khác nhau, **bốn** ca im lặng, **hai** ca có chặn. Đó là bảng hai thuộc tính hỏng của buổi 01 QT 7.1 dùng lần thứ **7**, và hôm nay nó đã thành **một cột trong hiện vật nộp**, không còn là một khái niệm.

```bash
cd ~/lab07
ld() { job_json "$1" | jq -r '.failure_reason // "-"'; }
{ printf 'ca\tnhanh\tjob\ttt\tfailure_reason\to_trong_bang\n'
  printf '1\tca-1\tdong-goi\t%s\t%s\tartifacts x pha 4-5\n'  "$(job_tt "$J_DG")"  "$(ld "$J_DG")"
  printf '2\tca-2\ttrien-khai\t%s\t%s\tbien x pha 4-5\n'      "$(job_tt "$J_TK")"  "$(ld "$J_TK")"
  printf '3\tca-3\tkiem-gpu\t%s\t%s\tha tang x pha 1\n'       "$(job_tt "$J_GPU")" "$(ld "$J_GPU")"
  printf '4\tca-4\t(khong co job)\tkhong-tao-pipeline\tkhong-co-job\tpha 0 (t0)\n'
  printf '5\tca-5\txay\t%s\t%s\tcache x pha 4-5\n'            "$(job_tt "$J_X2")"  "$(ld "$J_X2")"
  printf '6\tca-6\tsao-luu-du-lieu\t%s\t%s\tpha 6 va pha 7\n' "$(job_tt "$J_SL")"  "$(ld "$J_SL")"
  printf '# ca 4 khong co job nao nen truong failure_reason KHONG TON TAI — ghi khong-co-job\n'
} > bang-6-ca.tsv
column -t -s $'\t' bang-6-ca.tsv
awk -F'\t' '$1 ~ /^[1-6]$/ {n++; v[$5]=1} END {printf "so dong ca=%d  so gia tri failure_reason khac nhau=%d\n", n, length(v)}' bang-6-ca.tsv
grep -c '^## Ca ' ~/lab07/bao-cao-go-roi.md
grep -c 'im lang' ~/lab07/bao-cao-go-roi.md
```

Cột `failure_reason` có **bốn** giá trị khác nhau trên sáu ca, và hai trong sáu ca có giá trị `-` — tức nền tảng **không** phân loại được gì. Bảng này là câu trả lời gọn nhất cho QT 4.3: trường đó phân loại rất tốt cho ca ồn ào, và **không nói gì** cho ca im lặng. Biết trước điều đó là biết khi nào phải bỏ bước 0 mà đi thẳng vào nội dung hiện vật.

---

## L6. Bước 4 — `retry` và `timeout`: đo cái gì sửa được, cái gì bị che (30 phút)

Kiểm chứng QT 5.1, QT 5.2, QT 5.3, QT 6.1, QT 6.2, QT 6.3.

Ba bước đầu là gỡ rối bị động: có ca hỏng thì đi tìm. Bước 4 đổi vai — ta đặt sẵn ba công cụ vận hành rồi **đo** xem chúng thật sự làm gì. Tất cả nằm trên một nhánh `do-luong`.

### 6.1. Dựng nhánh đo và đọc hạn giờ của ba nguồn (7 phút)

```bash
cd ~/lab07
git checkout -qB do-luong main
cat > .gitlab-ci.yml <<'YML'
stages: [do]

default:
  image: alpine:3.20
  interruptible: false

# QT 5.1 — LỖI XÁC ĐỊNH: cùng đầu vào, cùng image, cùng script -> cùng kết quả.
# retry: 2 nghĩa là chạy 3 lần, mỗi lần ~90 giây, tổng ~270 giây, thêm 0% cơ hội.
hong-xac-dinh:
  stage: do
  retry: 2
  script:
    - echo "lan chay job id $CI_JOB_ID"
    - sleep 88
    - ls /khong-co-thu-muc-nay

# QT 5.2 — retry:when giới hạn vào nhóm hạ tầng, nên script_failure KHÔNG được chạy lại.
hong-co-when:
  stage: do
  retry:
    max: 2
    when: [runner_system_failure, stuck_or_timeout_failure, api_failure]
  script:
    - echo "loi script that, khong phai loi ha tang"
    - exit 1

# QT 6.1 — nguồn thứ HAI của hạn giờ: khoá timeout của job. Min của ba nguồn thắng.
qua-han-gio:
  stage: do
  timeout: 2m
  script:
    - echo "bat dau $(date -u +%H:%M:%S)"
    - sleep 300
    - echo "KHONG BAO GIO IN RA DONG NAY"

# QT 6.3 — after_script có hạn giờ RIÊNG. Số giây là đại lượng phải ĐO.
don-dep-bi-cat:
  stage: do
  timeout: 10m
  script:
    - echo "script xong ngay"
  after_script:
    - echo "bat dau don dep"
    - sleep 60
    - echo "DON DEP XONG do-luong"
YML
git add -A && git commit -q -m "nhanh do luong buoc 4"
git push -q -f origin HEAD:refs/heads/do-luong
sleep 8
```

Trước khi chạy, đọc **cả ba** nguồn hạn giờ của QT 6.1. Nguồn thứ nhất và thứ ba lấy qua API; nguồn thứ hai nằm trong YAML vì GitLab CE 17.7 **không** phơi `timeout` của job ra API job — đó là một giới hạn thật, và nó chính là lý do người ta hay tin YAML là hạn giờ thật:

```bash
curl -sf "${H[@]}" "$A" | jq '{build_timeout, auto_cancel_pending_pipelines}'   # nguồn 1: project
git show origin/do-luong:.gitlab-ci.yml | grep -nE '^\s+timeout:'              # nguồn 2: job
runner_han "$RID"                                                              # nguồn 3: runner
```

```bash
P_DL=$(tao_pipe do-luong); echo "pipeline do-luong = $P_DL"
cho_pipeline "$P_DL" 900
job_bang_rong "$P_DL"
```

Bảng in ra ba điều đọc được ngay ở cột `ly_do`: `hong-xac-dinh` xuất hiện **ba** dòng (vì `include_retried=true`), `hong-co-when` xuất hiện **một** dòng, `qua-han-gio` có `job_execution_timeout`.

### 6.2. Đo QT 5.1 — job `exit 1` với `retry: 2` tốn bao nhiêu giây (8 phút)

```bash
curl -sf "${H[@]}" "$A/pipelines/$P_DL/jobs?include_retried=true&per_page=100" \
  | jq -r '[.[] | select(.name=="hong-xac-dinh")]
           | "so_lan=\(length)  tong_giay=\([.[].duration | floor] | add)  moi_lan=\([.[].duration | floor] | @csv)"'
so_lan_chay "$P_DL" hong-xac-dinh
so_lan_chay "$P_DL" hong-co-when
```

Ba lần chạy, tổng khoảng **270 giây** cho một job 90 giây — đúng phép nhân `retry + 1` của QT 5.1. Còn phần "**0%** cơ hội thêm" thì phải chứng minh, không được nói suông: ba lần chạy cho **đúng cùng một** dòng lỗi:

```bash
for j in $(curl -sf "${H[@]}" "$A/pipelines/$P_DL/jobs?include_retried=true&per_page=100" \
           | jq -r '.[] | select(.name=="hong-xac-dinh") | .id'); do
  printf '%s\t' "$j"; job_log_sach "$j" | grep -m1 -iE 'No such file|not found' || echo "(khong tim thay dong loi)"
done | tee ~/lab07/ba-lan-chay.txt
awk -F'\t' '{print $2}' ~/lab07/ba-lan-chay.txt | sort -u | wc -l
```

Số dòng lỗi **khác nhau** là `1`. Ba lần chạy, một dòng lỗi, 270 giây — đó là toàn bộ hoá đơn của `retry` đặt sai chỗ: **+180 giây** mỗi lần hỏng, và người chờ nhận cùng một tin sau 4,5 phút thay vì sau 1,5 phút.

Đối chứng QT 5.2 nằm ngay bên cạnh: `hong-co-when` cũng hỏng `script_failure`, cũng có `retry`, mà chạy **đúng một** lần — vì `when` giới hạn việc chạy lại vào nhóm hạ tầng. Đây là toàn bộ khác biệt giữa `retry` trần trụi và `retry:when`, đo bằng số lần chạy.

`dem-retry.sh` là công cụ trả lời câu QT 5.3 đòi trước khi cho phép đặt `retry` ở bất cứ đâu:

```bash
cat > ~/lab07/dem-retry.sh <<'SH'
#!/usr/bin/env bash
# dem-retry.sh [so_pipeline] [PID] — tỉ lệ job phải chạy lại (QT 5.3). Ngưỡng 2%.
# Nguồn dữ liệu: mọi lần chạy của mọi job trong N pipeline gần nhất (include_retried=true).
# Ra: một dòng có dấu %, cộng một dòng kết luận so với ngưỡng.
set -uo pipefail
N="${1:-20}"; P="${2:-${PID:?chua dat PID}}"
: "${GITLAB:?}"; : "${GITLAB_TOKEN:?}"
HH=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN"); AA="$GITLAB/api/v4/projects/$P"
tong=0; lai=0; so_pipe=0
for p in $(curl -sf "${HH[@]}" "$AA/pipelines?per_page=$N" | jq -r '.[].id'); do
  d=$(curl -sf "${HH[@]}" "$AA/pipelines/$p/jobs?include_retried=true&per_page=100" \
      | jq -r '[.[].name] as $n | "\($n|length) \(($n|length) - ($n|unique|length))"')
  set -- $d; tong=$((tong + ${1:-0})); lai=$((lai + ${2:-0})); so_pipe=$((so_pipe + 1))
done
awk -v t="$tong" -v l="$lai" -v p="$so_pipe" 'BEGIN {
  ti = (t > 0 ? 100 * l / t : 0); s = sprintf("%.1f", ti); sub(/\./, ",", s)
  printf "pipeline=%d  lan_chay=%d  lan_chay_lai=%d  ti_le=%s%%  nguong=2,0%%\n", p, t, l, s
  print (ti > 2 ? "KET LUAN: vuot nguong — mo ve ha tang, dung tang retry" \
                : "KET LUAN: duoi nguong — retry dang khong che gi dang ke")
}'
SH
bash ~/lab07/dem-retry.sh 20
```

Con số in ra **của lab này** sẽ cao bất thường, và đó là kết quả đúng: ta vừa cố ý tạo một job chạy lại ba lần trong một project chỉ có vài pipeline. Trên repo thật, cùng lệnh đó là con số phải theo dõi hằng tuần. Ghi cả hai vào hiện vật để nhớ rằng ngưỡng **2%** là ngưỡng theo **kinh nghiệm thực tế**, không phải hằng số của nền tảng.

**CHECKPOINT 9 — `retry: 2` cho lỗi xác định: đúng 3 lần chạy, tổng khoảng 270 giây, một dòng lỗi duy nhất; job có `retry:when` hạ tầng chạy đúng 1 lần; `dem-retry.sh` in ra một dòng có dấu `%`.**

```bash
so_lan=$(so_lan_chay "$P_DL" hong-xac-dinh)
tong_giay=$(curl -sf "${H[@]}" "$A/pipelines/$P_DL/jobs?include_retried=true&per_page=100" \
  | jq -r '[.[] | select(.name=="hong-xac-dinh") | .duration | floor] | add')
so_dong_loi=$(awk -F'\t' '{print $2}' ~/lab07/ba-lan-chay.txt | sort -u | wc -l | tr -d ' ')
so_lan_when=$(so_lan_chay "$P_DL" hong-co-when)
pc=$(bash ~/lab07/dem-retry.sh 20 | grep -c 'ti_le=.*%')
{ [ "$so_lan" -eq 3 ] && [ "$tong_giay" -ge 230 ] && [ "$tong_giay" -le 330 ] \
  && [ "$so_dong_loi" -eq 1 ] && [ "$so_lan_when" -eq 1 ] && [ "$pc" -ge 1 ]; } \
  && echo "CHECKPOINT 9 — ĐẠT (hong-xac-dinh chay $so_lan lan, tong ${tong_giay}s ~ 270s, $so_dong_loi dong loi duy nhat, hong-co-when chay $so_lan_when lan, dem-retry.sh in ti le)" \
  || echo "CHECKPOINT 9 — LỖI (so_lan=$so_lan cần 3, tong_giay=$tong_giay cần 230–330, dong_loi=$so_dong_loi cần 1, so_lan_when=$so_lan_when cần 1 — xem §L9 dòng 15, 16)" \
  | tee -a ~/lab07/checkpoint.log
```

### 6.3. Đo QT 6.1, QT 6.2, QT 6.3 — ba nguồn hạn giờ và hạn giờ riêng của `after_script` (15 phút)

Nguồn nào thắng thì phải nhìn thấy bằng số đo, không bằng suy luận. `qua-han-gio` khai `timeout: 2m` trong khi project cho 3.600 giây và runner cho 600 giây — min là **120 giây**:

```bash
J_QH=$(job_id "$P_DL" qua-han-gio)
bash ~/lab07/go-roi.sh "$PID" "$J_QH"
bash ~/lab07/go-roi.sh "$PID" "$J_QH" --json | jq -r '{duration, failure_reason, runner_maximum_timeout}'
job_log_sach "$J_QH" | grep -c 'KHONG BAO GIO IN RA DONG NAY'
```

Hoàn thiện `bang-han-gio.tsv` — bảng này là hiện vật, nên nó phải có **ba** dòng nguồn, **một** dòng min, và **một** dòng đo được để đối chiếu:

```bash
cd ~/lab07
BT=$(curl -sf "${H[@]}" "$A" | jq -r .build_timeout)
RH=$(runner_han "$RID")
JT=120
DUR_QH=$(bash ~/lab07/go-roi.sh "$PID" "$J_QH" --json | jq -r .duration)
MIN=$(printf '%s\n%s\n%s\n' "$BT" "$RH" "$JT" | sort -n | head -1)
{ printf 'nguon\tgia_tri_giay\tlenh_doc\n'
  printf 'nguon1.project.build_timeout\t%s\tcurl "$A" | jq .build_timeout\n' "$BT"
  printf 'nguon2.job.timeout (YAML)\t%s\tgit show origin/do-luong:.gitlab-ci.yml | grep timeout\n' "$JT"
  printf 'nguon3.runner.maximum_timeout\t%s\trunner_han $RID\n' "$RH"
  printf 'MIN_THANG\t%s\tmin cua ba nguon tren (QT 6.1)\n' "$MIN"
  printf 'do_duoc.duration qua-han-gio\t%s\tgo-roi.sh --json | jq .duration\n' "$DUR_QH"
  printf 'ca6.after_script_bi_cat\t%s\tdo o buoc 3, muc 5.3\n' "${GIAY_AS:-chua-do}"
  printf '# may do: %s · GitLab CE 17.7 · Runner 17.7\n' "$(hostname)"
} > bang-han-gio.tsv
column -t -s $'\t' bang-han-gio.tsv
```

Bây giờ QT 6.2 — hai trạng thái trông giống nhau, phân biệt bằng **một** trường. Đặt cạnh nhau job `pending` của ca 3 và job bị cắt của bước này:

```bash
for J in "$J_GPU" "$J_QH"; do
  job_json "$J" | jq -c '{ten: .name, tt: .status, runner: (.runner.id // null),
                           cho: (.queued_duration // 0 | floor), chay: .duration,
                           ly_do: (.failure_reason // "-")}'
done
```

Dòng thứ nhất: `runner` là `null`, `chay` là `null` — **chưa ai nhận**, sửa bằng `tags` hoặc bằng runner. Dòng thứ hai: `runner` có id, `chay` khoảng 120 giây, `ly_do` là `job_execution_timeout` — **đã nhận rồi mà không xong**, sửa bằng hạn giờ hoặc bằng cách chia job. Thêm runner cho ca thứ hai là vô ích; tăng `timeout` cho ca thứ nhất cũng vô ích.

Phần cuối là hạn giờ riêng của `after_script`, và đây là chỗ **phải đo**. Job `don-dep-bi-cat` có `after_script` ngủ 60 giây; với giá trị mặc định của Runner 17.7 (tham chiếu 300 giây) thì nó chạy đủ:

```bash
J_DD=$(job_id "$P_DL" don-dep-bi-cat)
bash ~/lab07/go-roi.sh "$PID" "$J_DD" --pha | awk -F'\t' '$2=="after_script"'
job_log_sach "$J_DD" | grep -c 'DON DEP XONG do-luong'    # 1 = chay du
```

**Phần tuỳ chọn — chứng minh nguồn của con số đó nằm NGOÀI repo.** Cắt hạn giờ `after_script` xuống 30 giây bằng `config.toml` rồi chạy lại **đúng một job** (không chạy lại cả pipeline — dùng `POST /jobs/:id/retry`, tốn ~70 giây thay vì ~460 giây):

```bash
# TUỲ CHỌN — đụng hạ tầng dùng chung. Đã sao lưu ở §L1 dòng 11. §L8.2 khôi phục BẮT BUỘC.
docker exec lab-runner sh -c 'grep -q RUNNER_AFTER_SCRIPT_TIMEOUT /etc/gitlab-runner/config.toml \
  || sed -i "0,/^\s*\[\[runners\]\]/s||[[runners]]\n  environment = [\"RUNNER_AFTER_SCRIPT_TIMEOUT=30s\"]|" /etc/gitlab-runner/config.toml'
docker exec lab-runner grep -n 'RUNNER_AFTER_SCRIPT_TIMEOUT' /etc/gitlab-runner/config.toml
docker restart lab-runner >/dev/null && sleep 20
J_DD2=$(curl -s "${H[@]}" --request POST "$A/jobs/$J_DD/retry" | jq -r .id)
cho_pipeline "$P_DL" 300
bash ~/lab07/go-roi.sh "$PID" "$J_DD2" --pha | awk -F'\t' '$2=="after_script"'
job_log_sach "$J_DD2" | grep -c 'DON DEP XONG do-luong'   # 0 = da bi cat
{ printf 'tuy_chon.after_script_han_30s\t%s\tconfig.toml environment RUNNER_AFTER_SCRIPT_TIMEOUT=30s\n' \
  "$(bash ~/lab07/go-roi.sh "$PID" "$J_DD2" --pha | awk -F'\t' '$2=="after_script"{print $4}')"; } \
  >> ~/lab07/bang-han-gio.tsv
```

Cùng một `.gitlab-ci.yml`, cùng một commit, hai kết quả khác nhau — biến số duy nhất nằm trong `config.toml`. Đó là ranh giới hai tệp của buổi 02 QT 4.1 đo bằng 30 giây. **Đường B** cho ai không sửa được `config.toml`: truyền cùng biến đó vào lúc tạo pipeline (`tao_pipe do-luong RUNNER_AFTER_SCRIPT_TIMEOUT=30s`) — đo được **cùng** hành vi, nhưng mất phần chứng minh rằng nguồn nằm ngoài repo; ghi rõ điều đó vào `bang-han-gio.tsv`. Chi tiết ở §L9 dòng 3.

**CHECKPOINT 10 — `bang-han-gio.tsv` có ba nguồn cùng dòng min, min bằng giá trị nhỏ nhất trong ba nguồn, `duration` đo được của `qua-han-gio` khớp min trong biên 25%, dòng sau `sleep` không in ra, và trường `runner` phân biệt được job `pending` với job bị cắt.**

```bash
F=~/lab07/bang-han-gio.tsv
n_nguon=$(grep -cE '^nguon[123]\.' "$F")
minf=$(awk -F'\t' '$1=="MIN_THANG"{print $2}' "$F")
min3=$(awk -F'\t' '$1 ~ /^nguon[123]\./ {print $2}' "$F" | sort -n | head -1)
durq=$(awk -F'\t' '$1 ~ /^do_duoc/ {print $2}' "$F")
sot=$(job_log_sach "$J_QH" | grep -c 'KHONG BAO GIO IN RA DONG NAY' || true)
rn_p=$(job_json "$J_GPU" | jq -r '.runner // "null"')
rn_t=$(job_json "$J_QH"  | jq -r 'if .runner then "co-id" else "null" end')
as_ca6=$(awk -F'\t' '$1=="ca6.after_script_bi_cat"{print $2}' "$F")
{ [ "$n_nguon" -eq 3 ] && [ "$minf" = "$min3" ] \
  && [ "$durq" -ge $((minf * 75 / 100)) ] && [ "$durq" -le $((minf * 125 / 100)) ] \
  && [ "$sot" -eq 0 ] && [ "$rn_p" = null ] && [ "$rn_t" = co-id ] && [ -n "$as_ca6" ]; } \
  && echo "CHECKPOINT 10 — ĐẠT (3 nguon, MIN=${minf}s khop min ba nguon, duration do duoc=${durq}s, dong sau sleep in $sot lan, pending runner=$rn_p / bi cat runner=$rn_t, after_script ca6=${as_ca6}s)" \
  || echo "CHECKPOINT 10 — LỖI (n_nguon=$n_nguon cần 3, MIN=$minf vs min3=$min3, duration=$durq vs MIN=$minf, sot=$sot cần 0, runner pending=$rn_p / cat=$rn_t — xem §L9 dòng 17, 18)" \
  | tee -a ~/lab07/checkpoint.log
```

---

## L7. Bước 5 — `interruptible` và `resource_group`: đo giây tiết kiệm và chặn deploy chồng (15 phút)

Kiểm chứng QT 7.1, QT 7.2.

Hai dòng cấu hình, hai phép đo, và hai kết luận trái ngược nhau về giá: `interruptible` **trả lại** giây, `resource_group` **tiêu** giây. Cả hai đều đúng, và biết mình đang mua gì là toàn bộ nội dung của bước này.

### 7.1. Đo QT 7.1 — bật `interruptible` cho tất cả, rồi bỏ đúng một job (8 phút)

Trước khi đổi cấu hình project, sao lưu — đây là hạ tầng của project, và §L8.3 sẽ khôi phục từ tệp này:

```bash
cd ~/lab07
curl -sf "${H[@]}" "$A" | jq '{auto_cancel_pending_pipelines, build_timeout}' > project.bak
cat project.bak
curl -sf "${H[@]}" --request PUT "$A" \
  --data 'auto_cancel_pending_pipelines=enabled' | jq .auto_cancel_pending_pipelines
```

```bash
git checkout -qB do-huy main
cat > .gitlab-ci.yml <<'YML'
stages: [xay, kiem]

default:
  image: alpine:3.20
  interruptible: true      # QT 7.1 — khai ở default: là cách rẻ nhất, áp cả lượt

.viec: &viec
  script:
    - echo "$CI_JOB_NAME cua commit $CI_COMMIT_SHORT_SHA"
    - sleep 90

xay-1: { stage: xay, <<: *viec }
xay-2: { stage: xay, <<: *viec }
xay-3: { stage: xay, <<: *viec }
kiem-1: { stage: kiem, <<: *viec }
kiem-2: { stage: kiem, <<: *viec }
kiem-3: { stage: kiem, <<: *viec }
YML
git add -A && git commit -q -m "vong 1 — moi job interruptible"
git push -q -f origin HEAD:refs/heads/do-huy
for i in 1 2 3; do
  git commit -q --allow-empty -m "commit $i cua vong 1"
  git push -q origin HEAD:refs/heads/do-huy
  sleep 8
done
sleep 45
curl -sf "${H[@]}" "$A/pipelines?ref=do-huy&per_page=5" \
  | jq -r '.[] | "\(.id)\t\(.status)\t\(.sha[0:8])"' | column -t
```

Ba pipeline: bản mới nhất đang chạy, hai bản cũ ở trạng thái `canceled`. Đếm job bị huỷ và quy ra giây — trần lý thuyết của ca này là **2 pipeline × 6 job × 90 giây = 1.080 giây**, số đo thật nhỏ hơn vì các job đang chạy đã tiêu một phần thời gian trước khi bị huỷ:

```bash
CU=$(curl -sf "${H[@]}" "$A/pipelines?ref=do-huy&per_page=5" | jq -r '.[1:3][].id')
{ printf 'vong\tpipeline\tjob\ttrang_thai\tda_chay_giay\ttiet_kiem_giay\n'
  for p in $CU; do
    curl -sf "${H[@]}" "$A/pipelines/$p/jobs?per_page=100" \
      | jq -r --arg p "$p" '.[] | select(.status=="canceled")
          | ["1", $p, .name, .status, ((.duration // 0) | floor),
             (90 - ((.duration // 0) | floor))] | @tsv'
  done
} > bang-huy.tsv
column -t -s $'\t' bang-huy.tsv
awk -F'\t' 'NR>1 {n++; t += $6} END {printf "job bi huy=%d  tiet kiem do duoc=%d giay  tran ly thuyet=1080 giay\n", n, t}' bang-huy.tsv
```

Vòng 2 phá bỏ con số vừa đo: bỏ đánh dấu ở **đúng một** job của stage đầu — job đó **đã bắt đầu chạy** khi commit mới tới, nên nền tảng không dám huỷ pipeline nữa:

```bash
sed -i 's|^xay-3: { stage: xay, <<: \*viec }|xay-3: { stage: xay, interruptible: false, <<: *viec }|' .gitlab-ci.yml
grep -n 'xay-3' .gitlab-ci.yml
git add -A && git commit -q -m "vong 2 — mot job KHONG interruptible"
git push -q origin HEAD:refs/heads/do-huy
sleep 20
for i in 1 2; do
  git commit -q --allow-empty -m "commit $i cua vong 2"
  git push -q origin HEAD:refs/heads/do-huy
  sleep 8
done
sleep 40
curl -sf "${H[@]}" "$A/pipelines?ref=do-huy&per_page=6" | jq -r '.[] | "\(.id)\t\(.status)"' | column -t
V2=$(curl -sf "${H[@]}" "$A/pipelines?ref=do-huy&per_page=6" | jq -r '.[1:3][].id')
HUY2=0
for p in $V2; do
  HUY2=$(( HUY2 + $(curl -sf "${H[@]}" "$A/pipelines/$p/jobs?per_page=100" \
          | jq '[.[] | select(.status=="canceled")] | length') ))
done
echo "vong 2 — so job bi huy = $HUY2   (vong 1: $(awk -F'\t' 'NR>1' bang-huy.tsv | wc -l | tr -d ' '))"
printf 'vong2\t-\t-\tkhong-huy\t0\t0\n' >> bang-huy.tsv
```

Năm trong sáu job vẫn đánh dấu `interruptible: true` mà tiết kiệm được **0 giây**. Giá trị của tính năng này là **nhị phân theo cả pipeline**, không cộng dồn theo từng job — QT 7.1 đo bằng hai con số cạnh nhau. Và hệ quả vận hành nằm ở chỗ ngược lại: job deploy **phải** là job không đánh dấu, nên trên một pipeline có deploy đang chạy thì `interruptible` không trả lại gì. Đó là cái giá đúng phải trả, không phải một cấu hình sai.

### 7.2. Đo QT 7.2 — hai pipeline deploy cùng lúc, có và không có `resource_group` (7 phút)

Hai nhánh để hai pipeline cùng tồn tại mà không bị huỷ lẫn nhau (auto-cancel chỉ tác động trong **cùng** một ref):

```bash
cd ~/lab07
git checkout -qB do-hang-doi main
cat > .gitlab-ci.yml <<'YML'
stages: [trien-khai]

default:
  image: alpine:3.20
  interruptible: false

# QT 7.2 — cơ chế loại trừ lẫn nhau DUY NHẤT của GitLab CI.
trien-khai-staging:
  stage: trien-khai
  resource_group: staging
  script:
    - echo "BAT DAU $CI_COMMIT_REF_NAME $(date -u +%s)"
    - sleep 45
    - echo "XONG $CI_COMMIT_REF_NAME $(date -u +%s)"

# ĐỐI CHỨNG — cùng công việc, KHÔNG có resource_group.
doi-chung-khong-nhom:
  stage: trien-khai
  script:
    - echo "BAT DAU doi-chung $(date -u +%s)"
    - sleep 45
YML
git add -A && git commit -q -m "hang doi resource_group"
git push -q -f origin HEAD:refs/heads/do-hang-doi
git push -q -f origin HEAD:refs/heads/do-hang-doi-b
sleep 6
PA=$(tao_pipe do-hang-doi); PB=$(tao_pipe do-hang-doi-b)
echo "hai pipeline song song: $PA va $PB"
sleep 25
curl -sf "${H[@]}" "$A/resource_groups/staging/upcoming_jobs" | jq -r '.[] | "\(.id)\t\(.name)\t\(.status)"'
cho_pipeline "$PA" 300; cho_pipeline "$PB" 300
```

Đọc mốc thời gian của bốn job và tính phần **chồng nhau** bằng giây. Đây là phép đo, không phải quan sát:

```bash
lay() { curl -sf "${H[@]}" "$A/pipelines/$1/jobs?per_page=20" \
  | jq -r --arg p "$1" '.[] | [$p, .name, .started_at, .finished_at] | @tsv'; }
{ lay "$PA"; lay "$PB"; } | tee ~/lab07/moc-hang-doi.tsv | column -t -s $'\t'

chong() {   # chồng(giây) giữa hai job cùng tên trên hai pipeline
  awk -F'\t' -v ten="$1" '$2==ten {
      cmd = "date -u -d " $3 " +%s"; cmd | getline b; close(cmd)
      cmd = "date -u -d " $4 " +%s"; cmd | getline e; close(cmd)
      B[++k] = b; E[k] = e
    } END {
      lo = (E[1] < E[2] ? E[1] : E[2]); hi = (B[1] > B[2] ? B[1] : B[2])
      c = lo - hi; print (c > 0 ? c : 0)
    }' ~/lab07/moc-hang-doi.tsv
}
echo "chong nhau — co resource_group : $(chong trien-khai-staging) giay"
echo "chong nhau — doi chung khong nhom: $(chong doi-chung-khong-nhom) giay"
```

Cặp có `resource_group` chồng nhau **0 giây**: hai pipeline song song thành **1** hàng đợi, và cái giá là pipeline thứ hai chờ thêm đúng bằng thời lượng job kia (~45 giây). Cặp đối chứng chồng nhau **~45 giây** — đó chính là hai lần deploy đè lên nhau, và bản **kết thúc sau** thắng bất kể commit của nó mới hay cũ. Không có dòng log nào báo việc đó: chế độ hỏng **im lặng** và **không chặn**, ô nguy hiểm nhất của buổi.

```bash
{ printf 'phep_do\tchong_giay\tket_luan\n'
  printf 'co_resource_group\t%s\thai pipeline thanh mot hang doi\n' "$(chong trien-khai-staging)"
  printf 'khong_resource_group\t%s\thai lan deploy de nhau, ban ket thuc sau thang\n' "$(chong doi-chung-khong-nhom)"
} >> ~/lab07/bang-huy.tsv
tail -4 ~/lab07/bang-huy.tsv
```

**CHECKPOINT 11 — vòng 1 huỷ được ≥ 6 job và quy ra được số giây tiết kiệm, vòng 2 huỷ 0 job, cặp job cùng `resource_group` chồng nhau 0 giây, cặp đối chứng chồng nhau > 0 giây.**

```bash
huy1=$(awk -F'\t' 'NR>1 && $1=="1"' ~/lab07/bang-huy.tsv | wc -l | tr -d ' ')
tiet=$(awk -F'\t' 'NR>1 && $1=="1" {t += $6} END {print t+0}' ~/lab07/bang-huy.tsv)
c_rg=$(awk -F'\t' '$1=="co_resource_group"{print $2}' ~/lab07/bang-huy.tsv)
c_kh=$(awk -F'\t' '$1=="khong_resource_group"{print $2}' ~/lab07/bang-huy.tsv)
{ [ "$huy1" -ge 6 ] && [ "${HUY2:-99}" -eq 0 ] && [ "$tiet" -gt 0 ] \
  && [ "$c_rg" -eq 0 ] && [ "$c_kh" -gt 0 ]; } \
  && echo "CHECKPOINT 11 — ĐẠT (vong 1 huy $huy1 job = $tiet giay tiet kiem, tran ly thuyet 1.080 giay; vong 2 huy ${HUY2} job; chong nhau co resource_group=${c_rg}s, doi chung=${c_kh}s)" \
  || echo "CHECKPOINT 11 — LỖI (huy1=$huy1 cần ≥6, huy2=${HUY2:-?} cần 0, tiet_kiem=$tiet cần >0, chong_rg=$c_rg cần 0, chong_doi_chung=$c_kh cần >0 — xem §L9 dòng 19, 20)" \
  | tee -a ~/lab07/checkpoint.log
```

---

## L8. Nộp sản phẩm và dọn dẹp (10 phút)

### L8.1. Khôi phục `maximum_timeout` của runner — BẮT BUỘC

Runner là hạ tầng dùng chung: để nguyên `600` giây thì **mọi** job của **mọi** project bị cắt ở phút thứ 10 từ mai. Khôi phục đúng giá trị đã sao lưu ở §L1 dòng 10:

```bash
RID_CU=$(jq -r .id ~/lab07/han-gio-runner.bak)
MT_CU=$(jq -r '.maximum_timeout // "null"' ~/lab07/han-gio-runner.bak)
echo "khoi phuc runner $RID_CU ve maximum_timeout=$MT_CU"
if [ "$MT_CU" = null ]; then
  curl -sf "${H[@]}" --request PUT "$GITLAB/api/v4/runners/$RID_CU" --data 'maximum_timeout=' | jq .maximum_timeout
else
  curl -sf "${H[@]}" --request PUT "$GITLAB/api/v4/runners/$RID_CU" --data "maximum_timeout=$MT_CU" | jq .maximum_timeout
fi
runner_han "$RID_CU"
```

### L8.2. Khôi phục `config.toml` — BẮT BUỘC nếu đã làm phần tuỳ chọn của bước 4

Dòng `environment = ["RUNNER_AFTER_SCRIPT_TIMEOUT=30s"]` áp cho mọi job của runner. Để nó lại thì mọi `after_script` của mọi buổi sau bị cắt ở giây thứ 30 — một lỗi **im lặng** mà chính ta vừa dựng ra để học:

```bash
docker exec lab-runner sh -c 'test -f /etc/gitlab-runner/config.toml.buoi07.bak \
  && cp /etc/gitlab-runner/config.toml.buoi07.bak /etc/gitlab-runner/config.toml \
  && rm -f /etc/gitlab-runner/config.toml.buoi07.bak && echo "da khoi phuc" || echo "khong co ban sao luu"'
docker restart lab-runner >/dev/null && sleep 20
docker exec lab-runner grep -c 'RUNNER_AFTER_SCRIPT_TIMEOUT' /etc/gitlab-runner/config.toml || echo "0 — sach"
```

### L8.3. Dọn cấu hình mức project

```bash
curl -s "${H[@]}" --request DELETE "$A/variables/DEPLOY_TOKEN" -o /dev/null -w 'xoa DEPLOY_TOKEN: %{http_code}\n'
curl -sf "${H[@]}" "$A/variables" | jq 'length'                       # phải là 0
curl -s "${H[@]}" --request POST "$A/pipelines/$P3/cancel" | jq -r '"pipeline ca-3: " + .status'
AC=$(jq -r .auto_cancel_pending_pipelines ~/lab07/project.bak)
curl -sf "${H[@]}" --request PUT "$A" --data "auto_cancel_pending_pipelines=$AC" \
  | jq '{auto_cancel_pending_pipelines}'
```

Job `pending` của ca 3 **không tự chết**: nó nằm trong hàng đợi tới khi có người huỷ hoặc tới khi project bị xoá. Đó là đặc điểm của chế độ hỏng số 6, và cũng là lý do bước dọn này không phải việc hình thức.

### L8.4. Gom hiện vật và kiểm bằng lệnh

```bash
DICH=~/gitlab-portfolio/07-go-roi-pipeline
mkdir -p "$DICH"; cd ~/lab07
git show origin/do-luong:.gitlab-ci.yml > do-luong.gitlab-ci.yml
cp -f bao-cao-go-roi.md go-roi.sh dem-retry.sh kiem-bao-cao.sh cong-cu07.sh \
      bang-32-o.md bang-6-ca.tsv bang-han-gio.tsv bang-huy.tsv \
      do-luong.gitlab-ci.yml checkpoint.log "$DICH"/ 2>/dev/null
ls -l "$DICH"
```

```bash
cat > ~/lab07/kiem-hien-vat.sh <<'SH'
#!/usr/bin/env bash
# Kiểm hiện vật nộp của buổi 07. Dùng: bash kiem-hien-vat.sh [thu_muc]
D="${1:-$HOME/gitlab-portfolio/07-go-roi-pipeline}"
loi=0
bao() { if [ "$1" = 0 ]; then printf '  ĐẠT   %s\n' "$2"; else printf '  LỖI   %s\n' "$2"; loi=$((loi+1)); fi; }

for f in bao-cao-go-roi.md go-roi.sh dem-retry.sh bang-32-o.md bang-6-ca.tsv \
         bang-han-gio.tsv bang-huy.tsv do-luong.gitlab-ci.yml checkpoint.log; do
  [ -s "$D/$f" ]; bao $? "có $f và khác rỗng"
done

# HIỆN VẬT CỐT LÕI 1 — sáu báo cáo, mỗi cái đủ bốn nhãn và có dòng lệnh
bash "$HOME/lab07/kiem-bao-cao.sh" 6 "$D/bao-cao-go-roi.md" >/dev/null
bao $? "bao-cao-go-roi.md có đủ 6 ca hợp lệ (4 nhãn + ≥1 dòng lệnh mỗi ca)"
awk '/^\$ /{n++} END {exit !(n>=6)}' "$D/bao-cao-go-roi.md"
bao $? "có ít nhất 6 dòng bằng chứng dạng lệnh (QT 7.3)"
grep -qc 'im lang' "$D/bao-cao-go-roi.md" && [ "$(grep -c '^- O:' "$D/bao-cao-go-roi.md")" -ge 6 ]
bao $? "mỗi ca có dòng O ghi ô trong bảng và hai thuộc tính hỏng"
! grep -q 'DIEN-TEN-VAO-DAY' "$D/bao-cao-go-roi.md"
bao $? "đã ghi người gỡ và máy đo"

# HIỆN VẬT CỐT LÕI 2 — go-roi.sh
bash -n "$D/go-roi.sh"; bao $? "go-roi.sh không lỗi cú pháp"
grep -q 'section_start' "$D/go-roi.sh" && grep -q 'failure_reason' "$D/go-roi.sh"
bao $? "go-roi.sh đọc mốc section_* và trường failure_reason"
grep -q -- '--pha' "$D/go-roi.sh" && grep -q -- '--json' "$D/go-roi.sh"
bao $? "go-roi.sh có ba định dạng đầu ra"

bash -n "$D/dem-retry.sh"; bao $? "dem-retry.sh không lỗi cú pháp"
grep -q 'include_retried=true' "$D/dem-retry.sh"
bao $? "dem-retry.sh đếm trên include_retried=true, không đếm lần cuối"

awk -F'\t' '$1 ~ /^[1-6]$/ {n++; v[$5]=1} END {exit !(n==6 && length(v)>=4)}' "$D/bang-6-ca.tsv"
bao $? "bang-6-ca.tsv có 6 dòng ca và ≥4 giá trị khác nhau ở cột failure_reason"
awk -F'\t' '$1=="MIN_THANG"{m=$2} $1 ~ /^nguon[123]\./ {n++; if (s=="" || $2+0<s+0) s=$2}
            END {exit !(n==3 && m+0==s+0)}' "$D/bang-han-gio.tsv"
bao $? "bang-han-gio.tsv có 3 nguồn và MIN khớp nguồn nhỏ nhất (QT 6.1)"
awk -F'\t' '$1=="co_resource_group"{a=$2} $1=="khong_resource_group"{b=$2}
            END {exit !(a+0==0 && b+0>0)}' "$D/bang-huy.tsv"
bao $? "bang-huy.tsv chứng minh resource_group chồng 0 giây, đối chứng chồng >0"
awk -F'\t' 'NR>1 && $1=="1" {n++} END {exit !(n>=6)}' "$D/bang-huy.tsv"
bao $? "bang-huy.tsv có ≥6 job bị huỷ ở vòng 1 (QT 7.1)"
[ "$(grep -c '^\$ ' "$D/bang-32-o.md")" -ge 12 ]
bao $? "bang-32-o.md có ≥12 dòng lệnh chạy được"
[ "$(grep -c 'ĐẠT' "$D/checkpoint.log")" -ge 12 ]
bao $? "checkpoint.log có đủ 12 dòng ĐẠT"

# HẠ TẦNG DÙNG CHUNG đã trả về nguyên trạng
if [ -s "$HOME/lab07/han-gio-runner.bak" ]; then
  cu=$(jq -r '.maximum_timeout // "null"' "$HOME/lab07/han-gio-runner.bak")
  rid=$(jq -r .id "$HOME/lab07/han-gio-runner.bak")
  nay=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/$rid" \
        | jq -r '.maximum_timeout // "null"')
  [ "$cu" = "$nay" ]; bao $? "maximum_timeout của runner đã khôi phục ($cu)"
fi
if docker exec lab-runner test -f /etc/gitlab-runner/config.toml.buoi07.bak 2>/dev/null; then
  bao 1 "còn tệp config.toml.buoi07.bak — chưa khôi phục §L8.2"
else
  docker exec lab-runner grep -c RUNNER_AFTER_SCRIPT_TIMEOUT /etc/gitlab-runner/config.toml 2>/dev/null | grep -qx 0 \
    || docker exec lab-runner grep -q RUNNER_AFTER_SCRIPT_TIMEOUT /etc/gitlab-runner/config.toml 2>/dev/null
  if docker exec lab-runner grep -q RUNNER_AFTER_SCRIPT_TIMEOUT /etc/gitlab-runner/config.toml 2>/dev/null; then
    bao 1 "config.toml còn dòng RUNNER_AFTER_SCRIPT_TIMEOUT"
  else
    bao 0 "config.toml không còn dấu vết phần tuỳ chọn"
  fi
fi
so_bien=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
          "$GITLAB/api/v4/projects/${PID:-0}/variables" | jq 'if type=="array" then length else 0 end')
[ "${so_bien:-0}" -eq 0 ]; bao $? "biến mức project đã xoá hết (DEPLOY_TOKEN)"

echo "---"
[ "$loi" -eq 0 ] && echo "CHECKPOINT 12 — ĐẠT (moi hien vat hop le, ha tang dung chung da tra nguyen trang)" \
                 || echo "CHECKPOINT 12 — LỖI ($loi loi)"
exit "$loi"
SH
bash ~/lab07/kiem-hien-vat.sh | tee -a ~/lab07/checkpoint.log
```

**CHECKPOINT 12 — mọi hiện vật hợp lệ về NỘI DUNG, và hạ tầng dùng chung đã trả về nguyên trạng.**

Đoạn trên **là** checkpoint 12. Nó không đếm tệp mà kiểm bốn thứ khó gian hơn: sáu báo cáo có đủ dòng lệnh bằng chứng, `MIN` của bảng hạn giờ khớp phép min của ba nguồn, cặp `resource_group` chồng nhau đúng 0 giây, và `maximum_timeout` của runner bằng đúng giá trị trong tệp sao lưu.

### L8.5. Xoá nhánh và project — chỉ chạy sau khi CHECKPOINT 12 ĐẠT

```bash
for b in ca-1 ca-2 ca-3 ca-4 ca-5 ca-6 khoi-dong do-luong do-huy do-hang-doi do-hang-doi-b; do
  curl -s "${H[@]}" --request DELETE "$A/repository/branches/$b" -o /dev/null -w "$b %{http_code}\n"
done
curl -sf "${H[@]}" --request DELETE "$A" && echo "da xoa project $PID"
```

Giữ lại thư mục `~/lab07` tới hết buổi 14: **buổi 08** dùng `go-roi.sh` để đo `duration` từng job và tìm đường găng, **buổi 14** dùng lại cả `go-roi.sh` và `dem-retry.sh`, **buổi 46** dùng `dem-retry.sh` cho chỉ số DORA. Chỉ xoá phần nặng:

```bash
rm -f ~/lab07/lan-do.txt ~/lab07/lan-xanh.txt ~/lab07/ca5-lan1.txt ~/lab07/ca5-lan2.txt
du -sh ~/lab07
```

---

## L9. Xử lý sự cố thường gặp trong lab

| # | Triệu chứng | Nguyên nhân | Cách khắc phục |
|---|---|---|---|
| 1 | §L1 dòng 4 đếm được ít hơn 11 hàm | Chưa nạp `cong-cu.sh` của buổi 05, hoặc đã xoá `~/lab05` | Lấy lại từ `~/gitlab-portfolio/05-artifact-va-cache/`; không có thì viết lại **11** hàm theo §L3.1 buổi 05 — đừng viết hàm mới trùng tên |
| 2 | §L1 dòng 6 không thấy `dat-bien.sh` | Chưa làm buổi 06 hoặc đã dọn | Tạo biến trực tiếp: `curl -X POST "${H[@]}" "$A/variables" --data 'key=DEPLOY_TOKEN&value=t0k3n-that&protected=true&masked=false'` |
| 3 | **ĐƯỜNG B** — `GET /runners/:id` trả `403`, hoặc không `docker exec` được vào runner | Token không phải admin (trường `maximum_timeout` chỉ admin đọc được), hoặc runner không nằm trên máy của học viên | Đi đường B: (a) lấy hạn giờ runner từ dòng đầu `trace` (`Running with gitlab-runner … job timeout`) hoặc từ giảng viên đọc hộ; (b) đo hạn giờ `after_script` bằng biến pipeline `tao_pipe do-luong RUNNER_AFTER_SCRIPT_TIMEOUT=30s` thay cho `config.toml`; (c) `bang-han-gio.tsv` ghi **2** nguồn thay vì 3, thêm một dòng `# nguon3 khong doc duoc: 403 — đi đường B` và **vẫn** đạt CHECKPOINT 10 nếu MIN khớp min của hai nguồn còn lại |
| 4 | `go-roi.sh` in `KHONG-CO-SECTION` rồi thoát mã 5 | Phiên bản runner đặt tên section khác, hoặc job quá ngắn nên chưa kịp ghi section nào | `job_log "$J" \| grep -oE 'section_start:[0-9]+:[a-z_]+' \| sort -u` rồi bổ tên đó vào mảng `pha[...]` trong `go-roi.sh` |
| 5 | `--pha` in ít hơn 5 pha | Đang chạy trên job không có cache và không có artifact (chỉ 4 pha) | Chạy CHECKPOINT 1 trên `mau-xanh` của nhánh `khoi-dong` — job đó có đủ cả cache lẫn artifact |
| 6 | `art_http` trả `404` cho job **đã** có artifact | Token thiếu scope `api`, hoặc artifact đã hết `expire_in` | `job_json "$J" \| jq .artifacts_expire_at`; `null` thì là vấn đề token |
| 7 | Ca 1: job `chuan-bi` **đỏ** thay vì xanh | `script` có lệnh cuối trả mã thoát khác 0 nên hỏng ồn ào, mất tính chất "im lặng" của ca | Chỉ để sai **đường dẫn** trong `artifacts:paths`; `script` phải kết thúc bằng một lệnh thành công |
| 8 | Ca 2: `DO_DAI_TOKEN` khác `0` | Nhánh `ca-2` đang được bảo vệ, hoặc biến `DEPLOY_TOKEN` tạo thiếu `protected=true` | `curl "$A/repository/branches/ca-2" \| jq .protected` phải là `false`; và `jq` trên `/variables` phải cho `protected=true` |
| 9 | Ca 3: job **chạy** chứ không `pending` | Có runner mang tag `gpu-lon`, hoặc runner đặt `run_untagged=false` mà vẫn nhận | Đổi tag ca 3 sang một chuỗi chắc chắn không ai dùng (`gpu-lon-$RANDOM`), push lại nhánh |
| 10 | Ca 4: pipeline **vẫn** được tạo | `rules` không loại được job `xay` trên nhánh này (thường vì `$CI_COMMIT_BRANCH` khớp), nên đồ thị `needs` vẫn đóng | `ci/lint` với `dry_run=true` và `ref=ca-4`, đọc `merged_yaml` để xem job `xay` còn hay mất; sửa `rules` cho đúng |
| 11 | Ca 5: hai trường JSON **giống nhau** | Đang đọc artifact của lần chạy **thứ nhất**, hoặc cache đã bị xoá khỏi runner | Phải có commit mới giữa hai lần chạy; kiểm cache còn không: `grep -c 'Successfully extracted cache' ca5-lan2.txt` |
| 12 | `diff` hai `trace` in ra rỗng | Đang so cùng một job id hai lần | So `J_X1` với `J_X2` — hai id **khác nhau** thuộc hai pipeline khác nhau |
| 13 | Ca 6: `duration` khoảng 3.600 giây, không phải 600 | `maximum_timeout` của runner chưa được hạ, nên `timeout: 1h` của YAML thắng | `curl -X PUT "${H[@]}" "$GITLAB/api/v4/runners/$RID" --data 'maximum_timeout=600'`; GitLab 17.7 **không nhận** giá trị nhỏ hơn 600 |
| 14 | Ca 6: dòng `DON DEP XONG` **có** in ra | Hạn giờ `after_script` của bản runner này lớn hơn thời gian ngủ trong `after_script` | Đây là **số đo**, không phải lỗi: ghi giá trị đo được vào `bang-han-gio.tsv`, và tăng `sleep` trong `after_script` của ca 6 lên trên giá trị đó rồi chạy lại |
| 15 | `hong-xac-dinh` chỉ hiện **1** lần | Quên `include_retried=true` trong truy vấn, hoặc `retry` bị ghi đè bởi `default:` | So hai truy vấn có và không có tham số đó; `so_lan_chay` đã có sẵn tham số |
| 16 | Tổng giây của ba lần chạy lệch xa 270 | Máy chạy nhanh/chậm hơn máy tham chiếu, hoặc `sleep 88` đã bị đổi | Ghi **số đo thật** vào hiện vật, đừng chép 270; điều phải giữ là tỉ lệ `retry + 1` = 3 lần |
| 17 | `bang-han-gio.tsv` có `MIN_THANG` không khớp | Một nguồn đọc ra `null` và bị `sort -n` xếp đầu | Thay `null` bằng giá trị mặc định đọc được ở giao diện project rồi ghi rõ trong bảng là giá trị mặc định |
| 18 | `qua-han-gio` **không** bị cắt | `timeout: 2m` đặt sai cấp trong YAML nên hợp lệ mà không có tác dụng | Đọc tệp **sau phân giải** bằng `ci/lint` (buổi 03 QT 4.3), đừng đọc YAML thô |
| 19 | Vòng 1 của bước 5 huỷ **0** job | `auto_cancel_pending_pipelines` chưa `enabled`, hoặc ba commit push cách nhau quá xa nên pipeline trước đã xong | Kiểm `curl "$A" \| jq .auto_cancel_pending_pipelines`; push ba commit trong vòng 30 giây, và giữ `sleep 90` trong job |
| 20 | Hai job cùng `resource_group` **vẫn** chồng nhau | Hai nhánh khai tên nhóm khác nhau, hoặc đang so hai job **khác** tên | `grep -n resource_group` trên cả hai nhánh; tên nhóm phải giống đúng từng ký tự |
| Dòng cuối | §L1 dòng 13 báo project `lab07-go-roi` đã tồn tại | Buổi trước chưa dọn, hoặc có người trong lớp tạo trước | Xoá (`DELETE /projects/:id`) rồi tạo lại, hoặc đặt tên `lab07-go-roi-$(whoami)` và đặt lại `PID` cho đúng |

---

## L10. Bài tập mở rộng

Sáu bài đầu làm được với hạ tầng đã có. Bài 7 và 8 đi trước tới buổi 08 và buổi 46.

**BT1 — `go-roi.sh` trên repo thật.** Chạy `go-roi.sh` cho **job đỏ gần nhất** của một repo đang chạy thật của bạn, đọc cả ba định dạng đầu ra.
*Câu hỏi phải trả lời:* pha nào hỏng, `failure_reason` là gì, và bao nhiêu **giây** trôi qua ở các pha **trước** pha 6? Con số cuối là phần thời gian mà mọi việc sửa `script` đều không chạm tới được.

**BT2 — Tỉ lệ chạy lại thật.** `bash dem-retry.sh 100 <PID repo thật>`.
*Câu hỏi phải trả lời:* tỉ lệ là bao nhiêu **phần trăm**, nó ở trên hay dưới ngưỡng **2%**, và job nào chiếm nhiều lần chạy lại nhất?

**BT3 — Săn `retry` không có `when`.** Chạy `grep -n 'retry' .gitlab-ci.yml` trên mọi repo bạn có quyền đọc.
*Câu hỏi phải trả lời:* có **bao nhiêu** khối `retry` thiếu `when`, và mỗi khối đó đang nhân tối đa bao nhiêu **giây** cho mỗi lần hỏng (dùng `duration` trung vị của job đó)?

**BT4 — Ba nguồn hạn giờ của repo thật.** Lập lại `bang-han-gio.tsv` cho một repo thật với đủ ba nguồn.
*Câu hỏi phải trả lời:* hạn giờ **thật** đang áp cho job dài nhất là bao nhiêu giây, và nó lớn hơn `duration` **lớn nhất trong 30 ngày** của job đó bao nhiêu phần trăm? Dưới 50% là vùng sẽ hỏng vào ngày phát hành.

**BT5 — Đo hạn giờ `after_script` của bản runner bạn dùng.** Một job có `after_script` ngủ tăng dần 60, 180, 400 giây.
*Câu hỏi phải trả lời:* giá trị **giây** mà từ đó dòng cuối `after_script` không còn in ra là bao nhiêu, và nó có bằng 300 giây tham chiếu của Runner 17.7 không?

**BT6 — Ca thứ bảy.** Tự dựng một ca hỏng **im lặng** mới, không trùng sáu ca của buổi, rồi viết báo cáo bốn dòng cho nó.
*Câu hỏi phải trả lời:* dòng bằng chứng của bạn là **lệnh** nào, và `bash kiem-bao-cao.sh 7` có in `TONG_CA_DAT=7` không?

**BT7 — Ba con số cho buổi 08.** Chạy `go-roi.sh --json` cho **mọi** job của một pipeline thật, gom `duration` theo `stage`.
*Câu hỏi phải trả lời:* tổng các stage là bao nhiêu giây, đường dài nhất **theo dữ liệu** là bao nhiêu giây, và chênh lệch là bao nhiêu? Đây chính là con số buổi 08 sẽ đi lấy bằng `needs`.

**BT8 — `interruptible` trên repo thật.** Thêm `interruptible: true` vào `default:`, bật huỷ pipeline dư, để **nguyên** job deploy không đánh dấu, rồi đọc phút runner của tuần trước và tuần sau.
*Câu hỏi phải trả lời:* tiết kiệm bao nhiêu **phút runner** một tuần, và bao nhiêu pipeline **không** được huỷ vì job deploy đang chạy? Tỉ số hai con số đó là giá trị thật của QT 7.1 trên repo của bạn.

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| # | Hiện vật | Điểm | Tiêu chí đạt điểm tối đa |
|---|---|---|---|
| 1 | `bao-cao-go-roi.md` **(cốt lõi)** | 30 | Đủ **6** ca; mỗi ca có bốn nhãn của QT 7.3 và **≥ 1** dòng `$ ` là lệnh đã in ra được, kèm đầu ra thật; mỗi ca có dòng `O:` ghi ô trong bảng ba mươi hai ô cùng hai thuộc tính hỏng; ghi rõ người gỡ và máy đo |
| 2 | `go-roi.sh` **(cốt lõi)** | 20 | Không lỗi cú pháp; đọc mốc `section_start`/`section_end` từ `trace` **thô**; in `failure_reason`, `runner`, `queued_duration`, `maximum_timeout`; có ba định dạng `--bang`/`--pha`/`--json`; mã thoát riêng cho job `pending` |
| 3 | `bang-han-gio.tsv` | 12 | **3** nguồn hạn giờ (hoặc 2 nguồn kèm dòng ghi lý do đi đường B), dòng `MIN_THANG` khớp phép min, dòng `duration` đo được, và số giây `after_script` **tự đo** |
| 4 | `bang-huy.tsv` | 10 | Vòng 1 có **≥ 6** job `canceled` kèm giây tiết kiệm; vòng 2 ghi `0`; hai dòng chồng nhau `0` giây và `> 0` giây của cặp `resource_group` và cặp đối chứng |
| 5 | `bang-32-o.md` | 10 | **4** hàng đường vào, **≥ 12** dòng lệnh đã chạy được, ô pha 0, và bảng ba ô đã đóng ở bước 2 |
| 6 | `dem-retry.sh` | 8 | Không lỗi cú pháp; đếm trên `include_retried=true`; in một dòng có `%` và một dòng kết luận so với ngưỡng **2%** |
| 7 | `bang-6-ca.tsv` | 5 | **6** dòng ca, cột `failure_reason` có **≥ 4** giá trị khác nhau, cột ô trong bảng điền đủ |
| 8 | `checkpoint.log` | 5 | Đủ **12** dòng `ĐẠT`, theo thứ tự |
| | **Tổng** | **100** | |

**Điểm trừ — dẫn chiếu bảng Bẫy hay gặp ở §9 tệp lý thuyết:**

| Lỗi | Trừ | Bẫy số |
|---|---|---|
| Báo cáo có dòng bằng chứng là **câu văn** thay vì lệnh in ra được | **−5 mỗi ca** | 14 |
| Kết luận nguyên nhân một ca mà không có lệnh định vị pha trước đó | −8 | 1 |
| Đọc log bằng mắt trên giao diện, không có `trace` tải về để `diff` (ca 5) | −8 | 2 |
| Không đọc `failure_reason` trước khi mở log (thiếu cột `ly_do` trong hiện vật) | −6 | 3 |
| Ghi `270 giây` từ tệp lý thuyết thay vì tổng `duration` **tự đo** | **−12** | 4 |
| Kết luận `retry` "giúp pipeline ổn định hơn", hoặc đề xuất `retry` không kèm `when` | −10 | 5, 6 |
| `bang-han-gio.tsv` chỉ có nguồn trong YAML, không có nguồn runner và không ghi lý do | −10 | 7 |
| Nhập chung ca 3 (`pending`) với ca 6 (bị cắt) thành một loại sự cố | **−10** | 8 |
| Kết luận `after_script` chạy đủ mà không có số giây đo được | −6 | 9 |
| Kết luận `interruptible` tiết kiệm theo từng job (thiếu vòng 2 huỷ 0 job) | −8 | 10, 11 |
| Không đo được cặp đối chứng **không** `resource_group` | −6 | 12, 13 |
| Đã hạ `maximum_timeout` mà không khôi phục | **−15** | — |
| Đã sửa `config.toml` mà không khôi phục | **−15** | — |
| Nộp thiếu một trong hai hiện vật cốt lõi | **chưa nộp bài** | — |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| L1 | Điều kiện tiên quyết (làm trước giờ, không tính vào 150') | — |
| L2 | Kiến trúc bài lab (đọc trước giờ) | — |
| L3 | Bước 1 — Dựng bộ công cụ: `go-roi.sh`, `failure_reason`, bảng ba mươi hai ô | 25' |
| L4 | Bước 2 — Gỡ ca 1, 2, 3 và viết ba báo cáo bốn dòng | 35' |
| L5 | Bước 3 — Gỡ ca 4, 5, 6 (ca 5 là "xanh mà sai") | 35' |
| L6 | Bước 4 — `retry` và `timeout`: đo cái gì sửa được, cái gì bị che | 30' |
| L7 | Bước 5 — `interruptible` và `resource_group`: đo giây tiết kiệm và chặn deploy chồng | 15' |
| L8 | Nộp sản phẩm và dọn dẹp | 10' |
| L9–L11 | Xử lý sự cố · bài tập mở rộng · tiêu chí chấm (tra cứu, ngoài giờ) | — |
| **Tổng** | | **150'** |

---

## Phụ lục GV — dựng sáu ca hỏng (HỌC VIÊN KHÔNG ĐỌC TRƯỚC KHI XONG BƯỚC 3)

Giảng viên chạy khối dưới đây **trước giờ ít nhất 20 phút** — ca 6 tốn ~15 phút một mình. Học viên tự học một mình thì chép nguyên khối vào tệp và chạy **mà không đọc nội dung**; đọc rồi thì ghi một dòng vào hiện vật là đã đọc và bỏ phần điểm thời gian ở §L11.

```bash
cat > ~/dung-sau-ca.sh <<'GV'
#!/usr/bin/env bash
# dung-sau-ca.sh — dựng project lab07-go-roi với sáu ca hỏng. Chạy TRƯỚC giờ ≥ 20 phút.
set -uo pipefail
. "$HOME/.gitlab-lab.env"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")
PID=$(curl -sf "${H[@]}" --request POST \
      "$GITLAB/api/v4/projects?name=lab07-go-roi&initialize_with_readme=true" | jq -r .id)
A="$GITLAB/api/v4/projects/$PID"
RID=$(curl -sf "${H[@]}" "$GITLAB/api/v4/runners?status=online" | jq -r '.[0].id')
echo "PID=$PID RID=$RID"

# hạ tầng dùng chung: hạn giờ runner 600 giây (nửa đầu của ca 6). GitLab 17.7 không nhận < 600.
curl -sf "${H[@]}" --request PUT "$GITLAB/api/v4/runners/$RID" --data 'maximum_timeout=600' | jq .maximum_timeout
# biến protected cho ca 2 (buổi 06 QT 5.2)
curl -sf "${H[@]}" --request POST "$A/variables" \
  --data 'key=DEPLOY_TOKEN&value=t0k3n-that-cua-prod&protected=true&masked=false' | jq -r .key

W=$(mktemp -d); cd "$W"
git init -q -b main
git config user.email gv@lab.local; git config user.name "giang vien"
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$A" | jq -r .path_with_namespace).git"
echo "# lab07" > README.md; git add -A; git commit -q -m base
git push -q -f origin HEAD:refs/heads/main

day_ca() { git add -A; git commit -q -m "$1" --allow-empty; git push -q -f origin "HEAD:refs/heads/$1"; }

# ---- CA 1: artifacts:paths sai đường dẫn -> archive rỗng, job nguồn XANH (buổi 05 QT 5.3)
cat > .gitlab-ci.yml <<'Y'
stages: [chuan-bi, goi]
default: { image: alpine:3.20 }
chuan-bi:
  stage: chuan-bi
  script: ["mkdir -p ket-qua", "echo $CI_COMMIT_SHORT_SHA > ket-qua/goi.txt", "ls -la ket-qua"]
  artifacts: { paths: [ket_qua/], expire_in: 1 day }
dong-goi:
  stage: goi
  script: ["ls -la", "tar czf goi.tgz ket-qua"]
Y
day_ca ca-1

# ---- CA 2: biến protected rỗng trên nhánh không protected (buổi 06 QT 5.2)
cat > .gitlab-ci.yml <<'Y'
stages: [trien-khai]
default: { image: alpine:3.20 }
trien-khai:
  stage: trien-khai
  script:
    - apk add --no-cache curl >/dev/null
    - 'echo "DO_DAI_TOKEN=${#DEPLOY_TOKEN}"'
    - mkdir -p ket-qua
    - 'curl -s -o /dev/null -w "%{http_code}" --header "PRIVATE-TOKEN: $DEPLOY_TOKEN" "$CI_API_V4_URL/projects/$CI_PROJECT_ID/variables" > ket-qua/ma-http.txt'
    - 'echo "MA_HTTP=$(cat ket-qua/ma-http.txt)"'
    - echo "trien khai xong"
  artifacts: { paths: [ket-qua/], expire_in: 1 day }
Y
day_ca ca-2

# ---- CA 3: tags không khớp runner nào -> pending vô hạn (buổi 02 QT 6.3)
cat > .gitlab-ci.yml <<'Y'
stages: [kiem]
kiem-gpu:
  stage: kiem
  image: alpine:3.20
  tags: [gpu-lon]
  script: ["echo se khong bao gio chay"]
Y
day_ca ca-3

# ---- CA 4: needs trỏ job đã biến mất vì rules -> KHÔNG tạo được pipeline (buổi 04 QT 6.2, 7.3)
cat > .gitlab-ci.yml <<'Y'
stages: [xay, kiem]
default: { image: alpine:3.20 }
xay:
  stage: xay
  rules: [{ if: '$CI_COMMIT_BRANCH == "main"' }]
  script: ["echo chi chay tren main"]
kiem:
  stage: kiem
  needs: [xay]
  script: ["echo kiem"]
Y
day_ca ca-4

# ---- CA 5: cùng đường dẫn ở cả cache và artifacts -> XANH MÀ SAI (buổi 05 QT 7.2)
cat > .gitlab-ci.yml <<'Y'
stages: [xay, trien-khai]
default: { image: alpine:3.20 }
xay:
  stage: xay
  cache: { key: ca-5, paths: [dist/] }
  script:
    - apk add --no-cache jq >/dev/null
    - mkdir -p dist
    - test -f dist/sha-cu.txt || echo "$CI_COMMIT_SHORT_SHA" > dist/sha-cu.txt
    - jq -n --arg cu "$(cat dist/sha-cu.txt)" --arg moi "$CI_COMMIT_SHORT_SHA" '{sha_trong_goi:$cu, sha_dang_build:$moi}' > dist/phien-ban.json
    - cat dist/phien-ban.json
  artifacts: { paths: [dist/], expire_in: 1 day }
trien-khai:
  stage: trien-khai
  script:
    - apk add --no-cache jq >/dev/null
    - 'echo "trien khai ban $(jq -r .sha_trong_goi dist/phien-ban.json)"'
Y
day_ca ca-5

# ---- CA 6: config.toml cắt hạn giờ + after_script có hạn giờ riêng (buổi 02 QT 4.1, buổi 01 QT 4.3)
cat > .gitlab-ci.yml <<'Y'
stages: [sao-luu]
sao-luu-du-lieu:
  stage: sao-luu
  image: alpine:3.20
  timeout: 1h
  script:
    - echo "bat dau sao luu"
    - mkdir -p /tmp/tam && touch /tmp/tam/dang-chay.lock
    - sleep 3000
  after_script:
    - echo "bat dau don dep"
    - sleep 400
    - rm -f /tmp/tam/dang-chay.lock
    - echo "DON DEP XONG"
Y
day_ca ca-6

tao() { curl -s "${H[@]}" --request POST --data "ref=$1" "$A/pipeline" | jq -r '.id // .message'; }
echo "ca-6 (~15 phut): $(tao ca-6)"
echo "ca-3 (pending) : $(tao ca-3)"
echo "ca-5 (lan 1)   : $(tao ca-5)"
echo "XONG. Hoc vien tu tao pipeline cho ca-1, ca-2, ca-4."
GV
bash ~/dung-sau-ca.sh
```

**Bảng nguyên nhân — chỉ đọc sau khi lớp đã nộp sáu báo cáo:**

| Ca | Nguyên nhân thật | Ô trong bảng | Buổi nguồn | Im lặng? | Chặn? |
|---|---|---|---|---|---|
| 1 | `artifacts:paths` trỏ `ket_qua/` trong khi `script` tạo `ket-qua/` → archive rỗng, job nguồn xanh | artifacts × pha 4–5 | buổi 05 QT 5.3 | Im ở job nguồn | Không chặn |
| 2 | `DEPLOY_TOKEN` là biến `protected`, nhánh `ca-2` không `protected` → độ dài 0, `curl` nhận 401 mà mã thoát 0 | biến × pha 4–5 | buổi 06 QT 5.2 | **Im lặng** | Không chặn |
| 3 | `tags: [gpu-lon]` không khớp runner nào → job không được giao | hạ tầng × pha 1 | buổi 02 QT 6.3 | **Im lặng** | **Có chặn** |
| 4 | `rules` xoá job `xay` trên nhánh này, `kiem` vẫn khai `needs: [xay]` → đồ thị không đóng, pipeline bị từ chối tạo | pha 0 (`t0`) | buổi 04 QT 6.2, 7.3 | Ồn với người push | **Có chặn** |
| 5 | `dist/` nằm ở **cả** `cache:paths` và `artifacts:paths`; tệp mốc chỉ sinh khi chưa có → artifact mang sha của lần build trước | cache × pha 4–5 | buổi 05 QT 7.2 | **Im lặng** | Không chặn |
| 6 | `maximum_timeout=600` trong hạ tầng runner cắt `timeout: 1h`; `after_script` bị cắt bởi hạn giờ riêng nên mất bước dọn | pha 6 và pha 7 | buổi 02 QT 4.1, buổi 01 QT 4.3 | Nửa sau **im lặng** | Có chặn |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---



**Quy tắc cho giảng viên:**

- Chọn **5–7 câu** trong 12, ưu tiên câu 🔥. Trả lời **bằng miệng, không nhìn tài liệu**. **Gọi ngẫu nhiên**; ai thiếu thì gọi người kế tiếp bổ sung, giảng viên không trả lời thay.
- Sáu câu chen vào đã thành phản xạ của khoá: **"bao nhiêu?"** (01) · **"sửa ở tệp nào?"** (02) · **"đi qua đường nào trong bốn đường?"** (03) · **"quyết định ở `t0` hay sau `t0`?"** (04) · **"cái đó ai giữ — server hay runner?"** (05) · **"biến này thắng ở nấc nào?"** (06). Buổi này thêm câu thứ bảy, và nó chốt cả giai đoạn 1: **"bằng chứng của bạn là lệnh nào?"** Ai kể một câu chuyện thay vì đọc một lệnh thì tối đa **2 điểm**, dù cơ chế đúng.
- Câu **4** là câu **tính toán**. Buộc thí sinh nói ra con số; "tuỳ trường hợp" mà không kèm phép tính thì tối đa **1 điểm**.

**Thang điểm mỗi câu:**

| Điểm | Nghĩa |
|---|---|
| 0 | Không trả lời được, hoặc sai cơ chế |
| 1 | Nhắc được tên khái niệm, không nêu cơ chế |
| 2 | Nêu đúng cơ chế |
| 3 | Đúng cơ chế **và** một con số, hoặc **và** một ca nó không đúng |

**Hai lỗi làm trần điểm cả buổi là 1:**

1. **Nói `retry` giúp được với lỗi xác định, hoặc đề xuất `retry` mà không nhắc `when`.** Nó nhân phút runner lên **`retry` + 1** lần để nhận đúng cùng một tin, và nuốt luôn sự cố hạ tầng thật (QT 5.1, QT 5.2).
2. **Nói job `pending` và job hết hạn giờ là cùng một loại sự cố.** Hai trạng thái ở hai phía khác nhau của pha 1; người tin chúng giống nhau sẽ thêm runner để sửa job treo ở `docker pull`, hoặc tăng `timeout` cho job chưa ai nhận (QT 6.2).

**Bốn câu phân loại thật:**

| Câu | Phân loại điều gì |
|---|---|
| 2 | Người **phân biệt được lỗi xác định với lỗi chập chờn**. Chưa vận hành thì đáp "đặt `retry` cho chắc"; đã vận hành thì đòi chạy lại **hai** lần rồi so hai kết quả |
| 3 | Người **thấy `retry` là cơ chế che**. Lọc người coi nó là "làm pipeline ổn định hơn" — nó ổn định bằng cách làm ta không thấy sự cố |
| 9 | Người **đã từng bị deploy chồng**. Chưa bị thì đáp "deploy hỏng, chạy lại"; đã bị thì hỏi ngay hai lần deploy có chồng thời gian không |
| 12 | Người **ghép được buổi 05 và buổi 07 thành một quy trình**. Không có đáp án duy nhất; nó đo việc thu hẹp khi **không có gì đỏ** |

---

## V2. Bộ câu hỏi

### Câu 1 — 🔥

**Hỏi:** Một pipeline hỏng, không ai biết vì sao. **Bốn lệnh đầu tiên** của bạn là gì, và mỗi lệnh loại bỏ được bao nhiêu giả thuyết?

**Đáp án chuẩn:** Gỡ rối là **thu hẹp**, không phải thử lại. Không gian nghi ngờ có kích thước biết trước: **4** đường dữ liệu vào job (git · `cache` · `artifacts` · biến — buổi 01 QT 5.1) nhân **8** pha (buổi 01 QT 4.2) = **32** ô. Mỗi lệnh phải xoá một **hàng** hoặc một **cột**, không xoá từng ô.

| # | Lệnh | Xoá được gì |
|---|---|---|
| 1 | `curl … /pipelines/$PIPE/jobs \| jq -r '.[] \| .name+" "+.status+" "+(.failure_reason//"-")'` | Chia theo **4** nhóm quy trách nhiệm: lỗi `script`, hạ tầng runner, hết hạn giờ, mất artifact (QT 4.3) |
| 2 | `curl … /jobs/$ID/trace > lan-do.txt` | Đưa log thành **văn bản thuần** — `grep`, `wc`, `diff` được; giao diện web không cho cả ba (QT 4.2) |
| 3 | `go-roi.sh $ID` — bảng pha · dòng bắt đầu · giây | Định vị **1** pha hỏng, loại **7/8** nhóm nguyên nhân trước khi đọc dòng lỗi nào (QT 4.1) |
| 4 | Lấy `trace` lần **xanh** gần nhất rồi `diff lan-xanh.txt lan-do.txt` | Chỉ ra **dòng đầu tiên** khác nhau giữa hai lần chạy |

Bốn lệnh tốn khoảng **2 giây** một lượt gọi API, thay cho 10–20 phút đọc **400** dòng bằng mắt. Ca đặc biệt: job `pending` **không có `trace`** — nhảy sang `jq '.runner'` (QT 6.2).

**Tiêu chí chấm:**
- 0đ: "Chạy lại xem sao", hoặc "đọc log tìm chữ ERROR".
- 1đ: Đọc log từ dưới lên, không có lệnh nào và không có khung phân loại.
- 2đ: Đọc `failure_reason` trước rồi định vị pha; kể được ba trong bốn lệnh.
- 3đ: Đủ bốn lệnh, **và** nói ra **4 × 8 = 32** ô cùng con số loại bỏ **7/8**, **và** nêu ca `pending` không có `trace`.

**Câu hỏi đào sâu:** Bảng 32 ô **không** giải được lớp sự cố nào? *(Lớp ngoài phạm vi một job: hạ tầng GitLab, quota, hàng đợi runner ở quy mô. Đây là khung thu hẹp, không phải danh sách đầy đủ — buổi 13 và 47.)*

---

### Câu 2 — 🔥

**Hỏi:** `retry` sửa được nhóm lỗi nào? Bạn dùng **phép thử** nào để biết ca đang gặp thuộc nhóm đó?

**Đáp án chuẩn:** `retry` chỉ có giá trị với **lỗi chập chờn**. Cùng một đầu vào, cùng image, cùng `script` thì cho cùng một kết quả — nên `retry` chỉ đổi được thứ **không** giống nhau giữa hai lần chạy: mạng, tài nguyên máy, thời điểm. Với lỗi **xác định** — mã sai, biến rỗng, artifact rỗng, `needs` trỏ job vắng mặt — nó không thêm một phần trăm cơ hội nào (QT 5.1).

**Phép thử, một câu:** chạy lại **hai** lần. Hai kết quả **khác** nhau thì là chập chờn, đặt `retry` được. Giống nhau — cùng trạng thái, cùng dòng lỗi — thì đừng đặt, đi tìm nguyên nhân.

Nói thêm để đạt 3 điểm: đây là chỗ dễ tự lừa nhất, vì `retry` **có** làm biểu đồ "pipeline xanh" đẹp hơn, theo hai cách khác nhau — một cách thật (lỗi chập chờn được vượt qua) và một cách giả (sự cố hạ tầng **lặp lại** bị nuốt, hoá đơn phút runner tăng mà không ai biết, QT 5.3). Không đo tỉ lệ job phải chạy lại thì không phân biệt được hai cách đó.

**Tiêu chí chấm:**
- 0đ: "Đặt `retry: 2` cho chắc, pipeline ổn định hơn." **Trần điểm cả buổi là 1.**
- 1đ: Biết `retry` để chạy lại, không phân biệt được hai nhóm lỗi.
- 2đ: Nêu đúng "chỉ chập chờn" **và** phép thử chạy lại hai lần rồi so kết quả.
- 3đ: Như trên, **và** giải thích bằng cơ chế "cùng đầu vào cho cùng kết quả", **và** nhắc `retry` là cơ chế che nên phải đo tỉ lệ chạy lại.

**Câu hỏi đào sâu:** Biến `protected` rỗng làm job xanh mà không deploy gì (buổi 06 QT 5.2). `retry: 2` sửa được không? *(Không — hoàn toàn xác định: cùng nhánh, nền tảng vẫn không gửi biến đó, ba lần chạy cho ba kết quả giống nhau. Cách sửa là `: "${VAR:?}"`.)*

---

### Câu 3 — ★★★

**Hỏi:** Trong `.gitlab-ci.yml` có dòng `retry: 2` trần trụi, không có `when`. Sai ở đâu?

**Đáp án chuẩn:** Nó chạy lại **mọi** loại thất bại như nhau, kể cả `script_failure` — tức chạy lại đúng nhóm mà việc chạy lại vô nghĩa. Cách duy nhất để `retry` không che mất lỗi thật là gắn nó với **`failure_reason` cụ thể** bằng `retry:when`, để nền tảng phân loại thay ta bằng đúng trường ở QT 4.3 (QT 5.2).

```yaml
retry:
  max: 2                                                   # max tối đa 2 ở GitLab 17.7
  when: [runner_system_failure, stuck_or_timeout_failure]  # script_failure KHÔNG được chạy lại
```

Danh sách `when` có khoảng **12** giá trị; chỉ nhóm **hạ tầng** nên có mặt.

Cái làm câu này thành câu **đánh giá**: hậu quả là **im lặng, không chặn**. Trạng thái cuối của job vẫn xanh, các lần thất bại trung gian nằm trong dữ liệu API mà không nằm trên bảng điều khiển nào. Dấu hiệu ở mức đội: biểu đồ tỉ lệ job phải chạy lại phẳng ở mức cao nhiều tuần mà không ai mở vé hạ tầng; hoặc hoá đơn phút runner tăng 30% trong một tháng mà số pipeline không đổi. Ràng buộc kèm theo: dùng `retry` thì **bắt buộc** đo tỉ lệ chạy lại — `dem-retry.sh` đếm job có nhiều hơn một lần chạy trong 100 pipeline gần nhất; theo kinh nghiệm thực tế vượt **2%** là đáng mở vé, và ngưỡng đó khác nhau giữa đội 500 pipeline/ngày và đội 20 pipeline/ngày (QT 5.3).

**Tiêu chí chấm:**
- 0đ: "Không sai gì, `retry` giúp pipeline ổn định." **Trần điểm cả buổi là 1.**
- 1đ: Biết nên giới hạn lại, không nói được giới hạn bằng gì.
- 2đ: Nêu đúng `retry:when` gắn với `failure_reason`, viết được danh sách chỉ chứa nhóm hạ tầng.
- 3đ: Như trên, **và** gọi đúng ô *im lặng, không chặn*, **và** nêu ràng buộc phải đo tỉ lệ chạy lại kèm ngưỡng **2%** cùng giới hạn của ngưỡng đó.

**Câu hỏi đào sâu:** Đặt `when` đúng thì tốn thêm bao nhiêu giây? *(**0 giây** khi mọi thứ đúng — chỉ tốn khi hạ tầng thật sự hỏng. Đó là lý do `retry:when` là một trong những dòng rẻ nhất của khoá, còn `retry` trần trụi thì không.)*

---

### Câu 4 — ★★★

**Hỏi:** Một job chạy **90 giây** rồi `exit 1` vì lỗi cú pháp trong `script`. Bạn đặt `retry: 2`. Tổng thời gian bao nhiêu, và được thêm mấy phần trăm cơ hội thành công?

**Đáp án chuẩn:** **270 giây** và **0%**.

Phép tính phải nói ra: `retry: 2` nghĩa là **`retry` + 1 = 3** lần chạy. 3 × 90 = **270 giây**, tức **+180 giây** phút runner mỗi lần hỏng. Cơ hội thêm là **0%** vì lỗi cú pháp hoàn toàn xác định — lần thứ ba hỏng đúng chỗ lần thứ nhất hỏng, với đúng cùng một dòng lỗi. Cái thật sự mua bằng 180 giây đó là **chờ 4,5 phút thay vì 1,5 phút để nhận cùng một tin**.

Cách đo, không tra: job `exit 1` với `retry: 2` phải đỏ **ba** lần; cộng `duration` của cả ba lần chạy qua API.

Định lượng ngược lại, để thấy `retry` không phải luôn vô ích: nếu cùng job đó hỏng vì lỗi **chập chờn** với tỉ lệ hỏng 10% mỗi lần, `retry: 2` đưa tỉ lệ hỏng của job từ **10%** xuống **0,1%**, và chi phí kỳ vọng chỉ khoảng 90 × 0,11 ≈ **10 giây** mỗi lần chạy — vì hai lần chạy thêm chỉ xảy ra khi lần trước đã hỏng. Cùng một dòng cấu hình, một ca vô ích và một ca gần như miễn phí; thứ quyết định là **loại lỗi**, không phải con số `max`.

**Tiêu chí chấm:**
- 0đ: "Vẫn 90 giây", hoặc "tuỳ trường hợp" không kèm phép tính.
- 1đ: Biết là tốn thêm, không tính ra con số.
- 2đ: Tính đúng **270 giây** và nói đúng **0%**.
- 3đ: Như trên, **và** nêu **+180 giây** cùng câu "chờ 4,5 phút để nhận cùng một tin", **và** tính được ca chập chờn đối chứng để chỉ ra thứ quyết định là loại lỗi.

**Câu hỏi đào sâu:** `retry: 5` có được không? *(Không — `max` tối đa **2** ở GitLab 17.7, tức tối đa 3 lần chạy. Đó là giới hạn của **phiên bản**, không phải một quy luật; đừng viết số 2 vào tài liệu như hằng số.)*

---

### Câu 5 — ★★★

**Hỏi:** Job A đứng 20 phút không có log. Job B đứng 20 phút rồi bị cắt. Hai ca khác nhau thế nào, và bạn kiểm bằng **trường nào**?

**Đáp án chuẩn:** Hai trạng thái khác nhau tuy trông giống nhau. `pending` nghĩa là **chưa runner nào nhận** — nguyên nhân hay gặp nhất là `tags` không khớp runner nào (buổi 02 QT 6.3). Hết hạn giờ nghĩa là **đã nhận rồi mà không tiến triển** — treo ở `docker pull`, treo ở một lệnh chờ mạng, treo trong `script`. Hai trạng thái ở hai phía khác nhau của pha 1, hai cách sửa loại trừ nhau (QT 6.2).

**Trường phân biệt là `runner`** — đúng **1** trường, một lệnh:

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/projects/$PID/jobs/$ID" \
| jq '{status, runner: (.runner.id // null), queued_duration, duration}'
```

`runner` là `null` → chưa ai nhận, và `duration` cũng **null** vì đồng hồ chạy job chưa bắt đầu; thời gian đứng nằm ở `queued_duration`. Có id → đã nhận, đọc `duration` rồi đi tìm pha đang treo bằng bốn lệnh của câu 1.

Hệ quả phải nói ra: **thêm runner** sửa ca thứ nhất, vô ích với ca thứ hai; **tăng `timeout`** sửa ca thứ hai, vô ích với ca thứ nhất. Ca `pending` là ô **im lặng nhưng có chặn** — pipeline đứng nên sớm muộn có người thắc mắc; cái **im lặng** thật sự nằm ở bước dọn dẹp bị mất (câu 7).

**Tiêu chí chấm:**
- 0đ: "Hai ca giống nhau, chạy lại là được." **Trần điểm cả buổi là 1.**
- 1đ: Biết một ca do runner, không nêu được cách phân biệt.
- 2đ: Nêu đúng "chưa nhận" so với "đã nhận mà không tiến triển" **và** chỉ ra trường `runner`.
- 3đ: Như trên, **và** nêu `duration` = null cùng `queued_duration` cho ca `pending`, **và** nói rõ hai cách sửa loại trừ nhau.

**Câu hỏi đào sâu:** Vì sao ca `pending` không có gì để đọc trong `trace`? *(Vì `trace` chỉ tồn tại **sau khi** runner nhận job — không có runner thì không ai ghi log. Đây là ca duy nhất trong buổi mà lệnh thứ hai và thứ ba của câu 1 phải bỏ qua.)*

---

### Câu 6 — ★★★

**Hỏi:** Job khai `timeout: 3h` mà bị cắt ở phút thứ **60**. Trong `.gitlab-ci.yml` không có gì giải thích được. Vì sao?

**Đáp án chuẩn:** Hạn giờ của một job đến từ **ba** nguồn, giá trị **nhỏ nhất thắng** (QT 6.1):

| # | Nguồn | Ở đâu |
|---|---|---|
| 1 | Cấu hình project | Settings → CI/CD, **ngoài repo**; mặc định **60 phút** |
| 2 | Khoá `timeout` của job | `.gitlab-ci.yml`, trong repo |
| 3 | Hạn giờ khai trong `config.toml` của runner | Máy runner, **ngoài repo** — nguồn khó tìm nhất |

Vì sao là min: hạn giờ là hợp đồng giữa hai bên, bên nào cũng có quyền đặt giới hạn thấp hơn cho phần tài nguyên của mình. Con số 60 phút ở ca này gần như chắc chắn là cấu hình project mặc định, hoặc hạn giờ trong `config.toml` — cả hai nằm **ngoài repo**, đúng ranh giới hai tệp của buổi 02 QT 4.1. Đọc nguồn thứ ba bằng `GET /runners/:id`, đối chiếu với `timeout` của job và cấu hình project; ba con số, lấy min.

Điểm phải nêu để đạt 3 điểm: `timeout: 3h` trong YAML **không** phải hạn giờ thật, nó là một trong **ba** đề xuất. Chiều ngược lại cũng đúng — siết `timeout` xuống thấp "cho gọn" làm job build lớn nhất hỏng đúng ngày phát hành; cách đặt an toàn là đo `duration` **lớn nhất trong 30 ngày** rồi cộng **50%** biên.

**Tiêu chí chấm:**
- 0đ: "Chắc GitLab bỏ qua `timeout`."
- 1đ: Biết có cấu hình khác đè, không kể được nguồn nào.
- 2đ: Kể đủ **3** nguồn và nói đúng luật **min**.
- 3đ: Như trên, **và** chỉ ra hai trong ba nguồn nằm **ngoài repo** cùng cách đọc bằng `GET /runners/:id`, **và** nêu cách đặt `timeout` bằng max 30 ngày cộng 50% biên.

**Câu hỏi đào sâu:** Job hết hạn giờ thì `failure_reason` bằng gì, ai xử lý? *(`stuck_or_timeout_failure` — một trong bốn nhóm quy trách nhiệm của QT 4.3, và là nhóm cần cả hai bên: người viết pipeline xem job có thật cần lâu thế không, người vận hành runner xem `config.toml` cắt ở đâu.)*

---

### Câu 7 — ★★

**Hỏi:** `script` của một job chạy quá hạn giờ và bị cắt. `after_script` có chạy không?

**Đáp án chuẩn:** **Có** — `after_script` có hạn giờ **riêng** và ngắn, tách khỏi hạn giờ của `script`, nên job bị cắt ở `script` vẫn còn cơ hội chạy bước dọn dẹp (QT 6.3, tiếp nối buổi 01 QT 4.3 — lần thứ **2** nguyên lý "`after_script` là shell riêng" xuất hiện). Nền tảng cố ý làm vậy để bước dọn dẹp không bị cắt cùng lúc với `script`.

Nhưng "riêng" cũng có nghĩa "có thể hết trước khi dọn xong". Ca ngược lại là ca **im lặng**: job hết hạn giờ **trong** `after_script` thì mất bước dọn dẹp — container, tệp tạm, lock còn sót — và trong log **không có dòng nào** nói `after_script` đã bị cắt. Ô của bảng hai thuộc tính: *im lặng, không chặn*.

Con số và cách đo: giá trị tham chiếu của hạn giờ `after_script` ở Runner 17.7 là **5 phút**, và đây là đại lượng **phải đo, không được tra** — nó đổi được trong `config.toml` và đã đổi giữa các phiên bản. Phép đo hai chiều: (1) `script` ngủ quá hạn, `after_script` in một dòng mốc — xem dòng đó có trong `trace` không; (2) `after_script` ngủ lâu hơn hạn giờ riêng của nó — xem dòng cuối có mất không.

**Tiêu chí chấm:**
- 0đ: "Không, job bị cắt là mất hết."
- 1đ: Đáp "có" mà không biết vì sao.
- 2đ: Nêu đúng cơ chế **hạn giờ riêng** và ca ngược lại làm mất bước dọn dẹp.
- 3đ: Như trên, **và** đưa con số tham chiếu **5 phút** kèm khẳng định nó **phải đo lại**, **và** gọi đúng ô *im lặng, không chặn* vì log không ghi gì.

**Câu hỏi đào sâu:** Vậy đặt bước dọn dẹp quan trọng vào `after_script` có an toàn không? *(Không đủ, nếu bước đó chạy lâu — nó có hạn giờ riêng và ngắn. Việc dọn dẹp phải rẻ và chịu được chạy nửa vời; trạng thái dùng chung thật sự thì bảo vệ bằng `resource_group`.)*

---

### Câu 8 — ★★★

**Hỏi:** Bạn bật `interruptible: true` cho **9 trong 10** job. Phút runner không giảm chút nào. Vì sao?

**Đáp án chuẩn:** Vì giá trị của `interruptible` là **nhị phân theo cả pipeline**, không cộng dồn theo từng job. Nền tảng chỉ huỷ một pipeline lỗi thời khi chắc rằng **mọi** việc còn dở đều huỷ được an toàn; job không đánh dấu bị coi là không huỷ được, nên **một** job như thế đang chạy là đủ để phần còn lại **không** bị huỷ (QT 7.1).

Con số cho ca cụ thể — push **3** commit trong 2 phút, pipeline **6** job, mỗi job **90 giây**: mọi job đều `interruptible` thì hai pipeline cũ bị huỷ, tiết kiệm khoảng **2 × 6 × 90 = 1.080 giây**. Còn đúng một job không đánh dấu thì tiết kiệm **0 giây**. Đổi bất kỳ số nào trong ba số 3 · 6 · 90 thì kết quả đổi theo. Cách đo: push ba commit liên tiếp rồi đếm job `canceled` của hai pipeline cũ.

Điều kiện hay bị bỏ: `interruptible` cần bật thêm **huỷ pipeline dư** trong cấu hình project; khai trong YAML một mình thì không đủ.

Phần đắt nhất: job còn lại **nên** là job deploy, và nó **phải** không đánh dấu — deploy bị huỷ giữa đường để lại trạng thái nửa vời. Nghĩa là trên pipeline có deploy, QT 7.1 hầu như không cho ta tiết kiệm gì, và **đó là cái giá đúng phải trả**.

**Tiêu chí chấm:**
- 0đ: "Chắc tính năng đó không hoạt động."
- 1đ: Biết còn job chưa đánh dấu, không giải thích được vì sao một job là đủ.
- 2đ: Nêu đúng giá trị **nhị phân theo pipeline** và cơ chế "job không đánh dấu bị coi là không huỷ được".
- 3đ: Như trên, **và** tính được **1.080 giây** so với **0 giây** kèm giới hạn của con số, **và** nêu job deploy phải **không** đánh dấu cùng hệ quả.

**Câu hỏi đào sâu:** Bật `interruptible: true` ở đâu cho gọn? *(Ở `default:` một lần, rồi ghi đè `interruptible: false` cho đúng job deploy. Cách này làm cấu hình đúng theo mặc định và bắt người thêm job mới phải cố ý chọn ngoại lệ.)*

---

### Câu 9 — ★★★

**Hỏi:** Staging đang chạy phiên bản của một commit **cũ hơn** commit đã deploy xong sau đó. Không job nào đỏ. Nguyên nhân và **một dòng** sửa?

**Đáp án chuẩn:** Hai pipeline deploy chạy **chồng thời gian**, và bản thắng là bản **kết thúc sau** — không phải bản mới hơn. Kết quả không xác định và **im lặng**: hai job đều xanh, giao diện không có gì bất thường. Đây là ô nguy hiểm nhất của buổi: *im lặng, không chặn* (QT 7.2).

Bằng chứng, trước khi kết luận: đọc `started_at` và `finished_at` của hai job deploy gần nhất, xem hai khoảng có giao nhau không; và đọc `GET /projects/:id/resource_groups/:key/upcoming_jobs` xem có hàng đợi nào đang tồn tại.

```yaml
trien-khai-staging:
  resource_group: staging      # mọi job deploy vào cùng môi trường phải cùng một tên nhóm
```

`resource_group` là **cơ chế loại trừ lẫn nhau duy nhất** của GitLab CI. Không có gì khác trong `.gitlab-ci.yml` biểu đạt được "hai job này không được chạy cùng lúc": `stage` chỉ nói thứ tự **trong** một pipeline (buổi 03 QT 5.1). **1** dòng biến **2** pipeline song song thành **1** hàng đợi.

Cái giá và giới hạn: hai lần deploy song song 30 phút thành 60 phút chờ — đo `duration` của job deploy trước khi thêm. Và **đừng** đặt `resource_group` cho job test hay build "cho chắc": nó biến chạy song song thành hàng đợi và làm đường găng dài ra, đúng thứ buổi 14 phải đi rút ngắn.

**Tiêu chí chấm:**
- 0đ: "Deploy hỏng, chạy lại." Không nhận ra đây là ca hai pipeline chồng nhau.
- 1đ: Đoán có hai lần deploy đè nhau, không nêu được cơ chế chặn.
- 2đ: Nêu đúng "bản kết thúc sau thắng" và đề xuất `resource_group` cùng tên.
- 3đ: Như trên, **và** nêu bằng chứng bằng `started_at`/`finished_at` chồng nhau, **và** nêu cái giá cùng ca **không** nên dùng `resource_group`.

**Câu hỏi đào sâu:** `needs` hay `stage` chặn được ca này không? *(Không — cả hai chỉ điều khiển thứ tự **bên trong** một pipeline. Hai pipeline là hai đối tượng riêng, không có khoá thứ tự nào giữa chúng ngoài `resource_group`.)*

---

### Câu 10 — ★★

**Hỏi:** `failure_reason` của một job dùng để làm gì? Nó chia sự cố thành mấy nhóm?

**Đáp án chuẩn:** Nó phân loại nguyên nhân theo **nền tảng**, trước khi ta phán xét theo mã nguồn — nên nó là **bước 0** của mọi cuộc gỡ rối, đứng trước cả việc mở log (QT 4.3). **4** nhóm quy trách nhiệm: lỗi `script`, lỗi hạ tầng runner, hết hạn giờ, mất artifact. Bốn nhóm cần **bốn người khác nhau** xử lý.

Vì sao trường này quan trọng: cùng một trạng thái `failed` trên giao diện có thể là lỗi của lập trình viên hoặc của đội hạ tầng, và `failure_reason` là trường **duy nhất** phân biệt được hai thứ đó **mà không cần đọc log**. Dấu hiệu khi bỏ qua: một vé bị chuyển qua lại giữa hai đội suốt hai ngày, trong khi trường này đã ghi `runner_system_failure` ngay từ đầu.

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs" \
| jq -r '.[] | .name + "  " + .status + "  " + (.failure_reason // "-")'
```

Công dụng thứ hai, ít người biết: đây chính là tập giá trị mà `retry:when` nhận (QT 5.2). Đọc `failure_reason` không chỉ để quy trách nhiệm — nó còn là dữ liệu để quyết định job nào **đáng** chạy lại tự động.

**Tiêu chí chấm:**
- 0đ: Không biết có trường này; đọc log ngay từ đầu.
- 1đ: Biết nó ghi lý do hỏng, không nêu được nó dùng để làm gì.
- 2đ: Nêu đúng **4** nhóm quy trách nhiệm và một lệnh `jq` cho cả pipeline.
- 3đ: Như trên, **và** nói rõ nó phân biệt lỗi lập trình với lỗi hạ tầng **không cần đọc log**, **và** nối được với `retry:when`.

**Câu hỏi đào sâu:** Job **xanh** thì `failure_reason` bằng gì, và điều đó nói lên hạn chế nào? *(Rỗng — nên trường này vô dụng với lớp "job xanh mà sai", tức đúng ô nguy hiểm nhất. Với lớp đó phải đi bằng kích thước artifact và `duration` so với lần trước, xem câu 12.)*

---

### Câu 11 — ★★★

**Hỏi:** Vì sao trong một báo cáo gỡ rối, bằng chứng phải là **một lệnh** chứ không phải một câu mô tả?

**Đáp án chuẩn:** Vì lệnh là thứ duy nhất người khác **kiểm lại được** sau ba tháng, khi cả pipeline đã đổi. Một câu mô tả — "artifact có vẻ rỗng", "runner chắc bị nghẽn" — không kiểm lại được, nên nó không phân biệt được kết luận đúng với phỏng đoán hợp lý mà sai (QT 7.3).

Mẫu bắt buộc có **4** dòng: **triệu chứng** → **bằng chứng (một lệnh in ra được)** → **nguyên nhân** → **cách sửa**. Thiếu dòng thứ hai thì kết luận là phỏng đoán, và nó sẽ được lặp lại bởi người sau. Dòng bằng chứng cho ca artifact rỗng — hai lệnh `curl`, một in `success`, một in `404`:

```bash
$ curl -so /dev/null -w '%{http_code}\n' … /jobs/311/artifacts   # 404 — job xanh mà không có artifact
$ curl -sf … /jobs/311 | jq '.artifacts_file.size'               # null
```

Dấu hiệu khi kỷ luật này thiếu: cùng một sự cố xuất hiện **lần thứ ba** trong sáu tháng và mỗi lần lại được điều tra từ đầu. Đó là chi phí thật, tính bằng người-giờ, của việc bỏ một dòng.

Điểm phải nêu để đạt 3 điểm: kỷ luật này chỉ tồn tại khi được **máy cưỡng chế**. Trong lab, checkpoint kiểm dòng bằng chứng bằng `grep -c '^\$ '` trên `bao-cao-go-roi.md` — đếm dòng bắt đầu bằng dấu nhắc lệnh — chứ không đọc câu văn. Sáu báo cáo bốn dòng là hiện vật nộp của buổi.

**Tiêu chí chấm:**
- 0đ: "Viết mô tả là đủ, ai đọc cũng hiểu."
- 1đ: Đồng ý nên có lệnh, không nêu được vì sao.
- 2đ: Nêu đúng lập luận **kiểm lại được** và kể đủ **4** dòng của mẫu.
- 3đ: Như trên, **và** viết được một dòng bằng chứng dạng lệnh in ra hai giá trị đối lập, **và** nêu việc cưỡng chế bằng `grep` thay cho việc đọc câu văn.

**Câu hỏi đào sâu:** Dòng nào trong bốn dòng hay bị viết sai nhất? *(Dòng **triệu chứng** — người ta viết ngay nguyên nhân mình nghi vào đó, ví dụ "cache hỏng" thay vì "job `dong-goi` đỏ, không tìm thấy tệp `dist/app.js`". Viết triệu chứng đúng là điều kiện để bảng 32 ô dùng được.)*

---

### Câu 12 — 🔥

**Hỏi:** Job deploy **xanh**, không có gì đỏ trong cả pipeline, nhưng nội dung được triển khai là bản **cũ**. Dựng quy trình truy nguyên, và viết ra bốn dòng.

**Đáp án chuẩn:** Không có đáp án duy nhất; câu này đo việc thu hẹp khi **không có gì đỏ**. Ba lệnh đầu của câu 1 mất phần lớn giá trị: `failure_reason` rỗng vì job xanh, và log không có dòng lỗi nào để định vị pha. Phải đổi câu hỏi.

**Nhịp 1 — đổi trục.** Job xanh chỉ chứng minh mã thoát bằng 0. Với ô *im lặng, không chặn*, hai con số bắt được phần lớn ca: **kích thước artifact** và **`duration`**, so với lần chạy trước. Bản cũ được triển khai nghĩa là dữ liệu vào job đã cũ — nghi phạm nằm ở **hàng** `cache` hoặc **hàng** `artifacts`, ở **cột** pha 4–5 của bảng 32 ô (QT 4.1).

**Nhịp 2 — loại giữa hai hàng.** Lấy `trace` bằng `curl` rồi `grep` các dòng phục hồi `cache` và tải `artifacts` (QT 4.2). Nghi phạm số một: **cùng một đường dẫn ở cả `cache` và `artifacts`** — buổi 05 QT 7.2 đã đo: artifact tải về **trước**, rồi cache phục hồi lên **đè** lại bằng bản cũ. Không có dòng lỗi nào, vì đây không phải lỗi.

**Nhịp 3 — bằng chứng bằng lệnh.** Tải artifact của job nguồn về, `unzip -l` xem đúng tệp và đúng dấu thời gian; so với tệp mà job deploy thật sự đọc.

**Bốn dòng (QT 7.3):**

| Dòng | Nội dung |
|---|---|
| Triệu chứng | Job `trien-khai` xanh, `dist/app.js` trên đích là bản của commit trước, không job nào đỏ |
| Bằng chứng | `$ unzip -l artifacts.zip \| grep app.js` cho dấu thời gian mới; `$ grep -n 'Restoring cache' lan-do.txt` cho dòng cache phục hồi **sau** dòng tải artifact, cùng đường dẫn `dist/` |
| Nguyên nhân | `dist/` khai ở cả `cache:paths` và `artifacts:paths`; cache phục hồi sau nên đè bản mới bằng bản cũ (buổi 05 QT 7.2) |
| Cách sửa | Bỏ `dist/` khỏi `cache:paths` — cái job sau **cần** thì đi bằng `artifacts`; thêm một khẳng định so dấu thời gian để ca này thành job đỏ lần sau |

**Tiêu chí chấm:**
- 0đ: "Job xanh thì không có vấn đề gì", hoặc "chạy lại xem sao".
- 1đ: Nghi ngờ cache, không nêu được lệnh nào và không viết được bốn dòng.
- 2đ: Đổi trục sang kích thước artifact và `duration`, khoanh đúng hàng `cache`/`artifacts` × pha 4–5, viết được bốn dòng.
- 3đ: Đủ ba nhịp, **và** gọi đúng cơ chế "artifact tải trước, cache đè sau" của buổi 05 QT 7.2, **và** dòng bằng chứng là lệnh in ra được, **và** cách sửa kèm một khẳng định biến ca im lặng thành job đỏ.

**Câu hỏi đào sâu:** Nếu `trace` lần này giống hệt `trace` của lần bản mới lên đúng thì đi tiếp thế nào? *(Nghi phạm rời khỏi job, sang phía môi trường đích: hai pipeline deploy chồng nhau, bản kết thúc sau thắng — câu 9. Bằng chứng là `started_at`/`finished_at` giao nhau, cách sửa là `resource_group`.)*

---

## V3. Câu chốt để nói khi phỏng vấn

> Bốn câu dưới đây viết **nguyên văn, đúng ngữ điệu nói**. Học viên tập nói to từng câu tới khi trôi chảy mà không phải nghĩ.
> Mỗi câu chứa **một con số** hoặc **một cơ chế** — đó là thứ phân biệt câu trả lời của người đã đo với câu trả lời của người đã đọc.

**Câu 1 — khi được hỏi "bạn gỡ một pipeline hỏng thế nào":**

> "Tôi không chạy lại. Chạy lại là cách tốn tiền nhất để không học được gì. Việc tôi làm là **thu hẹp**, và không gian nghi ngờ có kích thước biết trước: một job có **bốn** đường dữ liệu vào — git, cache, artifact, biến — và **tám** pha. Bốn nhân tám là **ba mươi hai** ô, và một pipeline hỏng bất kỳ nằm ở đúng một ô. Nên lệnh đầu tiên của tôi không phải đọc lỗi, mà là đọc `failure_reason` qua API để biết đây là lỗi của ai; rồi định vị **pha** hỏng — việc đó mất mười giây và loại bỏ **bảy trong tám** nhóm nguyên nhân trước khi tôi đọc dòng lỗi nào. Mỗi lệnh phải xoá một hàng hoặc một cột. Lệnh nào không xoá được gì thì tôi không chạy."

**Câu 2 — khi được hỏi "bạn nghĩ gì về `retry`":**

> "`retry` là một cơ chế **che**, nên tôi coi nó là thứ phải **đo** mới được dùng. Nó chỉ giúp với lỗi chập chờn. Với lỗi xác định thì nó vô ích và tính được: một job chín mươi giây `exit 1` với `retry: 2` chạy ba lần, tức **hai trăm bảy mươi giây**, và **không phần trăm nào** cơ hội thêm — tôi trả thêm ba phút để chờ đúng cùng một dòng lỗi. Phép thử của tôi rất rẻ: chạy lại **hai** lần, hai kết quả giống nhau thì đừng đặt `retry`. Và khi đặt thì luôn có `when`, giới hạn vào nhóm hạ tầng, cộng một số đo là tỉ lệ job phải chạy lại. Theo kinh nghiệm của tôi vượt **hai phần trăm** là có sự cố hạ tầng thật đang bị `retry` nuốt, và lúc đó tôi mở vé chứ không tăng `max`."

**Câu 3 — khi được hỏi "job khai `timeout: 3h` mà bị cắt sớm, vì sao":**

> "Vì `timeout` trong YAML không phải hạn giờ thật, nó là một trong **ba** nguồn: cấu hình project, khoá `timeout` của job, và hạn giờ khai trong `config.toml` của runner. Giá trị **nhỏ nhất thắng**, vì hạn giờ là hợp đồng giữa hai bên và bên nào cũng có quyền đặt giới hạn thấp hơn. Bị cắt ở phút thứ sáu mươi thì tôi đoán ngay cấu hình project mặc định, hoặc `config.toml`. Cái khó là nguồn thứ ba nằm **ngoài repo**, trên máy runner, nên đọc `.gitlab-ci.yml` cả ngày cũng không thấy — tôi đọc nó bằng `GET /runners/:id`. Đây cũng là lý do tôi không đặt `timeout` bằng cảm giác: tôi lấy `duration` lớn nhất trong ba mươi ngày rồi cộng năm mươi phần trăm biên."

**Câu 4 — khi được hỏi "bạn cải thiện được gì cho pipeline của đội cũ":**

> "Một dòng, và nó chặn được loại sự cố đắt nhất tôi từng gặp. Staging của chúng tôi chạy bản **cũ hơn** bản vừa deploy xong, mà không job nào đỏ. Nguyên nhân là hai pipeline deploy chạy chồng thời gian, và bản thắng là bản **kết thúc sau** — không phải bản mới hơn. Đây là ô im lặng và không chặn, nên nó tồn tại được nhiều tuần. Cái tôi thêm vào là `resource_group: staging` cho job deploy. Đó là **cơ chế loại trừ lẫn nhau duy nhất** của GitLab CI — `stage` chỉ nói thứ tự bên trong một pipeline, nó không nói gì giữa hai pipeline. **Một** dòng biến **hai** pipeline song song thành **một** hàng đợi. Cái giá là deploy phải chờ nhau, nên tôi đo `duration` của job deploy trước khi thêm."

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
| ≥ 80% | Nắm vững. Hết giai đoạn 1 — giao BT mở rộng §L10 về `dem-retry.sh`, làm trước buổi 08 |
| 60–79% | Đạt. Đọc lại quy tắc bị mất điểm trước buổi 08 |
| 40–59% | Chưa đạt. Làm lại bước lab 2 và 3 (sáu ca hỏng) ở nhà, nộp lại `bao-cao-go-roi.md` |
| < 40% | Chưa đạt. Học lại cả buổi — bảng 32 ô còn quay lại ở buổi 13, 14, 22, 47, 48 |

**Bảng lỗi làm trần điểm là 1:**

| Lỗi | Vì sao nghiêm trọng đến mức trần điểm |
|---|---|
| "`retry` giúp được với lỗi xác định", hoặc đề xuất `retry` mà không nhắc `when` | Job 90 giây thành **270 giây** với **0%** cơ hội thêm; `retry` trần trụi còn nuốt sự cố hạ tầng lặp lại — im lặng, không chặn, hiện ra ở hoá đơn phút runner chứ không ở bảng điều khiển nào |
| "Job `pending` và job hết hạn giờ là cùng một loại sự cố" | Hai phía khác nhau của pha 1, phân biệt bằng đúng **1** trường `runner`. Người tin chúng giống nhau sẽ thêm runner để sửa job treo ở `docker pull`, hoặc tăng `timeout` cho job chưa ai nhận |
| Kết luận nguyên nhân mà không có lệnh chứng minh | Mẫu **4** dòng có dòng thứ hai là **một lệnh**. Không có lệnh thì đó là phỏng đoán, và cùng sự cố sẽ được điều tra lại từ đầu lần thứ ba |

---

## V5. Bài tập về nhà

### BTVN 1. Bốn lệnh trên job đỏ gần nhất của repo thật

Lấy một repo đang chạy (của mình hoặc của đội), tìm **job đỏ gần nhất**, chạy đủ bốn lệnh của câu 1. Việc này không đụng repo, làm được ngay hôm nay.

**Nộp:** bảng ba cột *pha · dòng bắt đầu · số giây* do `go-roi.sh` in ra, cộng giá trị `failure_reason`, cộng **một** câu: pha nào hỏng và điều đó loại bỏ nhóm nguyên nhân nào. Con số phải ghi lại: **thời gian từ lệnh đầu tiên tới lúc có kết luận** — số "đo trước" của §8, mục tiêu dưới **10 phút**.

### BTVN 2. Quét `retry` và đo tỉ lệ chạy lại

1. `grep -n 'retry' .gitlab-ci.yml` — mọi `retry` **không** có `when` là một chỗ đang che lỗi. Đếm số chỗ đó.
2. Chạy `dem-retry.sh` cho **100** pipeline gần nhất, ghi tỉ lệ job phải chạy lại.

**Nộp:** hai con số; và với **một** chỗ tìm được ở việc 1, viết lại thành `retry: {max: 2, when: [...]}` với danh sách chỉ chứa nhóm hạ tầng — đúng tên job thật, không viết `job-a` cho có. Nếu tỉ lệ vượt **2%**, thêm một câu: bằng chứng bạn đính vào vé hạ tầng là lệnh nào?

### BTVN 3. Ba ca của buổi tái hiện trên repo của mình

Trên một **nhánh riêng**, tái hiện **ba** ca, mỗi ca một job, ghi bằng chứng bằng số chứ không bằng ảnh chụp:

1. **`retry` vô ích** — job `exit 1` với `retry: 2`; cộng `duration` cả ba lần chạy qua API, ghi tổng và so với một lần.
2. **Ba nguồn hạn giờ** — đọc `timeout` của job, cấu hình project, và `GET /runners/:id`; ghi ba con số và cái nào là min.
3. **`after_script` bị cắt** — `script` ngủ quá hạn giờ, `after_script` in một dòng mốc; ghi dòng đó có trong `trace` không, rồi làm ca ngược lại.

**Nộp:** thêm ba mục vào `bao-cao-go-roi.md`, mỗi mục đúng bốn dòng: *triệu chứng · bằng chứng (một lệnh) · nguyên nhân · cách sửa*. Tự kiểm bằng `grep -c '^\$ '` — số dòng bắt đầu bằng dấu nhắc lệnh phải ít nhất bằng số mục.

### BTVN 4. Chuẩn bị cho buổi 08

Trả lời ba câu sau bằng viết, mỗi câu 3–5 dòng. Mang theo vào buổi 08.

1. Lấy `go-roi.sh` chạy cho **toàn bộ** một pipeline của bạn và ghi `duration` từng job. Cộng theo `stage` để có tổng thời gian pipeline hiện tại, rồi tìm **đường dài nhất theo dữ liệu** — chuỗi job mà job sau thật sự cần artifact của job trước. Đường đó **ngắn hơn tổng bao nhiêu giây**?
2. Với bản đồ phụ thuộc `ban-do-phu-thuoc.md` đã lập ở buổi 03, viết ra **những cặp job không cần chờ nhau**. Đếm số cặp đó.
3. Nếu một job test được chia thành **5** phần chạy song song, cái gì phải thay đổi ở phần thu artifact và phần báo cáo? Ghi phỏng đoán, kể cả khi bạn chưa biết cú pháp.

**Ba câu này dẫn vào đâu:** câu 1 dẫn vào **§4 buổi 08 — đường găng thay cho tổng các stage**; hiệu số giây bạn tính ra chính là phần thời gian đang bị `stage` bắt chờ vô cớ, và nó là số "đo trước" của cả buổi 08. Câu 2 dẫn vào **§5 buổi 08 — chuyển bản đồ phụ thuộc thành các dòng `needs:`**; mỗi cặp không cần chờ nhau sẽ thành một dòng cấu hình cụ thể, không phải một ý tưởng. Câu 3 dẫn vào **§6 buổi 08 — `parallel` và `matrix`**: chia một job thành 5 phần là việc dễ, việc khó là thu **5** bộ artifact về một báo cáo mà không job nào ghi đè job nào — và ca ghi đè đó chính là ô *im lặng, không chặn* mà bảng 32 ô của hôm nay dùng để bắt.
{% endraw %}
