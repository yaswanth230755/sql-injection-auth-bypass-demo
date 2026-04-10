# Deployment Guide (Resume/Public Demo)

This project includes an intentionally vulnerable route for educational use.
Do not deploy it without clearly labeling it as a security demo.

## Option 1: Render (recommended)

1. Push this repository to GitHub.
2. Sign in to Render and choose New + Blueprint.
3. Select your repository.
4. Render will detect render.yaml and configure the service automatically.
5. Wait for deployment to finish.
6. Open the generated URL.

### Environment variables used

- APP_SECRET_KEY (auto-generated in render.yaml)
- FLASK_DEBUG=0

## Option 2: Railway/Heroku-style platforms

This repo includes a Procfile.

Use:
- Build command: pip install -r sql_injection_demo/requirements.txt
- Start command: Procfile entry will be used automatically

## Local production-like run

From repository root:

1. pip install -r sql_injection_demo/requirements.txt
2. python -m sql_injection_demo.bootstrap_db
3. gunicorn -b 0.0.0.0:8000 sql_injection_demo.app:app

## Resume note suggestion

"Built and deployed a security-focused Flask demo that contrasts vulnerable SQL login logic with parameterized-query mitigation, bcrypt hashing, lockout controls, and audit logging."
