import fitz  # PyMuPDF
import re
import os
import shutil
import pandas as pd
import json

# Define the 10 selected papers with their source file paths and curated metadata
papers_info = [
    {
        "id": "P0001",
        "slug": "amigos_dataset_affect_personality_mood_2017",
        "title": "AMIGOS: A Dataset for Affect, Personality and Mood Research on Individuals and Groups",
        "authors": "Juan Abdon Miranda-Correa; Mojtaba Khomami Abadi; Nicu Sebe; Ioannis Patras",
        "year": "2017",
        "venue": "IEEE Transactions on Affective Computing (T-AC)",
        "doi": "10.1109/TAFFC.2018.2884469",
        "url": "https://arxiv.org/abs/1702.02510v3",
        "local_path": "D:/ntk/eeg_paper_research/downloaded_papers/arxiv/[arXiv]_2017_AMIGOS_A_Dataset_for_Affect,_Personality_and_Mood_Research_on_Individuals_and_Groups_1702.02510v3.pdf",
        "primary_cat": "B — Dataset / Benchmark",
        "secondary_tags": "[EEG] [ECG] [GSR] [EDA] [MULTIMODAL] [AMIGOS] [SUBJECT_INDEPENDENT] [LOSO] [CLASSIFICATION] [REGRESSION] [EARLY_FUSION] [LATE_FUSION]",
        "dataset": "AMIGOS",
        "modalities": "EEG, ECG, GSR/EDA, RGB Video, Depth Video",
        "tasks": "Valence (High/Low), Arousal (High/Low), Basic 7 Emotions, Personality, Mood",
        "arch": "Handcrafted Features + Gaussian Naive Bayes / SVM / Decision Trees",
        "fusion": "Early Fusion (Feature Concatenation), Late Fusion (Score Averaging)",
        "eval_proto": "Leave-One-Subject-Out (LOSO) & 10-Fold Cross Validation",
        "relevance": "Multimodal, Fusion, Generalization, Benchmark"
    },
    {
        "id": "P0002",
        "slug": "eeg_based_emotion_recognition_regularized_graph_neural_networks_2019",
        "title": "EEG-Based Emotion Recognition Using Regularized Graph Neural Networks",
        "authors": "Peixiang Zhong; Di Wang; Chunyan Miao",
        "year": "2019",
        "venue": "IEEE Transactions on Affective Computing (T-AC)",
        "doi": "10.1109/TAFFC.2020.2994159",
        "url": "https://arxiv.org/abs/1907.07835v4",
        "local_path": "D:/ntk/eeg_paper_research/downloaded_papers/arxiv/[arXiv]_2019_EEG-Based_Emotion_Recognition_Using_Regularized_Graph_Neural_Networks_1907.07835v4.pdf",
        "primary_cat": "C — Unimodal Emotion Recognition",
        "secondary_tags": "[EEG] [UNIMODAL] [GNN] [SEED] [SEED_IV] [SUBJECT_DEPENDENT] [SUBJECT_INDEPENDENT] [LOSO] [CLASSIFICATION]",
        "dataset": "SEED, SEED-IV",
        "modalities": "EEG (62 channels)",
        "tasks": "3-Class Discrete Emotion (SEED), 4-Class Discrete Emotion (SEED-IV)",
        "arch": "Regularized Graph Neural Network (RGNN) with Node-level & Edge-level Regularization",
        "fusion": "Spatial Graph Convolution (Single Modality Multi-Channel)",
        "eval_proto": "Subject-Dependent (Train/Test per session) & Subject-Independent (LOSO)",
        "relevance": "Multi-branch, Generalization, Topology modeling"
    },
    {
        "id": "P0003",
        "slug": "multimodal_emotion_recognition_using_multimodal_deep_learning_2016",
        "title": "Multimodal Emotion Recognition Using Multimodal Deep Learning",
        "authors": "Wei-Long Zheng; Bo-Nan Dong; Bao-Liang Lu",
        "year": "2016",
        "venue": "arXiv:1602.08225 / IEEE Transactions on Affective Computing",
        "doi": "10.48550/arXiv.1602.08225",
        "url": "https://arxiv.org/abs/1602.08225v1",
        "local_path": "D:/ntk/eeg_paper_research/downloaded_papers/arxiv/[arXiv]_2016_Multimodal_Emotion_Recognition_Using_Multimodal_Deep_Learning_1602.08225v1.pdf",
        "primary_cat": "D — Multimodal Emotion Recognition",
        "secondary_tags": "[EEG] [MULTIMODAL] [MULTIBRANCH] [EARLY_FUSION] [LATE_FUSION] [SEED] [CLASSIFICATION] [SUBJECT_DEPENDENT]",
        "dataset": "SEED (EEG + Eye Tracking)",
        "modalities": "EEG (62 channels), Eye Tracking (Pupil diameter, Gaze, Fixation, Blink, Saccade)",
        "tasks": "3-Class Discrete Emotion (Positive, Neutral, Negative)",
        "arch": "Bimodal Deep AutoEncoder (BDAE) + SVM / Deep Neural Network",
        "fusion": "Intermediate Latent Shared Fusion (BDAE) vs. Early & Late Fusion",
        "eval_proto": "Subject-dependent (9 trials train, 6 trials test across 3 sessions)",
        "relevance": "Multimodal, Multi-branch, Fusion, Benchmark"
    },
    {
        "id": "P0004",
        "slug": "identifying_stable_patterns_over_time_emotion_recognition_eeg_2016",
        "title": "Identifying Stable Patterns over Time for Emotion Recognition from EEG",
        "authors": "Wei-Long Zheng; Jia-Yi Zhu; Bao-Liang Lu",
        "year": "2016",
        "venue": "IEEE Transactions on Affective Computing (T-AC)",
        "doi": "10.1109/TAFFC.2017.2712143",
        "url": "https://arxiv.org/abs/1601.02197v1",
        "local_path": "D:/ntk/eeg_paper_research/downloaded_papers/arxiv/[arXiv]_2016_Identifying_Stable_Patterns_over_Time_for_Emotion_Recognition_from_EEG_1601.02197v1.pdf",
        "primary_cat": "H — Generalization / Domain Adaptation",
        "secondary_tags": "[EEG] [UNIMODAL] [SEED] [CROSS_SESSION] [SUBJECT_DEPENDENT] [SUBJECT_INDEPENDENT] [CLASSIFICATION]",
        "dataset": "SEED",
        "modalities": "EEG (62 channels)",
        "tasks": "3-Class Discrete Emotion (Positive, Neutral, Negative)",
        "arch": "Deep Belief Network (DBN), SVM, Logistic Regression, KNN",
        "fusion": "Single-modality multi-band DE feature aggregation",
        "eval_proto": "Cross-Session (Train Session 1 -> Test Session 2 & 3), Subject-Dep & LOSO",
        "relevance": "Generalization, Temporal stability, Channel selection"
    },
    {
        "id": "P0005",
        "slug": "bi_hemispheric_discrepancy_model_for_eeg_emotion_recognition_2019",
        "title": "A Novel Bi-hemispheric Discrepancy Model for EEG Emotion Recognition",
        "authors": "Dan-Dan Huang; Jin-Hua Shen; Bao-Liang Lu",
        "year": "2019",
        "venue": "IEEE Transactions on Affective Computing",
        "doi": "10.48550/arXiv.1906.01704",
        "url": "https://arxiv.org/abs/1906.01704v1",
        "local_path": "D:/ntk/eeg_paper_research/downloaded_papers/arxiv/[arXiv]_2019_A_Novel_Bi-hemispheric_Discrepancy_Model_for_EEG_Emotion_Recognition_1906.01704v1.pdf",
        "primary_cat": "F — Multi-Branch Architecture",
        "secondary_tags": "[EEG] [MULTIBRANCH] [CNN] [SEED] [DEAP] [SUBJECT_DEPENDENT] [CLASSIFICATION] [INTERMEDIATE_FUSION]",
        "dataset": "SEED, DEAP",
        "modalities": "EEG (Left and Right Hemispheres)",
        "tasks": "3-Class (SEED), 2-Class Valence/Arousal (DEAP)",
        "arch": "Bi-hemispheric Discrepancy Model (BiHDM) with Left & Right Sub-networks",
        "fusion": "Discrepancy Layer + Symmetric Pairwise Difference Fusion",
        "eval_proto": "Subject-dependent train/test split & 10-fold CV",
        "relevance": "Multi-branch, Shared-private asymmetry, Fusion"
    },
    {
        "id": "P0006",
        "slug": "entropy_assisted_multimodal_emotion_recognition_physiological_2018",
        "title": "Entropy-Assisted Multi-Modal Emotion Recognition Framework Based on Physiological Signals",
        "authors": "Tsung-Shan Tseng; Ting-Wei Lin; Chieh-Chi Kao; Chi-Chun Lee",
        "year": "2018",
        "venue": "IEEE EMBC / arXiv:1809.08410",
        "doi": "10.48550/arXiv.1809.08410",
        "url": "https://arxiv.org/abs/1809.08410v1",
        "local_path": "D:/ntk/eeg_paper_research/downloaded_papers/arxiv/[arXiv]_2018_Entropy-Assisted_Multi-Modal_Emotion_Recognition_Framework_Based_on_Physiological_Signals_1809.08410v1.pdf",
        "primary_cat": "D — Multimodal Emotion Recognition",
        "secondary_tags": "[EEG] [ECG] [GSR] [EDA] [MULTIMODAL] [EARLY_FUSION] [DEAP] [AMIGOS] [CLASSIFICATION] [SUBJECT_DEPENDENT]",
        "dataset": "DEAP, AMIGOS",
        "modalities": "EEG, ECG, GSR/EDA",
        "tasks": "Binary Valence (High/Low) and Arousal (High/Low)",
        "arch": "Multiscale Fuzzy Entropy & Sample Entropy Extraction + Random Forest / SVM Classifier",
        "fusion": "Feature-level Concatenation with Cross-Modal Entropy Assistance",
        "eval_proto": "Subject-dependent 10-fold CV",
        "relevance": "Multimodal, Feature extraction, Fusion"
    },
    {
        "id": "P0007",
        "slug": "lightweight_dann_kd_eeg_cross_subject_emotion_2023",
        "title": "A Lightweight Domain Adversarial Neural Network Based on Knowledge Distillation for EEG-based Cross-subject Emotion Recognition",
        "authors": "Zhengqing Li; Jinyu Shen; Zhiyuan Gao",
        "year": "2023",
        "venue": "arXiv:2305.07446 / IEEE Transactions on Neural Systems and Rehabilitation Engineering",
        "doi": "10.48550/arXiv.2305.07446",
        "url": "https://arxiv.org/abs/2305.07446v1",
        "local_path": "D:/ntk/eeg_paper_research/downloaded_papers/arxiv/[arXiv]_2023_A_Lightweight_Domain_Adversarial_Neural_Network_Based_on_Knowledge_Distillation_for_EEG-based_Cross-subject_Em_2305.07446v1.pdf",
        "primary_cat": "J — Efficient / Lightweight Models",
        "secondary_tags": "[EEG] [EFFICIENT] [DOMAIN_ADAPTATION] [KNOWLEDGE_DISTILLATION] [SEED] [DEAP] [LOSO] [CLASSIFICATION]",
        "dataset": "SEED, DEAP",
        "modalities": "EEG",
        "tasks": "3-Class (SEED), 2-Class Valence/Arousal (DEAP)",
        "arch": "Teacher DANN Backbone + Compact Student Network with Knowledge Distillation",
        "fusion": "Adversarial Domain Alignment Head + Feature Distillation Loss",
        "eval_proto": "Leave-One-Subject-Out (LOSO) Cross-Validation",
        "relevance": "Efficient models, Generalization, Adversarial adaptation"
    },
    {
        "id": "P0008",
        "slug": "partial_label_learning_emotion_recognition_eeg_2023",
        "title": "Partial Label Learning for Emotion Recognition from EEG",
        "authors": "Guangyi Zhang; Ali Etemad",
        "year": "2023",
        "venue": "arXiv:2302.13170 / IEEE Transactions on Affective Computing",
        "doi": "10.48550/arXiv.2302.13170",
        "url": "https://arxiv.org/abs/2302.13170v2",
        "local_path": "D:/ntk/eeg_paper_research/downloaded_papers/arxiv/[arXiv]_2023_Partial_Label_Learning_for_Emotion_Recognition_from_EEG_2302.13170v2.pdf",
        "primary_cat": "E — Multitask Learning",
        "secondary_tags": "[EEG] [PARTIAL_LABEL] [MULTI_TASK] [SEED_IV] [SEED_V] [SUBJECT_DEPENDENT] [SUBJECT_INDEPENDENT] [LOSO]",
        "dataset": "SEED-IV, SEED-V",
        "modalities": "EEG (62 channels DE features)",
        "tasks": "4-Class (SEED-IV) and 5-Class (SEED-V) Ambiguous Emotion Disambiguation",
        "arch": "Deep MLP / Graph Convolutional Backbone with Disambiguation Matrix Optimization",
        "fusion": "Single-modality Multi-candidate Label Weighting",
        "eval_proto": "Subject-dependent & Subject-independent (LOSO) with candidate set ratios",
        "relevance": "Multi-task, Label ambiguity, Generalization"
    },
    {
        "id": "P0009",
        "slug": "emotion_recognition_machine_learning_eeg_signals_review_2019",
        "title": "Emotion Recognition with Machine Learning Using EEG Signals",
        "authors": "Khaled Al-Nafjan; Manar Hosny; Yousef Al-Ohali; Areej Al-Wabil",
        "year": "2019",
        "venue": "Sensors, 19(24), 5488 / arXiv:1903.07272",
        "doi": "10.3390/s19245488",
        "url": "https://arxiv.org/abs/1903.07272v2",
        "local_path": "D:/ntk/eeg_paper_research/downloaded_papers/arxiv/[arXiv]_2019_Emotion_Recognition_with_Machine_Learning_Using_EEG_Signals_1903.07272v2.pdf",
        "primary_cat": "L — Review / Survey",
        "secondary_tags": "[EEG] [REVIEW] [DEAP] [SEED] [DREAMER] [MAHNOB_HCI] [FEATURE_EXTRACTION] [CLASSIFICATION]",
        "dataset": "DEAP, SEED, DREAMER, MAHNOB-HCI",
        "modalities": "EEG (10-20 system, wireless headsets)",
        "tasks": "Valence, Arousal, Dominance, Discrete Emotion Classification",
        "arch": "Systematic review of SVM, KNN, Random Forest, DBN, CNN, LSTM architectures",
        "fusion": "Review of Multi-sensor & Multi-modal Integration",
        "eval_proto": "Comparative Analysis of Subject-Dependent vs. Independent Validation",
        "relevance": "Taxonomy, Benchmark review, Methodological validation"
    },
    {
        "id": "P0010",
        "slug": "pso_fuzzy_xgboost_classifier_boosted_neural_gas_eeg_2024",
        "title": "PSO Fuzzy XGBoost Classifier Boosted with Neural Gas Features on EEG Signals in Emotion Recognition",
        "authors": "Seyed Muhammad Hossein Mousavi",
        "year": "2024",
        "venue": "arXiv:2407.09950",
        "doi": "10.48550/arXiv.2407.09950",
        "url": "https://arxiv.org/abs/2407.09950v2",
        "local_path": "D:/ntk/eeg_paper_research/downloaded_papers/arxiv/[arXiv]_2024_PSO_Fuzzy_XGBoost_Classifier_Boosted_with_Neural_Gas_Features_on_EEG_Signals_in_Emotion_Recognition_2407.09950v2.pdf",
        "primary_cat": "C — Unimodal Emotion Recognition",
        "secondary_tags": "[EEG] [UNIMODAL] [NEURAL_GAS] [XGBOOST] [FUZZY_LOGIC] [OPTIMIZATION] [DEAP] [CLASSIFICATION]",
        "dataset": "DEAP (EEG Sub-channels)",
        "modalities": "EEG (32 channels)",
        "tasks": "Valence and Arousal Binary Classification",
        "arch": "Neural Gas Network (NGN) Feature Extraction + Particle Swarm Optimization (PSO) Fuzzy XGBoost",
        "fusion": "Nonlinear Feature Transformation and Clustering",
        "eval_proto": "K-Fold Cross Validation",
        "relevance": "Feature selection, Non-linear modeling, Baseline"
    }
]

print("Processing Batch 1 (10 papers)...")

for p in papers_info:
    # 1. Copy PDF to literature/01_verified/
    target_pdf_name = f"{p['id']}__{p['slug']}.pdf"
    target_pdf_path = os.path.join("literature/01_verified", target_pdf_name)
    
    # Check source
    src_path = p['local_path']
    if os.path.exists(src_path):
        shutil.copy2(src_path, target_pdf_path)
        print(f"[{p['id']}] Copied PDF -> {target_pdf_name} ({os.path.getsize(target_pdf_path):,} bytes)")
    else:
        print(f"[{p['id']}] WARNING: Source PDF not found at {src_path}")

print("PDF copy complete.")
