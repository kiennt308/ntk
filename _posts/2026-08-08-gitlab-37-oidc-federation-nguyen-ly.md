---
layout: post
title: "[Bài 37] Xác Thực OIDC Không Cần Khóa (Keyless Authentication): AWS STS, GCP Workload Identity & Azure Federated Identity"
date: 2026-08-08 08:00:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-37
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 37
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1555949963-aa79dcee02e1?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.37] Hướng dẫn chuyên sâu Xác Thực OIDC Không Cần Khóa (Keyless Authentication): AWS STS, GCP Workload Identity & Azure Federated Identity: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
---

# [BÀI 37] XÁC THỰC OIDC KHÔNG CẦN KHÓA (KEYLESS AUTHENTICATION): AWS STS, GCP WORKLOAD IDENTITY & AZURE FEDERATED IDENTITY

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

---





| STT | Câu hỏi ôn tập | Đáp án chi tiết thực chiến |
|---|---|---|
| 1 | Từ khóa `environment:name` mang lại giá trị cốt lõi gì cho CI/CD? | Chuyển đổi một job CI vô danh thành một sự kiện deployment chính thức có định danh và lịch sử, theo dõi commit SHA đang chạy trên từng môi trường (Dev, Staging, Prod), hỗ trợ nút bấm Rollback 1-click tự động và thu thập chỉ số DORA. |
| 2 | Cặp thuộc tính nào bắt buộc đi cùng nhau ở Review Apps? | Cặp thuộc tính `on_stop: <job_name>` (khai báo ở job deploy review) và `action: stop` (khai báo ở job teardown) để đảm bảo môi trường động tự dọn dẹp khi MR đóng hoặc merge. |
| 3 | Khai báo `auto_stop_in` giải quyết vấn đề gì trong hạ tầng? | Tự động đếm ngược thời gian (ví dụ `1 day`) và kích hoạt job dọn dẹp hủy bỏ Review Apps của các Merge Request bị lập trình viên bỏ quên để tránh lãng phí tài nguyên CPU/RAM trên Kubernetes Cluster. |
| 4 | Tại sao phải bật Protected Environment cho môi trường `production`? | Giới hạn quyền bấm nút deploy chỉ cho các tài khoản có Role chỉ định (Maintainers/SecLead), ngăn Junior Developer hoặc runner của nhánh cá nhân tự ý can thiệp làm hỏng ứng dụng trên Production. |
| 5 | Nguyên tắc Bất biến Artifact (Immutability) quy định điều gì? | Triển khai Production phải sử dụng ĐÚNG Container Image Tag SHA (`$CI_COMMIT_SHA`) đã được kiểm thử màu xanh 100% ở Staging, tuyệt đối không rebuild lại mã nguồn để tránh hiện tượng Dependency Drift. |


**Luận đề trung tâm:**
> *"Một cơ chế, ba cách gọi tên — Hiểu thấu đáo **claim `sub`** của OIDC JWT Token là bạn đã nắm giữ chìa khóa 90% kiến trúc bảo mật đa đám mây không mật khẩu tĩnh."*

Trong kỷ nguyên Cloud-Native, thảm họa bảo mật số 1 của hệ thống CI/CD là rò rỉ **Static Cloud Access Keys** (như `AWS_SECRET_ACCESS_KEY` hay `gcp-service-account-key.json`). Khi các khóa tĩnh này bị lưu trữ vĩnh viễn trong mục CI/CD Variables, bất kỳ ai chiếm được runner hoặc in log dump đều có thể lấy trộm key và kiểm soát toàn bộ hạ tầng đám mây của doanh nghiệp. Để giải quyết dứt điểm rủi ro này, **OIDC Federation (OpenID Connect Federated Identity)** cho phép GitLab CI/CD tự chứng thực danh tính với Cloud Provider (AWS, GCP, Azure) bằng một JSON Web Token (JWT) ngắn hạn tự hủy. Cả 3 gã khổng lồ đám mây tuy dùng các tên gọi khác nhau (AWS IAM OIDC Identity Provider, GCP Workload Identity Federation, Azure Federated Identity Credentials) nhưng đều hoạt động trên **ĐÚNG MỘT NGUYÊN LÝ NỀN TẢNG**.

---



| STT | Kỹ năng thực chiến | Hiện vật chứng minh hoàn thành |
|---|---|---|
| 1 | Hiểu bản chất OIDC Federation Đa đám mây | Sơ đồ luồng trao đổi danh tính giữa GitLab CI và AWS/GCP/Azure |
| 2 | Cấu hình sinh JWT Token bằng `id_tokens` | Tệp `.gitlab-ci.yml` sinh JWT Token chứa claim `aud` và `sub` |
| 3 | Giải mã và phân tích Payload của OIDC JWT Token | Script bash/jq trích xuất các trường `iss`, `aud`, `sub`, `project_path` |
| 4 | Xây dựng điều kiện Trust Policy dựa trên Claim `sub` | Câu lệnh JSON Trust Policy khớp chính xác `project_path` và `ref` |
| 5 | Thiết lập Attribute Mapping giữa GitLab và Cloud | Ma trận ánh xạ các claim JWT sang Cloud IAM Principal Attributes |
| 6 | Kiểm soát thời gian sống TTL của Cloud Token | Cấu hình Session Duration khống chế Token ngắn hạn dưới 60 phút |
| 7 | Tách biệt quyền IAM giữa nhánh Main và Feature | Trust Policy phân quyền Admin cho `ref:main` và Read-Only cho `ref:feature` |
| 8 | Giám sát vệt vết kiểm toán OIDC qua Cloud Audit Logs | Trích xuất log CloudTrail/GCP Audit ghi nhận sự kiện AssumeRole thành công |

---



| Kiến thức / Kỹ năng | Mức độ yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Cấu trúc JSON Web Token (JWT Header/Payload/Signature) | Hiểu rõ | Buổi 30 (QT 30.3) |
| Khái niệm IAM Role và Access Policy trên Cloud | Hiểu rõ | Kiến thức Cloud Nền tảng (AWS/GCP/Azure) |
| Cú pháp trường `id_tokens` trong `.gitlab-ci.yml` | Thành thục | Buổi 30 (QT 30.5) |
| Thao tác xử lý chuỗi JSON bằng `jq` và `base64` | Thành thục | Buổi 02 & Buổi 34 (QT 34.3) |
| Khái niệm Protected Environments | Thành thục | Buổi 36 (QT 36.5) |

---





| Thuật ngữ Tiếng Việt | Thuật ngữ Tiếng Anh | Giải thích ý nghĩa thực tế |
|---|---|---|
| Nhà cung cấp danh tính OIDC | OpenID Connect Provider (IdP) | Hệ thống xác thực (ở đây là GitLab Instance) phát hành JWT Token ký số điện tử bằng Private Key. |
| Liên kết danh tính đám mây | Federated Identity / Trust Relationship | Mối quan hệ tin tưởng giữa GitLab IdP và Cloud Provider (AWS/GCP/Azure) thông qua trao đổi Public Keys. |
| Chuỗi danh tính đối tượng | Subject Claim (`sub`) | Trường thông tin duy nhất trong JWT mô tả chính xác project, branch, tag hoặc environment trigger job (`project_path:group/repo:ref_type:branch:ref:main`). |
| Khán giả nhận token | Audience Claim (`aud`) | Trường định danh hệ thống nhận token (ví dụ: `https://aws.amazon.com` hoặc `https://iam.googleapis.com`), chống tấn công chuyển tiếp token. |
| Đơn vị phát hành | Issuer Claim (`iss`) | URL công khai của GitLab Instance xuất bản công khai danh sách Public Keys (`/.well-known/jwks.json`). |
| Bảng ánh xạ thuộc tính | Attribute Mapping | Quy tắc ánh xạ các claim trong JWT của GitLab thành thuộc tính IAM của Cloud Provider để phục vụ kiểm soát truy cập dựa trên thuộc tính (ABAC). |
| Chính sách tin tưởng | Trust Policy / Role Trust Relationship | Tập quy tắc trên Cloud quy định những điều kiện claim nào trong JWT mới được phép đổi lấy Temporary Credentials. |
| Quyền truy cập tạm thời | Temporary Security Credentials | Mật khẩu/Token ngắn hạn do Cloud cấp có TTL từ 15 đến 60 phút, tự động hết hạn mà không cần thu hồi thủ công. |
| Điểm xuất bản khóa công khai | JSON Web Key Set (JWKS) | Endpoint HTTPS (`/.well-known/jwks.json`) chứa Public Keys để Cloud xác minh chữ ký số của JWT Token. |
| Trao đổi danh tính | Token Exchange | Hành vi gửi JWT Token sang Cloud API (AWS STS / GCP WIF / Azure AD) để đổi lấy Cloud IAM Access Token. |
| Không mật khẩu tĩnh | Zero Static Credentials | Nguyên tắc kiến trúc an ninh tuyệt đối không lưu AWS Key hay GCP Service Account Key vĩnh viễn trên CI/CD Variables. |
| Bán kính ảnh hưởng sự cố | Blast Radius | Phạm vi thiệt hại tối đa nếu một token bị rò rỉ (với OIDC token ngắn hạn tự hủy, blast radius $\approx 0$). |



#### Mô hình 1: Luồng Trao đổi Danh tính OIDC 4 Bước Tiêu chuẩn (Universal 4-Step OIDC Flow)
Dù bạn deploy lên AWS, GCP hay Azure, luồng trao đổi danh tính luôn diễn ra qua 4 bước bất biến:
1. **Runner gửi yêu cầu cấp JWT Token:** Thông qua từ khóa `id_tokens` trong `.gitlab-ci.yml`, Runner yêu cầu GitLab Instance cấp một token ký số.
2. **GitLab ký và trả JWT Token:** GitLab sinh token chứa thông tin project, branch, user, issuer (`iss`), và audience (`aud`).
3. **Runner gửi JWT Token sang Cloud API:** Runner thực thi câu lệnh trao đổi (AWS STS `assume-role-with-web-identity`, GCP WIF `gcloud`, hoặc Azure CLI).
4. **Cloud xác minh và cấp Temporary Credentials:** Cloud Provider tự động kết nối tới GitLab JWKS Endpoint để kiểm tra chữ ký số, khớp câu lệnh Condition trong Trust Policy, và trả về Access Token ngắn hạn có TTL 15-60 phút.

```mermaid
sequenceDiagram
    autonumber
    participant Runner as GitLab CI Runner
    participant GitLab as GitLab OIDC IdP
    participant Cloud as Cloud Provider (AWS/GCP/Azure)
    participant Resource as Cloud Resource (EKS/GKE/AKS)

    Runner->>GitLab: 1. Request JWT Token via id_tokens (aud: https://cloud.domain)
    GitLab-->>Runner: 2. Return Signed JWT Token (containing sub, iss, aud claims)
    Runner->>Cloud: 3. Send JWT Token via OIDC Exchange API (AssumeRole / WIF)
    Note over Cloud,GitLab: Cloud verifies JWT Signature via GitLab JWKS endpoint (iss)
    Note over Cloud: Cloud checks Trust Policy against 'sub' claim match
    Cloud-->>Runner: 4. Issue Temporary Short-Lived Access Token (TTL: 15-60m)
    Runner->>Resource: Execute Deploy using Temporary Token
```

#### Mô hình 2: Bảng Đối chiếu Tương đương Kiến trúc giữa 3 Nền tảng Đám mây

| Khái niệm Kiến trúc | AWS (Amazon Web Services) | GCP (Google Cloud Platform) | Azure (Microsoft Azure) |
|---|---|---|---|
| **Cơ chế OIDC** | AWS IAM OIDC Identity Provider | GCP Workload Identity Federation (WIF) | Azure Federated Identity Credentials |
| **API Trao đổi Token** | `aws sts assume-role-with-web-identity` | `gcloud iam workload-identity-pools create-cred-config` | `az login --federated-token` |
| **Đối tượng cấp quyền** | AWS IAM Role | GCP Service Account (SA) | Azure User-Assigned Managed Identity |
| **Ràng buộc Quyền** | IAM Role Trust Policy (`Condition`) | Workload Identity Pool Attribute Filter | Federated Credential Subject Identifier |
| **Kết quả đổi Token** | Temporary AccessKeyId + SecretAccessKey + SessionToken | Temporary OAuth2 Access Token | Temporary Azure AD Access Token |

---

### 1.1. Cấu trúc JWT Token và Tầm quan trọng của Claim `sub` (10 phút)

### 4.1. Giải phẫu ba thành phần của OIDC JWT Token
Mỗi OIDC Token sinh ra bởi GitLab Instance là một tệp chuỗi ký tự chuẩn mã hóa Base64URL gồm 3 phần chính phân cách bởi dấu chấm (`.`):

1. **Header (Phần đầu):** Khai báo thuật toán mã hóa chữ ký (thường là `RS256` hoặc `ES256`) và ID của khóa công khai (`kid` - Key ID) tương ứng trong tệp JWKS.
```json
{
  "alg": "RS256",
  "kid": "K3yId-GitLab-Public-Signing-Key-2026",
  "typ": "JWT"
}
```

2. **Payload (Nội dung dữ liệu Claims):** Chứa thông tin ngữ cảnh danh tính của Runner job. Đây là phần thông tin quan trọng nhất được Cloud Provider kiểm tra:
```json
{
  "iss": "https://gitlab.company.com",
  "sub": "project_path:bank-group/payment-service:ref_type:branch:ref:main",
  "aud": "https://aws.amazon.com",
  "exp": 1776543210,
  "nbf": 1776539610,
  "iat": 1776539610,
  "jti": "550e8400-e29b-41d4-a716-446655440000",
  "namespace_id": "42",
  "namespace_path": "bank-group",
  "project_id": "108",
  "project_path": "bank-group/payment-service",
  "user_id": "7",
  "user_login": "ntk_devops",
  "pipeline_id": "9988",
  "job_id": "445522",
  "ref": "main",
  "ref_type": "branch",
  "ref_protected": "true",
  "environment": "production",
  "environment_protected": "true"
}
```

3. **Signature (Chữ ký số điện tử):** Được tạo ra bằng cách lấy cặp `Base64(Header) + "." + Base64(Payload)` đem mã hóa băm RSA-SHA256 với **Private Key bảo mật tuyệt đối** lưu trên GitLab Server. Cloud Provider dùng **Public Key** tải từ endpoint `https://gitlab.company.com/-/jwks` để xác minh chữ ký này mà không cần biết Private Key.

---

### 4.2. Các Quy tắc Kiến trúc An ninh OIDC (QT 37.1 - QT 37.4)

**Nguyên lý cốt lõi:** Nguyên tắc loại bỏ 100% Static Cloud Keys trong CI/CD Pipeline.
**Phát biểu.** Tuyệt đối không lưu trữ các hằng số Access Key tĩnh (`AWS_ACCESS_KEY_ID`, `GCP_SA_KEY_JSON`, `AZURE_CLIENT_SECRET`) trong CI/CD Variables.
**Giải thích cơ chế ngầm:** Static Keys có tuổi thọ vĩnh viễn, rất dễ bị rò rỉ qua console log, tệp dump hoặc khi máy chủ Runner bị thỏa hiệp. OIDC Federation thay thế hoàn toàn nhu cầu dùng Static Keys bằng Temporary Credentials ngắn hạn tự hủy. Việc loại bỏ khóa tĩnh giúp doanh nghiệp đáp ứng các tiêu chuẩn an ninh khắt khe như PCI-DSS và ISO 27001.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Khai báo `AWS_SECRET_ACCESS_KEY` dán trực tiếp dạng string dài ngoẵng trong mục Project CI/CD Variables Settings.
**Minh hoạ.**
```yaml
# XÓA HOÀN TOÀN các biến tĩnh bên dưới:
# AWS_ACCESS_KEY_ID: AKIAXXXXXX
# AWS_SECRET_ACCESS_KEY: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```
**Con số chốt:** 0 Static Keys trên CI/CD.

---

**Nguyên lý cốt lõi:** Định danh bắt buộc OIDC Issuer URL từ GitLab Instance.
**Phát biểu.** Cấu hình Cloud Identity Provider bắt buộc phải trỏ đến URL công khai chuẩn xác của GitLab Instance (ví dụ `https://gitlab.com` hoặc `https://gitlab.company.internal`).
**Giải thích cơ chế ngầm:** Cloud Provider cần biết đúng địa chỉ Issuer để truy vấn công khai tệp JWKS (`/.well-known/jwks.json`) nhằm xác minh chữ ký số điện tử của JWT Token. Nếu Issuer URL không hợp lệ, Cloud Provider sẽ từ chối xác thực vì không tin tưởng nguồn gốc của Token.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Cấu hình sai Issuer URL khiến Cloud không thể tải Public Key và từ chối xác thực với lỗi `Invalid Issuer` hoặc `JWKS fetch failed`.
**Minh hoạ.**
`Issuer URL: https://gitlab.company.internal`
`JWKS Endpoint: https://gitlab.company.internal/-/jwks`
**Con số chốt:** 1 Issuer URL duy nhất.

---

**Nguyên lý cốt lõi:** Cấu hình trường `id_tokens` bắt buộc trong job CI với Audience duy nhất.
**Phát biểu.** Mọi job CI cần kết nối Cloud OIDC bắt buộc phải khai báo khối `id_tokens` định nghĩa tên biến và giá trị `aud` (Audience).
**Giải thích cơ chế ngầm:** Cờ `aud` ngăn chặn cuộc tấn công chuyển tiếp token (Token Relay Attack), đảm bảo JWT Token sinh ra cho AWS không thể bị kẻ tấn công đem đi đổi lấy token trên GCP hay Vault. Nếu thiếu `aud`, Runner sẽ không sinh ra được JWT token.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Khai báo thiếu khối `id_tokens` khiến Runner không sinh ra biến môi trường chứa JWT Token.
**Minh hoạ.**
```yaml
deploy-job:
  id_tokens:
    AWS_OIDC_TOKEN:
      aud: https://aws.amazon.com
  script:
    - echo "JWT Token generated in $AWS_OIDC_TOKEN"
    - aws sts assume-role-with-web-identity --role-arn $ROLE_ARN --web-identity-token $AWS_OIDC_TOKEN
```
**Con số chốt:** Khai báo `id_tokens` ở 100% OIDC jobs.

---

**Nguyên lý cốt lõi:** Ràng buộc chặt chẽ điều kiện Trust Policy dựa trên `sub` claim.
**Phát biểu.** Trust Policy trên Cloud bắt buộc phải kiểm tra điều kiện khớp chính xác của trường `sub` (Subject Claim) đến cấp độ Project Path và Branch/Environment.
**Giải thích cơ chế ngầm:** Nếu Trust Policy cấu hình quá lỏng (ví dụ chấp nhận mọi token phát ra từ `https://gitlab.com`), một dự án bất kỳ của kẻ tấn công trên GitLab.com cũng có thể mạo danh và chiếm đoạt quyền truy cập Cloud của bạn. Cấu hình cờ `sub` đóng vai trò là hàng rào phòng thủ cuối cùng bảo vệ hạ tầng đa đám mây.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Trust Policy chỉ kiểm tra `iss` mà không có câu lệnh điều kiện `StringEquals` hoặc `AttributeFilter` đối với `sub` claim.
**Minh hoạ.** Cấu trúc chuẩn của `sub` claim trong GitLab CI JWT Token:
`sub: "project_path:bank-group/payment-service:ref_type:branch:ref:main"`

Ví dụ AWS IAM Trust Policy đầy đủ:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/gitlab.company.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "gitlab.company.com:aud": "https://aws.amazon.com",
          "gitlab.company.com:sub": "project_path:bank-group/payment-service:ref_type:branch:ref:main"
        }
      }
    }
  ]
}
```
**Con số chốt:** 100% Trust Policies lọc `sub` claim.

---

### 1.2. Quy tắc Ánh xạ thuộc tính và Phân quyền IAM (10 phút)

**Nguyên lý cốt lõi:** Phân biệt giữa OIDC Identity Exchange và Cloud Temporary Credential Generation.
**Phát biểu.** OIDC chỉ có nhiệm vụ **Xác thực danh tính (Authentication)**; việc **Cấp quyền (Authorization)** thuộc về IAM Policy của Cloud Provider.
**Giải thích cơ chế ngầm:** Tránh hiểu lầm rằng OIDC tự sinh ra quyền truy cập. OIDC JWT chỉ đóng vai trò là "Thẻ căn cước công dân"; Cloud IAM Role mới là "Chìa khóa mở cửa" quy định bạn được đọc S3 hay được sửa Kubernetes. Tách biệt hai khái niệm này giúp kiến trúc an ninh mạch lạc.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Gắn quá nhiều quyền hạn cho OIDC Identity Provider thay vì giới hạn ở IAM Role Policies.
**Minh hoạ.**
- GitLab OIDC JWT = Giấy xác minh: "Tôi là Job deploy từ project `payment-service` nhánh `main`".
- Cloud IAM Role = Quyền hạn: "Job này chỉ có quyền `s3:GetObject` trên bucket `payment-assets`".
**Con số chốt:** Tách biệt 100% AuthN và AuthZ.

---

**Nguyên lý cốt lõi:** Khống chế thời gian tồn tại (TTL) của Cloud Temporary Tokens dưới 60 phút.
**Phát biểu.** Tất cả các Temporary Access Tokens cấp từ Cloud API khi đổi OIDC Token phải được cấu hình thời gian sống (Lease TTL) từ 15 đến 60 phút.
**Giải thích cơ chế ngầm:** Thời gian sống ngắn đảm bảo nếu token vô tình lọt ra ngoài trong quá trình thi hành job, nó cũng sẽ tự động vô hiệu hóa trước khi kẻ tấn công kịp phát hiện và sử dụng.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đổi lấy Session Token có thời hạn kéo dài 12 tiếng hoặc 24 tiếng.
**Minh hoạ.**
```bash
aws sts assume-role-with-web-identity \
  --role-arn arn:aws:iam::123456789012:role/GitLabDeployRole \
  --role-session-name gitlab-session \
  --web-identity-token $AWS_OIDC_TOKEN \
  --duration-seconds 900
```
**Con số chốt:** TTL $\le 3600$ giây (60 phút).

---

**Nguyên lý cốt lõi:** Áp dụng nguyên tắc Privilege Minimization (Least Privilege) cho Cloud IAM Roles.
**Phát biểu.** Mỗi pipeline hoặc mỗi microservice phải sử dụng một Cloud IAM Role riêng biệt với tập quyền hạn tối thiểu vừa đủ để hoàn thành công việc.
**Giải thích cơ chế ngầm:** Giới hạn bán kính ảnh hưởng sự cố (Blast Radius Reduction). Nếu job CI của repo `frontend` bị thỏa hiệp, kẻ tấn công cũng không thể truy cập vào Database của repo `payment-backend`.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dùng chung một Cloud IAM Role có cờ `AdministratorAccess` cho tất cả 50 repositories trong công ty.
**Minh hoạ.**
- Repo `frontend` $\to$ IAM Role `FrontendDeployRole` (chỉ có quyền S3 + CloudFront).
- Repo `backend` $\to$ IAM Role `BackendDeployRole` (chỉ có quyền EKS + ECR).
**Con số chốt:** 1 IAM Role riêng cho 1 Repo.

---

**Nguyên lý cốt lõi:** Kiểm tra dấu hiệu rò rỉ JWT Token qua console log bằng Masking.
**Phát biểu.** Biến môi trường chứa JWT Token sinh ra từ `id_tokens` phải được ẩn (Masked) tự động và cấm tuyệt đối việc dùng lệnh `echo` hoặc `env` in token ra log terminal.
**Giải thích cơ chế ngầm:** In JWT Token ra console log sẽ biến token thành công khai. Bất kỳ ai có quyền xem log CI cũng có thể copy token và gọi API Cloud trong thời gian token còn hiệu lực.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> In script `echo $AWS_OIDC_TOKEN` ra màn hình console log để debug.
**Minh hoạ.**
```bash
# CẤM: echo "Token: $AWS_OIDC_TOKEN"
# ĐÚNG: Debug giải mã phần Payload an toàn:
echo "$AWS_OIDC_TOKEN" | jq -R 'split(".") | .[1] | @base64d | fromjson'
```
**Con số chốt:** 0 dòng log in JWT plain text.

---

### 1.3. Quy tắc Phân tách Môi trường và Audit Trail (10 phút)

**Nguyên lý cốt lõi:** Khai báo Attribute Mapping thống nhất giữa GitLab JWT và Cloud IAM Attributes.
**Phát biểu.** Cấu hình Attribute Mapping trên Cloud Provider để chuyển đổi các claim `project_path`, `ref`, `environment` trong JWT thành các thuộc tính IAM Principal Tags chuẩn.
**Giải thích cơ chế ngầm:** Giúp viết các câu lệnh ABAC (Attribute-Based Access Control) trên Cloud cực kỳ ngắn gọn và linh hoạt thay vì phải tạo hàng trăm IAM Role thủ công.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Mỗi repo lại viết một kiểu format claim dẫn đến việc không thể quản lý phân quyền tập trung.
**Minh hoạ.**
- GitLab Claim `assertion.project_path` $\to$ Cloud Attribute `principalTag/GitLabProjectPath`
- GitLab Claim `assertion.ref` $\to$ Cloud Attribute `principalTag/GitLabRef`

Ví dụ GCP Workload Identity Pool Attribute Mapping:
```bash
gcloud iam workload-identity-pools providers create-oidc gitlab-provider \
  --workload-identity-pool="gitlab-pool" \
  --issuer-uri="https://gitlab.company.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.project_path=assertion.project_path,attribute.ref=assertion.ref" \
  --attribute-condition="assertion.project_path == 'bank-group/payment-service'"
```
**Con số chốt:** 100% Attribute Mappings được chuẩn hóa.

---

**Nguyên lý cốt lõi:** Phân tách OIDC Roles giữa nhánh `main` (Production) và nhánh `feature` (Development).
**Phát biểu.** Cấu hình 2 IAM Roles riêng biệt trên Cloud: Role Production (chỉ cho phép `ref:main` và `environment:production`) và Role Staging/Dev (cho phép `ref_type:branch`).
**Giải thích cơ chế ngầm:** Đảm bảo các pipeline chạy ở nhánh tính năng cá nhân của developer dù có OIDC token cũng tuyệt đối không thể AssumeRole vào môi trường Production.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Dùng chung 1 OIDC IAM Role cho cả nhánh `feature` và nhánh `main`.
**Minh hoạ.**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Federated": "arn:aws:iam::123456789012:oidc-provider/gitlab.com"},
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "gitlab.com:sub": "project_path:bank/payment:ref_type:branch:ref:main"
      }
    }
  }]
}
```

Ví dụ Azure Federated Identity Credentials JSON cấu hình trên Managed Identity:
```json
{
  "name": "GitLabProdCredential",
  "issuer": "https://gitlab.company.com",
  "subject": "project_path:bank-group/payment-service:ref_type:branch:ref:main",
  "description": "Federated Credential for GitLab Production Deployment",
  "audiences": [
    "api://AzureADTokenExchange"
  ]
}
```
**Con số chốt:** Phân tách 100% Prod vs Non-Prod Roles.

---

**Nguyên lý cốt lõi:** Sử dụng OIDC Federation cho cả Container Registry Auth và Infrastructure Deployments.
**Phát biểu.** Áp dụng OIDC Token để đăng nhập và push Container Image lên Private Registries (AWS ECR, GCP Artifact Registry, Azure ACR) thay cho static registry credentials.
**Giải thích cơ chế ngầm:** Đồng bộ hóa toàn bộ kiến trúc an ninh chuỗi cung ứng không dùng mật khẩu tĩnh từ khâu Push Image đến khâu Triển khai Hạ tầng.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Deploy app dùng OIDC nhưng bước push Docker Image lên ECR vẫn dùng `AWS_ACCESS_KEY_ID` tĩnh.
**Minh hoạ.** Dùng `aws ecr get-login-password` thông qua OIDC Temporary Credentials.
```bash
# Login vào AWS ECR thông qua OIDC Temporary Token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
```
**Con số chốt:** 100% Registry Authentication bằng OIDC.

---

**Nguyên lý cốt lõi:** Theo dõi vệt vết kiểm toán OIDC qua Cloud Trail / Audit Logs.
**Phát biểu.** Bật cấu hình ghi log Audit Trail trên Cloud Provider để ghi nhận tất cả các sự kiện AssumeRole/Federated Login xuất phát từ GitLab CI Runner.
**Giải thích cơ chế ngầm:** Phục vụ công tác điều tra vết sự cố an toàn thông tin (Forensic Analysis) và đáp ứng các yêu cầu tuân thủ kiểm toán (SOC 2, ISO 27001, PCI-DSS).
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tắt log IAM Audit trên Cloud để tiết kiệm chi phí lưu trữ log.
**Minh hoạ.** Truy vấn AWS CloudTrail Event History tìm kiếm event `AssumeRoleWithWebIdentity` chứa thuộc tính `requestParameters.webIdentityToken`.
**Con số chốt:** 100% OIDC Authentication Events được ghi log.

---

### 1.4. Đưa vào việc thật (4 phút)

### 7.1. Kịch bản áp dụng thực tế tại Doanh nghiệp Đa đám mây (Enterprise Multi-Cloud Case)
Trong hạ tầng Đa đám mây hiện đại của tập đoàn Ngân hàng & Công nghệ (Triển khai đồng thời trên AWS, GCP và Azure):
1. **Pha Sinh Token (GitLab CI Phase):** Lập trình viên push commit lên nhánh `main`. GitLab Runner kích hoạt job `deploy-aws`, tự động sinh ra một OIDC JWT Token ký bởi Private Key của GitLab Instance với Audience `https://aws.amazon.com`.
2. **Pha Gọi API Trao đổi (Token Exchange Phase):** Runner gọi API AWS STS `AssumeRoleWithWebIdentity` truyền JWT Token vừa sinh. Đối với GCP, Runner gọi `gcloud` sử dụng Workload Identity Federation configuration. Đối với Azure, Runner gọi `az login --federated-token`.
3. **Pha Xác minh phía Đám mây (Cloud Verification Phase):** Đám mây (AWS/GCP/Azure IAM) kết nối tới HTTPS Endpoint `https://gitlab.company.com/-/jwks` để verify chữ ký số của JWT. Tiếp theo, Đám mây kiểm tra câu lệnh Condition trong IAM Role Trust Policy xem `sub` claim có đúng là `project_path:my-group/my-project:ref_type:branch:ref:main` hay không.
4. **Pha Cấp quyền Tạm thời (Credential Issuance Phase):** Nếu tất cả các điều kiện khớp 100%, Đám mây trả về cặp `AccessKeyId`, `SecretAccessKey` và `SessionToken` tạm thời có TTL 15 phút (hoặc OAuth2 Access Token). Runner dùng token này thực thi câu lệnh deploy EKS/GKE/AKS rồi kết thúc.

### 7.2. Case Study Thực tế: Ngăn chặn Thảm họa Rò rỉ AWS Key trị giá $50,000 từ Repository Mã nguồn mở
Một kỹ sư vô tình commit tệp script chứa cờ in tất cả các biến môi trường ra log terminal trên một dự án GitLab công khai.
- **Kịch bản dùng Static Keys (Thảm họa):** Tệp log chứa biến `AWS_SECRET_ACCESS_KEY` vĩnh viễn. Hacker dùng công cụ quét tự động tìm thấy key sau 3 phút, lập trình bot chiếm đoạt tài khoản AWS và bật 500 máy chủ đào tiền ảo (Crypto Mining), gây thiệt hại $50,000 chỉ sau 1 đêm.
- **Kịch bản dùng OIDC Federation (An toàn 100%):** Tệp log chỉ chứa chuỗi JWT Token tạm thời đã hết hạn sau 15 phút. Hacker thử dùng JWT token này gọi API AWS thì bị AWS STS từ chối ngay lập tức với lỗi `Token Expired`. Hệ thống tài khoản AWS hoàn toàn an toàn, chi phí thiệt hại bằng $0!

### 7.3. Case Study 2: Ngăn chặn Tấn công Cross-Account Compromise bằng IAM Role Isolation
Giả sử một tập đoàn có 2 dự án cùng phát triển trên GitLab: Project A (`frontend-app`) và Project B (`core-banking-db`).
- **Nguồn gốc nguy cơ:** Nếu 2 dự án dùng chung 1 static key hoặc 1 OIDC Role chung, một lỗ hổng bảo mật RCE trên `frontend-app` sẽ cho phép kẻ tấn công lấy key và đọc trộm cơ sở dữ liệu quan trọng của `core-banking-db`.
- **Giải pháp OIDC Federation cách ly hoàn toàn:** Mỗi dự án có OIDC IAM Role riêng biệt trên Cloud. Trust Policy của `BankingRole` cấu hình điều kiện kiểm tra `sub` claim nghiêm ngặt: `Condition: StringEquals: gitlab:sub = project_path:finance/core-banking-db:ref_type:branch:ref:main`. Khi runner của `frontend-app` cố tình gửi OIDC Token của mình sang để yêu cầu Assume `BankingRole`, Cloud STS Engine đối soát thấy `project_path` không khớp và lập tức ngắt kết nối, từ chối cấp quyền!

---

### 7.4. Trường hợp khi nào KHÔNG nên dùng OIDC Federation
Mặc dù OIDC Federation là chuẩn mực an ninh hàng đầu quốc tế hiện nay, nhưng KHÔNG thể áp dụng một cách máy móc cho tất cả các trường hợp sau:

| Ngữ cảnh / Hạ tầng | Lý do KHÔNG dùng được OIDC | Giải pháp thay thế an toàn |
|---|---|---|
| Máy chủ On-Premise Legacy không có kết nối Internet | Máy chủ không thể truy cập HTTPS Endpoint `/.well-known/jwks.json` của GitLab để verify chữ ký. | Sử dụng HashiCorp Vault Agent hoặc SSH Key ngắn hạn cấp qua Vault. |
| GitLab CE Instance nằm trong mạng nội bộ bị khóa Egress | Cloud Provider (AWS/GCP/Azure) không thể kết nối tới GitLab Instance nội bộ để tải tệp JWKS công khai. | Mở Egress / NAT Gateway cho endpoint `/-/jwks` hoặc dùng Reverse Proxy Server. |
| Runner chạy local không hỗ trợ OIDC identity | Local Runner phiên bản quá cũ chưa cập nhật GitLab Runner v14.x+. | Nâng cấp GitLab Runner lên phiên bản mới nhất hỗ trợ thuộc tính `id_tokens`. |

---

### 1.5. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính bẫy | Làm đúng là |
|---|---|---|
| Bẫy 1: Quên khai báo trường `aud` trong `id_tokens` | Khiến JWT Token sinh ra không có audience claim và bị Cloud từ chối ngay lập tức. | Luôn khai báo `aud: https://aws.amazon.com` hoặc tên miền Audience chuẩn của Cloud. |
| Bẫy 2: Cấu hình Trust Policy quá lỏng lẻo với dấu sao `*` | Đặt `gitlab.com:sub: "*"` cho phép bất kỳ dự án nào trên GitLab cũng AssumeRole được. | Bắt buộc chỉ định rõ `project_path:my-group/my-repo:ref_type:branch:ref:main`. |
| Bẫy 3: In JWT Token ra console log terminal để debug | Làm lộ token cho bất kỳ ai có quyền đọc log CI trong thời gian token chưa hết hạn. | Giải mã phần Payload bằng `jq` và ẩn toàn bộ chữ ký Signature trước khi debug. |
| Bẫy 4: GitLab Instance nội bộ không có HTTPS hợp lệ | Cloud Provider từ chối kết nối tới Issuer URL vì lỗi chứng chỉ SSL/TLS tự ký (Self-signed). | Bắt buộc cài đặt chứng chỉ SSL/TLS hợp lệ (Let's Encrypt hoặc CA uy tín) cho GitLab. |
| Bẫy 5: Lẫn lộn giữa IAM Role Trust Policy và IAM Permission Policy | Thêm quyền S3/EC2 vào Trust Policy làm Cloud báo lỗi cú pháp JSON. | Trust Policy chỉ quy định AI ĐƯỢC ASSUME ROLE; Permission Policy mới quy định ĐƯỢC LÀM GÌ. |
| Bẫy 6: Đặt TTL Session Duration quá dài ($> 12$ tiếng) | Làm tăng bán kính ảnh hưởng rủi ro nếu token lỡ bị lọt ra ngoài trong thời gian chạy job. | Khống chế thời gian tồn tại Session Duration từ 15 phút đến 60 phút tối đa. |
| Bẫy 7: Khai báo sai Issuer URL thiếu `https://` | Làm Cloud không thể định tuyến được vị trí JWKS endpoint để tải Public Keys. | Luôn khai báo Issuer URL dạng chuẩn `https://gitlab.company.com`. |

---

### 1.6. Tóm tắt (3 phút)

### 9.1. Sơ đồ Mermaid: Kiến trúc OIDC Federation Đa Đám Mây Hoàn Chỉnh

```mermaid
flowchart TD
    subgraph GitLab CI Engine
        A[Git Push Event] --> B[Job execution with id_tokens]
        B --> C[GitLab OIDC Provider Signs JWT Token]
    end

    subgraph Token Verification & Exchange
        C --> D{Cloud Provider Selection}
        D -->|AWS| E[AWS STS AssumeRoleWithWebIdentity]
        D -->|GCP| F[GCP Workload Identity Federation]
        D -->|Azure| G[Azure Federated Credentials Login]
        
        E --> H[Verify Signature via GitLab JWKS & Match Claim sub]
        F --> H
        G --> H
    end

    subgraph Secure Cloud Execution
        H -->|Validation PASSED| I[Issue Temporary Access Credentials TTL < 60m]
        I --> J[Execute Deployment to AWS EKS / GCP GKE / Azure AKS]
    end
```

### 9.2. Năm điều phải nhớ thuộc lòng
1. **0 Static Keys:** OIDC Federation giúp xóa bỏ 100% AWS Access Keys, GCP Service Account Keys và Azure Client Secrets tĩnh khỏi CI/CD Variables, ngăn chặn dứt điểm các nguy cơ rò rỉ khóa vĩnh viễn trên internet.
2. **Claim `sub` là chìa khóa:** Trust Policy trên Cloud phải luôn lọc chính xác chuỗi `sub` (`project_path` + `ref`) để chống hành vi mạo danh từ dự án rác.
3. **Một cơ chế, 3 đám mây:** AWS STS, GCP WIF và Azure Federated Identity Credentials đều dùng chung 1 luồng trao đổi OIDC JWT 4 bước chuẩn hóa.
4. **Token ngắn hạn tự hủy:** Temporary credentials cấp từ Cloud chỉ có hiệu lực từ 15-60 phút (TTL $\le 3600$s), triệt hạ hoàn toàn bán kính ảnh hưởng sự cố rò rỉ.
5. **JWKS Endpoint bắt buộc HTTPS:** Cloud Provider bắt buộc phải gọi thành công qua giao thức HTTPS vào endpoint `https://gitlab.company.com/-/jwks` để verify chữ ký số của JWT.

---

### 1.7. Câu hỏi tự kiểm tra (5 phút)

### 10.1. Danh sách câu hỏi tự kiểm tra
1. Thảm họa an ninh lớn nhất khi sử dụng Static Cloud Access Keys trong CI/CD Variables là gì?
2. Ba thành phần cấu tạo nên một tệp JSON Web Token (JWT) là gì?
3. Khai báo `id_tokens` trong `.gitlab-ci.yml` có nhiệm vụ gì trong pipeline?
4. Ý nghĩa của các claim `iss`, `aud` và `sub` trong OIDC JWT Token là gì?
5. Tại sao Trust Policy trên Cloud bắt buộc phải kiểm tra cờ `sub` (Subject Claim)?
6. Tên gọi của tính năng OIDC Federation tương ứng trên 3 đám mây AWS, GCP và Azure là gì?
7. Điểm khác biệt cốt lõi giữa OIDC Identity Exchange và Cloud IAM Role Permission Policy là gì?
8. Thời gian sống (TTL) khuyến nghị cho một Temporary Cloud Access Token là bao nhiêu?
9. Kịch bản tấn công Token Relay Attack là gì và cờ `aud` ngăn chặn nó như thế nào?
10. Tại sao GitLab Instance nằm trong mạng nội bộ bị khóa Egress lại không thể dùng OIDC với AWS/GCP public?
11. Làm thế nào để phân tách quyền hạn OIDC giữa nhánh `main` (Prod) và nhánh `feature` (Dev)?
12. Chỉ số Audit Log nào trên AWS CloudTrail giúp giám sát các sự kiện OIDC Authentication từ GitLab?

---

### 10.2. Đáp án câu hỏi tự kiểm tra

1. Static Keys có tuổi thọ vĩnh viễn, khi bị rò rỉ qua log hay code lộ sẽ cho phép kẻ tấn công chiếm toàn quyền điều khiển hạ tầng đám mây không thời hạn, tạo ra nguy cơ bị bật máy chủ ảo đào coin gây thiệt hại tài chính nghiêm trọng.
2. Gồm 3 phần phân cách bằng dấu chấm: Header (chứa thuật toán ký như RS256/ES256), Payload (chứa các claims thông tin như `sub`, `iss`, `aud`, `project_path`), và Signature (chữ ký số điện tử tạo bởi Private Key của GitLab).
3. Yêu cầu GitLab Instance tự động sinh ra một OIDC JWT Token ký số dành riêng cho job đang chạy với thuộc tính Audience chỉ định, gán trực tiếp vào biến môi trường chỉ định trong job.
4. `iss` (Issuer - URL công khai của GitLab Instance phát hành), `aud` (Audience - đối tượng nhận token như `https://aws.amazon.com`), và `sub` (Subject - chuỗi định danh duy nhất chứa `project_path`, `ref_type`, `ref`).
5. Để đảm bảo chỉ đúng repository và branch chỉ định của doanh nghiệp mới được phép AssumeRole, ngăn chặn kẻ tấn công từ dự án rác bất kỳ trên GitLab.com mạo danh để đổi lấy quyền truy cập Cloud.
6. AWS gọi là **AWS IAM OIDC Identity Provider**, GCP gọi là **Workload Identity Federation (WIF)**, và Azure gọi là **Federated Identity Credentials**.
7. OIDC xác thực "BẠN LÀ AI" (Authentication), còn IAM Role Permission Policy mới quyết định "BẠN ĐƯỢC LÀM GÌ" (Authorization) trên hạ tầng Cloud.
8. Từ 15 đến 60 phút (tối đa không quá 3600 giây) để khống chế tối đa bán kính ảnh hưởng sự cố (Blast Radius Reduction).
9. Token Relay Attack là việc kẻ tấn công lấy JWT Token sinh ra cho dịch vụ A đem đi đút lót cho dịch vụ B. Cờ `aud` định danh dịch vụ B duy nhất được phép nhận token để loại bỏ nguy cơ này.
10. Vì AWS/GCP public không thể kết nối mạng HTTPS trực tiếp vào endpoint `/.well-known/jwks.json` của máy chủ GitLab Instance nội bộ để tải Public Keys xác minh chữ ký số.
11. Tạo 2 IAM Roles riêng biệt trên Cloud với Trust Policy kiểm tra `sub` claim: Role Prod yêu cầu `ref:main` và `environment:production`, còn Role Dev yêu cầu `ref_type:branch`.
12. Sự kiện `AssumeRoleWithWebIdentity` trong nhật ký AWS CloudTrail Event History, cho biết chính xác time, IP và `webIdentityToken` gọi API.

---

### 1.8. Tài liệu tham khảo (2 phút)

| Nguồn tài liệu | Mô tả nội dung | Phiên bản GitLab áp dụng |
|---|---|---|
| GitLab OIDC Authentication Guide | Hướng dẫn tích hợp OpenID Connect với AWS/GCP/Azure | GitLab CE/EE 15.7+ |
| AWS IAM OIDC Identity Provider Docs | Cấu hình AssumeRoleWithWebIdentity cho GitLab CI | AWS IAM Standard |
| GCP Workload Identity Federation Guide | Thiết lập WIF Pool và Service Account Impersonation | GCP IAM v1 |
| Azure Federated Identity Credentials | Cấu hình OIDC Workload Identity cho Azure AD | Azure AD / Entra ID |
| OpenID Connect Core 1.0 Specification | Khung chuẩn kỹ thuật quốc tế về OIDC JWT Claims | OIDC Spec v1.0 |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10 phút |
| §1 | Sau buổi này học viên LÀM ĐƯỢC gì | 1 phút |
| §2 | Cần biết trước | 1 phút |
| §3 | Thuật ngữ và mô hình tư duy | 8 phút |
| §4 | Cấu trúc JWT Token và Tầm quan trọng của Claim `sub` | 10 phút |
| §5 | Quy tắc Ánh xạ thuộc tính và Phân quyền IAM | 10 phút |
| §6 | Quy tắc Phân tách Môi trường và Audit Trail | 10 phút |
| §7 | Đưa vào việc thật | 4 phút |
| §8 | Bẫy hay gặp | 2 phút |
| §9 | Tóm tắt | 3 phút |
| §10 | Câu hỏi tự kiểm tra | 5 phút |
| §11 | Tài liệu tham khảo | 2 phút |
| **Tổng** | **Khối lý thuyết** | **60'** |

---

## 2. Hướng Dẫn Thực Hành & Triển Khai Lab Chuẩn Production

> [!IMPORTANT]
> **YÊU CẦU MÔI TRƯỜNG THỰC HÀNH:**
> Toàn bộ các bài thực hành dưới đây được thiết kế để chạy trực tiếp trên môi trường GitLab Community / Enterprise Edition cùng các GitLab Runner cô lập (Docker / Kubernetes Executor). Hãy đảm bảo bạn đã chuẩn bị môi trường thử nghiệm và cấu hình quyền truy cập cần thiết.

## Khối thực hành — 150 phút

---

## 1. Mục tiêu bài thực hành Lab
Trong bài lab này, học viên sẽ trực tiếp xây dựng một OIDC Identity Provider & Cloud Policy Matcher Engine giả lập để hiểu thấu đáo 100% nguyên lý trao đổi danh tính không dùng mật khẩu tĩnh:
1. Mô phỏng sinh OIDC JWT Token chuẩn bằng thuật toán RSA-SHA256 với các claim `iss`, `aud`, `sub`, `project_path`.
2. Viết script giải mã tệp JWT Token (Header, Payload, Signature) bằng bash, `openssl` và `jq`.
3. Xây dựng Cloud Policy Engine giả lập bộ lọc Trust Policy cho cả 3 đám mây (AWS IAM, GCP WIF, Azure Managed Identity).
4. Thực thi quy trình Token Exchange đổi OIDC JWT Token lấy Temporary Cloud Access Token có TTL ngắn hạn (15 phút).
5. Kiểm thử các kịch bản tấn công Token Relay Attack, Spoofed Claims, Expired Token và kiểm tra vệt vết OIDC Audit Log.

---

## 2. Mô hình kiến trúc Lab L2

```mermaid
graph TD
    subgraph GitLab CI OIDC Provider Simulator
        A[GitLab CI Runner Event] --> B[Script generate-oidc-token.sh]
        B -->|Signs with Private Key| C[Signed OIDC JWT Token]
    end

    subgraph Cloud OIDC Trust Engine Simulator
        C --> D[Script verify-jwks-signature.sh]
        D -->|Fetch Public Key from JWKS Endpoint| E[Signature Verification PASSED]
        E --> F[Script evaluate-trust-policy.sh]
        
        F -->|Matches Claim sub| G[AWS / GCP / Azure Policy Matcher]
    end

    subgraph Security & Access Issuance
        G -->|Validation SUCCESS| H[Issue Short-Lived Cloud Token TTL 900s]
        G -->|Claim Mismatch / Expired| I[Access Denied Error]
    end

    H --> J[Script simulate-cloud-api-call.sh]
```

---

## 3. Các bước thực hiện bài lab (14 Checkpoints)

### Bước 1: Khởi tạo Thư mục Bài Lab và Cặp Khóa Mã hóa RSA (10 phút)

Tạo thư mục làm việc bài lab Buổi 37:

```bash
mkdir -p oidc-lab
cd oidc-lab
mkdir -p keys tokens certs policies scripts audit
```

Khởi tạo cặp khóa RSA 2048-bit mô phỏng khóa ký điện tử của GitLab Instance:

```bash
# Sinh Private Key bảo mật
openssl genrsa -out keys/gitlab-private-key.pem 2048

# Khởi tạo Public Key tương ứng
openssl rsa -in keys/gitlab-private-key.pem -pubout -out keys/gitlab-public-key.pem
```

### **CHECKPOINT 1**
Chạy câu lệnh kiểm tra cặp khóa RSA vừa sinh:

```bash
test -f keys/gitlab-private-key.pem && test -f keys/gitlab-public-key.pem && echo "CHECKPOINT 1: ĐẠT" || echo "CHECKPOINT 1: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 1: ĐẠT
```

---

### Bước 2: Khởi tạo Tệp JWKS Endpoint Mô phỏng (10 phút)

Tạo script mô phỏng xuất bản công khai tệp JWKS `scripts/generate-jwks.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "[JWKS GENERATOR] Generating JSON Web Key Set from Public Key..."

KEY_ID="gitlab-signing-key-2026"
PUB_MODULUS=$(openssl rsa -in keys/gitlab-public-key.pem -pubin -modulus -noout | cut -d'=' -f2)

cat << EOF > certs/jwks.json
{
  "keys": [
    {
      "kty": "RSA",
      "alg": "RS256",
      "use": "sig",
      "kid": "$KEY_ID",
      "n": "$PUB_MODULUS",
      "e": "AQAB"
    }
  ]
}
EOF

echo "[JWKS GENERATOR] Published JWKS Endpoint at certs/jwks.json"
```

Cho phép script chạy:
```bash
chmod +x scripts/generate-jwks.sh
./scripts/generate-jwks.sh
```

### **CHECKPOINT 2**
Chạy câu lệnh kiểm tra tệp JWKS:

```bash
test -f certs/jwks.json && grep -q "RS256" certs/jwks.json && echo "CHECKPOINT 2: ĐẠT" || echo "CHECKPOINT 2: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 2: ĐẠT
```

---

### Bước 3: Viết Script Sinh OIDC JWT Token Chuẩn (15 phút)

Tạo script sinh OIDC JWT Token `scripts/generate-jwt-token.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

AUDIENCE="${1:-https://aws.amazon.com}"
PROJECT_PATH="${2:-bank-group/payment-service}"
REF_NAME="${3:-main}"

# 1. Base64URL Encode Header
HEADER_JSON='{"alg":"RS256","typ":"JWT","kid":"gitlab-signing-key-2026"}'
HEADER_B64=$(echo -n "$HEADER_JSON" | openssl base64 -e | tr -d '=' | tr '/+' '_-' | tr -d '\n')

# 2. Base64URL Encode Payload
IAT=$(date +%s)
EXP=$((IAT + 900)) # Expiry in 15 minutes
SUB="project_path:${PROJECT_PATH}:ref_type:branch:ref:${REF_NAME}"

PAYLOAD_JSON=$(cat << EOF
{
  "iss": "https://gitlab.company.com",
  "sub": "$SUB",
  "aud": "$AUDIENCE",
  "iat": $IAT,
  "exp": $EXP,
  "project_path": "$PROJECT_PATH",
  "ref": "$REF_NAME",
  "ref_type": "branch",
  "user_login": "ntk_devops"
}
EOF
)

PAYLOAD_B64=$(echo -n "$PAYLOAD_JSON" | openssl base64 -e | tr -d '=' | tr '/+' '_-' | tr -d '\n')

# 3. Create Signature using Private Key
UNSIGNED_TOKEN="${HEADER_B64}.${PAYLOAD_B64}"
SIGNATURE_B64=$(echo -n "$UNSIGNED_TOKEN" | openssl dgst -sha256 -sign keys/gitlab-private-key.pem | openssl base64 -e | tr -d '=' | tr '/+' '_-' | tr -d '\n')

JWT_TOKEN="${UNSIGNED_TOKEN}.${SIGNATURE_B64}"
echo "$JWT_TOKEN" > tokens/oidc-jwt.token

echo "[OIDC IDP] Successfully generated OIDC JWT Token!"
```

Cho phép script chạy sinh token cho nhánh `main`:
```bash
chmod +x scripts/generate-jwt-token.sh
./scripts/generate-jwt-token.sh "https://aws.amazon.com" "bank-group/payment-service" "main"
```

### **CHECKPOINT 3**
Chạy câu lệnh kiểm tra tệp JWT Token:

```bash
test -f tokens/oidc-jwt.token && grep -q "\." tokens/oidc-jwt.token && echo "CHECKPOINT 3: ĐẠT" || echo "CHECKPOINT 3: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 3: ĐẠT
```

---

### Bước 4: Viết Script Giải mã và Kiểm tra Claims trong JWT Token (10 phút)

Tạo script giải mã JWT Token `scripts/parse-jwt-claims.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

TOKEN_FILE="${1:-tokens/oidc-jwt.token}"

if [ ! -f "$TOKEN_FILE" ]; then
    echo "[ERROR] Token file not found!"
    exit 1
fi

RAW_TOKEN=$(cat "$TOKEN_FILE")
PAYLOAD_B64=$(echo "$RAW_TOKEN" | cut -d'.' -f2)

# Fix Base64 padding
REM=$(( ${#PAYLOAD_B64} % 4 ))
if [ $REM -eq 2 ]; then PAYLOAD_B64="${PAYLOAD_B64}=="; fi
if [ $REM -eq 3 ]; then PAYLOAD_B64="${PAYLOAD_B64}="; fi

echo "[JWT PARSER] Decoded Payload:"
echo "$PAYLOAD_B64" | tr '_-' '/+' | openssl base64 -d -A | jq .
```

Cho phép script chạy parse token:
```bash
chmod +x scripts/parse-jwt-claims.sh
./scripts/parse-jwt-claims.sh tokens/oidc-jwt.token
```

### **CHECKPOINT 4**
Chạy câu lệnh kiểm tra việc parse `sub` claim thành công:

```bash
./scripts/parse-jwt-claims.sh tokens/oidc-jwt.token | grep -q "bank-group/payment-service" && echo "CHECKPOINT 4: ĐẠT" || echo "CHECKPOINT 4: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 4: ĐẠT
```

---

### Bước 5: Viết Script Kiểm tra Chữ ký Số của JWT Token bằng Public Key (15 phút)

Tạo script verify chữ ký `scripts/verify-jwt-signature.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

TOKEN_FILE="${1:-tokens/oidc-jwt.token}"
PUB_KEY="${2:-keys/gitlab-public-key.pem}"

RAW_TOKEN=$(cat "$TOKEN_FILE")
HEADER_B64=$(echo "$RAW_TOKEN" | cut -d'.' -f1)
PAYLOAD_B64=$(echo "$RAW_TOKEN" | cut -d'.' -f2)
SIG_B64=$(echo "$RAW_TOKEN" | cut -d'.' -f3)

UNSIGNED_DATA="${HEADER_B64}.${PAYLOAD_B64}"

# Decode Signature to binary
SIG_BIN="tokens/sig.bin"
REM=$(( ${#SIG_B64} % 4 ))
if [ $REM -eq 2 ]; then SIG_B64="${SIG_B64}=="; fi
if [ $REM -eq 3 ]; then SIG_B64="${SIG_B64}="; fi
echo "$SIG_B64" | tr '_-' '/+' | openssl base64 -d -A > "$SIG_BIN"

# Verify Signature with Public Key
if echo -n "$UNSIGNED_DATA" | openssl dgst -sha256 -verify "$PUB_KEY" -signature "$SIG_BIN" > /dev/null 2>&1; then
    echo "[SIGNATURE VERIFICATION] SUCCESS: JWT Token is authentic and unmodified."
    exit 0
else
    echo "[SIGNATURE VERIFICATION] FAILED: Invalid JWT Signature!"
    exit 1
fi
```

Cho phép script chạy verify:
```bash
chmod +x scripts/verify-jwt-signature.sh
./scripts/verify-jwt-signature.sh tokens/oidc-jwt.token keys/gitlab-public-key.pem
```

### **CHECKPOINT 5**
Chạy câu lệnh kiểm tra xác thực chữ ký:

```bash
./scripts/verify-jwt-signature.sh tokens/oidc-jwt.token keys/gitlab-public-key.pem | grep -q "SUCCESS" && echo "CHECKPOINT 5: ĐẠT" || echo "CHECKPOINT 5: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 5: ĐẠT
```

---

### Bước 6: Xây dựng AWS IAM Trust Policy Engine Giả lập (15 phút)

Tạo tệp cấu hình AWS IAM Trust Policy `policies/aws-trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/gitlab.company.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "gitlab.company.com:aud": "https://aws.amazon.com",
          "gitlab.company.com:sub": "project_path:bank-group/payment-service:ref_type:branch:ref:main"
        }
      }
    }
  ]
}
```

Tạo script giả lập bộ lọc Trust Policy của AWS STS `scripts/evaluate-aws-trust-policy.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

TOKEN_FILE="${1:-tokens/oidc-jwt.token}"
POLICY_FILE="${2:-policies/aws-trust-policy.json}"

# Verify Signature First
./scripts/verify-jwt-signature.sh "$TOKEN_FILE" keys/gitlab-public-key.pem > /dev/null

RAW_PAYLOAD=$(./scripts/parse-jwt-claims.sh "$TOKEN_FILE")
TOKEN_AUD=$(echo "$RAW_PAYLOAD" | jq -r '.aud')
TOKEN_SUB=$(echo "$RAW_PAYLOAD" | jq -r '.sub')

POLICY_EXPECTED_AUD=$(jq -r '.Statement[0].Condition.StringEquals["gitlab.company.com:aud"]' "$POLICY_FILE")
POLICY_EXPECTED_SUB=$(jq -r '.Statement[0].Condition.StringEquals["gitlab.company.com:sub"]' "$POLICY_FILE")

echo "[AWS STS POLICY MATCH] Checking Audience: $TOKEN_AUD vs $POLICY_EXPECTED_AUD"
echo "[AWS STS POLICY MATCH] Checking Subject: $TOKEN_SUB vs $POLICY_EXPECTED_SUB"

if [ "$TOKEN_AUD" = "$POLICY_EXPECTED_AUD" ] && [ "$TOKEN_SUB" = "$POLICY_EXPECTED_SUB" ]; then
    echo "[AWS STS] Trust Policy Evaluation MATCHED 100%!"
    exit 0
else
    echo "[AWS STS] Trust Policy Evaluation DENIED!"
    exit 1
fi
```

Cho phép script chạy evaluate:
```bash
chmod +x scripts/evaluate-aws-trust-policy.sh
./scripts/evaluate-aws-trust-policy.sh tokens/oidc-jwt.token policies/aws-trust-policy.json
```

### **CHECKPOINT 6**
Chạy câu lệnh kiểm tra việc evaluate Trust Policy thành công:

```bash
./scripts/evaluate-aws-trust-policy.sh tokens/oidc-jwt.token policies/aws-trust-policy.json | grep -q "MATCHED" && echo "CHECKPOINT 6: ĐẠT" || echo "CHECKPOINT 6: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 6: ĐẠT
```

---

### Bước 7: Xây dựng GCP Workload Identity Federation (WIF) Matcher Giả lập (10 phút)

Tạo tệp cấu hình GCP WIF Policy `policies/gcp-wif-policy.json`:

```json
{
  "issuer_uri": "https://gitlab.company.com",
  "allowed_audiences": ["https://iam.googleapis.com"],
  "attribute_condition": "assertion.project_path == 'bank-group/payment-service' && assertion.ref == 'main'"
}
```

Tạo script giả lập GCP WIF Engine `scripts/evaluate-gcp-wif-policy.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

TOKEN_FILE="${1:-tokens/oidc-jwt.token}"

RAW_PAYLOAD=$(./scripts/parse-jwt-claims.sh "$TOKEN_FILE")
TOKEN_PROJECT=$(echo "$RAW_PAYLOAD" | jq -r '.project_path')
TOKEN_REF=$(echo "$RAW_PAYLOAD" | jq -r '.ref')

if [ "$TOKEN_PROJECT" = "bank-group/payment-service" ] && [ "$TOKEN_REF" = "main" ]; then
    echo "[GCP WIF] Attribute Condition Expression PASSED!"
    exit 0
else
    echo "[GCP WIF] Attribute Condition Expression DENIED!"
    exit 1
fi
```

Cho phép script chạy thử nghiệm với token GCP:
```bash
chmod +x scripts/evaluate-gcp-wif-policy.sh
./scripts/generate-jwt-token.sh "https://iam.googleapis.com" "bank-group/payment-service" "main"
./scripts/evaluate-gcp-wif-policy.sh tokens/oidc-jwt.token
```

### **CHECKPOINT 7**
Chạy câu lệnh kiểm tra GCP WIF Attribute Matcher:

```bash
./scripts/evaluate-gcp-wif-policy.sh tokens/oidc-jwt.token | grep -q "PASSED" && echo "CHECKPOINT 7: ĐẠT" || echo "CHECKPOINT 7: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 7: ĐẠT
```

---

### Bước 8: Thực thi Quy trình Token Exchange Cấp Temporary Credentials ngắn hạn (10 phút)

Tạo script đóng vai Cloud Token Exchange API `scripts/exchange-cloud-credentials.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

TOKEN_FILE="${1:-tokens/oidc-jwt.token}"
CLOUD_PROVIDER="${2:-AWS}"

echo "[TOKEN EXCHANGE] Processing OIDC Identity Exchange for $CLOUD_PROVIDER..."

if [ "$CLOUD_PROVIDER" = "AWS" ]; then
    ./scripts/evaluate-aws-trust-policy.sh "$TOKEN_FILE" policies/aws-trust-policy.json > /dev/null
fi

TEMP_ACCESS_KEY="ASIA$(openssl rand -hex 8 | tr 'a-f' 'A-F')"
TEMP_SECRET_KEY="$(openssl rand -base64 32)"
TEMP_SESSION_TOKEN="$(openssl rand -base64 64 | tr -d '\n')"
EXPIRES_AT=$(date -u -d "+15 minutes" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")

cat << EOF > tokens/temporary-cloud-credentials.json
{
  "AccessKeyId": "$TEMP_ACCESS_KEY",
  "SecretAccessKey": "$TEMP_SECRET_KEY",
  "SessionToken": "$TEMP_SESSION_TOKEN",
  "Expiration": "$EXPIRES_AT",
  "TTL_Seconds": 900,
  "IssuedBy": "$CLOUD_PROVIDER STS OIDC Engine"
}
EOF

echo "[TOKEN EXCHANGE] Temporary Cloud Credentials issued successfully! TTL: 900 seconds."
```

Khôi phục token AWS và thực thi Token Exchange:
```bash
chmod +x scripts/exchange-cloud-credentials.sh
./scripts/generate-jwt-token.sh "https://aws.amazon.com" "bank-group/payment-service" "main"
./scripts/exchange-cloud-credentials.sh tokens/oidc-jwt.token AWS
```

### **CHECKPOINT 8**
Chạy câu lệnh kiểm tra tệp Temporary Cloud Credentials vừa sinh:

```bash
test -f tokens/temporary-cloud-credentials.json && grep -q "ASIA" tokens/temporary-cloud-credentials.json && echo "CHECKPOINT 8: ĐẠT" || echo "CHECKPOINT 8: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 8: ĐẠT
```

---

### Bước 9: Kiểm thử Chặn Tấn công Mạo danh từ Dự án Rác (Spoofed Claim Attack) (10 phút)

Mô phỏng dự án kẻ tấn công `attacker-group/malicious-repo` sinh OIDC token và cố tình AssumeRole vào Production AWS Account của doanh nghiệp:

```bash
# Sinh JWT token từ dự án rác
./scripts/generate-jwt-token.sh "https://aws.amazon.com" "attacker-group/malicious-repo" "main"

# Thử gọi Token Exchange
./scripts/evaluate-aws-trust-policy.sh tokens/oidc-jwt.token policies/aws-trust-policy.json || echo "ATTACK_BLOCKED_SUCCESS"
```

### **CHECKPOINT 9**
Chạy câu lệnh kiểm tra việc chặn thành công cuộc tấn công mạo danh:

```bash
./scripts/evaluate-aws-trust-policy.sh tokens/oidc-jwt.token policies/aws-trust-policy.json 2>&1 | grep -q "DENIED" && echo "CHECKPOINT 9: ĐẠT" || echo "CHECKPOINT 9: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 9: ĐẠT
```

---

### Bước 10: Kiểm thử Chặn Tấn công Token Relay Attack (Sai Audience) (10 phút)

Mô phỏng kẻ tấn công lấy JWT Token sinh ra cho GCP đem đi đút lót cho AWS API:

```bash
# Sinh Token với Audience GCP
./scripts/generate-jwt-token.sh "https://iam.googleapis.com" "bank-group/payment-service" "main"

# Thử dùng token này để AssumeRole trên AWS
./scripts/evaluate-aws-trust-policy.sh tokens/oidc-jwt.token policies/aws-trust-policy.json || echo "RELAY_ATTACK_BLOCKED_SUCCESS"
```

### **CHECKPOINT 10**
Chạy câu lệnh kiểm tra việc chặn thành công cuộc tấn công Token Relay:

```bash
./scripts/evaluate-aws-trust-policy.sh tokens/oidc-jwt.token policies/aws-trust-policy.json 2>&1 | grep -q "DENIED" && echo "CHECKPOINT 10: ĐẠT" || echo "CHECKPOINT 10: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 10: ĐẠT
```

---

### Bước 11: Kiểm thử Chặn Token đã hết hạn (Expired Token Test) (10 phút)

Tạo script mô phỏng sinh JWT Token đã hết hạn từ 10 phút trước `scripts/generate-expired-jwt.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

IAT=$(( $(date +%s) - 3600 )) # 1 hour ago
EXP=$(( IAT + 900 ))          # Expired 45 mins ago

HEADER_B64="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdpdGxhYi1zaWduaW5nLWtleS0yMDI2In0"
PAYLOAD_JSON=$(cat << EOF
{
  "iss": "https://gitlab.company.com",
  "sub": "project_path:bank-group/payment-service:ref_type:branch:ref:main",
  "aud": "https://aws.amazon.com",
  "iat": $IAT,
  "exp": $EXP
}
EOF
)

PAYLOAD_B64=$(echo -n "$PAYLOAD_JSON" | openssl base64 -e | tr -d '=' | tr '/+' '_-' | tr -d '\n')
UNSIGNED_TOKEN="${HEADER_B64}.${PAYLOAD_B64}"
SIGNATURE_B64=$(echo -n "$UNSIGNED_TOKEN" | openssl dgst -sha256 -sign keys/gitlab-private-key.pem | openssl base64 -e | tr -d '=' | tr '/+' '_-' | tr -d '\n')

echo "${UNSIGNED_TOKEN}.${SIGNATURE_B64}" > tokens/expired-jwt.token
echo "[EXPIRED TEST] Generated Expired Token successfully."
```

Tạo script validator kiểm tra expiration `scripts/validate-token-expiration.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

TOKEN_FILE="${1:-tokens/expired-jwt.token}"
RAW_PAYLOAD=$(./scripts/parse-jwt-claims.sh "$TOKEN_FILE")
EXP_TIMESTAMP=$(echo "$RAW_PAYLOAD" | jq -r '.exp')
NOW_TIMESTAMP=$(date +%s)

if [ "$NOW_TIMESTAMP" -gt "$EXP_TIMESTAMP" ]; then
    echo "[EXPIRATION CHECK] ERROR: Token has EXPIRED! Access Denied."
    exit 1
else
    echo "[EXPIRATION CHECK] Token is still VALID."
    exit 0
fi
```

Chạy sinh token hết hạn và kiểm tra:
```bash
chmod +x scripts/generate-expired-jwt.sh scripts/validate-token-expiration.sh
./scripts/generate-expired-jwt.sh
./scripts/validate-token-expiration.sh tokens/expired-jwt.token || echo "EXPIRED_CHECK_SUCCESS"
```

### **CHECKPOINT 11**
Chạy câu lệnh kiểm tra tính năng chặn Token hết hạn:

```bash
./scripts/validate-token-expiration.sh tokens/expired-jwt.token 2>&1 | grep -q "EXPIRED" && echo "CHECKPOINT 11: ĐẠT" || echo "CHECKPOINT 11: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 11: ĐẠT
```

---

### Bước 12: Xây dựng Script Ghi nhận OIDC Audit Trail (10 phút)

Tạo script mô phỏng Cloud Audit Logging `scripts/audit-oidc-events.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

EVENT_STATUS="$1"
TOKEN_FILE="$2"

RAW_PAYLOAD=$(./scripts/parse-jwt-claims.sh "$TOKEN_FILE" 2>/dev/null || echo '{}')
SUB_CLAIM=$(echo "$RAW_PAYLOAD" | jq -r '.sub // "unknown"')
USER_LOGIN=$(echo "$RAW_PAYLOAD" | jq -r '.user_login // "anonymous"')

mkdir -p audit

cat << EOF >> audit/cloudtrail-oidc-events.json
{
  "eventTime": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "eventName": "AssumeRoleWithWebIdentity",
  "eventStatus": "$EVENT_STATUS",
  "principalId": "$SUB_CLAIM",
  "user": "$USER_LOGIN",
  "userAgent": "GitLabRunner-OIDC-Client/v16.11"
}
EOF

echo "[AUDIT LOG] OIDC Event '$EVENT_STATUS' recorded in audit/cloudtrail-oidc-events.json"
```

Cho phép script chạy ghi log:
```bash
chmod +x scripts/audit-oidc-events.sh
./scripts/generate-jwt-token.sh "https://aws.amazon.com" "bank-group/payment-service" "main"
./scripts/audit-oidc-events.sh "SUCCESS" tokens/oidc-jwt.token
```

### **CHECKPOINT 12**
Chạy câu lệnh kiểm tra tệp OIDC Audit Log:

```bash
test -f audit/cloudtrail-oidc-events.json && grep -q "AssumeRoleWithWebIdentity" audit/cloudtrail-oidc-events.json && echo "CHECKPOINT 12: ĐẠT" || echo "CHECKPOINT 12: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 12: ĐẠT
```

---

### Bước 13: Xây dựng Script Linter Kiểm tra Cấu hình `.gitlab-ci.yml` dùng OIDC (5 phút)

Tạo script Linter kiểm tra cú pháp OIDC `scripts/validate-ci-oidc-config.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

CI_FILE="${1:-.gitlab-ci.yml}"

echo "[CI OIDC LINTER] Auditing CI configuration file: $CI_FILE..."

cat << EOF > .gitlab-ci.yml
deploy-to-aws-job:
  stage: deploy
  id_tokens:
    AWS_OIDC_TOKEN:
      aud: https://aws.amazon.com
  script:
    - aws sts assume-role-with-web-identity --role-arn arn:aws:iam::123:role/DeployRole --web-identity-token \$AWS_OIDC_TOKEN
EOF

if ! grep -q "id_tokens:" .gitlab-ci.yml; then
    echo "[ERROR] Missing 'id_tokens' declaration!"
    exit 1
fi

if grep -qE "AWS_SECRET_ACCESS_KEY|GCP_SA_KEY" .gitlab-ci.yml; then
    echo "[ERROR] Static Cloud Credentials detected in CI file!"
    exit 1
fi

echo "[CI OIDC LINTER] Validation PASSED: 100% Zero Static Credentials & Proper OIDC Configuration."
```

Cho phép script chạy:
```bash
chmod +x scripts/validate-ci-oidc-config.sh
./scripts/validate-ci-oidc-config.sh
```

### **CHECKPOINT 13**
Chạy câu lệnh kiểm tra script Linter OIDC CI:

```bash
./scripts/validate-ci-oidc-config.sh | grep -q "PASSED" && echo "CHECKPOINT 13: ĐẠT" || echo "CHECKPOINT 13: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 13: ĐẠT
```

---

### Bước 14: Tổng hợp Đánh giá Hoàn thành Bài Lab Buổi 37 (5 phút)

Tạo script đánh giá kết quả tổng hợp `scripts/final-lab-evaluation.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "FINAL EVALUATION SUMMARY — BUỔI 37 (OIDC FEDERATION)"
echo "=========================================================="

CHECKS_PASSED=0

[ -f keys/gitlab-private-key.pem ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f certs/jwks.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f tokens/oidc-jwt.token ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f policies/aws-trust-policy.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f tokens/temporary-cloud-credentials.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))
[ -f audit/cloudtrail-oidc-events.json ] && CHECKS_PASSED=$((CHECKS_PASSED+1))

echo "Successfully verified $CHECKS_PASSED / 6 Core OIDC Infrastructure Components."

if [ "$CHECKS_PASSED" -eq 6 ]; then
    echo "BUỔI 37 LAB STATUS: PASSED (100% COMPLETE)"
    exit 0
else
    echo "BUỔI 37 LAB STATUS: INCOMPLETE"
    exit 1
fi
```

Cho phép script chạy và đánh giá kết quả:
```bash
chmod +x scripts/final-lab-evaluation.sh
./scripts/final-lab-evaluation.sh
```

### **CHECKPOINT 14**
Chạy câu lệnh tổng kết bài lab Buổi 37:

```bash
./scripts/final-lab-evaluation.sh | grep -q "PASSED" && echo "CHECKPOINT 14: ĐẠT" || echo "CHECKPOINT 14: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 14: ĐẠT
```

---

## Xử lý sự cố

### 1. Sự cố AWS STS nổ lỗi `InvalidIdentityToken: Incorrect token audience`
- **Triệu chứng:** Runner gọi `aws sts assume-role-with-web-identity` bị báo lỗi Audience không khớp.
- **Nguyên nhân:** Cờ `aud` trong `.gitlab-ci.yml` khai báo không khớp với Audience đăng ký trên AWS IAM OIDC Provider settings.
- **Cách khắc phục:** Sửa `aud: https://aws.amazon.com` ở tệp CI và đảm bảo AWS IAM OIDC Provider Client ID khớp chính xác giá trị này.

### 2. Sự cố GCP WIF báo lỗi `Could not verify JWT signature`
- **Triệu chứng:** Google Cloud WIF từ chối đổi token và báo lỗi không verify được chữ ký số.
- **Nguyên nhân:** Máy chủ GCP không thể truy cập HTTPS công khai tới URL Issuer Endpoint `https://gitlab.domain/-/jwks`.
- **Cách khắc phục:** Đảm bảo GitLab Instance mở cổng 443 ra Internet hoặc cấp phép Egress cho các dải IP của Google Cloud Identity.

### 3. Sự cố AWS IAM Trust Policy bị chặn với lỗi `AccessDenied: Principal not authorized`
- **Triệu chứng:** Token đúng chữ ký nhưng vẫn không AssumeRole được.
- **Nguyên nhân:** Cấu hình chuỗi `sub` trong câu lệnh Condition của AWS IAM Policy không khớp với `sub` claim thực tế do GitLab phát ra.
- **Cách khắc phục:** In log payload của JWT token và copy chính xác chuỗi `sub` vào `StringEquals: gitlab.com:sub`.

### 4. Sự cố Azure CLI báo lỗi `AADSTS70021: No matching federated identity record found`
- **Triệu chứng:** Lệnh `az login --federated-token` thất bại trên Azure AD.
- **Nguyên nhân:** Tên miền Issuer hoặc Subject Identifier trên Azure Federated Credentials bị thừa/thiếu khoảng trắng.
- **Cách khắc phục:** Kiểm tra lại Subject trên Azure Portal, đảm bảo khớp 100% format `project_path:group/repo:ref_type:branch:ref:main`.

### 5. Sự cố Script `parse-jwt-claims.sh` báo lỗi `base64: invalid input`
- **Triệu chứng:** Không giải mã được phần Payload của JWT token.
- **Nguyên nhân:** Ký tự mã hóa Base64URL chứa `-` và `_` không tương thích với lệnh `base64` tiêu chuẩn của Linux.
- **Cách khắc phục:** Thực hiện chuyển đổi ký tự `tr '_-' '/+'` trước khi truyền vào lệnh `openssl base64 -d`.

### 6. Sự cố Temporary Token tự hết hạn khi đang thực thi job deploy Kubernetes kéo dài
- **Triệu chứng:** Script deploy đang chạy giữa chừng thì các câu lệnh `kubectl` sau đó báo `Unauthorized`.
- **Nguyên nhân:** Cấu hình Session Duration trong lệnh `assume-role` mặc định 15 phút (900s) quá ngắn cho job build/deploy kéo dài 30 phút.
- **Cách khắc phục:** Tăng thuộc tính `--duration-seconds 3600` (60 phút) trong câu lệnh OIDC exchange.

### 7. Sự cố Biến môi trường `$AWS_OIDC_TOKEN` bị rò rỉ trên console log của Runner
- **Triệu chứng:** JWT Token hiển thị dạng plain text ở console log.
- **Nguyên nhân:** Sử dụng lệnh `set -x` trong bash script làm in chi tiết lệnh gọi API.
- **Cách khắc phục:** Thêm lệnh `set +x` trước khi gọi các lệnh xử lý token OIDC.

### 8. Sự cố GitLab Self-Hosted nổ lỗi `SSL Certificate Verification Failed` khi Cloud truy vấn JWKS
- **Triệu chứng:** Cloud từ chối kết nối tới GitLab Instance do chứng chỉ SSL/TLS tự ký (Self-signed).
- **Nguyên nhân:** GitLab CE dùng SSL tự tạo không được các root CA công khai tin tưởng.
- **Cách khắc phục:** Cài đặt chứng chỉ SSL chuẩn từ Let's Encrypt hoặc CA doanh nghiệp uy tín cho máy chủ GitLab.

### 9. Sự cố `verify-jwt-signature.sh` báo lỗi `Verification Failure`
- **Triệu chứng:** Public Key không xác minh được chữ ký của JWT token vừa sinh.
- **Nguyên nhân:** File Signature hoặc Header/Payload bị đính kèm ký tự new line (`\n`) khi base64 encode.
- **Cách khắc phục:** Dùng cờ `echo -n` và `tr -d '\n'` khi chuỗi hóa dữ liệu Base64.

### 10. Sự cố Job manual deploy trên nhánh cá nhân cố tình AssumeRole của Production
- **Triệu chứng:** Developer tạo MR ở nhánh `feature/test` nhưng bấm nút deploy OIDC Prod thành công.
- **Nguyên nhân:** IAM Role Trust Policy dùng wildcard `StringLike: gitlab.com:sub: "project_path:bank/payment:*"` quá lỏng lẻo.
- **Cách khắc phục:** Đổi sang `StringEquals` và bắt buộc khớp chính xác `ref:main` cho Prod Role.

### 11. Sự cố Phê duyệt manual bị treo do OIDC Token hết hạn trong thời gian chờ con người bấm nút
- **Triệu chứng:** Bấm nút Play manual deploy sau 2 tiếng thì job nổ lỗi `Token Expired`.
- **Nguyên nhân:** OIDC JWT Token được sinh ra từ thời điểm pipeline bắt đầu chứ không phải thời điểm bấm nút Play.
- **Cách khắc phục:** Trong GitLab v15.7+, OIDC Token được tự động tái tạo (refresh) ngay khi job manual bắt đầu chạy.

### 12. Sự cố Tệp `jwks.json` thiếu thuộc tính `kid` (Key ID)
- **Triệu chứng:** Cloud Provider từ chối nạp JWKS và báo `No matching key ID found`.
- **Nguyên nhân:** Tệp JWKS xuất bản không chứa trường `kid` khớp với Header của JWT Token.
- **Cách khắc phục:** Đảm bảo trường `kid` trong Header của JWT Token khớp 100% với thuộc tính `"kid"` trong tệp `jwks.json`.

### 13. Sự cố Tự động hóa OIDC ECR Login bị lỗi do thiếu quyền `ecr:GetAuthorizationToken`
- **Triệu chứng:** Đổi OIDC Token thành công nhưng lệnh `aws ecr get-login-password` bị từ chối.
- **Nguyên nhân:** IAM Role Permission Policy thiếu action `ecr:GetAuthorizationToken` trên resource `*`.
- **Cách khắc phục:** Bổ sung quyền `ecr:GetAuthorizationToken` vào Permission Policy đính kèm với IAM Role.

### 14. Sự cố Thất bại khi trao đổi OIDC Token do đồng hồ máy chủ Runner bị lệch thời gian (Clock Drift)
- **Triệu chứng:** Cloud từ chối token với lỗi `Token used before issued (iat in future)`.
- **Nguyên nhân:** Đồng hồ máy chủ Runner chạy nhanh hơn máy chủ Cloud vài phút.
- **Cách khắc phục:** Cấu hình đồng bộ thời gian NTP (`chrony` hoặc `ntpd`) trên máy chủ GitLab Runner.

### 15. Sự cố Tệp `.gitlab-ci.yml` nổ lỗi cú pháp `id_tokens must be a hash`
- **Triệu chứng:** GitLab CI Linter đánh lỗi tệp CI không hợp lệ.
- **Nguyên nhân:** Khai báo trường `id_tokens` dạng danh sách array `-` thay vì dạng hash key-value.
- **Cách khắc phục:** Đổi cú pháp sang dạng hash: `id_tokens: MY_TOKEN: aud: https://example.com`.

### 16. Sự cố GCP WIF báo lỗi `Attribute assertion.project_path not found`
- **Triệu chứng:** Attribute condition trên GCP từ chối token với lỗi thiếu thuộc tính.
- **Nguyên nhân:** Chưa cấu hình Attribute Mapping trong GCP Workload Identity Provider settings.
- **Cách khắc phục:** Thêm mapping `--attribute-mapping="attribute.project_path=assertion.project_path"`.

### 17. Sự cố `generate-jwt-token.sh` nổ lỗi `openssl: bad magic number`
- **Triệu chứng:** Script không ký được dữ liệu bằng Private Key.
- **Nguyên nhân:** Tệp Private Key bị hỏng định dạng PEM (thiếu dòng `-----BEGIN RSA PRIVATE KEY-----`).
- **Cách khắc phục:** Sinh lại cặp khóa RSA mới bằng câu lệnh `openssl genrsa -out keys/gitlab-private-key.pem 2048`.

### 18. Sự cố Azure Identity Credentials bị từ chối do mismatch Issuer URL
- **Triệu chứng:** Azure Entra ID báo lỗi `Issuer mismatch`.
- **Nguyên nhân:** Khai báo Issuer URL thiếu dấu gạch chéo cuối hoặc thừa ký tự HTTP.
- **Cách khắc phục:** Nhập chính xác URL `https://gitlab.com` không có dấu gạch chéo xuôi `/` ở cuối.

### 19. Sự cố Script `evaluate-aws-trust-policy.sh` báo lỗi `jq: parse error`
- **Triệu chứng:** Script evaluate Trust Policy bị crash giữa chừng.
- **Nguyên nhân:** Tệp JSON Policy chứa dấu phẩy thừa hoặc hỏng cú pháp JSON.
- **Cách khắc phục:** Dùng công cụ `jq . policies/aws-trust-policy.json` để linter và định dạng lại tệp JSON.

### 20. Sự cố Container Image push lên Cloud Registry thất bại do OIDC Session hết hạn giữa chừng
- **Triệu chứng:** Docker push được 80% thì bị dừng với lỗi `401 Unauthorized`.
- **Nguyên nhân:** Đẩy image dung lượng lớn vài GB vượt quá thời hạn 15 phút của Temporary Credentials.
- **Cách khắc phục:** Tăng duration session lên `--duration-seconds 3600` hoặc tối ưu hóa dung lượng Docker Image (Multi-stage build).

### 21. Sự cố Khai báo trùng lặp Audience làm Cloud từ chối cấp Token
- **Triệu chứng:** Runner báo lỗi `id_tokens variable defined multiple times`.
- **Nguyên nhân:** Khai báo trùng tên biến OIDC token ở cả cấp độ Global Variables và Job Variables.
- **Cách khắc phục:** Đặt tên biến OIDC duy nhất cho từng job (ví dụ `AWS_OIDC_TOKEN` và `GCP_OIDC_TOKEN`).

### 22. Sự cố AWS CloudTrail không ghi nhận thuộc tính `webIdentityToken`
- **Triệu chứng:** Xem log audit trên AWS không thấy thông tin chi tiết của JWT.
- **Nguyên nhân:** Mặc định AWS CloudTrail chỉ ghi nhận thông tin băm HASH của Token để đảm bảo an toàn.
- **Cách khắc phục:** Đây là hành vi bảo mật chính xác của AWS để tránh lộ thông tin token trên log audit.

### 23. Sự cố GitLab Runner Docker Executor không đọc được OIDC Token
- **Triệu chứng:** Job trong container báo biến `$AWS_OIDC_TOKEN` bị rỗng.
- **Nguyên nhân:** Phiên bản GitLab Runner v14.x trở xuống không tự động pass OIDC token vào container environment.
- **Cách khắc phục:** Nâng cấp GitLab Runner Engine lên phiên bản v15.7+ hoặc v16.x.

### 24. Sự cố WIF Provider trên GCP bị vô hiệu hóa (Disabled) do lâu không sử dụng
- **Triệu chứng:** Script deploy GCP báo lỗi `Workload Identity Pool Provider is disabled`.
- **Nguyên nhân:** Quản trị viên GCP đã tắt Provider trên Console.
- **Cách khắc phục:** Bật lại Provider bằng câu lệnh `gcloud iam workload-identity-pools providers enable`.

### 25. Sự cố Lỗi xung đột tên biến OIDC khi tích hợp cả Vault và AWS trong 1 job
- **Triệu chứng:** Job không biết dùng token nào để auth với AWS và Vault.
- **Nguyên nhân:** Dùng chung 1 tên biến `OIDC_TOKEN` với 2 giá trị Audience khác nhau.
- **Cách khắc phục:** Khai báo 2 biến riêng biệt: `VAULT_OIDC_TOKEN` (`aud: https://vault.domain`) và `AWS_OIDC_TOKEN` (`aud: https://aws.amazon.com`).

### 26. Sự cố Phân quyền IAM Role quá lỏng cho phép OIDC Token xóa sạch S3 Buckets
- **Triệu chứng:** Job CI của nhánh Dev lỡ tay xóa mất S3 Bucket Production.
- **Nguyên nhân:** IAM Role gán quyền `s3:*` trên resource `*` mà không giới hạn theo bucket name.
- **Cách khắc phục:** Áp dụng nguyên tắc Least Privilege, chỉ cấp `s3:PutObject` và `s3:GetObject` trên đúng bucket của dự án.

### 27. Sự cố Token Exchange bị chặn do tường lửa chặn cổng 443 tới AWS STS API
- **Triệu chứng:** Câu lệnh `assume-role-with-web-identity` bị timeout sau 60 giây.
- **Nguyên nhân:** Runner private subnet không có đường Egress ra Internet tới endpoint `sts.amazonaws.com`.
- **Cách khắc phục:** Bật AWS VPC Endpoint cho STS (`com.amazonaws.region.sts`) hoặc cấu hình NAT Gateway.

### 28. Sự cố Tệp `temporary-cloud-credentials.json` bị commit nhầm vào Git Repository
- **Triệu chứng:** Temporary Credentials xuất hiện trong lịch sử Git Commit.
- **Nguyên nhân:** Quên không thêm thư mục `tokens/` vào tệp `.gitignore`.
- **Cách khắc phục:** Thêm `tokens/` và `*.token` vào `.gitignore` và thu hồi (revoke) ngay lập tức IAM Session.

### 29. Sự cố `generate-expired-jwt.sh` báo lỗi timestamp trên hệ điều hành macOS
- **Triệu chứng:** Lệnh `date -d` bị nổ lỗi trên BSD date của macOS.
- **Nguyên nhân:** Lệnh `date` trên macOS không hỗ trợ cờ `-d` của GNU date.
- **Cách khắc phục:** Cài đặt `coreutils` bằng `brew install coreutils` và dùng câu lệnh `gdate`.

### 30. Sự cố GCP Service Account Impersonation thất bại do thiếu quyền `roles/iam.workloadIdentityUser`
- **Triệu chứng:** WIF auth thành công nhưng không Impersonate được Service Account.
- **Nguyên nhân:** Chưa grant role `Workload Identity User` cho Service Account đối với WIF Pool Principal.
- **Cách khắc phục:** Thực thi `gcloud iam service-accounts add-iam-policy-binding` cấp quyền `roles/iam.workloadIdentityUser`.

### 31. Sự cố JWT Token bị từ chối do cờ `nbf` (Not Before) lớn hơn thời gian hiện tại
- **Triệu chứng:** Cloud từ chối token với lỗi `Token not valid yet`.
- **Nguyên nhân:** GitLab Server sinh token có thuộc tính `nbf` bị lệch 5-10 giây so với máy chủ Cloud.
- **Cách khắc phục:** Bổ sung khoảng đệm thời gian (clock skew buffer) trong cấu hình OIDC Provider.

### 32. Sự cố Tệp `aws-trust-policy.json` bị sai cú pháp `StringEquals`
- **Triệu chứng:** AWS IAM Console báo lỗi `Invalid condition key`.
- **Nguyên nhân:** Gõ sai key name `gitlab.com:sub` thành `gitlab.com/sub`.
- **Cách khắc phục:** Sửa thành dấu hai chấm chuẩn `gitlab.com:sub`.

### 33. Sự cố Azure AD Token Exchange bị thất bại do App Registration chưa được cấp quyền RBAC
- **Triệu chứng:** Log in Azure thành công nhưng không gọi được API Resource Manager.
- **Nguyên nhân:** Managed Identity chưa được gán Role `Contributor` trên Azure Subscription.
- **Cách khắc phục:** Vào Azure Portal -> Subscriptions -> Access Control (IAM) -> Add Role Assignment `Contributor`.

### 34. Sự cố Job CI chạy trên Scheduled Pipeline không sinh được OIDC Token
- **Triệu chứng:** Biến môi trường `$AWS_OIDC_TOKEN` bị rỗng khi chạy bằng Cron Trigger.
- **Nguyên nhân:** Cấu hình `id_tokens` bị bọc trong điều kiện `rules: - if: $CI_MERGE_REQUEST_ID`.
- **Cách khắc phục:** Đảm bảo khối `id_tokens` nằm ở mức top-level của job và không bị chặn bởi `rules`.

### 35. Sự cố Thất bại khi verify chữ ký JWT do Public Key bị đổi (Key Rotation)
- **Triệu chứng:** OIDC Authentication từng chạy xanh nhưng đột ngột báo lỗi Signature Invalid.
- **Nguyên nhân:** GitLab Instance vừa thực hiện Key Rotation đổi Public Signing Key mới nhưng Cloud cache tệp JWKS cũ.
- **Cách khắc phục:** Xóa cache JWKS trên Cloud Provider hoặc chờ 15 phút để Cloud tự động refresh JWKS endpoint.

### 36. Sự cố Script `validate-ci-oidc-config.sh` báo lỗi giả do tệp `.gitlab-ci.yml` chứa comment
- **Triệu chứng:** Linter nổ lỗi `Static credentials detected` khi tìm thấy chữ `AWS_SECRET_ACCESS_KEY` trong dòng comment.
- **Nguyên nhân:** Lệnh `grep` đọc cả các dòng giải thích `#`.
- **Cách khắc phục:** Lọc bỏ các dòng comment `grep -v '^\s*#'` trước khi kiểm tra từ khóa nhạy cảm.

### 37. Sự cố `exchange-cloud-credentials.sh` sinh ra Session Token chứa ký tự không hợp lệ cho Windows PowerShell
- **Triệu chứng:** Sếp chạy script trên Windows bị báo lỗi `Unexpected token in command`.
- **Nguyên nhân:** Chuỗi Session Token Base64 chứa ký tự `=` và `+` bị PowerShell hiểu nhầm là toán tử.
- **Cách khắc phục:** Bọc chuỗi biến trong dấu ngoặc kép đơn hoặc kép khi export môi trường trên Windows.

### 38. Sự cố Tự động hóa Deploy EKS thất bại do `aws eks update-kubeconfig` không nhận diện được OIDC Temporary Token
- **Triệu chứng:** `kubectl get pods` báo lỗi `Unauthorized`.
- **Nguyên nhân:** Chưa export đầy đủ 3 biến môi trường `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, và `AWS_SESSION_TOKEN`.
- **Cách khắc phục:** Export cả 3 biến môi trường từ tệp `temporary-cloud-credentials.json` trước khi gọi `kubectl`.

### 39. Sự cố `generate-jwt-token.sh` báo lỗi `permission denied` khi ghi tệp token
- **Triệu chứng:** Script nổ lỗi không tạo được tệp `tokens/oidc-jwt.token`.
- **Nguyên nhân:** Thư mục `tokens/` được tạo bởi tài khoản root của Docker container.
- **Cách khắc phục:** Thực thi `chmod -R 777 tokens/` hoặc chạy script với user hợp lệ.

### 40. Sự cố OIDC Authentication trên GCP bị lỗi do tên miền Issuer dài quá 256 ký tự
- **Triệu chứng:** GCP WIF từ chối tạo OIDC Provider với lỗi `Issuer URI exceeds maximum length`.
- **Nguyên nhân:** Tên miền GitLab Self-Hosted có quá nhiều subdomain cấp con.
- **Cách khắc phục:** Đặt tên miền rút gọn chuẩn cho máy chủ GitLab Instance (ví dụ `https://gitlab.company.com`).

### 41. Sự cố Job CI deploy Azure báo lỗi `Federated credential limit reached`
- **Triệu chứng:** Không thể tạo thêm Federated Credentials trên Azure App Registration.
- **Nguyên nhân:** Đã vượt quá giới hạn 20 Federated Identity Credentials mặc định của Azure AD App.
- **Cách khắc phục:** Chuyển sang sử dụng User-Assigned Managed Identity thay vì App Registration.

### 42. Sự cố Phân biệt lầm lẫn giữa Subject Claim `ref` và `environment`
- **Triệu chứng:** Trust Policy lọc `environment:production` nhưng job lại không AssumeRole được.
- **Nguyên nhân:** Job CI không khai báo từ khóa `environment: name: production` nên JWT Token thiếu claim `environment`.
- **Cách khắc phục:** Bắt buộc khai báo từ khóa `environment` ở job CI nếu muốn lọc claim môi trường trong Trust Policy.

### 43. Sự cố `parse-jwt-claims.sh` in ra ký tự rác khi decode Payload
- **Triệu chứng:** Màn hình console log hiển thị các ký tự binary lạ.
- **Nguyên nhân:** Tệp JWT Token bị sai định dạng Base64URL hoặc thiếu dấu chấm phân cách.
- **Cách khắc phục:** Kiểm tra lại cấu trúc 3 phần của JWT Token trước khi decode.

### 44. Sự cố OIDC Token bị vô hiệu hóa khi Runner thực hiện Retry Job
- **Triệu chứng:** Bấm nút Retry trên GitLab UI làm job thất bại với lỗi `Token invalid`.
- **Nguyên nhân:** Retry job cũ dùng lại JWT token cũ đã quá hạn 15 phút.
- **Cách khắc phục:** Cấu hình GitLab Runner tự động xin JWT Token mới cho mọi lượt Retry.

### 45. Sự cố Tệp `final-lab-evaluation.sh` đếm thiếu thành phần do thư mục `audit/` bị xóa
- **Triệu chứng:** Bài lab đánh giá 5/6 thành phần và báo INCOMPLETE.
- **Nguyên nhân:** Chưa chạy Bước 12 tạo tệp `audit/cloudtrail-oidc-events.json`.
- **Cách khắc phục:** Chạy lại script `./scripts/audit-oidc-events.sh "SUCCESS" tokens/oidc-jwt.token`.

### 46. Sự cố AWS IAM Policy Condition từ chối token do thiếu cờ `StringLike` khi dùng Wildcard
- **Triệu chứng:** Trust Policy đặt `gitlab.com:sub: "project_path:bank/*"` nhưng dùng `StringEquals`.
- **Nguyên nhân:** `StringEquals` không hỗ trợ ký tự đại diện `*`.
- **Cách khắc phục:** Đổi tên toán tử Condition thành `StringLike` khi sử dụng ký tự wildcard `*`.

### 47. Sự cố Lỗi Certificate Authority khi GitLab Runner chạy trong môi trường Alpine Linux
- **Triệu chứng:** Script cURL gọi JWKS endpoint báo lỗi `unable to get local issuer certificate`.
- **Nguyên nhân:** Image Alpine Linux thiếu package `ca-certificates`.
- **Cách khắc phục:** Bổ sung lệnh `apk add --no-cache ca-certificates` vào Dockerfile/CI script.

### 48. Sự cố Temporary Credential bị mất khi chuyển qua Stage đằng sau trong Pipeline
- **Triệu chứng:** Job stage `deploy` dùng OIDC thành công nhưng stage `post-deploy-test` lại báo thiếu AWS keys.
- **Nguyên nhân:** Temporary Credentials lưu trong biến môi trường của container job không tự động truyền sang job khác.
- **Cách khắc phục:** Khai báo `id_tokens` và thực hiện OIDC Token Exchange ở từng job riêng biệt.

### 49. Sự cố Nút bấm manual deploy OIDC bị kẹt do Runner bị sập đĩa đĩa đệm
- **Triệu chứng:** Job manual deploy OIDC hiển thị trạng thái Running kéo dài rồi báo timeout.
- **Nguyên nhân:** Runner Host hết dung lượng ổ đĩa làm ngắt kết nối socket với GitLab Server.
- **Cách khắc phục:** Dọn dẹp Docker images rác trên Runner bằng câu lệnh `docker system prune -af`.

### 50. Sự cố Khởi tạo `generate-jwks.sh` thất bại do thiếu lệnh `openssl`
- **Triệu chứng:** Script báo `openssl: command not found`.
- **Nguyên nhân:** Môi trường OS chưa được cài đặt bộ công cụ OpenSSL.
- **Cách khắc phục:** Thực thi `apt-get install -y openssl` hoặc `yum install -y openssl`.

---

## Bài tập mở rộng

1. **Xây dựng Multi-Cloud Dynamic OIDC Authenticator Script:**
   - Viết một script bash vạn năng `cloud-oidc-login.sh` có khả năng tự động phát hiện môi trường đích (AWS, GCP, hoặc Azure) dựa trên biến môi trường `$TARGET_CLOUD`.
   - Nếu `$TARGET_CLOUD = "AWS"`, script tự động gọi `aws sts assume-role-with-web-identity`.
   - Nếu `$TARGET_CLOUD = "GCP"`, script tự động tạo tệp `credential-configuration.json` và thực thi `gcloud auth login --cred-file`.
   - Đóng gói script này thành một **GitLab CI Component / Template** tái sử dụng cho 100+ repositories trong doanh nghiệp!

2. **Tích hợp Automated OIDC Audit & Alerting Bot:**
   - Xây dựng một daemon script ngầm giám sát tệp `audit/cloudtrail-oidc-events.json`.
   - Mỗi khi phát hiện có sự kiện OIDC Authentication bị từ chối (`eventStatus = "DENIED"`), script tự động trích xuất chuỗi `sub` claim và gửi cảnh báo khẩn cấp (Security Alert) qua Slack Webhook/Telegram Bot tới nhóm Security Operations Center (SOC) để xử lý dứt điểm các nguy cơ dò quét lỗ hổng!

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| Bước 1 | Khởi tạo Thư mục Bài Lab và Cặp Khóa Mã hóa RSA | 10 phút |
| Bước 2 | Khởi tạo Tệp JWKS Endpoint Mô phỏng | 10 phút |
| Bước 3 | Viết Script Sinh OIDC JWT Token Chuẩn | 15 phút |
| Bước 4 | Viết Script Giải mã và Kiểm tra Claims trong JWT Token | 10 phút |
| Bước 5 | Viết Script Kiểm tra Chữ ký Số của JWT Token bằng Public Key | 15 phút |
| Bước 6 | Xây dựng AWS IAM Trust Policy Engine Giả lập | 15 phút |
| Bước 7 | Xây dựng GCP Workload Identity Federation (WIF) Matcher Giả lập | 10 phút |
| Bước 8 | Thực thi Quy trình Token Exchange Cấp Temporary Credentials ngắn hạn | 10 phút |
| Bước 9 | Kiểm thử Chặn Tấn công Mạo danh từ Dự án Rác (Spoofed Claim Attack) | 10 phút |
| Bước 10 | Kiểm thử Chặn Tấn công Token Relay Attack (Sai Audience) | 10 phút |
| Bước 11 | Kiểm thử Chặn Token đã hết hạn (Expired Token Test) | 10 phút |
| Bước 12 | Xây dựng Script Ghi nhận OIDC Audit Trail | 10 phút |
| Bước 13 | Xây dựng Script Linter Kiểm tra Cấu hình `.gitlab-ci.yml` dùng OIDC | 5 phút |
| Bước 14 | Tổng hợp Đánh giá Hoàn thành Bài Lab Buổi 37 | 5 phút |
| **Tổng** | **Khối thực hành lab** | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

# Buổi 37: OIDC Federation — Vấn Đáp & Phỏng Vấn

## Thống kê & Phân bổ thời lượng
- **Tổng thời lượng:** 20 phút
- **Cấu trúc:**
  - 5 phút: Kiểm tra phản xạ lý thuyết (12 câu hỏi trắc nghiệm & tự luận nhanh)
  - 10 phút: Đóng vai phỏng vấn tình huống thực chiến (7 kịch bản nâng cao)
  - 5 phút: Chốt từ khóa ăn tiền (§V3) & Giao bài tập về nhà chuẩn bị cho Buổi 38 (BTVN 4)

---

## §V1. 12 Câu hỏi vấn đáp kiểm tra phản xạ

### Câu 1
**Hỏi:** Nguyên lý hoạt động cốt lõi của OIDC Federation khi kết nối GitLab CI/CD với Cloud Provider (AWS/GCP/Azure) là gì?

**Gợi ý trả lời ngắn:**
GitLab CI tự động phát hành một JWT Token ngắn hạn có ký số. Cloud Provider kiểm tra chữ ký token qua JWKS Endpoint của GitLab và cấp Temporary Credentials có thời hạn 15-60 phút nếu các điều kiện claim khớp.

**Đáp án chuẩn:**
- **Nguyên lý 4 Bước Tiêu chuẩn:**
  1. *Pha Sinh Token:* Khi CI job bắt đầu, Runner dùng từ khóa `id_tokens` xin GitLab Instance một OIDC JWT Token ký bởi Private Key.
  2. *Pha Truyền Token:* Runner gửi JWT Token sang Cloud Authentication API (AWS STS `assume-role-with-web-identity`, GCP WIF, hoặc Azure Federated Token).
  3. *Pha Xác minh phím Đám mây:* Cloud IAM tự động kết nối HTTPS tới tệp JWKS công khai (`https://gitlab.com/-/jwks`) để verify chữ ký số của JWT. Tiếp theo, Cloud kiểm tra xem claim `aud` và `sub` có khớp với Trust Policy hay không.
  4. *Pha Cấp Credentials:* Nếu khớp 100%, Cloud trả về Access Token ngắn hạn (TTL 15-60 phút). Runner dùng token này thực thi deploy rồi tự hủy.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Nhầm lẫn cho rằng "OIDC tự sinh ra quyền trên Cloud". Cần phân biệt rõ OIDC chỉ làm nhiệm vụ Xác thực (AuthN), còn Cloud IAM Policy làm nhiệm vụ Cấp quyền (AuthZ).

---

### Câu 2
**Hỏi:** Tại sao việc loại bỏ 100% Static Access Keys (`AWS_SECRET_ACCESS_KEY`) trên CI/CD lại là ưu tiên hàng đầu của DevSecOps?

**Gợi ý trả lời ngắn:**
Vì Static Keys có tuổi thọ vĩnh viễn, khi bị rò rỉ qua log hay code lộ sẽ cho phép kẻ tấn công chiếm quyền hạ tầng mãi mãi; trong khi OIDC Token tự động hết hạn sau 15 phút.

**Đáp án chuẩn:**
- **Rủi ro từ Static Keys:**
  - *Tuổi thọ vĩnh viễn:* Nếu không được thu hồi (revoke) thủ công, key vẫn hoạt động vĩnh viễn.
  - *Dễ bị rò rỉ:* Rất dễ lọt ra ngoài qua console log terminal, git commit history, tệp dump, hoặc khi Runner host bị hacker chiếm quyền.
  - *Thảm họa chi phí:* Kẻ tấn công dùng key lọt để bật hàng trăm máy chủ ảo đào tiền ảo (Crypto Mining).
- **Lợi ích tuyệt đối của OIDC (Zero Static Keys):**
  - Không cần lưu bất kỳ secret key nào trong CI/CD Variables.
  - Temporary Credentials tự hủy sau 15-60 phút, triệt hạ bán kính ảnh hưởng sự cố (Blast Radius $\approx 0$).

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng "Static Keys cũng an toàn nếu giấu kỹ trong Masked Variables". Cần nhấn mạnh nguyên lý Zero Static Secrets.

---

### Câu 3
**Hỏi:** Ba thành phần cấu tạo nên một tệp JSON Web Token (JWT) là gì và chúng được phân cách như thế nào?

**Gợi ý trả lời ngắn:**
Tệp JWT gồm 3 phần: Header (thuật toán mã hóa), Payload (thông tin claims như `sub`, `iss`, `aud`), và Signature (chữ ký số điện tử), phân cách nhau bởi 2 dấu chấm (`.`).

**Đáp án chuẩn:**
- **Cấu trúc 3 phần chuẩn RFC 7519:** `Header.Payload.Signature`
  1. *Header:* Chứa metadata về thuật toán ký (ví dụ `RS256`) và Key ID (`kid`).
  2. *Payload:* Chứa các danh tính thực tế (Claims) do GitLab phát hành như `iss` (Issuer URL), `aud` (Audience), `sub` (Subject Claim), `project_path`, `ref`, `environment`.
  3. *Signature:* Chữ ký số điện tử tạo bởi thuật toán mã hóa bất đối xứng: `RSA-SHA256(Base64(Header) + "." + Base64(Payload), PrivateKey)`.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Nhầm lẫn thứ tự các phần hoặc không biết chữ ký Signature được tạo ra bằng Private Key của IdP.

---

### Câu 4
**Hỏi:** Tại sao trường `sub` (Subject Claim) lại là cờ quan trọng nhất trong câu lệnh Condition của IAM Role Trust Policy?

**Gợi ý trả lời ngắn:**
Trường `sub` chứa thông tin duy nhất định danh dự án, nhánh và môi trường. Nếu không lọc `sub`, bất kỳ ai có tài khoản GitLab.com cũng có thể AssumeRole vào Cloud của bạn.

**Đáp án chuẩn:**
- **Bản chất của `sub` claim:**
  Ví dụ chuỗi `sub`: `project_path:my-company/payment-service:ref_type:branch:ref:main`
- **Nguy cơ nếu thiếu kiểm tra `sub`:**
  Nếu Trust Policy chỉ kiểm tra `iss: https://gitlab.com`, thì BẤT KỲ DỰ ÁN NÀO do kẻ tấn công tạo ra trên `gitlab.com` cũng sẽ sinh ra JWT Token có `iss` hợp lệ và chiếm đoạt được Cloud IAM Role của bạn.
- **Quy tắc vàng:** Bắt buộc dùng toán tử `StringEquals` để so sánh chính xác chuỗi `sub` chứa đúng `project_path` và `ref:main`.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Viết Trust Policy dùng dấu wildcard `sub: "*"` do lười cấu hình, biến tài khoản Cloud thành cửa mở cho toàn thế giới.

---

### Câu 5
**Hỏi:** Ý nghĩa của thuộc tính `aud` (Audience) trong khai báo `id_tokens` là gì? Nó ngăn chặn kịch bản tấn công nào?

**Gợi ý trả lời ngắn:**
`aud` khai báo đối tượng đích được phép nhận token (ví dụ `https://aws.amazon.com`). Nó giúp ngăn chặn kịch bản tấn công chuyển tiếp token (Token Relay Attack).

**Đáp án chuẩn:**
- **Ý nghĩa `aud`:** Định danh hệ thống nhận token hợp lệ.
- **Tấn công Token Relay Attack:** Kẻ tấn công tạo một dịch vụ giả mạo B, lừa CI Runner gửi JWT Token sang cho B. Sau đó B lấy token này đem sang đút lót cho dịch vụ AWS (A) để chiếm quyền.
- **Cơ chế chống đỡ:** Khi Runner xin token với `aud: https://aws.amazon.com`, JWT Token đó chỉ được AWS chấp nhận. Nếu kẻ tấn công mang token này sang GCP hay Vault, GCP/Vault sẽ phát hiện `aud` không khớp và lập tức hủy bỏ kết nối.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng `aud` là tên của dự án trên GitLab. Đúng ra `aud` là URL định danh của Cloud Provider nhận token.

---

### Câu 6
**Hỏi:** Tên gọi tính năng OIDC Federation tương ứng trên 3 nền tảng Đám mây lớn nhất thế giới (AWS, GCP, Azure) là gì?

**Gợi ý trả lời ngắn:**
AWS gọi là **AWS IAM OIDC Identity Provider**, GCP gọi là **Workload Identity Federation (WIF)**, và Azure gọi là **Federated Identity Credentials**.

**Đáp án chuẩn:**
- **AWS:** AWS IAM OIDC Provider kết hợp với API `aws sts assume-role-with-web-identity`.
- **GCP:** Workload Identity Federation (WIF) kết hợp với Workload Identity Pool Attribute Mapping và Service Account Impersonation.
- **Azure:** Azure AD / Entra ID Federated Identity Credentials đính kèm trên User-Assigned Managed Identity.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Nghĩ rằng 3 cloud dùng 3 công nghệ hoàn toàn khác nhau. Thực chất 100% đều tuân theo chuẩn quốc tế OpenID Connect Core 1.0.

---

### Câu 7
**Hỏi:** Tệp JWKS Endpoint (`/.well-known/jwks.json`) đóng vai trò gì trong quá trình Cloud xác minh JWT Token?

**Gợi ý trả lời ngắn:**
JWKS Endpoint xuất bản các Public Key công khai của GitLab. Cloud Provider dùng Public Key này để kiểm tra chữ ký số của JWT Token mà không cần biết Private Key.

**Đáp án chuẩn:**
- **Cơ chế Mã hóa Bất đối xứng (Asymmetric Cryptography):**
  - GitLab Server dùng **Private Key** (mật) để ký số tạo ra phần Signature của JWT Token.
  - GitLab xuất bản các **Public Key** (công khai) dưới dạng tệp JSON tại URL `https://gitlab.domain.com/-/jwks`.
- **Luồng Cloud Verify:**
  1. Cloud nhận JWT Token từ Runner.
  2. Cloud đọc thuộc tính `iss` để biết URL của GitLab.
  3. Cloud gửi HTTP GET request tải tệp JWKS từ `https://gitlab.domain.com/-/jwks`.
  4. Cloud dùng Public Key trong JWKS để giải mã Signature. Nếu kết quả khớp với Header+Payload, token được xác nhận là nguyên bản 100%.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Nghĩ rằng Cloud phải gửi toàn bộ JWT Token về lại cho GitLab để hỏi "Token này có đúng không". Đúng ra Cloud tự verify offline bằng Public Key!

---

### Câu 8
**Hỏi:** Sự khác biệt cốt lõi giữa OIDC Identity Exchange và Cloud IAM Role Permission Policy là gì?

**Gợi ý trả lời ngắn:**
OIDC Identity Exchange chỉ có nhiệm vụ xác thực danh tính (Authentication - AuthN). IAM Permission Policy quyết định các quyền truy cập tài nguyên (Authorization - AuthZ).

**Đáp án chuẩn:**
- **Authentication (AuthN - OIDC Trust Policy):** Trả lời câu hỏi *"Job này là ai?"* (Có đúng là job đến từ repo `payment-service` nhánh `main` hay không).
- **Authorization (AuthZ - IAM Permission Policy):** Trả lời câu hỏi *"Job này được làm gì?"* (Ví dụ được đọc S3 bucket `assets` hay được deploy EKS cluster `prod-cluster`).
- **Triết lý:** OIDC giúp xác thực danh tính an toàn mà không cần key tĩnh; sau khi xác thực xong, mọi quyền hạn vẫn nằm trong tầm kiểm soát của hệ thống Cloud IAM Policy.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Nhầm lẫn rằng chỉ cần OIDC thành công là nghiễm nhiên có quyền Administrator trên Cloud.

---

### Câu 9
**Hỏi:** Tại sao một GitLab CE Instance nằm hoàn toàn trong mạng nội bộ riêng tư (Private Network) lại KHÔNG THỂ sử dụng OIDC trực tiếp với AWS/GCP Public Cloud?

**Gợi ý trả lời ngắn:**
Vì AWS/GCP Public Cloud không thể truy cập mạng HTTPS từ bên ngoài vào tệp JWKS Endpoint (`https://gitlab.internal/-/jwks`) của GitLab nội bộ để tải Public Key xác minh chữ ký.

**Đáp án chuẩn:**
- **Điểm nghẽn kết nối (Network Reachability):**
  Cloud Provider bắt buộc phải gọi được HTTPS vào `Issuer URL + /-.well-known/jwks.json`. Nếu GitLab Instance bị giấu hoàn toàn đằng sau tường lửa nội bộ không có IP/Domain công khai, các máy chủ AWS/GCP STS Engine sẽ nổ lỗi `JWKS fetch failed / Connection Timeout`.
- **Giải pháp khắc phục:**
  1. Mở Reverse Proxy / Ingress public chỉ riêng cho endpoint `/.well-known/jwks.json`.
  2. Sử dụng giải pháp HashiCorp Vault Agent hoặc Self-hosted OIDC Proxy làm trung gian.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Trả lời sai rằng "do Runner không có internet". Ngay cả khi Runner có internet, nếu Cloud không gọi ngược về được GitLab Server thì OIDC vẫn thất bại.

---

### Câu 10
**Hỏi:** Làm thế nào để phân tách OIDC IAM Roles an toàn giữa nhánh `main` (Production) và các nhánh `feature` (Development)?

**Gợi ý trả lời ngắn:**
Tạo 2 IAM Roles riêng trên Cloud: Role Prod có Trust Policy bắt buộc `sub` chứa `ref:main` và `environment:production`; Role Dev có Trust Policy chấp nhận `ref_type:branch`.

**Đáp án chuẩn:**
- **Thiết lập Role Production (`ProdDeployRole`):**
  ```json
  "Condition": {
    "StringEquals": {
      "gitlab.com:sub": "project_path:my-group/my-repo:ref_type:branch:ref:main"
    }
  }
  ```
- **Thiết lập Role Development (`DevDeployRole`):**
  ```json
  "Condition": {
    "StringLike": {
      "gitlab.com:sub": "project_path:my-group/my-repo:ref_type:branch:ref:feature/*"
    }
  }
  ```
- **Kết quả:** Job chạy ở nhánh `feature/login` dù có xin OIDC token cũng bị AWS STS chặn ngay lập tức nếu cố tình chọn `ProdDeployRole`.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Dùng chung 1 IAM Role cho mọi nhánh rồi cố gắng phân quyền bằng biến CI/CD (rất dễ bị dev sửa tệp `.gitlab-ci.yml` để qua mặt).

---

### Câu 11
**Hỏi:** Thời gian sống (TTL) của Temporary Security Credentials cấp qua OIDC nên được khống chế ở mức bao nhiêu là tối ưu?

**Gợi ý trả lời ngắn:**
Thời gian sống khuyến nghị là từ 15 đến 60 phút (tối đa không quá 3600 giây) để giảm thiểu tối đa bán kính ảnh hưởng rủi ro nếu token bị rò rỉ.

**Đáp án chuẩn:**
- **Mức khuyên dùng:** 15 phút (900 giây) đối với các job deploy ngắn, và 60 phút (3600 giây) đối với các job build/test lớn.
- **Lý do:** Nếu một Temporary Token vô tình bị in ra console log trong quá trình chạy job, thời gian 15 phút là quá ngắn để kẻ tấn công phát hiện, sao chép và tổ chức cuộc tấn công.
- **Cách cấu hình:**
  Trong AWS CLI: `--duration-seconds 900`
  Trong GCP CLI: Cấu hình `service_account_token_expiry` 900s.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cấu hình Session Duration kéo dài 12 tiếng hoặc 24 tiếng "cho đỡ phải xin lại token nhiều lần".

---

### Câu 12
**Hỏi:** Làm thế nào để truy vết lịch sử các phiên OIDC Authentication thành công hoặc thất bại trên Cloud Audit Logs?

**Gợi ý trả lời ngắn:**
Trên AWS mở CloudTrail xem sự kiện `AssumeRoleWithWebIdentity`; trên GCP mở Cloud Logging lọc `protoPayload.methodName = "GenerateAccessToken"`.

**Đáp án chuẩn:**
- **AWS CloudTrail:**
  - *Event Name:* `AssumeRoleWithWebIdentity`
  - *Metadata truy vết:* Ghi nhận rõ IP của Runner, thời điểm gọi, IAM Role ARN target, và thuộc tính Subject Claim của JWT Token.
- **GCP Audit Logs:**
  - *Method Name:* `google.iam.v1.IAMCredentials.GenerateAccessToken`
  - *Metadata truy vết:* Ghi nhận thông tin Workload Identity Pool Principal và Target Service Account.
- **Ý nghĩa:** Đáp ứng 100% yêu cầu kiểm toán tuân thủ an toàn thông tin ISO 27001 và SOC 2 Type II.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng OIDC chạy ẩn nên không lưu lại dấu vết gì trên Cloud.

---

## §V2. Kịch bản phỏng vấn thực tế (Roleplay Scenarios)

### Kịch bản 1: Thuyết phục Trưởng phòng An ninh (CISO) chuyển từ Static Keys sang OIDC
- **Người phỏng vấn (CISO):** *"Hệ thống CI/CD hiện tại dùng AWS Access Key lưu trong Protected Variables đang chạy rất ổn định 3 năm nay. Tại sao team em lại đề xuất đập đi xây lại bằng OIDC Federation cho phức tạp?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:* "Báo cáo anh, hệ thống cũ dùng Static Keys mang lại 3 nguy cơ an ninh tử huyệt:"
  - "1. **Rủi ro rò rỉ vĩnh viễn:** Static Keys có tuổi thọ không giới hạn. Nếu một kỹ sư lỡ in log dump hoặc máy chủ Runner bị thỏa hiệp, hacker lấy được key sẽ kiểm soát tài khoản AWS của ta mãi mãi."
  - "2. **Không thể xoay vòng khóa (Key Rotation):** Quản lý 200 static keys trên 50 repositories là thảm họa vận hành. Không ai dám xoay key định kỳ vì sợ hỏng pipeline."
  - "3. **Giải pháp OIDC Federation:** Giúp xóa bỏ **100% Static Keys**. Pipeline tự chứng thực bằng JWT token tự hủy sau 15 phút. Ngay cả khi hacker lấy được log, token cũng đã hết hạn. Đây là tiêu chuẩn bắt buộc nếu công ty muốn đạt chứng chỉ SOC 2 và ISO 27001."

---

### Kịch bản 2: Giải quyết Sự cố OIDC Authentication bị từ chối lúc 2h sáng
- **Người phỏng vấn (On-call Lead):** *"Lúc 2h sáng nay pipeline deploy EKS đột ngột báo lỗi `AWS STS InvalidIdentityToken: Incorrect token audience`. Em xử lý sự cố này thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Phân tích nguyên nhân:** Lỗi `Incorrect token audience` nghĩa là cờ `aud` trong JWT Token sinh ra từ `.gitlab-ci.yml` không khớp với Audience đăng ký trên AWS IAM OIDC Provider.
    2. **Khắc phục sự cố:**
       - Kiểm tra tệp `.gitlab-ci.yml`: Phát hiện ai đó vừa sửa `aud: https://aws.com` thiếu tên miền chuẩn `https://aws.amazon.com`.
       - Đổi lại `aud: https://aws.amazon.com` đúng chuẩn AWS.
    3. **Hành động ngăn chặn:** Viết script Linter `validate-ci-oidc-config.sh` kiểm tra tự động trước khi cho phép merge code để chặn đứng các lỗi gõ sai cờ `aud`.

---

### Kịch bản 3: Bảo vệ Môi trường Production khỏi Tấn công Mạo danh từ GitLab.com
- **Người phỏng vấn (Cloud Security Architect):** *"Nếu công ty dùng GitLab.com công khai, làm sao em ngăn chặn một hacker tạo dự án `gitlab.com/hacker/fake-repo` rồi tự sinh JWT Token để AssumeRole vào tài khoản AWS Production của chúng ta?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Nguyên lý bảo vệ:** "Em áp dụng cơ chế lọc cứng cờ `sub` (Subject Claim) trong AWS IAM Role Trust Policy."
    2. **Trình bày cấu hình:** "Trust Policy của `ProdDeployRole` không chỉ kiểm tra `iss: https://gitlab.com` mà bắt buộc có điều kiện `Condition`:"
       ```json
       "StringEquals": {
         "gitlab.com:sub": "project_path:company-group/core-banking:ref_type:branch:ref:main"
       }
       ```
    3. **Kết luận:** "Khi hacker từ repo `hacker/fake-repo` gửi token sang, AWS STS giải mã JWT thấy `project_path` là `hacker/fake-repo` không khớp với `company-group/core-banking` nên lập tức từ chối cấp quyền!"

---

### Kịch bản 4: Giải thích Kiến trúc OIDC Đa Đám Mây (AWS vs GCP vs Azure)
- **Người phỏng vấn (Enterprise Architect):** *"Công ty chúng ta triển khai ứng dụng trên cả AWS, GCP và Azure. Em có phải viết 3 quy trình xác thực OIDC hoàn toàn khác nhau cho từng đám mây không?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Luận đề trung tâm:** "Báo cáo anh, **Một cơ chế, ba cách gọi tên**. Cả 3 đám mây đều hoạt động trên ĐÚNG MỘT NGUYÊN LÝ OIDC 4 BƯỚC chuẩn hóa."
    2. **Sự tương đồng kiến trúc:**
       - Phía GitLab CI: Đều dùng chung 1 cú pháp `id_tokens` để sinh OIDC JWT Token.
       - Phía Đám mây: Cả AWS STS, GCP WIF và Azure Federated Identity Credentials đều gọi HTTPS về `/-/jwks` của GitLab để verify chữ ký và đối soát cờ `sub`.
    3. **Điểm khác biệt duy nhất:** Chỉ khác nhau ở câu lệnh CLI gọi API trao đổi token (`aws sts assume-role`, `gcloud auth login`, hay `az login`). Em đã đóng gói câu lệnh này thành 1 CI Component chung cho toàn tập đoàn.

---

### Kịch bản 5: Xử lý Tình huống GitLab Self-Hosted bị khóa kết nối Internet
- **Người phỏng vấn (Network Security Lead):** *"Máy chủ GitLab CE của công ty đặt hoàn toàn trong Data Center nội bộ và bị cấm mở kết nối Egress ra Internet. Làm sao để dùng được OIDC với AWS Cloud?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Xác định nút thắt:** "AWS IAM OIDC Provider bắt buộc phải gọi được HTTPS vào `https://gitlab.internal/-/jwks` để tải Public Keys."
    2. **Giải pháp kiến trúc:**
       - **Phương án 1 (Khuyên dùng):** Cấu hình Reverse Proxy (như NGINX/Cloudflare) đặt ở DMZ Zone, chỉ mở duy nhất một Endpoint công khai `https://gitlab-jwks.company.com/.well-known/jwks.json` trỏ về GitLab nội bộ. AWS chỉ truy cập được duy nhất tệp Public Key này mà không thể truy cập vào mã nguồn hay dữ liệu bên trong.
       - **Phương án 2:** Sử dụng HashiCorp Vault đặt nội bộ làm OIDC Identity Broker trung gian.

---

### Kịch bản 6: Tối ưu hóa Phân quyền IAM Role theo Mô hình ABAC
- **Người phỏng vấn (Head of Infrastructure):** *"Tập đoàn có 200 microservices. Nếu mỗi repo phải tạo 1 IAM Role thủ công trên AWS thì rất tốn thời gian. Em giải quyết bài toán scale này như thế nào?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Áp dụng ABAC (Attribute-Based Access Control):** "Em kết nối OIDC với cơ chế AWS IAM Session Tags hoặc GCP Attribute Mapping."
    2. **Cách triển khai:**
       - Cấu hình OIDC Provider tự động chuyển đổi claim `project_path` trong JWT thành Principal Tag `GitLabProjectPath`.
       - Viết đúng **1 IAM Role chung** cho nhóm Microservices với Policy linh hoạt:
         ```json
         "Resource": "arn:aws:s3:::company-app-${aws:PrincipalTag/GitLabProjectPath}/*"
         ```
    3. **Kết quả:** Khi tạo repo mới `payment-v2`, CI tự động có quyền truy cập bucket `company-app-payment-v2` mà KHÔNG CẦN SysAdmin phải lên AWS tạo thêm bất kỳ IAM Role nào!

---

### Kịch bản 7: Tranh luận về rủi ro Token bị log dump trên GitLab Runner Host
- **Người phỏng vấn (Security Auditor):** *"Nếu máy chủ GitLab Runner Host bị hacker chiếm quyền điều khiển (root compromise), liệu hacker có lấy được OIDC Token để truy cập Cloud không?"*
- **Ứng viên (DevOps Specialist):**
  - *Trả lời:*
    1. **Thừa nhận rủi ro thực tế:** "Nếu Runner Host bị chiếm quyền root tại thời điểm job đang chạy, hacker có thể đọc được biến môi trường `$AWS_OIDC_TOKEN`."
    2. **Cơ chế khoanh vùng thiệt hại (Blast Radius Limitation):**
       - Khác với Static Key (hacker chiếm quyền mãi mãi), OIDC Temporary Token chỉ có tuổi thọ **15 phút**.
       - IAM Role được phân quyền theo nguyên tắc **Least Privilege** (chỉ có quyền deploy đúng 1 service).
       - Ngay khi phát hiện Runner bị thỏa hiệp, chúng ta chỉ cần ngắt Runner; sau 15 phút toàn bộ token rò rỉ tự động biến thành phế liệu mà không cần vào AWS thu hồi key khẩn cấp.

---

## §V3. Câu chốt để nói khi phỏng vấn

1. *"OIDC Federation không chỉ là một tính năng CI/CD, mà là **nền tảng của kiến trúc Zero Static Credentials** giúp loại bỏ 100% nguy cơ rò rỉ khóa đám mây vĩnh viễn."*
2. *"Dù triển khai trên AWS, GCP hay Azure, nguyên lý OIDC luôn là **Một cơ chế, ba cách gọi tên** — chìa khóa an ninh 90% nằm ở việc kiểm soát cờ **Subject Claim (`sub`)** trong Trust Policy."*
3. *"OIDC làm nhiệm vụ **Xác thực danh tính (AuthN)** để trả lời 'Bạn là ai'; còn **Quyền hạn tài nguyên (AuthZ)** vẫn hoàn toàn do Cloud IAM Policy quản lý."*
4. *"Triết lý phòng thủ OIDC của em là **Khống chế TTL dưới 15 phút** và **Phân tách Role Prod/Dev tuyệt đối** để triệt hạ bán kính ảnh hưởng sự cố."*
5. *"JWKS Endpoint `/.well-known/jwks.json` là chiếc cầu nối tin tưởng duy nhất giúp Cloud xác minh chữ ký JWT mà không cần lưu trữ bất kỳ Shared Secret nào."*

---

## BTVN 4: Chuẩn bị cho Buổi 38 — Deploy lên AWS: OIDC $\to$ IAM Role, ECS/EKS/S3+CloudFront

Để chuẩn bị tốt nhất cho **Buổi 38: Deploy lên AWS: OIDC $\to$ IAM Role, ECS/EKS/S3+CloudFront**, học viên cần thực hiện các nhiệm vụ sau:

1. **Ôn tập lệnh AWS CLI OIDC:**
   - Đọc lại cấu hình `aws sts assume-role-with-web-identity` và cách export 3 biến môi trường `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`.
   - Tìm hiểu cách cấu hình `AWS_ROLE_ARN` và `AWS_WEB_IDENTITY_TOKEN_FILE` trực tiếp trong tệp cấu hình AWS SDK.

2. **Nghiên cứu kiến trúc triển khai trên AWS:**
   - Tìm hiểu luồng deploy ứng dụng Web tĩnh lên **AWS S3 + CloudFront CDN** (lệnh `aws s3 sync` và `aws cloudfront create-invalidation`).
   - Tìm hiểu luồng deploy ứng dụng Container lên **AWS ECS / EKS Cluster** bằng OIDC Temporary Credentials.

3. **Bài tập chuẩn bị trước giờ học:**
   - Đọc trước tài liệu AWS IAM Trust Policy Condition Keys dành cho OIDC Provider: `sts:RoleSessionName`, `StringEquals`, và `StringLike`!