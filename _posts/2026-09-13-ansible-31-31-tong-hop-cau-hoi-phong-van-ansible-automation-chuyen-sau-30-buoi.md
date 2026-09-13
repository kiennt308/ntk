---
layout: post
title: "[Bài 31] Tuyển Tập 100+ Câu Hỏi Phỏng Vấn Ansible Automation & DevOps Chuyên Sâu (30 Buổi)"
date: 2026-09-13 01:50:00 +0700
categories: [Ansible]
tags:
  - Ansible
  - Automation
  - IaC
  - DevOps
  - Linux
  - Part-31
series: "Ansible Automation Mastery"
series_order: 31
difficulty: Advanced
thumbnail: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80"
summary: "[Ansible P.31] Đại cẩm nang tổng hợp hơn 350 câu hỏi phỏng vấn Ansible Automation chuyên sâu từ 30 chuyên đề: kiến trúc agentless, module FQCN, idempotency, variable precedence, Jinja2, roles/collections, vault security, tối ưu forks/pipelining và AWX/AAP."
tldr:
  - "Nắm vững nguyên lý nền tảng và tư duy cốt lõi về Tuyển Tập 100+ Câu Hỏi Phỏng Vấn Ansible Automation & DevOps Chuyên Sâu (30 Buổi)."
  - "Xây dựng hạ tầng tự động hóa với tính Idempotency tuyệt đối qua Playbooks, Roles và Ansible Collections."
  - "Quản trị cấu hình máy chủ quy mô lớn an toàn, bảo mật dữ liệu nhạy cảm với Ansible Vault."
  - "Tự kiểm tra kiến thức chuyên sâu với bộ 10 câu hỏi phân tích tình huống thực tế kèm lời giải."
---
{% raw %}
# [BÀI 31] TUYỂN TẬP 100+ CÂU HỎI PHỎNG VẤN ANSIBLE AUTOMATION & DEVOPS CHUYÊN SÂU (30 BUỔI)

Bộ tài liệu đúc kết toàn bộ câu hỏi phỏng vấn thực chiến, bảng tiêu chí chấm điểm kỹ thuật và các câu hỏi đào sâu (Deep Dive) từ chuỗi 30 chuyên đề đào tạo chuyên gia tự động hóa Ansible Automation & DevOps Engineering.

---

### [Chuyên Đề 01] Tư Duy Configuration Management & Triết Lý Agentless Của Ansible: Push-Based vs Pull-Based & Idempotency

Gọi ngẫu nhiên, học viên đứng trả lời. Chấm ngay thang **0–3**: `0` không trả lời · `1` nhớ từ khoá sai
cơ chế · `2` đúng cơ chế · `3` đúng cơ chế **và** nêu lệnh/con số chứng minh. Câu 🔥 là câu tủ (≥2 phải
đạt); câu ★★★ phân loại mạnh.

**Hai lỗi làm trần điểm là 1:**
- Dùng **"PLAY RECAP xanh"** làm bằng chứng thay vì chạy lần hai + `docker exec` kiểm máy đích.
- Nộp/khẳng định một playbook **không idempotent** (chạy lần hai vẫn `changed` không lý do) là "đã xong".

## V2. Bộ câu hỏi — ĐÚNG 12 câu


<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Push: control node chủ động đẩy module qua SSH khi ta chạy. Agentless: máy đích <b style="color: var(--accent-primary);">không</b>
cần agent Ansible, chỉ cần <b style="color: var(--accent-primary);">Python + sshd</b>. Kết nối do control node khởi tạo, chạy xong đóng.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 sai · 1 nói "không cần agent" mà không rõ · 2 đúng push+agentless · 3 kèm "máy đích chỉ cần Python+sshd" và ví dụ <code>ping</code>.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> So với Puppet cổ điển? *(Puppet pull+agent, tự kéo theo chu kỳ.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Chạy playbook lần hai trên máy đã đúng trạng thái <b style="color: var(--accent-primary);">không đổi gì</b>. Bằng chứng:
<code>changed=0</code> ở PLAY RECAP lần hai. Mô tả *trạng thái muốn*, không phải *lệnh cần chạy*.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 không biết · 1 "chạy lại vẫn được" · 2 nêu <code>changed=0</code> · 3 kèm cách chứng minh (chạy hai lần) và vì sao nó là linh hồn CM.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Lần hai vẫn <code>changed</code> mà không ai đổi máy — nghi gì? *(Task <code>command</code>/<code>shell</code> không idempotent.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Chúng không có khái niệm trạng thái, chỉ chạy lệnh → luôn <code>changed</code>. Sửa: dùng module
chuyên (idempotent), hoặc thêm <code>creates</code>/<code>removes</code>/<code>changed_when</code> để chặn chạy lại/định nghĩa "đổi".
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 không biết · 1 "shell xấu" chung chung · 2 đúng lý do · 3 kèm <code>creates</code>/<code>changed_when</code> và ví dụ module chuyên thay thế.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Khi nào buộc phải dùng <code>shell</code>? *(Khi không có module chuyên; khi đó thêm creates/changed_when.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Không. Recap chỉ tổng hợp cái <b style="color: var(--accent-primary);">module báo cáo</b> cho controller. <code>ignore_errors</code> giấu
lỗi, <code>changed_when: false</code> che thay đổi, nhầm inventory chạy sai host — recap vẫn xanh. Kiểm máy đích:
<code>docker exec ... systemctl is-active</code>.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 "recap xanh là xong" (trần 1) · 1 mơ hồ · 2 nói recap không đủ · 3 kèm ≥2 ca xanh-mà-sai và lệnh kiểm máy đích.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Kiểm dịch vụ chạy thật bằng lệnh gì? *(<code>docker exec <target> systemctl is-active <svc></code>.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<code>ignore_errors: true</code> (biến task đỏ thành tiếp tục), <code>changed_when: false</code> (ép luôn <code>ok</code>),
nhầm inventory pattern (chạy đúng nhưng trên host khác cái ta tưởng).
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 không biết · 1 một cách · 2 hai cách · 3 ba cách + hệ quả từng cái.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> <code>ignore_errors</code> có bao giờ hợp lý không? *(Có — khi lỗi dự kiến và xử ở task sau; phải có chủ đích.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Danh sách máy bị quản + nhóm + biến kết nối (host, user). Pattern (<code>all</code>, tên nhóm,
<code>web:!db</code>) chọn tập host mỗi lần chạy. Kiểm: <code>ansible-inventory --graph</code>, <code>ansible <pattern> --list-hosts</code>.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 không biết · 1 "danh sách máy" · 2 đủ + pattern · 3 kèm lệnh kiểm và vì sao kiểm trước khi chạy task đổi trạng thái.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Vì sao kiểm <code>--list-hosts</code> trước? *(Tránh chạy nhầm máy — recap xanh trên sai host.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Ad-hoc: một module một lần (<code>ansible <pat> -m <mod> -a "..."</code>), nhanh, không lưu, không
version. Playbook: nhiều task, lặp lại được, đưa vào git. Việc >1 lần hoặc cần review → playbook.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 không biết · 1 nêu tên · 2 đúng khác biệt · 3 kèm tiêu chí chọn và "mất vết" khi ad-hoc prod.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Ad-hoc có idempotent không? *(Có nếu dùng module idempotent — cùng module với playbook.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Ansible push + agentless (chạy khi gọi, không agent); Puppet/Chef cổ điển pull + agent
(tự kéo theo chu kỳ). Push: đơn giản, nhanh triển khai, kiểm soát thời điểm. Pull: hội tụ liên tục, tự
sửa drift, mở rộng hạm đội lớn tốt hơn.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 "giống nhau" · 1 nói khác mà không rõ · 2 đúng push/pull · 3 kèm đánh đổi hai chiều.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Muốn Ansible hội tụ định kỳ thì sao? *(Lên lịch cron/AWX — Ansible không tự chạy nền.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Ansible = configuration management (cấu hình bên trong máy đã có, không state tập trung);
Terraform = provisioning (tạo/huỷ hạ tầng, có state, plan/diff). Ghép: Terraform dựng VM → xuất IP →
Ansible dùng IP làm inventory cài phần mềm.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 "giống nhau" · 1 khác mà không rõ · 2 đúng phân vai · 3 kèm mẫu ghép cụ thể.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Dùng Terraform <code>provisioner</code> cài phần mềm có nên không? *(Không — chống thiết kế, không idempotent; dùng Ansible.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Do <b style="color: var(--accent-primary);">SSH/inventory</b>: chưa trao key, sai <code>ansible_host</code>/user, host không tới được. KHÔNG
phải do module hay logic playbook — module còn chưa chạy được vì chưa kết nối. Kiểm <code>ssh ansible@<ip> true</code>.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 đổ lỗi module · 1 "lỗi kết nối" · 2 chỉ ra SSH/inventory · 3 kèm bước chẩn đoán (<code>ssh ... true</code>, <code>--list-hosts</code>).
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Khác <code>FAILED</code> chỗ nào? *(UNREACHABLE = không kết nối được; FAILED = kết nối được nhưng task lỗi.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Nêu rõ module thuộc collection nào, tránh nhầm khi tên trùng giữa các collection, và ổn
định khi bản đổi (nhiều module đã rời <code>ansible.builtin</code> sang collection riêng). Rõ ràng, dễ bảo trì.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 không biết · 1 "tên đầy đủ" · 2 đúng lý do · 3 kèm ví dụ nhầm tên và bối cảnh module rời collection.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> <code>ansible-doc -l</code> dùng làm gì? *(Liệt kê module có sẵn để tra FQCN đúng.)*
</div>
</details>

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
Dựng inventory → <code>ping</code> (SUCCESS) → viết <code>site.yml</code> module chuyên → chạy (recap
<code>failed=0</code>) → <b style="color: var(--accent-primary);">kiểm thật</b> <code>docker exec systemctl is-active</code> → chạy <b style="color: var(--accent-primary);">lần hai</b> (<code>changed=0</code>, idempotent)
→ (bẫy) thấy <code>shell</code> không idempotent → sửa bằng <code>creates</code> → thấy <code>ignore_errors</code> giấu lỗi. Ba chỗ kiểm
thật: sau chạy lần một, sau lần hai, và sau khi sửa task shell.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 0 kể thiếu · 1 chỉ chạy một lần · 2 đủ vòng đời · 3 đủ + ba điểm kiểm thật + bài học ignore_errors.
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu recap <code>failed=0</code> mà dịch vụ inactive thì kết luận gì? *(Không tin recap; có thể <code>ignore_errors</code>/nhầm host — kiểm máy đích.)*
</div>
</details>

## V3. Câu chốt để nói khi phỏng vấn

1. *"Ansible push + agentless: control node đẩy module qua SSH, máy đích chỉ cần Python và sshd — nên
   triển khai không phải cài agent trên hàng trăm máy."*
2. *"Bài kiểm tra thật của một playbook là chạy lần hai: phải `changed=0`. Nếu không, tôi tìm task
   `command`/`shell` và làm nó idempotent bằng `creates` hoặc module chuyên."*
3. *"Tôi không tin PLAY RECAP một mình — `ignore_errors` và `changed_when:false` làm nó xanh mà máy sai;
   tôi kiểm trên máy đích bằng `systemctl is-active` hoặc đọc file cấu hình."*
4. *"Ansible lo configuration, Terraform lo provisioning; tôi ghép: Terraform dựng VM rồi Ansible cài phần
   mềm — không lạm dụng `provisioner`."*

## V4. Bảng ghi điểm

| Câu | Chủ đề | Điểm 0–3 |
|---|---|---|
| 1 | Push, agentless | |
| 2 | Idempotency | |
| 3 | command/shell không idempotent | |
| 4 | PLAY RECAP không phải sự thật | |
| 5 | Ba cách xanh-mà-sai | |
| 6 | Inventory, pattern | |
| 7 | Ad-hoc vs playbook | |
| 8 | Ansible vs Puppet/Chef | |
| 9 | Ansible vs Terraform | |
| 10 | UNREACHABLE | |
| 11 | FQCN | |
| 12 | Tổng hợp | |
| **Tổng /36** | | |

Quy đổi: ≥ 30 giỏi · 24–29 khá · 18–23 đạt · < 18 chưa đạt (học lại §4–§6).

**Lỗi làm trần điểm là 1:** dùng "PLAY RECAP xanh" làm bằng chứng · khẳng định playbook không idempotent là "xong".

## V5. Bài tập về nhà

- **BTVN 1.** Viết `so-sanh.md`: Ansible vs Puppet vs Terraform (3 trục: mô hình push/pull, agent, mục đích).
- **BTVN 2.** Tự dựng lại vòng đời ở nhà, nộp recap hai lần chạy (lần hai `changed=0`) + `docker exec` kiểm dịch vụ.
- **BTVN 3.** Lấy một task `shell` bất kỳ, làm nó idempotent hai cách (module chuyên và `creates`); so sánh.
- **BTVN 4 — Chuẩn bị cho buổi 02 (đúng 3 câu):**
  1. Control node cần gì để chạy Ansible, và vì sao managed node chỉ cần Python + sshd? *(dẫn vào cài đặt + kiến trúc buổi 02)*
  2. `ansible.cfg` là gì, ba thiết lập hay dùng nhất là gì? *(dẫn vào cấu hình control node)*
  3. Lệnh ad-hoc `ansible all -m setup` trả về gì, dùng làm gì? *(dẫn vào facts, và ad-hoc sâu hơn buổi 02)*

Ba câu này dẫn vào buổi 02 — *Cài đặt, kiến trúc, lệnh ad-hoc*: control node, `ansible.cfg`, SSH,
module setup/facts, và các module ad-hoc thường dùng.

---


### [Chuyên Đề 02] Kiến Trúc Ansible & Lệnh Ad-Hoc: Control Node, Managed Nodes, SSH Authentication & Thực Thi Module Tức Thì

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Trình bày chi tiết thứ tự ưu tiên 4 tầng khi Ansible tìm kiếm file cấu hình <code>ansible.cfg</code>. Làm sao biết hệ thống đang dùng file nào? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b> Ansible tìm kiếm theo thứ tự ưu tiên giảm dần: (1) Biến môi trường <code>ANSIBLE_CONFIG</code>, (2) File <code>./ansible.cfg</code> tại thư mục hiện tại, (3) File ẩn <code>~/.ansible.cfg</code> tại thư mục cá nhân người dùng, (4) File cấu hình mặc định hệ thống <code>/etc/ansible/ansible.cfg</code>. Để biết chính xác file đang được áp dụng, chạy lệnh <code>ansible --version</code> và quan sát dòng <code>config file = ...</code>.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b> 
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không nêu được các tầng cấu hình.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Liệt kê được 2-3 tầng nhưng sai thứ tự ưu tiên.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Nêu đúng 4 tầng theo thứ tự chính xác.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng 4 tầng + chỉ ra lệnh <code>ansible --version</code> và bẫy file <code>./ansible.cfg</code> bị bỏ qua nếu lỡ gán quyền <code>world-writable</code> (<code>chmod 777</code>).</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu file <code>./ansible.cfg</code> bị gán quyền <code>chmod 777</code>, Ansible sẽ xử lý thế nào? *(Bỏ qua file đó vì lý do an toàn bảo mật và tự động lùi về dùng file tầng thấp hơn.)*
</div>
</details>

---

### Câu 2 — Xác thực SSH và Cơ chế Agentless 🔥
**Hỏi:** Tại sao Ansible không cần cài agent trên máy đích nhưng vẫn quản trị được? Việc gán `host_key_checking = False` có tác dụng gì? *(Liên quan QT 4.2)*
**Đáp án chuẩn:** Ansible là công cụ agentless, sử dụng giao thức SSH tiêu chuẩn để kết nối và tự động đẩy các module Python ngắn hạn lên máy đích thực thi, sau đó dọn dẹp file tạm. Máy đích chỉ cần dịch vụ `sshd` và môi trường Python 3. Cờ `host_key_checking = False` trong `ansible.cfg` giúp bỏ qua bước xác nhận Fingerprint SSH thủ công (gõ `yes`), giúp các kịch bản tự động hóa hoặc kịch bản thử nghiệm lab chạy mượt mà không bị treo vô hạn.
**Tiêu chí chấm:**
- 0: Trả lời "Ansible dùng agent ngầm".
- 1: Nêu được "dùng SSH" nhưng không giải thích được vai trò của Python trên target.
- 2: Nêu đầy đủ cơ chế SSH + Python + tác dụng của `host_key_checking`.
- 3: Nêu đủ cơ chế + phân tích rủi ro bảo mật của `host_key_checking = False` trên production và cách xử lý bằng `known_hosts`.
**Câu hỏi đào sâu:** Nếu máy đích là hệ điều hành Linux minimal không có sẵn Python 3, lệnh ad-hoc module `ping` có chạy được không? *(Không, phải dùng module `ansible.builtin.raw` để cài Python 3 trước.)*

---

### Câu 3 — Leo quyền quản trị với `become` 🔥
**Hỏi:** Cơ chế `become` trong Ansible hoạt động thế nào? Sự khác biệt giữa SSH user (`remote_user`) và `become_user` là gì? *(Liên quan QT 4.3)*
**Đáp án chuẩn:** Cơ chế `become` cho phép Ansible thực hiện privilege escalation (nâng quyền) trên target node, mặc định sử dụng công cụ `sudo`. `remote_user` là tài khoản dùng để thiết lập kết nối SSH ban đầu từ Control node sang Target node (ví dụ: `ansible`), còn `become_user` là tài khoản mà lệnh đó sẽ leo quyền tới trên máy đích để thực thi tác vụ (mặc định là `root`).
**Tiêu chí chấm:**
- 0: Nhầm lẫn `become` là cài đặt SSH password.
- 1: Biết `become` là `sudo` nhưng không phân biệt được `remote_user` và `become_user`.
- 2: Phân biệt chính xác `remote_user` vs `become_user` và cơ chế `sudo`.
- 3: Nêu đủ + cấu hình tường minh trong `ansible.cfg` (`become=True`, `become_method=sudo`, `become_ask_pass=False`) và điều kiện file `/etc/sudoers`.
**Câu hỏi đào sâu:** Muốn chạy lệnh ad-hoc leo quyền root mà không bị hỏi password sudo thì máy đích cần cấu hình gì trong `/etc/sudoers`? *(Cấu hình `NOPASSWD: ALL` cho user đăng nhập SSH.)*

---

### Câu 4 — Cấu trúc Lệnh Ad-hoc tổng quát
**Hỏi:** Phân tích cú pháp tiêu chuẩn của một lệnh ad-hoc Ansible. Khi nào nên dùng lệnh ad-hoc thay vì viết Playbook? *(Liên quan QT 5.1)*
**Đáp án chuẩn:** Cú pháp tiêu chuẩn: `ansible <pattern> -m <module> -a "<arguments>" [options]`. Lệnh ad-hoc nên được sử dụng cho các công việc quản trị một lần (one-off tasks), nhanh chóng, mang tính kiểm tra/truy vấn (ví dụ: reboot nhóm máy, kiểm tra dung lượng đĩa, cập nhật bản vá khẩn cấp). Khi công việc gồm chuỗi nhiều bước phức tạp có phụ thuộc lẫn nhau, bắt buộc phải dùng Playbook.
**Tiêu chí chấm:**
- 0: Trả lời sai cú pháp cờ lệnh CLI.
- 1: Đọc đúng cú pháp nhưng không nêu được ngữ cảnh sử dụng ad-hoc.
- 2: Đọc đúng cú pháp + so sánh chuẩn ngữ cảnh ad-hoc vs Playbook.
- 3: Nêu đúng cú pháp + đưa ví dụ thực tế cụ thể cho ad-hoc (`ansible all -m package ...`) và giải thích tham số `-a`.
**Câu hỏi đào sâu:** Nếu trong lệnh ad-hoc ta không truyền tham số `-m <module>`, Ansible sẽ sử dụng module mặc định nào? *(Module `ansible.builtin.command`.)*

---

### Câu 5 — So sánh `ping` Ansible vs `ping` ICMP hệ điều hành
**Hỏi:** Module `ansible.builtin.ping` khác gì với câu lệnh `ping` truyền thống của hệ điều hành? *(Liên quan QT 5.2)*
**Đáp án chuẩn:** Lệnh `ping` của hệ điều hành sử dụng giao thức ICMP để kiểm tra thông mạng ở tầng network. Module `ansible.builtin.ping` của Ansible thực hiện một chuỗi thao tác thực tế: mở kết nối SSH, xác thực tài khoản, đẩy một đoạn mã Python nhỏ lên máy đích, thực thi mã Python đó và nhận phản hồi `pong`. Do đó, `ansible ping` thành công chứng minh toàn bộ chuỗi SSH + Python + Quyền thi hành đã sẵn sàng.
**Tiêu chí chấm:**
- 0: Trả lời "hai cái là một".
- 1: Biết `ansible ping` dùng SSH nhưng không giải thích được đoạn mã Python.
- 2: Phân biệt chính xác ICMP network ping vs SSH+Python application ping.
- 3: Phân biệt chính xác + chỉ ra trường hợp `ping` ICMP thông nhưng `ansible ping` hỏng (do sai SSH key hoặc thiếu Python).
**Câu hỏi đào sâu:** Nếu target host chặn hoàn toàn giao thức ICMP, lệnh `ansible all -m ping` có chạy thành công không? *(Vẫn thành công bình thường vì Ansible dùng SSH port 22 chứ không dùng ICMP.)*

---

### Câu 6 — Phân biệt `command`, `shell` và `raw`
**Hỏi:** So sánh bản chất và trường hợp sử dụng của 3 module: `command`, `shell`, và `raw`. *(Liên quan QT 5.3)*
**Đáp án chuẩn:** `command` chạy trực tiếp file thực thi không qua shell (an toàn, không hỗ trợ pipe `|`, redirect `>`). `shell` thực thi câu lệnh thông qua `/bin/sh` trên máy đích (hỗ trợ đầy đủ pipe, redirect, biến môi trường shell). `raw` gửi câu lệnh SSH thô trực tiếp mà không cần sự tồn tại của Python trên máy đích (dùng bootstrap cài Python). Cả 3 module này đều luôn báo `CHANGED` và không idempotent.
**Tiêu chí chấm:**
- 0: Không phân biệt được 3 module.
- 1: Nêu được `shell` hỗ trợ pipe còn `command` thì không.
- 2: Phân biệt chính xác cơ chế của cả 3 module.
- 3: Phân biệt chính xác + giải thích rủi ro bảo mật Shell Injection và lý do tại sao cả 3 đều không đạt Idempotency tự nhiên.
**Câu hỏi đào sâu:** Tại sao Ansible khuyến cáo nên hạn chế tối đa việc dùng `shell` trong tự động hóa? *(Vì `shell` không có tính bất biến, dễ gây tác dụng phụ khi chạy lại và có nguy cơ Shell Injection.)*

---

### Câu 7 — Quản lý Gói phần mềm với `ansible.builtin.package`
**Hỏi:** Tại sao nên dùng module `ansible.builtin.package` thay vì gọi lệnh `apt` hay `dnf` qua ad-hoc shell? *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Module `package` là module trừu tượng hóa (abstraction module). Nó tự động phát hiện trình quản lý gói của hệ điều hành đích (RHEL dùng `dnf`, Ubuntu dùng `apt`). Quan trọng nhất, `package` kiểm tra trạng thái gói trước khi thực hiện. Nếu gói đã được cài đúng `state=present`, module sẽ giữ nguyên và báo `changed=false` (idempotent), trong khi gọi lệnh shell `apt-get install` sẽ luôn làm thay đổi hệ thống và báo `CHANGED`.
**Tiêu chí chấm:**
- 0: Trả lời "dùng cái nào cũng như nhau".
- 1: Nêu được tính đa nền tảng nhưng chưa đề cập tính Idempotency.
- 2: Nêu đủ tính đa nền tảng + kiểm tra trạng thái Idempotency.
- 3: Nêu đủ + minh họa được câu lệnh ad-hoc chuẩn và chỉ số `changed=false` khi chạy lại lần thứ hai.
**Câu hỏi đào sâu:** Tham số `state=latest` khác `state=present` ở điểm nào? *(`present` chỉ cần gói đã cài là dừng, `latest` sẽ nâng cấp gói lên phiên bản mới nhất nếu có.)*

---

### Câu 8 — Quản lý Dịch vụ với `ansible.builtin.service`
**Hỏi:** Khi dùng ad-hoc module `ansible.builtin.service`, làm sao để đảm bảo dịch vụ vừa được khởi chạy vừa tự động bật khi reboot máy? *(Liên quan QT 6.2)*
**Đáp án chuẩn:** Truyền đồng thời hai tham số trong thuộc tính `-a`: `state=started` (để đảm bảo dịch vụ đang chạy ở thời điểm hiện tại) và `enabled=yes` (để cấu hình init system/systemd tự động kích hoạt dịch vụ cùng hệ thống khi khởi động).
**Tiêu chí chấm:**
- 0: Không biết các tham số điều khiển dịch vụ.
- 1: Chỉ nhớ tham số `state=started` mà quên `enabled=yes`.
- 2: Nêu chính xác hai tham số `state=started` và `enabled=yes`.
- 3: Nêu chính xác + minh họa lệnh ad-hoc hoàn chỉnh kèm cờ `--become` và đối soát bằng `docker exec`.
**Câu hỏi đào sâu:** Nếu dịch vụ đã chạy và đã được `enabled=yes`, khi gõ lại lệnh ad-hoc đó Ansible sẽ trả về kết quả gì? *(Trả về `SUCCESS` với chỉ số `changed=false` do đã đạt đúng trạng thái khai báo.)*

---

### Câu 9 — Quản lý Người dùng và Phân quyền tệp tin
**Hỏi:** Làm thế nào để tạo một tài khoản người dùng `appuser` kèm file cấu hình riêng bằng ad-hoc module mà không làm đứt gãy hệ thống khi chạy lại? *(Liên quan QT 6.3)*
**Đáp án chuẩn:** Sử dụng module `ansible.builtin.user` với tham số `name=appuser state=present` để tạo user, sau đó dùng module `ansible.builtin.copy` với `content='...' dest=/etc/app.conf mode='0644'`. Cả hai module này đều tự động kiểm tra dữ liệu cũ trên máy đích, nếu thông tin đã trùng khớp sẽ không tạo lại hay ghi đè lãng phí, đảm bảo tính Idempotency.
**Tiêu chí chấm:**
- 0: Trả lời dùng lệnh `useradd` qua module `shell`.
- 1: Biết tên 2 module `user` và `copy` nhưng thiếu tham số phân quyền `mode`.
- 2: Nêu đúng 2 module và các tham số phân quyền chuẩn.
- 3: Nêu đúng + giải thích cơ chế check md5 hash của module `copy` trước khi chép file.
**Câu hỏi đào sâu:** Nếu file `/etc/app.conf` đã tồn tại trên target node với nội dung giống hệt nội dung ta truyền vào module `copy`, Ansible sẽ làm gì? *(Ansible so sánh hash mã hóa, thấy trùng khớp nên bỏ qua không ghi file và báo `changed=false`.)*

---

### Câu 10 — Phương pháp Xác minh tính Bất biến và Trạng thái Thực tế 🔥
**Hỏi:** Làm sao để chứng minh một tác vụ ad-hoc đạt chuẩn Idempotency và máy đích đang ở đúng trạng thái mong muốn?
**Đáp án chuẩn:** (1) Thực hiện chạy câu lệnh ad-hoc lần thứ nhất để áp đặt thay đổi (`changed=true`). (2) Thực hiện chạy chính xác câu lệnh ad-hoc đó lần thứ hai: nếu kết quả trả về `changed=false` thì tác vụ đạt tính Idempotency. (3) Dùng lệnh kiểm tra độc lập trực tiếp trên máy đích (truy vấn qua SSH hoặc `docker exec target1 systemctl is-active <service>` / `dpkg -l <package>`) để xác minh sự thật khách quan, tuyệt đối không phụ thuộc duy nhất vào báo cáo terminal của Control node.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal thấy báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Trả lời chạy lần 2 có `changed=false` nhưng quên bước kiểm tra trực tiếp trên máy đích.
- 2: Nêu đủ 2 bước: chạy lần 2 `changed=false` + kiểm tra bằng `docker exec`/truy vấn trực tiếp.
- 3: Trả lời xuất sắc cả 3 bước + đưa ví dụ thực tế minh chứng cho từng bước với lệnh CLI cụ thể.
**Câu hỏi đào sâu:** Tại sao báo cáo `SUCCESS` trên Control node đôi khi lại nói dối? *(Do cấu hình giấu lỗi `ignore_errors`, ép trạng thái `changed_when: false`, hoặc chỉ số inventory chỉ định nhầm target node.)*

---

### Câu 11 — Sử dụng cờ Thử nghiệm `--check` và `--diff`
**Hỏi:** Cờ cờ `--check` và `--diff` trong lệnh ad-hoc Ansible có vai trò gì trong quy trình vận hành an toàn trên Production?
**Đáp án chuẩn:** Cờ `--check` kích hoạt chế độ Dry-run (chạy thử nghiệm), Ansible sẽ mô phỏng quá trình thực thi lệnh ad-hoc và dự báo những thay đổi sẽ xảy ra mà không thực sự áp đặt bất kỳ thay đổi nào lên máy đích. Cờ `--diff` hiển thị chi tiết sự khác biệt dòng-theo-dòng (line-by-line diff) giữa cấu hình cũ và cấu hình mới. Kết hợp `--check --diff` giúp quản trị viên rà soát rủi ro trước khi áp dụng thật lên Production.
**Tiêu chí chấm:**
- 0: Không biết công dụng của 2 cờ CLI.
- 1: Biết `--check` là chạy thử nhưng không giải thích được `--diff`.
- 2: Nêu chính xác vai trò Dry-run của `--check` và so sánh cấu hình của `--diff`.
- 3: Nêu chính xác + lưu ý trường hợp một số module custom không hỗ trợ check mode.
**Câu hỏi đào sâu:** Nếu chạy lệnh ad-hoc với cờ `--check` lên một gói phần mềm chưa được cài, Ansible sẽ báo kết quả thế nào? *(Báo `CHANGED` để dự báo rằng gói này SẼ được cài nếu chạy thật, nhưng thực tế đĩa cứng chưa bị ghi dữ liệu.)*

---

### Câu 12 — Quản lý Phạm vi Thực thi với `--limit` ★★★
**Hỏi:** Trong một kịch bản ad-hoc tác động đến hạ tầng hàng ngàn máy chủ, làm thế nào để bó hẹp phạm vi thực thi thử nghiệm trên duy nhất 1 máy chủ trước khi nhân rộng?
**Đáp án chuẩn:** Sử dụng cờ `--limit <host_pattern>` trong câu lệnh ad-hoc (ví dụ: `ansible web --limit target1 -m package -a "name=curl state=present"`). Cờ `--limit` sẽ lọc danh sách máy đích rút gọn từ inventory gốc, đảm bảo lệnh ad-hoc chỉ tác động duy nhất lên `target1`.
**Tiêu chí chấm:**
- 0: Trả lời tạo file inventory mới chứa 1 máy.
- 1: Trớ trêu nhớ cờ `--limit` nhưng dùng sai cú pháp.
- 2: Nêu đúng cờ `--limit` và cú pháp áp dụng trên lệnh CLI ad-hoc.
- 3: Nêu đúng + kết hợp giải thích các pattern lọc nâng cao (ví dụ: `web:!db`, `target1,target2`, `all[0]`).
**Câu hỏi đào sâu:** Pattern `web:!db` trong lệnh ad-hoc Ansible có ý nghĩa gì? *(Thực thi trên tất cả máy thuộc nhóm `web` ngoại trừ các máy đồng thời nằm trong nhóm `db`.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về năng lực vận hành Ansible và lệnh Ad-hoc, học viên hãy tự tin đưa ra câu chốt sau:

> **"Lệnh ad-hoc Ansible là công cụ mạnh mẽ để ứng phó sự cố và quản trị một lần trên quy mô lớn nhờ kiến trúc agentless qua SSH. Tuy nhiên, nguyên tắc vận hành của tôi là luôn ưu tiên các module chuẩn như `package`, `service`, `user` thay vì lạm dụng `command`/`shell` nhằm duy trì tính bất biến (Idempotency). Tôi không bao giờ dừng lại ở thông báo màu xanh trên terminal của Control node, mà luôn chứng minh tính bất biến bằng cách thực thi lần 2 thu được `changed=false` và kiểm tra sự thật thực tế trên máy đích qua truy vấn trực tiếp."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–3 (Tủ) | Câu 4–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Nguyễn Văn A | 3 / 3 / 3 | 2 / 2 / 3 / 2 / 3 / 2 | 3 | 2 / 3 | 28 / 36 | Giỏi |
| Trần Văn B | 2 / 2 / 1 | 2 / 1 / 2 / 2 / 1 / 2 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 03

Để chuẩn bị tốt nhất cho **Buổi 03: Inventory — Static, Group, Host/Group Vars, Pattern**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** File Inventory dạng INI và YAML khác nhau như thế nào về mặt cú pháp? Tại sao dự án lớn ưu tiên dùng YAML?
2. **Nghiên cứu trước 2:** Thư mục `group_vars/` và `host_vars/` đặt ở đâu trong cây thư mục dự án? Ansible tự động nạp biến từ các thư mục này theo cơ chế nào?
3. **Nghiên cứu trước 3:** Lệnh `ansible-inventory --graph` và `ansible <pattern> --list-hosts` giúp ích gì cho quản trị viên trước khi thực thi một Playbook tác động hạ tầng lớn?

---


### [Chuyên Đề 03] Thiết Kế Inventory Chuẩn Enterprise: Static vs Dynamic Inventory, Host Groups, Group Vars & Host Vars

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Inventory trong Ansible có vai trò gì? Hai nhóm mặc định nào luôn tự động tồn tại trong mọi Inventory? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b> Inventory là nguồn chân lý chứa danh sách các máy chủ bị quản lý, thông tin phân nhóm và các biến kết nối tương ứng. Hai nhóm mặc định luôn tồn tại trong mọi Inventory là: (1) <code>all</code> (chứa tất cả các máy chủ có trong inventory) và (2) <code>ungrouped</code> (chứa các máy chủ không thuộc bất kỳ nhóm tùy chỉnh nào).
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không nêu được vai trò của Inventory.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Nêu được vai trò nhưng chỉ nhớ nhóm <code>all</code>, quên nhóm <code>ungrouped</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Nêu chính xác vai trò và 2 nhóm mặc định <code>all</code> và <code>ungrouped</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu chính xác + giải thích ý nghĩa của 2 nhóm mặc định trong việc nạp biến toàn cục (<code>group_vars/all.yml</code>).</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu một máy chủ nằm trong nhóm <code>web</code>, máy chủ đó có đồng thời thuộc nhóm <code>all</code> không? *(Có, 100% mọi host đều thuộc nhóm <code>all</code>.)*
</div>
</details>

---

### Câu 2 — Phân cấp Nhóm cha - Nhóm con (`children`) 🔥
**Hỏi:** Cấu trúc nhóm lồng nhóm (Child groups / Group nesting) được khai báo thế nào trong định dạng INI và YAML? Lợi ích là gì? *(Liên quan QT 4.2)*
**Đáp án chuẩn:** Trong INI, dùng cú pháp `[parent_name:children]` rồi liệt kê danh sách các nhóm con bên dưới. Trong YAML, dùng từ khóa `children:` bên dưới tên nhóm cha. Lợi ích: Cho phép quản lý phân cấp hạ tầng (ví dụ: nhóm cha `vietnam` chứa các nhóm con `hanoi` và `hcm`), giúp áp dụng biến chung hoặc thực thi lệnh trên quy mô vùng miền dễ dàng mà không cần gõ lại tên từng host.
**Tiêu chí chấm:**
- 0: Không biết cú pháp khai báo nhóm cha-con.
- 1: Biết từ khóa `children` nhưng nhầm lẫn giữa INI và YAML.
- 2: Nêu đúng cú pháp cho cả INI và YAML + lợi ích quản lý.
- 3: Nêu đúng + minh họa câu lệnh `ansible-inventory --graph` để kiểm tra cây phân cấp.
**Câu hỏi đào sâu:** Nếu gõ nhầm `[parent_name]` mà quên chữ `:children` trong file INI thì Ansible sẽ hiểu thế nào? *(Ansible hiểu các dòng bên dưới là tên máy chủ tĩnh chứ không phải tên nhóm con.)*

---

### Câu 3 — Cấu trúc Thư mục `group_vars/` và `host_vars/` 🔥
**Hỏi:** Tại sao nên tách biến ra thư mục `group_vars/` và `host_vars/` thay vì viết trực tiếp vào file Inventory tĩnh? *(Liên quan QT 4.3)*
**Đáp án chuẩn:** Việc đặt biến trực tiếp trong file Inventory khiến file phình to, rối mắt và rất khó bảo trì khi hạ tầng tăng trưởng. Tách thành thư mục `group_vars/` (file trùng tên nhóm, ví dụ `web.yml`) và `host_vars/` (file trùng tên host, ví dụ `target1.yml`) giúp chuẩn hóa cấu trúc dự án, dễ đọc, dễ bảo trì và thuận tiện cho việc quản lý mã nguồn qua Git.
**Tiêu chí chấm:**
- 0: Trả lời "viết vào đâu cũng được như nhau".
- 1: Biết tách thư mục là tốt nhưng không nêu được tên các file bên trong.
- 2: Nêu đúng đường dẫn thư mục và quy tắc đặt tên file trùng tên nhóm/host.
- 3: Nêu đúng + giải thích cơ chế Ansible tự động tìm kiếm và nạp các file này theo tên nhóm/host tương ứng.
**Câu hỏi đào sâu:** Nếu thư mục đặt tên là `groups_vars` (thừa chữ s) thì Ansible có nạp biến được không? *(Không, Ansible chỉ tìm đúng tên thư mục chuẩn là `group_vars`.)*

---

### Câu 4 — Thứ tự Ưu tiên Nạp biến trong Inventory và Vars
**Hỏi:** Trình bày quy tắc ưu tiên biến khi một biến `app_port` được định nghĩa ở cả `group_vars/all.yml`, `group_vars/web.yml` và `host_vars/target1.yml`. *(Liên quan QT 5.1)*
**Đáp án chuẩn:** Thứ tự ưu tiên tăng dần từ phạm vi rộng tới hẹp: `group_vars/all.yml` (thấp nhất) < `group_vars/web.yml` (nhóm con) < `host_vars/target1.yml` (cao nhất). Do đó, giá trị `app_port` khai báo tại `host_vars/target1.yml` sẽ chiến thắng và được áp dụng cho `target1`.
**Tiêu chí chấm:**
- 0: Trả lời sai thứ tự ưu tiên.
- 1: Nhớ `host_vars` ưu tiên hơn nhưng nhầm lẫn giữa `all.yml` và `web.yml`.
- 2: Nêu chính xác thứ tự 3 tầng ưu tiên.
- 3: Nêu chính xác + chỉ ra lệnh `ansible-inventory --host target1` để đối soát giá trị biến thực tế cuối cùng.
**Câu hỏi đào sâu:** Làm sao để định nghĩa biến mặc định cho toàn bộ tất cả các host trong hệ thống mà vẫn cho phép từng host override? *(Khai báo biến mặc định trong `group_vars/all.yml` và ghi đè khi cần trong `host_vars/`.)*

---

### Câu 5 — Cú pháp Biểu thức Host Pattern CLI 🔥
**Hỏi:** Phân biệt các toán tử Host Pattern: Dấu phẩy `,`, Dấu và `&`, và Dấu chấm cảm `!`. Cho ví dụ. *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Dấu phẩy `,` (hoặc `:`): Phép HỢP (UNION) — lấy tất cả máy thuộc nhóm 1 HOẶC nhóm 2 (ví dụ: `web,db`).
- Dấu và `&`: Phép GIAO (INTERSECTION) — lấy các máy VỪA thuộc nhóm 1 VỪA thuộc nhóm 2 (ví dụ: `web:&prod`).
- Dấu chấm cảm `!`: Phép LOẠI TRỪ (EXCLUSION) — lấy các máy thuộc nhóm 1 NHƯNG KHÔNG thuộc nhóm 2 (ví dụ: `web:!db`).
**Tiêu chí chấm:**
- 0: Không biết các toán tử pattern.
- 1: Nhớ được các dấu nhưng giải thích nhầm lẫn giữa phép giao và phép hợp.
- 2: Giải thích chính xác 3 phép toán logic + cho ví dụ.
- 3: Giải thích chính xác + cảnh báo lỗi Bash Event Expansion với dấu `!` và giải pháp bọc trong cặp ngoặc đơn `'...'`.
**Câu hỏi đào sâu:** Tại sao gõ `ansible web:!db --list-hosts` trực tiếp trên terminal Bash lại bị báo lỗi `bash: !db: event not found`? *(Do Bash hiểu nhầm dấu `!` là lệnh history expansion, phải bọcpattern trong cặp ngoặc đơn `'web:!db'`.)*

---

### Câu 6 — Kiểm tra và Đối soát Pattern bằng CLI ★★★
**Hỏi:** Hai câu lệnh CLI nào là công cụ quan trọng nhất để rà soát Inventory và Host Pattern trước khi chạy Playbook? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** (1) `ansible-inventory --graph` (hoặc `-i <inventory>`): Dùng để xem sơ đồ cây phân cấp kiểm kê tài nguyên toàn bộ hệ thống. (2) `ansible <pattern> --list-hosts`: Dùng để in ra danh sách tên/IP của các máy đích thực tế sẽ bị tác động bởi biểu thức pattern cụ thể.
**Tiêu chí chấm:**
- 0: Không biết câu lệnh rà soát.
- 1: Nhớ cờ `--list-hosts` nhưng không nhớ `ansible-inventory --graph`.
- 2: Nêu chính xác cả 2 câu lệnh CLI.
- 3: Nêu chính xác + giải thích quy trình an toàn bắt buộc trong vận hành Production (luôn gõ `--list-hosts` trước khi thực thi lệnh tác động).
**Câu hỏi đào sâu:** Nếu cờ `--list-hosts` trả về `hosts (0):`, điều đó có nghĩa là gì? *(Có nghĩa là biểu thức pattern không khớp với bất kỳ máy chủ nào trong inventory.)*

---

### Câu 7 — Các Biến Kết nối Đặc biệt trong Inventory
**Hỏi:** Kể tên 3 biến kết nối hệ thống thường dùng trong Inventory và giải thích công dụng của chúng. *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- `ansible_host`: Địa chỉ IP hoặc FQDN thực tế dùng để kết nối SSH (khi dùng tên alias ngắn trong inventory).
- `ansible_port`: Cổng kết nối SSH thực tế trên máy đích (khi không dùng port 22 mặc định).
- `ansible_user`: Tài khoản người dùng dùng để đăng nhập SSH vào máy đích (ví dụ: `ubuntu`, `ansible`).
- `ansible_ssh_private_key_file`: Đường dẫn tới chìa khóa SSH private key riêng.
**Tiêu chí chấm:**
- 0: Không kể được tên biến kết nối.
- 1: Kể được 1-2 biến nhưng không giải thích rõ công dụng.
- 2: Nêu đúng 3-4 biến kết nối và công dụng chính xác.
- 3: Nêu đúng + đưa ví dụ thực tế cấu hình container Docker SSH (port 2221, 2222).
**Câu hỏi đào sâu:** Nếu máy đích đổi cổng SSH sang 2222, ta cần khai báo biến nào trong inventory? *(Khai báo `ansible_port=2222`.)*

---

### Câu 8 — Quản lý Đa Môi trường Dev/Prod
**Hỏi:** Trình bày phương pháp tổ chức Inventory để quản lý đa môi trường (Development, Staging, Production) mà không cần sửa đổi Playbook. *(Liên quan QT 6.2)*
**Đáp án chuẩn:** Tạo các thư mục hoặc file inventory riêng biệt cho từng môi trường (ví dụ: `inventory/dev` và `inventory/prod`). Trong mỗi môi trường khai báo danh sách IP và `group_vars` riêng. Playbook giữ nguyên 100% mã nguồn xử lý. Khi thực thi, chỉ cần chỉ định cờ `-i` tương ứng: `ansible-playbook -i inventory/dev site.yml` hoặc `-i inventory/prod site.yml`.
**Tiêu chí chấm:**
- 0: Trả lời phải sửa IP trực tiếp trong Playbook.
- 1: Biết tách file inventory nhưng không giải thích được cơ chế cờ `-i`.
- 2: Nêu đúng phương pháp tách thư mục inventory + cờ CLI `-i`.
- 3: Nêu đúng + phân tích lợi ích an toàn (tránh vỡ môi trường Prod khi test ở Dev) và tích hợp vào CI/CD pipeline.
**Câu hỏi đào sâu:** Có nên để chung máy Dev và máy Prod trong cùng 1 file inventory tĩnh không? Tại sao? *(Không nên, vì rất dễ gõ nhầm pattern làm tác động lệnh thử nghiệm lên nhầm máy Production.)*

---

### Câu 9 — An toàn Bảo mật Biến trong Inventory
**Hỏi:** Nguyên tắc an toàn bảo mật đối với các biến nhạy cảm (mật khẩu, token) trong Inventory là gì? *(Liên quan QT 6.3)*
**Đáp án chuẩn:** Tuyệt đối không bao giờ lưu trữ mật khẩu, token hay chìa khóa bí mật dạng plain-text trong file Inventory hay thư mục `group_vars/host_vars` rồi commit lên Git. Giải pháp chuẩn: Chuyển sang dùng xác thực SSH Key không mật khẩu, hoặc sử dụng công cụ mã hóa **Ansible Vault** để mã hóa file chứa biến nhạy cảm trước khi lưu trữ.
**Tiêu chí chấm:**
- 0: Cho rằng ghi mật khẩu vào `group_vars` là bình thường.
- 1: Biết rủi ro lộ mật khẩu nhưng không nêu được giải pháp Ansible Vault.
- 2: Nêu đúng nguyên tắc an toàn + giải pháp SSH Key / Ansible Vault.
- 3: Nêu đúng + minh họa câu lệnh mã hóa `ansible-vault encrypt` và quản lý Vault ID.
**Câu hỏi đào sâu:** Nếu vô tình commit file inventory chứa mật khẩu thô lên GitHub public, cách xử lý khẩn cấp là gì? *(Đổi mật khẩu tài khoản lập tức trên hệ thống thật, xóa commit history chứa secret.)*

---

### Câu 10 — Phương pháp Xác minh tính Bất biến và Trạng thái Máy đích 🔥
**Hỏi:** Trình bày quy trình 3 bước để đảm bảo một lệnh tác động dựa trên Inventory vừa Idempotent vừa chính xác trên máy đích.
**Đáp án chuẩn:** 
1. **Bước 1 (Rà soát):** Chạy `ansible <pattern> --list-hosts` để chắc chắn 100% lệnh chỉ tác động đúng các host mong muốn.
2. **Bước 2 (Kiểm Idempotency):** Thực thi lệnh lần 1 (`changed=true`), sau đó thực thi lại chính xác lệnh đó lần 2: phải thu được `changed=false` (màu xanh lá cây).
3. **Bước 3 (Đối soát sự thật):** Dùng `docker exec <target> cat /etc/app_env.conf` hoặc SSH trực tiếp vào máy đích kiểm tra tệp tin/dịch vụ thật, không phụ thuộc duy nhất vào màn hình Control node.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal thấy OK là xong" (trần điểm 1).
- 1: Thiếu bước rà soát `--list-hosts` hoặc bước đối soát `docker exec`.
- 2: Trình bày đủ 3 bước nhưng chưa nêu lệnh CLI minh họa.
- 3: Trình bày xuất sắc cả 3 bước + lệnh CLI cụ thể và giải thích tầm quan trọng của từng bước.
**Câu hỏi đào sâu:** Nếu lệnh chạy lần 2 vẫn báo `CHANGED`, điều đó chứng tỏ điều gì? *(Tác vụ không đạt tính Idempotency, có thể do lạm dụng module shell hoặc nội dung thay đổi liên tục.)*

---

### Câu 11 — Sử dụng Ký tự Đại diện Wildcard trong Pattern
**Hỏi:** Khi nào nên dùng ký tự đại diện Wildcard `*` trong Host Pattern? Cần lưu ý gì khi sử dụng?
**Đáp án chuẩn:** Dùng wildcard `*` khi muốn chọn một tập hợp host có quy tắc đặt tên đồng nhất (ví dụ: `web*` chọn `web1`, `web2`, `web-prod-01`; `*.example.com` chọn tất cả host thuộc domain). Lưu ý: Phải dùng `--list-hosts` kiểm tra trước để tránh trường hợp wildcard chọn nhầm các host có tên tương tự không mong muốn (ví dụ `web*` có thể dính cả `web-deprecated`).
**Tiêu chí chấm:**
- 0: Không biết ký tự wildcard.
- 1: Biết `*` đại diện cho chuỗi ký tự nhưng không nêu được rủi ro.
- 2: Nêu chính xác cú pháp wildcard + các trường hợp sử dụng phổ biến.
- 3: Nêu đúng + lưu ý an toàn rà soát bằng `--list-hosts` trước khi chạy lệnh thật.
**Câu hỏi đào sâu:** Pattern `'192.168.1.*'` có hợp lệ không? *(Hợp lệ, chọn tất cả các host có IP thuộc dải subnet 192.168.1.0/24 trong inventory.)*

---

### Câu 12 — Quản lý Inventory Quy mô lớn với Dynamic Inventory ★★★
**Hỏi:** Khi hạ tầng mở rộng lên hàng ngàn máy chủ Cloud (AWS/GCP) tự động co giãn, hạn chế lớn nhất của Static Inventory là gì? Giải pháp thay thế ở các buổi sau là gì?
**Đáp án chuẩn:** Hạn chế của Static Inventory ghi tay: Không phản ánh kịp thời sự thay đổi của hạ tầng Cloud (các máy chủ mới tạo hoặc bị xoá bỏ tự động theo lưu lượng), gây ra tình trạng file tĩnh bị lạc hậu, kết nối SSH thất bại tới các máy đã xóa hoặc bỏ sót máy mới. Giải pháp: Chuyển sang sử dụng **Dynamic Inventory Plugin** (sẽ học ở Buổi 24), tự động gọi API của Cloud Provider để sinh danh sách host thời gian thực.
**Tiêu chí chấm:**
- 0: Không biết hạn chế của Static Inventory trên Cloud.
- 1: Nêu được hạn chế ghi tay vất vả nhưng không biết giải pháp Dynamic Inventory.
- 2: Phân tích chính xác hạn chế với hạ tầng Auto Scaling + giải pháp Dynamic Inventory Plugin.
- 3: Phân tích xuất sắc + so sánh ưu/nhược điểm giữa Static và Dynamic Inventory trong thực tế DevOps.
**Câu hỏi đào sâu:** Với dự án nhỏ 3-5 máy chủ tĩnh cố định, có cần thiết phải dùng Dynamic Inventory không? *(Không cần, static inventory ghi tay đơn giản và nhanh hơn cho dự án cố định.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm quản lý Inventory và cấu hình Ansible, học viên hãy sử dụng câu chốt tự tin sau:

> **"Tôi coi Inventory là nguồn chân lý điều khiển toàn bộ hệ thống Ansible. Trong thực tế, tôi luôn tổ chức Inventory chuẩn hóa với phân cấp nhóm rõ ràng và tách biệt cấu hình biến ra các thư mục `group_vars/` và `host_vars/` nhằm tuân thủ nghiêm ngặt quy luật ưu tiên biến. Trước mọi lần thực thi tác vụ, nguyên tắc an toàn hàng đầu của tôi là luôn kiểm tra danh sách máy đích bằng `ansible <pattern> --list-hosts` để ngăn chặn rủi ro tác động nhầm máy chủ. Đồng thời, tôi luôn chứng minh tính bất biến bằng cách thực thi lần 2 thu được `changed=false` và kiểm tra sự thật thực tế trên máy đích qua `docker exec` hoặc SSH độc lập."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–3 (Tủ) | Câu 4–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Nguyễn Văn C | 3 / 3 / 3 | 3 / 3 / 2 / 3 / 2 / 3 | 3 | 3 / 2 | 31 / 36 | Xuất sắc |
| Lê Thị D | 2 / 2 / 1 | 2 / 1 / 2 / 2 / 1 / 2 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 04

Để chuẩn bị tốt nhất cho **Buổi 04: Module Cơ bản và Lệnh Ad-hoc**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Các module cốt lõi `ansible.builtin.copy`, `ansible.builtin.file`, `ansible.builtin.lineinfile` khác nhau thế nào khi quản lý tệp tin trên máy đích?
2. **Nghiên cứu trước 2:** Module `ansible.builtin.cron` giúp quản trị viên tạo và quản lý các tác vụ định kỳ trên Linux như thế nào?
3. **Nghiên cứu trước 3:** Làm thế nào để sử dụng module `ansible.builtin.stat` kiểm tra sự tồn tại của một file trước khi quyết định thực thi các bước tiếp theo?

---


### [Chuyên Đề 04] Làm Chủ Các Modules Cốt Lõi: File, Copy, Template, Package, Service, Command vs Shell vs Raw

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Module <code>ansible.builtin.package</code> có ưu điểm gì vượt trội so với các module quản lý gói riêng biệt như <code>apt</code> hay <code>dnf</code>? Phân biệt <code>state=present</code> và <code>state=latest</code>. *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b> Module <code>package</code> là module trừu tượng hóa (generic package manager), tự động nhận diện hệ điều hành của máy đích (RHEL dùng <code>dnf</code>, Ubuntu dùng <code>apt</code>, Alpine dùng <code>apk</code>), giúp viết kịch bản dùng chung cho hạ tầng đa OS. <code>state=present</code> đảm bảo gói đã cài đặt (nếu đã có gói thì bỏ qua không làm gì), còn <code>state=latest</code> kiểm tra và nâng cấp gói lên phiên bản mới nhất nếu kho phần mềm có bản mới.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết tác dụng của module <code>package</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết tự đổi trình quản lý gói nhưng không phân biệt được <code>present</code> và <code>latest</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân biệt chính xác cơ chế đa nền tảng + khác biệt <code>present</code> vs <code>latest</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa câu lệnh ad-hoc cài gói và chỉ ra tính Idempotency lần 2.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Khi nào nên dùng module chuyên biệt <code>ansible.builtin.apt</code> thay vì <code>package</code>? *(Khi cần các tính năng đặc thụ riêng của Debian/Ubuntu như <code>update_cache=yes</code> hay <code>autoremove=yes</code>.)*
</div>
</details>

---

### Câu 2 — Điều khiển Dịch vụ với `ansible.builtin.service` 🔥
**Hỏi:** Phân biệt ý nghĩa của hai tham số `state=started` và `enabled=yes` trong module `ansible.builtin.service`. Khi nào dùng `state=reloaded`? *(Liên quan QT 4.2)*
**Đáp án chuẩn:** `state=started` kiểm tra và đảm bảo dịch vụ đang ở trạng thái hoạt động (active/running) ở thời điểm hiện tại. `enabled=yes` cấu hình init system (systemd) để dịch vụ tự động khởi động cùng hệ thống khi reboot. `state=reloaded` gửi tín hiệu reload cấu hình daemon (như Nginx/Apache) mà không ngắt các kết nối mạng hiện tại của người dùng, khác với `state=restarted` ngắt và chạy lại hoàn toàn.
**Tiêu chí chấm:**
- 0: Nhầm lẫn giữa `started` và `enabled`.
- 1: Giải thích được `started` và `enabled` nhưng không biết `reloaded`.
- 2: Phân biệt chính xác cả 3 thuộc tính `started`, `enabled`, `reloaded`.
- 3: Nêu chính xác + minh họa lệnh ad-hoc kiểm tra dịch vụ `sshd` và đối soát bằng `docker exec`.
**Câu hỏi đào sâu:** Nếu dịch vụ đã chạy và đã được `enabled=yes`, gõ lại lệnh ad-hoc `service` cũ Ansible sẽ báo gì? *(Báo `SUCCESS` với `changed=false` do đã đạt trạng thái mong muốn.)*

---

### Câu 3 — Quản lý Thư mục và Phân quyền với `ansible.builtin.file` 🔥
**Hỏi:** Module `ansible.builtin.file` thực hiện những loại thao tác nào trên tệp tin? Ý nghĩa của các tham số `mode`, `owner`, `group`? *(Liên quan QT 4.3)*
**Đáp án chuẩn:** Module `file` dùng để: (1) Tạo thư mục (`state=directory`), (2) Xóa tài nguyên an toàn (`state=absent`), (3) Tạo file rỗng/touch (`state=touch`), (4) Tạo liên kết mềm symlink (`state=link`). Các tham số `mode` gán phân quyền bát phân Linux (ví dụ `'0755'`, `'0644'`), `owner` gán chủ sở hữu tệp, `group` gán nhóm sở hữu tệp.
**Tiêu chí chấm:**
- 0: Trả lời dùng module `file` để ghi nội dung văn bản vào file.
- 1: Liệt kê được tạo thư mục nhưng không nêu được các `state` khác.
- 2: Nêu đúng 4 dạng `state` chính và các tham số phân quyền.
- 3: Nêu đúng + giải thích tại sao tham số `mode` nên bọc trong cặp ngoặc đơn `'0755'` để tránh lỗi parse số bát phân trong YAML/CLI.
**Câu hỏi đào sâu:** Muốn xóa hoàn toàn thư mục `/tmp/old_app` kèm tất cả file con bên trong qua ad-hoc, dùng lệnh gì? *(`ansible all -m file -a "path=/tmp/old_app state=absent" --become`)*

---

### Câu 4 — Sao chép Tệp tin và Cơ chế Sao lưu với `ansible.builtin.copy`
**Hỏi:** Module `ansible.builtin.copy` kiểm tra tính Idempotency bằng cơ chế nào? Tác dụng của tham số `backup=yes`? *(Liên quan QT 5.1)*
**Đáp án chuẩn:** Module `copy` tính toán md5/sha256 checksum của file nguồn local và file đích trên target host. Nếu checksum trùng khớp 100%, Ansible bỏ qua không chép đè và báo `changed=false`. Nếu checksum khác nhau và có truyền `backup=yes`, Ansible tự động tạo ra một bản sao lưu của file đích cũ (kèm mốc thời gian timestamp) trước khi chép file mới đè lên.
**Tiêu chí chấm:**
- 0: Trả lời `copy` luôn ghi đè file mỗi lần chạy.
- 1: Biết `copy` so sánh nội dung nhưng không biết cơ chế md5 checksum.
- 2: Nêu chính xác cơ chế md5 checksum + tác dụng tạo file timestamp của `backup=yes`.
- 3: Nêu đúng + minh họa câu lệnh ad-hoc `copy` kèm tham số `mode='0644'` và `backup=yes`.
**Câu hỏi đào sâu:** Nếu file nguồn local bị thay đổi 1 ký tự, chỉ số `changed` lần chạy tiếp theo sẽ là bao nhiêu? *(Chỉ số sẽ báo `changed=true` vì checksum bị thay đổi.)*

---

### Câu 5 — Chỉnh sửa Dòng Cấu hình với `ansible.builtin.lineinfile` 🔥
**Hỏi:** Module `ansible.builtin.lineinfile` giải quyết bài toán gì trong sửa file cấu hình? Vai trò của tham số `regexp`? *(Liên quan QT 5.2)*
**Đáp án chuẩn:** `lineinfile` dùng để đảm bảo MỘT DÒNG CẤU HÌNH cụ thể tồn tại hoặc bị sửa đổi trong file cấu hình dạng Key-Value (như `sshd_config`, `sysctl.conf`). Tham số `regexp` chứa biểu thức chính quy để tìm kiếm dòng cũ. Nếu tìm thấy dòng khớp regex, Ansible sửa dòng đó thành giá trị trong tham số `line`. Nếu không tìm thấy, Ansible chèn dòng mới vào cuối file, đảm bảo dòng đó chỉ xuất hiện DUY NHẤT 1 lần.
**Tiêu chí chấm:**
- 0: Nhầm lẫn `lineinfile` với việc ghi đè toàn bộ file.
- 1: Nêu được sửa dòng nhưng không giải thích được vai trò của `regexp`.
- 2: Phân tích chính xác vai trò của `regexp` và `line`.
- 3: Nêu đúng + so sánh sự khác biệt Idempotent của `lineinfile` so với việc dùng `echo >> file` bằng module `shell`.
**Câu hỏi đào sâu:** Nếu không truyền tham số `regexp` mà chỉ truyền `line='Port 2222'`, điều gì sẽ xảy ra khi chạy lệnh ad-hoc đó 2 lần? *(Nếu dòng `Port 2222` đã có trong file thì lần 2 báo `changed=false`; nếu dòng cũ là `Port 22` mà không có regex thì nó sẽ chèn thêm dòng `Port 2222` xuống bên dưới.)*

---

### Câu 6 — Chèn Khối Văn bản với `ansible.builtin.blockinfile`
**Hỏi:** Module `ansible.builtin.blockinfile` khác `lineinfile` ở điểm nào? Thẻ Marker tag có vai trò gì? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** `lineinfile` quản lý từng DÒNG đơn lẻ, còn `blockinfile` quản lý MỘT KHỐI NHIỀU DÒNG văn bản (multi-line block). Thẻ Marker tag (mặc định `# BEGIN ANSIBLE MANAGED BLOCK` và `# END ANSIBLE MANAGED BLOCK`) được Ansible chèn vào đầu và cuối khối văn bản để nhận diện chính xác vùng quản lý của Ansible. Nhờ có Marker tag, Ansible có thể cập nhật hoặc xóa toàn bộ khối văn bản đó ở các lần chạy sau mà không ảnh hưởng đến các phần khác của file.
**Tiêu chí chấm:**
- 0: Không phân biệt được `lineinfile` và `blockinfile`.
- 1: Biết `blockinfile` chèn nhiều dòng nhưng không giải thích được Marker tag.
- 2: Nêu đúng sự khác biệt + vai trò của Marker tag.
- 3: Nêu đúng + minh họa tham số `marker="# {mark} ANSIBLE MANAGED BLOCK"` tùy chỉnh.
**Câu hỏi đào sâu:** Làm sao để xóa hoàn toàn khối văn bản đã chèn bởi `blockinfile`? *(Truyền tham số `state=absent` kèm đúng thẻ marker cũ.)*

---

### Câu 7 — Quản lý Tài khoản và Nhóm với `user` và `group`
**Hỏi:** Trình bày các tham số quan trọng khi tạo một tài khoản người dùng hệ thống bằng module `ansible.builtin.user`. *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Các tham số cốt lõi: `name` (tên tài khoản), `state=present/absent` (tạo hoặc xóa user), `uid` (chỉ định UID cụ thể), `group` (nhóm chính của user), `groups` (danh sách các nhóm phụ), `append=yes` (thêm nhóm phụ không làm mất nhóm cũ), `shell` (đường dẫn shell mặc định như `/bin/bash`), và `create_home=yes` (tạo thư mục `/home/username`).
**Tiêu chí chấm:**
- 0: Không biết các tham số tạo user.
- 1: Kể được `name` và `state` nhưng thiếu `shell` và `group`.
- 2: Nêu đúng 5-6 tham số cốt lõi.
- 3: Nêu đúng + giải thích tầm quan trọng của tham số `append=yes` khi gán nhóm phụ.
**Câu hỏi đào sâu:** Nếu gán `state=absent` cho module `user`, thư mục `/home/username` có bị xóa không? *(Mặc định không xóa, muốn xóa thư mục home phải truyền thêm `remove=yes`.)*

---

### Câu 8 — Quản lý Tác vụ Định kỳ với `ansible.builtin.cron`
**Hỏi:** Tại sao thuộc tính `name` lại là tham số bắt buộc phải có khi sử dụng module `ansible.builtin.cron`? *(Liên quan QT 6.2)*
**Đáp án chuẩn:** Thuộc tính `name` đóng vai trò là nhãn định danh duy nhất (unique key identifier) cho một tác vụ cron trong file crontab của Linux. Ansible chèn một dòng comment `# Ansibled: <name>` trước dòng lệnh cron. Nhờ nhãn tên này, ở các lần chạy sau Ansible biết được job đã tồn tại để cập nhật hoặc sửa đổi thời gian thực thi, thay vì chèn trùng lặp nhiều dòng cron rác vào crontab.
**Tiêu chí chấm:**
- 0: Không biết vai trò của `name` trong `cron`.
- 1: Biết `name` là tên job nhưng không giải thích được cơ chế nhãn định danh trong crontab.
- 2: Nêu chính xác vai trò nhãn định danh chống trùng lặp job.
- 3: Nêu chính xác + minh họa lệnh ad-hoc tạo cron job và xóa cron job bằng `state=absent`.
**Câu hỏi đào sâu:** Viết cú pháp tham số `-a` cho module `cron` để tạo job chạy mỗi 15 phút một lần. *(`minute='*/15' hour='*' job='/path/to/script.sh' name='Quarterly Check'`)*

---

### Câu 9 — Truy vấn thuộc tính Tệp tin với `ansible.builtin.stat`
**Hỏi:** Module `ansible.builtin.stat` trả về những thông tin gì? Tại sao module này không làm thay đổi hệ thống? *(Liên quan QT 6.3)*
**Đáp án chuẩn:** Module `stat` là module chỉ đọc (read-only query module). Nó thực hiện lệnh truy vấn kernel để lấy thông tin trạng thái tệp tin/thư mục bao gồm: `stat.exists` (file có tồn tại không), `stat.isreg` (có phải file thường không), `stat.isdir` (có phải thư mục không), `stat.mode` (quyền phân quyền), `stat.size` (dung lượng byte), `stat.checksum` (mã hash md5/sha256). Do chỉ đọc dữ liệu, `stat` luôn trả về `changed=false` và không tác động làm sửa đổi hệ thống.
**Tiêu chí chấm:**
- 0: Nhầm `stat` với module chỉnh sửa file.
- 1: Nêu được `stat` kiểm tra file tồn tại nhưng không kể được các thuộc tính trả về.
- 2: Nêu đúng bản chất read-only + các thuộc tính JSON chính trả về.
- 3: Nêu đúng + giải thích ứng dụng của `stat` làm điều kiện rẽ nhánh logic cho các bước sau.
**Câu hỏi đào sâu:** Thuộc tính nào của `stat` dùng để biết một đường dẫn là liên kết mềm Symlink? *(`stat.islnk` trả về `true`.)*

---

### Câu 10 — Phương pháp Xác minh tính Bất biến và Trạng thái Thực tế 🔥
**Hỏi:** Làm sao để chứng minh bộ 9 module tiêu chuẩn (`package`, `service`, `file`, `copy`, `lineinfile`, `blockinfile`, `user`, `cron`, `stat`) đạt Idempotency và máy đích đúng trạng thái?
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi lần 1):** Chạy lệnh ad-hoc gọi module chuẩn áp đặt cấu hình (`changed=true`).
2. **Bước 2 (Kiểm Idempotency lần 2):** Chạy lại nguyên vẹn lệnh ad-hoc đó lần thứ hai: kết quả **bắt buộc** trả về `changed=false` (màu xanh lá cây).
3. **Bước 3 (Đối soát sự thật):** Dùng `docker exec <target> ...` (truy vấn `systemctl is-active`, `crontab -l`, `id <user>`, `cat <file>`) để kiểm tra hiện vật thật trên đĩa cứng máy đích, tuyệt đối không phụ thuộc duy nhất vào màn hình Control node.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal lần 1 thấy OK là xong" (dính bẫy trần điểm 1).
- 1: Nêu được chạy lần 2 `changed=false` nhưng quên bước `docker exec` đối soát máy đích.
- 2: Nêu đủ 3 bước nhưng chưa đưa câu lệnh CLI minh họa.
- 3: Trình bày xuất sắc 3 bước + cho ví dụ thực tế minh chứng với lệnh CLI và câu lệnh `docker exec`.
**Câu hỏi đào sâu:** Tại sao dùng module `command` gõ `useradd deployer` lần 2 lại bị đỏ FAILED, còn module `user` gõ lần 2 lại báo xanh `changed=false`? *(Vì `command` chạy mù không kiểm tra `/etc/passwd`, còn module `user` kiểm tra thấy user đã có đúng thông tin nên dừng lạiIdempotent.)*

---

### Câu 11 — Sử dụng Cờ Backup an toàn trong Module Thao tác File ★★★
**Hỏi:** Khi chỉnh sửa file cấu hình hạ tầng sản xuất bằng module `copy`, `lineinfile` hay `blockinfile`, cờ `backup=yes` giúp quản trị viên ứng phó sự cố như thế nào?
**Đáp án chuẩn:** Khi truyền `backup=yes`, trước khi thực hiện bất kỳ sửa đổi hay ghi đè nào lên file đích, Ansible tự động tạo ra một file bản sao lưu khẩn cấp tại cùng thư mục máy đích kèm chuỗi timestamp (ví dụ `/etc/nginx/nginx.conf.1234.2026-08-22@15:45~`). Nếu cấu hình mới làm ngắt kết nối dịch vụ, quản trị viên có thể ngay lập tức khôi phục file gốc từ bản backup này chỉ trong vài giây.
**Tiêu chí chấm:**
- 0: Không biết tác dụng của `backup=yes`.
- 1: Biết tạo file backup nhưng không giải thích được mốc thời gian timestamp.
- 2: Nêu chính xác cơ chế tạo file timestamp sao lưu khẩn cấp.
- 3: Nêu chính xác + chỉ ra cách kết hợp với cờ `--check --diff` để tối ưu quy trình vận hành an toàn.
**Câu hỏi đào sâu:** File backup tạo bởi Ansible được lưu ở đâu? *(Mặc định lưu ngay tại cùng thư mục chứa file đích trên máy target node, trừ khi khai báo `backup_file` riêng.)*

---

### Câu 12 — Phân biệt Module Tiêu chuẩn vs Custom Script ★★★
**Hỏi:** So sánh sự khác biệt về mặt Vận hành, Bảo trì và Idempotency giữa việc dùng Module tiêu chuẩn (`ansible.builtin.*`) và việc chạy Custom Shell Script trên 100 máy chủ.
**Đáp án chuẩn:**
- **Module tiêu chuẩn:** Viết bằng Python đã được cộng đồng Red Hat kiểm thử kỹ lưỡng, tự động quản lý lỗi, có sẵn tính năng Idempotency (chạy lần 2 `changed=false`), hiển thị `diff` dòng thay đổi, hỗ trợ Dry-run `--check`.
- **Custom Shell Script:** Phụ thuộc vào kỹ năng viết Bash của từng cá nhân, thường không có tính Idempotency (chạy lại dễ gây đè đúp hoặc lỗi), khó bảo trì, không hỗ trợ `--check` hay `--diff`, dễ đứt gãy giữa chừng không kiểm soát.
**Tiêu chí chấm:**
- 0: Cho rằng viết Shell script tốt hơn dùng module chuẩn.
- 1: Nêu được module chuẩn dễ dùng hơn nhưng không phân tích được khía cạnh vận hành và Idempotency.
- 2: So sánh chính xác trên 3 khía cạnh: Vận hành, Bảo trì, Idempotency.
- 3: Phân tích xuất sắc + kết luận tư duy DevOps chuẩn: Luôn ưu tiên 100% module tiêu chuẩn cho các tác vụ quản trị hệ thống phổ biến.
**Câu hỏi đào sâu:** Khi nào buộc phải dùng shell script thay vì module chuẩn? *(Chỉ khi tác vụ quá đặc thù của doanh nghiệp mà Ansible Collection chưa hỗ trợ module chuyên dụng.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kỹ năng sử dụng các module Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tư duy quản trị Ansible của tôi là luôn ưu tiên 100% các module chuyên dụng trong collection `ansible.builtin` như `package`, `service`, `file`, `copy`, `lineinfile`, `blockinfile`, `user`, `cron`, `stat` thay vì lạm dụng các lệnh shell thô. Các module chuẩn tự động kiểm tra trạng thái hiện tại của hệ thống để đảm bảo tính bất biến (Idempotency). Tôi luôn thiết lập cờ `backup=yes` khi chỉnh sửa file cấu hình quan trọng, rà soát cờ `--check --diff` trước khi bấm Enter, chứng minh chỉ số `changed=false` ở lần chạy thứ hai và luôn đối soát sự thật thực tế trên máy đích qua `docker exec` hoặc SSH độc lập."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–3 (Tủ) | Câu 4–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Hoàng Văn E | 3 / 3 / 3 | 3 / 3 / 3 / 3 / 2 / 3 | 3 | 3 / 3 | 33 / 36 | Xuất sắc |
| Đỗ Thị F | 2 / 2 / 1 | 2 / 1 / 2 / 2 / 1 / 2 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 05

Để chuẩn bị tốt nhất cho **Buổi 05: Playbook đầu tiên — Play, Task, PLAY RECAP**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Cấu trúc cú pháp tiêu chuẩn của một file Playbook YAML gồm những phần tử cơ bản nào (`name`, `hosts`, `become`, `tasks`)?
2. **Nghiên cứu trước 2:** Mỗi Task trong Playbook liên hệ thế nào với các module ad-hoc ta đã học ở Buổi 04?
3. **Nghiên cứu trước 3:** Ý nghĩa của các thông số `ok`, `changed`, `unreachable`, `failed` trong bảng tổng kết `PLAY RECAP` ở cuối lượt chạy Playbook?

---


### [Chuyên Đề 05] Xây Dựng Playbook Đầu Tiên: Cấu Trúc YAML, Plays, Tasks, Become Privilege Escalation & Đọc PLAY RECAP

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Trình bày cấu trúc cú pháp tiêu chuẩn của một file Playbook Ansible YAML. Ký tự nào bắt buộc nằm ở đầu file? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b> Một file Playbook bắt đầu bằng dòng đánh dấu tài liệu <code>---</code> (ba dấu gạch ngang). File chứa một danh sách các Play (bắt đầu bằng dấu gạch ngang <code>-</code>). Trong mỗi Play khai báo các phần tử cốt lõi: <code>name:</code> (tên Play), <code>hosts:</code> (nhóm máy đích), <code>become: true</code> (quyền root), <code>vars:</code> (biến Play) và <code>tasks:</code> (danh sách các nhiệm vụ đơn lẻ bên dưới).
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không nêu được cấu trúc Playbook.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Liệt kê được các phần tử nhưng quên ký tự <code>---</code> hoặc nhầm lẫn cú pháp YAML.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Nêu đầy đủ các phần tử cốt lõi của Playbook YAML.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + giải thích quy tắc dùng 2 dấu cách thay cho phím Tab trong định dạng YAML.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Tại sao phím Tab bị cấm tuyệt đối khi viết Playbook YAML? *(Vì trình biên dịch YAML dùng số lượng dấu cách để phân định cấp độ cấu trúc dữ liệu; dùng Tab sẽ gây lỗi parse syntax ngay lập tức.)*
</div>
</details>

---

### Câu 2 — Phân biệt Play và Task 🔥
**Hỏi:** Phân biệt mối quan hệ và vai trò giữa **Play** và **Task** trong Ansible Playbook. Mỗi Task được chứa tối đa bao nhiêu module? *(Liên quan QT 4.2)*
**Đáp án chuẩn:** **Play** đóng vai trò là khung chứa nối tập hợp máy đích (`hosts`) và quyền thực thi với các nhiệm vụ. **Task** là một bước hành động cụ thể nằm trong Play. Mỗi Task chỉ được chứa **đúng duy nhất 1 module** để đảm bảo tính độc lập và khả năng kiểm soát lỗi. Một Play có thể chứa nhiều Task chạy nối tiếp từ trên xuống dưới.
**Tiêu chí chấm:**
- 0: Nhầm lẫn giữa Play và Task.
- 1: Biết Play chứa Task nhưng cho rằng 1 Task có thể gọi nhiều module.
- 2: Nêu chính xác sự khác biệt giữa Play và Task + quy tắc 1 module/task.
- 3: Nêu chính xác + giải thích rủi ro nếu định nghĩa trùng tên Task trong cùng một Play.
**Câu hỏi đào sâu:** Điều gì xảy ra nếu ta khai báo cả `package:` và `service:` bên dưới cùng một `- name:` trong 1 Task? *(Ansible sẽ báo lỗi `conflicting action statements` và dừng thi hành.)*

---

### Câu 3 — Ý nghĩa Thuộc tính `name:` ở Play và Task 🔥
**Hỏi:** Tại sao việc khai báo thuộc tính `name:` ở từng Play và từng Task lại là quy định bắt buộc trong quản trị hạ tầng? *(Liên quan QT 4.3)*
**Đáp án chuẩn:** Thuộc tính `name:` cung cấp chuỗi văn bản mô tả mục đích hành động của Play/Task. Khi Playbook thực thi, Ansible in chuỗi `name:` này ra terminal giúp quản trị viên và các hệ thống CI/CD đọc hiểu ngay tiến trình đang làm gì. Việc thiếu `name:` khiến log hiển thị các tên module mặc định chung chung vô nghĩa, gây rất nhiều khó khăn khi debug lỗi.
**Tiêu chí chấm:**
- 0: Cho rằng thuộc tính `name:` là không cần thiết.
- 1: Biết `name` để đặt tên nhưng không nêu được vai trò trong logging/CI-CD.
- 2: Nêu chính xác vai trò mô tả tiến trình và hỗ trợ gỡ lỗi.
- 3: Nêu đúng + minh họa sự khác biệt giao diện hiển thị log có `name` và không có `name`.
**Câu hỏi đào sâu:** Nếu chuỗi văn bản trong `name:` có chứa dấu hai chấm (ví dụ `name: Task 1: Install Nginx`), ta phải xử lý thế nào để tránh lỗi cú pháp YAML? *(Bắt buộc bọc toàn bộ chuỗi văn bản trong cặp dấu ngoặc kép `"..."`.)*

---

### Câu 4 — Đọc hiểu các Chỉ số trong `PLAY RECAP` 🔥
**Hỏi:** Phân tích chi tiết ý nghĩa của 4 chỉ số quan trọng nhất trong bảng `PLAY RECAP`: `ok`, `changed`, `unreachable`, `failed`. *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- `ok`: Số Task thực thi thành công nhưng KHÔNG tạo ra thay đổi mới (do hệ thống đã đúng trạng thái).
- `changed`: Số Task thực thi thành công VÀ tạo ra thay đổi thực tế trên máy đích.
- `unreachable`: Số máy đích bị lỗi kết nối SSH (không thể chạm tới máy).
- `failed`: Số Task gặp lỗi thực thi ngắt kịch bản trên máy đích.
**Tiêu chí chấm:**
- 0: Không biết các chỉ số RECAP.
- 1: Phân biệt được `changed` và `failed` nhưng nhầm lẫn giữa `ok` và `changed`.
- 2: Phân tích chính xác bản chất của cả 4 chỉ số `ok`, `changed`, `unreachable`, `failed`.
- 3: Nêu đúng + giải thích các cột bổ sung `skipped`, `rescued`, `ignored`.
**Câu hỏi đào sâu:** Nếu cột `unreachable` báo `1`, điều đó có nghĩa là gì đối với các Task còn lại trong Playbook? *(Các Task còn lại của Playbook sẽ bị bỏ qua trên host bị unreachable đó.)*

---

### Câu 5 — Kỹ thuật Kiểm tra Cú pháp với `--syntax-check`
**Hỏi:** Cờ CLI `--syntax-check` hoạt động thế nào? Tại sao phải chạy nó trước khi thực thi Playbook? *(Liên quan QT 5.2)*
**Đáp án chuẩn:** Cờ `ansible-playbook --syntax-check site.yml` nạp file Playbook và phân tích cấu trúc cú pháp YAML, kiểm tra các từ khóa hợp lệ của Ansible ngay tại Control node mà KHÔNG mở kết nối SSH tới máy đích. Chạy `--syntax-check` giúp phát hiện lỗi thụt lề, lỗi sai từ khóa lập tức trong 1 giây mà không tốn thời gian chờ kết nối hạ tầng.
**Tiêu chí chấm:**
- 0: Trả lời `--syntax-check` có kết nối SSH tới máy đích.
- 1: Biết kiểm tra lỗi YAML nhưng không biết nó chạy thuần túy tại Control node.
- 2: Nêu chính xác cơ chế kiểm tra offline tại Control node.
- 3: Nêu đúng + chỉ ra câu lệnh CLI chuẩn và tích hợp bước này vào pipeline CI/CD.
**Câu hỏi đào sâu:** Lệnh `--syntax-check` có phát hiện được lỗi sai IP máy đích trong Inventory không? *(Không, vì nó chỉ kiểm tra cú pháp file Playbook YAML chứ không kiểm tra kết nối mạng.)*

---

### Câu 6 — Thực thi Mô phỏng Dry-run với `--check --diff` 🔥
**Hỏi:** Phân biệt vai trò của cờ `--check` và cờ `--diff`. Kết hợp `--check --diff` mang lại lợi ích gì cho quản trị viên? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** Cờ `--check` (Dry-run) mô phỏng quá trình thực thi Playbook và dự báo các Task sẽ tạo ra thay đổi mà không làm thay đổi hệ thống thật. Cờ `--diff` hiển thị chi tiết dòng văn bản sẽ bị thêm/xóa trong các file cấu hình. Kết hợp `--check --diff` cho phép quản trị viên xem trước chính xác những gì SẼ thay đổi trên máy đích trước khi chính thức bấm chạy thật trên Production.
**Tiêu chí chấm:**
- 0: Không biết vai trò của `--check` và `--diff`.
- 1: Nêu được `--check` là chạy thử nhưng không giải thích được `--diff`.
- 2: Phân tích chính xác vai trò mô phỏng của `--check` và so sánh văn bản của `--diff`.
- 3: Nêu đúng + chỉ ra lưu ý một số lệnh shell/command không hỗ trợ check mode.
**Câu hỏi đào sâu:** Khi chạy với cờ `--check`, bảng `PLAY RECAP` báo `changed=2` có nghĩa là hệ thống thật đã bị thay đổi 2 chỗ đúng không? *(Không, đó chỉ là dự báo rằng nếu chạy thật thì sẽ có 2 chỗ bị thay đổi, hệ thống thật hiện tại chưa bị tác động.)*

---

### Câu 7 — Bó hẹp Phạm vi Thực thi với cờ `--limit`
**Hỏi:** Làm thế nào để thực thi file Playbook `site.yml` (vốn được cấu hình cho toàn bộ nhóm `web`) nhưng chỉ áp đặt thay đổi trên duy nhất `target1`? *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Sử dụng cờ `--limit` trên dòng lệnh CLI: `ansible-playbook --limit target1 site.yml`. Cờ `--limit` sẽ bó hẹp phạm vi thực thi của Playbook trên danh sách máy được chỉ định mà KHÔNG cần phải sửa đổi từ khóa `hosts: web` bên trong file mã nguồn Playbook.
**Tiêu chí chấm:**
- 0: Trả lời sửa trực tiếp file Playbook YAML.
- 1: Biết cờ `--limit` nhưng viết sai cú pháp câu lệnh CLI.
- 2: Nêu đúng cờ `--limit` và cú pháp lệnh CLI hoàn chỉnh.
- 3: Nêu đúng + giải thích lợi ích an toàn khi Canary deploy (thử nghiệm 1 node trước khi nhân rộng).
**Câu hỏi đào sâu:** Cờ `--limit` có thể truyền một nhóm máy thay vì một host đích danh được không? *(Có thể truyền tên nhóm, ví dụ `--limit dev_web` hoặc biểu thức pattern.)*

---

### Câu 8 — Tối ưu hóa Tốc độ với `gather_facts: false`
**Hỏi:** Bước `Gathering Facts` tự động ở đầu mỗi Play làm công việc gì? Khi nào nên tắt nó bằng `gather_facts: false`? *(Liên quan QT 6.2)*
**Đáp án chuẩn:** Bước `Gathering Facts` tự động gọi module `setup` để thu thập toàn bộ dữ liệu cấu hình thực tế của máy đích (IP, RAM, OS, CPU) và lưu vào các biến `ansible_facts`. Bước này tiêu tốn 3-5 giây per host. Nên tắt bằng `gather_facts: false` khi Playbook chỉ làm các tác vụ chép file/cài gói đơn giản mà KHÔNG sử dụng đến bất kỳ biến facts nào, giúp Playbook chạy nhanh tức thì.
**Tiêu chí chấm:**
- 0: Không biết bước `Gathering Facts` làm gì.
- 1: Biết lấy thông tin máy nhưng không biết cách tắt để tối ưu.
- 2: Nêu đúng bản chất gọi module `setup` + tham số `gather_facts: false`.
- 3: Nêu đúng + đưa ra con số đo lường thời gian tiết kiệm được khi tắt facts trên 100 máy chủ.
**Câu hỏi đào sâu:** Nếu trong Playbook có dùng biến `{{ ansible_distribution }}`, ta có được tắt `gather_facts: false` không? *(Không được tắt, vì tắt facts thì biến `ansible_distribution` sẽ bị undefined làm Playbook bị lỗi.)*

---

### Câu 9 — Cấu trúc Multi-play Playbook ★★★
**Hỏi:** Multi-play Playbook là gì? Khi nào cần sử dụng cấu trúc Multi-play trong một kịch bản triển khai? *(Liên quan QT 6.3)*
**Đáp án chuẩn:** Multi-play Playbook là một file Playbook YAML chứa nhiều hơn một Play nối tiếp nhau (mỗi Play bắt đầu bằng `- name:` riêng). Cần sử dụng Multi-play khi kịch bản tự động hóa bao phủ một hệ thống nhiều tầng (Multi-tier), yêu cầu các nhóm máy khác nhau chạy các nhiệm vụ khác nhau theo đúng thứ tự (ví dụ: Play 1 cấu hình nhóm `db`, sau đó Play 2 mới cấu hình nhóm `web`).
**Tiêu chí chấm:**
- 0: Cho rằng 1 file Playbook chỉ được chứa duy nhất 1 Play.
- 1: Biết chứa nhiều Play nhưng không nêu được ngữ cảnh hệ thống nhiều tầng.
- 2: Nêu đúng khái niệm Multi-play + ngữ cảnh ứng dụng chuẩn.
- 3: Nêu đúng + minh họa cấu trúc YAML của Multi-play gồm Play DB và Play Web.
**Câu hỏi đào sâu:** Các Play trong Multi-play Playbook có thể dùng các user hoặc cờ `become` khác nhau không? *(Có thể, mỗi Play có thuộc tính `remote_user` và `become` hoàn toàn độc lập.)*

---

### Câu 10 — Phương pháp Xác minh tính Bất biến và Trạng thái Thực tế 🔥
**Hỏi:** Trình bày quy trình 3 bước chuẩn hóa để chứng minh một file Playbook đạt tính Idempotency và máy đích ở đúng trạng thái.
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site.yml` để áp đặt cấu hình (RECAP báo `changed=N`).
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn lệnh `ansible-playbook site.yml` lần thứ hai: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`**.
3. **Bước 3 (Đối soát Sự thật):** Dùng `docker exec <target> ...` (truy vấn `systemctl is-active`, `cat <file>`) để kiểm tra hiện vật thực tế trên đĩa cứng máy đích, không dừng lại ở thông báo màu xanh của terminal.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc bước đối soát `docker exec`.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa lệnh CLI cụ thể.
- 3: Trình bày xuất sắc 3 bước + cho ví dụ thực tế minh chứng với lệnh CLI và giải thích ý nghĩa chỉ số `changed=0`.
**Câu hỏi đào sâu:** Nếu lượt chạy Lần 2 bảng RECAP báo `ok=4 changed=1 failed=0`, Playbook này đã đạt Idempotency chưa? *(Chưa đạt, vì vẫn còn 1 Task tạo ra thay đổi thừa ở lần chạy thứ 2.)*

---

### Câu 11 — Ý nghĩa chỉ số `skipped` và `rescued` trong RECAP ★★★
**Hỏi:** Giải thích ý nghĩa của chỉ số `skipped` và `rescued` trong bảng `PLAY RECAP`.
**Đáp án chuẩn:**
- `skipped`: Số Task bị bỏ qua không thực thi do không thỏa mãn điều kiện lọc (ví dụ điều kiện `when:` bị sai).
- `rescued`: Số Task gặp lỗi nhưng đã được khôi phục/xử lý thành công nhờ khối xử lý lỗi `rescue` (sẽ học ở Buổi 13), giúp Playbook tiếp tục thi hành mà không bị dừng đột ngột.
**Tiêu chí chấm:**
- 0: Không biết ý nghĩa của `skipped` và `rescued`.
- 1: Nêu được `skipped` là bỏ qua nhưng không biết `rescued`.
- 2: Phân tích chính xác cả 2 chỉ số `skipped` và `rescued`.
- 3: Nêu đúng + cho ví dụ điều kiện `when` dẫn tới `skipped`.
**Câu hỏi đào sâu:** Chỉ số `skipped=2` có làm cho Playbook bị coi là thất bại (failed) không? *(Không, skipped chỉ là bỏ qua task theo logic thiết kế, Playbook vẫn thành công bình thường.)*

---

### Câu 12 — Quản lý Playbook trong Môi trường CI/CD ★★★
**Hỏi:** Trong một kịch bản CI/CD tự động (như GitLab CI/GitHub Actions), quy trình kiểm thử Playbook trước khi deploy Production được sắp xếp như thế nào?
**Đáp án chuẩn:** Quy trình 4 bước chuẩn hóa trong CI/CD:
1. **Stage 1 (Lint/Syntax):** Chạy `ansible-lint` và `ansible-playbook --syntax-check` để kiểm tra lỗi trình bày và cú pháp.
2. **Stage 2 (Dry-run):** Chạy `ansible-playbook --check --diff` trên môi trường Staging.
3. **Stage 3 (Deploy & Idempotency Test):** Chạy Playbook Lần 1 trên Staging -> Chạy Lần 2 kiểm tra `changed=0`.
4. **Stage 4 (Production Gate):** Nếu tất cả các stage trước xanh 100%, mới kích hoạt bước deploy thật lên Production.
**Tiêu chí chấm:**
- 0: Không nêu được quy trình CI/CD.
- 1: Nêu được chạy thử nhưng thiếu các bước linter và idempotency test.
- 2: Nêu chính xác quy trình 4 bước trong CI/CD.
- 3: Phân tích xuất sắc tầm quan trọng của tự động hóa kiểm thử Playbook trong DevOps.
**Câu hỏi đào sâu:** Nếu Stage 1 báo lỗi syntax check thì pipeline CI/CD sẽ xử lý thế nào? *(Pipeline lập tức bị ngắt dừng (failed) và chặn không cho tiến hành các bước deploy tiếp theo.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về năng lực viết và vận hành Ansible Playbook, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi xây dựng Ansible Playbook theo chuẩn khai báo declarative với cấu trúc Play và Task được đặt tên tường minh 100%. Quy trình vận hành kịch bản của tôi luôn tuân thủ nghiêm ngặt 3 bước an toàn: chạy `--syntax-check` để phát hiện lỗi cú pháp YAML, chạy thử nghiệm `--check --diff` để dự báo thay đổi dòng, và luôn kiểm tra chỉ số `PLAY RECAP` ở lượt chạy thứ hai bắt buộc phải đạt `changed=0` để chứng minh tính bất biến (Idempotency). Sau cùng, tôi luôn đối soát sự thật thực tế trên máy đích qua `docker exec` hoặc SSH độc lập."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Phạm Văn G | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 2 / 3 | 3 | 3 / 3 | 33 / 36 | Xuất sắc |
| Vũ Thị H | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 06

Để chuẩn bị tốt nhất cho **Buổi 06: Idempotency — ok/changed/failed, chạy lần hai**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Tại sao một Task lạm dụng module `command`/`shell` lại khiến cho Playbook không bao giờ đạt tính Idempotency ở lượt chạy lần 2?
2. **Nghiên cứu trước 2:** Thuộc tính `creates` và `removes` trong module `command` giúp biến tác vụ lệnh thô thành tác vụ đạt tính Idempotency như thế nào?
3. **Nghiên cứu trước 3:** Làm thế nào để tự định nghĩa lại khi nào một Task được coi là thay đổi bằng thuộc tính `changed_when`?

---


### [Chuyên Đề 06] Giải Mã Tính Bất Biến (Idempotency): Cơ Chế Kiểm Tra Trạng Thái Đích & Tránh Cạm Bẫy 'Always Changed'

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Tại sao tính Idempotency (tính bất biến) lại được coi là tiêu chuẩn vàng định nghĩa một công cụ Quản trị Cấu hình (Configuration Management)? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b> Idempotency đảm bảo rằng việc thực thi một kịch bản cấu hình một lần hay nhiều lần trên cùng một hệ thống đều mang lại KẾT QUẢ TRẠNG THÁI CUỐI CÙNG GIỐNG NHAU, mà không gây ra tác dụng phụ (như đè đúp dữ liệu, tạo file rác trùng lặp, làm sập dịch vụ). Nó chuyển đổi tư duy từ "gõ chuỗi lệnh thủ công" (Imperative) sang "khai báo trạng thái muốn có" (Declarative), giúp kịch bản chạy an toàn định kỳ trên hạ tầng quy mô lớn.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết định nghĩa Idempotency.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Nói "chạy lại không bị lỗi" nhưng không giải thích được Declarative State Model.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Giải thích đúng cơ chế Declarative và tính an toàn khi chạy lại nhiều lần.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Phân tích xuất sắc sự khác biệt giữa Script Bash (Imperative) và Ansible Playbook (Declarative) kèm ví dụ thực tế.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu một script Bash gõ lệnh <code>echo "export PATH=$PATH:/opt/bin" >> /etc/profile</code> được chạy 10 lần, điều gì sẽ xảy ra? *(Dòng cấu hình bị nối thêm 10 lần vào file profile làm hỏng file, thể hiện sự thiếu Idempotency.)*
</div>
</details>

---

### Câu 2 — Phân biệt 3 Trạng thái Task: OK, CHANGED, FAILED 🔥
**Hỏi:** Phân biệt ý nghĩa của 3 trạng thái Task: `ok`, `changed`, và `failed`. Tại sao lượt chạy Lần 2 chỉ số `ok` tăng lên lại là tín hiệu tốt? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- `ok`: Hệ thống trên máy đích ĐÃ Ở ĐÚNG TRẠNG THÁI khai báo, Ansible không thực hiện thay đổi nào.
- `changed`: Hệ thống CHƯA ĐÚNG TRẠNG THÁI, Ansible đã can thiệp thực hiện thay đổi thành công.
- `failed`: Task gặp lỗi đứt gãy trong quá trình thi hành và dừng Playbook.
Lượt chạy Lần 2 chỉ số `ok` tăng lên chứng minh hệ thống đang được giữ nguyên an toàn, các task không bị can thiệp thừa.
**Tiêu chí chấm:**
- 0: Không phân biệt được `ok` và `changed`.
- 1: Phân biệt được `changed` và `failed` nhưng nhầm `ok` là có thay đổi.
- 2: Phân tích chính xác bản chất của cả 3 trạng thái `ok`, `changed`, `failed`.
- 3: Nêu đúng + giải thích ý nghĩa chỉ số `changed=0` ở lượt chạy Lần 2.
**Câu hỏi đào sâu:** Nếu lượt chạy Lần 1 báo `ok=2 changed=3`, lượt chạy Lần 2 báo `ok=5 changed=0`, điều này khẳng định điều gì? *(Khẳng định Playbook đạt tính Idempotency 100%, toàn bộ 5 Task ở Lần 2 đã ở đúng trạng thái mong muốn.)*

---

### Câu 3 — Nguyên nhân Task Command/Shell không Idempotent 🔥
**Hỏi:** Tại sao các tác vụ sử dụng module `ansible.builtin.command` hoặc `ansible.builtin.shell` mặc định luôn báo `changed=true` ở mọi lượt chạy? *(Liên quan QT 4.3)*
**Đáp án chuẩn:** Vì Ansible Engine xem `command` và `shell` là các "hộp đen" thực thi câu lệnh Linux thô. Engine không thể biết đoạn script shell bên trong chứa những lệnh gì và có làm biến đổi đĩa cứng hay không. Để an toàn, Ansible mặc định coi mọi lệnh shell đều tạo ra thay đổi và gán trạng thái `CHANGED`.
**Tiêu chí chấm:**
- 0: Trả lời "do lệnh shell bị lỗi".
- 1: Biết lệnh shell luôn báo changed nhưng không giải thích được lý do Ansible không soi được bên trong script.
- 2: Giải thích đúng lý do Ansible xem lệnh shell là hộp đen không tự kiểm tra trạng thái được.
- 3: Nêu đúng + đề xuất 2 giải pháp khắc phục (`creates`/`removes` hoặc chuyển sang module chuyên dụng).
**Câu hỏi đào sâu:** Nếu không khắc phục task `shell` thô này, bảng `PLAY RECAP` ở lượt chạy Lần 2 sẽ ra sao? *(Bảng RECAP lượt 2 sẽ tiếp tục báo `changed > 0`, làm Playbook không bao giờ đạt chuẩn Idempotent.)*

---

### Câu 4 — Kỹ thuật Sử dụng `creates` và `removes` 🔥
**Hỏi:** Trình bày cơ chế hoạt động của thuộc tính `creates` và `removes` trong module `command`/`shell`. Cho ví dụ. *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- `creates: /path/to/file`: Kiểm tra xem file/thư mục có tồn tại trên máy đích hay chưa. Nếu ĐÃ TỒN TẠI, Ansible BỎ QUA Task (báo `ok / changed=false`); nếu CHƯA TỒN TẠI mới thực thi lệnh shell.
- `removes: /path/to/file`: Kiểm tra xem file/thư mục có tồn tại hay không. Nếu ĐANG TỒN TẠI mới thực thi lệnh shell (ví dụ lệnh xóa); nếu KHÔNG TỒN TẠI thì BỎ QUA Task.
**Tiêu chí chấm:**
- 0: Nhầm lẫn giữa `creates` và `removes`.
- 1: Biết `creates` bỏ qua khi có file nhưng không giải thích được `removes`.
- 2: Phân tích chính xác cơ chế kiểm tra file của cả `creates` và `removes`.
- 3: Nêu đúng + viết đoạn YAML minh họa kịch bản giải nén file tar.gz dùng `creates`.
**Câu hỏi đào sâu:** Nếu đường dẫn file khai báo trong `creates` bị gõ sai chính tả, điều gì sẽ xảy ra ở lượt chạy Lần 2? *(Ansible tìm không thấy file nên vẫn tiếp tục chạy lại lệnh shell ở Lần 2, làm mất tính Idempotency.)*

---

### Câu 5 — Điều khiển Trạng thái Báo Changed với `changed_when: false`
**Hỏi:** Khi nào nên khai báo thuộc tính `changed_when: false` cho một Task? Cho 2 ví dụ thực tế. *(Liên quan QT 5.2)*
**Đáp án chuẩn:** Nên dùng `changed_when: false` cho các Task **chỉ đọc dữ liệu hoặc truy vấn trạng thái** từ máy đích mà KHÔNG thực hiện bất kỳ thao tác ghi/sửa đổi nào lên đĩa cứng. Ví dụ: (1) Chạy lệnh `uname -a` lấy thông tin kernel, (2) Chạy lệnh `cat /etc/os-release` kiểm tra phiên bản OS, (3) Chạy lệnh truy vấn trạng thái DB.
**Tiêu chí chấm:**
- 0: Cho rằng `changed_when: false` dùng cho mọi loại Task.
- 1: Biết dùng cho task đọc nhưng không cho được ví dụ cụ thể.
- 2: Nêu đúng bản chất Task Read-Only + đưa 2 ví dụ chuẩn.
- 3: Nêu đúng + phân tích tác hại nếu lạm dụng `changed_when: false` cho task ghi dữ liệu thật.
**Câu hỏi đào sâu:** Nếu một Task chạy lệnh `echo "data" > /file.txt` mà khai báo `changed_when: false`, điều gì sẽ xảy ra? *(Bảng RECAP báo `changed=0` giả mạo, nhưng thực tế đĩa cứng máy đích vẫn bị ghi đè mỗi lần chạy vi phạm nguyên tắc quản trị.)*

---

### Câu 6 — Tự định nghĩa Điều kiện Changed với Biểu thức Logic
**Hỏi:** Làm thế nào để tự định nghĩa điều kiện báo `changed` dựa trên kết quả trả về của câu lệnh shell qua thuộc tính `changed_when`? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** Đăng ký kết quả trả về của lệnh shell vào một biến bằng thuộc tính `register: result_var`, sau đó sử dụng biểu thức logic trong `changed_when` để kiểm tra chuỗi `stdout` hoặc mã `rc`. Ví dụ: `changed_when: "'UPDATED' in result_var.stdout"` (chỉ báo `changed=true` khi chuỗi `stdout` chứa từ `UPDATED`).
**Tiêu chí chấm:**
- 0: Không biết kết hợp `register` và `changed_when`.
- 1: Nhớ `changed_when` nhưng viết sai cú pháp biểu thức Jinja/Python.
- 2: Nêu đúng cơ chế gán `register` + biểu thức `changed_when`.
- 3: Nêu đúng + viết đoạn mã YAML hoàn chỉnh minh họa kịch bản chạy script migration DB.
**Câu hỏi đào sâu:** Nếu câu lệnh shell trả về mã `rc=0` nhưng không làm thay đổi dữ liệu, biểu thức `changed_when: "result_var.rc == 0"` có chuẩn không? *(Không chuẩn, vì rc=0 chỉ là chạy lệnh thành công chứ không đồng nghĩa với có thay đổi dữ liệu.)*

---

### Câu 7 — Phép thử Lượt chạy Lần hai (Second-run Execution Test) 🔥
**Hỏi:** Trình bày quy trình Phép thử Lượt chạy Lần hai (Second-run test) để nghiệm thu một Playbook. Tại sao không thể bỏ qua bước này? *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Quy trình: (1) Chạy `ansible-playbook site.yml` Lần 1 để áp đặt cấu hình ban đầu. (2) Chạy lại nguyên vẹn câu lệnh `ansible-playbook site.yml` Lần thứ hai: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`**. Không thể bỏ qua bước này vì lượt chạy Lần 1 chỉ chứng minh kịch bản *chạy được*, chỉ có lượt chạy Lần 2 mới chứng minh kịch bản *an toàn bất biến khi vận hành định kỳ*.
**Tiêu chí chấm:**
- 0: Cho rằng chỉ cần chạy Lần 1 thành công là đủ nghiệm thu.
- 1: Nêu được chạy Lần 2 nhưng không giải thích được tại sao Lần 1 là chưa đủ.
- 2: Phân tích chính xác vai trò khác nhau của lượt Lần 1 (State Apply) và Lượt 2 (Idempotency Test).
- 3: Nêu đúng + minh họa bảng `PLAY RECAP` chuẩn của cả 2 lượt chạy.
**Câu hỏi đào sâu:** Nếu lượt chạy Lần 2 bảng RECAP báo `ok=4 changed=1 failed=0`, kết luận nghiệm thu là gì? *(Kết luận: Playbook KHÔNG ĐẠT tiêu chí Idempotency, bắt buộc phải tìm Task dính changed=1 để sửa lại.)*

---

### Câu 8 — Cảnh giác với "RECAP xanh mạo danh"
**Hỏi:** Phân biệt giữa "Bảng PLAY RECAP hiển thị màu xanh mạo danh" và "Hạ tầng đạt Idempotency thực tế". Làm sao để phát hiện gian lận này? *(Liên quan QT 6.2)*
**Đáp án chuẩn:** "RECAP xanh mạo danh" xảy ra khi người viết cố tình dùng `changed_when: false` hoặc `ignore_errors: true` để ép màn hình terminal báo `changed=0` / `failed=0`, nhưng thực tế trên máy đích dữ liệu vẫn bị ghi đè rác hoặc gặp lỗi ngầm. Để phát hiện gian lận: Dùng `docker exec <target> ...` đối soát trực tiếp nội dung file, số lượng dòng trùng lặp và trạng thái dịch vụ thật trên đĩa cứng máy đích.
**Tiêu chí chấm:**
- 0: Tin tưởng tuyệt đối 100% vào báo cáo màn hình Control node.
- 1: Biết có thể giấu lỗi nhưng không biết cách dùng `docker exec` đối soát.
- 2: Phân tích chính xác tác hại của RECAP mạo danh + giải pháp đối soát máy đích.
- 3: Nêu đúng + đưa ra ví dụ cụ thể câu lệnh `docker exec grep -c` đếm số dòng lặp để bóc phốt RECAP xanh mạo danh.
**Câu hỏi đào sâu:** Tại sao kiểm tra bằng `docker exec` lại là thước đo sự thật khách quan nhất? *(Vì docker exec truy vấn trực tiếp Kernel và File System của máy đích, không thông qua các bộ lọc báo cáo của Ansible Engine.)*

---

### Câu 9 — Tự động hóa Kiểm thử Idempotency trong CI/CD Pipeline ★★★
**Hỏi:** Trong một kịch bản CI/CD chuyên nghiệp (GitLab CI/GitHub Actions), bước Idempotency Test được tự động hóa bằng cách nào? *(Liên quan QT 6.3)*
**Đáp án chuẩn:** Trong pipeline CI/CD, sau bước chạy Playbook Lần 1 trên container thử nghiệm, kịch bản CI tự động thực thi lượt chạy Lần 2 và bắt luồng stdout của `PLAY RECAP`. Nếu script phát hiện chỉ số `changed=0`, pipeline trả về exit code 0 (PASSED). Nếu chỉ số `changed > 0`, pipeline trả về exit code 1 (FAILED) và tự động chặn không cho Merge mã nguồn.
**Tiêu chí chấm:**
- 0: Không biết cách tự động hóa kiểm thử Idempotency.
- 1: Biết chạy lần 2 trong CI nhưng không biết cách parse stdout RECAP.
- 2: Trình bày chính xác luồng kiểm thử 2 lượt + parse exit code trong CI pipeline.
- 3: Nêu đúng + đề xuất sử dụng công cụ kiểm thử tiêu chuẩn **Molecule** (`molecule verify / molecule test`).
**Câu hỏi đào sâu:** Công cụ **Molecule** trong hệ sinh thái Ansible có vai trò gì liên quan đến Idempotency? *(Molecule tự động khởi tạo container, chạy Playbook Lần 1, chạy Lần 2 kiểm tra changed=0, và dọn dẹp container tự động.)*

---

### Câu 10 — Kỹ thuật Chuyển đổi Lệnh thô sang Module Tiêu chuẩn 🔥
**Hỏi:** Trình bày 3 ví dụ chuyển đổi các câu lệnh Shell thô hay gặp trong thực tế thành các Module tiêu chuẩn đạt tính Idempotency 100%.
**Đáp án chuẩn:**
1. **Ca 1 (Tạo thư mục):** Chuyển `shell: mkdir /app` -> Module `ansible.builtin.file: path=/app state=directory mode='0755'`.
2. **Ca 2 (Sửa file cấu hình):** Chuyển `shell: echo "Port 2222" >> /etc/ssh/sshd_config` -> Module `ansible.builtin.lineinfile: path=/etc/ssh/sshd_config regexp='^#?Port' line='Port 2222'`.
3. **Ca 3 (Quản lý User):** Chuyển `shell: useradd deployer` -> Module `ansible.builtin.user: name=deployer state=present shell=/bin/bash`.
**Tiêu chí chấm:**
- 0: Không biết chuyển đổi sang module chuẩn.
- 1: Chuyển được 1 ca đơn giản nhưng nhầm lẫn tham số `lineinfile`.
- 2: Chuyển đổi chính xác cả 3 ca thực tế.
- 3: Trình bày xuất sắc cả 3 ca + giải thích lý do tại sao các module chuẩn lại đạt Idempotency tự nhiên.
**Câu hỏi đào sâu:** Tại sao dùng module `lineinfile` với `regexp` lại đảm bảo file không bị đè đúp dòng? *(Vì lineinfile tìm kiếm dòng cũ theo regex, nếu đã thấy dòng đúng nội dung thì nó giữ nguyên và báo changed=false.)*

---

### Câu 11 — Sử dụng Cờ `--check --diff` ở Lượt chạy Lần hai ★★★
**Hỏi:** Khi gõ lệnh `ansible-playbook --check --diff site.yml` ở lượt chạy Lần thứ hai, kết quả hiển thị trên terminal sẽ ra sao nếu Playbook chuẩn Idempotent?
**Đáp án chuẩn:** Kết quả hiển thị bảng `PLAY RECAP` với chỉ số `changed=0`, và KHÔNG HIỂN THỊ BẤT KỲ DÒNG DIFF NÀO (không có dòng xanh `+` hay dòng đỏ `-`). Điều này chứng minh 100% rằng không có bất kỳ dự báo thay đổi mạo danh nào trên máy đích.
**Tiêu chí chấm:**
- 0: Không biết kết quả hiển thị của `--check --diff` ở lượt chạy 2.
- 1: Biết `changed=0` nhưng không giải thích được màn hình diff trống.
- 2: Phân tích chính xác cả chỉ số RECAP `changed=0` và màn hình diff không xuất hiện thay đổi.
- 3: Nêu đúng + chỉ ra ý nghĩa của việc rà soát diff trống trước khi nghiệm thu kịch bản.
**Câu hỏi đào sâu:** Nếu màn hình diff Lần 2 hiển thị `- PermitRootLogin yes` và `+ PermitRootLogin no`, điều đó có nghĩa là gì? *(Có nghĩa là task vẫn đang đòi sửa đổi file ở Lần 2, Playbook chưa đạt tính Idempotency.)*

---

### Câu 12 — Tổng kết 5 Nguyên tắc Vàng kiểm soát Idempotency ★★★
**Hỏi:** Tóm tắt 5 Nguyên tắc Vàng để đảm bảo mọi Playbook Ansible do bạn viết ra đều đạt tính Idempotency tuyệt đối 100%.
**Đáp án chuẩn:**
1. **Nguyên tắc 1:** Luôn ưu tiên 100% Module tiêu chuẩn (`package`, `service`, `file`, `copy`, `lineinfile`, `user`, `cron`).
2. **Nguyên tắc 2:** Khi buộc phải dùng `command`/`shell`, bắt buộc bổ sung thuộc tính `creates` hoặc `removes`.
3. **Nguyên tắc 3:** Sử dụng `changed_when: false` cho các task chỉ đọc/truy vấn dữ liệu (`uname`, `cat`, `stat`).
4. **Nguyên tắc 4:** Bắt buộc thực thi Phép thử Lượt chạy Lần hai (Second-run test) đạt chỉ số `changed=0` trong RECAP.
5. **Nguyên tắc 5:** Tuyệt đối không dùng `changed_when: false` mạo danh; luôn dùng `docker exec` đối soát sự thật máy đích.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các nguyên tắc.
- 1: Liệt kê được 2-3 nguyên tắc chung chung.
- 2: Nêu đầy đủ 5 Nguyên tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 nguyên tắc + khẳng định thái độ làm việc chuẩn mực của một DevOps Engineer chuyên nghiệp.
**Câu hỏi đào sâu:** Trong 5 nguyên tắc trên, nguyên tắc nào đóng vai trò là "thước đo định lượng" để nghiệm thu kịch bản? *(Nguyên tắc 4: Phép thử Lượt chạy Lần hai đạt changed=0.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về tư duy kiểm soát Idempotency trong Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi coi Idempotency là linh hồn định nghĩa giá trị của Quản trị Cấu hình. Trong mọi kịch bản Ansible, tôi tuân thủ nghiêm ngặt nguyên tắc ưu tiên các module tiêu chuẩn, sử dụng `creates`/`removes` để kiểm soát các lệnh shell thô, và dùng `changed_when: false` cho các tác vụ truy vấn Read-Only. Tiêu chuẩn nghiệm thu duy nhất của tôi là Phép thử Lượt chạy Lần thứ hai bắt buộc phải đạt chỉ số `changed=0` trong `PLAY RECAP`. Tôi tuyệt đối nói không với hành vi ép trạng thái mạo danh và luôn dùng `docker exec` hoặc truy vấn hệ thống độc lập để đối soát sự thật thực tế trên máy đích."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Đăng Văn I | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 / 2 | 3 | 3 / 3 | 35 / 36 | Xuất sắc |
| Bùi Thị K | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 07

Để chuẩn bị tốt nhất cho **Buổi 07: Variables và Thứ tự Ưu tiên (Variables Precedence)**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Biến trong Ansible có thể được định nghĩa ở những vị trí nào (Playbook vars, Inventory vars, Extra vars, Role defaults)?
2. **Nghiên cứu trước 2:** Trong 22 tầng ưu tiên biến của Ansible, tầng nạp biến nào có quyền lực cao nhất (thắng tất cả các tầng khác)?
3. **Nghiên cứu trước 3:** Cờ CLI `-e` (hoặc `--extra-vars`) được sử dụng như thế nào khi muốn ghi đè giá trị biến ngay tại thời điểm thực thi Playbook?

---


### [Chuyên Đề 07] Hệ Thống Biến & Thứ Tự Ưu Tiên (Variable Precedence 22 Tầng): Extra Vars, Play Vars, Role Defaults & Inventory

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Trình bày cú pháp chuẩn để khai báo và truy vấn một biến trong Ansible Playbook. Khi nào bắt buộc phải bọc ngoặc kép quanh cú pháp <code>{{ }}</code>? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b> Biến được truy vấn bằng cú pháp Jinja2 bọc trong cặp ngoặc nhọn đúp <code>{{ variable_name }}</code>. Bắt buộc phải bọc ngoặc kép <code>"{{ variable_name }}"</code> khi biểu thức Jinja2 nằm ở ĐẦU GIÁ TRỊ của một thuộc tính YAML (ví dụ <code>dest: "{{ my_path }}"</code>), để ngăn trình biên dịch YAML hiểu nhầm cặp ngoặc nhọn <code>{</code> là mở đầu của một Dictionary YAML.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết cú pháp Jinja2 <code>{{ }}</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết <code>{{ }}</code> nhưng không giải thích được khi nào bắt buộc bọc ngoặc kép.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác cú pháp Jinja2 + lý do bọc ngoặc kép do quy chuẩn parser YAML.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + viết đoạn mã YAML minh họa lỗi nếu thiếu ngoặc kép và cách khắc phục.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu viết <code>dest: /etc/{{ app_name }}.conf</code> (không nằm ở đầu dòng giá trị), có bắt buộc phải bọc ngoặc kép không? *(Không bắt buộc, nhưng khuyến khích bọc toàn bộ chuỗi trong ngoặc kép để tạo thói quen an toàn.)*
</div>
</details>

---

### Câu 2 — Bảng Thứ tự Ưu tiên 22 Tầng Biến (Variable Precedence) 🔥
**Hỏi:** Trình bày nguyên tắc tổng quát của Bảng thứ tự ưu tiên biến trong Ansible. So sánh độ ưu tiên giữa `group_vars`, `host_vars`, Play `vars:`, và `vars_files:`. *(Liên quan QT 4.2)*
**Đáp án chuẩn:** Nguyên tắc tổng quát: **Càng hẹp và càng gần thời điểm thực thi thì có độ ưu tiên càng cao**. Thứ tự ưu tiên tăng dần: `group_vars` (Tầng 5) < `host_vars` (Tầng 9) < Play `vars:` (Tầng 12) < `vars_files:` (Tầng 14). Do đó, biến khai báo trong Play `vars:` hoặc `vars_files:` sẽ ghi đè lên biến cùng tên trong `host_vars` và `group_vars`.
**Tiêu chí chấm:**
- 0: Nhầm lẫn cho rằng `group_vars` có ưu tiên cao nhất.
- 1: Nêu được một vài tầng nhưng xếp sai thứ tự giữa `host_vars` và Play `vars:`.
- 2: Phân tích chính xác thứ tự 4 nguồn biến phổ biến này theo nguyên tắc từ rộng đến hẹp.
- 3: Nêu đúng + minh họa ví dụ thực tế xung đột biến `app_port` ở cả 4 tầng.
**Câu hỏi đào sâu:** Tại sao Ansible lại thiết kế nhiều tầng biến như vậy? *(Để cho phép định nghĩa các giá trị mặc định chung ở tầng rộng, sau đó cho phép tùy biến đè giá trị ở các tầng hẹp hơn mà không phải sửa mã nguồn gốc.)*

---

### Câu 3 — Quyền lực Tuyệt đối của Extra Vars `-e` 🔥
**Hỏi:** Extra Vars (truyền qua cờ CLI `-e` / `--extra-vars`) nằm ở tầng ưu tiên nào trong tháp ưu tiên biến? Cho ví dụ ứng dụng thực tế. *(Liên quan QT 4.3)*
**Đáp án chuẩn:** Extra Vars nằm ở TẦNG UY TIÊN CAO NHẤT TUYỆT ĐỐI (Tầng 22), ghi đè lên TẤT CẢ các biến đã được khai báo ở bất kỳ file hay vị trí nào khác trong Playbook và Inventory. Ứng dụng thực tế: Dùng khi người vận hành CLI cần hot-fix hoặc truyền tham số chạy khẩn cấp (ví dụ `ansible-playbook -e "app_port=9999" site.yml`) mà không muốn sửa mã nguồn trên Git.
**Tiêu chí chấm:**
- 0: Không biết cờ CLI `-e`.
- 1: Biết cờ `-e` truyền biến nhưng không biết nó đứng ở tầng cao nhất tuyệt đối.
- 2: Giải thích chính xác vị trí Tầng 22 của Extra Vars + cú pháp câu lệnh CLI.
- 3: Nêu đúng + minh họa 2 cách truyền cờ `-e` (dạng chuỗi `key=val` và dạng file JSON/YAML `-e "@file.yml"`).
**Câu hỏi đào sâu:** Nếu trong Playbook có gọi module `set_fact: app_port=8080`, cờ CLI `-e "app_port=9999"` có bị thay đổi theo không? *(Không, cờ Extra Vars -e vẫn thắng cả set_fact và duy trì giá trị 9999.)*

---

### Câu 4 — Phân biệt Phạm vi Biến (Variable Scopes) 🔥
**Hỏi:** Phân biệt 3 phạm vi hoạt động của biến: Global Scope, Play Scope, và Host Scope. Dưa ra ví dụ cho từng loại. *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- **Global Scope:** Biến có hiệu lực trên toàn bộ hệ thống (ví dụ: cờ Extra Vars `-e`, biến môi trường `ansible.cfg`).
- **Play Scope:** Biến chỉ có hiệu lực trong phạm vi một Play cụ thể (ví dụ: biến trong từ khóa `vars:` hoặc `vars_files:` của Play đó).
- **Host Scope:** Biến gắn liền với một host cụ thể (ví dụ: `host_vars`, `ansible_facts`, biến đăng ký `register`, `set_fact`).
**Tiêu chí chấm:**
- 0: Không phân biệt được Scope của biến.
- 1: Liệt kê được tên Scope nhưng xếp nhầm nguồn biến vào sai Scope.
- 2: Phân tích chính xác bản chất và ví dụ của cả 3 loại Scope.
- 3: Nêu đúng + giải thích lý do tại sao biến `register` ở Play 1 lại có thể dùng được ở Play 2 (vì mang Host Scope).
**Câu hỏi đào sâu:** Biến khai báo trong `vars:` của Play 1 có dùng được cho Task thuộc Play 2 trong cùng 1 file Playbook không? *(Không, vì biến trong `vars:` của Play mang Play Scope, tự động biến mất khi kết thúc Play 1.)*

---

### Câu 5 — Kỹ thuật Đăng ký Kết quả với `register`
**Hỏi:** Thuộc tính `register` hoạt động như thế nào? Cấu trúc của một biến `register` gồm những thông tin quan trọng nào? *(Liên quan QT 5.2)*
**Đáp án chuẩn:** Thuộc tính `register: var_name` bắt toàn bộ dữ liệu kết quả trả về từ việc thi hành một Task và lưu vào biến `var_name` mang Host Scope. Cấu trúc của biến `register` là một Dictionary chứa các trường dữ liệu quan trọng: `rc` (mã exit code), `stdout` (chuỗi văn bản in ra), `stdout_lines` (danh sách các dòng output), `stderr` (chuỗi báo lỗi), và `changed` (trạng thái có thay đổi hay không).
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `register`.
- 1: Biết `register` lưu kết quả nhưng không liệt kê được các trường `rc`, `stdout`, `stderr`.
- 2: Phân tích chính xác cơ chế lưu trữ và cấu trúc Dictionary của biến `register`.
- 3: Nêu đúng + viết đoạn YAML minh họa lấy `var_name.stdout` làm dữ liệu đầu vào cho task sau.
**Câu hỏi đào sâu:** Làm thế nào để kiểm tra một Task chạy lệnh shell có thành công (exit code = 0) hay không thông qua biến `register`? *(Dùng điều kiện `when: res_var.rc == 0` ở task tiếp theo.)*

---

### Câu 6 — Khởi tạo Biến Runtime với `ansible.builtin.set_fact`
**Hỏi:** Module `ansible.builtin.set_fact` được sử dụng trong trường hợp nào? Biến tạo bởi `set_fact` nằm ở tầng ưu tiên và Scope nào? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** `set_fact` được dùng để khởi tạo hoặc cập nhật giá trị biến mới một cách linh hoạt tại thời điểm runtime (dựa trên kết quả tính toán hoặc thông tin Facts thu thập được). Biến tạo bởi `set_fact` mang **Host Scope** (tồn tại xuyên suốt các Play sau) và nằm ở **Tầng ưu tiên rất cao (Tầng 19)**, ghi đè các biến tĩnh trong `vars:`, `vars_files:`, `host_vars`, `group_vars`.
**Tiêu chí chấm:**
- 0: Không biết module `set_fact`.
- 1: Biết `set_fact` tạo biến nhưng nhầm sang Play Scope.
- 2: Phân tích chính xác vai trò tạo biến runtime + Host Scope + Tầng ưu tiên 19.
- 3: Nêu đúng + cho ví dụ thực tế tính toán cổng dịch vụ động: `set_fact: app_port="{{ base_port | int + host_id }}"`.
**Câu hỏi đào sâu:** Biến tạo bởi `set_fact` ở Play 1 có bị đè bởi cờ Extra Vars CLI `-e` không? *(Có, vì Extra Vars Tầng 22 cao hơn set_fact Tầng 19.)*

---

### Câu 7 — Quy trình Gỡ lỗi Biến với module `debug`
**Hỏi:** Phân biệt cách dùng thuộc tính `msg:` và thuộc tính `var:` trong module `ansible.builtin.debug`. *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- `msg:` Dùng để in một chuỗi văn bản định dạng tự chọn. Nếu muốn chèn giá trị biến vào chuỗi thì **BẮT BUỘC bọc `{{ variable_name }}`** (ví dụ `msg: "Port is {{ app_port }}"`).
- `var:` Dùng để in toàn bộ giá trị hoặc cấu trúc dữ liệu (String, List, Dict) của một biến. **TUYỆT ĐỐI KHÔNG bọc `{{ }}`** (ví dụ `var: app_port` hoặc `var: register_res`).
**Tiêu chí chấm:**
- 0: Không phân biệt được `msg` và `var`.
- 1: Biết cả 2 nhưng nhầm lẫn bọc `{{ }}` ở thuộc tính `var`.
- 2: Phân tích chính xác sự khác biệt về mục đích sử dụng và cú pháp Jinja2 của `msg` và `var`.
- 3: Nêu đúng + minh họa output hiển thị của màn hình terminal trong cả 2 trường hợp.
**Câu hỏi đào sâu:** Nếu viết `- ansible.builtin.debug: var="{{ app_port }}"`, màn hình terminal sẽ in ra gì? *(Nó sẽ in ra tên chuỗi biến đại diện chứ không in cấu trúc dữ liệu chuẩn của biến.)*

---

### Câu 8 — Quy tắc Đặt tên Biến An toàn 🔥
**Hỏi:** Trình bày các quy tắc bắt buộc khi đặt tên biến trong Ansible. Tại sao việc dùng phím gạch ngang `-` (như `web-port`) lại gây ra lỗi hệ thống? *(Liên quan QT 6.2)*
**Đáp án chuẩn:** Quy tắc đặt tên biến: Chỉ được sử dụng chữ cái thường, chữ số và dấu gạch dưới `_` (dạng `snake_case`), bắt đầu bằng chữ cái. CẤM tuyệt đối dùng dấu gạch ngang `-`, khoảng trắng, hay ký tự đặc biệt. Dùng phím gạch ngang `-` sẽ bị trình biên dịch Jinja2 và Python hiểu nhầm là phép toán trừ (subtraction), dẫn tới lỗi cú pháp `UndefinedError` hoặc tính toán sai.
**Tiêu chí chấm:**
- 0: Cho rằng đặt tên biến kiểu gì cũng được.
- 1: Biết dùng dấu `_` nhưng không giải thích được lý do phím `-` bị lỗi toán trừ Python.
- 2: Giải thích chính xác quy chuẩn `snake_case` và xung đột toán tử trừ `-` trong Jinja2.
- 3: Nêu đúng + viết ví dụ các tên biến chuẩn cho dự án thực tế.
**Câu hỏi đào sâu:** Tên biến `123_app_port` có hợp lệ không? *(Không hợp lệ, vì tên biến không được bắt đầu bằng chữ số.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi dùng Biến 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook có sử dụng biến số để đảm bảo tính Idempotency và máy đích ở đúng trạng thái.
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1 với Biến):** Chạy `ansible-playbook -e "app_port=9999" site.yml` để áp đặt cấu hình theo giá trị biến mới.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn lệnh CLI đó Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`**.
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/app.conf` để kiểm tra giá trị `9999` thực sự được ghi xuống file đĩa cứng máy đích, không dừng lại ở báo cáo terminal.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần xem log terminal Lần 1 báo xanh là đủ" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc bước đối soát `docker exec`.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI cụ thể.
- 3: Trình bày xuất sắc 3 bước + cho ví dụ thực tế lệnh `docker exec grep` đối soát giá trị biến trên máy đích.
**Câu hỏi đào sâu:** Nếu ở Lần 2 không truyền cờ `-e "app_port=9999"`, chỉ số RECAP Lần 2 sẽ ra sao? *(Lần 2 sẽ bị `changed=1` do Playbook nạp lại biến cũ ở tầng thấp hơn và thực hiện sửa lùi cấu hình.)*

---

### Câu 10 — Kỹ thuật Nạp Biến từ File `vars_files` và `group_vars` ★★★
**Hỏi:** Phân biệt sự khác nhau về ngữ cảnh sử dụng giữa thư mục `group_vars/` và từ khóa `vars_files:` trong Playbook.
**Đáp án chuẩn:**
- `group_vars/`: Biến được Ansible TỰ ĐỘNG NẠP dựa trên tên nhóm máy trong Inventory (ví dụ: host thuộc nhóm `web` tự động nạp `group_vars/web.yml`). Giúp mã nguồn Playbook gọn gàng, tách biệt cấu hình môi trường khỏi logic Playbook.
- `vars_files:` Biến được KHAI BÁO CỨNG trong file Playbook YAML (ví dụ `vars_files: - vars/external.yml`). Tất cả các host chạy Play đó đều nạp chung file này bất kể thuộc nhóm nào.
**Tiêu chí chấm:**
- 0: Nhầm lẫn giữa `group_vars` và `vars_files`.
- 1: Nêu được `group_vars` tự động nạp nhưng không giải thích được vai trò của `vars_files`.
- 2: Phân tích chính xác cơ chế nạp tự động theo Inventory vs nạp khai báo cứng trong Playbook.
- 3: Nêu đúng + khuyến nghị tổ chức mã nguồn chuẩn DevOps (ưu tiên `group_vars` hơn `vars_files`).
**Câu hỏi đào sâu:** Nếu cả `group_vars/web.yml` và `vars_files:` cùng chứa biến `port`, giá trị ở đâu sẽ thắng? *(Giá trị trong `vars_files:` thắng vì có tầng ưu tiên Tầng 14 cao hơn group_vars Tầng 5.)*

---

### Câu 11 — Bảo mật Biến Nhạy cảm với Ansible Vault ★★★
**Hỏi:** Làm thế nào để quản lý các biến chứa thông tin nhạy cảm (như mật khẩu DB, API Key) một cách an toàn trong mã nguồn Playbook?
**Đáp án chuẩn:** Sử dụng công cụ **Ansible Vault** để mã hóa file chứa biến nhạy cảm (lệnh `ansible-vault encrypt vars/secrets.yml`). File sau khi mã hóa trở thành chuỗi văn bản vô nghĩa có thể commit an toàn lên Git. Khi thực thi Playbook, truyền cờ `--vault-id @prompt` hoặc `--vault-password-file` để Ansible giải mã file biến trong bộ nhớ RAM ở thời điểm chạy.
**Tiêu chí chấm:**
- 0: Cho rằng gõ mật khẩu plain-text vào Playbook rồi đẩy lên Git là bình thường.
- 1: Biết dùng Ansible Vault mã hóa nhưng không nhớ cờ CLI nạp password khi chạy.
- 2: Phân tích chính xác quy trình mã hóa bằng Vault + nạp password qua cờ CLI.
- 3: Nêu đúng + mô tả mô hình quản lý key Vault bằng file mật khẩu phân quyền trong doanh nghiệp.
**Câu hỏi đào sâu:** Nếu file biến bị mã hóa bởi Vault nhưng khi chạy Playbook không truyền cờ Vault password, Ansible sẽ báo lỗi gì? *(Ansible báo lỗi `Decryption failed` và dừng thi hành ngay lập tức.)*

---

### Câu 12 — Quản lý Biến trong Môi trường Đa Hạ tầng (Dev/Staging/Prod) ★★★
**Hỏi:** Trình bày kiến trúc tổ chức biến tối ưu cho một dự án triển khai trên 3 môi trường Dev, Staging, và Production nhưng chỉ dùng duy nhất 1 file Playbook `site.yml`.
**Đáp án chuẩn:**
1. Tạo 1 file Playbook duy nhất `site.yml` chứa logic khai báo trạng thái (dùng tên biến trừu tượng `{{ db_host }}`, `{{ app_port }}`).
2. Tổ chức cấu hình biến theo từng môi trường trong Inventory hoặc thư mục `group_vars`:
   - `group_vars/dev.yml` chứa biến môi trường Dev.
   - `group_vars/staging.yml` chứa biến môi trường Staging.
   - `group_vars/prod.yml` chứa biến môi trường Prod.
3. Khi deploy môi trường nào, chỉ cần chỉ định Inventory tương ứng: `ansible-playbook -i inventories/prod/hosts site.yml`.
**Tiêu chí chấm:**
- 0: Trả lời tạo 3 file Playbook riêng lẻ cho 3 môi trường.
- 1: Nêu được dùng 1 Playbook nhưng không biết cách chia biến theo `group_vars` môi trường.
- 2: Phân tích chính xác kiến trúc 1 Playbook + đa Inventory/group_vars theo môi trường.
- 3: Nêu đúng + phân tích lợi ích tối đa của việc tái sử dụng mã nguồn và tuân thủ nguyên tắc DRY (Don't Repeat Yourself).
**Câu hỏi đào sâu:** Kiến trúc trên giúp tiết kiệm bao nhiêu phần trăm công sức bảo trì mã nguồn Playbook? *(Tiết kiệm hơn 70% công sức, vì khi sửa đổi logic cài đặt chỉ cần sửa trên 1 file site.yml duy nhất.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về năng lực quản lý biến và xử lý xung đột trong Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi làm chủ Bảng thứ tự ưu tiên 22 tầng biến của Ansible để thiết kế kiến trúc cấu hình chuẩn hóa cho hệ thống đa môi trường. Tôi tuân thủ quy tắc tổ chức biến phân tầng từ `group_vars` rộng nhất đến `host_vars` đặc thù, giữ Playbook sạch sẽ và dùng cờ Extra Vars `-e` cho các quyết định override tức thì ở thời điểm thi hành. Mọi kịch bản dùng biến của tôi đều tuân thủ quy chuẩn đặt tên `snake_case`, được gỡ lỗi minh bạch qua module `debug`, bảo mật tuyệt đối bằng Ansible Vault, và kiểm thử Idempotency Lần 2 đạt `changed=0` kết hợp đối soát thực tế trên máy đích qua `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Ngô Văn L | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Trịnh Thị M | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 08

Để chuẩn bị tốt nhất cho **Buổi 08: Facts — ansible_facts, setup module, custom facts**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Ansible Facts là gì? Module nào tự động chạy ở đầu mỗi Play để thu thập thông tin này?
2. **Nghiên cứu trước 2:** Làm thế nào để trích xuất địa chỉ IP, dung lượng RAM, và phiên bản hệ điều hành từ biến `ansible_facts`?
3. **Nghiên cứu trước 3:** Custom Facts (.fact files) được lưu ở đường dẫn thư mục nào trên máy đích và có cấu trúc ra sao?

---


### [Chuyên Đề 08] Thu Thập & Khai Thác Ansible Facts: Setup Module, Custom Facts, Gathers Facts Optimization & Smart Caching

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Ansible Facts là gì? Module nào chịu trách nhiệm tự động thu thập Facts ở đầu mỗi Play? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b> Ansible Facts là tập hợp toàn bộ dữ liệu cấu hình thực tế về phần cứng (CPU, RAM, đĩa cứng), mạng (IP, MAC, hostname), và hệ điều hành của máy đích tại thời điểm chạy. Module <code>ansible.builtin.setup</code> được Ansible Engine tự động gọi ở đầu mỗi Play (nếu <code>gather_facts: true</code>) để thực hiện công việc tự khám phá (Auto-discovery) và đóng gói dữ liệu thành biến <code>ansible_facts</code>.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết định nghĩa Ansible Facts.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết Facts là thông tin máy nhưng không nhớ tên module <code>ansible.builtin.setup</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác khái niệm Facts + cơ chế tự động gọi module <code>setup</code> ở đầu Play.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa câu lệnh CLI Ad-hoc <code>ansible target1 -m setup</code> để soi facts.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Bước <code>Gathering Facts</code> diễn ra trước hay sau các Task khai báo trong Playbook? *(Diễn ra đầu tiên trước tất cả các Task khai báo trong Play.)*
</div>
</details>

---

### Câu 2 — Trích xuất Biến `ansible_facts` 🔥
**Hỏi:** Trình bày cú pháp chuẩn để trích xuất địa chỉ IP chính, tên hệ điều hành, và dung lượng RAM của máy đích từ biến `ansible_facts`. *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- Địa chỉ IP chính: `{{ ansible_facts.default_ipv4.address }}`
- Tên hệ điều hành: `{{ ansible_facts.distribution }}` (hoặc `{{ ansible_facts.os_family }}`)
- Dung lượng RAM (MB): `{{ ansible_facts.memtotal_mb }}`
**Tiêu chí chấm:**
- 0: Dùng sai tên biến hoặc không trích xuất được.
- 1: Dùng cú pháp legacy kiểu cũ `ansible_default_ipv4` mà không nêu được chuẩn mới `ansible_facts`.
- 2: Phân tích chính xác cấu pháp trích xuất 3 thông số này qua namespace `ansible_facts`.
- 3: Nêu đúng + giải thích lý do tại sao chuẩn mới `ansible_facts.key.subkey` lại an toàn hơn cú pháp cũ.
**Câu hỏi đào sâu:** Sự khác biệt giữa `ansible_facts.distribution` và `ansible_facts.os_family` là gì? *(distribution trả về tên OS cụ thể như Ubuntu, CentOS; os_family trả về nhóm họ OS như Debian, RedHat.)*

---

### Câu 3 — Tối ưu Hiệu năng với `gather_subset` và `gather_facts` 🔥
**Hỏi:** Làm thế nào để tối ưu tốc độ thực thi Playbook khi không sử dụng hết tất cả thông số Facts của hệ thống? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Cách 1: Tắt hoàn toàn bước quét facts nếu kịch bản không dùng đến biến facts bằng cách khai báo `gather_facts: false` ở cấp độ Play.
- Cách 2: Sử dụng thuộc tính `gather_subset` để chỉ định cụ thể nhóm thông tin cần quét (ví dụ `gather_subset: ["!all", "!min", "network"]` để chỉ quét thông tin mạng), giúp giảm 80% thời gian chờ thu thập.
**Tiêu chí chấm:**
- 0: Không biết cách tối ưu tốc độ thu thập facts.
- 1: Biết `gather_facts: false` nhưng không biết dùng `gather_subset` để lọc một phần.
- 2: Phân tích chính xác cả 2 giải pháp `gather_facts: false` và `gather_subset`.
- 3: Nêu đúng + đưa ra con số đo lường thời gian tiết kiệm được trên 100 máy chủ khi dùng `gather_subset`.
**Câu hỏi đào sâu:** Nếu trong Playbook có dùng `ansible_facts.os_family` mà ta lại đặt `gather_facts: false`, điều gì sẽ xảy ra? *(Playbook sẽ báo lỗi fatal: undefined variable cho ansible_facts.)*

---

### Câu 4 — Khái niệm và Đường dẫn Custom Facts (Local Facts) 🔥
**Hỏi:** Custom Facts (Local Facts) là gì? Chúng được lưu trữ ở đường dẫn thư mục nào trên máy đích? *(Liên quan QT 5.1)*
**Đáp án chuẩn:** Custom Facts là các thông tin tùy biến do người dùng/doanh nghiệp tự định nghĩa (như tên ứng dụng, môi trường, phiên bản release) để bổ sung vào bộ facts mặc định của Ansible. Tất cả các tệp Custom Facts **BẮT BUỘC phải đặt tại thư mục `/etc/ansible/facts.d/`** trên máy đích và phải có đuôi mở rộng `.fact`.
**Tiêu chí chấm:**
- 0: Không biết Custom Facts hoặc nhớ sai đường dẫn.
- 1: Biết Custom Facts nhưng nhớ nhầm sang đường dẫn `/etc/facts.d/` (thiếu `ansible`).
- 2: Phân tích chính xác khái niệm Custom Facts + đường dẫn tuyệt đối `/etc/ansible/facts.d/*.fact`.
- 3: Nêu đúng + giải thích cơ chế Ansible tự động nạp toàn bộ các file `.fact` trong thư mục này khi gọi module `setup`.
**Câu hỏi đào sâu:** Thư mục `/etc/ansible/facts.d/` nằm trên Control Node hay trên Managed Node (máy đích)? *(Nằm trực tiếp trên Managed Node máy đích.)*

---

### Câu 5 — Các Định dạng của Tệp Custom Facts
**Hỏi:** Tệp Custom Facts chấp nhận những định dạng tệp tin nào? Phân biệt giữa Custom Fact tĩnh và Custom Fact động. *(Liên quan QT 5.2)*
**Đáp án chuẩn:** Chấp nhận 3 định dạng:
1. **Định dạng INI tĩnh:** File chứa các cặp `[section]` và `key=value`.
2. **Định dạng JSON tĩnh:** File chứa cấu hình JSON Object chuẩn.
3. **Script thực thi (Custom Fact động):** Script Bash/Python có cờ `chmod +x` trả về chuỗi JSON ra `stdout`.
Custom Fact tĩnh dùng cho cấu hình cố định; Custom Fact động dùng để tính toán dữ liệu thời gian thực trên máy đích trước khi trả về cho Ansible.
**Tiêu chí chấm:**
- 0: Không biết các định dạng của tệp Custom Facts.
- 1: Biết định dạng INI/JSON tĩnh nhưng không giải thích được Script thực thi động.
- 2: Phân tích chính xác 3 định dạng + sự khác nhau giữa tĩnh và động.
- 3: Nêu đúng + viết ví dụ mã nguồn một Script Bash Custom Fact trả về JSON hợp lệ.
**Câu hỏi đào sâu:** Điều gì xảy ra nếu một Script Custom Fact động thiếu quyền thực thi `chmod +x`? *(Ansible xem đó là file văn bản thô và báo lỗi parse cú pháp khi chạy module setup.)*

---

### Câu 6 — Truy xuất Custom Facts trong Playbook
**Hỏi:** Trình bày cú pháp chuẩn Jinja2 để trích xuất một thuộc tính từ tệp Custom Fact tên `custom_app.fact` chứa section `[application]` và key `environment`. *(Liên quan QT 5.3)*
**Đáp án chuẩn:** Cú pháp: `{{ ansible_facts.ansible_local.custom_app.application.environment }}`. Trong đó: `ansible_facts.ansible_local` là không gian tên chung cho Custom Facts, `custom_app` là tên tệp (bỏ đuôi `.fact`), `application` là tên section, và `environment` là tên key.
**Tiêu chí chấm:**
- 0: Viết sai cú pháp không gian tên.
- 1: Thiếu thành phần `ansible_local` hoặc thiếu tên section.
- 2: Phân tích chính xác cấu trúc 4 thành phần trong đường dẫn biến `ansible_local`.
- 3: Nêu đúng + viết đoạn mã YAML dùng `debug` in giá trị biến custom fact này.
**Câu hỏi đào sâu:** Nếu tệp `custom_app.fact` được viết ở định dạng JSON `{ "environment": "production" }` (không có section INI), cú pháp trích xuất sẽ ra sao? *(Cú pháp: `{{ ansible_facts.ansible_local.custom_app.environment }}`.)*

---

### Câu 7 — Tái thu thập Facts bằng Module `setup` ở Giữa Playbook 🔥
**Hỏi:** Tại sao sau khi chép một file Custom Fact mới ở Task 1, ta bắt buộc phải gọi module `ansible.builtin.setup` ở Task 2 trước khi đọc biến `ansible_local` ở Task 3? *(Liên quan QT 6.2)*
**Đáp án chuẩn:** Vì bước `Gathering Facts` tự động ở đầu Play diễn ra TRƯỚC khi Task 1 được thực thi, nên tại thời điểm đó tệp Custom Fact mới chưa tồn tại trên máy đích. Bắt buộc phải gọi trực tiếp module `setup` (với `filter: "ansible_local"`) ở Task 2 để ép Ansible quét lại và nạp dữ liệu Custom Fact mới vừa tạo vào bộ nhớ Host Scope trước khi Task 3 sử dụng.
**Tiêu chí chấm:**
- 0: Cho rằng Ansible tự động phát hiện file mới mà không cần gọi module `setup`.
- 1: Biết cần gọi `setup` nhưng không giải thích được dòng thời gian (timeline) thu thập facts.
- 2: Phân tích chính xác mốc thời gian thu thập facts ở đầu Play và vai trò tái thu thập của module `setup`.
- 3: Nêu đúng + viết đoạn mã YAML minh họa chuỗi 3 task tạo file -> setup -> debug.
**Câu hỏi đào sâu:** Cờ `filter: "ansible_local"` trong module `setup` ở Task 2 có tác dụng gì? *(Giúp module setup chỉ quét lại duy nhất nhóm Custom Facts, không quét lại toàn bộ phần cứng/mạng để tiết kiệm thời gian.)*

---

### Câu 8 — Cơ chế Fact Caching trong Ansible
**Hỏi:** Fact Caching là gì? Cấu hình Fact Caching trong `ansible.cfg` đem lại lợi ích gì cho hạ tầng quy mô lớn? *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Fact Caching là cơ chế lưu trữ đệm dữ liệu facts của máy đích vào đĩa cứng (JSONFile) hoặc bộ nhớ (Redis) trên Control Node trong một khoảng thời gian quy định (`fact_caching_timeout`). Lợi ích: Giúp các lượt chạy Playbook tiếp theo nạp trực tiếp facts từ đệm mà KHÔNG cần gửi module `setup` qua SSH, giúp hạ tầng hàng ngàn máy chủ khởi chạy Playbook tức thì.
**Tiêu chí chấm:**
- 0: Không biết cơ chế Fact Caching.
- 1: Biết lưu đệm nhưng không nêu được các kiểu backend kết nối (`jsonfile`, `redis`).
- 2: Phân tích chính xác cơ chế hoạt động và lợi ích giảm tải kết nối SSH trên hạ tầng lớn.
- 3: Nêu đúng + viết đoạn cấu hình `[defaults]` trong file `ansible.cfg` kích hoạt JSONFile Caching.
**Câu hỏi đào sâu:** Rủi ro lớn nhất khi đặt thời gian `fact_caching_timeout` quá dài (ví dụ 1 tháng) là gì? *(Rủi ro Stale Cache: Khi máy đích bị thay đổi IP hay nâng cấp phần cứng, Ansible vẫn dùng dữ liệu cũ trong cache dẫn tới cấu hình sai.)*

---

### Câu 9 — Phương pháp Kiểm chứng Idempotency và Máy đúng khi dùng Facts 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook sử dụng Custom Facts để đảm bảo tính Idempotency và máy đích ở đúng trạng thái.
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site.yml` để tạo file Custom Fact và áp đặt cấu hình theo facts.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`**.
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/ansible/facts.d/custom_app.fact` kiểm tra nội dung file facts và các file cấu hình ăn theo trên đĩa cứng máy đích.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc bước đối soát `docker exec`.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI cụ thể.
- 3: Trình bày xuất sắc 3 bước + cho ví dụ thực tế lệnh `docker exec` đối soát cả file `.fact` và file sản phẩm trên máy đích.
**Câu hỏi đào sâu:** Nếu lượt chạy Lần 2 báo `changed=1` ở task chép file Custom Fact, nguyên nhân gốc rễ có thể là gì? *(Do nội dung file `.fact` bị thay đổi liên tục theo thời gian thực như lệnh date mà không cố định.)*

---

### Câu 10 — Phân quyền An toàn cho Thư mục Custom Facts ★★★
**Hỏi:** Tại sao việc kiểm soát phân quyền (Permissions) cho thư mục `/etc/ansible/facts.d/` và các tệp script `.fact` lại là yêu cầu bắt buộc về bảo mật? *(Liên quan QT 6.3)*
**Đáp án chuẩn:** Vì khi Playbook chạy với quyền `become: true`, module `setup` sẽ thi hành tất cả các script trong `/etc/ansible/facts.d/` dưới quyền root. Nếu thư mục hoặc script `.fact` bị phân quyền quá rộng (như `0777`), kẻ tấn công có thể chèn mã độc vào script `.fact` để chiếm quyền điều khiển root toàn bộ máy chủ (nguy cơ Privilege Escalation). Bắt buộc phải sở hữu bởi `root:root` và phân quyền tối đa `0755`.
**Tiêu chí chấm:**
- 0: Không quan tâm đến phân quyền file Custom Facts.
- 1: Biết cần phân quyền nhưng không giải thích được rủi ro leo thang quyền lực root.
- 2: Phân tích chính xác nguy cơ leo thang quyền lực khi Ansible chạy `setup` với `become: true`.
- 3: Nêu đúng + đưa ra bộ thông số phân quyền chuẩn (`0755` cho thư mục/script, `0644` cho tệp tĩnh).
**Câu hỏi đào sâu:** Làm thế nào để đảm bảo thư mục `/etc/ansible/facts.d/` luôn có phân quyền an toàn trong Playbook? *(Dùng module `ansible.builtin.file` khai báo `owner: root`, `group: root`, `mode: '0755'` trước khi chép file.)*

---

### Câu 11 — Ứng dụng Facts trong Kịch bản Multi-OS (Ubuntu vs RHEL) ★★★
**Hỏi:** Viết một đoạn Playbook YAML sử dụng `ansible_facts.os_family` để tự động cài đặt đúng gói dịch vụ Web và khởi chạy dịch vụ tương ứng trên cả 2 dòng OS Debian và RedHat.
**Đáp án chuẩn:**
```yaml
---
- name: Multi-OS Web Server Deployment
  hosts: all
  become: true
  tasks:
    - name: Set package name based on OS family
      ansible.builtin.set_fact:
        web_pkg: "{{ 'httpd' if ansible_facts.os_family == 'RedHat' else 'nginx' }}"

    - name: Ensure web package is installed
      ansible.builtin.package:
        name: "{{ web_pkg }}"
        state: present

    - name: Ensure web service is running
      ansible.builtin.service:
        name: "{{ web_pkg }}"
        state: started
        enabled: true
```
**Tiêu chí chấm:**
- 0: Không viết được kịch bản theo OS family.
- 1: Viết được lệnh cài đặt nhưng dùng 2 task riêng lẻ rườm rà với mệnh đề `when`.
- 2: Viết kịch bản ngắn gọn sử dụng `set_fact` và biểu thức điều kiện Jinja2 dựa trên `ansible_facts.os_family`.
- 3: Trình bày xuất sắc + giải thích tính ưu việt của việc dùng `ansible_facts` giúp 1 Playbook chạy thành công trên 100% các dòng Linux.
**Câu hỏi đào sâu:** Tên `os_family` của hệ điều hành CentOS 7 và AlmaLinux 9 trong `ansible_facts` là gì? *(Cả hai đều trả về chuỗi `"RedHat"`.)*

---

### Câu 12 — Tổng kết 5 Quy tắc Vàng khi Quản lý Ansible Facts ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên khai thác Ansible Facts hiệu quả và an toàn nhất trong môi trường Doanh nghiệp.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Luôn dùng cú pháp mới `ansible_facts.<property>` thay cho biến legacy cũ.
2. **Quy tắc 2:** Sử dụng `gather_subset` hoặc `gather_facts: false` để tối ưu tốc độ cho Playbook tác động lớn.
3. **Quy tắc 3:** Đặt Custom Facts chuẩn đường dẫn `/etc/ansible/facts.d/*.fact` và cấp `chmod +x` cho script động.
4. **Quy tắc 4:** Bắt buộc gọi module `setup: filter=ansible_local` tái nạp facts sau khi tạo mới file `.fact`.
5. **Quy tắc 5:** Kiểm soát phân quyền an toàn `root:root 0755/0644` cho thư mục facts và đối soát Lần 2 `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy làm chủ công nghệ tự động hóa chuyên nghiệp.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào đảm bảo hiệu năng (performance) tốt nhất cho Playbook? *(Quy tắc 2: Tối ưu thu thập facts bằng gather_subset hoặc gather_facts: false.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm khai thác Ansible Facts và Custom Facts, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi coi Ansible Facts là bức ảnh chụp thực tế hạ tầng giúp Playbook tự động đưa ra quyết định chính xác 100% mà không phụ thuộc vào khai báo thủ công. Tôi làm chủ kỹ thuật trích xuất `ansible_facts`, tối ưu tốc độ thực thi qua `gather_subset`, và tự thiết kế các Custom Facts tĩnh lẫn động trong `/etc/ansible/facts.d/` để gắn nhãn quản trị doanh nghiệp qua `ansible_local`. Mọi kịch bản dùng facts của tôi đều đảm bảo tiêu chí phân quyền an toàn `0755/0644`, tuân thủ Phép thử Lượt chạy Lần hai `changed=0`, và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Đỗ Văn N | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Hoàng Thị P | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 09

Để chuẩn bị tốt nhất cho **Buổi 09: Conditionals — when, tests, failed_when**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Mệnh đề `when` trong Ansible có tác dụng gì? Nó được đánh giá trước hay sau khi Task thực thi?
2. **Nghiên cứu trước 2:** Làm thế nào để kết hợp nhiều điều kiện rẽ nhánh bằng các toán tử `and`, `or`, `not` trong mệnh đề `when`?
3. **Nghiên cứu trước 3:** Phân biệt sự khác nhau về mục đích sử dụng giữa thuộc tính `when` và thuộc tính `failed_when`.

---


### [Chuyên Đề 09] Điều Khiển Luồng Với Conditionals (when): Phép So Sánh Logic, Kiểm Tra Trạng Thái Biến & Kỹ Thuật Bỏ Qua Task

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Mệnh đề <code>when</code> trong Ansible Playbook có tác dụng gì? Nó được đánh giá tại thời điểm nào trong chu trình thi hành Task? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b> Mệnh đề <code>when</code> cho phép đưa ra quyết định rẽ nhánh logic: Task chỉ được thực thi trên máy đích nếu biểu thức điều kiện sau <code>when:</code> đánh giá kết quả là <code>TRUE</code>. Mệnh đề <code>when</code> được Ansible Engine đánh giá ngay tại thời điểm runtime TRƯỚC KHU TASK ĐƯỢC GỬI THI HÀNH trên máy đích. Nếu điều kiện đánh giá <code>FALSE</code>, Task lập tức bị bỏ qua với trạng thái <code>skipped</code>.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết tác dụng của <code>when</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết <code>when</code> rẽ nhánh nhưng không giải thích được mốc thời gian đánh giá runtime trước khi chạy task.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò rẽ nhánh + thời điểm đánh giá runtime trên từng host.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ rẽ nhánh cài đặt gói theo <code>ansible_facts.os_family</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Mệnh đề <code>when</code> được đánh giá trên Control Node hay trên Managed Node? *(Được đánh giá trên Control Node dựa trên dữ liệu facts/biến của host đó.)*
</div>
</details>

---

### Câu 2 — Quy tắc Cấm bọc `{{ }}` trong `when` 🔥
**Hỏi:** Tại sao việc bọc cặp dấu ngoặc nhọn Jinja2 `{{ }}` bên trong từ khóa `when:` (ví dụ `when: "{{ var == 'val' }}"`) bị coi là sai cú pháp chuẩn? *(Liên quan QT 4.2)*
**Đáp án chuẩn:** Vì bản thân từ khóa `when:` đã tự động được Ansible Engine đặt sẵn trong môi trường biểu thức Jinja2 thô. Việc chèn thêm cặp ngoặc nhọn `{{ }}` bên trong sẽ làm Ansible hiểu nhầm là truyền một chuỗi mẫu template thô, dẫn đến cảnh báo `Bare variable warning` hoặc lỗi parse syntax làm sai lệch kết quả so sánh logic.
**Tiêu chí chấm:**
- 0: Cho rằng phải bọc `{{ }}` mới đúng cú pháp.
- 1: Biết không bọc `{{ }}` nhưng không giải thích được cơ chế parser Jinja2 thô của từ khóa `when`.
- 2: Phân tích chính xác lý do từ khóa `when` tự động xử lý môi trường Jinja2 thô.
- 3: Nêu đúng + viết ví dụ so sánh mã ĐÚNG và SAI trực quan.
**Câu hỏi đào sâu:** Ngoại lệ duy nhất nào cho phép bọc ngoặc kép `""` ở mệnh đề `when`? *(Bọc ngoặc kép toàn bộ chuỗi bên ngoài cùng để tránh lỗi YAML khi chuỗi chứa ký tự đặc biệt như dấu hai chấm.)*

---

### Câu 3 — Biểu diễn Toán tử Logic AND / OR / NOT 🔥
**Hỏi:** Trình bày 2 cách biểu diễn phép toán điều kiện AND trong mệnh đề `when`. Cách nào được khuyến khích trong thực tế? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- **Cách 1 (Toán tử `and` trên 1 dòng):** `when: cond1 and cond2 and cond3`.
- **Cách 2 (Mảng danh sách YAML - KHUYẾN KHÍCH):**
  ```yaml
  when:
    - cond1
    - cond2
    - cond3
  ```
Cách 2 được khuyến khích tuyệt đối trong thực tế vì trình bày dạng mảng danh sách rõ ràng, dễ đọc, dễ bảo trì và loại bỏ hoàn toàn nguy cơ nhầm lẫn thứ tự ưu tiên phép toán.
**Tiêu chí chấm:**
- 0: Không biết biểu diễn phép toán AND.
- 1: Biết gõ từ khóa `and` nhưng không biết cách biểu diễn mảng danh sách YAML.
- 2: Phân tích chính xác cả 2 cách + lý do chọn mảng danh sách theo chuẩn DevOps.
- 3: Nêu đúng + viết ví dụ kết hợp cả `and`, `or`, `not` có ngoặc đơn phân nhóm ưu tiên.
**Câu hỏi đào sâu:** Mảng danh sách các điều kiện bên dưới `when:` đại diện cho phép toán AND hay phép toán OR? *(Đại diện cho phép toán AND 100%.)*

---

### Câu 4 — Kỹ thuật Kiểm tra Biến với `is defined` 🔥
**Hỏi:** Jinja2 Test `is defined` được dùng trong trường hợp nào? Nếu truy xuất một biến chưa khai báo mà KHÔNG dùng `is defined`, điều gì sẽ xảy ra? *(Liên quan QT 5.1)*
**Đáp án chuẩn:** `is defined` được dùng để kiểm tra xem một biến tùy chọn (Optional variable) đã được khai báo hay chưa trước khi đọc giá trị của nó (ví dụ `when: custom_port is defined`). Nếu truy xuất một biến chưa bao giờ được khai báo mà KHÔNG dùng `is defined`, Ansible sẽ ném lỗi fatal `undefined variable` và làm dừng thi hành toàn bộ Playbook lập tức.
**Tiêu chí chấm:**
- 0: Không biết Jinja2 Test `is defined`.
- 1: Biết `is defined` kiểm tra biến nhưng không nêu được rủi ro văng lỗi fatal khi thiếu nó.
- 2: Phân tích chính xác vai trò phòng chống lỗi fatal undefined variable của `is defined`.
- 3: Nêu đúng + cho ví dụ thực tế cài đặt cổng dịch vụ tùy chỉnh với `is defined`.
**Câu hỏi đào sâu:** Phân biệt sự khác nhau giữa `when: my_var is defined` và `when: my_var`? *(is defined chỉ kiểm tra biến CÓ TỒN TẠI HAY KHÔNG; when: my_var vừa kiểm tra tồn tại vừa kiểm tra giá trị của biến có phải là TRUE/non-empty hay không.)*

---

### Câu 5 — Đánh giá Trạng thái Task trước với `is succeeded` / `is failed`
**Hỏi:** Trình bày cơ chế xây dựng Luồng phục hồi lỗi (Recovery Flow) kết hợp giữa thuộc tính `register` và Jinja2 Test `is failed`. *(Liên quan QT 5.2)*
**Đáp án chuẩn:** Quy trình 2 bước:
1. **Task chính:** Đăng ký kết quả chạy bằng `register: primary_res` và thêm `ignore_errors: true` để không dừng Playbook nếu bị lỗi.
2. **Task phục hồi (Fallback):** Khai báo mệnh đề `when: primary_res is failed`. Task phục hồi này CHỈ THỰC THI khi Task chính bị thất bại, giúp hệ thống tự động chuyển sang phương án dự phòng an toàn.
**Tiêu chí chấm:**
- 0: Không biết cách bắt lỗi để chạy task phục hồi.
- 1: Biết dùng `register` nhưng không biết các test `is failed` / `is succeeded`.
- 2: Trình bày chính xác luồng 2 bước kết hợp `register`, `ignore_errors`, và `is failed`.
- 3: Nêu đúng + viết đoạn YAML hoàn chỉnh thử nghiệm chạy script primary fail -> fallback run.
**Câu hỏi đào sâu:** Ngoài `is failed` và `is succeeded`, Ansible còn hỗ trợ các Jinja2 Status Tests nào khác? *(`is skipped`, `is changed`, `is finished`.)*

---

### Câu 6 — Kiểm tra Hệ thống Tệp tin với Jinja2 File Tests
**Hỏi:** Nêu 3 Jinja2 File Tests thường dùng để kiểm tra trạng thái tệp tin/thư mục trên đĩa cứng máy đích. Cho ví dụ. *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
1. `is file`: Kiểm tra đường dẫn có phải là một tệp tin thông thường (ví dụ `when: "'/etc/app.conf' is file"`).
2. `is directory`: Kiểm tra đường dẫn có phải là một thư mục (ví dụ `when: "'/var/log/app' is directory"`).
3. `is mount`: Kiểm tra đường dẫn có phải là một điểm mount đĩa cứng (ví dụ `when: "'/mnt/data' is mount"`).
**Tiêu chí chấm:**
- 0: Không biết các Jinja2 File Tests.
- 1: Liệt kê được 1 test nhưng viết sai cú pháp.
- 2: Phân tích chính xác cả 3 File Tests `is file`, `is directory`, `is mount`.
- 3: Nêu đúng + viết ví dụ Playbook rẽ nhánh chép file chỉ khi thư mục đích đã tồn tại.
**Câu hỏi đào sâu:** Để sử dụng các File Tests này một cách chính xác nhất, ta nên kết hợp với module thu thập thông số nào trước đó? *(Kết hợp với module `ansible.builtin.stat` để lấy thông số đĩa cứng.)*

---

### Câu 7 — Gom nhóm Task Rẽ nhánh bằng `block:` 🔥
**Hỏi:** Việc sử dụng khối `block:` kết hợp với mệnh đề `when:` mang lại lợi ích gì cho việc thiết kế mã nguồn Playbook? *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Khối `block:` cho phép nhóm nhiều Task có chung logic hoạt động lại với nhau và chỉ cần khai báo thuộc tính `when:` **duy nhất 1 lần ở cấp độ Block**. Tất cả các Task bên trong Block sẽ tự động thừa hưởng điều kiện `when` đó. Lợi ích: Giúp mã nguồn ngắn gọn, loại bỏ lặp lại mã (DRY principle) và dễ dàng quản lý luồng rẽ nhánh theo hạ tầng.
**Tiêu chí chấm:**
- 0: Không biết cấu trúc `block:`.
- 1: Biết `block` nhưng lặp lại thuộc tính `when` ở từng task bên trong.
- 2: Phân tích chính xác lợi ích thừa hưởng điều kiện `when` ở cấp độ Block.
- 3: Nêu đúng + viết đoạn mã YAML minh họa Block cấu hình dành riêng cho hệ điều hành RedHat.
**Câu hỏi đào sâu:** Nếu một Task bên trong Block có khai báo thêm mệnh đề `when` riêng, Ansible sẽ xử lý ra sao? *(Task đó phải thỏa mãn CẢ điều kiện của Block VÀ điều kiện riêng của Task thì mới được thực thi.)*

---

### Câu 8 — Quản lý Trạng thái `skipped` trong Bảng `PLAY RECAP`
**Hỏi:** Tại sao một Playbook có nhiều Task bị `skipped` ở lượt chạy Lần 2 nhưng vẫn được kết luận là ĐẠT chuẩn Idempotency 100%? *(Liên quan QT 6.2)*
**Đáp án chuẩn:** Vì chỉ số `skipped` trong bảng `PLAY RECAP` chỉ phản ánh số lượng Task rẽ nhánh bị bỏ qua do điều kiện `when` đánh giá FALSE. Việc bỏ qua một Task KHÔNG LÀM THAY ĐỔI bất kỳ byte nào trên đĩa cứng máy đích. Tiêu chuẩn nghiệm thu Idempotency chỉ căn cứ duy nhất vào chỉ số `changed=0` ở lượt chạy Lần 2. Do đó `skipped=N, changed=0` hoàn toàn đạt chuẩn Idempotency tuyệt đối.
**Tiêu chí chấm:**
- 0: Lầm tưởng `skipped > 0` là Playbook bị lỗi không đạt Idempotency.
- 1: Biết `skipped` là bỏ qua nhưng không giải thích được lý do tại sao nó không ảnh hưởng `changed=0`.
- 2: Phân tích chính xác bản chất chỉ số `skipped` và khẳng định tiêu chuẩn `changed=0` ở Lần 2.
- 3: Nêu đúng + minh họa bảng `PLAY RECAP` chuẩn chứa chỉ số `skipped`.
**Câu hỏi đào sâu:** Chỉ số `skipped` có làm tăng thời gian chạy Playbook nhiều không? *(Không, task bị skipped được bỏ qua gần như tức thì trong vài milisecond.)*

---

### Câu 9 — Cạm bẫy Bắt Biến `register` của Task bị `skipped` 🔥
**Hỏi:** Tại sao việc đọc `register_var.stdout` của một Task vừa bị `skipped` lại khiến Playbook bị văng lỗi fatal? Làm sao để xử lý an toàn? *(Liên quan QT 6.3)*
**Đáp án chuẩn:** Khi một Task bị `skipped`, Ansible vẫn khởi tạo biến đăng ký `register_var` nhưng CHỈ GÁN thuộc tính `skipped: true` chứ KHÔNG THỰC THI LỆNH để tạo ra trường `stdout`. Truy xuất `register_var.stdout` sẽ bị lỗi `undefined attribute`. Cách xử lý an toàn: Bổ sung điều kiện `when: register_var is succeeded` (hoặc `when: register_var.stdout is defined`) ở Task đằng sau trước khi đọc.
**Tiêu chí chấm:**
- 0: Không biết bẫy lỗi này.
- 1: Biết bị lỗi nhưng không giải thích được tại sao task skipped lại không có trường `stdout`.
- 2: Phân tích chính xác cơ chế tạo biến register khi skipped + giải pháp bọc `is succeeded`.
- 3: Nêu đúng + viết đoạn mã YAML minh họa cạm bẫy và cách xử lý chuẩn hóa.
**Câu hỏi đào sâu:** Nếu Task A bị skipped, thuộc tính `register_var.changed` sẽ có giá trị là gì? *(Có giá trị là `false`.)*

---

### Câu 10 — Phương pháp Chứng minh Idempotency và Máy đúng khi Rẽ nhánh 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook có sử dụng mệnh đề `when` rẽ nhánh để đảm bảo tính Idempotency và máy đích ở đúng trạng thái.
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook -e "target_env=production" site.yml` để áp đặt cấu hình theo nhánh production.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn lệnh CLI đó Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (chỉ số `skipped` giữ nguyên).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/production.conf` kiểm tra file sản phẩm của nhánh production thực sự tồn tại trên đĩa cứng máy đích, không dừng lại ở màn hình terminal.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là đủ" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc bước đối soát `docker exec`.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI cụ thể.
- 3: Trình bày xuất sắc 3 bước + cho ví dụ thực tế lệnh `docker exec` đối soát file được tạo bởi mệnh đề `when`.
**Câu hỏi đào sâu:** Nếu ở Lần 2 ta đổi cờ Extra Vars thành `-e "target_env=staging"`, chỉ số RECAP Lần 2 sẽ ra sao? *(RECAP Lần 2 sẽ báo `changed > 0` do Playbook thực thi nhánh staging mới và bỏ qua nhánh production.)*

---

### Câu 11 — Kỹ thuật Rẽ nhánh theo Thông tin Facts OS ★★★
**Hỏi:** Viết một đoạn Playbook YAML sử dụng `ansible_facts.os_family` kết hợp mệnh đề `when` để tự động chép file cấu hình thích hợp (`/etc/httpd/conf/httpd.conf` cho RedHat, `/etc/nginx/nginx.conf` cho Debian).
**Đáp án chuẩn:**
```yaml
---
- name: OS Family Conditional Configuration
  hosts: web
  become: true
  tasks:
    - name: Deploy Httpd Config on RedHat Family
      ansible.builtin.copy:
        src: files/httpd.conf
        dest: /etc/httpd/conf/httpd.conf
        mode: '0644'
      when: ansible_facts.os_family == "RedHat"

    - name: Deploy Nginx Config on Debian Family
      ansible.builtin.copy:
        src: files/nginx.conf
        dest: /etc/nginx/nginx.conf
        mode: '0644'
      when: ansible_facts.os_family == "Debian"
```
**Tiêu chí chấm:**
- 0: Không viết được kịch bản rẽ nhánh theo `os_family`.
- 1: Viết được kịch bản nhưng bọc ngoặc nhọn `{{ }}` sai cú pháp trong mệnh đề `when`.
- 2: Viết kịch bản chuẩn xác rẽ nhánh theo `os_family` cho 2 dòng OS.
- 3: Trình bày xuất sắc + giải thích tính an toàn khi 1 host chạy chỉ có 1 task thực thi và 1 task bị skipped.
**Câu hỏi đào sâu:** Nếu Playbook chạy trên hệ điều hành Alpine Linux (`os_family == "Alpine"`), cả 2 task trên sẽ ra sao? *(Cả 2 task sẽ đều bị skipped vì không thỏa mãn cả 2 điều kiện.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng khi Dùng Mệnh đề `when` ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên sử dụng mệnh đề `when` hiệu quả, an toàn và sạch sẽ nhất trong Ansible.
**Đáp án chuẩn:**
1. **Quy tắc 1:** KHÔNG bọc cặp dấu ngoặc nhọn `{{ }}` bên trong từ khóa `when:`.
2. **Quy tắc 2:** Ưu tiên dùng mảng danh sách YAML thay cho phép toán `and` dài trên 1 dòng.
3. **Quy tắc 3:** Luôn bọc `is defined` kiểm tra sự tồn tại trước khi đọc các biến tùy chọn.
4. **Quy tắc 4:** Sử dụng `block:` để gom nhóm các Task có cùng điều kiện rẽ nhánh (DRY principle).
5. **Quy tắc 5:** Kiểm tra `is succeeded` trước khi đọc `stdout` của biến `register` và đối soát Lần 2 `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy thiết kế Playbook thông minh chuyên nghiệp.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp ngăn chặn các lỗi crash Playbook phổ biến nhất? *(Quy tắc 1 và Quy tắc 3.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kỹ năng thiết kế kịch bản rẽ nhánh linh hoạt trong Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi sử dụng mệnh đề `when` và các Jinja2 Tests để xây dựng những Playbook thông minh có khả năng tự động thích ứng trên 100% hạ tầng đa dạng mà không cần duy trì nhiều file mã nguồn lặp lại. Tôi tuân thủ nghiêm ngặt quy tắc không bọc `{{ }}` trong `when`, biểu diễn toán tử AND bằng mảng danh sách clean-code, phòng chống lỗi undefined bằng `is defined`, và gom nhóm task bằng `block`. Mọi kịch bản rẽ nhánh của tôi đều được kiểm soát trạng thái `skipped` minh bạch, đảm bảo Phép thử Lượt chạy Lần hai đạt `changed=0`, và đối soát sự thật thực tế trên máy đích qua `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Ngô Văn Q | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Trần Thị R | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 10

Để chuẩn bị tốt nhất cho **Buổi 10: Loops — loop, loop_control, with_items**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Từ khóa `loop` trong Ansible dùng để làm gì? Biến mặc định chứa phần tử hiện tại của vòng lặp tên là gì?
2. **Nghiên cứu trước 2:** Phân biệt sự khác nhau giữa từ khóa lặp hiện đại `loop` và từ khóa lặp legacy `with_items`.
3. **Nghiên cứu trước 3:** Từ khóa `loop_control` hỗ trợ đổi tên biến phần tử lặp (`loop_var`) và hiển thị nhãn lặp (`label`) như thế nào?

---


### [Chuyên Đề 10] Vòng Lặp Nâng Cao (Loops): loop, with_items, loop_control (label/pause) & Xử Lý Danh Sách / Từ Điển Đa Tầng

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Từ khóa <code>loop:</code> trong Ansible Playbook dùng để làm gì? Phân biệt sự khác nhau giữa <code>loop:</code> hiện đại và <code>with_items:</code> legacy. *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b> Từ khóa <code>loop:</code> dùng để lặp qua một danh sách các phần tử (List hoặc List of Dictionaries) nhằm thực thi cùng 1 Task nhiều lần với dữ liệu khác nhau, giúp rút gọn mã nguồn. Phân biệt: <code>loop:</code> là cú pháp chuẩn hiện đại (từ bản 2.5+) duyệt danh sách trực tiếp và ít bị lỗi xung đột; <code>with_items:</code> là cú pháp legacy cũ tự động phẳng hóa (flatten) mảng 2 chiều và sắp bị loại bỏ ở các bản mới.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết từ khóa <code>loop:</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết <code>loop:</code> để lặp nhưng không phân biệt được với <code>with_items:</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò rút gọn mã của <code>loop:</code> và sự khác biệt về phẳng hóa mảng với <code>with_items:</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ cài đặt 4 gói phần mềm bằng 1 Task <code>loop:</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu truyền một mảng 2 chiều <code>[[a, b], [c, d]]</code> vào <code>loop:</code>, Ansible sẽ lặp thế nào? *(Ansible lặp 2 lượt: lượt 1 item=[a, b], lượt 2 item=[c, d]; muốn phẳng hóa phải dùng filter <code>loop: "{{ list | flatten }}"</code>.)*
</div>
</details>

---

### Câu 2 — Biến Phần tử Lặp Mặc định `{{ item }}` 🔥
**Hỏi:** Biến `{{ item }}` trong Task vòng lặp đóng vai trò gì? Cách trích xuất dữ liệu khi danh sách lặp là chuỗi thô vs khi danh sách lặp là Dictionary. *(Liên quan QT 4.2)*
**Đáp án chuẩn:** Biến `{{ item }}` là con trỏ mặc định đại diện cho phần tử của lượt lặp hiện tại.
- Khi danh sách là chuỗi thô (`[curl, git]`): Trích xuất trực tiếp `{{ item }}` (trả về chuỗi `"curl"` hoặc `"git"`).
- Khi danh sách là Dictionary (`[{name: 'alice', uid: 2001}]`): Trích xuất thuộc tính qua dấu chấm `{{ item.name }}` hoặc `{{ item.uid }}`.
**Tiêu chí chấm:**
- 0: Không biết biến `{{ item }}`.
- 1: Biết `item` nhưng không trích xuất được thuộc tính Dictionary `item.key`.
- 2: Phân tích chính xác cơ chế của con trỏ `item` trong cả 2 trường hợp chuỗi thô và Dictionary.
- 3: Nêu đúng + viết đoạn YAML minh họa tạo user với `{{ item.username }}` và `{{ item.shell }}`.
**Câu hỏi đào sâu:** Nếu trong Task không khai báo từ khóa `loop:` mà gọi biến `{{ item }}`, Ansible sẽ báo lỗi gì? *(Báo lỗi fatal: 'item' is undefined.)*

---

### Câu 3 — Đổi Tên Biến Lặp với `loop_control.loop_var` 🔥
**Hỏi:** Tại sao phải sử dụng thuộc tính `loop_control.loop_var` để đổi tên biến lặp mặc định `item`? Cho ví dụ thực tế. *(Liên quan QT 5.1)*
**Đáp án chuẩn:** Bắt buộc phải dùng `loop_control.loop_var` để đổi tên biến `item` (ví dụ `loop_var: outer_item`) khi có 2 vòng lặp lồng nhau (Nested loops) hoặc khi gọi task phụ trong vòng lặp. Nếu không đổi tên, vòng lặp bên trong sẽ ghi đè lên biến `item` của vòng lặp bên ngoài làm mất dữ liệu và crash Playbook.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `loop_control.loop_var`.
- 1: Biết `loop_var` đổi tên nhưng không giải thích được rủi ro xung đột ghi đè biến ở vòng lặp lồng nhau.
- 2: Phân tích chính xác hiện tượng xung đột biến `item` và giải pháp đổi tên bằng `loop_var`.
- 3: Nêu đúng + viết đoạn mã YAML minh họa vòng lặp lồng nhau dùng `loop_var` an toàn.
**Câu hỏi đào sâu:** Sau khi khai báo `loop_control: loop_var: pkg_item`, ta truy xuất phần tử lặp ở thuộc tính module bằng cú pháp nào? *(Cú pháp `{{ pkg_item }}` thay cho `{{ item }}`.)*

---

### Câu 4 — Làm sạch Log Terminal với `loop_control.label` 🔥
**Hỏi:** Thuộc tính `loop_control.label` giải quyết vấn đề gì khi thực thi Task vòng lặp với danh sách Dictionary lớn? *(Liên quan QT 5.2)*
**Đáp án chuẩn:** Khi lặp qua một danh sách Dictionary chứa nhiều thuộc tính dài (như SSH public key, password hash), mặc định Ansible sẽ in toàn bộ Dictionary thô ra terminal khiến nhật ký log bị rối mắt và dễ lộ thông tin nhạy cảm. Thuộc tính `loop_control.label: "{{ item.username }}"` ép terminal chỉ in ra giá trị nhãn đại diện ngắn gọn (như `=> (item=alice)`).
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `loop_control.label`.
- 1: Biết `label` làm ngắn log nhưng không biết cú pháp gán nhãn `label: "{{ item.name }}"`.
- 2: Phân tích chính xác tác dụng làm sạch log và bảo mật thông tin của `label`.
- 3: Nêu đúng + so sánh mẫu log terminal trước và sau khi dùng `label`.
**Câu hỏi đào sâu:** Nếu gán `loop_control: label: null`, màn hình terminal sẽ hiển thị log các phần tử lặp ra sao? *(Nó sẽ ẩn hoàn toàn thông tin phần tử lặp, chỉ in duy nhất trạng thái ok/changed.)*

---

### Câu 5 — Đánh số Chỉ số đếm với `loop_control.index_var`
**Hỏi:** Thuộc tính `loop_control.index_var` được sử dụng trong trường hợp nào? Chỉ số đếm bắt đầu từ số mấy? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** `loop_control.index_var: var_name` dùng để khai báo một biến tự động lưu trữ chỉ số đếm (Index) của lượt lặp hiện tại. Chỉ số đếm **bắt đầu từ số 0** (0, 1, 2...). Ứng dụng: Dùng để đánh số thứ tự file cấu hình (như `worker-0.conf`, `worker-1.conf`), tính toán cổng mạng tăng dần (`8000 + index`), hoặc theo dõi vị trí phần tử trong mảng.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `index_var`.
- 1: Biết `index_var` đếm số nhưng nhầm chỉ số bắt đầu từ số 1.
- 2: Phân tích chính xác cơ chế lưu chỉ số đếm từ 0 và các ứng dụng tính toán cổng/file.
- 3: Nêu đúng + viết đoạn YAML minh họa tạo file worker đính kèm index và cổng `8000 + idx`.
**Câu hỏi đào sâu:** Muốn chỉ số đếm hiển thị bắt đầu từ số 1 thay vì 0, biểu thức Jinja2 sẽ viết thế nào? *(Viết `{{ my_idx + 1 }}`.)*

---

### Câu 6 — Bắt Kết quả Vòng lặp với `register` và mảng `results` 🔥
**Hỏi:** Khi áp dụng thuộc tính `register: reg_var` cho một Task chứa `loop:`, dữ liệu kết quả trả về của các lượt lặp được lưu vào đâu? Làm sao để đọc kết quả này ở Task sau? *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Dữ liệu kết quả của TẤT CẢ các lượt lặp được Ansible đóng gói vào một mảng danh sách có tên `reg_var.results`. Muốn đọc kết quả ở Task sau, **bắt buộc phải dùng một vòng lặp mới duyệt qua `loop: "{{ reg_var.results }}"`**, trong đó từng phần tử lặp chứa `item.item` (phần tử gốc) và `item.stdout` (kết quả lệnh).
**Tiêu chí chấm:**
- 0: Đọc `reg_var.stdout` trực tiếp từ Task vòng lặp (dính bẫy error undefined).
- 1: Biết có mảng `results` nhưng không biết cách duyệt qua `loop: "{{ reg_var.results }}"`.
- 2: Phân tích chính xác cấu trúc mảng `results` và cú pháp duyệt lặp ở Task sau.
- 3: Nêu đúng + viết đoạn mã YAML hoàn chỉnh 2 Task: lặp chạy lệnh -> lặp debug kết quả `results`.
**Câu hỏi đào sâu:** Nếu 1 lượt lặp trong Task vòng lặp bị failed, trường `reg_var.results` có chứa thông tin của lượt lặp đó không? *(Có chứa, từng lượt lặp đều có 1 element tương ứng trong mảng results.)*

---

### Câu 7 — Kết hợp `loop:` và Mệnh đề Điều kiện `when:`
**Hỏi:** Khi một Task chứa cả từ khóa `loop:` và mệnh đề `when:`, Ansible Engine đánh giá điều kiện `when` như thế nào? *(Liên quan QT 6.2)*
**Đáp án chuẩn:** Ansible Engine đánh giá mệnh đề `when` **RIÊNG BIỆT cho từng phần tử lặp `item`** trong danh sách. Phần tử nào thỏa mãn điều kiện `when` sẽ được thực thi; phần tử nào không thỏa mãn sẽ bị bỏ qua riêng lẻ và terminal in log `skipping: [target1] => (item=...)`.
**Tiêu chí chấm:**
- 0: Cho rằng mệnh đề `when` đánh giá 1 lần duy nhất cho toàn bộ Task.
- 1: Biết rẽ nhánh từng phần tử nhưng không giải thích được log skipping riêng biệt.
- 2: Phân tích chính xác cơ chế đánh giá per-item của `when` trong vòng lặp.
- 3: Nêu đúng + viết ví dụ lọc danh sách gói phần mềm chỉ cài đặt những gói có `install: true`.
**Câu hỏi đào sâu:** Chỉ số `skipped` trong RECAP có tăng lên khi có 1 phần tử trong `loop` bị skipped không? *(Không, chỉ số skipped trong RECAP chỉ tăng khi TOÀN BỘ Task bị skipped.)*

---

### Câu 8 — Tối ưu Hiệu năng Module `package` vs `loop:` ★★★
**Hỏi:** Tại sao việc cài đặt 20 gói phần mềm bằng `ansible.builtin.package: name="{{ pkg_list }}"` lại tốt hơn nhiều so với `ansible.builtin.package: name="{{ item }}" loop: "{{ pkg_list }}"`?
**Đáp án chuẩn:**
- Dùng `name: "{{ pkg_list }}"` (không dùng loop): Ansible tự động gom toàn bộ 20 gói vào 1 câu lệnh quản lý gói duy nhất (`apt install pkg1 pkg2 ... pkg20`), chỉ gửi **1 kết nối SSH** và mở package manager đúng **1 lần** (chạy cực nhanh trong 5 giây).
- Dùng `loop:`: Ansible mở **20 kết nối SSH** và gọi package manager **20 lần độc lập** (chạy rất chậm, tốn CPU và có thể mất 2 phút).
**Tiêu chí chấm:**
- 0: Không biết sự khác biệt hiệu năng giữa 2 cách.
- 1: Biết truyền mảng nhanh hơn nhưng không giải thích được cơ chế 1 lệnh SSH vs 20 lệnh SSH.
- 2: Phân tích chính xác bản chất gộp lệnh của package manager vs 20 vòng lặp SSH riêng lẻ.
- 3: Nêu đúng + đưa ra lời khuyên thiết kế Playbook chuẩn performance cho DevOps Engineer.
**Câu hỏi đào sâu:** Khi nào thì ta BẮT BUỘC phải dùng `loop:` thay vì truyền mảng vào `name`? *(Khi mỗi phần tử trong danh sách có các thuộc tính riêng biệt phức tạp như state, version, repository khác nhau.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng `loop:` 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook sử dụng `loop:` để đảm bảo tính Idempotency và máy đích ở đúng trạng thái.
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site.yml` để tạo hàng loạt tài khoản user/file cấu hình theo danh sách `loop:`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (toàn bộ các phần tử lặp báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 id dev1` và `cat` các file cấu hình được sinh ra từ `loop:` để xác nhận sản phẩm thật trên đĩa cứng máy đích.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc bước đối soát `docker exec`.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI cụ thể.
- 3: Trình bày xuất sắc 3 bước + cho ví dụ thực tế lệnh `docker exec id` và `cat` đối soát sản phẩm vòng lặp.
**Câu hỏi đào sâu:** Nếu ở Lần 2 có 1 phần tử trong danh sách `loop:` bị báo `changed=1`, bảng `PLAY RECAP` của Playbook sẽ hiển thị ra sao? *(Bảng RECAP sẽ báo `changed=1`, thể hiện Playbook chưa đạt tính Idempotency.)*

---

### Câu 10 — Lặp Danh sách Dictionary Phức tạp ★★★
**Hỏi:** Viết một đoạn Task YAML sử dụng module `ansible.builtin.user` kết hợp `loop:` để tạo 2 tài khoản user `dev1` và `dev2` với các thuộc tính riêng biệt (username, uid, shell, groups) và dùng `loop_control.label` làm sạch log.
**Đáp án chuẩn:**
```yaml
- name: Create multiple user accounts with custom attributes
  ansible.builtin.user:
    name: "{{ item.username }}"
    uid: "{{ item.uid }}"
    shell: "{{ item.shell }}"
    groups: "{{ item.groups }}"
    state: present
  loop:
    - { username: 'dev1', uid: 3001, shell: '/bin/bash', groups: 'wheel' }
    - { username: 'dev2', uid: 3002, shell: '/bin/sh', groups: 'devs' }
  loop_control:
    label: "{{ item.username }}"
```
**Tiêu chí chấm:**
- 0: Không viết được kịch bản lặp Dictionary.
- 1: Viết được kịch bản nhưng thiếu thuộc tính `loop_control.label` hoặc sai cú pháp Dict YAML.
- 2: Viết kịch bản chuẩn xác lặp Dictionary cho 2 user kèm `loop_control.label`.
- 3: Trình bày xuất sắc + giải thích ý nghĩa của từng thuộc tính trong khối `loop:` và `loop_control:`.
**Câu hỏi đào sâu:** Nếu trong danh sách Dictionary có user thiếu thuộc tính `groups`, làm sao để tránh lỗi undefined? *(Dùng Jinja2 filter default: `groups: "{{ item.groups | default(omit) }}"`.)*

---

### Câu 11 — Tạm dừng Giữa các Lượt lặp với `loop_control.pause` ★★★
**Hỏi:** Thuộc tính `loop_control.pause` được sử dụng trong trường hợp nào? Cho ví dụ.
**Đáp án chuẩn:** `loop_control.pause: <seconds>` dùng để thiết lập thời gian tạm dừng (tính bằng giây) giữa các lượt lặp của Task. Ứng dụng: Dùng khi thực hiện khởi động lại hàng loạt các node trong cụm (Rolling restart / Rolling upgrade), để đảm bảo từng dịch vụ kịp khởi chạy hoàn toàn trước khi tiếp tục restart node tiếp theo, tránh gây ngắt quãng dịch vụ toàn hệ thống.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `pause`.
- 1: Biết `pause` là dừng nhưng không nêu được ứng dụng Rolling Restart trong hạ tầng Production.
- 2: Phân tích chính xác vai trò tạm dừng giữa các lượt lặp + ứng dụng Rolling Restart.
- 3: Nêu đúng + viết đoạn YAML minh họa restart từng instance ứng dụng kèm `pause: 10`.
**Câu hỏi đào sâu:** Cờ `pause` nằm bên trong từ khóa `loop:` hay bên trong khối `loop_control:`? *(Nằm trực tiếp bên trong khối `loop_control:`.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng khi Dùng Vòng lặp `loop:` ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên sử dụng vòng lặp `loop:` hiệu quả, sạch sẽ và đạt tính Idempotency cao nhất.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Sử dụng từ khóa hiện đại `loop:` thay cho `with_items:` legacy.
2. **Quy tắc 2:** Sử dụng `loop_control.label` để làm gọn nhật ký log terminal khi lặp Dictionary.
3. **Quy tắc 3:** Đổi tên biến lặp bằng `loop_control.loop_var` khi có nguy cơ xung đột biến `item`.
4. **Quy tắc 4:** Truy xuất mảng `register_var.results` khi đăng ký kết quả của Task vòng lặp.
5. **Quy tắc 5:** Truyền trực tiếp mảng vào `name` cho module `package` để tối ưu SSH, và kiểm thử Lần 2 `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy làm chủ kỹ thuật tự động hóa chuyên nghiệp.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào giúp bảo mật thông tin nhạy cảm tốt nhất trên log CI/CD? *(Quy tắc 2: Dùng loop_control.label để ẩn các secret key trong Dictionary.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm xử lý vòng lặp và tối ưu hóa Playbook trong Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi sử dụng từ khóa vòng lặp hiện đại `loop:` kết hợp với khối `loop_control` để tối ưu hóa mã nguồn Playbook, rút ngắn hàng chục Task trùng lặp thành các câu lệnh khai báo mảng ngắn gọn và dễ bảo trì. Tôi làm chủ kỹ thuật đổi tên biến lặp bằng `loop_var` để loại bỏ rủi ro xung đột vòng lặp lồng nhau, chuẩn hóa log terminal bằng `label`, và xử lý chính xác mảng `results` của biến đăng ký `register`. Đặc biệt, tôi luôn tối ưu hiệu năng SSH bằng cách truyền mảng trực tiếp cho module `package`, đảm bảo mọi phần tử lặp ở lượt chạy Lần hai đều đạt chỉ số `changed=0`, và đối soát sự thật thực tế trên máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Phan Văn S | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Lê Thị T | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 11

Để chuẩn bị tốt nhất cho **Buổi 11: Handlers và Notify — handlers, notify, listen**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Khái niệm `handlers` trong Ansible Playbook khác `tasks` thường ở điểm nào? Khi nào thì một handler được kích hoạt?
2. **Nghiên cứu trước 2:** Từ khóa `notify:` được sử dụng như thế nào? Nếu file cấu hình KHÔNG bị thay đổi (`changed=false`), handler có chạy không?
3. **Nghiên cứu trước 3:** Tính năng `listen:` trong handlers cho phép nhóm nhiều handler cùng lắng nghe một sự kiện thông báo như thế nào?

---


### [Chuyên Đề 11] Điều Phối Handlers & Notify: Cơ Chế Flush Handlers, Listen Topic & Xử Lý Khởi Động Lại Dịch Vụ Thông Minh

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Cơ chế <code>handlers</code> và từ khóa <code>notify:</code> trong Ansible Playbook có tác dụng gì? Tại sao không nên restart dịch vụ trực tiếp dưới <code>tasks:</code>? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b> Khối <code>handlers:</code> chứa các Task đặc biệt chỉ được kích hoạt thi hành khi nhận được thông báo từ thuộc tính <code>notify:</code> của các Task chính. Không nên restart dịch vụ trực tiếp dưới <code>tasks:</code> vì nó sẽ khiến dịch vụ bị restart vô điều kiện ở mọi lượt chạy kịch bản ngay cả khi tệp cấu hình KHÔNG đổi, gây gián đoạn dịch vụ lãng phí. Dùng <code>notify/handlers</code> đảm bảo dịch vụ CHỈ RESTART khi file cấu hình thực sự có sự thay đổi (<code>changed: true</code>).
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết vai trò của <code>handlers</code> và <code>notify</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết <code>handlers</code> để restart dịch vụ nhưng không giải thích được rủi ro gián đoạn khi đặt restart trong <code>tasks</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò phản ứng sự kiện và điều kiện kích hoạt <code>changed: true</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ chép file cấu hình Nginx phát <code>notify: Restart Nginx</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Khối <code>handlers:</code> nằm cùng cấp thụt lề với từ khóa nào trong file Playbook? *(Nằm ở cấp độ Play, cùng cấp thụt lề với từ khóa <code>tasks:</code>.)*
</div>
</details>

---

### Câu 2 — Điều kiện Bắt buộc Kích hoạt Handler 🔥
**Hỏi:** Điều kiện bắt buộc về trạng thái của Task để thông báo `notify:` đưa được Handler vào hàng chờ thực thi là gì? Ở lượt chạy Lần 2 điều gì sẽ xảy ra? *(Liên quan QT 4.2)*
**Đáp án chuẩn:** Điều kiện bắt buộc: Task chứa `notify:` phải trả về trạng thái **`changed: true`**. Ở lượt chạy Lần 2, khi tệp cấu hình đã trùng khớp hoàn toàn với đĩa cứng, Task báo trạng thái `ok` (`changed: false`), thông báo `notify` bị hủy bỏ và Handler **KHÔNG BỊ KÍCH HOẠT THỪA**, giúp Playbook đạt `changed=0` tuyệt đối.
**Tiêu chí chấm:**
- 0: Nhầm lẫn rằng Handler luôn chạy bất kể Task báo `ok` hay `changed`.
- 1: Biết cần `changed: true` nhưng thắc mắc tại sao lượt 2 Handler lại im lặng không chạy.
- 2: Phân tích chính xác điều kiện `changed: true` và khẳng định hành vi im lặng hợp lệ ở Lần 2.
- 3: Nêu đúng + chứng minh bằng kết quả bảng `PLAY RECAP` ở Lần 1 và Lần 2.
**Câu hỏi đào sâu:** Nếu 1 task dùng module `command` luôn trả về `changed: true`, làm sao để ngăn không cho nó liên tục kích hoạt Handler ở Lần 2? *(Khai báo thuộc tính `changed_when: false` cho task command đó.)*

---

### Câu 3 — Cơ chế Khử trùng lặp (Deduplication) 🔥
**Hỏi:** Giải thích cơ chế Khử trùng lặp (Deduplication) của Handler khi có 5 Task riêng biệt cùng phát thông báo `notify: Restart Nginx`. *(Liên quan QT 4.3)*
**Đáp án chuẩn:** Ansible Engine tự động quản lý một hàng chờ (Queue) các Handler đã được kích hoạt. Mặc định, dù có 5 Task hay 100 Task cùng phát thông báo `notify: Restart Nginx`, Ansible vẫn tự động khử trùng lặp và **CHỈ THỰC THI HANDLER ĐÓ ĐÚNG 1 LẦN DUY NHẤT Ở CUỐI PLAYBOOK** sau khi tất cả các Task chính đã hoàn thành.
**Tiêu chí chấm:**
- 0: Lầm tưởng Handler sẽ bị gọi chạy 5 lần liên tiếp.
- 1: Biết Handler chạy 1 lần nhưng không giải thích được mốc thời gian thi hành ở cuối Playbook.
- 2: Phân tích chính xác cơ chế hàng chờ và khử trùng lặp Deduplication tự động của Ansible.
- 3: Nêu đúng + phân tích lợi ích bảo vệ đĩa cứng và hiệu năng dịch vụ Nginx trong Production.
**Câu hỏi đào sâu:** Nếu 5 Task phát `notify` tới 5 Handler KHÁC NHAU, thứ tự chạy của 5 Handler đó ở cuối Playbook được quyết định bởi thứ tự `notify` hay thứ tự khai báo trong khối `handlers:`? *(Được quyết định bởi thứ tự khai báo trong khối `handlers:`.)*

---

### Câu 4 — Nhóm Handler với Từ khóa `listen:` 🔥
**Hỏi:** Từ khóa `listen:` trong khối `handlers:` dùng để làm gì? Cho ví dụ ứng dụng thực tế. *(Liên quan QT 5.1)*
**Đáp án chuẩn:** Từ khóa `listen: <topic_name>` cho phép định nghĩa một tên chủ đề thông báo chung để nhóm nhiều Handler khác nhau lại với nhau. Khi Task chính phát `notify: <topic_name>`, TẤT CẢ các Handler có khai báo `listen: <topic_name>` sẽ đồng loạt được đưa vào hàng chờ kích hoạt. Ứng dụng: Chỉ cần 1 dòng `notify: reload web stack` là tự động kích hoạt cả Handler restart Nginx và Handler restart PHP-FPM.
**Tiêu chí chấm:**
- 0: Không biết từ khóa `listen:`.
- 1: Biết `listen` nhưng không giải thích được cơ chế nhóm nhiều Handler theo chủ đề.
- 2: Phân tích chính xác vai trò pub/sub topic của `listen:` và lợi ích rút gọn mã `notify`.
- 3: Nêu đúng + viết đoạn YAML minh họa 2 Handler cùng lắng nghe `listen: restart web services`.
**Câu hỏi đào sâu:** Một Handler có thể vừa có thuộc tính `name:` vừa có thuộc tính `listen:` không? *(Có, Task có thể notify theo `name` hoặc notify theo `listen` đều được.)*

---

### Câu 5 — Ép thi hành Handler giữa chừng với `meta: flush_handlers` 🔥
**Hỏi:** Module `ansible.builtin.meta: flush_handlers` dùng để giải quyết vấn đề gì? Cho ví dụ. *(Liên quan QT 5.2)*
**Đáp án chuẩn:** Mặc định Handler sẽ chờ đến tận cuối Playbook mới thi hành. Module `ansible.builtin.meta: flush_handlers` dùng để ép Ansible thi hành NGAY LẬP TỨC toàn bộ các Handler đang nằm trong hàng chờ tại đúng mốc vị trí đó. Ứng dụng: Khi Task 1 sửa file cấu hình Nginx, cần ép Handler restart Nginx chạy ngay để Task 3 phía sau thực hiện test kết nối HTTP thành công.
**Tiêu chí chấm:**
- 0: Không biết module `meta: flush_handlers`.
- 1: Biết `flush_handlers` ép Handler chạy nhưng không giải thích được lý do tại sao phải dùng giữa 2 task.
- 2: Phân tích chính xác cơ chế ép thi hành hàng chờ Handler ngay tại thời điểm gọi.
- 3: Nêu đúng + viết đoạn mã YAML 3 bước: copy config -> flush_handlers -> verify URI test.
**Câu hỏi đào sâu:** Sau khi `flush_handlers` thi hành xong các Handler trong hàng chờ, hàng chờ Handler đó có bị xóa rỗng không? *(Có, hàng chờ được xóa rỗng hoàn toàn.)*

---

### Câu 6 — Bảo vệ Handler với `force_handlers: yes`
**Hỏi:** Điều gì xảy ra với các Handler trong hàng chờ nếu một Task phía sau bị văng lỗi đứt gãy? Làm sao để đảm bảo Handler vẫn được thi hành? *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Mặc định nếu một Task ở giữa Playbook bị crash, Ansible sẽ dừng ngay Playbook và BỎ QUA toàn bộ các Handler đang chờ. Để đảm bảo các Handler trong hàng chờ vẫn được thi hành phục hồi dịch vụ, ta khai báo thuộc tính **`force_handlers: yes`** ở cấp độ Play.
**Tiêu chí chấm:**
- 0: Không biết rủi ro bỏ qua Handler khi task sau crash.
- 1: Biết bị bỏ qua nhưng không nêu được tên thuộc tính `force_handlers: yes`.
- 2: Phân tích chính xác cơ chế hủy hàng chờ mặc định và giải pháp bọc `force_handlers: yes`.
- 3: Nêu đúng + minh họa ví dụ thực tế bảo vệ file cấu hình bảo mật hệ thống.
**Câu hỏi đào sâu:** Khai báo `force_handlers: yes` ở vị trí nào trong file Playbook? *(Khai báo ở cấp độ Play, cùng cấp thụt lề với `hosts:` và `tasks:`.)*

---

### Câu 7 — Handler với Mệnh đề Điều kiện `when:`
**Hỏi:** Có thể khai báo mệnh đề `when:` bên trong khối Handler được không? Khi nào nên áp dụng? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** Hoàn toàn có thể. Mệnh đề `when:` đặt bên trong khối Handler sẽ được đánh giá khi Handler đó chuẩn bị thi hành. Ứng dụng: Dùng để rẽ nhánh câu lệnh restart dịch vụ theo từng họ hệ điều hành (ví dụ `when: ansible_facts.os_family == "RedHat"` restart `httpd`, ngược lại restart `apache2`).
**Tiêu chí chấm:**
- 0: Cho rằng Handler không hỗ trợ mệnh đề `when`.
- 1: Biết dùng `when` nhưng đặt sai vị trí ở từ khóa `notify`.
- 2: Phân tích chính xác việc đặt `when` bên trong khối Handler và ứng dụng đa OS.
- 3: Nêu đúng + viết đoạn mã YAML Handler rẽ nhánh dịch vụ theo `os_family`.
**Câu hỏi đào sâu:** Nếu mệnh đề `when` trong Handler đánh giá FALSE, Handler đó có chạy không? *(Không, Handler sẽ bị skipped.)*

---

### Câu 8 — Graceful Reload vs Full Restart trong Handler ★★★
**Hỏi:** Tại sao trong các Handler quản lý Web Server (như Nginx, HAProxy), người ta thường ưu tiên dùng `state: reloaded` thay vì `state: restarted`?
**Đáp án chuẩn:**
- `state: restarted`: Tắt hẳn tiến trình chính và khởi động lại từ đầu, gây đứt gãy các kết nối HTTP/TCP đang mở của người dùng (downtime ngắn).
- `state: reloaded`: Thực hiện **Graceful Reload** — nạp lại file cấu hình mới vào bộ nhớ mà vẫn giữ nguyên các worker process đang phục vụ kết nối cũ, 0% rớt kết nối của khách hàng (Zero Downtime).
**Tiêu chí chấm:**
- 0: Không phân biệt được `restarted` và `reloaded`.
- 1: Biết `reloaded` nhẹ hơn nhưng không giải thích được cơ chế Graceful Reload duy trì kết nối HTTP.
- 2: Phân tích chính xác sự khác biệt về tiến trình và trải nghiệm người dùng giữa `restarted` và `reloaded`.
- 3: Nêu đúng + đưa ra lời khuyên thiết kế Playbook cho hệ thống E-commerce Production.
**Câu hỏi đào sâu:** Khi nào thì BẮT BUỘC phải dùng `restarted` thay vì `reloaded`? *(Khi có sự thay đổi về cổng lắng nghe listen port, thay đổi module kernel, hoặc nâng cấp phiên bản binary.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Handlers 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook sử dụng `handlers` để đảm bảo tính Idempotency và dịch vụ trên máy đích đúng trạng thái.
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site.yml`: Task chép file cấu hình báo `changed=1` và terminal xuất hiện dòng `RUNNING HANDLER [Restart App]`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** và KHÔNG CÓ BẤT KỲ dòng `RUNNING HANDLER` nào xuất hiện.
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/app.conf` và kiểm tra tiến trình/uptime để chứng minh dịch vụ đang hoạt động thực sự với cấu hình mới.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không chú ý việc Handler im lặng ở Lần 2.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và dòng log terminal.
- 3: Trình bày xuất sắc 3 bước + phân tích ý nghĩa của việc Handler không chạy ở Lần 2.
**Câu hỏi đào sâu:** Nếu ở Lần 2 bảng RECAP vẫn báo `changed=1` và Handler vẫn bị kích hoạt, nguyên nhân do đâu? *(Do có 1 Task chính bị lặp thay đổi liên tục, ví dụ task command không có changed_when: false.)*

---

### Câu 10 — `notify` trong Task Vòng lặp `loop:` ★★★
**Hỏi:** Khi thuộc tính `notify: Restart App` được đặt bên trong một Task chứa vòng lặp `loop:` duyệt 5 phần tử, Handler sẽ được kích hoạt khi nào và bao nhiêu lần?
**Đáp án chuẩn:** Handler sẽ được đưa vào hàng chờ KHI CÓ ÍT NHẤT 1 PHẦN TỬ trong 5 phần tử trả về `changed: true`. Nhờ cơ chế khử trùng lặp (Deduplication), Handler `Restart App` vẫn **CHỈ THỰC THI ĐÚNG 1 LẦN DUY NHẤT Ở CUỐI PLAYBOOK** chứ không bị restart 5 lần.
**Tiêu chí chấm:**
- 0: Cho rằng Handler sẽ bị chạy 5 lần cho 5 item.
- 1: Biết Handler chạy 1 lần nhưng không giải thích được điều kiện "ít nhất 1 item changed".
- 2: Phân tích chính xác cơ chế đánh giá cờ changed mảng loop và khử trùng lặp Handler.
- 3: Nêu đúng + viết đoạn YAML minh họa Task copy loop 3 file config phát notify.
**Câu hỏi đào sâu:** Nếu cả 5 phần tử trong `loop` ở Lần 2 đều báo `ok` (`changed: false`), Handler có chạy không? *(Không, Handler im lặng 100%.)*

---

### Câu 11 — Xử lý Tình huống Handler văng Lỗi Syntax Config ★★★
**Hỏi:** Giả sử Task 1 copy file cấu hình lỗi syntax Nginx, Task 2 `flush_handlers` chạy Handler `Reload Nginx` và Handler này bị văng lỗi fatal do file config sai syntax. Ansible sẽ xử lý các task phía sau ra sao?
**Đáp án chuẩn:** Khi Handler bị văng lỗi fatal trong quá trình thực thi, Ansible Engine sẽ coi đây là lỗi nghiêm trọng, ngay lập tức ngắt toàn bộ Playbook và BỎ QUA các Task chính phía sau. Hệ thống máy đích sẽ dừng lại ở đúng mốc thời gian đó để quản trị viên vào kiểm tra lỗi syntax file cấu hình.
**Tiêu chí chấm:**
- 0: Cho rằng Ansible bỏ qua lỗi Handler và chạy tiếp các task sau.
- 1: Biết Playbook dừng nhưng không giải thích được lý do ngắt thi hành khi Handler fatal.
- 2: Phân tích chính xác luồng xử lý ngắt thi hành an toàn của Ansible khi Handler fail.
- 3: Nêu đúng + đưa ra lời khuyên sử dụng module `command: nginx -t` kiểm tra syntax trước khi notify.
**Câu hỏi đào sâu:** Làm sao để viết Task kiểm tra syntax file config trước khi kích hoạt Handler restart? *(Thực hiện task `command: nginx -t` kiểm tra trước, nếu ok mới phát notify restart.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng khi Dùng handlers và notify ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên sử dụng `handlers` và `notify` hiệu quả, an toàn và chuẩn Idempotency nhất.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Tuyệt đối KHÔNG restart dịch vụ trong `tasks:`, hãy dùng `notify` và `handlers`.
2. **Quy tắc 2:** Tận dụng cơ chế khử trùng lặp tự động (Deduplication) để tiết kiệm thời gian restart.
3. **Quy tắc 3:** Sử dụng `listen:` để nhóm nhiều Handler cùng phản ứng với 1 chủ đề thông báo.
4. **Quy tắc 4:** Sử dụng `meta: flush_handlers` khi Task sau bắt buộc cần dịch vụ đã restart.
5. **Quy tắc 5:** Khai báo `force_handlers: yes` để bảo vệ hàng chờ, và đối soát Lần 2 `changed=0` (Handler im lặng) qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy kiến tạo hạ tầng tự động hóa chuyên nghiệp.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào đảm bảo 0% gián đoạn dịch vụ lãng phí cho người dùng? *(Quy tắc 1 và Quy tắc 2.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm thiết kế kịch bản phản ứng sự kiện và quản lý dịch vụ trong Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi xây dựng kịch bản quản lý dịch vụ theo nguyên lý phản ứng sự kiện thông minh: tuyệt đối không đặt lệnh restart dịch vụ vô điều kiện trong `tasks`, mà luôn sử dụng thuộc tính `notify:` kết hợp khối `handlers:`. Tôi làm chủ cơ chế khử trùng lặp tự động (Deduplication) giúp gom nhiều thông báo restart thành 1 lần duy nhất ở cuối Playbook, sử dụng `listen:` để nhóm các chuỗi dịch vụ liên quan, dùng `meta: flush_handlers` khi cần ép thi hành dịch vụ tức thì, và bảo vệ hệ thống bằng `force_handlers: yes`. Mọi Playbook của tôi ở lượt chạy Lần hai đều im lặng hoàn toàn không restart dịch vụ thừa, đạt chuẩn Idempotency `changed=0` tuyệt đối và đối soát sự thật qua `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Đặng Văn U | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Hoàng Thị V | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 12

Để chuẩn bị tốt nhất cho **Buổi 12: Templates và Filters — template, jinja2, filter**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Module `ansible.builtin.template` khác module `ansible.builtin.copy` ở điểm cốt lõi nào?
2. **Nghiên cứu trước 2:** Định dạng tệp tin Jinja2 Template thường có đuôi mở rộng là gì? Cú pháp chèn biến `{{ ... }}` và vòng lặp `{% for ... %}` trong Jinja2 viết ra sao?
3. **Nghiên cứu trước 3:** Liệt kê 3 Jinja2 Filters thường dùng để biến đổi dữ liệu (ví dụ `default`, `lower`, `join`).

---


### [Chuyên Đề 12] Lập Trình Bản Mẫu Jinja2 Templates: Filters, Biểu Thức Điều Kiện, Vòng Lặp & Tự Động Sinh File Cấu Hình Phức Tạp

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Module <code>ansible.builtin.template</code> khác module <code>ansible.builtin.copy</code> ở điểm cốt lõi nào? Khi nào thì bắt buộc phải dùng <code>template</code>? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Module <code>copy</code>: Chỉ chép nguyên vẹn dữ liệu thô (raw content) của tệp nguồn sang máy đích, KHÔNG HỀ tính toán hay giải mã các biểu thức Jinja2 bên trong tệp.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Module <code>template</code>: Khởi chạy bộ máy Jinja2 Engine trên Control Node để thế giá trị các biến <code>{{ var }}</code>, thực thi các vòng lặp <code>{% for %}</code> và rẽ nhánh <code>{% if %}</code> để sinh ra tệp cấu hình động hoàn chỉnh trước khi gửi tới máy đích.</div>
Bắt buộc dùng <code>template</code> khi tệp nguồn là tệp mẫu thiết kế <code>.j2</code> cần sinh cấu hình linh hoạt theo từng máy đích.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không phân biệt được <code>copy</code> và <code>template</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết <code>template</code> dùng cho <code>.j2</code> nhưng không giải thích được cơ chế render của Jinja2 Engine.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác sự khác biệt giữa chép thô và rendering động trên Control Node.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ tệp <code>nginx.conf.j2</code> sinh <code>worker_processes</code> theo CPU.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu dùng module <code>copy</code> chép file <code>app.conf.j2</code>, nội dung file trên máy đích sẽ ra sao? *(Nó sẽ chứa nguyên văn chuỗi thô <code>{{ ansible_facts.memtotal_mb }}</code> chưa được giải mã.)*
</div>
</details>

---

### Câu 2 — Cú pháp Biến và Khối Điều khiển Jinja2 🔥
**Hỏi:** Phân biệt cú pháp Jinja2 cặp ngoặc nhọn `{{ ... }}` và ngoặc phần trăm `{% ... %}`. Cho ví dụ. *(Liên quan QT 4.2, QT 4.3)*
**Đáp án chuẩn:**
- Cú pháp `{{ ... }}` (Variable Interpolation): Dùng để **IN GIÁ TRỊ** của một biến hoặc kết quả biểu thức ra tệp tin (ví dụ `listen {{ web_port }};`).
- Cú pháp `{% ... %}` (Control Structure): Dùng để **THỰC THI LỆNH ĐIỀU KHIỂN LOGIC** như vòng lặp `{% for item in list %}` hoặc rẽ nhánh `{% if condition %}` (ví dụ `{% if ssl_enabled %}`).
**Tiêu chí chấm:**
- 0: Nhầm lẫn giữa `{{ }}` và `{% %}`.
- 1: Biết `{{ }}` in biến nhưng không giải thích được cấu trúc điều khiển `{% %}`.
- 2: Phân tích chính xác cú pháp và chức năng của từng loại cặp ngoặc.
- 3: Nêu đúng + viết đoạn mã Jinja2 minh họa cả `{{ }}` và `{% for %}` sinh Virtual Hosts.
**Câu hỏi đào sâu:** Làm thế nào để xóa bỏ các khoảng trắng dòng trống thừa do vòng lặp `{% for %}` sinh ra? *(Sử dụng cú pháp ngắt khoảng trắng với dấu trừ `{%- for item in list -%}`.)*

---

### Câu 3 — Sử dụng Jinja2 Filter `default` 🔥
**Hỏi:** Jinja2 Filter `default` có tác dụng gì? Tại sao việc sử dụng filter `default` được coi là nguyên tắc lập trình phòng vệ (Defensive Programming)? *(Liên quan QT 5.1)*
**Đáp án chuẩn:** Filter `default('fallback_val')` dùng để cung cấp một giá trị mặc định phòng vệ khi biến được gọi chưa được khai báo ở bất kỳ tầng nào. Đây là nguyên tắc lập trình phòng vệ vì nó ngăn chặn 100% việc Playbook bị crash đứt gãy với lỗi fatal `undefined variable` khi chạy trên các máy đích thiếu biến tùy chọn (ví dụ `{{ app_port | default(8080) }}`).
**Tiêu chí chấm:**
- 0: Không biết Jinja2 Filter `default`.
- 1: Biết `default` gán giá trị mặc định nhưng không nêu được vai trò phòng chống lỗi fatal undefined.
- 2: Phân tích chính xác cơ chế fallback value và tư duy lập trình phòng vệ.
- 3: Nêu đúng + viết đoạn YAML và Jinja2 Template minh họa filter `default`.
**Câu hỏi đào sâu:** Nếu biến `app_port` có giá trị là `false`, filter `{{ app_port | default(8080) }}` sẽ trả về giá trị gì? *(Trả về false; muốn ép nhận default khi biến bằng false/empty phải dùng `default(8080, true)`.)*

---

### Câu 4 — Biến đổi Mảng với Jinja2 Filter `join` 🔥
**Hỏi:** Trình bày tác dụng của Jinja2 Filter `join`. Tại sao phải dùng filter `join` khi chèn một mảng biến Ansible List vào tệp cấu hình INI/Properties? *(Liên quan QT 5.2)*
**Đáp án chuẩn:** Filter `join('sep')` dùng để nối các phần tử của một mảng danh sách (List) thành một chuỗi duy nhất phân cách bởi ký tự `sep`. Phải dùng filter `join` vì tệp cấu hình ứng dụng (như INI, Java properties) không hiểu định dạng mảng Python `['10.0.0.1', '10.0.0.2']`, mà bắt buộc cần dạng chuỗi `10.0.0.1, 10.0.0.2`.
**Tiêu chí chấm:**
- 0: Không biết filter `join`.
- 1: Biết `join` nối chuỗi nhưng không giải thích được lý do ép kiểu từ mảng sang chuỗi cho file INI.
- 2: Phân tích chính xác cơ chế biến đổi mảng sang chuỗi chuẩn hóa ứng dụng.
- 3: Nêu đúng + minh họa cú pháp `{{ allowed_ips | join(', ') }}` trong template INI.
**Câu hỏi đào sâu:** Ngược lại với filter `join` là filter nào? *(Là filter `split` dùng để cắt chuỗi thành mảng.)*

---

### Câu 5 — Chuyển đổi Định dạng với `to_nice_yaml` và `to_json`
**Hỏi:** Các Jinja2 Filters `to_json` và `to_nice_yaml` được ứng dụng trong trường hợp nào? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** Các filter này dùng để tự động mã hóa (serialize) một từ điển hoặc mảng dữ liệu Ansible thành tệp tin định dạng JSON hoặc YAML chuẩn hóa. Ứng dụng: Dùng để sinh các tệp cấu hình JSON/YAML phức tạp (như Kubernetes manifest, Docker config, Elasticsearch settings) chỉ bằng 1 dòng trong template `{{ app_config_dict | to_nice_yaml }}` mà không cần nối chuỗi thủ công.
**Tiêu chí chấm:**
- 0: Không biết các filter chuyển đổi định dạng.
- 1: Biết `to_json` nhưng không phân biệt được với `to_nice_json`.
- 2: Phân tích chính xác vai trò mã hóa tự động cấu trúc dữ liệu sang JSON/YAML.
- 3: Nêu đúng + viết ví dụ template sinh tệp YAML đẹp với `to_nice_yaml`.
**Câu hỏi đào sâu:** Phân biệt sự khác nhau giữa `to_json` và `to_nice_json`? *(`to_json` in toàn bộ JSON trên 1 dòng dài; `to_nice_json` tự động thụt lề và xuống dòng đẹp cho người đọc.)*

---

### Câu 6 — Kiểm tra Cú pháp Cấu hình với `validate:` 🔥
**Hỏi:** Thuộc tính `validate:` trong module `template` có vai trò gì đối với sự an toàn của dịch vụ Production? Ký tự `%s` đại diện cho điều gì? *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Thuộc tính `validate: "<command> %s"` dùng để ép Ansible mở một tệp tạm thời trên máy đích, chạy câu lệnh kiểm tra cú pháp (ví dụ `nginx -t -c %s`), nếu câu lệnh kiểm tra thành công (exit code = 0) mới cho phép ghi đè vào tệp thật. Ký tự `%s` đại diện cho đường dẫn của tệp tạm thời đó. Vai trò: Ngăn chặn 100% rủi ro ghi đè file cấu hình lỗi làm ngắt dịch vụ Web Server trên Production.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `validate:`.
- 1: Biết `validate` kiểm tra file nhưng không giải thích được cơ chế tệp tạm `%s`.
- 2: Phân tích chính xác cơ chế tệp tạm `%s` và vai trò bảo vệ an toàn dịch vụ.
- 3: Nêu đúng + viết đoạn mã YAML module `template` có `validate: "nginx -t -c %s"`.
**Câu hỏi đào sâu:** Nếu câu lệnh trong `validate` trả về exit code != 0 (thất bại), Ansible sẽ làm gì? *(Ansible ngắt thi hành Task, báo lỗi fatal và HỦY BỎ việc ghi đè file thật.)*

---

### Câu 7 — Ý nghĩa Biến Header `{{ ansible_managed }}`
**Hỏi:** Biến `{{ ansible_managed }}` dùng để làm gì? Tại sao nên chèn nó ở dòng đầu tiên của mọi tệp template `.j2`? *(Liên quan QT 6.2)*
**Đáp án chuẩn:** Biến `{{ ansible_managed }}` tự động sinh ra một chuỗi comment header (ví dụ `# Ansible managed: modified on 2026-08-22 by user on control_node`). Nên chèn nó ở dòng 1 để cảnh báo các quản trị viên không được chỉnh sửa bằng tay trên máy đích (tránh bị Ansible ghi đè ở lượt sau) và lưu vết thời gian khởi tạo.
**Tiêu chí chấm:**
- 0: Không biết biến `ansible_managed`.
- 1: Biết `ansible_managed` là dòng comment nhưng không nêu được mục đích cảnh báo sửa tay.
- 2: Phân tích chính xác vai trò cảnh báo quản trị viên và lưu vết hệ thống.
- 3: Nêu đúng + minh họa dòng comment `# {{ ansible_managed }}` ở đầu file Nginx/Apache.
**Câu hỏi đào sâu:** Chuỗi định dạng của `ansible_managed` có thể tùy chỉnh trong tệp cấu hình nào? *(Tùy chỉnh trong tệp `ansible.cfg` qua thuộc tính `ansible_managed`.)*

---

### Câu 8 — Cạm bẫy Trôi Checksum Idempotency trong Template 🔥
**Hỏi:** Tại sao việc chèn các biến thời gian thực (như `{{ ansible_date_time.iso8601 }}`) vào nội dung tệp template lại bị coi là sai quy chuẩn Idempotency? *(Liên quan QT 6.3)*
**Đáp án chuẩn:** Vì biến thời gian thay đổi liên tục theo từng giây/ngày. Mỗi lần Playbook chạy, bộ máy Jinja2 Engine sinh ra nội dung mới có timestamp mới, làm checksum SHA1 của file render bị khác biệt so với file trên đĩa. Kết quả: Module `template` bị đánh lầm là có thay đổi và báo `changed=1` ở MỌI LƯỢT CHẠY LẦN 2, hỏng hoàn toàn tính Idempotency và làm restart dịch vụ lãng phí.
**Tiêu chí chấm:**
- 0: Không biết lý do tại sao biến thời gian làm hỏng Idempotency.
- 1: Biết `changed=1` nhưng không giải thích được cơ chế so sánh checksum SHA1 của module `template`.
- 2: Phân tích chính xác cơ chế so sánh checksum SHA1 nội dung render vs file đĩa cứng.
- 3: Nêu đúng + đưa ra giải pháp loại bỏ biến thời gian thực khỏi nội dung template.
**Câu hỏi đào sâu:** Làm sao để module `template` nhận biết tệp tin trên máy đích có cần thay đổi hay không? *(Bằng cách so sánh mã checksum SHA1 của chuỗi nội dung render với checksum SHA1 của tệp đĩa đích.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Templates 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook sử dụng `template` để đảm bảo tính Idempotency và tệp tin trên máy đích ở đúng trạng thái.
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site.yml`: Task template render và chép file báo `changed=1`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (vì checksum nội dung render trùng khớp 100%).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/nginx-demo.conf` kiểm tra nội dung file thực sự được giải mã biến và chứa đúng cấu hình đã render.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI cụ thể.
- 3: Trình bày xuất sắc 3 bước + cho ví dụ thực tế lệnh `docker exec cat` đối soát file đã render.
**Câu hỏi đào sâu:** Nếu ở Lần 2 ta thay đổi một giá trị biến trong `group_vars`, chỉ số RECAP Lần 2 sẽ báo thế nào? *(RECAP Lần 2 sẽ báo `changed=1` vì checksum nội dung mới bị thay đổi so với file đĩa.)*

---

### Câu 10 — Vòng lặp `{% for %}` và Filter `selectattr` Nâng cao ★★★
**Hỏi:** Viết một đoạn mã Jinja2 Template sử dụng vòng lặp `{% for %}` kết hợp filter `selectattr` để chỉ duyệt và in ra danh sách các Virtual Host có cờ `active == true`.
**Đáp án chuẩn:**
```jinja2
{% for vhost in web_vhosts | selectattr('active', 'defined') | selectattr('active', 'equalto', true) %}
server {
    listen {{ vhost.port | default(80) }};
    server_name {{ vhost.domain }};
}
{% endfor %}
```
**Tiêu chí chấm:**
- 0: Không viết được kịch bản Jinja2 nâng cao.
- 1: Viết được `{% for %}` nhưng không biết lọc mảng bằng `selectattr`.
- 2: Phân tích chính xác vai trò lọc phần tử mảng của filter `selectattr`.
- 3: Nêu đúng + viết đoạn mã Jinja2 Template hoàn chỉnh lọc vhost active.
**Câu hỏi đào sâu:** Filter `map(attribute='domain')` trong Jinja2 có tác dụng gì? *(Dùng để trích xuất mảng danh sách chỉ chứa thuộc tính domain từ danh sách từ điển.)*

---

### Câu 11 — Quản lý File Nhị phân Binary vs File Văn bản Text ★★★
**Hỏi:** Có nên dùng module `ansible.builtin.template` để chép các tệp nhị phân (Binary files như `.tar.gz`, `.png`, `.so`) hay không? Vì sao?
**Đáp án chuẩn:** TUYỆT ĐỐI KHÔNG. Module `template` và bộ máy Jinja2 Engine được thiết kế riêng cho các tệp văn bản mã hóa UTF-8. Nếu truyền tệp nhị phân vào module `template`, Jinja2 Parser sẽ cố gắng đọc và parse các ký tự nhị phân thành chuỗi văn bản, gây hỏng dữ liệu (corruption) và văng lỗi `UnicodeDecodeError`. Đối với tệp nhị phân, BẮT BUỘC dùng module `ansible.builtin.copy`.
**Tiêu chí chấm:**
- 0: Cho rằng `template` chép được mọi loại file kể cả binary.
- 1: Biết không nên chép binary bằng `template` nhưng không giải thích được lỗi `UnicodeDecodeError`.
- 2: Phân tích chính xác sự khác biệt về mã hóa UTF-8 text vs Binary data.
- 3: Nêu đúng + đưa ra quy tắc chọn module `template` (cho text dynamic) và `copy` (cho binary/raw).
**Câu hỏi đào sâu:** Nếu tệp tin là tệp văn bản tĩnh KHÔNG CÓ BIẾN ĐỘNG NÀO, nên chọn `copy` hay `template`? *(Nên chọn `copy` để tiết kiệm chi phí CPU rendering của Jinja2 Engine.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng khi Dùng `template` và Jinja2 ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên sử dụng `template` và Jinja2 Filters hiệu quả, an toàn và chuẩn Idempotency nhất.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Dùng module `template` cho tệp mẫu `.j2` và module `copy` cho tệp nhị phân/tĩnh.
2. **Quy tắc 2:** Phân biệt rõ cú pháp `{{ }}` (in giá trị) và `{% %}` (vòng lặp/rẽ nhánh).
3. **Quy tắc 3:** Luôn bọc filter `| default('val')` phòng thủ lỗi fatal undefined variable.
4. **Quy tắc 4:** Khai báo thuộc tính `validate:` kiểm tra cú pháp tệp tin trước khi ghi đĩa.
5. **Quy tắc 5:** Loại bỏ biến thời gian thực khỏi nội dung template, và kiểm thử Lần 2 `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy quản trị hạ tầng qua mã nguồn (IaC) chuyên nghiệp.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp ngăn ngừa sự cố sập dịch vụ do file config lỗi? *(Quy tắc 4: Khai báo thuộc tính validate:)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kỹ năng tự động hóa sinh file cấu hình động bằng Ansible và Jinja2, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi chuyển đổi toàn bộ các tệp cấu hình tĩnh rườm rà thành các tệp mẫu sinh cấu hình động Jinja2 Template `.j2` thông minh. Tôi làm chủ cú pháp nội suy biến `{{ }}`, vòng lặp `{% for %}`, rẽ nhánh `{% if %}`, và các bộ lọc Jinja2 Filters (`default`, `join`, `to_nice_yaml`) để xử lý an toàn mọi dữ liệu đầu vào. Để bảo vệ hạ tầng Production, tôi luôn sử dụng thuộc tính `validate:` kiểm tra cú pháp tệp tin trước khi ghi đĩa. Mọi tệp template của tôi đều được loại bỏ các biến trôi checksum, đảm bảo ở lượt chạy Lần hai đạt `changed=0` Idempotency tuyệt đối và đối soát sự thật thực tế trên máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Bùi Văn X | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Trịnh Thị Y | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 13

Để chuẩn bị tốt nhất cho **Buổi 13: Blocks, Error Handling — block, rescue, always, failed_when, changed_when**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Khối `block:` kết hợp `rescue:` và `always:` trong Ansible có cơ chế hoạt động tương đương cấu trúc `try...catch...finally` trong lập trình như thế nào?
2. **Nghiên cứu trước 2:** Thuộc tính `failed_when:` dùng để thay đổi định nghĩa một Task bị coi là THẤT BẠI khi nào?
3. **Nghiên cứu trước 3:** Thuộc tính `changed_when:` dùng để làm gì khi gọi các lệnh CLI thô với module `command` / `shell`?

---


### [Chuyên Đề 13] Xử Lý Lỗi Chuyên Sâu Với Blocks: block, rescue, always & Cơ Chế Try-Catch-Finally Trong Hạ Tầng

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Trình bày cơ chế hoạt động của bộ ba khối <code>block:</code>, <code>rescue:</code>, và <code>always:</code> trong Ansible Playbook. Cấu trúc này tương đương với mô hình nào trong lập trình? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>block:</code> Nơi chứa các Task thực thi chính.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>rescue:</code> Nơi chứa các Task cứu hộ/phục hồi CHỈ CHẠY khi có Task trong <code>block</code> bị văng lỗi.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>always:</code> Nơi chứa các Task dọn dẹp BẮT BUỘC THỰC THI trong mọi tình huống (dù block thành công hay rescue thất bại).</div>
Cấu trúc này tương đương 100% với mô hình <code>try...catch...finally</code> trong các ngôn ngữ lập trình hiện đại (Java, Python, C#).
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết cấu trúc <code>block-rescue-always</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết 3 khối nhưng không so sánh được với mô hình <code>try-catch-finally</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò và điều kiện thi hành của từng khối <code>block</code>, <code>rescue</code>, <code>always</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ cập nhật Database có Rollback trong <code>rescue</code> và xóa file tạm trong <code>always</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Khối <code>rescue:</code> và <code>always:</code> được đặt cùng cấp thụt lề với từ khóa nào trong YAML? *(Được đặt cùng cấp thụt lề với từ khóa <code>block:</code>.)*
</div>
</details>

---

### Câu 2 — Điều kiện Kích hoạt Khối `rescue:` 🔥
**Hỏi:** Khối `rescue:` được Ansible Engine thực thi trong điều kiện nào? Nếu tất cả các Task trong khối `block:` đều thành công, khối `rescue:` sẽ ra sao? *(Liên quan QT 4.2)*
**Đáp án chuẩn:** Khối `rescue:` CHỈ THỰC THI khi có ít nhất một Task trong khối `block:` bị văng lỗi thất bại (Failed). Nếu tất cả các Task trong khối `block:` đều thi hành thành công 100%, Ansible Engine sẽ **TỰ ĐỘNG BỎ QUA TOÀN BỘ KHỐI `rescue:`** và chuyển thẳng sang khối `always:` (hoặc task đằng sau).
**Tiêu chí chấm:**
- 0: Lầm tưởng khối `rescue:` luôn luôn chạy ở mọi lượt.
- 1: Biết `rescue` chạy khi có lỗi nhưng thắc mắc tại sao chạy bình thường `rescue` lại không xuất hiện log.
- 2: Phân tích chính xác điều kiện kích hoạt của `rescue:` như một lưới an toàn thụ động.
- 3: Nêu đúng + minh họa log terminal khi `block` thành công vs khi `block` bị fail.
**Câu hỏi đào sâu:** Nếu 1 task trong `block` bị fail và được `rescue` cứu hộ thành công, chỉ số trong bảng `PLAY RECAP` sẽ hiển thị ra sao? *(Hiển thị chỉ số `rescued=1` và `failed=0`.)*

---

### Câu 3 — Vai trò của Khối `always:` 🔥
**Hỏi:** Tại sao các thao tác dọn dẹp tài nguyên tạm (xóa file lock, mở lại cờ bảo trì) bắt buộc phải được đặt trong khối `always:`? *(Liên quan QT 4.3)*
**Đáp án chuẩn:** Vì khối `always:` đảm bảo tính thực thi 100% trong MỌI TÌNH HUỐNG (kể cả khi `block` thành công hay khi `rescue` bị văng lỗi tiếp). Đặt thao tác dọn dẹp trong `always:` giúp ngăn chặn hoàn toàn nguy cơ rò rỉ file tạm, rò rỉ tài nguyên đĩa cứng hoặc bỏ quên hệ thống trong trạng thái Maintenance Mode khi sự cố xảy ra.
**Tiêu chí chấm:**
- 0: Không biết vai trò của khối `always:`.
- 1: Biết `always` chạy ở cuối nhưng không giải thích được lý do bảo vệ rò rỉ tài nguyên khi rescue bị crash.
- 2: Phân tích chính xác tính thực thi 100% bắt buộc của `always:` và lợi ích an toàn hệ thống.
- 3: Nêu đúng + viết đoạn YAML minh họa xóa file tạm `/tmp/*.lock` trong khối `always:`.
**Câu hỏi đào sâu:** Nếu 1 task trong khối `always:` bị văng lỗi fatal, Playbook có bị dừng không? *(Có, ngoại trừ khi task trong always đó có cờ ignore_errors: true.)*

---

### Câu 4 — Tùy biến Điều kiện Thất bại với `failed_when:` 🔥
**Hỏi:** Thuộc tính `failed_when:` dùng để làm gì? Cho ví dụ trường hợp một lệnh CLI trả về exit code = 0 nhưng vẫn bị coi là FAILED. *(Liên quan QT 5.1)*
**Đáp án chuẩn:** Thuộc tính `failed_when:` cho phép quản trị viên định nghĩa lại điều kiện khiến một Task bị coi là THẤT BẠI dựa trên logic biểu thức Jinja2 tùy biến. Ví dụ: Lệnh script trả về `rc = 0` (exit code thành công) nhưng trong stdout lại in ra chuỗi `"FATAL_ERROR: Database Connection Refused"`. Khai báo `failed_when: "'FATAL_ERROR' in result.stdout"` sẽ ép Ansible đánh dấu Task đó là FAILED.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `failed_when:`.
- 1: Biết `failed_when` để báo lỗi nhưng không cho được ví dụ lệnh rc=0 chứa chuỗi lỗi stdout.
- 2: Phân tích chính xác cơ chế ghi đè cờ failed dựa trên thuộc tính biến `register`.
- 3: Nêu đúng + viết đoạn YAML minh họa task `command` kết hợp `register` và `failed_when`.
**Câu hỏi đào sâu:** Phân biệt sự khác nhau giữa `failed_when` và `ignore_errors`? *(`failed_when` ép task THẤT BẠI khi thỏa mãn điều kiện; `ignore_errors` BỎ QUA LỖI khi task bị thất bại.)*

---

### Câu 5 — Khống chế Cờ changed mạo danh với `changed_when: false` 🔥
**Hỏi:** Tại sao đối với các Task gọi lệnh CLI thô chỉ đọc (như `command: uptime` hoặc `command: date`), ta bắt buộc phải thêm thuộc tính `changed_when: false`? *(Liên quan QT 5.2)*
**Đáp án chuẩn:** Vì các module `ansible.builtin.command` và `shell` mặc định không nhận biết được tính Idempotency của câu lệnh shell thô, nên **mặc định luôn gán cờ `changed: true` ở mọi lượt thi hành**. Nếu không thêm `changed_when: false`, các lệnh đọc thông số sẽ liên tục báo `changed=1` ở lượt chạy Lần 2, làm sai lệch báo cáo và hỏng hoàn toàn tiêu chuẩn Idempotency (`changed=0`).
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `changed_when: false`.
- 1: Biết gõ `changed_when: false` nhưng không giải thích được cơ chế gán changed mạo danh mặc định của module `command`.
- 2: Phân tích chính xác lý do khống chế cờ changed mạo danh để bảo vệ tiêu chuẩn Idempotency.
- 3: Nêu đúng + chứng minh bằng bảng `PLAY RECAP` ở Lần 1 và Lần 2 khi có và không có `changed_when: false`.
**Câu hỏi đào sâu:** Làm sao để Task `command: echo "UPDATED"` chỉ báo `changed: true` khi stdout chứa từ `"UPDATED"`? *(Khai báo `changed_when: "'UPDATED' in result.stdout"`.)*

---

### Câu 6 — Rủi ro của `ignore_errors: yes`
**Hỏi:** Tại sao việc lạm dụng thuộc tính `ignore_errors: yes` cho các Task cốt lõi bị coi là một anti-pattern nguy hiểm trong Ansible? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** Vì `ignore_errors: yes` sẽ "nuốt chửng" lỗi (silent error). Nếu áp dụng cho Task cốt lõi (như task phân quyền hoặc chép file SSL), khi Task bị thất bại, Ansible vẫn in màu xanh/vàng mạo danh và chạy tiếp. Kết quả: Playbook báo hoàn thành 100% nhưng hệ thống Production bị sập đứt gãy do thiếu file SSL. Thay vì lạm dụng `ignore_errors`, hãy dùng khối `block-rescue` có kiểm soát.
**Tiêu chí chấm:**
- 0: Cho rằng nên dùng `ignore_errors: yes` cho mọi task để Playbook không bao giờ bị dừng.
- 1: Biết `ignore_errors` nguy hiểm nhưng không phân tích được hậu quả nuốt chửng lỗi làm sập Production.
- 2: Phân tích chính xác tác hại của nuốt chửng lỗi và đề xuất thay thế bằng `block-rescue`.
- 3: Nêu đúng + cho ví dụ trường hợp hợp lệ duy nhất nên dùng `ignore_errors` (như ping thử server phụ tùy chọn).
**Câu hỏi đào sâu:** Thuộc tính `ignore_errors: yes` có bỏ qua được lỗi syntax YAML static không? *(Không, lỗi syntax YAML static bị ngắt thi hành ngay ở bước parse.)*

---

### Câu 7 — Dừng Khẩn cấp Cụm Máy chủ với `any_errors_fatal`
**Hỏi:** Thuộc tính `any_errors_fatal: true` giải quyết bài toán an toàn gì khi triển khai Playbook trên một cụm máy chủ (Cluster)? *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Mặc định khi 1 host trong Inventory bị lỗi, Ansible chỉ ngắt thi hành trên host đó và tiếp tục chạy Playbook trên các host còn lại. Trong các bài toán nâng cấp cụm (như K8s hay DB Cluster), điều này làm lệch phiên bản phần mềm giữa các node. Thuộc tính `any_errors_fatal: true` buộc Ansible kích hoạt **phanh khẩn cấp dừng 100% các host ngay lập tức** khi có ít nhất 1 host bị lỗi.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `any_errors_fatal`.
- 1: Biết `any_errors_fatal` dừng host nhưng không nêu được bài toán bảo vệ tính đồng nhất phiên bản cụm cluster.
- 2: Phân tích chính xác cơ chế phanh khẩn cấp toàn cụm và ứng dụng cho Cluster Deployment.
- 3: Nêu đúng + viết đoạn YAML khai báo `any_errors_fatal: true` ở cấp Playbook.
**Câu hỏi đào sâu:** Cờ `any_errors_fatal: true` được khai báo ở cấp độ Task hay cấp độ Playbook? *(Được khai báo ở cấp độ Playbook, cùng cấp với `hosts:` và `tasks:`.)*

---

### Câu 8 — Tự động Rollback trong Khối `rescue:` ★★★
**Hỏi:** Trình bày mô hình thiết kế tự động Rollback khôi phục trạng thái cũ bằng khối `rescue:` khi gặp sự cố nâng cấp phần mềm.
**Đáp án chuẩn:** Mô hình 3 bước:
1. **Khối `block:`:** Bước A1 tạo bản sao lưu file cấu hình cũ (`app.conf.bak`), Bước A2 thực hiện chép file cấu hình mới và chạy script upgrade.
2. **Khối `rescue:`:** Nếu Bước A2 bị fail, khối `rescue:` lập tức gọi Task chép đè lại file `app.conf.bak` về vị trí `app.conf` gốc và restart lại dịch vụ cũ.
3. **Khối `always:`:** Xóa bỏ file tạm sao lưu `/tmp/upgrade.lock`.
**Tiêu chí chấm:**
- 0: Không thiết kế được mô hình Rollback.
- 1: Biết rollback trong `rescue` nhưng không nêu được bước tạo file bak trước đó trong `block`.
- 2: Phân tích chính xác luồng 3 bước backup -> attempt upgrade -> rollback on rescue -> cleanup.
- 3: Trình bày xuất sắc mô hình + viết kịch bản YAML Rollback hoàn chỉnh chuẩn DevOps.
**Câu hỏi đào sâu:** Làm sao để biết khối `rescue:` ở bước 2 có thực sự trả lại đĩa sạch hay không? *(Dùng lệnh `docker exec target1 cat /etc/app.conf` đối soát lại nội dung file sau khi rescue chạy xong.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Error Handling 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook có cấu trúc xử lý lỗi để đảm bảo tính Idempotency và máy đích ở đúng trạng thái.
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site.yml`: Bắt lỗi và phục hồi thành công qua khối `rescue:`, bảng `PLAY RECAP` hiển thị `rescued=1`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task chính và task kiểm tra đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/error-app.conf` kiểm tra file sản phẩm phục hồi thực sự tồn tại trên đĩa cứng máy đích.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không chú ý chỉ số `rescued=1` ở Lần 1.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và dòng log RECAP.
- 3: Trình bày xuất sắc 3 bước + phân tích ý nghĩa chỉ số `rescued=1` và `changed=0`.
**Câu hỏi đào sâu:** Nếu ở Lần 2 bảng RECAP hiển thị `changed=1` do 1 task `command` trong `block` bị lặp, nguyên nhân do đâu? *(Do task command đó thiếu thuộc tính `changed_when: false`.)*

---

### Câu 10 — Chỉ số `rescued=1` trong Bảng `PLAY RECAP` ★★★
**Hỏi:** Ý nghĩa của chỉ số `rescued=1` trong bảng tổng kết `PLAY RECAP` ở cuối buổi thi hành là gì? Nó có bị coi là lỗi thi hành không?
**Đáp án chuẩn:** Chỉ số `rescued=1` phản ánh rằng có 1 host bị văng ngoại lệ ở khối `block:`, và Ansible Engine đã **tự động chuyển sang khối `rescue:` bắt lỗi và khắc phục sự cố thành công 100%**. Nó KHÔNG BỊ COI LÀ LỖI (`failed=0`), mà là bằng chứng chứng minh kịch bản xử lý lỗi hoạt động tuyệt vời đúng thiết kế.
**Tiêu chí chấm:**
- 0: Lầm tưởng `rescued=1` là Playbook bị lỗi không đạt yêu cầu.
- 1: Biết `rescued` là bắt lỗi nhưng không khẳng định được `failed=0` là kịch bản thành công.
- 2: Phân tích chính xác ý nghĩa của `rescued=1` và khẳng định tính an toàn của Playbook.
- 3: Nêu đúng + so sánh chỉ số `rescued=1, failed=0` vs `rescued=0, failed=1`.
**Câu hỏi đào sâu:** Nếu trong khối `rescue:` lại có 1 Task bị văng lỗi tiếp, chỉ số RECAP sẽ hiển thị thế nào? *(Bảng RECAP sẽ hiển thị `failed=1` và Playbook dừng thi hành.)*

---

### Câu 11 — Tùy biến `failed_when` Kết hợp Phép toán Logic Complex ★★★
**Hỏi:** Viết thuộc tính `failed_when:` kết hợp 2 điều kiện: Task bị coi là FAILED khi exit code `rc != 0` VÀ trong `stderr` KHÔNG CHỨA chuỗi `"WARNING_ONLY"`.
**Đáp án chuẩn:**
```yaml
- name: Execute custom system check script
  ansible.builtin.command: /usr/bin/custom-check.sh
  register: check_out
  failed_when:
    - check_out.rc != 0
    - "'WARNING_ONLY' not in check_out.stderr"
```
**Tiêu chí chấm:**
- 0: Không viết được biểu thức `failed_when` kết hợp logic complex.
- 1: Viết được 1 điều kiện `rc != 0` nhưng sai cú pháp phủ định `'not in'`.
- 2: Viết chuẩn xác mảng điều kiện AND trong `failed_when` cho 2 tiêu chí.
- 3: Trình bày xuất sắc + giải thích cơ chế đánh giá logic AND của dạng mảng list trong `failed_when`.
**Câu hỏi đào sâu:** Nếu muốn đổi sang logic OR giữa 2 điều kiện trên trong `failed_when`, ta viết ra sao? *(Viết trên 1 dòng: `failed_when: check_out.rc != 0 or ('WARNING_ONLY' not in check_out.stderr)`.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Error Handling trong Ansible ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên xây dựng kịch bản xử lý lỗi chuyên nghiệp, an toàn và chuẩn Idempotency nhất.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Bọc các tác vụ nguy hiểm trong bộ ba `block:`, `rescue:`, `always:`.
2. **Quy tắc 2:** Sử dụng `changed_when: false` cho tất cả các Task đọc dữ liệu CLI thô.
3. **Quy tắc 3:** Tùy biến điều kiện thất bại thực sự bằng `failed_when:` thay vì chỉ tin vào exit code.
4. **Quy tắc 4:** Tuyệt đối không lạm dụng `ignore_errors: yes` cho các tác vụ hệ thống cốt lõi.
5. **Quy tắc 5:** Khai báo `any_errors_fatal: true` cho kịch bản cụm, và đối soát Lần 2 `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy thiết kế Playbook chống chịu sự cố (Resilient Playbook) cho Enterprise.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào đảm bảo 100% đĩa cứng không bị đứt gãy dở dang khi có sự cố? *(Quy tắc 1 và Quy tắc 4.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm thiết kế kịch bản bắt lỗi và phục hồi sự cố tự động trong Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi xây dựng kịch bản tự động hóa theo tiêu chuẩn chống chịu sự cố cao cấp (Resilient Infrastructure Playbook): bọc toàn bộ các tác vụ rủi ro trong cấu trúc bộ ba `block:`, `rescue:`, `always:` để tự động Rollback khôi phục đĩa cứng và dọn dẹp tài nguyên 100% khi có sự cố. Tôi kiểm soát chính xác sự thật trạng thái bằng `failed_when:` và khống chế cờ changed mạo danh bằng `changed_when: false`, tuyệt đối không lạm dụng `ignore_errors` để nuốt chửng lỗi. Mọi kịch bản xử lý lỗi của tôi đều được bảo vệ toàn cụm bằng `any_errors_fatal: true`, đạt chuẩn Idempotency `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích qua `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Đỗ Văn Z | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Vũ Thị W | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 14

Chúc mừng học viên đã **HOÀN THÀNH 100% GIAI ĐOẠN 2 (Buổi 07–13)**! Để chuẩn bị bước vào **Giai đoạn 3 (Tổ chức và tái dùng)** với **Buổi 14: Roles — Cấu trúc thư mục, ansible-galaxy role init**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Khái niệm `Role` trong Ansible là gì? Tại sao phải chia nhỏ Playbook khổng lồ thành các Role?
2. **Nghiên cứu trước 2:** Cấu trúc thư mục chuẩn của 1 Ansible Role gồm những thư mục con nào (ví dụ `tasks/`, `handlers/`, `templates/`, `vars/`, `defaults/`, `meta/`)?
3. **Nghiên cứu trước 3:** Lệnh CLI `ansible-galaxy role init <role_name>` dùng để làm gì?

---


### [Chuyên Đề 14] Đóng Gói Tái Sử Dụng Với Ansible Roles: Cấu Trúc Thư Mục Chuẩn, Tasks, Handlers, Vars, Defaults & Meta

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Ansible Role là gì? Tại sao việc sử dụng Role lại được coi là chuẩn mực thiết kế mã nguồn IaC (Infrastructure as Code) cho các dự án Enterprise? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
Ansible Role là chuẩn tổ chức mã nguồn tự động hóa dưới dạng mô-đun độc lập, gom toàn bộ Tasks, Handlers, Variables, Templates và Files vào một cấu trúc thư mục quy chuẩn.
Lợi ích chuẩn mực Enterprise:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Tách biệt rõ ràng các mối quan tâm (Separation of Concerns).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Tái sử dụng mã nguồn 100% trên nhiều Playbook và dự án khác nhau.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Dễ dàng quản lý phiên bản, kiểm thử độc lập và chia sẻ cho cộng đồng qua Ansible Galaxy.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không hiểu khái niệm Ansible Role.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết Role để chia nhỏ file nhưng không giải thích được các lợi ích chuẩn mực Enterprise.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác khái niệm Role và nguyên lý đóng gói mô-đun hóa.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa kiến trúc tổ chức Role cho hệ thống Web/DB Enterprise.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu không dùng Role, một file Playbook triển khai cụm ứng dụng lớn sẽ gặp khó khăn gì? *(Mã nguồn rườm rà hàng nghìn dòng, trùng lặp code, cực kỳ khó bảo trì và không thể tái sử dụng.)*
</div>
</details>

---

### Câu 2 — Khởi tạo Role với Lệnh `ansible-galaxy role init` 🔥
**Hỏi:** Trình bày tác dụng của lệnh CLI `ansible-galaxy role init <role_name>`. Tại sao nên dùng lệnh này thay vì tạo thư mục thủ công? *(Liên quan QT 4.2)*
**Đáp án chuẩn:** Lệnh `ansible-galaxy role init <role_name>` tự động sinh ra toàn bộ khung cây thư mục quy chuẩn gồm 8 thư mục con (`tasks`, `handlers`, `defaults`, `vars`, `templates`, `files`, `meta`, `tests`) cùng các tệp `main.yml` tương ứng. Nên dùng lệnh này vì nó đảm bảo 100% tên thư mục và cấu trúc tuân thủ chính xác quy ước của Ansible Engine, tránh lỗi gõ sai tên thư mục (như gõ nhầm `task/` thiếu 's').
**Tiêu chí chấm:**
- 0: Không biết lệnh `ansible-galaxy role init`.
- 1: Biết lệnh init nhưng không nêu được các thư mục con nó tự động sinh ra.
- 2: Phân tích chính xác lợi ích tiết kiệm thời gian và chống lỗi gõ sai quy chuẩn.
- 3: Nêu đúng + thực thi lệnh CLI minh họa cây thư mục `roles/webserver`.
**Câu hỏi đào sâu:** Tệp `README.md` được tạo ra trong thư mục Role init dùng để làm gì? *(Dùng để viết tài liệu hướng dẫn cách sử dụng biến và cách gọi Role.)*

---

### Câu 3 — Chức năng của các Thư mục Quy chuẩn trong Role 🔥
**Hỏi:** Phân biệt chức năng của 4 thư mục cốt lõi trong Role: `tasks/`, `handlers/`, `templates/`, và `files/`. *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- `tasks/`: Chứa tệp `main.yml` định nghĩa danh sách các Task thi hành chính của Role.
- `handlers/`: Chứa tệp `main.yml` định nghĩa các Handler xử lý khi có thông báo `notify`.
- `templates/`: Chứa các tệp mẫu Jinja2 `.j2` được render động bởi module `template`.
- `files/`: Chứa các tệp tin tĩnh (raw static files) được chép trực tiếp bởi module `copy` hay `script`.
**Tiêu chí chấm:**
- 0: Không phân biệt được các thư mục trong Role.
- 1: Phân biệt được `tasks` và `templates` nhưng nhầm lẫn giữa `templates` và `files`.
- 2: Phân tích chính xác chức năng của cả 4 thư mục quy chuẩn.
- 3: Nêu đúng + cho ví dụ cụ thể về loại file được đặt trong từng thư mục.
**Câu hỏi đào sâu:** Nếu đặt tệp `.j2` vào thư mục `files/` và gọi module `copy`, chuyện gì sẽ xảy ra? *(Tệp `.j2` sẽ bị chép thô sang máy đích mà không được render giải mã biến Jinja2.)*

---

### Câu 4 — Phân biệt Biến `defaults/main.yml` và `vars/main.yml` 🔥
**Hỏi:** Phân biệt thứ tự ưu tiên biến và mục đích sử dụng giữa `defaults/main.yml` và `vars/main.yml` trong Ansible Role. *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- `defaults/main.yml`: Chứa các biến mặc định có **độ ưu tiên thấp nhất** trong toàn bộ hệ thống Ansible. Mục đích: Đóng vai trò là "fallback values" giúp người gọi Role dễ dàng ghi đè từ `inventory`, `group_vars` hoặc khi gọi Role.
- `vars/main.yml`: Chứa các biến nội bộ của Role có **độ ưu tiên rất cao**. Mục đích: Dùng để lưu trữ các hằng số nội bộ không muốn người dùng ghi đè tùy tiện từ bên ngoài.
**Tiêu chí chấm:**
- 0: Lầm tưởng `defaults` và `vars` có độ ưu tiên giống nhau.
- 1: Biết `defaults` ưu tiên thấp hơn `vars` nhưng giải thích sai mục đích áp dụng cho người dùng.
- 2: Phân tích chính xác thứ tự ưu tiên và tư duy phân chia biến linh hoạt vs biến hằng số.
- 3: Nêu đúng + cho ví dụ biến `http_port` đặt ở `defaults` và biến `internal_app_code` đặt ở `vars`.
**Câu hỏi đào sâu:** Nếu một biến được định nghĩa ở CẢ `defaults/main.yml` VÀ `vars/main.yml`, giá trị nào sẽ được Ansible chọn sử dụng? *(Giá trị trong `vars/main.yml` sẽ thắng vì có độ ưu tiên cao hơn.)*

---

### Câu 5 — Gọi Role và Ghi đè Biến trong Playbook 🔥
**Hỏi:** Viết cú pháp YAML trong Playbook `site.yml` gọi Role `webserver` và ghi đè hai biến `webserver_port: 9090` và `webserver_title: "My Portal"`. *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
```yaml
- name: Deploy Custom Webserver Role
  hosts: web
  become: true
  roles:
    - role: webserver
      vars:
        webserver_port: 9090
        webserver_site_title: "My Portal"
```
**Tiêu chí chấm:**
- 0: Không viết được cú pháp gọi Role.
- 1: Viết được `roles: - webserver` nhưng sai cú pháp truyền biến `vars:`.
- 2: Viết chuẩn xác cấu trúc YAML gọi Role truyền biến tùy chỉnh.
- 3: Nêu đúng + giải thích cơ chế biến truyền qua `vars:` ghi đè biến trong `defaults/main.yml`.
**Câu hỏi đào sâu:** Có thể gọi cùng một Role 2 lần trong 1 Playbook với 2 bộ biến khác nhau được không? *(Có thể, bằng cách định nghĩa 2 item trong danh sách `roles:` với bộ `vars:` riêng.)*

---

### Câu 6 — Tham chiếu Đường dẫn Tương đối trong Role
**Hỏi:** Trong Task của Role, khi gọi module `template: src=index.html.j2`, làm thế nào Ansible Engine biết chính xác vị trí tệp `index.html.j2` mà không cần đường dẫn tuyệt đối? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** Vì Ansible Engine có cơ chế tự động tìm kiếm đường dẫn tương đối (Implicit relative path search). Khi một Task nằm bên trong thư mục `roles/<role_name>/tasks/`, Ansible sẽ tự động ưu tiên tìm kiếm tệp template trong thư mục `roles/<role_name>/templates/` và tệp tĩnh trong `roles/<role_name>/files/` của chính Role đó.
**Tiêu chí chấm:**
- 0: Không hiểu cơ chế tìm kiếm đường dẫn tương đối.
- 1: Biết không cần gõ đường dẫn dài nhưng không giải thích được quy tắc implicit search của Ansible Engine.
- 2: Phân tích chính xác cơ chế nạp tài nguyên tương đối theo chuẩn cấu trúc Role.
- 3: Nêu đúng + cảnh báo tác hại của việc gõ đường dẫn tuyệt đối làm hỏng tính di động của Role.
**Câu hỏi đào sâu:** Nếu tệp `index.html.j2` không có trong `roles/webserver/templates/`, Ansible sẽ tìm tiếp ở đâu? *(Tìm ở thư mục `templates/` nằm cùng cấp với file Playbook chính.)*

---

### Câu 7 — Siêu dữ liệu Meta và Dependencies trong Role
**Hỏi:** Tệp `meta/main.yml` trong Role dùng để làm gì? Nêu ví dụ trường hợp sử dụng từ khóa `dependencies:`. *(Liên quan QT 6.1)*
**Đáp án chuẩn:** Tệp `meta/main.yml` chứa các siêu dữ liệu của Role bao gồm thông tin tác giả, license, phiên bản Ansible hỗ trợ, và danh sách các Role phụ thuộc (`dependencies:`).
Ví dụ: Role `wordpress` khai báo `dependencies: - role: php` và `- role: mysql`. Khi Playbook gọi `role: wordpress`, Ansible Engine sẽ tự động thực thi `role: php` và `role: mysql` trước rồi mới chạy `wordpress`.
**Tiêu chí chấm:**
- 0: Không biết tệp `meta/main.yml`.
- 1: Biết `meta` chứa tác giả nhưng không giải thích được cơ chế tự động chạy Role phụ thuộc qua `dependencies`.
- 2: Phân tích chính xác vai trò của `meta/main.yml` và cơ chế nạp dependencies.
- 3: Nêu đúng + viết đoạn YAML minh họa khai báo `dependencies` cho role WordPress.
**Câu hỏi đào sâu:** Điều gì xảy ra nếu 2 Role cùng phụ thuộc vào 1 Role thứ 3? *(Ansible mặc định chỉ thi hành Role thứ 3 đúng 1 lần duy nhất để tránh trùng lặp.)*

---

### Câu 8 — Thiết kế Role Độc lập và Di động (Portable Role) ★★★
**Hỏi:** Thế nào là một Ansible Role độc lập (Portable Role)? Cần tuân thủ nguyên tắc thiết kế nào để một Role có thể mang đi sử dụng ở bất kỳ dự án nào? *(Liên quan QT 6.2)*
**Đáp án chuẩn:** Một Portable Role là Role có tính đóng gói hoàn chỉnh, có thể mang sang bất kỳ hệ thống hay dự án Ansible nào chạy mà **không bị văng lỗi thiếu biến hay thiếu phụ thuộc**.
Nguyên tắc thiết kế:
1. Mọi biến tùy chọn được gọi trong Role phải có giá trị mặc định fallback định nghĩa trong `defaults/main.yml`.
2. Tuyệt đối không tham chiếu đến các biến toàn cục chỉ tồn tại ở `group_vars` của dự án gốc.
3. Không gõ cứng đường dẫn đĩa cứng tuyệt đối.
**Tiêu chí chấm:**
- 0: Không hiểu khái niệm Portable Role.
- 1: Biết khái niệm di động nhưng không nêu được các nguyên tắc thiết kế phòng tránh lỗi undefined.
- 2: Phân tích chính xác các nguyên tắc đóng gói độc lập và giá trị mặc định trong `defaults`.
- 3: Trình bày xuất sắc 3 nguyên tắc + cho ví dụ thực tế về việc chia sẻ Role lên Ansible Galaxy.
**Câu hỏi đào sâu:** Làm thế nào để kiểm thử một Role xem nó có thực sự độc lập hay không? *(Viết kịch bản kiểm thử đơn giản trong thư mục `tests/test.yml` của chính Role đó.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Roles 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook sử dụng Ansible Roles để đảm bảo tính Idempotency và máy đích ở đúng trạng thái.
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-roles.yml`: Các Task bên trong Role thực thi và chép file báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-roles.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task trong Role đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /var/www/html/index.html` kiểm tra nội dung file thực sự được render đúng biến từ Role.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file render.
- 3: Trình bày xuất sắc 3 bước + cho ví dụ thực tế lệnh `docker exec cat` kiểm tra kết quả render từ Role.
**Câu hỏi đào sâu:** Việc đóng gói Task vào trong Role có làm thay đổi cơ chế đánh giá Idempotency của Ansible Engine không? *(Hoàn toàn không, các task trong Role vẫn được so sánh checksum SHA1 như task thông thường.)*

---

### Câu 10 — Vị trí Đặt Thư mục `roles/` trong Dự án ★★★
**Hỏi:** Ansible Engine tìm kiếm các Role theo các thứ tự đường dẫn mặc định nào? Nếu đặt thư mục `roles/` sai vị trí, làm thế nào để cấu hình lại trong `ansible.cfg`?
**Đáp án chuẩn:**
Thứ tự tìm kiếm Role mặc định:
1. Thư mục `roles/` nằm cùng cấp ngang hàng với file Playbook chính.
2. Thư mục `~/.ansible/roles`.
3. Thư mục hệ thống `/etc/ansible/roles`.
Nếu muốn đặt thư mục Role ở vị trí khác (như `shared_roles/`), ta cấu hình thuộc tính `roles_path` trong tệp `ansible.cfg`:
```ini
[defaults]
roles_path = ./shared_roles:/etc/ansible/roles
```
**Tiêu chí chấm:**
- 0: Không biết vị trí tìm kiếm mặc định của thư mục `roles/`.
- 1: Biết `roles/` nằm cùng cấp với Playbook nhưng không biết cấu hình `roles_path` trong `ansible.cfg`.
- 2: Phân tích chính xác thứ tự ưu tiên đường dẫn tìm kiếm Role.
- 3: Nêu đúng + viết đoạn mã cấu hình `roles_path` chuẩn trong `ansible.cfg`.
**Câu hỏi đào sâu:** Dấu hai chấm `:` trong dòng `roles_path` của `ansible.cfg` có ý nghĩa gì? *(Dùng để phân cách danh sách nhiều đường dẫn tìm kiếm Role khác nhau theo thứ tự ưu tiên từ trái qua phải.)*

---

### Câu 11 — Quản lý Tên Biến trong Role để Tránh Xung đột (Namespacing) ★★★
**Hỏi:** Tại sao việc đặt tên biến trong `defaults/main.yml` của Role bắt buộc phải có tiền tố tên Role (Role Prefix Namespacing)? Cho ví dụ.
**Đáp án chuẩn:** Vì Ansible lưu trữ tất cả các biến vào một không gian biến toàn cục (Global Variable Namespace). Nếu Role `webserver` đặt tên biến chung chung `port: 80` và Role `database` cũng đặt `port: 5432`, hai biến này sẽ ghi đè lẫn nhau gây ra lỗi cấu hình nghiêm trọng.
Giải pháp (Role Prefix Namespacing): Bắt buộc thêm tiền tố tên Role vào trước mọi biến: `webserver_port: 80` và `dbserver_port: 5432`.
**Tiêu chí chấm:**
- 0: Không biết kỹ thuật Role Prefix Namespacing.
- 1: Biết quy tắc đặt tên biến có tiền tố nhưng không giải thích được nguy cơ xung đột không gian biến toàn cục.
- 2: Phân tích chính xác cơ chế Global Variable Namespace và tác hại ghi đè biến chéo giữa các Role.
- 3: Nêu đúng + cho ví dụ chuẩn hóa tên biến cho 2 Role `nginx` và `postgresql`.
**Câu hỏi đào sâu:** Kỹ thuật này áp dụng cho loại biến nào trong Role? *(Áp dụng cho TOÀN BỘ các biến trong cả defaults, vars, và facts do Role tạo ra.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng khi Xây dựng Ansible Roles ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên xây dựng Ansible Roles chuyên nghiệp, chuẩn đóng gói và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Luôn dùng `ansible-galaxy role init` để tạo tự động cấu trúc Role chuẩn.
2. **Quy tắc 2:** Phân biệt đúng `defaults/` (biến tùy chỉnh cho phép đè) và `vars/` (hằng số nội bộ).
3. **Quy tắc 3:** Thêm tiền tố tên Role cho mọi tên biến để tránh xung đột Global Namespace.
4. **Quy tắc 4:** Sử dụng tham chiếu đường dẫn tương đối cho tệp trong `templates/` và `files/`.
5. **Quy tắc 5:** Đảm bảo Role độc lập (Portable Role) và kiểm thử Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy thiết kế mô-đun hạ tầng chuyên nghiệp.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào giúp ngăn ngừa lỗi biến bị ghi đè nhầm khi gọi nhiều Role? *(Quy tắc 3: Thêm tiền tố tên Role cho mọi tên biến.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm cấu trúc mã nguồn tự động hóa và xây dựng Ansible Roles, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi chuẩn hóa 100% mã nguồn hạ tầng theo kiến trúc mô-đun hóa Ansible Role chuyên nghiệp: sử dụng `ansible-galaxy role init` để khởi tạo khung 8 thư mục quy chuẩn, tách biệt rõ ràng giữa biến mặc định tùy chỉnh `defaults/main.yml` và hằng số nội bộ `vars/main.yml`. Tôi áp dụng kỹ thuật Role Prefix Namespacing để triệt tiêu hoàn toàn rủi ro xung đột biến toàn cục, và tận dụng cơ chế nạp tương đối cho các mẫu Jinja2 template. Mọi Role do tôi phát triển đều đảm bảo tính độc lập di động (Portable Role), đạt chỉ số `changed=0` Idempotent ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Phan Văn K | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Lê Thị M | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 15

Để chuẩn bị tốt nhất cho **Buổi 15: Roles Nâng cao — include_role, import_role, role dependencies**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Phân biệt sự khác nhau giữa việc nạp Role động `include_role` (Dynamic Re-use) và nạp Role tĩnh `import_role` (Static Re-use)?
2. **Nghiên cứu trước 2:** Khi nào thì nên dùng `include_role` bên trong một vòng lặp `loop:`?
3. **Nghiên cứu trước 3:** Làm thế nào để truyền danh sách biến phức tạp khi gọi `include_role` trong Task?

---


### [Chuyên Đề 15] Kỹ Thuật Role Nâng Cao: Role Dependencies, Search Paths, Parameterized Roles & Tái Cấu Trúc Playbook Quy Mô Lớn

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> So sánh sự khác nhau cốt lõi về thời điểm thi hành (Execution Time) và hành vi giữa <code>ansible.builtin.import_role</code> và <code>ansible.builtin.include_role</code>. *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>import_role</code> (Static Import): Nạp tĩnh tại thời điểm <b style="color: var(--accent-primary);">Parse Playbook</b> (Pre-parse). Toàn bộ các Task của Role được chèn trực tiếp vào cây Playbook trước khi chạy. Hỗ trợ đầy đủ cờ <code>tags</code> và <code>handlers</code> toàn cục.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>include_role</code> (Dynamic Include): Nạp động tại thời điểm <b style="color: var(--accent-primary);">Runtime</b> khi tiến trình chạy đến đúng Task đó. Cho phép kết hợp linh hoạt với vòng lặp <code>loop:</code> và điều kiện <code>when:</code>.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không phân biệt được <code>import_role</code> và <code>include_role</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết một cái tĩnh một cái động nhưng giải thích sai về thời điểm parse time vs runtime.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác sự khác biệt về Parse time vs Runtime và khả năng dùng với <code>loop:</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ kịch bản thực tế khi nào dùng <code>import_role</code> vs <code>include_role</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu muốn gọi 1 Role lặp qua một mảng danh sách IP, bắt buộc phải dùng module nào? *(Bắt buộc dùng <code>ansible.builtin.include_role</code>.)*
</div>
</details>

---

### Câu 2 — Tự động hóa Giải quyết Phụ thuộc với Role Dependencies 🔥
**Hỏi:** Cơ chế Role Dependencies trong tệp `meta/main.yml` hoạt động như thế nào? Nêu lợi ích của nó trong quản lý mô-đun hạ tầng Doanh nghiệp. *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
Cơ chế: Khi một Role chính (như `app_server`) khai báo danh sách các Role phụ thuộc (`dependencies: - role: common`) trong `meta/main.yml`, Ansible Engine sẽ **tự động nhận biết và thực thi toàn bộ các Role phụ thuộc đó TRƯỚC KHI các Task của Role chính chạy**.
Lợi ích: Đảm bảo 100% các máy chủ ứng dụng tự động được cài đặt sẵn hạ tầng nền tảng (như Security, NTP, Logging) mà không cần người dùng phải khai báo thủ công `role: common` trong mọi Playbook.
**Tiêu chí chấm:**
- 0: Không biết cơ chế Role Dependencies.
- 1: Biết dependency trong `meta` nhưng không giải thích được thứ tự ưu tiên thi hành trước Role chính.
- 2: Phân tích chính xác cơ chế tự động nạp trước và lợi ích chuẩn hóa hạ tầng Doanh nghiệp.
- 3: Nêu đúng + viết đoạn YAML minh họa file `meta/main.yml` khai báo dependency truyền biến.
**Câu hỏi đào sâu:** Mặc định, nếu 2 Role chính cùng phụ thuộc vào `role: common`, `role: common` sẽ chạy mấy lần? *(Mặc định chỉ chạy 1 LẦN duy nhất để tránh trùng lặp.)*

---

### Câu 3 — Sử dụng `include_role` trong Vòng lặp `loop:` 🔥
**Hỏi:** Trình bày cách kết hợp module `ansible.builtin.include_role` với từ khóa vòng lặp `loop:`. Tại sao không thể dùng `import_role` với `loop:`? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Cách kết hợp: Dùng `include_role` với `loop: {{ my_list }}` để nạp và thực thi lại Role cho từng phần tử trong danh sách, biến từng phần tử thành một bộ tham số đè cho Role.
- Không dùng được `import_role` với `loop:` vì `import_role` là nạp tĩnh ở thời điểm Parse Playbook (Pre-parse), lúc này các biến vòng lặp `loop:` chưa được Ansible Engine tính toán.
**Tiêu chí chấm:**
- 0: Lầm tưởng `import_role` dùng được với `loop:`.
- 1: Biết `include_role` đi được với `loop:` nhưng giải thích sai nguyên nhân parser của `import_role`.
- 2: Phân tích chính xác lý do pre-parse của `import_role` khiến nó không thể nhận biến `loop:`.
- 3: Nêu đúng + viết đoạn Playbook YAML minh họa lặp `include_role` tạo Virtual Hosts.
**Câu hỏi đào sâu:** Khi lồng `include_role` trong `loop:`, cần lưu ý thuộc tính nào để tránh ghi đè tên biến `item`? *(Sử dụng `loop_control: loop_var: my_custom_var`.)*

---

### Câu 4 — Chia nhỏ Task với `tasks_from:` 🔥
**Hỏi:** Thuộc tính `tasks_from:` trong `include_role` / `import_role` dùng để làm gì? Nêu trường hợp sử dụng thực tế. *(Liên quan QT 5.1)*
**Đáp án chuẩn:** Thuộc tính `tasks_from: <file.yml>` dùng để chỉ định nạp một tệp Task cụ thể nằm trong thư mục `tasks/` của Role thay vì tệp mặc định `tasks/main.yml`.
Trường hợp sử dụng: Khi Role được chia nhỏ thành nhiều công đoạn riêng biệt (như `install.yml`, `configure.yml`, `cleanup.yml`), người dùng có thể gọi riêng `tasks_from: cleanup.yml` để thực hiện tác vụ dọn dẹp mà không cần chạy lại toàn bộ tiến trình cài đặt.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `tasks_from:`.
- 1: Biết `tasks_from` chỉ file nhưng không cho được ví dụ thực tế chia nhỏ công đoạn.
- 2: Phân tích chính xác cơ chế chỉ định tệp entrypoint và tư duy chia nhỏ mã nguồn.
- 3: Nêu đúng + viết đoạn YAML minh họa nạp `tasks_from: configure.yml`.
**Câu hỏi đào sâu:** Có thể áp dụng tương tự cho tệp Handler và tệp Variable không? *(Có, sử dụng thuộc tính `handlers_from:` và `vars_from:`.)*

---

### Câu 5 — Truyền Biến Tùy chỉnh Nâng cao cho Role
**Hỏi:** Có những cách nào để truyền biến tùy chỉnh khi nạp Role bằng `include_role` hoặc `import_role`? Cách nào có độ ưu tiên cao nhất? *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
Có 2 cách truyền biến chính:
1. Truyền trực tiếp dưới từ khóa `vars:` của `include_role`:
   ```yaml
   include_role:
     name: webserver
   vars:
     webserver_port: 8080
   ```
2. Truyền dạng tham số inline: `include_role: name=webserver webserver_port=8080`.
Khối biến truyền trực tiếp dưới `vars:` của task nạp có **độ ưu tiên rất cao**, ghi đè toàn bộ các biến trong `defaults/main.yml` của Role.
**Tiêu chí chấm:**
- 0: Không biết cách truyền biến cho `include_role`.
- 1: Biết truyền biến nhưng không nắm được độ ưu tiên ghi đè của nó.
- 2: Phân tích chính xác các cú pháp truyền biến và thứ tự ưu tiên.
- 3: Nêu đúng + minh họa ví dụ truyền biến tùy chỉnh cho môi trường Production.
**Câu hỏi đào sâu:** Mặc định, các biến truyền vào `include_role` có bị rò rỉ (leak) sang các Task phía sau không? *(Mặc định có bị rò rỉ; muốn giới hạn phạm vi phải dùng cờ `public: false`.)*

---

### Câu 6 — Nạp Tệp Variable Theo Hệ điều hành với `vars_from:`
**Hỏi:** Làm thế nào để tự động nạp các tệp biến số khác nhau (`vars/RedHat.yml` vs `vars/Debian.yml`) trong Role dựa trên hệ điều hành của máy đích? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** Sử dụng thuộc tính `vars_from:` kết hợp với Ansible Facts `ansible_facts.os_family`:
```yaml
- name: Load OS specific variables
  ansible.builtin.include_role:
    name: common
    vars_from: "{{ ansible_facts.os_family }}.yml"
```
Ansible sẽ tự động giải mã biến và nạp đúng tệp `vars/RedHat.yml` trên CentOS/RHEL hoặc `vars/Debian.yml` trên Ubuntu.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `vars_from:`.
- 1: Biết `vars_from` nhưng không kết hợp được với facts `os_family`.
- 2: Phân tích chính xác cơ chế nạp biến đa nền tảng OS linh hoạt.
- 3: Nêu đúng + viết đoạn YAML minh họa hoàn chỉnh nạp biến OS.
**Câu hỏi đào sâu:** Nếu tệp `vars/Solaris.yml` không tồn tại khi chạy trên máy Solaris, Ansible sẽ xử lý ra sao? *(Ansible sẽ văng lỗi fatal `Could not find vars file` ngoại trừ khi dùng `first_available_file`.)*

---

### Câu 7 — Kiểm soát Nạp Trùng lặp với `allow_duplicates`
**Hỏi:** Mặc định khi một Role đã thi hành 1 lần, nếu Playbook gọi lại Role đó lần thứ 2, Ansible Engine sẽ xử lý thế nào? Làm sao để bắt buộc Role chạy lại? *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- Mặc định: Ansible Engine áp dụng cơ chế chống trùng lặp (`allow_duplicates: false`), sẽ **IM LẶNG BỎ QUA** lượt gọi thứ 2 để tiết kiệm tài nguyên.
- Muốn bắt buộc Role chạy lại: Khai báo thuộc tính `allow_duplicates: true` trong tệp `meta/main.yml` của Role đó.
**Tiêu chí chấm:**
- 0: Lầm tưởng Role luôn chạy lại ở mọi lần gọi.
- 1: Biết Role bị bỏ qua nhưng không nêu được thuộc tính `allow_duplicates` trong `meta/main.yml`.
- 2: Phân tích chính xác cơ chế chống trùng lặp mặc định và cách override bằng `allow_duplicates: true`.
- 3: Nêu đúng + cho ví dụ trường hợp thực tế cần `allow_duplicates: true` (như Role tạo tài khoản tạm).
**Câu hỏi đào sâu:** Nếu gọi cùng 1 Role 2 lần nhưng với 2 bộ tham số `vars:` KHÁC NHAU, Role có chạy lại không? *(Mặc định vẫn chạy lại vì bộ biến khác nhau được tính là invocation riêng.)*

---

### Câu 8 — Điều khiển Nạp Role theo Môi trường với `when:`
**Hỏi:** Trình bày kỹ thuật nạp Role linh hoạt theo môi trường triển khai (Dev/Prod) bằng thuộc tính `when:` trong `include_role`. *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
Kỹ thuật: Kết hợp `include_role` với điều kiện `when:` để kiểm tra biến môi trường `env_type`.
```yaml
- name: Deploy SSL Security Role on Production Only
  ansible.builtin.include_role:
    name: ssl_security
  when: env_type == 'production'
```
Ý nghĩa: Ngăn ngừa tuyệt đối việc thực thi các tác vụ Production đắt tiền hoặc nguy hiểm (như đăng ký SSL thật) trên các máy chủ Local Dev.
**Tiêu chí chấm:**
- 0: Không biết kết hợp `when:` với `include_role`.
- 1: Viết được `when:` nhưng nhầm lẫn dùng với `import_role` gây nạp tĩnh sai thời điểm.
- 2: Phân tích chính xác lợi ích nạp động runtime bảo vệ môi trường Dev/Prod.
- 3: Nêu đúng + viết ví dụ Playbook phân nhánh môi trường chuẩn hóa.
**Câu hỏi đào sâu:** Nếu dùng `import_role` với `when: env_type == 'production'`, cờ `when:` sẽ áp dụng cho cái gì? *(Cờ `when:` sẽ bị ép gắn vào TOÀN BỘ từng task riêng lẻ trong Role đó.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Advanced Roles 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook sử dụng nạp Role nâng cao để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (kỷ niệm mốc 50% khóa học).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-advanced-roles.yml`: Các Role nạp động/tĩnh thi hành và chép file báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-advanced-roles.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task nạp qua import/include đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/app-server.conf` kiểm tra nội dung file chứa đúng dữ liệu từ `include_role` loop.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và dòng log RECAP.
- 3: Trình bày xuất sắc 3 bước + tự tin khẳng định tiêu chí Idempotency mốc 50% khóa học.
**Câu hỏi đào sâu:** Việc nạp Role động với `include_role` trong vòng lặp `loop:` có làm trôi cờ Idempotency không? *(Hoàn toàn không, nếu các task bên trong chuẩn hóa `changed_when: false` cho task read-only.)*

---

### Câu 10 — Giới hạn Phạm vi Biến với `public: false` ★★★
**Hỏi:** Thuộc tính `public: false` trong module `ansible.builtin.include_role` có tác dụng gì đối với phạm vi biến (Variable Scope)?
**Đáp án chuẩn:** Mặc định (`public: true`), các biến và defaults được nạp từ `include_role` sẽ tồn tại và lan truyền (leak) sang tất cả các Task phía sau trong cùng một Play. Khi khai báo `public: false`, toàn bộ biến của Role đó sẽ **BỊ GIỚI HẠN PHẠM VI CHỈ NẰM TRONG BẢN THÂN ROLE ĐÓ**, giúp chống ô nhiễm không gian biến toàn cục của Playbook.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `public: false`.
- 1: Biết `public` liên quan đến biến nhưng không giải thích được hiện tượng rò rỉ biến (variable leakage).
- 2: Phân tích chính xác cơ chế phong tỏa phạm vi biến của `public: false`.
- 3: Nêu đúng + minh họa ví dụ ngăn chặn rò rỉ biến bằng `public: false`.
**Câu hỏi đào sâu:** Đối với `import_role` (Static), biến có mặc định bị rò rỉ không? *(Có, `import_role` luôn luôn làm rò rỉ biến ra toàn Playbook vì nó nạp ở Parse time.)*

---

### Câu 11 — Thừa hưởng Thẻ Tags với `apply:` trong `include_role` ★★★
**Hỏi:** Làm thế nào để áp dụng một thuộc tính task (như `tags:` hoặc `become:`) cho TOÀN BỘ các Task bên trong một Role nạp động bằng `include_role`?
**Đáp án chuẩn:** Sử dụng thuộc tính `apply:` bên trong `include_role`:
```yaml
- name: Include Webserver Role with global tags
  ansible.builtin.include_role:
    name: webserver
    apply:
      tags:
        - web_deploy
      become: true
```
Toàn bộ các Task được nạp động từ role `webserver` sẽ tự động thừa hưởng thẻ `tags: ['web_deploy']` và quyền `become: true`.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `apply:`.
- 1: Biết gắn tag cho include_role nhưng nhầm lẫn gắn trực tiếp làm tag chỉ áp dụng cho task include chứ không áp dụng cho các task con.
- 2: Phân tích chính xác vai trò truyền thuộc tính xuống các task con của `apply:`.
- 3: Nêu đúng + viết đoạn YAML minh họa dùng `apply: tags:`.
**Câu hỏi đào sâu:** Đối với `import_role` (Static), có cần dùng `apply:` để gắn tag cho task con không? *(Không cần, `import_role` nạp tĩnh nên gắn tag trực tiếp sẽ tự động lan xuống mọi task con.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Tổ chức Role Nâng cao ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên làm chủ các kỹ thuật nạp Role nâng cao chuyên nghiệp và chuẩn Idempotency nhất.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Chọn đúng module: dùng `import_role` cho static tags/handlers, dùng `include_role` cho `loop:` và `when:`.
2. **Quy tắc 2:** Khai báo tự động giải quyết phụ thuộc trong `meta/main.yml` (`dependencies:`).
3. **Quy tắc 3:** Chia nhỏ công đoạn bằng `tasks_from: <file.yml>` để tăng tính mô-đun hóa.
4. **Quy tắc 4:** Sử dụng `public: false` hoặc Role Prefix Namespacing để tránh rò rỉ và xung đột biến.
5. **Quy tắc 5:** Kiểm soát `allow_duplicates` và đảm bảo Lần 2 đạt `changed=0` Idempotent qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + tự tin khẳng định năng lực làm chủ Ansible mô-đun hóa mốc 50% khóa học.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp giúp Playbook chạy linh hoạt theo danh sách đối tượng? *(Quy tắc 1 và Quy tắc 3.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm kiến trúc kịch bản Ansible nâng cao và làm chủ nạp Role mô-đun hóa, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi làm chủ hoàn toàn kiến trúc tổ chức Ansible Role nâng cao: sử dụng chuẩn xác `import_role` cho nạp tĩnh kế thừa Handlers/Tags và `include_role` cho nạp động linh hoạt với vòng lặp `loop:` và phân nhánh môi trường `when:`. Tôi tự động hóa giải quyết phụ thuộc hạ tầng bằng Role Dependencies trong `meta/main.yml`, chia nhỏ công đoạn kịch bản qua `tasks_from:`, và phong tỏa phạm vi biến với `public: false`. Đạt mốc 50% hành trình tự động hóa, mọi kịch bản nạp Role nâng cao của tôi đều đảm bảo tính độc lập tuyệt đối, đạt chỉ số `changed=0` Idempotent ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–4 (Tủ) | Câu 5–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Nguyễn Văn A | 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Trần Thị B | 2 / 2 / 1 / 2 | 2 / 1 / 2 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 16

Chúc mừng học viên đã **ĐẠT MỐC 50% KHÓA HỌC (Buổi 01–15)**! Để chuẩn bị bước vào **Buổi 16: Ansible Galaxy — Quản lý Roles và Collections từ Galaxy**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Ansible Galaxy là gì? Lệnh CLI nào dùng để tìm kiếm và cài đặt một Role công đồng từ Galaxy?
2. **Nghiên cứu trước 2:** Tệp `requirements.yml` dùng để làm gì trong việc quản lý danh sách các Roles và Collections phụ thuộc của dự án?
3. **Nghiên cứu trước 3:** Lệnh CLI `ansible-galaxy install -r requirements.yml` có tác dụng gì khi triển khai dự án mới?

---


### [Chuyên Đề 16] Quản Trị Hệ Sinh Thái Ansible Galaxy: Cài Đặt, Xuất Bản, Versioning & Quản Lý requirements.yml Chuẩn Doanh Nghiệp

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Ansible Galaxy (galaxy.ansible.com) là gì? Việc khai thác kho tài nguyên công cộng Galaxy mang lại lợi ích gì cho các dự án tự động hóa Doanh nghiệp? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
Ansible Galaxy là kho tài nguyên công cộng chính thức lưu trữ hàng vạn Roles và Collections tự động hóa được đóng gói sẵn bởi Red Hat và cộng đồng kỹ sư toàn cầu.
Lợi ích Doanh nghiệp:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Tiết kiệm 90% thời gian phát triển: Tái sử dụng kịch bản đã được kiểm thử chuẩn hóa cho các dịch vụ phổ biến (Nginx, PostgreSQL, Kubernetes).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Chuẩn hóa chất lượng mã nguồn theo Best Practices của Red Hat.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Thúc đẩy khả năng chia sẻ và đóng góp mã nguồn mô-đun hóa trong cộng đồng.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không hiểu khái niệm Ansible Galaxy.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết Galaxy là nơi tải code nhưng không giải thích được các lợi ích quy mô Doanh nghiệp.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò kho tài nguyên công cộng và lợi ích tiết kiệm thời gian triển khai.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ lệnh CLI <code>ansible-galaxy search nginx</code> tìm kiếm tài nguyên.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Có thể xem thông tin tác giả và điểm đánh giá chất lượng của một Role trên Galaxy bằng lệnh CLI nào? *(Lệnh <code>ansible-galaxy role info <author.role_name></code>.)*
</div>
</details>

---

### Câu 2 — Vai trò của Tệp `requirements.yml` 🔥
**Hỏi:** Tệp `requirements.yml` trong dự án Ansible dùng để làm gì? Tại sao việc quản lý phụ thuộc qua `requirements.yml` lại quan trọng trong quy trình CI/CD? *(Liên quan QT 4.2)*
**Đáp án chuẩn:** Tệp `requirements.yml` là tệp định nghĩa danh sách tất cả các Roles và Collections phụ thuộc bên ngoài của dự án.
Tầm quan trọng trong CI/CD:
- Giúp mã nguồn Git repository của dự án siêu gọn nhẹ (không cần commit trực tiếp mã nguồn của các Role bên ngoài vào Git).
- Tự động hóa 100%: Pipeline CI/CD chỉ cần chạy 1 câu lệnh `ansible-galaxy install -r requirements.yml` để tự động kéo toàn bộ phụ thuộc chuẩn xác trước khi thi hành Playbook.
**Tiêu chí chấm:**
- 0: Không biết tệp `requirements.yml`.
- 1: Biết `requirements.yml` để tải role nhưng không giải thích được vai trò giữ Git gọn nhẹ và tích hợp CI/CD.
- 2: Phân tích chính xác cơ chế manifest file quản lý phụ thuộc tập trung.
- 3: Nêu đúng + viết đoạn YAML minh họa tệp `requirements.yml` chứa mục `roles:` và `collections:`.
**Câu hỏi đào sâu:** Sự khác biệt về cấu trúc khai báo giữa mảng `roles:` và mảng `collections:` trong `requirements.yml` là gì? *(Dạng `roles:` hỗ trợ thuộc tính `src`, `scm`, `version`; dạng `collections:` hỗ trợ thuộc tính `name`, `version`, `source`.)*

---

### Câu 3 — Cài đặt Phụ thuộc với `ansible-galaxy install -r` 🔥
**Hỏi:** Trình bày câu lệnh CLI cài đặt toàn bộ phụ thuộc từ tệp `requirements.yml`. Giải thích ý nghĩa của cờ tham số `-r` và `--force`. *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Lệnh cài đặt: `ansible-galaxy install -r requirements.yml` (cho Roles) hoặc `ansible-galaxy collection install -r requirements.yml` (cho Collections).
- Cờ `-r` (`--role-file` / `--requirements`): Chỉ định đường dẫn tới tệp định nghĩa phụ thuộc `requirements.yml`.
- Cờ `--force`: Ép Ansible Galaxy tải và ghi đè cài đặt lại toàn bộ các Role/Collection đã có sẵn trên đĩa cứng local (dùng khi muốn cập nhật code mới).
**Tiêu chí chấm:**
- 0: Không biết lệnh `ansible-galaxy install -r`.
- 1: Biết lệnh install nhưng không giải thích được ý nghĩa cờ `-r` và cờ ghi đè `--force`.
- 2: Phân tích chính xác câu lệnh CLI và ý nghĩa từng cờ tham số.
- 3: Nêu đúng + minh họa câu lệnh thực thi cài đặt trong pipeline build tự động.
**Câu hỏi đào sâu:** Nếu không có cờ `--force`, chuyện gì xảy ra khi cài đặt một Role đã tồn tại sẵn trong thư mục `./roles`? *(Ansible Galaxy sẽ im lặng bỏ qua không tải lại với thông báo `is already installed, skipping`.)*

---

### Câu 4 — Kỹ thuật Chốt Phiên bản (Version Pinning) 🔥
**Hỏi:** Kỹ thuật Version Pinning trong `requirements.yml` là gì? Tại sao việc chốt phiên bản lại là nguyên tắc sinh tử khi sử dụng tài nguyên công cộng từ Galaxy? *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
Kỹ thuật Version Pinning là việc khai báo cố định một phiên bản cụ thể (ví dụ `version: "3.1.0"`) hoặc dải phiên bản an toàn (ví dụ `version: ">=2.0.0,<3.0.0"`) cho các Role/Collection trong `requirements.yml`.
Nguyên tắc sinh tử: Tác giả của Role trên Galaxy có thể phát hành phiên bản mới chứa breaking changes (thay đổi cấu trúc đứt gãy). Nếu không chốt phiên bản, kịch bản tự động hóa của Doanh nghiệp có thể bị crash đột ngột khi chạy trên server mới do tự động tải bản code mới không tương thích.
**Tiêu chí chấm:**
- 0: Không hiểu khái niệm Version Pinning.
- 1: Biết ghi version nhưng không nêu được nguy cơ rủi ro rách việc do breaking changes từ tác giả Galaxy.
- 2: Phân tích chính xác vai trò chốt phiên bản bảo vệ tính ổn định lâu dài của mã nguồn IaC.
- 3: Nêu đúng + minh họa các cú pháp khai báo `version:` chuẩn trong `requirements.yml`.
**Câu hỏi đào sâu:** Nếu muốn chấp nhận tất cả các bản vá lỗi (patch updates) của phiên bản 3.1.x nhưng không muốn lên 3.2.0, ta viết `version:` ra sao? *(Viết `version: "~>3.1.0"` hoặc `version: ">=3.1.0,<3.2.0"`.)*

---

### Câu 5 — Cô lập Đường dẫn Cài đặt trong `ansible.cfg` 🔥
**Hỏi:** Tại sao quản trị viên bắt buộc phải cấu hình `roles_path = ./roles` và `collections_path = ./collections` trong tệp `ansible.cfg` của dự án? *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
Vì mặc định Ansible Galaxy sẽ cài đặt tất cả các tài nguyên tải về vào thư mục cá nhân người dùng (`~/.ansible/roles`).
Lý do cô lập:
1. Tránh ô nhiễm môi trường: Ngăn ngừa việc 2 dự án Ansible trên cùng 1 server ghi đè làm hỏng Role của nhau.
2. Quản lý độc lập: Giúp dự án tự chứa (Self-contained) toàn bộ tài nguyên lưu ngay tại thư mục làm việc local.
**Tiêu chí chấm:**
- 0: Không biết cấu hình `roles_path` trong `ansible.cfg`.
- 1: Biết thuộc tính `roles_path` nhưng không giải thích được nguy cơ xung đột giữa các dự án trên cùng server.
- 2: Phân tích chính xác tư duy cô lập môi trường dự án tự chứa (Self-contained Project).
- 3: Nêu đúng + viết đoạn mã cấu hình thuộc tính `roles_path` và `collections_path` trong `ansible.cfg`.
**Câu hỏi đào sâu:** Làm thế nào để kiểm tra danh sách các đường dẫn mà Ansible đang tìm kiếm Role? *(Dùng lệnh `ansible-config dump | grep ROLES_PATH`.)*

---

### Câu 6 — Nạp Role từ Git Repository Cá nhân
**Hỏi:** Ngoài kho công cộng Galaxy, làm thế nào để khai báo tải một Role nội bộ bảo mật từ Gitlab/Github riêng tư của Doanh nghiệp trong `requirements.yml`? *(Liên quan QT 5.3)*
**Đáp án chuẩn:** Khai báo thông số `src` chỉ tới đường dẫn Git SSH/HTTP, `scm: git`, và `version:` chỉ tới branch/tag:
```yaml
roles:
  - src: git@gitlab.company.com:ansible-roles/role-security.git
    scm: git
    version: v1.2.0
    name: company_security
```
Điều kiện: Máy Control Node phải được cấp quyền truy cập SSH Key để clone repo riêng tư đó.
**Tiêu chí chấm:**
- 0: Lầm tưởng `requirements.yml` chỉ tải được từ kho công cộng Galaxy.
- 1: Biết nạp từ Git nhưng không nêu được các từ khóa `src`, `scm: git`, `version`.
- 2: Phân tích chính xác cơ chế nạp Role riêng tư từ Gitlab/Github Enterprise.
- 3: Nêu đúng + viết đoạn YAML chuẩn khai báo nạp Role từ Gitlab riêng tư.
**Câu hỏi đào sâu:** Cụm từ `name: company_security` trong khai báo trên có tác dụng gì? *(Dùng để đổi tên thư mục Role tải về thành `company_security` trong thư mục `./roles`.)*

---

### Câu 7 — Quản lý Hạ tầng Offline Air-Gapped với Galaxy
**Hỏi:** Trong môi trường trung tâm dữ liệu bảo mật cao bị ngắt hoàn toàn Internet (Air-gapped Network), làm thế nào để cài đặt các Roles/Collections từ Galaxy? *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
Quy trình 2 bước:
1. **Tại máy ngoài có mạng Internet:** Sử dụng lệnh `ansible-galaxy role download <role_name>` hoặc tải tệp nén tarball `.tar.gz` chứa mã nguồn Role/Collection.
2. **Chuyển tệp vào máy Air-gapped:** Chép tệp `.tar.gz` qua ổ đĩa an toàn vào Control Node local và chạy lệnh cài đặt offline:
   `ansible-galaxy role install ./downloads/geerlingguy-nginx-3.1.0.tar.gz`
**Tiêu chí chấm:**
- 0: Cho rằng không thể cài đặt tài nguyên Galaxy trong môi trường Air-gapped.
- 1: Biết tải file tarball nhưng không nêu được câu lệnh CLI cài đặt từ file `.tar.gz` local.
- 2: Phân tích chính xác quy trình 2 bước triển khai offline cho Air-gapped Network.
- 3: Nêu đúng + viết câu lệnh CLI cài đặt từ tệp nén tarball offline.
**Câu hỏi đào sâu:** Cần lưu ý điều gì về các Role phụ thuộc (dependencies) khi cài đặt offline từ tệp tarball? *(Phải tải thủ công đầy đủ tất cả các tệp tarball của các Role phụ thuộc.)*

---

### Câu 8 — Gọi Tài nguyên Galaxy trong Playbook
**Hỏi:** Sau khi đã tải các Roles và Collections từ Galaxy về thư mục local, làm thế nào để gọi và áp dụng chúng trong Playbook `site-galaxy.yml`? *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
Khai báo từ khóa `collections:` và `roles:` ở cấp Playbook:
```yaml
- name: Apply Galaxy Resources
  hosts: web
  become: true
  collections:
    - community.general
  roles:
    - role: geerlingguy.nginx
      vars:
        nginx_http_port: 8080
```
**Tiêu chí chấm:**
- 0: Không biết cách gọi tài nguyên Galaxy trong Playbook.
- 1: Biết gọi `roles:` nhưng nhầm lẫn tên Role trên đĩa làm Ansible không nạp được.
- 2: Phân tích chính xác cú pháp gọi Collection và Role nạp từ Galaxy.
- 3: Nêu đúng + viết ví dụ Playbook hoàn chỉnh gọi Role Galaxy truyền biến tùy chỉnh.
**Câu hỏi đào sâu:** Tại sao tên Role tải từ Galaxy thường có dạng `username.rolename` (như `geerlingguy.nginx`)? *(Đó là chuẩn phân biệt không gian tên Namespace của Ansible Galaxy để chống trùng tên.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Galaxy Roles 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook sử dụng Roles/Collections tải từ Ansible Galaxy để đảm bảo tính Idempotency và máy đích ở đúng trạng thái.
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-galaxy.yml`: Các Task trong Role Galaxy thực thi và cài đặt ứng dụng báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-galaxy.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task trong Role Galaxy đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/galaxy-demo.conf` kiểm tra file cấu hình thực sự tồn tại và chứa đúng tham số đã render.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file render.
- 3: Trình bày xuất sắc 3 bước + cho ví dụ thực tế lệnh `docker exec cat` kiểm tra kết quả từ Role Galaxy.
**Câu hỏi đào sâu:** Làm sao để biết một Role trên Galaxy có đạt chuẩn Idempotency trước khi tải về dùng? *(Xem điểm đánh giá Quality Score và chỉ số CI Build Status trên trang galaxy.ansible.com.)*

---

### Câu 10 — Tệp Nạp Cấu hình Nâng cao `ansible-galaxy.yml` ★★★
**Hỏi:** Tệp `ansible-galaxy.yml` khác tệp `requirements.yml` ở điểm cốt lõi nào?
**Đáp án chuẩn:**
- `requirements.yml`: Dùng cho **NGƯỜI DÙNG (Consumer)** để khai báo danh sách các Roles/Collections phụ thuộc cần tải về dự án.
- `ansible-galaxy.yml` (hoặc `galaxy.yml`): Dùng cho **TÁC GIẢ (Author/Publisher)** để định nghĩa siêu dữ liệu (namespace, name, version, readme) khi đóng gói và xuất bản một Collection mới lên Ansible Galaxy.
**Tiêu chí chấm:**
- 0: Nhầm lẫn giữa `requirements.yml` và `galaxy.yml`.
- 1: Biết 2 file khác nhau nhưng không phân biệt được góc độ Consumer vs Publisher.
- 2: Phân tích chính xác vai trò Consumer tải về vs Publisher xuất bản Collection.
- 3: Nêu đúng + viết các trường siêu dữ liệu chính trong tệp `galaxy.yml`.
**Câu hỏi đào sâu:** Lệnh CLI nào dùng để đóng gói một Collection từ tệp `galaxy.yml` thành tệp nén tarball? *(Lệnh `ansible-galaxy collection build`.)*

---

### Câu 11 — Xử lý Xung đột Phiên bản Phụ thuộc (Dependency Resolution) ★★★
**Hỏi:** Khi 2 Collections trong `requirements.yml` cùng phụ thuộc vào một Collection thứ 3 nhưng yêu cầu 2 phiên bản khác nhau, Ansible Galaxy sẽ xử lý ra sao?
**Đáp án chuẩn:** Ansible Galaxy có thuật toán giải quyết phụ thuộc (Dependency Resolver). Nó sẽ cố gắng tìm một phiên bản chung duy nhất thỏa mãn tất cả các điều kiện ràng buộc phiên bản (Version Constraints). Nếu không tìm thấy phiên bản thỏa mãn đồng thời, lệnh `ansible-galaxy install` sẽ dừng và báo lỗi `Dependency resolution failed conflict`.
**Tiêu chí chấm:**
- 0: Không biết cơ chế xử lý xung đột phiên bản của Galaxy.
- 1: Biết văng lỗi nhưng không giải thích được nguyên lý tìm phiên bản giao thoa của Dependency Resolver.
- 2: Phân tích chính xác thuật toán Dependency Resolver và lý do báo lỗi xung đột phiên bản.
- 3: Nêu đúng + đưa ra giải pháp điều chỉnh dải phiên bản trong `requirements.yml` để khắc phục lỗi.
**Câu hỏi đào sâu:** Cờ tham số nào cho phép bỏ qua kiểm tra dependency khi cài đặt Collection? *(Cờ `--ignore-with-deps` hoặc `--no-deps`.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng khi Khai thác Ansible Galaxy ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên khai thác tài nguyên Ansible Galaxy chuyên nghiệp, an toàn bảo mật và chuẩn Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Quản lý tập trung 100% phụ thuộc qua tệp `requirements.yml`.
2. **Quy tắc 2:** Luôn chốt phiên bản (Version Pinning) cố định để chống đứt gãy code.
3. **Quy tắc 3:** Cô lập đường dẫn cài đặt `./roles` và `./collections` trong `ansible.cfg`.
4. **Quy tắc 4:** Kiểm tra mã nguồn (Code Audit) các Role công cộng trước khi đưa vào Production.
5. **Quy tắc 5:** Tự động hóa cài đặt bằng `install -r` trong CI/CD và kiểm thử Lần 2 `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy quản lý tài nguyên IaC chuyên nghiệp Doanh nghiệp.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp bảo vệ an toàn thông tin hạ tầng Doanh nghiệp? *(Quy tắc 4: Kiểm tra mã nguồn Code Audit trước khi chạy Production.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm khai thác kho tài nguyên mở và quản lý phụ thuộc trong Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi khai thác tối đa sức mạnh của kho tài nguyên mở Ansible Galaxy để tăng tốc độ triển khai hạ tầng gấp 10 lần: quản lý tập trung 100% các Roles và Collections phụ thuộc thông qua tệp định nghĩa `requirements.yml` chuẩn hóa, áp dụng nghiêm ngặt kỹ thuật Version Pinning để triệt tiêu hoàn toàn rủi ro đứt gãy kịch bản do breaking changes. Tôi cô lập hoàn toàn môi trường lưu trữ qua `roles_path` trong `ansible.cfg`, thiết lập quy trình kiểm tra mã nguồn (Code Audit) bảo mật cho mọi tài nguyên công cộng, tự động hóa cài đặt bằng `ansible-galaxy install -r` trong pipeline CI/CD, đảm bảo ở lượt chạy Lần hai đạt `changed=0` Idempotent và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Hoàng Văn P | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Đặng Thị Q | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 17

Để chuẩn bị tốt nhất cho **Buổi 17: Collections và FQCN — Fully Qualified Collection Name**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Khái niệm FQCN (Fully Qualified Collection Name) trong Ansible 2.9+ là gì? Cho ví dụ minh họa FQCN của module `copy` và module `user`.
2. **Nghiên cứu trước 2:** Khác biệt lớn nhất về mặt cấu trúc lưu trữ giữa một Ansible Role truyền thống và một Ansible Collection là gì?
3. **Nghiên cứu trước 3:** Tại sao Red Hat khuyến nghị bắt buộc phải sử dụng FQCN thay vì tên short-name module cũ trong các Playbook Enterprise?

---


### [Chuyên Đề 17] Ansible Collections & Fully Qualified Collection Name (FQCN): Tách Biệt Core Engine & Tích Hợp Đa Nền Tảng Đám Mây

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> FQCN (Fully Qualified Collection Name) là gì? Hãy phân tích cấu trúc 3 thành phần quy chuẩn của một tên FQCN và cho ví dụ. *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
FQCN là chuẩn đặt tên định danh đầy đủ giúp Ansible Engine xác định chính xác tuyệt đối vị trí mã nguồn của module/plugin.
Cấu trúc 3 thành phần: <code><namespace>.<collection_name>.<plugin_name></code>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code><namespace></code>: Không gian tên của nhà phát triển (ví dụ: <code>ansible</code>, <code>community</code>, <code>amazon</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code><collection_name></code>: Tên bộ sưu tập (ví dụ: <code>builtin</code>, <code>general</code>, <code>aws</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code><plugin_name></code>: Tên module/plugin thi hành (ví dụ: <code>copy</code>, <code>ini_file</code>, <code>ec2_instance</code>).</div>
Ví dụ: <code>ansible.builtin.copy</code> hoặc <code>community.general.ini_file</code>.
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không hiểu khái niệm FQCN.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết FQCN nhưng không phân tích được 3 thành phần <code>namespace.collection.plugin</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác cấu trúc 3 thành phần và nêu lý do chống xung đột module.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + viết ví dụ 3 tên FQCN thực tế cho module Core, Community và Cloud.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Từ phiên bản Ansible nào trở đi Red Hat khuyến nghị bắt buộc phải dùng FQCN? *(Từ Ansible 2.9 và Ansible Core 2.10 trở đi.)*
</div>
</details>

---

### Câu 2 — Khái niệm Ansible Collection 🔥
**Hỏi:** Ansible Collection là gì? Nó khác biệt gì so với một Ansible Role truyền thống về mặt đóng gói nội dung? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- Ansible Collection là định dạng đóng gói nội dung tự động hóa thế hệ mới của Red Hat.
- Khác biệt đóng gói:
  + Ansible Role truyền thống: Chỉ đóng gói Tasks, Handlers, Templates và Files.
  + Ansible Collection: Đóng gói **TOÀN BỘ HỆ SINH THÁI** gồm Modules (Python code), Action Plugins, Filter Plugins, Lookup Plugins, Roles, và cả Playbooks mẫu vào duy nhất 1 gói nén.
**Tiêu chí chấm:**
- 0: Lầm tưởng Ansible Collection chỉ là một dạng khác của Role.
- 1: Biết Collection lớn hơn Role nhưng không liệt kê được các loại Plugins và Modules nó chứa.
- 2: Phân tích chính xác khái niệm Collection và sự khác biệt về phạm vi đóng gói nội dung.
- 3: Nêu đúng + vẽ sơ đồ cây thư mục cấu trúc của 1 Collection (`plugins/modules/`, `plugins/filter/`, `roles/`).
**Câu hỏi đào sâu:** Tại sao Red Hat lại tách các Module ra khỏi bộ nhân `ansible-core` để đưa vào các Collections? *(Để các nhà cung cấp như VMware, AWS, Cisco có thể độc lập phát hành và update module mà không cần chờ chu kỳ phát hành của Ansible Core.)*

---

### Câu 3 — Lý do Bắt buộc Chuyển đổi sang FQCN 🔥
**Hỏi:** Tại sao trong các kịch bản Ansible Enterprise mới, quản trị viên bắt buộc phải viết `ansible.builtin.copy` thay vì viết `copy:` như trước đây? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
Lý do bắt buộc:
1. **Triệt tiêu 100% xung đột tên module:** Nếu có 2 Collection cùng có module tên `copy`, dùng FQCN `ansible.builtin.copy` giúp Ansible Engine gọi đúng module cốt lõi của Ansible Core.
2. **Tăng tốc độ thực thi:** Ansible Engine không phải mất thêm tài nguyên tìm kiếm và tra cứu bảng ánh xạ tên ngắn sang FQCN.
3. **Đảm bảo tính tương thích lâu dài:** Sẵn sàng cho các phiên bản Ansible Core tương lai khi tên ngắn bị loại bỏ hoàn toàn.
**Tiêu chí chấm:**
- 0: Cho rằng gõ tên ngắn `copy:` hay FQCN `ansible.builtin.copy:` cũng hoàn toàn giống hệt nhau.
- 1: Biết FQCN tốt hơn nhưng không giải thích được lý do triệt tiêu xung đột module và hiệu năng parse.
- 2: Phân tích chính xác 3 lý do kỹ thuật bắt buộc phải dùng FQCN trong Enterprise.
- 3: Nêu đúng + minh họa so sánh kịch bản dùng Short-name vs FQCN.
**Câu hỏi đào sâu:** Nếu gõ nhầm `ansible.copy:` (thiếu `builtin`), Ansible Engine sẽ báo lỗi gì? *(Báo lỗi `Could not resolve module/action 'ansible.copy'`.)*

---

### Câu 4 — Sử dụng Từ khóa `collections:` Directive 🔥
**Hỏi:** Trình bày tác dụng của từ khóa `collections:` ở cấp Playbook. Khi nào nên dùng và khi nào KHÔNG nên lạm dụng từ khóa này? *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- Tác dụng: Khai báo danh sách các không gian tên Collection (như `collections: - community.general`), cho phép rút ngắn cú pháp gọi module trong Playbook mà không cần gõ tiền tố FQCN dài ở từng Task.
- Khi nên dùng: Khi một Playbook gọi hàng chục module thuộc cùng 1 Collection ngoài (như `community.general`).
- Khi KHÔNG lạm dụng: Trong các dự án Doanh nghiệp lớn có nhiều Collection trùng tên module, lạm dụng `collections:` có thể gây nhầm lẫn thứ tự ưu tiên giải mã module.
**Tiêu chí chấm:**
- 0: Không biết từ khóa `collections:` directive.
- 1: Biết `collections:` để rút ngắn code nhưng không nêu được nguy cơ rủi ro khi có module trùng tên.
- 2: Phân tích chính xác cơ chế giải mã module của `collections:` directive và trường hợp áp dụng.
- 3: Nêu đúng + viết đoạn YAML minh họa dùng `collections:` ở cấp Playbook.
**Câu hỏi đào sâu:** Từ khóa `collections:` có tác dụng tự động tải Collection từ mạng về không? *(Không, Collection phải được cài đặt sẵn trước đó qua requirements.yml.)*

---

### Câu 5 — Tra cứu Tài liệu FQCN với `ansible-doc` 🔥
**Hỏi:** Nêu câu lệnh CLI `ansible-doc` để tra cứu tài liệu và xem ví dụ mẫu của module `ansible.builtin.file`. Giải thích ý nghĩa của cờ `-s`. *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Lệnh tra cứu đầy đủ: `ansible-doc ansible.builtin.file`
- Lệnh xem ví dụ mẫu ngắn gọn: `ansible-doc ansible.builtin.file -s`
- Ý nghĩa cờ `-s` (`--snippet`): Chỉ in ra đoạn mã mẫu cú pháp YAML (Snippet) của module với các tham số chính, giúp copy nhanh vào Playbook mà không cần đọc toàn bộ mô tả lý thuyết dài.
**Tiêu chí chấm:**
- 0: Không biết lệnh `ansible-doc`.
- 1: Biết lệnh `ansible-doc` nhưng gõ short-name hoặc không giải thích được cờ `-s`.
- 2: Phân tích chính xác câu lệnh CLI tra cứu FQCN và vai trò của cờ `-s`.
- 3: Nêu đúng + thực thi lệnh CLI minh họa tra cứu tài liệu `ansible.builtin.file` trên terminal.
**Câu hỏi đào sâu:** Làm thế nào để liệt kê toàn bộ các module có sẵn trong Collection `community.general` bằng `ansible-doc`? *(Chạy lệnh `ansible-doc -l community.general`.)*

---

### Câu 6 — Sử dụng FQCN cho Plugins
**Hỏi:** Ngoài Module, chuẩn FQCN được áp dụng cho các loại Plugin nào khác trong Ansible Playbook? Cho ví dụ với Lookup Plugin. *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
Chuẩn FQCN áp dụng đồng bộ cho tất cả các loại Plugins: Lookup Plugins, Filter Plugins, Action Plugins, Connection Plugins, và Callback Plugins.
Ví dụ Lookup Plugin đọc biến môi trường:
- Cũ: `{{ lookup('env', 'PATH') }}`
- Chuẩn FQCN: `{{ lookup('ansible.builtin.env', 'PATH') }}`
Ví dụ Filter Plugin: `{{ my_dict | ansible.builtin.to_nice_json }}`.
**Tiêu chí chấm:**
- 0: Lầm tưởng FQCN chỉ áp dụng cho Module.
- 1: Biết FQCN dùng cho Plugin nhưng không viết được cú pháp FQCN cho Lookup Plugin.
- 2: Phân tích chính xác tính đồng nhất FQCN cho toàn bộ hệ thống Plugins.
- 3: Nêu đúng + viết ví dụ YAML minh họa dùng FQCN cho cả Module, Filter và Lookup Plugin trong 1 Playbook.
**Câu hỏi đào sâu:** Tại sao nên dùng FQCN cho Filter Plugin `ansible.builtin.to_nice_yaml`? *(Để tránh xung đột nếu dự án có một custom filter trùng tên `to_nice_yaml`.)*

---

### Câu 7 — Triệt tiêu Rủi ro Module Name Collision
**Hỏi:** Bài toán Module Name Collision (xung đột tên module) là gì? FQCN giải quyết triệt để bài toán này ra sao? *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
Module Name Collision xảy ra khi hệ thống cài đặt 2 Collections khác nhau nhưng cùng chứa 1 module trùng tên (ví dụ `amazon.aws.ec2` vs `community.aws.ec2`). Nếu người dùng viết short-name `ec2:`, Ansible Engine sẽ nạp nhầm module tùy theo thứ tự ưu tiên đường dẫn đĩa cứng, gây ra lỗi thực thi nghiêm trọng.
FQCN giải quyết bằng cách ép buộc chỉ định chính xác nhà phát triển: `amazon.aws.ec2` hoặc `community.aws.ec2`, triệt tiêu 100% sự nhập nhằng.
**Tiêu chí chấm:**
- 0: Không hiểu khái niệm Module Name Collision.
- 1: Biết xung đột tên nhưng không giải thích được cơ chế định danh duy nhất của FQCN.
- 2: Phân tích chính xác bài toán xung đột tên module và giải pháp triệt để của FQCN.
- 3: Nêu đúng + cho ví dụ thực tế xung đột giữa module AWS hoặc VMware.
**Câu hỏi đào sâu:** Nếu trong 1 Playbook có khai báo `collections: - community.aws` và `collections: - amazon.aws`, module short-name `ec2:` sẽ nạp cái nào? *(Nạp Collection được khai báo ĐẦU TIÊN trong danh sách `collections:`.)*

---

### Câu 8 — Cài đặt Collections Phụ thuộc qua `requirements.yml`
**Hỏi:** Trình bày cấu trúc khai báo cài đặt Collection `community.general` trong `requirements.yml` và câu lệnh CLI để tự động cài đặt. *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
- Cấu trúc `requirements.yml`:
  ```yaml
  collections:
    - name: community.general
      version: ">=7.0.0"
  ```
- Câu lệnh CLI cài đặt:
  `ansible-galaxy collection install -r requirements.yml`
**Tiêu chí chấm:**
- 0: Không biết cách khai báo Collection trong `requirements.yml`.
- 1: Viết được YAML nhưng nhầm lệnh `ansible-galaxy install` (thiếu từ khóa `collection`).
- 2: Phân tích chính xác cấu trúc YAML và câu lệnh CLI cài đặt Collection.
- 3: Nêu đúng + minh họa câu lệnh cài đặt cô lập vào thư mục `./collections` của dự án.
**Câu hỏi đào sâu:** Thư mục lưu trữ mặc định của Collections khi cài đặt cô lập trong dự án được cấu hình ở thuộc tính nào của `ansible.cfg`? *(Thuộc tính `collections_path = ./collections`.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng FQCN 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook sử dụng 100% module FQCN để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective RHCE EX294 #12).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-fqcn.yml`: Các module FQCN `ansible.builtin.*` và `community.general.*` thực thi và chép file báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-fqcn.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task FQCN đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/fqcn-app.conf` kiểm tra file cấu hình thực sự tồn tại đúng dữ liệu từ module FQCN.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file render.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE EX294 #12 (`☑`).
**Câu hỏi đào sâu:** Việc chuyển đổi từ short-name sang FQCN có làm thay đổi logic kiểm tra checksum SHA1 của module `ansible.builtin.copy` không? *(Hoàn toàn không, checksum SHA1 vẫn được so sánh chuẩn xác.)*

---

### Câu 10 — Công cụ `ansible-lint` Kiểm tra Cú pháp FQCN ★★★
**Hỏi:** Công cụ `ansible-lint` là gì? Cờ kiểm tra `fqcn[action]` trong `ansible-lint` có tác dụng gì đối với việc chuẩn hóa mã nguồn tự động hóa?
**Đáp án chuẩn:**
- `ansible-lint`: Là công cụ phân tích mã nguồn tĩnh (Static Code Analyzer) chính thức của Red Hat giúp kiểm tra tiêu chuẩn chất lượng và Best Practices của Playbook.
- Cờ `fqcn[action]`: Tự động quét và phát hiện tất cả các Task vẫn còn sử dụng tên module ngắn cũ (như `copy:`, `file:`), và cảnh báo ép người viết phải refactor sang chuẩn FQCN `ansible.builtin.copy`.
**Tiêu chí chấm:**
- 0: Không biết công cụ `ansible-lint`.
- 1: Biết `ansible-lint` check code nhưng không giải thích được rule `fqcn[action]`.
- 2: Phân tích chính xác vai trò quét mã nguồn tĩnh và ép chuẩn FQCN trong CI/CD pipeline.
- 3: Nêu đúng + viết lệnh CLI `ansible-lint site-fqcn.yml` chạy kiểm tra.
**Câu hỏi đào sâu:** Có thể tự động sửa lỗi FQCN short-name bằng `ansible-lint` không? *(Có thể dùng cờ `ansible-lint --write` để tự động refactor short-name sang FQCN.)*

---

### Câu 11 — Tự Tạo Một Ansible Collection Nội bộ ★★★
**Hỏi:** Lệnh CLI nào dùng để khởi tạo cấu trúc khung của một Ansible Collection mới? Cấu trúc thư mục của nó khác gì so với Role?
**Đáp án chuẩn:**
- Lệnh khởi tạo: `ansible-galaxy collection init <namespace>.<collection_name>` (ví dụ `ansible-galaxy collection init my_company.my_tools`).
- Khác biệt cấu trúc:
  + Role: Khung thư mục phẳng chứa `tasks/`, `handlers/`, `templates/`.
  + Collection: Thư mục phân cấp chứa `plugins/modules/`, `plugins/filter/`, `plugins/lookup/`, `roles/`, và tệp siêu dữ liệu `galaxy.yml`.
**Tiêu chí chấm:**
- 0: Không biết lệnh `ansible-galaxy collection init`.
- 1: Biết lệnh init nhưng không nêu được cấu trúc thư mục phân cấp `plugins/` của Collection.
- 2: Phân tích chính xác câu lệnh CLI khởi tạo và cấu trúc đa tầng của Collection.
- 3: Nêu đúng + cho ví dụ minh họa tạo Collection nội bộ Doanh nghiệp `company.core`.
**Câu hỏi đào sâu:** Tệp siêu dữ liệu chính của Collection mới tạo tên là gì? *(Tệp `galaxy.yml`.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Sử dụng FQCN và Collections ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên áp dụng chuẩn FQCN và Collections chuyên nghiệp, an toàn bảo mật và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Viết 100% FQCN `ansible.builtin.*` cho tất cả các module hệ thống cốt lõi.
2. **Quy tắc 2:** Sử dụng `ansible-doc <FQCN> -s` để tra cứu cú pháp và ví dụ chuẩn từ CLI.
3. **Quy tắc 3:** Quản lý tập trung Collections mở rộng qua `requirements.yml` và cô lập trong `ansible.cfg`.
4. **Quy tắc 4:** Sử dụng `ansible-lint` trong CI/CD để chặn 100% kịch bản dùng tên ngắn cũ.
5. **Quy tắc 5:** Triệt tiêu hoàn toàn rủi ro xung đột module và đảm bảo Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy chuẩn hóa mã nguồn IaC cấp Enterprise.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp tự động hóa việc gác cổng chất lượng mã nguồn? *(Quy tắc 4: Sử dụng `ansible-lint` trong CI/CD.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về tiêu chuẩn viết mã Ansible hiện đại và làm chủ FQCN / Collections, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi chuẩn hóa 100% mã nguồn Ansible theo tiêu chuẩn Red Hat Enterprise modern IaC: sử dụng tên định danh đầy đủ FQCN (`ansible.builtin.*` và `namespace.collection.*`) cho toàn bộ Modules, Filters và Lookup Plugins để triệt tiêu 100% rủi ro xung đột tên gọi module và tăng hiệu năng parse của Ansible Engine. Tôi làm chủ công cụ tra cứu CLI `ansible-doc`, quản lý tập trung Collections mở rộng qua `requirements.yml` cô lập trong `ansible.cfg`, tích hợp `ansible-lint` gác cổng chất lượng CI/CD, đảm bảo mọi kịch bản FQCN đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Đỗ Văn K | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Trịnh Thị L | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 18

Để chuẩn bị tốt nhất cho **Buổi 18: include vs import — static vs dynamic re-use**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Phân biệt sự khác nhau giữa `include_tasks` vs `import_tasks` và `include_playbook` vs `import_playbook`?
2. **Nghiên cứu trước 2:** Tại sao khi dùng `import_tasks` (Static), ta không thể sử dụng biến được tạo ra ở Runtime (như biến từ `register`) trong điều kiện `when:`?
3. **Nghiên cứu trước 3:** Khi nào thì nên chia nhỏ tệp Playbook thành nhiều tệp task con bằng `include_tasks`?

---


### [Chuyên Đề 18] So Sánh Thực Chiến Include vs Import: Dynamic Runtime Evaluation vs Static Pre-Processing Của Tasks/Roles

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Phân biệt sự khác nhau cốt lõi về thời điểm thi hành giữa <code>ansible.builtin.import_tasks</code> (Static Import) và <code>ansible.builtin.include_tasks</code> (Dynamic Include)? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>import_tasks</code> (Static Import): Nạp tĩnh tại thời điểm <b style="color: var(--accent-primary);">Parse-time</b> (trước khi Playbook chạy). Toàn bộ nội dung tệp task con được hòa trộn phẳng vào cây Playbook chính ngay ở bước đọc file.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• <code>include_tasks</code> (Dynamic Include): Nạp động tại thời điểm <b style="color: var(--accent-primary);">Runtime</b> (khi tiến trình chạy tới đúng Task đó). Tệp task con chỉ được đọc và phân tích khi execution engine chạy tới task include.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không phân biệt được Static vs Dynamic.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết <code>import</code> là tĩnh <code>include</code> là động nhưng không giải thích được khái niệm Parse-time vs Runtime.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác bản chất Parse-time hòa trộn phẳng vs Runtime nạp tại thời điểm chạy.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ sử dụng thực tế của 2 module trong Playbook.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Module nào chạy nhanh hơn về mặt hiệu năng thi hành? *(<code>import_tasks</code> chạy nhanh hơn vì không mất overhead phân tích file ở runtime.)*
</div>
</details>

---

### Câu 2 — Sử dụng `include_tasks` với Vòng lặp `loop:` 🔥
**Hỏi:** Tại sao ta có thể dùng `include_tasks` với từ khóa `loop:` để lặp danh sách task con nhưng KHÔNG THỂ dùng `import_tasks` với `loop:`? *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
Vì `import_tasks` được hòa trộn phẳng ở bước Parse-time trước khi chạy. Tại thời điểm Parse-time, Ansible Parser chưa thể tính toán được số lượng phần tử của mảng `loop:` ở Runtime, nên việc kết hợp `import_tasks` với `loop:` là bất khả thi về mặt kiến trúc (văng lỗi syntax).
Ngược lại, `include_tasks` được đánh giá ở Runtime nên có thể nạp tệp task con lặp đi lặp lại linh hoạt ứng với từng phần tử của mảng `loop:`.
**Tiêu chí chấm:**
- 0: Không giải thích được lý do kỹ thuật.
- 1: Biết `import_tasks` không chạy được với `loop:` nhưng lầm tưởng là do lỗi bug phần mềm.
- 2: Phân tích chính xác nguyên lý Parse-time không thể tính toán số phần tử mảng của `import_tasks`.
- 3: Nêu đúng + viết ví dụ YAML chuẩn nạp `include_tasks` với `loop:` và `loop_control`.
**Câu hỏi đào sâu:** Cần làm gì nếu muốn đổi tên biến mặc định `item` khi dùng `include_tasks` trong vòng lặp? *(Sử dụng `loop_control: loop_var: custom_var_name`.)*

---

### Câu 3 — Gom Nhóm Playbook bằng `import_playbook` 🔥
**Hỏi:** Module `ansible.builtin.import_playbook` dùng để làm gì? Vị trí khai báo của nó trong file YAML tổng khác gì so với `import_tasks`? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Tác dụng: Dùng để gom nhóm và thi hành tuần tự nhiều tệp Playbook hoàn chỉnh độc lập (chứa từ khóa `hosts:`) trong một kịch bản tổng thể (như `site-all.yml`).
- Vị trí khai báo: `import_playbook` là directive ở **cấp root Playbook** (cùng cấp với `hosts:`), tuyệt đối **KHÔNG nằm trong khối `tasks:`**. Ngược lại, `import_tasks` là module nằm bên trong khối `tasks:`.
**Tiêu chí chấm:**
- 0: Nhầm lẫn giữa `import_playbook` và `import_tasks`.
- 1: Biết `import_playbook` để nạp file playbook nhưng đặt sai vị trí bên trong khối `tasks:`.
- 2: Phân tích chính xác vai trò gom nhóm Playbook và vị trí khai báo cấp root.
- 3: Nêu đúng + viết ví dụ file `site-all.yml` gọi 2 Playbook con qua `import_playbook`.
**Câu hỏi đào sâu:** Chuyện gì xảy ra nếu đặt `import_playbook` bên trong khối `tasks:`? *(Ansible Engine báo lỗi `The task 'import_playbook' was not found in a play`.)*

---

### Câu 4 — Thừa hưởng Thẻ Tags và Handlers qua `import_tasks` 🔥
**Hỏi:** Tại sao các Task con nạp qua `import_tasks` lại tự động thừa hưởng thẻ `tags` và có thể thông báo `notify:` tới Handler nằm ở Playbook chính một cách trực tiếp? *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
Vì `import_tasks` thực hiện hòa trộn phẳng (Flattening) toàn bộ danh sách task con vào cây Playbook chính ở thời điểm parse-time. Do đó, về mặt bản chất mã nguồn, các task con trở thành các task trực tiếp của Playbook chính, nên tự động nhận thẻ `tags` gán ở task import và nhìn thấy tất cả các Handler khai báo ở `handlers/main.yml`.
**Tiêu chí chấm:**
- 0: Không hiểu cơ chế thừa hưởng tags và handlers.
- 1: Biết nhận được tags nhưng không giải thích được bản chất hòa trộn phẳng ở parse-time.
- 2: Phân tích chính xác cơ chế hòa trộn phẳng cây Playbook (Playbook Tree Flattening).
- 3: Nêu đúng + minh họa ví dụ gán `tags:` ở `import_tasks` lan xuống task con.
**Câu hỏi đào sâu:** Nếu gán `tags: [web]` ở dòng `import_tasks`, khi chạy `ansible-playbook --tags web` thì các task con trong tệp import có chạy không? *(Có, 100% task con đều chạy vì đã thừa hưởng tag `web`.)*

---

### Câu 5 — Thuộc tính `apply:` trong `include_tasks` 🔥
**Hỏi:** Tại sao khi gán `tags: [web]` cho `include_tasks`, các task con bên trong tệp nạp động lại KHÔNG tự động nhận tag? Giải thích vai trò của thuộc tính `apply:`. *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
Vì `include_tasks` nạp động ở runtime, thẻ `tags:` gán trực tiếp ở dòng `include_tasks` chỉ có hiệu lực áp dụng cho bản thân task include đó (để quyết định có include tệp hay không), mà **không lan xuống các task con bên trong**.
Vai trò của `apply:`: Khối `apply:` cho phép chỉ định ép buộc truyền các thuộc tính task (như `tags:`, `become:`, `environment:`) xuống từng task con bên trong tệp được include động.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `apply:`.
- 1: Biết `apply:` dùng cho `include_tasks` nhưng không giải thích được lý do thẻ tag không tự lan xuống task con.
- 2: Phân tích chính xác cơ chế nạp động runtime và vai trò của khối `apply:`.
- 3: Nêu đúng + viết đoạn YAML chuẩn dùng `apply: tags:` trong `include_tasks`.
**Câu hỏi đào sâu:** Viết cú pháp `apply:` gán cả `tags: [deploy]` và `become: true` cho `include_tasks`. *(Viết `apply: tags: [deploy] become: true`.)*

---

### Câu 6 — Bẫy Tham chiếu Biến Runtime trong `import_tasks`
**Hỏi:** Tại sao tuyệt đối không được tham chiếu các biến sinh ra ở thời điểm Runtime (như biến `register:`) vào cờ điều kiện `when:` của `import_tasks`? *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
Vì `import_tasks` được Ansible Engine phân tích và đánh giá cờ `when:` ngay ở bước Parse-time trước khi Playbook bắt đầu chạy. Tại thời điểm Parse-time, các biến sinh ra từ `register:` ở các task trước chưa hề tồn tại trên bộ nhớ. Việc tham chiếu này sẽ làm cờ `when:` bị đánh giá sai hoặc văng lỗi `undefined variable`.
Giải pháp: Chuyển sang dùng `include_tasks` (Dynamic) để đánh giá cờ `when:` theo biến runtime.
**Tiêu chí chấm:**
- 0: Không thấy được rủi ro khi dùng biến `register` với `import_tasks`.
- 1: Biết bị lỗi nhưng không nêu được bản chất đánh giá cờ `when:` ở parse-time vs runtime.
- 2: Phân tích chính xác xung đột thời điểm giữa parse-time evaluation và runtime variable registration.
- 3: Nêu đúng + minh họa ví dụ sửa lỗi từ `import_tasks` sang `include_tasks`.
**Câu hỏi đào sâu:** Cờ `when:` gán cho `import_tasks` sẽ áp dụng lên task include hay áp dụng lên từng task con? *(Áp dụng lên TỪNG task con sau khi hòa trộn phẳng.)*

---

### Câu 7 — Nạp Tệp Task Theo Môi trường và Hệ điều hành
**Hỏi:** Trình bày kỹ thuật sử dụng `include_tasks` kết hợp với biến facts hệ điều hành để nạp linh hoạt các tệp task cấu hình theo từng OS (CentOS vs Ubuntu). *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
Sử dụng biến facts `ansible_facts.os_family` để truyền động vào tên tệp trong `include_tasks`:
```yaml
- name: Include OS-specific setup tasks dynamically
  ansible.builtin.include_tasks: "tasks/{{ ansible_facts.os_family | lower }}_tasks.yml"
```
Khi chạy trên RedHat, nó nạp `tasks/redhat_tasks.yml`; khi chạy trên Debian, nó nạp `tasks/debian_tasks.yml`.
**Tiêu chí chấm:**
- 0: Không biết kỹ thuật nạp tệp theo biến hệ điều hành.
- 1: Biết dùng `when:` cho từng task nhưng không biết nạp động cả tệp task bằng biến.
- 2: Phân tích chính xác cơ chế nội suy chuỗi tên tệp trong `include_tasks`.
- 3: Nêu đúng + viết đoạn YAML chuẩn nạp tệp task theo hệ điều hành.
**Câu hỏi đào sâu:** Kỹ thuật này có áp dụng được với `import_tasks` không? *(Không áp dụng được an toàn với `import_tasks` nếu biến facts chưa được thu thập ở parse-time.)*

---

### Câu 8 — Cấu trúc Thư mục Dự án Mô-đun hóa `tasks/`
**Hỏi:** Trình bày cấu trúc thư mục tiêu chuẩn của một dự án Ansible Playbook mô-đun hóa được chia nhỏ thành nhiều tệp task con. *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
Cấu trúc tiêu chuẩn:
```bash
project/
├── ansible.cfg
├── inventory.ini
├── site-all.yml               (Playbook chính gọi import_playbook)
├── playbooks/
│   ├── webservers.yml
│   └── dbservers.yml
└── tasks/
    ├── common_tasks.yml       (Tasks dùng chung nạp qua import_tasks)
    ├── web_tasks.yml          (Tasks ứng dụng nạp qua include_tasks)
    └── db_tasks.yml
```
**Tiêu chí chấm:**
- 0: Đặt tất cả file nằm lộn xộn trong thư mục gốc.
- 1: Biết chia thư mục nhưng không phân định được vai trò thư mục `tasks/` và `playbooks/`.
- 2: Phân tích chính xác cấu trúc thư mục mô-đun hóa chuẩn mực.
- 3: Nêu đúng + vẽ sơ đồ cây thư mục và giải thích luồng nạp tệp của `site-all.yml`.
**Câu hỏi đào sâu:** Thư mục `tasks/` có thể chứa các thư mục con nữa không? *(Có thể, ví dụ `tasks/web/nginx.yml`.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Chia nhỏ Playbook 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook chia nhỏ bằng `include_tasks` / `import_tasks` để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective RHCE EX294 #13).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-include-import.yml`: Các tệp task con nạp qua `import_tasks` và `include_tasks` thực thi và chép file báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-include-import.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task trong các tệp con đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/include-import-app.conf` kiểm tra file cấu hình thực sự tồn tại đúng dữ liệu từ tệp task con.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file render.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE EX294 #13 (`☑`).
**Câu hỏi đào sâu:** Việc chia nhỏ Playbook thành 5 tệp task con có làm thay đổi cơ chế tính toán checksum của module `ansible.builtin.copy` bên trong tệp con không? *(Hoàn toàn không, checksum vẫn được so sánh chuẩn xác.)*

---

### Câu 10 — Phạm vi Biến (Variable Scope) trong `include_tasks` ★★★
**Hỏi:** Khi truyền biến qua thuộc tính `vars:` trong `include_tasks`, phạm vi tồn tại của biến đó ảnh hưởng tới các Task phía sau như thế nào?
**Đáp án chuẩn:**
Mặc định trong Ansible, biến được truyền vào `include_tasks` qua thuộc tính `vars:` sẽ tồn tại trong phạm vi của tệp task được include và **lan ra cả các Task tiếp theo nằm sau task include đó trong cùng một Play**.
Để phong tỏa phạm vi biến chỉ nằm trong tệp task include mà không bị rò rỉ ra ngoài, quản trị viên nên sử dụng cấu trúc Role với `public: false` hoặc đặt tên biến có tiền tố chuyên biệt.
**Tiêu chí chấm:**
- 0: Không biết phạm vi tồn tại của biến truyền trong `include_tasks`.
- 1: Lầm tưởng biến truyền vào `include_tasks` tự động biến mất khi chạy xong tệp task con.
- 2: Phân tích chính xác cơ chế rò rỉ biến out-of-scope trong cùng một Play.
- 3: Nêu đúng + giải pháp đặt tiền tố biến hoặc dùng Role cô lập biến.
**Câu hỏi đào sâu:** Làm sao để ngăn 2 tệp task con nạp qua `include_tasks` ghi đè biến của nhau? *(Đặt tên biến có tiền tố riêng biệt cho từng tệp task con.)*

---

### Câu 11 — Lồng `include_tasks` (Nested Includes) và Giới hạn Độ sâu ★★★
**Hỏi:** Ansible có cho phép lồng `include_tasks` bên trong một tệp task con đã được `include_tasks` trước đó không? Giới hạn độ sâu khuyến nghị là bao nhiêu?
**Đáp án chuẩn:**
- Ansible hoàn toàn cho phép lồng `include_tasks` nhiều cấp (Nested Includes).
- Giới hạn độ sâu khuyến nghị: **Tối đa 2 đến 3 cấp**.
- Lý do giới hạn: Lồng quá nhiều cấp include sẽ khiến tiến trình thi hành bị rối luồng, rất khó theo dõi vết lỗi khi gặp exception, và làm giảm hiệu năng phân tích runtime của Ansible Engine.
**Tiêu chí chấm:**
- 0: Lầm tưởng Ansible cấm lồng `include_tasks`.
- 1: Biết cho phép lồng nhưng không đưa ra được giới hạn độ sâu khuyến nghị và lý do kỹ thuật.
- 2: Phân tích chính xác cơ chế Nested Includes và giới hạn độ sâu 2-3 cấp.
- 3: Nêu đúng + đưa ra lời khuyên refactor sang cấu trúc Role khi kịch bản quá phức tạp.
**Câu hỏi đào sâu:** Nếu nạp lặp đệ quy `include_tasks` chính tệp đó thì chuyện gì xảy ra? *(Dẫn đến vòng lặp vô tận văng lỗi `Maximum recursion depth exceeded`.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về `include` vs `import` ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên lựa chọn chính xác giữa `include` và `import`, chia nhỏ Playbook chuyên nghiệp và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Dùng `import_tasks` cho các task tĩnh nền tảng để thừa hưởng Tags & Handlers hòa trộn ở Parse-time.
2. **Quy tắc 2:** Dùng `include_tasks` khi cần lặp mảng danh sách `loop:` hoặc nạp động theo cờ `when:` biến Runtime.
3. **Quy tắc 3:** Sử dụng `import_playbook` ở cấp root để gom nhóm các tệp Playbook độc lập.
4. **Quy tắc 4:** Sử dụng thuộc tính `apply: tags:` khi gán thẻ tag cho `include_tasks`.
5. **Quy tắc 5:** Giữ cấu trúc chia nhỏ phẳng gọn và đảm bảo ở lượt chạy Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy thiết kế mã nguồn IaC chuyên nghiệp Doanh nghiệp.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp triệt tiêu lỗi syntax khi kết hợp với vòng lặp `loop:`? *(Quy tắc 2: Dùng `include_tasks` với `loop:`.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm tổ chức mã nguồn Playbook lớn và phân biệt `include` vs `import`, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi thiết kế kiến trúc mã nguồn Ansible mô-đun hóa chuyên nghiệp bằng cách phân định chính xác giữa nạp tĩnh (Static Re-use) và nạp động (Dynamic Re-use): tôi sử dụng `import_tasks` cho các nhiệm vụ cố định ở thời điểm Parse-time để tận dụng khả năng hòa trộn phẳng kế thừa Tags và Handlers toàn cục; sử dụng `include_tasks` kết hợp khối `apply:` cho các nhiệm vụ nạp động ở Runtime theo vòng lặp `loop:` và điều kiện `when:` phức tạp. Tôi gom nhóm hệ thống Playbook cấp Doanh nghiệp bằng `import_playbook`, giữ độ sâu nạp tệp không quá 2 cấp, đảm bảo mọi kịch bản mô-đun hóa đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Ngô Văn M | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Bùi Thị N | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 19

Để chuẩn bị tốt nhất cho **Buổi 19: da-moi-truong-inventory — Đa môi trường, inventory và group_vars layering**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Cấu trúc tổ chức hai thư mục inventory riêng biệt `inventory/staging/` và `inventory/production/` khác gì so với dùng 1 file inventory duy nhất?
2. **Nghiên cứu trước 2:** Thứ tự ghi đè biến (Precedence) giữa `group_vars/all.yml`, `group_vars/web.yml`, và `host_vars/target1.yml` diễn ra như thế nào?
3. **Nghiên cứu trước 3:** Làm thế nào để chỉ định tệp inventory khi chạy lệnh `ansible-playbook` cho môi trường Staging vs Production bằng cờ `-i`?

---


### [Chuyên Đề 19] Quản Trị Đa Môi Trường (Multi-Environment): Tổ Chức Directory Layout Cho Dev, Staging, UAT & Production Không Lặp Code

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Tại sao Red Hat khuyến nghị tổ chức đa môi trường qua cấu trúc thư mục <code>inventory/staging/</code> và <code>inventory/production/</code> riêng biệt thay vì gom chung vào 1 file inventory? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
Lý do cô lập:
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <b style="color: var(--accent-primary);">Cô lập 100% dữ liệu:</b> Tách biệt hoàn toàn danh sách IP máy chủ và các biến cấu hình giữa Staging và Production, triệt tiêu nguy cơ biến Staging bị rò rỉ đè hỏng cấu hình Production.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <b style="color: var(--accent-primary);">Quản lý biến tự động:</b> Khi thi hành với cờ <code>-i inventory/staging</code>, Ansible Engine chỉ tự động nạp các biến trong <code>inventory/staging/group_vars/</code>, ngăn ngừa đọc nhầm biến của Production.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết cấu trúc thư mục inventory đa môi trường.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết tách thư mục nhưng không giải thích được cơ chế tự động nạp biến theo cờ <code>-i</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò cô lập biến và triệt tiêu nguy cơ rò rỉ cấu hình Production.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + vẽ sơ đồ cây thư mục chuẩn <code>inventory/staging/</code> và <code>inventory/production/</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu dự án có thêm môi trường UAT, ta tạo thư mục nào? *(Tạo thư mục <code>inventory/uat/</code> chứa <code>hosts.ini</code> và <code>group_vars/</code> tương tự.)*
</div>
</details>

---

### Câu 2 — Vị trí Đặt Thư mục `group_vars/` 🔥
**Hỏi:** Thư mục `group_vars/` bắt buộc phải nằm ở vị trí nào trong cấu trúc dự án đa môi trường? Chuyện gì xảy ra nếu để `group_vars/` ở root dự án? *(Liên quan QT 4.2, QT 6.1)*
**Đáp án chuẩn:**
- Vị trí bắt buộc: Đặt trực tiếp bên trong từng thư mục môi trường tương ứng (ví dụ `inventory/staging/group_vars/` và `inventory/production/group_vars/`).
- Nguy cơ nếu để ở root: Nếu để `group_vars/` ở root dự án, Ansible Engine sẽ nạp hòa trộn biến ở root với biến môi trường, dẫn đến các biến ở root ghi đè hoặc xung đột với biến của môi trường cụ thể, gây rủi ro ghi đè nhầm cấu hình Production.
**Tiêu chí chấm:**
- 0: Không biết vị trí đặt `group_vars/` trong dự án đa môi trường.
- 1: Biết đặt trong thư mục môi trường nhưng không giải thích được nguy cơ hòa trộn biến khi để ở root.
- 2: Phân tích chính xác cơ chế nạp biến theo vị trí thư mục và nguy cơ ghi đè nhầm lẫn.
- 3: Nêu đúng + minh họa ví dụ cấu trúc thư mục ĐÚNG vs SAI trên terminal.
**Câu hỏi đào sâu:** Ansible Engine ưu tiên nạp biến trong `inventory/staging/group_vars/all.yml` hay `group_vars/all.yml` ở root? *(Biến trong `inventory/staging/group_vars/all.yml` có độ ưu tiên cao hơn.)*

---

### Câu 3 — Sử dụng Cờ Tham số `-i` (`--inventory`) 🔥
**Hỏi:** Trình bày tác dụng của cờ tham số `-i` trong lệnh `ansible-playbook`. Tại sao khi truyền cờ `-i`, ta nên truyền đường dẫn thư mục `inventory/staging` thay vì chỉ truyền file `hosts.ini`? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Tác dụng cờ `-i`: Chỉ định tường minh đường dẫn danh mục máy chủ và cấu hình môi trường mục tiêu cho Playbook.
- Lý do truyền đường dẫn thư mục: Nếu chỉ truyền file `inventory/staging/hosts.ini`, Ansible chỉ nạp file `hosts.ini` mà bỏ qua không tự động nạp thư mục `group_vars/` bên cạnh. Khi truyền đường dẫn thư mục `inventory/staging`, Ansible sẽ nạp đồng thời file host và **toàn bộ thư mục `group_vars/` bên trong**.
**Tiêu chí chấm:**
- 0: Không biết cờ `-i`.
- 1: Biết cờ `-i` dùng trỏ inventory nhưng không phân biệt được truyền file vs truyền thư mục.
- 2: Phân tích chính xác sự khác nhau giữa truyền file `.ini` và truyền đường dẫn thư mục chứa `group_vars/`.
- 3: Nêu đúng + minh họa câu lệnh CLI `ansible-playbook -i inventory/staging site-env.yml`.
**Câu hỏi đào sâu:** Có thể truyền nhiều cờ `-i` trong 1 câu lệnh `ansible-playbook` không? *(Có thể, ví dụ `-i inventory/staging -i inventory/common`.)*

---

### Câu 4 — Nguyên lý Phân tầng Biến Group Variables Layering 🔥
**Hỏi:** Trình bày thứ tự độ ưu tiên nạp biến (Variable Precedence) từ rộng đến hẹp giữa các tệp biến: `group_vars/all.yml`, `group_vars/web.yml`, và `host_vars/target1.yml`. *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
Thứ tự ưu tiên từ thấp đến cao (biến ở tầng hẹp hơn sẽ đè giá trị biến ở tầng rộng hơn):
1. **`group_vars/all.yml` (Ưu tiên thấp nhất trong nhóm):** Khai báo các biến dùng chung cho mọi máy chủ (như `env_name`, `dns_server`).
2. **`group_vars/web.yml` (Ưu tiên trung bình):** Ghi đè các biến dành riêng cho nhóm máy chủ web (như `app_port: 8080`).
3. **`host_vars/target1.yml` (Ưu tiên cao nhất trong kiểm kê):** Ghi đè các biến đặc thù dành riêng cho duy nhất máy chủ `target1` (như `max_clients: 99`).
**Tiêu chí chấm:**
- 0: Không biết thứ tự ưu tiên phân tầng biến.
- 1: Nêu được 3 tầng file nhưng xếp sai thứ tự ưu tiên đè biến.
- 2: Phân tích chính xác nguyên lý phân tầng từ rộng đến hẹp `all` -> `group` -> `host`.
- 3: Nêu đúng + cho ví dụ minh họa 1 biến `app_port` bị ghi đè qua 3 tầng.
**Câu hỏi đào sâu:** Nếu trong `group_vars/all.yml` ghi `app_port: 80` và `group_vars/web.yml` ghi `app_port: 8080`, thì máy trong nhóm `web` nhận giá trị nào? *(Nhận giá trị `8080` từ `group_vars/web.yml`.)*

---

### Câu 5 — Tra cứu Ma trận Biến với `ansible-inventory` CLI 🔥
**Hỏi:** Nêu các câu lệnh CLI `ansible-inventory` dùng để xem đồ thị phân nhóm máy chủ và tra cứu ma trận biến đã giải mã của môi trường Staging. *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Xem đồ thị phân nhóm host:
  `ansible-inventory -i inventory/staging --graph`
- Xem ma trận biến giải mã của toàn bộ inventory:
  `ansible-inventory -i inventory/staging --vars --list`
- Tra cứu ma trận biến của 1 host cụ thể (`target1`):
  `ansible-inventory -i inventory/staging --host target1`
**Tiêu chí chấm:**
- 0: Không biết công cụ `ansible-inventory`.
- 1: Biết công cụ nhưng không nhớ cờ `--graph` và `--vars`.
- 2: Phân tích chính xác vai trò tra cứu ma trận biến và đồ thị phân nhóm host của CLI.
- 3: Nêu đúng + thực thi câu lệnh CLI minh họa tra cứu trên terminal.
**Câu hỏi đào sâu:** Công cụ `ansible-inventory` có tác động làm thay đổi cấu hình trên máy đích không? *(Không, nó chỉ là công cụ read-only tra cứu thông tin trên Control Node.)*

---

### Câu 6 — Thiết lập Lá chắn Mặc định An toàn trong `ansible.cfg`
**Hỏi:** Tại sao trong tệp `ansible.cfg` ta lại bắt buộc phải khai báo `inventory = ./inventory/staging` làm cấu hình mặc định? *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
Đây là lá chắn an toàn tối quan trọng (Fail-safe Default):
Nếu người dùng đứng ở terminal gõ lệnh `ansible-playbook site.yml` mà lỡ **quên không truyền cờ `-i`**, Ansible Engine sẽ tự động lấy cấu hình mặc định trỏ vào môi trường thử nghiệm **Staging**, giúp bảo vệ môi trường Production không bao giờ bị tác động nhầm bất ngờ.
**Tiêu chí chấm:**
- 0: Không hiểu ý nghĩa thiết lập safe default trong `ansible.cfg`.
- 1: Biết dòng cấu hình nhưng không giải thích được vai trò lá chắn bảo vệ Production.
- 2: Phân tích chính xác cơ chế phòng thủ tác động nhầm Production khi thiếu cờ `-i`.
- 3: Nêu đúng + viết đoạn mã cấu hình `ansible.cfg` chuẩn mực Doanh nghiệp.
**Câu hỏi đào sâu:** Chuyện gì xảy ra nếu ai đó đặt `inventory = ./inventory/production` làm mặc định trong `ansible.cfg`? *(Cực kỳ nguy hiểm, mọi lệnh gõ thiếu cờ `-i` sẽ tự động giội thẳng vào Production.)*

---

### Câu 7 — Định nghĩa Biến Nhận dạng Môi trường `env_name`
**Hỏi:** Tại sao ta nên định nghĩa bộ biến nhận dạng môi trường (`env_name`, `domain_suffix`) trong từng tệp `group_vars/all.yml` của mỗi môi trường? *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
Giúp Playbook và các tệp Template Jinja2 giữ nguyên tính tổng quát:
Thay vì phải cứng hóa chuỗi URL hay cấu hình riêng cho từng môi trường, Template chỉ cần tham chiếu biến `{{ env_name }}` và `{{ domain_suffix }}`. Khi chạy với `-i inventory/staging`, nó tự render thành `staging.internal`; khi chạy với `-i inventory/production`, nó tự render thành `company.com`.
**Tiêu chí chấm:**
- 0: Cứng hóa URL và thông số môi trường trực tiếp trong Playbook/Template.
- 1: Biết dùng biến nhưng không đưa biến lên `group_vars/all.yml`.
- 2: Phân tích chính xác vai trò giúp Playbook duy trì tính tổng quát và dễ tái sử dụng.
- 3: Nêu đúng + minh họa đoạn file Template Jinja2 sử dụng biến `env_name`.
**Câu hỏi đào sâu:** Làm thế nào để bật cờ `log_level: debug` ở Staging nhưng `log_level: warn` ở Production? *(Khai báo `log_level: debug` trong `inventory/staging/group_vars/all.yml` và `log_level: warn` trong `inventory/production/group_vars/all.yml`.)*

---

### Câu 8 — Duy trì 1 Playbook Duy nhất cho Đa Môi trường
**Hỏi:** Tại sao trong tư duy IaC hiện đại, quản trị viên chỉ nên duy trì **ĐÚNG 1 FILE PLAYBOOK DUY NHẤT** (`site-env.yml`) để triển khai cho tất cả các môi trường Staging, UAT, và Production? *(Liên quan QT 4.1, QT 4.3)*
**Đáp án chuẩn:**
- Triệt tiêu rủi ro Lệch Mã nguồn (Code Drift): Nếu tạo 2 file Playbook `site-staging.yml` và `site-prod.yml`, khi sửa lỗi ở file này rất dễ quên sửa ở file kia.
- Đảm bảo tính nhất quán 100%: Code triển khai trên Staging được kiểm thử ra sao thì khi đưa lên Production sẽ thi hành chính xác 100% như vậy, sự khác biệt duy nhất chỉ là dữ liệu biến nạp từ `inventory/`.
**Tiêu chí chấm:**
- 0: Cho rằng nên tạo 2 file Playbook riêng cho Staging và Production.
- 1: Biết dùng 1 Playbook nhưng không giải thích được khái niệm Code Drift.
- 2: Phân tích chính xác rủi ro Code Drift và nguyên lý tách biệt logic thi hành vs dữ liệu biến.
- 3: Nêu đúng + minh họa tư duy triển khai Playbook qua các stage của pipeline CI/CD.
**Câu hỏi đào sâu:** Khái niệm "Infrastructure as Code - Separation of Code and Data" nghĩa là gì? *(Nghĩa là mã nguồn Playbook chỉ chứa logic thi hành, toàn bộ dữ liệu cấu hình được đẩy hết ra tệp biến inventory.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Đa Môi trường 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook thi hành trên môi trường Staging qua cờ `-i inventory/staging` để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective RHCE EX294 #4).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook -i inventory/staging site-env.yml`: Task chép file cấu hình nạp biến Staging thực thi báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook -i inventory/staging site-env.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/environment-app.conf` kiểm tra file cấu hình thực sự tồn tại đúng dữ liệu `ENVIRONMENT=staging` và `APP_PORT=8080`.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file render.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE EX294 #4 (`☑`).
**Câu hỏi đào sâu:** Nếu chạy lại Lần 2 mà terminal báo `changed=1`, nguyên nhân có thể do đâu? *(Do task trong Playbook bị lặp changed mạo danh hoặc do file template bị thay đổi timestamp/checksum liên tục.)*

---

### Câu 10 — Sử dụng `host_vars/` Nạp đè Biến Cá biệt ★★★
**Hỏi:** Thư mục `host_vars/` dùng để làm gì trong cấu trúc inventory đa môi trường? Cho ví dụ trường hợp phải dùng `host_vars/`.
**Đáp án chuẩn:**
- Tác dụng: `host_vars/` chứa các tệp biến dành riêng cho từng máy chủ cá biệt (tên tệp trùng với tên hostname trong `hosts.ini`, ví dụ `host_vars/target1.yml`). Biến trong `host_vars/` có độ ưu tiên cao nhất trong inventory, nạp đè lên biến của `group_vars/`.
- Ví dụ trường hợp dùng: Máy chủ `target1` trong nhóm Web là máy Master đảm nhận vai trò Primary Node, cần cấu hình `is_primary: true` hoặc số lượng kết nối `max_clients: 99` khác với các máy Worker trong cùng nhóm.
**Tiêu chí chấm:**
- 0: Không biết khái niệm `host_vars/`.
- 1: Biết `host_vars/` nhưng không giải thích được độ ưu tiên nạp đè lên `group_vars/`.
- 2: Phân tích chính xác vai trò nạp đè biến cá biệt cho từng node.
- 3: Nêu đúng + minh họa ví dụ tệp `inventory/staging/host_vars/target1.yml`.
**Câu hỏi đào sâu:** Thư mục `host_vars/` nên đặt ở đâu trong dự án đa môi trường? *(Được đặt bên trong thư mục môi trường tương ứng, ví dụ `inventory/staging/host_vars/`.)*

---

### Câu 11 — Guard Task Bảo vệ Môi trường Production ★★★
**Hỏi:** Làm thế nào để viết một Guard Task (Task bảo vệ) trong Playbook giúp ngăn chặn tuyệt đối việc người dùng gõ nhầm lệnh làm tác động sai môi trường Production?
**Đáp án chuẩn:**
Thêm một Task kiểm tra điều kiện an toàn ngay ở đầu Playbook, dùng module `ansible.builtin.assert` hoặc `fail`:
```yaml
- name: Guard Task - Prevent accidental execution on Production
  ansible.builtin.assert:
    that:
      - not (env_name == 'production' and ansible_host == '127.0.0.1')
    fail_msg: "ERROR: Accidental execution detected! Production env cannot use localhost IP!"
```
Nếu phát hiện biến `env_name == 'production'` nhưng IP lại trỏ vào máy local Staging, Playbook lập tức dừng ngắt an toàn.
**Tiêu chí chấm:**
- 0: Không biết khái niệm Guard Task bảo vệ môi trường.
- 1: Biết kiểm tra điều kiện nhưng không viết được module `assert` hay `fail`.
- 2: Phân tích chính xác cơ chế gác cổng an toàn ngay ở đầu Playbook.
- 3: Nêu đúng + viết đoạn mã Guard Task chuẩn bằng `ansible.builtin.assert`.
**Câu hỏi đào sâu:** Module `ansible.builtin.assert` khác gì so với module `ansible.builtin.fail`? *(`assert` kiểm tra biểu thức logic `that:`, nếu sai mới trigger fail; còn `fail` luôn luôn ngắt execution.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Tổ chức Đa Môi trường ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên tổ chức đa môi trường chuyên nghiệp, an toàn bảo mật và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Tách biệt 100% thư mục môi trường `inventory/staging/` và `inventory/production/`.
2. **Quy tắc 2:** Đặt `group_vars/` bên trong từng thư mục môi trường tương ứng để nạp đè tự động theo cờ `-i`.
3. **Quy tắc 3:** Luôn chỉ định cờ `-i` khi thi hành và khai báo `inventory = ./inventory/staging` mặc định trong `ansible.cfg`.
4. **Quy tắc 4:** Duy trì 1 Playbook logic duy nhất (`site-env.yml`) cho tất cả các môi trường.
5. **Quy tắc 5:** Tra cứu ma trận biến với `ansible-inventory` và đảm bảo Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy thiết kế hệ thống IaC an toàn cấp Enterprise.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp triệt tiêu nguy cơ Code Drift? *(Quy tắc 4: Duy trì 1 Playbook logic duy nhất cho tất cả các môi trường.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm quản lý đa môi trường và phân tầng biến trong Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi làm chủ phương pháp tổ chức hạ tầng đa môi trường chuẩn Red Hat Enterprise IaC: cô lập 100% dữ liệu danh mục máy chủ và cấu hình bằng cấu trúc thư mục `inventory/staging/` và `inventory/production/` riêng biệt, áp dụng kỹ thuật phân tầng biến Group Variables Layering tự động nạp đè theo độ ưu tiên từ `all.yml` đến `web.yml` và `host_vars/`. Tôi thiết lập lá chắn an toàn mặc định trong `ansible.cfg`, kiểm tra ma trận biến bằng công cụ CLI `ansible-inventory`, duy trì 1 bộ Playbook logic duy nhất để triệt tiêu hoàn toàn rủi ro Code Drift và ghi đè nhầm Production, đảm bảo mọi kịch bản đa môi trường đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Vũ Văn O | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Lý Thị P | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 20

Để chuẩn bị tốt nhất cho **Buổi 20: ansible-vault — Bảo vệ dữ liệu nhạy cảm**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Công cụ `ansible-vault` dùng để làm gì? Tại sao không bao giờ được lưu mật khẩu hoặc private key dạng plaintext trên Git repository?
2. **Nghiên cứu trước 2:** Lệnh CLI nào dùng để mã hóa một file biến (`vault.yml`) và lệnh nào dùng để xem nội dung file đã mã hóa?
3. **Nghiên cứu trước 3:** Làm thế nào để truyền mật khẩu giải mã Vault khi chạy `ansible-playbook` bằng cờ `--vault-id` hoặc `--ask-vault-pass`?

---


### [Chuyên Đề 20] Bảo Mật Dữ Liệu Nhạy Cảm Với Ansible Vault: Mã Hóa File/String, Vault Password Client, Multi-Vault IDs & CI/CD Vault

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Ansible Vault là gì? Tại sao việc sử dụng Ansible Vault lại là yêu cầu sinh tử khi quản lý mã nguồn tự động hóa trên Git repository? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Ansible Vault là tính năng bảo mật tích hợp sẵn trong Ansible Core, sử dụng thuật toán mã hóa đối xứng AES-256 để bảo vệ thông tin nhạy cảm.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Yêu cầu sinh tử: Trong dự án IaC, Playbook chứa rất nhiều thông tin bí mật (mật khẩu DB, SSH keys, API tokens). Nếu không dùng Vault mã hóa, lưu plaintext rồi push lên Git public sẽ dẫn tới nguy cơ lộ bí mật Doanh nghiệp, bị tin tặc tấn công chiếm đoạt hệ thống.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết Ansible Vault.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết Vault để giấu mật khẩu nhưng không nêu được thuật toán AES-256 và nguy cơ rò rỉ secret trên Git.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác cơ chế mã hóa AES-256 tích hợp giúp bảo vệ thông tin nhạy cảm trên Git repository.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa đoạn header mã hóa <code>$ANSIBLE_VAULT;1.1;AES256</code> trên terminal.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Thuật toán mã hóa đối xứng AES-256 sử dụng mấy khóa để mã hóa và giải mã? *(Sử dụng đúng 1 khóa bí mật chung - Secret Key / Passphrase.)*
</div>
</details>

---

### Câu 2 — Bộ Lệnh CLI Quản lý Vault 🔥
**Hỏi:** Nêu công dụng của các câu lệnh CLI Ansible Vault sau: `create`, `encrypt`, `decrypt`, `view`, `edit`, và `rekey`. *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- `ansible-vault create`: Tạo một tệp mới và mã hóa ngay lập tức.
- `ansible-vault encrypt`: Mã hóa một tệp văn bản plaintext sẵn có thành dạng ciphertext.
- `ansible-vault decrypt`: Giải mã vĩnh viễn tệp Vault trở lại dạng plaintext trên đĩa.
- `ansible-vault view`: Xem trực tiếp nội dung giải mã trên màn hình terminal mà KHÔNG giải mã file trên đĩa.
- `ansible-vault edit`: Mở tệp mã hóa ra chỉnh sửa (tự động giải mã tạm thời và tự động mã hóa lại khi lưu).
- `ansible-vault rekey`: Thay đổi mật khẩu giải mã Vault sang một mật khẩu mới.
**Tiêu chí chấm:**
- 0: Không biết các lệnh CLI của `ansible-vault`.
- 1: Biết 1-2 lệnh cơ bản nhưng nhầm lẫn giữa `view` và `decrypt`.
- 2: Phân tích chính xác công dụng của cả 6 câu lệnh CLI quản lý Vault.
- 3: Nêu đúng + minh họa câu lệnh thực thi `ansible-vault edit vars/vault.yml`.
**Câu hỏi đào sâu:** Tại sao khi cần sửa file mã hóa, ta nên dùng `ansible-vault edit` thay vì `ansible-vault decrypt` rồi gõ `vim`? *(Vì `edit` giúp chỉnh sửa và tự mã hóa lại ngay trong RAM, tránh rủi ro quên không mã hóa lại làm lộ file trần trên đĩa.)*

---

### Câu 3 — Mã hóa Chuỗi Biến Đơn lẻ `encrypt_string` 🔥
**Hỏi:** Trình bày tác dụng của lệnh `ansible-vault encrypt_string`. Khi nào nên dùng `encrypt_string` thay vì mã hóa toàn bộ tệp biến? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Tác dụng: Dùng để mã hóa một chuỗi biến đơn lẻ (Inline Secret) và in ra định dạng YAML bọc trong khối `!vault |` để dán trực tiếp vào file biến.
- Khi nên dùng: Khi tệp `group_vars/web.yml` chứa hàng chục biến cấu hình bình thường (như `port`, `domain`) và chỉ có riêng 1 biến mật khẩu `db_password` là nhạy cảm. Mã hóa chuỗi đơn lẻ giúp đồng đội vẫn đọc hiểu được toàn bộ file YAML mà chỉ có riêng chuỗi mật khẩu là bị ẩn.
**Tiêu chí chấm:**
- 0: Không biết lệnh `encrypt_string`.
- 1: Biết `encrypt_string` để mã hóa chuỗi nhưng không giải thích được ưu điểm giữ tính đọc hiểu cho file YAML.
- 2: Phân tích chính xác cơ chế Inline Vault Encryption và trường hợp áp dụng thực tế.
- 3: Nêu đúng + viết đoạn mã YAML minh họa chuỗi bọc trong từ khóa `!vault |`.
**Câu hỏi đào sâu:** Viết lệnh CLI mã hóa chuỗi `'MySecret123'` gán cho biến `db_pass`. *(Chạy `ansible-vault encrypt_string 'MySecret123' --name 'db_pass'`.)*

---

### Câu 4 — Tệp Mật khẩu `.vault_pass` và `ansible.cfg` 🔥
**Hỏi:** Nêu tác dụng của tệp mật khẩu local `.vault_pass` và thuộc tính `vault_password_file` trong `ansible.cfg`. Phân quyền Linux an toàn cho tệp `.vault_pass` phải là bao nhiêu? *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- Tác dụng: Giúp tự động hóa quá trình giải mã Vault khi thi hành Playbook, khiến người dùng hoặc hệ thống CI/CD không phải gõ mật khẩu từ bàn phím ở từng lần chạy lệnh `ansible-playbook`.
- Phân quyền Linux an toàn: Phải là **`chmod 0600`** (chỉ có duy nhất owner được đọc và ghi, ngắt toàn bộ quyền truy cập của Group và Others).
- Cấu hình `ansible.cfg`: `vault_password_file = ./.vault_pass` (trong mục `[defaults]`).
**Tiêu chí chấm:**
- 0: Không biết tệp `.vault_pass` và cấu hình `ansible.cfg`.
- 1: Biết file `.vault_pass` nhưng không nhớ phân quyền `0600` và cấu hình `ansible.cfg`.
- 2: Phân tích chính xác vai trò tự động hóa giải mã và tầm quan trọng của phân quyền `0600`.
- 3: Nêu đúng + dán đoạn cấu hình `ansible.cfg` chứa `vault_password_file = ./.vault_pass`.
**Câu hỏi đào sâu:** Chuyện gì xảy ra nếu để tệp `.vault_pass` ở quyền `0777` trên server dùng chung? *(Bất kỳ user nào trên server cũng đọc được tệp để giải mã toàn bộ thông tin nhạy cảm.)*

---

### Câu 5 — Quản lý Mật khẩu với Tệp `.gitignore` 🔥
**Hỏi:** Tại sao việc khai báo tệp `.vault_pass` vào tệp cấu hình `.gitignore` lại là quy tắc an toàn sinh tử? *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
Vì tệp `.vault_pass` chứa mật khẩu giải mã tĩnh của Ansible Vault. Nếu mã hóa file `vars/vault.yml` rất cẩn thận bằng AES-256 nhưng lại quên không cho `.vault_pass` vào `.gitignore` rồi push cả 2 file lên Git repository public, kẻ xấu chỉ cần tải file `.vault_pass` về là lập tức giải mã được toàn bộ bí mật của Doanh nghiệp.
**Tiêu chí chấm:**
- 0: Không biết mối liên hệ giữa `.vault_pass` và `.gitignore`.
- 1: Biết thêm vào `.gitignore` nhưng không giải thích được hậu quả triệt tiêu tính bảo mật của Vault.
- 2: Phân tích chính xác nguyên tắc an toàn sinh tử bảo vệ kho mã nguồn Git.
- 3: Nêu đúng + minh họa câu lệnh `echo ".vault_pass" >> .gitignore` và kiểm tra bằng `git status`.
**Câu hỏi đào sâu:** Làm thế nào để kiểm tra xem một file đã bị Git bỏ qua qua tệp `.gitignore` chưa? *(Chạy lệnh `git check-ignore -v .vault_pass`.)*

---

### Câu 6 — Quản lý Nhiều Mật khẩu Vault với `--vault-id`
**Hỏi:** Cờ tham số `--vault-id` dùng để làm gì? Trình bày kịch bản áp dụng `--vault-id` khi quản lý dữ liệu nhạy cảm cho 2 môi trường Dev và Prod. *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Tác dụng: Cho phép quản lý nhiều mật khẩu Vault khác nhau và gắn nhãn phân loại (Label Identity) cho từng môi trường hoặc từng phân quyền đội nhóm.
- Kịch bản áp dụng:
  + Môi trường Dev: Mã hóa với nhãn `dev@.vault_dev` (đội Dev nắm tệp `.vault_dev`).
  + Môi trường Prod: Mã hóa với nhãn `prod@.vault_prod` (chỉ đội SysAdmin nắm tệp `.vault_prod`).
  + Khi chạy Playbook Prod: `ansible-playbook --vault-id prod@.vault_prod site-vault.yml`.
**Tiêu chí chấm:**
- 0: Không biết cờ `--vault-id`.
- 1: Biết `--vault-id` nhưng không nêu được kịch bản phân quyền giữa Dev và SysAdmin/Prod.
- 2: Phân tích chính xác cơ chế gán nhãn Vault ID và kịch bản phân quyền đa môi trường.
- 3: Nêu đúng + viết câu lệnh CLI thực thi mã hóa và chạy Playbook với `--vault-id`.
**Câu hỏi đào sâu:** Có thể truyền nhiều cờ `--vault-id` trong 1 câu lệnh `ansible-playbook` không? *(Có thể, ví dụ `--vault-id dev@.vault_dev --vault-id prod@.vault_prod`.)*

---

### Câu 7 — Tự động hóa Giải mã Vault trong Pipeline CI/CD
**Hỏi:** Làm thế nào để tự động hóa quá trình giải mã Ansible Vault trong các pipeline CI/CD (như Gitlab CI, Github Actions) mà không cần gõ mật khẩu từ bàn phím và không lộ mật khẩu trên kho mã nguồn? *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
Quy trình 2 bước SecOps trong CI/CD:
1. **Lưu mật khẩu vào Secret Variable của CI/CD:** Đẩy mật khẩu Vault vào hệ thống quản lý Secret của CI/CD (ví dụ biến `$ANSIBLE_VAULT_PASSWORD` trong Gitlab CI / Secret trong Github Actions).
2. **Tạo tệp `.vault_pass` tạm thời trong runner execution:** Trước khi thi hành Playbook, runner chạy lệnh:
   `echo "$ANSIBLE_VAULT_PASSWORD" > .vault_pass && chmod 0600 .vault_pass`
   Sau khi thi hành xong, tệp tạm bị xóa tự động.
**Tiêu chí chấm:**
- 0: Không biết cách đưa Ansible Vault vào CI/CD pipeline.
- 1: Biết dùng biến môi trường nhưng không nêu được bước ghi ra file `.vault_pass` tạm và phân quyền 0600.
- 2: Phân tích chính xác quy trình SecOps tiêm Secret Variable trong runner execution.
- 3: Nêu đúng + viết đoạn mã YAML minh họa trong `before_script` của pipeline.
**Câu hỏi đào sâu:** Có thể truyền biến môi trường trực tiếp vào Ansible Vault không? *(Có thể dùng biến `ANSIBLE_VAULT_PASSWORD_FILE` trỏ tới script in mật khẩu.)*

---

### Câu 8 — Đổi Mật khẩu Vault với `ansible-vault rekey`
**Hỏi:** Trình bày nguyên lý và câu lệnh CLI đổi mật khẩu Vault (Rekeying). Tại sao việc định kỳ rekey mật khẩu Vault lại là yêu cầu bắt buộc trong chính sách an toàn thông tin? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- Lệnh đổi mật khẩu: `ansible-vault rekey vars/vault.yml`.
- Nguyên lý: Lệnh `rekey` sẽ giải mã dữ liệu AES-256 bằng mật khẩu cũ trong bộ nhớ RAM, sau đó lập tức mã hóa lại toàn bộ dữ liệu bằng mật khẩu mới và ghi đè tệp ciphertext.
- Lý do bắt buộc: Định kỳ đổi mật khẩu (như 6 tháng/lần) giúp tuân thủ chính sách an toàn thông tin Doanh nghiệp, triệt tiêu nguy cơ nếu mật khẩu cũ lỡ bị rò rỉ cho nhân sự đã nghỉ việc.
**Tiêu chí chấm:**
- 0: Không biết lệnh `ansible-vault rekey`.
- 1: Biết lệnh `rekey` nhưng lầm tưởng phải giải mã tay `decrypt` rồi `encrypt` lại.
- 2: Phân tích chính xác cơ chế giải mã trong RAM và mã hóa lại với mật khẩu mới của `rekey`.
- 3: Nêu đúng + minh họa lệnh `rekey` kết hợp cờ `--new-vault-password-file`.
**Câu hỏi đào sâu:** Lệnh `rekey` có làm thay đổi tên các biến bên trong tệp Vault không? *(Hoàn toàn không, giá trị biến giải mã giữ nguyên 100%, chỉ có khóa mã hóa AES-256 là thay đổi.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Vault 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook sử dụng biến mã hóa từ Ansible Vault để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective RHCE EX294 #14).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-vault.yml`: Biến được nạp và giải mã tạm trong RAM, Task chép file cấu hình bảo mật thực thi báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-vault.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/vault-app.conf` kiểm tra file cấu hình thực sự tồn tại đúng dữ liệu mật khẩu `DATABASE_PASSWORD=SuperSecretDBPassword2026`.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file render.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE EX294 #14 (`☑`).
**Câu hỏi đào sâu:** Dữ liệu giải mã từ Vault trên máy Control Node có bị lưu lại tệp log trên máy đích không? *(Tùy thuộc vào thuộc tính `no_log: true` của task để ẩn log sensitive data trên terminal.)*

---

### Câu 10 — Thuộc tính `no_log: true` Bảo vệ Log Terminal ★★★
**Hỏi:** Thuộc tính `no_log: true` trong Ansible Task có tác dụng gì? Tại sao nên kết hợp `no_log: true` với các Task xử lý biến mã hóa từ Vault?
**Đáp án chuẩn:**
- Tác dụng: Thuộc tính `no_log: true` chỉ đạo Ansible Engine ẩn toàn bộ thông tin tham số và giá trị biến của Task đó khỏi màn hình terminal và các tệp log xuất ra.
- Lý do kết hợp: Mặc dù biến trong tệp Vault đã được mã hóa AES-256 trên đĩa, nhưng khi Playbook chạy ở chế độ Verbose (`-v` hoặc `-vvv`), giá trị biến sau khi giải mã có thể bị in ra màn hình terminal dưới dạng plaintext. Thuộc tính `no_log: true` ngăn chặn 100% việc rò rỉ bí mật ra màn hình console log.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `no_log: true`.
- 1: Biết `no_log` để giấu log nhưng không giải thích được nguy cơ rò rỉ bí mật khi chạy cờ verbose `-vvv`.
- 2: Phân tích chính xác vai trò bảo mật màn hình console log và tệp nhật ký thi hành.
- 3: Nêu đúng + viết đoạn YAML minh họa task copy dùng `no_log: true`.
**Câu hỏi đào sâu:** Khi bật `no_log: true`, nếu task bị fail thì terminal hiển thị thông tin gì? *(Terminal chỉ hiển thị thông báo task fail nhưng ẩn toàn bộ giá trị biến nhạy cảm.)*

---

### Câu 11 — Tích hợp Ansible Vault với External Vault Services ★★★
**Hỏi:** Ngoài việc dùng tệp mật khẩu tĩnh `.vault_pass`, Ansible Vault có khả năng tích hợp với các hệ thống Quản lý Mật khẩu Doanh nghiệp (như HashiCorp Vault, CyberArk) ra sao?
**Đáp án chuẩn:**
Ansible Vault hỗ trợ cơ chế Vault Password Script: thay vì chỉ định một tệp tin tĩnh, tham số `vault_password_file` có thể trỏ tới một **bàn kịch bản có thể thực thi (Executable Script)** (ví dụ `vault_password_file = ./get_vault_pass.sh`). Khi thi hành, Ansible sẽ gọi script này để lấy mật khẩu giải mã trực tiếp từ HashiCorp Vault hoặc CyberArk API thông qua Token bảo mật.
**Tiêu chí chấm:**
- 0: Lầm tưởng Ansible Vault chỉ đọc được tệp mật khẩu file văn bản tĩnh.
- 1: Biết tích hợp với HashiCorp Vault nhưng không nêu được cơ chế Executable Script của `vault_password_file`.
- 2: Phân tích chính xác cơ chế Executable Password Script gọi API từ Secret Manager Doanh nghiệp.
- 3: Nêu đúng + viết ví dụ script bash đơn giản gọi API lấy token giải mã Vault.
**Câu hỏi đào sâu:** Tệp script `get_vault_pass.sh` bắt buộc phải có quyền thi hành gì trong Linux? *(Bắt buộc phải có quyền thi hành Executable `chmod +x`.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Ansible Vault ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên sử dụng Ansible Vault chuyên nghiệp, bảo mật 100% dữ liệu nhạy cảm và đạt chuẩn Idempotency.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Mã hóa 100% mật khẩu và private keys bằng `ansible-vault` (AES-256) trước khi commit Git.
2. **Quy tắc 2:** Sử dụng `encrypt_string` cho các chuỗi biến đơn lẻ để giữ tính dễ đọc cho file YAML.
3. **Quy tắc 3:** Phân quyền `chmod 0600` cho `.vault_pass` và thêm ngay vào tệp `.gitignore`.
4. **Quy tắc 4:** Tự động hóa giải mã trong CI/CD bằng Secret Variables và kết hợp `no_log: true` ẩn log console.
5. **Quy tắc 5:** Định kỳ rekey mật khẩu và đảm bảo lượt chạy Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy SecOps quản lý dữ liệu bí mật cấp Enterprise.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp ngăn ngừa nguy cơ rò rỉ mật khẩu lên mạng Internet công cộng? *(Quy tắc 3: Thêm `.vault_pass` vào `.gitignore`.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm bảo mật dữ liệu nhạy cảm và làm chủ Ansible Vault, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi áp dụng tiêu chuẩn SecOps nghiêm ngặt trong quản trị tự động hóa hạ tầng với Ansible Vault: bảo vệ 100% dữ liệu bí mật (mật khẩu DB, SSH Keys, API Tokens) qua thuật toán mã hóa đối xứng AES-256, sử dụng `encrypt_string` giữ nguyên tính trong sáng cho mã nguồn YAML. Tôi bảo vệ tệp mật khẩu `.vault_pass` với quyền `chmod 0600`, chặn 100% nguy cơ rò rỉ lên Git qua `.gitignore`, tự động hóa tiêm mật khẩu Vault trong pipeline CI/CD qua Secret Variables, kết hợp `no_log: true` triệt tiêu rủi ro lộ log console, định kỳ rekey đổi mật khẩu, đảm bảo mọi kịch bản Vault đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Đào Văn R | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Mai Thị S | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 21

Để chuẩn bị tốt nhất cho **Buổi 21: system-roles-selinux — RHEL System Roles, become elevation và SELinux**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** RHEL System Roles (`redhat.rhel_system_roles`) là gì? Tại sao Red Hat lại đóng gói sẵn các Role chuẩn hóa cho SELinux, Firewall, Timesync?
2. **Nghiên cứu trước 2:** Cơ chế nâng quyền `become: true` trong Ansible hoạt động ra sao bên dưới hệ điều hành Linux?
3. **Nghiên cứu trước 3:** Các module Ansible như `ansible.posix.selinux` và `ansible.posix.seport` dùng để quản lý trạng thái và cổng kết nối của SELinux như thế nào?

---


### [Chuyên Đề 21] Triển Khai System Roles & Tự Động Hóa SELinux / Firewalld: Quản Trị Chính Sách An Ninh OS Chuẩn RHEL/Ubuntu

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> RHEL System Roles (<code>redhat.rhel_system_roles</code>) là gì? Tại sao Red Hat lại khuyến nghị áp dụng bộ System Roles này trong các dự án tự động hóa Enterprise? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• RHEL System Roles là bộ sưu tập các Roles được Red Hat kiểm thử, bảo trì và phát hành chính thức để tự động hóa các dịch vụ hệ thống cốt lõi của RHEL (như SELinux, Firewall, Timesync, Network, Storage).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Lợi ích Enterprise:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> Tự động hóa chuẩn hóa theo Best Practices của Red Hat.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> Đảm bảo tính tương thích và ổn định 100% qua tất cả các phiên bản RHEL 8/9.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> Tiết kiệm 90% thời gian phát triển kịch bản tự động hóa hệ điều hành.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết RHEL System Roles.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết System Role để cấu hình RHEL nhưng không nêu được các lợi ích tuân thủ Best Practices của Red Hat.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác khái niệm và vai trò chuẩn hóa hệ thống RHEL.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ nạp collection <code>redhat.rhel_system_roles</code> trong <code>requirements.yml</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Kể tên 3 System Role phổ biến nhất trong bộ sưu tập RHEL System Roles. *(<code>redhat.rhel_system_roles.selinux</code>, <code>timesync</code>, <code>firewall</code>, <code>network</code>.)*
</div>
</details>

---

### Câu 2 — Cơ chế Nâng quyền `become: true` 🔥
**Hỏi:** Trình bày cơ chế nâng quyền `become: true`, `become_method: sudo`, và `become_user: root`. Tại sao Ansible khuyến nghị kết nối SSH ban đầu bằng user thường rồi mới `become`? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- Cơ chế hoạt động: Ansible kết nối SSH bằng tài khoản không phải root (user `ansible`), sau đó sử dụng lệnh `sudo` trên target node để thực thi Task dưới danh nghĩa `root` (UID 0).
- Lý do khuyến nghị:
  1. Bắt buộc theo chính sách an toàn thông tin: Cấm kết nối SSH trực tiếp bằng `root` qua mạng.
  2. Kiểm soát đặc quyền: Chỉ nâng quyền ở đúng những Task thực sự đòi hỏi quyền quản trị, giúp nhật ký audit log ghi nhận rõ ràng user nào vừa gọi sudo.
**Tiêu chí chấm:**
- 0: Không hiểu cơ chế nâng quyền `become`.
- 1: Biết `become: true` để thành root nhưng không giải thích được lý do an toàn thông tin cấm SSH root trực tiếp.
- 2: Phân tích chính xác cơ chế sudo escalation và nguyên tắc cấm SSH root qua mạng.
- 3: Nêu đúng + viết đoạn mã cấu hình `ansible.cfg` cài đặt `become = True` và `become_method = sudo`.
**Câu hỏi đào sâu:** Thuộc tính `become_ask_pass: False` trong `ansible.cfg` có tác dụng gì? *(Dùng để chỉ đạo Ansible không hỏi mật khẩu sudo tương tác khi tài khoản đã được cấu hình NOPASSWD.)*

---

### Câu 3 — Quản lý Trạng thái SELinux với `ansible.posix.selinux` 🔥
**Hỏi:** Trình bày 3 trạng thái của SELinux (Enforcing, Permissive, Disabled). Làm thế nào để quản lý trạng thái SELinux bằng module `ansible.posix.selinux`? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- 3 Trạng thái SELinux:
  1. `Enforcing`: SELinux bật cưỡng chế, chặn tất cả các hành vi vi phạm chính sách bảo mật.
  2. `Permissive`: SELinux không chặn, chỉ ghi lại nhật ký cảnh báo lỗi vào audit log (dùng để gỡ lỗi).
  3. `Disabled`: SELinux tắt hoàn toàn (KHÔNG KHUYẾN NGHỊ).
- Module Ansible: `ansible.posix.selinux: policy=targeted state=enforcing`. Module này tự động cập nhật tệp `/etc/selinux/config` để duy trì trạng thái qua các lần reboot.
**Tiêu chí chấm:**
- 0: Không biết 3 trạng thái SELinux.
- 1: Biết 3 trạng thái nhưng lầm tưởng khuyên dùng `disabled` để sửa lỗi.
- 2: Phân tích chính xác 3 trạng thái và cú pháp module `ansible.posix.selinux`.
- 3: Nêu đúng + viết đoạn Task YAML cấu hình SELinux sang `enforcing` chuẩn FQCN.
**Câu hỏi đào sâu:** Tại sao không được tắt SELinux sang `disabled` trên môi trường Production? *(Vì làm mất hoàn toàn lớp bảo mật kiểm soát truy cập bắt buộc MAC của kernel Linux, vi phạm quy chuẩn tuân thủ.)*

---

### Câu 4 — Gán Nhãn File Context với `ansible.posix.sefcontext` 🔥
**Hỏi:** Module `ansible.posix.sefcontext` dùng để làm gì? Tại sao việc dùng `sefcontext` lại vượt trội hoàn toàn so với chạy lệnh `chcon` thô? *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- Tác dụng: Dùng để ghi nhận quy tắc gán nhãn ngữ cảnh bảo mật tệp tin SELinux (File Context) cho các thư mục ứng dụng tùy chỉnh (ví dụ gán `/webdata` thành `httpd_sys_content_t`).
- Sự vượt trội: `sefcontext` ghi nhãn vĩnh viễn vào tệp cơ sở dữ liệu chính sách SELinux (`/etc/selinux/targeted/contexts/files/file_contexts.local`). Khi máy chủ reboot hoặc chạy `restorecon`, nhãn vẫn được giữ nguyên 100%. Ngược lại, lệnh `chcon` chỉ gán nhãn tạm thời trên inode đĩa, nhãn sẽ bị mất sạch khi chạy `restorecon`.
**Tiêu chí chấm:**
- 0: Không biết module `sefcontext`.
- 1: Biết gán nhãn file nhưng không phân biệt được tính vĩnh viễn của `sefcontext` vs tính tạm thời của `chcon`.
- 2: Phân tích chính xác cơ chế lưu vĩnh viễn vào chính sách SELinux local policy của `sefcontext`.
- 3: Nêu đúng + viết đoạn Task YAML gán nhãn `/webdata(/.*)?` thành `httpd_sys_content_t`.
**Câu hỏi đào sâu:** Lệnh Linux nào phải chạy ngay sau `sefcontext` để áp dụng nhãn mới lên đĩa? *(Lệnh `restorecon -Rv /path`.)*

---

### Câu 5 — Gán Nhãn Cổng SELinux Port Type với `ansible.posix.seport` 🔥
**Hỏi:** Trình bày tác dụng của module `ansible.posix.seport`. Khi nào quản trị viên bắt buộc phải sử dụng module này? *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Tác dụng: Dùng để gán nhãn loại cổng dịch vụ (Port Type) cho các cổng mạng trong SELinux.
- Trường hợp bắt buộc: Khi cấu hình dịch vụ lắng nghe trên cổng phi tiêu chuẩn (Non-standard Port). Ví dụ: SELinux mặc định chỉ cho phép Nginx/Apache lắng nghe trên cổng 80, 443 (nhãn `http_port_t`). Nếu đổi Nginx sang chạy cổng 8080 hoặc 8443, SELinux sẽ chặn kết nối. Bắt buộc phải dùng `seport` để đăng ký cổng 8080 vào nhãn `http_port_t`.
**Tiêu chí chấm:**
- 0: Không biết module `seport`.
- 1: Biết đổi cổng nhưng không giải thích được khái niệm cổng phi tiêu chuẩn trong SELinux.
- 2: Phân tích chính xác cơ chế gán nhãn `http_port_t` cho cổng tùy chỉnh qua `seport`.
- 3: Nêu đúng + viết đoạn Task YAML mở cổng 8080 protocol tcp bằng `seport`.
**Câu hỏi đào sâu:** Lệnh CLI Linux thô tương đương với module `seport` là gì? *(Lệnh `semanage port -a -t http_port_t -p tcp 8080`.)*

---

### Câu 6 — Cấu hình Sudoers An toàn với `/etc/sudoers.d/`
**Hỏi:** Tại sao quản trị viên nên tạo tệp cấu hình sudoers riêng trong `/etc/sudoers.d/ansible` thay vì chỉnh sửa trực tiếp tệp `/etc/sudoers` gốc? Cờ `validate` có tác dụng gì? *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- Lý do tách file: Sửa tệp `/etc/sudoers` gốc có nguy cơ làm hỏng cú pháp toàn bộ hệ thống, trong khi tạo file riêng trong `/etc/sudoers.d/` giúp quản lý mô-đun hóa sạch sẽ và dễ thu hồi quyền.
- Tác dụng cờ `validate: /usr/sbin/visudo -cf %s`: Chỉ đạo Ansible chạy công cụ `visudo` kiểm tra cú pháp của tệp tạm trước khi chép đè vào `/etc/sudoers.d/ansible`. Nếu có lỗi cú pháp, Ansible sẽ hủy task ngay lập tức, ngăn ngừa nguy cơ hỏng quyền sudo của server.
**Tiêu chí chấm:**
- 0: Không biết thư mục `/etc/sudoers.d/`.
- 1: Biết tạo file trong `sudoers.d/` nhưng không giải thích được tác dụng của cờ `validate`.
- 2: Phân tích chính xác vai trò mô-đun hóa và cơ chế kiểm tra cú pháp an toàn của `visudo validate`.
- 3: Nêu đúng + viết đoạn Task YAML copy file sudoers NOPASSWD có cờ `validate`.
**Câu hỏi đào sâu:** Phân quyền Linux bắt buộc cho các tệp trong `/etc/sudoers.d/` là bao nhiêu? *(Bắt buộc là `0440` hoặc `0400`.)*

---

### Câu 7 — Quản lý User và Group bằng Module FQCN
**Hỏi:** Nêu các tham số chính của module `ansible.builtin.user` và `ansible.builtin.group` để tạo người dùng `sys_admin` thuộc nhóm `sysops` có shell `/bin/bash`. *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
Task YAML mẫu:
```yaml
- name: Create sysops group
  ansible.builtin.group:
    name: sysops
    state: present

- name: Create sys_admin user
  ansible.builtin.user:
    name: sys_admin
    group: sysops
    shell: /bin/bash
    state: present
```
Các tham số chính: `name`, `group`, `groups` (nhóm phụ), `shell`, `home`, `state`, `remove`.
**Tiêu chí chấm:**
- 0: Không biết module `ansible.builtin.user`.
- 1: Viết được YAML nhưng dùng lệnh `useradd` thô qua module `shell`.
- 2: Phân tích chính xác các tham số chuẩn FQCN của module `group` và `user`.
- 3: Nêu đúng + viết đoạn Playbook chuẩn tạo cả nhóm và user kết hợp `become: true`.
**Câu hỏi đào sâu:** Làm thế nào để xóa một user và xóa luôn thư mục home của user đó bằng module `user`? *(Khai báo `state: absent` và `remove: yes`.)*

---

### Câu 8 — Sử dụng RHEL System Role `redhat.rhel_system_roles.selinux`
**Hỏi:** Trình bày cấu trúc khai báo biến để sử dụng RHEL System Role `redhat.rhel_system_roles.selinux` quản lý đồng thời SELinux state và SELinux ports. *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
Khai báo mảng biến cấu hình tập trung ở cấp Playbook hoặc `group_vars`:
```yaml
vars:
  selinux_policy: targeted
  selinux_state: enforcing
  selinux_ports:
    - ports: '8080'
      protocol: 'tcp'
      setype: 'http_port_t'
      state: 'present'
roles:
  - role: redhat.rhel_system_roles.selinux
```
**Tiêu chí chấm:**
- 0: Không biết cách gọi RHEL System Role `selinux`.
- 1: Biết gọi Role nhưng không nêu được các biến chuẩn `selinux_state` và `selinux_ports`.
- 2: Phân tích chính xác cơ chế truyền biến cho RHEL System Role SELinux.
- 3: Nêu đúng + viết đoạn Playbook hoàn chỉnh gọi System Role SELinux.
**Câu hỏi đào sâu:** Làm thế nào để gán nhãn File Context qua RHEL System Role `selinux`? *(Sử dụng mảng biến `selinux_fcontexts`.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng System Roles 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook cấu hình nâng quyền, User và SELinux để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective RHCE EX294 #3 & #15).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-selinux.yml`: Các Task tạo sudoers, tạo User `sys_admin`, gán nhãn SELinux thực thi báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-selinux.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 id sys_admin` kiểm tra user thực sự tồn tại thuộc nhóm `sysops`, và `docker exec target1 getenforce` kiểm tra trạng thái SELinux.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file/user thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát user/selinux.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE EX294 #3 & #15 (`☑`).
**Câu hỏi đào sâu:** Nếu lệnh `docker exec target1 getenforce` báo `Enforcing`, điều đó chứng minh điều gì? *(Chứng minh SELinux đang hoạt động ở trạng thái cưỡng chế bảo mật đúng yêu cầu.)*

---

### Câu 10 — Quản lý SELinux Booleans với `ansible.posix.seboolean` ★★★
**Hỏi:** SELinux Booleans là gì? Module `ansible.posix.seboolean` dùng để bật/tắt các công tắc bảo mật của SELinux ra sao?
**Đáp án chuẩn:**
- SELinux Booleans: Là các công tắc bật/tắt (On/Off switches) trong chính sách SELinux, cho phép thay đổi hành vi bảo mật của dịch vụ mà không cần biên dịch lại chính sách.
- Module Ansible: `ansible.posix.seboolean` dùng để thay đổi trạng thái Boolean:
  ```yaml
  - name: Allow Apache to send mail
    ansible.posix.seboolean:
      name: httpd_can_sendmail
      state: true
      persistent: true
  ```
  Tham số `persistent: true` đảm bảo trạng thái Boolean không bị mất sau khi reboot.
**Tiêu chí chấm:**
- 0: Không biết SELinux Booleans.
- 1: Biết công tắc Boolean nhưng không nêu được tham số `persistent: true`.
- 2: Phân tích chính xác cơ chế công tắc Boolean và tầm quan trọng của `persistent: true`.
- 3: Nêu đúng + viết đoạn Task YAML bật boolean `httpd_can_network_connect_db`.
**Câu hỏi đào sâu:** Lệnh CLI Linux thô tương đương với module `seboolean` là gì? *(Lệnh `setsebool -P httpd_can_sendmail on`.)*

---

### Câu 11 — Xử lý Sự cố SELinux Audit Log với `sealert` ★★★
**Hỏi:** Khi một ứng dụng bị SELinux chặn kết nối gây lỗi `Permission Denied`, quản trị viên sử dụng công cụ nào trên RHEL để phân tích nguyên nhân và lấy gợi ý sửa lỗi từ Ansible?
**Đáp án chuẩn:**
Quy trình gỡ lỗi SELinux chuyên nghiệp:
1. **Kiểm tra audit log:** Soi file `/var/log/audit/audit.log` hoặc nhật ký `journalctl -t setroubleshoot`.
2. **Phân tích với `sealert`:** Chạy lệnh `sealert -l <AVC_ID>` để đọc phân tích chi tiết nguyên nhân gốc rễ.
3. **Áp dụng gợi ý vào Ansible:** Lấy thông tin File Context hoặc Port Type bị chặn từ `sealert` để bổ sung vào task `ansible.posix.sefcontext` hoặc `seport` trong Playbook.
**Tiêu chí chấm:**
- 0: Không biết cách gỡ lỗi SELinux, trả lời "tắt SELinux đi cho xong".
- 1: Biết xem audit log nhưng không nêu được công cụ `sealert` và cách đưa gợi ý vào Ansible.
- 2: Phân tích chính xác quy trình gỡ lỗi AVC denial và chuyển đổi gợi ý sang Ansible module.
- 3: Nêu đúng + thể hiện tư duy xử lý sự cố bảo mật RHEL chuẩn Enterprise.
**Câu hỏi đào sâu:** AVC trong SELinux audit log là viết tắt của từ gì? *(Access Vector Cache.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về System Roles và SELinux ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên tự động hóa bảo mật RHEL, quản lý SELinux chuyên nghiệp và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Khai thác bộ RHEL System Roles (`redhat.rhel_system_roles`) để chuẩn hóa cấu hình RHEL.
2. **Quy tắc 2:** Nâng quyền an toàn với `become: true` và cấu hình sudoers `NOPASSWD` qua tệp riêng `/etc/sudoers.d/ansible`.
3. **Quy tắc 3:** Giữ SELinux ở trạng thái `enforcing` 100%, không bao giờ tắt SELinux trên Production.
4. **Quy tắc 4:** Gán nhãn File Context vĩnh viễn với `sefcontext` + `restorecon` và gán nhãn cổng tùy chỉnh với `seport`.
5. **Quy tắc 5:** Quản lý User/Group qua module FQCN `ansible.builtin.user` và đảm bảo Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy SecOps chuẩn hóa RHEL Enterprise.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp bảo vệ tính toàn vẹn của hệ điều hành RHEL? *(Quy tắc 3: Giữ SELinux ở trạng thái `enforcing`.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm quản trị bảo mật RHEL, nâng quyền become và làm chủ SELinux với Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi tự động hóa và chuẩn hóa 100% cấu hình bảo mật hệ điều hành Red Hat Enterprise Linux theo tiêu chuẩn Red Hat Enterprise SecOps: nâng quyền kiểm soát đặc quyền an toàn qua `become: true` và file sudoers NOPASSWD mô-đun hóa có cờ `validate`, khai thác bộ RHEL System Roles (`redhat.rhel_system_roles`) cho các dịch vụ hệ thống cốt lõi. Tôi duy trì trạng thái SELinux `enforcing` tuyệt đối trên Sản xuất, làm chủ các module `ansible.posix.selinux`, `sefcontext` (kết hợp `restorecon`) và `seport` để mở rộng ngữ cảnh bảo mật tệp tin và cổng dịch vụ tùy chỉnh mà không làm suy giảm lá chắn an toàn, quản lý tài khoản chuẩn FQCN, đảm bảo mọi kịch bản RHEL Security đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Trịnh Văn T | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Đỗ Thị U | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 22

Để chuẩn bị tốt nhất cho **Buổi 22: strategy-performance — Strategy và hiệu năng: forks, serial, pipelining**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Tham số `forks` trong `ansible.cfg` có tác dụng gì đối với số lượng máy chủ thi hành song song? Mặc định `forks` bằng bao nhiêu?
2. **Nghiên cứu trước 2:** Phân biệt sự khác nhau giữa 2 chiến lược thi hành Playbook (Execution Strategy): `strategy: linear` vs `strategy: free`?
3. **Nghiên cứu trước 3:** Từ khóa `serial:` ở cấp Playbook được áp dụng ra sao trong bài toán Rolling Update (nâng cấp cuốn chiếu từng cụm server)?

---


### [Chuyên Đề 22] Tối Ưu Hiệu Năng & Tốc Độ Thực Thi: Forks, Free Strategy, Pipelining, ControlPersist SSH & Mitogen Accelerator

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Tham số <code>forks</code> trong <code>ansible.cfg</code> quy định điều gì? Mặc định <code>forks</code> bằng bao nhiêu? Tại sao điều chỉnh <code>forks</code> lại là bước đầu tiên khi tối ưu Playbook quy mô lớn? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Quy định: Tham số <code>forks</code> quy định số lượng kết nối SSH và tiến trình xử lý song song tối đa mà Control Node có thể mở đồng thời tới các máy chủ Managed Nodes.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Mặc định: <code>forks = 5</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Lý do điều chỉnh: Với hạ tầng 100 máy chủ, nếu giữ mặc định 5, Ansible phải chia làm 20 đợt chạy nối tiếp. Tăng <code>forks = 10</code> hoặc <code>20</code> giúp Ansible tận dụng sức mạnh đa nhân CPU của Control Node, giảm 75% thời gian chờ đợi qua mạng SSH.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết tham số <code>forks</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết <code>forks</code> quy định số máy nhưng không nhớ mặc định 5 và cách tính toán tối ưu theo RAM/CPU.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác cơ chế mở tiến trình song song SSH của <code>forks</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + viết đoạn cấu hình <code>ansible.cfg</code> cài đặt <code>forks = 10</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Công thức ước tính số <code>forks</code> an toàn dựa trên dung lượng RAM của Control Node là gì? *(<code>forks = (RAM_GB - 2) * 20</code>, giả định mỗi fork tốn khoảng 50MB RAM.)*
</div>
</details>

---

### Câu 2 — Kỹ thuật Đường ống SSH Pipelining 🔥
**Hỏi:** SSH Pipelining (`pipelining = True`) hoạt động ra sao bên dưới? Tại sao bật Pipelining lại giúp giảm 50% số lượng giao dịch SSH và tăng tốc Playbook gấp 2 lần? *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- Cơ chế hoạt động: Mặc định Ansible thực thi từng Task qua 3 bước: chép file script Python tạm lên `/tmp` máy đích -> mở kết nối SSH thứ hai để thi hành -> mở kết nối SSH thứ ba để xóa file tạm. Khi bật `pipelining = True`, Ansible sẽ nạp thẳng lệnh Python trực tiếp vào luồng stdin của kết nối SSH mở sẵn mà không cần chép tệp tạm ra đĩa.
- Lợi ích: Triệt tiêu hoàn bộ chi phí I/O ghi đĩa `/tmp` và giảm 50% số lượng giao dịch kết nối SSH, giúp Playbook chạy siêu tốc.
**Tiêu chí chấm:**
- 0: Không biết tính năng SSH Pipelining.
- 1: Biết `pipelining = True` làm nhanh nhưng không giải thích được cơ chế bỏ qua chép file tạm Python lên `/tmp`.
- 2: Phân tích chính xác cơ chế truyền lệnh qua stdin SSH stream của Pipelining.
- 3: Nêu đúng + viết đoạn cấu hình `[ssh_connection] pipelining = True` trong `ansible.cfg`.
**Câu hỏi đào sâu:** Điều kiện tiên quyết trên tệp `/etc/sudoers` của máy đích để SSH Pipelining hoạt động trôi chảy là gì? *(Tệp `/etc/sudoers` không được chứa thuộc tính `requiretty` - tức phải có `Defaults !requiretty`.)*

---

### Câu 3 — Phân biệt Execution Strategy `linear` vs `free` 🔥
**Hỏi:** Phân biệt sự khác nhau giữa 2 chiến lược thi hành `strategy: linear` (mặc định) và `strategy: free`. Khi nào nên dùng `strategy: free`? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- `strategy: linear` (mặc định): Thực thi đồng bước theo từng Task. 100% máy chủ phải hoàn thành xong Task 1 mới được chuyển sang Task 2. Nếu có 1 máy bị chậm, tất cả các máy khác đều phải đứng chờ.
- `strategy: free`: Thực thi tự do theo từng Host. Mỗi máy chủ sẽ liên tục chạy liền mạch từ Task 1 -> Task 2 -> Task 3 mà không cần chờ đợi các máy chủ khác.
- Khi nên dùng `free`: Khi các Task không có sự phụ thuộc lẫn nhau giữa các máy chủ (như thu thập log, dọn dẹp đĩa, cài đặt package độc lập) và muốn tối ưu thời gian hoàn thành nhanh nhất.
**Tiêu chí chấm:**
- 0: Không biết từ khóa `strategy`.
- 1: Biết `free` chạy nhanh hơn `linear` nhưng không giải thích được cơ chế bỏ qua chốt chờ đồng bước giữa các host.
- 2: Phân tích chính xác điểm khác biệt giữa đồng bước theo Task (`linear`) và tự do theo Host (`free`).
- 3: Nêu đúng + viết đoạn Playbook YAML khai báo `strategy: free`.
**Câu hỏi đào sâu:** Tại sao kịch bản Migrate Database trước rồi mới Update Web App lại KHÔNG ĐƯỢC dùng `strategy: free`? *(Vì `free` có thể khiến một số Web node tự ý chạy sang task Update Web App trước khi DB node hoàn thành task Migrate DB.)*

---

### Câu 4 — Quản lý Nâng cấp Cuốn chiếu Rolling Update với `serial:` 🔥
**Hỏi:** Từ khóa `serial:` ở cấp Playbook có tác dụng gì? Trình bày kịch bản áp dụng `serial:` để giữ Zero Downtime cho cụm Web Server Production 10 máy. *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Tác dụng: Dùng để chia nhỏ cụm máy chủ target thành các lô (Batch) nâng cấp cuốn chiếu nối tiếp nhau, ngăn ngừa nguy cơ sập toàn bộ dịch vụ cùng một lúc.
- Kịch bản Zero Downtime (10 máy Web đằng sau Load Balancer):
  Khai báo `serial: 2` (hoặc `serial: "20%"`). Ansible sẽ lấy 2 máy đầu tiên ra nâng cấp, kiểm tra sức khỏe OK rồi mới tiếp tục nâng cấp 2 máy tiếp theo. Trong suốt quá trình, 80% số máy còn lại vẫn liên tục phục vụ lưu lượng người dùng, đảm bảo Zero Downtime.
**Tiêu chí chấm:**
- 0: Không biết từ khóa `serial`.
- 1: Biết `serial` để chạy từng đợt nhưng không nêu được bài toán Zero Downtime cho Production.
- 2: Phân tích chính xác cơ chế chia lô Batching của `serial` và lợi ích bảo vệ dịch vụ.
- 3: Nêu đúng + viết đoạn Playbook YAML khai báo `serial: 2` hoặc `serial: "20%"`.
**Câu hỏi đào sâu:** Chuyện gì xảy ra nếu lô máy chủ đầu tiên trong `serial: 1` bị thi hành thất bại (`failed > 0`)? *(Ansible lập tức dừng toàn bộ Playbook, 9 máy còn lại trong cụm được bảo vệ an toàn 100%.)*

---

### Câu 5 — Nhiệm vụ Bất đồng bộ `async` và `poll: 0` 🔥
**Hỏi:** Trình bày ý nghĩa của thuộc tính `async: 60` và `poll: 0` trong một Task. Khi nào bắt buộc phải dùng `async`? *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Ý nghĩa:
  + `async: 60`: Cho phép Task thi hành bất đồng bộ ngầm trên máy đích với thời lượng tối đa 60 giây.
  + `poll: 0`: Chỉ đạo Ansible giao nhiệm vụ xong là lập tức ngắt đứng chờ, chuyển sang thi hành Task tiếp theo ngay trong Playbook.
- Khi bắt buộc phải dùng: Khi thi hành các Task nặng kéo dài (như backup database 500GB, download tệp ISO 20GB, hoặc khởi động lại dịch vụ tốn 15 phút) để tránh bị đứt kết nối SSH Timeout.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `async` và `poll`.
- 1: Biết `async` để chạy ngầm nhưng nhầm lẫn ý nghĩa của `poll: 0` vs `poll: 5`.
- 2: Phân tích chính xác cơ chế giao nhiệm vụ ngầm và ngăn ngừa SSH Timeout của `async` + `poll: 0`.
- 3: Nêu đúng + viết đoạn Task YAML minh họa chạy `sleep 10` với `async: 60` và `poll: 0`.
**Câu hỏi đào sâu:** Nếu để `poll: 5` thay vì `poll: 0` thì Ansible xử lý ra sao? *(Ansible sẽ đứng chờ và cứ 5 giây lại kiểm tra xem task bất đồng bộ đã xong chưa - vẫn bị giữ luồng execution.)*

---

### Câu 6 — Theo dõi Tiến độ với `ansible.builtin.async_status`
**Hỏi:** Làm thế nào để theo dõi và xác nhận kết quả của một async job chạy ngầm trước đó bằng module `ansible.builtin.async_status`? *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
Quy trình 2 bước:
1. **Bước 1 (Khởi chạy & Lưu Job ID):**
   ```yaml
   - name: Start long backup job
     ansible.builtin.command: /usr/local/bin/backup.sh
     async: 300
     poll: 0
     register: backup_res
   ```
2. **Bước 2 (Kiểm tra với `async_status`):**
   ```yaml
   - name: Poll backup job status
     ansible.builtin.async_status:
       jid: "{{ backup_res.ansible_job_id }}"
     register: job_stat
     until: job_stat.finished
     retries: 30
     delay: 5
     changed_when: false
   ```
**Tiêu chí chấm:**
- 0: Không biết module `async_status`.
- 1: Biết `async_status` nhưng không nhớ thuộc tính `ansible_job_id` và vòng lặp `until:`.
- 2: Phân tích chính xác cơ chế dùng `jid` và vòng lặp `until: job_stat.finished`.
- 3: Nêu đúng + viết đoạn Playbook YAML hoàn chỉnh minh họa cả 2 bước.
**Câu hỏi đào sâu:** Tại sao task `async_status` nên khai báo thêm `changed_when: false`? *(Để tránh task thăm dò kiểm tra trạng thái liên tục báo `changed=1` ở Lần chạy thứ 2.)*

---

### Câu 7 — Triển khai Canary Deployment với Mảng `serial:`
**Hỏi:** Trình bày cú pháp mảng `serial: ["1", "30%", "100%"]`. Mô hình triển khai Canary Deployment này bảo vệ hạ tầng Production ra sao? *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- Cú pháp mảng:
  ```yaml
  serial:
    - 1
    - "30%"
    - "100%"
  ```
- Cơ chế bảo vệ Canary Deployment:
  + **Batch 1 (1 máy):** Thử nghiệm Canary. Nếu code mới có lỗi nghiêm trọng, chỉ duy nhất 1 máy bị ảnh hưởng, Ansible dừng ngay lập tức.
  + **Batch 2 (30% máy):** Nếu Batch 1 OK, mở rộng nâng cấp cho 30% số máy để theo dõi tải.
  + **Batch 3 (100% máy):** Khi Batch 2 OK, nâng cấp toàn bộ số máy còn lại.
**Tiêu chí chấm:**
- 0: Không biết mảng `serial:`.
- 1: Biết viết mảng nhưng không giải thích được chiến thuật thử nghiệm Canary Deployment.
- 2: Phân tích chính xác cơ chế mở rộng lô nâng cấp tăng dần Canary.
- 3: Nêu đúng + viết đoạn Playbook YAML sử dụng mảng `serial:`.
**Câu hỏi đào sâu:** Dấu ngoặc kép xung quanh `"30%"` có bắt buộc không? *(Bắt buộc, nếu thiếu ngoặc kép YAML parser sẽ báo lỗi cú pháp.)*

---

### Câu 8 — Tối ưu hóa Kết nối SSH ControlPersist
**Hỏi:** Thuộc tính `ControlPersist=60s` trong cấu hình SSH của Ansible giúp tiết kiệm tài nguyên mạng và thời gian thi hành ra sao? *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
- Cơ chế: `ControlPersist=60s` (kết hợp `ControlMaster=auto`) chỉ đạo SSH client giữ kết nối mạng Unix socket tới máy đích mở sẵn trong 60 giây sau khi một Task hoàn thành.
- Tiết kiệm: Khi Task tiếp theo chạy trên cùng host đó trong vòng 60 giây, Ansible sẽ tái sử dụng ngay socket SSH mở sẵn mà không cần thực hiện lại quy trình bắt tay xác thực SSH Key (SSH Handshake). Điều này triệt tiêu hoàn toàn độ trễ 1-2 giây xác thực ban đầu của từng Task.
**Tiêu chí chấm:**
- 0: Không biết tùy chọn `ControlPersist`.
- 1: Biết giữ kết nối SSH nhưng không giải thích được cơ chế Unix socket reuse và triệt tiêu SSH handshake.
- 2: Phân tích chính xác vai trò tái sử dụng socket SSH của `ControlPersist`.
- 3: Nêu đúng + viết dòng cấu hình `ssh_args` chứa `ControlPersist=60s` trong `ansible.cfg`.
**Câu hỏi đào sâu:** Tệp Unix socket của SSH ControlMaster mặc định được lưu ở đâu trên Control Node? *(Lưu trong thư mục `~/.ansible/cp/`.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Tối ưu Hiệu năng 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook áp dụng chiến lược thi hành `strategy: free`, `serial:`, `async` và SSH Pipelining để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective Performance Tuning & Rolling Update).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-performance.yml`: Tối ưu SSH Pipelining giúp kịch bản thi hành siêu tốc, Task chép file cấu hình hiệu năng thực thi báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-performance.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/performance-app.conf` kiểm tra file cấu hình thực sự tồn tại đúng dữ liệu `FORKS=10` và `PIPELINING=ENABLED`.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file render.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective Performance Tuning & Rolling Update.
**Câu hỏi đào sâu:** Việc đo thời gian thi hành Playbook ở Lần 2 có nhanh hơn Lần 1 không? *(Lần 2 chạy nhanh hơn gấp nhiều lần vì không có Task nào phải ghi đĩa `changed=0` và SSH socket đã mở sẵn.)*

---

### Câu 10 — Plugin Profiling `profile_tasks` Đo Thời gian Task ★★★
**Hỏi:** Làm thế nào để bật plugin `profile_tasks` trong Ansible để phát hiện chính xác Task nào đang ngốn nhiều thời gian nhất trong Playbook?
**Đáp án chuẩn:**
Khai báo trong tệp `ansible.cfg`:
```ini
[defaults]
callbacks_enabled = profile_tasks
```
Khi thi hành Playbook, Ansible sẽ tự động in ra bảng thống kê danh sách Top 10 Task ngốn nhiều thời gian thi hành nhất ở cuối chương trình, giúp kỹ sư biết chính xác Task nào cần áp dụng `async` hoặc tối ưu hóa.
**Tiêu chí chấm:**
- 0: Không biết plugin `profile_tasks`.
- 1: Biết đo thời gian nhưng không nhớ thuộc tính `callbacks_enabled = profile_tasks` trong `ansible.cfg`.
- 2: Phân tích chính xác cơ chế profiling in bảng Top 10 Task ngốn thời gian.
- 3: Nêu đúng + viết đoạn cấu hình `ansible.cfg` kích hoạt callback plugin.
**Câu hỏi đào sâu:** Ngoài `profile_tasks`, callback plugin nào giúp đo tổng thời gian thi hành của toàn bộ Playbook? *(`profile_roles` hoặc `timer`.)*

---

### Câu 11 — Quản lý Lỗi Rolling Update với `max_fail_percentage` ★★★
**Hỏi:** Từ khóa `max_fail_percentage:` trong Ansible Playbook dùng để làm gì khi kết hợp với Rolling Update `serial:`?
**Đáp án chuẩn:**
- Tác dụng: Quy định tỷ lệ phần trăm số máy chủ lỗi tối đa cho phép trong một đợt (Batch). Nếu tỷ lệ lỗi vượt quá `max_fail_percentage`, Ansible mới dừng Playbook; nếu số máy lỗi thấp hơn tỷ lệ này, Ansible vẫn cho phép tiếp tục nâng cấp các đợt tiếp theo.
- Ví dụ: Trong lô 100 máy, khai báo `serial: 10` và `max_fail_percentage: 20`. Nếu trong lô 10 máy có 1 máy bị lỗi (10% < 20%), Ansible vẫn coi lô đó chấp nhận được và đi tiếp lô sau.
**Tiêu chí chấm:**
- 0: Không biết `max_fail_percentage`.
- 1: Biết tỷ lệ lỗi nhưng không giải thích được mối kết hợp với `serial:`.
- 2: Phân tích chính xác cơ chế tính ngưỡng tỷ lệ lỗi chấp nhận được cho từng batch.
- 3: Nêu đúng + viết đoạn YAML Playbook sử dụng `serial:` và `max_fail_percentage:`.
**Câu hỏi đào sâu:** Mặc định nếu không khai báo `max_fail_percentage`, chỉ cần 1 host bị fail thì Ansible xử lý ra sao? *(Mặc định chỉ cần 1 host fail là lô đó bị coi là failed và dừng Playbook.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Performance Tuning & Strategy ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên tối ưu hiệu năng Playbook gấp 5 lần, triển khai Rolling Update an toàn và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Đặt `forks = 10` (hoặc lớn hơn) và bật `pipelining = True` trong `ansible.cfg` để tối ưu SSH song song.
2. **Quy tắc 2:** Sử dụng `strategy: free` cho các kịch bản không có phụ thuộc bước giữa các host để bứt phá tốc độ.
3. **Quy tắc 3:** Áp dụng `serial: ["1", "30%", "100%"]` giữ Zero Downtime và bảo vệ hạ tầng Production.
4. **Quy tắc 4:** Chuyển các Task nặng ngầm sang bất đồng bộ `async:` / `poll: 0` và theo dõi qua `async_status`.
5. **Quy tắc 5:** Duy trì SSH `ControlPersist=60s` và đảm bảo Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy tối ưu hiệu năng Enterprise.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp triệt tiêu độ trễ mạng SSH giữa Control Node và Managed Nodes? *(Quy tắc 1 & 5: SSH Pipelining & ControlPersist.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm tối ưu hóa hiệu năng Playbook quy mô lớn và quản lý Rolling Update với Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi làm chủ các giải pháp tối ưu hóa hiệu năng toàn diện cho Ansible trên hạ tầng Enterprise: tăng tốc độ thi hành gấp 5-10 lần bằng cách nâng `forks = 20`, bật SSH `pipelining = True` triệt tiêu overhead tệp tạm, duy trì socket SSH với `ControlPersist=60s`, áp dụng linh hoạt `strategy: free` cho các tác vụ độc lập. Tôi bảo vệ tuyệt đối tính khả dụng Zero Downtime cho cụm Production bằng quy trình Rolling Update Canary phân tầng `serial: ['1', '30%', '100%']`, quản lý các tác vụ nặng ngầm qua `async` và `ansible.builtin.async_status`, đồng thời đảm bảo mọi kịch bản tối ưu hiệu năng đạt chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Phan Văn V | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Vũ Thị X | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 23

Để chuẩn bị tốt nhất cho **Buổi 23: error-handling-nang-cao — Error handling nâng cao: retry, any_errors_fatal, ignore_errors**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Thuộc tính `ignore_errors: true` khác gì với `failed_when:` trong việc xử lý lỗi Task?
2. **Nghiên cứu trước 2:** Từ khóa `any_errors_fatal: true` ở cấp Playbook có tác dụng gì khi 1 host trong cụm bị fail?
3. **Nghiên cứu trước 3:** Làm thế nào để cấu hình tự động thử lại (Retry mechanism) cho một Task bị lỗi mạng bằng `until:`, `retries:`, và `delay:`?

---


### [Chuyên Đề 23] Quản Trị Lỗi Nâng Cao: failed_when, changed_when, ignore_errors, ignore_unreachable & any_errors_fatal

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Thuộc tính <code>ignore_errors: true</code> trong Ansible Task có tác dụng gì? Khi nào NÊN và KHÔNG NÊN sử dụng <code>ignore_errors: true</code>? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Tác dụng: Cho phép Ansible tiếp tục thi hành các Task phía sau trong Playbook ngay cả khi Task hiện tại bị trả về trạng thái lỗi (<code>failed</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• khi NÊN dùng: Cho các task kiểm tra thông tin không quan trọng (như dọn dẹp file tạm <code>/tmp</code>, xóa cache cũ) mà sự thất bại của nó không ảnh hưởng đến kịch bản chính.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Khi KHÔNG NÊN dùng: Tuyệt đối KHÔNG dùng cho các task nạp biến mật khẩu, cài đặt package phần mềm cốt lõi, hoặc định hình cấu hình hệ thống.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết thuộc tính <code>ignore_errors</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết <code>ignore_errors</code> để cho qua lỗi nhưng không phân biệt được trường hợp NÊN và KHÔNG NÊN dùng.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác tác dụng và cảnh báo nguy cơ che đậy lỗi nghiêm trọng của <code>ignore_errors</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + viết đoạn Task YAML minh họa dọn dẹp cache dùng <code>ignore_errors: true</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Thuộc tính <code>ignore_unreachable: true</code> khác <code>ignore_errors: true</code> như thế nào? *(<code>ignore_errors</code> bỏ qua lỗi execution của module; <code>ignore_unreachable</code> bỏ qua lỗi mất kết nối SSH tới máy đích.)*
</div>
</details>

---

### Câu 2 — Dừng Toàn Cụm khi Có Lỗi với `any_errors_fatal` 🔥
**Hỏi:** Từ khóa `any_errors_fatal: true` ở cấp Playbook xử lý ra sao khi 1 host trong cụm 10 host bị thi hành thất bại? Tại sao thuộc tính này lại quan trọng trong triển khai cụm Cluster? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- Cơ chế xử lý: Mặc định Ansible chỉ dừng host bị lỗi và tiếp tục chạy 9 host còn lại. Khi có `any_errors_fatal: true`, nếu 1 host bị lỗi, Ansible sẽ lập tức CANCEL toàn bộ Playbook trên tất cả 9 host còn lại ngay ở bước đó.
- Tầm quan trọng: Bảo vệ an toàn tuyệt đối cho cụm Cluster (như Database, Kubernetes, Ceph Storage): ngắt toàn cụm ngay lập tức để kỹ sư kiểm tra, ngăn ngừa thảm họa mất đồng bộ dữ liệu (Split-Brain).
**Tiêu chí chấm:**
- 0: Không biết từ khóa `any_errors_fatal`.
- 1: Biết ngắt Playbook nhưng không giải thích được bài toán bảo vệ tính đồng bộ cho cụm Cluster.
- 2: Phân tích chính xác cơ chế ngắt toàn cụm của `any_errors_fatal` và bài toán chống Data Split-Brain.
- 3: Nêu đúng + viết đoạn Playbook YAML khai báo `any_errors_fatal: true`.
**Câu hỏi đào sâu:** Nếu muốn chấp nhận tối đa 20% số host bị lỗi trước khi ngắt toàn cụm thì dùng thuộc tính nào? *(Dùng thuộc tính `max_fail_percentage: 20`.)*

---

### Câu 3 — Bảo vệ Handler với `force_handlers` 🔥
**Hỏi:** Thuộc tính `force_handlers: true` giải quyết vấn đề gì khi Playbook bị ngắt giữa chừng do một Task phía sau bị lỗi? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Vấn đề giải quyết: Mặc định nếu Task 1 sửa file cấu hình và `notify: Restart Service`, nhưng Task 2 phía sau bị lỗi, Ansible sẽ ngắt Playbook và BỎ QUA không chạy Handler `Restart Service`. Kết quả là dịch vụ bị giữ nguyên cấu hình cũ chưa được nạp.
- Tác dụng: `force_handlers: true` ép buộc Ansible phải thực thi toàn bộ các Handlers đã được thông báo (`notify:`) trước đó ngay cả khi Playbook bị dừng do lỗi ở Task sau, bảo vệ dịch vụ được cập nhật cấu hình an toàn.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `force_handlers`.
- 1: Biết `force_handlers` ép chạy handler nhưng không giải thích được trường hợp Task sau bị lỗi ngắt mid-way.
- 2: Phân tích chính xác cơ chế cứu Handler khi Playbook bị gián đoạn giữa chừng.
- 3: Nêu đúng + viết đoạn cấu hình `force_handlers = True` trong `ansible.cfg`.
**Câu hỏi đào sâu:** Có thể khai báo `force_handlers` ở những vị trí nào? *(Khai báo ở cấp Playbook `force_handlers: true` hoặc trong `ansible.cfg` `force_handlers = True`.)*

---

### Câu 4 — Cơ chế Tự động Thử lại Retry với `until` 🔥
**Hỏi:** Trình bày 3 thuộc tính kết hợp để xây dựng cơ chế tự động thử lại (Retry Mechanism) cho một Task bị lỗi kết nối mạng chập chờn. *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
3 thuộc tính kết hợp:
1. `until:` Điều kiện dừng vòng lặp (ví dụ `until: result.rc == 0` hoặc `until: result is succeeded`).
2. `retries:` Số lần thử lại tối đa (ví dụ `retries: 5`).
3. `delay:` Khoảng thời gian tạm dừng giữa các lần thử tính bằng giây (ví dụ `delay: 2`).
**Tiêu chí chấm:**
- 0: Không biết cơ chế Retry trong Ansible.
- 1: Biết `until` nhưng không nêu đủ 3 thuộc tính `until`, `retries`, và `delay`.
- 2: Phân tích chính xác vai trò của 3 thuộc tính trong cơ chế tự phục hồi Self-Healing khi đứt mạng.
- 3: Nêu đúng + viết đoạn Task YAML hoàn chỉnh sử dụng `until`, `retries: 5`, và `delay: 2`.
**Câu hỏi đào sâu:** Mặc định nếu không khai báo `retries` và `delay` thì Ansible gán giá trị mặc định là bao nhiêu? *(Mặc định `retries = 30` và `delay = 1`.)*

---

### Câu 5 — Khối Cứu hộ Giao dịch `block - rescue - always` 🔥
**Hỏi:** Trình bày ý nghĩa và luồng thi hành của 3 khối `block`, `rescue`, và `always` trong Ansible Playbook. *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- `block:` Nơi chứa các Task thi hành giao dịch chính (Main Transaction).
- `rescue:` Nơi chứa các Task cứu hộ/Rollback. Khối `rescue` CHỈ THỰC THI khi có ít nhất 1 Task trong khối `block` bị lỗi.
- `always:` Nơi chứa các Task dọn dẹp tài nguyên. Khối `always` LUÔN LUÔN THỰC THI dù khối `block` thành công hay thất bại.
**Tiêu chí chấm:**
- 0: Không biết cấu trúc `block - rescue - always`.
- 1: Biết 3 khối nhưng nhầm lẫn điều kiện kích hoạt của khối `rescue` và `always`.
- 2: Phân tích chính xác luồng thi hành giao dịch và quy trình Rollback khôi phục an toàn.
- 3: Nêu đúng + viết đoạn Playbook YAML sử dụng cả 3 khối `block`, `rescue`, và `always`.
**Câu hỏi đào sâu:** Khối `rescue` có thể chứa các task khôi phục file cấu hình cũ (Rollback) không? *(Có, đó chính là công dụng hàng đầu của khối `rescue`.)*

---

### Câu 6 — Ngưỡng Lỗi Tối đa với `max_fail_percentage`
**Hỏi:** Thuộc tính `max_fail_percentage: 20` có ý nghĩa gì khi triển khai Playbook trên cụm 50 máy chủ? *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Ý nghĩa: Quy định ngưỡng tỷ lệ phần trăm số máy chủ bị lỗi tối đa cho phép trong một cụm trước khi Ansible quyết định hủy toàn bộ Playbook.
- Áp dụng trên cụm 50 máy: 20% của 50 máy = 10 máy. Nếu trong quá trình thi hành có tới 11 máy bị lỗi (22% > 20%), Ansible sẽ dừng ngay Playbook. Nếu chỉ có 3 máy bị lỗi (6% < 20%), Ansible vẫn coi là trong ngưỡng cho phép và tiếp tục thực thi các máy còn lại.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `max_fail_percentage`.
- 1: Biết tỷ lệ lỗi nhưng không tính toán được con số cụ thể trên ví dụ 50 máy.
- 2: Phân tích chính xác cơ chế tính ngưỡng phần trăm lỗi cho phép cho cụm máy chủ lớn.
- 3: Nêu đúng + viết đoạn Playbook YAML khai báo `max_fail_percentage: 20`.
**Câu hỏi đào sâu:** Sự khác nhau giữa `any_errors_fatal: true` và `max_fail_percentage: 10` là gì? *(`any_errors_fatal` tương đương `max_fail_percentage: 0` - ngắt ngay lập tức khi có 1 host lỗi.)*

---

### Câu 7 — Tự định nghĩa Điều kiện Lỗi với `failed_when`
**Hỏi:** Trình bày tác dụng của từ khóa `failed_when:`. Làm thế nào để chỉ đạo Ansible coi một Task là THÀNH CÔNG ngay cả khi lệnh trả về mã lỗi `rc != 0`? *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
- Tác dụng: Cho phép kỹ sư tự định nghĩa logic điều kiện khi nào một Task bị coi là lỗi (đè lên logic mặc định `rc != 0`).
- Cách chỉ đạo thành công khi `rc != 0`: Khai báo `failed_when: false` hoặc kiểm tra chuỗi output:
  ```yaml
  - name: Run command that returns non-zero code safely
    ansible.builtin.command: /usr/local/bin/check-user.sh
    register: user_check
    failed_when:
      - user_check.rc != 0
      - "'NOT_FOUND' not in user_check.stdout"
  ```
**Tiêu chí chấm:**
- 0: Không biết từ khóa `failed_when`.
- 1: Biết `failed_when` để kiểm tra lỗi nhưng không nêu được kỹ thuật `failed_when: false`.
- 2: Phân tích chính xác cơ chế ghi đè logic đánh giá lỗi của `failed_when`.
- 3: Nêu đúng + viết đoạn Task YAML kết hợp `register` và `failed_when`.
**Câu hỏi đào sâu:** Thuộc tính `failed_when:` được đánh giá trước hay sau khi Task thi hành xong? *(Được đánh giá sau khi Task thi hành xong và đã bắt được kết quả `register`.)*

---

### Câu 8 — Tự định nghĩa Điều kiện Thay đổi với `changed_when`
**Hỏi:** Thuộc tính `changed_when: false` giải quyết vấn đề gì khi thực thi các Task kiểm tra (như `command: cat` hoặc `command: sestatus`)? Tại sao nó lại bảo vệ tính Idempotency? *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
- Vấn đề giải quyết: Mặc định module `command` hoặc `shell` luôn luôn trả về `changed=1` ở mọi lần chạy vì Ansible không biết lệnh đó có làm sửa đổi đĩa hay không.
- Tác dụng: `changed_when: false` ép buộc Ansible đánh giá Task đó là `ok` (`changed=0`), vì task đó chỉ đọc dữ liệu chứ không làm sửa đổi đĩa.
- Bảo vệ Idempotency: Giúp bảng `PLAY RECAP` ở Lần chạy thứ 2 đạt chuẩn `changed=0` tuyệt đối.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `changed_when`.
- 1: Biết `changed_when: false` để không hiện changed nhưng không giải thích được vai trò bảo vệ Idempotency.
- 2: Phân tích chính xác cơ chế triệt tiêu `changed=1` mạo danh của các task đọc dữ liệu.
- 3: Nêu đúng + viết đoạn Task YAML `command: cat /etc/app.conf` sử dụng `changed_when: false`.
**Câu hỏi đào sâu:** Có thể dùng biểu thức logic trong `changed_when:` không? *(Có thể, ví dụ `changed_when: "'UPDATED' in result.stdout"`.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Xử lý Lỗi 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook áp dụng xử lý lỗi nâng cao (`any_errors_fatal`, `force_handlers`, `until` retry, `block-rescue`) để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective RHCE EX294 #10).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-error-handling.yml`: Cơ chế Retry tự động tự phục hồi lỗi mạng, khối `block` thi hành nạp cấu hình, Handler được gọi và thi hành báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-error-handling.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/error-handling-app.conf` kiểm tra file cấu hình thực sự tồn tại đúng dữ liệu `ERROR_HANDLING=ADVANCED`, và `docker exec target1 cat /etc/audit-handler.log` kiểm tra Handler đã thi hành.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file/handler thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file/handler render.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE EX294 #10 (`☑`).
**Câu hỏi đào sâu:** Ở Lần 2, các task Retry `until:` có bị chạy lại đủ 5 lần không nếu điều kiện đã thành công ngay ở lần 1? *(Không, ở Lần 2 task Retry chạy 1 lần thấy thành công ngay là dừng và báo `ok`.)*

---

### Câu 10 — Xử lý Lỗi Kết nối SSH với `ignore_unreachable` ★★★
**Hỏi:** Thuộc tính `ignore_unreachable: true` có tác dụng gì? Khi nào nên áp dụng `ignore_unreachable: true` thay vì để Playbook bị dừng?
**Đáp án chuẩn:**
- Tác dụng: Cho phép Ansible bỏ qua lỗi ngắt kết nối SSH (Unreachable Host) và tiếp tục thi hành các host còn lại trong inventory.
- Khi áp dụng: Trong kịch bản kiểm tra sức khỏe danh sách 1000 máy chủ (Healthcheck Audit): nếu có 5 máy chủ bị tắt nguồn (unreachable SSH), Ansible sẽ đánh dấu 5 máy đó là unreachable, bỏ qua và tiếp tục quét 995 máy chủ còn lại để thu thập báo cáo audit toàn cục.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `ignore_unreachable`.
- 1: Biết bỏ qua lỗi SSH nhưng không nêu được bài toán quét audit healthcheck hạ tầng lớn.
- 2: Phân tích chính xác vai trò bỏ qua lỗi SSH unreachable trong các task thu thập thông tin.
- 3: Nêu đúng + viết đoạn Task YAML khai báo `ignore_unreachable: true`.
**Câu hỏi đào sâu:** Nếu một host bị unreachable ở Task 1 và có `ignore_unreachable: true`, host đó có được chạy tiếp Task 2 không? *(Không, host đó bị bỏ qua các task phía sau của chính nó, nhưng không làm ảnh hưởng đến các host khác.)*

---

### Câu 11 — Quản lý Handler khi Bị Lỗi với `meta: flush_handlers` ★★★
**Hỏi:** Lệnh `ansible.builtin.meta: flush_handlers` có tác dụng gì? Tại sao nên gọi `flush_handlers` trước một Task quan trọng?
**Đáp án chuẩn:**
- Tác dụng: Ép buộc Ansible phải thi hành NGAY LẬP TỨC toàn bộ các Handler đang nằm trong hàng chờ (notify queue) tại chính thời điểm đó, thay vì chờ đến cuối Playbook mới chạy.
- Lý do sử dụng: Khi Task 1 sửa file cấu hình Nginx và notify `Restart Nginx`, Task 2 phía sau là một bài test HTTP request tới Nginx. Nếu không gọi `flush_handlers`, Nginx chưa được restart nên Task 2 test HTTP sẽ bị fail. Lệnh `meta: flush_handlers` giúp Nginx restart ngay lập tức trước khi Task 2 thi hành.
**Tiêu chí chấm:**
- 0: Không biết lệnh `meta: flush_handlers`.
- 1: Biết xả handler nhưng không giải thích được bài toán phụ thuộc thời điểm thi hành của task test phía sau.
- 2: Phân tích chính xác cơ chế ép buộc thi hành Handler tức thì của `flush_handlers`.
- 3: Nêu đúng + viết đoạn Task YAML gọi `ansible.builtin.meta: flush_handlers`.
**Câu hỏi đào sâu:** Nếu `flush_handlers` bị fail thì các task phía sau xử lý ra sao? *(Playbook sẽ bị dừng ngay tại vị trí `flush_handlers` trừ khi có `force_handlers` hoặc `ignore_errors`.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Advanced Error Handling ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên xây dựng kịch bản Ansible kiên cố, chịu lỗi cao và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Sử dụng `any_errors_fatal: true` cho các cụm máy chủ cốt lõi để bảo vệ tính đồng bộ dữ liệu.
2. **Quy tắc 2:** Khai báo `force_handlers = True` trong `ansible.cfg` để đảm bảo Handler luôn được thực thi an toàn.
3. **Quy tắc 3:** Tự động hóa tự phục hồi lỗi mạng bằng cơ chế Retry `until:`, `retries: 5`, và `delay: 2`.
4. **Quy tắc 4:** Sử dụng mô hình `block - rescue - always` để xây dựng quy trình Rollback khôi phục bản cũ khi có sự cố.
5. **Quy tắc 5:** Dùng `changed_when: false` cho các task kiểm tra và đảm bảo Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy chịu lỗi Fault-Tolerant Enterprise.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp ngăn ngừa nguy cơ dịch vụ bị hỏng state khi kịch bản đứt mid-way? *(Quy tắc 2: `force_handlers = True`.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm xử lý lỗi nâng cao và xây dựng kịch bản Ansible kiên cố chịu lỗi cao, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi thiết kế các kịch bản tự động hóa Ansible có khả năng chịu lỗi cao (Fault-Tolerant) và tự phục hồi (Self-Healing) theo chuẩn Enterprise: áp dụng `any_errors_fatal: true` bảo vệ tính toàn vẹn đồng bộ cho các cụm Cluster cốt lõi, bật `force_handlers = True` trong `ansible.cfg` đảm bảo các dịch vụ luôn được cập nhật cấu hình an toàn ngay cả khi kịch bản bị ngắt giữa chừng. Tôi xây dựng cơ chế tự động thử lại Retry với `until:`, `retries: 5`, `delay: 2` khắc phục 100% sự cố mạng chập chờn, triển khai quy trình Rollback giao dịch với khối `block - rescue - always`, triệt tiêu `changed=1` mạo danh với `changed_when: false`, đảm bảo mọi kịch bản Error Handling đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Nguyễn Văn Y | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Trần Thị Z | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 24

Để chuẩn bị tốt nhất cho **Buổi 24: dynamic-inventory — Dynamic inventory: plugin, constructed, aws_ec2**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Dynamic Inventory là gì? Tại sao trong môi trường Cloud (AWS, Azure, GCP), việc dùng Static Inventory lại trở nên bất khả thi?
2. **Nghiên cứu trước 2:** Sự khác nhau giữa Dynamic Inventory Script (kiểu cũ) và Dynamic Inventory Plugin (kiểu mới đuôi `.aws_ec2.yml`) trong Ansible là gì?
3. **Nghiên cứu trước 3:** Plugin `ansible.builtin.constructed` dùng để tự động tạo các nhóm máy chủ động dựa trên các thông số Tags và Facts như thế nào?

---


### [Chuyên Đề 24] Dynamic Inventory Đa Nền Tảng: Tự Động Khám Phá Máy Chủ Trên AWS EC2, GCP Compute, Azure VM & Kubernetes Pods

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Dynamic Inventory Plugin là gì? Tại sao trong môi trường Đám mây (Cloud Auto-scaling) việc sử dụng Static Inventory lại trở nên bất khả thi? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Dynamic Inventory Plugin: Là cơ chế tự động kết nối API của Cloud Provider (AWS, Azure, GCP) hoặc Facts hệ thống để tự động phát hiện danh sách máy chủ, địa chỉ IP và trạng thái realtime.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Tại sao Static Inventory bất khả thi: Trên môi trường Cloud, các VM/Container liên tục được tạo mới, thay đổi địa chỉ IP hoặc tự động co giãn (Auto-scaling). Việc duy trì tệp <code>inventory.ini</code> tĩnh sửa tay thủ công sẽ gây tốn thời gian, chậm trễ và nguy cơ cao bỏ sót máy chủ chưa được cấu hình.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết Dynamic Inventory Plugin.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết Dynamic Inventory để phát hiện IP nhưng không giải thích được lý do Static Inventory bị phá phá vỡ trên môi trường Cloud Auto-scaling.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác cơ chế tự động kết nối API Cloud để phát hiện danh sách máy chủ realtime.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ tệp Dynamic Inventory Plugin <code>inventory/02-cloud.aws_ec2.yml</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Phân biệt sự khác nhau giữa Dynamic Inventory Script (kiểu cũ) và Dynamic Inventory Plugin (kiểu mới). *(Script cũ dùng file thực thi Python/Bash trả về JSON; Plugin mới dùng tệp cấu hình YAML tích hợp sẵn trong Ansible Core/Collections với khả năng caching và keyed_groups.)*
</div>
</details>

---

### Câu 2 — Cấu trúc Tệp kiểm kê động và Thuộc tính `plugin:` 🔥
**Hỏi:** Thuộc tính `plugin:` ở dòng đầu tiên của tệp YAML kiểm kê động có tác dụng gì? Nêu 2 quy tắc bắt buộc về đặt tên tệp kiểm kê động. *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- Tác dụng: Dùng để chỉ đạo cho Ansible Engine biết cần gọi Plugin FQCN cụ thể nào (như `plugin: amazon.aws.aws_ec2` hoặc `plugin: ansible.builtin.constructed`) để xử lý tệp kiểm kê đó.
- 2 Quy tắc đặt tên tệp:
  1. Tệp bắt buộc phải kết thúc bằng extension chuẩn: `.aws_ec2.yml`, `.yaml`, hoặc `.yml` (KHÔNG dùng `.ini` hoặc `.txt`).
  2. Nếu có nhiều tệp kiểm kê trong cùng thư mục, đặt tên theo thứ tự chữ cái (ví dụ `01-static.ini` nạp trước, `02-constructed.yaml` nạp sau).
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `plugin:`.
- 1: Biết `plugin:` nhưng không nêu được 2 quy tắc bắt buộc về extension và thứ tự nạp file.
- 2: Phân tích chính xác vai trò chỉ định FQCN của `plugin:` và quy tắc đặt tên tệp.
- 3: Nêu đúng + dán đoạn YAML minh họa 2 dòng đầu tiên của tệp kiểm kê động.
**Câu hỏi đào sâu:** Điều gì xảy ra nếu quên thuộc tính `plugin:` ở dòng đầu file YAML? *(Ansible không biết dùng plugin nào để parse và báo lỗi `auto plugin failed to parse`.)*

---

### Câu 3 — Gom nhóm Tự động theo Tags với `keyed_groups` 🔥
**Hỏi:** Trình bày tác dụng của thuộc tính `keyed_groups` trong Dynamic Inventory Plugin. Viết đoạn YAML tự động gom nhóm máy chủ theo nhãn `Environment` và `Role`. *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Tác dụng: `keyed_groups` tự động tạo các nhóm máy chủ động dựa trên giá trị của các nhãn Tags (như `Environment`, `Role`, `Owner`) do Cloud Provider hoặc Facts cung cấp.
- Đoạn YAML mẫu:
  ```yaml
  keyed_groups:
    - key: tags.Environment
      prefix: env
    - key: tags.Role
      prefix: role
  ```
  Nếu máy chủ có tag `Environment: production`, nó sẽ tự động được xếp vào nhóm `env_production`.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `keyed_groups`.
- 1: Biết gom nhóm theo tag nhưng không viết được cú pháp `key` và `prefix`.
- 2: Phân tích chính xác cơ chế tự động tạo tên nhóm bằng tiền tố `prefix` và nhãn `key`.
- 3: Nêu đúng + viết đoạn YAML minh họa hoàn chỉnh 4 dòng `keyed_groups`.
**Câu hỏi đào sâu:** Tiền tố `prefix:` trong `keyed_groups` có tác dụng gì? *(Dùng để đặt tên tiền tố cho nhóm động sinh ra, giúp tên nhóm sạch sẽ dễ đọc như `env_prod` thay vì `tag_Environment_prod`.)*

---

### Câu 4 — Gom nhóm theo Facts với `ansible.builtin.constructed` 🔥
**Hỏi:** Plugin `ansible.builtin.constructed` dùng để làm gì? Nêu ví dụ ứng dụng `constructed` plugin để gom nhóm máy chủ theo hệ điều hành (`ansible_distribution`). *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- Tác dụng: Plugin `constructed` cho phép "xây dựng" các nhóm máy chủ động mới dựa trên các biến Facts (như `ansible_distribution`, `ansible_memtotal_mb`) hoặc các biến sẵn có từ tệp kiểm kê gốc.
- Ví dụ YAML gom nhóm theo hệ điều hành:
  ```yaml
  plugin: ansible.builtin.constructed
  strict: false
  keyed_groups:
    - key: ansible_distribution
      prefix: os
  ```
  Sẽ tự động tạo ra các nhóm như `os_RedHat`, `os_Ubuntu`, `os_CentOS`.
**Tiêu chí chấm:**
- 0: Không biết Plugin `constructed`.
- 1: Biết `constructed` nhưng không giải thích được cơ chế dùng Facts để tạo nhóm động.
- 2: Phân tích chính xác vai trò gom nhóm nâng cao dựa trên Facts của `constructed` plugin.
- 3: Nêu đúng + viết đoạn YAML tệp `02-constructed.yaml` hoàn chỉnh.
**Câu hỏi đào sâu:** Thuộc tính `strict: false` trong `constructed` plugin có ý nghĩa gì? *(Nó ngăn Ansible quăng lỗi crash chương trình khi một máy chủ bị thiếu biến được truy vấn trong `key`.)*

---

### Câu 5 — Bật Cache Inventory trong `ansible.cfg` 🔥
**Hỏi:** Tại sao việc bật Cache Inventory (`cache = True`) lại là yêu cầu bắt buộc khi làm việc với hạ tầng Cloud lớn? Khai báo Cache trong `ansible.cfg` ra sao? *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Tầm quan trọng: Mỗi lần chạy `ansible-playbook`, Dynamic Inventory Plugin phải thực hiện hàng chục cuộc gọi API qua Internet tới Cloud Provider. Khi cụm có 5000 máy chủ, việc gọi API liên tục gây trễ hàng chục giây và dễ bị Cloud API từ chối do vượt giới hạn Rate Limit. Bật Cache giúp lưu kết quả danh sách máy chủ cục bộ trong tệp JSONFile trên Control Node.
- Cấu hình `ansible.cfg`:
  ```ini
  [inventory]
  cache = True
  cache_plugin = jsonfile
  cache_connection = /tmp/ansible_inventory_cache
  cache_timeout = 3600
  ```
**Tiêu chí chấm:**
- 0: Không biết cơ chế Cache Inventory.
- 1: Biết bật Cache cho nhanh nhưng không giải thích được bài toán tránh Cloud API Rate Limit.
- 2: Phân tích chính xác cơ chế lưu bộ nhớ đệm JSONFile và thời hạn `cache_timeout`.
- 3: Nêu đúng + viết đoạn cấu hình `[inventory]` chứa 4 dòng cache trong `ansible.cfg`.
**Câu hỏi đào sâu:** Làm thế nào để xóa bộ nhớ đệm cache và ép Ansible truy vấn lại Cloud API tươi mới? *(Xóa tệp cache trong `/tmp/ansible_inventory_cache` hoặc chạy `ansible-inventory --flush-cache`.)*

---

### Câu 6 — Tra cứu Đồ thị với `ansible-inventory --graph`
**Hỏi:** Lệnh CLI `ansible-inventory -i inventory/ --graph` và `--host target1` có tác dụng gì trước khi thi hành Playbook? *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
- Tác dụng cờ `--graph`: In ra màn hình đồ thị dạng cây trực quan hiển thị toàn bộ các nhóm động vừa được sinh ra (như `dynamic_web_nodes`, `role_web_app`, `env_production`) và danh sách máy chủ thuộc từng nhóm.
- Tác dụng cờ `--host target1`: In ra toàn bộ ma trận biến (variables matrix) được nạp cho máy chủ `target1` (bao gồm các biến `compose`, facts, group_vars).
- Mục đích: Giúp kỹ sư đối soát minh bạch 100% trước khi chạy Playbook Production, ngăn ngừa đánh nhầm nhóm máy.
**Tiêu chí chấm:**
- 0: Không biết lệnh `ansible-inventory`.
- 1: Biết `--graph` để xem cây nhưng không nêu được tác dụng đối soát ma trận biến của `--host`.
- 2: Phân tích chính xác vai trò đối soát an toàn minh bạch trước khi deploy.
- 3: Nêu đúng + minh họa câu lệnh CLI và kết quả cây đồ thị trên terminal.
**Câu hỏi đào sâu:** Cờ `--list` trong `ansible-inventory` xuất ra định dạng dữ liệu nào? *(Xuất ra định dạng chuỗi JSON toàn bộ inventory.)*

---

### Câu 7 — Đổi tên Hostname và Biến Động với `compose:`
**Hỏi:** Thuộc tính `compose:` trong Dynamic Inventory Plugin dùng để làm gì? Viết ví dụ gán `ansible_host` bằng địa chỉ `public_ip_address`. *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- Tác dụng: `compose:` cho phép tự động tính toán hoặc gán lại các biến động bằng biểu thức Jinja2 từ dữ liệu trả về của Cloud API.
- Ví dụ YAML gán IP public:
  ```yaml
  compose:
    ansible_host: public_ip_address
    node_fqdn: inventory_hostname + '.company.local'
  ```
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `compose:`.
- 1: Biết `compose` để gán biến nhưng không viết được cú pháp biểu thức Jinja2.
- 2: Phân tích chính xác cơ chế tính toán biến động từ dữ liệu API của `compose:`.
- 3: Nêu đúng + viết đoạn YAML minh họa gán `ansible_host` và `node_fqdn`.
**Câu hỏi đào sâu:** Thuộc tính `groups:` khác `keyed_groups:` ở điểm nào? *(`groups:` tạo nhóm điều kiện thủ công bằng biểu thức Jinja2; `keyed_groups:` tự động tạo nhóm hàng loạt theo tiền tố giá trị của nhãn Tag.)*

---

### Câu 8 — Đăng ký Plugin An toàn với `enable_plugins`
**Hỏi:** Thuộc tính `enable_plugins` trong `ansible.cfg` đóng vai trò bảo mật gì? Khai báo thuộc tính này ra sao? *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
- Vai trò bảo mật: Là lá chắn an toàn ngăn chặn việc vô tình thi hành các script/plugin kiểm kê độc hại không rõ nguồn gốc nằm trong thư mục inventory. Bắt buộc phải khai báo tên Plugin hợp lệ mới được Ansible cấp phép nạp.
- Cấu hình `ansible.cfg`:
  ```ini
  [inventory]
  enable_plugins = host_list, script, auto, yaml, ini, constructed, amazon.aws.aws_ec2
  ```
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `enable_plugins`.
- 1: Biết `enable_plugins` để bật plugin nhưng không nêu được vai trò bảo mật whitelist plugin.
- 2: Phân tích chính xác cơ chế whitelist cấp phép nạp plugin an toàn của `enable_plugins`.
- 3: Nêu đúng + viết đoạn cấu hình `[inventory]` chứa `enable_plugins` trong `ansible.cfg`.
**Câu hỏi đào sâu:** Nếu nạp plugin `constructed` mà trong `enable_plugins` quên ghi `constructed` thì bị lỗi gì? *(Ansible báo lỗi `constructed plugin not enabled` và từ chối nạp file.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Dynamic Inventory 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook thi hành trên danh sách máy chủ được phát hiện từ Dynamic Inventory Plugin để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective RHCE EX294 #4).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook -i inventory/ site-dynamic-inventory.yml`: Dynamic Inventory Plugin phát hiện máy chủ động và gom nhóm `dynamic_web_nodes`, Playbook nạp cấu hình thực thi báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook -i inventory/ site-dynamic-inventory.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/dynamic-discovery.conf` kiểm tra file cấu hình thực sự tồn tại đúng dữ liệu `DYNAMIC_DISCOVERY=ACTIVE` và `FULL_FQDN=target1.company.local`.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file render.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE EX294 #4 (`☑`).
**Câu hỏi đào sâu:** Lệnh `ansible-inventory -i inventory/ --graph` ở Lần 2 có thay đổi không nếu hạ tầng tĩnh? *(Hoàn toàn giữ nguyên 100%, đồ thị nhóm giữ tính nhất quán Idempotent.)*

---

### Câu 10 — Tự động Gom nhóm Theo Môi trường và Vùng Cloud ★★★
**Hỏi:** Viết đoạn tệp YAML Dynamic Inventory Plugin `inventory/02-cloud.aws_ec2.yml` hoàn chỉnh gom nhóm tự động theo AWS Region và Tag `Environment`.
**Đáp án chuẩn:**
```yaml
plugin: amazon.aws.aws_ec2
regions:
  - ap-southeast-1
  - us-east-1
filters:
  instance-state-name: running
keyed_groups:
  - key: placement.region
    prefix: aws_region
  - key: tags.Environment
    prefix: env
compose:
  ansible_host: public_ip_address
```
**Tiêu chí chấm:**
- 0: Không viết được tệp cấu hình AWS EC2 Plugin.
- 1: Viết được tệp nhưng thiếu `plugin:` hoặc `keyed_groups`.
- 2: Phân tích chính xác các thuộc tính `regions`, `filters`, `keyed_groups` và `compose`.
- 3: Nêu đúng + viết đoạn YAML hoàn chỉnh chuẩn FQCN `amazon.aws.aws_ec2`.
**Câu hỏi đào sâu:** Thuộc tính `filters:` trong AWS EC2 Inventory Plugin có tác dụng gì? *(Dùng để lọc chỉ lấy các instance đang ở trạng thái `running`, bỏ qua các instance đã bị `terminated` hoặc `stopped`.)*

---

### Câu 11 — Quản lý Inventory Phân tầng Thứ tự Nạp File ★★★
**Hỏi:** Khi chỉ định cờ `-i inventory/` trỏ tới một thư mục chứa cả file tĩnh `01-static.ini` và file động `02-constructed.yaml`, Ansible sắp xếp thứ tự nạp các tệp kiểm kê như thế nào?
**Đáp án chuẩn:**
Ansible sắp xếp thứ tự nạp các tệp trong thư mục inventory **theo thứ tự bảng chữ cái (Alphabetical Order)**:
1. Nạp tệp `01-static.ini` trước để xây dựng danh sách hosts và vars cơ bản.
2. Nạp tệp `02-constructed.yaml` sau để đọc các hosts/vars từ `01-static.ini` rồi "xây dựng" (construct) ra các nhóm mới.
Đó là lý do tại sao quy ước luôn đặt tên tệp kiểm kê tĩnh bắt đầu bằng `01-` và tệp `constructed` bắt đầu bằng `02-`.
**Tiêu chí chấm:**
- 0: Không biết quy luật nạp file theo thứ tự bảng chữ cái.
- 1: Biết nạp file tĩnh trước nhưng không giải thích được lý do quy ước đặt tên `01-` và `02-`.
- 2: Phân tích chính xác cơ chế nạp Alphabetical Order và sự phụ thuộc dữ liệu của `constructed` plugin.
- 3: Nêu đúng + thể hiện tư duy tổ chức kiến trúc inventory chuyên nghiệp.
**Câu hỏi đào sâu:** Nếu đặt tên file `constructed.yaml` (bắt đầu bằng c) và `static.ini` (bắt đầu bằng s) thì thứ tự nạp ra sao? *(File `constructed.yaml` sẽ bị nạp trước `static.ini`, dẫn đến `constructed` không tìm thấy host để gom nhóm và tạo ra nhóm rỗng.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Dynamic Inventory ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên làm chủ Dynamic Inventory Plugin, tự động hóa hạ tầng Cloud và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Khai thác Dynamic Inventory Plugin (`.aws_ec2.yml` / `constructed`) thay thế hoàn toàn việc sửa file tĩnh thủ công.
2. **Quy tắc 2:** Luôn khai báo `plugin:` ở dòng đầu file YAML và đặt tên tệp theo thứ tự bảng chữ cái (`01-static.ini`, `02-constructed.yaml`).
3. **Quy tắc 3:** Phân nhóm máy chủ tự động bằng `keyed_groups` dựa trên Tags và Facts hệ thống.
4. **Quy tắc 4:** Bật Cache Inventory (`cache = True`) trong `ansible.cfg` để tăng tốc độ và tránh bị Cloud API rate limit.
5. **Quy tắc 5:** Khai báo `enable_plugins` an toàn, kiểm tra đồ thị bằng `ansible-inventory --graph` và đảm bảo Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy tự động hóa Đám mây cấp Enterprise.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp loại bỏ rủi ro do con người thao tác sai địa chỉ IP trên Cloud? *(Quy tắc 1: Tự động hóa phát hiện IP qua Dynamic Inventory Plugin.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm quản lý hạ tầng Cloud và làm chủ Dynamic Inventory với Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi tự động hóa 100% việc phát hiện và quản lý hạ tầng Đám mây biến động quy mô lớn bằng Dynamic Inventory Plugin (`amazon.aws.aws_ec2`, `azure.azcollection`, `ansible.builtin.constructed`): loại bỏ hoàn toàn việc chỉnh sửa tệp kiểm kê tĩnh thủ công, tự động gom nhóm máy chủ theo Tags và Facts bằng `keyed_groups` và `compose`, bật cơ chế Cache Inventory JSONFile trong `ansible.cfg` triệt tiêu chi phí gọi Cloud API qua Internet. Tôi quản lý phân tầng inventory theo thứ tự bảng chữ cái nghiêm ngặt, khai báo `enable_plugins` bảo mật, đối soát minh bạch đồ thị cây bằng `ansible-inventory --graph`, đảm bảo mọi kịch bản Dynamic Inventory đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Đỗ Văn A | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Hoàng Thị B | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 25

Để chuẩn bị tốt nhất cho **Buổi 25: testing-lint-molecule — Testing: ansible-lint, molecule, check mode**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Công cụ `ansible-lint` là gì? Tại sao việc kiểm tra linter trước khi push code lên Git lại giúp ngăn ngừa 90% lỗi cú pháp và Security Smells?
2. **Nghiên cứu trước 2:** Cờ `--check` (Check Mode) và `--diff` trong câu lệnh `ansible-playbook` có tác dụng gì trong việc thử nghiệm thay đổi (Dry-run execution)?
3. **Nghiên cứu trước 3:** Framework `Molecule` dùng để tự động hóa việc kiểm thử Role (Testing Roles) trên các container Docker cách ly ra sao?

---


### [Chuyên Đề 25] Kiểm Thử Tự Động Playbooks & Roles: Ansible-Lint, Syntax Check, Molecule Testing Framework & Docker Scenario Test

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Cờ <code>--syntax-check</code> trong câu lệnh <code>ansible-playbook</code> dùng để làm gì? Tại sao việc chạy <code>--syntax-check</code> lại là bước đầu tiên trong quy trình CI/CD? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Tác dụng: Dùng để kiểm tra cú pháp tĩnh (Static Syntax Check) của tệp Playbook mà không thực hiện kết nối SSH tới các máy chủ Managed Nodes.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Tại sao là bước đầu tiên trong CI/CD: Giúp phát hiện ngay lập tức các lỗi cú pháp cơ bản (như sai khoảng trắng indent YAML, thiếu dấu hai chấm, thiếu từ khóa <code>hosts:</code>) chỉ trong 1 giây. Chặn không cho các commit lỗi cú pháp đi tiếp vào các bước build tốn nhiều tài nguyên hơn.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết cờ <code>--syntax-check</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết <code>--syntax-check</code> để soi lỗi nhưng không giải thích được lý do chặn sớm (Fail-Fast) trong pipeline CI/CD.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác cơ chế Static Syntax Check và vai trò Fail-Fast trong CI/CD.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + viết câu lệnh CLI thực thi <code>ansible-playbook --syntax-check site-testing.yml</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Cờ <code>--syntax-check</code> có kiểm tra được biến rỗng hay lỗi SSH connection không? *(Không, nó chỉ kiểm tra cấu trúc cú pháp tĩnh của file YAML.)*
</div>
</details>

---

### Câu 2 — Thử nghiệm Dry-run với `--check` và `--diff` 🔥
**Hỏi:** Trình bày tác dụng của cờ `--check` (Check Mode) và cờ `--diff`. Tại sao quản trị viên bắt buộc phải kết hợp bộ đôi `--check --diff` trước khi triển khai Production? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- `--check` (Check Mode / Dry-run): Mô phỏng quá trình thi hành Playbook mà KHÔNG làm thay đổi bất kỳ trạng thái tệp tin hay dịch vụ nào trên máy đích.
- `--diff`: In ra console sự khác biệt từng dòng (`+` thêm vào, `-` xóa đi) của các tệp tin cấu hình nếu Task được thi hành thật.
- Tại sao bắt buộc kết hợp: Giúp quản trị viên soi trực quan chính xác 100% những dòng mã nào trong file cấu hình Production sẽ bị thay đổi trước khi quyết định thi hành thật, triệt tiêu rủi ro làm hỏng file cấu hình hệ thống.
**Tiêu chí chấm:**
- 0: Không biết cờ `--check` và `--diff`.
- 1: Biết `--check` để chạy thử nhưng không giải thích được tác dụng in dòng khác biệt `+`/`-` của `--diff`.
- 2: Phân tích chính xác cơ chế mô phỏng Dry-run kết hợp xem dòng khác biệt file cấu hình.
- 3: Nêu đúng + viết câu lệnh CLI `ansible-playbook --check --diff site-testing.yml`.
**Câu hỏi đào sâu:** Nếu một Task dùng module `command` thô thì cờ `--check` xử lý ra sao? *(Mặc định module `command` bị skip trong Check Mode trừ khi khai báo `check_mode: false`.)*

---

### Câu 3 — Điều khiển Check Mode với `check_mode: false` 🔥
**Hỏi:** Thuộc tính `check_mode: false` (hoặc `check_mode: no`) trong một Task có tác dụng gì? Khi nào bắt buộc phải dùng `check_mode: false`? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Tác dụng: Ép buộc Task đó LUÔN THỰC THI THẬT trên máy đích ngay cả khi câu lệnh `ansible-playbook` đang được chạy ở chế độ thử nghiệm `--check`.
- Khi bắt buộc phải dùng: Dùng cho các Task đọc dữ liệu kiểm tra (như `command: cat /proc/uptime` hoặc đọc trạng thái service) thu thập thông tin gán vào biến `register`. Nếu bị skip trong Check Mode, các Task phía sau dùng biến đó sẽ bị crash do biến undefined.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `check_mode`.
- 1: Biết `check_mode: false` để chạy thật nhưng không giải thích được lý do tránh lỗi undefined biến `register`.
- 2: Phân tích chính xác cơ chế ép buộc thi hành thật trong Dry-run để thu thập dữ liệu biến `register`.
- 3: Nêu đúng + viết đoạn Task YAML sử dụng `check_mode: false` kết hợp `changed_when: false`.
**Câu hỏi đào sâu:** Ngược lại với `check_mode: false`, thuộc tính `check_mode: true` có tác dụng gì? *(Ép buộc Task đó CHỈ chạy ở chế độ Check Mode ngay cả khi Playbook được thi hành thật.)*

---

### Câu 4 — Phân tích Tĩnh Mã nguồn với `ansible-lint` 🔥
**Hỏi:** Công cụ `ansible-lint` dùng để làm gì? Nêu 3 lỗi vi phạm quy chuẩn (Lint Violations / Security Smells) phổ biến mà `ansible-lint` phát hiện. *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- Tác dụng: `ansible-lint` là công cụ phân tích mã nguồn tĩnh (Static Code Analysis) giúp kiểm tra Playbooks và Roles theo bộ quy chuẩn Best Practices và an toàn thông tin của Red Hat.
- 3 Lỗi phổ biến:
  1. Dùng tên module ngắn thay vì tên FQCN (ví dụ dùng `copy` thay vì `ansible.builtin.copy`).
  2. Quên thuộc tính `changed_when` cho module `command` / `shell`.
  3. Cứng hóa mật khẩu plaintext (Hardcoded Secret) hoặc dùng `mode` dạng số không có ngoặc đơn `'0644'`.
**Tiêu chí chấm:**
- 0: Không biết công cụ `ansible-lint`.
- 1: Biết `ansible-lint` để soi code nhưng không liệt kê được 3 lỗi vi phạm chuẩn FQCN và Security Smells.
- 2: Phân tích chính xác vai trò chuẩn hóa mã nguồn Best Practices của `ansible-lint`.
- 3: Nêu đúng + viết câu lệnh CLI thực thi `ansible-lint site-testing.yml`.
**Câu hỏi đào sâu:** Làm thế nào để chỉ đạo `ansible-lint` bỏ qua 1 dòng vi phạm cụ thể? *(Thêm comment `# noqa <rule_name>` ở cuối dòng code đó.)*

---

### Câu 5 — Khởi tạo Cấu hình Quy tắc với `.ansible-lint` 🔥
**Hỏi:** Tệp cấu hình `.ansible-lint` đặt ở thư mục gốc dự án dùng để làm gì? Trình bày 2 thuộc tính chính `profile` và `skip_list`. *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
- Tác dụng: Dùng để tùy biến bộ quy tắc linter cho toàn bộ dự án Doanh nghiệp.
- 2 Thuộc tính chính:
  + `profile:` Quy định mức độ nghiêm ngặt của linter (ví dụ `profile: production` hoặc `profile: basic`).
  + `skip_list:` Khai báo danh sách các mã quy tắc linter tạm thời được phép bỏ qua (ví dụ `skip_list: [yaml[line-length]]` bỏ qua kiểm tra độ dài dòng).
**Tiêu chí chấm:**
- 0: Không biết tệp cấu hình `.ansible-lint`.
- 1: Biết tệp `.ansible-lint` nhưng không nêu được thuộc tính `profile` và `skip_list`.
- 2: Phân tích chính xác cơ chế quản lý quy tắc linter của tệp `.ansible-lint`.
- 3: Nêu đúng + viết đoạn YAML cấu hình tệp `.ansible-lint` hoàn chỉnh.
**Câu hỏi đào sâu:** Thuộc tính `exclude_paths:` trong `.ansible-lint` dùng để làm gì? *(Dùng để khai báo danh sách các thư mục linter bỏ qua không quét, như `.cache/` hoặc `collections/`.)*

---

### Câu 6 — Kiểm thử Role Cách ly với Framework `Molecule`
**Hỏi:** Framework `Molecule` đóng vai trò gì trong việc kiểm thử Ansible Role? Trình bày quy trình hoạt động của câu lệnh `molecule test`. *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Vai trò: Molecule là tiêu chuẩn công nghiệp giúp tự động hóa việc kiểm thử độc lập cho Ansible Role trên các container Docker cách ly.
- Quy trình `molecule test` (8 bước tự động):
  1. `dependency`: Tải các role/collection phụ thuộc.
  2. `lint`: Chạy `ansible-lint` quét mã nguồn.
  3. `cleanup` / `destroy`: Xóa các container cũ.
  4. `syntax`: Kiểm tra cú pháp static.
  5. `create`: Khởi tạo container Docker thử nghiệm mới.
  6. `converge`: Thi hành Role thật Lần 1 trên container.
  7. `idempotence`: Thi hành Role Lần 2 khẳng định `changed=0`.
  8. `verify` / `destroy`: Chạy test nghiệm thu và xóa container.
**Tiêu chí chấm:**
- 0: Không biết framework `Molecule`.
- 1: Biết `Molecule` để test Role nhưng không nêu được quy trình tự động create -> converge -> idempotence -> verify -> destroy.
- 2: Phân tích chính xác quy trình kiểm thử 8 bước của `molecule test` trên Docker.
- 3: Nêu đúng + viết các câu lệnh CLI `molecule init` và `molecule test`.
**Câu hỏi đào sâu:** Driver mặc định phổ biến nhất được Molecule sử dụng là gì? *(Driver `docker`.)*

---

### Câu 7 — Viết Kịch bản Nghiệm thu với `verify.yml`
**Hỏi:** Tệp `molecule/default/verify.yml` trong Molecule dùng để làm gì? Viết đoạn Task nghiệm thu khẳng định tệp `/etc/app.conf` tồn tại đúng mode `'0644'`. *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
- Tác dụng: Dùng để chứa các bài test nghiệm thu (Verification Tests) tự động khẳng định máy đích đạt 100% đúng trạng thái sau khi Role thi hành xong.
- Đoạn Task nghiệm thu mẫu:
  ```yaml
  - name: Stat app config file
    ansible.builtin.stat:
      path: /etc/app.conf
    register: app_stat

  - name: Assert file exists and mode is 0644
    ansible.builtin.assert:
      that:
        - app_stat.stat.exists
        - app_stat.stat.mode == '0644'
  ```
**Tiêu chí chấm:**
- 0: Không biết tệp `verify.yml`.
- 1: Biết `verify.yml` để test nhưng không viết được đoạn task dùng `stat` và `assert`.
- 2: Phân tích chính xác vai trò nghiệm thu trạng thái hệ thống của `verify.yml`.
- 3: Nêu đúng + viết đoạn YAML tệp `verify.yml` hoàn chỉnh với `ansible.builtin.assert`.
**Câu hỏi đào sâu:** Ngoài module `ansible.builtin.assert`, framework nào khác có thể dùng làm verifier cho Molecule? *(Testinfra - framework kiểm thử bằng Python pytest.)*

---

### Câu 8 — Tích hợp Bộ 3 Kiểm thử Đa tầng
**Hỏi:** Trình bày mô hình tích hợp bộ 3 kiểm thử (`--syntax-check` -> `ansible-lint` -> `molecule test`) trước khi commit mã nguồn lên Git. *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
Mô hình lá chắn kiểm thử 3 lớp (Fail-Fast Architecture):
- **Lớp 1 (`--syntax-check`):** Chặn các lỗi cú pháp YAML ngớ ngẩn ngay lập tức trong 1 giây.
- **Lớp 2 (`ansible-lint`):** Chặn các lỗi vi phạm quy chuẩn Best Practices, FQCN và Security Smells trong 5 giây.
- **Lớp 3 (`molecule test`):** Thi hành thực tế trên container Docker cách ly, khẳng định tính đúng đắn và tính Idempotency `changed=0` trong 30 giây.
**Tiêu chí chấm:**
- 0: Không biết mô hình kiểm thử 3 lớp.
- 1: Biết 3 công cụ nhưng không giải thích được tư duy xếp tầng từ nhẹ tới nặng (Fail-Fast).
- 2: Phân tích chính xác cơ chế lá chắn 3 lớp nâng cao chất lượng mã nguồn IaC.
- 3: Nêu đúng + viết câu lệnh bash one-liner kết hợp cả 3 công cụ bằng toán tử `&&`.
**Câu hỏi đào sâu:** Tại sao nên xếp `syntax-check` trước `ansible-lint` và `molecule test`? *(Vì `syntax-check` chạy nhanh nhất 1s, giúp phát hiện lỗi sai YAML ngay mà không tốn công chạy các linter nặng.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng trong Testing 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook đã qua kiểm thử (`--syntax-check`, `ansible-lint`, `--check --diff`) để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective RHCE Testing & Validation).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-testing.yml`: Playbook đã qua kiểm thử linter chạy mượt mà, Task nạp file cấu hình thực thi báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-testing.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Chạy `ansible-playbook molecule/default/verify.yml` và dùng `docker exec target1 cat /etc/testing-app.conf` kiểm tra file cấu hình tồn tại đúng dữ liệu `SYNTAX_CHECK=PASSED`.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `verify.yml` và `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file/verify render.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE Testing & Validation.
**Câu hỏi đào sâu:** Trong Molecule, bước test nào trực tiếp thực hiện Bước 2 trong quy trình trên? *(Bước `idempotence` trong quy trình `molecule test`.)*

---

### Câu 10 — Kiểm tra Dòng Khác biệt Chi tiết với `--diff` ★★★
**Hỏi:** Khi chạy `ansible-playbook --check --diff site.yml`, terminal hiển thị các ký tự `---`, `+++`, `-`, và `+` có ý nghĩa gì trong việc xem sự thay đổi tệp tin?
**Đáp án chuẩn:**
- `---` (trừ 3 cái): Đường dẫn tệp tin gốc hiện tại trên máy đích (before).
- `+++` (cộng 3 cái): Đường dẫn tệp tin mới sẽ được ghi đè (after).
- `-` (dấu trừ ở đầu dòng): Dòng văn bản sẽ bị XÓA BỎ khỏi file trên máy đích.
- `+` (dấu cộng ở đầu dòng): Dòng văn bản sẽ được THÊM MỚI vào file trên máy đích.
Giúp kỹ sư đối soát từng ký tự thay đổi trước khi deploy.
**Tiêu chí chấm:**
- 0: Không đọc được log `--diff`.
- 1: Biết dấu `+` là thêm nhưng không giải thích được cú pháp diff chuẩn unified diff.
- 2: Phân tích chính xác ý nghĩa 4 ký tự `---`, `+++`, `-`, `+` của `--diff`.
- 3: Nêu đúng + minh họa đoạn log `--diff` mẫu trên terminal console.
**Câu hỏi đào sâu:** Cờ `--diff` có hoạt động khi chạy thi hành thật (không có `--check`) không? *(Có, khi chạy thật cờ `--diff` vẫn in ra dòng khác biệt đã được thay đổi trên đĩa.)*

---

### Câu 11 — Bỏ qua Quy tắc Linter với Inline Rule Ignoring ★★★
**Hỏi:** Khi một câu lệnh `command` thô bắt buộc phải sử dụng và không thể thay bằng module FQCN khác, làm thế nào để viết comment chỉ đạo `ansible-lint` bỏ qua cảnh báo linter tại đúng dòng đó?
**Đáp án chuẩn:**
Thêm comment `# noqa <rule_id>` ngay tại dòng Task đó:
```yaml
- name: Run legacy custom binary script
  ansible.builtin.command: /usr/local/bin/legacy-tool --fix
  changed_when: false
  # noqa command-instead-of-module
```
Từ khóa `# noqa` (No Quality Assurance) chỉ đạo `ansible-lint` bỏ qua cảnh báo rule `command-instead-of-module` cho riêng task đó mà vẫn quét các task khác bình thường.
**Tiêu chí chấm:**
- 0: Không biết từ khóa `# noqa`.
- 1: Biết dùng comment nhưng không nhớ cú pháp `# noqa <rule_name>`.
- 2: Phân tích chính xác cơ chế bỏ qua quy tắc cục bộ của `# noqa`.
- 3: Nêu đúng + viết đoạn Task YAML chứa comment `# noqa` chuẩn xác.
**Câu hỏi đào sâu:** Cụm từ `noqa` là viết tắt của từ gì trong ngôn ngữ lập trình? *(Viết tắt của "No Quality Assurance" hoặc "No QA".)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Testing & Quality Assurance ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên xây dựng quy trình kiểm thử mã nguồn IaC chuyên nghiệp, triệt tiêu 99% lỗi Production và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Chạy `ansible-playbook --syntax-check` ngay lập tức để phát hiện lỗi cú pháp YAML trong 1s.
2. **Quy tắc 2:** Luôn thực thi `ansible-playbook --check --diff` thử nghiệm mô phỏng và đối soát dòng khác biệt file `+`/`-` trước khi deploy.
3. **Quy tắc 3:** Phân tích mã nguồn tĩnh với `ansible-lint` và quản lý quy tắc dự án qua tệp `.ansible-lint`.
4. **Quy tắc 4:** Kiểm thử Role tự động trên container Docker cách ly với `Molecule` và tệp nghiệm thu `verify.yml`.
5. **Quy tắc 5:** Dùng `check_mode: false` cho task đọc dữ liệu và đảm bảo lượt chạy Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy Quản lý Chất lượng Mã nguồn IaC Enterprise.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp ngăn ngừa rủi ro sửa nhầm nội dung file cấu hình trên máy chủ Production? *(Quy tắc 2: Đối soát dòng khác biệt với `--check --diff`.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm kiểm thử kịch bản Ansible và quản lý chất lượng mã nguồn IaC, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi xây dựng quy trình kiểm thử mã nguồn Ansible IaC đa tầng nghiêm ngặt theo chuẩn DevSecOps: áp dụng mô hình lá chắn 4 lớp với `--syntax-check` phát hiện lỗi YAML tĩnh trong 1s, chuẩn hóa 100% Best Practices, FQCN và triệt tiêu Security Smells qua `ansible-lint` và tệp cấu hình `.ansible-lint`, thử nghiệm Dry-run và đối soát dòng khác biệt file `+`/`-` với `--check --diff` trước khi deploy Production. Tôi tự động hóa kiểm thử Role cách ly trên Docker container với `Molecule` framework và nghiệm thu bằng `verify.yml`, điều khiển linh hoạt `check_mode: false` cho các task thu thập dữ liệu, đảm bảo 100% kịch bản đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Bùi Văn C | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Lê Thị D | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 26

Để chuẩn bị tốt nhất cho **Buổi 26: ansible-trong-cicd — Ansible trong CI/CD (GitLab: lint → molecule → deploy)**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Pipeline CI/CD trong Gitlab CI (`.gitlab-ci.yml`) được chia làm các giai đoạn (Stages) như thế nào để tích hợp Ansible tự động?
2. **Nghiên cứu trước 2:** Làm thế nào để truyền mật khẩu Vault giải mã an toàn trong Runner execution của CI/CD mà không bị rò rỉ log console?
3. **Nghiên cứu trước 3:** Kỹ thuật Rolling Deployment kết hợp với cờ `serial:` và Load Balancer unregister/register trong pipeline CI/CD diễn ra ra sao?

---


### [Chuyên Đề 26] Tích Hợp Ansible Trong CI/CD: GitLab CI, GitHub Actions, Jenkins Automation & Quản Lý SSH Private Keys Không Để Lộ

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Trình bày 4 giai đoạn (Stages) tiêu chuẩn trong một pipeline CI/CD tự động hóa Ansible cấp Enterprise. Tại sao việc chia 4 stage này lại là bắt buộc? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 4 Giai đoạn:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <code>lint</code>: Kiểm tra cú pháp tĩnh (<code>--syntax-check</code>) và linter (<code>ansible-lint</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <code>test</code>: Kiểm thử Role trên container Docker cách ly bằng <code>molecule test</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> <code>staging</code>: Triển khai tự động lên môi trường Staging (<code>-i inventory/staging</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">4.</b> <code>production</code>: Triển khai cuốn chiếu Zero Downtime lên Production sau khi có phê duyệt thủ công (<code>when: manual</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Tại sao bắt buộc: Tạo lá chắn kiểm thử Fail-Fast đa tầng, phát hiện lỗi sớm từ bước 1, ngăn ngừa 100% rủi ro lọt code lỗi gây ngưng trệ máy chủ Production.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết cấu trúc pipeline CI/CD.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết các stage nhưng không liệt kê đủ 4 stage <code>lint</code> -> <code>test</code> -> <code>staging</code> -> <code>production</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò lá chắn Fail-Fast đa tầng của 4 stages trong pipeline CI/CD.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + viết đoạn YAML <code>stages:</code> trong tệp <code>.gitlab-ci.yml</code>.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Nếu Stage 1 (<code>lint</code>) bị lỗi, runner sẽ xử lý các Stage tiếp theo như thế nào? *(Runner sẽ ngắt pipeline ngay lập tức, không chạy các Stage <code>test</code>, <code>staging</code>, <code>production</code> phía sau.)*
</div>
</details>

---

### Câu 2 — Bảo mật Secret Variables trong CI/CD Runner 🔥
**Hỏi:** Làm thế nào để nạp mật khẩu Vault và SSH Key an toàn trong CI/CD Runner mà không lưu vết trong kho mã nguồn Git? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
Quy trình SecOps nạp secret trong CI/CD:
1. **Lưu trong CI/CD Secret Manager:** Khai báo biến mật `$ANSIBLE_VAULT_PASSWORD` và `$SSH_PRIVATE_KEY` trong phần Cài đặt CI/CD Settings của GitLab / GitHub (đánh dấu `Protected` và `Masked`).
2. **Nạp trong `before_script`:** Trong tệp `.gitlab-ci.yml`, dùng khối `before_script` để ghi mật khẩu ra tệp tạm `.vault_pass` với quyền `0600`:
   ```yaml
   before_script:
     - echo "$ANSIBLE_VAULT_PASSWORD" > .vault_pass
     - chmod 0600 .vault_pass
   ```
**Tiêu chí chấm:**
- 0: Không biết cách quản lý Secret Variables trong CI/CD.
- 1: Biết dùng biến mật nhưng quên bước `chmod 0600 .vault_pass` trong `before_script`.
- 2: Phân tích chính xác cơ chế tiêm Secret Variable và cấp quyền `0600` cho tệp tạm.
- 3: Nêu đúng + viết đoạn YAML `before_script` hoàn chỉnh.
**Câu hỏi đào sâu:** Tính năng `Mask variable` trong GitLab CI Settings có tác dụng gì? *(Nó tự động che giấu giá trị biến trong màn hình console log của runner, thay giá trị thật bằng `[MASKED]`.)*

---

### Câu 3 — Phân tách Môi trường Staging và Production 🔥
**Hỏi:** Làm thế nào để phân tách biến cấu hình và inventory giữa Staging và Production trong pipeline CI/CD để tránh deploy nhầm? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Tổ chức tệp kiểm kê phân tách: Tạo 2 thư mục riêng `inventory/staging/hosts.ini` và `inventory/production/hosts.ini`.
- Chỉ định cờ `-i` trong job CI/CD:
  ```yaml
  deploy-staging:
    stage: staging
    script:
      - ansible-playbook -i inventory/staging/hosts.ini site-cicd.yml

  deploy-production:
    stage: production
    script:
      - ansible-playbook -i inventory/production/hosts.ini site-cicd.yml
  ```
**Tiêu chí chấm:**
- 0: Không biết phân tách môi trường trong CI/CD.
- 1: Biết chia môi trường nhưng không nêu được kỹ thuật truyền cờ `-i inventory/` phân tách trong từng job.
- 2: Phân tích chính xác vai trò cô lập kiểm kê ngăn ngừa thảm họa deploy nhầm môi trường.
- 3: Nêu đúng + viết đoạn YAML job `deploy-staging` và `deploy-production`.
**Câu hỏi đào sâu:** Có nên dùng chung 1 file `inventory.ini` cho cả Staging và Prod không? *(Tuyệt đối không, vi phạm nguyên tắc cô lập môi trường.)*

---

### Câu 4 — Cổng Phê duyệt Thủ công `when: manual` 🔥
**Hỏi:** Thuộc tính `when: manual` trong tệp `.gitlab-ci.yml` có tác dụng gì? Tại sao job triển khai Production bắt buộc phải có `when: manual`? *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
- Tác dụng: Tạo ra một cổng phê duyệt thủ công (Manual Approval Gate). Job có `when: manual` sẽ tạm dừng và chờ cho đến khi quản trị viên truy cập vào GitLab CI Web UI gạt nút "Play" thủ công mới thi hành.
- Tại sao bắt buộc cho Prod: Để đảm bảo sự hiện diện và kiểm soát có trách nhiệm của con người trước khi thực hiện thay đổi trên máy chủ Production, cho phép Release Manager chủ động chọn thời điểm bảo trì thích hợp (như 2h sáng).
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `when: manual`.
- 1: Biết `when: manual` để bấm nút chạy nhưng không giải thích được vai trò kiểm soát trách nhiệm khi deploy Prod.
- 2: Phân tích chính xác cơ chế cổng phê duyệt thủ công và bài toán chọn thời điểm bảo trì.
- 3: Nêu đúng + viết đoạn YAML job `deploy-production` chứa `when: manual` và `only: [main]`.
**Câu hỏi đào sâu:** Thuộc tính `only: [main]` kết hợp với `when: manual` có ý nghĩa gì? *(Chỉ cho phép bấm nút phê duyệt manual deploy Production khi code nằm trên nhánh chính `main`.)*

---

### Câu 5 — Triển khai Cuốn chiếu Zero Downtime trong CI/CD 🔥
**Hỏi:** Làm thế nào để tự động hóa quy trình triển khai cuốn chiếu Zero Downtime trên Production trong pipeline CI/CD? *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
Kết hợp từ khóa `serial:` ở cấp Playbook (hoặc truyền cờ `--serial 1` khi gọi `ansible-playbook` trong job CI/CD):
```yaml
deploy-production:
  stage: production
  script:
    - ansible-playbook -i inventory/production/hosts.ini --serial 1 site-cicd.yml
```
Runner sẽ chỉ đạo Ansible lấy từng máy chủ ra cập nhật, kiểm tra sức khỏe OK rồi mới làm máy tiếp theo, đảm bảo cụm Production luôn có máy chủ phục vụ người dùng, đạt Zero Downtime.
**Tiêu chí chấm:**
- 0: Không biết kết hợp `serial` trong CI/CD.
- 1: Biết `serial` nhưng không giải thích được cơ chế runner gọi `--serial 1` bảo vệ Zero Downtime.
- 2: Phân tích chính xác cơ chế triển khai cuốn chiếu theo lô trong runner execution.
- 3: Nêu đúng + viết đoạn YAML job CI/CD truyền cờ `--serial 1`.
**Câu hỏi đào sâu:** Nếu đợt nâng cấp host đầu tiên bị lỗi trong `--serial 1`, runner sẽ xử lý ra sao? *(Ansible ngắt job ngay lập tức, báo fail pipeline và giữ an toàn cho các host còn lại.)*

---

### Câu 6 — Dọn dẹp Bí mật Tạm với `after_script`
**Hỏi:** Tại sao việc xóa tệp `.vault_pass` tạm trong khối `after_script` của CI/CD runner lại là quy định an toàn bắt buộc? *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
- Lý do bắt buộc: Trong hạ tầng CI/CD, các Runner thường được dùng chung (Shared Runners) cho nhiều dự án khác nhau. Nếu `before_script` tạo tệp `.vault_pass` trên đĩa cứng của Runner mà quên không xóa trong `after_script`, tệp chứa mật khẩu đó sẽ nằm lại trên đĩa cứng và có thể bị các job của dự án khác đọc lén.
- Khối `after_script`:
  ```yaml
  after_script:
    - rm -f .vault_pass
  ```
  Khối `after_script` LUÔN THỰC THI kể cả khi job thành công hay bị crash do lỗi, đảm bảo xóa sạch dấu vết.
**Tiêu chí chấm:**
- 0: Không biết khối `after_script`.
- 1: Biết xóa file nhưng không giải thích được rủi ro lộ secret trên Shared Runner.
- 2: Phân tích chính xác cơ chế luôn thi hành dọn dẹp vết secret của `after_script`.
- 3: Nêu đúng + viết đoạn YAML `after_script` xóa `.vault_pass` và SSH key.
**Câu hỏi đào sâu:** Nếu job bị fail ở giữa bước `script`, khối `after_script` có được chạy không? *(Có, `after_script` luôn được gọi bất chấp job thành công hay thất bại.)*

---

### Câu 7 — Tự động hóa Stage `lint` trong Runner
**Hỏi:** Trình bày các câu lệnh thi hành ở Stage `lint` trong tệp `.gitlab-ci.yml`. *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
Giai đoạn `lint` thi hành bộ đôi kiểm tra chất lượng mã nguồn:
```yaml
lint-job:
  stage: lint
  script:
    - ansible-playbook --syntax-check site-cicd.yml
    - ansible-lint site-cicd.yml
```
1. `ansible-playbook --syntax-check`: Soi lỗi cú pháp tĩnh YAML trong 1s.
2. `ansible-lint`: Soi lỗi FQCN, Best Practices và Security Smells trong 5s.
**Tiêu chí chấm:**
- 0: Không biết câu lệnh chạy stage `lint`.
- 1: Biết `ansible-lint` nhưng thiếu `--syntax-check`.
- 2: Phân tích chính xác bộ đôi câu lệnh soi code trong stage `lint`.
- 3: Nêu đúng + viết đoạn YAML job `lint-job` hoàn chỉnh.
**Câu hỏi đào sâu:** Nếu `ansible-lint` phát hiện lỗi FQCN thì pipeline xử lý ra sao? *(Job `lint` bị đánh dấu FAILED, pipeline dừng lại không cho deploy.)*

---

### Câu 8 — Tự động hóa Stage `test` với Molecule
**Hỏi:** Làm thế nào để chạy kịch bản Molecule test trên GitLab CI Runner sử dụng Docker-in-Docker (`dind`)? *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
Khai báo service `docker:dind` trong job `test`:
```yaml
molecule-test-job:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_HOST: tcp://docker:2375
  script:
    - molecule test
```
Cho phép runner tự động dựng container Docker cách ly, thi hành Role, test Idempotency và nghiệm thu.
**Tiêu chí chấm:**
- 0: Không biết cách chạy Molecule trong CI/CD.
- 1: Biết `molecule test` nhưng không nêu được service `docker:dind` để kích hoạt Docker-in-Docker.
- 2: Phân tích chính xác cơ chế Docker-in-Docker trong GitLab CI runner để chạy Molecule.
- 3: Nêu đúng + viết đoạn YAML job `molecule-test-job` hoàn chỉnh.
**Câu hỏi đào sâu:** `dind` trong `docker:dind` là viết tắt của từ gì? *(Viết tắt của "Docker-in-Docker".)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng trong CI/CD 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một kịch bản Ansible được thực thi qua pipeline CI/CD để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Giai đoạn 4 & Objective EX294 Enterprise Deployment).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1 qua Pipeline):** Push code kích hoạt pipeline CI/CD: các Stage `lint` -> `test` -> `staging` -> `production` thi hành mượt mà, runner giải mã Vault và deploy mã nguồn lên máy đích báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2 qua Re-run Pipeline):** Thực hiện Re-run lại pipeline CI/CD Lần 2 mà không đổi code: bảng `PLAY RECAP` trong log runner **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/cicd-deployment.conf` kiểm tra file cấu hình thực sự tồn tại đúng dữ liệu `CICD_PIPELINE=SUCCESSFUL` và `DEPLOYED_ENV=production`.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 Re-run pipeline `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát file render trong runner log.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Giai đoạn 4 & Objective RHCE Enterprise Deployment (`☑`).
**Câu hỏi đào sâu:** Nếu Re-run pipeline Lần 2 mà log runner báo `changed=1`, điều đó chứng tỏ điều gì? *(Chứng tỏ kịch bản Ansible bị lỗi Idempotency mạo danh, cần rà soát lại các task trong Playbook.)*

---

### Câu 10 — Tắt Cảnh báo SSH Host Key trong Runner với `ANSIBLE_HOST_KEY_CHECKING` ★★★
**Hỏi:** Tại sao việc khai báo `ANSIBLE_HOST_KEY_CHECKING: "False"` lại là bắt buộc trong môi trường CI/CD Runner?
**Đáp án chuẩn:**
- Lý do: CI/CD Runner là một container/VM tạm thời được tạo mới liên tục. Khi Runner lần đầu thực hiện kết nối SSH tới máy đích, SSH client mặc định sẽ dừng ngắt chương trình và hỏi câu tương tác `Are you sure you want to continue connecting (yes/no)?`. Vì Runner chạy tự động không có con người gõ `yes`, job sẽ bị treo timeout và fail.
- Khai báo `ANSIBLE_HOST_KEY_CHECKING: "False"` trong variables của `.gitlab-ci.yml` chỉ đạo Ansible tự động chấp nhận SSH Host Key mà không bị dừng ngắt.
**Tiêu chí chấm:**
- 0: Không biết biến `ANSIBLE_HOST_KEY_CHECKING`.
- 1: Biết tắt check host key nhưng không giải thích được lý do Runner bị treo câu hỏi `(yes/no)`.
- 2: Phân tích chính xác cơ chế ngăn ngừa SSH prompt timeout trong non-interactive runner.
- 3: Nêu đúng + viết đoạn YAML `variables:` trong `.gitlab-ci.yml`.
**Câu hỏi đào sâu:** Ngoài biến môi trường, có thể tắt host key checking ở đâu nữa? *(Trong file `ansible.cfg` với thuộc tính `host_key_checking = False`.)*

---

### Câu 11 — Tích hợp Slack/Teams Notification Webhook ★★★
**Hỏi:** Làm thế nào để gửi thông báo tự động kết quả triển khai CI/CD (Thành công hay Thất bại) về kênh ChatOps Slack hoặc Microsoft Teams của đội kỹ thuật?
**Đáp án chuẩn:**
Sử dụng module FQCN `community.general.slack` hoặc `ansible.builtin.uri` trong khối `always` hoặc trong `after_script` của CI/CD pipeline:
```yaml
- name: Send Slack Notification on Deployment Finish
  community.general.slack:
    token: "$SLACK_TOKEN"
    channel: "#deploy-alerts"
    msg: "Deployment to {{ target_env }} completed with status: {{ ansible_failed_result | default('SUCCESS') }}"
  delegate_to: localhost
```
Giúp toàn bộ đội ngũ kỹ thuật nắm bắt realtime kết quả triển khai hạ tầng.
**Tiêu chí chấm:**
- 0: Không biết cách tích hợp ChatOps notification.
- 1: Biết gửi Slack nhưng không nêu được module `community.general.slack` hoặc `uri`.
- 2: Phân tích chính xác vai trò ChatOps notification trong quy trình CI/CD Enterprise.
- 3: Nêu đúng + viết đoạn Task YAML gửi Slack notification chuẩn xác.
**Câu hỏi đào sâu:** Thuộc tính `delegate_to: localhost` trong task gửi Slack có tác dụng gì? *(Chỉ đạo task gửi Slack HTTP request được thi hành từ chính Control Node/Runner chứ không phải chạy từ máy đích.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Ansible trong CI/CD Enterprise ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên tích hợp Ansible vào pipeline CI/CD Enterprise chuyên nghiệp, bảo mật 100% secret và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Xây dựng pipeline 4 giai đoạn chuẩn: `lint` -> `test` -> `staging` -> `production` (cổng `when: manual`).
2. **Quy tắc 2:** Nạp mật khẩu Vault và SSH Key qua Secret Variables trong `before_script` với quyền `chmod 0600 .vault_pass`.
3. **Quy tắc 3:** Phân tách hoàn toàn môi trường qua `-i inventory/staging` và `-i inventory/production`.
4. **Quy tắc 4:** Triển khai cuốn chiếu Zero Downtime trên Production với `serial: 1` và xóa tệp mật khẩu tạm trong `after_script`.
5. **Quy tắc 5:** Tắt SSH prompt với `ANSIBLE_HOST_KEY_CHECKING: "False"` và đảm bảo Re-run pipeline Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy Tự động hóa CI/CD Enterprise đỉnh cao.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp đánh dấu việc hoàn thành 100% Giai đoạn 4 của khóa học ntkansible? *(Tất cả 5 quy tắc hợp nhất trong Buổi 26 đánh dấu hoàn thành 100% Giai đoạn 4.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm tích hợp Ansible vào quy trình CI/CD và tự động hóa triển khai hạ tầng Doanh nghiệp, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi thiết kế và vận hành hệ thống tự động hóa triển khai hạ tầng Enterprise tích hợp Ansible vào pipeline CI/CD (GitLab CI / GitHub Actions) theo chuẩn DevSecOps chuyên nghiệp: xây dựng luồng thi hành Fail-Fast 4 giai đoạn `lint` -> `test` -> `staging` -> `production`, quản lý bảo mật Secret Variables tuyệt đối với `before_script` nạp `.vault_pass` quyền `0600` và dọn dẹp sạch trong `after_script`. Tôi phân tách môi trường kiểm kê nghiêm ngặt với `-i inventory/staging` và `-i inventory/production`, thiết lập cổng phê duyệt thủ công `when: manual` cho nhánh `main`, tự động hóa triển khai cuốn chiếu Zero Downtime với `--serial 1`, tắt SSH prompt với `ANSIBLE_HOST_KEY_CHECKING: 'False'`, đảm bảo 100% pipeline Re-run Lần 2 đạt tiêu chuẩn Idempotent `changed=0` và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Ngô Văn E | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Dương Thị F | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 27

Để chuẩn bị tốt nhất cho **Buổi 27: systemd-custom-service — Khởi đầu Giai đoạn 5 (Nâng cao và Capstone): Systemd service tùy chỉnh và quản lý Daemon**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Cấu trúc tệp Unit File của Systemd (gồm các phần `[Unit]`, `[Service]`, `[Install]`) được quản lý bằng Ansible module nào?
2. **Nghiên cứu trước 2:** Lệnh `systemctl daemon-reload` bắt buộc phải chạy khi nào? Module `ansible.builtin.systemd` hỗ trợ cờ `daemon_reload: yes` ra sao?
3. **Nghiên cứu trước 3:** Làm thế nào để tạo một Custom Systemd Service chạy ứng dụng Python/NodeJS ngầm dưới quyền user không phải root?

---


### [Chuyên Đề 27] Quản Lý Systemd Unit & Custom Services: Tạo Daemon, Quản Trị Vòng Đời Tiến Trình & Health Check Tự Phục Hồi

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Trình bày cấu trúc 3 phần bắt buộc trong một tệp Systemd Unit File (<code>.service</code>). Mỗi phần chứa các chỉ thị quan trọng nào? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3 Phần cấu trúc:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <code>[Unit]</code>: Chứa mô tả dịch vụ (<code>Description=</code>) và sự phụ thuộc khởi động (<code>After=network.target</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <code>[Service]</code>: Chứa loại dịch vụ (<code>Type=simple</code>), tài khoản thực thi (<code>User=sysops</code>), lệnh khởi chạy (<code>ExecStart=</code>), và cơ chế tự khôi phục (<code>Restart=always</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> <code>[Install]</code>: Chứa điểm gắn kết khởi động cùng hệ thống khi boot (<code>WantedBy=multi-user.target</code>).</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết cấu trúc Unit File.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết các phần nhưng không giải thích được vai trò chỉ thị <code>WantedBy=</code> hay <code>ExecStart=</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò 3 phần <code>[Unit]</code>, <code>[Service]</code>, <code>[Install]</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + viết đoạn Unit File mẫu <code>my-app.service.j2</code> hoàn chỉnh.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Điều gì xảy ra nếu một tệp <code>.service</code> bị thiếu phần <code>[Install]</code>? *(Lệnh <code>systemctl enable</code> sẽ báo lỗi từ chối tạo symbolic link tự khởi động cùng boot.)*
</div>
</details>

---

### Câu 2 — Vị trí Thư mục Unit File và Deploy với Template 🔥
**Hỏi:** Thư mục nào trên hệ thống Linux được dùng để lưu trữ các Custom Systemd Unit File? Module Ansible nào được dùng để deploy tệp này? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- Thư mục lưu trữ: `/etc/systemd/system/` (đây là thư mục chứa các Custom Unit File do sysadmin định nghĩa, ưu tiên cao hơn thư mục hệ thống `/usr/lib/systemd/system/`).
- Module Ansible dùng deploy: Module `ansible.builtin.template` (kết hợp Jinja2 template để biến đổi động các thông số như `{{ app_dir }}` hay `{{ app_user }}` với mode `'0644'`).
**Tiêu chí chấm:**
- 0: Không nhớ thư mục `/etc/systemd/system/`.
- 1: Biết thư mục nhưng không giải thích được tại sao nên dùng module `template` thay vì `copy` thô.
- 2: Phân tích chính xác vai trò ưu tiên cấu hình của `/etc/systemd/system/` và biến đổi động qua `template`.
- 3: Nêu đúng + viết đoạn Task Ansible `ansible.builtin.template` hoàn chỉnh.
**Câu hỏi đào sâu:** Quyền hạn (permissions) chuẩn của tệp `.service` trong `/etc/systemd/system/` là gì? *(Mode `'0644'` thuộc sở hữu `root:root`.)*

---

### Câu 3 — Kích hoạt `daemon_reload: yes` khi Sửa Unit File 🔥
**Hỏi:** Tại sao việc nạp lại daemon (`daemon_reload: yes`) là bắt buộc mỗi khi tạo mới hoặc sửa đổi tệp `.service`? Khai báo thuộc tính này trong Ansible ra sao? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Tại sao bắt buộc: Systemd Manager lưu vạ bộ nhớ đệm (cache) của các Unit File trên RAM. Khi tệp `.service` bị chỉnh sửa trên đĩa cứng, nếu không kích hoạt `daemon_reload: yes` (`systemctl daemon-reload`), Systemd sẽ cảnh báo `Warning: my-app.service changed on disk` và tiếp tục dùng cấu hình cũ.
- Cấu hình Ansible: Dùng thuộc tính `daemon_reload: true` trong module `ansible.builtin.systemd` (nên đặt trong Handler để chỉ chạy khi file đổi).
**Tiêu chí chấm:**
- 0: Không biết khái niệm `daemon-reload`.
- 1: Biết `daemon-reload` nhưng không giải thích được bộ nhớ đệm trên RAM của Systemd Manager.
- 2: Phân tích chính xác cơ chế nạp lại cấu hình từ đĩa cứng của `daemon_reload: true`.
- 3: Nêu đúng + viết đoạn Handler Ansible sử dụng `daemon_reload: true`.
**Câu hỏi đào sâu:** Nên đặt `daemon_reload: true` trực tiếp trong Task hay trong Handler? *(Nên đặt trong Handler chỉ gọi khi Unit File có sự thay đổi để đảm bảo Idempotency.)*

---

### Câu 4 — Cơ chế Tự Khôi phục Crash với `Restart=always` 🔥
**Hỏi:** Thuộc tính `Restart=always` và `RestartSec=5s` trong phần `[Service]` có tác dụng gì đối với độ sẵn sàng của ứng dụng? *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- Tác dụng `Restart=always`: Tự động khởi động lại tiến trình ứng dụng khi tiến trình bị ngắt ngầm đột ngột do lỗi crash, tràn bộ nhớ (OOM Killer) hoặc bị gửi tín hiệu `SIGKILL`.
- Tác dụng `RestartSec=5s`: Chỉ đạo Systemd tạm dừng 5 giây trước khi thực hiện khởi động lại tiến trình, tránh việc restart quá dồn dập làm ngập tài nguyên CPU/RAM.
- Lợi ích: Đảm bảo tính tự phục hồi (Self-healing) của ứng dụng mà không cần con người can thiệp thủ công.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `Restart=always`.
- 1: Biết `Restart=always` để tự chạy lại nhưng không nêu được khoảng dừng `RestartSec=5s`.
- 2: Phân tích chính xác cơ chế Self-healing tự phục hồi dịch vụ sau crash.
- 3: Nêu đúng + viết đoạn YAML/INI chứa 2 dòng `Restart=always` và `RestartSec=5s`.
**Câu hỏi đào sâu:** Khác biệt giữa `Restart=always` và `Restart=on-failure` là gì? *(`on-failure` chỉ restart khi tiến trình thoát với mã lỗi exit status khác 0; `always` restart trong mọi trường hợp kể cả bị kill.)*

---

### Câu 5 — Hạ đặc quyền Chạy dưới User Non-root 🔥
**Hỏi:** Tại sao việc cấu hình `User=sysops` và `Group=sysops` trong Unit File lại là nguyên tắc an toàn bắt buộc khi chạy các ứng dụng tùy chỉnh? *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Lý do an toàn bắt buộc: Tuân thủ nguyên tắc bảo mật tối thiểu (Principle of Least Privilege). Nếu ứng dụng (Python/NodeJS) bị dính lỗ hổng bảo mật nghiêm trọng (RCE), kẻ tấn công chỉ chiếm được quyền hạn hạn chế của user `sysops`, tuyệt đối không thể can thiệp hay phá hoại toàn bộ hệ điều hành như khi chạy dưới quyền `root`.
- Cách triển khai trong Ansible: Dùng module `ansible.builtin.user` tạo user hệ thống `sysops` (`shell: /sbin/nologin`), sau đó khai báo `User=sysops` trong `[Service]`.
**Tiêu chí chấm:**
- 0: Không biết lý do hạ đặc quyền user non-root.
- 1: Biết tạo user `sysops` nhưng không giải thích được bài toán chặn leo thang đặc quyền khi app bị hack.
- 2: Phân tích chính xác nguyên tắc Least Privilege và cô lập môi trường thực thi ứng dụng.
- 3: Nêu đúng + viết đoạn Task tạo user `sysops` và đoạn INI `User=sysops`.
**Câu hỏi đào sâu:** Tại sao nên đặt `shell: /sbin/nologin` cho tài khoản service user `sysops`? *(Để ngăn không cho ai sử dụng tài khoản `sysops` đăng nhập SSH trực tiếp vào server.)*

---

### Câu 6 — Bật và Khởi chạy Dịch vụ với `ansible.builtin.systemd`
**Hỏi:** Trình bày sự khác nhau giữa thuộc tính `enabled: yes` và `state: started` trong module `ansible.builtin.systemd`. *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
- `enabled: yes`: Chỉ đạo Systemd tạo symbolic link khởi chạy tự động cùng hệ điều hành mỗi khi máy chủ được bật / reboot (tương đương lệnh `systemctl enable`).
- `state: started`: Chỉ đạo Systemd kích hoạt khởi chạy tiến trình ứng dụng ngay tại thời điểm hiện tại (tương đương lệnh `systemctl start`).
- Bắt buộc phải khai báo kết hợp cả hai thuộc tính để vừa đảm bảo app đang chạy ngay, vừa đảm bảo không bị tắt khi máy chủ reboot.
**Tiêu chí chấm:**
- 0: Không phân biệt được `enabled` và `state`.
- 1: Biết `enabled` để tự chạy cùng boot nhưng không giải thích được mối quan hệ với `state: started`.
- 2: Phân tích chính xác sự khác biệt giữa cấu hình boot link và runtime process state.
- 3: Nêu đúng + viết đoạn Task Ansible `ansible.builtin.systemd` kết hợp cả 2 thuộc tính.
**Câu hỏi đào sâu:** Nếu khai báo `enabled: yes` nhưng `state: stopped` thì điều gì xảy ra? *(Dịch vụ hiện tại sẽ bị dừng, nhưng ở lần reboot máy chủ tiếp theo nó sẽ tự động khởi chạy.)*

---

### Câu 7 — Quản lý Nhật ký Tập trung với `journalctl`
**Hỏi:** Làm thế nào để xem nhật ký tập trung của Custom Systemd Service qua công cụ `journalctl`? Nêu 2 cờ lệnh phổ biến. *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- Tác dụng: Mọi luồng in `stdout`/`stderr` của ứng dụng được Systemd tự động thu gom và đánh chỉ mục tập trung trong `systemd-journald`.
- Câu lệnh CLI: `journalctl -u my-app.service`
- 2 Cờ lệnh phổ biến:
  1. `-n 20`: Chỉ hiển thị 20 dòng nhật ký mới nhất.
  2. `-f` (follow): Theo dõi nhật ký theo thời gian thực (realtime streaming log).
  3. `--no-pager`: Xuất thẳng dữ liệu không dừng trang (dùng cho script tự động).
**Tiêu chí chấm:**
- 0: Không biết lệnh `journalctl`.
- 1: Biết `journalctl` nhưng không nhớ cờ `-u` để lọc theo tên dịch vụ.
- 2: Phân tích chính xác cơ chế tập trung log của journald và các cờ `-u`, `-n`, `-f`.
- 3: Nêu đúng + viết câu lệnh CLI `journalctl -u my-app.service -n 20 --no-pager`.
**Câu hỏi đào sâu:** Ưu điểm của journald so với việc ứng dụng tự ghi log ra file thô `/tmp/app.log` là gì? *(Journald tự động xoay vòng log, đánh chỉ mục theo thời gian/mức độ lỗi, chống tràn đĩa cứng.)*

---

### Câu 8 — Tối ưu Hiệu năng với Handler cho `daemon-reload`
**Hỏi:** Tại sao nên đưa task `daemon_reload: true` vào Handler thay vì chạy trực tiếp ở mọi lượt Playbook? *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
- Lý do: Đảm bảo tính Idempotency và tối ưu hiệu năng. Việc nạp lại daemon (`daemon-reload`) tiêu tốn một lượng tài nguyên CPU của Systemd Manager trên máy đích. Nếu đưa vào Handler với thuộc tính `notify:` từ task template `.service`, Ansible sẽ CHỈ THỰC THI `daemon-reload` khi nội dung Unit File trên đĩa thực sự có sự thay đổi.
- Nếu không đổi code: Handler không chạy, Playbook kết thúc với `changed=0`.
**Tiêu chí chấm:**
- 0: Không biết lý do dùng Handler cho `daemon-reload`.
- 1: Biết dùng Handler cho gọn nhưng không giải thích được bài toán bảo vệ tính Idempotency.
- 2: Phân tích chính xác cơ chế trigger của Handler khi Unit File bị biến đổi nội dung.
- 3: Nêu đúng + viết đoạn Task template có `notify:` và đoạn Handler tương ứng.
**Câu hỏi đào sâu:** Nếu trong Playbook có 3 task cùng notify cho 1 Handler `daemon-reload` thì Handler đó chạy mấy lần? *(Chỉ chạy đúng 1 lần duy nhất ở cuối Playbook.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Systemd 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook quản lý Systemd Custom Service để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective RHCE Service Management).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-systemd.yml`: Ansible tạo user `sysops`, render tệp `/etc/systemd/system/my-app.service`, kích hoạt Handler `daemon-reload` và start service báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-systemd.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/systemd/system/my-app.service` kiểm tra Unit File đúng `User=sysops` và dùng `docker exec target1 ps aux | grep app.py` kiểm tra tiến trình thực sự chạy dưới user `sysops`.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` và `ps aux` đối soát tiến trình thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát tiến trình `ps aux`.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE Service Management.
**Câu hỏi đào sâu:** Lệnh `systemctl status my-app.service` ở Lần 2 trả về trạng thái gì? *(Trả về `active (running)` và hiển thị PID của tiến trình.)*

---

### Câu 10 — Cấu hình Giới hạn Tài nguyên Resource Limits trong Unit File ★★★
**Hỏi:** Làm thế nào để giới hạn dung lượng RAM và số lượng File Descriptors tối đa mà một Custom Systemd Service được phép sử dụng?
**Đáp án chuẩn:**
Khai báo các chỉ thị giới hạn tài nguyên trong phần `[Service]` của Unit File:
```ini
[Service]
MemoryMax=512M
LimitNOFILE=65536
```
- `MemoryMax=512M`: Giới hạn dịch vụ chỉ được phép ngốn tối đa 512MB RAM (nếu vượt quá sẽ bị cgroup OOM kill và restart lại).
- `LimitNOFILE=65536`: Nâng giới hạn mở file tối đa cho tiến trình daemon (tránh lỗi `Too many open files`).
**Tiêu chí chấm:**
- 0: Không biết các chỉ thị resource limits của Systemd.
- 1: Biết giới hạn RAM nhưng không nhớ tên thuộc tính `MemoryMax` hoặc `LimitNOFILE`.
- 2: Phân tích chính xác cơ chế cgroups điều khiển giới hạn tài nguyên dịch vụ của Systemd.
- 3: Nêu đúng + viết đoạn INI cấu hình `MemoryMax` và `LimitNOFILE` chuẩn xác.
**Câu hỏi đào sâu:** Systemd dùng công nghệ kernel Linux nào để thực thi giới hạn `MemoryMax`? *(Công nghệ Linux Control Groups - cgroups.)*

---

### Câu 11 — Ngăn ngừa Lặp Restart Vô tận với `StartLimitBurst` ★★★
**Hỏi:** Nếu một ứng dụng tùy chỉnh dính lỗi code nghiêm trọng khiến nó bị crash liên tục ngay khi vừa khởi động, thuộc tính nào trong Systemd giúp ngăn ngừa việc restart vô hạn làm ngập CPU/Log?
**Đáp án chuẩn:**
Khai báo thuộc tính giới hạn tần suất restart trong phần `[Unit]`:
```ini
[Unit]
StartLimitIntervalSec=60s
StartLimitBurst=5
```
- Ý nghĩa: Nếu dịch vụ bị crash và phải restart lại quá 5 lần (`StartLimitBurst=5`) trong vòng 60 giây (`StartLimitIntervalSec=60s`), Systemd sẽ tạm ngắt dịch vụ và chuyển sang trạng thái `failed` chứ không cố restart nữa.
Giúp bảo vệ máy chủ không bị treo đứt tài nguyên do kịch bản crash loop gây ra.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính ngăn ngừa flapping restart.
- 1: Biết ngắt restart nhưng không nhớ tên `StartLimitIntervalSec` và `StartLimitBurst`.
- 2: Phân tích chính xác cơ chế ngắt mạch (Circuit Breaker) chống flapping crash loop của Systemd.
- 3: Nêu đúng + viết đoạn INI `[Unit]` chứa 2 chỉ thị trên chuẩn xác.
**Câu hỏi đào sâu:** Làm thế nào để xoá trạng thái `failed` để dịch vụ được phép start lại sau khi sửa code? *(Chạy lệnh `systemctl reset-failed my-app.service`.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Custom Systemd Service Enterprise ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên tự động hóa đóng gói và quản lý Systemd Service chuyên nghiệp, hạ đặc quyền an toàn và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Biên soạn Unit File 3 phần chuẩn (`[Unit]`, `[Service]`, `[Install]`) bằng `ansible.builtin.template` đặt vào `/etc/systemd/system/`.
2. **Quy tắc 2:** Luôn bật cơ chế tự khôi phục `Restart=always` và `RestartSec=5s` cho 100% Custom Service.
3. **Quy tắc 3:** Hạ đặc quyền an toàn cho tiến trình ứng dụng chạy dưới tài khoản `User=sysops` (`shell: /sbin/nologin`).
4. **Quy tắc 4:** Bật `enabled: yes` và `state: started`, sử dụng Handler cho `daemon_reload: true` chỉ chạy khi Unit File đổi.
5. **Quy tắc 5:** Quản lý log tập trung qua `journalctl -u service` và đối soát Lần 2 đạt `changed=0` qua `docker exec` và `ps aux`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy Quản trị Hệ thống Linux & Ansible Enterprise.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp mở màn cho Giai đoạn 5 (Nâng cao và Capstone)? *(Tất cả 5 quy tắc hợp nhất trong Buổi 27 khởi đầu cho Giai đoạn 5.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm đóng gói ứng dụng và quản lý Systemd Service trên Linux với Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi tự động hóa 100% việc đóng gói và quản lý vòng đời ứng dụng dưới dạng Custom Systemd Unit File (`/etc/systemd/system/*.service`) bằng Ansible: biên soạn Template Jinja2 chuẩn 3 phần (`[Unit]`, `[Service]`, `[Install]`), cấu hình cơ chế Self-healing tự khôi phục khi crash với `Restart=always` và `RestartSec=5s`, tuân thủ bảo mật tối thiểu bằng cách hạ đặc quyền chạy under user non-root (`User=sysops`). Tôi tự động hóa việc nạp lại daemon `daemon_reload: yes` qua Handler tối ưu, bật `enabled: yes` và `state: started`, quản lý nhật ký tập trung qua `journalctl`, đảm bảo 100% Playbook đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát tiến trình thực tế bằng `docker exec` và `ps aux`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Phạm Văn G | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Trần Thị H | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 28

Để chuẩn bị tốt nhất cho **Buổi 28: firewalld-iptables-security — Quản lý Tường lửa Firewalld, Iptables và Bảo mật Hệ thống**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Ansible Collection `ansible.posix.firewalld` quản lý các vùng bảo mật (Zones) và cổng dịch vụ (Ports / Services) như thế nào?
2. **Nghiên cứu trước 2:** Sự khác biệt giữa thuộc tính `permanent: yes` và `immediate: yes` trong module `ansible.posix.firewalld` là gì?
3. **Nghiên cứu trước 3:** Làm thế nào để mở cổng 80/4000 cho Web Server và cổng 22 cho SSH một cách an toàn mà không làm đứt kết nối quản trị?

---


### [Chuyên Đề 28] Tự Động Hóa An Ninh Mạng Với Firewalld & Iptables: Quản Lý Port, Rich Rules, IP Sets & Chặn IP Độc Hại Tự Động

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Ansible Collection FQCN nào là công cụ tiêu chuẩn để quản lý dịch vụ tường lửa Firewalld trên Enterprise Linux? Nêu 3 tham số cơ bản của module này. *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Collection FQCN: <code>ansible.posix.firewalld</code></div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3 Tham số cơ bản:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <code>zone:</code> Chỉ định phân vùng bảo mật (ví dụ <code>zone: public</code> hoặc <code>zone: internal</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <code>service:</code> / <code>port:</code> Chỉ định tên dịch vụ mở (như <code>service: http</code>) hoặc số cổng kèm giao thức (như <code>port: 8080/tcp</code>).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> <code>state:</code> Trạng thái áp dụng (<code>state: enabled</code> mở quy tắc, <code>state: disabled</code> đóng quy tắc).</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không nhớ Collection <code>ansible.posix.firewalld</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết tên Collection nhưng không liệt kê được các tham số <code>zone</code>, <code>service</code>, <code>port</code>, <code>state</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò Collection FQCN chính chủ của Red Hat trong quản lý Firewalld.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + viết đoạn Task Ansible <code>ansible.posix.firewalld</code> hoàn chỉnh.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Làm thế nào để cài đặt Collection <code>ansible.posix</code> nếu môi trường Control Node bị thiếu? *(Chạy lệnh <code>ansible-galaxy collection install ansible.posix</code>.)*
</div>
</details>

---

### Câu 2 — Phối hợp Kép `permanent: true` và `immediate: true` 🔥
**Hỏi:** Tại sao việc kết hợp cả hai thuộc tính `permanent: true` và `immediate: true` lại là quy định bắt buộc khi mở cổng/dịch vụ tường lửa? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- Sự phối hợp bắt buộc:
  + `permanent: true`: Ghi quy tắc tường lửa vào tệp cấu hình trên đĩa cứng (`/etc/firewalld/zones/public.xml`) để quy tắc giữ nguyên không bị mất khi máy chủ reboot.
  + `immediate: true`: Nạp ngay quy tắc vào bộ nhớ đệm RAM để quy tắc có hiệu lực lập tức ngay tại thời điểm thi hành mà không cần chạy `firewall-cmd --reload`.
- Nếu thiếu 1 trong 2: Thiếu `permanent` quy tắc sẽ mất khi reboot; thiếu `immediate` quy tắc không có hiệu lực ngay khiến ứng dụng bị chặn mạng.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `permanent` và `immediate`.
- 1: Biết `permanent` để lưu khi reboot nhưng không giải thích được vai trò có hiệu lực ngay của `immediate`.
- 2: Phân tích chính xác tác dụng lưu đĩa vs nạp RAM của bộ đôi `permanent: true` & `immediate: true`.
- 3: Nêu đúng + viết đoạn Task Ansible chứa bộ đôi thuộc tính chuẩn xác.
**Câu hỏi đào sâu:** Điều gì xảy ra nếu chỉ đặt `permanent: true` mà không có `immediate: true`? *(Quy tắc được ghi vào file XML trên đĩa nhưng chưa có hiệu lực trong RAM, ứng dụng vẫn bị tường lửa chặn cho đến khi reboot máy.)*

---

### Câu 3 — Phòng chống Tự khóa SSH với Lockout Protection First 🔥
**Hỏi:** Tại sao Task mở cổng SSH 22 bắt buộc phải nằm ở vị trí ĐẦU TIÊN trong Playbook cấu hình tường lửa? *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- Lý do bắt buộc: Đây là quy tắc an toàn sinh tử (Lockout Protection First). Khi Ansible thi hành Playbook cấu hình tường lửa, nếu bạn đặt các task đóng tường lửa hoặc đổi default policy ở phía trên trước khi mở cổng SSH 22, kết nối SSH của Ansible Control Node sẽ bị ngắt lập tức. Playbook sẽ bị crash đứt kết nối giữa chừng và máy chủ Managed Node bị khóa hoàn toàn không thể truy cập từ xa.
- Đặt mở `service: ssh` lên vị trí Task 1 bảo đảm duy trì kết nối SSH xuyên suốt quá trình thi hành.
**Tiêu chí chấm:**
- 0: Không biết rủi ro tự khóa mất SSH.
- 1: Biết nên mở SSH trước nhưng không giải thích được cơ chế đứt kết nối SSH điều khiển của Ansible Control Node.
- 2: Phân tích chính xác rủi ro ngắt SSH giữa chừng và nguyên tắc Lockout Protection First.
- 3: Nêu đúng + viết đoạn Task 1 mở cổng SSH 22 chuẩn xác.
**Câu hỏi đào sâu:** Làm thế nào để ứng cứu khẩn cấp nếu lỡ tay khóa mất SSH của server Production? *(Phải truy cập qua console trực tiếp, Out-of-band IPMI/iLO/iDRAC hoặc KVM của Cloud Provider để gõ lệnh khôi phục.)*

---

### Câu 4 — Mở Cổng Dịch vụ `service:` vs Cổng Số `port:` 🔥
**Hỏi:** Phân biệt cách sử dụng thuộc tính `service:` và `port:` trong `ansible.posix.firewalld`. Nêu ví dụ cho từng trường hợp. *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- `service:` Dùng để mở các cổng mạng được định nghĩa sẵn theo chuẩn hệ thống (như `http` cổng 80, `https` cổng 443, `ssh` cổng 22, `postgresql` cổng 5432).
  Ví dụ: `service: http`
- `port:` Dùng để mở các cổng số tùy chỉnh kèm giao thức TCP hoặc UDP (như `8080/tcp`, `9000/tcp`, `53/udp`).
  Ví dụ: `port: 8080/tcp`
- Quy tắc: Cổng tùy chỉnh bắt buộc phải có hậu tố `/tcp` hoặc `/udp`.
**Tiêu chí chấm:**
- 0: Không phân biệt được `service:` và `port:`.
- 1: Biết tên dịch vụ vs cổng số nhưng quên cú pháp bắt buộc hậu tố `/tcp` của `port:`.
- 2: Phân tích chính xác sự khác biệt giữa dịch vụ định nghĩa sẵn và cổng số giao thức tùy chỉnh.
- 3: Nêu đúng + viết 2 đoạn Task YAML ví dụ cho cả `service:` và `port:`.
**Câu hỏi đào sâu:** Tệp cấu hình nào trên Linux định nghĩa danh sách các tên service và số cổng tương ứng? *(Tệp `/etc/services`.)*

---

### Câu 5 — Giới hạn IP Nguồn với Rich Rules 🔥
**Hỏi:** Tác dụng của thuộc tính `rich_rule:` trong `ansible.posix.firewalld` là gì? Viết Rich Rule chỉ cho phép dải IP `192.168.1.0/24` truy cập cổng PostgreSQL 5432. *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Tác dụng `rich_rule:` Dùng để thiết lập các quy tắc tường lửa nâng cao (Firewalld Rich Rules), giúp lọc chi tiết địa chỉ IP nguồn (Source IP filtering), giao thức và hành động (accept/reject/drop).
- Đoạn Rich Rule mẫu:
  ```yaml
  - name: Allow PostgreSQL only from 192.168.1.0/24
    ansible.posix.firewalld:
      rich_rule: rule family="ipv4" source address="192.168.1.0/24" port port="5432" protocol="tcp" accept
      zone: public
      permanent: true
      immediate: true
      state: enabled
  ```
**Tiêu chí chấm:**
- 0: Không biết khái niệm Rich Rules.
- 1: Biết Rich Rule để lọc IP nhưng không viết được cú pháp chuỗi `rule family="ipv4" source address=...`.
- 2: Phân tích chính xác vai trò cứng hóa bảo mật ngăn chặn mở toang cổng DB cho public Internet.
- 3: Nêu đúng + viết đoạn YAML Task chứa Rich Rule chuẩn xác từng từ khóa.
**Câu hỏi đào sâu:** Khác biệt giữa hành động `reject` và `drop` trong Rich Rule là gì? *(`reject` trả về thông báo từ chối cho máy gửi; `drop` lặng lẽ vứt bỏ gói tin không trả về bất kỳ phản hồi nào.)*

---

### Câu 6 — Phân vùng Bảo mật Firewall Zones
**Hỏi:** Khái niệm Firewall Zones trong Firewalld là gì? Nêu 3 vùng phổ biến và mục đích sử dụng. *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- Khái niệm: Firewall Zones là cơ chế phân chia mức độ tin cậy bảo mật khác nhau cho các card mạng (Interfaces) hoặc dải IP khác nhau.
- 3 Vùng phổ biến:
  1. `public`: Mức tin cậy thấp, dùng cho card mạng kết nối Internet (chỉ mở các cổng công cộng như 80/443).
  2. `internal` / `work`: Mức tin cậy trung bình, dùng cho dải mạng nội bộ Doanh nghiệp (mở thêm các dịch vụ trao đổi nội bộ).
  3. `trusted`: Mức tin cậy tuyệt đối, chấp nhận toàn bộ lưu lượng mạng đi qua.
**Tiêu chí chấm:**
- 0: Không biết khái niệm Firewall Zones.
- 1: Biết tên zone `public` nhưng không giải thích được vai trò gán chính sách bảo mật theo card mạng.
- 2: Phân tích chính xác cơ chế phân tầng bảo mật theo Zones của Firewalld.
- 3: Nêu đúng + minh họa ví dụ cấu hình rule trên zone `public` và zone `internal`.
**Câu hỏi đào sâu:** Lệnh CLI nào kiểm tra xem card mạng `eth0` đang thuộc zone nào? *(Lệnh `firewall-cmd --get-zone-of-interface=eth0`.)*

---

### Câu 7 — Cấu hình Iptables Cấp thấp với `ansible.builtin.iptables`
**Hỏi:** Khi nào cần sử dụng module `ansible.builtin.iptables` thay vì `ansible.posix.firewalld`? Nêu ví dụ thêm quy tắc ACCEPT cho cổng 80. *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
- Khi nào cần dùng: Dùng khi làm việc trên các hệ thống Linux không sử dụng Firewalld (như Ubuntu/Debian dùng iptables/ufw thô) hoặc khi cần can thiệp các quy tắc hạt nhân cấp thấp như NAT Masquerade, PREROUTING, Port Forwarding.
- Đoạn Task mẫu:
  ```yaml
  - name: Allow HTTP in Iptables
    ansible.builtin.iptables:
      chain: INPUT
      protocol: tcp
      destination_port: '80'
      jump: ACCEPT
  ```
**Tiêu chí chấm:**
- 0: Không biết module `ansible.builtin.iptables`.
- 1: Biết `iptables` nhưng không giải thích được trường hợp dùng cho NAT/Forwarding cấp thấp.
- 2: Phân tích chính xác sự khác biệt giữa Firewalld (dịch vụ tầng trên) và Iptables (hạt nhân tầng dưới).
- 3: Nêu đúng + viết đoạn Task Ansible `ansible.builtin.iptables` chuẩn xác.
**Câu hỏi đào sâu:** Thuộc tính `chain:` trong `ansible.builtin.iptables` gồm các giá trị cơ bản nào? *(`INPUT`, `OUTPUT`, `FORWARD`, `PREROUTING`, `POSTROUTING`.)*

---

### Câu 8 — Cấu hình Tường lửa Offline với `offline: true`
**Hỏi:** Thuộc tính `offline: true` trong `ansible.posix.firewalld` có tác dụng gì khi dịch vụ `firewalld` đang bị stopped? *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
- Tác dụng: Cho phép Ansible can thiệp và chỉnh sửa trực tiếp các quy tắc tường lửa trong các tệp cấu hình XML tại `/etc/firewalld/` ngay cả khi dịch vụ daemon `firewalld` đang ở trạng thái dừng (`stopped`).
- Ý nghĩa thực tế: Giúp kỹ sư chuẩn bị sẵn bộ quy tắc an toàn mạng trước khi bật dịch vụ tường lửa, đảm bảo ngay tại thời điểm `firewalld` daemon vừa khởi chạy là các quy tắc an toàn đã có hiệu lực ngay lập tức.
**Tiêu chí chấm:**
- 0: Không biết cờ `offline: true`.
- 1: Biết `offline` để sửa khi stop nhưng không giải thích được cơ chế can thiệp trực tiếp file XML `/etc/firewalld/`.
- 2: Phân tích chính xác cơ chế cấu hình tĩnh offline trước khi boot service.
- 3: Nêu đúng + viết đoạn Task YAML chứa `offline: true`.
**Câu hỏi đào sâu:** Nếu service `firewalld` đang stopped mà gọi `ansible.posix.firewalld` không có `offline: true` thì bị lỗi gì? *(Ansible báo lỗi `firewalld is not running` và fail task.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng Firewall 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một Playbook quản lý quy tắc tường lửa để đảm bảo tính Idempotency và máy đích ở đúng trạng thái an toàn (hoàn thành 100% Objective RHCE Firewall Management).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1):** Chạy `ansible-playbook site-firewall.yml`: Ansible đảm bảo service `firewalld` running, mở cổng SSH 22 ở Task 1, mở `http`/`https`, mở `8080/tcp`, nạp Rich Rule `5432` báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2):** Chạy lại nguyên vẹn `ansible-playbook site-firewall.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 firewall-cmd --zone=public --list-all` kiểm tra danh sách dịch vụ/cổng mở và Rich Rules thực sự tồn tại trên máy đích.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` hoặc không dùng `docker exec` và `firewall-cmd --list-all` đối soát quy tắc thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa câu lệnh CLI và đối soát `firewall-cmd`.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE Firewall Management.
**Câu hỏi đào sâu:** Lệnh `firewall-cmd --zone=public --list-all` ở Lần 2 có thay đổi không? *(Hoàn toàn giữ nguyên 100%, các quy tắc đã có sẵn trên đĩa và RAM.)*

---

### Câu 10 — Xóa Quy tắc Tường lửa với `state: disabled` ★★★
**Hỏi:** Làm thế nào để đóng một cổng dịch vụ hoặc xóa một Rich Rule cũ đã được nạp từ trước bằng `ansible.posix.firewalld`?
**Đáp án chuẩn:**
Sử dụng thuộc tính `state: disabled` (hoặc `state: absent`) kết hợp với `permanent: true` và `immediate: true`:
```yaml
- name: Close custom port 8080 immediately and permanently
  ansible.posix.firewalld:
    port: 8080/tcp
    zone: public
    permanent: true
    immediate: true
    state: disabled
```
Ansible sẽ xóa quy tắc khỏi bộ nhớ RAM và xóa khỏi tệp XML trên đĩa cứng `/etc/firewalld/zones/public.xml`.
**Tiêu chí chấm:**
- 0: Không biết cách xóa quy tắc tường lửa.
- 1: Biết dùng `state: disabled` nhưng quên thuộc tính `permanent: true` & `immediate: true`.
- 2: Phân tích chính xác cơ chế gỡ bỏ quy tắc cả RAM và đĩa cứng của `state: disabled`.
- 3: Nêu đúng + viết đoạn Task Ansible xóa cổng `8080/tcp` chuẩn xác.
**Câu hỏi đào sâu:** Nếu chỉ đặt `state: disabled` với `immediate: true` mà quên `permanent: true` thì điều gì xảy ra khi reboot? *(Cổng bị đóng ngay lập tức trên RAM, nhưng khi reboot máy chủ cổng sẽ tự động mở lại do file XML vẫn lưu quy tắc cũ.)*

---

### Câu 11 — Chuyển tiếp Cổng Port Forwarding với Firewalld ★★★
**Hỏi:** Viết Task Ansible sử dụng `ansible.posix.firewalld` cấu hình chuyển tiếp cổng (Port Forwarding): mọi lưu lượng truy cập cổng 80 sẽ tự động được chuyển tiếp sang cổng 8080 trên cùng máy chủ.
**Đáp án chuẩn:**
Sử dụng thuộc tính `port_forward:` trong `ansible.posix.firewalld`:
```yaml
- name: Forward port 80 to 8080
  ansible.posix.firewalld:
    port_forward:
      - port: 80
        proto: tcp
        toport: 8080
    zone: public
    permanent: true
    immediate: true
    state: enabled
```
Giúp ứng dụng Web chạy ở cổng non-privileged `8080` có thể tiếp nhận lưu lượng từ cổng chuẩn `80` mà không cần chạy under root.
**Tiêu chí chấm:**
- 0: Không biết cấu hình Port Forwarding trong Firewalld.
- 1: Biết chuyển tiếp cổng nhưng không viết được cú pháp thuộc tính `port_forward:`.
- 2: Phân tích chính xác bài toán chuyển tiếp cổng cho ứng dụng non-root.
- 3: Nêu đúng + viết đoạn Task Ansible `port_forward:` chuẩn xác từng chi tiết.
**Câu hỏi đào sâu:** Cần bật tính năng kernel Linux nào để Port Forwarding hoạt động giữa các card mạng khác nhau? *(Bật IP Forwarding: `net.ipv4.ip_forward = 1`.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Quản lý Tường lửa Enterprise ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên tự động hóa quản lý tường lửa Firewalld & Iptables chuyên nghiệp, cứng hóa an toàn mạng và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Dùng Collection `ansible.posix.firewalld` và BẮT BUỘC mở cổng SSH 22 ở vị trí ĐẦU TIÊN (Lockout Protection First).
2. **Quy tắc 2:** Luôn kết hợp bộ đôi `permanent: true` (lưu đĩa) và `immediate: true` (áp dụng RAM) cho mọi task.
3. **Quy tắc 3:** Mở cổng theo `service:` hoặc `port: 8080/tcp` và phân vùng bảo mật rõ ràng theo `zone:`.
4. **Quy tắc 4:** Bảo vệ cổng Database bằng Rich Rules (`rich_rule:`) giới hạn dải IP nguồn, tuyệt đối không mở toang public.
5. **Quy tắc 5:** Dùng `ansible.builtin.iptables` cho quy tắc hạt nhân NAT/Forwarding và đối soát Lần 2 đạt `changed=0` qua `firewall-cmd --list-all`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy Network Security Hardening Enterprise đỉnh cao.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp bảo vệ kỹ sư không bị ngắt đứt kết nối SSH quản trị giữa chừng? *(Quy tắc 1: Mở cổng SSH 22 ở vị trí đầu tiên.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm quản lý tường lửa Firewalld, Iptables và bảo mật hệ thống mạng với Ansible, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi tự động hóa 100% việc quản lý tường lửa và cứng hóa an toàn mạng (Network Hardening) cấp Enterprise bằng Collection `ansible.posix.firewalld` và `ansible.builtin.iptables`: luôn thực thi quy tắc Lockout Protection mở cổng SSH 22 ở vị trí đầu tiên chống đứt kết nối quản trị, kết hợp triệt để bộ đôi `permanent: true` và `immediate: true` đảm bảo quy tắc có hiệu lực tức thì và duy trì sau reboot. Tôi phân vùng bảo mật theo Zones (`public`, `internal`), bảo vệ tuyệt đối cổng Database bằng Rich Rules (`rich_rule:`) giới hạn dải IP nguồn, cấu hình Port Forwarding linh hoạt, đảm bảo 100% Playbook đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật mạng bằng `docker exec` và `firewall-cmd --list-all`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Nguyễn Văn I | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Đặng Thị K | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 29

Để chuẩn bị tốt nhất cho **Buổi 29: awx-aap — Quản trị Tập trung với AWX / Ansible Automation Platform (AAP)**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** AWX và Red Hat Ansible Automation Platform (AAP) cung cấp giao diện Web UI, REST API và RBAC quản lý Ansible như thế nào?
2. **Nghiên cứu trước 2:** Khái niệm Execution Environments (EE), Project, Inventory, Credentials và Job Templates trong AWX hoạt động ra sao?
3. **Nghiên cứu trước 3:** Làm thế nào để kích hoạt tự động chạy Playbook trong AWX qua Webhook từ GitHub / GitLab khi có sự kiện push code?

---


### [Chuyên Đề 29] Quản Trị Tự Động Hóa Doanh Nghiệp Với AWX & Red Hat Ansible Automation Platform (AAP): RBAC, Job Templates & Workflows

---



## Bộ câu hỏi phỏng vấn chuyên sâu — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> AWX và Red Hat Ansible Automation Platform (AAP) là gì? Trình bày 4 lý do lớn tại sao Doanh nghiệp phải chuyển đổi từ chạy Ansible CLI cá nhân sang nền tảng tập trung AWX / AAP. *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Định nghĩa: AWX (Open Source) và AAP (Enterprise) là nền tảng quản trị tập trung kịch bản tự động hóa Ansible qua giao diện Web UI, REST API và mô hình phân quyền RBAC.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 4 Lý do chuyển đổi:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <b style="color: var(--accent-primary);">Phân quyền RBAC:</b> Phân chia chi tiết quyền hạn ai được gạt nút chạy kịch bản nào, trên môi trường nào.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <b style="color: var(--accent-primary);">Bảo mật Credentials tập trung:</b> Mã hóa AES-256 SSH Keys và Vault Passwords, không cho phép xem hay lộ plaintext.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> <b style="color: var(--accent-primary);">Nhật ký Audit tập trung:</b> Lưu trữ lịch sử toàn bộ các lần chạy kịch bản (ai chạy, khi nào, log chi tiết).</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">4.</b> <b style="color: var(--accent-primary);">REST API & Webhooks:</b> Tích hợp tự động hóa với hệ thống CI/CD, ServiceNow, Jira và event push code.</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không biết AWX / AAP.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết AWX để chạy giao diện Web nhưng không liệt kê được 4 bài toán lớn về RBAC, Audit, Credentials và API.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò chuyển đổi quy mô Enterprise từ CLI cá nhân lên nền tảng tập trung AWX.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + minh họa ví dụ tệp định nghĩa AWX Project & Job Template.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Phân biệt sự khác nhau giữa AWX và Red Hat Ansible Automation Platform (AAP). *(AWX là dự án mã nguồn mở upstream của cộng đồng; AAP là sản phẩm thương mại được Red Hat hỗ trợ chính thức có thêm tính năng Enterprise Automation Controller, Private Automation Hub và Event-Driven Ansible.)*
</div>
</details>

---

### Câu 2 — Môi trường Thi hành Container Execution Environment (EE) 🔥
**Hỏi:** Khái niệm Execution Environment (EE) trong AWX / AAP là gì? Tại sao EE lại giải quyết được triệt tiêu bài toán "trên máy tôi chạy được mà trên máy anh lại lỗi"? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- Khái niệm: Execution Environment (EE) là một Container Image (xây dựng qua `ansible-builder`) chứa phiên bản `ansible-core`, các gói thư viện Python dependencies và các Ansible Collections được định nghĩa cố định.
- Tại sao giải quyết xung đột: Trước đây khi chạy CLI, mỗi máy cá nhân có phiên bản Python hay Collections khác nhau gây lỗi không đồng nhất. Với EE, 100% các Job thi hành trên AWX đều chạy bên trong một container EE đóng gói chuẩn hóa, bảo đảm tính nhất quán môi trường tuyệt đối.
**Tiêu chí chấm:**
- 0: Không biết khái niệm Execution Environment (EE).
- 1: Biết EE là container nhưng không giải thích được cơ chế đóng gói ansible-core + Python libs + Collections.
- 2: Phân tích chính xác vai trò triệt tiêu xung đột môi trường bằng container EE.
- 3: Nêu đúng + dán tệp cấu hình YAML định nghĩa EE `execution-environment.yml`.
**Câu hỏi đào sâu:** Công cụ CLI nào của Red Hat được dùng để đóng gói và build một Execution Environment container image? *(Công cụ `ansible-builder`.)*

---

### Câu 3 — Bảo mật Mật khẩu với AWX Credentials 🔥
**Hỏi:** AWX Credentials quản lý thông tin xác thực (SSH Keys, Vault Passwords, Cloud Tokens) như thế nào để đảm bảo tính an toàn tối thượng? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Cơ chế bảo mật AWX Credentials:
  1. Mã hóa bằng thuật toán AES-256 trong cơ sở dữ liệu PostgreSQL của AWX.
  2. Khi gán Credential vào Job Template, AWX tự động tiêm bí mật vào tiến trình runner execution khi chạy Job.
  3. Mật khẩu và SSH Private Key tuyệt đối KHÔNG BAO GIỜ hiển thị lại dưới dạng chuỗi rõ (Plaintext) trên màn hình Web UI hay trong log console. Kỹ sư có quyền gạt nút run nhưng KHÔNG THỂ đọc hay copy mật khẩu.
**Tiêu chí chấm:**
- 0: Không biết cơ chế mã hóa AWX Credentials.
- 1: Biết AWX giấu mật khẩu nhưng không giải thích được cơ chế tiêm bí mật mã hóa AES-256 vào runner execution.
- 2: Phân tích chính xác vai trò bảo vệ bí mật tối thượng không lộ plaintext của AWX Credentials.
- 3: Nêu đúng + minh họa ví dụ khai báo Credential Machine trong AWX.
**Câu hỏi đào sâu:** Nếu một kỹ sư cố tình viết task `ansible.builtin.debug: var=ansible_password` để in mật khẩu ra log thì AWX xử lý ra sao? *(AWX Runner có cơ chế tự động lọc và thay thế các chuỗi secret thành `[ENCRYPTED]` hoặc `[HIDDEN]` trong log.)*

---

### Câu 4 — Quản lý Job Templates và Extra Variables 🔥
**Hỏi:** Job Template trong AWX đại diện cho những thành phần cấu hình nào gắn kết với nhau? Tính năng `Prompt on Launch` có tác dụng gì? *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- Thành phần gắn kết trong Job Template:
  1. **Project:** Kho mã nguồn Playbook Git.
  2. **Inventory:** Danh sách máy chủ mục tiêu.
  3. **Credentials:** Mật khẩu SSH / Vault.
  4. **Execution Environment:** Container môi trường thi hành.
  5. **Playbook:** File `.yml` chính cần chạy (ví dụ `site-awx.yml`).
- Tác dụng `Prompt on Launch`: Cho phép hiển thị một bảng hỏi (Survey / Prompt) bắt buộc người dùng truyền hoặc chọn các biến động (Extra Variables như `release_version`) trước khi bấm nút khởi chạy Job.
**Tiêu chí chấm:**
- 0: Không biết Job Template.
- 1: Biết Job Template để chạy code nhưng không liệt kê đủ 5 thành phần cốt lõi trỏ tới.
- 2: Phân tích chính xác cơ chế gắn kết 5 thành phần và vai trò truyền biến động của `Prompt on Launch`.
- 3: Nêu đúng + viết đoạn YAML định nghĩa `awx/job-template.yml`.
**Câu hỏi đào sâu:** Phân biệt sự khác nhau giữa `job_type: run` và `job_type: check` trong Job Template. *(`run` thi hành thật; `check` thi hành mô phỏng Check Mode `--check`.)*

---

### Câu 5 — Xây dựng Luồng Quy trình với Workflow Job Template 🔥
**Hỏi:** Workflow Job Template trong AWX dùng để làm gì? Trình bày 2 nhánh liên kết điều kiện `On Success` và `On Failure`. *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- Tác dụng: Cho phép kết nối nhiều Job Templates độc lập thành một sơ đồ đồ thị quy trình tự động hóa phức tạp cấp Enterprise.
- 2 Nhánh điều kiện:
  + `On Success` (màu xanh): Chỉ đạo bước tiếp theo thi hành KHI VÀ CHỈ KHI bước trước đó hoàn thành trạng thái `successful`.
  + `On Failure` (màu đỏ): Chỉ đạo bước tiếp theo thi hành KHI bước trước đó rơi vào trạng thái `failed` (dùng để gửi cảnh báo Slack hoặc chạy kịch bản tự động Rollback).
**Tiêu chí chấm:**
- 0: Không biết Workflow Job Template.
- 1: Biết nối nhiều Job nhưng không nêu được cơ chế phân nhánh điều kiện `On Success` / `On Failure`.
- 2: Phân tích chính xác vai trò tự động hóa quy trình phức tạp và xử lý sự cố rẽ nhánh.
- 3: Nêu đúng + vẽ sơ đồ đồ thị Workflow hoặc viết đoạn YAML `awx/workflow-template.yml`.
**Câu hỏi đào sâu:** Ngoài `On Success` và `On Failure`, còn có nhánh liên kết điều kiện nào nữa? *(Nhánh `Always` — luôn luôn thi hành bất kể bước trước thành công hay thất bại.)*

---

### Câu 6 — Tự động hóa qua Webhook Triggers và REST API
**Hỏi:** Làm thế nào để tự động hóa việc gạt nút thi hành AWX Job Template thông qua REST API hoặc Webhook từ GitLab? *(Liên quan QT 5.3, QT 6.2)*
**Đáp án chuẩn:**
- Qua REST API: Gửi một HTTP POST request tới endpoint `/api/v2/job_templates/<id>/launch/` kèm Header chứa OAuth2 Bearer Token.
- Qua Webhook Trigger: Bật cờ `enable_webhook: true` trong Job Template và lấy Secret Token dán vào phần Webhook Settings của GitLab project. Khi có sự kiện `push` code, GitLab tự động kích hoạt AWX Job Template chạy mà không cần con người bấm nút.
**Tiêu chí chấm:**
- 0: Không biết REST API hay Webhook của AWX.
- 1: Biết gọi API nhưng không viết được cờ `curl` hoặc không giải thích được cơ chế Event-driven từ GitLab.
- 2: Phân tích chính xác triết lý Event-Driven Automation qua REST API & Webhooks.
- 3: Nêu đúng + viết câu lệnh `curl -X POST` kích hoạt launch Job Template.
**Câu hỏi đào sâu:** Định dạng dữ liệu trả về của AWX REST API khi launch Job thành công là gì? *(Trả về JSON mã HTTP Status 201 Created chứa `job_id` vừa khởi tạo.)*

---

### Câu 7 — Phân quyền Người dùng theo Mô hình RBAC
**Hỏi:** Mô hình RBAC (Role-Based Access Control) trong AWX hoạt động như thế nào? Nêu 3 Roles phổ biến cấp cho User/Team. *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- Hoạt động: RBAC cho phép gán các vai trò (Roles) cụ thể cho các Người dùng (Users) hoặc Nhóm (Teams) trên từng Tài nguyên (Organization, Project, Inventory, Job Template).
- 3 Roles phổ biến:
  1. `Admin` (Organization Admin / System Admin): Có toàn quyền quản trị, chỉnh sửa cấu hình.
  2. `Execute` (Job Template Execute): Chỉ có quyền gạt nút bấm chạy Job Template, không có quyền sửa code hay sửa Inventory.
  3. `Read` (Auditor / Read-Only): Chỉ có quyền xem cấu hình và lịch sử log audit.
**Tiêu chí chấm:**
- 0: Không biết mô hình RBAC trong AWX.
- 1: Biết phân quyền nhưng không liệt kê được 3 Roles `Admin`, `Execute`, `Read`.
- 2: Phân tích chính xác cơ chế phân quyền bảo mật Least Privilege cho các Teams (Devs, Ops, Security).
- 3: Nêu đúng + viết đoạn YAML ví dụ gán quyền Execute cho Team Developers.
**Câu hỏi đào sâu:** Tại sao nên gán quyền RBAC cho Team thay vì gán trực tiếp cho từng User cá nhân? *(Để dễ quản lý: khi có nhân sự mới gia nhập hoặc rời Team, chỉ cần thêm/xóa User khỏi Team mà không phải sửa quyền rải rác.)*

---

### Câu 8 — Đồng bộ Mã nguồn Project với `scm_update_on_launch`
**Hỏi:** Thuộc tính `scm_update_on_launch` trong AWX Project đóng vai trò gì để đảm bảo kịch bản luôn dùng code mới nhất? *(Liên quan QT 4.1)*
**Đáp án chuẩn:**
- Vai trò: Khi bật `scm_update_on_launch: true`, mỗi lần một Job Template trỏ tới Project đó được khởi chạy, AWX sẽ tự động thực hiện lệnh `git pull` đồng bộ mã nguồn mới nhất từ Git Repository về trước khi thi hành Playbook.
- Tầm quan trọng: Đảm bảo kịch bản luôn sử dụng mã nguồn mới nhất đã được duyệt trên nhánh `main`, loại bỏ rủi ro thi hành bằng code cũ bị lỗi đang cache trên AWX.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `scm_update_on_launch`.
- 1: Biết để sync code nhưng không giải thích được cơ chế tự động `git pull` trước mỗi lượt launch Job.
- 2: Phân tích chính xác vai trò đồng bộ hóa mã nguồn tức thì của `scm_update_on_launch`.
- 3: Nêu đúng + viết đoạn YAML cấu hình AWX Project chứa `scm_update_on_launch: true`.
**Câu hỏi đào sâu:** Nếu tắt `scm_update_on_launch`, làm thế nào để cập nhật mã nguồn trong AWX Project? *(Phải bấm nút "Sync Project" thủ công trên Web UI hoặc gọi API sync.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng khi Dùng AWX 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu một kịch bản Ansible được thực thi qua AWX Job Template để đảm bảo tính Idempotency và máy đích ở đúng trạng thái (hoàn thành 100% Objective RHCE Enterprise Platform).
**Đáp án chuẩn:**
1. **Bước 1 (Thực thi Lần 1 qua AWX):** Bấm nút Launch Job Template trên AWX Web UI (hoặc gọi REST API): AWX tiêm Credentials, nạp container EE, thi hành Playbook `site-awx.yml` nạp cấu hình lên máy đích báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Lần 2 qua Re-launch AWX):** Bấm Re-launch Job Template Lần 2 trên AWX: nhật ký Job Details trên giao diện Web UI **bắt buộc phải đạt `changed=0`** (tất cả các Task đều báo `ok`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/awx-deployment.conf` kiểm tra file cấu hình thực sự tồn tại đúng dữ liệu `AWX_PLATFORM_STATUS=SUCCESSFUL` và `RELEASE_VERSION=3.5.0`.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 Re-launch Job Template `changed=0` hoặc không dùng `docker exec` đối soát file thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa log AWX Job Details và đối soát file thật.
- 3: Trình bày xuất sắc 3 bước + khẳng định hoàn thành 100% Objective RHCE Enterprise Platform (`☑`).
**Câu hỏi đào sâu:** Màn hình AWX Job Details hiển thị màu gì khi Job chạy thành công Lần 2 với `changed=0`? *(Màu xanh lá cây với status `Successful` và `changed=0`.)*

---

### Câu 10 — Tương tác qua AWX CLI Client Tool ★★★
**Hỏi:** Trình bày cách cài đặt và sử dụng bộ công cụ dòng lệnh `awx` CLI client tool để tương tác với AWX Server mà không cần mở trình duyệt Web.
**Đáp án chuẩn:**
- Cài đặt: `pip install awxkit`
- Cấu hình biến môi trường kết nối:
  ```bash
  export TOWER_HOST=https://awx.company.local
  export TOWER_OAUTH_TOKEN="my_oauth2_bearer_token"
  ```
- Các câu lệnh CLI cơ bản:
  ```bash
  # Liệt kê danh sách các Job Templates
  awx job_templates list

  # Kích hoạt chạy Job Template ID 42 và theo dõi log
  awx job_templates launch --id 42 --monitor
  ```
**Tiêu chí chấm:**
- 0: Không biết công cụ `awx` CLI.
- 1: Biết tên tool nhưng không liệt kê được biến môi trường `TOWER_HOST` và lệnh `launch --monitor`.
- 2: Phân tích chính xác cơ chế tương tác dòng lệnh qua `awx` CLI tool.
- 3: Nêu đúng + viết các câu lệnh CLI `export` và `awx job_templates launch`.
**Câu hỏi đào sâu:** Cờ `--monitor` trong lệnh `awx job_templates launch` có tác dụng gì? *(Nó giữ kết nối terminal và stream toàn bộ log thi hành của Job từ AWX Server về màn hình console local.)*

---

### Câu 11 — Tự động hóa Phân tích Sự cố Event-Driven Ansible (EDA) ★★★
**Hỏi:** Trong hệ sinh thái Red Hat Ansible Automation Platform 2.4+, Event-Driven Ansible (EDA) và Rulebooks đóng vai trò gì trong việc xử lý sự cố tự động không cần con người?
**Đáp án chuẩn:**
- Vai trò EDA: Event-Driven Ansible (EDA) là thành phần mới cho phép Ansible lắng nghe liên tục các sự kiện (Events) từ hệ thống giám sát (Prometheus, Kafka, Webhooks, Syslog).
- Cơ chế Rulebooks: Khi phát hiện sự kiện bất thường (ví dụ Prometheus báo `MemoryHighWarning`), EDA Rulebook sẽ phân tích và TỰ ĐỘNG kích hoạt AWX Job Template xử lý sự cố (như restart service hoặc dọn đĩa) trong vài giây mà không cần con người can thiệp.
**Tiêu chí chấm:**
- 0: Không biết khái niệm Event-Driven Ansible (EDA).
- 1: Biết EDA để lắng nghe event nhưng không nêu được cơ chế Rulebook kết hợp với AWX Job Template.
- 2: Phân tích chính xác mô hình tự động hóa tự chữa lành (Self-healing Infrastructure) của EDA.
- 3: Nêu đúng + mô tả luồng Prometheus Event -> EDA Rulebook -> AWX Job Launch.
**Câu hỏi đào sâu:** Ngôn ngữ dùng để viết Ansible Rulebook trong EDA là gì? *(Ngôn ngữ YAML chứa các phần `sources`, `rules`, `actions`.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng về Quản trị Tập trung AWX / AAP ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng giúp quản trị viên chuyển đổi và vận hành nền tảng tự động hóa tập trung AWX / AAP Enterprise chuyên nghiệp, bảo mật 100% bí mật và đạt Idempotency 100%.
**Đáp án chuẩn:**
1. **Quy tắc 1:** Chuyển đổi quản trị từ CLI cá nhân sang nền tảng tập trung AWX / AAP Web UI & REST API.
2. **Quy tắc 2:** Chuẩn hóa môi trường thi hành bằng Execution Environment (EE) container đóng gói cố định.
3. **Quy tắc 3:** Bảo mật bí mật tuyệt đối bằng AWX Credentials mã hóa AES-256, tuyệt đối không lộ plaintext.
4. **Quy tắc 4:** Tự động hóa luồng quy trình phức tạp bằng Workflow Job Template (`On Success` / `On Failure`) và Webhook triggers.
5. **Quy tắc 5:** Phân quyền RBAC tối thiểu cho Teams và đảm bảo Job Re-launch Lần 2 đạt `changed=0` qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được các quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện tư duy Nền tảng Tự động hóa Enterprise đỉnh cao.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào trực tiếp chuẩn bị nền tảng cho Buổi 30 (Capstone Project)? *(Tất cả 5 quy tắc hợp nhất trong Buổi 29 chuẩn bị nền tảng vững chắc cho Buổi 30 Capstone Project.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn về kinh nghiệm vận hành nền tảng quản trị tập trung AWX / Red Hat Ansible Automation Platform (AAP) cấp Enterprise, học viên hãy đưa ra câu chốt tự tin sau:

> **"Tôi vận hành nền tảng tự động hóa hạ tầng tập trung cấp Enterprise với AWX / Red Hat Ansible Automation Platform (AAP): chuyển đổi toàn bộ kịch bản từ CLI cá nhân sang quản trị tập trung qua Web UI và REST API (`/api/v2/`), đóng gói và chuẩn hóa môi trường runner bằng Execution Environments (EE) container image, quản lý bảo mật tuyệt đối thông tin xác thực bằng AWX Credentials mã hóa AES-256 không bao giờ lộ plaintext. Tôi thiết kế luồng quy trình phức tạp bằng Workflow Job Templates với phân nhánh điều kiện `On Success` và `On Failure`, tự động hóa kích hoạt qua Event Webhook Triggers từ GitLab, áp dụng mô hình phân quyền RBAC chặt chẽ cho các phòng ban, đảm bảo 100% kịch bản thi hành qua AWX Job Template đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai và đối soát sự thật máy đích bằng `docker exec`."**

---

## V4. Bảng tổng hợp điểm vấn đáp

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại |
|---|---|---|---|---|---|---|
| Đinh Văn L | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | Xuất sắc |
| Mai Thị M | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | Trung bình |

---

## V5. BTVN 4 — Ba câu chuẩn bị cho Buổi 30 (CAPSTONE PROJECT)

Để chuẩn bị tốt nhất cho **Buổi 30: capstone-tu-dong-hoa-da-tang — ĐỈNH CAO KHÓA HỌC: Capstone Project — Tự động hóa Hệ thống Nhiều tầng Đầu-Cuối (Multi-Tier Enterprise Infrastructure Automation)**, học viên làm 3 câu hỏi nghiên cứu trước sau:

1. **Nghiên cứu trước 1:** Kiến trúc hệ thống Web-App-DB 3 tầng (Multi-tier Infrastructure) gồm Load Balancer Nginx, Web Node Python/NodeJS và Database PostgreSQL được phối hợp như thế nào bằng Ansible Roles?
2. **Nghiên cứu trước 2:** Làm thế nào để hợp nhất toàn bộ các kỹ năng đã học (Inventory, Variables, Vault, System Roles, Performance, Error Handling, Testing, CI/CD, Systemd, Firewall, AWX) vào tệp Playbook Capstone tổng thể?
3. **Nghiên cứu trước 3:** Kịch bản kiểm thử Idempotency toàn diện từ đầu tới cuối (End-to-End Idempotency Test) cho một hạ tầng 3 tầng phức tạp đòi hỏi các bước đối soát CLI và `docker exec` ra sao để đạt điểm tuyệt đối 100% của khóa học?

---


### [Chuyên Đề 30] Đồ Án Capstone: Xây Dựng Hệ Thống Tự Động Hóa Hạ Tầng Doanh Nghiệp Đa Tầng (Load Balancer, Web, DB, Security) End-to-End

---



Hội đồng Giám khảo gọi trực tiếp từng học viên lên bảo vệ báo cáo Dự án Capstone Tốt nghiệp toàn khóa và trả lời trực tiếp các câu hỏi phỏng vấn chuyên sâu trong bộ 12 câu bên dưới.

Giám khảo thực hiện chấm điểm tốt nghiệp theo thang **0–3 điểm**:
- **0 điểm:** Không trả lời được hoặc trả lời sai lệch hoàn toàn bản chất vấn đề hạ tầng Enterprise.
- **1 điểm:** Chỉ nhớ được từ khóa bề nổi nhưng giải thích sai cơ chế hoạt động bên dưới.
- **2 điểm:** Giải thích chính xác cơ chế hoạt động nhưng thiếu minh hoạ câu lệnh hoặc con số thực tế.
- **3 điểm:** Trả lời xuất sắc cơ chế, nêu rõ câu lệnh CLI, cờ tham số, cấu trúc Roles và con số chứng minh Idempotency trên môi trường thật.

Các câu hỏi gắn nhãn 🔥 là **câu hỏi tủ tốt nghiệp bắt buộc**, học viên phải đạt tối thiểu 2 điểm. Các câu gắn nhãn ★★★ là **câu hỏi phân loại chuyên gia IaC**.

> **Hai lỗi nghiêm trọng dẫn tới TRẦN ĐIỂM 1:**
> 1. Đóng gói gộp 3 tầng vào 1 server duy nhất, để lộ mật khẩu CSDL hoặc khóa SSH dưới dạng plaintext, hoặc chạy Web App dưới quyền `root`.
> 2. Luồng HTTP 3 tầng End-to-End bị đứt gãy lỗi 502/500, và không kiểm tra lại Idempotency Lần 2 (`changed=0`) và sự thật trên máy đích qua `docker exec`.

---

## V2. Bộ câu hỏi — ĐÚNG 12 câu

<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  
<b style="color: var(--accent-primary);">Hỏi:</b> Trình bày mô hình kiến trúc Enterprise 3 tầng (Nginx LB -> Web Cluster -> PostgreSQL DB) trong Dự án Capstone. Tại sao việc chia 3 tầng độc lập lại vượt trội hơn cài gộp vào 1 server? *(Liên quan QT 4.1)*
<b style="color: var(--accent-primary);">Đáp án chuẩn:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Mô hình 3 tầng:</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">1.</b> <b style="color: var(--accent-primary);">Tầng 1 (Load Balancer Nginx):</b> Tiếp nhận lưu lượng HTTP/HTTPS cổng 80/443 từ công chúng và điều hướng round-robin tới cụm Web Nodes.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">2.</b> <b style="color: var(--accent-primary);">Tầng 2 (Web Cluster Systemd Service):</b> Xử lý logic ứng dụng, chạy hạ đặc quyền under user <code>sysops</code> với <code>Restart=always</code>.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-cyan);"><b style="color: var(--accent-cyan);">3.</b> <b style="color: var(--accent-primary);">Tầng 3 (Database Cluster PostgreSQL):</b> Lưu trữ dữ liệu hệ thống, bảo vệ tuyệt đối bằng Firewalld Rich Rules chỉ cho phép IP Web Nodes truy cập cổng 5432.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• Ưu điểm vượt trội: Tăng khả năng mở rộng (Scalability - dễ dàng add thêm Web Node), tính sẵn sàng cao (High Availability), và bảo mật chuyên sâu (Defense in Depth - DB bị cô lập khỏi Internet).</div>
<b style="color: var(--accent-primary);">Tiêu chí chấm:</b>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 0: Không nêu được 3 tầng kiến trúc.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 1: Biết 3 tầng nhưng không giải thích được vai trò mở rộng và bảo mật chuyên sâu Defense in Depth.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 2: Phân tích chính xác vai trò của 3 tầng Nginx LB, Systemd Web App và PostgreSQL DB.</div>
  <div style="margin: 0.35rem 0; padding-left: 1rem; border-left: 2px solid var(--accent-primary);">• 3: Nêu đúng + vẽ sơ đồ luồng dữ liệu 3 tầng xuất sắc.</div>
<b style="color: var(--accent-primary);">Câu hỏi đào sâu:</b> Làm thế nào để thêm máy chủ Web Node thứ 3 vào cụm Web Cluster mà không phải sửa file Playbook? *(Chỉ cần khai báo thêm host <code>web3</code> vào nhóm <code>[web]</code> trong <code>inventory/capstone-hosts.ini</code>, Nginx Upstream Jinja2 Template sẽ tự động phát hiện và sinh cấu hình mới.)*
</div>
</details>

---

### Câu 2 — Tổ chức Cấu trúc Bộ Roles Phân tầng Capstone 🔥
**Hỏi:** Tại sao việc tổ chức bộ 4 Roles Capstone (`role_common_security`, `role_db`, `role_web`, `role_lb`) lại là tiêu chuẩn bắt buộc cho kịch bản tự động hóa quy mô lớn? *(Liên quan QT 4.2)*
**Đáp án chuẩn:**
- Lý do bắt buộc:
  1. **Tính mô-đun hóa (Modularity):** Mỗi Role quản lý duy nhất 1 thành phần hạ tầng độc lập, giúp mã nguồn sạch sẽ, dễ đọc.
  2. **Tính tái sử dụng (Reusability):** `role_common_security` hoặc `role_lb` có thể được tái sử dụng 100% cho các dự án khác mà không cần sửa đổi.
  3. **Dễ bảo trì và làm việc nhóm (Maintainability & Collaboration):** Đội Security bảo trì `role_common_security`, Đội DBA bảo trì `role_db`, Đội Web Dev bảo trì `role_web`.
**Tiêu chí chấm:**
- 0: Không biết cấu trúc Roles.
- 1: Biết dùng Roles nhưng không nêu được 3 nguyên lý Modularity, Reusability và Maintainability.
- 2: Phân tích chính xác cấu trúc bộ 4 Roles Capstone trong dự án Enterprise.
- 3: Nêu đúng + vẽ sơ đồ cấu trúc cây thư mục `roles/` chuẩn mực.
**Câu hỏi đào sâu:** Thứ tự gọi thi hành 4 Roles trong Playbook `site-capstone.yml` có quan trọng không? Tại sao? *(Rất quan trọng: phải chạy `role_common_security` đầu tiên để chống tự khóa SSH, tiếp theo là `role_db`, sau đó `role_web`, và cuối cùng là `role_lb` để đảm bảo phụ thuộc hạ tầng.)*

---

### Câu 3 — Bảo mật Mật khẩu và Chìa khóa Bí mật với Ansible Vault 🔥
**Hỏi:** Ansible Vault mã hóa tệp `vars/vault.yml` chứa mật khẩu CSDL PostgreSQL như thế nào để đảm bảo an toàn tuyệt đối khi đưa code lên Git Repository? *(Liên quan QT 4.3)*
**Đáp án chuẩn:**
- Cơ chế Ansible Vault:
  + Sử dụng thuật toán mã hóa đối xứng chuẩn AES-256 (Advanced Encryption Standard).
  + Tệp `vars/vault.yml` chứa mật khẩu `vault_db_password` được mã hóa thành các chuỗi byte không thể đọc được.
  + Khi thi hành Playbook, Ansible nạp khóa Vault qua cờ `--vault-password-file .vault_pass` để giải mã biến trong RAM tại thời điểm thi hành.
  + Tệp mã hóa `vars/vault.yml` an toàn 100% khi commit lên Git Repository công cộng.
**Tiêu chí chấm:**
- 0: Không biết Ansible Vault.
- 1: Biết Vault để giấu mật khẩu nhưng không giải thích được cơ chế mã hóa AES-256 và giải mã trong RAM khi thi hành.
- 2: Phân tích chính xác vai trò bảo vệ bí mật theo chuẩn SecOps của Ansible Vault.
- 3: Nêu đúng + viết câu lệnh `ansible-vault encrypt` và `ansible-playbook --vault-password-file`.
**Câu hỏi đào sâu:** Làm thế nào để tự động xóa tệp `.vault_pass` sau khi pipeline CI/CD thi hành xong? *(Thêm bước `after_script: rm -f .vault_pass` trong pipeline CI/CD.)*

---

### Câu 4 — Render Dynamic Nginx Upstream với Jinja2 Template 🔥
**Hỏi:** Đoạn mã Jinja2 Template trong `roles/role_lb/templates/nginx.conf.j2` tự động sinh danh sách Web Nodes Nginx Upstream như thế nào? *(Liên quan QT 5.1)*
**Đáp án chuẩn:**
- Đoạn mã Jinja2 Template:
  ```nginx
  upstream capstone_web_backend {
  {% for host in groups['web'] %}
      server {{ hostvars[host]['ansible_host'] }}:8080 max_fails=3 fail_timeout=10s;
  {% endfor %}
  }
  ```
- Cơ chế: Vòng lặp `{% for host in groups['web'] %}` duyệt qua tất cả các máy chủ thuộc nhóm `web` trong Inventory, lấy địa chỉ `ansible_host` của từng máy và render ra dòng `server <ip>:8080`.
- Kết quả: Khi thêm hoặc bớt máy chủ trong nhóm `web`, file `nginx.conf` sẽ tự động cập nhật chính xác danh sách Nginx Upstream.
**Tiêu chí chấm:**
- 0: Không biết Nginx Upstream Jinja2 Template.
- 1: Biết vòng lặp `for` nhưng không viết được cú pháp `groups['web']` và `hostvars[host]['ansible_host']`.
- 2: Phân tích chính xác cơ chế tự động hóa phát hiện Web Node động (Dynamic Discovery).
- 3: Nêu đúng + viết đoạn mã Jinja2 Template `nginx.conf.j2` chuẩn xác.
**Câu hỏi đào sâu:** Tham số `max_fails=3` và `fail_timeout=10s` trong Nginx Upstream có ý nghĩa gì? *(Nó chỉ đạo Nginx đánh dấu Web Node bị lỗi nếu nó trả về thất bại 3 lần liên tiếp trong 10 giây và tạm thời không chuyển request tới node đó.)*

---

### Câu 5 — Đóng gói Web App với Custom Systemd Service dưới User `sysops` 🔥
**Hỏi:** Tại sao Web App trong `role_web` bắt buộc phải đóng gói dưới dạng Custom Systemd Service (`web-app.service`), bật `Restart=always` và chạy under non-root user `sysops`? *(Liên quan QT 5.2)*
**Đáp án chuẩn:**
- 3 Lý do chuyên sâu:
  1. **Đóng gói chuẩn hóa (Standardization):** Giúp quản lý vòng đời ứng dụng bằng các lệnh chuẩn `systemctl start/stop/status web-app`.
  2. **Tự khôi phục sự cố (Self-healing):** Thuộc tính `Restart=always` và `RestartSec=5s` chỉ đạo Systemd tự động khởi động lại Web App trong 5 giây nếu tiến trình bị crash đột ngột.
  3. **Hạ đặc quyền bảo mật (Security Hardening):** Khai báo `User=sysops` bảo đảm ứng dụng chạy hạ đặc quyền; nếu ứng dụng bị dính lỗ hổng bảo mật RCE, kẻ tấn công cũng không thể chiếm quyền quản trị `root` của máy chủ.
**Tiêu chí chấm:**
- 0: Không biết Systemd Service.
- 1: Biết Systemd để start service nhưng không giải thích được tác dụng tự phục hồi `Restart=always` và hạ đặc quyền `User=sysops`.
- 2: Phân tích xuất sắc 3 vai trò Standardization, Self-healing và Security Hardening.
- 3: Nêu đúng + dán tệp Unit File template `web-app.service.j2` chuẩn mực.
**Câu hỏi đào sâu:** Điều gì xảy ra nếu bạn quên task `daemon_reload: true` khi chỉnh sửa tệp `web-app.service`? *(Systemd Manager sẽ phát cảnh báo tệp Unit File bị thay đổi trên đĩa và không nạp cấu hình mới cho đến khi daemon được reload.)*

---

### Câu 6 — Cứng hóa An toàn Mạng với Firewalld Rich Rules
**Hỏi:** Tầng Database PostgreSQL trong `role_db` được bảo vệ bằng Firewalld Rich Rules ra sao? Nêu câu lệnh hoặc Task Ansible khai báo. *(Liên quan QT 5.3)*
**Đáp án chuẩn:**
- Cơ chế bảo vệ: Cống PostgreSQL 5432 bị cô lập hoàn toàn. Sử dụng Firewalld Rich Rule chỉ cho phép duy nhất các địa chỉ IP của các máy chủ thuộc nhóm `web` được mở kết nối vào cổng 5432.
- Đoạn Task Ansible:
  ```yaml
  - name: Allow PostgreSQL access ONLY from Web Nodes
    ansible.posix.firewalld:
      rich_rule: rule family="ipv4" source address="{{ hostvars[item]['ansible_host'] }}" port port="5432" protocol="tcp" accept
      zone: public
      permanent: true
      immediate: true
      state: enabled
    loop: "{{ groups['web'] }}"
  ```
**Tiêu chí chấm:**
- 0: Không biết Firewalld Rich Rules.
- 1: Biết lọc IP nhưng không viết được cú pháp chuỗi `rich_rule:` dùng vòng lặp `loop: "{{ groups['web'] }}"`.
- 2: Phân tích chính xác nguyên lý Zero Trust bảo vệ tầng Database.
- 3: Nêu đúng + viết đoạn Task Ansible `ansible.posix.firewalld` Rich Rule chuẩn xác.
**Câu hỏi đào sâu:** Làm thế nào để đối soát quy tắc Rich Rule vừa nạp trên máy chủ DB? *(Chạy lệnh `docker exec target2 firewall-cmd --zone=public --list-all`.)*

---

### Câu 7 — Rolling Deployment `serial: 1` Zero Downtime
**Hỏi:** Ý nghĩa của thuộc tính `serial: 1` trong Playbook `site-capstone.yml` khi triển khai cụm Web Nodes là gì? *(Liên quan QT 6.1)*
**Đáp án chuẩn:**
- Ý nghĩa: `serial: 1` chỉ đạo Ansible thực thi kịch bản cập nhật cuốn chiếu (Rolling Update): Ansible chia cụm Web Nodes thành từng máy chủ một (1 host/batch).
- Luồng triển khai Zero Downtime:
  1. Ansible rút Web Node 1 ra khỏi lưu lượng, cập nhật code mới, restart `web-app.service` và kiểm tra sức khỏe thành công.
  2. Nginx Load Balancer tự động nhận diện Web Node 1 đã OK.
  3. Ansible chuyển sang cập nhật tiếp Web Node 2.
- Kết quả: Hệ thống luôn duy trì ít nhất 1 Web Node phục vụ người dùng, đạt tiêu chuẩn triển khai Zero Downtime 100%.
**Tiêu chí chấm:**
- 0: Không biết thuộc tính `serial: 1`.
- 1: Biết `serial: 1` là chạy từng máy nhưng không giải thích được cơ chế nâng cấp cuốn chiếu Zero Downtime.
- 2: Phân tích chính xác luồng Rolling Update cuốn chiếu của `serial: 1`.
- 3: Nêu đúng + minh họa ví dụ cấu hình `serial: 1` trong Playbook Capstone.
**Câu hỏi đào sâu:** Nếu trong cụm 10 Web Nodes có 1 Node bị fail khi chạy `serial: 1` thì Ansible xử lý ra sao? *(Ansible ngắt dừng Playbook ngay lập tức ở Node bị fail đó, bảo vệ 9 Nodes còn lại không bị nâng cấp nhầm mã nguồn lỗi.)*

---

### Câu 8 — Tự động hóa End-to-End Verification Luồng HTTP 3 Tầng
**Hỏi:** Làm thế nào để tự động hóa quy trình kiểm thử nghiệm thu End-to-End Verification cho cả 3 tầng (Nginx LB -> Web App -> PostgreSQL DB) bằng Ansible? *(Liên quan QT 6.2)*
**Đáp án chuẩn:**
- Sử dụng module `ansible.builtin.uri` ở bước cuối của Playbook Capstone để gửi một HTTP GET request tới địa chỉ IP của Nginx Load Balancer.
- Đoạn Task mẫu:
  ```yaml
  - name: Verify End-to-End HTTP 3-Tier flow
    ansible.builtin.uri:
      url: "http://{{ hostvars[groups['lb'][0]]['ansible_host'] }}/"
      status_code: 200
      return_content: true
    register: e2e_check
    failed_when: "'DB_CONNECTED_SUCCESS' not in e2e_check.content"
  ```
- Kết quả: Khi Nginx nhận request, nó chuyển tiếp tới Web Node; Web Node truy vấn PostgreSQL DB OK và trả về chuỗi `DB_CONNECTED_SUCCESS`. Task `uri` xác nhận kết quả thành công.
**Tiêu chí chấm:**
- 0: Không biết kiểm thử nghiệm thu End-to-End.
- 1: Biết dùng lệnh `curl` nhưng không viết được Task `ansible.builtin.uri` với điều kiện `failed_when`.
- 2: Phân tích chính xác vai trò khẳng định sự thông suốt thực tế của cả 3 tầng.
- 3: Nêu đúng + viết đoạn Task Ansible `ansible.builtin.uri` chuẩn xác.
**Câu hỏi đào sâu:** Nếu Task End-to-End Verification bị fail do lỗi HTTP 502 Bad Gateway thì nguyên nhân nằm ở đâu? *(Do Nginx LB không thể kết nối tới cổng 8080 của Web Nodes hoặc dịch vụ `web-app.service` trên Web Nodes chưa ở trạng thái started.)*

---

### Câu 9 — Phương pháp Chứng minh Idempotency và Máy đúng Tốt nghiệp Capstone 🔥
**Hỏi:** Trình bày quy trình 3 bước nghiệm thu Dự án Capstone để đạt chuẩn Tốt nghiệp Xuất sắc khóa học ntkansible (100% Idempotency PASSED và Máy đúng). *(Liên quan QT 6.3)*
**Đáp án chuẩn:**
1. **Bước 1 (Thi hành Capstone Lần 1):** Chạy `ansible-playbook -i inventory/capstone-hosts.ini site-capstone.yml`: Ansible khởi tạo user `sysops`, nạp Vault pass, cài Nginx, deploy Systemd `web-app.service`, mở Firewalld Rich Rules báo `changed > 0`.
2. **Bước 2 (Kiểm Idempotency Capstone Lần 2):** Chạy lại nguyên vẹn `ansible-playbook -i inventory/capstone-hosts.ini site-capstone.yml` Lần 2: bảng `PLAY RECAP` **bắt buộc phải đạt `changed=0` tuyệt đối trên TẤT CẢ các máy chủ** (`lb1`, `web1`, `web2`, `db1`).
3. **Bước 3 (Đối soát Sự thật Máy đích):** Dùng `docker exec target1 cat /etc/capstone-app.conf` kiểm tra file cấu hình chứa đúng `APP_STATUS=ACTIVE` và `DB_CONNECTED_SUCCESS=TRUE`, và `ps aux` xác nhận tiến trình `app.py` chạy under `sysops`.
**Tiêu chí chấm:**
- 0: Trả lời "chỉ cần nhìn terminal Lần 1 báo xanh là xong" (dính bẫy trần điểm 1).
- 1: Thiếu bước Lần 2 `changed=0` trên tất cả các nodes hoặc không dùng `docker exec` đối soát file và tiến trình thật.
- 2: Trình bày đủ 3 bước nhưng chưa minh họa log `PLAY RECAP` Lần 2 và đối soát máy đích.
- 3: Trình bày xuất sắc 3 bước + khẳng định TỐT NGHIỆP XUẤT SẮC KHÓA HỌC NTKANSIBLE.
**Câu hỏi đào sâu:** Chỉ số `changed=0` ở Lần 2 khẳng định điều gì về chất lượng mã nguồn bộ Roles Capstone? *(Khẳng định 100% các Tasks trong bộ Roles đều được thiết kế tuân thủ nghiêm ngặt nguyên lý Idempotency, không có task nào dùng lệnh shell thô bị lặp changed.)*

---

### Câu 10 — Tự động hóa Hạ tầng Tương lai với Infrastructure as Code (IaC) ★★★
**Hỏi:** Sau khi hoàn thành Dự án Capstone ntkansible, bạn sẽ ứng dụng tư duy Infrastructure as Code (IaC) này như thế nào để xây dựng hệ thống CI/CD/GitOps tự động hóa toàn diện cho Doanh nghiệp?
**Đáp án chuẩn:**
- Chiến lược ứng dụng IaC toàn diện:
  1. **Quản lý mã nguồn tập trung (GitOps):** Đưa 100% kịch bản Ansible Roles và Playbooks vào Git Repository, quản lý phiên bản qua Pull/Merge Requests.
  2. **Tự động hóa Kiểm thử (Automated Testing):** Tích hợp `ansible-lint` và Molecule (Buổi 25) vào pipeline GitLab CI / GitHub Actions (Buổi 26) để tự động kiểm thử kịch bản trên môi trường ephemeral container.
  3. **Vận hành tập trung (Centralized Execution):** Đăng ký kịch bản lên AWX / Red Hat AAP (Buổi 29), phân quyền RBAC và kích hoạt tự động qua Event-driven Webhooks khi merge code mới.
**Tiêu chí chấm:**
- 0: Không có định hướng ứng dụng IaC.
- 1: Nói chung chung về dùng Ansible nhưng không kết nối được chuỗi kiến thức GitOps + Molecule + CI/CD + AWX.
- 2: Phân tích chính xác luồng ứng dụng tư duy IaC Enterprise từ Git -> Testing -> AWX.
- 3: Nêu đúng + thể hiện tư duy Kiến trúc sư Tự động hóa Hạ tầng (Infrastructure Automation Architect) chuyên nghiệp.
**Câu hỏi đào sâu:** Công cụ nào kết hợp với Ansible để khởi tạo tài nguyên hạ tầng ảo hóa Cloud (AWS/Azure/GCP) trước khi Ansible nạp cấu hình? *(Công cụ HashiCorp Terraform hoặc OpenToFu.)*

---

### Câu 11 — Lộ trình Chinh phục Chứng chỉ Quốc tế Red Hat Certified Engineer (RHCE EX294) ★★★
**Hỏi:** Hãy tóm tắt các nhóm kỹ năng trọng tâm trong chứng chỉ RHCE EX294 và phương pháp làm bài thi thực hành 100% trên máy thật của Red Hat.
**Đáp án chuẩn:**
- Các nhóm kỹ năng RHCE EX294 (phủ 100% trong ntkansible):
  1. **Ansible Control Node Setup:** `ansible.cfg`, `inventory`, Ansible Vault, Ad-hoc commands.
  2. **Playbooks & Roles Execution:** Variables, Facts, Conditionals, Loops, Handlers, Templates, Blocks, Jinja2, Custom Roles, Ansible Galaxy collections.
  3. **System Administration Automation:** Storage LVM, Users/Groups, Systemd Services, SELinux, Cron Jobs, Firewalld & Ports.
- Phương pháp làm bài thi RHCE EX294:
  + Bài thi kéo dài 4 giờ, thực hành 100% trên máy lab thật.
  + Luôn kiểm tra cú pháp bằng `ansible-playbook --syntax-check`.
  + Luôn chạy lại Playbook Lần 2 để đảm bảo Idempotency `changed=0`.
  + Luôn dùng câu lệnh hệ thống (`systemctl`, `firewall-cmd`, `curl`) đối soát máy đích trước khi nộp bài.
**Tiêu chí chấm:**
- 0: Không biết về kỳ thi RHCE EX294.
- 1: Biết tên chứng chỉ nhưng không liệt kê được 3 nhóm kỹ năng trọng tâm và phương pháp đối soát máy thật.
- 2: Phân tích chính xác cấu trúc bài thi RHCE EX294 và bí quyết làm bài Idempotency `changed=0`.
- 3: Nêu đúng + khẳng định tự tin 100% thi đạt chứng chỉ RHCE EX294 điểm cao.
**Câu hỏi đào sâu:** Điểm đạt (Passing Score) của kỳ thi RHCE EX294 là bao nhiêu? *(Đạt tối thiểu 210 / 300 điểm - tương ứng 70%.)*

---

### Câu 12 — Tóm tắt 5 Quy tắc Vàng Tốt nghiệp Khóa học NTKANSIBLE ★★★
**Hỏi:** Tóm tắt 5 Quy tắc Vàng khẳng định tư duy và năng lực của một Chuyên gia Tự động hóa Ansible cấp Enterprise (Tốt nghiệp Khóa học ntkansible).
**Đáp án chuẩn:**
1. **Quy tắc 1 (Mô-đun hóa & Phân tầng):** Tổ chức bộ Roles phân tầng chuyên nghiệp (`role_common_security`, `role_db`, `role_web`, `role_lb`), tái sử dụng cao và dễ bảo trì.
2. **Quy tắc 2 (An toàn & SecOps First):** Luôn mở cổng SSH 22 ở vị trí ĐẦU TIÊN (Lockout Protection First), mã hóa bí mật với Ansible Vault AES-256, chạy app under non-root user `sysops`, và cô lập DB bằng Firewalld Rich Rules.
3. **Quy tắc 3 (Tự động hóa Động & Triển khai Zero Downtime):** Render Jinja2 Templates động cho Nginx Upstream và áp dụng Rolling Deployment `serial: 1` Zero Downtime.
4. **Quy tắc 4 (Kiểm thử & Tự động hóa Tập trung):** Tích hợp Molecule testing, CI/CD pipeline, và vận hành tập trung qua AWX / AAP Web UI & REST API.
5. **Quy tắc 5 (Nguyên lý Cốt lõi Idempotency 100%):** Mọi kịch bản Playbook ở lượt chạy Lần 2 bắt buộc phải đạt `changed=0` tuyệt đối và đối soát sự thật máy đích qua `docker exec`.
**Tiêu chí chấm:**
- 0: Không tóm tắt được 5 quy tắc.
- 1: Liệt kê được 2-3 quy tắc chung chung.
- 2: Nêu đầy đủ 5 Quy tắc Vàng Tốt nghiệp chính xác.
- 3: Phân tích xuất sắc cả 5 quy tắc + thể hiện thần thái Chuyên gia Tự động hóa Ansible hàng đầu.
**Câu hỏi đào sâu:** Trong 5 quy tắc trên, quy tắc nào là "kim chỉ nam" xuyên suốt từ Buổi 01 tới Buổi 30 của ntkansible? *(Quy tắc 5: Nguyên lý Cốt lõi Idempotency `changed=0` và đối soát sự thật máy đích.)*

---

## V3. Câu chốt để nói khi phỏng vấn

Khi nhà tuyển dụng phỏng vấn hoặc hội đồng giám khảo chấm tốt nghiệp, học viên hãy dõng dạc đưa ra phát biểu chốt đại diện cho bản lĩnh của một **Chuyên gia Tự động hóa Hạ tầng Ansible (Enterprise Infrastructure Automation Specialist)**:

> **"Tôi sở hữu tư duy và năng lực tự động hóa hạ tầng Enterprise toàn diện từ A-Z với Ansible: thiết kế kiến trúc phân tầng 3 lớp (Nginx LB -> Web App Cluster -> PostgreSQL DB), đóng gói bộ Roles chuẩn hóa chuyên nghiệp, thực thi chiến lược an toàn SecOps First (khóa SSH 22 mở đầu tiên, Ansible Vault AES-256 mã hóa bí mật, Systemd Custom Service running under non-root user `sysops`, và Firewalld Rich Rules cô lập CSDL). Tôi tự động hóa quy trình triển khai cuốn chiếu Zero Downtime với `serial: 1`, tích hợp pipeline CI/CD và vận hành tập trung qua AWX / Red Hat Automation Platform API, cam kết 100% kịch bản Playbook đạt tiêu chuẩn Idempotent `changed=0` ở lượt chạy Lần hai, đối soát sự thật máy đích bằng `docker exec` và sẵn sàng 100% chinh phục chứng chỉ quốc tế Red Hat Certified Engineer (RHCE EX294)."**

---

## V4. Bảng tổng hợp điểm tốt nghiệp toàn khóa

| Học viên | Câu 1–5 (Tủ) | Câu 6–9 (Nền) | Câu 10 (Chủ chốt) | Câu 11–12 (Phân loại) | Điểm tổng | Xếp loại Tốt nghiệp |
|---|---|---|---|---|---|---|
| Ngô Văn N | 3 / 3 / 3 / 3 / 3 | 3 / 3 / 3 / 3 | 3 | 3 / 3 | 36 / 36 | **XUẤT SẮC (RHCE READY)** |
| Phạm Thị P | 2 / 2 / 1 / 2 / 2 | 2 / 1 / 2 / 1 | 1 (Dính trần điểm 1) | 1 / 1 | 16 / 36 (Khóa trần 1) | **TRUNG BÌNH (CẦN ÔN LẠI)** |

---

## V5. BTVN 4 — Ba hướng dẫn sau khi Tốt nghiệp Khóa học ntkansible

Chúc mừng bạn đã hoàn thành xuất sắc 30/30 Buổi học của khóa học **ntkansible**! Dưới đây là 3 bước tiếp theo để bạn nâng tầm sự nghiệp DevOps / SysAdmin / Cloud Engineer:

1. **Bước 1 — Xây dựng Portfolio IaC trên GitHub:** Push toàn bộ bộ 4 Roles Capstone, `site-capstone.yml`, tệp `README.md` hướng dẫn và hình ảnh sơ đồ Mermaid L2 lên kho GitHub cá nhân. Đây là minh chứng vàng cho năng lực thực chiến khi ứng tuyển các vị trí Senior DevOps / Cloud Engineer.
2. **Bước 2 — Đăng ký và Ôn luyện Kỳ thi RHCE EX294:** Rà soát lại 100% các mục tiêu bài thi RHCE EX294 Blueprint, tự bấm giờ làm lại kịch bản Capstone Buổi 30 trong 2.5 giờ để sẵn sàng thi đạt RHCE điểm tối đa.
3. **Bước 3 — Mở rộng Hệ sinh thái Tự động hóa:** Tiếp tục nghiên cứu mở rộng tích hợp Ansible với HashiCorp Terraform (khai báo ảo hóa Cloud), Kubernetes / OpenShift (quản lý container orchestration), và Event-Driven Ansible (EDA) để xây dựng hạ tầng tự động hóa tự chữa lành (Self-healing Infrastructure) cấp Doanh nghiệp.

---
{% endraw %}
