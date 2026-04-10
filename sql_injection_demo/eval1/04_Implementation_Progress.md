# Evaluation 1 &mdash; Implementation Progress

**Course:** CS4033E Computer Security | NIT Calicut

---

## Status: ALL STEPS COMPLETE

| Step | Task | Status |
|---|---|---|
| 1 | Scope lock finalized | ✓ Complete |
| 2 | Dependencies installed (flask, bcrypt) | ✓ Complete |
| 3 | Full project structure created | ✓ Complete |
| 4 | database.py — DB init and seed script | ✓ Complete |
| 5 | auth_vulnerable.py — Module A | ✓ Complete |
| 6 | auth_secure.py — Module B+C | ✓ Complete |
| 7 | logger.py — audit logging | ✓ Complete |
| 8 | app.py — Flask routes | ✓ Complete |
| 9 | All 5 HTML templates | ✓ Complete |
| 10 | Application verified running at localhost:5000 | ✓ Complete |
| 11 | 17-row test matrix executed — 17/17 passed | ✓ Complete |
| 12 | Evidence screenshots captured (11 files) | ✓ Complete |
| 13 | Technical explanation document prepared | ✓ Complete |

---

## How to Run (Verified Commands)

```bash
# From the sql_injection_demo directory:

# 1. Install dependencies
pip install flask bcrypt

# 2. Initialize database (run once; safe to re-run)
python database.py

# 3. Start application
python app.py

# 4. Open browser
http://localhost:5000
```

---

## Key Artifacts Produced

| Artifact | Location |
|---|---|
| All source code | `sql_injection_demo/*.py` |
| HTML templates | `sql_injection_demo/templates/` |
| Test matrix (17 rows) | `sql_injection_demo/test_matrix_results_step11_17rows.md` |
| Evidence screenshots | `sql_injection_demo/evidence/ev01_*.png` to `ev11_*.png` |
| Technical explanation | `sql_injection_demo/13_Technical_Explanation.md` |
| Audit log (live run) | `sql_injection_demo/auth.log` |

---

## Eval 1 Criteria — All Satisfied

| Criterion | Delivered By |
|---|---|
| Literature Survey | `eval1/01_Literature_Survey.md` |
| Revised/Final Specification and Design | `eval1/02_Revised_Specification.md` |
| Clarity on Input/Output | Section 4 of Revised Specification |
| Progress of Implementation | This document + running application |
