# Evaluation 2 &mdash; Rehearsal Checklist

**Course:** CS4033E Computer Security | NIT Calicut

---

## Pre-Rehearsal Setup

```bash
cd sql_injection_demo
python database.py          # reset to clean state
python app.py               # start on port 5000
# In second terminal:
tail -f auth.log            # watch events in real time
```

Confirm before starting:
- [ ] `http://localhost:5000` loads home page
- [ ] Both module cards visible
- [ ] Second terminal showing `tail -f auth.log`
- [ ] Code editor open at `auth_vulnerable.py` dangerous line
- [ ] Code editor open at `auth_secure.py` parameterized line
- [ ] Test matrix file open

---

## Rehearsal Run 1

**Problem statement (30&ndash;45 sec)**
- [ ] OWASP A03:2021 mentioned
- [ ] "Authentication bypass — no valid credentials needed" stated
- [ ] Two-flow architecture described

**Module A — Vulnerable demo**
- [ ] Normal login shown first (admin / adminpass123)
- [ ] Attack payload `' OR '1'='1' --` entered
- [ ] Bypass success page shown
- [ ] Query on page explained (OR true, -- comment)
- [ ] Second payload `admin'--` shown

**Module B+C — Secure demo**
- [ ] Same payload entered on secure side
- [ ] Fail page shown with mitigation banner
- [ ] Parameterized line in code pointed to
- [ ] Engine-level explanation given (compile first, bind after)
- [ ] Valid login `alice / alice2024` confirmed working

**Hardening**
- [ ] bcrypt hash shown in terminal (`$2b$` prefix)
- [ ] Lockout triggered by 5 wrong passwords
- [ ] `auth.log` entries shown

**Results**
- [ ] Test matrix shown (17/17)
- [ ] Takeaway delivered

**Timing**
- [ ] Total under 7 minutes

---

## Rehearsal Run 2

- [ ] Problem statement (30&ndash;45 sec)
- [ ] Vulnerable demo complete
- [ ] Secure demo complete
- [ ] Hardening demo complete
- [ ] Results shown
- [ ] Total under 7 minutes

---

## Quick Answer Bank (Know These Without Notes)

| Question | One-line answer |
|---|---|
| What does ? do? | DB compiles structure first; value bound as data after — parser never sees input |
| Why not just sanitize? | Encoding/unicode tricks bypass filters; parameterization is structural |
| Why bcrypt? | Random salt per hash; slow by design; rainbow tables defeated |
| Why lockout? | Throttles online brute-force against bcrypt hashes |
| Why logging? | Traceability for incident detection and forensic evidence |
| Why keep vulnerable code? | Controlled academic demo only; isolated file; never deployed |
| What proves mitigation? | Same 3 payloads: bypass vuln, blocked secure; valid login still works |
| What is user enumeration? | Inferring valid usernames from different error messages; prevented by generic message |
