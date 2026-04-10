# CS4033E: Computer Security — Security Assignment (Evaluation I)
## SQL Injection-Based Authentication Bypass in a Self-Built Login Module with Parameterized Query Mitigation

**Name:** Adimulam Yaswanth Veera Nagesh  
**Roll Number:** B230755CS  
**Course:** CS4033E Computer Security | NIT Calicut  
**Semester:** VI B.Tech. CSE — Winter 2025-26  
**Submission Date:** 11 April 2026

---

## 1. Title of Security Assignment

**SQL Injection-Based Authentication Bypass in a Self-Built Login Module with Parameterized Query Mitigation**

*Adimulam Yaswanth Veera Nagesh — B230755CS*

This assignment involves coding a login system from scratch in Python and Flask to demonstrate SQL injection-based authentication bypass through an intentionally vulnerable module, followed by mitigation using parameterized queries, with additional hardening through bcrypt password hashing, account lockout, and audit logging.

---

## 2. Abstract

SQL injection is a code injection technique where an attacker inserts malicious SQL syntax into input fields to manipulate the backend database query. When a login module constructs SQL queries by concatenating user-supplied input directly into SQL strings, an attacker can inject always-true conditions that bypass authentication entirely without possessing any valid credentials. This is known as authentication bypass and represents one of the most critical forms of SQL injection, as it defeats the primary access control boundary of any system.

This assignment implements a self-built login system from scratch in Python and Flask with two distinct authentication flows. The first is a vulnerable module that uses string-concatenated SQL to demonstrate authentication bypass in a controlled local environment. The second is a secure module that uses parameterized query binding as the primary mitigation, supplemented by bcrypt password hashing, account lockout after five consecutive failures, and audit logging. A 17-row comparative test matrix was executed under identical inputs across both flows, including normal credential tests, three SQL injection payloads, and edge cases. All three injection payloads successfully bypassed the vulnerable flow and were blocked by the secure flow, while valid credentials continued to function correctly. The results confirm that parameterized queries prevent SQL injection at the database execution layer by separating SQL code structure from user-supplied data, an approach that cannot be circumvented through input content manipulation.

---

## 3. Introduction

SQL injection (SQLi) is ranked under OWASP A03:2021 — Injection, one of the most critical web application security risks globally [1]. First publicly documented in 1998, it has appeared in every edition of the OWASP Top 10 and has been responsible for major security breaches including the Heartland Payment Systems incident (2008, ~130 million card records) and the RockYou breach (2009, 32 million plaintext credentials).

Authentication is the primary access boundary in any multi-user system. If the login module is vulnerable to SQL injection, an attacker does not need to know any valid username or password to gain access. By injecting SQL syntax through a normal input field, the attacker can alter the WHERE clause logic so that it always evaluates to true, causing the database to return the first user row regardless of the supplied credentials.

The core cause of this vulnerability is a pattern called string concatenation, where the developer builds the SQL query by directly inserting user-supplied values into the query string. The correct and complete fix is parameterized query binding (also called prepared statements), where the query template is compiled by the database engine before any user value is supplied. This makes structural manipulation through input impossible.

This assignment builds both the vulnerable and secure implementations side by side in Python and Flask, with SQLite as the database, to demonstrate the vulnerability and its mitigation through a working, demonstrable system. No existing attack tools are used — the entire login system is written from scratch.

---

## 4. Literature Survey

This section surveys tools, techniques, and literature on SQL injection detection, exploitation, and prevention.

### 4.1 sqlmap

sqlmap [2] is an open-source penetration testing tool that automates the detection and exploitation of SQL injection vulnerabilities. Key functionalities include fingerprinting the database management system, extracting database contents, and supporting various injection techniques including boolean-based, time-based, and error-based. It supports MySQL, PostgreSQL, SQLite, Oracle, and Microsoft SQL Server. sqlmap is used in professional penetration testing but requires an existing web target. In this assignment, sqlmap is not used for the attack — the vulnerable query is coded manually — but it serves as a reference for understanding what automated SQLi tools exploit.

### 4.2 Burp Suite

Burp Suite [3] is a web application security testing platform. Its Scanner component can detect SQL injection points by fuzzing input parameters with payloads. The Repeater and Intruder modules allow manual crafting and replay of HTTP requests. Burp Suite is widely used for identifying injection points and analyzing HTTP traffic. It is relevant to this assignment as a tool that could identify the vulnerable login endpoint in a real-world scenario.

### 4.3 OWASP Testing Guide (OTG-INPVAL-005)

The OWASP Testing Guide [1] provides methodology for testing SQL injection including identification of injection points, characterization of the injection type, and assessment of impact. It recommends parameterized queries as the primary prevention measure and provides test vectors including tautology-based (`' OR '1'='1' --`), union-based, and time-based payloads. The test payloads used in this assignment are directly derived from this guide.

### 4.4 Parameterized Queries / Prepared Statements

Parameterized queries [4] are the standard prevention mechanism recommended by OWASP, NIST, and all major database vendors. The application sends a query template with placeholder markers to the database engine, which compiles the query structure. User-supplied values are then bound to the placeholders as typed data, never as SQL text. This means the SQL parser sees only the template — not the user value — making it structurally impossible for input to alter query logic regardless of its content. All major database libraries support this pattern: Python sqlite3 uses `?`, psycopg2 uses `%s`, and Java JDBC uses `?` with `PreparedStatement`.

### 4.5 bcrypt Password Hashing

bcrypt [5] is a password hashing function designed by Niels Provos and David Mazières, published in 1999. It incorporates a random salt to prevent rainbow table attacks and has a configurable cost factor that makes the hash computation intentionally slow. Increasing the cost factor as hardware improves maintains resistance to brute-force. Python's bcrypt library implements this and is the industry standard for password storage alongside Argon2 and PBKDF2. In this assignment, bcrypt is used in the secure module to store and verify passwords.

### 4.6 Comparison of Prevention Techniques

| Technique | Layer | Prevents SQLi | Bypass Risk | Notes |
|---|---|---|---|---|
| Parameterized queries | DB execution layer | Yes (structural) | None via input | Primary recommended defense |
| Input validation / filtering | Application layer | Partial | Encoding, unicode tricks | Secondary control only |
| Stored procedures | DB layer | Yes (if used correctly) | Possible if dynamic SQL used inside | Must still use parameters |
| WAF (Web Application Firewall) | Network/HTTP layer | Partial | Custom payloads, evasion | Additional layer, not primary |
| ORM frameworks | Application layer | Yes (if not bypassed) | Raw query methods bypass it | Depends on ORM usage |

Parameterized queries are the only technique that provides a structural guarantee — they work regardless of input content, at the query compilation layer.

---

## 5. System/Network Environment

### 5.1 Hardware Requirements

| Component | Specification |
|---|---|
| Processor | Any modern CPU (Intel/AMD x86-64 or ARM) |
| RAM | Minimum 512 MB (2 GB recommended) |
| Storage | 100 MB free space |
| Network | Loopback only (localhost) — no external network required |

### 5.2 Software Requirements

| Component | Version | Purpose |
|---|---|---|
| Operating System | Ubuntu 22.04 / any Linux or macOS | Development and demo environment |
| Python | 3.9 or higher | Backend language |
| Flask | 3.0 or higher | Web framework |
| bcrypt | 4.0 or higher | Password hashing library |
| SQLite | Built into Python stdlib | Database (no separate install needed) |
| Web browser | Any modern browser (Firefox, Chrome) | Frontend UI |

### 5.3 Environment Notes

- All testing is performed on localhost only (127.0.0.1:5000)
- No external network connections are made
- The vulnerable module runs only in this local test environment
- SQLite database file (`users.db`) is created locally by `database.py`
- No production server, cloud instance, or third-party system is involved

### 5.4 Installation

```bash
pip install flask bcrypt
python database.py    # initialize DB
python app.py         # start server at http://localhost:5000
```

---

## 6. Design of Modules

### 6.1 Module A — Vulnerable Login Module

**File:** `auth_vulnerable.py`

**Purpose:** Demonstrate SQL injection authentication bypass using unsafe string-concatenated query construction.

**Algorithm:**

```
Input:  username (string), password (string)
Output: (user_dict or None, query_string, error or None)

1. Build SQL query by string concatenation:
      query = "SELECT * FROM users WHERE username = '" +
              username + "' AND password_plain = '" + password + "'"
2. Execute query against users.db
3. If cursor returns any row → return that user dict (login accepted)
4. If no row → return None (login rejected)
5. If SQL error → return None and error string
```

**Attack Scenario:**

When `username = ' OR '1'='1' --` and `password = anything`:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password_plain = 'anything'
```

`OR '1'='1'` is always TRUE. `--` comments out the password check. The first row is returned. Authentication is bypassed.

**Input:** username, password strings (no validation)  
**Output:** user row if found (even via injection), the constructed SQL query for display

---

### 6.2 Module B — Secure Login Module (Parameterized Query)

**File:** `auth_secure.py`

**Purpose:** Demonstrate SQL injection prevention using parameterized query binding.

**Algorithm:**

```
Input:  username (string), password (string), source_ip (string)
Output: (user_dict or None, message or None, success_bool)

1. Execute parameterized lookup:
      cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
   [DB compiles template first; username bound as data, not SQL]
2. If no user found → log event → return "Invalid credentials.", False
3. Check lock_until: if time.time() < lock_until → return lockout message, False
4. bcrypt.checkpw(password.encode(), user["password_hash"].encode())
5. If password incorrect:
      Increment failed_attempts
      If failed_attempts >= MAX_ATTEMPTS (5): set lock_until = now + 300
      Log event
      Return "Invalid credentials.", False
6. If password correct:
      Reset failed_attempts = 0, lock_until = NULL
      Log LOGIN_SUCCESS
      Return user dict, True
```

**Why the ? placeholder prevents injection:**

The database engine receives the template `SELECT * FROM users WHERE username = ?` and compiles its execution plan. The query structure is locked. The user value is then bound as a typed string literal — it is never parsed as SQL. `' OR '1'='1' --` becomes a 20-character literal to search for. No user with that username exists. Login fails correctly.

**Input:** username, password, source IP  
**Output:** user dict on success; error message on failure

---

### 6.3 Module C — Hardening Controls

**File:** `auth_secure.py` (integrated) and `logger.py`

#### 6.3.1 bcrypt Password Hashing

```
At database setup:
  hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
  Store hash in users.password_hash column

At login:
  bcrypt.checkpw(input_password.encode(), stored_hash.encode())
```

bcrypt generates a random salt per hash. The same password produces a different hash on every call — defeating rainbow table attacks. The cost factor makes brute-forcing computationally expensive.

#### 6.3.2 Account Lockout

```
MAX_ATTEMPTS = 5
LOCKOUT_SECS = 300

On each wrong password:
  failed_attempts += 1
  if failed_attempts >= 5:
    lock_until = now + 300
    
On locked account access:
  remaining = lock_until - now
  Return "Account locked. Try again in N seconds."

On successful login:
  failed_attempts = 0
  lock_until = NULL
```

#### 6.3.3 Audit Logging

```
On every auth event:
  Write to auth.log:
    [timestamp] user=<username> event=<EVENT> source=<ip>
  Write to audit_log table in users.db:
    INSERT INTO audit_log (timestamp, username, event, source)
```

Events logged: LOGIN_SUCCESS, LOGIN_FAIL_USER_NOT_FOUND, LOGIN_FAIL_WRONG_PASSWORD_ATTEMPT_N, ACCOUNT_LOCKED_AFTER_N_FAILURES, LOGIN_BLOCKED_ACCOUNT_LOCKED.

Raw passwords are never logged.

---

### 6.4 Flask Routes Module

**File:** `app.py`

| Route | Method | Handler | Description |
|---|---|---|---|
| `/` | GET | `index()` | Home page with module selector |
| `/login_vuln` | GET/POST | `login_vuln()` | Module A vulnerable login |
| `/login_safe` | GET/POST | `login_safe()` | Module B+C secure login |

**Input:** HTTP form POST with `username` and `password` fields (max 200 chars each)  
**Output:** Rendered HTML result page showing login outcome, SQL query, and mode-specific explanation

---

### 6.5 Database Schema

**users table:**

| Column | Type | Purpose |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| username | TEXT UNIQUE | Login identifier |
| password_plain | TEXT | Vulnerable module only (intentional naive mistake) |
| password_hash | TEXT | bcrypt hash for secure module |
| role | TEXT | 'administrator' or 'user' |
| failed_attempts | INTEGER | Lockout counter |
| lock_until | REAL | Lockout expiry Unix timestamp |

**audit_log table:**

| Column | Type | Purpose |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| timestamp | TEXT | Event datetime |
| username | TEXT | Username involved |
| event | TEXT | Event type label |
| source | TEXT | Source IP |

---

## 7. Progress of Implementation

All implementation steps are complete. The full working application has been built and tested.

### Completed Steps

| Step | Description | Status |
|---|---|---|
| 1 | Project structure and virtual environment | Complete |
| 2 | `database.py` — DB init and user seeding | Complete |
| 3 | `auth_vulnerable.py` — Module A | Complete |
| 4 | `auth_secure.py` — Module B+C | Complete |
| 5 | `logger.py` — audit logging | Complete |
| 6 | `app.py` — Flask routes | Complete |
| 7 | HTML templates (5 pages) | Complete |
| 8 | Application verified running at localhost:5000 | Complete |
| 9 | 17-row test matrix executed — 17/17 passed | Complete |
| 10 | 11 evidence screenshots captured | Complete |

### Test Matrix Summary (17 rows)

| ID | Username Input | Module | Expected | Actual | Result |
|---|---|---|---|---|---|
| T01 | admin / adminpass123 | Vulnerable | Success | Success | PASS |
| T02 | admin / adminpass123 | Secure | Success | Success | PASS |
| T07 | `' OR '1'='1' --` | Vulnerable | BYPASS | BYPASS | PASS |
| T08 | `' OR '1'='1' --` | Secure | BLOCKED | BLOCKED | PASS |
| T09 | `admin'--` | Vulnerable | BYPASS | BYPASS | PASS |
| T10 | `admin'--` | Secure | BLOCKED | BLOCKED | PASS |
| T11 | `' OR 1=1--` | Vulnerable | BYPASS | BYPASS | PASS |
| T12 | `' OR 1=1--` | Secure | BLOCKED | BLOCKED | PASS |
| T13 | alice / wrongpass ×5 | Secure | Locked | Locked | PASS |

(Full 17-row matrix available in test_matrix_results_step11_17rows.md)

### Evidence Captured

- ev01–ev02: Normal login on both modules
- ev03–ev04: Core attack bypass and block
- ev05–ev06: Comment-truncation attack and block
- ev07: Account lockout triggered
- ev08: Audit log entries visible
- ev09–ev10: Code snippets showing dangerous line vs parameterized line
- ev11: bcrypt `$2b$` hash visible in database

---

## 8. Conclusion

This assignment successfully demonstrated SQL injection-based authentication bypass and its mitigation through a working self-built implementation. The vulnerable login module confirmed that string-concatenated SQL construction allows an attacker to bypass authentication by injecting always-true conditions, without requiring any valid credentials. Three distinct injection payloads — tautology injection, comment truncation, and alternate tautology — all successfully bypassed the vulnerable flow.

The secure login module confirmed that parameterized queries prevent this class of attack entirely. By compiling the SQL structure before any user value is supplied, the database engine treats all input as literal data — injection payloads become meaningless search strings rather than executable SQL logic. This protection operates at the database execution layer and cannot be bypassed through input content manipulation, unlike application-layer filtering.

The additional hardening controls — bcrypt password hashing, account lockout, and audit logging — address related threat vectors: credential theft through database exposure, brute-force guessing, and lack of incident traceability respectively. Together, these form a defense-in-depth posture that is far more robust than any single control.

The primary takeaway is that parameterized queries are not optional — they are the essential baseline for any application that interacts with a database using user-supplied input. All major web frameworks and database libraries support them with minimal code change.

---

## 9. References

[1] OWASP Foundation, "OWASP Top 10 2021 — A03: Injection," *OWASP*, 2021. [Online]. Available: https://owasp.org/Top10/A03_2021-Injection/

[2] sqlmap project, "sqlmap: Automatic SQL injection and database takeover tool," *GitHub*, 2024. [Online]. Available: https://github.com/sqlmapproject/sqlmap

[3] PortSwigger Ltd., "Burp Suite Web Security Testing Guide," *PortSwigger*, 2024. [Online]. Available: https://portswigger.net/burp/documentation

[4] OWASP Foundation, "SQL Injection Prevention Cheat Sheet," *OWASP Cheat Sheet Series*, 2024. [Online]. Available: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

[5] N. Provos and D. Mazieres, "A Future-Adaptable Password Scheme," in *Proc. USENIX Annual Technical Conference (FREENIX Track)*, Monterey, CA, USA, 1999, pp. 81–91.

[6] Python Software Foundation, "sqlite3 — DB-API 2.0 interface for SQLite databases," *Python Documentation*, 2024. [Online]. Available: https://docs.python.org/3/library/sqlite3.html

[7] pypi.org, "bcrypt 4.x — Modern password hashing for your software and your servers," *PyPI*, 2024. [Online]. Available: https://pypi.org/project/bcrypt/

[8] W. Stallings, *Cryptography and Network Security: Principles and Practice*, 8th ed. Pearson India, 2023, ch. 20: "Software Security."

[9] D. Gollmann, *Computer Security*, 3rd ed. John Wiley and Sons Ltd., 2006, ch. 9: "Web Security."

[10] J. Forristal, "NT Web Technology Vulnerabilities," *Phrack Magazine*, vol. 8, no. 54, art. 8, 1998. [Online]. Available: http://phrack.org/issues/54/8.html

---

*Report compiled by Adimulam Yaswanth Veera Nagesh B230755CS | CS4033E Computer Security | NIT Calicut | Winter 2025-26*
