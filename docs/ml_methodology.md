# Machine Learning Methodology

## Objectives

The machine learning pipeline provides explainable matching between extracted symptoms and database health conditions.

## Model Selection

We selected **TF-IDF (Term Frequency - Inverse Document Frequency) Vectorization** combined with **Multinomial Naive Bayes** and **Jaccard/Cosine Overlap Similarity**.

### Why Naive Bayes & TF-IDF?
1. **Explainability**: High interpretability suitable for viva defense.
2. **Efficiency**: Lightweight execution requiring minimal computational resources.
3. **Probabilistic Basis**: Based on Bayes' Theorem:
   \( P(Condition | Symptoms) = \frac{P(Symptoms | Condition) \cdot P(Condition)}{P(Symptoms)} \)

## Transparent Scoring

Instead of displaying misleading diagnostic probability percentages (e.g., *"You have an 82% chance of disease X"*), the system presents an explicit **Match Score** (e.g., `Match Score: 0.82`) derived from TF-IDF feature overlap.

## Model Evaluation Metrics

Metric results generated during training (`scripts/train_model.py`):
- **Accuracy**: Measure of correct condition classification.
- **Precision**: Ratio of true positive matches.
- **Recall**: Ability to retrieve all relevant conditions.
- **F1-Score**: Harmonic mean of precision and recall.
