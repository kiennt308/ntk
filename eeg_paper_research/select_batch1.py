import sqlite3
import os
import shutil
import pandas as pd

conn = sqlite3.connect('downloaded_papers/checklist.db')
cursor = conn.cursor()
cursor.execute("SELECT id, source, doi, title, authors, year, journal, local_path, status, file_size, abstract, pdf_url FROM papers WHERE status = 'Success'")
rows = cursor.fetchall()
columns = ['id', 'source', 'doi', 'title', 'authors', 'year', 'journal', 'local_path', 'status', 'file_size', 'abstract', 'pdf_url']
df = pd.DataFrame(rows, columns=columns)

print(f"Total successful papers in DB: {len(df)}")

def resolve_path(p):
    if not p:
        return None
    if os.path.exists(p):
        return p
    p2 = p.replace('eeg_paper_downloader', 'eeg_paper_research')
    if os.path.exists(p2):
        return p2
    # Check downloaded_papers relative path
    fname = os.path.basename(p)
    for root, dirs, files in os.walk('downloaded_papers'):
        if fname in files:
            return os.path.join(root, fname)
    return None

df['actual_path'] = df['local_path'].apply(resolve_path)
df = df[df['actual_path'].notna()].copy()
print(f"Total verified local PDF files found: {len(df)}")

# Target search for 10 diverse foundational/methodological papers across the 15 categories
target_queries = [
    # 1. AMIGOS Dataset / Multimodal Benchmark
    ("AMIGOS", "AMIGOS: A Dataset for Affect, Personality and Mood Research"),
    # 2. Regularized Graph Neural Networks (RGNN)
    ("RGNN", "Regularized Graph Neural Networks"),
    # 3. Dynamic Graph / MPED Dataset
    ("MPED", "MPED: A Multi-Modal Physiological Emotion Database"),
    # 4. Multimodal Deep Learning for Emotion Recognition
    ("Multimodal Deep Learning", "Multimodal Emotion Recognition Using Multimodal Deep Learning"),
    # 5. Identifying Stable Patterns over Time
    ("Stable Patterns", "Identifying Stable Patterns over Time for Emotion Recognition"),
    # 6. Bi-hemispheric Discrepancy / Asymmetry
    ("Bi-hemispheric", "A Novel Bi-hemispheric Discrepancy Model"),
    # 7. Entropy-Assisted Multi-Modal Framework
    ("Entropy-Assisted", "Entropy-Assisted Multi-Modal Emotion Recognition Framework"),
    # 8. Lightweight Deep CNN Ensemble
    ("Lightweight", "Automatic Emotion Recognition (AER) System based on Two-Level Ensemble of Lightweight Deep CNN Models"),
    # 9. Partial Label Learning (SEED-IV & SEED-V)
    ("Partial Label", "Partial Label Learning for Emotion Recognition from EEG"),
    # 10. Emotion Recognition with Machine Learning Review
    ("Review", "Emotion Recognition with Machine Learning Using EEG Signals")
]

selected = []
used_ids = set()

for tag, q in target_queries:
    m = df[df['title'].str.contains(q, case=False, na=False)]
    if len(m) == 0:
        m = df[df['title'].str.contains(tag, case=False, na=False)]
    for _, r in m.iterrows():
        if r['id'] not in used_ids:
            selected.append((tag, r))
            used_ids.add(r['id'])
            break

# If any slot is empty, fill with top emotional biosignal papers
if len(selected) < 10:
    extra = df[~df['id'].isin(used_ids) & df['title'].str.contains('emotion', case=False, na=False)]
    for _, r in extra.iterrows():
        selected.append(('General', r))
        used_ids.add(r['id'])
        if len(selected) >= 10:
            break

print(f"\nSelected {len(selected)} papers for Batch 1:")
for idx, (tag, r) in enumerate(selected[:10]):
    print(f"P{idx+1:04d} [{tag}] {r['year']} - {r['title']}")
    print(f"      File: {r['actual_path']}")
