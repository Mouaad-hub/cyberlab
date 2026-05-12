#  Task 1.1 — Network Scanner Script



##  Overview

`scanner.py` is a CLI-based network scanner built with Python and Nmap. It scans a given private/local subnet, displays open ports in a formatted table, and saves the results to both `.txt` and `.json` report files with timestamps.


---

##  Features

- Accepts a target IP or range as a CLI argument
- Restricts scanning to **private/local IP ranges only** (no public IPs)
- Validates IP format including CIDR and nmap-style ranges
- Displays a live formatted table of open ports during the scan
- Handles unreachable hosts gracefully (no crash, clean output)
- Saves results to:
  - `scan_YYYY-MM-DD_HH-MM-SS.txt`
  - `scan_YYYY-MM-DD_HH-MM-SS.json` 


---

##  File Structure

```
task-1.1-network-scanner/
├── scanner.py                         # Main scanner script
└── README.md                          # This file
└── scan_YYYY-MM-DD_HH-MM-SS.txt       # the text report
└── scan_YYYY-MM-DD_HH-MM-SS.json      # This json report
```

---

##  Requirements

- Python 3.10+
- `nmap` installed on the system
- `python-nmap` Python package

### Install dependencies

```bash
sudo apt update && sudo apt install nmap -y
pip3 install python-nmap
```

---

##  Usage

```bash
sudo python3 scanner.py <target>
```

### Valid target formats

| Format | Example | Description |
|---|---|---|
| Single IP | `192.168.1.5` | One host |
| CIDR range | `192.168.1.0/24` | Full subnet |
| Nmap range | `192.168.10-30.100-255` | IP range |

### Allowed IP ranges (private only)

- `10.x.x.x`
- `172.16.x.x` – `172.31.x.x`
- `192.168.x.x`
- `127.x.x.x` (loopback)

---

##  Example Output


[text file ](scan_2026-04-27_20-21-15.txt)


### JSON output format


[json file ](scan_2026-04-27_20-21-15.json)


---

##  Security Notes
- Scans are limited to ports `1–1024` using `-T4 -Pn` nmap flags.
- This tool is intended for use in **controlled lab environments only** (e.g., VirtualBox/VMware local networks). Never run it against networks you don't own or have explicit permission to test.


##  Skills Practiced

- Python CLI argument parsing (`argparse`)
- Regex-based input validation
- Network scanning with `python-nmap`
- File I/O (`.txt` and `.json` output)
- Error handling and graceful exits

