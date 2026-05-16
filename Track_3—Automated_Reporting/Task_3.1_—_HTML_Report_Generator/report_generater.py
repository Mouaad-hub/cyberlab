import jinja2
import argparse
import json
import subprocess
import sys

# Setup argument parser to accept the findings JSON file
parser = argparse.ArgumentParser()
parser.add_argument("findings", help="Path to the JSON findings file")
args = parser.parse_args()

# Store the provided file path
json_file = args.findings

# Execute the 'uname -n' command to get the system's hostname
run = subprocess.run(
    ['uname', '-n'], 
    capture_output=True, 
    text=True
)
hostname = run.stdout.strip()

# Open and parse the JSON findings file
try:
    # Check if the provided file has a .json extension
    if json_file.endswith('.json'):
        with open(json_file, "r") as f:
            data = json.load(f)
    else:
        print("Please pass a JSON file as an argument")
        sys.exit(1)

    # Setup Jinja2 environment to load templates from the current directory
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))

    # Load the specific HTML template
    template = env.get_template('template.html')

    # Render the template with the JSON data and hostname
    output = template.render(data=data, hostname=hostname)

    # Generate the output HTML file name based on the audit date
    html_file = f"results_{data['audit date']}.html"

    # Write the rendered HTML to the output file
    with open(html_file, 'w') as f:
        f.write(output)

except FileNotFoundError:
    # Handle the case where the JSON file is not found
    print("File not found")
    sys.exit(1)
    
