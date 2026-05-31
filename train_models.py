import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, classification_report
import warnings
warnings.filterwarnings('ignore')

def main():
    print("Mulai proses Machine Learning...")
    
    # 1. Load Data
    # Menggunakan salah satu file yang memiliki mix Benign dan Malicious yang seimbang
    file_path = 'data/processed/iotsim-air-quality-1.csv'
    print(f"Loading data dari {file_path}...")
    df = pd.read_csv(file_path)
    
    print(f"Total baris awal: {df.shape[0]}, Kolom: {df.shape[1]}")
    
    # 2. Preprocessing
    # Hapus kolom yang tidak relevan secara generalisasi (seperti waktu, MAC, IP, checksum)
    cols_to_drop = [
        'frame.time', 'eth.src', 'eth.dst', 'ip.src', 'ip.dst', 
        'ip.checksum', 'tcp.checksum'
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    # Menangani missing values
    df = df.fillna(0)
    
    # Konversi label ke binary (Benign = 0, Serangan = 1)
    df['is_attack'] = (df['label'] != 'Benign').astype(int)
    print("\nDistribusi Kelas (0: Benign, 1: Serangan):")
    print(df['is_attack'].value_counts())
    
    # Hapus kolom label asli
    df = df.drop(columns=['label'])
    
    # Encoding categorical features menggunakan One-Hot Encoding
    categorical_cols = df.select_dtypes(include=['object']).columns
    print(f"\nMelakukan encoding (Label Encoding) pada kolom kategorikal: {list(categorical_cols)}")
    for col in categorical_cols:
        df[col] = df[col].astype('category').cat.codes
    
    # 3. Pisahkan Fitur (X) dan Target (y)
    X = df.drop(columns=['is_attack'])
    y = df['is_attack']
    
    # Split Data (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale Fitur (Penting untuk SVM)
    print("\nMelakukan scaling fitur (StandardScaler)...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 4. Training Random Forest
    print("\nMelatih model Random Forest...")
    start_time = time.time()
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train_scaled, y_train)
    rf_time = time.time() - start_time
    
    # 5. Training SVM
    print(f"Random Forest selesai dalam {rf_time:.2f} detik. Mulai melatih model SVM (LinearSVC)...")
    start_time = time.time()
    svm = LinearSVC(random_state=42, dual=False, max_iter=2000)
    svm.fit(X_train_scaled, y_train)
    svm_time = time.time() - start_time
    print(f"SVM selesai dalam {svm_time:.2f} detik.")
    
    # 6. Evaluasi
    print("\n" + "="*40)
    print("HASIL EVALUASI MODEL")
    print("="*40)
    
    # Evaluasi RF
    rf_preds = rf.predict(X_test_scaled)
    rf_acc = accuracy_score(y_test, rf_preds)
    rf_f1 = f1_score(y_test, rf_preds)
    
    # Evaluasi SVM
    svm_preds = svm.predict(X_test_scaled)
    svm_acc = accuracy_score(y_test, svm_preds)
    svm_f1 = f1_score(y_test, svm_preds)
    
    print(f"[Random Forest]")
    print(f"  Accuracy : {rf_acc * 100:.2f}%")
    print(f"  F1-Score : {rf_f1 * 100:.2f}%\n")
    
    print(f"[Support Vector Machine (Linear)]")
    print(f"  Accuracy : {svm_acc * 100:.2f}%")
    print(f"  F1-Score : {svm_f1 * 100:.2f}%")
    print("="*40)
    print("Proses selesai.")

if __name__ == "__main__":
    main()
