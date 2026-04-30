#!/usr/bin/env python3
# generate_fake_auth_log.py

import random
from datetime import datetime, timedelta

output_path="auth.log"
num_entries=200
    
# Pool of fake attacker IPs
attacker_ips = [
        "192.168.1.105", "10.0.0.22", "203.0.113.45",
        "198.51.100.7", "172.16.0.88", "45.33.32.156",
        "185.220.101.3", "91.240.118.172", "194.165.16.11"
    ]
    
usernames = ["root", "youness" , "admin", "ubuntu", "pi", "test", "deploy" , "mouaad" , "kali" ]
ports = ["22", "2222"]
    
base_time = datetime(2026, 4, 30, 0, 0, 0)
lines = []

for i in range(num_entries):
        ip = random.choice(attacker_ips)
        user = random.choice(usernames)
        port = random.choice(ports)
        pid = random.randint(10000, 99999)
        ts = base_time + timedelta(seconds=i * random.randint(10, 120))
        timestamp = ts.strftime("%Y-%m-%dT%H:%M:%S")
# example of a log : 2026-04-29T16:05:11.266464+01:00 kali sshd-session[44196]: Failed password for mouaad from 10.180.162.41 port 49365 ssh2
        line = (
            f"{timestamp} kali sshd-session[{pid}]: "
            f"Failed password for {user} from {ip} port {port} ssh2\n "
           
        )
        lines.append(line)

# Mix in some unrelated/benign log lines so the parser has noise to filter
noise = [
        f"{base_time.strftime('%Y-%m-%d %H:%M:%S')} myserver systemd[1]: Started Session.\n",
        f"{base_time.strftime('%Y-%m-%d %H:%M:%S')} myserver sudo: user ran a command\n",
        f"{base_time.strftime('%Y-%m-%d %H:%M:%S')} myserver sshd[9999]: Accepted password for alice from 10.1.1.1 port 22 ssh2\n",
    ]
lines += noise
random.shuffle(lines)

with open(output_path, "w") as f:
        f.writelines(lines)

print(f"[+] Generated {len(lines)} log lines → {output_path}")

