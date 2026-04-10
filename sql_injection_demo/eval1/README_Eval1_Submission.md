# Eval 1 Submission Pack

**Course:** CS4033E Computer Security | NIT Calicut  
**Topic:** SQL Injection-Based Authentication Bypass in a Self-Built Login Module with Parameterized Query Mitigation

---

## Contents of This Folder

| File | Covers |
|---|---|
| `01_Literature_Survey.md` | History, OWASP, types, real breaches, SQL examples, references |
| `02_Revised_Specification.md` | Objective, modules, I/O, functional requirements, DB schema |
| `03_Architecture_and_Dataflow.md` | Diagrams, route behavior, step-by-step data flows |
| `04_Implementation_Progress.md` | All 13 steps complete, run commands, artifact list |

---

## Related Artifacts (Outside This Folder)

| Artifact | Location |
|---|---|
| Test matrix results | `../test_matrix_results_step11_17rows.md` |
| Evidence screenshots | `../evidence/ev01_*.png` through `ev11_*.png` |
| Technical explanation | `../13_Technical_Explanation.md` |
| Source code | `../app.py`, `../auth_vulnerable.py`, `../auth_secure.py` etc. |

---

## How to Run Implementation Evidence

```bash
cd sql_injection_demo
pip install flask bcrypt
python database.py
python app.py
# Open http://localhost:5000
```

---

## Note on PDF Export

If sir requires PDF format for submission, export each `.md` file to PDF using any Markdown-to-PDF tool (e.g. Pandoc, VS Code Markdown PDF extension, or browser print-to-PDF from rendered preview) in the order listed above.
