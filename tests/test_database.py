"""
tests/test_database.py
-----------------------
Unit tests for SQLite database operations, searching, and feedback storage.
"""

from src.database import get_dashboard_stats, search_medicines, insert_feedback


def test_dashboard_stats():
    stats = get_dashboard_stats()
    assert 'symptoms' in stats
    assert 'conditions' in stats
    assert 'medicines' in stats
    assert isinstance(stats['symptoms'], int)


def test_search_medicines():
    # Test query search
    results = search_medicines("paracetamol")
    assert isinstance(results, list)
    if len(results) > 0:
        assert "paracetamol" in results[0]['medicine_name'].lower()


def test_insert_feedback():
    initial_stats = get_dashboard_stats()
    insert_feedback("Test User", "test@example.com", 5, "Great educational project.")
    new_stats = get_dashboard_stats()
    assert new_stats['feedback'] == initial_stats['feedback'] + 1
