# sql-injection-auth-bypass-demo

Security-focused Flask demo that contrasts an intentionally vulnerable login flow against a secure, parameterized-query flow.

## Live Demo

- https://sql-injection-demo-jgb2.onrender.com

## Highlights

- Module A (vulnerable): SQL string concatenation to demonstrate authentication bypass
- Module B (secure): parameterized query binding to block SQL injection
- Module C (hardening): bcrypt password hashing, account lockout, and audit logging
- Includes side-by-side UI routes for manual testing

## Tech Stack

- Python
- Flask
- SQLite
- bcrypt
- Gunicorn

## Quick Start (Local)

```bash
# Skip clone if you already have the repository
git clone https://github.com/yaswanth230755/sql-injection-auth-bypass-demo.git
cd sql-injection-auth-bypass-demo
python -m venv .venv
source .venv/bin/activate
pip install -r sql_injection_demo/requirements.txt
python -m sql_injection_demo.bootstrap_db
python sql_injection_demo/app.py
```

Run commands from the repository root (`sql-injection-auth-bypass-demo`) so relative paths resolve correctly.

Open:

- http://127.0.0.1:5000/
- Vulnerable route: `/login_vuln`
- Secure route: `/login_safe`

## Test Payloads (Demo)

Use these on the vulnerable route to observe bypass behavior:

- Username: `' OR '1'='1' --` | Password: `anything`
- Username: `admin'--` | Password: `anything`
- Username: `' OR 1=1--` | Password: `anything`

Try the same payloads on `/login_safe` to see mitigation in action.

## Deploy

For deployment options and platform-specific setup, see DEPLOY_RESUME.md.

## Security Notice

This project contains an intentionally vulnerable route for educational demonstration only. Do not use this code pattern in production systems.
