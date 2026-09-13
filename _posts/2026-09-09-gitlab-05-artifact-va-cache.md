---
layout: post
title: "[Bài 05] Quản Trị Dữ Liệu Tạm Thời: Phân Biệt Artifacts vs Caching, S3 MinIO Backend & Tối Ưu Tốc Độ Build"
date: 2026-09-09 08:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-05
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 5
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.05] Hướng dẫn chuyên sâu Quản Trị Dữ Liệu Tạm Thời: Phân Biệt Artifacts vs Caching, S3 MinIO Backend & Tối Ưu Tốc Độ Build: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

# [BÀI 05] QUẢN TRỊ DỮ LIỆU TẠM THỜI: PHÂN BIỆT ARTIFACTS VS CACHING, S3 MINIO BACKEND & TỐI ƯU TỐC ĐỘ BUILD

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · executor `docker`.
> Mọi đoạn YAML dán được vào `.gitlab-ci.yml` và chạy trong dưới 90 giây.
> Lệnh `curl` dùng bốn biến đã có từ buổi 01: `$GITLAB`, `$GITLAB_TOKEN`, `$PID`, `$PIPE`.

---





Năm câu này là năm mảnh nền mà buổi hôm nay dựng trực tiếp lên. Ai sai câu 1 sẽ tắc ở QT 4.2; ai sai câu 3 sẽ tắc ở QT 5.2.

| # | Câu hỏi | Đáp án vắn tắt | Dẫn vào đâu hôm nay |
|---|---|---|---|
| 1 | `rules` được đánh giá mấy lần, lúc nào | **1** lần, tại `t0` lúc **tạo** pipeline (buổi 04 QT 4.1) | §4 QT 4.2 — `cache:key` **không** tính ở `t0`, đây là điểm đối lập |
| 2 | Vì sao biến `dotenv` không dùng được trong `rules` | Tới **quá muộn**; chỉ **2** loại biến dùng được (buổi 04 QT 4.2) | §5 QT 5.4 — `dotenv` là một loại `artifacts:reports` |
| 3 | Ba trạng thái "job không chạy" | Không có mặt · `manual` · `skipped`. **1** câu phân biệt: *nó có trong danh sách job không* | §5 QT 5.2 — job nguồn artifact **không có mặt** thì job sau nhận gì |
| 4 | Mở MR không có `workflow` sinh mấy pipeline | **2** pipeline cho **1** commit = gấp đôi phút runner | Lab §L1 — thiếu `workflow` thì mọi con số giây ở bước 4 bị đếm hai lần |
| 5 | `rules:changes` sai âm thầm ở mấy ca | **3** ca; `compare_to` sửa được **2** | §5 — cùng họ lỗi: khai đúng cú pháp mà kết quả rỗng, job vẫn xanh |



Buổi 04 chốt: danh sách job đóng băng tại `t0`. Câu hỏi tiếp theo không còn là "job nào chạy" mà là *cái gì chảy giữa những job đã đóng băng đó*. Buổi 01 QT 5.1 liệt kê bốn đường vào một job — mã nguồn, `cache`, `artifacts`, biến. Buổi 06 sẽ mổ đường thứ tư. Hôm nay ta mổ **hai đường ở giữa**, và chúng gây ra nhiều giờ gỡ lỗi hơn hai đường kia cộng lại — vì cú pháp của chúng gần như giống nhau (cùng một khối YAML với `paths:`) trong khi **đảm bảo** thì ngược nhau hoàn toàn.

**Luận đề trung tâm.**

> **`artifacts` là HỢP ĐỒNG: nó đi qua server GitLab, được đảm bảo, và kiểm chứng được từ bên ngoài job. `cache` là TỐI ƯU: nó nằm trên runner, KHÔNG được đảm bảo, và runner không báo lỗi khi thiếu. Dùng cache ở chỗ cần hợp đồng thì pipeline vẫn xanh — nhưng không tái lập được, và ngày nó hỏng là ngày không ai đoán được.**

Buổi 01 QT 5.2 đã **phát biểu** câu này nhưng chưa mở cơ chế — đó là lần thứ nhất. Hôm nay là **lần thứ hai**, và lần này ta mở nắp: ai lưu, lưu ở đâu, tính khoá lúc nào, tốn bao nhiêu giây.

```
   Server GitLab  ─┐  artifacts: upload cuối job → download đầu job sau
                   │  ĐẢM BẢO · kiểm chứng được bằng API · tính vào dung lượng project
                   │
   Job A ──────────┼──────────► Job B
                   │
   Đĩa runner     ─┘  cache: nén cuối job → giải nén đầu job sau, CÙNG runner
                      KHÔNG ĐẢM BẢO · không có API đọc · tính vào đĩa runner

   Thứ tự runner làm ở đầu job:  clone → RESTORE CACHE → DOWNLOAD ARTIFACTS → script
                                              └── artifact ghi đè cache khi trùng đường dẫn
```

**Kết quả buổi trước được dùng lại.** Mỗi dòng là một tiền đề; thiếu nó thì phần tương ứng hôm nay nghe như một quy ước tuỳ ý.

| Kết quả | Nguồn | Dùng ở đâu hôm nay |
|---|---|---|
| `cache` là tối ưu, `artifacts` là hợp đồng | buổi 01 QT 5.2 | **Toàn bộ buổi** — hôm nay mở cơ chế, **lần thứ 2** |
| Mặc định tải artifact mọi stage trước; `dependencies: []` tắt hẳn | buổi 01 QT 5.3 | §5 QT 5.1, QT 5.2 — hôm nay **đo** bằng số tệp |
| Bốn đường vào job | buổi 01 QT 5.1 | §4 — hai trong bốn đường được mổ hôm nay |
| Job xanh không chứng minh việc đã làm; phải có **khẳng định** | buổi 01 QT 7.2, QT 7.3 | §5 QT 5.3 — artifact rỗng là ca kinh điển nhất |
| Bảng hai thuộc tính hỏng | buổi 01 QT 7.1 | §4, §5, §6 — **lần thứ 5** |
| Danh sách job chốt ở `t0` | buổi 04 QT 4.1 | §4 QT 4.2 — `cache:key` **không** chốt ở `t0` |
| Job biến mất vì `rules` không khớp | buổi 04 QT 6.2, QT 7.1 | §5 QT 5.2 — job nguồn artifact biến mất thì job sau ra sao |
| `workflow` chuẩn của khoá | buổi 04 lab B5 | Lab §L1 — dán nguyên vào để không sinh pipeline trùng khi đo giây |
| Ba nấc ưu tiên `cache` (`config.toml` → `default` → job) | buổi 03 QT 7.1 | §6 QT 6.4 — cache dùng chung khai ở nấc xa nhất |

**Nguyên lý xuất hiện lần thứ mấy.** Giảng viên **nói ra con số** để học viên thấy chúng là công cụ, không phải khẩu hiệu:

- **Bảng hai thuộc tính hỏng** — **lần thứ 5**. Buổi này góp **5** ca mới, **4** ca nằm ở ô nguy hiểm nhất.
- **"Hành vi phụ thuộc phiên bản thì phải ĐO, không tra"** — **lần thứ 5**. Hôm nay có **3** quy tắc loại (c): QT 5.3, QT 5.4, QT 7.2.
- **"Job xanh không chứng minh gì, phải có khẳng định"** — **lần thứ 3**. Hôm nay nó có hình thức cụ thể nhất của giai đoạn 1: **1** dòng `test -s`, giá **0,1 s**.

**Ba câu hỏi trung tâm của buổi:**

1. Cái gì lưu ở đâu, và ai đảm bảo nó còn đó khi job sau cần?
2. Vì sao một job có `artifacts` khai đúng cú pháp vẫn có thể upload **0 byte** mà job vẫn **xanh**?
3. Cache tiết kiệm hay làm chậm — với repo của tôi, con số là bao nhiêu giây?

**Ba câu BTVN 4 buổi 04 đáp thẳng vào ba mục hôm nay.** Gọi ba học viên đọc phỏng đoán đã ghi, **không sửa ngay**, ghi lên bảng để đối chiếu cuối buổi.

| Câu BTVN 4 buổi 04 | Trả lời ở đâu hôm nay |
|---|---|
| `cache:key` được tính lúc nào | §4 QT 4.2 |
| Job nguồn artifact biến mất thì `dependencies` / `needs` ra sao | §5 QT 5.2, và lab bước 1 **phải đo** chứ không đoán |
| Ba thư mục nên đi bằng cache, ba thư mục nên đi bằng artifact | §7 QT 7.1, hiện vật `bang-phan-loai.md` |

---



| # | Làm được gì | Hiện vật chứng minh |
|---|---|---|
| LĐ1 | Trả lời "cái này đi bằng `artifacts` hay `cache`" bằng **ba câu hỏi**, không tra tài liệu | `bang-phan-loai.md` — 10 thư mục của sáu ngôn ngữ, lab bước 5 |
| LĐ2 | Chứng minh bằng API rằng một job **xanh** có artifact **rỗng**, và chặn được ca đó | Hai khẳng định độc lập, lab bước 2 CHECKPOINT 4 và 5 |
| LĐ3 | Đo ba con số giây: `Restoring cache`, `Downloading artifacts`, `Creating cache` | `doc-pha.sh` và `bang-do-cache.tsv`, lab bước 4 |
| LĐ4 | Tính **điểm hoà vốn** của một cache cụ thể và nói được nó lãi hay lỗ | Bốn dòng đo lại của bảng QT 6.3, lab bước 4 CHECKPOINT 9 |
| LĐ5 | Thu hẹp lượng artifact tải về bằng đúng công cụ trong ba công cụ | Ba job đếm số tệp nhận được, lab bước 1 CHECKPOINT 3 |
| LĐ6 | Chỉ ra vì sao `cache:key: $CI_COMMIT_SHA` cho tỉ lệ trúng **0%** mà log không có chữ "lỗi" | `trace` của 5 lần chạy, lab bước 3 CHECKPOINT 7 |
| LĐ7 | Chứng minh thứ tự **4** bước ở đầu job, và ai thắng khi trùng đường dẫn | `trace` có cả hai pha, lab bước 5 CHECKPOINT 11 |
| LĐ8 | Đặt `expire_in` đúng cho hai loại hiện vật và nói ra chênh lệch dung lượng | So `statistics.job_artifacts_size` trước và sau, lab bước 5 |

---



| Cần biết | Mức yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Bốn đường vào một job; `cache` là đường 2, `artifacts` là đường 3 | **Vận dụng** | buổi 01 QT 5.1 — tiền đề của cả §4 |
| Tám pha của một job; pha 4, 5, 8 là ba pha hôm nay đo | **Vận dụng** | buổi 01 QT 4.2 |
| Bảng hai thuộc tính hỏng | Vận dụng | buổi 01 QT 7.1 |
| Khẳng định làm job đỏ khi kết quả sai | **Vận dụng** | buổi 01 QT 7.3 — dùng ở mọi ví dụ của §5 |
| `rules` chốt danh sách job ở `t0` | Vận dụng | buổi 04 QT 4.1 — cần để thấy `cache:key` khác chỗ nào |
| Ba nấc ưu tiên cấu hình runner | Nhớ | buổi 03 QT 7.1, buổi 02 QT 4.3 |
| Đọc `trace` qua API bằng `curl`, lọc bằng `grep` và `jq` | **Vận dụng** | buổi 01 QT 4.2 — mọi phép đo hôm nay dựa vào nó |
| `du -sh`, `find | wc -l`, `test -s` trong shell | Nhớ | Bất kỳ tài liệu shell cơ bản |

---



### 3.1. Đối chiếu thuật ngữ

Từ khoá YAML **giữ nguyên tiếng Anh**, vì học viên gõ đúng chữ đó vào tệp. Khái niệm không phải từ khoá thì dùng tiếng Việt, kèm tiếng Anh để đi phỏng vấn.

| Tiếng Việt dùng trong bài | Tiếng Anh | Dùng thẳng tiếng Anh? | Ghi chú |
|---|---|---|---|
| hiện vật | artifact | **Có** — `artifacts` | Tệp job sinh ra, GitLab giữ, có API tải |
| bộ nhớ đệm | cache | **Có** — `cache` | Tệp nén giữ trên runner để lần sau nhanh hơn |
| khoá cache | cache key | **Có** — `cache:key` | Định danh của một gói cache |
| chính sách cache | cache policy | **Có** — `cache:policy` | `pull-push` (mặc định) · `pull` · `push` |
| khoá dự phòng | fallback key | **Có** — `cache:fallback_keys` | Khoá thử tiếp khi khoá chính trượt |
| phụ thuộc hiện vật | artifact dependency | **Có** — `dependencies` | Thu hẹp *tải của ai*, không đổi thứ tự |
| báo cáo có cấu trúc | report | **Có** — `artifacts:reports` | GitLab phân tích nội dung, không chỉ lưu |
| hạn giữ | expiration | **Có** — `expire_in` | Hạn **giữ**, không phải hạn dùng |
| tệp khoá phiên bản | lockfile | Việt + Anh, dùng "lockfile" | `package-lock.json`, `go.sum`, `pom.xml` |
| tỉ lệ trúng | hit rate | Việt | Số lần trúng chia tổng số lần chạy |
| trúng cache · trượt cache | cache hit · cache miss | Việt | Đọc từ `trace`, không có API riêng |
| cache dùng chung | distributed cache | Việt | Cache đặt trên object storage thay vì đĩa runner |
| điểm hoà vốn | break-even | Việt | Số lần trúng tối thiểu để cache có lãi |
| nén và tải lên | archive and upload | Việt | Pha `archive_cache` ở cuối job |
| tái lập được | reproducible | Việt | Chạy lại cho cùng kết quả, không phụ thuộc máy |
| khẳng định | assertion | Việt | Lệnh tự làm job đỏ khi kết quả sai |
| dung lượng project | artifacts size | Việt | Trường `statistics.job_artifacts_size` |
| kho đối tượng | object storage | Việt | S3, MinIO — nơi đặt cache dùng chung |
| thứ tự phục hồi | restore order | Việt | Bốn bước ở đầu job, xem QT 7.2 |
| hiện vật trung gian · hiện vật phát hành | intermediate · release artifact | Việt | Hai loại có `expire_in` khác nhau (QT 5.5) |



Mô hình phải dùng được trong **5 giây**, vì ta gọi nó ra mỗi lần thêm một thư mục vào `.gitlab-ci.yml`. Nó gồm đúng một câu hỏi:

> *"Job sau **SAI** nếu thiếu nó, hay chỉ **CHẬM** hơn?"*

Sai thì `artifacts`. Chậm thì `cache`. Không có ô thứ ba và không có ô "vừa vừa".

Giá trị thực dụng: nó biến một cuộc tranh luận vô hạn ("cái nào tốt hơn") thành câu hỏi có đáp án khách quan. Cách kiểm rẻ nhất là thí nghiệm trong đầu: xoá thư mục đó rồi tưởng tượng job sau chạy — nó đỏ, hay chỉ mất thêm 20 giây? Không trả lời được nghĩa là ta chưa biết job sau làm gì, và đó mới là việc phải sửa trước. Mô hình quay lại ở buổi 08, 15–22, 25, 34.

### 3.3. Mô hình tư duy 2: hai kho, hai chủ

Artifact và cache khác nhau ở **chủ giữ**; mọi khác biệt còn lại là hệ quả.

| | `artifacts` | `cache` |
|---|---|---|
| Ai giữ | **Server GitLab** | **Runner** (hoặc kho đối tượng nếu đã cấu hình) |
| Có bản ghi trong cơ sở dữ liệu | Có | Không |
| Có API đọc | **Có** — `GET /jobs/:id/artifacts` | **Không có API nào** |
| Hạn sống | Khai được — `expire_in` | Do runner dọn, không khai được chính xác |
| Tính vào đâu | Dung lượng project | Đĩa runner |
| Thiếu thì sao | Job phụ thuộc đỏ ở pha 5 | Ghi một dòng log rồi chạy tiếp |

Giá trị thực dụng: khi cần **chứng minh** một việc đã xảy ra — cho người review, cho auditor, cho chính mình ba tuần sau — thứ duy nhất dùng được là artifact, vì chỉ nó có API. "Tôi tin là job đó có chạy" không phải bằng chứng; `GET /jobs/4711/artifacts` trả `200` với 12 MB thì là bằng chứng. Mô hình quay lại ở buổi 13, 14, 17, 19.

### 3.4. Mô hình tư duy 3: sổ thu chi của cache

Cache **không** miễn phí. Nó là khoản đầu tư có giá đọc được bằng giây, ghi sổ bằng một bất đẳng thức:

```
tiết kiệm mỗi lần chạy = p × (tạo_lại − giải_nén) − nén_và_tải

p            tỉ lệ trúng, từ 0 đến 1
tạo_lại      giây để dựng lại thư mục từ đầu (npm ci, mvn dependency:go-offline...)
giải_nén     giây để tải cache về và bung ra
nén_và_tải   giây để nén thư mục và đẩy lên kho cache, ở CUỐI job
```

Ba việc mô hình này cho phép làm mà cảm giác không cho: (1) nói *"cache này lãi 51 giây mỗi lần trúng"* thay vì *"cache giúp nhanh hơn"*; (2) chỉ ra chính xác vì sao một cache **lỗ** — vì `p` nhỏ, hầu như không bao giờ vì thư mục to; (3) quyết định `policy` — `policy: pull` chính là cách đưa số hạng `nén_và_tải` về **0**. Không tính ra số thì ta đang **tin**, không phải **biết**. Mô hình quay lại ở buổi 14, 17, 19, 46.

---

### 1.1. Hai đường vận chuyển, hai đảm bảo (9 phút)

### 4.1. Chủ giữ khác nhau thì đảm bảo khác nhau

**Nguyên lý cốt lõi:** `artifacts` đi **lên server GitLab** rồi đi xuống job sau; `cache` **không đi đâu cả** — nó nằm trên đĩa của chính runner đã chạy job (hoặc trên object storage nếu đã cấu hình distributed cache). Khác nhau về **chủ giữ** sinh ra khác nhau về **đảm bảo**.

**Giải thích cơ chế ngầm:** Ở pha 8, runner làm hai việc riêng biệt. Với `artifacts`, nó nén tập tệp khớp `paths` rồi **gửi lên GitLab qua HTTP**; GitLab tạo một bản ghi trong cơ sở dữ liệu, gắn `expire_in`, mở một URL tải. Với `cache`, nó nén thư mục rồi **ghi ra một tệp trên đĩa cục bộ** theo đường dẫn dẫn xuất từ `cache:key` — không HTTP, không bản ghi, không ai ghi sổ. Đó là lý do artifact có API đọc còn cache không: cái gì server không biết thì server không kể lại được. Đây là loại (a) — tài liệu *Job artifacts* và *Caching in GitLab CI/CD*.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job sau hỏng vì thiếu tệp, mà `GET /projects/:id/jobs/:job_id/artifacts` của job trước trả `404` — nghĩa là thứ ta **tưởng** là artifact vốn đi bằng cache. Dấu hiệu thấy trước cả khi hỏng: `trace` của job sau có dòng `Restoring cache` nhưng **không có** dòng `Downloading artifacts for <job trước>`.

**Minh hoạ.**

```yaml
stages: [tao, doc]

tao-hai-kho:
  stage: tao
  image: alpine:3.20
  script:
    - mkdir -p qua-artifact qua-cache
    - echo "đi qua server GitLab" > qua-artifact/noi-dung.txt
    - echo "nằm trên đĩa runner"  > qua-cache/noi-dung.txt
  cache:    { key: bai-05-co-dinh, paths: [qua-cache/] }
  artifacts: { paths: [qua-artifact/], expire_in: 1 hour }

doc-hai-kho:
  stage: doc
  image: alpine:3.20
  cache: { key: bai-05-co-dinh, paths: [qua-cache/], policy: pull }
  script:
    - cat qua-artifact/noi-dung.txt                       # từ artifact — đảm bảo
    - cat qua-cache/noi-dung.txt || echo "cache không có — job VẪN XANH"
```

```bash
# Bất đối xứng của hai kho. Artifact có URL tải; cache không có endpoint nào.
curl -s -o /dev/null -w 'artifacts → HTTP %{http_code}, %{size_download} byte\n' \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID/jobs/$JOB/artifacts"
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB/trace" \
| grep -aE 'Restoring cache|Creating cache|Successfully extracted cache'
```

**Con số chốt.** **2** kho, đúng **1** trong 2 có API đọc. Đó là câu trả lời ngắn nhất cho câu vấn đáp *"artifact khác cache ở đâu"* — trả lời bằng **chủ giữ**, không bằng định nghĩa.

### 4.2. `cache:key` không chốt ở `t0`

**Nguyên lý cốt lõi:** `cache:key` được tính **lúc job bắt đầu, trên runner**, không phải ở `t0` như `rules`. Với `cache:key:files`, khoá là hash **nội dung** các tệp được liệt kê tại commit đang checkout.

**Giải thích cơ chế ngầm:** Runner phải chạy xong pha `get_sources` mới có tệp trên đĩa để hash, nên việc tính khoá bắt buộc xảy ra **sau** `t0` — thật ra sau `t0` một khoảng bằng thời gian chờ runner rảnh cộng thời gian clone. Đây là điểm đối lập trực tiếp với buổi 04 QT 4.1: cùng một job, `rules` được GitLab tính ở `t0` còn `cache:key` được runner tính muộn hơn nhiều. Hệ quả thực dụng: `rules` **không** đọc được biến `dotenv`, `cache:key` thì đọc được — vì nó tính sau. Loại (b), suy từ cơ chế: muốn hash nội dung tệp thì phải có tệp trước.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> `cache:key: $CI_COMMIT_SHA` thì mọi commit là khoá mới, tỉ lệ trúng về **0%** vĩnh viễn, mà log **không hề có chữ "lỗi"**. Quan sát được: mọi lần chạy đều có dòng trượt cache trong `trace`; thời gian job không giảm sau 20 lần chạy; đĩa runner phình vì mỗi lần để lại một gói cache không ai dùng lại.

**Minh hoạ.**

```yaml
build-khoa-theo-lockfile:
  image: node:22-alpine
  cache:
    key:
      files:
        - package-lock.json        # tối đa 2 tệp ở GitLab 17.7
    paths: [.npm/]
    policy: pull-push
    fallback_keys:                 # tối đa 5 khoá
      - npm-$CI_DEFAULT_BRANCH
      - npm-chung
  script:
    - npm ci --cache .npm --prefer-offline
    - echo "khoá thật sự dùng nằm ở dòng 'Checking cache for ...' trong trace"
```

```bash
# Khoá là hash NỘI DUNG: đổi đúng một ký tự trong lockfile thì khoá phải khác.
for J in "$JOB_TRUOC" "$JOB_SAU"; do
  curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/jobs/$J/trace" | grep -a 'Checking cache for'
done
```

**Con số chốt, và giới hạn của nó.** `cache:key:files` nhận **tối đa 2** tệp ở GitLab 17.7; `cache:fallback_keys` nhận **tối đa 5** khoá. Cả hai là **giới hạn của phiên bản, không phải quy luật tự nhiên** — monorepo có 9 lockfile thì phải tự ghép khoá (hash tất cả lockfile vào một tệp rồi trỏ `files` vào tệp đó), và buổi 22 làm đúng việc ấy.

### 4.3. Cả hai đều hỏng im lặng, chỉ khác mức độ

**Nguyên lý cốt lõi:** Thiếu cache là **không lỗi**: runner ghi một dòng thông báo rồi chạy tiếp. Thiếu artifact **cũng có thể không lỗi** nếu `script` không kiểm. Cả hai đều là ô **im lặng, không chặn** — ô nguy hiểm nhất của bảng hai thuộc tính (buổi 01 QT 7.1, lần thứ 5).

**Giải thích cơ chế ngầm:** Với cache đây là thiết kế có chủ đích: một tối ưu không nên làm hỏng việc khi nó vắng mặt, và runner **không có cách nào** phân biệt "lần chạy đầu tiên" với "lần thứ hai mươi bị mất cache". Với artifact thì pha 5 **có thể** làm job đỏ — nhưng nếu artifact vốn **rỗng** (QT 5.3) hoặc job nguồn **không có mặt** (QT 5.2) thì pha 5 chạy êm, và job đỏ hay không hoàn toàn phụ thuộc `script` có kiểm hay không. Loại (b).

| | **Có chặn** | **Không chặn** |
|---|---|---|
| **Ồn ào** | Artifact cần mà job nguồn đỏ → job sau đỏ ở pha 5. Phát hiện: **giây** | Cảnh báo `no matching files` trong `trace` — in ra nhưng không ai đọc. Phát hiện: **tuần** |
| **Im lặng** | Buổi này gần như không có ca nào rơi vào ô này | **Ô nguy hiểm nhất.** Trượt cache · artifact rỗng · báo cáo test không upload · cache cũ lẫn artifact. Phát hiện: **tuần**, thường ở prod |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job xanh 9 lần rồi lần thứ 10 hỏng ở một job **khác**, xa chỗ gây lỗi — và người sửa không phải người gây ra. Cách nhận biết trong 30 giây: đọc `trace` của job **nguồn**, không phải job đỏ.

**Minh hoạ.**

```yaml
# Cố ý trượt cache. Kết quả đúng: job XANH, và trace có dòng thông báo trượt.
truot-cache-co-y:
  image: alpine:3.20
  cache:
    key: khoa-chua-bao-gio-ton-tai-$CI_JOB_ID
    paths: [thu-muc-khong-co/]
  script:
    - ls -la thu-muc-khong-co/ 2>/dev/null || echo "cache trượt — không có gì để giải nén"
    - exit 0
```

```bash
# Hai khẳng định: job XANH, và trace CÓ dòng trượt, với 0 dòng ERROR.
ST=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB" | jq -r .status)
TR=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB/trace")
echo "status = $ST"
echo "$TR" | grep -aciE 'no URL provided|file does not exist|Failed to extract cache' \
  | sed 's/^/dòng báo trượt cache: /'
echo "$TR" | grep -ac 'ERROR' | sed 's/^/số dòng ERROR: /'
```

**Con số chốt.** Trượt cache sinh ra **0** dòng lỗi và **0** thay đổi mã thoát. Vì vậy không có cách nào phát hiện trượt cache bằng cách "nhìn pipeline" — phải đọc `trace`, và vì phải đọc `trace` nên phải có script đọc `trace`. Đó là `doc-pha.sh` của lab bước 4, hiện vật dùng lại ở buổi 14.

---

### 1.2. `artifacts` là hợp đồng — và hợp đồng rỗng (11 phút)

### 5.1. Mặc định tải nhiều hơn học viên nghĩ

**Nguyên lý cốt lõi:** Mặc định, một job tải artifact của **mọi job ở mọi stage trước nó** — không phải chỉ stage liền trước. Số byte tải về tăng theo **tổng** artifact của các stage trước.

**Giải thích cơ chế ngầm:** Mặc định này có lý do lịch sử: nó làm một pipeline đơn giản chạy được mà không cần khai gì. Cái giá là mọi job ở stage sau trả tiền cho artifact của mọi job ở stage trước, kể cả artifact nó không đụng tới. Điểm hay bị bỏ sót: mặc định tính theo **stage**, không theo khoảng cách — job ở stage 5 tải artifact của cả 4 stage trước, không phải của stage 4. Loại (a) — tài liệu *Job artifacts*, mục `dependencies`.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pha `Downloading artifacts` dài vài chục giây trong một job chỉ cần một tệp 2 kB. Phát hiện nhanh nhất: mở **job nhẹ nhất** của pipeline — job `lint` chẳng hạn — nếu tổng thời gian của nó lâu bất thường so với `script` thì gần như chắc chắn thời gian nằm ở pha 5.

**Minh hoạ.**

```yaml
stages: [xay-a, xay-b, dem]

build-a:
  stage: xay-a
  image: alpine:3.20
  script:
    - mkdir -p ra-a && dd if=/dev/urandom of=ra-a/goi.bin bs=1M count=45 2>/dev/null
    - test -s ra-a/goi.bin || exit 1
  artifacts: { paths: [ra-a/], expire_in: 1 hour }

build-b:
  stage: xay-b
  image: alpine:3.20
  script:
    - mkdir -p ra-b && dd if=/dev/urandom of=ra-b/goi.bin bs=1M count=45 2>/dev/null
    - test -s ra-b/goi.bin || exit 1
  artifacts: { paths: [ra-b/], expire_in: 1 hour }

bao-cao-nho:
  stage: dem
  image: alpine:3.20
  # KHÔNG khai dependencies, KHÔNG khai needs — và nó tải 90 MB
  script:
    - find ra-a ra-b -type f 2>/dev/null | sed 's/^/nhận được: /'
    - du -sh ra-a ra-b 2>/dev/null
```

**Con số chốt.** Với **2** job nguồn mỗi job 45 MB, job sau tải **90 MB** mà không khai gì cả. Theo bảng QT 6.3, 45 MB ứng khoảng **6 giây** tải và bung, nên 90 MB là khoảng **12 giây** cộng vào **mỗi** job ở stage sau. Pipeline có 6 job ở stage sau thì đốt **72 giây** thời gian máy cho việc không ai cần.

### 5.2. Ba cách thu hẹp, khác nhau ở thứ tự chạy

**Nguyên lý cốt lõi:** `dependencies` và `needs` **thu hẹp** tập artifact tải về; `dependencies: []` tắt hẳn về **0 byte**; `needs:artifacts: false` giữ quan hệ thứ tự nhưng bỏ việc tải. Ba cách này khác nhau ở chỗ chúng có đổi **thứ tự chạy** hay không.

**Giải thích cơ chế ngầm:** `dependencies` chỉ nói *tải của ai*. `needs` nói *chạy sau ai* **và** *tải của ai* — nó thay hàng rào stage bằng một đồ thị phụ thuộc, nên nó đổi cả thời điểm job bắt đầu. Đây là chỗ khác nhau duy nhất cần nhớ hôm nay; buổi 08 dành trọn cho `needs`. Loại (a) — mục `dependencies` và `needs:artifacts` trong *CI/CD YAML syntax reference*.

| Cách khai | Tải artifact của ai | Đổi thứ tự chạy | Byte tải về |
|---|---|---|---|
| Không khai gì | Mọi job mọi stage trước | Không | Tổng của tất cả |
| `dependencies: [build-a]` | Đúng `build-a` | **Không** | Của `build-a` |
| `dependencies: []` | Không của ai | Không | **0** |
| `needs: [build-a]` | Đúng `build-a` | **Có** — chạy ngay khi `build-a` xong | Của `build-a` |
| `needs: [{job: build-a, artifacts: false}]` | Không của ai | **Có** | **0** |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thêm `dependencies` mà job vẫn chờ hết cả stage trước → đang nhầm `dependencies` với `needs`. Dấu hiệu ngược cũng hay gặp: thêm `needs` "cho nhanh" rồi mất artifact của một job không có trong danh sách `needs` — vì `needs` **thu hẹp** artifact, không mở rộng.

**Minh hoạ.**

```yaml
stages: [xay, kiem]

build-a:
  stage: xay
  image: alpine:3.20
  script: ['mkdir -p ra-a && seq 1 30 | xargs -I{} touch ra-a/tep-{}.txt']
  artifacts: { paths: [ra-a/], expire_in: 1 hour }

build-b:
  stage: xay
  image: alpine:3.20
  script: ['mkdir -p ra-b && seq 1 12 | xargs -I{} touch ra-b/tep-{}.txt']
  artifacts: { paths: [ra-b/], expire_in: 1 hour }

.dem: &dem
  stage: kiem
  image: alpine:3.20
  script: ['echo "số tệp nhận được: $(find ra-a ra-b -type f 2>/dev/null | wc -l)"']

test-mac-dinh: { <<: *dem }                                        # 42 tệp
test-tat-han:  { <<: *dem, dependencies: [] }                      # 0  tệp
test-chi-mot:  { <<: *dem, dependencies: [build-a] }               # 30 tệp
test-needs-khong-artifact:
  <<: *dem
  needs:
    - job: build-a
      artifacts: false        # giữ thứ tự, bỏ việc tải → 0 tệp
```

**Con số chốt.** **3** cách thu hẹp, và `dependencies: []` cho đúng **0** byte. Bốn job trên cho bốn con số đếm được: **42 · 0 · 30 · 0** tệp — hiện vật của lab bước 1 CHECKPOINT 3.

**Một ca phải ĐO, không đoán.** Nếu `dependencies` trỏ tới một job **không có mặt** trong pipeline (vì `rules` của nó không khớp — buổi 04 QT 6.2), có phiên bản GitLab báo lỗi ngay lúc tạo pipeline và có phiên bản bỏ qua êm. Bài giảng **không** kết luận; lab bước 1 dùng `rules` làm job nguồn biến mất rồi xem pipeline có được tạo không, và ghi kết quả kèm số phiên bản.

### 5.3. Hợp đồng rỗng: chế độ hỏng im lặng số một của giai đoạn 1

**Nguyên lý cốt lõi:** `artifacts:paths` không khớp tệp nào thì job **vẫn xanh** và artifact **rỗng** — đây là chế độ hỏng im lặng số một của cả giai đoạn 1. Đường thoát duy nhất là một **khẳng định** trong `script` (buổi 01 QT 7.3, lần thứ 3).

**Giải thích cơ chế ngầm:** Upload artifact là một **bước riêng sau `script`**, ở pha 8. Kết quả của nó không được cộng vào mã thoát của job: runner đã đọc mã thoát của `script` từ trước, và pha 8 chỉ ghi thêm cảnh báo vào log nếu mẫu `paths` không khớp gì. Nói cách khác, `artifacts` là **khai báo cho runner làm hộ**, không phải một lệnh trong `script` mà ta đọc được mã thoát. Muốn nó có mã thoát thì ta phải tự viết ra.

Đây là loại (c) — **phải đo**, vì mức độ "im lặng" của bước upload đã đổi giữa các bản runner: có bản chỉ in cảnh báo, có bản cho cấu hình coi đó là lỗi. Bài giảng **không** kết luận thay lab: **lab bước 2 CHECKPOINT 4 và 5** đo đúng ca này trên GitLab CE 17.7 với runner 17.7, bằng **hai khẳng định độc lập**.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> `status == "success"` nhưng `GET /projects/:id/jobs/:job_id/artifacts` trả **404**, và `trace` có dòng cảnh báo `no matching files`. Dấu hiệu ở đầu kia, đắt hơn: job deploy chạy xanh mà `dist/` nó nhận được trống, nên nó deploy một bản rỗng — không ai biết cho tới khi có người mở trang web.

**Minh hoạ.**

```yaml
# Hai job giống nhau, khác đúng MỘT dòng. Kết quả đúng: job dưới ĐỎ.
build-khong-khang-dinh:
  image: alpine:3.20
  script:
    - mkdir -p dist && echo "console.log(1)" > dist/app.js
  artifacts:
    paths: [build/**/*.js]     # SAI — tệp nằm ở dist/. Job XANH, artifact RỖNG, API 404.
    expire_in: 1 hour

build-co-khang-dinh:
  image: alpine:3.20
  script:
    - mkdir -p dist && echo "console.log(1)" > dist/app.js
    # MỘT dòng, 0,1 giây, đổi ô của bảng hai thuộc tính
    - test -s build/app.js || { echo "KĐ HỎNG: không có build/app.js để đóng gói"; exit 1; }
  artifacts:
    paths: [build/**/*.js]
    expire_in: 1 hour
```

```bash
# Hai khẳng định ĐỘC LẬP — quyết định thiết kế số 3 của lab.
# Một mình 404 có thể do token thiếu quyền; một mình success không nói gì về artifact.
ST=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB" | jq -r .status)
HTTP=$(curl -s -o /dev/null -w '%{http_code}' --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB/artifacts")
[ "$ST" = "success" ] && [ "$HTTP" = "404" ] \
  && echo "TÁI HIỆN ĐƯỢC ca xanh-mà-rỗng: status=$ST, artifacts=HTTP $HTTP" \
  || echo "chưa tái hiện được: status=$ST, artifacts=HTTP $HTTP"
```

Mẫu khẳng định dùng ngay hôm nay, đặt ngay trước khối `artifacts`:

```yaml
script:
  - npm run build
  - test -d dist        || { echo "KĐ: không có dist/";   exit 1; }
  - test -s dist/app.js || { echo "KĐ: dist/app.js rỗng"; exit 1; }
  - '[ "$(du -sk dist | cut -f1)" -ge 10 ] || { echo "KĐ: dist nhỏ hơn 10 kB"; exit 1; }'
```

**Con số chốt.** **1** dòng khẳng định đổi ô của bảng hai thuộc tính từ *im lặng, không chặn* sang *ồn ào, có chặn*. Giá của nó là **0,1 giây** — thứ rẻ nhất trong cả khoá. Không có lý do kinh tế nào để không viết nó.

### 5.4. `artifacts:when` — thứ ta cần nhất là thứ mặc định không cho lấy

**Nguyên lý cốt lõi:** Đừng dựa vào mặc định của `artifacts:when` cho báo cáo: khai **tường minh** `when: always` cho mọi thứ ta cần đọc lúc job **đỏ** — báo cáo test, báo cáo scan, log gỡ rối. Hành vi mặc định khác nhau giữa `artifacts:paths` và từng loại `artifacts:reports`, và nó phụ thuộc phiên bản.

**Giải thích cơ chế ngầm:** Mặc định là `on_success`: job xanh thì upload, job đỏ thì không. Nhưng thứ ta cần nhất khi job đỏ **chính là** báo cáo test cho biết ca nào đỏ, hoặc log công cụ build cho biết nó hỏng ở đâu — mặc định `on_success` lấy đúng thứ đó khỏi tay ta ở đúng lúc ta cần. Đó là mặc định hợp lý cho `dist/` (bản build lỗi thì giữ làm gì) và là mặc định sai cho báo cáo.

Đây là loại (c) — **phải đo**. Với `artifacts:paths` thì mặc định `on_success` rõ ràng; với từng loại `artifacts:reports` thì hành vi **không** thống nhất và **đã đổi giữa các phiên bản**. Bài giảng vì thế không phát biểu một câu chắc chắn cho mọi loại report; **lab bước 2 CHECKPOINT 6** cho một job test đỏ rồi đọc `GET /projects/:id/pipelines/:id/test_report`, so với mã HTTP khi tải `artifacts`, và ghi kết quả kèm số phiên bản GitLab và runner.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job test đỏ, mở ra không có báo cáo nào để đọc; phải chạy lại với `CI_DEBUG_TRACE` hoặc thêm `cat` vào `script` mới biết vì sao — tức **một vòng 4 phút** bị đốt cho mỗi lần chẩn đoán, và thường phải vài vòng.

**Minh hoạ.**

```yaml
.test-do: &test-do
  image: alpine:3.20
  script:
    - mkdir -p bao-cao && echo "<testsuite tests='1' failures='1'/>" > bao-cao/junit.xml
    - echo "log gỡ rối quan trọng" > bao-cao/chi-tiet.log
    - exit 1

test-mac-dinh:
  <<: *test-do
  artifacts:
    paths: [bao-cao/]          # when mặc định = on_success → job đỏ thì KHÔNG có gì để đọc

test-when-always:
  <<: *test-do
  artifacts:
    when: always               # ba giá trị: on_success (mặc định) · on_failure · always
    paths: [bao-cao/]
    reports: { junit: bao-cao/junit.xml }
    expire_in: 7 days
```

```bash
# So 404 với 200 giữa hai job đỏ. Đây là CHECKPOINT 6 của lab.
for TEN in test-mac-dinh test-when-always; do
  J=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs" \
    | jq -r --arg t "$TEN" '.[] | select(.name==$t) | .id')
  H=$(curl -s -o /dev/null -w '%{http_code}' --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/jobs/$J/artifacts")
  printf '%-18s job=%s artifacts=HTTP %s\n' "$TEN" "$J" "$H"
done
```

> **Nếu có Ultimate:** báo cáo scan bảo mật (`artifacts:reports:sast`, `dependency_scanning`, `container_scanning`, `secret_detection`) chỉ được GitLab gom vào widget merge request và Security Dashboard ở bản Ultimate. Trên CE, các tệp báo cáo đó vẫn upload **nguyên vẹn** bằng `artifacts:paths` cộng `when: always` và vẫn đọc được qua API — mất phần hiển thị, không mất dữ liệu. Các buổi 30–35 dựng trên đường CE (Semgrep, Gitleaks, Trivy, Grype, Checkov, ZAP, Syft, Cosign) nên **không** phụ thuộc điều này. Báo cáo `junit` hiển thị được ở mọi bản.

**Con số chốt.** `when` có **3** giá trị: `on_success` (mặc định), `on_failure`, `always`. Đổi sang `always` cho một thư mục báo cáo 200 kB tốn dưới **1 giây**; giá của việc không đổi là một vòng chạy lại 4 phút mỗi lần cần chẩn đoán.

### 5.5. `expire_in` là hạn giữ, không phải hạn dùng

**Nguyên lý cốt lõi:** `expire_in` là **hạn giữ**, không phải hạn dùng: artifact hết hạn làm việc `retry` một job cũ và việc điều tra một pipeline cũ **không còn khả thi**, trong khi tuỳ chọn *keep latest artifacts* âm thầm giữ lại artifact của pipeline mới nhất bất chấp `expire_in`.

**Giải thích cơ chế ngầm:** GitLab dọn artifact hết hạn bằng một tiến trình định kỳ, và nó xoá **tệp**, không xoá bản ghi job. Job cũ vẫn còn, log vẫn còn, nút `retry` vẫn còn — nhưng bấm `retry` một job **phụ thuộc** thì không tải được artifact nữa, và điều tra "bản build hôm ấy chứa gì" thì không còn tệp để mở. Ở hướng ngược lại, *Keep artifacts from most recent successful jobs* (bật mặc định ở mức project) giữ artifact của pipeline thành công gần nhất **bất chấp** `expire_in` — nên ai đặt `expire_in: 1 hour` rồi chờ sẽ thấy con số không về 0 như tính toán. Loại (a) — tài liệu *Job artifacts*.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hai dấu hiệu ở hai đầu: pipeline 40 ngày trước, bấm vào job build thì nút tải artifact biến mất — `expire_in` quá ngắn cho thứ cần điều tra. Hoặc dung lượng project tăng đều mỗi tuần mà không ai đặt `expire_in` — mặc định 30 ngày đang áp cho thứ chỉ cần sống 20 phút.

**Minh hoạ.**

```yaml
stages: [xay, phat-hanh]

build-trung-gian:
  stage: xay
  image: alpine:3.20
  script:
    - mkdir -p dist && dd if=/dev/urandom of=dist/goi.bin bs=1M count=45 2>/dev/null
    - test -s dist/goi.bin || { echo "KĐ: dist/goi.bin rỗng"; exit 1; }
  artifacts: { paths: [dist/], expire_in: 1 hour }      # job sau dùng trong vài phút là xong

dong-goi-phat-hanh:
  stage: phat-hanh
  image: alpine:3.20
  needs: [build-trung-gian]
  script:
    - mkdir -p phat-hanh && cp dist/goi.bin phat-hanh/
    - sha256sum phat-hanh/goi.bin > phat-hanh/SHA256SUMS
    - test -s phat-hanh/SHA256SUMS || { echo "KĐ: thiếu SHA256SUMS"; exit 1; }
  artifacts: { paths: [phat-hanh/], expire_in: 30 days }  # người ngoài cần đọc — QT 7.1 câu 3
  rules:
    - if: $CI_COMMIT_TAG
```

```bash
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects/$PID?statistics=true" \
| jq '{ artifacts_MB: (.statistics.job_artifacts_size / 1048576 | floor) }'
```

**Con số chốt, và giới hạn của nó.** Mặc định của instance là **30 ngày**. Repo đẩy **20 pipeline mỗi ngày**, mỗi pipeline giữ **45 MB** hiện vật trung gian: 20 × 45 MB × 30 ngày = **27 GB** để giữ những tệp không ai mở lại sau 20 phút. Đổi hiện vật trung gian sang `expire_in: 1 hour` thì lượng tồn về khoảng **90 MB** (2 pipeline trong một giờ). Con số 30 ngày **không phổ quát**: nó là **cấu hình mức instance**, admin đổi được, và *keep latest artifacts* phá nó ở hướng ngược lại.

> **Nếu có Ultimate:** bản trả phí có thêm phần quản lý dung lượng ở mức group với hạn mức và cảnh báo theo project, thấy ngay project nào đang đốt dung lượng. Trên CE, thay thế đủ dùng là gọi `GET /projects/:id?statistics=true` cho từng project trong một vòng lặp và ghi vào một tệp TSV theo tuần — ba dòng shell, và đó là bài tập mở rộng của lab.

---

### 1.3. `cache` là tối ưu — đo xem nó lãi hay lỗ (10 phút)

### 6.1. Khoá quyết định toàn bộ giá trị của cache

**Nguyên lý cốt lõi:** Khoá cache quyết định toàn bộ giá trị của cache, và có đúng **ba** kiểu khoá dùng được trong thực tế: theo **nội dung lockfile** (`key:files`), theo **nhánh** (`$CI_COMMIT_REF_SLUG`), và **cố định** cho cả project. Khoá theo commit là phản-cache.

**Giải thích cơ chế ngầm:** Cache chỉ có giá trị khi khoá **đổi chậm hơn** commit. Khoá đổi mỗi commit thì mỗi lần chạy đều là lần đầu tiên: ta trả toàn bộ chi phí ghi mà không bao giờ thu được lợi ích đọc. Ba kiểu dùng được xếp theo mức đổi chậm: lockfile đổi vài lần một tháng, nhánh đổi khi có nhánh mới, cố định thì không bao giờ đổi. Loại (b).

| Kiểu khoá | Đổi khi nào | Tỉ lệ trúng điển hình | Rủi ro |
|---|---|---|---|
| `key: { files: [package-lock.json] }` | Khi lockfile đổi | **19/20 = 95%** trên repo đổi lockfile 1 lần trong 20 lần chạy | Gần như không có — kiểu nên dùng |
| `key: $CI_COMMIT_REF_SLUG` | Khi sang nhánh khác | Cao trong một nhánh, **0%** ở commit đầu của nhánh mới | Nhánh nhiều thì cache phình; cần `fallback_keys` |
| `key: chung-cho-project` | Không bao giờ | Cao nhất | Cache "bẩn": rác lần trước còn nằm lại, khó truy nguyên |
| `key: $CI_COMMIT_SHA` | **Mỗi commit** | **0%** vĩnh viễn | Phản-cache: trả 100% chi phí ghi, thu 0% lợi ích |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> `trace` **luôn** có dòng trượt cache ở mọi lần chạy; thời gian job không giảm sau 20 lần chạy; đĩa runner phình vì mỗi lần chạy để lại một gói cache không ai dùng lại. Dấu hiệu này rất dễ bị đọc thành "cache không hiệu quả với repo của tôi" — trong khi thật ra cache chưa từng được đọc lần nào.

**Minh hoạ.**

```yaml
.co-cache: &co-cache
  image: node:22-alpine
  script:
    - npm ci --cache .npm --prefer-offline >/dev/null 2>&1 || true
    - echo "kích thước .npm: $(du -sh .npm 2>/dev/null | cut -f1)"

khoa-theo-lockfile: { <<: *co-cache, cache: { key: { files: [package-lock.json] }, paths: [.npm/] } }
khoa-theo-nhanh:    { <<: *co-cache, cache: { key: "npm-$CI_COMMIT_REF_SLUG", paths: [.npm/], fallback_keys: ["npm-main"] } }
khoa-co-dinh:       { <<: *co-cache, cache: { key: "npm-chung", paths: [.npm/] } }
khoa-theo-commit-PHAN-CACHE: { <<: *co-cache, cache: { key: "$CI_COMMIT_SHA", paths: [.npm/] } }
```

```bash
# Đếm số lần trúng của MỘT job trên 5 pipeline gần nhất. Lặp cho cả bốn tên job.
TEN=khoa-theo-lockfile; TRUNG=0; TONG=0
for P in $(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/pipelines?per_page=5" | jq -r '.[].id'); do
  J=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/pipelines/$P/jobs" \
    | jq -r --arg t "$TEN" '.[] | select(.name==$t) | .id')
  [ -z "$J" ] && continue; TONG=$((TONG+1))
  curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/jobs/$J/trace" \
    | grep -aq 'Successfully extracted cache' && TRUNG=$((TRUNG+1))
done
echo "$TEN: trúng $TRUNG/$TONG"
```

**Con số chốt.** Khoá theo commit cho tỉ lệ trúng **0%**. Khoá theo lockfile, trên repo có 20 lần chạy và 1 lần đổi lockfile, cho **19/20 = 95%**. Chênh lệch giữa hai dòng cấu hình trông gần giống nhau là toàn bộ giá trị của cache.

### 6.2. `policy` tách quyền đọc khỏi quyền ghi

**Nguyên lý cốt lõi:** `policy` tách **quyền đọc** khỏi **quyền ghi** cache, và job chỉ tiêu thụ phụ thuộc phải khai `policy: pull`. Đây là cách rẻ nhất để bỏ toàn bộ chi phí nén và tải lên ở các job không tạo ra gì mới.

**Giải thích cơ chế ngầm:** Với `pull-push` (mặc định), **mỗi** job nén lại toàn bộ thư mục cache ở cuối job, dù không thay đổi gì trong đó. Runner không so nội dung để quyết định có cần nén lại hay không — nó chỉ đọc `policy`. Cho nên ba job test song song, cùng khoá, cùng thư mục sẽ nén ba lần cùng một nội dung rồi lần lượt ghi đè lên nhau. Loại (a) — tài liệu *Caching in GitLab CI/CD*, mục `cache:policy`.

| `policy` | Đầu job | Cuối job | Dùng cho |
|---|---|---|---|
| `pull-push` (mặc định) | Giải nén | **Nén và tải lên** | Đúng **một** job: job tạo ra thư mục cache |
| `pull` | Giải nén | Không làm gì | Mọi job còn lại — test, lint, đóng gói |
| `push` | Không làm gì | Nén và tải lên | Job hâm nóng cache chạy theo `rules:changes` trên lockfile |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ba job test song song, mỗi job có pha `Creating cache` dài 40–60 giây ở cuối, và chúng ghi đè lên nhau cùng một khoá. Bằng chứng đủ, không cần đo thêm: `trace` của cả ba job đều có dòng `Creating cache ...` với cùng một tên khoá.

**Minh hoạ.**

```yaml
stages: [xay, kiem]

build:
  stage: xay
  image: node:22-alpine
  cache:
    key: { files: [package-lock.json] }
    paths: [.npm/]
    policy: pull-push          # job DUY NHẤT được ghi
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run build
    - test -s dist/app.js || { echo "KĐ: dist/app.js rỗng"; exit 1; }
  artifacts: { paths: [dist/], expire_in: 1 hour }

.chi-doc-cache: &chi-doc
  stage: kiem
  image: node:22-alpine
  needs: [build]
  cache:
    key: { files: [package-lock.json] }
    paths: [.npm/]
    policy: pull               # bỏ hẳn pha Creating cache

test-unit: { <<: *chi-doc, script: [npm ci --cache .npm --prefer-offline, npx jest] }
test-lint: { <<: *chi-doc, script: [npm ci --cache .npm --prefer-offline, npx eslint .] }
test-kieu: { <<: *chi-doc, script: [npm ci --cache .npm --prefer-offline, npx tsc --noEmit] }
```

```bash
# Lõi của doc-pha.sh: đếm giây từng pha. Hiện vật dùng lại ở buổi 14.
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB/trace" \
| grep -aE 'Restoring cache|Downloading artifacts|Creating cache|Uploading artifacts|Job succeeded'
```

**Con số chốt.** Với cache **380 MB**, bỏ pha `Creating cache` ở **3** job test tiết kiệm **3 × 61 = 183 giây** mỗi pipeline. Giá phải trả là **3** dòng `policy: pull`, và không có rủi ro nào — ba job đó vốn không tạo ra gì mới trong `.npm/`.

### 6.3. Sổ thu chi: cache có thể lỗ, và điểm hoà vốn tính được

**Nguyên lý cốt lõi:** Cache **có thể lỗ**, và điểm hoà vốn tính được bằng một phép chia. Với `p` là tỉ lệ trúng, cache có lãi khi `p × (tạo_lại − giải_nén) > nén_và_tải`. Cái làm cache lỗ hầu như luôn là **khoá sai**, không phải **kích thước lớn**.

**Giải thích cơ chế ngầm:** Kích thước lớn làm **cả hai vế** lớn lên gần như cùng tỉ lệ: thư mục to thì `tạo_lại` to, mà `nén_và_tải` cũng to. Khoá sai thì khác — nó đưa `p` về **0** và **giữ nguyên** chi phí ghi. Một vế về 0, vế kia không đổi: đó là định nghĩa của lỗ. Loại (b), và đây là chỗ **định lượng ngược lại** của buổi này: con số sẽ cho thấy cái ai cũng bảo là tệ ("cache 380 MB, to quá không đáng") thật ra không tệ.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thêm cache mà thời gian pipeline **tăng**. Hoặc kiểu tinh vi hơn: pipeline nhanh hơn ở lần thứ hai rồi chậm lại ở mọi lần sau — dấu hiệu khoá đổi theo một thứ đổi thường xuyên, hoặc job nhảy giữa các runner (QT 6.4).

**Minh hoạ.** Bảng dưới là **giá trị tham chiếu, loại (c) — học viên PHẢI đo lại**. Bốn thư mục sinh bằng `sinh-thu-muc.sh` ở lab bước 4; giây đọc từ `trace` bằng `doc-pha.sh`, không nhìn giao diện.

| Cache | Số tệp | Tạo lại (`npm ci`) | Nén + tải lên | Tải + giải nén | Lãi mỗi lần trúng | Lỗ mỗi lần trượt | Số lần trúng để hoà vốn |
|---|---|---|---|---|---|---|---|
| 12 MB | 380 | 8 s | 3 s | 2 s | **+6 s** | −3 s | **1** |
| 45 MB | 1.200 | 22 s | 9 s | 6 s | **+16 s** | −9 s | **1** |
| 160 MB | 9.500 | 58 s | 26 s | 18 s | **+40 s** | −26 s | **1** |
| 380 MB | 28.000 | 95 s | 61 s | 44 s | **+51 s** | −61 s | **2** |

Cách đọc bảng, ba điều:

1. **Cột "lãi mỗi lần trúng" = tạo_lại − giải_nén**, và nó giả định job đang trúng **chỉ đọc**, tức `policy: pull` — chính là QT 6.2. Nếu để `pull-push` thì mỗi lần trúng vẫn trả tiền nén, cột này tụt xuống `tạo_lại − giải_nén − nén_và_tải`: dòng 380 MB thành 95 − 44 − 61 = **−10 s**, tức **lỗ ngay cả khi trúng**. QT 6.2 và QT 6.3 phải đọc cùng nhau, không tách được.
2. **Số lần trúng để hoà vốn = `nén_và_tải` chia `lãi mỗi lần trúng`, làm tròn lên.** Dòng 380 MB: 61 / 51 → **2**. Cache 380 MB chỉ cần **2** lần trúng là hoà vốn; với khoá theo lockfile cho tỉ lệ trúng 19/20, hai lần trúng đến trong buổi sáng.
3. **Số tệp quan trọng không kém số MB.** So dòng 160 MB (9.500 tệp) với 380 MB (28.000 tệp): kích thước gấp 2,4 lần mà giây nén gấp 2,3 lần — vì thời gian nén chi phối bởi số tệp phải duyệt, không chỉ bởi tổng byte. Đây là lý do `~/.npm` (nhiều tệp nhỏ) hành xử khác `target/*.jar` (ít tệp lớn) ở cùng một số MB.

Và đây là con số của ca lỗ, cạnh con số của ca lãi:

```
Cache 380 MB, policy pull-push ở CẢ 4 job, khoá = $CI_COMMIT_SHA:
   chi phí ghi = 4 × 61 s = 244 s mỗi pipeline · lợi ích đọc = 0 (p = 0)
   → LỖ 244 giây mỗi pipeline, MÃI MÃI, và không có dòng lỗi nào trong log.

Cùng cache đó, khoá theo lockfile + 3 job dùng policy pull:
   lãi thô = 4 lần trúng × 51 s = 204 s mỗi pipeline
```

**Ghi chú thật thà về 204 s.** Đó là **lãi thô** của 4 lần trúng. Nếu job `build` vẫn giữ `pull-push` thì nó trả lại 61 s, còn **143 s** ròng. Muốn thu đủ 204 s thì đẩy việc ghi cache sang một job riêng chỉ chạy khi lockfile đổi — 19 trong 20 pipeline không trả đồng nào cho việc ghi:

```yaml
# mảnh — dán vào .gitlab-ci.yml; ghép QT 6.1 + QT 6.2 + rules:changes của buổi 04
ham-nong-cache:
  stage: chuan-bi
  image: node:22-alpine
  cache: { key: { files: [package-lock.json] }, paths: [.npm/], policy: push }   # chỉ GHI
  rules:
    - changes: [package-lock.json]
  script:
    - npm ci --cache .npm --prefer-offline
    - test -d .npm || { echo "KĐ: .npm không được tạo"; exit 1; }
```

**Con số chốt và giới hạn của nó.** Bốn dòng bảng trên đo trên executor `docker`, đĩa SSD, 8 vCPU. Runner `kubernetes` với volume mạng, hoặc đĩa mạng, cho số **khác hẳn**: thứ tự lớn nhỏ giữa bốn dòng giữ nguyên, tỉ lệ thì không. Vì vậy lab bước 4 **buộc đo lại** và ghi vào `bang-do-cache.tsv` kèm số phiên bản runner và loại đĩa.

### 6.4. Nhiều runner mà không có cache dùng chung thì trần trúng là `1/N`

**Nguyên lý cốt lõi:** Với `N` runner **không** có distributed cache, tỉ lệ trúng trần ở khoảng `1/N` vì cache nằm trên đĩa của runner đã tạo ra nó. `cache:fallback_keys` giảm thiệt hại khi khoá đổi, nhưng **không** sửa được việc cache nằm ở máy khác.

**Giải thích cơ chế ngầm:** Hệ quả trực tiếp của QT 4.1: cache là một tệp trên đĩa cục bộ, và runner số 2 không có cách nào đọc đĩa của runner số 1. Nếu GitLab chia job đều giữa `N` runner thì xác suất job rơi đúng vào runner đang giữ cache là khoảng `1/N`. `fallback_keys` giải một vấn đề **khác**: khi khoá chính trượt thì thử tiếp các khoá cũ hơn — hữu ích khi lockfile vừa đổi, vô ích khi cache ở máy khác. Loại (b).

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cùng một commit, chạy lại pipeline thì lần trúng lần trượt **không theo quy luật nào** — dấu hiệu job nhảy giữa các runner. Xác nhận trong 20 giây: in `$CI_RUNNER_ID` mỗi lần chạy và đối chiếu với việc lần đó trúng hay trượt; nếu trúng luôn ứng với một runner cố định thì kết luận xong.

**Minh hoạ.**

```yaml
do-ti-le-trung:
  image: node:22-alpine
  cache:
    key: { files: [package-lock.json] }
    paths: [.npm/]
    fallback_keys: [npm-main, npm-chung]
  script:
    - echo "runner = $CI_RUNNER_ID ($CI_RUNNER_DESCRIPTION)"
    - test -d .npm && echo "CÓ .npm — trúng" || echo "KHÔNG có .npm — trượt"
    - npm ci --cache .npm --prefer-offline >/dev/null
```

```toml
# mảnh — dán vào /etc/gitlab-runner/config.toml, mục [[runners]] tương ứng.
# ĐÂY LÀ HẠ TẦNG DÙNG CHUNG: sao lưu config.toml trước, khôi phục ở §L8 (buổi 02 QT 4.3).
# Khai ở NẤC XA NHẤT trong ba nấc của buổi 03 QT 7.1 — cả lớp dùng chung.
[runners.cache]
  Type   = "s3"
  Shared = true
  [runners.cache.s3]
    ServerAddress = "minio.lab:9000"
    BucketName    = "gitlab-runner-cache"
    Insecure      = true
    AuthenticationType = "access-key"
```

**Con số chốt và giới hạn của nó.** Với **2** runner và không có cache dùng chung, tỉ lệ trúng đo được khoảng **3/6**. Bật distributed cache (MinIO trên máy lab, thêm **1** container khoảng **512 MB** RAM) thì lên **5/6** — lần đầu **luôn** trượt, vì bucket còn trống. Con số "≈ 1/N" chỉ đúng khi **không** có distributed cache **và** job được chia đều giữa các runner; nếu một runner mạnh hơn và nhận phần lớn job thì tỉ lệ trúng cao hơn `1/N` mà không cần cấu hình gì — đó là may mắn, không phải thiết kế.

---

### 1.4. Bảng phân loại và thứ tự phục hồi (4 phút)

### 7.1. Ba câu hỏi, dừng ở câu đầu tiên trả lời được

**Nguyên lý cốt lõi:** Phân loại một thư mục bằng **ba** câu hỏi, theo đúng thứ tự, và dừng ở câu đầu tiên trả lời được: (1) *Job sau **sai** nếu thiếu nó, hay chỉ **chậm** hơn?* → sai thì `artifacts`. (2) *Tái tạo được từ tệp có trong git (lockfile) không?* → được thì `cache`. (3) *Có người ngoài pipeline cần đọc nó không?* → cần thì `artifacts` kể cả khi tái tạo được.

**Giải thích cơ chế ngầm:** Đây không phải danh sách kiểm mà là **cây quyết định có thứ tự**, và thứ tự là phần quan trọng. Câu 1 đặt trước vì nó bắt được lỗi đắt nhất: đưa cái job sau **cần** vào một kho không đảm bảo. Câu 2 đặt sau vì nó là câu tối ưu, chỉ có nghĩa khi câu 1 đã cho "chỉ chậm hơn". Câu 3 đặt cuối vì nó **ghi đè** kết luận của câu 2: một thứ tái tạo được nhưng có người ngoài cần đọc — báo cáo test, SBOM — vẫn phải là `artifacts`, vì chỉ artifact có API. Loại (b), suy từ mô hình tư duy 2.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hai dấu hiệu đối xứng: `node_modules` đi bằng `artifacts` → dung lượng project tăng vọt, mỗi pipeline cộng hàng chục MB không ai đọc. Hoặc `dist/` đi bằng `cache` → deploy được **bản cũ** mà không ai biết, vì cache của lần chạy trước vẫn còn nằm đó.

**Minh hoạ.** Bảng phân loại 10 thư mục thật của sáu ngôn ngữ. Cột cuối ghi **dừng ở câu hỏi số mấy** — đó là phần phải giải thích được ở vấn đáp câu 11.

| Thư mục | Ngôn ngữ | Đi bằng | Dừng ở câu | Lý do một dòng |
|---|---|---|---|---|
| `dist/`, `build/` | Node, front-end | `artifacts` | **1** | Job deploy **sai** nếu thiếu; nó là kết quả của commit này |
| `node_modules/` | Node | `cache` | 2 | Tái tạo được từ `package-lock.json` |
| `~/.npm` (hoặc `.npm/`) | Node | `cache` | 2 | Kho tải về thuần, không ai ngoài cần đọc |
| `target/*.jar` | Java | `artifacts` | **1** | Job đóng gói image **sai** nếu thiếu |
| `~/.m2/repository` | Java | `cache` | 2 | Tái tạo được từ `pom.xml` — buổi 17 đo lại |
| `.gradle/caches` | Java, Kotlin | `cache` | 2 | Tái tạo được; rất nhiều tệp nhỏ, xem QT 6.3 điều 3 |
| `GOMODCACHE` và `GOCACHE` | Go | `cache` | 2 | Tái tạo được từ `go.sum`; buổi 19 tách hai loại |
| `.venv/` hoặc `~/.cache/pip` | Python | `cache` | 2 | Tái tạo được từ `requirements.txt` / `poetry.lock` |
| Báo cáo test `junit.xml`, báo cáo coverage | Mọi ngôn ngữ | `artifacts` | **3** | Tái tạo được, **nhưng** người review cần đọc → câu 3 ghi đè |
| SBOM, chữ ký số, `SHA256SUMS` | Mọi ngôn ngữ | `artifacts` | **3** | Auditor cần đọc, phải kiểm chứng từ ngoài — buổi 25, 34 |

```yaml
# Hình dạng chuẩn: mỗi job có ĐÚNG một khối cache và ĐÚNG một khối artifacts,
# và hai khối đó KHÔNG có đường dẫn nào trùng nhau. Xem QT 7.2 vì sao.
build:
  image: node:22-alpine
  cache:                                          # tái tạo được → câu 2
    key: { files: [package-lock.json] }
    paths: [.npm/]
    policy: pull-push
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run build
    - npm test -- --reporters=default --reporters=jest-junit
    - test -s dist/app.js || { echo "KĐ: dist/app.js rỗng"; exit 1; }
    - test -s junit.xml   || { echo "KĐ: junit.xml rỗng";   exit 1; }
  artifacts:                                      # job sau cần → câu 1; người ngoài đọc → câu 3
    when: always
    paths: [dist/]
    reports: { junit: junit.xml }
    expire_in: 1 hour
```

**Con số chốt.** **3** câu hỏi. `dist/`, báo cáo test và SBOM **luôn** là `artifacts`. `~/.npm`, `~/.m2`, `.gradle/caches`, `GOMODCACHE` **luôn** là `cache` — bốn cái tên sẽ quay lại ở buổi 15–22, mỗi buổi một ngôn ngữ.

### 7.2. Bốn bước ở đầu job, và ai thắng khi trùng đường dẫn

**Nguyên lý cốt lõi:** Ở đầu job, runner làm theo thứ tự **clone → phục hồi cache → tải artifacts → `script`**. Vì vậy khi một đường dẫn nằm trong **cả** `cache` và `artifacts`, thứ thắng là **artifact**. Đặt cùng một đường dẫn vào hai kho là tự tạo ra một lớp lỗi "xanh mà sai" không cần thiết.

**Giải thích cơ chế ngầm:** Hai bước ghi vào cùng một thư mục thì bước sau ghi đè bước trước. Vì `download_artifacts` là pha 5 và `restore_cache` là pha 4 (buổi 01 QT 4.2), artifact ghi sau nên artifact thắng. Đây là loại (c) — **phải đo bằng cách đọc `trace`**, vì kết luận đứng trên **thứ tự bốn bước**: nếu một phiên bản runner đổi thứ tự thì kết luận đổi theo. Bài giảng vì thế không chốt "artifact luôn thắng" như chân lý; **lab bước 5 CHECKPOINT 11** đọc `trace` tìm hai dòng `Restoring cache` và `Downloading artifacts`, so số dòng, rồi in nội dung tệp nhận được.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job sau dùng bản `dist/` **cũ** còn sót trong cache; đổi mã nguồn mà kết quả deploy không đổi. Đây là ca đắt nhất trong năm ca hỏng im lặng của buổi này, vì nó không hỏng ở CI mà hỏng ở prod — người phát hiện là người dùng cuối, và câu hỏi đầu tiên của cuộc điều tra ("code đã được build chưa") có đáp án "đã, và pipeline xanh".

**Minh hoạ.**

```yaml
# Một job ghi CÙNG một đường dẫn vào cả hai kho với hai nội dung KHÁC nhau.
stages: [ghi, doc]

ghi-vao-hai-kho:
  stage: ghi
  image: alpine:3.20
  script:
    - mkdir -p chung
    - echo "NOI-DUNG-TU-CACHE"    > chung/dau.txt   # bản này bị nén vào cache ở cuối job
    - cp chung/dau.txt /tmp/ban-cache.txt
    - echo "NOI-DUNG-TU-ARTIFACT" > chung/dau.txt
  cache:     { key: bai-05-trung-duong-dan, paths: [chung/] }
  artifacts: { paths: [chung/], expire_in: 1 hour }

doc-tu-hai-kho:
  stage: doc
  image: alpine:3.20
  cache: { key: bai-05-trung-duong-dan, paths: [chung/], policy: pull }
  script:
    - cat chung/dau.txt
    - >
      grep -q 'ARTIFACT' chung/dau.txt
      && echo "KẾT LUẬN ĐO ĐƯỢC: artifact thắng cache"
      || echo "KẾT LUẬN ĐO ĐƯỢC: cache thắng artifact — GHI LẠI phiên bản runner"
```

```bash
# Chứng minh thứ tự bốn bước bằng SỐ DÒNG trong trace, không bằng niềm tin.
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB/trace" \
| grep -anE 'Getting source|Restoring cache|Downloading artifacts|Executing "step_script"'
# Kỳ vọng: bốn dòng, số dòng TĂNG DẦN theo đúng thứ tự trên.

# Và cách tránh cả lớp lỗi này, chạy trước khi push:
grep -A4 'cache:' .gitlab-ci.yml | grep -oE '^\s+- \S+' | sort > /tmp/duong-cache.txt
grep -A4 'artifacts:' .gitlab-ci.yml | grep -oE '^\s+- \S+' | sort > /tmp/duong-artifact.txt
comm -12 /tmp/duong-cache.txt /tmp/duong-artifact.txt | grep . \
  && echo "LỖI: có đường dẫn nằm trong CẢ hai kho" \
  || echo "ĐẠT: không đường dẫn nào trùng hai kho"
```

**Con số chốt.** **4** bước ở đầu job. Trong mọi lần đo trên GitLab Runner 17.7, artifact thắng cache ở **100%** các lần. Nhưng cách rẻ hơn nhiều so với việc nhớ ai thắng là: **đừng để đường dẫn nào xuất hiện trong cả hai khối**.

---

### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước

Ba việc, tổng 45 phút, xếp theo rủi ro tăng dần. Cả ba làm được **hôm nay** trên một nhánh riêng.

**Việc 1 — 15 phút, rủi ro bằng 0.** Chạy `grep -n 'artifacts:' .gitlab-ci.yml`, và với **mỗi** khối tìm được, thêm một dòng khẳng định vào cuối `script` của job đó: `test -s <tệp quan trọng nhất> || { echo "KĐ: <tệp> rỗng"; exit 1; }`. Thay đổi này **không đổi hành vi** khi mọi thứ đang đúng — nó chỉ làm job đỏ ở đúng những chỗ vốn đã hỏng im lặng. Không đụng ai, không cần bàn với ai; và nếu nó làm một job đỏ ngay hôm nay thì ta vừa phát hiện một lỗi tồn tại từ lâu.

**Việc 2 — 10 phút, rủi ro thấp.** Đặt `expire_in: 1 hour` cho **mọi** hiện vật trung gian, giữ `30 days` cho hiện vật phát hành. Ghi lại dung lượng project trước và sau bằng `GET /projects/:id?statistics=true`, trường `statistics.job_artifacts_size`. Với repo 20 pipeline mỗi ngày và 45 MB mỗi pipeline, con số này đi từ khoảng **27 GB** xuống khoảng **90 MB** trong một chu kỳ dọn.

**Việc 3 — 20 phút, rủi ro bằng 0 vì chỉ đọc.** Lấy `trace` của **một** pipeline gần nhất và ghi **ba con số**: giây `Downloading artifacts`, giây `Restoring cache`, giây `Creating cache`, cộng dồn trên toàn pipeline.

```bash
for J in $(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs" | jq -r '.[].id'); do
  curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB/api/v4/projects/$PID/jobs/$J/trace" \
  | grep -aE 'Restoring cache|Downloading artifacts|Creating cache' | sed "s/^/job $J: /"
done
```

Ba con số đó là **toàn bộ cơ sở** để nói chuyện tối ưu ở buổi 14. Không có chúng thì mọi câu về tối ưu chỉ là ý kiến.

### Cái gì hỏng nếu áp thẳng lên prod

**Đổi `cache:key` làm mọi job trượt cache đúng một lần.** Pipeline đầu tiên sau khi merge chậm hơn bình thường đúng bằng thời gian tạo lại — theo bảng QT 6.3, với cache 380 MB đó là khoảng **95 giây mỗi job**. Đừng làm lúc đang chuẩn bị phát hành, và đừng làm chiều thứ Sáu.

**Đặt `dependencies: []` sai chỗ làm job mất tệp nó vẫn đang âm thầm dùng** nhờ mặc định của QT 5.1. Đây là rủi ro thật, vì cái đang dùng ngầm thường không được ghi ở đâu cả. Cách áp an toàn: một nhánh riêng, và **trước khi merge phải chạy đủ một pipeline hoàn chỉnh** trên nhánh đó — một pipeline, không phải một job. Muốn nhẹ hơn nữa thì chạy song song bằng một job nhân bản không chặn ai, đúng như buổi 04 đã làm:

```yaml
# mảnh — chạy thử dependencies: [] mà không chặn ai, trong 3–5 ngày
lint-thu-nghiem:
  extends: lint
  dependencies: []
  allow_failure: true            # ồn ào nhưng KHÔNG chặn
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

**Thêm `expire_in` ngắn cho hiện vật mà đội khác đang tải bằng tay** là cách nhanh nhất để làm hỏng việc của người khác mà không ai hiểu vì sao — họ thấy nút tải biến mất, không thấy commit nào của mình. Trước khi rút hạn giữ, hỏi một câu trong kênh chung: *"có ai đang tải tay `<tên>` của pipeline cũ không"*.

### Đo trước — đo sau

Ba con số, đo trước khi làm và đo lại sau 2 tuần. Không có ba con số này thì không chứng minh được gì.

| # | Chỉ số | Đo bằng | Vì sao chỉ số này |
|---|---|---|---|
| 1 | Tổng giây ba pha `Downloading artifacts` + `Restoring cache` + `Creating cache` trên **toàn** pipeline | `doc-pha.sh` đọc `trace` từng job qua API | Đây là toàn bộ phần mà `dependencies: []` và `policy: pull` cắt được, và nó đo được chính xác |
| 2 | Dung lượng artifact của project | `GET /projects/:id?statistics=true`, trường `statistics.job_artifacts_size` | Đây là phần `expire_in` cắt được, và nó là một hoá đơn thật |
| 3 | Tỉ lệ trúng cache trên **20** lần chạy gần nhất | Đếm dòng `Successfully extracted cache` trong `trace` của 20 pipeline | Đây là `p` trong công thức QT 6.3; không có `p` thì không tính được lãi lỗ |

### Khi nào KHÔNG nên dùng

**Đừng dùng `cache` cho bất cứ thứ gì đi vào bản phát hành** — image, chart, SBOM, chữ ký số. Chúng phải **tái lập được** và phải **kiểm chứng được từ ngoài**, tức là `artifacts`. Các buổi 25, 27 và 34 dựa hết vào điều này: một chữ ký số nằm trong cache là một chữ ký không chứng minh được nguồn gốc, và đó là lỗi bảo mật, không phải lỗi hiệu năng.

**Đừng thêm `cache` cho repo mà `npm ci` hoặc `mvn` chạy dưới 10 giây.** Theo dòng 12 MB của bảng QT 6.3, lãi ròng khoảng **6 giây** mỗi lần trúng — không đủ trả cho một khối cấu hình phải bảo trì, phải giải thích cho người mới, và phải nghi ngờ mỗi lần pipeline hỏng lạ. Ngưỡng thực dụng: dưới 10 giây thì bỏ, 10–30 giây thì tuỳ, trên 30 giây thì làm.

**Đừng dùng `artifacts` để chuyển thư mục phụ thuộc** (`node_modules`, `.m2`, `.venv`) giữa các job chỉ vì nó "chắc chắn hơn". 90 MB × mỗi job × mỗi pipeline là một hoá đơn dung lượng thật, và ta đã có `cache` đúng cho việc đó. Ngoại lệ duy nhất đáng cân nhắc: pipeline chạy trên nhiều runner **không** có cache dùng chung, nơi tỉ lệ trúng trần ở `1/N` (QT 6.4) — khi ấy `artifacts` cho `node_modules` với `expire_in: 1 hour` là đánh đổi tính được, và việc phải làm là **tính nó ra giây** rồi mới quyết, không chọn theo cảm giác.

**Và điều buổi này KHÔNG giải quyết được.** Buổi này không rút ngắn tổng thời gian đồng hồ của pipeline — nó chỉ cho ba con số giây làm nguyên liệu; việc dùng chúng để cắt đường găng là buổi 08 (`needs`) và buổi 14 (tối ưu). Buổi này cũng không xử lý việc chuyển **giá trị** giữa các job (biến, chuỗi ký tự) — đó là `dotenv`, nội dung buổi 06.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy | Vì sao dính | Làm đúng là |
|---|---|---|---|
| 1 | Tin cache còn đó vì job trước vừa tạo | Đúng trong 9 lần chạy đầu nên trông như một đảm bảo | Cache nằm trên **đĩa runner**, không đảm bảo. Cái job sau **cần** thì đi bằng `artifacts` (QT 4.1) |
| 2 | `cache:key: $CI_COMMIT_SHA` | Nghe có lý: "khoá theo commit thì luôn đúng bản" | Tỉ lệ trúng **0%** vĩnh viễn. Khoá theo nội dung lockfile (QT 4.2, QT 6.1) |
| 3 | Tưởng trượt cache thì job đỏ | Trực giác từ mọi cơ chế phụ thuộc khác | **0** dòng lỗi, **0** đổi mã thoát — phải đọc `trace` mới thấy (QT 4.3) |
| 4 | Không khai gì, tưởng job không tải artifact | Không khai thì tưởng là không có gì | Tải của **mọi** job ở **mọi** stage trước; 2 × 45 MB = **90 MB** (QT 5.1) |
| 5 | Nhầm `dependencies` với `needs` | Hai từ khoá chồng lấn, tài liệu để cạnh nhau | `dependencies` chỉ đổi *tải của ai*, **không** đổi thứ tự chạy (QT 5.2) |
| 6 | `artifacts:paths` sai đường dẫn, không ai biết | Job vẫn xanh nên không có tín hiệu nào | Job **xanh**, artifact **404** — kiểm bằng **hai** khẳng định độc lập (QT 5.3) |
| 7 | Không có khẳng định sau bước quan trọng | "Build hỏng thì nó tự đỏ" — sai, chỉ khi lệnh trả mã thoát khác 0 | **1** dòng `test -s`, tốn **0,1 s** (QT 5.3, buổi 01 QT 7.3) |
| 8 | Báo cáo test không có khi job đỏ | Không đọc mặc định `on_success` | Khai tường minh `when: always` cho mọi thứ cần đọc lúc đỏ (QT 5.4) |
| 9 | Không đặt `expire_in` cho hiện vật trung gian | Mặc định 30 ngày trông như lựa chọn ai đó đã cân nhắc | **27 GB** sau 30 ngày, xuống khoảng **90 MB** với `1 hour` (QT 5.5) |
| 10 | Để `policy: pull-push` ở mọi job test | Đó là mặc định, và mặc định trông vô hại | **3 × 61 = 183 s** mỗi pipeline đốt cho việc nén lại thứ không đổi (QT 6.2) |
| 11 | Kết luận "cache không đáng" vì nó to | Nhìn số MB, không nhìn số giây | Điểm hoà vốn của cache 380 MB là **2** lần trúng (QT 6.3) |
| 12 | Nhiều runner mà không có cache dùng chung | Cache "hoạt động" nên tưởng đã xong | Tỉ lệ trúng trần ở **1/N**; 2 runner → khoảng **3/6** (QT 6.4) |
| 13 | `node_modules` đi bằng `artifacts` | Nó chạy được, và "chắc chắn hơn" | Ba câu hỏi phân loại — tái tạo được từ lockfile nên là `cache` (QT 7.1) |
| 14 | Cùng đường dẫn ở cả cache và artifact | Khai cả hai cho "an toàn gấp đôi" | **4** bước đầu job, artifact ghi đè cache; đừng để trùng đường dẫn (QT 7.2) |

---

### 1.7. Tóm tắt

```mermaid
graph TD
    LD["LUẬN ĐỀ: artifacts là HỢP ĐỒNG, cache là TỐI ƯU<br/>hai kho, hai chủ giữ, hai đảm bảo"]

    LD --> S4["§4 HAI ĐƯỜNG VẬN CHUYỂN<br/>QT 4.1 chủ giữ khác nhau, đảm bảo khác nhau<br/>QT 4.2 cache:key tính trên runner, KHÔNG ở t0<br/>QT 4.3 cả hai hỏng im lặng, không chặn"]
    LD --> S5["§5 HỢP ĐỒNG, VÀ HỢP ĐỒNG RỖNG<br/>QT 5.1 mặc định tải mọi stage trước<br/>QT 5.2 ba cách thu hẹp, khác ở thứ tự chạy<br/>QT 5.3 artifact rỗng mà job XANH<br/>QT 5.4 when: always cho thứ cần đọc lúc đỏ<br/>QT 5.5 expire_in là hạn GIỮ"]
    LD --> S6["§6 TỐI ƯU, ĐO LÃI LỖ<br/>QT 6.1 khoá quyết định mọi thứ<br/>QT 6.2 policy: pull bỏ chi phí ghi<br/>QT 6.3 điểm hoà vốn tính được<br/>QT 6.4 N runner thì trần trúng 1/N"]

    S4 --> S7["§7 PHÂN LOẠI VÀ THỨ TỰ<br/>QT 7.1 ba câu hỏi, dừng ở câu đầu trả lời được<br/>QT 7.2 bốn bước đầu job, artifact thắng cache"]
    S5 --> S7
    S6 --> S7

    S7 --> KQ["Ô NGUY HIỂM NHẤT: im lặng + không chặn<br/>5 ca mới hôm nay, 4 ca ở ô này<br/>1 dòng test -s đổi ô, giá 0,1 s"]
    KQ --> VT["§8 ĐƯA VÀO VIỆC THẬT<br/>khẳng định · expire_in · ba con số giây<br/>áp trên nhánh riêng, chạy đủ MỘT pipeline"]

    S4 -.dùng lại.-> B13["buổi 13 runner quy mô · buổi 47 vận hành runner"]
    S5 -.dùng lại.-> B08["buổi 08 needs · buổi 09 child · buổi 22 monorepo · buổi 27 release"]
    S6 -.dùng lại.-> B14["buổi 14 tối ưu · buổi 17 Java · buổi 19 Go · buổi 46 chi phí"]
    S7 -.dùng lại.-> B25["buổi 15-22 sáu ngôn ngữ · buổi 25 SBOM · buổi 34 chữ ký"]
```

**Năm điều phải nhớ sau buổi học:**

1. **Hai kho, hai chủ.** Artifact do **server** giữ và có API đọc; cache do **runner** giữ và **không có API nào**. Mọi khác biệt còn lại là hệ quả của một câu đó.
2. **Một câu hỏi để phân loại:** *job sau **sai** nếu thiếu, hay chỉ **chậm** hơn?* Sai thì `artifacts`, chậm thì `cache`. Có người ngoài cần đọc thì `artifacts`, kể cả khi tái tạo được.
3. **Artifact rỗng mà job xanh** là chế độ hỏng im lặng số một của giai đoạn 1. **1** dòng `test -s`, giá **0,1 s**, đổi ô của bảng hai thuộc tính từ *im lặng không chặn* sang *ồn ào có chặn*.
4. **Cache có sổ thu chi:** `p × (tạo_lại − giải_nén) > nén_và_tải`. Cache 380 MB hoà vốn sau **2** lần trúng; thứ làm cache lỗ là **khoá**, không phải **kích thước**.
5. **Bốn bước ở đầu job:** clone → cache → artifacts → `script`. Artifact ghi đè cache, nên đừng bao giờ để một đường dẫn nằm trong cả hai khối.

---

### 1.8. Câu hỏi tự kiểm tra

1. Nêu **cơ chế** (không phải định nghĩa) khiến artifact có API đọc mà cache không có.
2. `cache:key` được tính ở thời điểm nào, và vì sao nó **không thể** được tính ở `t0` như `rules`?
3. Một pipeline có 3 stage. Job ở stage 3 không khai `dependencies` cũng không khai `needs`. Nó tải artifact của những job nào?
4. Với 2 job nguồn mỗi job sinh 45 MB artifact, một job ở stage sau tải bao nhiêu MB nếu không khai gì? Quy ra bao nhiêu giây theo bảng QT 6.3?
5. Phân biệt `dependencies: []`, `dependencies: [build-a]` và `needs: [{job: build-a, artifacts: false}]` theo **hai** tiêu chí: byte tải về và thứ tự chạy.
6. Job có `artifacts:paths: [build/**/*.js]` nhưng `script` sinh tệp vào `dist/`. Job xanh hay đỏ? `GET /jobs/:id/artifacts` trả mã HTTP nào? Đây là ô nào của bảng hai thuộc tính?
7. Viết đúng **một** dòng shell chặn được ca ở câu 6, và nói giá của nó bằng giây.
8. Job test `exit 1` và có `artifacts:paths: [bao-cao/]` không khai `when`. Có tải được báo cáo về không? Sửa bằng gì?
9. Repo đẩy 20 pipeline mỗi ngày, mỗi pipeline giữ 45 MB hiện vật trung gian, `expire_in` để mặc định. Sau 30 ngày dung lượng artifact là bao nhiêu? Đặt `expire_in: 1 hour` thì còn khoảng bao nhiêu?
10. Tính điểm hoà vốn của một cache có `tạo_lại = 95 s`, `nén_và_tải = 61 s`, `giải_nén = 44 s`. Nếu để `policy: pull-push` ở job đang trúng cache thì lãi mỗi lần trúng là bao nhiêu?
11. Ba job test song song dùng cùng một cache 380 MB với `policy` mặc định. Đổi sang `policy: pull` tiết kiệm bao nhiêu giây mỗi pipeline, và vì sao không có rủi ro?
12. Cùng một commit, chạy lại pipeline thì lần trúng lần trượt cache không theo quy luật nào. Nêu giả thuyết và **một biến** xác nhận nó.
13. Nêu thứ tự **bốn** bước ở đầu job. Khi một đường dẫn nằm trong cả `cache:paths` và `artifacts:paths` thì ai thắng, và vì sao đây là phát biểu loại (c) chứ không phải loại (a)?
14. Phân loại năm thư mục sau và nói **dừng ở câu hỏi số mấy**: `dist/` · `~/.m2/repository` · `junit.xml` · `GOMODCACHE` · `SHA256SUMS`.
15. Nêu **một** trường hợp dùng `artifacts` cho `node_modules` là quyết định biện minh được, và cho biết phải tính con số nào trước khi quyết.

### Đáp án

1. Với `artifacts`, runner **gửi tệp lên GitLab qua HTTP** ở pha 8; GitLab tạo bản ghi trong cơ sở dữ liệu, gắn `expire_in`, mở URL tải. Với `cache`, runner chỉ **ghi một tệp nén ra đĩa cục bộ** theo đường dẫn dẫn xuất từ `cache:key` — server không biết gì về nó, nên không có gì để kể lại qua API (QT 4.1).
2. Tính **lúc job bắt đầu, trên runner**, sau pha `get_sources`. Không thể ở `t0` vì `cache:key:files` là hash **nội dung** các tệp được liệt kê, mà muốn hash thì phải có tệp trên đĩa — tức phải clone xong trước (QT 4.2). Hệ quả kèm theo: `cache:key` đọc được biến sinh muộn, còn `rules` thì không (buổi 04 QT 4.2).
3. Artifact của **mọi** job ở **cả stage 1 và stage 2**, không phải chỉ stage 2 (QT 5.1).
4. **90 MB**. Theo bảng QT 6.3, 45 MB ứng khoảng 6 giây tải và bung, nên 90 MB là khoảng **12 giây**, cộng vào **mỗi** job ở stage sau.
5. `dependencies: []` → **0** byte, **không** đổi thứ tự chạy. `dependencies: [build-a]` → chỉ artifact của `build-a`, **không** đổi thứ tự. `needs: [{job: build-a, artifacts: false}]` → **0** byte, **có** đổi thứ tự (job chạy ngay khi `build-a` xong, không chờ hết stage) (QT 5.2).
6. **Xanh**, artifact rỗng, `GET /jobs/:id/artifacts` trả **404**, và `trace` có cảnh báo `no matching files`. Đây là ô **im lặng + không chặn** — ô nguy hiểm nhất (QT 5.3, buổi 01 QT 7.1). Việc upload là bước riêng sau `script`, kết quả của nó không cộng vào mã thoát của job.
7. `test -s dist/app.js || { echo "KĐ: dist/app.js rỗng"; exit 1; }` — giá khoảng **0,1 giây**.
8. **Không.** Mặc định `artifacts:when` là `on_success`, nên job đỏ thì không upload gì. Sửa bằng `artifacts: { when: always, paths: [bao-cao/] }`. Riêng từng loại `artifacts:reports` thì hành vi khác nhau và phụ thuộc phiên bản — loại (c), đo ở lab bước 2 CHECKPOINT 6 (QT 5.4).
9. 20 × 45 MB × 30 = 27.000 MB = **27 GB**. Với `expire_in: 1 hour` thì lượng tồn còn khoảng **90 MB** (2 pipeline trong một giờ). Lưu ý *keep latest artifacts* vẫn giữ artifact của pipeline thành công gần nhất bất chấp `expire_in`, nên con số không về 0 (QT 5.5).
10. Lãi mỗi lần trúng = 95 − 44 = **51 s**; điểm hoà vốn = 61 / 51 làm tròn lên = **2** lần trúng. Nếu để `policy: pull-push` ở job đang trúng thì phải trừ thêm chi phí ghi: 95 − 44 − 61 = **−10 s**, tức **lỗ ngay cả khi trúng** (QT 6.2, QT 6.3).
11. **3 × 61 = 183 giây** mỗi pipeline. Không có rủi ro vì ba job test đó không tạo ra gì mới trong thư mục cache — chúng chỉ đọc, nên bỏ quyền ghi không mất thông tin nào (QT 6.2).
12. Giả thuyết: job nhảy giữa các runner, và cache nằm trên đĩa của runner đã tạo nó (QT 6.4). Xác nhận bằng `$CI_RUNNER_ID`: in nó trong `script` rồi đối chiếu với việc lần đó trúng hay trượt; nếu trúng luôn ứng với một `CI_RUNNER_ID` cố định thì kết luận xong. Cách sửa: bật distributed cache — tỉ lệ trúng đi từ khoảng **3/6** lên **5/6**.
13. **clone → phục hồi cache → tải artifacts → `script`.** **Artifact thắng**, vì nó ghi sau. Đây là loại (c) vì kết luận đứng trên **thứ tự bốn bước** của runner: một phiên bản runner đổi thứ tự thì kết luận đổi theo. Vì vậy phải đo bằng cách `grep` số dòng của `Restoring cache` và `Downloading artifacts` trong `trace` (QT 7.2).
14. `dist/` → `artifacts`, dừng ở **câu 1** (job deploy sai nếu thiếu). `~/.m2/repository` → `cache`, dừng ở **câu 2** (tái tạo từ `pom.xml`). `junit.xml` → `artifacts`, dừng ở **câu 3** (tái tạo được, nhưng người review cần đọc). `GOMODCACHE` → `cache`, dừng ở **câu 2**. `SHA256SUMS` → `artifacts`, dừng ở **câu 3** (phải kiểm chứng được từ ngoài) (QT 7.1).
15. Khi pipeline chạy trên nhiều runner **không** có cache dùng chung: tỉ lệ trúng trần ở `1/N` nên cache gần như không sinh lãi, trong khi `artifacts` được đảm bảo. Con số phải tính trước khi quyết: so **giây** tiết kiệm được (thời gian tạo lại `node_modules` nhân số job) với **giây** phải trả (upload ở job nguồn cộng download ở mỗi job sau), cộng thêm **MB dung lượng project** mỗi pipeline. Nếu không tính ra được hai con số đó thì mặc định vẫn là `cache` (QT 6.4, §8).

---

## §12. Tài liệu tham khảo

| Nguồn | Loại | Phiên bản |
|---|---|---|
| GitLab Docs — *Job artifacts* (`artifacts:paths`, `artifacts:reports`, `artifacts:when`, `expire_in`, keep latest artifacts) | (a) tài liệu chính thức | **17.7** |
| GitLab Docs — *Caching in GitLab CI/CD* (`cache:key`, `cache:key:files`, `cache:policy`, `cache:fallback_keys`) | (a) | **17.7** |
| GitLab Docs — *CI/CD YAML syntax reference*, mục `dependencies` và `needs:artifacts` | (a) | **17.7** |
| GitLab Runner Docs — *Advanced configuration*, mục `[runners.cache]` và `[runners.cache.s3]` | (a) | **17.7** |
| GitLab API — `GET /jobs/:id/artifacts`, `GET /jobs/:id/trace`, `GET /projects/:id?statistics=true`, `GET /pipelines/:id/test_report` | (a) | v4 |
| Bốn dòng bảng đo cache (8/22/58/95 s và các cột kèm theo) | (c) **phải đo** | Lab bước 4, `bang-do-cache.tsv` |
| Job upload artifact rỗng có xanh không; artifact `404` khi job xanh | (c) **phải đo** | Lab bước 2, CHECKPOINT 4 và 5 |
| `artifacts:reports:junit` có được upload khi job đỏ không | (c) **phải đo** — khác nhau theo loại report và phiên bản | Lab bước 2, CHECKPOINT 6 |
| `dependencies` trỏ job **không có mặt** trong pipeline | (c) **phải đo** — có phiên bản báo lỗi tạo pipeline, có phiên bản bỏ qua | Lab bước 1 |
| Thứ tự phục hồi cache và artifact; ai thắng khi trùng đường dẫn | (c) **phải đo** bằng cách đọc `trace` | Lab bước 5, CHECKPOINT 11 |
| Tỉ lệ trúng cache với 2 runner (≈ 3/6) và với distributed cache (5/6) | (c) **phải đo** | Lab bước 4, phần tuỳ chọn |
| Ngưỡng "dưới 10 giây thì đừng thêm cache"; giá 0,1 s của một khẳng định | (c) kinh nghiệm thực tế | — |

> **Về việc trích dẫn.** Năm dòng loại (a) là chỗ nên tra tài liệu chính thức khi cần con số chính xác cho phiên bản đang dùng — đặc biệt hai giới hạn của GitLab 17.7: `cache:key:files` tối đa **2** tệp và `cache:fallback_keys` tối đa **5** khoá. Bảy dòng loại (c) là chỗ **không được** tra: chúng phụ thuộc phiên bản runner, loại đĩa, số runner và cấu hình instance, nên phải đo trên chính hệ thống của mình và ghi kết quả kèm số phiên bản.

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập buổi 04 | 10' |
| §1 | Sau buổi này học viên làm được gì | 1' |
| §2 | Cần biết trước | 1' |
| §3 | Thuật ngữ và mô hình tư duy | 8' |
| §4 | Hai đường vận chuyển, hai đảm bảo | 9' |
| §5 | `artifacts` là hợp đồng — và hợp đồng rỗng | 11' |
| §6 | `cache` là tối ưu — đo xem nó lãi hay lỗ | 10' |
| §7 | Bảng phân loại và thứ tự phục hồi | 4' |
| §8 | Đưa vào việc thật | 4' |
| §9 | Bẫy hay gặp | 2' |
| §10–§12 | Tóm tắt · tự kiểm tra · tài liệu tham khảo (học viên đọc ngoài giờ) | — |
| **Tổng** | | **60'** |

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên môi trường GitLab Community / Enterprise Edition cùng các GitLab Runner cô lập (Docker / Kubernetes Executor). Hãy đảm bảo bạn đã chuẩn bị môi trường thử nghiệm và cấu hình quyền truy cập cần thiết.

## Khối thực hành — 150 phút

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · executor `docker`.
> Mọi checkpoint gọi **API GitLab**, không xem giao diện. Lý do ở §L2 quyết định 1.
> Mọi con số giây in trong bài là **giá trị tham chiếu** đo trên executor `docker`, đĩa SSD, 8 vCPU, GitLab CE 17.7 + Runner 17.7. Học viên **phải đo lại** trên máy mình và ghi số của mình vào `bang-do-cache.tsv`.

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| # | Mục tiêu | Tiêu chí hoàn thành (kiểm chứng được bằng lệnh) |
|---|---|---|
| TH1 | Chứng minh artifact **có** kho đọc được từ ngoài job | `GET /jobs/:id/artifacts` trả **200** và `unzip -l` đếm đúng số tệp |
| TH2 | **Đo QT 5.1** — job không khai gì nhận artifact của những job nào | Hiện vật `nhan-duoc.json` do chính job sinh, `so_tep` khớp tổng của **mọi** stage trước |
| TH3 | Kiểm chứng QT 5.2 — `dependencies: []` cho đúng **0** tệp | `so_tep == 0` đọc từ artifact của job đó |
| TH4 | **Đo** ca job nguồn artifact biến mất vì `rules` | `bang-artifact.tsv` ghi mã HTTP của `POST /pipeline` và số tệp job sau nhận được |
| TH5 | Tái hiện hỏng im lặng **số 1** — artifact rỗng mà job xanh | `status == "success"` **và** `GET /jobs/:id/artifacts` trả **404** |
| TH6 | Kiểm chứng QT 5.3 — một dòng khẳng định đổi ô bảng hai thuộc tính | Job `build-co-khang-dinh` có `status == "failed"` |
| TH7 | **Đo QT 5.4** — `artifacts:paths` và `artifacts:reports:junit` khi job đỏ | Hai mã HTTP đối chứng (200 so 404) **và** `GET /pipelines/:id/test_report` đọc được |
| TH8 | **Đo QT 4.2** — `cache:key:files` tính lúc nào, đổi khi nào | Khoá trích từ `trace`: hai lần chạy không đổi lockfile cho **cùng** khoá |
| TH9 | Tái hiện hỏng im lặng **số 2** — trượt cache, **0** dòng lỗi | Job `status == "success"`, `grep -c '^ERROR'` trên `trace` bằng **0** |
| TH10 | **Đo QT 6.3** — bốn kích thước cache và điểm hoà vốn | `bang-do-cache.tsv` có **4** dòng dữ liệu, cột hoà vốn khớp phép chia bằng `awk` |
| TH11 | Kiểm chứng QT 6.2 và QT 7.2 | Job `policy: pull` **không** có pha `Creating cache`; artifact thắng cache khi trùng đường dẫn |
| TH12 | Nộp hiện vật và trả hạ tầng về nguyên trạng | `kiem-hien-vat.sh` in `ĐẠT`; nếu làm phần tuỳ chọn thì `config.toml` khớp bản sao lưu |

**Sản phẩm cuối buổi:** `gitlab-portfolio/05-artifact-va-cache/` gồm `bang-artifact.tsv` (số tệp nhận được của bốn ca thu hẹp), `hop-dong-rong.md` (hỏng im lặng số 1 và 3, kèm bằng chứng API), `bang-khoa-cache.tsv` (bốn kiểu khoá × ba lần chạy), **`bang-do-cache.tsv`** (bốn kích thước, điểm hoà vốn — hiện vật quan trọng nhất), **`doc-pha.sh`** (công cụ đọc giây ba pha từ `trace`, **dùng lại ở buổi 14**), `sinh-thu-muc.sh`, `bang-phan-loai.md` (mười thư mục thật + thứ tự phục hồi + `expire_in`), `.gitlab-ci.yml` bản cuối, `checkpoint.log`.

Hai hiện vật **cốt lõi** — thiếu một trong hai là chưa nộp bài — là `bang-do-cache.tsv` và `doc-pha.sh`. Ai bỏ phần tuỳ chọn của bước 4 vẫn có đủ cả hai.

---

## L1. Điều kiện tiên quyết về môi trường

| # | Kiểm tra | Lệnh | Kết quả kỳ vọng |
|---|---|---|---|
| 1 | Đã nạp biến môi trường lab | `echo "$GITLAB" "$GITLAB_TOKEN" \| wc -w` | `2` |
| 2 | GitLab sẵn sàng | `curl -sf -o /dev/null -w '%{http_code}\n' "$GITLAB/-/readiness"` | `200` |
| 3 | Token gọi được API | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/user" \| jq -r .username` | tên đăng nhập, khác rỗng |
| 4 | Runner online và nhận job không tag | (đoạn kiểm ba điều kiện của buổi 02 §L1) | ≥ 1 runner đạt cả ba |
| 5 | **`concurrent` của runner ≥ 4** — bước 4 chạy bốn job đo song song | `docker exec lab-runner sh -c 'grep -E "^concurrent" /etc/gitlab-runner/config.toml'` | `concurrent = 4` trở lên; nếu `1` thì bốn job chạy nối tiếp, xem §L9 |
| 6 | Có `jq`, `curl`, `git`, `awk`, `unzip` | `command -v jq curl git awk unzip \| wc -l` | `5` |
| 7 | Đĩa trống — bài lab sinh khoảng **1,2 GB** cache và **250 MB** artifact | `df -BG --output=avail "$HOME" \| tail -1` | `> 15G` |
| 8 | Bộ nhớ trống | `free -g \| awk '/Mem:/{print $7}'` | `>= 3` (`>= 4` nếu làm phần tuỳ chọn MinIO) |
| 9 | Có thư mục portfolio | `test -d "$PORTFOLIO" && echo có` | `có` |
| 10 | Chưa có project lab 05 | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects?search=lab05-artifact" \| jq length` | `0` — khác `0` thì xoá trước, xem dòng cuối §L9 |
| 11 | **Chỉ khi làm phần tuỳ chọn bước 4:** vào được container runner | `docker exec lab-runner sh -c 'echo ok'` | `ok` |

### Sao lưu bắt buộc — chỉ khi định làm phần tuỳ chọn của bước 4

Phần **bắt buộc** của cả năm bước **không** đụng `config.toml`. Riêng phần **tuỳ chọn** ở cuối bước 4 (MinIO làm cache dùng chung) thêm một mục `[runners.cache]` vào tệp đó — tức đụng hạ tầng dùng chung của **cả lớp** (buổi 02 QT 4.3). Ai định làm thì sao lưu **trước khi bắt đầu buổi**, không phải trước khi bắt đầu bước 4:

```bash
source ~/.gitlab-lab.env
docker exec lab-runner sh -c \
  'cp /etc/gitlab-runner/config.toml /etc/gitlab-runner/config.toml.buoi05.bak'
docker exec lab-runner sh -c 'ls -la /etc/gitlab-runner/config.toml*'
```

§L8.1 khôi phục bản sao lưu này và CHECKPOINT 12 kiểm `diff` phải rỗng. Bỏ bước khôi phục là để lại hạ tầng dùng chung ở trạng thái khác lúc đầu — đúng cái buổi 02 đã cấm.

**Cảnh báo về mức độ tác động.** Bài lab tạo **một** project `lab05-artifact-cache` và không đụng project nào khác. Nó sinh khoảng **14–18 pipeline**, khoảng **250 MB** artifact trên server GitLab và khoảng **1,2 GB** cache trên đĩa runner. Trên lớp đông người dùng chung một GitLab, nhân hai con số đó với sĩ số trước khi bắt đầu — nếu đĩa dưới 40 GB thì giảm bộ 380 MB theo §L9. Bước 4 làm runner nén và tải khoảng **600 MB** trong vài phút; job của người khác sẽ chậm hơn trong khoảng thời gian đó, nên lớp làm bước 4 **cùng lúc**, không rải rác. Phần tuỳ chọn cuối bước 4 thêm **một** container MinIO 512 MB RAM ở cổng `9000` và sửa `config.toml`; nếu cả lớp dùng chung một runner thì **chỉ giảng viên làm phần này trước lớp**, học viên quan sát và ghi số. §L8.3 xoá artifact và cache để trả đĩa lại.

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    HV["Học viên<br/>máy chủ lab"]
    HV -->|"git push"| PRJ["Project lab05-artifact-cache"]
    HV -->|"curl + jq — mọi checkpoint"| API["API GitLab v4<br/>jobs · trace · artifacts · test_report"]

    PRJ -->|"giao job"| RN["Runner lab-runner<br/>executor docker"]

    RN --> KHO1["KHO 1 — server GitLab<br/>artifacts<br/>CÓ bản ghi, CÓ URL tải, CÓ expire_in"]
    RN --> KHO2["KHO 2 — đĩa runner<br/>cache<br/>KHÔNG bản ghi, KHÔNG API tải"]

    KHO1 -->|"đọc được bằng API<br/>200 hay 404"| API
    KHO2 -.->|"không có endpoint nào<br/>chỉ đọc gián tiếp qua trace"| API

    API --> B1["Bước 1 — hợp đồng<br/>mặc định tải bao nhiêu tệp<br/>dependencies thu hẹp thế nào"]
    API --> B2["Bước 2 — hợp đồng RỖNG<br/>xanh mà 404 · khẳng định · when always"]
    API --> B3["Bước 3 — cache key tính lúc nào<br/>trượt cache im lặng"]
    API --> B4["Bước 4 — sổ thu chi<br/>4 kích thước · điểm hoà vốn · policy"]
    API --> B5["Bước 5 — phân loại · thứ tự phục hồi<br/>expire_in"]

    DP["doc-pha.sh<br/>đọc section_start / section_end<br/>trong trace THÔ"] --> B4
    DP --> B5
    ST["sinh-thu-muc.sh<br/>12 MB / 45 MB / 160 MB / 380 MB"] --> B4
    WF["workflow chuẩn của buổi 04<br/>dán lại ở bước 5"] --> B5
```

**Năm quyết định thiết kế:**

1. **Đo giây bằng cách đọc `trace` qua API, không nhìn giao diện.** Giao diện chỉ cho **một** con số: tổng thời gian job. Ba con số ta cần — giây của `Restoring cache`, `Downloading artifacts`, `Creating cache` — không có ở đâu ngoài `trace`, và trong `trace` **thô** chúng nằm ở các cặp điều khiển `section_start:<epoch>:<tên>` / `section_end:<epoch>:<tên>`. Hiệu hai mốc epoch là số giây của pha, chính xác tới **1 giây**, không phụ thuộc việc runner có bật dấu thời gian từng dòng hay không. Vì vậy `doc-pha.sh` không phải một script dùng một lần: nó là hiện vật được dùng lại ở **buổi 14** khi ta tối ưu thời gian pipeline, nên bước 4 bắt viết nó cho tử tế — nhận `PID` và `JOB_ID` làm tham số, có thông báo lỗi rõ, có ba định dạng đầu ra.

2. **Bốn kích thước cache sinh bằng script, không lấy repo thật.** Repo thật không cho ta kiểm soát biến số: `node_modules` của hai project khác nhau khác nhau cả về số tệp, cả về tỉ lệ nén, cả về thời gian `npm ci`. Muốn thấy **quan hệ** giữa kích thước và giây thì kích thước phải là thứ ta đặt được, và số tệp cũng vậy — vì thời gian nén phụ thuộc **số tệp** nhiều hơn phụ thuộc **tổng byte**. Đó chính là lý do bảng của QT 6.3 có cột "Số tệp" nằm ngay cạnh cột kích thước, và `sinh-thu-muc.sh` nhận cả hai con số.

3. **Ca artifact rỗng đo bằng hai khẳng định độc lập** — `status == "success"` **và** `GET /jobs/:id/artifacts` trả **404** — chứ không bằng một. Một mình `404` không kết luận được: token thiếu quyền cũng cho `404`, artifact hết hạn cũng cho `404`. Một mình `success` thì không nói gì về artifact cả. Hai khẳng định cùng lúc mới loại được hai cách giải thích khác, và đó là toàn bộ giá trị của CHECKPOINT 4.

4. **Cache dùng chung là phần tuỳ chọn, đặt ở cuối bước 4.** Nó đụng `config.toml`, tức đụng hạ tầng dùng chung của cả lớp (buổi 02 QT 4.3), nên không được nằm trên đường tới hiện vật nộp. Ai không làm vẫn đủ cả hai hiện vật cốt lõi; ai làm thì bắt buộc khôi phục ở §L8.1 và CHECKPOINT 12 kiểm `diff`.

5. **Bước 5 dùng lại `workflow` chuẩn của buổi 04.** Không có nó, mỗi lần push lên một nhánh đang có merge request mở sinh **2** pipeline cho **1** commit (buổi 04 QT 5.2) — và khi đó mọi con số giây của bước 4 bị đếm hai lần, đúng lúc ta đang xây một bảng mà toàn bộ giá trị nằm ở độ chính xác của con số. Bước 5 dán lại nguyên khối `workflow` đó, không viết lại.

**Ca đối chứng PHẢI THẤT BẠI — báo trước cho lớp.** Ở bước 2, job `build-co-khang-dinh` **phải đỏ**; đó là kết quả đúng và là bằng chứng của QT 5.3. Ai gọi giảng viên vì "job đỏ" ở chỗ đó là đã bỏ qua đoạn này. Ở bước 1, ca job có `needs` trỏ tới một job đã biến mất vì `rules` cho một kết quả mà lớp **phải đo** — không ai được nói trước đáp án, kể cả giảng viên.

---

## L3. Bước 1 — Artifact là hợp đồng: mặc định tải bao nhiêu, thu hẹp bằng gì (30 phút)

Kiểm chứng QT 4.1, QT 5.1, QT 5.2.

### 3.1. Tạo project và bộ công cụ dùng chung (6 phút)

```bash
source ~/.gitlab-lab.env
export HAU_TO="${USER}"                       # hoặc số thứ tự học viên
export TEN_PRJ="lab05-artifact-cache-${HAU_TO}"
mkdir -p ~/lab05 && cd ~/lab05

PID=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{\"name\":\"$TEN_PRJ\",\"visibility\":\"internal\",\"initialize_with_readme\":false}" \
  "$GITLAB/api/v4/projects" | jq -r .id)
echo "PID=$PID"
echo "export PID=$PID" >> ~/.gitlab-lab.env
```

Bộ công cụ của buổi. Ba hàm cuối (`art_http`, `art_tep`, `art_zip`) là thứ phân biệt buổi này với bốn buổi trước: chúng đọc **kho artifact** từ ngoài job, và không có hàm nào tương đương cho cache — đó là QT 4.1 nói bằng shell.

```bash
cat > ~/lab05/cong-cu.sh <<'SH'
#!/usr/bin/env bash
# Bộ công cụ lab buổi 05. Nạp bằng: source ~/lab05/cong-cu.sh
: "${GITLAB:?chưa nạp ~/.gitlab-lab.env}"
: "${GITLAB_TOKEN:?chưa nạp ~/.gitlab-lab.env}"
: "${PID:?chưa có PID}"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")
A="$GITLAB/api/v4/projects/$PID"

# đẩy commit hiện tại lên nhánh main và trả về id pipeline mới nhất
day() {
  local msg="${1:-cap nhat}"
  git add -A >/dev/null
  git commit -q -m "$msg" --allow-empty
  git push -q origin HEAD:refs/heads/main 2>/dev/null
  sleep 6
  curl -sf "${H[@]}" "$A/pipelines?per_page=1" | jq -r '.[0].id // "KHONG-CO"'
}

# đẩy lên một nhánh khác main
day_nhanh() {
  local nhanh="$1" msg="${2:-cap nhat}"
  git add -A >/dev/null
  git commit -q -m "$msg" --allow-empty
  git push -q -f origin "HEAD:refs/heads/$nhanh" 2>/dev/null
  sleep 6
  curl -sf "${H[@]}" "$A/pipelines?ref=$nhanh&per_page=1" | jq -r '.[0].id // "KHONG-CO"'
}

cho_pipeline() {
  local pipe="$1" han="${2:-420}" t=0 st
  [ "$pipe" = "KHONG-CO" ] && { echo "KHONG-CO"; return 0; }
  while [ "$t" -lt "$han" ]; do
    st=$(curl -sf "${H[@]}" "$A/pipelines/$pipe" | jq -r .status)
    case "$st" in success|failed|canceled|skipped) echo "$st"; return 0 ;; esac
    sleep 5; t=$((t+5))
  done
  echo "$st"
}

job_bang() {
  curl -sf "${H[@]}" "$A/pipelines/$1/jobs?per_page=100" \
  | jq -r '.[] | [.id, .name, .status, (.duration//0)] | @tsv'
}
job_id()  { curl -sf "${H[@]}" "$A/pipelines/$1/jobs?per_page=100" \
            | jq -r --arg n "$2" '.[] | select(.name==$n) | .id' | head -1; }
job_tt()  { curl -sf "${H[@]}" "$A/jobs/$1" | jq -r .status; }
job_log() { curl -sf "${H[@]}" "$A/jobs/$1/trace"; }
# log đã bỏ mã màu ANSI — dùng khi cần grep chính xác
job_log_sach() { job_log "$1" | sed 's/\x1b\[[0-9;K]*[a-zA-Z]//g' | tr -d '\r'; }

# ===== ba hàm ĐỌC KHO ARTIFACT TỪ NGOÀI JOB — cache KHÔNG có hàm tương đương =====
# mã HTTP khi tải toàn bộ artifact của một job: 200 = có, 404 = không có
art_http() { curl -sL -o /dev/null -w '%{http_code}' "${H[@]}" "$A/jobs/$1/artifacts"; }
# tải MỘT tệp trong artifact ra stdout:  art_tep <job_id> <duong/dan/trong/artifact>
art_tep()  { curl -sfL "${H[@]}" "$A/jobs/$1/artifacts/$2"; }
# tải cả gói zip ra một tệp:  art_zip <job_id> <tep_dich.zip>
art_zip()  { curl -sfL -o "$2" "${H[@]}" "$A/jobs/$1/artifacts"; }
SH
source ~/lab05/cong-cu.sh
```

Khởi tạo kho git:

```bash
cd ~/lab05
git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$A" | jq -r .path_with_namespace).git"
git config user.email "hocvien@lab.local"
git config user.name  "hoc vien"
echo "# lab05 artifact va cache" > README.md
```

### 3.2. Ba job nguồn, hai stage, và kho đọc được từ ngoài (8 phút)

Pipeline dưới đây có **hai** stage nguồn chứ không phải một — vì QT 5.1 nói job mặc định tải artifact của **mọi stage trước**, không phải chỉ stage liền trước, và một pipeline chỉ có một stage nguồn thì không phân biệt được hai phát biểu đó.

```yaml
# ~/lab05/.gitlab-ci.yml
stages: [nen, giua, kiem]

default:
  image: alpine:3.20

# --- stage 1: hai job nguồn, 3 tệp + 2 tệp ---
build-a:
  stage: nen
  script:
    - mkdir -p ra-a
    - echo "a1" > ra-a/mot.txt
    - echo "a2" > ra-a/hai.txt
    - echo "a3" > ra-a/ba.txt
    - echo "so tep build-a: $(find ra-a -type f | wc -l)"
  artifacts:
    paths: [ra-a/]
    expire_in: 1 hour

build-b:
  stage: nen
  script:
    - mkdir -p ra-b
    - echo "b1" > ra-b/mot.txt
    - echo "b2" > ra-b/hai.txt
  artifacts:
    paths: [ra-b/]
    expire_in: 1 hour

# --- stage 2: một job nguồn nữa, 1 tệp ---
build-c:
  stage: giua
  script:
    - mkdir -p ra-c
    - echo "c1" > ra-c/mot.txt
  artifacts:
    paths: [ra-c/]
    expire_in: 1 hour

# --- stage 3: bốn ca thu hẹp khác nhau ---
.dem-tep:
  stage: kiem
  script:
    - mkdir -p bao-cao
    - find . -type f -path './ra-*/*' | sort > bao-cao/nhan-duoc.txt
    - SO=$(wc -l < bao-cao/nhan-duoc.txt)
    - echo "SO_TEP_NHAN_DUOC=$SO"
    - printf '{"job":"%s","so_tep":%s,"tep":[' "$CI_JOB_NAME" "$SO" > bao-cao/nhan-duoc.json
    - awk '{printf "%s\"%s\"", (NR>1?",":""), $0}' bao-cao/nhan-duoc.txt >> bao-cao/nhan-duoc.json
    - printf ']}\n' >> bao-cao/nhan-duoc.json
    - cat bao-cao/nhan-duoc.json
  artifacts:
    when: always
    paths: [bao-cao/]
    expire_in: 1 hour

nhan-het:
  extends: .dem-tep
  # KHÔNG khai gì cả — đây là ca mặc định của QT 5.1

nhan-khong:
  extends: .dem-tep
  dependencies: []          # tắt hẳn — QT 5.2

nhan-mot:
  extends: .dem-tep
  dependencies: [build-a]   # thu hẹp còn một nguồn — QT 5.2
```

```bash
cd ~/lab05
PIPE1=$(day "buoc 1: ba nguon hai stage, bon ca thu hep")
echo "pipeline $PIPE1"
cho_pipeline "$PIPE1"
job_bang "$PIPE1"
```

Bây giờ đọc **kho 1** từ ngoài job. Đây là điều không làm được với cache:

```bash
JA=$(job_id "$PIPE1" "build-a")
echo "mã HTTP khi tải artifact của build-a: $(art_http "$JA")"
art_zip "$JA" /tmp/build-a.zip && unzip -l /tmp/build-a.zip
curl -sf "${H[@]}" "$A/jobs/$JA" | jq '{status, artifacts_file, artifacts_expire_at}'
```

**CHECKPOINT 1 — job `build-a` upload được artifact: `GET /jobs/:id/artifacts` trả 200 và gói zip chứa đúng 3 tệp.**

```bash
JA=$(job_id "$PIPE1" "build-a")
ma=$(art_http "$JA")
art_zip "$JA" /tmp/build-a.zip 2>/dev/null
so=$(unzip -l /tmp/build-a.zip 2>/dev/null | awk '/ra-a\/.*\.txt$/{n++} END{print n+0}')
{ [ "$ma" = "200" ] && [ "$so" -eq 3 ]; } \
  && echo "CHECKPOINT 1 — ĐẠT (HTTP $ma, $so tệp trong gói)" \
  || echo "CHECKPOINT 1 — LỖI (HTTP $ma, $so tệp — kỳ vọng 200 và 3)"
```

Ghi ngay vào `bang-artifact.tsv` một dòng đối lập: **không có endpoint nào của API GitLab trả về nội dung cache.** Học viên thử tự tìm trong 60 giây rồi ghi kết luận — đó là QT 4.1 tự chứng minh, không cần giảng viên nói.

### 3.3. Đếm số tệp mỗi ca nhận được (10 phút)

Bốn ca, bốn con số. Job tự in danh sách vào hiện vật của chính nó, ta khẳng định bằng `jq` và `wc -l` trên hiện vật đó — không tin dòng `echo` trong log, vì log không phải hiện vật kiểm chứng lại được.

```bash
for j in nhan-het nhan-khong nhan-mot; do
  ID=$(job_id "$PIPE1" "$j")
  echo "--- $j (job $ID) ---"
  art_tep "$ID" "bao-cao/nhan-duoc.json" | jq -c '{job, so_tep, tep}'
done
```

Dựng hiện vật:

```bash
{
  echo "# Buổi 05 bước 1 — số tệp artifact mỗi ca nhận được"
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version) · pipeline $PIPE1"
  echo "# nguồn: build-a 3 tệp (stage nen) · build-b 2 tệp (stage nen) · build-c 1 tệp (stage giua)"
  printf 'ca\tkhai_bao\tso_tep_nhan_duoc\tky_vong\n'
  for j in nhan-het nhan-khong nhan-mot; do
    ID=$(job_id "$PIPE1" "$j")
    N=$(art_tep "$ID" "bao-cao/nhan-duoc.json" | jq -r .so_tep)
    case "$j" in
      nhan-het)   K="khong khai gi";        E=6 ;;
      nhan-khong) K="dependencies: []";     E=0 ;;
      nhan-mot)   K="dependencies:[build-a]"; E=3 ;;
    esac
    printf '%s\t%s\t%s\t%s\n' "$j" "$K" "$N" "$E"
  done
} | tee ~/lab05/bang-artifact.tsv
```

**CHECKPOINT 2 — job không khai gì nhận artifact của **cả** hai stage trước: đúng 6 tệp.**

```bash
IDH=$(job_id "$PIPE1" "nhan-het")
art_tep "$IDH" "bao-cao/nhan-duoc.json" > /tmp/nhan-het.json
art_tep "$IDH" "bao-cao/nhan-duoc.txt"  > /tmp/nhan-het.txt
qua_jq=$(jq -r '.so_tep' /tmp/nhan-het.json)
qua_wc=$(wc -l < /tmp/nhan-het.txt | tr -d ' ')
co_a=$(jq -r '[.tep[] | select(startswith("./ra-a/"))] | length' /tmp/nhan-het.json)
co_c=$(jq -r '[.tep[] | select(startswith("./ra-c/"))] | length' /tmp/nhan-het.json)
{ [ "$qua_jq" -eq 6 ] && [ "$qua_wc" -eq 6 ] && [ "$co_a" -eq 3 ] && [ "$co_c" -eq 1 ]; } \
  && echo "CHECKPOINT 2 — ĐẠT (jq=$qua_jq, wc=$qua_wc, có cả stage nen ($co_a tệp) và stage giua ($co_c tệp))" \
  || echo "CHECKPOINT 2 — LỖI (jq=$qua_jq, wc=$qua_wc, ra-a=$co_a, ra-c=$co_c — kỳ vọng 6/6/3/1)"
```

Con số `co_c = 1` là chỗ quan trọng nhất: nếu mặc định chỉ tải stage **liền trước** thì `ra-a` và `ra-b` sẽ không có mặt. Chúng có mặt — QT 5.1 nói đúng, và ta vừa đo chứ không tra.

**CHECKPOINT 3 — job `dependencies: []` nhận đúng 0 tệp.**

```bash
IDK=$(job_id "$PIPE1" "nhan-khong")
art_tep "$IDK" "bao-cao/nhan-duoc.json" > /tmp/nhan-khong.json
n0=$(jq -r '.so_tep' /tmp/nhan-khong.json)
mang0=$(jq -r '.tep | length' /tmp/nhan-khong.json)
tai0=$(job_log_sach "$IDK" | grep -c 'Downloading artifacts' || true)
{ [ "$n0" -eq 0 ] && [ "$mang0" -eq 0 ] && [ "$tai0" -eq 0 ]; } \
  && echo "CHECKPOINT 3 — ĐẠT (0 tệp, 0 phần tử, và KHÔNG có pha Downloading artifacts)" \
  || echo "CHECKPOINT 3 — LỖI (so_tep=$n0, mảng=$mang0, dòng Downloading=$tai0)"
```

### 3.4. Ca phải ĐO: job nguồn artifact biến mất vì `rules` (6 phút)

Đây là chế độ hỏng im lặng **số 5** của buổi, và là câu 2 trong BTVN 4 của buổi 04. Job nguồn chỉ chạy khi có tag; ta kích hoạt trên một nhánh **không** tag. Hai biến thể, hai câu hỏi khác nhau: `dependencies` chỉ nói *tải của ai*, `needs` nói cả *chạy sau ai*.

```yaml
# ~/lab05/.gitlab-ci.yml — thay toàn bộ. Biến thể 1: dependencies
stages: [nen, kiem]

default:
  image: alpine:3.20

build-chi-tag:
  stage: nen
  rules:
    - if: $CI_COMMIT_TAG
  script:
    - mkdir -p ra-tag && echo "chi co khi co tag" > ra-tag/tep.txt
  artifacts:
    paths: [ra-tag/]
    expire_in: 1 hour

nhan-deps-bien-mat:
  stage: kiem
  dependencies: [build-chi-tag]
  script:
    - SO=$(find . -type f -path './ra-tag/*' | wc -l)
    - echo "SO_TEP_NHAN_DUOC=$SO"
    - echo "job nay KHONG kiem gi ca — no se XANH voi $SO tep"
```

```bash
cd ~/lab05
git checkout -q -b bien-mat 2>/dev/null || git checkout -q bien-mat
PIPE_BM=$(day_nhanh "bien-mat" "ca deps tro job da bien mat")
echo "pipeline = $PIPE_BM"
cho_pipeline "$PIPE_BM"
job_bang "$PIPE_BM"
```

Đo bằng cách tạo pipeline qua API — mã HTTP và thông báo là dữ liệu:

```bash
KQ=$(curl -s -o /tmp/kq-deps.json -w '%{http_code}' --request POST "${H[@]}" \
      "$A/pipeline?ref=bien-mat")
echo "HTTP=$KQ"; jq -r '.message // .id' /tmp/kq-deps.json
```

Bây giờ biến thể 2 — đổi `dependencies:` thành `needs:` **và giữ nguyên mọi thứ khác**:

```yaml
# mảnh — dán vào ~/lab05/.gitlab-ci.yml, thay đúng khối nhan-deps-bien-mat
nhan-needs-bien-mat:
  stage: kiem
  needs: [build-chi-tag]
  script:
    - echo "SO_TEP_NHAN_DUOC=$(find . -type f -path './ra-tag/*' | wc -l)"
```

```bash
git add -A >/dev/null && git commit -q -m "ca needs tro job da bien mat"
git push -q -f origin HEAD:refs/heads/bien-mat 2>/dev/null
sleep 4
KQ2=$(curl -s -o /tmp/kq-needs.json -w '%{http_code}' --request POST "${H[@]}" \
       "$A/pipeline?ref=bien-mat")
echo "HTTP=$KQ2"; jq -r '.message // .id' /tmp/kq-needs.json

{
  echo "# ca job nguon artifact BIEN MAT vi rules — DO tren GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
  printf 'bien_the\thttp_tao_pipeline\tthong_bao\tso_tep_job_sau_nhan\n'
  printf 'dependencies\t%s\t%s\t%s\n' "$KQ" "$(jq -rc '.message // "tao duoc"' /tmp/kq-deps.json)" \
    "$(ID=$(job_id "$PIPE_BM" "nhan-deps-bien-mat"); job_log_sach "$ID" | grep -oE 'SO_TEP_NHAN_DUOC=[0-9]+' | tail -1)"
  printf 'needs\t%s\t%s\t%s\n' "$KQ2" "$(jq -rc '.message // "tao duoc"' /tmp/kq-needs.json)" "xem pipeline moi neu tao duoc"
} | tee -a ~/lab05/bang-artifact.tsv

git checkout -q main
```

**Câu hỏi phải trả lời trước khi sang bước 2** — ghi vào `bang-artifact.tsv`:

1. Biến thể `dependencies` có tạo được pipeline không? Job sau **xanh hay đỏ**, và nó nhận bao nhiêu tệp? Ô nào của bảng hai thuộc tính (buổi 01 QT 7.1)?
2. Biến thể `needs` cho mã HTTP nào? Nếu nó khác biến thể `dependencies`, hãy phát biểu bằng **một** câu sự khác nhau giữa hai từ khoá — dựa vào cơ chế của QT 5.2, không dựa vào trí nhớ.
3. `nhan-het` tải 6 tệp bé tí nên không thấy chậm. Nếu `build-a` và `build-b` mỗi job sinh **45 MB** thì `nhan-het` tải bao nhiêu MB **mà không khai một dòng nào**? Quy ra giây với tốc độ đo được ở bước 4.

---

## L4. Bước 2 — Hợp đồng rỗng: artifact 0 byte mà job xanh, và cách chặn (30 phút)

Kiểm chứng QT 4.3, QT 5.3, QT 5.4. Đây là bước quan trọng nhất của cả buổi: nó tái hiện chế độ hỏng im lặng **số 1** — ô *im lặng, không chặn* của bảng hai thuộc tính (buổi 01 QT 7.1, lần thứ 5).

### 4.1. Ba job, một sai đường dẫn, một có khẳng định, một tiêu thụ mà không kiểm (12 phút)

```yaml
# ~/lab05/.gitlab-ci.yml — thay toàn bộ
stages: [build, tieu-thu]

default:
  image: alpine:3.20

# Ca 1 — SAI đường dẫn artifact. Job này sẽ XANH và artifact RỖNG.
build-rong:
  stage: build
  script:
    - mkdir -p dist
    - echo "console.log('xin chao')" > dist/app.js
    - echo "build xong, noi dung dist/:" && ls -la dist/
  artifacts:
    paths:
      - build/**/*.js        # tệp nằm ở dist/, mẫu trỏ vào build/ — không khớp gì
    expire_in: 1 hour

# Ca 2 — ĐÚNG một dòng khẳng định. Job này PHẢI ĐỎ. Đó là kết quả đúng.
build-co-khang-dinh:
  stage: build
  script:
    - mkdir -p dist
    - echo "console.log('xin chao')" > dist/app.js
    # khẳng định: mẫu artifact phải khớp ít nhất một tệp, và tệp đó phải khác rỗng
    - >
      [ "$(find build -name '*.js' 2>/dev/null | wc -l)" -ge 1 ] ||
      { echo "KHANG DINH HONG: mau artifact build/**/*.js khong khop tep nao"; exit 1; }
    - test -s build/app.js || { echo "KHANG DINH HONG: build/app.js rong"; exit 1; }
  artifacts:
    paths:
      - build/**/*.js
    expire_in: 1 hour
  allow_failure: true        # để pipeline hoàn tất và checkpoint so được hai job

# Ca 3 — nửa thứ hai của QT 4.3: thiếu artifact mà script KHÔNG kiểm thì cũng không lỗi
tieu-thu-khong-kiem:
  stage: tieu-thu
  dependencies: [build-rong]
  script:
    - echo "so tep nhan duoc: $(find . -type f -path './dist/*' -o -type f -path './build/*' | wc -l)"
    - cat dist/app.js 2>/dev/null || echo "khong co dist/app.js — va job nay VAN XANH"
```

```bash
cd ~/lab05
PIPE2=$(day "buoc 2: hop dong rong")
cho_pipeline "$PIPE2"
job_bang "$PIPE2"
```

Bằng chứng nằm ở **hai** chỗ, không phải một:

```bash
JR=$(job_id "$PIPE2" "build-rong")
echo "trạng thái job : $(job_tt "$JR")"
echo "HTTP artifact  : $(art_http "$JR")"
curl -sf "${H[@]}" "$A/jobs/$JR" | jq '{status, artifacts_file, artifacts}'
echo "--- dòng cảnh báo trong trace ---"
job_log_sach "$JR" | grep -iE 'WARNING|no matching files|no files' || echo "(khong co dong nao)"
```

**CHECKPOINT 4 — job `build-rong` XANH **và đồng thời** artifact trả 404: hai khẳng định độc lập.**

```bash
JR=$(job_id "$PIPE2" "build-rong")
st=$(job_tt "$JR")
ma=$(art_http "$JR")
sz=$(curl -sf "${H[@]}" "$A/jobs/$JR" | jq -r '.artifacts_file.size // 0')
{ [ "$st" = "success" ] && [ "$ma" = "404" ]; } \
  && echo "CHECKPOINT 4 — ĐẠT (status=$st VÀ artifact HTTP=$ma, size=$sz — IM LẶNG, KHÔNG CHẶN)" \
  || echo "CHECKPOINT 4 — LỖI (status=$st, HTTP=$ma, size=$sz — kỳ vọng success và 404)"
```

Nếu `ma` ra `401` hay `403` thay vì `404` thì token thiếu quyền, và **cả checkpoint mất giá trị** — đó chính là lý do quyết định thiết kế 3 bắt hai khẳng định độc lập chứ không một.

**CHECKPOINT 5 — ca đối chứng `build-co-khang-dinh` PHẢI ĐỎ.**

```bash
JK=$(job_id "$PIPE2" "build-co-khang-dinh")
sk=$(job_tt "$JK")
kd=$(job_log_sach "$JK" | grep -c 'KHANG DINH HONG' || true)
{ [ "$sk" = "failed" ] && [ "$kd" -ge 1 ]; } \
  && echo "CHECKPOINT 5 — ĐẠT (status=$sk, $kd dòng khẳng định đã bắt được lỗi — ỒN ÀO, CÓ CHẶN)" \
  || echo "CHECKPOINT 5 — LỖI (status=$sk, dòng khẳng định=$kd — job này PHẢI đỏ)"
```

Đo giá của khẳng định — con số để trả lời phản đối "thêm khẳng định làm pipeline chậm":

```bash
dr=$(curl -sf "${H[@]}" "$A/jobs/$JR" | jq -r .duration)
dk=$(curl -sf "${H[@]}" "$A/jobs/$JK" | jq -r .duration)
echo "build-rong           : ${dr}s"
echo "build-co-khang-dinh  : ${dk}s (thêm 2 khẳng định)"
echo "chênh lệch           : $(awk -v a="$dk" -v b="$dr" 'BEGIN{printf "%.2f", a-b}')s"
```

Giá trị tham chiếu: **0,1 giây mỗi khẳng định**. Đây là thứ rẻ nhất trong cả khoá.

### 4.2. Đo QT 5.4 — job đỏ thì lấy được gì ra ngoài (13 phút)

Hai job **giống nhau tới từng dòng**, cùng `exit 1`, chỉ khác **một** dòng `when: always`. Và mỗi job sinh một báo cáo JUnit với **tên bộ test khác nhau**, để `test_report` chỉ đúng báo cáo nào đã tới được server.

```yaml
# ~/lab05/.gitlab-ci.yml — thay toàn bộ
stages: [kiem]

default:
  image: alpine:3.20

.mau-test-do:
  stage: kiem
  allow_failure: true
  script:
    - mkdir -p bao-cao
    - |
      cat > bao-cao/junit.xml <<XML
      <?xml version="1.0" encoding="UTF-8"?>
      <testsuites>
        <testsuite name="$TEN_BO" tests="2" failures="1">
          <testcase classname="phep.cong" name="cong_hai_so"/>
          <testcase classname="phep.chia" name="chia_cho_khong">
            <failure message="chia cho 0">boom</failure>
          </testcase>
        </testsuite>
      </testsuites>
      XML
    - echo "log go roi cua $CI_JOB_NAME" > bao-cao/go-roi.log
    - ls -la bao-cao/
    - echo "job nay se DO ngay sau day"
    - exit 1

test-do-khong-always:
  extends: .mau-test-do
  variables:
    TEN_BO: "bo-khong-always"
  artifacts:
    # KHÔNG khai when — dùng mặc định
    paths: [bao-cao/]
    reports:
      junit: bao-cao/junit.xml
    expire_in: 1 hour

test-do-co-always:
  extends: .mau-test-do
  variables:
    TEN_BO: "bo-co-always"
  artifacts:
    when: always            # ĐÚNG MỘT DÒNG khác biệt
    paths: [bao-cao/]
    reports:
      junit: bao-cao/junit.xml
    expire_in: 1 hour
```

```bash
PIPE3=$(day "buoc 2: when always khi job do")
cho_pipeline "$PIPE3"
job_bang "$PIPE3"

JN=$(job_id "$PIPE3" "test-do-khong-always")
JY=$(job_id "$PIPE3" "test-do-co-always")
echo "khong-always : status=$(job_tt "$JN")  artifact HTTP=$(art_http "$JN")"
echo "co-always    : status=$(job_tt "$JY")  artifact HTTP=$(art_http "$JY")"
```

Bây giờ **đo** hành vi của `artifacts:reports:junit` khi job đỏ. Đề cương xếp đại lượng này vào loại (c) — *phải đo, không tra*. Không ai nói trước đáp án:

```bash
curl -sf "${H[@]}" "$A/pipelines/$PIPE3/test_report" \
| jq '{total_count, failed_count, cac_bo: [.test_suites[] | {name, total_count, failed_count}]}'
```

**CHECKPOINT 6 — `when: always` cho 200, mặc định cho 404; và `test_report` đọc được để ghi số.**

```bash
mn=$(art_http "$JN"); my=$(art_http "$JY")
sn=$(job_tt "$JN");   sy=$(job_tt "$JY")
curl -sf "${H[@]}" "$A/pipelines/$PIPE3/test_report" > /tmp/test-report.json
doc=$(jq -e '.total_count != null' /tmp/test-report.json >/dev/null 2>&1 && echo 1 || echo 0)
tong=$(jq -r '.total_count // "-"' /tmp/test-report.json)
bo=$(jq -r '[.test_suites[]?.name] | join(",")' /tmp/test-report.json)
{ [ "$sn" = "failed" ] && [ "$sy" = "failed" ] && [ "$my" = "200" ] && [ "$mn" = "404" ] && [ "$doc" -eq 1 ]; } \
  && echo "CHECKPOINT 6 — ĐẠT (cả hai job failed; co-always=$my, khong-always=$mn; test_report total_count=$tong, bộ=[$bo])" \
  || echo "CHECKPOINT 6 — LỖI (sn=$sn sy=$sy, mn=$mn my=$my, đọc được test_report=$doc)"
```

Con số `total_count` và danh sách `bo` là **kết quả đo**, không phải điều kiện đạt. Ghi cả hai vào `hop-dong-rong.md` kèm phiên bản GitLab, rồi trả lời: `artifacts:reports:junit` của job **không** khai `when: always` có tới được server hay không? Nếu có, nó tới bằng đường nào khi `artifacts:paths` của cùng job đó trả 404?

### 4.3. Viết hiện vật `hop-dong-rong.md` (5 phút)

Chép bảng dưới đây vào hiện vật và **điền số của mình**, không chép số tham chiếu:

| | Ca artifact rỗng | Ca có khẳng định | Ca báo cáo mất khi job đỏ |
|---|---|---|---|
| Chế độ hỏng số | 1 | — (đã chặn) | 3 |
| Trạng thái job | `success` | `failed` | `failed` (đã đỏ vì lý do khác) |
| `GET /jobs/:id/artifacts` | `404` | `404` | `404` khi thiếu `when: always` |
| Ô của bảng hai thuộc tính | **im lặng, không chặn** | ồn ào, có chặn | im lặng, không chặn thêm |
| Ai phát hiện, sau bao lâu | người deploy, hàng tuần | pipeline, **ngay** | người đọc lỗi, 10–30 phút |
| Giá để chặn | — | **0,1 s** mỗi khẳng định | **1** dòng `when: always` |

---

## L5. Bước 3 — `cache:key` tính lúc nào, và trượt cache im lặng ra sao (30 phút)

Kiểm chứng QT 4.2, QT 6.1.

### 5.1. Bốn kiểu khoá trong một pipeline, và lần chạy đầu luôn trượt (10 phút)

```bash
cd ~/lab05
cat > khoa-lock.json <<'JSON'
{
  "phien_ban_lockfile": 1,
  "goi": { "left-pad": "1.3.0", "chalk": "5.3.0" }
}
JSON
```

```yaml
# ~/lab05/.gitlab-ci.yml — thay toàn bộ
stages: [do-khoa]

default:
  image: alpine:3.20

.mau-khoa:
  stage: do-khoa
  script:
    - mkdir -p .kho-npm
    - >
      if [ -f .kho-npm/dau.txt ]; then
        echo "KET_QUA=TRUNG khoa_cua_toi=$CI_JOB_NAME dau=$(cat .kho-npm/dau.txt)";
      else
        echo "KET_QUA=TRUOT khoa_cua_toi=$CI_JOB_NAME";
      fi
    - date +%s > .kho-npm/dau.txt
    - echo "so dong ERROR trong chinh script nay: 0"

khoa-lockfile:
  extends: .mau-khoa
  cache:
    key:
      files: [khoa-lock.json]      # hash NỘI DUNG lockfile — QT 4.2
    paths: [.kho-npm/]
    policy: pull-push

khoa-nhanh:
  extends: .mau-khoa
  cache:
    key: "nhanh-$CI_COMMIT_REF_SLUG"
    paths: [.kho-npm/]

khoa-co-dinh:
  extends: .mau-khoa
  cache:
    key: "lab05-co-dinh"
    paths: [.kho-npm/]

khoa-theo-commit:
  extends: .mau-khoa
  cache:
    key: "$CI_COMMIT_SHA"          # PHẢN-CACHE — QT 6.1
    paths: [.kho-npm/]
```

Lần chạy 1. Ở lần này **mọi** job đều trượt, và đây là lúc đo chế độ hỏng im lặng số 2:

```bash
PIPE_L1=$(day "lan 1: bon kieu khoa, lockfile v1")
cho_pipeline "$PIPE_L1"
job_bang "$PIPE_L1"

JL1=$(job_id "$PIPE_L1" "khoa-lockfile")
echo "--- các dòng liên quan cache trong trace ---"
job_log_sach "$JL1" | grep -iE 'Checking cache|Creating cache|extract|WARNING|KET_QUA' || true
```

Bốn job đều trượt, đều xanh, và không job nào có một dòng lỗi. Con số đầy đủ cho ca này được khẳng định ở CHECKPOINT 8 sau khi ta đã có cả ba lần chạy — vì cùng một `trace` đó còn phải trả lời câu hỏi về khoá trước.

### 5.2. Khoá tính lúc nào — hai lần chạy không đổi lockfile, một lần đổi (12 phút)

Khoá của `cache:key:files` **không** chốt ở `t0` như `rules` (buổi 04 QT 4.1). Runner phải checkout xong mới đọc được `khoa-lock.json` để hash — nên việc tính khoá **bắt buộc** xảy ra sau `t0`, trên runner. Ta lấy khoá bằng cách `grep` chính `trace`:

```bash
lay_khoa() {   # $1 = job id → in ra khoá cache runner đã dùng
  job_log_sach "$1" \
  | grep -oE 'Checking cache for [^ .]+' | head -1 | sed 's/^Checking cache for //'
}

K1=$(lay_khoa "$(job_id "$PIPE_L1" "khoa-lockfile")")
echo "khoá lần 1 = $K1"
```

Lần chạy 2 — **không** đổi `khoa-lock.json`, chỉ đổi một tệp khác:

```bash
echo "ghi chu lan 2" >> README.md
PIPE_L2=$(day "lan 2: KHONG doi lockfile")
cho_pipeline "$PIPE_L2"
K2=$(lay_khoa "$(job_id "$PIPE_L2" "khoa-lockfile")")
echo "khoá lần 2 = $K2"
```

Lần chạy 3 — đổi **một ký tự** trong lockfile:

```bash
sed -i 's/"1.3.0"/"1.3.1"/' khoa-lock.json
PIPE_L3=$(day "lan 3: DOI lockfile mot ky tu")
cho_pipeline "$PIPE_L3"
K3=$(lay_khoa "$(job_id "$PIPE_L3" "khoa-lockfile")")
echo "khoá lần 3 = $K3"
```

**CHECKPOINT 7 — `cache:key:files`: hai lần chạy không đổi lockfile cho CÙNG khoá, đổi lockfile cho khoá KHÁC.**

```bash
{ [ -n "$K1" ] && [ "$K1" = "$K2" ] && [ "$K3" != "$K1" ]; } \
  && echo "CHECKPOINT 7 — ĐẠT (K1=K2=$K1 ; K3=$K3 khác K1)" \
  || echo "CHECKPOINT 7 — LỖI (K1=$K1 K2=$K2 K3=$K3)"
```

Con số chốt của QT 4.2 cần nhớ: `cache:key:files` nhận **tối đa 2** tệp ở GitLab 17.7; `cache:fallback_keys` nhận **tối đa 5** khoá.

### 5.3. Trượt cache im lặng, và bảng bốn kiểu khoá × ba lần chạy (8 phút)

**CHECKPOINT 8 — lần chạy đầu TRƯỢT cache mà job vẫn `success`, và `trace` không có dòng lỗi nào.**

> Định nghĩa dùng cho phép đo này: "dòng lỗi" là dòng có tiền tố `ERROR` — tức thứ runner ghi khi có gì đó **làm job đỏ**. Dòng `WARNING` và dòng `Failed to extract cache` là **cảnh báo**, không đổi mã thoát; ta đếm riêng chúng để thấy đúng bản chất của ô *im lặng, không chặn*.

```bash
JL1=$(job_id "$PIPE_L1" "khoa-lockfile")
s1=$(job_tt "$JL1")
L=$(job_log_sach "$JL1")
n_err=$(printf '%s\n' "$L" | grep -cE '^ERROR' || true)
n_truot=$(printf '%s\n' "$L" | grep -c 'KET_QUA=TRUOT' || true)
n_canh=$(printf '%s\n' "$L" | grep -ciE 'WARNING|Failed to extract cache' || true)
{ [ "$s1" = "success" ] && [ "$n_err" -eq 0 ] && [ "$n_truot" -ge 1 ]; } \
  && echo "CHECKPOINT 8 — ĐẠT (status=$s1, 0 dòng ERROR, trượt cache=$n_truot, chỉ có $n_canh dòng cảnh báo — IM LẶNG, KHÔNG CHẶN)" \
  || echo "CHECKPOINT 8 — LỖI (status=$s1, ERROR=$n_err, trượt=$n_truot)"
```

Hai con số của QT 4.3 vừa được đo: **0** dòng lỗi khi trượt cache, **0** thay đổi mã thoát.

```bash
{
  echo "# Buổi 05 bước 3 — bốn kiểu khoá cache, ba lần chạy"
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version) · Runner: $(job_log_sach "$(job_id "$PIPE_L1" "khoa-lockfile")" | grep -m1 'Running with gitlab-runner')"
  echo "# lần 1 = lockfile v1 · lần 2 = KHÔNG đổi lockfile · lần 3 = đổi lockfile"
  printf 'kieu_khoa\tlan_1\tlan_2\tlan_3\tso_lan_trung\tti_le_trung\n'
  for j in khoa-lockfile khoa-nhanh khoa-co-dinh khoa-theo-commit; do
    r=""
    for p in "$PIPE_L1" "$PIPE_L2" "$PIPE_L3"; do
      ID=$(job_id "$p" "$j")
      kq=$(job_log_sach "$ID" | grep -oE 'KET_QUA=(TRUNG|TRUOT)' | head -1 | cut -d= -f2)
      r="$r\t${kq:-?}"
    done
    trung=$(printf "$r" | grep -o 'TRUNG' | wc -l | tr -d ' ')
    printf '%s%s\t%s\t%s\n' "$j" "$r" "$trung" "$(awk -v t="$trung" 'BEGIN{printf "%.0f%%", t*100/3}')"
  done
} | tee ~/lab05/bang-khoa-cache.tsv
```

Giá trị tham chiếu: `khoa-lockfile` **1/3** (trượt · trúng · trượt), `khoa-nhanh` **2/3**, `khoa-co-dinh` **2/3**, `khoa-theo-commit` **0/3**. Kéo dài ra repo thật: khoá theo lockfile trên repo có 20 lần chạy và 1 lần đổi lockfile cho **19/20 = 95%**; khoá theo commit cho **0%** vĩnh viễn, và log không hề có chữ "lỗi".

**Câu hỏi phải trả lời, ghi vào `bang-khoa-cache.tsv`:**

1. `khoa-co-dinh` và `khoa-nhanh` cùng cho 2/3 trong lab này. Nêu **một** tình huống thật mà hai kiểu khoá đó cho kết quả khác hẳn nhau.
2. Job `khoa-theo-commit` trúng 0/3 nhưng **xanh cả 3 lần**. Nó tốn thêm bao nhiêu giây mỗi lần chạy — và ai trong đội sẽ báo cáo con số đó nếu không ai đi đo?
3. Khoá lần 1 và lần 2 giống nhau tuy hai commit khác nhau. Điều đó chứng minh khoá được tính ở `t0` hay trên runner? Nêu **cơ chế**, không nêu kết luận.

---

## L6. Bước 4 — Sổ thu chi của cache: đo bốn kích thước, tính điểm hoà vốn (35 phút)

Kiểm chứng QT 6.2, QT 6.3, QT 6.4. Đây là bước sinh ra **cả hai** hiện vật cốt lõi của buổi.

Bảng dưới đây là **giá trị tham chiếu** của QT 6.3, đo trên executor `docker`, đĩa **SSD**, **8 vCPU**, GitLab CE 17.7 + Runner 17.7. Học viên **không** chép bảng này vào hiện vật — học viên đo lại và ghi số của chính mình:

| Cache | Số tệp | Tạo lại | Nén + tải lên | Tải + giải nén | Lãi mỗi lần trúng | Lỗ mỗi lần trượt | Số lần trúng để hoà vốn |
|---|---|---|---|---|---|---|---|
| 12 MB | 380 | 8 s | 3 s | 2 s | **+6 s** | −3 s | **1** |
| 45 MB | 1.200 | 22 s | 9 s | 6 s | **+16 s** | −9 s | **1** |
| 160 MB | 9.500 | 58 s | 26 s | 18 s | **+40 s** | −26 s | **1** |
| 380 MB | 28.000 | 95 s | 61 s | 44 s | **+51 s** | −61 s | **2** |

Đọc bảng: cache **380 MB** — thứ mà ai cũng bảo "to quá không đáng" — chỉ cần **2** lần trúng là hoà vốn. Đây là chỗ định lượng ngược lại. Nhưng nếu để `pull-push` ở cả 4 job và khoá đổi mỗi commit thì nó lỗ **61 s × 4 = 244 giây mỗi pipeline**, mãi mãi. Cái làm cache lỗ là **khoá**, không phải **kích thước**.

> Số ở bảng này chỉ đúng với đĩa SSD cục bộ. Runner `kubernetes` với volume mạng, hay executor `docker` trên đĩa mạng, cho số khác hẳn — **thứ tự lớn nhỏ giữa bốn dòng giữ nguyên**, còn tỉ lệ thì không. Vì vậy dòng đầu của `bang-do-cache.tsv` bắt buộc ghi loại đĩa và số vCPU của máy đã đo.

### 6.1. Công cụ 1 — `sinh-thu-muc.sh` (8 phút)

Bốn thư mục phụ thuộc **giả**, kích thước và số tệp đặt trước. Nội dung là văn bản kiểu JavaScript nên nén được khoảng 4 lần — giống `node_modules` thật hơn nhiều so với `/dev/urandom`, và điều đó quan trọng vì pha `Creating cache` là pha **nén**.

```bash
cat > ~/lab05/sinh-thu-muc.sh <<'SH'
#!/bin/sh
# sinh-thu-muc.sh — sinh thư mục phụ thuộc GIẢ với kích thước và số tệp đặt trước.
#
# Dùng:  sh sinh-thu-muc.sh <bo> [thu_muc_goc]
#   bo = 12mb | 45mb | 160mb | 380mb | tat-ca
#
# Bốn bộ khớp đúng bảng QT 6.3:
#   12mb  →    380 tệp ·  12 MB
#   45mb  →  1.200 tệp ·  45 MB
#   160mb →  9.500 tệp · 160 MB
#   380mb → 28.000 tệp · 380 MB
#
# Vì sao dùng nội dung văn bản chứ không /dev/urandom: cache được NÉN.
# Dữ liệu ngẫu nhiên không nén được, cho thời gian nén sai lệch so với
# node_modules / .m2 thật (vốn là mã nguồn, nén được 3–5 lần).
#
# Vì sao chia thành thư mục con 100 tệp: thư mục có 28.000 mục con làm
# chính lệnh tar chậm bất thường và không giống repo thật.
set -eu

BO="${1:?thiếu tên bộ: 12mb | 45mb | 160mb | 380mb | tat-ca}"
GOC="${2:-.}"

sinh_mot() {
  ten="$1"; so_tep="$2"; tong_mb="$3"
  dich="$GOC/$ten"
  rm -rf "$dich"
  mkdir -p "$dich"

  # kích thước mỗi tệp tính bằng KB, làm tròn LÊN để không hụt kích thước đích
  kb=$(( (tong_mb * 1024 + so_tep - 1) / so_tep ))
  [ "$kb" -lt 1 ] && kb=1

  mau="$GOC/.mau-$ten"
  yes 'module.exports = function (a, b) { return a + b; };   // dong dem cho du kich thuoc, nen duoc' \
    | head -c "$(( kb * 1024 ))" > "$mau"

  i=0
  while [ "$i" -lt "$so_tep" ]; do
    thu=$(( i / 100 ))
    d="$dich/goi-$thu"
    [ -d "$d" ] || mkdir -p "$d"
    cp "$mau" "$d/tep-$i.js"
    i=$(( i + 1 ))
  done
  rm -f "$mau"

  thuc_mb=$(du -sm "$dich" | cut -f1)
  thuc_tep=$(find "$dich" -type f | wc -l | tr -d ' ')
  echo "SINH_XONG ten=$ten so_tep_thuc=$thuc_tep kich_thuoc_thuc_mb=$thuc_mb kb_moi_tep=$kb"
}

case "$BO" in
  12mb)    sinh_mot kho-12mb    380   12 ;;
  45mb)    sinh_mot kho-45mb   1200   45 ;;
  160mb)   sinh_mot kho-160mb  9500  160 ;;
  380mb)   sinh_mot kho-380mb 28000  380 ;;
  tat-ca)
    sinh_mot kho-12mb    380   12
    sinh_mot kho-45mb   1200   45
    sinh_mot kho-160mb  9500  160
    sinh_mot kho-380mb 28000  380
    ;;
  *) echo "bo khong hop le: $BO" >&2; exit 2 ;;
esac
SH
chmod +x ~/lab05/sinh-thu-muc.sh
```

Thử ngay bộ nhỏ nhất trên máy chủ lab để biết script chạy được và biết máy mình nhanh chậm ra sao:

```bash
cd /tmp && time sh ~/lab05/sinh-thu-muc.sh 12mb /tmp
du -sm /tmp/kho-12mb ; find /tmp/kho-12mb -type f | wc -l ; rm -rf /tmp/kho-12mb
cd ~/lab05
```

### 6.2. Công cụ 2 — `doc-pha.sh`, hiện vật dùng lại ở buổi 14 (7 phút)

Giao diện GitLab chỉ cho **một** con số: tổng thời gian job. Ba con số ta cần nằm trong `trace` **thô**, ở các cặp `section_start:<epoch>:<tên>` và `section_end:<epoch>:<tên>`. Viết script này cho tử tế — buổi 14 sẽ gọi lại nó nguyên xi.

```bash
cat > ~/lab05/doc-pha.sh <<'SH'
#!/usr/bin/env bash
# doc-pha.sh — đọc trace của MỘT job qua API GitLab và in số GIÂY của ba pha:
#
#     Restoring cache        ← section  restore_cache
#     Downloading artifacts  ← section  download_artifacts
#     Creating cache         ← section  archive_cache
#
# Dùng:
#     bash doc-pha.sh <PID> <JOB_ID>            # mặc định --tsv
#     bash doc-pha.sh <PID> <JOB_ID> --tsv      # ba dòng: pha \t section \t giay
#     bash doc-pha.sh <PID> <JOB_ID> --json     # một đối tượng JSON
#     bash doc-pha.sh <PID> <JOB_ID> --tat-ca   # MỌI section runner ghi ra
#
# Cần: biến môi trường GITLAB và GITLAB_TOKEN; có curl và awk.
#
# CƠ CHẾ. Trace thô chứa các cặp điều khiển do runner ghi:
#     section_start:1738000000:restore_cache\r<esc>[0KRestoring cache
#     section_end:1738000006:restore_cache\r<esc>[0K
# Hiệu hai mốc epoch là số giây của pha, chính xác tới 1 giây. Cách này
# KHÔNG phụ thuộc việc runner có bật dấu thời gian từng dòng hay không,
# nên nó chạy được trên mọi cấu hình runner 14.0 trở lên.
#
# GIÁ TRỊ TRẢ VỀ CHO TỪNG PHA:
#     >= 0   số giây đo được
#     -1     runner KHÔNG chạy pha đó (ví dụ policy: pull thì không có
#            archive_cache; dependencies: [] thì không có download_artifacts)
# Số -1 là DỮ LIỆU, không phải lỗi: nó chính là bằng chứng của QT 6.2.
#
# MÃ THOÁT: 0 bình thường · 2 thiếu tham số · 3 không tải được trace
#           · 4 trace rỗng (job còn pending) · 5 trace không có section nào
set -uo pipefail

PID_IN="${1:-}"; JOB_IN="${2:-}"; DANG="${3:---tsv}"

if [ -z "$PID_IN" ] || [ -z "$JOB_IN" ]; then
  echo "Dùng: bash doc-pha.sh <PID> <JOB_ID> [--tsv|--json|--tat-ca]" >&2
  exit 2
fi
: "${GITLAB:?chưa đặt GITLAB}"
: "${GITLAB_TOKEN:?chưa đặt GITLAB_TOKEN}"

TRACE=$(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID_IN/jobs/$JOB_IN/trace") \
  || { echo "khong tai duoc trace cua job $JOB_IN (kiem PID, JOB_ID, token)" >&2; exit 3; }

if [ -z "$TRACE" ]; then
  echo "trace rong — job $JOB_IN co the dang pending hoac vua bi xoa log" >&2
  exit 4
fi

printf '%s' "$TRACE" | tr '\r' '\n' | awk -v dang="$DANG" -v job="$JOB_IN" '
  function ghi(ten,    s) {
    if (match($0, /section_(start|end):[0-9]+:[A-Za-z0-9_]+/)) {
      s = substr($0, RSTART, RLENGTH)
      split(s, p, ":")
      if (p[1] == "section_start") { if (!(p[3] in bd)) { bd[p[3]] = p[2]; thu_tu[++n] = p[3] } }
      else                         { kt[p[3]] = p[2] }
    }
  }
  /section_start:[0-9]+:/ { ghi() }
  /section_end:[0-9]+:/   { ghi() }
  END {
    if (n == 0) { print "KHONG-CO-SECTION" > "/dev/stderr"; exit 5 }

    ten_pha["restore_cache"]       = "Restoring cache"
    ten_pha["download_artifacts"]  = "Downloading artifacts"
    ten_pha["archive_cache"]       = "Creating cache"
    thu[1] = "restore_cache"; thu[2] = "download_artifacts"; thu[3] = "archive_cache"

    tong = 0
    for (i = 1; i <= 3; i++) {
      s = thu[i]
      if ((s in bd) && (s in kt)) { g[s] = kt[s] - bd[s]; tong += g[s] } else { g[s] = -1 }
    }

    if (dang == "--json") {
      printf "{\"job\":%s", job
      for (i = 1; i <= 3; i++) printf ",\"%s\":%d", thu[i], g[thu[i]]
      printf ",\"tong_ba_pha\":%d}\n", tong
    } else if (dang == "--tat-ca") {
      print "section\tgiay"
      for (i = 1; i <= n; i++) {
        s = thu_tu[i]
        printf "%s\t%d\n", s, ((s in kt) ? kt[s] - bd[s] : -1)
      }
    } else {
      print "pha\tsection\tgiay"
      for (i = 1; i <= 3; i++) printf "%s\t%s\t%d\n", ten_pha[thu[i]], thu[i], g[thu[i]]
      printf "TONG_BA_PHA\t-\t%d\n", tong
    }
  }
'
SH
chmod +x ~/lab05/doc-pha.sh
```

Thử ngay trên một job đã có từ bước 1 — nếu nó chạy được ở đây thì bảng của bước 4 mới có nghĩa:

```bash
bash ~/lab05/doc-pha.sh "$PID" "$(job_id "$PIPE1" "nhan-het")" --tsv
bash ~/lab05/doc-pha.sh "$PID" "$(job_id "$PIPE1" "nhan-khong")" --json
bash ~/lab05/doc-pha.sh "$PID" "$(job_id "$PIPE1" "nhan-het")" --tat-ca
```

Job `nhan-khong` có `dependencies: []` nên `download_artifacts` phải ra **−1**. Đó là bằng chứng script đọc đúng chỗ, không phải đoán.

### 6.3. Đo bốn kích thước và dựng `bang-do-cache.tsv` (12 phút)

Bốn job, bốn khoá riêng. Chạy **hai lần**: lần 1 trượt (đo *tạo lại* và *nén + tải lên*), lần 2 trúng (đo *tải + giải nén*).

```yaml
# ~/lab05/.gitlab-ci.yml — thay toàn bộ
stages: [do-cache]

variables:
  # Bump biến này lên 2, 3, ... nếu cần đo lại từ đầu: khoá đổi thì cache
  # cũ không còn được tìm thấy, và lần chạy tiếp theo lại TRƯỢT như lần 1.
  CACHE_GEN: "1"

default:
  image: alpine:3.20
  before_script:
    - apk add --no-cache coreutils >/dev/null 2>&1 || true

.do-mot-bo:
  stage: do-cache
  script:
    - T0=$(date +%s)
    - >
      if [ -d "$BO_THU_MUC" ] && [ "$(find "$BO_THU_MUC" -type f | wc -l)" -gt 0 ]; then
        echo "KET_QUA=TRUNG";
      else
        echo "KET_QUA=TRUOT";
        sh ./sinh-thu-muc.sh "$BO";
      fi
    - T1=$(date +%s)
    - echo "TAO_LAI_GIAY=$((T1-T0))"
    - echo "SO_TEP=$(find "$BO_THU_MUC" -type f | wc -l)"
    - echo "KICH_THUOC_MB=$(du -sm "$BO_THU_MUC" | cut -f1)"

do-kho-12mb:
  extends: .do-mot-bo
  variables: { BO: "12mb",  BO_THU_MUC: "kho-12mb" }
  cache: { key: "do-12mb-$CACHE_GEN",  paths: [kho-12mb/],  policy: pull-push }

do-kho-45mb:
  extends: .do-mot-bo
  variables: { BO: "45mb",  BO_THU_MUC: "kho-45mb" }
  cache: { key: "do-45mb-$CACHE_GEN",  paths: [kho-45mb/],  policy: pull-push }

do-kho-160mb:
  extends: .do-mot-bo
  variables: { BO: "160mb", BO_THU_MUC: "kho-160mb" }
  cache: { key: "do-160mb-$CACHE_GEN", paths: [kho-160mb/], policy: pull-push }

do-kho-380mb:
  extends: .do-mot-bo
  variables: { BO: "380mb", BO_THU_MUC: "kho-380mb" }
  cache: { key: "do-380mb-$CACHE_GEN", paths: [kho-380mb/], policy: pull-push }
```

```bash
cd ~/lab05
git add sinh-thu-muc.sh >/dev/null
PIPE_C1=$(day "buoc 4 lan 1: TRUOT cache, do tao lai va nen")
cho_pipeline "$PIPE_C1" 900
job_bang "$PIPE_C1"

PIPE_C2=$(day "buoc 4 lan 2: TRUNG cache, do tai va giai nen")
cho_pipeline "$PIPE_C2" 900
job_bang "$PIPE_C2"
```

Xác nhận lần 1 trượt và lần 2 trúng trước khi tin bất kỳ con số nào:

```bash
for p in "$PIPE_C1" "$PIPE_C2"; do
  echo "--- pipeline $p ---"
  for b in 12mb 45mb 160mb 380mb; do
    ID=$(job_id "$p" "do-kho-$b")
    echo "  kho-$b : $(job_log_sach "$ID" | grep -oE 'KET_QUA=(TRUNG|TRUOT)' | head -1)"
  done
done
```

Script dựng bảng — đây là hiện vật, nên nó phải chạy lại được, không phải gõ tay:

```bash
cat > ~/lab05/dung-bang.sh <<'SH'
#!/usr/bin/env bash
# dung-bang.sh — dựng bang-do-cache.tsv từ HAI pipeline của bước 4.
# Dùng: bash dung-bang.sh <PIPE_TRUOT> <PIPE_TRUNG> > bang-do-cache.tsv
set -uo pipefail
source ~/lab05/cong-cu.sh
P1="${1:?thiếu pipeline lần 1 (trượt)}"
P2="${2:?thiếu pipeline lần 2 (trúng)}"

giay_pha() {  # $1 = job id, $2 = tên section
  bash ~/lab05/doc-pha.sh "$PID" "$1" --tsv | awk -F'\t' -v s="$2" '$2==s{print $3}'
}
lay_so() {    # $1 = job id, $2 = tên biến in trong log
  job_log_sach "$1" | grep -oE "$2=[0-9]+" | tail -1 | cut -d= -f2
}

echo "# bang-do-cache.tsv — buổi 05 bước 4, ĐO trên chính máy này"
echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version) · project $PID"
echo "# $(job_log_sach "$(job_id "$P1" "do-kho-12mb")" | grep -m1 'Running with gitlab-runner')"
echo "# may do: $(nproc) vCPU · RAM $(free -g | awk '/Mem:/{print $2}') GB · dia: DIEN-VAO-DAY (SSD hay HDD hay dia mang)"
echo "# pipeline truot=$P1 · pipeline trung=$P2 · ngay do $(date -Iseconds)"
echo "# hoa_von = lam tron len cua  nen_va_tai / (tao_lai - tai_va_giai_nen)"
printf 'cache\tso_tep\ttao_lai_giay\tnen_va_tai_giay\ttai_va_giai_nen_giay\tlai_moi_lan_trung\tlo_moi_lan_truot\tso_lan_trung_hoa_von\n'

for bo in 12mb 45mb 160mb 380mb; do
  j1=$(job_id "$P1" "do-kho-$bo")
  j2=$(job_id "$P2" "do-kho-$bo")
  tao=$(lay_so "$j1" TAO_LAI_GIAY)
  sotep=$(lay_so "$j1" SO_TEP)
  nen=$(giay_pha "$j1" archive_cache)
  giai=$(giay_pha "$j2" restore_cache)
  awk -v a="kho-$bo" -v b="${sotep:-0}" -v t="${tao:-0}" -v n="${nen:-0}" -v g="${giai:-0}" 'BEGIN{
    OFS="\t"
    den = t - g
    lai = den
    lo  = -n
    hv  = (den > 0) ? int((n + den - 1) / den) : "vo-cuc"
    print a, b, t, n, g, (lai>0 ? "+" lai : lai), lo, hv
  }'
done
SH
chmod +x ~/lab05/dung-bang.sh

bash ~/lab05/dung-bang.sh "$PIPE_C1" "$PIPE_C2" | tee ~/lab05/bang-do-cache.tsv
```

Sửa dòng `# may do:` — thay `DIEN-VAO-DAY` bằng loại đĩa thật của máy. Thiếu con số đó thì cả bảng không so được với bảng của người khác, và hạng mục này **0 điểm** ở §L11.

**CHECKPOINT 9 — `bang-do-cache.tsv` có đúng 4 dòng dữ liệu, mọi ô giây > 0, và cột hoà vốn khớp phép chia làm tròn lên.**

```bash
awk -F'\t' '
  $1 ~ /^kho-/ {
    n++
    if ($3+0 <= 0 || $4+0 <= 0 || $5+0 <= 0) { xau++; ly = ly " " $1 ":co-o-giay-<=0" }
    den = $3 - $5
    if (den <= 0) { xau++; ly = ly " " $1 ":tao_lai<=giai_nen"; next }
    hv = int(($4 + den - 1) / den)
    if (hv != $8+0) { xau++; ly = ly " " $1 ":hoa_von=" $8 "-nhung-phai-la-" hv }
  }
  END {
    if (n == 4 && xau == 0)
      print "CHECKPOINT 9 — ĐẠT (4 dòng dữ liệu, mọi ô giây > 0, cột hoà vốn khớp phép chia)"
    else
      print "CHECKPOINT 9 — LỖI (" n " dòng, " xau+0 " chỗ sai:" ly ")"
  }' ~/lab05/bang-do-cache.tsv
```

**Câu hỏi phải trả lời, ghi ngay vào `bang-do-cache.tsv`:**

1. Dòng nào có điểm hoà vốn cao nhất, và nó có phải dòng có cache **to nhất** không? Nếu có, chênh lệch giữa dòng đó và dòng 160 MB là bao nhiêu lần trúng?
2. Với tỉ lệ trúng đo được ở bước 3 cho khoá theo lockfile, dòng 380 MB **lãi hay lỗ** trên máy của mình? Viết ra phép tính `p × (tạo_lại − giải_nén) > nén_và_tải` với số của mình.
3. So bốn dòng: khi kích thước tăng **31 lần** (12 MB → 380 MB), thời gian nén tăng bao nhiêu lần, và **số tệp** tăng bao nhiêu lần? Đại lượng nào giải thích thời gian nén tốt hơn?

### 6.4. `policy: pull` bỏ hẳn pha `Creating cache` (5 phút)

```yaml
# ~/lab05/.gitlab-ci.yml — thay toàn bộ
stages: [tao, tieu-thu]

variables:
  CACHE_GEN: "1"

default:
  image: alpine:3.20

policy-pull-push:
  stage: tao
  cache:
    key: "policy-45mb-$CACHE_GEN"
    paths: [kho-45mb/]
    policy: pull-push            # mặc định: đọc VÀ ghi
  script:
    - test -d kho-45mb || sh ./sinh-thu-muc.sh 45mb
    - echo "so tep: $(find kho-45mb -type f | wc -l)"

policy-pull:
  stage: tieu-thu
  cache:
    key: "policy-45mb-$CACHE_GEN"
    paths: [kho-45mb/]
    policy: pull                 # chỉ ĐỌC — job này không tạo ra gì mới
  script:
    - echo "so tep nhan duoc tu cache: $(find kho-45mb -type f 2>/dev/null | wc -l)"
```

```bash
PIPE_P=$(day "buoc 4: policy pull so pull-push")
cho_pipeline "$PIPE_P" 900
JPP=$(job_id "$PIPE_P" "policy-pull-push")
JP=$(job_id  "$PIPE_P" "policy-pull")
bash ~/lab05/doc-pha.sh "$PID" "$JPP" --tsv
bash ~/lab05/doc-pha.sh "$PID" "$JP"  --tsv
```

**CHECKPOINT 10 — job `policy: pull` KHÔNG có pha `Creating cache`, job `pull-push` thì có.**

```bash
g_pp=$(bash ~/lab05/doc-pha.sh "$PID" "$JPP" --tsv | awk -F'\t' '$2=="archive_cache"{print $3}')
g_p=$(bash  ~/lab05/doc-pha.sh "$PID" "$JP"  --tsv | awk -F'\t' '$2=="archive_cache"{print $3}')
d_pp=$(job_log_sach "$JPP" | grep -c 'Creating cache' || true)
d_p=$(job_log_sach  "$JP"  | grep -c 'Creating cache' || true)
{ [ "$g_p" = "-1" ] && [ "$d_p" -eq 0 ] && [ "$g_pp" -ge 0 ] && [ "$d_pp" -ge 1 ]; } \
  && echo "CHECKPOINT 10 — ĐẠT (pull-push: archive_cache=${g_pp}s, $d_pp dòng Creating cache; pull: archive_cache=$g_p, $d_p dòng)" \
  || echo "CHECKPOINT 10 — LỖI (pull-push=$g_pp/$d_pp, pull=$g_p/$d_p)"
```

Quy ra tiền: với cache 380 MB, bỏ `Creating cache` ở **3** job test tiết kiệm **3 × 61 = 183 giây** mỗi pipeline. Nhân với số lần chạy một ngày của repo mình — con số đó là toàn bộ nội dung cần nói khi đề xuất `policy: pull` cho đội.

### 6.5. Tuỳ chọn — MinIO làm cache dùng chung (đọc 3 phút, làm ngoài giờ nếu lớp không đủ thời gian)

Kiểm chứng QT 6.4. **Phần này đụng `config.toml` — hạ tầng dùng chung của cả lớp (buổi 02 QT 4.3).** Ai chưa sao lưu theo §L1 thì **dừng ở đây**, bỏ phần này, và vẫn có đủ cả hai hiện vật cốt lõi. Nếu cả lớp dùng chung một runner thì chỉ giảng viên làm trước lớp.

Trước khi sửa gì, đo hiện trạng: với `N` runner **không** có cache dùng chung, tỉ lệ trúng trần ở khoảng `1/N` vì cache nằm trên đĩa của chính runner đã tạo ra nó. Giá trị tham chiếu với 2 runner: trúng khoảng **3/6**.

```bash
# 1) Dựng MinIO — một container 512 MB RAM, cổng 9000
docker run -d --name lab-minio \
  --network ntkgitlab-lab_lab \
  -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=labminio -e MINIO_ROOT_PASSWORD=labminio12345 \
  --memory 512m \
  quay.io/minio/minio:latest server /data --console-address ":9001"
sleep 8
docker exec lab-minio mc alias set loc http://127.0.0.1:9000 labminio labminio12345 2>/dev/null \
  || echo "khong co mc trong image — tao bucket bang buoc 2 duoi day"
docker exec lab-minio mc mb loc/gitlab-cache 2>/dev/null || true
```

```toml
# mảnh — dán vào /etc/gitlab-runner/config.toml, BÊN TRONG khối [[runners]]
# đang dùng cho lab, ngay sau mục [runners.docker]. Thụt lề đúng như dưới.
  [runners.cache]
    Type = "s3"
    Shared = true
    [runners.cache.s3]
      ServerAddress = "lab-minio:9000"
      AccessKey = "labminio"
      SecretKey = "labminio12345"
      BucketName = "gitlab-cache"
      Insecure = true
```

```bash
# 2) Áp cấu hình rồi khởi động lại runner (buổi 02 đã đo: runner KHÔNG tự nạp lại)
docker exec -it lab-runner vi /etc/gitlab-runner/config.toml     # hoặc chỉnh bằng cách khác
docker restart lab-runner >/dev/null && sleep 20
docker exec lab-runner sh -c 'grep -A8 "\[runners.cache\]" /etc/gitlab-runner/config.toml'

# 3) Bump CACHE_GEN rồi chạy 6 pipeline, đếm số lần trúng
sed -i 's/CACHE_GEN: "1"/CACHE_GEN: "9"/' ~/lab05/.gitlab-ci.yml
for i in 1 2 3 4 5 6; do
  P=$(day "minio lan $i"); cho_pipeline "$P" 600 >/dev/null
  ID=$(job_id "$P" "policy-pull-push")
  echo "lan $i : $(job_log_sach "$ID" | grep -oE 'Successfully extracted cache|Failed to extract cache' | head -1)"
done
```

Ghi vào `bang-phan-loai.md`: số lần trúng **trước** khi bật cache dùng chung và **sau**. Giá trị tham chiếu là **3/6** lên **5/6** — lần đầu luôn trượt, không cách nào tránh. Và ghi thêm một câu: `cache:fallback_keys` giảm thiệt hại khi khoá đổi, nhưng **không** sửa được việc cache nằm ở máy khác.

**Bắt buộc:** §L8.1 khôi phục `config.toml` và xoá container MinIO. CHECKPOINT 12 kiểm `diff`.

---

## L7. Bước 5 — Bảng phân loại, thứ tự phục hồi, `expire_in` (15 phút)

Bước này ngắn nhất nhưng nó là bước biến bốn bước trước thành một quy tắc dùng được ở mọi repo. Ba việc: dán lại `workflow` chuẩn để số đo không bị đếm hai lần, **đo** thứ tự phục hồi hai kho, và lập bảng phân loại mười thư mục thật.

### 5.1. Dán lại `workflow` chuẩn của buổi 04 (2 phút)

Không có khối này, mỗi lần push lên một nhánh đang có merge request mở sinh **2** pipeline cho **1** commit (buổi 04 QT 5.2). Ở bước 4 điều đó làm mọi con số giây bị đếm hai lần; ở bước 5 nó làm cache bị ghi hai lượt và thứ tự phục hồi khó đọc.

```yaml
# mảnh — dán vào ĐẦU ~/lab05/.gitlab-ci.yml, nguyên khối, không viết lại
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS'
      when: never
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
    - if: '$CI_COMMIT_TAG'
    - if: '$CI_COMMIT_BRANCH'
```

### 5.2. Đo thứ tự phục hồi: cùng một đường dẫn ở hai kho (7 phút)

Đây là phần **đo** của QT 7.2. Ta không kết luận từ tài liệu rằng artifact thắng cache; ta dựng đúng ca trùng đường dẫn, đọc nội dung job sau nhận được, **và** đọc số dòng của hai pha trong `trace`. Hai bằng chứng, không một.

Ba job: một job chỉ ghi vào **cache**, một job chỉ ghi vào **artifact**, và job thứ ba nhận cả hai với **cùng** đường dẫn `chung/dau.txt`.

```yaml
# mảnh — dán vào ~/lab05/.gitlab-ci.yml, thêm 'trung-duong-dan' vào stages
ghi-cache:
  stage: trung-duong-dan
  script:
    - mkdir -p chung && echo "TU-CACHE" > chung/dau.txt
    - 'echo "ghi vao cache: $(cat chung/dau.txt)"'
  cache:
    key: trung-duong-dan-v1
    paths: [chung/]
    policy: pull-push

ghi-artifact:
  stage: trung-duong-dan
  script:
    - mkdir -p chung && echo "TU-ARTIFACT" > chung/dau.txt
    - 'echo "ghi vao artifact: $(cat chung/dau.txt)"'
  artifacts:
    paths: [chung/dau.txt]
    expire_in: 1 hour

doc-hai-kho:
  stage: doc-hai-kho
  needs: [ghi-cache, ghi-artifact]
  cache:
    key: trung-duong-dan-v1
    paths: [chung/]
    policy: pull            # chỉ đọc — QT 6.2
  script:
    - 'echo "NOI_DUNG=$(cat chung/dau.txt)"'
    - '[ -f chung/dau.txt ] || { echo "khong co tep — bao cao va dung"; exit 1; }'
```

Chạy hai lần: lần đầu cache còn rỗng nên chưa có gì để tranh; **lần thứ hai** mới là lần đo được, vì lúc đó cache đã có `TU-CACHE` trong đó.

```bash
cd ~/lab05
P_L1=$(day "trung duong dan lan 1"); cho_pipeline "$P_L1" 420
P_L2=$(day "trung duong dan lan 2"); cho_pipeline "$P_L2" 420
J=$(job_id "$P_L2" "doc-hai-kho")
job_log_sach "$J" | grep -nE 'Restoring cache|Downloading artifacts|NOI_DUNG='
```

**CHECKPOINT 11 — cùng một đường dẫn ở hai kho: nội dung nhận được là của ARTIFACT, và trong `trace` dòng `Restoring cache` đứng TRƯỚC dòng `Downloading artifacts`.**

```bash
J=$(job_id "$P_L2" "doc-hai-kho")
L=$(job_log_sach "$J")
ND=$(printf '%s' "$L" | grep -oE 'NOI_DUNG=[A-Z-]+' | tail -1 | cut -d= -f2)
DC=$(printf '%s' "$L" | grep -nE 'Restoring cache'      | head -1 | cut -d: -f1)
DA=$(printf '%s' "$L" | grep -nE 'Downloading artifacts' | head -1 | cut -d: -f1)
echo "noi dung nhan duoc = $ND · dong Restoring cache = ${DC:-khong-co} · dong Downloading artifacts = ${DA:-khong-co}"
if [ "$ND" = "TU-ARTIFACT" ] && [ -n "$DC" ] && [ -n "$DA" ] && [ "$DC" -lt "$DA" ]; then
  echo "CHECKPOINT 11 — ĐẠT"
else
  echo "CHECKPOINT 11 — LỖI"
fi
```

Ghi kết quả vào `bang-phan-loai.md`, kèm **bốn** bước đầu job theo đúng thứ tự quan sát được: clone → phục hồi cache → tải artifacts → `script`. Đây là con số **4** của QT 7.2, và nó là con số **đo được**, không phải con số tra được: nếu một phiên bản runner nào đổi thứ tự hai pha giữa thì kết luận "artifact thắng cache" đổi theo, và bảng ở trên là cách duy nhất biết điều đó.

> **Nếu có Ultimate:** không có tính năng nào của Premium hay Ultimate đổi thứ tự bốn bước này. Đây là hành vi của runner, không phải của tầng license.

### 5.3. `expire_in` và hoá đơn dung lượng (3 phút)

`expire_in` là hạn **giữ**, không phải hạn **dùng** (QT 5.5). Đọc dung lượng artifact thật của project bằng một lệnh:

```bash
curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID?statistics=true" \
| jq '{artifact_byte: .statistics.job_artifacts_size,
       artifact_MB: ((.statistics.job_artifacts_size/1048576)*10|round/10)}'
```

Rồi tính hoá đơn cho một repo thật bằng ba con số của chính lớp mình:

```bash
SO_PIPELINE_NGAY=20        # sửa theo repo của bạn
MB_MOI_PIPELINE=45
NGAY_GIU=30
echo "giu mac dinh : $(( SO_PIPELINE_NGAY * MB_MOI_PIPELINE * NGAY_GIU / 1024 )) GB"
echo "giu 1 gio    : ~$(( MB_MOI_PIPELINE * 2 )) MB   # chi con pipeline dang chay"
```

Với 20 pipeline/ngày × 45 MB × 30 ngày, con số là **27 GB**; đổi hiện vật trung gian sang `expire_in: 1 hour` còn khoảng **90 MB**. Ghi cả hai vào `bang-phan-loai.md`, kèm một câu về tuỳ chọn *keep latest artifacts*: nó giữ artifact của pipeline mới nhất **bất chấp** `expire_in`, nên một project bật nó sẽ không bao giờ về 0 dù `expire_in` ngắn tới đâu.

### 5.4. Bảng phân loại mười thư mục thật (3 phút)

Áp **ba** câu hỏi của QT 7.1 theo đúng thứ tự, dừng ở câu đầu tiên trả lời được. Điền cột "Vì sao" bằng **số hiệu câu hỏi**, không bằng cảm nhận. Đây là hiện vật trả lời trực tiếp câu 3 của BTVN 4 buổi 04.

```bash
cat >> ~/lab05/bang-phan-loai.md <<'MD'

## Bảng phân loại mười thư mục — áp ba câu hỏi của QT 7.1

| Thư mục | Ngôn ngữ | Kho đúng | Câu hỏi số mấy quyết định | Ghi chú |
|---|---|---|---|---|
| `dist/`, `build/` | Node, chung | `artifacts` | 1 — job deploy SAI nếu thiếu | `expire_in` ngắn cho bản trung gian |
| `bao-cao/junit.xml` | chung | `artifacts` | 3 — người ngoài pipeline cần đọc | bắt buộc `when: always` (QT 5.4) |
| `sbom.cdx.json` | chung | `artifacts` | 3 — đầu vào của buổi 25, 31, 34 | không bao giờ đi bằng cache |
| `.npm/` | Node | `cache` | 2 — tái tạo từ `package-lock.json` | `key:files` trên lockfile |
| `node_modules/` | Node | `cache` | 2 — tái tạo được | KHÔNG dùng artifacts: 90 MB mỗi job |
| `~/.m2/repository` | Java | `cache` | 2 — tái tạo từ `pom.xml` | buổi 17 mở rộng |
| `.gradle/caches` | Java | `cache` | 2 — tái tạo từ khai báo | buổi 17 |
| `GOMODCACHE`, `GOCACHE` | Go | `cache` | 2 — hai loại cache khác nhau | buổi 19 tách hai loại |
| `.venv/` hoặc `~/.cache/pip` | Python | `cache` | 2 — tái tạo từ lockfile | buổi 18 |
| `chart-1.4.2.tgz` | Helm | `artifacts` | 1 và 3 — deploy cần, và phải rollback được | buổi 26, 27 |
MD
```

---

## L8. Nộp sản phẩm và dọn dẹp (10 phút)

### L8.1. Khôi phục hạ tầng dùng chung — BẮT BUỘC nếu đã làm phần tuỳ chọn của bước 4

Phần tuỳ chọn đã thêm một mục `[runners.cache]` vào `config.toml` và dựng một container MinIO. Cả hai phải trả về nguyên trạng: `config.toml` là hạ tầng dùng chung của **cả lớp** (buổi 02 QT 4.3), và một mục cache trỏ tới MinIO đã tắt sẽ làm **mọi** job của mọi buổi sau chậm thêm vài giây mỗi lần thử kết nối rồi bỏ.

```bash
# 1) Khôi phục đúng bản sao lưu đã tạo ở §L1
docker cp ~/lab05/sao-luu/config.toml.truoc-buoi-05 lab-runner:/etc/gitlab-runner/config.toml
docker restart lab-runner >/dev/null && sleep 20

# 2) Xoá MinIO
docker rm -f lab-minio >/dev/null 2>&1 || true
docker volume rm lab-minio-data >/dev/null 2>&1 || true

# 3) Đối chiếu
docker exec lab-runner cat /etc/gitlab-runner/config.toml > /tmp/config.sau
diff ~/lab05/sao-luu/config.toml.truoc-buoi-05 /tmp/config.sau && echo "config.toml KHOP ban sao luu"
```

Ai **không** làm phần tuỳ chọn thì bỏ qua mục này, và CHECKPOINT 12 vẫn đạt — đoạn kiểm dưới đây bỏ qua phép `diff` khi không tìm thấy tệp sao lưu.

### L8.2. Gom hiện vật và kiểm bằng lệnh

```bash
DICH=~/gitlab-portfolio/05-artifact-va-cache
mkdir -p "$DICH"
cd ~/lab05
cp -f bang-artifact.tsv hop-dong-rong.md bang-khoa-cache.tsv \
      bang-do-cache.tsv doc-pha.sh sinh-thu-muc.sh bang-phan-loai.md \
      .gitlab-ci.yml checkpoint.log "$DICH"/ 2>/dev/null
ls -l "$DICH"
```

```bash
cat > ~/lab05/kiem-hien-vat.sh <<'SH'
#!/usr/bin/env bash
# Kiểm hiện vật nộp của buổi 05. Dùng: bash kiem-hien-vat.sh [thu_muc]
D="${1:-$HOME/gitlab-portfolio/05-artifact-va-cache}"
loi=0
bao() { if [ "$1" = 0 ]; then printf '  ĐẠT   %s\n' "$2"; else printf '  LỖI   %s\n' "$2"; loi=$((loi+1)); fi; }

for f in bang-artifact.tsv hop-dong-rong.md bang-khoa-cache.tsv bang-do-cache.tsv \
         doc-pha.sh sinh-thu-muc.sh bang-phan-loai.md .gitlab-ci.yml checkpoint.log; do
  [ -s "$D/$f" ]; bao $? "có $f và khác rỗng"
done

# hai hiện vật CỐT LÕI phải đúng nội dung, không chỉ tồn tại
awk -F'\t' 'NR>1 && $1 !~ /^#/ && NF>=8 {n++} END {exit !(n==4)}' "$D/bang-do-cache.tsv"
bao $? "bang-do-cache.tsv có đúng 4 dòng dữ liệu, mỗi dòng 8 cột"

awk -F'\t' 'NR>1 && $1 !~ /^#/ && NF>=8 {
              if ($3+0<=0 || $4+0<=0 || $5+0<=0) bad=1
              hv = int($4/($3-$5)); if ($4 % ($3-$5) != 0) hv++
              if ($8+0 != hv) bad=1
            } END {exit bad}' "$D/bang-do-cache.tsv"
bao $? "mọi ô giây > 0 và cột hoà vốn khớp phép chia làm tròn lên"

grep -q 'may do:' "$D/bang-do-cache.tsv" && ! grep -q 'DIEN-VAO-DAY' "$D/bang-do-cache.tsv"
bao $? "bang-do-cache.tsv ghi rõ máy đã đo (đã thay DIEN-VAO-DAY)"

bash -n "$D/doc-pha.sh"; bao $? "doc-pha.sh không lỗi cú pháp"
grep -qE 'section_start|section_end' "$D/doc-pha.sh"
bao $? "doc-pha.sh đọc mốc section_start/section_end (không đoán từ dòng log)"

grep -c 'ĐẠT' "$D/checkpoint.log" | awk '{exit !($1>=12)}'
bao $? "checkpoint.log có đủ 12 dòng ĐẠT"

grep -q 'TU-ARTIFACT' "$D/bang-phan-loai.md"
bao $? "bang-phan-loai.md ghi kết quả đo thứ tự phục hồi (QT 7.2)"

grep -qE '\| *`?dist/' "$D/bang-phan-loai.md" && grep -qE 'GOMODCACHE|\.m2' "$D/bang-phan-loai.md"
bao $? "bang-phan-loai.md có bảng mười thư mục"

SL="$HOME/lab05/sao-luu/config.toml.truoc-buoi-05"
if [ -f "$SL" ]; then
  docker exec lab-runner cat /etc/gitlab-runner/config.toml > /tmp/config.sau 2>/dev/null
  diff -q "$SL" /tmp/config.sau >/dev/null 2>&1
  bao $? "config.toml đã khôi phục khớp bản sao lưu (phần tuỳ chọn)"
  ! docker ps --format '{{.Names}}' | grep -qx lab-minio
  bao $? "container lab-minio đã xoá"
else
  printf '  BỎ QUA  không làm phần tuỳ chọn — không cần khôi phục config.toml\n'
fi

echo "---"
[ "$loi" -eq 0 ] && echo "CHECKPOINT 12 — ĐẠT" || echo "CHECKPOINT 12 — LỖI ($loi lỗi)"
exit "$loi"
SH
bash ~/lab05/kiem-hien-vat.sh
```

**CHECKPOINT 12 — mọi hiện vật tồn tại và hợp lệ về NỘI DUNG, và hạ tầng dùng chung đã trả về nguyên trạng.**

Đoạn trên **là** checkpoint 12: nó không kiểm tệp có tồn tại hay không mà kiểm ba thứ khó gian hơn — bảng đo có đúng bốn dòng và cột hoà vốn khớp phép chia, `doc-pha.sh` thật sự đọc mốc `section_start`/`section_end` chứ không đoán từ dòng log, và `config.toml` khớp bản sao lưu.

### L8.3. Dọn project lab

Giữ lại `~/lab05` tới hết buổi 06 — bước 1 buổi 06 dùng lại `cong-cu.sh` và `doc-pha.sh`. Chỉ xoá project trên GitLab khi đã nộp hiện vật:

```bash
# Xoá project lab (chỉ chạy khi kiem-hien-vat.sh đã ĐẠT)
curl -sf --request DELETE "${H[@]}" "$GITLAB/api/v4/projects/$PID" && echo "da xoa project $PID"
# Xoá bốn thư mục nặng đã sinh ở bước 4 — chúng chiếm khoảng 600 MB
rm -rf ~/lab05/kho-12mb ~/lab05/kho-45mb ~/lab05/kho-160mb ~/lab05/kho-380mb
```

---

## L9. Xử lý sự cố thường gặp trong lab

| # | Triệu chứng | Nguyên nhân | Cách khắc phục |
|---|---|---|---|
| 1 | `art_http` trả `404` cho job **đã** có artifact | Đang gọi bằng token thiếu scope `api`, hoặc artifact đã hết hạn `expire_in` | Kiểm bằng `curl -sf "${H[@]}" "$A/jobs/$J" \| jq .artifacts_expire_at`; nếu `null` thì là vấn đề token — tạo lại token scope `api` |
| 2 | `art_http` trả `302` chứ không phải `200` | Thiếu `-L`: endpoint artifact trả về chuyển hướng tới nơi lưu | Ba hàm `art_*` đã có `-L`; nếu tự viết `curl` thì phải thêm |
| 3 | CHECKPOINT 2 cho số tệp **lớn hơn** kỳ vọng | Còn artifact của một pipeline trước sót lại trong nhánh, hoặc job đang tải cả artifact của stage xa hơn — đúng như QT 5.1 | In `find . -type f` vào hiện vật rồi đọc danh sách; đừng chỉ đếm |
| 4 | CHECKPOINT 3 cho số tệp khác `0` | `dependencies: []` bị đặt sai cấp (dưới `script` chẳng hạn), nên YAML hợp lệ mà không có tác dụng | Đọc tệp **sau phân giải** bằng `ci/lint` (buổi 03 QT 4.3), không đọc YAML thô |
| 5 | Job `build-rong` **đỏ** thay vì xanh | `script` có lệnh cuối trả mã thoát khác 0 (thường do `cp` không tìm thấy tệp) | Đây là ca đối chứng ngược: bỏ lệnh gây lỗi ra, chỉ để `artifacts:paths` trỏ đường dẫn không tồn tại |
| 6 | `GET /pipelines/:id/test_report` trả `404` | Job không sinh `artifacts:reports:junit`, hoặc tệp XML sai định dạng nên bị bỏ | Kiểm `trace` tìm dòng cảnh báo về report; và kiểm tệp XML bằng `xmllint --noout` |
| 7 | Không tìm thấy khoá cache trong `trace` | Runner ghi khoá ở dòng `Checking cache for <khoá>...`; log đã bị cắt vì quá dài | Dùng `job_log_sach` rồi `grep -oE 'Checking cache for [^.]+'`; nếu log bị cắt thì giảm bớt job trong pipeline |
| 8 | Cả bốn job bước 4 đều **trượt** cache mọi lần | `CACHE_GEN` đã bump nhưng `cache:key` không tham chiếu tới nó, nên khoá cũ vẫn dùng lại | Đọc khoá thật bằng `lay_khoa`, đừng suy từ YAML |
| 9 | Cả bốn job đều **trúng** cache ngay lần đầu | Đĩa runner còn cache của lần chạy trước với cùng khoá | Bump `CACHE_GEN`, hoặc `docker exec lab-runner rm -rf /cache/*` rồi chạy lại |
| 10 | Giây của `Creating cache` bằng `0` hoặc rỗng | Job không tạo cache (đang `policy: pull`), hoặc `doc-pha.sh` đang khớp tên section sai | `job_log "$J" \| grep -oE 'section_start:[0-9]+:[a-z_]+'` để xem đúng tên section của phiên bản runner này |
| 11 | Bảng `bang-do-cache.tsv` có ô giây **âm** | Lấy hiệu hai mốc epoch theo thứ tự ngược | `doc-pha.sh` phải lấy `section_end − section_start`; kiểm bằng một job đã biết thời lượng |
| 12 | Sinh thư mục 380 MB làm đầy đĩa | Bốn thư mục cộng lại khoảng 600 MB, cộng cache nén trên runner nữa | `df -h /` trước khi chạy; §L8.3 xoá bốn thư mục sau khi đo xong |
| 13 | `sinh-thu-muc.sh` chạy rất lâu ở bộ 28.000 tệp | Tạo nhiều tệp nhỏ là thao tác nặng về inode, không về byte | Đây là kết quả đúng và là lý do bảng có cột **Số tệp**; đừng "tối ưu" bằng cách giảm số tệp |
| 14 | Pipeline sinh **hai** bản cho một commit, số giây bị đếm hai lần | Chưa dán `workflow` chuẩn của buổi 04 | Làm §L7 mục 5.1 **trước** khi đo lại bất cứ con số nào |
| 15 | Job `doc-hai-kho` in `TU-CACHE` chứ không phải `TU-ARTIFACT` | Chạy ở lần **đầu** khi cache còn rỗng, hoặc job `ghi-artifact` upload rỗng (đúng ca QT 5.3) | Chạy lần thứ hai; và kiểm `art_http` của `ghi-artifact` bằng **200** trước khi kết luận |
| 16 | `Restoring cache` **không** xuất hiện trong `trace` của `doc-hai-kho` | Khoá cache khác nhau giữa hai job, nên không có gì để phục hồi | So khoá của `ghi-cache` và `doc-hai-kho` bằng `lay_khoa`; hai job phải cùng `cache:key` |
| 17 | Sau khi bật MinIO, mọi job chậm thêm 5–10 giây | `[runners.cache]` trỏ tới địa chỉ runner không tới được, nên mỗi job chờ hết hạn kết nối rồi bỏ | Dùng tên container trong cùng mạng docker, không dùng `localhost`; nếu vẫn lỗi thì §L8.1 khôi phục và chấp nhận bỏ phần tuỳ chọn |
| 18 | `kiem-hien-vat.sh` báo lỗi cột hoà vốn | Cột 8 điền bằng tay và làm tròn **xuống** | Công thức là làm tròn **lên**: `hv = ceil(nén_và_tải / (tạo_lại − giải_nén))` |

---

## L10. Bài tập mở rộng

Sáu bài đầu làm được với hạ tầng đã có. Bài 7 và 8 dành cho ai muốn đi trước tới buổi 14 và buổi 17.

**BT1 — Điểm hoà vốn của repo thật.** Lấy một repo thật của bạn, đo ba con số (tạo lại phụ thuộc · nén và tải lên · tải và giải nén) rồi tính điểm hoà vốn theo công thức QT 6.3.
*Câu hỏi phải trả lời:* repo của bạn cần **bao nhiêu** lần trúng cache để hoà vốn, và tỉ lệ trúng thật trong 20 lần chạy gần nhất là bao nhiêu? Cache của bạn đang **lãi** hay **lỗ**?

**BT2 — Săn artifact rỗng.** Viết một job chạy được trên repo thật: nó đọc `.gitlab-ci.yml`, liệt kê mọi khối `artifacts:paths`, và với mỗi job đã chạy trong pipeline gần nhất thì gọi `art_http` để phân loại 200 / 404.
*Câu hỏi phải trả lời:* có bao nhiêu job đang **xanh** mà artifact **404**? Mỗi ca đó nằm ở ô nào của bảng hai thuộc tính hỏng?

**BT3 — Chi phí của `policy` mặc định.** Trên pipeline lab, đổi cả bốn job về `policy: pull-push` rồi đo lại tổng thời gian; sau đó đổi ba job tiêu thụ sang `policy: pull` và đo lại.
*Câu hỏi phải trả lời:* chênh lệch bao nhiêu giây, và nó có khớp con số **3 × 61 = 183 giây** của QT 6.2 không? Nếu lệch quá 20% thì phần cố định nào trên máy bạn khác với máy tham chiếu?

**BT4 — `fallback_keys` đáng bao nhiêu.** Thêm `cache:fallback_keys` cho job bước 4, rồi đổi lockfile để khoá chính đổi.
*Câu hỏi phải trả lời:* lần chạy sau khi đổi khoá tiết kiệm được bao nhiêu giây so với trượt hoàn toàn? Và vì sao `fallback_keys` **không** sửa được ca cache nằm ở runner khác (QT 6.4)?

**BT5 — Ca `dependencies` trỏ job vắng mặt.** Dùng `rules` làm job nguồn biến mất (buổi 04 QT 6.2), rồi khai `dependencies` trỏ tới nó. Đo: pipeline có được tạo không, job sau nhận bao nhiêu tệp.
*Câu hỏi phải trả lời:* kết quả **đo được** trên GitLab 17.7 là gì, và nó khác `needs` trỏ job vắng mặt (buổi 04 QT 7.3) ở chỗ nào?

**BT6 — Hoá đơn dung lượng thật.** Với một project thật, đọc `statistics.job_artifacts_size`, rồi đặt `expire_in: 1 hour` cho mọi hiện vật trung gian và đọc lại sau 48 giờ.
*Câu hỏi phải trả lời:* giảm bao nhiêu MB, và tuỳ chọn *keep latest artifacts* có đang giữ lại phần nào không?

**BT7 — Ba con số cho buổi 14.** Dùng `doc-pha.sh` cho **mọi** job của một pipeline thật, cộng ba pha `Restoring cache`, `Downloading artifacts`, `Creating cache` trên toàn pipeline.
*Câu hỏi phải trả lời:* ba pha đó chiếm bao nhiêu phần trăm tổng thời gian pipeline? Đây chính là ngân sách mà buổi 14 sẽ đi rút, nên hãy lưu con số lại.

**BT8 — Cache của một ngôn ngữ khác.** Chọn Java (`~/.m2/repository`) hoặc Go (`GOMODCACHE`), đo bốn con số của QT 6.3 cho nó.
*Câu hỏi phải trả lời:* tỉ lệ giữa **tạo lại** và **giải nén** của ngôn ngữ đó khác Node ở đâu, và điều đó đổi kết luận về `policy` như thế nào? Buổi 17 và buổi 19 sẽ đối chiếu với con số bạn đo hôm nay.

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| # | Hiện vật | Điểm | Tiêu chí đạt điểm tối đa |
|---|---|---|---|
| 1 | `bang-do-cache.tsv` **(cốt lõi)** | 25 | Bốn dòng dữ liệu đủ 8 cột; mọi ô giây > 0; cột hoà vốn khớp phép chia làm tròn lên; có dòng ghi máy đã đo và phiên bản GitLab/runner |
| 2 | `doc-pha.sh` **(cốt lõi)** | 20 | Không lỗi cú pháp; đọc mốc `section_start`/`section_end` từ `trace` **thô**; nhận `PID` và `JOB_ID` làm tham số; có ít nhất hai định dạng đầu ra |
| 3 | `hop-dong-rong.md` | 15 | Ghi hỏng im lặng số 1 và số 3 kèm **hai** bằng chứng API cho mỗi ca (`status` và mã HTTP), và ghi rõ ô của bảng hai thuộc tính |
| 4 | `bang-artifact.tsv` | 10 | Bốn ca thu hẹp (mặc định · `dependencies: []` · `dependencies: [x]` · `needs`) kèm số tệp thật nhận được |
| 5 | `bang-khoa-cache.tsv` | 10 | Bốn kiểu khoá × ba lần chạy, khoá lấy từ `trace` chứ không suy từ YAML |
| 6 | `bang-phan-loai.md` | 10 | Bảng mười thư mục có cột "câu hỏi số mấy quyết định"; kết quả đo thứ tự phục hồi; hai con số dung lượng 27 GB và 90 MB |
| 7 | `checkpoint.log` | 5 | Đủ **12** dòng `ĐẠT`, theo thứ tự |
| 8 | `.gitlab-ci.yml` bản cuối | 5 | Có `workflow` chuẩn buổi 04; mọi job sinh hiện vật đều có một dòng khẳng định |
| | **Tổng** | **100** | |

**Điểm trừ — dẫn chiếu bảng Bẫy hay gặp ở §9 tệp lý thuyết:**

| Lỗi | Trừ | Bẫy số |
|---|---|---|
| Bảng đo lấy số từ đề cương hoặc từ tệp lý thuyết thay vì tự đo | **−25** (mất trọn hiện vật cốt lõi) | 11 |
| `doc-pha.sh` đọc thời lượng bằng cách trừ dấu thời gian đầu dòng thay vì mốc `section_*` | −10 | 11 |
| Kết luận "artifact thắng cache" mà không có số dòng của hai pha | −8 | 14 |
| Kết luận về `cache:key` mà không lấy khoá từ `trace` | −8 | 2 |
| Ca artifact rỗng chỉ có **một** khẳng định | −6 | 6 |
| Không có dòng khẳng định trong job sinh hiện vật | −6 | 7 |
| Bảng phân loại đặt `node_modules` vào `artifacts` | −5 | 13 |
| Không ghi máy đã đo và phiên bản runner | −5 | — |
| Đã làm phần tuỳ chọn mà không khôi phục `config.toml` | **−15** | — |
| Nộp thiếu một trong hai hiện vật cốt lõi | **chưa nộp bài** | — |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| L1 | Điều kiện tiên quyết (làm trước giờ, không tính vào 150') | — |
| L2 | Kiến trúc bài lab (đọc trước giờ) | — |
| L3 | Bước 1 — Artifact là hợp đồng: mặc định tải bao nhiêu, thu hẹp bằng gì | 30' |
| L4 | Bước 2 — Hợp đồng rỗng: artifact 0 byte mà job xanh, và cách chặn | 30' |
| L5 | Bước 3 — `cache:key` tính lúc nào, và trượt cache im lặng ra sao | 30' |
| L6 | Bước 4 — Sổ thu chi của cache: bốn kích thước, điểm hoà vốn | 35' |
| L7 | Bước 5 — Bảng phân loại, thứ tự phục hồi, `expire_in` | 15' |
| L8 | Nộp sản phẩm và dọn dẹp | 10' |
| L9–L11 | Xử lý sự cố · bài tập mở rộng · tiêu chí chấm (tra cứu, ngoài giờ) | — |
| **Tổng** | | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---



**Quy tắc cho giảng viên:**

- Chọn **5–7 câu** trong 12, ưu tiên câu 🔥. Trả lời **bằng miệng, không nhìn tài liệu**. **Gọi ngẫu nhiên**; ai thiếu thì gọi người kế tiếp bổ sung, giảng viên không trả lời thay.
- Bốn câu chen vào đã thành phản xạ của khoá: **"bao nhiêu?"** (buổi 01), **"sửa ở tệp nào?"** (buổi 02), **"đi qua đường nào trong bốn đường?"** (buổi 03), **"quyết định ở `t0` hay sau `t0`?"** (buổi 04).
- Buổi này thêm câu thứ năm, và nó theo học viên suốt giai đoạn 3: **"cái đó ai giữ — server hay runner?"** Trả lời được câu ấy là trả lời được luôn chuyện có đảm bảo hay không, có API đọc hay không.
- Câu **7** và câu **8** là câu **tính toán**. Giảng viên buộc thí sinh nói ra một con số. "Tuỳ repo" mà không kèm phép tính nào thì tối đa **1 điểm**, dù phần cơ chế đúng. Cho phép hỏi lại các số đầu vào — nhớ số không phải mục tiêu, biết chia là mục tiêu.

**Thang điểm mỗi câu:**

| Điểm | Nghĩa |
|---|---|
| 0 | Không trả lời được, hoặc sai cơ chế |
| 1 | Nhắc được tên khái niệm, không nêu cơ chế |
| 2 | Nêu đúng cơ chế |
| 3 | Đúng cơ chế **và** một con số, hoặc **và** một ca nó không đúng |

**Hai lỗi làm trần điểm cả buổi là 1:**

1. **Nói cache được đảm bảo tồn tại, hoặc nói runner báo lỗi khi trượt cache.** Hiểu sai luận đề cả buổi. Người tin điều này sẽ dùng cache để truyền `node_modules` giữa hai job và sinh ra loại lỗi tốn nhiều giờ điều tra nhất: chạy tốt 9 lần, hỏng lần thứ 10, không ai đổi gì.
2. **Nói job upload artifact rỗng thì job đỏ.** Đây là chế độ hỏng im lặng số một của cả giai đoạn 1. Người tin job sẽ đỏ thì không bao giờ viết một dòng khẳng định nào.

**Bốn câu phân loại thật:**

| Câu | Phân loại điều gì |
|---|---|
| 2 | Người **phân biệt `t0` với thời điểm job bắt đầu**. Người học thuộc sẽ nói `cache:key` tính ở `t0` cho giống `rules` buổi 04 — và sai. Người hiểu cơ chế tự lập luận: muốn hash lockfile thì phải checkout xong, mà checkout xảy ra trên runner |
| 3 | Người **đã từng bị hỏng im lặng cắn**. Chưa bị thì đáp "thì job đỏ chứ sao"; đã bị thì kể ngay cách phát hiện: kích thước artifact, hoặc mã HTTP `404` |
| 7 | Người **dám tính ra số**. Câu này đo thái độ hơn đo kiến thức. Trả lời "tuỳ workload" rồi dừng là người chưa mở `trace` đọc giây từng pha lần nào |
| 12 | **Tư duy hệ thống.** Không có đáp án duy nhất; nó đo cách thu hẹp vùng nghi ngờ, và đo luôn học viên có ghép được buổi 01, buổi 04 với buổi 05 hay không |

---

## V2. Bộ câu hỏi

### Câu 1 — 🔥

**Hỏi:** `artifacts` và `cache` khác nhau ở đâu? Trả lời bằng **cơ chế**, đừng trả lời bằng định nghĩa.

**Đáp án chuẩn:** Khác ở **ai giữ**; mọi khác biệt còn lại là hệ quả. Có **2** kho, chỉ **1** trong 2 có API đọc.

`artifacts` đi **lên server GitLab**: cuối job runner nén và upload; GitLab ghi một bản ghi vào cơ sở dữ liệu, cấp URL tải, gắn `expire_in`, cộng số byte vào dung lượng project. Vì có bản ghi nên có API — `GET /projects/:id/jobs/:job_id/artifacts` trả `200` kèm nội dung hoặc `404`. Tức artifact **kiểm chứng được từ ngoài job**.

`cache` **không đi đâu cả**: cuối job runner nén thư mục đã khai thành một tệp và để lại **trên đĩa của chính runner vừa chạy job** (hoặc object storage nếu người vận hành đã cấu hình distributed cache). Không ai ghi sổ, không endpoint nào để hỏi "cache của khoá X còn không", và khi thiếu thì runner ghi **một dòng thông báo** rồi chạy tiếp — **0** dòng lỗi.

Nói gọn để đạt 3 điểm: **`artifacts` là hợp đồng, `cache` là tối ưu.** Câu hỏi để chọn chỉ có một: *"job sau **sai** nếu thiếu nó, hay chỉ **chậm** hơn?"*

**Tiêu chí chấm:**
- 0đ: "Giống nhau, chỉ khác cách dùng." Hoặc nói cache được đảm bảo. **Trần điểm cả buổi là 1.**
- 1đ: Nói được cache để tăng tốc, artifact để truyền tệp, không nêu được ai giữ.
- 2đ: Nêu đúng **hai chủ giữ** — server và runner — và suy ra khác biệt về đảm bảo.
- 3đ: Như trên, **và** nêu chỉ artifact có API đọc nên chỉ nó kiểm chứng được từ ngoài, **và** đưa được câu hỏi chọn "sai hay chỉ chậm".

**Câu hỏi đào sâu:** Bật distributed cache thì cache có thành hợp đồng chưa? *(Chưa. Nó chỉ chuyển cache từ đĩa một runner sang kho dùng chung, tức tăng tỉ lệ trúng. Vẫn không có bản ghi trong cơ sở dữ liệu GitLab, không có API đọc, runner vẫn không báo lỗi khi thiếu. Đổi tỉ lệ trúng không đổi loại đảm bảo.)*

---

### Câu 2 — ★★★

**Hỏi:** `cache:key` được tính lúc nào? Vì sao nó **không thể** được tính ở `t0` như `rules`?

**Đáp án chuẩn:** Tính **lúc job bắt đầu, trên runner** — sau `t0`.

Lập luận bắt buộc: dạng khoá mạnh nhất là `cache:key:files`, khoá là **hash nội dung** các tệp được liệt kê. Muốn hash nội dung thì phải **có tệp trong tay**; tệp nằm trong repo, repo chỉ có mặt sau pha clone, mà clone xảy ra trên runner ở đầu job. Vậy việc tính khoá **bắt buộc** xảy ra sau `t0` — không có cách nào đưa nó về `t0` mà vẫn giữ ngữ nghĩa "khoá theo nội dung lockfile". Đây là **điểm đối lập tường minh** với buổi 04 QT 4.1: danh sách job chốt ở `t0` và không gì đổi được, còn `cache:key` được giải quyết muộn hơn nhiều, ở mỗi job, trên máy đã checkout xong.

```yaml
key: $CI_COMMIT_SHA          # SAI — mỗi commit một khoá mới, trúng 0% VĨNH VIỄN, log không có chữ "lỗi"
key: { files: [package-lock.json] }   # ĐÚNG — khoá đổi chậm hơn commit
```

Con số để đạt 3 điểm: ở GitLab 17.7, `cache:key:files` nhận **tối đa 2** tệp và `cache:fallback_keys` nhận **tối đa 5** khoá. Đó là giới hạn của phiên bản, không phải quy luật tự nhiên — monorepo 6 lockfile phải tự ghép khoá bằng biến, và đó là buổi 22.

**Tiêu chí chấm:**
- 0đ: "Ở `t0`, giống `rules`."
- 1đ: Biết là lúc job chạy, không giải thích được vì sao không thể sớm hơn.
- 2đ: Nêu đúng lập luận **phải checkout xong mới hash được tệp**, nên tính khoá nằm sau `t0`.
- 3đ: Như trên, **và** nêu ca `$CI_COMMIT_SHA` cho tỉ lệ trúng **0%** mà không có dòng lỗi nào, **và** nêu một trong hai giới hạn (2 tệp `files`, 5 khoá `fallback_keys`).

**Câu hỏi đào sâu:** `cache:fallback_keys` cứu được việc lockfile vừa đổi không? *(Một phần: khoá chính trượt thì runner thử lần lượt tối đa 5 khoá dự phòng, nên ta lấy được cache của lockfile **cũ** và chỉ tải phần chênh lệch. Nhưng nó **không** sửa việc cache đang nằm trên đĩa một runner khác — chuyện đó là QT 6.4, fallback không chạm tới.)*

---

### Câu 3 — 🔥

**Hỏi:** Job build của bạn xanh, nhưng artifact tải về **rỗng**. Vì sao job không đỏ, và bạn chặn bằng gì?

**Đáp án chuẩn:** Vì upload artifact là **một bước riêng chạy sau `script`**, và kết quả bước ấy **không** được cộng vào mã thoát của job. `artifacts:paths` trỏ vào mẫu không khớp tệp nào thì runner ghi một dòng cảnh báo kiểu `no matching files`, đóng gói một gói rỗng, job kết thúc với mã thoát 0. Ô **im lặng, không chặn** của bảng hai thuộc tính (buổi 01 QT 7.1) — ô nguy hiểm nhất, vì không có tín hiệu và cũng không có gì bị chặn để buộc ai đó nhìn vào.

Đo từ ngoài phải bằng **hai** khẳng định độc lập: `status == "success"` **và** `GET /jobs/:id/artifacts` trả **404**. Một mình `404` có thể do token thiếu quyền; một mình `success` không nói gì về artifact. Chỉ **cặp** ấy là bằng chứng.

Đường thoát duy nhất là một khẳng định trong `script` (buổi 01 QT 7.3 — lần thứ **3** nguyên lý này xuất hiện):

```yaml
script:
  - npm run build
  - test -s dist/app.js || { echo "KHANG DINH HONG: dist/app.js rỗng"; exit 1; }
```

Con số để đạt 3 điểm: **1** dòng khẳng định đổi ô của bảng hai thuộc tính từ *im lặng, không chặn* sang *ồn ào, có chặn*, và tốn khoảng **0,1 giây** — rẻ nhất cả khoá. Nhưng nói rõ giới hạn: khẳng định trả lời *"hiện vật có tồn tại và có kích thước hợp lý không"*, **không** trả lời *"hiện vật có đúng không"*.

**Tiêu chí chấm:**
- 0đ: "Job phải đỏ chứ." **Trần điểm cả buổi là 1.**
- 1đ: Biết job vẫn xanh, không giải thích được vì sao.
- 2đ: Nêu đúng cơ chế **upload là bước riêng sau `script`, không vào mã thoát**, và đề xuất được khẳng định.
- 3đ: Như trên, **và** nêu **cặp** khẳng định `success` + `404` như cách đo từ ngoài, **và** gọi đúng ô của bảng hai thuộc tính kèm chi phí 0,1 giây.

**Câu hỏi đào sâu:** Có cách nào làm bước upload thất bại thì job đỏ, không cần viết khẳng định? *(Có vài cấu hình phía runner ảnh hưởng tới hành vi này, nhưng **đừng** dựa vào chúng: hành vi phụ thuộc phiên bản, tức loại (c) — phải đo. Một dòng `test -s` thì không phụ thuộc phiên bản nào và đọc được ngay trong tệp YAML.)*

---

### Câu 4 — ★★★

**Hỏi:** Một job **không khai** `dependencies` và **không khai** `needs`. Nó tải artifact của những job nào?

**Đáp án chuẩn:** Của **mọi job ở mọi stage trước nó** — không phải chỉ stage liền trước. Đây là mặc định, và là mặc định **tốn tiền**.

Cơ chế: khi dựng pipeline, GitLab gắn cho mỗi job một danh sách nguồn artifact mặc định gồm toàn bộ job thuộc các stage có thứ tự nhỏ hơn. Đầu job, runner tải lần lượt từng gói và giải nén vào thư mục dự án. Số byte tải về tăng theo **tổng** artifact của các stage trước, không theo thứ job này cần.

Con số: **2** job nguồn, mỗi job để lại **45 MB** — job ở stage sau tải về **90 MB** mà trong YAML của nó **không có một dòng nào** nói tới artifact. Với 6 job ở stage sau, đó là 540 MB qua mạng và khoảng **36 giây** thời gian máy mỗi lần chạy để tải thứ phần lớn không dùng. Dấu hiệu trong `trace`: pha `Downloading artifacts` dài vài chục giây trong một job mà `script` chỉ đọc đúng một tệp 2 kB. Đếm chính xác bằng `grep -c 'Downloading artifacts for'` trên `trace` — số dòng đó là số job nguồn đang tải; so với số job mà `script` thật sự cần là ra ngay số job nên thu hẹp.

Điểm để đạt 3 điểm: đây là **thời gian máy**, không nhất thiết là **thời gian đồng hồ** (buổi 01 đã đặt ra phân biệt này). Job chạy song song trên đủ slot runner thì thời gian đồng hồ giảm ít; cái tiết kiệm được là băng thông và slot runner cho việc khác.

**Tiêu chí chấm:**
- 0đ: "Không khai gì thì không tải gì."
- 1đ: "Tải của stage liền trước."
- 2đ: Nêu đúng **mọi job ở mọi stage trước**, và biết cách đếm bằng `trace` hoặc bằng số tệp nhận được.
- 3đ: Như trên, **và** quy ra con số cụ thể (2 × 45 MB = 90 MB, hoặc số của repo mình), **và** phân biệt thời gian máy với thời gian đồng hồ.

**Câu hỏi đào sâu:** Job **cùng** stage với job nguồn có tải artifact của nó không? *(Không — mặc định chỉ lấy của các stage **trước**. Muốn lấy của job cùng stage thì phải dùng `needs`, và khi đó `needs` đổi luôn thứ tự chạy: job này không chờ hết stage trước mà chờ đúng job kia. Buổi 08 mổ phần đồ thị.)*

---

### Câu 5 — ★★★

**Hỏi:** `dependencies: []`, `dependencies: [build-a]`, và `needs: [{job: build-a, artifacts: false}]` — ba cách này khác nhau ra sao?

**Đáp án chuẩn:** **3** cách, khác nhau ở chỗ có đổi **thứ tự chạy** hay không.

| Cách viết | Tải artifact của ai | Đổi thứ tự chạy | Số byte tải |
|---|---|---|---|
| Không khai gì | Mọi job mọi stage trước | Không | Tổng của các stage trước |
| `dependencies: []` | **Không ai** | **Không** | Đúng **0 byte** |
| `dependencies: [build-a]` | Chỉ `build-a` | **Không** — vẫn chờ hết stage trước | Chỉ của `build-a` |
| `needs: [{job: build-a, artifacts: false}]` | **Không ai** | **Có** — chỉ chờ `build-a` | 0 byte |

Câu phân biệt gốc rễ: **`dependencies` chỉ nói *tải của ai*; `needs` nói *chạy sau ai* **và** *tải của ai*.** Nên `dependencies` không bao giờ làm pipeline nhanh hơn về thời gian đồng hồ — nó chỉ bỏ việc tải; còn `needs` phá luôn ranh giới stage. Dấu hiệu thí sinh đang nhầm hai thứ: "tôi thêm `dependencies` mà job vẫn chờ cả stage". Đúng, nó phải chờ.

`needs:artifacts: false` dùng khi cần **quan hệ thứ tự** nhưng không cần tệp: `deploy` phải chạy sau `phe-duyet` mà chẳng cần tệp nào của nó. Cạm bẫy của `dependencies: []`: nó tắt về 0 byte kể cả tệp job **vẫn đang âm thầm dùng** nhờ mặc định ở câu 4 — kiểm rẻ nhất trước khi tắt là đọc `trace` lần chạy gần nhất, liệt kê các dòng `Downloading artifacts for ...` rồi đối chiếu với `script`. Tắt nhầm cho một job đỏ ở lần chạy sau, và người sửa thường không phải người tắt.

**Tiêu chí chấm:**
- 0đ: "Ba cái giống nhau, viết cách nào cũng được."
- 1đ: Biết cả ba đều liên quan việc thu hẹp artifact.
- 2đ: Nêu đúng trục phân biệt — `dependencies` **không** đổi thứ tự, `needs` **có** — và biết `dependencies: []` cho **0 byte**.
- 3đ: Như trên, **và** đưa được một ca dùng `needs:artifacts: false` cho đúng chỗ, **và** nêu cách kiểm bằng `trace` trước khi tắt.

**Câu hỏi đào sâu:** Job có **cả** `needs` và `dependencies` thì cái nào thắng? *(`dependencies` phải là **tập con** các job trong `needs`; khai ngoài tập đó thì pipeline không tạo được — ô ồn ào có chặn, phát hiện trong vài giây. Thực tế đừng khai cả hai: chọn `needs` và dùng cờ `artifacts` của chính nó, để chỉ có một nơi phải đọc khi điều tra.)*

---

### Câu 6 — ★★★

**Hỏi:** Job test của bạn **đỏ**. Bạn mở ra đọc báo cáo test xem test nào hỏng — và không có báo cáo nào. Vì sao?

**Đáp án chuẩn:** Vì mặc định của `artifacts:when` là **`on_success`**. Job đỏ thì bước upload không chạy, nên đúng thứ ta cần nhất — báo cáo của một job đã hỏng — lại là thứ mặc định không cho ta lấy. `when` có **3** giá trị: `on_success` (mặc định), `on_failure`, `always`. Với mọi thứ cần đọc lúc job **đỏ** — báo cáo test, báo cáo scan, log gỡ rối — phải khai **tường minh** `when: always`, kèm `expire_in: 7 days` để không phình dung lượng.

Cách đo, không tra tài liệu: hai job cùng `exit 1`, một job khai `when: always`, so mã HTTP khi tải artifact — **200** so với **404**.

Phần phải nói để đạt 3 điểm, và đây là đại lượng loại (c) **phải đo**: hành vi của `artifacts:reports` **không giống** hành vi của `artifacts:paths`, và nó khác nhau theo **từng loại report** cùng **từng phiên bản** — một số loại vẫn được thu về khi job đỏ, vì nếu không thì tính năng hiển thị test thất bại trong merge request sẽ vô nghĩa. Vậy kết luận đúng không phải "reports luôn được upload" mà là: **đo trên phiên bản mình đang chạy, rồi khai `when: always` tường minh cho khỏi phải nhớ.** Bài lab đo trên GitLab CE 17.7, runner 17.7, executor `docker`. Phần report hỏi một endpoint khác: `GET /projects/:id/pipelines/:id/test_report`.

Ô của bảng hai thuộc tính: **im lặng, không chặn thêm** — nó lẫn vào một job đã đỏ nên không ai coi là lỗi riêng; cái giá thật là một vòng chạy lại 6 phút với `CI_DEBUG_TRACE` chỉ để biết test nào hỏng.

**Tiêu chí chấm:**
- 0đ: "Chắc job chưa kịp sinh báo cáo."
- 1đ: Biết liên quan `artifacts:when`, không nêu được mặc định là gì.
- 2đ: Nêu đúng mặc định `on_success`, 3 giá trị của `when`, và cách sửa bằng `when: always`.
- 3đ: Như trên, **và** nói rõ hành vi của `artifacts:reports` là thứ **phải đo** chứ không tra, kèm cách đo, **và** gọi đúng ô của bảng hai thuộc tính.

**Câu hỏi đào sâu:** `when: always` có làm dung lượng project tăng không? *(Có — giờ ta giữ cả artifact của những lần chạy đỏ, mà lần đỏ nhiều hơn ta tưởng. Xử lý bằng `expire_in` ngắn đi kèm: log gỡ rối `7 days` là quá đủ để điều tra một sự cố, chỉ hiện vật phát hành mới cần `30 days`. Chi tiết ở QT 5.5.)*

---

### Câu 7 — ★★★

**Hỏi:** Đội bạn có cache `node_modules` nặng **380 MB**. Một người nói "to thế thì cache làm gì, nén với tải còn lâu hơn cài lại". Bạn trả lời bằng số.

**Đáp án chuẩn:** Cache là một khoản đầu tư và nó có **sổ thu chi**. Ba con số phải đo bằng cách đọc giây từng pha trong `trace`: tạo lại từ đầu (`npm ci`) **95 s**; nén + tải lên (`Creating cache`) **61 s**; tải + giải nén (`Restoring cache`) **44 s**. Suy ra lãi mỗi lần **trúng** là 95 − 44 = **+51 s**, lỗ mỗi lần **trượt** là **−61 s** (vẫn phải ghi cache mà không được lợi gì). Điểm hoà vốn là một phép chia:

```
số lần trúng để hoà vốn = nén_và_tải / (tạo_lại − giải_nén) = 61 / 51 = 1,196 → làm tròn lên = 2
```

Vậy câu trả lời: **cache 380 MB hoà vốn sau 2 lần trúng.** Với repo chạy 20 pipeline mỗi ngày, 2 lần trúng là chuyện của buổi sáng. Đây đúng là chỗ **định lượng ngược lại**: cái mà ai cũng bảo "to quá không đáng" thì hoà vốn nhanh gần như cache nhỏ nhất.

| Cache | Tạo lại | Nén + tải | Tải + giải nén | Lãi/lần trúng | Lần trúng để hoà vốn |
|---|---|---|---|---|---|
| 12 MB | 8 s | 3 s | 2 s | +6 s | **1** |
| 45 MB | 22 s | 9 s | 6 s | +16 s | **1** |
| 160 MB | 58 s | 26 s | 18 s | +40 s | **1** |
| 380 MB | 95 s | 61 s | 44 s | +51 s | **2** |

Kết luận đọc được từ bảng, và đây là phần giá trị nhất: **cái làm cache lỗ hầu như luôn là khoá sai, không phải kích thước lớn.** Kích thước lớn làm **cả hai vế** lớn lên gần cùng tỉ lệ — cột "tạo lại" và cột "nén + tải" cùng tăng nên tỉ số giữa chúng gần như không đổi. Còn khoá sai đưa tỉ lệ trúng về **0** và **giữ nguyên** chi phí ghi: cùng cache 380 MB, nếu khoá đổi mỗi commit và để `policy: pull-push` ở cả 4 job thì nó lỗ **61 × 4 = 244 giây mỗi pipeline, mãi mãi** — không có lần trúng nào để hoà vốn.

Giới hạn phải nêu để đạt 3 điểm: bốn dòng này đo trên executor `docker`, đĩa SSD, 8 vCPU. Runner `kubernetes` với volume mạng cho số khác hẳn — **thứ tự lớn nhỏ giữa các dòng giữ nguyên, tỉ lệ thì không**. Đây là loại (c): con số để biết cách tính, không phải con số để chép vào tài liệu của đội mình.

**Tiêu chí chấm:**
- 0đ: "Tuỳ workload thôi." Hoặc đồng ý luôn rằng cache to thì không đáng.
- 1đ: Biết phải so thời gian tạo lại với thời gian nén và tải, nhưng không đưa ra được con số hay phép tính nào.
- 2đ: Viết đúng phép chia `nén_và_tải / (tạo_lại − giải_nén)` và tính ra **2** lần trúng, hoặc tính đúng trên số của repo mình.
- 3đ: Như trên, **và** nêu kết luận "cái làm cache lỗ là khoá, không phải kích thước" kèm lập luận hai vế cùng tăng, **và** nêu giới hạn của bảng đo.

**Câu hỏi đào sâu:** Bất đẳng thức `p × (tạo_lại − giải_nén) > nén_và_tải` với `p = 1` cho `51 > 61` là **sai** — vậy cache 380 MB lỗ à? *(Hai cách đọc, phân biệt được chúng mới là hiểu. Bất đẳng thức là góc nhìn **mỗi lần chạy đều ghi lại cache** — tức `policy: pull-push` khắp nơi; đọc thế thì đúng là nó không bao giờ có lãi. Phép chia `61/51 = 2` là góc nhìn **chi phí ghi trả một lần cho mỗi khoá**: chỉ ghi khi lockfile đổi, các job tiêu thụ khai `policy: pull`. Cái quyết định ta ở kết luận nào chính là `policy` — đó là câu 8.)*

---

### Câu 8 — ★★

**Hỏi:** `cache:policy: pull` tiết kiệm cái gì? Bao nhiêu giây?

**Đáp án chuẩn:** `policy` tách **quyền đọc** khỏi **quyền ghi**. Mặc định là `pull-push`: đầu job phục hồi cache, **cuối job nén lại toàn bộ thư mục cache và ghi lên** — dù `script` không đổi một byte nào trong đó. `policy: pull` bỏ hẳn phần ghi. Với cache 380 MB của câu 7 (pha `Creating cache` mất **61 giây**):

```
3 job test × 61 s = 183 giây tiết kiệm mỗi pipeline
```

Cấu hình đúng: job nào **tạo ra** nội dung cache thì giữ `pull-push` (thường chỉ job `build`); job nào chỉ **tiêu thụ** thì `pull`.

Lợi ích thứ hai, ít ai nói mà quan trọng hơn: ba job test song song với `pull-push` **ghi đè lên nhau cùng một khoá**. Job nào kết thúc sau cùng thì bản của nó thắng, mà ta không kiểm soát được job nào kết thúc sau cùng — nghĩa là cache của khoá đó có nội dung khác nhau giữa hai lần chạy pipeline giống hệt nhau. `policy: pull` xoá luôn lớp lỗi này vì chỉ còn **1** job có quyền ghi. Dấu hiệu trong `trace`: dòng `Creating cache` dài 40–60 giây ở cuối những job mà `script` không cài đặt gì cả.

Điểm để đạt 3 điểm — nói được cả bức tranh chi phí: cùng cache 380 MB, để `pull-push` ở cả 4 job và khoá đổi mỗi commit thì tốn **244 s mỗi pipeline** không đổi lại được gì; chuyển sang khoá theo lockfile cộng `policy: pull` ở 3 job test thì thành **tiết kiệm 204 s** mỗi pipeline (4 job × 51 s lãi mỗi lần trúng). Khoảng cách giữa hai cấu hình là gần **450 giây một lần chạy** cho đúng một repo — và cả hai cấu hình đều **xanh** như nhau.

**Tiêu chí chấm:**
- 0đ: Không biết `policy` là gì.
- 1đ: Biết `pull` là chỉ đọc, không nêu được nó bỏ pha nào và tiết kiệm bao nhiêu.
- 2đ: Nêu đúng nó bỏ pha `Creating cache` và tính được **3 × 61 = 183 giây** mỗi pipeline.
- 3đ: Như trên, **và** nêu lợi ích thứ hai là bỏ chuyện các job song song ghi đè nhau cùng một khoá, **và** đưa con số so sánh hai cấu hình (244 s tốn so với 204 s tiết kiệm).

**Câu hỏi đào sâu:** Có `policy: push` không, dùng khi nào? *(Có — chỉ ghi, không đọc. Dùng cho job có nhiệm vụ **làm mới cache** sạch sẽ, ví dụ một job theo lịch ban đêm cài phụ thuộc từ đầu rồi đẩy cache lên cho cả ngày sau; nó bỏ pha phục hồi nên không kế thừa rác của bản cũ. Phải cẩn thận: chạy nó lúc đang chuẩn bị phát hành thì mọi job trong pipeline kế tiếp trượt cache một lần.)*

---

### Câu 9 — ★★★

**Hỏi:** Cùng một commit, không ai đổi gì. Chạy lại pipeline nhiều lần thì có lần cache trúng, có lần trượt, không theo quy luật nào. Chẩn đoán.

**Đáp án chuẩn:** Nghi phạm số một: **job đang nhảy giữa nhiều runner, và cache nằm trên đĩa của runner đã tạo ra nó.** Không có distributed cache thì cache là một tệp nén trên đĩa local; job rơi vào runner A thì trúng, rơi vào runner B thì trượt. Với `N` runner và job được chia tương đối đều, tỉ lệ trúng trần ở khoảng **1/N**; với 2 runner và 6 lần chạy ta đo được khoảng **3/6**.

Sự **không theo quy luật nào** chính là bằng chứng phân biệt nguyên nhân này với các nguyên nhân khác:

| Dấu hiệu | Nguyên nhân |
|---|---|
| Trúng/trượt **ngẫu nhiên** với cùng commit | Nhiều runner, không có cache dùng chung |
| Trượt **mọi lần**, đều đặn | Khoá đổi mỗi commit (QT 4.2) |
| Trúng đến một ngày rồi trượt hẳn từ đó | Cache đã bị dọn, lockfile vừa đổi, hoặc đĩa runner đầy |
| Trúng ở job này, trượt ở job kia trong **cùng** pipeline | Hai job khai `cache:key` khác nhau, hoặc chạy trên hai runner khác nhau |

Cách kiểm bằng số: chạy 6 pipeline, với mỗi job ghi `runner.id` (`GET /jobs/:id`, trường `.runner.id`) **cùng với** số dòng `successfully extracted cache` trong `trace`. Cột `runner` đổi và cột trúng đổi theo nó thì chẩn đoán xong — đây là phép đo **phân biệt được nguyên nhân**, không chỉ khẳng định có vấn đề.

Ba cách sửa và giới hạn từng cách: bật **distributed cache** (MinIO, S3) đưa tỉ lệ trúng lên khoảng **5/6** — lần đầu vẫn luôn trượt, và cache vẫn không thành hợp đồng; `cache:fallback_keys` (tối đa 5 khoá) chỉ giảm thiệt hại khi **khoá** đổi, **không** sửa việc cache nằm ở máy khác; gắn `tags` để job luôn về một runner cho trúng gần 100% nhưng mất chạy song song và mất chịu lỗi khi runner đó chết.

Điểm để đạt 3 điểm: nói rõ "trần ở 1/N" **không phổ quát** — nó chỉ đúng khi không có distributed cache **và** job được chia tương đối đều. Runner có `concurrent` khác nhau, hoặc có runner đang `paused`, thì phân bố lệch và con số lệch theo.

**Tiêu chí chấm:**
- 0đ: "Chắc GitLab lag." Hoặc đề nghị chạy lại xem sao.
- 1đ: Đoán được là do cache, không nêu được vì sao ngẫu nhiên.
- 2đ: Nêu đúng cơ chế **cache nằm trên đĩa runner, job nhảy runner**, và biết trần ở khoảng `1/N`.
- 3đ: Như trên, **và** nêu phép đo ghép `runner.id` với dòng trúng cache, **và** phân biệt cái `fallback_keys` sửa được với cái nó không sửa được.

**Câu hỏi đào sâu:** Vì sao ngay cả với distributed cache, lần đầu vẫn luôn trượt? *(Vì khoá mới thì chưa có gì ở khoá đó — không kho nào tạo dữ liệu từ không khí. Con số 5/6 chính là "1 lần trượt bắt buộc + 5 lần trúng". Đây là lý do đổi `cache:key` trên nhánh chính làm pipeline đầu tiên sau merge chậm hơn đúng bằng thời gian tạo lại — đừng làm việc đó lúc đang chuẩn bị phát hành.)*

---

### Câu 10 — ★★

**Hỏi:** Một đường dẫn được khai trong **cả** `cache:paths` **và** `artifacts:paths`. Ở job sau, cái nào thắng? Vì sao?

**Đáp án chuẩn:** **Artifact thắng**, và lý do nằm ở **thứ tự bốn bước** ở đầu job: **clone → phục hồi cache → tải artifacts → `script`**. Hai bước giữa cùng ghi vào thư mục dự án; bước sau ghi đè bước trước, và tải artifact nằm **sau** phục hồi cache. Vậy nội dung mà `script` nhìn thấy là của **artifact** — trong bài lab, **100%** các lần đo.

Đây là loại (c), phải **đo** chứ không tra, vì kết luận phụ thuộc thứ tự runner thực hiện và thứ tự đó có thể đổi giữa các phiên bản: `grep -nE 'Restoring cache|Downloading artifacts'` trên `trace`, số dòng của `Restoring cache` phải **nhỏ hơn**. Ghi lại phiên bản đã đo — bài lab đo trên runner 17.7, executor `docker`.

Nhưng câu trả lời đúng **không dừng ở "artifact thắng"**. Nó là: **đừng đặt cùng một đường dẫn vào hai kho.** Việc đó tạo ra một lớp lỗi "xanh mà sai" không cần thiết, vì hai kho có hai đảm bảo khác nhau và nội dung của chúng không được đồng bộ bởi cơ chế nào. Ca hay gặp nhất: `dist/` khai ở cả hai. Một hôm job build biến mất vì `rules` không khớp (buổi 04 QT 6.2), hoặc artifact của nó rỗng vì đường dẫn sai (QT 5.3). Job deploy vẫn chạy, vẫn tìm thấy một thư mục `dist/` — bản **cũ còn sót trong cache** — và deploy nó lên. Pipeline xanh, người ta đổi mã nguồn mà bản deploy không đổi, và không ai nghĩ tới cache vì "cache chỉ để chạy nhanh hơn mà". Ô: **im lặng, không chặn** — cái sai xuất hiện ở prod chứ không ở pipeline.

**Tiêu chí chấm:**
- 0đ: "Cache thắng vì nó phục hồi trước." Hoặc "tuỳ, không đoán được."
- 1đ: Đoán đúng artifact thắng, không giải thích được vì sao.
- 2đ: Nêu đúng **thứ tự bốn bước** và suy ra artifact ghi đè cache.
- 3đ: Như trên, **và** nói rõ đây là thứ **phải đo** bằng cách đọc `trace` chứ không tra, **và** kết luận là đừng đặt cùng đường dẫn vào hai kho, kèm ca `dist/` deploy bản cũ.

**Câu hỏi đào sâu:** Nếu job trước **không** upload artifact lần này thì job sau thấy gì? *(Thấy nội dung của cache — vì bước tải artifact không có gì để ghi đè. Đây chính là cơ chế làm ca `dist/` nguy hiểm: nó chỉ hỏng vào **đúng lần** artifact vắng mặt, tức lần ta ít để ý nhất; và vì pipeline vẫn xanh, dấu hiệu duy nhất là kết quả deploy không đổi.)*

---

### Câu 11 — ★★★

**Hỏi:** Cho **năm** thư mục: `dist/` · `node_modules/` · `~/.m2/repository` · `bao-cao/junit.xml` (báo cáo test JUnit) · `sbom.cdx.json` (SBOM sinh bởi Syft). Với mỗi cái, nói nó đi bằng `artifacts` hay `cache`, giải thích bằng **ba câu hỏi phân loại**, và nói rõ ta **dừng ở câu hỏi số mấy**.

**Đáp án chuẩn:** Ba câu hỏi, hỏi **theo đúng thứ tự**, **dừng ở câu đầu tiên trả lời được**: (1) *Job sau **sai** nếu thiếu nó, hay chỉ **chậm** hơn?* → sai thì `artifacts`. (2) *Tái tạo được từ tệp có trong git (lockfile) không?* → được thì `cache`. (3) *Có người **ngoài pipeline** cần đọc nó không?* → cần thì `artifacts`, kể cả khi tái tạo được.

| Thư mục | Kết luận | Dừng ở câu | Lý do |
|---|---|---|---|
| `dist/` | **`artifacts`** | **1** | Job deploy **sai** nếu thiếu — nó deploy bản cũ hoặc deploy rỗng. Hợp đồng, không phải tối ưu. Kèm `expire_in: 1 hour` nếu chỉ là hiện vật trung gian |
| `node_modules/` | **`cache`** | **2** | Câu 1 trả lời "chỉ **chậm** hơn" vì job tự chạy `npm ci` được. Câu 2: tái tạo được từ `package-lock.json`, tệp này **có trong git**. Khoá `key:files: [package-lock.json]` |
| `~/.m2/repository` | **`cache`** | **2** | Y hệt dòng trên: chỉ chậm hơn, tái tạo được từ `pom.xml` trong git. Buổi 17 mổ cách khai `.m2` cho Maven |
| `bao-cao/junit.xml` | **`artifacts`** | **3** | Câu 1: không job nào **sai** nếu thiếu — không ai tiêu thụ nó. Câu 2: tái tạo được, chạy lại test là có. Nhưng câu 3 trả lời **có**: người review merge request và người điều tra sự cố cần đọc. Bắt buộc kèm `when: always` (QT 5.4), vì lúc cần nó nhất là lúc job đỏ |
| `sbom.cdx.json` | **`artifacts`** | **3** | Câu 3 trả lời **có** và mạnh hơn dòng trên: SBOM là hiện vật để chứng minh với người ngoài, phải **kiểm chứng được từ ngoài job** và phải **tái lập được**; cache không đáp ứng cả hai. `expire_in` bằng vòng đời bản phát hành, không phải `1 hour` |

Hai bẫy trong bộ năm thư mục này, và đây là chỗ phân loại thí sinh:

- **`node_modules/`** — người trả lời nhanh nói "job test **cần** nó, thiếu thì test không chạy được, vậy là `artifacts`". Sai: câu 1 hỏi *job sau sai nếu thiếu* trong điều kiện job sau **có** cách tự tạo lại. Nó có: `npm ci`. Vậy thiếu cache chỉ là **chậm**. Cho `node_modules` đi bằng `artifacts` là hoá đơn dung lượng thật — 90 MB × mỗi job × mỗi pipeline.
- **`bao-cao/junit.xml`** — người chỉ dùng hai câu hỏi đầu sẽ xếp nó vào `cache` vì câu 2 trả lời "tái tạo được". Câu hỏi thứ **3** tồn tại chính vì ca này; không có nó thì mọi báo cáo, mọi log gỡ rối, mọi SBOM đều bị xếp sai.

Hai danh sách thuộc lòng để nói thêm: `dist/`, báo cáo test, SBOM **luôn** là `artifacts`; `~/.npm`, `~/.m2`, `.gradle/caches`, `GOMODCACHE` **luôn** là `cache`.

**Tiêu chí chấm:**
- 0đ: Phân loại theo cảm giác, không dùng câu hỏi nào. Hoặc xếp `dist/` vào `cache`.
- 1đ: Đúng 3–4 trong 5 nhưng không nói được dừng ở câu hỏi nào.
- 2đ: Đúng cả 5 **và** chỉ ra đúng câu hỏi mà mỗi dòng dừng lại.
- 3đ: Như trên, **và** giải thích được **cả hai** bẫy (`node_modules` không phải artifact vì `npm ci` tái tạo được; `junit.xml` là artifact nhờ câu hỏi thứ 3 chứ không nhờ hai câu đầu).

**Câu hỏi đào sâu:** `.terraform/` của một job `terraform plan` đi đường nào? *(`.terraform/` chứa provider tải về — chỉ **chậm** hơn nếu thiếu, tái tạo được từ `.terraform.lock.hcl` trong git → `cache`, dừng ở câu 2. Nhưng tệp `tfplan` thì khác hẳn: job `apply` **sai** nếu thiếu, và người phê duyệt ngoài pipeline cần đọc → `artifacts`, dừng ngay ở câu 1. Cùng một job, hai thư mục, hai đường — đó là lý do phải phân loại từng thư mục chứ không phân loại từng job.)*

---

### Câu 12 — 🔥

**Hỏi:** "Pipeline xanh nhưng bản deploy sai." Không ai đổi gì trong `.gitlab-ci.yml`. Dựng cho tôi một quy trình truy nguyên.

**Đáp án chuẩn:** Không có đáp án duy nhất; câu này đo cách thu hẹp vùng nghi ngờ. Đáp án tốt đi theo **năm nhịp**, mỗi nhịp là một phép **đo**.

**Nhịp 1 — đổi câu hỏi.** Pipeline xanh chỉ chứng minh mã thoát bằng 0 (buổi 01 QT 7.2), không chứng minh việc đã làm. Đừng đi tìm dòng `ERROR` — sẽ không có. Đi tìm **hai con số** so với lần chạy tốt gần nhất: **kích thước artifact** và **thời lượng job**. Lấy chúng mất khoảng 30 giây và chúng bắt được phần lớn ca im lặng.

```bash
curl -s -o /dev/null -w 'http=%{http_code} bytes=%{size_download}\n' \
  --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/projects/$PID/jobs/$JOB/artifacts"
```

**Nhịp 2 — hợp đồng có rỗng không?** `http=404` hoặc `bytes` vài trăm trong khi lẽ ra vài MB thì dừng ở đây: artifact rỗng, job xanh (QT 5.3). Nguyên nhân thường là `artifacts:paths` trỏ sai thư mục sau một lần đổi công cụ build; trong `trace` có dòng `no matching files` mà không ai đọc.

**Nhịp 3 — job nguồn có mặt không?** Nếu artifact `404` vì **job build không tồn tại** thì đó là chuyện khác hẳn và thuộc buổi 04: `rules` không khớp nên job **biến mất** khỏi pipeline ở `t0` (buổi 04 QT 6.2). Kiểm bằng cách đếm job trong `pipelines/:id/jobs` — job biến mất **không xuất hiện**, và chính sự vắng mặt đó là bằng chứng. Nếu job deploy có `needs: [{job: build, optional: true}]` thì pipeline vẫn tạo được và deploy vẫn chạy với **0 tệp**.

**Nhịp 4 — job deploy lấy tệp từ kho nào?** Đây là nhịp mà người chưa học buổi này không nghĩ tới: `grep -nE 'Restoring cache|Downloading artifacts'` trên `trace` của job deploy. Nếu `dist/` có trong `cache:paths` **và** trong `artifacts:paths` thì ta đang ở ca QT 7.2 — bốn bước đầu job, artifact ghi đè cache, nhưng khi artifact vắng mặt thì **cache còn sót vẫn ở đó** và deploy đẩy bản cũ lên. Nhớ QT 4.3: trượt cache cho **0** dòng lỗi và **0** thay đổi mã thoát, nên sự có mặt hay vắng mặt của cache không bao giờ tự báo.

**Nhịp 5 — đóng lại vòng, để lần sau ồn ào.** Truy nguyên xong mà không đổi gì thì tuần sau lặp lại. Ba việc, rẻ trước: (1) khẳng định ở job build, `test -s dist/app.js || exit 1` — **0,1 giây**, đổi ô bảng hai thuộc tính sang *ồn ào, có chặn* (buổi 01 QT 7.3); (2) khẳng định ở **đầu** job deploy, cộng một kiểm dấu vết nhận dạng bản build kiểu `grep -q "$CI_COMMIT_SHORT_SHA" dist/app.js` — khẳng định thứ hai này mới bắt được ca "bản cũ trong cache"; (3) bỏ `dist/` khỏi `cache:paths`: một đường dẫn, một kho.

Điều cần nêu để đạt 3 điểm — vấn đề **điều tra được**: nếu pipeline hỏng là của 40 ngày trước thì có thể không còn gì để đọc. `expire_in` mặc định của instance là **30 ngày**, và artifact hết hạn làm việc `retry` một job cũ cùng việc điều tra một pipeline cũ **không còn khả thi** (QT 5.5). Vậy một phần của việc truy nguyên đã quyết từ trước: log gỡ rối `7 days` với `when: always`, hiện vật phát hành `30 days`, hiện vật trung gian về `1 hour` để đổi lấy dung lượng — 20 pipeline/ngày × 45 MB × 30 ngày là **27 GB**, xuống khoảng **90 MB** với `expire_in: 1 hour`.

**Tiêu chí chấm:**
- 0đ: "Chạy lại xem sao." Hoặc đi tìm chữ `ERROR` trong log.
- 1đ: Biết mở log job deploy đọc, không có thứ tự nào.
- 2đ: Có quy trình có thứ tự ít nhất ba nhịp, bắt đầu bằng việc đo kích thước artifact chứ không đọc log.
- 3đ: Đủ năm nhịp, **và** ghép được cả ba buổi — buổi 01 (job xanh không chứng minh gì, khẳng định), buổi 04 (job biến mất ở `t0`, `optional: true`), buổi 05 (artifact rỗng, cache còn sót, thứ tự bốn bước) — **và** nêu được chuyện `expire_in` quyết định việc điều tra có khả thi hay không.

**Câu hỏi đào sâu:** Trong năm nhịp đó, nhịp nào bỏ được nếu chỉ có 2 phút? *(Bỏ nhịp 3 và 4, giữ nhịp 1: hai con số kích thước artifact và thời lượng job lấy trong 30 giây và phân loại được vùng nghi ngờ ngay — `404` hoặc vài trăm byte thì đi về phía hợp đồng rỗng; artifact đúng kích thước mà deploy vẫn sai thì đi về phía cache còn sót. Nhịp 5 không bỏ được — không phải vì nó gấp, mà vì bỏ nó nghĩa là tuần sau làm lại toàn bộ bốn nhịp kia.)*

---

## V3. Câu chốt để nói khi phỏng vấn

> Bốn câu dưới đây viết **nguyên văn, đúng ngữ điệu nói**. Học viên tập nói to từng câu tới khi trôi chảy mà không phải nghĩ.
> Mỗi câu chứa **một con số** hoặc **một cơ chế** — đó là thứ phân biệt câu trả lời của người đã đo với câu trả lời của người đã đọc.

**Câu 1 — khi được hỏi "artifact và cache khác nhau chỗ nào":**

> "Tôi trả lời bằng chuyện **ai giữ**, vì mọi khác biệt khác đều từ đó ra. Artifact do **server GitLab** giữ: nó có bản ghi trong cơ sở dữ liệu, có URL tải, có hạn giữ, và tôi hỏi được nó bằng API từ ngoài job. Cache do **runner** giữ: nó là một tệp nén trên đĩa của đúng cái máy vừa chạy job, không ai ghi sổ, và **không có endpoint nào** để tôi hỏi 'cache của khoá này còn không'. Hai kho, một cái có API đọc. Nên artifact là **hợp đồng** — tôi kiểm chứng được từ bên ngoài; cache là **tối ưu** — tôi chỉ tin được, không kiểm được. Câu tôi hỏi để chọn giữa hai cái chỉ có một: job sau **sai** nếu thiếu nó, hay chỉ **chậm** hơn?"

**Câu 2 — khi được hỏi "lỗi CI nào làm bạn mất nhiều thời gian nhất":**

> "Không phải job đỏ — job đỏ là loại rẻ nhất, thấy trong vài giây. Loại làm tôi mất thời gian là job **xanh mà artifact rỗng**. Cơ chế thế này: upload artifact là một bước **riêng chạy sau `script`**, và kết quả bước đó không được cộng vào mã thoát của job. Nên `artifacts:paths` trỏ sai thư mục thì runner ghi một dòng cảnh báo, đóng gói một gói rỗng, và job vẫn xanh. Tôi phát hiện bằng hai khẳng định cùng lúc: job trả `status` là `success`, mà gọi API tải artifact thì được `404`. Cách chặn rẻ đến mức vô lý — **một dòng `test -s dist/app.js`** sau bước build, tốn khoảng **một phần mười giây**. Một dòng đó chuyển lỗi từ ô 'im lặng, không chặn' sang ô 'job đỏ ngay'. Lần đầu tôi bật nó lên, có hai job đang đóng gói artifact rỗng suốt mấy tuần mà không ai biết."

**Câu 3 — khi được hỏi "bạn quyết định có nên thêm cache hay không như thế nào":**

> "Tôi coi cache là một khoản đầu tư và tôi lập sổ thu chi cho nó. Ba con số, đọc từ giây của từng pha trong `trace` chứ không nhìn tổng thời gian job trên giao diện: thời gian **tạo lại** từ đầu, thời gian **nén và tải lên** ở cuối job, thời gian **tải và giải nén** ở đầu job. Cache có lãi khi tỉ lệ trúng nhân với hiệu 'tạo lại trừ giải nén' lớn hơn chi phí nén và tải. Chia ra là biết cần bao nhiêu lần trúng để hoà vốn. Ví dụ thật của tôi: cache `node_modules` **380 MB** — tạo lại 95 giây, ghi 61 giây, đọc 44 giây. Lãi mỗi lần trúng 51 giây, chia 61 cho 51 thì ra **hoà vốn sau 2 lần trúng**. Cái cache mà cả đội bảo 'to quá chắc không đáng' thì hoà vốn trong buổi sáng."

**Câu 4 — khi được hỏi "vì sao cache của đội bạn không hiệu quả":**

> "Vì **khoá**, gần như không bao giờ vì kích thước. Kích thước lớn làm cả hai vế của phép tính lớn lên cùng tỉ lệ — tạo lại lâu hơn thì nén và tải cũng lâu hơn, nên tỉ số gần như không đổi. Còn khoá sai thì nó đưa tỉ lệ trúng về **không** và giữ nguyên chi phí ghi. Ca tôi gặp nhiều nhất là `cache:key` đặt bằng `CI_COMMIT_SHA` — mỗi commit một khoá mới nên **trúng 0% vĩnh viễn**, mà trong log không có một chữ 'lỗi' nào, vì trượt cache không làm job đỏ. Đổi sang khoá theo hash của `package-lock.json` thì trên hai mươi lần chạy chỉ có một lần đổi lockfile — **19 trên 20, tức 95%** trúng. Và tôi kiểm được khoá tính lúc nào: nó tính **trên runner sau khi checkout xong**, không phải lúc tạo pipeline — vì muốn hash lockfile thì phải có lockfile trong tay trước đã."

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
| ≥ 80% | Nắm vững. Giao BT mở rộng §L10 về distributed cache, làm trước buổi 13 |
| 60–79% | Đạt. Đọc lại quy tắc bị mất điểm trước buổi 06 |
| 40–59% | Chưa đạt. Làm lại bước lab tương ứng ở nhà, ưu tiên bước 2 (artifact rỗng) và bước 4 (sổ thu chi cache) |
| < 40% | Chưa đạt. Học lại cả buổi trước khi sang buổi 06 — buổi 08, 14 và cả giai đoạn 3 dựng thẳng lên bảng phân loại của buổi này |

**Bảng lỗi làm trần điểm là 1:**

| Lỗi | Vì sao nghiêm trọng đến mức trần điểm |
|---|---|
| "Cache được đảm bảo tồn tại" hoặc "runner báo lỗi khi trượt cache" | Hiểu sai luận đề cả buổi. Người tin điều này dùng cache để truyền `node_modules` giữa hai job, sinh ra loại lỗi tốn nhiều giờ điều tra nhất: chạy tốt 9 lần, hỏng lần thứ 10, không ai đổi gì. Thực tế là **0** dòng lỗi và **0** thay đổi mã thoát khi trượt cache |
| "Job upload artifact rỗng thì job đỏ" | Chế độ hỏng im lặng số một của cả giai đoạn 1. Người tin job sẽ đỏ thì không bao giờ viết một dòng khẳng định nào, nên mọi hiện vật của họ đều đang không được kiểm |
| Nói định lượng ("cache nhanh hơn nhiều", "artifact tốn lắm") mà khi hỏi lại vẫn không có số | Vi phạm nguyên tắc của khoá. Ở phỏng vấn thật, đây là dấu hiệu người chưa mở `trace` đọc giây từng pha lần nào — mà với buổi này thì đó là toàn bộ nội dung |

---

## V5. Bài tập về nhà

### BTVN 1. Ba con số giây của một pipeline thật

Lấy pipeline **gần nhất** của một repo đang chạy (của mình hoặc của đội). Với **mỗi** job, đọc `trace` qua API và ghi ba con số giây: pha `Downloading artifacts`, pha `Restoring cache`, pha `Creating cache`.

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs" | jq -r '.[] | "\(.id)\t\(.name)"' \
| while IFS=$'\t' read -r JID JNAME; do
    T=$(curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/projects/$PID/jobs/$JID/trace")
    echo -e "$JNAME\tdownload=$(printf '%s' "$T" | grep -c 'Downloading artifacts for')\trestore=$(printf '%s' "$T" | grep -ci 'restoring cache')\tcreate=$(printf '%s' "$T" | grep -ci 'creating cache')"
  done
```

**Nộp:** bảng có số dòng bằng số job, cộng **một dòng tổng** ba con số giây của cả pipeline. Ba con số tổng đó là toàn bộ cơ sở để nói chuyện tối ưu ở buổi 14 — giữ lại, đừng làm mất.

### BTVN 2. Đếm hợp đồng đang không được kiểm

Trong repo đó, đếm hai con số: (1) số khối `artifacts:` trong `.gitlab-ci.yml` và mọi tệp được `include`; (2) số khối `artifacts:` mà job tương ứng có **ít nhất một khẳng định** (`test -s`, `test -d`, `test -n`, hoặc tương đương) đứng **trước** khối đó trong `script`.

**Nộp:** hai con số và tỉ số của chúng. Tỉ số càng xa 1 thì càng nhiều hợp đồng có thể rỗng mà không ai biết. Kèm danh sách tên job thuộc phần chênh lệch, và với **một** job trong đó, viết dòng khẳng định cụ thể phải thêm — đúng đường dẫn thật, không viết `dist/app.js` cho có.

### BTVN 3. Sổ thu chi cache cho repo thật

Chọn **một** thư mục phụ thuộc của repo đó (`node_modules`, `.m2/repository`, `.gradle/caches`, `GOMODCACHE`, `vendor/`, `.venv`). Đo bốn con số bằng cách chạy pipeline, không đoán: kích thước cache (`du -sh` in ra log) · tạo lại từ đầu (một lần chạy có khoá cố ý sai để trượt) · nén + tải lên (giây pha `Creating cache`) · tải + giải nén (giây pha `Restoring cache` ở lần chạy thứ hai). Rồi tính `nén_và_tải / (tạo_lại − giải_nén)`, làm tròn lên.

**Nộp:** bốn con số đo được, điểm hoà vốn tính ra, và **một câu** kết luận: cache này đang lãi hay lỗ với `cache:key` mà repo đang dùng. Nếu lỗ, ghi thêm nguyên nhân là **khoá** hay **kích thước**, kèm bằng chứng cho lựa chọn đó.

### BTVN 4. Chuẩn bị cho buổi 06

Trả lời ba câu sau bằng viết, mỗi câu 3–5 dòng. Mang theo vào buổi 06.

1. Hôm nay QT 4.2 cho thấy `cache:key` **đọc được biến** — ví dụ `key: $CI_COMMIT_REF_SLUG`. Hãy liệt kê **mọi** chỗ trong GitLab mà một biến có thể được khai, càng nhiều càng tốt, rồi **đoán thứ tự ưu tiên** giữa chúng khi hai chỗ khai cùng một tên biến. Ghi phỏng đoán kèm lập luận, đừng tra tài liệu.
2. Hôm nay QT 5.4 nói về `artifacts:reports`, và buổi 01 QT 5.4 đã dùng `artifacts:reports:dotenv` để sinh biến cho job sau. Biến sinh bởi `dotenv` nằm ở **nấc nào** trong thứ tự ưu tiên bạn vừa đoán ở câu 1? Nó có **ghi đè** được một biến khai ở cấp project không? Ghi phỏng đoán, và ghi luôn phép đo bạn sẽ dùng để kiểm.
3. Hôm nay QT 5.3 dựng cả buổi quanh chuyện *hiện vật không có nội dung mà job vẫn xanh*. Ghi lại **một** ca thật *"biến không có giá trị đúng"* bạn đã từng gặp: **giá trị mong đợi**, **giá trị thật**, và **cách bạn đã phát hiện**. Nếu chưa gặp, ghi rõ "chưa gặp" và mô tả ca bạn cho là dễ gặp nhất trong repo hiện tại của mình.

**Ba câu này dẫn vào đâu:** câu 1 dẫn thẳng vào **§4 buổi 06** với bảng **9 nguồn biến** — cái đáng giá không phải danh sách 9 dòng, mà là việc học viên tự đoán thứ tự trước rồi đối chiếu, vì chỗ đoán sai chính là chỗ sẽ gây sự cố ở nơi làm việc. Câu 2 dẫn vào **§4 buổi 06 (QT 4.3)**, nơi khoá học chốt `dotenv` nằm ở **nấc 5** trong 9 nấc đó, nó ghi đè được gì và không ghi đè được gì — nối trực tiếp với trục `t0` của buổi 04 và với đường vào thứ tư của buổi 01 QT 5.1. Câu 3 dẫn vào **lab buổi 06, bước 2 và bước 4**, nơi ta tái hiện **5** ca *"biến không có giá trị đúng"* — ca thật mà học viên mang tới gần như luôn trùng với một trong năm ca đó, nên hãy ghi cụ thể chứ đừng ghi chung chung; nó sẽ được dùng làm **ca thứ sáu** của lớp.