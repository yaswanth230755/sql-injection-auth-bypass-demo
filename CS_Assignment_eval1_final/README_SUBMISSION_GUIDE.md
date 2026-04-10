# Evaluation 1 Submission Guide
## CS4033E Computer Security | NIT Calicut
## SQL Injection Authentication Bypass Assignment

---

## WHAT TO SUBMIT ON MOODLE

**One PDF file:** `AdimulamYaswanthVeeraNagesh_B230755CS.pdf`

This PDF must contain all 10 sections as specified by sir:
1. Title — Name with Roll Number
2. Abstract (max 250 words)
3. Introduction
4. Literature Survey (with comparison table)
5. System/Network Environment (hardware + software requirements)
6. Design of modules (with algorithms, input/output)
7. Progress of Implementation
8. Conclusion
9. References (IEEE format)
10. (Submitted via Moodle as AdimulamYaswanthVeeraNagesh_B230755CS.pdf)

**Source:** `Eval1_Report_AdimulamYaswanthVeeraNagesh_B230755CS.md` in this folder contains the complete report. Export it to PDF before submission.

---

## HOW TO EXPORT MD TO PDF

**Option 1 — Pandoc (recommended, best output):**
```bash
pandoc Eval1_Report_AdimulamYaswanthVeeraNagesh_B230755CS.md -o AdimulamYaswanthVeeraNagesh_B230755CS.pdf \
  --pdf-engine=wkhtmltopdf \
  --margin-top=25mm --margin-bottom=25mm \
  --margin-left=25mm --margin-right=25mm
```

**Option 2 — VS Code:**
Install "Markdown PDF" extension → right-click the .md file → Export (pdf)

**Option 3 — Browser:**
Open rendered Markdown preview → Ctrl+P → Save as PDF

---

## BEFORE SUBMITTING — CHECK THESE

- [ ] Your name and roll number on the title page
- [ ] Abstract is under 250 words
- [ ] Report is under 10 pages
- [ ] Literature Survey has the comparison table (Section 4)
- [ ] Section 5 has hardware AND software requirements
- [ ] Section 6 has algorithm pseudocode for each module
- [ ] References are in IEEE format [1], [2], [3]...
- [ ] Filename: `AdimulamYaswanthVeeraNagesh_B230755CS.pdf`
- [ ] Submitted on Moodle before 11 April 2026, 11:00 PM

---

## RUNNING THE IMPLEMENTATION (for demo evidence)

```bash
cd source_code
pip install flask bcrypt
python database.py
python app.py
# Open http://localhost:5000
```

Test payloads for Vulnerable Login:
- Username: `' OR '1'='1' --`  Password: anything
- Username: `admin'--`          Password: anything

Valid credentials:
- admin / adminpass123
- alice / alice2024
- bob / bobsecret

---

## DEADLINE

**11 April 2026 (Saturday) 11:00 PM — HARD DEADLINE**

No extensions. Submit well before the deadline.
