import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Class names based on metrics.txt and the SMOTE balancing results
data = {
    'Benign': 200000,
    'TCP Scan': 200000,
    'Telnet Brute Force': 200000,
    'Ingress Tool Transfer': 200000,
    'File Download': 200000,
    'C&C Communication': 200000,
    'Reporting': 200000
}

df = pd.Series(data)

plt.figure(figsize=(12, 6))
sns.barplot(x=df.index, y=df.values, palette='Blues_d')
plt.title('Distribusi Dataset Sesudah SMOTE (Training Set)', fontsize=14)
plt.xlabel('Kategori Serangan', fontsize=12)
plt.ylabel('Jumlah Data', fontsize=12)
plt.xticks(rotation=45, ha="right")

for i, count in enumerate(df.values):
    plt.text(i, count, f'{count:,}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
os.makedirs('hasil', exist_ok=True)
plt.savefig('hasil/distribusi_sesudah_smote.png')
print("Plot successfully saved to hasil/distribusi_sesudah_smote.png")
