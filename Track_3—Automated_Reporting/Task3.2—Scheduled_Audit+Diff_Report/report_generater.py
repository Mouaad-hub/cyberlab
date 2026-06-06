import jinja2
import argparse
import json
import sys
from datetime import datetime
import os
# Setup argument parser to accept the findings JSON file
parser = argparse.ArgumentParser()
parser.add_argument("findings", help="Path to the JSON findings file")
parser.add_argument("--diff_findings", "-d",     help= "Path to diff file", default=None)
args = parser.parse_args()

# Store the provided file path
json_file = args.findings
diff_json_file = args.diff_findings


# Open and parse the JSON findings file

try:

    if diff_json_file and not diff_json_file.endswith('.json'):
        print("Diff file must be a JSON file")
        sys.exit(1)
    diff_data = None
    if diff_json_file and diff_json_file.endswith('.json'):
        with open(diff_json_file, "r") as f:
            diff_data = json.load(f)
    # Check if the provided file has a .json extension
    if json_file.endswith('.json'):
        with open(json_file, "r") as f:
            data = json.load(f)
        
    else:
        print("Please pass a JSON file as an argument")
        sys.exit(1)

    # Setup Jinja2 environment to load templates from the current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(script_dir))

    # Load the specific HTML template
    template = env.get_template('template.html')

    # Render the template with the JSON data and hostname

    output = template.render(data=data, diff_data = diff_data,  hostname=data["host name"])
         
    

    # Generate the output HTML file name based on the audit date
    date = datetime.now().strftime("%Y-%m-%d")
    html_file = f"/var/reports/html_reports/report_{date}.html"
    
    # Write the rendered HTML to the output file
    with open(html_file, 'w') as f:
        f.write(output)

except Exception as e :
    # Handle Errors
    print(f"ERROR {e}")
    sys.exit(1)