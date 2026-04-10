# Evaluation 1 &mdash; Revised / Final Specification and Design

**Course:** CS4033E Computer Security | NIT Calicut  
**Topic:** SQL Injection-Based Authentication Bypass in a Self-Built Login Module with Parameterized Query Mitigation

---

## 1. Objective Statement

Build a self-coded login system from scratch with two authentication flows: an intentionally vulnerable flow using string-concatenated SQL for controlled SQL injection demonstration, and a secure flow using parameterized queries as the primary mitigation, supplemented by bcrypt password hashing, account lockout, and audit logging. A comparative test matrix documents before/after behavior under identical inputs.

---

## 2. Fixed Implementation Modules

| Module | Name | Core Technique | Purpose |
|---|---|---|---|
| A | Vulnerable Login | String-concatenated SQL | Demonstrate authentication bypass risk |
| B | Secure Login | Parameterized query (? placeholder) | Demonstrate prevention at DB execution layer |
| C | Hardening | bcrypt + account lockout + audit logging | Demonstrate defense-in-depth |
| D | Evaluation | 17-row test matrix + 11 evidence screenshots | Prove reproducible before/after results |

---

## 3. Scope Constraints

- Local machine only
- Test database and test users only (admin, alice, bob)
- No testing on public, live, or third-party systems
- Vulnerable module is isolated in a separate file, clearly labelled, for academic demonstration only
- Application runs on Flask development server — not a production deployment

---

## 4. Input / Output Definition

### 4.1 Inputs

| Input | Type | Description |
|---|---|---|
| username | String (max 200 chars) | Entered by user in login form |
| password | String (max 200 chars) | Entered by user in login form |
| route | URL path | `/login_vuln` selects Module A; `/login_safe` selects Module B+C |

### 4.2 Outputs

| Output | Description |
|---|---|
| Login result page | Shows success or failure with module mode label |
| SQL query display | Exact constructed query (Module A) or parameterized template (Module B) |
| Attack banner | Shown on success page when injection payload detected in Module A |
| Mitigation banner | Shown on fail page when secure mode blocks a payload |
| Lockout message | Shows remaining lock time when account is locked (Module B+C) |
| auth.log entries | Timestamped event records written on every authentication attempt |
| audit_log table | Same events stored in structured SQLite table |

---

## 5. Functional Requirements

| ID | Requirement |
|---|---|
| FR1 | Home page provides navigation to both vulnerable and secure login routes |
| FR2 | Vulnerable route builds SQL query by direct string concatenation of username and password |
| FR3 | Vulnerable route displays the constructed SQL query in the result page |
| FR4 | Secure route uses parameterized placeholder binding exclusively |
| FR5 | Secure route verifies passwords using bcrypt hash comparison |
| FR6 | Secure route increments failed_attempts on each wrong password |
| FR7 | Secure route locks account for 300 seconds after 5 consecutive failures |
| FR8 | Secure route logs every authentication event to auth.log and audit_log table |
| FR9 | Secure route returns generic "Invalid credentials." — never exposes raw SQL errors |
| FR10 | Database is resettable to a clean known state by running database.py |

---

## 6. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR1 | Vulnerable and secure logic must be in separate Python files |
| NFR2 | All result pages must show which module mode is active |
| NFR3 | Application must handle empty, long (500+ char), and unicode inputs without crashing |
| NFR4 | Demonstration must be reproducible from a clean database state |

---

## 7. Technology Stack

| Component | Choice | Reason |
|---|---|---|
| Backend | Python + Flask | Minimal framework; all logic written from scratch |
| Database | SQLite (built-in) | Zero installation, portable, raw SQL visible |
| Password hashing | bcrypt | Industry standard, built-in salt, tunable cost factor |
| Frontend | Plain HTML + CSS | No external frameworks; all code written manually |

No ORM is used intentionally — raw SQL queries must be visible to demonstrate the vulnerability and fix clearly.

---

## 8. Database Schema

### users table

| Column | Type | Notes |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| username | TEXT UNIQUE | Login identifier |
| password_plain | TEXT | Vulnerable module only — simulates naive developer mistake |
| password_hash | TEXT | bcrypt hash — secure module only |
| role | TEXT | 'administrator' or 'user' |
| failed_attempts | INTEGER | Lockout failure counter, default 0 |
| lock_until | REAL | Unix timestamp of lockout expiry; NULL = not locked |

### audit_log table

| Column | Type | Notes |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| timestamp | TEXT | YYYY-MM-DD HH:MM:SS |
| username | TEXT | Username involved in event |
| event | TEXT | Event label |
| source | TEXT | Source IP address |

---

## 9. Acceptance Criteria

All five must be true for the assignment to be considered complete:

1. Crafted SQL injection payloads bypass the vulnerable login flow in controlled test
2. The same payloads are blocked in the secure login flow
3. Valid credentials authenticate correctly in the secure flow
4. Account lockout triggers after 5 failed attempts and holds correctly
5. All 17 test cases are documented with expected and actual results
