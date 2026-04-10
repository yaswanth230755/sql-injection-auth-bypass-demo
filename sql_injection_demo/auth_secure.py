"""Secure authentication module with parameterized queries and hardening.

CS4033E Computer Security | NIT Calicut

Primary mitigation : Parameterized SQL query (? placeholder).
Additional hardening: bcrypt password hashing, account lockout, audit logging.
"""

import sqlite3
import time
from pathlib import Path

import bcrypt

try:
    from .logger import log_event
except ImportError:
    from logger import log_event

DB           = str(Path(__file__).resolve().parent / "users.db")
MAX_ATTEMPTS = 5    # consecutive failures before lockout
LOCKOUT_SECS = 300  # lockout duration in seconds (5 minutes)


def secure_login(username: str, password: str, source_ip: str = "unknown"):
    """Authenticate securely using parameterized query binding and bcrypt.

    How parameterized query prevents SQL injection:
        Step 1: DB receives the query TEMPLATE:
                    SELECT * FROM users WHERE username = ?
        Step 2: DB compiles and locks the query structure. Parsing is complete.
        Step 3: The user-supplied value is bound as typed data — never as SQL text.
        Step 4: ' OR '1'='1' -- is treated as a literal string to search for.
        Step 5: No such username exists. Login fails correctly.

    Returns:
        tuple: (user_dict_or_none, message_or_none, success_bool)
    """

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # ── Step 1: Parameterized lookup ────────────────────────────────────────
    # The ? placeholder is compiled into the query structure BEFORE any value
    # is supplied. User input cannot alter SQL grammar.
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()

    # ── Step 2: Unknown username ─────────────────────────────────────────────
    # Return the same generic message as wrong password.
    # Prevents user enumeration — attacker cannot tell which field was wrong.
    if not user:
        conn.close()
        log_event(username, "LOGIN_FAIL_USER_NOT_FOUND", source_ip)
        return None, "Invalid credentials.", False

    user = dict(user)

    # ── Step 3: Lockout check ────────────────────────────────────────────────
    if user["lock_until"] and time.time() < user["lock_until"]:
        remaining = int(user["lock_until"] - time.time())
        conn.close()
        log_event(username, "LOGIN_BLOCKED_ACCOUNT_LOCKED", source_ip)
        return (
            None,
            f"Account temporarily locked. Try again in {remaining} seconds.",
            False,
        )

    # ── Step 4: bcrypt password verification ────────────────────────────────
    # checkpw hashes the input and compares against stored hash.
    # Plaintext passwords are never stored or compared directly.
    # bcrypt salt prevents rainbow-table attacks.
    password_correct = bcrypt.checkpw(
        password.encode(),
        user["password_hash"].encode(),
    )

    if not password_correct:
        new_attempts = user["failed_attempts"] + 1
        lock_until = None

        if new_attempts >= MAX_ATTEMPTS:
            lock_until = time.time() + LOCKOUT_SECS
            c.execute(
                "UPDATE users SET failed_attempts = ?, lock_until = ? WHERE username = ?",
                (new_attempts, lock_until, username),
            )
            log_event(username, f"ACCOUNT_LOCKED_AFTER_{new_attempts}_FAILURES", source_ip)
        else:
            c.execute(
                "UPDATE users SET failed_attempts = ? WHERE username = ?",
                (new_attempts, username),
            )
            log_event(
                username,
                f"LOGIN_FAIL_WRONG_PASSWORD_ATTEMPT_{new_attempts}",
                source_ip,
            )

        conn.commit()
        conn.close()
        return None, "Invalid credentials.", False

    # ── Step 5: Success — reset failure counters ─────────────────────────────
    c.execute(
        "UPDATE users SET failed_attempts = 0, lock_until = NULL WHERE username = ?",
        (username,),
    )
    conn.commit()
    conn.close()
    log_event(username, "LOGIN_SUCCESS", source_ip)
    return user, None, True
