# Step 19 &mdash; Marks-Critical Checklist

**Course:** CS4033E Computer Security | NIT Calicut  
**Assignment:** Security Attack Assignment (20 marks)

---

## Before Evaluation 1 (10 marks)

| Item | File | Status |
|---|---|---|
| Literature survey written | eval1/01_Literature_Survey.md | [x] Done |
| SQLi history, OWASP, types covered | eval1/01_Literature_Survey.md | [x] Done |
| Real breach details with specifics | eval1/01_Literature_Survey.md | [x] Done |
| SQL attack example shown | eval1/01_Literature_Survey.md | [x] Done |
| References with URLs | eval1/01_Literature_Survey.md | [x] Done |
| Revised specification prepared | eval1/02_Revised_Specification.md | [x] Done |
| Input/Output clearly defined | eval1/02_Revised_Specification.md Section 4 | [x] Done |
| Functional requirements listed | eval1/02_Revised_Specification.md | [x] Done |
| Architecture diagram drawn | eval1/03_Architecture_and_Dataflow.md | [x] Done |
| Step-by-step data flows documented | eval1/03_Architecture_and_Dataflow.md | [x] Done |
| DB schema documented | eval1/02_Revised_Specification.md | [x] Done |
| `python database.py` runs successfully | database.py | [x] Done |
| App starts on port 5000 | app.py | [x] Done |
| Vulnerable login works (normal creds) | auth_vulnerable.py | [x] Done |

---

## Before Evaluation 2 (10 marks)

| Item | File | Status |
|---|---|---|
| Vulnerable and secure in separate files | auth_vulnerable.py / auth_secure.py | [x] Done |
| Dangerous concatenation line annotated | auth_vulnerable.py | [x] Done |
| Parameterized query line annotated | auth_secure.py | [x] Done |
| T07: bypass on vulnerable, blocked on secure | Test evidence | [x] Done |
| T09: bypass on vulnerable, blocked on secure | Test evidence | [x] Done |
| T11: bypass on vulnerable, blocked on secure | Test evidence | [x] Done |
| bcrypt `$2b$` prefix visible in DB | users.db / ev11_bcrypt_hash.png | [x] Done |
| Lockout triggers after 5 failures | ev07_lockout.png | [x] Done |
| auth.log populates, no passwords | ev08_audit_log.png | [x] Done |
| 17-row test matrix complete | test_matrix_results_step11_17rows.md | [x] Done |
| All 11 evidence screenshots present | evidence/ folder | [x] Done |
| Report has all 13 sections | eval2/08_Final_Report_Draft.md | [x] Done |
| Ethical scope statement in report | eval2/08_Final_Report_Draft.md Section 4 | [x] Done |
| Technical explanation complete | 13_Technical_Explanation.md | [x] Done |
| Demo rehearsed twice | eval2/07_Rehearsal_Log.txt | [x] Done |

---

## Common Mistakes to Avoid

| Mistake | Guard |
|---|---|
| Only theory, no working code | App runs end-to-end from clean terminal |
| Input validation claimed as full mitigation | Report explicitly states it is secondary |
| Plaintext passwords stored | Secure module uses bcrypt only |
| Vulnerable and secure logic mixed | Completely separate files |
| No before/after evidence for same payload | T07/T08, T09/T10, T11/T12 pairs in matrix |
| No ethical scope statement | Section 4 of report covers this |
| Cannot explain own code | Rehearsed twice; can point to exact lines |
| No reference URLs | All 7 references have full URLs |

---

## Run Commands (Verified)

```bash
cd sql_injection_demo
pip install flask bcrypt
python database.py
python app.py
# Open http://localhost:5000
```
