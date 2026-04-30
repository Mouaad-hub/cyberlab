#!/usr/bin/env python3


#necessary pachages 
import sys
import argparse
import json
from datetime import datetime
import nmap
import re
#allowed targets (private ips )

def is_allowed_target(target: str) -> bool:
    allowed_prefixes = (
        "192.168.",
        "10.",
        "127.",
        "172.16.", "172.17.", "172.18.", "172.19.",
        "172.20.", "172.21.", "172.22.", "172.23.",
        "172.24.", "172.25.", "172.26.", "172.27.",
        "172.28.", "172.29.", "172.30.", "172.31."
    )
    return target.startswith(allowed_prefixes)
def is_valid_target(target: str) -> bool:
    octet = r"(\d{1,3}(-\d{1,3})?)"
    pattern = rf"^{octet}\.{octet}\.{octet}\.{octet}(/\d{{1,2}})?$"
    
    if not re.match(pattern, target):  
        return False
    
    parts = re.split(r"[.\-/]", target)
    for part in parts:
        if part.isdigit() and not (0 <= int(part) <= 255):
            return False
    
    return True
#the main function 
def main():
# add an argumment for the target ip 
    parser = argparse.ArgumentParser(description="Scan local/private network targets using nmap.")
    parser.add_argument("target", help="The target IP or network range ")
    args = parser.parse_args()

    target = args.target
# target not valid 
    if not is_allowed_target(target) or  not is_valid_target(target):
        print(
            "Error: Target must be a valid private/local IP or range.\n"
            "Valid formats:\n"
            "  192.168.x.x\n"
            "  10.x.x.x\n"
            "  172.16-31.x.x\n"
            "  127.0.0.1\n"
            "  192.168.1.0/24  (CIDR)\n"
            "  192.168.10-30.100-255  (nmap range)\n"
            "Public IPs are not allowed."
        )
        sys.exit()
    

#put the time of the scan in the name of the scan file 

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    txt_file = f"scan_{timestamp}.txt"
    json_file = f"scan_{timestamp}.json"

    scanner = nmap.PortScanner()
    results = {
        "timestamp": timestamp,
        "target": target,
        "hosts": []
    }
#handel scan errors 
    try:
        scanner.scan(
            hosts=target,
            arguments="-T4 -Pn -p 1-1024"
        )
    except Exception as e:
        print(f"Scan error: {e}")
        sys.exit()

    print("\nIP Address\tPort\tState\tService")
    print("-" * 50)

    for host in scanner.all_hosts():
        host_state = scanner[host].state()
        host_entry = {
            "ip": host,
            "state": host_state,
            "ports": []
        }
        open_ports_for_host = 0
        if "tcp" in scanner[host]:
# extract port details
            for port in sorted(scanner[host]["tcp"].keys()):
                port_info = scanner[host]["tcp"][port]
                state = port_info.get("state", "unknown")
                service = port_info.get("name", "unknown")
                if state == "open":
                    open_ports_for_host += 1
                    print(
                        f"{host}\t{port}\t{state}\t{service}"
                    )
                    host_entry["ports"].append({
                        "port": port,
                        "state": state,
                        "service": service
                    })
        if open_ports_for_host == 0:
            print(
                f"{host_entry['ip']}\tNone\tNone\tNo open ports found"
            )
        results["hosts"].append(host_entry)
    if not scanner.all_hosts():
        print("No hosts found.")
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write("IP Address\tPort\tState\tService\n")
        f.write("-" * 50 + "\n")
        if not results["hosts"]:
            f.write("No hosts found.\n")
        else:
            for host in results["hosts"]:
                if host["ports"]:
                    for port in host["ports"]:
                        f.write(
                            f"{host['ip']}\t"
                            f"{port['port']}\t"
                            f"{port['state']}\t"
                            f"{port['service']}\n"
                        )
                else:
                    f.write(f"{host['ip']}\tNone\tNone\tNo open ports found\n")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"\nSaved TXT report: {txt_file}")
    print(f"Saved JSON report: {json_file}")

if __name__ == "__main__":
 try:
    main()
 except KeyboardInterrupt:
    print("\n[!] Scan stopped by user. Exiting...")
    sys.exit()
