import requests
import csv
import subprocess
from io import StringIO

# Fetch the IP blocklist
response = requests.get("https://feodotracker.abuse.ch/downloads/ipblocklist.csv").text

# Delete existing firewall rule
delete_rule = "sudo ufw delete deny from any to any"
subprocess.run(["bash", "-c", delete_rule], check=True)

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
            if ip:
                print("Added Rule to block:", ip)
                # Add firewall rule to block IP
                rule = f"sudo ufw deny from {ip}"
                subprocess.run(["bash", "-c", rule], check=True)
                added_rules.append(ip)
        else:
            print("Invalid row:", row)

    # Verify added rules
    verify_rule = "sudo ufw show added"
    subprocess.run(["bash", "-c", verify_rule])

    # Save added rules to a file
    with open("added_rules.txt", "w") as file:
        file.write("\n".join(added_rules))

    print("All IP rules have been processed and added to the firewall.")
