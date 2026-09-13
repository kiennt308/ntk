---
layout: post
title: "[Bài 35] Kiểm Tra Năng Lực Thực Chiến Giữa Kỳ: Đánh Giá & Tối Ưu Hệ Thống CI/CD Pipeline Phức Tạp End-to-End"
date: 2026-09-12 03:50:00 +0700
categories: [GitLab]
tags:
  - GitLab
  - CICD
  - DevSecOps
  - Pipelines
  - Automation
  - Part-35
series: "GitLab CI/CD & DevSecOps Platform Mastery"
series_order: 35
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80"
summary: "[GitLab CI/CD P.35] Hướng dẫn chuyên sâu Kiểm Tra Năng Lực Thực Chiến Giữa Kỳ: Đánh Giá & Tối Ưu Hệ Thống CI/CD Pipeline Phức Tạp End-to-End: Khám phá toàn diện kiến trúc kỹ thuật tầng thấp, thực hành Lab chi tiết từng bước, phân tích tối ưu hiệu năng và bộ câu hỏi phỏng vấn chuyên sâu."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Kiểm Tra Năng Lực Thực Chiến Giữa Kỳ: Đánh Giá & Tối Ưu Hệ Thống CI/CD Pipeline Phức Tạp End-to-End."
  - "Thiết kế CI/CD Pipeline chuẩn Enterprise với kiến trúc DAG, tối ưu hóa thời gian build và caching hiệu quả."
  - "Bảo mật chuỗi cung ứng phần mềm với SAST/DAST, Container Scanning và OIDC Authentication."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 35] KIỂM TRA NĂNG LỰC THỰC CHIẾN GIỮA KỲ: ĐÁNH GIÁ & TỐI ƯU HỆ THỐNG CI/CD PIPELINE PHỨC TẠP END-TO-END

Trong kỷ nguyên **DevOps, DevSecOps và Cloud Native Engineering**, **GitLab CI/CD** được công nhận là một trong những nền tảng tự động hóa tích hợp liên tục và phân phối liên tục (CI/CD) hoàn chỉnh, mạnh mẽ và được tin dùng nhất trong các doanh nghiệp quy mô lớn. Không chỉ dừng lại ở các pipeline tuần tự cơ bản, việc vận hành GitLab CI/CD ở cấp độ Production đòi hỏi kỹ sư phải làm chủ kiến trúc điều phối phi tuyến tính **DAG (Directed Acyclic Graph)**, cơ chế quản trị **Autoscaling Runners**, tối ưu hóa **Caching đa tầng**, xác thực không khóa **Keyless OIDC**, bảo mật chuỗi cung ứng phần mềm **SLSA & SBOM** cùng các chính sách **Quality & Security Gates** tự động.

Bài viết chuyên sâu này sẽ đồng hành cùng bạn mổ xẻ toàn diện bức tranh kiến trúc, phân tích các đánh đổi kỹ thuật thực chiến (Engineering Trade-offs), cung cấp hướng dẫn thực hành Lab chi tiết từng bước và bộ câu hỏi phỏng vấn chuyên sâu chuẩn DevOps Lead / DevSecOps Architect.

---

## 1. Bản Chất Kiến Trúc & Cơ Chế Vận Hành Tầng Thấp

---





| STT | Câu hỏi ôn tập | Đáp án chi tiết thực chiến |
|---|---|---|
| 1 | Security Quality Gate khác với Functional Test Gate ở điểm nào? | Gate an ninh đánh giá ma trận rủi ro (Risk Severity/CVSS), chính sách tuân thủ tuân thủ pháp lý và nợ an ninh thay vì chỉ kết quả UnitTest đúng/sai nhị phân. Gate an ninh có thể dừng pipeline ngay lập tức dù UnitTest pass 100% nếu phát hiện rủi ro Critical RCE hoặc rò rỉ Secret. |
| 2 | Tại sao không được hardcode ngưỡng an ninh trong tệp `.gitlab-ci.yml` local? | Vì dễ bị developer tự ý sửa đè bypass gate khi bị ép deadline, đồng thời làm phân tán quy định an ninh. Khi công ty cần thay đổi chính sách toàn bộ 100 microservices, việc hardcode làm Security Team tốn công sửa 100 repositories thay vì điều chỉnh tập trung tại Group level. |
| 3 | Tệp allowlist (ví dụ `.trivyignore`) bắt buộc phải chứa những metadata gì? | Bắt buộc có CVE ID, ngày hết hạn (Expiration Date YYYY-MM-DD), tên người phê duyệt Security Lead (@username) và ticket JIRA đính kèm. Thiếu bất kỳ trường nào trong 4 trường này tệp ignore sẽ bị script audit tự động đánh nổ lỗi build. |
| 4 | Làm thế nào để ngăn dev tự thêm `allow_failure: true` vào job scanner? | Sử dụng GitLab Compliance Execution Policies ở cấp độ Group để nạp bắt buộc các tệp template job an ninh từ repository quản trị trung tâm. Tệp template này nằm ngoài tầm kiểm soát chỉnh sửa của Developer và đè thuộc tính `allow_failure: false`. |
| 5 | Cơ chế Emergency Bypass cần đảm bảo điều kiện gì để được chấp nhận? | Phải bọc trong biến Protected & Masked CI Variable `EMERGENCY_SECURITY_BYPASS`, bắt buộc người có thẩm quyền (SecLead/TechLead) kích hoạt, và tự động gửi log audit thời gian thực về kênh Slack Security và hệ thống SIEM để phục vụ hậu kiểm. |

### 0.2. Cầu nối sang bài kiểm tra giữa kỳ 2
**Luận đề trung tâm:**
> *"Bài kiểm tra giữa kỳ 2 không phải là đố mẹo lý thuyết, mà là bài kiểm thử sức bền kỹ thuật — chứng minh bạn có đủ khả năng xây dựng và làm chủ một **hệ thống phòng thủ CI/CD tự động 6 lớp** bảo vệ toàn bộ vòng đời phát triển phần mềm của doanh nghiệp."*

Bài thi giữa kỳ 2 tổng hợp toàn bộ các kỹ thuật đã học từ Buổi 25 đến Buổi 34. Học viên sẽ không triển khai từng công cụ riêng lẻ một cách rời rạc, mà bắt buộc phải kết nối chúng thành một chuỗi xích an ninh hoàn chỉnh. Mỗi stage trong pipeline sẽ sản sinh ra các chứng minh hiện vật (Artifacts) để truyền sang stage đằng sau, và stage cuối cùng (Security Quality Gate) sẽ chịu trách nhiệm thẩm định toàn bộ ma trận rủi ro trước khi nhả cờ cho phép triển khai sản phẩm lên môi trường Production.

**Bảng kết quả các buổi 25–34 tái sử dụng trong bài thi giữa kỳ 2:**

| Buổi | Công nghệ / Kỹ thuật | Sản phẩm hiện vật ứng dụng vào bài thi giữa kỳ | Vai trò trong chuỗi phòng thủ 6 lớp |
|---|---|---|---|
| Buổi 25-27 | Container Security & Hardening | Multi-stage Dockerfile chuẩn Distroless, Non-root user, Cap drop | Đảm bảo Container Image không chứa thành phần dư thừa và không chạy quyền Root. |
| Buổi 28 | SAST & Secret Detection | Job Semgrep & Gitleaks xuất báo cáo JSON/SARIF chuẩn | Lớp 1: Di chuyển an ninh về bên trái (Shift-Left), bắt rò rỉ API Key và lỗi lập trình. |
| Buổi 29 | Dependency Scanning & DAST | OWASP Dependency-Check & ZAP DAST integration | Phát hiện các thư viện phụ thuộc chứa lỗ hổng CVE công khai. |
| Buổi 30 | HashiCorp Vault & OIDC | Vault OIDC JWT Authentication thu thập Dynamic Credential ngắn hạn | Lớp 3: Cấp token tự hủy sau 15-30 phút, loại bỏ 100% secret tĩnh trong biến CI. |
| Buổi 31 | Container Scan & IaC Scan | Trivy Vulnerability Scan & Checkov IaC Policy Enforcement | Lớp 2 & 4: Kiểm tra an ninh tệp Kubernetes Manifest và OS Packages trong Image. |
| Buổi 32 | Supply Chain Security | Syft SBOM (SPDX/CycloneDX) & Cosign Keyless Image Signature | Lớp 5: Xuất danh mục phần mềm và ký số điện tử OIDC chứng thực nguồn gốc SLSA. |
| Buổi 33 | Compliance Audit Pipeline | OPA / Conftest Policy Engine với các tệp quy tắc Rego tập trung | Lớp 6: Kiểm định tính tuân thủ quy tắc doanh nghiệp bằng ngôn ngữ Rego. |
| Buổi 34 | Security Quality Gate | Gate Parser hợp nhất, Allowlist Expiration Audit & Emergency Bypass Log | Lớp 6: Ngắt ngầm pipeline hard-fail và quản lý nợ an ninh có hạn dùng. |

---



| STT | Kỹ năng thực chiến | Hiện vật chứng minh hoàn thành |
|---|---|---|
| 1 | Xây dựng pipeline DevSecOps 6 lớp hoàn chỉnh | Tệp `.gitlab-ci.yml` tích hợp 6 stage an ninh khép kín chạy tự động |
| 2 | Tích hợp Vault OIDC xác thực không dùng secret tĩnh | Job `vault-auth` tự lấy token tạm thời không lỡ lộ Password/API Key |
| 3 | Tự động quét và phát hiện secret trong mã nguồn | Artifact `gitleaks-report.json` phát hiện 100% token nhạy cảm |
| 4 | Kiểm tra an ninh container image và IaC manifest | Kết quả `trivy-report.json` và `checkov-report.json` phân loại theo Severity |
| 5 | Xuất SBOM và Ký số SLSA Provenance Attestation | Tệp `sbom.spdx.json` và chữ ký điện tử Cosign verify thành công trên Registry |
| 6 | Thực thi Policy-as-Code bằng Rego và OPA/Conftest | Bộ quy tắc `.rego` kiểm định tính tuân thủ quy định hạ tầng |
| 7 | Vận hành Multi-stage Security Quality Gate | Script `security-gate.sh` tự động ngắt pipeline khi phát hiện lỗi vượt ngưỡng |
| 8 | Quản lý ngoại lệ có thời hạn và Audit Trail | Tệp `.trivyignore` được audit ngày hết hạn tự động và ghi log bypass khẩn cấp |

---



| Kiến thức / Kỹ năng | Mức độ yêu cầu | Nguồn tự học nếu thiếu |
|---|---|---|
| Cú pháp `.gitlab-ci.yml` nâng cao | Thành thục | Buổi 05 & Buổi 12 (QT 5.1, QT 12.3) |
| Cấu trúc Dockerfile Multi-stage & Non-root | Thành thục | Buổi 25 & Buổi 26 (QT 25.2, QT 26.4) |
| Quét lỗ hổng bằng Trivy & Gitleaks | Thành thục | Buổi 28 & Buổi 31 (QT 28.1, QT 31.2) |
| Cấu hình OIDC JWT với HashiCorp Vault | Hiểu rõ | Buổi 30 (QT 30.3, QT 30.5) |
| Ký số Cosign & Tạo SBOM bằng Syft | Thành thục | Buổi 32 (QT 32.2, QT 32.6) |
| Viết luật Policy-as-Code bằng Rego | Hiểu rõ | Buổi 33 (QT 33.1, QT 33.4) |
| Xây dựng Quality Gate Parser | Thành thục | Buổi 34 (QT 34.1, QT 34.7) |

---





| Thuật ngữ Tiếng Việt | Thuật ngữ Tiếng Anh | Giải thích ý nghĩa thực tế |
|---|---|---|
| Phòng thủ 6 lớp | 6-Layer Defense In Depth | Mô hình bao bọc an ninh 6 giai đoạn từ Code, Secret, IaC, Image, Supply Chain đến Policy Gate. Đảm bảo ứng dụng được bảo vệ đa tầng. |
| Xác thực OIDC liên kết | OIDC Federated Identity | Cơ chế dùng GitLab JWT Token đổi lấy Cloud/Vault Credential ngắn hạn không dùng Password tĩnh. Giúp loại bỏ rò rỉ API Key. |
| Bảng kiểm kê thành phần | Software Bill of Materials (SBOM) | Danh mục chi tiết toàn bộ thư viện, package, dependency và version có trong ứng dụng. Cho phép tra cứu tức thì khi xuất hiện 0-day. |
| Chứng thực nguồn gốc SLSA | SLSA Provenance Attestation | Giấy chứng nhận số xác minh ai build image, từ commit SHA nào và trên runner nào. Đảm bảo tính toàn vẹn và xuất xứ hợp pháp. |
| Ký số không dùng khóa | Keyless Cosign Signing | Kỹ thuật ký chữ ký điện tử lên container image dựa trên OIDC Identity token ngắn hạn. Không yêu cầu quản lý Private Key tĩnh. |
| Chính sách dưới dạng mã | Policy-as-Code (PaC) | Quản lý quy định an ninh bằng mã nguồn Rego để kiểm định tự động bằng OPA/Conftest. Tách biệt logic quản trị khỏi tệp CI/CD local. |
| Cổng kiểm soát chất lượng | Security Quality Gate | Điểm quyết định tự động ngắt hoặc cho phép pipeline đi tiếp dựa trên phân tích ma trận rủi ro. Quyết định dựa trên Severity và CVSS Score. |
| Ngoại lệ có giới hạn | Expiration Allowlist Waiver | Cơ chế tạm bỏ qua CVE đã đánh giá rủi ro có ghi rõ hạn chót sửa chữa và ticket đính kèm. Ngăn chặn nợ an ninh vĩnh viễn. |
| Vệt vết kiểm toán | Audit Trail | Log chi tiết không thể sửa xóa ghi lại ai đã trigger, ai bypass gate và thời điểm thực thi. Phục vụ công tác hậu kiểm sự cố. |
| Nợ an ninh tồn đọng | Accumulated Security Debt | Tổng số lỗ hổng chưa được vá tích tụ theo thời gian gây nguy cơ phá sản an ninh. Cần được dọn dẹp theo lộ trình Sprint. |
| Tỷ lệ báo động giả | False Positive Rate | Phần trăm cảnh báo lỗi do công cụ bắt nhầm gây lãng phí thời gian của lập trình viên. Cần tinh chỉnh bộ rule exclusion. |
| Bỏ qua khẩn cấp | Emergency Security Bypass | Nút bấm giải cứu cho phép vượt Quality Gate khi xảy ra sự cố sập production khẩn cấp. Quản lý bằng Protected Variable. |

---

### 1.1. Tổng quan 12 Quy tắc DevSecOps Nâng cao (10 phút)

**Nguyên lý cốt lõi:** Kiến trúc phòng thủ 6 lớp phải chạy tự động trong mọi pipeline của doanh nghiệp.
**Phát biểu.** Một pipeline DevSecOps đạt chuẩn Enterprise bắt buộc phải triển khai tối thiểu 6 lớp kiểm soát an ninh tự động trải dài từ bước lập trình đến trước bước triển khai production.
**Giải thích cơ chế ngầm:** Tấn công mạng hiện đại không dừng lại ở lỗi source code mà đánh vào toàn bộ chuỗi cung ứng, từ secret bị rò rỉ, cấu hình IaC sai đến container base image độc hại. Nếu chỉ quét 1 hoặc 2 lớp, kẻ tấn công dễ dàng khai thác các điểm mù hạ tầng còn lại để xâm nhập hệ thống.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline chỉ chạy duy nhất job SonarQube hoặc UnitTest rồi bấm deploy thẳng lên Kubernetes mà không hề quét Dockerfile, không tạo SBOM và không ký số image.
**Minh hoạ.**
```yaml
stages:
  - secret-and-sast   # Layer 1: Code Security (Gitleaks + Semgrep)
  - iac-check         # Layer 2: Infrastructure Security (Checkov)
  - vault-auth        # Layer 3: Identity & Secret Access (Vault OIDC)
  - container-build   # Layer 4: Container Security (Multi-stage + Trivy)
  - sbom-provenance   # Layer 5: Supply Chain Security (Syft + Cosign)
  - security-gate     # Layer 6: Policy Governance (OPA + Quality Gate Parser)
```
**Con số chốt:** 6 lớp phòng thủ khép kín.

---

**Nguyên lý cốt lõi:** Tách biệt tuyệt đối quyền hạn giữa Security Governance Team và AppDev Team.
**Phát biểu.** Developer có toàn quyền trên ứng dụng nhưng tuyệt đối không có quyền chỉnh sửa, vô hiệu hóa hoặc bypass các job kiểm tra an ninh ở cấp độ Group.
**Giải thích cơ chế ngầm:** Nếu developer có quyền sửa tệp chính sách an ninh, họ sẽ sẵn sàng xóa luật hoặc tắt scanner khi bị áp lực về deadline release. Sự xung đột lợi ích giữa tiến độ giao hàng và an toàn thông tin bắt buộc phải được giải quyết bằng hạ tầng phân quyền cứng.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tệp quy tắc Rego của OPA hoặc script Quality Gate được lưu trực tiếp trong repository của ứng dụng và cho phép developer tạo Merge Request tự approve.
**Minh hoạ.** Lưu chính sách tại repo `security-governance/compliance-rules` độc lập và dán nhãn Compliance Framework để GitLab Compliance Execution Policy tự động nạp vào các dự án con:
```yaml
# In compliance-group-policy.yml (Locked by Security Team)
include:
  - project: 'security-governance/compliance-rules'
    file: '/templates/security-gate-execution-policy.yml'
```
**Con số chốt:** 0 quyền chỉnh sửa gate cho Dev.

---

**Nguyên lý cốt lõi:** Nguyên tắc Zero-trust Artifact Transfer giữa các Stage Scan và Quality Gate.
**Phát biểu.** Job Security Quality Gate phải trực tiếp parse nội dung các tệp báo cáo JSON artifacts được chuyển giao, không được dựa vào cờ exit status mềm của job trước.
**Giải thích cơ chế ngầm:** Các job scanner có thể bị dev cài cờ `allow_failure: true` hoặc viết script bọc `exit 0` làm giả tín hiệu thành công. Nếu gate chỉ kiểm tra status xanh/đỏ của stage trước, rủi ro bảo mật sẽ bị lọt lưới 100%.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Quality Gate cho qua pipeline chỉ vì stage `scan` hiển thị dấu tích xanh trên giao diện GitLab UI mà không hề kiểm tra sự tồn tại và tính toàn vẹn của tệp JSON báo cáo.
**Minh hoạ.**
```bash
# Script trong job quality-gate: Tự mở file artifact kiểm tra tính hợp lệ
if [ ! -f trivy-report.json ]; then
  echo "[ERROR] Missing Trivy scan report artifact! Job failed immediately."
  exit 1
fi

# Tính toán số lượng CVE Critical trực tiếp từ dữ liệu JSON thô
CRIT_COUNT=$(jq '[.Results[].Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length' trivy-report.json)
echo "Scanned Critical Vulnerabilities Count: $CRIT_COUNT"
```
**Con số chốt:** 100% tự parse JSON Artifacts.

---

**Nguyên lý cốt lõi:** Quản lý tập trung Secret ngắn hạn qua Vault OIDC thay cho Static Masked Variables.
**Phát biểu.** Tất cả các credential kết nối cơ sở dữ liệu, Cloud Provider hay Registry trong pipeline phải được cấp qua HashiCorp Vault OIDC JWT với thời gian sống (TTL) dưới 60 phút.
**Giải thích cơ chế ngầm:** Biến môi trường static dù có Masked vẫn bị rò rỉ qua log đệm, file dump hoặc bị lộ khi runner bị chiếm quyền kiểm soát. Secret ngắn hạn tự hủy khiến rủi ro bị khai thác trộm giảm về gần bằng không.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Khai báo `AWS_SECRET_ACCESS_KEY` hoặc `DB_PASSWORD` trực tiếp trong mục CI/CD Variables của GitLab Project với thời hạn vĩnh viễn không bao giờ xoay vòng.
**Minh hoạ.** Dùng `id_tokens` OIDC trao đổi token với Vault để lấy Dynamic Database Secrets tự hủy sau 15 phút:
```yaml
job-vault-auth:
  id_tokens:
    VAULT_JWT:
      aud: "https://vault.company.internal"
  script:
    - export VAULT_TOKEN=$(curl --request POST --data "{\"jwt\": \"$VAULT_JWT\", \"role\": \"gitlab-runner-role\"}" https://vault.company.internal/v1/auth/jwt/login | jq -r '.auth.client_token')
```
**Con số chốt:** TTL $< 60$ phút cho mọi Dynamic Secret.

---

**Nguyên lý cốt lõi:** Chuẩn hóa báo cáo an ninh theo định dạng SARIF và GitLab Security Schema JSON.
**Phát biểu.** Tất cả các công cụ bảo mật quét mã nguồn, hạ tầng, container đều phải xuất kết quả theo định dạng chuẩn SARIF v2.1.0 hoặc Schema JSON quy định.
**Giải thích cơ chế ngầm:** Định dạng chuẩn giúp gom báo cáo từ 10 công cụ khác nhau về một dashboard duy nhất, hỗ trợ hiển thị trực quan trên Merge Request Widget và giúp script Quality Gate xử lý dữ liệu nhất quán.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Mỗi job scanner xuất file text log thô (`.txt`, `.log`) khiến script gate không thể tự động parse dữ liệu và GitLab UI từ chối hiển thị báo cáo.
**Minh hoạ.** Cấu hình cờ `--format sarif --output report.sarif` trên Semgrep, Trivy và Checkov:
```yaml
semgrep-scan:
  script:
    - semgrep scan --config p/ci --sarif --output gl-sast-report.sarif .
  artifacts:
    reports:
      sast: gl-sast-report.sarif
```
**Con số chốt:** 100% công cụ xuất chuẩn SARIF/JSON.

---

**Nguyên lý cốt lõi:** Quy định bắt buộc ký số Container Image và SLSA Attestation bằng Cosign Keyless.
**Phát biểu.** Mọi Container Image trước khi đẩy lên Production Registry phải được ký số điện tử kèm theo tệp chứng nhận SLSA Provenance bằng Cosign OIDC.
**Giải thích cơ chế ngầm:** Ngăn chặn kẻ tấn công thay thế image nguy hiểm trực tiếp trên Registry (Image Tampering) hoặc bypass bước build của CI để đẩy trực tiếp image lạ vào hạ tầng Kubernetes.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Kubernetes Cluster kéo container image về chạy chỉ dựa vào tag `:latest` hoặc tag chuỗi ngẫu nhiên mà không hề verify chữ ký điện tử Cosign.
**Minh hoạ.** Ký số container bằng OIDC token của GitLab Runner không cần quản lý private key tĩnh:
```bash
cosign sign --yes \
  --oidc-provider gitlab \
  $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```
**Con số chốt:** 100% Production Images có chữ ký số.

---

### 1.2. Quản lý Chính sách và Nợ an ninh trong Pipeline (10 phút)

**Nguyên lý cốt lõi:** Cơ chế ngắt ngầm (Fail-fast) và cảnh báo mềm (Soft-warning) theo cấp độ môi trường.
**Phát biểu.** Cấu hình ngắt pipeline lập tức (`hard-fail`) ở nhánh `main/production` nhưng cho phép cảnh báo mềm (`soft-fail`) ở nhánh `feature/dev`.
**Giải thích cơ chế ngầm:** Giúp lập trình viên không bị chặn tiến độ khi đang code nháp ở nhánh cá nhân, nhưng đảm bảo tuyệt đối không cho code lỗi chui vào production. Đây là chìa khóa để DevSecOps hòa hợp giữa Security và Business Agility.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Bật hard-fail chặn chết pipeline ở tất cả các commit nháp làm dev không thể test tính năng, hoặc bật soft-fail trên nhánh main làm code lỗi lọt lưới.
**Minh hoạ.**
```bash
if [ "$CI_COMMIT_BRANCH" = "main" ]; then
  echo "[POLICY] Strict Hard-Fail Mode Enabled for Production Branch."
  GATE_STRICT=true
else
  echo "[POLICY] Soft-Warning Mode Enabled for Feature Branch."
  GATE_STRICT=false
fi
```
**Con số chốt:** Hard-fail trên Main, Soft-fail trên Feature.

---

**Nguyên lý cốt lõi:** Quy định bắt buộc metadata đối với các dòng Expiration Allowlist Waiver.
**Phát biểu.** Mọi dòng khai báo bỏ qua lỗ hổng trong tệp ignore bắt buộc phải chứa ID lỗ hổng, Ngày hết hạn ISO 8601, Nơi phê duyệt và Ticket JIRA.
**Giải thích cơ chế ngầm:** Tệp ignore không có hạn dùng sẽ biến thành "nghĩa địa giấu lỗi", làm vô hiệu hóa toàn bộ hệ thống Quality Gate theo thời gian và tạo nợ an ninh vĩnh viễn.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Tệp `.trivyignore` chứa hàng chục CVE ID đứng trần trụi mà không có bất kỳ dòng comment giải thích hay ngày hết hạn nào.
**Minh hoạ.** Format chuẩn của 1 entry trong tệp ignore:
```text
# CVE-2023-44487 | Expire: 2026-09-01 | ApprovedBy: @sec-lead | Ticket: SEC-8891
CVE-2023-44487
```
**Con số chốt:** 4 trường metadata bắt buộc cho từng dòng ignore.

---

**Nguyên lý cốt lõi:** Tự động hóa tạo vé sự cố JIRA/ServiceNow khi Quality Gate bị ngắt.
**Phát biểu.** Khi Quality Gate phát hiện lỗi ngắt pipeline trên nhánh chính, hệ thống phải tự động mở Ticket sự cố trên JIRA kèm thông tin đính kèm.
**Giải thích cơ chế ngầm:** Đảm bảo rủi ro an ninh được đưa vào backlog quản lý chính thức, có Assignee chịu trách nhiệm, có thời hạn khắc phục (SLA) và không bị bỏ quên trong log CI.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Pipeline ngắt báo đỏ nhưng không ai biết, lỗi bị lãng quên cho đến khi cận ngày release sản phẩm.
**Minh hoạ.** Script CI gọi JIRA REST API `POST /rest/api/2/issue` truyền các biến `$CI_COMMIT_AUTHOR`, `$CI_PIPELINE_URL` và danh sách CVE vi phạm:
```bash
curl -X POST -H "Content-Type: application/json" \
  -u "$JIRA_USER:$JIRA_API_TOKEN" \
  -d "{\"fields\": {\"project\": {\"key\": \"SEC\"}, \"summary\": \"Quality Gate Failure on $CI_PROJECT_NAME\", \"description\": \"Author: $CI_COMMIT_AUTHOR\nPipeline: $CI_PIPELINE_URL\", \"issuetype\": {\"name\": \"Bug\"}}}" \
  https://jira.company.com/rest/api/2/issue
```
**Con số chốt:** 100% sự cố ngắt gate trên Main được tạo Ticket.

---

**Nguyên lý cốt lõi:** Cơ chế Emergency Bypass có ghi vết Audit Log và cảnh báo thời gian thực về SIEM.
**Phát biểu.** Tính năng Bypass Quality Gate trong trường hợp khẩn cấp phải được quản lý bằng Protected Variable và bắn cảnh báo tới Slack/SIEM.
**Giải thích cơ chế ngầm:** Cho phép Business ứng phó sự cố sập prod khẩn cấp nhưng ngăn chặn việc lạm dụng cờ bypass để trốn tránh trách nhiệm an ninh của cá nhân.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Developer tự gõ chữ `[skip-security]` ở commit message để bypass gate mà không hề có bất kỳ cảnh báo nào gửi về nhóm an ninh.
**Minh hoạ.** Bắn Webhook về Slack Channel `#security-alerts` kèm thông tin người kích hoạt biến `EMERGENCY_SECURITY_BYPASS`:
```bash
if [ "$EMERGENCY_SECURITY_BYPASS" = "true" ]; then
  echo "[WARNING] EMERGENCY BYPASS DETECTED!"
  curl -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"🚨 *EMERGENCY BYPASS ACTIVATED*\n*User:* $GITLAB_USER_LOGIN\n*Project:* $CI_PROJECT_PATH\n*Pipeline:* $CI_PIPELINE_URL\"}" \
    $SLACK_SECURITY_WEBHOOK
fi
```
**Con số chốt:** 100% lượt bypass được cảnh báo tức thì.

---

### 1.3. Hiệu năng và Đo lường DevSecOps Enterprise (10 phút)

**Nguyên lý cốt lõi:** Tối ưu hóa hiệu năng Pipeline Security bằng Parallel Execution và Remote Caching.
**Phát biểu.** Tất cả các job scanner độc lập phải được cấu hình chạy song song (parallel) và sử dụng Distributed Cache cho cơ sở dữ liệu lỗ hổng.
**Giải thích cơ chế ngầm:** Thời gian chạy pipeline security quá lâu ($> 15$ phút) sẽ làm đứt gãy luồng làm việc của lập trình viên, gây tâm lý ức chế và dẫn đến yêu cầu tháo bỏ công cụ an ninh.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Các job SAST, Secret, IaC, Container scan chạy nối tiếp từng job một khiến pipeline kéo dài 30 phút.
**Minh hoạ.** Khai báo `needs: []` trên GitLab CI để cho 5 job scan chạy song song cùng lúc ở thời điểm bắt đầu pipeline:
```yaml
sast-scan:
  stage: scan
  needs: []
secret-scan:
  stage: scan
  needs: []
iac-scan:
  stage: scan
  needs: []
```
**Con số chốt:** Thời gian scan tổng hợp $< 5$ phút.

---

**Nguyên lý cốt lõi:** Đánh giá độ hiệu quả DevSecOps bằng chỉ số Escaped Vulnerabilities và MTTR.
**Phát biểu.** Hệ thống phòng thủ CI/CD phải được đánh giá dựa trên số lỗ hổng lọt lên Production và thời gian trung bình để khắc phục lỗi (MTTR).
**Giải thích cơ chế ngầm:** Số lượng bài quét hay số tool scan không chứng minh được ứng dụng an toàn; chỉ số lỗ hổng lọt lưới thực tế mới là thước đo năng lực thật của bộ phận DevSecOps.
> [!WARNING]
> **CẠM BẪY THỰC CHIẾN:**
> Đo đạc thành tích DevSecOps bằng tổng số CVE phát hiện được trong tháng mà không quan tâm bao nhiêu lỗi đã được vá hoặc bao nhiêu lỗi lọt lên Prod.
**Minh hoạ.** Theo dõi ma trận SLA MTTR doanh nghiệp:
- Critical Vulnerabilities: MTTR $< 24$ giờ.
- High Vulnerabilities: MTTR $< 7$ ngày.
**Con số chốt:** MTTR Critical $< 24$ giờ.

---



#### Mô hình 1: Chuỗi phòng thủ 6 lớp khép kín (6-Layer DevSecOps Defense Matrix)
Không tin tưởng vào bất kỳ lớp kiểm tra đơn lẻ nào. Một lỗi có thể lọt qua SAST nhưng sẽ bị bắt ở Container Scan; một CVE chưa vá trong Container sẽ bị phát hiện và chặn ở OPA Policy Gate.
- **Lớp 1 (Code & Secret Security):** Gitleaks quét nợ secret trong lịch sử git commit + Semgrep SAST kiểm tra lỗ hổng logic mã nguồn (SQLi, XSS, RCE, IDOR).
- **Lớp 2 (Infrastructure as Code Security):** Checkov quét kiểm tra tính tuân thủ bảo mật cho Dockerfile, Kubernetes Manifests (`.yaml`), Terraform files và Helm Charts.
- **Lớp 3 (Identity & Dynamic Secret Access):** HashiCorp Vault OIDC Token Retrieval sinh credential truy cập ngắn hạn tự hủy sau 15-30 phút.
- **Lớp 4 (Container Image Security):** Multi-stage Docker build Distroless + Trivy vulnerability scanner quét toàn bộ OS packages và ứng dụng binaries.
- **Lớp 5 (Supply Chain Security):** Syft tự động xuất danh mục thành phần phần mềm SBOM (SPDX/CycloneDX) + Cosign Keyless signing ký số xác minh tính toàn vẹn của Image.
- **Lớp 6 (Governance & Quality Gate):** OPA / Conftest Rego Policy evaluation kiểm định quy tắc doanh nghiệp + Central Security Quality Gate Parser tổng hợp kết quả ngắt pipeline.

#### Mô hình 2: Nguyên tắc Bất biến & Không tin tưởng (Zero-Trust CI/CD Pipeline)
Tất cả các tệp báo cáo JSON/SARIF sinh ra từ các job scan phải được ghi vết bằng Artifact Hashes. Job Security Quality Gate đứng ở cuối không tin vào tín hiệu `status: success` của các job trước mà tự tay mở tệp JSON Artifact để parse và tính toán ma trận rủi ro độc lập.

#### Mô hình 3: Ma trận Phân loại Rủi ro và SLA Khắc phục Lỗi (Severity & Remediation SLA Matrix)
Phân loại các phát hiện an ninh theo mức độ ảnh hưởng thực tế đến hoạt động kinh doanh:
- **Cấp độ Critical (RCE, Hardcoded Production Master Key, SQLi Unauthenticated):** Yêu cầu khắc phục trong vòng 24 giờ. Quality Gate ngắt pipeline hard-fail 100%.
- **Cấp độ High (Privilege Escalation, Missing Auth Check, High CVSS Container CVE):** Yêu cầu khắc phục trong vòng 7 ngày. Quality Gate hard-fail trên nhánh `main`.
- **Cấp độ Medium (CSRF, Information Disclosure, Deprecated TLS Config):** Yêu cầu khắc phục trong vòng 30 ngày. Quality Gate phát cảnh báo Warning.
- **Cấp độ Low/Unknown (Code Style, Debug Log Enabled):** Đưa vào danh sách backlog xem xét tối ưu sau.

---

### 1.4. Đưa vào việc thật (4 phút)

### 7.1. Kịch bản áp dụng thực tế tại Doanh nghiệp Tài chính - Ngân hàng
Trong môi trường Ngân hàng hoặc Thương mại điện tử:
1. **Pha Lập trình (Pre-commit Phase):** Dev sử dụng Gitleaks CLI kiểm tra secret cục bộ trên máy tính cá nhân trước khi push code. Nếu phát hiện API Key trong mã nguồn, git hook tự động ngăn cản việc commit.
2. **Pha Merge Request (CI Pipeline Phase):** GitLab Runner tự động kích hoạt 6 lớp scan song song. Nếu phát hiện Secret hoặc CVE Critical $\to$ MR bị khóa nút Merge, đồng thời gửi thông báo về Slack Channel của Dev Team.
3. **Pha Duyệt Ngoại lệ (Security Waiver Review):** Nếu gặp lỗi Vendor chưa có bản vá, Dev tạo Ticket JIRA xin phép SecLead. SecLead thẩm định khả năng khai thác thực tế. Nếu chấp thuận, SecLead thêm 1 dòng có Expiration Date vào tệp `.trivyignore` ở repo quản trị tập trung.
4. **Pha Staging/Production Deployment (CD Pipeline Phase):** Kubernetes Cluster sử dụng Kyverno/OPA Gatekeeper verify chữ ký điện tử Cosign trên Container Image trước khi cho phép Pod khởi chạy. Nếu Image không có chữ ký của GitLab CI, Kubernetes Admission Controller từ chối tạo Pod.

### 7.2. Case Study Thực tế: Giải cứu Hệ thống khỏi Tấn công Chuỗi cung ứng (Supply Chain Attack)
Một thư viện npm mã nguồn mở phổ biến bị hacker chiếm tài khoản và đẩy bản cập nhật chứa mã độc mã hóa dữ liệu (Ransomware).
- **Hệ thống thông thường (Chưa có DevSecOps):** Tự động kéo npm package mới nhất về build image, đẩy thẳng lên Prod và bị mã hóa toàn bộ dữ liệu.
- **Hệ thống có Phòng thủ 6 Lớp (Buổi 35):**
  1. Job Dependency Scan phát hiện phiên bản npm package mới xuất hiện trong danh sách cảnh báo của OSS Index.
  2. Job Trivy Container Scan phát hiện mã độc hại có điểm CVSS 10.0.
  3. Job Syft tạo SBOM và OPA Gatekeeper so sánh hash của package với danh sách allowlist.
  4. Security Quality Gate phát hiện `Critical_Count > 0` $\to$ **Hard-Fail ngắt pipeline lập tức** ở minute thứ 2.
  5. Tự động gửi cảnh báo khẩn cấp đến Security SOC Team và tạo Ticket JIRA ưu tiên Highest. Hệ thống Production hoàn toàn bình an vô sự!

### 7.3. Trường hợp khi nào KHÔNG nên dùng quy trình 6 lớp đầy đủ
Không phải mọi dự án đều cần bật full 6 lớp scanner cồng kềnh. Cần biết khi nào KHÔNG nên dùng quy trình 6 lớp:

| Loại dự án / Ngữ cảnh | Lý do KHÔNG nên dùng 6 lớp full | Giải pháp thay thế tinh gọn |
|---|---|---|
| PoC / Internal Tool thử nghiệm cá nhân | Gây lãng phí tài nguyên Runner và làm đứt gãy tốc độ làm PoC. | Chỉ giữ lại Secret Scan (Gitleaks) nhẹ nhàng. |
| Documentation Repos / Static Web (HTML/CSS) | Không có mã nguồn backend, không có container image. | Tắt SAST, Container Scan, SBOM và Vault OIDC. |
| Emergency Production Hotfix Patch | Cần khôi phục hệ thống Prod khẩn cấp khi đang sập dịch vụ. | Sử dụng cờ `EMERGENCY_SECURITY_BYPASS` có vết Audit Trail. |


### 1.5. Bẫy hay gặp (2 phút)

| Bẫy hay gặp | Vì sao dính bẫy | Làm đúng là |
|---|---|---|
| Bẫy 1: Tắt scanner khi gặp quá nhiều báo động giả (False Positive) | Do không dành thời gian tinh chỉnh bộ Rule Regex cho phù hợp với đặc thù dự án. | Tinh chỉnh exclusion pattern trong tệp config scanner thay vì tắt hoàn toàn công cụ. |
| Bẫy 2: Dùng biến static thay cho OIDC authentication với Vault | Muốn làm nhanh không tốn công cấu hình OIDC Role trust policy giữa GitLab và Vault. | Cấu hình OIDC JWT Role trên Vault để cấp Dynamic Credential ngắn hạn cho Runner. |
| Bẫy 3: Quên cấu hình dọn dẹp Artifacts báo cáo an ninh | Để cờ `expire_in` quá ngắn (ví dụ 1 hour) khiến job Quality Gate đằng sau không tìm thấy tệp báo cáo. | Khai báo `artifacts:expire_in: 1 week` cho các tệp báo cáo JSON/SARIF. |
| Bẫy 4: Thêm cờ `allow_failure: true` ở tất cả các job scan | Muốn pipeline luôn màu xanh để không bị dính trách nhiệm khi build lỗi. | Đè thuộc tính `allow_failure: false` ở các stage quan trọng thông qua Compliance Policy. |
| Bẫy 5: Không test tệp ignore dẫn đến ngày hết hạn quá hạn làm sập pipeline đột ngột | Do ghi bừa ngày hết hạn trong quá khứ hoặc không chạy script audit tự động. | Tích hợp job `check-allowlist-audit.sh` chạy định kỳ để nhắc nhở các CVE sắp hết hạn waiver. |

---

### 1.6. Tóm tắt (3 phút)

### 9.1. Sơ đồ Mermaid: Kiến trúc Pipeline DevSecOps 6 Lớp Hoàn Chỉnh

```mermaid
flowchart TD
    A[Dev Push Code / Create MR] --> B[Layer 1: Code & Secret Scan\nGitleaks + Semgrep SAST]
    A --> C[Layer 2: IaC Security\nCheckov IaC Scan]
    A --> D[Layer 3: Vault OIDC\nFetch Dynamic Tokens]
    
    B --> E[Layer 4: Container Build & Scan\nMulti-stage Docker + Trivy]
    C --> E
    D --> E
    
    E --> F[Layer 5: Supply Chain Security\nSyft SBOM + Cosign Keyless Sign]
    F --> G[Layer 6: Policy & Quality Gate\nOPA Rego Audit + Gate Parser]
    
    G -->|CRITICAL > 0 / Expiration Passed| H[FAIL-FAST: Block MR & Auto-Create JIRA Ticket]
    G -->|Emergency Bypass = true| I[WARNING: Allow Deployment & Send SIEM Alert]
    G -->|All Checks PASSED| J[SUCCESS: Approve Merge & Deploy to Prod K8s]
```

### 9.2. Năm điều phải nhớ thuộc lòng
1. **6 Lớp phòng thủ:** Code, Secret, IaC, Container Image, Supply Chain và Policy Quality Gate.
2. **OIDC Dynamic Secret:** Không bao giờ lưu Password/API Key tĩnh trong CI Variables; sử dụng Vault JWT token.
3. **Immutability (Tính bất biến):** Chính sách an ninh phải được quản lý tập trung ở Group level, Dev không thể sửa đè.
4. **Metadata Waiver:** Mọi dòng bỏ qua lỗi phải có CVE ID, Ngày hết hạn, Phê duyệt và Ticket JIRA.
5. **Audit Trail:** Mọi hành vi bypass khẩn cấp đều phải ghi log vết và gửi cảnh báo tức thì về hệ thống giám sát.

---

### 1.7. Câu hỏi tự kiểm tra (5 phút)

### 10.1. Danh sách câu hỏi tự kiểm tra
1. Kiến trúc phòng thủ DevSecOps chuẩn Enterprise gồm tối thiểu bao nhiêu lớp? Kể tên các lớp đó.
2. Tại sao OIDC JWT lại an toàn hơn việc lưu Static Masked Variables trên GitLab CI?
3. Tệp báo cáo an ninh định dạng chuẩn quốc tế phổ biến nhất hiện nay là gì?
4. Kỹ thuật ký số container không cần quản lý private key tĩnh gọi là gì?
5. Sự khác biệt giữa Hard-fail và Soft-fail trong cấu hình Security Quality Gate là gì?
6. Bốn trường metadata bắt buộc khi khai báo một dòng trong tệp `.trivyignore` là gì?
7. Script Quality Gate cần làm gì khi phát hiện biến `EMERGENCY_SECURITY_BYPASS=true`?
8. Tại sao job Security Quality Gate phải tự parse file JSON artifact thay vì tin vào exit status của job trước?
9. Công cụ nào dùng để kiểm định tính tuân thủ quy định hạ tầng bằng ngôn ngữ Rego?
10. Tệp SBOM (Software Bill of Materials) cung cấp giá trị gì cho an ninh chuỗi cung ứng?
11. Hai chỉ số KPI quan trọng nhất để đo độ hiệu quả của hệ thống DevSecOps là gì?
12. Thời hạn tồn tại tối đa (TTL) khuyến nghị cho một Dynamic Secret cấp từ HashiCorp Vault là bao nhiêu?

---

### 10.2. Đáp án câu hỏi tự kiểm tra

1. Gồm 6 lớp phòng thủ tự động:
   - Lớp 1 (Code & Secret Security): Gitleaks + Semgrep SAST.
   - Lớp 2 (Infrastructure as Code Security): Checkov IaC Security.
   - Lớp 3 (Identity & Secret Access): HashiCorp Vault OIDC JWT.
   - Lớp 4 (Container Image Security): Multi-stage Docker Distroless + Trivy Scan.
   - Lớp 5 (Supply Chain Security): Syft SBOM + Cosign Keyless Signing.
   - Lớp 6 (Governance & Quality Gate): OPA / Conftest Rego Policy + Security Quality Gate Parser.
2. Vì OIDC sinh ra token tạm thời tự hết hạn sau thời gian ngắn (ví dụ 15-30 phút) và không lọt secret tĩnh vào log đệm hay đĩa cứng Runner. Ngược lại, static variable vĩnh viễn rất dễ bị lộ khi log dump hoặc runner bị compromised.
3. Định dạng SARIF (Static Analysis Results Interchange Format) v2.1.0 và GitLab Security Schema JSON (`gl-sast-report.json`, `gl-container-scanning-report.json`).
4. Kỹ thuật Ký số không dùng khóa (Keyless Cosign Signing) dựa trên OIDC Identity Provider (như GitLab/Fulcio) kết hợp với minh chứng công khai Rekor Transparency Log.
5. Hard-fail dừng ngay pipeline và ngắt nút bấm Merge (áp dụng bắt buộc trên nhánh `main` và các môi trường Production). Soft-fail chỉ phát cảnh báo Warning và ghi log (áp dụng trên nhánh `feature` để không chặn tiến độ dev nháp).
6. 4 trường metadata bắt buộc gồm: ID lỗ hổng (CVE ID), Ngày hết hạn chuẩn ISO 8601 (YYYY-MM-DD), Người phê duyệt (@username), và Mã Ticket JIRA/ServiceNow theo dõi (`SEC-XXXX`).
7. Script Quality Gate cần:
   - In thông báo Warning đỏ nổi bật: `[WARNING] EMERGENCY SECURITY BYPASS ACTIVATED`.
   - Bắn Webhook chứa thông tin người trigger (`$GITLAB_USER_LOGIN`), dự án, pipeline URL về Slack Security Channel và hệ thống SIEM.
   - Trả về mã thoát `exit 0` để nhả pipeline cho phép khôi phục sản phẩm Production khẩn cấp.
8. Để tránh trường hợp job trước bị developer lỡ tay hoặc cố tình cài thuộc tính `allow_failure: true` hay script bọc `exit 0` làm giả tín hiệu thành công. Quality Gate độc lập bắt buộc tự tay đọc file JSON thô để tính toán số lượng CVE thực tế.
9. Công cụ Conftest kết hợp với Open Policy Agent (OPA) và bộ quy tắc được soạn thảo bằng ngôn ngữ Rego.
10. Tệp SBOM (Software Bill of Materials) cung cấp danh mục chi tiết toàn bộ thành phần phần mềm, thư viện phụ thuộc và version. Giúp nhóm an ninh tra cứu tức thì danh sách dự án bị ảnh hưởng khi xuất hiện lỗ hổng 0-day mới công bố trên toàn cầu.
11. Hai chỉ số KPI gồm: Số lỗ hổng lọt lưới lên Production (Escaped Vulnerabilities) và Thời gian trung bình để khắc phục lỗ hổng (MTTR - Mean Time to Remediate).
12. Thời hạn tồn tại tối đa (TTL) khuyến nghị cho một Dynamic Secret cấp từ HashiCorp Vault là dưới 60 phút (khuyên dùng tốt nhất ở mức 15 đến 30 phút).

---

### 1.8. Tài liệu tham khảo (2 phút)

| Nguồn tài liệu | Mô tả nội dung | Phiên bản GitLab áp dụng |
|---|---|---|
| GitLab DevSecOps Documentation | Hướng dẫn tích hợp Security Scanning & Compliance Frameworks | GitLab EE 16.x + |
| CNCF Financial Services Security Whitepaper | Chuẩn phòng thủ an ninh 6 lớp cho ngành tài chính ngân hàng | Version 2.0 |
| Cosign & Sigstore Documentation | Hướng dẫn Ký số Container Image Keyless qua OIDC | Cosign v2.x |
| Open Policy Agent (OPA) / Conftest Guide | Ngôn ngữ Rego và viết luật kiểm định IaC/Security JSON | OPA v0.50+ |
| NIST SP 800-218 (SSDF) | Khung chuẩn phát triển phần mềm an toàn của NIST | NIST SSDF v1.1 |

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| §0 | Khởi động và ôn tập | 10 phút |
| §1 | Sau buổi này học viên LÀM ĐƯỢC gì | 1 phút |
| §2 | Cần biết trước | 1 phút |
| §3 | Thuật ngữ và mô hình tư duy | 8 phút |
| §4 | Tổng quan 12 Quy tắc DevSecOps Nâng cao | 10 phút |
| §5 | Quản lý Chính sách và Nợ an ninh trong Pipeline | 10 phút |
| §6 | Hiệu năng và Đo lường DevSecOps Enterprise | 10 phút |
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

## 1. Mục tiêu bài thi Lab Giữa Kỳ 2
Bài thi thực hành giữa kỳ 2 là một kịch bản mô phỏng thực chiến tại Doanh nghiệp Enterprise: Học viên đóng vai trò DevSecOps Lead thiết lập toàn bộ hệ thống phòng thủ CI/CD 6 lớp cho một sản phẩm Microservice ngân hàng từ con số 0.

Hệ thống bắt buộc phải tích hợp thành công:
1. Stage 1: SAST Code Analysis (Semgrep) & Secret Detection (Gitleaks).
2. Stage 2: Infrastructure as Code Security Inspection (Checkov).
3. Stage 3: Dynamic Secret Exchange via HashiCorp Vault OIDC JWT.
4. Stage 4: Multi-stage Docker Image Build & Container Vulnerability Scanning (Trivy).
5. Stage 5: Supply Chain Verification (Syft SBOM Generation & Cosign Keyless Image Signature).
6. Stage 6: Policy-as-Code Audit (Conftest/OPA) & Multi-stage Security Quality Gate Parser.
7. Exception Waiver Audit Management & Real-time Emergency Bypass Logging.

---

## 2. Mô hình kiến trúc Lab L2

```mermaid
graph TD
    subgraph GitLab CI/CD Pipeline Execution Host
        A[Git Commit Push] --> B[Stage 1: Code & Secret Scan\nSemgrep & Gitleaks]
        A --> C[Stage 2: IaC Security Scan\nCheckov Engine]
        
        B --> D[Stage 3: Vault OIDC Token Retrieval\nJWT Authentication]
        C --> D
        
        D --> E[Stage 4: Container Build & Scan\nMulti-stage Docker + Trivy]
        E --> F[Stage 5: Supply Chain Attestation\nSyft SBOM + Cosign Signature]
        
        F --> G[Stage 6: Policy & Quality Gate\nConftest OPA + Gate Parser]
    end

    subgraph Security Artifacts & Logs
        G --> H[Artifact: gl-security-report.json]
        G --> I[Artifact: sbom.spdx.json]
        G --> J[Artifact: image-cosign.bundle]
        G --> K[Artifact: security-audit.log]
    end

    G -->|CRITICAL > 0| L[HARD-FAIL: Block Merge Request & Fail Pipeline]
    G -->|EMERGENCY_BYPASS = true| M[WARNING: Allow Deployment & Audit SIEM Alert]
    G -->|ALL PASS| N[SUCCESS: Deploy Container to Kubernetes Prod]
```

---

## 3. Các bước thực hiện bài thi (14 Checkpoints)

### Bước 1: Khởi tạo Cấu trúc Dự án và Mã nguồn Đơn vị (10 phút)

Tạo thư mục làm việc và các tệp mã nguồn cơ bản cho bài thi giữa kỳ 2.

```bash
mkdir -p devsecops-midterm2-lab
cd devsecops-midterm2-lab
mkdir -p app infrastructure policies scripts
```

Tạo tệp ứng dụng Go đơn giản `app/main.go`:
```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Bank Payment Service v2.0 - Secure Endpoint")
	})
	fmt.Println("Server running on port 8080...")
	http.ListenAndServe(":8080", nil)
}
```

Tạo tệp Kubernetes Manifest nhạy cảm `infrastructure/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: payment-app
        image: registry.company.internal/payment:v2.0
        ports:
        - containerPort: 8080
        securityContext:
          runAsNonRoot: true
          allowPrivilegeEscalation: false
```

### **CHECKPOINT 1**
Chạy câu lệnh kiểm tra cấu trúc thư mục khởi tạo bài thi:

```bash
test -f app/main.go && test -f infrastructure/deployment.yaml && echo "CHECKPOINT 1: ĐẠT" || echo "CHECKPOINT 1: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 1: ĐẠT
```

---

### Bước 2: Tích hợp Lớp 1 — Secret Scanning & SAST Code Scan (15 phút)

Tạo script thực thi Lớp 1 `scripts/layer1-code-scan.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "LAYER 1: SECRET DETECTION & SAST SCANNING"
echo "=========================================================="

mkdir -p reports

# 1. Quét Secret bằng Gitleaks (Giả lập output chuẩn)
echo "[1/2] Running Gitleaks Secret Detection..."
cat << 'EOF' > reports/gitleaks-report.json
[
  {
    "Description": "AWS Access Key",
    "StartLine": 12,
    "EndLine": 12,
    "FilePath": "config/aws.go",
    "Secret": "AKIAIOSFODNN7EXAMPLE",
    "RuleID": "aws-access-token",
    "Entropy": 3.67
  }
]
EOF
echo "Gitleaks scan completed. Output saved to reports/gitleaks-report.json"

# 2. Quét SAST bằng Semgrep
echo "[2/2] Running Semgrep SAST Code Scan..."
cat << 'EOF' > reports/semgrep-report.json
{
  "results": [
    {
      "check_id": "go.lang.security.audit.net.use-of-http.use-of-http",
      "path": "app/main.go",
      "extra": {
        "severity": "WARNING",
        "message": "Use of HTTP without TLS"
      }
    }
  ]
}
EOF
echo "Semgrep SAST scan completed. Output saved to reports/semgrep-report.json"
```

Cho phép script chạy và kiểm tra kết quả:
```bash
chmod +x scripts/layer1-code-scan.sh
./scripts/layer1-code-scan.sh
```

### **CHECKPOINT 2**
Chạy câu lệnh kiểm tra báo cáo Lớp 1:

```bash
test -f reports/gitleaks-report.json && test -f reports/semgrep-report.json && echo "CHECKPOINT 2: ĐẠT" || echo "CHECKPOINT 2: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 2: ĐẠT
```

---

### Bước 3: Tích hợp Lớp 2 — Infrastructure as Code (IaC) Scan (10 phút)

Tạo script thực thi Lớp 2 `scripts/layer2-iac-scan.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "LAYER 2: INFRASTRUCTURE AS CODE (IaC) SECURITY SCAN"
echo "=========================================================="

echo "[Checkov] Scanning Kubernetes Manifests and Dockerfiles..."
cat << 'EOF' > reports/checkov-report.json
{
  "check_type": "kubernetes",
  "summary": {
    "passed": 4,
    "failed": 1,
    "skipped": 0,
    "parsing_errors": 0
  },
  "results": {
    "failed_checks": [
      {
        "check_id": "CKV_K8S_14",
        "check_name": "Image should Use Digest",
        "file_path": "/infrastructure/deployment.yaml",
        "severity": "LOW"
      }
    ]
  }
}
EOF
echo "Checkov IaC scan completed. Output saved to reports/checkov-report.json"
```

Cho phép script chạy:
```bash
chmod +x scripts/layer2-iac-scan.sh
./scripts/layer2-iac-scan.sh
```

### **CHECKPOINT 3**
Chạy câu lệnh kiểm tra báo cáo Lớp 2:

```bash
test -f reports/checkov-report.json && grep -q "CKV_K8S_14" reports/checkov-report.json && echo "CHECKPOINT 3: ĐẠT" || echo "CHECKPOINT 3: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 3: ĐẠT
```

---

### Bước 4: Tích hợp Lớp 3 — Vault OIDC Token Retrieval (10 phút)

Mô phỏng quy trình xác thực OIDC JWT với Vault để lấy Dynamic Database Secret ngắn hạn `scripts/layer3-vault-auth.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "LAYER 3: HASHICORP VAULT OIDC DYNAMIC SECRET RETRIEVAL"
echo "=========================================================="

# Mô phỏng lấy JWT ID Token từ GitLab Runner
MOCK_GITLAB_JWT="eyJhbGciOiJSUzI1NiIsImtpZCI6ImdpdGxhYi1jaSJ9.eyJpc3MiOiJodHRwczovL2dpdGxhYi5jb21wYW55LmludGVybmFsIiwiYXVkIjoiaHR0cHM6Ly92YXVsdC5jb21wYW55LmludGVybmFsIiwic3ViIjoicHJvamVjdF9wYXRoOmJhbmsvcGF5bWVudC1zZXJ2aWNlOnJlZjptYWluIn0"

echo "[Vault OIDC] Exchanging JWT Token with Vault API..."
cat << 'EOF' > reports/vault-token.json
{
  "auth": {
    "client_token": "s.vlt-mock-dynamic-token-8891223",
    "lease_duration": 1800,
    "renewable": true,
    "policies": ["payment-service-prod-role"]
  }
}
EOF
echo "Successfully authenticated with Vault via OIDC JWT."
echo "Dynamic Lease TTL: 1800 seconds (30 minutes)."
```

Cho phép script chạy:
```bash
chmod +x scripts/layer3-vault-auth.sh
./scripts/layer3-vault-auth.sh
```

### **CHECKPOINT 4**
Chạy câu lệnh kiểm tra Token Vault OIDC:

```bash
grep -q "s.vlt-mock-dynamic-token" reports/vault-token.json && echo "CHECKPOINT 4: ĐẠT" || echo "CHECKPOINT 4: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 4: ĐẠT
```

---

### Bước 5: Tích hợp Lớp 4 — Multi-stage Docker Build & Container Scan (15 phút)

Tạo `Dockerfile` chuẩn Multi-stage Distroless trong thư mục ứng dụng:

```dockerfile
# Stage 1: Build binary
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY app/main.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o payment-service main.go

# Stage 2: Distroless Runtime Image
FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /
COPY --from=builder /app/payment-service /payment-service
USER 65532:65532
ENTRYPOINT ["/payment-service"]
```

Tạo script quét container image `scripts/layer4-container-scan.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "LAYER 4: CONTAINER MULTI-STAGE BUILD & TRIVY SCAN"
echo "=========================================================="

echo "[Trivy] Scanning Image registry.company.internal/payment:v2.0..."
cat << 'EOF' > reports/trivy-report.json
{
  "SchemaVersion": 2,
  "Results": [
    {
      "Target": "registry.company.internal/payment:v2.0 (debian 12.5)",
      "Class": "os-pkgs",
      "Vulnerabilities": [
        {
          "VulnerabilityID": "CVE-2024-24790",
          "PkgName": "stdlib",
          "InstalledVersion": "1.22.0",
          "FixedVersion": "1.22.4",
          "Severity": "CRITICAL",
          "Title": "net/netip: unexpected behavior of IsLoopback"
        }
      ]
    }
  ]
}
EOF
echo "Trivy Container Scan completed. Vulnerability report saved to reports/trivy-report.json"
```

Cho phép script chạy:
```bash
chmod +x scripts/layer4-container-scan.sh
./scripts/layer4-container-scan.sh
```

### **CHECKPOINT 5**
Chạy câu lệnh kiểm tra báo cáo quét Container:

```bash
test -f reports/trivy-report.json && grep -q "CVE-2024-24790" reports/trivy-report.json && echo "CHECKPOINT 5: ĐẠT" || echo "CHECKPOINT 5: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 5: ĐẠT
```

---

### Bước 6: Tích hợp Lớp 5 — Syft SBOM & Cosign Image Signature (15 phút)

Tạo script sinh tệp kiểm kê SBOM và thực hiện ký số container image `scripts/layer5-supply-chain.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "LAYER 5: SUPPLY CHAIN SECURITY (SBOM & COSIGN KEYLESS)"
echo "=========================================================="

# 1. Tạo SBOM bằng Syft
echo "[Syft] Generating SPDX SBOM Document..."
cat << 'EOF' > reports/sbom.spdx.json
{
  "SPDXID": "SPDXRef-DOCUMENT",
  "spdxVersion": "SPDX-2.3",
  "creationInfo": {
    "created": "2026-08-22T08:00:00Z",
    "creators": ["Tool: Syft-v1.3.0", "Organization: Enterprise Security"]
  },
  "name": "payment-service-sbom",
  "packages": [
    {
      "name": "stdlib",
      "SPDXID": "SPDXRef-Package-stdlib-1.22.0",
      "versionInfo": "1.22.0"
    }
  ]
}
EOF
echo "SBOM Document created at reports/sbom.spdx.json"

# 2. Ký số bằng Cosign Keyless
echo "[Cosign] Signing Container Image via OIDC Identity..."
cat << 'EOF' > reports/cosign.bundle
{
  "mediaType": "application/vnd.dev.sigstore.bundle+json;version=0.1",
  "verificationMaterial": {
    "publicCertificate": {
      "rawBytes": "MIIB0zCCAXygAwIBAgIUY2lhdXRoLWdpdGxhYi1vaWRj..."
    }
  },
  "messageSignature": {
    "signature": "MEUCIQDx88Y129...signed-by-gitlab-runner-identity"
  }
}
EOF
echo "Cosign keyless signature generated at reports/cosign.bundle"
```

Cho phép script chạy:
```bash
chmod +x scripts/layer5-supply-chain.sh
./scripts/layer5-supply-chain.sh
```

### **CHECKPOINT 6**
Chạy câu lệnh kiểm tra SBOM và chữ ký Cosign:

```bash
test -f reports/sbom.spdx.json && test -f reports/cosign.bundle && echo "CHECKPOINT 6: ĐẠT" || echo "CHECKPOINT 6: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 6: ĐẠT
```

---

### Bước 7: Tích hợp Lớp 6 — Policy-as-Code Rego Enforcement (15 phút)

Tạo tệp quy tắc kiểm định an ninh bằng ngôn ngữ Rego `policies/security.rego`:

```rego
package main

default allow = false

# Quy tắc 1: Không chấp nhận lỗ hổng CRITICAL trong Container Image
deny[msg] {
    some i
    input.vulnerabilities[i].severity == "CRITICAL"
    msg := sprintf("POLICY VIOLATION: Found CRITICAL vulnerability %v in package %v", [input.vulnerabilities[i].id, input.vulnerabilities[i].package])
}

# Quy tắc 2: Không cho phép có Secret bị rò rỉ trong Gitleaks report
deny[msg] {
    count(input.secrets) > 0
    msg := sprintf("POLICY VIOLATION: Exposed Secrets Detected! Count: %v", [count(input.secrets)])
}

allow {
    count(deny) == 0
}
```

Tạo script thực thi kiểm định Conftest OPA `scripts/layer6-policy-audit.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "LAYER 6: POLICY-AS-CODE OPA REGULATION AUDIT"
echo "=========================================================="

echo "[OPA/Conftest] Evaluating security policies against reports..."
cat << 'EOF' > reports/opa-evaluation.json
{
  "status": "FAIL",
  "violations": [
    "POLICY VIOLATION: Found CRITICAL vulnerability CVE-2024-24790 in package stdlib",
    "POLICY VIOLATION: Exposed Secrets Detected! Count: 1"
  ]
}
EOF
echo "OPA Policy Audit evaluated. Status: FAIL."
```

Cho phép script chạy:
```bash
chmod +x scripts/layer6-policy-audit.sh
./scripts/layer6-policy-audit.sh
```

### **CHECKPOINT 7**
Chạy câu lệnh kiểm tra kết quả đánh giá OPA Rego Policy:

```bash
test -f reports/opa-evaluation.json && grep -q "POLICY VIOLATION" reports/opa-evaluation.json && echo "CHECKPOINT 7: ĐẠT" || echo "CHECKPOINT 7: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 7: ĐẠT
```

---

### Bước 8: Tạo Tệp Allowlist Waiver có Hạn dùng ISO 8601 (10 phút)

Tạo tệp ngoại lệ an ninh có metadata đầy đủ `.trivyignore`:

```text
# CVE-2024-24790 | Expire: 2026-12-31 | ApprovedBy: @sec-lead | Ticket: SEC-9912
CVE-2024-24790
```

Tạo script kiểm tra hạn dùng allowlist `scripts/check-allowlist-audit.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

IGNORE_FILE=".trivyignore"
CURRENT_DATE=$(date +"%Y-%m-%d")

echo "[Allowlist Audit] Checking expiration dates in $IGNORE_FILE..."

while IFS= read -r line || [ -n "$line" ]; do
    if [[ "$line" =~ ^#\ (CVE-[0-9-]+)\ \|\ Expire:\ ([0-9]{4}-[0-9]{2}-[0-9]{2})\ \|\ ApprovedBy:\ (@[a-zA-Z0-9_-]+)\ \|\ Ticket:\ ([a-zA-Z0-9_-]+) ]]; then
        cve_id="${BASH_REMATCH[1]}"
        expire_date="${BASH_REMATCH[2]}"
        approver="${BASH_REMATCH[3]}"
        ticket="${BASH_REMATCH[4]}"

        echo "Auditing $cve_id: Expire=$expire_date, Approver=$approver, Ticket=$ticket"

        if [[ "$CURRENT_DATE" > "$expire_date" ]]; then
            echo "[ERROR] Allowlist entry for $cve_id EXPIRED on $expire_date!"
            exit 1
        else
            echo "[OK] Waiver valid until $expire_date."
        fi
    fi
done < "$IGNORE_FILE"

echo "Allowlist audit PASSED."
```

Cho phép script chạy:
```bash
chmod +x scripts/check-allowlist-audit.sh
./scripts/check-allowlist-audit.sh
```

### **CHECKPOINT 8**
Chạy câu lệnh kiểm tra script audit tệp allowlist:

```bash
./scripts/check-allowlist-audit.sh | grep -q "PASSED" && echo "CHECKPOINT 8: ĐẠT" || echo "CHECKPOINT 8: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 8: ĐẠT
```

---

### Bước 9: Xây dựng Multi-stage Security Quality Gate Parser (15 phút)

Tạo tệp script ngắt pipeline tổng hợp `scripts/security-gate-parser.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "CENTRAL SECURITY QUALITY GATE PARSER — BUỔI 35"
echo "=========================================================="

CRIT_COUNT=0
HIGH_COUNT=0

# 1. Parse Trivy Container Report (Bỏ qua CVE trong .trivyignore)
if [ -f reports/trivy-report.json ]; then
    RAW_CRIT=$(jq '[.Results[].Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length' reports/trivy-report.json || echo 0)
    
    # Kiểm tra xem CVE có trong allowlist hợp lệ hay không
    if [ -f .trivyignore ] && grep -q "CVE-2024-24790" .trivyignore; then
        echo "[INFO] CVE-2024-24790 is suppressed via active allowlist waiver."
        CRIT_COUNT=0
    else
        CRIT_COUNT=$RAW_CRIT
    fi
fi

# 2. Parse Secret Detection
if [ -f reports/gitleaks-report.json ]; then
    SECRET_COUNT=$(jq 'length' reports/gitleaks-report.json || echo 0)
else
    SECRET_COUNT=0
fi

echo "----------------------------------------------------------"
echo "QUALITY GATE ANALYSIS RESULTS:"
echo "Active Critical Vulnerabilities: $CRIT_COUNT"
echo "Exposed Secrets Count: $SECRET_COUNT"
echo "----------------------------------------------------------"

# 3. Kiểm tra biến Emergency Bypass
if [ "${EMERGENCY_SECURITY_BYPASS:-false}" = "true" ]; then
    echo "[WARNING] EMERGENCY SECURITY BYPASS IS ACTIVATED!"
    echo "Bypassing hard-fail checks. Sending Audit log to SIEM..."
    echo "$(date -u) | BYPASS | User: $USER | Reason: Production Incident Hotfix" >> reports/audit-trail.log
    echo "QUALITY GATE RESULT: BYPASSED (PASSED WITH WARNINGS)"
    exit 0
fi

# 4. Ra quyết định Quality Gate
if [ "$CRIT_COUNT" -gt 0 ] || [ "$SECRET_COUNT" -gt 0 ]; then
    echo "[FAIL-FAST] Security Quality Gate FAILED!"
    echo "Reason: Critical vulnerabilities or Exposed secrets detected."
    echo "QUALITY GATE RESULT: REJECTED"
    exit 1
else
    echo "QUALITY GATE RESULT: APPROVED (PASSED ALL 6 LAYERS)"
    exit 0
fi
```

Cho phép script chạy:
```bash
chmod +x scripts/security-gate-parser.sh
```

### **CHECKPOINT 9**
Test chạy script Quality Gate Parser trong điều kiện Allowlist active (kết quả mong đợi APPROVED):

```bash
./scripts/security-gate-parser.sh | grep -q "APPROVED" && echo "CHECKPOINT 9: ĐẠT" || echo "CHECKPOINT 9: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 9: ĐẠT
```

---

### Bước 10: Thử nghiệm Cịch bản Hard-Fail khi phát hiện Secret (10 phút)

Sửa script để mô phỏng sự cố phát hiện Secret không nằm trong allowlist và chạy gate:

```bash
# Đổi gitleaks-report để có 1 secret nguy hiểm
cat << 'EOF' > reports/gitleaks-report.json
[
  {
    "Description": "Production Master API Key",
    "FilePath": "app/main.go",
    "Secret": "MOCK_DUMMY_SECRET_KEY_FOR_TESTING"
  }
]
EOF
```

Chạy Quality Gate và bắt mã lỗi:

### **CHECKPOINT 10**
Chạy câu lệnh kiểm tra tính năng Hard-Fail ngắt pipeline:

```bash
./scripts/security-gate-parser.sh || echo "CHECKPOINT 10: ĐẠT"
```

**Kết quả kỳ vọng:**
```text
QUALITY GATE RESULT: REJECTED
CHECKPOINT 10: ĐẠT
```

---

### Bước 11: Kiểm thử Kịch bản Emergency Bypass Khẩn cấp (10 phút)

Kích hoạt biến môi trường `EMERGENCY_SECURITY_BYPASS=true` và thực thi gate:

```bash
export EMERGENCY_SECURITY_BYPASS=true
./scripts/security-gate-parser.sh
```

### **CHECKPOINT 11**
Chạy câu lệnh kiểm tra tính năng Emergency Bypass và Audit Log:

```bash
test -f reports/audit-trail.log && grep -q "BYPASS" reports/audit-trail.log && echo "CHECKPOINT 11: ĐẠT" || echo "CHECKPOINT 11: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 11: ĐẠT
```

---

### Bước 12: Dọn dẹp Trạng thái Bypass và Khôi phục Clean State (5 phút)

Hủy biến Bypass và khôi phục báo cáo Secret sạch:

```bash
unset EMERGENCY_SECURITY_BYPASS
echo "[]" > reports/gitleaks-report.json
```

### **CHECKPOINT 12**
Chạy câu lệnh kiểm tra trạng thái Clean State của Quality Gate:

```bash
./scripts/security-gate-parser.sh | grep -q "APPROVED" && echo "CHECKPOINT 12: ĐẠT" || echo "CHECKPOINT 12: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 12: ĐẠT
```

---

### Bước 13: Xây dựng tệp `.gitlab-ci.yml` Tích hợp 6 Stage Hoàn chỉnh (10 phút)

Tạo tệp cấu hình GitLab CI/CD chính thức của bài thi giữa kỳ 2 `.gitlab-ci.yml`:

```yaml
stages:
  - layer1-sast-secret
  - layer2-iac-scan
  - layer3-vault-auth
  - layer4-container-build
  - layer5-supply-chain
  - layer6-security-gate

variables:
  DOCKER_DRIVER: overlay2
  SEC_STRICT_MODE: "true"

layer1-code-scan-job:
  stage: layer1-sast-secret
  script:
    - ./scripts/layer1-code-scan.sh
  artifacts:
    paths:
      - reports/gitleaks-report.json
      - reports/semgrep-report.json
    expire_in: 7 days

layer2-iac-scan-job:
  stage: layer2-iac-scan
  script:
    - ./scripts/layer2-iac-scan.sh
  artifacts:
    paths:
      - reports/checkov-report.json
    expire_in: 7 days

layer3-vault-auth-job:
  stage: layer3-vault-auth
  script:
    - ./scripts/layer3-vault-auth.sh
  artifacts:
    paths:
      - reports/vault-token.json
    expire_in: 1 day

layer4-container-build-job:
  stage: layer4-container-build
  script:
    - ./scripts/layer4-container-scan.sh
  artifacts:
    paths:
      - reports/trivy-report.json
    expire_in: 7 days

layer5-supply-chain-job:
  stage: layer5-supply-chain
  script:
    - ./scripts/layer5-supply-chain.sh
  artifacts:
    paths:
      - reports/sbom.spdx.json
      - reports/cosign.bundle
    expire_in: 30 days

layer6-security-gate-job:
  stage: layer6-security-gate
  script:
    - ./scripts/check-allowlist-audit.sh
    - ./scripts/layer6-policy-audit.sh
    - ./scripts/security-gate-parser.sh
  artifacts:
    paths:
      - reports/audit-trail.log
    expire_in: 90 days
```

### **CHECKPOINT 13**
Chạy câu lệnh kiểm tra tệp `.gitlab-ci.yml` chuẩn cú pháp:

```bash
test -f .gitlab-ci.yml && grep -q "layer6-security-gate" .gitlab-ci.yml && echo "CHECKPOINT 13: ĐẠT" || echo "CHECKPOINT 13: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 13: ĐẠT
```

---

### Bước 14: Tổng hợp Báo cáo và Đánh giá Hoàn thành Bài thi Giữa Kỳ 2 (5 phút)

Tạo script đánh giá kết quả tổng hợp `scripts/final-exam-evaluation.sh`:

```bash
#!/usr/bin/env bash
set -eo pipefail

echo "=========================================================="
echo "EVALUATION SUMMARY: DEVSECOPS MIDTERM EXAM 2 (BUỔI 35)"
echo "=========================================================="

PASSED_LAYERS=0

[ -f reports/gitleaks-report.json ] && PASSED_LAYERS=$((PASSED_LAYERS+1))
[ -f reports/checkov-report.json ] && PASSED_LAYERS=$((PASSED_LAYERS+1))
[ -f reports/vault-token.json ] && PASSED_LAYERS=$((PASSED_LAYERS+1))
[ -f reports/trivy-report.json ] && PASSED_LAYERS=$((PASSED_LAYERS+1))
[ -f reports/sbom.spdx.json ] && PASSED_LAYERS=$((PASSED_LAYERS+1))
[ -f reports/opa-evaluation.json ] && PASSED_LAYERS=$((PASSED_LAYERS+1))

echo "Successfully verified $PASSED_LAYERS / 6 DevSecOps Security Layers."

if [ "$PASSED_LAYERS" -eq 6 ]; then
    echo "MIDTERM EXAM 2 STATUS: PASSED WITH DISTINCTION (100%)"
    exit 0
else
    echo "MIDTERM EXAM 2 STATUS: INCOMPLETE"
    exit 1
fi
```

Cho phép script chạy và kiểm tra kết quả cuối cùng:
```bash
chmod +x scripts/final-exam-evaluation.sh
./scripts/final-exam-evaluation.sh
```

### **CHECKPOINT 14**
Chạy câu lệnh tổng kết bài kiểm tra giữa kỳ 2:

```bash
./scripts/final-exam-evaluation.sh | grep -q "DISTINCTION" && echo "CHECKPOINT 14: ĐẠT" || echo "CHECKPOINT 14: LỖI"
```

**Kết quả kỳ vọng:**
```text
CHECKPOINT 14: ĐẠT
```

---

## Xử lý sự cố

### 1. Sự cố Script `security-gate-parser.sh` nổ lỗi `jq: command not found`
- **Triệu chứng:** Pipeline báo lỗi lệnh `jq` không tồn tại ở stage `layer6-security-gate`.
- **Nguyên nhân:** Image của CI Runner không cài đặt công cụ xử lý JSON `jq`.
- **Cách khắc phục:** Thêm bước `apk add --no-cache jq` hoặc `apt-get install -y jq` trước khi gọi script parser.

### 2. Sự cố Tệp `reports/gitleaks-report.json` bị mất do `artifacts:paths` khai báo sai
- **Triệu chứng:** Job gate báo `Missing Gitleaks report artifact`.
- **Nguyên nhân:** Khai báo sai đường dẫn tương đối trong tệp `.gitlab-ci.yml`.
- **Cách khắc phục:** Đảm bảo thư mục `reports/` được tạo thống nhất và khai báo đúng trong `artifacts:paths`.

### 3. Sự cố Script `check-allowlist-audit.sh` đánh nổ lỗi build do quá hạn ngày ISO 8601
- **Triệu chứng:** Script báo `Allowlist entry EXPIRED`.
- **Nguyên nhân:** Ngày trong comment tệp `.trivyignore` đã nhỏ hơn ngày hiện tại của hệ thống.
- **Cách khắc phục:** Kiểm tra với Security Lead để gia hạn ngày expiration hoặc sửa triệt để CVE để gỡ khỏi ignore file.

### 4. Sự cố OIDC Vault Authentication bị từ chối `403 Forbidden`
- **Triệu chứng:** Job Vault lấy token bị lỗi JWT claim mismatch.
- **Nguyên nhân:** Biến `aud` (audience) trong tệp CI không khớp với cấu hình OIDC Role trên Vault.
- **Cách khắc phục:** Cấu hình đúng cờ `bound_audiences` trên Vault role khớp với tham số `aud` trong `id_tokens`.

### 5. Sự cố Trivy Scanner không nhận diện được tệp `.trivyignore`
- **Triệu chứng:** Trivy vẫn quét ra CVE đã nằm trong tệp ignore.
- **Nguyên nhân:** Tệp ignore không đặt ở thư mục gốc của dự án hoặc thiếu cờ `--ignorefile .trivyignore`.
- **Cách khắc phục:** Truyền cờ `trivy image --ignorefile .trivyignore` trong script scan.

### 6. Sự cố Cosign Sign báo lỗi `missing OIDC token`
- **Triệu chứng:** Lệnh ký số keyless cosign bị thất bại ở Lớp 5.
- **Nguyên nhân:** CI job chưa khai báo trường `id_tokens` để cấp danh tính OIDC cho Cosign.
- **Cách khắc phục:** Thêm mục `id_tokens: SIGSTORE_ID_TOKEN: aud: sigstore` vào job cấu hình ký số.

### 7. Sự cố `checkov` bị timeout khi quét tệp Kubernetes Manifest quá to
- **Triệu chứng:** Job Layer 2 IaC scan bị treo 15 phút.
- **Nguyên nhân:** Checkov cố gắng tải các framework external kiểm thử.
- **Cách khắc phục:** Thêm cờ `checkov --framework kubernetes --skip-download` để chạy offline tốc độ cao.

### 8. Sự cố Tệp `sbom.spdx.json` sinh ra bị rỗng 0 byte
- **Triệu chứng:** Syft không trích xuất được danh mục package.
- **Nguyên nhân:** Image chưa được build xong hoặc target image name bị gõ sai cú pháp.
- **Cách khắc phục:** Đảm bảo stage `container-build` hoàn tất thành công trước khi gọi `syft`.

### 9. Sự cố Biến `EMERGENCY_SECURITY_BYPASS` không hoạt động khi được truyền ở commit message
- **Triệu chứng:** Gate vẫn hard-fail dù commit message chứa `BYPASS`.
- **Nguyên nhân:** Script parser chỉ kiểm tra biến CI/CD Protected Variable chứ không đọc commit message để đảm bảo an ninh.
- **Cách khắc phục:** Khai báo biến `EMERGENCY_SECURITY_BYPASS` trong GitLab CI/CD Variables Settings.

### 10. Sự cố Job `security-gate` bị bỏ qua do `needs` khai báo sai
- **Triệu chứng:** Pipeline chạy xong Stage 5 nhưng dừng lại không chạy Stage 6.
- **Nguyên nhân:** Cấu hình `needs` bị sót các job phụ thuộc ở stage trước.
- **Cách khắc phục:** Kiểm tra và khai báo đầy đủ các job cần lấy artifacts trong thuộc tính `needs`.

### 11. Sự cố Lỗi cú pháp TOML/YAML trong tệp quy tắc OPA Rego
- **Triệu chứng:** Conftest báo `rego parse error: unexpected token`.
- **Nguyên nhân:** Thiếu từ khóa `package main` hoặc sai cú pháp gán biến `:=`.
- **Cách khắc phục:** Sử dụng lệnh `opa check policies/` để lint tệp Rego trước khi đưa vào CI.

### 12. Sự cố Tệp `audit-trail.log` bị mất sau khi pipeline kết thúc
- **Triệu chứng:** Không tìm thấy log audit khi xảy ra sự cố bypass.
- **Nguyên nhân:** Job Quality Gate thiếu khai báo lưu trữ artifact cho tệp `audit-trail.log`.
- **Cách khắc phục:** Bổ sung `artifacts:paths: - reports/audit-trail.log` với thời hạn `expire_in: 90 days`.

### 13. Sự cố `semgrep` ngốn quá nhiều RAM gây crash Runner Docker
- **Triệu chứng:** Job Layer 1 bị ngắt với lỗi `OOMKilled`.
- **Nguyên nhân:** Quét mã nguồn trong thư mục tạm `node_modules` hoặc `.git`.
- **Cách khắc phục:** Bổ sung tệp `.semgrepignore` để loại trừ các thư mục phụ thuộc không cần thiết.

### 14. Sự cố Chữ ký Cosign bị từ chối khi verify trên Kubernetes Cluster
- **Triệu chứng:** Pod không tạo được với lỗi `ImageSignatureVerificationFailed`.
- **Nguyên nhân:** Subject email hoặc OIDC Issuer URL trong Policy của Kyverno bị lệch so với chứng chỉ của Runner.
- **Cách khắc phục:** Khai báo khớp cờ `issuer: https://gitlab.company.internal` trong Kyverno ClusterPolicy.

### 15. Sự cố Tệp `gl-security-report.json` không hiển thị trên Merge Request Tab
- **Triệu chứng:** GitLab UI không tự động gom báo cáo an ninh.
- **Nguyên nhân:** Khai báo sai thuộc tính `reports:sast` hoặc `reports:container_scanning` trong tệp CI.
- **Cách khắc phục:** Sử dụng đúng cú pháp `artifacts:reports:container_scanning: reports/trivy-report.json`.

### 16. Sự cố Multiline comment trong tệp `.trivyignore` bị script audit parse sai
- **Triệu chứng:** Script audit báo `invalid format` ở các dòng comment giải thích dài.
- **Nguyên nhân:** Regex parser chưa xử lý được các dòng bắt đầu bằng dấu `#` mà không theo mẫu chuẩn.
- **Cách khắc phục:** Bổ sung câu lệnh kiểm tra `[[ "$line" =~ ^#\ CVE ]]` để chỉ audit các dòng chứa thông tin CVE.

### 17. Sự cố Vault Dynamic Lease bị thu hồi sớm làm Job Build bị ngắt giữa chừng
- **Triệu chứng:** Job đang build thì bị lỗi `401 Unauthorized` khi kết nối DB.
- **Nguyên nhân:** Lease TTL của Vault Token được đặt quá ngắn ($< 60$ seconds).
- **Cách khắc phục:** Tăng Lease TTL lên 15-30 phút cho phù hợp với thời gian thực thi của pipeline.

### 18. Sự cố `syft` sinh báo cáo SBOM sai chuẩn định dạng SPDX
- **Triệu chứng:** OPA Gatekeeper từ chối tệp JSON SBOM do thiếu trường `spdxVersion`.
- **Nguyên nhân:** Dùng cờ `-o json` mặc định của Syft thay vì cờ `-o spdx-json`.
- **Cách khắc phục:** Sử dụng chính xác câu lệnh `syft $IMAGE -o spdx-json=reports/sbom.spdx.json`.

### 19. Sự cố Git History bị thiếu làm Gitleaks quét không triệt để
- **Triệu chứng:** Gitleaks bỏ qua các secret đã bị xóa ở commit cũ.
- **Nguyên nhân:** Runner cấu hình `GIT_DEPTH: 1` (Shallow Clone).
- **Cách khắc phục:** Đặt cờ `GIT_DEPTH: 0` hoặc `GIT_DEPTH: 50` cho job Secret Scanning.

### 20. Sự cố Script `final-exam-evaluation.sh` báo lỗi `INCOMPLETE` dù cả 6 job đều xanh
- **Triệu chứng:** Đánh giá bài thi bị 0 điểm.
- **Nguyên nhân:** Các tệp báo cáo JSON nằm rải rác ở các thư mục khác nhau thay vì gom về `reports/`.
- **Cách khắc phục:** Đảm bảo tất cả các script Lớp 1 đến Lớp 6 đều xuất file báo cáo vào thư mục chuẩn `reports/`.

### 21. Sự cố Lỗi nạp biến môi trường `$CI_REGISTRY_IMAGE` khi chạy local runner
- **Triệu chứng:** Script build container báo `invalid repository name`.
- **Nguyên nhân:** Chạy script local không có sẵn các biến mặc định của GitLab CI.
- **Cách khắc phục:** Thêm giá trị fallback mặc định `REGISTRY_IMAGE=${CI_REGISTRY_IMAGE:-registry.local/app}` ở đầu script.

### 22. Sự cố Gate Parser báo pass khi tệp `trivy-report.json` rỗng
- **Triệu chứng:** Container có 10 lỗ hổng Critical nhưng Gate vẫn báo APPROVED.
- **Nguyên nhân:** File JSON bị rỗng do lệnh quét bị lỗi giữa chừng nhưng vẫn xuất file 0 byte.
- **Cách khắc phục:** Bổ sung kiểm tra kích thước file `[ -s reports/trivy-report.json ]` trước khi parse.

### 23. Sự cố `conftest test` không tìm thấy thư mục chính sách `policies/`
- **Triệu chứng:** Job Layer 6 nổ lỗi `no policies found`.
- **Nguyên nhân:** Đường dẫn tệp `.rego` bị truyền sai tham số.
- **Cách khắc phục:** Chỉ định rõ cờ `conftest test --policy policies/ reports/`.

### 24. Sự cố Quá tải CPU Runner do chạy 6 job scan cùng một lúc
- **Triệu chứng:** Runner bị đơ, các job bị ngắt giữa chừng do hết tài nguyên host.
- **Nguyên nhân:** Cấu hình concurrent runner vượt quá khả năng phần cứng máy chủ.
- **Cách khắc phục:** Điều chỉnh cờ `concurrent = 3` trong tệp `config.toml` của GitLab Runner.

### 25. Sự cố Xung đột phiên bản Go trong Dockerfile Multi-stage
- **Triệu chứng:** Lỗi `undefined: net.ListenConfig` khi compile app Go.
- **Nguyên nhân:** Stage builder dùng Go version cũ hơn version yêu cầu trong `go.mod`.
- **Cách khắc phục:** Đồng bộ phiên bản `golang:1.22-alpine` ở Stage 1 của Dockerfile.

### 26. Sự cố Permission Denied khi script cố ghi tệp `audit-trail.log`
- **Triệu chứng:** Job gate nổ lỗi `cannot create reports/audit-trail.log: Permission denied`.
- **Nguyên nhân:** Thư mục `reports/` được tạo bởi user root ở container trước.
- **Cách khắc phục:** Thêm câu lệnh `chmod -R 777 reports/` hoặc chạy script với user phù hợp.

### 27. Sự cố `checkov` bỏ qua tệp `.dockerfile` không đúng đuôi tên
- **Triệu chứng:** Dockerfile bị bỏ qua không quét an ninh IaC.
- **Nguyên nhân:** Tệp đặt tên là `Dockerfile.dev` nhưng Checkov mặc định chỉ tìm `Dockerfile`.
- **Cách khắc phục:** Truyền cờ `checkov -f Dockerfile.dev --framework dockerfile`.

### 28. Sự cố Webhook bắn tin Slack khi Emergency Bypass thất bại do thiếu cờ `--silent`
- **Triệu chứng:** Job gate bị treo 2 phút ở bước cắm curl.
- **Nguyên nhân:** Mạng Runner không kết nối được tới internet để tới API Slack.
- **Cách khắc phục:** Thêm cờ `--connect-timeout 5` để ngắt chờ kết nối nhanh.

### 29. Sự cố `gitleaks` báo lỗi `failed to load custom gitleaks.toml`
- **Triệu chứng:** Job Secret scan bị ngắt do sai cú pháp TOML.
- **Nguyên nhân:** Tệp `gitleaks.toml` thiếu dấu ngoặc vuông `[]` ở tên rule.
- **Cách khắc phục:** Kiểm tra cú pháp TOML bằng công cụ `gitleaks detect --config gitleaks.toml`.

### 30. Sự cố Tệp `gl-security-dashboard-report.json` bị mất thuộc tính `scan.scanner.name`
- **Triệu chứng:** GitLab UI từ chối nạp báo cáo JSON với lỗi `missing scanner name`.
- **Nguyên nhân:** Tệp JSON tự xuất thiếu trường định danh tên scanner.
- **Cách khắc phục:** Bắt buộc đính kèm `"scanner": {"id": "gitlab-security", "name": "Security Dashboard"}`.

### 31. Sự cố `check-allowlist-audit.sh` nổ lỗi `cannot parse Expiration Date format`
- **Triệu chứng:** Script audit báo lỗi định dạng ngày trên dòng comment của tệp `.trivyignore`.
- **Nguyên nhân:** Soạn thảo sai định dạng ngày `Expire: DD-MM-YYYY` thay vì `YYYY-MM-DD` chuẩn ISO 8601.
- **Cách khắc phục:** Ép buộc định dạng ngày `Expire: YYYY-MM-DD` trong tệp ignore.

### 32. Sự cố Multi-stage Quality Gate bị treo 10 phút do không thể kết nối tới Registry
- **Triệu chứng:** Job container scan bị timeout ở bước kéo Image.
- **Nguyên nhân:** Mạng CI Runner bị nghẽn đường truyền HTTPS kết nối Docker Registry.
- **Cách khắc phục:** Cấu hình cờ `trivy image --timeout 2m` ngắt chờ nhanh.

### 33. Sự cố Tệp `gl-security-dashboard-report.json` bị rỗng dữ liệu khi `checkov` bị cancel
- **Triệu chứng:** GitLab UI không hiển thị kết quả kiểm thử IaC Security.
- **Nguyên nhân:** Lệnh `checkov` bị timeout và không xuất ra tệp JSON.
- **Cách khắc phục:** Thêm cờ `checkov --soft-fail` ở bước tạo báo cáo JSON nháp.

### 34. Sự cố Biến `EMERGENCY_SECURITY_BYPASS` bị lập trình viên tự gõ ở Commit Message
- **Triệu chứng:** CI Pipeline tự động bypass Quality Gate khi commit message chứa chuỗi `SEC-999`.
- **Nguyên nhân:** Script CI kiểm tra `$CI_COMMIT_MESSAGE` thay vì biến Protected CI Variable.
- **Cách khắc phục:** Chỉ kiểm tra biến môi trường Protected & Masked `EMERGENCY_SECURITY_BYPASS`.

### 35. Sự cố Tệp `.trivyignore` bị xóa mất bởi lập trình viên ở nhánh con
- **Triệu chứng:** CI Pipeline ở nhánh Feature bị đỏ ngầu do không tìm thấy tệp ignore.
- **Nguyên nhân:** Lập trình viên lỡ tay rebase xóa mất tệp `.trivyignore`.
- **Cách khắc phục:** Đảm bảo script CI tự động kiểm tra `if [ -f .trivyignore ]; then ... fi` trước khi scan.

### 36. Sự cố CODEOWNERS không chặn được Merge Request khi chưa có phê duyệt của Security Lead
- **Triệu chứng:** Developer tự bấm Merge MR sửa tệp Ignore mà không cần ai duyệt.
- **Nguyên nhân:** Chưa bật cờ `Prevent approval by author` trong Merge Request Approval Rules.
- **Cách khắc phục:** Bật cờ `Prevent approval by author` trên GitLab Project Settings.

### 37. Sự cố `gitleaks detect` báo lỗi `failed to load custom gitleaks.toml config`
- **Triệu chứng:** Job secret scan bị ngắt do sai cú pháp TOML.
- **Nguyên nhân:** Tệp `gitleaks.toml` thiếu ngoặc vuông `[]` ở tên rule.
- **Cách khắc phục:** Kiểm tra cú pháp TOML bằng công cụ `gitleaks detect --config gitleaks.toml`.

### 38. Sự cố Tệp `reports/opa-evaluation.json` bị từ chối do sai kiểu dữ liệu timestamp
- **Triệu chứng:** GitLab UI từ chối nạp báo cáo JSON với lỗi `invalid ISO 8601 timestamp`.
- **Nguyên nhân:** Script gom báo cáo in timestamp dạng Unix epoch thay vì ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).
- **Cách khắc phục:** Sử dụng câu lệnh `date -u +"%Y-%m-%dT%H:%M:%SZ"` để format timestamp chuẩn.

### 39. Sự cố Script `check-allowlist-audit.sh` bị dừng do hết đĩa đĩa đĩa đệm tạm `/tmp`
- **Triệu chứng:** Script audit báo `no space left on device` trên CI Runner host.
- **Nguyên nhân:** Thư mục giải nén tạm `/tmp` của Runner bị phình quá to.
- **Cách khắc phục:** Khai báo cờ `TMPDIR=.tmp/` lưu đệm đệm trực tiếp trong workspace dự án.

### 40. Sự cố Security Quality Gate không ngắt được pipeline do cờ `allow_failure: true` trên template
- **Triệu chứng:** Semgrep báo đỏ 3 lỗ hổng SAST Critical nhưng Merge Request vẫn cho phép bấm nút Merge.
- **Nguyên nhân:** Kế thừa template GitLab Compliance mặc định có sẵn cờ `allow_failure: true`.
- **Cách khắc phục:** Đè thuộc tính `sast-semgrep-scan: allow_failure: false` trong `.gitlab-ci.yml`.

### 41. Sự cố `gitleaks detect` nổ lỗi `cannot parse git history` trên Shallow Clone Runner
- **Triệu chứng:** Job secret scan bị crash khi Runner cấu hình `GIT_DEPTH: 1`.
- **Nguyên nhân:** Gitleaks cần nạp lịch sử Git commit history để phát hiện các secret bị xóa ở commit cũ.
- **Cách khắc phục:** Đặt cờ `gitleaks detect --no-git` hoặc tăng `GIT_DEPTH: 50`.

### 42. Sự cố Multi-stage Quality Gate không gửi được báo cáo an ninh do thiếu `artifacts:expire_in`
- **Triệu chứng:** Các tệp báo cáo JSON bị xóa mất sau 1 giờ khiến Merge Request Widget bị hỏng.
- **Nguyên nhân:** Kế thừa cấu hình dọn dẹp artifacts ngắn hạn.
- **Cách khắc phục:** Khai báo cờ `artifacts:expire_in: 30 days` cho các tệp báo cáo Security JSON.

### 43. Sự cố Script `check-allowlist-audit.sh` thất bại do không hỗ trợ khoảng trắng trong đường dẫn tệp
- **Triệu chứng:** Script báo `file not found` khi chạy ở thư mục có chứa khoảng trắng.
- **Nguyên nhân:** Biến đường dẫn không được bọc trong dấu ngoặc kép `"$IGNORE_FILE"`.
- **Cách khắc phục:** Bọc tất cả tham số đường dẫn tệp bằng dấu double quotes `"$IGNORE_FILE"`.

### 44. Sự cố Custom Rule OPA / Rego báo lỗi `undefined decision`
- **Triệu chứng:** Policy Engine từ chối pipeline với lỗi không xác định được kết quả đánh giá.
- **Nguyên nhân:** Tệp chính sách Rego thiếu khai báo giá trị mặc định `default allow = false`.
- **Cách khắc phục:** Khai báo quy tắc mặc định `default allow = false` ở đầu gói chính sách Rego.

### 45. Sự cố Quality Gate ngắt pipeline sai do tệp báo cáo JSON bị hỏng định dạng Unicode
- **Triệu chứng:** Lệnh `jq` báo lỗi `invalid UTF-8 byte sequence` khi đọc kết quả scan.
- **Nguyên nhân:** Công cụ scan trên Windows Runner xuất file với encoding UTF-16LE có BOM.
- **Cách khắc phục:** Chuyển đổi mã hóa bằng `iconv -f UTF-16LE -t UTF-8` trước khi đưa vào pipeline parser.

### 46. Sự cố Pipeline bị treo vô tận do `cosign sign` chờ nhập mật khẩu passphrase
- **Triệu chứng:** Job Layer 5 supply chain bị hang không phản hồi ở bước ký số.
- **Nguyên nhân:** Thiếu cờ `--yes` làm Cosign mở prompt hỏi xác nhận tương tác terminal.
- **Cách khắc phục:** Luôn đính kèm cờ `cosign sign --yes` khi thực thi trong môi trường CI/CD tự động.

### 47. Sự cố `syft` báo lỗi `failed to inspect image` trên private registry
- **Triệu chứng:** Job xuất SBOM bị ngắt với lỗi authentication error.
- **Nguyên nhân:** Syft không có quyền kéo image từ Private Docker Registry.
- **Cách khắc phục:** Truyền biến môi trường `SYFT_CONTAINER_IMAGE_EXECUTIVE_AUTH_USERNAME` và `SYFT_CONTAINER_IMAGE_EXECUTIVE_AUTH_PASSWORD`.

### 48. Sự cố Tệp `audit-trail.log` bị lộ secret khi ứng dụng log full environment variables
- **Triệu chứng:** File audit chứa các token nhạy cảm ở dạng plain text.
- **Nguyên nhân:** Script gate ghi log `env` công khai mà không sanitize.
- **Cách khắc phục:** Sử dụng `grep -v -E "(TOKEN|SECRET|PASSWORD)"` lọc sạch secret trước khi append vào file audit.

---

## Bài tập mở rộng

1. **Tích hợp DAST (Dynamic Application Security Testing) vào Bài Thi Giữa Kỳ:**
   - Bổ sung Stage 7 `layer7-dast-scan` vào `.gitlab-ci.yml` sử dụng OWASP ZAP Baseline Scan.
   - Cấu hình cho DAST chạy sau khi container app đã được deploy thử nghiệm ở môi trường ephemeral staging.
   - Gom báo cáo DAST JSON vào script Quality Gate Parser để kiểm tra lỗ hổng XSS và Missing Security Headers ở môi trường runtime.

2. **Xây dựng Dashboard Giám sát Nợ An ninh Tập trung (Centralized Security Debt Dashboard):**
   - Viết script Python tự động thu thập tất cả các tệp `reports/*.json` từ các pipeline vừa hoàn thành bài thi giữa kỳ.
   - Đẩy dữ liệu lỗ hổng về ElasticSearch / DefectDojo để vẽ biểu đồ theo dõi MTTR và số lượng CVE tồn đọng toàn công ty theo thời gian thực.

---

## Bảng đối soát thời lượng

| Mục | Nội dung | Thời lượng |
|---|---|---|
| Bước 1 | Khởi tạo Cấu trúc Dự án và Mã nguồn Đơn vị | 10 phút |
| Bước 2 | Tích hợp Lớp 1 — Secret Scanning & SAST Code Scan | 15 phút |
| Bước 3 | Tích hợp Lớp 2 — Infrastructure as Code (IaC) Scan | 10 phút |
| Bước 4 | Tích hợp Lớp 3 — Vault OIDC Token Retrieval | 10 phút |
| Bước 5 | Tích hợp Lớp 4 — Multi-stage Docker Build & Container Scan | 15 phút |
| Bước 6 | Tích hợp Lớp 5 — Syft SBOM & Cosign Image Signature | 15 phút |
| Bước 7 | Tích hợp Lớp 6 — Policy-as-Code Rego Enforcement | 15 phút |
| Bước 8 | Tạo Tệp Allowlist Waiver có Hạn dùng ISO 8601 | 10 phút |
| Bước 9 | Xây dựng Multi-stage Security Quality Gate Parser | 15 phút |
| Bước 10 | Thử nghiệm Kịch bản Hard-Fail khi phát hiện Secret | 10 phút |
| Bước 11 | Kiểm thử Kịch bản Emergency Bypass Khẩn cấp | 10 phút |
| Bước 12 | Dọn dẹp Trạng thái Bypass và Khôi phục Clean State | 5 phút |
| Bước 13 | Xây dựng tệp `.gitlab-ci.yml` Tích hợp 6 Stage Hoàn chỉnh | 10 phút |
| Bước 14 | Tổng hợp Báo cáo và Đánh giá Hoàn thành Bài thi Giữa Kỳ 2 | 5 phút |
| **Tổng** | **Khối thực hành lab** | **150'** |

---

## 3. Bộ Câu Hỏi Vấn Đáp & Phỏng Vấn Kỹ Thuật Chuyên Sâu

Dưới đây là bộ câu hỏi phỏng vấn thực chiến dành cho các vị trí **DevOps Engineer**, **DevSecOps Specialist** và **Platform Infrastructure Lead**, giúp bạn tự đánh giá độ sâu hiểu biết và rèn luyện phản xạ giải quyết vấn đề hệ thống:

# Buổi 35: Kiểm Tra Giữa Kỳ 2 — Vấn Đáp & Phỏng Vấn DevSecOps

## Thống kê & Phân bổ thời lượng
- **Tổng thời lượng:** 20 phút
- **Cấu trúc:**
  - 5 phút: Kiểm tra phản xạ lý thuyết tổng hợp DevSecOps (12 câu hỏi trắc nghiệm & tự luận nhanh)
  - 10 phút: Đóng vai phỏng vấn tình huống thực chiến cao cấp (7 kịch bản kiến trúc & sự cố)
  - 5 phút: Chốt từ khóa ăn tiền (§V3) & Giao bài tập về nhà mở đầu Giai đoạn 6 (BTVN 4)

---

## §V1. 12 Câu hỏi vấn đáp kiểm tra phản xạ giữa kỳ 2

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Gợi ý trả lời ngắn:</b>
Phòng thủ 6 lớp bao gồm: Secret/Code SAST (1), IaC Security (2), Vault Authentication (3), Container Scan (4), Supply Chain SBOM/Cosign (5) và Policy Quality Gate (6). Thiếu bất kỳ lớp nào cũng tạo ra một mắt xích yếu nhất để hacker tấn công vào chuỗi cung ứng.

<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Kiến trúc 6 Lớp:</b></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> *Lớp 1 (Code & Secret):* Gitleaks + Semgrep SAST ngăn ngừa rò rỉ API key và lỗi lập trình logic từ bước viết mã.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> *Lớp 2 (Infrastructure as Code):* Checkov kiểm tra tính an toàn của Dockerfile, Kubernetes Manifests và Terraform files.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> *Lớp 3 (Identity & Dynamic Access):* HashiCorp Vault OIDC JWT cung cấp credential tạm thời tự hủy dưới 60 phút.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">4.</b> *Lớp 4 (Container Image Security):* Trivy quét lỗ hổng OS packages và application dependencies trên Distroless image.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">5.</b> *Lớp 5 (Supply Chain Security):* Syft xuất SBOM và Cosign ký số Keyless chứng thực nguồn gốc SLSA Provenance.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">6.</b> *Lớp 6 (Governance & Quality Gate):* OPA/Conftest Rego evaluation kiểm định quy tắc doanh nghiệp và Parser ngắt pipeline.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Rủi ro khi thiếu lớp:</b> Ví dụ, nếu ứng dụng có SAST pass 100% nhưng thiếu Container Scan (Lớp 4) $\to$ Base Image Alpine chứa CVE RCE vẫn lọt lên Prod; nếu có Container Scan nhưng thiếu Cosign Signature (Lớp 5) $\to$ Hacker có thể tráo Image nguy hiểm trực tiếp trên Registry.</div>

<b style="color: var(--accent-primary);">Bẫy tuyển dụng / Trả lời sai hay gặp:</b>
Trả lời qua loa "DevSecOps là cài SonarQube với Trivy là xong". Cần phân tích sâu cả 6 lớp từ Code đến Supply Chain & Policy Enforcement.
</div>
</details>

---

### Câu 2
**Hỏi:** Tại sao OIDC Federated Identity lại là chuẩn mực vàng để thay thế biến môi trường tĩnh (Static Masked CI Variables) khi kết nối với HashiCorp Vault hoặc Cloud Providers?

**Gợi ý trả lời ngắn:**
OIDC sử dụng JWT Token ngắn hạn do GitLab cấp theo từng pipeline execution, tự động hết hạn và không cần lưu trữ Secret/Password tĩnh trên Runner hay GitLab Project.

**Đáp án chuẩn:**
- **Hạn chế của Static Variables:** Biến tĩnh dù được tick `Masked` hay `Protected` vẫn có thể bị rò rỉ qua log đệm, file dump khi runner bị chiếm quyền, không tự động xoay vòng (Rotate), và tạo nguy cơ credential tồn tại vĩnh viễn (Long-lived secret vulnerability).
- **Nguyên lý OIDC Federation:**
  1. GitLab Runner tự động sinh ra một token dạng JWT (JSON Web Token) ngắn hạn thông qua trường `id_tokens` trong job.
  2. Runner gửi JWT này sang Vault hoặc AWS STS / GCP WIF với claim `sub` (Subject Identity: bao gồm repo URL, branch name, commit SHA).
  3. Identity Provider xác minh tính hợp lệ của chữ ký JWT $\to$ Cấp một Temporary Access Token có TTL ngắn (15-30 phút).
  4. Hết thời gian lease, token tự hủy hoàn toàn. Nếu hacker lấy được token này cũng không kịp làm gì.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Nhầm lẫn OIDC với SSH Key hay Personal Access Token. Cần nhấn mạnh tính chất **Short-lived (ngắn hạn)** và **Zero Static Credentials**.

---

### Câu 3
**Hỏi:** Phân biệt cơ chế hoạt động và vai trò của SBOM (Software Bill of Materials) và SLSA Provenance Attestation trong an ninh chuỗi cung ứng.

**Gợi ý trả lời ngắn:**
SBOM là "danh mục thành phần phần mềm" (bên trong có thư viện gì, version bao nhiêu). SLSA Provenance là "chứng minh nhân dân của Artifact" (ai build, từ commit nào, trên runner nào, môi trường ra sao).

**Đáp án chuẩn:**
- **SBOM (Software Bill of Materials):**
  - *Định dạng chuẩn:* SPDX, CycloneDX (tạo bởi công cụ Syft/Trivy).
  - *Mục đích:* Giúp Doanh nghiệp tra cứu tức thì toàn bộ ứng dụng bị ảnh hưởng khi xuất hiện lỗ hổng 0-day mới (ví dụ vụ Log4j 2021). Thay vì phải scan lại 1,000 repo, chỉ cần query DB SBOM trong 5 giây.
- **SLSA Provenance Attestation:**
  - *Định dạng chuẩn:* In-toto Attestation, Cosign Bundle.
  - *Mục đích:* Chứng minh tính toàn vẹn và nguồn gốc hợp pháp của Container Image. Giúp Kubernetes Admission Controller (Kyverno/OPA Gatekeeper) đảm bảo Image sắp chạy đúng là do GitLab CI chính chủ build từ commit SHA hợp lệ chứ không phải do hacker upload trộm.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Gộp chung SBOM và Provenance làm một. Ứng viên giỏi phải chỉ rõ SBOM là kiểm kê thành phần, Provenance là xác minh quy trình xuất xứ.

---

### Câu 4
**Hỏi:** Làm thế nào để thiết kế một hệ thống Security Quality Gate vừa đảm bảo an toàn tuyệt đối cho nhánh `main` vừa không làm đứt gãy năng suất làm việc của Dev ở nhánh `feature`?

**Gợi ý trả lời ngắn:**
Áp dụng chiến lược Phân cấp Ngưỡng rủi ro theo Ngữ cảnh: Hard-fail (ngắt pipeline ngay lập tức) trên nhánh `main` đối với lỗi Critical/High, và Soft-fail (chỉ cảnh báo Warning) trên nhánh `feature`.

**Đáp án chuẩn:**
- **Phân tách Ngữ cảnh Pipeline (Context-aware Enforcement):**
  - *Feature Branch Pipeline (Pre-merge):* Chạy Incremental Scan, bật cờ `GATE_STRICT=false`. Đóng vai trò làm công cụ hỗ trợ Dev phát hiện sớm lỗi (Shift-Left Feedback Loop). Nếu có lỗi, CI vẫn hiện cảnh báo vàng nhưng không block công việc dev nháp.
  - *Main / Release Branch Pipeline (Pre-deploy):* Bật cờ `GATE_STRICT=true`. Áp dụng Hard-Fail tuyệt đối đối với `Critical_Count > 0` hoặc phát hiện Secret rò rỉ.
- **Cơ chế Expiration Waiver (Duyệt Ngoại lệ):** Cung cấp tệp ignore có ngày hết hạn để unblock Dev đối với các lỗi Third-party Vendor chưa có bản vá, dưới sự approve bắt buộc của Security Lead trên CODEOWNERS.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cực đoan một chiều: Hoặc hard-fail ở tất cả các nhánh làm dev nản lòng, hoặc soft-fail khắp nơi làm gate mất tác dụng.

---

### Câu 5
**Hỏi:** Ngôn ngữ Rego và công cụ Conftest / OPA được ứng dụng như thế nào để hiện thực hóa triết lý Policy-as-Code trong GitLab CI?

**Gợi ý trả lời ngắn:**
Conftest sử dụng ngôn ngữ Rego để viết các quy tắc chính sách dưới dạng mã nguồn (Code). Job CI dùng Conftest kiểm định các tệp báo cáo JSON/YAML xem có vi phạm quy định tổ chức hay không.

**Đáp án chuẩn:**
- **Nguyên lý Policy-as-Code:** Chuyển đổi các văn bản quy định an ninh khô khan thành các tệp luật Rego thực thi được tự động.
- **Tích hợp Conftest trong CI:**
  ```rego
  package main
  deny[msg] {
    input.vulnerabilities[_].severity == "CRITICAL"
    msg := sprintf("CRITICAL CVE Detected: %v", [input.vulnerabilities[_].id])
  }
  ```
- **Lợi ích Enterprise:** Tách rời hoàn toàn Logic chính sách an ninh khỏi tệp `.gitlab-ci.yml`. Tệp luật Rego được bảo quản tập trung tại repo bảo mật, có thể viết Unit Test cho chính luật (`conftest test policy_test.rego`), và tái sử dụng cho hàng ngàn dự án khác nhau.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Nhầm Rego với các câu lệnh `jq` hay Bash script đơn thuần. Cần nhấn mạnh tính chất Khai báo (Declarative Policy Engine) của OPA.

---

### Câu 6
**Hỏi:** Khi một lỗ hổng 0-day Critical xuất hiện trên base image sản xuất mà Vendor chưa kịp tung ra bản vá (No Fix Available), quy trình xử lý ngoại lệ an ninh (Exception Waiver Workflow) chuẩn sẽ diễn ra như thế nào?

**Gợi ý trả lời ngắn:**
Kích hoạt quy trình đánh giá rủi ro VEX $\to$ Áp dụng biện pháp bọc đệm (Mitigating Control) $\to$ SecLead approve một dòng ignore trong tệp allowlist có ngày hết hạn (Expiration Date) ngắn hạn ($7-14$ ngày) và ticket JIRA theo dõi.

**Đáp án chuẩn:**
- **Bước 1: Đánh giá Rủi ro Thực tế (VEX/Exploitability Analysis):** AppSec Engineer kiểm tra xem tính năng bị ảnh hưởng bởi 0-day có thực sự được gọi thực thi trong container hay không.
- **Bước 2: Áp dụng Lớp phòng thủ bổ sung (Mitigating Controls):** Cấu hình WAF rule chặn payload tấn công, hoặc bật Seccomp/AppArmor profile cô lập container trên Kubernetes.
- **Bước 3: Tạo Temporary Expiration Waiver:**
  Thêm entry vào tệp `.trivyignore` ở repo quản trị với metadata bắt buộc:
  `# CVE-2024-XXXX | Expire: 2026-09-05 | ApprovedBy: @appsec-lead | Ticket: SEC-9901`
- **Bước 4: Automated Expiration Audit:** Script `check-allowlist-audit.sh` chạy hàng ngày. Nếu sau 14 ngày mà Vendor chưa ra patch và không được SecLead gia hạn, pipeline sẽ tự động nổ lỗi lại.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Trả lời "Sửa file ignore là xong". Cần trình bày đầy đủ quy trình 4 bước có kiểm soát rủi ro và ngày hết hạn tự động.

---

### Câu 7
**Hỏi:** Làm thế nào để đảm bảo các tệp báo cáo JSON/SARIF truyền giữa các Stage Scan và Stage Quality Gate trong GitLab CI không bị can thiệp làm giả dữ liệu (Artifact Tampering)?

**Gợi ý trả lời ngắn:**
Sử dụng cờ mã hóa artifact hash, thiết lập runner cách ly (Isolated Runner), khóa thuộc tính `artifacts:expire_in`, và cho job Quality Gate tự parse dữ liệu thô kết hợp với chữ ký checksum tệp.

**Đáp án chuẩn:**
- **Zero-trust Artifact Validation:** Job Quality Gate ở Lớp 6 không bao giờ tin vào exit status hay log hiển thị của các job scan Lớp 1-5. Gate bắt buộc kiểm tra sự tồn tại và tính toàn vẹn của tệp JSON thô.
- **Ghi vết SHA256 Checksum:** Job scan xuất file báo cáo kèm file checksum: `sha256sum trivy-report.json > trivy-report.json.sha256`. Job Gate verify checksum trước khi đọc dữ liệu.
- **GitLab Compliance Immutability:** Lưu giữ artifacts ở object storage an toàn và không cấp quyền ghi đè (overwrite) cho runner ở các stage sau.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Cho rằng artifacts trên GitLab mặc định là an toàn tuyệt đối. Cần chỉ ra các góc tấn công (như script job sau ghi đè file rỗng vào file báo cáo của job trước).

---

### Câu 8
**Hỏi:** Thiết kế tính năng "Emergency Security Bypass" cho phép vượt Quality Gate khi xảy ra sự cố Production sập khẩn cấp (Hotfix Incident) sao cho vừa linh hoạt vừa chống lạm dụng.

**Gợi ý trả lời ngắn:**
Kích hoạt thông qua biến Protected & Masked CI Variable `EMERGENCY_SECURITY_BYPASS`, chỉ cho phép SecLead/Maintainer bật, tự động ghi log Audit Trail không thể sửa xóa và gửi cảnh báo tức thời tới Slack/SIEM.

**Đáp án chuẩn:**
- **Nguyên tắc Quản trị:** Bỏ qua an ninh là quyết định kinh doanh có rủi ro (Business Risk Decision). Cần đảm bảo tính Minh bạch (Transparency) và Trách nhiệm giải trình (Accountability).
- **Thiết kế Kỹ thuật:**
  ```bash
  if [ "${EMERGENCY_SECURITY_BYPASS:-false}" = "true" ]; then
    echo "[WARNING] EMERGENCY BYPASS ACTIVATED BY $GITLAB_USER_LOGIN"
    echo "$(date -u) | BYPASS | User: $GITLAB_USER_LOGIN | Project: $CI_PROJECT_PATH" >> reports/audit-trail.log
    curl -X POST -d "🚨 User $GITLAB_USER_LOGIN bypassed Security Gate on $CI_PROJECT_NAME" $SLACK_SECURITY_WEBHOOK
    exit 0
  fi
  ```
- **Post-incident Audit:** Trong vòng 24h sau khi khắc phục sự cố Prod, ticket JIRA tự động yêu cầu gỡ bỏ biến bypass và sửa dứt điểm các lỗ hổng đã bị tạm qua mặt.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Nói rằng "Không bao giờ được phép bypass" (phi thực tế) hoặc "Cho phép dev gõ commit message `[skip ci]` để bypass" (mất kiểm soát an ninh).

---

### Câu 9
**Hỏi:** Làm thế nào để tối ưu thời gian thực thi của một Pipeline DevSecOps 6 lớp từ 25 phút xuống dưới 5 phút?

**Gợi ý trả lời ngắn:**
Áp dụng cơ chế chạy song song (Parallel execution với cờ `needs: []`), cache cơ sở dữ liệu lỗ hổng (Distributed Caching cho Trivy/Semgrep DB), và sử dụng Docker Socket / Fast Runner specs.

**Đáp án chuẩn:**
- **Tối ưu Cấu trúc Pipeline (DAG - Directed Acyclic Graph):**
  Cho các job scan độc lập (SAST, Secret, IaC) chạy song song ngay tại thời điểm bắt đầu pipeline bằng thuộc tính `needs: []`.
- **Cấu hình Distributed Caching:**
  Cache các thư mục chứa cơ sở dữ liệu lỗ hổng trên Runner (`~/.cache/trivy`, `~/.cache/semgrep`) để không phải tải lại 500MB DB mỗi lần chạy job.
- **Phân tách Loại Scan:**
  Chỉ chạy Incremental Fast Scan (quét phần diff code) trên Merge Request; dời các bài quét ngốn thời gian (Full Deep SAST, Full DAST) sang Schedule Pipeline đêm trên nhánh `main`.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Trả lời chung chung là "tăng RAM cho runner". Ứng viên xuất sắc phải phân tích ở góc độ cấu trúc pipeline DAG và caching strategy.

---

### Câu 10
**Hỏi:** Hai chỉ số DORA & DevSecOps KPI quan trọng nhất để đo lường mức độ trưởng thành của hệ thống phòng thủ CI/CD là gì?

**Gợi ý trả lời ngắn:**
Đó là Escaped Vulnerabilities (Số lỗ hổng lọt lưới lên Production) và MTTR - Mean Time to Remediate (Thời gian trung bình để phát hiện và vá lỗ hổng).

**Đáp án chuẩn:**
- **Chỉ số 1: Escaped Vulnerabilities Rate:**
  Đo lường số lượng lỗ hổng Critical/High lọt lên môi trường Prod được phát hiện bởi Bug Bounty, Pentest hoặc sự cố thực tế mà 6 lớp Security Gate ở CI/CD không chặn được. Chỉ số này phản ánh độ phủ (Coverage) và chất lượng của bộ Rule scanner.
- **Chỉ số 2: MTTR (Mean Time to Remediate):**
  Thời gian tính từ lúc Quality Gate phát hiện lỗ hổng cho đến khi bản vá được merge thành công.
  - SLA chuẩn Enterprise: Critical $< 24$ giờ, High $< 7$ ngày, Medium $< 30$ ngày.
- **Chỉ số phụ:** False Positive Rate (Tỷ lệ báo động giả) và Emergency Bypass Frequency (Tần suất bypass khẩn cấp).

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Trả lời bằng các chỉ số bề nổi như "Tổng số lần chạy scan" hay "Số lượng tool đã cài".

---

### Câu 11
**Hỏi:** Khi tích hợp 6 lớp scanner (Gitleaks, Semgrep, Checkov, Trivy, Syft, Conftest), làm sao để hiển thị kết quả hợp nhất trên giao diện Merge Request Widget của GitLab?

**Gợi ý trả lời ngắn:**
Cấu hình các công cụ xuất báo cáo theo đúng tên tệp và schema quy định của GitLab (`gl-sast-report.json`, `gl-secret-detection-report.json`, `gl-container-scanning-report.json`) trong mục `artifacts:reports`.

**Đáp án chuẩn:**
- **GitLab Security Reports Integration:**
  GitLab CI hỗ trợ hiển thị kết quả bảo mật trực quan ngay tại giao diện Merge Request Widget nếu job CI khai báo đúng thuộc tính `artifacts:reports`:
  ```yaml
  artifacts:
    reports:
      sast: reports/gl-sast-report.json
      secret_detection: reports/gitleaks-report.json
      container_scanning: reports/trivy-report.json
      cyclonedx: reports/sbom.cdx.json
  ```
- **Lợi ích:** Developer xem được dòng code bị lỗi, tên CVE, điểm CVSS và gợi ý khắc phục ngay trên giao diện MR mà không cần tải file log thô về máy.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Không biết đến tính năng Native Security Report Widget của GitLab, trả lời thủ công là bắt dev vào đọc console log của Runner.

---

### Câu 12
**Hỏi:** Tự động hóa quy trình phản ứng sự cố (Incident Response) khi Quality Gate bị ngắt trên nhánh chính `main` diễn ra như thế nào?

**Gợi ý trả lời ngắn:**
Script Quality Gate bắt mã lỗi `exit 1` $\to$ Gọi JIRA REST API tự động mở Ticket Bug ưu tiên Highest $\to$ Bắn cảnh báo về Slack Security Channel $\to$ Khóa luồng CD deployment.

**Đáp án chuẩn:**
- **Luồng Phản ứng Tự động (Zero-Touch Incident Response):**
  1. Job `layer6-security-gate` phân tích báo cáo phát hiện `Critical_Count > 0` trên nhánh `main`.
  2. Script CI tự động thu thập thông tin: `$CI_COMMIT_AUTHOR`, `$CI_COMMIT_SHA`, `$CI_PROJECT_URL`, danh sách CVE ID.
  3. Gọi REST API JIRA: `POST /rest/api/2/issue` tạo Bug Ticket tự động gán cho `$CI_COMMIT_AUTHOR`.
  4. Bắn thông báo Webhook về Slack/Microsoft Teams: "🚨 *Pipeline Main Blocked due to Security Gate Failure*".
  5. Đánh dấu trạng thái pipeline `Failed`, ngăn chặn tuyệt đối job `deploy-production` kích hoạt.

**Bẫy tuyển dụng / Trả lời sai hay gặp:**
Trả lời "Thấy build đỏ thì dev tự nhìn rồi tự lên JIRA tạo ticket". Phải thể hiện năng lực tự động hóa hoàn toàn quy trình Governance.

---

## §V2. Kịch bản phỏng vấn thực tế cao cấp (Roleplay Scenarios)

### Kịch bản 1: Đánh giá Năng lực Kiến trúc DevSecOps của Ứng viên
- **Người phỏng vấn (VP of Engineering):** *"Công ty chúng tôi sắp triển khai hệ thống Ngân hàng số trên Kubernetes. Em hãy phác thảo một kiến trúc phòng thủ DevSecOps hoàn chỉnh từ lúc dev push code đến khi container chạy trên Prod."*
- **Ứng viên (DevSecOps Specialist):**
  - *Trả lời:* "Báo cáo anh, em sẽ triển khai mô hình **Phòng thủ 6 Lớp tự động (6-Layer Defense in Depth)** khép kín trên GitLab CI/CD và Kubernetes:"
  - "1. **Lớp 1 (Code & Secret):** Chạy Gitleaks và Semgrep SAST ngay khi Dev tạo Merge Request để di chuyển an ninh về bên trái (Shift-Left)."
  - "2. **Lớp 2 (IaC Security):** Quét Dockerfile và Kubernetes Manifests bằng Checkov để chặn các lỗi như chạy root user hay thiếu resource limit."
  - "3. **Lớp 3 (Identity):** Dùng Vault OIDC JWT để sinh credential ngắn hạn (TTL 15 phút), không lưu bất kỳ password tĩnh nào trên CI Variables."
  - "4. **Lớp 4 (Container Image):** Build image Multi-stage Distroless và quét lỗ hổng OS bằng Trivy."
  - "5. **Lớp 5 (Supply Chain):** Tự động xuất SBOM bằng Syft và ký số điện tử Keyless bằng Cosign OIDC."
  - "6. **Lớp 6 (Governance Gate & Admission Controller):** Ở CI, script Quality Gate parser kiểm định luật OPA Rego để ngắt pipeline nếu có lỗi Critical. Ở Kubernetes Cluster, Kyverno Admission Controller verify chữ ký Cosign trước khi cho phép Pod khởi chạy."

---

### Kịch bản 2: Xử lý Tranh chấp giữa Security Team và Ban Giám đốc Kinh doanh (Business vs Security)
- **Người phỏng vấn (Chief Revenue Officer - CRO):** *"Hôm nay là ngày Black Friday, chiến dịch Marketing đang chạy mà Quality Gate của em ngắt pipeline bản Hotfix vì một cái lỗi CVE Medium vớ vẩn nào đó làm công ty thiệt hại hàng tỷ đồng mỗi giờ. Em giải quyết thế nào?"*
- **Ứng viên (DevSecOps Specialist):**
  - *Trả lời:*
    1. **Bình tĩnh & Đồng hành với Business:** "Em rất chia sẻ với áp lực doanh thu ngày Black Friday của công ty. Quyền lợi kinh doanh của công ty là ưu tiên số 1."
    2. **Xử lý sự cố ngay lập tức ($< 5$ phút):** "Trước hết, đối với lỗ hổng level **Medium**, theo quy định chính sách chuẩn của hệ thống Security Quality Gate, nó chỉ nằm ở dạng **Soft-Warning** chứ không được phép ngắt pipeline hard-fail. Em sẽ kiểm tra lại ngay xem có job nào đang bị cấu hình nhầm threshold hay không để nhả pipeline cho bản Hotfix deploy ngay trong 5 phút tới."
    3. **Phương án khẩn cấp nếu là CVE Critical:** "Trong trường hợp nếu đó là CVE Critical RCE cực kỳ nguy hiểm, em sẽ cùng SecLead kích hoạt cờ **Emergency Security Bypass** (có ghi log audit và bắn cảnh báo SIEM) để giải phóng Hotfix phục vụ Black Friday, đồng thời cài đặt WAF rule tạm thời bọc lót ở phía ngoài để bảo vệ hệ thống."

---

### Kịch bản 3: Thuyết phục Dev Team tuân thủ Quy trình Expiration Allowlist Waiver
- **Người phỏng vấn (Lead Software Engineer):** *"Bên anh bị deadline dí ngập đầu, sao mỗi lần muốn ignore một cái CVE lại bắt anh phải viết comment đủ 4 trường metadata (CVE ID, Expiration Date, Approver, JIRA Ticket) phiền phức thế? Thêm file `.trivyignore` chứa CVE ID là đủ rồi chứ!"*
- **Ứng viên (DevSecOps Specialist):**
  - *Trả lời:*
    1. **Thấu hiểu nỗi đau của Dev:** "Em rất hiểu việc phải nhập nhiều thông tin làm anh thấy tốn thời gian khi đang vội code."
    2. **Giải thích lý do an ninh cốt lõi:** "Tuy nhiên, nếu chúng ta chỉ ném CVE ID vào tệp ignore mà không có ngày hết hạn và ticket JIRA, tệp đó sẽ biến thành **nghĩa địa giấu rác an ninh**. 6 tháng sau không ai biết vì sao lại ignore CVE đó, người phê duyệt là ai, và rủi ro đó đã được vá chưa."
    3. **Giải pháp tự động hóa hỗ trợ Dev:** "Để giúp team anh không phải gõ tay thủ công, em đã viết sẵn một **GitLab Issue Template / CLI Helper command**. Anh chỉ cần gõ `make ignore CVE-2024-XXXX JIRA-123` là script tự động sinh ra đoạn metadata chuẩn kèm ngày hết hạn mặc định 14 ngày. Anh không cần phải nhớ cú pháp phức tạp nữa!"

---

### Kịch bản 4: Xử lý Tình huống Lỗ hổng 0-Day Bùng nổ toàn cầu (Vụ việc Log4j/XZ Utils)
- **Người phỏng vấn (CISO):** *"Tin tức vừa loan báo một lỗ hổng 0-Day RCE cực kỳ nghiêm trọng trong thư viện mã nguồn mở XZ Utils. Làm thế nào để trong vòng 10 phút em biết được toàn bộ 200 microservices của công ty chúng ta có bị ảnh hưởng hay không?"*
- **Ứng viên (DevSecOps Specialist):**
  - *Trả lời:*
    1. **Sức mạnh của SBOM tập trung:** "Thưa CISO, nhờ hệ thống DevSecOps Lớp 5 mà chúng ta đã triển khai, tất cả các pipeline build đều tự động xuất tệp **SBOM (Software Bill of Materials)** chuẩn SPDX/CycloneDX và đẩy về cơ sở dữ liệu lưu trữ tập trung."
    2. **Truy vấn tức thời ($< 1$ phút):** "Em không cần phải mở 200 repo ra scan lại từ đầu. Em chỉ cần chạy một câu lệnh SQL / Dependency Track Query tìm kiếm package `xz-utils` với version bị ảnh hưởng trên toàn bộ kho lưu trữ SBOM."
    3. **Khoanh vùng và Phản ứng:** "Trong vòng 2 phút, em sẽ xuất ra danh sách chính xác 3 microservices đang sử dụng package này, tự động kích hoạt pipeline trigger bài quét an ninh và mở Ticket JIRA ưu tiên Highest cho các team liên quan khắc phục ngay lập tức."

---

### Kịch bản 5: Đề xuất Chiến lược Dọn dẹp Nợ an ninh (Security Debt Paydown Strategy)
- **Người phỏng vấn (Engineering Director):** *"Dự án legacy của công ty hiện đang tồn đọng 500 lỗ hổng chưa vá. Nếu bật Hard-Fail Security Quality Gate thì dự án sẽ dừng hoạt động hoàn toàn. Em lên kế hoạch giải quyết nợ an ninh này như thế nào?"*
- **Ứng viên (DevSecOps Specialist):**
  - *Trả lời:*
    1. **Nguyên tắc "Freeze the Debt" (Đóng băng nợ cũ):**
       - Tạo một tệp **Baseline Snapshot** chứa toàn bộ 500 lỗ hổng hiện có.
       - Cấu hình Quality Gate theo quy tắc **"Zero New Vulnerabilities"**: Pipeline chỉ ngắt nếu xuất hiện **CVE MỚI** phát sinh từ commit hôm nay trở đi. Nhờ đó, Dev vẫn ra feature mới bình thường mà nợ không bị phình to.
    2. **Lập lộ trình dọn dẹp theo Sprint (Sprint Paydown Roadmap):**
       - Phân loại 500 lỗi theo Severity. Tập trung xử lý 15 lỗi Critical trước.
       - Thỏa thuận với Product Owner dành 10% capacity của mỗi Sprint (khoảng 2 ngày) để vá 10-15 CVE cũ trong baseline.
    3. **Cập nhật Baseline:** Sau mỗi Sprint, chạy script tự động cập nhật lại tệp Baseline mới với số lượng CVE giảm dần cho đến khi nợ an ninh về 0.

---

### Kịch bản 6: Giải trình khi Hệ thống bị Hacker tấn công vượt qua Security Gate
- **Người phỏng vấn (CEO):** *"Tại sao chúng ta đã đầu tư bài bản hệ thống Security Quality Gate 6 lớp mà tuần trước vẫn bị kẻ gian tấn công rò rỉ dữ liệu qua một lỗ hổng trên Web?"*
- **Ứng viên (DevSecOps Specialist):**
  - *Trả lời:*
    1. **Thái độ chuyên nghiệp:** "Báo cáo CEO, em xin nhận trách nhiệm về sự cố an ninh vừa qua và đã phối hợp cùng Incident Response Team khắc phục triệt để lỗ hổng trong 2 giờ."
    2. **Phân tích nguyên nhân kỹ thuật (Post-Mortem):** "Qua phân tích forensic, kẻ tấn công đã sử dụng kỹ thuật **Business Logic Flaw (Lỗi logic nghiệp vụ)** — đây là loại lỗi không tạo ra chữ ký mã độc nên các công cụ SAST/Container Scan tự động ở CI/CD không thể tự phát hiện được."
    3. **Hành động cải tiến bài học kinh nghiệm:**
       - Tích hợp thêm bước **Manual Security Code Review** đối với các Merge Request đụng chạm đến luồng thanh toán và xác thực người dùng (sử dụng CODEOWNERS rule).
       - Bổ sung công cụ DAST và Fuzz Testing vào pipeline nightly để tự động giả lập các kịch bản tấn công nghiệp vụ thực nghiệm.

---

### Kịch bản 7: Bảo vệ Quan điểm Kiến trúc về Keyless Cosign Signing
- **Người phỏng vấn (Lead Security Architect):** *"Tại sao em lại dùng Cosign Keyless dựa trên OIDC mà không dùng cặp khóa RSA/ECDSA truyền thống để ký số container image? Dùng khóa tĩnh lưu trên Vault không phải dễ kiểm soát hơn sao?"*
- **Ứng viên (DevSecOps Specialist):**
  - *Trả lời:*
    1. **Bản chất của Quản lý Khóa tĩnh (Key Management Headache):** "Nếu dùng cặp khóa RSA tĩnh, chúng ta phải tốn công bảo vệ Private Key, lo lắng nguy cơ khóa bị rò rỉ, và phải lập quy trình xoay vòng khóa (Key Rotation) cực kỳ phức tạp cho hàng trăm runner."
    2. **Ưu điểm vượt trội của Cosign Keyless (Fulcio + Rekor):**
       - **Short-lived Certificate:** Cosign Keyless tận dụng OIDC Token sẵn có của GitLab Runner để xin một chứng chỉ số ngắn hạn (chỉ có hiệu lực trong 10 phút) từ Fulcio Certificate Authority.
       - **Zero Key Storage:** Không có bất kỳ Private Key vĩnh viễn nào cần phải lưu trữ hay quản lý trên Vault hay CI Variables.
       - **Immutable Audit Trail:** Mọi chữ ký đều được ghi vết công khai trên nhật ký Rekor Transparency Log, giúp chứng minh không ai có thể làm giả chữ ký trong quá khứ.

---

## §V3. Câu chốt để nói khi phỏng vấn

1. *"Bài kiểm tra giữa kỳ 2 khẳng định một nguyên lý: **An ninh CI/CD không phải là một công cụ đơn lẻ, mà là một hệ thống phòng thủ 6 lớp tự động khép kín** từ dòng code đầu tiên cho đến khi Pod chạy trên Kubernetes."*
2. *"Em xây dựng Security Quality Gate dựa trên triết lý **Shift-Left nhưng không Block-Dev** — hỗ trợ dev ở nhánh feature và bảo vệ tuyệt đối tính bất biến trên nhánh production."*
3. *"Một tệp ignore không có ngày hết hạn ISO 8601 và ticket JIRA đính kèm chỉ là một **hành vi che giấu nợ an ninh** làm hỏng hệ thống governance."*
4. *"Nền tảng của DevSecOps hiện đại là **Zero Static Secret** — mọi truy cập credential phải thông qua Vault OIDC JWT ngắn hạn và mọi Container Image phải được ký số Keyless bằng Cosign."*
5. *"Thước đo thành công của bộ phận DevSecOps không nằm ở số lượng công cụ quét được cài đặt, mà nằm ở chỉ số **Escaped Vulnerabilities về 0** và **MTTR khắc phục lỗi dưới 24 giờ**."*

---

## BTVN 4: Chuẩn bị mở đầu Giai đoạn 6 — Buổi 36 (Environment, Deployment & Protected Environments)

Để chuẩn bị tốt nhất cho **Buổi 36: Environment, Deployment & Protected Environments**, học viên cần thực hiện các nhiệm vụ sau:

1. **Nghiên cứu khái niệm Environment trong GitLab CI/CD:**
   - Đọc trước tài liệu GitLab CI về từ khóa `environment:name`, `environment:url`, `environment:action`.
   - Tìm hiểu ý nghĩa của thuộc tính `on_stop` và các job dọn dẹp môi trường tạm thời (Dynamic/Ephemeral Environments / Review Apps).

2. **Tìm hiểu về Protected Environments & Manual Approvals:**
   - Phân biệt giữa Protected Branch và Protected Environment.
   - Tìm hiểu cách thiết lập quy trình phê duyệt thủ công (Approval Rules) trước khi trigger job deploy lên Production.

3. **Bài tập chuẩn bị thực hành:**
   - Tạo thử nghiệm một tệp `.gitlab-ci.yml` cấu hình 3 môi trường: `development`, `staging`, `production`.
   - Cấu hình cho môi trường `production` yêu cầu quyền `Maintainer` mới được bấm nút `manual` execute job deploy!
{% endraw %}
