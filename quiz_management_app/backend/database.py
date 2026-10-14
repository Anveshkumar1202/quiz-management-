"""SQLite database operations."""

import json
import os
import sqlite3
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
DATABASE_FILE = os.path.join(DATA_DIR, "quiz.db")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _connect():
    _ensure_data_dir()
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Initialize the database if it doesn't exist."""
    with _connect() as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY COLLATE NOCASE,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                text TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_index INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL COLLATE NOCASE,
                category TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                time_taken_seconds INTEGER NOT NULL DEFAULT 0
            );
        """)


# User management
def save_user(username, salt, password_hash, role="participant"):
    """Save a new user."""
    with _connect() as connection:
        connection.execute(
            "INSERT OR REPLACE INTO users (username, salt, password_hash, role) VALUES (?, ?, ?, ?)",
            (username, salt, password_hash, role)
        )
        connection.commit()


def get_user(username):
    """Get a user by username."""
    with _connect() as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE username = ? COLLATE NOCASE",
            (username,)
        ).fetchone()
        if row:
            return dict(row)
    return None


def load_users():
    """Load all users."""
    with _connect() as connection:
        rows = connection.execute("SELECT * FROM users").fetchall()
        return [dict(row) for row in rows]


# Question management
def add_question(category, difficulty, text, options, correct_index):
    """Add a new question."""
    with _connect() as connection:
        cursor = connection.execute(
            "INSERT INTO questions (category, difficulty, text, options, correct_index) VALUES (?, ?, ?, ?, ?)",
            (category, difficulty, text, json.dumps(options), correct_index)
        )
        connection.commit()
        return cursor.lastrowid


def delete_question(question_id):
    """Delete a question by ID."""
    with _connect() as connection:
        connection.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        connection.commit()


def load_questions(category=None):
    """Load questions, optionally filtered by category."""
    with _connect() as connection:
        if category:
            rows = connection.execute(
                "SELECT * FROM questions WHERE category = ? COLLATE NOCASE",
                (category,)
            ).fetchall()
        else:
            rows = connection.execute("SELECT * FROM questions").fetchall()
        
        questions = []
        for row in rows:
            q = dict(row)
            q["options"] = json.loads(q["options"])
            questions.append(q)
        return questions


def get_categories():
    """Get all question categories."""
    with _connect() as connection:
        rows = connection.execute("SELECT DISTINCT category FROM questions ORDER BY category").fetchall()
        return [row[0] for row in rows]


# Result management
def save_result(username, category, score, total, timestamp, time_taken):
    """Save a quiz result."""
    with _connect() as connection:
        connection.execute(
            "INSERT INTO results (username, category, score, total, timestamp, time_taken_seconds) VALUES (?, ?, ?, ?, ?, ?)",
            (username, category, score, total, timestamp, time_taken)
        )
        connection.commit()


def load_results(username=None):
    """Load quiz results, optionally filtered by username."""
    with _connect() as connection:
        if username:
            rows = connection.execute(
                "SELECT * FROM results WHERE username = ? COLLATE NOCASE ORDER BY timestamp DESC",
                (username,)
            ).fetchall()
        else:
            rows = connection.execute("SELECT * FROM results ORDER BY timestamp DESC").fetchall()
        
        return [dict(row) for row in rows]


# Admin initialization
def ensure_admin():
    """Create default admin user if none exists."""
    existing_admin = get_user("admin")
    if not existing_admin:
        import hashlib
        import os
        import binascii
        
        salt = os.urandom(16)
        salt_hex = binascii.hexlify(salt).decode()
        digest = hashlib.pbkdf2_hmac("sha256", b"admin123", salt, 100_000)
        hash_hex = binascii.hexlify(digest).decode()
        
        save_user("admin", salt_hex, hash_hex, "admin")
