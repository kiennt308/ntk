---
description: "Quy chuẩn thiết kế và định dạng nội dung hiển thị chuyên nghiệp cho toàn bộ bài viết trong _posts"
globs: ["_posts/*.md"]
alwaysApply: true
---

# Quy Chuẩn Định Dạng & Trình Bày Bài Viết Kỹ Thuật (Article Presentation Standard)

Bộ quy chuẩn này được đúc kết từ quá trình chuẩn hóa thực tế để áp dụng đồng bộ cho toàn bộ các bài viết markdown (`_posts/*.md`). Mục tiêu là mang lại trải nghiệm đọc cao cấp (**Premium Reading Experience**), thu hút thị giác, tối ưu hóa giao diện Light/Dark theme, chống mỏi mắt và hiển thị hoàn hảo các khối kỹ thuật phức tạp (Mermaid, Code Diffs, Q&A Accordion, Tables).

---

## 1. Cấu Trúc Frontmatter & TL;DR

- Mỗi bài viết bắt buộc phải có trường `tldr:` dạng danh sách gồm 3–5 gạch đầu dòng tóm tắt các điểm cốt lõi:
  ```yaml
  tldr:
    - "Điểm mấu chốt 1 về kiến trúc và tư duy cốt lõi."
    - "Điểm mấu chốt 2 về cơ chế vận hành hệ thống."
    - "Điểm mấu chốt 3 về thực tiễn triển khai Production."
  ```
- **Lưu ý thực thể HTML**: Không dùng các ký tự `&` đứng trước chuỗi kết thúc bằng dấu chấm phẩy `;` mà phải escape thành `&amp;` hoặc dùng từ nối tiếng Việt ("và") để tránh lỗi parse HTML entity.

---

## 2. Bao Bọc Nội Dung Bằng Khối Liquid `{% raw %}`

- Toàn bộ nội dung bài viết sau phần tiêu đề `# Title` phải được bọc trong cặp thẻ:
  ```markdown
  {% raw %}
  # Tiêu Đề Bài Viết
  ... (Toàn bộ nội dung bài viết) ...
  {% endraw %}
  ```
- **Mục đích**: Ngăn ngừa trình biên dịch Jekyll/Liquid hiểu nhầm các cú pháp mã nguồn (Ansible `{{ item }}`, Helm, Jinja2, Go Templates) thành biến của Jekyll gây lỗi build.

---

## 3. Hệ Thống Điểm Nhấn Thị Giác & Màu Sắc (Color Accents & Badges)

Để bài viết không bị đơn điệu bởi quá nhiều chữ (text-heavy), bắt buộc sử dụng các thành phần thị giác:

### 3.1. Huy Hiệu Phân Loại (Badges)
Sử dụng các class Badge định sẵn tương thích với cả Light & Dark mode:
- `<span class="badge badge--emerald">Tên Badge</span>`: Dành cho Khái niệm tích cực, Declarative, Thành công, Tối ưu, Best Practice.
- `<span class="badge badge--rose">Tên Badge</span>`: Dành cho Nguy hiểm, Imperative, Cạm bẫy, Outage, Mốc thời gian sự cố (`🕒 02:00 AM`).
- `<span class="badge badge--amber">Tên Badge</span>`: Dành cho Cảnh báo, Drift, State File, Bước cần thận trọng.
- `<span class="badge badge--primary">Tên Badge</span>`: Dành cho Kiến trúc, Bước thực hiện (`Bước 1`), Nhãn câu hỏi (`Why 1`).
- `<span class="badge badge--cyan">Tên Badge</span>`: Dành cho Cloud APIs, Giám sát, Metrics, Tự động hóa.
- `<span class="badge badge--indigo">Tên Badge</span>`: Dành cho Công cụ phụ trợ, Frameworks, Modules.

### 3.2. Tô Màu Từ Khóa Kỹ Thuật (Inline Color Accents)
Sử dụng các biến CSS theme-aware thay vì hardcode mã màu:
- Từ khóa cốt lõi: `<strong style="color: var(--accent-primary);">Từ khóa</strong>`
- Từ khóa thành công / tiết kiệm: `<b style="color: var(--accent-emerald);">Từ khóa</b>`
- Từ khóa rủi ro / lỗi: `<b style="color: var(--accent-rose);">Từ khóa</b>`
- Từ khóa cảnh báo / state: `<b style="color: var(--accent-amber);">Từ khóa</b>`
- Từ khóa cloud / API: `<b style="color: var(--accent-cyan);">Từ khóa</b>`
- Inline code quan trọng: `<code style="color: var(--accent-rose); font-weight: 700;">-auto-approve</code>`

---

## 4. Chuẩn Hóa Khối Hộp Cảnh Báo (GitHub Alerts / Callout Boxes)

- Sử dụng định dạng GitHub Alerts chuẩn:
  ```markdown
  > [!NOTE]
  > **TIÊU ĐỀ NỔI BẬT:**
  > Nội dung giải thích chi tiết có highlight các từ khóa quan trọng.

  > [!TIP]
  > **BÀI HỌC TIẾP THEO:**
  > Giới thiệu súc tích về nội dung bài học kế tiếp.

  > [!IMPORTANT]
  > **QUY TẮC VÀNG DOANH NGHIỆP:**
  > Các quy định bắt buộc phải tuân thủ trong kiến trúc thực tế.

  > [!WARNING]
  > **CẢNH BÁO RỦI RO:**
  > Phân tích các mối nguy tiềm ẩn nếu thực hiện sai quy trình.
  ```

---

## 5. Chuẩn Hóa Sơ Đồ Kiến Trúc Mermaid (Flowcharts & Sequence Diagrams)

Mọi sơ đồ Mermaid (bao gồm `flowchart`, `graph`, và `sequenceDiagram`) phải tuân thủ nghiêm ngặt các quy tắc sau:

### 5.1. Quy chuẩn chung & Lightbox Modal Zoom
1. **Khử hoàn toàn nền đặc (Zero Solid Fill)**: Mọi khối hình (Nodes), hình thoi điều kiện (Decision Rhombus `ID{"..."}` / `<polygon>`), hộp Actor, và đặc biệt là **khung bao Subgraph / Clusters (`subgraph ... end`)** đều phải trong suốt 100% (`fill:none` hoặc `fill:transparent`). Tuyệt đối không để sót background màu đen (`#000000`, `#1f2020`) hay màu xám đặc khi hiển thị bình thường cũng như khi phóng to trong Lightbox Zoom Modal.
2. **Khung bao Subgraph / Cluster**: Viền khung subgraph sử dụng nét đứt nhẹ nhàng (`stroke-dasharray: 4, 4`), màu viền `--border-color` (`#334155`), bo góc `rx: 8px` và tiêu đề subgraph in hoa đậm nét (`font-weight: 700`, `letter-spacing: 0.04em`).
3. **Hình thoi quyết định (Decision / Rhombus Nodes)**: Bắt buộc sử dụng nền trong suốt `fill:none` hoặc `fill:transparent`, viền màu nổi bật (`stroke: var(--accent-amber)` hoặc `#f59e0b`, `stroke-width: 1.75px`) để đảm bảo độ tương phản cao trên cả nền sáng và nền tối.
4. **Tăng cường độ tương phản (High Contrast)**: Phông chữ trong sơ đồ sử dụng màu `--text-primary` (`#f8fafc` trên nền tối, `#0f172a` trên nền sáng) với độ dày chữ `font-weight: 600 - 700`.
5. **Ngắt dòng thông minh**: Dùng `<br/>` để chia text trong các khối dài thành 2–3 dòng gọn gàng, tránh làm khối bị quá dài theo chiều ngang.

### 5.2. Quy chuẩn dành riêng cho Sequence Diagrams
- **Actors / Participants**: Hộp actor phải có viền bo tròn (`rx: 8px`), viền màu kỹ thuật (Primary Blue `#38bdf8` / `#0284c7`), nền trong suốt `fill: transparent`, chữ in đậm dễ đọc.
- **Actor Lifeline**: Đường thẳng dóng xuống dạng đứt nét `stroke-dasharray: 5, 5` với màu `--text-muted`.
- **Message Lines & Arrows**: Nét vẽ rõ ràng (`stroke-width: 1.75px`), text trên đường truyền (`.messageText`) có màu rõ nét và không bị đè lên đường kẻ (`messageMargin: 35`).
- **Ghi chú (Notes)**: Khối `Note over ...` sử dụng nền mờ cao cấp (`--bg-surface-elevated`), viền màu hổ phách `#f59e0b`, text màu Amber nổi bật và bo góc 6px.
- **Đánh số tự động**: Luôn kích hoạt chỉ thị `autonumber` ở đầu mỗi sơ đồ `sequenceDiagram` để người đọc dễ dàng theo dõi tuần tự các bước tương tác.

### 5.3. Bảng Màu Viền Quy Ước (Stroke Colors):
- Đầu vào / HCL / Dev: `#6366f1` (Indigo/Primary)
- Lưu trữ / State / S3: `#f59e0b` (Amber)
- Cloud / Thực tế / AWS APIs: `#0ea5e9` (Cyan)
- Engine tính toán / Core: `#3b82f6` (Blue)
- Kế hoạch / Plan: `#f59e0b` (Amber)
- Thực thi / Thành công: `#10b981` (Emerald)
- Lỗi / Sự cố / Outage: `#f43f5e` hoặc `#dc2626` (Rose/Red)

### 5.4. Quy Chuẩn Cú Pháp & Thoát Ký Tự Tránh Lỗi Parser (Mermaid Syntax Standards)
1. **Bọc nhãn đường nối (Edge Labels) bằng dấu ngoặc kép**:
   - Tất cả nhãn trên đường kết nối (`-->|"..."|`, `---|"..."|`, `==>|"..."|`, `-.->|"..."|`) **bắt buộc phải được bọc trong cặp dấu ngoặc kép `"`**.
   - ❌ **Sai (Gây sập Mermaid Parser)**: `MASK -->|BẬT (sensitive=true)| CLI` (lỗi: `Expecting PS, got...`).
   - ✅ **Đúng**: `MASK -->|"BẬT (sensitive=true)"| CLI`.
2. **Bọc nhãn khối Node (Node Labels & Shapes) bằng dấu ngoặc kép**:
   - Mọi khối chứa dấu ngoặc đơn `()`, ngoặc vuông `[]`, ngoặc nhọn `{}`, dấu bằng `=`, dấu hai chấm `:`, hoặc `<br/>` phải bọc text bên trong bằng dấu ngoặc kép:
     - Node chữ nhật: `ID["Nhãn chi tiết (VPC CIDR / 10.0.0.0/16)"]`
     - Node hình thoi (Decision): `MASK{"Cờ sensitive = true"}`
     - Node bo tròn: `ID("Nội dung text")` hoặc `ID(["Stadium text"])`
     - Node Database: `DB[("PostgreSQL Cluster (Primary)")]`
3. **Tuyệt đối không dùng ký tự Markdown thô (`**`, `` ` ``) trong nhãn Mermaid**: Mermaid không hỗ trợ parse markdown trong text nhãn thông thường; dùng chữ in hoa hoặc nhãn rõ ràng.

---

## 6. Chuẩn Hóa Bảng So Sánh & Bảng Thực Hành (Table Optimization Standards)

Mọi bảng Markdown trong bài viết phải đảm bảo tính co giãn linh hoạt (**Responsive Width 100%**), tối ưu hóa trải nghiệm đọc và **tuyệt đối không để xảy ra hiện tượng xuất hiện thanh cuộn ngang (horizontal scrollbar)** trên màn hình tiêu chuẩn:

### 6.1. Quy tắc Thiết Kế & Bố Cục Bảng (Layout & Structure)
1. **Giới hạn số lượng cột hợp lý**:
   - Bảng Hands-on Lab: **3 cột** (`Bước` :---: \| `Lệnh CLI / Cấu Hình` :--- \| `Mục Đích Thực Thi` :---).
   - Bảng so sánh tham số / cờ CLI: **3–4 cột** (`Tham Số` \| `Mặc Định` \| `Hành Vi Kỹ Thuật` \| `Khuyến Nghị`).
   - Bảng so sánh công cụ / giải pháp: **3–4 cột** (`Tiêu Chí` \| `Giải Pháp A` \| `Giải Pháp B` \| `Ghi Chú`).
2. **Căn lề cột chuẩn ngữ nghĩa**:
   - Cột số thứ tự / Badge / Icon: Căn giữa (`:---:`).
   - Cột tên tham số / Lệnh CLI / Khái niệm: Căn trái (`:---`).
   - Cột số liệu / Dung lượng / Thời gian: Căn phải (`---:`).
3. **Cột Thứ tự / Badge (First Column Auto-Fit)**:
   - Cột đầu tiên chứa số bước (`01`, `02`, ...) hoặc Badge phân loại luôn dùng Badge pill căn giữa `<span class="badge badge--primary">01</span>`. Cột này được CSS tự động ép gọn (`width: 1%; white-space: nowrap;`) để nhường tối đa 90%+ chiều rộng cho nội dung chi tiết.

### 6.2. Kích Thước Chữ & Tối Ưu Nội Dung Ô (Compact Typography & Text Wrapping)
1. **Typography nhỏ gọn**: Font chữ bảng cỡ `0.8rem` (~12.8px - 13px), header `0.775rem` in hoa nhẹ nhàng, padding ô `0.55rem 0.7rem` chống dãn khung.
2. **Xử lý lệnh CLI & Thẻ `code` dài**:
   - Thẻ `code` trong ô bảng phải được định dạng tự động ngắt dòng mềm mại (`word-break: break-all`, `white-space: normal`).
   - Tuyệt đối không đặt code block nhiều dòng (fenced code block ` ``` `) bên trong ô bảng Markdown. Nếu lệnh quá phức tạp, chỉ ghi tóm tắt lệnh chính trong bảng và đặt code block chi tiết ngay bên dưới bảng.
3. **Cô đọng nội dung**: Mô tả trong ô bảng phải súc tích, trực diện, gạch bỏ các từ thừa, bôi đậm từ khóa kỹ thuật cốt lõi.

### 6.3. Bảng Mẫu Chuẩn Hands-on Lab:
```markdown
| Bước | Lệnh CLI | Mục Đích Thực Thi |
| :---: | :--- | :--- |
| <span class="badge badge--primary">01</span> | `terraform init -upgrade` | Tải Provider Plugins mới nhất và xác thực mã băm SHA-256 |
| <span class="badge badge--cyan">02</span> | `terraform plan -parallelism=5` | Tạo kế hoạch thực thi với mức độ song song kiểm soát an toàn |
| <span class="badge badge--emerald">03</span> | `terraform apply -auto-approve` | Áp dụng cấu hình hạ tầng trực tiếp lên môi trường đám mây |
```

### 6.4. Checklist Kiểm Tra Bảng Trước Khi Xuất Bản:
- [ ] Bảng có vừa khít 100% khung bài viết mà không sinh scrollbar ngang không?
- [ ] Các thẻ `code` chứa lệnh dài có xuống dòng tự nhiên không bị tràn ô không?
- [ ] Cột số bước có dùng badge pill `<span class="badge badge--...">` và căn giữa `:---:` không?
- [ ] Cột tiêu chí / lệnh có in đậm hoặc bọc backticks rõ ràng không?

---

## 7. Chuẩn Hóa Phân Tích Cạm Bẫy Thực Chiến (5-Whys Incident Analysis)

Mỗi bài viết phân tích sự cố phải bao gồm đủ 3 phần:
1. **Tình Huống Sự Cố Thực Tế**: Có timeline badge mốc thời gian rõ ràng (`<span class="badge badge--rose">🕒 02:00 AM</span>`).
2. **Hậu Quả & Log Lỗi Thực Tế**:
   - Sử dụng khối ````diff` để hiển thị trực quan các thay đổi: `+` (thêm/xanh), `-` (xóa/đỏ), `~` (sửa/vàng), `!` (lỗi nghiêm trọng).
   - Đi kèm sơ đồ Mermaid mô tả diễn biến sự cố từ nguyên nhân đến hậu quả gián đoạn dịch vụ.
3. **5-Whys Root Cause Analysis**:
   - Đánh số câu hỏi bằng badge: `1. <span class="badge badge--primary">Why 1</span> **Tại sao...?** $\rightarrow$ Lời giải.`
   - Biện pháp khắc phục: `5. <span class="badge badge--emerald">Root Cause Remedy</span> **Biện pháp khắc phục tận gốc:**` kèm các badge chính sách (`<span class="badge badge--rose">Enforce IaC-Only</span>`, `<span class="badge badge--cyan">Drift Detection</span>`, `<span class="badge badge--amber">Plan Review Gate</span>`).

---

## 8. Chuẩn Hóa 10 Câu Hỏi Tự Kiểm Tra (Self-Check Q&A Accordion)

Tất cả 10 câu hỏi trắc nghiệm / tự luận chuyên sâu ở cuối bài phải sử dụng component Accordion chuẩn thẻ HTML `<details class="qa-card">`:

```html
<details class="qa-card">
<summary class="qa-summary">
  <div class="qa-summary-left">
    <span class="qa-num-badge">Q01</span>
    <span>Câu hỏi chuyên sâu cần kiểm tra?</span>
  </div>
  <span class="qa-chevron">
    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
  </span>
</summary>
<div class="qa-answer">
  <div class="qa-answer-header">
    <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
    <span>Phân Tích &amp; Lời Giải Kỹ Thuật</span>
  </div>
  Lời giải thích chi tiết, ngắn gọn, có highlight các thuật ngữ chuyên môn trọng tâm bằng <b style="color: var(--accent-primary);">Màu Sắc Nhận Diện</b> và mã nguồn trong thẻ <code>inline code</code>.
</div>
</details>
```

- **Quy tắc chuyển đổi Markdown bên trong khối HTML (`<div class="qa-answer">`)**:
  - Do Jekyll/Kramdown không tự động parse cú pháp Markdown bên trong các block thẻ HTML thuần (`<div>`, `<details>`), **tất cả nội dung bên trong `<div class="qa-answer">` và `<summary>` PHẢI được chuyển đổi hoàn toàn sang HTML chuẩn**:
    - `**chữ in đậm**` $\rightarrow$ `<b style="color: var(--accent-primary);">chữ in đậm</b>` hoặc `<strong>chữ in đậm</strong>`.
    - `` `mã nguồn inline` `` $\rightarrow$ `<code>mã nguồn inline</code>`.
    - `- Danh sách bullet` hoặc `1. Thứ tự` $\rightarrow$ chuyển đổi thành các khối `<div style="margin-bottom: 8px; padding-left: 12px; border-left: 2px solid var(--accent-primary);">...</div>` hoặc thẻ `<ul>`/`<ol>` chuẩn HTML.
  - **Tuyệt đối KHÔNG để sót cú pháp Markdown thô** (như `**...**`, `` `...` ``, `- `) vì sẽ hiển thị nguyên văn chuỗi thô ra ngoài trang web gây mất thẩm mỹ.
  - **Làm sạch ký tự**: Loại bỏ dấu hai chấm dính liền thừa (`: `) ngay sau thẻ đóng `</span>` hoặc `</div>` trong tiêu đề / tóm tắt câu hỏi.

---

## 9. Chuẩn Hóa Khối Mã Nguồn (Code Blocks)

- **Định danh ngôn ngữ**: Mọi code block đều phải khai báo định danh ngôn ngữ (`hcl`, `bash`, `yaml`, `diff`, `json`, `python`, `typescript`).
- **Header và Nút Thao Tác (Wrap & Copy Buttons)**:
  - Tất cả các khối code block đều tự động được gắn thanh tiêu đề hiển thị macOS Dots, tên ngôn ngữ (`HCL`, `BASH`, `YAML`...) và nhóm nút điều khiển (`Wrap` và `Copy`).
  - **Mặc định Word Wrap (BẬT)**: Toàn bộ code block được kích hoạt chế độ **tự động xuống dòng mềm mại (`white-space: pre-wrap`)** để người đọc có thể theo dõi trọn vẹn source code mà không cần phải cuộn ngang (scrollbar). Người dùng có thể bấm nút `Wrap` trên thanh header để chuyển qua lại giữa chế độ Wrap và Scroll mode truyền thống.
- **Header chú thích tệp**: Các file cấu hình lớn phải có header chú thích tệp rõ ràng:
  ```hcl
  # ==============================================================================
  # File: main.tf - Mô tả chức năng tệp
  # ==============================================================================
  ```
- **Line-by-Line Breakdown**: Khối giải thích code từng dòng phải gắn badge cho từng tham số quan trọng: `<span class="badge badge--rose"><code>prevent_destroy = true</code></span>`.
