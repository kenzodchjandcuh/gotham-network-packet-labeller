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
from sklearn.preprocessing import label_binarize
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
    
    # Filter dataset
    valid_labels = ['Benign', 'TCP Scan', 'File Download', 'Ingress Tool Transfer', 'C&C Communication', 'Telnet Brute Force', 'Reporting']
    df = df[df['label'].isin(valid_labels)]
    log_print(f"Total baris setelah filtering: {df.shape[0]}")

    # Downsample Benign class to prevent memory overflow during SMOTE
    benign_df = df[df['label'] == 'Benign']
    other_df = df[df['label'] != 'Benign']
    if len(benign_df) > 250000:
        log_print(f"Downsampling Benign dari {len(benign_df)} menjadi 250000 agar RAM aman...")
        benign_df = benign_df.sample(n=250000, random_state=42)
        df = pd.concat([benign_df, other_df]).reset_index(drop=True)
        log_print(f"Total baris setelah downsampling: {df.shape[0]}")
    # 2. Distribusi Data Awal
    plt.figure(figsize=(12, 6))
    label_counts = df['label'].value_counts()
    sns.barplot(x=label_counts.index, y=label_counts.values, palette='Blues_d')
    plt.title('Distribusi Dataset Sebelum SMOTE', fontsize=14)
    plt.xlabel('Kategori Serangan', fontsize=12)
    plt.ylabel('Jumlah Data', fontsize=12)
    plt.xticks(rotation=45, ha="right")
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
    
    # Encode label ke numerik (multiclass)
    label_encoder = LabelEncoder()
    df['is_attack'] = label_encoder.fit_transform(df['label'])
    target_names = list(label_encoder.classes_)
    
    log_print("\nDistribusi Kelas Target:")
    log_print(str(df['label'].value_counts()))
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
        report = classification_report(y_test, preds, target_names=target_names)
        log_print(f"\n[ {name} ]")
        log_print(report)
        
        # Confusion Matrix Plot
        cm = confusion_matrix(y_test, preds)
        plt.figure(figsize=(10,8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
        plt.title(f'Confusion Matrix - {name}')
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.tight_layout()
        cm_filename = f"results/cm_{name.replace(' ', '_').lower()}.png"
        plt.savefig(cm_filename)
        log_print(f"Confusion matrix disimpan di {cm_filename}")
        
    # 7. ROC Curve Plot
    plt.figure(figsize=(10,8))
    if len(target_names) == 2:
        for name, model in models.items():
            if name == "Support Vector Machine":
                y_scores = model.decision_function(X_test_scaled)
            else:
                y_scores = model.predict_proba(X_test_scaled)[:, 1]
                
            fpr, tpr, _ = roc_curve(y_test, y_scores)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, lw=2, label=f'{name} (AUC = {roc_auc:.3f})')
    else:
        y_test_bin = label_binarize(y_test, classes=range(len(target_names)))
        n_classes = len(target_names)
        for name, model in models.items():
            if name == "Support Vector Machine":
                y_scores = model.decision_function(X_test_scaled)
            else:
                y_scores = model.predict_proba(X_test_scaled)
                
            fpr = dict()
            tpr = dict()
            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_scores[:, i])
                
            all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))
            mean_tpr = np.zeros_like(all_fpr)
            for i in range(n_classes):
                mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
            mean_tpr /= n_classes
            
            mac_auc = auc(all_fpr, mean_tpr)
            plt.plot(all_fpr, mean_tpr, lw=2, label=f'{name} Macro-average (AUC = {mac_auc:.3f})')
            
        
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
