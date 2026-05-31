import pandas as pd
import glob
import os
from collections import Counter

files = glob.glob('data/processed/*.csv')
total_counts = Counter()

print(f"Mulai memproses {len(files)} file CSV...")
for i, f in enumerate(files):
    try:
        # Hanya baca kolom 'label' agar proses jauh lebih cepat
        df = pd.read_csv(f, usecols=['label'])
        counts = df['label'].value_counts().to_dict()
        total_counts.update(counts)
        if (i+1) % 10 == 0:
            print(f"[{i+1}/{len(files)}] files processed...")
    except Exception as e:
        print(f"Error reading {f}: {e}")

print("\n=== TOTAL JUMLAH DATA PER LABEL KESELURUHAN ===")
# Sort by value descending
sorted_counts = sorted(total_counts.items(), key=lambda x: x[1], reverse=True)
for label, count in sorted_counts:
    print(f"{label}: {count:,}")
