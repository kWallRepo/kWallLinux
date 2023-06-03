import requests
import csv
import subprocess
from io import StringIO
import re
import shlex

# Fetch the IP blocklist
response = requests.get("https://feodotracker.abuse.ch/downloads/ipblocklist.csv").text

# Process the IP blocklist
csv_data = csv.reader(filter(lambda x: not x.startswith("#"), StringIO(response)))
header = next(csv_data)  # Get the header row
ip_index = header.index("dst_ip") if "dst_ip" in header else None

if ip_index is None:
    print("Unable to find the column containing IP addresses.")
else:
    added_rules = []
    for row in csv_data:
        if ip_index < len(row):
            ip = row[ip_index]
            if ip and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
                # Check if rule already exists
                check_rule = ["ufw", "show", "added", "|", "grep", "-w", ip]
                existing_rule = subprocess.run(check_rule, capture_output=True, text=True)
                if existing_rule.stdout.strip():
                    print("Rule already exists. Skipping:", ip)
                else:
                    print("Added Rule to block:", ip)
                    # Add firewall rule to block IP
                    rule = ["sudo", "ufw", "deny", "from", ip]
                    subprocess.run(rule, check=True)
                    added_rules.append(ip)
            else:
                print("Invalid IP address:", ip)
        else:
            print("Invalid row:", row)

    # Verify added rules
    verify_rule = ["ufw", "show", "added"]
    subprocess.run(verify_rule)

    # Save added rules to a file
    with open("added_rules.txt", "w") as file:
        file.write("\n".join(added_rules))

    print("All IP rules have been processed and added to the firewall.")
