import pandas as pd
import glob
import os

files = glob.glob('data/processed/*.csv')
res = {}

for f in files[:20]: # just test first 20 files
    try:
        df = pd.read_csv(f, usecols=['label'])
        counts = df['label'].value_counts().to_dict()
        if len(counts) > 1 or 'Benign' not in counts:
            res[os.path.basename(f)] = counts
    except Exception as e:
        print(f"Error reading {f}: {e}")

print("Files with malicious data (first 20):")
print(res)
