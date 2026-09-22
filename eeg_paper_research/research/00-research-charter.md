# Research Charter

## Working Title

Kiến trúc học đa nhiệm vụ đa nhánh cho nhận diện cảm xúc từ tín hiệu y sinh đa phương thức

## English Title

Multi-Task Multi-Branch Architecture for Emotion Recognition from Multimodal Biosignals

## Core Problem

Develop a multimodal biosignal representation learning framework for emotion recognition using multi-branch and multi-task learning.

## Core Modalities (Focused Trinity)

- **EEG** (Central Nervous System — Cortical Cognitive Appraisal)
- **ECG** (Autonomic Nervous System — Cardiac Chronotropy & HRV)
- **EDA/GSR** (Autonomic Sympathetic Nervous System — Sudomotor Sweat Arousal)

## Primary Research Objectives & Scientific Novelty

1. **Physics-Informed Multi-Branch Architecture**: Dedicated Spatial-Temporal 2D-CNN for EEG montages and Multi-Scale Dilated 1D-CNNs for cardiac/sudomotor dynamics.
2. **Shared-Private Subspace Disentanglement**: Explicit separation of emotion-invariant shared semantics from sensor-private artifacts via CMD and soft Frobenius orthogonality.
3. **Directional Cross-Modal Attention**: QKV autonomic-cortical interaction.
4. **Homoscedastic Aleatoric Uncertainty Loss Balancing**: Dynamically learned multi-task weighting resolving gradient conflict between continuous regression and discrete classification.
5. **Generalization & Missing-Modality Robustness**: Adversarial domain alignment (GRL) and cross-modal latent inpainting.

## Research Lifecycle Status

- **Status**: **100% Completed, Literature-Grounded, and Defense-Ready**.
- **Master Guide**: See [`research/01-phd-executive-handbook.md`](file:///d:/ntk/eeg_paper_research/research/01-phd-executive-handbook.md) for the condensed doctoral roadmap and defense guide.