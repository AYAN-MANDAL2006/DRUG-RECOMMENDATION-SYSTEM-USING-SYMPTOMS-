import os

class Config:
    """Flask application configuration settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'drug-recommendation-academic-project-secret-key-2026')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    MODEL_PATH = os.path.join(MODELS_DIR, 'model.pkl')
    VECTORIZER_PATH = os.path.join(MODELS_DIR, 'vectorizer.pkl')
    SYMPTOM_SEARCH_PATH = os.path.join(DATA_DIR, 'symptom_search_dataset.csv')
    
    # NLP & Matching Configuration
    MIN_MATCH_SCORE_THRESHOLD = 0.15
    MAX_RECOMMENDATION_RESULTS = 3

    # Safety Disclaimer
    DISCLAIMER_TEXT = (
        "IMPORTANT NOTICE: This system provides educational medicine information only based on matched symptoms. "
        "It is NOT a medical diagnosis tool or an autonomous prescription system. "
        "Always consult a qualified healthcare professional before taking, stopping, or altering any medication."
    )
