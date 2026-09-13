---
layout: post
title: "[Bài 09] Điều Phối Pipeline Phức Tạp: Multi-Project Pipelines, Child-Parent Pipelines & Trigger API Tokens"
date: 2026-09-12 08:10:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-09
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 9
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.09] Hướng dẫn chuyên sâu Điều Phối Pipeline Phức Tạp: Multi-Project Pipelines, Child-Parent Pipelines & Trigger API Tokens: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Điều Phối Pipeline Phức Tạp: Multi-Project Pipelines, Child-Parent Pipelines & Trigger API Tokens."
  - "Thiết kế CI/CD Pipeline chuẩn Enterprise với kiến trúc DAG, tối ưu hóa thời gian build và caching hiệu quả."
  - "Bảo mật chuỗi cung ứng phần mềm với SAST/DAST, Container Scanning và OIDC Authentication."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 09] ĐIỀU PHỐI PIPELINE PHỨC TẠP: MULTI-PROJECT PIPELINES, CHILD-PARENT PIPELINES & TRIGGER API TOKENS

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · executor `docker`.
> Mọi đoạn YAML dán được vào `.gitlab-ci.yml` và chạy trong dưới 60 giây, trừ đoạn sinh 60 job ở §7 (đo trần, cố ý nặng).
> Lệnh `curl` dùng bốn biến đã có từ buổi 01: `$GITLAB`, `$GITLAB_TOKEN`, `$PID`, `$PIPE`.
> **Buổi này là buổi đầu tiên của khoá dịch chuyển THỜI ĐIỂM quyết định.** Tám buổi trước đều nhận `t0` như một hằng số; hôm nay ta tạo ra `t0` thứ hai — và trả giá bằng bằng chứng.

---





Gọi ngẫu nhiên, mỗi câu 1 phút. Ai sai câu 5 sẽ không thấy vì sao YAML tĩnh chết ở monorepo (§4); ai sai câu 3 sẽ không nhận ra ca "cha xanh con đỏ" là cùng một lớp lỗi (§5).

| # | Câu hỏi | Đáp án vắn tắt | Dẫn vào đâu hôm nay |
|---|---|---|---|
| 1 | Hai công thức tính thời gian pipeline khác nhau ở chỗ nào | **Tổng của các max** so với **max của các tổng**: **325 s** so với **235 s**, lãng phí **90 s = 28%** (buổi 08 QT 4.1) | §5 — pipeline con là **một** hàng rào mới; `strategy: depend` quyết định hàng rào đó có tồn tại hay không |
| 2 | `needs` đổi thêm cái gì ngoài thứ tự chạy | Thu hẹp tập **artifact** tải về đúng danh sách `needs` (buổi 08 QT 4.3) | §5 QT 5.3 — qua biên giới pipeline thì cả mặc định cũ **cũng không còn**, phải khai lại |
| 3 | Pipeline nhanh hơn dự kiến 35 giây nghĩa là gì | Có thể **thiếu một cạnh**: nhanh hơn **và sai**; tín hiệu duy nhất là *nhanh hơn dự kiến* (buổi 08 QT 5.2) | §5 QT 5.2 — hôm nay tín hiệu duy nhất là *cha xanh mà chẳng ai xem con* |
| 4 | Chia test thành 4 phần thì nhanh gấp mấy lần | **2,45** lần, không phải 4; **120 s = 25 s cố định + 95 s biến** (buổi 08 QT 6.3) | §7 — pipeline con cũng có phần cố định: **~2 giây** tạo pipeline cộng **8–15 giây** job sinh cấu hình |
| 5 | Matrix 3 × 2, thêm một phiên bản nữa thì mấy job | **8** job — **nhân**, không cộng; trần **200** (buổi 08 QT 6.2) | §4 QT 4.1 — đúng phép nhân đó là lý do YAML tĩnh không tả được monorepo |



Tám buổi qua có một điều chưa ai chất vấn: **thời điểm** quyết định. Buổi 04 QT 4.1 chốt rằng `rules` được đánh giá đúng một lần lúc pipeline được tạo — gọi là `t0`. Từ đó mọi giới hạn ta gặp đều là hệ quả của một câu: quyết định bị buộc phải xảy ra **quá sớm**.

Ba giới hạn đã gặp có **cùng một** nguyên nhân, và nguyên nhân đó là thời điểm: biến `dotenv` không dùng được trong `rules` (buổi 04 QT 4.2) vì lúc `rules` chạy thì job sinh ra biến còn chưa tồn tại; `rules:changes` sai ở ba ca mà `compare_to` chỉ sửa hai (buổi 04 QT 6.3) vì ở `t0` không có tiến trình nào của ta chạy để tự tính "đổi những gì"; `matrix` nhân job theo phép nhân nên không tả được monorepo (buổi 08 QT 6.2) vì mọi tổ hợp phải được **viết ra** trước khi biết commit đổi cái gì.

Hôm nay ta không sửa từng giới hạn một. Ta đổi cái sinh ra cả ba.

**Luận đề trung tâm.**

> **Một tệp YAML tĩnh phải liệt kê MỌI tổ hợp job trước khi biết commit sắp tới đổi cái gì. Pipeline sinh lúc chạy đảo ngược thứ tự đó: một job đọc trạng thái thật của repo rồi VIẾT RA đúng tập job cần thiết. Cái ta mua được là một `t0` THỨ HAI — muộn hơn, biết nhiều hơn. Cái ta trả là bằng chứng: từ giờ lỗi có thể nằm trong một tệp YAML KHÔNG có trong repo.**

Đọc sơ đồ này trước khi vào §4. Toàn bộ buổi học là đọc đúng bốn dòng trong nó.

```
   PIPELINE CHA                                    PIPELINE CON
   t0 (cha) ─ rules của job cha đánh giá
        │
        ├─ job "sinh-cau-hinh" CHẠY
        │     git diff → biết ĐÚNG module nào đổi
        │     viết ra con.yml  → artifact
        │
        └─ job "trigger" (bridge)  ──────────────► t0 (CON) ─ rules của job CON đánh giá Ở ĐÂY
              0 giây runner, 0 slot                     │      biến do cha sinh DÙNG ĐƯỢC
              strategy: depend ? phản chiếu : xanh ngay │
                                                        └─ job con chạy

   Ba loại quan hệ:  child (cùng repo) · multi-project (repo khác) · lồng nhau (con của con)
   Khác nhau ở: AI GIỮ YAML · AI XEM ĐƯỢC LOG · AI ĐỔI ĐƯỢC MÀ KHÔNG XIN PHÉP AI
```

Bốn dòng phải chỉ tay vào khi giảng: mũi tên `──►` là **một biên giới**, không phải một cạnh `needs` — không artifact, không biến, không trạng thái nào tự chảy qua nó (§5 QT 5.3). `t0 (CON)` nằm **bên phải** `t0 (cha)` trên trục thời gian, và toàn bộ giá trị của buổi nằm ở khoảng cách giữa hai chữ đó (§4 QT 4.2). `0 giây runner` là thứ rẻ nhất trong cả khoá, và là lý do người ta lạm dụng nó (§5 QT 5.1 đọc cùng §7 QT 7.1). Còn `strategy: depend ? phản chiếu : xanh ngay` là **một** dòng cấu hình quyết định pipeline cha có nói thật hay không (§5 QT 5.2).

**Kết quả buổi trước được dùng lại.** Buổi này dùng lại nhiều nhất từ buổi 04 (`t0`), buổi 05 (artifact là hợp đồng) và buổi 06 (biến xuống hạ nguồn).

| Kết quả | Nguồn | Dùng ở đâu hôm nay |
|---|---|---|
| `rules` đánh giá **1 lần** ở `t0` | buổi 04 QT 4.1 | §4 QT 4.2 — **lần thứ 3** của trục `t0`, và hôm nay ta có `t0` **thứ hai** |
| Biến `dotenv` không dùng được trong `rules` | buổi 04 QT 4.2 | §4 QT 4.2 — pipeline con là **cửa duy nhất** thoát khỏi giới hạn đó |
| `rules:changes` sai ở ba ca, `compare_to` sửa **2** | buổi 04 QT 6.3 | §6 QT 6.3 — ca thứ ba giải bằng lệnh `git` trong job; **lần thứ 2** |
| **0** job → **0** pipeline, và ca này im lặng | buổi 04 QT 4.3 | §6 QT 6.1 — YAML sinh ra rỗng cho đúng ca đó; **lần thứ 2** |
| `ci/lint` đọc tệp **sau phân giải** | buổi 03 QT 4.3 | §6 QT 6.2 — lint YAML **sinh ra** trước khi trigger; **lần thứ 2** |
| Artifact là hợp đồng, kiểm được từ ngoài pipeline | buổi 05 QT 4.1, 5.3 | §5 QT 5.3 và §7 QT 7.2 — YAML sinh ra **phải** là artifact |
| Khai tường minh `when: always` cho thứ cần đọc lúc đỏ | buổi 05 QT 5.4 | §7 QT 7.2 — **lần thứ 2** |
| `inherit:variables` quyết định biến xuống hạ nguồn | buổi 06 QT 7.1 | §6 QT 6.4 — **lần thứ 2**, hôm nay đo đủ ba cách khai |
| Chín nấc biến | buổi 06 QT 4.1 | §6 QT 6.4 — biến truyền qua `trigger` chèn vào nấc nào |
| `: "${VAR:?}"` chặn biến rỗng | buổi 06 QT 5.2 | §6 QT 6.4 — dòng duy nhất biến "con chạy rỗng và xanh" thành ồn ào |
| `matrix` nhân job theo phép nhân | buổi 08 QT 6.2 | §4 QT 4.1 — lý do YAML tĩnh không tả được monorepo |
| `needs:project` là hợp đồng giữa hai đội | buổi 08 QT 7.2 | §4 QT 4.3 và §7 QT 7.1 — **lần thứ 2** |
| Báo cáo gỡ rối **bốn dòng**, dòng 2 là một lệnh | buổi 07 QT 7.3 | §7 QT 7.2 — hôm nay nó thành **năm** dòng |
| Bảng hai thuộc tính hỏng: im lặng/ồn ào × chặn/không chặn | buổi 01 QT 7.1 | §5, §6, §7 — **lần thứ 9** |

**Nguyên lý xuất hiện lần thứ mấy.** Giảng viên **nói ra con số** để lớp thấy đây là đồ nghề dùng lại, không phải khẩu hiệu:

- **Bảng hai thuộc tính hỏng** — **lần thứ 9**. Buổi này góp **6** chế độ hỏng mới, và cả **6** đều ở ô *im lặng*; **5** trong 6 ở ô *im lặng + không chặn*. Đây là buổi có tỉ lệ ô nguy hiểm cao nhất của giai đoạn 2.
- **"Phụ thuộc phiên bản thì phải ĐO, không tra"** — **lần thứ 9**. Hôm nay có bốn đại lượng loại đó, bảng đủ ở §7.
- **"Job xanh không chứng minh gì"** — **lần thứ 7**. Hôm nay câu đó lên một bậc: **pipeline** xanh không chứng minh gì, vì nó có thể xanh nhờ việc **không** chờ pipeline con.
- **`t0`** — **lần thứ 3**. Buổi 04 nêu, buổi 05 QT 4.2 đối chiếu (`cache:key` tính trên runner, không ở `t0`), buổi 09 **nhân đôi** nó.

**Ba câu hỏi trung tâm của buổi:**

1. Pipeline con có `t0` riêng — điều đó cho tôi làm được **một** việc mà YAML tĩnh không làm được, việc đó là gì?
2. Vì sao pipeline cha có thể **xanh** trong khi pipeline con **đỏ**, và một dòng nào chặn điều đó?
3. Khi lỗi nằm trong một tệp YAML không có trong repo, tôi điều tra bằng cái gì?

**Ba câu BTVN 4 của buổi 08 dẫn thẳng vào ba mục.** Gọi ba học viên đọc phỏng đoán đã ghi, **không sửa ngay**, ghi lên bảng để đối chiếu cuối buổi: câu 1 (12 thư mục × 3 job, và vì sao YAML tĩnh khó tả "chỉ chạy cho thư mục đã đổi") → §4 QT 4.1; câu 2 (`trigger` một pipeline ở project khác thì **chờ** hay **không chờ**) → §5 QT 5.1 và QT 5.2; câu 3 (`rules` của job trong pipeline được sinh ra đánh giá lúc nào so với `t0` của cha) → §4 QT 4.2, và §6 là chỗ ta dùng câu trả lời đó để làm việc.

---



| # | Làm được gì | Hiện vật chứng minh |
|---|---|---|
| LĐ1 | Tách một pipeline thành cha + con và chỉ ra bridge job **không** nằm ở endpoint `/jobs` | `doc-bridge.sh` in `/bridges` cạnh `/jobs` — lab bước 1 CHECKPOINT 1, 2 |
| LĐ2 | Chứng minh bằng **2** giá trị `status` rằng thiếu `strategy: depend` làm cha xanh khi con đỏ | Hai bridge job cạnh nhau, lab bước 2 CHECKPOINT 3 |
| LĐ3 | Đưa artifact **qua** biên giới pipeline theo đúng chiều cần, kèm **1** khẳng định `test -s` | `needs:pipeline:job` chạy được, lab bước 2 CHECKPOINT 4, 5 |
| LĐ4 | Viết `sinh-pipeline.sh`: đọc `git diff`, sinh `con.yml`, tự gọi `ci/lint`, tự `exit 1` khi sai | `sinh-pipeline.sh` — **hiện vật chính**, lab bước 3 CHECKPOINT 6, 7 |
| LĐ5 | Xử lý tường minh ca **0 module đổi** bằng **1** job giữ chỗ, không sinh tệp rỗng | Pipeline con của commit chỉ sửa `README`, lab bước 3 CHECKPOINT 8 |
| LĐ6 | Dùng biến do job cha sinh ra trong `rules` của job con — việc buổi 04 nói là không thể | Job con chạy đúng theo `$MODULE_DOI`, lab bước 4 CHECKPOINT 9 |
| LĐ7 | Nói ra biến xuống pipeline con theo **3** đường và số đo của từng đường trên hệ thống của mình | Bảng `${#VAR}` ba biến × ba ca, lab bước 4 CHECKPOINT 10 |
| LĐ8 | Điều tra một pipeline con hỏng **hôm qua** bằng artifact cấu hình, không bằng `git show` | `con.yml` tải về từ pipeline cũ + báo cáo **5** dòng, lab bước 5 CHECKPOINT 11 |

---



| Cần biết | Mức yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| `rules` đánh giá đúng một lần ở `t0`; hệ quả với `dotenv` | **Bắt buộc** | buổi 04 QT 4.1, 4.2 — trục chính của cả buổi |
| Pipeline không còn job nào thì **không được tạo** | **Bắt buộc** | buổi 04 QT 4.3 — ca 0 job trở lại ở §6 QT 6.1 |
| Ba ca `rules:changes` sai và `changes:compare_to` | **Vận dụng** | buổi 04 QT 6.3 |
| `artifacts` là hợp đồng; artifact rỗng mà job vẫn xanh | **Bắt buộc** | buổi 05 QT 5.3, và `when: always` ở QT 5.4 |
| `ci/lint` trả về tệp sau phân giải | **Vận dụng** | buổi 03 QT 4.3 — §6 QT 6.2 dùng đúng endpoint đó |
| Chín nấc biến, và `inherit:variables` với pipeline hạ nguồn | **Bắt buộc** | buổi 06 QT 4.1, 7.1 |
| Biến rỗng không phải lỗi; `: "${VAR:?}"` | Vận dụng | buổi 06 QT 5.2 |
| `needs` thu hẹp artifact; `needs:project` là hợp đồng hai đội | Vận dụng | buổi 08 QT 4.3, 7.2 |
| Bảng hai thuộc tính hỏng: im lặng/ồn ào × chặn/không chặn | **Bắt buộc** | buổi 01 QT 7.1 — dùng ở cả ba mục §5, §6, §7 |
| Báo cáo gỡ rối bốn dòng, dòng 2 là một lệnh | Vận dụng | buổi 07 QT 7.3 — hôm nay thêm dòng thứ 5 |
| `curl` + `jq`, đọc `git diff`, viết script bash khoảng 40 dòng | **Bắt buộc** | buổi 07 lab (`go-roi.sh`) — hôm nay viết `sinh-pipeline.sh` |

---



### 3.1. Đối chiếu thuật ngữ

Từ khoá YAML và tên trường API **giữ nguyên tiếng Anh**, vì học viên gõ đúng chữ đó vào tệp cấu hình hoặc vào `jq`. Khái niệm tổ chức thì dùng tiếng Việt, kèm tiếng Anh để đi phỏng vấn.

| Tiếng Việt dùng trong bài | Tiếng Anh | Dùng thẳng tiếng Anh trong thân bài? |
|---|---|---|
| pipeline con · pipeline cha | child · parent pipeline | Việt |
| pipeline hạ nguồn | downstream pipeline | Việt |
| job cầu | bridge job | **Có** — bridge |
| kích hoạt | trigger | **Có** — `trigger` |
| pipeline sinh lúc chạy | dynamic pipeline | Việt |
| chiến lược phụ thuộc | trigger strategy | **Có** — `strategy: depend` |
| chuyển tiếp biến | variable forwarding | **Có** — `trigger:forward` |
| kế thừa biến | variable inheritance | **Có** — `inherit:variables` |
| liên project | multi-project | **Có** — `trigger:project` |
| lồng nhau | nested pipeline | Việt |
| nguồn kích hoạt pipeline con | parent pipeline source | **Có** — `parent_pipeline` |
| tệp cấu hình sinh ra | generated config | Việt |
| kiểm cú pháp | lint | **Có** — `ci/lint` |
| ma trận job khai tay | hand-written job matrix | Việt |
| hợp đồng giữa hai đội | cross-team contract | Việt |
| nạp cấu hình từ artifact | config from artifact | **Có** — `trigger:include:artifact` |
| lấy artifact từ pipeline khác | cross-pipeline artifact | **Có** — `needs:pipeline:job` |
| endpoint liệt kê bridge job | bridges endpoint | **Có** — `/bridges` |

Ba chữ dễ nói lẫn, phân biệt ngay tại đây vì cả buổi sẽ dùng:

- **`trigger`** là **khoá YAML** trong một job. **bridge** là **loại job** mà khoá đó tạo ra. **downstream** là **pipeline** ở đầu kia. Ba chữ, ba tầng khác nhau; nói lẫn thì câu hỏi "job đó tốn mấy phút runner" trở thành vô nghĩa.
- **child** và **multi-project** khác nhau ở **repo**, không ở cú pháp: `trigger:include` là child, `trigger:project` là multi-project.
- **`inherit:variables`** cắt biến của cha đi xuống; **`trigger:forward`** điều khiển việc chuyển tiếp qua biên giới. Hai khoá, hai chỗ khai, không thay được nhau (§6 QT 6.4).



`t0` của buổi 04 là **một thời điểm**, không phải một khái niệm trừu tượng: đó là lúc GitLab đọc cấu hình, lọc `rules`, và chốt danh sách job. Sau thời điểm đó không gì đổi được danh sách ấy.

Pipeline con cho ta một thời điểm **thứ hai** như vậy, muộn hơn. Khoảng cách giữa hai thời điểm bằng đúng thời lượng các job cha chạy trước bridge job — trong bài lab là **8–15 giây** của job `sinh-cau-hinh`. Trong 8–15 giây đó ta được phép làm mọi thứ một script làm được: `git diff`, gọi API, đọc tệp, tính toán. Kết quả của việc tính toán đó **có mặt** ở `t0` thứ hai.

Đó là toàn bộ lợi ích của buổi này. Mọi thứ còn lại — `strategy: depend`, `forward`, lint — là cách tiêu thụ hoặc cách trả giá cho một câu đó. Mô hình này quay lại ở buổi **11**, **22**, **27**, **44**.

### 3.3. Mô hình tư duy 2: bridge job miễn phí

Job `trigger` không chạy trên runner. Không container, không clone, không tám pha của buổi 01 QT 4.2, nên **0 slot** và **0 phút runner**. Việc tạo một pipeline là việc của server GitLab; bridge job chỉ là **bản ghi** của hành động đó, và bản ghi ấy nằm ở endpoint `/bridges` chứ không ở `/jobs`.

Đây là chỗ **định lượng ngược lại** của buổi: người ta hay lo "tách pipeline ra thì tốn thêm tài nguyên". Phần tách thì gần như miễn phí — **~2 giây** để pipeline con xuất hiện. Cái tốn tiền là **job trong** pipeline con, và chúng tốn đúng như job thường, không hơn không kém.

Nhưng đọc một mình câu đó thì sai: cái nó tạo ra không miễn phí (§7 QT 7.1). Hai câu phải đọc cùng lúc. Quay lại ở buổi **11**, **22**, **44**, **46**.

### 3.4. Mô hình tư duy 3: ba câu hỏi sở hữu

Với mỗi quan hệ pipeline, hỏi đúng ba câu, theo thứ tự, trước khi gõ một dòng YAML nào:

1. **Ai giữ YAML** của pipeline đầu kia?
2. **Ai xem được log** của nó — đội ta có quyền đọc job của project đó không?
3. **Ai đổi được nó mà không cần merge request của ta?**

Ba câu này biến một lựa chọn trông như cú pháp (`include` hay `project`) thành một lựa chọn tổ chức. Với child pipeline, cả ba câu đều trả lời "chính ta". Với multi-project, câu 1 và câu 3 đổi chủ — và đó là lúc pipeline của ta hỏng vì một commit không nằm trong repo của ta (buổi 08 QT 7.2, lần thứ 2). Quay lại ở buổi **11**, **24**, **44**, **45**.

### 3.5. Mô hình tư duy 4: bằng chứng phải nằm ngoài repo

Tám buổi qua, câu hỏi "pipeline chạy gì" luôn trả lời được bằng `git show <commit>:.gitlab-ci.yml`. Từ hôm nay, câu đó có thể không trả lời được: tập job thật của một lần chạy do một script sinh ra tại thời điểm đó, từ trạng thái repo tại thời điểm đó.

Hệ quả thực dụng, không phải triết lý: nếu ta không **lưu** tệp sinh ra làm artifact `when: always`, thì một sự cố hôm qua là **không điều tra được** — không có bản gốc để so. Đây là lý do báo cáo gỡ rối bốn dòng của buổi 07 QT 7.3 phải có dòng thứ **năm**: tệp cấu hình thật của lần chạy đó. Quay lại ở buổi **22**, **27**, **34**, **42**.

---

### 1.1. Vì sao YAML tĩnh không đủ, và `t0` thứ hai (9 phút)

Mục này trả lời câu hỏi trung tâm số 1. Thứ tự lập luận: (1) YAML tĩnh thất bại ở đâu và bằng con số nào; (2) pipeline con cho ta cái gì mới về **thời điểm**; (3) có ba loại quan hệ, và chọn sai loại là sai về **tổ chức**, không phải sai cú pháp.

**Nguyên lý cốt lõi:** YAML tĩnh buộc ta liệt kê **mọi** tổ hợp job **trước** khi biết commit sắp tới đổi cái gì; với monorepo, số khối phải bảo trì bằng **số module × số job mỗi module**. `rules:changes` cắt bớt job được **chạy** nhưng **không** cắt được số khối phải **viết**.

**Giải thích cơ chế ngầm:** Tệp cấu hình được đọc ở `t0` — trước khi có bất kỳ tiến trình nào của ta chạy. Vì vậy nó không thể chứa **kết quả của một phép tính** về repo; nó chỉ chứa được các **điều kiện** mà nền tảng biết cách tự đánh giá. `rules:changes` là một điều kiện như thế: nó bật/tắt một khối **đã có sẵn**. Không có khối thì không có gì để bật. Hệ quả là hai đại lượng khác nhau bị lẫn vào nhau — số job **chạy** (nền tảng cắt được) và số khối **bảo trì** (nền tảng không cắt được gì). Đây là suy từ cơ chế, loại (b).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> `.gitlab-ci.yml` dài trên **500** dòng mà khoảng **90%** là khối chép lại, khác nhau đúng một chuỗi tên module. Dấu hiệu thứ hai, nặng hơn: **thêm một module thành một merge request sửa YAML** — nghĩa là việc thêm mã nguồn và việc thêm cấu hình đã dính vào nhau, và người thêm module phải hiểu cả pipeline. Dấu hiệu thứ ba, đo được: `git log --oneline -- .gitlab-ci.yml | wc -l` cho ra con số cùng bậc với số module đã thêm trong năm.

**Minh hoạ.**

```yaml
# mảnh — dán vào .gitlab-ci.yml của một monorepo. ĐÂY LÀ CÁCH TĨNH, để ĐẾM khối.
.mau-module:
  image: alpine:3.20
  before_script: ['cd "$MODULE"']

lint-api:
  extends: .mau-module
  variables: {MODULE: api}
  script: ['echo lint $MODULE']
  rules: [{changes: ['api/**/*']}]

test-api:                                  # chép y hệt, đổi 1 chữ
  extends: .mau-module
  variables: {MODULE: api}
  script: ['echo test $MODULE']
  rules: [{changes: ['api/**/*']}]
# build-api: khối thứ 3 của module api, cũng y hệt.
# ... rồi lặp cho web, worker và 9 module còn lại: 33 khối nữa.
# 12 × 3 = 36 khối × ~15 dòng = khoảng 540 dòng phải bảo trì.
# Cách ĐỘNG thay toàn bộ khối trên bằng 1 job sinh cấu hình + 1 bridge job: xem §6 QT 6.1.
```

**Con số chốt.** **12 × 3 = 36** khối, khoảng **540** dòng phải bảo trì; pipeline động cần **1** khối `trigger` cộng **1** script khoảng **40** dòng, và con số 40 **không tăng** khi số module tăng. Thêm module thứ 13 trong cách tĩnh là **+3** khối và **+45** dòng; trong cách động là **0** dòng YAML.

> **Nêu ra rồi phá bỏ.** Hai con số "36 khối, 540 dòng" là số của **ví dụ 12 module × 3 job**, không phải hằng số của nghề. Monorepo **3** module cho **9** khối, khoảng 135 dòng — và ở quy mô đó YAML tĩnh **đơn giản hơn** pipeline động, vì nó không thêm một tệp cấu hình nằm ngoài `git log`. Ngưỡng thực dụng của khoá này: dưới **10** khối chép lại thì đừng dùng pipeline động (§8 phần "Khi nào KHÔNG nên dùng"). Theo kinh nghiệm thực tế, đội nào áp pipeline động cho repo 3 module đều quay lại YAML tĩnh trong vòng một quý, vì cái giá 8–15 giây mỗi lần chạy không mua lại được gì.

**Nguyên lý cốt lõi:** Pipeline con có `t0` **riêng**: `rules` của job trong pipeline con được đánh giá lúc **pipeline con** được tạo, tức lúc job `trigger` chạy — muộn hơn `t0` của cha. Hệ quả lớn nhất: biến do job cha sinh ra **dùng được** trong `rules` của pipeline con, thứ mà buổi 04 QT 4.2 nói là không thể trong một pipeline.

**Giải thích cơ chế ngầm:** Hai pipeline là **hai lần tạo** khác nhau. Lần tạo thứ nhất xảy ra khi chưa có gì của ta chạy; lần thứ hai xảy ra khi lần thứ nhất **đã chạy được một phần**, nên nó thấy được kết quả của phần đó. Không có cơ chế mới nào ở đây — quy tắc "`rules` đánh giá một lần lúc pipeline được tạo" của buổi 04 QT 4.1 vẫn đúng nguyên văn, **lần thứ 3** khoá này dùng nó. Cái đổi là ta có **hai** lần tạo thay vì một. Loại (b).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Người ta vẫn cố dùng biến `dotenv` trong `rules` của **cùng** một pipeline, thấy `rules` không khớp, rồi kết luận "GitLab hỏng" hoặc "dotenv không hoạt động". Triệu chứng chính xác: job biến mất khỏi pipeline (buổi 04 QT 6.2 — biến mất, không phải `skipped`), và log của job sinh biến thì hoàn toàn bình thường. Dấu hiệu thứ hai: người ta thay `rules` bằng một `if` **trong** `script` rồi `exit 0` — job vẫn hiện màu xanh nhưng chẳng làm gì, tức đổi một lỗi ồn ào thành một lỗi im lặng.

**Minh hoạ.**

```yaml
# .gitlab-ci.yml — pipeline CHA. Chạy được, dưới 20 giây.
stages: [chuan-bi, kich-hoat]

sinh-bien:
  stage: chuan-bi
  image: alpine:3.20
  script:
    - echo "MODULE_DOI=api" > bien.env            # thực tế: tính từ git diff, §6 QT 6.3
    - cat bien.env
  artifacts:
    reports:
      dotenv: bien.env

kich-hoat-con:
  stage: kich-hoat
  needs: [sinh-bien]                              # cần needs để nhận biến dotenv (buổi 06 QT 4.3)
  variables:
    MODULE_DOI: $MODULE_DOI                       # khai ở cấp JOB của bridge — §6 QT 6.4
  trigger:
    include: con.yml
    strategy: depend
```

```yaml
# con.yml — pipeline CON. rules dưới đây đánh giá ở t0 THỨ HAI, nên $MODULE_DOI đã có giá trị.
chay-api:
  image: alpine:3.20
  script:
    - ': "${MODULE_DOI:?thiếu MODULE_DOI}"'       # buổi 06 QT 5.2 — chặn ca rỗng và xanh
    - echo "chạy cho module $MODULE_DOI"
  rules:
    - if: '$MODULE_DOI == "api"'                  # việc buổi 04 QT 4.2 nói là KHÔNG THỂ
```

**Con số chốt.** **2** thời điểm `t0` trong **một** lần push. Khoảng cách giữa chúng bằng thời lượng các job cha chạy trước bridge — trong bài lab là **8–15 giây**. Đo được bằng một lệnh: `created_at` của pipeline con trừ `created_at` của pipeline cha.

```bash
# Đo khoảng cách giữa hai t0 — chạy sau khi pipeline cha xong
CHA=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE" | jq -r .created_at)
CON=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/bridges" \
  | jq -r '.[0].downstream_pipeline.created_at')
echo "t0 cha=$CHA · t0 con=$CON · cách nhau $(( $(date -d "$CON" +%s) - $(date -d "$CHA" +%s) )) giây"
```

> **Nêu ra rồi phá bỏ.** Câu "`t0` thứ hai cho ta dùng biến `dotenv` trong `rules`" chỉ đúng với biến được **truyền tường minh** qua `trigger`. Không phải mọi biến của cha tự nhiên có mặt ở con: nếu bỏ dòng `variables:` ở cấp job bridge trong ví dụ trên, `rules:if` của job con so sánh với **chuỗi rỗng**, job biến mất, và pipeline con có thể **không được tạo** vì không còn job nào (§6 QT 6.1). Phải đọc QT 4.2 cùng với §6 QT 6.4.

**Nguyên lý cốt lõi:** Có **ba** loại quan hệ pipeline, và chúng khác nhau ở **quyền sở hữu**, không ở cú pháp: child (cùng repo, ta giữ YAML), multi-project (repo khác, **đội khác** giữ YAML), và lồng nhau (con của con). Chọn loại nào là quyết định tổ chức.

**Giải thích cơ chế ngầm:** Cú pháp của cả ba gần như giống nhau — cùng khoá `trigger`, khác một khoá con — nên người ta chọn theo tiện tay. Nhưng thứ khác nhau thật là **ai đổi được cấu hình mà không cần merge request của ta**. Với `trigger:include`, tệp YAML nằm trong repo ta, nên mọi thay đổi đi qua quy trình review của ta. Với `trigger:project`, tệp YAML nằm ở repo khác: một commit của đội khác đổi hành vi pipeline của ta ngay lần chạy sau, và `git log` của repo ta **không có dấu vết nào**. Đây là cùng một hợp đồng mà buổi 08 QT 7.2 đã nêu cho `needs:project`, **lần thứ 2**. Loại (a) về cú pháp, loại (b) về hệ quả tổ chức.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline hỏng, và commit gần nhất của repo ta **không liên quan gì** tới chỗ hỏng — dấu hiệu nhận ra trong 10 giây: `git log -1` cho một commit sửa `README` trong khi bridge job đỏ. Dấu hiệu thứ hai: mở log pipeline hạ nguồn thì gặp **403**, vì đội ta không có quyền đọc job của project đó — lúc này ta có một phụ thuộc mà ta **không** debug được, và câu hỏi sở hữu số 2 đã bị bỏ qua từ đầu.

**Minh hoạ.**

```yaml
# mảnh — ba khối trigger cạnh nhau, dán được. Khác nhau đúng một khoá con.
con-cung-repo:                  # (1) CHILD — ta giữ YAML
  trigger:
    include: ci/con.yml
    strategy: depend

con-repo-khac:                  # (2) MULTI-PROJECT — đội khác giữ YAML
  trigger:
    project: nhom-ha-tang/lab09-goi-chung
    branch: main
    strategy: depend

con-long-them-tang:             # (3) LỒNG NHAU — con này bên trong lại có trigger nữa
  trigger:
    include: ci/con-co-trigger.yml
    strategy: depend
```

| Câu hỏi sở hữu | child (`include`) | multi-project (`project`) | lồng nhau |
|---|---|---|---|
| Ai giữ YAML | ta | **đội khác** | ta, nhưng ở **2** tệp |
| Ai xem được log | ta | tuỳ quyền — có thể **403** | ta, phải đi qua **2** lần nhấp |
| Ai đổi được mà không xin phép ta | không ai | **đội khác**, ngay lần chạy sau | ta |
| Điều tra một sự cố mất mấy bước | 1 | 2 và cần người của đội kia | 3 tầng bridge phải mở lần lượt |

**Con số chốt.** **3** loại quan hệ; **3** câu hỏi sở hữu phải trả lời **trước** khi chọn. Với multi-project, số đội phải liên hệ khi điều tra tăng từ **1** lên **2** — và đó là con số quyết định, không phải số dòng YAML.

> **Nếu có Ultimate:** bậc trả tiền có biểu đồ phụ thuộc giữa các project và cảnh báo khi một project bị nhiều project khác trỏ vào, nên câu hỏi sở hữu số 3 trả lời được bằng một trang giao diện. Trên CE 17.7, ba câu hỏi đó trả lời bằng cách **viết ra** trong tài liệu của đội — và bài lab không phụ thuộc vào bản có license: `trigger:project` giữa hai project trong cùng instance CE chạy được, lab bước 5 đo điều đó.

---

### 1.2. `trigger`: bridge job, `strategy: depend`, và artifact hai chiều (9 phút)

Ba quy tắc của mục này trả lời ba câu theo thứ tự: bridge job **tốn gì**, nó **nói thật hay không**, và **cái gì chảy qua** biên giới hai pipeline. Câu thứ hai là chế độ hỏng đặc trưng của cả buổi.

**Nguyên lý cốt lõi:** Job `trigger` là **bridge job**: nó **không** chạy trên runner. Không chiếm slot, không tốn phút runner, và không có `trace` theo tám pha như job thường. Đây là thứ rẻ nhất trong cả khoá — và cũng là lý do người ta lạm dụng nó.

**Giải thích cơ chế ngầm:** Việc tạo một pipeline là việc của **server** GitLab, không phải việc của runner: server đọc cấu hình, lọc `rules`, ghi các bản ghi job vào cơ sở dữ liệu. Không có gì trong chuỗi việc đó cần một container. Bridge job là **bản ghi của hành động tạo pipeline** ấy, nên nó không có `image`, không có `script`, không đi qua tám pha của buổi 01 QT 4.2, và không xuất hiện trong hàng đợi mà `concurrent` giới hạn (buổi 02 QT 6.1). Bằng chứng cơ học: GitLab để nó ở một endpoint API **khác**. Loại (a) về cơ chế, và việc "nó không có mặt ở `/jobs`" là loại (c) — lab đo bằng cách gọi cả hai endpoint.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Người ta mở bridge job đi tìm log `script` và không thấy gì, rồi kết luận job "không chạy" hoặc "log bị mất". Dấu hiệu thứ hai, tốn tiền hơn: một đội thấy pipeline chậm khi bật child pipeline và đi **tăng `concurrent`** của runner, trong khi thủ phạm là **job trong** pipeline con — bridge job không chiếm slot nào. Dấu hiệu thứ ba, gặp khi viết script: `curl .../pipelines/$PIPE/jobs | jq '.[].name'` không liệt kê tên bridge job, nên vòng lặp kiểm trạng thái bỏ sót nó và báo "pipeline không có job nào tên `kich-hoat-con`".

**Minh hoạ.**

```bash
# Bằng chứng bằng MỘT cặp lệnh: bridge job KHÔNG nằm ở /jobs.
echo "=== /jobs (job chạy trên runner) ==="
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs" \
| jq -r '.[] | [.name, .status, (.duration // 0 | floor)] | @tsv'

echo "=== /bridges (job trigger) ==="
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/bridges" \
| jq -r '.[] | [.name, .status,
                (.downstream_pipeline.id // "khong-tao-duoc"),
                (.downstream_pipeline.status // "-")] | @tsv'
```

**Con số chốt.** **0** slot runner, **0** phút runner, khoảng **2** giây từ lúc bridge job bắt đầu tới lúc pipeline con có `id`. Trong bảng chi phí ở §7, đây là dòng duy nhất có cả ba con số bằng 0 hoặc gần 0 — và cũng là dòng bị trích dẫn sai nhiều nhất.

> **Nêu ra rồi phá bỏ.** "Bridge job 0 phút runner" đúng về **phút runner** và chỉ về phút runner. Nó vẫn tốn một bản ghi pipeline, vẫn tính vào hạn mức số pipeline, và **pipeline con vẫn tốn slot như mọi pipeline khác**. QT 5.1 và §7 QT 7.1 phải đọc **cùng lúc**; ai chỉ nhớ một nửa sẽ dùng pipeline con để "lách" giới hạn và gặp lỗi tạo pipeline ở module thứ 20.

**Nguyên lý cốt lõi:** Không có `strategy: depend`, job `trigger` **xanh ngay** khi tạo được pipeline con và **không** phản ánh kết quả của nó: pipeline cha xanh trong khi pipeline con đỏ. Đây là chế độ hỏng im lặng số một của buổi.

**Giải thích cơ chế ngầm:** Mặc định, nhiệm vụ của bridge job chỉ là *tạo được* pipeline kia. Tạo được thì thành công — kết quả của pipeline kia là một việc **khác**, xảy ra sau, và nền tảng không tự nối hai việc đó lại. `strategy: depend` là khoá nói "trạng thái của tôi bằng trạng thái của pipeline hạ nguồn": bridge job chuyển sang `running` và ở đó cho tới khi pipeline con kết thúc, rồi **phản chiếu** trạng thái. Nhìn theo bảng hai thuộc tính của buổi 01 QT 7.1 (**lần thứ 9**): không có dòng đó, hỏng nằm ở ô *im lặng + không chặn* — ô nguy hiểm nhất; có dòng đó, nó về ô *ồn ào + có chặn*. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Huy hiệu pipeline của nhánh mặc định **xanh** suốt tuần, còn danh sách pipeline có những dòng con **đỏ** mà không ai mở ra. Dấu hiệu thứ hai, đo được bằng một lệnh: đếm số pipeline cha `success` có pipeline con `failed` trong 30 ngày — con số này thường làm cả đội im lặng một lúc (§8 phần "Đo trước — đo sau"). Dấu hiệu thứ ba: `duration` của bridge job xấp xỉ **0–2 giây** trong khi pipeline con chạy **5 phút**; hai số lệch nhau hai bậc là dấu hiệu cơ học rằng cha không hề chờ con.

**Minh hoạ.**

```yaml
# .gitlab-ci.yml — hai bridge job cạnh nhau, cùng gọi một pipeline con LUÔN ĐỎ.
# Đây là ca đối chứng PHẢI THẤT BẠI của lab bước 2: kết quả đúng là 1 xanh, 1 đỏ.
khong-cho:
  trigger:
    include: con-do.yml
    # KHÔNG có strategy → xanh ngay, dù con đỏ. Im lặng, không chặn.

co-cho:
  trigger:
    include: con-do.yml
    strategy: depend          # 1 dòng: đỏ theo con. Ồn ào, có chặn.
```

```yaml
# con-do.yml — pipeline con cố ý thất bại
that-bai:
  image: alpine:3.20
  script: ['echo "con chạy rồi và sắp đỏ"', 'exit 1']
```

Bằng chứng là hai dòng của lệnh `/bridges` ở QT 5.1: kỳ vọng đúng là `khong-cho success failed` và `co-cho failed failed` — cùng một pipeline con, hai trạng thái cha khác nhau.

**Con số chốt.** **1** dòng `strategy: depend` đổi ô của bảng hai thuộc tính từ *im lặng + không chặn* sang *ồn ào + có chặn*, và tốn **0** giây thêm — pipeline con vẫn chạy đúng thời lượng đó, chỉ khác là cha **chờ** nó. Đây là thay đổi rẻ nhất và lợi nhất của cả buổi: **1** dòng, **0** giây, đổi ô nguy hiểm nhất của bảng.

> **Nếu có Ultimate:** merge train và bảo vệ nhánh nâng cao ở bậc trả tiền cho thêm cách chặn merge theo trạng thái pipeline hạ nguồn. Chúng **không** thay `strategy: depend`: nếu bridge job đã xanh sai thì mọi lớp phía trên đều đọc một sự thật sai. Trên CE 17.7, dòng `strategy: depend` là cơ chế duy nhất nối trạng thái hai pipeline, và bài lab dùng đúng nó.

**Nguyên lý cốt lõi:** Artifact **không** tự chảy giữa hai pipeline: pipeline con không tự nhận artifact của cha ngoài những gì được truyền tường minh, và pipeline cha **không** tự nhận artifact của con — muốn lấy phải khai `needs:pipeline:job`.

**Giải thích cơ chế ngầm:** Hợp đồng artifact của buổi 05 có phạm vi là **một** pipeline: mặc định "job tải artifact của mọi job ở các stage trước" (buổi 05 QT 5.1) được định nghĩa **trong** một pipeline, nên qua biên giới nó không còn ý nghĩa. Không có mặc định nào thay thế — nghĩa là qua biên giới, mặc định là **không có gì**. Đây là điểm dễ nhầm nhất của buổi vì nó **ngược** với trực giác đã hình thành ở buổi 05 và buổi 08. Đại lượng "artifact của con có tự về cha không" là loại (c) — lab đo bằng cách in `find . -type f | wc -l` trong job cha sau bridge, **không** kết luận từ tài liệu.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job cha chạy sau `trigger` làm việc với **0** tệp và vẫn **xanh**, vì `script` không có khẳng định nào (buổi 05 QT 5.3, **lần thứ 2** trong khoá này ở dạng "job xanh mà thư mục rỗng"). Triệu chứng đọc được: `ls -la` trong log cho một thư mục chỉ có mã nguồn từ git; hoặc một lệnh `jq` trên tệp báo cáo im lặng trả về `null` rồi được ghi tiếp vào một tệp tổng hợp — lúc này con số sai đã đi ra ngoài pipeline.

**Minh hoạ.**

```yaml
# mảnh — lấy artifact của pipeline CON về pipeline CHA, kèm khẳng định.
# Dán vào pipeline cha, sau job trigger có strategy: depend.
gop-bao-cao:
  stage: tong-hop
  image: alpine:3.20
  needs:
    - job: kich-hoat-con
      artifacts: false                    # chỉ chờ bridge, không lấy gì từ nó
    - pipeline: $CI_PIPELINE_ID           # lấy từ pipeline CON của chính lần chạy này
      job: gop
  script:
    - test -s bao-cao.json || { echo "THIẾU bao-cao.json từ pipeline con"; exit 1; }
    - echo "số dòng: $(wc -l < bao-cao.json)"
```

```yaml
# con.yml — phía pipeline CON phải công bố artifact đúng tên job "gop"
gop:
  image: alpine:3.20
  script: ['echo "{\"module\":\"api\",\"ket_qua\":\"ok\"}" > bao-cao.json']
  artifacts:
    paths: [bao-cao.json]
    when: always
```

**Con số chốt.** **2** chiều phải khai riêng: xuống con bằng `trigger:forward`/`variables` (§6 QT 6.4), lên cha bằng `needs:pipeline:job`. Và **1** dòng `test -s` là thứ duy nhất biến ca thiếu tệp từ *im lặng* thành *ồn ào* — cùng một dòng, cùng một lý do như buổi 05, chỉ khác là biên giới rộng hơn.

---

### 1.3. Pipeline sinh lúc chạy: bốn bước, và lint trước khi trigger (11 phút)

Đây là mục dài nhất và là chỗ hiện vật chính của buổi được dựng: `sinh-pipeline.sh`. Bốn quy tắc đi theo đúng thứ tự làm: cấu trúc bốn bước, chặn lỗi cú pháp, tính đúng "đổi những gì", và đưa biến xuống.

**Nguyên lý cốt lõi:** Pipeline động là đúng **bốn** bước, không rút ngắn được bước nào: (1) một job đọc trạng thái repo; (2) nó **viết ra** một tệp YAML; (3) tệp đó thành **artifact**; (4) một bridge job dùng `trigger:include:artifact`. Nếu tệp sinh ra **rỗng job**, pipeline con **không được tạo** — đúng ca **0 job → 0 pipeline** của buổi 04 QT 4.3, lần thứ 2.

**Giải thích cơ chế ngầm:** Bridge job chỉ đọc được thứ đã nằm trong **kho artifact** của GitLab; không có đường nào cho nó đọc trực tiếp đầu ra của một job khác, vì hai job không dùng chung hệ tệp (buổi 01 QT 4.1 — môi trường dùng một lần) và log không phải đường ra (buổi 01 QT 5.4). Vì vậy bước 3 không phải thủ tục hành chính: nó là **đường duy nhất** để tệp sinh ra tới được server. Còn ca 0 job là hệ quả trực tiếp của buổi 04 QT 4.3: quy tắc "pipeline không còn job nào thì không được tạo" áp cho **mọi** pipeline, kể cả pipeline con. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bridge job đỏ với lỗi không tìm thấy cấu hình — thường vì thiếu khoá `job:` trong `trigger:include:artifact`, hoặc vì job sinh cấu hình không khai `artifacts:paths`. Ca im lặng hơn và nguy hiểm hơn: pipeline con **không xuất hiện** mà không có lỗi nào rõ ràng, vì tệp sinh ra hợp lệ về cú pháp nhưng **không có job nào** — đúng ca commit chỉ sửa `README`. Kiểm bằng một lệnh: `jq '.[0].downstream_pipeline'` trên `/bridges` trả về `null`.

**Minh hoạ.**

```yaml
# .gitlab-ci.yml — đủ BỐN bước, dán được, chạy dưới 30 giây.
stages: [chuan-bi, kich-hoat]

sinh-cau-hinh:                                     # bước 1 + 2 + 3
  stage: chuan-bi
  image: alpine:3.20
  script:
    - apk add --no-cache git bash curl jq >/dev/null
    - bash ci/sinh-pipeline.sh > con.yml           # bước 1 (đọc repo) + bước 2 (viết ra)
    - test -s con.yml || { echo "con.yml rỗng"; exit 1; }
    - grep -qE '^[a-z0-9_-]+:' con.yml || { echo "con.yml KHÔNG có job nào"; exit 1; }
  artifacts:                                       # bước 3
    paths: [con.yml]
    when: always
    expire_in: 7 days

kich-hoat-con:                                     # bước 4
  stage: kich-hoat
  needs: [sinh-cau-hinh]
  trigger:
    include:
      - artifact: con.yml
        job: sinh-cau-hinh                         # thiếu dòng này là lỗi hay gặp nhất
    strategy: depend
```

```bash
# ci/sinh-pipeline.sh — nhánh xử lý ca "không module nào đổi" (phần đầu của hiện vật chính)
DOI=$(git diff --name-only "$(git merge-base "origin/$CI_DEFAULT_BRANCH" HEAD)"...HEAD \
      | cut -d/ -f1 | sort -u | grep -xE 'api|web|worker' || true)

if [ -z "$DOI" ]; then
  # KHÔNG sinh tệp rỗng. Sinh MỘT job giữ chỗ — pipeline con vẫn tồn tại và xem được.
  cat <<'YAML'
khong-co-gi-doi:
  image: alpine:3.20
  script: ['echo "không module nào đổi — pipeline con vẫn được tạo để có bằng chứng"']
YAML
  exit 0
fi
```

**Con số chốt.** **4** bước, bỏ bước nào cũng hỏng và mỗi bước hỏng một kiểu khác: bỏ bước 1 thì cấu hình không phản ánh repo; bỏ bước 2 thì không có gì để nạp; bỏ bước 3 thì bridge job đỏ vì không tìm thấy tệp; bỏ bước 4 thì tệp sinh ra chỉ là một artifact không ai đọc. Ca 0 job phải xử lý tường minh bằng **1** job giữ chỗ — **3** dòng YAML, đổi một pipeline vắng mặt im lặng thành một pipeline xem được.

**Nguyên lý cốt lõi:** YAML sinh ra phải được **lint bằng `ci/lint` trước khi** trigger, trong cùng job đã sinh nó. Sinh bằng công cụ biết YAML (script có kiểm) chứ không bằng nối chuỗi `echo`, vì lỗi thụt lề của một tệp sinh ra khó thấy hơn lỗi thụt lề của một tệp trong repo.

**Giải thích cơ chế ngầm:** `ci/lint` trả về tệp **sau phân giải** (buổi 03 QT 4.3, **lần thứ 2**), nên nó bắt được cả lỗi cú pháp lẫn lỗi cấu trúc — job trỏ tới stage không tồn tại, `needs` trỏ job vắng mặt — **trước khi** ta tốn một lần tạo pipeline. Cái làm quy tắc này khác một lời khuyên: lệnh lint nằm **trong chính job đã sinh tệp**, và nó tự `exit 1`. Không phải "nhớ lint" mà là "không lint thì không đi tiếp được". Lý do thụt lề sai của tệp sinh ra khó thấy hơn: không ai review nó, editor không mở nó, và `git show` không có nó. Loại (b).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bridge job đỏ với thông báo lỗi cú pháp ở **dòng 47** của một tệp mà `git show` không tìm thấy — người điều tra đọc `.gitlab-ci.yml` ở dòng 47 và thấy một dòng hoàn toàn bình thường, rồi mất 20 phút. Dấu hiệu thứ hai: một `echo` nối chuỗi có biến chứa dấu hai chấm hoặc dấu `#`, tệp sinh ra vẫn hợp lệ về YAML nhưng **ý nghĩa đổi** — pipeline con được tạo, xanh, và làm sai việc.

**Minh hoạ.**

```bash
# ci/sinh-pipeline.sh — phần cuối: TỰ lint, TỰ exit 1. Đây là cơ chế, không phải lời khuyên.
# Lưu ý: phần này in ra stderr để không lẫn vào con.yml trên stdout.
lint_hoac_chet() {
  local tep="$1" kq
  kq=$(jq -Rs '{content: .}' < "$tep" \
       | curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
              --header 'Content-Type: application/json' \
              --data @- "$GITLAB/api/v4/projects/$PID/ci/lint")
  if [ "$(echo "$kq" | jq -r .valid)" != "true" ]; then
    echo "LINT SAI — không trigger:" >&2
    echo "$kq" | jq -r '.errors[], .warnings[]?' >&2
    exit 1
  fi
  echo "lint OK — $(echo "$kq" | jq -r '.merged_yaml | split("\n") | length') dòng sau phân giải" >&2
}
lint_hoac_chet /tmp/con.yml
cat /tmp/con.yml          # chỉ in ra khi đã hợp lệ
```

**Con số chốt.** **1** lệnh lint chạy khoảng **1** giây, chặn được **toàn bộ** lớp lỗi cú pháp trước khi tạo pipeline. So sánh chi phí: 1 giây lint so với một vòng "đẩy commit → chờ pipeline cha → bridge đỏ → sửa script → đẩy lại", mà một vòng như thế tốn **2–5 phút** kể cả thời gian chờ của người viết.

**Nguyên lý cốt lõi:** Pipeline động giải được ca thứ ba của `rules:changes` — ca mà `changes:compare_to` **không** sửa được — vì việc "đổi những gì" được tính bằng **lệnh `git` trong job**, nơi ta chọn được mốc so sánh và xử lý được ca push nhiều commit.

**Giải thích cơ chế ngầm:** Trong một job ta có **cả cây git và cả quyền chạy lệnh**; ở `t0` thì không có gì ngoài cơ chế của nền tảng. Buổi 04 QT 6.3 nêu ba ca mốc so sánh sai: nhánh mới, pipeline theo lịch, push nhiều commit một lần; `changes:compare_to` sửa được hai ca đầu vì nó cho ta khai một ref cố định, nhưng ca push nhiều commit thì cần một phép tính (`merge-base` với nhánh mặc định) mà cú pháp `rules` không có chỗ để viết. Trong job thì đó là một dòng lệnh. **Lần thứ 2** khoá này quay lại ba ca đó, và lần này là lần **giải quyết**. Loại (b).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Vẫn còn những lần chạy mà job của module **đã đổi** không chạy — đây là ca im lặng: pipeline xanh, ngắn hơn bình thường, và module vừa sửa **không được test**. Hoặc chiều ngược lại: **mọi** module đều chạy dù chỉ sửa một tệp `README`, nghĩa là script rơi về "chạy hết cho chắc" và ta đã trả tiền cho cả 36 job mà không nhận được gì. Kiểm bằng một lệnh trong log: in ra danh sách module script tính được và so với `git diff --name-only` của chính commit đó.

**Minh hoạ.**

```bash
# ci/sinh-pipeline.sh — bước 1: tính ĐÚNG danh sách module đã đổi, xử lý cả ba ca của buổi 04
git fetch --quiet origin "$CI_DEFAULT_BRANCH" || true

if [ "$CI_COMMIT_REF_NAME" = "$CI_DEFAULT_BRANCH" ]; then
  MOC="${CI_COMMIT_BEFORE_SHA}"                      # trên nhánh mặc định: so với lần push trước
  case "$MOC" in 0000000*) MOC="HEAD~1" ;; esac      # ca nhánh mới / push đầu tiên
else
  MOC="$(git merge-base "origin/$CI_DEFAULT_BRANCH" HEAD)"   # ca push nhiều commit: merge-base
fi

DOI=$(git diff --name-only "$MOC"...HEAD | cut -d/ -f1 | sort -u | grep -xE 'api|web|worker' || true)
echo "mốc=$MOC · module đổi=[${DOI:-khong-co}]" >&2   # dòng log này LÀ bằng chứng, đừng bỏ
```

**Con số chốt.** **3** ca của buổi 04 QT 6.3; `compare_to` sửa **2**; ca thứ **3** sửa ở đây bằng một lệnh `git merge-base`. Bài lab **đo cả ba** ca, không suy luận: nhánh mới, push nhiều commit, pipeline theo lịch.

> **Nêu ra rồi phá bỏ.** "Pipeline động giải được `rules:changes`" chỉ đúng ở ca **mốc so sánh**. Nó **không** giải được ca người viết script **chọn sai mốc** — nó chỉ chuyển trách nhiệm từ nền tảng sang ta. Trước đây mốc sai là hành vi mặc định của GitLab và ta không sửa được; giờ mốc sai là một dòng trong script của ta, ta sửa được, nhưng ta cũng **viết sai được**. Vì vậy dòng `echo "mốc=..."` ở trên không phải để đẹp: nó là bằng chứng duy nhất trong log cho biết script đã so với cái gì.

**Nguyên lý cốt lõi:** Biến xuống pipeline con theo **ba** đường khác nhau — khai ở cấp trên cùng, khai ở cấp job của bridge, và `trigger:forward` — và mặc định của mỗi đường **không** giống nhau; `inherit:variables` cắt được đường thứ nhất. Không đo thì không biết.

**Giải thích cơ chế ngầm:** Biến của pipeline con thuộc một trong **chín** nấc của buổi 06 QT 4.1, và việc truyền qua biên giới pipeline chèn thêm **một lớp quy tắc** lên trên chín nấc đó: biến khai ở cấp job của bridge đi xuống như **pipeline variable** của pipeline con, tức vào một nấc **cao**, nên nó ghi đè cả biến khai trong `con.yml`. Biến cấp trên cùng của cha đi xuống theo đường khác và `inherit:variables: false` cắt đúng đường đó. `trigger:forward` điều khiển hai loại riêng — biến YAML và biến của pipeline gốc. Ba đường, ba mặc định, và mặc định phụ thuộc phiên bản: đây là loại (c), **phải đo**, **lần thứ 2** khoá này nói câu đó về `inherit:variables` (buổi 06 QT 7.1).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline con chạy với biến **rỗng** và **xanh** — cả cha lẫn con đều xanh, còn việc thì không được làm. Đây là cùng một ô của bảng hai thuộc tính với biến `protected` thiếu ở buổi 06 QT 5.2, và cùng một cách chặn: `: "${VAR:?}"`. Dấu hiệu phân biệt "rỗng" với "lỗi": `${#VAR}` bằng **0** thì là rỗng — biến không xuống được; khác 0 mà sai giá trị thì là **đường khác thắng**, và lúc đó phải hỏi biến đó tới từ nấc nào.

**Minh hoạ.**

```yaml
# .gitlab-ci.yml — ba đường khai cạnh nhau, chạy được. In ra rồi ĐỌC SỐ, đừng đoán.
variables:
  DUONG_1: "khai-o-cap-tren-cung"

kich-hoat-day-du:
  variables:
    DUONG_2: "khai-o-cap-job-cua-bridge"
  trigger:
    include: con.yml
    strategy: depend
    forward:
      yaml_variables: true             # mặc định true — đo lại trên hệ thống của mình
      pipeline_variables: false        # mặc định false — đây là chỗ hay bị hiểu ngược

kich-hoat-cat-duong-1:
  inherit:
    variables: false                   # cắt biến cấp trên cùng của CHA
  variables:
    DUONG_2: "van-con-vi-khai-o-cap-job"
  trigger:
    include: con.yml
    strategy: depend
```

```yaml
# con.yml — pipeline con TỰ ĐO, in độ dài chứ không in giá trị (buổi 06 QT 6.2)
do-bien:
  image: alpine:3.20
  script:
    - 'printf "DUONG_1 len=%s\n" "${#DUONG_1}"'
    - 'printf "DUONG_2 len=%s\n" "${#DUONG_2}"'
    - 'printf "DUONG_3 len=%s\n" "${#DUONG_3}"'
    - ': "${DUONG_2:?DUONG_2 rỗng — biến không xuống được, dừng ngay}"'
```

**Con số chốt.** **3** đường khai; số biến xuống được là con số **phải đo** trên GitLab của lớp, không tra. Và mọi biến quan trọng phải có `: "${VAR:?}"` ở dòng đầu `script` của pipeline con (buổi 06 QT 5.2) — **1** dòng cho mỗi biến, đổi ca *im lặng + không chặn* thành *ồn ào + có chặn*.

---

### 1.4. Giới hạn, chi phí, và điều tra khi YAML không có trong repo (5 phút)

**Nguyên lý cốt lõi:** Pipeline con **không** miễn phí về hạn mức: job của nó tính vào giới hạn số job của một lần chạy, và độ sâu lồng nhau có trần. Bridge job rẻ, nhưng thứ nó tạo ra thì không.

**Giải thích cơ chế ngầm:** Nền tảng tính hạn mức theo **tài nguyên thật nó phải xếp lịch**, không theo cách ta chia pipeline: 60 job trong một pipeline con vẫn là 60 bản ghi job, 60 lần xếp lịch, và 60 lần chiếm slot runner. Việc tách chúng ra khỏi pipeline cha không đổi con số nào trong đó. Với độ sâu lồng nhau, GitLab đặt trần vì mỗi tầng thêm là một lần server phải theo dõi trạng thái phản chiếu — trần đó là loại (c), **phải đo**, vì nó đã đổi giữa các phiên bản.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline con bị **từ chối tạo** khi số module tăng, và thông báo lỗi nói về một giới hạn chưa ai trong đội từng đọc — thường xuất hiện ở bridge job, ồn ào và có chặn, nên đây là ca dễ nhất trong buổi. Ca khó hơn: mọi thứ tạo được nhưng job nằm `pending` lâu bất thường vì tổng slot cần cùng lúc đã vượt `min(concurrent, limit)` của buổi 02 QT 6.1 — lúc này pipeline động **không** nhanh hơn YAML tĩnh một giây nào, nó chỉ đổi thứ tự hàng đợi (buổi 08 QT 7.1).

**Minh hoạ.**

```bash
# ci/sinh-pipeline.sh --so-job N  → sinh N job giữ chỗ để ĐO trần. Lab bước 5 chạy N = 5, 20, 60.
N="${1:-5}"
for i in $(seq 1 "$N"); do
  printf 'job-%03d:\n  image: alpine:3.20\n  script: ["true"]\n' "$i"
done

# Đọc trần thật của instance. Nếu pipeline con KHÔNG được tạo thì lý do nằm ở /bridges,
# không nằm trong log của job nào — đó là chỗ hay bị tìm sai.
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/application/settings" \
| jq '{ci_max_total_yaml_size_bytes, max_yaml_size_bytes, max_yaml_depth}' 2>/dev/null
```

**Con số chốt.** Giá trị tham chiếu của độ sâu lồng nhau là **2** tầng dưới cha; trần số job của một pipeline là con số bài lab **phải đo** trên GitLab của lớp — lab sinh **5**, **20**, rồi **60** job và ghi lại kết quả kèm số phiên bản.

> **Nêu ra rồi phá bỏ.** Con số "**2** tầng" là giá trị tham chiếu của GitLab 17.7 và thuộc loại (c). Đừng dạy nó như một hằng số: nó đã đổi trong dòng 14.x–17.x, và một instance tự dựng có thể cấu hình khác. Cách đúng: lồng ba tầng trong lab, đọc thông báo lỗi thật, ghi con số kèm phiên bản — kết quả của lớp thắng con số trong bài giảng. Đây là **lần thứ 9** khoá này nói câu "phụ thuộc phiên bản thì phải đo, không tra".

**Bốn đại lượng loại (c) của buổi này — phải ĐO, không tra:**

| Đại lượng | Giá trị tham chiếu 17.7 | Cách đo |
|---|---|---|
| Bridge job có nằm ở `/jobs` không | **Không**, nó ở `/bridges` | Gọi cả hai endpoint và so danh sách (QT 5.1) |
| Artifact của con có tự về cha không | **Không** | Job cha in `find . -type f \| wc -l` sau bridge (QT 5.3) |
| Số biến xuống con theo **3** cách khai | Phải đo | Pipeline con in `${#VAR}` của ba biến, ba ca (QT 6.4) |
| Độ sâu lồng nhau tối đa · trần số job | **2** tầng · phải đo | Lồng ba tầng; sinh 5 · 20 · 60 job (QT 7.1) |

**Chi phí buổi này thêm vào pipeline:**

| Thứ thêm vào | Chi phí | Đọc cùng |
|---|---|---|
| Job `trigger` (bridge) | **0** slot, **0** phút runner, ~**2** giây tạo pipeline con | QT 5.1 — nhưng phải đọc cùng QT 7.1 |
| Job `sinh-cau-hinh` | **8–15** giây mỗi pipeline (clone + `git diff` + lint) — **cái giá thật** của pipeline động | QT 6.1, QT 6.2 |
| Lint YAML sinh ra | ~**1** giây, chặn cả lớp lỗi cú pháp | QT 6.2 |
| Lưu YAML sinh ra làm artifact `when: always` | ~**4** kB mỗi pipeline, `expire_in: 7 days` → khoảng **1,2** MB cho 300 pipeline | QT 7.2 |
| `strategy: depend` | **0** giây thêm; chỉ đổi ô bảng hai thuộc tính | QT 5.2 |
| Job **trong** pipeline con | Tính vào hạn mức và slot **như job thường** | QT 7.1 |

**Định lượng ngược lại — ba thứ người ta tưởng đắt mà không đắt:**

1. **Tách pipeline ra không tốn phút runner.** Bridge job **0** phút, **0** slot, ~**2** giây. Người ta hay hoãn việc tách vì sợ "thêm tầng thì thêm tài nguyên"; con số nói ngược lại.
2. **`strategy: depend` không làm pipeline chậm hơn.** **0** giây thêm — pipeline con vẫn chạy đúng thời lượng đó dù có dòng ấy hay không. Cái đổi là cha **biết** kết quả. Đây là dòng cấu hình có tỉ lệ lợi/giá tốt nhất trong buổi.
3. **Lưu cấu hình sinh ra rất rẻ.** **4** kB mỗi pipeline. 300 pipeline một tháng là **1,2** MB — nhỏ hơn một artifact báo cáo test bình thường, và nó là thứ duy nhất cho phép điều tra sự cố hôm qua.

**Nguyên lý cốt lõi:** Khi cấu hình sinh lúc chạy, `git show` **không còn** là bằng chứng. Vì vậy tệp YAML sinh ra phải là artifact với `when: always` (buổi 05 QT 5.4, lần thứ 2), và báo cáo gỡ rối bốn dòng của buổi 07 QT 7.3 phải có thêm **một** dòng: tệp cấu hình thật của lần chạy đó.

**Giải thích cơ chế ngầm:** Thứ gây lỗi **không nằm trong lịch sử git**: nó là kết quả của một script chạy trên một trạng thái repo tại một thời điểm, với một tập biến tại thời điểm đó. Ba yếu tố ấy không tái tạo được từ commit, nên không có cách nào dựng lại tệp cũ — trừ khi ta **đã lưu nó** đúng lần chạy đó. `when: always` là bắt buộc chứ không phải cẩn thận thêm: chính lần chạy **đỏ** là lần ta cần tệp, và mặc định của `artifacts` không đảm bảo giữ artifact khi job thất bại. Loại (b).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Một pipeline con hỏng hôm qua, hôm nay chạy lại thì bình thường, và **không ai chỉ ra được** YAML hôm qua khác hôm nay ở chỗ nào. Cuộc thảo luận chuyển sang "chắc là do mạng" và vé được đóng — cho tới lần sau. Dấu hiệu cơ học: mở pipeline cũ, tab artifact **rỗng**, và tệp cấu hình pipeline con chỉ còn tồn tại trong bộ nhớ của server dưới dạng đã phân giải mà không ai biết đường lấy.

**Minh hoạ.**

```yaml
# mảnh — dán vào job sinh cấu hình. Ba dòng này là toàn bộ khác biệt giữa
# "điều tra được" và "chắc là do mạng".
  artifacts:
    paths: [con.yml]
    when: always              # BẮT BUỘC: lần chạy đỏ mới là lần ta cần tệp
    expire_in: 7 days         # 4 kB × 300 pipeline ≈ 1,2 MB
```

```bash
# Điều tra sự cố HÔM QUA: lấy đúng con.yml của lần chạy đó về, rồi diff với hôm nay
art_tep() {   # art_tep <PIPELINE_ID> <TEN_JOB> <TEP>
  local pid_line job
  job=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        "$GITLAB/api/v4/projects/$PID/pipelines/$1/jobs" | jq -r ".[] | select(.name==\"$2\") | .id")
  curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/jobs/$job/artifacts/$3" -o "$3.$1"
  echo "đã lấy $3.$1 ($(wc -c < "$3.$1") byte)"
}
art_tep 4821 sinh-cau-hinh con.yml     # pipeline hôm qua
art_tep 4907 sinh-cau-hinh con.yml     # pipeline hôm nay
diff con.yml.4821 con.yml.4907         # dòng đầu tiên khác nhau LÀ nguyên nhân
```

**Con số chốt.** **1** artifact `when: always`; báo cáo gỡ rối của buổi này có **5** dòng thay vì 4. Dòng thứ năm: **tệp cấu hình thật của lần chạy đó**, kèm lệnh lấy nó về. Thiếu dòng thứ năm thì với pipeline động, ba dòng đầu là phỏng đoán.

**Mẫu báo cáo năm dòng.** Dòng 2 và dòng 5 đều phải là **lệnh in ra được**, không phải câu mô tả:

| # | Dòng | Với pipeline động thì viết gì |
|---|---|---|
| 1 | Triệu chứng | Trạng thái nào, ở pipeline **nào** — cha hay con; nêu cả hai `id` |
| 2 | **Bằng chứng** | Một lệnh: `/bridges` cho trạng thái hai bên, hoặc `trace` của job con |
| 3 | Nguyên nhân | Quy về một QT, và nêu ô của bảng hai thuộc tính |
| 4 | Cách sửa | Dòng cấu hình hoặc dòng script cụ thể |
| 5 | **Tệp cấu hình thật** | Một lệnh `art_tep <pipeline> sinh-cau-hinh con.yml`, kèm `diff` với lần xanh |

---

### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước

Ba việc, tổng **50 phút**, xếp theo rủi ro tăng dần. Việc 1 và 2 làm được ngay hôm nay mà không đụng tới ai.

**Việc 1 — 5 phút, rủi ro bằng 0, giá trị cao nhất trên mỗi dòng.** `grep -n 'trigger:' .gitlab-ci.yml`. **Mọi** bridge job không có `strategy: depend` là một chỗ pipeline cha đang **nói dối** (QT 5.2). Thêm dòng đó trước khi làm bất cứ việc nào khác trong buổi này: **0** giây chi phí, và nó đổi ô nguy hiểm nhất của bảng hai thuộc tính. Đây là thay đổi rẻ nhất và lợi nhất của cả buổi.

**Việc 2 — 15 phút, rủi ro bằng 0.** Đếm số khối job chép lại trong YAML của repo mình — khối chép lại là khối khác nhau đúng một chuỗi tên module hoặc tên service. Nếu dưới **10** khối thì **dừng ở đây**: pipeline động không đáng (QT 4.1). Ghi con số đó vào tài liệu của đội để lần sau không phải đếm lại, và ghi cả ngày đếm.

**Việc 3 — 30 phút, rủi ro trung bình, chỉ làm nếu việc 2 cho trên 10 khối.** Viết script sinh cấu hình cho **một** module trước, không phải cả 12. Chạy nó **song song** với YAML tĩnh trong một tuần bằng một bridge job `allow_failure: true`, rồi so tập job hai bên sinh ra. Một tuần là thời lượng đủ để gặp cả ba ca `rules:changes` của buổi 04 QT 6.3 trên nhánh thật.

```yaml
# mảnh — áp thử song song, không chặn ai trong một tuần
thu-pipeline-dong:
  stage: kich-hoat
  needs: [sinh-cau-hinh]
  allow_failure: true                     # ồn ào nhưng KHÔNG chặn — buổi 01 QT 7.1
  trigger:
    include: [{artifact: con.yml, job: sinh-cau-hinh}]
    strategy: depend                      # vẫn phải có, để biết nó đỏ hay xanh
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

### Cái gì hỏng nếu áp thẳng lên prod

**Mọi bảo vệ dựa trên việc đọc YAML mất hiệu lực trong một đêm.** `CODEOWNERS` đặt trên `.gitlab-ci.yml` không còn che được tập job thật, vì tập job thật giờ do một script quyết định — và script đó có thể nằm ở một tệp không có `CODEOWNERS`. Người xem merge request không còn nhìn thấy pipeline sẽ chạy gì. Buổi **45** (compliance, audit) quay lại đúng chỗ này; hôm nay chỉ cần biết rằng chuyển sang pipeline động là một quyết định có mặt an ninh, không chỉ có mặt kỹ thuật. Cách áp thử an toàn: đặt `CODEOWNERS` lên **cả** `ci/sinh-pipeline.sh` trước khi bật, cùng ngày.

**Script chọn sai mốc so sánh thì job của module đã đổi không chạy, và không ai biết** (QT 6.3, chế độ hỏng số 5). Vì vậy tuần đầu phải chạy **cả hai** đường và so tập job — đừng cắt đường cũ ngay. Phép so cụ thể: lấy danh sách tên job của pipeline con và danh sách job đã chạy của YAML tĩnh, `comm -3` hai danh sách; kỳ vọng là **rỗng**, và mỗi dòng lệch là một lần script tính sai.

**Bridge job không có `strategy: depend` mà lại thêm `allow_failure: true`** là hai lớp che chồng lên nhau: cha xanh vì không chờ, và kể cả có chờ thì cũng không đỏ. Nếu đang có cấu hình như vậy trong repo thì sửa `strategy` **trước**, giữ `allow_failure` trong đúng một tuần thử nghiệm rồi bỏ.

### Đo trước — đo sau

| # | Chỉ số | Đo bằng | Kỳ vọng |
|---|---|---|---|
| 1 | Số khối job phải bảo trì trong YAML | Đếm tay một lần, ghi ngày | Từ **36** về **1** khối `trigger` + 1 script ~40 dòng (QT 4.1) |
| 2 | Số giây của job `sinh-cau-hinh` | `jq '.duration'` trên job đó, 20 lần chạy, lấy trung vị | Biết nó là **8** giây hay **40** giây; trên 20 giây thì phải bỏ bớt việc ra khỏi job này |
| 3 | Số pipeline cha **xanh** có pipeline con **đỏ** trong 30 ngày | Lệnh dưới đây | Về **0** sau khi thêm `strategy: depend`; con số trước khi sửa thường làm cả đội im lặng một lúc |

```bash
# Chỉ số 3 — đếm ca "cha xanh, con đỏ" trong 30 ngày. Chạy TRƯỚC khi sửa gì.
sau=$(date -d '30 days ago' -Iseconds)
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines?status=success&updated_after=$sau&per_page=100" \
| jq -r '.[].id' \
| while read -r p; do
    curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
      "$GITLAB/api/v4/projects/$PID/pipelines/$p/bridges" \
    | jq -r --arg p "$p" '.[] | select(.downstream_pipeline.status=="failed")
                            | "cha \($p) XANH · con \(.downstream_pipeline.id) ĐỎ · bridge \(.name)"'
  done | tee cha-xanh-con-do.txt | wc -l
```

### Khi nào KHÔNG nên dùng

**Đừng** dùng pipeline động khi số khối chép lại dưới **10**. QT 4.1 chỉ có lợi khi phép nhân đủ lớn, còn cái giá — **8–15** giây mỗi pipeline cộng một tệp cấu hình không có trong `git log` — thì phải trả **mọi** lần chạy. Repo 3 module có 9 khối; ở quy mô đó YAML tĩnh dễ đọc hơn, dễ review hơn, và không cần bất cứ thứ gì trong §7.

**Đừng** dùng `trigger:project` khi hai đội chưa có thoả thuận về tên job và tên artifact. QT 4.3 nói đó là một **hợp đồng**, và hợp đồng không viết ra thì pipeline của ta hỏng vì một commit ta không thấy. Buổi **11** (component) cho ta cách tốt hơn để dùng lại cấu hình giữa các đội — dùng lại **cấu hình** mà không mua **quan hệ chạy**.

**Đừng** lồng pipeline quá **một** tầng nếu chưa đo trần thật của instance (QT 7.1). Và kể cả khi trần cho phép, mỗi tầng lồng thêm là một tầng nữa che mất bằng chứng: điều tra một sự cố ở tầng 3 phải mở **3** lần bridge và lấy **3** tệp cấu hình sinh ra.

**Buổi này không giải quyết** việc dùng lại cấu hình **giữa các repo**. `trigger` cho ta chạy pipeline của người khác, không cho ta dùng khối YAML của người khác — hai việc khác nhau. Đó là buổi **10** (`include`, `extends`, anchor) và buổi **11** (component). Nếu bài toán thật của học viên là "ba repo dùng chung một khối job", buổi này là câu trả lời **sai**, và câu hỏi số 2 của BTVN 4 đưa lớp đúng vào chỗ đó.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy | Vì sao dính | Làm đúng là |
|---|---|---|---|
| 1 | Dùng pipeline động cho repo 3 module | Nghe hiện đại, và ai cũng vừa học xong | Dưới **10** khối chép lại thì đừng dùng; 9 khối thì YAML tĩnh thắng (QT 4.1) |
| 2 | Cố dùng `dotenv` trong `rules` của **cùng** pipeline | Biến in ra được ở job sau nên tưởng `rules` cũng thấy | Đẩy phần đó xuống pipeline con — `t0` thứ **2** (QT 4.2, buổi 04 QT 4.2) |
| 3 | Chọn `trigger:project` vì thấy tiện | Cú pháp gần giống `include`, khác một chữ | **3** câu hỏi sở hữu phải trả lời **trước** (QT 4.3) |
| 4 | Đi tìm `trace` của job `trigger` | Nó hiện trong danh sách như một job bình thường | Bridge job không chạy trên runner; nó ở `/bridges` (QT 5.1) |
| 5 | Thiếu `strategy: depend` | Mặc định trông hợp lý, và huy hiệu vẫn xanh | Cha **xanh** con **đỏ**; **1** dòng sửa, **0** giây thêm (QT 5.2) |
| 6 | Tưởng artifact tự chảy giữa hai pipeline | Trong một pipeline nó tự chảy suốt 8 buổi qua | Phải khai **2** chiều riêng; lên cha bằng `needs:pipeline:job` (QT 5.3) |
| 7 | Job cha sau `trigger` không có khẳng định | Thư mục rỗng không làm shell báo lỗi | **1** dòng `test -s` (QT 5.3, buổi 05 QT 5.3) |
| 8 | Sinh YAML rồi trigger luôn, không lint | Lint có vẻ là việc của người viết YAML tay | **1** lệnh, **1** giây, chặn cả lớp lỗi cú pháp (QT 6.2) |
| 9 | Sinh tệp rỗng khi không module nào đổi | Không có job nào thì tệp rỗng nghe đúng | **0** job → **0** pipeline; dùng **1** job giữ chỗ **3** dòng (QT 6.1, buổi 04 QT 4.3) |
| 10 | Nối chuỗi `echo` để sinh YAML | Nhanh nhất khi viết bản đầu | Sinh bằng script có kiểm và tự `exit 1` khi lint sai (QT 6.2) |
| 11 | Tin script sinh cấu hình chọn đúng mốc so sánh | Nó chạy đúng trên nhánh của người viết | Đo cả **3** ca của buổi 04 QT 6.3, và in dòng `mốc=` vào log (QT 6.3) |
| 12 | Tưởng biến của cha tự có ở con | Cùng một lần push nên tưởng cùng một môi trường | **3** đường khai, mặc định khác nhau, **phải đo**; `${VAR:?}` chặn ca rỗng (QT 6.4) |
| 13 | Lồng pipeline nhiều tầng cho gọn | Mỗi tầng riêng lẻ trông sạch sẽ | Trần tham chiếu **2** tầng; mỗi tầng che thêm một lớp bằng chứng (QT 7.1) |
| 14 | Không lưu YAML sinh ra | Nó là tệp tạm, xoá được | `git show` không còn là bằng chứng; artifact `when: always`, **4** kB (QT 7.2) |

---

### 1.7. Tóm tắt

```mermaid
graph TD
    LD["LUẬN ĐỀ: YAML tĩnh phải liệt kê MỌI tổ hợp TRƯỚC khi biết commit đổi gì<br/>Pipeline động mua một t0 THỨ HAI — muộn hơn, biết nhiều hơn<br/>Giá phải trả: lỗi có thể nằm trong tệp YAML KHÔNG có trong repo"]

    G1["BA GIỚI HẠN CÙNG MỘT NGUYÊN NHÂN<br/>b04 QT 4.2 dotenv không dùng được trong rules<br/>b04 QT 6.3 rules:changes sai 3 ca, compare_to sửa 2<br/>b08 QT 6.2 matrix nhân job — không tả được monorepo"] --> LD

    LD --> S4["§4 t0 THỨ HAI<br/>QT 4.1 36 khối / 540 dòng so với 1 khối + script 40 dòng<br/>QT 4.2 pipeline con có t0 riêng — 2 thời điểm một lần push<br/>QT 4.3 ba loại quan hệ khác nhau ở QUYỀN SỞ HỮU"]
    LD --> S5["§5 trigger<br/>QT 5.1 bridge job: 0 slot, 0 phút runner, ~2 giây, ở /bridges<br/>QT 5.2 thiếu strategy depend → CHA XANH CON ĐỎ<br/>QT 5.3 artifact không tự chảy — khai 2 chiều riêng"]
    LD --> S6["§6 PIPELINE ĐỘNG<br/>QT 6.1 bốn bước; 0 job → 0 pipeline, dùng 1 job giữ chỗ<br/>QT 6.2 lint trước khi trigger — 1 giây chặn cả lớp lỗi<br/>QT 6.3 ca thứ 3 của rules:changes giải bằng git trong job<br/>QT 6.4 ba đường biến xuống con — PHẢI ĐO"]

    S4 --> S7["§7 GIỚI HẠN VÀ BẰNG CHỨNG<br/>QT 7.1 bridge rẻ, thứ nó tạo thì không: hạn mức, trần 2 tầng<br/>QT 7.2 git show không còn là bằng chứng<br/>artifact when always → báo cáo gỡ rối 5 DÒNG"]
    S5 --> S7
    S6 --> S7

    S7 --> KQ["6 CHẾ ĐỘ HỎNG MỚI, cả 6 IM LẶNG, 5 KHÔNG CHẶN<br/>bảng hai thuộc tính — LẦN THỨ 9<br/>ca đặc trưng: pipeline CHA XANH mà con đỏ hoặc không làm gì"]
    KQ --> VT["§8 ĐƯA VÀO VIỆC THẬT<br/>1. grep trigger: thêm strategy depend — 5 phút, 0 giây chi phí<br/>2. đếm khối chép lại, dưới 10 thì DỪNG<br/>3. chạy song song 1 tuần, so tập job"]

    S4 -.dùng lại.-> B1["buổi 22 monorepo · 27 release · 44 pipeline tập trung"]
    S5 -.dùng lại.-> B2["buổi 12 merge train · 41 GitOps · 43 canary · 46 chi phí"]
    S6 -.dùng lại.-> B3["buổi 22 dùng lại NGUYÊN sinh-pipeline.sh · 44"]
    S7 -.dùng lại.-> B4["buổi 34 provenance · 42 Terraform · 45 audit · 48 capstone"]
    KQ -.buổi sau.-> B5["buổi 10 include, extends, anchor — dùng lại CẤU HÌNH giữa các repo"]
```

**Năm điều phải nhớ sau buổi học:**

1. **Cái ta mua là một `t0` thứ hai.** **2** thời điểm quyết định trong một lần push, cách nhau **8–15** giây. Mọi lợi ích của buổi — kể cả việc dùng biến `dotenv` trong `rules` — là hệ quả của một câu đó, không phải của một khoá YAML nào.
2. **Bridge job miễn phí, thứ nó tạo ra thì không.** **0** slot, **0** phút runner, ~**2** giây; nó ở `/bridges` chứ không ở `/jobs`. Nhưng job **trong** pipeline con tính vào hạn mức và slot như job thường. Ai chỉ nhớ nửa đầu sẽ dùng pipeline con để lách giới hạn.
3. **Thiếu một dòng thì huy hiệu xanh nói dối.** Không có `strategy: depend`, cha xanh khi con đỏ — ô *im lặng + không chặn*, ô nguy hiểm nhất của bảng hai thuộc tính (**lần thứ 9**). **1** dòng, **0** giây, đổi ô. Đây là việc đầu tiên làm khi về chỗ.
4. **Pipeline động là bốn bước và bước nào cũng cần.** Đọc repo → viết YAML → thành artifact → `trigger:include:artifact`. Lint **trong** job đã sinh nó, **1** giây. Và ca **0 job → 0 pipeline** phải xử lý tường minh bằng **1** job giữ chỗ.
5. **Bằng chứng phải nằm ngoài repo.** `git show` không còn trả lời được câu "pipeline chạy gì hôm qua". Artifact `when: always`, **4** kB mỗi lần chạy, và báo cáo gỡ rối từ **4** dòng thành **5** dòng.

---

### 1.8. Câu hỏi tự kiểm tra

1. Pipeline con cho ta làm được **một** việc mà YAML tĩnh không làm được. Việc đó là gì, và nó là hệ quả của điều gì về **thời điểm**?
2. Monorepo 12 module, mỗi module cần 3 job. YAML tĩnh cần bao nhiêu khối và khoảng bao nhiêu dòng? Pipeline động cần bao nhiêu? Thêm module thứ 13 thì mỗi cách tốn thêm bao nhiêu?
3. Repo của bạn có **3** module. Có nên chuyển sang pipeline động không? Trả lời bằng một con số và một lý do.
4. Vì sao biến `dotenv` của pipeline cha dùng được trong `rules` của pipeline con, trong khi buổi 04 nói việc đó là không thể? Quy tắc nào của buổi 04 vẫn đúng nguyên văn?
5. Kể **ba** loại quan hệ pipeline và nói chúng khác nhau ở đâu — **không** được trả lời bằng cú pháp.
6. Job `trigger` tốn bao nhiêu phút runner và bao nhiêu slot? Nó nằm ở endpoint API nào, và vì sao nó **không** nằm ở endpoint kia?
7. Pipeline con `exit 1` mà job `trigger` của cha **xanh**. Đây là bug hay là hành vi đúng? Một dòng nào đổi nó, và dòng đó tốn thêm bao nhiêu giây?
8. Viết **một lệnh** đếm số pipeline cha xanh có pipeline con đỏ trong 30 ngày.
9. Job cha chạy sau `trigger` cần tệp `bao-cao.json` do pipeline con sinh ra. Nó có tự nhận được không? Viết khối `needs` đúng và **một** dòng khẳng định.
10. Kể **bốn** bước của pipeline động. Bỏ bước 3 thì triệu chứng là gì? Bỏ bước 1 thì triệu chứng là gì?
11. Một commit chỉ sửa `README` làm pipeline con **không xuất hiện** và không có lỗi nào rõ ràng. Nguyên nhân là gì, quy tắc nào của buổi 04, và cách xử lý tường minh?
12. YAML sinh ra sai thụt lề. Chặn ở đâu, bằng lệnh gì, tốn mấy giây? Vì sao lỗi thụt lề của tệp **sinh ra** khó thấy hơn lỗi thụt lề của tệp trong repo?
13. Buổi 04 nêu ba ca `rules:changes` sai. `compare_to` sửa mấy ca? Ca còn lại giải bằng gì, và cái gì bị chuyển từ nền tảng sang ta?
14. Pipeline con chạy **xanh** mà không làm gì; nghi biến không xuống được. Nêu **ba** đường biến có thể xuống con, một lệnh phân biệt "rỗng" với "sai giá trị", và một dòng chặn ca rỗng.
15. Một pipeline con hỏng hôm qua, hôm nay chạy lại thì bình thường. Điều tra bằng gì? Báo cáo gỡ rối của buổi này có mấy dòng, và dòng thêm vào là dòng nào?

### Đáp án

1. Được **quyết định muộn hơn**: một job đọc trạng thái thật của repo rồi **viết ra** đúng tập job cần thiết. Hệ quả của việc có **2** thời điểm `t0` trong một lần push, cách nhau bằng thời lượng các job cha chạy trước bridge (**8–15** giây trong lab) (QT 4.2).
2. Tĩnh: **12 × 3 = 36** khối, khoảng **540** dòng. Động: **1** khối `trigger` + **1** script khoảng **40** dòng. Thêm module thứ 13: tĩnh **+3** khối và **+45** dòng, động **+0** dòng YAML (QT 4.1).
3. **Không.** 3 module × 3 job = **9** khối, dưới ngưỡng **10**. Cái giá của pipeline động — **8–15** giây mỗi lần chạy cộng một tệp cấu hình không có trong `git log` — phải trả mọi lần chạy, còn lợi ích thì tỉ lệ với phép nhân, và ở đây phép nhân quá nhỏ (QT 4.1, §8).
4. Vì đó là **hai lần tạo pipeline** khác nhau: lần thứ hai xảy ra khi lần thứ nhất đã chạy được một phần, nên nó thấy kết quả của phần đó. Quy tắc buổi 04 QT 4.1 vẫn đúng nguyên văn — `rules` vẫn đánh giá **đúng một lần lúc pipeline được tạo**; ta chỉ có hai lần tạo. Điều kiện: biến phải được truyền **tường minh** qua `trigger` (QT 4.2 đọc cùng QT 6.4).
5. child (cùng repo — **ta** giữ YAML), multi-project (repo khác — **đội khác** giữ YAML), lồng nhau (con của con). Khác nhau ở **quyền sở hữu**, trả lời qua ba câu: ai giữ YAML · ai xem được log · ai đổi được mà không cần merge request của ta. Với multi-project, số đội phải liên hệ khi điều tra tăng từ **1** lên **2** (QT 4.3).
6. **0** phút runner, **0** slot, ~**2** giây để pipeline con có `id`. Nó ở `/bridges`. Không ở `/jobs` vì việc tạo pipeline là việc của **server**, không cần container — bridge job là bản ghi của hành động đó, không đi qua tám pha của buổi 01 QT 4.2 (QT 5.1).
7. **Hành vi đúng.** Mặc định nhiệm vụ của bridge job chỉ là *tạo được* pipeline kia. `strategy: depend` đổi nó, tốn **0** giây thêm — pipeline con vẫn chạy đúng thời lượng đó, chỉ khác là cha chờ và phản chiếu trạng thái. Ô của bảng hai thuộc tính đi từ *im lặng + không chặn* sang *ồn ào + có chặn* (QT 5.2).
8. Lặp qua `pipelines?status=success&updated_after=...` rồi với mỗi `id` gọi `/pipelines/:id/bridges` và lọc `select(.downstream_pipeline.status=="failed")` — đoạn đầy đủ ở §8 "Đo trước — đo sau". Kỳ vọng sau khi sửa: **0**.
9. **Không tự nhận được** — qua biên giới pipeline, mặc định là **không có gì** (QT 5.3). Khai `needs: [{pipeline: $CI_PIPELINE_ID, job: gop}]`, và thêm `needs: [{job: kich-hoat-con, artifacts: false}]` nếu chỉ muốn chờ bridge. Dòng khẳng định: `test -s bao-cao.json || exit 1` — thiếu nó thì job chạy với **0** tệp và vẫn xanh (buổi 05 QT 5.3).
10. (1) job đọc trạng thái repo; (2) **viết ra** tệp YAML; (3) tệp thành **artifact**; (4) bridge job dùng `trigger:include:artifact`. Bỏ bước 3: bridge job **đỏ** vì không tìm thấy cấu hình — ồn ào, có chặn, dễ sửa. Bỏ bước 1: tệp sinh ra không phản ánh repo, pipeline con **xanh** và làm sai việc — im lặng (QT 6.1).
11. Tệp sinh ra hợp lệ nhưng **không có job nào**, và **0** job → **0** pipeline (buổi 04 QT 4.3, lần thứ 2). Kiểm bằng `jq '.[0].downstream_pipeline'` trên `/bridges` trả về `null`. Xử lý tường minh: sinh **1** job giữ chỗ `khong-co-gi-doi` (**3** dòng YAML) thay vì để tệp rỗng (QT 6.1).
12. Chặn **trong chính job đã sinh tệp**, bằng `POST /projects/:id/ci/lint` với nội dung tệp, rồi `exit 1` nếu `valid != true`. Khoảng **1** giây. Khó thấy hơn vì không ai review nó, editor không mở nó, `git show` không có nó — nên thông báo "lỗi ở dòng 47" trỏ vào một tệp người điều tra không tìm thấy (QT 6.2).
13. `compare_to` sửa **2** ca (nhánh mới, pipeline theo lịch). Ca thứ **3** — push nhiều commit — giải bằng `git merge-base "origin/$CI_DEFAULT_BRANCH" HEAD` trong job. Cái bị chuyển: **trách nhiệm chọn mốc** đi từ nền tảng sang ta. Trước đây ta không sửa được mốc sai; giờ sửa được, nhưng cũng **viết sai được** — vì vậy phải in dòng `mốc=` vào log làm bằng chứng (QT 6.3).
14. Ba đường: khai ở cấp trên cùng, khai ở cấp **job của bridge**, và `trigger:forward`; `inherit:variables: false` cắt đường thứ nhất. Lệnh phân biệt: in `${#VAR}` — bằng **0** là **rỗng** (biến không xuống được); khác 0 mà sai là **đường khác thắng**, phải hỏi nó tới từ nấc nào trong chín nấc (buổi 06 QT 4.1). Dòng chặn: `: "${VAR:?}"` ở dòng đầu `script` của pipeline con (QT 6.4, buổi 06 QT 5.2).
15. Tải `con.yml` của pipeline hôm qua từ artifact (`when: always`, `expire_in: 7 days`) rồi `diff` với hôm nay; dòng đầu tiên khác nhau **là** nguyên nhân. `git show` vô dụng ở đây vì tệp chưa bao giờ nằm trong git. Báo cáo có **5** dòng; dòng thêm vào là dòng cuối: **tệp cấu hình thật của lần chạy đó**, kèm lệnh lấy nó về (QT 7.2, buổi 07 QT 7.3).

---

## §12. Tài liệu tham khảo

| Nguồn | Loại | Phiên bản |
|---|---|---|
| GitLab Docs — *CI/CD YAML syntax reference*: `trigger`, `trigger:include`, `trigger:project`, `trigger:strategy`, `trigger:forward`, `inherit:variables` | (a) tài liệu chính thức | **17.7** |
| GitLab Docs — *Downstream pipelines*: parent-child, multi-project, nested | (a) | **17.7** |
| GitLab Docs — *Dynamic child pipelines* (sinh cấu hình từ artifact) | (a) | **17.7** |
| GitLab Docs — *CI/CD artifacts*: `needs:pipeline:job`, `artifacts:when` | (a) | **17.7** |
| GitLab API v4 — `GET /projects/:id/pipelines/:id/bridges`, `.../jobs`, `POST /projects/:id/ci/lint`, `GET /projects/:id/jobs/:id/artifacts/:path`, `GET /application/settings` | (a) | v4 trên CE **17.7** |
| Bridge job **không** nằm ở `/jobs`; thời gian tạo pipeline con (~2 giây) | **(c) phải ĐO** | Lab bước 1 |
| Artifact của con **không** tự về cha; trạng thái bridge khi con đỏ | **(c) phải ĐO** | Lab bước 2 |
| Số biến xuống pipeline con theo **3** cách khai, gồm ca `inherit:variables: false` | **(c) phải ĐO** | Lab bước 4 |
| Độ sâu lồng nhau tối đa (**2** tầng tham chiếu) và trần số job của một pipeline | **(c) phải ĐO** | Lab bước 5 |
| Ngưỡng **10** khối chép lại để đáng chuyển sang pipeline động; job `sinh-cau-hinh` **8–15** giây | (c) kinh nghiệm thực tế | — |

> **Về việc trích dẫn.** Năm dòng loại (a) là chỗ nên tra tài liệu khi cần con số chính xác cho phiên bản đang chạy. Năm dòng loại (c) là chỗ **không được** tra: bốn dòng đầu phụ thuộc phiên bản GitLab và cấu hình instance, dòng cuối là ngưỡng kinh nghiệm và phải đọc kèm quy mô repo của chính mình. Đây là **lần thứ 9** khoá học nhắc nguyên tắc "phụ thuộc phiên bản thì phải đo, không tra".

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10' |
| §1 | Sau buổi này học viên làm được gì | 1' |
| §2 | Cần biết trước | 1' |
| §3 | Thuật ngữ và mô hình tư duy | 8' |
| §4 | Vì sao YAML tĩnh không đủ, và `t0` thứ hai | 9' |
| §5 | `trigger`: bridge job, `strategy: depend`, và artifact hai chiều | 9' |
| §6 | Pipeline sinh lúc chạy: bốn bước, và lint trước khi trigger | 11' |
| §7 | Giới hạn, chi phí, và điều tra khi YAML không có trong repo | 5' |
| §8 | Đưa vào việc thật | 4' |
| §9 | Bẫy hay gặp | 2' |
| **Tổng** | | **60'** |
| §10, §11, §12 | Tóm tắt · Câu hỏi tự kiểm tra · Tài liệu tham khảo | ngoài giờ giảng, dùng để tự học và ôn |

**Ghi chú cho giảng viên về nhịp.** §6 là mục dài nhất (11') và là chỗ dễ cháy giờ nhất, vì lớp sẽ hỏi về `sinh-pipeline.sh`. Nếu §6 vượt 13 phút, cắt phần đọc mã của QT 6.3 và để nó lại cho lab bước 3 — nhưng **không** được cắt QT 6.2 (lint), vì đó là cơ chế mà lab bước 3 dựa vào. §7 chỉ 5 phút và đủ để nêu hai quy tắc cộng ba con số chi phí; ba bảng của §7 để lớp đọc lại khi làm lab bước 5.

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên môi trường GitLab Community / Enterprise Edition cùng các GitLab Runner cô lập (Docker / Kubernetes Executor). Hãy đảm bảo bạn đã chuẩn bị môi trường thử nghiệm và cấu hình quyền truy cập cần thiết.

## Khối thực hành — 150 phút

> **Mục tiêu thực hành:** Xây dựng mô hình Child/Parent Pipeline tĩnh và động cho Monorepo 3 module (`api/`, `web/`, `worker/`). Làm chủ bridge job, cơ chế `strategy: depend`, kiểm định cú pháp YAML động bằng `ci/lint` trước khi kích hoạt, truyền biến qua hai thời điểm `t0`, và quản lý hợp đồng liên project (`trigger:project`).

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| Mã | Mục tiêu thực hành | Tiêu chí hoàn thành (đo bằng lệnh) | Checkpoint |
|---|---|---|---|
| TH1 | Dựng Monorepo 3 module và chạy Child Pipeline tĩnh | 3 child pipeline được kích hoạt từ 3 bridge job | CP 1, CP 2 |
| TH2 | Kiểm chứng tính chất của bridge job | `GET /jobs` không chứa bridge job; `GET /bridges` chứa đúng bridge job | CP 2 |
| TH3 | Tái hiện chế độ hỏng im lặng do thiếu `strategy: depend` | Job bridge `success` khi child pipeline `failed` | CP 3 |
| TH4 | Thiết lập `strategy: depend` để phản chiếu trạng thái | Job bridge chuyển `failed` khi child pipeline `failed` | CP 4 |
| TH5 | Chuyển giao hiện vật hai chiều giữa pipeline cha và con | Pipeline cha tải được `bao-cao.json` từ con bằng `needs:pipeline:job` | CP 5 |
| TH6 | Viết script `sinh-pipeline.sh` tự động tạo YAML từ `git diff` | Script sinh YAML đúng cấu trúc cho module thay đổi | CP 6 |
| TH7 | Tích hợp `ci/lint` vào script sinh cấu hình | Script tự `exit 1` khi tệp YAML sinh ra sai cú pháp | CP 7 |
| TH8 | Xử lý ca 0 module thay đổi (0 job → 0 pipeline) | Sinh job giữ chỗ `khong-co-gi-doi` để không bị hỏng pipeline | CP 8 |
| TH9 | Khai thác `t0` thứ hai để truyền biến `dotenv` vào `rules` | Job con đánh giá `rules:if` thành công trên biến do cha sinh ra | CP 9 |
| TH10 | Kiểm tra 3 đường truyền biến xuống pipeline con | Mọi biến nhận được có độ dài lớn hơn 0 | CP 10 |
| TH11 | Quản lý hợp đồng liên project (`trigger:project`) và lưu artifact | Tệp `con.yml` được lưu làm artifact `when: always` | CP 11 |
| TH12 | Hoàn thiện hiện vật và dọn dẹp môi trường | Script `kiem-hien-vat.sh` báo ĐẠT cho toàn bộ tệp | CP 12 |

---

## L1. Điều kiện tiên quyết về môi trường

| STT | Cấu hình / Kiểm tra | Lệnh thực hiện | Kết quả kỳ vọng |
|---|---|---|---|
| 1 | GitLab CE và Runner đang hoạt động | `curl -sf "$GITLAB/api/v4/version"` | HTTP 200, phiên bản 17.7 |
| 2 | Biến môi trường hệ thống | `echo "$GITLAB_TOKEN"` | Chuỗi Token không rỗng |
| 3 | Bộ công cụ trợ giúp `cong-cu.sh` | `test -f ~/lab05/cong-cu.sh` | Tệp tồn tại |
| 4 | Quyền tạo project trên GitLab | `curl -sf "${H[@]}" "$GITLAB/api/v4/projects"` | HTTP 200 |
| 5 | Docker executor sẵn sàng | `docker exec lab-runner gitlab-runner status` | Runner đang chạy |
| 6 | Thư mục làm việc `~/lab09` | `mkdir -p ~/lab09 && cd ~/lab09` | Thư mục được tạo thành công |
| 7 | Git client cấu hình đúng | `git config --get user.name` | Trả về tên người dùng |
| 8 | Công cụ `jq` và `curl` | `jq --version && curl --version` | Đã cài đặt |

> **Cảnh báo tác động:** Bài lab này khởi tạo project `lab09-monorepo` và `lab09-goi-chung`. Bài lab không đụng vào `config.toml` của Runner nên hoàn toàn an toàn cho hạ tầng chung.

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    subgraph Pipeline Cha [Pipeline Parent - t0 ban dau]
        A[Job sinh-cau-hinh: git diff] --> B[Job lint: ci/lint API]
        B --> C[Bridge Job: trigger:include:artifact]
    end

    subgraph Pipeline Con [Pipeline Child - t0 thu hai]
        C -- strategy: depend --> D[Job build module]
        D --> E[Job test module]
        E --> F[Job sinh bao-cao.json]
    end

    F -- needs:pipeline:job --> G[Job tong-hop o Pipeline Cha]
```

### 5 Quyết định thiết kế cốt lõi:
1. **Bước 1 làm Child Pipeline TĨNH trước:** Giúp học viên quan sát trực quan cơ chế bridge job độc lập hoàn toàn với script sinh YAML. Mọi biến số về script hay lỗi cú pháp sinh ra được loại bỏ khỏi bước này.
2. **Đọc bridge job bằng `/bridges` thay vì `/jobs`:** Đây là bằng chứng cơ học khẳng định bridge job không chiếm slot runner (QT 5.1). Học viên kiểm chứng bằng 2 lệnh REST API riêng biệt.
3. **`sinh-pipeline.sh` bắt buộc tự gọi `ci/lint` và `exit 1`:** Đảm bảo cấu hình sinh ra phải hợp lệ trước khi trigger (QT 6.2). Việc kiểm tra tự động biến lời khuyên thành cơ chế cưỡng chế.
4. **Xử lý ca 0 module thay đổi bằng job giữ chỗ:** Tránh bẫy 0 job → 0 pipeline làm đỏ bridge job (QT 6.1). Khi không có file nào trong module đổi, sinh tệp YAML chứa job giữ chỗ `khong-co-gi-doi`.
5. **Lưu `con.yml` làm artifact `when: always`:** Đảm bảo có vết cấu hình để điều tra sự cố khi `git show` không còn tác dụng (QT 7.2). Giúp truy nguyên nguyên nhân hỏng hóc kể cả khi tệp YAML sinh lúc chạy đã biến mất khỏi môi trường làm việc.

### Bảng Ánh xạ 12 Quy tắc Kỹ thuật (QT 4.1 - QT 7.2) vào Các Bước Lab:

| Quy tắc | Nội dung quy tắc | Vị trí áp dụng trong bài lab | Mốc kiểm tra Checkpoint |
|---|---|---|---|
| **QT 4.1** | Phân tách không gian tên giữa pipeline cha và con | §L3.1 Dựng Monorepo 3 module | Checkpoint 1 |
| **QT 4.2** | Tận dụng thời điểm `t0` thứ hai để truyền biến `dotenv` | §L6.1 Khai thác `t0` thứ hai | Checkpoint 9 |
| **QT 4.3** | Hạn chế độ sâu child pipeline không quá 2 tầng | §L3.1 Cấu hình 1 tầng child pipeline | Checkpoint 1 |
| **QT 5.1** | Bridge job tiêu tốn 0 phút runner, 0 slot runner | §L3.2 Truy vấn REST API `/bridges` | Checkpoint 2 |
| **QT 5.2** | Luôn khai báo `strategy: depend` để phản chiếu trạng thái | §L4.1 và §L4.2 Tái hiện & Sửa lỗi | Checkpoint 3, 4 |
| **QT 5.3** | Truyền artifact hai chiều bằng `needs:pipeline:job` | §L4.3 Gom báo cáo từ pipeline con | Checkpoint 5 |
| **QT 6.1** | Xử lý ca 0 module thay đổi bằng job giữ chỗ | §L5.3 Kiểm tra commit chỉ sửa README | Checkpoint 8 |
| **QT 6.2** | Tự động xác thực cú pháp YAML qua `/ci/lint` API | §L5.1 Script `sinh-pipeline.sh` | Checkpoint 6 |
| **QT 6.3** | Quy trình 4 bước bắt buộc cho Dynamic Pipeline | §L5.2 Cấu hình `.gitlab-ci.yml` động | Checkpoint 7 |
| **QT 6.4** | Kiểm soát 3 đường truyền biến xuống pipeline con | §L6.2 Kiểm tra `forward:pipeline_variables` | Checkpoint 10 |
| **QT 7.1** | Multi-project pipeline tuân thủ hợp đồng liên project | §L7.1 Kích hoạt project `lab09-goi-chung` | Checkpoint 11 |
| **QT 7.2** | Lưu tệp cấu hình sinh ra làm artifact `when: always` | §L5.2 và §L7.1 Artifact retention | Checkpoint 7, 11 |

---

## L3. Bước 1 — Child pipeline tĩnh cho monorepo 3 module; bridge job là gì (30 phút)

Kiểm chứng **QT 4.1**, **QT 4.3**, **QT 5.1**.

### 1.1. Dựng Monorepo 3 module

Trong phần này, ta sẽ khởi tạo một repository Monorepo chứa 3 thư mục module riêng biệt: `api/`, `web/`, và `worker/`. Mỗi module sẽ có tệp định nghĩa CI riêng nằm trong thư mục `.gitlab/ci/`.

```bash
cd ~/lab09
. "$HOME/.gitlab-lab.env"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")

PID=$(curl -sf "${H[@]}" --request POST \
  "$GITLAB/api/v4/projects?name=lab09-monorepo&initialize_with_readme=true" | jq -r .id)
A="$GITLAB/api/v4/projects/$PID"
echo "PID_MONOREPO=$PID" > ~/lab09/moi-truong.env

mkdir -p monorepo && cd monorepo
git init -q -b main
git config user.email "hocvien@lab.local"; git config user.name "hoc vien"
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$A" | jq -r .path_with_namespace).git"

mkdir -p api web worker .gitlab/ci
echo "console.log('api v1.0.0 microservice');" > api/app.js
echo "console.log('web v1.0.0 frontend app');" > web/app.js
echo "console.log('worker v1.0.0 queue processor');" > worker/app.js

cat > .gitlab/ci/api.yml <<'YML'
stages: [build, test]
default: { image: alpine:3.20 }

build-api:
  stage: build
  script:
    - echo "=== BUILDING MODULE API ==="
    - echo "Compiling TypeScript files for API service..."
    - mkdir -p dist
    - echo "api-binary-v1.0.0-production-build" > dist/api.txt
    - ls -la dist/
  artifacts:
    paths:
      - dist/
    expire_in: 1 day

test-api:
  stage: test
  script:
    - echo "=== TESTING MODULE API ==="
    - echo "Executing Unit Tests & Integration Tests for API..."
    - test -f dist/api.txt
    - cat dist/api.txt
    - echo "API Tests passed successfully!"
YML

cat > .gitlab/ci/web.yml <<'YML'
stages: [build, test]
default: { image: alpine:3.20 }

build-web:
  stage: build
  script:
    - echo "=== BUILDING MODULE WEB ==="
    - echo "Bundling React/Next.js frontend assets..."
    - mkdir -p dist
    - echo "web-bundle-v1.0.0-production-assets" > dist/web.txt
    - ls -la dist/
  artifacts:
    paths:
      - dist/
    expire_in: 1 day

test-web:
  stage: test
  script:
    - echo "=== TESTING MODULE WEB ==="
    - echo "Executing Component Tests & End-to-End Tests for Web..."
    - test -f dist/web.txt
    - cat dist/web.txt
    - echo "Web UI Tests passed successfully!"
YML

cat > .gitlab/ci/worker.yml <<'YML'
stages: [build, test]
default: { image: alpine:3.20 }

build-worker:
  stage: build
  script:
    - echo "=== BUILDING MODULE WORKER ==="
    - echo "Compiling Go background worker process..."
    - mkdir -p dist
    - echo "worker-service-v1.0.0-binary" > dist/worker.txt
    - ls -la dist/
  artifacts:
    paths:
      - dist/
    expire_in: 1 day

test-worker:
  stage: test
  script:
    - echo "=== TESTING MODULE WORKER ==="
    - echo "Executing Queue Benchmark & Concurrency Tests..."
    - test -f dist/worker.txt
    - cat dist/worker.txt
    - echo "Worker Queue Tests passed successfully!"
YML

cat > .gitlab-ci.yml <<'YML'
stages: [triggers]

trigger-api:
  stage: triggers
  trigger:
    include: .gitlab/ci/api.yml

trigger-web:
  stage: triggers
  trigger:
    include: .gitlab/ci/web.yml

trigger-worker:
  stage: triggers
  trigger:
    include: .gitlab/ci/worker.yml
YML

git add -A && git commit -q -m "monorepo 3 module child pipeline tinh"
git push -q -u origin main
sleep 5

P_CHA=$(curl -sf "${H[@]}" "$A/pipelines?ref=main&per_page=1" | jq -r '.[0].id')
echo "P_CHA=$P_CHA" >> ~/lab09/moi-truong.env
```

**Bảng so sánh 5 tiêu chí: Monorepo Tĩnh vs Monorepo Động (QT 4.1):**

| Tiêu chí | Monorepo YAML Tĩnh | Monorepo YAML Động (Dynamic Pipeline) |
|---|---|---|
| Khối lượng YAML | 36 khối cho 12 module (540+ dòng) | 1 bridge job + 1 script sinh (~40 dòng) |
| Thời điểm chốt job | `t0` ban đầu của Pipeline Cha | `t0` thứ hai của Pipeline Con |
| Tự động hóa chọn job | Thủ công bằng `rules:changes` cố định | Động bằng `git diff` trong runtime script |
| Quản lý lỗi cú pháp | Cố định trước khi push | Tích hợp xác thực qua `/ci/lint` API |
| Chi phí xử lý ban đầu | Đánh giá `rules` ở tất cả các khối | 8–15 giây chạy script sinh cấu hình |

**Mẫu Log phản hồi khi tạo Project thành công:**
```json
{
  "id": 142,
  "description": null,
  "name": "lab09-monorepo",
  "name_with_namespace": "root / lab09-monorepo",
  "path": "lab09-monorepo",
  "path_with_namespace": "root/lab09-monorepo",
  "created_at": "2026-08-21T00:44:00.000Z",
  "default_branch": "main"
}
```

**CHECKPOINT 1 — Pipeline cha kích hoạt thành công 3 child pipeline cho 3 module.**

```bash
cd ~/lab09
so_con=$(curl -sf "${H[@]}" "$A/pipelines/$P_CHA/bridges" | jq length)
{ [ "$so_con" -eq 3 ]; } \
  && echo "CHECKPOINT 1 — ĐẠT (Pipeline cha P=$P_CHA da kich hoat thanh cong $so_con child pipeline)" \
  || echo "CHECKPOINT 1 — LỖI (so_child=$so_con, can 3)" \
  | tee -a ~/lab08/checkpoint.log ~/lab09/checkpoint.log
```

---

### 1.2. Đo tính chất của Bridge Job (QT 5.1)

Bridge job là một đối tượng đặc biệt trên GitLab CI. Nó không chạy trên bất kỳ Runner nào (0 slot runner, 0 phút runner) mà được xử lý trực tiếp bởi server GitLab trong khoảng ~2 giây. Để chứng minh điều này bằng lệnh cơ học, ta truy vấn 2 API endpoint khác nhau: `/jobs` và `/bridges`.

```bash
cd ~/lab09
cat > doc-bridge.sh <<'SH'
#!/usr/bin/env bash
set -uo pipefail
. "$HOME/.gitlab-lab.env"
. "$HOME/lab09/moi-truong.env"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")
A="$GITLAB/api/v4/projects/$PID_MONOREPO"

echo "======================================================================"
echo "=== KIỂM TRA ĐỐI SÓAT ENDPOINT /jobs VS /bridges (CƠ CHẾ BRIDGE JOB) ==="
echo "======================================================================"

n_jobs=$(curl -sf "${H[@]}" "$A/pipelines/$P_CHA/jobs" | jq length)
n_bridges=$(curl -sf "${H[@]}" "$A/pipelines/$P_CHA/bridges" | jq length)

echo "[1] Trạng thái API /jobs (các job thật chạy trên Runner chiếm slot):"
echo "    -> Số lượng job tìm thấy trong Parent Pipeline: $n_jobs"
if [ "$n_jobs" -gt 0 ]; then
  curl -sf "${H[@]}" "$A/pipelines/$P_CHA/jobs" | jq -c '.[] | {id, name, stage, runner_id: .runner.id}'
else
  echo "    -> Trống! Không có job nào chạy trên Runner trong Parent Pipeline."
fi

echo ""
echo "[2] Trạng thái API /bridges (các bridge job điều phối từ Server):"
echo "    -> Số lượng bridge job tìm thấy: $n_bridges"
curl -sf "${H[@]}" "$A/pipelines/$P_CHA/bridges" | jq -r '.[] | "    - Bridge Job: \(.name) | Status: \(.status) | Downstream Pipeline ID: \(.downstream_pipeline.id) | Created At: \(.created_at)"'

echo ""
echo "=== KẾT LUẬN QUY TẮC QT 5.1 ==="
if [ "$n_jobs" -eq 0 ] && [ "$n_bridges" -eq 3 ]; then
  echo "=> ĐÚNG MÔ HÌNH: Bridge job tốn 0 slot runner, 0 phút runner! Không nằm trong /jobs endpoint."
else
  echo "=> SAI MÔ HÌNH: Vẫn phát hiện job nằm trong /jobs endpoint."
fi
SH
chmod +x doc-bridge.sh
bash doc-bridge.sh
```

**Mẫu Log chi tiết đầu ra của `doc-bridge.sh`:**
```text
======================================================================
=== KIỂM TRA ĐỐI SÓAT ENDPOINT /jobs VS /bridges (CƠ CHẾ BRIDGE JOB) ===
======================================================================
[1] Trạng thái API /jobs (các job thật chạy trên Runner chiếm slot):
    -> Số lượng job tìm thấy trong Parent Pipeline: 0
    -> Trống! Không có job nào chạy trên Runner trong Parent Pipeline.

[2] Trạng thái API /bridges (các bridge job điều phối từ Server):
    -> Số lượng bridge job tìm thấy: 3
    - Bridge Job: trigger-api | Status: success | Downstream Pipeline ID: 412 | Created At: 2026-08-21T00:44:05.123Z
    - Bridge Job: trigger-web | Status: success | Downstream Pipeline ID: 413 | Created At: 2026-08-21T00:44:05.145Z
    - Bridge Job: trigger-worker | Status: success | Downstream Pipeline ID: 414 | Created At: 2026-08-21T00:44:05.167Z

=== KẾT LUẬN QUY TẮC QT 5.1 ===
=> ĐÚNG MÔ HÌNH: Bridge job tốn 0 slot runner, 0 phút runner! Không nằm trong /jobs endpoint.
```

**CHECKPOINT 2 — Bridge job nằm ở endpoint `/bridges`, không nằm ở `/jobs`, tốn 0 slot runner.**

```bash
cd ~/lab09
n_j=$(curl -sf "${H[@]}" "$A/pipelines/$P_CHA/jobs" | jq length)
n_b=$(curl -sf "${H[@]}" "$A/pipelines/$P_CHA/bridges" | jq length)
{ [ "$n_j" -eq 0 ] && [ "$n_b" -eq 3 ]; } \
  && echo "CHECKPOINT 2 — ĐẠT (Bridge job khong nam trong /jobs (count=$n_j), nam dung trong /bridges (count=$n_b))" \
  || echo "CHECKPOINT 2 — LỖI (jobs=$n_j, bridges=$n_b)" \
  | tee -a ~/lab09/checkpoint.log
```

---

## L4. Bước 2 — `strategy: depend`: cha xanh con đỏ; artifact hai chiều (25 phút)

Kiểm chứng **QT 5.2**, **QT 5.3**.

### 2.1. Tái hiện ca hỏng im lặng: Cha Xanh Con Đỏ (Thiếu `strategy: depend`)

Một trong những bẫy phổ biến nhất khi triển khai Child Pipeline là không khai báo `strategy: depend`. Theo mặc định, bridge job sẽ chuyển trạng thái sang `success` ngay sau khi tạo thành công pipeline con, mặc cho pipeline con đó thất bại sau đó. Chế độ hỏng này vừa **im lặng** vừa **không chặn**, làm huy hiệu pipeline chính luôn xanh.

```bash
cd ~/lab09/monorepo
git checkout -qB thieu-depend main

cat > .gitlab/ci/api.yml <<'YML'
stages: [build, test]
default: { image: alpine:3.20 }

build-api:
  stage: build
  script:
    - echo "=== CO Y LAM HONG PIPELINE CON (SIMULATED FAILURE) ==="
    - echo "Error: Missing required dependency libssl-dev!"
    - exit 1

test-api:
  stage: test
  script:
    - echo "test api will not run"
YML

git add -A && git commit -q -m "co y lam child pipeline hong"
git push -q -f origin HEAD:refs/heads/thieu-depend
sleep 8

P_THIEU=$(curl -sf "${H[@]}" "$A/pipelines?ref=thieu-depend&per_page=1" | jq -r '.[0].id')
sleep 10

st_bridge=$(curl -sf "${H[@]}" "$A/pipelines/$P_THIEU/bridges" | jq -r '.[] | select(.name=="trigger-api") | .status')
p_down=$(curl -sf "${H[@]}" "$A/pipelines/$P_THIEU/bridges" | jq -r '.[] | select(.name=="trigger-api") | .downstream_pipeline.id')
st_down=$(curl -sf "${H[@]}" "$A/pipelines/$p_down" | jq -r .status)

echo "========================================================================"
echo "=== KIỂM TRA MÔ HÌNH HỎNG IM LẶNG: THIẾU STRATEGY: DEPEND (QT 5.2) ==="
echo "========================================================================"
echo "Bridge Job Status (Parent Pipeline - trigger-api) : $st_bridge (TƯỞNG XANH!)"
echo "Downstream Pipeline Status (Child Pipeline ID $p_down) : $st_down (ĐỎ THỰC TẾ!)"
echo "Hệ quả: Pipeline Cha báo Success trong khi sản phẩm build đã bị thất bại!"
```

**Bảng Ma trận Trạng thái khi có và không có `strategy: depend` (QT 5.2):**

| Cấu hình `strategy` | Kết quả Child Pipeline | Trạng thái Bridge Job | Trạng thái Parent Pipeline | Thuộc tính hỏng hóc |
|---|---|---|---|---|
| Mặc định (Không khai báo) | `failed` (Đỏ) | `success` (Xanh) | `success` (Xanh) | Im lặng & Không chặn |
| Khai báo `strategy: depend` | `failed` (Đỏ) | `failed` (Đỏ) | `failed` (Đỏ) | Ồn ào & Có chặn |
| Khai báo `strategy: depend` | `success` (Xanh) | `success` (Xanh) | `success` (Xanh) | Hoạt động hoàn hảo |

**Chi tiết JSON Trạng thái API:**
```json
{
  "bridge_job": {
    "name": "trigger-api",
    "status": "success",
    "allow_failure": false
  },
  "downstream_pipeline": {
    "id": 415,
    "status": "failed",
    "ref": "thieu-depend"
  }
}
```

**CHECKPOINT 3 — Tái hiện ca im lặng: Bridge job status là `success` trong khi downstream pipeline status là `failed`.**

```bash
{ [ "$st_bridge" = "success" ] && [ "$st_down" = "failed" ]; } \
  && echo "CHECKPOINT 3 — ĐẠT (Tai hien ca hong im lang: Bridge=$st_bridge, Downstream=$st_down)" \
  || echo "CHECKPOINT 3 — LỖI (Bridge=$st_bridge, Downstream=$st_down)" \
  | tee -a ~/lab09/checkpoint.log
```

---

### 2.2. Sửa bằng `strategy: depend`

Bằng cách bổ sung `strategy: depend`, bridge job sẽ giữ kết nối theo dõi và chỉ hoàn thành khi pipeline con kết thúc. Trạng thái của bridge job sẽ phản chiếu chính xác trạng thái của pipeline con, đổi thuộc tính hỏng từ *im lặng không chặn* sang *ồn ào có chặn*.

```bash
cd ~/lab09/monorepo
git checkout -qB co-depend main

cat > .gitlab-ci.yml <<'YML'
stages: [triggers]

trigger-api:
  stage: triggers
  trigger:
    include: .gitlab/ci/api.yml
    strategy: depend

trigger-web:
  stage: triggers
  trigger:
    include: .gitlab/ci/web.yml
    strategy: depend
YML

cat > .gitlab/ci/api.yml <<'YML'
stages: [build]
default: { image: alpine:3.20 }

build-api:
  stage: build
  script:
    - echo "=== BUILD API STILL FAILING WITH STRATEGY DEPEND ==="
    - echo "Error: Fatal build crash!"
    - exit 1
YML

git add -A && git commit -q -m "them strategy depend"
git push -q -f origin HEAD:refs/heads/co-depend
sleep 12

P_DEPEND=$(curl -sf "${H[@]}" "$A/pipelines?ref=co-depend&per_page=1" | jq -r '.[0].id')
sleep 10

st_bridge_dep=$(curl -sf "${H[@]}" "$A/pipelines/$P_DEPEND/bridges" | jq -r '.[] | select(.name=="trigger-api") | .status')

echo "Bridge status khi CÓ strategy: depend : $st_bridge_dep (ĐÃ PHẢN CHIẾU ĐÚNG ĐỎ!)"
```

**CHECKPOINT 4 — Với `strategy: depend`, Bridge job phản chiếu đúng trạng thái `failed` của child pipeline.**

```bash
{ [ "$st_bridge_dep" = "failed" ]; } \
  && echo "CHECKPOINT 4 — ĐẠT (Bridge job phan chieu dung trang thai: Bridge status = $st_bridge_dep)" \
  || echo "CHECKPOINT 4 — LỖI (Bridge status = $st_bridge_dep, can failed)" \
  | tee -a ~/lab09/checkpoint.log
```

---

### 2.3. Chuyển giao Artifact hai chiều giữa Pipeline Cha và Con (QT 5.3)

Artifact không tự động luân chuyển giữa Pipeline Cha và Pipeline Con. Muốn lấy artifact từ Pipeline Con về Pipeline Cha để thực hiện bước tổng hợp báo cáo, ta phải sử dụng cú pháp `needs:pipeline:job`.

```bash
cd ~/lab09/monorepo
git checkout -qB artifact-2-chieu main

cat > .gitlab/ci/api.yml <<'YML'
stages: [build]
default: { image: alpine:3.20 }

build-api:
  stage: build
  script:
    - mkdir -p bao-cao
    - echo '{"status":"OK","coverage":88.5,"tests":120,"passed":120,"failed":0}' > bao-cao/api-report.json
    - echo "Generated api-report.json successfully in child pipeline"
  artifacts:
    paths:
      - bao-cao/
    expire_in: 1 day
YML

cat > .gitlab-ci.yml <<'YML'
stages: [triggers, summary]

trigger-api:
  stage: triggers
  trigger:
    include: .gitlab/ci/api.yml
    strategy: depend

gop-bao-cao:
  stage: summary
  image: alpine:3.20
  needs:
    - pipeline: $CI_PIPELINE_ID
      job: trigger-api
  script:
    - echo "=== KIỂM TRA ARTIFACT TRUYỀN TỪ CHILD PIPELINE SANG PARENT PIPELINE ==="
    - ls -la
    - test -s bao-cao/api-report.json
    - echo "Nội dung báo cáo nhận được từ Child Pipeline:"
    - cat bao-cao/api-report.json
    - echo ""
    - echo "HOAN_THANH_GOP_ARTIFACT"
YML

git add -A && git commit -q -m "artifact 2 chieu cha con"
git push -q -f origin HEAD:refs/heads/artifact-2-chieu
sleep 15

P_ART=$(curl -sf "${H[@]}" "$A/pipelines?ref=artifact-2-chieu&per_page=1" | jq -r '.[0].id')
sleep 12

j_gop_st=$(curl -sf "${H[@]}" "$A/pipelines/$P_ART/jobs" | jq -r '.[] | select(.name=="gop-bao-cao") | .status')
```

**CHECKPOINT 5 — Pipeline cha lấy thành công artifact từ pipeline con bằng `needs:pipeline:job`.**

```bash
{ [ "$j_gop_st" = "success" ]; } \
  && echo "CHECKPOINT 5 — ĐẠT (Job gop-bao-cao o pipeline cha lay thanh cong artifact tu child pipeline)" \
  || echo "CHECKPOINT 5 — LỖI (Job status = $j_gop_st, can success)" \
  | tee -a ~/lab09/checkpoint.log
```

---

## L5. Bước 3 — Pipeline động: sinh YAML từ `git diff`, lint trước khi trigger (40 phút)

Kiểm chứng **QT 6.1**, **QT 6.2**, **QT 6.3**.

### 3.1. Viết script `sinh-pipeline.sh`

Script sinh cấu hình pipeline động đọc danh sách các tệp thay đổi qua `git diff`. Nếu phát hiện thay đổi thuộc thư mục module nào, script sẽ append cấu hình tương ứng vào tệp `.gitlab/generated/child-pipeline.yml`. Quan trọng nhất: script gọi trực tiếp API `/ci/lint` của GitLab để xác thực cú pháp trước khi chấp nhận tệp YAML (QT 6.2).

```bash
cd ~/lab09/monorepo
git checkout -qB pipeline-dong main

cat > sinh-pipeline.sh <<'SH'
#!/usr/bin/env bash
set -uo pipefail

REF_BASE="${1:-origin/main}"
echo "=================================================="
echo "=== SCRIPT SINH PIPELINE ĐỘNG (DYNAMIC GENERATOR) ==="
echo "=================================================="
echo "Mốc so sánh git diff: $REF_BASE"

CHANGES=$(git diff --name-only "$REF_BASE" HEAD || true)
echo "Danh sách các tệp có thay đổi trong commit:"
echo "$CHANGES"
echo "--------------------------------------------------"

mkdir -p .gitlab/generated

cat > .gitlab/generated/child-pipeline.yml <<'YML'
stages: [build, test]
default: { image: alpine:3.20 }
YML

COUNT=0

if echo "$CHANGES" | grep -q "^api/"; then
  echo "-> [DETECTED] Thay đổi thuộc module api/"
  cat >> .gitlab/generated/child-pipeline.yml <<'YML'
build-api-dynamic:
  stage: build
  script:
    - echo "=== DYNAMIC BUILD API SERVICE ==="
    - echo "Building API module from dynamic pipeline"

test-api-dynamic:
  stage: test
  script:
    - echo "=== DYNAMIC TEST API SERVICE ==="
    - echo "Running tests for API module"
YML
  COUNT=$((COUNT+1))
fi

if echo "$CHANGES" | grep -q "^web/"; then
  echo "-> [DETECTED] Thay đổi thuộc module web/"
  cat >> .gitlab/generated/child-pipeline.yml <<'YML'
build-web-dynamic:
  stage: build
  script:
    - echo "=== DYNAMIC BUILD WEB FRONTEND ==="
    - echo "Building Web module from dynamic pipeline"

test-web-dynamic:
  stage: test
  script:
    - echo "=== DYNAMIC TEST WEB FRONTEND ==="
    - echo "Running tests for Web module"
YML
  COUNT=$((COUNT+1))
fi

if echo "$CHANGES" | grep -q "^worker/"; then
  echo "-> [DETECTED] Thay đổi thuộc module worker/"
  cat >> .gitlab/generated/child-pipeline.yml <<'YML'
build-worker-dynamic:
  stage: build
  script:
    - echo "=== DYNAMIC BUILD WORKER PROCESS ==="
    - echo "Building Worker process from dynamic pipeline"

test-worker-dynamic:
  stage: test
  script:
    - echo "=== DYNAMIC TEST WORKER PROCESS ==="
    - echo "Running tests for Worker process"
YML
  COUNT=$((COUNT+1))
fi

if [ "$COUNT" -eq 0 ]; then
  echo "-> [DETECTED] Không có module nào thay đổi (Ca 0 module đổi - QT 6.1)"
  cat >> .gitlab/generated/child-pipeline.yml <<'YML'
khong-co-gi-doi:
  stage: build
  script:
    - echo "No code modules changed in this commit."
    - echo "Placeholder job executed to keep downstream pipeline valid."
YML
fi

echo ""
echo "=== VERIFYING GENERATED YAML VIA /ci/lint API (QT 6.2) ==="
. "$HOME/.gitlab-lab.env"
. "$HOME/lab09/moi-truong.env"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")
A="$GITLAB/api/v4/projects/$PID_MONOREPO"

CONTENT=$(jq -n --arg c "$(cat .gitlab/generated/child-pipeline.yml)" '{content: $c}')
LINT_RES=$(curl -sf "${H[@]}" --request POST --header 'Content-Type: application/json' \
  --data "$CONTENT" "$A/ci/lint")

VALID=$(echo "$LINT_RES" | jq -r .valid)
if [ "$VALID" != "true" ]; then
  echo "LỖI: Tệp YAML sinh ra KHÔNG HỢP LỆ theo /ci/lint API!"
  echo "$LINT_RES" | jq -c .errors
  exit 1
fi
echo "LINT THÀNH CÔNG: Tệp .gitlab/generated/child-pipeline.yml hoàn toàn hợp lệ!"
SH
chmod +x sinh-pipeline.sh
```

**Chi tiết cấu trúc Request Payload gửi tới `/ci/lint` API:**
```json
{
  "content": "stages:\n  - build\n  - test\ndefault:\n  image: alpine:3.20\n..."
}
```

**Mẫu phản hồi khi gọi API `/ci/lint` thành công:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "merged_yaml": "stages:\n  - build\n  - test\ndefault:\n  image: alpine:3.20\n..."
}
```

**CHECKPOINT 6 — Script `sinh-pipeline.sh` hoạt động đúng và tự động gọi `ci/lint` để kiểm định.**

```bash
cd ~/lab09/monorepo
bash sinh-pipeline.sh HEAD~1 > /tmp/lint-out.log
{ grep -q "LINT THÀNH CÔNG" /tmp/lint-out.log; } \
  && echo "CHECKPOINT 6 — ĐẠT (Script sinh pipeline va lint qua API thanh cong)" \
  || echo "CHECKPOINT 6 — LỖI (Lint khong qua)" \
  | tee -a ~/lab09/checkpoint.log
```

---

### 3.2. Cấu hình Pipeline động 4 bước trong `.gitlab-ci.yml`

Quy trình 4 bước của Pipeline động:
1. Job `sinh-cau-hinh` chạy script để tạo `.gitlab/generated/child-pipeline.yml`.
2. Script tự gọi `ci/lint` API để kiểm tra tệp YAML.
3. Tệp YAML được xuất ra làm artifact với `when: always`.
4. Job `trigger-dynamic` sử dụng `trigger:include:artifact` để kích hoạt Child Pipeline.

```bash
cd ~/lab09/monorepo
cat > .gitlab-ci.yml <<'YML'
stages: [generate, trigger]

sinh-cau-hinh:
  stage: generate
  image: alpine:3.20
  script:
    - apk add --no-cache bash git curl jq
    - bash sinh-pipeline.sh origin/main
  artifacts:
    paths:
      - .gitlab/generated/child-pipeline.yml
    when: always

trigger-dynamic:
  stage: trigger
  trigger:
    include:
      - artifact: .gitlab/generated/child-pipeline.yml
        job: sinh-cau-hinh
    strategy: depend
YML

echo "/* modify api module codebase */" >> api/app.js
git add -A && git commit -q -m "test pipeline dong 4 buoc"
git push -q -f origin HEAD:refs/heads/pipeline-dong
sleep 15

P_DYN=$(curl -sf "${H[@]}" "$A/pipelines?ref=pipeline-dong&per_page=1" | jq -r '.[0].id')
sleep 12

st_dyn_bridge=$(curl -sf "${H[@]}" "$A/pipelines/$P_DYN/bridges" | jq -r '.[] | select(.name=="trigger-dynamic") | .status')
```

**CHECKPOINT 7 — Pipeline động 4 bước thực thi thành công, bridge job đạt trạng thái `success`.**

```bash
{ [ "$st_dyn_bridge" = "success" ]; } \
  && echo "CHECKPOINT 7 — ĐẠT (Pipeline dong 4 buoc chay thanh cong: Bridge status = $st_dyn_bridge)" \
  || echo "CHECKPOINT 7 — LỖI (Bridge status = $st_dyn_bridge, can success)" \
  | tee -a ~/lab09/checkpoint.log
```

---

### 3.3. Xử lý Ca 0 Module Thay Đổi (0 Job → 0 Pipeline - QT 6.1)

Nếu một commit chỉ chỉnh sửa tệp `README.md` hoặc tệp cấu hình bên ngoài, không có module nào thay đổi. Nếu tệp YAML sinh ra không chứa bất kỳ job nào (0 job), GitLab sẽ từ chối tạo pipeline con và làm hỏng bridge job. Script `sinh-pipeline.sh` đã xử lý ca này bằng cách sinh ra job giữ chỗ `khong-co-gi-doi`.

```bash
cd ~/lab09/monorepo
git checkout -qB ca-0-module main

echo "# Update Documentation README for Monorepo Project" >> README.md
git add -A && git commit -q -m "chi sua README"
git push -q -f origin HEAD:refs/heads/ca-0-module
sleep 15

P_0MOD=$(curl -sf "${H[@]}" "$A/pipelines?ref=ca-0-module&per_page=1" | jq -r '.[0].id')
sleep 10

p_0mod_down=$(curl -sf "${H[@]}" "$A/pipelines/$P_0MOD/bridges" | jq -r '.[] | select(.name=="trigger-dynamic") | .downstream_pipeline.id')
j_placeholder=$(curl -sf "${H[@]}" "$A/pipelines/$p_0mod_down/jobs" | jq -r '.[0].name')

echo "Job name trong downstream pipeline (Ca 0 module doi): $j_placeholder"
```

**CHECKPOINT 8 — Khi 0 module thay đổi, job giữ chỗ `khong-co-gi-doi` được sinh ra giúp pipeline con không rỗng.**

```bash
{ [ "$j_placeholder" = "khong-co-gi-doi" ]; } \
  && echo "CHECKPOINT 8 — ĐẠT (Ca 0 module doi sinh dung job giu cho: $j_placeholder)" \
  || echo "CHECKPOINT 8 — LỖI (Job giu cho = $j_placeholder, can khong-co-gi-doi)" \
  | tee -a ~/lab09/checkpoint.log
```

---

## L6. Bước 4 — `t0` thứ hai: biến của cha dùng được trong `rules` của con (25 phút)

Kiểm chứng **QT 4.2**, **QT 6.4**.

### 4.1. Truyền biến `dotenv` vào `rules` của Pipeline con (QT 4.2)

Trong cùng một pipeline, biến sinh ra từ báo cáo `dotenv` trong `script` **không thể** được sử dụng bởi `rules` của các job sau (vì `rules` đánh giá tại `t0` ban đầu). Tuy nhiên, với Child Pipeline, `t0` của pipeline con xảy ra tại thời điểm bridge job được kích hoạt (`t0` thứ hai). Do đó, biến `dotenv` do job cha sinh ra **hoàn toàn dùng được** trong `rules` của pipeline con.

```bash
cd ~/lab09/monorepo
git checkout -qB t0-thu-hai main

cat > .gitlab-ci.yml <<'YML'
stages: [generate, trigger]

sinh-bien:
  stage: generate
  image: alpine:3.20
  script:
    - echo "=== GENERATING DYNAMIC ENV VAR AT RUNTIME ==="
    - echo "TARGET_MODULE=worker" > build.env
    - echo "DYNAMIC_BUILD_TAG=v2.5.0-rc1" >> build.env
  artifacts:
    reports:
      dotenv: build.env

trigger-t0-hai:
  stage: trigger
  variables:
    MODULE_CHON: $TARGET_MODULE
  trigger:
    include: .gitlab/ci/child-rules.yml
    strategy: depend
YML

mkdir -p .gitlab/ci
cat > .gitlab/ci/child-rules.yml <<'YML'
stages: [build]
default: { image: alpine:3.20 }

build-api-rules:
  stage: build
  rules:
    - if: '$MODULE_CHON == "api"'
  script:
    - echo "Build API tu rules"

build-worker-rules:
  stage: build
  rules:
    - if: '$MODULE_CHON == "worker"'
  script:
    - echo "=== BUILD WORKER EXECUTED VIA DYNAMIC DOTENV RULES AT SECOND T0 ==="
    - echo "Selected module from parent dotenv: $MODULE_CHON"
YML

git add -A && git commit -q -m "test t0 thu hai voi dotenv"
git push -q -f origin HEAD:refs/heads/t0-thu-hai
sleep 15

P_T0=$(curl -sf "${H[@]}" "$A/pipelines?ref=t0-thu-hai&per_page=1" | jq -r '.[0].id')
sleep 10

p_t0_down=$(curl -sf "${H[@]}" "$A/pipelines/$P_T0/bridges" | jq -r '.[] | select(.name=="trigger-t0-hai") | .downstream_pipeline.id')
j_t0_name=$(curl -sf "${H[@]}" "$A/pipelines/$p_t0_down/jobs" | jq -r '.[0].name')

echo "Selected Job Name in Child Pipeline (Dynamic Dotenv Rules): $j_t0_name"
```

**CHECKPOINT 9 — `rules` của pipeline con đánh giá thành công trên biến `dotenv` do job cha sinh ra tại `t0` thứ hai.**

```bash
{ [ "$j_t0_name" = "build-worker-rules" ]; } \
  && echo "CHECKPOINT 9 — ĐẠT (t0 thu hai hoat dong dung: Job duoc chon la $j_t0_name)" \
  || echo "CHECKPOINT 9 — LỖI (Job selected = $j_t0_name, can build-worker-rules)" \
  | tee -a ~/lab09/checkpoint.log
```

---

### 4.2. Đo 3 đường truyền biến xuống Pipeline con (QT 6.4)

Biến có thể truyền xuống Pipeline con qua 3 đường:
1. Biến toàn cục (Global Variables) của Pipeline cha.
2. Biến định nghĩa trực tiếp trong khối `trigger:variables` của bridge job.
3. Biến chuyển tiếp tự động thông qua `forward:pipeline_variables: true`.

```bash
cd ~/lab09/monorepo
git checkout -qB do-truyen-bien main

cat > .gitlab-ci.yml <<'YML'
variables:
  VAR_GLOBAL: "global-value-from-parent-pipeline"

stages: [trigger]

trigger-bien:
  stage: trigger
  variables:
    VAR_BRIDGE: "bridge-value-from-trigger-job"
  trigger:
    include: .gitlab/ci/child-bien.yml
    forward:
      pipeline_variables: true
    strategy: depend
YML

cat > .gitlab/ci/child-bien.yml <<'YML'
stages: [check]
default: { image: alpine:3.20 }

check-bien:
  stage: check
  script:
    - echo "=== CHECKING FORWARDED VARIABLES IN CHILD PIPELINE ==="
    - echo "1. VAR_GLOBAL = $VAR_GLOBAL (length=${#VAR_GLOBAL})"
    - echo "2. VAR_BRIDGE = $VAR_BRIDGE (length=${#VAR_BRIDGE})"
    - test -n "$VAR_GLOBAL" && test -n "$VAR_BRIDGE"
    - echo "ALL FORWARDED VARIABLES RECEIVED SUCCESSFULLY WITH NON-ZERO LENGTH!"
YML

git add -A && git commit -q -m "test 3 duong truyen bien"
git push -q -f origin HEAD:refs/heads/do-truyen-bien
sleep 15

P_BIEN=$(curl -sf "${H[@]}" "$A/pipelines?ref=do-truyen-bien&per_page=1" | jq -r '.[0].id')
sleep 10

p_bien_down=$(curl -sf "${H[@]}" "$A/pipelines/$P_BIEN/bridges" | jq -r '.[] | select(.name=="trigger-bien") | .downstream_pipeline.id')
st_child_job=$(curl -sf "${H[@]}" "$A/pipelines/$p_bien_down/jobs" | jq -r '.[0].status')
```

**CHECKPOINT 10 — Biến được truyền thành công xuống pipeline con qua các đường khai báo.**

```bash
{ [ "$st_child_job" = "success" ]; } \
  && echo "CHECKPOINT 10 — ĐẠT (Truyen bien xuong pipeline con thanh cong: Status = $st_child_job)" \
  || echo "CHECKPOINT 10 — LỖI (Child job status = $st_child_job, can success)" \
  | tee -a ~/lab09/checkpoint.log
```

---

## L7. Bước 5 — Giới hạn, lưu YAML sinh ra, `trigger:project` (20 phút)

Kiểm chứng **QT 7.1**, **QT 7.2**.

### 5.1. Thiết lập `trigger:project` và Lưu Artifact `when: always`

Multi-project pipeline kích hoạt pipeline thuộc một project khác trên GitLab. Quyền sở hữu tệp định nghĩa CI thuộc về project đích. Lưu tệp cấu hình sinh lúc chạy làm artifact `when: always` là điều kiện bắt buộc để có bằng chứng điều tra sự cố.

```bash
cd ~/lab09
PID_GC=$(curl -sf "${H[@]}" --request POST \
  "$GITLAB/api/v4/projects?name=lab09-goi-chung&initialize_with_readme=true" | jq -r .id)
A_GC="$GITLAB/api/v4/projects/$PID_GC"
echo "PID_GC=$PID_GC" >> ~/lab09/moi-truong.env

cd ~/lab09/monorepo
git checkout -qB test-multi-project main

cat > .gitlab-ci.yml <<'YML'
stages: [trigger]

trigger-multi:
  stage: trigger
  trigger:
    project: root/lab09-goi-chung
    branch: main
    strategy: depend
YML

git add -A && git commit -q -m "test multi project trigger"
git push -q -f origin HEAD:refs/heads/test-multi-project
sleep 12

P_MULTI=$(curl -sf "${H[@]}" "$A/pipelines?ref=test-multi-project&per_page=1" | jq -r '.[0].id')
sleep 10

st_multi_bridge=$(curl -sf "${H[@]}" "$A/pipelines/$P_MULTI/bridges" | jq -r '.[] | select(.name=="trigger-multi") | .status')
```

**CHECKPOINT 11 — Kích hoạt thành công Multi-Project Pipeline (`trigger:project`) và lưu artifact cấu hình.**

```bash
{ [ "$st_multi_bridge" = "success" ]; } \
  && echo "CHECKPOINT 11 — ĐẠT (Multi-project trigger hoat dong dung: Status = $st_multi_bridge)" \
  || echo "CHECKPOINT 11 — LỖI (Multi-project status = $st_multi_bridge, can success)" \
  | tee -a ~/lab09/checkpoint.log
```

---

## L8. Nộp sản phẩm và dọn dẹp (10 phút)

### L8.1. Kiểm định hiện vật tổng hợp

```bash
cat > ~/lab09/kiem-hien-vat.sh <<'SH'
#!/usr/bin/env bash
set -uo pipefail
D="$HOME/lab09"
loi=0
bao() { if [ "$1" -eq 0 ]; then echo "  ĐẠT   $2"; else echo "  LỖI   $2"; loi=$((loi+1)); fi; }

echo "========================================================================"
echo "=== KIỂM TRA TOÀN BỘ HIỆN VẬT SẢN PHẨM LAB 09 (VERIFY ALL ARTIFACTS) ==="
echo "========================================================================"
for f in moi-truong.env doc-bridge.sh checkpoint.log; do
  [ -s "$D/$f" ]; bao $? "có $f và khác rỗng"
done

[ "$(grep -c 'ĐẠT' "$D/checkpoint.log")" -ge 11 ]
bao $? "checkpoint.log có đủ 11 dòng ĐẠT"

echo "------------------------------------------------------------------------"
[ "$loi" -eq 0 ] && echo "CHECKPOINT 12 — ĐẠT (mọi hiện vật hợp lệ)" || echo "CHECKPOINT 12 — LỖI ($loi lỗi)"
exit "$loi"
SH
chmod +x ~/lab09/kiem-hien-vat.sh
bash ~/lab09/kiem-hien-vat.sh | tee -a ~/lab09/checkpoint.log
```

**CHECKPOINT 12 — mọi hiện vật hợp lệ về NỘI DUNG, và dọn dẹp môi trường sạch sẽ.**

---

## L9. Xử lý sự cố thường gặp trong lab

| # | Triệu chứng | Nguyên nhân | Cách khắc phục |
|---|---|---|---|
| 1 | Bridge job đỏ với lỗi "downstream pipeline could not be created" | Cú pháp tệp YAML con bị sai hoặc đường dẫn `include` không đúng | Kiểm tra tệp `.gitlab-ci.yml` con bằng `ci/lint` API |
| 2 | Pipeline cha `success` nhưng pipeline con `failed` | Thiếu khai báo `strategy: depend` trong bridge job | Bổ sung `strategy: depend` vào khối `trigger` |
| 3 | Job cha không nhận được artifact từ pipeline con | Thiếu `needs:pipeline:job` hoặc tên job nguồn bị sai | Khai báo đúng `pipeline: $CI_PIPELINE_ID` và tên bridge job |
| 4 | Biến `dotenv` không truyền được vào pipeline con | Chưa khai báo `reports:dotenv` hoặc thiếu `pipeline_variables: true` | Khai báo `artifacts:reports:dotenv` ở job sinh biến |
| 5 | Script `sinh-pipeline.sh` báo lỗi `git diff` | Chưa `fetch` hoặc mốc so sánh `origin/main` chưa tồn tại | Chạy `git fetch origin` trước khi `git diff` |
| 6 | 0 module thay đổi làm bridge job bị đỏ | Tệp YAML sinh ra rỗng không chứa job nào | Thêm job giữ chỗ `khong-co-gi-doi` vào tệp YAML |
| 7 | `ci/lint` API trả về `401 Unauthorized` | `$GITLAB_TOKEN` bị thiếu hoặc hết hạn | Kiểm tra lại biến môi trường `GITLAB_TOKEN` |
| 8 | Bridge job trong `/jobs` endpoint không có | Bridge job nằm riêng ở `/bridges` endpoint | Dùng `GET /projects/:id/pipelines/:p_id/bridges` |
| 9 | Multi-project trigger báo `project not found` | Đường dẫn project dạng `namespace/project` bị sai | Kiểm tra `path_with_namespace` qua API |
| 10 | Biến toàn cục không xuống pipeline con | Đặt `inherit:variables: false` | Bỏ `inherit:variables: false` nếu muốn kế thừa |
| 11 | Lỗi lồng pipeline quá 2 tầng | GitLab giới hạn độ sâu child pipeline (tối đa 2 tầng) | Rút gọn kiến trúc pipeline về 1-2 tầng |
| 12 | `git diff` nhận diện sai tệp thay đổi | Chưa commit tệp hoặc đang làm việc ở detached HEAD | Commit thay đổi trước khi chạy script sinh pipeline |
| 13 | Artifact của child pipeline bị hết hạn | Khai báo `expire_in` quá ngắn | Tăng `expire_in` lên `1 day` hoặc `7 days` |
| 14 | Job con không chạy khi `rules:if` đúng | Tên biến trong `rules` khác tên biến được truyền | Kiểm tra chính xác tên biến truyền qua `trigger:variables` |

---

## L10. Bài tập mở rộng

**BT1 — Tự động hóa sinh pipeline cho 5 module.** Mở rộng `sinh-pipeline.sh` hỗ trợ 5 thư mục module khác nhau (`api/`, `web/`, `worker/`, `auth/`, `payment/`). Script cần kiểm tra linh hoạt và tự sinh các stage tương ứng cho từng module.

```bash
# Đoạn mã gợi ý mở rộng script sinh-pipeline.sh cho 5 module:
MODULES=("api" "web" "worker" "auth" "payment")
for mod in "${MODULES[@]}"; do
  if echo "$CHANGES" | grep -q "^$mod/"; then
    echo "Phát hiện thay đổi ở $mod/"
    cat >> .gitlab/generated/child-pipeline.yml <<YML
build-$mod-dynamic:
  stage: build
  script: [echo "Build $mod"]
test-$mod-dynamic:
  stage: test
  script: [echo "Test $mod"]
YML
  fi
done
```

**BT2 — Đo thời gian chênh lệch giữa 2 `t0`.** Viết script đếm số giây từ khi pipeline cha tạo đến khi pipeline con bắt đầu. Đo khoảng thời gian tiêu tốn cho việc clone repo, chạy `git diff`, và gọi API `ci/lint`.

```bash
# Đoạn mã gợi ý đếm số giây giữa 2 t0:
t0_parent=$(curl -sf "${H[@]}" "$A/pipelines/$P_CHA" | jq -r .created_at)
t0_child=$(curl -sf "${H[@]}" "$A/pipelines/$P_CHILD" | jq -r .created_at)
echo "t0 parent: $t0_parent | t0 child: $t0_child"
```

**BT3 — Tích hợp Slack notification khi pipeline con hỏng.** Dùng `strategy: depend` kết hợp job sau trong pipeline cha để gửi webhook thông báo đến Slack khi có bất kỳ child pipeline nào bị lỗi.

```bash
# Đoạn mã gợi ý gửi Slack Webhook:
cat >> .gitlab-ci.yml <<'YML'
notify-slack:
  stage: summary
  when: on_failure
  script:
    - curl -X POST -H 'Content-type: application/json' --data '{"text":"Child Pipeline Failed!"}' $SLACK_WEBHOOK_URL
YML
```

**BT4 — Truyền file JSON qua lại giữa 3 tầng pipeline.** Thử nghiệm child pipeline lồng 2 tầng (Parent -> Child -> Grandchild) và kiểm tra luồng luân chuyển artifact qua 3 tầng bằng `needs:pipeline:job`.

```bash
# Sơ đồ 3 tầng pipeline:
# Parent Pipeline (.gitlab-ci.yml)
#   └── Child Pipeline Level 1 (.gitlab/ci/child.yml)
#         └── Grandchild Pipeline Level 2 (.gitlab/ci/grandchild.yml)
```

**BT5 — Linting offline cho generated YAML.** Dùng `yamllint` hoặc `gitlab-ci-lint` CLI kiểm tra cú pháp trước khi gọi API `/ci/lint` nhằm tiết kiệm số lần gọi API mạng.

```bash
# Đoạn mã gợi ý lint offline:
yamllint .gitlab/generated/child-pipeline.yml
```

**BT6 — So sánh tốc độ giữa YAML tĩnh và Pipeline động.** Đo tổng phút runner và tổng thời gian hoàn thành (wall-clock time) của cả 2 cách trên monorepo thực tế có 10+ module.

```bash
# Lệnh đo thời gian hoàn thành pipeline từ API:
curl -sf "${H[@]}" "$A/pipelines/$P_ID" | jq -r '{duration, queued_duration}'
```

**BT7 — Xây dựng matrix động.** Sinh tệp YAML chứa `parallel: matrix` từ dữ liệu danh sách phiên bản đọc được trong kho (ví dụ đọc danh sách phiên bản Node.js từ `package.json`).

**BT8 — Quản lý nhiều downstream project.** Viết 1 pipeline cha trigger đồng thời 3 project độc lập khác nhau (`trigger:project`) và thu thập báo cáo kiểm thử của cả 3 project về pipeline cha.

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| # | Hiện vật | Điểm | Tiêu chí đạt điểm tối đa |
|---|---|---|---|
| 1 | `sinh-pipeline.sh` | 30 | Sinh đúng YAML từ `git diff`, có gọi `ci/lint` API và xử lý ca 0 module đổi bằng job giữ chỗ |
| 2 | `doc-bridge.sh` | 25 | Đọc đúng endpoint `/bridges`, hiển thị trạng thái hai phía và phân biệt rõ với `/jobs` endpoint |
| 3 | `.gitlab-ci.yml` (Monorepo) | 20 | Đủ 4 bước pipeline động, có `strategy: depend` và `needs:pipeline:job` thu thập artifact |
| 4 | `moi-truong.env` | 15 | Lưu đầy đủ ID các project và pipeline kiểm chứng trong suốt bài lab |
| 5 | `checkpoint.log` | 10 | Đủ 12 mốc CHECKPOINT ĐẠT theo đúng thứ tự thực hiện |
| | **Tổng** | **100** | |

**Điểm trừ — dẫn chiếu bảng Bẫy hay gặp ở §9 tệp lý thuyết:**
* Thiếu `strategy: depend` làm cha xanh con đỏ: **−10 điểm**.
* Sinh tệp YAML rỗng làm hỏng bridge job (không xử lý ca 0 module đổi): **−10 điểm**.
* Không tích hợp `ci/lint` API vào script sinh cấu hình: **−10 điểm**.
* Đọc bridge job từ `/jobs` endpoint thay vì `/bridges` endpoint: **−5 điểm**.
* Không lưu tệp YAML sinh ra làm artifact `when: always`: **−5 điểm**.

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| L1–L2 | Điều kiện tiên quyết và kiến trúc | — |
| L3 | Bước 1 — Child pipeline tĩnh cho monorepo 3 module; bridge job | 30' |
| L4 | Bước 2 — `strategy: depend`: cha xanh con đỏ; artifact hai chiều | 25' |
| L5 | Bước 3 — Pipeline động: sinh YAML từ `git diff`, lint trước khi trigger | 40' |
| L6 | Bước 4 — `t0` thứ hai: biến của cha dùng được trong `rules` của con | 25' |
| L7 | Bước 5 — Giới hạn, lưu YAML sinh ra, `trigger:project` | 20' |
| L8 | Nộp sản phẩm và dọn dẹp | 10' |
| **Tổng** | | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---



**Quy tắc cho giảng viên:**

- Chọn **5–7 câu** trong 12, ưu tiên câu 🔥. Trả lời **bằng miệng, không nhìn tài liệu**. **Gọi ngẫu nhiên**; ai thiếu thì gọi người kế tiếp bổ sung, giảng viên không trả lời thay.
- Tám câu chen vào của buổi 01–08 vẫn dùng nguyên. Buổi này thêm hai câu. Thứ nhất: **"bạn đang nói về pipeline nào — CHA hay CON?"** Từ hôm nay một lần push sinh **từ 2 pipeline trở lên**, nên "pipeline đỏ" không còn là phát biểu đủ. Thứ hai, quan trọng hơn: **"tệp YAML gây ra lỗi này có trong repo không?"** Nếu *không* thì `git show` vô dụng, điều tra phải đi bằng artifact (QT 7.2).
- Câu **10** là câu **tính toán**: "nhiều lắm" hoặc "tuỳ repo" mà không kèm phép nhân thì tối đa **1 điểm**, dù cơ chế đúng.
- Câu **2** hỏi ngược: thí sinh được đưa một tin **có vẻ tốt** — huy hiệu xanh suốt tuần. Giảng viên **không** gợi ý gì, chờ xem thí sinh có tự hỏi "xanh của cha hay của con".

**Thang điểm mỗi câu:** 0 = không trả lời được hoặc sai cơ chế · 1 = nhắc được tên khái niệm, không nêu cơ chế · 2 = nêu đúng cơ chế · 3 = đúng cơ chế **và** một con số, hoặc **và** một ca nó không đúng.

**Hai lỗi làm trần điểm cả buổi là 1:**

1. **Nói job `trigger` chạy trên runner và tốn phút runner.** Bridge job là bản ghi một hành động **phía server**: **0** slot, **0** phút runner, ~**2** giây, nằm ở `/bridges` chứ không ở `/jobs` (QT 5.1). Người tin ngược lại đi tìm `trace` của một job không có `trace`, và chặn việc tách pipeline vì "sợ cạn slot" trong khi thủ phạm là job **trong** pipeline con (QT 7.1).
2. **Nói pipeline cha tự đỏ khi pipeline con đỏ.** Mặc định thì **không**; **1** dòng `strategy: depend` là thứ duy nhất bắt nó phản chiếu (QT 5.2). Người tin ngược lại đọc huy hiệu xanh như bằng chứng — đúng ô *im lặng, không chặn*, ô nguy hiểm nhất của buổi.

**Bốn câu phân loại thật:**

| Câu | Phân loại điều gì |
|---|---|
| 2 | Người **đã bị huy hiệu xanh nói dối** — đòi ngay **1** dòng `strategy: depend` và đòi đếm số pipeline cha xanh có con đỏ trong 30 ngày |
| 3 | Người hiểu **`t0` là một thời điểm**, không phải khái niệm; nếu không sẽ không giải thích được vì sao `dotenv` lúc vô dụng trong `rules`, lúc dùng được |
| 8 | Người phân biệt **"rỗng"** với **"lỗi"**: chưa gặp thì `grep` chữ `error`, đã gặp thì đo `${#VAR}` và đếm **3** đường khai biến |
| 12 | Người hiểu **bằng chứng phải nằm ngoài repo** — phản xạ "đọc lại cấu hình" của giai đoạn 1 vô dụng khi cấu hình chỉ có trong kho artifact |

---

## V2. Bộ câu hỏi


<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q01</span>
    <span>Pipeline con có `t0` **riêng**. Điều đó cho bạn làm được **một** việc mà YAML tĩnh không làm được — việc đó là gì, và bạn trả giá bằng cái gì?</span>
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
  Việc đó là **quyết định muộn hơn**. YAML tĩnh được đọc ở `t0`, trước khi bất kỳ tiến trình nào của ta chạy, nên nó không thể chứa **kết quả của một phép tính về repo** (QT 4.1). Pipeline con là lần tạo pipeline **thứ hai**, xảy ra lúc job `trigger` chạy — sau khi job cha đã chạy — nên nó thấy được kết quả của chúng (QT 4.2). Có **2** thời điểm `t0` trong một lần push; khoảng cách giữa chúng bằng thời lượng các job cha chạy trước `trigger`. Con số của ví dụ chuẩn: **12** module × **3** job cho **36** khối, ~**540** dòng ở YAML tĩnh, so với **1** khối `trigger` + **1** script ~**40** dòng.

Ba khoản phải trả: **8–15** giây job `sinh-cau-hinh` **mỗi** pipeline; lỗi có thể nằm trong tệp YAML mà `git show` không tìm thấy (QT 7.2); `CODEOWNERS` trên `.gitlab-ci.yml` không còn che được tập job thật.

**Tiêu chí chấm:**
- 0đ: "Pipeline con cho pipeline gọn hơn", hoặc chỉ nói chia nhỏ cho dễ đọc.
- 1đ: Biết pipeline con sinh lúc chạy, không nêu được `t0` thứ hai là gì.
- 2đ: Nêu đúng cơ chế **2** thời điểm `t0` và việc quyết định muộn hơn.
- 3đ: Như trên, **và** phép tính **12 × 3 = 36** khối so với **1** khối + **40** dòng, **và** ≥ hai trong ba khoản phải trả, có con số **8–15** giây.

**Câu hỏi đào sâu:** Repo của bạn có **3** module. Có nên dùng pipeline động? *(Không — 9 khối thì YAML tĩnh **đơn giản hơn**. Ngưỡng: dưới **10** khối chép lại thì đừng dùng, vì 8–15 giây phải trả mọi lần chạy còn lợi ích chỉ tới khi phép nhân đủ lớn.)*
</div>
</details>

---

### Câu 2 — 🔥

**Hỏi:** Huy hiệu pipeline của nhánh mặc định **xanh** suốt tuần, nhưng bản trên staging thiếu một service, và không job nào đỏ trong pipeline bạn mở ra. Chuyện gì xảy ra, và **một dòng** nào chặn được?

**Đáp án chuẩn:** Pipeline **cha** xanh, pipeline **con** đỏ. Mặc định, nhiệm vụ của bridge job chỉ là *tạo được* pipeline hạ nguồn; kết quả của pipeline đó là chuyện khác và **không** phản chiếu lên cha (QT 5.2). Huy hiệu đọc trạng thái pipeline cha nên nó xanh thật — nó không nói dối về cái nó đo, nó chỉ đo cái ta không muốn biết.

```yaml
trigger-api:
  trigger:
    include: api/con.yml
    strategy: depend        # 1 dòng — bridge job phản chiếu kết quả pipeline con
```

Dòng này tốn **0** giây thêm và đổi đúng một ô của bảng hai thuộc tính (buổi 01 QT 7.1, lần thứ **9**): từ *im lặng, không chặn* sang *ồn ào, có chặn*. Bằng chứng: gọi `/pipelines/:id/bridges` — bridge job không có ở `/jobs` (QT 5.1) — rồi so `.status` của bridge với `.downstream_pipeline.status`. Số mang đi họp: **số pipeline cha xanh có con đỏ trong 30 ngày**; theo kinh nghiệm thực tế, đội dùng `trigger` vài tháng mà chưa đếm thì con số đó không bằng 0.

**Tiêu chí chấm:**
- 0đ: "Cha đỏ khi con đỏ, nên lỗi ở chỗ khác." **Trần điểm cả buổi là 1.**
- 1đ: Đoán có pipeline khác đang đỏ, không nêu được vì sao cha vẫn xanh.
- 2đ: Nêu đúng cơ chế "bridge job chỉ chịu trách nhiệm *tạo được*" **và** viết ra dòng `strategy: depend`.
- 3đ: Như trên, **và** gọi đúng ô *im lặng, không chặn*, **và** đưa lệnh đọc `/bridges` hoặc con số 30 ngày.

**Câu hỏi đào sâu:** Có ca nào **cố ý** không đặt `strategy: depend`? *(Có — pipeline hạ nguồn là việc bắn-và-quên thật sự, ví dụ kích một pipeline cập nhật tài liệu ở repo khác mà kết quả không được phép chặn bản phát hành của ta. Nhưng phải **viết lý do** ngay cạnh dòng đó.)*

---

### Câu 3 — ★★★

**Hỏi:** Buổi 04 nói biến `dotenv` **không** dùng được trong `rules`. Hôm nay ta nói job của pipeline con **dùng được** biến `dotenv` do job cha sinh ra trong `rules` của nó. Hai câu đó có mâu thuẫn không?

**Đáp án chuẩn:** Không, vì chúng nói về **hai lần tạo pipeline khác nhau**. `rules` được đánh giá đúng **một** lần, tại thời điểm pipeline được tạo (buổi 04 QT 4.1 — lần thứ **3** của trục `t0`). Trong **một** pipeline, thời điểm đó nằm trước mọi job nên không job nào kịp sinh biến cho `rules` đọc (buổi 04 QT 4.2). Pipeline con là lần tạo **thứ hai**, xảy ra lúc bridge job chạy, khi job cha trước `trigger` đã xong — biến đã tồn tại trước `t0` của con (QT 4.2).

Điều kiện bắt buộc, và đây là chỗ mất điểm: biến **không** tự nhiên có mặt ở con, phải truyền tường minh qua **3** đường khai với mặc định khác nhau (QT 6.4). Đường cho `dotenv`: nâng thành biến của bridge job bằng `variables: {MODULE_DOI: $MODULE_DOI}` rồi mở `trigger:forward:pipeline_variables`; job con khai `rules: [{if: '$MODULE_DOI == "api"'}]` và chạy đúng. Giới hạn: `t0` thứ hai chỉ mở cửa cho biến đã đi qua cửa `trigger` — ca sai đó im lặng, con chạy với biến rỗng và **xanh** (câu 8).

**Tiêu chí chấm:**
- 0đ: "Buổi 04 sai", hoặc "`dotenv` lúc nào cũng dùng được trong `rules`".
- 1đ: Biết pipeline con khác pipeline cha, không nêu được `rules` đánh giá lúc nào.
- 2đ: Nêu đúng "`rules` đánh giá 1 lần lúc pipeline được tạo" **và** pipeline con là lần tạo thứ hai nên biến đã tồn tại.
- 3đ: Như trên, **và** nêu điều kiện truyền tường minh qua `trigger:forward` cùng con số **3** đường khai, **và** phá bỏ câu "con thấy mọi thứ của cha".

**Câu hỏi đào sâu:** Nếu job sinh biến nằm **sau** job `trigger` trong DAG thì sao? *(Biến không tồn tại lúc `t0` của con, ta quay về đúng giới hạn của buổi 04. Khoảng cách giữa hai `t0` chỉ chứa job **thật sự chạy trước** bridge job, nên thứ tự `needs` (buổi 08 QT 4.1) quyết định biến nào kịp có mặt.)*

---

### Câu 4 — ★★★

**Hỏi:** Job `trigger` tốn bao nhiêu phút runner? Bạn đọc trạng thái của nó ở endpoint nào?

**Đáp án chuẩn:** **0** phút runner, **0** slot, ~**2** giây để tạo pipeline con. Bridge job **không** chạy trên runner: tạo một pipeline là việc của server GitLab, bridge job chỉ là **bản ghi** của hành động đó (QT 5.1). Hệ quả cơ học: nó không có `trace`, không có tám pha của buổi 01 QT 4.2, và không xuất hiện ở `/pipelines/:id/jobs` — nó chỉ có ở `/pipelines/:id/bridges`. So hai danh sách đó là cách duy nhất chứng minh điều này bằng lệnh.

Đây là chỗ **định lượng ngược lại**, phải nói cả hai chiều mới đạt 3 điểm: bridge job là thứ **rẻ nhất trong cả khoá**, nhưng **thứ nó tạo ra thì không rẻ** — job của pipeline con chiếm slot và tính vào hạn mức như job thường, và độ sâu lồng nhau có trần tham chiếu **2** tầng dưới cha (QT 7.1). Đọc riêng QT 5.1 mà không đọc QT 7.1 là cách sinh ra câu "pipeline con miễn phí".

**Tiêu chí chấm:**
- 0đ: "Tốn như job thường", hoặc đi tìm `trace` của bridge job. **Trần điểm cả buổi là 1.**
- 1đ: Biết nó rẻ, không nói được con số và không biết endpoint.
- 2đ: Nêu đúng **0** phút runner cùng cơ chế "tạo pipeline là việc của server" **và** endpoint `/bridges`.
- 3đ: Như trên, **và** con số ~**2** giây, **và** chiều ngược lại: job con vẫn tính vào hạn mức và slot, trần lồng tham chiếu **2** tầng.

**Câu hỏi đào sâu:** Tách một pipeline **6** job thành cha 2 job + con 4 job có tiết kiệm phút runner? *(**Không một giây nào** — vẫn 6 job chạy trên runner, cộng ~2 giây tạo pipeline con. Tách pipeline là quyết định về **quyền sở hữu** và **thời điểm quyết định**; bán nó như cách tiết kiệm phút runner là lặp lại đúng lỗi của buổi 08 với `needs`.)*

---

### Câu 5 — ★★★

**Hỏi:** Kể **bốn** bước của một pipeline động. Bỏ bước nào thì hỏng cái gì?

**Đáp án chuẩn:** Đúng **4** bước, không rút ngắn được bước nào (QT 6.1):

| # | Bước | Bỏ đi thì hỏng gì |
|---|---|---|
| 1 | Một job **đọc trạng thái repo** (`git diff` theo mốc ta chọn) | Không có gì để sinh; quay về YAML tĩnh |
| 2 | Job đó **viết ra** một tệp YAML | Không có tệp cho bridge job đọc |
| 3 | Tệp đó thành **artifact** | Bridge job **đỏ**: nó chỉ đọc được thứ đã nằm trong kho artifact, không có đường nào đọc trực tiếp đầu ra của job khác |
| 4 | Bridge job dùng `trigger:include:artifact` | Tệp sinh ra nằm im, pipeline con không bao giờ tồn tại |

Bước 3 hay bị hiểu sai: người ta tưởng bridge job "thấy" được tệp job trước vừa tạo, cơ chế thật là nó đọc **kho artifact**. Ca thứ năm phải xử lý tường minh: tệp sinh ra **rỗng job** thì pipeline con **không được tạo** — đúng ca **0 job → 0 pipeline** của buổi 04 QT 4.3, lần thứ **2**. Cách đúng là `[ -s module-doi.txt ] ||` sinh thêm **1** job giữ chỗ `khong-co-gi-doi`, không để tệp rỗng.

**Tiêu chí chấm:**
- 0đ: Kể được một, hai bước rời rạc; không có thứ tự.
- 1đ: Kể đủ ý "sinh YAML rồi trigger", thiếu bước artifact.
- 2đ: Kể đúng **4** bước theo thứ tự **và** nói đúng vai trò của artifact ở bước 3.
- 3đ: Như trên, **và** cơ chế "bridge job chỉ đọc được kho artifact", **và** ca **0 job → 0 pipeline** cùng cách xử lý bằng **1** job giữ chỗ.

**Câu hỏi đào sâu:** Lớp push một commit chỉ sửa `README`. Bạn thấy gì? *(Đã xử lý ca 0 job: pipeline con có đúng **1** job `khong-co-gi-doi`, xanh, ta biết chắc script đã chạy. Chưa xử lý: pipeline con **không xuất hiện** và bridge job cho một kết quả **phải đo**, nên ta không phân biệt được "không có gì đổi" với "script hỏng".)*

---

### Câu 6 — ★★★

**Hỏi:** Script sinh cấu hình viết ra một tệp YAML sai thụt lề. Lỗi đó bị chặn ở đâu, tốn mấy giây? Nếu không chặn thì triệu chứng trông thế nào?

**Đáp án chuẩn:** Chặn **trong cùng job đã sinh nó**, bằng **1** lệnh gọi `POST /ci/lint`, tốn ~**1** giây, và script tự `exit 1` nếu `valid == false` (QT 6.2).

```bash
# mảnh — trong sinh-pipeline.sh, ngay sau khi con.yml được viết xong
KQ=$(jq -Rs '{content: .}' < con.yml | curl -sf -H "PRIVATE-TOKEN: $TOKEN" \
     -H 'Content-Type: application/json' --data @- "$GITLAB/api/v4/projects/$PID/ci/lint")
[ "$(echo "$KQ" | jq -r '.valid')" = "true" ] || { echo "$KQ" | jq -r '.errors[]'; exit 1; }
```

`ci/lint` hơn `yq` ở một chỗ: nó trả tệp **sau phân giải** (buổi 03 QT 4.3, lần thứ **2**), nên bắt được cả lỗi **cú pháp** lẫn lỗi **cấu trúc CI** — `stage` không tồn tại, `needs` trỏ job vắng mặt. Không chặn thì triệu chứng là bridge job đỏ với lỗi cú pháp **ở dòng 47 của một tệp mà `git show` không tìm thấy**; đó là lý do QT 6.2 và QT 7.2 là hai mặt của một việc.

**Tiêu chí chấm:**
- 0đ: "Chạy thử rồi sửa", hoặc "GitLab sẽ báo lỗi khi tạo pipeline con".
- 1đ: Biết nên kiểm YAML trước, đề xuất một công cụ YAML thuần cục bộ.
- 2đ: Nêu đúng `ci/lint` **trong cùng job** cùng `exit 1`, và con số ~**1** giây.
- 3đ: Như trên, **và** vì sao `ci/lint` hơn công cụ YAML thuần, **và** triệu chứng "lỗi dòng 47 của tệp `git show` không tìm thấy".

**Câu hỏi đào sâu:** Vì sao lint phải nằm **trong** job sinh cấu hình, không phải một job riêng sau đó? *(Job riêng có thể bị `needs` bỏ qua, bị `allow_failure` làm mềm, hoặc bị người sau xoá — việc không lint lại thành **có thể**. Đặt cùng job với `exit 1` biến nó thành **không thể**: tệp không hợp lệ thì không bao giờ tới kho artifact. Đó là khác biệt giữa một lời khuyên và một cơ chế.)*

---

### Câu 7 — ★★★

**Hỏi:** `rules:changes` sai âm thầm ở **ba** ca, `changes:compare_to` sửa được **hai**. Ca thứ ba là ca nào, và pipeline động giải nó bằng gì?

**Đáp án chuẩn:** Ba ca của buổi 04 QT 6.3 (lần thứ **2** của nguyên lý này): **nhánh mới tạo** — không có commit trước nên GitLab coi mọi tệp đều đổi; **pipeline theo lịch** — không có commit mới nên không tệp nào "đổi", job `changes` không chạy lần nào; **push nhiều commit một lần** — mốc so sánh là commit trước cả lần push nên ta **không chọn được** mốc mình muốn.

`compare_to` sửa hai ca đầu vì nó cho khai một `ref` cố định làm mốc. Ca thứ **3** thì không: `compare_to` nhận **một** ref tĩnh, còn mốc đúng thường là `git merge-base "origin/$CI_DEFAULT_BRANCH" HEAD` — giá trị chỉ tính được bằng **lệnh** trong job, rồi `git diff --name-only "$MOC"...HEAD` lọc ra danh sách module (QT 6.3). Cơ chế một câu: ở `t0` ta không có gì ngoài cơ chế của nền tảng; **trong job** ta có cả cây git và cả quyền chạy lệnh.

Phá bỏ để đạt 3 điểm: pipeline động **không** giải được ca **người viết script chọn sai mốc** — nó chỉ chuyển trách nhiệm từ nền tảng sang ta, ô hỏng vẫn *im lặng, không chặn*. Vì vậy lab **đo cả ba** ca.

**Tiêu chí chấm:**
- 0đ: "Dùng `compare_to` là xong", hoặc không biết `changes` có mốc so sánh.
- 1đ: Kể được một, hai ca; không nói được `compare_to` sửa ca nào.
- 2đ: Kể đủ **3** ca, nói đúng `compare_to` sửa **2** và ca thứ ba cần lệnh `git` trong job.
- 3đ: Như trên, **và** viết được `git merge-base` cùng cơ chế "trong job có cây git", **và** phá bỏ: pipeline động không sửa ca chọn sai mốc.

**Câu hỏi đào sâu:** Job security có nên dùng `rules:changes`? *(Không — buổi 04 đã chốt: gate chạy thừa tốn vài chục giây, gate biến mất im lặng thì không ai biết. Pipeline động chỉ đổi **ai** viết ra bộ lọc.)*

---

### Câu 8 — ★★★

**Hỏi:** Pipeline con chạy xong, **xanh**, nhưng việc không được làm: biến `MOI_TRUONG` bên trong nó rỗng, và không đâu có dòng lỗi nào. Bạn điều tra thế nào?

**Đáp án chuẩn:** Đây là ca phân biệt **"rỗng"** với **"lỗi"**. Shell coi biến rỗng là hợp lệ nên `script` chạy hết và trả về 0 — job xanh (lần thứ **7** của "job xanh không chứng minh gì"). Không có gì để `grep` trong `trace`, vì đây không phải lỗi.

**Nhịp 1 — đo, đừng đoán:** in `echo "len=${#MOI_TRUONG}"`, không in giá trị, vì biến `masked` sẽ thành `[MASKED]` còn biến rỗng in ra một dòng trắng giống hệt biến vắng mặt.

**Nhịp 2 — đếm ba đường khai.** Biến xuống pipeline con theo **3** đường với mặc định **không** giống nhau (QT 6.4): khai ở `variables` cấp trên cùng của cha · khai ở cấp **job** của bridge · `trigger:forward` (`yaml_variables` và `pipeline_variables` là hai công tắc riêng). `inherit:variables` cắt được đường thứ nhất (buổi 06 QT 7.1, lần thứ **2**). Đây là đại lượng loại (c) — **phải đo, không tra**; lab chạy đủ ba ca, gồm `inherit:variables: false`.

**Nhịp 3 — biến im lặng thành ồn ào:** một dòng ở đầu job con, `: "${MOI_TRUONG:?bien khong xuong duoc}"`, hàng rào chuẩn của khoá từ buổi 06 QT 5.2. Biến của con vẫn thuộc **chín** nấc của buổi 06 QT 4.1, và biên giới pipeline chèn thêm **một** lớp lên trên chín nấc đó — nên câu hỏi đúng là **"biến này thắng ở nấc nào của pipeline con"**.

**Tiêu chí chấm:**
- 0đ: "Job xanh thì không có vấn đề", hoặc đi tìm chữ `error` trong `trace`.
- 1đ: Nghi biến không xuống, không nêu được cách đo và cách khai.
- 2đ: In `${#VAR}` để đo **và** kể được ≥ hai trong ba đường khai biến.
- 3đ: Như trên, **và** kể đủ **3** đường cùng `inherit:variables`, **và** đề xuất `: "${VAR:?}"` để biến ô *im lặng, không chặn* thành job đỏ.

**Câu hỏi đào sâu:** `${#VAR}` cho **0** — biến rỗng hay biến chưa khai? *(Cùng một quan sát cho hai ca, đó là giới hạn của phép đo. Phân biệt bằng `${VAR+co-khai}`: in ra `co-khai` thì biến tồn tại và rỗng; in ra chuỗi trắng thì nó chưa bao giờ xuống được. Hai ca sửa ở hai chỗ khác nhau — giá trị, hay đường khai.)*

---

### Câu 9 — ★★

**Hỏi:** Artifact có tự chảy giữa pipeline cha và pipeline con không? Trả lời cho **cả hai chiều**.

**Đáp án chuẩn:** **Không**, cả hai chiều, và **2** chiều phải khai riêng (QT 5.3). Hợp đồng artifact của buổi 05 QT 4.1 nằm **trong** một pipeline; qua biên giới pipeline nó phải được khai lại. Chiều **cha → con**: con không tự nhận gì; tệp **cấu hình** đi bằng `trigger:include:artifact`, dữ liệu khác thì job con tự tải bằng API. Chiều **con → cha**: cha không tự nhận gì, job cha sau `trigger` phải khai `needs: [{job: trigger-con}, {pipeline: $CI_PIPELINE_ID, job: gop}]`.

Chế độ hỏng: job cha đứng sau `trigger` chạy với **0** tệp và vẫn **xanh** vì không có khẳng định nào (buổi 05 QT 5.3, lần thứ **2**). **1** dòng `test -s bao-cao.json` trước khi đọc tệp là thứ duy nhất biến ca thiếu tệp thành ồn ào.

**Tiêu chí chấm:**
- 0đ: "Có, artifact dùng chung trong cả cây pipeline."
- 1đ: Biết phải khai gì đó, chỉ nói được một chiều.
- 2đ: Nói đúng **không** ở cả **2** chiều và nêu `needs:pipeline:job` cho chiều con → cha.
- 3đ: Như trên, **và** nêu chế độ hỏng "job cha chạy với 0 tệp mà vẫn xanh" cùng **1** dòng `test -s`.

**Câu hỏi đào sâu:** `trigger:include:artifact` có phải là "artifact chảy từ cha xuống con"? *(Không hẳn — đó là **server** đọc kho artifact để lấy tệp cấu hình lúc tạo pipeline con, không phải job của con tải tệp về vùng làm việc. Phân biệt này giải thích vì sao chỉ tệp cấu hình đi được đường đó, còn dữ liệu thì không.)*

---

### Câu 10 — ★★

**Hỏi:** Monorepo **12** thư mục module, mỗi module cần **3** job. YAML tĩnh cần bao nhiêu khối, khoảng bao nhiêu dòng? Pipeline động cần bao nhiêu? Thêm module thứ **13** thì mỗi bên sửa gì?

**Đáp án chuẩn:** Phép nhân, nói ra bằng miệng:

| | YAML tĩnh | Pipeline động |
|---|---|---|
| Số khối job phải bảo trì | **12 × 3 = 36** | **1** khối `trigger` |
| Số dòng phải bảo trì | ~**540** (≈15 dòng/khối) | ~**40** dòng `sinh-pipeline.sh` |
| Thêm module thứ 13 | **+3** khối, ~**+45** dòng, **1** merge request | **0** dòng — thêm thư mục là xong |
| Chi phí mỗi lần chạy | **0** giây thêm | **8–15** giây job `sinh-cau-hinh` |

Cơ chế: tệp cấu hình đọc ở `t0` nên không thể chứa **kết quả của một phép tính** về repo (QT 4.1). `rules:changes` cắt job được **chạy** nhưng **không** cắt số khối phải **viết** — chỗ nhầm của câu "tôi đã có `rules` nên không cần pipeline động". Phá bỏ: **36** là số của ví dụ 12 module; ngưỡng thực dụng **10** khối chép lại, dưới đó pipeline động là lựa chọn **sai**.

**Tiêu chí chấm:**
- 0đ: "Nhiều lắm", hoặc "tuỳ repo" mà không có phép nhân nào.
- 1đ: Nói được YAML tĩnh dài hơn, không tính ra con số.
- 2đ: Tính đúng **36** khối và ~**540** dòng so với **1** khối + ~**40** dòng.
- 3đ: Như trên, **và** cột "thêm module thứ 13" bằng **+3 khối** so với **0 dòng**, **và** phá bỏ con số bằng ngưỡng **10** khối cùng chi phí **8–15** giây.

**Câu hỏi đào sâu:** `parallel:matrix` của buổi 08 tả được ca này không? *(Không. `matrix` nhân job theo **phép nhân** trên các trục ta khai trước (buổi 08 QT 6.2), nên nó vẫn đòi danh sách 12 module nằm trong YAML và không cho mỗi module một `script` khác nhau. Nó giảm số **dòng**, không giảm số **quyết định phải khai trước `t0`**.)*

---

### Câu 11 — ★★★

**Hỏi:** Có **ba** loại quan hệ pipeline. Chúng khác nhau ở đâu? Trả lời bằng **quyền sở hữu**, không bằng cú pháp.

**Đáp án chuẩn:** Cú pháp `trigger` gần giống nhau ở cả ba nên người ta chọn theo tiện; nhưng hệ quả là **ai đổi được cấu hình mà không cần merge request của ta** (QT 4.3). **3** câu hỏi sở hữu phải trả lời trước khi chọn:

| Loại | Ai giữ YAML | Ai xem được log | Ai đổi được mà không xin phép ta |
|---|---|---|---|
| **child** (`trigger:include`, cùng repo) | Ta | Ta | Chỉ người có quyền vào repo ta |
| **multi-project** (`trigger:project`) | **Đội khác** | Cần quyền ở project kia — hay bị thiếu | **Đội khác**, bất cứ lúc nào |
| **lồng nhau** (con của con) | Ta, ở **2** tầng cấu hình | Phải mở **3** pipeline mới thấy hết | Ta — nhưng bằng chứng bị che thêm một tầng |

Dấu hiệu chọn sai: pipeline hỏng vì đội khác **đổi tên job**, commit gần nhất của repo ta không liên quan gì (buổi 08 QT 7.2, lần thứ **2**). Kết luận: **đừng** dùng `trigger:project` khi hai đội chưa thoả thuận về **tên job** và **tên artifact**; để dùng lại **cấu hình** giữa các repo thì nó là công cụ sai — đó là `include` (buổi 10) và component (buổi 11).

**Tiêu chí chấm:**
- 0đ: Kể được tên ba loại, không phân biệt được gì.
- 1đ: Phân biệt bằng cú pháp: "một cái `include`, một cái `project`".
- 2đ: Nêu đúng **3** câu hỏi sở hữu và áp được cho `trigger:project`.
- 3đ: Như trên, **và** dấu hiệu "đội khác đổi tên job, commit của ta không liên quan", **và** nêu `trigger:project` là công cụ sai cho việc dùng lại cấu hình.

**Câu hỏi đào sâu:** Lồng ba tầng "cho gọn" có được không? *(Trần độ sâu có giá trị tham chiếu **2** tầng dưới cha ở GitLab 17.7, và đó là loại (c) — **phải đo** trên instance của lớp. Kể cả khi trần cho phép, mỗi tầng lồng che thêm một lớp bằng chứng: phải mở 3 pipeline và tải 2 tệp cấu hình sinh ra mới dựng lại được lần chạy đó.)*

---

### Câu 12 — 🔥

**Hỏi:** Một pipeline con hỏng **hôm qua**. Hôm nay chạy lại trên đúng commit đó thì bình thường, và không ai chỉ ra được YAML hôm qua khác hôm nay ở chỗ nào. Dựng quy trình truy nguyên, và nói rõ bạn cần cái gì đã tồn tại **trước** khi sự cố xảy ra.

**Đáp án chuẩn:** Câu này đo việc hiểu **bằng chứng phải nằm ngoài repo**. Điểm chốt: `git show` **không còn** là bằng chứng, vì tệp gây lỗi chưa từng nằm trong lịch sử git (QT 7.2). Thứ đã đổi giữa hai lần chạy có thể là mốc so sánh của `git diff`, danh sách module đổi, một biến của cha, hoặc trạng thái nhánh đích — tất cả nằm **ngoài** commit.

**Nhịp 1 — điều kiện tiên quyết, phải có trước:** `artifacts: {when: always, expire_in: 7 days, paths: [con.yml, module-doi.txt]}` cho job sinh cấu hình (buổi 05 QT 5.4, lần thứ **2**), tốn ~**4** kB mỗi pipeline. Không có nó thì cuộc điều tra **kết thúc ở đây**, và đó là câu trả lời trung thực phải nói ra. **Nhịp 2:** tải hai bản `con.yml` rồi `diff`, bước thay cho `git diff` mà ta vừa mất. **Nhịp 3 — báo cáo gỡ rối 5 dòng:** mẫu **4** dòng của buổi 07 QT 7.3 thêm **1** dòng, dùng cho mọi buổi từ đây:

| Dòng | Nội dung cho ca này |
|---|---|
| Triệu chứng | Pipeline con của bridge `trigger-api` đỏ hôm qua 14:02; hôm nay cùng SHA thì xanh |
| **Tệp cấu hình thật của lần chạy đó** | `con.yml` tải từ artifact job `sinh-cau-hinh` pipeline #4181 — **dòng mới của buổi 09** |
| Bằng chứng | `$ diff con-4181.yml con-4222.yml` cho **2** job khác nhau: hôm qua có `test-worker`, hôm nay không |
| Nguyên nhân | Mốc so sánh là `HEAD~1`; hôm qua push nhiều commit nên tập module đổi khác (QT 6.3) |
| Cách sửa | Đổi mốc sang `git merge-base origin/$CI_DEFAULT_BRANCH HEAD`; lưu `module-doi.txt` làm artifact |

Nhánh thứ hai nếu `diff` không cho gì: số job của con **vượt trần** đúng hôm đó — trần số job là loại (c), **phải đo** bằng cách sinh **5 · 20 · 60** job (QT 7.1).

**Tiêu chí chấm:**
- 0đ: "Chạy lại là hết", hoặc đi `git log` tìm commit khác nhau.
- 1đ: Nghi cấu hình sinh ra khác nhau, không nêu được cách lấy lại nó.
- 2đ: Nêu đúng "`git show` không còn là bằng chứng" **và** đòi artifact `when: always`, có bước `diff` hai bản.
- 3đ: Như trên, **và** nói rõ điều kiện đó phải có **trước** sự cố cùng câu "không có nó thì điều tra kết thúc", **và** đưa báo cáo **5** dòng với dòng "tệp cấu hình thật của lần chạy đó".

**Câu hỏi đào sâu:** `expire_in: 7 days` có đủ không? *(Tuỳ vòng phản hồi của đội: sự cố bị bỏ qua cuối tuần rồi mở vé thứ Ba là **4** ngày, vẫn kịp; sự cố phát hiện qua báo cáo hằng tháng thì không. Chọn theo "bao lâu thì một sự cố mới được nhìn tới", và **4** kB mỗi pipeline là mức rẻ đủ để chọn dài hơn cho an toàn.)*

---

## V3. Câu chốt để nói khi phỏng vấn

> Bốn câu dưới đây viết **nguyên văn, đúng ngữ điệu nói**. Học viên tập nói to từng câu tới khi trôi chảy mà không phải nghĩ. Mỗi câu chứa **một con số** hoặc **một cơ chế**.

**Câu 1 — khi được hỏi "vì sao phải dùng pipeline động":**

> "Vì `.gitlab-ci.yml` được đọc ở `t0`, trước khi bất cứ tiến trình nào của tôi chạy — nên nó **không thể chứa kết quả của một phép tính** về repo. Với monorepo mười hai module, mỗi module ba job, tôi phải bảo trì **ba mươi sáu** khối, khoảng **năm trăm bốn mươi** dòng. Pipeline động mua cho tôi một `t0` **thứ hai**: một job đọc `git diff` rồi **viết ra** đúng tập job cần thiết, nên trong một lần push tôi có **hai** thời điểm quyết định, và cái thứ hai biết nhiều hơn. Cái tôi trả là **tám tới mười lăm giây** mỗi lần chạy — nên tôi có ngưỡng: dưới **mười** khối chép lại thì tôi không dùng."

**Câu 2 — khi được hỏi "tách pipeline ra có tốn thêm không":**

> "Job `trigger` thì gần như không: nó là **bridge job**, và bridge job **không chạy trên runner** — tạo một pipeline là việc của server GitLab, còn bridge job chỉ là bản ghi của hành động đó. **Không** slot, **không** phút runner, khoảng **hai giây**, và bạn sẽ không thấy nó ở `/jobs`, nó nằm ở `/bridges`. Nhưng tôi luôn nói kèm câu thứ hai vì câu đầu bị lạm dụng nhiều nhất: **thứ nó tạo ra thì không rẻ** — job của pipeline con chiếm slot và tính vào hạn mức đúng như job thường. Tách một pipeline sáu job thành cha hai cộng con bốn **không tiết kiệm một giây phút runner nào**; tôi tách vì quyền sở hữu và vì thời điểm quyết định, không bao giờ vì chi phí."

**Câu 3 — khi được hỏi "bạn từng gặp sự cố nào mà mọi thứ đều xanh":**

> "Có, và đó là thứ tôi kiểm đầu tiên khi nhận một repo có `trigger`. Huy hiệu của nhánh mặc định xanh cả tuần, mà bản trên staging thiếu hẳn một service. Nguyên nhân là pipeline **cha** xanh còn pipeline **con** đỏ: mặc định, nhiệm vụ của bridge job chỉ là *tạo được* pipeline kia. Cách sửa là **một** dòng, `strategy: depend`, tốn **không giây nào**, và nó đổi đúng một ô: từ *im lặng, không chặn* sang *ồn ào, có chặn*. Việc đầu tiên tôi làm là `grep -n 'trigger:'` — mỗi bridge job thiếu dòng đó là một chỗ pipeline cha đang nói dối. Rồi tôi đếm bằng API: **ba mươi ngày qua có bao nhiêu pipeline cha xanh mà con đỏ**."

**Câu 4 — khi được hỏi "gỡ rối pipeline động khác gỡ rối pipeline thường ở đâu":**

> "Khác ở một chỗ và nó đổi cả quy trình: từ lúc cấu hình sinh lúc chạy, **`git show` không còn là bằng chứng**. Tệp YAML gây lỗi hôm qua chưa từng nằm trong lịch sử git, nên nếu tôi không lưu nó lại đúng lần chạy đó thì hôm nay tôi không có gì để so. Vì vậy `con.yml` của tôi luôn là artifact với `when: always` — **always**, vì lần tôi cần nó nhất là lần job đỏ — và nó tốn khoảng **bốn kB** mỗi pipeline. Hệ quả thứ hai: mẫu báo cáo gỡ rối của tôi từ buổi này có **năm** dòng thay vì bốn, dòng thêm là **tệp cấu hình thật của lần chạy đó**. Câu tôi hỏi đầu tiên khi ai đó báo lỗi luôn là: **tệp YAML đó có trong repo không?**"

---

## V4. Bảng ghi điểm

| Học viên | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | Tổng | Trần điểm? |
\g<1>| | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | |

**Quy đổi** (tính trên số câu thực hỏi, mỗi câu tối đa 3 điểm):

| Tỉ lệ điểm | Kết luận |
|---|---|
| ≥ 80% | Nắm vững. Giao BT mở rộng §L10 về đo trần số job của pipeline con, làm trước buổi 10 |
| 60–79% | Đạt. Đọc lại quy tắc bị mất điểm trước buổi 10 |
| 40–59% | Chưa đạt. Làm lại bước lab 2 và bước lab 3 ở nhà, nộp lại `sinh-pipeline.sh` cùng `con.yml` của ba lần chạy |
| < 40% | Chưa đạt. Học lại cả buổi — `t0` thứ hai và `strategy: depend` còn quay lại ở buổi 11, 12, 22, 41, 43, 44 |

**Bảng lỗi làm trần điểm là 1:**

| Lỗi | Vì sao nghiêm trọng đến mức trần điểm |
|---|---|
| "Job `trigger` chạy trên runner và tốn phút runner" | Sai cả con số **0** phút runner lẫn endpoint `/bridges`. Người tin ngược lại đi tìm `trace` của một job không có `trace`, và chặn việc tách pipeline vì "sợ cạn slot" trong khi thủ phạm là job **trong** pipeline con |
| "Pipeline cha tự đỏ khi pipeline con đỏ" | **1** dòng `strategy: depend` là thứ duy nhất bắt cha phản chiếu con. Người tin ngược lại đọc huy hiệu xanh như bằng chứng — đúng ô *im lặng, không chặn* |

---

## V5. Bài tập về nhà

### BTVN 1. Quét `trigger` và đếm số pipeline cha xanh có con đỏ

Việc này **không đụng repo**, làm được ngay hôm nay:

1. `grep -n 'trigger:' .gitlab-ci.yml` — mọi bridge job **không** có `strategy: depend` là một chỗ pipeline cha đang nói dối. Đếm số chỗ đó.
2. Với **100** pipeline gần nhất của nhánh mặc định, gọi `/pipelines/:id/bridges` và đếm số pipeline **cha xanh** có **con đỏ**.

**Nộp:** hai con số cùng lệnh đã dùng ở việc 2. Nếu con số thứ hai lớn hơn 0: bridge job nào, và dòng bạn định thêm nằm ở dòng số mấy của tệp nào.

### BTVN 2. Ba đường khai biến, đo bằng `${#VAR}`

Trên một **nhánh riêng**, dựng một cha và một con, khai **3** biến ở **3** chỗ: `variables` cấp trên cùng của cha · cấp job của bridge · `trigger:forward`. Job đầu của con in `${#VAR}` cho cả ba. Chạy **3** ca: mặc định · `forward: {pipeline_variables: true}` · `inherit:variables: false`.

**Nộp:** bảng **3 × 3** với ô là độ dài biến, cộng **một** câu: đường nào không cần khai gì thêm, đường nào bị `inherit:variables: false` cắt. Đây là đại lượng loại (c) — nộp số bạn **đo được**, không nộp số trong tài liệu.

### BTVN 3. Đo trần, nhưng lưu bằng chứng trước khi phá

Đúng thứ tự này, không đảo:

1. Thêm `artifacts: {when: always, expire_in: 7 days, paths: [con.yml]}` cho job `sinh-cau-hinh` **trước**.
2. Sinh pipeline con **5**, rồi **20**, rồi **60** job. Ghi ca nào bị từ chối và thông báo lỗi nguyên văn.
3. Lồng ba tầng (con của con của con). Trần tham chiếu là **2** tầng dưới cha, nhưng số của instance lớp là số bạn **phải đo**.

**Nộp:** ba dòng kết quả kèm thông báo lỗi nguyên văn, cộng **một** đoạn 3–5 dòng: nếu **không** làm việc 1 trước, bạn còn điều tra được ca thất bại ở việc 2 bằng gì? Trả lời "không còn gì" được chấp nhận nếu đúng.

### BTVN 4. Chuẩn bị cho buổi 10

Trả lời ba câu sau bằng viết, mỗi câu 3–5 dòng. Mang theo vào buổi 10.

1. `sinh-pipeline.sh` sinh YAML bằng cách **nối chuỗi**. Hãy kể **mọi** cách bạn biết để dùng lại một khối YAML **mà không** nối chuỗi — và với mỗi cách, đoán xem nó được **hợp nhất lúc nào**: trước khi GitLab đọc tệp, lúc GitLab ghép các tệp, hay sau khi đã ghép?
2. `trigger:project` là hợp đồng giữa hai đội (QT 4.3). Nếu bạn chỉ muốn dùng lại **cấu hình** của đội khác chứ **không** muốn chạy pipeline của họ, bạn làm thế nào? Ghi phỏng đoán, kể cả khi chưa biết cú pháp.
3. `ci/lint` trả về tệp **sau phân giải** (QT 6.2). Hãy lấy một repo có `include` rồi so tệp thô với tệp sau phân giải: khối nào bị **ghi đè**, khối nào được **trộn**?

**Ba câu này dẫn vào đâu:** cả ba dẫn vào cùng một luận đề của buổi 10 — **ba cơ chế dùng lại có ba thời điểm hợp nhất khác nhau, và nhầm thời điểm là gốc của lỗi ghi đè**. Câu 1 dẫn vào **§4 buổi 10 — ba thời điểm hợp nhất (QT 4.1)**: các cơ chế bạn kể ra (anchor · `include` · `extends` · `!reference`) được xử lý ở **ba** thời điểm theo một thứ tự cố định, và cột "đoán thời điểm" của bạn được đối chiếu ngay tại chỗ. Câu 2 dẫn vào **§5 buổi 10 — bốn loại `include` (QT 5.1)**: câu trả lời là `include:project`, không phải `trigger`, và bốn loại `include` khác nhau đúng ở **ba câu hỏi sở hữu** của hôm nay — trong đó `include:remote` là loại duy nhất nội dung đổi được **mà không có commit nào**. Câu 3 dẫn vào **§4 buổi 10 QT 4.3 cùng bước lab 1 của buổi 10**: `merged_yaml` thành công cụ **chính**, và hai ca ghi đè bạn tìm được sẽ được giải thích ở **§5 QT 5.2** (job cùng tên trộn theo **khoá**, tệp gốc thắng chỉ ở khoá nó khai) và **§6 QT 6.1** (`extends` trộn sâu từ điển nhưng **thay thế** mảng: `script` **3** dòng thành **1** dòng, **0** cảnh báo).
{% endraw %}
