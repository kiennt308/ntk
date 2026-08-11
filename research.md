---
layout: page
title: "Academic Research: Multimodal Emotion Recognition"
permalink: /research.html
---

<div class="research-page" style="margin-top: 1rem;">
  
  <div style="background-color: rgba(var(--primary-rgb), 0.03); border: 1px solid var(--border); border-radius: var(--border-radius); padding: 1.75rem; margin-bottom: 3rem; border-left: 4px solid var(--primary);">
    <h3 style="margin-top: 0; color: var(--primary);">Project Overview</h3>
    <p style="font-size: 1.05rem; line-height: 1.6; margin-bottom: 0; font-style: italic;">
      "Developing robust, deep learning-based multimodal frameworks to classify human emotional states by integrating electroencephalogram (EEG) signals with peripheral physiological responses and facial expressions."
    </p>
  </div>

  <h2>1. Research Abstract & Focus</h2>
  <p>
    Human emotion recognition plays a key role in next-generation Human-Computer Interaction (HCI). While facial expressions and speech audio are common indicators of emotion, they are easily masked or manipulated. Electroencephalogram (EEG) signals, which capture direct electrical brain activity, offer an objective "gold standard" for physiological emotion tracking.
  </p>
  <p>
    Our research focuses on building hybrid convolutional and recurrent networks (CNN + LSTM) and Transformer models capable of extraction and fusion of spatial-temporal features from multi-channel EEG signals.
  </p>

  <h2 style="margin-top: 3rem;">2. Core Datasets</h2>
  <p>
    To train and validate our neural models, we utilize two of the primary datasets in the affective computing field:
  </p>
  <div class="grid grid--2col" style="margin: 1.5rem 0 3rem 0;">
    <div class="card" style="padding: 1.5rem; background: var(--surface);">
      <h3 style="margin-top:0; color: var(--accent);">DEAP Dataset</h3>
      <p style="font-size: 0.9rem; margin-bottom: 0;">
        <strong>Description:</strong> Multimodal dataset containing EEG and peripheral physiological signals of 32 participants watching 40 music video clips. Includes valence, arousal, dominance, and liking ratings.
      </p>
    </div>
    <div class="card" style="padding: 1.5rem; background: var(--surface);">
      <h3 style="margin-top:0; color: var(--accent);">SEED Dataset</h3>
      <p style="font-size: 0.9rem; margin-bottom: 0;">
        <strong>Description:</strong> Standardized EEG dataset from SJTU containing recordings of 15 subjects watching emotional film clips. Highly optimized for studying valence classifications (positive, neutral, negative).
      </p>
    </div>
  </div>

  <h2>3. Proposed Methodology</h2>
  <p>
    Our classification pipeline involves four major stages:
  </p>
  <ol style="margin-left: 1.5rem; margin-bottom: 2rem;">
    <li style="margin-bottom: 0.75rem;">
      <strong>Signal Preprocessing:</strong> Applying Bandpass filters (4–45Hz) to remove DC offsets, powerline hum, and electrooculogram (EOG) artifacts.
    </li>
    <li style="margin-bottom: 0.75rem;">
      <strong>Feature Extraction:</strong> Calculating Differential Entropy (DE) and Power Spectral Density (PSD) across five distinct frequency bands: Delta (1-4Hz), Theta (4-8Hz), Alpha (8-14Hz), Beta (14-30Hz), and Gamma (30-45Hz).
    </li>
    <li style="margin-bottom: 0.75rem;">
      <strong>Deep Learning Classifier:</strong> Utilizing spatial-temporal network modules. CNN grids learn topology representations from EEG channel locations, while bidirectional GRU/LSTM layers model sequential patterns.
    </li>
    <li style="margin-bottom: 0.75rem;">
      <strong>Multimodal Fusion:</strong> Applying attention-based fusion mechanisms to merge EEG classification outputs with features extracted from facial keypoint sequences.
    </li>
  </ol>

  <h2 style="margin-top: 3rem;">4. Academic Publications & Presentations</h2>
  
  <div style="display: flex; flex-direction: column; gap: 1.5rem; margin-top: 1.5rem; margin-bottom: 3rem;">
    
    <div style="border: 1px solid var(--border); border-radius: var(--border-radius); padding: 1.5rem; background-color: var(--surface);">
      <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.5rem;">
        <span class="badge badge--primary">Conference Paper</span>
        <span style="font-size: 0.85rem; color: var(--text-muted);">October 2025</span>
      </div>
      <h3 style="margin-top: 0; font-size: 1.15rem; margin-bottom: 0.5rem;">
        "Attention-Based Spatial-Temporal Fusion for EEG-Based Emotion Recognition"
      </h3>
      <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem; font-style: italic;">
        International Joint Conference on Neural Networks (IJCNN 2025)
      </p>
      <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0;">
        Authors: Kien Nguyen, Dr. Sarah Jenkins, et al.
      </p>
    </div>

    <div style="border: 1px solid var(--border); border-radius: var(--border-radius); padding: 1.5rem; background-color: var(--surface);">
      <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.5rem;">
        <span class="badge badge--accent">Journal Pre-print</span>
        <span style="font-size: 0.85rem; color: var(--text-muted);">Under Review (2026)</span>
      </div>
      <h3 style="margin-top: 0; font-size: 1.15rem; margin-bottom: 0.5rem;">
        "Multimodal Emotion Classification Using Deep Transformer Networks and Physiological Signals"
      </h3>
      <p style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem; font-style: italic;">
        IEEE Transactions on Affective Computing
      </p>
      <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0;">
        Authors: Kien Nguyen, Dr. Sarah Jenkins.
      </p>
    </div>

  </div>

  <h2>5. Current Research Progress</h2>
  <div style="position: relative; padding-left: 20px; border-left: 2px solid var(--border); margin-top: 1.5rem;">
    <div style="margin-bottom: 1.5rem; position: relative;">
      <div style="position: absolute; left: -26px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background-color: var(--accent);"></div>
      <strong style="font-size: 0.9rem; color: var(--accent);">Q1 2026:</strong>
      <p style="font-size: 0.95rem; margin-top: 0.25rem;">
        Completed benchmarking of Vision Transformer (ViT) feature collectors on DEAP physiological samples. Achieved an 88.5% classification rate on Valence mappings.
      </p>
    </div>
    <div style="position: relative;">
      <div style="position: absolute; left: -26px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background-color: var(--primary);"></div>
      <strong style="font-size: 0.9rem; color: var(--primary);">Ongoing:</strong>
      <p style="font-size: 0.95rem; margin-top: 0.25rem;">
        Developing low-latency cross-attention networks to synchronize high-frequency EEG channel frames with lower-resolution physiological feeds in real-time.
      </p>
    </div>
  </div>

</div>
