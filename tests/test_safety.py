"""
tests/test_safety.py
---------------------
Unit tests for emergency red-flag symptom checking and safety disclaimers.
"""

from src.safety import check_emergency_symptoms, get_standard_disclaimer


def test_emergency_chest_pain():
    input_text = "I am having severe chest pain and shortness of breath"
    is_emergency, warning = check_emergency_symptoms(input_text)
    assert is_emergency is True
    assert warning is not None
    assert "chest pain" in warning.lower()


def test_non_emergency_input():
    input_text = "I have mild fever and headache"
    is_emergency, warning = check_emergency_symptoms(input_text)
    assert is_emergency is False
    assert warning is None


def test_standard_disclaimer():
    disclaimer = get_standard_disclaimer()
    assert "EDUCATIONAL DISCLAIMER" in disclaimer
    assert "NOT a medical diagnostic tool" in disclaimer
