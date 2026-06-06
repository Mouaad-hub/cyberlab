# Task 3.2 — Scheduled Audit + Diff Report

## Overview

This task automates the full security audit pipeline via a cron job. Each day, it runs the audit, compares results against the previous day's findings, and generates an HTML report highlighting what's new and what's been resolved.

## Files

| File | Description |
|---|---|
| `run_audit.sh` | Orchestrator script — runs the full pipeline in order |
| `diff_reports.py` | Compares today's findings against yesterday's and outputs a diff JSON |
| `report_generater.py` | Renders the HTML report from findings and diff data using Jinja2 |
| `template.html` | Jinja2 HTML template for the styled report |

## Pipeline

```
run_audit.sh
 └─> audit.py                → /path/to/findings_YYYY-MM-DD.json
 └─> diff_reports.py         → /var/reports/diff/diff_report_YYYY-MM-DD.json
 └─> report_generater.py     → /var/reports/html_reports/report_YYYY-MM-DD.html
```

## Setup

### 1. Directory structure

Create the required output directories:

```bash
sudo mkdir -p /var/reports/diff
sudo mkdir -p /var/reports/html_reports
sudo mkdir -p /var/findings
sudo touch -p /var/log/auditlogs.log
```


### 2. Install dependencies

```bash
pip3 install jinja2
```

### 3. Schedule via cron

Open the crontab editor:

```bash
sudo crontab -e
```

Add the following line to run the pipeline daily at 3:00 AM:

```
0 12 * * * /bin/bash /path/to/run_audit.sh >> /var/log/auditlogs.log 2>&1
```

## Usage

### Run manually

```bash
sudo bash run_audit.sh
```

### Run individual components

```bash
# Run the audit
sudo python3 audit.py

# Run the diff
sudo python3 diff_reports.py findings_2026-05-21.json findings_2026-05-20.json

# Run the HTML report
sudo python3 report_generater.py findings_2026-05-21.json

```

## Output

### Diff report — `diff_report_YYYY-MM-DD.json`

Saved to `/var/reports/diff/`. Contains two sections:

- **New findings** — vulnerabilities that appeared since the last run
- **Resolved findings** — vulnerabilities that are no longer present

[Json_file](diff_report_2026-05-21.json)

### HTML report — `report_YYYY-MM-DD.html`

Saved to `/var/reports/html_reports/`. Includes:

- Summary cards (total, high, medium, low counts)
- Diff section showing new and resolved findings if the diff script ran
- Full findings list with collapsible cards
- Remediation checklist

