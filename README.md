# kWall Firewall Utility, but for Linux
kWall is a firewall utility improves your network security. It fetches a IP blocklist filled with malicious IPs provided by abuse.ch, then creates rules in UFW Firewall to block incoming/outgoing connections from/to these IPs. The IP blocklist is generated every 5 minutes.

REQUIREMENTS: Python 3.11.3, which can be installed using "sudo apt install python3".

To start using kWall, simply download, open your terminal and navigate to the directory the script is in, then run the script using "sudo python3 kWall.py".

Downloads can be found on the kWall website: https://kwall.rf.gd
