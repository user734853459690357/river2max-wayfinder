# What goes in the warranty evidence package

Type: prototype
Status: resolved
Blocked by: 10

## Question

Draft the complete warranty evidence package for the user to react to and approve, per [Calibrate first or claim the warranty now](10-calibrate-or-claim.md) and [What the Test Cycle data says about the cause](09-diagnose-from-data.md).

**Contents:**
- the **Fault report**, a factual owner's technical report. It must not mention AI, assistants or tooling.
- the four PNG charts generated from Prometheus
- the key numbers
- a list of the app screenshots the user must capture: limits at 0–100%, firmware, cycles
- a decision on whether a Cutout / Rebound / Collapse to zero video is worth recording

**The report must cover:**
- the symptom history, including 5+ calibration cycles with no improvement
- the Test Cycle method and results
- Usable capacity of about 11 Ah against the 20 Ah design and the "80%+ after 3000 cycles" spec
- that a low-capacity cell is suspected

**Formats:** a printable version for the box and an email version for the dealer.

Resolved when the user has reviewed and approved the package. That approved package is the hand-off: the user ships the unit.

## Comments

- **Draft package built, 2026-11-12. Awaiting the user's review.**
  - Assets: [evidence/package/](../evidence/package/) contains `fault-report.pdf` (6 pages), `fault-report.html`, figures 1–5 and `email-to-dealer.txt`.
  - Review notes, placeholders and the screenshot/video checklist: [evidence/REVIEW.md](../evidence/REVIEW.md).
  - Generator: [evidence/tools/](../evidence/tools/).
  - The report is written in the owner's voice, contains only data, and has no mention of AI or tooling.
- **Revised, 2026-11-13, at the user's direction: the deliverable is the report only.**
  - The email text was removed.
  - All blank or fill-in fields (dealer, purchase, owner) and the "Request" section were removed.
  - [evidence/package/fault-report.pdf](../evidence/package/fault-report.pdf) is a complete diagnosis report, ready to send as it is.
  - Screenshots and video are not part of the package.
- **2026-11-13: Ukrainian copy added, and the serial is split for the public repo.**
  - Added: `fault-report-uk.pdf` with Ukrainian figures.
  - `package/` (committed) holds the reports with the serial masked.
  - The dealer copies with the full serial are in `evidence/dealer/`, which is git-ignored.

## Answer

**Approved by the user, 2026-11-13. The package is the Fault report alone: a finished diagnosis report, ready to send.**

- **Contents:**
  - symptoms, steps already taken, test method and timeline, results, assessment ("defective cell suspected"; "not consistent with normal wear")
  - 5 figures
  - no email draft, no fill-in fields, no request section
- **Languages:** English and Ukrainian (the Ukrainian copy is for the dealer). Both versions have their own chart labels.
- **Files:**
  - [evidence/package/](../evidence/package/) is in the public repo. It holds the PDF and HTML for both languages, with the serial masked.
  - `evidence/dealer/` is git-ignored. It holds the PDFs with the full serial; these are the copies to send.
  - [evidence/tools/](../evidence/tools/) holds the generator: report templates and `make_charts.py`.
- **Hand-off:** the user sends the dealer copy and ships the unit to the dealer.
