# Task 4.2 — Live Security Dashboard

A self-contained web dashboard that reads the latest JSON audit report and displays security findings in real time.

## Overview

This dashboard is the capstone deliverable of the cybersecurity internship program. It consumes the `latest_report.json` output produced by `audit.py` (Task 2.2) and presents findings in a clean, filterable UI with charts.

## Files

```
dashboard/
├── index.html          # Self-contained dashboard (HTML + CSS + JS)
└── latest_report.json  # Symlink or copy of the most recent audit output
```

## Usage

1. Copy or symlink your latest audit report into the dashboard directory:

   ```bash
   cp /var/reports/findings/findings_$(date).json dashboard/latest_report.json
   # or as a symlink updated by the pipeline:
   ln -sf /var/reports/findings/findings_$(date).json dashboard/latest_report.json
   ```

2. Serve the dashboard with Python's built-in HTTP server:

   ```bash
   cd dashboard
   python3 -m http.server 8080
   ```

3. Open your browser and navigate to:

   ```
   http://localhost:8080
   ```

## Expected `latest_report.json` Format

The dashboard expects the JSON structure produced by `audit.py`. Example:




Each finding object must include:

| Field | Type | Description |
|---|---|---|
| `Check` | string | Name of the audit check |
| `Severity` | string | `HIGH`, `MEDIUM`, or `LOW` |
| `Description` | string | Human-readable finding summary |
| `Affected value` / `Affected path` / `Affected users` | array | Impacted assets or values |
| `Recommendation` | string | Suggested remediation step |

## Dashboard Features

- **Summary cards** — total findings count plus individual HIGH / MEDIUM / LOW counts
- **Severity filter** — dropdown to filter the findings table by severity level
- **Findings table** — all findings with check name, severity, description, affected assets, and recommendation
- **Severity bar chart** — visual breakdown of findings by severity (Chart.js)
- **Timeline line chart** — tracks total finding counts across scans over time (persisted in browser `localStorage`)
- **Responsive layout** — works on desktop and mobile screens

## Integration with the Audit Pipeline

The dashboard is automatically kept up to date by `run_audit.sh` (Task 3.2). After running `audit.py`, the script copies today's findings directly into the dashboard directory:

```bash
sudo cp /var/reports/findings/findings_$today.json /path/to/dashboard/latest_report.json
```

### Full Pipeline Flow

`run_audit.sh` orchestrates the following steps in order:

```
run_audit.sh
 │
 ├─ audit.py
 │    └─ produces → /var/reports/findings/findings_YYYY-MM-DD.json
 │    └─ copies   → /path/to/dashboard/latest_report.json          ← feeds this dashboard
 │
 ├─ diff_reports.py  (runs only if yesterday's findings file exists)
 │    └─ produces → /var/reports/diff/diff_report_YYYY-MM-DD.json
 │
 ├─ alerter.py  (runs only if the diff report was generated)
 │    └─ reads   → diff_report_YYYY-MM-DD.json + config_file.json
 │    └─ sends alerts for any NEW HIGH severity findings
 │
 └─ report_generater.py
      └─ with diff  → report_generater.py findings_YYYY-MM-DD.json -d diff_report_YYYY-MM-DD.json
      └─ without    → report_generater.py findings_YYYY-MM-DD.json
      └─ produces   → report_YYYY-MM-DD_HH-MM.html
```

### Scheduling with Cron

To run the full pipeline automatically every day at 03:00 AM:

```cron
0 3 * * * /path/to/run_audit.sh >> /var/log/auditlogs.log 2>&1
```

## Dependencies

All dependencies are bundled — no build step or package manager required.

| Library | Version | How it's loaded |
|---|---|---|
| [Chart.js](https://www.chartjs.org/) | 4.5.1 | Inlined in `dashboard.html` |

## Acceptance Criteria Checklist

- [x] Reads `latest_report.json` via a relative `fetch()` call
- [x] Works when served with `python3 -m http.server`
- [x] Responsive layout (mobile-friendly)
- [x] Summary cards for total, high, medium, and low findings
- [x] Findings table with severity filter dropdown
- [x] Timeline chart showing finding counts per day

