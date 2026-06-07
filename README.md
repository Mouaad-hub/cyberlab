# 🛡️ CyberLab — Cybersecurity Internship Project

A 8-week hands-on cybersecurity lab covering network scanning, SSH log analysis, vulnerability simulation, automated auditing, HTML reporting, real-time alerting, and a live web dashboard — built on Linux VMs using Python 3 and Bash.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Track 1 — Python Scripting Foundations](#track-1--python-scripting-foundations)
- [Track 2 — Vulnerability Lab on VM](#track-2--vulnerability-lab-on-vm)
- [Track 3 — Automated Reporting](#track-3--automated-reporting)
- [Track 4 — Alerting System](#track-4--alerting-system)
- [Git Workflow](#git-workflow)
- [Evaluation Rubric](#evaluation-rubric)

---

## Overview

| Property | Details |
|---|---|
| **Level** | Beginner–Intermediate |
| **Duration** | 8 Weeks |
| **Languages** | Python 3, Bash |
| **Environment** | Linux VM (Ubuntu Server / Metasploitable2) + Host Machine |

---

## Environment Setup

### Requirements

- VirtualBox or VMware
- Ubuntu Server 22.04 LTS (target/victim VM)
- Kali Linux or Ubuntu Desktop (attacker/analyst machine)
- Python 3.10+
- Git



---

## Project Structure

```
cyberlab/
├── Track_1_—_Python_Scripting_Foundations/
│   ├── Task_1.1_—_Network_Scanner_Script/
│   │   ├── scanner.py                        # Network scanner
│   │   ├── scan_2026-05-21_17-32-29.json     # Sample scan output (JSON)
│   │   └── scan_2026-05-21_17-32-29.txt      # Sample scan output (TXT)
│   └── Task_1.2—_Log_Parser/
│       ├── log_parser.py                     # SSH log parser
│       ├── fake_logs.py                      # A script that generates some fack logs
│       ├── auth.log                          # Sample of the fack logs generated 
│       └── SSH_report2026-04-30_15:41:30.json # Sample report output
│
├── Track_2_—_Vulnerability_Lab_on_VM/
│   ├── Task_2.1_—_Cronjob_Vulnerability_Injector/
│   │   ├── vuln_injector.sh                  # Vulnerability injector
│   │   └── vuln_injector.log                 # Sample injection log
│   └── Task_2.2—Audit_Script/
│       ├── audit.py                          # Security audit script
│       └── findings2026-05-16_19:23:22.json  # Sample findings output
│
├── Track_3—Automated_Reporting/
│   ├── Task_3.1_—_HTML_Report_Generator/
│   │   ├── report_generater.py               # HTML report generator
│   │   ├── template.html                     # Jinja2 HTML template
│   │   ├── findings2026-05-16_19:23:22.json  # Sample input
│   │   └── report_2026-05-12_12:40:28.html   # Sample report output
│   └── Task3.2—Scheduled_Audit+Diff_Report/
│       ├── run_audit.sh                      # Full pipeline orchestrator
│       ├── diff_reports.py                   # Diff between audit runs
│       ├── report_generater.py               # HTML report generator (with diff support)
│       ├── template.html                     # Jinja2 HTML template
│       └── diff_report_2026-05-21.json       # Sample diff output
│
└── Track_4—Alerting_System/
    ├── Task_4.1—Alert_System/
    │   ├── alerter.py                        # Alert system (email + Discord)
    │   ├── config_file.json                  # Alert configuration
    │   ├── run_audit.sh                      # Pipeline script
    │   └── diff_report_2026-05-21.json       # Sample diff input
    └── Task4.2—Live_Dashboard(Capstone)/
        ├── dashboard.html                    # Self-contained live dashboard
        └── run_audit.sh                      # Full pipeline (audit → diff → alert → report)
```

> All reports are saved to `/var/reports/` with the following subdirectories:
> - `/var/reports/findings/` — raw audit JSON files
> - `/var/reports/diff/` — diff report JSON files
> - `/var/reports/html_reports/` — generated HTML reports

---

## Track 1 — Python Scripting Foundations

### Task 1.1 — Network Scanner (`scanner.py`)

Scans a subnet using Nmap and displays open ports in a formatted table. Restricted to private/local IP ranges only.

**Usage:**
```bash
python3 scanner.py 192.168.1.0/24
```

**Sample Output:**
```
IP Address      Port    State   Service
--------------------------------------------------
192.168.1.1     22      open    ssh
192.168.1.1     80      open    http
192.168.1.5     3306    open    mysql

Saved TXT report: scan_2026-05-21_17-32-29.txt
Saved JSON report: scan_2026-05-21_17-32-29.json
```

**Features:**
- Accepts a private/local IP range as a CLI argument (rejects public IPs)
- Validates IP format and CIDR notation
- Handles unreachable hosts gracefully
- Saves timestamped results to both `.txt` and `.json`

---

### Task 1.2 — Log Parser (`log_parser.py`)

Parses an `auth.log` file to detect SSH brute-force activity. Flags IPs with 5+ failed login attempts.

> A `fake_logs.py` helper script is included to generate a realistic `auth.log` for testing without needing a live server.

**Usage:**
```bash
# (Optional) Generate a fake auth.log for testing
python3 fake_logs.py

# Run the parser
python3 log_parser.py
```

**Sample Output:**
```
[!] Suspicious Activity Report — 2026-04-30_15:41:30
------------------------------------------------------------
IP: 192.168.1.105 | Total Failed Attempts: 28 | Last Seen: 15:38:10
IP: 10.0.0.22     | Total Failed Attempts: 15 | Last Seen: 15:40:55

Results saved in SSH_report2026-04-30_15:41:30.json
```

**Features:**
- Detects IPs with 5 or more failed SSH login attempts
- Displays attempt count and last seen timestamp per IP
- Exports results to a timestamped JSON report
- Handles `PermissionError` and `FileNotFoundError` gracefully

---

## Track 2 — Vulnerability Lab on VM

### Task 2.1 — Vulnerability Injector (`vuln_injector.sh`)

Introduces intentional misconfigurations into the VM on a cron schedule to simulate a vulnerable environment for auditing.

**Usage:**
```bash
sudo bash vuln_injector.sh           # Randomly inject 2 vulnerabilities
sudo bash vuln_injector.sh --reset   # Restore system to a clean state
```

**Vulnerabilities Injected (randomly selects 2 per run):**

| ID | Vulnerability | What it does |
|---|---|---|
| V1 | Open backdoor port | Starts a Netcat listener on port 4444 via named pipe |
| V2 | World-writable cron file | `chmod 777 /etc/cron.daily/check` |
| V3 | Weak SSH config | Appends `PermitRootLogin yes` and `PermitEmptyPasswords yes` to `sshd_config`, restarts SSH |
| V4 | SUID binary | Compiles a C shell escalation binary and sets its SUID bit at `/usr/local/bin/shell` |
| V5 | Exposed credentials | Writes plaintext passwords, API keys, and JWT tokens to `/tmp/creds.txt` |

**Cron Schedule** (daily at 02:00 AM):
```bash
0 2 * * * /path/to/vuln_injector.sh >> /var/log/vuln_injector.log 2>&1
```

The `--reset` flag cleanly undoes all five vulnerabilities: kills the netcat listener, restores cron permissions, removes weak SSH lines and restarts SSH, deletes the SUID binary, and removes `/tmp/creds.txt`.

---

### Task 2.2 — Audit Script (`audit.py`)

Scans the local VM for the vulnerabilities introduced by Task 2.1 and produces a structured JSON findings report. Must be run with `sudo`.

**Usage:**
```bash
sudo python3 audit.py
```

**Sample Output:**
```
Check                   Severity    Description
----------------------------------------------------------------------
Open ports scan         HIGH        Unexpected open ports
World-writable files    HIGH        Files with 777 or o+w in sensitive dirs
SUID/SGID binaries      HIGH        Unexpected binaries with SUID bit
SSH config audit        MEDIUM      Root login, empty passwords, protocol version
Cron job review         MEDIUM      Unusual or new cron entries
User account audit      MEDIUM      Accounts with no password or UID 0
/tmp sensitive files    LOW         Credentials or keys in /tmp
Firewall status         LOW         UFW/iptables disabled
```

**Checks Performed:**

| Check | Severity | Description |
|---|---|---|
| Open ports scan | 🔴 HIGH | Full port scan of localhost (`-p-`) via Nmap |
| World-writable files | 🔴 HIGH | Finds `o+w` files in sensitive system directories |
| SUID/SGID binaries | 🔴 HIGH | Flags SUID/SGID binaries outside expected system paths |
| SSH config audit | 🟠 MEDIUM | Checks for `PermitRootLogin yes`, `PermitEmptyPasswords yes`, legacy protocol |
| Cron job review | 🟠 MEDIUM | Flags cron files not owned by any installed package (`dpkg -S`) |
| User account audit | 🟠 MEDIUM | Detects non-root UID 0 accounts and empty-password accounts |
| `/tmp` sensitive files | 🔵 LOW | Scans `/tmp` for passwords, API keys, JWTs, private keys, DB credentials |
| Firewall status | 🔵 LOW | Checks if UFW and/or iptables have no active rules |

**Output:** Saves findings to `/var/reports/findings/findings_YYYY-MM-DD.json`. Exits with code `1` if any HIGH severity findings are present.

---

## Track 3 — Automated Reporting

### Task 3.1 — HTML Report Generator (`report_generater.py`)

Converts a JSON findings file from `audit.py` into a styled, self-contained HTML report using Jinja2.

**Usage:**
```bash
sudo python3 report_generater.py findings2026-05-16_19:23:22.json
# Output: /var/reports/html_reports/report_YYYY-MM-DD.html
```

**Report Features:**
- Hostname and scan date in the header (retrieved via `uname -n`)
- Color-coded finding cards by severity (red / orange / green)
- Self-contained HTML (no external CSS dependencies)

---

### Task 3.2 — Scheduled Audit + Diff Report

Orchestrates the full audit pipeline and highlights what has changed since the previous day's run.

#### `diff_reports.py` — Diff Generator

Compares today's findings against yesterday's and outputs new and resolved findings.

**Usage:**
```bash
sudo python3 diff_reports.py findings_today.json findings_yesterday.json
# Output: /var/reports/diff/diff_report_YYYY-MM-DD.json
```

#### `run_audit.sh` — Pipeline Orchestrator

Runs the full pipeline in sequence: audit → diff → report.

**Usage:**
```bash
sudo bash run_audit.sh
```

**Pipeline:**
```
run_audit.sh
 └─> audit.py              → /var/reports/findings/findings_YYYY-MM-DD.json
 └─> diff_reports.py       → /var/reports/diff/diff_report_YYYY-MM-DD.json
 └─> report_generater.py   → /var/reports/html_reports/report_YYYY-MM-DD.html
```

The diff step is skipped automatically if no previous day's findings file exists.

**Cron Entry:**
```bash
0 3 * * * /path/to/run_audit.sh >> /var/log/run_audit.log 2>&1
```

---

## Track 4 — Alerting System

### Task 4.1 — Alert System (`alerter.py`)

Reads the diff report and sends alerts only when **new** HIGH severity findings appear — no spam on repeated runs.

**Usage:**
```bash
python3 alerter.py /var/reports/diff/diff_report_2026-05-21.json config_file.json
```

**Alert Channels:**
- **Email** via `smtplib` with Gmail SMTP (SSL on port 465)
- **Discord** via webhook

**Sample Alert Body:**
```
🚨 New HIGH severity findings:

- date: 2026-05-21 03:00:12
- New HIGH findings: 2

[HIGH] Open ports scan: port: 4444  service: unknown |
[HIGH] World-writable files: Path: /etc/cron.daily/check  Permissions: -rwxrwxrwx |

View full report: /var/reports/report_2026-05-21.html
```

**Configuration (`config_file.json`):**
```json
{
  "email_from": "sender@gmail.com",
  "email_to": "recipient@gmail.com",
  "email_password": "your_app_password",
  "discord_webhook": "https://discord.com/api/webhooks/..."
}
```

**Features:**
- Alerts only on new HIGH findings (compares against previous run via diff file)
- Graceful failure with printed error if network/SMTP is unavailable

---

### Task 4.2 — Live Dashboard (`dashboard.html`) — Capstone

A self-contained web dashboard built with vanilla HTML, CSS, and JavaScript (Chart.js bundled inline). Reads `latest_report.json` to display findings in real time.

**Usage:**
```bash
cd "Track_4—Alerting_System/Task4.2—Live_Dashboard(Capstone)"
python3 -m http.server
# Open http://localhost:8000/dashboard.html
```

**Dashboard Features:**
- Summary cards: total findings, HIGH / MEDIUM / LOW counts
- Findings table with severity filter
- Timeline chart (Chart.js) showing finding counts per day
- Last scan timestamp and hostname display
- Responsive layout — works on mobile

#### `run_audit.sh` (Capstone version)

The Task 4.2 folder includes a complete pipeline script that runs the full audit, copies the latest findings to `latest_report.json` for the dashboard, runs diff, sends alerts, and generates the HTML report.

```bash
sudo bash run_audit.sh
```

---

## Git Workflow

Each task is developed on its own branch and merged via pull request.

```bash
git checkout -b task/1.1-network-scanner

# ... do the work ...

git add scanner.py
git commit -m "feat: add nmap wrapper with table output"
git push origin task/1.1-network-scanner

# Open a pull request for review
```

**Branch naming convention:** `task/<number>-<short-description>`

---


> ⚠️ **Disclaimer:** This project is for educational purposes only. All vulnerability injection and exploitation activities must be performed exclusively within an isolated lab environment. Never run these scripts against systems you do not own or have explicit written permission to test.
