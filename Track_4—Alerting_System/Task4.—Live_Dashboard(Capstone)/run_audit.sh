#!/bin/bash 

# Set the variables for today's and yesterday's dates
today=$(date +"%Y-%m-%d")
yesterday=$(date -d "-1 day" +"%Y-%m-%d")

# Check if the audit script exists, then execute it
if [ -f /home/mouaad/audit/audit.py ]; then 
    sudo python3 /home/mouaad/audit/audit.py
    # copy the today findings to the dashboard folder and change its name to latest_report.json
    sudo cp /var/reports/findings/findings_$today.json /path/to/dashboard/latest_report.json
    
    # Check if the diff report script and yesterday's findings exist, then execute diff generation
    if [ -f /home/mouaad/audit/diff_reports.py ] && [ -f /var/reports/findings/findings_$yesterday.json ]; then 
        sudo python3 /home/mouaad/audit/diff_reports.py /var/reports/findings/findings_$today.json /var/reports/findings/findings_$yesterday.json
        # run the alter script to notify for any new HIGH findings 
        sudo python /home/mouaad/audit/alerter.py /var/reports/diff/diff_report_$today.json /home/mouaad/audit/config_file.json
    fi
    
    # Check if the report generator script exists
    if [ -f /home/mouaad/audit/report_generater.py ]; then 
        # Run the report generator with or without the diff report based on its existence
        if [ -f /var/reports/diff/diff_report_$today.json ]; then 
            sudo python3 /home/mouaad/audit/report_generater.py /var/reports/findings/findings_$today.json -d /var/reports/diff/diff_report_$today.json
        else  
            sudo python3 /home/mouaad/audit/report_generater.py /var/reports/findings/findings_$today.json
        fi
    else 
        echo "can't find report_generater.py"
        exit 1 
    fi 
fi
