import pandas as pd
import glob
import os

def rebuild():
    print("Rebuilding mirai_dataset.csv...")
    benign_files = glob.glob("data/labelled/benign/*.csv")
    malicious_files = glob.glob("data/labelled/malicious/mirai-infection/*.csv")
    
    all_files = benign_files + malicious_files
    print(f"Found {len(benign_files)} benign files and {len(malicious_files)} malicious files.")
    
    df_list = []
    for f in all_files:
        df = pd.read_csv(f, sep="\t", low_memory=False)
        df_list.append(df)
        
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        # Check label distribution
        print("Label Distribution:")
        print(combined_df['label'].value_counts())
        
        # Save to mirai_dataset.csv
        # Using comma separator as train_mirai.py uses pd.read_csv without sep parameter (default is comma)
        # But wait! The earlier mirai_dataset.csv had comma separator.
        combined_df.to_csv("data/mirai_dataset.csv", index=False, sep=",")
        print("Saved to data/mirai_dataset.csv")
    else:
        print("No data found!")

if __name__ == "__main__":
    rebuild()
