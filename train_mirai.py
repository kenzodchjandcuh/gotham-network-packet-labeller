import pandas as pd
import numpy as np
import time
import os
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, roc_curve, auc
import warnings
warnings.filterwarnings('ignore')

def main():
    os.makedirs('results', exist_ok=True)
    
    metrics_file = open('results/metrics.txt', 'w')
    def log_print(text):
        print(text)
        metrics_file.write(text + '\n')
        
    log_print("Mulai proses Machine Learning untuk Deteksi Mirai Infection...")
    
    # 1. Load Data
    file_path = 'data/mirai_dataset.csv'
    log_print(f"Loading data dari {file_path}...")
    df = pd.read_csv(file_path)
    log_print(f"Total baris awal: {df.shape[0]}, Kolom: {df.shape[1]}")
    
    # 2. Distribusi Data Awal
    plt.figure(figsize=(8, 6))
    label_counts = df['label'].value_counts()
    sns.barplot(x=label_counts.index, y=label_counts.values, palette='Blues_d')
    plt.title('Distribusi Dataset Sebelum SMOTE', fontsize=14)
    plt.xlabel('Kategori (Benign / Mirai Infection)', fontsize=12)
    plt.ylabel('Jumlah Data', fontsize=12)
    for i, count in enumerate(label_counts.values):
        plt.text(i, count, f'{count:,}', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.savefig('results/distribusi_sebelum_smote.png')
    log_print("Distribusi awal disimpan di 'results/distribusi_sebelum_smote.png'")
    
    # 3. Preprocessing
    cols_to_drop = [
        'frame.time', 'eth.src', 'eth.dst', 'ip.src', 'ip.dst', 
        'ip.checksum', 'tcp.checksum'
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    df = df.fillna(0)
    
    # Label ke binary (0: Benign, 1: Telnet Brute Force)
    df['is_attack'] = (df['label'] == 'Telnet Brute Force').astype(int)
    log_print("\nDistribusi Kelas Target (0: Benign, 1: Mirai Infection):")
    log_print(str(df['is_attack'].value_counts()))
    df = df.drop(columns=['label'])
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = df[col].astype('category').cat.codes
        
    X = df.drop(columns=['is_attack'])
    y = df['is_attack']
    
    # Train-Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # SMOTE (Hanya di Data Training)
    log_print("\nMenerapkan SMOTE pada data training untuk menyeimbangkan kelas...")
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)
    log_print(f"Bentuk X_train setelah SMOTE: {X_train_smote.shape}")
    
    # 4. Training Random Forest
    log_print("\nMelatih model Random Forest...")
    start_time = time.time()
    rf = RandomForestClassifier(n_estimators=50, max_depth=20, n_jobs=-1, random_state=42)
    rf.fit(X_train_smote, y_train_smote)
    rf_time = time.time() - start_time
    
    # 5. Training Linear SVM
    log_print(f"Random Forest selesai dalam {rf_time:.2f} detik. Mulai melatih model SVM (LinearSVC)...")
    start_time = time.time()
    svm = LinearSVC(random_state=42, dual=False, max_iter=2000)
    svm.fit(X_train_smote, y_train_smote)
    svm_time = time.time() - start_time
    log_print(f"SVM selesai dalam {svm_time:.2f} detik.")
    
    models = {
        "Random Forest": rf,
        "Support Vector Machine": svm
    }
    
    # 6. Evaluasi dan Visualisasi
    log_print("\n" + "="*40)
    log_print("HASIL EVALUASI MODEL")
    log_print("="*40)
    
    for name, model in models.items():
        preds = model.predict(X_test_scaled)
        
        # Classification Report
        report = classification_report(y_test, preds, target_names=["Benign", "Mirai Infection"])
        log_print(f"\n[ {name} ]")
        log_print(report)
        
        # Confusion Matrix Plot
        cm = confusion_matrix(y_test, preds)
        plt.figure(figsize=(6,5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Benign", "Mirai Infection"], yticklabels=["Benign", "Mirai Infection"])
        plt.title(f'Confusion Matrix - {name}')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        cm_filename = f"results/cm_{name.replace(' ', '_').lower()}.png"
        plt.savefig(cm_filename)
        log_print(f"Confusion matrix disimpan di {cm_filename}")
        
    # 7. ROC Curve Plot
    plt.figure(figsize=(8,6))
    for name, model in models.items():
        if name == "Support Vector Machine":
            y_scores = model.decision_function(X_test_scaled)
        else:
            y_scores = model.predict_proba(X_test_scaled)[:, 1]
            
        fpr, tpr, _ = roc_curve(y_test, y_scores)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, lw=2, label=f'{name} (AUC = {roc_auc:.3f})')
        
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('results/roc_curve.png')
    log_print("ROC Curve disimpan di 'results/roc_curve.png'")
    
    log_print("="*40)
    log_print("Proses selesai.")
    metrics_file.close()

if __name__ == "__main__":
    main()
