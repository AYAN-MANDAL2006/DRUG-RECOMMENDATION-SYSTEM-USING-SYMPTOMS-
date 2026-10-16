"""
src/nlp_processor.py
--------------------
Basic NLP module for text preprocessing, tokenization, stopword removal,
symptom extraction, synonym normalization, and term mapping.
"""

import re
import string

# Standard English stopwords fallback set
ENGLISH_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
    'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
    'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't",
    'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",
    'suffering', 'feeling', 'got', 'have', 'having', 'severe', 'mild', 'bad', 'lot'
}

# Explicit Medical Symptom Synonym Dictionary
SYNONYM_MAP = {
    'head ache': 'headache',
    'headaches': 'headache',
    'temperature': 'fever',
    'high temp': 'fever',
    'high temperature': 'fever',
    'febrile': 'fever',
    'stomach ache': 'stomach pain',
    'stomachache': 'stomach pain',
    'abdominal pain': 'stomach pain',
    'belly pain': 'stomach pain',
    'belly ache': 'stomach pain',
    'body ache': 'body pain',
    'body paining': 'body pain',
    'body aches': 'body pain',
    'muscle ache': 'muscle ache',
    'muscle pain': 'muscle ache',
    'coughing': 'cough',
    'coughed': 'cough',
    'throat pain': 'sore throat',
    'scratchy throat': 'sore throat',
    'throat irritation': 'sore throat',
    'runny nose': 'runny nose',
    'nasal congestion': 'runny nose',
    'stuffy nose': 'runny nose',
    'watery eyes': 'watery eyes',
    'vomiting': 'vomiting',
    'throwing up': 'vomiting',
    'loose motion': 'diarrhea',
    'loose stools': 'diarrhea',
    'skin rash': 'skin rash',
    'red rash': 'skin rash',
    'itchy skin': 'itching',
    'itching': 'itching',
    'joint pain': 'joint pain',
    'painful joints': 'joint pain',
    'sleeplessness': 'difficulty sleeping',
    'can not sleep': 'difficulty sleeping',
    'cant sleep': 'difficulty sleeping',
    'insomnia': 'difficulty sleeping'
}

# Known Database Symptoms Dictionary for Exact/Partial Matching
KNOWN_SYMPTOMS = [
    'fever', 'headache', 'cough', 'sore throat', 'runny nose', 'sneezing',
    'body pain', 'chills', 'fatigue', 'sweating', 'neck pain', 'muscle tension',
    'sensitivity to light', 'muscle ache', 'heartburn', 'stomach pain', 'nausea',
    'chest discomfort', 'sour taste', 'vomiting', 'diarrhea', 'cramps', 'watery eyes',
    'itching', 'stiffness', 'dizziness', 'difficulty swallowing', 'bloating',
    'infrequent bowel movement', 'restlessness', 'difficulty sleeping', 'anxiety',
    'skin rash', 'redness', 'skin irritation', 'swelling', 'throat irritation',
    'dry throat', 'fullness', 'shortness of breath', 'painful urination',
    'lower abdominal pain', 'frequent urination', 'wheezing', 'joint pain', 'limping'
]


def clean_text(text):
    """Converts text to lower case and removes unnecessary punctuation."""
    if not text:
        return ""
    text = text.lower()
    # Remove punctuation except spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize_and_remove_stopwords(text):
    """Tokenizes clean text and removes standard English stopwords."""
    cleaned = clean_text(text)
    words = cleaned.split()
    filtered_words = [w for w in words if w not in ENGLISH_STOPWORDS]
    return filtered_words


def normalize_symptoms(text):
    """
    Normalizes symptom synonyms in the input text.
    Example: 'I have head ache and temperature' -> 'I have headache and fever'
    """
    cleaned = clean_text(text)

    # First pass: multi-word synonym replacement
    for syn, target in SYNONYM_MAP.items():
        pattern = r'\b' + re.escape(syn) + r'\b'
        cleaned = re.sub(pattern, target, cleaned)

    return cleaned


def extract_symptoms(text):
    """
    Extracts recognized symptoms from natural language input.
    Returns a list of identified normalized symptom strings.
    """
    if not text or not text.strip():
        return []

    normalized_input = normalize_symptoms(text)
    extracted = set()

    # Match multi-word symptoms first
    for symptom in KNOWN_SYMPTOMS:
        pattern = r'\b' + re.escape(symptom) + r'\b'
        if re.search(pattern, normalized_input):
            extracted.add(symptom)

    # Token fallback check for single word symptoms
    tokens = tokenize_and_remove_stopwords(normalized_input)
    for token in tokens:
        if token in KNOWN_SYMPTOMS:
            extracted.add(token)

    return sorted(list(extracted))
