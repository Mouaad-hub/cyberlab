#!/usr/bin/env python3

# Import required modules for regex, JSON, file paths, and dates
import re
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

# Set up file paths and report generation timestamp

auth = Path( "auth.log")  # normaly we use /ver/log/auth.log but for testing perpuses we will use auth.log
timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
json_file = f"SSH_report{timestamp}.json"
min_failed_attempts = 5
# Attempt to parse the authentication log file
try:
    with open(auth,"r") as f:

        # Initialize variables to store SSH attempt data
        ssh_login_exist = False
        ip_list = []
        date_list = []
        time_list = []
        
        # Iterate through each line to find failed SSH login attempts
        for line in f:
            failed_pattern = re.search(r"sshd.*Failed password", line)
            ip_pattern = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            # If a failed login and an IP are found, extract and save the details
            if failed_pattern and ip_pattern:
                time_pattern = re.search(r"\d{1,2}:\d{1,2}:\d{1,2}", line)
                date_pattern = re.search(r"\d{1,4}-\d{1,2}-\d{1,2}", line)
                ip_list.append(ip_pattern.group())
                time_list.append(time_pattern.group())
                date_list.append(date_pattern.group())
                ssh_login_exist = True
        # If failed logins were detected, generate and display the report
        if ssh_login_exist:
            print(f"[!] Suspicious Activity Report — {timestamp}")
            print(f"-" * 60)
            unique_ips = set(ip_list)
            results = []
            ip_counts = Counter(ip_list)
            # Process each unique IP to count occurrences and get the last seen time
            for unique_ip in unique_ips:
                count = ip_counts[unique_ip]
                flipped_ip_list = list(reversed(ip_list))
                last_index = len(ip_list) - 1 - flipped_ip_list.index(unique_ip)
                last_time = time_list[last_index]
                if count >= min_failed_attempts:
                    attack_data = {
                        "ip": unique_ip,
                        "failed connections ": count,
                        "last time seen ": last_time,
                    }
                    results.append(attack_data)
                    print(
                        f"IP: {unique_ip} | Total Failed Attempts: {count} | Last Seen: {last_time}"
                    )
            # Structure the final report and save it to a JSON file
            final_report = {
                "report_generated": timestamp,
                "total unique attackers": len(results),
                "attackers": results,
            }
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(final_report, f, indent=4)
        # Notify if no failed connections were found in the log
        if not ssh_login_exist:
            print(f"no failed connections found ")

    print(f"\n\nresults saved in {json_file}")
# Catch exceptions related to missing files or incorrect permissions
except PermissionError:
    print(f"you cant read this file")
except FileNotFoundError:
    print(f"Error: {auth} not found")
