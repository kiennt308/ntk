---
layout: post
title: "CKA (Bài 11/35) - ServiceAccount & Token Bảo Mật: Projected Volume, TokenRequest API & Chống Thất Thoát Token"
date: 2026-09-12
categories: [Kubernetes, CKA, Security, Workload]
tags: [cka, serviceaccount, token, tokenrequest, projected-volume, oidc, security]
series: "CKA Exam & Cluster Admin Mastery"
series_order: 11
author: "Nguyen Thao Kien"
description: "Làm chủ cơ chế xác thực danh tính Workload với ServiceAccount trong Kubernetes. Phân tích kiến trúc Bound ServiceAccount Token, cơ chế Projected Volume, TokenRequest API, OIDC Federation và kỹ thuật vô hiệu hóa automount bảo mật."
summary: "Hướng dẫn toàn diện về Kubernetes ServiceAccount và Token bảo mật cho CKA và production: kiến trúc Bound Token Projection, TokenRequest API, JWT claims, OIDC Workload Identity và kỹ thuật phòng thủ token."
keywords:
  - kubernetes serviceaccount
  - cka serviceaccount token
  - projected volume kubernetes
  - tokenrequest api
  - automountserviceaccounttoken false
  - bound serviceaccount token
  - kubernetes workload identity
image:
  path: /assets/img/posts/cka/cka-11-serviceaccount-banner.png
  alt: "Mô hình xác thực ServiceAccount và Token Projection trong Kubernetes"
difficulty: ADVANCED
tldr:
  - "ServiceAccount là thực thể API định danh máy (Workload/Pod) giao tiếp an toàn với `kube-apiserver`, tách biệt hoàn toàn với User tài khoản con người."
  - "Từ Kubernetes v1.21+ (mặc định GA v1.22+), hệ thống áp dụng Bound ServiceAccount Token Projection: Token là JWT có thời hạn ngắn, gắn chặt với vòng đời Pod và tự động xoay vòng (Auto-rotation)."
  - "Legacy Token (Secret v1 loại `kubernetes.io/service-account-token`) không có thời hạn hết hạn, tạo ra nguy cơ rò rỉ token vĩnh viễn và bị loại bỏ mặc định khỏi Pod."
  - "Nguyên tắc bảo mật số một: Luôn đặt `automountServiceAccountToken: false` trên ServiceAccount hoặc Pod Spec cho các workload không cần tương tác với Kubernetes API."
  - "Làm chủ lệnh `kubectl create token <sa-name>` để tạo token tùy chỉnh thời hạn và Audience (`--audience`, `--duration`)."
---

{% raw %}
> [!IMPORTANT]
> **Mục tiêu kỹ thuật & Trọng tâm CKA**:
> - Hiểu rõ cơ chế khởi tạo và gắn kết ServiceAccount vào Pod Spec.
> - Nắm vững kiến trúc **Bound ServiceAccount Token Volume Projection** và API `TokenRequest`.
> - Phân tích cấu trúc JWT Claims (`iss`, `sub`, `aud`, `exp`, `kubernetes.io`) và quy trình xác thực bằng khóa công khai `sa.pub`.
> - Thực thi nguyên tắc Least Privilege thông qua `automountServiceAccountToken: false`.
> - Thành thạo kỹ năng debug token bị từ chối và cấu hình phân quyền RBAC tương ứng cho Pod.

---

## 1. Bản Chất Kiến Trúc & Tư Duy Cốt Lõi: Danh Tính Workload & Token Projection

Trong hệ sinh thái Kubernetes, nếu như **User / Group** là các khái niệm danh tính dành cho con người (được quản lý bên ngoài qua OIDC, LDAP, X.509 Client Certificates), thì **ServiceAccount (SA)** là danh tính chính thức dành riêng cho các tiến trình chạy bên trong **Pod**.

Mỗi khi một Pod muốn gửi request tới `kube-apiserver` (ví dụ: Ingress Controller theo dõi Services, Prometheus cào metrics, hoặc CI/CD runner triển khai ứng dụng), nó phải tự xác thực thông qua một **Bearer Token** do ServiceAccount cấp phát.

### 1.1. Sự Tiến Hóa: Từ Legacy Static Secret Sang Bound Token Projection

| Đặc Điểm | Legacy Token (Kubernetes ≤ v1.20) | Bound ServiceAccount Token (v1.21+ GA) |
| :--- | :--- | :--- |
| **Cơ chế lưu trữ** | Lưu dưới dạng đối tượng `Secret` v1 trong etcd | Tạo động trong bộ nhớ bởi Kubelet qua `TokenRequest` API |
| **Thời hạn hết hạn (TTL)**| Vĩnh viễn (Không bao giờ hết hạn trừ khi xóa Secret)| Có thời hạn (Mặc định 1 giờ, tự động renew khi đạt 80% TTL)|
| **Gắn kết vòng đời** | Độc lập với Pod (Lộ token vẫn dùng được từ bất kỳ đâu)| Gắn chặt với UID của Pod (Xóa Pod là Token lập tức bị vô hiệu)|
| **Audience (`aud`)** | Mặc định không giới hạn | Giới hạn đối tượng nhận token cụ thể (tránh dội ngược)|
| **Phương thức Mount** | Kubelet mount Volume từ đối tượng Secret | Sử dụng `projected` volume nạp thẳng từ RAM vào Pod |

### 1.2. Sơ đồ Chu Trình Cấp Phát & Xác Thực Bound ServiceAccount Token

```mermaid
sequenceDiagram
    autonumber
    participant Kubelet as Node Kubelet
    participant API as kube-apiserver
    participant Pod as Container / App
    participant TokenAPI as TokenRequest Subresource

    Kubelet->>API: 1. Watch & Nhận định nghĩa Pod (kèm SA: my-sa)
    Kubelet->>TokenAPI: 2. Gọi POST /api/v1/namespaces/ns/serviceaccounts/my-sa/token (gắn Pod UID)
    TokenAPI->>TokenAPI: 3. Ký JWT bằng sa.key (Private Key của Cluster)
    TokenAPI-->>Kubelet: 4. Trả về JWT Token có thời hạn (TTL = 1h)
    Kubelet->>Pod: 5. Mount Token vào /var/run/secrets/kubernetes.io/serviceaccount/token
    Pod->>API: 6. Gửi request kèm Header "Authorization: Bearer <JWT>"
    API->>API: 7. Xác thực chữ ký bằng sa.pub & Kiểm tra Pod UID còn sống
    API-->>Pod: 8. HTTP 200 OK (Thành công)
```

Khi Container khởi động, ba tệp tin bảo mật được nạp tự động vào thư mục `/var/run/secrets/kubernetes.io/serviceaccount/`:
1. `token`: Chuỗi JWT Token dùng để xác thực Bearer Header.
2. `ca.crt`: Chứng chỉ CA công khai của cụm để ứng dụng xác thực HTTPS endpoint của `kube-apiserver`.
3. `namespace`: Tên của Namespace mà Pod đang cư ngụ.

---

## 2. Bảng Ma Trận So Sánh Kỹ Thuật Toàn Diện (Engineering Matrix)

Bảng đối chiếu các phương thức cấu hình danh tính và quyền hạn của ServiceAccount:

| Tiêu Chí So Sánh | Default ServiceAccount | Dedicated ServiceAccount | Projected Bound Token | Manual Short-Lived Token |
| :--- | :--- | :--- | :--- | :--- |
| **Tạo mặc định** | Tự sinh khi tạo Namespace | Quản trị viên/Dev tạo chủ động | Tự sinh khi Pod khởi chạy | Quản trị viên chạy lệnh `kubectl create token` |
| **Quyền hạn mặc định** | Không có quyền (0% RBAC) | Không có quyền (Gán qua RoleBinding)| Theo quyền của SA | Theo quyền của SA |
| **Cơ chế nạp** | Tự động Mount nếu không tắt | Khai báo `serviceAccountName` | Nạp vào Projected Volume | Truyền qua CLI, CI/CD, hoặc Script |
| **Thời hạn sử dụng** | 1 giờ (Auto-rotated) | 1 giờ (Auto-rotated) | 1 giờ (Auto-rotated) | Tùy chỉnh qua `--duration` (10m - 24h) |
| **Mức độ an toàn** | Kém (Dễ bị lạm dụng nếu cấp RBAC)| Rất cao (Đúng nguyên tắc Least Privilege)| Cực cao (Gắn với Pod UID)| Cao (Dành cho kiểm thử/Task tạm) |
| **Ứng dụng chính** | Workload không cần gọi API | Backend API, Controller, Ingress | Production Workloads | CI/CD Runner, External Scripts |

---

## 3. Cấu Trúc Khai Báo Manifest & Chi Tiết Bound Volume

### 3.1. Pod Spec Khai Báo ServiceAccount & Vô Hiệu Hóa Automount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: backend-processor-sa
  namespace: production
automountServiceAccountToken: false # Vô hiệu hóa ở cấp độ ServiceAccount
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-processor
  namespace: production
spec:
  replicas: 2
  selector:
    matchLabels:
      app: order-processor
  template:
    metadata:
      labels:
        app: order-processor
    spec:
      serviceAccountName: backend-processor-sa
      automountServiceAccountToken: false # Vô hiệu hóa ở cấp độ Pod Spec (Override)
      containers:
        - name: app
          image: registry.k8s.io/pause:3.9
          resources:
            limits:
              cpu: "200m"
              memory: "256Mi"
            requests:
              cpu: "100m"
              memory: "128Mi"
```

### 3.2. Cấu Trúc Projected Volume Thực Tế Do Kubelet Tự Động Tạo

Khi `automountServiceAccountToken: true`, Kubelet sẽ tự động inject khối cấu hình Volume Projection sau vào Pod Spec:

```yaml
volumes:
  - name: kube-api-access-x8k2p
    projected:
      defaultMode: 420 # Quyền file 0644
      sources:
        - serviceAccountToken:
            expirationSeconds: 3607
            path: token
        - configMap:
            name: kube-root-ca.crt
            items:
              - key: ca.crt
                path: ca.crt
        - downwardAPI:
            items:
              - fieldRef:
                  apiVersion: v1
                  fieldPath: metadata.namespace
                path: namespace
```

---

## 4. Phân Tích Cạm Bẫy Thực Chiến: Lỗ Hổng Bảo Mật & Rò Rỉ Token

### Tình huống 1: Cấp quyền RBAC trực tiếp cho `default` ServiceAccount

Một kỹ sư muốn kiểm thử nhanh ứng dụng nên đã bind quyền `cluster-admin` cho ServiceAccount `default` trong namespace `default`. Hậu quả: Bất kỳ Pod nào khởi tạo trong namespace `default` không khai báo `serviceAccountName` đều tự động kế thừa quyền quản trị toàn cụm!

### Hậu Quả & Log Lỗi Thực Tế:

```text
# Kẻ tấn công khai thác Pod bị chiếm quyền (RCE) để chiếm toàn bộ cụm:
$ kubectl auth can-i create clusterrolebindings --as=system:serviceaccount:default:default
yes
$ kubectl auth can-i delete namespaces --as=system:serviceaccount:default:default
yes
```

### 5-Whys Root Cause Analysis:
1. **Tại sao Pod của kẻ tấn công có quyền xóa cụm?** -> Pod sử dụng `default` ServiceAccount có gán `cluster-admin`.
2. **Tại sao `default` SA có quyền này?** -> Quản trị viên đã tạo `ClusterRoleBinding` trỏ vào `default:default`.
3. **Tại sao lại gán vào `default` SA thay vì SA riêng?** -> Kỹ sư muốn cấu hình nhanh cho Pod dev mà không tạo ServiceAccount mới.
4. **Tại sao Pod tự động nhận `default` SA?** -> Mọi Pod không khai báo trường `serviceAccountName` đều mặc định nhận `default`.
5. **Giải pháp triệt để là gì?** -> Không bao giờ gán quyền RBAC cho `default` SA; luôn tạo Dedicated SA và đặt `automountServiceAccountToken: false` cho `default` SA.

```diff
- apiVersion: rbac.authorization.k8s.io/v1
- kind: ClusterRoleBinding
- metadata:
-   name: bad-admin-binding
- subjects:
-   - kind: ServiceAccount
-     name: default
-     namespace: default
- roleRef:
-   kind: ClusterRole
-   name: cluster-admin
-   apiGroup: rbac.authorization.k8s.io
```

---

### Tình huống 2: Pod không cần gọi API Server nhưng vẫn mount Token

Một website tĩnh frontend bị lỗ hổng Local File Inclusion (LFI). Kẻ tấn công đọc nội dung tệp tin `/var/run/secrets/kubernetes.io/serviceaccount/token` và sử dụng token đó để quét toàn bộ hệ thống API nội bộ.

### Hậu Quả & Log Lỗi Thực Tế:

```text
# Log truy cập API trái phép từ bên ngoài sử dụng token bị đánh cắp:
GET /api/v1/namespaces/default/secrets HTTP/2.0
Host: 192.168.10.10:6443
User-Agent: curl/7.88.1
Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ik16...
HTTP/2 403 Forbidden
```

> [!WARNING]
> Mặc dù RBAC mặc định từ chối (403), nhưng việc để lộ Token tạo điều kiện cho kẻ tấn công xác thực danh tính hợp lệ và thăm dò (reconnaissance) toàn bộ API endpoints của cụm. Luôn vô hiệu hóa automount cho 100% workload không trực tiếp quản trị cụm.

---

### Tình huống 3: Lỗi giải mã JWT do sai lệch thời gian hệ thống (Clock Skew)

Token được tạo từ API Server nhưng Kubelet hoặc Container từ chối xác thực vì lỗi `token is not valid yet` hoặc `token has expired`.

### Hậu Quả & Log Lỗi Thực Tế:

```text
E0916 00:15:32.102934 1 round_trippers.go:553] GET https://10.96.0.1:443/api/v1/pods 401 Unauthorized
{
  "kind": "Status",
  "apiVersion": "v1",
  "status": "Failure",
  "message": "Unauthorized: token is expired",
  "code": 401
}
```

Nguyên nhân do dịch vụ đồng bộ thời gian `chrony` hoặc `systemd-timesyncd` trên Worker Node bị dừng, dẫn đến chênh lệch thời gian vượt quá thời hạn sống của Bound Token.

---

## 5. Hands-on Lab: Quản Trị & Kiểm Định ServiceAccount (8 Bước)

Bảng tổng hợp 8 bước thực hành:

| Bước | Thao Tác | Mục Tiêu Kỹ Thuật | Lệnh / Công Cụ |
| :--- | :--- | :--- | :--- |
| **1** | Tạo Namespace & ServiceAccount | Thiết lập không gian tên và danh tính mới | `kubectl create ns`, `kubectl create sa` |
| **2** | Khóa Automount trên SA | Thiết lập an toàn ở cấp độ tài khoản | `kubectl patch sa` |
| **3** | Khởi chạy Pod với SA | Triển khai workload sử dụng danh tính riêng | `kubectl apply -f pod.yaml` |
| **4** | Kiểm tra thư mục Mount trong Pod | Xác nhận token không bị mount thừa | `kubectl exec -- ls /var/run/secrets` |
| **5** | Tạo Token thủ công ngắn hạn | Khởi tạo JWT có thời hạn và Audience cụ thể | `kubectl create token` |
| **6** | Giải mã & Phân tích JWT Payload | Đọc các trường claim tiêu chuẩn | `jq`, `base64` |
| **7** | Gán quyền RBAC cho SA | Cấp quyền đọc Pods trong Namespace | `kubectl create role`, `rolebinding` |
| **8** | Gọi API Server trực tiếp với Token | Xác thực truy vấn thành công với `curl` | `curl -k -H "Authorization: Bearer..."` |

---

### Bước 1: Khởi tạo Namespace và ServiceAccount

Tạo không gian tên và ServiceAccount riêng biệt:

```bash
kubectl create namespace sa-lab
kubectl create serviceaccount app-runner -n sa-lab
```

---

### Bước 2: Thiết lập `automountServiceAccountToken: false`

Khóa tự động mount token cho ServiceAccount vừa tạo:

```bash
kubectl patch serviceaccount app-runner -n sa-lab -p '{"automountServiceAccountToken": false}'
```

Kiểm tra lại cấu hình:

```bash
kubectl get sa app-runner -n sa-lab -o yaml
```

---

### Bước 3: Triển khai Pod gắn kết ServiceAccount

Tạo một Pod chạy ảnh Alpine/Curl sử dụng `app-runner`:

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  namespace: sa-lab
spec:
  serviceAccountName: app-runner
  containers:
    - name: runner
      image: curlimages/curl:8.4.0
      command: ["sleep", "3600"]
EOF
```

---

### Bước 4: Xác nhận Token không bị rò rỉ vào Pod

Thực thi lệnh kiểm tra thư mục secret bên trong Container:

```bash
kubectl exec -it secure-app -n sa-lab -- ls -la /var/run/secrets/kubernetes.io/serviceaccount/ || echo "Thư mục không tồn tại - An toàn tuyệt đối!"
```

---

### Bước 5: Tạo Token ngắn hạn theo yêu cầu (On-Demand Token)

Sinh một token có thời hạn 30 phút dành riêng cho dịch vụ kiểm thử:

```bash
TOKEN=$(kubectl create token app-runner -n sa-lab --duration=30m --audience="https://kubernetes.default.svc")
echo "Token sinh ra: ${TOKEN:0:40}..."
```

---

### Bước 6: Giải mã và phân tích Payload của JWT

Giải mã phần Payload của token để kiểm tra các Claims:

```bash
echo $TOKEN | cut -d. -f2 | base64 -d 2>/dev/null | jq .
```

Kết quả trả về định dạng JSON:

```json
{
  "aud": [
    "https://kubernetes.default.svc"
  ],
  "exp": 1726475400,
  "iat": 1726473600,
  "iss": "https://kubernetes.default.svc.cluster.local",
  "kubernetes.io": {
    "namespace": "sa-lab",
    "serviceaccount": {
      "name": "app-runner",
      "uid": "a2c13d80-5fb2-4f36-9b5a-9b7e71f98124"
    }
  },
  "nbf": 1726473600,
  "sub": "system:serviceaccount:sa-lab:app-runner"
}
```

---

### Bước 7: Cấp quyền đọc Pods cho ServiceAccount

Tạo Role và RoleBinding để ServiceAccount có quyền đọc tài nguyên trong namespace:

```bash
kubectl create role pod-viewer -n sa-lab --verb=get,list --resource=pods
kubectl create rolebinding bind-pod-viewer -n sa-lab --role=pod-viewer --serviceaccount=sa-lab:app-runner
```

---

### Bước 8: Kiểm thử truy vấn `kube-apiserver` với Token

Sử dụng curl gửi Bearer Token trực tiếp tới API Server:

```bash
APISERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')

curl -k -H "Authorization: Bearer $TOKEN" \
  "$APISERVER/api/v1/namespaces/sa-lab/pods" | jq '.items[].metadata.name'
```

Output phản hồi thành công:
```text
"secure-app"
```

---

## 6. 10 Câu Hỏi Tự Kiểm Tra Chuyên Sâu (Self-Check Q&A Accordion)

<details class="qa-card">
  <summary><b>Câu 1: Điểm khác biệt căn bản giữa ServiceAccount và User Account trong Kubernetes là gì?</b></summary>
  <div class="qa-answer">
    <b>Trả lời:</b><br>
    <ul>
      <li><b>ServiceAccount:</b> Là API Object được quản lý trực tiếp bởi Kubernetes, thuộc về một Namespace cụ thể, dành cho các tiến trình chạy trong Pod để tương tác với API Server.</li>
      <li><b>User Account:</b> Đại diện cho con người (quản trị viên, lập trình viên), không phải API Object trong etcd, được xác thực thông qua hệ thống chứng thực bên ngoài (X.509 Certificates, OIDC, Webhook).</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary><b>Câu 2: Cơ chế Bound ServiceAccount Token Volume Projection là gì và mang lại lợi ích bảo mật nào?</b></summary>
  <div class="qa-answer">
    <b>Trả lời:</b><br>
    Bound ServiceAccount Token là cơ chế tạo token JWT động thông qua <code>TokenRequest</code> API của Kubelet. Token này có thời hạn ngắn (mặc định 1 giờ), tự động xoay vòng và <i>gắn chặt với vòng đời của Pod (Pod UID)</i>. Khi Pod bị xóa, Token ngay lập tức mất hiệu lực, triệt tiêu nguy cơ token bị đánh cắp và sử dụng vĩnh viễn từ bên ngoài.
  </div>
</details>

<details class="qa-card">
  <summary><b>Câu 3: Làm thế nào để vô hiệu hóa việc tự động mount token vào Pod cho một ứng dụng không cần gọi API Server?</b></summary>
  <div class="qa-answer">
    <b>Trả lời:</b><br>
    Bạn có thể thiết lập <code>automountServiceAccountToken: false</code> tại một trong hai nơi:<br>
    1. Trong định nghĩa <code>ServiceAccount</code> (áp dụng cho mọi Pod dùng SA này trừ khi Pod ghi đè).<br>
    2. Trong định nghĩa <code>Pod.spec</code> (áp dụng riêng cho Pod đó).
  </div>
</details>

<details class="qa-card">
  <summary><b>Câu 4: Ba tệp tin nào được Kubelet mount mặc định vào thư mục /var/run/secrets/kubernetes.io/serviceaccount/?</b></summary>
  <div class="qa-answer">
    <b>Trả lời:</b><br>
    1. <code>token</code>: Chứa chuỗi JWT Bearer token để xác thực với API Server.<br>
    2. <code>ca.crt</code>: Chứng chỉ Certificate Authority của cụm để Pod xác minh danh tính API Server.<br>
    3. <code>namespace</code>: Tệp văn bản chứa tên của Namespace hiện tại của Pod.
  </div>
</details>

<details class="qa-card">
  <summary><b>Câu 5: Cú pháp chuẩn của subject username mà API Server gán cho một ServiceAccount là gì?</b></summary>
  <div class="qa-answer">
    <b>Trả lời:</b><br>
    Cú pháp chuẩn có dạng: <code>system:serviceaccount:&lt;namespace&gt;:&lt;serviceaccount-name&gt;</code>.<br>
    Ví dụ: ServiceAccount <code>app-runner</code> trong namespace <code>sa-lab</code> sẽ có username là <code>system:serviceaccount:sa-lab:app-runner</code>.
  </div>
</details>

<details class="qa-card">
  <summary><b>Câu 6: Lệnh kubectl nào cho phép tạo thủ công một Token ngắn hạn cho ServiceAccount mà không cần tạo Secret?</b></summary>
  <div class="qa-answer">
    <b>Trả lời:</b><br>
    Sử dụng lệnh:<br>
    <code>kubectl create token &lt;sa-name&gt; --namespace=&lt;ns&gt; [--duration=1h] [--audience=&lt;aud&gt;]</code>
  </div>
</details>

<details class="qa-card">
  <summary><b>Câu 7: Khóa mật mã nào được kube-apiserver sử dụng để ký và xác thực JWT token của ServiceAccount?</b></summary>
  <div class="qa-answer">
    <b>Trả lời:</b><br>
    <ul>
      <li><b>Ký token:</b> Sử dụng Private Key được chỉ định qua cờ <code>--service-account-private-key-file</code> (thường là <code>/etc/kubernetes/pki/sa.key</code>).</li>
      <li><b>Xác thực token:</b> Sử dụng Public Key được chỉ định qua cờ <code>--service-account-key-file</code> (thường là <code>/etc/kubernetes/pki/sa.pub</code>).</li>
    </ul>
  </div>
</details>

<details class="qa-card">
  <summary><b>Câu 8: Khái niệm OIDC Discovery (Service Account Issuer Discovery) dùng để làm gì trong quản trị Workload Identity?</b></summary>
  <div class="qa-answer">
    <b>Trả lời:</b><br>
    OIDC Discovery cho phép các nhà cung cấp Cloud (như AWS IAM Roles for Service Accounts - IRSA, GCP Workload Identity, Azure Workload Identity) xác thực token do Kubernetes ký thông qua endpoint công khai <code>/.well-known/openid-configuration</code> và <code>openid/v1/jwks</code>. Nhờ đó, Pod có thể trực tiếp nhận quyền truy cập tài nguyên Cloud (S3, RDS, Cloud Storage) mà không cần nhúng Secret/Key tĩnh vào Pod.
  </div>
</details>

<details class="qa-card">
  <summary><b>Câu 9: Nếu cả ServiceAccount có automountServiceAccountToken: true nhưng Pod Spec có automountServiceAccountToken: false thì kết quả như thế nào?</b></summary>
  <div class="qa-answer">
    <b>Trả lời:</b><br>
    Cấu hình tại <b>Pod Spec có độ ưu tiên cao hơn (Override)</b>. Do đó, token sẽ <b>KHÔNG</b> được mount vào Container của Pod.
  </div>
</details>

<details class="qa-card">
  <summary><b>Câu 10: Tại sao từ Kubernetes v1.24+, Secret token không còn được tự động tạo khi tạo một ServiceAccount mới?</b></summary>
  <div class="qa-answer">
    <b>Trả lời:</b><br>
    Để tăng cường bảo mật và loại bỏ hoàn toàn các Static Token không có thời hạn (Legacy Secret-based tokens). Kubernetes chuyển dịch hoàn toàn sang cơ chế Bound Token thông qua <code>TokenRequest</code> API. Nếu người dùng thực sự cần static token cho các hệ thống cũ, họ phải tự tạo đối tượng Secret với annotation <code>kubernetes.io/service-account.name</code>.
  </div>
</details>

---

## 7. Tổng Kết & Lộ Trình Bài Học Tiếp Theo

```mermaid
mindmap
  root((ServiceAccount & Token))
    Danh Tinh
      API Object Namespaced
      Dành cho Máy / Pod
      system:serviceaccount:ns:name
    Bound Token Projection
      TokenRequest API
      Auto-rotation (1h TTL)
      Gắn chặt Pod UID
      Mounted tại /var/run/secrets/
    Bảo Mật
      automountServiceAccountToken: false
      Least Privilege RBAC
      Không cấp quyền default SA
      OIDC Workload Identity
```

Nắm vững cơ chế vận hành của ServiceAccount và cấu trúc Bound Token Projection giúp bạn bảo vệ toàn diện các workload trên cụm khỏi rủi ro rò rỉ đặc quyền và tấn công lateral movement.

> [!TIP]
> **Bài học tiếp theo**: Trong [Bài 12: Thiết Lập Cụm HA Control Plane với Stacked & External etcd](cka-12-12-ha-control-plane.html), chúng ta sẽ khám phá kiến trúc sẵn sàng cao (High Availability) cho Kubernetes Control Plane, cấu hình Load Balancer HAProxy/Keepalived và so sánh chi tiết giữa mô hình Stacked etcd vs External etcd topology.
{% endraw %}
