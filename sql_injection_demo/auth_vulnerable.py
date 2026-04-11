"""Intentionally vulnerable authentication module.

SECURITY TRAINING DEMONSTRATION ONLY — DO NOT USE IN ANY PRODUCTION SYSTEM.

This module is deliberately insecure to demonstrate SQL injection-based
authentication bypass in a controlled local test environment.
"""

import sqlite3
from pathlib import Path

DB = str(Path(__file__).resolve().parent / "users.db")


def vulnerable_login(username: str, password: str):
    """Authenticate via unsafe SQL string concatenation.

    The username and password strings are pasted directly into the SQL query.
    An attacker who supplies SQL syntax in either field can alter the WHERE
    clause logic and bypass authentication without valid credentials.

    Attack example:
        username = ' OR '1'='1' --
        password = anything

        Query becomes:
            SELECT * FROM users WHERE username = '' OR '1'='1' --'
            AND password_plain = 'anything'

        OR '1'='1' is always TRUE.
        The -- comments out the password check entirely.
        DB returns the first row. Login succeeds. No valid password needed.

    Returns:
        tuple: (user_dict_or_none, query_string, error_string_or_none)
    """

    # ══════════════════════════════════════════════════════════════════════
    # THE DANGEROUS LINE — user input becomes part of SQL code.
    # Never do this in any real application.
    # ══════════════════════════════════════════════════════════════════════
    query = (
        "SELECT * FROM users "
        "WHERE username = '" + username + "' "
        "AND password_plain = '" + password + "'"
    )

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(query)          # executes whatever string was constructed
        user = cursor.fetchone()
    except Exception as exc:
        conn.close()
        return None, query, str(exc)   # return error from malformed injection

    conn.close()

    if user:
        return dict(user), query, None
    return None, query, None
