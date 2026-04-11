"""Database initialization script for the SQL injection demo project.

Security training demonstration only — local test environment.

Run this once before starting the app.
Safe to re-run — drops and recreates all tables for a clean state.
"""

import sqlite3
from pathlib import Path

import bcrypt

DB = str(Path(__file__).resolve().parent / "users.db")


def init_db() -> None:
    """Create tables and seed test users."""

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Clean slate for every run — ensures repeatable demonstrations.
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS audit_log")

    # Schema design notes:
    #   password_plain  — used ONLY by vulnerable module (simulates naive dev mistake)
    #   password_hash   — used ONLY by secure module (bcrypt hash, correct practice)
    #   failed_attempts — hardening: tracks consecutive failures for lockout
    #   lock_until      — hardening: Unix timestamp when lockout expires (NULL = not locked)
    c.execute(
        """
        CREATE TABLE users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            username        TEXT    NOT NULL UNIQUE,
            password_plain  TEXT    NOT NULL,
            password_hash   TEXT    NOT NULL,
            role            TEXT    NOT NULL DEFAULT 'user',
            failed_attempts INTEGER NOT NULL DEFAULT 0,
            lock_until      REAL    DEFAULT NULL
        )
        """
    )

    c.execute(
        """
        CREATE TABLE audit_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            username  TEXT NOT NULL,
            event     TEXT NOT NULL,
            source    TEXT
        )
        """
    )

    # Seed: one admin + two regular users for clear demo outcomes.
    users = [
        ("admin", "adminpass123", "administrator"),
        ("alice", "alice2024",    "user"),
        ("bob",   "bobsecret",   "user"),
    ]

    for uname, pwd, role in users:
        hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
        c.execute(
            "INSERT INTO users (username, password_plain, password_hash, role) "
            "VALUES (?, ?, ?, ?)",
            (uname, pwd, hashed, role),
        )

    conn.commit()
    conn.close()

    print("[+] Database initialized successfully.")
    print("[+] Test users seeded:")
    print("      admin  /  adminpass123  (role: administrator)")
    print("      alice  /  alice2024     (role: user)")
    print("      bob    /  bobsecret     (role: user)")
    print(f"[+] Database path: {DB}")


if __name__ == "__main__":
    init_db()
