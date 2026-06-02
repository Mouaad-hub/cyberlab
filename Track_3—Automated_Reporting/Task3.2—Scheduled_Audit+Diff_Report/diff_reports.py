import argparse 
import sys 
import json
from datetime import datetime 

# Set up argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("new_findings", help="Path to the JSON new findings file")
parser.add_argument("prev_findings", help="Path to the JSON previous findings file")
args = parser.parse_args()

# Validate file extensions
if not args.new_findings.endswith('.json') or not args.prev_findings.endswith('.json'):
    print("Please pass a JSON file as an argument")
    sys.exit(1)

# Load JSON data from both files
try:
    with open(args.new_findings, "r") as f:
        new_data = json.load(f)
    with open(args.prev_findings, "r") as f:
        prev_data = json.load(f)
except FileNotFoundError:
    print("File not found")
    sys.exit(1)
except PermissionError:
    print("Permission denied, try running with sudo ")
    sys.exit(1)

# If there are no differences, exit early
if new_data == prev_data:
    print("No new findings, and no resolved findings")
    sys.exit(0)

# Initialize dictionary for diff results
diff_results = {
    "New findings": [],
    "Resolved findings": []
}

# Identify new findings
for key, value in new_data.items():
    if not isinstance(value, list):
        continue
    if new_data[key] == prev_data[key]:
        continue

    # Prevent IndexError if new_data[key] is empty (meaning no new findings for this check)
    if not value:
        continue

    for item in value[0]:  
        if item.startswith("Affected"):
            new_findings_value = [] 
            # Safely get previous affected items. Default to empty list if prev_data[key] is []
            prev_affected = prev_data[key][0][item] if prev_data.get(key) and len(prev_data[key]) > 0 else []
            
            for entry in value[0][item]: 
                if entry not in prev_affected:
                    new_findings_value.append(entry)

            if new_findings_value:
                finding_copy = {k: v for k, v in value[0].items()} 
                finding_copy[item] = new_findings_value
                diff_results["New findings"].append([finding_copy])

# Identify resolved findings
for key, value in prev_data.items():
    if not isinstance(value, list):
        continue
    if prev_data[key] == new_data[key]:
        continue

    # Prevent IndexError if prev_data[key] is empty (meaning no old findings to resolve)
    if not value:
        continue

    for item in value[0]:  
        if item.startswith("Affected"):
            resolved_findings_value = [] 
            # Safely get new affected items. Default to empty list if new_data[key] is []
            new_affected = new_data[key][0][item] if new_data.get(key) and len(new_data[key]) > 0 else []
            
            for entry in value[0][item]: 
                if entry not in new_affected:
                    resolved_findings_value.append(entry)

            if resolved_findings_value:
                finding_copy = {k: v for k, v in value[0].items()} 
                finding_copy[item] = resolved_findings_value
                diff_results["Resolved findings"].append([finding_copy])

# Save the diff report to a JSON file
date = datetime.now().strftime("%Y-%m-%d")
diff_file = f"/var/reports/diff/diff_report_{date}.json"
with open(diff_file, "w", encoding="utf-8") as f:
    json.dump(diff_results, f, indent=4)

print("Diff report successfully generated: diff_report.json")