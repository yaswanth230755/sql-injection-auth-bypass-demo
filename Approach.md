Looking at everything in this conversation — the course plan, all previous outputs, and all AI suggestions — here is the single, definitive, nothing-missing master guide:

---

# COMPLETE MASTER GUIDE
## CS4033E Computer Security | NIT Calicut
### SQL Injection Authentication Bypass Assignment (20 Marks)

---

## UNDERSTANDING THE MARKING SCHEME FIRST

From the course plan PDF:

| Evaluation | Marks | What is checked |
|---|---|---|
| Eval 1 | 10 | Literature Survey + Revised Specification + Input/Output Clarity + Implementation Progress |
| Eval 2 | 10 | Technical Explanation + Implementation + Demonstration + Report |

**Every single thing you build must map directly to one of these items. Nothing extra, nothing missing.**

---

## STEP 1: FREEZE YOUR SCOPE (Do This Before Opening Any Editor)

**Your exact topic:** SQL Injection-Based Authentication Bypass in a Self-Built Login Module with Parameterized Query Mitigation

**One-sentence objective** (say this to sir if asked):
> "I am building a login system from scratch with two flows — an intentionally vulnerable module using string-concatenated SQL to demonstrate authentication bypass in a controlled lab, and a secure module using parameterized queries as the primary mitigation — supplemented by bcrypt password hashing, account lockout, and audit logging, with a comparative test matrix as evidence."

**Four modules — lock these, never change:**

| Module | Name | What it proves |
|---|---|---|
| A | Vulnerable Login | Unsafe SQL construction allows bypass |
| B | Secure Login | Parameterized query blocks same bypass |
| C | Hardening | bcrypt + lockout + logging = defense depth |
| D | Evaluation | Test matrix + screenshots = reproducible evidence |

**Constraints — write this verbatim in your report:**
- Local machine only
- Test database with test users only
- No testing on any public, live, or third-party system
- Vulnerable module exists solely for controlled academic demonstration

**Success criteria — your assignment is complete only when all four are true:**
1. Vulnerable path shows bypass under crafted SQL payload
2. Secure path blocks the exact same payload
3. Normal valid login still works correctly on secure path
4. All results are documented with test matrix and screenshot evidence

---

## STEP 2: INSTALL DEPENDENCIES

```bash
pip install flask bcrypt
```

That is all you need. SQLite is built into Python. No other tools required.

---

## STEP 3: CREATE PROJECT STRUCTURE

Create this exact folder layout:

```
sql_injection_demo/
│
├── app.py                  ← All Flask routes
├── database.py             ← DB creation and test user seeding
├── auth_vulnerable.py      ← Module A: unsafe login logic only
├── auth_secure.py          ← Module B+C: safe login + hardening
├── logger.py               ← Audit logging utility
│
├── users.db                ← Auto-created when you run database.py
├── auth.log                ← Auto-created when first login event fires
│
└── templates/
    ├── index.html          ← Home page with module selector
    ├── login_vuln.html     ← Module A login form
    ├── login_safe.html     ← Module B+C login form
    ├── success.html        ← Result page for successful login
    └── fail.html           ← Result page for failed login
```

---

## STEP 4: BUILD THE DATABASE

**`database.py`** — run this once before starting the app

```python
import sqlite3
import bcrypt

DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Clean slate every run
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS audit_log")

    # Users table
    # password_plain  → used ONLY by vulnerable module (simulates naive dev mistake)
    # password_hash   → used ONLY by secure module (correct practice)
    # failed_attempts → hardening: track consecutive failures
    # lock_until      → hardening: Unix timestamp when lockout expires
    c.execute("""
        CREATE TABLE users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            username        TEXT    NOT NULL UNIQUE,
            password_plain  TEXT    NOT NULL,
            password_hash   TEXT    NOT NULL,
            role            TEXT    NOT NULL DEFAULT 'user',
            failed_attempts INTEGER NOT NULL DEFAULT 0,
            lock_until      REAL    DEFAULT NULL
        )
    """)

    # Audit log table — structured event records
    c.execute("""
        CREATE TABLE audit_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            username  TEXT NOT NULL,
            event     TEXT NOT NULL,
            source    TEXT
        )
    """)

    # Seed three test users — one admin, two normal users
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
            (uname, pwd, hashed, role)
        )

    conn.commit()
    conn.close()

    print("[+] Database initialized successfully.")
    print("[+] Test users seeded:")
    print("      admin  /  adminpass123  (role: administrator)")
    print("      alice  /  alice2024     (role: user)")
    print("      bob    /  bobsecret     (role: user)")

if __name__ == "__main__":
    init_db()
```

**Why two password columns:** This is an intentional design decision — document it in your report. The same careless developer who writes concatenated SQL also stores plaintext passwords. The secure module never touches `password_plain`. This contrast is visible in the schema itself and is a strong talking point in your viva.

---

## STEP 5: MODULE A — VULNERABLE LOGIN

**`auth_vulnerable.py`**

```python
import sqlite3

DB = "users.db"

# ╔══════════════════════════════════════════════════════════╗
# ║  INTENTIONALLY VULNERABLE — ACADEMIC DEMONSTRATION ONLY  ║
# ║  DO NOT USE IN ANY PRODUCTION OR PUBLIC-FACING SYSTEM    ║
# ║  CS4033E Computer Security | NIT Calicut                 ║
# ╚══════════════════════════════════════════════════════════╝

def vulnerable_login(username, password):
    """
    Builds SQL by direct string concatenation of user input.

    Attack example:
      username = ' OR '1'='1' --
      password = anything

      Query becomes:
        SELECT * FROM users
        WHERE username = '' OR '1'='1' --' AND password_plain = 'anything'

      OR '1'='1' is always TRUE.
      The -- comments out the rest of the query including password check.
      DB returns the first user row. Login succeeds with no valid credentials.
    """

    # ── THE DANGEROUS LINE ─────────────────────────────────────────────────
    # User input is pasted directly into SQL string. Never do this.
    query = (
        "SELECT * FROM users "
        "WHERE username = '" + username + "' "
        "AND password_plain = '" + password + "'"
    )
    # ──────────────────────────────────────────────────────────────────────

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(query)       # executes whatever malformed string was built
        user = cursor.fetchone()
    except Exception as e:
        conn.close()
        return None, query, str(e) # return the error and the query for display

    conn.close()

    if user:
        return dict(user), query, None
    return None, query, None
```

---

## STEP 6: MODULE B+C — SECURE LOGIN WITH HARDENING

**`auth_secure.py`**

```python
import sqlite3
import bcrypt
import time
from logger import log_event

DB           = "users.db"
MAX_ATTEMPTS = 5     # lock after this many consecutive failures
LOCKOUT_SECS = 300   # 5 minutes

def secure_login(username, password, source_ip="unknown"):
    """
    PRIMARY MITIGATION: Parameterized query.
      DB receives query template first. Structure is compiled and locked.
      User input is then bound as pure data — it cannot alter SQL structure.
      ' OR '1'='1' -- becomes a literal 20-character search string, not SQL.

    ADDITIONAL HARDENING:
      bcrypt hash verification — no plaintext password comparison.
      Account lockout — brute force throttled after MAX_ATTEMPTS failures.
      Audit logging — every event recorded with timestamp.
      Generic error messages — no user enumeration clues.
    """

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # ── Step 1: Parameterized fetch by username ──────────────────────────
    # The ? placeholder is bound AFTER query structure is compiled.
    # Injection payload in username cannot alter WHERE clause logic.
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()

    # ── Step 2: User not found ────────────────────────────────────────────
    # Generic message only — never reveal whether username exists or not.
    # Revealing this is called user enumeration, a separate vulnerability.
    if not user:
        conn.close()
        log_event(username, "LOGIN_FAIL_USER_NOT_FOUND", source_ip)
        return None, "Invalid credentials.", False

    user = dict(user)

    # ── Step 3: Check account lockout ────────────────────────────────────
    if user["lock_until"] and time.time() < user["lock_until"]:
        remaining = int(user["lock_until"] - time.time())
        conn.close()
        log_event(username, "LOGIN_BLOCKED_ACCOUNT_LOCKED", source_ip)
        return None, f"Account temporarily locked. Try again in {remaining} seconds.", False

    # ── Step 4: bcrypt password verification ─────────────────────────────
    # checkpw hashes the input and compares — never compares plaintext.
    # bcrypt includes a random salt, so rainbow table attacks fail.
    password_correct = bcrypt.checkpw(
        password.encode(),
        user["password_hash"].encode()
    )

    if not password_correct:
        new_attempts = user["failed_attempts"] + 1
        lock_until   = None

        if new_attempts >= MAX_ATTEMPTS:
            lock_until = time.time() + LOCKOUT_SECS
            c.execute(
                "UPDATE users SET failed_attempts = ?, lock_until = ? WHERE username = ?",
                (new_attempts, lock_until, username)
            )
            log_event(username, f"ACCOUNT_LOCKED_AFTER_{new_attempts}_FAILURES", source_ip)
        else:
            c.execute(
                "UPDATE users SET failed_attempts = ? WHERE username = ?",
                (new_attempts, username)
            )
            log_event(username, f"LOGIN_FAIL_WRONG_PASSWORD_ATTEMPT_{new_attempts}", source_ip)

        conn.commit()
        conn.close()
        return None, "Invalid credentials.", False

    # ── Step 5: Successful login — reset counters ─────────────────────────
    c.execute(
        "UPDATE users SET failed_attempts = 0, lock_until = NULL WHERE username = ?",
        (username,)
    )
    conn.commit()
    conn.close()
    log_event(username, "LOGIN_SUCCESS", source_ip)
    return user, None, True
```

---

## STEP 7: LOGGING MODULE

**`logger.py`**

```python
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB = str(BASE_DIR / "users.db")
LOGFILE = str(BASE_DIR / "auth.log")

def log_event(username, event, source="unknown"):
    """
    Records security events to both flat file and DB table.
    Rule: NEVER log raw passwords — only usernames, events, timestamps.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Flat file — easiest to show during demo
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(
            f"[{timestamp}] "
            f"user={username:<20} "
            f"event={event:<50} "
            f"source={source}\n"
        )

    # DB table — structured, can be queried
    try:
        conn = sqlite3.connect(DB)
        conn.execute(
            "INSERT INTO audit_log (timestamp, username, event, source) "
            "VALUES (?, ?, ?, ?)",
            (timestamp, username, event, source)
        )
        conn.commit()
        conn.close()
    except Exception as exc:
      # Keep auth flow resilient if DB write fails, but keep observability.
      with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(
          f"[{timestamp}] user={username:<20} event=LOGGER_DB_WRITE_FAILED source={source} error={exc}\n"
        )
```

---

## STEP 8: FLASK ROUTES

**`app.py`**

```python
import os

from flask import Flask, request, render_template

try:
  # Package-style imports (works when run from workspace root).
  from .auth_vulnerable import vulnerable_login
  from .auth_secure import secure_login
except ImportError:
  # Script-style imports (works when run from project directory).
  from auth_vulnerable import vulnerable_login
  from auth_secure import secure_login

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "cs4033e_nitc_demo_only")


# ── Home page ──────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── Module A: Vulnerable login ─────────────────────────────────
@app.route("/login_vuln", methods=["GET", "POST"])
def login_vuln():
    if request.method == "GET":
        return render_template("login_vuln.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    user, query, error = vulnerable_login(username, password)

    # Detect if the successful login used an injection-style payload
    injection_indicators = ["'", "--", " OR ", " or ", "="]
    is_attack = (user is not None) and any(ind in username for ind in injection_indicators)

    if user:
        return render_template("success.html",
            username  = user["username"],
            role      = user["role"],
            query     = query,
            mode      = "VULNERABLE",
            is_attack = is_attack
        )
    return render_template("fail.html",
        query = query,
        error = error,
        mode  = "VULNERABLE"
    )


# ── Module B+C: Secure login ───────────────────────────────────
@app.route("/login_safe", methods=["GET", "POST"])
def login_safe():
    if request.method == "GET":
        return render_template("login_safe.html")

    username  = request.form.get("username", "")
    password  = request.form.get("password", "")
    source_ip = request.remote_addr

    # Show the parameterized template — the ? never gets user input substituted as SQL
    display_query = (
        f"SELECT * FROM users WHERE username = ?  "
        f"→  value bound as literal data: ('{username}')"
    )

    user, message, success = secure_login(username, password, source_ip)

    if success:
        return render_template("success.html",
            username  = user["username"],
            role      = user["role"],
            query     = display_query,
            mode      = "SECURE",
            is_attack = False
        )
    return render_template("fail.html",
        query = display_query,
        error = message,
        mode  = "SECURE"
    )


if __name__ == "__main__":
  debug_enabled = os.getenv("FLASK_DEBUG", "0") in {"1", "true", "True"}
  port = int(os.getenv("PORT", "5000"))
  app.run(debug=debug_enabled, port=port)
```

---

## STEP 9: ALL HTML TEMPLATES

**`templates/index.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>SQL Injection Demo | CS4033E NIT Calicut</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Courier New', monospace;
      background: #0d0d1a; color: #cdd6f4;
      min-height: 100vh;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      padding: 40px 20px;
    }
    h1 { color: #cba6f7; font-size: 1.6em; margin-bottom: 6px; text-align: center; }
    .sub { color: #6c7086; font-size: 0.82em; margin-bottom: 36px; text-align: center; }
    .cards { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; margin-bottom: 32px; }
    .card {
      background: #1e1e2e; border-radius: 12px; padding: 26px 22px;
      width: 220px; text-align: center; border: 1px solid #313244;
    }
    .card h3 { margin-bottom: 8px; font-size: 0.95em; }
    .card p { font-size: 0.76em; color: #6c7086; margin-bottom: 16px; line-height: 1.6; }
    .btn { display: block; padding: 11px; border-radius: 7px; text-decoration: none; font-weight: bold; font-size: 0.88em; }
    .btn-red   { background: #f38ba8; color: #1e1e2e; }
    .btn-green { background: #a6e3a1; color: #1e1e2e; }
    .info-box {
      background: #1e1e2e; border: 1px solid #45475a;
      border-radius: 10px; padding: 22px; max-width: 560px; width: 100%;
    }
    .info-box h3 { color: #f9e2af; margin-bottom: 12px; font-size: 0.9em; }
    .row { font-size: 0.82em; margin: 7px 0; }
    code { background: #313244; color: #f38ba8; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
    .note { margin-top: 14px; font-size: 0.76em; color: #6c7086; line-height: 1.7; }
    .green { color: #a6e3a1; }
  </style>
</head>
<body>
  <h1>SQL Injection: Authentication Bypass Demo</h1>
  <p class="sub">CS4033E Computer Security &middot; NIT Calicut &middot; Security Attack Assignment</p>

  <div class="cards">
    <div class="card">
      <h3 style="color:#f38ba8">&#9888; Module A</h3>
      <p>Vulnerable login — SQL built by string concatenation. Controlled academic demo only.</p>
      <a href="/login_vuln" class="btn btn-red">Vulnerable Login</a>
    </div>
    <div class="card">
      <h3 style="color:#a6e3a1">&#10004; Module B+C</h3>
      <p>Secure login — parameterized query + bcrypt + lockout + logging.</p>
      <a href="/login_safe" class="btn btn-green">Secure Login</a>
    </div>
  </div>

  <div class="info-box">
    <h3>&#128270; Attack Payloads to Try on Vulnerable Login</h3>
    <div class="row">Username: <code>' OR '1'='1' --</code> &nbsp; Password: <code>anything</code></div>
    <div class="row">Username: <code>admin'--</code> &nbsp; Password: <code>anything</code></div>
    <div class="row">Username: <code>' OR 1=1--</code> &nbsp; Password: <code>anything</code></div>
    <div class="note">
      &#8594; Vulnerable Login: authentication bypassed, no valid credentials needed.<br>
      &#8594; Secure Login: same payloads treated as literal strings, access denied.<br><br>
      <span class="green">&#10003; Valid test credentials:</span>
      &nbsp;<code>admin / adminpass123</code>
      &nbsp;<code>alice / alice2024</code>
      &nbsp;<code>bob / bobsecret</code>
    </div>
  </div>
</body>
</html>
```

**`templates/login_vuln.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><title>Vulnerable Login | Module A</title>
  <style>
    body { font-family:'Courier New',monospace; background:#0d0d1a; color:#cdd6f4;
           display:flex; align-items:center; justify-content:center; min-height:100vh; padding:20px; }
    .box { background:#1e1e2e; border:2px solid #f38ba8; border-radius:12px; padding:38px; width:360px; }
    h2 { color:#f38ba8; margin-bottom:8px; font-size:1.1em; }
    .warn { background:#3d0014; border:1px solid #f38ba8; color:#f38ba8; padding:10px;
            border-radius:6px; font-size:0.76em; margin-bottom:20px; line-height:1.6; }
    label { font-size:0.8em; color:#6c7086; display:block; margin-bottom:4px; }
    input { display:block; width:100%; padding:10px; margin-bottom:14px; background:#313244;
            border:1px solid #45475a; color:#cdd6f4; border-radius:6px; font-family:inherit; font-size:0.92em; }
    button { width:100%; padding:12px; background:#f38ba8; color:#1e1e2e; border:none;
             border-radius:6px; font-weight:bold; cursor:pointer; font-size:0.95em; }
    a { display:block; text-align:center; margin-top:16px; color:#89b4fa; font-size:0.8em; }
  </style>
</head>
<body>
  <div class="box">
    <h2>&#9888; Module A — Vulnerable Login</h2>
    <div class="warn">
      ACADEMIC DEMONSTRATION ONLY.<br>
      This module intentionally uses unsafe SQL string<br>
      concatenation. Do not use in any real system.
    </div>
    <form method="POST" action="/login_vuln">
      <label>Username</label>
      <input type="text" name="username" placeholder="Try: ' OR '1'='1' --" autocomplete="off">
      <label>Password</label>
      <input type="password" name="password" placeholder="Any value works in attack">
      <button type="submit">Login (Vulnerable)</button>
    </form>
    <a href="/">&#8592; Back to Home</a>
  </div>
</body>
</html>
```

**`templates/login_safe.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><title>Secure Login | Module B+C</title>
  <style>
    body { font-family:'Courier New',monospace; background:#0d0d1a; color:#cdd6f4;
           display:flex; align-items:center; justify-content:center; min-height:100vh; padding:20px; }
    .box { background:#1e1e2e; border:2px solid #a6e3a1; border-radius:12px; padding:38px; width:360px; }
    h2 { color:#a6e3a1; margin-bottom:8px; font-size:1.1em; }
    .info { background:#0d2b12; border:1px solid #a6e3a1; color:#a6e3a1; padding:10px;
            border-radius:6px; font-size:0.76em; margin-bottom:20px; line-height:1.6; }
    label { font-size:0.8em; color:#6c7086; display:block; margin-bottom:4px; }
    input { display:block; width:100%; padding:10px; margin-bottom:14px; background:#313244;
            border:1px solid #45475a; color:#cdd6f4; border-radius:6px; font-family:inherit; font-size:0.92em; }
    button { width:100%; padding:12px; background:#a6e3a1; color:#1e1e2e; border:none;
             border-radius:6px; font-weight:bold; cursor:pointer; font-size:0.95em; }
    a { display:block; text-align:center; margin-top:16px; color:#89b4fa; font-size:0.8em; }
  </style>
</head>
<body>
  <div class="box">
    <h2>&#10004; Module B+C — Secure Login</h2>
    <div class="info">
      Parameterized query + bcrypt hash verification<br>
      + account lockout + audit logging.<br>
      Try the same attack payloads — they will fail.
    </div>
    <form method="POST" action="/login_safe">
      <label>Username</label>
      <input type="text" name="username" placeholder="Enter username" autocomplete="off">
      <label>Password</label>
      <input type="password" name="password" placeholder="Enter password">
      <button type="submit">Login (Secure)</button>
    </form>
    <a href="/">&#8592; Back to Home</a>
  </div>
</body>
</html>
```

**`templates/success.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><title>Login Result</title>
  <style>
    body { font-family:'Courier New',monospace; background:#0d0d1a; color:#cdd6f4;
           display:flex; align-items:center; justify-content:center; min-height:100vh; padding:20px; }
    .card { background:#1e1e2e; border-radius:12px; padding:34px; max-width:640px; width:100%; }
    .attack { background:#3d0014; border:2px solid #f38ba8; color:#f38ba8; padding:16px;
              border-radius:8px; margin-bottom:16px; line-height:1.7; font-size:1em; }
    .ok     { background:#0d2b12; border:2px solid #a6e3a1; color:#a6e3a1; padding:14px;
              border-radius:8px; margin-bottom:16px; }
    .info-row { margin:7px 0; font-size:0.88em; }
    .query-box { background:#11111b; border:1px solid #313244; border-radius:8px;
                 padding:16px; margin-top:18px; word-break:break-all; }
    .query-box strong { color:#cba6f7; display:block; margin-bottom:8px; font-size:0.82em; }
    code { color:#f9e2af; font-size:0.85em; line-height:1.7; }
    .meta { color:#6c7086; font-size:0.76em; margin-top:12px; }
    a { display:block; text-align:center; margin-top:18px; color:#89b4fa; font-size:0.82em; }
  </style>
</head>
<body>
  <div class="card">
    {% if is_attack %}
      <div class="attack">
        &#128680; ATTACK SUCCESSFUL — AUTHENTICATION BYPASSED<br>
        No valid password was provided. Injected SQL logic altered<br>
        the WHERE clause and granted unauthorized access.
      </div>
    {% else %}
      <div class="ok">&#10004; Login Successful — Credentials validated correctly.</div>
    {% endif %}

    <div class="info-row">Logged in as: <strong>{{ username }}</strong></div>
    <div class="info-row">Role: <strong>{{ role }}</strong></div>

    <div class="query-box">
      <strong>SQL QUERY EXECUTED BY DATABASE:</strong>
      <code>{{ query }}</code>
    </div>

    <p class="meta">Module mode: {{ mode }}</p>
    <a href="/">&#8592; Back to Home</a>
  </div>
</body>
</html>
```

**`templates/fail.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><title>Login Failed</title>
  <style>
    body { font-family:'Courier New',monospace; background:#0d0d1a; color:#cdd6f4;
           display:flex; align-items:center; justify-content:center; min-height:100vh; padding:20px; }
    .card { background:#1e1e2e; border-radius:12px; padding:34px; max-width:640px; width:100%; }
    .fail { background:#1a1a2e; border:1px solid #45475a; padding:14px; border-radius:8px; margin-bottom:12px; }
    .reason { color:#f38ba8; font-size:0.84em; margin:10px 0; }
    .mitigated { background:#0d2b12; border:1px solid #a6e3a1; color:#a6e3a1;
                 padding:12px; border-radius:6px; margin-top:10px; font-size:0.82em; line-height:1.7; }
    .query-box { background:#11111b; border:1px solid #313244; border-radius:8px;
                 padding:16px; margin-top:18px; word-break:break-all; }
    .query-box strong { color:#cba6f7; display:block; margin-bottom:8px; font-size:0.82em; }
    code { color:#f9e2af; font-size:0.85em; line-height:1.7; }
    .meta { color:#6c7086; font-size:0.76em; margin-top:12px; }
    a { display:block; text-align:center; margin-top:18px; color:#89b4fa; font-size:0.82em; }
  </style>
</head>
<body>
  <div class="card">
    <div class="fail">&#10006; Login Failed</div>

    {% if error %}
      <p class="reason">Reason: {{ error }}</p>
    {% endif %}

    {% if mode == "SECURE" %}
      <div class="mitigated">
        &#10004; MITIGATION ACTIVE: Parameterized query compiled SQL structure<br>
        before any user input was processed. The injection payload was<br>
        bound as a literal data value — it cannot alter query logic.<br>
        No user with that literal username exists &#8594; access correctly denied.
      </div>
    {% endif %}

    <div class="query-box">
      <strong>SQL QUERY USED:</strong>
      <code>{{ query }}</code>
    </div>

    <p class="meta">Module mode: {{ mode }}</p>
    <a href="/">&#8592; Back to Home</a>
  </div>
</body>
</html>
```

---

## STEP 10: HOW TO RUN

```bash
# 1. Create/activate virtual environment (example)
python -m venv .venv

# 2. Install pinned dependencies
.venv/bin/pip install -r sql_injection_demo/requirements.txt

# 3. Initialize the database — run once
cd sql_injection_demo
../.venv/bin/python database.py

# 4. Start the application
../.venv/bin/python app.py

# (Alternative package-style run from workspace root)
# .venv/bin/python -c "from sql_injection_demo.app import app; app.run(debug=False, port=5000)"

# 5. Open in your browser
http://localhost:5000
```

---

## STEP 11: COMPLETE TEST MATRIX

Run every single row. Screenshot every result. These are your Eval 2 evidence.

| ID | Username input | Password | Module | Expected | Key point proven |
|---|---|---|---|---|---|
| T01 | admin | adminpass123 | Vulnerable | Success | Normal flow works |
| T02 | admin | adminpass123 | Secure | Success | Normal flow works |
| T03 | alice | wrongpass | Vulnerable | Fail | Wrong password rejected |
| T04 | alice | wrongpass | Secure | Fail | Wrong password rejected |
| T05 | nobody | anything | Vulnerable | Fail | Unknown user rejected |
| T06 | nobody | anything | Secure | Fail | Unknown user rejected |
| T07 | `' OR '1'='1' --` | anything | **Vulnerable** | **BYPASS SUCCEEDS** | Core attack visible |
| T08 | `' OR '1'='1' --` | anything | **Secure** | **BLOCKED** | Core mitigation visible |
| T09 | `admin'--` | anything | **Vulnerable** | **BYPASS SUCCEEDS** | Comment truncation attack |
| T10 | `admin'--` | anything | **Secure** | **BLOCKED** | Comment truncation blocked |
| T11 | `' OR 1=1--` | anything | **Vulnerable** | **BYPASS SUCCEEDS** | Tautology attack |
| T12 | `' OR 1=1--` | anything | **Secure** | **BLOCKED** | Tautology blocked |
| T13 | alice | wrongpass ×5 | Secure | Locked after 5th | Lockout triggers |
| T14 | alice | alice2024 | Secure (after T13) | Still locked | Lockout holds |
| T15 | (empty) | (empty) | Both | Fail gracefully | Empty input handled |
| T16 | 500-char string | anything | Both | Fail, no crash | Long input robust |
| T17 | ünïcödé | anything | Both | Fail gracefully | Unicode handled |

For each row record: Test ID · Input used · Expected result · Vulnerable result · Secure result · Pass/Fail · Screenshot filename

---

## STEP 12: EVIDENCE SCREENSHOTS TO COLLECT

Take these during testing, name them consistently:

| Screenshot | Filename |
|---|---|
| Normal login success — vulnerable side | ev01_normal_vuln.png |
| Normal login success — secure side | ev02_normal_secure.png |
| T07 bypass success + query shown | ev03_attack_bypass.png |
| T08 same payload blocked on secure | ev04_attack_blocked.png |
| T09 admin'-- bypass | ev05_comment_attack.png |
| T10 admin'-- blocked | ev06_comment_blocked.png |
| Lockout triggering after 5 failures | ev07_lockout.png |
| auth.log file contents | ev08_audit_log.png |
| Code: the dangerous concatenation line | ev09_code_vuln.png |
| Code: the parameterized ? line | ev10_code_secure.png |
| DB showing bcrypt hash column | ev11_bcrypt_hash.png |

---

## STEP 13: THE TECHNICAL EXPLANATION YOU MUST MASTER

**Why string concatenation is dangerous — with exact example:**

```
Developer writes:
  query = "SELECT * FROM users WHERE username = '" + username + "'"

Attacker inputs username:   ' OR '1'='1' --

Query string becomes:
  SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password_plain = '...'
                                           ↑              ↑
                                    always true     password check
                                                    commented out

Result: DB evaluates OR '1'='1' as TRUE.
        Returns first user row in the table.
        Attacker is logged in. Zero valid credentials used.
```

**Why parameterized queries fix this — at the engine level:**

```
Developer writes:
  cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

What the DB engine does, step by step:
  Step 1: Receives template   →  SELECT * FROM users WHERE username = ?
  Step 2: Compiles and locks query structure. Parsing is complete.
  Step 3: Binds value  ' OR '1'='1' --  into the ? slot as DATA, not SQL.
  Step 4: Searches for user whose username literally equals  ' OR '1'='1' --
  Step 5: No such user. Returns nothing. Login fails correctly.

The fundamental guarantee:
  Code (SQL structure) and Data (user input) are processed separately.
  Input can never alter structure because structure is already compiled.
  This is enforced at the DB driver level, not at the application level.
```

**Why input validation alone is not sufficient (important for viva):**
Input validation filters characters like `'` and `--` but can be bypassed with encoding tricks, Unicode normalization, or second-order injection. Parameterization works at the query compilation level and cannot be bypassed this way. This is why parameterization is the primary mitigation and validation is only secondary.

**Why bcrypt is the right choice for passwords:**
bcrypt is intentionally slow (tunable cost factor). Each hash includes a random salt. Rainbow table attacks fail because the same password produces a different hash every time. Even if the DB is stolen, cracking bcrypt hashes is computationally expensive.

---

## STEP 14: EVAL 1 — WHAT TO PREPARE

**Literature Survey (1–2 pages covering all of these):**

- SQL injection was first publicly documented in 1998 by Jeff Forristal
- It has appeared in OWASP Top 10 every year since the list began
- Current ranking: OWASP A03:2021 (Injection category)
- Types of SQL injection: Classic/In-band, Blind, Time-based Blind, Error-based, Union-based
- Authentication bypass is the most immediately impactful form — grants access with zero credentials
- Real-world breaches: Heartland Payment Systems 2008 (130 million cards), RockYou 2009 (32 million plaintext passwords), TalkTalk 2015 (£400k fine), BSNL India (customer data exposed)
- Stallings textbook Chapter on Software Security covers injection vulnerabilities
- OWASP SQL Injection Prevention Cheat Sheet is your primary reference

**Revised Specification (one page):**
- Objective statement
- Four modules listed with one-line description each
- Scope constraints
- Input/Output clearly defined (username + password fields → success/fail result page showing SQL query used)

**Architecture diagram to draw:**
```
Browser
  │
  ├─ GET/POST /login_vuln ──► auth_vulnerable.py ──► users.db (password_plain col)
  │                                │
  │                          String concat SQL
  │
  └─ GET/POST /login_safe ──► auth_secure.py ──────► users.db (password_hash col)
                                   │
                             Parameterized SQL
                             + bcrypt verify
                             + lockout check
                             + logger.py ──────────► auth.log + audit_log table
```

**Implementation progress for Eval 1:**
- Show `python database.py` running and confirming users seeded
- Show the Flask app starting on port 5000
- Show the home page loading in browser
- Show at least the vulnerable login working for normal credentials

---

## STEP 15: EVAL 2 — DEMO FLOW (Rehearse This Twice)

**Minute 1 — Problem statement:**
"SQL injection is OWASP Top 10 A03:2021. Authentication bypass is the most dangerous form — an attacker gains system access without any valid credentials by injecting SQL logic through a normal input field. I built this system from scratch to demonstrate the attack and its mitigation."

**Minutes 2–3 — Module A demonstration:**
- Open home page in browser
- Click Vulnerable Login
- Enter `' OR '1'='1' --` in username, type `hello` in password, click submit
- Point to the red attack banner: "Authentication bypassed. No valid password was provided."
- Point to the query displayed: "Here is exactly what the database executed. The OR '1'='1' is always true. The double dash comments out the password check. The database returned the first user row."

**Minutes 4–5 — Module B+C demonstration:**
- Click Back to Home
- Click Secure Login
- Enter the exact same payload in username, same password
- Point to the fail page: "Blocked. Reason shown."
- Point to the green mitigation box: "The parameterized query compiled SQL structure before my input arrived. The payload was bound as a literal 20-character string to search for, not as SQL code."
- Open `auth_secure.py` in editor, point to `cursor.execute("... WHERE username = ?", (username,))`: "This single line is the entire fix. The question mark is a placeholder. Structure is compiled and locked before any value is bound."

**Minute 6 — Hardening features:**
- Open DB browser or run `SELECT username, password_hash FROM users;` in terminal: "Passwords stored as bcrypt hashes — never plaintext. The `$2b$` prefix confirms bcrypt. Even if this DB file is stolen, recovering passwords requires massive computation."
- Fail login 5 times on secure side: "Account locked. Brute force is throttled."
- Open `auth.log` in terminal: "Every event logged with timestamp, username, event type. Passwords never appear in logs."

**Minute 7 — Results and takeaway:**
- Show test matrix table: "17 test cases. T07 through T12 show the before/after contrast directly. Vulnerable path bypassed on all three attack payloads. Secure path blocked all three."
- "Takeaway: secure coding — specifically enforcing separation of SQL code from user data at the query compilation level — completely eliminates this class of attack."

---

## STEP 16: REPORT STRUCTURE (13 Sections — Write in This Order)

| Section | Content |
|---|---|
| 1. Abstract | 8–10 lines: problem, approach, key result |
| 2. Introduction | What is SQLi, why auth bypass specifically, OWASP A03:2021 |
| 3. Objectives | Four modules listed with one sentence each |
| 4. Ethical Scope Statement | Local only, test data only, academic purpose — no public systems |
| 5. Literature Survey | History, types, real breaches, OWASP ranking, references |
| 6. System Design | Architecture diagram, DB schema table, data flow description |
| 7. Implementation — Module A | The dangerous concatenation line, annotated code snippet |
| 8. Implementation — Module B | The parameterized `?` line, annotated code snippet, why it works |
| 9. Implementation — Module C | bcrypt logic, lockout logic, logging code, each explained |
| 10. Testing and Results | Full 17-row test matrix, before/after comparison, screenshot references |
| 11. Discussion | Why parameterization is stronger than validation, remaining risks, defense-in-depth |
| 12. Best Practices | Least-privilege DB user, secret management, WAF, MFA, CAPTCHA |
| 13. Conclusion and References | Summary, future extensions, OWASP link, sqlite3 docs, bcrypt docs, Stallings |

---

## STEP 17: 7-DAY EXECUTION PLAN

| Day | Exact tasks | Done when |
|---|---|---|
| Day 1 | Install flask + bcrypt. Write `database.py`. Run it. Confirm DB created with 3 users. Start literature notes. | `python database.py` prints all 3 users |
| Day 2 | Write `auth_vulnerable.py`. Write vulnerable route + template. Test T01, T03, T05 (normal flows work). | Normal login works on vulnerable side |
| Day 3 | Write `auth_secure.py` (parameterized only, no hardening yet). Test T07 vs T08 side by side. | Bypass works on vuln, blocked on secure |
| Day 4 | Add bcrypt verification, lockout, and `logger.py`. Test T09–T14. Confirm log file created. | Lockout triggers, auth.log populates |
| Day 5 | Run all 17 test cases. Take all 11 screenshots. Name files using evidence table from Step 12. | Evidence folder complete |
| Day 6 | Write full report using 13-section structure. Insert screenshots as figures. | Report draft complete |
| Day 7 | Rehearse viva script twice from memory. Run app from clean terminal to verify setup instructions work. Final proofread. | Ready to present |

---

## STEP 18: FINAL SUBMISSION PACKAGE

Organize exactly this before Eval 2:

```
submission_package/
│
├── source_code/
│   ├── app.py
│   ├── auth_vulnerable.py
│   ├── auth_secure.py
│   ├── database.py
│   ├── logger.py
│   └── templates/
│       ├── index.html
│       ├── login_vuln.html
│       ├── login_safe.html
│       ├── success.html
│       └── fail.html
│
├── setup_instructions.txt
│     → pip install flask bcrypt
│     → python database.py
│     → python app.py
│     → open http://localhost:5000
│
├── test_matrix.pdf            ← all 17 rows with results filled in
├── evidence/                  ← ev01 through ev11 screenshots
└── report.pdf                 ← 13-section report
```

---

## STEP 19: MARKS-CRITICAL CHECKLIST

Go through this the night before each evaluation:

**Before Eval 1:**
- [ ] Literature survey written covering: history, types, breaches, OWASP ranking
- [ ] Revised specification has objective, modules, input/output, constraints
- [ ] Architecture diagram drawn
- [ ] `python database.py` runs and prints all 3 test users
- [ ] App starts on port 5000 and home page loads
- [ ] At least vulnerable login works for normal credentials

**Before Eval 2:**
- [ ] App runs from a clean terminal with just two install commands
- [ ] Vulnerable and secure logic are in **separate files** with clear labels
- [ ] The dangerous concatenation line is visible and commented in `auth_vulnerable.py`
- [ ] The `?` parameterized line is visible and commented in `auth_secure.py`
- [ ] T07 bypass succeeds on vulnerable, fails on secure — same payload both times
- [ ] bcrypt hashing working (`$2b$` prefix visible in DB `password_hash` column)
- [ ] Lockout triggers after exactly 5 failures
- [ ] `auth.log` populates on every login attempt, no raw passwords in it
- [ ] All 17 test cases have results and screenshots
- [ ] Report has ethical scope statement and all 13 sections
- [ ] You can explain the `?` binding mechanism without looking at notes
- [ ] You can point to the exact dangerous line and the exact fix line during demo
- [ ] Demo rehearsed at least twice end-to-end

---

## ADDENDUM: EXTRA POINTS FROM FINAL MASTER APPROACH (APPENDED ONLY)

These points are added to ensure nothing from the final combined approach is missed.

### A) FINAL TECH CHOICE CHECK (EXPLICIT)

1. Use Python + Flask + SQLite.
2. Use raw SQL intentionally for educational visibility.
3. Avoid ORM for this assignment so vulnerability and mitigation remain explicit.
4. Keep dependencies minimal: one web framework + one password hashing package.

### B) MANDATORY TEST PLAN CHECKLIST (EXPLICIT)

1. Functional: valid login, invalid username, invalid password.
2. Security behavior: run approved SQLi-style crafted inputs on vulnerable route, then run the exact same inputs on secure route.
3. Hardening behavior: failed-attempt threshold triggers lockout; valid login during lockout is blocked; valid login after lockout expiry succeeds.
4. Robustness: empty input, long input, Unicode/special input.
5. Logging: verify each important event appears in `auth.log` and/or `audit_log` table.

### C) TEST MATRIX MINIMUM RULE (EXPLICIT)

Maintain at least 15 to 17 total test cases. Current matrix already uses 17.

### D) COMMON MISTAKES TO AVOID (EXPLICIT)

1. Submitting only theory without a working implementation.
2. Claiming input filtering alone as complete mitigation.
3. Keeping vulnerable and secure logic mixed in one module without clear separation.
4. Missing before/after evidence for the same payload.
5. Failing to demonstrate normal valid login on secure flow.
6. Logging sensitive data such as plaintext passwords.
7. Inability to explain the exact vulnerable line and exact fix line during viva.

### E) QUICK FINAL COMPLETION CHECK

1. Application runs end-to-end from a clean terminal.
2. Vulnerable path demonstrates bypass in controlled local environment.
3. Secure path blocks the same payload while preserving valid login behavior.
4. Hardening features (bcrypt, lockout, logging) are visible in demo evidence.
5. Report, matrix, evidence, and source package are all ready before Eval 2.

---

## POST-IMPLEMENTATION IMPROVEMENTS APPLIED

The following improvements were implemented after the full step-by-step build to make the project more robust and submission-friendly:

1. Import path robustness
- `app.py` now supports both package-style imports and script-style imports.
- `auth_secure.py` now supports both package-style and script-style logger imports.
- This resolves the root-level run issue with `from sql_injection_demo.app import app`.

2. Secret key handling improvement
- `app.py` now reads `APP_SECRET_KEY` from environment variable.
- A safe default remains for local coursework demo.

3. Debug-mode and port control improvement
- `app.py` now uses environment variables:
  - `FLASK_DEBUG` (default off)
  - `PORT` (default 5000)
- This avoids accidental debug-enabled runs in final demos.

4. Logger resilience visibility improvement
- `logger.py` still keeps authentication flow resilient on DB-log failure.
- Additionally, it now writes a `LOGGER_DB_WRITE_FAILED` line to `auth.log` when DB log insert fails.

5. Dependency reproducibility improvement
- Added `requirements.txt` in project folder and submission package with pinned tested versions:
  - `flask==3.1.3`
  - `bcrypt==5.0.0`

6. Submission usability improvement
- Added `run_demo.txt` in `submission_package` with exact run commands and environment variable options.

7. Submission sync improvement
- Updated `submission_package/source_code` with improved `app.py`, `auth_secure.py`, and `logger.py`.

8. Repository hygiene improvement
- Added root `.gitignore` to exclude local environment/runtime artifacts such as `.venv`, `users.db`, `auth.log`, and `__pycache__`.

9. Package initialization improvement
- Added `sql_injection_demo/__init__.py` to make package-style execution cleaner and explicit.