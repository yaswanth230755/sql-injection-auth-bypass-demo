# Final Readiness Check

**Course:** CS4033E Computer Security | NIT Calicut

---

## Night-Before-Demo Verification

Run these in order and confirm each:

```bash
cd sql_injection_demo
pip install flask bcrypt
python database.py          # must print all 3 users
python app.py               # must start on port 5000
```

In browser:
1. `http://localhost:5000` loads home page &mdash; both cards visible
2. Vulnerable login &rarr; `admin / adminpass123` &rarr; success
3. Vulnerable login &rarr; `' OR '1'='1' --` / anything &rarr; BYPASS shown
4. Secure login &rarr; same payload &rarr; BLOCKED shown
5. Secure login &rarr; fail 5 times &rarr; lockout message appears
6. `cat auth.log` &rarr; events visible, no passwords in file

All 6 must pass. If all pass: ready.

---

## Full Readiness Checklist

### Code
- [x] App runs from clean terminal with two install commands
- [x] Vulnerable and secure logic in separate files, clearly labelled
- [x] Dangerous concatenation line visible in auth_vulnerable.py
- [x] Parameterized query line visible in auth_secure.py
- [x] T07 bypass succeeds on vulnerable, blocked on secure
- [x] bcrypt `$2b$` prefix visible in users.db password_hash column
- [x] Lockout triggers after exactly 5 failures
- [x] auth.log populates on every login attempt
- [x] No raw passwords in auth.log
- [x] Empty, long, and unicode inputs handled without crash

### Documentation
- [x] Report has all 13 sections including ethical scope statement
- [x] Literature survey has SQL examples, breach details, reference URLs
- [x] Test matrix: 17 rows, all PASS, evidence filenames linked
- [x] Technical explanation covers 5-step binding mechanism
- [x] Demo script has 7-minute structure and all Q&A answers

### Evidence
- [x] 11 evidence screenshots in evidence/ folder
- [x] Screenshots named ev01 through ev11
- [x] Each screenshot matches its label in the test matrix

### Demo
- [x] Demo rehearsed twice &mdash; see 07_Rehearsal_Log.txt
- [x] Can point to exact dangerous line without searching
- [x] Can point to exact fix line without searching
- [x] Can explain ? binding in own words without notes
- [x] Can answer all 8 common viva questions

---

## Port Conflict Resolution

If port 5000 is in use:

```bash
PORT=5001 python app.py
# Then open http://localhost:5001
```
