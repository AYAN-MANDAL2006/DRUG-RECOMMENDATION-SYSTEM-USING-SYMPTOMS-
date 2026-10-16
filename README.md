# DRUG RECOMMENDATION SYSTEM BASED ON SYMPTOMS

A complete, ready-to-run academic web application built for B.Tech CSE (AI/ML) project demonstration using **Python**, **Flask**, **Basic NLP**, **Scikit-Learn (TF-IDF + Naive Bayes)**, and **SQLite**.

---

## 1. Project Overview

The **Drug Recommendation System Based on Symptoms** provides users with reliable, **EDUCATIONAL information** about commonly used Over-The-Counter (OTC) medicines for basic health symptoms. The user enters symptoms in plain natural language, which are processed using NLP, matched against a structured relational dataset using explainable ML, and displayed alongside precautions, side effects, and safety disclaimers.

> [!IMPORTANT]
> **Safety & Non-Diagnostic Notice:**
> - This is **NOT** a medical diagnostic system.
> - This is **NOT** an autonomous prescription engine.
> - The application does not calculate personalized dosage or treatment duration.
> - Emergency symptoms (e.g., chest pain, shortness of breath) immediately trigger urgent emergency care warnings and withhold medicine suggestions.

---

## 2. Problem Statement

Many individuals search the internet for health symptoms and encounter confusing, unstructured medical information or misleading diagnostic tools. Students and researchers require a transparent, explainable educational platform that demonstrates how NLP, Machine Learning, and Relational Databases can safely process symptom queries and retrieve structured OTC drug information with clear disclaimers.

---

## 3. Key Objectives

1. Process natural language symptom inputs using lightweight NLP techniques.
2. Normalize informal symptoms and medical synonyms (e.g., *"head ache"* → *"headache"*).
3. Implement explainable matching using TF-IDF vectorization and Naive Bayes / overlap similarity.
4. Maintain a normalized 3NF SQLite database (`database.db`).
5. Enforce strict medical safety disclaimers across all application pages.

---

## 4. Key Features

- **Natural Language Input**: Free-form text input with interactive example symptom tags.
- **NLP Preprocessing Engine**: Tokenization, lowercasing, stopword removal, and synonym normalization.
- **Explainable Match Scores**: Transparent similarity scores (e.g., `Match Score: 0.85`) instead of misleading probability percentages.
- **Searchable Medicine Catalog**: Search OTC medicines by name, generic name, category, or symptom keyword.
- **Dynamic Telemetry Dashboard**: Real-time total counts of symptoms, conditions, medicines, and feedback entries from SQLite.
- **Emergency Safety Guard**: Immediate emergency warnings for red-flag symptoms (chest pain, breathlessness, etc.).
- **User Feedback Module**: Rating and feedback form stored directly in SQLite database.
- **Responsive Healthcare UI**: Modern teal/blue design built with Vanilla CSS3.

---

## 5. Technology Stack

- **Backend**: Python 3.11, Flask
- **Data Processing**: Pandas, NumPy
- **Natural Language Processing**: Basic NLP (NLTK-style tokenization, stopword removal, synonym mapping)
- **Machine Learning**: Scikit-Learn (TF-IDF Vectorizer + Multinomial Naive Bayes / Cosine Similarity)
- **Database**: SQLite3
- **Frontend**: HTML5, Vanilla CSS3, Jinja2 Templates, Vanilla JavaScript
- **Testing**: Pytest

---

## 6. System Architecture

```
User Input (Natural Language Text)
       │
       ▼
  Flask Web App (app.py)
       │
       ├──► Emergency Guard (src/safety.py) ──► Emergency Warning Banner
       │
       ├──► NLP Processor (src/nlp_processor.py)
       │     ├── Lowercasing & Punctuation Stripping
       │     ├── Stopword Removal
       │     └── Synonym Normalization
       │
       ├──► Recommender Engine (src/recommender.py)
       │     ├── TF-IDF Vectorizer + Naive Bayes Classifier
       │     └── Explainable Overlap Score
       │
       └──► SQLite Database (database.db)
             ├── symptoms, conditions, medicines, condition_symptoms, condition_medicines
             └── feedback
```

---

## 7. Installation & Setup Guide

### Step 1: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run Data Preprocessing & Validation

```bash
python scripts/preprocess_data.py
```

### Step 4: Initialize SQLite Database

```bash
python scripts/initialize_db.py
```

### Step 5: Train Machine Learning Model

```bash
python scripts/train_model.py
```

### Step 6: Start Flask Web Application

```bash
python app.py
```

Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 8. Running Automated Unit Tests

Execute `pytest` to run all 13 unit tests across NLP, ML recommender, database DAO, and safety guard modules:

```bash
python -m pytest
```

---

## 9. Project Directory Structure

```
DRUG RECOMMENDATION ANTIGRAVITY/
├── app.py                      # Main Flask application entry point
├── config.py                   # Global configuration & safety disclaimers
├── requirements.txt            # Lightweight Python dependencies
├── database.db                 # SQLite database (generated)
├── data_validation_report.txt  # Dataset inspection report (generated)
├── README.md                   # Main project documentation
│
├── data/                       # Dataset directory
│   ├── Diseases_and_Symptoms_dataset.csv
│   ├── medications.csv
│   └── precautions.csv
│
├── models/                     # Trained ML artifacts (generated)
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── src/                        # Core Python source code
│   ├── __init__.py
│   ├── nlp_processor.py        # Tokenization, stopword removal & synonym mapping
│   ├── database.py             # SQLite DAO & parameterized queries
│   ├── recommender.py          # TF-IDF similarity & match score engine
│   ├── safety.py               # Emergency symptom detector & safety rules
│   └── utils.py                # Text sanitization helpers
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── analyzer.html
│   ├── results.html
│   ├── medicines.html
│   ├── medicine_detail.html
│   ├── about.html
│   ├── how_it_works.html
│   ├── disclaimer.html
│   ├── feedback.html
│   ├── admin_stats.html
│   ├── 404.html
│   └── 500.html
│
├── static/                     # Web assets
│   ├── css/
│   │   └── style.css           # Healthcare design system stylesheet
│   └── js/
│       └── main.js             # Interactive tag insertion & form handlers
│
├── scripts/                    # CLI execution scripts
│   ├── preprocess_data.py
│   ├── initialize_db.py
│   └── train_model.py
│
├── tests/                      # Automated unit test suite
│   ├── test_nlp.py
│   ├── test_recommender.py
│   ├── test_database.py
│   └── test_safety.py
│
└── docs/                       # Academic viva documentation
    ├── architecture.md
    ├── database_schema.md
    ├── nlp_methodology.md
    ├── ml_methodology.md
    └── testing.md
```

---

## 10. Screenshots Placeholder

*(Screenshots can be captured when running `http://127.0.0.1:5000`)*
- **Home Page Hero & Dashboard Stats**
- **Symptom Analyzer Interface**
- **Symptom Analysis Results Report**
- **Medicine Directory Search**
- **Emergency Safety Warning**

---

## 11. Limitations & Future Scope

### Current Limitations:
- Designed for academic educational purposes with a curated dataset.
- Supports English language symptom inputs.
- Intended for non-emergency, basic OTC symptom information.

### Future Scope:
- Integration of multilingual NLP symptom support.
- Expansion of the educational OTC drug database.
- Integration of voice-to-text symptom description.

---

## 12. Safety Disclaimer

This system is developed strictly for educational and academic evaluation as part of a B.Tech CSE (AI/ML) degree project. It is **NOT** a substitute for professional medical advice, clinical diagnosis, or treatment. Always consult a qualified healthcare professional before starting or changing any medication.
