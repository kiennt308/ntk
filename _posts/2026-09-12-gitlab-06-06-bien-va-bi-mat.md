---
layout: post
title: "[Bài 06] Quản Lý Biến & Bảo Mật Secrets: CI/CD Variables, Masked / Protected Variables & File-type Variables"
date: 2026-09-12 08:40:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-06
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 6
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.06] Hướng dẫn chuyên sâu Quản Lý Biến & Bảo Mật Secrets: CI/CD Variables, Masked / Protected Variables & File-type Variables: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

{% raw %}
# [BÀI 06] QUẢN LÝ BIẾN & BẢO MẬT SECRETS: CI/CD VARIABLES, MASKED / PROTECTED VARIABLES & FILE-TYPE VARIABLES

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · executor `docker`.
> Mọi đoạn YAML dán được vào `.gitlab-ci.yml` và chạy trong dưới 60 giây.
> Lệnh `curl` dùng bốn biến đã có từ buổi 01: `$GITLAB`, `$GITLAB_TOKEN`, `$PID`, `$PIPE`.

---





Gọi ngẫu nhiên, mỗi câu 1 phút. Năm câu này là năm mảnh nền mà buổi hôm nay dựng trực tiếp lên. Ai sai câu 2 sẽ tắc ở QT 4.1; ai sai câu 3 sẽ tắc ở QT 5.2.

| # | Câu hỏi | Đáp án vắn tắt | Dẫn vào đâu hôm nay |
|---|---|---|---|
| 1 | Artifact khác cache ở **chủ giữ** nào | Artifact do **server** giữ và **có** API; cache do **runner** giữ và **không** có API (buổi 05 QT 4.1) | §5 QT 5.1 — biến masked ghi vào artifact thì đọc lại được **bằng API** |
| 2 | `cache:key` tính lúc nào | Lúc **job bắt đầu, trên runner** — không phải `t0`; `key:files` tối đa **2** tệp (buổi 05 QT 4.2) | §4 QT 4.1 — khoá đó đọc biến, biến sai thì khoá sai |
| 3 | Vì sao job upload artifact rỗng vẫn xanh | Upload là bước riêng sau `script`, **không** cộng vào mã thoát; chặn bằng **1** dòng `test -s` (buổi 05 QT 5.3) | §5 QT 5.2 — biến rỗng cũng không cộng vào mã thoát |
| 4 | Cache 380 MB hoà vốn sau mấy lần trúng | **2** lần; `p × (tạo_lại − giải_nén) > nén_và_tải` (buổi 05 QT 6.3) | §4 QT 4.1 — biến sai làm tỉ lệ trúng về **0%** |
| 5 | Cùng đường dẫn ở cache và artifact thì cái nào thắng | **Artifact** — thứ tự **4** bước đầu job: clone → cache → artifacts → `script` (buổi 05 QT 7.2) | §4 — hôm nay làm việc đó cho biến, với **9** nấc chứ không phải 2 |



Buổi 05 khép lại hai đường ở giữa của bốn đường vào một job. Còn đúng **một** đường chưa mổ: biến môi trường — đường thứ tư của buổi 01 QT 5.1, và là đường vào duy nhất mà học viên **không** kiểm chứng được bằng cách đọc repo. Buổi 05 để lại hai đầu mối: `cache:key` đọc biến (buổi 05 QT 4.2) — biến lấy giá trị từ một nấc không ai ngờ thì khoá cache sai mà log không có chữ nào là "lỗi"; và `artifacts:reports:dotenv` sinh biến cho job sau (buổi 05 QT 5.4) — biến đó nằm nấc nào, thắng ai thua ai. Buổi 03 QT 7.2 cũng hoãn đúng câu này một lần. Hôm nay trả nợ cả ba.

**Luận đề trung tâm.**

> **Biến trong GitLab CI đến từ CHÍN nguồn, và thứ tự ưu tiên giữa chúng là thuộc tính của NỀN TẢNG, không phải của tệp `.gitlab-ci.yml`. Vì vậy không ai đọc được giá trị thật của một biến bằng cách đọc YAML — mọi ca "biến không có giá trị đúng" đều giải được bằng đúng một bảng chín nấc, và bảng đó phải tự tay đo mới tin được.**

```
   NẤC CAO GHI ĐÈ NẤC THẤP — 9 nấc, cao nhất trước:

   1  pipeline variables      (trigger · schedule · bấm tay · API)   ← ngoài repo, khó thấy nhất
   2  project variables       (Settings > CI/CD)                     ← ca "sửa YAML không tác dụng"
   3  group variables
   4  instance variables
   5  dotenv của job trước    (chỉ tới job SAU, cần needs/dependencies)
   6  variables: cấp JOB      trong .gitlab-ci.yml
   7  variables: cấp TRÊN CÙNG trong .gitlab-ci.yml
   8  deployment variables    (từ tích hợp môi trường)
   9  predefined variables    CI_*                                   ← thấp nhất, nên ghi đè được

   Học viên KHÔNG được tin sơ đồ này. Bước 1 lab bắt buộc đo lại từng cặp nấc.
```

Dòng cuối của sơ đồ là quy định thi hành, không phải câu nói khiêm tốn: đây là **thứ tự tham chiếu** của GitLab CE 17.7, ranh giới giữa vài nấc kề nhau đã đổi trong dòng 15.x–17.x, nên nó là phát biểu loại (c) và bước 1 lab đo lại **tám cặp** nấc kề nhau.

**Kết quả buổi trước được dùng lại.** Mỗi dòng là một tiền đề; thiếu nó thì phần tương ứng hôm nay nghe như quy ước tuỳ ý.

| Kết quả | Nguồn | Dùng ở đâu hôm nay |
|---|---|---|
| Biến là **một** trong bốn đường vào job | buổi 01 QT 5.1 | §4 — hôm nay mổ đường thứ tư, đường cuối cùng chưa mổ |
| Ba nấc ưu tiên của `image`/`cache`/`artifacts` | buổi 03 QT 7.1 | §4 QT 4.4 — biến có **chín** nấc, và **không** theo quy tắc ba nấc đó |
| `variables` cấp trên cùng không thuộc `default:` | buổi 03 QT 7.2 | §4 — hôm nay trả nợ đúng câu buổi 03 đã hoãn |
| Biến `dotenv` không dùng được trong `rules` | buổi 04 QT 4.2 | §4 QT 4.3 — **lần thứ 2**, giờ giải thích bằng nấc 5 của bảng |
| `cache:key` đọc biến, tính trên runner | buổi 05 QT 4.2 | §4 QT 4.1 — biến sai làm khoá sai, trúng cache **0%** |
| `artifacts:reports:dotenv` sinh biến cho job sau | buổi 05 QT 5.4 | §4 QT 4.3 — nấc 5, và giới hạn của nó |
| Khẳng định chặn hỏng im lặng | buổi 01 QT 7.3 | §5 QT 5.2 — biến rỗng phải làm job **đỏ** ngay, không được để chạy tiếp |
| Bảng hai thuộc tính hỏng | buổi 01 QT 7.1 | §4, §5, §6 — **lần thứ 6** |
| `workflow` chuẩn của khoá | buổi 04 lab B5 | Lab §L1 — dán vào để mỗi ca đo chỉ sinh **1** pipeline |
| `doc-pha.sh` đọc `trace` qua API | buổi 05 lab B4 | Lab bước 3 và bước 5 — dùng lại để đọc log tìm dấu vết biến |

**Nguyên lý xuất hiện lần thứ mấy.** Giảng viên **nói ra con số** để học viên thấy đây là công cụ dùng lại, không phải khẩu hiệu:

- **Bảng hai thuộc tính hỏng** — **lần thứ 6**. Buổi này góp **6** chế độ hỏng mới, **5** trong 6 nằm ở ô *im lặng + không chặn* — tỉ lệ cao nhất của giai đoạn 1.
- **"Phụ thuộc phiên bản thì phải ĐO, không tra"** — **lần thứ 6**. Hôm nay phải đo **thứ tự chín nấc**, thứ mọi người tưởng chỉ cần tra một trang tài liệu.
- **"Job xanh không chứng minh gì, phải có khẳng định"** — **lần thứ 4**. Hình thức ngắn nhất của cả khoá: **1** dòng `: "${VAR:?}"`, giá **0,01 giây**.

**Ba câu hỏi trung tâm của buổi:**

1. Biến này lấy giá trị từ nấc nào trong chín nấc, và tôi chứng minh điều đó bằng lệnh gì?
2. `masked` và `protected` giải hai bài toán khác nhau nào, và cái nào **không** phải là bảo vệ secret?
3. Vì sao một token đúng từng ký tự vẫn trả về 401, và tôi tìm ra điều đó trong bao nhiêu giây?

**Ba câu BTVN 4 buổi 05 đáp thẳng vào ba mục hôm nay.** Gọi ba học viên đọc phỏng đoán đã ghi, **không sửa ngay**, ghi lên bảng để đối chiếu cuối buổi: câu 1 (mọi chỗ khai được biến, đoán thứ tự) → §4 QT 4.1 và lab bước 1 **đo** tám cặp; câu 2 (`dotenv` nằm nấc nào, có ghi đè project variable không) → §4 QT 4.3; câu 3 (một ca thật "biến không có giá trị đúng" của chính học viên) → §7 và lab bước 2, dùng làm **ca thứ sáu** của lớp.

---



| # | Làm được gì | Hiện vật chứng minh |
|---|---|---|
| LĐ1 | Trả lời "biến này thắng ở nấc nào" cho một biến bất kỳ, không tra tài liệu | `bang-9-nguon-bien.tsv` — 8 cặp nấc tự đo, lab bước 1 |
| LĐ2 | Chẩn đoán ca "sửa YAML mà không có tác dụng" trong dưới 2 phút bằng **1** lệnh API | Lab bước 2 CHECKPOINT 4 |
| LĐ3 | Chứng minh biến `masked` **không** được che trong artifact, bằng cách tải về `grep` | Lab bước 3 CHECKPOINT 6 |
| LĐ4 | Biến một job deploy **xanh mà không deploy gì** thành job **đỏ ở dòng đầu** | Lab bước 2 CHECKPOINT 5 |
| LĐ5 | Phân biệt `$VAR` là đường dẫn với `$(cat $VAR)` là nội dung | Lab bước 4 CHECKPOINT 8 |
| LĐ6 | Tìm ra **1** byte thừa của một token dán lỗi, bằng `${#VAR}` và `od -c` | `nam-ca-bien-sai.md` ca 4, lab bước 4 CHECKPOINT 9 |
| LĐ7 | Nói ra số biến xuống được pipeline con theo ba cách khai, kèm số đo | Lab bước 5 CHECKPOINT 11 |
| LĐ8 | Bật `CI_DEBUG_TRACE` cho đúng một job, đo log trước/sau, rồi **xoá log bằng API** | Lab §L8 CHECKPOINT 12 |

---



| Cần biết | Mức yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Bốn đường vào một job; biến là đường thứ tư | **Vận dụng** | buổi 01 QT 5.1 — tiền đề của §4 |
| Tám pha của một job; biến nạp ở pha `prepare_script` | Vận dụng | buổi 01 QT 4.2 |
| Bảng hai thuộc tính hỏng: im lặng/ồn ào × chặn/không chặn | **Vận dụng** | buổi 01 QT 7.1 |
| Khẳng định làm job đỏ khi kết quả sai | **Vận dụng** | buổi 01 QT 7.3 — dùng ở mọi ví dụ §5 |
| `rules` chốt ở `t0`, không đọc được biến sinh lúc chạy | Vận dụng | buổi 04 QT 4.1, QT 4.2 |
| `artifacts:reports:dotenv` và ba giới hạn của nó | Vận dụng | buổi 05 QT 5.4 |
| Mở rộng tham số shell POSIX: `${VAR:-}`, `${VAR:?}`, `${#VAR}` | **Vận dụng** | `man sh` phần Parameter Expansion; 15 phút là đủ |
| Gọi API GitLab bằng `curl`, lọc bằng `jq`; đọc `trace` | **Vận dụng** | buổi 01 QT 4.2, buổi 05 lab B4 (`doc-pha.sh`) |

---



### 3.1. Đối chiếu thuật ngữ

Từ khoá YAML và tên tuỳ chọn trong giao diện **giữ nguyên tiếng Anh**, vì học viên gõ hoặc bấm đúng chữ đó. Khái niệm khác dùng tiếng Việt, kèm tiếng Anh để đi phỏng vấn.

| Tiếng Việt dùng trong bài | Tiếng Anh | Dùng thẳng tiếng Anh trong thân bài? |
|---|---|---|
| biến | variable | **Có** — `variables` |
| nguồn biến · nấc | variable source · precedence level | Việt |
| thứ tự ưu tiên | precedence | Việt |
| biến định trước | predefined variable | **Có** — `CI_*` |
| biến mức project · group · instance | project/group/instance variable | Việt + tên Anh trong ngoặc |
| biến truyền lúc tạo pipeline | pipeline variable | **Có** — pipeline variable |
| che trong log | masked | **Có** — `masked` |
| chỉ cho nhánh được bảo vệ | protected | **Có** — `protected` |
| biến kiểu file | file variable | **Có** — `type: file` |
| mở rộng biến | variable expansion | **Có** — `expand: false` |
| biến sinh từ job trước | dotenv variable | **Có** — `artifacts:reports:dotenv` |
| kế thừa xuống pipeline con | inheritance | **Có** — `inherit:variables` |
| pipeline hạ nguồn | downstream pipeline | Việt |
| ký tự vô hình | invisible character | Việt |
| dấu vết gỡ rối | debug trace | **Có** — `CI_DEBUG_TRACE` |
| rò rỉ | leak | Việt |
| nhánh được bảo vệ | protected branch | Việt |



Câu hỏi sai là *"biến này bằng gì"*. Câu hỏi đúng là *"biến này thắng ở nấc nào"*. Đổi câu hỏi thì mọi ca gỡ lỗi về biến thành một phép tra bảng chín dòng: liệt kê những nấc có khai tên biến đó, lấy nấc cao nhất, xong.

Giá trị đo được: ca "biến không có giá trị đúng" giải bằng cách đọc YAML mất từ nửa buổi tới cả ngày, vì bốn nấc cao nhất không nằm trong repo. Giải bằng bảng chín nấc mất **2** lệnh API và dưới **2** phút. Quay lại ở buổi 09, 11, 22, 29, 37–43 và **44**.

### 3.3. Mô hình tư duy 2: `masked` khác `protected` khác `secret`

Ba chữ này bị dùng lẫn nhau trong mọi cuộc họp, hậu quả là người ta tưởng đã làm bảo mật khi chưa làm gì cả. Mỗi cái một câu: `masked` che **log**; `protected` giới hạn **nhánh và tag**; không cái nào làm giá trị thành secret thật, vì cả hai đều để giá trị nằm nguyên trong cơ sở dữ liệu GitLab và trong môi trường của mọi job thấy được nó.

Secret thật có **vòng đời ngắn** và **sinh lúc chạy** — buổi 29 (Vault, OIDC) mới là chỗ giải bài toán đó. Hôm nay ta học hai cơ chế giảm rủi ro và học **giới hạn** của chúng, vì phần giới hạn mới là phần người ta không biết. Quay lại ở buổi 28, 29, 37–43.

### 3.4. Mô hình tư duy 3: rỗng không phải lỗi

Shell không coi biến thiếu là lỗi; nó thay bằng **chuỗi rỗng** rồi chạy tiếp. `curl -H "PRIVATE-TOKEN: "` hợp lệ; `helm upgrade --namespace ""` hợp lệ; `aws s3 sync dist/ s3:///` hợp lệ về cú pháp. Không có gì đỏ, và có khi không có gì được làm.

Vậy mọi biến mà thiếu nó thì job **sai** chứ không **đỏ** đều phải có khẳng định ở dòng đầu `script`. Dạng ngắn nhất là `: "${VAR:?thiếu VAR}"` — dấu hai chấm là lệnh rỗng của POSIX shell, chỉ buộc shell mở rộng tham số; `:?` làm shell in thông báo rồi thoát khác 0. Giá **0,01 giây**. Quay lại ở buổi 07, 29, 36, 38–43.

---

### 1.1. Chín nguồn biến và một bảng thứ tự (11 phút)

Cột quan trọng nhất của bảng dưới là cột cuối: **có thấy trong git không**. Bốn nấc trên cùng đều "không", và đó là toàn bộ nguyên nhân của lớp lỗi này.

| Nấc | Nguồn | Khai ở đâu | Ai đổi được | Thấy trong git? |
|---|---|---|---|---|
| 1 | pipeline variable | Bấm "Run pipeline", schedule, `trigger`, API `POST /projects/:id/pipeline` | Người bấm chạy, người đặt schedule | **Không** |
| 2 | project variable | Settings > CI/CD > Variables | Maintainer của project | **Không** |
| 3 | group variable | Settings của group | Owner của group | **Không** |
| 4 | instance variable | Admin Area | Admin instance | **Không** |
| 5 | `dotenv` job trước | `artifacts:reports:dotenv` | Giá trị sinh lúc chạy | Nửa — thấy cơ chế, không thấy giá trị |
| 6 | `variables` cấp job | `.gitlab-ci.yml` | Ai gửi được merge request | Có |
| 7 | `variables` cấp trên cùng | `.gitlab-ci.yml` | Ai gửi được merge request | Có |
| 8 | deployment variable | Tích hợp môi trường | Người cấu hình tích hợp | **Không** |
| 9 | predefined `CI_*` | Nền tảng sinh ra | Không ai — nhưng **ghi đè được** | Không, nhưng tra được tên |

**Nguyên lý cốt lõi:** Biến đến từ **chín** nguồn, và thứ tự ưu tiên giữa chúng do **nền tảng** quyết định, không do tệp YAML. Hệ quả thực dụng: giá trị thật của một biến **không** đọc được bằng cách đọc `.gitlab-ci.yml` — chỉ đọc được bằng cách in nó ra trong job.

**Giải thích cơ chế ngầm:** Bốn nấc cao nhất — pipeline variable, project, group, instance — nằm **ngoài** repo, nên người chỉ có quyền đọc mã nguồn không thấy chúng dù đọc kỹ tới đâu. Việc hợp nhất chín nguồn xảy ra trên server lúc tạo job; runner nhận về một tập biến đã dẹp phẳng và **không** biết mỗi biến đến từ nấc nào. Đó là lý do không có lệnh nào in ra "nấc": ta chỉ suy ra nấc bằng cách so cặp.

**Phần thứ tự giữa các nấc là loại (c) — phải đo, không tra.** Sơ đồ chín nấc ở §0.2 là thứ tự tham chiếu của GitLab CE 17.7; bài giảng này **không** kết luận nó đúng trên hệ thống của học viên. Lab bước 1 khai cùng một tên biến ở hai nấc kề nhau, chạy job in giá trị, lặp cho **8** cặp. Riêng "có chín nhóm nguồn" là loại (a) — và ngay cả nó có bẫy: nhóm 1 gộp **bốn** cách truyền (trigger, schedule, bấm tay, API) không hoàn toàn như nhau.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hai người đọc cùng một tệp YAML và kết luận khác nhau về giá trị một biến — cả hai đều đọc đúng, vì cả hai đều thiếu bốn nấc trên. Hoặc: sửa YAML rồi push mà giá trị không đổi.

**Minh hoạ.**

```yaml
# Job chẩn đoán nấc: in giá trị thật, ghi cạnh nó nấc PHỎNG ĐOÁN của mình, rồi
# đối chiếu với bảng đo ở lab bước 1. Dán vào bất kỳ pipeline nào.
variables:
  MOI_TRUONG: "yaml-tren-cung"      # nấc 7

soi-bien:
  image: alpine:3.20
  variables:
    VUNG: "yaml-cap-job"            # nấc 6
  script:
    - |
      for v in MOI_TRUONG VUNG PHIEN_BAN TOKEN CI_COMMIT_REF_NAME; do
        eval "gt=\${$v-<KHONG CO>}"; printf '%-20s %-24s nac=?\n' "$v" "$gt"
      done
```

**Con số chốt.** **9** nấc; **4** nấc cao nhất nằm ngoài repo — hai con số này là câu chốt phỏng vấn số 1.

**Nguyên lý cốt lõi:** Biến khai trong `.gitlab-ci.yml` nằm ở **nấc thấp** (nấc 6 và 7), nên project/group/instance variable **ghi đè** nó. Đây là nguyên nhân số một của câu "tôi sửa YAML mà không có tác dụng gì".

**Giải thích cơ chế ngầm:** Nền tảng cố ý xếp cấu hình vận hành **trên** cấu hình trong repo, để đội vận hành đổi được giá trị mà không cần merge request — đổi một biến ở Settings mất 10 giây, một merge request mất vài giờ tới vài ngày. Thiết kế đó hợp lý cho người vận hành và là cái bẫy hoàn hảo cho người viết YAML: hai bên nhìn hai nguồn sự thật khác nhau mà không ai sai. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> `git log -p .gitlab-ci.yml` cho thấy giá trị đã đổi ba lần, còn job vẫn in giá trị cũ — và giá trị cũ đó **không** tồn tại ở bất cứ đâu trong repo, kể cả trong lịch sử git, vì nó chưa bao giờ ở trong repo.

**Minh hoạ.**

```bash
# Chẩn đoán ca "sửa YAML không tác dụng" — dưới 2 phút. Nấc 3: đổi projects -> groups/:id
grep -nE '^[[:space:]]{2,}[A-Z_][A-Z0-9_]*:' .gitlab-ci.yml \
  | awk -F: '{print $2}' | tr -d ' ' | sort -u > /tmp/yaml.txt

curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/variables?per_page=100" | jq -r '.[].key' | sort -u > /tmp/project.txt

# Giao của hai tập = danh sách quả bom hẹn giờ. Mỗi dòng ở đây, nấc 2 THẮNG nấc 7.
comm -12 /tmp/yaml.txt /tmp/project.txt
```

**Con số chốt.** Nấc **2** thắng nấc **7**; **1** lần xoá project variable đủ để YAML có tác dụng lại. Số dòng lệnh `comm` in ra là chỉ số phải đưa về **0** — xem §8.

**Nguyên lý cốt lõi:** Biến `dotenv` (nấc 5) chỉ tới được job **sau** và chỉ khi có quan hệ `needs`/`dependencies`; nó **không** dùng được trong `rules` (buổi 04 QT 4.2 — lần thứ 2), và nó **không** ghi đè được project variable cùng tên.

**Giải thích cơ chế ngầm:** Suy từ cơ chế, loại (b), và cơ chế gồm hai nửa độc lập. Nửa thứ nhất là **vị trí**: nấc 5 nằm dưới nấc 2, nên khi hai bên cùng khai một tên thì nấc 2 thắng — không có ngoại lệ cho việc "biến này mới sinh ra nên phải mới hơn". Nửa thứ hai là **thời điểm**: `rules` được đánh giá ở `t0` lúc tạo pipeline (buổi 04 QT 4.1), còn biến `dotenv` chỉ tồn tại sau khi job nguồn chạy xong. Không phải GitLab từ chối; lúc `rules` cần giá trị thì giá trị chưa được sinh ra.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job trước in `PHIEN_BAN=1.4.2` rõ ràng trong log, job sau in một giá trị khác. Đây là ca dễ mất nhiều giờ nhất của §4, vì cả hai giá trị đều **có thật** và đều đúng ở nấc của nó — người gỡ lỗi không biết mình đang so hai nấc.

**Minh hoạ.**

```yaml
# Kiểm chứng nấc 5: chạy hai lần — lần 2 sau khi đặt project variable PHIEN_BAN=9.9.9
stages: [chuan-bi, dung]

sinh-bien:
  stage: chuan-bi
  image: alpine:3.20
  script:
    - echo "PHIEN_BAN=1.4.2" > bien.env
    - cat bien.env
  artifacts:
    reports:
      dotenv: bien.env

dung-bien:
  stage: dung
  image: alpine:3.20
  needs: ["sinh-bien"]              # thiếu dòng này thì biến KHÔNG tới
  script:
    - 'echo "job sau thấy PHIEN_BAN = [$PHIEN_BAN]"'
    # Lần 1 in 1.4.2 (nấc 5). Lần 2 in 9.9.9 (nấc 2 thắng nấc 5).
```

**Con số chốt.** Nấc **5**; **1** project variable cùng tên đủ vô hiệu hoá toàn bộ cơ chế `dotenv` cho biến đó. Vì vậy biến `dotenv` nên có tiền tố riêng, ví dụ `OUT_PHIEN_BAN`, để không đụng vùng tên của nấc 2.

**Nguyên lý cốt lõi:** `variables` cấp **job** ghi đè `variables` cấp **trên cùng** theo kiểu **thay thế từng khoá**, không phải trộn cả khối — và đây là chỗ biến **không** theo quy tắc ba nấc của `image`/`cache` (buổi 03 QT 7.1, lần thứ 2).

**Giải thích cơ chế ngầm:** Hai khối `variables` là hai từ điển, nền tảng hợp nhất theo **tên biến**: khoá có ở cả hai thì bản cấp job thắng, khoá chỉ có ở cấp trên cùng thì còn nguyên. Khác hẳn `image` hay `cache` — những khoá đó là **một giá trị**, khai lại ở cấp job là thay cả cụm. Loại (a). Chỗ hay nhầm: `inherit:variables: false` **tắt hẳn** việc kế thừa nấc 7, và khi đó "còn nguyên hai biến kia" không còn đúng — đó là công tắc, không phải mặc định.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Có người chép cả khối `variables` từ cấp trên cùng xuống cấp job "cho chắc", bỏ sót một biến, và biến đó thành rỗng ở **đúng một** job. Triệu chứng: 7 job cùng loại chạy đúng, 1 job sai, YAML nhìn qua thì giống nhau.

**Minh hoạ.**

```yaml
variables:
  DANG_KY: "jfrog.lab/ntkgitlab"
  MOI_TRUONG: "dev"
  MUC_LOG: "info"

.in-ba: &in-ba
  image: alpine:3.20
  script:
    - 'echo "DANG_KY=[$DANG_KY] MOI_TRUONG=[$MOI_TRUONG] MUC_LOG=[$MUC_LOG]"'

in-ba-bien:
  <<: *in-ba
  variables:
    MOI_TRUONG: "staging"           # khai lại ĐÚNG 1 biến -> vẫn thấy đủ 3 biến

in-ba-bien-tat-ke-thua:
  <<: *in-ba
  inherit:
    variables: false                # công tắc: KHÔNG nhận gì từ nấc 7 -> chỉ còn 1
  variables:
    MOI_TRUONG: "staging"
```

**Con số chốt.** **1** biến bị ghi đè, **2** biến còn nguyên ở job thứ nhất; job thứ hai chỉ còn **1** trong ba. Chi phí hai job chẩn đoán trên: khoảng **6** giây runner.

---

### 1.2. `masked` và `protected`: hai cơ chế, hai bài toán (9 phút)

Hai ô tick nằm cạnh nhau trong cùng một biểu mẫu, nên người ta tưởng chúng là hai mức của cùng một thứ. Không phải — bảng dưới là bảng cần thuộc trước khi vào quy tắc.

| | `masked` | `protected` |
|---|---|---|
| Giải bài toán gì | Giá trị **hiện trong log** | Giá trị **có mặt trong job** ở nhánh không đáng tin |
| Cơ chế | Thay thế chuỗi trên đường log runner → server | Nền tảng **không gửi** biến nếu ref không được bảo vệ |
| Còn lộ ở đâu | Artifact, giá trị bị biến đổi, giao diện | Nhánh được bảo vệ vẫn thấy đủ giá trị |
| Có phải bảo vệ secret không | **Không** | **Không** — là kiểm soát truy cập theo ref |

**Nguyên lý cốt lõi:** `masked` che giá trị **trong log job**, và chỉ thế. Nó **không** che trong artifact, **không** che khi giá trị bị biến đổi trước khi in (base64, đảo chuỗi, chèn ký tự), và **không** giới hạn ai đọc được nó trong giao diện.

**Giải thích cơ chế ngầm:** Cơ chế là **thay thế chuỗi**: runner giữ danh sách giá trị cần che, khi đẩy log về server thì tìm đúng chuỗi đó và thay bằng `[MASKED]`. Ba hệ quả rơi ra từ một câu đó. Thứ gì **không đi qua đường log** thì không được thay — artifact lên server dưới dạng tệp nén, đường khác. Thứ gì **không còn giống chuỗi gốc** thì không khớp — `base64` của một token là chuỗi khác hoàn toàn. Và việc che xảy ra **sau khi** giá trị đã có đủ trong môi trường job và trong cơ sở dữ liệu GitLab.

**Ba đường lộ này là loại (c) — phải đo.** Đừng tin ba câu trên vì bài giảng nói vậy: lab bước 3 in một biến masked theo ba đường, tải artifact về bằng API rồi `grep` giá trị gốc, ghi kết quả kèm số phiên bản. Hành vi masking đã được siết dần qua các bản 15.x–17.x.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Log hiện `[MASKED]` nên cả đội yên tâm, trong khi cùng giá trị đó nằm nguyên văn trong một artifact `.env` mà bất cứ ai đọc được project đều tải về bằng một lệnh `curl`. Dấu hiệu phụ: có người dán `echo $TOKEN | base64` vào script "để gỡ lỗi cho an toàn".

**Minh hoạ.**

```yaml
# Ba đường: 1 bị che, 2 KHÔNG bị che. Đặt TOKEN là project variable có masked.
lo-ba-duong:
  image: alpine:3.20
  script:
    - 'echo "duong 1 truc tiep: $TOKEN"'          # log hiện [MASKED]
    - 'echo -n "$TOKEN" | base64'                  # log hiện base64 — KHÔNG che
    - 'echo "TOKEN=$TOKEN" > ro-ri.env'            # vào artifact — KHÔNG che
  artifacts:
    paths: [ro-ri.env]
```

```bash
# Chứng minh bằng hiện vật, không bằng mắt: tải artifact về rồi grep giá trị gốc
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB_ID/artifacts/ro-ri.env" | grep -c "$TOKEN_THAT"   # -> 1
```

**Con số chốt.** **1** cơ chế thay thế chuỗi; **3** đường lộ nó không bịt. Đây là câu chốt phỏng vấn số 3 và là một trong hai quy tắc trần điểm ở vấn đáp.

> **Nếu có Ultimate:** Secret Detection quét được secret bị commit vào repo, và `secrets:` với HashiCorp Vault hoặc Azure Key Vault là tính năng Premium/Ultimate. Cả hai giảm số ca rò rỉ nhưng **không** đổi gì trong QT 5.1: `masked` vẫn là thay thế chuỗi và vẫn không che artifact. Lab hôm nay chạy trên GitLab CE, không dùng tới hai thứ đó; đường OSS tương đương là Gitleaks, dựng ở buổi 30.

**Nguyên lý cốt lõi:** `protected` là **kiểm soát truy cập theo nhánh và tag**: pipeline chạy trên nhánh không được bảo vệ thì biến **không tồn tại** — cho ra chuỗi **rỗng**, không cho ra lỗi. Đây là chế độ hỏng im lặng số một của buổi.

**Giải thích cơ chế ngầm:** Nền tảng đơn giản là **không gửi** biến đó cho job. Runner nhận về một tập biến không có tên ấy và không có gì để báo thiếu, vì nó không biết đáng ra phải có — trong giao thức giữa server và runner không tồn tại khái niệm "biến bị từ chối", chỉ có "có tên đó" và "không có tên đó". Sang tới shell, biến chưa đặt được thay bằng chuỗi rỗng. Loại (a), cộng với mô hình tư duy 3.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job deploy trên nhánh feature **xanh** mà không có gì được deploy. Hoặc `curl` đi tới đúng địa chỉ với header `PRIVATE-TOKEN:` rỗng và nhận 401 ở một chỗ cách xa nguyên nhân — người gỡ lỗi đi kiểm quyền token, hạn dùng, firewall, trong khi token chưa bao giờ có mặt.

**Minh hoạ.**

```yaml
# Hai job đối chứng. Chạy trên nhánh mặc định rồi chạy lại trên nhánh feature.
deploy-khong-khang-dinh:
  image: alpine:3.20
  script:
    - 'echo "do dai TOKEN = ${#TOKEN}"'          # nhánh bảo vệ: 20 · nhánh feature: 0
    - apk add --no-cache curl >/dev/null
    - curl -sS -o /dev/null -w 'HTTP %{http_code}\n' --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/user" || true
    # XANH trên cả hai nhánh. Ô im lặng + không chặn.

deploy-co-khang-dinh:
  image: alpine:3.20
  script:
    - ': "${TOKEN:?thiếu TOKEN — nhánh này chưa được bảo vệ}"'
    - 'echo "do dai TOKEN = ${#TOKEN}"'
    # ĐỎ ngay dòng đầu trên nhánh feature. Đó là kết quả ĐÚNG.
```

**Con số chốt.** Độ dài **0** thay vì một lỗi; **1** dòng `${VAR:?}` đổi ô bảng hai thuộc tính từ *im lặng không chặn* sang *ồn ào có chặn*, giá **0,01 giây**. Lần thứ **4** khoá này nói "job xanh không chứng minh gì".

**Nguyên lý cốt lõi:** Bật được `masked` là một ràng buộc lên **giá trị**, không lên ý muốn: giá trị phải một dòng, không khoảng trắng, và đủ dài. Secret không thoả điều kiện thì phải **đổi secret**, không phải bỏ `masked`.

**Giải thích cơ chế ngầm:** Cơ chế thay thế chuỗi cần một chuỗi **ổn định và phân biệt được**. Giá trị 3 ký tự như `abc` xuất hiện bên trong hàng trăm chuỗi khác trong log, che nó thì băm nát log; giá trị có khoảng trắng hoặc nhiều dòng bị các lớp xử lý log tách ra, nên tới chỗ so khớp không còn nguyên chuỗi. Vì vậy nền tảng từ chối bật `masked` thay vì bật rồi che sai. Loại (a), ràng buộc cụ thể phụ thuộc phiên bản.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Giao diện từ chối bật `masked` kèm thông báo về định dạng, người ta bỏ ô tick rồi đi tiếp. Từ hôm ấy mọi log của mọi job có biến đó đều chứa secret nguyên văn, và không có tín hiệu nào — không cảnh báo, không job đỏ, không dòng log nào khác thường.

**Minh hoạ.**

```bash
# Ba giá trị, hai cái đầu API PHẢI từ chối. Đây là ca đối chứng bắt buộc thất bại.
for v in "abc" "mot hai ba" "$(head -c16 /dev/urandom | od -An -tx1 | tr -d ' \n')"; do
  code=$(curl -s -o /tmp/kq.json -w '%{http_code}' --request POST \
    --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID/variables" \
    --form "key=THU_MASKED" --form "value=$v" --form "masked=true")
  printf '%-34s -> HTTP %s %s\n' "[$v]" "$code" "$(jq -rc '.message // empty' /tmp/kq.json)"
  [ "$code" = "201" ] && curl -sf --request DELETE --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/variables/THU_MASKED" >/dev/null
done
```

**Con số chốt.** Tối thiểu **8** ký tự, **1** dòng, **0** khoảng trắng ở GitLab 17.7. Con số 8 **không phổ quát** — nó đã đổi nhiều lần trong dòng 15.x–17.x, nên sang instance khác thì đo lại bằng đúng đoạn lệnh trên, đừng chép con số này vào tài liệu nội bộ.

---

### 1.3. Biến kiểu file, ký tự vô hình, và việc mở rộng biến (9 phút)

Ba mục của §6 là một họ: cả ba đều là ca "giá trị tới nơi không phải giá trị tôi đặt" — QT 6.1 tới nơi là đường dẫn thay vì nội dung, QT 6.2 dài hơn 1 byte, QT 6.3 ngắn đi 2 ký tự. Cả ba đều không sinh ra dòng log nào có chữ "lỗi".

**Nguyên lý cốt lõi:** Biến `type: file` làm runner ghi giá trị ra một **tệp tạm** và đặt **đường dẫn tệp** vào biến. Vậy `$VAR` là đường dẫn, còn nội dung ở `$(cat $VAR)` — dùng sai kiểu là lớp lỗi hay gặp nhất khi tích hợp kubeconfig, service account key, hay chứng chỉ.

**Giải thích cơ chế ngầm:** Nhiều công cụ chỉ nhận **đường dẫn**: `KUBECONFIG`, `GOOGLE_APPLICATION_CREDENTIALS`, `AWS_SHARED_CREDENTIALS_FILE`, `--cacert` của `curl`. Trước khi có biến kiểu file, người ta phải tự viết `echo "$KUBECONFIG_B64" | base64 -d > /tmp/kc` ở đầu mỗi job — mỗi lần là một lần có thể quên `chmod`, quên xoá, hoặc để nội dung lọt vào log. Biến kiểu file phục vụ đúng nhóm đó nên cố ý đặt đường dẫn vào biến; runner xoá tệp tạm ở pha dọn dẹp cuối job (`cleanup_file_variables`, buổi 01 QT 4.2). Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hai triệu chứng **đối xứng**, nhận ra cặp này là nhận ra cả lớp lỗi. Dùng biến thường ở chỗ cần tệp: công cụ báo lỗi phân tích cú pháp ở **dòng 1 cột 1**, vì nó vừa `open()` một chuỗi YAML dài như thể đó là tên tệp. Dùng biến file ở chỗ cần nội dung: công cụ báo nội dung là `/builds/<group>/<project>.tmp/KUBECONFIG_FILE` — một dòng trông như đường dẫn, và nó đúng là đường dẫn.

**Minh hoạ.**

```yaml
# KUBECONFIG_FILE khai type: file · KUBECONFIG_TEXT khai kiểu thường, cùng nội dung
so-hai-kieu:
  image: alpine:3.20
  script:
    - 'echo "kieu file, echo -> $KUBECONFIG_FILE"'       # in ra ĐƯỜNG DẪN
    - 'echo "kieu file, wc   -> $(wc -l < "$KUBECONFIG_FILE") dòng nội dung"'
    - kubectl --kubeconfig "$KUBECONFIG_FILE" config current-context   # ĐÚNG
    # Khi chỉ có biến thường: tự ghi ra tệp rồi mới dùng
    - printf %s "$KUBECONFIG_TEXT" > /tmp/kc && chmod 600 /tmp/kc
    - kubectl --kubeconfig /tmp/kc config current-context
```

**Con số chốt.** **2** kiểu biến; **2** triệu chứng đối xứng khi dùng sai chiều; chi phí là **1** tệp tạm mỗi biến và **0** giây thêm.

**Nguyên lý cốt lõi:** Ký tự vô hình cuối giá trị — xuống dòng, khoảng trắng, dấu nháy bị chép vào — là nguyên nhân số một của "token đúng từng ký tự mà vẫn 401". Chẩn đoán bằng `${#VAR}` và `od -c`, **không** bằng mắt và **không** bằng cách so sánh chuỗi trong log đã bị `masked`.

**Giải thích cơ chế ngầm:** Suy từ cơ chế, loại (b), gồm ba chỗ cộng lại. Một: ô nhập trong giao diện là một `textarea`, nó giữ ký tự xuống dòng cuối mà không hiển thị gì khác biệt. Hai: bôi đen bằng chuột trong terminal rất dễ kèm theo một `\n` hoặc khoảng trắng. Ba, và là chỗ mất nhiều giờ nhất: biến có `masked` thì log in `[MASKED]`, che mất đúng chỗ cần nhìn — càng làm đúng bảo mật thì càng khó chẩn đoán bằng mắt. Vì vậy phải đo bằng số byte.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> `${#TOKEN}` cho **21** trong khi token thật dài **20**; hoặc `od -c` hiện `\n` ở byte cuối. Ở tầng ứng dụng: 401 với đúng một token, trong khi cùng token đó dán vào `curl` trên máy cá nhân thì 200 — vì ở đó shell đã cắt khoảng trắng cuối.

**Minh hoạ.**

```yaml
# TOKEN_SACH và TOKEN_BAN cùng giá trị, TOKEN_BAN có thêm 1 ký tự xuống dòng cuối
chan-doan-1-byte:
  image: alpine:3.20
  script:
    - apk add --no-cache curl coreutils >/dev/null
    - 'echo "do dai: sach=${#TOKEN_SACH} ban=${#TOKEN_BAN}"'     # 20 so với 21
    - printf %s "$TOKEN_BAN" | od -c | tail -2                    # thấy \n ở byte cuối
    - |
      for t in TOKEN_SACH TOKEN_BAN; do
        eval "gt=\$$t"
        printf '%-11s -> HTTP %s\n' "$t" \
          "$(curl -s -o /dev/null -w '%{http_code}' --header "PRIVATE-TOKEN: $gt" "$GITLAB/api/v4/user")"
      done
    # TOKEN_SACH -> 200 · TOKEN_BAN -> 401. Chênh nhau đúng 1 byte.
    # Dọn tại chỗ khi chưa sửa được nguồn:
    - 'echo "sau khi don: ${#TOKEN_DON}"' # TOKEN_DON="$(printf %s "$TOKEN_BAN" | tr -d "\r\n")"
```

**Con số chốt.** **1** byte thừa đủ đổi 200 thành 401; `${#VAR}` tốn **0,01 giây**. Đặt cả `${#VAR}` và `od -c` vào đầu job nghi vấn tốn **0,02** giây và cắt được vài giờ đi kiểm quyền token.

**Nguyên lý cốt lõi:** Giá trị biến được **mở rộng**: `$` và `${...}` trong giá trị bị hiểu là tham chiếu tới biến khác. Mật khẩu chứa `$` vì thế bị đổi âm thầm; `expand: false` tắt việc mở rộng cho biến đó.

**Giải thích cơ chế ngầm:** Mở rộng biến là tính năng có ích, dùng khắp nơi: `DUONG_DAN: "$CI_PROJECT_DIR/dist"`, `KHOA_CACHE: "$CI_COMMIT_REF_SLUG-npm"`. Nền tảng không có cách nào biết một giá trị là đường dẫn hay mật khẩu, nên nó mở rộng tất. Với `Pa$$w0rd`, `$$` được đọc là tham chiếu tới một biến rỗng nên tới nơi chỉ còn `Paw0rd`. Công tắc `expand: false` (API: `raw=true`) tắt việc này cho đúng một biến. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Xác thực thất bại với mật khẩu mà người ta chắc chắn là đúng, log không hé ra gì vì `masked` che phần còn lại. Dấu hiệu định lượng nhanh nhất: `${#MAT_KHAU}` ngắn hơn số ký tự đã dán.

**Minh hoạ.**

```yaml
# MK_MO_RONG: khai thường · MK_THO: khai expand: false (API: raw=true). Cùng giá trị Pa$$w0rd
variables:
  MK_THO:
    value: 'Pa$$w0rd'
    expand: false

so-mo-rong:
  image: alpine:3.20
  script:
    - 'echo "MK_MO_RONG do dai=${#MK_MO_RONG}"'      # 6 — đã hụt 2
    - 'echo "MK_THO     do dai=${#MK_THO}"'          # 8 — nguyên vẹn
    - printf %s "$MK_THO" | od -c | head -2
```

```bash
# Tạo biến raw (tương đương expand: false) bằng API — dùng ở lab bước 4
curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/variables" \
  --form 'key=MK_THO' --form 'value=Pa$$w0rd' --form 'raw=true' | jq '{key, raw}'
```

**Con số chốt.** `Pa$$w0rd` dài **8** ký tự, sau khi mở rộng còn **6** — hụt **2**. Số hụt phụ thuộc giá trị cụ thể, nên đừng nhớ số 2; nhớ cách đo là `${#VAR}` so với số ký tự đã dán.

---

### 1.4. Biến xuống downstream pipeline, và `CI_DEBUG_TRACE` (5 phút)

**Nguyên lý cốt lõi:** Pipeline hạ nguồn **không** tự thấy mọi biến của pipeline cha: quy tắc kế thừa do `inherit:variables` điều khiển, và biến khai ở cấp **job** của job `trigger` truyền xuống theo đường riêng so với biến cấp trên cùng. Đây là nền của buổi 09 và buổi 11.

**Giải thích cơ chế ngầm:** Hai pipeline là hai đối tượng riêng trên server, có id riêng và tập biến riêng; truyền biến giữa chúng là **hành động tường minh** của job `trigger`, không phải hệ quả tự nhiên của việc cùng project. Ba chỗ khai đi ba đường: `variables` cấp job của job `trigger` xuống con như pipeline variable của con (nấc 1 ở phía dưới, nên thắng cả YAML của repo con); `variables` cấp trên cùng của cha vào job `trigger` theo kế thừa thường và chịu công tắc `inherit:variables`; pipeline variable của cha chịu `trigger:forward`.

**Đây là loại (c) — phải đo.** Bài giảng **không** kết luận con số cuối cùng: mặc định của `trigger:forward` và cách các đường trên tương tác đã đổi giữa các phiên bản. Lab bước 5 chạy ba ca, cho pipeline con in môi trường rồi đếm, ghi hiện vật kèm số phiên bản.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline con chạy với biến rỗng và **xanh**: cha xanh, con xanh, mũi nối xanh — việc thì không được làm. Đây là chế độ hỏng đắt nhất của §7 vì có hai lớp xanh che nhau, và người điều tra thường bắt đầu từ pipeline cha nơi mọi thứ đều đúng.

**Minh hoạ.**

```yaml
# Pipeline CHA — hai chỗ khai, tên khác nhau để đếm được ở phía con
variables:
  TU_TREN_CUNG: "cha-nac-7"

kich-hoat:
  variables:
    TU_CAP_JOB: "cha-cap-job"        # xuống con như pipeline variable của con
  trigger:
    include: .gitlab-ci-con.yml
    strategy: depend
  # Bỏ chú thích hai dòng dưới rồi chạy lại: đây là phép ĐO của lab bước 5
  # inherit:
  #   variables: false
```

```yaml
# .gitlab-ci-con.yml — pipeline CON đếm chính xác biến nào xuống được
dem-bien:
  image: alpine:3.20
  script:
    - 'echo "TU_TREN_CUNG=[$TU_TREN_CUNG] TU_CAP_JOB=[$TU_CAP_JOB]"'
    - 'echo "so bien khong phai CI_*: $(env | grep -cvE "^CI_")"'
    - ': "${TU_CAP_JOB:?pipeline con KHÔNG nhận được biến — dừng ngay}"'
```

**Con số chốt.** **3** chỗ khai; số biến xuống được **phải đo**, không được đoán. Một dòng `${VAR:?}` trong pipeline con là cách rẻ nhất biến hai lớp xanh thành một job đỏ.

**Nguyên lý cốt lõi:** `CI_DEBUG_TRACE: "true"` in **toàn bộ** môi trường của job vào log — đó là cách nhanh nhất để trả lời "biến này bằng gì và tới từ nấc nào", và cũng là cách nhanh nhất làm lộ mọi secret cho bất cứ ai đọc được log. Chỉ bật trên nhánh riêng, cho **một** job, rồi xoá log.

**Giải thích cơ chế ngầm:** Debug trace bật `set -x` cho script sinh ra của runner và in cả bảng biến trước khi chạy. Vì in **mọi** biến, nó in cả những thứ `masked` không bịt nổi theo đúng QT 5.1: giá trị đã bị biến đổi, đường dẫn và có khi cả nội dung biến kiểu file, và `CI_JOB_TOKEN` — token có quyền thật với API và registry suốt thời gian job chạy. Đó là lý do GitLab yêu cầu quyền cấp cao mới bật được. Loại (a).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Log job phình từ **12 kB** lên hàng trăm kB, trong đó có `CI_JOB_TOKEN` nguyên văn. Tệ hơn: một nhánh có `CI_DEBUG_TRACE: "true"` trong `.gitlab-ci.yml` từ ba tháng trước vì ai đó bật rồi commit luôn — kiểm bằng `git grep -n CI_DEBUG_TRACE $(git rev-list --all | head -200)`.

**Minh hoạ.**

```bash
# 1) Bật cho ĐÚNG một job: truyền biến lúc bấm chạy tay, KHÔNG commit vào YAML
curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipeline?ref=go-roi-bien" \
  --form 'variables[][key]=CI_DEBUG_TRACE' --form 'variables[][value]=true' | jq '{id, ref}'

# 2) Đo kích thước log và đếm số dòng biến
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB_ID/trace" | tee /tmp/trace.txt | wc -c
grep -c '^++ export' /tmp/trace.txt

# 3) BẮT BUỘC: xoá log job sau khi đọc xong
curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB_ID/erase" | jq '{id, erased_at}'
```

**Con số chốt.** Log tăng từ **12 kB** lên khoảng **400 kB**; số biến in ra khoảng **250–400** dòng — bài lab **đo**. Cả hai **không phổ quát**: chúng phụ thuộc số biến của project và số dòng `script`, nên lấy làm bậc độ lớn. Rủi ro lộ secret không quy ra giây được, và đó là lý do §L8 có bước xoá log **bắt buộc**.

---

### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước

Ba việc, tổng **35** phút, xếp theo rủi ro tăng dần; cả ba làm được hôm nay mà không cần xin ai.

**Việc 1 — 10 phút, rủi ro bằng 0.** Liệt kê project và group variable bằng `GET /projects/:id/variables` và `GET /groups/:id/variables`, đối chiếu với danh sách tên biến khai trong `.gitlab-ci.yml`. Mọi tên có ở **cả hai** chỗ là một quả bom hẹn giờ của QT 4.2 — ghi lại, đó là chỉ số đo trước/đo sau thứ nhất. Đoạn `comm -12` ở minh hoạ QT 4.2 làm đúng việc này.

**Việc 2 — 15 phút, rủi ro thấp.** Với mọi biến mà thiếu nó thì job **sai** chứ không **đỏ**, thêm `: "${VAR:?thiếu VAR}"` vào dòng đầu `script`. Tiêu chí chọn: biến đi vào lệnh có tác dụng phụ ra bên ngoài — deploy, push image, gọi API, xoá — thì phải có khẳng định; biến chỉ dùng cho log hay tên tệp thì không cần.

**Việc 3 — 10 phút, rủi ro thấp.** Kiểm mọi biến chứa token xem `masked` đã bật chưa và `protected` có đúng ý định chưa. Cột `protected` phải đối chiếu với **danh sách nhánh được bảo vệ** lấy từ `GET /projects/:id/protected_branches`, không đối chiếu với trí nhớ — trí nhớ về danh sách đó gần như luôn sai ở repo có tuổi.

### Cái gì hỏng nếu áp thẳng lên prod

Bật `protected` cho một biến đang dùng ở nhánh feature làm **mọi** pipeline nhánh feature mất biến đó ngay lập tức — và chúng **xanh** chứ không đỏ, nên không ai báo: thao tác "siết bảo mật" này tạo ra đúng chế độ hỏng số một của buổi, trên diện rộng. Làm ngược lại cũng hỏng: thêm `${VAR:?}` cho một biến vốn **được phép** rỗng ở một môi trường sẽ làm job đỏ đúng lúc phát hành, tức lúc đắt nhất.

Cách áp thử an toàn cho cả hai chiều: chạy khẳng định ở chế độ ồn ào **nhưng không chặn** một tuần, đọc số, rồi mới chuyển thành khẳng định thật.

```yaml
# Chạy song song job thật, KHÔNG chặn ai, trong 1 tuần — ô ồn ào + không chặn của QT 7.1
kiem-bien-thu:
  stage: kiem-tra
  image: alpine:3.20
  allow_failure: true
  script:
    - ': "${TOKEN_DEPLOY:?}"'
    - ': "${MOI_TRUONG:?}"'
    - ': "${DANG_KY:?}"'
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

Sau một tuần, đếm số lần `kiem-bien-thu` đỏ — đó chính là số ca "job xanh mà biến rỗng" đang tồn tại. Khi nó về 0, bỏ `allow_failure` và chuyển các dòng khẳng định vào job thật.

### Đo trước — đo sau

| Chỉ số | Đo bằng | Mục tiêu |
|---|---|---|
| Số tên biến trùng giữa YAML và project/group variable | `comm -12` ở minh hoạ QT 4.2, chạy mỗi tuần | Về **0** |
| Số biến quan trọng đã có khẳng định `${VAR:?}` trên tổng số | `grep -c ':?' .gitlab-ci.yml` so với danh sách Việc 2 | Tỉ số về **1** |
| Số job từng chạy với biến rỗng trong 30 ngày | Đếm số lần `kiem-bien-thu` đỏ sau 1 tuần rồi ngoại suy | Về **0** trước khi bỏ `allow_failure` |

### Khi nào KHÔNG nên dùng

**Đừng** coi `masked` là bảo vệ secret. Nó là **1** cơ chế thay thế chuỗi trên đường log, và QT 5.1 chỉ ra **3** đường lộ nó không bịt. Khi một secret rò rỉ, hậu quả không phụ thuộc chút nào vào việc nó có `masked` hay không — cái phụ thuộc là secret sống bao lâu và có quyền gì. Secret thật cần vòng đời ngắn, sinh lúc chạy: buổi 29 (Vault, OIDC) mới là chỗ giải bài toán đó; trước buổi 29 thì cách giảm rủi ro tốt nhất là giảm **số** secret dài hạn, không phải tick thêm ô.

**Đừng** dùng project variable để cấu hình thứ thuộc về mã nguồn: tên image, phiên bản công cụ, tên thư mục build, cờ tính năng. Nó tạo trạng thái vô hình với `git log` — không lịch sử, không review, không rollback theo commit — và một hôm sẽ có người sửa YAML cả buổi mà không hiểu vì sao vô ích. Nấc 2 dành cho thứ khác nhau giữa các môi trường: địa chỉ đích, token, tên namespace.

**Đừng** bật `CI_DEBUG_TRACE` trên nhánh mặc định hay trên project có người ngoài đội đọc được log — kể cả một lần, kể cả "chỉ 5 phút", vì log còn đó tới khi có người xoá và không có gì nhắc ai xoá. Và đừng commit nó vào YAML: bật bằng biến lúc bấm chạy tay như minh hoạ QT 7.2 thì nó tự hết hiệu lực sau một pipeline.

**Buổi này KHÔNG giải quyết** ba việc: không làm secret an toàn (buổi 29), không cho cách lưu tệp secret có kiểm soát phiên bản (buổi 29), và không trả lời "ai đã đọc biến này" — cần audit event, buổi 45.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy | Vì sao dính | Làm đúng là |
|---|---|---|---|
| 1 | Đọc YAML để biết giá trị biến | YAML là thứ duy nhất thấy được trong repo | Hỏi "thắng ở nấc nào": **9** nấc, **4** nấc ngoài repo; in giá trị trong job (QT 4.1) |
| 2 | Sửa YAML mãi không tác dụng | Không biết có nấc nào trên nấc 7 | Nấc **2** thắng nấc **7**; đối chiếu API rồi xoá project variable (QT 4.2) |
| 3 | Dùng biến `dotenv` trong `rules` | Tưởng biến nào cũng dùng ở mọi chỗ | Quá muộn — nấc 5 sinh lúc chạy, `rules` chạy ở `t0` (QT 4.3) |
| 4 | Chép cả khối `variables` xuống cấp job | Tưởng khai lại một biến thì mất cả khối | Hợp nhất theo **tên biến**; chỉ khai lại biến cần đổi (QT 4.4) |
| 5 | Tin `masked` bảo vệ được secret | Chữ "masked" nghe như đã che kín | **1** cơ chế thay thế chuỗi, **3** đường lộ nó không bịt (QT 5.1) |
| 6 | Ghi biến secret vào artifact | Thấy log có `[MASKED]` nên yên tâm | Artifact **không** được `masked`; tải về `grep` là ra (QT 5.1) |
| 7 | Tưởng biến protected thiếu thì job đỏ | Thiếu thứ cần thì phải lỗi — trực giác sai | Cho ra độ dài **0**, không cho ra lỗi (QT 5.2) |
| 8 | Không có khẳng định cho biến quan trọng | Chưa từng gặp ca deploy xanh mà rỗng | **1** dòng `: "${VAR:?}"`, tốn **0,01** giây (QT 5.2) |
| 9 | Bỏ `masked` vì giá trị không thoả | Giao diện chặn, tìm đường đi tiếp nhanh nhất | Đổi **secret**, không bỏ `masked`; cần ≥ **8** ký tự, **1** dòng (QT 5.3) |
| 10 | Dùng `$VAR` của biến file như nội dung | Không biết có hai kiểu biến | `$VAR` là **đường dẫn**; nội dung ở `$(cat $VAR)` (QT 6.1) |
| 11 | So token bằng mắt trong log | Log bị `masked` nên không so được thật | `${#VAR}` và `od -c`; **1** byte thừa đủ gây 401 (QT 6.2) |
| 12 | Mật khẩu có `$` | Không biết giá trị biến bị mở rộng | Bị mở rộng: **8** ký tự còn **6**; dùng `expand: false` (QT 6.3) |
| 13 | Tưởng pipeline con thấy mọi biến của cha | Cùng project nên tưởng cùng môi trường | `inherit:variables` và `trigger:forward` quyết định; **phải đo** (QT 7.1) |
| 14 | Bật `CI_DEBUG_TRACE` rồi để đó | Bật lúc gấp, xong việc thì quên | Log **12 kB → 400 kB** kèm `CI_JOB_TOKEN` nguyên văn; xoá log bằng API (QT 7.2) |

---

### 1.7. Tóm tắt

```mermaid
graph TD
    LD["LUẬN ĐỀ: biến đến từ CHÍN nguồn<br/>thứ tự ưu tiên là thuộc tính của NỀN TẢNG<br/>không đọc giá trị bằng cách đọc YAML"]

    LD --> N["§4 CHÍN NẤC<br/>QT 4.1 bốn nấc ngoài repo — thứ tự PHẢI ĐO<br/>QT 4.2 nấc 2 thắng nấc 7<br/>QT 4.3 dotenv là nấc 5, không vào rules<br/>QT 4.4 hợp nhất theo tên biến"]
    LD --> M["§5 MASKED và PROTECTED<br/>QT 5.1 masked che log, 3 đường lộ — PHẢI ĐO<br/>QT 5.2 protected thiếu cho ra RỖNG<br/>QT 5.3 điều kiện bật masked ràng buộc lên giá trị"]
    LD --> G["§6 GIÁ TRỊ TỚI NƠI KHÔNG NHƯ ĐẶT<br/>QT 6.1 type: file — VAR là đường dẫn<br/>QT 6.2 1 byte thừa đổi 200 thành 401<br/>QT 6.3 mở rộng biến: 8 ký tự còn 6"]

    N --> D["§7 XUỐNG PIPELINE CON<br/>QT 7.1 ba chỗ khai — số xuống được PHẢI ĐO<br/>QT 7.2 CI_DEBUG_TRACE: 12 kB → 400 kB"]
    M --> D
    G --> D

    D --> KQ["Ô NGUY HIỂM NHẤT — lần thứ 6:<br/>im lặng + không chặn<br/>5 trong 6 chế độ hỏng nằm ở đây"]
    KQ --> VT["§8 ĐƯA VÀO VIỆC THẬT<br/>comm -12 giữa YAML và API → về 0<br/>khẳng định VAR:? giá 0,01 s<br/>áp thử qua allow_failure 1 tuần"]

    N -.dùng lại.-> B1["buổi 09 · 11 · 22 · 44"]
    M -.dùng lại.-> B2["buổi 28 · 29 Vault/OIDC · 45"]
    G -.dùng lại.-> B3["buổi 39 · 41 kubeconfig · 42"]
    D -.dùng lại.-> B4["buổi 07 gỡ rối · 09"]
```

**Năm điều phải nhớ sau buổi học:**

1. **Chín nấc, cao ghi đè thấp, bốn nấc cao nhất ngoài repo.** Đừng hỏi "biến bằng gì", hỏi "biến thắng ở nấc nào".
2. **Nấc 2 thắng nấc 7.** Đó là toàn bộ ca "sửa YAML mà không có tác dụng"; **1** lệnh API tìm ra nó trong dưới 2 phút.
3. **`masked` là thay thế chuỗi trên đường log, không phải bảo vệ secret.** **3** đường nó không bịt: artifact, giá trị bị biến đổi, giao diện.
4. **Rỗng không phải lỗi.** `protected` thiếu cho ra `${#TOKEN}` = **0** và job **xanh**; **1** dòng `: "${VAR:?}"` giá **0,01 giây** đổi ô của bảng.
5. **Thứ tự nấc và số biến xuống pipeline con phải ĐO** — lần thứ **6** khoá này nói câu đó. Sơ đồ trong bài là điểm khởi đầu, không phải kết luận.

---

### 1.8. Câu hỏi tự kiểm tra

1. Kể chín nguồn biến theo thứ tự ưu tiên từ cao xuống thấp. Bốn nguồn nào **không** nhìn thấy được trong repo?
2. Một biến khai `MOI_TRUONG: "dev"` ở cấp trên cùng, job in ra `prod`. Nêu hai nấc có thể đang thắng và **một** lệnh phân biệt chúng.
3. Job A xuất `PHIEN_BAN=1.4.2` qua `dotenv`, project variable có `PHIEN_BAN=9.9.9`. Job B có `needs: [A]` in ra gì? Và vì sao `PHIEN_BAN` không dùng được trong `rules`?
4. Cấp trên cùng khai ba biến, job khai lại một biến. Job thấy mấy biến? Thêm `inherit:variables: false` thì thấy mấy biến?
5. `masked` che ở đâu và **không** che ở đâu? Kể đủ ba đường lộ.
6. Điều kiện bật được `masked` ở GitLab 17.7 là gì? Secret không thoả thì làm gì, và **không** được làm gì?
7. Một biến `protected` dùng trong job deploy, pipeline chạy trên nhánh feature. `${#TOKEN}` bằng bao nhiêu, job xanh hay đỏ, đó là ô nào của bảng hai thuộc tính, và **một** dòng nào đổi được ô đó?
8. Biến `KUBECONFIG_FILE` khai `type: file`. `echo "$KUBECONFIG_FILE"` in ra gì? Nêu hai triệu chứng đối xứng khi dùng sai kiểu theo hai chiều.
9. Một token dán vào giao diện: `curl` trong job trả 401, trên máy cá nhân trả 200. Nêu **hai** lệnh chẩn đoán và con số kỳ vọng của chúng.
10. Mật khẩu `Pa$$w0rd` khai ở `variables` thường thì tới nơi còn mấy ký tự? Vì sao, và tắt bằng gì?
11. Pipeline cha có `variables` cấp trên cùng và `variables` cấp job của job `trigger`. Cái nào xuống được pipeline con, và vì sao bài giảng nói "phải đo"?
12. `CI_DEBUG_TRACE: "true"` làm log tăng từ bao nhiêu lên bao nhiêu? Kể **hai** thứ nó in ra mà `masked` không che nổi.

### Đáp án

1. pipeline variable → project → group → instance → `dotenv` job trước → `variables` cấp job → `variables` cấp trên cùng → deployment variable → predefined `CI_*`. Bốn nguồn không thấy trong repo: pipeline variable, project, group, instance. Thứ tự này là tham chiếu của 17.7, loại (c), phải đo lại từng cặp (QT 4.1).
2. Nấc 2 (project variable) hoặc nấc 1 (pipeline variable từ lúc bấm chạy hay từ schedule). Lệnh phân biệt: `GET /projects/:id/variables` rồi `jq -r '.[].key'` — có `MOI_TRUONG` thì là nấc 2; không có thì xem `GET /projects/:id/pipelines/:pipeline_id/variables` (QT 4.2).
3. In `9.9.9`: `dotenv` là nấc 5, project variable là nấc 2, nấc cao thắng — cả hai giá trị đều có thật, đó là lý do ca này khó gỡ. Không dùng được trong `rules` vì `rules` đánh giá **1** lần ở `t0`, còn biến `dotenv` chỉ tồn tại sau khi job nguồn chạy xong (QT 4.3, buổi 04 QT 4.2 — lần 2).
4. Thấy **3** biến: 1 bị ghi đè, 2 còn nguyên, vì hợp nhất theo tên biến. Với `inherit:variables: false` chỉ còn **1** biến khai ở cấp job (QT 4.4).
5. Che trong **log job**. Không che: giá trị trong **artifact**; giá trị đã **bị biến đổi** trước khi in (base64, đảo chuỗi); và không giới hạn ai **đọc được trong giao diện**. Cơ chế là thay thế chuỗi trên đường log, nên cái gì không đi đường đó hoặc không còn giống chuỗi gốc thì không được thay (QT 5.1).
6. Giá trị phải **1** dòng, **0** khoảng trắng, tối thiểu **8** ký tự ở 17.7. Không thoả thì **đổi secret**; **không** được bỏ `masked` để đi tiếp (QT 5.3). Con số 8 phụ thuộc phiên bản, đo bằng `POST /projects/:id/variables`.
7. `${#TOKEN}` = **0**, job **xanh**, ô **im lặng + không chặn** — ô nguy hiểm nhất, lần thứ 6 bảng này xuất hiện trong khoá. Dòng đổi ô: `: "${TOKEN:?thiếu TOKEN}"` ở dòng đầu `script`, giá **0,01 giây** (QT 5.2).
8. In ra **đường dẫn** tệp tạm, ví dụ `/builds/<group>/<project>.tmp/KUBECONFIG_FILE`. Hai triệu chứng đối xứng: biến thường ở chỗ cần tệp → lỗi phân tích cú pháp ở **dòng 1 cột 1**; biến file ở chỗ cần nội dung → nội dung là một dòng trông như đường dẫn (QT 6.1).
9. `echo ${#TOKEN}` — kỳ vọng **20**, thực tế **21**; và `printf %s "$TOKEN" | od -c | tail -2` — thấy `\n` ở byte cuối. **1** byte thừa đủ đổi 200 thành 401. Không so bằng mắt trong log vì `masked` che đúng chỗ cần nhìn (QT 6.2).
10. Còn **6** ký tự (`Paw0rd`), hụt **2**, vì giá trị biến được mở rộng: `$$` bị đọc là tham chiếu tới biến rỗng. Tắt bằng `expand: false` trong YAML hoặc `raw=true` qua API (QT 6.3).
11. `variables` cấp job của job `trigger` xuống con như **pipeline variable** của con (nấc 1 ở phía dưới, thắng cả YAML repo con); `variables` cấp trên cùng vào job `trigger` theo kế thừa thường, chịu `inherit:variables`; pipeline variable của cha chịu `trigger:forward`. "Phải đo" vì mặc định và tương tác giữa ba đường đổi giữa các phiên bản (QT 7.1).
12. Từ **12 kB** lên khoảng **400 kB**, khoảng **250–400** dòng biến — bậc độ lớn, không phải hằng số. Hai thứ `masked` không che nổi: `CI_JOB_TOKEN` nguyên văn, và biến kiểu file (đường dẫn cùng nội dung in ra khi script chạy) — đúng theo QT 5.1 (QT 7.2).

---

## §12. Tài liệu tham khảo

| Nguồn | Loại | Phiên bản |
|---|---|---|
| GitLab Docs — *CI/CD variables* và *CI/CD variables precedence* | (a) tài liệu chính thức | 17.7 |
| GitLab Docs — *Mask a CI/CD variable* · *Protect a CI/CD variable* | (a) | 17.7 |
| GitLab Docs — *Use file type CI/CD variables* · *Prevent variable expansion* | (a) | 17.7 |
| GitLab Docs — *Predefined variables reference* (`CI_*`, `CI_JOB_TOKEN`) | (a) | 17.7 |
| GitLab Docs — *Downstream pipelines*: `trigger`, `inherit:variables`, `trigger:forward` | (a) | 17.7 |
| GitLab Docs — *Debug logging* (`CI_DEBUG_TRACE`) | (a) | 17.7 |
| GitLab API — `/projects/:id/variables`, `/groups/:id/variables`, `.../jobs/:id/trace`, `POST .../erase`, `.../protected_branches` | (a) | v4 |
| Thứ tự ưu tiên từng **cặp** nấc trên chính instance của mình | (c) **phải đo** | Lab bước 1, tám cặp |
| `masked` có che trong artifact và qua `base64` hay không; ngưỡng bật `masked` | (c) **phải đo** | Lab bước 3 |
| Số biến xuống pipeline con; kích thước log khi bật `CI_DEBUG_TRACE` | (c) **phải đo** | Lab bước 5 |

> **Về việc trích dẫn.** Tám dòng loại (a) là chỗ nên tra tài liệu của **đúng phiên bản đang chạy**. Ba dòng loại (c) là chỗ **không được** tra: sơ đồ chín nấc, hành vi masking, kế thừa xuống pipeline con và ngưỡng `masked` đều đã đổi trong dòng 15.x–17.x. Hiện vật buổi này phải ghi kèm số phiên bản GitLab và runner đã đo.

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10' |
| §1 | Sau buổi này học viên làm được gì | 1' |
| §2 | Cần biết trước | 1' |
| §3 | Thuật ngữ và mô hình tư duy | 8' |
| §4 | Chín nguồn biến và một bảng thứ tự | 11' |
| §5 | `masked` và `protected`: hai cơ chế, hai bài toán | 9' |
| §6 | Biến kiểu file, ký tự vô hình, và việc mở rộng biến | 9' |
| §7 | Biến xuống downstream pipeline, và `CI_DEBUG_TRACE` | 5' |
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
> Mọi checkpoint gọi **API GitLab**, không xem giao diện. Lý do ở §L2 quyết định 2.
> Buổi này **nạp lại** bộ công cụ buổi 05 (`~/lab05/cong-cu.sh`, `~/lab05/doc-pha.sh`) và không viết lại một hàm nào của nó.
> Buổi này đụng **hạ tầng dùng chung** ở ba chỗ: biến mức **project**, biến mức **group**, biến mức **instance**. Cả ba đều được chụp ảnh trạng thái ở §L1, xoá sạch ở §L8, và CHECKPOINT 12 kiểm bằng lệnh.
> Buổi này cũng là lần đầu học viên chạm vào một thao tác **có hậu quả bảo mật**: `CI_DEBUG_TRACE` in toàn bộ môi trường job vào log, kể cả `CI_JOB_TOKEN`. §L8 có bước **xoá log** bắt buộc và CHECKPOINT 12 kiểm nó.
> Hiện vật nộp chính là `bang-9-nguon-bien.tsv` — **8** dòng dữ liệu, mỗi dòng là một phép so **cặp nấc kề nhau** với nấc thắng **đo được** trên GitLab của chính học viên. Không ai được chép bảng chín nấc từ tệp lý thuyết vào đó.

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| # | Mục tiêu | Tiêu chí hoàn thành (kiểm chứng được bằng lệnh) |
|---|---|---|
| TH1 | Viết `dat-bien.sh` — tạo/xoá/liệt kê biến qua API ở **ba** phạm vi, có bốn cờ giá trị | `bash -n dat-bien.sh` không lỗi; `liet-ke` in được mã HTTP; buổi 07 §L1 dòng 6 gọi lại chính tệp này |
| TH2 | Viết `so-nac.sh` — chạy **một** cặp nấc và in nấc thắng | Chạy `bash so-nac.sh 6 7` in ra một dòng TSV có cột `nac_thang` khác rỗng |
| TH3 | **Đo QT 4.1** — dựng `bang-9-nguon-bien.tsv` bằng **tám** phép so cặp kề nhau | Tệp có **8** dòng dữ liệu, mỗi dòng ≥ **8** cột, mọi ô `nac_thang` khác rỗng, có dòng ghi phiên bản GitLab đã đo |
| TH4 | Kiểm chứng QT 4.2 — nấc **2** thắng nấc **7**, và liệt kê được danh sách "bom hẹn giờ" | Job in ra `project` chứ không phải `yaml`; `comm -12` in ra đúng **1** tên biến |
| TH5 | Kiểm chứng QT 4.4 — `variables` cấp job hợp nhất theo **tên biến** | Một job thấy **3** biến (1 bị ghi đè, 2 còn nguyên); job `inherit:variables: false` chỉ thấy **1** |
| TH6 | Tái hiện hỏng im lặng **số 2 và số 1** trong **một** pipeline xanh | `status == "success"` **và** `MOI_TRUONG=project` **và** `${#TOKEN}` = **0** — ba khẳng định cùng lúc |
| TH7 | Ca đối chứng **PHẢI THẤT BẠI** — `${VAR:?}` làm job đỏ ngay dòng đầu | `status == "failed"`, `trace` có dòng khẳng định, và **0** dòng của lệnh thứ hai |
| TH8 | **Đo QT 5.1** — `masked` che gì, và **ba** đường nó không bịt | Tải artifact về bằng API rồi `grep -c` giá trị gốc ra **1**; log trực tiếp ra **0** |
| TH9 | **Đo QT 5.3** — điều kiện bật `masked` | Hai giá trị đầu cho mã HTTP **400**, giá trị thứ ba cho **201**; đo được ngưỡng độ dài thật |
| TH10 | **Đo QT 6.1, QT 6.2, QT 6.3** — ba ca "giá trị tới nơi không phải giá trị tôi đặt" | Ba tệp JSON do job sinh: đường dẫn so nội dung · độ dài hụt/thừa **1** byte và **200** so **401** · **8** so **6** ký tự |
| TH11 | **Đo QT 4.3, QT 7.1, QT 7.2** — nấc 5 · ba cách khai xuống pipeline con · giá `CI_DEBUG_TRACE` | Job sau in giá trị của nấc **2**; `pipeline-con.md` ghi số biến xuống được của **3** ca; log **12 kB → ~400 kB** đo bằng `wc -c` |
| TH12 | Nộp hiện vật và trả hạ tầng dùng chung về nguyên trạng | `kiem-hien-vat.sh` in `ĐẠT`; `GET /variables` của **cả ba** phạm vi trả mảng rỗng; job đã bật `CI_DEBUG_TRACE` có `erased_at` khác `null` |

**Sản phẩm cuối buổi:** `gitlab-portfolio/06-bien-va-bi-mat/` gồm **`bang-9-nguon-bien.tsv`** (8 phép so cặp — hiện vật chính), **`nam-ca-bien-sai.md`** (năm ca, mỗi ca bốn dòng), `dat-bien.sh`, `so-nac.sh`, `masked-lo.md`, `bien-file-va-expand.md`, `pipeline-con.md`, `.gitlab-ci.yml` bản cuối, `checkpoint.log` đủ **12** dòng `ĐẠT`.

Hai hiện vật **cốt lõi** — thiếu một trong hai là chưa nộp bài — là `bang-9-nguon-bien.tsv` và `nam-ca-bien-sai.md`. Ai đi **đường B** ở §L9 (không có quyền tạo biến mức group) vẫn có đủ cả hai, với bảng ghi **6** dòng thay vì 8 và một dòng ghi rõ lý do.

---

## L1. Điều kiện tiên quyết về môi trường

| # | Kiểm tra | Lệnh | Kết quả kỳ vọng |
|---|---|---|---|
| 1 | Đã nạp biến môi trường lab | `echo "$GITLAB" "$GITLAB_TOKEN" \| wc -w` | `2` |
| 2 | GitLab sẵn sàng | `curl -sf -o /dev/null -w '%{http_code}\n' "$GITLAB/-/readiness"` | `200` |
| 3 | Token gọi được API | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/user" \| jq -r .username` | tên đăng nhập, khác rỗng |
| 4 | **Còn bộ công cụ buổi 05** — buổi này nạp lại, không viết lại | `grep -cE '^(day\|day_nhanh\|cho_pipeline\|job_bang\|job_id\|job_tt\|job_log\|job_log_sach\|art_http\|art_tep\|art_zip)\(\)' ~/lab05/cong-cu.sh` | `11` — thiếu thì §L9 dòng 1 |
| 5 | **Còn `doc-pha.sh` buổi 05** — bước 5 dùng nó đọc `trace` | `bash -n ~/lab05/doc-pha.sh && grep -c section_start ~/lab05/doc-pha.sh` | `≥ 1` |
| 6 | Token **tạo và xoá được** biến mức **project** | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects?membership=true&per_page=1" \| jq -r '.[0].id'` rồi thử `POST /variables` trên project đó | một số; `POST` trả `201` — `403` thì không làm được buổi này, xem §L9 dòng 2 |
| 7 | Token **tạo và xoá được** biến mức **group** — đường A của bước 1 | `curl -s -o /dev/null -w '%{http_code}\n' --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/groups" --form "name=lab06-thu-$USER" --form "path=lab06-thu-$USER"` | `201` — khác `201` thì đi **đường B** §L9 dòng 3, bảng còn **6** dòng |
| 8 | Có quyền **admin instance** — cần cho nấc 4 | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/user" \| jq -r .is_admin` | `true` — `false` hay `null` thì §L9 dòng 4, bảng bớt tiếp |
| 9 | Nhánh mặc định **được bảo vệ** — QT 5.2 không đo được nếu thiếu | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID/protected_branches" \| jq -r '.[].name'` | có `main` — chạy sau khi tạo project ở §L3 mục 1.1 |
| 10 | Tạo được **project access token** — ca 4 cần một token thật dùng một lần | `curl -s -o /dev/null -w '%{http_code}\n' --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID/access_tokens" --form 'name=lab06-thu' --form 'scopes[]=read_api' --form "expires_at=$(date -d '+2 days' +%F)"` | `201` — khác thì §L9 dòng 5 |
| 11 | Có `jq`, `curl`, `git`, `awk`, `od`, `base64` | `command -v jq curl git awk od base64 \| wc -l` | `6` |
| 12 | Chưa có project lab 06 | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects?search=lab06-bien" \| jq length` | `0` — khác `0` thì §L9 dòng cuối |
| 13 | Đĩa trống — bài lab sinh khoảng **3 MB** artifact và **1,5 MB** log | `df -BG --output=avail "$HOME" \| tail -1` | `> 3G` |
| 14 | Ghi lại phiên bản để dán vào hiện vật | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/version" \| jq -r .version` | một chuỗi phiên bản — dán vào dòng đầu `bang-9-nguon-bien.tsv` |

### Sao lưu bắt buộc — ba phạm vi biến là hạ tầng dùng chung

Bài lab tạo biến ở **ba** phạm vi: project (của riêng mình), group (của riêng mình), và **instance** (của cả GitLab). Phạm vi thứ ba ảnh hưởng **mọi project của mọi người**, nên trước khi tạo gì phải chụp ảnh trạng thái hiện có. Bản chụp này là căn cứ để §L8 chứng minh ta chỉ xoá đúng thứ mình tạo:

```bash
source ~/.gitlab-lab.env
mkdir -p ~/lab06/sao-luu
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")

# Ảnh chụp trước buổi học — mức instance là quan trọng nhất
curl -sf "${H[@]}" "$GITLAB/api/v4/admin/ci/variables?per_page=100" \
  | jq -r '[.[].key] | sort | .[]' > ~/lab06/sao-luu/instance.truoc.txt
wc -l ~/lab06/sao-luu/instance.truoc.txt
```

Nếu tệp trên **khác rỗng** thì trên instance này đã có người đặt biến mức 4 — đừng xoá của họ. Ghi lại danh sách đó, và ở §L8 chỉ xoá đúng tên `NAC_THU` mà ta tạo. Nếu không có quyền admin thì tệp rỗng và nấc 4 đi theo §L9 dòng 4.

**Cảnh báo về mức độ tác động.** Bài lab tạo **hai** project (`lab06-bien` và `lab06-bien-downstream`), **một** group, và sinh khoảng **22–26 pipeline** — trong đó **8** pipeline là để dựng bảng chín nấc, tốn khoảng **4 phút runner**. Bốn thứ **tồn tại sau khi buổi học kết thúc** nếu không dọn, xếp theo mức tác động giảm dần:

1. **Biến `NAC_THU` mức instance (nấc 4).** Nó có mặt trong **mọi** job của **mọi** project trên GitLab này. Đây là thứ nguy hiểm nhất buổi tạo ra, và nó chỉ tồn tại trong khoảng 2 phút của một phép so cặp. Trên lớp đông người dùng chung một GitLab, **chỉ giảng viên** tạo biến mức instance, một lần, trước lớp; học viên đọc số và ghi vào bảng của mình. §L8.1 xoá và CHECKPOINT 12 kiểm.
2. **Biến `NAC_THU` mức group (nấc 3).** Ảnh hưởng mọi project trong group. Dùng group riêng của mình, không dùng group chung của lớp. §L8.1 xoá.
3. **Log của job đã bật `CI_DEBUG_TRACE`.** Khoảng **400 kB** log chứa `CI_JOB_TOKEN` nguyên văn và toàn bộ biến của job. Ai đọc được project đều tải về được bằng một lệnh `curl`. §L8.2 xoá bằng `POST /jobs/:id/erase` và CHECKPOINT 12 đòi `erased_at` khác `null`.
4. **Một project access token** tạo ở §L1 dòng 10 cho ca 4. Nó có scope `read_api` và hạn 2 ngày; §L8.1 thu hồi ngay chứ không đợi hết hạn.

Chi phí phút runner của buổi: **8** pipeline của bước 1 khoảng **4 phút**, bước 2 khoảng **2 phút**, bước 3 khoảng **1,5 phút**, bước 4 khoảng **2 phút**, bước 5 khoảng **3 phút** — tổng khoảng **13 phút runner**. Đây là buổi **rẻ nhất** về phút runner trong giai đoạn 1: mọi job đều là job in một dòng chữ, không có job nào biên dịch hay tải phụ thuộc.

**Hai ca đối chứng PHẢI THẤT BẠI — báo trước cho lớp.** Ở **bước 2**, job `deploy-co-khang-dinh` trên nhánh feature **phải đỏ** ngay dòng đầu vì `: "${TOKEN:?}"`. Đó là kết quả **đúng**, và nó đối lập với job `deploy-khong-khang-dinh` **xanh mà không làm gì**. Ở **bước 3**, việc bật `masked` cho `abc` và `mot hai ba` **phải bị API từ chối** với mã HTTP **400**. Ai gọi giảng viên vì hai chỗ đó là đã bỏ qua đoạn này.

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    HV["Học viên<br/>máy chủ lab"]
    HV -->|"dat-bien.sh — POST/PUT/DELETE"| API["API GitLab v4<br/>projects/groups/admin variables<br/>pipelines · jobs · trace · artifacts"]
    HV -->|"so-nac.sh — 1 cặp = 1 pipeline"| API
    HV -->|"git push -o ci.skip"| PRJ["Project lab06-bien"]

    API --> N1["Nấc 1 pipeline variable<br/>POST /pipeline?ref=..."]
    API --> N2["Nấc 2 project variable"]
    API --> N3["Nấc 3 group variable"]
    API --> N4["Nấc 4 instance variable<br/>CHỈ giảng viên"]
    PRJ --> N57["Nấc 5 dotenv · 6 job · 7 trên cùng<br/>trong .gitlab-ci.yml"]
    PRJ --> N89["Nấc 8 deployment · 9 predefined<br/>không đặt được bằng tay"]

    N1 --> RN["Runner lab-runner<br/>executor docker<br/>nhận tập biến ĐÃ DẸP PHẲNG"]
    N2 --> RN
    N3 --> RN
    N4 --> RN
    N57 --> RN
    N89 --> RN

    RN -->|"in NAC_THU=[...]"| TR["trace đọc qua API"]
    TR --> BANG["bang-9-nguon-bien.tsv<br/>8 dòng · 8 phép so cặp kề nhau"]

    BANG --> B1["Bước 1 — bảng chín nấc<br/>CP1 CP2 CP3"]
    API --> B2["Bước 2 — ca 1 và ca 2<br/>YAML vô hiệu · protected rỗng<br/>CP4 CP5"]
    API --> B3["Bước 3 — masked che gì<br/>artifact tải về rồi grep<br/>CP6 CP7"]
    API --> B4["Bước 4 — ca 3 4 5<br/>type file · 1 byte · expand<br/>CP8 CP9 CP10"]
    API --> B5["Bước 5 — dotenv · pipeline con<br/>CI_DEBUG_TRACE<br/>CP11"]
    API --> B8["L8 — xoá 3 phạm vi biến<br/>xoá log debug trace<br/>CP12"]

    CC["cong-cu.sh buổi 05 — 11 hàm<br/>doc-pha.sh buổi 05"] --> B1
    CC --> B5
    WF["workflow chuẩn buổi 04<br/>dán vào từ đầu"] --> B1
    DS["Project lab06-bien-downstream"] --> B5
```

**Năm quyết định thiết kế:**

1. **Bảng chín nấc dựng bằng TÁM phép so cặp kề nhau, không bằng một job in tất cả.** Một job in tất cả biến chỉ cho ta **giá trị cuối cùng** của mỗi biến, và giá trị cuối cùng không nói nấc nào thắng — nó là kết quả của một phép hợp nhất đã xảy ra trên server và runner không biết gì về nó. Phép so cặp thì cho một kết quả **nhị phân** không thể hiểu nhầm: khai cùng một tên `NAC_THU` ở đúng hai nấc, giá trị in ra là `nac-2` hay `nac-7`, hết. Chín nấc có đúng **8** khe kề nhau, nên **8** phép so là đủ để suy ra toàn bộ thứ tự — và rẻ hơn 36 phép so mọi cặp. Cái giá: **8** pipeline, khoảng **4 phút runner**, dùng lại được cả năm.

2. **Mọi biến tạo bằng API, không tạo bằng giao diện.** Ba lý do, không phải một. Việc dựng bảng phải **lặp lại được**: tám cặp nghĩa là tạo và xoá biến hơn hai mươi lần, làm tay trong giao diện thì sai một lần là bảng sai mà không biết sai ở đâu. Việc dọn phải **kiểm được bằng lệnh**: `GET /variables` trả mảng rỗng là bằng chứng, "tôi đã xoá rồi" thì không. Và mã HTTP là **dữ liệu** của bài: bước 3 lấy chính mã **400** của `POST /variables` làm bằng chứng cho QT 5.3, thứ mà giao diện chỉ hiện thành một dòng chữ đỏ không đo được.

3. **Năm ca "biến sai" tái hiện theo thứ tự hay gặp trong thực tế, không theo thứ tự dễ dựng.** Hai ca đắt nhất khi gặp ở prod — nấc 2 âm thầm ghi đè YAML, và biến `protected` rỗng làm job deploy **xanh** — đứng ở **bước 2**, trước ba ca dễ dựng hơn của bước 4. Ca `protected` rỗng phải là ca học viên gặp **sớm nhất**, vì nó là lý do của mọi dòng `: "${VAR:?}"` trong 42 buổi còn lại; để nó xuống cuối buổi thì lớp đã cạn sức tập trung đúng lúc gặp ô nguy hiểm nhất của bảng hai thuộc tính hỏng (buổi 01 QT 7.1).

4. **Việc chứng minh `masked` không che artifact làm bằng cách TẢI artifact về rồi `grep`, không bằng cách nhìn log.** Đây là dạng checkpoint số 2 của quy ước khoá — kiểm tệp hiện vật. Nhìn log thì thấy `[MASKED]` và kết luận được đúng một điều: đường log đã bị bịt. Nó không nói gì về ba đường còn lại. Chỉ khi `curl` tải `ro-ri.env` về máy mình rồi `grep -c "$TOKEN_THAT"` ra **1**, câu "`masked` không phải bảo vệ secret" mới thôi là một lời tuyên bố và trở thành một con số.

5. **`CI_DEBUG_TRACE` chỉ bật cho MỘT job, trên MỘT nhánh riêng, và §L8 có bước xoá log bắt buộc.** Buổi này là buổi đầu tiên học viên chạm vào một thao tác để lại **hậu quả bảo mật** chứ không phải hậu quả về giây hay MB. Vì vậy nó không được bật bằng cách commit `CI_DEBUG_TRACE: "true"` vào `.gitlab-ci.yml` — commit là thứ ở lại trong lịch sử git và sẽ có người merge lên nhánh mặc định. Nó được bật bằng **pipeline variable** truyền lúc `POST /pipeline` (nấc 1), tức thứ tồn tại đúng một pipeline. Và log của job đó bị xoá ở §L8.2. Thói quen dọn phải được tập ngay tại đây, không đợi tới buổi 29.

---

## L3. Bước 1 — Dựng bảng chín nấc bằng thực nghiệm, tám cặp (35 phút)

Kiểm chứng QT 4.1, QT 4.2, QT 4.4.

Đây là bước dài nhất và là bước sinh ra hiện vật cốt lõi. Sơ đồ chín nấc ở §0.2 tệp lý thuyết là **giá trị tham chiếu** của GitLab CE 17.7; bài lab **không** chép nó. Nếu bảng lớp đo ra khác sơ đồ ở một khe nào, thì bảng lớp đúng và sơ đồ sai — đó là điểm dạy, không phải sự cố.

### 1.1. Tạo hai project, một group, và nạp lại bộ công cụ buổi 05 (5 phút)

```bash
source ~/.gitlab-lab.env
source ~/lab05/cong-cu.sh 2>/dev/null || true      # nạp trước để có H[@]; PID chưa có thì bỏ qua
export HAU_TO="${USER}"
mkdir -p ~/lab06 && cd ~/lab06
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")

# Group riêng của học viên — nấc 3 nằm ở đây, KHÔNG dùng group chung của lớp
GID=$(curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/groups" \
  --form "name=lab06-nhom-$HAU_TO" --form "path=lab06-nhom-$HAU_TO" | jq -r .id)

# Project chính và project hạ nguồn, cả hai trong group vừa tạo
PID=$(curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects" \
  --form "name=lab06-bien-$HAU_TO" --form "namespace_id=$GID" --form 'visibility=internal' | jq -r .id)
PID_CON=$(curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects" \
  --form "name=lab06-bien-downstream-$HAU_TO" --form "namespace_id=$GID" --form 'visibility=internal' | jq -r .id)

{ echo "export GID=$GID"; echo "export PID=$PID"; echo "export PID_CON=$PID_CON"; } >> ~/.gitlab-lab.env
echo "GID=$GID  PID=$PID  PID_CON=$PID_CON"
source ~/lab05/cong-cu.sh          # nạp lại ĐẦY ĐỦ, giờ đã có PID
```

Kho git cho project chính, kèm `workflow` chuẩn của buổi 04 ngay từ commit đầu — không có nó thì một push lên nhánh đang có merge request mở sinh **2** pipeline cho **1** commit, và mọi phép so cặp của bước 1 có hai kết quả để chọn:

```bash
cd ~/lab06 && git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID" | jq -r .path_with_namespace).git"
```

```yaml
# ~/lab06/khoi-workflow.yml — mảnh dùng lại, so-nac.sh sẽ ghép nó vào mọi tệp nó sinh
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS'
      when: never
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
    - if: '$CI_COMMIT_TAG'
    - if: '$CI_COMMIT_BRANCH'
```

```bash
cd ~/lab06
printf 'lab06\n' > README.md
cat > .gitlab-ci.yml <<'YML'
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS'
      when: never
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
    - if: '$CI_COMMIT_TAG'
    - if: '$CI_COMMIT_BRANCH'
in-nac:
  image: alpine:3.20
  script:
    - 'echo "NAC_THU=[$NAC_THU]"'
YML
git add -A && git commit -q -m "khoi tao lab06"
git push -q -o ci.skip origin HEAD:refs/heads/main
# Nhánh mặc định phải ĐƯỢC BẢO VỆ — QT 5.2 ở bước 2 không đo được nếu thiếu
curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/protected_branches" | jq -r '.[].name'
```

`git push -o ci.skip` là công cụ đắt giá của cả bước 1: nó đẩy commit lên **mà không sinh pipeline**. Nhờ đó mỗi phép so cặp sinh đúng **1** pipeline do `so-nac.sh` gọi `POST /pipeline`, không phải 2 — và con số **8 pipeline** ở §L1 mới đúng.

### 1.2. Công cụ 1 — `dat-bien.sh`, hiện vật dùng lại ở buổi 07 và các buổi cloud (7 phút)

Đây là hiện vật được gọi lại nhiều nhất của buổi: buổi 07 §L1 dòng 6 kiểm sự tồn tại của nó, và các buổi 37–43 dùng nó dựng biến OIDC. Viết cho tử tế: **ba** phạm vi, **bốn** cờ giá trị, và **luôn in mã HTTP** — vì mã HTTP là dữ liệu của QT 5.3, không phải thông tin phụ.

```bash
cat > ~/lab06/dat-bien.sh <<'SH'
#!/usr/bin/env bash
# dat-bien.sh — tạo / xoá / liệt kê biến CI qua API GitLab. LUÔN in mã HTTP.
#
# Dùng:
#   bash dat-bien.sh dat     <TEN> <GIA_TRI> [cờ...]
#   bash dat-bien.sh xoa     <TEN>           [cờ phạm vi]
#   bash dat-bien.sh liet-ke                 [cờ phạm vi]
#   bash dat-bien.sh don-sach                [cờ phạm vi]   # xoá MỌI biến trong phạm vi
#
# Cờ GIÁ TRỊ (chỉ dùng với 'dat'):
#   --masked        masked=true       che giá trị trong log job          (QT 5.1)
#   --protected     protected=true    chỉ cấp cho ref được bảo vệ        (QT 5.2)
#   --file          variable_type=file  ghi ra tệp tạm, biến giữ ĐƯỜNG DẪN (QT 6.1)
#   --no-expand     raw=true          tắt mở rộng biến, tương đương expand: false (QT 6.3)
#
# Cờ PHẠM VI (dùng với mọi lệnh):
#   (mặc định)      project  -> /projects/$PID/variables
#   --group <GID>   group    -> /groups/<GID>/variables
#   --instance      instance -> /admin/ci/variables      (cần quyền admin)
#
# ĐẦU RA: một dòng  <lenh>\t<pham_vi>\t<TEN>\t<HTTP>\t<thong_diep>
# MÃ THOÁT: 0 nếu HTTP thuộc 2xx · 1 nếu khác · 2 thiếu tham số · 3 thiếu biến môi trường
#
# CƠ CHẾ đáng nhớ: 'dat' thử POST trước; nếu API trả 400 vì biến đã tồn tại thì
# tự chuyển sang PUT. Đó là lý do một lệnh 'dat' đôi khi in HTTP 200 (PUT) chứ
# không phải 201 (POST) — cả hai đều là thành công.
set -uo pipefail

LENH="${1:-}"; shift || true
: "${GITLAB:?chưa đặt GITLAB}"    || exit 3
: "${GITLAB_TOKEN:?chưa đặt GITLAB_TOKEN}" || exit 3

TEN=""; GT=""; PHAM_VI="project"; GID_IN=""
FORM=()
case "$LENH" in
  dat)  TEN="${1:-}"; GT="${2:-}"; shift 2 2>/dev/null || true ;;
  xoa)  TEN="${1:-}"; shift 1 2>/dev/null || true ;;
  liet-ke|don-sach) : ;;
  *) echo "Dùng: bash dat-bien.sh {dat|xoa|liet-ke|don-sach} ..." >&2; exit 2 ;;
esac

while [ $# -gt 0 ]; do
  case "$1" in
    --masked)     FORM+=(--form 'masked=true') ;;
    --protected)  FORM+=(--form 'protected=true') ;;
    --file)       FORM+=(--form 'variable_type=file') ;;
    --no-expand)  FORM+=(--form 'raw=true') ;;
    --group)      PHAM_VI="group"; GID_IN="${2:-}"; shift ;;
    --instance)   PHAM_VI="instance" ;;
    *) echo "cờ không hiểu: $1" >&2; exit 2 ;;
  esac
  shift
done

case "$PHAM_VI" in
  project)  : "${PID:?chưa có PID}" || exit 3; GOC="$GITLAB/api/v4/projects/$PID/variables" ;;
  group)    [ -n "$GID_IN" ] || { echo "--group cần <GID>" >&2; exit 2; }
            GOC="$GITLAB/api/v4/groups/$GID_IN/variables" ;;
  instance) GOC="$GITLAB/api/v4/admin/ci/variables" ;;
esac
HDR=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")
TMP=$(mktemp)

bao() { printf '%s\t%s\t%s\t%s\t%s\n' "$1" "$PHAM_VI" "$2" "$3" "$4"; }

case "$LENH" in
  dat)
    [ -n "$TEN" ] || { echo "thiếu TEN" >&2; exit 2; }
    MA=$(curl -s -o "$TMP" -w '%{http_code}' --request POST "${HDR[@]}" "$GOC" \
          --form "key=$TEN" --form "value=$GT" "${FORM[@]}")
    if [ "$MA" = "400" ] && grep -q 'has already been taken' "$TMP"; then
      MA=$(curl -s -o "$TMP" -w '%{http_code}' --request PUT "${HDR[@]}" "$GOC/$TEN" \
            --form "value=$GT" "${FORM[@]}")
    fi
    bao dat "$TEN" "$MA" "$(jq -rc '.message // .error // "-"' "$TMP" 2>/dev/null || echo -)"
    ;;
  xoa)
    [ -n "$TEN" ] || { echo "thiếu TEN" >&2; exit 2; }
    MA=$(curl -s -o "$TMP" -w '%{http_code}' --request DELETE "${HDR[@]}" "$GOC/$TEN")
    bao xoa "$TEN" "$MA" -
    ;;
  liet-ke)
    MA=$(curl -s -o "$TMP" -w '%{http_code}' "${HDR[@]}" "$GOC?per_page=100")
    bao liet-ke "-" "$MA" "$(jq -rc '[.[] | {key, masked, protected, variable_type, raw}]' "$TMP" 2>/dev/null || echo -)"
    ;;
  don-sach)
    MA=$(curl -s -o "$TMP" -w '%{http_code}' "${HDR[@]}" "$GOC?per_page=100")
    n=0
    for k in $(jq -r '.[].key' "$TMP" 2>/dev/null); do
      curl -s -o /dev/null --request DELETE "${HDR[@]}" "$GOC/$k"; n=$((n+1))
    done
    bao don-sach "$n biến" "$MA" -
    ;;
esac
rm -f "$TMP"
case "$MA" in 2*) exit 0 ;; *) exit 1 ;; esac
SH
chmod +x ~/lab06/dat-bien.sh
bash -n ~/lab06/dat-bien.sh && echo "cu phap dat-bien.sh: OK"
bash ~/lab06/dat-bien.sh liet-ke
```

Thử ba phạm vi ngay tại đây — nếu một phạm vi nào không chạy được thì phải biết **trước** khi bắt đầu tám cặp, không phải giữa cặp thứ tư:

```bash
bash ~/lab06/dat-bien.sh dat THU_PHAM_VI p                    # project   -> 201
bash ~/lab06/dat-bien.sh dat THU_PHAM_VI g --group "$GID"      # group     -> 201
bash ~/lab06/dat-bien.sh dat THU_PHAM_VI i --instance          # instance  -> 201 hoặc 403
for c in "" "--group $GID" "--instance"; do
  bash ~/lab06/dat-bien.sh xoa THU_PHAM_VI $c
done
```

### 1.3. Công cụ 2 — `so-nac.sh`, chạy MỘT cặp và in nấc thắng (8 phút)

Script này làm đúng bốn việc cho một cặp `<A> <B>`: dọn `NAC_THU` ở mọi phạm vi, đặt nó ở đúng hai nấc, sinh **một** pipeline, rồi đọc `trace` in ra một dòng TSV. Ba nấc cuối cần đường riêng và script nói rõ điều đó trong phần chú thích — đó là một phần kết quả của bài lab, không phải thiếu sót của script.

```bash
cat > ~/lab06/so-nac.sh <<'SH'
#!/usr/bin/env bash
# so-nac.sh — chạy MỘT phép so cặp nấc kề nhau và in MỘT dòng TSV cho bang-9-nguon-bien.tsv
#
# Dùng:  bash so-nac.sh <nac_A> <nac_B>          ví dụ: bash so-nac.sh 6 7
# Cần:   GITLAB, GITLAB_TOKEN, PID; GID nếu cặp có nấc 3; quyền admin nếu có nấc 4
#        thư mục kho git ~/lab06 đã push nhánh 'do-nac'
#
# CÁCH ĐẶT GIÁ TRỊ Ở TỪNG NẤC — giá trị luôn là chuỗi "nac-<N>":
#   1  pipeline variable   POST /pipeline?ref=do-nac  --form 'variables[][key]=NAC_THU'
#   2  project variable    dat-bien.sh dat NAC_THU nac-2
#   3  group variable      dat-bien.sh dat NAC_THU nac-3 --group $GID
#   4  instance variable   dat-bien.sh dat NAC_THU nac-4 --instance
#   5  dotenv job trước    job 'sinh' ghi NAC_THU=nac-5 vào bien.env, job 'in-nac' có needs
#   6  variables cấp job   khối variables của job 'in-nac'
#   7  variables cấp trên cùng
#   8  deployment variable KHÔNG đặt được bằng tay trên GitLab CE không tích hợp môi trường.
#      Cặp 7-8 vì thế đo bằng cách cho job có 'environment:' và ĐẾM số biến deployment
#      nhận được; kết quả 0 nghĩa là nấc 8 rỗng và nấc 7 thắng vì không có đối thủ.
#   9  predefined CI_*     không đặt được. Cặp 8-9 đo bằng đường thay thế 7-9: khai một
#      biến CI_* ở nấc 7 rồi xem giá trị nào tới job. Biến dùng là CI_PROJECT_TITLE —
#      KHÔNG dùng CI_DEFAULT_BRANCH hay CI_PIPELINE_SOURCE vì khối workflow đọc chúng.
#
# ĐẦU RA (TSV, 9 cột):
#   cap  nac_cao  nac_thap  ten_bien  gia_tri_in_ra  nac_thang  pipeline_id  trang_thai  ghi_chu
# MÃ THOÁT: 0 đo được · 2 thiếu tham số · 4 pipeline không xanh · 5 không đọc được giá trị
set -uo pipefail
A="${1:-}"; B="${2:-}"
[ -n "$A" ] && [ -n "$B" ] || { echo "Dùng: bash so-nac.sh <nac_A> <nac_B>" >&2; exit 2; }
[ "$A" -gt "$B" ] && { t="$A"; A="$B"; B="$t"; }     # A luôn là nấc CAO (số nhỏ)
: "${GITLAB:?}"; : "${GITLAB_TOKEN:?}"; : "${PID:?}"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")
A_URL="$GITLAB/api/v4/projects/$PID"
DB="$HOME/lab06/dat-bien.sh"
BIEN="NAC_THU"; GHI="-"
if [ "$A" = 8 ] && [ "$B" = 9 ]; then
  BIEN="CI_PROJECT_TITLE"; GHI="nac 8 rong -> do bang duong thay the 7-9"
fi

# 1) DỌN: NAC_THU không được sót ở nấc nào ngoài hai nấc của cặp này
for c in "" "--group ${GID:-0}" "--instance"; do
  bash "$DB" xoa "$BIEN" $c >/dev/null 2>&1 || true
done

# 2) Sinh .gitlab-ci.yml cho đúng cặp này
cd "$HOME/lab06"
{
  cat khoi-workflow.yml
  [ "$A" = 7 ] || [ "$B" = 7 ] && printf 'variables:\n  NAC_THU: "nac-7"\n'
  [ "$A" = 8 ] && [ "$B" = 9 ] && printf 'variables:\n  CI_PROJECT_TITLE: "nac-7"\n'
  if [ "$A" = 5 ] || [ "$B" = 5 ]; then
    printf 'stages: [sinh, doc]\nsinh:\n  stage: sinh\n  image: alpine:3.20\n  script:\n'
    printf '    - echo "NAC_THU=nac-5" > bien.env\n  artifacts:\n    reports:\n      dotenv: bien.env\n'
    printf 'in-nac:\n  stage: doc\n  needs: ["sinh"]\n'
  else
    printf 'in-nac:\n'
  fi
  printf '  image: alpine:3.20\n'
  [ "$A" = 8 ] && [ "$B" != 9 ] && printf '  environment:\n    name: do-nac-8\n'
  [ "$B" = 8 ] && printf '  environment:\n    name: do-nac-8\n'
  [ "$A" = 6 ] || [ "$B" = 6 ] && printf '  variables:\n    NAC_THU: "nac-6"\n'
  printf '  script:\n    - '"'"'echo "GIA_TRI=[$%s]"'"'"'\n' "$BIEN"
  printf '    - '"'"'echo "SO_BIEN_DEPLOY=$(env | grep -cE "^(KUBE_|CI_ENVIRONMENT_SLUG=)" || true)"'"'"'\n'
} > .gitlab-ci.yml

git add -A >/dev/null; git commit -q -m "so nac $A-$B" --allow-empty
git push -q -f -o ci.skip origin HEAD:refs/heads/do-nac 2>/dev/null

# 3) Đặt giá trị ở hai nấc bằng API (nấc 5,6,7 đã nằm trong YAML ở trên)
for n in "$A" "$B"; do
  case "$n" in
    2) bash "$DB" dat "$BIEN" "nac-2" >/dev/null ;;
    3) bash "$DB" dat "$BIEN" "nac-3" --group "${GID:?cặp này cần GID}" >/dev/null ;;
    4) bash "$DB" dat "$BIEN" "nac-4" --instance >/dev/null ;;
  esac
done

# 4) MỘT pipeline. Nấc 1 truyền biến ngay lúc tạo pipeline.
if [ "$A" = 1 ] || [ "$B" = 1 ]; then
  PIPE=$(curl -sf --request POST "${H[@]}" "$A_URL/pipeline?ref=do-nac" \
    --form "variables[][key]=$BIEN" --form "variables[][value]=nac-1" | jq -r .id)
else
  PIPE=$(curl -sf --request POST "${H[@]}" "$A_URL/pipeline?ref=do-nac" | jq -r .id)
fi
t=0; ST=running
while [ "$t" -lt 300 ]; do
  ST=$(curl -sf "${H[@]}" "$A_URL/pipelines/$PIPE" | jq -r .status)
  case "$ST" in success|failed|canceled|skipped) break ;; esac
  sleep 5; t=$((t+5))
done

# 5) Đọc giá trị từ trace của job in-nac
JID=$(curl -sf "${H[@]}" "$A_URL/pipelines/$PIPE/jobs?per_page=100" \
      | jq -r '.[] | select(.name=="in-nac") | .id' | head -1)
GT=$(curl -sf "${H[@]}" "$A_URL/jobs/$JID/trace" | tr -d '\r' \
     | sed 's/\x1b\[[0-9;K]*[a-zA-Z]//g' | grep -oE 'GIA_TRI=\[[^]]*\]' | head -1 \
     | sed 's/GIA_TRI=\[//; s/\]$//')
NDEP=$(curl -sf "${H[@]}" "$A_URL/jobs/$JID/trace" | tr -d '\r' \
     | grep -oE 'SO_BIEN_DEPLOY=[0-9]+' | head -1 | cut -d= -f2)

THANG=""
case "$GT" in
  nac-*) THANG="${GT#nac-}" ;;
  *)     THANG="9"; GHI="$GHI; gia tri predefined that: $GT" ;;
esac
[ "$B" = 8 ] && GHI="nac 8 rong: SO_BIEN_DEPLOY=${NDEP:-?}"
[ -n "$GT" ] || { echo "khong doc duoc gia tri (job $JID)" >&2; exit 5; }
printf '%s-%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
  "$A" "$B" "$A" "$B" "$BIEN" "$GT" "$THANG" "$PIPE" "$ST" "$GHI"
[ "$ST" = success ] || exit 4
SH
chmod +x ~/lab06/so-nac.sh
bash -n ~/lab06/so-nac.sh && echo "cu phap so-nac.sh: OK"
```

Tạo tệp `khoi-workflow.yml` mà script cần, rồi thử **một** cặp dễ nhất trước khi chạy cả tám — cặp `6-7` chỉ đụng YAML, không đụng API nào:

```bash
cat > ~/lab06/khoi-workflow.yml <<'YML'
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS'
      when: never
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
    - if: '$CI_COMMIT_TAG'
    - if: '$CI_COMMIT_BRANCH'
YML
cd ~/lab06 && bash so-nac.sh 6 7
```

Một dòng TSV in ra là bằng chứng script chạy đúng. Nếu cột `nac_thang` là `6` thì `variables` cấp job thắng cấp trên cùng — đúng nửa đầu của QT 4.4, và ta vừa **đo** chứ không tra.

### 1.4. Chạy tám cặp và dựng `bang-9-nguon-bien.tsv` (10 phút)

Tám cặp, tám pipeline, khoảng **4 phút runner**. Chạy nối tiếp, đừng chạy song song — hai phép so cùng lúc đều dùng tên biến `NAC_THU` ở cùng những phạm vi đó và sẽ ăn kết quả của nhau.

```bash
cd ~/lab06
{
  echo "# bang-9-nguon-bien.tsv — dung bang TAM phep so CAP NAC KE NHAU"
  echo "# phien ban: $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version) · runner: $(docker exec lab-runner gitlab-runner --version 2>/dev/null | awk '/^Version/{print $2}')"
  echo "# may do: $(hostname) · ngay: $(date +%F)"
  printf 'cap\tnac_cao\tnac_thap\tten_bien\tgia_tri_in_ra\tnac_thang\tpipeline_id\ttrang_thai\tghi_chu\n'
  for cap in "1 2" "2 3" "3 4" "4 5" "5 6" "6 7" "7 8" "8 9"; do
    bash so-nac.sh $cap || echo "$cap	-	-	-	-	-	-	LOI	khong do duoc"
  done
} | tee ~/lab06/bang-9-nguon-bien.tsv
```

Đọc bảng theo đúng một câu hỏi: **ở mỗi khe, nấc số nhỏ hơn có thắng không?** Tám ô `nac_thang` trả lời tám lần. Nếu cả tám lần nấc số nhỏ thắng thì thứ tự tham chiếu đúng trên instance này. Nếu có một khe ngược, ghi nó vào cột `ghi_chu` và **giữ nguyên số đo** — đừng sửa cho khớp sơ đồ.

Hai dòng cuối bảng cần đọc kỹ hơn sáu dòng đầu. Dòng `7-8`: nấc 8 là deployment variable, chỉ sinh ra từ tích hợp môi trường; trên GitLab CE 17.7 không tích hợp gì, job có `environment:` nhận **0** biến deployment. Nấc 7 thắng vì **không có đối thủ**, và đó là một kết quả đo được, không phải một chỗ trống. Dòng `8-9`: vì nấc 8 rỗng, khe này được đo bằng đường thay thế `7-9` — khai `CI_PROJECT_TITLE` ở nấc 7 rồi xem giá trị nào tới job. Đây là chỗ trả lời câu "biến `CI_*` có ghi đè được không" bằng số, không bằng trí nhớ.

**CHECKPOINT 1 — `bang-9-nguon-bien.tsv` có đúng 8 dòng dữ liệu, mỗi dòng ≥ 8 cột, mọi ô `nac_thang` khác rỗng, và có dòng ghi phiên bản đã đo.**

```bash
awk -F'\t' '
  /^# phien ban:/ { if ($0 !~ /DIEN-VAO-DAY/) pv=1 }
  /^#/ { next }
  $1 == "cap" { next }
  NF >= 8 { n++; if ($6 == "" || $6 == "-") xau++; if ($1 !~ /^[0-9]+-[0-9]+$/) xau++ }
  END {
    if (n == 8 && xau+0 == 0 && pv == 1)
      print "CHECKPOINT 1 — ĐẠT (" n " dòng dữ liệu, 8 khe kề nhau, mọi nấc thắng đo được, có dòng phiên bản)"
    else
      print "CHECKPOINT 1 — LỖI (" n+0 " dòng, " xau+0 " ô sai, dòng phiên bản=" pv+0 " — kỳ vọng 8/0/1)"
  }' ~/lab06/bang-9-nguon-bien.tsv | tee -a ~/lab06/checkpoint.log
```

Từ đây trở đi **mọi** đoạn checkpoint đều kết thúc bằng `| tee -a ~/lab06/checkpoint.log`. Hiện vật nộp số 9 đòi đủ **12** dòng `ĐẠT`, theo thứ tự.

### 1.5. Nấc 2 thắng nấc 7 — và danh sách "bom hẹn giờ" của repo (3 phút)

Bảng tám khe cho ta thứ tự. Việc còn lại là biến thứ tự đó thành một **thao tác chẩn đoán** dùng được lúc 2 giờ sáng: cho một repo bất kỳ, liệt kê những tên biến khai ở **cả** YAML và project variable. Mỗi dòng trong danh sách đó là một ca QT 4.2 chờ nổ.

```bash
cd ~/lab06
bash dat-bien.sh dat MOI_TRUONG project >/dev/null
cat > .gitlab-ci.yml <<'YML'
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH'
variables:
  MOI_TRUONG: "yaml"
  MUC_LOG: "info"
in-moi-truong:
  image: alpine:3.20
  script:
    - 'echo "MOI_TRUONG=[$MOI_TRUONG] MUC_LOG=[$MUC_LOG]"'
YML
git add -A && git commit -q -m "ca 1: yaml so project" --allow-empty
PIPE_A=$(day_nhanh do-nac "ca 1")
cho_pipeline "$PIPE_A"

grep -nE '^[[:space:]]{2,}[A-Z_][A-Z0-9_]*:' .gitlab-ci.yml \
  | awk -F: '{print $2}' | tr -d ' ' | sort -u > /tmp/yaml.txt
bash dat-bien.sh liet-ke | awk -F'\t' '{print $5}' | jq -r '.[].key' | sort -u > /tmp/project.txt
comm -12 /tmp/yaml.txt /tmp/project.txt | tee /tmp/bom.txt
```

**CHECKPOINT 2 — nấc 2 thắng nấc 7: job in `project` chứ không phải `yaml`, biến chỉ có ở YAML thì còn nguyên, và `comm -12` chỉ ra đúng 1 tên biến.**

```bash
J=$(job_id "$PIPE_A" "in-moi-truong")
DONG=$(job_log_sach "$J" | grep -oE 'MOI_TRUONG=\[[^]]*\] MUC_LOG=\[[^]]*\]' | head -1)
mt=$(echo "$DONG" | sed 's/.*MOI_TRUONG=\[\([^]]*\)\].*/\1/')
ml=$(echo "$DONG" | sed 's/.*MUC_LOG=\[\([^]]*\)\].*/\1/')
nbom=$(wc -l < /tmp/bom.txt | tr -d ' ')
{ [ "$mt" = "project" ] && [ "$ml" = "info" ] && [ "$nbom" -eq 1 ]; } \
  && echo "CHECKPOINT 2 — ĐẠT (MOI_TRUONG=$mt tức nấc 2 thắng nấc 7; MUC_LOG=$ml còn nguyên; $nbom tên biến trong danh sách bom hẹn giờ)" \
  || echo "CHECKPOINT 2 — LỖI (MOI_TRUONG=$mt, MUC_LOG=$ml, bom=$nbom — kỳ vọng project/info/1)" \
  | tee -a ~/lab06/checkpoint.log
```

`MUC_LOG` vẫn in `info` là nửa quan trọng thứ hai của checkpoint này: nấc 2 **không** thay cả khối `variables`, nó chỉ thắng ở đúng tên biến nó có. Đó là QT 4.4 nhìn từ phía trên.

### 1.6. `variables` cấp job hợp nhất theo tên biến, và công tắc `inherit` (2 phút)

```bash
cd ~/lab06
cat > .gitlab-ci.yml <<'YML'
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH'
variables:
  DANG_KY: "jfrog.lab/ntkgitlab"
  MOI_TRUONG_YAML: "dev"
  MUC_LOG: "info"
.in-ba: &in-ba
  image: alpine:3.20
  script:
    - 'echo "DEM=$(env | grep -cE "^(DANG_KY|MOI_TRUONG_YAML|MUC_LOG)=") MOI_TRUONG_YAML=[$MOI_TRUONG_YAML]"'
in-ba-bien:
  <<: *in-ba
  variables:
    MOI_TRUONG_YAML: "staging"
in-ba-bien-tat-ke-thua:
  <<: *in-ba
  inherit:
    variables: false
  variables:
    MOI_TRUONG_YAML: "staging"
YML
git add -A && git commit -q -m "QT 4.4" --allow-empty
PIPE_B=$(day_nhanh do-nac "QT 4.4"); cho_pipeline "$PIPE_B"
```

**CHECKPOINT 3 — hợp nhất theo tên biến: job thường thấy 3 biến (1 bị ghi đè, 2 còn nguyên), job `inherit:variables: false` chỉ thấy 1.**

```bash
lay() { job_log_sach "$(job_id "$PIPE_B" "$1")" | grep -oE 'DEM=[0-9]+ MOI_TRUONG_YAML=\[[^]]*\]' | head -1; }
d1=$(lay in-ba-bien);            n1=$(echo "$d1" | grep -oE 'DEM=[0-9]+' | cut -d= -f2)
d2=$(lay in-ba-bien-tat-ke-thua); n2=$(echo "$d2" | grep -oE 'DEM=[0-9]+' | cut -d= -f2)
v1=$(echo "$d1" | sed 's/.*\[\([^]]*\)\]/\1/')
{ [ "$n1" -eq 3 ] && [ "$n2" -eq 1 ] && [ "$v1" = "staging" ]; } \
  && echo "CHECKPOINT 3 — ĐẠT (job thường: $n1 biến, MOI_TRUONG_YAML=$v1 — 1 ghi đè 2 còn nguyên; job tắt kế thừa: $n2 biến)" \
  || echo "CHECKPOINT 3 — LỖI (n1=$n1 v1=$v1 n2=$n2 — kỳ vọng 3/staging/1)" \
  | tee -a ~/lab06/checkpoint.log
```

Chênh lệch **3** so **1** là con số đáng nhớ nhất của QT 4.4: `variables` cấp job là **thay thế từng khoá**, còn `inherit:variables: false` là **công tắc tắt cả nấc 7**. Hai thứ khác nhau, nằm cách nhau ba dòng YAML.

---

## L4. Bước 2 — Ca 1 và ca 2: YAML vô hiệu · biến `protected` rỗng (30 phút)

Kiểm chứng QT 4.2, QT 5.2.

Đây là bước **không bao giờ được cắt**. Nó là chỗ duy nhất trong cả khoá học viên thấy tận mắt một job deploy **XANH** với `${#TOKEN}` = **0**, và nó là lý do của mọi dòng `: "${VAR:?}"` trong 42 buổi còn lại.

### 2.1. Dựng biến cho hai ca (4 phút)

Ba biến, ba mục đích khác nhau. `TOKEN` là biến `protected` và `masked` — 20 ký tự hex, thoả điều kiện của QT 5.3 nên bật được cả hai cờ:

```bash
cd ~/lab06
TOKEN_THAT=$(head -c10 /dev/urandom | od -An -tx1 | tr -d ' \n')
echo "TOKEN_THAT=$TOKEN_THAT  do dai=${#TOKEN_THAT}"      # phải là 20
echo "export TOKEN_THAT=$TOKEN_THAT" >> ~/.gitlab-lab.env

bash dat-bien.sh dat TOKEN "$TOKEN_THAT" --masked --protected
bash dat-bien.sh dat MOI_TRUONG project
bash dat-bien.sh liet-ke | awk -F'\t' '{print $5}' | jq -r '.[] | "\(.key)\tmasked=\(.masked)\tprotected=\(.protected)"'
```

Ba dòng đầu ra cuối cùng là bản kê **ý định**; nó chưa chứng minh gì. Ý định `protected=true` chỉ có nghĩa khi đối chiếu với **danh sách nhánh được bảo vệ**, và danh sách đó phải lấy từ API chứ không lấy từ trí nhớ:

```bash
curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/protected_branches" | jq -r '.[] | .name'
# Phải thấy 'main'. Nhánh 'feature-06' ta sắp tạo KHÔNG có trong danh sách này.
```

### 2.2. Ca 1 — sửa YAML ba lần mà job vẫn in giá trị cũ (8 phút)

Ca 1 là ca **đắt về thời gian người**, không đắt về phút runner. Ta tái hiện đúng triệu chứng mà đề bài thực tế đưa ra: `git log -p` cho thấy giá trị đã đổi ba lần, job vẫn in một giá trị **không tồn tại ở bất cứ đâu trong repo**.

```bash
cd ~/lab06
git checkout -q -B feature-06
cat > .gitlab-ci.yml <<'YML'
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH'
variables:
  MOI_TRUONG: "yaml-lan-1"
deploy-khong-khang-dinh:
  image: alpine:3.20
  script:
    - 'echo "MOI_TRUONG=[$MOI_TRUONG]"'
    - 'echo "do dai TOKEN = ${#TOKEN}"'
    - apk add --no-cache curl >/dev/null 2>&1
    - 'curl -s -o /dev/null -w "goi API voi token: HTTP %{http_code}\n" --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/user" || true'
    - 'echo "DEPLOY XONG"'
deploy-co-khang-dinh:
  image: alpine:3.20
  script:
    - ': "${TOKEN:?thiếu TOKEN — nhánh này chưa được bảo vệ}"'
    - 'echo "do dai TOKEN = ${#TOKEN}"'
    - 'echo "DEPLOY XONG"'
YML
git add -A && git commit -q -m "sua YAML lan 1"
for lan in 2 3; do
  sed -i "s/yaml-lan-[0-9]/yaml-lan-$lan/" .gitlab-ci.yml
  git add -A && git commit -q -m "sua YAML lan $lan"
done
git log --oneline -3
git grep -n 'MOI_TRUONG:' HEAD -- .gitlab-ci.yml      # trong repo chỉ có 'yaml-lan-3'
PIPE_C=$(day_nhanh feature-06 "ba lan sua yaml")
cho_pipeline "$PIPE_C"
```

`git grep` khẳng định repo chỉ chứa `yaml-lan-3`. Giá trị job sắp in ra là `project` — một chuỗi **chưa bao giờ** ở trong repo, kể cả trong lịch sử git. Đó là toàn bộ nội dung của câu "tôi sửa YAML mà không có tác dụng gì": người sửa đọc một nguồn sự thật, nền tảng đọc một nguồn khác, và **không ai sai**.

### 2.3. Ca 2 — biến `protected` rỗng, và hai job đối chứng (12 phút)

Cùng một pipeline vừa chạy ở trên đã chứa cả hai job đối chứng. Đọc bảng job trước khi đọc log — hai dòng này là bảng hai thuộc tính hỏng (buổi 01 QT 7.1) hiện ra thành hai màu:

```bash
job_bang "$PIPE_C"
```

```bash
JK=$(job_id "$PIPE_C" "deploy-khong-khang-dinh")
JC=$(job_id "$PIPE_C" "deploy-co-khang-dinh")
job_log_sach "$JK" | grep -E 'MOI_TRUONG=|do dai TOKEN|HTTP|DEPLOY XONG'
echo "--- job có khẳng định ---"
job_log_sach "$JC" | tail -5
```

**CHECKPOINT 4 — trong MỘT job XANH có đồng thời hai ca hỏng im lặng: nấc 2 ghi đè YAML (`MOI_TRUONG=project`) và biến `protected` rỗng (`${#TOKEN}` = 0), mà job vẫn chạy tới dòng cuối.**

```bash
st=$(job_tt "$JK")
L=$(job_log_sach "$JK")
mt=$(echo "$L" | grep -oE 'MOI_TRUONG=\[[^]]*\]' | head -1 | sed 's/.*\[\([^]]*\)\]/\1/')
dl=$(echo "$L" | grep -oE 'do dai TOKEN = [0-9]+' | head -1 | awk '{print $NF}')
http=$(echo "$L" | grep -oE 'goi API voi token: HTTP [0-9]+' | head -1 | awk '{print $NF}')
xong=$(echo "$L" | grep -c 'DEPLOY XONG')
{ [ "$st" = "success" ] && [ "$mt" = "project" ] && [ "$dl" -eq 0 ] && [ "$xong" -eq 1 ]; } \
  && echo "CHECKPOINT 4 — ĐẠT (status=$st, MOI_TRUONG=$mt tức nấc 2 thắng nấc 7, do dai TOKEN=$dl, API tra HTTP=$http, vẫn in DEPLOY XONG $xong lần — IM LẶNG, KHÔNG CHẶN)" \
  || echo "CHECKPOINT 4 — LỖI (status=$st, MOI_TRUONG=$mt, do dai=$dl, DEPLOY XONG=$xong — kỳ vọng success/project/0/1)" \
  | tee -a ~/lab06/checkpoint.log
```

Bốn con số trong dòng `ĐẠT` là bốn thứ phải nhớ. `status=success`: nền tảng hài lòng. `do dai TOKEN=0`: biến `protected` **không tồn tại** trên nhánh này, và shell thay biến chưa đặt bằng chuỗi rỗng chứ không báo lỗi. `HTTP=401`: `curl` đi tới đúng địa chỉ với header rỗng, nhận 401, rồi trả **mã thoát 0** nên `script` không đỏ. `DEPLOY XONG` in ra **1** lần: job chạy hết, tự tin, và không deploy gì.

**CHECKPOINT 5 — ca đối chứng PHẢI THẤT BẠI: `deploy-co-khang-dinh` ĐỎ ngay dòng đầu, và lệnh thứ hai không bao giờ chạy.**

```bash
sc=$(job_tt "$JC")
LC=$(job_log_sach "$JC")
kd=$(echo "$LC" | grep -c 'thiếu TOKEN')
sau=$(echo "$LC" | grep -c 'DEPLOY XONG')
dodai2=$(echo "$LC" | grep -c 'do dai TOKEN')
{ [ "$sc" = "failed" ] && [ "$kd" -ge 1 ] && [ "$sau" -eq 0 ] && [ "$dodai2" -eq 0 ]; } \
  && echo "CHECKPOINT 5 — ĐẠT (status=$sc, $kd dòng khẳng định, 0 dòng DEPLOY XONG, 0 dòng lệnh thứ hai — ỒN ÀO, CÓ CHẶN)" \
  || echo "CHECKPOINT 5 — LỖI (status=$sc, khẳng định=$kd, DEPLOY XONG=$sau, lệnh 2=$dodai2 — job này PHẢI đỏ)" \
  | tee -a ~/lab06/checkpoint.log
```

Hai checkpoint vừa rồi khác nhau đúng **một dòng** `: "${TOKEN:?...}"`. Chi phí của dòng đó: khoảng **0,01 giây** — nó là một phép mở rộng biến trong shell, không gọi mạng, không đọc đĩa. Đổi lại, ô của bảng hai thuộc tính đi từ *im lặng — không chặn* sang *ồn ào — có chặn*. Đây là lần thứ **4** khoá này nói "job xanh không chứng minh gì".

Đối chứng cuối cùng: cùng hai job đó trên nhánh **mặc định**, nơi biến `protected` **có** mặt.

```bash
cd ~/lab06 && git checkout -q main
git checkout -q feature-06 -- .gitlab-ci.yml
PIPE_D=$(day "chay tren nhanh duoc bao ve")
cho_pipeline "$PIPE_D"
for n in deploy-khong-khang-dinh deploy-co-khang-dinh; do
  J=$(job_id "$PIPE_D" "$n")
  printf '%-26s %-8s %s\n' "$n" "$(job_tt "$J")" \
    "$(job_log_sach "$J" | grep -oE 'do dai TOKEN = [0-9]+' | head -1)"
done
```

Hai dòng đầu ra phải cho `success` và `do dai TOKEN = 20` cho **cả hai** job. Cùng một YAML, cùng một runner, cùng một biến — khác nhau đúng ở chỗ nhánh có được bảo vệ hay không. **20 so với 0**, và không có dòng log nào ở nhánh feature nói rằng con số đáng ra là 20.

### 2.4. Hai ca đầu tiên vào `nam-ca-bien-sai.md` (6 phút)

Hiện vật này là hiện vật cốt lõi thứ hai. Mỗi ca đúng **bốn** dòng, và dòng thứ hai phải là **một lệnh in ra được** — không phải một câu văn. Ba tháng sau, câu văn không kiểm lại được, còn lệnh thì kiểm được kể cả khi pipeline đã đổi hết.

```bash
cat > ~/lab06/nam-ca-bien-sai.md <<'MD'
# Năm ca "biến không có giá trị đúng" — đo trên GitLab CE 17.7 · Runner 17.7 · executor docker

Mẫu bốn dòng: triệu chứng · bằng chứng bằng LỆNH · nguyên nhân theo NẤC · cách sửa.

## Ca 1 — sửa YAML ba lần mà job vẫn in giá trị cũ

- **Triệu chứng:** `git log -p .gitlab-ci.yml` cho thấy `MOI_TRUONG` đã đổi ba lần thành `yaml-lan-3`; job in ra `project`, một chuỗi không có trong repo.
- **Bằng chứng:** `$ comm -12 <(grep -oE '^  [A-Z_]+:' .gitlab-ci.yml | tr -d ' :') <(bash dat-bien.sh liet-ke | awk -F'\t' '{print $5}' | jq -r '.[].key')` -> in ra `MOI_TRUONG`
- **Nguyên nhân:** nấc **2** (project variable) thắng nấc **7** (`variables` cấp trên cùng). Bốn nấc cao nhất nằm ngoài repo nên `git log` không thấy chúng.
- **Cách sửa:** xoá project variable nếu giá trị thuộc về mã nguồn (`bash dat-bien.sh xoa MOI_TRUONG`), hoặc bỏ khai báo trong YAML nếu giá trị thuộc về vận hành. Không giữ cả hai.

## Ca 2 — job deploy XANH mà không deploy gì

- **Triệu chứng:** job `deploy-khong-khang-dinh` trên nhánh `feature-06` `success`, in đủ `DEPLOY XONG`, nhưng lời gọi API nhận `401`.
- **Bằng chứng:** `$ job_log_sach $JK | grep -E 'do dai TOKEN|HTTP'` -> `do dai TOKEN = 0` và `HTTP 401`; cùng job đó trên `main` cho `do dai TOKEN = 20`
- **Nguyên nhân:** biến `TOKEN` có `protected=true`; nhánh `feature-06` không nằm trong `GET /projects/:id/protected_branches`, nên nền tảng **không gửi** biến. Shell thay biến chưa đặt bằng chuỗi rỗng.
- **Cách sửa:** thêm `: "${TOKEN:?thiếu TOKEN}"` vào dòng đầu `script` — **0,01 giây**, đổi ô bảng hai thuộc tính từ im lặng không chặn sang ồn ào có chặn. Nếu nhánh feature thật sự cần deploy thì bảo vệ nhánh đó, đừng bỏ cờ `protected`.
MD
grep -c '^- \*\*' ~/lab06/nam-ca-bien-sai.md      # phải là 8 (2 ca × 4 dòng)
```

---

## L5. Bước 3 — `masked` che gì và không che gì; điều kiện bật (25 phút)

Kiểm chứng QT 5.1, QT 5.3.

Cơ chế của `masked` là **một** phép thay thế chuỗi trên đường log đi từ runner về server. Cả bước này là việc rút ba hệ quả ra khỏi một câu đó, và **đo** từng hệ quả — vì hành vi masking đã bị siết dần qua các bản 15.x–17.x nên đây là đại lượng loại (c), phải đo, không tra.

### 3.1. Ba đường lộ, và bằng chứng là artifact tải về được (12 phút)

```bash
cd ~/lab06 && git checkout -q -B lo-masked
cat > .gitlab-ci.yml <<'YML'
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH'
lo-ba-duong:
  image: alpine:3.20
  script:
    - 'echo "duong 1 truc tiep: $TOKEN"'
    - 'echo -n "$TOKEN" | base64 > duong2.txt && echo "duong 2 base64: $(cat duong2.txt)"'
    - 'echo "TOKEN=$TOKEN" > ro-ri.env'
    - 'echo "duong 3: da ghi $(wc -c < ro-ri.env) byte vao artifact"'
  artifacts:
    paths: [ro-ri.env, duong2.txt]
YML
git add -A && git commit -q -m "ba duong lo cua masked" --allow-empty
PIPE_E=$(day_nhanh lo-masked "ba duong lo")
cho_pipeline "$PIPE_E"
JE=$(job_id "$PIPE_E" "lo-ba-duong")
job_log_sach "$JE" | grep -E 'duong [123]'
```

Biến `TOKEN` là biến `protected`, mà `lo-masked` không phải nhánh được bảo vệ — nên nếu chạy nguyên như trên thì `TOKEN` rỗng và cả phép đo vô nghĩa. Đó là bẫy thứ nhất của bước này, và cách thoát là tạo một biến **chỉ masked, không protected** riêng cho phép đo:

```bash
bash ~/lab06/dat-bien.sh dat TOKEN "$TOKEN_THAT" --masked          # bỏ --protected
bash ~/lab06/dat-bien.sh liet-ke | awk -F'\t' '{print $5}' | jq -r '.[] | select(.key=="TOKEN")'
PIPE_E=$(day_nhanh lo-masked "chay lai voi TOKEN chi masked")
cho_pipeline "$PIPE_E"; JE=$(job_id "$PIPE_E" "lo-ba-duong")
job_log_sach "$JE" | grep -E 'duong [123]'
```

Giờ đọc ba dòng đó theo đúng ba câu hỏi. Đường 1 phải hiện `[MASKED]`. Đường 2 hiện một chuỗi base64 **nguyên vẹn** — nó không còn giống chuỗi gốc nên phép thay thế không khớp. Đường 3 không in giá trị ra log, nhưng giá trị đã nằm trong tệp; và tệp đó lên server qua đường **artifact**, không qua đường log.

Chứng minh đường 2 và đường 3 bằng hiện vật, không bằng mắt:

```bash
art_tep "$JE" "duong2.txt" | base64 -d > /tmp/giai-ma.txt; cat /tmp/giai-ma.txt; echo
art_tep "$JE" "ro-ri.env"  > /tmp/ro-ri.env; cat /tmp/ro-ri.env
grep -c "$TOKEN_THAT" /tmp/ro-ri.env /tmp/giai-ma.txt
```

**CHECKPOINT 6 — `masked` bịt đường log và KHÔNG bịt hai đường còn lại: log có 0 lần giá trị gốc, còn artifact tải về có 1 lần ở mỗi đường.**

```bash
LG=$(job_log_sach "$JE")
n_log=$(echo "$LG" | grep -c "$TOKEN_THAT" || true)
n_mask=$(echo "$LG" | grep -c 'MASKED' || true)
art_tep "$JE" "ro-ri.env"  > /tmp/ro-ri.env
art_tep "$JE" "duong2.txt" | base64 -d > /tmp/giai-ma.txt
n_art=$(grep -c "$TOKEN_THAT" /tmp/ro-ri.env || true)
n_b64=$(grep -c "$TOKEN_THAT" /tmp/giai-ma.txt || true)
{ [ "$n_log" -eq 0 ] && [ "$n_mask" -ge 1 ] && [ "$n_art" -eq 1 ] && [ "$n_b64" -eq 1 ]; } \
  && echo "CHECKPOINT 6 — ĐẠT (log: $n_log lần giá trị gốc và $n_mask dòng MASKED; artifact ro-ri.env: $n_art lần; base64 giải mã: $n_b64 lần — 1 cơ chế, 3 đường lộ)" \
  || echo "CHECKPOINT 6 — LỖI (log=$n_log mask=$n_mask artifact=$n_art base64=$n_b64 — kỳ vọng 0/≥1/1/1)" \
  | tee -a ~/lab06/checkpoint.log
```

Đường lộ thứ ba mà lệnh trên **không** kiểm được là giao diện: ai có quyền Maintainer đều bấm "Reveal value" đọc được giá trị nguyên văn. Nó không đo bằng `grep` nên nó nằm trong hiện vật dưới dạng một câu và một tham chiếu API — `GET /projects/:id/variables/TOKEN` trả về `value` nguyên văn cho token có scope `api`. Thử ngay:

```bash
curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/variables/TOKEN" | jq -r '.value' | head -c 8; echo "..."
```

Ba đường lộ, một dòng lệnh mỗi đường. Đó là lý do câu "`masked` không phải bảo vệ secret" là **trần điểm 1** ở vấn đáp nếu học viên nói ngược lại.

### 3.2. Điều kiện bật `masked` — ca đối chứng phải bị API từ chối (8 phút)

Bật được `masked` là ràng buộc lên **giá trị**, không lên ý muốn. Ba giá trị, hai cái đầu **phải** bị từ chối. Đây là ca đối chứng thứ hai của buổi và mã HTTP là dữ liệu:

```bash
cd ~/lab06
{
  printf 'gia_tri\tdo_dai\tso_dong\tso_khoang_trang\thttp\tthong_diep\n'
  while IFS= read -r v; do
    ma=$(bash dat-bien.sh dat THU_MASKED "$v" --masked | awk -F'\t' '{print $4"\t"$5}')
    printf '%s\t%s\t%s\t%s\t%s\n' "[$v]" "${#v}" \
      "$(printf '%s' "$v" | wc -l | tr -d ' ')" \
      "$(printf '%s' "$v" | tr -cd ' ' | wc -c | tr -d ' ')" "$ma"
    bash dat-bien.sh xoa THU_MASKED >/dev/null 2>&1
  done <<'EOF'
abc
mot hai ba
a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
EOF
} | tee /tmp/dieu-kien-masked.tsv
```

Hai dòng đầu phải cho HTTP **400** kèm thông báo về định dạng; dòng thứ ba cho **201**. Giờ đo **ngưỡng độ dài thật** thay vì tin con số 8 trong tài liệu — thử lần lượt 6, 7, 8, 9 ký tự và tìm chỗ mã HTTP đổi:

```bash
for n in 6 7 8 9; do
  v=$(head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n' | cut -c1-$n)
  ma=$(bash ~/lab06/dat-bien.sh dat THU_NGUONG "$v" --masked | awk -F'\t' '{print $4}')
  printf 'do dai %s -> HTTP %s\n' "$n" "$ma"
  bash ~/lab06/dat-bien.sh xoa THU_NGUONG >/dev/null 2>&1
done
```

**CHECKPOINT 7 — API từ chối `masked` cho hai giá trị đầu (HTTP 400) và nhận giá trị thứ ba (HTTP 201); ngưỡng độ dài đo được là 8.**

```bash
m1=$(awk -F'\t' 'NR==2{print $5}' /tmp/dieu-kien-masked.tsv)
m2=$(awk -F'\t' 'NR==3{print $5}' /tmp/dieu-kien-masked.tsv)
m3=$(awk -F'\t' 'NR==4{print $5}' /tmp/dieu-kien-masked.tsv)
n7=$(v=$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n' | cut -c1-7); \
     bash ~/lab06/dat-bien.sh dat THU_NGUONG "$v" --masked | awk -F'\t' '{print $4}')
bash ~/lab06/dat-bien.sh xoa THU_NGUONG >/dev/null 2>&1
n8=$(v=$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n' | cut -c1-8); \
     bash ~/lab06/dat-bien.sh dat THU_NGUONG "$v" --masked | awk -F'\t' '{print $4}')
bash ~/lab06/dat-bien.sh xoa THU_NGUONG >/dev/null 2>&1
{ [ "$m1" = 400 ] && [ "$m2" = 400 ] && [ "$m3" = 201 ] && [ "$n7" = 400 ] && [ "$n8" = 201 ]; } \
  && echo "CHECKPOINT 7 — ĐẠT (abc=$m1, 'mot hai ba'=$m2, 32 hex=$m3; 7 ký tự=$n7, 8 ký tự=$n8 — ngưỡng đo được là 8 ký tự, 1 dòng, 0 khoảng trắng)" \
  || echo "CHECKPOINT 7 — LỖI (m1=$m1 m2=$m2 m3=$m3 n7=$n7 n8=$n8 — kỳ vọng 400/400/201/400/201)" \
  | tee -a ~/lab06/checkpoint.log
```

Con số **8** vừa đo là con số của **instance này, phiên bản này**. Nó đã đổi nhiều lần trong dòng 15.x–17.x, nên đừng chép nó vào tài liệu nội bộ của đội — chép **đoạn lệnh** vào, để lần sau đo lại trong 20 giây. Và khi một secret không thoả điều kiện thì việc phải làm là **đổi secret**, không phải bỏ `masked`: bỏ `masked` nghĩa là từ hôm ấy mọi log của mọi job có biến đó đều chứa secret nguyên văn, không cảnh báo, không job đỏ, không tín hiệu nào.

### 3.3. `masked-lo.md` (5 phút)

```bash
cat > ~/lab06/masked-lo.md <<MD
# masked che gì và không che gì — đo trên GitLab CE $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)

Cơ chế: **1** phép thay thế chuỗi trên đường log runner -> server. Ba đường dưới đây
KHÔNG đi qua đường đó, hoặc không còn giống chuỗi gốc, nên không được thay thế.

| # | Đường | Đo bằng lệnh | Kết quả |
|---|---|---|---|
| 0 | log trực tiếp — ĐƯỢC che | \`job_log_sach \$JE | grep -c "\$TOKEN_THAT"\` | **0** lần, và có dòng \`[MASKED]\` |
| 1 | qua \`base64\` | \`art_tep \$JE duong2.txt | base64 -d | grep -c "\$TOKEN_THAT"\` | **1** lần — chuỗi đã đổi nên không khớp |
| 2 | vào artifact | \`art_tep \$JE ro-ri.env | grep -c "\$TOKEN_THAT"\` | **1** lần — artifact lên server bằng đường khác |
| 3 | qua API biến | \`curl "\$GITLAB/api/v4/projects/\$PID/variables/TOKEN" | jq -r .value\` | trả **nguyên văn** cho token scope \`api\` |

## Điều kiện bật masked, đo bằng mã HTTP của POST /projects/:id/variables

| Giá trị | Độ dài | Số dòng | Khoảng trắng | HTTP |
|---|---|---|---|---|
| \`abc\` | 3 | 1 | 0 | **400** |
| \`mot hai ba\` | 10 | 1 | 2 | **400** |
| 32 ký tự hex | 32 | 1 | 0 | **201** |
| 7 ký tự hex | 7 | 1 | 0 | **400** |
| 8 ký tự hex | 8 | 1 | 0 | **201** |

Ngưỡng đo được: >= **8** ký tự, **1** dòng, **0** khoảng trắng. Con số 8 KHÔNG phổ quát —
đã đổi nhiều lần trong dòng 15.x-17.x. Secret không thoả thì **đổi secret**, không bỏ masked.

Kết luận: \`masked\` giảm rủi ro rò rỉ **tình cờ qua log**, và chỉ thế. Secret thật cần
vòng đời ngắn sinh lúc chạy — buổi 29 (Vault, OIDC).
MD
grep -c '^|' ~/lab06/masked-lo.md
```

---

## L6. Bước 4 — Ca 3, 4, 5: biến file · ký tự vô hình · mở rộng biến (30 phút)

Kiểm chứng QT 6.1, QT 6.2, QT 6.3.

Ba ca của bước này là một họ: cả ba đều là "giá trị tới nơi **không phải** giá trị tôi đặt". Ca 3 tới nơi là **đường dẫn** thay vì nội dung; ca 4 dài hơn **1** byte; ca 5 ngắn đi **2** ký tự. Không ca nào sinh ra một dòng log có chữ "lỗi".

### 4.1. Ca 3 — `type: file`: `$VAR` là đường dẫn, nội dung ở `$(cat $VAR)` (10 phút)

Hai biến, cùng một nội dung, khác nhau đúng ở cờ `--file`:

```bash
cd ~/lab06
cat > /tmp/kubeconfig.yaml <<'YML'
apiVersion: v1
kind: Config
clusters:
  - name: lab
    cluster: {server: https://k8s.lab:6443}
contexts:
  - name: lab
    context: {cluster: lab, user: lab}
current-context: lab
YML
wc -l /tmp/kubeconfig.yaml           # 10 dòng — con số sẽ dùng ở checkpoint
bash dat-bien.sh dat KUBECONFIG_FILE "$(cat /tmp/kubeconfig.yaml)" --file
bash dat-bien.sh dat KUBECONFIG_TEXT "$(cat /tmp/kubeconfig.yaml)"
```

```bash
cd ~/lab06 && git checkout -q -B ca-345
cat > .gitlab-ci.yml <<'YML'
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH'
so-hai-kieu:
  image: alpine:3.20
  script:
    - apk add --no-cache jq >/dev/null
    - |
      DUONG_DAN="$KUBECONFIG_FILE"
      jq -n \
        --arg dd "$DUONG_DAN" \
        --argjson ton_tai "$( [ -f "$KUBECONFIG_FILE" ] && echo true || echo false )" \
        --argjson so_dong_file "$(wc -l < "$KUBECONFIG_FILE" 2>/dev/null || echo 0)" \
        --argjson so_dong_text "$(printf '%s' "$KUBECONFIG_TEXT" | wc -l)" \
        --argjson text_la_tep "$( [ -f "$KUBECONFIG_TEXT" ] && echo true || echo false )" \
        '{duong_dan:$dd, duong_dan_ton_tai:$ton_tai, so_dong_file:$so_dong_file,
          so_dong_text:$so_dong_text, text_la_tep:$text_la_tep}' > kieu-bien.json
      cat kieu-bien.json
    # Triệu chứng ĐỐI XỨNG 1 — dùng biến FILE ở chỗ cần nội dung: in ra một đường dẫn
    - 'echo "sai chieu 1: $KUBECONFIG_FILE"'
    # Triệu chứng ĐỐI XỨNG 2 — dùng biến THƯỜNG ở chỗ cần tệp: công cụ mở một chuỗi YAML như tên tệp
    - 'cat "$KUBECONFIG_TEXT" 2>&1 | head -1 || true'
  artifacts:
    paths: [kieu-bien.json]
YML
git add -A && git commit -q -m "ca 3: type file" --allow-empty
PIPE_F=$(day_nhanh ca-345 "ca 3"); cho_pipeline "$PIPE_F"
JF=$(job_id "$PIPE_F" "so-hai-kieu")
job_log_sach "$JF" | grep -E 'sai chieu|No such file|kubeconfig'
```

**CHECKPOINT 8 — biến `type: file` cho ĐƯỜNG DẪN tồn tại với 10 dòng nội dung; biến thường cho 10 dòng ngay trong giá trị và KHÔNG phải một tệp.**

```bash
art_tep "$JF" "kieu-bien.json" > /tmp/kieu-bien.json
jq . /tmp/kieu-bien.json
dd=$(jq -r '.duong_dan' /tmp/kieu-bien.json)
tt=$(jq -r '.duong_dan_ton_tai' /tmp/kieu-bien.json)
sdf=$(jq -r '.so_dong_file' /tmp/kieu-bien.json)
sdt=$(jq -r '.so_dong_text' /tmp/kieu-bien.json)
tlt=$(jq -r '.text_la_tep' /tmp/kieu-bien.json)
{ [ "$tt" = true ] && [ "$tlt" = false ] && [ "$sdf" -eq 10 ] && [ "$sdt" -eq 10 ] \
  && case "$dd" in /*) true ;; *) false ;; esac; } \
  && echo "CHECKPOINT 8 — ĐẠT (kiểu file: đường dẫn=$dd tồn tại=$tt nội dung=$sdf dòng; kiểu thường: là tệp=$tlt, giá trị có $sdt dòng — 2 kiểu, 2 triệu chứng đối xứng)" \
  || echo "CHECKPOINT 8 — LỖI (dd=$dd tt=$tt sdf=$sdf sdt=$sdt tlt=$tlt — kỳ vọng /... /true/10/10/false)" \
  | tee -a ~/lab06/checkpoint.log
```

Chi phí của biến kiểu file: **1** tệp tạm mỗi biến trong thư mục job, và **0** giây thêm. Runner xoá tệp tạm ở pha dọn dẹp cuối job (buổi 01 QT 4.2), nên không cần tự `rm`.

### 4.2. Ca 4 — một byte vô hình đổi 200 thành 401 (10 phút)

Ta cần một token **thật và dùng được** để có 200, nhưng không được dùng token cá nhân của học viên. Cách đúng: một **project access token** scope `read_api`, hạn 2 ngày, thu hồi ở §L8.

```bash
cd ~/lab06
KQ=$(curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects/$PID/access_tokens" \
  --form 'name=lab06-ca4' --form 'scopes[]=read_api' \
  --form "expires_at=$(date -d '+2 days' +%F)")
PAT=$(echo "$KQ" | jq -r .token); PAT_ID=$(echo "$KQ" | jq -r .id)
echo "export PAT_ID=$PAT_ID" >> ~/.gitlab-lab.env
echo "do dai token sach = ${#PAT}"

# Bản SẠCH và bản BẨN — bản bẩn thừa đúng 1 ký tự xuống dòng cuối
bash dat-bien.sh dat TOKEN_SACH "$PAT"
bash dat-bien.sh dat TOKEN_BAN "$(printf '%s\n' "$PAT")"
bash dat-bien.sh liet-ke | awk -F'\t' '{print $5}' | jq -r '.[] | select(.key|startswith("TOKEN_")) | .key'
```

Một điểm dễ trượt: `--form "value=$(printf '%s\n' "$PAT")"` có thể bị `curl` cắt ký tự cuối. Nếu độ dài hai biến in ra bằng nhau ở bước sau, dùng đường vòng của §L9 dòng 8 — đặt giá trị bẩn bằng `--form-string` với `%0A` đã mã hoá, hoặc đặt bằng giao diện. Ca này chỉ có nghĩa khi hai độ dài **chênh nhau đúng 1**.

```bash
cat > .gitlab-ci.yml <<'YML'
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH'
chan-doan-1-byte:
  image: alpine:3.20
  script:
    - apk add --no-cache curl coreutils jq >/dev/null
    - 'echo "do dai: sach=${#TOKEN_SACH} ban=${#TOKEN_BAN}"'
    - printf %s "$TOKEN_BAN" | od -c | tail -2
    - |
      h_sach=$(curl -s -o /dev/null -w '%{http_code}' --header "PRIVATE-TOKEN: $TOKEN_SACH" "$GITLAB/api/v4/user")
      h_ban=$(curl -s -o /dev/null -w '%{http_code}' --header "PRIVATE-TOKEN: $TOKEN_BAN" "$GITLAB/api/v4/user")
      TOKEN_DON=$(printf %s "$TOKEN_BAN" | tr -d '\r\n')
      h_don=$(curl -s -o /dev/null -w '%{http_code}' --header "PRIVATE-TOKEN: $TOKEN_DON" "$GITLAB/api/v4/user")
      jq -n --argjson ds "${#TOKEN_SACH}" --argjson db "${#TOKEN_BAN}" --argjson dd "${#TOKEN_DON}" \
            --arg hs "$h_sach" --arg hb "$h_ban" --arg hd "$h_don" \
            '{do_dai_sach:$ds, do_dai_ban:$db, do_dai_don:$dd, http_sach:$hs, http_ban:$hb, http_don:$hd}' \
        > mot-byte.json
      cat mot-byte.json
  artifacts:
    paths: [mot-byte.json]
YML
git add -A && git commit -q -m "ca 4: mot byte vo hinh" --allow-empty
PIPE_G=$(day_nhanh ca-345 "ca 4"); cho_pipeline "$PIPE_G"
JG=$(job_id "$PIPE_G" "chan-doan-1-byte")
job_log_sach "$JG" | grep -A2 -E 'do dai:|0000'
```

**CHECKPOINT 9 — token bẩn dài hơn token sạch đúng 1 byte, và chênh lệch 1 byte đó đổi HTTP 200 thành 401; dọn `\r\n` đưa về 200.**

```bash
art_tep "$JG" "mot-byte.json" > /tmp/mot-byte.json
jq . /tmp/mot-byte.json
ds=$(jq -r .do_dai_sach /tmp/mot-byte.json); db=$(jq -r .do_dai_ban /tmp/mot-byte.json)
hs=$(jq -r .http_sach /tmp/mot-byte.json);   hb=$(jq -r .http_ban /tmp/mot-byte.json)
hd=$(jq -r .http_don /tmp/mot-byte.json)
{ [ "$db" -eq $((ds+1)) ] && [ "$hs" = 200 ] && [ "$hb" = 401 ] && [ "$hd" = 200 ]; } \
  && echo "CHECKPOINT 9 — ĐẠT (sach=$ds ban=$db tức thừa 1 byte; HTTP sach=$hs ban=$hb don=$hd — 1 byte đổi 200 thành 401)" \
  || echo "CHECKPOINT 9 — LỖI (ds=$ds db=$db hs=$hs hb=$hb hd=$hd — kỳ vọng db=ds+1 và 200/401/200)" \
  | tee -a ~/lab06/checkpoint.log
```

Giá trị tham chiếu của đề cương là **21** so với **20** cho một token 20 ký tự; project access token dài hơn thế, nên số đo của lớp sẽ khác. Điều **không** đổi là phép so: `db = ds + 1`. Ghi cả hai con số thật vào hiện vật, đừng ghi 20 và 21.

Hai lệnh chẩn đoán của cả ca này tốn **0,02 giây** cộng lại: `${#VAR}` và `od -c`. Chúng cắt được vài giờ đi kiểm quyền token, hạn dùng, firewall — vì `masked` che mất đúng chỗ ta cần nhìn, nên càng làm đúng bảo mật thì càng không chẩn đoán được bằng mắt.

### 4.3. Ca 5 — `Pa$$w0rd` tới nơi còn 6 ký tự (6 phút)

```bash
cd ~/lab06
bash dat-bien.sh dat MK_MO_RONG 'Pa$$w0rd'
bash dat-bien.sh dat MK_THO     'Pa$$w0rd' --no-expand
bash dat-bien.sh liet-ke | awk -F'\t' '{print $5}' | jq -r '.[] | select(.key|startswith("MK_")) | "\(.key) raw=\(.raw)"'

cat > .gitlab-ci.yml <<'YML'
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH'
so-mo-rong:
  image: alpine:3.20
  script:
    - apk add --no-cache jq coreutils >/dev/null
    - 'echo "MK_MO_RONG do dai=${#MK_MO_RONG}  MK_THO do dai=${#MK_THO}"'
    - printf %s "$MK_MO_RONG" | od -c | head -2
    - |
      jq -n --argjson a "${#MK_MO_RONG}" --argjson b "${#MK_THO}" \
            --arg va "$MK_MO_RONG" --arg vb "$MK_THO" \
            '{do_dai_mo_rong:$a, do_dai_tho:$b, hut:($b-$a), gt_mo_rong:$va, gt_tho:$vb}' > expand.json
      cat expand.json
  artifacts:
    paths: [expand.json]
YML
git add -A && git commit -q -m "ca 5: mo rong bien" --allow-empty
PIPE_H=$(day_nhanh ca-345 "ca 5"); cho_pipeline "$PIPE_H"
JH=$(job_id "$PIPE_H" "so-mo-rong")
```

**CHECKPOINT 10 — `Pa$$w0rd` khai thường tới nơi còn 6 ký tự, khai `--no-expand` (raw) giữ đủ 8; hụt đúng 2.**

```bash
art_tep "$JH" "expand.json" > /tmp/expand.json
jq . /tmp/expand.json
a=$(jq -r .do_dai_mo_rong /tmp/expand.json); b=$(jq -r .do_dai_tho /tmp/expand.json)
hut=$(jq -r .hut /tmp/expand.json)
{ [ "$b" -eq 8 ] && [ "$a" -eq 6 ] && [ "$hut" -eq 2 ]; } \
  && echo "CHECKPOINT 10 — ĐẠT (khai thường=$a ký tự, raw=$b ký tự, hụt=$hut — mở rộng biến đã ăn mất 2 ký tự, im lặng)" \
  || echo "CHECKPOINT 10 — LỖI (mo_rong=$a tho=$b hut=$hut — kỳ vọng 6/8/2)" \
  | tee -a ~/lab06/checkpoint.log
```

Nếu lớp đo ra `do_dai_mo_rong` bằng **8** chứ không phải 6 thì đó là **dữ liệu**, không phải lỗi bài lab: instance này xử lý `$$` như một dấu `$` được thoát. Ghi số đo được vào hiện vật kèm một dòng ghi rõ phiên bản, và đọc §L9 dòng 9. Điều không phụ thuộc phiên bản là **cách đo**: `${#VAR}` so với số ký tự đã dán, và `expand: false` (API `raw=true`) là công tắc tắt việc mở rộng cho đúng một biến.

### 4.4. Ba ca còn lại vào hiện vật (4 phút)

```bash
cat > ~/lab06/bien-file-va-expand.md <<MD
# Ba ca "giá trị tới nơi không phải giá trị tôi đặt" — GitLab CE 17.7 · Runner 17.7 · docker

| Ca | Đại lượng đo | Kỳ vọng tham chiếu | Đo được ở lớp |
|---|---|---|---|
| 3 — \`type: file\` | \`\$VAR\` là gì | đường dẫn tệp tạm | $(jq -r .duong_dan /tmp/kieu-bien.json) |
| 3 — \`type: file\` | số dòng \`\$(cat \$VAR)\` | 10 | $(jq -r .so_dong_file /tmp/kieu-bien.json) |
| 3 — biến thường | \`[ -f "\$VAR" ]\` | false | $(jq -r .text_la_tep /tmp/kieu-bien.json) |
| 4 — 1 byte vô hình | độ dài sạch / bẩn | chênh đúng 1 | $(jq -r .do_dai_sach /tmp/mot-byte.json) / $(jq -r .do_dai_ban /tmp/mot-byte.json) |
| 4 — 1 byte vô hình | HTTP sạch / bẩn / đã dọn | 200 / 401 / 200 | $(jq -r .http_sach /tmp/mot-byte.json) / $(jq -r .http_ban /tmp/mot-byte.json) / $(jq -r .http_don /tmp/mot-byte.json) |
| 5 — mở rộng biến | \`Pa\$\$w0rd\` khai thường | 6 ký tự | $(jq -r .do_dai_mo_rong /tmp/expand.json) |
| 5 — mở rộng biến | \`Pa\$\$w0rd\` khai raw | 8 ký tự | $(jq -r .do_dai_tho /tmp/expand.json) |

**Hai triệu chứng đối xứng của ca 3.** Dùng biến thường ở chỗ cần tệp: công cụ báo lỗi
phân tích cú pháp ở dòng 1 cột 1, vì nó vừa \`open()\` một chuỗi YAML dài như tên tệp.
Dùng biến file ở chỗ cần nội dung: công cụ nhận một dòng trông như đường dẫn — và đó
đúng là đường dẫn. Nhận ra **cặp** này là nhận ra cả lớp lỗi kubeconfig / service account
key / chứng chỉ ở buổi 39, 41, 42.

**Chi phí:** biến kiểu file tốn **1** tệp tạm mỗi biến và **0** giây thêm.
Hai lệnh chẩn đoán \`\${#VAR}\` và \`od -c\` tốn **0,02 giây** cộng lại.
MD
cat >> ~/lab06/nam-ca-bien-sai.md <<MD

## Ca 3 — công cụ báo lỗi cú pháp ở dòng 1 cột 1

- **Triệu chứng:** \`kubectl --kubeconfig "\$KUBECONFIG_TEXT"\` báo lỗi phân tích cú pháp ở đầu tệp; đổi sang \`\$KUBECONFIG_FILE\` thì chạy.
- **Bằng chứng:** \`\$ art_tep \$JF kieu-bien.json | jq '{duong_dan, duong_dan_ton_tai, text_la_tep}'\` -> \`duong_dan_ton_tai=true\`, \`text_la_tep=false\`
- **Nguyên nhân:** biến \`type: file\` đặt **đường dẫn** vào biến, nội dung ở \`\$(cat \$VAR)\`. Dùng sai kiểu theo hai chiều cho hai triệu chứng đối xứng.
- **Cách sửa:** công cụ nhận đường dẫn thì dùng biến \`type: file\`; công cụ nhận nội dung thì \`printf %s "\$VAR_TEXT" > /tmp/x && chmod 600 /tmp/x\`.

## Ca 4 — token đúng từng ký tự mà vẫn 401

- **Triệu chứng:** cùng một token cho \`200\` trên máy cá nhân và \`401\` trong job.
- **Bằng chứng:** \`\$ art_tep \$JG mot-byte.json | jq '{do_dai_sach, do_dai_ban, http_sach, http_ban}'\` -> độ dài chênh **1**, HTTP **200** so **401**
- **Nguyên nhân:** một ký tự xuống dòng ở cuối giá trị. Ô nhập trong giao diện là \`textarea\` và giữ nó; \`masked\` che mất đúng chỗ cần nhìn.
- **Cách sửa:** \`\${#VAR}\` và \`od -c\` ở đầu job nghi vấn (**0,02 giây**); sửa nguồn giá trị, và chỉ dùng \`tr -d '\\r\\n'\` như bản vá tạm.

## Ca 5 — mật khẩu có \`\$\` tới nơi ngắn đi 2 ký tự

- **Triệu chứng:** xác thực thất bại với mật khẩu chắc chắn đúng; log không hé ra gì vì \`masked\` che phần còn lại.
- **Bằng chứng:** \`\$ art_tep \$JH expand.json | jq '{do_dai_mo_rong, do_dai_tho, hut}'\` -> **6** so **8**, hụt **2**
- **Nguyên nhân:** giá trị biến được **mở rộng**; \`\$\$\` bị đọc là tham chiếu tới một biến rỗng.
- **Cách sửa:** khai \`expand: false\` trong YAML, hoặc \`raw=true\` qua API — \`bash dat-bien.sh dat MK 'Pa\$\$w0rd' --no-expand\`.
MD
grep -c '^- \*\*' ~/lab06/nam-ca-bien-sai.md      # phải là 20 (5 ca × 4 dòng)
```

---

## L7. Bước 5 — Biến xuống pipeline con · `dotenv` · `CI_DEBUG_TRACE` (20 phút)

Kiểm chứng QT 4.3, QT 7.1, QT 7.2.

### 5.1. `dotenv` là nấc 5, và một project variable cùng tên vô hiệu hoá nó (5 phút)

```bash
cd ~/lab06 && git checkout -q -B pipeline-con
cat > .gitlab-ci.yml <<'YML'
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH'
stages: [chuan-bi, dung]
sinh-bien:
  stage: chuan-bi
  image: alpine:3.20
  script:
    - echo "PHIEN_BAN=1.4.2" > bien.env
    - cat bien.env
  artifacts:
    reports:
      dotenv: bien.env
dung-bien:
  stage: dung
  image: alpine:3.20
  needs: ["sinh-bien"]
  script:
    - 'echo "job sau thay PHIEN_BAN=[$PHIEN_BAN]"'
YML
git add -A && git commit -q -m "dotenv nac 5" --allow-empty
bash dat-bien.sh xoa PHIEN_BAN >/dev/null 2>&1
PIPE_I=$(day_nhanh pipeline-con "dotenv lan 1"); cho_pipeline "$PIPE_I"
job_log_sach "$(job_id "$PIPE_I" "dung-bien")" | grep 'PHIEN_BAN='

# Lần 2: thêm ĐÚNG MỘT project variable cùng tên
bash dat-bien.sh dat PHIEN_BAN 9.9.9
PIPE_J=$(day_nhanh pipeline-con "dotenv lan 2"); cho_pipeline "$PIPE_J"
job_log_sach "$(job_id "$PIPE_J" "sinh-bien")" | grep 'PHIEN_BAN='
job_log_sach "$(job_id "$PIPE_J" "dung-bien")" | grep 'PHIEN_BAN='
```

Lần 2 là ca dễ mất nhiều giờ nhất của §4 tệp lý thuyết: job trước in `1.4.2` **rõ ràng trong log**, job sau in `9.9.9`. Cả hai giá trị đều **có thật** và đều đúng ở nấc của nó — nấc 5 so nấc 2 — và người gỡ lỗi không biết mình đang so hai nấc. Hệ quả thực dụng: biến `dotenv` nên có tiền tố riêng, ví dụ `OUT_PHIEN_BAN`, để không đụng vùng tên của nấc 2.

### 5.2. Ba cách khai biến xuống pipeline con (8 phút)

Project hạ nguồn `lab06-bien-downstream` cần một `.gitlab-ci.yml` biết đếm. Đẩy nó lên trước:

```bash
mkdir -p ~/lab06-con && cd ~/lab06-con && git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID_CON" | jq -r .path_with_namespace).git"
cat > .gitlab-ci.yml <<'YML'
variables:
  TU_CAP_JOB: "gia-tri-cua-REPO-CON"
dem-bien:
  image: alpine:3.20
  script:
    - apk add --no-cache jq >/dev/null
    - |
      jq -n --arg tc "${TU_TREN_CUNG-KHONG-CO}" --arg cj "${TU_CAP_JOB-KHONG-CO}" \
            --arg pv "${TU_PIPELINE-KHONG-CO}" \
            --argjson n "$(env | grep -cvE '^(CI_|GITLAB_|FF_|PATH=|HOME=|HOSTNAME=|PWD=|SHLVL=|_=)')" \
            '{tu_tren_cung:$tc, tu_cap_job:$cj, tu_pipeline:$pv, so_bien_khong_phai_CI:$n}' > xuong.json
      cat xuong.json
  artifacts:
    paths: [xuong.json]
YML
git add -A && git commit -q -m "repo con dem bien"
git push -q -o ci.skip origin HEAD:refs/heads/main
```

Pipeline cha, ba chỗ khai, cộng một ca đối chứng tắt kế thừa:

```bash
cd ~/lab06
DUONG_CON=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID_CON" | jq -r .path_with_namespace)
cat > .gitlab-ci.yml <<YML
workflow:
  rules:
    - if: '\$CI_COMMIT_BRANCH'
variables:
  TU_TREN_CUNG: "cha-nac-7"
kich-hoat:
  variables:
    TU_CAP_JOB: "cha-cap-job"
  trigger:
    project: $DUONG_CON
    branch: main
    strategy: depend
kich-hoat-tat-ke-thua:
  inherit:
    variables: false
  variables:
    TU_CAP_JOB: "cha-cap-job"
  trigger:
    project: $DUONG_CON
    branch: main
    strategy: depend
YML
git add -A && git commit -q -m "ba cach khai xuong pipeline con" --allow-empty
git push -q -f -o ci.skip origin HEAD:refs/heads/pipeline-con
# Nấc 1 của CHA: pipeline variable, để đo đường trigger:forward
PIPE_K=$(curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipeline?ref=pipeline-con" \
  --form 'variables[][key]=TU_PIPELINE' --form 'variables[][value]=cha-pipeline-variable' | jq -r .id)
cho_pipeline "$PIPE_K" 600
```

Đọc kết quả ở phía **con**, không ở phía cha. Đường đi từ cha xuống con qua `bridges`:

```bash
curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE_K/bridges" \
  | jq -r '.[] | "\(.name)\t\(.status)\t\(.downstream_pipeline.id)"'
doc_con() {   # doc_con <id pipeline con>  -> in xuong.json
  local dp="$1" jid
  jid=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID_CON/pipelines/$dp/jobs" \
        | jq -r '.[] | select(.name=="dem-bien") | .id' | head -1)
  curl -sfL "${H[@]}" "$GITLAB/api/v4/projects/$PID_CON/jobs/$jid/artifacts/xuong.json"
}
DP1=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE_K/bridges" \
      | jq -r '.[] | select(.name=="kich-hoat") | .downstream_pipeline.id')
DP2=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE_K/bridges" \
      | jq -r '.[] | select(.name=="kich-hoat-tat-ke-thua") | .downstream_pipeline.id')
doc_con "$DP1" | tee /tmp/con-1.json | jq .
doc_con "$DP2" | tee /tmp/con-2.json | jq .
```

Ba con số phải đọc kỹ. `tu_cap_job` ở pipeline con **1**: nếu nó là `cha-cap-job` thì biến khai ở cấp job của job `trigger` xuống con như **pipeline variable của con** và thắng cả `variables` của repo con — đó là đường mạnh nhất trong ba đường. `tu_tren_cung`: nó chịu công tắc `inherit:variables`, nên hai pipeline con phải cho hai giá trị khác nhau. `tu_pipeline`: nó chịu `trigger:forward`, và giá trị mặc định của cờ đó **phải đo**, không được đoán — đây là đại lượng loại (c) của bước này.

### 5.3. `CI_DEBUG_TRACE` — bật một lần, đo hai con số, rồi xoá log (4 phút)

Bật bằng **pipeline variable** (nấc 1) trên nhánh riêng, không commit vào YAML. Đo log **trước** khi bật để có mốc so:

```bash
cd ~/lab06
J_TRUOC=$(job_id "$PIPE_I" "dung-bien")
KB_TRUOC=$(job_log "$J_TRUOC" | wc -c)
echo "log truoc khi bat = $KB_TRUOC byte"

PIPE_L=$(curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipeline?ref=pipeline-con" \
  --form 'variables[][key]=CI_DEBUG_TRACE' --form 'variables[][value]=true' \
  --form 'variables[][key]=TU_PIPELINE'    --form 'variables[][value]=x' | jq -r .id)
cho_pipeline "$PIPE_L" 600
J_SAU=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE_L/jobs" | jq -r '.[0].id')
job_log "$J_SAU" > /tmp/trace-debug.txt
wc -c /tmp/trace-debug.txt
grep -cE '^\+\+ export|^\+ export' /tmp/trace-debug.txt
grep -c 'CI_JOB_TOKEN' /tmp/trace-debug.txt
bash ~/lab05/doc-pha.sh "$PID" "$J_SAU" --tsv        # dùng lại công cụ buổi 05
echo "export J_SAU=$J_SAU" >> ~/.gitlab-lab.env
```

**CHECKPOINT 11 — ba phép đo của bước 5 cùng lúc: nấc 2 thắng nấc 5; ba cách khai xuống pipeline con cho ba kết quả và ca tắt kế thừa khác ca thường; `CI_DEBUG_TRACE` làm log phình từ ~12 kB lên hàng trăm kB kèm `CI_JOB_TOKEN` nguyên văn.**

```bash
# (a) QT 4.3 — nấc 5 so nấc 2
v5=$(job_log_sach "$(job_id "$PIPE_J" "sinh-bien")" | grep -oE 'PHIEN_BAN=[0-9.]+' | head -1 | cut -d= -f2)
v2=$(job_log_sach "$(job_id "$PIPE_J" "dung-bien")" | grep -oE 'PHIEN_BAN=\[[^]]*\]' | head -1 | sed 's/.*\[\([^]]*\)\]/\1/')
# (b) QT 7.1 — ba cách khai
cj1=$(jq -r .tu_cap_job     /tmp/con-1.json); tc1=$(jq -r .tu_tren_cung /tmp/con-1.json)
tc2=$(jq -r .tu_tren_cung   /tmp/con-2.json); pv1=$(jq -r .tu_pipeline  /tmp/con-1.json)
n1=$(jq -r .so_bien_khong_phai_CI /tmp/con-1.json); n2=$(jq -r .so_bien_khong_phai_CI /tmp/con-2.json)
# (c) QT 7.2 — giá của CI_DEBUG_TRACE
kb_sau=$(wc -c < /tmp/trace-debug.txt); n_exp=$(grep -cE '^\+\+ export|^\+ export' /tmp/trace-debug.txt || true)
n_tok=$(grep -c 'CI_JOB_TOKEN' /tmp/trace-debug.txt || true)
{ [ "$v5" = "1.4.2" ] && [ "$v2" = "9.9.9" ] \
  && [ "$cj1" = "cha-cap-job" ] && [ "$tc1" != "$tc2" ] \
  && [ "$kb_sau" -gt $((KB_TRUOC*5)) ] && [ "$n_tok" -ge 1 ]; } \
  && echo "CHECKPOINT 11 — ĐẠT (nấc 5 sinh $v5 nhưng job sau nhận $v2 tức nấc 2 thắng; con: tu_cap_job=$cj1 tu_tren_cung=$tc1 so $tc2, tu_pipeline=$pv1, số biến $n1 so $n2; log $KB_TRUOC -> $kb_sau byte, $n_exp dòng export, CI_JOB_TOKEN xuất hiện $n_tok lần)" \
  || echo "CHECKPOINT 11 — LỖI (v5=$v5 v2=$v2 cj1=$cj1 tc1=$tc1 tc2=$tc2 log=$KB_TRUOC->$kb_sau token=$n_tok)" \
  | tee -a ~/lab06/checkpoint.log
```

Con số tham chiếu của đề cương là **12 kB → ~400 kB** và **250–400** dòng biến. Cả hai **không phổ quát**: chúng phụ thuộc số biến của project và số dòng `script`, nên lấy làm **bậc độ lớn**, không lấy làm hằng số. Điều không đổi là dòng `grep -c 'CI_JOB_TOKEN'` ra một số **lớn hơn 0** — nghĩa là log này chứa một token có quyền thật với API và registry suốt thời gian job chạy, và bất cứ ai đọc được project đều tải nó về bằng một lệnh `curl`.

Vì thế **việc xoá log của job này là bắt buộc**, và nó nằm ở §L8.2. `CHECKPOINT 12` kiểm chính việc đó bằng lệnh — đó là lý do bảng quy tắc ở README ghi QT 7.2 được kiểm chứng ở **CP11 và CP12**: CP11 đo cái giá, CP12 đo việc đã trả giá xong chưa.

### 5.4. `pipeline-con.md` (3 phút)

```bash
cat > ~/lab06/pipeline-con.md <<MD
# Biến xuống pipeline con, và giá của CI_DEBUG_TRACE — GitLab CE 17.7 · Runner 17.7

## Ba cách khai, đo ở phía CON (đọc artifact xuong.json qua API)

| # | Chỗ khai ở pipeline cha | Cơ chế xuống con | Ca thường | Ca \`inherit:variables: false\` |
|---|---|---|---|---|
| 1 | \`variables\` cấp **job** của job \`trigger\` | xuống như **pipeline variable của con**, thắng cả YAML repo con | \`$(jq -r .tu_cap_job /tmp/con-1.json)\` | \`$(jq -r .tu_cap_job /tmp/con-2.json)\` |
| 2 | \`variables\` cấp **trên cùng** của cha | vào job \`trigger\` theo kế thừa, chịu công tắc \`inherit:variables\` | \`$(jq -r .tu_tren_cung /tmp/con-1.json)\` | \`$(jq -r .tu_tren_cung /tmp/con-2.json)\` |
| 3 | **pipeline variable** của cha (POST /pipeline) | chịu \`trigger:forward\` — mặc định PHẢI ĐO | \`$(jq -r .tu_pipeline /tmp/con-1.json)\` | \`$(jq -r .tu_pipeline /tmp/con-2.json)\` |

Số biến không phải \`CI_*\` mà pipeline con nhận được: **$(jq -r .so_bien_khong_phai_CI /tmp/con-1.json)** (ca thường)
so **$(jq -r .so_bien_khong_phai_CI /tmp/con-2.json)** (ca tắt kế thừa). Đây là con số PHẢI ĐO, không được đoán.

Chế độ hỏng: cha xanh, con xanh, mũi nối xanh — việc không được làm. Cách rẻ nhất biến
hai lớp xanh thành một job đỏ là một dòng \`: "\${TU_CAP_JOB:?pipeline con KHÔNG nhận được biến}"\`
trong \`.gitlab-ci.yml\` của repo con.

## Giá của CI_DEBUG_TRACE

| Đại lượng | Trước | Sau | Tham chiếu đề cương |
|---|---|---|---|
| Kích thước log job | $KB_TRUOC byte | $(wc -c < /tmp/trace-debug.txt) byte | 12 kB -> ~400 kB |
| Số dòng \`export\` | 0 | $(grep -cE '^\+\+ export|^\+ export' /tmp/trace-debug.txt) | 250-400 dòng |
| \`CI_JOB_TOKEN\` nguyên văn | 0 lần | $(grep -c CI_JOB_TOKEN /tmp/trace-debug.txt) lần | > 0 là đủ để phải xoá log |

Cách bật đúng: **pipeline variable** truyền lúc \`POST /pipeline\` (nấc 1), trên **nhánh riêng**,
cho **một** job — KHÔNG commit \`CI_DEBUG_TRACE: "true"\` vào YAML, vì commit ở lại trong lịch sử git.
Kiểm repo mình có ai từng làm thế chưa: \`git grep -n CI_DEBUG_TRACE \$(git rev-list --all | head -200)\`.
MD
head -20 ~/lab06/pipeline-con.md
```

---

## L8. Nộp sản phẩm và dọn dẹp (10 phút)

Buổi này khác năm buổi trước ở một điểm: **việc dọn là phần của bài nộp**, không phải việc lịch sự làm nếu còn thời gian. Bài lab đã tạo biến ở ba phạm vi — trong đó một phạm vi ảnh hưởng **mọi project của mọi người** — và đã sinh một log chứa `CI_JOB_TOKEN` nguyên văn. Nộp bài mà còn biến sót hoặc còn log là **chưa nộp**.

### L8.1. Xoá mọi biến đã tạo ở ba phạm vi (3 phút)

```bash
source ~/.gitlab-lab.env
cd ~/lab06
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")

# 1) Mức PROJECT — bài lab chỉ tạo biến trong project lab, xoá sạch được
bash dat-bien.sh don-sach
bash dat-bien.sh liet-ke

# 2) Mức GROUP — group này là group riêng của học viên nên cũng xoá sạch được
bash dat-bien.sh don-sach --group "$GID"
bash dat-bien.sh liet-ke --group "$GID"

# 3) Mức INSTANCE — CHỈ xoá đúng tên mình tạo, đối chiếu ảnh chụp ở §L1
for k in NAC_THU THU_PHAM_VI; do bash dat-bien.sh xoa "$k" --instance; done
curl -sf "${H[@]}" "$GITLAB/api/v4/admin/ci/variables?per_page=100" \
  | jq -r '[.[].key] | sort | .[]' > ~/lab06/sao-luu/instance.sau.txt
diff ~/lab06/sao-luu/instance.truoc.txt ~/lab06/sao-luu/instance.sau.txt \
  && echo "mức instance KHỚP ảnh chụp trước buổi học"

# 4) Thu hồi project access token của ca 4 — đừng đợi nó hết hạn sau 2 ngày
curl -s -o /dev/null -w 'thu hoi PAT: HTTP %{http_code}\n' --request DELETE "${H[@]}" \
  "$GITLAB/api/v4/projects/$PID/access_tokens/$PAT_ID"
```

Nếu `don-sach --group` báo `403` thì học viên đã đi đường B và group không có biến nào — bỏ qua, CHECKPOINT 12 vẫn đạt vì đoạn kiểm dưới đây coi mảng rỗng và phạm vi không truy cập được là như nhau.

### L8.2. Xoá log của job đã bật `CI_DEBUG_TRACE` (2 phút)

`POST /jobs/:id/erase` xoá cả `trace` và artifact của job. Đây là thao tác **một chiều**, và đó là chủ ý: log kia không có phiên bản nào đáng giữ.

```bash
curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$J_SAU/erase" \
  | jq '{id, name, erased_at}'
# Bằng chứng: trace giờ rỗng hoặc rất ngắn, và erased_at khác null
curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$J_SAU/trace" | wc -c
rm -f /tmp/trace-debug.txt
```

Một chỗ dễ quên: bản `/tmp/trace-debug.txt` trên **máy học viên** cũng chứa `CI_JOB_TOKEN`. Xoá cả nó — dọn nửa vời còn tệ hơn không dọn, vì nó tạo cảm giác đã xong.

### L8.3. Gom hiện vật và kiểm bằng lệnh (4 phút)

```bash
DICH=~/gitlab-portfolio/06-bien-va-bi-mat
mkdir -p "$DICH"
cd ~/lab06
cp -f bang-9-nguon-bien.tsv nam-ca-bien-sai.md dat-bien.sh so-nac.sh \
      masked-lo.md bien-file-va-expand.md pipeline-con.md \
      .gitlab-ci.yml checkpoint.log "$DICH"/ 2>/dev/null
ls -l "$DICH"
```

```bash
cat > ~/lab06/kiem-hien-vat.sh <<'SH'
#!/usr/bin/env bash
# Kiểm hiện vật nộp của buổi 06. Dùng: bash kiem-hien-vat.sh [thu_muc]
D="${1:-$HOME/gitlab-portfolio/06-bien-va-bi-mat}"
loi=0
bao() { if [ "$1" = 0 ]; then printf '  ĐẠT   %s\n' "$2"; else printf '  LỖI   %s\n' "$2"; loi=$((loi+1)); fi; }

for f in bang-9-nguon-bien.tsv nam-ca-bien-sai.md dat-bien.sh so-nac.sh \
         masked-lo.md bien-file-va-expand.md pipeline-con.md .gitlab-ci.yml checkpoint.log; do
  [ -s "$D/$f" ]; bao $? "có $f và khác rỗng"
done

# --- hiện vật CỐT LÕI 1: bảng chín nấc phải đúng NỘI DUNG, không chỉ tồn tại ---
awk -F'\t' '!/^#/ && $1!="cap" && NF>=8 {n++} END {exit !(n==8 || n==6)}' "$D/bang-9-nguon-bien.tsv"
bao $? "bang-9-nguon-bien.tsv có 8 dòng dữ liệu (hoặc 6 nếu đi đường B)"
awk -F'\t' '!/^#/ && $1!="cap" && NF>=8 { if ($6=="" || $6=="-") bad=1
             if ($1 !~ /^[0-9]+-[0-9]+$/) bad=1 } END {exit bad}' "$D/bang-9-nguon-bien.tsv"
bao $? "mọi dòng có cột nac_thang đo được và cột cap dạng <A>-<B>"
grep -q '^# phien ban:' "$D/bang-9-nguon-bien.tsv" && ! grep -q 'DIEN-VAO-DAY' "$D/bang-9-nguon-bien.tsv"
bao $? "bang-9-nguon-bien.tsv ghi rõ phiên bản GitLab đã đo"

# --- hiện vật CỐT LÕI 2: năm ca, mỗi ca bốn dòng, dòng 2 là MỘT LỆNH ---
[ "$(grep -c '^## Ca ' "$D/nam-ca-bien-sai.md")" -eq 5 ]
bao $? "nam-ca-bien-sai.md có đúng 5 ca"
[ "$(grep -c '^- \*\*' "$D/nam-ca-bien-sai.md")" -eq 20 ]
bao $? "nam-ca-bien-sai.md có 20 dòng nhãn (5 ca × 4 dòng)"
[ "$(grep -c '^- \*\*Bằng chứng:\*\* .*\$ ' "$D/nam-ca-bien-sai.md")" -ge 5 ]
bao $? "mỗi ca có dòng bằng chứng dạng LỆNH, không phải câu văn"

# --- hai script phải chạy được và có đủ cờ ---
bash -n "$D/dat-bien.sh"; bao $? "dat-bien.sh không lỗi cú pháp"
grep -q -- '--masked'  "$D/dat-bien.sh" && grep -q -- '--protected' "$D/dat-bien.sh" \
  && grep -q -- '--file' "$D/dat-bien.sh" && grep -q -- '--no-expand' "$D/dat-bien.sh"
bao $? "dat-bien.sh có đủ bốn cờ giá trị"
grep -q 'http_code' "$D/dat-bien.sh"; bao $? "dat-bien.sh in mã HTTP"
bash -n "$D/so-nac.sh"; bao $? "so-nac.sh không lỗi cú pháp"
grep -q 'nac_thang\|THANG' "$D/so-nac.sh"; bao $? "so-nac.sh in nấc thắng"

# --- ba hiện vật đo ---
grep -q 'ro-ri.env' "$D/masked-lo.md" && grep -q 'base64' "$D/masked-lo.md"
bao $? "masked-lo.md ghi ba đường lộ kèm bằng chứng grep trên artifact"
grep -qE '400' "$D/masked-lo.md"; bao $? "masked-lo.md ghi mã HTTP 400 của ca đối chứng"
grep -q 'do_dai_ban\|độ dài sạch' "$D/bien-file-va-expand.md" && grep -q '401' "$D/bien-file-va-expand.md"
bao $? "bien-file-va-expand.md có ba ca đo (file · 1 byte · expand)"
grep -qE 'trigger:forward|inherit' "$D/pipeline-con.md" && grep -q 'CI_JOB_TOKEN' "$D/pipeline-con.md"
bao $? "pipeline-con.md có ba cách khai và số đo CI_DEBUG_TRACE"

# --- 12 dòng ĐẠT ---
grep -c 'ĐẠT' "$D/checkpoint.log" | awk '{exit !($1>=12)}'
bao $? "checkpoint.log có đủ 12 dòng ĐẠT"

# --- DỌN DẸP: ba phạm vi biến rỗng, và log debug trace đã bị xoá ---
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")
np=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/variables?per_page=100" | jq 'length' 2>/dev/null || echo 0)
[ "${np:-0}" -eq 0 ]; bao $? "biến mức project đã xoá sạch (GET /variables trả mảng rỗng, đếm=$np)"
ng=$(curl -sf "${H[@]}" "$GITLAB/api/v4/groups/${GID:-0}/variables?per_page=100" | jq 'length' 2>/dev/null || echo 0)
[ "${ng:-0}" -eq 0 ]; bao $? "biến mức group đã xoá sạch (đếm=$ng)"
if [ -f "$HOME/lab06/sao-luu/instance.truoc.txt" ] && [ -f "$HOME/lab06/sao-luu/instance.sau.txt" ]; then
  diff -q "$HOME/lab06/sao-luu/instance.truoc.txt" "$HOME/lab06/sao-luu/instance.sau.txt" >/dev/null
  bao $? "biến mức instance khớp ảnh chụp trước buổi học"
else
  printf '  BỎ QUA  không tạo biến mức instance — không có gì phải khôi phục\n'
fi
er=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/${J_SAU:-0}" | jq -r '.erased_at // "null"' 2>/dev/null || echo null)
[ "$er" != "null" ]; bao $? "log của job CI_DEBUG_TRACE đã bị xoá (erased_at=$er)"
tb=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/${J_SAU:-0}/trace" | wc -c)
[ "$tb" -lt 2000 ]; bao $? "trace của job đó còn $tb byte (< 2.000 byte)"
[ ! -f /tmp/trace-debug.txt ]; bao $? "bản sao log trên máy học viên đã xoá"

echo "---"
[ "$loi" -eq 0 ] && echo "CHECKPOINT 12 — ĐẠT" || echo "CHECKPOINT 12 — LỖI ($loi lỗi)"
exit "$loi"
SH
bash ~/lab06/kiem-hien-vat.sh | tee -a ~/lab06/checkpoint.log
cp -f ~/lab06/checkpoint.log ~/gitlab-portfolio/06-bien-va-bi-mat/
```

**CHECKPOINT 12 — mọi hiện vật hợp lệ về NỘI DUNG, ba phạm vi biến đã xoá sạch, và log của job đã bật `CI_DEBUG_TRACE` đã bị xoá.**

Đoạn trên **là** checkpoint 12. Nó không kiểm tệp có tồn tại hay không mà kiểm bốn thứ khó gian hơn: bảng chín nấc có đúng 8 dòng với cột `nac_thang` đo được; mỗi ca trong `nam-ca-bien-sai.md` có dòng bằng chứng dạng **lệnh** chứ không phải câu văn; `GET /variables` của **cả ba** phạm vi trả mảng rỗng; và job đã bật `CI_DEBUG_TRACE` có `erased_at` khác `null` với `trace` còn dưới **2.000** byte.

### L8.4. Dọn project lab (1 phút)

Giữ nguyên `~/lab06` tới hết buổi 07 — buổi 07 §L1 dòng 6 kiểm `bash -n ~/lab06/dat-bien.sh` và ca 2 của nó dựng lại đúng biến `protected` của QT 5.2. Chỉ xoá project trên GitLab sau khi `kiem-hien-vat.sh` đã `ĐẠT`:

```bash
for p in "$PID_CON" "$PID"; do
  curl -sf --request DELETE "${H[@]}" "$GITLAB/api/v4/projects/$p" && echo "da xoa project $p"
done
curl -sf --request DELETE "${H[@]}" "$GITLAB/api/v4/groups/$GID" && echo "da xoa group $GID"
rm -rf ~/lab06-con
```

---

## L9. Xử lý sự cố thường gặp trong lab

| # | Triệu chứng | Nguyên nhân | Cách khắc phục |
|---|---|---|---|
| 1 | `~/lab05/cong-cu.sh` không có, hay đếm ra dưới 11 hàm | Đã xoá `~/lab05` sau buổi 05 dù §L8.3 buổi đó dặn giữ tới hết buổi 06 | Chép lại khối `cat > ~/lab05/cong-cu.sh` ở buổi 05 §L3 mục 3.1 nguyên xi; không viết lại theo trí nhớ |
| 2 | `POST /projects/:id/variables` trả `403` | Token thiếu scope `api`, hoặc vai trò dưới Maintainer trên project | Tạo lại personal access token scope `api`; nếu không được thì buổi này không làm được — biến mức project là nền của cả 12 quy tắc |
| 3 | **Đường B — không tạo được biến mức group** (`POST /groups` hay `/groups/:id/variables` trả `403`) | Instance cấm tạo group ở namespace gốc, hoặc vai trò dưới Owner của group | Bỏ **hai** cặp có nấc 3 là `2-3` và `3-4`; chạy sáu cặp `1-2`, `4-5`, `5-6`, `6-7`, `7-8`, `8-9`; bảng còn **6** dòng. Thêm vào đầu tệp TSV một dòng `# duong B: khong co quyen tao bien muc group -> bo cap 2-3 va 3-4, bang con 6 dong`. Nấc 3 vẫn được kể trong bài nộp dưới dạng suy luận từ nấc 2 và nấc 4, và §L11 **không** trừ điểm |
| 4 | `GET /user \| jq .is_admin` cho `false` — không tạo được biến mức instance | Không phải admin của GitLab lab | Bỏ cặp `3-4` và `4-5`, chạy sáu cặp còn lại; bảng cũng còn **6** dòng. Nếu **vừa** không có group **vừa** không có admin thì bỏ ba cặp `2-3`, `3-4`, `4-5` và bảng còn **5** dòng — ghi lý do vào dòng `#` đầu tệp |
| 5 | `POST /projects/:id/access_tokens` trả `403` hay `404` | Project access token bị tắt ở mức instance | Dùng đường của README: một token thật **đã hết hiệu lực**. Khi đó ca 4 chỉ còn bằng chứng `${#VAR}` chênh **1** byte, còn cột HTTP là `401` cho **cả hai** — ghi rõ điều đó vào `bien-file-va-expand.md` và CHECKPOINT 9 đổi điều kiện `hs=200` thành `hs=hb=401` |
| 6 | `so-nac.sh` in `khong doc duoc gia tri` | Job `in-nac` chưa chạy xong, hoặc pipeline bị `workflow` chặn nên không có job nào | `curl "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE" \| jq .status`; nếu `skipped` thì khối `workflow` trong `khoi-workflow.yml` chưa có dòng `- if: '$CI_COMMIT_BRANCH'` cuối |
| 7 | Một cặp cho `nac_thang` **ngược** với sơ đồ chín nấc | Có thể là kết quả **đúng** của instance này, hoặc biến `NAC_THU` sót ở một phạm vi thứ ba | Chạy `bash dat-bien.sh liet-ke` ở cả ba phạm vi trước khi kết luận. Nếu ba phạm vi sạch mà kết quả vẫn ngược thì **giữ số đo** và ghi vào cột `ghi_chu` — sơ đồ là giá trị tham chiếu, bảng của lớp là số thật |
| 8 | `${#TOKEN_SACH}` và `${#TOKEN_BAN}` bằng nhau — ca 4 mất ý nghĩa | `curl --form` đã cắt ký tự xuống dòng cuối khi gửi giá trị | Đặt bằng JSON thay vì form: `curl --request POST -H 'Content-Type: application/json' --data "{\"key\":\"TOKEN_BAN\",\"value\":\"$PAT\\n\"}" "$GITLAB/api/v4/projects/$PID/variables"`; kiểm lại bằng `${#VAR}` trong job trước khi chạy checkpoint |
| 9 | Ca 5 cho `do_dai_mo_rong` bằng **8** chứ không phải 6 | Instance/runner xử lý `$$` như một dấu `$` được thoát — hành vi này đã đổi trong dòng 15.x–17.x | Đây là **dữ liệu**, không phải lỗi. Ghi số đo được kèm phiên bản, rồi đổi giá trị thử sang `Pa$MOI_TRUONGw0rd` với `MOI_TRUONG` rỗng để thấy cơ chế mở rộng rõ hơn; CHECKPOINT 10 đổi điều kiện thành `b > a` và ghi `hut` thật |
| 10 | Job `lo-ba-duong` in `duong 1 truc tiep: ` rỗng | Biến `TOKEN` vẫn còn cờ `protected` mà nhánh `lo-masked` không được bảo vệ — đúng QT 5.2 lặp lại | Đặt lại `TOKEN` **chỉ** với `--masked`, bỏ `--protected`, rồi chạy lại; đây là bẫy có chủ ý của §L5 mục 3.1 |
| 11 | Log **không** hiện `[MASKED]` dù biến có `masked=true` | Giá trị bị biến đổi trước khi in, hoặc runner cũ hơn 14.x, hoặc biến được in trong `after_script` của một job đã bị cắt | `bash dat-bien.sh liet-ke \| jq` kiểm cờ `masked` là `true`; nếu cờ đúng mà vẫn không che thì đó là đường lộ thứ tư — ghi vào `masked-lo.md`, đó là điểm cộng |
| 12 | `POST /variables --form 'masked=true'` cho `201` với giá trị `abc` | Ngưỡng độ dài của instance này khác 8, hoặc `masked_and_hidden` được cấu hình khác | **Giữ số đo**: chạy vòng lặp 6/7/8/9 ký tự ở §L5 mục 3.2 để tìm ngưỡng thật, rồi ghi ngưỡng đó vào `masked-lo.md`. Con số 8 là số của phiên bản, không phải hằng số |
| 13 | Job `so-hai-kieu` báo `wc: can't open ...` cho biến `type: file` | Biến chưa được đặt lại với cờ `--file`, hoặc job đang chạy trên nhánh mà biến có `protected` | `bash dat-bien.sh liet-ke \| jq '.[] \| select(.key=="KUBECONFIG_FILE")'` phải cho `variable_type: "file"` |
| 14 | Pipeline con **không** được tạo, `bridges` trả mảng rỗng | Đường `project:` sai, hoặc token không có quyền tạo pipeline ở project hạ nguồn | `curl "$GITLAB/api/v4/projects/$PID_CON" \| jq -r .path_with_namespace` và dán đúng chuỗi đó; job `trigger` đỏ thì đọc `trace` của nó, thông báo lỗi nằm ngay dòng đầu |
| 15 | `wc -c` của log sau khi bật `CI_DEBUG_TRACE` chỉ tăng vài kB | Biến truyền vào bị gộp sai khi dùng nhiều cặp `variables[][key]` trong một lệnh `curl` | Truyền **một** biến mỗi lệnh, hoặc dùng JSON `--data '{"variables":[{"key":"CI_DEBUG_TRACE","value":"true"}]}'`; kiểm bằng `curl .../pipelines/$PIPE/variables \| jq` |
| 16 | `POST /jobs/:id/erase` trả `403` | Job thuộc pipeline mới nhất của một nhánh được bảo vệ, hoặc thiếu quyền Maintainer | Bật `CI_DEBUG_TRACE` trên **nhánh riêng** như §L2 quyết định 5 dặn; nếu đã bật trên nhánh mặc định thì chạy thêm một pipeline mới trên nhánh đó rồi xoá log job cũ |
| 17 | `kiem-hien-vat.sh` báo biến mức project chưa xoá sạch | `don-sach` chạy trước khi một job đang chạy kết thúc và job đó tạo lại biến, hoặc còn `THU_*` sót | `bash dat-bien.sh liet-ke` rồi `bash dat-bien.sh xoa <TEN>` từng cái; chạy lại `kiem-hien-vat.sh` |
| 18 | Đã có project `lab06-bien` từ lần chạy trước | Buổi bị ngắt giữa đường | `curl --request DELETE "${H[@]}" "$GITLAB/api/v4/projects?search=lab06-bien"` không dùng được — lấy id bằng `?search=` rồi `DELETE /projects/:id` từng cái, kèm `DELETE /groups/:id` |

**Đường B tóm lại thành một câu:** nấc 3 và nấc 4 là hai nấc **duy nhất** của buổi cần quyền ngoài project. Không có chúng thì bảng còn **6** dòng thay vì 8, và sáu dòng đó vẫn giải thích trọn hai ca hay gặp nhất — nấc 2 thắng nấc 7, và nấc 2 thắng nấc 5. Điều duy nhất mất đi là câu trả lời cho "group hay project thắng", và câu đó suy được từ dòng `4-5` cộng với dòng `1-2`.

---

## L10. Bài tập mở rộng

Sáu bài đầu làm được với hạ tầng đã có. Bài 7 và 8 dành cho ai muốn đi trước tới buổi 09 và buổi 29.

**BT1 — Danh sách bom hẹn giờ của repo thật.** Trên một repo thật của đội, lấy danh sách project variable và group variable bằng API, đối chiếu với tên biến khai trong `.gitlab-ci.yml` bằng đoạn `comm -12` của §L3 mục 1.5.
*Câu hỏi phải trả lời:* có **bao nhiêu** tên biến xuất hiện ở cả hai chỗ, và với mỗi tên đó, giá trị nào đang thắng? Chỉ số này phải đưa về **0** — bao lâu thì làm được, và cần xin ai?

**BT2 — Đếm biến quan trọng chưa có khẳng định.** Viết một job đọc `.gitlab-ci.yml` của repo thật, liệt kê mọi biến được dùng trong `script` của những job có tác dụng phụ ra bên ngoài (deploy, push image, gọi API, xoá), rồi đếm bao nhiêu trong số đó đã có `: "${VAR:?}"` ở dòng đầu.
*Câu hỏi phải trả lời:* tỉ lệ đã có khẳng định là bao nhiêu phần trăm, và thêm đủ khẳng định cho phần còn lại tốn bao nhiêu **giây runner** mỗi pipeline? So với **0,01 giây** mỗi khẳng định thì con số đó có đáng bàn không?

**BT3 — Bảng chín nấc trên GitLab.com.** Nếu có tài khoản GitLab.com miễn phí, chạy lại **bốn** cặp `1-2`, `2-3`, `5-6`, `6-7` bằng chính `so-nac.sh`.
*Câu hỏi phải trả lời:* có khe nào cho kết quả khác instance lab không? Nếu có, khe nào và phiên bản hai bên là gì? Đây chính là lý do bảng chín nấc là đại lượng loại (c).

**BT4 — Đường lộ thứ tư của `masked`.** Tìm thêm **một** đường mà `masked` không bịt, ngoài ba đường của QT 5.1. Gợi ý để thử: `after_script`, tên artifact, thông báo lỗi của một công cụ in ra chuỗi đã cắt bớt, biến ghi vào `dotenv`.
*Câu hỏi phải trả lời:* đường bạn tìm được đi qua cơ chế nào, và `grep -c` trên hiện vật nào chứng minh nó? Nếu không tìm được đường thứ tư, hãy viết ra **ba** đường bạn đã thử và vì sao chúng bị che.

**BT5 — Ngưỡng `masked` theo phiên bản.** Dùng vòng lặp 4 tới 12 ký tự của §L5 mục 3.2 trên **hai** instance GitLab khác phiên bản.
*Câu hỏi phải trả lời:* ngưỡng của mỗi instance là bao nhiêu, và ràng buộc về ký tự cho phép có khác nhau không? Ghi lại **đoạn lệnh**, không ghi con số, vào tài liệu nội bộ của đội — vì sao?

**BT6 — `trigger:forward` mặc định là gì.** Chạy lại §L7 mục 5.2 với ba biến thể `trigger:forward:pipeline_variables` là `true`, `false`, và không khai.
*Câu hỏi phải trả lời:* ba ca cho ba con số `so_bien_khong_phai_CI` nào, và mặc định của cờ đó trên GitLab của bạn là gì? Buổi 09 sẽ dựng child pipeline trên đúng con số này.

**BT7 — Săn `CI_DEBUG_TRACE` trong lịch sử git.** Trên **mọi** repo bạn có quyền đọc, chạy `git grep -n CI_DEBUG_TRACE $(git rev-list --all | head -500)`.
*Câu hỏi phải trả lời:* có bao nhiêu repo từng commit `CI_DEBUG_TRACE: "true"`, commit sớm nhất cách đây bao lâu, và có bao nhiêu job đã chạy với nó? Nếu tìm thấy một ca, log của những job đó còn tồn tại không?

**BT8 — Biến ngắn hạn thay cho biến dài hạn.** Đọc trước tài liệu về `id_tokens` của GitLab và viết ra bốn dòng: token hiện tại của đội sống bao lâu, ai đổi được nó, thao tác đổi mất bao lâu, và ai biết nó đã bị lộ chưa.
*Câu hỏi phải trả lời:* bốn con số đó là bao nhiêu, và cái nào tệ nhất? Buổi 29 sẽ đi giải đúng bốn con số này, nên hãy lưu chúng lại.

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| # | Hiện vật | Điểm | Tiêu chí đạt điểm tối đa |
|---|---|---|---|
| 1 | `bang-9-nguon-bien.tsv` **(cốt lõi)** | 25 | **8** dòng dữ liệu (6 nếu đi đường B, có dòng `#` ghi lý do); mỗi dòng ≥ 8 cột; mọi ô `nac_thang` là số đo được; hai dòng cuối có `ghi_chu` giải thích nấc 8; có dòng ghi phiên bản GitLab, runner, máy đã đo |
| 2 | `nam-ca-bien-sai.md` **(cốt lõi)** | 20 | Đúng **5** ca, mỗi ca **4** dòng nhãn; dòng "Bằng chứng" là **một lệnh** in ra được, không phải câu văn; dòng "Nguyên nhân" gọi đúng **số nấc** |
| 3 | `masked-lo.md` | 12 | **3** đường lộ, mỗi đường một lệnh và một con số `grep -c`; bảng điều kiện bật `masked` có cột **mã HTTP** với hai dòng `400` và ngưỡng độ dài **đo được** |
| 4 | `dat-bien.sh` | 10 | Không lỗi cú pháp; **3** phạm vi (project, group, instance); **4** cờ giá trị; **luôn** in mã HTTP; có lệnh `don-sach` |
| 5 | `bien-file-va-expand.md` | 10 | Ba ca đo với **số của mình**: đường dẫn so nội dung · độ dài chênh **1** byte và HTTP 200 so 401 · **8** so **6** ký tự (hoặc số đo được kèm giải thích) |
| 6 | `so-nac.sh` | 8 | Nhận **hai** tham số là hai số nấc; dọn biến trước khi đo; sinh đúng **1** pipeline mỗi lần chạy; in một dòng TSV có cột `nac_thang` |
| 7 | `pipeline-con.md` | 5 | **3** cách khai kèm giá trị đo được ở phía **con**; ca `inherit:variables: false` đối chứng; hai con số của `CI_DEBUG_TRACE` trước và sau |
| 8 | `.gitlab-ci.yml` bản cuối | 5 | Có `workflow` chuẩn buổi 04; mọi biến quan trọng có `: "${VAR:?}"` ở dòng đầu `script` |
| 9 | `checkpoint.log` | 5 | Đủ **12** dòng `ĐẠT`, theo thứ tự |
| | **Tổng** | **100** | Đạt ≥ **60** · đạt tốt ≥ **80** |

**Điểm trừ — dẫn chiếu bảng Bẫy hay gặp ở §9 tệp lý thuyết:**

| Lỗi | Trừ | Bẫy số |
|---|---|---|
| Bảng chín nấc chép từ tệp lý thuyết hay đề cương thay vì tự đo | **−25** (mất trọn hiện vật cốt lõi) | 1 |
| `bang-9-nguon-bien.tsv` không ghi phiên bản GitLab đã đo | −5 | 1 |
| Dòng "Bằng chứng" của một ca là câu văn chứ không phải lệnh | −4 mỗi ca | 11 |
| Kết luận `masked` không che artifact **mà không** tải artifact về `grep` | −8 | 5, 6 |
| Viết rằng biến `protected` thiếu thì job sẽ **đỏ** | **trần điểm 1** | 7 |
| Viết rằng `masked` bảo vệ được secret, hay biến masked không lộ ra artifact | **trần điểm 1** | 5 |
| Không có dòng `: "${VAR:?}"` nào trong `.gitlab-ci.yml` bản cuối | −6 | 8 |
| Bỏ `masked` vì giá trị không thoả điều kiện, thay vì đổi secret | −5 | 9 |
| Kết luận về nấc mà không có mã HTTP hay dòng log làm bằng chứng | −5 | 2 |
| Còn biến sót ở bất kỳ phạm vi nào sau §L8 | **−15** | — |
| Còn log của job đã bật `CI_DEBUG_TRACE` | **−15** | 14 |
| Nộp thiếu một trong hai hiện vật cốt lõi | **chưa nộp bài** | — |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| L1 | Điều kiện tiên quyết và sao lưu ba phạm vi (làm trước giờ, không tính vào 150') | — |
| L2 | Kiến trúc bài lab (đọc trước giờ) | — |
| L3 | Bước 1 — Dựng bảng chín nấc bằng thực nghiệm, tám cặp | 35' |
| L4 | Bước 2 — Ca 1 và ca 2: YAML vô hiệu · biến `protected` rỗng | 30' |
| L5 | Bước 3 — `masked` che gì và không che gì; điều kiện bật | 25' |
| L6 | Bước 4 — Ca 3, 4, 5: biến file · ký tự vô hình · mở rộng biến | 30' |
| L7 | Bước 5 — Biến xuống pipeline con · `dotenv` · `CI_DEBUG_TRACE` | 20' |
| L8 | Nộp sản phẩm và dọn dẹp | 10' |
| L9–L11 | Xử lý sự cố · bài tập mở rộng · tiêu chí chấm (tra cứu, ngoài giờ) | — |
| **Tổng** | | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---



**Quy tắc cho giảng viên:**

- Chọn **5–7 câu** trong 12, ưu tiên câu 🔥. Trả lời **bằng miệng, không nhìn tài liệu**. **Gọi ngẫu nhiên**; ai thiếu thì gọi người kế tiếp bổ sung.
- Năm câu chen vào đã thành phản xạ của khoá: **"bao nhiêu?"** (01), **"sửa ở tệp nào?"** (02), **"đi qua đường nào trong bốn đường?"** (03), **"quyết định ở `t0` hay sau `t0`?"** (04), **"cái đó ai giữ — server hay runner?"** (05). Buổi này thêm câu thứ sáu, theo học viên tới hết khoá: **"biến này thắng ở nấc nào?"** Ai còn đáp "biến này bằng X vì YAML ghi X" thì chưa qua được buổi 06.
- Câu **7** và câu **9** là câu **tính toán**. Giảng viên buộc thí sinh nói ra một con số. "Tuỳ trường hợp" mà không kèm phép tính nào thì tối đa **1 điểm**, dù cơ chế đúng.

**Thang điểm mỗi câu:**

| Điểm | Nghĩa |
|---|---|
| 0 | Không trả lời được, hoặc sai cơ chế |
| 1 | Nhắc được tên khái niệm, không nêu cơ chế |
| 2 | Nêu đúng cơ chế |
| 3 | Đúng cơ chế **và** một con số, hoặc **và** một ca nó không đúng |

**Hai lỗi làm trần điểm cả buổi là 1:**

1. **Nói `masked` bảo vệ được secret, hoặc nói biến masked không lộ ra artifact.** `masked` là **1** phép thay thế chuỗi trên đường log; người tin ngược lại sẽ ghi token vào artifact rồi yên tâm vì log hiện `[MASKED]`.
2. **Nói biến `protected` thiếu thì job sẽ đỏ.** Nền tảng **không gửi** biến đó, job nhận chuỗi **rỗng** và chạy tiếp. Người tin job sẽ đỏ thì không viết dòng `${VAR:?}` nào.

**Bốn câu phân loại thật:**

| Câu | Phân loại điều gì |
|---|---|
| 2 | Người **đã từng mất nửa ngày vì nấc 2**. Chưa gặp thì đáp "sửa YAML thì phải có tác dụng chứ"; đã gặp thì gọi API liệt kê biến **trước** khi đọc YAML |
| 4 | Người **phân biệt được "rỗng" với "lỗi"**. Shell không coi rỗng là lỗi, nên chỉ người viết pipeline chặn được |
| 3 | Người **biết `masked` không phải bảo vệ secret** — câu lọc người nói theo tài liệu marketing; phải kể ra **3** đường lộ |
| 12 | Người **cân được lợi ích gỡ rối với rủi ro bảo mật**. "Bật lên xem cho nhanh" là 0; "không bao giờ bật" cũng chỉ 1 |

---

## V2. Bộ câu hỏi

### Câu 1 — 🔥

**Hỏi:** Biến trong GitLab CI đến từ bao nhiêu nguồn? Kể theo thứ tự ưu tiên, cao trước.

**Đáp án chuẩn:** **9** nguồn, thứ tự do **nền tảng** quyết định, không do tệp YAML.

| Nấc | Nguồn |
|---|---|
| 1 | pipeline variable — trigger · schedule · bấm tay · API — **ngoài repo** |
| 2 | project variable, Settings > CI/CD — **ngoài repo** |
| 3 | group variable — **ngoài repo** |
| 4 | instance variable — **ngoài repo** |
| 5 | `dotenv` của job trước, cần `needs`/`dependencies` |
| 6 | `variables` cấp **job** |
| 7 | `variables` cấp **trên cùng** |
| 8 | deployment variable |
| 9 | predefined variable `CI_*` |

Con số phải nói ra: **4** nấc cao nhất nằm **ngoài** repo. Nghĩa là **giá trị thật của một biến không đọc được bằng cách đọc `.gitlab-ci.yml`**, chỉ đọc được bằng cách in nó trong job hoặc gọi API. Giới hạn: đây là thứ tự tham chiếu của **GitLab CE 17.7**, ranh giới vài nấc kề nhau đã đổi giữa các phiên bản nên nó **phải đo** — lab bước 1 dựng lại bằng **8** phép so cặp, **4 phút runner**.

**Tiêu chí chấm:**
- 0đ: "Biến khai trong `.gitlab-ci.yml`" rồi dừng.
- 1đ: Kể được 3–4 nguồn, không có thứ tự.
- 2đ: Kể đủ **9** nấc đúng thứ tự.
- 3đ: Như trên, **và** nói rõ **4** nấc cao nhất ngoài repo nên không đọc được bằng YAML, **và** nêu bảng phải đo lại theo phiên bản.

**Câu hỏi đào sâu:** Vì sao nền tảng xếp cấu hình ngoài repo **trên** cấu hình trong repo? *(Cố ý: để đội vận hành đổi giá trị mà không cần merge request.)*

---

### Câu 2 — 🔥

**Hỏi:** "Tôi sửa biến trong `.gitlab-ci.yml` ba lần rồi, push lên, mà job vẫn in giá trị cũ." Chẩn đoán.

**Đáp án chuẩn:** Gần như chắc chắn **nấc 2 thắng nấc 7**: có một project variable cùng tên ghi đè khối `variables` cấp trên cùng.

Lệnh chẩn đoán, làm **trước** khi đọc YAML lần thứ tư:

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/projects/$PID/variables" \
| jq -r '.[] | "\(.key)\t\(.protected)\t\(.masked)"'          # rồi so với tên biến trong repo:
grep -nE '^\s{2,}[A-Z][A-Z0-9_]*:' .gitlab-ci.yml
```

Đúng **1** lần xoá project variable là đủ để YAML có tác dụng lại; không được xoá thì đổi **tên** biến trong YAML — không có cách nào "ưu tiên YAML". Ô của bảng hai thuộc tính (buổi 01 QT 7.1 — lần thứ **6**): **im lặng, không chặn**. Cách phòng: **đừng** dùng project variable cho thứ thuộc về mã nguồn — tên image, phiên bản công cụ, cờ build — chúng phải ở trong repo để `git log` giải thích được. Số đo: số tên biến trùng, về **0**.

**Tiêu chí chấm:**
- 0đ: "Chắc cache YAML, chạy lại xem sao."
- 1đ: Đoán có biến nào đó ghi đè, không nói được nấc nào và kiểm bằng gì.
- 2đ: Gọi đúng **nấc 2 thắng nấc 7** và nêu `GET /projects/:id/variables`.
- 3đ: Như trên, **và** gọi đúng ô *im lặng, không chặn*, **và** nêu quy tắc "cấu hình thuộc mã nguồn thì để trong repo".

**Câu hỏi đào sâu:** Group variable và project variable cùng tên thì cái nào thắng? *(Project — nấc 2 trên nấc 3.)*

---

### Câu 3 — ★★★

**Hỏi:** `masked` che cái gì, và **không** che cái gì?

**Đáp án chuẩn:** `masked` là **1** cơ chế: **thay thế chuỗi** trên đường log đi từ runner về server. **3** đường lộ nó không bịt:

| Đường lộ | Vì sao thoát được |
|---|---|
| Giá trị trong **artifact** | Artifact là gói tệp upload lên server, không phải log — không phép thay thế nào chạy trên nó; tải về rồi `grep` là thấy nguyên văn |
| Giá trị bị **biến đổi** trước khi in (`base64`, đảo chuỗi, chèn ký tự) | Chuỗi sau biến đổi khác chuỗi gốc nên không khớp |
| **Ai đọc được** giá trị trong giao diện | Không phải kiểm soát truy cập — Maintainer vẫn xem được ở Settings |

Cách đo: một job in biến masked ba cách — trực tiếp (bị che), qua `base64` (không che), ghi vào artifact (không che) — rồi tải artifact về `grep`; đó là checkpoint **kiểm tệp hiện vật**, không phải "nhìn log thấy `[MASKED]`". Kết luận: **`masked` không phải bảo vệ secret, nó là cơ chế giảm rò rỉ do vô tình** — secret thật cần **vòng đời ngắn, sinh lúc chạy**: buổi 29.

**Tiêu chí chấm:**
- 0đ: "`masked` che secret, bật lên là an toàn." **Trần điểm cả buổi là 1.**
- 1đ: Biết nó che trong log, không nêu được đường nào nó không bịt.
- 2đ: Nêu đúng cơ chế **thay thế chuỗi trên đường log** và kể ít nhất **2** đường lộ.
- 3đ: Đủ **3** đường lộ, **và** nêu cách đo bằng tải artifact về `grep`, **và** chốt "`masked` không phải bảo vệ secret".

**Câu hỏi đào sâu:** Biến sinh qua `artifacts:reports:dotenv` có tự động masked không? *(Không — buổi 01 QT 5.4. Truyền secret qua `dotenv` là vừa ghi nó vào artifact vừa mất `masked` ở job sau.)*

---

### Câu 4 — ★★★

**Hỏi:** Job `deploy` chạy trên nhánh feature. Nó **xanh**, và không có gì được deploy. Vì sao?

**Đáp án chuẩn:** Biến chứa token bật `protected`, nhánh feature **không** được bảo vệ. `protected` là **kiểm soát truy cập theo nhánh và tag**: nền tảng đơn giản là **không gửi** biến đó cho job.

Job nhận chuỗi **rỗng**, và shell coi rỗng là giá trị hợp lệ: `curl` đi tới đúng địa chỉ với header rỗng, nhận **401**, và `curl` không có `-f` thì mã thoát vẫn 0. Job xanh. Ô **im lặng, không chặn** — ô nguy hiểm nhất.

```yaml
script:
  - echo "do dai TOKEN = ${#TOKEN}"    # nhánh được bảo vệ: 20 · nhánh feature: 0
  - ': "${TOKEN:?thiếu TOKEN — biến protected, nhánh này chưa được bảo vệ}"'
```

Dòng thứ hai là toàn bộ cách sửa: **1** dòng `${VAR:?}` tốn **0,01 giây** và đổi ô của bảng hai thuộc tính từ *im lặng, không chặn* sang *ồn ào, có chặn* — đặt ở **dòng đầu** `script`.

**Tiêu chí chấm:**
- 0đ: "Biến protected thiếu thì job phải đỏ." **Trần điểm cả buổi là 1.**
- 1đ: Đoán do biến thiếu, không giải thích được vì sao job không đỏ.
- 2đ: Nêu đúng **nền tảng không gửi biến, job nhận rỗng, shell không coi rỗng là lỗi**.
- 3đ: Như trên, **và** đưa `${#TOKEN}` cho **0** so với **20** cùng dòng `${VAR:?}` kèm chi phí 0,01 giây, **và** gọi đúng ô của bảng hai thuộc tính.

**Câu hỏi đào sâu:** `${VAR:?}` khác `${VAR?}` chỗ nào? *(`:?` bắt cả rỗng lẫn chưa khai; `${VAR?}` chỉ bắt chưa khai — ca của ta là **rỗng** nên phải có dấu hai chấm.)*

---

### Câu 5 — ★★★

**Hỏi:** Biến sinh bởi `artifacts:reports:dotenv` nằm ở nấc nào? Kể **hai** điều nó không làm được.

**Đáp án chuẩn:** Nấc **5** — dưới cả bốn nấc ngoài repo, trên `variables` trong YAML.

**Một — không dùng được trong `rules`.** Lần thứ **2** nguyên lý này xuất hiện (buổi 04 QT 4.2). `rules` giải quyết ở `t0`, lúc đó job sinh biến còn **chưa chạy**.

**Hai — không ghi đè được project variable cùng tên.** Nấc 5 dưới nấc 2. Job trước in `PHIEN_BAN=1.4.2` rõ ràng, job sau in giá trị của project variable — hai giá trị **cùng tồn tại**, nấc cao thắng. Đúng **1** project variable cùng tên đủ vô hiệu hoá cơ chế `dotenv` cho biến đó, im lặng.

Cộng điều kiện tồn tại: `dotenv` chỉ tới job **sau**, và chỉ khi có `needs`/`dependencies`; thiếu quan hệ đó thì job sau nhận rỗng chứ không nhận lỗi, nên nó vẫn phải mở đầu bằng `: "${PHIEN_BAN:?dotenv không tới}"`.

**Tiêu chí chấm:**
- 0đ: "`dotenv` là cách mạnh nhất để đặt biến, nó thắng mọi thứ."
- 1đ: Biết `dotenv` truyền biến sang job sau, không biết nấc nào.
- 2đ: Nói đúng nấc **5** và nêu được **một** trong hai điều nó không làm được.
- 3đ: Đủ **hai** điều, **và** giải thích `rules` bằng lập luận `t0` chứ không bằng "GitLab không hỗ trợ", **và** nêu điều kiện `needs`/`dependencies`.

**Câu hỏi đào sâu:** Job A và B **cùng stage** đều sinh `PHIEN_BAN` qua `dotenv`, job C `needs` cả hai. C thấy giá trị nào? *(Không đoán được — hai nguồn cùng nấc, không có thứ tự xác định. Tránh bằng thiết kế: một biến, một nguồn.)*

---

### Câu 6 — ★★

**Hỏi:** Khai `variables` ở cấp trên cùng **và** ở cấp job: hai khối đó được **trộn** hay được **thay thế**?

**Đáp án chuẩn:** Hợp nhất theo **tên biến**, không thay thế cả khối. Hai khối `variables` là hai từ điển; nền tảng gộp theo khoá, trùng khoá thì cấp **job** (nấc 6) thắng cấp **trên cùng** (nấc 7).

```yaml
variables: { MOI_TRUONG: "dev", KHU_VUC: "ap-southeast-1", MUC_LOG: "info" }

trien-khai:
  variables: { MOI_TRUONG: "prod" }           # ghi đè 1 biến
  script:
    - echo "$MOI_TRUONG $KHU_VUC $MUC_LOG"    # in: prod ap-southeast-1 info
```

Con số chốt: **1** biến bị ghi đè, **2** biến còn nguyên.

Điểm đáng nói nhất: đây là chỗ biến **không** theo quy tắc ba nấc của `image`/`cache` (buổi 03 QT 7.1 — lần thứ **2**), nơi khai lại ở cấp job là **thay cả khối** và mất hết cấu hình `default:`. Bẫy thực tế: chép cả khối `variables` xuống cấp job "cho chắc", rồi một biến bị bỏ sót trong bản chép thành **rỗng** ở đúng một job. Làm đúng là chỉ khai lại **biến cần đổi**.

**Tiêu chí chấm:**
- 0đ: "Khai ở cấp job thì mất hết biến cấp trên cùng."
- 1đ: Biết cấp job thắng, không nói được là gộp theo tên biến.
- 2đ: Nêu đúng hợp nhất theo **tên biến**, và ví dụ 1 biến đổi 2 biến còn.
- 3đ: Như trên, **và** đối chiếu tường minh với quy tắc ba nấc ở buổi 03 QT 7.1, **và** nêu bẫy chép cả khối rồi bỏ sót một biến.

**Câu hỏi đào sâu:** Có cách nào làm một job **không** nhận biến cấp trên cùng? *(Có — `inherit:variables: false`. Đây cũng là cơ chế điều khiển việc truyền biến xuống pipeline con ở câu 11.)*

---

### Câu 7 — ★★★

**Hỏi:** Một token bạn đã so **từng ký tự** với bản gốc, đúng hoàn toàn, mà API vẫn trả **401**. Bạn tìm ra nguyên nhân trong mấy lệnh?

**Đáp án chuẩn:** **2** lệnh, dưới **1** giây. Nguyên nhân số một là **ký tự vô hình cuối giá trị** — xuống dòng, khoảng trắng, hoặc dấu nháy bị chép vào khi dán.

```bash
echo "${#TOKEN}"                          # in 21 — token thật dài 20 → thừa 1 byte
printf '%s' "$TOKEN" | od -c | tail -2    # byte cuối là \n
```

Phép tính phải nói ra: token thật dài **20** ký tự, `${#TOKEN}` cho **21**, thừa đúng **1** byte — và **1** byte thừa đủ đổi **200** thành **401**, vì server so khớp theo byte. Lệnh thứ nhất tốn **0,01 giây**, trả lời *"có thừa không"*; lệnh thứ hai trả lời *"thừa cái gì"*.

Vì sao mắt không thấy: giao diện và log **không hiển thị được** ký tự cuối chuỗi, còn `masked` thì che mất đúng chỗ ta cần nhìn. Quy tắc: **đừng so token bằng mắt và đừng so bằng log** — so bằng độ dài.

**Tiêu chí chấm:**
- 0đ: Đề nghị tạo token mới, hoặc đi kiểm quyền trước.
- 1đ: Biết có thể do ký tự lạ, không nêu lệnh nào đo được.
- 2đ: Nêu đúng `${#VAR}` và `od -c`, và cơ chế 1 byte thừa gây 401.
- 3đ: Như trên, **và** đưa con số **21 so với 20** kèm chi phí 0,01 giây, **và** nói rõ vì sao mắt và log không thấy được.

**Câu hỏi đào sâu:** `${#TOKEN}` cho đúng **20** mà vẫn 401 thì đi tiếp thế nào? *(Nghi phạm kế tiếp là mở rộng biến — câu 9. Sau đó mới tới nấc: biến có thể đang lấy từ nấc 2.)*

---

### Câu 8 — ★★★

**Hỏi:** Biến khai `type: file`. `$VAR` chứa gì? Kể **hai** triệu chứng khi dùng sai.

**Đáp án chuẩn:** Runner ghi giá trị ra một **tệp tạm** trong thư mục job và đặt **đường dẫn tệp** vào biến. Vậy `$VAR` là **đường dẫn**; nội dung ở `$(cat "$VAR")`. Có **2** kiểu biến.

**2** triệu chứng đối xứng, mỗi cái một chiều dùng sai:

| Triệu chứng | Nghĩa |
|---|---|
| **Lỗi phân tích cú pháp ở dòng 1 cột 1** | Biến khai kiểu **thường**, ta truyền nội dung vào chỗ chờ đường dẫn — công cụ mở "tệp" tên `-----BEGIN...` |
| **Không tìm thấy tệp `/builds/.../tmp/abc123`** | Biến khai kiểu **file**, ta dùng `$VAR` như nội dung — nhận đường dẫn thay vì dữ liệu |

`KUBECONFIG`, `GOOGLE_APPLICATION_CREDENTIALS`, `AWS_SHARED_CREDENTIALS_FILE` chỉ nhận **đường dẫn** → khai `type: file`; token dùng trong header HTTP thì khai kiểu **thường**. Dùng đúng là `kubectl --kubeconfig "$KUBECONFIG_FILE"`, kèm `test -s` để bắt ca tệp rỗng. Chi phí: **1** tệp tạm mỗi biến, **0** giây thêm. Ô của bảng hai thuộc tính: **ồn ào, có chặn** — nhưng ồn ào **sai hướng**, vì thông báo nói về cú pháp dữ liệu nên người ta đi sửa dữ liệu chứ không sửa kiểu biến.

**Tiêu chí chấm:**
- 0đ: "`$VAR` chứa nội dung, như biến thường."
- 1đ: Biết nó liên quan tệp, không nói rõ biến chứa đường dẫn.
- 2đ: Nêu đúng `$VAR` là **đường dẫn**, nội dung ở `$(cat "$VAR")`, và nêu được **một** triệu chứng.
- 3đ: Đủ **2** triệu chứng đối xứng, **và** kể được nhóm công cụ chỉ nhận đường dẫn, **và** nhận xét thông báo lỗi ồn ào nhưng **sai hướng**.

**Câu hỏi đào sâu:** Biến kiểu file có bật được `masked` không? *(Thường bị từ chối vì nội dung nhiều dòng — QT 5.3. Mà kể cả bật được thì nội dung vẫn nằm trong một tệp, và tệp đó vào artifact nếu ai khai `artifacts:paths: [.]`.)*

---

### Câu 9 — ★★

**Hỏi:** Mật khẩu `Pa$$w0rd` được đặt làm project variable. Job đọc ra thì nó dài mấy ký tự?

**Đáp án chuẩn:** **6**, hụt **2**.

Phép tính: `Pa$$w0rd` dài **8** ký tự. Giá trị biến được **mở rộng** — `$` và `${...}` trong giá trị bị hiểu là tham chiếu tới biến khác. Hai ký tự `$$` cho ra một tham chiếu tới tên biến rỗng và bị thay bằng chuỗi rỗng; còn lại `Pa` + `w0rd` = **6** ký tự, tức `Paw0rd`. Hụt đúng **2**.

```yaml
variables:
  MK_SAI: "Pa$$w0rd"        # ${#MK_SAI} = 6
  MK_DUNG:
    value: "Pa$$w0rd"
    expand: false           # ${#MK_DUNG} = 8
```

Vì sao ca này ác: xác thực thất bại ở **một nơi khác** — ở dịch vụ đích, không ở GitLab — và log không hé ra gì. Ô **im lặng, không chặn**.

**Tiêu chí chấm:**
- 0đ: "Vẫn 8, biến thì lưu y nguyên."
- 1đ: Biết `$` có thể gây vấn đề, không tính ra được con số.
- 2đ: Tính đúng ra **6** và nêu cơ chế mở rộng biến.
- 3đ: Như trên, **và** nêu `expand: false` là cách tắt cho đúng biến đó, **và** gọi đúng ô *im lặng, không chặn* vì thất bại xảy ra ở dịch vụ đích chứ không ở GitLab.

**Câu hỏi đào sâu:** Có nên bật `expand: false` cho mọi biến cho chắc? *(Không — nó phá biến cố ý tham chiếu biến khác; bật cho biến chứa **secret**, để nguyên cho biến cấu hình.)*

---

### Câu 10 — ★★

**Hỏi:** Giao diện GitLab **từ chối** bật `masked` cho một secret của bạn. Bạn làm gì?

**Đáp án chuẩn:** **Đổi secret**, không bỏ `masked`.

Bật được `masked` là ràng buộc lên **giá trị**, không lên ý muốn. Ở GitLab 17.7: tối thiểu **8** ký tự, đúng **1** dòng, **0** khoảng trắng. Lý do nằm ở cơ chế: phép thay thế chuỗi cần một chuỗi ổn định và phân biệt được. Đo bằng `POST /projects/:id/variables` với `masked=true` rồi đọc mã HTTP: `abc` và `mot hai ba` bị từ chối, chuỗi 32 ký tự hex thì được.

Đường sai rất hấp dẫn: giao diện từ chối, người ta bỏ `masked` để đi tiếp, và từ đó **mọi** log của project có secret nguyên văn — đổi một bất tiện 5 phút thành rò rỉ vô hạn định. Đường đúng theo thứ tự: (1) sinh lại secret theo định dạng thoả điều kiện; (2) giữ dạng base64 trong biến, giải mã trong job; (3) để `masked` tắt nhưng chuyển sang **biến kiểu file** để nó không bao giờ đi qua `echo`. Giới hạn: con số **8** là ràng buộc của **phiên bản**, đã đổi nhiều lần trong dòng 15.x–17.x — viết cách kiểm bằng API, đừng viết nó như hằng số.

**Tiêu chí chấm:**
- 0đ: "Bỏ `masked` đi cho nhanh." **Trần điểm cả buổi là 1.**
- 1đ: Biết có ràng buộc định dạng, không nêu được điều kiện nào.
- 2đ: Nêu đủ **8** ký tự · **1** dòng · **0** khoảng trắng, và chốt phải đổi secret.
- 3đ: Như trên, **và** giải thích ràng buộc bằng cơ chế thay thế chuỗi, **và** nêu con số 8 là của phiên bản nên phải đo bằng API.

**Câu hỏi đào sâu:** Vì sao nhiều nhà cung cấp phát token có tiền tố kiểu `glpat-`, `ghp_`? *(Để token nhận dạng và quét được — buổi 33 Gitleaks dựa vào đúng các tiền tố này. Cái lợi kèm theo: chuỗi dài và đặc trưng hơn, dễ thoả điều kiện `masked`.)*

---

### Câu 11 — ★★★

**Hỏi:** Pipeline con do job `trigger` sinh ra chạy với biến **rỗng**, và nó **xanh**. Bạn điều tra thế nào?

**Đáp án chuẩn:** Pipeline hạ nguồn **không** tự thấy mọi biến của pipeline cha. Quy tắc kế thừa do `inherit:variables` điều khiển, và biến khai ở cấp **job** của job `trigger` truyền xuống theo đường riêng so với biến cấp trên cùng. Có **3** chỗ khai — cấp trên cùng, cấp job của `trigger`, và pipeline variable đặt lúc bấm chạy (nấc 1) — và số biến xuống được là con số **phải đo**, không được đoán.

Thứ tự điều tra, mỗi nhịp là một phép đo:

1. **In môi trường trong pipeline con**, không đọc YAML của cha: `env | sort | grep -E '^(A|B)='` — dữ kiện duy nhất đáng tin.
2. **Đối chiếu ca `inherit:variables: false`** trên cùng job `trigger`, chạy lại, so hai danh sách; hiệu giữa chúng là tập biến đang đi bằng cơ chế kế thừa.
3. **Kiểm nấc trong pipeline con.** Con có project variable riêng nếu là project khác — nấc 2 của con thắng mọi thứ cha gửi xuống.
4. **Chặn cho lần sau:** `${VAR:?}` ở dòng đầu mỗi job của **pipeline con**, không phải của cha.

**Tiêu chí chấm:**
- 0đ: "Pipeline con thấy mọi biến của cha."
- 1đ: Biết có chuyện kế thừa, không nêu cách đo.
- 2đ: Nêu đúng `inherit:variables` điều khiển việc kế thừa và đề xuất in `env` trong pipeline con.
- 3đ: Như trên, **và** kể được **3** chỗ khai kèm khẳng định số biến xuống được là thứ **phải đo**, **và** nhớ kiểm project variable của chính pipeline con.

**Câu hỏi đào sâu:** Pipeline con là **project khác** thì có gì đổi? *(Nó có project variable riêng ở nấc 2, có nhánh được bảo vệ riêng nên `protected` tính theo nhánh của **nó**.)*

---

### Câu 12 — 🔥

**Hỏi:** `CI_DEBUG_TRACE: "true"` — bạn dùng nó khi nào, và cái giá của nó là gì?

**Đáp án chuẩn:** Nó in **toàn bộ** môi trường của job vào log — cách **nhanh nhất** trả lời "biến này bằng gì và tới từ nấc nào", và cũng là cách nhanh nhất làm lộ mọi secret cho bất cứ ai đọc được log.

**Vế lợi:** không công cụ nào khác cho ta cả chín nấc cùng lúc; khi bảng chín nấc và `${#VAR}` không phân giải được ca đang gặp thì đây là nước tiếp theo, tốn **1** pipeline. **Vế giá, bằng số:** log job phình từ **12 kB** lên khoảng **400 kB**, in khoảng **250–400** dòng biến — phụ thuộc số biến của project và số dòng `script`, lấy làm **bậc độ lớn** chứ không phải hằng số. Trong đó có `CI_JOB_TOKEN` nguyên văn, nội dung biến kiểu file, và cả giá trị đã bị biến đổi mà `masked` không che nổi — đúng **3** đường lộ của QT 5.1. Và log **còn đó tới khi có người xoá**.

**Cách dùng có kỷ luật, bốn điều kiện cùng lúc:**

1. Trên **nhánh riêng** — nhánh mặc định thường được bảo vệ nên nó có đúng những biến ta ít muốn in nhất.
2. Cho **một** job, bật bằng biến đặt lúc **bấm chạy tay**; đừng commit `CI_DEBUG_TRACE` vào YAML — commit vào là chắc chắn có ngày quên xoá.
3. **Xoá log ngay sau khi đọc** — `DELETE /projects/:id/jobs/:job_id/erase` — bước bắt buộc.
4. **Không bật** trên project mà người ngoài đội đọc được log, kể cả một lần.

**Khi nào chọn đường khác:** cần biết **một** biến thì `echo "${#VAR}"` cộng `echo "${VAR:0:4}"` cho độ dài và bốn ký tự đầu — đủ phân biệt rỗng, sai nấc, thừa byte, tốn **0,01 giây** và **0** rủi ro. Chỉ leo lên `CI_DEBUG_TRACE` khi cần **cả tập** biến.

**Tiêu chí chấm:**
- 0đ: "Bật lên cho nhanh, tiện mà." Hoặc "không bao giờ dùng" mà không nêu được cách dùng an toàn.
- 1đ: Biết nó in nhiều biến và có rủi ro, không có con số và không có quy trình.
- 2đ: Nêu đúng cả hai vế lợi–giá kèm con số **12 kB → ~400 kB**, và ít nhất hai điều kiện dùng.
- 3đ: Như trên, **và** đủ **4** điều kiện gồm bước xoá log bằng API, **và** nêu đường rẻ hơn `${#VAR}` cho ca chỉ cần một biến, **và** nói rõ 400 kB là bậc độ lớn phải đo lại.

**Câu hỏi đào sâu:** Đã xoá log job rồi thì secret an toàn chưa? *(Chưa. Coi mọi secret đã in ra là đã lộ và **thay** nó — log có thể đã bị người khác mở, đã vào bản sao lưu, hoặc đã được một tích hợp bên ngoài đọc. Buổi 29 làm việc thay secret rẻ đến mức không phải cân nhắc.)*

---

## V3. Câu chốt để nói khi phỏng vấn

> Bốn câu dưới đây viết **nguyên văn, đúng ngữ điệu nói**. Học viên tập nói to từng câu tới khi trôi chảy mà không phải nghĩ.
> Mỗi câu chứa **một con số** hoặc **một cơ chế** — đó là thứ phân biệt câu trả lời của người đã đo với câu trả lời của người đã đọc.

**Câu 1 — khi được hỏi "biến trong GitLab CI hoạt động thế nào":**

> "Điều đầu tiên tôi nói là: tôi **không** đọc giá trị của một biến bằng cách đọc `.gitlab-ci.yml`. Biến đến từ **chín** nguồn, và **bốn** nguồn cao nhất nằm **ngoài** repo — pipeline variable lúc bấm chạy, rồi project, group, instance. Nên câu tôi hỏi không phải 'biến này bằng gì' mà là 'biến này **thắng ở nấc nào**' — và tôi trả lời nó bằng cách in biến ra trong job hoặc gọi API liệt kê biến, chứ không bằng cách đọc YAML rồi suy luận."

**Câu 2 — khi được hỏi "kể một lỗi CI làm bạn mất nhiều thời gian":**

> "Tôi mất nửa ngày cho một biến. Tôi sửa nó trong `.gitlab-ci.yml`, push, job vẫn in giá trị cũ. Hoá ra có một project variable cùng tên do người khác tạo từ trước — **nấc 2 thắng nấc 7**, và nền tảng chạy đúng thiết kế: nó cố ý xếp cấu hình vận hành trên cấu hình trong repo. Từ hôm đó, việc đầu tiên tôi làm với một ca biến sai là gọi `GET /projects/:id/variables` rồi `grep` các tên đó trong repo — tên nào xuất hiện ở **cả hai** chỗ là một quả bom hẹn giờ. Mất ba mươi giây, và nó thay cả nửa ngày kia."

**Câu 3 — khi được hỏi "bạn quản lý secret trong CI thế nào":**

> "Trước hết tôi nói rõ một điều hay bị hiểu sai: `masked` **không phải** cơ chế bảo vệ secret. Nó là **một** phép thay thế chuỗi trên đường log đi từ runner về server, và có **ba** đường nó không bịt được. Một, giá trị nằm trong **artifact** — tôi tải artifact về rồi `grep` là thấy nguyên văn, vì artifact không phải log. Hai, giá trị bị **biến đổi** trước khi in: `base64` một cái là nó ra khỏi phép so khớp. Ba, nó không giới hạn **ai đọc được** giá trị trong giao diện. Nên tôi vẫn bật `masked` — nó chặn rò rỉ do vô tình, rất đáng — nhưng tôi không dựng quy trình nào lên nó. Bảo vệ thật cần secret **vòng đời ngắn, sinh lúc chạy**, kiểu Vault hoặc OIDC."

**Câu 4 — khi được hỏi "bạn cải thiện được gì cho pipeline của đội cũ":**

> "Một dòng, và nó rẻ đến mức vô lý. Chúng tôi có job deploy chạy trên nhánh feature: **xanh**, mà không có gì được deploy. Nguyên nhân là biến token bật `protected`, nhánh feature không được bảo vệ, nên nền tảng **không gửi** biến đó cho job. Job nhận chuỗi **rỗng** — `${#TOKEN}` bằng **0** thay vì **20** — và shell không coi rỗng là lỗi, nên nó chạy tiếp và xanh. Cái tôi thêm vào là một dòng `: \"${TOKEN:?}\"` ở đầu `script`, tốn khoảng **một phần trăm giây**, và nó chuyển lỗi từ ô 'im lặng, không chặn' sang ô 'job đỏ ngay'. Lần đầu bật lên, chúng tôi tìm ra ba job đã chạy hàng tuần với biến rỗng mà không ai biết. Từ đó nguyên tắc của tôi là: **rỗng không phải lỗi** — muốn nó là lỗi thì phải tự viết ra."

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
| ≥ 80% | Nắm vững. Giao BT mở rộng §L10 về `inherit:variables`, làm trước buổi 09 |
| 60–79% | Đạt. Đọc lại quy tắc bị mất điểm trước buổi 07 |
| 40–59% | Chưa đạt. Làm lại bước lab 1 (bảng chín nấc) và bước 2 (biến protected rỗng) ở nhà |
| < 40% | Chưa đạt. Học lại cả buổi trước khi sang buổi 07 — buổi 07, 29 và nhóm 37–43 dựng thẳng lên bảng chín nấc này |

**Bảng lỗi làm trần điểm là 1:**

| Lỗi | Vì sao nghiêm trọng đến mức trần điểm |
|---|---|
| "`masked` bảo vệ được secret", hoặc "biến masked không lộ ra artifact" | `masked` là **1** phép thay thế chuỗi trên đường log và có **3** đường lộ nó không bịt. Người tin ngược lại ghi token vào artifact rồi yên tâm vì log hiện `[MASKED]` — rò rỉ im lặng, không chặn, tồn tại tới khi có người xoá |
| "Biến `protected` thiếu thì job sẽ đỏ" | Nền tảng **không gửi** biến, job nhận **rỗng**, `${#TOKEN}` bằng **0**. Người tin job sẽ đỏ thì không viết dòng `${VAR:?}` nào — ca đắt nhất khi gặp ở prod: job deploy **xanh** mà không deploy gì |
| Nói định lượng ("log to lắm", "token sai một chút") mà hỏi lại vẫn không có số | Mọi ca của buổi này đều có một con số chẩn đoán rẻ: **21 so với 20**, **6 so với 8**, **12 kB so với 400 kB** |

---

## V5. Bài tập về nhà

### BTVN 1. Bảng chín nấc của repo thật

Lấy một repo đang chạy. Liệt kê biến ở mọi nấc **đọc được** bằng API, rồi đối chiếu với YAML:

```bash
for LV in "projects/$PID" "groups/$GID"; do
  curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/$LV/variables" \
  | jq -r --arg lv "$LV" '.[] | "\($lv)\t\(.key)\t\(.protected)\t\(.masked)\t\(.variable_type)"'
done | sort -k2 ; grep -nE '^\s{2,}[A-Z][A-Z0-9_]*:' .gitlab-ci.yml
```

**Nộp:** một bảng cột *tên biến · nấc · masked · protected · kiểu*, và một danh sách riêng: **mọi tên xuất hiện ở cả hai** chỗ — **số dòng** của danh sách đó là số "đo trước" của §8, mục tiêu đưa về **0**.

### BTVN 2. Đếm biến quan trọng đang không được kiểm

Trong repo đó, đếm hai con số: (1) số biến mà **thiếu nó thì job sai chứ không đỏ**; (2) số biến trong nhóm đó đã có `: "${VAR:?}"` hoặc `test -n` đứng **trước** lần dùng đầu tiên trong `script`.

**Nộp:** hai con số và tỉ số của chúng, kèm danh sách tên job thuộc phần chênh lệch. Với **một** job trong đó, viết ra dòng khẳng định phải thêm — đúng tên biến thật, không viết `VAR` cho có.

### BTVN 3. Ba ca "biến sai" tái hiện trên repo của mình

Trên một **nhánh riêng** của repo đó, tái hiện **ba** trong năm ca của lab, mỗi ca một job, ghi bằng chứng bằng số:

1. **Biến protected rỗng** — in `${#VAR}` trên nhánh được bảo vệ và trên nhánh riêng, ghi hai con số.
2. **Ký tự vô hình** — hai biến cùng giá trị, một có xuống dòng cuối; in `${#VAR}` của cả hai và chạy `od -c`.
3. **Mở rộng biến** — hai biến giá trị `Pa$$w0rd`, một khai `expand: false`; in `${#VAR}` của cả hai.

**Nộp:** tệp `nam-ca-bien-sai.md` có ba mục, mỗi mục đúng bốn dòng: *triệu chứng · bằng chứng bằng số · nguyên nhân · cách sửa*. Kèm một câu trả lời: ca nào trong ba ca đó **đã** tồn tại sẵn trong repo của bạn?

### BTVN 4. Chuẩn bị cho buổi 07

Trả lời ba câu sau bằng viết, mỗi câu 3–5 dòng. Mang theo vào buổi 07.

1. Hôm nay QT 7.2 cho thấy `CI_DEBUG_TRACE` cho ta **mọi** biến nhưng cũng cho ta khoảng **400 kB** log. Hãy đọc log **một** job thật của bạn — lấy qua `GET /projects/:id/jobs/:job_id/trace` — và chia nó thành các **phần** theo **tám pha** của buổi 01: mỗi pha bắt đầu ở **dòng số bao nhiêu**? Ghi cả số dòng của phần bạn **không** xếp được vào pha nào.
2. Hôm nay QT 5.2 cho thấy một job có thể hỏng vì biến rỗng. Nếu bạn khai `retry: 2` cho job đó, `retry` có sửa được không? **Vì sao?** Ghi phỏng đoán, rồi kể thêm **một** loại lỗi bạn tin `retry` sửa được và **một** loại bạn tin nó không sửa được, kèm lý do phân biệt hai loại.
3. Chọn **một** pipeline hỏng mà bạn từng mất nhiều thời gian nhất. Viết lại theo mẫu **bốn dòng**: *triệu chứng → bằng chứng → nguyên nhân → cách sửa*. Mỗi dòng một câu, và dòng "bằng chứng" bắt buộc có một con số hoặc một lệnh.

**Ba câu này dẫn vào đâu:** câu 1 dẫn thẳng vào **§4 buổi 07 — cấu trúc log job theo tám pha**; cái đáng giá không phải bảng tám pha (buổi 01 đã có) mà là việc tự tìm ranh giới trên log thật, vì phần **không xếp được vào pha nào** chính là phần buổi 07 sẽ mổ. Câu 2 dẫn vào **§5 buổi 07 — `retry` sửa được nhóm lỗi nào và không sửa được nhóm nào**: `retry` chỉ có tác dụng với lỗi **không xác định** (mạng, runner chết, hạn giờ), còn biến rỗng là lỗi **xác định**. Câu 3 dẫn vào **§6 buổi 07 và mẫu báo cáo gỡ rối bốn dòng** mà cả buổi 07 dùng — ca thật học viên mang tới sẽ thành ca thứ bảy của lớp.
{% endraw %}
