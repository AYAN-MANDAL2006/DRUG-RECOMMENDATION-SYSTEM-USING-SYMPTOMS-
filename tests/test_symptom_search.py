"""
tests/test_symptom_search.py
----------------------------
Automated unit tests for symptom search functionality using Pandas.
Tests case-insensitive partial matching, search_terms synonym matching,
multi-result completeness, and robust error handling.
"""

import os
import tempfile
import pytest
import pandas as pd

from src.symptom_search import (
    load_symptom_dataset, search_symptoms, get_all_symptoms, get_categories
)
from app import app


def test_load_dataset_success():
    """Verify that dataset loads successfully into Pandas DataFrame with expected columns."""
    df = load_symptom_dataset(force_reload=True)
    assert not df.empty
    assert 'symptom_name' in df.columns
    assert 'search_terms' in df.columns
    assert len(df) > 100


def test_search_head():
    """Verify typing 'head' returns 'Headache', 'Migraine', and relevant symptoms."""
    results = search_symptoms("head")
    assert len(results) > 0
    names = [r['symptom_name'] for r in results]
    assert "Headache" in names
    # Headache should be ranked first because it starts with 'head'
    assert names[0] == "Headache"


def test_search_fever():
    """Verify typing 'fever' returns 'Fever'."""
    results = search_symptoms("fever")
    assert len(results) > 0
    names = [r['symptom_name'] for r in results]
    assert "Fever" in names


def test_search_cough():
    """Verify typing 'cough' returns 'Cough', 'Dry cough', 'Wet cough', 'Phlegm'."""
    results = search_symptoms("cough")
    assert len(results) >= 4
    names = [r['symptom_name'] for r in results]
    assert "Cough" in names
    assert "Dry cough" in names
    assert "Wet cough" in names
    assert "Phlegm" in names


def test_search_high_temperature():
    """Verify typing 'high temperature' returns 'Fever' via search_terms matching."""
    results = search_symptoms("high temperature")
    assert len(results) > 0
    names = [r['symptom_name'] for r in results]
    assert "Fever" in names
    fever_item = next(r for r in results if r['symptom_name'] == "Fever")
    assert "search_terms" in fever_item['matched_by']


def test_case_insensitive_matching():
    """Verify case-insensitivity across uppercase, lowercase, and mixed queries."""
    res_lower = search_symptoms("head")
    res_upper = search_symptoms("HEAD")
    res_mixed = search_symptoms("HeAd")

    assert [r['symptom_name'] for r in res_lower] == [r['symptom_name'] for r in res_upper]
    assert [r['symptom_name'] for r in res_lower] == [r['symptom_name'] for r in res_mixed]

    res_temp_upper = search_symptoms("HIGH TEMPERATURE")
    assert "Fever" in [r['symptom_name'] for r in res_temp_upper]


def test_results_not_unnecessarily_limited():
    """Verify that search displays all relevant matching symptoms rather than arbitrarily capping."""
    results = search_symptoms("pain")
    # There are multiple pain-related symptoms in the dataset
    assert len(results) > 5


def test_empty_and_whitespace_query():
    """Verify empty queries return an empty list gracefully."""
    assert search_symptoms("") == []
    assert search_symptoms("   ") == []
    assert search_symptoms(None) == []


def test_missing_file_error_handling():
    """Verify that a non-existent file path returns an empty DataFrame gracefully without crashing."""
    df = load_symptom_dataset(filepath="non_existent_path_xyz.csv", force_reload=True)
    assert isinstance(df, pd.DataFrame)
    assert df.empty
    # Reset back to valid dataset
    load_symptom_dataset(force_reload=True)


def test_missing_columns_error_handling():
    """Verify that a CSV missing 'symptom_name' is handled safely without unhandled exceptions."""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.csv') as f:
        f.write("wrong_col_1,wrong_col_2\nval1,val2\n")
        temp_path = f.name

    try:
        df = load_symptom_dataset(filepath=temp_path, force_reload=True)
        assert isinstance(df, pd.DataFrame)
        assert df.empty
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        # Reset back to valid dataset
        load_symptom_dataset(force_reload=True)


def test_api_symptom_search_endpoint():
    """Verify the Flask /api/symptoms/search endpoint returns valid JSON with status 200."""
    client = app.test_client()
    response = client.get('/api/symptoms/search?q=cough')
    assert response.status_code == 200
    data = response.get_json()
    assert data['query'] == 'cough'
    assert data['count'] >= 4
    names = [r['symptom_name'] for r in data['results']]
    assert "Cough" in names
