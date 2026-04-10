# Technical Explanation &mdash; SQL Injection and Parameterized Query Mitigation

**Course:** CS4033E Computer Security | NIT Calicut

---

## 1. Why the Vulnerable Version Is Exploitable

### The dangerous code

```python
query = (
    "SELECT * FROM users "
    "WHERE username = '" + username + "' "
    "AND password_plain = '" + password + "'"
)
cursor.execute(query)
```

User input is pasted directly into the SQL string. The database receives a fully constructed SQL statement. It cannot distinguish which parts were written by the developer and which parts came from the user.

### Exact attack walkthrough

Attacker enters:
```
username:  ' OR '1'='1' --
password:  anything
```

The string the application constructs:
```sql
SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password_plain = 'anything'
```

Token-by-token breakdown:

| Fragment | Role |
|---|---|
| `username = ''` | Closes the username string early with empty value |
| `OR '1'='1'` | Attacker-injected always-true condition |
| `--` | SQL comment &mdash; everything after is ignored |
| `AND password_plain = 'anything'` | Password check &mdash; commented out, never evaluated |

Result: WHERE clause reduces to `OR TRUE` = `TRUE`. Database returns the first row. Login succeeds. Attacker authenticated with no valid password.

### Second payload: `admin'--`

```sql
SELECT * FROM users WHERE username = 'admin'--' AND password_plain = 'anything'
```

Username matched to `admin`, then `--` comments out the password check entirely. Admin account accessed without knowing the password.

### Third payload: `' OR 1=1--`

```sql
SELECT * FROM users WHERE username = '' OR 1=1--' AND password_plain = 'anything'
```

`1=1` is always true. Password check commented out. Same result.

---

## 2. Why Parameterized Queries Prevent the Bypass

### The secure code

```python
c.execute("SELECT * FROM users WHERE username = ?", (username,))
```

### What happens at the database engine level &mdash; step by step

| Step | What happens |
|---|---|
| 1 | App sends template to DB: `SELECT * FROM users WHERE username = ?` |
| 2 | DB parser tokenizes and builds execution plan. Structure compiled and locked. |
| 3 | App sends the user value: `' OR '1'='1' --` |
| 4 | DB driver binds the value as a typed string literal into the `?` slot |
| 5 | The parser has already finished. Value is not re-parsed. |
| 6 | DB executes: find user whose username literally equals `' OR '1'='1' --` |
| 7 | No such user in the table. Returns nothing. Login fails correctly. |

**The fundamental guarantee:** SQL code (structure) and user data are processed in completely separate phases. There is no phase where user input touches the SQL parser.

### Side-by-side comparison

| Property | Vulnerable | Secure |
|---|---|---|
| Input processed by SQL parser | Yes &mdash; can alter structure | No &mdash; structure already compiled |
| `' OR '1'='1' --` treated as | SQL logic altering WHERE | 20-char literal string |
| `admin'--` treated as | Username + SQL comment | Literal string `admin'--` |
| Authentication result | Bypassed | Blocked correctly |

---

## 3. Why Input Validation Alone Is Insufficient

Input validation (filtering `'`, `--`, `OR` etc.) is useful but cannot be the primary defense:

1. **Encoding attacks:** `%27` decodes to `'` after validation has run
2. **Unicode normalization:** Unicode lookalikes for SQL characters can bypass character filters
3. **Second-order injection:** Input stored cleanly, later retrieved and used in an unprotected query without re-validation
4. **Developer error:** Custom filters are custom code with potential gaps and edge cases

Parameterized queries have none of these weaknesses. They operate at the DB driver layer, independently of input content. It is structurally impossible to alter query grammar through a bound parameter.

---

## 4. bcrypt Password Hashing &mdash; Why It Matters

Even with SQL injection fully prevented, if the database is leaked through another attack vector, plaintext passwords would be immediately usable.

```
bcrypt(password, salt, cost_factor)  →  hash
```

- **Salt:** Random bytes generated per hash. Same password &rarr; different hash every time. Defeats pre-computed rainbow tables.
- **Cost factor:** bcrypt is designed to be slow. Increasing the factor makes brute-force expensive as hardware improves.
- **One-way:** Cannot reverse the hash to recover the password. Attacker must brute-force each hash individually.

The secure module uses:
```python
bcrypt.checkpw(password.encode(), stored_hash.encode())
```

This hashes the input with the same salt embedded in the stored hash and compares. Plaintext is never stored or compared directly.

---

## 5. Account Lockout &mdash; Why It Matters

Without lockout, an attacker can attempt unlimited passwords. Brute-forcing bcrypt is slow per attempt but feasible at scale with enough attempts.

The secure module:
- `MAX_ATTEMPTS = 5` &mdash; threshold before lockout
- `LOCKOUT_SECS = 300` &mdash; 5-minute lock duration
- `failed_attempts` column tracks consecutive failures
- `lock_until` stores the Unix timestamp when lock expires

On each wrong password: `failed_attempts` increments. At threshold: `lock_until` = now + 300. During lock: all attempts blocked with remaining time shown. On success: both reset to 0 / NULL.

---

## 6. Audit Logging &mdash; Why It Matters

Logging provides traceability. Without logs, there is no evidence of what happened, when, and from where.

Events logged:

| Event | When |
|---|---|
| `LOGIN_SUCCESS` | Credentials verified |
| `LOGIN_FAIL_USER_NOT_FOUND` | Username does not exist |
| `LOGIN_FAIL_WRONG_PASSWORD_ATTEMPT_N` | Wrong password, attempt N |
| `ACCOUNT_LOCKED_AFTER_N_FAILURES` | Lockout threshold reached |
| `LOGIN_BLOCKED_ACCOUNT_LOCKED` | Attempt during active lockout |

**Critical rule:** Raw passwords are never logged. Only username, event type, timestamp, and source IP.

---

## 7. Short Viva Answer (30&ndash;45 seconds)

> "The vulnerable login is exploitable because it concatenates user input directly into the SQL string. This lets an attacker inject SQL operators that alter the WHERE clause logic &mdash; so the condition becomes always-true and authentication is bypassed without any valid password.
>
> The secure login fixes this with a parameterized query. The database receives and compiles the query template before any user value is supplied. The value is then bound as typed data &mdash; it cannot alter SQL grammar because the parser has already finished.
>
> On top of that, bcrypt protects stored passwords from being usable even if the database is leaked. Account lockout defeats brute-force attempts. Audit logging records every event for traceability. Together this is defense-in-depth &mdash; and the parameterized query is the essential primary control."

---

## 8. Common Viva Follow-Up Answers

**Q: Is parameterization enough by itself?**  
It is the primary and essential defense for SQL injection. Production systems should still add validation, least-privilege DB accounts, safe error handling, monitoring, and rate limiting for complete security posture.

**Q: Why not rely only on input sanitization?**  
Sanitization can have gaps and can be bypassed through encoding. Parameterized execution is structural &mdash; it works regardless of input content.

**Q: Why keep vulnerable code at all?**  
Only for controlled academic demonstration in local test environment. Isolated in its own file, clearly labelled, never deployed.

**Q: What is user enumeration?**  
If the app says "username not found" vs "wrong password," an attacker learns which usernames are valid. The secure module always returns "Invalid credentials." preventing enumeration.

**Q: What proves mitigation in this project?**  
The same three payloads (T07, T09, T11) that bypass vulnerable authentication are all blocked by secure authentication, while valid credentials (T02) still work. Direct before/after comparison under identical inputs.

**Q: What other mitigations exist beyond parameterization?**  
Least-privilege DB user, generic error messages, input length limits, WAF, MFA, CAPTCHA, SIEM logging in production.

**Q: Why bcrypt over MD5 or SHA-1?**  
MD5 and SHA-1 are fast &mdash; billions of hashes per second possible on modern hardware. bcrypt is intentionally slow and includes salt. It is designed specifically for password storage.

**Q: What is second-order injection?**  
Input is stored safely (e.g. after validation), but later retrieved and used in a different unprotected SQL query without re-validation. Parameterization prevents this because it protects at the query execution layer, not the input layer.
