"""
mac_changer_input.py
---------------------
Early version: asks the user for the interface and new MAC address
interactively (input()) instead of taking them as command-line
arguments. Kept as part of the project history alongside the final
argument-based version.

Usage:
    sudo python mac_changer_input.py
    (then type the interface and MAC address when prompted)
"""

import subprocess

interface = input("interface >>")
new_mac = input("Mac_Addess >>")

print("[+] changing mac address for " + interface + " to " + new_mac)
subprocess.run(["ifconfig", interface, "down"])
subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
subprocess.run(["ifconfig", interface, "up"])
