"""
src/symptom_search.py
---------------------
Module for loading, indexing, and searching symptom vocabulary from
data/symptom_search_dataset.csv using Pandas.
Supports case-insensitive partial matching on symptom_name and search_terms,
with robust error handling for missing files or missing columns.
"""

import os
import logging
import pandas as pd
from config import Config

logger = logging.getLogger(__name__)

# Cached DataFrame
_SYMPTOM_DF = None


def load_symptom_dataset(filepath=None, force_reload=False):
    """
    Loads symptom search dataset CSV using Pandas.
    Provides robust error handling for missing files or corrupt structure.
    
    Returns:
        pd.DataFrame: A valid DataFrame containing symptom records or an empty DataFrame.
    """
    global _SYMPTOM_DF

    if _SYMPTOM_DF is not None and not force_reload:
        return _SYMPTOM_DF

    path = filepath or Config.SYMPTOM_SEARCH_PATH

    if not os.path.exists(path):
        logger.warning(f"Symptom search dataset file not found at: {path}")
        _SYMPTOM_DF = pd.DataFrame(columns=[
            'symptom_id', 'symptom_name', 'category', 'synonyms', 'search_terms', 'data_note'
        ])
        return _SYMPTOM_DF

    try:
        df = pd.read_csv(path, dtype=str)
        # Normalize column names: strip spaces
        df.columns = [c.strip() for c in df.columns]

        # Check required columns
        if 'symptom_name' not in df.columns:
            logger.error("Required column 'symptom_name' missing in symptom search dataset.")
            _SYMPTOM_DF = pd.DataFrame(columns=[
                'symptom_id', 'symptom_name', 'category', 'synonyms', 'search_terms', 'data_note'
            ])
            return _SYMPTOM_DF

        # Ensure essential optional columns exist
        for col in ['symptom_id', 'category', 'synonyms', 'search_terms', 'data_note']:
            if col not in df.columns:
                df[col] = ''

        # Clean string columns: fill NaN with empty string and strip whitespace
        for col in df.columns:
            df[col] = df[col].fillna('').astype(str).str.strip()

        _SYMPTOM_DF = df
        return _SYMPTOM_DF

    except Exception as e:
        logger.error(f"Error loading symptom search dataset from {path}: {e}")
        _SYMPTOM_DF = pd.DataFrame(columns=[
            'symptom_id', 'symptom_name', 'category', 'synonyms', 'search_terms', 'data_note'
        ])
        return _SYMPTOM_DF


def search_symptoms(query, limit=None):
    """
    Performs case-insensitive partial matching across symptoms using Pandas.
    Matches against:
      - symptom_name (e.g. typing 'head' matches 'Headache')
      - search_terms (e.g. typing 'high temperature' matches 'Fever')
      - synonyms (e.g. alternative clinical terms)
    
    Args:
        query (str): The search query text.
        limit (int, optional): Optional maximum results. Defaults to None (returns all relevant matches).

    Returns:
        list of dict: List of matching symptom dictionaries.
    """
    if not query or not str(query).strip():
        return []

    df = load_symptom_dataset()
    if df.empty or 'symptom_name' not in df.columns:
        return []

    q = str(query).strip().lower()

    # Case-insensitive partial matching
    mask_name = df['symptom_name'].str.lower().str.contains(q, regex=False, na=False)
    mask_terms = df['search_terms'].str.lower().str.contains(q, regex=False, na=False) if 'search_terms' in df.columns else False
    mask_synonyms = df['synonyms'].str.lower().str.contains(q, regex=False, na=False) if 'synonyms' in df.columns else False

    matched_df = df[mask_name | mask_terms | mask_synonyms].copy()

    if matched_df.empty:
        return []

    # Score matches for intuitive ordering (most direct matches first)
    # 0 = exact name match
    # 1 = name starts with query
    # 2 = name contains query
    # 3 = search_terms match
    # 4 = synonyms match
    def compute_rank(row):
        name_lower = row['symptom_name'].lower()
        if name_lower == q:
            return (0, name_lower)
        if name_lower.startswith(q):
            return (1, name_lower)
        if q in name_lower:
            return (2, name_lower)
        terms_lower = row.get('search_terms', '').lower()
        if q in terms_lower:
            return (3, name_lower)
        return (4, name_lower)

    matched_df['rank'] = matched_df.apply(compute_rank, axis=1)
    matched_df = matched_df.sort_values(by='rank').drop(columns=['rank'])

    if limit is not None and limit > 0:
        matched_df = matched_df.head(limit)

    results = []
    for _, row in matched_df.iterrows():
        s_name = row['symptom_name']
        s_terms = row.get('search_terms', '')
        s_syn = row.get('synonyms', '')

        # Annotate how match was found for transparency
        matched_by = []
        if q in s_name.lower():
            matched_by.append('name')
        if s_terms and q in s_terms.lower():
            matched_by.append('search_terms')
        if s_syn and q in s_syn.lower():
            matched_by.append('synonyms')

        results.append({
            'symptom_id': row.get('symptom_id', ''),
            'symptom_name': s_name,
            'category': row.get('category', 'General'),
            'synonyms': s_syn,
            'search_terms': s_terms,
            'data_note': row.get('data_note', ''),
            'matched_by': matched_by
        })

    return results


def get_all_symptoms():
    """Returns all symptoms available in the search dataset as a list of dicts."""
    df = load_symptom_dataset()
    if df.empty:
        return []
    return df.to_dict(orient='records')


def get_categories():
    """Returns sorted unique category names from the search dataset."""
    df = load_symptom_dataset()
    if df.empty or 'category' not in df.columns:
        return []
    return sorted([c for c in df['category'].unique() if c])
