"""
preprocess_data.py
------------------
Data preprocessing and validation script for Drug Recommendation System.
Inspects CSV datasets, cleans missing/duplicate data, normalizes strings,
and generates a data validation report.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORT_FILE = os.path.join(BASE_DIR, 'data_validation_report.txt')


def inspect_and_preprocess():
    print("==================================================")
    print("STARTING DATASET INSPECTION AND PREPROCESSING")
    print("==================================================")

    report_lines = []
    report_lines.append("DRUG RECOMMENDATION SYSTEM - DATA VALIDATION REPORT\n")
    report_lines.append("====================================================\n")

    files_to_check = {
        'Diseases_and_Symptoms': os.path.join(DATA_DIR, 'Diseases_and_Symptoms_dataset.csv'),
        'Medications': os.path.join(DATA_DIR, 'medications.csv'),
        'Precautions': os.path.join(DATA_DIR, 'precautions.csv')
    }

    for name, path in files_to_check.items():
        report_lines.append(f"\n--- DATASET: {name} ---")
        if not os.path.exists(path):
            msg = f"CRITICAL: File not found at {path}"
            print(msg)
            report_lines.append(msg)
            continue

        try:
            df = pd.read_csv(path)
            print(f"\n[+] Loaded {name} successfully.")
            print(f"    Rows: {len(df)}, Columns: {len(df.columns)}")
            print(f"    Columns detected: {list(df.columns)}")

            report_lines.append(f"File Path: {path}")
            report_lines.append(f"Total Rows: {len(df)}")
            report_lines.append(f"Detected Columns: {list(df.columns)}")

            # Check missing / NaN values
            null_counts = df.isnull().sum()
            report_lines.append(f"Missing Values per Column:\n{null_counts.to_string()}")

            # Check duplicates
            dup_count = df.duplicated().sum()
            report_lines.append(f"Duplicate Rows Count: {dup_count}")

            if dup_count > 0:
                df = df.drop_duplicates().reset_index(drop=True)
                print(f"    Removed {dup_count} duplicate rows.")

            # String cleaning
            for col in df.columns:
                if df[col].dtype == object:
                    df[col] = df[col].astype(str).str.strip()

            # Overwrite cleaned CSV
            df.to_csv(path, index=False)
            report_lines.append("Status: Successfully validated, cleaned, and saved.")

        except Exception as e:
            error_msg = f"ERROR processing {name}: {str(e)}"
            print(error_msg)
            report_lines.append(error_msg)

    # Save report file
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print("\n==================================================")
    print("Validation report saved successfully.")
    print("==================================================")


if __name__ == '__main__':
    inspect_and_preprocess()
