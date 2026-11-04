"""
Lightweight local authentication for CropShield AI.

Uses a small SQLite database stored next to the application so the project
stays fully self-contained and works offline. Passwords are hashed with
Werkzeug's PBKDF2 implementation (never stored in plain text).
"""

import os
import re
import sqlite3
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "users.db")

DEMO_EMAIL = "demo@cropshield.ai"
DEMO_PHONE = "9999999999"
DEMO_PASSWORD = "demo1234"
DEMO_NAME = "Demo Farmer"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the users table and seed a demo farmer account if needed."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                preferred_language TEXT NOT NULL DEFAULT 'en',
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()

        existing = conn.execute(
            "SELECT id FROM users WHERE email = ? OR phone = ?",
            (DEMO_EMAIL, DEMO_PHONE),
        ).fetchone()

        if not existing:
            conn.execute(
                """
                INSERT INTO users (name, phone, email, password_hash,
                                   preferred_language, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    DEMO_NAME,
                    DEMO_PHONE,
                    DEMO_EMAIL,
                    generate_password_hash(DEMO_PASSWORD),
                    "en",
                    datetime.utcnow().isoformat(timespec="seconds"),
                ),
            )
            conn.commit()


def normalize_phone(phone: str) -> str:
    """Keep only digits, drop a +91 / 0 prefix, and return the last 10 digits."""
    digits = re.sub(r"\D", "", phone or "")
    if len(digits) > 10:
        digits = digits[-10:]
    return digits


def is_valid_phone(phone: str) -> bool:
    return len(normalize_phone(phone)) == 10


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or ""))


def create_user(name, phone, email, password, preferred_language="en"):
    """
    Create a new farmer account.

    Raises ValueError with a translation-friendly error code when the input is
    invalid or the account already exists.
    """
    name = (name or "").strip()
    phone = normalize_phone(phone)
    email = (email or "").strip().lower() or None
    preferred_language = preferred_language if preferred_language in ("en", "hi", "kn") else "en"

    if not name or not phone or not password:
        raise ValueError("fill_all")
    if not is_valid_phone(phone):
        raise ValueError("invalid_phone")
    if email and not is_valid_email(email):
        raise ValueError("invalid_email")
    if len(password) < 6:
        raise ValueError("password_short")

    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE phone = ? OR (email IS NOT NULL AND email = ?)",
            (phone, email),
        ).fetchone()
        if existing:
            raise ValueError("user_exists")

        conn.execute(
            """
            INSERT INTO users (name, phone, email, password_hash,
                               preferred_language, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                phone,
                email,
                generate_password_hash(password),
                preferred_language,
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()
        return conn.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()


def authenticate(identifier: str, password: str):
    """Return the matching user row for an email or mobile number, else None."""
    identifier = (identifier or "").strip()
    if not identifier or not password:
        return None

    lookup_email = identifier.lower() if "@" in identifier else None
    lookup_phone = None if lookup_email else normalize_phone(identifier)

    with get_connection() as conn:
        if lookup_email:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?", (lookup_email,)
            ).fetchone()
        else:
            user = conn.execute(
                "SELECT * FROM users WHERE phone = ?", (lookup_phone,)
            ).fetchone()

    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def get_user_by_id(user_id):
    if not user_id:
        return None
    with get_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def update_user_language(user_id, language):
    if language not in ("en", "hi", "kn"):
        return
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET preferred_language = ? WHERE id = ?",
            (language, user_id),
        )
        conn.commit()
