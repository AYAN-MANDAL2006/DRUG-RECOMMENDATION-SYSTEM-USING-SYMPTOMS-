"""
src/database.py
---------------
SQLite Database Access Object for the Drug Recommendation System.
Provides thread-safe parameterized database operations.
"""

import sqlite3
import os
from config import Config


def get_db_connection():
    """Establishes and returns a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db_schema():
    """Creates normalized SQLite database tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS symptoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom_name TEXT NOT NULL UNIQUE,
            normalized_name TEXT NOT NULL,
            synonyms TEXT
        );

        CREATE TABLE IF NOT EXISTS conditions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            condition_name TEXT NOT NULL UNIQUE,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS condition_symptoms (
            condition_id INTEGER NOT NULL,
            symptom_id INTEGER NOT NULL,
            PRIMARY KEY (condition_id, symptom_id),
            FOREIGN KEY (condition_id) REFERENCES conditions (id) ON DELETE CASCADE,
            FOREIGN KEY (symptom_id) REFERENCES symptoms (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT NOT NULL,
            generic_name TEXT,
            category TEXT,
            description TEXT,
            common_use TEXT,
            precautions TEXT,
            side_effects TEXT,
            contraindications TEXT,
            warning TEXT
        );

        CREATE TABLE IF NOT EXISTS condition_medicines (
            condition_id INTEGER NOT NULL,
            medicine_id INTEGER NOT NULL,
            PRIMARY KEY (condition_id, medicine_id),
            FOREIGN KEY (condition_id) REFERENCES conditions (id) ON DELETE CASCADE,
            FOREIGN KEY (medicine_id) REFERENCES medicines (id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()


def get_dashboard_stats():
    """Retrieves total count statistics from the database dynamically."""
    conn = get_db_connection()
    cursor = conn.cursor()

    symptoms_count = cursor.execute("SELECT COUNT(*) FROM symptoms").fetchone()[0]
    conditions_count = cursor.execute("SELECT COUNT(*) FROM conditions").fetchone()[0]
    medicines_count = cursor.execute("SELECT COUNT(*) FROM medicines").fetchone()[0]
    feedback_count = cursor.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]

    conn.close()
    return {
        'symptoms': symptoms_count,
        'conditions': conditions_count,
        'medicines': medicines_count,
        'feedback': feedback_count
    }


def search_medicines(query=None):
    """Searches medicines by medicine_name, generic_name, category, or common_use."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if not query:
        rows = cursor.execute("SELECT * FROM medicines ORDER BY medicine_name ASC").fetchall()
    else:
        pattern = f"%{query.strip()}%"
        rows = cursor.execute("""
            SELECT DISTINCT * FROM medicines 
            WHERE medicine_name LIKE ? 
               OR generic_name LIKE ? 
               OR category LIKE ? 
               OR common_use LIKE ?
            ORDER BY medicine_name ASC
        """, (pattern, pattern, pattern, pattern)).fetchall()

    conn.close()
    return [dict(row) for row in rows]


def get_medicine_by_id(medicine_id):
    """Retrieves a single medicine record by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM medicines WHERE id = ?", (medicine_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_medicines_for_condition(condition_name):
    """Retrieves all associated educational medicines for a specific condition."""
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("""
        SELECT m.* FROM medicines m
        JOIN condition_medicines cm ON m.id = cm.medicine_id
        JOIN conditions c ON c.id = cm.condition_id
        WHERE LOWER(c.condition_name) = LOWER(?)
    """, (condition_name,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_precautions_for_condition(condition_name):
    """Retrieves precautions listed for a condition from medicines/precautions data."""
    medicines = get_medicines_for_condition(condition_name)
    precautions_set = set()
    for med in medicines:
        if med.get('precautions'):
            precautions_set.add(med['precautions'])
    return list(precautions_set)


def insert_feedback(name, email, rating, message):
    """Stores user feedback securely into SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (name, email, rating, message)
        VALUES (?, ?, ?, ?)
    """, (name, email, rating, message))
    conn.commit()
    conn.close()
