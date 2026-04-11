"""Audit logging utility for authentication security events.

Writes to two destinations:
    1. auth.log     — human-readable flat file (easy to show during demo)
    2. audit_log    — structured SQLite table (queryable, part of DB schema)

Rule: NEVER log raw passwords. Only username, event type, timestamp, source IP.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB       = str(BASE_DIR / "users.db")
LOGFILE  = str(BASE_DIR / "auth.log")


def log_event(username: str, event: str, source: str = "unknown") -> None:
    """Record a security event to both flat log file and audit_log table.

    Args:
        username: The username involved in the event.
        event:    Short descriptive event label (e.g. LOGIN_SUCCESS).
        source:   Source IP address or identifier.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Flat file (primary record) ───────────────────────────────────────────
    line = (
        f"[{timestamp}] "
        f"user={username:<20} "
        f"event={event:<50} "
        f"source={source}\n"
    )
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(line)

    # ── Database table (structured record) ──────────────────────────────────
    try:
        conn = sqlite3.connect(DB)
        conn.execute(
            "INSERT INTO audit_log (timestamp, username, event, source) "
            "VALUES (?, ?, ?, ?)",
            (timestamp, username, event, source),
        )
        conn.commit()
        conn.close()
    except Exception as exc:
        # Auth flow must not fail if audit DB write fails.
        # Append a warning to flat log as fallback evidence.
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write(
                f"[{timestamp}] user={username:<20} "
                f"event=LOGGER_DB_WRITE_FAILED "
                f"source={source} error={exc}\n"
            )
