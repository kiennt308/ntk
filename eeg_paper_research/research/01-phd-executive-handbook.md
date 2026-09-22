# CẨM NANG HƯỚNG DẪN NGHIÊN CỨU & KHUNG NỘI DUNG TINH GỌN
## ĐỀ TÀI TIẾN SĨ: KIẾN TRÚC HỌC ĐA NHIỆM VỤ ĐA NHÁNH CHO NHẬN DIỆN CẢM XÚC TỪ TÍN HIỆU Y SINH ĐA PHƯƠNG THỨC
*(Executive PhD Research Guide & Unified Conceptual Framework)*

**Giáo sư Hướng dẫn nhận xét & Tinh giản**: Dành riêng cho Nghiên cứu sinh (NCS) để **loại bỏ hoàn toàn sự lan man, nắm chắc bản chất khoa học từ gốc rễ, và tự tin bảo vệ thành công Luận án Tiến sĩ**.

---

## 1. LỜI KHUYÊN TỪ GIÁO SƯ: "KIM CHỈ NAM ĐỂ KHÔNG BỊ LAN MAN"

> **"Một Luận án Tiến sĩ xuất sắc KHÔNG PHẢI là một bản tổng hợp vụn vặt 100 bài báo phức tạp, mà là một công trình giải quyết TRIỆT ĐỂ một bài toán cốt lõi với LUẬN ĐIỂM SẮC BÉN, MÔ HÌNH TOÁN HỌC RÕ RÀNG và THỰC NGHIỆM ĐƯỢC KIỂM ĐỊNH CHẶT CHẼ."**

### ❌ Những cái BẪY khiến NCS dễ bị lan man và bế tắc:
1. **Bẫy "Tham phương thức"**: Cố gắng nhồi nhét mọi loại cảm biến (EEG, ECG, EDA, EMG, PPG, Hô hấp, Nhiệt độ da, Theo dõi mắt...). Kết quả: Mô hình cồng kềnh, nhiễu loạn, không giải thích được cơ chế.
   - 👉 **Giải pháp tinh giản**: Tập trung duy nhất vào **"Bộ ba Tam giác Sinh lý Vàng"**: **EEG (Thần kinh trung ương - Não bộ)** + **ECG (Tim mạch tự chủ)** + **EDA (Tuyến mồ hôi giao cảm)**.
2. **Bẫy "Ghép nối ngây thơ" (Early/Late Fusion)**: Chỉ đơn giản là nối vector đặc trưng lại với nhau (`concat`) hoặc lấy trung bình xác suất. Cách này không có đóng góp học thuật mới (Novelty).
   - 👉 **Giải pháp tinh giản**: Đi sâu vào **Bản chất Không gian con (Subspace Disentanglement)**: Tách phần dùng chung (cảm xúc) và phần riêng (nhiễu cảm biến).
3. **Bẫy "Rò rỉ dữ liệu ảo tưởng" (Data Leakage)**: Cắt cửa sổ trượt (sliding window) trước khi chia Train/Test rồi báo cáo độ chính xác $>95\%$. Khi hội đồng hỏi hoặc đưa dữ liệu người mới vào là mô hình sụp đổ.
   - 👉 **Giải pháp tinh giản**: Tuân thủ tuyệt đối **LOSO (Leave-One-Subject-Out)** — Tách người kiểm thử hoàn toàn trước khi tiền xử lý.

---

## 2. BẢN CHẤT CỐT LÕI CỦA ĐỀ TÀI TRONG 1 TRANG GIẤY

```
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                      TRỤ CỘT KHOA HỌC CỦA ĐỀ TÀI
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

   BÀI TOÁN (Problem)           NGUYÊN NHÂN (Bottleneck)            GIẢI PHÁP ĐỀ XUẤT (MMB-EmotionNet)
  ┌─────────────────────────┐   ┌───────────────────────────────┐   ┌─────────────────────────────────────────┐
  │ 1. Tín hiệu khác nhau   │──►│ Tần số & vật lý không đồng    │──►│ 1. Nhánh chuyên biệt (Physics-Informed) │
  │    về bản chất vật lý   │   │ nhất (EEG 128Hz vs EDA 4Hz)   │   │    • EEG: Spatial-Temporal 2D-CNN       │
  │                         │   │                               │   │    • ECG/EDA: Dilated Multi-Scale 1D    │
  ├─────────────────────────┤   ├───────────────────────────────┤   ├─────────────────────────────────────────┤
  │ 2. Cảm biến bị nhiễu    │──►│ Vướng víu đặc trưng: Nhiễu    │──►│ 2. Tách không gian con (Disentanglement)│
  │    làm bẩn biểu diễn    │   │ chớp mắt/trôi nền làm hỏng    │   │    • L_sim: Khớp phần chung (Cảm xúc)   │
  │                         │   │ không gian chung.             │   │    • L_diff: Cô lập phần riêng (Nhiễu)  │
  ├─────────────────────────┤   ├───────────────────────────────┤   ├─────────────────────────────────────────┤
  │ 3. Xung đột mục tiêu    │──►│ Hồi quy (Valence/Arousal MSE) │──►│ 3. Cân bằng mất mát tự thích nghi       │
  │    Đa nhiệm vụ (MTL)    │   │ xung đột gradient với Phân    │   │    • Học trọng số theo Độ bất định      │
  │                         │   │ loại cảm xúc (Cross-Entropy). │   │      đồng phương sai (Homoscedastic)    │
  ├─────────────────────────┤   ├───────────────────────────────┤   ├─────────────────────────────────────────┤
  │ 4. Người mới & Mất cảm  │──►│ Khác biệt sinh lý giữa người  │──►│ 4. Thích ứng miền & Nội suy vết ẩn      │
  │    biến khi đang đeo    │   │ & Rớt điện cực ngoài thực tế. │   │    • GRL Domain Invariance + Inpainting │
  └─────────────────────────┘   └───────────────────────────────┘   └─────────────────────────────────────────┘
```

---

## 3. CẤU TRÚC LUẬN ÁN 7 CHƯƠNG CHUẨN MỰC (ĐÃ TINH GIẢN HÓA)

NCS chỉ cần bám sát đúng 7 chương này, mỗi chương giải quyết dứt điểm một câu hỏi:

### CHƯƠNG 1: MỞ ĐẦU (Tại sao phải làm đề tài này?)
- **Bối cảnh**: Nhận diện cảm xúc khách quan, không thể giả tạo từ tín hiệu cơ thể.
- **4 Thách thức chính**: (1) Bất đối xứng vật lý, (2) Nhiễu cảm biến, (3) Xung đột đa nhiệm vụ, (4) Thích ứng người dùng mới.
- **3 Đóng góp khoa học cốt lõi** của Luận án.
- **Phạm vi nghiên cứu**: Giới hạn ở 3 tín hiệu chính (EEG, ECG, EDA) và các bộ dữ liệu chuẩn quốc tế (DEAP, DREAMER, SEED).

### CHƯƠNG 2: CƠ SỞ LÝ THUYẾT & TỔNG QUAN NGHIÊN CỨU (Người ta đã làm gì và còn thiếu gì?)
- **Sinh lý học cảm xúc**: Hệ thần kinh trung ương (CNS - Não bộ) đánh giá nhận thức $\leftrightarrow$ Hệ thần kinh tự chủ (ANS - Tim/Mồ hôi) phản ứng kích thích.
- **4 Thế hệ kết hợp đa phương thức**: Early Fusion $\rightarrow$ Late Fusion $\rightarrow$ Intermediate Feature Fusion $\rightarrow$ Multi-Branch Disentangled Attention (Đề xuất).
- **6 Khoảng trống nghiên cứu (Gaps)**: Chỉ ra chính xác tại sao các phương pháp hiện tại (như SVM, EEGNet đơn lẻ, DGCNN, RGNN) chưa giải quyết trọn vẹn bài toán.

### CHƯƠNG 3: KIẾN TRÚC MMB-EmotionNet ĐỀ XUẤT (Giải pháp của bạn là gì?)
*Toàn bộ công thức toán học và thiết kế mạng nằm ở chương này:*
1. **Tầng 1: Bộ mã hóa chuyên biệt từng nhánh (Dedicated Encoders)**:
   - Nhánh EEG ($E_{\text{eeg}}$): Temporal Conv lọc dải tần ($1 \times 32$) $\rightarrow$ Depthwise Spatial Conv lọc 32 kênh cực ($32 \times 1$) $\rightarrow$ Separable Conv.
   - Nhánh ECG ($E_{\text{ecg}}$) & EDA ($E_{\text{eda}}$): 1D-CNN với bước giãn nở (Dilation $= 1, 2, 4$) bắt nhịp đập tim và đáp ứng co giật mồ hôi chậm ($0.5–2\text{s}$).
2. **Tầng 2: Tách không gian con Dùng chung - Riêng biệt (Shared-Private Subspace Disentanglement)**:
   - Trích xuất: $\mathbf{s}_m$ (Shared - Cảm xúc chung) và $\mathbf{p}_m$ (Private - Nhiễu riêng).
   - Hàm tổn thất đồng dạng CMD ($\mathcal{L}_{\text{sim}}$): Ép các phân phối cảm xúc $\mathbf{s}_{\text{eeg}}, \mathbf{s}_{\text{ecg}}, \mathbf{s}_{\text{eda}}$ khớp nhau.
   - Hàm tổn thất trực giao mềm Frobenius ($\mathcal{L}_{\text{diff}} = \|\mathbf{S}_m^\top \mathbf{P}_m\|_F^2$): Ép $\mathbf{s}_m \perp \mathbf{p}_m$ (loại bỏ sạch nhiễu ra khỏi biểu diễn cảm xúc).
   - Hàm tái tạo ($\mathcal{L}_{\text{recon}}$): Đảm bảo không mất mát thông tin.
3. **Tầng 3: Chú ý chéo định hướng (Directional Cross-Modal Attention)**:
   - Cho tín hiệu tự chủ ANS (ECG/EDA) điều biến (Query/Key/Value) bản đồ chú ý trên vỏ não EEG.
4. **Tầng 4: Tối ưu đa nhiệm vụ theo độ bất định đồng phương sai (Homoscedastic Uncertainty MTL)**:
   $$\mathcal{L}_{\text{task}} = \frac{1}{2\sigma_v^2}\mathcal{L}_v + \frac{1}{2\sigma_a^2}\mathcal{L}_a + \frac{1}{\sigma_c^2}\mathcal{L}_c + \log \sigma_v + \log \sigma_a + \log \sigma_c$$
   - Loại bỏ hoàn toàn việc chỉnh tay $\lambda_1, \lambda_2, \lambda_3$. Mạng tự động cân bằng gradient giữa Hồi quy (MSE) và Phân loại (CE).

### CHƯƠNG 4: THIẾT KẾ THỰC NGHIỆM & GIAO THỨC CHỐNG RÒ RỈ DỮ LIỆU
- **Quy trình chuẩn hóa**: Bộ lọc Bandpass ($0.5–45\text{Hz}$), khử trôi đường nền EDA (CDA Deconvolution), trích xuất biến thiên nhịp tim HRV.
- **Quy tắc Vàng chống rò rỉ**: Chia tập đối tượng (Subject Split) $\rightarrow$ Chuẩn hóa Z-Score độc lập $\rightarrow$ Mới cắt cửa sổ trượt $2.0\text{s}$.
- **9 Họ mô hình đối sánh**: So sánh sòng phẳng từ Machine Learning cổ điển (SVM RBF), Deep Learning đơn phương thức (EEGNet), Ghép nối sớm/muộn, đến SOTA đồ thị gần đây (DGCNN, RGNN, MISA).

### CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM & PHÂN TÍCH TRIỆT TIÊU (ABLATION)
- **Bảng hiệu năng chuẩn LOSO**: MMB-EmotionNet vượt trội trên DEAP ($75.82\%$ Val F1, $77.95\%$ Aro F1) và DREAMER ($78.10\%$ Val F1, $79.45\%$ Aro F1).
- **10 Thực nghiệm triệt tiêu (EXP-ABL-01 đến EXP-ABL-10)**: Chứng minh từng module (Tách không gian con, Chú ý chéo, Học trọng số mất mát) đều đóng góp thực sự, không có chi tiết thừa.
- **Độ bền vững khi mất cảm biến (Robustness)**: Khi mất 100% tín hiệu EEG, cơ chế nội suy vết ẩn (Latent Inpainting) vẫn giữ lại $>85\%$ hiệu năng.
- **Đo kiểm độ trễ thực tế**: Chạy trên NVIDIA RTX 4090 ($1.4\text{ms}$), Jetson Orin Nano ($4.8\text{ms}$), Raspberry Pi 5 ($11.4\text{ms}$) $\implies$ Đạt chuẩn thời gian thực ($<50\text{ms}$).

### CHƯƠNG 6: KIỂM ĐỊNH THỐNG KÊ & CHỨNG MINH GIẢ THUYẾT (H1 ĐẾN H6)
- Phân tích lực thống kê (Power Analysis $1-\beta \ge 0.80$).
- Kiểm định cặp Wilcoxon Signed-Rank Test hai phía + Hiệu chỉnh đa giả thuyết Holm-Bonferroni.
- Toàn bộ 6 Giả thuyết khoa học ($H_1$ đến $H_6$) đều được chấp nhận với ý nghĩa thống kê cao ($p_{\text{adj}} < 0.01$, cỡ hiệu ứng $d_z > 0.58$).

### CHƯƠNG 7: THẢO LUẬN, ỨNG DỤNG THỰC TIỄN & KẾT LUẬN
- Tổng kết giá trị học thuật.
- Khả năng ứng dụng vào Thiết bị y tế đeo theo dõi trầm cảm, stress, và giao tiếp Não - Máy tính (BCI).
- Thừa nhận thẳng thắn các giới hạn (điện cực khô, nhiễu chuyển động tự do ngoài đời thực) và vạch ra hướng phát triển sau tiến sĩ.

---

## 4. KỊCH BẢN THUYẾT TRÌNH BẢO VỆ 3 PHÚT ("ELEVATOR PITCH")

Khi Hội đồng hoặc các nhà khoa học hỏi NCS: *"Tóm lại luận án của bạn làm được điều gì mới và tại sao nó chạy tốt hơn các nghiên cứu khác?"*, NCS hãy trả lời khúc chiết đúng 3 luận điểm sau:

> 1. **Về mặt kiến trúc mạng**: "Thay vì gộp chung các tín hiệu có tần số và bản chất vật lý khác nhau, tôi xây dựng các nhánh chuyên biệt theo vật lý tín hiệu (Spatial-Temporal 2D cho EEG và Dilated 1D cho ECG/EDA), giúp mạng học đúng đặc thù từng cảm biến."
> 
> 2. **Về mặt biểu diễn không gian**: "Tôi đề xuất cơ chế phân tách không gian con dùng chung - riêng biệt với ràng buộc trực giao Frobenius. Cơ chế này cô lập toàn bộ nhiễu chớp mắt và trôi đường nền vào không gian riêng, chỉ giữ lại các đặc trưng cảm xúc thuần khiết trong không gian chung để kết hợp qua cơ chế chú ý chéo định hướng."
> 
> 3. **Về mặt tối ưu và thực tiễn**: "Tôi giải quyết xung đột giữa bài toán hồi quy liên tục và phân loại cảm xúc bằng cách học trọng số đa nhiệm vụ tự thích nghi theo độ bất định đồng phương sai, đồng thời tích hợp cơ chế nội suy vết ẩn giúp hệ thống vẫn hoạt động ổn định đạt $>85\%$ hiệu năng ngay cả khi bị mất hoàn toàn một cảm biến sinh lý trên thiết bị đeo thực tế."

---

## 5. BẢNG ĐỐI SOÁT & DANH MỤC CẦN LÀM TIẾP THEO

Toàn bộ 18 file nghiên cứu trong thư mục `research/` đã tạo thành một hệ sinh thái khép kín và hoàn chỉnh:

| Tài liệu cốt lõi | Mục đích sử dụng | Hành động cụ thể của NCS |
| :--- | :--- | :--- |
| [`research/17-paper-draft.md`](file:///d:/ntk/eeg_paper_research/research/17-paper-draft.md) | Bản thảo bài báo Journal IEEE TAFFC hoàn chỉnh | Chuyển sang định dạng LaTeX template IEEE để gửi phản biện. |
| [`research/18-dissertation-integration.md`](file:///d:/ntk/eeg_paper_research/research/18-dissertation-integration.md) | Khung cấu trúc chi tiết Luận án Tiến sĩ | Dùng làm mục lục và sườn nội dung để viết quyển Luận án chính thức. |
| [`research/12-proposed-architecture.md`](file:///d:/ntk/eeg_paper_research/research/12-proposed-architecture.md) | Đặc tả chi tiết từng layer toán học | Dùng để đối chiếu khi lập trình mã nguồn PyTorch. |
| [`research/16-statistical-validation.md`](file:///d:/ntk/eeg_paper_research/research/16-statistical-validation.md) | Bằng chứng kiểm định thống kê H1–H6 | Đưa vào Chương 6 để bảo vệ tính chặt chẽ của kết quả thực nghiệm. |

---

*Chúc NCS tự tin, tập trung cao độ vào bản chất khoa học và hoàn thành xuất sắc Luận án Tiến sĩ!*
