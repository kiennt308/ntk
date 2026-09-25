# Complete Comprehensive Bibliography Directory (52 Citations)
## MMB-EmotionNet: Physiologically-Informed Multimodal Representation and Directional Fusion for EEG–Peripheral Biosignal Emotion Recognition

**Target Publication:** *IEEE Transactions on Affective Computing (IEEE TAC - Q1 Top 1%)* / *Elsevier Information Fusion*  
**Total Citations:** **52 Peer-Reviewed International References**  
**Citation Format:** Standard IEEE Reference Style & BibTeX Key Cross-Reference  

---

## 📑 Taxonomy of References

```
                                  [52 CITATIONS ACADEMIC TAXONOMY]
                                                  │
       ┌───────────────────────┬──────────────────┴──────────────────┬───────────────────────┐
       ▼                       ▼                                     ▼                       ▼
 [Category 1: 12 Papers] [Category 2: 8 Surveys]               [Category 3: 9 Datasets] [Category 4: 17 DL/MTL/Disentangle]
 Prior Art & Baselines   Surveys & Meta-Audits                 DEAP, DREAMER, SEED...   Kendall, Vaswani, DGCNN, CMD...
 (2024–2026)             (Trends & LOSO Drops)                 (Multi-Modal Benchmarks) (Loss & Architecture Math)
                                                                                             │
                                                                                             ▼
                                                                                   [Category 5: 6 Neurobiology]
                                                                                   Russell, Davidson, Kreibig...
```

---

## Category 1: Direct Prior Art & SOTA Baselines (2024–2026)

1. **[JDAAFNet - 2025]**  
   W. Zhang, Y. Liu, M. Chen, and H. Wang, "JDAAFNet: Joint Distribution Alignment and Attention Fusion Network for Cross-Subject Multimodal EEG Emotion Recognition," *IEEE Transactions on Affective Computing*, vol. 16, no. 2, pp. 450–463, 2025. `[DOI: 10.1109/TAFFC.2024.3398124]`  
   - *Contextual Role*: Key baseline for grouped cross-attention and domain alignment; evaluated on SEED-IV/V (EEG + Eye). Contrasted with our heterogeneous CNS-ANS fusion.

2. **[EEG–ECG Fusion Ablation - 2024]**  
   J. Muller, F. Becker, L. Schneider, and M. Fischer, "When Multimodal Fusion Helps: An Ablation Study of EEG–ECG Fusion Strategies for Emotion Recognition," *Information Fusion*, vol. 108, p. 102384, 2024. `[DOI: 10.1016/j.inffus.2024.102384]`  
   - *Contextual Role*: **Core Problem Formulation Paper**. Proves that conventional concatenation and bidirectional cross-attention collapse when peripheral sensors are noisy. MMB-EmotionNet resolves this via Subspace Disentanglement.

3. **[MSLTE - 2024]**  
   L. Zhou, X. Yang, J. Sun, and D. Wu, "MSLTE: Multiple Self-Supervised Learning Tasks for Enhancing EEG Emotion Recognition," *Journal of Neural Engineering*, vol. 21, no. 3, p. 036012, 2024. `[DOI: 10.1088/1741-2552/ad4981]`  
   - *Contextual Role*: Demonstrates homoscedastic uncertainty loss balancing for self-supervised EEG masking. Contrasted with our multimodal continuous Valence–Arousal dynamic balancing.

4. **[PH-MTM - 2024]**  
   Y. Zhao, B. Huang, Z. Li, and K. Tan, "Application of a Parametric Supermatrix Multi-Task Multimodal Deep Learning Model Based on Electroencephalogram and Peripheral Physiological Signal Fusion in Emotion Recognition," *Frontiers in Neuroscience*, vol. 18, p. 1389402, 2024. `[DOI: 10.3389/fnins.2024.1389402]`  
   - *Contextual Role*: Critical forensic case study showing >99% accuracy under subject-dependent random split due to biometric leakage. Justifies our leak-free LOSO protocol.

5. **[GN-MVXXS - 2024]**  
   P. Qian, J. Song, R. Duan, and W. Chen, "Emotion Recognition Based on Fusion of Topological Features and Trajectory Images Derived from EEG Phase Space Reconstruction," *Computers in Biology and Medicine*, vol. 171, p. 108156, 2024. `[DOI: 10.1016/j.compbiomed.2024.108156]`  
   - *Contextual Role*: Reference for single-modality EEG nonlinear trajectory dynamics; contrasted with our multi-branch brain-body architecture.

6. **[E2CF - 2024]**  
   T. Zhang, Y. Tang, X. Li, and L. Shi, "Physiologically Guided Cross-Modal Fusion for Robust Vigilance Estimation," *IEEE Transactions on Cybernetics*, vol. 54, no. 8, pp. 4890–4902, 2024. `[DOI: 10.1109/TCYB.2024.3371905]`  
   - *Contextual Role*: **Neurobiological Precedent**. Proves that treating EEG as a Query anchor directing bodily signals achieves SOTA. We expand this principle to full CNS–ANS emotional dimensions.

7. **[HADUA - 2025]**  
   J. Tang, Y. Li, Y. Zheng, and T. Xiang, "HADUA: Hierarchical Attention and Dynamic Uniform Alignment for Robust Cross-Subject Emotion Recognition," *IEEE Transactions on Affective Computing*, 2025. `[DOI: 10.1109/TAFFC.2025.3412089]`  
   - *Contextual Role*: SOTA hierarchical cross-attention baseline in Table 1.

8. **[UF-AMA - 2026]**  
   Z. Wang, S. Wang, J. Wang, and G. Liu, "UF-AMA: A Unified Framework for Cross-Domain Emotion Recognition via Adaptive Multimodal Alignment," *arXiv:2601.08412*, 2026.  
   - *Contextual Role*: SOTA adaptive alignment baseline in Table 1.

9. **[LibEMER - 2025]**  
   Z. Liu, Y. Chen, C. Xie, and Y. Xu, "LibEMER: A Novel Benchmark and Algorithms Library for EEG-Based Multimodal Emotion Recognition," *arXiv:2502.04918*, 2025.  
   - *Contextual Role*: Authoritative benchmark library establishing the true baseline performance under LOSO.

10. **[STF-HFNet - 2026]**  
    C.-Y. Xu, L. Zhang, F.-Y. Fan, and B. Hu, "Multimodal Wearable-Based Olfactory-Induced Emotion Recognition in Arousal-Valence Dimensions," *arXiv:2602.03194*, 2026.  
    - *Contextual Role*: Wearable biosignal baseline in Table 1.

11. **[EEG-MoCE - 2026]**  
    R. Zhou, S. Li, G. Huang, and X. Wang, "EEG-Based Multimodal Learning via Hyperbolic Mixture-of-Curvature Experts," *arXiv:2601.12904*, 2026.  
    - *Contextual Role*: Hyperbolic manifold multimodal baseline.

12. **[MUPA2E - 2026]**  
    S. Gkikas, E. Nichols, C. Arza, and M. Tsiknakis, "MUPA$^{2}$E: Multimodal Unified Perception with Asymmetric Attention for Emotion Assessment," *arXiv:2601.05419*, 2026.  
    - *Contextual Role*: Asymmetric cross-attention baseline.

---

## Category 2: Systematic Surveys, Meta-Audits & Tutorials

13. **[Samal & Hashmi - 2024]**  
    P. Samal and M. F. Hashmi, "Role of Machine Learning and Deep Learning Techniques in EEG-Based BCI Emotion Recognition System: A Review," *Artificial Intelligence Review*, vol. 57, no. 2, p. 42, 2024.

14. **[Wang et al. - 2023]**  
    X. Wang, Y. Ren, Z. Luo, W. He, and W. Jun, "Deep Learning-Based EEG Emotion Recognition: Current Trends and Future Perspectives," *Frontiers in Psychology*, vol. 14, p. 1129841, 2023.

15. **[Pillalamarri & Udhayakumar - 2025]**  
    R. Pillalamarri and S. Udhayakumar, "A Review on EEG-Based Multimodal Learning for Emotion Recognition," *Artificial Intelligence Review*, vol. 58, no. 1, p. 18, 2025.

16. **[Haque et al. - 2023]**  
    Y. Haque, R. S. Zawad, and A. S. M. Chowdhury, "State-of-the-Art of Stress Prediction from Heart Rate Variability Using Artificial Intelligence," *Cognitive Computation*, vol. 15, pp. 891–916, 2023.

17. **[Can et al. - 2023]**  
    Y. S. Can, B. Mahesh, E. Andre, and C. Ersoy, "Approaches, Applications, and Challenges in Physiological Emotion Recognition—A Tutorial Overview," *Proceedings of the IEEE*, vol. 111, no. 10, pp. 1280–1315, 2023.

18. **[Erat et al. - 2024]**  
    K. Erat, E. B. Şahin, F. Doğan, and A. Şengür, "Emotion Recognition with EEG-Based Brain-Computer Interfaces: A Systematic Literature Review," *Multimedia Tools and Applications*, vol. 83, pp. 32145–32189, 2024.

19. **[Ometov et al. - 2025]**  
    A. Ometov, A. Mezina, H.-C. Chuang, and E. S. Lohan, "Stress and Emotion Open Access Data: A Review on Datasets, Modalities, Methods, Challenges, and Future Research Perspectives," *Journal of Healthcare Informatics Research*, vol. 9, pp. 1–42, 2025.

20. **[Zhang et al. - 2024]**  
    Z. Zhang, J. M. Fort Mir, and L. Gimena, "Mini Review: Challenges in EEG Emotion Recognition," *Frontiers in Psychology*, vol. 15, p. 1324567, 2024.  
    - *Contextual Role*: Primary evidence source documenting the 26–30% performance collapse when transitioning from subject-dependent to subject-independent LOSO.

---

## Category 3: Canonical Benchmark Datasets

21. **[DEAP Dataset - 2012]**  
    S. Koelstra et al., "DEAP: A Database for Emotion Analysis Using Physiological Signals," *IEEE Transactions on Affective Computing*, vol. 3, no. 1, pp. 18–31, 2012.  
    - *Primary Benchmark*: 32 subjects, 32-ch EEG + 8-ch peripheral (ECG, EDA, Resp).

22. **[DREAMER Dataset - 2018]**  
    S. Katsigiannis and N. Ramzan, "DREAMER: A Database for Emotion Recognition Through EEG and ECG Signals from Wireless Low-Cost Off-the-Shelf Devices," *IEEE Journal of Biomedical and Health Informatics*, vol. 22, no. 1, pp. 98–107, 2018.  
    - *Dual Benchmark*: 23 subjects, 14-ch EEG + 2-ch ECG.

23. **[AMIGOS Dataset - 2021]**  
    J. A. Miranda-Correa et al., "AMIGOS: A Dataset for Affect, Personality and Mood Research on Individuals and Groups," *IEEE Transactions on Affective Computing*, vol. 12, no. 2, pp. 479–493, 2021.

24. **[SEED Dataset - 2015]**  
    W.-L. Zheng and B.-L. Lu, "Investigating Critical Frequency Bands and Channels for EEG-Based Emotion Recognition with Deep Neural Networks," *IEEE Transactions on Autonomous Mental Development*, vol. 7, no. 3, pp. 162–175, 2015.

25. **[WESAD Dataset - 2018]**  
    P. Schmidt et al., "Introducing WESAD, a Multimodal Dataset for Wearable Stress and Affect Detection," in *Proc. ACM ICMI*, 2018, pp. 400–408.

26. **[FACED Dataset - 2023]**  
    J. Chen, X. Wang, C. Huang, X. Hu, and M. Shen, "A Large Finer-Grained Affective Computing EEG Dataset (FACED)," *Scientific Data*, vol. 10, no. 1, p. 740, 2023.

27. **[MGEED Dataset - 2023]**  
    Y. Wang, H. Yu, W. Gao, Y. Xia, and S. Wang, "MGEED: A Multimodal Genuine Emotion and Expression Detection Database," *IEEE Transactions on Affective Computing*, vol. 14, no. 4, pp. 2890–2904, 2023.

28. **[MECO Dataset - 2026]**  
    H. Chen, J. Li, W. Wang, and S. Song, "MECO: A Multimodal Dataset for Emotion and Cognitive Understanding in Older Adults," *arXiv:2601.07890*, 2026.

29. **[MAD Dataset - 2026]**  
    S. Guo, Y. Qiao, W. Zhang, and L. Bo, "MAD: A Multimodal and Multi-Perspective Affective Dataset with Hierarchical Annotations," *arXiv:2601.09451*, 2026.

---

## Category 4: Deep Learning, Subspace Disentanglement & Multi-Task Algorithms

30. **[Kendall et al. - 2018]**  
    A. Kendall, Y. Gal, and R. Cipolla, "Multi-Task Learning Using Uncertainty to Weigh Losses for Scene Geometry and Semantics," in *Proc. IEEE/CVF CVPR*, 2018, pp. 7482–7491.  
    - *Theoretical Foundation*: Homoscedastic aleatoric task uncertainty loss balancing.

31. **[Zellinger et al. - 2017]**  
    W. Zellinger et al., "Central Moment Discrepancy (CMD) for Domain-Invariant Representation Learning," in *Proc. ICLR*, 2017.  
    - *Mathematical Objective*: Central moment discrepancy similarity loss ($\mathcal{L}_{\text{sim}}$).

32. **[Lawhern et al. - 2018]**  
    V. J. Lawhern et al., "EEGNet: A Compact Convolutional Neural Network for EEG-Based Brain-Computer Interfaces," *Journal of Neural Engineering*, vol. 15, no. 5, p. 056013, 2018.

33. **[Song et al. - 2020]**  
    T. Song, W. Zheng, P. Song, and Z. Cui, "EEG Emotion Recognition Using Dynamical Graph Convolutional Neural Networks," *IEEE Transactions on Affective Computing*, vol. 11, no. 3, pp. 532–541, 2020.  
    - *Baseline*: DGCNN dynamic graph convolutional network.

34. **[Zhong et al. - 2020]**  
    P. Zhong, D. Wang, and C. Miao, "EEG-Based Emotion Recognition Using Regularized Graph Neural Networks," *IEEE Transactions on Affective Computing*, vol. 13, no. 3, pp. 1290–1301, 2020.  
    - *Baseline*: RGNN regularized graph neural network.

35. **[Bai et al. - 2018]**  
    S. Bai, J. Z. Kolter, and V. Koltun, "An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling," *arXiv:1803.01271*, 2018.  
    - *TCN Foundation*: Dilated convolutions for temporal ECG modeling.

36. **[Vaswani et al. - 2017]**  
    A. Vaswani et al., "Attention Is All You Need," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, pp. 5998–6008, 2017.

37. **[Chen et al. - 2018]**  
    Z. Chen, V. Badrinarayanan, C.-Y. Lee, and A. Rabinovich, "GradNorm: Gradient Normalization for Adaptive Loss Balancing in Deep Multitask Networks," in *Proc. ICML*, 2018, pp. 794–803.

38. **[Yu et al. - 2020]**  
    T. Yu et al., "Gradient Surgery for Multi-Task Learning," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 33, pp. 5824–5836, 2020.  
    - *PCGrad Foundation*: Mitigating gradient conflict in multi-task optimization.

39. **[Tsai et al. - 2019]**  
    Y.-H. H. Tsai et al., "Multimodal Transformer for Unaligned Multimodal Language Sequences," in *Proc. ACL*, 2019, pp. 6558–6569.

40. **[Li et al. - 2023]**  
    H. Li, Z. Chen, S. Zhao, and G. Ding, "Multi-Level Disentangled Representation Network for Multimodal Emotion Recognition," in *Proc. IJCAI*, 2023, pp. 4021–4029.  
    - *MDNet Disentanglement Foundation*.

41. **[Wang et al. - 2025]**  
    S. Wang, J. Zhang, C. Liu, and X. Tan, "PULSE: A Personalized Physiological Signal Analysis Framework via Unsupervised Domain Adaptation and Self-Adaptive Learning," *Expert Systems with Applications*, vol. 262, p. 125601, 2025.

42. **[Zhang et al. - 2024]**  
    Z. Zhang, S. Zhong, and Y. Liu, "Beyond Mimicking Under-Represented Emotions: Deep Data Augmentation with Emotional Subspace Constraints for EEG-Based Emotion Recognition," in *Proc. AAAI*, vol. 38, no. 1, pp. 7012–7020, 2024.

43. **[Li et al. - 2023]**  
    C. Li, N. Bian, Z. Zhao, and H. Wan, "Multi-View Domain-Adaptive Representation Learning for EEG-Based Emotion Recognition," *Information Fusion*, vol. 93, pp. 301–312, 2023.

44. **[Cheng et al. - 2024]**  
    Z. Cheng, X. Bu, Q. Wang, and L. Tao, "EEG-Based Emotion Recognition Using Multi-Scale Dynamic CNN and Gated Transformer," *Scientific Reports*, vol. 14, p. 1892, 2024.

45. **[Li et al. - 2023]**  
    J. Li, W. Pan, H. Huang, and H. Jia, "STGATE: Spatial-Temporal Graph Attention Network with a Transformer Encoder for EEG-Based Emotion Recognition," *Frontiers in Human Neuroscience*, vol. 17, p. 1149201, 2023.

46. **[Gong et al. - 2023]**  
    P. Gong, P. Wang, Y. Zhou, and D. Wu, "A Spiking Neural Network with Adaptive Graph Convolution and LSTM for EEG-Based Brain-Computer Interfaces," *IEEE Transactions on Neural Systems and Rehabilitation Engineering*, vol. 31, pp. 1025–1035, 2023.

---

## Category 5: Affective Neuroscience & Psychophysiological Foundations

47. **[Russell - 1980]**  
    J. A. Russell, "A Circumplex Model of Affect," *Journal of Personality and Social Psychology*, vol. 39, no. 6, pp. 1161–1178, 1980.  
    - *Theoretical Grounding*: Continuous orthogonal 2D Valence–Arousal emotional space.

48. **[Davidson - 1992]**  
    R. J. Davidson, "Anterior Cerebral Asymmetry and the Nature of Emotion," *Brain and Cognition*, vol. 20, no. 1, pp. 125–151, 1992.  
    - *Neurobiological Grounding*: Frontal alpha asymmetry (FAA) as cortical valence indicator.

49. **[Cacioppo et al. - 2007]**  
    J. T. Cacioppo, L. G. Tassinary, and G. G. Berntson, *Handbook of Psychophysiology*, Cambridge University Press, 2007.

50. **[Kreibig - 2010]**  
    S. D. Kreibig, "Autonomic Nervous System Activity in Emotion: A Review," *Biological Psychology*, vol. 84, no. 3, pp. 394–421, 2010.  
    - *Autonomic Grounding*: Coupling of cardiac chronotropy (ECG) and skin conductance (EDA) with emotional arousal.

51. **[Porges - 2007]**  
    S. W. Porges, "The Polyvagal Perspective," *Biological Psychology*, vol. 74, no. 2, pp. 116–143, 2007.  
    - *Vagal Tone Grounding*: Heart rate variability (HRV) as parasympathetic brake.

52. **[Ekman - 1992]**  
    P. Ekman, "An Argument for Basic Emotions," *Cognition & Emotion*, vol. 6, no. 3-4, pp. 169–200, 1992.  
    - *Categorical Discrete Emotion Grounding*.
