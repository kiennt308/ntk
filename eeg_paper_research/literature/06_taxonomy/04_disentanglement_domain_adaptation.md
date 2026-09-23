# Khối 4: Tách Không Gian Con & Thích Ứng Miền (Disentanglement & Domain Adaptation)

## 1. Mô Hình Tách Biểu Diễn (Shared-Private Subspace Disentanglement)
- $Z_{shared}$: Mang thông tin cảm xúc dùng chung giữa các đối tượng (Subject-Invariant Affective Features).
- $Z_{private}$: Mang thông tin đặc thù của từng cá nhân (Subject Identity / Baseline Physiology).
- **Ràng buộc trực giao (Orthogonality Constraint)**: $\mathcal{L}_{diff} = || Z_{shared}^T Z_{private} ||_F^2$ triệt tiêu tương quan giữa 2 không gian con.

## 2. Thích Ứng Miền Đối Kháng (DANN / Adversarial Domain Adaptation)
Sử dụng Gradient Reversal Layer (GRL) và bộ phân biệt đối tượng (Subject Discriminator) để huấn luyện Backbone trích xuất đặc trưng cảm xúc mà bộ phân biệt không thể đoán được đối tượng nào.
