# Deteksi Mirai Infection menggunakan Machine Learning pada Dataset Gotham 2025

Repositori ini berisi kode dan hasil eksperimen yang dikhususkan untuk **Penerapan Machine Learning Untuk Mendeteksi Serangan Mirai Infection Pada Jaringan Komputer Menggunakan Dataset Gotham 2025**. Eksperimen ini disusun sebagai bagian dari pemenuhan tugas akhir (Skripsi).

## Deskripsi Singkat
Penelitian ini berfokus pada deteksi aktivitas *Telnet Brute Force* yang merupakan mekanisme awal infeksi *botnet* Mirai. Data jaringan yang tidak wajar tersebut diklasifikasikan dengan membandingkannya terhadap trafik normal (*Benign*). 

Karena sifat dataset keamanan jaringan yang sering kali sangat tidak seimbang (imbalance), penelitian ini mengimplementasikan teknik **SMOTE (Synthetic Minority Over-sampling Technique)** pada fase pra-pemrosesan.

Dua algoritma yang dievaluasi performanya dalam repositori ini adalah:
1. **Random Forest** (Algoritma Ensemble)
2. **Support Vector Machine / SVM** (Algoritma Linear)

---

## Struktur Direktori

```text
.
├── data/
│   └── mirai_dataset.csv     # Dataset bersih yang hanya berisi Benign & Mirai Infection
├── results/                  # Folder tempat semua grafik & metrik skripsi disimpan
│   ├── cm_random_forest.png
│   ├── cm_support_vector_machine.png
│   ├── distribusi_sebelum_smote.png
│   ├── metrics.txt           # Hasil angka mentah Precision, Recall, dll.
│   └── roc_curve.png
├── train_mirai.py            # Script utama untuk klasifikasi (SMOTE, RF, SVM)
└── README.md                 # Dokumentasi ini
```

---

## Hasil Metrik Evaluasi

Kedua model dievaluasi menggunakan metrik akurasi (*Accuracy*), kepresisian (*Precision*), nilai *Recall*, *F1-Score*, *Confusion Matrix*, dan kurva *ROC-AUC*.

- **Random Forest**: Mencapai **Akurasi 100%** dengan *F1-score* 1.00 untuk kelas Mirai. Model mampu mempelajari fitur dataset Gotham secara sempurna.
- **Linear SVM**: Mencapai **Akurasi 98%** dengan tingkat *Recall* 1.00. Sangat baik dalam menangkap seluruh serangan Mirai, meskipun menghasilkan sedikit positif palsu (menganggap lalu lintas jinak sebagai serangan).

Hasil pengujian grafis dan detail angka evaluasinya bisa dilihat secara lengkap di dalam direktori `results/` dan bisa langsung diintegrasikan ke dalam Bab 4 Laporan Skripsi.

---

## Cara Menjalankan Program

Pastikan Anda sudah menginstal seluruh *library* Python yang dibutuhkan:

```bash
pip install pandas numpy scikit-learn imbalanced-learn matplotlib seaborn
```

Untuk menjalankan ulang pelatihan dari awal dan menghasilkan grafik:

```bash
python train_mirai.py
```
Kode akan secara otomatis menyimpan semua grafik hasil uji ke dalam folder `results`.
