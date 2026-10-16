"""
src/safety.py
-------------
Safety validation, emergency symptom filtering, and non-prescriptive disclaimers
for the Drug Recommendation System.
"""

# Red-flag emergency symptom patterns
EMERGENCY_SYMPTOMS = [
    'chest pain', 'severe chest pain', 'difficulty breathing', 'shortness of breath',
    'breathlessness', 'unconscious', 'unconsciousness', 'fainted', 'fainting',
    'severe bleeding', 'uncontrolled bleeding', 'seizure', 'fits', 'convulsions',
    'stroke', 'numbness on one side', 'slurred speech', 'paralysis', 'chest tightness',
    'coughing blood', 'vomiting blood', 'bluish lips', 'severe head injury'
]


def check_emergency_symptoms(text):
    """
    Evaluates input text for high-risk emergency medical keywords.
    Returns (is_emergency: bool, warning_message: str or None).
    """
    if not text:
        return False, None

    text_lower = text.lower()
    detected_emergency_terms = []

    for term in EMERGENCY_SYMPTOMS:
        if term in text_lower:
            detected_emergency_terms.append(term)

    if detected_emergency_terms:
        warning_msg = (
            "URGENT HEALTH SAFETY NOTICE: The entered text contains symptoms ("
            f"'{', '.join(detected_emergency_terms)}') that may require immediate emergency medical care. "
            "Please seek immediate attention at the nearest emergency room or consult a qualified physician immediately. "
            "Educational medicine information is withheld for emergency symptoms."
        )
        return True, warning_msg

    return False, None


def get_standard_disclaimer():
    """Returns the mandatory educational disclaimer text."""
    return (
        "EDUCATIONAL DISCLAIMER: This tool provides general educational information based on symptom text matching. "
        "It is NOT a medical diagnostic tool or an autonomous prescription system. "
        "Do NOT use this result to self-diagnose or alter your medical treatment. "
        "Always consult a qualified healthcare professional before taking any medication."
    )
