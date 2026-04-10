# Ready to Submit Checklist

**Course:** CS4033E Computer Security | NIT Calicut  
**Status: READY**

---

## Source Code

- [x] source_code/app.py
- [x] source_code/auth_vulnerable.py
- [x] source_code/auth_secure.py
- [x] source_code/database.py
- [x] source_code/logger.py
- [x] source_code/requirements.txt
- [x] source_code/templates/index.html
- [x] source_code/templates/login_vuln.html
- [x] source_code/templates/login_safe.html
- [x] source_code/templates/success.html
- [x] source_code/templates/fail.html

## Documentation

- [x] setup_instructions.txt
- [x] run_demo.txt
- [x] requirements.txt (root copy)

## Report and Test Matrix

- [x] report.pdf (export of eval2/08_Final_Report_Draft.md)
- [x] test_matrix.pdf (export of test_matrix_results_step11_17rows.md)

## Evidence

- [x] evidence/ev01_normal_vuln.png
- [x] evidence/ev02_normal_secure.png
- [x] evidence/ev03_attack_bypass.png
- [x] evidence/ev04_attack_blocked.png
- [x] evidence/ev05_comment_attack.png
- [x] evidence/ev06_comment_blocked.png
- [x] evidence/ev07_lockout.png
- [x] evidence/ev08_audit_log.png
- [x] evidence/ev09_code_vuln.png
- [x] evidence/ev10_code_secure.png
- [x] evidence/ev11_bcrypt_hash.png

---

## Final Verification Commands

```bash
cd source_code
pip install flask bcrypt
python database.py          # must print 3 test users
python app.py               # must start on port 5000
```

Browser checks:
1. Home page loads with both module cards
2. Vulnerable login: `' OR '1'='1' --` bypasses
3. Secure login: same payload blocked
4. Secure login: 5 failures trigger lockout
5. `cat auth.log` shows events, no passwords

---

## Note on PDF Files

`report.pdf` and `test_matrix.pdf` are PDF exports of:
- `../sql_injection_demo/eval2/08_Final_Report_Draft.md`
- `../sql_injection_demo/test_matrix_results_step11_17rows.md`

If you need to regenerate them, open each `.md` file and export to PDF via:
- Pandoc: `pandoc 08_Final_Report_Draft.md -o report.pdf`
- VS Code: Markdown PDF extension
- Browser: Open rendered preview and print to PDF
