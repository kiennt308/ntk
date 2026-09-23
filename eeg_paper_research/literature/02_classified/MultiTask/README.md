# Phân Hệ Tài Liệu: Học Đa Nhiệm Vụ trong Tính Toán Cảm Xúc (Multi-Task Learning)

## 1. Bản Chất Học Đa Nhiệm Vụ Trong Tính Toán Cảm Xúc
- **Không gian cảm xúc đa chiều (Russell's Circumplex Model)**: Cảm xúc con người không tồn tại đơn lẻ mà biểu hiện đồng thời trên các chiều liên tục: **Valence** (Hài lòng - Tiêu cực), **Arousal** (Kích động - Bình tĩnh), và **Dominance** (Kiểm soát - Phụ thuộc).
- **Lợi ích của Multi-Task Learning (MTL)**:
  - Chia sẻ biểu diễn chung (Shared Representation Learning) giữa các nhiệm vụ giúp tăng tính khái quát hóa và giảm hiện tượng Overfitting.
  - Học đồng thời các nhiệm vụ phụ trợ (Auxiliary Tasks): Phân biệt đối tượng (Subject ID Invariance), Nhận diện trạng thái căng thẳng (Stress Detection), hoặc Tái tạo tín hiệu (Signal Reconstruction).

## 2. Kỹ Thuật Tối Ưu Hóa Hàm Mất Mát Đa Nhiệm Tiên Tiến
1. **Kendall Homoscedastic Aleatoric Uncertainty Loss**: Tự động học trọng số $\sigma_i^2$ dựa trên độ bất định nội tại của từng nhiệm vụ:
   $$\mathcal{L}_{MTL} = \frac{1}{2\sigma_v^2}\mathcal{L}_v + \frac{1}{2\sigma_a^2}\mathcal{L}_a + \frac{1}{2\sigma_d^2}\mathcal{L}_d + \log(\sigma_v \sigma_a \sigma_d)$$
2. **GradNorm (Gradient Normalization)**: Tự động cân bằng tốc độ học giữa các task heads, triệt tiêu xung đột gradient (Gradient Interference / Negative Transfer).

## 3. Tài Liệu Tham Khảo
- [`kw02_multitask_learning_affect`](../open_access_repository/kw02_multitask_learning_affect/README.md): 43 bài báo chuyên sâu.
- Các bài báo nền tảng: `P0001`, `P0007`, `P0011`, `P0015` trong thư mục [`03_notes/`](../03_notes/).
