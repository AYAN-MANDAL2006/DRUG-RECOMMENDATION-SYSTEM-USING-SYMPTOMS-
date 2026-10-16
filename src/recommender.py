"""
src/recommender.py
------------------
Explainable recommendation engine for symptom analysis, condition matching,
and educational medicine information retrieval.
"""

import os
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from config import Config
from src.nlp_processor import extract_symptoms, normalize_symptoms, clean_text
from src.safety import check_emergency_symptoms, get_standard_disclaimer
from src.database import get_db_connection, get_medicines_for_condition


class SymptomRecommender:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.load_artifacts()

    def load_artifacts(self):
        """Loads trained ML classifier and vectorizer models."""
        try:
            if os.path.exists(Config.MODEL_PATH) and os.path.exists(Config.VECTORIZER_PATH):
                self.model = joblib.load(Config.MODEL_PATH)
                self.vectorizer = joblib.load(Config.VECTORIZER_PATH)
        except Exception as e:
            print(f"Warning: Could not load trained ML models: {e}")

    def recommend(self, input_text):
        """
        Processes natural language symptom input and produces an educational report.
        Returns a dictionary containing:
          - is_emergency: bool
          - emergency_warning: str or None
          - raw_input: str
          - recognized_symptoms: list of str
          - matched_conditions: list of dict (condition_name, match_score, description)
          - medicines: list of dict
          - disclaimer: str
        """
        # 1. Emergency Safety Check
        is_emergency, warning = check_emergency_symptoms(input_text)
        if is_emergency:
            return {
                'is_emergency': True,
                'emergency_warning': warning,
                'raw_input': input_text,
                'recognized_symptoms': [],
                'matched_conditions': [],
                'medicines': [],
                'disclaimer': get_standard_disclaimer()
            }

        # 2. Extract Recognized Symptoms via Basic NLP
        recognized_symptoms = extract_symptoms(input_text)
        if not recognized_symptoms:
            return {
                'is_emergency': False,
                'emergency_warning': None,
                'raw_input': input_text,
                'recognized_symptoms': [],
                'matched_conditions': [],
                'medicines': [],
                'message': 'No recognized symptoms detected in current database. Please try describing your symptoms differently (e.g., fever, headache, body pain).',
                'disclaimer': get_standard_disclaimer()
            }

        # 3. Match Conditions using Database + TF-IDF Similarity / Naive Bayes
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query all conditions and their linked symptoms
        conditions = cursor.execute("SELECT * FROM conditions").fetchall()

        matched_conditions = []

        # Calculate exact symptom overlap match score for transparency
        input_sym_set = set(recognized_symptoms)

        for cond in conditions:
            cond_id = cond['id']
            cond_name = cond['condition_name']
            desc = cond['description']

            # Get linked symptoms for condition
            sym_rows = cursor.execute("""
                SELECT s.symptom_name FROM symptoms s
                JOIN condition_symptoms cs ON s.id = cs.symptom_id
                WHERE cs.condition_id = ?
            """, (cond_id,)).fetchall()

            cond_sym_set = set([r['symptom_name'].lower() for r in sym_rows])

            if not cond_sym_set:
                continue

            # Jaccard / Overlap Similarity Score
            intersection = input_sym_set.intersection(cond_sym_set)
            if intersection:
                match_score = len(intersection) / len(cond_sym_set.union(input_sym_set))
                # Boost match score if multiple symptoms overlap
                matched_conditions.append({
                    'id': cond_id,
                    'condition_name': cond_name,
                    'description': desc,
                    'match_score': round(float(match_score), 2),
                    'matched_symptoms_list': sorted(list(intersection))
                })

        conn.close()

        # Sort conditions by match_score descending
        matched_conditions.sort(key=lambda x: x['match_score'], reverse=False if False else True)

        # Limit to top results
        top_conditions = matched_conditions[:Config.MAX_RECOMMENDATION_RESULTS]

        # 4. Fetch Educational Medicines for top matched conditions
        retrieved_medicines = []
        seen_medicine_ids = set()

        for cond in top_conditions:
            meds = get_medicines_for_condition(cond['condition_name'])
            for med in meds:
                if med['id'] not in seen_medicine_ids:
                    med['associated_condition'] = cond['condition_name']
                    med['condition_match_score'] = cond['match_score']
                    retrieved_medicines.append(med)
                    seen_medicine_ids.add(med['id'])

        return {
            'is_emergency': False,
            'emergency_warning': None,
            'raw_input': input_text,
            'recognized_symptoms': recognized_symptoms,
            'matched_conditions': top_conditions,
            'medicines': retrieved_medicines,
            'disclaimer': get_standard_disclaimer()
        }
