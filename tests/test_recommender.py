"""
tests/test_recommender.py
--------------------------
Unit tests for symptom recommendation engine, match scores, empty input,
and emergency handling.
"""

from src.recommender import SymptomRecommender


def test_recommendation_flow():
    rec = SymptomRecommender()
    result = rec.recommend("I have fever and headache")

    assert result['is_emergency'] is False
    assert "fever" in result['recognized_symptoms']
    assert "headache" in result['recognized_symptoms']
    assert len(result['matched_conditions']) > 0
    assert result['matched_conditions'][0]['match_score'] > 0


def test_recommendation_empty_input():
    rec = SymptomRecommender()
    result = rec.recommend("  ")
    assert result['is_emergency'] is False
    assert len(result['recognized_symptoms']) == 0
    assert len(result['matched_conditions']) == 0


def test_recommendation_emergency_trigger():
    rec = SymptomRecommender()
    result = rec.recommend("I have severe chest pain and unconsciousness")
    assert result['is_emergency'] is True
    assert result['emergency_warning'] is not None
    assert len(result['medicines']) == 0
