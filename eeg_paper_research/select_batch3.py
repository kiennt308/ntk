import sqlite3
import os
import pandas as pd

conn = sqlite3.connect('downloaded_papers/checklist.db')
cursor = conn.cursor()
cursor.execute("SELECT id, source, doi, title, authors, year, journal, local_path, status, file_size, abstract, pdf_url FROM papers WHERE status = 'Success'")
rows = cursor.fetchall()
columns = ['id', 'source', 'doi', 'title', 'authors', 'year', 'journal', 'local_path', 'status', 'file_size', 'abstract', 'pdf_url']
df = pd.DataFrame(rows, columns=columns)

def resolve_path(p):
    if not p: return None
    if os.path.exists(p): return p
    p2 = p.replace('eeg_paper_downloader', 'eeg_paper_research')
    if os.path.exists(p2): return p2
    fname = os.path.basename(p)
    for root, dirs, files in os.walk('downloaded_papers'):
        if fname in files:
            return os.path.join(root, fname)
    return None

df['actual_path'] = df['local_path'].apply(resolve_path)
df = df[df['actual_path'].notna()].copy()

# Filter out Batch 1 & 2 paper IDs
b1_b2_ids = [
    '1702.02510v3', '1907.07835v4', '1602.08225v1', '1601.02197v1', '1906.01704v1', 
    '1809.08410v1', '2305.07446v1', '2302.13170v2', '1903.07272v2', '2407.09950v2',
    '1705.04515v1', '1905.11678v4', '1809.04208v1', '1804.09452v2', '1811.10027v1',
    '1809.08273v1', '1811.07516v2', '1611.10120v1', '1810.04582v4', '1905.09472v2'
]
df = df[~df['id'].isin(b1_b2_ids)].copy()

print(f"Remaining papers available in pool: {len(df)}")

# Targeted queries across remaining priority categories:
target_queries = [
    # 1. Transfer Support Vector Machine / Domain Adaptation
    ("Transfer SVM", "Based on EEG Signals Using Transfer Support Vector Machine Algorithm"),
    # 2. Steady State Cognition-Emotion Models
    ("Steady State Visual Cortex", "The value of steady state models of cognition-emotion"),
    # 3. Microstate Dynamics
    ("EEG Microstates", "Valence-specific EEG microstate modulations during self-generated affective states"),
    # 4. Neural Networks and Foundation Models EEG-to-fMRI
    ("Foundation Models EEG-fMRI", "Neural networks and foundation models: two strategies for EEG-to-fMRI prediction"),
    # 5. Cultural & Interpersonal Emotion Regulation
    ("Emotion Regulation", "Cultural Differences in Interpersonal Emotion Regulation"),
    # 6. Deep Learning Mental Health / EEG
    ("Deep Learning Mental Health", "Leveraging deep learning for robust EEG analysis in mental health monitoring"),
    # 7. Time-frequency Denoising for ERP EEG
    ("Time-Frequency Denoising", "A time-frequency denoising method for single-channel event-related EEG"),
    # 8. EEG Referencing Methods
    ("EEG Referencing", "Effect of EEG Referencing Methods on Auditory Mismatch Negativity"),
    # 9. Emotion Differentiation
    ("Negative Emotion Differentiation", "Negative Emotion Differentiation Predicts Psychotherapy Outcome"),
    # 10. Emotion Kinds & Theories
    ("Emotion Taxonomy Theory", "How Many Different Kinds of Emotion are There")
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

# If any slot is empty, fill with other top papers
if len(selected) < 10:
    extra = df[~df['id'].isin(used_ids) & df['title'].str.contains('emotion', case=False, na=False)]
    for _, r in extra.iterrows():
        selected.append(('General', r))
        used_ids.add(r['id'])
        if len(selected) >= 10:
            break

print(f"\nSelected {len(selected[:10])} papers for Batch 3:")
for idx, (tag, r) in enumerate(selected[:10]):
    print(f"P{idx+21:04d} [{tag}] {r['year']} - {r['title']}")
    print(f"       File: {r['actual_path']}")

