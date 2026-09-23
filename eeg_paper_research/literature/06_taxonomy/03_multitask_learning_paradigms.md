# Khối 3: Khung Học Đa Nhiệm Vụ (Multi-Task Learning)

## 1. Hàm Mất Mát Đa Nhiệm Tổng Quát (Total Multi-Task Objective)
$$\mathcal{L}_{total} = w_v \mathcal{L}_{valence} + w_a \mathcal{L}_{arousal} + w_d \mathcal{L}_{dominance} + \lambda_{reg} \mathcal{L}_{auxiliary}$$

## 2. Kỹ Thuật Cân Bằng Gradient Tự Động (Dynamic Weighting)
- **Uncertainty Weighting (Kendall et al.)**: Điều chỉnh trọng số $w_i = \frac{1}{2\sigma_i^2}$ theo phương sai bất định của từng nhiệm vụ.
- **GradNorm**: Chuẩn hóa độ lớn gradient của các task heads về cùng một quy mô để tránh một nhiệm vụ áp đảo quá trình cập nhật Shared Backbone.
