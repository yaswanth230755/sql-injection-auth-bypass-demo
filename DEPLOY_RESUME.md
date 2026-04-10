# Deployment And Resume Notes

This project is a security-focused Flask demo that contrasts vulnerable SQL-based authentication logic with secure, parameterized-query handling.

## Live Demo

- https://sql-injection-demo-jgb2.onrender.com

## Resume-Ready Highlights

- Built and deployed a Flask security demo showing SQL injection authentication bypass versus parameterized-query mitigation.
- Implemented password hardening and account-protection controls using bcrypt, lockout behavior, and audit logging.
- Designed side-by-side vulnerable and secure login flows to clearly demonstrate exploitability and remediation.
- Deployed on Render with production process management using Gunicorn and automated database bootstrap.
- Validated production-like behavior locally before deployment using Gunicorn startup and SQLite initialization.

## Deployment (Render Recommended)

1. Push the repository to GitHub.
2. In Render, choose New + Blueprint and connect the repository.
3. Render reads render.yaml for build and start commands.
4. Wait for deployment to complete, then open the generated URL.

Environment variables:

- APP_SECRET_KEY (auto-generated)
- FLASK_DEBUG=0

## Alternative Platforms (Railway Or Heroku-Style)

This repository includes a Procfile.

- Build command: pip install -r sql_injection_demo/requirements.txt
- Start command: use the Procfile web entry

## Local Production-Like Verification

Run from repository root:

1. python -m venv .venv
2. source .venv/bin/activate
3. pip install -r sql_injection_demo/requirements.txt
4. python -m sql_injection_demo.bootstrap_db
5. gunicorn -b 0.0.0.0:8000 sql_injection_demo.app:app

## Notes

- This repository intentionally contains a vulnerable route for educational demonstration.
- Keep the demo clearly labeled as non-production training content.
