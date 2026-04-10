# Evaluation 1 &mdash; Literature Survey

**Course:** CS4033E Computer Security | NIT Calicut  
**Topic:** SQL Injection-Based Authentication Bypass in a Self-Built Login Module with Parameterized Query Mitigation

---

## 1. Background and Historical Context

SQL injection (SQLi) is a class of attack where user-supplied input is interpreted as SQL command syntax rather than as plain data. This occurs when applications construct database queries by concatenating user input directly into SQL strings instead of using parameterized binding.

SQL injection was first publicly documented in 1998 by Jeff Forristal in Phrack Magazine, Issue 54. Despite being a known and well-documented vulnerability for over twenty-five years, it consistently appears in every edition of the OWASP Top 10 security risk list. In OWASP Top 10 2021, it is classified under **A03:2021 — Injection**, one of the three most critical web application security risks globally.

Its persistence is attributed to legacy codebases, developer unawareness, and insufficient code review practices that fail to catch unsafe query construction patterns.

---

## 2. OWASP Classification

**OWASP Top 10 2021 — A03: Injection**

OWASP (Open Web Application Security Project) publishes the globally recognized Top 10 list of critical web security risks. Injection flaws occur when user-supplied data is sent to an interpreter as part of a command, altering intended execution. SQL injection is the most prevalent and impactful example in this category.

Key OWASP guidance:
- Parameterized queries (prepared statements) are the **primary defense**
- Input validation is a secondary, supplementary control only
- Stored procedures, allow-lists, and LIMIT clauses provide additional protection

---

## 3. Types of SQL Injection

### 3.1 Classic (In-Band) SQLi
User input directly alters query logic and the effect is visible immediately in the application response. **This is the type demonstrated in this assignment** — authentication bypass is a classic in-band attack.

### 3.2 Error-Based SQLi
Database error messages are exposed to users and can leak schema details, table names, and column structures to the attacker.

### 3.3 Union-Based SQLi
Attacker appends a `UNION SELECT` clause to combine results and extract data from other tables. Requires knowledge of column count and data types.

### 3.4 Blind SQLi
No direct SQL output is visible. The attacker infers database behavior from application response differences (true/false branching conditions).

### 3.5 Time-Based Blind SQLi
Uses database timing functions (`SLEEP()` in MySQL, `pg_sleep()` in PostgreSQL) to infer conditions when output is completely suppressed.

---

## 4. Why Authentication Bypass Is Critical

Authentication is the first and primary security boundary in any multi-user system. If authentication is bypassed, an attacker gains access to protected functionality and data without possessing any valid credentials.

In insecure login implementations, the SQL query typically takes the form:

```sql
SELECT * FROM users WHERE username = '<input>' AND password = '<input>'
```

When user input is concatenated directly into this string, an attacker can supply:

```
username:  ' OR '1'='1' --
password:  anything
```

The resulting query becomes:

```sql
SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password = 'anything'
```

Token-by-token breakdown:

| Fragment | Effect |
|---|---|
| `username = ''` | Closes the username string early with empty value |
| `OR '1'='1'` | Attacker-injected always-true condition |
| `--` | SQL comment — everything after is ignored by the DB |
| `AND password = 'anything'` | Password check — now commented out, never evaluated |

Result: The WHERE clause reduces to `OR TRUE` = `TRUE`. The database returns the first row in the users table. The attacker is authenticated without knowing any valid password.

This exact behavior is demonstrated in Module A of this assignment.

---

## 5. Real-World Impact

SQL injection has caused some of the most consequential security breaches on record:

- **Heartland Payment Systems (2008):** SQL injection enabled theft of approximately 130 million credit and debit card records — one of the largest breach events in history at that time.
- **RockYou (2009):** SQL injection exposed 32 million user credentials that were stored in plaintext, enabling mass credential reuse attacks.
- **TalkTalk, UK (2015):** SQL injection on a UK telecom company exposed 157,000 customer records. The company received a regulatory fine of £400,000 from the Information Commissioner's Office.
- **BSNL India:** Multiple SQL injection incidents exposed customer data and internal systems across different incidents.

The common thread in all cases: developers concatenated user input into SQL queries without parameterized statements.

---

## 6. The Correct Mitigation: Parameterized Queries

Parameterized queries (also called prepared statements) enforce strict separation between SQL code structure and user-supplied data.

**How it works at the engine level:**
1. The application sends the query template with placeholder(s) to the database
2. The database engine tokenizes and compiles the query structure — execution plan is built and locked
3. User values are then bound to placeholder slots as typed data
4. Bound values are never seen by the SQL parser — they cannot alter SQL grammar
5. Injection payload is treated as a literal string to search for, not as SQL code

**Python sqlite3 example:**

```python
# Vulnerable — do not use
query = "SELECT * FROM users WHERE username = '" + username + "'"
cursor.execute(query)

# Secure — parameterized
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

The injection payload `' OR '1'='1' --` is treated as a 20-character literal string to search for. No user with that username exists, so login fails correctly.

---

## 7. Why Input Validation Alone Is Insufficient

Input validation (filtering `'`, `--`, `OR` etc.) is a useful secondary control but cannot replace parameterization as the primary defense:

- **Encoding attacks:** URL encoding (`%27` for `'`), Unicode normalization, or double encoding can bypass naive character filters
- **Second-order injection:** Input is stored cleanly, then retrieved and used in a different unprotected query later — validation at insert time does not protect the later query
- **Developer error:** Custom filters are custom code — they can have gaps, edge cases, or logic bugs

Parameterized queries work at the database driver layer and are not bypassable through input content manipulation.

---

## 8. Additional Defense Controls

While parameterized queries are the essential primary mitigation, a complete security posture adds:

| Control | Security Value |
|---|---|
| bcrypt password hashing | Protects credentials at rest if DB is stolen through another vector |
| Account lockout | Limits online brute-force guessing attempts |
| Audit logging | Provides traceability for incident detection and investigation |
| Least-privilege DB user | Limits damage scope if injection does occur |
| Generic error messages | Prevents user enumeration attacks |
| Input length limits | Reduces attack surface |

---

## 9. Relevance to This Assignment

This assignment directly implements all of the above:

1. **Module A** demonstrates the vulnerable flow with string-concatenated SQL
2. **Module B** implements the secure fix using parameterized query binding
3. **Module C** adds bcrypt hashing, account lockout, and audit logging
4. **Module D** provides a 17-row comparative test matrix with 11 evidence screenshots

---

## 10. References

1. OWASP Top 10 2021 — A03: Injection. https://owasp.org/Top10/A03_2021-Injection/
2. OWASP SQL Injection Prevention Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
3. Python sqlite3 Documentation — Parameterized Queries. https://docs.python.org/3/library/sqlite3.html
4. bcrypt library documentation. https://pypi.org/project/bcrypt/
5. W. Stallings, *Cryptography and Network Security — Principles and Practice*, 8/e, Pearson India, 2023.
6. D. Gollmann, *Computer Security*, 3/e, John Wiley and Sons Ltd., 2006.
7. Forristal, J. (1998). NT Web Technology Vulnerabilities. *Phrack Magazine*, Issue 54.
