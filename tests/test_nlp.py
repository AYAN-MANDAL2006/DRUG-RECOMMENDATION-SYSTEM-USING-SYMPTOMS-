"""
tests/test_nlp.py
------------------
Unit tests for Basic NLP preprocessing, tokenization, synonym normalization,
and symptom extraction.
"""

from src.nlp_processor import (
    clean_text, tokenize_and_remove_stopwords, normalize_symptoms, extract_symptoms
)


def test_clean_text():
    text = "I have a FEVER, and severe Headache!!!"
    cleaned = clean_text(text)
    assert cleaned == "i have a fever and severe headache"


def test_tokenize_and_remove_stopwords():
    text = "I am suffering from severe fever and headache"
    tokens = tokenize_and_remove_stopwords(text)
    assert "fever" in tokens
    assert "headache" in tokens
    assert "i" not in tokens
    assert "am" not in tokens


def test_normalize_symptoms_synonyms():
    # Test synonym mapping
    input1 = "I have head ache and high temperature"
    norm1 = normalize_symptoms(input1)
    assert "headache" in norm1
    assert "fever" in norm1

    input2 = "stomach ache and coughing"
    norm2 = normalize_symptoms(input2)
    assert "stomach pain" in norm2
    assert "cough" in norm2


def test_extract_symptoms():
    raw_input = "I am having fever, headache and body pain"
    extracted = extract_symptoms(raw_input)
    assert "fever" in extracted
    assert "headache" in extracted
    assert "body pain" in extracted
