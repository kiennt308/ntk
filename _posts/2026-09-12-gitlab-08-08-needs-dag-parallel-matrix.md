---
layout: post
title: "[Bài 08] Tối Ưu Pipeline Phi Tuyến Tính Với Directed Acyclic Graph (DAG): needs, parallel & Matrix Builds"
date: 2026-09-12 08:20:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-08
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 8
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.08] Hướng dẫn chuyên sâu Tối Ưu Pipeline Phi Tuyến Tính Với Directed Acyclic Graph (DAG): needs, parallel & Matrix Builds: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Tối Ưu Pipeline Phi Tuyến Tính Với Directed Acyclic Graph (DAG): needs, parallel & Matrix Builds."
  - "Thiết kế CI/CD Pipeline chuẩn Enterprise với kiến trúc DAG, tối ưu hóa thời gian build và caching hiệu quả."
  - "Bảo mật chuỗi cung ứng phần mềm với SAST/DAST, Container Scanning và OIDC Authentication."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 08] TỐI ƯU PIPELINE PHI TUYẾN TÍNH VỚI DIRECTED ACYCLIC GRAPH (DAG): NEEDS, PARALLEL & MATRIX BUILDS

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · executor `docker` · `concurrent = 8`.
> Mọi đoạn YAML dán được vào `.gitlab-ci.yml`; đoạn nào là mảnh thì có ghi chú `# mảnh — dán vào <chỗ>`.
> Lệnh `curl` dùng bốn biến đã có từ buổi 01: `$GITLAB`, `$GITLAB_TOKEN`, `$PID`, `$PIPE`.
> Buổi này mở **giai đoạn 2 — kiến trúc pipeline**. Từ đây trở đi, mỗi buổi sửa một thứ mà giai đoạn 1 chỉ đo và ghi nhận.

---





Gọi ngẫu nhiên, mỗi câu 1 phút. Năm câu này là năm mảnh nền hôm nay dựng trực tiếp lên: ai sai câu 1 sẽ không đo được đường găng ở lab bước 1, ai sai câu 5 sẽ tắc ở §7.

| # | Câu hỏi | Đáp án vắn tắt | Dẫn vào đâu hôm nay |
|---|---|---|---|
| 1 | Bốn lệnh đầu tiên khi gỡ một pipeline hỏng, theo thứ tự | `failure_reason` → đọc `trace` theo pha → kiểm `runner` → `diff` với lần xanh. **4** đường vào job × **8** pha = **32** ô để thu hẹp (buổi 07 QT 4.1–4.3) | Lab bước 1 — cùng bộ lệnh, nhưng đọc `duration` thay vì đọc lỗi |
| 2 | `retry` sửa được nhóm lỗi nào | Chỉ **lỗi chập chờn**. Job 90 s với `retry: 2` cho ra tối đa **270 s** và **0%** cơ hội thêm với lỗi xác định (buổi 07 QT 5.1) | §7 — hôm nay cũng nhân, nhưng nhân **phút runner** chứ không nhân thời gian chờ |
| 3 | Hạn giờ của một job đến từ mấy nguồn, ai thắng | **3** nguồn: project · `timeout` của job · `config.toml`. Giá trị **nhỏ nhất** thắng; nguồn khó tìm nhất nằm ngoài repo (buổi 07 QT 6.1) | §7 QT 7.1 — `concurrent` cũng là một trần nằm ngoài repo, và cũng thắng theo **min** |
| 4 | `pending` khác hết hạn giờ ở đâu | Ở trường `runner`: `null` nghĩa là **chưa ai nhận**; có giá trị nghĩa là **đã nhận rồi mà không tiến triển** (buổi 07 QT 6.2) | §7 QT 7.1 — `queued_duration` là con số chứng minh ta thiếu slot, không thiếu `needs` |
| 5 | Vì sao bật `interruptible` cho 9 trong 10 job vẫn không tiết kiệm gì | Vì giá trị của nó là **nhị phân theo cả pipeline**: **1** job không `interruptible` đang chạy là đủ để không huỷ được gì (buổi 07 QT 7.1) | §7 QT 7.1 — lợi ích của DAG cũng nhị phân theo một thứ: đủ slot hay không đủ |



Giai đoạn 1 khép lại với một món nợ ghi rõ ngày. Buổi 03 QT 5.3 chỉ ra một stage chỉ bắt đầu khi **mọi** job stage trước kết thúc, gọi đó là "nguồn lãng phí lớn nhất của pipeline tuần tự", rồi **cố ý không sửa** — vì lúc đó học viên chưa đo được lãng phí ấy bằng giây. Hiện vật `ban-do-phu-thuoc.md` của buổi 03 lập ra để chờ hôm nay, và BTVN 4 buổi 07 vừa buộc mỗi người cộng `duration` theo stage cho một pipeline thật rồi tìm đường dài nhất theo dữ liệu — nghĩa là con số lãng phí của repo mình, ai cũng **đã có sẵn** trước khi vào lớp. Hôm nay có hai nửa: biến con số đó thành cấu hình, và trả đúng cái giá của việc đó.

**Luận đề trung tâm.**

> **Bỏ hàng rào `stage` đổi công thức tính thời gian pipeline: từ TỔNG THEO STAGE của job chậm nhất mỗi stage, sang ĐƯỜNG GĂNG DÀI NHẤT theo quan hệ dữ liệu. Chênh lệch giữa hai con số đó là lãng phí hàng rào — nó có thật, đo được bằng giây, và `needs` là cách duy nhất lấy lại. Nhưng đổi lại, thứ tự chạy không còn được nền tảng bảo đảm hộ ta nữa: cạnh nào ta quên khai thì job đó chạy sớm, và nó chạy sớm một cách IM LẶNG.**

```
   TUẦN TỰ (hàng rào stage)                DAG (needs)
   ────────────────────────                ────────────────────
   T = Σ  max(job trong stage)             T = max  Σ(job trên một đường)
       stage                                   đường

   "tổng của các max"                      "max của các tổng"

   Ví dụ chuẩn của buổi — 8 job trên 4 stage:
     stage build   : build-fe 60 · build-be 90 · lint 20 · scan 150
     stage test    : test-unit 45 (cần build-be) · test-e2e 120 (cần cả hai build)
     stage package : package 30 (cần cả hai build)
     stage deploy  : deploy 25 (cần package · test-unit · test-e2e)

   Tổng theo stage = 150 + 120 + 30 + 25 = 325 s
   Đường găng      = build-be 90 → test-e2e 120 → deploy 25 = 235 s
   LÃNG PHÍ HÀNG RÀO = 90 s = 28%     ← scan 150 s chặn mọi thứ mà không ai cần nó
   Tổng phút runner  = 540 s Ở CẢ HAI CA  ← DAG không giảm phút runner, chỉ giảm chờ
```

Hai dòng cuối là hai dòng đắt nhất của cả buổi. Dòng trên là lý do ta làm việc này. Dòng dưới là lý do đừng mang `needs` đi bán cho người trả tiền hoá đơn runner: họ trả **540 s** trước và sau, không đổi một giây. Người được lợi là lập trình viên đang chờ merge request xanh — **90 s** mỗi lần chạy, nhân với số lần chạy mỗi ngày.

**Kết quả buổi trước được dùng lại.** Mỗi dòng là tiền đề của một mục hôm nay.

| Kết quả | Nguồn | Dùng ở đâu hôm nay |
|---|---|---|
| `stage` là ràng buộc **thứ tự**, không phải ràng buộc **dữ liệu** | buổi 03 QT 5.1 | §4 — hôm nay tách hẳn hai thứ đó ra bằng cấu hình; **lần thứ 3** |
| Một stage chỉ bắt đầu khi **mọi** job stage trước kết thúc — nguồn lãng phí lớn nhất | buổi 03 QT 5.3 | §4 QT 4.1 — hôm nay **đo** rồi **sửa**; **lần thứ 2**, và là lần sửa |
| Hiện vật `ban-do-phu-thuoc.md` | buổi 03 lab | §5 QT 5.1 — đầu vào trực tiếp, mỗi mũi tên thành **một** dòng `needs` |
| Mặc định job tải artifact của **mọi** job ở **mọi** stage trước | buổi 05 QT 5.1 | §4 QT 4.3 — `needs` phá mặc định này, và đó là ca hỏng ồn ào duy nhất của buổi |
| `dependencies` thu hẹp artifact; `needs` đổi **cả** thứ tự **và** artifact | buổi 05 QT 5.2 | §4 QT 4.3 — **lần thứ 2** |
| Artifact rỗng mà job xanh; phải có khẳng định | buổi 05 QT 5.3, buổi 01 QT 7.3 | §5 QT 5.2 — DAG thiếu cạnh cho ra **đúng** lớp lỗi đó; **lần thứ 6** |
| `needs` trỏ job không có mặt gây lỗi tạo pipeline; `optional` làm nó im lặng | buổi 04 QT 7.3 | §5 QT 5.3 — **lần thứ 2**, giờ đo hậu quả bằng giây |
| `concurrent` là trần **toàn cục**, `limit` là trần một mục runner, thắng theo **min** | buổi 02 QT 6.1 | §7 QT 7.1 — song song đổi chờ thành **slot**; **lần thứ 2** |
| Thêm runner **không** giúp nếu nút cổ chai là CPU, đĩa, mạng | buổi 02 QT 6.2 | §7 QT 7.1 — lý do DAG có thể không nhanh hơn một giây nào |
| `go-roi.sh` đọc `duration` từng pha qua API | buổi 07 lab B1 | Lab bước 1 và 2 — nền của `do-duong-gang.sh` |
| Bảng hai thuộc tính hỏng: im lặng/ồn ào × chặn/không chặn | buổi 01 QT 7.1 | §5, §6 — **lần thứ 8** |

**Nguyên lý xuất hiện lần thứ mấy.** Giảng viên **nói ra con số**, để học viên thấy đây là công cụ dùng lại:

- **Bảng hai thuộc tính hỏng** — **lần thứ 8**. Buổi này góp **6** chế độ hỏng mới, **5** trong 6 nằm ở ô *im lặng + không chặn*.
- **"Hành vi phụ thuộc phiên bản thì phải ĐO, không tra"** — **lần thứ 8**. Hôm nay có ba đại lượng thuộc loại đó: trần `needs`, ràng buộc `needs` theo stage, và việc `needs:project` có chạy trên GitLab CE hay không.
- **"Job xanh không chứng minh gì, phải có khẳng định"** — **lần thứ 6**. Hôm nay khẳng định phải trả lời một câu mới: tệp này **mới** hay **cũ**, không chỉ có hay không có.
- **Lãng phí hàng rào stage** — **lần thứ 2**. Buổi 03 nêu, buổi 08 sửa.

**Ba câu hỏi trung tâm của buổi:**

1. Pipeline của tôi lãng phí bao nhiêu **giây** vì hàng rào stage, và tôi lấy lại được bao nhiêu trong số đó?
2. Khi bỏ hàng rào, cạnh nào tôi quên khai — và tôi phát hiện ra bằng cách nào, vì job vẫn **xanh**?
3. Chia một job test thành 4 phần thì nó nhanh gấp mấy — và vì sao **không** phải gấp 4?

**Ba câu BTVN 4 buổi 07 đáp thẳng vào ba mục hôm nay** — gọi ba học viên đọc con số đã ghi, ghi lên bảng để đối chiếu cuối buổi: câu 1 (cộng `duration` theo stage và tìm đường dài nhất) → §4 QT 4.1 và lab bước 1; câu 2 (đếm cặp job không cần chờ nhau) → §5 QT 5.1 và lab bước 2; câu 3 (chia test thành 5 phần thì cái gì phải đổi) → §6 QT 6.1 và QT 6.4.

---



| # | Làm được gì | Hiện vật chứng minh |
|---|---|---|
| LĐ1 | Tính **hai** con số thời gian cho một pipeline bất kỳ — tổng theo stage và đường găng — bằng script, không bằng cách nhìn biểu đồ | `bang-duong-gang.tsv` và `do-duong-gang.sh`, lab bước 1 CHECKPOINT 1, 2 |
| LĐ2 | Dịch một bản đồ phụ thuộc dữ liệu thành các dòng `needs`, và **đếm** để chứng minh không thiếu không thừa cạnh | `dag.mmd` đặt cạnh `.gitlab-ci.yml`, lab bước 2 CHECKPOINT 3 |
| LĐ3 | Trả lời "job này nhận được mấy tệp" trước và sau khi thêm `needs`, bằng số | Lab bước 2 CHECKPOINT 4, 5 |
| LĐ4 | Nhận ra "pipeline nhanh hơn dự kiến **35 s**" là **dấu hiệu hỏng**, và chứng minh bằng mốc thời gian của tệp | Lab bước 3 CHECKPOINT 6 |
| LĐ5 | Viết khẳng định làm job **đỏ** khi nó đang đọc một hiện vật **cũ hơn** pipeline hiện tại | Lab bước 3 CHECKPOINT 6, 7 |
| LĐ6 | Chia một job test thành N phần theo `CI_NODE_INDEX`, và đo đường cong bão hoà ở bốn mức 1 · 2 · 4 · 8 | `chia-viec.sh` và bảng 4 dòng, lab bước 4 CHECKPOINT 8, 9 |
| LĐ7 | Viết job gộp báo cáo có khẳng định số tệp đầu vào, và chỉ ra coverage sai bằng tỉ số **1/N** | Lab bước 4 CHECKPOINT 10 |
| LĐ8 | Phân biệt "DAG không có tác dụng" với "thiếu slot runner" bằng tổng `queued_duration` | Lab bước 5 CHECKPOINT 11 |

---



| Cần biết | Mức yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| `stage` là ràng buộc thứ tự; hàng rào stage là nguồn lãng phí | **Vận dụng** | buổi 03 QT 5.1, QT 5.3 — tiền đề của cả §4 |
| Dữ liệu giữa hai job đi bằng `artifacts`, không đi bằng `stage` | **Vận dụng** | buổi 01 QT 5.1, buổi 05 QT 4.1 |
| Mặc định tải artifact của mọi stage trước, và cách thu hẹp | **Vận dụng** | buổi 05 QT 5.1, QT 5.2 — không có nó thì QT 4.3 hôm nay vô nghĩa |
| Artifact rỗng vẫn xanh; khẳng định là đường thoát duy nhất | **Vận dụng** | buổi 05 QT 5.3, buổi 01 QT 7.3 |
| `rules` chốt danh sách job ở `t0`; job không khớp thì **biến mất** | Vận dụng | buổi 04 QT 4.1, QT 6.2 — nền của `needs:optional` |
| `concurrent` và `limit`, thắng theo min | **Vận dụng** | buổi 02 QT 6.1, QT 6.2 — nền của §7 |
| Đọc `duration`, `queued_duration`, `started_at` của job qua API | **Vận dụng** | buổi 07 lab B1 (`go-roi.sh`), buổi 01 QT 4.2 |
| Bảng hai thuộc tính hỏng: im lặng/ồn ào × chặn/không chặn | **Vận dụng** | buổi 01 QT 7.1 — dùng ở §5 và §6 |
| Số học lớp 6: cộng, chia, và phần trăm | Vận dụng | Không có nguồn — nhưng đây là toàn bộ phần toán của buổi |

---



### 3.1. Đối chiếu thuật ngữ

Từ khoá YAML **giữ nguyên tiếng Anh** vì học viên gõ đúng chữ đó vào tệp. Khái niệm thì dùng tiếng Việt, kèm tiếng Anh để đi phỏng vấn nói được.

| Tiếng Việt dùng trong bài | Tiếng Anh | Dùng thẳng tiếng Anh trong thân bài? |
|---|---|---|
| đồ thị có hướng không chu trình | directed acyclic graph | **Có** — DAG |
| cạnh phụ thuộc | dependency edge | Việt |
| đường găng | critical path | Việt |
| hàng rào stage | stage barrier | Việt |
| lãng phí hàng rào | barrier waste | Việt |
| phụ thuộc tường minh | explicit dependency | **Có** — `needs` |
| phụ thuộc tuỳ chọn | optional dependency | **Có** — `needs:optional` |
| chia phần song song | job parallelization | **Có** — `parallel` |
| ma trận biến | matrix | **Có** — `parallel:matrix` |
| chỉ số phần · tổng số phần | node index · node total | **Có** — `CI_NODE_INDEX`, `CI_NODE_TOTAL` |
| tích Descartes | Cartesian product | Việt |
| phần cố định · phần chia được | fixed cost · divisible cost | Việt |
| gộp báo cáo | report aggregation | Việt |
| slot runner | runner slot | Việt + "slot" |
| phụ thuộc liên project | cross-project dependency | **Có** — `needs:project` |
| thời gian chờ của lập trình viên | developer wait time | Việt |
| cạnh cổng | gate edge | Việt |
| thời gian xếp hàng | queued duration | **Có** — `queued_duration` |



Pipeline tuần tự là **tổng của các max**; pipeline DAG là **max của các tổng**. Hai câu đó là toàn bộ phần toán của buổi, và chúng cho hai con số khác nhau trên cùng một tập job: **325 s** so với **235 s**. Hiệu của chúng là ngân sách tối ưu của ta, tính bằng giây.

Giá trị đo được: người không có mô hình này rút ngắn job **chậm nhất** — ở ví dụ chuẩn là `scan` 150 s — và được **0** giây, vì `scan` không nằm trên đường găng. Người có mô hình này chỉ chạm vào ba job trên đường găng. Quay lại ở buổi 09, 13, **14**, 22, 46.

### 3.3. Mô hình tư duy 2: cạnh bị quên là hỏng im lặng

Thiếu một cạnh `needs` làm pipeline **nhanh hơn và sai** cùng lúc — kết hợp tệ nhất có thể có, vì hai nửa triệt tiêu nhau trong đầu người quan sát: nhanh hơn là tin tốt nên không ai điều tra, còn phần sai thì không có dòng log nào nói ra. Artifact rỗng của buổi 05 ít nhất còn để lại một tệp 0 byte; cạnh bị quên **không để lại gì** ngoài một con số thời gian tốt hơn dự kiến.

Vì vậy từ hôm nay, "pipeline nhanh hơn dự kiến" vào danh sách triệu chứng phải điều tra, ngang hàng với "pipeline đỏ". Quay lại ở buổi 09, 22, 27, 34.

### 3.4. Mô hình tư duy 3: phần cố định không chia được

Mỗi job có một phần thời gian **không** phụ thuộc lượng việc: kéo image, khởi tạo container, clone repo, phục hồi cache, tải artifact, khởi động công cụ test. Chia N phần thì phần đó bị trả **N lần**, nên tốc độ thật là `T / (cố_định + biến/N)`, trần là `T / cố_định` dù N lớn đến đâu.

Con số của buổi: job test 120 s gồm **25 s cố định + 95 s biến**. `parallel: 4` cho **49 s**, nhanh **2,45** lần — không phải 4 lần. Trần lý thuyết là **4,8** lần, đạt được khi N tiến ra vô cùng, tức không bao giờ. Quay lại ở buổi 14, 16–21, 30, 33.

### 3.5. Mô hình tư duy 4: chờ khác tốn

Có hai đại lượng, và người trả tiền cho chúng là hai người khác nhau. **Thời gian chờ** là của lập trình viên đang ngồi đợi merge request xanh. **Phút runner** là của người ký hoá đơn hạ tầng. `needs` giảm thứ nhất mà **không** đổi thứ hai — 540 s trước và sau. `parallel` giảm thứ nhất và **tăng** thứ hai — từ 120 s lên 196 s, tức **+63%**.

Hệ quả: khi trình bày một thay đổi pipeline, nói ra **cả hai** con số. Quay lại ở buổi 13, 14, **46**.

---
### 1.1. Hai công thức tính thời gian pipeline (10 phút)

Ví dụ chuẩn của buổi có **4** stage và **8** job. Tám job này quay lại ở mọi mục sau, ở lab bước 1–3, và ở câu 2 phần vấn đáp — học viên nên chép bảng dưới vào vở.

| Job | stage | Thời lượng | Cần dữ liệu của | Bắt đầu (tuần tự) | Bắt đầu (DAG) |
|---|---|---|---|---|---|
| `build-fe` | build | 60 s | — | 0 | 0 |
| `build-be` | build | 90 s | — | 0 | 0 |
| `lint` | build | 20 s | — | 0 | 0 |
| `scan` | build | **150 s** | — | 0 | 0 |
| `test-unit` | test | 45 s | `build-be` | 150 | 90 |
| `test-e2e` | test | **120 s** | `build-fe`, `build-be` | 150 | 90 |
| `package` | package | 30 s | `build-fe`, `build-be` | 270 | 90 |
| `deploy` | deploy | 25 s | `package`, `test-e2e`, và **chờ** `test-unit` | 300 | 210 |

**Tổng theo stage** = `max(60, 90, 20, 150)` + `max(45, 120)` + `30` + `25` = 150 + 120 + 30 + 25 = **325 s**.
**Đường găng** = `build-be` 90 → `test-e2e` 120 → `deploy` 25 = **235 s**. Ba đường khác ngắn hơn: qua `package` là 145 s, qua `test-unit` là 160 s, còn `scan` kết thúc ở giây thứ 150 và không có job nào phía sau.
**Lãng phí hàng rào** = 325 − 235 = **90 s**, tức **28%** thời gian pipeline.
**Tổng phút runner** = 60 + 90 + 20 + 150 + 45 + 120 + 30 + 25 = **540 s** — **ở cả hai ca**, không đổi một giây.

**Nguyên lý cốt lõi:** Pipeline tuần tự mất **tổng theo stage của job chậm nhất mỗi stage**; pipeline DAG mất **đường dài nhất theo quan hệ dữ liệu**. Hiệu của hai số là **lãng phí hàng rào**, và nó tồn tại độc lập với việc runner có mạnh hay không.

**Giải thích cơ chế ngầm:** Hàng rào stage buộc mọi job chờ job chậm nhất **cùng stage**, kể cả job không có một byte dữ liệu liên quan tới nó (buổi 03 QT 5.3 — lần thứ 2). Ở ví dụ chuẩn, `test-unit` chỉ cần `build-be` xong ở giây 90 nhưng phải đợi `scan` xong ở giây 150: **60 giây** ngồi không vì một job không ai đọc kết quả. Bỏ hàng rào thì mỗi job chỉ chờ đúng thứ nó cần, nên thời gian pipeline tụt về độ dài **một** đường — đường dài nhất.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Một job `scan` hoặc `lint` dài chặn cả pipeline: xoá tạm nó thì pipeline nhanh hơn hẳn dù không ai dùng kết quả. Dấu hiệu đo được: job có `duration` nhỏ mà khoảng cách từ `created_at` của pipeline tới `started_at` của nó lớn — đó là chờ hàng rào, không phải xếp hàng.

**Minh hoạ.**

```yaml
# Pipeline mẫu 8 job — dán NGUYÊN vào .gitlab-ci.yml của project lab08-dag.
# Dùng sleep vì thời lượng job phải là hằng số ta đặt được: công việc thật dao
# động 10–30% và làm mất chính tín hiệu cấu trúc đồ thị mà ta cần đo.
stages: [build, test, package, deploy]

default:
  image: alpine:3.20
  artifacts:
    expire_in: 1h

build-fe:
  stage: build
  script: [sleep 60, 'mkdir -p fe && date +%s > fe/dau-thoi-gian.txt']
  artifacts: {paths: [fe/]}

build-be:
  stage: build
  script: [sleep 90, 'mkdir -p be && date +%s > be/dau-thoi-gian.txt']
  artifacts: {paths: [be/]}

lint:
  stage: build
  script: [sleep 20, 'echo "lint xong — không job nào cần kết quả này"']

scan:
  stage: build
  script: [sleep 150, 'echo "scan xong — không ai cần, và nó đang chặn cả pipeline"']

test-unit:
  stage: test
  script:
    - sleep 45
    - test -s be/dau-thoi-gian.txt
    - mkdir -p bao-cao && echo '{"coverage": 82}' > bao-cao/unit.json
  artifacts: {paths: [bao-cao/]}

test-e2e:
  stage: test
  script:
    - sleep 120
    - test -s fe/dau-thoi-gian.txt
    - test -s be/dau-thoi-gian.txt
    - mkdir -p bao-cao && echo '{"e2e": "pass"}' > bao-cao/e2e.json
  artifacts: {paths: [bao-cao/]}

package:
  stage: package
  script:
    - sleep 30
    - test -s fe/dau-thoi-gian.txt
    - test -s be/dau-thoi-gian.txt
    - mkdir -p goi && tar czf goi/app.tgz fe be
  artifacts: {paths: [goi/]}

deploy:
  stage: deploy
  script:
    - sleep 25
    - test -s goi/app.tgz
    - test -s bao-cao/e2e.json
    - 'echo "deploy goi $(wc -c < goi/app.tgz) byte"'
```

```bash
# Hai con số từ MỘT lệnh — nền của do-duong-gang.sh ở lab bước 1.
# Nhóm job theo stage, lấy max duration mỗi nhóm, rồi cộng.
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?per_page=100" \
| jq -r '
    (group_by(.stage) | map({stage: .[0].stage, cham_nhat: (map(.duration) | max)})) as $s
    | ($s | map(.cham_nhat) | add) as $tong_stage
    | (map(.duration) | add) as $phut_runner
    | "tong theo stage = \($tong_stage | floor) s   phut runner = \($phut_runner | floor) s"'

# Thời gian pipeline THẬT (đường găng khi đã khai needs): lấy từ chính pipeline.
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE" | jq '{duration, queued_duration, status}'
```

**Con số chốt.** Tổng theo stage **325 s**; đường găng **235 s**; lãng phí **90 s = 28%**; phút runner **540 s** ở **cả hai** ca. Hai con số 90 s và 28% **không phổ quát** — chúng là số của ví dụ chuẩn với một job `scan` 150 s lệch pha. Repo không có job dài nằm ngoài quan hệ dữ liệu thì lãng phí gần **0** và `needs` không đáng làm, xem §8.

**Nguyên lý cốt lõi:** `needs` **không** xoá `stage`: `stage` vẫn tồn tại, vẫn quyết định cách pipeline được vẽ ra, và vẫn giới hạn được job nào có thể `needs` job nào. `needs` chỉ bỏ **điều kiện chờ** của hàng rào.

**Giải thích cơ chế ngầm:** Hai khái niệm ở hai tầng. `stage` là **thuộc tính khai báo** của job; hàng rào là **hành vi mặc định** dựa trên thuộc tính ấy: "chưa chạy job stage sau khi stage trước còn job chưa kết thúc". `needs` thay hành vi bằng một danh sách tường minh, nó không xoá thuộc tính.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Xoá khối `stages` để "chuyển sang DAG" rồi nhận lỗi tạo pipeline, hoặc nhận một biểu đồ dồn 20 job vào một cột không đọc được ai chờ ai. Dấu hiệu thứ hai: khai `needs` trỏ job ở stage **sau** và pipeline không được tạo — phụ thuộc phiên bản, phải đo.

**Phần ràng buộc theo stage là loại (c) — phải đo, không tra.** Ràng buộc "job được `needs` phải cùng stage hoặc stage trước" đã đổi trong dòng 14.x–17.x, nên lab bước 2 khai một cạnh ngược stage rồi gọi `ci/lint` (buổi 03 QT 4.3) và ghi kết quả kèm số phiên bản. **Lần thứ 8** khoá này nói câu "phụ thuộc phiên bản thì phải đo".

**Minh hoạ.** Cùng một DAG viết hai lần: bản A giữ `stages: [build, test, package, deploy]`, bản B đổi thành `stages: [tat-ca]` và đặt `stage: tat-ca` cho cả 8 job, giữ nguyên mọi dòng `needs`. Hai bản cho **cùng 235 s**; bản B cho một biểu đồ một cột không đọc được — đó là toàn bộ lý do giữ `stage`.

```bash
# Đo ràng buộc theo stage mà KHÔNG cần chạy pipeline: hỏi ci/lint.
# Sửa tệp cho deploy needs một job ở stage SAU nó rồi chạy đoạn này.
jq -Rs '{content: .}' < .gitlab-ci.yml > /tmp/lint.json
curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" --data @/tmp/lint.json \
  "$GITLAB/api/v4/projects/$PID/ci/lint" | jq '{valid, errors}'
# valid=false kèm thông báo về needs -> ràng buộc còn hiệu lực trên bản này.
# valid=true                        -> bản này đã bỏ ràng buộc. Ghi số phiên bản vào hiện vật.
```

**Con số chốt.** **50** là trần số phần tử `needs` của một job ở GitLab CE 17.7. Trần này đã đổi nhiều lần, nên đừng chép số 50 vào tài liệu nội bộ — chép **cách đo**: thêm phần tử thứ 51 rồi gọi `ci/lint`. Nó chỉ chạm phải khi có người sinh `needs` bằng script cho monorepo, tức bài toán buổi 09 và 22.

**Nguyên lý cốt lõi:** `needs` mang **hai** việc cùng lúc: đổi thứ tự chạy **và** thu hẹp tập artifact tải về đúng danh sách được liệt kê (buổi 05 QT 5.2 — lần thứ 2). Tách hai việc đó bằng `needs:artifacts: false`, và đây là cách duy nhất nói được "chờ nó, nhưng không cần tệp của nó".

**Giải thích cơ chế ngầm:** Mặc định của buổi 05 QT 5.1 là "tải artifact của **mọi** job ở **mọi** stage trước". Khi job có `needs`, mặc định đó **không** còn áp dụng — tập nguồn bị thay bằng đúng danh sách `needs`. Một dòng cấu hình cho **hai** thay đổi hành vi, và người khai thường chỉ nghĩ tới thay đổi thứ nhất.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chuyển sang `needs` xong, một job đột nhiên thiếu tệp mà trước đó vẫn có — nó vốn sống nhờ mặc định "tải mọi stage trước". Đây là chế độ hỏng **ồn ào và có chặn** duy nhất của buổi, nhưng nó ồn ào **ở một job khác** với job vừa sửa. Dấu hiệu đo được: số tệp `find` đếm được giảm đúng lúc thêm dòng `needs`.

**Minh hoạ.**

```yaml
# mảnh — thay khối script và thêm needs cho job deploy của pipeline mẫu.
deploy:
  stage: deploy
  needs:
    - package                       # cạnh dữ liệu: deploy đọc goi/app.tgz
    - test-e2e                      # cạnh dữ liệu: deploy đọc bao-cao/e2e.json
    - job: test-unit
      artifacts: false              # CẠNH CỔNG: chờ nó xanh, KHÔNG lấy tệp của nó
  script:
    - 'echo "so tep nhan duoc = $(find fe be goi bao-cao -type f 2>/dev/null | wc -l)"'
    - test -s goi/app.tgz
    - test -s bao-cao/e2e.json
    - test ! -f bao-cao/unit.json    # khẳng định artifacts:false thật sự có tác dụng
    - sleep 25
```

Phép đo: chạy pipeline **một** lần khi `deploy` chưa có `needs`, **một** lần sau khi có, rồi đọc lại dòng `so tep nhan duoc` trong `trace` của cả hai lần bằng `GET /projects/:id/jobs/:job_id/trace` (buổi 07 QT 4.2). Hai con số phải là 5 và 2.

**Con số chốt.** **1** dòng `needs` đổi tập artifact của `deploy` từ **5** tệp xuống **2** tệp (`goi/app.tgz`, `bao-cao/e2e.json`). Nếu `deploy` vốn đang đọc `fe/` mà không ai nhớ, nó hỏng ngay pipeline đầu tiên. Khẳng định `test -s` giá **0,01 giây**.

---

### 1.2. Dựng DAG từ bản đồ phụ thuộc — và cạnh bị quên (9 phút)

**Nguyên lý cốt lõi:** Dựng DAG theo đúng **ba** bước, không đảo thứ tự: (1) lập bản đồ **dữ liệu** — job nào đọc tệp do job nào tạo ra; (2) mỗi mũi tên của bản đồ thành **một** dòng `needs`; (3) **đo lại** đường găng và so với con số cũ. Bỏ bước 3 thì không biết mình vừa sửa được bao nhiêu, và cũng không biết mình có làm chậm đi hay không.

**Giải thích cơ chế ngầm:** `needs` là bản **dịch cơ học** của quan hệ dữ liệu: việc suy nghĩ đã xong ở bước 1, nơi ta trả lời câu hỏi kiểm chứng được ("job này đọc tệp nào, do ai tạo") thay vì câu cảm tính ("job này nên chạy sau ai"). Khai theo **cảm nhận thứ tự** cho ra hai lỗi đối xứng: thiếu cạnh (QT 5.2) và thừa cạnh — chờ vô ích, không ai phát hiện vì pipeline vẫn đúng, chỉ chậm.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bản đồ có 8 mũi tên mà YAML có 6 phần tử `needs` — thiếu 2 cạnh. Hoặc ngược lại: YAML có cạnh mà bản đồ không có, tức job chờ thứ nó không đọc, và mỗi cạnh thừa cộng thẳng vào đường găng. Dấu hiệu bỏ bước 3: có người tuyên bố "đã chuyển sang DAG" mà không nói được con số trước và sau.

**Minh hoạ.**

```
# ban-do-phu-thuoc.md của buổi 03 — 8 mũi tên = 7 cạnh DỮ LIỆU + 1 cạnh CỔNG

  build-be  -> test-unit  : đọc be/dau-thoi-gian.txt   needs: [build-be]
  build-fe  -> test-e2e   : đọc fe/dau-thoi-gian.txt   needs: [build-fe, build-be]
  build-be  -> test-e2e   : đọc be/dau-thoi-gian.txt
  build-fe  -> package    : đọc fe/                    needs: [build-fe, build-be]
  build-be  -> package    : đọc be/
  package   -> deploy     : đọc goi/app.tgz            needs: [package, test-e2e,
  test-e2e  -> deploy     : đọc bao-cao/e2e.json               {job: test-unit, artifacts: false}]
  test-unit -> deploy     : KHÔNG đọc tệp nào -> cạnh CỔNG
  lint, scan              : không mũi tên nào vào, không mũi tên nào ra
```

```bash
# Bước 3 dạng máy kiểm: đếm mũi tên trong bản đồ và đếm phần tử needs trong YAML.
# Hai con số phải bằng nhau. Chạy trước mỗi lần push đổi cấu trúc pipeline.
MT=$(grep -cE '^[[:space:]]*[a-z0-9-]+[[:space:]]*->' dag.mmd)
CY=$(awk '/^[[:space:]]*needs:/{f=1;next} f&&/^[[:space:]]*-[[:space:]]/{n++;next}
          f&&!/^[[:space:]]*(-|[[:space:]]|artifacts:|job:)/{f=0} END{print n+0}' .gitlab-ci.yml)
[ "$MT" -eq "$CY" ] && echo "ĐẠT: $MT mũi tên = $CY phần tử needs" \
                    || echo "LỖI: bản đồ $MT mũi tên, YAML $CY phần tử needs"
```

**Con số chốt.** **3** bước; ví dụ chuẩn có **7** cạnh dữ liệu cộng **1** cạnh cổng và lấy lại **90 s** — hơn **11 giây** mỗi dòng `needs`, tỉ lệ lợi ích trên mỗi dòng YAML cao nhất của giai đoạn 2.

**Nguyên lý cốt lõi:** DAG **thiếu** một cạnh cho ra pipeline **nhanh hơn và sai**: job chạy trước khi dữ liệu nó cần tồn tại, rồi vẫn **xanh** vì nó đọc được một bản cũ trong cache, một tệp có sẵn trong git, hoặc một thư mục rỗng mà script không kiểm. Đây là chế độ hỏng đặc trưng của buổi này, và nó không có triệu chứng nào ngoài việc **nhanh hơn dự kiến**.

**Giải thích cơ chế ngầm:** Bỏ hàng rào nghĩa là nền tảng **thôi bảo đảm thứ tự hộ ta** — hàng rào là lưới an toàn ta không phải trả tiền, vì trong pipeline tuần tự một job stage `deploy` không thể chạy trước job stage `build` dù khai sai thế nào. Từ khi có `needs`, thứ tự đúng là **trách nhiệm của người khai**: GitLab không biết `test-e2e` đọc `be/dau-thoi-gian.txt`, nó chỉ biết ta bảo `test-e2e` cần `build-fe`. Cộng hai cơ chế của giai đoạn 1 — cache còn bản cũ (buổi 05 QT 4.3) và shell coi thư mục rỗng là bình thường (buổi 06 mô hình tư duy 3) — ba thứ gặp nhau ở ô **im lặng + không chặn**, **lần thứ 8** khoá này dùng bảng hai thuộc tính.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thời gian pipeline giảm **nhiều hơn** mức tính từ đường găng. Ở ví dụ chuẩn, bỏ cạnh `test-e2e ← build-be` cho **205 s**: **30 s** do `test-e2e` khởi động ở giây 60 thay vì 90, cộng khoảng **5 s** do thôi phải tải artifact của `build-be` (QT 4.3) — tổng **khoảng 35 s**. Dấu hiệu chắc chắn hơn: hiện vật job đang đọc có mốc thời gian **cũ hơn** lúc pipeline được tạo, tức nó đến từ pipeline trước hoặc từ git.

**Minh hoạ.**

```yaml
# mảnh — dán vào ĐẦU script của MỌI job có cạnh needs mang dữ liệu.
# Hiện vật của pipeline mẫu tự đóng dấu epoch, nên khẳng định là một phép so số.
  script:
    - apk add --no-cache coreutils >/dev/null
    - MOC=$(date -d "$CI_PIPELINE_CREATED_AT" +%s)
    - test -s be/dau-thoi-gian.txt || { echo "LỖI: thiếu be/dau-thoi-gian.txt"; exit 1; }
    - |
      if [ "$(cat be/dau-thoi-gian.txt)" -lt "$MOC" ]; then
        echo "LỖI: hiện vật sinh TRƯỚC pipeline này ($(cat be/dau-thoi-gian.txt) < $MOC)"
        echo "     -> đang thiếu một cạnh needs, hoặc đang đọc bản cũ trong cache"
        exit 1
      fi
      echo "ĐẠT: hiện vật thuộc đúng pipeline này"
```

Với repo thật, nơi hiện vật không tự đóng dấu thời gian, dạng tương đương là một dòng `find` (cần `apk add findutils` trên Alpine): `find dist/ -type f -newermt "$CI_PIPELINE_CREATED_AT" | grep -q . || { echo "LỖI: không tệp nào mới hơn t0"; exit 1; }`.

**Con số chốt.** **1** cạnh thiếu làm pipeline nhanh hơn khoảng **35 s** so với đường găng đúng — **tín hiệu duy nhất** ta có. Khẳng định `find -newermt` tốn **0,2 giây** mỗi job và biến ô *im lặng + không chặn* thành *ồn ào + có chặn*.

**Nguyên lý cốt lõi:** `needs:optional: true` làm một cạnh **được phép không tồn tại**; khi job nguồn vắng mặt vì `rules` (buổi 04 QT 6.2), cạnh đó biến mất và cả nhánh phía sau chạy sớm hơn dự kiến — im lặng. Trong pipeline tuần tự điều này không xảy ra vì hàng rào vẫn còn.

**Giải thích cơ chế ngầm:** Không có `optional`, `needs` trỏ job không có mặt gây **lỗi tạo pipeline** (buổi 04 QT 7.3 — lần thứ 2): ồn ào, có chặn, sửa ngay. `optional: true` đổi đúng ô đó. Vấn đề là "bỏ qua cạnh" trong DAG nghĩa là **bỏ điều kiện chờ**, nên job sau chạy sớm — và nếu nó vốn đọc tệp của job vắng mặt thì ta rơi vào QT 5.2, với nguyên nhân nằm ở `rules` của một job khác, cách xa chỗ hỏng.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline chạy nhanh khác thường trên nhánh mà một job bị `rules` loại — không ai để ý vì nhanh hơn thì tốt. Cách phát hiện: so **số job** giữa hai nhánh, không so thời gian.

**Minh hoạ.**

```yaml
# Chạy hai lần: một lần trên nhánh mặc định, một lần trên nhánh feature.
# Nhánh feature: sinh-cau-hinh KHÔNG có mặt -> cạnh mất -> dung-cau-hinh chạy ngay ở giây 0.
sinh-cau-hinh:
  stage: build
  image: alpine:3.20
  rules:
    - if: $CI_COMMIT_REF_NAME == $CI_DEFAULT_BRANCH
  script:
    - sleep 40
    - echo "cau_hinh=that" > cau-hinh.env
  artifacts:
    paths: [cau-hinh.env]

dung-cau-hinh:
  stage: test
  image: alpine:3.20
  needs:
    - job: sinh-cau-hinh
      optional: true                 # KHÔNG có dòng này -> lỗi tạo pipeline trên nhánh feature
  script:
    - 'echo "job hien co trong pipeline nay: $CI_JOB_NAME"'
    - test -s cau-hinh.env || { echo "LỖI: cạnh optional đã mất, không có cấu hình"; exit 1; }
```

Phép so đúng là đếm **số job** của pipeline trên hai nhánh, không so thời gian: `GET /projects/:id/pipelines/:pipeline_id/jobs` rồi `jq 'length'`. Nhánh mặc định cho **2**, nhánh feature cho **1** — chênh 1 job là chênh 1 cạnh.

**Con số chốt.** **1** cờ `optional` biến **1** lỗi ồn ào có chặn thành **1** cạnh mất im lặng không chặn: nhánh feature nhanh hơn **40 s** và `dung-cau-hinh` chạy mà không có cấu hình. Dòng `test -s` là thứ duy nhất giữ lại phần "có chặn".

---

### 1.3. `parallel` và `parallel:matrix` (10 phút)

**Nguyên lý cốt lõi:** `parallel: N` sinh **N** job **giống nhau như đúc**; điều duy nhất khác nhau giữa chúng là `CI_NODE_INDEX`. Việc **chia việc** hoàn toàn thuộc về `script` — GitLab không biết gì về nội dung công việc. Không chia thì N job làm **cùng một việc N lần**, vẫn xanh, và tốn N lần phút runner.

**Giải thích cơ chế ngầm:** Nền tảng chỉ làm hai thứ: nhân bản định nghĩa job N lần, và bơm vào mỗi bản hai biến `CI_NODE_INDEX` (1 tới N) và `CI_NODE_TOTAL` (N). Nó không biết bộ test của ta chia được theo tệp, theo thư mục, hay không chia được. Công cụ test có sẵn tham số chia phần (`--shard`) thì việc của ta chỉ là truyền hai biến vào; không có thì phải tự chia bằng shell, và **không ai nhắc rằng ta chưa chia**.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> 4 job song song, mỗi job in **cùng** số test và có `duration` gần bằng job gốc — chia đúng thì thời lượng mỗi phần phải **giảm**. Phút runner tăng gấp 4 mà thời gian pipeline không giảm một giây. Ô bảng hai thuộc tính: **im lặng, không chặn**.

**Minh hoạ.**

```yaml
# 40 tệp test chia cho 4 phần, mỗi phần đúng 10 tệp. Nền của chia-viec.sh ở lab bước 4.
test-chia-phan:
  stage: test
  image: alpine:3.20
  parallel: 4
  script:
    - mkdir -p test && i=1; while [ $i -le 40 ]; do echo "case $i" > "test/t$i.spec"; i=$((i+1)); done
    # Chia theo phần dư: phần i nhận tệp có NR chia n dư i mod n. Không trùng, không sót.
    - ls -1 test/*.spec | awk -v i="$CI_NODE_INDEX" -v n="$CI_NODE_TOTAL" 'NR % n == i % n' > phan.txt
    - SO=$(wc -l < phan.txt); echo "phan $CI_NODE_INDEX/$CI_NODE_TOTAL nhan $SO tep"
    # Khẳng định chống ca "không chia việc": mỗi phần PHẢI nhận ít hơn tổng số tệp.
    - test "$SO" -lt 40 || { echo "LỖI: phần này nhận đủ 40 tệp — chưa chia việc"; exit 1; }
    - while read -r f; do sleep 2; echo "chay $f"; done < phan.txt
    - mkdir -p bao-cao && echo "{\"phan\": $CI_NODE_INDEX, \"so_test\": $SO}" > "bao-cao-$CI_NODE_INDEX.json"
  artifacts:
    paths: ["bao-cao-*.json"]
```

**Con số chốt.** `parallel` nhận **2–200** ở GitLab CE 17.7 (loại (c), đo bằng `ci/lint`). **4** job không chia việc = **4 lần** cùng công việc: **40** tệp thành **160** lần chạy test. Dòng `test "$SO" -lt 40` tốn **0,01 giây** và là thứ duy nhất phân biệt "đã chia" với "chưa chia".

**Nguyên lý cốt lõi:** `parallel:matrix` sinh job theo **tích Descartes** của các danh sách biến, nên số job **nhân lên** chứ không cộng vào: thêm một giá trị vào một biến làm số job tăng theo tích của các biến còn lại.

**Giải thích cơ chế ngầm:** Matrix là cách khai một **tổ hợp**, và tổ hợp lớn lên theo phép nhân: hai biến có `|a|` và `|b|` giá trị cho `|a| × |b|` job, nên thêm một giá trị vào `a` là thêm `|b|` job. Trực giác "thêm một dòng thì thêm một việc" đúng với mọi khoá khác của GitLab CI và sai với đúng khoá này.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thêm một phiên bản Node vào danh sách và hôm sau hàng đợi runner đầy, hoặc thời gian chờ trung bình của cả nhóm tăng mà không ai đổi gì ngoài một dòng YAML. Dấu hiệu ồn ào: pipeline bị từ chối vì vượt trần số job của một khối matrix.

**Minh hoạ.**

```yaml
# 3 phiên bản × 2 nền = 6 job. Tên job sinh ra: kiem-tra-tuong-thich: [18, alpine], ...
kiem-tra-tuong-thich:
  stage: test
  image: node:$PHIEN_BAN-$NEN
  parallel:
    matrix:
      - PHIEN_BAN: ["18", "20", "22"]     # thêm "23" vào đây -> 4 × 2 = 8 job, không phải 7
        NEN: ["alpine", "slim"]
  script:
    - 'echo "$CI_JOB_NAME chay tren $(node --version)"'
    - node -e 'process.exit(0)'
```

```bash
# Đếm số job matrix sinh ra TRƯỚC khi push — rẻ hơn đếm sau khi hàng đợi đã đầy.
jq -Rs '{content: .}' < .gitlab-ci.yml > /tmp/lint.json
curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" --data @/tmp/lint.json \
  "$GITLAB/api/v4/projects/$PID/ci/lint?include_jobs=true" \
| jq '[.jobs[] | select(.name | startswith("kiem-tra-tuong-thich"))] | length'   # 6, rồi 8
```

**Con số chốt.** **3 × 2 = 6** job; thêm **1** giá trị → **8** job, tức **+2** chứ không phải +1. Trần của một khối matrix là **200** job ở GitLab CE 17.7 — loại (c), phụ thuộc phiên bản. Con số cần nhớ không phải 200 mà là phép nhân: một matrix ba biến 5 × 4 × 3 đã là **60** job, và nếu mỗi job tốn 90 s thì đó là **90 phút** runner cho một lần push.

**Nguyên lý cốt lõi:** Chia thành N phần **không** cho tốc độ gấp N lần, vì mỗi phần vẫn phải trả **phần cố định**: khởi tạo container, phục hồi cache, tải artifact, khởi động công cụ test. Tốc độ thật là `T / (cố_định + biến/N)`, và trần của nó là `T / cố_định` dù N lớn bao nhiêu.

**Giải thích cơ chế ngầm:** Phần cố định lặp lại **mỗi phần**, nên chia càng nhỏ thì tỉ lệ phí càng lớn. Đây là chỗ **định lượng ngược lại** của buổi: `parallel` không tệ như người bi quan nói, cũng không tuyến tính như người lạc quan tưởng — nó có một đường cong bão hoà mà ta tính ra được bằng hai điểm đo. Từ `T(1)` và `T(N)`, phần cố định là `(N × T(N) − T(1)) / (N − 1)`; với 120 s và 49 s ở N = 4 thì ra `(196 − 120) / 3 = 25 s`, và biết 25 s là biết trước mọi mức N khác.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tăng `parallel` từ 4 lên 8 mà pipeline chỉ nhanh thêm **12 giây**, trong khi phút runner tăng từ 196 s lên 296 s. Dấu hiệu định lượng: tỉ số `T(N) × N / T(1)` càng lớn hơn 1 thì càng đang trả phí — ở N = 8 nó là **2,47**, nghĩa là ta đang mua 3,24 lần tốc độ bằng 2,47 lần tiền.

**Minh hoạ.**

| `parallel` | Thời lượng phần dài nhất | Nhanh gấp | Phút runner | So với N = 1 |
|---|---|---|---|---|
| 1 | **120 s** | 1,00 lần | 120 s | — |
| 2 | **72 s** | 1,67 lần | 144 s | +20% |
| 4 | **49 s** | **2,45 lần** | 196 s | **+63%** |
| 8 | **37 s** | 3,24 lần | 296 s | +147% |
| ∞ | 25 s | 4,80 lần | rất lớn | — |

```bash
# Đo một mức bằng API (lặp lại cho P = 1, 2, 4, 8 — mỗi mức một pipeline).
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?per_page=100" \
| jq -r '[.[] | select(.name | startswith("test-chia-phan"))]
    | "dai nhat=\(map(.duration) | max | floor) s   phut runner=\(map(.duration) | add | floor) s"'

# Từ hai điểm đo, tính phần cố định: (N * T(N) - T(1)) / (N - 1)
awk 'BEGIN{ t1=120; n=4; tn=49; printf "phan co dinh = %.1f s\n", (n*tn - t1)/(n-1) }'   # 25,3 s
```

**Con số chốt.** Job test **120 s** gồm cố định **25 s** + biến **95 s**. `parallel: 4` cho **49 s**, nhanh **2,45** lần chứ không phải 4 lần; `parallel: 8` cho **37 s**, nhanh **3,2** lần; trần lý thuyết **4,8** lần. Phút runner đi từ **120 s** lên **4 × 49 = 196 s**, tức **+63%**. Tỉ lệ 25/95 **không phổ quát**: repo có phần cố định lớn hơn thì con số tệ hơn nhiều, và job 40 s với 30 s khởi tạo thì chia bao nhiêu phần cũng vô nghĩa — xem §8 "Khi nào KHÔNG nên dùng".

**Nguyên lý cốt lõi:** N job song song sinh **N** báo cáo rời; nếu không có **một** job gộp thì mọi thứ đọc báo cáo — coverage, số test, gate chất lượng — chỉ thấy **1/N** sự thật. Thiếu bước gộp là hỏng im lặng, vì con số vẫn hiện ra, chỉ là nó sai.

**Giải thích cơ chế ngầm:** Mỗi job chạy một tập con nên mỗi báo cáo chỉ nói về tập con đó; việc hợp nhất là việc của ta, không phải của nền tảng. Chỗ nguy hiểm nhất không phải con số hiển thị sai, mà là một **gate** đang đọc con số đó: gate coverage đặt ngưỡng 70% sẽ **chặn** khi thấy 21%, còn gate "số test thất bại bằng 0" sẽ **mở** khi phần chứa test hỏng không nằm trong báo cáo được đọc.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Coverage tụt từ **82%** xuống **21%** đúng vào lần commit bật `parallel: 4`, và tỉ số 21/82 gần đúng **1/4**. Đó là dấu vân tay của lớp lỗi này: khi một chỉ số tụt xuống gần đúng `1/N` của giá trị cũ, đừng đi tìm nguyên nhân trong mã nguồn, đi tìm số phần.

**Minh hoạ.**

```yaml
# parallel KHÔNG nhận biến làm giá trị, nên số 4 phải nằm ở hai chỗ và sửa cùng lúc.
# Đây là một bẫy thật: khai SO_PHAN để khẳng định có chỗ đọc, và ghi chú ngay cạnh.
variables:
  SO_PHAN: "4"                      # phải khớp parallel bên dưới — sửa thì sửa cả hai

gop-bao-cao:
  stage: test
  image: alpine:3.20
  needs: ["test-chia-phan"]         # needs một job parallel -> nhận artifact của CẢ N phần
  script:
    - apk add --no-cache jq >/dev/null
    - N=$(ls bao-cao-*.json 2>/dev/null | wc -l)
    - |
      if [ "$N" -ne "$SO_PHAN" ]; then
        echo "LỖI: chỉ có $N/$SO_PHAN báo cáo — một phần thiếu, con số gộp sẽ SAI"; exit 1
      fi
    - TONG=$(jq -s 'map(.so_test) | add' bao-cao-*.json)
    - 'echo "ĐẠT: gộp $N báo cáo, tổng $TONG test"'
    - jq -s '{so_phan: length, tong_test: (map(.so_test) | add)}' bao-cao-*.json > bao-cao-gop.json
  artifacts:
    paths: [bao-cao-gop.json]
    when: always                    # buổi 05 QT 5.4: báo cáo phải đọc được cả khi job đỏ
```

**Con số chốt.** **N** artifact vào, **1** artifact ra. **1** dòng khẳng định `[ "$N" -ne "$SO_PHAN" ]` chặn được ca thiếu phần; job gộp tốn **+8 giây** mỗi pipeline (kéo image, `apk add jq`, đọc 4 tệp). Tám giây đó là **cái giá bắt buộc** của `parallel`, không phải tuỳ chọn: bật `parallel` mà không có job gộp là đổi 71 giây chờ lấy một chỉ số chất lượng sai.

---

### 1.4. Cái giá: slot runner, phút runner, và phụ thuộc liên project (5 phút)

**Nguyên lý cốt lõi:** DAG và `parallel` đổi **thời gian chờ** thành **số slot runner cần có cùng lúc**: N job song song cần N slot, và trần slot là `min(concurrent, limit)` của buổi 02 QT 6.1 (lần thứ 2). Thiếu slot thì DAG **không nhanh hơn một giây nào** — nó chỉ đổi thứ tự hàng đợi.

**Giải thích cơ chế ngầm:** Nền tảng **cho phép** chạy song song, runner mới là chỗ **có tài nguyên**. `needs` không sinh ra máy: nó chỉ nói với scheduler rằng job này đã đủ điều kiện chạy. Nếu mọi slot đang bận, job đủ điều kiện vẫn nằm `pending` — và thời gian nằm đó xuất hiện ở trường `queued_duration`, không xuất hiện ở `duration`. Thêm vào đó buổi 02 QT 6.2: nếu nút cổ chai là CPU hay đĩa của máy chủ runner thì tăng `concurrent` cũng không giúp, chỉ làm mọi job chậm đều.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chuyển sang DAG mà thời gian pipeline không đổi, và tổng `queued_duration` của các job **tăng lên đúng bằng** phần thời gian tưởng là tiết kiệm được. Kết luận sai mà người ta hay rút ra: "`needs` vô dụng". Kết luận đúng: cấu hình đã đúng, tài nguyên chưa đủ — hai việc của hai người khác nhau, đúng theo ranh giới hai tệp của buổi 02 QT 4.1.

**Minh hoạ.**

```bash
# Hai con số phân biệt "DAG vô dụng" với "thiếu slot". Chạy cho cả hai lần cấu hình.
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?per_page=100" \
| jq -r '"phut runner=\(map(.duration) | add | floor) s   tong xep hang=\(map(.queued_duration // 0) | add | floor) s"'
```

Phép đo cần hạ `concurrent = 2` trong `/etc/gitlab-runner/config.toml` rồi trả lại **8** — hạ tầng **dùng chung**, nên sao lưu trước và khôi phục bắt buộc sau khi đo (buổi 02 QT 4.3). Đường B khi không được sửa tệp đó: chỉ đọc `queued_duration`, không đổi cấu hình.

**Con số chốt.** Ví dụ chuẩn cần **4** slot ở đỉnh — bốn job stage `build` đều đủ điều kiện ở giây 0. Với `concurrent = 8` ta đo được **235 s**; với `concurrent = 2` con số trở lại khoảng **300 s**, tức mất **65** trong **90** giây vừa lấy lại được. Bài lab **đo** con số 300 s này, không tra: nó phụ thuộc thứ tự runner nhận job, nên hai lần chạy có thể lệch nhau vài giây.

**Nguyên lý cốt lõi:** `needs:project` và `needs:pipeline` cho phép lấy artifact từ **project khác**, và cùng lúc tạo ra một phụ thuộc **giữa hai đội**: pipeline của ta hỏng khi đội kia đổi tên job hoặc bỏ artifact. Đây là quyết định tổ chức, không chỉ là dòng cấu hình.

**Giải thích cơ chế ngầm:** Cạnh phụ thuộc đi xuyên biên giới project cũng đi xuyên biên giới **quyền sở hữu**. Trong một project, `needs` trỏ sai gây lỗi tạo pipeline ngay lúc merge request — người gây ra và người chịu hậu quả là một người. Khi cạnh đi ra ngoài, tên job của đội kia thành **giao diện công khai** mà họ không biết mình đã hứa: không có gì ngăn họ đổi tên `dong-goi` thành `build-package`, và không có gì cảnh báo họ rằng ba project khác đang trỏ vào đó.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline hỏng với thông báo không tìm thấy job hoặc không có artifact, `git log` của repo ta ba ngày không có gì mới. Dấu hiệu thứ hai, im lặng hơn: `ref: main` của đội kia đã đi xa mấy chục commit nên ta đang nhận một hiện vật mới hơn dự kiến mà không có phiên bản nào ghi lại — buổi 27 gọi đó là "prod chạy cái gì không ai biết".

**Minh hoạ.**

```yaml
# Cách A — needs:project. PHẢI ĐO trên instance của mình: đây là loại (c),
# và ở GitLab CE tính năng này có thể bị từ chối ở tầng tạo pipeline.
lay-goi-chung:
  stage: build
  image: alpine:3.20
  needs:
    - job: dong-goi
      project: nhom/lab08-goi-chung
      ref: main
      artifacts: true
  script:
    - test -s goi-chung/thu-vien.tgz || { echo "LỖI: không nhận được hiện vật liên project"; exit 1; }
    - 'echo "nhan $(wc -c < goi-chung/thu-vien.tgz) byte tu project khac"'
```

```yaml
# Cách B — đường CE, dùng API artifact của project khác. Cùng cơ chế, cùng rủi ro tổ chức.
lay-goi-chung-ce:
  stage: build
  image: alpine:3.20
  script:
    - apk add --no-cache curl >/dev/null
    - |
      curl -sf --header "JOB-TOKEN: $CI_JOB_TOKEN" -o goi-chung.zip \
        "$CI_SERVER_URL/api/v4/projects/nhom%2Flab08-goi-chung/jobs/artifacts/main/download?job=dong-goi" \
        || { echo "LỖI: đội kia đã đổi tên job, đổi ref, hoặc bỏ artifact"; exit 1; }
    - 'echo "nhan $(wc -c < goi-chung.zip) byte"'
    # Ghi lại ĐÚNG cái ta đã lấy — nếu không thì không tái lập được pipeline này:
    - 'echo "nguon=nhom/lab08-goi-chung job=dong-goi ref=main lay_luc=$(date -u +%FT%TZ)" > nguon-hien-vat.txt'
  artifacts:
    paths: [goi-chung.zip, nguon-hien-vat.txt]
```

> **Nếu có Ultimate:** `needs:project` để tải artifact từ pipeline của project khác là tính năng bậc trả tiền trên nhiều bản GitLab; bậc CE phản ứng thế nào với khoá này thuộc loại (c) — lab bước 5 gọi `ci/lint` để đo và ghi kèm số phiên bản. Nội dung buổi này **không** phụ thuộc vào nó: cách B chạy trên GitLab CE 17.7, dùng đúng cơ chế (một job kéo hiện vật của project khác bằng `CI_JOB_TOKEN`) và đặt ra đúng câu hỏi tổ chức. Buổi 09 và buổi 44 mới cho ta cách làm việc này an toàn.

**Con số chốt.** **1** cạnh liên project = **1** hợp đồng giữa hai đội, và hợp đồng đó gồm đúng **ba** thứ phải thoả thuận trước: tên job, tên đường dẫn artifact, và `ref` được phép dùng. Thiếu thoả thuận thì cạnh này là một lời hứa một chiều — xem §8 "Khi nào KHÔNG nên dùng".

### Chi phí buổi này thêm vào pipeline

Mỗi kỹ thuật thêm vào pipeline đều tốn. Bảng dưới là hoá đơn của buổi 08, tính bằng giây và phần trăm:

| Thứ thêm vào | Chi phí | Đo ở bước lab |
|---|---|---|
| Chuyển sang `needs` | **0** giây thêm; **−90 s** thời gian chờ; phút runner **không đổi** (540 s) | Bước 1, 2 |
| `parallel: 4` cho job test | Thời gian chờ **120 s → 49 s**; phút runner **120 s → 196 s** (**+63%**) — hai con số này của hai người trả tiền khác nhau | Bước 4 |
| Job `gop-bao-cao` | **+8 s** mỗi pipeline; bắt buộc, không tuỳ chọn (QT 6.4) | Bước 4 |
| Khẳng định `find -newermt` chống cạnh thiếu | **0,2 s** mỗi job, cộng ~3 s `apk add findutils` nếu image thiếu | Bước 3 |
| Slot runner ở đỉnh | Cần **4** slot cùng lúc; thiếu thì mất **65** trong **90** giây lợi ích | Bước 5 |
| Công sức người: lập bản đồ + khai `needs` cho một repo thật | Khoảng **50** phút một lần, xem §8 | — |

---
### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước

Ba việc, tổng **50** phút, làm được hôm nay trên một nhánh riêng mà không cần xin ai.

**Việc 1 — 15 phút, rủi ro bằng 0.** Chạy `do-duong-gang.sh` (mở rộng từ `go-roi.sh` buổi 07) cho **một** pipeline gần nhất và tính **hai** con số: tổng theo stage và đường găng. Chênh lệch là ngân sách tối ưu của ta, và là con số duy nhất đáng mang đi họp: "tôi lấy lại được tối đa bấy nhiêu giây" thay vì "pipeline hơi chậm".

**Việc 2 — 20 phút, rủi ro thấp.** Tìm **job dài nhất mà không job nào cần kết quả của nó** — thường là `scan`, `lint`, `báo cáo` — rồi khai `needs` cho các job phía sau để chúng thôi chờ nó. Đây là thay đổi cho lợi ích lớn nhất trên mỗi dòng YAML: ở ví dụ chuẩn, **8** dòng `needs` mua **90 giây**. Chưa cần chuyển cả pipeline sang DAG trong lần đầu.

**Việc 3 — 15 phút, rủi ro thấp.** Với mỗi job vừa khai `needs`, thêm **một** khẳng định `test -s` cho tệp đầu vào quan trọng nhất. Nền tảng không giữ thứ tự hộ ta nữa (QT 5.2), nên dòng này thay chỗ hàng rào vừa bỏ. Giá: **0,01 giây** mỗi job.

### Cái gì hỏng nếu áp thẳng lên prod

Thêm `needs` **thu hẹp** tập artifact (QT 4.3), nên job đang âm thầm sống nhờ mặc định "tải mọi stage trước" (buổi 05 QT 5.1) sẽ mất tệp ngay lần chạy đầu — và nó có thể mất **im lặng** nếu script không kiểm. Cách áp thử an toàn: làm trên một nhánh riêng, chạy **một** pipeline đầy đủ, và so `find . -type f | wc -l` của **từng** job trước và sau.

Bật `parallel` mà chưa có job gộp làm mọi chỉ số chất lượng tụt xuống `1/N` (QT 6.4), với hai hậu quả đối xứng: gate coverage **chặn oan** cả nhóm, còn gate "0 test thất bại" thì **mở cửa** vì phần chứa test hỏng không nằm trong báo cáo được đọc. Job gộp phải nằm **trong cùng một commit** với `parallel`.

```yaml
# mảnh — cách áp thử một cạnh needs mà KHÔNG chặn ai trong 1 tuần.
kiem-canh-thu:
  stage: test
  image: alpine:3.20
  needs: ["build-be"]
  allow_failure: true              # ồn ào NHƯNG không chặn — ô an toàn của buổi 01 QT 7.1
  script:
    - apk add --no-cache coreutils >/dev/null
    - MOC=$(date -d "$CI_PIPELINE_CREATED_AT" +%s)
    - test -s be/dau-thoi-gian.txt && [ "$(cat be/dau-thoi-gian.txt)" -ge "$MOC" ]
```

Sau một tuần, đếm số lần `kiem-canh-thu` đỏ: đó là số ca "job đọc hiện vật của pipeline khác" đang tồn tại. Khi nó về **0**, bỏ `allow_failure` và chuyển khẳng định vào job thật.

### Đo trước — đo sau

| Chỉ số | Đo bằng | Kỳ vọng |
|---|---|---|
| Tổng theo stage và đường găng, tính bằng giây | `do-duong-gang.sh` trên cùng một ref, trước và sau | Hiệu về gần **0**; ở ví dụ chuẩn: 325 → 235 s |
| Tổng phút runner mỗi pipeline | `map(.duration) \| add` qua API | **Không đổi** khi chỉ thêm `needs` (540 s); **+63%** khi bật `parallel: 4` — biết trước con số |
| Tổng `queued_duration` của pipeline | `map(.queued_duration) \| add` qua API | Không tăng. Tăng nghĩa là ta đang thiếu slot, không thiếu `needs` (QT 7.1) |

### Khi nào KHÔNG nên dùng

**Đừng** chuyển sang DAG khi lãng phí hàng rào dưới khoảng **10%** thời gian pipeline: ta đánh đổi việc nền tảng bảo đảm thứ tự hộ ta lấy vài giây, và QT 5.2 nói cái giá là **một lớp hỏng im lặng mới** — pipeline 200 s thì 20 s tiết kiệm không mua nổi lớp rủi ro đó.

**Đừng** bật `parallel` cho job có phần cố định lớn hơn phần chia được. QT 6.3 cho thấy trần tốc độ là `T / cố_định`, nên job **40 s** với **30 s** khởi tạo có trần **1,33 lần**: chia 4 phần cho ra khoảng 32 s, tiết kiệm 8 giây chờ và trả thêm **88 s** phút runner. Phép thử: đo `T(1)` và `T(2)`, tính cố định bằng `(2 × T(2) − T(1))`, và bỏ ý định nếu nó lớn hơn nửa `T(1)`.

**Đừng** dùng `needs:optional` để "cho pipeline khỏi lỗi". Nó biến **1** lỗi ồn ào có chặn thành **1** cạnh mất im lặng không chặn (QT 5.3). Chỉ dùng khi job nguồn **thật sự** là tuỳ chọn về mặt dữ liệu, và khi đó vẫn phải có khẳng định ở job đích.

**Đừng** dùng `needs:project` khi hai project chưa thoả thuận **ba** thứ: tên job, đường dẫn artifact, và `ref` được phép dùng. Buổi 09 (`trigger`, multi-project) và buổi 44 (pipeline tập trung) mới cho ta cách làm việc đó có phiên bản và có hợp đồng.

**Buổi này KHÔNG giải quyết** ba việc: không giảm **phút runner** (chỉ giảm chờ — và `parallel` làm tăng); không cho cách sinh `needs` **động** theo thứ mục đã đổi trong monorepo (buổi 09 và 22); và không nói được nên mua thêm bao nhiêu slot runner cho hết chờ — đó là bài toán hàng đợi của buổi 13.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy | Vì sao dính | Làm đúng là |
|---|---|---|---|
| 1 | Tính thời gian pipeline bằng cách cộng hết `duration` của mọi job | Cộng là phép dễ nghĩ nhất | Hai công thức khác nhau: **325 s** theo stage so với **235 s** đường găng; 540 s là **phút runner**, không phải thời gian (QT 4.1) |
| 2 | Xoá khối `stages` để "chuyển sang DAG" | Tưởng `stage` và hàng rào là một thứ | `needs` bỏ **hàng rào**, không bỏ `stage`; giữ `stages` để biểu đồ đọc được (QT 4.2) |
| 3 | Khai quá **50** phần tử `needs` cho một job | Sinh `needs` bằng script | Trần **50** ở CE 17.7; đo bằng `ci/lint`, đừng chép con số vào tài liệu nội bộ (QT 4.2) |
| 4 | Thêm `needs` rồi một job khác mất tệp | Job đó sống nhờ mặc định mà không ai biết | `needs` **thu hẹp** tập artifact: **5** tệp xuống **2**; so `find` trước và sau (QT 4.3, buổi 05 QT 5.1) |
| 5 | Khai `needs` theo cảm nhận về thứ tự | Nhanh hơn lập bản đồ | Khai theo **tệp**: 1 mũi tên của bản đồ dữ liệu = **1** phần tử `needs` (QT 5.1) |
| 6 | Bỏ bước đo lại đường găng sau khi khai `needs` | Pipeline xanh nên coi là xong việc | Không đo thì không biết đã sửa hay đã làm chậm; **3** bước, bước 3 là bước không được bỏ (QT 5.1) |
| 7 | Mừng vì pipeline nhanh hơn dự kiến | Nhanh hơn luôn là tin tốt | Nhanh hơn khoảng **35 s** so với đường găng = có thể **thiếu cạnh**; kiểm mốc thời gian hiện vật (QT 5.2) |
| 8 | Dùng `needs:optional` cho tiện, để pipeline khỏi lỗi | Lỗi tạo pipeline nghẽn việc | Nó biến **1** lỗi ồn ào có chặn thành **1** cạnh mất im lặng không chặn (QT 5.3) |
| 9 | `parallel: N` mà `script` không chia việc | Tưởng GitLab tự chia | **4** job làm **4 lần** cùng việc, xanh, tốn 4 lần phút runner; khẳng định phần nhận ít hơn tổng (QT 6.1) |
| 10 | Thêm một giá trị vào một biến của matrix | Tưởng thêm 1 dòng thì thêm 1 job | Số job **nhân** lên: 3 × 2 = **6** thành **8**; trần **200** job một khối (QT 6.2) |
| 11 | Tưởng chia 4 phần thì nhanh 4 lần | Bỏ qua phần cố định | **2,45** lần, trần là `T / cố_định` = **4,8** lần; tính cố định bằng `(N·T(N) − T(1))/(N − 1)` (QT 6.3) |
| 12 | Bật `parallel` mà chưa có job gộp báo cáo | Job nào cũng xanh, số vẫn hiện ra | Coverage còn **1/N**: 82% thành 21%; **1** khẳng định đếm tệp chặn được (QT 6.4) |
| 13 | Chuyển sang DAG mà `concurrent` vẫn thấp | Tưởng song song là chuyện của YAML | Cần **4** slot ở đỉnh; thiếu thì 235 s về lại khoảng **300 s** — đọc `queued_duration` (QT 7.1) |
| 14 | `needs:project` khi chưa nói gì với đội kia | Một dòng YAML là chạy ngay | **1** cạnh liên project = **1** hợp đồng gồm **3** khoản: tên job, đường dẫn artifact, `ref` (QT 7.2) |

---

### 1.7. Tóm tắt

```mermaid
graph TD
    LD["LUẬN ĐỀ: bỏ hàng rào stage đổi công thức<br/>từ TỔNG CỦA CÁC MAX sang MAX CỦA CÁC TỔNG<br/>325 s → 235 s, lãng phí 90 s = 28%<br/>phút runner 540 s KHÔNG đổi"]

    LD --> A["§4 HAI CÔNG THỨC<br/>QT 4.1 hiệu hai số = lãng phí hàng rào<br/>QT 4.2 needs bỏ hàng rào, KHÔNG bỏ stage — trần 50, PHẢI ĐO<br/>QT 4.3 needs thu hẹp artifact: 5 tệp → 2"]
    LD --> B["§5 DỰNG DAG VÀ CẠNH BỊ QUÊN<br/>QT 5.1 ba bước, 1 mũi tên = 1 needs<br/>QT 5.2 thiếu cạnh: nhanh hơn 35 s VÀ SAI<br/>QT 5.3 optional: lỗi ồn ào thành cạnh mất im lặng"]
    LD --> C["§6 PARALLEL VÀ MATRIX<br/>QT 6.1 N job giống nhau, script phải tự chia<br/>QT 6.2 tích Descartes: 6 → 8 job<br/>QT 6.3 120 s = 25 cố định + 95 biến → 2,45 lần<br/>QT 6.4 thiếu job gộp: coverage còn 1/N"]

    A --> D["§7 CÁI GIÁ<br/>QT 7.1 chờ đổi thành slot: cần 4 slot, thiếu thì về 300 s<br/>QT 7.2 cạnh liên project = hợp đồng 3 khoản giữa hai đội"]
    B --> D
    C --> D

    D --> KQ["Ô NGUY HIỂM NHẤT — lần thứ 8:<br/>im lặng + không chặn<br/>5 trong 6 chế độ hỏng của buổi nằm ở đây<br/>và tín hiệu duy nhất là NHANH HƠN DỰ KIẾN"]
    KQ --> VT["§8 ĐƯA VÀO VIỆC THẬT<br/>đo hai con số → bỏ chờ job không ai cần<br/>→ thêm khẳng định 0,01 s thay chỗ hàng rào<br/>gộp báo cáo cùng commit với parallel"]

    A -.dùng lại.-> B1["buổi 09 · 15 · 22 · 25"]
    B -.dùng lại.-> B2["buổi 09 · 22 · 27 · 34"]
    C -.dùng lại.-> B3["buổi 14 · 16–21 · 30–35"]
    D -.dùng lại.-> B4["buổi 13 · 14 · 44 · 46"]
```

**Năm điều phải nhớ sau buổi học:**

1. **Tuần tự là tổng của các max, DAG là max của các tổng.** Ở ví dụ chuẩn: **325 s** so với **235 s**, lãng phí **90 s = 28%**. Không đo hai con số này thì mọi tối ưu sau đó là đoán.
2. **`needs` giảm chờ, không giảm phút runner.** **540 s** ở cả hai ca. `parallel` thì ngược: giảm chờ và **tăng** phút runner **+63%**. Hai đại lượng, hai người trả tiền.
3. **Cái giá của DAG là một lớp hỏng im lặng.** Thiếu **1** cạnh cho ra pipeline **nhanh hơn khoảng 35 s và sai**; tín hiệu duy nhất là *nhanh hơn dự kiến*. Từ nay đó là triệu chứng phải điều tra.
4. **Chia N phần không nhanh gấp N.** 120 s = **25 s cố định + 95 s biến** cho ra **2,45** lần ở N = 4, trần **4,8** lần. Và N phần sinh N báo cáo: thiếu job gộp thì mọi chỉ số còn **1/N**.
5. **`needs` không sinh ra máy.** Cần **4** slot ở đỉnh; với `concurrent = 2` thì 235 s về lại khoảng **300 s**. Trước khi kết luận "`needs` vô dụng", cộng `queued_duration` lại đã.

---

### 1.8. Câu hỏi tự kiểm tra

1. Viết hai công thức tính thời gian pipeline bằng lời. Hiệu của hai con số gọi là gì, và nó phụ thuộc runner mạnh hay yếu không?
2. Cho bảng 8 job của §4. Tính tổng theo stage và đường găng, chỉ ra job nào **không** nằm trên đường găng nhưng làm chậm pipeline.
3. Rút `scan` từ 150 s xuống 100 s sau khi đã khai `needs` thì tiết kiệm được mấy giây? Vì sao?
4. `needs` có xoá `stage` không? Kể **hai** thứ `stage` vẫn làm sau khi đã có `needs`.
5. Ngoài thứ tự chạy, `needs` đổi thêm cái gì? Cho con số của ví dụ chuẩn, và nêu cú pháp để **chỉ** chờ mà không lấy tệp.
6. Kể **ba** bước dựng DAG. Bỏ bước nào thì nguy hiểm nhất, và bỏ bước nào thì chỉ vô ích?
7. Pipeline nhanh hơn dự kiến **35 s**. Đây là tin tốt hay tin xấu? Nêu cơ chế và **hai** lệnh chứng minh.
8. `needs:optional: true` đổi ô nào của bảng hai thuộc tính hỏng, theo chiều nào? Phép so nào phát hiện được ca đó — so thời gian hay so cái gì?
9. `parallel: 4` mà `script` không chia việc thì xảy ra gì? Job xanh hay đỏ, và tốn thêm bao nhiêu phút runner?
10. Matrix `3 × 2`, thêm một phiên bản thì thành mấy job? Viết phép tính.
11. Job test 120 s, `parallel: 4` cho 49 s. Tính phần cố định, tốc độ thật, trần tốc độ, và phần trăm phút runner tăng thêm.
12. Coverage tụt từ 82% xuống 21% ngay lần commit bật `parallel: 4`. Nguyên nhân là gì, và **một** dòng nào chặn được ca đó?
13. Chuyển sang DAG mà thời gian pipeline không đổi. Nêu **hai** con số phải đọc để phân biệt "cấu hình sai" với "thiếu tài nguyên", và kết luận đúng trong mỗi ca.

### Đáp án

1. Tuần tự: **tổng theo stage của job chậm nhất mỗi stage**. DAG: **đường dài nhất theo quan hệ dữ liệu**. Hiệu là **lãng phí hàng rào**, một thuộc tính của **cấu trúc đồ thị** nên độc lập với sức mạnh runner: runner mạnh hơn làm cả hai con số nhỏ đi mà tỉ lệ lãng phí gần như không đổi (QT 4.1).
2. Tổng theo stage = 150 + 120 + 30 + 25 = **325 s**. Đường găng = `build-be` 90 + `test-e2e` 120 + `deploy` 25 = **235 s**. `scan` 150 s không có job nào phía sau nhưng làm chậm **90 s** vì hàng rào stage; `lint` 20 s cũng ngoài đường găng nhưng vô hại vì ngắn (QT 4.1).
3. **0** giây. `scan` không nằm trên đường găng nên thời lượng của nó không cộng vào 235 s — chỉ khi nó dài hơn 235 s thì mới thành nút chặn. Đây là lý do phải biết đường găng trước khi tối ưu job nào (QT 4.1, mô hình tư duy 1).
4. Không xoá. `stage` vẫn (a) quyết định cách pipeline được **vẽ** thành cột, và (b) vẫn giới hạn job nào `needs` được job nào — ràng buộc này phụ thuộc phiên bản nên **phải đo** bằng `ci/lint` (QT 4.2, lần thứ 8 của quy tắc "phải đo").
5. Nó **thu hẹp** tập artifact tải về đúng danh sách `needs`, thay cho mặc định "mọi job ở mọi stage trước" của buổi 05 QT 5.1. Ví dụ chuẩn: `deploy` từ **5** tệp xuống **2** tệp. Cú pháp chỉ chờ: `needs: [{job: test-unit, artifacts: false}]` — cạnh cổng (QT 4.3).
6. (1) Lập bản đồ **dữ liệu**; (2) mỗi mũi tên thành **một** phần tử `needs`; (3) **đo lại** đường găng. Bỏ bước 1 nguy hiểm nhất vì nó sinh ra cạnh thiếu, tức QT 5.2. Bỏ bước 3 thì không hỏng ngay nhưng vô ích: không biết đã sửa được bao nhiêu, cũng không biết mình vừa thêm cạnh thừa làm chậm đi (QT 5.1).
7. **Tin xấu** cho tới khi chứng minh được ngược lại. Cơ chế: thiếu một cạnh làm job khởi động sớm (ở ví dụ chuẩn: sớm **30 s**) và thôi phải tải artifact của job bị bỏ cạnh (thêm khoảng **5 s**), tổng khoảng **35 s** — job vẫn xanh vì nó đọc bản cũ trong cache, tệp có trong git, hoặc thư mục rỗng. Hai lệnh: so hiện vật với `t0` bằng `[ "$(cat be/dau-thoi-gian.txt)" -ge "$MOC" ]` với `MOC=$(date -d "$CI_PIPELINE_CREATED_AT" +%s)`, và `find dist/ -type f -newermt "$CI_PIPELINE_CREATED_AT"` (QT 5.2).
8. Từ **ồn ào + có chặn** (lỗi tạo pipeline khi job nguồn vắng mặt, buổi 04 QT 7.3) sang **im lặng + không chặn** (cạnh biến mất, nhánh sau chạy sớm). Phép so đúng là so **số job** của pipeline giữa hai nhánh, không so thời gian — vì thời gian ngắn hơn trông như tin tốt (QT 5.3).
9. N job làm **cùng một việc N lần**: 4 job cùng thời lượng, cùng số test. Job **xanh**, ô im lặng + không chặn. Phút runner từ 120 s lên khoảng **480 s** (4 × 120) mà thời gian pipeline không giảm một giây. Khẳng định chặn: mỗi phần phải nhận **ít hơn** tổng số tệp (QT 6.1).
10. `4 × 2 = 8` job, tức **+2** chứ không phải +1: thêm một giá trị vào một biến thì thêm đúng tích của các biến còn lại. Trần một khối matrix là **200** job ở CE 17.7 (QT 6.2).
11. Cố định = `(4 × 49 − 120) / 3` = **25,3 s**, làm tròn **25 s**; biến = **95 s**. Tốc độ thật `120 / 49` = **2,45** lần. Trần `120 / 25` = **4,8** lần. Phút runner `4 × 49 = 196 s` so với 120 s, tức **+63%** (QT 6.3).
12. Thiếu job gộp báo cáo: 4 job sinh 4 báo cáo rời, thứ đọc báo cáo chỉ thấy **1/4** sự thật — tỉ số 21/82 chính là dấu vân tay. Dòng chặn: `[ "$(ls bao-cao-*.json | wc -l)" -eq "$SO_PHAN" ] || exit 1` trong job gộp; job gộp tốn **+8 s** và là chi phí bắt buộc của `parallel` (QT 6.4).
13. Đọc **tổng `duration`** và **tổng `queued_duration`** của pipeline. Nếu tổng `duration` giảm mà `queued_duration` tăng đúng bằng phần đó thì cấu hình đúng, **thiếu slot** — trần là `min(concurrent, limit)` của buổi 02 QT 6.1, ví dụ chuẩn cần **4** slot ở đỉnh. Nếu `queued_duration` gần **0** mà thời gian không đổi thì cạnh `needs` khai chưa đúng, hoặc job dài nhất chính là đường găng và không có gì để lấy lại (QT 7.1).

---

## §12. Tài liệu tham khảo

| Nguồn | Loại | Phiên bản |
|---|---|---|
| GitLab Docs — *CI/CD YAML syntax reference*: `needs`, `needs:artifacts`, `needs:optional`, `needs:project`, `needs:pipeline` | (a) tài liệu chính thức | CE 17.7 |
| GitLab Docs — *Needs keyword / Directed Acyclic Graph pipelines* | (a) | CE 17.7 |
| GitLab Docs — *Parallelize large jobs*: `parallel`, `parallel:matrix`, `CI_NODE_INDEX`, `CI_NODE_TOTAL` | (a) | CE 17.7 |
| GitLab Docs — *Stages*, `.pre`/`.post`, cách pipeline được vẽ | (a) | CE 17.7 |
| GitLab API — `/projects/:id/pipelines/:pipeline_id/jobs` (`duration`, `queued_duration`, `stage`), `/jobs/:id/trace`, `POST /projects/:id/ci/lint?include_jobs=true`, `/projects/:id/jobs/artifacts/:ref/download` | (a) | v4 |
| GitLab Runner — `concurrent`, `limit` trong `config.toml` | (a) | Runner 17.7 |
| Trần **50** phần tử `needs`; `parallel` **2–200**; matrix **200** job | (c) **phải đo** | Lab bước 2 và 4, bằng `ci/lint` |
| Ràng buộc "`needs` chỉ trỏ job cùng stage hoặc stage trước" | (c) **phải đo** | Lab bước 2 — đã đổi trong dòng 14.x–17.x |
| `needs:project` có được bậc CE chấp nhận hay không | (c) **phải đo** | Lab bước 5; đường B là API artifact với `CI_JOB_TOKEN` |
| Bốn mức `parallel` 1 · 2 · 4 · 8 và phần cố định của **repo mình** | (c) **phải đo** | Lab bước 4 — con số 25/95 là của ví dụ chuẩn |
| Thời gian pipeline khi `concurrent = 2` | (c) **phải đo** | Lab bước 5, khoảng **300 s** |
| Kinh nghiệm thực tế: job dài nằm ngoài quan hệ dữ liệu thường là `scan`, `lint`, `báo cáo` | (c) kinh nghiệm thực tế | — |

> **Về việc trích dẫn.** Sáu dòng đầu là chỗ nên tra tài liệu của **đúng phiên bản đang chạy**. Năm dòng loại (c) là chỗ **không được** tra: cả ba con số trần, ràng buộc theo stage, hành vi của `needs:project` ở bậc CE, và tỉ lệ cố định/biến của một job test đều thay đổi theo phiên bản hoặc theo repo. Mọi hiện vật của buổi này (`bang-duong-gang.tsv`, `dag.mmd`) phải ghi kèm số phiên bản GitLab và runner đã đo — đây là **lần thứ 8** khoá này yêu cầu điều đó.

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10' |
| §1 | Sau buổi này học viên làm được gì | 1' |
| §2 | Cần biết trước | 1' |
| §3 | Thuật ngữ và mô hình tư duy | 8' |
| §4 | Hai công thức tính thời gian pipeline | 10' |
| §5 | Dựng DAG từ bản đồ phụ thuộc — và cạnh bị quên | 9' |
| §6 | `parallel` và `parallel:matrix` | 10' |
| §7 | Cái giá: slot runner, phút runner, và phụ thuộc liên project | 5' |
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

> Kiểm chứng trên **GitLab CE 17.7 · GitLab Runner 17.7 · executor `docker` · `concurrent = 8`**.
> Mọi checkpoint gọi **API GitLab** rồi khẳng định một trường cụ thể. Không có checkpoint nào là "mở biểu đồ pipeline thấy đẹp" — lý do ở §L2 quyết định 2.
> Buổi này **nạp lại** hiện vật của ba buổi trước, không viết lại: `cong-cu.sh` buổi 05 (11 hàm), `go-roi.sh` và `cong-cu07.sh` buổi 07 (6 hàm đọc), và bảng `ban-do-phu-thuoc.md` buổi 03 — bảng đó là **đầu vào trực tiếp** của bước 1.
> Ba con số của buổi là **325 s** (tổng theo stage) · **235 s** (đường găng sau `needs`) · **90 s** (phần cắt được, 27,7%). Học viên **đo ra** cả ba, không chép. Con số thứ tư quan trọng bằng cả ba: **540 s** phút runner, **giống nhau ở cả hai ca**.
> Buổi này đụng **hạ tầng dùng chung** ở đúng một chỗ **tuỳ chọn**: hạ `concurrent` xuống **2** ở bước 5 để đo trần slot. Sao lưu ở §L1 dòng 13, khôi phục bắt buộc ở §L8.1, CHECKPOINT 12 kiểm bằng `diff`. Đường B ở §L9 dòng 20 cho lớp không có quyền.

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| # | Mục tiêu | Tiêu chí hoàn thành (kiểm chứng được bằng lệnh) |
|---|---|---|
| TH1 | Viết `do-duong-gang.sh` — đọc mọi job của một pipeline qua API, in **hai** công thức cạnh nhau | `bash -n do-duong-gang.sh` không lỗi; chạy cho một pipeline thật in đủ `TONG_THEO_STAGE`, `DUONG_GANG_LY_THUYET`, `LANG_PHI_HANG_RAO`, `PHUT_RUNNER`, `SLOT_DINH` |
| TH2 | **Đo QT 4.1 trên ca tuần tự** — tổng theo stage của pipeline mẫu | `bang-duong-gang.tsv` dòng `tuan-tu` có `tong_theo_stage` trong **318–335 s** và `phut_runner` trong **530–560 s** — CHECKPOINT 1 |
| TH3 | Lập bản đồ dữ liệu theo đúng định dạng `ban-do-phu-thuoc.md` buổi 03, rồi biến thành `canh.tsv` | `ban-do-du-lieu.md` có **8** dòng job; `canh.tsv` có **8** cạnh; số mũi tên bằng số dòng — CHECKPOINT 2 |
| TH4 | **Đo QT 5.1 và QT 4.1 trên ca DAG** — đường găng và phần cắt được | Dòng `dag-4-stage`: `duong_gang` trong **228–248 s**, `lang_phi` **≥ 80 s**, `phut_runner` **không đổi ±5%** so với dòng `tuan-tu` — CHECKPOINT 3 |
| TH5 | **Đo QT 4.2** — `stage` còn tồn tại nhưng thôi quyết định thời gian | Dòng `dag-1-stage` có `duong_gang` lệch dòng `dag-4-stage` **≤ 15 s**; kết quả thử `needs` trỏ job ở stage **sau** được ghi vào `bang-gioi-han.tsv` — CHECKPOINT 4 |
| TH6 | **Đo QT 4.3** — `needs` thu hẹp tập artifact, và **cạnh cổng** thu hẹp thêm một lần nữa | `SO_TEP_NHAN_DUOC` của `deploy` đổi **15 → 5 → 2** (mặc định → `needs` trần trụi → cạnh cổng có `artifacts: false`); của `package` **14 → 7** — CHECKPOINT 5 |
| TH7 | **Tái hiện QT 5.2** — bỏ đúng cạnh `test-e2e ← build-be`: pipeline **205 s** thay vì **235 s** và **xanh mà sai** | Vòng thiếu cạnh: `test-e2e` `success` mà `bao-cao/e2e.json` ghi `cau_hinh=0.0.0-mac-dinh`; hiệu 35 s tách được thành **30 s** khởi động sớm + **~5 s** thôi tải artifact — CHECKPOINT 6 |
| TH8 | Chặn lại bằng hai khẳng định đo được, và đo QT 5.3 `needs:optional` trên hai nhánh | Vòng đối chứng: `test-e2e` **failed** với `script_failure`; `bang-thieu-cang.tsv` có **3** dòng; `bang-optional.tsv` có **3** dòng và **2** giá trị đường găng khác nhau — CHECKPOINT 7 |
| TH9 | Viết `chia-viec.sh` và **đo QT 6.1** — `parallel` không chia việc hộ ta | Nhóm `test-khong-chia` có **4** job cùng `so_test = 95` và `duration` lệch nhau **≤ 8 s**; nhóm `test-p4` có 4 job với `so_test` **24/24/24/23** — CHECKPOINT 8 |
| TH10 | **Đo QT 6.3** — bảng bốn điểm đo `parallel` 1/2/4/8, tự tính phần cố định | `bang-parallel.tsv` có **4** dòng đơn điệu giảm; tốc độ ở N=4 trong **2,0–2,9** lần; phần cố định tính ngược trong **18–32 s** — CHECKPOINT 9 |
| TH11 | **Đo QT 6.4** — job gộp, và ca đối chứng thiếu phần **phải đỏ** | `gop-bao-cao` xanh với `tong_test = 95`; `gop-doi-chung` **failed`; con số "1/N sự thật" ghi được bằng số — CHECKPOINT 10 |
| TH12 | **Đo QT 6.2, QT 7.1, QT 7.2** — matrix nhân lên, trần slot, hợp đồng liên project **trên GitLab CE** | Matrix cho **6** rồi **8** job; `SLOT_DINH` của DAG bằng **4**; job lấy artifact project khác qua API đỏ với **404** khi đội kia đổi tên job — CHECKPOINT 11 |
| TH13 | Nộp hiện vật và trả hạ tầng về nguyên trạng | `kiem-hien-vat.sh` in `ĐẠT`; nếu đã hạ `concurrent` thì `diff` với bản sao lưu **rỗng** — CHECKPOINT 12 |

**Sản phẩm cuối buổi:** `gitlab-portfolio/08-needs-dag-parallel-matrix/` gồm **`bang-duong-gang.tsv`** (6 dòng ca đo — hiện vật chính), **`do-duong-gang.sh`** (công cụ buổi 14 dùng lại), `dag.mmd`, `ban-do-du-lieu.md`, `canh.tsv`, `chia-viec.sh`, `bang-parallel.tsv`, `bang-thieu-cang.tsv`, `bang-optional.tsv`, `bang-gioi-han.tsv`, `bang-artifact-08.tsv`, `hop-dong-lien-project.md`, `.gitlab-ci.yml` bản cuối của nhánh `dag`, `checkpoint.log`.

Hai hiện vật **cốt lõi** — thiếu một trong hai là chưa nộp bài — là `bang-duong-gang.tsv` và `do-duong-gang.sh`. Ai đi **đường B** ở §L9 (không sửa được `concurrent`, không có project thứ hai) vẫn có đủ cả hai, với dòng `dag-concurrent-2` ghi `-` và một dòng ghi rõ lý do.

---

## L1. Điều kiện tiên quyết về môi trường

| # | Kiểm tra | Lệnh | Kết quả kỳ vọng |
|---|---|---|---|
| 1 | Đã nạp biến môi trường lab | `echo "$GITLAB" "$GITLAB_TOKEN" \| wc -w` | `2` |
| 2 | GitLab sẵn sàng | `curl -sf -o /dev/null -w '%{http_code}\n' "$GITLAB/-/readiness"` | `200` |
| 3 | Token gọi được API | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/user" \| jq -r .username` | tên đăng nhập, khác rỗng |
| 4 | **`jq` có `strptime`/`mktime`** — `do-duong-gang.sh` đổi mốc ISO sang epoch bằng hai hàm này | `echo '"2026-01-01T00:00:00"' \| jq 'strptime("%Y-%m-%dT%H:%M:%S")\|mktime'` | `1767225600` — lỗi thì §L9 dòng 1 |
| 5 | **Còn `cong-cu.sh` buổi 05 — 11 hàm.** Buổi này nạp lại, không viết lại | `grep -cE '^(day\|day_nhanh\|cho_pipeline\|job_bang\|job_id\|job_tt\|job_log\|job_log_sach\|art_http\|art_tep\|art_zip)\(\)' ~/lab05/cong-cu.sh` | `11` — thiếu thì §L9 dòng 2 |
| 6 | **Còn `cong-cu07.sh` buổi 07 — 6 hàm đọc.** Bước 3 và 5 cần `tao_pipe` để đọc lỗi khi pipeline **không** được tạo | `grep -cE '^(job_json\|job_bang_rong\|tao_pipe\|runner_han\|trace_chuan\|so_lan_chay)\(\)' ~/lab07/cong-cu07.sh` | `6` |
| 7 | **Còn `go-roi.sh` buổi 07.** `do-duong-gang.sh` gọi nó để lấy **giây pha `step_script`** của từng job | `bash -n ~/lab07/go-roi.sh && grep -c 'step_script' ~/lab07/go-roi.sh` | `≥ 1` — thiếu thì §L9 dòng 3 |
| 8 | **Còn `ban-do-phu-thuoc.md` buổi 03** — đầu vào trực tiếp của bước 1 | `grep -c '^\|' ~/gitlab-portfolio/03-cu-phap-yaml-va-stage/ban-do-phu-thuoc.md` | `≥ 5` (một dòng tiêu đề + một dòng phân cách + ≥ 3 dòng job) |
| 9 | Runner online và nhận job **không** tag | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners?status=online" \| jq -r '.[] \| "\(.id)\t\(.description)"'` | ≥ 1 dòng; lấy `id` làm `$RID` |
| 10 | **`concurrent` hiện tại ≥ 8** — dưới 8 thì ví dụ chuẩn không bao giờ đạt 235 s | `docker exec lab-runner sh -c 'grep -E "^concurrent" /etc/gitlab-runner/config.toml'` | `concurrent = 8` hoặc lớn hơn; nhỏ hơn thì §L9 dòng 19 |
| 11 | Chưa có project lab 08 | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects?search=lab08-" \| jq length` | `0` — khác `0` thì §L9 dòng 21 |
| 12 | Có `jq`, `curl`, `git`, `awk`, `sed`, `date`, `column`, `mktemp` | `command -v jq curl git awk sed date column mktemp \| wc -l` | `8` |
| 13 | **Tuỳ chọn — sao lưu `config.toml`** trước phần hạ `concurrent` của bước 5 | `docker exec lab-runner sh -c 'cp /etc/gitlab-runner/config.toml /etc/gitlab-runner/config.toml.buoi08.bak && ls -la /etc/gitlab-runner/config.toml*'` | thấy cả hai tệp; không làm được thì bỏ phần tuỳ chọn, đi đường B §L9 dòng 20 |
| 14 | Đĩa trống — bài lab sinh khoảng **14 MB** artifact và **6 MB** log | `df -BG --output=avail "$HOME" \| tail -1` | `> 5G` |
| 15 | Bộ nhớ trống — đỉnh của bước 4 có **8** container cùng lúc | `free -g \| awk '/Mem:/{print $7}'` | `≥ 4` |
| 16 | Ghi lại phiên bản để dán vào mọi hiện vật | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/version" \| jq -r '.version'; docker exec lab-runner gitlab-runner --version \| head -2` | hai chuỗi phiên bản |

**Cảnh báo về mức độ tác động.** Bài lab tạo **hai** project — `lab08-dag` (bảy nhánh: `tuan-tu`, `dag`, `dag-mot-stage`, `thieu-cang`, `do-parallel`, `do-matrix`, `do-lien-project`) và `lab08-goi-chung` (một nhánh `main`). Hai thứ **tồn tại sau khi buổi học kết thúc** nếu không dọn:

1. **`concurrent` của runner bị hạ xuống 2** ở phần **tuỳ chọn** của bước 5. Đây là hạ tầng dùng chung của cả lớp (buổi 02 QT 4.3): trong lúc nó bằng 2, **mọi** job của **mọi** project đứng xếp hàng theo hai. Sao lưu ở dòng 13, khôi phục **bắt buộc** ở §L8.1, và CHECKPOINT 12 đòi `diff` với bản sao lưu **rỗng**. Trên lớp đông người dùng chung một runner, **chỉ giảng viên** hạ `concurrent`, một lần, trước lớp; học viên đọc số. Bỏ phần này vẫn đo được trần slot bằng `queued_duration` của pipeline bước 4 — đó là đường B ở §L9 dòng 20, và nó **không** đụng hạ tầng dùng chung.
2. **Một pipeline đỏ có chủ ý** trên nhánh `do-parallel` (job `gop-doi-chung`) và **một pipeline đỏ có chủ ý** trên nhánh `thieu-cang` (job `dung-goi` vòng 2). Cả hai là **đáp án đúng**, không phải sự cố. §L8.3 xoá project là dọn xong.

**Chi phí phút runner của buổi — con số phải biết trước khi bắt đầu.** Bảng dưới là ngân sách runner thật, đo trên máy tham chiếu:

| Bước | Phút runner (giây) | Thời gian chờ thật (wall, giây) | Vì sao tốn |
|---|---|---|---|
| Bước 1 — pipeline tuần tự | **540** | ~355 | 8 job, tổng `sleep` 540 s |
| Bước 2 — DAG 4 stage + DAG 1 stage + `deploy` cạnh cổng | **~1.140** | ~255 + ~255 | **Cùng 540 s runner mỗi ca** — đây là bằng chứng chính của buổi |
| Bước 3 — thiếu cạnh · đối chứng đỏ · vá cạnh · `optional` × 2 | **~1.620** | ~480 | Ba lần chạy pipeline 8 job; vòng 2 và vòng 3 đẩy **cùng lúc** để tiết kiệm 4 phút |
| Bước 4 — `parallel` 1/2/4/8 + không chia việc + hai job gộp | **1.254** | ~300 | 21 job trong một pipeline, `concurrent = 8` cho 3 đợt |
| Bước 5 — matrix 6 rồi 8 job, liên project qua API | ~**220** | ~140 | Job 8 giây |
| **Tổng** | **~4.774 s ≈ 80 phút runner** | **~1.530 s ≈ 26 phút chờ** | Tỉ số **3,1 lần** là do song song |

Đọc bảng này **trước** khi chạy: 80 phút runner cho 26 phút chờ là toàn bộ chủ đề của buổi gói trong một tỉ số. Trên máy 8 vCPU, tám container `alpine` chạy `sleep` chiếm khoảng 0,3 vCPU tổng — nút cổ chai của lab **không** phải CPU, nên buổi 02 QT 6.2 chưa can thiệp ở đây; bước 5 sẽ tạo ra ca nút cổ chai bằng cách hạ `concurrent`.

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    CU["Hiện vật NẠP LẠI<br/>cong-cu.sh buổi 05 — 11 hàm<br/>cong-cu07.sh buổi 07 — 6 hàm<br/>go-roi.sh buổi 07 — giây từng pha<br/>ban-do-phu-thuoc.md buổi 03"]
    CU --> DDG["do-duong-gang.sh<br/>MỚI của buổi 08<br/>đọc API + canh.tsv<br/>in HAI công thức"]

    HV["Học viên"] -->|"git push 7 nhánh"| PRJ["Project lab08-dag"]
    HV -->|"git push main"| PRJ2["Project lab08-goi-chung<br/>job dong-goi-chung"]
    PRJ -->|"giao job"| RN["Runner lab-runner<br/>executor docker<br/>concurrent = 8 → 8 slot"]
    PRJ2 --> RN
    RN --> API["API GitLab v4<br/>jobs · trace · artifacts<br/>ci/lint · pipelines"]
    API --> DDG

    DDG --> B1["Bước 1 — tuần tự<br/>TỔNG THEO STAGE = 325 s<br/>phút runner 540 s"]
    DDG --> B2["Bước 2 — DAG<br/>ĐƯỜNG GĂNG = 235 s<br/>phút runner VẪN 540 s<br/>artifact 15 → 5 → 2 tệp"]
    DDG --> B3["Bước 3 — THIẾU CẠNH<br/>205 s thay vì 235 s<br/>XANH MÀ SAI<br/>30 s + 5 s"]
    DDG --> B4["Bước 4 — parallel 1/2/4/8<br/>120 · 73 · 49 · 37 s<br/>phút runner +63%"]
    DDG --> B5["Bước 5 — matrix 6 → 8 job<br/>SLOT ĐỈNH = 4<br/>hợp đồng liên project"]

    B1 --> BDG["bang-duong-gang.tsv<br/>6 dòng ca đo<br/>HIỆN VẬT CHÍNH"]
    B2 --> BDG
    B3 --> BDG
    B5 --> BDG
    B2 --> MMD["dag.mmd<br/>8 job · 8 cạnh<br/>đường găng in đậm"]
    B4 --> BPR["bang-parallel.tsv<br/>4 điểm đo<br/>phần cố định tính ngược"]
```

**Năm quyết định thiết kế:**

1. **Job trong pipeline mẫu dùng `sleep` với thời lượng cố định, không dùng công việc thật.** Điều bài lab đo là quan hệ giữa **cấu trúc đồ thị** và **thời gian**, nên thời lượng job phải là hằng số ta đặt được. Một `npm test` thật dao động 20–40% giữa hai lần chạy trên cùng một máy; với dao động đó, hiệu **90 s** giữa 325 và 235 nằm lẫn trong nhiễu và cả bài học biến thành "có vẻ nhanh hơn". Cái giá của quyết định này: `sleep` không tiêu CPU, nên lab **không** thấy hiệu ứng tranh chấp CPU của buổi 02 QT 6.2 — bước 5 bù lại bằng cách hạ `concurrent` để tạo ra một trần tài nguyên thật.

2. **Đo đường găng bằng script, không bằng cách nhìn biểu đồ pipeline.** Biểu đồ DAG của GitLab cho **cảm nhận** về hình dạng đồ thị; nó không cho hai con số so được với nhau, và nó không cộng được `duration`. `do-duong-gang.sh` in cả `TONG_THEO_STAGE` và `DUONG_GANG_LY_THUYET` trong một lần chạy, nên hiệu của chúng là một số nguyên chứ không phải một ấn tượng. Thêm nữa, script tính đường găng **lý thuyết** từ `canh.tsv` **trước khi** ta chạy pipeline DAG — nhờ đó học viên **dự đoán 235 s rồi mới đo**, và sai lệch giữa dự đoán và số đo trở thành một dữ kiện chẩn đoán (thiếu slot, hay thiếu cạnh). Đây là hiện vật buổi 14 dùng lại nguyên vẹn.

3. **Ca thiếu cạnh được đặt riêng ở bước 3 — trên CHÍNH pipeline mẫu, bỏ đúng MỘT cạnh — và có bước tái lập ngược.** Học viên phải thấy pipeline **nhanh hơn** rồi mới thấy nó **sai**. Nếu gộp ca này vào bước 2 thì tín hiệu "nhanh hơn dự kiến" bị chìm trong 90 s lãng phí vừa cắt được — đúng lúc cả lớp đang ăn mừng vì con số giảm. Cạnh bị bỏ là `test-e2e ← build-be`, và nó được chọn vì hiệu **tách được thành hai phần đo riêng**: đường găng rơi từ **235 s** xuống **205 s** — **30 s** vì `test-e2e` thôi chờ `build-be` (90 s) mà chỉ còn chờ `build-fe` (60 s) — cộng khoảng **5 s** nữa ở `wall` vì `test-e2e` thôi phải tải artifact của `build-be`. Tổng khoảng **35 s**, và học viên phải chỉ ra được đâu là 30 và đâu là 5; một con số gộp không dạy được gì vì nó không phân biệt được "chạy sớm hơn" với "làm ít việc hơn".

4. **`parallel` đo ở bốn mức 1/2/4/8 chứ không chỉ bật/tắt, và cả bốn mức nằm trong MỘT pipeline.** Với bốn điểm đo, học viên tự thấy đường cong bão hoà và tự tính phần cố định bằng `C = (N·T(N) − T(1)) / (N − 1)` — một công thức hai điểm, ra ngay một con số vận hành. Đặt cả bốn mức trong một pipeline có lý do đo lường: `duration` của một job **không** tính thời gian nằm trong hàng đợi (`queued_duration` là trường riêng), nên bốn nhóm chen nhau tranh 8 slot vẫn cho bốn con số so được với nhau — và cùng lúc sinh ra dữ liệu `queued_duration` mà bước 5 cần.

5. **Job gộp báo cáo được viết trong CÙNG bước với `parallel`, không tách thành bài tập mở rộng.** QT 6.4 nói thiếu nó là hỏng im lặng: coverage tụt còn 1/N mà con số vẫn hiện ra. Đưa job gộp vào bài tập tự chọn là dạy sai thứ tự ưu tiên — nó không phải phần nâng cao của `parallel`, nó là **một nửa** của `parallel`. Bước 4 vì thế có hai job gộp: một job đúng, và một job đối chứng khai thiếu đầu vào để cho thấy khẳng định đếm tệp thật sự chặn được.

**Ca đối chứng PHẢI THẤT BẠI — báo trước cho lớp.** Bốn kết quả dưới đây là **đáp án đúng**, không phải sự cố của bài lab:

| Ở đâu | Cái gì | Vì sao đó là đáp án đúng |
|---|---|---|
| Bước 3 vòng 1 | Job `test-e2e` **XANH** trong khi `bao-cao/e2e.json` ghi `cau_hinh=0.0.0-mac-dinh`; đường găng chỉ **205 s** | Đây là hỏng im lặng số 1 của buổi: thiếu cạnh cho ra pipeline **nhanh hơn và sai** |
| Bước 3 vòng 2 | Job `test-e2e` **ĐỎ** với `failure_reason = script_failure` | Hai khẳng định vừa thêm đã đổi ô bảng từ *im lặng · không chặn* sang *ồn ào · có chặn* |
| Bước 3 phần `optional` | Pipeline trên nhánh `nhanh-phu` **KHÔNG ĐƯỢC TẠO** khi bỏ `optional: true` | Đây là lỗi ồn ào mà `optional` đem đi đổi lấy một cạnh mất im lặng (QT 5.3) |
| Bước 4 | Job `gop-doi-chung` **ĐỎ** vì chỉ nhận 2 trong 4 báo cáo | Khẳng định `[ $(ls bao-cao/p4-*.json \| wc -l) -eq 4 ]` của QT 6.4 đang làm đúng việc của nó |

---

## L3. Bước 1 — Dựng pipeline tám job tuần tự, đo **325 s**, và lập bản đồ dữ liệu (30 phút)

Kiểm chứng QT 4.1.

Bước này có một thứ tự bắt buộc: **đẩy pipeline chạy trước, viết công cụ trong lúc nó chạy.** Pipeline tuần tự mất khoảng 355 giây; viết `do-duong-gang.sh` mất khoảng 12 phút. Làm tuần tự thì bước này tràn giờ; làm chồng lên nhau thì vừa đúng 30 phút.

### 1.1. Tạo hai project, nạp lại bộ công cụ ba buổi trước (5 phút)

```bash
source ~/.gitlab-lab.env
mkdir -p ~/lab08 && cd ~/lab08
export HAU_TO="${USER}"

PID=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{\"name\":\"lab08-dag-${HAU_TO}\",\"visibility\":\"internal\"}" \
  "$GITLAB/api/v4/projects" | jq -r .id)
PID_GC=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{\"name\":\"lab08-goi-chung-${HAU_TO}\",\"visibility\":\"internal\"}" \
  "$GITLAB/api/v4/projects" | jq -r .id)
RID=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/runners?status=online" | jq -r '.[0].id')
export PID PID_GC RID
{ echo "export PID=$PID"; echo "export PID_GC=$PID_GC"; echo "export RID=$RID"; } >> ~/.gitlab-lab.env
echo "PID=$PID  PID_GC=$PID_GC  RID=$RID"
```

Nạp lại — **không** viết lại. `cong-cu07.sh` của buổi 07 tự nạp `cong-cu.sh` của buổi 05, nên một dòng `source` được cả 17 hàm, và chúng bám vào `$PID` vừa đặt:

```bash
source ~/lab07/cong-cu07.sh
type job_id job_tt art_http job_bang_rong tao_pipe >/dev/null \
  && echo "nap du 11 + 6 ham, A=$A"
# hai biến tiện dụng riêng cho buổi 08
export A_GC="$GITLAB/api/v4/projects/$PID_GC"
export GO_ROI="$HOME/lab07/go-roi.sh"
```

Khởi tạo kho git của `lab08-dag`:

```bash
cd ~/lab08
git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$A" | jq -r .path_with_namespace).git"
git config user.email "hocvien@lab.local"; git config user.name "hoc vien"
printf '# lab08 needs dag parallel matrix\n' > README.md
# tệp cấu hình CÓ SẴN TRONG GIT — bước 3 sẽ cần đúng tệp này
mkdir -p cau-hinh && printf '{"phien_ban":"0.0.0-mac-dinh"}\n' > cau-hinh/app.json
git add -A && git commit -q -m "khoi tao"
git push -q -u origin main
```

### 1.2. Pipeline mẫu — tám job, bốn stage, KHÔNG một dòng `needs` nào (5 phút)

Đây là **ví dụ chuẩn của buổi**, và ba con số của cả buổi đều rơi ra từ nó. Đọc bảng thiết kế trước khi đọc YAML:

| stage | job | `sleep` (giây) | Artifact sinh ra | Job nào **thực sự đọc tệp** của nó |
|---|---|---|---|---|
| `xay` | `build-fe` | **60** | `ra-fe/` — 3 tệp | `test-e2e`, `package` |
| `xay` | `build-be` | **90** | `ra-be/` — 4 tệp **và** `cau-hinh/app.json` | `test-unit`, `test-e2e`, `package` |
| `xay` | `lint` | **20** | `ra-lint/` — 1 tệp | **không ai** |
| `xay` | `scan` | **150** | `ra-scan/` — 2 tệp | **không ai** |
| `kiem` | `test-unit` | **45** | `ra-unit/` — 3 tệp | **không ai** — `deploy` chỉ cần nó **xanh** (cạnh cổng) |
| `kiem` | `test-e2e` | **120** | `bao-cao/e2e.json` — 1 tệp | `deploy` **đọc tệp này** (cạnh dữ liệu) |
| `dong-goi` | `package` | **30** | `ra-goi/goi.txt` — 1 tệp | `deploy` **đọc tệp này** (cạnh dữ liệu) |
| `trien-khai` | `deploy` | **25** | `ket-qua/` | — |

Hai dòng cuối chứa phân biệt quan trọng nhất của bước 2: trong tám mũi tên của bản đồ, **bảy là cạnh dữ liệu** (job sau đọc tệp của job trước) và **một là cạnh cổng** — `deploy ← test-unit`. `deploy` không đọc một byte nào của `test-unit`; nó chỉ cần biết bộ test đã xanh. Cạnh cổng vẫn phải khai, vì nếu không thì `deploy` chạy song song với `test-unit` và ta triển khai trước khi biết kết quả test. Nhưng nó khai kèm `artifacts: false`, và bước 2.4 đo cái giá của việc quên hai chữ đó bằng số tệp.

Còn `cau-hinh/app.json` là tệp **có sẵn trong git** với giá trị `0.0.0-mac-dinh`, và `build-be` ghi đè nó bằng số hiệu pipeline. Nó tồn tại để bước 3 có chỗ tái hiện hỏng im lặng; đừng xoá nó khỏi git.

Ba phép cộng phải làm **bằng tay trước khi chạy**, rồi máy sẽ xác nhận:

```
Tổng theo stage = max(60,90,20,150) + max(45,120) + 30 + 25
                = 150 + 120 + 30 + 25 = 325 giây          <- công thức TUẦN TỰ
Đường găng      = build-be 90 -> test-e2e 120 -> deploy 25 = 235 giây   <- công thức DAG
Phút runner     = 60+90+20+150+45+120+30+25 = 540 giây     <- GIỐNG NHAU ở cả hai ca
Lãng phí hàng rào = 325 - 235 = 90 giây = 27,7% của 325
```

Con số **540** là con số dễ bỏ qua nhất và quan trọng nhất: nó nói rằng `needs` **không** trả lại một giây phút runner nào. Hai đại lượng, hai người trả tiền — người trả tiền cho 540 s là bộ phận hạ tầng, người trả tiền cho 325 s là lập trình viên đang chờ.

```yaml
# ~/lab08/.gitlab-ci.yml — nhánh tuan-tu. KHÔNG có dòng needs nào.
stages: [xay, kiem, dong-goi, trien-khai]

default:
  image: alpine:3.20

variables:
  GIT_DEPTH: "5"

# ---------- stage xay: bốn job, không job nào chờ ai ----------
build-fe:
  stage: xay
  script:
    - mkdir -p ra-fe
    - for i in 1 2 3; do echo "fe-$i pipeline=$CI_PIPELINE_ID" > "ra-fe/tep-$i.txt"; done
    - sleep 60
  artifacts: { paths: [ra-fe/], expire_in: 1 hour }

build-be:
  stage: xay
  script:
    - mkdir -p ra-be cau-hinh
    - for i in 1 2 3 4; do echo "be-$i pipeline=$CI_PIPELINE_ID" > "ra-be/tep-$i.txt"; done
    # GHI ĐÈ tệp cấu hình có sẵn trong git bằng số hiệu pipeline này
    - 'printf ''{"phien_ban":"%s"}\n'' "$CI_PIPELINE_ID" > cau-hinh/app.json'
    - cat cau-hinh/app.json
    - sleep 90
  artifacts: { paths: [ra-be/, cau-hinh/], expire_in: 1 hour }

lint:
  stage: xay
  script:
    - mkdir -p ra-lint
    - echo "lint ok" > ra-lint/ket-qua.txt
    - sleep 20
  artifacts: { paths: [ra-lint/], expire_in: 1 hour }

# JOB DÀI NHẤT VÀ KHÔNG AI CẦN KẾT QUẢ CỦA NÓ — nguồn của toàn bộ 90 giây lãng phí.
scan:
  stage: xay
  script:
    - mkdir -p ra-scan
    - echo "0 lo hong" > ra-scan/bao-cao.txt
    - echo "quet 1.240 tep" > ra-scan/so-lieu.txt
    - sleep 150
  artifacts: { paths: [ra-scan/], expire_in: 1 hour }

# ---------- stage kiem ----------
test-unit:
  stage: kiem
  script:
    - test -s ra-be/tep-1.txt || { echo "THIEU artifact cua build-be"; exit 1; }
    - mkdir -p ra-unit
    - echo "95 test, 0 that bai" > ra-unit/ket-qua.txt
    - echo "coverage=82" > ra-unit/so-lieu.txt
    - echo '<testsuite tests="95" failures="0"/>' > ra-unit/junit.xml
    - sleep 45
  artifacts: { paths: [ra-unit/], expire_in: 1 hour }

test-e2e:
  stage: kiem
  script:
    - test -s ra-fe/tep-1.txt || { echo "THIEU artifact cua build-fe"; exit 1; }
    # ĐỌC cấu hình do build-be sinh ra. Bước 3 sẽ bỏ cạnh trỏ build-be và
    # dòng dưới VẪN đọc được — vì cau-hinh/app.json cũng có trong git.
    - 'CH=$(sed -n ''s/.*"phien_ban":"\([^"]*\)".*/\1/p'' cau-hinh/app.json)'
    - 'echo "CAU_HINH_DUOC_KIEM=$CH   (pipeline nay = $CI_PIPELINE_ID)"'
    - mkdir -p bao-cao
    - 'printf ''{"job":"test-e2e","luong":12,"that_bai":0,"cau_hinh":"%s"}\n'' "$CH" > bao-cao/e2e.json'
    - cat bao-cao/e2e.json
    - sleep 120
  artifacts: { paths: [bao-cao/], expire_in: 1 hour }

# ---------- stage dong-goi ----------
package:
  stage: dong-goi
  script:
    # ĐẾM TỆP NHẬN ĐƯỢC — phép đo của QT 4.3, bước 2 sẽ so lại.
    # Đếm TRƯỚC khi job tự tạo tệp nào, và cau-hinh/ KHÔNG nằm trong danh sách đếm.
    - 'echo "SO_TEP_NHAN_DUOC=$(find ra-fe ra-be ra-lint ra-scan ra-unit ra-goi bao-cao -type f 2>/dev/null | wc -l | tr -d " ")"'
    - find ra-fe ra-be ra-lint ra-scan ra-unit ra-goi bao-cao -type f 2>/dev/null | sort
    - test -s ra-fe/tep-1.txt && test -s ra-be/tep-1.txt
    - mkdir -p ra-goi
    - echo "goi cua pipeline $CI_PIPELINE_ID" > ra-goi/goi.txt
    - sleep 30
  artifacts: { paths: [ra-goi/], expire_in: 1 hour }

# ---------- stage trien-khai ----------
deploy:
  stage: trien-khai
  script:
    - 'SO=$(find ra-fe ra-be ra-lint ra-scan ra-unit ra-goi bao-cao -type f 2>/dev/null | wc -l | tr -d " ")'
    - 'echo "SO_TEP_NHAN_DUOC=$SO"'
    - find ra-fe ra-be ra-lint ra-scan ra-unit ra-goi bao-cao -type f 2>/dev/null | sort
    # HAI cạnh dữ liệu: goi cua package, va bao cao cua test-e2e
    - test -s ra-goi/goi.txt      || { echo "THIEU goi cua package"; exit 1; }
    - test -s bao-cao/e2e.json    || { echo "THIEU bao cao cua test-e2e"; exit 1; }
    - 'echo "TRIEN_KHAI_CAU_HINH=$(sed -n ''s/.*"cau_hinh":"\([^"]*\)".*/\1/p'' bao-cao/e2e.json)"'
    - mkdir -p ket-qua
    - 'printf ''{"job":"%s","so_tep":%s}\n'' "$CI_JOB_NAME" "$SO" > ket-qua/nhan-duoc.json'
    - sleep 25
  artifacts: { paths: [ket-qua/], expire_in: 1 hour }
```

Đẩy lên nhánh `tuan-tu` và **đi tiếp ngay**, đừng ngồi xem:

```bash
cd ~/lab08
git checkout -qB tuan-tu main
# dán YAML ở trên vào ~/lab08/.gitlab-ci.yml rồi:
git add -A && git commit -q -m "pipeline mau 8 job — tuan tu, khong needs"
git push -q -f origin HEAD:refs/heads/tuan-tu
sleep 6
P_TT=$(curl -sf "${H[@]}" "$A/pipelines?ref=tuan-tu&per_page=1" | jq -r '.[0].id')
echo "pipeline tuan-tu = $P_TT  (khoang 355 giay — viet cong cu trong luc cho)"
```

### 1.3. `do-duong-gang.sh` — công cụ chính của buổi, viết trong lúc pipeline chạy (12 phút)

`go-roi.sh` của buổi 07 trả lời câu hỏi *"job này hỏng ở pha nào"*. `do-duong-gang.sh` trả lời câu hỏi của buổi 08: *"pipeline này lãng phí bao nhiêu giây vì hàng rào stage"*. Nó cần bốn thứ mà API cho sẵn (`stage`, `duration`, `queued_duration`, `started_at`/`finished_at`) và một thứ API **không** cho: đồ thị phụ thuộc. Cạnh phụ thuộc nằm trong tệp YAML, không nằm trong dữ liệu pipeline — nên script nhận nó qua tệp `canh.tsv` mà ta lập ở mục 1.4.

Script có một thủ pháp đo cần hiểu trước khi chạy. `duration` của một job **gồm cả phần cố định**: tạo container, `git fetch`, phục hồi cache, tải artifact, tải lên artifact. Với job `sleep 150` thì `duration` thường là 155–162 giây. Nếu tính hai công thức trên `duration` thì cả hai số đều phồng lên và hiệu của chúng lệch theo số stage. Vì vậy script gọi lại `go-roi.sh` để lấy **giây pha `step_script`** — phần thời gian đúng bằng lệnh của ta — và tính hai công thức trên đó. Hiệu giữa `duration` và `step_script` chính là **phần cố định mỗi job**, và đó là đại lượng bước 4 sẽ dùng lại.

```bash
cat > ~/lab08/do-duong-gang.sh <<'SH'
#!/usr/bin/env bash
# do-duong-gang.sh — HAI công thức tính thời gian pipeline, đo từ API GitLab.
#
# Dùng:
#   bash do-duong-gang.sh <PID> <PIPELINE_ID> [--canh canh.tsv] [--pha] [--bang|--tsv]
#     --canh <tep>  tệp cạnh phụ thuộc, mỗi dòng "job<TAB>job_no_can"; bật tính ĐƯỜNG GĂNG
#     --pha         lấy giây pha step_script qua go-roi.sh buổi 07 (chậm hơn ~1 giây/job,
#                   nhưng loại được phần cố định ra khỏi hai công thức)
#     --bang        mặc định: bảng job + khối tổng kết
#     --tsv         MỘT dòng TSV để nối vào bang-duong-gang.tsv
#
# CƠ CHẾ HAI CÔNG THỨC
#   TUẦN TỰ : T = Σ  max(job trong stage)     <- hàng rào stage, buổi 03 QT 5.3
#                 stage
#   DAG     : T = max  Σ(job trên một đường)  <- quan hệ dữ liệu, buổi 08 QT 4.1
#                 đường
#   LÃNG PHÍ HÀNG RÀO = TUẦN TỰ − DAG. Hiệu này tồn tại độc lập với việc runner mạnh hay yếu.
#
# PHÚT RUNNER = Σ duration của MỌI job. Nó KHÔNG đổi khi chuyển sang needs — đó là
# kết luận quan trọng nhất mà script này in ra, và là chỗ người ta hay nói sai.
#
# MÃ THOÁT: 0 bình thường · 2 thiếu tham số · 3 không đọc được pipeline · 4 pipeline chưa xong
set -uo pipefail
PID_IN=""; PIPE_IN=""; CANH=""; PHA=0; DANG="--bang"
while [ $# -gt 0 ]; do
  case "$1" in
    --canh) CANH="${2:-}"; shift 2 ;;
    --pha)  PHA=1; shift ;;
    --tsv|--bang) DANG="$1"; shift ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) if [ -z "$PID_IN" ]; then PID_IN="$1"; elif [ -z "$PIPE_IN" ]; then PIPE_IN="$1"; fi; shift ;;
  esac
done
[ -n "$PID_IN" ] && [ -n "$PIPE_IN" ] || {
  echo "Dùng: bash do-duong-gang.sh <PID> <PIPELINE_ID> [--canh canh.tsv] [--pha] [--bang|--tsv]" >&2
  exit 2; }
: "${GITLAB:?chưa đặt GITLAB}"; : "${GITLAB_TOKEN:?chưa đặt GITLAB_TOKEN}"
GO_ROI="${GO_ROI:-$HOME/lab07/go-roi.sh}"
HH=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")
AA="$GITLAB/api/v4/projects/$PID_IN"

PP=$(curl -sf "${HH[@]}" "$AA/pipelines/$PIPE_IN") || { echo "khong doc duoc pipeline $PIPE_IN" >&2; exit 3; }
REF=$(printf '%s' "$PP" | jq -r '.ref'); TT_P=$(printf '%s' "$PP" | jq -r '.status')
JOBS=$(curl -sf "${HH[@]}" "$AA/pipelines/$PIPE_IN/jobs?per_page=100") || exit 3

# id · stage · ten · giay_job · giay_script(-1 nếu chưa đo) · cho · bat_dau · ket_thuc · tt
RAW=$(printf '%s' "$JOBS" | jq -r '
  def ep: if . == null then 0 else (.[0:19] | strptime("%Y-%m-%dT%H:%M:%S") | mktime) end;
  [ .[] | select(.status != "skipped" and .status != "manual") ]
  | sort_by(.id) | .[]
  | [ .id, .stage, .name, ((.duration // 0) | floor), -1,
      ((.queued_duration // 0) | floor), (.started_at | ep), (.finished_at | ep), .status ]
  | @tsv')
[ -n "$RAW" ] || { echo "pipeline $PIPE_IN khong co job nao" >&2; exit 3; }

if [ "$PHA" = 1 ] && [ -f "$GO_ROI" ]; then
  RAW=$(printf '%s\n' "$RAW" | while IFS=$'\t' read -r id st ten gj gs cho bd kt tt; do
    s=$(bash "$GO_ROI" "$PID_IN" "$id" --pha 2>/dev/null \
        | awk -F'\t' '$2=="step_script" || $2=="build_script" {print $4; exit}')
    case "$s" in ''|*[!0-9]*) s=-1 ;; esac
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$id" "$st" "$ten" "$gj" "$s" "$cho" "$bd" "$kt" "$tt"
  done)
fi

TMPJ=$(mktemp); printf '%s\n' "$RAW" > "$TMPJ"
trap 'rm -f "$TMPJ"' EXIT

# ---- ĐƯỜNG GĂNG LÝ THUYẾT: đường dài nhất trên đồ thị canh.tsv ----
GANG=0; DUONG="(chua co canh.tsv)"
if [ -n "$CANH" ] && [ -s "$CANH" ]; then
  KQ=$(awk -F'\t' '
    FNR==NR { g[$3] = ($5+0 >= 0 ? $5+0 : $4+0)
              if (!($3 in co)) { co[$3]=1; V[++nv]=$3 }
              next }
    /^#/ { next }
    NF < 2 { next }
    { j=$1; d=$2
      gsub(/^[ \t]+|[ \t]+$/, "", j); gsub(/^[ \t]+|[ \t]+$/, "", d)
      if (j == "" || d == "" || j == "job") next
      nd[j]++; dep[j, nd[j]] = d }
    END {
      for (r = 1; r <= nv; r++)
        for (i = 1; i <= nv; i++) {
          j = V[i]; best = 0; bp = "-"
          for (k = 1; k <= nd[j]; k++) { dd = dep[j,k]
            if ((dd in co) && dp[dd] > best) { best = dp[dd]; bp = dd } }
          v = best + g[j]
          if (v > dp[j]) { dp[j] = v; pre[j] = bp }
        }
      mx = 0; cuoi = "-"
      for (i = 1; i <= nv; i++) if (dp[V[i]] > mx) { mx = dp[V[i]]; cuoi = V[i] }
      p = cuoi; duong = cuoi
      while ((p in pre) && pre[p] != "-" && pre[p] != "") { p = pre[p]; duong = p " -> " duong }
      printf "%d\t%s\n", mx, duong
    }' "$TMPJ" "$CANH")
  GANG=$(printf '%s' "$KQ" | cut -f1); DUONG=$(printf '%s' "$KQ" | cut -f2)
fi

# ---- khối tổng kết: hai công thức, phút runner, slot đỉnh ----
TK=$(awk -F'\t' '
  { n++; st[n]=$2; ten[n]=$3; gj[n]=$4+0; gs[n]=($5+0 >= 0 ? $5+0 : $4+0)
    cho[n]=$6+0; bd[n]=$7+0; kt[n]=$8+0
    if (gj[n] > mj[st[n]]) mj[st[n]] = gj[n]
    if (gs[n] > ms[st[n]]) ms[st[n]] = gs[n]
    if (!(st[n] in co)) { co[st[n]]=1; S[++ns]=st[n] }
    tj += gj[n]; ts += gs[n]; tc += cho[n]
    if (bd[n] > 0 && (mb == 0 || bd[n] < mb)) mb = bd[n]
    if (kt[n] > mk) mk = kt[n] }
  END {
    for (i = 1; i <= ns; i++) { ttj += mj[S[i]]; tts += ms[S[i]] }
    wall = (mk > mb ? mk - mb : 0)
    dinh = 0
    for (i = 1; i <= n; i++) if (bd[i] > 0) { c = 0
      for (j = 1; j <= n; j++) if (bd[j] > 0 && bd[j] <= bd[i] && kt[j] > bd[i]) c++
      if (c > dinh) dinh = c }
    printf "%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n", n, tts, ttj, ts, tj, wall, dinh, tc, (tj - ts)
  }' "$TMPJ")
read -r SO_JOB TTS TTJ RUN_S RUN_J WALL DINH TCHO CO_DINH <<EOF
$TK
EOF
LP=$(( TTS - GANG )); [ "$GANG" -eq 0 ] && LP=0
PT="0,0"
[ "$TTS" -gt 0 ] && [ "$GANG" -gt 0 ] \
  && PT=$(awk -v a="$LP" -v b="$TTS" 'BEGIN{printf "%.1f", 100*a/b}' | tr '.' ',')
CDTB=$(awk -v a="$CO_DINH" -v n="$SO_JOB" 'BEGIN{printf "%.1f", (n?a/n:0)}' | tr '.' ',')

if [ "$DANG" = "--tsv" ]; then
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$REF" "$TTS" "$GANG" "$LP" "$PT" "$RUN_S" "$DINH" "$TCHO" "$WALL"
  exit 0
fi

printf '===== do-duong-gang.sh · pipeline %s · ref %s · %s · %s job =====\n' \
  "$PIPE_IN" "$REF" "$TT_P" "$SO_JOB"
printf 'stage\tjob\tgiay_job\tgiay_script\tcho\ttt\n'
awk -F'\t' '{printf "%s\t%s\t%s\t%s\t%s\t%s\n", $2, $3, $4, ($5+0>=0?$5:"-"), $6, $9}' "$TMPJ" \
  | column -t -s $'\t'
echo
printf 'TONG_THEO_STAGE_script  %6d giay   <- cong thuc TUAN TU (QT 4.1)\n' "$TTS"
printf 'TONG_THEO_STAGE_job     %6d giay   (gom phan co dinh)\n' "$TTJ"
printf 'DUONG_GANG_LY_THUYET    %6d giay   <- cong thuc DAG: %s\n' "$GANG" "$DUONG"
printf 'LANG_PHI_HANG_RAO       %6d giay   = %s%% cua tong theo stage\n' "$LP" "$PT"
printf 'WALL_DO_DUOC            %6d giay   (finished_at cuoi - started_at dau)\n' "$WALL"
printf 'PHUT_RUNNER_script      %6d giay   <- KHONG doi khi chuyen sang needs\n' "$RUN_S"
printf 'PHUT_RUNNER_job         %6d giay\n' "$RUN_J"
printf 'PHAN_CO_DINH_TONG       %6d giay   trung binh %s giay/job\n' "$CO_DINH" "$CDTB"
printf 'SLOT_DINH               %6d job cung luc\n' "$DINH"
printf 'TONG_QUEUED_DURATION    %6d giay   <- lon la dau hieu thieu slot (QT 7.1)\n' "$TCHO"
SH
chmod +x ~/lab08/do-duong-gang.sh
bash -n ~/lab08/do-duong-gang.sh && echo "cu phap OK"
```

### 1.4. Bản đồ dữ liệu — nối tiếp `ban-do-phu-thuoc.md` của buổi 03 (8 phút)

Buổi 03 đã lập `ban-do-phu-thuoc.md` với đúng năm cột và cố ý **không** sửa gì. Mở lại nó và đọc cột cuối:

```bash
sed -n '1,40p' ~/gitlab-portfolio/03-cu-phap-yaml-va-stage/ban-do-phu-thuoc.md \
  | grep -E '^\|' | column -t -s '|'
```

Cột *Chênh lệch* của bảng đó ghi những dòng như `chờ build vô ích` và `chờ test-cham vô ích 60 giây`. Mỗi dòng ấy là **một cạnh sẽ bị xoá** hôm nay. Bây giờ lập bảng cùng định dạng cho pipeline mẫu tám job — giữ nguyên năm cột để hai bảng đọc liền được nhau:

```bash
cd ~/lab08
cat > ban-do-du-lieu.md <<'MD'
# Bản đồ dữ liệu — pipeline mẫu buổi 08
Nối tiếp `ban-do-phu-thuoc.md` buổi 03, giữ nguyên năm cột.
Đo trên GitLab CE 17.7 · Runner 17.7 · executor docker · concurrent 8. Máy đo: DIEN-VAO-DAY.
Quy tắc lập bảng (QT 5.1 bước 1): cột 3 chỉ ghi job mà job này **đọc tệp** của nó.
Cửa chất lượng (chờ nhưng KHÔNG lấy tệp) ghi vào cột 4 kèm chữ "cửa" — cạnh đó sẽ khai `artifacts: false`.

| Job | Stage | Nó cần artifact của ai | Nó **thực sự** phải chờ ai | Chênh lệch |
|---|---|---|---|---|
| `build-fe` | xay | — | — | — |
| `build-be` | xay | — | — | — |
| `lint` | xay | — | — | — |
| `scan` | xay | — | — | chờ hàng rào **0 giây**, nhưng **bắt 4 job sau chờ nó 150 giây** |
| `test-unit` | kiem | `ra-be/` của `build-be` | `build-be` | chờ `scan` **vô ích 60 giây** |
| `test-e2e` | kiem | `ra-fe/` của `build-fe`, `cau-hinh/app.json` của `build-be` | `build-fe`, `build-be` | chờ `scan` **vô ích 60 giây** |
| `package` | dong-goi | `ra-fe/` và `ra-be/` | `build-fe`, `build-be` | chờ `test-e2e` **vô ích 120 giây** |
| `deploy` | trien-khai | `ra-goi/goi.txt` của `package`, `bao-cao/e2e.json` của `test-e2e` | `package`, `test-e2e`, **`test-unit` (cửa)** | — |

Tổng: **8** mũi tên = **7** cạnh dữ liệu + **1** cạnh cổng (`deploy` <- `test-unit`).
MD
sed -i "s/DIEN-VAO-DAY/$(hostname)/" ban-do-du-lieu.md
grep -cE '^\| `' ban-do-du-lieu.md
```

Bước 2 của QT 5.1 nói: **một mũi tên thành một dòng `needs`**. Để phép chuyển đó là cơ học chứ không là cảm nhận, ta rút bảng thành một tệp cạnh — mỗi dòng đúng **một** cạnh:

```bash
cd ~/lab08
cat > canh.tsv <<'TSV'
# job	job_no_can	loai	(TAB phan cach; moi dong = MOT canh = MOT phan tu trong needs)
test-unit	build-be	du-lieu
test-e2e	build-fe	du-lieu
test-e2e	build-be	du-lieu
package	build-fe	du-lieu
package	build-be	du-lieu
deploy	package	du-lieu
deploy	test-e2e	du-lieu
deploy	test-unit	cong
TSV
awk -F'\t' '!/^#/ && NF>=2 {n++; l[$3]++} END {printf "so canh = %d (du-lieu %d, cong %d)\n", n, l["du-lieu"], l["cong"]}' canh.tsv
```

Tám cạnh cho tám job: **7 cạnh dữ liệu** và **1 cạnh cổng**. Cột thứ ba không tham gia phép tính đường găng — cả hai loại cạnh đều buộc thứ tự như nhau — nhưng nó quyết định **một** thứ ở bước 2: cạnh `cong` khai thêm `artifacts: false`, cạnh `du-lieu` thì không. Đó là toàn bộ khác biệt giữa 5 tệp và 2 tệp mà mục 2.4 sẽ đo.

Hai job `lint` và `scan` **không xuất hiện ở cột nào** — chúng không cần ai và không ai cần chúng, và đó chính là câu trả lời cho câu hỏi *"90 giây lãng phí đến từ đâu"*.

Dự đoán **trước khi** pipeline tuần tự chạy xong. `do-duong-gang.sh` tính đường găng từ `canh.tsv` cộng `duration` của pipeline tuần tự — nghĩa là nó cho ra con số **DAG** trong khi ta vẫn chưa viết một dòng `needs` nào:

```bash
cd ~/lab08
cho_pipeline "$P_TT" 600
bash ~/lab08/do-duong-gang.sh "$PID" "$P_TT" --canh canh.tsv --pha
```

Đọc khối tổng kết và đối chiếu ba con số đã cộng tay: `TONG_THEO_STAGE_script` phải là **325** (dao động ±5 vì `sleep` cộng một hai giây thiết lập shell), `DUONG_GANG_LY_THUYET` phải là **235** kèm đường `build-be -> test-e2e -> deploy`, `LANG_PHI_HANG_RAO` phải là **90** và **27,7%**. Đồng thời `PHUT_RUNNER_script` phải là **540**, và `WALL_DO_DUOC` khoảng **355** — hiệu giữa 355 và 325 là phần cố định của bốn stage, tức chi phí chuyển stage mà không công thức nào tính tới.

Ghi dòng đầu tiên của hiện vật chính:

```bash
cd ~/lab08
{ printf 'ca\ttong_theo_stage\tduong_gang\tlang_phi\tphan_tram\tphut_runner\tslot_dinh\ttong_cho\twall\n'
  bash ~/lab08/do-duong-gang.sh "$PID" "$P_TT" --canh canh.tsv --pha --tsv
} > bang-duong-gang.tsv
column -t -s $'\t' bang-duong-gang.tsv
```

**CHECKPOINT 1 — pipeline tuần tự xong; tổng theo stage trong 318–335 s, đường găng lý thuyết trong 228–248 s, phút runner trong 530–560 s, và `do-duong-gang.sh` in đủ năm nhãn tổng kết.**

```bash
touch ~/lab08/checkpoint.log
cd ~/lab08
OUT=$(bash ~/lab08/do-duong-gang.sh "$PID" "$P_TT" --canh canh.tsv --pha)
tts=$(printf '%s\n' "$OUT" | awk '/^TONG_THEO_STAGE_script/{print $2}')
gg=$(printf  '%s\n' "$OUT" | awk '/^DUONG_GANG_LY_THUYET/{print $2}')
run=$(printf '%s\n' "$OUT" | awk '/^PHUT_RUNNER_script/{print $2}')
nhan=$(printf '%s\n' "$OUT" | grep -cE '^(TONG_THEO_STAGE_script|DUONG_GANG_LY_THUYET|LANG_PHI_HANG_RAO|PHUT_RUNNER_script|SLOT_DINH)')
tt=$(curl -sf "${H[@]}" "$A/pipelines/$P_TT" | jq -r .status)
{ [ "$tt" = success ] && [ "$nhan" -eq 5 ] \
  && [ "$tts" -ge 318 ] && [ "$tts" -le 335 ] \
  && [ "$gg"  -ge 228 ] && [ "$gg"  -le 248 ] \
  && [ "$run" -ge 530 ] && [ "$run" -le 560 ]; } \
  && echo "CHECKPOINT 1 — ĐẠT (tong_theo_stage=${tts}s tham chieu 325 · duong_gang=${gg}s tham chieu 235 · phut_runner=${run}s tham chieu 540 · pipeline=$tt)" \
  || echo "CHECKPOINT 1 — LỖI (tt=$tt, tong=${tts:-?} can 318-335, gang=${gg:-?} can 228-248, runner=${run:-?} can 530-560, nhan=$nhan can 5 — xem §L9 dòng 4, 5, 6)" \
  | tee -a ~/lab08/checkpoint.log
```

**CHECKPOINT 2 — bản đồ dữ liệu có 8 dòng job, `canh.tsv` có đúng 8 cạnh, và mọi tên job trong `canh.tsv` đều là job có thật trong pipeline.**

```bash
cd ~/lab08
so_job=$(grep -cE '^\| `[a-z-]+` \|' ban-do-du-lieu.md)
so_canh=$(awk -F'\t' '!/^#/ && NF>=2 {n++} END {print n+0}' canh.tsv)
co_may=$(grep -c 'DIEN-VAO-DAY' ban-do-du-lieu.md)
curl -sf "${H[@]}" "$A/pipelines/$P_TT/jobs?per_page=100" | jq -r '.[].name' | sort -u > /tmp/ten-job.txt
la=$(awk -F'\t' '!/^#/ && NF>=2 {print $1; print $2}' canh.tsv | sort -u | comm -23 - /tmp/ten-job.txt | wc -l | tr -d ' ')
{ [ "$so_job" -eq 8 ] && [ "$so_canh" -eq 8 ] && [ "$co_may" -eq 0 ] && [ "$la" -eq 0 ]; } \
  && echo "CHECKPOINT 2 — ĐẠT (8 dòng job, $so_canh cạnh, 0 tên job lạ, đã thay DIEN-VAO-DAY)" \
  || echo "CHECKPOINT 2 — LỖI (so_job=$so_job cần 8, so_canh=$so_canh cần 8, ten_la=$la cần 0, con_cho_trong=$co_may cần 0 — xem §L9 dòng 7)" \
  | tee -a ~/lab08/checkpoint.log
```

---

## L4. Bước 2 — Bản đồ thành `needs`: đo đường găng **235 s**, và đo tập artifact đổi (30 phút)

Kiểm chứng QT 4.2, QT 4.3, QT 5.1.

Bước này làm **bước 2 và bước 3** của QT 5.1: dịch tám cạnh thành tám phần tử `needs`, rồi **đo lại**. Bỏ bước đo lại thì không biết mình vừa cắt được 90 giây hay vừa làm chậm đi — và cả hai đều đã xảy ra trên các repo thật.

### 2.1. Tám cạnh thành tám phần tử `needs` — bản trần trụi (7 phút)

Vòng này khai **cả tám cạnh giống nhau**, chưa phân biệt cạnh dữ liệu với cạnh cổng. Làm vậy có chủ ý: mục 2.4 sẽ đo cái giá của việc không phân biệt, bằng số tệp. Viết `needs` ở dạng một dòng cho mỗi job để đếm được bằng máy. Đây là bốn dòng duy nhất khác so với YAML bước 1:

```yaml
# mảnh — dán vào ~/lab08/.gitlab-ci.yml, mỗi khối thêm ĐÚNG một dòng needs
test-unit:
  needs: [build-be]

test-e2e:
  needs: [build-fe, build-be]

package:
  needs: [build-fe, build-be]

deploy:
  needs: [package, test-unit, test-e2e]
```

Lệnh dưới đây chèn bốn dòng đó vào đúng chỗ, rồi **đếm cạnh trong YAML và so với `canh.tsv`** — đây là cơ chế chống đúng cái bẫy mà QT 5.1 mô tả: bản đồ có 8 mũi tên mà YAML chỉ có 6 dòng:

```bash
cd ~/lab08
git checkout -qB dag tuan-tu
sed -i \
  -e 's|^test-unit:$|test-unit:\n  needs: [build-be]|' \
  -e 's|^test-e2e:$|test-e2e:\n  needs: [build-fe, build-be]|' \
  -e 's|^package:$|package:\n  needs: [build-fe, build-be]|' \
  -e 's|^deploy:$|deploy:\n  needs: [package, test-unit, test-e2e]|' \
  .gitlab-ci.yml
grep -nE '^ +needs:' .gitlab-ci.yml

cat > ~/lab08/so-canh.sh <<'SH'
#!/usr/bin/env bash
# so-canh.sh [tep_yaml] [tep_canh] — QT 5.1: mỗi mũi tên đúng MỘT phần tử needs.
# Đọc được CẢ HAI cách viết needs: dạng một dòng "needs: [a, b]" và dạng khối
# "needs:" + "- job: a" (+ "artifacts: false" của cạnh cổng).
# In BAN_DO=<n> YAML=<n> và danh sách cạnh lệch. Mã thoát 0 khi hai bên khớp.
Y="${1:-$HOME/lab08/.gitlab-ci.yml}"; C="${2:-$HOME/lab08/canh.tsv}"
awk -F'\t' '!/^#/ && NF>=2 {print $1"\t"$2}' "$C" | sort -u > /tmp/canh-ban-do.txt
awk '
  /^[a-z][a-z0-9._-]*:$/ { job = $0; sub(/:$/, "", job); trong = 0; next }
  /^ +needs: \[/ {
    trong = 0
    line = $0; sub(/^ +needs: \[/, "", line); sub(/\].*$/, "", line)
    n = split(line, a, ",")
    for (i = 1; i <= n; i++) { d = a[i]; gsub(/[ \t"]/, "", d); if (d != "") print job "\t" d }
    next
  }
  /^ +needs:[ \t]*$/            { trong = 1; next }
  trong && /^ +- +job: /        { d = $0; sub(/^ +- +job: /, "", d); gsub(/[ \t"]/, "", d)
                                  if (d != "") print job "\t" d; next }
  trong && /^ +artifacts: /     { next }
  trong && /^ +[a-z_]+:/        { trong = 0 }
  ' "$Y" | sort -u > /tmp/canh-yaml.txt
bd=$(wc -l < /tmp/canh-ban-do.txt | tr -d ' '); yl=$(wc -l < /tmp/canh-yaml.txt | tr -d ' ')
printf 'BAN_DO=%s YAML=%s\n' "$bd" "$yl"
echo "--- co trong ban do, THIEU trong YAML (job dang cho vo ich hoac chua khai) ---"
comm -23 /tmp/canh-ban-do.txt /tmp/canh-yaml.txt
echo "--- co trong YAML, KHONG co trong ban do (dang cho vo ich) ---"
comm -13 /tmp/canh-ban-do.txt /tmp/canh-yaml.txt
[ "$bd" = "$yl" ] && [ -z "$(comm -3 /tmp/canh-ban-do.txt /tmp/canh-yaml.txt)" ]
SH
bash ~/lab08/so-canh.sh; echo "ma thoat = $?"
```

Trước khi đẩy, đọc tệp **sau phân giải** để chắc `needs` nằm đúng cấp — buổi 03 QT 4.3 đã dạy việc này, và ở đây nó cần thiết vì `needs` đặt sai cấp vẫn cho YAML hợp lệ và **không có tác dụng gì**:

```bash
cd ~/lab08
curl -sf "${H[@]}" --request POST --header 'Content-Type: application/json' \
  --data "$(jq -n --arg c "$(cat .gitlab-ci.yml)" '{content:$c}')" \
  "$A/ci/lint" | jq '{valid, errors, so_dong_needs: (.merged_yaml | [scan("needs:")] | length)}'
git add -A && git commit -q -m "8 canh thanh 8 phan tu needs"
git push -q -f origin HEAD:refs/heads/dag
sleep 6
P_DAG=$(curl -sf "${H[@]}" "$A/pipelines?ref=dag&per_page=1" | jq -r '.[0].id')
echo "pipeline dag = $P_DAG  (du kien 235 giay script, wall ~255)"
```

### 2.2. Đo lại — bước 3 của QT 5.1 (7 phút)

```bash
cd ~/lab08
cho_pipeline "$P_DAG" 600
bash ~/lab08/do-duong-gang.sh "$PID" "$P_DAG" --canh canh.tsv --pha
bash ~/lab08/do-duong-gang.sh "$PID" "$P_DAG" --canh canh.tsv --pha --tsv >> bang-duong-gang.tsv
column -t -s $'\t' bang-duong-gang.tsv
```

Ba việc phải đọc ra từ hai dòng của bảng, theo thứ tự quan trọng giảm dần:

1. `wall` giảm từ khoảng **355** xuống khoảng **255** giây. Đây là con số duy nhất mà lập trình viên cảm nhận được.
2. `phut_runner` **không đổi**: 540 ở cả hai dòng. Nếu dòng thứ hai lệch quá 5% thì có job bị chạy lại hoặc bị bỏ — kiểm bằng `job_bang_rong "$P_DAG"` trước khi kết luận gì thêm.
3. `slot_dinh` tăng từ **4** lên **4** — bằng nhau, vì stage `xay` của ca tuần tự cũng đã có 4 job song song. Đây là chỗ **định lượng ngược lại**: người ta hay nghĩ DAG luôn đòi nhiều slot hơn, nhưng đỉnh slot phụ thuộc hình dạng đồ thị, không phụ thuộc việc có `needs` hay không. Ở ví dụ chuẩn, đỉnh không đổi mà thời gian giảm 90 giây — bữa trưa miễn phí duy nhất của buổi.

Vẽ `dag.mmd` để hiện vật kể được câu chuyện mà bảng số không kể: đường găng đi qua đâu.

```bash
cd ~/lab08
cat > dag.mmd <<'MMD'
%% dag.mmd — pipeline mau buoi 08. GitLab CE 17.7 · Runner 17.7.
%% Duong gang: build-be 90 -> test-e2e 120 -> deploy 25 = 235 giay.
%% Tong theo stage 325 giay. Lang phi hang rao 90 giay = 27,7%.
%% 8 mui ten = 7 canh du lieu + 1 canh cong (deploy <- test-unit, artifacts false).
graph LR
    FE["build-fe<br/>60 s"]
    BE["build-be<br/>90 s"]
    LI["lint<br/>20 s<br/>khong ai can"]
    SC["scan<br/>150 s<br/>KHONG AI CAN<br/>nguon cua 90 s lang phi"]
    TU["test-unit<br/>45 s"]
    TE["test-e2e<br/>120 s"]
    PK["package<br/>30 s"]
    DP["deploy<br/>25 s"]

    BE ==> TU
    FE --> TE
    BE ==> TE
    FE --> PK
    BE --> PK
    PK --> DP
    TU -->|"canh CONG<br/>artifacts false"| DP
    TE ==> DP
MMD
grep -c '\-\->\|==>' dag.mmd
```

Tám cạnh trong `canh.tsv`, tám cạnh trong YAML, tám mũi tên trong `dag.mmd`. Ba con số đó bằng nhau là điều kiện để tin bất cứ kết luận nào của bước này.

**CHECKPOINT 3 — DAG chạy xong; đường găng 228–248 s, lãng phí ≥ 80 s, phút runner lệch ca tuần tự ≤ 5%, và số cạnh trong YAML bằng số cạnh trong `canh.tsv`.**

```bash
cd ~/lab08
tt=$(curl -sf "${H[@]}" "$A/pipelines/$P_DAG" | jq -r .status)
bash ~/lab08/so-canh.sh >/dev/null; khop_canh=$?
gg=$(awk -F'\t'  '$1=="dag"{print $3}' bang-duong-gang.tsv)
lp=$(awk -F'\t'  '$1=="dag"{print $4}' bang-duong-gang.tsv)
r1=$(awk -F'\t'  '$1=="tuan-tu"{print $6}' bang-duong-gang.tsv)
r2=$(awk -F'\t'  '$1=="dag"{print $6}' bang-duong-gang.tsv)
w1=$(awk -F'\t'  '$1=="tuan-tu"{print $9}' bang-duong-gang.tsv)
w2=$(awk -F'\t'  '$1=="dag"{print $9}' bang-duong-gang.tsv)
lech=$(awk -v a="$r1" -v b="$r2" 'BEGIN{d=a-b; if(d<0)d=-d; printf "%d", (a? 100*d/a : 99)}')
{ [ "$tt" = success ] && [ "$khop_canh" -eq 0 ] \
  && [ "$gg" -ge 228 ] && [ "$gg" -le 248 ] && [ "$lp" -ge 80 ] && [ "$lech" -le 5 ]; } \
  && echo "CHECKPOINT 3 — ĐẠT (duong_gang=${gg}s · lang_phi=${lp}s · phut_runner ${r1}->${r2}s lech ${lech}% · wall ${w1}->${w2}s · so canh YAML khop canh.tsv)" \
  || echo "CHECKPOINT 3 — LỖI (tt=$tt, gang=${gg:-?} cần 228-248, lang_phi=${lp:-?} cần ≥80, lech_runner=${lech}% cần ≤5, khop_canh=$khop_canh cần 0 — xem §L9 dòng 8, 9)" \
  | tee -a ~/lab08/checkpoint.log
```

### 2.3. Đo QT 4.2 — `stage` còn tồn tại, nhưng thôi quyết định thời gian (9 phút)

Hai phép đo, cả hai đều là loại **phải đo, không tra** — hành vi này đã đổi giữa các phiên bản GitLab, nên câu trả lời chỉ có giá trị khi kèm số hiệu phiên bản.

**Phép đo A — cùng một DAG, dồn tám job vào MỘT stage.** Nếu `stage` còn quyết định thời gian thì hai ca phải khác nhau; nếu `stage` chỉ còn là nhãn thì hai ca bằng nhau:

```bash
cd ~/lab08
git checkout -qB dag-mot-stage dag
sed -i -e 's|^stages: \[xay, kiem, dong-goi, trien-khai\]$|stages: [tat-ca]|' \
       -e 's|^  stage: xay$|  stage: tat-ca|' \
       -e 's|^  stage: kiem$|  stage: tat-ca|' \
       -e 's|^  stage: dong-goi$|  stage: tat-ca|' \
       -e 's|^  stage: trien-khai$|  stage: tat-ca|' .gitlab-ci.yml
grep -cE '^  stage: tat-ca$' .gitlab-ci.yml    # phải là 8
git add -A && git commit -q -m "cung DAG, mot stage duy nhat"
git push -q -f origin HEAD:refs/heads/dag-mot-stage
sleep 6
P_1ST=$(curl -sf "${H[@]}" "$A/pipelines?ref=dag-mot-stage&per_page=1" | jq -r '.[0].id')
cho_pipeline "$P_1ST" 600
bash ~/lab08/do-duong-gang.sh "$PID" "$P_1ST" --canh canh.tsv --pha
bash ~/lab08/do-duong-gang.sh "$PID" "$P_1ST" --canh canh.tsv --pha --tsv >> bang-duong-gang.tsv
```

Chú ý một chỗ dễ đọc sai: ở ca một stage, `TONG_THEO_STAGE_script` sụt xuống còn **150** giây (chỉ còn một stage, max của nó là `scan`). Con số đó **không** phải là "pipeline nhanh hơn" — nó là bằng chứng rằng công thức tuần tự **mất nghĩa** khi không còn nhiều stage. Con số so được giữa hai ca là `DUONG_GANG_LY_THUYET` và `wall`, và chúng phải gần bằng nhau. Đó là toàn bộ nội dung QT 4.2: `stage` vẫn ở đó, vẫn vẽ ra biểu đồ, nhưng thôi làm chủ thời gian.

**Phép đo B — `needs` trỏ một job ở stage SAU.** Không tra tài liệu, thử rồi đọc kết quả. Dùng `ci/lint` cho rẻ (buổi 03 QT 4.3), rồi thử tạo pipeline thật bằng `tao_pipe` của buổi 07 để đọc thông báo lỗi nếu có:

```bash
cd ~/lab08
cat > /tmp/thu-stage-sau.yml <<'YML'
stages: [som, muon]
default: { image: alpine:3.20 }
a-som:
  stage: som
  needs: [b-muon]          # trỏ job ở stage SAU — hành vi này PHẢI ĐO
  script: [echo a]
b-muon:
  stage: muon
  script: [echo b]
YML
KQ_SAU=$(curl -sf "${H[@]}" --request POST --header 'Content-Type: application/json' \
  --data "$(jq -n --arg c "$(cat /tmp/thu-stage-sau.yml)" '{content:$c}')" \
  "$A/ci/lint" | jq -c '{valid, errors}')
echo "needs tro stage SAU  -> $KQ_SAU"

cat > /tmp/thu-cung-stage.yml <<'YML'
stages: [mot]
default: { image: alpine:3.20 }
a: { stage: mot, script: [echo a] }
b: { stage: mot, needs: [a], script: [echo b] }   # cùng stage
YML
KQ_CUNG=$(curl -sf "${H[@]}" --request POST --header 'Content-Type: application/json' \
  --data "$(jq -n --arg c "$(cat /tmp/thu-cung-stage.yml)" '{content:$c}')" \
  "$A/ci/lint" | jq -c '{valid, errors}')
echo "needs tro job CUNG stage -> $KQ_CUNG"

cat > /tmp/thu-chu-trinh.yml <<'YML'
stages: [mot]
default: { image: alpine:3.20 }
a: { stage: mot, needs: [b], script: [echo a] }
b: { stage: mot, needs: [a], script: [echo b] }   # CHU TRINH — chữ A trong DAG
YML
KQ_CT=$(curl -sf "${H[@]}" --request POST --header 'Content-Type: application/json' \
  --data "$(jq -n --arg c "$(cat /tmp/thu-chu-trinh.yml)" '{content:$c}')" \
  "$A/ci/lint" | jq -c '{valid, errors}')
echo "needs tao CHU TRINH -> $KQ_CT"

# trần số phần tử needs của một job — QT 4.2 nói 50 ở 17.7; ĐO, không tra
python3 - <<'PY' > /tmp/thu-tran-needs.yml 2>/dev/null || awk 'BEGIN{
  print "stages: [mot]"; print "default: { image: alpine:3.20 }"
  s=""
  for (i=1;i<=51;i++){ printf "n%d: { stage: mot, script: [echo %d] }\n", i, i; s = s (i>1?", ":"") "n" i }
  printf "cuoi: { stage: mot, needs: [%s], script: [echo cuoi] }\n", s
}' > /tmp/thu-tran-needs.yml
PY
KQ_TRAN=$(curl -sf "${H[@]}" --request POST --header 'Content-Type: application/json' \
  --data "$(jq -n --arg c "$(cat /tmp/thu-tran-needs.yml)" '{content:$c}')" \
  "$A/ci/lint" | jq -c '{valid, errors}')
echo "needs 51 phan tu -> $KQ_TRAN"

{ printf 'phep_do\tket_qua_json\tphien_ban\n'
  printf 'needs_tro_stage_sau\t%s\t17.7\n'   "$KQ_SAU"
  printf 'needs_cung_stage\t%s\t17.7\n'      "$KQ_CUNG"
  printf 'needs_chu_trinh\t%s\t17.7\n'       "$KQ_CT"
  printf 'needs_51_phan_tu\t%s\t17.7\n'      "$KQ_TRAN"
} > ~/lab08/bang-gioi-han.tsv
cat ~/lab08/bang-gioi-han.tsv
```

Bốn dòng vừa ghi là bốn phát biểu **của phiên bản 17.7 trên hạ tầng của mình**, không phải bốn câu trích tài liệu. Ghi kèm số hiệu phiên bản vào hiện vật, vì cả bốn đều đã đổi ít nhất một lần trong lịch sử GitLab. Dòng `needs_chu_trinh` là dòng dạy chữ **A** trong **DAG**: đồ thị **không chu trình** không phải một tính chất đẹp đẽ, nó là điều kiện để pipeline được tạo ra.

**CHECKPOINT 4 — hai cách xếp stage cho cùng một DAG có đường găng lệch ≤ 15 s và `wall` lệch ≤ 25 s; bốn phép đo giới hạn đều ghi được kết quả vào `bang-gioi-han.tsv`.**

```bash
cd ~/lab08
g4=$(awk -F'\t' '$1=="dag"{print $3}' bang-duong-gang.tsv)
g1=$(awk -F'\t' '$1=="dag-mot-stage"{print $3}' bang-duong-gang.tsv)
w4=$(awk -F'\t' '$1=="dag"{print $9}' bang-duong-gang.tsv)
w1=$(awk -F'\t' '$1=="dag-mot-stage"{print $9}' bang-duong-gang.tsv)
dg=$(awk -v a="$g4" -v b="$g1" 'BEGIN{d=a-b; print (d<0?-d:d)}')
dw=$(awk -v a="$w4" -v b="$w1" 'BEGIN{d=a-b; print (d<0?-d:d)}')
so_do=$(awk -F'\t' 'NR>1 && $2 ~ /valid/ {n++} END {print n+0}' bang-gioi-han.tsv)
tt=$(curl -sf "${H[@]}" "$A/pipelines/$P_1ST" | jq -r .status)
{ [ "$tt" = success ] && [ "$dg" -le 15 ] && [ "$dw" -le 25 ] && [ "$so_do" -eq 4 ]; } \
  && echo "CHECKPOINT 4 — ĐẠT (duong_gang 4-stage=${g4}s vs 1-stage=${g1}s lech ${dg}s · wall ${w4}s vs ${w1}s lech ${dw}s · $so_do phép đo giới hạn đã ghi)" \
  || echo "CHECKPOINT 4 — LỖI (tt=$tt, lech_gang=$dg cần ≤15, lech_wall=$dw cần ≤25, so_phep_do=$so_do cần 4 — xem §L9 dòng 10)" \
  | tee -a ~/lab08/checkpoint.log
```

### 2.4. Đo QT 4.3 — `needs` thu hẹp artifact **15 → 5**, cạnh cổng thu hẹp tiếp **5 → 2** (7 phút)

`needs` mang **hai** việc: đổi thứ tự **và** thu hẹp tập artifact tải về (buổi 05 QT 5.2 — lần thứ 2). Ta đã đo việc thứ nhất; việc thứ hai đo bằng dòng `SO_TEP_NHAN_DUOC` mà `package` và `deploy` in ra:

```bash
cd ~/lab08
dem() {   # dem <pipeline> <ten_job>
  job_log_sach "$(job_id "$1" "$2")" | grep -oE 'SO_TEP_NHAN_DUOC=[0-9]+' | head -1 | cut -d= -f2
}
echo "package tuan-tu=$(dem "$P_TT" package)  dag=$(dem "$P_DAG" package)"
echo "deploy  tuan-tu=$(dem "$P_TT" deploy)   dag=$(dem "$P_DAG" deploy)"
```

Con số kỳ vọng, và cách cộng ra chúng bằng tay để kiểm số đo:

| Job | Ca tuần tự | Cách cộng | Ca DAG trần trụi | Cách cộng |
|---|---|---|---|---|
| `package` | **14** | `ra-fe` 3 + `ra-be` 4 + `ra-lint` 1 + `ra-scan` 2 + `ra-unit` 3 + `bao-cao` 1 | **7** | `needs: [build-fe, build-be]` → 3 + 4 |
| `deploy` | **15** | 14 dòng trên + `ra-goi` 1 | **5** | `needs: [package, test-unit, test-e2e]` → 1 + 3 + 1 |

Mười trong mười lăm tệp mà `deploy` mất đi là artifact của `lint`, `scan` và hai job xây — không ai đọc chúng. Đây cũng là chỗ QT 4.3 trở thành chế độ hỏng: nếu `deploy` đang âm thầm đọc một tệp trong `ra-lint/` mà không ai nhớ, dòng `needs` vừa thêm lấy tệp đó đi **ngay lần chạy đầu**. Ở ví dụ chuẩn nó **ồn ào và có chặn** vì `deploy` có `test -s`; bỏ dòng khẳng định đó thì nó chuyển sang **im lặng** — đó là hỏng im lặng số 6 của buổi.

Bây giờ tới cạnh cổng. Trong 5 tệp `deploy` còn nhận, **3 tệp là của `test-unit`** mà `deploy` không đọc một byte nào. `needs` cho phép nói *"chờ nó, nhưng không cần tệp của nó"*, và đây là cách **duy nhất** nói được câu đó:

```yaml
# mảnh — thay khối needs một dòng của deploy trong ~/lab08/.gitlab-ci.yml
deploy:
  needs:
    - job: package                       # cạnh DỮ LIỆU — cần ra-goi/goi.txt
    - job: test-e2e                      # cạnh DỮ LIỆU — cần bao-cao/e2e.json
    - job: test-unit
      artifacts: false                   # cạnh CỔNG — chỉ cần nó xanh
```

```bash
cd ~/lab08
python3 - "$PWD/.gitlab-ci.yml" <<'PY' 2>/dev/null || perl -0pi -e \
  's/^  needs: \[package, test-unit, test-e2e\]$/  needs:\n    - job: package\n    - job: test-e2e\n    - job: test-unit\n      artifacts: false/m' .gitlab-ci.yml
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text()
t = t.replace("  needs: [package, test-unit, test-e2e]\n",
  "  needs:\n    - job: package\n    - job: test-e2e\n    - job: test-unit\n      artifacts: false\n")
p.write_text(t)
PY
grep -nA5 '^deploy:' .gitlab-ci.yml
bash ~/lab08/so-canh.sh    # vẫn phải BAN_DO=8 YAML=8 — cách viết đổi, số cạnh KHÔNG đổi
git add -A && git commit -q -m "tach canh cong: test-unit artifacts false"
git push -q -f origin HEAD:refs/heads/dag
sleep 6
P_CONG=$(curl -sf "${H[@]}" "$A/pipelines?ref=dag&per_page=1" | jq -r '.[0].id')
cho_pipeline "$P_CONG" 600
echo "deploy voi canh cong = $(dem "$P_CONG" deploy) tep"
```

```bash
cd ~/lab08
{ printf 'job\ttuan_tu\tdag_tran_trui\tdag_canh_cong\tghi_chu\n'
  printf 'package\t%s\t%s\t%s\tmac dinh moi stage truoc -> 2 job trong needs\n' \
    "$(dem "$P_TT" package)" "$(dem "$P_DAG" package)" "$(dem "$P_CONG" package)"
  printf 'deploy\t%s\t%s\t%s\t15 -> 5 -> 2: canh cong bo 3 tep cua test-unit\n' \
    "$(dem "$P_TT" deploy)" "$(dem "$P_DAG" deploy)" "$(dem "$P_CONG" deploy)"
} | tee ~/lab08/bang-artifact-08.tsv | column -t -s $'\t'
bash ~/lab08/do-duong-gang.sh "$PID" "$P_CONG" --canh canh.tsv --pha --tsv \
  | sed 's/^dag/dag-canh-cong/' >> bang-duong-gang.tsv
```

Đo cái giá bằng giây, không bằng cảm nhận — pha `download_artifacts` của `deploy` ở ba ca:

```bash
cd ~/lab08
for p in "$P_TT" "$P_DAG" "$P_CONG"; do
  id=$(job_id "$p" deploy)
  printf 'pipeline %s deploy: ' "$p"
  bash "$GO_ROI" "$PID" "$id" --pha \
    | awk -F'\t' '$2=="download_artifacts"{printf "download_artifacts=%s giay\n", $4}' \
    || echo "download_artifacts=0 giay"
done
```

Trên máy tham chiếu, pha `download_artifacts` của `deploy` đi **3 → 2 → 1** giây. Hai giây không phải lý do dùng `needs` — lý do là 90 giây ở mục 2.2. Nhưng hai giây ấy là lý do phải **kiểm** sau khi thêm `needs`: cái mất đi không phải thời gian, mà là tệp. Và trên một repo thật mà artifact xây là 180 MB thì hai giây ấy thành **25–40 giây mỗi job hạ nguồn** — nhân với số job, đó là con số đáng mang đi họp.

**CHECKPOINT 5 — `deploy` nhận đúng 15 → 5 → 2 tệp qua ba ca; `package` nhận 14 rồi 7; số cạnh trong YAML vẫn là 8 sau khi đổi cách viết.**

```bash
cd ~/lab08
pt=$(awk -F'\t' '$1=="package"{print $2}' bang-artifact-08.tsv)
pd=$(awk -F'\t' '$1=="package"{print $3}' bang-artifact-08.tsv)
d1=$(awk -F'\t' '$1=="deploy"{print $2}'  bang-artifact-08.tsv)
d2=$(awk -F'\t' '$1=="deploy"{print $3}'  bang-artifact-08.tsv)
d3=$(awk -F'\t' '$1=="deploy"{print $4}'  bang-artifact-08.tsv)
bash ~/lab08/so-canh.sh >/dev/null; kc=$?
{ [ "$pt" -eq 14 ] && [ "$pd" -eq 7 ] \
  && [ "$d1" -eq 15 ] && [ "$d2" -eq 5 ] && [ "$d3" -eq 2 ] && [ "$kc" -eq 0 ]; } \
  && echo "CHECKPOINT 5 — ĐẠT (package 14->7 tệp; deploy 15->5->2 tệp; artifacts:false trên 1 cạnh cổng bỏ 3 tệp; số cạnh YAML vẫn khớp canh.tsv)" \
  || echo "CHECKPOINT 5 — LỖI (package=${pt:-?}->${pd:-?} cần 14->7, deploy=${d1:-?}->${d2:-?}->${d3:-?} cần 15->5->2, khop_canh=$kc cần 0 — xem §L9 dòng 11, 12)" \
  | tee -a ~/lab08/checkpoint.log
```

## L5. Bước 3 — Bỏ một cạnh: pipeline **nhanh hơn và sai**; rồi `needs:optional` (25 phút)

Kiểm chứng QT 5.2, QT 5.3.

Bước 2 vừa cho một con số dễ chịu: 90 giây cắt được. Bước 3 lấy hoá đơn. Từ lúc ta bỏ hàng rào, nền tảng **thôi** bảo đảm thứ tự hộ ta — và cạnh nào ta quên khai thì job đó chạy sớm **một cách im lặng**. Đây là chế độ hỏng đặc trưng của cả buổi, và điều làm nó nguy hiểm hơn mọi ca của buổi 07 là: nó **không** có triệu chứng nào ngoài việc **nhanh hơn dự kiến**.

**Đọc trước khi làm:** vòng 1 của bước này cho một pipeline **XANH** và một kết quả **SAI**. Đó là đáp án đúng.

### 3.1. Vòng 1 — bỏ đúng cạnh `test-e2e <- build-be` (9 phút)

Tình huống thật: ai đó nhìn `test-e2e` và nghĩ *"nó test giao diện, nó chỉ cần bản build frontend"*, rồi khai `needs: [build-fe]`. Đó là khai `needs` theo **cảm nhận về thứ tự** thay vì theo **tệp** — đúng cái bẫy QT 5.1 mô tả.

Dự đoán **bằng tay trước khi chạy**, dùng chính `canh.tsv` đã có:

```bash
cd ~/lab08
grep -v $'^test-e2e\tbuild-be' canh.tsv > canh-thieu.tsv
awk -F'\t' '!/^#/ && NF>=2 {n++} END {print "so canh con lai =", n}' canh-thieu.tsv   # 7
```

```
Đường găng khi CÒN cạnh : build-be 90 -> test-e2e 120 -> deploy 25 = 235 s
Đường găng khi MẤT cạnh : build-fe 60 -> test-e2e 120 -> deploy 25 = 205 s
Hiệu phần 1 (chạy sớm hơn)     = 235 - 205 = 30 s   <- test-e2e thôi chờ build-be
Hiệu phần 2 (làm ít việc hơn)  = pha download_artifacts của test-e2e nhỏ đi
Tổng khoảng 35 s. HAI phần này phải đo RIÊNG — chúng là hai cơ chế khác nhau.
```

```bash
cd ~/lab08
git checkout -qB thieu-cang dag
sed -i 's|^  needs: \[build-fe, build-be\]$|  needs: [build-fe]|' .gitlab-ci.yml
# chỉ khối test-e2e được đổi — kiểm lại, vì package cũng có đúng dòng đó
grep -nB4 '^  needs: \[build-fe\]$' .gitlab-ci.yml
grep -c '^  needs: \[build-fe, build-be\]$' .gitlab-ci.yml    # phải còn 1 (của package)
bash ~/lab08/so-canh.sh ~/lab08/.gitlab-ci.yml ~/lab08/canh.tsv | head -4
```

Dòng `BAN_DO=8 YAML=7` cùng dòng `test-e2e	build-be` trong khối *"có trong bản đồ, THIẾU trong YAML"* là **cách duy nhất** phát hiện cạnh thiếu **trước khi** chạy. Trên repo thật, chạy `so-canh.sh` trong một job `lint-dag` là cách rẻ nhất để biến hỏng im lặng thành hỏng ồn ào — bài BT3 làm việc đó.

```bash
cd ~/lab08
git add -A && git commit -q -m "vong 1 — THIEU canh test-e2e <- build-be"
git push -q -f origin HEAD:refs/heads/thieu-cang
sleep 6
P_TC=$(curl -sf "${H[@]}" "$A/pipelines?ref=thieu-cang&per_page=1" | jq -r '.[0].id')
cho_pipeline "$P_TC" 600
bash ~/lab08/do-duong-gang.sh "$PID" "$P_TC" --canh canh-thieu.tsv --pha
bash ~/lab08/do-duong-gang.sh "$PID" "$P_TC" --canh canh-thieu.tsv --pha --tsv >> bang-duong-gang.tsv
```

Pipeline **XANH**. Đường găng **205** giây. Không một dòng log nào cảnh báo. Bây giờ đi tìm cái sai, và tìm nó ở nơi duy nhất còn dấu vết — trong **artifact**, không trong log:

```bash
cd ~/lab08
echo "--- e2e.json cua ca DAG DUNG (pipeline $P_CONG) ---"
art_tep "$(job_id "$P_CONG" test-e2e)" "bao-cao/e2e.json"
echo "--- e2e.json cua ca THIEU CANH (pipeline $P_TC) ---"
art_tep "$(job_id "$P_TC"  test-e2e)" "bao-cao/e2e.json"
echo "--- gia tri da di tiep toi deploy ---"
job_log_sach "$(job_id "$P_TC" deploy)" | grep -E 'TRIEN_KHAI_CAU_HINH|SO_TEP_NHAN_DUOC'
```

Ca đúng ghi `"cau_hinh":"<số hiệu pipeline>"`. Ca thiếu cạnh ghi `"cau_hinh":"0.0.0-mac-dinh"` — giá trị **có sẵn trong git**. `test-e2e` đã kiểm 12 luồng nghiệp vụ trên **một cấu hình không phải cấu hình của bản build này**, rồi báo 0 thất bại, rồi `deploy` mang con số đó đi triển khai. Ba job xanh liên tiếp, một kết luận sai, và tín hiệu duy nhất là **205 thay vì 235**.

Bây giờ tách hiệu 35 giây thành hai phần, mỗi phần một phép đo:

```bash
cd ~/lab08
g_dung=$(awk -F'\t' '$1=="dag-canh-cong"{print $3}' bang-duong-gang.tsv)
g_thieu=$(awk -F'\t' '$1=="thieu-cang"{print $3}'   bang-duong-gang.tsv)
echo "PHAN 1 — chay som hon: $g_dung - $g_thieu = $((g_dung - g_thieu)) giay (ky vong 30)"

pha_dl() {  # pha_dl <pipeline> <ten_job>  -> giay pha download_artifacts
  bash "$GO_ROI" "$PID" "$(job_id "$1" "$2")" --pha 2>/dev/null \
    | awk -F'\t' '$2=="download_artifacts"{print $4; exit}'; }
dl_dung=$(pha_dl "$P_CONG" test-e2e); dl_thieu=$(pha_dl "$P_TC" test-e2e)
echo "PHAN 2 — lam it viec hon: download_artifacts ${dl_dung:-0}s -> ${dl_thieu:-0}s"

{ printf 'phep_do\tgia_tri\tghi_chu\n'
  printf 'duong_gang_canh_dung\t%s\t235 giay tham chieu\n'  "$g_dung"
  printf 'duong_gang_thieu_canh\t%s\t205 giay tham chieu\n' "$g_thieu"
  printf 'phan_1_chay_som_hon\t%s\t30 giay: test-e2e thoi cho build-be 90s, chi cho build-fe 60s\n' "$((g_dung - g_thieu))"
  printf 'phan_2_download_artifacts\t%s\thieu %ss -> %ss; nho trong lab vi artifact vai KB\n' \
    "$(( ${dl_dung:-0} - ${dl_thieu:-0} ))" "${dl_dung:-0}" "${dl_thieu:-0}"
} > bang-thieu-cang.tsv
column -t -s $'\t' bang-thieu-cang.tsv
```

Phần 1 là **30 giây** và nó ổn định, vì nó thuần cấu trúc đồ thị. Phần 2 trong lab chỉ **1–5 giây** vì artifact của `build-be` chỉ vài KB; trên một repo Java thật với artifact 180 MB thì chính phần 2 là phần lớn, và khi đó "nhanh hơn dự kiến" có thể là 40–60 giây. Điều bất biến giữa hai môi trường không phải trị tuyệt đối — mà là **dấu**: pipeline nhanh hơn con số ta đã tính thì có một cạnh đang thiếu.

### 3.2. Vòng 2 và vòng 3 — hai khẳng định, một job phải đỏ, rồi vá cạnh (8 phút)

Từ giờ nền tảng không giữ thứ tự hộ ta nữa, nên mỗi job có `needs` phải tự kiểm đầu vào của mình. Hai khẳng định, hai cơ chế khác nhau:

| # | Khẳng định | Cơ chế | Có bắt được ca thiếu cạnh không |
|---|---|---|---|
| 1 | Tệp đầu vào phải mang **dấu vết pipeline này** | `build-be` ghi `$CI_PIPELINE_ID` vào `cau-hinh/app.json`; bản trong git ghi `0.0.0-mac-dinh` | **Có, luôn luôn** — chặn được, chi phí ~0,1 s |
| 2 | Tệp đầu vào phải **cũ hơn** tệp do `git checkout` tạo ra | Artifact được giải nén **giữ nguyên** mốc thời gian của job nguồn nên cũ hơn; tệp từ git checkout mới bằng thời điểm checkout | **Phải đo** — đây là loại (c), có thể đổi theo phiên bản runner |

Trước khi viết khẳng định 2, đo xem `alpine:3.20` có cờ nào dùng được không — `find -newermt` là cờ của **GNU findutils**, còn `alpine` dùng `find` của busybox:

```bash
docker run --rm alpine:3.20 sh -c 'find --help 2>&1 | grep -c newermt; find / -maxdepth 0 -newer /etc/hostname >/dev/null 2>&1; echo "ma thoat -newer = $?"'
```

Kết quả `0` cho `newermt` nghĩa là **không** có cờ đó; `-newer <tệp>` thì có. Vậy khẳng định 2 viết bằng `-newer`, và mốc so sánh là `README.md` — một tệp chắc chắn do `git checkout` tạo ra trong **chính** job này.

```yaml
# mảnh — thêm vào ĐẦU script của test-e2e trong ~/lab08/.gitlab-ci.yml
    # KHẲNG ĐỊNH 1 — dấu vết pipeline. Chặn được, và luôn đúng.
    - 'grep -q "\"$CI_PIPELINE_ID\"" cau-hinh/app.json || { echo "cau-hinh/app.json KHONG phai cua pipeline $CI_PIPELINE_ID -> THIEU CANH needs"; exit 1; }'
    # KHẲNG ĐỊNH 2 — mốc thời gian. Chỉ CẢNH BÁO, vì ta đang ĐO xem nó có phân biệt được không.
    - 'echo "MOC_README=$(stat -c %Y README.md) MOC_CAUHINH=$(stat -c %Y cau-hinh/app.json)"'
    - 'find README.md -newer cau-hinh/app.json | grep -q . && echo "MOC: cau-hinh cu hon README -> den tu ARTIFACT" || echo "MOC: cau-hinh KHONG cu hon README -> den tu GIT CHECKOUT"'
```

```bash
cd ~/lab08
# vòng 2: vẫn THIẾU cạnh, nhưng đã có hai khẳng định -> test-e2e PHẢI ĐỎ
python3 - "$PWD/.gitlab-ci.yml" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text()
kd = ('    - \'grep -q "\\"$CI_PIPELINE_ID\\"" cau-hinh/app.json || '
      '{ echo "cau-hinh/app.json KHONG phai cua pipeline $CI_PIPELINE_ID -> THIEU CANH needs"; exit 1; }\'\n'
      '    - \'echo "MOC_README=$(stat -c %Y README.md) MOC_CAUHINH=$(stat -c %Y cau-hinh/app.json)"\'\n'
      '    - \'find README.md -newer cau-hinh/app.json | grep -q . '
      '&& echo "MOC: cau-hinh cu hon README -> den tu ARTIFACT" '
      '|| echo "MOC: cau-hinh KHONG cu hon README -> den tu GIT CHECKOUT"\'\n')
moc = "test-e2e:\n  needs: [build-fe]\n  stage: kiem\n  script:\n"
t = t.replace(moc, moc + kd) if moc in t else t
p.write_text(t)
PY
grep -nA6 '^test-e2e:' .gitlab-ci.yml
git add -A && git commit -q -m "vong 2 — them hai khang dinh, van thieu canh"
git push -q -f origin HEAD:refs/heads/thieu-cang

# vòng 3: VÁ cạnh, GIỮ hai khẳng định -> phải xanh và trở lại 235 giây
git checkout -qB da-va-cang thieu-cang
sed -i 's|^  needs: \[build-fe\]$|  needs: [build-fe, build-be]|' .gitlab-ci.yml
bash ~/lab08/so-canh.sh | head -2      # phải BAN_DO=8 YAML=8
git add -A && git commit -q -m "vong 3 — va canh, giu khang dinh"
git push -q -f origin HEAD:refs/heads/da-va-cang
sleep 8
P_V2=$(curl -sf "${H[@]}" "$A/pipelines?ref=thieu-cang&per_page=1"  | jq -r '.[0].id')
P_V3=$(curl -sf "${H[@]}" "$A/pipelines?ref=da-va-cang&per_page=1" | jq -r '.[0].id')
echo "vong 2 = $P_V2 (phai DO)   vong 3 = $P_V3 (phai XANH, 235 giay)"
cho_pipeline "$P_V2" 600; cho_pipeline "$P_V3" 600
```

Hai pipeline này đẩy **cùng lúc** để tiết kiệm bốn phút. Điều đó làm `wall` và `slot_dinh` của cả hai **không dùng được** (chúng chen nhau 8 slot), nhưng `duong_gang` vẫn dùng được — nó tính trên giây pha `step_script` của từng job, và giây pha không đổi khi job phải xếp hàng. Ghi rõ điều đó vào hiện vật, vì một con số `wall` không ghi điều kiện đo là một con số không dùng lại được.

```bash
cd ~/lab08
job_bang_rong "$P_V2" | head -12
job_log_sach "$(job_id "$P_V2" test-e2e)" | grep -E 'THIEU CANH|MOC_README|^MOC:'
echo "--- vong 2: trang thai test-e2e = $(job_tt "$(job_id "$P_V2" test-e2e)") ---"
echo "--- vong 3: trang thai test-e2e = $(job_tt "$(job_id "$P_V3" test-e2e)") ---"
job_log_sach "$(job_id "$P_V3" test-e2e)" | grep -E '^MOC:|CAU_HINH_DUOC_KIEM'
bash ~/lab08/do-duong-gang.sh "$PID" "$P_V3" --canh canh.tsv --pha --tsv >> bang-duong-gang.tsv
{ printf 'khang_dinh_1_dau_vet\t%s\tchan duoc ca thieu canh\n' "$(job_tt "$(job_id "$P_V2" test-e2e)")"
  printf 'khang_dinh_2_moc_thoi_gian\t%s\tket qua do tren Runner 17.7 + alpine 3.20\n' \
    "$(job_log_sach "$(job_id "$P_V2" test-e2e)" | grep -m1 '^MOC:' | cut -c1-60)"
} >> bang-thieu-cang.tsv
column -t -s $'\t' bang-thieu-cang.tsv
```

Chi phí của hai khẳng định: so giây pha `step_script` của `test-e2e` giữa vòng 3 và ca DAG đúng ở bước 2 — cả hai đều `sleep 120`, nên hiệu chính là chi phí của ba lệnh vừa thêm. Trên máy tham chiếu hiệu là **0–1 giây**, tính tròn **0,2 giây mỗi job**. Đó là giá của việc đổi một chế độ hỏng im lặng thành một chế độ hỏng ồn ào, và nó là giá rẻ nhất trong cả khoá.

**CHECKPOINT 6 — ca thiếu cạnh xanh mà sai: `test-e2e` `success`, `e2e.json` ghi `0.0.0-mac-dinh`, đường găng 198–215 s, và hiệu phần 1 nằm trong 25–35 s.**

```bash
cd ~/lab08
tt_tc=$(job_tt "$(job_id "$P_TC" test-e2e)")
ch=$(art_tep "$(job_id "$P_TC" test-e2e)" "bao-cao/e2e.json" | sed -n 's/.*"cau_hinh":"\([^"]*\)".*/\1/p')
g_thieu=$(awk -F'\t' '$1=="thieu-cang"{print $3}' bang-duong-gang.tsv)
g_dung=$(awk -F'\t'  '$1=="dag-canh-cong"{print $3}' bang-duong-gang.tsv)
p1=$(( g_dung - g_thieu ))
tt_p=$(curl -sf "${H[@]}" "$A/pipelines/$P_TC" | jq -r .status)
{ [ "$tt_tc" = success ] && [ "$tt_p" = success ] && [ "$ch" = "0.0.0-mac-dinh" ] \
  && [ "$g_thieu" -ge 198 ] && [ "$g_thieu" -le 215 ] \
  && [ "$p1" -ge 25 ] && [ "$p1" -le 35 ]; } \
  && echo "CHECKPOINT 6 — ĐẠT (pipeline=$tt_p, test-e2e=$tt_tc, cau_hinh=$ch <- BAN CU TRONG GIT, duong_gang=${g_thieu}s tham chieu 205, phan 1 = ${p1}s tham chieu 30)" \
  || echo "CHECKPOINT 6 — LỖI (tt_pipeline=$tt_p cần success, test-e2e=$tt_tc cần success, cau_hinh=$ch cần 0.0.0-mac-dinh, gang=${g_thieu:-?} cần 198-215, phan1=$p1 cần 25-35 — xem §L9 dòng 13, 14)" \
  | tee -a ~/lab08/checkpoint.log
```

### 3.3. Đo QT 5.3 — `needs:optional` làm một cạnh **được phép không tồn tại** (8 phút)

`optional: true` nghe như một cờ cho tiện. Nó không phải: nó **đổi ô** trong bảng hai thuộc tính hỏng (buổi 01 QT 7.1 — lần thứ 8). Không có nó, `needs` trỏ một job bị `rules` loại bỏ là **lỗi tạo pipeline** — ồn ào, có chặn. Có nó, cạnh đó **biến mất** và cả nhánh phía sau chạy sớm hơn — im lặng, không chặn. Ba lần chạy, ba ô khác nhau:

```bash
cd ~/lab08
git checkout -qB do-optional main
cat > .gitlab-ci.yml <<'YML'
stages: [sinh, dung]
default: { image: alpine:3.20 }

# Job này CHỈ tồn tại trên nhánh mặc định (buổi 04 QT 6.2).
sinh-cau-hinh-phu:
  stage: sinh
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  script:
    - mkdir -p phu
    - echo "$CI_PIPELINE_ID" > phu/ma.txt
    - sleep 30
  artifacts: { paths: [phu/], expire_in: 1 hour }

mot-viec-khac:
  stage: sinh
  script: [sleep 10]

dung-phu:
  stage: dung
  needs:
    - job: sinh-cau-hinh-phu
      optional: true            # <- CỜ ĐANG ĐO
  script:
    - 'if [ -s phu/ma.txt ]; then echo "CO_CANH=1 ma=$(cat phu/ma.txt)"; else echo "CO_CANH=0 CANH DA BIEN MAT"; fi'
    - sleep 15
YML
git add -A && git commit -q -m "do needs optional"
git push -q -f origin HEAD:refs/heads/main
git push -q -f origin HEAD:refs/heads/nhanh-phu
sleep 8
P_OPT_M=$(curl -sf "${H[@]}" "$A/pipelines?ref=main&per_page=1"      | jq -r '.[0].id')
P_OPT_N=$(curl -sf "${H[@]}" "$A/pipelines?ref=nhanh-phu&per_page=1" | jq -r '.[0].id')
cho_pipeline "$P_OPT_M" 300; cho_pipeline "$P_OPT_N" 300
for p in "$P_OPT_M" "$P_OPT_N"; do
  echo "--- pipeline $p ($(curl -sf "${H[@]}" "$A/pipelines/$p" | jq -r .ref)) ---"
  job_bang_rong "$p"
  job_log_sach "$(job_id "$p" dung-phu)" | grep -E 'CO_CANH'
done
```

Lần thứ ba là **ca đối chứng phải thất bại**: bỏ `optional: true` trên nhánh mà job nguồn vắng mặt. `tao_pipe` của buổi 07 in ra cả thông báo lỗi khi pipeline **không** được tạo — đó chính là hàm cần cho ô này:

```bash
cd ~/lab08
sed -i '/optional: true/d' .gitlab-ci.yml
grep -nA3 '^  needs:' .gitlab-ci.yml
git add -A && git commit -q -m "bo optional — pipeline PHAI KHONG TAO DUOC tren nhanh-phu"
git push -q -f origin HEAD:refs/heads/nhanh-phu
sleep 4
KQ_OPT=$(tao_pipe nhanh-phu); echo "ket qua tao pipeline: $KQ_OPT"
```

```bash
cd ~/lab08
gang() { bash ~/lab08/do-duong-gang.sh "$PID" "$1" --pha \
         | awk '/^WALL_DO_DUOC/{print $2}'; }
{ printf 'ca\tnhanh\tjob_nguon\tco_canh\twall_giay\to_bang_hai_thuoc_tinh\n'
  printf 'co_optional_canh_con\tmain\tco\t1\t%s\tkhong hong\n' "$(gang "$P_OPT_M")"
  printf 'co_optional_canh_mat\tnhanh-phu\tvang (rules)\t0\t%s\tIM LANG · KHONG CHAN\n' "$(gang "$P_OPT_N")"
  printf 'khong_optional\tnhanh-phu\tvang (rules)\t-\t0\tON AO · CO CHAN: %s\n' "$(printf '%s' "$KQ_OPT" | tr '\t' ' ' | cut -c1-70)"
} > bang-optional.tsv
column -t -s $'\t' bang-optional.tsv
```

Đọc hai dòng đầu: cùng một tệp YAML, hai nhánh, `wall` chênh khoảng **30 giây** — đúng bằng thời lượng `sinh-cau-hinh-phu`. Không có gì đỏ, không có cảnh báo, và `dung-phu` in `CO_CANH=0` chỉ vì ta **cố ý** thêm dòng in đó. Trong một pipeline thật không ai in dòng đó, nên tín hiệu duy nhất lại vẫn là **nhanh hơn dự kiến**. Dòng thứ ba là ô đối lập: bỏ `optional` và nền tảng **từ chối tạo pipeline** — ồn ào và có chặn. `optional: true` chính là cái nút đổi từ ô thứ ba sang ô thứ hai, và biết mình đang đổi cái gì là toàn bộ QT 5.3.

Điều bước này **không** giải quyết được, và phải nói ra: `optional` không phải lỗi thiết kế của GitLab. Nó cần thật khi một job nguồn hợp lệ vắng mặt theo `rules` — ví dụ job build image chỉ chạy khi `Dockerfile` đổi. Cách dùng đúng là `optional: true` **cộng** một dòng khẳng định trong job đích để nó tự biết cạnh có tồn tại hay không, chứ không phải dùng `optional` để pipeline khỏi báo lỗi.

**CHECKPOINT 7 — vòng 2 có `test-e2e` `failed`; vòng 3 xanh với đường găng 228–248 s; `bang-optional.tsv` có 3 dòng và hai `wall` chênh ≥ 20 s; bỏ `optional` thì pipeline không được tạo.**

```bash
cd ~/lab08
tt_v2=$(job_tt "$(job_id "$P_V2" test-e2e)")
ly_do=$(job_json "$(job_id "$P_V2" test-e2e)" | jq -r '.failure_reason // "-"')
tt_v3=$(job_tt "$(job_id "$P_V3" test-e2e)")
g_v3=$(awk -F'\t' '$1=="da-va-cang"{print $3}' bang-duong-gang.tsv)
w_m=$(awk -F'\t' '$1=="co_optional_canh_con"{print $5}' bang-optional.tsv)
w_n=$(awk -F'\t' '$1=="co_optional_canh_mat"{print $5}' bang-optional.tsv)
dw=$(( w_m - w_n )); so_dong=$(awk 'NR>1' bang-optional.tsv | wc -l | tr -d ' ')
khong_tao=$(printf '%s' "$KQ_OPT" | grep -c 'KHONG-TAO-DUOC')
{ [ "$tt_v2" = failed ] && [ "$ly_do" = script_failure ] && [ "$tt_v3" = success ] \
  && [ "$g_v3" -ge 228 ] && [ "$g_v3" -le 248 ] \
  && [ "$so_dong" -eq 3 ] && [ "$dw" -ge 20 ] && [ "$khong_tao" -eq 1 ]; } \
  && echo "CHECKPOINT 7 — ĐẠT (vong 2 test-e2e=$tt_v2/$ly_do · vong 3=$tt_v3 duong_gang=${g_v3}s · optional: wall ${w_m}s vs ${w_n}s chenh ${dw}s · bo optional -> KHONG-TAO-DUOC)" \
  || echo "CHECKPOINT 7 — LỖI (v2=$tt_v2/$ly_do cần failed/script_failure, v3=$tt_v3 gang=${g_v3:-?} cần 228-248, so_dong=$so_dong cần 3, chenh_wall=$dw cần ≥20, khong_tao=$khong_tao cần 1 — xem §L9 dòng 15, 16)" \
  | tee -a ~/lab08/checkpoint.log
```

---

## L6. Bước 4 — `parallel` 1/2/4/8, chia việc theo `CI_NODE_INDEX`, và job gộp (35 phút)

Kiểm chứng QT 6.1, QT 6.3, QT 6.4.

Ba bước đầu đổi **hình dạng** đồ thị mà không đổi tập job. Bước này đổi **số job**, và đó là chỗ hoá đơn thay đổi: `needs` giảm chờ mà không tăng phút runner; `parallel` giảm chờ và **tăng** phút runner. Hai đại lượng, hai người trả tiền, và câu hỏi vận hành duy nhất là: đổi bao nhiêu giây chờ lấy bao nhiêu giây runner.

### 4.1. Bộ 95 tệp test và `chia-viec.sh` (7 phút)

`parallel: N` sinh N job **giống nhau như đúc**; điều duy nhất khác nhau giữa chúng là `CI_NODE_INDEX`. Việc chia việc hoàn toàn thuộc về `script` — nền tảng không biết bộ test của ta chia được theo tệp, theo thư mục, hay không chia được. Bộ test của lab là 95 tệp, mỗi tệp một giây:

```bash
cd ~/lab08
git checkout -qB do-parallel main
mkdir -p bo-test
for i in $(seq -w 1 95); do printf 'sleep 1\n' > "bo-test/test-$i.sh"; done
ls bo-test | wc -l      # 95
```

```bash
cat > ~/lab08/chia-viec.sh <<'SH'
#!/usr/bin/env bash
# chia-viec.sh — chia một danh sách tệp thành CI_NODE_TOTAL phần, in phần thứ CI_NODE_INDEX.
#
# Nạp trong job:  . ./chia-viec.sh    rồi gọi:  chia_phan bo-test '*.sh'
#
# QT 6.1: GitLab KHÔNG chia việc hộ ta. Nó nhân bản định nghĩa job và bơm ĐÚNG HAI biến.
# Khi job KHÔNG khai parallel thì hai biến đó không tồn tại — hai dòng dưới là lý do
# cùng một script chạy được ở cả hai chế độ.
: "${CI_NODE_INDEX:=1}"
: "${CI_NODE_TOTAL:=1}"

# chia_phan <thu_muc> [mau_ten] — chia vòng tròn theo số dòng, cân nhất trong các cách chia rẻ.
chia_phan() {
  local thu_muc="${1:-bo-test}" mau="${2:-*.sh}"
  find "$thu_muc" -type f -name "$mau" | LC_ALL=C sort \
  | awk -v i="$CI_NODE_INDEX" -v n="$CI_NODE_TOTAL" 'NR % n == (i % n)'
}

# chia_thong_ke <thu_muc> [mau] — in một dòng để checkpoint đọc được bằng grep
chia_thong_ke() {
  local tong so
  tong=$(find "${1:-bo-test}" -type f -name "${2:-*.sh}" | wc -l | tr -d ' ')
  so=$(chia_phan "$@" | wc -l | tr -d ' ')
  echo "PHAN=$CI_NODE_INDEX/$CI_NODE_TOTAL SO_TEST=$so TONG_TEST=$tong"
}
SH
bash -n ~/lab08/chia-viec.sh && echo "cu phap OK"

# thử ngay trên máy, không cần đợi pipeline: 95 chia 4 phải ra 24/24/24/23
for i in 1 2 3 4; do
  CI_NODE_INDEX=$i CI_NODE_TOTAL=4 bash -c '. ~/lab08/chia-viec.sh; chia_thong_ke ~/lab08/bo-test'
done
for n in 1 2 8; do
  echo "n=$n -> phan dai nhat = $(for i in $(seq 1 "$n"); do
    CI_NODE_INDEX=$i CI_NODE_TOTAL=$n bash -c '. ~/lab08/chia-viec.sh; chia_phan ~/lab08/bo-test' | wc -l
  done | sort -n | tail -1) tep"
done
```

Bảng chia phần — tính **trước**, để biết mỗi job phải mất bao nhiêu giây trước khi runner nói cho ta biết:

| `parallel` | Phần dài nhất (tệp) | Phần cố định | Thời lượng job dài nhất | Ghi chú |
|---|---|---|---|---|
| không khai (1) | **95** | 25 s | **120 s** | `CI_NODE_TOTAL` không tồn tại, script vẫn chạy |
| `2` | **48** (48/47) | 25 s | **73 s** | tham chiếu của khoá là 72 s, ứng với phép chia chẵn 95/2 = 47,5 |
| `4` | **24** (24/24/24/23) | 25 s | **49 s** | nhanh **2,45** lần, **không** phải 4 lần |
| `8` | **12** (12×7 và 11) | 25 s | **37 s** | nhanh **3,2** lần; phần dài nhất 12 so với trung bình 11,875 |

Một giây lệch ở mức `parallel: 2` là con số đáng để ý, không phải sai số: **95 không chia hết cho 2**, nên phần dài nhất luôn là `ceil(95/N)` và chính nó quyết định thời lượng nhóm. Tỉ lệ phí của phép chia không chẵn tăng theo N: ở 8 phần, ta trả cho 12 tệp trong khi trung bình chỉ 11,875. Đây là một trong hai lý do tốc độ không bao giờ tuyến tính; lý do còn lại là phần cố định 25 giây.

### 4.2. Một pipeline, hai mươi mốt job, bốn điểm đo (8 phút)

```yaml
# ~/lab08/.gitlab-ci.yml — nhánh do-parallel, thay toàn bộ
stages: [kiem, gop]

default:
  image: alpine:3.20

# ---- khuôn chung: CÓ chia việc theo CI_NODE_INDEX ----
.test-chia:
  stage: kiem
  script:
    - . ./chia-viec.sh
    # PHẦN CỐ ĐỊNH mô phỏng: phục hồi cache + tải artifact + khởi động công cụ test.
    # Nó lặp lại ĐẦY ĐỦ ở MỖI phần — đó là toàn bộ lý do chia N phần không nhanh gấp N.
    - sleep 25
    - chia_thong_ke bo-test
    - chia_phan bo-test > phan-cua-toi.txt
    - while read -r t; do sh "$t"; done < phan-cua-toi.txt
    - mkdir -p bao-cao
    - 'printf ''{"nhom":"%s","phan":%s,"tong_phan":%s,"so_test":%s}\n'' "$NHOM" "$CI_NODE_INDEX" "$CI_NODE_TOTAL" "$(wc -l < phan-cua-toi.txt | tr -d " ")" > "bao-cao/$NHOM-$CI_NODE_INDEX.json"'
    - cat "bao-cao/$NHOM-$CI_NODE_INDEX.json"
  artifacts: { paths: [bao-cao/], expire_in: 1 hour }

test-p1: { extends: .test-chia, variables: { NHOM: p1 } }
test-p2: { extends: .test-chia, variables: { NHOM: p2 }, parallel: 2 }
test-p4: { extends: .test-chia, variables: { NHOM: p4 }, parallel: 4 }
test-p8: { extends: .test-chia, variables: { NHOM: p8 }, parallel: 8 }

# ---- CA HỎNG IM LẶNG SỐ 2: parallel: 4 mà script KHÔNG chia việc ----
test-khong-chia:
  stage: kiem
  parallel: 4
  script:
    - sleep 25
    - ls bo-test/*.sh > phan-cua-toi.txt
    - 'echo "PHAN=${CI_NODE_INDEX:-1}/${CI_NODE_TOTAL:-1} SO_TEST=$(wc -l < phan-cua-toi.txt | tr -d " ") TONG_TEST=95"'
    - while read -r t; do sh "$t"; done < phan-cua-toi.txt

# ---- QT 6.4: job gộp ĐÚNG — đọc số phần từ chính báo cáo ----
gop-bao-cao:
  stage: gop
  needs: [test-p4]
  script:
    - ls -1 bao-cao/p4-*.json
    - 'SO=$(ls -1 bao-cao/p4-*.json | wc -l | tr -d " ")'
    - 'CAN=$(sed -n ''s/.*"tong_phan":\([0-9]*\).*/\1/p'' bao-cao/p4-1.json)'
    - '[ "$SO" -eq "$CAN" ] || { echo "chi co $SO/$CAN bao cao -> THIEU PHAN"; exit 1; }'
    - 'TONG=$(sed -n ''s/.*"so_test":\([0-9]*\).*/\1/p'' bao-cao/p4-*.json | tr "\n" "+" | sed "s/+$//")'
    - 'TONG=$((TONG))'
    - '[ "$TONG" -eq 95 ] || { echo "gop duoc $TONG/95 test -> bao cao KHONG day du"; exit 1; }'
    - 'MOT=$(sed -n ''s/.*"so_test":\([0-9]*\).*/\1/p'' bao-cao/p4-1.json)'
    - 'echo "GOP_XONG so_bao_cao=$SO tong_test=$TONG mot_bao_cao=$MOT phan_tram_neu_khong_gop=$((100*MOT/TONG))"'
    - mkdir -p tong-hop
    - 'printf ''{"so_bao_cao":%s,"tong_test":%s,"mot_bao_cao":%s}\n'' "$SO" "$TONG" "$MOT" > tong-hop/gop.json'
  artifacts: { paths: [tong-hop/], expire_in: 1 hour }

# ---- CA ĐỐI CHỨNG PHẢI THẤT BẠI: khẳng định so với HẰNG SỐ viết tay ----
gop-doi-chung:
  stage: gop
  needs: [test-p2]
  script:
    - 'SO=$(ls -1 bao-cao/p2-*.json | wc -l | tr -d " ")'
    - 'echo "so bao cao nhan duoc = $SO"'
    - '[ "$SO" -eq 4 ] || { echo "CHI CO $SO/4 BAO CAO -> job nay PHAI DO (QT 6.4)"; exit 1; }'
```

```bash
cd ~/lab08
# dán YAML ở trên vào ~/lab08/.gitlab-ci.yml rồi:
git add -A && git commit -q -m "bon muc parallel + khong chia viec + hai job gop"
git push -q -f origin HEAD:refs/heads/do-parallel
sleep 8
P_PAR=$(curl -sf "${H[@]}" "$A/pipelines?ref=do-parallel&per_page=1" | jq -r '.[0].id')
echo "pipeline do-parallel = $P_PAR — 21 job, khoang 300 giay wall, 1.254 giay runner"
cho_pipeline "$P_PAR" 900
job_bang_rong "$P_PAR" | head -25
```

Pipeline này **phải đỏ** ở cuối, vì `gop-doi-chung` là ca đối chứng. Mọi job khác phải xanh.

### 4.3. Đo QT 6.1 — `parallel: 4` mà không chia việc thì xảy ra gì (5 phút)

```bash
cd ~/lab08
so_test() {   # so_test <ten_nhom> -> danh sách "PHAN SO_TEST" của từng job trong nhóm
  curl -sf "${H[@]}" "$A/pipelines/$P_PAR/jobs?per_page=100" \
  | jq -r --arg n "$1" '.[] | select((.name | split(" ")[0]) == $n) | .id' \
  | while read -r id; do job_log_sach "$id" | grep -oE 'PHAN=[0-9]+/[0-9]+ SO_TEST=[0-9]+'; done
}
echo "=== test-p4 — CO chia viec ==="        ; so_test test-p4
echo "=== test-khong-chia — KHONG chia viec ==="; so_test test-khong-chia
```

Hai khối đầu ra cạnh nhau là toàn bộ QT 6.1 trong một màn hình. Nhóm `test-p4` in `SO_TEST=24`, `24`, `24`, `23` — bốn phần khác nhau, cộng lại đúng 95. Nhóm `test-khong-chia` in `SO_TEST=95` **bốn lần**: bốn job làm **cùng một việc bốn lần**, tất cả đều **xanh**, không một dòng cảnh báo nào. Đây là hỏng im lặng số 2 của buổi, và cái giá của nó là một con số:

```bash
cd ~/lab08
nhom() {  # nhom <ten> -> "so_job  giay_dai_nhat  tong_giay"
  curl -sf "${H[@]}" "$A/pipelines/$P_PAR/jobs?per_page=100" \
  | jq -r --arg n "$1" '.[] | select((.name | split(" ")[0]) == $n) | ((.duration // 0) | floor)' \
  | awk '{n++; s+=$1; if($1>m) m=$1} END {printf "%d\t%d\t%d\n", n, m, s}'
}
printf 'nhom\tso_job\tgiay_dai_nhat\tphut_runner\n'
for g in test-p1 test-p2 test-p4 test-p8 test-khong-chia; do printf '%s\t%s\n' "$g" "$(nhom "$g")"; done \
  | column -t -s $'\t'
```

`test-khong-chia` tốn khoảng **480 giây** phút runner để cho ra **đúng cùng một kết quả** với `test-p1` tốn 120 giây. Bốn lần phút runner, **0** giây chờ tiết kiệm được, và mọi job đều xanh. Trên một đội chạy 60 pipeline mỗi ngày, đó là **6 giờ runner mỗi ngày** đổ vào việc chạy lại cùng một bộ test — và không có dashboard nào báo, vì mọi thứ đều xanh.

**CHECKPOINT 8 — nhóm `test-khong-chia` có 4 job đều `SO_TEST=95` với `duration` lệch ≤ 12 s; nhóm `test-p4` có 4 job với `SO_TEST` là 24/24/24/23 cộng lại đúng 95.**

```bash
cd ~/lab08
kc=$(so_test test-khong-chia | grep -oE 'SO_TEST=[0-9]+' | cut -d= -f2 | sort -u | tr '\n' ' ')
kc_n=$(so_test test-khong-chia | wc -l | tr -d ' ')
p4=$(so_test test-p4 | grep -oE 'SO_TEST=[0-9]+' | cut -d= -f2 | sort -n | tr '\n' ',' | sed 's/,$//')
p4_tong=$(so_test test-p4 | grep -oE 'SO_TEST=[0-9]+' | cut -d= -f2 | awk '{s+=$1} END{print s+0}')
lech=$(curl -sf "${H[@]}" "$A/pipelines/$P_PAR/jobs?per_page=100" \
  | jq -r '.[] | select((.name|split(" ")[0])=="test-khong-chia") | ((.duration//0)|floor)' \
  | awk '{if(!mn||$1<mn)mn=$1; if($1>mx)mx=$1} END{print mx-mn}')
{ [ "$kc_n" -eq 4 ] && [ "$kc" = "95 " ] && [ "$lech" -le 12 ] \
  && [ "$p4" = "23,24,24,24" ] && [ "$p4_tong" -eq 95 ]; } \
  && echo "CHECKPOINT 8 — ĐẠT (test-khong-chia: 4 job deu SO_TEST=95, duration lech ${lech}s -> 4 lan CUNG MOT viec; test-p4: $p4 cong lai $p4_tong)" \
  || echo "CHECKPOINT 8 — LỖI (khong_chia so_job=$kc_n cần 4, gia_tri='$kc' cần '95 ', lech=$lech cần ≤12, p4='$p4' cần '23,24,24,24', tong=$p4_tong cần 95 — xem §L9 dòng 17)" \
  | tee -a ~/lab08/checkpoint.log
```

### 4.4. Đo QT 6.3 — bốn điểm đo, và tự tính phần cố định (8 phút)

```bash
cd ~/lab08
T1=$(nhom test-p1 | cut -f2)
{ printf 'so_phan\tgiay_dai_nhat\ttoc_do_lan\tphut_runner\ttang_runner_phan_tram\ttham_chieu\n'
  for g in test-p1 test-p2 test-p4 test-p8; do
    read -r n m s <<< "$(nhom "$g" | tr '\t' ' ')"
    case "$g" in test-p1) tc=120 ;; test-p2) tc=72 ;; test-p4) tc=49 ;; test-p8) tc=37 ;; esac
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$n" "$m" \
      "$(awk -v a="$T1" -v b="$m" 'BEGIN{printf "%.2f", (b? a/b : 0)}' | tr '.' ',')" \
      "$s" \
      "$(awk -v a="$T1" -v b="$s" 'BEGIN{printf "%+.0f", 100*(b-a)/a}')" "$tc"
  done
} > bang-parallel.tsv
column -t -s $'\t' bang-parallel.tsv
```

Bây giờ **tự tính phần cố định** từ hai điểm đo, không tra bảng. Công thức đến từ mô hình `T(N) = C + B/N`: viết nó cho `N = 1` và cho `N` bất kỳ rồi khử `B`:

```
C = (N · T(N) − T(1)) / (N − 1)
```

```bash
cd ~/lab08
T4=$(awk -F'\t' '$1==4{print $2}' bang-parallel.tsv)
T8=$(awk -F'\t' '$1==8{print $2}' bang-parallel.tsv)
C4=$(awk -v t1="$T1" -v t="$T4" 'BEGIN{printf "%.1f", (4*t - t1)/3}')
C8=$(awk -v t1="$T1" -v t="$T8" 'BEGIN{printf "%.1f", (8*t - t1)/7}')
TRAN=$(awk -v t1="$T1" -v c="$C4" 'BEGIN{printf "%.2f", (c? t1/c : 0)}')
echo "T(1)=$T1  T(4)=$T4  T(8)=$T8"
echo "phan co dinh tu cap (1,4) = $(echo "$C4" | tr '.' ',') giay"
echo "phan co dinh tu cap (1,8) = $(echo "$C8" | tr '.' ',') giay"
echo "TRAN toc do = T(1)/C = $(echo "$TRAN" | tr '.' ',') lan — du N lon bao nhieu"
{ printf 'phan_co_dinh_tu_1_4\t%s\ttham chieu 25\n' "$C4"
  printf 'phan_co_dinh_tu_1_8\t%s\ttham chieu 25\n' "$C8"
  printf 'tran_toc_do\t%s\ttham chieu 4,8 lan\n' "$TRAN"
} >> bang-parallel.tsv
```

Đọc bảng theo hai chiều, vì đây là chỗ **định lượng ngược lại** của cả buổi:

| Chiều | Con số | Kết luận vận hành |
|---|---|---|
| Chiều người ta mong | 1 → 4 phần: **120 s → 49 s**, nhanh **2,45** lần | Đáng làm: 71 giây chờ trả lại cho mỗi lập trình viên, mỗi lần chạy |
| Chiều người ta quên | 4 → 8 phần: **49 s → 37 s**, chỉ thêm **12 s**, mà phút runner **196 s → 296 s** | **Không** đáng làm: mua 12 giây chờ bằng 100 giây runner |
| Trần tuyệt đối | `T(1)/C = 120/25 = 4,8` lần | Chia 20 phần cũng không bao giờ vượt 4,8 lần; mọi phần vượt 8 là tiền đổ đi |
| Hoá đơn phút runner | 120 → 196 giây, **+63%** ở mức `parallel: 4` | Người trả tiền cho 63% này khác người nhận 71 giây kia |

Và đây là câu để nói khi ai đó đề nghị "bật `parallel: 16` cho nhanh": job có phần cố định 25 giây trên tổng 120 giây thì trần là 4,8 lần; ở `parallel: 8` ta đã lấy 3,2 trong 4,8 lần đó, tức **67%** của trần, với 296 giây runner. Mọi mức cao hơn mua phần còn lại với giá tăng dần. Job nào có phần cố định **lớn hơn** phần chia được — ví dụ job 40 giây với 30 giây khởi tạo — thì trần là 1,33 lần, và bật `parallel` cho nó là tăng phút runner thật để lấy một con số làm tròn thành không.

**CHECKPOINT 9 — bốn điểm đo đơn điệu giảm; tốc độ ở 4 phần trong 2,0–2,9 lần; phần cố định tính ngược từ hai cặp điểm đo đều nằm trong 18–32 s; phút runner ở 4 phần tăng 40–90%.**

```bash
cd ~/lab08
don_dieu=$(awk -F'\t' 'NR>1 && $1 ~ /^[0-9]+$/ {if (truoc != "" && $2+0 >= truoc+0) bad=1; truoc=$2} END{print (bad?0:1)}' bang-parallel.tsv)
so_diem=$(awk -F'\t' 'NR>1 && $1 ~ /^[0-9]+$/' bang-parallel.tsv | wc -l | tr -d ' ')
td4=$(awk -F'\t' '$1==4{print $3}' bang-parallel.tsv | tr ',' '.')
tr4=$(awk -F'\t' '$1==4{print $5}' bang-parallel.tsv | tr -d '+')
ok_td=$(awk -v x="$td4" 'BEGIN{print (x>=2.0 && x<=2.9)?1:0}')
ok_c4=$(awk -v x="$C4" 'BEGIN{print (x>=18 && x<=32)?1:0}')
ok_c8=$(awk -v x="$C8" 'BEGIN{print (x>=18 && x<=32)?1:0}')
{ [ "$so_diem" -eq 4 ] && [ "$don_dieu" -eq 1 ] && [ "$ok_td" -eq 1 ] \
  && [ "$ok_c4" -eq 1 ] && [ "$ok_c8" -eq 1 ] && [ "$tr4" -ge 40 ] && [ "$tr4" -le 90 ]; } \
  && echo "CHECKPOINT 9 — ĐẠT (4 diem do don dieu giam: ${T1}s -> $(awk -F'\t' '$1==2{print $2}' bang-parallel.tsv)s -> ${T4}s -> ${T8}s · toc do o 4 phan = $(echo "$td4"|tr '.' ',') lan (KHONG phai 4) · phan co dinh $(echo "$C4"|tr '.' ',')s va $(echo "$C8"|tr '.' ',')s · phut runner +${tr4}%)" \
  || echo "CHECKPOINT 9 — LỖI (so_diem=$so_diem cần 4, don_dieu=$don_dieu cần 1, toc_do_4=$td4 cần 2,0-2,9, C(1,4)=$C4 và C(1,8)=$C8 cần 18-32, tang_runner=${tr4}% cần 40-90 — xem §L9 dòng 18)" \
  | tee -a ~/lab08/checkpoint.log
```

### 4.5. Đo QT 6.4 — N báo cáo rời, và cái giá của việc thiếu job gộp (7 phút)

N job song song sinh **N** báo cáo rời. Nếu không có **một** job gộp thì mọi thứ đọc báo cáo — coverage, số test, gate chất lượng — chỉ thấy **1/N** sự thật. Con số vẫn hiện ra; nó chỉ sai.

```bash
cd ~/lab08
echo "--- bon bao cao roi cua nhom test-p4 ---"
for i in 1 2 3 4; do art_tep "$(job_id "$P_PAR" "test-p4 $i/4")" "bao-cao/p4-$i.json"; done
echo "--- ket qua job gop ---"
job_log_sach "$(job_id "$P_PAR" gop-bao-cao)" | grep -E 'GOP_XONG'
art_tep "$(job_id "$P_PAR" gop-bao-cao)" "tong-hop/gop.json"
```

Dòng `GOP_XONG` in cả `phan_tram_neu_khong_gop`. Đọc nó: một gate đọc **một** báo cáo thấy **24/95 = 25%**; sự thật là **95/95 = 100%**. Tỉ số 25/100 gần đúng **1/4**, đúng lớp lỗi mà QT 6.4 mô tả bằng ví dụ coverage tụt từ 82% xuống 21%. Điều đáng sợ không phải con số sai — mà là nó **hợp lý**: 25% coverage là một con số tin được, không ai nghi ngờ, và nếu gate đặt ở 20% thì nó còn **mở cửa** cho commit đi qua.

```bash
cd ~/lab08
mot=$(art_tep "$(job_id "$P_PAR" gop-bao-cao)" "tong-hop/gop.json" | sed -n 's/.*"mot_bao_cao":\([0-9]*\).*/\1/p')
tong=$(art_tep "$(job_id "$P_PAR" gop-bao-cao)" "tong-hop/gop.json" | sed -n 's/.*"tong_test":\([0-9]*\).*/\1/p')
echo "mot bao cao = $mot / $tong = $(awk -v a="$mot" -v b="$tong" 'BEGIN{printf "%.1f", 100*a/b}' | tr '.' ',')% <- con so mot gate se doc neu khong gop"
echo "ti so voi 1/4 = $(awk -v a="$mot" -v b="$tong" 'BEGIN{printf "%.2f", (a/b)/0.25}' | tr '.' ',')"
echo "gia cua job gop = $(nhom gop-bao-cao | cut -f2) giay moi pipeline"
```

Ca đối chứng — `gop-doi-chung` khai `[ "$SO" -eq 4 ]` bằng một **hằng số viết tay** trong khi nhóm nguồn có 2 phần:

```bash
cd ~/lab08
echo "gop-doi-chung: $(job_tt "$(job_id "$P_PAR" gop-doi-chung)") / $(job_json "$(job_id "$P_PAR" gop-doi-chung)" | jq -r .failure_reason)"
job_log_sach "$(job_id "$P_PAR" gop-doi-chung)" | grep -E 'so bao cao|PHAI DO'
echo "gop-bao-cao : $(job_tt "$(job_id "$P_PAR" gop-bao-cao)")"
```

Hai job gộp, cùng một khẳng định về **số phần**, hai kết quả — và khác biệt duy nhất giữa chúng là nguồn của con số kỳ vọng. `gop-bao-cao` đọc `tong_phan` từ **chính báo cáo**, nên nó đúng khi ai đó đổi `parallel: 4` thành `parallel: 6` ngày mai. `gop-doi-chung` so với hằng số `4`, nên nó đỏ ngay lần đầu. Đây là quy tắc rút ra được và mang đi dùng: **khẳng định về số phần phải lấy số kỳ vọng từ `CI_NODE_TOTAL`, không từ một hằng số trong YAML.**

Cái giá bắt buộc của `parallel`, ghi bằng số: job gộp tốn **~8 giây** mỗi pipeline. Nó không phải tuỳ chọn — không có nó thì mọi chỉ số chất lượng của pipeline sai theo hệ số `1/N`, và sai theo hướng **dễ dãi hơn**.

**CHECKPOINT 10 — `gop-bao-cao` xanh với `tong_test = 95` từ 4 báo cáo; `gop-doi-chung` `failed`; tỉ số "một báo cáo / tổng" nằm trong 0,22–0,28; job gộp tốn ≤ 20 s.**

```bash
cd ~/lab08
tt_g=$(job_tt "$(job_id "$P_PAR" gop-bao-cao)")
tt_d=$(job_tt "$(job_id "$P_PAR" gop-doi-chung)")
gop=$(art_tep "$(job_id "$P_PAR" gop-bao-cao)" "tong-hop/gop.json")
so_bc=$(printf '%s' "$gop" | sed -n 's/.*"so_bao_cao":\([0-9]*\).*/\1/p')
tong=$(printf  '%s' "$gop" | sed -n 's/.*"tong_test":\([0-9]*\).*/\1/p')
mot=$(printf   '%s' "$gop" | sed -n 's/.*"mot_bao_cao":\([0-9]*\).*/\1/p')
ti=$(awk -v a="$mot" -v b="$tong" 'BEGIN{printf "%.3f", a/b}')
ok_ti=$(awk -v x="$ti" 'BEGIN{print (x>=0.22 && x<=0.28)?1:0}')
gia=$(nhom gop-bao-cao | cut -f2)
{ [ "$tt_g" = success ] && [ "$tt_d" = failed ] && [ "$so_bc" -eq 4 ] \
  && [ "$tong" -eq 95 ] && [ "$ok_ti" -eq 1 ] && [ "$gia" -le 20 ]; } \
  && echo "CHECKPOINT 10 — ĐẠT (gop-bao-cao=$tt_g: $so_bc bao cao -> tong_test=$tong · mot bao cao = $mot/$tong = $(echo "$ti"|tr '.' ',') xap xi 1/4 · gop-doi-chung=$tt_d dung nhu du bao · gia job gop=${gia}s)" \
  || echo "CHECKPOINT 10 — LỖI (gop=$tt_g cần success, doi_chung=$tt_d cần failed, so_bao_cao=$so_bc cần 4, tong=$tong cần 95, ti_so=$ti cần 0,22-0,28, gia=${gia}s cần ≤20 — xem §L9 dòng 19)" \
  | tee -a ~/lab08/checkpoint.log
```

---

## L7. Bước 5 — `matrix`, trần slot runner, và hợp đồng liên project (20 phút)

Kiểm chứng QT 6.2, QT 7.1, QT 7.2.

### 5.1. Đo QT 6.2 — matrix nhân lên, không cộng vào (7 phút)

```bash
cd ~/lab08
git checkout -qB do-matrix main
cat > .gitlab-ci.yml <<'YML'
stages: [kiem]
default: { image: alpine:3.20 }

kiem-tuong-thich:
  stage: kiem
  parallel:
    matrix:
      - PHIEN_BAN: ["18", "20", "22"]
        HE: ["alpine", "debian"]
  script:
    - echo "kiem tren node $PHIEN_BAN / $HE — job $CI_NODE_INDEX/$CI_NODE_TOTAL"
    - sleep 8
YML
git add -A && git commit -q -m "matrix 3 x 2"
git push -q -f origin HEAD:refs/heads/do-matrix
sleep 8
P_M1=$(curl -sf "${H[@]}" "$A/pipelines?ref=do-matrix&per_page=1" | jq -r '.[0].id')
cho_pipeline "$P_M1" 300
curl -sf "${H[@]}" "$A/pipelines/$P_M1/jobs?per_page=100" | jq -r '.[].name' | sort
SO_M1=$(curl -sf "${H[@]}" "$A/pipelines/$P_M1/jobs?per_page=100" | jq length)
echo "3 x 2 -> $SO_M1 job"
```

Tên job sinh ra có dạng `kiem-tuong-thich: [18, alpine]` — nền tảng đặt tên bằng **tổ hợp giá trị**, không bằng chỉ số, và đó là lý do thêm một giá trị làm **đổi tên** nhiều job cùng lúc (điều này phá vỡ mọi thứ trỏ tới job theo tên: `needs`, `rules`, quy tắc bảo vệ nhánh, dashboard). Bây giờ thêm **một** giá trị vào **một** biến:

```bash
cd ~/lab08
sed -i 's|PHIEN_BAN: \["18", "20", "22"\]|PHIEN_BAN: ["18", "20", "22", "24"]|' .gitlab-ci.yml
git add -A && git commit -q -m "them MOT phien ban vao matrix"
git push -q -f origin HEAD:refs/heads/do-matrix
sleep 8
P_M2=$(curl -sf "${H[@]}" "$A/pipelines?ref=do-matrix&per_page=1" | jq -r '.[0].id')
cho_pipeline "$P_M2" 300
SO_M2=$(curl -sf "${H[@]}" "$A/pipelines/$P_M2/jobs?per_page=100" | jq length)
echo "4 x 2 -> $SO_M2 job   (them 1 gia tri -> them $((SO_M2 - SO_M1)) job)"
```

Một giá trị thêm vào, **hai** job thêm ra — vì số job tăng theo **tích của các biến còn lại**, không theo phép cộng. Với ba biến `3 × 2 × 4 = 24` job thì thêm một giá trị vào biến đầu là **+8** job. Đây là công thức phải nói ra trong buổi họp trước khi ai đó thêm một phiên bản Node: *"thêm một giá trị vào biến này làm số job tăng thêm bằng tích của các biến còn lại"*.

Trần **200** job của một khối matrix — đo bằng `ci/lint`, không tra tài liệu, vì đo mất một giây và không tốn phút runner nào:

```bash
cd ~/lab08
awk 'BEGIN{
  print "stages: [mot]"; print "default: { image: alpine:3.20 }"
  print "qua-tran:"; print "  stage: mot"; print "  parallel:"; print "    matrix:"
  printf "      - A: ["; for(i=1;i<=21;i++) printf "%s\"a%d\"", (i>1?", ":""), i; print "]"
  printf "        B: ["; for(i=1;i<=11;i++) printf "%s\"b%d\"", (i>1?", ":""), i; print "]"
  print "  script: [echo x]"
}' > /tmp/qua-tran.yml
lint_kq() { curl -sf "${H[@]}" --request POST --header 'Content-Type: application/json' \
  --data "$(jq -n --arg c "$(cat "$1")" '{content:$c}')" "$A/ci/lint" | jq -c '{valid, errors}'; }
echo "matrix 21 x 11 = 231 job -> $(lint_kq /tmp/qua-tran.yml)"

printf 'stages: [mot]\ndefault: { image: alpine:3.20 }\nj: { stage: mot, parallel: 201, script: [echo x] }\n' > /tmp/qua-tran-par.yml
echo "parallel: 201 -> $(lint_kq /tmp/qua-tran-par.yml)"
printf 'stages: [mot]\ndefault: { image: alpine:3.20 }\nj: { stage: mot, parallel: 1, script: [echo x] }\n' > /tmp/par-1.yml
echo "parallel: 1   -> $(lint_kq /tmp/par-1.yml)"

{ printf 'matrix_231_job\t%s\t17.7\n'  "$(lint_kq /tmp/qua-tran.yml)"
  printf 'parallel_201\t%s\t17.7\n'    "$(lint_kq /tmp/qua-tran-par.yml)"
  printf 'parallel_1\t%s\t17.7\n'      "$(lint_kq /tmp/par-1.yml)"
} >> bang-gioi-han.tsv
column -t -s $'\t' bang-gioi-han.tsv
```

### 5.2. Đo QT 7.1 — DAG đổi thời gian chờ thành **slot runner** (7 phút)

`needs` không sinh ra máy. Nó cho phép chạy song song; runner mới là chỗ có tài nguyên. Trần slot là `min(concurrent, limit)` của buổi 02 QT 6.1 — lần thứ 2 của nguyên lý đó. Ta đã có sẵn hai bộ dữ liệu để đo, không cần chạy gì thêm:

```bash
cd ~/lab08
echo "=== DAG 8 job — dinh slot va tong cho ==="
awk -F'\t' 'NR==1 || $1 ~ /^(tuan-tu|dag|dag-canh-cong)$/ {print $1"\t"$7"\t"$8"\t"$9}' bang-duong-gang.tsv \
  | column -t -s $'\t'
echo "=== pipeline parallel 21 job — dinh slot va tong cho ==="
bash ~/lab08/do-duong-gang.sh "$PID" "$P_PAR" --pha | grep -E '^(SLOT_DINH|TONG_QUEUED|WALL)'
```

Hai bộ số cho hai kết luận trái ngược, và cả hai đều đúng:

- DAG 8 job: `SLOT_DINH = 4`, `TONG_QUEUED_DURATION` gần **0**. Đồ thị chỉ cần 4 slot ở đỉnh, runner có 8, nên **toàn bộ** 90 giây tiết kiệm được là thật.
- Pipeline 21 job: `SLOT_DINH = 8` — chạm trần `concurrent` — và `TONG_QUEUED_DURATION` lên tới hàng nghìn giây. Ở đây thời gian không mất đi trong job, nó nằm trong **hàng đợi**; và đó là lý do `duration` của từng job vẫn dùng được để so sánh trong khi `wall` thì không.

Đây là chế độ hỏng im lặng số 5, và nó nguy hiểm vì kết luận sai rất tự nhiên: *"chuyển sang DAG rồi mà chẳng nhanh hơn, `needs` vô dụng"*. Cách phân biệt là **một** con số: nếu `TONG_QUEUED_DURATION` tăng lên xấp xỉ bằng phần thời gian tưởng là tiết kiệm được, thì vấn đề là **slot**, không phải `needs`.

**Phần tuỳ chọn — hạ `concurrent` xuống 2.** Đây là hạ tầng dùng chung; chỉ làm nếu đã sao lưu ở §L1 dòng 13, và §L8.1 **bắt buộc** khôi phục. Trên lớp đông người, chỉ giảng viên chạy:

```bash
# TUỲ CHỌN — đụng hạ tầng dùng chung. Bỏ qua được, xem đường B ở §L9 dòng 20.
docker exec lab-runner sh -c 'sed -i "s/^concurrent = .*/concurrent = 2/" /etc/gitlab-runner/config.toml'
docker exec lab-runner sh -c 'grep -E "^concurrent" /etc/gitlab-runner/config.toml'
docker restart lab-runner >/dev/null && sleep 20
P_C2=$(tao_pipe dag); echo "chay lai DAG voi concurrent=2 -> $P_C2"
cho_pipeline "$P_C2" 900
bash ~/lab08/do-duong-gang.sh "$PID" "$P_C2" --canh ~/lab08/canh.tsv --pha \
  | grep -E '^(DUONG_GANG|WALL_DO_DUOC|SLOT_DINH|TONG_QUEUED)'
bash ~/lab08/do-duong-gang.sh "$PID" "$P_C2" --canh ~/lab08/canh.tsv --pha --tsv \
  | sed 's/^dag/dag-concurrent-2/' >> ~/lab08/bang-duong-gang.tsv
```

Con số phải thấy: `DUONG_GANG_LY_THUYET` **không đổi** — vẫn 235, vì đồ thị không đổi — nhưng `WALL_DO_DUOC` lên khoảng **300 giây** và `SLOT_DINH` rơi xuống **2**. Đường găng là một tính chất của **đồ thị**; thời gian thật là tính chất của **đồ thị cộng tài nguyên**. Với 2 slot, sàn tuyệt đối của 540 giây công việc là 270 giây, nên 235 giây là điều **không thể đạt** dù `needs` viết hoàn hảo. Ai bỏ phần này thì ghi dòng `dag-concurrent-2` là `-` và ghi lý do vào hiện vật; con số `SLOT_DINH = 4` của DAG cùng `TONG_QUEUED_DURATION` của pipeline 21 job đã đủ để kết luận.

### 5.3. Đo QT 7.2 — hợp đồng liên project, làm được trên GitLab CE (6 phút)

Cạnh phụ thuộc đi xuyên biên giới project cũng đi xuyên biên giới **quyền sở hữu**: không có gì trong project ta ngăn đội kia đổi tên job hay bỏ artifact. Đây là quyết định tổ chức, không chỉ là dòng cấu hình.

Dựng project nguồn — đây là "đội kia":

```bash
mkdir -p ~/lab08/goi-chung && cd ~/lab08/goi-chung
git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$A_GC" | jq -r .path_with_namespace).git"
git config user.email "doikia@lab.local"; git config user.name "doi kia"
cat > .gitlab-ci.yml <<'YML'
stages: [dong-goi]
dong-goi-chung:
  stage: dong-goi
  image: alpine:3.20
  script:
    - mkdir -p goi-chung
    - 'printf "thu-vien v1.4.2 pipeline=%s\n" "$CI_PIPELINE_ID" > goi-chung/thu-vien.txt'
    - sleep 10
  artifacts: { paths: [goi-chung/], expire_in: 1 day }
YML
echo "# goi chung cua doi kia" > README.md
git add -A && git commit -q -m "dong goi thu vien chung"
git push -q -u origin main
sleep 8
P_GC=$(curl -sf "${H[@]}" "$A_GC/pipelines?ref=main&per_page=1" | jq -r '.[0].id')
cho_pipeline "$P_GC" 300
curl -s -o /dev/null -w 'HTTP tai artifact theo ten job dung: %{http_code}\n' \
  "${H[@]}" "$A_GC/jobs/artifacts/main/download?job=dong-goi-chung"
curl -s -o /dev/null -w 'HTTP tai artifact theo ten job SAI : %{http_code}\n' \
  "${H[@]}" "$A_GC/jobs/artifacts/main/download?job=dong-goi-chung-v2"
```

Hai mã HTTP `200` và `404` là **toàn bộ** hợp đồng liên project gói trong hai lệnh. Bây giờ dùng nó trong một job của `lab08-dag`. Trên GitLab CE, đường chính là gọi API artifact bằng `JOB-TOKEN` — token này GitLab tự cấp cho từng job và tự thu hồi khi job kết thúc, nên không phải quản lý bí mật nào (buổi 06):

```bash
cd ~/lab08
git checkout -qB do-lien-project dag
cat > .gitlab-ci.yml <<'YML'
stages: [kiem]
default: { image: alpine:3.20 }

dung-thu-vien:
  stage: kiem
  variables:
    # BA KHOẢN CỦA HỢP ĐỒNG — cả ba đều nằm trong tay ĐỘI KIA
    GC_ID:  "THAY-BANG-PID-GC"      # 1. project + ref
    GC_REF: "main"
    GC_JOB: "dong-goi-chung"        # 2. tên job
    GC_TEP: "goi-chung/thu-vien.txt" # 3. đường dẫn tệp trong artifact
  script:
    - 'wget -q --header="JOB-TOKEN: $CI_JOB_TOKEN" -O goi.zip "$CI_API_V4_URL/projects/$GC_ID/jobs/artifacts/$GC_REF/download?job=$GC_JOB" || { echo "KHONG TAI DUOC artifact cua $GC_JOB tren ref $GC_REF -> HOP DONG BI PHA (khoan 1 hoac 2)"; exit 1; }'
    - unzip -o -q goi.zip
    - 'test -s "$GC_TEP" || { echo "artifact tai duoc nhung KHONG co $GC_TEP -> HOP DONG BI PHA (khoan 3)"; exit 1; }'
    - cat "$GC_TEP"
    - echo "HOP_DONG_OK $GC_JOB@$GC_REF -> $GC_TEP"
YML
sed -i "s|THAY-BANG-PID-GC|$PID_GC|" .gitlab-ci.yml
git add -A && git commit -q -m "lay artifact project khac qua API — duong GitLab CE"
git push -q -f origin HEAD:refs/heads/do-lien-project
sleep 8
P_LP=$(curl -sf "${H[@]}" "$A/pipelines?ref=do-lien-project&per_page=1" | jq -r '.[0].id')
cho_pipeline "$P_LP" 300
job_log_sach "$(job_id "$P_LP" dung-thu-vien)" | grep -E 'thu-vien|HOP_DONG_OK'
```

Bây giờ **đội kia đổi tên job** — không ai hỏi ta, và commit gần nhất của repo ta không liên quan gì:

```bash
cd ~/lab08/goi-chung
sed -i 's/^dong-goi-chung:/dong-goi-chung-v2:/' .gitlab-ci.yml
git add -A && git commit -q -m "doi ten job — doi kia khong hoi ai"
git push -q origin main
sleep 8
cho_pipeline "$(curl -sf "${H[@]}" "$A_GC/pipelines?ref=main&per_page=1" | jq -r '.[0].id')" 300

cd ~/lab08
P_LP2=$(tao_pipe do-lien-project); cho_pipeline "$P_LP2" 300
TT_LP2=$(job_tt "$(job_id "$P_LP2" dung-thu-vien)")
echo "sau khi doi kia doi ten job: dung-thu-vien = $TT_LP2"
job_log_sach "$(job_id "$P_LP2" dung-thu-vien)" | grep -E 'HOP DONG BI PHA'
```

```bash
cd ~/lab08
cat > hop-dong-lien-project.md <<MD
# Hợp đồng liên project — buổi 08 QT 7.2
Đo trên GitLab CE 17.7 · Runner 17.7. Project nguồn: lab08-goi-chung (id $PID_GC).

Một cạnh liên project là **một hợp đồng ba khoản** giữa hai đội. Cả ba khoản nằm trong
tay đội kia, và không có gì trong repo của ta ngăn họ đổi:

| # | Khoản | Ai đổi được | Ta phát hiện bằng |
|---|---|---|---|
| 1 | Đường dẫn project + \`ref\` | đội kia (đổi tên project, đổi nhánh mặc định) | HTTP **404** khi tải artifact |
| 2 | **Tên job** sinh artifact | đội kia | HTTP **404** — đã đo: đổi tên job thì job của ta chuyển \`$TT_LP2\` |
| 3 | Đường dẫn tệp trong artifact | đội kia | tải được nhưng \`test -s\` đỏ |

Số đo: tên job đúng -> HTTP 200; tên job sai -> HTTP **404**; job của ta -> **$TT_LP2**,
với dòng log "HOP DONG BI PHA" chỉ rõ khoản nào bị phá.

Điều kiện tôi đặt ra trước khi dùng một cạnh liên project:
1. Tên job và đường dẫn artifact được ghi thành văn bản ở phía đội kia, không phải quy ước miệng.
2. Job của ta có khẳng định riêng cho từng khoản, để lỗi chỉ ra khoản nào bị phá (đã có, ba dòng).
3. Có \`ref\` cố định hoặc tag, không trỏ nhánh đang phát triển.
4. Có người tên tuổi ở đội kia nhận là chủ hợp đồng — buổi 09 và 44 mới cho cách làm việc này an toàn ở quy mô.
MD
head -20 hop-dong-lien-project.md
```

> **Nếu có Ultimate:** GitLab bậc trả tiền có `needs:project`, khai thẳng trong YAML:
> ```yaml
> dung-thu-vien:
>   needs:
>     - project: nhom/lab08-goi-chung
>       ref: main
>       job: dong-goi-chung
>       artifacts: true
> ```
> Nó gọn hơn ba dòng `wget`/`unzip`/`test -s` ở trên, nhưng **không đổi** một chữ nào trong luận điểm tổ chức: vẫn đúng ba khoản, vẫn nằm trong tay đội kia. Khác biệt về vận hành là **thời điểm** báo lỗi — `needs:project` sai làm **pipeline không được tạo** (ồn ào, có chặn, phát hiện sớm hơn), còn đường API làm **job đỏ** (cũng ồn ào, cũng có chặn, nhưng sau khi đã tiêu phút runner của các job trước). Bài lab **không** phụ thuộc vào nó. Muốn biết GitLab của lớp có nhận `needs:project` hay không thì đo, đừng tra:
> ```bash
> printf 'stages: [mot]\ndefault: { image: alpine:3.20 }\nj:\n  stage: mot\n  needs:\n    - project: %s\n      ref: main\n      job: dong-goi-chung\n      artifacts: true\n  script: [echo x]\n' \
>   "$(curl -sf "${H[@]}" "$A_GC" | jq -r .path_with_namespace)" > /tmp/thu-needs-project.yml
> curl -sf "${H[@]}" --request POST --header 'Content-Type: application/json' \
>   --data "$(jq -n --arg c "$(cat /tmp/thu-needs-project.yml)" '{content:$c}')" \
>   "$A/ci/lint" | jq -c '{valid, errors}' \
>   | tee -a /dev/stderr >> ~/lab08/bang-gioi-han.tsv
> ```

**CHECKPOINT 11 — matrix 3 × 2 cho 6 job và 4 × 2 cho 8 job; `SLOT_DINH` của DAG bằng 4; tải artifact project khác cho HTTP 200 rồi 404 sau khi đội kia đổi tên job, và job `dung-thu-vien` chuyển từ `success` sang `failed`.**

```bash
cd ~/lab08
m1=$(curl -sf "${H[@]}" "$A/pipelines/$P_M1/jobs?per_page=100" | jq length)
m2=$(curl -sf "${H[@]}" "$A/pipelines/$P_M2/jobs?per_page=100" | jq length)
slot=$(awk -F'\t' '$1=="dag-canh-cong"{print $7}' bang-duong-gang.tsv)
h_dung=$(curl -s -o /dev/null -w '%{http_code}' "${H[@]}" "$A_GC/jobs/artifacts/main/download?job=dong-goi-chung")
h_sai=$(curl  -s -o /dev/null -w '%{http_code}' "${H[@]}" "$A_GC/jobs/artifacts/main/download?job=khong-he-co-job-nay")
tt1=$(job_tt "$(job_id "$P_LP"  dung-thu-vien)")
tt2=$(job_tt "$(job_id "$P_LP2" dung-thu-vien)")
pha=$(job_log_sach "$(job_id "$P_LP2" dung-thu-vien)" | grep -c 'HOP DONG BI PHA')
{ [ "$m1" -eq 6 ] && [ "$m2" -eq 8 ] && [ "$slot" -eq 4 ] \
  && [ "$h_dung" = 200 ] && [ "$h_sai" = 404 ] \
  && [ "$tt1" = success ] && [ "$tt2" = failed ] && [ "$pha" -ge 1 ] \
  && [ -s hop-dong-lien-project.md ]; } \
  && echo "CHECKPOINT 11 — ĐẠT (matrix 3x2=$m1 job -> 4x2=$m2 job, them 1 gia tri = +$((m2-m1)) job · SLOT_DINH cua DAG = $slot · artifact lien project: ten dung=$h_dung ten sai=$h_sai · dung-thu-vien $tt1 -> $tt2 voi $pha dong chi ro khoan bi pha)" \
  || echo "CHECKPOINT 11 — LỖI (matrix=$m1/$m2 cần 6/8, slot=${slot:-?} cần 4, http=$h_dung/$h_sai cần 200/404, job=$tt1/$tt2 cần success/failed, dong_pha=$pha cần ≥1 — xem §L9 dòng 21, 22)" \
  | tee -a ~/lab08/checkpoint.log
```

## L8. Nộp sản phẩm và dọn dẹp (10 phút)

### L8.1. Khôi phục cấu hình runner (nếu có làm phần tuỳ chọn ở §L7.2)

```bash
if docker exec lab-runner test -f /etc/gitlab-runner/config.toml 2>/dev/null; then
  docker exec lab-runner sh -c 'sed -i "s/^concurrent = .*/concurrent = 8/" /etc/gitlab-runner/config.toml'
  docker restart lab-runner >/dev/null && sleep 5
fi
```

### L8.2. Kiểm định hiện vật tổng hợp

```bash
cat > ~/lab08/kiem-hien-vat.sh <<'SH'
#!/usr/bin/env bash
set -uo pipefail
D="$HOME/lab08"
loi=0
bao() { if [ "$1" -eq 0 ]; then echo "  ĐẠT   $2"; else echo "  LỖI   $2"; loi=$((loi+1)); fi; }

echo "=== KIỂM TRA HIỆN VẬT LAB 08 ==="
for f in ban-do-phu-thuoc.md do-duong-gang.sh bang-duong-gang.tsv bang-parallel.tsv bang-gioi-han.tsv hop-dong-lien-project.md checkpoint.log; do
  [ -s "$D/$f" ]; bao $? "có $f và khác rỗng"
done

[ "$(grep -c 'ĐẠT' "$D/checkpoint.log")" -ge 11 ]
bao $? "checkpoint.log có đủ 11 dòng ĐẠT"

echo "---"
[ "$loi" -eq 0 ] && echo "CHECKPOINT 12 — ĐẠT (mọi hiện vật hợp lệ)" || echo "CHECKPOINT 12 — LỖI ($loi lỗi)"
exit "$loi"
SH
bash ~/lab08/kiem-hien-vat.sh | tee -a ~/lab08/checkpoint.log
```

**CHECKPOINT 12 — mọi hiện vật hợp lệ về NỘI DUNG, và hạ tầng dùng chung đã trả về nguyên trạng.**

---

## L9. Xử lý sự cố thường gặp trong lab

| # | Triệu chứng | Nguyên nhân | Cách khắc phục |
|---|---|---|---|
| 1 | `do-duong-gang.sh` báo không tìm thấy job | ID pipeline hoặc ID project sai, hoặc token hết hạn | Kiểm tra lại `$PID` và `$P_DAG` bằng lệnh `curl` |
| 2 | DAG chạy chậm hơn dự kiến | Slot runner bị nghẽn (`concurrent` thấp) | Kiểm tra `SLOT_DINH` và `TONG_QUEUED_DURATION` |
| 3 | `needs` báo lỗi tạo pipeline | Job nguồn không tồn tại hoặc bị `rules` loại bỏ | Dùng `optional: true` hoặc điều chỉnh `rules` |
| 4 | Matrix sinh quá 200 job | Tổ hợp biến nhân lên quá trần cho phép của GitLab | Rút gọn mảng giá trị của matrix |
| 5 | Gộp báo cáo bị sai tỉ lệ | Đọc từ hằng số cứng thay vì `CI_NODE_TOTAL` | Dùng `CI_NODE_TOTAL` làm mốc kỳ vọng |

---

## L10. Bài tập mở rộng

**BT1 — Tối ưu pipeline thật.** Vẽ DAG cho một pipeline 10 job thực tế và đo thời gian giảm được.

**BT2 — Đo trần slot.** Giới hạn slot runner và vẽ biểu đồ đường găng lý thuyết so với thực tế.

**BT3 — Matrix đa nền tảng.** Xây dựng matrix test cho 3 phiên bản Node x 2 hệ điều hành.

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| # | Hiện vật | Điểm | Tiêu chí đạt điểm tối đa |
|---|---|---|---|
| 1 | `do-duong-gang.sh` | 30 | Tính chính xác đường găng và thời gian chờ |
| 2 | `bang-duong-gang.tsv` | 25 | Đầy đủ dữ liệu so sánh tuần tự vs DAG |
| 3 | `bang-parallel.tsv` | 20 | Đo chính xác hiệu năng song song |
| 4 | `hop-dong-lien-project.md` | 15 | Phân tích đủ 3 khoản hợp đồng |
| 5 | `checkpoint.log` | 10 | Đủ 12 mốc CHECKPOINT ĐẠT |
| | **Tổng** | **100** | |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| L1–L2 | Điều kiện tiên quyết và kiến trúc | — |
| L3 | Bước 1 — Đo đường găng tuần tự | 30' |
| L4 | Bước 2 — Chuyển sang DAG | 35' |
| L5 | Bước 3 — Chống bẫy DAG | 35' |
| L6 | Bước 4 — `parallel` và `matrix` | 30' |
| L7 | Bước 5 — Trần slot và hợp đồng liên project | 20' |
| L8 | Nộp sản phẩm và dọn dẹp | 10' |
| **Tổng** | | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---



**Quy tắc cho giảng viên:**

- Chọn **5–7 câu** trong 12, ưu tiên câu 🔥. Trả lời **bằng miệng, không nhìn tài liệu**. **Gọi ngẫu nhiên**; ai thiếu thì gọi người kế tiếp bổ sung.
- Buổi này thêm một câu chen vào, theo học viên tới hết khoá: **"cái đó giảm thời gian CHỜ hay giảm PHÚT RUNNER?"** Hai đại lượng, hai người trả tiền. Ai còn đáp "`needs` làm pipeline rẻ hơn" thì chưa qua được buổi 08.
- Câu **2**, **7**, **10** là câu **tính toán**: buộc thí sinh nói ra một con số. "Tuỳ trường hợp" mà không kèm phép tính nào thì tối đa **1 điểm**, dù cơ chế đúng.
- Câu **6** hỏi ngược — thí sinh được đưa một tin có vẻ tốt. Giảng viên **không** gợi ý gì và chờ xem thí sinh có tự đặt dấu hỏi hay không.

**Thang điểm mỗi câu:** 0 = không trả lời được hoặc sai cơ chế · 1 = nhắc được tên khái niệm · 2 = nêu đúng cơ chế · 3 = đúng cơ chế **và** một con số, hoặc **và** một ca nó không đúng.

**Hai lỗi làm trần điểm cả buổi là 1:**

1. **Nói `needs` làm giảm phút runner.** Phút runner **không đổi**: **540 s** ở cả hai ca. `needs` giảm thời gian **chờ**, từ **325 s** xuống **235 s**.
2. **Nói chia N phần thì nhanh gấp N lần.** Job **120 s** với `parallel: 4` cho **49 s**, tức **2,45** lần; trần lý thuyết **4,8** lần dù N bao nhiêu.

**Bốn câu phân loại thật:**

| Câu | Phân loại điều gì |
|---|---|
| 6 | Người **dám coi "nhanh hơn dự kiến" là dấu hiệu hỏng** — câu lọc mạnh nhất của buổi |
| 7 | Người **biết phần cố định không chia được**: tách được **25 s + 95 s** ra khỏi con số 120 s |
| 9 | Người **đã từng bị 1/N sự thật**: nhìn tỉ số **21/82** là gọi luôn tên nguyên nhân |
| 11 | Người **phân biệt lợi ích cấu hình với giới hạn tài nguyên**: `needs` không sinh ra máy |

---

## V2. Bộ câu hỏi


<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hai</b> công thức, cho hai con số khác nhau trên <b style="color: var(--accent-primary);">cùng</b> một tập job (QT 4.1). Tuần tự: <code>T = Σ max(job trong stage)</code> — <b style="color: var(--accent-primary);">tổng của các max</b>. DAG: <code>T = max Σ(job trên một đường)</code> — <b style="color: var(--accent-primary);">max của các tổng</b>. Hiệu gọi là <b style="color: var(--accent-primary);">lãng phí hàng rào</b>: hàng rào <code>stage</code> buộc mọi job chờ job chậm nhất <b style="color: var(--accent-primary);">cùng stage</b>, kể cả job không có quan hệ dữ liệu nào với nó (buổi 03 QT 5.3 — lần thứ <b style="color: var(--accent-primary);">2</b>, lần này là lần <b style="color: var(--accent-primary);">sửa</b>).

Ví dụ chuẩn <b style="color: var(--accent-primary);">7 job</b>: tổng theo stage <b style="color: var(--accent-primary);">325 s</b>, đường găng <b style="color: var(--accent-primary);">235 s</b>, lãng phí <b style="color: var(--accent-primary);">90 s = 28%</b> — thủ phạm là <code>scan</code> <b style="color: var(--accent-primary);">150 s</b> chặn cả pipeline mà không ai cần kết quả của nó. Phải nói kèm: <b style="color: var(--accent-primary);">phút runner 540 s ở CẢ HAI ca</b>, vì <code>needs</code> không bỏ job nào, nó bỏ <b style="color: var(--accent-primary);">điều kiện chờ</b>. Vùng con số 28% không đúng: repo không có job dài lệch pha thì lãng phí gần <b style="color: var(--accent-primary);">0</b>, và dưới khoảng <b style="color: var(--accent-primary);">10%</b> thì chuyển sang DAG là đổi vài giây lấy một lớp hỏng im lặng.

<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: "Cộng thời gian tất cả job." Hoặc nói <code>needs</code> giảm phút runner — <b style="color: var(--accent-primary);">trần điểm cả buổi là 1</b>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Biết stage chạy lần lượt, không nêu được công thức thứ hai.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2đ: Nêu đúng <b style="color: var(--accent-primary);">hai</b> công thức bằng lời, gọi đúng tên <b style="color: var(--accent-primary);">lãng phí hàng rào</b>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Như trên, <b style="color: var(--accent-primary);">và</b> đưa <b style="color: var(--accent-primary);">325 · 235 · 90 s = 28%</b>, <b style="color: var(--accent-primary);">và</b> chốt <b style="color: var(--accent-primary);">540 s</b> không đổi, <b style="color: var(--accent-primary);">và</b> nêu vùng con số 28% không đúng.</div>

<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Bỏ hẳn <code>scan</code> khỏi pipeline thì hai con số thành mấy? *(<b style="color: var(--accent-primary);">265 s</b> và <b style="color: var(--accent-primary);">235 s</b>, lãng phí còn <b style="color: var(--accent-primary);">30 s = 11%</b>, phút runner giảm <b style="color: var(--accent-primary);">150 s</b> — nhưng khoản đó do <b style="color: var(--accent-primary);">bỏ job</b>, không do DAG.)*
</div>
</details>

---

### Câu 2 — ★★★

**Hỏi:** Pipeline một repo thật — `build`: `build-fe` 60 s · `build-be` 90 s · `lint` 20 s · `scan` 150 s; `test`: `test-unit` 45 s (đọc tệp của `build-be`) · `test-e2e` 120 s (đọc của **cả hai** build); `package`: `package` 30 s (đọc của cả hai build); `deploy`: `deploy` 25 s (đọc của `package`, `test-unit`, `test-e2e`). Tính **hai** con số: nó mất bao lâu bây giờ, và bao lâu nếu khai `needs` đúng theo dữ liệu.

**Đáp án chuẩn:** **325 s** bây giờ, **235 s** sau khi khai `needs` (QT 4.1).

Số thứ nhất — tổng của các max: `max(60,90,20,150)=150` · `max(45,120)=120` · `30` · `25` → **325 s**. Số thứ hai — theo mốc thời gian, giả định đủ slot: giây 0 bốn job `build` khởi động cùng lúc (**4 slot**); giây 90 `build-be` xong nên `test-unit`, `test-e2e`, `package` khởi động; giây 150 `scan` xong mà **không ai chờ nó**; giây 210 `test-e2e` xong; giây **235** `deploy` xong. Đường găng `build-be 90 → test-e2e 120 → deploy 25 = 235 s`, lãng phí **90 s = 28%**.

Hai điều nói kèm để được 3 điểm: thời gian DAG là **max của mọi nhánh**, nên nếu `scan` là **300 s** thì pipeline mất **300 s** dù đường găng vẫn 235; và con số 235 s chỉ có nếu runner cho **4** job chạy cùng lúc ở đỉnh (QT 7.1).

**Tiêu chí chấm:**
- 0đ: Cộng cả 8 job thành 540 s, hoặc không tính được số nào.
- 1đ: Tính đúng **một** trong hai số.
- 2đ: Đúng **cả hai**, và chỉ ra đường găng `build-be → test-e2e → deploy`.
- 3đ: Như trên, **và** nêu điều kiện **4 slot**, **và** nhận ra thời gian DAG là max của **mọi** nhánh nên một job không ai cần vẫn quyết định thời gian nếu nó đủ dài.

**Câu hỏi đào sâu:** Sau khi khai `needs`, giảm `scan` từ 150 s xuống 100 s thì nhanh thêm mấy giây? *(**0** giây — `scan` ngoài đường găng. Trước khi khai `needs` thì đúng 50 giây đó là tiết kiệm thật: cùng một thay đổi, hai giá trị.)*

---

### Câu 3 — 🔥

**Hỏi:** Khai `needs` thì `stage` còn tác dụng gì không? Và ngoài thứ tự chạy, `needs` còn đổi cái gì?

**Đáp án chuẩn:** **Vế một — `needs` KHÔNG xoá `stage`** (QT 4.2). Hai khái niệm ở hai tầng: `stage` là **thuộc tính khai báo**, hàng rào là **hành vi mặc định** dựa trên thuộc tính đó; `needs` thay hành vi, không thay thuộc tính. `stage` vẫn quyết định cách pipeline được **vẽ ra**, và vẫn **giới hạn** job nào được `needs` job nào — ràng buộc đó là loại **phải đo** theo phiên bản. Trần **50** phần tử `needs` cho một job ở GitLab 17.7.

**Vế hai — `needs` mang HAI việc cùng lúc** (QT 4.3, lần thứ **2** của buổi 05 QT 5.2): đổi thứ tự chạy **và** đổi tập artifact. Có `needs`, tập artifact **thu hẹp** về đúng danh sách `needs`; mặc định "tải artifact của **mọi** job stage trước" (buổi 05 QT 5.1) thôi áp dụng. **1** dòng `needs` đổi tập artifact từ "mọi job stage trước" xuống đúng **n** job liệt kê. Tách hai việc bằng `needs:artifacts: false` — cách duy nhất nói *"chờ nó, nhưng không cần tệp của nó"*:

```yaml
  needs:
    - job: dong-goi                # chờ và lấy tệp
    - job: kiem-tra-tai
      artifacts: false             # chờ, không lấy tệp
```

**Tiêu chí chấm:**
- 0đ: "Khai `needs` thì xoá `stages` đi cho gọn."
- 1đ: Biết `stage` vẫn còn, không nói được nó còn giữ việc gì.
- 2đ: Nêu đúng **`needs` bỏ hàng rào chứ không bỏ `stage`**, và nêu được vế artifact.
- 3đ: Như trên, **và** nói rõ tập artifact **thu hẹp** chứ không cộng thêm, **và** đưa `artifacts: false`, **và** ghi nhận ràng buộc theo stage **phải đo** cùng trần **50**.

**Câu hỏi đào sâu:** `needs: []` nghĩa là gì? *(Job khởi động ngay từ giây 0, không chờ ai kể cả stage trước, và nhận **0** artifact — cách đưa một job `lint` ra khỏi đường găng bằng một dòng.)*

---

### Câu 4 — ★★★

**Hỏi:** Đội tôi vừa chuyển sang `needs`. Chạy lần đầu: job `dong-goi` đỏ, báo không tìm thấy `dist/app.js`. Trước đó nó chưa hỏng lần nào, và không ai sửa nó. Chẩn đoán.

**Đáp án chuẩn:** `dong-goi` vốn sống nhờ **mặc định** "tải artifact của mọi job stage trước" (buổi 05 QT 5.1). Thêm `needs` **thu hẹp** tập artifact về đúng danh sách liệt kê (QT 4.3), và `build-fe` — job sinh `dist/app.js` — không có trong danh sách. Không ai sửa `dong-goi`; cái đổi là **tập tệp nó được nhận**.

Chẩn đoán bằng **1** phép đo, không bằng đọc YAML: đặt `echo "so tep = $(find . -type f | wc -l)"` ở dòng đầu `script`, chạy lại, so hai con số — trước khi có `needs` job nhận tệp của **cả 4** job stage `build`, sau đó nhận của đúng **n** job liệt kê. Cách sửa là **khai đủ cạnh dữ liệu**, không phải bỏ `needs` (QT 5.1 bước 1).

Ô của bảng hai thuộc tính (buổi 01 QT 7.1 — lần thứ **8**): ca này **ồn ào, có chặn** — ca **dễ nhất**. Ca ác là bản im lặng của cùng nguyên nhân: script chỉ `cp -r dist/ goi/ || true` rồi gói một thư mục rỗng thành `.tar.gz` **0 byte** và xanh. Vì vậy mỗi job đã khai `needs` phải có một dòng `test -s` cho tệp đầu vào quan trọng nhất — **0,2 s** mỗi job.

**Tiêu chí chấm:**
- 0đ: Đi tìm lỗi trong lệnh build của `build-fe`, hoặc đề nghị chạy lại pipeline.
- 1đ: Đoán liên quan artifact, không nói được vì sao thêm `needs` lại **mất** tệp.
- 2đ: Nêu đúng **`needs` thu hẹp tập artifact**, và cách sửa là khai đủ cạnh.
- 3đ: Như trên, **và** đưa phép đo `find . -type f | wc -l` trước/sau, **và** chỉ ra bản **im lặng** của cùng nguyên nhân cùng dòng `test -s` chặn nó.

**Câu hỏi đào sâu:** `dependencies` khác `needs` chỗ nào? *(`dependencies` chỉ thu hẹp **artifact**, không đổi thứ tự; `needs` đổi **cả hai** — buổi 05 QT 5.2. Đã có `needs` thì đừng khai thêm `dependencies` cho cùng job.)*

---

### Câu 5 — ★★★

**Hỏi:** Cho bạn một pipeline tuần tự 30 job và bảo chuyển sang DAG. Bạn làm theo mấy bước, thứ tự thế nào, và bỏ bước nào thì nguy hiểm nhất?

**Đáp án chuẩn:** **Ba** bước, không đảo thứ tự (QT 5.1): (1) lập bản đồ **dữ liệu** — job nào **đọc tệp** do job nào tạo ra, hiện vật `ban-do-phu-thuoc.md` của buổi 03; (2) mỗi mũi tên thành **một** dòng `needs`; (3) **đo lại** đường găng và so với con số cũ, ghi vào `bang-duong-gang.tsv`.

Phép kiểm rẻ nhất giữa bước 1 và 2: **số mũi tên phải bằng số dòng `needs`** — ví dụ chuẩn của buổi có **7** cạnh (QT 5.1). Bản đồ nhiều hơn YAML là **thiếu cạnh**, ca hỏng im lặng của QT 5.2; YAML nhiều hơn bản đồ là **chờ vô ích**, mất giây mà không ai biết vì pipeline vẫn xanh và vẫn đúng.

Bỏ bước nào nguy hiểm nhất — phải phân biệt **hai loại hậu quả**. Bỏ **bước 1** cho kết quả **sai**: khai `needs` theo cảm nhận thứ tự thay vì theo tệp thì sớm muộn thiếu một cạnh, pipeline **nhanh hơn và sai** (QT 5.2) — nguy hiểm nhất. Bỏ **bước 3** thì kết quả có thể vẫn đúng, nhưng ta **không biết** vừa sửa được bao nhiêu giây và có làm **chậm đi** hay không; đo bằng `do-duong-gang.sh`, đừng đo bằng cách nhìn biểu đồ.

**Tiêu chí chấm:**
- 0đ: "Thêm `needs` vào các job theo thứ tự trong file."
- 1đ: Kể được việc thêm `needs`, không có bước lập bản đồ và không có bước đo.
- 2đ: Đủ **3** bước đúng thứ tự, nhấn "khai theo **tệp**, không theo cảm nhận thứ tự".
- 3đ: Như trên, **và** đưa phép kiểm **số mũi tên = số dòng `needs`** kèm cả hai chiều lệch, **và** phân biệt hậu quả bỏ bước 1 (sai) với bỏ bước 3 (không có bằng chứng).

**Câu hỏi đào sâu:** Chỉ có 20 phút thì chuyển job nào trước? *(**Job dài nhất mà không job nào cần kết quả của nó** — thường là `scan`, `lint`, `báo cáo`. Ví dụ chuẩn: **1** thay đổi lấy lại **90 s**.)*

---

### Câu 6 — ★★★

**Hỏi:** Sáng nay pipeline của bạn xong sau **200 s**, trong khi mọi lần trước là **235 s**. Không ai sửa job nào. Đây là tin tốt hay tin xấu?

**Đáp án chuẩn:** **Tin xấu cho tới khi chứng minh được là tin tốt.** Nhanh hơn đường găng đúng **35 s** là triệu chứng đặc trưng của **DAG thiếu một cạnh** (QT 5.2), và là **tín hiệu duy nhất** mà lớp hỏng này phát ra.

Cơ chế: bỏ hàng rào nghĩa là nền tảng **thôi bảo đảm thứ tự hộ ta**, nên thứ tự đúng thành trách nhiệm của người khai `needs`. Thiếu một cạnh thì job chạy **trước khi** dữ liệu nó cần tồn tại mà vẫn **xanh**, vì nó đọc được một trong ba thứ: bản **cũ** trong cache; tệp có sẵn trong **git** vì ai đó từng commit bản sinh ra; hoặc thư mục **rỗng** mà script không kiểm — `tar` một thư mục rỗng cho gói hợp lệ **0 byte**, mã thoát 0.

Điều tra ba nhịp: (1) **so `duration` từng job, không so tổng thời gian pipeline** — từng job không đổi mà tổng giảm 35 s thì thứ đổi là **đồ thị**; (2) `find dist -newermt "@$CI_JOB_STARTED_AT_TS"` — tệp job đang đọc mà **cũ hơn** lúc job bắt đầu là bằng chứng trực tiếp; (3) đếm lại số mũi tên trên bản đồ so với số dòng `needs`. Ô của bảng hai thuộc tính: **im lặng, không chặn** — ô nguy hiểm nhất, chế độ hỏng số **1** của buổi; chặn bằng `test -s` cộng `find -newermt`, **0,2 s** mỗi job.

**Tiêu chí chấm:**
- 0đ: "Tin tốt, chắc runner rảnh." Đi báo cáo thành tích.
- 1đ: Thấy hơi lạ nhưng không gọi được tên nguyên nhân nào.
- 2đ: Gọi đúng **thiếu cạnh `needs`** và giải thích được vì sao job vẫn xanh.
- 3đ: Như trên, **và** kể **hai** trong ba nguồn dữ liệu cũ, **và** đưa phép đo mốc thời gian tệp, **và** gọi đúng ô *im lặng, không chặn* kèm chi phí 0,2 s.

**Câu hỏi đào sâu:** Có lý do **lành** nào cho việc nhanh hơn 35 s không? *(Có — cache nóng hơn hoặc `queued_duration` giảm; nhưng cả hai đều làm **`duration` của job đổi theo**. `duration` y nguyên mà tổng giảm thì chỉ còn cách giải thích là đồ thị đã đổi.)*

---

### Câu 7 — ★★★

**Hỏi:** Job test của tôi mất **120 s**. Tôi đặt `parallel: 4`. Nó còn bao nhiêu giây, và phút runner thành bao nhiêu?

**Đáp án chuẩn:** Khoảng **49 s**, tức nhanh **2,45** lần — **không** phải 4 lần. Phút runner đi từ **120 s** lên **196 s**, tức **+63%** (QT 6.3).

Phép tính phải nói ra: job 120 s tách thành **phần cố định 25 s** — khởi tạo container, phục hồi cache, tải artifact, khởi động công cụ test — và **phần chia được 95 s**. `T(N) = 25 + 95/N`, nên `T(4) = 25 + 23,75 ≈ 49 s`. Bốn điểm đo của bài lab: N = 1 · 2 · 4 · 8 cho **120 · 72 · 49 · 37 s**, phút runner đi **120 · 144 · 196 · 296 s**.

Trần lý thuyết là `120 / 25 =` **4,8** lần dù N bằng 100, vì phần cố định lặp lại **mỗi phần**: từ N = 4 lên N = 8 mua thêm **12 s** thời gian chờ bằng **100 s** phút runner. Vùng con số không đúng: **2,45** là số của tỉ lệ **25/95**; job **40 s** mà **30 s** là khởi tạo thì chia bao nhiêu phần cũng vô nghĩa, còn phút runner thì tăng thật.

**Tiêu chí chấm:**
- 0đ: "Nhanh gấp 4, còn 30 s." **Trần điểm cả buổi là 1.**
- 1đ: Biết không đạt 4 lần, không tính ra con số nào.
- 2đ: Nêu đúng cơ chế **phần cố định không chia được** và ra khoảng **49 s**.
- 3đ: Như trên, **và** viết được `25 + 95/N` cùng trần **4,8** lần, **và** nói phút runner **+63%** kèm nhận xét hai đại lượng do hai người trả tiền.

**Câu hỏi đào sâu:** Muốn `parallel: 8` thực sự đáng thì phải giảm cái gì? *(Giảm **phần cố định**, không tăng N: image mỏng hơn, cache nhỏ hơn, `needs` chỉ tải artifact cần dùng. Bớt 10 s cố định thì trần nhảy từ 4,8 lên **8** lần.)*

---

### Câu 8 — ★★

**Hỏi:** Tôi đặt `parallel: 4` cho job test và không sửa gì trong `script`. Chuyện gì xảy ra?

**Đáp án chuẩn:** **4** job làm **cùng một việc 4 lần**, tất cả **xanh**, phút runner tăng gấp **4** mà thời gian pipeline **không giảm** (QT 6.1).

Cơ chế: `parallel: N` sinh **N** job **giống nhau như đúc**; điều duy nhất khác nhau giữa chúng là `CI_NODE_INDEX` (1..N), kèm `CI_NODE_TOTAL`. Nền tảng chỉ nhân bản định nghĩa job và bơm hai biến — nó **không biết gì** về nội dung công việc, nên không thể biết bộ test của ta chia được theo tệp hay không. Việc **chia việc** hoàn toàn thuộc về `script`:

```yaml
    - DS=$(ls tests/*.spec.js | sort | awk "NR % $CI_NODE_TOTAL == $CI_NODE_INDEX - 1")
    - echo "phan $CI_NODE_INDEX/$CI_NODE_TOTAL nhan $(echo "$DS" | wc -l) tep"
    - npx jest $DS
```

Dấu hiệu của ca hỏng: 4 job có **cùng số test được chạy** và **cùng thời lượng**. `parallel` nhận **2–200** ở GitLab 17.7. Ô của bảng hai thuộc tính: **im lặng, không chặn** — chế độ hỏng số 2 của buổi; dòng in số tệp mỗi phần nhận được là thứ biến nó thành ồn ào.

**Tiêu chí chấm:**
- 0đ: "GitLab tự chia test ra 4 phần."
- 1đ: Biết cần chia việc, không nói được chia bằng gì.
- 2đ: Nêu đúng `CI_NODE_INDEX`/`CI_NODE_TOTAL` và việc chia thuộc `script`.
- 3đ: Như trên, **và** đưa dấu hiệu **cùng số test, cùng thời lượng**, **và** gọi đúng ô *im lặng, không chặn* kèm dòng in số tệp mỗi phần.

**Câu hỏi đào sâu:** Chia theo `NR % N` có nhược điểm gì? *(Chia đều theo **số tệp**, không theo **thời lượng**: một tệp test 80 s lọt vào phần nào thì phần đó thành đường găng mới. Tốt hơn là chia theo thời lượng lần chạy trước.)*

---

### Câu 9 — ★★★

**Hỏi:** Coverage của repo tôi tụt từ **82%** xuống **21%** đúng vào commit hôm qua. Commit đó chỉ có một dòng: `parallel: 4`. Giải thích.

**Đáp án chuẩn:** Không có gì tụt. **4** job song song sinh **4** báo cáo rời, và thứ đọc báo cáo chỉ thấy **1/4** sự thật (QT 6.4). Tỉ số nói ra nguyên nhân: `21 / 82 ≈ 0,26 ≈ 1/4` — đúng bằng **số phần**.

Cơ chế: mỗi job chạy một tập con nên mỗi báo cáo chỉ nói về tập con đó; việc **hợp nhất** là việc của ta, không phải của nền tảng. Hỏng im lặng vì **con số vẫn hiện ra**, chỉ là nó sai — và nếu có gate thì nó **chặn sai**, hoặc tệ hơn, gate đọc **một** trong bốn báo cáo rồi **mở cửa** cho thứ nó chưa từng đo.

```yaml
gop-bao-cao:
  needs: ["kiem-thu"]                 # nhận artifact của cả 4 phần
  script:
    - '[ "$(ls bao-cao-*.json | wc -l)" -eq 4 ] || { echo "thieu phan"; exit 1; }'
    - jq -s "add" bao-cao-*.json > bao-cao.json
```

**N** artifact vào, **1** artifact ra, chi phí **+8 s** mỗi pipeline. Đây là cái giá **bắt buộc** của `parallel`: job gộp phải vào **cùng một commit** với `parallel`, không bao giờ tách hai việc.

**Tiêu chí chấm:**
- 0đ: Đi tìm test bị xoá, hoặc kết luận "chắc đo sai, bỏ qua".
- 1đ: Đoán liên quan `parallel`, không nói được cơ chế N báo cáo rời.
- 2đ: Nêu đúng **N báo cáo rời, thiếu job gộp**, dùng tỉ số 21/82 ≈ 1/4 làm bằng chứng.
- 3đ: Như trên, **và** đưa khẳng định đếm số tệp bằng `CI_NODE_TOTAL`, **và** nêu chi phí **+8 s**, **và** chốt job gộp phải đi cùng commit với `parallel`.

**Câu hỏi đào sâu:** `needs: ["kiem-thu"]` cho một job `parallel: 4` thì nhận artifact của phần nào? *(Của **cả 4**. Nhưng số tệp thực nhận vẫn **phải đo**: bốn phần ghi cùng tên tệp thì ghi đè nhau, ta được đúng **1** tệp, xanh, và sai — nên tên tệp phải chứa `CI_NODE_INDEX`.)*

---

### Câu 10 — ★★

**Hỏi:** Tôi có `parallel:matrix` gồm 3 phiên bản Node × 2 hệ điều hành. Thêm một phiên bản Node nữa thì thành mấy job?

**Đáp án chuẩn:** **8** job, không phải 7. Matrix sinh job theo **tích Descartes** của các danh sách biến, nên số job **nhân lên** chứ không cộng vào (QT 6.2): `3 × 2 = 6` thành `4 × 2 =` **8**.

Quy luật phải nói kèm: thêm một giá trị vào **một** biến làm số job tăng theo **tích của các biến còn lại** — cùng phép thêm đó trên matrix `4 × 3 × 2` cộng thêm **6** job. Trần một khối matrix là **200** job ở GitLab 17.7, con số của phiên bản nên phải kiểm lại, đừng viết như hằng số. Dấu hiệu khi làm sai: thêm một phiên bản Node và hôm sau **hàng đợi runner đầy**, vì mỗi job mới cũng cần một slot (QT 7.1).

**Tiêu chí chấm:**
- 0đ: "7 job."
- 1đ: Biết số job tăng, tính ra sai số.
- 2đ: Trả lời đúng **8** và gọi tên **tích Descartes**.
- 3đ: Như trên, **và** phát biểu quy luật "tăng theo **tích của các biến còn lại**" kèm ví dụ thứ hai, **và** nêu trần **200** cùng hệ quả slot runner.

**Câu hỏi đào sâu:** Muốn bỏ đúng một tổ hợp trong 8 thì làm thế nào? *(Không trừ được trong một khối; khai **hai** khối matrix nhỏ hơn, hoặc thêm `rules` theo giá trị biến. Đây cũng là lúc nên hỏi đã tới lúc sinh pipeline lúc chạy chưa — buổi 09.)*

---

### Câu 11 — ★★★

**Hỏi:** Tôi khai `needs` đúng theo bản đồ dữ liệu, đo lại: pipeline vẫn **325 s**, không nhanh hơn một giây. Điều tra thế nào?

**Đáp án chuẩn:** Nghi phạm số một là **thiếu slot runner**, không phải `needs` sai (QT 7.1). DAG cho phép chạy song song, nhưng **runner** mới là chỗ có tài nguyên — `needs` không sinh ra máy. Ví dụ chuẩn cần **4** slot ở đỉnh; với `concurrent = 2` thì 235 s trở lại khoảng **300 s**, và với 1 slot thì DAG chỉ **đổi thứ tự hàng đợi**.

Bốn nhịp, mỗi nhịp một con số:

1. **Cộng `queued_duration` của mọi job**, trước và sau — thiếu slot có dấu hiệu rất đặc trưng: phần thời gian tưởng là tiết kiệm được **hiện lại nguyên vẹn** trong `queued_duration`.
2. **Đếm số job chạy đồng thời ở đỉnh** từ `started_at`/`finished_at`, so với `min(concurrent, limit)` của buổi 02 QT 6.1 (lần thứ **2**) — `concurrent` ở `config.toml` là trần toàn cục, `limit` là trần một mục runner, **min** thắng, và cái ở `config.toml` khó tìm nhất.
3. **Slot đủ mà vẫn không nhanh hơn:** nút cổ chai là **CPU hay đĩa** của máy chạy runner (buổi 02 QT 6.2) — bốn job cùng lúc trên 2 vCPU thì mỗi job chậm đi và tổng gần như không đổi.
4. Sau cùng mới xét khả năng **lãng phí hàng rào của repo này vốn gần 0**; nếu vậy thì `needs` không đáng làm ở đây, và đó là kết luận hợp lệ.

Ô của bảng hai thuộc tính: **im lặng, không chặn** — cái giá thật là một **kết luận sai**: "`needs` vô dụng".

**Tiêu chí chấm:**
- 0đ: Kết luận `needs` không có tác dụng, hoặc đi khai thêm `needs`.
- 1đ: Nghi tài nguyên runner, không nêu được phép đo nào.
- 2đ: Gọi đúng **thiếu slot** và đề xuất đọc `queued_duration`.
- 3đ: Như trên, **và** nêu `min(concurrent, limit)` dẫn buổi 02 QT 6.1, **và** kể được nhánh CPU/đĩa, **và** để mở ca "lãng phí hàng rào gần 0" như kết luận hợp lệ.

**Câu hỏi đào sâu:** Thêm một runner nữa thì có chắc nhanh hơn? *(Không — buổi 02 QT 6.2: nút cổ chai là CPU hoặc đĩa của **cùng một máy** thì thêm mục runner chỉ chia nhỏ cùng lượng tài nguyên.)*

---

### Câu 12 — 🔥

**Hỏi:** `needs:project` cho bạn lấy artifact từ project khác. Bạn dùng nó khi nào, và đặt điều kiện gì trước khi dùng?

**Đáp án chuẩn:** `needs:project` và `needs:pipeline` lấy được artifact từ project khác, và cùng lúc tạo ra một phụ thuộc **giữa hai đội** (QT 7.2). Cạnh phụ thuộc đi xuyên biên giới project cũng đi xuyên biên giới **quyền sở hữu**: **1** cạnh liên project = **1** hợp đồng giữa hai đội. Không có gì trong project ta ngăn đội kia đổi tên job hoặc bỏ artifact — và khi họ đổi, pipeline ta hỏng với lỗi **không tìm thấy job** trong khi commit gần nhất của repo ta không liên quan gì.

Khai đúng là `needs: [{project: nhom/goi-chung, ref: main, job: dong-goi, artifacts: true}]`, kèm ngay `test -s thu-vien/lib.jar || exit 1`.

**Ba điều kiện phải có:** (1) **thoả thuận bằng chữ về tên job và đường dẫn artifact**, vì đó là hai thứ ta đang khoá cứng vào YAML của mình; (2) **`ref` trỏ vào thứ ổn định** — một tag hoặc nhánh được bảo vệ, không phải nhánh làm việc của đội kia; (3) **một dòng khẳng định** kiểm hiện vật nhận được, vì ca artifact rỗng vẫn cho job **xanh** (buổi 05 QT 5.3, buổi 01 QT 7.3 — lần thứ **6**).

Đường thay thế đáng cân nhắc trước: **đẩy artifact vào registry** theo phiên bản rồi kéo về theo phiên bản — đắt hơn vài giây, đổi lại có một **phiên bản cố định** không đổi dưới chân ta. Buổi 09 và buổi 44 quay lại đúng chỗ này.

**Tiêu chí chấm:**
- 0đ: "Cứ khai vào, tiện hơn copy tệp."
- 1đ: Biết nó lấy artifact từ project khác, không thấy vấn đề sở hữu.
- 2đ: Nêu đúng **phụ thuộc giữa hai đội** và triệu chứng "hỏng mà commit của ta không liên quan".
- 3đ: Như trên, **và** đủ **ba** điều kiện gồm `ref` ổn định và dòng khẳng định, **và** so được với đường registry theo phiên bản.

**Câu hỏi đào sâu:** Đội kia để artifact hết hạn theo `expire_in` thì pipeline ta hỏng lúc nào? *(Vào một lúc **không** liên quan tới commit nào của cả hai bên — ca khó chẩn đoán nhất. Vì vậy hợp đồng phải nói cả `expire_in`, không chỉ tên job.)*

---

## V3. Câu chốt để nói khi phỏng vấn

> Bốn câu dưới đây viết **nguyên văn, đúng ngữ điệu nói**. Học viên tập nói to từng câu tới khi trôi chảy mà không phải nghĩ. Mỗi câu chứa **một con số** hoặc **một cơ chế** — thứ phân biệt người đã đo với người đã đọc.

**Câu 1 — khi được hỏi "bạn tối ưu thời gian pipeline thế nào":**



**Câu 2 — khi được hỏi "chuyển sang DAG thì tiết kiệm được bao nhiêu tiền":**

> "Không đồng nào, và tôi nói rõ điều đó trước khi có ai kỳ vọng sai. `needs` giảm **thời gian chờ** của lập trình viên từ **325** xuống **235 giây**, còn **phút runner thì đúng 540 giây ở cả hai ca** — vì tôi không bỏ job nào, tôi chỉ bỏ **điều kiện chờ**. Đây là hai đại lượng và **hai người khác nhau trả tiền**: thời gian chờ thì đội phát triển trả, phút runner thì hoá đơn trả. Muốn giảm hoá đơn thì tôi bán một việc khác — bỏ hẳn job không ai dùng — và tôi không trộn hai việc đó vào một con số."

**Câu 3 — khi được hỏi "kỹ thuật nào bạn dùng mà có mặt tối":**

> "DAG. Cái giá của nó là một lớp hỏng **im lặng**, vì bỏ hàng rào nghĩa là nền tảng thôi giữ thứ tự hộ tôi. Tôi thiếu đúng **một** cạnh `needs` một lần: job test chạy trước khi build xong, mà vẫn **xanh** vì nó đọc được bản build cũ còn trong cache. Triệu chứng duy nhất là pipeline **nhanh hơn dự kiến 35 giây** — mà nhanh hơn thì không ai đi điều tra. Từ đó tôi có hai thói quen: số mũi tên trên bản đồ dữ liệu phải **bằng** số dòng `needs`, lệch là đi tìm; và mỗi job đã khai `needs` mở đầu bằng `test -s` với `find -newermt` cho tệp đầu vào — tốn **0,2 giây**, và nó đổi lỗi từ ô *im lặng không chặn* sang *job đỏ ngay*."

**Câu 4 — khi được hỏi "bật `parallel` lên thì nhanh gấp mấy":**

> "Không gấp N lần, và tôi tính được ra số. Job test của tôi **120 giây**, trong đó **25 giây cố định** — khởi tạo container, phục hồi cache, tải artifact — và **95 giây chia được**. Nên `parallel: 4` cho **25 + 95/4**, khoảng **49 giây**: nhanh **2,45 lần**, không phải 4. Trần của nó là **120 chia 25**, tức **4,8 lần**, dù tôi đặt N bao nhiêu. Đổi lại phút runner đi từ 120 lên **196 giây, tăng 63%**. Nếu phần cố định lớn hơn phần chia được thì tôi **không** bật `parallel`, tôi đi làm phần cố định nhỏ lại. Và một thứ tôi luôn đưa vào **cùng commit** với `parallel`: job gộp báo cáo — thiếu nó thì coverage chỉ còn **1/N** sự thật, mà con số vẫn hiện ra nên không ai nghi gì."

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
| ≥ 80% | Nắm vững. Giao phần `needs:project` của lab bước 5 làm trước buổi 09 |
| 60–79% | Đạt. Đọc lại quy tắc bị mất điểm trước buổi 09 |
| 40–59% | Chưa đạt. Làm lại lab bước 1 và bước 2 ở nhà: phải tự tính ra **325 s** và **235 s** trên repo mình |
| < 40% | Chưa đạt. Học lại cả buổi — buổi 09, 13, 14 và 46 dựng thẳng lên hai công thức này |

**Bảng lỗi làm trần điểm là 1:**

| Lỗi | Vì sao nghiêm trọng đến mức trần điểm |
|---|---|
| "`needs` làm giảm phút runner" | Phút runner **không đổi**: **540 s** ở cả hai ca. Người lẫn hai đại lượng sẽ hứa với người giữ hoá đơn một khoản tiết kiệm không tồn tại, và sẽ không biết trả lời khi `parallel` làm phút runner **tăng 63%** |
| "Chia N phần thì nhanh gấp N lần" | **120 s** với `parallel: 4` cho **49 s**, tức **2,45** lần; trần `T/cố_định` = **4,8** lần. Người tin gấp N lần sẽ tăng N lên 8 rồi 16, thấy thời gian gần như không đổi mà phút runner tăng thật, rồi kết luận sai là "GitLab không song song thật" thay vì đi giảm **phần cố định** |

---

## V5. Bài tập về nhà

### BTVN 1. Hai con số của repo thật

Lấy **một** pipeline đã xanh của repo mình, đọc `stage`, `duration`, `started_at`, `finished_at` của **mọi** job:

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?per_page=100" \
| jq -r '.[] | [.stage, .name, (.duration|floor), .started_at, .finished_at] | @tsv'
```

**Nộp:** `bang-duong-gang.tsv` và **ba** con số — tổng theo stage, đường găng theo quan hệ dữ liệu, lãng phí hàng rào tính bằng **giây** và **phần trăm**. Kèm một câu kết luận: lãng phí của repo này **trên hay dưới 10%**, tức chuyển sang DAG có đáng làm hay không.

### BTVN 2. Bản đồ dữ liệu và phép đếm hai chiều

Lập `ban-do-phu-thuoc.md` theo **tệp**, không theo cảm nhận thứ tự: mỗi dòng là *job X đọc tệp `<đường dẫn>` do job Y tạo ra*.

**Nộp:** (1) số **mũi tên** của bản đồ và số dòng `needs` hiện có trong YAML, kèm hiệu của chúng; (2) tên **job dài nhất mà không job nào cần kết quả của nó** kèm `duration` — ứng viên số một cho thay đổi lợi nhất trên mỗi dòng YAML; (3) với **một** job trong danh sách, viết ra dòng `test -s` phải thêm, đúng tên tệp thật.

### BTVN 3. Tách phần cố định của job test dài nhất

Chạy job test dài nhất ở **hai** mức `parallel` — 1 và 4 — rồi giải hai ẩn: `T(N) = cố_định + biến/N` → `cố_định = (4·T(4) − T(1)) / 3`.

**Nộp:** bốn con số — `T(1)`, `T(4)`, phần cố định, phần chia được — cộng **hai** con số suy ra: tốc độ thật ở N = 4, và trần `T/cố_định`. Kèm một câu trả lời **có/không**: repo này có đáng bật `parallel` không, và job **gộp báo cáo** đã tồn tại chưa — nếu chưa, ghi ra dòng khẳng định đếm số tệp đầu vào sẽ thêm vào nó.

### BTVN 4. Chuẩn bị cho buổi 09

Trả lời ba câu sau bằng viết, mỗi câu 3–5 dòng. Mang theo vào buổi 09.

1. Hôm nay QT 6.2 cho thấy matrix nhân job lên rất nhanh. Với một monorepo có **12** thư mục con, mỗi thư mục cần **3** job, hãy đếm số **khối** YAML phải viết và bảo trì. Rồi trả lời: vì sao một tệp YAML **tĩnh** khó tả được việc *"chỉ chạy cho thư mục đã đổi"*, dù `rules:changes` có tồn tại?
2. Hôm nay QT 7.2 cho thấy `needs:project` lấy artifact từ project khác. Hãy **đoán**: nếu ta `trigger` một pipeline ở project khác thì job `trigger` **chờ** pipeline đó xong hay **không chờ**, và trạng thái xanh/đỏ của job `trigger` phụ thuộc vào cái gì? Ghi phỏng đoán trước khi tra tài liệu.
3. Hôm nay QT 5.2 cho thấy cạnh bị quên là hỏng im lặng. Nếu pipeline được **sinh ra bởi một job** — một job viết ra tệp YAML rồi bảo GitLab chạy nó — thì `rules` của các job trong pipeline đó được đánh giá **lúc nào** so với `t0` của pipeline cha? Ghi phỏng đoán, kèm một câu: điều đó cho phép làm **một** việc mà buổi 04 nói là không thể.

**Ba câu này dẫn vào đâu:** câu 1 dẫn vào **§4 buổi 09 QT 4.1** — con số học viên tự đếm được (**12 × 3 = 36** khối, khoảng **540** dòng) chính là con số buổi 09 đối chiếu với **1** khối `trigger` cộng **1** script khoảng 40 dòng; **lab bước 1 buổi 09** dựng lại bài toán đó ở quy mô 3 module. Câu 2 dẫn vào **§5 buổi 09 QT 5.1 và QT 5.2** — job `trigger` là **bridge job**, **0** slot và **0** phút runner, mặc định nó **xanh ngay** khi tạo được pipeline con; đúng **1** dòng `strategy: depend` đổi điều đó, và **lab bước 2 buổi 09** đặt hai bridge job cạnh nhau để đo. Câu 3 dẫn vào **§4 buổi 09 QT 4.2** — pipeline con có `t0` **riêng**, nên biến do job cha sinh ra **dùng được** trong `rules` của pipeline con, thứ buổi 04 QT 4.2 nói là không thể trong một pipeline; đây là trục `t0` **lần thứ 3**, và **lab bước 4 buổi 09** đo nó. Bốn bước sinh pipeline lúc chạy nằm ở **§6 buổi 09 QT 6.1**.
{% endraw %}
