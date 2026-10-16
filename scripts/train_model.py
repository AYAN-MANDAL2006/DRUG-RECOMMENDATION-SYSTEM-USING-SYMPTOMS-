"""
scripts/train_model.py
----------------------
Machine Learning model training script for Drug Recommendation System.
Trains a TF-IDF Vectorizer + Multinomial Naive Bayes classifier on dataset symptoms,
evaluates precision, recall, F1-score, and accuracy, and exports model artifacts.
"""

import os
import sys
import pandas as pd
import numpy as np
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from config import Config


def train_and_save_model():
    print("==================================================")
    print("TRAINING MACHINE LEARNING MODEL (TF-IDF + NAIVE BAYES)")
    print("==================================================")

    dataset_path = os.path.join(Config.DATA_DIR, 'Diseases_and_Symptoms_dataset.csv')
    if not os.path.exists(dataset_path):
        print("Error: Dataset file not found.")
        return

    df = pd.read_csv(dataset_path)
    if df.empty or 'Symptoms' not in df.columns or 'Disease' not in df.columns:
        print("Error: Invalid or empty dataset.")
        return

    # Prepare dataset with symptom permutations for robust multi-class training
    training_data = []
    for idx, row in df.iterrows():
        disease = str(row['Disease']).strip()
        syms_raw = str(row['Symptoms']).strip().replace(';', ' ').replace(',', ' ').lower()
        training_data.append({'Disease': disease, 'FeatureText': syms_raw})

        # Augment with individual symptom tokens for better model recall
        sym_list = [s.strip() for s in str(row['Symptoms']).replace(';', ',').split(',') if s.strip()]
        for s in sym_list:
            training_data.append({'Disease': disease, 'FeatureText': s.lower()})

    df_augmented = pd.DataFrame(training_data)

    X = df_augmented['FeatureText']
    y = df_augmented['Disease']

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X_vectorized = vectorizer.fit_transform(X)

    # Train Naive Bayes Classifier
    classifier = MultinomialNB(alpha=0.1)

    # Evaluate on full dataset
    classifier.fit(X_vectorized, y)
    y_pred = classifier.predict(X_vectorized)

    acc = accuracy_score(y, y_pred)
    prec = precision_score(y, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y, y_pred, average='weighted', zero_division=0)

    print("\nModel Evaluation Metrics:")
    print(f"  Training Samples: {len(df_augmented)}")
    print(f"  Accuracy:         {acc:.4f}")
    print(f"  Precision:        {prec:.4f}")
    print(f"  Recall:           {rec:.4f}")
    print(f"  F1-Score:         {f1:.4f}")

    # Ensure models directory exists
    os.makedirs(Config.MODELS_DIR, exist_ok=True)

    # Save model artifacts
    joblib.dump(classifier, Config.MODEL_PATH)
    joblib.dump(vectorizer, Config.VECTORIZER_PATH)

    print("\nModel artifacts exported successfully.")
    print("==================================================")


if __name__ == '__main__':
    train_and_save_model()
