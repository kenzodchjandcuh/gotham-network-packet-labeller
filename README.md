# Processing Pipeline: A Device-Level Distributed IoT Network Traffic Dataset with Non-IID Characteristics for Intrusion Detection

This repository contains a pipeline for processing the network traffic dataset, including **feature extraction**, **feature cleaning**, and **data labelling**. The pipeline is designed for extensibility and reproducibility.

---

## **Table of Contents**
1. [Installation](#installation)
2. [Pipeline Tasks](#pipeline-tasks)
3. [Usage](#usage)
4. [Files and Folders Structure](#files-and-folders-structure)
5. [Requirements](#requirements)
6. [License](#license)
7. [Authors](#authors)

---

## **Installation**

* Before running the pipeline, ensure you have **Python 3.8+** and **Tshark 4.2.2** golbally installed in your computer;*. If not, you can get python [here](https://www.python.org) and tshark [here](https://tshark.dev/setup/install/).
* Then, clone the repository to your PC:
    ```bash
        $ git clone https://github.com/othmbela/gotham-network-packet-labeller.git
    ```
* ### Dependencies
    1. cd into your cloned repository as such:
        ```bash
            $ cd gotham-network-packet-labeller
        ```
    2. Initialise the project as such:
        ```bash
            $ make init
        ```
    First, the command line will create your vcirtual environment and install the dependencies needed to run the app. Then, it will create the data folders.
    3. Move the dataset to the `./data/raw` folder.

    > **Windows Users Note**: If you do not have `make` installed, you can initialize the project by running the provided PowerShell script:
    > ```powershell
    > .\init.ps1
    > ```
    > This will create the `venv`, install dependencies, and create all necessary data folders.

## **Using the Pre-Processed Zenodo Dataset**

If you downloaded the official `GothamDataset2025.zip` from Zenodo, it already contains a `processed/` folder with fully cleaned and labelled CSV files. 
You **do not** need to run the extraction or cleaning pipeline if you just want to train Machine Learning models. You can directly use the `.csv` files inside the `data/processed/` folder.


## **Pipeline Tasks**

The pipeline is divided into the following stages:

1. **Feature Extraction:** Converts raw network traffic data (e.g., pcap files) into feature datasets.
2. **Feature Cleaning:** Cleans and processes extracted features to ensure consistency.
3. **Data Labelling:** Labels the cleaned datasets with attack and benign traffic labels.
4. **Full Pipeline:** Executes all steps sequentially.


## **Usage**

### **Running Individual Steps**

You can run each stage of the pipeline individually using the Makefile. This allows you to perform specific steps as needed:

- Feature Extraction:
    ``` bash
    make extract_features
    ```
    This will extract features from raw network traffic data.

- Feature Cleaning:
    ``` bash
    make clean_features
    ```
    This will clean and preprocess the extracted feature datasets.

- Data Labelling:
    ``` bash
    make label_data
    ```
    This will label the cleaned datasets with appropriate attack/benign classifications.

### **Running the Full Pipeline**

To run all stages in sequence, execute the following command:
```bash
make run_pipeline
```

This will run feature extraction, feature cleaning, and data labelling one after the other, automating the entire pipeline.


## **Machine Learning & Utilities**

We have added a few custom scripts to help you get started with building Intrusion Detection Systems (IDS):

### **1. Training Machine Learning Models**
Use the `train_models.py` script to train and evaluate **Random Forest** and **Support Vector Machine (SVM)** on the dataset.
It automatically handles categorical label encoding, feature scaling, and prints Accuracy and F1-score.
```bash
python train_models.py
```

**Evaluation Results (Binary Classification on 55k subset):**
- **Random Forest**: Accuracy `100.00%`, F1-Score `100.00%`
- **Support Vector Machine (LinearSVC)**: Accuracy `99.11%`, F1-Score `99.49%`

### **2. Counting Dataset Labels**
Use the `count_all_labels.py` script to quickly aggregate the distribution of attack categories (e.g., Mirai, Merlin, Benign) across all CSV files in the `data/processed/` directory.
```bash
python count_all_labels.py
```

**Dataset Distribution Overview (Total 35,133,026 Records):**
- **Benign**: 12,256,883
- **Mirai UDP Flooding**: 8,897,895
- **Mirai TCP Flooding**: 6,548,173
- **Mirai GRE Flooding**: 5,911,401
- **TCP Scan**: 737,764
- **CoAP Amplification**: 274,837
- **Telnet Brute Force**: 227,649
- **Merlin TCP Flooding**: 120,000
- **Merlin ICMP Flooding**: 57,580
- **Merlin UDP Flooding**: 29,996
- **Merlin C&C Communication**: 29,356
- **Ingress Tool Transfer**: 21,587
- **Unknown**: 7,670
- **File Download**: 7,196
- **UDP Scan**: 4,242
- **Mirai C&C Communication**: 1,074
- **C&C Communication**: 528
- **Reporting**: 450


## **Files and Folders Structure**

The pipeline expects the following directory structure:
```
    ├── bash_scripts/
    │
    ├── data/
    │   ├── raw/                     # Raw network traffic data (input)
    │   ├── extracted_features/      # Extracted features (output from feature extraction)
    │   ├── cleaned_features/        # Cleaned features (output from feature cleaning)
    │   └── labeled_data/            # Labeled data (output from labelling)
    │
    ├── features/
    ├── images/
    ├── metadata/
    ├── notebooks/
    │
    ├── scripts/
    │   ├── run_cleaning.py
    │   ├── run_extraction.py
    │   └── run_labelling.py
    │
    ├── src/
    │   ├── __init__.py
    │   ├── feature_cleaner.py
    │   ├── feature_extractor.py
    │   ├── labeller.py
    │   └── utils.py
    │
    ├── venv/
    ├── .dockerignore
    ├── .gitignore
    ├── Dockerfile
    ├── Makefile
    ├── README.md
    └── requirements.txt
```


## Requirements

All the experiments were conducted using a 64-bit Intel(R) Core(TM) i7-7500U CPU with 16GB RAM in Windows 10 environment.


## License

This project is released under the [Apache 2.0 license](LICENSE)


## Authors

**Othmane Belarbi**


## Citation

If you find this code useful in your research, please cite this article as:
```bibtex
@misc{belarbi2025gothamdataset2025reproducible,
      title={Gotham Dataset 2025: A Reproducible Large-Scale IoT Network Dataset for Intrusion Detection and Security Research}, 
      author={Othmane Belarbi and Theodoros Spyridopoulos and Eirini Anthi and Omer Rana and Pietro Carnelli and Aftab Khan},
      year={2025},
      eprint={2502.03134},
      archivePrefix={arXiv},
      primaryClass={cs.CR},
      url={https://arxiv.org/abs/2502.03134}, 
}
```

