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

## 5. Chuẩn Hóa Sơ Đồ Kiến Trúc Mermaid

Mọi sơ đồ Mermaid phải tuân thủ các quy tắc sau:
1. **Khối không dùng màu nền đặc**: Luôn dùng `fill:none` kết hợp viền màu kỹ thuật (`stroke:#...`, `stroke-width:1.5px` hoặc `2px`) để hiển thị sắc nét trên cả giao diện sáng lẫn tối và hỗ trợ chuẩn khi phóng to trong Lightbox.
2. **Phân nhóm bằng Subgraph**: Đặt tên subgraph trực quan, có đánh số thứ tự (ví dụ `subgraph Inputs["1. ĐẦU VÀO HỆ THỐNG"]`).
3. **Ngắt dòng thông minh**: Dùng `<br/>` để chia text trong các khối dài thành 2–3 dòng gọn gàng, tránh làm khối bị quá dài theo chiều ngang.
4. **Màu viền quy ước**:
   - Đầu vào / HCL: `#6366f1` (Indigo/Primary)
   - Lưu trữ / State: `#f59e0b` (Amber)
   - Cloud / Thực tế: `#0ea5e9` (Cyan)
   - Engine tính toán: `#3b82f6` (Blue)
   - Kế hoạch / Plan: `#f59e0b` (Amber)
   - Thực thi / Thành công: `#10b981` (Emerald)
   - Lỗi / Sự cố: `#f43f5e` hoặc `#dc2626` (Rose/Red)

---

## 6. Chuẩn Hóa Bảng So Sánh & Bảng Thực Hành (Tables)

1. **Bảng so sánh kỹ thuật**:
   - Đặt tên cột rõ ràng: `| Tiêu Chí Kỹ Thuật | Công Cụ A | Công Cụ B | ... |`
   - Cột tiêu chí dùng in đậm: `**Tiêu chí**`
   - Các từ khóa giá trị dùng Code span hoặc in đậm có màu.
2. **Bảng Hands-on Lab (Các bước thực hành)**:
   - Cột bước đánh số bằng Badge pill căn giữa:
     `| <span class="badge badge--primary">01</span> | \`lenh-cli\` | Mục đích thực thi chi tiết |`

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
  Lời giải thích chi tiết, ngắn gọn, có highlight các thuật ngữ chuyên môn trọng tâm bằng <b style="color: var(--accent-primary);">Màu Sắc Nhận Diện</b>.
</div>
</details>
```

---

## 9. Chuẩn Hóa Khối Mã Nguồn (Code Blocks)

- Mọi code block đều phải khai báo định danh ngôn ngữ (`hcl`, `bash`, `yaml`, `diff`, `json`, `python`, `typescript`).
- Các file cấu hình lớn phải có header chú thích tệp rõ ràng:
  ```hcl
  # ==============================================================================
  # File: main.tf - Mô tả chức năng tệp
  # ==============================================================================
  ```
- Khối giải thích code từng dòng (`Line-by-Line Breakdown`) phải gắn badge cho từng tham số quan trọng: `<span class="badge badge--rose"><code>prevent_destroy = true</code></span>`.
