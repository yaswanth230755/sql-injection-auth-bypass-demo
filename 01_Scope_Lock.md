# STEP 1 — SCOPE LOCK

**Course:** CS4033E Computer Security | NIT Calicut

---

## Topic

SQL Injection-Based Authentication Bypass in a Self-Built Login Module with Parameterized Query Mitigation

---

## Final Objective Statement

I am building a login system from scratch with two flows: an intentionally vulnerable module using string-concatenated SQL to demonstrate authentication bypass in a controlled lab, and a secure module using parameterized queries as the primary mitigation, supplemented by bcrypt password hashing, account lockout, and audit logging, with a comparative test matrix as evidence.

---

## Fixed Implementation Modules

| Module | Name | What It Proves |
|---|---|---|
| A | Vulnerable Login | Unsafe SQL construction allows authentication bypass |
| B | Secure Login | Parameterized query blocks the same bypass payload |
| C | Hardening | bcrypt + lockout + logging provide defense-in-depth |
| D | Evaluation | Test matrix + screenshots provide reproducible evidence |

---

## Scope Constraints

- Local machine only
- Test database and test users only
- No testing on public, live, or third-party systems
- Vulnerable module exists only for controlled academic demonstration

---

## Assignment Completion Criteria

The assignment is complete only when all four are true:

1. Vulnerable path shows bypass under crafted SQL payload
2. Secure path blocks the exact same payload
3. Normal valid login still works correctly on secure path
4. Results are documented with test matrix and screenshot evidence

---

## Eval Mapping

### Eval 1 (10 marks)
- Literature survey
- Revised specification and design
- Clarity on input/output
- Progress of implementation

### Eval 2 (10 marks)
- Technical explanation
- Implementation and demonstration
- Report submission

---

## Inputs and Outputs

### Inputs
- Username (string)
- Password (string)
- Route selection: `/login_vuln` (Module A) or `/login_safe` (Module B+C)

### Outputs
- Login success/failure result page
- Mode label (VULNERABLE or SECURE)
- SQL query display (exact query for Module A, parameterized template for Module B)
- Attack/mitigation banners on result pages
- Audit log entries (Module B+C only)
