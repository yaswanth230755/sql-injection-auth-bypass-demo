# Step 11 Test Matrix Results

| ID | Username | Password | Module | Expected | Actual | Pass/Fail | Key point proven |
|---|---|---|---|---|---|---|---|
| T01 | admin | adminpass123 | Vulnerable | Success | Success | Pass | Normal flow works |
| T02 | admin | adminpass123 | Secure | Success | Success | Pass | Normal flow works |
| T03 | alice | wrongpass | Vulnerable | Fail | Fail | Pass | Wrong password rejected |
| T04 | alice | wrongpass | Secure | Fail | Fail | Pass | Wrong password rejected |
| T05 | nobody | anything | Vulnerable | Fail | Fail | Pass | Unknown user rejected |
| T06 | nobody | anything | Secure | Fail | Fail | Pass | Unknown user rejected |
| T07 | ' OR '1'='1' -- | anything | Vulnerable | BYPASS SUCCEEDS | BYPASS SUCCEEDS | Pass | Core attack visible |
| T08 | ' OR '1'='1' -- | anything | Secure | BLOCKED | BLOCKED | Pass | Core mitigation visible |
| T09 | admin'-- | anything | Vulnerable | BYPASS SUCCEEDS | BYPASS SUCCEEDS | Pass | Comment truncation attack |
| T10 | admin'-- | anything | Secure | BLOCKED | BLOCKED | Pass | Comment truncation blocked |
| T11 | ' OR 1=1-- | anything | Vulnerable | BYPASS SUCCEEDS | BYPASS SUCCEEDS | Pass | Tautology attack |
| T12 | ' OR 1=1-- | anything | Secure | BLOCKED | BLOCKED | Pass | Tautology blocked |
| T13 | alice | wrongpass x5 | Secure | Locked after 5th | Locked after 5th | Pass | Lockout triggers |
| T14 | alice | alice2024 | Secure | Locked | Locked | Pass | Lockout holds |
| T15 |  |  | Vulnerable | Fail | Fail | Pass | Empty input handled |
| T15b |  |  | Secure | Fail | Fail | Pass | Empty input handled |
| T16 | AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA | anything | Vulnerable | Fail | Fail | Pass | Long input robust |
| T16b | AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA | anything | Secure | Fail | Fail | Pass | Long input robust |
| T17 | unicoode_test | anything | Vulnerable | Fail | Fail | Pass | Unicode/special handled |
| T17b | unicoode_test | anything | Secure | Fail | Fail | Pass | Unicode/special handled |