# Task 3.1 — HTML Report Generator

## Overview

Converts a structured JSON audit output (from `audit.py`) into a styled, self-contained HTML security report using Python and Jinja2 templating.


---

## Usage

```bash
python3 report_generator.py findings.json
```

**Output:** `results_<audit date>.html` — a self-contained HTML report written to the current directory.

---

## How It Works

### `report_generator.py`

1. **Argument Parsing** — Accepts a single positional argument: the path to a `.json` findings file.
2. **JSON Loading** — Opens and parses the findings file; exits with an error if the file is missing or not a `.json`.
3. **Jinja2 Rendering** — Loads `template.html` from the current directory, renders it with the JSON data and hostname, and writes the output HTML file.

### `template.html`

A dark-themed, responsive HTML/CSS report with the following sections:

- **Header** — Displays the audit date and hostname.
- **Summary Cards** — Shows total, high, medium, and low finding counts (computed via Jinja2 loops).
- **Finding Cards** — One collapsible card per finding, color-coded by severity (`HIGH` / `MEDIUM` / `LOW`), each showing:
  - Check name and severity badge
  - Description
  - Affected items table (any field prefixed with `"Affected"`)
- **Remediation Checklist** — A consolidated list of all recommendations across findings.
- **Footer** — Displays the audit date.
---

## Acceptance Criteria

- [x] Takes a JSON file as input: `python3 report_generator.py findings.json`
- [x] Outputs `results_<audit date>.html`
- [x] Report is self-contained (no external CSS or JS dependencies)
- [x] Gracefully handles missing or invalid files with an informative error message

---
## Dependencies

```bash
pip3 install jinja2
```
**or**
```bash
sudo apt install python3-jinja2 -y
```