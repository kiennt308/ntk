# Khối 2: Cơ Chế Dung Hợp & Chú Ý Chéo (Cross-Modal Attention)

## 1. Công Thức Chú Ý Chéo (Cross-Modal Attention Formula)
$$Attention(Q_{EEG}, K_{Bio}, V_{Bio}) = \text{softmax}\left(\frac{Q_{EEG} K_{Bio}^T}{\sqrt{d_k}}\right) V_{Bio}$$
Trong đó:
- $Q_{EEG}$ đóng vai trò truy vấn trạng thái thần kinh trung ương.
- $K_{Bio}, V_{Bio}$ cung cấp ngữ cảnh phản ứng thần kinh tự chủ (nhịp tim, đáp ứng da).

## 2. Dung Hợp Tương Tác Hai Chiều (Bi-directional Cross-Attention)
Đồng thời tính toán chiều ngược lại $Attention(Q_{Bio}, K_{EEG}, V_{EEG})$ để đảm bảo thông tin ngoại vi có thể tinh chỉnh lại đặc trưng vỏ não trước khi đưa vào bộ phân loại.
