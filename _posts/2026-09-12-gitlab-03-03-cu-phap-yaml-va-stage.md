---
layout: post
title: "[Bài 03] Cú Pháp YAML Cốt Lõi & Thiết Kế Stages: .gitlab-ci.yml, Pipeline Execution Order & Điều Phối Tuyến Tính"
date: 2026-09-12 09:10:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-03
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 3
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.03] Hướng dẫn chuyên sâu Cú Pháp YAML Cốt Lõi & Thiết Kế Stages: .gitlab-ci.yml, Pipeline Execution Order & Điều Phối Tuyến Tính: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

{% raw %}
# [BÀI 03] CÚ PHÁP YAML CỐT LÕI & THIẾT KẾ STAGES: .GITLAB-CI.YML, PIPELINE EXECUTION ORDER & ĐIỀU PHỐI TUYẾN TÍNH

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7.
> Mọi đoạn YAML dán được vào `.gitlab-ci.yml` và chạy trong dưới 60 giây.

---





| # | Câu hỏi | Đáp án vắn tắt |
|---|---|---|
| 1 | Một job được cấu hình bởi những tệp nào | **Hai**: `.gitlab-ci.yml` nói **làm gì**; `config.toml` nói **chạy ở đâu và với quyền gì**. **3 trên 8 pha** thuộc phía hạ tầng — không có dòng `Executing "step_script"` thì đừng sửa YAML nữa |
| 2 | Bốn executor xếp theo trục nào | **Mức cô lập**, không phải tốc độ. Cái giá là **chi phí khởi tạo**: `shell` ≈ 0 giây, `docker` bậc 1–5 giây, `kubernetes` bậc 5–20 giây |
| 3 | Executor `shell` rò rỉ qua đâu | **Ba kênh**: hệ tệp ngoài thư mục dự án · tiến trình nền còn sống · trạng thái công cụ toàn cục. Ô **im lặng, không chặn** |
| 4 | `concurrent` khác `limit` thế nào | `concurrent` là trần **toàn cục** của tiến trình runner; `limit` là trần **một mục**. Trần thật là **min** của hai. Mặc định `concurrent = 1` |
| 5 | Runner chấm xanh mà job vẫn `pending` | Chấm xanh chỉ nói về **một** trong **ba** điều kiện độc lập: `online` + không `paused` + khớp định tuyến. **3 nguyên nhân, 1 triệu chứng** |



Hai buổi trước đã nói hai điều mà hôm nay ghép lại:

- Buổi 01 QT 5.1: dữ liệu vào một job đi qua đúng **bốn đường** — và `stage` **không** phải một trong bốn đường đó.
- Buổi 02 QT 6.1: số job chạy song song do **`concurrent`** quyết định — không do `stage`.

Ghép hai điều ấy lại thì `stage` còn lại đúng một chức năng, và chức năng đó nhỏ hơn nhiều so với điều phần lớn người dùng nghĩ.

**Luận đề trung tâm.**

> **`stage` là ràng buộc THỨ TỰ, không phải ràng buộc DỮ LIỆU. Nó nói "job này chạy sau job kia"; nó KHÔNG nói "job này nhận được gì từ job kia". Nhầm hai thứ ấy sinh ra cả hai loại lỗi cùng lúc: pipeline CHẬM vì hàng rào không cần thiết, và pipeline SAI vì tưởng có dữ liệu chảy qua hàng rào.**

```
   HIỂU SAI (rất phổ biến)              HIỂU ĐÚNG
   stage: build ──dữ liệu──▶ stage: test    stage chỉ là HÀNG RÀO THỜI GIAN
        │                                    ├── dữ liệu đi bằng artifacts (buổi 01 QT 5.1)
        └── "test tự có dist/"                └── song song đi bằng concurrent (buổi 02 QT 6.1)

   Hai hệ quả của việc hiểu sai:
   (1) CHẬM : dựng hàng rào ở chỗ không cần → job chờ job chẳng liên quan
   (2) SAI  : bỏ artifacts vì tưởng stage đã chuyển dữ liệu → job xanh, hiện vật rỗng
```

| Kết quả buổi trước | Nguồn | Dùng ở đâu hôm nay |
|---|---|---|
| Bốn đường vào; `stage` không phải một trong bốn | buổi 01 QT 5.1 | **§5 — nửa "không phải ràng buộc dữ liệu" của luận đề** |
| Artifact là hợp đồng, cache là tối ưu | buổi 01 QT 5.2 | §5 QT 5.1 — cái **thật sự** chuyển dữ liệu |
| `after_script` là shell mới | buổi 01 QT 4.3 | §6 QT 6.1 — hôm nay đo cả ba khối lệnh |
| `concurrent` là trần toàn cục | buổi 02 QT 6.1 | **§5 QT 5.2 — song song do `concurrent`, không do `stage`** |
| Hai tệp cấu hình | buổi 02 QT 4.1 | §7 — hôm nay thêm nấc thứ ba là `default:` |

Hôm nay là **lần thứ BA** khoá học áp quy tắc *hành vi phụ thuộc phiên bản thì phải ĐO, không tra tài liệu* — lần một ở buổi 01 lab bước 4 (mã thoát ống dẫn), lần hai ở buổi 02 lab bước 1 (nạp lại `config.toml`). Hôm nay có năm đại lượng phải đo, liệt kê ở §6 và §7.

**Ba câu hỏi trung tâm của buổi:**

1. Trong một tệp `.gitlab-ci.yml`, làm sao biết khoá nào là **job** và khoá nào không?
2. `stage` cho ta cái gì, và **không** cho ta cái gì?
3. Khi ba nguồn cùng khai `image`, cái nào thắng — và làm sao biết chắc mà không phải đoán?

---



| # | Làm được gì | Hiện vật chứng minh |
|---|---|---|
| LĐ1 | Nhìn một tệp `.gitlab-ci.yml` lạ và chỉ ra ngay khoá nào là job, khoá nào là từ khoá | Lab bước 1, CHECKPOINT 1 |
| LĐ2 | Dùng `ci/lint` để đọc tệp **sau phân giải** thay vì đoán từ YAML thô | Lab bước 1, CHECKPOINT 3 |
| LĐ3 | Phát hiện được job rác do gõ sai khoá | Lab bước 1, CHECKPOINT 2 |
| LĐ4 | **Đo được lãng phí hàng rào** của một pipeline bằng giây | `lang-phi-hang-rao.tsv`, lab bước 2 |
| LĐ5 | Giải thích được vì sao 6 job cùng stage có thể chạy tuần tự | Lab bước 3, CHECKPOINT 7 |
| LĐ6 | Chẩn đoán được lỗi do `cd` xuyên dòng và do YAML nuốt ký tự | Lab bước 4, CHECKPOINT 9, 10 |
| LĐ7 | Nói được `image` khai ở ba nơi thì cái nào thắng, và chứng minh bằng đo | Lab bước 5, CHECKPOINT 11 |

---



| Cần biết | Mức yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Bốn đường vào, hai đường ra | **Vận dụng** | Buổi 01 QT 5.1, 5.4 — **tiền đề của §5** |
| Artifact là hợp đồng, cache là tối ưu | Vận dụng | Buổi 01 QT 5.2 |
| `after_script` là shell mới | Vận dụng | Buổi 01 QT 4.3 — cơ sở của §6 |
| `concurrent` là trần toàn cục | **Vận dụng** | Buổi 02 QT 6.1 — **tiền đề của QT 5.2** |
| Hai tệp cấu hình | Vận dụng | Buổi 02 QT 4.1 — cơ sở của §7 |
| YAML: thụt lề, danh sách, ánh xạ | Vận dụng | YAML có đúng ba cấu trúc; §3.1 nhắc lại |
| `curl` gửi được `--data-urlencode` | Nhớ | Dùng ở bước 1 để gọi `ci/lint` |

---



### 3.1. Đối chiếu thuật ngữ

| Tiếng Việt | Tiếng Anh | Trong bài dùng gì | Ghi chú |
|---|---|---|---|
| khoá cấp trên cùng | top-level keyword | tiếng Việt | Khoá không thụt lề trong tệp |
| từ khoá dành riêng | reserved keyword | tiếng Việt | 13 khoá GitLab hiểu là cấu hình, không phải job |
| công việc ẩn | hidden job | tiếng Việt | Job tên bắt đầu bằng `.`, không bao giờ chạy |
| khối mặc định | default block | `default` | Nấc giữa của thứ tự ưu tiên |
| hàng rào | barrier | tiếng Việt | Điểm đồng bộ thời gian giữa hai stage |
| chặng | stage | `stage` | Từ khoá; dùng thẳng tiếng Anh |
| chặng ngầm | implicit stage | tiếng Việt | `.pre` và `.post` |
| khối lệnh | script block | `script` | Ba khối: `before_script`, `script`, `after_script` |
| chuỗi khối | block scalar | tiếng Việt | `\|` giữ xuống dòng, `>` gộp dòng |
| neo YAML | YAML anchor | anchor | `&ten` và `*ten`; buổi 10 xử lý đầy đủ |
| kiểm tệp trước khi chạy | CI lint | `ci/lint` | Endpoint API trả về tệp sau phân giải |
| phân giải | resolve / merge | tiếng Việt | Hợp nhất `include`, `extends`, `default`, anchor |
| thứ tự ưu tiên | precedence | tiếng Việt | Ba nấc ở §7 |
| đường găng | critical path | tiếng Việt | Chuỗi phụ thuộc **dữ liệu** dài nhất |
| lãng phí hàng rào | barrier waste | tiếng Việt | Tổng thời gian trừ đường găng |

Nhắc lại YAML trong ba dòng, vì cả khoá này gõ nó: **ánh xạ** là `khoa: gia-tri`; **danh sách** là các dòng bắt đầu bằng `- `; **thụt lề** quyết định cấp — và thụt lề chỉ dùng **dấu cách**, không dùng tab.



`stage` không phải một thùng chứa. Nó là một **hàng rào**: mọi job trước hàng rào phải kết thúc thì hàng rào mới mở.

Cách nhìn này trả lời ngay ba câu hỏi hay gặp. Dữ liệu có chảy qua hàng rào không? Không — hàng rào chỉ chặn thời gian, không chuyển gì. Job cùng bên hàng rào có chạy cùng lúc không? Chỉ khi có đủ slot; hàng rào không cấp slot. Thêm một hàng rào tốn gì? Tốn đúng thời gian của job chậm nhất ở bên trước nó.

Mô hình này quay lại ở buổi 08 (`needs` **bỏ** hàng rào và biến pipeline thành đồ thị), buổi 12 (merge train), buổi 14 (đường găng), buổi 22 (monorepo).

### 3.3. Mô hình tư duy 2: phân giải rồi mới đọc

Từ buổi 10 trở đi, tệp `.gitlab-ci.yml` mà học viên viết **không phải** tệp mà GitLab chạy: `include` kéo tệp khác vào, `extends` hợp nhất job, `default` điền vào chỗ trống, anchor được khai triển. Đọc tệp thô để đoán hành vi là đoán về một tệp không tồn tại.

Công cụ đúng là endpoint `ci/lint`: nó trả về **tệp sau phân giải**, tức đúng thứ GitLab sẽ chạy. Một lệnh `curl` mất 1 giây; một vòng đẩy commit rồi chờ pipeline mất 3–5 phút. Chênh lệch ấy nhân với số lần thử sai trong một buổi chiều là con số đáng kể.

Mô hình này quay lại ở buổi 10, 11, 44 — và ở đó nó không còn là tiện lợi mà là **điều kiện cần**.

### 3.4. Mô hình tư duy 3: gần job nhất thì thắng

Ba nguồn có thể khai cùng một thứ — ví dụ `image`. Chúng xếp theo **khoảng cách tới job**:

```
   xa nhất ──────────────────────────────────────► gần nhất
   config.toml           default:              trong chính job
   (mặc định của runner)  (mặc định của tệp)    (khai riêng)
```

Cái gần job nhất thắng, và nó **thay thế** chứ không **hợp nhất**. Đây là quy tắc duy nhất cần nhớ cho `image`, `cache`, `artifacts`, `before_script`, `after_script`, `services`, `tags`.

Cảnh báo đi kèm: **`variables` không theo quy tắc này**. Nó có bộ quy tắc riêng với chín nguồn, và buổi 06 dành trọn cho nó. Suy quy tắc của `image` sang cho `variables` là một trong những nhầm lẫn tốn thời gian nhất.

Mô hình này quay lại ở buổi 06 (biến), buổi 10 (`extends` thêm nấc thứ tư), buổi 11 (component thêm nấc thứ năm).

---

### 1.1. Giải phẫu một tệp: cái gì là job, cái gì không (9 phút)

### 4.1. Mọi khoá không dành riêng đều là một job

**Nguyên lý cốt lõi:** Mọi khoá **cấp trên cùng** không nằm trong danh sách từ khoá dành riêng đều được GitLab hiểu là **một job**. Gõ sai tên một từ khoá thì GitLab **không báo lỗi** — nó tạo một job mang tên gõ sai.

**Giải thích cơ chế ngầm:** GitLab phân tích tệp theo nguyên tắc loại trừ: nó có một danh sách từ khoá cấu hình cấp trên cùng; mọi khoá còn lại được coi là định nghĩa job. Nguyên tắc ấy làm cú pháp gọn — không cần khối `jobs:` bao ngoài — nhưng nó đánh đổi bằng việc **mọi lỗi chính tả đều hợp lệ về cú pháp**.

Mười ba từ khoá cấp trên cùng của GitLab 17.x:

| Từ khoá | Làm gì |
|---|---|
| `stages` | Khai danh sách stage và **thứ tự** của chúng |
| `default` | Giá trị mặc định cho mọi job — nấc giữa của §7 |
| `variables` | Biến cấp pipeline — quy tắc riêng, buổi 06 |
| `include` | Kéo tệp khác vào — buổi 10 |
| `workflow` | Quyết định **cả pipeline** có được tạo không — buổi 04 |
| `image` | Image mặc định (tương đương `default:image`) |
| `services` | Service mặc định |
| `cache` | Cache mặc định |
| `before_script` | Khối lệnh mặc định chạy trước |
| `after_script` | Khối lệnh mặc định chạy sau |
| `pages` | Job đặc biệt xuất bản GitLab Pages |
| `hooks` | Móc chạy ở thời điểm đặc biệt |
| `spec` | Khai `inputs` cho tệp được `include` — buổi 11 |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Trong danh sách job của pipeline xuất hiện một job mang tên lạ: `sciprt`, `stgaes`, `artefacts`, `varaibles`. Và tệ hơn: khoá **thật** mà học viên định gõ **không có tác dụng gì**, nên hành vi mong đợi biến mất mà không có thông báo nào.

Ô của bảng hai thuộc tính: **im lặng, không chặn** — job rác thường xanh (nó chẳng làm gì), và cấu hình bị mất cũng không báo. Đây là **lần thứ BA** khoá học gặp một ca rơi vào ô nguy hiểm nhất.

**Minh hoạ.**

```yaml
# Tệp này KHÔNG có lỗi cú pháp. Nó tạo 3 job, không phải 2.
stages: [build, test]

variabels:              # ← gõ sai `variables`. GitLab tạo một JOB tên "variabels".
  MOI_TRUONG: "dev"

build:
  stage: build
  script: [echo "build"]

test:
  stage: test
  script: [echo "MOI_TRUONG=$MOI_TRUONG"]   # in ra rỗng — biến chưa bao giờ tồn tại
```

Cách phát hiện trong 1 giây, trước khi đẩy commit — đây chính là QT 4.3:

```bash
curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "$(jq -Rs '{content: .}' < .gitlab-ci.yml)" \
  "$GITLAB/api/v4/projects/$PID/ci/lint" \
| jq -r '.valid, (.jobs[].name)'
```

Nếu danh sách job in ra có tên lạ thì đã tìm được lỗi mà không cần đẩy commit.

**Con số cần nhớ, và giới hạn của nó.** **13** từ khoá cấp trên cùng ở GitLab 17.x. Con số này **đổi theo phiên bản** — `hooks` và `spec` là thêm mới của dòng 17.x. Đừng học thuộc danh sách; học **nguyên tắc loại trừ** và học cách gọi `ci/lint`.

### 4.2. Job ẩn: một dấu chấm là đủ

**Nguyên lý cốt lõi:** Job có tên bắt đầu bằng **dấu chấm** là **job ẩn**: GitLab không bao giờ chạy nó. Đó là cơ chế dùng lại rẻ nhất, và là nền của `extends` ở buổi 10.

**Giải thích cơ chế ngầm:** GitLab bỏ qua mọi khoá cấp trên cùng bắt đầu bằng `.` khi dựng danh sách job. Nhưng nội dung của chúng vẫn được phân giải, nên chúng dùng được làm khuôn mẫu cho `extends` và cho anchor.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Quên dấu chấm: khuôn mẫu **chạy thật** như một job bình thường, thường là đỏ vì nó không có `script` đầy đủ. Ngược lại, thêm dấu chấm nhầm vào một job thật: job biến mất khỏi pipeline **im lặng** — không lỗi, không cảnh báo, chỉ là nó không còn ở đó.

**Minh hoạ.**

```yaml
# .mau là job ẩn — không chạy, nhưng dùng lại được
.mau-test:
  image: node:22-alpine
  before_script: [npm ci]
  cache:
    key:
      files: [package-lock.json]
    paths: [.npm/]

test-unit:
  extends: .mau-test
  script: [npm run test:unit]

test-e2e:
  extends: .mau-test
  script: [npm run test:e2e]
```

**Con số cần nhớ: 1 ký tự.** Một dấu chấm biến một job thành khuôn mẫu, và bỏ nó đi biến khuôn mẫu thành job chạy thật.

### 4.3. Đọc tệp sau phân giải, đừng đoán

**Nguyên lý cốt lõi:** API `ci/lint` trả về tệp **sau khi phân giải** — sau `include`, `extends`, `default`, anchor. Đọc nó thay vì đoán từ YAML thô.

**Giải thích cơ chế ngầm:** Tệp mà học viên viết và tệp mà GitLab chạy là hai thứ khác nhau ngay khi có `default:`, và khác nhau rất nhiều khi có `include` và `extends`. Endpoint `ci/lint` chạy đúng bộ phân giải của GitLab và trả về kết quả cuối cùng, gồm danh sách job kèm cấu hình đầy đủ của từng job.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Vòng lặp "sửa một dòng, đẩy commit, chờ 4 phút, xem kết quả, đoán tiếp". Một buổi chiều theo cách ấy gỡ được hai lỗi. Với `ci/lint`, cùng số lần thử mất vài phút.

**Minh hoạ.**

```bash
# Hàm dùng lại cho cả khoá — nạp vào ~/.bashrc thì tiện
lint() {
  curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    --header "Content-Type: application/json" \
    --data "$(jq -Rs '{content: ., include_merged_yaml: true}' < "${1:-.gitlab-ci.yml}")" \
    "$GITLAB/api/v4/projects/$PID/ci/lint"
}

# Có hợp lệ không, và nếu không thì lỗi ở đâu
lint | jq -r '.valid, .errors[]?, .warnings[]?'

# Danh sách job SAU phân giải — chỗ phát hiện job rác
lint | jq -r '.jobs[] | "\(.name)\tstage=\(.stage)"'

# Cấu hình đầy đủ của một job sau khi hợp nhất default và extends
lint | jq -r '.jobs[] | select(.name=="test") | {name, stage, script, before_script, tag_list}'
```

**Con số cần nhớ: 1 giây thay cho 3–5 phút.** Đó là chênh lệch giữa một lệnh `curl` và một vòng đẩy commit rồi chờ pipeline. Nhân với số lần thử sai trong một buổi thì nó là chênh lệch giữa xong việc và không xong việc.

---

### 1.2. `stage` là ràng buộc thứ tự, không phải ràng buộc dữ liệu (11 phút)

### 5.1. Nửa thứ nhất: không chuyển dữ liệu

**Nguyên lý cốt lõi:** `stage` là ràng buộc **thứ tự**, không phải ràng buộc **dữ liệu**. Dữ liệu giữa hai job đi bằng `artifacts` (buổi 01 QT 5.1), không đi bằng `stage`.

**Giải thích cơ chế ngầm:** Buổi 01 đã liệt kê đủ bốn đường vào một job: git, cache, artifact, biến. `stage` không nằm trong danh sách ấy, và không có cơ chế nào của runner đọc `stage` để quyết định chuyển gì. Job ở stage sau vẫn phải tải artifact ở pha `download_artifacts` — và nó chỉ tải được nếu job trước đã **khai** `artifacts`.

Chỗ gây hiểu nhầm là mặc định của GitLab: job tải artifact của **mọi** job ở các stage trước (buổi 01 QT 5.3). Mặc định ấy làm ta có cảm giác `stage` chuyển dữ liệu — nhưng cái chuyển dữ liệu là `artifacts`, còn `stage` chỉ quyết định **tập nào được tải mặc định**.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job stage sau báo `No such file or directory` với một tệp mà job stage trước rõ ràng đã tạo và log job trước có in ra tên tệp đó. Đây đúng là ca hỏng số 1 của buổi 01, chỉ khác lý do: buổi 01 là ghi vào `/tmp`, hôm nay là quên khai `artifacts`.

**Minh hoạ.**

```yaml
# SAI — tưởng stage chuyển dữ liệu
stages: [build, test]

build-sai:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p dist && echo "console.log(1)" > dist/app.js
    - ls -la dist/          # có tệp, log chứng minh rõ ràng
  # thiếu artifacts

test-sai:
  stage: test
  image: alpine:3.20
  script:
    - cat dist/app.js       # ĐỎ — stage không chuyển gì

# ĐÚNG
build-dung:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p dist && echo "console.log(1)" > dist/app.js
  artifacts:
    paths: [dist/]
    expire_in: 1 hour

test-dung:
  stage: test
  image: alpine:3.20
  script:
    - test -s dist/app.js || { echo "KHANG DINH HONG: khong co dist/app.js"; exit 1; }
    - cat dist/app.js
```

**Con số cần nhớ: `stage` chuyển 0 byte.**

### 5.2. Nửa thứ hai: không đảm bảo song song

Đây là câu trả lời cho BTVN 4 câu 2 của buổi 02.

**Nguyên lý cốt lõi:** Hai job cùng `stage` chạy song song **chỉ khi có đủ slot runner**. `stage` không đảm bảo song song; `concurrent` mới quyết định (buổi 02 QT 6.1).

**Giải thích cơ chế ngầm:** `stage` chỉ nói rằng các job trong đó **được phép** chạy đồng thời — nó gỡ ràng buộc thứ tự giữa chúng. Việc chúng có thật sự chạy đồng thời hay không do phía runner quyết định: trần `concurrent`, trần `limit`, số runner khớp tag, và tài nguyên máy. Với `concurrent = 1`, sáu job cùng stage chạy **tuần tự**, và thời gian của stage bằng **tổng** thời gian sáu job chứ không bằng **max**.

Đây là chỗ hai buổi trước ghép vào nhau: `stage` thuộc `.gitlab-ci.yml`, `concurrent` thuộc `config.toml` — hai tệp, hai người (buổi 02 QT 4.1). Người viết pipeline khai sáu job cùng stage và tưởng chúng chạy song song; người vận hành runner đặt `concurrent = 1` và không biết ai đang trông chờ gì.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Một stage có 6 job, mỗi job 30 giây, nhưng stage mất 180 giây. Cách kiểm nhanh: lấy `started_at` và `finished_at` của các job qua API và xem chúng có **chồng lấn** nhau không.

**Minh hoạ.**

```bash
# Đo song song THẬT — kỹ thuật đã dùng ở buổi 02 lab bước 3
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE/jobs?per_page=100" \
| jq -r '[ .[] | select(.started_at != null and .finished_at != null)
           | {s: (.started_at|fromdateiso8601), f: (.finished_at|fromdateiso8601)} ] as $j
         | [ $j[].s ] | map( . as $t | [ $j[] | select(.s <= $t and .f > $t) ] | length ) | max // 0'
# Kết quả 1  → không có job nào chạy song song, dù chúng cùng stage
```

**Con số cần nhớ:** với `concurrent = 1`, thời gian một stage `n` job bằng **tổng**, không bằng **max**. Với 6 job × 30 giây: 180 giây thay vì 30 giây.

### 5.3. Hàng rào và cái giá của nó

**Nguyên lý cốt lõi:** Một stage chỉ bắt đầu khi **mọi** job của stage trước **kết thúc**, kể cả job chẳng liên quan gì. Đây là nguồn lãng phí lớn nhất của pipeline tuần tự.

**Giải thích cơ chế ngầm:** Hàng rào là ràng buộc **toàn cục** giữa hai stage: nó không phân biệt job nào phụ thuộc job nào. Một job ở stage sau chỉ cần artifact của **một** job ở stage trước vẫn phải chờ **tất cả** job stage trước xong.

Định lượng được bằng phép trừ:

```
lãng phí hàng rào = tổng thời gian pipeline − đường găng dữ liệu thật
```

Trong đó **đường găng dữ liệu** là chuỗi phụ thuộc `artifacts` dài nhất — tức thời gian tối thiểu mà pipeline không thể ngắn hơn.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Trong một pipeline, có một job dài bất thường ở stage giữa mà **không job nào sau nó cần artifact của nó**. Job ấy đang giữ hàng rào cho cả pipeline mà không đóng góp gì vào kết quả.

**Minh hoạ.** Cấu hình bài lab đo, với số cụ thể:

```yaml
stages: [build, test, dong-goi]

build:
  stage: build
  script: [sleep 10, mkdir -p dist, "echo x > dist/app.js"]
  artifacts: {paths: [dist/]}

test-nhanh:
  stage: test
  script: [sleep 5]

test-cham:                  # 60 giây, và KHÔNG job nào sau nó cần artifact của nó
  stage: test
  script: [sleep 60]

dong-goi:
  stage: dong-goi
  script: [ls -la dist/]    # chỉ cần artifact của `build`
```

| Đại lượng | Giá trị |
|---|---|
| Tổng thời gian pipeline | 10 + 60 + thời gian `dong-goi` ≈ **72 giây** |
| Đường găng dữ liệu thật (`build` → `dong-goi`) | 10 + 2 ≈ **12 giây** |
| **Lãng phí hàng rào** | ≈ **60 giây** |

`dong-goi` chờ `test-cham` 60 giây mà chẳng cần gì của nó. Buổi 08 giải chuyện này bằng `needs`, và con số 60 giây chính là con số đo được trước khi giải.

**Con số cần nhớ, và giới hạn:** con số 55–60 giây là của **bài lab**, phụ thuộc chênh lệch thời lượng job. Cái phổ quát là **phép trừ**, không phải con số.

### 5.4. Hai stage luôn tồn tại

**Nguyên lý cốt lõi:** Có hai stage **luôn tồn tại** mà không cần khai: `.pre` chạy trước mọi stage, `.post` chạy sau mọi stage.

**Giải thích cơ chế ngầm:** GitLab dựng sẵn hai stage này ở hai đầu để đặt các job hạ tầng — kiểm tra đầu vào, thu thập báo cáo, dọn dẹp — mà không phải sửa danh sách `stages:` của từng project. Chúng **không** đếm vào `stages:` và **không** đổi thứ tự các stage khác.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thêm một stage `kiem-tra-truoc` vào đầu `stages:` cho mọi project trong tổ chức, rồi phải sửa 30 tệp khi muốn đổi. Dùng `.pre` thì không cần khai gì.

**Minh hoạ.**

```yaml
stages: [build, test]     # .pre và .post KHÔNG cần khai

kiem-secret:
  stage: .pre             # chạy trước build, luôn luôn
  image: zricethezav/gitleaks:latest
  script: [gitleaks detect --source . --no-banner]

thu-thap-bao-cao:
  stage: .post            # chạy sau test, kể cả khi có job đỏ (tuỳ rules)
  script: [echo "gom bao cao"]
```

**Con số cần nhớ: 2 stage ngầm.** Chúng dùng nhiều ở buổi 29 (Gitleaks đặt ở `.pre` để chặn sớm) và buổi 46 (thu thập số liệu DORA ở `.post`).

---

### 1.3. `script`: ba khối lệnh, hai shell, và YAML nuốt ký tự (9 phút)

### 6.1. Ba khối, hai shell

**Nguyên lý cốt lõi:** Ba khối lệnh chạy trong **hai** shell: `before_script` và `script` nối vào **cùng một** shell; `after_script` chạy trong shell **riêng** (buổi 01 QT 4.3).

**Giải thích cơ chế ngầm:** Runner ghép `before_script` và `script` thành một script duy nhất rồi chạy nó — nên biến, `cd`, hàm shell đều đi xuyên từ khối đầu sang khối sau. `after_script` được sinh thành một script riêng và chạy như tiến trình riêng, để nó vẫn chạy được kể cả khi `script` đã chết.

| Khối | Shell | Thấy biến của `before_script`? | Chạy khi `script` đỏ? |
|---|---|---|---|
| `before_script` | A | — | — |
| `script` | **A** | **Có** | — |
| `after_script` | **B** | **Không** | **Có** |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Biến in ra rỗng ở `after_script` dù `before_script` đã `export`. Hoặc: `after_script` chạy `cat build/log.txt` không thấy tệp vì `script` đã `cd` sang thư mục khác.

**Minh hoạ.**

```yaml
do-ba-khoi:
  image: alpine:3.20
  before_script:
    - export BIEN_A="dat-o-before_script"
    - echo "before_script: pwd=$(pwd)"
  script:
    - echo "script: BIEN_A=[$BIEN_A]"        # CÓ giá trị — cùng shell
    - echo "script: pwd=$(pwd)"
  after_script:
    - echo "after_script: BIEN_A=[${BIEN_A:-RONG}]"   # RỖNG — shell khác
    - echo "after_script: pwd=$(pwd)"
```

**Con số cần nhớ: 3 khối, 2 shell.** Đây là hành vi **phải đo**, không tra — nó đã đổi giữa các phiên bản runner, nên bài lab bước 4 đo trực tiếp và ghi kèm số phiên bản.

### 6.2. `cd` đi xuyên các dòng

**Nguyên lý cốt lõi:** Mỗi phần tử của danh sách `script` được runner ghép vào cùng một script shell, nên biến và `cd` **tồn tại xuyên các dòng** — và đó vừa là tiện lợi vừa là nguồn nhầm lẫn.

**Giải thích cơ chế ngầm:** Danh sách YAML chỉ là cách viết; runner ghép các phần tử thành các dòng liên tiếp của một tệp script. Không có gì tách chúng thành các tiến trình riêng. Hệ quả: `cd` ở dòng `k` ảnh hưởng **mọi** dòng sau nó trong cùng khối, và cả sang khối `script` nếu `cd` nằm ở `before_script`.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ca kinh điển: dòng 3 `cd` vào thư mục con, dòng 7 ghi tệp — tệp nằm trong thư mục con, nhưng `artifacts:paths` trỏ vào thư mục gốc. Kết quả: **artifact rỗng, job xanh**. Đây là ô im lặng + không chặn, và nó chính là ca hỏng số 2 của buổi 01 xuất hiện lại dưới một nguyên nhân khác.

**Minh hoạ.**

```yaml
# SAI — artifact rỗng, job XANH
build-cd-sai:
  image: alpine:3.20
  script:
    - mkdir -p sau && cd sau
    - mkdir -p dist && echo "console.log(1)" > dist/app.js   # thật ra là sau/dist/app.js
  artifacts:
    paths: [dist/]        # không tồn tại ở gốc → gói RỖNG, job vẫn xanh

# ĐÚNG — quay về gốc trước khi kết thúc, và có khẳng định
build-cd-dung:
  image: alpine:3.20
  script:
    - mkdir -p sau && cd sau
    - mkdir -p dist && echo "console.log(1)" > dist/app.js
    - cd "$CI_PROJECT_DIR"
    - mv sau/dist ./dist
    - test -s dist/app.js || { echo "KHANG DINH HONG: dist/app.js rong"; exit 1; }
  artifacts:
    paths: [dist/]
```

**Con số cần nhớ:** `cd` ở dòng `k` ảnh hưởng **mọi** dòng sau nó. Cách phòng rẻ nhất là dùng `$CI_PROJECT_DIR` làm mốc tuyệt đối, hoặc chạy phần cần đổi thư mục trong subshell: `(cd sau && lam-gi-do)`.

### 6.3. YAML nuốt ký tự

**Nguyên lý cốt lõi:** YAML nuốt ký tự: dấu `:` theo sau khoảng trắng, và các ký tự **mở đầu** `*`, `&`, `{`, `[`, `|`, `>`, `%`, `@` làm YAML hiểu sai dòng lệnh. Bọc bằng nháy đơn hoặc dùng chuỗi khối.

**Giải thích cơ chế ngầm:** YAML phân tích trước, shell chạy sau. Một dòng như `- echo ket qua: xong` bị YAML hiểu là ánh xạ `echo ket qua` → `xong`, không phải một chuỗi lệnh. Tương tự, `*` mở đầu là tham chiếu anchor, `&` là định nghĩa anchor, `{` và `[` là ánh xạ và danh sách dạng gọn.

Hai chuỗi khối cần phân biệt: `|` **giữ** ký tự xuống dòng, `>` **gộp** các dòng thành một.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> `ci/lint` trả về `valid: false` với thông báo lỗi YAML khó hiểu; hoặc tệ hơn, tệp **hợp lệ** nhưng lệnh chạy khác ý định.

**Minh hoạ.**

```yaml
vi-du-yaml:
  image: alpine:3.20
  script:
    # SAI — YAML hiểu là ánh xạ
    # - echo ket qua: xong

    # ĐÚNG — bọc nháy đơn
    - 'echo "ket qua: xong"'

    # ĐÚNG — ký tự mở đầu đặc biệt cũng bọc nháy đơn
    - '*.log se bi xoa'

    # Chuỗi khối `|` — GIỮ xuống dòng, dùng cho script nhiều dòng
    - |
      if [ -d dist ]; then
        echo "co dist"
      else
        echo "khong co dist"
      fi

    # Chuỗi khối `>` — GỘP thành một dòng, dùng cho lệnh dài
    - >
      docker build
      --build-arg PHIEN_BAN="$CI_COMMIT_SHORT_SHA"
      --tag "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA" .
```

**Con số cần nhớ: 8 ký tự** cần chú ý — `:` (theo sau khoảng trắng), `*`, `&`, `{`, `[`, `|`, `>`, `%`, `@` khi ở **đầu** giá trị. Và một quy tắc thực hành rẻ hơn việc nhớ danh sách: **lệnh nào dài quá một dòng hoặc có dấu câu thì dùng chuỗi khối `|`**.

---

### 1.4. Thứ tự ưu tiên: `config.toml` → `default` → job (5 phút)

Đây là câu trả lời cho BTVN 4 câu 3 của buổi 02.

### 7.1. Ba nấc, gần job nhất thì thắng

**Nguyên lý cốt lõi:** Với `image`, `cache`, `artifacts`, `before_script`, `after_script`, `services`, `tags`, có **ba** nguồn xếp theo khoảng cách tới job: `config.toml` (xa nhất, chỉ làm mặc định) → `default:` → khai trong chính job (gần nhất). **Gần job nhất thì thắng.**

**Giải thích cơ chế ngầm:** Ba nguồn ứng với ba phạm vi trách nhiệm: người vận hành runner đặt mặc định cho **mọi project** dùng runner đó; người viết pipeline đặt mặc định cho **một project**; và người viết một job đặt riêng cho **job đó**. Quy tắc "gần nhất thắng" là quy tắc duy nhất tương thích với ba phạm vi lồng nhau ấy.

Điểm dễ nhầm: nấc gần hơn **thay thế** nấc xa hơn, **không hợp nhất** với nó. Khai `before_script` trong một job thì `before_script` ở `default:` bị **bỏ hoàn toàn**, không phải nối vào.

| Nấc | Ai viết | Phạm vi |
|---|---|---|
| `config.toml` | Người vận hành runner | Mọi project dùng runner đó |
| `default:` | Người viết pipeline | Một project |
| Trong job | Người viết pipeline | Một job |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Khai `before_script: [npm ci]` ở `default:` rồi thêm `before_script: [apk add curl]` vào một job — và ngạc nhiên vì `npm ci` không chạy nữa. Nó không chạy vì nấc gần hơn đã thay thế nấc xa hơn.

**Minh hoạ.**

```yaml
default:
  image: alpine:3.20
  before_script:
    - echo "before_script cua default"

job-dung-mac-dinh:
  script: [echo "image = alpine"]

job-ghi-de-image:
  image: node:22-alpine          # thắng default
  script: [node --version]

job-ghi-de-before:
  before_script:
    - echo "before_script rieng"  # THAY THẾ hoàn toàn cái ở default
  script: [echo "before_script cua default KHONG chay"]
```

Kiểm bằng `ci/lint` thay vì đoán — đây là QT 4.3 áp vào một câu hỏi cụ thể:

```bash
lint | jq -r '.jobs[] | "\(.name)\timage=\(.image.name // "khong khai")\tbefore=\(.before_script // [] | join(";"))"'
```

**Con số cần nhớ: 3 nấc; nấc gần nhất thắng và nó thay thế chứ không hợp nhất.** Buổi 10 thêm nấc thứ tư (`extends`), buổi 11 thêm nấc thứ năm (component `inputs`) — và quy tắc vẫn giữ nguyên hình dạng.

### 7.2. `variables` không theo quy tắc này

**Nguyên lý cốt lõi:** `variables` ở cấp trên cùng **không** thuộc `default:` và có quy tắc riêng — nó là một trong chín nguồn biến sẽ học ở buổi 06. Đừng suy quy tắc của `image` sang cho `variables`.

**Giải thích cơ chế ngầm:** Biến đến từ nhiều nguồn hơn hẳn: cấp instance, cấp group, cấp project, `variables` trong tệp, `variables` trong job, biến do `dotenv` truyền, biến hệ thống của GitLab, biến nhập tay khi chạy pipeline thủ công, và biến từ pipeline cha khi có `trigger`. Chín nguồn ấy có thứ tự ưu tiên riêng, và một số nguồn còn có cờ `protected` và `masked` chen vào.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đặt `variables: {MOI_TRUONG: dev}` ở cấp tệp, rồi ngạc nhiên vì job in ra `prod` — vì có một biến cùng tên ở cấp project và nó thắng.

**Minh hoạ.**

```yaml
variables:                 # KHÔNG nằm trong default:
  MOI_TRUONG: "dev"
  LOG_LEVEL: "info"

default:
  image: alpine:3.20
  # KHÔNG đặt variables ở đây — nó không phải khoá của default

in-bien:
  variables:
    LOG_LEVEL: "debug"     # cấp job — thắng cấp tệp
  script:
    - echo "MOI_TRUONG=$MOI_TRUONG"   # dev, TRỪ KHI có biến cùng tên ở cấp project
    - echo "LOG_LEVEL=$LOG_LEVEL"     # debug
```

**Con số cần nhớ: 9 nguồn biến.** Buổi 06 dành trọn cho chúng, kèm bảng thứ tự ưu tiên đầy đủ và năm ca thực nghiệm. Hôm nay chỉ cần nhớ **đừng suy quy tắc ba nấc sang cho biến**.

---

### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước

**Việc 1 — 2 phút, rủi ro bằng 0.** Gọi `ci/lint` cho `.gitlab-ci.yml` hiện tại và đọc **danh sách job** trả về. So với danh sách job mình nghĩ là có. Chênh lệch nào cũng đáng điều tra — thường là job rác do gõ sai (QT 4.1) hoặc job biến mất vì thừa dấu chấm (QT 4.2).

**Việc 2 — 20 phút, rủi ro bằng 0.** Đo **lãng phí hàng rào**:

```
lãng phí = tổng thời gian pipeline − đường găng dữ liệu thật
```

Đường găng dữ liệu là chuỗi phụ thuộc `artifacts` dài nhất. Tính bằng tay trên giấy cũng được với pipeline dưới 20 job.

**Việc 3 — 30 phút, rủi ro bằng 0, và là đầu vào trực tiếp của buổi 08.** Với **mỗi** job, trả lời một câu: *"nó cần artifact của ai?"*. Bảng ấy là bản đồ phụ thuộc dữ liệu thật của pipeline, và ở buổi 08 nó biến thẳng thành các dòng `needs:`.

### Cái gì hỏng nếu áp thẳng lên prod

Gộp hai stage lại làm một để bỏ hàng rào sẽ làm **mất** sự đảm bảo thứ tự mà một job nào đó đang **ngầm** dựa vào — ví dụ một job deploy đang ngầm dựa vào việc job security ở stage trước đã chạy xong.

Trước khi gộp phải biết chắc không job nào dựa vào thứ tự ngầm ấy, và cách kiểm chính là bảng ở việc 3. Đường đi an toàn: **đừng gộp stage** — thay vào đó dùng `needs` ở buổi 08, vì `needs` khai báo **tường minh** phụ thuộc thay vì xoá bỏ nó.

### Đo trước — đo sau

| Chỉ số | Đo bằng | Vì sao chỉ số này |
|---|---|---|
| Tổng thời gian pipeline | API `pipelines/:id` trường `duration` | Con số đội quan tâm |
| Đường găng dữ liệu thật | Cộng thời lượng chuỗi phụ thuộc `artifacts` dài nhất | Đây là **giới hạn dưới** — pipeline không thể nhanh hơn |
| **Lãng phí hàng rào** = hiệu hai số trên | Phép trừ | Đây là số giây có thể lấy lại được, và là lý do dùng `needs` ở buổi 08 |

### Khi nào KHÔNG nên dùng

**Đừng bỏ hàng rào stage ở chỗ nó đang làm cổng kiểm soát có chủ ý.** Một stage `security` chặn stage `deploy` là **tính năng**, không phải lãng phí: hàng rào ở đó bảo đảm không có gì deploy trước khi quét xong. Buổi 35 dựng gate trên đúng cơ chế này. Trước khi gọi một hàng rào là lãng phí, hỏi *"nó có đang bảo đảm điều gì không"*.

**Đừng dùng job ẩn `.mau` cho những chỗ chỉ dùng một lần.** Job ẩn có giá trị khi có từ hai job trở lên dùng chung. Dùng cho một job thì nó chỉ thêm một lớp gián tiếp: người đọc phải nhảy qua lại giữa hai chỗ trong tệp mà không đổi lại được gì.

**Đừng suy quy tắc ba nấc sang cho `variables`.** Đó là bộ quy tắc khác, chín nguồn, và buổi 06 xử lý riêng.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy | Vì sao dính | Làm đúng là |
|---|---|---|---|
| 1 | Tưởng `stage` chuyển dữ liệu giữa các job | Mặc định tải artifact của mọi job stage trước tạo cảm giác đó | Dữ liệu đi bằng `artifacts` (QT 5.1). `stage` chuyển **0 byte** |
| 2 | Tưởng job cùng stage **luôn** chạy song song | Giao diện vẽ chúng cạnh nhau | Phụ thuộc `concurrent` (QT 5.2). Đo bằng chồng lấn `started_at`/`finished_at` |
| 3 | Gõ `scripts:` thay `script:` | GitLab không báo lỗi | Nó tạo **job rác**. Kiểm bằng `ci/lint` (QT 4.1, 4.3) |
| 4 | Gõ `stages:` trong một job thay `stage:` | Tên gần giống | Job rơi vào stage mặc định `test`. Kiểm bằng `ci/lint` |
| 5 | Thêm stage cho "gọn gàng" | Trông có tổ chức hơn | Mỗi stage cộng thêm một hàng rào bằng job chậm nhất stage trước (QT 5.3) |
| 6 | Đọc YAML thô để đoán hành vi | Tệp ngay trước mặt | Gọi `ci/lint` — nó cho tệp **sau phân giải** (QT 4.3) |
| 7 | `cd` ở dòng 3 rồi ghi tệp ở dòng 7 | Tưởng mỗi dòng là một lệnh độc lập | `cd` xuyên dòng (QT 6.2). Dùng `$CI_PROJECT_DIR` hoặc subshell |
| 8 | Đặt biến ở `script`, đọc ở `after_script` | Tưởng cùng shell | 3 khối, **2** shell (QT 6.1, buổi 01 QT 4.3) |
| 9 | Viết `- echo ket qua: xong` không bọc nháy | Nhìn như một câu lệnh bình thường | YAML hiểu `:` là ánh xạ (QT 6.3). Bọc nháy đơn |
| 10 | Dùng `>` khi cần giữ xuống dòng | Hai ký hiệu trông giống nhau | `>` **gộp** dòng; `\|` **giữ** dòng |
| 11 | Quên dấu chấm ở job khuôn mẫu | Dễ sót | Không có `.` thì khuôn mẫu **chạy thật** và thường đỏ (QT 4.2) |
| 12 | Khai `before_script` trong job rồi mong nó nối vào cái ở `default` | Trực giác nói là "thêm vào" | Nấc gần hơn **thay thế**, không hợp nhất (QT 7.1) |
| 13 | Suy quy tắc ba nấc sang cho `variables` | Chúng nằm cạnh nhau trong tệp | `variables` có **9** nguồn và quy tắc riêng (QT 7.2), buổi 06 |
| 14 | Khai thêm stage `truoc-tien` ở đầu mọi project | Không biết `.pre` tồn tại | `.pre` và `.post` có sẵn, không cần khai (QT 5.4) |

---

### 1.7. Tóm tắt

```mermaid
graph TD
    LD["LUẬN ĐỀ: stage là ràng buộc THỨ TỰ, không phải ràng buộc DỮ LIỆU"]

    LD --> A["§4 GIẢI PHẪU TỆP<br/>QT 4.1 khoá không dành riêng = một JOB<br/>QT 4.2 dấu chấm = job ẩn<br/>QT 4.3 ci/lint cho tệp SAU phân giải"]
    LD --> B["§5 HAI NỬA CỦA LUẬN ĐỀ<br/>QT 5.1 stage chuyển 0 byte<br/>QT 5.2 song song do concurrent<br/>QT 5.3 hàng rào = job chậm nhất stage trước<br/>QT 5.4 .pre và .post có sẵn"]
    LD --> C["§6 SCRIPT<br/>QT 6.1 ba khối, HAI shell<br/>QT 6.2 cd xuyên dòng<br/>QT 6.3 YAML nuốt ký tự"]
    LD --> D["§7 THỨ TỰ ƯU TIÊN<br/>QT 7.1 ba nấc, gần job nhất thắng, THAY THẾ<br/>QT 7.2 variables có quy tắc RIÊNG"]

    B --> KQ["LÃNG PHÍ HÀNG RÀO<br/>= tổng thời gian − đường găng dữ liệu<br/>đo được bằng GIÂY"]
    A --> KQ
    KQ --> VT["§8 ĐƯA VÀO VIỆC THẬT<br/>ci/lint tìm job rác · đo lãng phí<br/>bảng 'job này cần artifact của ai'"]
    VT --> B08["→ ĐẦU VÀO TRỰC TIẾP CỦA BUỔI 08 (needs)"]

    C -.dùng lại.-> B16["buổi 07 gỡ rối · 16–21 mọi buổi ngôn ngữ"]
    D -.dùng lại.-> B06["buổi 06 biến · 10 extends · 11 component"]
    A -.dùng lại.-> B10["buổi 10 include · 11 catalog · 44 template"]
```

**Năm điều phải nhớ sau buổi học:**

1. **Khoá cấp trên cùng không dành riêng là một job.** Gõ sai không báo lỗi — nó tạo job rác và làm mất cấu hình thật.
2. **`stage` chuyển 0 byte.** Dữ liệu đi bằng `artifacts`.
3. **`stage` không đảm bảo song song.** Với `concurrent = 1`, thời gian stage bằng **tổng**, không bằng **max**.
4. **Lãng phí hàng rào = tổng thời gian − đường găng dữ liệu.** Đó là số giây lấy lại được, và buổi 08 lấy nó.
5. **Ba nấc ưu tiên, gần job nhất thắng, và nó THAY THẾ chứ không hợp nhất.** Trừ `variables` — nó có quy tắc riêng.

---

### 1.8. Câu hỏi tự kiểm tra

1. Trong tệp dưới đây có bao nhiêu job? `stages`, `variables`, `build`, `test`, `varaibles`, `.mau`.
2. Gõ `scripts:` thay vì `script:` trong một job thì chuyện gì xảy ra? Ô nào của bảng hai thuộc tính?
3. Làm sao phát hiện job rác **trước khi** đẩy commit? Viết lệnh.
4. `stage` chuyển bao nhiêu byte dữ liệu giữa hai job? Cái gì mới chuyển dữ liệu?
5. Một stage có 6 job, mỗi job 30 giây. Stage mất bao lâu? Nêu **hai** trường hợp cho hai đáp số khác nhau.
6. Định nghĩa "lãng phí hàng rào" bằng một phép tính.
7. Pipeline: `build` (10s, sinh artifact) → `test-nhanh` (5s) và `test-cham` (60s) → `dong-goi` (2s, chỉ cần artifact của `build`). Tổng thời gian? Đường găng dữ liệu? Lãng phí?
8. `.pre` và `.post` là gì? Nêu một việc nên đặt ở mỗi cái.
9. Ba khối lệnh chạy trong mấy shell? Cái nào chung, cái nào riêng?
10. `cd sau` ở dòng 2, ghi tệp `dist/app.js` ở dòng 3, `artifacts:paths: [dist/]`. Job xanh hay đỏ, và artifact có gì?
11. Viết một dòng `script` in ra chuỗi `ket qua: xong` mà không làm YAML hiểu sai.
12. Phân biệt chuỗi khối `|` và `>` bằng một câu, kèm một ca dùng mỗi cái.
13. `image` khai ở `config.toml`, ở `default:`, và trong job. Cái nào thắng? Nó thay thế hay hợp nhất?
14. Khai `before_script` ở `default:` và cũng khai trong một job. Job đó chạy mấy `before_script`?
15. Vì sao không được suy quy tắc ba nấc sang cho `variables`?

### Đáp án

1. **Bốn job**: `build`, `test`, `varaibles` (gõ sai `variables` → thành job), và `.mau` — nhưng `.mau` là **job ẩn** nên không chạy. Vậy **ba job chạy**. `stages` và `variables` là từ khoá dành riêng (QT 4.1, 4.2).
2. GitLab tạo một job tên `scripts` bên trong job đó — thực ra `scripts` ở cấp job là khoá không hợp lệ và `ci/lint` sẽ báo. Nếu gõ sai ở **cấp trên cùng** thì nó thành một job riêng. Ô **im lặng, không chặn** — job rác thường xanh và cấu hình thật bị mất không có thông báo (QT 4.1).
3. `curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" --header "Content-Type: application/json" --data "$(jq -Rs '{content: .}' < .gitlab-ci.yml)" "$GITLAB/api/v4/projects/$PID/ci/lint" | jq -r '.jobs[].name'` — rồi so danh sách với danh sách mình nghĩ là có (QT 4.3).
4. **0 byte.** `artifacts` chuyển dữ liệu; `stage` chỉ là hàng rào thời gian (QT 5.1).
5. Với `concurrent >= 6` và đủ runner: khoảng **30 giây** (song song). Với `concurrent = 1`: **180 giây** (tuần tự). `stage` chỉ **cho phép** song song, `concurrent` mới quyết định (QT 5.2).
6. `lãng phí hàng rào = tổng thời gian pipeline − đường găng dữ liệu thật`, trong đó đường găng dữ liệu là chuỗi phụ thuộc `artifacts` dài nhất (QT 5.3).
7. Tổng ≈ 10 + 60 + 2 = **72 giây** (`dong-goi` chờ `test-cham`). Đường găng dữ liệu = 10 + 2 = **12 giây**. Lãng phí ≈ **60 giây**. Buổi 08 lấy lại 60 giây ấy bằng `needs`.
8. Hai stage **luôn tồn tại**, không cần khai: `.pre` chạy trước mọi stage, `.post` sau mọi stage. Ví dụ: quét secret bằng Gitleaks ở `.pre` (buổi 29); thu thập số liệu DORA ở `.post` (buổi 46) (QT 5.4).
9. **Hai** shell. `before_script` và `script` chung một shell; `after_script` shell riêng — để nó vẫn chạy được khi `script` đã chết (QT 6.1).
10. Job **xanh**, artifact **rỗng**. `cd` ở dòng 2 làm tệp thật ra nằm ở `sau/dist/app.js`, còn `artifacts:paths` trỏ `dist/` ở gốc — mẫu không khớp gì nên gói rỗng mà pha upload vẫn thành công. Ô im lặng + không chặn (QT 6.2).
11. `- 'echo "ket qua: xong"'` — bọc toàn bộ trong nháy đơn (QT 6.3).
12. `|` **giữ** ký tự xuống dòng, `>` **gộp** các dòng thành một. Dùng `|` cho khối `if`/`for` nhiều dòng; dùng `>` cho một lệnh dài như `docker build` có nhiều tham số.
13. **Trong job** thắng, vì nó gần job nhất. Nó **thay thế** hoàn toàn, không hợp nhất (QT 7.1).
14. **Một** — cái khai trong job. Cái ở `default:` bị bỏ hoàn toàn, không nối vào (QT 7.1).
15. Vì biến đến từ **chín** nguồn khác nhau (instance, group, project, tệp, job, `dotenv`, biến hệ thống, nhập tay, pipeline cha), có thứ tự ưu tiên riêng và còn có cờ `protected`/`masked` chen vào. Buổi 06 xử lý đầy đủ (QT 7.2).

---

## §12. Tài liệu tham khảo

| Nguồn | Loại | Phiên bản |
|---|---|---|
| GitLab Docs — *CI/CD YAML syntax reference*, mục *Keywords* và *Global keywords* | (a) tài liệu chính thức | 17.7 |
| GitLab Docs — *`stages`*, *`stage`*, *`.pre` and `.post`* | (a) | 17.7 |
| GitLab Docs — *`default`*, và mục về thứ tự ưu tiên | (a) | 17.7 |
| GitLab Docs — *Hidden jobs* và *`extends`* | (a) | 17.7 |
| GitLab API — `POST /projects/:id/ci/lint` (`include_merged_yaml`) | (a) | v4 |
| Đặc tả YAML 1.2 — chuỗi khối `\|` và `>`, ký tự chỉ báo | (a) | YAML 1.2 |
| Hành vi khi gõ sai khoá; `before_script` cùng shell với `script`; `cd` xuyên dòng; nấc nào thắng | (c) **phải đo** | Lab bước 1, 4, 5 |
| Quy tắc "lệnh dài quá một dòng thì dùng chuỗi khối `\|`" | (c) kinh nghiệm thực tế | — |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10' |
| §1 | Sau buổi này học viên làm được gì | 1' |
| §2 | Cần biết trước | 1' |
| §3 | Thuật ngữ và mô hình tư duy | 8' |
| §4 | Giải phẫu một tệp: cái gì là job, cái gì không | 9' |
| §5 | `stage` là ràng buộc thứ tự, không phải ràng buộc dữ liệu | 11' |
| §6 | `script`: ba khối lệnh, hai shell, YAML nuốt ký tự | 9' |
| §7 | Thứ tự ưu tiên: `config.toml` → `default` → job | 5' |
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
> **Bước 3 đụng `config.toml`** — sao lưu ở §L1, khôi phục ở §L8, giống quy trình buổi 02.

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| # | Mục tiêu | Tiêu chí hoàn thành (kiểm chứng được bằng lệnh) |
|---|---|---|
| TH1 | Gọi được `ci/lint` và đọc danh sách job sau phân giải | `lint` trả về `valid: true` và liệt kê job |
| TH2 | **Đo QT 4.1** — gõ sai khoá cấp trên cùng thì GitLab làm gì | `job-rac.md` ghi tên job rác GitLab sinh ra |
| TH3 | Kiểm chứng QT 4.2 — job ẩn không chạy | Job `.mau` không có trong danh sách job của pipeline |
| TH4 | Kiểm chứng QT 5.1 — `stage` chuyển 0 byte | Job `test-thieu-artifact` **đỏ**, job `test-co-artifact` **xanh** |
| TH5 | **Đo QT 5.3** — lãng phí hàng rào bằng giây | `lang-phi-hang-rao.tsv` có cả ba số: tổng, đường găng, hiệu |
| TH6 | Kiểm chứng QT 5.4 — `.pre` chạy trước mọi stage | `started_at` của job `.pre` nhỏ hơn mọi job khác |
| TH7 | **Đo QT 5.2** — song song trong stage phụ thuộc `concurrent` | Cùng pipeline, hai mức `concurrent`, hai giá trị song song đo được |
| TH8 | **Đo QT 6.1** — `before_script` và `script` có cùng shell không | `hanh-vi-script.txt` ghi kết quả **kèm phiên bản runner** |
| TH9 | Kiểm chứng QT 6.2 — `cd` xuyên dòng làm artifact rỗng mà job xanh | Job xanh **và** `artifacts_file.size` dưới 200 byte |
| TH10 | Kiểm chứng QT 6.3 — YAML nuốt ký tự | `ci/lint` trả `valid: false` cho bản sai, `true` cho bản bọc nháy |
| TH11 | **Đo QT 7.1** — ba nấc ưu tiên, nấc nào thắng | `thu-tu-uu-tien.tsv` có 3 dòng, mỗi dòng ghi image thực tế |
| TH12 | Nộp hiện vật và khôi phục `config.toml` | `kiem-hien-vat.sh` in ĐẠT; `config.toml` khớp bản sao lưu |

**Sản phẩm cuối buổi:** `gitlab-portfolio/03-cu-phap-yaml-va-stage/` gồm `job-rac.md`, `lang-phi-hang-rao.tsv`, `do-song-song-stage.tsv`, `hanh-vi-script.txt`, `thu-tu-uu-tien.tsv`, `ban-do-phu-thuoc.md` (bảng "job này cần artifact của ai"), `.gitlab-ci.yml`, `checkpoint.log`.

---

## L1. Điều kiện tiên quyết về môi trường

| # | Kiểm tra | Lệnh | Kết quả kỳ vọng |
|---|---|---|---|
| 1 | Đã nạp biến môi trường lab | `echo "$GITLAB" "$GITLAB_TOKEN" \| wc -w` | `2` |
| 2 | GitLab sẵn sàng | `curl -sf -o /dev/null -w '%{http_code}\n' "$GITLAB/-/readiness"` | `200` |
| 3 | Runner online và nhận job không tag | (đoạn kiểm ba điều kiện của buổi 02 §L1) | ít nhất 1 runner `online=true run_untagged=true` |
| 4 | **Có `jq` phiên bản hỗ trợ `-Rs`** | `echo x \| jq -Rs '{content: .}' \| jq -r .content` | in ra `x` |
| 5 | Đã học buổi 01 và 02 | (tự kiểm) phát biểu được bốn đường vào và `concurrent` là gì | Bắt buộc — §5 dựng thẳng lên cả hai |
| 6 | Bộ nhớ trống | `free -g \| awk '/Mem:/{print $7}'` | `>= 3` |
| 7 | Số lõi CPU | `nproc` | ghi vào hiện vật |
| 8 | Chưa có project lab 03 | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects?search=lab03-cu-phap" \| jq length` | `0` |
| 9 | `docker exec` vào runner được | `docker exec lab-runner gitlab-runner --version \| head -1` | in ra phiên bản |

### Sao lưu bắt buộc

Bước 3 sửa `concurrent`. Sao lưu như buổi 02 — hạ tầng dùng chung (buổi 02 QT 4.3):

```bash
source ~/.gitlab-lab.env
docker exec lab-runner sh -c \
  'cp /etc/gitlab-runner/config.toml /etc/gitlab-runner/config.toml.buoi03.bak'
docker exec lab-runner sh -c 'grep -E "^concurrent" /etc/gitlab-runner/config.toml'
```

**Cảnh báo về mức độ tác động.** Bài lab tạo project `lab03-cu-phap` và sửa `concurrent` **hai lần** ở bước 3. Trên lớp đông dùng chung một runner, chỉ giảng viên chạy bước 3; học viên ghi số chung. §L8 khôi phục.

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    HV["Học viên"]
    HV -->|"POST ci/lint — KHÔNG đẩy commit"| LINT["API ci/lint<br/>trả về tệp SAU PHÂN GIẢI<br/>1 giây thay cho 3–5 phút"]
    HV -->|"git push"| PRJ["Project lab03-cu-phap"]
    HV -->|"curl + jq"| API["API GitLab v4"]
    HV -->|"docker exec"| CFG["config.toml — concurrent"]

    LINT --> B1["Bước 1: giải phẫu tệp<br/>gõ sai khoá → JOB RÁC<br/>job ẩn không chạy"]
    LINT --> B4B["Bước 4: YAML nuốt ký tự<br/>valid=false trước, true sau"]

    PRJ --> API
    API --> B2["Bước 2: stage chuyển 0 byte<br/>+ ĐO LÃNG PHÍ HÀNG RÀO<br/>tổng − đường găng = hiệu"]
    CFG --> B3["Bước 3: cùng pipeline, hai mức concurrent<br/>→ song song KHÔNG do stage"]
    API --> B4["Bước 4: ba khối, hai shell<br/>cd xuyên dòng → artifact rỗng, job XANH"]
    API --> B5["Bước 5: ba nấc ưu tiên<br/>config.toml → default → job"]

    B2 --> BD["ban-do-phu-thuoc.md<br/>'job này cần artifact của ai'<br/>→ ĐẦU VÀO TRỰC TIẾP CỦA BUỔI 08"]
```

**Bốn quyết định thiết kế:**

1. **Bước 1 dùng `ci/lint` thay vì đẩy commit.** Vòng đẩy-chờ-xem mất 3–5 phút; `ci/lint` mất 1 giây. Bài lab bắt học viên quen công cụ này ngay ở buổi có cú pháp, vì từ buổi 10 (`include`, `extends`) đọc YAML thô để đoán hành vi không còn khả thi. Phương án hiển nhiên — đẩy commit rồi xem — cũng cho kết quả, nhưng nó dạy sai thói quen và tốn 60 lần thời gian.

2. **Đo lãng phí hàng rào bằng hiệu của hai con số**, không bằng cảm nhận: tổng thời gian pipeline trừ đường găng dữ liệu thật. Hiệu ấy là con số học viên mang về áp vào repo mình, và là đầu vào trực tiếp của buổi 08. Nói "pipeline chậm vì nhiều stage" mà không có hiệu số thì không thuyết phục được ai.

3. **Bước 3 tái dùng đúng hàm `song_song_toi_da` của buổi 02.** Dùng lại công cụ cũ cho một câu hỏi mới cho học viên thấy hai buổi nối vào nhau — `stage` thuộc tệp thứ nhất, `concurrent` thuộc tệp thứ hai, và câu trả lời chỉ có khi ghép cả hai.

4. **Bước 4 đo ba hành vi shell trong MỘT job duy nhất.** Ba phép đo chung một job thì chia sẻ cùng môi trường nên so sánh được với nhau. Tách ba job cho ba kết quả không so được, vì mỗi job có container riêng.

**Ca đối chứng PHẢI THẤT BẠI — báo trước cho lớp.** Bước 2 có job `test-thieu-artifact` **đỏ** vì tưởng `stage` chuyển dữ liệu. Bước 4 có job `build-cd-sai` **xanh nhưng artifact rỗng**. Cả hai là kết quả đúng.

---

## L3. Bước 1 — Giải phẫu tệp bằng `ci/lint` (30 phút)

### 3.1. Tạo project và hàm `lint` (8 phút)

```bash
source ~/.gitlab-lab.env
export HAU_TO="${USER}"
mkdir -p ~/lab03 && cd ~/lab03

PID3=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{\"name\":\"lab03-cu-phap-${HAU_TO}\",\"visibility\":\"internal\"}" \
  "$GITLAB/api/v4/projects" | jq -r .id)
echo "PID3=$PID3"
```

```bash
cat > ~/lab03/cong-cu.sh <<'SH'
#!/usr/bin/env bash
# Bộ công cụ lab buổi 03. Nạp: source ~/lab03/cong-cu.sh
: "${GITLAB:?}"; : "${GITLAB_TOKEN:?}"; : "${PID3:?}"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")

# HÀM QUAN TRỌNG NHẤT CỦA BUỔI: đọc tệp SAU PHÂN GIẢI, không đẩy commit
lint() {
  curl -sf --request POST "${H[@]}" --header "Content-Type: application/json" \
    --data "$(jq -Rs '{content: ., include_merged_yaml: true}' < "${1:-.gitlab-ci.yml}")" \
    "$GITLAB/api/v4/projects/$PID3/ci/lint"
}
lint_job() { lint "${1:-.gitlab-ci.yml}" | jq -r '.jobs[]?.name'; }
lint_loi() { lint "${1:-.gitlab-ci.yml}" | jq -r '.valid, (.errors[]?), (.warnings[]?)'; }

day() {
  git add -A >/dev/null; git commit -q -m "${1:-cap nhat}" --allow-empty
  git push -q origin HEAD 2>/dev/null; sleep 4
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/pipelines?per_page=1" | jq -r '.[0].id'
}
cho_pipeline() {
  local pipe="$1" han="${2:-420}" t=0 st
  while [ "$t" -lt "$han" ]; do
    st=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/pipelines/$pipe" | jq -r .status)
    case "$st" in success|failed|canceled|skipped) echo "$st"; return 0 ;; esac
    sleep 5; t=$((t+5))
  done
  echo "$st"
}
job_bang() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/pipelines/$1/jobs?per_page=100" \
  | jq -r '.[] | [.name, .stage, .status, (.duration//0)] | @tsv'
}
job_id() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/pipelines/$1/jobs?per_page=100" \
  | jq -r --arg n "$2" '.[] | select(.name==$n) | .id' | head -1
}
job_log() { curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$1/trace" \
            | sed 's/\x1b\[[0-9;K]*[a-zA-Z]//g'; }

# Kỹ thuật của BUỔI 02 — dùng lại nguyên vẹn
song_song_toi_da() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/pipelines/$1/jobs?per_page=100" \
  | jq -r '[ .[] | select(.started_at != null and .finished_at != null)
             | {s: (.started_at|fromdateiso8601), f: (.finished_at|fromdateiso8601)} ] as $j
           | [ $j[].s ] | map( . as $t | [ $j[] | select(.s <= $t and .f > $t) ] | length ) | max // 0'
}
tong_dong_ho() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/pipelines/$1/jobs?per_page=100" \
  | jq -r '[ .[] | select(.started_at != null and .finished_at != null) ] as $j
           | if ($j|length)==0 then 0
             else (([$j[].finished_at|fromdateiso8601]|max) - ([$j[].started_at|fromdateiso8601]|min)) end'
}
SH
source ~/lab03/cong-cu.sh

git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3" | jq -r .path_with_namespace).git"
git config user.email "hocvien@lab.local"; git config user.name "hoc vien"
```

### 3.2. Đo QT 4.1 — gõ sai khoá thì GitLab làm gì (12 phút)

Đại lượng loại (c). Đo bằng `ci/lint`, **không đẩy commit**.

```yaml
# ~/lab03/.gitlab-ci.yml
stages: [build, test]

variabels:                 # ← gõ sai `variables`
  MOI_TRUONG: "dev"

stgaes: [a, b]             # ← gõ sai `stages`

.mau-an:                   # ← job ẩn, KHÔNG chạy
  image: alpine:3.20
  before_script: [echo "khuon mau"]

build:
  stage: build
  image: alpine:3.20
  script: [echo "build"]

test:
  extends: .mau-an
  stage: test
  script: [echo "MOI_TRUONG=[$MOI_TRUONG]"]
```

```bash
cd ~/lab03
echo "=== TỆP CÓ HỢP LỆ KHÔNG ==="
lint_loi
echo "=== DANH SÁCH JOB SAU PHÂN GIẢI ==="
lint_job
```

Ghi hiện vật:

```bash
{
  echo "# QT 4.1 — gõ sai khoá cấp trên cùng thì GitLab làm gì? ĐO bằng ci/lint."
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
  echo "# Ngày đo: $(date -Iseconds)"
  echo
  echo "## Tệp có hợp lệ không"
  lint | jq -r '"valid = \(.valid)"'
  echo
  echo "## Danh sách job GitLab sinh ra"
  lint_job | sed 's/^/  - /'
  echo
  echo "## Job tôi ĐỊNH tạo: build, test"
  echo "## Job RÁC (chênh lệch):"
  comm -23 <(lint_job | sort) <(printf 'build\ntest\n' | sort) | sed 's/^/  - /'
} | tee ~/lab03/job-rac.md
```

**CHECKPOINT 1 — `ci/lint` gọi được và trả về danh sách job.**

```bash
v=$(lint | jq -r '.valid')
n=$(lint_job | grep -c . || true)
{ [ -n "$v" ] && [ "$n" -ge 2 ]; } \
  && echo "CHECKPOINT 1 — ĐẠT (valid=$v, $n job sau phân giải)" \
  || echo "CHECKPOINT 1 — LỖI (valid=$v, job=$n)"
```

**CHECKPOINT 2 — phát hiện được ít nhất một job rác do gõ sai khoá.**

```bash
rac=$(comm -23 <(lint_job | sort) <(printf 'build\ntest\n' | sort) | grep -c . || true)
[ "$rac" -ge 1 ] \
  && echo "CHECKPOINT 2 — ĐẠT ($rac job rác: $(comm -23 <(lint_job|sort) <(printf 'build\ntest\n'|sort) | tr '\n' ' '))" \
  || echo "CHECKPOINT 2 — LỖI (không phát hiện job rác nào — kiểm lại tệp)"
```

**Ba câu hỏi phải trả lời, ghi vào `job-rac.md`:**

1. Tệp có `valid: true` không, dù có hai lỗi chính tả? Điều đó nói gì về việc dựa vào `ci/lint` để bắt lỗi chính tả?
2. Job `test` in ra `MOI_TRUONG=[...]` là gì? Vì sao?
3. Job `.mau-an` có xuất hiện trong danh sách không? Điều đó khớp QT 4.2 chỗ nào?

### 3.3. Sửa và kiểm chứng job ẩn (10 phút)

```bash
cd ~/lab03
sed -i 's/^variabels:/variables:/' .gitlab-ci.yml
sed -i '/^stgaes: \[a, b\]$/d' .gitlab-ci.yml
lint_job
P1=$(day "buoc 1: sua khoa go sai"); cho_pipeline "$P1"
job_bang "$P1"
```

**CHECKPOINT 3 — sau khi sửa, pipeline có đúng 2 job và job ẩn không chạy.**

```bash
n=$(job_bang "$P1" | wc -l)
an=$(job_bang "$P1" | grep -c 'mau-an' || true)
bien=$(job_log "$(job_id "$P1" test)" | grep -c 'MOI_TRUONG=\[dev\]' || true)
{ [ "$n" -eq 2 ] && [ "$an" -eq 0 ] && [ "$bien" -ge 1 ]; } \
  && echo "CHECKPOINT 3 — ĐẠT (2 job, job ẩn không chạy, biến có giá trị dev)" \
  || echo "CHECKPOINT 3 — LỖI (job=$n, job ẩn=$an, biến đúng=$bien)"
```

---

## L4. Bước 2 — `stage` chuyển 0 byte; đo lãng phí hàng rào (30 phút)

### 4.1. `stage` không chuyển dữ liệu (10 phút)

Kiểm chứng QT 5.1. **Job `test-thieu-artifact` sẽ đỏ — đó là kết quả đúng.**

```yaml
# ~/lab03/.gitlab-ci.yml — thay toàn bộ
stages: [build, test]

build-khong-artifact:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p dist && echo "console.log(1)" > dist/app.js
    - echo "job build da tao tep:" && ls -la dist/

build-co-artifact:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p ra && echo "console.log(2)" > ra/app.js
  artifacts:
    paths: [ra/]
    expire_in: 1 hour

test-thieu-artifact:
  stage: test
  image: alpine:3.20
  script:
    - cat dist/app.js        # ĐỎ — stage chuyển 0 byte

test-co-artifact:
  stage: test
  image: alpine:3.20
  script:
    - test -s ra/app.js || { echo "KHANG DINH HONG: khong co ra/app.js"; exit 1; }
    - cat ra/app.js          # XANH — artifact mới chuyển dữ liệu
```

```bash
cd ~/lab03
P2=$(day "buoc 2a: stage chuyen 0 byte"); cho_pipeline "$P2"
job_bang "$P2"
```

**CHECKPOINT 4 — `test-thieu-artifact` ĐỎ, `test-co-artifact` XANH.**

```bash
s1=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$(job_id "$P2" test-thieu-artifact)" | jq -r .status)
s2=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$(job_id "$P2" test-co-artifact)" | jq -r .status)
loi=$(job_log "$(job_id "$P2" test-thieu-artifact)" | grep -c 'No such file' || true)
{ [ "$s1" = failed ] && [ "$s2" = success ] && [ "$loi" -ge 1 ]; } \
  && echo "CHECKPOINT 4 — ĐẠT (thiếu artifact=$s1, có artifact=$s2 → stage chuyển 0 byte)" \
  || echo "CHECKPOINT 4 — LỖI ($s1 / $s2 / loi=$loi)"
```

### 4.2. Đo lãng phí hàng rào (14 phút)

Kiểm chứng và **định lượng** QT 5.3. Đây là con số học viên mang về áp vào repo thật.

```yaml
# ~/lab03/.gitlab-ci.yml — thay toàn bộ
stages: [build, test, dong-goi]

kiem-truoc:
  stage: .pre                # kiểm chứng QT 5.4
  image: alpine:3.20
  script: [echo "chay TRUOC moi stage"]

build:
  stage: build
  image: alpine:3.20
  script:
    - sleep 10
    - mkdir -p dist && echo "console.log(1)" > dist/app.js
  artifacts:
    paths: [dist/]
    expire_in: 1 hour

test-nhanh:
  stage: test
  image: alpine:3.20
  dependencies: []
  script: [sleep 5]

test-cham:                   # 60 giây; KHÔNG job nào sau nó cần artifact của nó
  stage: test
  image: alpine:3.20
  dependencies: []
  script: [sleep 60]

dong-goi:
  stage: dong-goi
  image: alpine:3.20
  script:
    - test -s dist/app.js || { echo "KHANG DINH HONG"; exit 1; }
    - echo "dong goi xong"
```

```bash
cd ~/lab03
P3=$(day "buoc 2b: do lang phi hang rao"); cho_pipeline "$P3" 300
job_bang "$P3"

TONG=$(tong_dong_ho "$P3")
D_BUILD=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$(job_id "$P3" build)" | jq -r '.duration|floor')
D_DG=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$(job_id "$P3" dong-goi)" | jq -r '.duration|floor')
GANG=$((D_BUILD + D_DG))

{
  echo "# QT 5.3 — LÃNG PHÍ HÀNG RÀO. Đo trên pipeline $P3."
  echo "# nproc = $(nproc)"
  echo "# Đường găng DỮ LIỆU = build -> dong-goi (dong-goi chỉ cần artifact của build)"
  echo -e "dai_luong\tgiay"
  echo -e "tong_thoi_gian_pipeline\t$TONG"
  echo -e "duong_gang_du_lieu\t$GANG"
  echo -e "lang_phi_hang_rao\t$((TONG - GANG))"
  echo "# lang_phi = tong - duong_gang. Buổi 08 lấy lại con số này bằng needs."
} | tee ~/lab03/lang-phi-hang-rao.tsv
```

**CHECKPOINT 5 — lãng phí hàng rào đo được và lớn hơn 30 giây.**

```bash
LP=$(awk -F'\t' '/^lang_phi_hang_rao/{print int($2)}' ~/lab03/lang-phi-hang-rao.tsv)
{ [ -n "$LP" ] && [ "$LP" -ge 30 ]; } \
  && echo "CHECKPOINT 5 — ĐẠT (lãng phí hàng rào = ${LP}s; dong-goi chờ test-cham vô ích)" \
  || echo "CHECKPOINT 5 — LỖI (lãng phí = ${LP}s, kỳ vọng >= 30s)"
```

**CHECKPOINT 6 — job ở `.pre` bắt đầu trước mọi job khác.**

```bash
T_PRE=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$(job_id "$P3" kiem-truoc)" | jq -r '.started_at|fromdateiso8601')
T_MIN=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/pipelines/$P3/jobs?per_page=100" \
        | jq -r '[.[] | select(.name!="kiem-truoc" and .started_at!=null) | (.started_at|fromdateiso8601)] | min')
{ [ -n "$T_PRE" ] && [ -n "$T_MIN" ] && [ "$T_PRE" -le "$T_MIN" ]; } \
  && echo "CHECKPOINT 6 — ĐẠT (.pre bắt đầu trước mọi job khác)" \
  || echo "CHECKPOINT 6 — LỖI (pre=$T_PRE, min khác=$T_MIN)"
```

### 4.3. Bản đồ phụ thuộc — đầu vào của buổi 08 (6 phút)

Ghi `ban-do-phu-thuoc.md`. Đây là hiện vật có giá trị dài hạn nhất của buổi.

| Job | Stage | Nó cần artifact của ai | Nó **thực sự** phải chờ ai | Chênh lệch |
|---|---|---|---|---|
| `build` | build | — | — | — |
| `test-nhanh` | test | không ai | không ai | chờ `build` **vô ích** |
| `test-cham` | test | không ai | không ai | chờ `build` **vô ích** |
| `dong-goi` | dong-goi | `build` | `build` | chờ `test-cham` **vô ích 60 giây** |

**Hai câu hỏi phải trả lời:** (1) nếu bỏ được mọi hàng rào vô ích, pipeline này mất bao lâu? (2) Với repo thật của mình, lập bảng tương tự cho ít nhất **5 job** — đây cũng là BTVN 1.

---

## L5. Bước 3 — Song song trong stage phụ thuộc `concurrent` (30 phút)

Kiểm chứng QT 5.2, ghép buổi 02 QT 6.1 với buổi 03 QT 5.1.

```yaml
# ~/lab03/.gitlab-ci.yml — thay toàn bộ
stages: [song-song]
.mau:
  stage: song-song
  image: alpine:3.20
  dependencies: []
  script: [sleep 20]

s1: {extends: .mau}
s2: {extends: .mau}
s3: {extends: .mau}
s4: {extends: .mau}
s5: {extends: .mau}
s6: {extends: .mau}
```

Sáu job **cùng một stage**. Chạy ở hai mức `concurrent`:

```bash
cd ~/lab03
git add -A && git commit -q -m "buoc 3: sau job cung stage" --allow-empty && git push -q origin HEAD

echo -e "concurrent\tsong_song_do_duoc\ttong_dong_ho_s\tky_vong_neu_song_song" > ~/lab03/do-song-song-stage.tsv

for C in 1 6; do
  docker exec lab-runner sh -c "sed -i 's/^concurrent.*/concurrent = $C/' /etc/gitlab-runner/config.toml"
  # Nếu buổi 02 kết luận PHẢI KHỞI ĐỘNG LẠI thì bỏ comment dòng dưới
  # docker restart lab-runner >/dev/null && sleep 20
  sleep 15
  P=$(day "sau job cung stage, concurrent=$C")
  cho_pipeline "$P" 400 >/dev/null
  SS=$(song_song_toi_da "$P"); TT=$(tong_dong_ho "$P")
  echo -e "$C\t$SS\t$TT\t~20" | tee -a ~/lab03/do-song-song-stage.tsv
done
echo "# nproc = $(nproc)" >> ~/lab03/do-song-song-stage.tsv
cat ~/lab03/do-song-song-stage.tsv
```

**CHECKPOINT 7 — với `concurrent = 1`, sáu job cùng stage chạy TUẦN TỰ.**

```bash
SS1=$(awk -F'\t' '$1=="1"{print int($2)}' ~/lab03/do-song-song-stage.tsv)
TT1=$(awk -F'\t' '$1=="1"{print int($3)}' ~/lab03/do-song-song-stage.tsv)
{ [ "${SS1:-9}" -eq 1 ] && [ "${TT1:-0}" -ge 100 ]; } \
  && echo "CHECKPOINT 7 — ĐẠT (concurrent=1: song song=$SS1, tổng=${TT1}s ≈ TỔNG chứ không phải MAX)" \
  || echo "CHECKPOINT 7 — LỖI (song song=$SS1, tổng=${TT1}s)"
```

**CHECKPOINT 8 — với `concurrent = 6`, sáu job chạy song song và tổng thời gian giảm mạnh.**

```bash
SS6=$(awk -F'\t' '$1=="6"{print int($2)}' ~/lab03/do-song-song-stage.tsv)
TT6=$(awk -F'\t' '$1=="6"{print int($3)}' ~/lab03/do-song-song-stage.tsv)
{ [ "${SS6:-0}" -ge 2 ] && [ "${TT6:-999}" -lt "${TT1:-0}" ]; } \
  && echo "CHECKPOINT 8 — ĐẠT (concurrent=6: song song=$SS6, tổng=${TT6}s < ${TT1}s)" \
  || echo "CHECKPOINT 8 — LỖI (song song=$SS6, tổng=${TT6}s so ${TT1}s)"
```

**Ba câu hỏi phải trả lời, ghi vào `do-song-song-stage.tsv`:**

1. Cùng một tệp `.gitlab-ci.yml`, cùng một `stage` — vì sao hai kết quả khác nhau? Tệp nào đã đổi?
2. Với `concurrent = 1`, thời gian stage bằng **tổng** hay bằng **max** thời lượng sáu job? Con số đo được là bao nhiêu?
3. Nếu một người nói "tôi đặt sáu job cùng stage cho nó chạy song song", câu hỏi ngược lại của bạn là gì?

Đặt `concurrent` về mức làm việc trước khi sang bước 4:

```bash
docker exec lab-runner sh -c "sed -i 's/^concurrent.*/concurrent = 4/' /etc/gitlab-runner/config.toml"
sleep 15
```

---

## L6. Bước 4 — Ba khối, hai shell; `cd` xuyên dòng; YAML nuốt ký tự (30 phút)

### 6.1. Đo hành vi shell trong một job duy nhất (12 phút)

Đại lượng loại (c) — **lần thứ BA** khoá học áp quy tắc "phải đo".

```yaml
# ~/lab03/.gitlab-ci.yml — thay toàn bộ
stages: [do]

do-hanh-vi-shell:
  stage: do
  image: alpine:3.20
  before_script:
    - export BIEN_BEFORE="dat-o-before_script"
    - echo "BEFORE pwd=$(pwd)"
  script:
    # Phép đo 1: before_script và script có cùng shell không
    - echo "DO1_BIEN_BEFORE=[${BIEN_BEFORE:-RONG}]"
    # Phép đo 2: cd ở dòng này có ảnh hưởng dòng sau không
    - mkdir -p thu-muc-con && cd thu-muc-con
    - echo "DO2_PWD_SAU_CD=$(pwd)"
    - cd "$CI_PROJECT_DIR"
    # Phép đo 3: biến đặt ở dòng script này có sang dòng script sau không
    - export BIEN_SCRIPT="dat-o-script"
    - echo "DO3_BIEN_SCRIPT=[${BIEN_SCRIPT:-RONG}]"
  after_script:
    - echo "DO4_BIEN_BEFORE_O_AFTER=[${BIEN_BEFORE:-RONG}]"
    - echo "DO5_BIEN_SCRIPT_O_AFTER=[${BIEN_SCRIPT:-RONG}]"
    - echo "DO6_PWD_O_AFTER=$(pwd)"
```

```bash
cd ~/lab03
P4=$(day "buoc 4a: do hanh vi shell"); cho_pipeline "$P4"
JD=$(job_id "$P4" do-hanh-vi-shell)
job_log "$JD" | grep -E '^(BEFORE|DO[1-6])'
```

```bash
L=$(job_log "$JD")
{
  echo "# QT 6.1, 6.2 — hành vi shell. ĐO trên chính runner này, không tra tài liệu."
  echo "# $(docker exec lab-runner gitlab-runner --version | head -1)"
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
  echo "# Ngày đo: $(date -Iseconds)"
  echo
  echo "$L" | grep -E '^(BEFORE|DO[1-6])'
  echo
  echo "# Kết luận (học viên tự điền):"
  echo "# - before_script và script CÙNG shell?  ..."
  echo "# - cd xuyên dòng trong script?          ..."
  echo "# - after_script thấy biến của script?   ..."
} | tee ~/lab03/hanh-vi-script.txt
```

**CHECKPOINT 9 — đo đủ sáu phép đo và ghi phiên bản runner.**

```bash
n=$(grep -cE '^DO[1-6]_' ~/lab03/hanh-vi-script.txt || true)
v=$(grep -c 'gitlab-runner' ~/lab03/hanh-vi-script.txt || true)
{ [ "$n" -eq 6 ] && [ "$v" -ge 1 ]; } \
  && echo "CHECKPOINT 9 — ĐẠT (6 phép đo, có ghi phiên bản runner)" \
  || echo "CHECKPOINT 9 — LỖI (phép đo=$n, phiên bản=$v)"
```

### 6.2. `cd` xuyên dòng làm artifact rỗng mà job xanh (10 phút)

Kiểm chứng QT 6.2. **Job sẽ XANH nhưng artifact rỗng — đó là kết quả đúng.**

```yaml
# ~/lab03/.gitlab-ci.yml — thay toàn bộ
stages: [build]

build-cd-sai:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p sau && cd sau
    - mkdir -p dist && echo "console.log(1)" > dist/app.js   # thật ra là sau/dist/app.js
    - echo "tep vua tao nam o: $(pwd)/dist/app.js"
  artifacts:
    paths: [dist/]        # gói RỖNG, job vẫn XANH

build-cd-dung:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p sau && (cd sau && mkdir -p dist && echo "console.log(2)" > dist/app.js)
    - mv sau/dist ./dist
    - test -s dist/app.js || { echo "KHANG DINH HONG: dist/app.js rong"; exit 1; }
  artifacts:
    paths: [dist/]
```

```bash
cd ~/lab03
P5=$(day "buoc 4b: cd xuyen dong"); cho_pipeline "$P5"
for j in build-cd-sai build-cd-dung; do
  id=$(job_id "$P5" "$j")
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$id" \
  | jq -r --arg n "$j" '"\($n)\tstatus=\(.status)\tartifact=\(.artifacts_file.size // 0) byte"'
done
```

**CHECKPOINT 10 — bản sai XANH với artifact rỗng; bản đúng XANH với artifact khác rỗng.**

```bash
IDS=$(job_id "$P5" build-cd-sai); IDD=$(job_id "$P5" build-cd-dung)
SS=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$IDS" | jq -r .status)
ZS=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$IDS" | jq -r '.artifacts_file.size // 0')
SD=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$IDD" | jq -r .status)
ZD=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$IDD" | jq -r '.artifacts_file.size // 0')
{ [ "$SS" = success ] && [ "$ZS" -lt 200 ] && [ "$SD" = success ] && [ "$ZD" -ge 200 ]; } \
  && echo "CHECKPOINT 10 — ĐẠT (cd-sai: $SS artifact ${ZS}B ← HỎNG IM LẶNG; cd-dung: $SD artifact ${ZD}B)" \
  || echo "CHECKPOINT 10 — LỖI (sai=$SS/${ZS}B, dung=$SD/${ZD}B)"
```

### 6.3. YAML nuốt ký tự (8 phút)

Kiểm chứng QT 6.3 bằng `ci/lint`, **không đẩy commit**.

```bash
cd ~/lab03
cat > /tmp/yaml-sai.yml <<'EOF'
job-sai:
  image: alpine:3.20
  script:
    - echo ket qua: xong
EOF
cat > /tmp/yaml-dung.yml <<'EOF'
job-dung:
  image: alpine:3.20
  script:
    - 'echo "ket qua: xong"'
    - |
      if [ -d dist ]; then
        echo "co dist"
      else
        echo "khong co dist"
      fi
    - >
      echo mot lenh dai
      duoc gop thanh mot dong
EOF

echo "=== bản SAI ==="; lint /tmp/yaml-sai.yml | jq -r '.valid, (.errors[]?)'
echo "=== bản ĐÚNG ==="; lint /tmp/yaml-dung.yml | jq -r '.valid, (.errors[]?)'
```

Ghi kết quả vào `hanh-vi-script.txt`:

```bash
{
  echo
  echo "## QT 6.3 — YAML nuốt ký tự"
  echo "ban_sai_valid  = $(lint /tmp/yaml-sai.yml  | jq -r .valid)"
  echo "ban_dung_valid = $(lint /tmp/yaml-dung.yml | jq -r .valid)"
} >> ~/lab03/hanh-vi-script.txt
```

---

## L7. Bước 5 — Thứ tự ưu tiên ba nguồn (20 phút)

Kiểm chứng QT 7.1. Đây là câu trả lời cho BTVN 4 câu 3 của buổi 02.

```yaml
# ~/lab03/.gitlab-ci.yml — thay toàn bộ
stages: [uu-tien]

default:
  image: alpine:3.20
  before_script:
    - echo "BEFORE_TU=default"

nac-1-chi-config-toml:
  stage: uu-tien
  # không khai image, không khai default cho job này → dùng default: alpine
  script:
    - echo "IMAGE_THUC_TE=$(cat /etc/os-release | grep '^ID=' | cut -d= -f2)"

nac-2-default:
  stage: uu-tien
  script:
    - echo "IMAGE_THUC_TE=$(cat /etc/os-release | grep '^ID=' | cut -d= -f2)"
    - echo "BEFORE chay may lan: kiem trong log"

nac-3-trong-job:
  stage: uu-tien
  image: debian:12-slim          # gần job nhất → THẮNG
  before_script:
    - echo "BEFORE_TU=job"        # THAY THẾ cái ở default, không nối vào
  script:
    - echo "IMAGE_THUC_TE=$(cat /etc/os-release | grep '^ID=' | cut -d= -f2)"
```

```bash
cd ~/lab03
echo "=== ĐỌC TỆP SAU PHÂN GIẢI — đoán trước, rồi so ==="
lint | jq -r '.jobs[] | "\(.name)\timage=\(.image.name // "khong khai")\tbefore=\((.before_script // []) | join(";"))"'

P6=$(day "buoc 5: thu tu uu tien"); cho_pipeline "$P6"

{
  echo "# QT 7.1 — ba nấc ưu tiên. ĐO image THỰC TẾ trong job, không tra tài liệu."
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
  echo -e "job\timage_khai_o\timage_thuc_te\tbefore_script_chay"
  for j in nac-1-chi-config-toml nac-2-default nac-3-trong-job; do
    id=$(job_id "$P6" "$j"); L=$(job_log "$id")
    IMG=$(echo "$L" | grep -m1 'IMAGE_THUC_TE=' | cut -d= -f2 | tr -d '"\r')
    BEF=$(echo "$L" | grep -oE 'BEFORE_TU=[a-z]+' | tr '\n' ',' | sed 's/,$//')
    case "$j" in
      nac-1*) khai="default" ;; nac-2*) khai="default" ;; nac-3*) khai="trong job" ;;
    esac
    echo -e "$j\t$khai\t$IMG\t${BEF:-khong-co}"
  done
} | tee ~/lab03/thu-tu-uu-tien.tsv
```

**CHECKPOINT 11 — job khai `image` riêng dùng đúng image đó, và `before_script` của nó THAY THẾ cái ở `default`.**

```bash
IMG3=$(awk -F'\t' '/^nac-3-trong-job/{print $3}' ~/lab03/thu-tu-uu-tien.tsv)
BEF3=$(awk -F'\t' '/^nac-3-trong-job/{print $4}' ~/lab03/thu-tu-uu-tien.tsv)
IMG1=$(awk -F'\t' '/^nac-1-chi-config-toml/{print $3}' ~/lab03/thu-tu-uu-tien.tsv)
{ [ "$IMG3" = "debian" ] && [ "$IMG1" = "alpine" ] && [ "$BEF3" = "BEFORE_TU=job" ]; } \
  && echo "CHECKPOINT 11 — ĐẠT (nấc 3 thắng: image=$IMG3, before=$BEF3 → THAY THẾ chứ không nối)" \
  || echo "CHECKPOINT 11 — LỖI (img nấc1=$IMG1, img nấc3=$IMG3, before nấc3=$BEF3)"
```

**Ba câu hỏi phải trả lời, ghi vào `thu-tu-uu-tien.tsv`:**

1. Job `nac-3-trong-job` chạy **mấy** `before_script`? Điều đó chứng minh nấc gần hơn **thay thế** hay **hợp nhất**?
2. Nếu `config.toml` khai `image = "ubuntu:24.04"` làm mặc định, job `nac-1` sẽ chạy image nào? Vì sao? (Không cần chạy thật — lập luận từ QT 7.1.)
3. Cả ba job đều dùng `default:`. Nếu xoá khối `default:` đi thì job nào còn chạy được, job nào không?

### 7.1. `variables` không theo quy tắc ba nấc (6 phút)

Kiểm chứng QT 7.2 **bằng đo**, không bằng lập luận. Hai phép thử, cả hai dùng `ci/lint` nên không tốn thời gian chạy pipeline.

**Phép thử A — `variables` có phải khoá của `default:` không.**

```bash
cd ~/lab03
cat > /tmp/bien-trong-default.yml <<'EOF'
default:
  image: alpine:3.20
  variables:
    X: "dat-trong-default"

in-bien:
  script: [echo "X=[$X]"]
EOF
echo "=== variables đặt TRONG default: ==="
lint /tmp/bien-trong-default.yml | jq -r '.valid, (.errors[]?), (.warnings[]?)'
```

**Phép thử B — `variables` cấp job so cấp tệp.**

```bash
cat > /tmp/bien-hai-cap.yml <<'EOF'
variables:
  X: "cap-tep"
  Y: "cap-tep"

job-ghi-de:
  image: alpine:3.20
  variables:
    X: "cap-job"
  script:
    - echo "X=[$X]"
    - echo "Y=[$Y]"
EOF
echo "=== biến hai cấp, sau phân giải ==="
lint /tmp/bien-hai-cap.yml | jq -r '.jobs[] | {name, variables}'
```

Điểm cần nhìn ở phép thử B: `Y` **vẫn còn** dù job có khai `variables` riêng. Đây chính là chỗ `variables` khác `before_script` — với `before_script`, nấc gần hơn **thay thế toàn bộ** (đã đo ở CHECKPOINT 11); với `variables`, nấc gần hơn chỉ **ghi đè từng khoá**, các khoá khác giữ nguyên.

Ghi hai kết quả vào hiện vật:

```bash
{
  echo
  echo "## QT 7.2 — variables KHÔNG theo quy tắc ba nấc của image/before_script"
  echo "phep_thu_A_variables_trong_default_valid = $(lint /tmp/bien-trong-default.yml | jq -r .valid)"
  echo "phep_thu_A_canh_bao = $(lint /tmp/bien-trong-default.yml | jq -r '[.warnings[]?, .errors[]?] | join(" | ")')"
  echo "phep_thu_B_bien_sau_phan_giai:"
  lint /tmp/bien-hai-cap.yml | jq -r '.jobs[] | "  \(.name): \(.variables // {} | tostring)"'
  echo "# So với before_script (CHECKPOINT 11): nấc gần hơn THAY THẾ TOÀN BỘ."
  echo "# Với variables: nấc gần hơn chỉ GHI ĐÈ TỪNG KHOÁ. → hai quy tắc KHÁC NHAU."
} | tee -a ~/lab03/thu-tu-uu-tien.tsv
```

**Hai câu hỏi phải trả lời, ghi ngay dưới:**

1. Ở phép thử B, biến `Y` còn giá trị không sau khi job khai `variables` riêng? So với kết quả của `before_script` ở CHECKPOINT 11 — hai cơ chế **giống hay khác**?
2. Nếu ở cấp **project** (Settings → CI/CD → Variables) cũng có một biến tên `X`, bạn đoán job in ra giá trị nào? Ghi phỏng đoán kèm lập luận — buổi 06 sẽ đo thật với đủ **chín** nguồn.

```bash
rm -f /tmp/bien-trong-default.yml /tmp/bien-hai-cap.yml
```

---

## L8. Nộp sản phẩm và dọn dẹp (10 phút)

### 8.1. Khôi phục `config.toml` — làm trước tiên

```bash
docker exec lab-runner sh -c \
  'cp /etc/gitlab-runner/config.toml.buoi03.bak /etc/gitlab-runner/config.toml'
docker restart lab-runner >/dev/null && sleep 20
docker exec lab-runner sh -c 'grep -E "^concurrent" /etc/gitlab-runner/config.toml'
```

### 8.2. Gom hiện vật và kiểm

```bash
DICH="$PORTFOLIO/03-cu-phap-yaml-va-stage"
mkdir -p "$DICH"
cp ~/lab03/job-rac.md              "$DICH/"
cp ~/lab03/lang-phi-hang-rao.tsv   "$DICH/"
cp ~/lab03/do-song-song-stage.tsv  "$DICH/"
cp ~/lab03/hanh-vi-script.txt      "$DICH/"
cp ~/lab03/thu-tu-uu-tien.tsv      "$DICH/"
cp ~/lab03/.gitlab-ci.yml          "$DICH/"
# ban-do-phu-thuoc.md do học viên tự viết ở §L4.3

cat > "$DICH/kiem-hien-vat.sh" <<'SH'
#!/usr/bin/env bash
cd "$(dirname "$0")"
P=0; F=0
kiem() { if eval "$2" >/dev/null 2>&1; then echo "ĐẠT   $1"; P=$((P+1)); else echo "LỖI   $1"; F=$((F+1)); fi; }

kiem "job-rac.md có danh sách job rác"          "grep -q 'Job RÁC' job-rac.md"
kiem "job-rac.md ghi phiên bản GitLab"          "grep -q 'GitLab' job-rac.md"
kiem "lang-phi-hang-rao.tsv có 3 đại lượng"     "[ \$(grep -cE '^(tong_thoi_gian_pipeline|duong_gang_du_lieu|lang_phi_hang_rao)' lang-phi-hang-rao.tsv) -eq 3 ]"
kiem "do-song-song-stage.tsv có 2 mức"          "[ \$(grep -cE '^[0-9]+\s' do-song-song-stage.tsv) -eq 2 ]"
kiem "do-song-song-stage.tsv ghi nproc"         "grep -q 'nproc' do-song-song-stage.tsv"
kiem "hanh-vi-script.txt có 6 phép đo"          "[ \$(grep -cE '^DO[1-6]_' hanh-vi-script.txt) -eq 6 ]"
kiem "hanh-vi-script.txt ghi phiên bản runner"  "grep -q 'gitlab-runner' hanh-vi-script.txt"
kiem "hanh-vi-script.txt có kết quả YAML lint"  "grep -q 'ban_sai_valid' hanh-vi-script.txt"
kiem "thu-tu-uu-tien.tsv có 3 nấc"              "[ \$(grep -cE '^nac-[123]') -eq 3 ] || [ \$(grep -cE '^nac-' thu-tu-uu-tien.tsv) -eq 3 ]"
kiem "ban-do-phu-thuoc.md có >= 4 job"          "[ \$(grep -cE '^\| *\`?[a-z]' ban-do-phu-thuoc.md) -ge 4 ]"
kiem "checkpoint.log có 11 dòng CHECKPOINT"     "[ \$(grep -c 'CHECKPOINT' checkpoint.log) -ge 11 ]"
kiem "checkpoint.log không có LỖI"              "! grep -q 'LỖI' checkpoint.log"

echo "=== $P đạt, $F lỗi ==="
[ "$F" -eq 0 ]
SH
chmod +x "$DICH/kiem-hien-vat.sh"
```

**CHECKPOINT 12 — hiện vật đầy đủ và `config.toml` đã khôi phục.**

```bash
hv=$(bash "$DICH/kiem-hien-vat.sh" >/dev/null 2>&1 && echo 1 || echo 0)
same=$(docker exec lab-runner sh -c \
  'cmp -s /etc/gitlab-runner/config.toml /etc/gitlab-runner/config.toml.buoi03.bak && echo 1 || echo 0')
{ [ "$hv" -eq 1 ] && [ "$same" = "1" ]; } \
  && echo "CHECKPOINT 12 — ĐẠT" \
  || echo "CHECKPOINT 12 — LỖI (hiện vật=$hv, config khớp=$same)"
```

```bash
cd "$PORTFOLIO"
git add 03-cu-phap-yaml-va-stage
git commit -q -m "buoi 03: cu phap yaml va stage — job rac, lang phi hang rao, thu tu uu tien"
git push -q 2>/dev/null || echo "chưa cấu hình remote cho portfolio"
```

### 8.3. Dọn dẹp

```bash
source ~/lab03/cong-cu.sh
for j in $(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs?scope[]=pending&scope[]=running&per_page=100" | jq -r '.[].id'); do
  curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects/$PID3/jobs/$j/cancel" >/dev/null
done
curl -sf --request DELETE "${H[@]}" "$GITLAB/api/v4/projects/$PID3/artifacts" >/dev/null
rm -f /tmp/yaml-sai.yml /tmp/yaml-dung.yml
```

---

## L9. Xử lý sự cố thường gặp trong lab

| Triệu chứng | Nguyên nhân | Cách khắc phục |
|---|---|---|
| `lint` trả về rỗng | `jq -Rs` không tạo đúng JSON, hoặc token thiếu scope `api` | Kiểm: `jq -Rs '{content: .}' < .gitlab-ci.yml \| head -c 200` |
| `lint` báo `404` | Sai `PID3`, hoặc project chưa tồn tại | `echo $PID3`; kiểm bằng `curl .../projects/$PID3` |
| `lint` trả `valid: true` dù có lỗi chính tả | **Đây là kết quả đúng** — QT 4.1: gõ sai vẫn hợp lệ về cú pháp | Không phải lỗi. Phải so **danh sách job**, không nhìn `valid` |
| CHECKPOINT 2 không thấy job rác | Đã sửa tệp trước khi chạy checkpoint | Khôi phục bản có lỗi chính tả rồi chạy lại |
| `test-thieu-artifact` lại **xanh** | Job trước có `artifacts` bao trùm `dist/`, hoặc còn artifact cũ | Xoá artifact: `curl -X DELETE .../artifacts`; kiểm lại tệp |
| Lãng phí hàng rào đo được gần 0 | `test-cham` không chạy, hoặc `concurrent` quá thấp làm mọi thứ tuần tự | Kiểm `job_bang`; đảm bảo `concurrent >= 2` ở bước 2 |
| CHECKPOINT 6 báo `.pre` không chạy trước | Runner nhận job không theo thứ tự vì hàng đợi | Chạy lại; nếu vẫn vậy, kiểm `concurrent >= 2` |
| CHECKPOINT 7 báo song song > 1 ở `concurrent = 1` | Runner chưa nạp lại `config.toml` | Xem kết luận buổi 02 CHECKPOINT 3; thêm `docker restart lab-runner` |
| Bước 3 tổng thời gian ở `concurrent = 6` không giảm | Máy hết CPU — đây là **QT 6.2 buổi 02** | Không phải lỗi. Ghi vào hiện vật kèm `nproc` và `docker stats` |
| `DO2_PWD_SAU_CD` in ra thư mục gốc | Runner tách mỗi dòng thành tiến trình riêng — **phát hiện đáng ghi** | Ghi vào hiện vật kèm phiên bản runner; đó là dữ liệu, không phải lỗi |
| `build-cd-sai` lại **đỏ** | Runner đặt `set -e` và `mkdir` lỗi | Kiểm log; nếu vậy thì đơn giản hoá script và ghi lại hành vi |
| `nac-3-trong-job` không kéo được `debian:12-slim` | Docker Hub giới hạn tốc độ | Đổi sang image khác đã có sẵn; ghi lại image đã dùng |
| Sau khôi phục `config.toml`, job không chạy | Runner chưa khởi động lại xong | Chờ 30 giây; kiểm `runners/:id` trường `online` |
| Phép thử A ở §L7.1 trả `valid: true` | Phiên bản GitLab này chấp nhận `variables` trong `default:` | Đó là **dữ liệu**, không phải lỗi. Ghi lại kèm phiên bản; điểm cần thấy là ở phép thử B |
| `lint` trả `.jobs[].variables` là `null` | Phiên bản này không trả trường đó trong `ci/lint` | Đo bằng cách chạy pipeline thật và đọc `echo` trong log; ghi rõ đã dùng cách nào |
| `job-rac.md` rỗng vì `comm` báo lỗi | Hai đầu vào của `comm` chưa được sắp xếp | Cả hai vế đều phải qua `sort`; kiểm bằng `lint_job \| sort \| head` |
| Bước 2 `dong-goi` chạy **trước** `test-cham` xong | Có `needs` sót lại từ lần chỉnh trước | Buổi này **chưa dùng `needs`**; kiểm tệp và bỏ nó đi — nếu không thì phép đo lãng phí sai |
| Muốn làm lại từ đầu | — | Khôi phục `config.toml`, xoá project, chạy lại §L3.1 |

---

## L10. Bài tập mở rộng

### BT1. Đếm từ khoá cấp trên cùng thật sự

Thử đặt lần lượt từng khoá trong 13 từ khoá của QT 4.1 ở cấp trên cùng với giá trị tối thiểu, gọi `lint`, và xem khoá nào **không** biến thành job.

**Câu hỏi phải trả lời:** phiên bản GitLab của bạn có đúng 13 từ khoá không? Nếu khác, khác cái nào?

### BT2. `!reference` so `extends` so anchor

Viết cùng một khuôn mẫu bằng ba cách: job ẩn + `extends`, YAML anchor, và `!reference`. Gọi `lint` cho cả ba.

**Câu hỏi phải trả lời:** tệp sau phân giải có giống nhau không? Cách nào đọc dễ nhất khi có 20 job? (Buổi 10 trả lời đầy đủ.)

### BT3. Lãng phí hàng rào của repo thật

Lấy pipeline thật của đội mình, lập bảng "job này cần artifact của ai", tính đường găng dữ liệu và lãng phí hàng rào.

**Câu hỏi phải trả lời:** lãng phí bao nhiêu giây? Nhân với số lần chạy pipeline một ngày thì bao nhiêu phút runner một tháng? (Buổi 46 quy con số đó ra tiền.)

### BT4. `.post` chạy khi pipeline đỏ không

Đặt một job ở `.post` và làm một job ở stage giữa đỏ.

**Câu hỏi phải trả lời:** job `.post` có chạy không? Cần thêm gì để nó luôn chạy? (Gợi ý: `when`.)

### BT5. Chuỗi khối `|` so `>`

Viết cùng một lệnh `docker build` nhiều tham số bằng cả hai, và một khối `if` bằng cả hai.

**Câu hỏi phải trả lời:** cái nào hỏng ở ca nào, và vì sao?

### BT6. Job rác im lặng tới mức nào

Tạo một tệp có `artefacts:` (gõ sai `artifacts`) trong một job, chạy pipeline thật.

**Câu hỏi phải trả lời:** job xanh hay đỏ? Artifact có gì? Ô nào của bảng hai thuộc tính? So với ca artifact rỗng của buổi 01 — giống và khác chỗ nào?

### BT7. Ba nấc thành bốn nấc

Thêm `extends` vào bài lab bước 5 và đo lại: `config.toml` → `default` → `extends` → job.

**Câu hỏi phải trả lời:** `extends` nằm ở nấc nào? Nó thay thế hay hợp nhất? (Buổi 10 trả lời đầy đủ — hôm nay chỉ cần đo.)

### BT8. Viết hàm `lint` dùng lại

Đóng gói hàm `lint` thành một script nhận đường dẫn tệp và in ra danh sách job cùng cảnh báo, dùng được cho mọi project.

**Câu hỏi phải trả lời:** script của bạn xử lý thế nào khi tệp có `include` trỏ tới project khác mà token không có quyền đọc?

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| Hạng mục | Điểm | Tiêu chí |
|---|---|---|
| `job-rac.md` — danh sách job rác + 3 câu trả lời | 3 | Phải trả lời được câu 1 về `valid: true` dù có lỗi chính tả |
| `lang-phi-hang-rao.tsv` — 3 đại lượng | 4 | Có cả tổng, đường găng, và **hiệu**; thiếu hiệu thì hạng mục này 0 điểm |
| `ban-do-phu-thuoc.md` — bảng "job này cần artifact của ai" | 4 | ≥ 4 job, có cột "chờ ai **vô ích**" |
| `do-song-song-stage.tsv` — 2 mức + `nproc` + 3 câu trả lời | 4 | Phải trả lời được câu 1: cùng tệp YAML, tệp nào đã đổi |
| `hanh-vi-script.txt` — 6 phép đo + phiên bản runner + kết quả lint YAML | 4 | Thiếu phiên bản runner thì hạng mục này **0 điểm** |
| `thu-tu-uu-tien.tsv` — 3 nấc + 3 câu trả lời | 3 | Phải trả lời đúng câu 1: **thay thế**, không hợp nhất |
| `thu-tu-uu-tien.tsv` — hai phép thử của §L7.1 + 2 câu trả lời | 2 | Phải chỉ ra được `variables` **ghi đè từng khoá** còn `before_script` **thay thế toàn bộ** |
| `checkpoint.log` — 12 dòng, không có `LỖI` | 2 | Chạy lại một checkpoint bất kỳ phải ra `ĐẠT` |
| **Tổng** | **26** | Đạt ≥ 16, đạt tốt ≥ 21 |

**Điểm trừ** — dẫn chiếu Bẫy hay gặp của `01-ly-thuyet.md` §9:

| Lỗi | Trừ |
|---|---|
| **Không khôi phục `config.toml`** ở §L8.1 | **Trần điểm 1 cho cả bài** |
| `checkpoint.log` ghi ĐẠT nhưng chạy lại ra LỖI | **Trần điểm 1 cho cả bài** |
| Kết luận "`stage` chuyển dữ liệu" — bẫy 1 | −4 |
| Kết luận "job cùng stage luôn chạy song song" — bẫy 2 | −4 |
| `hanh-vi-script.txt` chép đáp án thay vì đo | −3 |
| `lang-phi-hang-rao.tsv` chỉ có tổng thời gian, không có hiệu | −3 |
| Trả lời `before_script` ở job **nối vào** cái ở `default` — bẫy 12 | −2 |
| Nộp ảnh chụp màn hình thay kết quả API | **Trần điểm 1** cho hạng mục đó |

**Mức 3 của rubric buổi** đạt được khi: hoàn thành ≥ 3 bài BT của §L10 kèm câu trả lời; **hoặc** làm BT3 trên repo thật và nộp số giây lãng phí kèm quy đổi ra phút runner một tháng; **hoặc** phát hiện thêm một hành vi shell ngoài sáu phép đo, kèm bằng chứng log.

---

## Bảng đối soát thời lượng

| Bước | Nội dung | Thời lượng |
|---|---|---|
| L3 | Bước 1 — Giải phẫu tệp bằng `ci/lint`; job rác; job ẩn | 30' |
| L4 | Bước 2 — `stage` chuyển 0 byte; đo lãng phí hàng rào; `.pre` | 30' |
| L5 | Bước 3 — Song song trong stage phụ thuộc `concurrent` | 30' |
| L6 | Bước 4 — Ba khối hai shell; `cd` xuyên dòng; YAML nuốt ký tự | 30' |
| L7 | Bước 5 — Thứ tự ưu tiên ba nguồn; và `variables` có quy tắc riêng | 20' |
| L8 | Nộp sản phẩm, khôi phục `config.toml`, dọn dẹp | 10' |
| **Tổng** | | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---



**Quy tắc cho giảng viên:**

- Chọn **5–7 câu** trong 12, ưu tiên câu 🔥.
- **Gọi ngẫu nhiên.** Người trả lời sai thì người kế tiếp bổ sung.
- Trả lời **bằng miệng, không nhìn tài liệu**.
- Hai câu hỏi chen vào bất kỳ lúc nào, đã thành phản xạ của khoá: **"bao nhiêu?"** khi có khẳng định định lượng, và **"sửa ở tệp nào?"** khi học viên đề xuất sửa gì đó (buổi 02).
- Buổi này thêm câu thứ ba: **"cái đó đi qua đường nào trong bốn đường?"** — dùng khi học viên nói về dữ liệu giữa hai job.

**Thang điểm mỗi câu:**

| Điểm | Nghĩa |
|---|---|
| 0 | Không trả lời được, hoặc sai cơ chế |
| 1 | Nhắc được tên khái niệm, không nêu cơ chế |
| 2 | Nêu đúng cơ chế |
| 3 | Đúng cơ chế **và** một con số, hoặc **và** một ca nó không đúng |

**Hai lỗi làm trần điểm cả buổi là 1:**

1. **Trả lời rằng `stage` chuyển dữ liệu giữa các job.** Đây là hiểu sai gốc của cả buổi, và nó mâu thuẫn trực tiếp với buổi 01 QT 5.1 — bốn đường vào không có `stage`.
2. **Khẳng định job cùng stage LUÔN chạy song song.** Đây là hiểu sai nửa sau của luận đề, và nó bỏ qua toàn bộ buổi 02.

**Bốn câu phân loại thật:**

| Câu | Phân loại điều gì |
|---|---|
| 3 | Phân loại người **từng bị job rác cắn**. Người chưa gặp sẽ nói "GitLab sẽ báo lỗi thôi" |
| 5 | Phân loại **tư duy đường găng**. Người không có tư duy này chỉ nói "nhiều stage thì chậm" mà không tính được |
| 8 | Phân loại người **đọc log kỹ**. `cd` xuyên dòng chỉ nhớ được nếu từng mất một buổi vì nó |
| 12 | Phân loại **tư duy tối ưu có đo**. Câu này đo cách người ta chuyển từ cảm nhận sang con số |

---

## V2. Bộ câu hỏi

### Câu 1 — 🔥

**Hỏi:** `stage` trong GitLab CI cho ta cái gì?

**Đáp án chuẩn:** Cho **một ràng buộc thứ tự**, và **chỉ có thế**. `stage` nói "mọi job của stage này chạy sau khi mọi job của stage trước kết thúc". Nó là một **hàng rào thời gian**.

Hai thứ nó **không** cho:

1. **Không chuyển dữ liệu.** Buổi 01 đã liệt kê đủ bốn đường vào một job — git, cache, artifact, biến — và `stage` không nằm trong đó. `stage` chuyển **0 byte**. Cái chuyển dữ liệu là `artifacts`. Chỗ gây hiểu nhầm là mặc định của GitLab: job tải artifact của mọi job ở các stage trước — nhưng cái chuyển là `artifacts`, còn `stage` chỉ quyết định **tập nào được tải mặc định**.

2. **Không đảm bảo song song.** `stage` chỉ **cho phép** các job trong nó chạy đồng thời. Việc chúng có chạy đồng thời hay không do `concurrent` và số slot runner quyết định — tức do `config.toml`, tệp thứ hai của buổi 02.

**Tiêu chí chấm:**
- 0đ: "`stage` chuyển kết quả từ job này sang job kia." **Trần điểm cả buổi là 1.**
- 1đ: Nói được nó quyết định thứ tự.
- 2đ: Nêu đúng cả hai thứ nó **không** cho.
- 3đ: Như trên, **và** nêu con số 0 byte, **và** giải thích được vì sao mặc định tải artifact stage trước gây hiểu nhầm.

**Câu hỏi đào sâu:** Vậy cái gì bỏ được hàng rào? *(`needs` — buổi 08. Nó biến pipeline từ chuỗi stage thành một đồ thị phụ thuộc, và thời gian pipeline chuyển từ "tổng các stage" sang "đường găng dài nhất".)*

---

### Câu 2 — ★★

**Hỏi:** Mở một tệp `.gitlab-ci.yml` lạ. Làm sao biết khoá nào là job, khoá nào không?

**Đáp án chuẩn:** Theo **nguyên tắc loại trừ**: GitLab có một danh sách từ khoá cấu hình cấp trên cùng; **mọi khoá còn lại đều là một job**.

Mười ba từ khoá cấp trên cùng ở GitLab 17.x: `stages`, `default`, `variables`, `include`, `workflow`, `image`, `services`, `cache`, `before_script`, `after_script`, `pages`, `hooks`, `spec`.

Thêm một quy tắc: khoá bắt đầu bằng **dấu chấm** là **job ẩn** — GitLab không bao giờ chạy nó, nhưng nội dung vẫn được phân giải nên dùng làm khuôn mẫu cho `extends` được.

Điểm để đạt 3 điểm: **đừng học thuộc danh sách** — nó đổi theo phiên bản (`hooks` và `spec` là thêm mới của dòng 17.x). Học nguyên tắc loại trừ, và học cách hỏi `ci/lint` để lấy danh sách job **sau phân giải**.

**Tiêu chí chấm:**
- 0đ: Không biết cách phân biệt.
- 1đ: Kể được vài từ khoá.
- 2đ: Nêu đúng nguyên tắc loại trừ và biết về job ẩn.
- 3đ: Như trên, **và** nói rõ danh sách phụ thuộc phiên bản, **và** nêu `ci/lint` là cách kiểm chắc chắn.

**Câu hỏi đào sâu:** Job ẩn dùng làm gì? *(Khuôn mẫu cho `extends` và anchor. Một ký tự `.` biến job thành khuôn mẫu. Ngược lại, thêm nhầm dấu chấm vào job thật thì job biến mất khỏi pipeline **im lặng** — không lỗi, không cảnh báo.)*

---

### Câu 3 — ★★★

**Hỏi:** Bạn gõ `variabels:` thay vì `variables:` ở cấp trên cùng. Chuyện gì xảy ra?

**Đáp án chuẩn:** GitLab **không báo lỗi**. Nó tạo một **job** tên `variabels`, vì `variabels` không nằm trong danh sách từ khoá dành riêng nên nguyên tắc loại trừ coi nó là job.

Hai hậu quả cùng lúc, và hậu quả thứ hai mới là cái đắt:

1. Pipeline có thêm một **job rác**. Job này thường xanh vì nó chẳng làm gì — hoặc đỏ vì thiếu `script`, tuỳ nội dung.
2. Khoá **thật** mà ta định gõ **không tồn tại**. Mọi biến khai trong đó biến mất, và job đọc chúng nhận chuỗi rỗng. Shell không báo lỗi khi biến rỗng, nên job thường **vẫn xanh** và chỉ tạo ra hiện vật có tên sai hoặc cấu hình sai.

Ô của bảng hai thuộc tính: **im lặng, không chặn** — ô nguy hiểm nhất.

Cách phát hiện, mất 1 giây và không cần đẩy commit:

```bash
curl -sf --request POST --header "PRIVATE-TOKEN: $TOKEN" \
  --header "Content-Type: application/json" \
  --data "$(jq -Rs '{content: .}' < .gitlab-ci.yml)" \
  "$GITLAB/api/v4/projects/$PID/ci/lint" | jq -r '.jobs[].name'
```

So danh sách job trả về với danh sách mình **nghĩ** là có. Chênh lệch nào cũng đáng điều tra.

**Tiêu chí chấm:**
- 0đ: "GitLab sẽ báo lỗi cú pháp."
- 1đ: Biết là nó không báo lỗi, không nêu được hậu quả.
- 2đ: Nêu đúng cả hai hậu quả.
- 3đ: Như trên, **và** xếp được vào ô im lặng + không chặn, **và** đưa được cách phát hiện bằng `ci/lint`.

**Câu hỏi đào sâu:** `ci/lint` trả về `valid: true` cho tệp đó không? *(**Có** — tệp hợp lệ về cú pháp. Đó là lý do phải so **danh sách job**, không nhìn cờ `valid`. Đây là bẫy mà bài lab bước 1 dựng riêng để học viên gặp.)*

---

### Câu 4 — 🔥

**Hỏi:** Bạn đặt 6 job vào cùng một `stage` để chúng chạy song song. Chúng có chạy song song không?

**Đáp án chuẩn:** **Chưa chắc.** `stage` chỉ **cho phép** song song — nó gỡ ràng buộc thứ tự giữa sáu job. Việc chúng có thật sự chạy đồng thời hay không do phía runner quyết định: `concurrent`, `limit`, số runner khớp tag, và tài nguyên máy.

Con số cụ thể: với `concurrent = 1`, sáu job mỗi job 30 giây chạy **tuần tự** và stage mất **180 giây**, không phải 30 giây. Tức thời gian stage bằng **tổng**, không bằng **max**.

Điểm quan trọng để đạt 3 điểm: đây là chỗ hai tệp gặp nhau. `stage` thuộc `.gitlab-ci.yml` — người viết pipeline. `concurrent` thuộc `config.toml` — người vận hành runner. Người viết pipeline khai sáu job cùng stage và tưởng chúng song song; người vận hành đặt `concurrent = 1` và không biết ai đang trông chờ gì. Không ai sai, nhưng kết quả sai.

Cách kiểm bằng số, không đoán:

```bash
# lấy started_at và finished_at của các job, xem chúng có CHỒNG LẤN không
curl -sf --header "PRIVATE-TOKEN: $TOKEN" ".../pipelines/$PIPE/jobs" \
| jq -r '.[] | [.name, .started_at, .finished_at] | @tsv'
```

**Tiêu chí chấm:**
- 0đ: "Có, cùng stage thì chạy song song." **Trần điểm cả buổi là 1.**
- 1đ: Nói được là còn tuỳ, không nêu được tuỳ vào cái gì.
- 2đ: Nêu đúng `concurrent` quyết định.
- 3đ: Như trên, **và** nêu con số tổng-so-max, **và** nói rõ đây là chỗ hai tệp gặp nhau.

**Câu hỏi đào sâu:** Nếu ai đó nói "tôi đặt sáu job cùng stage cho nó chạy song song", câu hỏi ngược của bạn là gì? *("`concurrent` của runner là bao nhiêu?" — và nếu họ không biết thì họ chưa kiểm được điều họ vừa khẳng định.)*

---

### Câu 5 — ★★★

**Hỏi:** Pipeline: `build` 10 giây sinh artifact; stage `test` có `test-nhanh` 5 giây và `test-cham` 60 giây; `dong-goi` 2 giây và **chỉ cần artifact của `build`**. Tổng thời gian bao nhiêu, và lãng phí bao nhiêu?

**Đáp án chuẩn:**

| Đại lượng | Tính | Giá trị |
|---|---|---|
| Tổng thời gian pipeline | 10 + 60 + 2 (`dong-goi` chờ `test-cham`) | **72 giây** |
| Đường găng **dữ liệu** thật | `build` → `dong-goi` = 10 + 2 | **12 giây** |
| **Lãng phí hàng rào** | 72 − 12 | **60 giây** |

Định nghĩa cần nói ra: **lãng phí hàng rào = tổng thời gian pipeline − đường găng dữ liệu thật**, trong đó đường găng dữ liệu là chuỗi phụ thuộc `artifacts` dài nhất — tức giới hạn dưới mà pipeline không thể nhanh hơn.

Cơ chế sinh ra lãng phí: hàng rào stage là ràng buộc **toàn cục**, nó không phân biệt job nào phụ thuộc job nào. `dong-goi` chỉ cần artifact của `build` nhưng vẫn phải chờ **tất cả** job stage `test` xong, kể cả `test-cham` mà nó chẳng cần gì.

Điểm để đạt 3 điểm: nói rõ con số 60 giây là của **ví dụ này**, còn cái phổ quát là **phép trừ**. Và nói được rằng buổi 08 lấy lại đúng 60 giây ấy bằng `needs`.

**Tiêu chí chấm:**
- 0đ: Không tính được.
- 1đ: Tính đúng tổng 72 giây.
- 2đ: Tính đúng cả ba số.
- 3đ: Như trên, **và** phát biểu được định nghĩa lãng phí bằng phép trừ, **và** nói rõ con số phụ thuộc ví dụ còn phép trừ thì phổ quát.

**Câu hỏi đào sâu:** Nhân con số ấy với gì để nó thành lập luận thuyết phục sếp? *(Với số lần chạy pipeline một ngày, ra phút runner một tháng. Buổi 46 quy phút runner thành tiền. 60 giây × 40 lần/ngày × 22 ngày ≈ 880 phút runner một tháng cho **một** repo.)*

---

### Câu 6 — ★★

**Hỏi:** `.pre` và `.post` là gì?

**Đáp án chuẩn:** Hai stage **luôn tồn tại** mà không cần khai trong `stages:`. `.pre` chạy **trước** mọi stage khác; `.post` chạy **sau** mọi stage khác. Chúng không đếm vào `stages:` và không đổi thứ tự các stage đã khai.

Giá trị thực dụng: đặt các job hạ tầng ở hai đầu mà **không phải sửa `stages:` của từng project**. Nếu một tổ chức có 30 project và muốn thêm một bước kiểm ở đầu mọi pipeline, dùng `.pre` thì không project nào phải sửa danh sách stage.

Hai ví dụ dùng trong khoá này: quét secret bằng Gitleaks ở `.pre` để chặn sớm (buổi 29); thu thập số liệu DORA ở `.post` (buổi 46).

**Tiêu chí chấm:**
- 0đ: Không biết chúng tồn tại.
- 1đ: Biết chúng là stage đặc biệt.
- 2đ: Nêu đúng thứ tự và biết chúng không cần khai.
- 3đ: Như trên, **và** nêu được giá trị thực dụng khi có nhiều project, **và** cho ví dụ cụ thể.

**Câu hỏi đào sâu:** Job ở `.post` có chạy khi pipeline đỏ không? *(Mặc định **không** — nó theo quy tắc `when` thông thường. Muốn nó luôn chạy thì đặt `when: always`. Đây đúng là chỗ nhiều người mất báo cáo khi pipeline đỏ.)*

---

### Câu 7 — ★★

**Hỏi:** `before_script`, `script`, `after_script` — chúng chạy trong mấy shell?

**Đáp án chuẩn:** **Ba** khối, **hai** shell.

| Khối | Shell | Thấy biến của `before_script`? | Chạy khi `script` đỏ? |
|---|---|---|---|
| `before_script` | A | — | — |
| `script` | **A** | **Có** | — |
| `after_script` | **B** | **Không** | **Có** |

Runner ghép `before_script` và `script` thành một script duy nhất rồi chạy — nên biến, `cd`, hàm shell đi xuyên từ khối đầu sang khối sau. `after_script` được sinh thành script riêng và chạy như tiến trình riêng, **để nó vẫn chạy được kể cả khi `script` đã chết**. Đó là lý do thiết kế: nếu cùng shell thì shell chết là mất luôn `after_script`.

Cách truyền giá trị sang `after_script`: ghi ra **tệp trong thư mục dự án**, vì thư mục dự án là thứ cả hai shell cùng thấy.

**Tiêu chí chấm:**
- 0đ: "Cả ba cùng một shell."
- 1đ: Biết `after_script` khác nhưng không giải thích được.
- 2đ: Nêu đúng 3 khối 2 shell và cơ chế.
- 3đ: Như trên, **và** nêu **lý do thiết kế**, **và** nêu cách truyền qua tệp.

**Câu hỏi đào sâu:** Đây là hành vi bạn tra tài liệu hay đo? *(**Đo.** Nó đã đổi giữa các phiên bản runner. Bài lab đo sáu điểm trong một job duy nhất và ghi kèm số phiên bản runner — đây là lần thứ ba khoá học áp quy tắc "phải đo".)*

---

### Câu 8 — ★★★

**Hỏi:** Job có `script` gồm: dòng 1 `mkdir sau && cd sau`, dòng 2 tạo `dist/app.js`. `artifacts:paths` là `[dist/]`. Job xanh hay đỏ, và artifact có gì?

**Đáp án chuẩn:** Job **XANH**. Artifact **RỖNG** — vài trăm byte.

Cơ chế: mỗi phần tử của danh sách `script` được runner ghép vào **cùng một** script shell, nên `cd` ở dòng 1 ảnh hưởng **mọi** dòng sau nó. Tệp thật ra nằm ở `sau/dist/app.js`. Mẫu `artifacts:paths: [dist/]` trỏ vào `dist/` ở **gốc** thư mục dự án, không khớp gì — và pha `upload_artifacts` upload một gói rỗng rồi báo **thành công**.

Ô của bảng hai thuộc tính: **im lặng, không chặn** — ô nguy hiểm nhất. Đây là cùng một ô với ca artifact rỗng của buổi 01, chỉ khác nguyên nhân: buổi 01 là mẫu đường dẫn sai, hôm nay là `cd` xuyên dòng.

Ba cách phòng, xếp theo độ mạnh:

1. **Khẳng định** — `test -s dist/app.js || exit 1` (buổi 01 QT 7.3). Mạnh nhất vì nó bắt mọi nguyên nhân.
2. **Dùng mốc tuyệt đối** — `cd "$CI_PROJECT_DIR"` trước khi kết thúc.
3. **Subshell** — `(cd sau && lam-gi-do)`, để `cd` không thoát ra ngoài dấu ngoặc.

**Tiêu chí chấm:**
- 0đ: "Đỏ, vì không tìm thấy thư mục."
- 1đ: Đoán đúng là xanh nhưng không giải thích được artifact.
- 2đ: Nêu đúng xanh + artifact rỗng và cơ chế `cd` xuyên dòng.
- 3đ: Như trên, **và** xếp vào ô im lặng + không chặn, **và** nêu được cả ba cách phòng kèm cách nào mạnh nhất.

**Câu hỏi đào sâu:** Nếu `cd` nằm ở `before_script` thì sao? *(Ảnh hưởng luôn cả `script`, vì hai khối cùng một shell. Nhưng **không** ảnh hưởng `after_script` — shell khác, thư mục làm việc về mặc định.)*

---

### Câu 9 — ★★

**Hỏi:** Bạn viết `- echo ket qua: xong` trong `script`. Chuyện gì xảy ra?

**Đáp án chuẩn:** YAML hiểu dấu `:` theo sau khoảng trắng là **ánh xạ**, nên nó phân tích dòng đó thành cặp khoá-giá trị `echo ket qua` → `xong`, không phải một chuỗi lệnh. Kết quả: tệp không hợp lệ, hoặc tệ hơn, hợp lệ nhưng chạy khác ý định.

Nguyên nhân gốc: **YAML phân tích trước, shell chạy sau**. Ngoài `:`, các ký tự **mở đầu** cũng bị nuốt: `*` (tham chiếu anchor), `&` (định nghĩa anchor), `{` và `[` (ánh xạ và danh sách dạng gọn), `|` và `>` (chuỗi khối), `%` và `@`.

Hai cách sửa:

```yaml
script:
  # Cách 1: bọc nháy đơn
  - 'echo "ket qua: xong"'

  # Cách 2: chuỗi khối — dùng cho lệnh dài hoặc nhiều dòng
  - |
    if [ -d dist ]; then
      echo "co dist"
    fi
```

Phân biệt hai chuỗi khối: `|` **giữ** ký tự xuống dòng; `>` **gộp** các dòng thành một. Dùng `|` cho khối `if`/`for`; dùng `>` cho một lệnh dài nhiều tham số như `docker build`.

Quy tắc thực hành rẻ hơn việc nhớ danh sách 8 ký tự: **lệnh nào dài quá một dòng hoặc có dấu câu thì dùng chuỗi khối `|`**.

**Tiêu chí chấm:**
- 0đ: Không biết vì sao lỗi.
- 1đ: Biết phải bọc nháy.
- 2đ: Nêu đúng cơ chế YAML phân tích trước và biết cả hai cách sửa.
- 3đ: Như trên, **và** phân biệt đúng `|` với `>` kèm ca dùng mỗi cái, **và** nêu quy tắc thực hành.

**Câu hỏi đào sâu:** Làm sao biết trước khi đẩy commit? *(Gọi `ci/lint` — nó trả về `valid: false` kèm thông báo lỗi YAML. 1 giây thay cho một vòng đẩy-chờ 3–5 phút.)*

---

### Câu 10 — ★★★

**Hỏi:** `image` được khai ở `config.toml`, ở `default:`, và trong chính job. Cái nào thắng?

**Đáp án chuẩn:** **Trong job thắng** — quy tắc là **gần job nhất thì thắng**.

Ba nấc xếp theo khoảng cách tới job, và ba nấc ứng với ba phạm vi trách nhiệm:

| Nấc | Ai viết | Phạm vi |
|---|---|---|
| `config.toml` | Người vận hành runner | Mọi project dùng runner đó |
| `default:` | Người viết pipeline | Một project |
| Trong job | Người viết pipeline | Một job |

Quy tắc "gần nhất thắng" là quy tắc duy nhất tương thích với ba phạm vi lồng nhau ấy.

Điểm dễ nhầm nhất và là chỗ đạt 3 điểm: nấc gần hơn **THAY THẾ** nấc xa hơn, **không hợp nhất**. Khai `before_script` trong một job thì `before_script` ở `default:` bị **bỏ hoàn toàn** — job chạy **một** `before_script`, không phải hai nối tiếp.

Cùng quy tắc áp cho: `image`, `cache`, `artifacts`, `before_script`, `after_script`, `services`, `tags`.

**Cảnh báo bắt buộc nói kèm:** `variables` **không** theo quy tắc này. Nó có bộ quy tắc riêng với chín nguồn — instance, group, project, tệp, job, `dotenv`, biến hệ thống, nhập tay, pipeline cha — và còn có cờ `protected`/`masked` chen vào. Buổi 06 dành trọn cho nó.

**Tiêu chí chấm:**
- 0đ: Đoán sai thứ tự.
- 1đ: Trả lời đúng "trong job thắng" mà không giải thích.
- 2đ: Nêu đúng ba nấc và nguyên tắc gần nhất thắng.
- 3đ: Như trên, **và** nói rõ **thay thế chứ không hợp nhất** kèm ví dụ `before_script`, **và** cảnh báo `variables` có quy tắc riêng.

**Câu hỏi đào sâu:** Làm sao kiểm chắc mà không phải đoán? *(Gọi `ci/lint` với `include_merged_yaml: true` rồi đọc cấu hình từng job sau phân giải: `.jobs[] | {name, image, before_script}`. Từ buổi 10 trở đi, khi có `include` và `extends`, đây không còn là tiện lợi mà là điều kiện cần.)*

---

### Câu 11 — ★★★

**Hỏi:** Job ẩn dùng để làm gì? Khi nào **không** nên dùng?

**Đáp án chuẩn:** Job ẩn — tên bắt đầu bằng dấu chấm — không bao giờ chạy, nhưng nội dung vẫn được phân giải nên dùng làm **khuôn mẫu** cho `extends` và cho YAML anchor.

Giá trị: một ký tự `.` cho ta cơ chế dùng lại rẻ nhất trong GitLab CI, và nó tốn **0 giây** vì job ẩn không chạy.

```yaml
.mau-test:
  image: node:22-alpine
  before_script: [npm ci]
  cache:
    key: {files: [package-lock.json]}
    paths: [.npm/]

test-unit:
  extends: .mau-test
  script: [npm run test:unit]

test-e2e:
  extends: .mau-test
  script: [npm run test:e2e]
```

**Khi nào không nên dùng** — đây là phần đạt 3 điểm: khi chỉ có **một** job dùng nó. Job ẩn có giá trị khi từ hai job trở lên dùng chung. Dùng cho một job thì nó chỉ thêm một lớp gián tiếp: người đọc phải nhảy qua lại giữa hai chỗ trong tệp mà không đổi lại được gì. Đây là dạng trừu tượng hoá sớm, và nó làm tệp khó đọc hơn chứ không dễ hơn.

Rủi ro cần nêu: quên dấu chấm thì khuôn mẫu **chạy thật** và thường đỏ vì thiếu `script`. Ngược lại, thêm nhầm dấu chấm vào một job thật thì job **biến mất khỏi pipeline im lặng** — không lỗi, không cảnh báo.

**Tiêu chí chấm:**
- 0đ: Không biết job ẩn là gì.
- 1đ: Biết nó không chạy.
- 2đ: Nêu đúng công dụng làm khuôn mẫu kèm ví dụ.
- 3đ: Như trên, **và** nêu được ca **không** nên dùng (chỉ một job dùng), **và** nêu cả hai rủi ro về dấu chấm.

**Câu hỏi đào sâu:** Job ẩn với anchor YAML khác nhau chỗ nào? *(Anchor được YAML khai triển **trước** khi GitLab đọc, nên nó chỉ dùng được trong **cùng một tệp**. Job ẩn + `extends` do GitLab xử lý, nên nó vượt được ranh giới `include`. Buổi 10 xử lý đầy đủ, và đó là lý do khoá này dùng `extends` chứ không dùng anchor.)*

---

### Câu 12 — 🔥

**Hỏi:** Đội bạn nói pipeline chậm. Bạn làm gì đầu tiên?

**Đáp án chuẩn:** **Đo, không đoán.** Ba nhịp.

**Nhịp 1 — lập bản đồ phụ thuộc dữ liệu.** Với mỗi job, trả lời một câu: *"nó cần artifact của ai?"*. Bảng ấy cho ta **đường găng dữ liệu** — chuỗi phụ thuộc `artifacts` dài nhất, tức giới hạn dưới mà pipeline không thể nhanh hơn.

**Nhịp 2 — tính lãng phí hàng rào.**

```
lãng phí = tổng thời gian pipeline − đường găng dữ liệu
```

Con số này chính là số giây lấy lại được. Không có nó thì mọi đề xuất tối ưu đều là cảm nhận.

**Nhịp 3 — phân loại nguồn chậm.** Không phải mọi chậm đều là hàng rào:

| Nguồn chậm | Dấu hiệu | Buổi giải |
|---|---|---|
| Hàng rào stage | Lãng phí lớn ở nhịp 2 | 08 (`needs`) |
| Không đủ slot | `queued_duration` cao; job cùng stage không chồng lấn | 02, 13 |
| Pha `download_artifacts` | Job nhẹ mà `duration` cao | 01 (`dependencies: []`) |
| Cache không ăn | Log có `Failed to extract cache` | 05, 16–21 |
| Image nặng | Chi phí khởi tạo cao | 02, 25 |

Điểm để đạt 3 điểm: nói rõ rằng **trước khi bỏ một hàng rào phải hỏi nó có đang bảo đảm điều gì không**. Một stage `security` chặn stage `deploy` là **tính năng**, không phải lãng phí — buổi 35 dựng gate trên đúng cơ chế ấy. Và đường an toàn không phải gộp stage mà là dùng `needs` ở buổi 08, vì `needs` khai báo **tường minh** phụ thuộc thay vì xoá bỏ nó.

**Tiêu chí chấm:**
- 0đ: "Thêm runner cho nhanh."
- 1đ: Nói được là do nhiều stage.
- 2đ: Nêu đúng phép trừ lãng phí và lập được bản đồ phụ thuộc.
- 3đ: Đủ ba nhịp, **và** phân biệt được hàng rào lãng phí với hàng rào là **cổng kiểm soát**, **và** nêu `needs` thay vì gộp stage.

**Câu hỏi đào sâu:** Vì sao không gộp hai stage lại cho gọn? *(Vì gộp làm **mất** sự đảm bảo thứ tự mà một job nào đó có thể đang **ngầm** dựa vào — ví dụ job deploy ngầm dựa vào việc job security stage trước đã chạy. `needs` giữ được đảm bảo ấy vì nó khai báo tường minh, còn gộp stage thì xoá nó đi.)*

---

## V3. Câu chốt để nói khi phỏng vấn

> Bốn câu viết **nguyên văn, đúng ngữ điệu nói**. Mỗi câu chứa một con số hoặc một cơ chế.

**Câu 1 — khi được hỏi "`stage` để làm gì":**

> "`stage` chỉ là một hàng rào thời gian, nó chuyển không byte dữ liệu nào. Dữ liệu giữa hai job đi bằng artifacts — `stage` chỉ quyết định tập artifact nào được tải mặc định, và chính cái mặc định đó làm nhiều người tưởng `stage` chuyển dữ liệu. Chỗ này tôi kiểm bằng một câu hỏi: nếu bỏ khối `artifacts` của job trước đi, job sau còn thấy tệp không? Không thấy. Vậy cái chuyển dữ liệu không phải `stage`."

**Câu 2 — khi được hỏi "làm sao cho pipeline chạy song song":**

> "Đặt chung stage chỉ **cho phép** song song, chứ không tạo ra song song. Cái quyết định là `concurrent` trong `config.toml` của runner — tệp mà người viết pipeline thường không nhìn thấy. Tôi từng đo trên lab: sáu job cùng stage, mỗi job hai mươi giây, với `concurrent` bằng một thì stage mất một trăm hai mươi giây chứ không phải hai mươi. Nên khi ai nói 'tôi để chung stage cho nó chạy song song', câu hỏi ngược của tôi luôn là: `concurrent` của runner là bao nhiêu?"

**Câu 3 — khi được hỏi "bạn tối ưu pipeline thế nào":**

> "Tôi bắt đầu bằng một phép trừ. Lấy tổng thời gian pipeline trừ đi đường găng dữ liệu — tức chuỗi phụ thuộc artifacts dài nhất. Hiệu số đó là lãng phí hàng rào, và nó là số giây tôi có thể lấy lại. Trên một pipeline mẫu tôi đo được bảy mươi hai giây tổng, mười hai giây đường găng, tức sáu mươi giây bị vứt đi vì một job đóng gói phải chờ một job test mà nó chẳng cần gì. Nhân với bốn mươi lần chạy một ngày là gần chín trăm phút runner một tháng, chỉ cho một repo."

**Câu 4 — khi được hỏi "bạn kiểm tệp CI thế nào trước khi đẩy":**

> "Tôi gọi endpoint `ci/lint` và đọc danh sách job trả về, rồi so với danh sách job tôi nghĩ là có. Lý do là GitLab hiểu mọi khoá cấp trên cùng không nằm trong danh sách từ khoá dành riêng là một job — nên gõ sai `variables` thành `variabels` không báo lỗi, nó tạo một job rác và làm biến của tôi biến mất im lặng. Một lệnh `curl` mất một giây; một vòng đẩy commit rồi chờ pipeline mất ba tới năm phút. Từ khi có `include` và `extends` thì việc này không còn là tiện lợi nữa mà là bắt buộc, vì tệp tôi viết không còn là tệp GitLab chạy."

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
| ≥ 80% | Nắm vững. Giao BT3 (đo lãng phí trên repo thật) làm trước buổi 08 |
| 60–79% | Đạt. Đọc lại quy tắc bị mất điểm trước buổi 04 |
| 40–59% | Chưa đạt. Làm lại bước lab tương ứng ở nhà |
| < 40% | Chưa đạt. Học lại cả buổi — buổi 08 dựng thẳng lên mô hình hàng rào này |

**Bảng lỗi làm trần điểm là 1:**

| Lỗi | Vì sao nghiêm trọng |
|---|---|
| "`stage` chuyển dữ liệu giữa các job" | Mâu thuẫn trực tiếp với buổi 01 QT 5.1; dẫn tới pipeline bỏ `artifacts` và hỏng ngẫu nhiên |
| "Job cùng stage **luôn** chạy song song" | Bỏ qua toàn bộ buổi 02; dẫn tới ước lượng thời gian pipeline sai hệ số |
| Nói "chậm lắm", "nhanh hơn nhiều" mà khi hỏi lại vẫn không có số | Vi phạm nguyên tắc của khoá |

---

## V5. Bài tập về nhà

### BTVN 1. Bản đồ phụ thuộc của repo thật

Lấy pipeline thật của đội mình. Với **mỗi** job, trả lời: *"nó cần artifact của ai?"*

**Nộp:** bảng ≥ 5 job với bốn cột — job · stage · cần artifact của ai · **thực sự phải chờ ai**. Cột thứ tư trừ cột thứ ba chính là hàng rào vô ích.

> Đây là hiện vật có giá trị dài hạn nhất của buổi. Ở buổi 08 nó biến thẳng thành các dòng `needs:`.

### BTVN 2. Lãng phí hàng rào của repo thật

Từ bảng ở BTVN 1, tính ba con số: tổng thời gian pipeline, đường găng dữ liệu, và hiệu của chúng.

**Nộp:** ba con số, và quy đổi: lãng phí × số lần chạy pipeline một ngày × 22 ngày = bao nhiêu **phút runner** một tháng.

### BTVN 3. Tìm job rác

Gọi `ci/lint` cho **ba** repo khác nhau (của mình hoặc của đội) và so danh sách job trả về với danh sách bạn nghĩ là có.

**Nộp:** kết quả ba repo. Nếu tìm được job rác, ghi tên nó và ghi cấu hình nào đã bị mất im lặng vì lỗi chính tả đó.

### BTVN 4. Chuẩn bị cho buổi 04

Trả lời ba câu sau bằng viết, mỗi câu 3–5 dòng. Mang theo vào buổi 04.

1. Liệt kê **ba** cách khác nhau làm cho một job **không chạy** trong một lần chạy pipeline. Với mỗi cách, đoán xem job đó hiện lên giao diện với trạng thái gì — không có mặt, `skipped`, hay `manual`?
2. Mở một pipeline gần đây và tìm biến `CI_PIPELINE_SOURCE`. Nó nhận những giá trị nào? Liệt kê ít nhất **bốn** giá trị bạn tìm được hoặc đoán được.
3. Nếu một job **không chạy**, các job ở stage sau phụ thuộc artifact của nó sẽ ra sao — chạy bình thường, bị bỏ qua, hay đỏ? Ghi phỏng đoán kèm lập luận dựa trên buổi 01 QT 5.3 và buổi 03 QT 5.1.

**Ba câu này dẫn vào đâu:** câu 1 dẫn vào §4 buổi 04 phân biệt `rules` với `only/except` với `when: manual` — ba cách "không chạy" có ba trạng thái khác nhau và hệ quả khác nhau; câu 2 dẫn vào §5 buổi 04 với **bảng chân trị 12 ca kích hoạt × `rules`**, bảng cần nhất của cả giai đoạn 1; câu 3 dẫn vào §6 buổi 04 về job bị bỏ qua và `allow_failure` — và nó là chỗ mô hình hàng rào của hôm nay gặp mô hình `rules` của buổi sau.
{% endraw %}
