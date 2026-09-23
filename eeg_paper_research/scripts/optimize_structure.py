import os
import shutil
import re

# 1. Clean up legacy duplicate folders in notebooklm_workspace
ws_dir = r"d:\ntk\eeg_paper_research\notebooklm_workspace"
legacy_folders = [
    "notebook_01_Biosignal_Emotion_Recognition",
    "notebook_02_Multimodal_Emotion_Recognition",
    "notebook_03_Multi_Task_Learning_Emotion",
    "notebook_04_Multi_Branch_Fusion_Architecture",
    "notebook_05_Generalization_Robustness_Missing_Modality"
]

for legacy in legacy_folders:
    target_path = os.path.join(ws_dir, legacy)
    if os.path.exists(target_path):
        print(f"Removing legacy duplicate folder: {legacy}")
        shutil.rmtree(target_path)

# 2. Rename kw1..kw9 to kw01..kw09 in literature/open_access_repository
oa_dir = r"d:\ntk\eeg_paper_research\literature\open_access_repository"
rename_map = {
    "kw01_multimodal_eeg_biosignals": "kw01_multimodal_eeg_biosignals",
    "kw02_multitask_learning_affect": "kw02_multitask_learning_affect",
    "kw03_multibranch_crossmodal_attention": "kw03_multibranch_crossmodal_attention",
    "kw04_subspace_disentanglement_domain_adaptation": "kw04_subspace_disentanglement_domain_adaptation",
    "kw05_missing_modality_wearable_robustness": "kw05_missing_modality_wearable_robustness",
    "kw06_foundation_models_self_supervised_biosignals": "kw06_foundation_models_self_supervised_biosignals",
    "kw07_graph_neural_networks_eeg_connectivity": "kw07_graph_neural_networks_eeg_connectivity",
    "kw08_transformers_crossmodal_affective_computing": "kw08_transformers_crossmodal_affective_computing",
    "kw09_explainable_ai_interpretable_biosignals": "kw09_explainable_ai_interpretable_biosignals",
    # kw10 is already 2 digits
}

for old_name, new_name in rename_map.items():
    old_p = os.path.join(oa_dir, old_name)
    new_p = os.path.join(oa_dir, new_name)
    if os.path.exists(old_p):
        print(f"Renaming {old_name} -> {new_name}")
        os.rename(old_p, new_p)

# 3. Update references across markdown files in the repository
base_dir = r"d:\ntk\eeg_paper_research"

def replace_in_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return
    
    modified = content
    for old_k, new_k in rename_map.items():
        modified = modified.replace(old_k, new_k)
    
    # Also update OA_KW1..OA_KW9 in IDs if needed, but directory paths are the key
    if modified != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified)
        print(f"Updated links in: {file_path}")

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith((".md", ".py", ".csv", ".json")):
            replace_in_file(os.path.join(root, f))

print("Optimization complete.")
