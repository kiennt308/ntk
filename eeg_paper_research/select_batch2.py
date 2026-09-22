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

# Filter out Batch 1 papers
b1_ids = ['1702.02510v3', '1907.07835v4', '1602.08225v1', '1601.02197v1', '1906.01704v1', 
          '1809.08410v1', '2305.07446v1', '2302.13170v2', '1903.07272v2', '2407.09950v2']
df = df[~df['id'].isin(b1_ids)].copy()

# Target queries for Batch 2:
target_queries = [
    # 1. Spatial-temporal Recurrent Neural Network
    ("Spatial-Temporal RNN", "Spatial-Temporal Recurrent Neural Network for Emotion Recognition"),
    # 2. Connectivity & Graph Neural Network
    ("Connectivity Structure", "EEG-based Emotional Video Classification via Learning Connectivity Structure"),
    # 3. Brain Connectivity & CNN
    ("Brain Connectivity CNN", "Convolutional Neural Network Approach for EEG-based Emotion Recognition using Brain Connectivity"),
    # 4. Multi-modal Approach for Affective Computing
    ("Multimodal Affective Computing", "Multi-modal Approach for Affective Computing"),
    # 5. Stressful Environments Multimodal
    ("Stressful Environments", "Multimodal Classification of Stressful Environments in Visually Impaired Mobility Using EEG and Peripheral"),
    # 6. Inter-Subject Correlation
    ("Inter-Subject Correlation", "EEG-based Inter-Subject Correlation Schemes in a Stimuli-Shared Framework"),
    # 7. Unsupervised Reservoir Computing for EEG Emotion
    ("Reservoir Computing", "Unsupervised Learning in Reservoir Computing for EEG-based Emotion Recognition"),
    # 8. Fusion of EEG and Musical Features
    ("Continuous Music Emotion", "Fusion of EEG and Musical Features in Continuous Music-emotion Recognition"),
    # 9. Consumer Grade Brain Sensing
    ("Consumer Brain Sensing", "Consumer Grade Brain Sensing for Emotion Recognition"),
    # 10. Sensor Configuration Factoring
    ("Sensor Configuration", "EEG Classification by factoring in Sensor Configuration")
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

print(f"Selected {len(selected[:10])} papers for Batch 2:")
for idx, (tag, r) in enumerate(selected[:10]):
    print(f"P{idx+11:04d} [{tag}] {r['year']} - {r['title']}")
    print(f"       File: {r['actual_path']}")

