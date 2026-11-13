# Evidence package (internal notes, not sent)

- **`package/`** (in git): the example reports in English and Ukrainian, as PDF and as HTML with their figures. The serial number is masked.
- **`dealer/`** (local only, git-ignored): the same PDFs with the full serial number. These are the copies to send to the dealer.

To regenerate:
- **Charts:** run `tools/make_charts.py <prometheus-url> <out-dir> [en|uk]` in a `python:3.12-slim` container.
- **Reports:** fill `{{SERIAL}}` in `tools/fault-report*.template.html` (the full serial for the dealer copies, a masked one for `package/`), then print to PDF with Edge headless.
- **Serial number:** taken from `ecoflow-monitor/.env`.
