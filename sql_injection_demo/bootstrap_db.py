"""Initialize the demo database only when missing.

This avoids resetting data on every deployment restart while still ensuring
first-time deployments are usable.
"""

import sqlite3
from pathlib import Path

from .database import init_db

DB_PATH = Path(__file__).resolve().parent / "users.db"


def _has_users_table(db_path: Path) -> bool:
    if not db_path.exists():
        return False

    conn = sqlite3.connect(str(db_path))
    try:
        row = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def ensure_db() -> None:
    if _has_users_table(DB_PATH):
        print("[+] Existing database detected. Skipping initialization.")
        return

    print("[+] Database missing or incomplete. Initializing demo database.")
    init_db()


if __name__ == "__main__":
    ensure_db()
