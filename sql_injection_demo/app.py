"""Flask application entrypoint for the SQL injection demo project.

Security training demonstration only — local test environment.

Routes:
    GET  /             -> Home page (module selector)
    GET  /login_vuln   -> Vulnerable login form (Module A)
    POST /login_vuln   -> Vulnerable authentication (Module A)
    GET  /login_safe   -> Secure login form (Module B+C)
    POST /login_safe   -> Secure authentication with hardening (Module B+C)
"""

import os

from flask import Flask, render_template, request

try:
    # Package-style imports (works when run from workspace root).
    from .auth_secure import secure_login
    from .auth_vulnerable import vulnerable_login
except ImportError:
    # Script-style imports (works when run from project directory).
    from auth_secure import secure_login
    from auth_vulnerable import vulnerable_login

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", "sqli_demo_project_only")

# Maximum input length accepted before truncating (robustness guard)
MAX_INPUT_LEN = 200


@app.route("/")
def index():
    """Render the home page."""
    return render_template("index.html")


@app.route("/learn")
def learn():
    """Render educational SQL injection explanation page."""
    return render_template("learn.html")


@app.route("/login_vuln", methods=["GET", "POST"])
def login_vuln():
    """Module A: intentionally vulnerable login route using string-concatenated SQL."""
    if request.method == "GET":
        return render_template("login_vuln.html")

    username = request.form.get("username", "")[:MAX_INPUT_LEN]
    password = request.form.get("password", "")[:MAX_INPUT_LEN]

    user, query, error = vulnerable_login(username, password)

    # Detect if a successful login used injection-style input
    injection_indicators = ["'", "--", " OR ", " or ", "1=1"]
    is_attack = (user is not None) and any(
        ind in username for ind in injection_indicators
    )

    if user:
        return render_template(
            "success.html",
            username=user["username"],
            role=user["role"],
            query=query,
            mode="VULNERABLE",
            is_attack=is_attack,
        )

    return render_template(
        "fail.html",
        query=query,
        error=error,
        mode="VULNERABLE",
    )


@app.route("/login_safe", methods=["GET", "POST"])
def login_safe():
    """Module B+C: secure login route with parameterized query and hardening."""
    if request.method == "GET":
        return render_template("login_safe.html")

    username = request.form.get("username", "")[:MAX_INPUT_LEN]
    password = request.form.get("password", "")[:MAX_INPUT_LEN]
    source_ip = request.remote_addr or "unknown"

    # Show the parameterized template so readers can see the difference
    display_query = (
        "SELECT * FROM users WHERE username = ?  "
        f"-- value bound as literal data: ('{username}')"
    )

    user, message, success = secure_login(username, password, source_ip)

    if success:
        return render_template(
            "success.html",
            username=user["username"],
            role=user["role"],
            query=display_query,
            mode="SECURE",
            is_attack=False,
        )

    return render_template(
        "fail.html",
        query=display_query,
        error=message,
        mode="SECURE",
    )


if __name__ == "__main__":
    debug_enabled = os.getenv("FLASK_DEBUG", "0") in {"1", "true", "True"}
    port = int(os.getenv("PORT", "5000"))
    app.run(debug=debug_enabled, port=port)
