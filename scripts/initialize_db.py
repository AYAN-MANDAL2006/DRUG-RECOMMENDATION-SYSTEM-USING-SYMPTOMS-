"""
scripts/initialize_db.py
------------------------
Initializes the SQLite database (database.db) from cleaned CSV datasets.
Populates normalized tables for symptoms, conditions, medicines, condition_symptoms,
and condition_medicines.
"""

import os
import sys
import pandas as pd
import sqlite3

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from config import Config
from src.database import init_db_schema, get_db_connection


def initialize_database():
    print("==================================================")
    print("INITIALIZING SQLITE DATABASE (database.db)")
    print("==================================================")

    # 1. Initialize schema
    init_db_schema()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing table contents for clean seed
    cursor.execute("DELETE FROM condition_medicines")
    cursor.execute("DELETE FROM condition_symptoms")
    cursor.execute("DELETE FROM medicines")
    cursor.execute("DELETE FROM conditions")
    cursor.execute("DELETE FROM symptoms")
    conn.commit()

    diseases_path = os.path.join(Config.DATA_DIR, 'Diseases_and_Symptoms_dataset.csv')
    meds_path = os.path.join(Config.DATA_DIR, 'medications.csv')
    precautions_path = os.path.join(Config.DATA_DIR, 'precautions.csv')

    df_diseases = pd.read_csv(diseases_path) if os.path.exists(diseases_path) else pd.DataFrame()
    df_meds = pd.read_csv(meds_path) if os.path.exists(meds_path) else pd.DataFrame()
    df_precautions = pd.read_csv(precautions_path) if os.path.exists(precautions_path) else pd.DataFrame()

    symptom_map = {}  # name -> id
    condition_map = {}  # name -> id
    medicine_map = {}  # name -> id

    # 2. Populate Conditions & Symptoms
    if not df_diseases.empty:
        for idx, row in df_diseases.iterrows():
            disease_name = str(row['Disease']).strip()
            description = str(row.get('Description', '')).strip()

            if disease_name not in condition_map:
                cursor.execute("INSERT INTO conditions (condition_name, description) VALUES (?, ?)",
                               (disease_name, description))
                condition_map[disease_name] = cursor.lastrowid

            cond_id = condition_map[disease_name]

            symptoms_str = str(row.get('Symptoms', ''))
            # Support both semicolon and comma delimiters
            delims = ';' if ';' in symptoms_str else ','
            symptoms_list = [s.strip().lower() for s in symptoms_str.split(delims) if s.strip()]

            for sym in symptoms_list:
                if sym not in symptom_map:
                    cursor.execute(
                        "INSERT INTO symptoms (symptom_name, normalized_name, synonyms) VALUES (?, ?, ?)",
                        (sym, sym, sym)
                    )
                    symptom_map[sym] = cursor.lastrowid

                sym_id = symptom_map[sym]

                cursor.execute(
                    "INSERT OR IGNORE INTO condition_symptoms (condition_id, symptom_id) VALUES (?, ?)",
                    (cond_id, sym_id)
                )

    # 3. Populate Medicines & Link with Conditions
    if not df_meds.empty:
        for idx, row in df_meds.iterrows():
            disease_name = str(row['Disease']).strip()
            med_name = str(row['Medicine_Name']).strip()
            generic_name = str(row.get('Generic_Name', '')).strip()
            category = str(row.get('Category', '')).strip()
            common_use = str(row.get('Common_Use', '')).strip()
            precautions = str(row.get('Precautions', '')).strip()
            side_effects = str(row.get('Side_Effects', '')).strip()
            contraindications = str(row.get('Contraindications', '')).strip()
            warning = str(row.get('Warning', '')).strip()

            # Merge precautions from precautions.csv if available
            if not df_precautions.empty and disease_name in df_precautions['Disease'].values:
                p_row = df_precautions[df_precautions['Disease'] == disease_name].iloc[0]
                p_list = [str(p_row[c]) for c in p_row.index if 'Precaution' in c and pd.notnull(p_row[c])]
                if p_list:
                    precautions += " Additional precautions: " + " | ".join(p_list)

            cursor.execute("""
                INSERT INTO medicines (medicine_name, generic_name, category, description, common_use, precautions, side_effects, contraindications, warning)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (med_name, generic_name, category, common_use, common_use, precautions, side_effects, contraindications, warning))
            
            med_id = cursor.lastrowid

            if disease_name in condition_map:
                cond_id = condition_map[disease_name]
                cursor.execute(
                    "INSERT OR IGNORE INTO condition_medicines (condition_id, medicine_id) VALUES (?, ?)",
                    (cond_id, med_id)
                )

    conn.commit()

    # Get counts
    sym_count = cursor.execute("SELECT COUNT(*) FROM symptoms").fetchone()[0]
    cond_count = cursor.execute("SELECT COUNT(*) FROM conditions").fetchone()[0]
    med_count = cursor.execute("SELECT COUNT(*) FROM medicines").fetchone()[0]
    cond_sym_count = cursor.execute("SELECT COUNT(*) FROM condition_symptoms").fetchone()[0]

    conn.close()

    print("\nDatabase initialized successfully.")
    print(f"Symptoms: {sym_count}")
    print(f"Conditions: {cond_count}")
    print(f"Medicines: {med_count}")
    print(f"Condition-Symptom Links: {cond_sym_count}")
    print("==================================================")


if __name__ == '__main__':
    initialize_database()
