# Step 17 &mdash; 7-Day Execution Tracking

**Course:** CS4033E Computer Security | NIT Calicut

---

## Plan vs Completion

| Day | Planned Work | Status |
|---|---|---|
| Day 1 | Environment setup, database script, literature notes | Complete |
| Day 2 | Vulnerable module and baseline route checks | Complete |
| Day 3 | Secure module and mitigation verification | Complete |
| Day 4 | Hardening controls (bcrypt, lockout, logging) | Complete |
| Day 5 | Full test matrix execution and evidence capture | Complete |
| Day 6 | Full report draft preparation | Complete |
| Day 7 | Rehearsal runs and final readiness checks | Complete |

---

## All Artifacts Produced

| Artifact | Location |
|---|---|
| Scope lock | `01_Scope_Lock.md` |
| Source code | `sql_injection_demo/*.py` |
| HTML templates | `sql_injection_demo/templates/*.html` |
| Test matrix (17 rows) | `sql_injection_demo/test_matrix_results_step11_17rows.md` |
| Evidence screenshots (11) | `sql_injection_demo/evidence/ev01_*.png` &mdash; `ev11_*.png` |
| Eval 1 package | `sql_injection_demo/eval1/*.md` |
| Eval 2 package | `sql_injection_demo/eval2/*.md` |
| Technical explanation | `sql_injection_demo/13_Technical_Explanation.md` |
| Submission package | `submission_package/` |

---

## Rehearsal Status

| Run | Date | Status |
|---|---|---|
| Rehearsal 1 | 2026-04-06 | PASS |
| Rehearsal 2 | 2026-04-06 | PASS |

Log: `sql_injection_demo/eval2/07_Rehearsal_Log.txt`

---

## Clean-Run Verification Record

**Date:** 2026-04-06

Commands verified:

```bash
cd sql_injection_demo
pip install flask bcrypt
python database.py      # prints all 3 test users
python app.py           # starts on port 5000
```

Route checks confirmed:
- `GET /` &rarr; HTML returned
- `GET /login_vuln` &rarr; HTML returned
- `GET /login_safe` &rarr; HTML returned

**Run note:** Always run from inside the `sql_injection_demo` directory using `python app.py` for clean script-style imports. Package-style execution from workspace root also supported via `__init__.py`.
