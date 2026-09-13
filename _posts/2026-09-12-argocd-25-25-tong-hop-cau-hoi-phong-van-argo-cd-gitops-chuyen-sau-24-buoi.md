---
layout: post
title: "[Bài 25] Đại Tuyển Tập 100+ Câu Hỏi Phỏng Vấn Argo CD & GitOps Chuyên Sâu (24 Chuyên Đề)"
date: 2026-09-12 21:40:00 +0700
categories: [ArgoCD]
tags:
  - ArgoCD
  - GitOps
  - Kubernetes
  - CICD
  - CloudNative
  - Part-25
series: "ArgoCD & GitOps Mastery"
series_order: 25
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80"
summary: "Bộ cẩm nang 100+ câu hỏi phỏng vấn tuyển dụng kỹ thuật chuyên sâu về Argo CD & GitOps Enterprise dành cho DevOps Engineer, SRE và Platform Architect: Bao phủ 5 cấp độ từ Kiến trúc cốt lõi, Kustomize/Helm, Multi-Cluster ApplicationSet, Security/RBAC/Secrets đến Progressive Delivery và Troubleshooting sự cố Production."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Đại Tuyển Tập 100+ Câu Hỏi Phỏng Vấn Argo CD & GitOps Chuyên Sâu (24 Chuyên Đề)."
  - "Ứng dụng triết lý GitOps với Git làm nguồn chân lý duy nhất (Single Source of Truth), đồng bộ tự động 24/7."
  - "Kiểm soát chặt chẽ quy trình triển khai đa cụm Kubernetes, phát hiện và triệt tiêu Configuration Drift."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# Đại Tuyển Tập 100+ Câu Hỏi Phỏng Vấn Argo CD & GitOps Chuyên Sâu (24 Chuyên Đề)

Chào mừng bạn đến với chuyên đề tổng kết đặc biệt của toàn bộ Series **Argo CD & GitOps Enterprise Architecture**. 

Trong thị trường tuyển dụng công nghệ hiện đại, vai trò **Platform Engineer**, **DevOps Lead** và **Site Reliability Engineer (SRE)** đòi hỏi sự am hiểu sâu sắc về triết lý GitOps, khả năng thiết kế hệ thống phân phối đa cụm và năng lực xử lý sự cố thực chiến. Các câu hỏi phỏng vấn ngày nay không còn dừng lại ở mức định nghĩa lý thuyết cơ bản, mà tập trung vào các bài toán thiết kế kiến trúc quy mô lớn, tối ưu hóa hiệu năng và đối soát các cạm bẫy "Synced nhưng sai".

Bộ tài liệu này tổng hợp **100+ câu hỏi phỏng vấn kỹ thuật chuyên sâu** được đúc kết từ 24 chuyên đề, phân loại theo 5 nhóm chủ đề cốt lõi giúp bạn tự tin chinh phục mọi vòng phỏng vấn kỹ thuật cấp cao và chứng chỉ quốc tế **Certified Argo Project Associate (CAPA)**.

```mermaid
flowchart LR
    G1["Phần 1<br/>Kiến Trúc Cốt Lõi<br/>(Câu 01 - 20)"]
    G2["Phần 2<br/>Sync Waves, Helm, Kustomize<br/>(Câu 21 - 40)"]
    G3["Phần 3<br/>Multi-Cluster & AppSet<br/>(Câu 41 - 60)"]
    G4["Phần 4<br/>RBAC, SSO, Secrets & DR<br/>(Câu 61 - 80)"]
    G5["Phần 5<br/>Rollouts & Troubleshooting<br/>(Câu 81 - 100+)"]

    G1 --> G2 --> G3 --> G4 --> G5


```

> [!TIP]
> **CHIẾN THUẬT TRẢ LỜI PHỎNG VẤN ĐỈNH CAO:**
> Khi người phỏng vấn hỏi về một lỗi hoặc cơ chế trong Argo CD, đừng chỉ trả lời "đúng định nghĩa". Hãy luôn trả lời theo công thức 3 bước:
> 1. **Bản chất kỹ thuật (How it works under the hood)**.
> 2. **Cạm bẫy thực chiến hay gặp ("Synced nhưng sai")**.
> 3. **Giải pháp kiến trúc chuẩn Enterprise (Best Practice & Zero-Trust)**.

> [!IMPORTANT]
> **CHUẨN BỊ CHO CHỨNG CHỈ QUỐC TẾ CAPA:**
> Hãy đọc kỹ các câu hỏi thuộc Phần 2 (Sync Waves/Hooks) và Phần 4 (RBAC/OIDC/Secrets), đây là 2 phần chiếm tỷ trọng câu hỏi tình huống cao nhất trong kỳ thi Certified Argo Project Associate.

---

## Mục Lục 5 Khối Kiến Thức Trọng Tâm

1. [Phần 1: Nguyên Lý GitOps & Kiến Trúc Cốt Lõi Argo CD (Câu 01 – 20)](#phan-1-nguyen-ly-gitops--kien-truc-cot-loi-argo-cd)
2. [Phần 2: Điều Phối Nâng Cao, Kustomize, Helm & Config Management Plugins (Câu 21 – 40)](#phan-2-dieu-phoi-nang-cao-kustomize-helm--config-management-plugins)
3. [Phần 3: Quy Mô Đa Cụm, App-of-Apps & ApplicationSet Engine (Câu 41 – 60)](#phan-3-quy-mo-da-cum-app-of-apps--applicationset-engine)
4. [Phần 4: Bảo Mật, RBAC, SSO/OIDC, Secrets Management & Disaster Recovery (Câu 61 – 80)](#phan-4-bao-mat-rbac-ssooidc-secrets-management--disaster-recovery)
5. [Phần 5: Progressive Delivery, Observability & Khắc Phục Sự Cố Production (Câu 81 – 100+)](#phan-5-progressive-delivery-observability--khac-phuc-su-co-production)

---

## Phần 1: Nguyên Lý GitOps & Kiến Trúc Cốt Lõi Argo CD

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q01</span>
    <span class="qa-question-text">Sự khác biệt bản chất giữa mô hình Push-based CD truyền thống và Pull-based GitOps của Argo CD là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Push CD:</b> CI/CD runner nằm bên ngoài cụm Kubernetes, giữ quyền <code>cluster-admin</code> (hoặc ServiceAccount token) và chủ động "đẩy" (<code>kubectl apply</code>) lệnh vào cụm. Nguy cơ: Lộ credential bảo mật ra bên ngoài, không phát hiện được Configuration Drift nếu có ai đó sửa trực tiếp trên cụm.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Pull GitOps:</b> Argo CD controller chạy trực tiếp *bên trong* cụm (hoặc Hub cluster), liên tục kéo (pull) khai báo từ Git về và so sánh với trạng thái thực tế (<code>Reconciliation Loop</code>). Ưu điểm: Zero-trust credentials (không cần mở cổng mạng Ingress vào cụm), tự động phát hiện và sửa chữa Drift (<code>Self-Healing</code>).</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q02</span>
    <span class="qa-question-text">Chu kỳ thăm dò (polling interval) mặc định của Argo CD tới Git là bao lâu và làm thế nào để đồng bộ tức thì khi có commit mới?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chu kỳ quét mặc định là <b style="color: var(--accent-primary);">180 giây (3 phút)</b>. Để cập nhật tức thì trong vòng 1 giây mà không cần chờ 180s, ta cấu hình <b style="color: var(--accent-primary);">Git Webhooks</b> (GitHub/GitLab/Gitea) trỏ về endpoint <code>/api/webhook</code> của <code>argocd-server</code>. Khi có sự kiện <code>push</code>, Webhook sẽ đánh thức Reconcile loop ngay lập tức.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q03</span>
    <span class="qa-question-text">Argo CD nhận diện và quản lý vòng đời các tài nguyên trên cụm Kubernetes bằng cơ chế Resource Tracking nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Argo CD sử dụng cơ chế <b style="color: var(--accent-primary);">Resource Tracking</b>. Có 3 phương pháp tracking:
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <code>label</code> (Mặc định trước đây): Gắn nhãn <code>app.kubernetes.io/instance: &lt;app-name&gt;</code>.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <code>annotation</code> (Khuyên dùng hiện nay): Gắn annotation <code>argocd.argoproj.io/tracking-id: &lt;app-name&gt;:&lt;group/kind&gt;:&lt;namespace&gt;/&lt;name&gt;</code>.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> <code>annotation+label</code>: Kết hợp cả hai để vừa tương thích UI vừa tránh xung đột tên.</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q04</span>
    <span class="qa-question-text">Điều gì sẽ xảy ra nếu một kỹ sư sửa trực tiếp cấu hình Pod trên cụm Kubernetes khi selfHeal: false?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Khi một kỹ sư dùng lệnh <code>kubectl edit</code> sửa trực tiếp cấu hình trên Live Cluster (ví dụ đổi image hoặc scale số Pod), Argo CD sẽ phát hiện trạng thái <code>OutOfSync</code>. Nhưng vì <code>selfHeal: false</code>, Argo CD không tự động kéo lại trạng thái từ Git. Nếu người vận hành chạy lệnh <code>argocd app sync</code> nhưng trên Git file cấu hình chưa được cập nhật, trạng thái có thể bị lệch mà không được tự khôi phục.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q05</span>
    <span class="qa-question-text">Ba trường bắt buộc cốt lõi trong spec của một Application Custom Resource (CRD) là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>spec.source</code>: Định nghĩa "Nguồn chân lý" (Git repo URL, branch/tag/commit revision, và thư mục path chứa manifests).</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>spec.destination</code>: Định nghĩa "Đích đến triển khai" (Kubernetes API server URL và target namespace).</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>spec.project</code>: Gán ứng dụng vào một <code>AppProject</code> để áp dụng các rào chắn bảo mật và phân quyền RBAC.</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q06</span>
    <span class="qa-question-text">Kiến trúc Argo CD Control Plane gồm 4 microservices chính nào và nhiệm vụ của từng thành phần là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <code>argocd-server</code>: API Gateway tiếp nhận Web UI, CLI, Webhook, xử lý Auth JWT &amp; RBAC.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <code>argocd-repo-server</code>: Clone Git repository, render Helm/Kustomize/CMP sang raw Kubernetes manifests qua cổng gRPC <code>:8081</code>.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> <code>argocd-application-controller</code>: Chạy Reconciliation Loop, tính toán Three-Way Diff, thực thi Auto-Sync, Prune và Self-Heal.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">4.</b> <code>argocd-redis</code>: Bộ nhớ đệm phân tán lưu trữ manifest cache, session token và trạng thái cụm.</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q07</span>
    <span class="qa-question-text">Cơ chế Three-Way Diff trong Argo CD hoạt động như thế nào để phát hiện Configuration Drift?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    So sánh: (1) Manifest mới trên Git (Desired State), (2) Trạng thái thực tế trên Live Cluster (Live State), và (3) Bản ghi cấu hình lần apply trước (<code>Last-Applied-Configuration</code>).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q08</span>
    <span class="qa-question-text">Sự khác biệt giữa lệnh đồng bộ Soft Refresh và Hard Refresh trong Argo CD là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <code>--refresh</code> (Soft) kiểm tra commit Git mới nhưng vẫn dùng lại manifest render trong Redis cache nếu SHA không đổi; <code>--hard-refresh</code> xóa sạch cache Redis và ép <code>repo-server</code> clone và render lại 100% từ đầu.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q09</span>
    <span class="qa-question-text">Tác dụng của cơ chế bảo vệ thư mục Git rỗng trong Argo CD là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Ngăn chặn thảm họa xóa sạch toàn bộ tài nguyên trên cụm Kubernetes nếu thư mục Git bị rỗng ngoài ý muốn (do merge PR nhầm hoặc script CI bị lỗi).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q10</span>
    <span class="qa-question-text">Server-Side Apply (SSA) giải quyết vấn đề gì so với Client-Side Apply?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Loại bỏ giới hạn kích thước 256KB của annotation <code>kubectl.kubernetes.io/last-applied-configuration</code>, nhường việc quản lý trường cho <code>fieldManagers</code> của Kubernetes API Server và tối ưu xử lý xung đột với CRD lớn.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q11</span>
    <span class="qa-question-text">Lợi ích kỹ thuật của tùy chọn ApplyOutOfSyncOnly trong Sync Options là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chỉ apply đúng những tài nguyên đang bị sai lệch (OutOfSync) thay vì gửi toàn bộ 500 file YAML lên etcd, giúp tăng tốc độ đồng bộ lên gấp 10 lần và giảm tải API Server.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q12</span>
    <span class="qa-question-text">Khi gắn Finalizer resources-finalizer.argocd.argoproj.io, hành vi xóa Application sẽ diễn ra thế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Kích hoạt cơ chế <b style="color: var(--accent-primary);">Cascade Deletion</b>: Argo CD sẽ chặn việc xóa Application, tìm và xóa sạch toàn bộ các tài nguyên con (Pods, Services, PVC) trên Kubernetes trước rồi mới xóa Application CRD.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q13</span>
    <span class="qa-question-text">Làm thế nào để xóa một Application trong Argo CD mà vẫn giữ nguyên các tài nguyên đang chạy trên cụm?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chạy lệnh <code>argocd app delete &lt;app-name&gt; --cascade=false</code> hoặc patch gỡ bỏ <code>metadata.finalizers</code> trước khi xóa.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q14</span>
    <span class="qa-question-text">Tại sao trong triết lý GitOps lại cấm tuyệt đối việc sử dụng image tag :latest trên môi trường Production?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Tag <code>:latest</code> là Mutable (có thể bị ghi đè nội dung image mà tag không đổi), phá vỡ nguyên tắc xác định phiên bản bất biến của GitOps và khiến Argo CD không phát hiện được sự thay đổi để Reconcile.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q15</span>
    <span class="qa-question-text">Thông tin kết nối và chứng chỉ của các cụm Kubernetes đích được Argo CD lưu trữ ở đâu và với nhãn gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Được lưu dưới dạng Kubernetes Secret trong namespace <code>argocd</code> có gắn nhãn <code>argocd.argoproj.io/secret-type: cluster</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q16</span>
    <span class="qa-question-text">Biến môi trường nào trong argocd-repo-server quy định thời gian timeout tối đa khi thực thi render manifests?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Biến <code>ARGOCD_EXEC_TIMEOUT</code> (mặc định là <code>90s</code>).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q17</span>
    <span class="qa-question-text">Trong trường hợp nào nên sử dụng tính năng Foreground Deletion thay vì Background Deletion khi xóa tài nguyên?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Khi bạn muốn đảm bảo toàn bộ tài nguyên con phải bị xóa hoàn tất trước khi đối tượng cha được đánh dấu là đã xóa xong.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q18</span>
    <span class="qa-question-text">Tham số backoff.factor trong Retry Policy của Application có ý nghĩa kỹ thuật gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Là hệ số nhân lũy tiến thời gian chờ giữa các lần thử lại đồng bộ thất bại (ví dụ <code>duration: 5s</code>, <code>factor: 2</code> $\rightarrow$ Thử lại sau <code>5s</code>, <code>10s</code>, <code>20s</code>, <code>40s</code>).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q19</span>
    <span class="qa-question-text">Làm thế nào để xem luồng nhật ký log trực tiếp của một Application từ dòng lệnh Argo CD CLI?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Lệnh <code>argocd app logs &lt;app-name&gt; --follow</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q20</span>
    <span class="qa-question-text">Nguyên nhân nào dẫn đến lỗi kết nối gRPC Unavailable khi chạy Argo CD CLI qua Ingress và cách khắc phục?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Do CLI mặc định dùng giao thức HTTP/2 gRPC trong khi Ingress Controller chỉ cấu hình cho HTTP/1.1. Khắc phục bằng cách thêm cờ <code>--grpc-web</code> vào câu lệnh CLI.
  </div>
</details>

---


## Phần 2: Điều Phối Nâng Cao, Kustomize, Helm & Config Management Plugins

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q21</span>
    <span class="qa-question-text">Sự khác biệt giữa Sync Waves và Resource Hooks trong Argo CD là gì và khi nào nên sử dụng loại nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Sync Waves (<code>argocd.argoproj.io/sync-wave</code>):</b> Sắp xếp thứ tự đồng bộ các tài nguyên theo số thứ tự từ bé đến lớn (ví dụ: Wave -1: Namespace/CRD $\rightarrow$ Wave 0: ConfigMap/Secret $\rightarrow$ Wave 1: Deployment). Wave sau chỉ chạy khi toàn bộ tài nguyên của Wave trước đạt trạng thái <code>Healthy</code>.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Resource Hooks (<code>argocd.argoproj.io/hook</code>):</b> Chạy các tác vụ ngắn hạn (thường là Kubernetes Job/Pod) tại các thời điểm cụ thể trong vòng đời Sync: <code>PreSync</code> (chạy Database Migration trước khi roll code), <code>PostSync</code> (gửi thông báo Slack sau khi deploy xong), <code>SyncFail</code> (dọn dẹp khi deploy lỗi).</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Quy tắc lựa chọn:</b> Dùng Sync Waves để điều phối thứ tự tài nguyên Kubernetes chuẩn; dùng Hooks cho các tác vụ Job xử lý nghiệp vụ một lần.</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q22</span>
    <span class="qa-question-text">Khi PreSync Hook Job thất bại, Argo CD xử lý đợt Sync tiếp theo như thế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Quá trình đồng bộ (Sync Phase) sẽ bị <b style="color: var(--accent-primary);">Dừng ngay lập tức (Aborted)</b>. Argo CD sẽ không bao giờ thực thi bước Sync chính (không tạo hay cập nhật Deployment/Service), bảo vệ hệ thống không bị đưa vào trạng thái nửa vời hoặc hỏng Database.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q23</span>
    <span class="qa-question-text">Làm thế nào để viết Custom Lua Health Check cho một Custom Resource Definition (CRD)?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Ta cấu hình script Lua trong ConfigMap <code>argocd-cm</code> dưới thuộc tính <code>resource.customizations.health.&lt;group_kind&gt;</code>. Script Lua nhận đối tượng tài nguyên qua biến <code>obj</code> và trả về bảng trạng thái gồm <code>status</code> (<code>Healthy</code>, <code>Progressing</code>, <code>Degraded</code>, <code>Suspended</code>) và <code>message</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q24</span>
    <span class="qa-question-text">Cách giải quyết xung đột vĩnh viễn giữa HorizontalPodAutoscaler (HPA) và số lượng replicas trong Git?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cấu hình thuộc tính <code>ignoreDifferences</code> trong Application CRD:
    <pre><code class="language-yaml">spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas</code></pre>
    Đồng thời, khuyến nghị xóa hẳn trường <code>spec.replicas</code> trong tệp YAML Deployment trên Git để HPA toàn quyền làm chủ số lượng Pods.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q25</span>
    <span class="qa-question-text">Tính năng Multiple Sources trong Argo CD cho phép kết hợp Helm Chart và values.yaml riêng như thế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cho phép kết hợp Helm Chart công khai từ một kho Helm/OCI với tệp <code>values.yaml</code> nội bộ bảo mật nằm trong một kho Git riêng của doanh nghiệp bằng từ khóa <code>$values</code>:
    <pre><code class="language-yaml">spec:
  sources:
    - repoURL: 'https://charts.bitnami.com/bitnami'
      chart: redis
      targetRevision: 18.0.1
      helm:
        valueFiles:
          - $values/environments/prod/redis-values.yaml
    - repoURL: 'https://github.com/company/internal-configs.git'
      targetRevision: main
      ref: values</code></pre>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q26</span>
    <span class="qa-question-text">Tại sao trong cấu hình JSON Pointer của ignoreDifferences, dấu gạch chéo / trong tên nhãn phải viết thành ~1?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Theo chuẩn <b style="color: var(--accent-primary);">RFC 6901</b>, dấu <code>/</code> là ký tự phân tách cấp độ JSON. Khi tên key chứa dấu <code>/</code>, bắt buộc phải escape thành <code>~1</code> (và <code>~</code> thành <code>~0</code>) để bộ phân tích cú pháp không hiểu nhầm là cấp con mới.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q27</span>
    <span class="qa-question-text">Ý nghĩa kỹ thuật của tùy chọn RespectIgnoreDifferences trong Sync Options là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Ép buộc Argo CD Controller phải bỏ qua các trường đã khai báo trong <code>ignoreDifferences</code> ngay cả trong lúc thực thi lệnh Apply, thay vì chỉ bỏ qua lúc tính toán trạng thái so sánh.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q28</span>
    <span class="qa-question-text">Kustomize ConfigMap Generator kích hoạt rolling update cho Deployment như thế nào khi nội dung config đổi?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Kustomize tự động tính toán mã băm nội dung (Content Hash Suffix) và gắn vào tên ConfigMap (ví dụ <code>config-7b8f9g</code>). Khi nội dung đổi, tên ConfigMap đổi $\rightarrow$ Pod Template trong Deployment đổi $\rightarrow$ Kubernetes tự động kích hoạt <b style="color: var(--accent-primary);">Rolling Update</b> Pods mới.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q29</span>
    <span class="qa-question-text">Config Management Plugins (CMP) phiên bản v2 giao tiếp với repo-server qua phương thức nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Giao tiếp qua <b style="color: var(--accent-primary);">Unix Domain Socket gRPC</b> đặt trong thư mục chia sẻ <code>/var/run/argocd/plugins</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q30</span>
    <span class="qa-question-text">Ba chính sách dọn dẹp Hook (hook-delete-policy) trong Argo CD là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <code>HookSucceeded</code> (xóa khi thành công), <code>HookFailed</code> (xóa khi thất bại), và <code>BeforeHookCreation</code> (xóa bản ghi cũ trước khi tạo Job mới).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q31</span>
    <span class="qa-question-text">Tại sao lệnh generate trong plugin CMP v2 bắt buộc phải in log debug ra STDERR thay vì STDOUT?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Vì Argo CD yêu cầu luồng STDOUT của lệnh <code>generate</code> phải là <b style="color: var(--accent-primary);">100% tài nguyên Kubernetes YAML/JSON hợp lệ</b>. Mọi dòng chữ log in ra STDOUT sẽ làm hỏng bộ phân tích cú pháp AST của Controller. Log thông báo phải chuyển hướng sang <b style="color: var(--accent-primary);">STDERR</b> (<code>&gt;&amp;2</code>).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q32</span>
    <span class="qa-question-text">Làm thế nào để Argo CD kéo Helm Chart từ một kho lưu trữ bảo mật sử dụng giao thức OCI Registry?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Tạo Secret có nhãn <code>argocd.argoproj.io/secret-type: repository</code>, khai báo <code>type: helm</code>, <code>enableOCI: "true"</code> và URL có tiền tố <code>oci://</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q33</span>
    <span class="qa-question-text">Tùy chọn PrunePropagationPolicy và PruneLast trong Sync Options mang lại lợi ích gì cho hệ thống?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Tài nguyên cũ cần prune sẽ chỉ bị xóa sau khi toàn bộ tài nguyên mới đã được apply và đạt trạng thái <code>Healthy</code>, đảm bảo quá trình chuyển đổi Zero-Downtime.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q34</span>
    <span class="qa-question-text">Trạng thái sức khỏe Suspended của tài nguyên trong Argo CD xuất hiện trong những tình huống nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Khi tài nguyên tạm dừng có chủ đích theo nghiệp vụ (ví dụ: CronJob <code>spec.suspend: true</code> hoặc Argo Rollouts Canary đang trong bước Pause).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q35</span>
    <span class="qa-question-text">Làm thế nào để kiểm tra tính hợp lệ của một Lua Health Check script trước khi đưa vào Production bằng CLI?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Lệnh <code>argocd admin settings resource-overrides health &lt;file.yaml&gt; --lua-script &lt;script.lua&gt;</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q36</span>
    <span class="qa-question-text">Cấu trúc Kustomize Base/Overlays giúp tối ưu hóa việc quản lý cấu hình đa môi trường như thế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Đảm bảo nguyên lý <b style="color: var(--accent-primary);">DRY</b>: Cấu hình chung đặt ở Base, các môi trường Dev/Prod chỉ viết các tệp Patch đè lên các tham số riêng biệt (Replicas, CPU/RAM, Ingress), loại bỏ sao chép trùng lặp.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q37</span>
    <span class="qa-question-text">Làm thế nào để ghi đè (override) một tham số Helm values trực tiếp từ câu lệnh CLI mà không cần sửa file YAML?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chạy lệnh <code>argocd app set &lt;app-name&gt; --parameter &lt;key&gt;=&lt;value&gt;</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q38</span>
    <span class="qa-question-text">Tại sao nên luôn đặt thuộc tính activeDeadlineSeconds cho các Kubernetes Job được dùng làm Resource Hook?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Đặt thời gian timeout tối đa cho Job. Nếu Job bị kẹt deadlock, Kubernetes sẽ tự hủy Job sau thời gian này, ngăn chặn việc treo vô hạn toàn bộ tiến trình deploy của Argo CD.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q39</span>
    <span class="qa-question-text">Lợi ích của việc sử dụng cú pháp JQ Path Expressions thay cho RFC 6902 JSON Pointers trong ignoreDifferences là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cho phép lọc động các phần tử trong mảng (ví dụ <code>.spec.containers[] | select(.name == "istio-proxy")</code>) mà không phụ thuộc vào vị trí chỉ số index cố định của phần tử.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q40</span>
    <span class="qa-question-text">Làm thế nào để dừng khẩn cấp một thao tác Sync đang chạy (in-progress) khi phát hiện sự cố?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chạy lệnh <code>argocd app terminate-op &lt;app-name&gt;</code>.
  </div>
</details>

---


## Phần 3: Quy Mô Đa Cụm, App-of-Apps & ApplicationSet Engine

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q41</span>
    <span class="qa-question-text">Mô hình Root App-of-Apps là gì và cơ chế hoạt động tự động hóa của nó ra sao?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Là mô hình quản trị cây thư mục ứng dụng phân tầng. Một <b style="color: var(--accent-primary);">Root Application</b> duy nhất được triển khai trên Argo CD, trỏ tới một thư mục Git chứa định nghĩa của hàng chục <b style="color: var(--accent-primary);">Child Applications</b>. Khi thêm một service mới, kỹ sư chỉ cần commit file <code>application.yaml</code> con vào Git, Root App sẽ tự động phát hiện và sinh ra ứng dụng mới mà không cần chạm tay vào Argo CD UI.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q42</span>
    <span class="qa-question-text">Hãy liệt kê và phân tích vai trò của các loại Generators cốt lõi trong ApplicationSet Engine?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">List Generator:</b> Sinh ứng dụng dựa trên một danh sách tĩnh khai báo trực tiếp trong YAML.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Cluster Generator:</b> Tự động quét các cụm Kubernetes kết nối với Argo CD (dựa vào Labels) để sinh ứng dụng lên từng cụm.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Git Directory/File Generator:</b> Quét cấu trúc thư mục hoặc file JSON/YAML trên kho Git để tự động tạo ứng dụng tương ứng (Zero-Touch Deployment).</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Matrix Generator:</b> Nhân ma trận tích Descartes giữa 2 generators (ví dụ: 10 Microservices $\times$ 5 Cụm = Tự động sinh 50 Ứng dụng con).</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Merge Generator:</b> Gộp các generator và cho phép override các tham số cấu hình cục bộ theo điều kiện.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <b style="color: var(--accent-primary);">Pull Request Generator:</b> Quét các PR đang mở trên GitHub/GitLab để tự động dựng môi trường thử nghiệm tạm thời (Ephemeral/Preview Environment) và tự xóa khi PR đóng.</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q43</span>
    <span class="qa-question-text">Khi Hub Cluster bị mất kết nối mạng với Spoke Cluster, các ứng dụng trên Spoke Cluster có bị dừng hoạt động không?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <b style="color: var(--accent-primary);">Không!</b> Các ứng dụng trên Spoke Cluster vẫn tiếp tục hoạt động bình thường nhờ tính chất phân tán của Kubernetes. Chỉ có luồng cập nhật cấu hình mới (Reconciliation) từ Hub sang Spoke bị tạm hoãn cho đến khi kết nối mạng được phục hồi.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q44</span>
    <span class="qa-question-text">Năm rào chắn an ninh cốt lõi mà một AppProject cung cấp để bảo vệ môi trường đa tenant là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <code>sourceRepos</code>: Giới hạn các kho Git được phép sử dụng.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <code>destinations</code>: Giới hạn các cụm và namespace được phép deploy tới.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> <code>clusterResourceWhitelist / Blacklist</code>: Giới hạn các tài nguyên cấp cụm (Namespace, PV, CRD, ClusterRole).</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">4.</b> <code>namespaceResourceWhitelist / Blacklist</code>: Giới hạn các tài nguyên trong namespace.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">5.</b> <code>syncWindows</code>: Thiết lập khung giờ cấm hoặc cho phép deploy (ngăn deploy vào giờ cao điểm hoặc ban đêm).</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q45</span>
    <span class="qa-question-text">Tại sao Root Application báo Synced màu xanh nhưng một ứng dụng con bên trong lại bị lỗi Degraded?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Do Root App chỉ kiểm tra xem tệp <code>Application CRD</code> con có lưu thành công vào etcd không. Trạng thái lỗi Pods bên trong Child App không tự động nổi lên tầng Root nếu không cấu hình Custom Health Check cho Application CRD.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q46</span>
    <span class="qa-question-text">Làm thế nào để khắc phục giới hạn Rate Limit của GitHub API khi sử dụng Git Generator trong ApplicationSet?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Khai báo GitHub Personal Access Token hoặc GitHub App trong <code>tokenRef</code> (tăng hạn mức từ 60 lên 5,000 requests/giờ) và kết hợp với Git Webhook.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q47</span>
    <span class="qa-question-text">Biến thay thế path.basename trong Git Directory Generator của ApplicationSet trả về giá trị gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Trả về tên của thư mục cuối cùng trong đường dẫn (ví dụ: <code>services/payment-api</code> $\rightarrow$ <code>payment-api</code>).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q48</span>
    <span class="qa-question-text">Làm thế nào để khi xóa một ApplicationSet, các Application con và tài nguyên của chúng không bị xóa theo?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cấu hình <code>spec.syncPolicy.preserveResourcesOnDeletion: true</code> trong ApplicationSet.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q49</span>
    <span class="qa-question-text">ServiceAccount nào được tạo tự động trên Spoke Cluster khi thực hiện kết nối cụm qua lệnh argocd cluster add?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    ServiceAccount <code>argocd-manager</code> (nằm trong namespace <code>kube-system</code>).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q50</span>
    <span class="qa-question-text">Hai loại Sync Windows trong AppProject là gì và vai trò kiểm soát an toàn vận hành của chúng ra sao?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Hỗ trợ 2 loại: <code>kind: allow</code> (chỉ cho phép deploy trong khung giờ này) và <code>kind: deny</code> (cấm tuyệt đối deploy trong khung giờ này).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q51</span>
    <span class="qa-question-text">Hàm template path.basenameNormalized trong ApplicationSet xử lý tên nhánh Git như thế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Tự động chuẩn hóa tên nhánh Git thành định dạng an toàn cho Kubernetes DNS (đổi chữ hoa thành thường, đổi <code>/</code> và <code>_</code> thành dấu <code>-</code>).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q52</span>
    <span class="qa-question-text">Tại sao tên của Application được sinh ra bởi ApplicationSet không được phép chứa dấu gạch dưới (_) hoặc chữ in hoa?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Vì tên Application sẽ trở thành tên đối tượng Kubernetes CRD trên etcd, cấm chứa chữ hoa và dấu gạch dưới <code>_</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q53</span>
    <span class="qa-question-text">Làm thế nào để cấu hình Application quét đệ quy toàn bộ thư mục con bên trong Git repository?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cấu hình <code>spec.source.directory.recurse: true</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q54</span>
    <span class="qa-question-text">Làm thế nào để gắn nhãn (labels) bổ sung cho một cụm Kubernetes đã đăng ký trong Argo CD?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chạy lệnh <code>kubectl label secret &lt;cluster-secret-name&gt; -n argocd &lt;key&gt;=&lt;value&gt;</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q55</span>
    <span class="qa-question-text">Lệnh CLI nào cho phép tạo JWT Project Token cho CI/CD pipeline xác thực vào một AppProject cụ thể?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Lệnh <code>argocd proj role create-token &lt;project-name&gt; &lt;role-name&gt;</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q56</span>
    <span class="qa-question-text">Khi triển khai kiến trúc Hub-and-Spoke, luồng kết nối mạng giữa Hub Cluster và Spoke Cluster cần mở những cổng nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chỉ cần mở kết nối Egress một chiều từ Hub Cluster tới cổng TCP <code>:6443</code> (API Server) của Spoke Cluster.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q57</span>
    <span class="qa-question-text">Merge Generator trong ApplicationSet có vai trò gì trong việc ghi đè tham số cấu hình cho từng cụm?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cho phép gộp các generator và override tham số dựa trên thuộc tính định danh chung (<code>mergeKeys</code>).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q58</span>
    <span class="qa-question-text">Làm thế nào để ngăn chặn các Pull Request từ Fork Repo độc hại kích hoạt dựng Ephemeral Environment trong ApplicationSet?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Sử dụng bộ lọc <code>filters.labels</code> (chỉ build khi Maintainer gắn nhãn <code>safe-to-test</code>) hoặc giới hạn <code>filters.forkMatch: false</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q59</span>
    <span class="qa-question-text">Tại sao lệnh argocd cluster add có thể bị lỗi xác thực trên các phiên bản Kubernetes 1.24+ mới?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Do Kubernetes 1.24+ chuyển sang dùng Token ServiceAccount có thời hạn ngắn. Cần tạo Secret tĩnh gắn annotation <code>kubernetes.io/service-account.name</code> để cấp token dài hạn.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q60</span>
    <span class="qa-question-text">Sự khác biệt cốt lõi giữa List Generator và Matrix Generator trong ApplicationSet là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    List Generator chỉ duyệt qua 1 danh sách tĩnh 1 chiều; Matrix Generator nhân ma trận 2 chiều giữa 2 generator độc lập (ví dụ Dịch vụ $\times$ Cụm).
  </div>
</details>

---

## Phần 4: Bảo Mật, RBAC, SSO/OIDC, Secrets Management & Disaster Recovery

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q61</span>
    <span class="qa-question-text">Cú pháp phân quyền Casbin CSV trong argocd-rbac-cm có định dạng chuẩn như thế nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Định dạng chuẩn gồm 6 trường:
    <pre><code>p, &lt;subject/role&gt;, &lt;resource&gt;, &lt;action&gt;, &lt;object&gt;, &lt;effect&gt;</code></pre>
    Ví dụ:
    <code>p, role:developer, applications, sync, ecommerce-project/*, allow</code> (Cho phép role <code>developer</code> được thực thi lệnh <code>sync</code> trên toàn bộ ứng dụng thuộc project <code>ecommerce-project</code>).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q62</span>
    <span class="qa-question-text">So sánh 3 giải pháp quản lý Secret trong GitOps: Sealed Secrets, External Secrets Operator (ESO), và SOPS.</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"><b style="color: var(--accent-primary);">&bull; Bitnami Sealed Secrets:</b> Mã hóa Secret bất đối xứng (Asymmetric Encryption) bằng Public Key phía client (<code>kubeseal</code>), an toàn đẩy lên Git. Controller trong cụm giữ Private Key để giải mã thành Kubernetes Secret. Điểm mạnh: Nhẹ, không phụ thuộc hạ tầng Cloud bên ngoài.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"><b style="color: var(--accent-primary);">&bull; External Secrets Operator (ESO):</b> Đồng bộ Secret từ các dịch vụ bên ngoài (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault, GCP Secret Manager) vào cụm qua đối tượng <code>ExternalSecret</code> CRD. Điểm mạnh: Quản trị tập trung chuẩn doanh nghiệp.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);"><b style="color: var(--accent-primary);">&bull; Mozilla SOPS:</b> Mã hóa từng giá trị (value) trong file YAML/JSON bằng khóa KMS (AWS/GCP/Azure) hoặc PGP. Tích hợp trực tiếp qua CMP Plugin.</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q63</span>
    <span class="qa-question-text">Tại sao nên vô hiệu hóa tài khoản cục bộ admin (admin.enabled: "false") khi đã tích hợp Dex OIDC SSO?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Tài khoản <code>admin</code> mặc định là tài khoản toàn quyền (God-mode), dùng chung mật khẩu tĩnh, không có xác thực đa yếu tố (MFA) và khó thực hiện Audit Log truy vết cá nhân. Tắt tài khoản này và bắt buộc đăng nhập qua SSO (Okta, Google, Azure AD) giúp áp dụng nguyên lý Zero Trust và kiểm soát định danh tập trung.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q64</span>
    <span class="qa-question-text">Quy trình Disaster Recovery (Khôi phục thảm họa) Argo CD thực hiện như thế nào khi toàn bộ Data Center bị phá hủy?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> Khởi tạo cụm Kubernetes mới tại Data Center dự phòng.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> Cài đặt Argo CD bản sạch.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> Nạp lại toàn bộ cấu hình khai báo từ file sao lưu đã mã hóa bằng lệnh: <code>argocd admin import -n argocd &lt; argocd-backup.yaml</code></div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">4.</b> Sau khi import, Argo CD Controller sẽ tự động kết nối lại kho Git và tự động kéo/tái lập toàn bộ hàng trăm ứng dụng lên cụm mới.</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q65</span>
    <span class="qa-question-text">Sáu loại tài nguyên được kiểm soát bởi Casbin RBAC trong Argo CD là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <code>applications</code>, <code>clusters</code>, <code>repositories</code>, <code>projects</code>, <code>accounts</code>, và <code>logs</code>/<code>exec</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q66</span>
    <span class="qa-question-text">Scope OIDC nào bắt buộc phải khai báo để Argo CD nhận diện được danh sách nhóm người dùng cho RBAC?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Scope <b style="color: var(--accent-primary);"><code>groups</code></b> trong <code>oidc.config.requestedScopes</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q67</span>
    <span class="qa-question-text">Sự khác biệt về Callback Redirect URI giữa Direct OIDC và Dex Broker là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Direct OIDC là <code>https://&lt;host&gt;/auth/callback</code>; Dex Broker là <code>https://&lt;host&gt;/api/dex/callback</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q68</span>
    <span class="qa-question-text">Ba chế độ Scope trong Bitnami Sealed Secrets là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <code>strict</code> (khóa theo Name + Namespace), <code>namespace-wide</code> (khóa theo Namespace), và <code>cluster-wide</code> (dùng toàn cụm).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q69</span>
    <span class="qa-question-text">Tại sao readOnlyRootFilesystem: true trên argocd-repo-server bắt buộc phải mount emptyDir vào /tmp?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Vì <code>repo-server</code> cần ghi các tệp tạm khi clone Git và render Helm/Kustomize vào <code>/tmp</code>. Nếu không mount <code>emptyDir</code>, tiến trình render sẽ sập vì không có quyền ghi đĩa.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q70</span>
    <span class="qa-question-text">Lệnh CLI nào dùng để kiểm tra tính hợp lệ của toàn bộ bảng phân quyền argocd-rbac-cm?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Lệnh <code>argocd admin settings rbac validate</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q71</span>
    <span class="qa-question-text">Điều gì xảy ra nếu Sealed Secret Controller bị mất Private Key trên cụm?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Toàn bộ các file <code>SealedSecret</code> đã mã hóa trên Git sẽ vĩnh viễn không thể giải mã được nữa. Cần backup Secret Private Key định kỳ.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q72</span>
    <span class="qa-question-text">Cổng TCP nào bắt buộc phải mở giữa argocd-application-controller và argocd-repo-server trong NetworkPolicy?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cổng <b style="color: var(--accent-primary);">TCP <code>:8081</code></b> (giao thức gRPC).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q73</span>
    <span class="qa-question-text">Biến môi trường nào được sử dụng để kích hoạt tính năng Controller Sharding?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Biến <code>ARGOCD_CONTROLLER_REPLICAS</code> (chạy trên StatefulSet).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q74</span>
    <span class="qa-question-text">Lệnh CLI nào cho phép đăng nhập Argo CD qua giao diện SSO trên trình duyệt?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Lệnh <code>argocd login &lt;host&gt; --sso --grpc-web</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q75</span>
    <span class="qa-question-text">Làm thế nào để kiểm tra quyền hạn của một vai trò cụ thể qua CLI?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chạy lệnh <code>argocd account can-i &lt;action&gt; &lt;resource&gt; &lt;sub-object&gt;</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q76</span>
    <span class="qa-question-text">Chuẩn Pod Security Standards (PSS) Restricted yêu cầu UID chạy container tối thiểu là bao nhiêu?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Yêu cầu chạy dưới User non-root (UID khác 0, ví dụ UID <code>999</code> hoặc <code>10001</code>).
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q77</span>
    <span class="qa-question-text">Cơ chế External Secrets Operator (ESO) kết nối với HashiCorp Vault qua phương thức xác thực nào là an toàn nhất?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Xác thực bằng <b style="color: var(--accent-primary);">Kubernetes ServiceAccount Token</b> (Vault Kubernetes Auth Method), không dùng secret tĩnh.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q78</span>
    <span class="qa-question-text">Làm thế nào để vô hiệu hóa tính năng Web Terminal vào Pod trên Argo CD?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cấu hình <code>exec.enabled: "false"</code> trong <code>argocd-cm</code> hoặc phân quyền <code>p, &lt;role&gt;, exec, create, *, deny</code> trong <code>argocd-rbac-cm</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q79</span>
    <span class="qa-question-text">Tại sao Secret argocd-initial-admin-secret bắt buộc phải xóa sau khi cài đặt?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Vì nó chứa mật khẩu admin khởi tạo dạng plaintext, vi phạm chuẩn an ninh CIS Kubernetes Benchmark.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q80</span>
    <span class="qa-question-text">Lệnh CLI argocd admin export xuất dữ liệu ra định dạng gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Xuất toàn bộ trạng thái cấu hình tĩnh (CRD, ConfigMap, Secret) ra định dạng <b style="color: var(--accent-primary);">Kubernetes YAML Stream</b> chuẩn.
  </div>
</details>

---

## Phần 5: Progressive Delivery, Observability & Khắc Phục Sự Cố Production

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q81</span>
    <span class="qa-question-text">Sự khác biệt cơ bản giữa Kubernetes Deployment tiêu chuẩn và Argo Rollouts là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Deployment tiêu chuẩn của Kubernetes chỉ hỗ trợ chiến lược Rolling Update thô sơ (thay thế dần từng Pod cũ bằng Pod mới) mà không có khả năng kiểm soát tỷ lệ Traffic mạng, không hỗ trợ tạm dừng theo dõi và không thể tự động Rollback dựa trên số liệu PromQL. <b style="color: var(--accent-primary);">Argo Rollouts</b> là giải pháp Progressive Delivery cung cấp chiến lược <b style="color: var(--accent-primary);">Canary Release</b> (chia nhỏ traffic 10% &rarr; 30% &rarr; 100%), <b style="color: var(--accent-primary);">Blue-Green Deployment</b> và tích hợp <code>AnalysisTemplate</code> để tự động đo lường số liệu Prometheus/Datadog.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q82</span>
    <span class="qa-question-text">Trong Argo Rollouts Canary, cơ chế AnalysisRun tự động Rollback hoạt động như thế nào khi tỷ lệ lỗi HTTP 5xx tăng vọt?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Trong tệp <code>Rollout</code>, ta liên kết với một <code>AnalysisTemplate</code>. Template này thực thi định kỳ các câu truy vấn PromQL (ví dụ đo <code>http_requests_total</code> lỗi 5xx chia cho tổng request). Nếu kết quả vượt ngưỡng <code>failureLimit</code> (ví dụ Error Rate &gt; 1%), <code>AnalysisRun</code> sẽ chuyển sang trạng thái <code>Failed</code>. Argo Rollouts Controller ngay lập tức ngắt toàn bộ traffic đến Pods Canary và trả lại 100% traffic cho phiên bản ổn định cũ trong vòng chưa đầy 1 giây.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q83</span>
    <span class="qa-question-text">Cần cấu hình những gì để Argo CD Notifications gửi tin nhắn cảnh báo trực tiếp về kênh Telegram hoặc Slack khi ứng dụng bị Degraded?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cần cấu hình 4 thành phần trong ConfigMap <code>argocd-notifications-cm</code>:
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <b style="color: var(--accent-primary);">Services:</b> Khai báo Bot Token và Chat ID của Telegram / Webhook URL của Slack.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <b style="color: var(--accent-primary);">Templates:</b> Soạn thảo mẫu tin nhắn thông báo (chứa biến <code>&#123;&#123;.app.metadata.name&#125;&#125;</code>, <code>&#123;&#123;.app.status.sync.status&#125;&#125;</code>).</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> <b style="color: var(--accent-primary);">Triggers:</b> Định nghĩa điều kiện kích hoạt (ví dụ: <code>when: app.status.health.status == 'Degraded'</code>).</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">4.</b> <b style="color: var(--accent-primary);">Subscriptions:</b> Đăng ký nhận thông báo cho Application qua annotation: <code>notifications.argoproj.io/subscribe.on-degraded.telegram: &lt;chat_id&gt;</code>.</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q84</span>
    <span class="qa-question-text">Bốn chỉ số PromQL vàng (Golden Metrics) mà mọi SRE phải theo dõi trên Grafana cho Argo CD là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <code>argocd_app_reconcile_count</code>: Tần suất và số lượng đợt Reconcile của Controller.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <code>argocd_app_sync_total</code>: Tổng số lượt Sync ứng dụng phân theo trạng thái (Success vs Failed).</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> <code>argocd_git_request_duration_seconds</code>: Thời gian trễ khi kết nối và clone kho Git.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">4.</b> <code>argocd_redis_request_duration_seconds</code>: Độ trễ truy vấn bộ nhớ đệm Redis Cache.</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q85</span>
    <span class="qa-question-text">Làm thế nào để xử lý sự cố Pod argocd-repo-server bị lỗi OOMKilled (Out Of Memory) liên tục?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">&bull; Tăng cấu hình <code>resources.limits.memory</code> từ 1Gi lên 2Gi - 4Gi.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">&bull; Cấu hình biến môi trường <code>ARGOCD_EXEC_TIMEOUT: "180s"</code> để tránh các tiến trình render kẹt vô hạn.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">&bull; Tăng số lượng Replicas của <code>argocd-repo-server</code> lên 3 - 5 Pods để chia sẻ tải biên dịch manifests.</div>
    <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">&bull; Đảm bảo mount <code>emptyDir</code> vào <code>/tmp</code> để không làm nghẽn bộ nhớ đệm trên đĩa.</div>
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q86</span>
    <span class="qa-question-text">Thuộc tính oncePer trong Argo CD Notifications Trigger giải quyết vấn đề gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Ngăn chặn hiện tượng <b style="color: var(--accent-primary);">Notification Storm</b> (bão tin nhắn spam) khi Pod bị lỗi flapping liên tục giữa Progressing và Degraded.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q87</span>
    <span class="qa-question-text">Lệnh CLI nào dùng để theo dõi trực quan quá trình Canary Release của Argo Rollouts trên Terminal?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Lệnh <code>kubectl argo rollouts get rollout &lt;rollout-name&gt; --watch</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q88</span>
    <span class="qa-question-text">Làm thế nào để thúc đẩy một đợt Rollout vượt qua bước pause: {} thủ công?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chạy lệnh <code>kubectl argo rollouts promote &lt;rollout-name&gt;</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q89</span>
    <span class="qa-question-text">Cổng phát metrics Prometheus mặc định của argocd-application-controller là cổng nào?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cổng <b style="color: var(--accent-primary);">TCP <code>:8082</code></b>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q90</span>
    <span class="qa-question-text">Mã ID của Dashboard tổng quan chính thức của Argo CD trên Grafana Community là bao nhiêu?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Mã <b style="color: var(--accent-primary);">ID: <code>14584</code></b>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q91</span>
    <span class="qa-question-text">Hiện tượng "Reconcile Storm" xuất hiện khi nào và cách khắc phục?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Xuất hiện khi hàng ngàn ứng dụng đồng thời hết hạn cache 180s làm CPU Controller quá tải 100%. Khắc phục bằng cách tăng <code>timeout.reconciliation: "600s"</code>, bật Controller Sharding và dùng Webhook.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q92</span>
    <span class="qa-question-text">Làm thế nào để gửi thử một thông báo test từ Notifications Controller qua dòng lệnh?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chạy lệnh <code>kubectl exec -n argocd deploy/argocd-notifications-controller -- argocd-notifications template notify &lt;template-name&gt; &lt;app-name&gt; --recipient &lt;service&gt;:&lt;dest&gt;</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q93</span>
    <span class="qa-question-text">Sự khác biệt giữa canaryService và stableService trong Argo Rollouts là gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    <code>stableService</code> luôn trỏ vào các Pods phiên bản ổn định cũ (nhận phần lớn traffic); <code>canaryService</code> trỏ vào các Pods phiên bản mới để phục vụ lưu lượng thử nghiệm hoặc kiểm thử nội bộ.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q94</span>
    <span class="qa-question-text">Làm thế nào để ép buộc Argo Rollouts hủy bỏ đợt phát hành và Rollback ngay lập tức qua CLI?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Chạy lệnh <code>kubectl argo rollouts abort &lt;rollout-name&gt;</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q95</span>
    <span class="qa-question-text">Metric nào phản ánh số lượng ứng dụng đang rơi vào trạng thái Degraded trong Prometheus?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Metric <code>argocd_app_health_status&#123;health_status="Degraded"&#125;</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q96</span>
    <span class="qa-question-text">Khi GitHub Webhook bắn tín hiệu về Argo CD nhưng ứng dụng không tự cập nhật, cần kiểm tra những gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Kiểm tra: (1) Secret Webhook trong <code>argocd-secret</code> khớp với GitHub secret, (2) NetworkPolicy có cho phép Ingress vào port 80/443 của <code>argocd-server</code>, (3) URL repo trong Application khớp 100% với URL trong Webhook payload.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q97</span>
    <span class="qa-question-text">Tùy chọn failureLimit: 2 trong AnalysisTemplate có ý nghĩa gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Cho phép câu truy vấn PromQL đo lường thất bại tối đa 2 lần liên tiếp. Nếu thất bại đến lần thứ 3, đợt AnalysisRun sẽ bị đánh trượt và kích hoạt Rollback.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q98</span>
    <span class="qa-question-text">Trong Blue-Green Deployment của Argo Rollouts, thuộc tính autoPromotionEnabled: false có tác dụng gì?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Ngăn không cho Rollouts tự động chuyển đổi traffic sang môi trường Green mới, bắt buộc kỹ sư phải kiểm thử thủ công trên <code>previewService</code> và chạy lệnh promote thì mới đổi cờ traffic.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q99</span>
    <span class="qa-question-text">Lệnh nào kiểm tra xem Controller có đang bị kẹt hàng đợi Workqueue xử lý không?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Kiểm tra metric <code>workqueue_depth&#123;name="app_reconciliation_queue"&#125;</code> qua cổng <code>:8082</code>.
  </div>
</details>

<details class="qa-card">
  <summary class="qa-summary">
    <span class="qa-num-badge">Q100</span>
    <span class="qa-question-text">Bẫy "Synced nhưng sai đa tầng" (The Multi-Layer Synced Trap) là gì và làm thế nào để phòng chống triệt để?</span>
  </summary>
  <div class="qa-answer">
    <div class="qa-answer-header">
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
    </div>
    Là hiện tượng Root App báo <code>Synced</code> màu xanh nhưng bên dưới dính 3 tầng lỗi ngầm: (1) SealedSecret giải mã sập, (2) Rollout bị Prometheus rollback về code cũ, (3) NetworkPolicy chặn gRPC reconcile code mới. Phòng chống bằng cách thực thi <b style="color: var(--accent-primary);">Quy trình kiểm thử nghiệm thu Production Handover Audit 5 bước</b> đối soát tận gốc Live State.
  </div>
</details>

---

## Bảng Tổng Kết Lộ Trình 25 Chuyên Đề Argo CD & GitOps Enterprise

```mermaid
flowchart LR
    G1["Giai Đoạn 1<br/>Nền Tảng GitOps<br/>(Bài 01 - 05)"]
    G2["Giai Đoạn 2<br/>Đồng Bộ Nâng Cao<br/>(Bài 06 - 10)"]
    G3["Giai Đoạn 3<br/>Quy Mô Đa Cụm<br/>(Bài 11 - 16)"]
    G4["Giai Đoạn 4<br/>Bảo Mật & Rollouts<br/>(Bài 17 - 22)"]
    G5["Giai Đoạn 5<br/>Production & Capstone<br/>(Bài 23 - 25)"]

    G1 --> G2 --> G3 --> G4 --> G5

    style G1 fill:none
    style G2 fill:none
    style G3 fill:none
    style G4 fill:none
    style G5 fill:none
```

---

## Lời Kết

Chúc mừng bạn đã hoàn thành trọn vẹn **Series 25 Chuyên Đề Argo CD & GitOps Enterprise Architecture**! 

Hành trình từ những dòng manifest đầu tiên cho tới việc thiết kế và vận hành hệ thống E-commerce đa cụm cấp doanh nghiệp là một bước tiến vượt bậc trong sự nghiệp kỹ thuật của bạn. Hãy lưu giữ bộ cẩm nang 100+ câu hỏi phỏng vấn này, liên tục thực hành trên các môi trường lab thực tế và tự tin khẳng định vị thế **GitOps Platform Lead** trong mọi dự án công nghệ lớn!

> [!NOTE]
> **Hoàn Tất Khóa Học:** Chúc mừng bạn đã hoàn thành toàn bộ 25 bài học thuộc series **ArgoCD & GitOps Mastery**. Hãy tiếp tục áp dụng các kiến thức chuẩn SRE vào hệ thống thực tế và tối ưu hóa hạ tầng Kubernetes của bạn!

{% endraw %}

