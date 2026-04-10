# SQL Injection-Based Authentication Bypass in a Self-Built Login Module with Parameterized Query Mitigation

**Course:** CS4033E Computer Security  
**Institution:** National Institute of Technology Calicut  
**Department:** Computer Science and Engineering  
**Semester:** VI &mdash; Winter 2025-26  
**Assignment:** Security Attack Assignment (20 marks)

---

## 1. Abstract

This report documents a controlled academic implementation of SQL injection-based authentication bypass and its mitigation using parameterized queries. A login system was built from scratch in Python and Flask with two separate authentication flows. The vulnerable flow constructs SQL queries by direct string concatenation of user input, enabling injected SQL operators to alter WHERE clause logic and bypass authentication without valid credentials. The secure flow uses parameterized query binding, where the database compiles SQL structure before any user value is supplied, making structural manipulation impossible regardless of input content. Additional hardening controls &mdash; bcrypt password hashing, account lockout after five consecutive failures, and audit logging &mdash; were implemented in the secure flow. A 17-row test matrix compared both flows under identical inputs including valid credentials, three SQL injection payloads, and edge cases. All three injection payloads bypassed the vulnerable flow and were blocked by the secure flow. Valid credentials worked correctly in the secure flow throughout. Results confirm that parameterized queries are an effective, structural defense against SQL injection authentication bypass.

---

## 2. Introduction

SQL injection is a class of attack in which user-supplied input is interpreted as SQL command syntax rather than as data. It is classified under **OWASP A03:2021 &mdash; Injection**, consistently one of the three most critical web application security risks globally. Its persistence despite being documented since 1998 reflects the ongoing prevalence of legacy code and developers who concatenate user input into SQL strings without parameterized statements.

Authentication bypass is the most immediately dangerous form of SQL injection. The login module is the primary access boundary for any system. If it can be bypassed, an attacker gains unauthorized access to protected functionality without possessing any valid credentials.

This assignment demonstrates authentication bypass in a controlled local environment with test data only, then implements and verifies the parameterized query mitigation. The comparison is made concrete through a working two-flow application, a 17-row test matrix, and 11 evidence screenshots showing before/after behavior under identical inputs.

**Ethical scope:** All testing was on a local machine using a test database with test users only. No public, live, or third-party systems were accessed. The vulnerable module exists solely for controlled academic demonstration and must not be deployed.

---

## 3. Objectives

1. Implement a vulnerable login module using direct SQL string concatenation to demonstrate authentication bypass.
2. Implement a secure login module using parameterized query binding as the primary mitigation.
3. Add defense-in-depth hardening: bcrypt password hashing, account lockout, and audit logging.
4. Execute a comparative 17-row test matrix with reproducible screenshot evidence.
5. Explain at the database execution layer why parameterized queries prevent the bypass.

---

## 4. Ethical Scope Statement

- All testing performed on local machine only
- Only test users seeded by `database.py` were used (admin, alice, bob)
- No third-party, public, live, or production systems were accessed
- The vulnerable module (`auth_vulnerable.py`) is isolated in a separate file, clearly labelled as academic-only in code comments and UI warnings
- The vulnerable module must never be deployed or used outside this controlled local demonstration

---

## 5. Literature Survey

### 5.1 Historical Background

SQL injection was first publicly documented in 1998 by Jeff Forristal in Phrack Magazine, Issue 54. Despite being known for over twenty-five years, it consistently appears in every edition of the OWASP Top 10. In OWASP Top 10 2021, it is classified as **A03:2021 &mdash; Injection**, one of the top three critical web application security risks. Its persistence reflects legacy codebases and developers who construct queries by concatenating user input rather than using parameterized statements.

### 5.2 Types of SQL Injection

| Type | Description |
|---|---|
| Classic / In-band | Input alters query logic; effect visible in response. **This assignment demonstrates this type.** |
| Error-based | DB errors exposed reveal schema details |
| Union-based | UNION SELECT appended to extract other table data |
| Blind | No direct output; attacker infers from response differences |
| Time-based Blind | DB timing functions (SLEEP) used when output suppressed |

### 5.3 Authentication Bypass Mechanism

Typical insecure login query:

```sql
SELECT * FROM users WHERE username = '<input>' AND password = '<input>'
```

Attacker inputs username: `' OR '1'='1' --`

Query becomes:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password = 'anything'
```

| Fragment | Effect |
|---|---|
| `username = ''` | Closes the username string early |
| `OR '1'='1'` | Attacker-injected always-true condition |
| `--` | SQL comment &mdash; password check commented out |
| `AND password = 'anything'` | Never evaluated |

Result: WHERE clause reduces to TRUE. First row returned. Authentication bypassed.

### 5.4 Real-World Incidents

- **Heartland Payment Systems (2008):** SQL injection led to theft of approximately 130 million credit/debit card records.
- **RockYou (2009):** SQL injection exposed 32 million user credentials stored in plaintext.
- **TalkTalk, UK (2015):** SQL injection exposed 157,000 customer records; £400,000 regulatory fine issued.

All three shared the same root cause: user input concatenated into SQL queries without parameterized statements.

### 5.5 Prevention Guidance

OWASP SQL Injection Prevention Cheat Sheet identifies parameterized queries as the **primary defense**. Input validation is listed as a secondary control that cannot substitute for parameterization, because it can be bypassed through encoding tricks, Unicode normalization, or second-order injection.

### 5.6 References

1. OWASP Top 10 2021 &mdash; A03: Injection. https://owasp.org/Top10/A03_2021-Injection/
2. OWASP SQL Injection Prevention Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
3. Python sqlite3 Documentation. https://docs.python.org/3/library/sqlite3.html
4. bcrypt library. https://pypi.org/project/bcrypt/
5. W. Stallings, *Cryptography and Network Security*, 8/e, Pearson India, 2023.
6. D. Gollmann, *Computer Security*, 3/e, John Wiley and Sons, 2006.
7. Forristal, J. (1998). NT Web Technology Vulnerabilities. *Phrack Magazine*, Issue 54.

---

## 6. System Design

### 6.1 Architecture

```
sql_injection_demo/
├── app.py               Flask routes
├── auth_vulnerable.py   Module A — unsafe SQL
├── auth_secure.py       Module B+C — parameterized query + hardening
├── logger.py            Audit logging
├── database.py          DB init and seeding
├── users.db             SQLite database
├── auth.log             Flat-file audit log
└── templates/           5 HTML templates
```

### 6.2 Database Schema

**users table:**

| Column | Type | Purpose |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| username | TEXT UNIQUE | Login identifier |
| password_plain | TEXT | Vulnerable module only |
| password_hash | TEXT | bcrypt hash, secure module only |
| role | TEXT | 'administrator' or 'user' |
| failed_attempts | INTEGER | Lockout counter |
| lock_until | REAL | Unix timestamp of lockout expiry (NULL = not locked) |

**audit_log table:**

| Column | Type | Purpose |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| timestamp | TEXT | Event datetime |
| username | TEXT | Username involved |
| event | TEXT | Event label |
| source | TEXT | Source IP |

**Design note:** `password_plain` simulates the same careless developer who writes concatenated SQL also storing plaintext passwords. The secure module never reads this column. This contrast is visible in the schema itself.

### 6.3 Data Flow

**Vulnerable path (Module A):**
1. User submits to POST `/login_vuln`
2. username + password concatenated into raw SQL string
3. DB executes the string — if any row returns, login accepted
4. Result page shows the exact constructed query

**Secure path (Module B+C):**
1. User submits to POST `/login_safe`
2. Parameterized lookup: `SELECT * FROM users WHERE username = ?`
3. DB compiles template, binds value as data
4. Lockout check &rarr; bcrypt hash verify &rarr; counter update
5. logger.py writes to auth.log and audit_log
6. Result page shows parameterized template with mitigation explanation

### 6.4 Security Boundary Comparison

| Property | Module A | Module B+C |
|---|---|---|
| SQL construction | String concatenation | Parameterized placeholder |
| Password comparison | SQL string equality | bcrypt.checkpw() |
| Brute-force protection | None | 5 attempts, 300s lockout |
| Audit trail | None | auth.log + audit_log |
| Error messages | Raw error may show | "Invalid credentials." only |
| Injection resistance | None | Full — input bound as data |

---

## 7. Implementation &mdash; Module A: Vulnerable Flow

**File:** `auth_vulnerable.py`

```python
# THE DANGEROUS LINE — user input becomes part of SQL code
query = (
    "SELECT * FROM users "
    "WHERE username = '" + username + "' "
    "AND password_plain = '" + password + "'"
)
cursor.execute(query)
```

The database receives a fully constructed SQL string. It cannot distinguish developer-written SQL from user-injected SQL. If `username` is `' OR '1'='1' --`:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password_plain = 'anything'
```

`OR '1'='1'` is always true. `--` comments out the password check. The database returns the first row. Authentication succeeds with no valid credentials.

The module is isolated in its own file, contains prominent academic-only warnings, and is never used by the secure path. The result page displays the exact query executed so the evaluator can directly read how the payload altered the WHERE clause.

---

## 8. Implementation &mdash; Module B: Secure Flow (Parameterized Query)

**File:** `auth_secure.py`

```python
# THE FIX — parameterized placeholder binding
c.execute("SELECT * FROM users WHERE username = ?", (username,))
```

**Why this prevents bypass &mdash; at the engine level:**

| Step | What happens |
|---|---|
| 1 | App sends template: `SELECT * FROM users WHERE username = ?` |
| 2 | DB parser tokenizes and compiles. Execution plan built. Structure locked. |
| 3 | User value `' OR '1'='1' --` sent to DB driver |
| 4 | Driver binds value as typed string data into the `?` slot |
| 5 | Parser never sees the value. Cannot alter grammar. |
| 6 | DB searches for user whose username literally equals `' OR '1'='1' --` |
| 7 | No such user. Returns nothing. Login fails correctly. |

**Why input validation cannot substitute:** Validation filters characters at the application layer. URL encoding (`%27` &rarr; `'`), Unicode normalization, or second-order injection can bypass filters. Parameterization works at the query compilation layer &mdash; by the time input arrives, SQL structure is already locked.

---

## 9. Implementation &mdash; Module C: Hardening Controls

### 9.1 bcrypt Password Hashing

```python
# Seeding:
hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

# Verification:
password_correct = bcrypt.checkpw(password.encode(), user["password_hash"].encode())
```

bcrypt generates a random salt per hash. Same password &rarr; different hash on every call &mdash; defeating rainbow table attacks. bcrypt is intentionally slow: even if the database is stolen, brute-forcing hashes is computationally expensive per attempt. Plaintext passwords are never stored or compared.

### 9.2 Account Lockout

```python
MAX_ATTEMPTS = 5     # consecutive failures before lockout
LOCKOUT_SECS = 300   # 5-minute duration

if new_attempts >= MAX_ATTEMPTS:
    lock_until = time.time() + LOCKOUT_SECS
```

`failed_attempts` increments on each wrong password. After threshold, `lock_until` is set. Subsequent attempts return a message showing remaining locked time. On successful login, both counters reset. This defeats online brute-force attacks.

### 9.3 Audit Logging

Events written to both `auth.log` (flat, human-readable) and `audit_log` DB table (structured). Events logged:

| Event | Trigger |
|---|---|
| LOGIN_SUCCESS | Credentials verified |
| LOGIN_FAIL_USER_NOT_FOUND | Username not in DB |
| LOGIN_FAIL_WRONG_PASSWORD_ATTEMPT_N | Wrong password, attempt N |
| ACCOUNT_LOCKED_AFTER_N_FAILURES | Lockout triggered |
| LOGIN_BLOCKED_ACCOUNT_LOCKED | Attempt during lockout |

Raw passwords are never logged. Only username, event, timestamp, source IP.

### 9.4 User Enumeration Prevention

Both unknown username and wrong password return the same message: `"Invalid credentials."` &mdash; preventing an attacker from learning which field was wrong.

---

## 10. Testing and Results

### 10.1 Complete Test Matrix &mdash; 17 Rows

| ID | Username | Password | Module | Expected | Actual | Pass/Fail |
|---|---|---|---|---|---|---|
| T01 | admin | adminpass123 | Vulnerable | Success | Success | **PASS** |
| T02 | admin | adminpass123 | Secure | Success | Success | **PASS** |
| T03 | alice | wrongpass | Vulnerable | Fail | Fail | **PASS** |
| T04 | alice | wrongpass | Secure | Fail | Fail | **PASS** |
| T05 | nobody | anything | Vulnerable | Fail | Fail | **PASS** |
| T06 | nobody | anything | Secure | Fail | Fail | **PASS** |
| T07 | `' OR '1'='1' --` | anything | **Vulnerable** | **BYPASS** | **BYPASS** | **PASS** |
| T08 | `' OR '1'='1' --` | anything | **Secure** | **BLOCKED** | **BLOCKED** | **PASS** |
| T09 | `admin'--` | anything | **Vulnerable** | **BYPASS** | **BYPASS** | **PASS** |
| T10 | `admin'--` | anything | **Secure** | **BLOCKED** | **BLOCKED** | **PASS** |
| T11 | `' OR 1=1--` | anything | **Vulnerable** | **BYPASS** | **BYPASS** | **PASS** |
| T12 | `' OR 1=1--` | anything | **Secure** | **BLOCKED** | **BLOCKED** | **PASS** |
| T13 | alice | wrongpass &times;5 | Secure | Locked | Locked | **PASS** |
| T14 | alice | alice2024 | Secure (locked) | Still locked | Still locked | **PASS** |
| T15 | (empty) | (empty) | Both | Fail gracefully | Fail | **PASS** |
| T16 | 500-char string | anything | Both | Fail, no crash | Fail | **PASS** |
| T17 | &uuml;n&iuml;c&ouml;d&eacute; | anything | Both | Fail gracefully | Fail | **PASS** |

**Total: 17 / 17 PASSED**

### 10.2 Before / After Comparison

| Input | Vulnerable Result | Secure Result |
|---|---|---|
| Valid credentials | Login success | Login success |
| Wrong password | Login fail | Login fail |
| `' OR '1'='1' --` | **BYPASS** | **BLOCKED** |
| `admin'--` | **BYPASS** | **BLOCKED** |
| `' OR 1=1--` | **BYPASS** | **BLOCKED** |
| 5&times; wrong password | No protection | Account locked 300s |
| Empty input | Fail gracefully | Fail gracefully |
| 500-char input | Fail, no crash | Fail, no crash |

### 10.3 Evidence Screenshots

| File | Content |
|---|---|
| ev01_normal_vuln.png | Normal login success &mdash; vulnerable side |
| ev02_normal_secure.png | Normal login success &mdash; secure side |
| ev03_attack_bypass.png | T07 bypass with query displayed |
| ev04_attack_blocked.png | T08 blocked with mitigation banner |
| ev05_comment_attack.png | T09 admin'-- bypass |
| ev06_comment_blocked.png | T10 admin'-- blocked |
| ev07_lockout.png | T13 lockout triggered |
| ev08_audit_log.png | auth.log contents |
| ev09_code_vuln.png | Dangerous concatenation line |
| ev10_code_secure.png | Parameterized query line |
| ev11_bcrypt_hash.png | `$2b$` hash in DB column |

---

## 11. Discussion

### 11.1 Why Parameterization Is the Essential Defense

Parameterized queries enforce code/data separation at the database execution layer. SQL structure is compiled before user input is ever processed. There is no phase where input can alter grammar &mdash; this is independent of what the input contains.

Input validation is application-layer filtering. It can be bypassed through URL encoding, Unicode normalization, double encoding, or second-order injection where stored input is later used in an unprotected query. Validation is useful as an additional layer but structurally cannot provide the same guarantee as parameterization.

### 11.2 Defense-in-Depth

The three hardening controls address separate threat vectors:

| Control | Threat addressed |
|---|---|
| bcrypt hashing | Credential recovery if DB stolen |
| Account lockout | Online brute-force guessing |
| Audit logging | Detection, traceability, forensics |

Together they provide defense-in-depth &mdash; multiple independent layers so no single failure creates a complete breach.

### 11.3 Limitations

- Uses SQLite and Flask development server &mdash; not production infrastructure
- Production deployment would need HTTPS, Gunicorn/Nginx, secret management, least-privilege DB user

---

## 12. Best Practices

### 12.1 Implemented in This Project

| Practice | Where |
|---|---|
| Parameterized queries | auth_secure.py |
| bcrypt password hashing | database.py + auth_secure.py |
| Account lockout | auth_secure.py |
| Audit logging | logger.py |
| Generic error messages | auth_secure.py |
| Input length limits (200 chars) | app.py |
| Separate vulnerable/secure files | auth_vulnerable.py vs auth_secure.py |

### 12.2 Recommended for Production

- Least-privilege DB user (no DROP/ALTER rights)
- HTTPS/TLS on all connections
- Secret management for keys (environment variables, vault)
- Web Application Firewall (WAF)
- Multi-factor authentication (MFA) for privileged accounts
- CAPTCHA after repeated failures
- SIEM integration for anomaly detection

---

## 13. Conclusion

This assignment achieved all stated objectives. The vulnerable login module confirmed that string-concatenated SQL allows an attacker to bypass authentication entirely by injecting always-true SQL conditions, without possessing any valid credentials. The secure login module confirmed that parameterized queries prevent the same bypass by compiling SQL structure before any user value arrives, making structural manipulation impossible.

Three distinct SQL injection payloads &mdash; tautology injection (`' OR '1'='1' --`), comment truncation (`admin'--`), and alternate tautology (`' OR 1=1--`) &mdash; were tested. All three bypassed the vulnerable flow and all three were blocked by the secure flow, while valid credentials continued to work correctly. Account lockout, bcrypt hashing, and audit logging demonstrated defense-in-depth against related threat vectors.

The core conclusion: parameterized queries provide a structural guarantee against SQL injection authentication bypass that input filtering alone cannot match, because they operate at the database execution layer independently of input content.

**Future extensions** for a complete production posture: MFA, CAPTCHA after repeated failures, HTTPS enforcement, SIEM integration, and role-based access control (RBAC).

---

## References

1. OWASP Top 10 2021 &mdash; A03: Injection. https://owasp.org/Top10/A03_2021-Injection/
2. OWASP SQL Injection Prevention Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
3. Python sqlite3 Documentation. https://docs.python.org/3/library/sqlite3.html
4. bcrypt library documentation. https://pypi.org/project/bcrypt/
5. W. Stallings, *Cryptography and Network Security &mdash; Principles and Practice*, 8/e, Pearson India, 2023.
6. D. Gollmann, *Computer Security*, 3/e, John Wiley and Sons Ltd., 2006.
7. Forristal, J. (1998). NT Web Technology Vulnerabilities. *Phrack Magazine*, Issue 54.
