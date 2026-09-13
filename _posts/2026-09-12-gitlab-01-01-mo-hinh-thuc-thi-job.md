---
layout: post
title: "[Bài 01] Kiến Trúc GitLab CI/CD & Mô Hình Thực Thi Job: GitLab Server, Runner, Coordinator & Vòng Đời Pipeline"
date: 2026-09-12 09:30:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-01
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 1
difficulty: Intermediate
thumbnail: "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.01] Hướng dẫn chuyên sâu Kiến Trúc GitLab CI/CD & Mô Hình Thực Thi Job: GitLab Server, Runner, Coordinator & Vòng Đời Pipeline: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Kiến Trúc GitLab CI/CD & Mô Hình Thực Thi Job: GitLab Server, Runner, Coordinator & Vòng Đời Pipeline."
  - "Thiết kế CI/CD Pipeline chuẩn Enterprise với kiến trúc DAG, tối ưu hóa thời gian build và caching hiệu quả."
  - "Bảo mật chuỗi cung ứng phần mềm với SAST/DAST, Container Scanning và OIDC Authentication."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 01] KIẾN TRÚC GITLAB CI/CD & MÔ HÌNH THỰC THI JOB: GITLAB SERVER, RUNNER, COORDINATOR & VÒNG ĐỜI PIPELINE

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · Docker Engine 27.x.
> Mọi đoạn YAML trong tệp này dán được vào `.gitlab-ci.yml` và chạy trong dưới 60 giây.

---





Đây là buổi mở đầu nên không có buổi trước để ôn. Thay vào đó, giảng viên hỏi năm câu dưới đây và **gọi ngẫu nhiên**. Năm câu này không kiểm tra kiến thức GitLab — chúng kiểm tra đúng năm mảnh nền mà toàn bộ buổi hôm nay dựng lên. Học viên trả lời sai câu nào thì giảng viên đánh dấu, vì câu đó sẽ quay lại làm học viên tắc ở lab.

| # | Câu hỏi | Đáp án vắn tắt | Nó dẫn vào đâu |
|---|---|---|---|
| 1 | Container khác máy ảo ở chỗ nào | Container chia sẻ nhân của máy chủ, cô lập bằng namespace và cgroup. Điều quan trọng cho hôm nay: **hệ tệp bên trong container biến mất khi container bị xoá** | §4, QT 4.1 |
| 2 | `git clone` và `git fetch` khác nhau thế nào | `clone` tạo một kho mới từ số 0; `fetch` cập nhật một kho đã có. Runner dùng cái nào là một **lựa chọn cấu hình**, không phải mặc định bất biến | §5, `GIT_STRATEGY` |
| 3 | Mã thoát của một lệnh Linux nghĩa là gì | `0` là thành công, khác `0` là thất bại. Đây là **toàn bộ** thông tin mà runner dùng để quyết định job xanh hay đỏ | §5, QT 5.4 và §7 |
| 4 | Một tiến trình con thấy được biến môi trường nào của tiến trình cha | Thấy các biến đã `export`. Nhưng **hai shell anh em không thấy biến của nhau** — shell B không thấy `export` của shell A | §4, QT 4.3 |
| 5 | Trong một container, `localhost` trỏ tới đâu | Trỏ tới **chính container đó**, không phải máy chủ và không phải container khác | §6, QT 6.2 |

### 0.2. Vì sao buổi này là buổi đầu tiên

Hầu hết học viên đến khoá này đã viết được một `.gitlab-ci.yml` chạy được. Cái thiếu không phải cú pháp — cú pháp tra 10 phút là ra. Cái thiếu là **mô hình về nơi job chạy**.

Không có mô hình đó, mọi lỗi CI đều trở thành thử-và-sai: thêm một dòng, đẩy commit, chờ 4 phút, xem kết quả, đoán tiếp. Một buổi chiều đi theo cách đó gỡ được hai lỗi. Có mô hình đó, gỡ lỗi trở thành thu hẹp vùng nghi ngờ — và phần lớn lỗi xác định được **trước khi đẩy commit đầu tiên**.

**Luận đề trung tâm.**

> **Một job không chạy "trong GitLab". Nó chạy trong một môi trường DÙNG MỘT LẦN do runner dựng lên, và mọi thứ job cần chỉ vào được qua BỐN ĐƯỜNG: mã nguồn từ git, cache, artifact của job trước, và biến môi trường. Gần như mọi lỗi CI của người mới là do tưởng có đường thứ năm.**

Toàn bộ buổi hôm nay là việc dựng và kiểm chứng sơ đồ này:

```
        BỐN ĐƯỜNG VÀO                MÔI TRƯỜNG DÙNG MỘT LẦN            HAI ĐƯỜNG RA
   ┌──────────────────────┐        ┌────────────────────────┐      ┌──────────────────┐
   │ 1. git clone/fetch   │───────▶│                        │─────▶│ 1. artifacts     │
   │ 2. cache (KHÔNG hứa) │───────▶│   container của job    │─────▶│ 2. mã thoát      │
   │ 3. artifact job trước│───────▶│   (xoá sạch khi xong)  │      └──────────────────┘
   │ 4. biến môi trường   │───────▶│                        │
   └──────────────────────┘        └────────────────────────┘
                                    mọi thứ khác ghi ra đây
                                          → MẤT
```

**Ba câu hỏi trung tâm của buổi:**

1. Khi một job hỏng, ta biết nó hỏng ở **đâu** trong vòng đời của nó bằng cách nào?
2. Cái gì **chắc chắn** có mặt trong job, và cái gì chỉ **có thể** có mặt?
3. Vì sao một job **xanh** không chứng minh được việc đã làm xong?

---



| # | Làm được gì | Hiện vật chứng minh |
|---|---|---|
| LĐ1 | Mở log một job bất kỳ và chỉ ra nó đang ở pha nào trong tám pha, kèm thời lượng từng pha | Bảng tám pha đo từ log thật, lab bước 1 |
| LĐ2 | Nói được cái gì đi qua ranh giới giữa hai job và cái gì không, không cần tra tài liệu | Bốn ca thực nghiệm ở lab bước 2 |
| LĐ3 | Phân biệt được `cache` với `artifacts` và chọn đúng cái cần dùng cho một tình huống cho trước | Lab bước 2 checkpoint 5 |
| LĐ4 | Tái hiện được bốn kiểu hỏng im lặng và chỉ ra dấu hiệu nhận biết từng kiểu | Bốn bằng chứng ở lab bước 3 và 4 |
| LĐ5 | Viết được khẳng định biến một bước hỏng im lặng thành hỏng ồn ào | `.gitlab-ci.yml` cuối cùng ở lab bước 5 |
| LĐ6 | Chẩn đoán được một job `pending` mà không có log, và biết mất bao lâu mới có ai phát hiện | Lab bước 3 ca 1, và vấn đáp câu 7 |
| LĐ7 | Truyền được một giá trị từ job này sang job sau bằng cơ chế đúng | Lab bước 4, phần `dotenv` |

---



| Cần biết | Mức yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Chạy được `docker run` và đọc được `Dockerfile` | Vận dụng | Bất kỳ tài liệu Docker cơ bản nào; đủ để hiểu "container xoá đi thì mất" |
| Git ở mức nhánh, commit, push | Vận dụng | — |
| Mã thoát và `echo $?` trong shell | Vận dụng | §0.1 câu 3 |
| Biến môi trường và `export` | Nhớ | §0.1 câu 4 |
| Đọc YAML: thụt lề, danh sách, ánh xạ | Vận dụng | YAML có đúng ba cấu trúc; học 15 phút là đủ cho cả khoá |
| Gọi API bằng `curl` và lọc bằng `jq` | Nhớ | Mọi checkpoint của khoá dùng hai công cụ này; xem `00-tong-quan/02-moi-truong-lab.md` |
| Môi trường lab đã dựng và `make kiem-tra` in toàn ĐẠT | Bắt buộc | `00-tong-quan/02-moi-truong-lab.md` |

---



### 3.1. Đối chiếu thuật ngữ

Khoá này **dùng thẳng tiếng Anh** cho từ khoá YAML, vì học viên gõ đúng những chữ đó vào file cấu hình. Việt hoá chúng chỉ gây thêm một lớp dịch trong đầu. Các khái niệm không phải từ khoá YAML thì dùng tiếng Việt, và tiếng Anh để trong ngoặc — vì học viên sẽ phỏng vấn bằng tiếng Anh.

| Tiếng Việt | Tiếng Anh | Trong bài dùng gì | Ghi chú |
|---|---|---|---|
| công việc | job | `job` | Đơn vị nhỏ nhất được runner thực thi |
| chuỗi công việc | pipeline | `pipeline` | Tập hợp job của một lần chạy |
| chặng | stage | `stage` | Nhóm job chạy song song với nhau |
| bộ chạy | runner | `runner` | Tiến trình nhận job và giao cho executor |
| bộ thực thi | executor | `executor` | Cơ chế runner dùng để tạo môi trường chạy |
| hiện vật | artifact | `artifacts` | Tệp job sinh ra và GitLab giữ lại |
| bộ nhớ đệm | cache | `cache` | Tệp giữ lại để lần sau chạy nhanh hơn |
| nhãn định tuyến | tag | `tags` | Cơ chế ghép job với runner |
| ảnh nền | image | `image` | Image container mà job chạy trong đó |
| môi trường dùng một lần | ephemeral environment | tiếng Việt | Dựng ra, dùng, rồi xoá |
| pha | phase / step | tiếng Việt | Một trong tám giai đoạn của vòng đời job |
| mã thoát | exit code | tiếng Việt | Số trả về của lệnh; `0` là thành công |
| khẳng định | assertion / assert | tiếng Việt | Lệnh kiểm tra tự làm job đỏ khi sai |
| hỏng im lặng | silent failure | tiếng Việt | Hỏng mà không có gì báo |
| bản sao nông | shallow clone | tiếng Việt | Clone chỉ lấy `n` commit gần nhất |
| đường găng | critical path | tiếng Việt | Chuỗi phụ thuộc dài nhất quyết định tổng thời gian |
| thư mục dự án | project directory / build dir | tiếng Việt | Nơi runner đặt mã nguồn trong job |



Đây là mô hình quan trọng nhất của cả giai đoạn 1. Nó nói: **ranh giới của một job có đúng sáu lỗ thủng, và ta biết cả sáu**. Bốn lỗ để dữ liệu vào, hai lỗ để dữ liệu ra. Không có lỗ nào khác.

Giá trị thực dụng của mô hình: khi một job không có thứ nó cần, câu hỏi không còn là "sao lại thiếu" mà là **"nó lẽ ra vào qua đường nào trong bốn đường, và đường đó có được cấu hình không"**. Câu hỏi thứ hai trả lời được trong 30 giây; câu hỏi thứ nhất trả lời được sau nửa buổi chiều.

Mô hình này quay lại ở buổi 05 (artifact và cache chi tiết), buổi 08 (`needs` đổi đường thứ ba), và buổi 22 (monorepo, nơi đường thứ nhất trở thành vấn đề).

### 3.3. Mô hình tư duy 2: tám pha

Một job không phải một khối liền. Nó là tám pha nối tiếp, và **log job in ra tên từng pha**. Mỗi lỗi thuộc về đúng một pha.

Giá trị thực dụng: xác định pha là xác định nhóm nguyên nhân. Lỗi ở pha lấy mã nguồn là lỗi quyền hoặc mạng — sửa code không giúp gì. Lỗi ở pha tải artifact là lỗi phụ thuộc giữa job — sửa `script` không giúp gì. Người mới hay sửa `script` cho mọi loại lỗi vì `script` là phần duy nhất họ viết.

Mô hình này quay lại ở buổi 07 (gỡ rối có hệ thống), buổi 14 (tối ưu — vì muốn rút ngắn thì phải biết thời gian đi vào pha nào), buổi 47 (sự cố runner — hầu hết nằm ở hai pha đầu).

### 3.4. Mô hình tư duy 3: xanh không phải bằng chứng

Trạng thái của một job là kết quả của **mã thoát**, không phải của công việc. Runner không biết job "đáng lẽ" phải làm gì; nó chỉ biết lệnh cuối cùng trả về `0` hay khác `0`.

Giá trị thực dụng: mọi bước quan trọng phải kèm một khẳng định. Không có khẳng định thì bước đó có thể hỏng mà không ai biết — và đó là loại hỏng đắt nhất, vì thời gian phát hiện tính bằng tuần chứ không bằng phút.

Mô hình này là chủ đề xuyên suốt cả khoá. Nó quay lại rõ nhất ở buổi 30 và 35, nơi một job quét bảo mật "xanh" có thể nghĩa là quét sạch, mà cũng có thể nghĩa là công cụ quét không chạy.

---

### 1.1. Vòng đời một job: tám pha (10 phút)

### 4.1. Tám pha, và pha nào là của học viên

Khi runner nhận một job, nó chạy tám pha theo thứ tự cố định. Bảng dưới đây ghi tên pha trong tài liệu runner, dòng tiêu đề tương ứng trong log, và **nhóm nguyên nhân khi pha đó hỏng** — cột cuối là cột có giá trị nhất.

| # | Tên pha | Dòng trong log job | Hỏng ở đây nghĩa là gì |
|---|---|---|---|
| 1 | `prepare_executor` | `Preparing the "docker" executor` | Không kéo được `image`, không có quyền với Docker, runner cấu hình sai. **Không liên quan tới code** |
| 2 | `prepare_script` | `Preparing environment` | Shell trong image không có, biến file không ghi được. Hiếm, nhưng khi gặp thì rất khó đoán |
| 3 | `get_sources` | `Getting source from Git repository` | Không xác thực được với GitLab, không phân giải được tên miền, `GIT_STRATEGY` sai. **Không liên quan tới code** |
| 4 | `restore_cache` | `Restoring cache` | Gần như **không bao giờ làm job đỏ** — xem QT 5.2 |
| 5 | `download_artifacts` | `Downloading artifacts for <job>` | Job phụ thuộc không sinh artifact, hoặc artifact đã hết hạn |
| 6 | `step_script` | `Executing "step_script" stage of the job script` | **Pha duy nhất chứa lệnh của học viên.** `before_script` và `script` đều nằm trong pha này |
| 7 | `after_script` | `Running after_script` | Chạy trong shell mới — xem QT 4.3 |
| 8 | `archive_cache` + `upload_artifacts` | `Saving cache for successful job` · `Uploading artifacts for successful job` | Đường dẫn `paths` không khớp gì, hoặc vượt hạn mức kích thước |

Sau pha 8 còn một pha dọn dẹp (`cleanup_file_variables`, log in `Cleaning up project directory and file based variables`) và dòng cuối `Job succeeded`.

**Nguyên lý cốt lõi:** Job chạy trong một môi trường **dùng một lần**: mọi thứ ghi ra ngoài thư mục dự án đều biến mất khi job kết thúc, và ngay cả thư mục dự án cũng không được đảm bảo còn nguyên ở job sau.

**Giải thích cơ chế ngầm:** Với executor `docker`, runner tạo một container mới cho mỗi job, chạy tám pha trong đó, rồi xoá container. Hệ tệp của container là một lớp ghi tạm nằm trên image — xoá container là xoá lớp đó. Không có cơ chế nào tự động chuyển lớp ghi ấy sang job kế tiếp. Với executor `kubernetes` cũng vậy: mỗi job là một pod mới, pod bị xoá sau khi job xong. Chỉ executor `shell` là ngoại lệ, và ngoại lệ đó lại là nguồn của một lớp lỗi khác — xem QT 6.1.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Job thứ hai báo `No such file or directory` với một tệp mà job thứ nhất rõ ràng đã tạo và log của job thứ nhất có in ra tên tệp đó. Đây là ca chiếm nhiều thời gian nhất của tuần đầu tiên, vì học viên đọc log job 1 thấy đúng, đọc log job 2 thấy sai, và kết luận là "GitLab lỗi".

**Minh hoạ.**

```yaml
# Ca thực nghiệm: chứng minh /tmp không đi qua ranh giới job
stages: [a, b]

ghi-tep:
  stage: a
  image: alpine:3.20
  script:
    - echo "noi-dung-quan-trong" > /tmp/du-lieu.txt
    - echo "đã ghi:" && cat /tmp/du-lieu.txt

doc-tep:
  stage: b
  image: alpine:3.20
  script:
    # Job này ĐỎ. Đó là kết quả đúng và là điều cần thấy.
    - cat /tmp/du-lieu.txt
```

### 4.2. Đọc log theo pha

**Nguyên lý cốt lõi:** Một job chạy đúng **tám pha** theo thứ tự cố định, log job in tên từng pha, và xác định được pha hỏng là xác định được nhóm nguyên nhân — nhờ đó bỏ qua được phần lớn các giả thuyết sai.

**Giải thích cơ chế ngầm:** Runner phát ra một dòng tiêu đề trước mỗi pha, và dòng đó có màu riêng trong giao diện. Vì thứ tự pha cố định, dòng tiêu đề cuối cùng xuất hiện trước thông báo lỗi cho biết chính xác lỗi thuộc pha nào. Đây là thông tin miễn phí mà phần lớn người dùng không đọc, vì họ cuộn thẳng xuống cuối log tìm chữ `ERROR`.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Học viên sửa `script` năm lần liên tiếp mà lỗi không đổi, vì lỗi nằm ở pha 1 hoặc pha 3 — `script` chưa hề được chạy. Cách nhận ra trong 5 giây: nếu trong log **không có** dòng `Executing "step_script" stage of the job script` thì lệnh của học viên chưa chạy lần nào.

**Minh hoạ.**

```bash
# Lấy log job qua API và chỉ in các dòng tiêu đề pha.
# Đây là công cụ dùng lại ở lab bước 1 để đo thời lượng từng pha.
JOB_ID=123
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB/api/v4/projects/$PID/jobs/$JOB_ID/trace" \
| grep -aE 'Preparing the|Preparing environment|Getting source|Restoring cache|Downloading artifacts|Executing "step_script"|Running after_script|Saving cache|Uploading artifacts|Cleaning up|Job succeeded|Job failed'
```

**Ghi chú loại (a) và giới hạn của nó.** Tên tám pha lấy từ tài liệu GitLab Runner 17.x. Tên pha **đã đổi giữa các bản runner** trong quá khứ, và ba pha phụ không phải lúc nào cũng in ra. Vì vậy bài lab bước 1 **đo tám pha từ log thật** thay vì chép bảng này — đó là quy tắc chung của khoá với mọi hành vi phụ thuộc phiên bản.

### 4.3. `after_script` là một shell khác

**Nguyên lý cốt lõi:** `after_script` chạy trong một shell **mới**: nó không thấy biến do `script` tạo ra, thư mục làm việc đã quay về mặc định, và nó có hạn giờ riêng.

**Giải thích cơ chế ngầm:** Runner sinh ra hai script riêng biệt và chạy chúng như hai tiến trình. Biến `export` trong tiến trình A không tồn tại trong tiến trình B — đây đúng là câu 4 của phần kiểm tra đầu vào. `after_script` được thiết kế để dọn dẹp và thu thập bằng chứng, nên nó phải chạy được **kể cả khi `script` đã chết**; muốn thế thì nó không thể nằm trong cùng một shell.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Một biến in ra rỗng trong `after_script` dù `script` đã `export` nó ngay dòng trên. Hoặc: `after_script` chạy `cat build/log.txt` không thấy tệp, vì `script` đã `cd` sang thư mục khác rồi tạo tệp ở đó.

**Minh hoạ.**

```yaml
kiem-chung-after-script:
  image: alpine:3.20
  script:
    - export BIEN_CUA_TOI="gia-tri"
    - mkdir -p sau && cd sau && echo noi-dung > tep.txt
    - echo "trong script, BIEN_CUA_TOI = $BIEN_CUA_TOI"
    - echo "trong script, pwd = $(pwd)"
  after_script:
    # Cả hai dòng dưới đây đều KHÔNG cho kết quả như mong đợi
    - echo "trong after_script, BIEN_CUA_TOI = [$BIEN_CUA_TOI]"   # rỗng
    - echo "trong after_script, pwd = $(pwd)"                      # thư mục dự án, không phải sau/
    # Cách đúng: truyền qua TỆP, vì tệp trong thư mục dự án thì hai shell cùng thấy
    - cat trang-thai.env 2>/dev/null || echo "chưa có trang-thai.env"
```

Cách đúng để `after_script` biết được thứ `script` tạo ra là **ghi ra tệp trong thư mục dự án**:

```yaml
script:
  - echo "PHIEN_BAN=1.2.3" > trang-thai.env
after_script:
  - source trang-thai.env && echo "phiên bản là $PHIEN_BAN"
```

**Con số cần nhớ.** Hạn giờ mặc định của `after_script` là **5 phút**, đổi bằng biến `RUNNER_AFTER_SCRIPT_TIMEOUT`. Con số này **không phổ quát**: nó phụ thuộc phiên bản runner, và một số bản cũ không có biến đó. Đừng thiết kế `after_script` chạy gần 5 phút — nếu việc dọn dẹp tốn tới mức đó thì nó nên là một job riêng.

---

### 1.2. Bốn đường vào và hai đường ra (11 phút)

### 5.1. Bốn đường vào

**Nguyên lý cốt lõi:** Chỉ có **bốn** đường đưa dữ liệu vào một job: mã nguồn từ git, `cache`, `artifacts` của job trước, và biến môi trường. Không có đường thứ năm.

**Giải thích cơ chế ngầm:** Ba pha đầu tiên trong tám pha của QT 4.2 chính là ba đường vào đầu tiên, chạy đúng theo thứ tự đó: `get_sources` → `restore_cache` → `download_artifacts`. Đường thứ tư — biến môi trường — được nạp ở pha `prepare_script`, tức trước cả ba đường kia. Sau khi bốn pha ấy chạy xong, không còn cơ chế nào của runner đưa thêm gì vào nữa; mọi thứ khác phải do chính `script` đi lấy về (và khi ấy nó là việc của học viên, không phải của runner).

Bảng dưới đây là bảng cần thuộc:

| Đường | Cơ chế | Có được đảm bảo không | Kích thước điển hình | Cấu hình bằng |
|---|---|---|---|---|
| 1. Mã nguồn | `git clone` hoặc `git fetch` | **Có** — job không có mã nguồn thì đỏ ở pha 3 | Bằng repo | `GIT_STRATEGY`, `GIT_DEPTH` |
| 2. Cache | Giải nén tệp nén từ kho cache | **KHÔNG** | 50 MB – 2 GB | `cache:key`, `cache:paths`, `cache:policy` |
| 3. Artifact | Tải từ GitLab | **Có**, nếu job nguồn thành công và chưa hết hạn | 1 MB – 500 MB | `artifacts:paths`, `dependencies`, `needs` |
| 4. Biến | Đặt vào môi trường tiến trình | **Có** | Vài KB | Biến project/group/instance, `variables:` |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Học viên hỏi "làm sao để job này dùng được tệp X" mà tệp X không đến từ bốn đường nào — ví dụ tệp nằm trên máy học viên, hoặc trên một server nội bộ, hoặc do job trước ghi vào `/tmp`. Câu trả lời luôn là một trong ba: đưa nó vào git, đưa nó thành artifact, hoặc để `script` tự tải nó về (và khi đó phải xử lý xác thực và mạng — buổi 47 nói về chuyện này khi runner bị chặn ra ngoài).

**Minh hoạ.**

```yaml
# Bốn đường vào, đủ cả bốn, trong một job
variables:
  DUONG_4: "biến môi trường"        # đường 4

lay-du-lieu:
  image: alpine:3.20
  # đường 1: mã nguồn — mặc định luôn có, không cần khai báo
  cache:                            # đường 2
    key:
      files: [package-lock.json]
    paths: [.npm/]
    policy: pull
  dependencies: [job-truoc]         # đường 3
  script:
    - ls -la .                      # đường 1: thấy mã nguồn
    - ls -la .npm/ 2>/dev/null || echo "cache chưa có — job VẪN XANH"
    - ls -la dist/                  # đường 3: artifact của job-truoc
    - echo "$DUONG_4"               # đường 4
```

### 5.2. Cache là tối ưu, artifact là hợp đồng

Đây là quy tắc bị vi phạm nhiều nhất trong cả khoá, và nó là nguyên nhân của loại lỗi khó chịu nhất: pipeline chạy tốt nhiều lần rồi đột nhiên hỏng mà không ai đổi gì.

**Nguyên lý cốt lõi:** `cache` là tối ưu tốc độ, `artifacts` là hợp đồng giữa hai job. Cache **không** được đảm bảo tồn tại, và runner **không** báo lỗi khi thiếu nó.

**Giải thích cơ chế ngầm:** Cache được lưu theo `cache:key` và — nếu không cấu hình kho dùng chung — nó nằm **trên chính runner đã chạy job**. Không có gì bảo đảm job sau chạy trên cùng runner ấy. Ngay cả khi có kho dùng chung, cache vẫn có thể đã bị dọn, hoặc `cache:key` đã đổi vì tệp khoá đổi. Khi không tìm thấy, runner ghi một dòng vào log và **chạy tiếp bình thường**. Artifact thì ngược lại: nó nằm trên GitLab, có thời hạn khai báo được, và job phụ thuộc **đỏ** nếu artifact cần mà không có.

Bảng đối chiếu:

| | `cache` | `artifacts` |
|---|---|---|
| Lưu ở đâu | Trên runner, hoặc kho dùng chung nếu cấu hình | Trên GitLab |
| Có đảm bảo tồn tại | **Không** | Có |
| Thiếu thì job | Chạy tiếp, chỉ chậm hơn | Đỏ ở pha 5 |
| Đi giữa các pipeline | Có — đó là mục đích của nó | Không (trừ khi tải thủ công) |
| Đi giữa các job trong một pipeline | Có, nhưng **không đảm bảo** | Có, **đảm bảo** |
| Thời hạn | Do runner dọn, không khai báo được chính xác | `expire_in`, khai báo được |
| Dùng cho | Thư mục phụ thuộc tải từ mạng: `.npm/`, `~/.m2/`, `$GOMODCACHE` | Kết quả build: `dist/`, `target/*.jar`, báo cáo test |

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline chạy tốt 9 lần, lần thứ 10 hỏng ở job `test` với lỗi thiếu module. Trong log 9 lần đầu có dòng `Successfully extracted cache`; lần thứ 10 có `Failed to extract cache` hoặc không có dòng nào. Không ai đổi code, không ai đổi cấu hình — cái đổi là runner nào nhận job.

**Con số cần nhớ.** Cache miss làm job **thất bại 0 lần** khi dùng đúng. Nó chỉ làm job chậm thêm đúng bằng thời gian tải lại phụ thuộc. Nếu cache miss làm job của bạn đỏ, đó là bằng chứng bạn đang dùng cache như artifact.

**Minh hoạ.**

```yaml
# SAI — job test trông chờ node_modules do job build để lại trong cache
build:
  script: [npm ci]
  cache:
    key: $CI_COMMIT_REF_SLUG
    paths: [node_modules/]
test:
  script: [npx jest]          # đỏ ngẫu nhiên khi cache miss

# ĐÚNG — cái job sau CẦN thì đi bằng artifact; cache chỉ để build nhanh hơn
build:
  script: [npm ci]
  cache:
    key:
      files: [package-lock.json]   # khoá theo nội dung lockfile
    paths: [.npm/]                 # kho tải về, KHÔNG phải node_modules
    policy: pull-push
  artifacts:
    paths: [node_modules/]
    expire_in: 1 hour
test:
  needs: [build]
  script: [npx jest]
```

### 5.3. Artifact tải về nhiều hơn học viên nghĩ

**Nguyên lý cốt lõi:** Mặc định một job tải artifact của **mọi job ở các stage trước**; `needs` và `dependencies` thu hẹp tập đó, và `dependencies: []` tắt hẳn.

**Giải thích cơ chế ngầm:** Mặc định này có lý do lịch sử: nó làm pipeline đơn giản chạy được mà không cần khai báo gì. Cái giá là mỗi job phải tải toàn bộ artifact của các stage trước, kể cả những artifact nó không đụng tới. Trong một pipeline có job build sinh 300 MB, mọi job ở stage sau — kể cả job chỉ chạy `helm lint` — đều tải đủ 300 MB đó.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Trong log của một job có nhiều dòng `Downloading artifacts for ...` với tên những job chẳng liên quan, và pha 5 chiếm 30–60 giây trong một job mà `script` chỉ chạy 5 giây. Cách phát hiện nhanh: mở job nhẹ nhất của pipeline và xem tổng thời gian của nó — nếu nó lâu bất thường thì gần như chắc chắn là pha `download_artifacts`.

**Minh hoạ.**

```yaml
# Job này chỉ cần mã nguồn, không cần kết quả build của ai
lint-yaml:
  stage: kiem-tra
  image: alpine:3.20
  dependencies: []          # tắt hẳn pha download_artifacts
  script:
    - apk add --no-cache yamllint >/dev/null
    - yamllint .gitlab-ci.yml

# Job này chỉ cần artifact của ĐÚNG một job
dong-goi:
  stage: dong-goi
  needs: ["build-backend"]  # với needs, artifact chỉ đến từ job được liệt kê
  script:
    - ls -la target/
```

> **Ghi chú về `needs` và `dependencies`.** Hai từ khoá này chồng lấn nhau và đây là chỗ hay nhầm. Nói ngắn: `needs` đổi **thứ tự chạy** và đồng thời thu hẹp artifact; `dependencies` chỉ thu hẹp artifact mà không đổi thứ tự. Buổi 08 xử lý đầy đủ chuyện này. Hôm nay chỉ cần nhớ `dependencies: []` là công tắc tắt.

### 5.4. Hai đường ra — và log không phải một trong hai

**Nguyên lý cốt lõi:** Chỉ có **hai** đường ra khỏi job: `artifacts` và **mã thoát**. Log không phải đường ra — không job nào đọc được log của job khác một cách có cấu trúc.

**Giải thích cơ chế ngầm:** Runner báo về GitLab đúng hai thứ khi job kết thúc: tập tệp được khai báo trong `artifacts`, và mã thoát của script. Log được lưu để người đọc, không phải để máy đọc. GitLab không phân tích log để rút giá trị ra, trừ đúng một ngoại lệ được thiết kế riêng: `artifacts:reports:dotenv` — và đó là một dạng artifact, không phải log.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Trong `.gitlab-ci.yml` có `echo "VERSION=1.2.3"` ở job A và job B mong đợi biến `VERSION` có giá trị. Job B chạy với `VERSION` rỗng, và vì shell không báo lỗi khi biến rỗng nên job B thường **vẫn xanh** — nó chỉ tạo ra một hiện vật có tên sai. Đây là ca hỏng im lặng không chặn, loại nguy hiểm nhất theo QT 7.1.

**Minh hoạ.**

```yaml
# ĐÚNG — cơ chế duy nhất để truyền một giá trị sang job sau
tinh-phien-ban:
  stage: chuan-bi
  image: alpine:3.20
  script:
    - PHIEN_BAN="1.2.$CI_PIPELINE_IID"
    - echo "PHIEN_BAN=$PHIEN_BAN" > bien.env
    - cat bien.env
  artifacts:
    reports:
      dotenv: bien.env

dung-phien-ban:
  stage: dong-goi
  needs: ["tinh-phien-ban"]
  image: alpine:3.20
  script:
    # Khẳng định trước khi dùng — xem QT 7.3
    - test -n "$PHIEN_BAN" || { echo "PHIEN_BAN rỗng, dừng"; exit 1; }
    - echo "đóng gói phiên bản $PHIEN_BAN"
```

**Ba giới hạn của `dotenv` cần biết ngay từ hôm nay**, vì học viên sẽ gặp cả ba trong tháng đầu đi làm: giá trị bị giới hạn kích thước (bậc vài KB, không nhét được nội dung tệp vào); biến truyền qua `dotenv` **không** tự động là biến masked, nên đừng truyền secret qua nó (buổi 29 nói kỹ); và biến chỉ tới được job có `needs` hoặc ở stage sau, không đi ngược lên.

---

### 1.3. Runner, executor và định tuyến job (8 phút)

Buổi 02 dành trọn cho runner và executor. Hôm nay chỉ lấy đúng ba điều mà thiếu chúng thì không hiểu nổi log job.

### 6.1. Executor quyết định cái gì tồn tại giữa hai job

**Nguyên lý cốt lõi:** `executor` quyết định **cái gì tồn tại giữa hai job**: `shell` giữ lại trạng thái của máy, `docker` và `kubernetes` thì không.

**Giải thích cơ chế ngầm:** Runner là tiến trình nhận job từ GitLab; executor là cơ chế nó dùng để tạo môi trường chạy. Với `shell`, môi trường chạy là **chính máy đang cài runner** — mọi thứ job cài đặt, mọi tệp job ghi ra ngoài thư mục dự án, mọi biến ghi vào profile đều còn nguyên cho job kế tiếp. Với `docker`, môi trường là một container mới toanh dựng từ `image`, và nó bị xoá ngay sau job.

Đây không phải chuyện "cái nào tốt hơn". Với `shell`, trạng thái còn lại vừa là tiện lợi vừa là nguồn của một lớp lỗi rất khó tái lập: pipeline chạy được vì một phụ thuộc **do một job khác cài từ ba tuần trước**, và không ai biết cho tới ngày máy runner được dựng lại.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline chạy được trên runner cũ nhưng đỏ ngay khi chuyển sang runner mới, với lỗi kiểu `command not found`. Bằng chứng xác nhận: chạy `which <công-cụ>` trong job và thấy nó nằm ở `/usr/local/bin` chứ không đến từ `image`.

**Minh hoạ.**

```yaml
# Job chẩn đoán: chạy trên cả runner shell và runner docker rồi so kết quả
chan-doan-moi-truong:
  image: alpine:3.20
  script:
    - echo "hostname trong job: $(hostname)"
    - echo "runner: $CI_RUNNER_DESCRIPTION ($CI_RUNNER_EXECUTABLE_ARCH)"
    - echo "công cụ có sẵn ngoài image:"
    - for c in node python3 java go docker; do
        printf '  %-8s %s\n' "$c" "$(command -v $c || echo 'không có')";
      done
    # Với executor docker, danh sách trên chỉ có cái nằm trong alpine:3.20.
    # Với executor shell, nó phản ánh máy chủ — và đó là điều cần thấy.
```

**Con số cần nhớ.** Với executor `docker`, số byte trạng thái còn lại giữa hai job là **0**. Con số này là lý do executor `docker` được chọn làm mặc định của khoá.

### 6.2. Job không nằm trong mạng của runner

**Nguyên lý cốt lõi:** Container của job **không** nằm trong mạng của runner: `localhost` trong job trỏ vào chính job đó, và tên miền nội bộ không phân giải được nếu không cấu hình.

**Giải thích cơ chế ngầm:** Runner dùng Docker socket của máy chủ để tạo container job. Container ấy là **anh em** của container runner, không phải con của nó, và mặc định nó nằm ở mạng bridge mặc định — không phải mạng mà runner đang ở. Hệ quả là hai thứ cùng lúc: tên container khác trong mạng compose không phân giải được, và `localhost` là chính job.

Đây đúng là câu 5 của phần kiểm tra đầu vào, và nó là lý do lab của khoá này dùng tên `gitlab.lab` với một IP tĩnh thay vì dùng `localhost`.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Hai thông báo lỗi, và chúng chỉ hai nguyên nhân khác nhau: `curl: (7) Failed to connect to localhost port 8080: Connection refused` nghĩa là tên phân giải được nhưng không có gì lắng nghe ở đó — tức job đang gọi vào chính nó. `curl: (6) Could not resolve host: gitlab.lab` nghĩa là tên không phân giải được — tức thiếu cấu hình mạng hoặc thiếu ánh xạ tên.

**Minh hoạ.**

```yaml
# Đoạn chẩn đoán mạng, dán vào bất kỳ job nào đang nghi ngờ vấn đề mạng
chan-doan-mang:
  image: alpine:3.20
  script:
    - apk add --no-cache curl bind-tools >/dev/null
    - echo "== IP của chính job =="
    - ip -4 addr show | grep inet
    - echo "== phân giải tên =="
    - nslookup gitlab.lab || echo "KHÔNG phân giải được gitlab.lab"
    - echo "== gọi thử =="
    - curl -sS -o /dev/null -w 'gitlab.lab → HTTP %{http_code}\n' http://gitlab.lab:8929/-/readiness || true
    - curl -sS -o /dev/null -w 'localhost   → HTTP %{http_code}\n' http://localhost:8929/ || echo "localhost KHÔNG có gì lắng nghe — đúng như dự đoán"
```

**Hai tuỳ chọn giải quyết**, và lab của khoá dùng **cả hai** vì chúng giải hai nửa khác nhau của vấn đề:

| Tuỳ chọn khi đăng ký runner | Giải quyết gì |
|---|---|
| `--docker-network-mode "ntkgitlab-lab_lab"` | Đưa container job vào cùng mạng, nhờ đó DNS của Docker phân giải được tên các dịch vụ khác |
| `--docker-extra-hosts "gitlab.lab:172.28.0.10"` | Ánh xạ thẳng tên → IP, dùng được kể cả khi job không ở trong mạng đó |

### 6.3. Tag là cơ chế định tuyến duy nhất

**Nguyên lý cốt lõi:** `tags` là **cơ chế định tuyến duy nhất** giữa job và runner. Job không tìm được runner khớp thì nằm `pending` **vô hạn**, và **không có ai báo lỗi**.

**Giải thích cơ chế ngầm:** GitLab ghép job với runner theo một phép so khớp đơn giản: runner chỉ nhận job nếu tập `tags` của job là tập con của tập tag runner có. Ngoài ra, runner có tuỳ chọn "chạy job không có tag" — tắt tuỳ chọn ấy thì runner **không** nhận job nào không khai báo tag. Khi không runner nào khớp, GitLab không coi đó là lỗi: nó coi đó là "chưa có runner rảnh", vì về mặt logic hai tình huống ấy không phân biệt được. Job nằm `pending` cho tới khi chạm hạn giờ.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline hiển thị "đang chạy" hàng giờ, job ở trạng thái `pending`, **không có log** — vì log chỉ tồn tại sau khi runner nhận job. Học viên mở log không thấy gì và nghĩ giao diện bị lỗi. Cách chẩn đoán trong 20 giây là hỏi API xem có runner nào khớp tag không, thay vì nhìn giao diện.

**Minh hoạ.**

```bash
# Chẩn đoán job pending: liệt kê tag mà mỗi runner đang phục vụ
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/all" \
| jq -r '.[] | "\(.id)\t\(.description)\tonline=\(.online)"'

# Với từng runner, xem tag và có nhận job không tag hay không
curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/1" \
| jq '{tag_list, run_untagged, paused, online}'
```

```yaml
# Job này sẽ nằm pending vô hạn nếu không runner nào có tag "gpu"
huan-luyen:
  tags: [gpu]
  script: [echo "sẽ không bao giờ chạy"]
```

**Con số cần nhớ, và giới hạn của nó.** Hạn giờ mặc định của một job là **60 phút**; sau đó job mới chuyển sang `failed`. Nghĩa là một job định tuyến sai gây **60 phút im lặng** trước khi có bất cứ tín hiệu nào. Con số 60 phút **không phổ quát**: nó là mặc định ở cấp project, đổi được ở Settings → CI/CD → General pipelines; runner cũng có hạn giờ riêng, và **cái nhỏ hơn thắng**.

---

### 1.4. Ba chế độ hỏng, và chế độ nguy hiểm nhất (5 phút)

### 7.1. Bảng hai thuộc tính

**Nguyên lý cốt lõi:** Chế độ hỏng của pipeline phân loại theo **hai** thuộc tính: **ồn ào hay im lặng** (có báo hay không) và **có chặn hay không chặn** (pipeline dừng hay đi tiếp). Loại nguy hiểm nhất là **im lặng, không chặn**.

**Giải thích cơ chế ngầm:** Chi phí của một sự cố tỉ lệ với **thời gian phát hiện**, không tỉ lệ với mức nghiêm trọng của nguyên nhân. Hỏng ồn ào có chặn thì phát hiện sau vài giây — có người nhìn thấy job đỏ. Hỏng im lặng nhưng có chặn thì phát hiện sau hàng chục phút — có người thắc mắc sao lâu thế. Hỏng im lặng và không chặn thì **không có ai phát hiện cả**, cho tới khi hệ quả xuất hiện ở nơi khác: sản phẩm thiếu tệp, bản vá không được kiểm, image chạy ở prod không phải image đã test.

| | **Có chặn** (pipeline dừng) | **Không chặn** (pipeline đi tiếp) |
|---|---|---|
| **Ồn ào** (có báo) | Job đỏ. Thời gian phát hiện: **giây**. Đây là loại rẻ nhất, và mục tiêu của mọi kỹ thuật hôm nay là **dồn hỏng về ô này** | Job đỏ nhưng `allow_failure: true`. Thời gian phát hiện: **ngày** — có báo nhưng không ai buộc phải nhìn |
| **Im lặng** (không báo) | Job `pending` mãi, hoặc job treo tới hạn giờ. Thời gian phát hiện: **60 phút** hoặc tới khi có người hỏi | **Ô nguy hiểm nhất.** Job xanh, sản phẩm sai. Thời gian phát hiện: **tuần**, và thường phát hiện ở prod |

Bốn ca mà bài lab hôm nay tái hiện rơi vào ba ô khác nhau của bảng này — có chủ ý, để học viên cảm nhận được chênh lệch thời gian phát hiện giữa các ô.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Một đội tự hào rằng "pipeline lúc nào cũng xanh". Đó là dữ liệu, nhưng nó tương thích với hai giả thuyết: mọi thứ thật sự tốt, hoặc pipeline không kiểm gì cả. Câu hỏi phân biệt hai giả thuyết ấy là *"lần gần nhất pipeline đỏ vì một lỗi thật là khi nào, và nó đỏ ở job nào"*.

**Minh hoạ.**

```yaml
# Ba job cùng "thành công" nhưng thuộc ba ô khác nhau của bảng
on-ao-co-chan:
  script:
    - test -f khong-ton-tai.txt      # đỏ ngay, phát hiện trong vài giây

on-ao-khong-chan:
  allow_failure: true
  script:
    - test -f khong-ton-tai.txt      # đỏ nhưng pipeline vẫn xanh

im-lang-khong-chan:
  script:
    - ls khong-ton-tai.txt || true   # XANH, và không ai biết gì đã không xảy ra
```

### 7.2. Xanh không phải bằng chứng

**Nguyên lý cốt lõi:** Job xanh **không** chứng minh việc đã được làm. Nó chỉ chứng minh rằng lệnh cuối cùng runner đo được trả về mã thoát 0.

**Giải thích cơ chế ngầm:** Runner không có mô hình về ý định của học viên. Nó chạy script và đọc mã thoát. Nếu công cụ test không được cài, `npx jest` có thể trả về 0 sau khi in một cảnh báo; nếu mẫu đường dẫn không khớp tệp nào, `artifacts` upload một gói rỗng và pha 8 vẫn thành công; nếu lệnh nằm trong một ống dẫn, mã thoát của ống là mã thoát của **lệnh cuối cùng** trong ống, không phải của lệnh đã hỏng.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Ba dấu hiệu, xếp theo mức độ hay gặp: artifact tải về nặng vài trăm byte trong khi lẽ ra phải vài MB; log job có dòng `0 tests ran` hoặc tương đương mà không ai đọc; và job quét bảo mật kết thúc sau 3 giây trong khi lần trước nó chạy 90 giây.

**Minh hoạ.**

```yaml
# Ba ca job xanh mà việc KHÔNG được làm
xanh-nhung-sai:
  image: alpine:3.20
  script:
    # Ca 1: mẫu không khớp gì → artifact rỗng, pha 8 vẫn thành công
    - mkdir -p dist && echo x > dist/app.js
    # Ca 2: ống dẫn nuốt mã thoát của lệnh đầu
    - false | tee ket-qua.txt ; echo "mã thoát của ống dẫn = $?"
    # Ca 3: || true bôi xoá mọi thất bại
    - ls tep-khong-co.txt || true
  artifacts:
    paths:
      - build/**/*.js      # SAI đường dẫn — dist/ mới đúng. Job vẫn XANH.
```

### 7.3. Khẳng định biến im lặng thành ồn ào

**Nguyên lý cốt lõi:** Mỗi bước quan trọng phải kèm một **khẳng định** tự nó làm job đỏ khi kết quả không đúng. Không có khẳng định thì bước đó thuộc loại hỏng im lặng.

**Giải thích cơ chế ngầm:** Đây là hệ quả trực tiếp của QT 7.2. Nếu runner chỉ đọc mã thoát, thì cách duy nhất để "việc không được làm" trở thành "job đỏ" là **tự mình sinh ra một mã thoát khác 0** khi kiểm tra thấy kết quả sai. Khẳng định không phải là kiểm thử — nó là một câu hỏi có/không rẻ tiền đặt ngay sau bước sinh ra kết quả.

Đây là phát biểu loại (c) — **theo kinh nghiệm thực tế**. Không có tài liệu GitLab nào bắt làm việc này; nó là thói quen kỹ thuật.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Trong `.gitlab-ci.yml` có job sinh ra hiện vật mà không có dòng nào kiểm tra hiện vật ấy tồn tại và khác rỗng. Đếm nhanh: số job sinh artifact chia cho số dòng `test -s` hoặc tương đương — tỉ số càng xa 1 thì càng nhiều bước hỏng im lặng.

**Minh hoạ.**

```yaml
build:
  image: node:22-alpine
  script:
    - npm ci
    - npm run build
    # Bốn khẳng định, tổng chi phí khoảng 0,2 giây
    - test -d dist || { echo "KHẲNG ĐỊNH HỎNG: không có thư mục dist"; exit 1; }
    - test -s dist/app.js || { echo "KHẲNG ĐỊNH HỎNG: dist/app.js rỗng"; exit 1; }
    - >
      [ "$(find dist -name '*.js' | wc -l)" -ge 1 ] ||
      { echo "KHẲNG ĐỊNH HỎNG: không có tệp .js nào trong dist"; exit 1; }
    - >
      [ "$(du -sk dist | cut -f1)" -ge 10 ] ||
      { echo "KHẲNG ĐỊNH HỎNG: dist nhỏ hơn 10 KB, gần như chắc chắn build hụt"; exit 1; }
  artifacts:
    paths: [dist/]
```

**Con số cần nhớ.** Một khẳng định dạng `test -s` tốn khoảng **0,05 giây**. So với thời gian một pipeline điển hình 5–15 phút, chi phí này nằm dưới ngưỡng đo được. Không có lý do kinh tế nào để bỏ nó.

**Một mẹo dùng được ngay hôm nay:** đặt `set -euo pipefail` ở đầu `script` biến ba loại hỏng im lặng thành ồn ào cùng lúc — lệnh lỗi dừng script (`-e`), biến chưa đặt thành lỗi (`-u`), và ống dẫn trả về mã thoát của lệnh **đầu tiên** hỏng chứ không phải lệnh cuối (`-o pipefail`). Xem giới hạn của mẹo này ở §8.

```yaml
before_script:
  - set -euo pipefail
```

> **Hành vi mặc định của shell trong runner là thứ phải ĐO, không phải thứ tra tài liệu.** Việc runner có tự đặt `-e` hay `pipefail` cho script sinh ra hay không **đã thay đổi giữa các phiên bản runner** và còn phụ thuộc cờ tính năng. Đây chính là lý do lab bước 4 có một bước đo riêng cho chuyện này thay vì chép một câu khẳng định vào bài giảng. Kết quả đo được ghi vào hiện vật nộp, kèm số phiên bản runner.

---

### 1.5. Đưa vào việc thật (4 phút)

### Áp vào repo đang chạy thì làm gì trước

Ba việc, xếp theo thứ tự rủi ro tăng dần. Việc 1 và 2 làm được ngay hôm nay mà không đụng tới ai.

**Việc 1 — 5 phút, rủi ro bằng 0.** Mở log của một job bất kỳ trong repo đang chạy và đánh dấu tám pha. Ghi lại thời lượng từng pha. Chỉ riêng việc này thường phát hiện ra một chuyện: pha `download_artifacts` hoặc `restore_cache` chiếm nhiều thời gian hơn `step_script`.

**Việc 2 — 15 phút, rủi ro thấp.** Liệt kê mọi job trong `.gitlab-ci.yml` và đánh dấu job nào **không** dùng artifact của stage trước. Thêm `dependencies: []` cho từng job đó. Đây là thay đổi không đổi hành vi, chỉ bỏ bớt việc tải thừa.

**Việc 3 — 30 phút, rủi ro trung bình.** Chọn **một** job sinh ra hiện vật quan trọng nhất — thường là job build của service quan trọng nhất — và thêm 2–4 khẳng định vào cuối `script`. Làm một job trước, không làm cả loạt.

### Cái gì hỏng nếu áp thẳng lên prod

Thêm `set -euo pipefail` vào một `script` đang **dựa ngầm** vào việc lệnh lỗi không làm dừng job sẽ làm pipeline đang xanh chuyển sang đỏ ngay lập tức. Đó là đỏ **đúng** — nó phơi ra thứ vốn đã hỏng — nhưng nếu làm vào chiều thứ Sáu trên nhánh chính thì cả đội bị chặn.

Cách áp an toàn:

```yaml
# Bước 1: chạy song song, không chặn ai, trong 3–5 ngày
build-nghiem-ngat:
  extends: build
  allow_failure: true          # ồn ào nhưng KHÔNG chặn — ô góc trên phải của bảng QT 7.1
  before_script:
    - set -euo pipefail
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

Sau 3–5 ngày, đếm số lần `build-nghiem-ngat` đỏ trong khi `build` xanh. Con số đó chính là số ca hỏng im lặng đang tồn tại. Khi con số về 0, bỏ `allow_failure` và gộp vào job chính.

### Đo trước — đo sau

Ba con số, đo trước khi làm và đo lại sau 2 tuần:

| Chỉ số | Đo bằng | Vì sao chỉ số này |
|---|---|---|
| Tổng thời lượng pha `download_artifacts` cộng dồn cả pipeline | Cộng chênh lệch dấu thời gian trong log từng job | Đây là phần `dependencies: []` cắt được, và nó đo được chính xác |
| Số job sinh artifact mà không có khẳng định nào | `grep` đếm job có `artifacts:` trừ số job có `test -s`/`test -d` | Đây là số bước đang hỏng im lặng |
| Số job ở trạng thái `pending` quá 5 phút trong 7 ngày qua | API `/projects/:id/jobs?scope=pending` chạy theo lịch, hoặc lọc từ lịch sử | Đây là chỉ số của lỗi định tuyến tag |

### Khi nào KHÔNG nên dùng

**`dependencies: []` không dùng** cho job mà ta chưa xác định được nó đang dùng artifact của ai. Trước khi tắt phải biết chắc — cách kiểm rẻ nhất là đọc log job đó, xem những dòng `Downloading artifacts for ...`, rồi đối chiếu với `script` xem có đụng tới tệp nào trong số đó không. Tắt nhầm cho ra một job đỏ khó hiểu ở lần chạy sau, và người sửa thường không phải người tắt.

**`set -euo pipefail` không dùng** cho script cố tình cho phép một số lệnh trả mã thoát khác 0. Ca hay gặp nhất là `grep`: không tìm thấy gì thì `grep` trả về 1, và đó là kết quả hợp lệ chứ không phải lỗi. Ở những chỗ ấy dùng `|| true` **kèm ghi chú lý do ngay tại dòng đó**, thay vì bỏ `pipefail` cho cả script:

```yaml
script:
  - set -euo pipefail
  # grep trả 1 khi không khớp — ở đây "không khớp" là kết quả hợp lệ
  - grep -c "CANH_BAO" nhat-ky.txt || true
```

**Khẳng định không thay thế được kiểm thử.** Khẳng định trả lời "hiện vật có tồn tại và có kích thước hợp lý không". Nó không trả lời "hiện vật có đúng không". Đừng để việc thêm khẳng định tạo cảm giác an toàn thay cho việc viết test.

---

### 1.6. Bẫy hay gặp (2 phút)

| # | Bẫy | Vì sao dính | Làm đúng là |
|---|---|---|---|
| 1 | Tưởng job chạy trên một máy có sẵn công cụ | Kinh nghiệm từ Jenkins agent hoặc từ executor `shell` | Job chỉ có cái nằm trong `image`. Kiểm bằng `command -v <công-cụ>` |
| 2 | Ghi tệp vào `/tmp` mong job sau đọc được | Mô hình sai: tưởng các job dùng chung một máy | Dùng `artifacts`. Xem QT 4.1 |
| 3 | Dùng `cache` để truyền `node_modules` sang job test | Nó chạy được 9 lần đầu nên trông có vẻ đúng | `artifacts` cho cái job sau **cần**; `cache` chỉ cho cái làm nhanh hơn. Xem QT 5.2 |
| 4 | `echo "VERSION=1.2.3"` rồi mong job sau đọc được | Nhầm log với đường ra | `artifacts:reports:dotenv` — cơ chế duy nhất. Xem QT 5.4 |
| 5 | Đặt `tags` mà không runner nào có tag đó | Chép YAML từ repo khác dùng runner khác | Kiểm bằng API `runners/all` **trước khi** đẩy commit. Xem QT 6.3 |
| 6 | `curl localhost:8080` để gọi một dịch vụ | `localhost` đúng trên máy mình nên tưởng đúng cả trong job | Dùng tên dịch vụ khai trong `services:`, hoặc tên miền phân giải được. Xem QT 6.2 |
| 7 | Sửa `script` khi lỗi thật ra nằm ở pha `get_sources` | Cuộn thẳng xuống cuối log tìm chữ `ERROR` | Đọc dòng tiêu đề pha cuối cùng **trước** dòng lỗi. Xem QT 4.2 |
| 8 | `export X=1` ở `script` rồi đọc ở `after_script` | Tưởng cùng một shell | Ghi ra tệp trong thư mục dự án. Xem QT 4.3 |
| 9 | Tin rằng job xanh nghĩa là việc đã xong | Đây là mặc định của trực giác | Thêm khẳng định. Xem QT 7.3 |
| 10 | `cmd \| tee nhat-ky.txt` che mã thoát của `cmd` | Mã thoát của ống dẫn là của lệnh **cuối** | `set -o pipefail`, hoặc đọc `${PIPESTATUS[0]}` |
| 11 | Không đặt `dependencies` nên job nhẹ tải hết artifact | Mặc định của GitLab là tải tất cả | `dependencies: []` cho job không cần. Xem QT 5.3 |
| 12 | `artifacts:paths` trỏ đường dẫn tuyệt đối kiểu `/builds/...` | Sao chép từ log ra | Đường dẫn **tương đối** so với thư mục dự án |
| 13 | Nghĩ artifact vẫn được upload khi job hỏng | Không đọc mặc định | Mặc định là `when: on_success`. Muốn lấy log gỡ lỗi thì `artifacts:when: always` |
| 14 | Bản sao nông làm `git describe --tags` cho kết quả sai | `GIT_DEPTH` mặc định chỉ lấy vài chục commit | `GIT_DEPTH: 0` cho job cần lịch sử đầy đủ |

---

### 1.7. Tóm tắt

```mermaid
graph TD
    LD["LUẬN ĐỀ: job chạy trong môi trường DÙNG MỘT LẦN<br/>bốn đường vào, hai đường ra, không có đường thứ năm"]

    LD --> P["§4 TÁM PHA<br/>QT 4.1 môi trường dùng một lần<br/>QT 4.2 xác định pha = xác định nhóm nguyên nhân<br/>QT 4.3 after_script là shell khác"]
    LD --> D["§5 BỐN ĐƯỜNG VÀO / HAI ĐƯỜNG RA<br/>QT 5.1 chỉ có bốn đường<br/>QT 5.2 cache tối ưu, artifact hợp đồng<br/>QT 5.3 mặc định tải hết artifact stage trước<br/>QT 5.4 log KHÔNG phải đường ra"]
    LD --> R["§6 RUNNER VÀ ĐỊNH TUYẾN<br/>QT 6.1 executor quyết định cái gì còn lại<br/>QT 6.2 job không ở trong mạng runner<br/>QT 6.3 tag là định tuyến duy nhất"]

    P --> H["§7 BA CHẾ ĐỘ HỎNG<br/>QT 7.1 bảng hai thuộc tính<br/>QT 7.2 xanh không phải bằng chứng<br/>QT 7.3 khẳng định biến im lặng thành ồn ào"]
    D --> H
    R --> H

    H --> KQ["Ô NGUY HIỂM NHẤT:<br/>im lặng + không chặn<br/>thời gian phát hiện tính bằng TUẦN"]
    KQ --> VT["§8 ĐƯA VÀO VIỆC THẬT<br/>dependencies: [] · khẳng định · set -euo pipefail<br/>áp qua allow_failure trước, đo 3–5 ngày"]

    P -.dùng lại.-> B07["buổi 07 gỡ rối · buổi 14 tối ưu · buổi 47 sự cố runner"]
    D -.dùng lại.-> B05["buổi 05 artifact/cache · buổi 08 needs · buổi 22 monorepo"]
    R -.dùng lại.-> B02["buổi 02 executor · buổi 13 quy mô · buổi 23 đặc quyền"]
    H -.dùng lại.-> BALL["MỌI BUỔI — chủ đề xuyên khoá"]
```

**Năm điều phải nhớ sau buổi học:**

1. **Bốn vào, hai ra.** Git · cache · artifact · biến vào; artifact · mã thoát ra. Không có đường thứ năm.
2. **Tám pha.** Đọc dòng tiêu đề pha trước khi đọc dòng lỗi. Không có `Executing "step_script"` nghĩa là lệnh của mình chưa chạy lần nào.
3. **Cache miss làm chậm, không làm hỏng.** Nếu cache miss làm job đỏ thì đang dùng cache như artifact.
4. **Xanh không phải bằng chứng.** Trạng thái job là kết quả của mã thoát, không phải của công việc.
5. **Ô nguy hiểm nhất là im lặng + không chặn.** Mọi kỹ thuật hôm nay đều nhằm dồn hỏng về ô ồn ào + có chặn.

---

### 1.8. Câu hỏi tự kiểm tra

1. Kể tên tám pha của một job theo đúng thứ tự. Pha nào chứa lệnh do học viên viết?
2. Một job báo `Could not resolve host: gitlab.lab`. Lỗi này thuộc pha nào, và tại sao sửa `script` không giúp được gì?
3. Job A chạy `echo abc > /tmp/x`. Job B ở stage sau chạy `cat /tmp/x`. Kết quả là gì, và vì sao?
4. Nêu hai điểm khác nhau giữa `cache` và `artifacts` mà nếu nhầm sẽ gây hỏng ngẫu nhiên.
5. Vì sao một job có `cache` bị miss vẫn xanh, còn một job thiếu artifact cần thiết lại đỏ?
6. `dependencies: []` làm gì? Nêu một tình huống **không** nên dùng nó.
7. Một pipeline có 6 job ở stage 2, mỗi job cần 20 giây tải artifact 300 MB từ stage 1, nhưng chỉ 2 job thật sự dùng artifact ấy. Thêm `dependencies: []` cho 4 job kia tiết kiệm bao nhiêu giây thời gian máy?
8. Vì sao `after_script` không thấy biến `export` trong `script`? Nêu cách truyền một giá trị từ `script` sang `after_script`.
9. Một job nằm `pending` 40 phút, không có log. Nêu hai giả thuyết và **một lệnh** phân biệt được chúng.
10. Với hạn giờ mặc định, một job định tuyến sai gây bao nhiêu phút im lặng trước khi có tín hiệu? Con số đó đổi được ở đâu?
11. Vẽ bảng hai thuộc tính của chế độ hỏng. Ô nào nguy hiểm nhất và vì sao?
12. `false | tee log.txt` trả về mã thoát bao nhiêu? Làm sao để nó trả về mã thoát của `false`?
13. Cho `artifacts:paths: [build/**/*.js]` nhưng job sinh tệp vào `dist/`. Job xanh hay đỏ? Đây là ô nào của bảng hai thuộc tính?
14. Viết một khẳng định kiểm tra rằng job build đã sinh ra ít nhất một tệp `.jar` trong `target/` và tệp đó lớn hơn 1 MB.
15. Nêu **một** trường hợp `set -euo pipefail` gây hại, và cách xử lý trường hợp ấy mà không bỏ `pipefail` cho cả script.

### Đáp án

1. `prepare_executor` → `prepare_script` → `get_sources` → `restore_cache` → `download_artifacts` → `step_script` → `after_script` → `archive_cache`/`upload_artifacts`. Lệnh của học viên nằm trong `step_script` (cả `before_script` lẫn `script`).
2. Pha `get_sources` — pha 3. Sửa `script` vô ích vì pha 6 chưa hề chạy; đây là lỗi phân giải tên, thuộc cấu hình mạng của runner (QT 6.2).
3. Job B **đỏ** với `No such file or directory`. `/tmp` nằm ngoài thư mục dự án và container của job A đã bị xoá; không đường nào trong bốn đường mang nó sang (QT 4.1).
4. (a) Cache **không được đảm bảo tồn tại**, artifact thì có; (b) thiếu cache job vẫn xanh và chạy tiếp, thiếu artifact cần thiết thì job đỏ ở pha 5. Nhầm hai điều này cho ra pipeline hỏng ngẫu nhiên khi job rơi vào runner khác (QT 5.2).
5. Vì cache là tối ưu: runner ghi một dòng log rồi chạy tiếp. Artifact là hợp đồng: pha `download_artifacts` thất bại thì job đỏ ngay.
6. Nó tắt hẳn pha `download_artifacts` cho job đó. **Không** dùng khi chưa xác định được job đang dùng artifact của ai — kiểm bằng cách đọc các dòng `Downloading artifacts for ...` trong log rồi đối chiếu với `script`.
7. 4 job × 20 giây = **80 giây** thời gian máy. Lưu ý phân biệt với thời gian đồng hồ: nếu 6 job chạy song song thì thời gian đồng hồ tiết kiệm được là 0 — trừ khi số job vượt số slot runner. Buổi 14 xử lý phân biệt này.
8. Vì runner sinh hai script và chạy chúng như hai tiến trình riêng; biến `export` không vượt qua ranh giới tiến trình anh em (QT 4.3). Cách truyền: ghi ra tệp trong thư mục dự án, ví dụ `echo "X=1" > trang-thai.env`, rồi `source trang-thai.env` trong `after_script`.
9. Giả thuyết A: không runner nào khớp `tags`. Giả thuyết B: mọi runner đang bận. Lệnh phân biệt: `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/all" | jq '.[] | {tag_list, run_untagged, online}'` — so tập tag của job với tập tag runner.
10. **60 phút** với mặc định. Đổi ở Settings → CI/CD → General pipelines (cấp project); runner cũng có hạn giờ riêng và **cái nhỏ hơn thắng**.
11. Hai trục: ồn ào/im lặng × có chặn/không chặn. Ô nguy hiểm nhất là **im lặng + không chặn** — job xanh nhưng sản phẩm sai; thời gian phát hiện tính bằng tuần vì không có tín hiệu nào và không có gì bị chặn để buộc ai đó nhìn.
12. Trả về **0**, vì mã thoát của ống dẫn là của lệnh cuối (`tee`). Sửa bằng `set -o pipefail`, hoặc đọc `${PIPESTATUS[0]}` trong bash.
13. **Xanh.** Mẫu không khớp tệp nào thì pha `upload_artifacts` upload một gói rỗng và vẫn thành công. Đây là ô **im lặng + không chặn** — ô nguy hiểm nhất (QT 7.1, 7.2).
14. Ví dụ: `[ "$(find target -name '*.jar' -size +1M | wc -l)" -ge 1 ] || { echo "KHẲNG ĐỊNH HỎNG: không có .jar nào lớn hơn 1 MB trong target/"; exit 1; }`
15. `grep` trả về mã thoát 1 khi không tìm thấy gì, và "không tìm thấy" thường là kết quả hợp lệ. Xử lý: thêm `|| true` **kèm ghi chú lý do ngay tại dòng đó**, thay vì bỏ `pipefail` cho cả script.

---

## §12. Tài liệu tham khảo

| Nguồn | Loại | Phiên bản |
|---|---|---|
| GitLab Docs — *CI/CD YAML syntax reference* | (a) tài liệu chính thức | 17.7 |
| GitLab Runner Docs — *Executors* và *Advanced configuration* (`config.toml`) | (a) | 17.7 |
| GitLab Docs — *Job artifacts* và *Caching in GitLab CI/CD* | (a) | 17.7 |
| GitLab Docs — *Runner tags* và *Job timeouts* | (a) | 17.7 |
| GitLab API — `GET /projects/:id/jobs/:job_id/trace`, `GET /runners/all` | (a) | v4 |
| Bảng tám pha, thời lượng từng pha, hành vi mã thoát trong ống dẫn | (c) **phải đo** | Lab bước 1 và bước 4 |
| Thói quen thêm khẳng định, ngưỡng "0,05 giây" | (c) kinh nghiệm thực tế | — |

> **Về việc trích dẫn.** Bốn dòng loại (a) ở trên là những chỗ nên tra tài liệu chính thức khi cần con số chính xác cho phiên bản đang dùng. Hai dòng loại (c) là những chỗ **không được** tra — phải đo trên chính hệ thống của mình, vì chúng phụ thuộc phiên bản runner, cấu hình máy và cờ tính năng.

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và kiểm tra đầu vào | 10' |
| §1 | Sau buổi này học viên làm được gì | 1' |
| §2 | Cần biết trước | 1' |
| §3 | Thuật ngữ và mô hình tư duy | 8' |
| §4 | Vòng đời một job: tám pha | 10' |
| §5 | Bốn đường vào và hai đường ra | 11' |
| §6 | Runner, executor và định tuyến job | 8' |
| §7 | Ba chế độ hỏng, và chế độ nguy hiểm nhất | 5' |
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

> Kiểm chứng trên GitLab CE 17.7 · GitLab Runner 17.7 · Docker Engine 27.x.
> Mọi checkpoint gọi **API GitLab**, không xem giao diện. Lý do ở §L2 quyết định 1.

---

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| # | Mục tiêu | Tiêu chí hoàn thành (kiểm chứng được bằng lệnh) |
|---|---|---|
| TH1 | Dựng project và chạy pipeline đầu tiên | API `pipelines` trả `status == "success"` |
| TH2 | **Đo tám pha của QT 4.2 từ log thật** | Tệp `tam-pha.tsv` có **≥ 8 dòng**, mỗi dòng có tên pha và thời lượng bằng giây |
| TH3 | Kiểm chứng QT 4.1 — `/tmp` không qua được ranh giới job | Job `doc-tep` có `status == "failed"` và log chứa `No such file` |
| TH4 | Kiểm chứng QT 5.2 — cache miss **không** làm job đỏ | Job `dung-cache-lan-1` xanh, và log có dòng cache miss |
| TH5 | Kiểm chứng QT 5.2 — artifact **có** đảm bảo | Job `thieu-artifact` đỏ ở pha `download_artifacts` |
| TH6 | **Đo QT 5.3** — `dependencies: []` tiết kiệm bao nhiêu giây | Bảng hai job đối chứng, chênh lệch tính bằng giây |
| TH7 | Tái hiện hỏng im lặng 1 — tag không khớp | Job ở `status == "pending"` sau 3 phút, và API `runners/all` chứng minh không runner nào khớp |
| TH8 | Tái hiện hỏng im lặng 2 — artifact rỗng, job **xanh** | Job xanh **và** `artifacts_file.size` dưới 200 byte |
| TH9 | Kiểm chứng QT 6.2 và QT 4.3 — `localhost` và shell của `after_script` | Log chứa cả hai bằng chứng: `localhost` không kết nối được, biến rỗng trong `after_script` |
| TH10 | **Đo QT 7.2** — hành vi mã thoát trong ống dẫn trên runner này | Tệp `hanh-vi-shell.txt` ghi kết quả đo **và** số phiên bản runner |
| TH11 | Kiểm chứng QT 7.3 — khẳng định biến im lặng thành ồn ào | Cùng một lỗi: bản không khẳng định **xanh**, bản có khẳng định **đỏ** |
| TH12 | Nộp hiện vật đầy đủ | `kiem-hien-vat.sh` in `ĐẠT` cho cả 7 tệp |

**Sản phẩm cuối buổi:** `gitlab-portfolio/01-mo-hinh-thuc-thi-job/` gồm `tam-pha.tsv` (bảng tám pha đo được), `bon-duong-vao.md` (bốn ca thực nghiệm kèm mã job), `do-dependencies.tsv` (đo tiết kiệm của `dependencies: []`), `hong-im-lang.md` (bốn ca hỏng im lặng kèm bằng chứng API), `hanh-vi-shell.txt` (kết quả đo mã thoát kèm phiên bản runner), `.gitlab-ci.yml` (bản cuối có khẳng định), `checkpoint.log` (kết quả 12 checkpoint).

---

## L1. Điều kiện tiên quyết về môi trường

| # | Kiểm tra | Lệnh | Kết quả kỳ vọng |
|---|---|---|---|
| 1 | Đã nạp biến môi trường lab | `echo "$GITLAB" "$GITLAB_TOKEN" \| wc -w` | `2` |
| 2 | GitLab sẵn sàng | `curl -sf -o /dev/null -w '%{http_code}\n' "$GITLAB/-/readiness"` | `200` |
| 3 | Token gọi được API | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/user" \| jq -r .username` | tên đăng nhập, không phải rỗng |
| 4 | **Có ít nhất một runner online** | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/all" \| jq '[.[]\|select(.online)]\|length'` | `>= 1` |
| 5 | **Runner nhận được job không có tag** | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/all" \| jq '[.[]\|select(.online)]\|length'` rồi kiểm từng runner (xem ghi chú dưới) | ít nhất một runner có `run_untagged == true` |
| 6 | Có `jq`, `curl`, `git`, `awk` | `command -v jq curl git awk \| wc -l` | `4` |
| 7 | Đĩa trống | `df -BG --output=avail "$HOME" \| tail -1` | `> 10G` |
| 8 | Bộ nhớ trống | `free -g \| awk '/Mem:/{print $7}'` | `>= 3` |
| 9 | Có thư mục portfolio | `test -d "$PORTFOLIO" && echo có` | `có` |
| 10 | **Không còn project lab cũ** | `curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/projects?search=lab01-mo-hinh" \| jq length` | `0` — nếu khác `0` thì xoá trước, xem §L9 dòng cuối |

Ghi chú cho dòng 5 — đây là điều kiện dễ bị bỏ qua nhất và nó làm hỏng cả bước 1:

```bash
for id in $(curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/all" | jq -r '.[].id'); do
  curl -sf --header "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB/api/v4/runners/$id" \
  | jq -r '"runner \(.id)  online=\(.online)  run_untagged=\(.run_untagged)  tags=\(.tag_list|join(","))"'
done
```

Kết quả phải có ít nhất một dòng `online=true  run_untagged=true`. Nếu không có, mở Admin → CI/CD → Runners → runner của mình → bật **Run untagged jobs**. Ghi nhớ chính cái ô tick này — bước 3 của bài lab sẽ dùng nó để tái hiện ca hỏng im lặng thứ nhất.

**Cảnh báo về mức độ tác động.** Bài lab tạo **một** project mới tên `lab01-mo-hinh` và không đụng tới bất kỳ project nào khác. Nó **không** đụng tới JFrog, kind, hay MinIO. Bước 3 cố tình tạo một job nằm `pending` — job đó chiếm một slot của runner cho tới khi bị huỷ, nên §L8 bắt buộc huỷ nó trước khi kết thúc buổi. Trên lớp đông người dùng chung một GitLab, mỗi học viên đặt hậu tố riêng vào tên project (xem bước 1).

---

## L2. Kiến trúc bài lab

```mermaid
graph TD
    HV["Học viên<br/>máy chủ lab"]
    HV -->|"git push"| PRJ["Project lab01-mo-hinh<br/>trên GitLab CE"]
    HV -->|"curl + jq (mọi checkpoint)"| API["API GitLab v4<br/>pipelines · jobs · trace · runners"]

    PRJ -->|"giao job"| RN["Runner lab-runner<br/>executor: docker"]
    RN -->|"tạo container ANH EM<br/>qua Docker socket"| JOB["Container của job<br/>image alpine/node<br/>XOÁ khi job xong"]

    JOB -->|"đường ra 1"| ART["artifacts<br/>lưu trên GitLab"]
    JOB -->|"đường ra 2"| EXIT["mã thoát<br/>0 hay khác 0"]

    PRJ -.->|"đường vào 1: get_sources"| JOB
    CACHE["kho cache trên runner"] -.->|"đường vào 2: restore_cache<br/>KHÔNG đảm bảo"| JOB
    ART -.->|"đường vào 3: download_artifacts"| JOB
    VARS["biến project + variables:"] -.->|"đường vào 4: prepare_script"| JOB

    API --> B1["Bước 1: đo TÁM PHA<br/>từ endpoint /jobs/:id/trace"]
    API --> B2["Bước 2: bốn đường vào<br/>+ đo dependencies: []"]
    API --> B3["Bước 3: hỏng im lặng 1 và 2<br/>tag không khớp · artifact rỗng"]
    API --> B4["Bước 4: hỏng im lặng 3 và 4<br/>localhost · ống dẫn nuốt mã thoát"]
    API --> B5["Bước 5: khẳng định<br/>im lặng → ồn ào"]
```

**Bốn quyết định thiết kế:**

1. **Mọi checkpoint gọi API, không xem giao diện.** Hai lý do. Thứ nhất, giao diện không đưa ra bằng chứng nộp được — một ảnh chụp màn hình không kiểm chứng lại được, và rubric của khoá đặt trần điểm 1 cho hiện vật dạng ảnh. Thứ hai, API chính là thứ buổi 46 dùng để lấy bốn chỉ số DORA; học viên bắt đầu quen với nó từ buổi đầu tiên thì tới buổi 46 không phải học lại. Phương án hiển nhiên — nhìn màu xanh trên web — nhanh hơn nhưng không cho ra dữ liệu.

2. **Đo tám pha bằng dấu thời gian trong log tải qua API, không bằng đồng hồ bấm tay.** Log job chứa mã thời gian ANSI cho từng dòng khi bật tuỳ chọn tương ứng; kể cả khi không có, thứ tự dòng tiêu đề pha vẫn cho phép ghép với dấu thời gian ở cấp job. Đo tay cho sai số bậc vài giây trên tổng vài chục giây — tức sai số 10–30%, đủ để làm kết luận về pha nào tốn nhiều thời gian trở nên vô nghĩa.

3. **Bốn ca hỏng được tái hiện theo cặp: mỗi cặp một ca im lặng và một ca ồn ào.** Học viên chạy hai ca liền nhau rồi so **thời gian từ lúc đẩy commit tới lúc biết có chuyện**. Cặp thứ nhất (bước 3): ca im lặng mất tới 3 phút mới thấy bất thường, ca ồn ào mất 40 giây. Cặp thứ hai (bước 4): ca ồn ào báo lỗi ngay trong log, ca im lặng **không báo gì cả** và chỉ lộ ra khi kiểm hiện vật. Nếu dạy bốn ca liên tiếp không theo cặp thì học viên nhớ bốn kỹ thuật rời, không nhớ được cái đáng nhớ là **chênh lệch thời gian phát hiện**.

4. **Bước 5 không viết lại pipeline từ đầu mà thêm khẳng định vào chính pipeline đã hỏng ở bước 3–4.** Nhờ đó cùng một lỗi cho hai kết quả khác nhau — xanh khi không có khẳng định, đỏ khi có — và đó là bằng chứng trực tiếp cho QT 7.3. Viết một pipeline mới "đúng chuẩn" thì không có phép so sánh nào cả.

**Ca đối chứng PHẢI THẤT BẠI — báo trước cho lớp.** Ở bước 3 ca 1, job `chi-chay-tren-gpu` sẽ nằm `pending` và **không bao giờ chạy**. Đó là kết quả đúng. Ai gọi giảng viên vì "job không chạy" ở bước này là đã bỏ qua đoạn cảnh báo.

---

## L3. Bước 1 — Dựng project, chạy pipeline đầu, và đo tám pha (30 phút)

### 3.1. Tạo project và bộ công cụ dùng chung (8 phút)

Trên lớp đông người dùng chung một GitLab, thêm hậu tố riêng để không đụng tên nhau:

```bash
source ~/.gitlab-lab.env
export HAU_TO="${USER}"                      # hoặc số thứ tự học viên
export TEN_PRJ="lab01-mo-hinh-${HAU_TO}"
mkdir -p ~/lab01 && cd ~/lab01
```

Tạo project qua API:

```bash
PID=$(curl -sf --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  --data "{\"name\":\"$TEN_PRJ\",\"visibility\":\"internal\",\"initialize_with_readme\":false}" \
  "$GITLAB/api/v4/projects" | jq -r .id)
echo "PID=$PID"
echo "export PID=$PID" >> ~/.gitlab-lab.env
```

Bộ công cụ dùng cho cả buổi — ba hàm shell. Đây là thứ học viên dùng lại ở mọi bước, nên đọc kỹ:

```bash
cat > ~/lab01/cong-cu.sh <<'SH'
#!/usr/bin/env bash
# Bộ công cụ dùng chung cho lab buổi 01.
# Nạp bằng: source ~/lab01/cong-cu.sh
: "${GITLAB:?chưa nạp ~/.gitlab-lab.env}"
: "${GITLAB_TOKEN:?chưa nạp ~/.gitlab-lab.env}"
: "${PID:?chưa có PID}"
H=(--header "PRIVATE-TOKEN: $GITLAB_TOKEN")

# đẩy .gitlab-ci.yml hiện tại và trả về id pipeline mới
day() {
  local msg="${1:-cap nhat pipeline}"
  git add -A >/dev/null
  git commit -q -m "$msg" --allow-empty
  git push -q origin HEAD 2>/dev/null
  sleep 4
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipelines?per_page=1" | jq -r '.[0].id'
}

# chờ pipeline kết thúc; in trạng thái cuối. Tham số 2: hạn giờ giây (mặc định 300)
cho_pipeline() {
  local pipe="$1" han="${2:-300}" t=0 st
  while [ "$t" -lt "$han" ]; do
    st=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipelines/$pipe" | jq -r .status)
    case "$st" in
      success|failed|canceled|skipped) echo "$st"; return 0 ;;
    esac
    sleep 5; t=$((t+5))
  done
  echo "$st"   # còn running hoặc pending khi hết hạn giờ — đó là DỮ LIỆU, không phải lỗi
}

# in bảng job của một pipeline: tên, trạng thái, thời lượng
job_bang() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipelines/$1/jobs?per_page=100" \
  | jq -r '.[] | [.id, .name, .status, (.duration//0)] | @tsv'
}

# id của một job theo tên, trong một pipeline
job_id() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipelines/$1/jobs?per_page=100" \
  | jq -r --arg n "$2" '.[] | select(.name==$n) | .id' | head -1
}

# log thô của một job
job_log() {
  curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$1/trace"
}
SH
chmod +x ~/lab01/cong-cu.sh
source ~/lab01/cong-cu.sh
```

Khởi tạo kho git và trỏ về project vừa tạo:

```bash
cd ~/lab01
git init -q -b main
git remote add origin "http://oauth2:${GITLAB_TOKEN}@gitlab.lab:8929/$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID" | jq -r .path_with_namespace).git"
git config user.email "hocvien@lab.local"
git config user.name  "hoc vien"
echo "# lab01" > README.md
```

**CHECKPOINT 1 — có runner online và runner đó nhận được job không tag.**

```bash
n=$(curl -sf "${H[@]}" "$GITLAB/api/v4/runners/all" | jq -r '.[].id' | while read -r id; do
      curl -sf "${H[@]}" "$GITLAB/api/v4/runners/$id" | jq -r 'select(.online==true and .run_untagged==true) | .id'
    done | wc -l)
[ "$n" -ge 1 ] && echo "CHECKPOINT 1 — ĐẠT ($n runner nhận job không tag)" \
                || echo "CHECKPOINT 1 — LỖI (không runner nào online + run_untagged)"
```

Không đạt thì dừng ở đây. Mọi bước sau đều phụ thuộc điều kiện này, và triệu chứng khi thiếu nó là **job nằm pending im lặng** — đúng cái mà bước 3 sẽ tái hiện có chủ ý.

### 3.2. Pipeline đầu tiên, thiết kế để tám pha đều xuất hiện (10 phút)

Pipeline này cố ý dùng đủ cả bốn đường vào và cả hai đường ra, để tám pha đều được kích hoạt và đều in ra log:

```yaml
# ~/lab01/.gitlab-ci.yml
stages: [chuan-bi, do-dac]

variables:
  BIEN_DUONG_4: "day la duong vao thu tu"

sinh-artifact:
  stage: chuan-bi
  image: alpine:3.20
  script:
    - mkdir -p ra
    - echo "noi dung artifact" > ra/du-lieu.txt
    - dd if=/dev/urandom of=ra/chen.bin bs=1M count=8 2>/dev/null   # 8 MB để pha 5 đo được
  artifacts:
    paths: [ra/]
    expire_in: 1 day

do-tam-pha:
  stage: do-dac
  image: alpine:3.20
  cache:
    key: lab01-cache
    paths: [.kho-cache/]
    policy: pull-push
  script:
    - mkdir -p .kho-cache && date +%s > .kho-cache/lan-chay.txt
    - echo "duong vao 1 (git)      : $(ls -1 | tr '\n' ' ')"
    - echo "duong vao 2 (cache)    : $(cat .kho-cache/lan-chay.txt)"
    - echo "duong vao 3 (artifact) : $(cat ra/du-lieu.txt)"
    - echo "duong vao 4 (bien)     : $BIEN_DUONG_4"
    - sleep 3
  after_script:
    - echo "day la pha after_script"
  artifacts:
    paths: [ra/du-lieu.txt]
```

```bash
cd ~/lab01
PIPE1=$(day "pipeline dau tien")
echo "pipeline $PIPE1"
cho_pipeline "$PIPE1"
job_bang "$PIPE1"
```

**CHECKPOINT 2 — pipeline đầu tiên thành công và có đúng hai job.**

```bash
st=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/pipelines/$PIPE1" | jq -r .status)
nj=$(job_bang "$PIPE1" | wc -l)
[ "$st" = "success" ] && [ "$nj" -eq 2 ] \
  && echo "CHECKPOINT 2 — ĐẠT (status=$st, $nj job)" \
  || echo "CHECKPOINT 2 — LỖI (status=$st, $nj job)"
```

### 3.3. Đo tám pha từ log thật (12 phút)

Đây là phép đo trung tâm của bước 1. Nó kiểm chứng QT 4.2 và cho ra hiện vật `tam-pha.tsv`.

```bash
cat > ~/lab01/do-tam-pha.sh <<'SH'
#!/usr/bin/env bash
# Trích tám pha và thời lượng từng pha từ log một job.
# Dùng: bash do-tam-pha.sh <job_id> > tam-pha.tsv
set -euo pipefail
source ~/lab01/cong-cu.sh
JOB="${1:?thiếu job_id}"

# Runner in dấu thời gian dạng ISO ở đầu mỗi dòng tiêu đề pha khi bật
# tuỳ chọn timestamp; nếu không có, ta rơi về cách đếm theo thứ tự dòng.
job_log "$JOB" \
| sed 's/\x1b\[[0-9;K]*[a-zA-Z]//g' \
| grep -nE 'Preparing the .* executor|Preparing environment|Getting source from Git repository|Restoring cache|Downloading artifacts for|Executing "step_script"|Running after_script|Saving cache|Uploading artifacts|Cleaning up project directory|Job succeeded|Job failed' \
| awk -F: '
  BEGIN { OFS="\t"; print "thu_tu","dong_log","ten_pha" }
  {
    dong=$1
    $1=""
    ten=$0
    gsub(/^[: ]+/,"",ten)
    gsub(/\r/,"",ten)
    print ++i, dong, ten
  }'
SH

JID=$(job_id "$PIPE1" "do-tam-pha")
bash ~/lab01/do-tam-pha.sh "$JID" | tee ~/lab01/tam-pha-tho.tsv
```

Bảng trên cho **thứ tự** pha. Để có **thời lượng**, dùng thêm dấu thời gian ở cấp job và tổng thời lượng:

```bash
curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JID" \
| jq -r '{
    ten: .name,
    tao: .created_at,
    bat_dau: .started_at,
    ket_thuc: .finished_at,
    thoi_luong_giay: .duration,
    cho_hang_doi_giay: .queued_duration
  }'
```

Ghép hai nguồn thành hiện vật nộp:

```bash
cat > ~/lab01/tam-pha.tsv <<EOF
# Buổi 01 — tám pha đo từ job $JID, project $PID
# GitLab $(curl -sf "$GITLAB/api/v4/version" -H "PRIVATE-TOKEN: $GITLAB_TOKEN" | jq -r .version)
# Runner: $(job_log "$JID" | sed 's/\x1b\[[0-9;K]*[a-zA-Z]//g' | grep -m1 'Running with gitlab-runner' | tr -d '\r')
$(cat ~/lab01/tam-pha-tho.tsv)
EOF
cat ~/lab01/tam-pha.tsv
```

**CHECKPOINT 3 — bảng tám pha có ít nhất 8 dòng pha và chứa pha `step_script`.**

```bash
n=$(grep -cE '^[0-9]+\s' ~/lab01/tam-pha.tsv || true)
has=$(grep -c 'step_script' ~/lab01/tam-pha.tsv || true)
{ [ "$n" -ge 8 ] && [ "$has" -ge 1 ]; } \
  && echo "CHECKPOINT 3 — ĐẠT ($n dòng pha, có step_script)" \
  || echo "CHECKPOINT 3 — LỖI ($n dòng pha, step_script=$has)"
```

**Câu hỏi phải trả lời trước khi sang bước 2** — ghi câu trả lời vào `bon-duong-vao.md`:

1. Pha nào chiếm nhiều dòng log nhất, và nó có phải pha chứa lệnh của mình không?
2. Trong bảng đo được, `queued_duration` là bao nhiêu? Nó thuộc pha nào trong tám pha, hay không thuộc pha nào?
3. Nếu bỏ khối `cache:` khỏi job, dòng tiêu đề nào biến mất khỏi log?

---

## L4. Bước 2 — Bốn đường vào: chứng minh không có đường thứ năm (30 phút)

### 4.1. Ca A — `/tmp` không qua được ranh giới job (8 phút)

Kiểm chứng QT 4.1.

```yaml
# ~/lab01/.gitlab-ci.yml — thay toàn bộ
stages: [a, b]

ghi-tep:
  stage: a
  image: alpine:3.20
  script:
    - echo "noi-dung-quan-trong" > /tmp/du-lieu.txt
    - echo "đã ghi vào /tmp:" && cat /tmp/du-lieu.txt
    - echo "hostname của job này: $(hostname)"

doc-tep:
  stage: b
  image: alpine:3.20
  script:
    - echo "hostname của job này: $(hostname)"
    - cat /tmp/du-lieu.txt      # ĐỎ — đây là kết quả đúng
```

```bash
cd ~/lab01
PIPE2=$(day "ca A: /tmp khong qua duoc ranh gioi")
cho_pipeline "$PIPE2"
job_bang "$PIPE2"
```

**CHECKPOINT 4 — `ghi-tep` xanh, `doc-tep` đỏ, và hai job chạy trên hai hostname khác nhau.**

```bash
J1=$(job_id "$PIPE2" "ghi-tep"); J2=$(job_id "$PIPE2" "doc-tep")
s1=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$J1" | jq -r .status)
s2=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$J2" | jq -r .status)
h1=$(job_log "$J1" | grep -o 'hostname của job này: .*' | head -1)
h2=$(job_log "$J2" | grep -o 'hostname của job này: .*' | head -1)
loi=$(job_log "$J2" | grep -c 'No such file' || true)
{ [ "$s1" = success ] && [ "$s2" = failed ] && [ "$loi" -ge 1 ] && [ "$h1" != "$h2" ]; } \
  && echo "CHECKPOINT 4 — ĐẠT (ghi-tep=$s1, doc-tep=$s2, hostname khác nhau)" \
  || echo "CHECKPOINT 4 — LỖI ($s1 / $s2 / loi=$loi)"
echo "  $h1"; echo "  $h2"
```

Hai hostname khác nhau là bằng chứng trực tiếp nhất của QT 4.1: hai job **không** chạy trong cùng một container.

### 4.2. Ca B — cache miss không làm job đỏ, artifact thiếu thì đỏ (10 phút)

Kiểm chứng QT 5.2. Hai job đối chứng, cùng một tình huống "thứ mình cần không có", nhưng đi qua hai đường khác nhau.

```yaml
# ~/lab01/.gitlab-ci.yml — thay toàn bộ
stages: [nguon, tieu-thu]

# job nguồn CỐ TÌNH không sinh artifact và không đẩy cache
khong-sinh-gi:
  stage: nguon
  image: alpine:3.20
  script:
    - echo "job nay khong sinh artifact, khong day cache"

dung-cache-lan-1:
  stage: tieu-thu
  image: alpine:3.20
  cache:
    key: cache-chua-bao-gio-ton-tai-$CI_PIPELINE_ID
    paths: [.kho-khong-co/]
  script:
    - echo "cache co ton tai khong:"
    - ls -la .kho-khong-co/ 2>/dev/null || echo "KHONG CO CACHE — va job nay VAN XANH"

thieu-artifact:
  stage: tieu-thu
  image: alpine:3.20
  needs: ["khong-sinh-gi"]
  script:
    - echo "job nay can artifact cua khong-sinh-gi"
    - test -f ra/du-lieu.txt || { echo "khong co artifact"; exit 1; }
```

```bash
PIPE3=$(day "ca B: cache miss so artifact thieu")
cho_pipeline "$PIPE3"
job_bang "$PIPE3"
```

**CHECKPOINT 5 — cache miss cho job XANH, thiếu artifact cho job ĐỎ.**

```bash
JC=$(job_id "$PIPE3" "dung-cache-lan-1"); JA=$(job_id "$PIPE3" "thieu-artifact")
sc=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JC" | jq -r .status)
sa=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JA" | jq -r .status)
mc=$(job_log "$JC" | grep -ciE 'no.*cache|not found|KHONG CO CACHE' || true)
{ [ "$sc" = success ] && [ "$sa" = failed ] && [ "$mc" -ge 1 ]; } \
  && echo "CHECKPOINT 5 — ĐẠT (cache miss → $sc, thiếu artifact → $sa)" \
  || echo "CHECKPOINT 5 — LỖI (cache=$sc, artifact=$sa, dấu hiệu cache miss=$mc)"
```

Ghi vào `bon-duong-vao.md`: **cùng một tình huống thiếu dữ liệu, hai đường cho hai kết quả trái ngược.** Đó là toàn bộ nội dung của QT 5.2, và nó vừa được đo chứ không phải được kể.

### 4.3. Ca C — đo `dependencies: []` tiết kiệm bao nhiêu giây (12 phút)

Kiểm chứng và **định lượng** QT 5.3. Đây là con số học viên mang về áp vào repo thật ngay tuần này.

```yaml
# ~/lab01/.gitlab-ci.yml — thay toàn bộ
stages: [nguon, tieu-thu]

sinh-artifact-lon:
  stage: nguon
  image: alpine:3.20
  script:
    - mkdir -p ra && dd if=/dev/urandom of=ra/khoi.bin bs=1M count=120 2>/dev/null
    - ls -lh ra/
  artifacts:
    paths: [ra/]
    expire_in: 1 hour

co-tai-artifact:
  stage: tieu-thu
  image: alpine:3.20
  script:
    - echo "job nay KHONG dung ra/khoi.bin nhung van tai ve"
    - ls -lh ra/ 2>/dev/null || echo "khong co"

khong-tai-artifact:
  stage: tieu-thu
  image: alpine:3.20
  dependencies: []
  script:
    - echo "job nay tat han pha download_artifacts"
    - ls -lh ra/ 2>/dev/null || echo "khong co — dung nhu mong doi"
```

```bash
PIPE4=$(day "ca C: do dependencies rong")
cho_pipeline "$PIPE4" 420
job_bang "$PIPE4"

JT=$(job_id "$PIPE4" "co-tai-artifact"); JK=$(job_id "$PIPE4" "khong-tai-artifact")
dt=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JT" | jq -r '.duration')
dk=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JK" | jq -r '.duration')

{ echo -e "job\tthoi_luong_giay\tco_tai_artifact"
  echo -e "co-tai-artifact\t$dt\tco"
  echo -e "khong-tai-artifact\t$dk\tkhong"
  echo -e "chenh_lech\t$(awk -v a="$dt" -v b="$dk" 'BEGIN{printf "%.2f", a-b}')\t-"
  echo "# kich thuoc artifact: 120 MB"
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
} | tee ~/lab01/do-dependencies.tsv
```

**CHECKPOINT 6 — job có `dependencies: []` nhanh hơn, và log của nó KHÔNG có dòng `Downloading artifacts`.**

```bash
ntai=$(job_log "$JK" | grep -c 'Downloading artifacts' || true)
nhanh=$(awk -v a="$dt" -v b="$dk" 'BEGIN{print (b<a)?1:0}')
{ [ "$ntai" -eq 0 ] && [ "$nhanh" -eq 1 ]; } \
  && echo "CHECKPOINT 6 — ĐẠT (tiết kiệm $(awk -v a=$dt -v b=$dk 'BEGIN{printf "%.1f", a-b}')s, không có pha download_artifacts)" \
  || echo "CHECKPOINT 6 — LỖI (dòng Downloading=$ntai, nhanh hơn=$nhanh)"
```

**Câu hỏi phải trả lời, ghi vào `do-dependencies.tsv`:** chênh lệch đo được là bao nhiêu giây trên 120 MB? Nếu repo thật có 8 job ở stage sau và artifact 300 MB, ước tính tiết kiệm được bao nhiêu **giây thời gian máy** một lần chạy? Và vì sao con số ấy **không** bằng số giây tiết kiệm được trên **đồng hồ**?

---

## L5. Bước 3 — Hai ca hỏng im lặng: tag không khớp và artifact rỗng (30 phút)

Cặp thứ nhất của quyết định thiết kế 3. Học viên bấm giờ từ lúc `git push` tới lúc biết có chuyện, cho **cả hai** ca, rồi so.

### 5.1. Ca 1 — job `pending` vô hạn vì tag không khớp (15 phút)

Kiểm chứng QT 6.3. **Đây là ca đối chứng phải thất bại — job sẽ không bao giờ chạy.**

```yaml
# ~/lab01/.gitlab-ci.yml — thay toàn bộ
stages: [chay]

binh-thuong:
  stage: chay
  image: alpine:3.20
  script: [echo "job nay chay binh thuong"]

chi-chay-tren-gpu:
  stage: chay
  image: alpine:3.20
  tags: [gpu-a100-khong-ton-tai]
  script: [echo "job nay se KHONG BAO GIO chay"]
```

```bash
T0=$(date +%s)
PIPE5=$(day "ca 1: tag khong khop")
# Chờ tối đa 180 giây. Kết quả mong đợi là pipeline VẪN running — đó là dữ liệu.
st=$(cho_pipeline "$PIPE5" 180)
T1=$(date +%s)
echo "sau $((T1-T0)) giây, trạng thái pipeline = $st"
job_bang "$PIPE5"
```

Chẩn đoán bằng API — đây là kỹ năng chính của ca này:

```bash
JG=$(job_id "$PIPE5" "chi-chay-tren-gpu")
echo "== trạng thái job và log =="
curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JG" | jq '{status, tag_list, queued_duration, runner}'
echo "== độ dài log (pending thì log RỖNG) =="
job_log "$JG" | wc -c
echo "== tag mà các runner đang phục vụ =="
for id in $(curl -sf "${H[@]}" "$GITLAB/api/v4/runners/all" | jq -r '.[].id'); do
  curl -sf "${H[@]}" "$GITLAB/api/v4/runners/$id" \
  | jq -r '"runner \(.id)  online=\(.online)  run_untagged=\(.run_untagged)  tags=[\(.tag_list|join(","))]"'
done
```

**CHECKPOINT 7 — job ở `pending`, log rỗng, và không runner nào có tag khớp.**

```bash
sg=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JG" | jq -r .status)
len=$(job_log "$JG" | wc -c)
khop=$(for id in $(curl -sf "${H[@]}" "$GITLAB/api/v4/runners/all" | jq -r '.[].id'); do
         curl -sf "${H[@]}" "$GITLAB/api/v4/runners/$id" \
         | jq -r 'select(.tag_list|index("gpu-a100-khong-ton-tai")) | .id'
       done | wc -l)
{ [ "$sg" = "pending" ] && [ "$len" -lt 50 ] && [ "$khop" -eq 0 ]; } \
  && echo "CHECKPOINT 7 — ĐẠT (status=$sg, log $len byte, $khop runner khớp tag)" \
  || echo "CHECKPOINT 7 — LỖI (status=$sg, log=$len byte, khớp=$khop)"
```

Ghi vào `hong-im-lang.md`:

- Thời gian từ `git push` tới lúc **nhận ra** có chuyện: `___` giây (thường 120–180 giây, vì phải chờ đủ lâu mới thấy bất thường).
- Thời gian tới khi hệ thống **tự** báo: **60 phút** — bằng hạn giờ job.
- Ô nào của bảng hai thuộc tính (QT 7.1)? **Im lặng, có chặn.**

Huỷ job đang chờ để trả slot runner lại:

```bash
curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JG/cancel" | jq -r .status
```

### 5.2. Ca 2 — artifact rỗng nhưng job xanh (15 phút)

Kiểm chứng QT 7.2. Đây là ô **nguy hiểm nhất** của bảng QT 7.1.

```yaml
# ~/lab01/.gitlab-ci.yml — thay toàn bộ
stages: [build]

build-artifact-rong:
  stage: build
  image: alpine:3.20
  script:
    - mkdir -p dist
    - echo "console.log('xin chao')" > dist/app.js
    - echo "đã build xong, nội dung dist/:" && ls -la dist/
  artifacts:
    # SAI đường dẫn — tệp nằm ở dist/, mẫu trỏ vào build/
    paths:
      - build/**/*.js
```

```bash
T0=$(date +%s)
PIPE6=$(day "ca 2: artifact rong nhung job xanh")
cho_pipeline "$PIPE6"
T1=$(date +%s)
echo "pipeline xong sau $((T1-T0)) giây"
job_bang "$PIPE6"
```

Job **xanh**. Bằng chứng cho thấy nó sai nằm ở kích thước artifact, không nằm ở trạng thái:

```bash
JB=$(job_id "$PIPE6" "build-artifact-rong")
curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JB" \
| jq '{status, artifacts_file, artifacts: [.artifacts[]? | {file_type, size}]}'
```

**CHECKPOINT 8 — job XANH nhưng artifact dưới 200 byte hoặc không tồn tại.**

```bash
sb=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JB" | jq -r .status)
sz=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JB" | jq -r '.artifacts_file.size // 0')
{ [ "$sb" = "success" ] && [ "${sz:-0}" -lt 200 ]; } \
  && echo "CHECKPOINT 8 — ĐẠT (status=$sb, artifact $sz byte — HỎNG IM LẶNG KHÔNG CHẶN)" \
  || echo "CHECKPOINT 8 — LỖI (status=$sb, artifact $sz byte)"
```

Ghi vào `hong-im-lang.md` và **so hai ca**:

| | Ca 1 — tag không khớp | Ca 2 — artifact rỗng |
|---|---|---|
| Ô của bảng QT 7.1 | Im lặng, **có chặn** | Im lặng, **không chặn** |
| Trạng thái job | `pending` | `success` |
| Có gì bất thường nhìn thấy được | Pipeline không bao giờ xong | **Không có gì** |
| Thời gian học viên phát hiện trong lab | ~150 giây | ~0 giây — vì đề bài đã nói trước |
| Thời gian phát hiện **ở nơi làm việc** | tới 60 phút | **hàng tuần**, thường ở prod |
| Ai phát hiện | Người chờ pipeline | Người dùng, hoặc người deploy |

Đây là bảng có giá trị nhất của cả bài lab. Chép nó vào hiện vật nộp.

---

## L6. Bước 4 — Hai ca nữa: `localhost` và ống dẫn nuốt mã thoát (30 phút)

Cặp thứ hai. Ca đầu ồn ào, ca sau im lặng — và ca sau là ca cần **đo** chứ không tra tài liệu được.

### 6.1. Ca 3 — `localhost` trong job, và shell của `after_script` (12 phút)

Kiểm chứng QT 6.2 và QT 4.3 trong cùng một job.

```yaml
# ~/lab01/.gitlab-ci.yml — thay toàn bộ
stages: [chan-doan]

chan-doan-ranh-gioi:
  stage: chan-doan
  image: alpine:3.20
  script:
    - apk add --no-cache curl bind-tools >/dev/null 2>&1
    - echo "=== IP CUA CHINH JOB ==="
    - ip -4 addr show | grep inet || true
    - echo "=== PHAN GIAI TEN ==="
    - (nslookup gitlab.lab >/dev/null 2>&1 && echo "gitlab.lab: PHAN GIAI DUOC") || echo "gitlab.lab: KHONG PHAN GIAI DUOC"
    - echo "=== GOI THU ==="
    - curl -sS -m 5 -o /dev/null -w 'gitlab.lab -> HTTP %{http_code}\n' http://gitlab.lab:8929/-/readiness || echo "gitlab.lab: GOI KHONG DUOC"
    - curl -sS -m 5 -o /dev/null -w 'localhost  -> HTTP %{http_code}\n' http://localhost:8929/ || echo "localhost: KHONG CO GI LANG NGHE — dung nhu du doan"
    - echo "=== BIEN VA THU MUC ==="
    - export BIEN_CUA_TOI="gia-tri-trong-script"
    - mkdir -p sau && cd sau && echo noi-dung > tep.txt
    - echo "trong script: BIEN_CUA_TOI=[$BIEN_CUA_TOI] pwd=$(pwd)"
    - cd "$CI_PROJECT_DIR" && echo "PHIEN_BAN=1.2.3" > trang-thai.env
  after_script:
    - echo "trong after_script: BIEN_CUA_TOI=[${BIEN_CUA_TOI:-RONG}] pwd=$(pwd)"
    - . ./trang-thai.env 2>/dev/null && echo "doc qua TEP thi duoc: PHIEN_BAN=$PHIEN_BAN" || echo "khong doc duoc trang-thai.env"
```

```bash
PIPE7=$(day "ca 3: localhost va after_script")
cho_pipeline "$PIPE7"
JD=$(job_id "$PIPE7" "chan-doan-ranh-gioi")
job_log "$JD" | sed 's/\x1b\[[0-9;K]*[a-zA-Z]//g' | grep -E 'PHAN GIAI|HTTP|KHONG|trong script|trong after_script|doc qua TEP'
```

**CHECKPOINT 9 — có đủ ba bằng chứng: `gitlab.lab` gọi được, `localhost` không, và biến rỗng trong `after_script`.**

```bash
L=$(job_log "$JD" | sed 's/\x1b\[[0-9;K]*[a-zA-Z]//g')
b1=$(echo "$L" | grep -c 'gitlab.lab -> HTTP 200' || true)
b2=$(echo "$L" | grep -c 'localhost: KHONG CO GI LANG NGHE' || true)
b3=$(echo "$L" | grep -c 'trong after_script: BIEN_CUA_TOI=\[RONG\]' || true)
b4=$(echo "$L" | grep -c 'doc qua TEP thi duoc' || true)
{ [ "$b1" -ge 1 ] && [ "$b2" -ge 1 ] && [ "$b3" -ge 1 ] && [ "$b4" -ge 1 ]; } \
  && echo "CHECKPOINT 9 — ĐẠT (4/4 bằng chứng)" \
  || echo "CHECKPOINT 9 — LỖI (gitlab.lab=$b1 localhost=$b2 bien_rong=$b3 doc_tep=$b4)"
```

Nếu `b1` bằng 0 thì runner của học viên thiếu `--docker-extra-hosts` hoặc `--docker-network-mode` — xem §L9. Đây không phải lỗi bài lab; đó chính là ca hỏng mà QT 6.2 mô tả, chỉ khác là nó xảy ra thật.

### 6.2. Ca 4 — đo hành vi mã thoát của shell trên runner này (18 phút)

Đây là phép đo loại (c): kết quả **phụ thuộc phiên bản runner và cờ tính năng**, nên không được chép từ tài liệu.

```yaml
# ~/lab01/.gitlab-ci.yml — thay toàn bộ
stages: [do-hanh-vi]

# Job 1: lệnh hỏng ở GIỮA script, có lệnh sau nó
loi-o-giua:
  stage: do-hanh-vi
  image: alpine:3.20
  script:
    - echo "dong 1 chay"
    - ls /thu-muc-khong-ton-tai      # trả mã thoát khác 0
    - echo "dong 3 — dong nay CO CHAY khong?"

# Job 2: lệnh hỏng nằm trong ỐNG DẪN
loi-trong-ong-dan:
  stage: do-hanh-vi
  image: alpine:3.20
  script:
    - echo "chuan bi chay ong dan"
    - false | tee ket-qua.txt
    - echo "ma thoat cua ong dan da duoc runner ghi nhan la gi?"

# Job 3: lệnh hỏng nằm trong ống dẫn, CÓ set -o pipefail
ong-dan-co-pipefail:
  stage: do-hanh-vi
  image: alpine:3.20
  script:
    - set -o pipefail
    - echo "chuan bi chay ong dan CO pipefail"
    - false | tee ket-qua.txt
    - echo "dong nay CO CHAY khong?"

# Job 4: biến chưa đặt
bien-chua-dat:
  stage: do-hanh-vi
  image: alpine:3.20
  script:
    - echo "gia tri = [$BIEN_KHONG_HE_TON_TAI]"
    - echo "dong nay CO CHAY khong?"
```

```bash
PIPE8=$(day "ca 4: do hanh vi ma thoat")
cho_pipeline "$PIPE8"
job_bang "$PIPE8"
```

Ghi kết quả đo thành hiện vật — **kèm số phiên bản runner**, vì không có nó thì kết quả đo vô nghĩa:

```bash
RUNNER_VER=$(job_log "$(job_id "$PIPE8" "loi-o-giua")" \
  | sed 's/\x1b\[[0-9;K]*[a-zA-Z]//g' | grep -m1 'Running with gitlab-runner' | tr -d '\r')

{
  echo "# Hành vi mã thoát của shell — ĐO trên chính runner này, không tra tài liệu"
  echo "# $RUNNER_VER"
  echo "# GitLab $(curl -sf "${H[@]}" "$GITLAB/api/v4/version" | jq -r .version)"
  echo "# Ngày đo: $(date -Iseconds)"
  echo
  printf "%-24s %-10s %s\n" "job" "trang_thai" "dong_sau_loi_co_chay"
  for j in loi-o-giua loi-trong-ong-dan ong-dan-co-pipefail bien-chua-dat; do
    id=$(job_id "$PIPE8" "$j")
    st=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$id" | jq -r .status)
    ch=$(job_log "$id" | grep -c 'CO CHAY khong' || true)
    printf "%-24s %-10s %s\n" "$j" "$st" "$([ "$ch" -ge 1 ] && echo CO || echo KHONG)"
  done
} | tee ~/lab01/hanh-vi-shell.txt
```

**CHECKPOINT 10 — bốn job đã đo xong và hiện vật ghi đủ phiên bản runner.**

```bash
n=$(grep -cE '^(loi-o-giua|loi-trong-ong-dan|ong-dan-co-pipefail|bien-chua-dat)' ~/lab01/hanh-vi-shell.txt || true)
v=$(grep -c 'gitlab-runner' ~/lab01/hanh-vi-shell.txt || true)
{ [ "$n" -eq 4 ] && [ "$v" -ge 1 ]; } \
  && echo "CHECKPOINT 10 — ĐẠT (4 job đo được, có ghi phiên bản runner)" \
  || echo "CHECKPOINT 10 — LỖI (n=$n, phiên bản=$v)"
```

**Ba câu hỏi phải trả lời, ghi ngay vào `hanh-vi-shell.txt`:**

1. Job `loi-trong-ong-dan` xanh hay đỏ? Nếu xanh, đó là ô nào của bảng QT 7.1?
2. So `loi-trong-ong-dan` với `ong-dan-co-pipefail`: một dòng `set -o pipefail` đổi kết quả thế nào?
3. Job `bien-chua-dat` xanh hay đỏ, và điều đó nói gì về việc dùng biến chưa chắc có giá trị trong tên tệp hoặc tên image?

> **Vì sao bài lab bắt đo thay vì đưa đáp án.** Hành vi `-e` và `pipefail` của script do runner sinh ra **đã thay đổi giữa các phiên bản** và còn phụ thuộc cờ tính năng của runner. Một bài giảng chép đáp án vào sẽ sai với một nửa số lớp. Đo mất 3 phút và cho ra một con số đúng với chính hệ thống của học viên — đó là quy tắc chung của khoá với mọi hành vi phụ thuộc phiên bản.

---

## L7. Bước 5 — Khẳng định biến hỏng im lặng thành hỏng ồn ào (20 phút)

Kiểm chứng QT 7.3. Theo quyết định thiết kế 4, bước này **không** viết pipeline mới mà thêm khẳng định vào chính hai ca hỏng im lặng của bước 3 và bước 4.

```yaml
# ~/lab01/.gitlab-ci.yml — thay toàn bộ
stages: [khong-khang-dinh, co-khang-dinh]

default:
  image: alpine:3.20

# ---- Bản KHÔNG có khẳng định: lặp lại đúng hai ca hỏng im lặng ----

build-khong-khang-dinh:
  stage: khong-khang-dinh
  script:
    - mkdir -p dist && echo "console.log('xin chao')" > dist/app.js
    - false | tee nhat-ky.txt          # ca 4: ống dẫn
  artifacts:
    paths: [build/**/*.js]             # ca 2: đường dẫn sai

# ---- Bản CÓ khẳng định: cùng lỗi, khác kết quả ----

build-co-khang-dinh:
  stage: co-khang-dinh
  script:
    - set -euo pipefail
    - mkdir -p dist && echo "console.log('xin chao')" > dist/app.js
    # Khẳng định 1: thư mục sắp đóng gói phải tồn tại
    - >
      test -d dist ||
      { echo "KHANG DINH HONG: khong co thu muc dist"; exit 1; }
    # Khẳng định 2: tệp chính phải khác rỗng
    - >
      test -s dist/app.js ||
      { echo "KHANG DINH HONG: dist/app.js rong"; exit 1; }
    # Khẳng định 3: mẫu artifact phải khớp ít nhất một tệp — đây là khẳng định bắt được ca 2
    - >
      [ "$(find dist -name '*.js' | wc -l)" -ge 1 ] ||
      { echo "KHANG DINH HONG: mau artifact khong khop tep nao"; exit 1; }
    # Ca 4 bây giờ ĐỎ, vì pipefail đã bật ở dòng đầu
    - false | tee nhat-ky.txt
    - echo "dong nay se KHONG chay neu pipefail hoat dong"
  artifacts:
    paths: [dist/]
  allow_failure: true    # để pipeline vẫn hoàn tất và checkpoint 11 so được hai job
```

```bash
PIPE9=$(day "buoc 5: khang dinh")
cho_pipeline "$PIPE9"
job_bang "$PIPE9"
```

**CHECKPOINT 11 — cùng một lỗi, bản không khẳng định XANH, bản có khẳng định ĐỎ.**

```bash
JN=$(job_id "$PIPE9" "build-khong-khang-dinh"); JY=$(job_id "$PIPE9" "build-co-khang-dinh")
sn=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JN" | jq -r .status)
sy=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JY" | jq -r .status)
szn=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JN" | jq -r '.artifacts_file.size // 0')
{ [ "$sn" = "success" ] && [ "$sy" = "failed" ]; } \
  && echo "CHECKPOINT 11 — ĐẠT (không khẳng định=$sn artifact ${szn}B; có khẳng định=$sy)" \
  || echo "CHECKPOINT 11 — LỖI (không khẳng định=$sn, có khẳng định=$sy)"
```

Đo chi phí của khẳng định — con số này để trả lời câu "thêm khẳng định có làm pipeline chậm không":

```bash
JY_DUR=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JY" | jq -r .duration)
JN_DUR=$(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$JN" | jq -r .duration)
echo "thời lượng không khẳng định: ${JN_DUR}s"
echo "thời lượng có khẳng định   : ${JY_DUR}s"
echo "chênh lệch                 : $(awk -v a=$JY_DUR -v b=$JN_DUR 'BEGIN{printf "%.2f", a-b}')s cho 3 khẳng định"
```

Ghi con số này vào `hong-im-lang.md`. Nó là câu trả lời cho phản đối hay gặp nhất khi đề xuất thêm khẳng định vào pipeline của đội.

---

## L8. Nộp sản phẩm và dọn dẹp (10 phút)

### 8.1. Gom hiện vật

```bash
DICH="$PORTFOLIO/01-mo-hinh-thuc-thi-job"
mkdir -p "$DICH"
cp ~/lab01/tam-pha.tsv          "$DICH/"
cp ~/lab01/do-dependencies.tsv  "$DICH/"
cp ~/lab01/hanh-vi-shell.txt    "$DICH/"
cp ~/lab01/.gitlab-ci.yml       "$DICH/"
# bon-duong-vao.md và hong-im-lang.md do học viên tự viết theo câu hỏi ở từng bước
ls -la "$DICH"
```

### 8.2. Script kiểm hiện vật

```bash
cat > "$DICH/kiem-hien-vat.sh" <<'SH'
#!/usr/bin/env bash
# Kiểm hiện vật buổi 01. Chạy trong chính thư mục hiện vật.
cd "$(dirname "$0")"
P=0; F=0
kiem() { if eval "$2" >/dev/null 2>&1; then echo "ĐẠT   $1"; P=$((P+1)); else echo "LỖI   $1"; F=$((F+1)); fi; }

kiem "tam-pha.tsv có ≥ 8 dòng pha"            "[ \$(grep -cE '^[0-9]+' tam-pha.tsv) -ge 8 ]"
kiem "tam-pha.tsv ghi phiên bản GitLab"        "grep -q 'GitLab' tam-pha.tsv"
kiem "do-dependencies.tsv có dòng chênh lệch"  "grep -q 'chenh_lech' do-dependencies.tsv"
kiem "hanh-vi-shell.txt có 4 job đo"           "[ \$(grep -cE '^(loi-o-giua|loi-trong-ong-dan|ong-dan-co-pipefail|bien-chua-dat)' hanh-vi-shell.txt) -eq 4 ]"
kiem "hanh-vi-shell.txt ghi phiên bản runner"  "grep -q 'gitlab-runner' hanh-vi-shell.txt"
kiem "bon-duong-vao.md tồn tại và khác rỗng"   "[ -s bon-duong-vao.md ]"
kiem "hong-im-lang.md có bảng so hai ca"       "grep -qi 'khong chan' hong-im-lang.md"
kiem "checkpoint.log có đủ 12 dòng CHECKPOINT" "[ \$(grep -c 'CHECKPOINT' checkpoint.log) -ge 12 ]"
kiem "checkpoint.log không có dòng LỖI"        "! grep -q 'LỖI' checkpoint.log"
kiem ".gitlab-ci.yml có khẳng định"            "grep -q 'KHANG DINH HONG' .gitlab-ci.yml"

echo "=== $P đạt, $F lỗi ==="
[ "$F" -eq 0 ]
SH
chmod +x "$DICH/kiem-hien-vat.sh"
```

**CHECKPOINT 12 — hiện vật đầy đủ.**

```bash
bash "$DICH/kiem-hien-vat.sh" \
  && echo "CHECKPOINT 12 — ĐẠT" || echo "CHECKPOINT 12 — LỖI"
```

Commit:

```bash
cd "$PORTFOLIO"
git add 01-mo-hinh-thuc-thi-job
git commit -q -m "buoi 01: mo hinh thuc thi job — tam pha, bon duong vao, bon ca hong im lang"
git push -q 2>/dev/null || echo "chưa cấu hình remote cho portfolio — làm ở đây"
```

### 8.3. Dọn dẹp

```bash
# Huỷ mọi job còn đang chờ — bắt buộc, kẻo chiếm slot runner của người khác
for j in $(curl -sf "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs?scope[]=pending&scope[]=running&per_page=100" | jq -r '.[].id'); do
  curl -sf --request POST "${H[@]}" "$GITLAB/api/v4/projects/$PID/jobs/$j/cancel" >/dev/null
  echo "đã huỷ job $j"
done

# Xoá artifact để lấy lại đĩa (bài lab này sinh khoảng 130 MB)
curl -sf --request DELETE "${H[@]}" "$GITLAB/api/v4/projects/$PID/artifacts" >/dev/null && echo "đã xoá artifact"

# Giữ lại project để buổi 02 dùng tiếp. Chỉ xoá khi hết giai đoạn 1:
# curl -sf --request DELETE "${H[@]}" "$GITLAB/api/v4/projects/$PID"
```

---

## L9. Xử lý sự cố thường gặp trong lab

| Triệu chứng | Nguyên nhân | Cách khắc phục |
|---|---|---|
| `git push` báo `403 Forbidden` | Token thiếu scope `write_repository`, hoặc URL remote sai | Tạo lại token với scope `api` + `write_repository`; kiểm bằng `git remote -v` |
| `day()` trả về `null` thay vì id pipeline | Pipeline chưa được tạo sau 4 giây, hoặc `.gitlab-ci.yml` sai cú pháp | Kiểm cú pháp bằng API lint: `curl -sf "${H[@]}" --data-urlencode "content@.gitlab-ci.yml" "$GITLAB/api/v4/projects/$PID/ci/lint"` |
| Mọi job nằm `pending` ngay từ bước 1 | Runner không nhận job không tag | Bật **Run untagged jobs**; xem §L1 dòng 5 |
| Job đỏ ở pha `Preparing the "docker" executor` | Runner không kéo được image, hoặc Docker Hub giới hạn tốc độ | Đăng nhập Docker Hub trên máy chủ; hoặc dùng image đã có sẵn cục bộ |
| Job đỏ ở pha `Getting source from Git repository` với `Could not resolve host` | Container job không phân giải được `gitlab.lab` — chính là QT 6.2 | Đăng ký lại runner có `--docker-extra-hosts "gitlab.lab:172.28.0.10"` và `--docker-network-mode "ntkgitlab-lab_lab"` |
| CHECKPOINT 9 báo `gitlab.lab=0` | Cùng nguyên nhân dòng trên | Như trên. Đây **là** bài học của ca 3, không phải lỗi bài lab |
| `job_log` trả về rỗng | Job đang `pending` nên chưa có log | Đó là **kết quả đúng** ở bước 3 ca 1. Ở bước khác thì chờ job chạy |
| Bảng tám pha chỉ có 5–6 dòng | Job không kích hoạt đủ pha (không có cache, không có artifact) | Dùng đúng pipeline ở §L3.2 — nó cố ý dùng đủ bốn đường vào |
| CHECKPOINT 6 báo job có `dependencies: []` **chậm hơn** | Nhiễu đo: hai job chạy trên hai runner khác nhau, hoặc máy đang tải nặng | Chạy lại pipeline 3 lần, lấy trung vị. Ghi rõ số lần chạy vào hiện vật |
| Artifact 120 MB làm job hết hạn giờ | Đĩa chậm hoặc mạng lab chậm | Giảm `count=120` xuống `count=60`, và **ghi lại con số đã dùng** vào hiện vật |
| `dd` báo `No space left on device` | Đĩa đầy vì artifact các lần chạy trước | `curl -X DELETE .../artifacts` như ở §L8.3, rồi `docker system prune -af` |
| Pipeline chạy nhưng job không đúng thứ tự stage | Có `needs` ở đâu đó ghi đè thứ tự stage | Buổi 08 xử lý; hôm nay chỉ cần bỏ `needs` nếu không cố ý dùng |
| CHECKPOINT 8 báo `artifact 0 byte` nhưng job đỏ | Mẫu `build/**/*.js` bị shell của học viên khai triển trước khi vào YAML | Đặt trong nháy đơn hoặc để nguyên trong file YAML, đừng `echo` vào file |
| `cho_pipeline` treo mãi ở bước 3 | Đó là **kết quả đúng** — pipeline có job pending | Hàm có hạn giờ 180 giây và sẽ trả về `running`. Đừng chờ 60 phút |
| Project trùng tên với học viên khác | Chưa đặt `HAU_TO` | Xoá project cũ hoặc đổi `HAU_TO`; xem §L3.1 |
| Muốn làm lại từ đầu | — | `curl -X DELETE "${H[@]}" "$GITLAB/api/v4/projects/$PID"` rồi chạy lại §L3.1 |

---

## L10. Bài tập mở rộng

Dành cho học viên xong sớm. Làm bao nhiêu bài ghi bấy nhiêu vào hiện vật.

### BT1. Đo pha `get_sources` theo `GIT_DEPTH`

Chạy cùng một job với `GIT_DEPTH: 1`, `GIT_DEPTH: 20`, `GIT_DEPTH: 0` và đo thời lượng pha 3 cho từng mức.

**Câu hỏi phải trả lời:** với repo lab (rất nhỏ), chênh lệch có đo được không? Với repo 20.000 commit thì bạn **dự đoán** chênh lệch bậc bao nhiêu, và dựa trên lập luận nào?

### BT2. `git describe --tags` với bản sao nông

Tạo một tag, rồi chạy `git describe --tags` trong job với `GIT_DEPTH: 1` và với `GIT_DEPTH: 0`.

**Câu hỏi phải trả lời:** kết quả khác nhau thế nào? Đây là ô nào của bảng QT 7.1 — và điều đó nghĩa là gì với một pipeline dùng `git describe` để đánh phiên bản image?

### BT3. `artifacts:when: always`

Làm job đỏ có chủ ý nhưng vẫn lấy được log gỡ lỗi ra ngoài.

**Câu hỏi phải trả lời:** vì sao đây là thứ nên bật mặc định cho mọi job build ở nơi làm việc? Nó tốn thêm bao nhiêu dung lượng một tháng nếu pipeline chạy 40 lần một ngày và log 2 MB?

### BT4. Đo `queued_duration`

Đẩy 10 pipeline liên tiếp và ghi `queued_duration` của từng job.

**Câu hỏi phải trả lời:** `queued_duration` thuộc pha nào trong tám pha? Nếu nó lớn thì vấn đề nằm ở `.gitlab-ci.yml` hay ở runner? (Buổi 13 sẽ dùng lại con số này.)

### BT5. Truyền giá trị bằng `dotenv`

Viết pipeline hai job: job 1 tính `PHIEN_BAN=1.2.<số pipeline>` và truyền sang job 2 bằng `artifacts:reports:dotenv`.

**Câu hỏi phải trả lời:** thử bỏ `needs` khỏi job 2 — biến còn tới nơi không? Thử truyền một chuỗi 100 KB — chuyện gì xảy ra?

### BT6. Ba cách xử lý mã thoát của ống dẫn

Cùng một ống dẫn `false | tee x.txt`, xử lý bằng ba cách: `set -o pipefail`, `${PIPESTATUS[0]}`, và tách thành hai lệnh.

**Câu hỏi phải trả lời:** cách nào dùng được trong image `alpine` với shell mặc định là `sh`, và cách nào cần `bash`?

### BT7. Khẳng định cho một repo thật

Lấy một repo thật của mình, chọn job build quan trọng nhất, và viết 3 khẳng định cho nó.

**Câu hỏi phải trả lời:** ba khẳng định đó bắt được ca hỏng nào mà pipeline hiện tại đang bỏ lọt? Ghi cụ thể, không viết chung chung.

### BT8. Đảo ngược ca 2

Sửa `artifacts:paths` cho đúng rồi chạy lại, và chứng minh bằng API rằng artifact bây giờ khác rỗng.

**Câu hỏi phải trả lời:** ngoài khẳng định, còn cách nào **khác** bắt được ca artifact rỗng trước khi nó lên tới môi trường thật? (Gợi ý: nghĩ về job ở stage sau.)

---

## L11. Sản phẩm nộp và tiêu chí chấm điểm

| Hạng mục | Điểm | Tiêu chí |
|---|---|---|
| `tam-pha.tsv` có ≥ 8 dòng pha, kèm phiên bản GitLab và runner | 3 | Chạy lại `do-tam-pha.sh` ra kết quả tương đương |
| `bon-duong-vao.md` trả lời đủ câu hỏi của bước 1 và bước 2 | 3 | Có câu trả lời cho cả 3 câu bước 1 và 3 câu bước 2 |
| `do-dependencies.tsv` có chênh lệch **bằng giây** và kích thước artifact | 3 | Có dòng `chenh_lech`, và có ghi số lần chạy nếu chạy nhiều lần |
| `hong-im-lang.md` có **bảng so hai ca** của bước 3 | 4 | Bảng phải có cột "ô của bảng QT 7.1" và cột "thời gian phát hiện ở nơi làm việc" |
| `hanh-vi-shell.txt` có 4 job đo + phiên bản runner + 3 câu trả lời | 3 | Thiếu phiên bản runner thì hạng mục này **0 điểm** |
| `.gitlab-ci.yml` bản cuối có ≥ 3 khẳng định | 2 | `grep -c 'KHANG DINH HONG'` ≥ 3 |
| `checkpoint.log` đủ 12 dòng, không có dòng `LỖI` | 2 | Chạy lại một checkpoint bất kỳ phải ra `ĐẠT` |
| **Tổng** | **20** | Đạt ≥ 12, đạt tốt ≥ 16 |

**Điểm trừ** — dẫn chiếu mục Bẫy hay gặp của `01-ly-thuyet.md` §9:

| Lỗi | Trừ |
|---|---|
| Nộp ảnh chụp màn hình thay cho kết quả API | **Trần điểm 1** cho hạng mục đó |
| `checkpoint.log` ghi ĐẠT nhưng chạy lại ra LỖI | **Trần điểm 1** cho cả bài |
| `hanh-vi-shell.txt` chép đáp án thay vì đo (thiếu phiên bản runner là dấu hiệu) | −3 |
| Kết luận "cache và artifact giống nhau, chỉ khác cách dùng" — bẫy 3 | −3 |
| Không huỷ job `pending` ở §L8.3, để chiếm slot runner | −2 |
| Bảng so hai ca thiếu cột thời gian phát hiện — bỏ mất điểm chính của bước 3 | −2 |
| Dùng `localhost` thay `gitlab.lab` trong script — bẫy 6 | −1 |

**Mức 3 của rubric buổi** (xem `00-tong-quan/01-chuan-dau-ra-danh-gia.md` mục 2) đạt được khi làm thêm **một** trong ba việc: hoàn thành ≥ 3 bài BT của §L10 kèm câu trả lời; hoặc phát hiện thêm một ca hỏng im lặng ngoài bốn ca của đề bài, kèm bằng chứng API; hoặc áp phần "Đưa vào việc thật" vào một repo thật và nộp số đo trước/sau.

---

## Bảng đối soát thời lượng

| Bước | Nội dung | Thời lượng |
|---|---|---|
| L3 | Bước 1 — Dựng project, chạy pipeline đầu, đo tám pha | 30' |
| L4 | Bước 2 — Bốn đường vào: `/tmp`, cache so artifact, đo `dependencies: []` | 30' |
| L5 | Bước 3 — Hỏng im lặng 1 và 2: tag không khớp, artifact rỗng | 30' |
| L6 | Bước 4 — Hỏng im lặng 3 và 4: `localhost`, ống dẫn nuốt mã thoát | 30' |
| L7 | Bước 5 — Khẳng định biến im lặng thành ồn ào | 20' |
| L8 | Nộp sản phẩm và dọn dẹp | 10' |
| **Tổng** | | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

---



**Quy tắc cho giảng viên:**

- Chọn **5–7 câu** trong 12, ưu tiên câu đánh dấu 🔥. Không cố hỏi hết 12 câu trong 20 phút.
- **Gọi ngẫu nhiên**, không hỏi cả lớp. Người trả lời sai thì gọi người kế tiếp bổ sung, giảng viên không trả lời thay.
- Học viên trả lời **bằng miệng, không nhìn tài liệu**. Đây là buổi tập nói, không phải buổi kiểm tra kiến thức.
- Khi học viên nói một khẳng định định lượng ("nhanh hơn nhiều", "tốn lắm"), giảng viên **luôn** hỏi lại "bao nhiêu". Đây là phản xạ cần rèn từ buổi đầu.

**Thang điểm mỗi câu:**

| Điểm | Nghĩa |
|---|---|
| 0 | Không trả lời được, hoặc trả lời sai cơ chế |
| 1 | Nhắc được tên khái niệm nhưng không nêu được cơ chế |
| 2 | Nêu đúng cơ chế |
| 3 | Nêu đúng cơ chế **và** một con số, hoặc **và** một ca mà nó không đúng |

**Hai lỗi làm trần điểm cả buổi là 1:**

1. **Trả lời rằng cache và artifact "giống nhau, chỉ khác cách dùng".** Đây là hiểu sai gốc rễ, và nó sinh ra loại lỗi ngẫu nhiên tốn nhiều thời gian nhất ở nơi làm việc. Người trả lời như vậy chưa nắm QT 5.2.
2. **Khẳng định rằng job xanh nghĩa là công việc đã xong.** Đây là hiểu sai mà cả khoá dựng lên để phá.

**Bốn câu phân loại thật của buổi này:**

| Câu | Phân loại điều gì |
|---|---|
| 4 | Phân loại người **đọc log** với người **đoán**. Ai từng thật sự đọc log job sẽ nhớ chuyện `after_script` là shell khác |
| 6 | Phân loại người hiểu **ranh giới môi trường**. Người chỉ dùng CI ở mức chép YAML sẽ không phân biệt được hai thông báo lỗi |
| 10 | Phân loại người **từng bị hỏng im lặng cắn**. Người chưa bị sẽ trả lời "hỏng nào cũng như nhau, sửa là được" |
| 12 | Phân loại **tư duy hệ thống**. Câu này không có đáp án duy nhất; nó đo cách người ta thu hẹp vùng nghi ngờ |

---

## V2. Bộ câu hỏi


<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Bốn đường vào và hai đường ra. Vào: (1) mã nguồn từ git ở pha <code>get_sources</code>; (2) <code>cache</code> ở pha <code>restore_cache</code>; (3) <code>artifacts</code> của job trước ở pha <code>download_artifacts</code>; (4) biến môi trường, nạp ở pha <code>prepare_script</code> tức trước cả ba đường kia. Ra: <code>artifacts</code> và <b style="color: var(--accent-primary);">mã thoát</b>. Log <b style="color: var(--accent-primary);">không phải</b> đường ra — không job nào đọc được log của job khác một cách có cấu trúc; ngoại lệ duy nhất được thiết kế riêng là <code>artifacts:reports:dotenv</code>, và nó là một dạng artifact chứ không phải log.

Điểm cần nói thêm để đạt 3 điểm: <b style="color: var(--accent-primary);">không có đường thứ năm</b>. Mọi thứ khác mà job cần thì <code>script</code> phải tự đi lấy, và khi ấy nó là việc của người viết pipeline chứ không phải của runner.

<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Trả lời "từ repo" mà không nêu được cơ chế nào khác.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Kể được git và artifact, quên cache hoặc quên biến.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2đ: Kể đủ bốn vào hai ra.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Đủ bốn vào hai ra, <b style="color: var(--accent-primary);">và</b> nói rõ log không phải đường ra, <b style="color: var(--accent-primary);">và</b> nêu <code>dotenv</code> là ngoại lệ duy nhất.</div>

<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu job cần một tệp nằm trên một server nội bộ, nó vào bằng đường nào? *(Không đường nào cả — <code>script</code> phải tự tải về, và khi đó phải xử lý xác thực và đường ra internet của runner. Đó là chủ đề buổi 47 khi runner bị chặn egress.)*
</div>
</details>

---

### Câu 2 — ★★

**Hỏi:** Kể tên các pha của một job theo thứ tự. Pha nào chứa lệnh do bạn viết?

**Đáp án chuẩn:** Tám pha: `prepare_executor` → `prepare_script` → `get_sources` → `restore_cache` → `download_artifacts` → `step_script` → `after_script` → `archive_cache` cùng `upload_artifacts`. Sau đó còn pha dọn dẹp. Lệnh do người viết pipeline viết nằm trong **`step_script`** — cả `before_script` lẫn `script` đều thuộc pha này.

Giá trị thực dụng của việc thuộc bảng này: nếu trong log **không có** dòng `Executing "step_script" stage of the job script` thì lệnh của mình **chưa chạy lần nào**, và mọi việc sửa `script` đều vô ích.

**Tiêu chí chấm:**
- 0đ: Không kể được pha nào.
- 1đ: Kể được 3–4 pha, không đúng thứ tự.
- 2đ: Kể đủ và đúng thứ tự, chỉ đúng `step_script`.
- 3đ: Như trên, **và** nêu được mẹo "không có dòng `step_script` nghĩa là lệnh chưa chạy".

**Câu hỏi đào sâu:** Tên pha có bất biến giữa các phiên bản runner không? *(Không — đã đổi trong quá khứ, và ba pha phụ không phải lúc nào cũng in ra. Vì thế bài lab đo từ log thật thay vì chép bảng.)*

---

### Câu 3 — 🔥

**Hỏi:** `cache` và `artifacts` khác nhau thế nào? Khi nào dùng cái nào?

**Đáp án chuẩn:** Khác nhau ở **sự đảm bảo**, không phải ở cách dùng. `artifacts` là **hợp đồng** giữa hai job: nó nằm trên GitLab, có `expire_in` khai báo được, và job phụ thuộc sẽ **đỏ** ở pha `download_artifacts` nếu artifact cần mà không có. `cache` là **tối ưu tốc độ**: nó nằm trên runner đã chạy job (hoặc trên kho dùng chung nếu cấu hình), không có gì bảo đảm nó còn tồn tại, và khi thiếu thì runner ghi một dòng log rồi **chạy tiếp bình thường**.

Quy tắc chọn: cái job sau **cần** thì đi bằng `artifacts`; cái chỉ làm job chạy **nhanh hơn** thì đi bằng `cache`. Cụ thể: `dist/`, `target/*.jar`, báo cáo test → artifact. `.npm/`, `~/.m2/`, `$GOMODCACHE` → cache.

Con số để đạt 3 điểm: **cache miss làm job thất bại 0 lần** khi dùng đúng. Nếu cache miss làm job của bạn đỏ, đó là bằng chứng bạn đang dùng cache như artifact.

**Tiêu chí chấm:**
- 0đ: "Giống nhau, chỉ khác cách dùng." **Trần điểm cả buổi là 1.**
- 1đ: Nói được cache để tăng tốc, artifact để truyền tệp, nhưng không nêu được sự khác biệt về đảm bảo.
- 2đ: Nêu đúng chuyện artifact có đảm bảo còn cache thì không.
- 3đ: Như trên, **và** nêu con số "cache miss làm hỏng 0 lần", **và** cho được ví dụ cụ thể thư mục nào đi đường nào.

**Câu hỏi đào sâu:** Một pipeline chạy tốt 9 lần rồi lần thứ 10 hỏng vì thiếu module, không ai đổi gì. Chẩn đoán? *(Gần như chắc chắn đang dùng cache để truyền `node_modules`; lần thứ 10 job rơi vào runner khác hoặc cache đã bị dọn. Bằng chứng: tìm dòng `Successfully extracted cache` trong 9 lần đầu và sự vắng mặt của nó ở lần thứ 10.)*

---

### Câu 4 — ★★★

**Hỏi:** Vì sao `after_script` không thấy biến mà `script` vừa `export`?

**Đáp án chuẩn:** Vì runner sinh ra **hai script riêng biệt** và chạy chúng như hai tiến trình. Biến `export` chỉ được kế thừa từ tiến trình cha sang con, không đi ngang giữa hai tiến trình anh em. Ngoài ra thư mục làm việc của `after_script` quay về mặc định, nên `cd` trong `script` cũng không có tác dụng ở đó.

Lý do thiết kế: `after_script` phải chạy được **kể cả khi `script` đã chết**. Muốn thế thì nó không thể nằm trong cùng một shell — nếu cùng shell thì shell chết là mất luôn `after_script`.

Cách truyền giá trị sang `after_script`: ghi ra **tệp trong thư mục dự án**, vì thư mục dự án là thứ cả hai shell cùng thấy.

Con số để đạt 3 điểm: `after_script` có hạn giờ riêng, mặc định **5 phút**, đổi bằng `RUNNER_AFTER_SCRIPT_TIMEOUT` — và con số này phụ thuộc phiên bản runner.

**Tiêu chí chấm:**
- 0đ: "Chắc GitLab không hỗ trợ."
- 1đ: Biết là nó không thấy, không giải thích được vì sao.
- 2đ: Nêu đúng cơ chế hai tiến trình riêng.
- 3đ: Như trên, **và** nêu lý do thiết kế (`after_script` phải chạy được khi `script` đã chết), **và** nêu cách truyền qua tệp.

**Câu hỏi đào sâu:** Còn thư mục làm việc thì sao? *(Cũng quay về mặc định. `cd sau && echo x > tep.txt` trong `script` thì `after_script` chạy `cat tep.txt` sẽ không thấy, vì nó đang đứng ở thư mục dự án.)*

---

### Câu 5 — ★★

**Hỏi:** `executor` là gì, và việc chọn `shell` hay `docker` ảnh hưởng đến điều gì?

**Đáp án chuẩn:** Runner là tiến trình nhận job từ GitLab; `executor` là cơ chế nó dùng để **tạo môi trường chạy** cho job. Điều bị ảnh hưởng lớn nhất là **cái gì tồn tại giữa hai job**. Với `shell`, môi trường chạy là chính máy đang cài runner, nên mọi thứ job cài đặt và mọi tệp job ghi ra ngoài thư mục dự án đều còn nguyên cho job sau. Với `docker` và `kubernetes`, mỗi job là một container hoặc pod mới, bị xoá ngay sau job.

Vì sao chuyện này quan trọng: với `shell`, trạng thái còn lại vừa là tiện lợi vừa là nguồn của loại lỗi rất khó tái lập — pipeline chạy được nhờ một phụ thuộc do một job khác cài từ ba tuần trước, và không ai biết cho tới ngày máy runner được dựng lại.

Con số để đạt 3 điểm: với executor `docker`, số byte trạng thái còn lại giữa hai job là **0**.

**Tiêu chí chấm:**
- 0đ: Không phân biệt được runner với executor.
- 1đ: Nói được docker thì sạch, shell thì không.
- 2đ: Nêu đúng "cái gì tồn tại giữa hai job" là điều bị ảnh hưởng.
- 3đ: Như trên, **và** nêu được ca lỗi khó tái lập của executor `shell`.

**Câu hỏi đào sâu:** Có ca nào executor `shell` là lựa chọn đúng không? *(Có — khi job cần truy cập phần cứng đặc thù của máy đó, hoặc khi chi phí khởi tạo container vượt quá thời gian chạy job. Buổi 02 và buổi 13 xử lý đầy đủ.)*

---

### Câu 6 — ★★★

**Hỏi:** Job của bạn chạy `curl http://localhost:8080` để gọi một dịch vụ. Nó báo lỗi. Chuyện gì đang xảy ra?

**Đáp án chuẩn:** `localhost` trong job trỏ vào **chính container của job**, không phải máy chủ và không phải container khác. Container của job là **anh em** của container runner — runner tạo nó qua Docker socket của máy chủ — nên nó nằm ở mạng bridge mặc định, không phải mạng của runner.

Hai thông báo lỗi khác nhau chỉ hai nguyên nhân khác nhau, và phân biệt được chúng là điểm cốt lõi của câu này:

| Thông báo | Nghĩa |
|---|---|
| `Failed to connect to localhost port 8080: Connection refused` | Tên phân giải được nhưng **không có gì lắng nghe** ở đó — job đang gọi vào chính nó |
| `Could not resolve host: <tên>` | **Tên không phân giải được** — thiếu cấu hình mạng hoặc thiếu ánh xạ tên |

Cách sửa: dùng tên dịch vụ khai trong `services:` (GitLab tự nối mạng cho chúng), hoặc dùng một tên miền phân giải được, và cấu hình runner bằng `--docker-network-mode` để đưa job vào đúng mạng, cộng `--docker-extra-hosts` để ánh xạ tên sang IP.

**Tiêu chí chấm:**
- 0đ: "Chắc dịch vụ chưa chạy."
- 1đ: Biết `localhost` không phải máy chủ, không giải thích được vì sao.
- 2đ: Nêu đúng cơ chế container anh em và mạng khác nhau.
- 3đ: Như trên, **và** phân biệt được hai thông báo lỗi ứng với hai nguyên nhân, **và** nêu được cả hai tuỳ chọn cấu hình runner.

**Câu hỏi đào sâu:** Nếu dùng `services:` để chạy một database bên cạnh job, job gọi nó bằng địa chỉ nào? *(Bằng tên service — GitLab đặt các service vào cùng mạng với job container và tạo alias theo tên image. Không dùng `localhost` được, trừ khi bật tuỳ chọn network per build.)*

---

### Câu 7 — ★★

**Hỏi:** Một job nằm ở trạng thái `pending` suốt 40 phút và không có log. Chẩn đoán thế nào, và với cấu hình mặc định thì bao lâu nữa hệ thống mới tự báo?

**Đáp án chuẩn:** Không có log vì log chỉ tồn tại **sau khi runner nhận job** — job `pending` nghĩa là chưa runner nào nhận. Hai giả thuyết: (A) không runner nào khớp `tags` của job; (B) mọi runner đang bận.

Lệnh phân biệt hai giả thuyết — hỏi API, không nhìn giao diện:

```bash
curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/runners/all" \
| jq -r '.[] | "\(.id) online=\(.online)"'
# rồi với từng runner:
curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$GITLAB/api/v4/runners/<id>" \
| jq '{tag_list, run_untagged, paused, online}'
```

So tập `tags` của job với tập tag của runner. Chú ý cả cờ `run_untagged`: runner tắt cờ này thì **không nhận job không có tag**, và đó là ca hay bị bỏ sót.

Con số: với mặc định, job chuyển sang `failed` sau **60 phút** — tức 60 phút im lặng hoàn toàn. Con số này **không phổ quát**: nó là mặc định cấp project, đổi được ở Settings → CI/CD; runner cũng có hạn giờ riêng và **cái nhỏ hơn thắng**.

**Tiêu chí chấm:**
- 0đ: "Chắc GitLab lag."
- 1đ: Đoán được là do runner, không nêu được cách kiểm.
- 2đ: Nêu đúng hai giả thuyết và cách kiểm bằng API.
- 3đ: Như trên, **và** nêu con số 60 phút **cùng với** giới hạn của nó, **và** nhắc tới cờ `run_untagged`.

**Câu hỏi đào sâu:** Đây là ô nào của bảng hai thuộc tính? *(Im lặng, có chặn. Không phải ô nguy hiểm nhất — vì có chặn nên sớm muộn cũng có người thắc mắc sao pipeline lâu thế.)*

---

### Câu 8 — ★★★

**Hỏi:** `dependencies: []` làm gì, tiết kiệm được gì, và khi nào **không** nên dùng?

**Đáp án chuẩn:** Mặc định một job tải artifact của **mọi job ở các stage trước**. `dependencies: []` tắt hẳn pha `download_artifacts` cho job đó, tiết kiệm đúng thời gian của pha ấy.

Tiết kiệm bao nhiêu thì phụ thuộc kích thước artifact và số job. Ví dụ tính được: pipeline có job build sinh 300 MB, 8 job ở stage sau, mỗi job mất 20 giây tải, nhưng chỉ 2 job thật sự dùng. Thêm `dependencies: []` cho 6 job kia tiết kiệm 6 × 20 = **120 giây thời gian máy** mỗi lần chạy.

Phân biệt quan trọng để đạt 3 điểm: đó là **thời gian máy**, không phải **thời gian đồng hồ**. Nếu 8 job chạy song song trên đủ slot runner thì thời gian đồng hồ tiết kiệm được là 0 — cái tiết kiệm được là dung lượng mạng và slot runner cho việc khác. Chỉ khi số job vượt số slot thì thời gian đồng hồ mới giảm theo.

**Khi nào không nên dùng:** khi chưa xác định được job đang dùng artifact của ai. Cách kiểm rẻ nhất trước khi tắt: đọc log job, xem các dòng `Downloading artifacts for ...`, rồi đối chiếu với `script` xem có đụng tệp nào trong số đó không. Tắt nhầm cho ra một job đỏ khó hiểu ở lần chạy sau, và người sửa thường không phải người tắt.

**Tiêu chí chấm:**
- 0đ: Không biết `dependencies` làm gì.
- 1đ: Biết nó liên quan artifact, không nêu được nó tắt pha nào.
- 2đ: Nêu đúng nó tắt pha `download_artifacts` và tính được ví dụ số.
- 3đ: Như trên, **và** phân biệt được thời gian máy với thời gian đồng hồ, **và** nêu được ca không nên dùng kèm cách kiểm.

**Câu hỏi đào sâu:** `needs` có làm điều tương tự không? *(Có, và hơn thế — `needs` vừa thu hẹp artifact vừa đổi thứ tự chạy, còn `dependencies` chỉ thu hẹp artifact. Buổi 08 xử lý đầy đủ.)*

---

### Câu 9 — 🔥

**Hỏi:** Pipeline của bạn xanh. Điều đó chứng minh được gì?

**Đáp án chuẩn:** Chỉ chứng minh rằng mã thoát mà runner đo được bằng 0. Nó **không** chứng minh việc đã được làm.

Ba ca cụ thể mà job xanh nhưng việc không xảy ra:

1. **`artifacts:paths` trỏ mẫu không khớp tệp nào** — pha `upload_artifacts` upload một gói rỗng và vẫn thành công. Job xanh, artifact vài trăm byte.
2. **Lệnh nằm trong ống dẫn** — mã thoát của ống là của lệnh **cuối cùng**, không phải của lệnh đã hỏng. `false | tee log.txt` trả về 0.
3. **Công cụ không chạy nhưng không báo lỗi** — ví dụ job quét bảo mật kết thúc sau 3 giây trong khi lần trước nó chạy 90 giây.

Cách phát hiện: ba dấu hiệu, xếp theo mức hay gặp — artifact tải về nặng vài trăm byte trong khi lẽ ra vài MB; log có dòng kiểu `0 tests ran` mà không ai đọc; job đột ngột nhanh hơn hẳn lần trước.

Cách sửa: mỗi bước quan trọng kèm một **khẳng định** tự nó làm job đỏ. Chi phí khoảng **0,05 giây** cho một `test -s` — dưới ngưỡng đo được so với pipeline 5–15 phút.

**Tiêu chí chấm:**
- 0đ: "Chứng minh mọi thứ đều ổn." **Trần điểm cả buổi là 1.**
- 1đ: Nói được là không chắc chắn, không nêu được ca cụ thể.
- 2đ: Nêu đúng cơ chế mã thoát và cho được ít nhất một ca cụ thể.
- 3đ: Như trên, **và** nêu được cách phát hiện qua kích thước artifact hoặc thời lượng job, **và** nêu giải pháp khẳng định kèm chi phí bằng số.

**Câu hỏi đào sâu:** Khẳng định có thay được kiểm thử không? *(Không. Khẳng định trả lời "hiện vật có tồn tại và có kích thước hợp lý không"; nó không trả lời "hiện vật có đúng không". Đừng để việc thêm khẳng định tạo cảm giác an toàn thay cho việc viết test.)*

---

### Câu 10 — ★★★

**Hỏi:** Phân loại các chế độ hỏng của một pipeline. Loại nào nguy hiểm nhất và vì sao?

**Đáp án chuẩn:** Hai trục: **ồn ào hay im lặng** (có báo hay không) và **có chặn hay không chặn** (pipeline dừng hay đi tiếp). Bốn ô:

| | Có chặn | Không chặn |
|---|---|---|
| **Ồn ào** | Job đỏ. Phát hiện sau **vài giây**. Rẻ nhất | Job đỏ nhưng `allow_failure: true`. Phát hiện sau **vài ngày** — có báo nhưng không ai buộc phải nhìn |
| **Im lặng** | Job `pending` mãi, hoặc treo tới hạn giờ. Phát hiện sau **60 phút** hoặc khi có người hỏi | **Nguy hiểm nhất.** Job xanh, sản phẩm sai. Phát hiện sau **hàng tuần**, thường ở prod |

Vì sao ô im lặng + không chặn nguy hiểm nhất: **chi phí của một sự cố tỉ lệ với thời gian phát hiện**, không tỉ lệ với mức nghiêm trọng của nguyên nhân. Ở ô đó không có tín hiệu nào và cũng không có gì bị chặn để buộc ai đó nhìn vào — nên thời gian phát hiện tính bằng tuần, và người phát hiện thường là người dùng.

Hệ quả thực hành: mục tiêu của mọi kỹ thuật trong buổi này là **dồn hỏng về ô ồn ào + có chặn**. Khẳng định làm đúng việc đó — nó biến một hỏng im lặng thành job đỏ.

**Tiêu chí chấm:**
- 0đ: "Hỏng nào cũng như nhau, sửa là được."
- 1đ: Phân biệt được job đỏ với job xanh mà sai.
- 2đ: Nêu đủ hai trục và bốn ô.
- 3đ: Như trên, **và** giải thích được bằng **thời gian phát hiện** chứ không bằng mức nghiêm trọng, **và** nêu được hệ quả "mục tiêu là dồn về ô ồn ào có chặn".

**Câu hỏi đào sâu:** `allow_failure: true` nằm ở ô nào, và vì sao nó nguy hiểm hơn người ta tưởng? *(Ồn ào, không chặn. Nguy hiểm vì nó tạo cảm giác "đã có kiểm tra rồi" trong khi không ai bị buộc phải nhìn. Buổi 35 gọi đây là **gate giả** và xử lý đầy đủ.)*

---

### Câu 11 — ★★★

**Hỏi:** Job A tính ra một số phiên bản. Job B cần dùng số đó. Làm thế nào?

**Đáp án chuẩn:** Cơ chế duy nhất là **`artifacts:reports:dotenv`**. Job A ghi `PHIEN_BAN=1.2.3` vào một tệp và khai tệp đó là `dotenv` report; GitLab đọc tệp, biến các dòng thành biến môi trường, và nạp chúng vào job ở stage sau hoặc job có `needs` tới job A.

```yaml
tinh-phien-ban:
  script:
    - echo "PHIEN_BAN=1.2.$CI_PIPELINE_IID" > bien.env
  artifacts:
    reports:
      dotenv: bien.env

dung-phien-ban:
  needs: ["tinh-phien-ban"]
  script:
    - test -n "$PHIEN_BAN" || { echo "PHIEN_BAN rỗng, dừng"; exit 1; }
    - echo "đóng gói $PHIEN_BAN"
```

Cách **không** hoạt động: `echo "PHIEN_BAN=1.2.3"` rồi mong job sau đọc được từ log. Log không phải đường ra. Điều tệ hơn là job sau thường **vẫn xanh** với biến rỗng — shell không báo lỗi khi biến rỗng — nên nó tạo ra một hiện vật có tên sai. Đây là ô im lặng + không chặn.

Ba giới hạn của `dotenv` cần nêu để đạt 3 điểm: giá trị bị giới hạn kích thước ở bậc vài KB nên không nhét nội dung tệp vào được; biến truyền qua `dotenv` **không** tự động là biến masked nên đừng truyền secret qua nó; và biến chỉ đi xuôi tới job có `needs` hoặc ở stage sau, không đi ngược lên.

**Tiêu chí chấm:**
- 0đ: Đề xuất `echo` rồi đọc log.
- 1đ: Đề xuất ghi ra tệp rồi truyền bằng artifact thường — hoạt động được nhưng job sau phải tự `source`, và không phải cơ chế chuẩn.
- 2đ: Nêu đúng `artifacts:reports:dotenv`.
- 3đ: Như trên, **và** nêu được ít nhất hai trong ba giới hạn, **và** nói rõ vì sao cách sai lại là ô im lặng không chặn.

**Câu hỏi đào sâu:** Vì sao đừng truyền secret qua `dotenv`? *(Vì nó không được masked tự động, nên giá trị có thể hiện nguyên trong log của job sau. Buổi 29 xử lý cách đúng.)*

---

### Câu 12 — 🔥

**Hỏi:** Đội bạn có một pipeline hỏng. Không ai biết vì sao. Bạn bắt đầu từ đâu?

**Đáp án chuẩn:** Câu này không có một đáp án duy nhất; nó đo cách thu hẹp vùng nghi ngờ. Đáp án tốt đi theo bốn nhịp:

**Nhịp 1 — xác định pha.** Mở log, tìm dòng tiêu đề pha **cuối cùng xuất hiện trước** thông báo lỗi. Việc này mất 10 giây và loại bỏ phần lớn giả thuyết. Nếu không có dòng `Executing "step_script" stage of the job script` thì lệnh của mình chưa chạy — mọi việc sửa `script` là vô ích.

**Nhịp 2 — ánh xạ pha sang nhóm nguyên nhân.** Pha `prepare_executor` hoặc `get_sources` là lỗi hạ tầng: image, quyền, mạng, xác thực. Pha `download_artifacts` là lỗi phụ thuộc giữa job. Pha `step_script` mới là lỗi của code hoặc của lệnh.

**Nhịp 3 — nếu là `step_script`, hỏi bốn đường vào.** Cái job cần lẽ ra vào qua đường nào? Git thì kiểm `GIT_STRATEGY` và `GIT_DEPTH`. Cache thì nhớ nó **không đảm bảo** — nếu pipeline hỏng ngẫu nhiên thì đây là nghi phạm số một. Artifact thì kiểm `needs`/`dependencies` và kích thước artifact của job nguồn. Biến thì kiểm thứ tự ưu tiên và cờ protected.

**Nhịp 4 — hỏi ngược lại.** Nếu job **xanh** mà kết quả sai thì đổi câu hỏi: kiểm **kích thước artifact** và **thời lượng job** so với lần chạy trước. Hai con số đó bắt được phần lớn ca im lặng.

Trường hợp đặc biệt cần nêu: nếu job ở `pending` và **không có log**, không có gì để đọc — chuyển thẳng sang hỏi API `runners/all` xem có runner nào khớp `tags` không.

**Tiêu chí chấm:**
- 0đ: "Chạy lại xem sao."
- 1đ: Đọc log tìm chữ `ERROR`.
- 2đ: Xác định pha trước rồi mới ánh xạ sang nhóm nguyên nhân.
- 3đ: Đủ bốn nhịp, **và** nêu được trường hợp job xanh mà sai, **và** nêu được ca `pending` không có log.

**Câu hỏi đào sâu:** Bạn đã thử lại pipeline 3 lần và nó lúc xanh lúc đỏ. Nghi phạm số một? *(Cache — vì nó là đường vào duy nhất **không được đảm bảo**, và nó phụ thuộc job rơi vào runner nào. Kiểm bằng cách so log của lần xanh và lần đỏ ở dòng `Restoring cache`.)*

---

## V3. Câu chốt để nói khi phỏng vấn

> Bốn câu dưới đây viết **nguyên văn, đúng ngữ điệu nói**. Học viên tập nói to từng câu tới khi trôi chảy mà không phải nghĩ.
> Mỗi câu chứa một con số hoặc một cơ chế — đó là thứ phân biệt câu trả lời của người đã làm với câu trả lời của người đã đọc.

**Câu 1 — khi được hỏi "bạn gỡ lỗi pipeline thế nào":**

> "Việc đầu tiên tôi làm không phải là đọc thông báo lỗi, mà là tìm dòng tiêu đề pha cuối cùng trước nó. Một job GitLab chạy tám pha cố định, và mỗi pha ứng với một nhóm nguyên nhân khác hẳn nhau. Nếu lỗi ở `get_sources` thì đó là chuyện quyền hoặc mạng, sửa code không giúp gì. Nếu trong log thậm chí không có dòng `Executing step_script` thì lệnh của tôi còn chưa chạy lần nào. Việc này mất mười giây và nó loại bỏ khoảng ba phần tư số giả thuyết."

**Câu 2 — khi được hỏi "cache và artifact khác nhau chỗ nào":**

> "Khác ở sự đảm bảo, không phải ở cách dùng. Artifact là hợp đồng — nó nằm trên GitLab, và job phụ thuộc sẽ đỏ nếu không có. Cache là tối ưu — nó nằm trên runner, và khi không tìm thấy thì runner chỉ ghi một dòng log rồi chạy tiếp. Nói cách khác, cache miss làm job **chậm** chứ không làm job **hỏng**. Nếu ở chỗ nào cache miss làm pipeline đỏ, thì đó là bằng chứng người ta đang dùng cache như artifact — và đấy chính là nguyên nhân của loại lỗi chạy tốt chín lần rồi hỏng lần thứ mười."

**Câu 3 — khi được hỏi "bạn quan tâm nhất điều gì trong một pipeline":**

> "Tôi phân loại hỏng theo hai trục: có báo hay không, và có chặn hay không. Job đỏ là loại rẻ nhất, phát hiện trong vài giây. Loại tôi sợ là im lặng và không chặn — job xanh nhưng artifact rỗng, hoặc test thực ra không chạy. Ở đó thời gian phát hiện tính bằng tuần, và người phát hiện thường là người dùng chứ không phải chúng tôi. Nên mọi thứ tôi làm với pipeline đều nhằm một việc: đẩy các chế độ hỏng về ô 'job đỏ ngay'."

**Câu 4 — khi được hỏi "bạn cải thiện được gì cho pipeline của đội cũ":**

> "Một việc rất nhỏ nhưng đo được. Tôi thêm khẳng định vào các bước sinh hiện vật — kiểu `test -s dist/app.js` ngay sau khi build. Một khẳng định như thế tốn khoảng năm phần trăm giây, so với pipeline chạy mười phút thì không đo nổi. Nhưng nó biến một hỏng im lặng thành một job đỏ. Lần đầu bật lên, chúng tôi phát hiện có hai job đang đóng gói artifact rỗng suốt mấy tuần mà không ai biết, vì mẫu đường dẫn trỏ sai thư mục và pha upload vẫn báo thành công."

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
| ≥ 80% | Nắm vững. Giao bài tập mở rộng §L10 ở buổi sau |
| 60–79% | Đạt. Đọc lại phần quy tắc bị mất điểm trước buổi 02 |
| 40–59% | Chưa đạt. Làm lại bước lab tương ứng ở nhà |
| < 40% | Chưa đạt. Học lại cả buổi trước khi sang buổi 02 — buổi 02 dựng thẳng lên mô hình này |

**Bảng lỗi làm trần điểm là 1:**

| Lỗi | Vì sao nghiêm trọng đến mức trần điểm |
|---|---|
| "Cache và artifact giống nhau, chỉ khác cách dùng" | Hiểu sai gốc rễ, sinh ra loại lỗi ngẫu nhiên tốn nhiều thời gian nhất ở nơi làm việc |
| "Job xanh nghĩa là công việc đã xong" | Hiểu sai mà cả khoá dựng lên để phá |
| Nói "nhanh hơn nhiều", "tốn lắm" và khi hỏi lại vẫn không có con số | Vi phạm nguyên tắc của khoá; và ở phỏng vấn thật đây là dấu hiệu người chưa đo bao giờ |

---

## V5. Bài tập về nhà

### BTVN 1. Áp vào repo thật — việc 1 và việc 2

Lấy một repo đang chạy của mình (hoặc của đội). Làm hai việc đầu trong mục "Đưa vào việc thật" của `01-ly-thuyet.md` §8:

1. Mở log **một** job và đánh dấu tám pha. Ghi thời lượng từng pha.
2. Liệt kê mọi job và đánh dấu job nào **không** dùng artifact của stage trước.

**Nộp:** một bảng tám pha của repo thật, và danh sách job có thể thêm `dependencies: []` kèm ước tính giây tiết kiệm.

### BTVN 2. Đếm số bước đang hỏng im lặng

Trong repo đó, đếm số job có khối `artifacts:` và số job có ít nhất một khẳng định (`test -s`, `test -d`, hoặc tương đương).

**Nộp:** hai con số và tỉ số của chúng. Tỉ số càng xa 1 thì càng nhiều bước đang hỏng im lặng.

### BTVN 3. Viết ba khẳng định

Chọn job build quan trọng nhất trong repo đó và viết **ba** khẳng định cho nó — nhưng **đừng đẩy lên nhánh chính**. Đẩy lên một nhánh riêng và chạy thử.

**Nộp:** ba khẳng định, và trả lời: chúng bắt được ca hỏng nào mà pipeline hiện tại đang bỏ lọt? Viết cụ thể, không viết chung chung.

### BTVN 4. Chuẩn bị cho buổi 02

Trả lời ba câu sau bằng viết, mỗi câu 3–5 dòng. Mang theo vào buổi 02.

1. Buổi 01 QT 6.1 nói executor `shell` giữ lại trạng thái của máy giữa hai job. Hãy nêu **hai** thứ cụ thể có thể rò rỉ từ job này sang job kia trên một runner `shell`, và với mỗi thứ, nói nó thuộc ô nào của bảng hai thuộc tính (QT 7.1).
2. Một runner nhận được **bao nhiêu job cùng lúc**? Con số đó đặt ở đâu — trong `.gitlab-ci.yml`, trong giao diện GitLab, hay ở chỗ khác? Nếu bạn chưa biết, hãy tìm trong container `lab-runner` và ghi lại đường dẫn tệp bạn tìm thấy.
3. Trong tám pha của QT 4.2, pha nào **không** phụ thuộc vào `.gitlab-ci.yml` mà phụ thuộc vào cấu hình runner? Nêu ít nhất hai pha và giải thích ngắn gọn vì sao.

**Ba câu này dẫn vào đâu:** câu 1 dẫn vào phần mô hình cô lập của ba executor ở buổi 02; câu 2 dẫn thẳng vào `concurrent` và `limit` trong `config.toml`, tức phần cấu hình runner mà học viên chưa hề đụng tới ở buổi 01; câu 3 dẫn vào việc **phân chia trách nhiệm giữa người viết pipeline và người vận hành runner** — chủ đề trung tâm của buổi 02, và là thứ quyết định ai phải sửa khi pipeline hỏng.
{% endraw %}
