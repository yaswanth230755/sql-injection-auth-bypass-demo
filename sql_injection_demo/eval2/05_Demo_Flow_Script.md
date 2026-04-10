# Evaluation 2 &mdash; Demo Flow Script (5&ndash;7 Minutes)

**Course:** CS4033E Computer Security | NIT Calicut

---

## Pre-Demo Setup (Do Before Entering Room)

```bash
cd sql_injection_demo

# Reset DB to clean known state
python database.py

# Start app
python app.py

# In a second terminal — watch logs in real time
tail -f auth.log
```

Have these open and ready:
- Browser at `http://localhost:5000`
- Terminal with `tail -f auth.log` running
- Code editor open at `auth_vulnerable.py` (the dangerous line)
- Code editor open at `auth_secure.py` (the parameterized line)
- Test matrix file open

---

## Minute 1 &mdash; Problem Statement (30&ndash;45 seconds)

Say this:

> "SQL injection is ranked under OWASP A03:2021 — Injection, one of the three most critical web security risks globally. Authentication bypass is the most impactful form: an attacker logs in without any valid credentials by injecting SQL syntax through a normal input field. I built this system from scratch in Python and Flask with two authentication flows — a vulnerable one to demonstrate the attack, and a secure one to demonstrate the mitigation using parameterized queries."

Show: the home page with the two module cards.

---

## Minutes 2&ndash;3 &mdash; Module A: Vulnerable Login

**Step 1:** Click "Vulnerable Login."

**Step 2:** Show normal flow first.
- Username: `admin` / Password: `adminpass123` → Submit
- Show success page. "Normal login works."

**Step 3:** Click Back. Now the attack.

Enter:
- Username: `' OR '1'='1' --`
- Password: `hello`
- Submit

**Step 4:** Show attack success page. Point to:
- Red banner: "ATTACK SUCCESSFUL — AUTHENTICATION BYPASSED"
- The SQL query displayed on the page

Say this:
> "Look at the query the database actually executed. The single quote closes the username string early. OR '1'='1' is always true — the WHERE clause is always satisfied. The double dash comments out everything after, including the password check. The database returned the first row — admin — without any valid password."

**Step 5:** Try second payload `admin'--` to reinforce the point.

---

## Minutes 4&ndash;5 &mdash; Module B+C: Secure Login

**Step 1:** Return to home. Click "Secure Login."

**Step 2:** Enter the exact same attack payload:
- Username: `' OR '1'='1' --`
- Password: `hello`
- Submit

**Step 3:** Show the fail page. Point to:
- Green mitigation banner
- Parameterized query template: `SELECT * FROM users WHERE username = ?  -- value bound as literal data`

Say this:
> "Same payload — completely blocked. Here is why."

**Step 4:** Open `auth_secure.py`. Point to:
```python
c.execute("SELECT * FROM users WHERE username = ?", (username,))
```

Say this:
> "The question mark is a placeholder. The database receives this template and compiles the query structure — parsing is complete before any user value arrives. The value is then bound as typed data. The injection payload is treated as a 20-character literal string to search for. No user with that username exists. Login fails correctly. The parser never sees the input."

**Step 5:** Confirm valid login still works:
- Username: `alice` / Password: `alice2024` → Success

---

## Minute 6 &mdash; Hardening Features

**bcrypt:**
```bash
python3 -c "import sqlite3; c=sqlite3.connect('users.db').cursor(); c.execute('SELECT username, password_hash FROM users'); print(c.fetchall())"
```
Point to `$2b$` prefix: "Passwords never stored as plaintext. bcrypt salt means same password produces different hash each time — rainbow tables fail."

**Lockout:**
- Fail login as `alice` 5 times on secure side
- Show lockout message with remaining seconds
- "Brute-force attempts are throttled."

**Logging:**
- Show `auth.log` output in second terminal
- "Every event logged — timestamp, username, event type. No passwords in logs."

---

## Minute 7 &mdash; Results and Takeaway

Show test matrix:
- T07, T09, T11: three different payloads — all bypassed on vulnerable, all blocked on secure
- T13, T14: lockout confirmed
- 17 total, 17 passed

Say this:
> "Parameterized queries enforce separation of SQL code from user data at the database execution layer. Input filtering can be bypassed. Parameterization cannot — structure is already compiled when input arrives."

---

## Likely Viva Questions and Answers

**Q: What does the ? placeholder do exactly?**  
A: The DB engine receives the query template and builds an execution plan. Structure is compiled and locked. Then the driver binds the value bytes to the placeholder as a typed literal. The value is never seen by the SQL parser. It cannot alter grammar regardless of content.

**Q: Why not just sanitize/filter input?**  
A: Validation is application-layer code. URL encoding, Unicode normalization, or second-order injection can bypass it. Parameterization works at the execution layer — structurally impossible to bypass.

**Q: Why keep vulnerable code at all?**  
A: Controlled academic demonstration in local test environment only. Isolated in a separate file, clearly labelled, never deployed.

**Q: Why bcrypt specifically?**  
A: bcrypt is intentionally slow and includes a random salt per hash. Same password produces a different hash every time. Defeating rainbow tables. Cost factor can be tuned as hardware improves.

**Q: What other mitigations exist?**  
A: Least-privilege DB user, generic error messages, input length limits, WAF, MFA, CAPTCHA, SIEM logging.

**Q: What is user enumeration?**  
A: If the app says "username not found" vs "wrong password," an attacker learns which usernames are valid. The secure module always returns "Invalid credentials." regardless — preventing enumeration.

**Q: What proves mitigation in this project?**  
A: Same three payloads (T07, T09, T11) that bypass vulnerable authentication are all blocked by secure authentication, while valid credentials (T02) still work.
