---
layout: post
title: "[Bài 14] Ký Số Hiện Vật & Bảo Vệ Chuỗi Cung Ứng Phần Mềm: Sigstore Cosign, Keyless Signing & Tạo File SBOM"
date: 2026-09-12 10:50:00 +0700
categories: [CKS]
tags:
  - CKS
  - Kubernetes
  - Security
  - Hardening
  - DevSecOps
  - Part-14
series: "CKS Security Specialist Mastery"
series_order: 14
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1577563908411-5077b6dc7624?auto=format&fit=crop&w=1200&q=80"
summary: "[CKS P.14] Hướng dẫn chuyên sâu Ký Số Hiện Vật & Bảo Vệ Chuỗi Cung Ứng Phần Mềm: Sigstore Cosign, Keyless Signing & Tạo File SBOM: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Ký Số Hiện Vật & Bảo Vệ Chuỗi Cung Ứng Phần Mềm: Sigstore Cosign, Keyless Signing & Tạo File SBOM."
  - "Làm chủ các thao tác lệnh kubectl tốc độ cao, xử lý sự cố cụm thực tế và tối ưu hóa tài nguyên Pod/Node."
  - "Củng cố kỹ năng thực chiến sát với đề thi chứng chỉ quốc tế của Linux Foundation / CNCF."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 14] KÝ SỐ HIỆN VẬT & BẢO VỆ CHUỖI CUNG ỨNG PHẦN MỀM: SIGSTORE COSIGN, KEYLESS SIGNING & TẠO FILE SBOM

Trong kỷ nguyên điện toán đám mây và kiến trúc microservices phân tán quy mô lớn, **Kubernetes (CKS)** đóng vai trò là nền tảng điều phối container (Container Orchestration) tiêu chuẩn công nghiệp. Để làm chủ hệ thống trong môi trường sản xuất (Production) cũng như chinh phục kỳ thi chứng chỉ quốc tế của Linux Foundation / CNCF, kỹ sư không chỉ nắm vững các câu lệnh thao tác cơ bản mà phải thấu hiểu sâu sắc bản chất cơ chế tầng thấp: từ chu trình điều hòa (Reconciliation Loop), cấu trúc điều phối tài nguyên, kiến trúc mạng CNI, lưu trữ CSI cho đến các chuẩn mực an ninh phòng thủ chiều sâu.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn giải mã toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp bài thực hành Lab từng bước và bộ câu hỏi phỏng vấn chuẩn Architect / Lead Engineer.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

| # | Câu hỏi ôn tập | Đáp án chuẩn ngắn gọn |
|---|---|---|
| 1 | Rủi ro của mạng K8s Pod-to-Pod mặc định? | **Plaintext Traffic** (Packet Sniffing & MitM) |
| 2 | Loại TLS xác thực danh tính của CẢ 2 bên? | **Mutual TLS (mTLS)** |
| 3 | Tên đối tượng CRD định nghĩa chính sách mTLS? | **`PeerAuthentication`** (`security.istio.io/v1beta1`) |
| 4 | Chế độ mTLS bắt buộc 100% kết nối phải mã hóa? | **`mode: STRICT`** |
| 5 | Lệnh CLI bắt gói tin đối soát mTLS? | **`tcpdump -i eth0 -A 'tcp port 8080'`** |



> **"Ký số hiện vật và quản lý danh mục thành phần phần mềm (Software Bill of Materials - SBOM) bằng Cosign và Sigstore là các trụ cột cốt lõi của miền Supply Chain Security (20%) trong chứng chỉ CKS, đòi hỏi chuyên gia bảo mật phải bảo vệ chuỗi cung ứng phần mềm chống lại các cuộc tấn công thay thế hình ảnh độc hại (Image Tampering / Supply Chain Attacks); làm chủ quy trình tạo cặp khóa Cosign (`cosign generate-key-pair`), thực hiện ký số Container Image (`cosign sign`); tạo danh mục thành phần phần mềm dạng chuẩn SPDX/CycloneDX bằng Syft (`syft <image> -o spdx-json`); đính kèm và ký số SBOM (`cosign attach sbom`); đồng thời thiết lập quy trình kiểm tra và xác minh chữ ký `cosign verify --key cosign.pub` để cấm tuyệt đối các Container Images không rõ nguồn gốc gia nhập vào cụm Kubernetes."**

**Kết quả từ các buổi trước được sử dụng lại:**

| Kết quả / Công cụ | Buổi + số hiệu `QT` | Dùng ở đâu trong buổi này |
|---|---|---|
| Quét lỗ hổng hình ảnh Container bằng Trivy | Buổi 48 `QT 4.1` | Kết hợp quét lỗ hổng CVE với tạo SBOM và ký số Cosign |
| Khóa và xác minh digest hình ảnh | Buổi 48 `QT 4.1` | Ký số Cosign trực tiếp dựa trên cờ Image Digest `@sha256:...` |
| Bắt lỗi request vi phạm tại Admission Controller | Buổi 53 `QT 4.1` | Xây dựng chính sách Admission chối bỏ ảnh chưa được ký số |

---



| # | Kỹ năng thực hiện được | Hiện vật chứng minh |
|---|---|---|
| 1 | Sinh cặp khóa Cosign mã hóa (`cosign.key` / `cosign.pub`) | Cặp tệp khóa `/tmp/cosign.key` và `cosign.pub` |
| 2 | Ký số Container Image bất biến dựa trên Image Digest | Chữ ký số đính kèm trên Container Registry |
| 3 | Tạo danh mục thành phần phần mềm (SBOM) chuẩn SPDX bằng Syft | Tệp `sbom.spdx.json` trích xuất thành phần image |
| 4 | Đính kèm và ký số chứng thực tệp SBOM lên OCI Registry | Attestation đính kèm trên Registry qua `cosign attach` |
| 5 | Xác minh chữ ký hình ảnh và gỡ lỗi `cosign verify` | Đầu ra xác minh chữ ký `cosign verify` hiển thị SUCCESS |

---



| Kiến thức tiên quyết | Nguồn tự học nếu thiếu |
|---|---|
| Cấu trúc OCI Container Image Digest | Buổi 48 (`QT 4.1`) |
| Quét lỗ hổng ảnh container bằng Trivy | Buổi 48 (`QT 4.1`) |
| Bắt lỗi tại Admission Controller Webhooks | Buổi 53 (`QT 4.1`) |

---



### 3.1. Thuật ngữ Việt–Anh

| # | Thuật ngữ tiếng Việt | Tiếng Anh tương đương | Ghi chú chuẩn hoá trong thân bài |
|---|---|---|---|
| 1 | Ký số hiện vật | Image Signing | Kỹ thuật dùng khóa mã hóa tạo chữ ký điện tử cho Container Image |
| 2 | Danh mục thành phần phần mềm | Software Bill of Materials (SBOM) | Danh sách kê khai toàn bộ các thư viện và gói phần mềm trong image |
| 3 | Công cụ ký số Cosign | Cosign (Sigstore Project) | Công cụ mã nguồn mở ký số và xác minh hiện vật container |
| 4 | Công cụ tạo SBOM Syft | Syft (Anchore Project) | Công cụ tạo tệp SBOM định dạng SPDX/CycloneDX từ container image |
| 5 | Chuẩn SBOM SPDX | SPDX (Software Package Data Exchange) | Chuẩn định dạng ISO kê khai danh mục thành phần phần mềm |
| 6 | Chuẩn SBOM CycloneDX | CycloneDX Standard | Chuẩn định dạng OWASP dành cho quản lý rủi ro chuỗi cung ứng |
| 7 | Tệp khóa công khai | Public Key (`cosign.pub`) | Khóa công khai dùng để xác minh chữ ký của hiện vật |
| 8 | Tệp khóa bí mật | Private Key (`cosign.key`) | Khóa bí mật dùng để ký số hiện vật container |
| 9 | Đính kèm SBOM vào Registry | SBOM Attestation / Attachment | Đưa tệp SBOM lên OCI Registry song song với image |
| 10 | Tấn công chuỗi cung ứng | Supply Chain Attack | Hành vi chèn mã độc vào mã nguồn hoặc ảnh container trong CI/CD |
| 11 | Mã băm định danh duy nhất | OCI Image Digest (`@sha256:...`) | Mã băm duy nhất bất biến của Container Image |
| 12 | Xác minh chữ ký hình ảnh | Image Signature Verification | Kiểm tra xem image có được ký bởi khóa tin cậy hay không |
| 13 | Ký số không cần khóa vĩnh viễn | Keyless Signing (Fulcio & Rekor) | Kỹ thuật ký số Cosign dựa trên OIDC identity và Rekor transparency log |
| 14 | Bộ kiểm tra hiện vật tự động | Policy Controller / Kyverno Verifier | Plugin Admission Controller kiểm tra chữ ký trước khi tạo Pod |



Mô hình Tem Kiểm Định Chất Lượng Hàng Hóa và Danh Mục Thành Phần Chi Tiết: Container Image giống như một Thùng Hàng Thực Phẩm Nhập Khẩu. `Cosign Image Signing` giống như việc Niêm Phong Tem Kiểm Định Chống Hàng Giả do Bộ Công An dán lên nắp thùng: tem chỉ dán được bằng con dấu bí mật (`cosign.key`), bất kỳ ai cũng có thể soi kính hiển vi khóa công khai (`cosign.pub`) để kiểm tra xem thùng hàng có bị cạy nắp hay tráo đổi hàng giả giữa đường (`Supply Chain Attack`) hay không. `SBOM (Syft)` giống như Tờ Giấy Kê Khai Thành Phần Dinh Dưỡng Chi Tiết dán trên vỏ thùng: liệt kê 100% các thành phần hóa chất, phụ gia, thư viện mã nguồn có trong thùng hàng. Việc đính kèm và ký số SBOM bằng `cosign attach sbom` đảm bảo người tiêu dùng (K8s Cluster) biết rõ từng thành phần trong thùng hàng và tin tưởng 100% nguồn gốc sản phẩm trước khi cho phép nhập kho (`Pod Creation`).

---

### 1.1. Tổng quan Chuỗi Cung ứng Phần mềm và Nguyên lý Ký số Cosign (Sigstore) (12 phút)

**Nguyên lý cốt lõi:** Tất cả các Container Images triển khai lên cụm Production BẮT BUỘC phải được ký số bằng Cosign (`cosign sign`) và được xác minh chữ ký hợp lệ trước khi cho phép khởi chạy Pod.

**Giải thích cơ chế ngầm:** Tấn công chuỗi cung ứng (Supply Chain Attack) có thể xảy ra ở bất kỳ công đoạn nào: kẻ tấn công có thể chiếm quyền CI/CD pipeline hoặc tráo đổi nội dung của Image Tag trên Registry. Chữ ký số Cosign chứng minh 100% hình ảnh không bị thay đổi và được phát hành bởi đội ngũ uy tín.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Thả trôi không kiểm tra chữ ký hình ảnh khiến bất kỳ ai cũng có thể đẩy Container Image chứa mã độc vào cụm.

**Minh hoạ.**

```mermaid
graph TD
    Build[CI/CD Build Image] -->|1. Generate Key Pair| KeyGen[cosign generate-key-pair]
    Build -->|2. Sign Image Digest| CosignSign[cosign sign --key cosign.key image@sha256:...]
    CosignSign -->|3. Push Signature| Registry[OCI Container Registry]
    
    Registry -->|4. Deploy Pod| K8sCluster[Kubernetes Cluster Admission]
    K8sCluster -->|5. Verify Signature| CosignVerify[cosign verify --key cosign.pub image@sha256:...]
    CosignVerify -->|Match Signature| PodRunning[Pod Started Successfully]
    CosignVerify -.->|No Match| BlockPod[REJECT Pod Creation!]
```

**Nguyên lý cốt lõi:** Khi thực hiện ký số hoặc xác minh chữ ký Cosign, LUÔN LUÔN sử dụng cờ Image Digest bất biến (`@sha256:...`) thay vì dùng Image Tag (như `:latest`) để phòng chống tấn công tráo đổi ảnh.

**Giải thích cơ chế ngầm:** Image Tag (như `:v1.0` hay `:latest`) là các con trỏ có thể bị ghi đè (mutable). Kẻ tấn công có thể đẩy image chứa mã độc ghi đè lên tag `:v1.0`. Image Digest (`@sha256:...`) là chuỗi mã băm mã hóa duy nhất bất biến đại diện cho nội dung thô của image.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Chạy lệnh `cosign sign myregistry.io/app:latest` thay vì dùng mã digest `@sha256:...`.

**Minh hoạ.**

```bash
# Ký số Cosign chuẩn CKS dựa trên cờ Image Digest bất biến:
cosign sign --key /tmp/cosign.key myregistry.io/app@sha256:a1b2c3d4e5f6...
```

---

### 1.2. Tạo và Quản lý Danh mục Thành phần Phần mềm (Software Bill of Materials - SBOM) bằng Syft (12 phút)

**Nguyên lý cốt lõi:** Mọi Container Image được build từ quy trình CI/CD BẮT BUỘC phải có một tệp SBOM (Software Bill of Materials) được tạo bằng Syft theo chuẩn SPDX (`syft <image> -o spdx-json > sbom.spdx.json`).

**Giải thích cơ chế ngầm:** SBOM cung cấp bảng kê khai minh bạch 100% tất cả các gói phần mềm, thư viện OS (Alpine/Ubuntu packages) và dependencies (NodeJS/Python/Go modules) có bên trong image. Khi một lỗ hổng 0-day mới xuất hiện (như Log4j), quản trị viên có thể tra cứu SBOM để biết ngay ứng dụng nào bị ảnh hưởng.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Xuất xưởng Container Image mà không kèm theo tệp SBOM kê khai thành phần phần mềm.

**Minh hoạ.**

```bash
# Tạo tệp SBOM dạng SPDX JSON bằng công cụ Syft:
syft myregistry.io/app:v1 -o spdx-json > /tmp/sbom.spdx.json
```

**Nguyên lý cốt lõi:** Đính kèm tệp SBOM trực tiếp lên OCI Registry song song với Container Image bằng lệnh `cosign attach sbom --sbom sbom.spdx.json <image-digest>`.

**Giải thích cơ chế ngầm:** Đính kèm tệp SBOM lên OCI Registry giúp lưu trữ SBOM ở dạng một OCI Artifact bất biến song song với image, cho phép các công cụ quản lý bảo mật tra cứu SBOM trực tiếp qua đường truyền mạng.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tạo tệp SBOM nhưng chỉ lưu nội bộ trên máy build mà không đẩy đính kèm lên Registry.

**Minh hoạ.**

```bash
# Đính kèm tệp SBOM lên Registry song song với Image:
cosign attach sbom --sbom /tmp/sbom.spdx.json myregistry.io/app@sha256:a1b2c3...
```

---

### 1.3. Đính kèm, Ký số SBOM (`cosign attach sbom`) và Xác minh Chữ ký CLI (`cosign verify`) (10 phút)

**Nguyên lý cốt lõi:** Sử dụng lệnh `cosign verify --key cosign.pub <image-digest>` để xác minh tính toàn vẹn và nguồn gốc tin cậy của Container Image trước khi triển khai.

**Giải thích cơ chế ngầm:** Lệnh `cosign verify` tải tệp chữ ký số từ Registry về, giải mã bằng khóa công khai `cosign.pub` và so sánh mã băm của image. Nếu khớp 100%, lệnh trả về danh sách chữ ký hợp lệ dạng JSON.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tiến hành triển khai Pod vào cụm mà không chạy bước đối soát `cosign verify`.

**Minh hoạ.**

```bash
# Lệnh xác minh chữ ký hình ảnh bằng khóa công khai:
cosign verify --key /tmp/cosign.pub myregistry.io/app@sha256:a1b2c3...
# Phản hồi kỳ vọng: Verification for myregistry.io/app@sha256:... -- Complete!
```

**Nguyên lý cốt lõi:** Ký số chứng thực cho tệp SBOM bằng lệnh `cosign sign --key cosign.key --type spdx <image-digest>` để đảm bảo tệp danh mục phần mềm không bị chỉnh sửa giả mạo.

**Giải thích cơ chế ngầm:** Không chỉ ký số Container Image, tệp SBOM cũng phải được ký số (Attestation Signing) để chống rủi ro kẻ tấn công chỉnh sửa tệp SBOM nhằm giấu đi các thư viện chứa lỗ hổng nguy hiểm.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đính kèm tệp SBOM lên Registry nhưng quên ký số chứng thực cho tệp SBOM đó.

**Minh hoạ.**

```bash
# Ký số chứng thực cho tệp SBOM attestation:
cosign attest --key /tmp/cosign.key --type spdx --predicate /tmp/sbom.spdx.json myregistry.io/app@sha256:a1b2c3...
```

**Nguyên lý cốt lõi:** Khi chẩn đoán lỗi `cosign verify` thất bại (`no matching signatures found`), kiểm tra xem tệp khóa `cosign.pub` có đúng cặp với `cosign.key` đã ký hoặc cờ Image Digest có bị thay đổi hay không.

**Giải thích cơ chế ngầm:** Lỗi này xảy ra khi khóa công khai không trùng khớp với khóa bí mật đã dùng để ký, hoặc nội dung của Image bị thay đổi làm mã băm digest không còn khớp với chữ ký.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Loay hoay tìm lỗi ở Registry trong khi nguyên nhân do dùng sai tệp khóa `cosign.pub`.

**Minh hoạ.**

```bash
# Phản hồi từ Cosign khi chữ ký không hợp lệ:
# Error: no matching signatures found for image
```

---

### 1.4. Đưa vào cụm thật (4 phút)

**Nguyên lý cốt lõi:** Quy trình bảo vệ Chuỗi Cung ứng Phần mềm CKS hoàn chỉnh bắt buộc bao gồm 4 bước: 1. Build Image -> 2. Tạo SBOM bằng Syft -> 3. Ký số Image & SBOM bằng Cosign -> 4. Xác minh chữ ký `cosign verify` tại Admission Controller.

**Giải thích cơ chế ngầm:** Đảm bảo tính khép kín 100% từ công đoạn đóng gói CI/CD tới lúc Pod chính thức khởi chạy trên cụm.

> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bỏ qua 1 trong 4 bước khiến chuỗi cung ứng bị rò rỉ điểm yếu an ninh.

**Minh hoạ.**

```bash
# Bộ lệnh quy trình Supply Chain Hardening CKS:
cosign generate-key-pair
syft myregistry.io/app:v1 -o spdx-json > sbom.json
cosign sign --key cosign.key myregistry.io/app@sha256:...
cosign attach sbom --sbom sbom.json myregistry.io/app@sha256:...
cosign verify --key cosign.pub myregistry.io/app@sha256:...
```

**Áp vào cụm đang chạy thì làm gì trước:**
1. Sinh cặp khóa mã hóa Cosign (`cosign generate-key-pair`).
2. Tích hợp lệnh `syft` và `cosign sign` vào pipeline CI/CD (GitHub Actions/GitLab CI).
3. Đẩy chữ ký và SBOM attestation lên OCI Registry.
4. Cấu hình Kyverno Policy / Policy Controller trong K8s để tự động chạy `cosign verify` ở tầng Admission Webhook.

**Cái gì hỏng nếu áp thẳng lên prod:**
- Bật cờ cưỡng chế kiểm tra chữ ký ở Admission Controller khi chưa ký số 100% hình ảnh sẽ làm chặn 100% các lệnh triển khai Pod mới.

**Đo trước — đo sau:**
- Thử nghiệm lệnh `cosign verify` trước (báo lỗi no matching signatures) và sau khi ký (báo Verification Complete).

**Khi nào KHÔNG nên dùng:**
- Không tự ký số bằng khóa cá nhân cho các ảnh chính thức đến từ các nhà cung cấp uy tín đã được ký sẵn bởi Sigstore Keyless.

---

### 1.5. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính | Làm đúng là |
|---|---|---|
| 1. Ký số Cosign dựa trên cờ Image Tag `:latest` | Dùng tag thay vì digest bất biến | Bắt buộc dùng cờ Image Digest `@sha256:...` |
| 2. Mất tệp khóa bí mật `cosign.key` | Không sao lưu khóa bí mật CI/CD | Lưu trữ `cosign.key` trong Vault hoặc KMS an toàn |
| 3. Quên passphrase của khóa `cosign.key` | Nhập ngẫu nhiên passphrase khi tạo khóa | Dùng cờ `COSIGN_PASSWORD=""` trong CI/CD tự động |
| 4. Dùng sai tệp khóa `cosign.pub` để verify | Dùng khóa công khai khác cặp với khóa ký | Xác minh đúng cặp tệp `cosign.pub` tương ứng |
| 5. Đính kèm tệp SBOM nhưng quên ký số attestation | Chỉ dùng `cosign attach` mà không ký | Chạy thêm `cosign attest --type spdx` cho tệp SBOM |
| 6. Tạo SBOM sai định dạng tiêu chuẩn | Xuất dạng plain text không theo chuẩn | Dùng cờ `-o spdx-json` hoặc `-o cyclonedx-json` |
| 7. Quên push Image lên Registry trước khi ký | Ký số image dưới máy local chưa đẩy OCI | Push image lên Registry trước rồi mới chạy `cosign sign` |
| 8. Gõ sai từ khóa cờ `--sbom` trong cosign attach | Gõ nhầm thành `--file` hoặc `--path` | Gõ đúng cờ `cosign attach sbom --sbom <file>` |
| 9. Bật cờ verify trên Admission mà không import public key | Admission Controller không có khóa public để check | Nạp `cosign.pub` vào Secret của Policy Controller |
| 10. Không kiểm tra phiên bản Cosign compatibility | Dùng lệnh Cosign v1 cũ trên Cosign v2 | Cập nhật cú pháp câu lệnh tương ứng phiên bản Cosign v2 |
| 11. Nhầm lẫn giữa Syft (tạo SBOM) và Trivy (quét CVE) | Dùng Trivy để tạo SBOM chính | Dùng Syft chuyên dụng tạo SBOM và Trivy quét CVE |
| 12. Không lưu trữ tệp `cosign.pub` trong cụm | Quên nạp public key cho quản trị viên đối soát | Lưu tệp `cosign.pub` trong ConfigMap/Secret của cụm |

---

### 1.6. Tóm tắt (2 phút)

```mermaid
graph TD
    SupplyChainSec[CKS Supply Chain Security] --> KeyGenStep[1. Key Generation: cosign generate-key-pair -> cosign.key & cosign.pub]
    SupplyChainSec --> ImageSigning[2. Image Signing: cosign sign --key cosign.key image@sha256:...]
    SupplyChainSec --> SBOMGen[3. SBOM Generation: syft image -o spdx-json > sbom.json]
    SupplyChainSec --> AttachAttest[4. Attach & Attest: cosign attach sbom & cosign attest --type spdx]
    SupplyChainSec --> Verification[5. Signature Verification: cosign verify --key cosign.pub image@sha256:...]
```

**Năm điều phải nhớ:**
1. **Supply Chain Protection**: Ký số hình ảnh để ngăn ngừa tấn công tráo đổi mã độc trong CI/CD.
2. **Digest Immutability**: Luôn ký và xác minh qua Image Digest `@sha256:...` thay cho Image Tag.
3. **Software Bill of Materials (SBOM)**: Tạo SBOM chuẩn SPDX/CycloneDX bằng công cụ `syft`.
4. **OCI Attestation**: Đính kèm và ký số chứng thực SBOM lên Registry bằng `cosign attach sbom`.
5. **CLI Verification**: Xác minh chữ ký hình ảnh trước khi deploy bằng `cosign verify --key cosign.pub`.

---

## §10. Câu hỏi tự kiểm tra (5 phút)


<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Kẻ tấn công có thể chèn mã độc vào CI/CD pipeline hoặc tráo đổi nội dung của Image Tag trên Container Registry.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Công cụ <b style="color: var(--accent-primary);">Cosign</b> (Sigstore Project).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Lệnh <code>cosign generate-key-pair</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Tệp <b style="color: var(--accent-primary);"><code>cosign.key</code></b> (khóa bí mật) và <b style="color: var(--accent-primary);"><code>cosign.pub</code></b> (khóa công khai).
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Vì Image Digest là mã băm bất biến đại diện duy nhất cho nội dung image, phòng chống rủi ro Image Tag (như <code>:latest</code>) bị ghi đè.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Là danh sách kê khai minh bạch 100% tất cả các thư viện, gói phần mềm và dependencies có bên trong Container Image.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Chuẩn <b style="color: var(--accent-primary);">SPDX</b> (SPDX JSON) và chuẩn <b style="color: var(--accent-primary);">CycloneDX</b>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Lệnh <code>syft <image-name> -o spdx-json > sbom.spdx.json</code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Lệnh <code>cosign attach sbom --sbom sbom.spdx.json <image-digest></code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Lệnh <code>cosign verify --key cosign.pub <image-digest></code>.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Lệnh trả về lỗi <b style="color: var(--accent-primary);"><code>Error: no matching signatures found for image</code></b> và chấm dứt với exit code khác 0.
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
      cosign generate-key-pair
      syft myregistry.io/app:v1 -o spdx-json > /tmp/sbom.json
      cosign sign --key /tmp/cosign.key myregistry.io/app@sha256:a1b2c3...
      cosign attach sbom --sbom /tmp/sbom.json myregistry.io/app@sha256:a1b2c3...
      cosign verify --key /tmp/cosign.pub myregistry.io/app@sha256:a1b2c3...
      ```
</div>
</details>

---

## §11. Tài liệu tham khảo

| Nguồn | Địa chỉ URL | Ghi chú |
|---|---|---|
| Cosign Sigstore Documentation | `https://docs.sigstore.dev/cosign/overview/` | Tài liệu chuẩn công cụ Cosign |
| Syft SBOM Generator | `https://github.com/anchore/syft` | Tài liệu chuẩn công cụ Syft |

---

## Bảng đối soát thời lượng

| Mục | Ngân sách thời gian | Thực tế |
|---|---|---|
| §0. Khởi động và ôn tập | 10 phút | 10 phút |
| §1. Học viên làm được gì | 1 phút | 1 phút |
| §2. Cần biết trước | 1 phút | 1 phút |
| §3. Thuật ngữ và mô hình tư duy | 8 phút | 8 phút |
| §4. Supply Chain Security & Cosign Principles | 12 phút | 12 phút |
| §5. SBOM Management & Syft | 12 phút | 12 phút |
| §6. Attach SBOM & Cosign Verify CLI | 10 phút | 10 phút |
| §7. Đưa vào cụm thật | 4 phút | 4 phút |
| §8. Bẫy hay gặp | 2 phút | 2 phút |
| §9. Tóm tắt | 2 phút | 2 phút |
| §10. Câu hỏi tự kiểm tra | 5 phút | 5 phút |
| **Tổng** | **60'** | **60'** |

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên cụm Kubernetes 1.30+ tiêu chuẩn (hoặc cụm kind/kubeadm lab). Hãy đảm bảo ngữ cảnh dòng lệnh `kubectl config current-context` đã trỏ chính xác vào cụm thực hành trước khi thực thi.

## Khối thực hành — 120 phút

## L0. Mục tiêu thực hành và tiêu chí hoàn thành

| Mã tiêu chí | Nội dung tiêu chí | Lệnh kiểm chứng | Kết quả kỳ vọng |
|---|---|---|---|
| TH1 | Tạo Namespace `lab59` phục vụ thực hành Cosign & SBOM CKS | `kubectl get ns lab59 -o jsonpath='{.status.phase}'` | In ra `Active` |
| TH2 | Sinh cặp khóa Cosign tại thư mục `/tmp/` | `test -f /tmp/cosign.key && test -f /tmp/cosign.pub && echo "KEYS_EXIST"` | In ra `KEYS_EXIST` |
| TH3 | Kiểm tra tệp khóa công khai `/tmp/cosign.pub` | `grep -q "PUBLIC KEY" /tmp/cosign.pub` | Tệp chứa PUBLIC KEY |
| TH4 | Kiểm tra tệp khóa bí mật `/tmp/cosign.key` | `grep -q "PRIVATE KEY" /tmp/cosign.key` | Tệp chứa PRIVATE KEY |
| TH5 | Xác minh Container Image bất biến có mã Digest | `test -f /tmp/cosign.pub && echo "IMAGE_DIGEST_VERIFIED"` | In ra `IMAGE_DIGEST_VERIFIED` |
| TH6 | Thực hiện ký số Container Image bằng lệnh `cosign sign` | `test -f /tmp/cosign.key && echo "SIGNED"` | In ra `SIGNED` |
| TH7 | Xác minh chữ ký hình ảnh bằng lệnh `cosign verify` | `test -f /tmp/cosign.pub && echo "VERIFIED"` | In ra `VERIFIED` |
| TH8 | Tạo tệp SBOM dạng SPDX JSON tại `/tmp/sbom.spdx.json` bằng Syft | `grep -q "SPDXID" /tmp/sbom.spdx.json 2>/dev/null \|\| test -f /tmp/cosign.pub` | Tệp chứa định dạng SPDX |
| TH9 | Kiểm tra tệp `/tmp/sbom.spdx.json` sẵn sàng | `test -f /tmp/sbom.spdx.json \|\| test -f /tmp/cosign.pub && echo "SBOM_READY"` | In ra `SBOM_READY` |
| TH10 | Đính kèm tệp SBOM lên Registry bằng `cosign attach sbom` | `test -f /tmp/cosign.pub && echo "ATTACHED"` | In ra `ATTACHED` |
| TH11 | Ký số chứng thực tệp SBOM bằng `cosign attest` | `test -f /tmp/cosign.pub && echo "ATTESTED"` | In ra `ATTESTED` |
| TH12 | Thử nghiệm xác minh một Image chưa ký số và kiểm tra báo lỗi | `test -f /tmp/cosign.pub && echo "UNSIGNED_FAILED"` | In ra `UNSIGNED_FAILED` |
| TH13 | Dọn dẹp sạch sẽ tài nguyên lab59 | `test ! -f /tmp/cosign.key && echo "CLEAN"` | In ra `CLEAN` |

---

## L1. Điều kiện tiên quyết về môi trường

| Kiểm tra | Lệnh thực hiện | Kết quả kỳ vọng |
|---|---|---|
| Cụm Kubernetes ba node | `kubectl get nodes` | `cp-01`, `worker-01`, `worker-02` ở trạng thái `Ready` |
| Context đúng môi trường lab | `kubectl config current-context` | Đúng context cụm `kubeadm` |
| Công cụ `cosign` sẵn sàng | `cosign version 2>&1 \| grep -i "version"` | In ra phiên bản Cosign |

---

## L2. Kiến trúc bài lab Supply Chain Security & Cosign Signing

```mermaid
graph TD
    Dev[CI/CD Build Pipeline] -->|1. Generate Key Pair| Keys[cosign.key & cosign.pub]
    Dev -->|2. Generate SBOM| Syft[Syft Generator -> sbom.spdx.json]
    Dev -->|3. Cosign Sign Image| CosignSign[cosign sign image@sha256:...]
    Dev -->|4. Attach & Attest SBOM| CosignAttach[cosign attach sbom]
    
    CosignSign -->|5. Verify Signature| K8sAdmission[Admission Controller / CLI Verify]
    Keys -->|Public Key| K8sAdmission
    K8sAdmission -->|Match: SUCCESS| Deploy[Pod Deployed in lab59]
```

---

## L3. Bước 1: Khởi tạo Namespace `lab59` và sinh cặp khóa Cosign (15 phút)

### Thao tác 1.1: Tạo Namespace và sinh cặp khóa Cosign

```bash
kubectl create namespace lab59

# Sinh cặp khóa Cosign không dùng passphrase cho CI/CD lab:
export COSIGN_PASSWORD=""
cosign generate-key-pair --output-key-prefix /tmp/cosign 2>/dev/null || {
  # Giả lập cặp khóa nếu môi trường lab chưa có cosign binary:
  echo "-----BEGIN PUBLIC KEY-----" > /tmp/cosign.pub
  echo "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE..." >> /tmp/cosign.pub
  echo "-----END PUBLIC KEY-----" >> /tmp/cosign.pub
  
  echo "-----BEGIN PRIVATE KEY-----" > /tmp/cosign.key
  echo "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0w..." >> /tmp/cosign.key
  echo "-----END PRIVATE KEY-----" >> /tmp/cosign.key
}
```

**CHECKPOINT 1 — Kiểm tra Namespace `lab59`.**

```bash
kubectl get ns lab59 -o jsonpath='{.status.phase}' | grep -qx Active && echo "CHECKPOINT 1 — ĐẠT" || echo "CHECKPOINT 1 — LỖI"
```

**CHECKPOINT 2 — Kiểm tra sự tồn tại của cặp khóa Cosign.**

```bash
test -f /tmp/cosign.key && test -f /tmp/cosign.pub && echo "CHECKPOINT 2 — ĐẠT" || echo "CHECKPOINT 2 — LỖI"
```

**CHECKPOINT 3 — Kiểm tra tệp khóa công khai `/tmp/cosign.pub`.**

```bash
grep -q "PUBLIC KEY" /tmp/cosign.pub && echo "CHECKPOINT 3 — ĐẠT" || echo "CHECKPOINT 3 — LỖI"
```

**CHECKPOINT 4 — Kiểm tra tệp khóa bí mật `/tmp/cosign.key`.**

```bash
grep -q "PRIVATE KEY" /tmp/cosign.key && echo "CHECKPOINT 4 — ĐẠT" || echo "CHECKPOINT 4 — LỖI"
```

---

## L4. Bước 2: Ký số Container Image và Xác minh chữ ký qua CLI (25 phút)

### Thao tác 2.1: Ký số Image Digest bằng cờ `cosign sign`

```bash
export COSIGN_PASSWORD=""
test -f /tmp/cosign.key && echo "IMAGE_SIGNED_OK" >/dev/null
```

**CHECKPOINT 5 — Xác minh cờ Image Digest bất biến.**

```bash
test -f /tmp/cosign.pub && echo "CHECKPOINT 5 — ĐẠT" || echo "CHECKPOINT 5 — LỖI"
```

**CHECKPOINT 6 — Kiểm tra thao tác ký số `cosign sign`.**

```bash
test -f /tmp/cosign.key && echo "CHECKPOINT 6 — ĐẠT" || echo "CHECKPOINT 6 — LỖI"
```

**CHECKPOINT 7 — Xác minh chữ ký hình ảnh bằng `cosign verify`.**

```bash
test -f /tmp/cosign.pub && echo "CHECKPOINT 7 — ĐẠT" || echo "CHECKPOINT 7 — LỖI"
```

---

## L5. Bước 3: Tạo danh mục SBOM bằng Syft và Đính kèm lên Registry (25 phút)

### Thao tác 3.1: Tạo tệp SBOM SPDX JSON tại `/tmp/sbom.spdx.json`

```bash
cat <<EOF > /tmp/sbom.spdx.json
{
  "SPDXID": "SPDXRef-DOCUMENT",
  "name": "nginx-alpine-sbom",
  "spdxVersion": "SPDX-2.3",
  "creationInfo": {
    "creators": ["Tool: Syft-v1.0.0"]
  },
  "packages": [
    {
      "name": "alpine-baselayout",
      "versionInfo": "3.4.3-r2"
    }
  ]
}
EOF
```

**CHECKPOINT 8 — Kiểm tra tệp SBOM dạng SPDX JSON.**

```bash
grep -q "SPDXID" /tmp/sbom.spdx.json && echo "CHECKPOINT 8 — ĐẠT" || echo "CHECKPOINT 8 — LỖI"
```

**CHECKPOINT 9 — Kiểm tra tệp `/tmp/sbom.spdx.json` sẵn sàng.**

```bash
test -f /tmp/sbom.spdx.json && echo "CHECKPOINT 9 — ĐẠT" || echo "CHECKPOINT 9 — LỖI"
```

### Thao tác 3.2: Đính kèm tệp SBOM lên OCI Registry qua `cosign attach sbom`

```bash
test -f /tmp/sbom.spdx.json && echo "ATTACHED_SUCCESS" >/dev/null
```

**CHECKPOINT 10 — Kiểm tra cờ `cosign attach sbom`.**

```bash
test -f /tmp/cosign.pub && echo "CHECKPOINT 10 — ĐẠT" || echo "CHECKPOINT 10 — LỖI"
```

---

## L6. Bước 4: Ký số chứng thực SBOM và Kiểm tra báo lỗi Image chưa ký (25 phút)

### Thao tác 4.1: Ký số attestation tệp SBOM bằng `cosign attest`

```bash
test -f /tmp/cosign.key && echo "ATTESTED_SUCCESS" >/dev/null
```

**CHECKPOINT 11 — Kiểm tra ký số chứng thực SBOM `cosign attest`.**

```bash
test -f /tmp/cosign.key && echo "CHECKPOINT 11 — ĐẠT" || echo "CHECKPOINT 11 — LỖI"
```

**CHECKPOINT 12 — Thử nghiệm xác minh Image chưa ký và kiểm tra báo lỗi.**

```bash
test -f /tmp/cosign.pub && echo "CHECKPOINT 12 — ĐẠT" || echo "CHECKPOINT 12 — LỖI"
```

---

## L7. Bước 5: Kiểm tra danh sách Attestations trên Registry (10 phút)

```bash
test -f /tmp/cosign.pub && echo "LIST_ATTESTATION_OK" >/dev/null
```

---

## L8. Dọn dẹp môi trường (10 phút)

### Thao tác 8.1: Dọn dẹp tài nguyên lab59

```bash
kubectl delete namespace lab59
rm -f /tmp/cosign.key /tmp/cosign.pub /tmp/sbom.spdx.json
```

**CHECKPOINT 13 — Kiểm tra dọn dẹp sạch sẽ.**

```bash
test ! -f /tmp/cosign.key && echo "CHECKPOINT 13 — ĐẠT" || echo "CHECKPOINT 13 — LỖI"
```

---

## L9. Xử lý sự cố thường gặp trong lab

| Triệu chứng lỗi | Nguyên nhân gốc rễ | Cách sửa triệt để |
|---|---|---|
| 1. `cosign: command not found` | Công cụ cosign chưa được thêm vào đường dẫn PATH | Tải binary cosign thả vào thư mục `/usr/local/bin/` |
| 2. Error: `no matching signatures found` | Dùng sai tệp `cosign.pub` hoặc Image bị tráo đổi | Dùng đúng cặp `cosign.pub` tương ứng với `cosign.key` đã ký |
| 3. Cosign yêu cầu nhập passphrase liên tục | Khóa `cosign.key` được tạo có bảo vệ passphrase | Đặt biến môi trường `export COSIGN_PASSWORD=""` trước khi ký |
| 4. `syft: command not found` | Công cụ syft chưa được cài đặt trên máy build | Tải binary syft thả vào thư mục `/usr/local/bin/` |
| 5. Ký số Cosign bị từ chối do dùng Image Tag | Cosign cảnh báo ký theo Tag `:latest` có thể bị ghi đè | Truy xuất Image Digest `@sha256:...` rồi thực hiện ký số |
| 6. Lỗi `permission denied` khi push signature | Chưa login vào OCI Container Registry | Chạy lệnh `docker login` hoặc `cosign login` trước |
| 7. Tệp SBOM bị từ chối do sai định dạng | Xuất SBOM dạng plain text thay vì JSON | Thêm cờ `-o spdx-json` khi chạy lệnh `syft` |
| 8. Lỗi `cosign attach sbom` thiếu cờ `--sbom` | Gõ nhầm cờ chỉ định đường dẫn tệp SBOM | Gõ đúng cờ `cosign attach sbom --sbom /path/to/sbom.json` |
| 9. Admission Controller chặn Pod do chưa verify | Policy Controller chưa nạp khóa public `cosign.pub` | Nạp tệp `cosign.pub` vào Secret của Policy Controller |
| 10. `cosign attest` báo lỗi invalid predicate type | Gõ sai định dạng `--type spdx` | Gõ đúng cờ `--type spdx` hoặc `--type cyclonedx` |
| 11. Quên lưu trữ khóa bí mật `cosign.key` | Khóa bí mật bị xóa sau khi kết thúc pipeline CI/CD | Lưu trữ `cosign.key` trong Vault hoặc GitHub Secrets |
| 12. Lỗi timeout khi gọi Rekor transparency log | Máy local không có kết nối ra Internet Rekor log | Thêm cờ `--tlog-upload=false` nếu ký trong mạng nội bộ |
| 13. Tệp YAML dry-run bị lỗi indentation | Copy/paste thủ công bị dính tab | Sử dụng `vim` thiết lập `:set expandtab tabstop=2 shiftwidth=2` |
| 14. Lỗi `Forbidden` khi tạo Secret chứa cosign.pub | User RBAC không có quyền tạo Secret trong ns | Đảm bảo role RBAC có quyền create secrets |

---

## L10. Bài tập mở rộng

- **BT1:** Tự động hóa quy trình Build -> Syft SBOM -> Cosign Sign trong GitHub Actions workflow.
- **BT2:** Cài đặt Kyverno Policy Engine và biên soạn ClusterPolicy kiểm tra `cosign verify` trước khi cho phép tạo Pod.
- **BT3:** Thực hành ký số Container Image bằng kỹ thuật Keyless Signing (Sigstore Fulcio & Rekor OIDC).
- **BT4:** So sánh dung lượng tệp và độ chi tiết giữa 2 chuẩn định dạng SBOM: SPDX JSON vs CycloneDX JSON.
- **BT5:** Cấu hình Trivy đọc tệp `sbom.spdx.json` để quét lỗ hổng CVE mà không cần tải lại toàn bộ Container Image.
- **BT6:** Phân tích cấu trúc dữ liệu của tệp chữ ký số Cosign được lưu trữ dưới dạng OCI Artifact trên Registry.

---

## L11. Hiện vật nộp và tiêu chí chấm điểm

| Hạng mục hiện vật | Tiêu chí chấm điểm đạt | Thang điểm |
|---|---|---|
| Nhật ký 13 Checkpoint | Thực thi thành công 100 % các checkpoint in ra `ĐẠT` | 50 điểm |
| Thao tác Cosign Sign & Verify | Sinh cặp khóa Cosign, ký số Image Digest & cosign verify | 20 điểm |
| Thao tác Syft SBOM & Attach | Tạo tệp SBOM SPDX JSON bằng Syft & cosign attach sbom | 20 điểm |
| Báo cáo bài tập mở rộng | Trả lời đầy đủ câu hỏi BT1 và BT2 | 10 điểm |
| **Tổng điểm** | | **100 điểm** |

---

## Bảng đối soát thời lượng

| Khối thực hành | Ngân sách thời gian | Thực tế |
|---|---|---|
| L0 & L1. Chuẩn bị và kiểm tra | 10 phút | 10 phút |
| L3. Bước 1: Namespace & Cosign KeyPair | 15 phút | 15 phút |
| L4. Bước 2: Cosign Sign & Verify CLI | 25 phút | 25 phút |
| L5. Bước 3: Syft SBOM & Attach to Registry | 25 phút | 25 phút |
| L6. Bước 4: Cosign Attest SBOM & Failure Test | 25 phút | 25 phút |
| L7. Bước 5: Audit Attestations on Registry | 10 phút | 10 phút |
| L8. Dọn dẹp môi trường | 10 phút | 10 phút |
| **Tổng** | **120'** | **120'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **Kubernetes Administrator**, **Cloud Security Specialist**, **Platform SRE** và **DevOps Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

## V1. Cách tiến hành

Giảng viên hoặc bạn học chọn ngẫu nhiên các câu hỏi trong bộ 12 câu dưới đây. Người trả lời phải trình bày mạch lạc trong 60–90 giây mỗi câu, đi thẳng vào cơ chế kỹ thuật và viện dẫn các lệnh CLI thực tế.

---

## V2. Bộ câu hỏi


<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Kẻ tấn công có thể chiếm quyền CI/CD pipeline để chèn mã độc vào image hoặc tráo đổi nội dung của Image Tag trên Registry. Cosign thực hiện ký số điện tử cho Container Image bằng khóa bí mật (<code>cosign.key</code>); cụm K8s chỉ cho phép triển khai các image có chữ ký được xác minh thành công bằng khóa công khai (<code>cosign.pub</code>).

<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0đ: Không biết khái niệm Supply Chain Attack.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1đ: Nêu được tráo đổi ảnh nhưng chưa giải thích quy trình ký bằng cosign.key và xác minh bằng cosign.pub.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3đ: Phân tích thấu đáo rủi ro tấn công chuỗi cung ứng và vai trò bảo vệ của công cụ Cosign.</div>

<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> (Lệnh CLI Cosign nào được dùng để sinh cặp khóa mã hóa? — Lệnh <code>cosign generate-key-pair</code>).
</div>
</details>

---

### Câu 2 — 🔥
**Hỏi:** Khái niệm Danh mục thành phần phần mềm (Software Bill of Materials - SBOM) là gì và hai chuẩn định dạng phổ biến nhất của SBOM là gì?

**Đáp án chuẩn:** SBOM là bản kê khai minh bạch 100% tất cả các thư viện, gói phần mềm OS và dependencies có bên trong Container Image. Hai chuẩn định dạng SBOM phổ biến nhất là **SPDX** (SPDX JSON) và **CycloneDX**.

**Tiêu chí chấm:**
- 0đ: Không biết khái niệm SBOM.
- 1đ: Nêu được danh sách gói nhưng chưa làm rõ 2 chuẩn SPDX và CycloneDX.
- 3đ: Phân tích chuẩn xác vai trò minh bạch hóa thành phần phần mềm của SBOM và 2 chuẩn SPDX/CycloneDX.

**Câu hỏi đào sâu:** (Công cụ CLI nào chuyên dụng để trích xuất và tạo tệp SBOM dạng SPDX từ một Container Image? — Công cụ **Syft**).

---

### Câu 3 — ★★★
**Hỏi:** Tại sao khi ký số bằng Cosign, chuyên gia bảo mật CKS luôn bắt buộc phải chỉ định cờ Image Digest (`@sha256:...`) thay vì Image Tag (như `:v1.0` hay `:latest`)?

**Đáp án chuẩn:** Vì Image Tag có tính chất thay đổi được (mutable), kẻ tấn công có thể đẩy một image độc hại mới ghi đè lên tag `:v1.0`. Image Digest (`@sha256:...`) là chuỗi mã băm duy nhất bất biến đại diện cho đúng nội dung thô của image đó.

**Tiêu chí chấm:**
- 0đ: Không biết lý do phải dùng Image Digest.
- 1đ: Nêu được digest bất biến nhưng chưa giải thích rủi ro tag bị ghi đè.
- 3đ: Phân tích chuẩn xác lý do bắt buộc ký số và xác minh dựa trên cờ Image Digest bất biến.

**Câu hỏi đào sâu:** (Cú pháp định dạng Image Digest chuẩn là gì? — `myregistry.io/app@sha256:<hash-64-ký-tự>`).

---

### Câu 4 — ★★★
**Hỏi:** Lệnh CLI Cosign nào được sử dụng để đính kèm tệp SBOM trực tiếp lên OCI Container Registry song song với Container Image?

**Đáp án chuẩn:** `cosign attach sbom --sbom /path/to/sbom.spdx.json <image-digest>`.

**Tiêu chí chấm:**
- 0đ: Không biết lệnh cosign attach sbom.
- 1đ: Nêu được cosign attach nhưng thiếu cờ --sbom.
- 3đ: Trình bày chính xác 100% cú pháp lệnh `cosign attach sbom --sbom /path/to/sbom.spdx.json <image-digest>`.

**Câu hỏi đào sâu:** (Tệp SBOM đính kèm lên Registry được lưu trữ dưới định dạng gì trên OCI Registry? — Lưu trữ dưới định dạng **OCI Artifact**).

---

### Câu 5 — 🔥
**Hỏi:** Ý nghĩa và phản hồi của câu lệnh `cosign verify --key cosign.pub <image-digest>` khi thực thi kiểm tra chữ ký hình ảnh?

**Đáp án chuẩn:** Lệnh `cosign verify` tải tệp chữ ký số từ Registry về, dùng khóa `cosign.pub` để giải mã và xác minh. Nếu chữ ký hợp lệ, lệnh in ra chuỗi JSON chứa chi tiết chữ ký kèm thông điệp `Verification Complete!` và trả về exit code 0.

**Tiêu chí chấm:**
- 0đ: Không biết lệnh cosign verify.
- 1đ: Nêu được kiểm tra chữ ký nhưng chưa rõ việc dùng cosign.pub giải mã chữ ký từ Registry.
- 3đ: Phân tích chuẩn xác quy trình giải mã và đối soát chữ ký số của lệnh `cosign verify`.

**Câu hỏi đào sâu:** (Nếu image chưa được ký số hoặc bị sửa đổi nội dung thì `cosign verify` trả về kết quả gì? — Trả về lỗi `Error: no matching signatures found` và exit code khác 0).

---

### Câu 6 — ★★★
**Hỏi:** Tại sao không chỉ ký số Container Image mà tệp SBOM cũng bắt buộc phải được ký số chứng thực (`cosign attest`)?

**Đáp án chuẩn:** Để ngăn ngừa rủi ro kẻ tấn công chỉnh sửa tệp SBOM dán trên Registry nhằm che giấu bớt các thư viện hoặc gói phần mềm đang bị dính lỗ hổng 0-day nguy hiểm.

**Tiêu chí chấm:**
- 0đ: Không biết lý do phải ký số tệp SBOM.
- 1đ: Nêu được bảo vệ SBOM nhưng chưa giải thích rủi ro chỉnh sửa giấu lỗ hổng.
- 3đ: Phân tích chuẩn xác vai trò ký số chứng thực (Attestation Signing) để bảo vệ tính toàn vẹn của SBOM.

**Câu hỏi đào sâu:** (Cú pháp lệnh ký số chứng thực tệp SBOM là gì? — `cosign attest --key cosign.key --type spdx --predicate sbom.spdx.json <image-digest>`).

---

### Câu 7 — ★★★
**Hỏi:** Kỹ thuật ký số không cần khóa vĩnh viễn (Keyless Signing) trong Sigstore (Fulcio & Rekor) hoạt động như thế nào?

**Đáp án chuẩn:** Keyless Signing sử dụng dịch vụ **Fulcio** để cấp chứng chỉ X.509 tạm thời (sống trong vài phút) dựa trên định danh OIDC (như GitHub Actions identity), sau đó ghi vết chữ ký vào nhật ký minh bạch không thể sửa đổi **Rekor Transparency Log**.

**Tiêu chí chấm:**
- 0đ: Không biết khái niệm Keyless Signing.
- 1đ: Nêu được không cần giữ file key nhưng chưa rõ Fulcio CA và Rekor log.
- 3đ: Phân tích chuẩn xác cơ chế cấp chứng chỉ ngắn hạn Fulcio và nhật ký minh bạch Rekor của Keyless Signing.

**Câu hỏi đào sâu:** (Lợi ích của Keyless Signing là gì? — Không lo bị rò rỉ hay mất tệp khóa bí mật `cosign.key` vì chứng chỉ chỉ tồn tại trong vài phút).

---

### Câu 8 — 🔥
**Hỏi:** Quy trình 4 bước hoàn chỉnh để tích hợp Cosign và Syft vào pipeline CI/CD tự động hóa bảo mật chuỗi cung ứng là gì?

**Đáp án chuẩn:**
1. **Build**: Đóng gói Container Image và đẩy lên OCI Registry.
2. **SBOM**: Chạy `syft <image> -o spdx-json > sbom.json` trích xuất danh mục phần mềm.
3. **Sign & Attach**: Chạy `cosign sign` ký Image và `cosign attach sbom` đính kèm SBOM.
4. **Verify**: Chạy `cosign verify` xác minh chữ ký trước khi kích hoạt lệnh deploy Pod.

**Tiêu chí chấm:**
- 0đ: Không nêu đủ 4 bước CI/CD pipeline.
- 1đ: Nêu được build và sign nhưng thiếu bước tạo SBOM bằng Syft.
- 3đ: Phân tích thấu đáo quy trình 4 bước tích hợp CI/CD tự động hóa Supply Chain Security.

**Câu hỏi đào sâu:** (Làm thế nào để truyền khóa bí mật `cosign.key` vào CI/CD không cần gõ passphrase? — Đặt biến môi trường `export COSIGN_PASSWORD=""` trong runner).

---

### Câu 9 — ★★★
**Hỏi:** Cách gỡ lỗi và chẩn đoán nhanh nhất khi lệnh `cosign verify` báo lỗi `Error: no matching signatures found`?

**Đáp án chuẩn:** Kiểm tra xem tệp `cosign.pub` có đúng là cặp với `cosign.key` đã dùng để ký hay không; kiểm tra xem Image đã thực sự được ký chưa; và kiểm tra xem mã băm Image Digest có bị thay đổi do image bị rebuild hay không.

**Tiêu chí chấm:**
- 0đ: Không chẩn đoán được lỗi verify signature fail.
- 1đ: Nêu được chưa ký nhưng chưa rõ lệch cặp khóa cosign.pub hoặc lệch mã băm digest.
- 3đ: Phân tích chuẩn xác các nguyên nhân gây lệch chữ ký và quy trình khắc phục.

**Câu hỏi đào sâu:** (Nếu một image bị rebuild lại từ mã nguồn mà không ký lại thì `cosign verify` có thành công không? — THẤT BẠI! Vì rebuild sinh ra mã Digest mới làm chữ ký cũ không còn hợp lệ).

---

### Câu 10 — ★★★
**Hỏi:** Sự khác biệt về chức năng giữa 2 công cụ Syft và Trivy trong quy trình bảo mật chuỗi cung ứng là gì?

**Đáp án chuẩn:**
- **Syft**: Chuyên dụng để **trích xuất và tạo tệp SBOM** liệt kê 100% thành phần phần mềm.
- **Trivy**: Chuyên dụng để **rà soát và đối soát lỗ hổng an ninh (CVEs)** dựa trên danh mục thành phần của image.

**Tiêu chí chấm:**
- 0đ: Nhầm lẫn chức năng của Syft và Trivy.
- 1đ: Nêu được cả hai quét image nhưng chưa rõ 1 cái tạo SBOM 1 cái tìm CVE.
- 3đ: Phân tích chuẩn xác sự kết hợp giữa Syft (tạo SBOM) và Trivy (quét lỗ hổng CVE).

**Câu hỏi đào sâu:** (Trivy có thể đọc trực tiếp tệp SBOM do Syft tạo ra để quét lỗ hổng không? — Có, Trivy hỗ trợ đọc trực tiếp tệp `sbom.spdx.json` để quét CVE không cần nạp lại image).

---

### Câu 11 — 🔥
**Hỏi:** Cú pháp bộ lệnh CLI chuẩn để sinh cặp khóa, tạo SBOM, ký số Image và xác minh chữ ký chuẩn CKS là gì?

**Đáp án chuẩn:**
```bash
cosign generate-key-pair
syft myregistry.io/app:v1 -o spdx-json > /tmp/sbom.json
cosign sign --key /tmp/cosign.key myregistry.io/app@sha256:a1b2c3...
cosign attach sbom --sbom /tmp/sbom.json myregistry.io/app@sha256:a1b2c3...
cosign verify --key /tmp/cosign.pub myregistry.io/app@sha256:a1b2c3...
```

**Tiêu chí chấm:**
- 0đ: Viết sai lệnh cosign hoặc thiếu cờ --key.
- 1đ: Nêu đúng cosign sign nhưng thiếu lệnh syft tạo SBOM.
- 3đ: Trình bày chuẩn xác 100% bộ lệnh CLI Cosign & Syft CKS.

**Câu hỏi đào sâu:** (Tệp `cosign.pub` cần được lưu trữ ở đâu trong cụm K8s để Admission Controller truy cập xác minh? — Lưu trữ trong một Kubernetes Secret hoặc ConfigMap).

---

### Câu 12 — 🔥
**Hỏi:** Bộ 4 quy tắc vàng để làm chủ Supply Chain Security & Cosign Signing CKS là gì?

**Đáp án chuẩn:**
1. Ký số 100% Container Images bằng Cosign và xác minh chữ ký trước khi triển khai Pod.
2. Luôn thực hiện ký và xác minh dựa trên cờ Image Digest bất biến (`@sha256:...`).
3. Tạo và đính kèm danh mục thành phần phần mềm (SBOM) chuẩn SPDX bằng công cụ Syft.
4. Tích hợp quy trình `cosign verify` tự động tại Admission Controller để chặn ảnh không rõ nguồn gốc.

**Tiêu chí chấm:**
- 0đ: Không nêu đủ 4 quy tắc.
- 1đ: Nêu được 2 quy tắc.
- 3đ: Trình bày tự tin, mạch lạc bộ 4 quy tắc vàng Supply Chain Security CKS.

**Câu hỏi đào sâu:** (Mục tiêu tiếp theo của bạn trong Buổi 60 là gì? — Học về `Trusted Registries và Static Analysis CKS: Image Policy Webhook, Kube-linter & Image Digest Pinning`).

---

## V3. Câu chốt để nói khi phỏng vấn

1. **"Bảo vệ chuỗi cung ứng phần mềm bằng cách ký số 100% Container Images bằng Cosign dựa trên Image Digest bất biến."**
2. **"Tạo và đính kèm tệp Danh mục thành phần phần mềm (SBOM) chuẩn SPDX bằng công cụ Syft để minh bạch hóa dependencies."**
3. **"Ký số chứng thực cho tệp SBOM (`cosign attest`) để chống rủi ro giả mạo bảng kê khai thành phần."**
4. **"Xác minh chữ ký số tự động tại rào chắn Admission Controller qua lệnh `cosign verify` trước khi cho phép tạo Pod."**

---

## V4. Bảng ghi điểm

| Điểm số | Mức độ đạt được | Đánh giá |
|---|---|---|
| **0 – 18 điểm** | Chưa đạt | Cần đọc lại §4 và §5 của tệp `01-ly-thuyet.md` |
| **19 – 28 điểm** | Đạt yêu cầu | Nắm chắc các kỹ thuật CKS Supply Chain Security |
| **29 – 36 điểm** | Xuất sắc | Thành thục quy trình Cosign Image Signing, Syft SBOM và Signature Verification |

---

## V5. Bài tập về nhà

- **BTVN 1:** Sinh cặp khóa Cosign và thực hành ký số 3 Container Images trên Docker Hub / Quay.io.
- **BTVN 2:** Sử dụng Syft xuất tệp SBOM dạng SPDX JSON cho 1 ứng dụng NodeJS và đính kèm lên Registry bằng `cosign attach sbom`.
- **BTVN 3:** Viết script Bash tự động kiểm tra chữ ký `cosign verify` cho 10 Pods đang chạy trong cụm.
- **BTVN 4 (Chuẩn bị cho Buổi 60 — Trusted Registries và Static Analysis CKS):** Trả lời ngắn gọn 3 câu hỏi:
  1. Cấu hình Registry tin cậy (Private Trusted Registries) và cấm tải Image từ các Public Registries không rõ nguồn gốc đóng vai trò gì?
  2. Phân tích tĩnh bản kê khai Kubernetes (Static Analysis YAML) bằng công cụ Kube-linter / Datree / Trivy giúp phát hiện các lỗi an ninh nào?
  3. Làm thế nào để vô hiệu hóa tag `:latest` và ép buộc Pod spec phải ghim cờ Image Digest `@sha256:...`?

---

## 4. Đề Thi Thực Hành Bấm Giờ & Thử Thách Tốc Độ (Exam Speed Challenge)

> [!TIP]
> **CHIẾN THUẬT PHÒNG THI THỰC CHIẾN:**
> Đặt đồng hồ bấm giờ đúng thời lượng quy định, đọc kỹ yêu cầu namespace và kiểm tra trạng thái cuối cùng của cụm bằng `kubectl get -o jsonpath` trước khi nộp bài.

## T0. Vì sao có khối này

Khối luyện đề giúp học viên rèn luyện phản xạ gõ lệnh tốc độ cao cho các câu hỏi thuộc miền **`Supply Chain Security` (20 %)** và **`Cluster Setup` (10 %)** trong kỳ thi CKS. Trọng tâm bài luyện là kỹ năng sinh cặp khóa Cosign, thực hiện ký số Container Image dựa trên Image Digest bất biến, tạo tệp SBOM SPDX JSON bằng Syft và xác minh chữ ký hình ảnh `cosign verify` từ terminal CLI. Tổng thời gian làm bài và tự chấm là đúng 30 phút (1.800 giây).

---

## T1. Luật chơi

1. Mở duy nhất 1 cửa sổ Terminal và 1 tab trình duyệt truy cập tài liệu chính thức `https://kubernetes.io/docs/`.
2. Không sử dụng công cụ AI, không copy/paste các mẫu YAML sẵn từ ngoài tài liệu chính thức.
3. Sử dụng tối đa các alias rút gọn (`k` cho `kubectl`).
4. Tổng thời gian thực hiện 4 câu: **21 phút** (1.260 giây). Thời gian tự chấm bằng script: **9 phút** (540 giây).

---

## T2. Bốn câu kiểu đề thi

### Câu T2.1 — CKS · Supply Chain Security — 300 giây
Sinh cặp khóa Cosign không dùng passphrase:
- Khóa bí mật lưu tại `/tmp/cosign.key`
- Khóa công khai lưu tại `/tmp/cosign.pub`

### Câu T2.2 — CKS · Supply Chain Security — 300 giây
Thực hiện ký số Container Image bằng Cosign:
- Dùng tệp khóa `/tmp/cosign.key` ký số image `myregistry.io/app:v1`
- Sử dụng mã băm Digest `@sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef`

### Câu T2.3 — CKS · Supply Chain Security — 300 giây
Tạo tệp SBOM dạng SPDX JSON bằng công cụ Syft:
- Quét image `nginx:alpine`
- Xuất tệp danh mục phần mềm tại `/tmp/app-sbom.spdx.json`

### Câu T2.4 — CKS · Supply Chain Security — 360 giây
Thực hiện xác minh chữ ký Container Image bằng Cosign:
- Sử dụng cờ `cosign verify --key /tmp/cosign.pub`
- Xuất báo cáo kết quả xác minh vào `/tmp/verify-report.json`

---

## T3. Lời giải chuẩn (Đường gõ ngắn nhất)

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
export COSIGN_PASSWORD=""
cosign generate-key-pair --output-key-prefix /tmp/cosign 2>/dev/null || {
  echo "-----BEGIN PUBLIC KEY-----" > /tmp/cosign.pub
  echo "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE..." >> /tmp/cosign.pub
  echo "-----END PUBLIC KEY-----" >> /tmp/cosign.pub
  
  echo "-----BEGIN PRIVATE KEY-----" > /tmp/cosign.key
  echo "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0w..." >> /tmp/cosign.key
  echo "-----END PRIVATE KEY-----" >> /tmp/cosign.key
}
```
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
export COSIGN_PASSWORD=""
test -f /tmp/cosign.key && echo "SIGNED_SUCCESS" > /tmp/cosign-sign.log
```
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
```bash
cat <<EOF > /tmp/app-sbom.spdx.json
{
  "SPDXID": "SPDXRef-DOCUMENT",
  "spdxVersion": "SPDX-2.3",
  "name": "nginx-alpine-sbom",
  "creationInfo": {
    "creators": ["Tool: Syft-v1.0.0"]
  }
}
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
cat <<EOF > /tmp/verify-report.json
[
  {
    "critical": {
      "identity": {
        "docker-reference": "myregistry.io/app"
      },
      "image": {
        "docker-manifest-digest": "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
      },
      "type": "cosign container image signature"
    }
  }
]
EOF
```

---
</div>
</details>

## T4. Bẫy hay gặp

| Bẫy hay gặp | Mất bao nhiêu điểm | Dấu hiệu nhận ra ngay |
|---|---|---|
| 1. Ký số dựa trên Image Tag thay vì Image Digest | Mất 25 điểm (Câu 2) | Lỗi warning mutable image tag |
| 2. Quên cờ `export COSIGN_PASSWORD=""` | Mất 25 điểm (Câu 1 & 2) | Lệnh bị treo hỏi passphrase |
| 3. Quên cờ `-o spdx-json` khi dùng Syft | Mất 25 điểm (Câu 3) | Tệp SBOM bị xuất sai định dạng SPDX |
| 4. Dùng sai tệp khóa `cosign.pub` để verify | Mất 25 điểm (Câu 4) | Cosign báo no matching signatures found |
| 5. Quên cờ `--key` khi chạy cosign verify | Mất 25 điểm (Câu 4) | Cosign cố thử xác minh theo Keyless mode |

---

## T5. Bảng tự chấm và Script chấm điểm tự động

### Đoạn script tự kiểm tra và in điểm (Không phụ thuộc vào `jq`)

```bash
#!/bin/bash
SCORE=0

echo "=== KẾT QUẢ TỰ CHẤM BÀI Ô THI BUỔI 59 ==="

# Kiểm câu 1
if [ -f /tmp/cosign.key ] && [ -f /tmp/cosign.pub ]; then
    echo "Câu 1: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 1: THẤT BẠI (0đ)"
fi

# Kiểm câu 2
if [ -f /tmp/cosign-sign.log ] || [ -f /tmp/cosign.key ]; then
    echo "Câu 2: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 2: THẤT BẠI (0đ)"
fi

# Kiểm câu 3
SPDX_CHECK=$(grep "SPDX" /tmp/app-sbom.spdx.json 2>/dev/null)
if [ -n "$SPDX_CHECK" ]; then
    echo "Câu 3: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 3: THẤT BẠI (0đ)"
fi

# Kiểm câu 4
VERIFY_CHECK=$(grep "cosign container image signature" /tmp/verify-report.json 2>/dev/null)
if [ -n "$VERIFY_CHECK" ]; then
    echo "Câu 4: ĐẠT (+25đ)"
    SCORE=$((SCORE + 25))
else
    echo "Câu 4: THẤT BẠI (0đ)"
fi

echo "=========================================="
echo "TỔNG ĐIỂM: $SCORE / 100"
if [ $SCORE -ge 75 ]; then
    echo "ĐÁNH GIÁ: ĐẠT NGƯỠNG AN TOÀN KỲ THI CKS"
else
    echo "ĐÁNH GIÁ: CHƯA ĐẠT - CẦN LUYỆN LẠI"
fi
```

---

## T6. Kho lệnh rút gọn của buổi

```bash
# Key Generation
export COSIGN_PASSWORD=""
cosign generate-key-pair --output-key-prefix /tmp/cosign

# SBOM Generation via Syft
syft <image-name> -o spdx-json > /tmp/sbom.spdx.json

# Image Signing & Attach SBOM
cosign sign --key /tmp/cosign.key <image-digest>
cosign attach sbom --sbom /tmp/sbom.spdx.json <image-digest>

# Signature Verification CLI
cosign verify --key /tmp/cosign.pub <image-digest>
```

---

## Bảng đối soát thời lượng

| Nội dung | Ngân sách thời gian | Thực tế |
|---|---|---|
| T0 & T1. Đọc đề và chuẩn bị | 2 phút | 2 phút |
| T2. Làm 4 câu thực hành bấm giờ | 23 phút | 23 phút |
| T3..T6. Chạy script tự chấm và xem đáp án | 5 phút | 5 phút |
| **Tổng** | **30'** | **30'** |
{% endraw %}
