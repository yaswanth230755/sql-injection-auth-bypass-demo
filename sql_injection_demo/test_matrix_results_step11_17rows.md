# Test Matrix Results &mdash; 17 Rows

**Course:** CS4033E Computer Security | NIT Calicut  
**Date executed:** 2026-04-06  
**Result: 17 / 17 PASSED**

---

| ID | Username Input | Password | Module | Expected Result | Actual Result | Pass/Fail | Key Point Proven | Evidence |
|---|---|---|---|---|---|---|---|---|
| T01 | admin | adminpass123 | Vulnerable | Login success | Login success | **PASS** | Normal flow works on vulnerable side | ev01_normal_vuln.png |
| T02 | admin | adminpass123 | Secure | Login success | Login success | **PASS** | Normal flow works on secure side | ev02_normal_secure.png |
| T03 | alice | wrongpass | Vulnerable | Login fail | Login fail | **PASS** | Wrong password rejected | &mdash; |
| T04 | alice | wrongpass | Secure | Login fail | Login fail | **PASS** | Wrong password rejected + logged | &mdash; |
| T05 | nobody | anything | Vulnerable | Login fail | Login fail | **PASS** | Unknown user rejected | &mdash; |
| T06 | nobody | anything | Secure | Login fail | Login fail | **PASS** | Unknown user rejected + logged | &mdash; |
| T07 | `' OR '1'='1' --` | anything | **Vulnerable** | **BYPASS SUCCEEDS** | **BYPASS SUCCEEDS** | **PASS** | Core tautology attack visible | ev03_attack_bypass.png |
| T08 | `' OR '1'='1' --` | anything | **Secure** | **BLOCKED** | **BLOCKED** | **PASS** | Core mitigation &mdash; payload bound as literal | ev04_attack_blocked.png |
| T09 | `admin'--` | anything | **Vulnerable** | **BYPASS SUCCEEDS** | **BYPASS SUCCEEDS** | **PASS** | Comment-truncation attack | ev05_comment_attack.png |
| T10 | `admin'--` | anything | **Secure** | **BLOCKED** | **BLOCKED** | **PASS** | Comment-truncation blocked | ev06_comment_blocked.png |
| T11 | `' OR 1=1--` | anything | **Vulnerable** | **BYPASS SUCCEEDS** | **BYPASS SUCCEEDS** | **PASS** | Alternate tautology attack | &mdash; |
| T12 | `' OR 1=1--` | anything | **Secure** | **BLOCKED** | **BLOCKED** | **PASS** | Alternate tautology blocked | &mdash; |
| T13 | alice | wrongpass &times;5 | Secure | Locked after 5th | Locked after 5th | **PASS** | Lockout triggers at threshold | ev07_lockout.png |
| T14 | alice | alice2024 | Secure (after T13) | Still locked | Still locked | **PASS** | Lockout holds even with correct password | &mdash; |
| T15 | (empty) | (empty) | Both | Fail gracefully | Vuln: Fail / Secure: Fail | **PASS** | Empty input handled without crash | &mdash; |
| T16 | 500-char string | anything | Both | Fail, no crash | Vuln: Fail / Secure: Fail | **PASS** | Long input robustness confirmed | &mdash; |
| T17 | &uuml;n&iuml;c&ouml;d&eacute; | anything | Both | Fail gracefully | Vuln: Fail / Secure: Fail | **PASS** | Unicode input handled without crash | &mdash; |

---

## Before / After Summary

| Input | Vulnerable Result | Secure Result |
|---|---|---|
| Valid credentials | Login success | Login success |
| Wrong password | Login fail | Login fail |
| `' OR '1'='1' --` | **BYPASS** | **BLOCKED** |
| `admin'--` | **BYPASS** | **BLOCKED** |
| `' OR 1=1--` | **BYPASS** | **BLOCKED** |
| 5&times; wrong password | No protection | Account locked 300s |
| Empty input | Fail gracefully | Fail gracefully |
| 500-char input | Fail, no crash | Fail, no crash |
| Unicode input | Fail gracefully | Fail gracefully |
