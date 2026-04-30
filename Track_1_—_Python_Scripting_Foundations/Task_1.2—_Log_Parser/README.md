# Task 1.2 — SSH Log Parser

## Objective

Parse the `/var/log/auth.log` file and identify potentially suspicious SSH brute-force activity by counting how many times a specific IP address has had failed login attempts.

---

## Files

| File | Description |
|------|-------------|
| `log_parser.py` | Main parser script. |
| `fake_logs.py` | Test log generator for running on your local machine. Use this only when needed. |
| `SSH_report<timestamp>.json` | The output report (generated automatically by the script). |

---

## Requirements

- Python 3.10+
- Standard linux log system

---

## Usage

### On real linux systems
```bash
python3 log_parser.py
```
> Make sure that you've the read access for `/var/log/auth.log` or use `sudo`

### For local testing
```bash
# Generate fake auth.log first
python3 fake_logs.py
# Now run the parser
python3 log_parser.py
```

---

## Expected Output

```
[!] Suspicious Activity Report

IP: 185.220.101.3 | Failed Attempts: 28 | Last Seen: 14:31:58
IP: 45.33.32.156  | Failed Attempts: 19 | Last Seen: 13:58:44
IP: 10.0.0.22     | Failed Attempts: 14 | Last Seen: 12:45:01

Results saved to SSH_report2026-04-30_14:32:00.json
```

---

## JSON Report Structure


[json result file ](SSH_report2026-04-30_13:20:11.json )


---

## Configuration

Top of file `log_parser.py` allows modification:

| Variable | Default | Description |
|:---------------------|:--------|:-------------------------------------|
| `min_failed_attempts` | `5` | Min failed attempts per IP to flag |
| `auth` | `auth.log` | Path to auth log file (prod: `/var/log/auth.log`) |

---

## Acceptance Criteria

- Detects an IP if there are more than 5 attempts.
- Prints the IP count and time of last attempt.
- Exports a `.json` file with timestamp.
- Returns graceful handling of file not found / insufficient permissions error.

---

## Notes

- The script uses `sshd.*Failed password` as the detection pattern — compatible with both `sshd` and `sshd-session` log formats
- The fake log generator (`fake_logs.py`) is for testing only