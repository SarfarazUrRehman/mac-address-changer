#!/usr/bin/env python3
"""
mac_changer.py
---------------
Changes the MAC address of a network interface on Linux. Built while
practicing ethical hacking / penetration testing fundamentals
(identity/traffic anonymization during authorized security testing)
in a VMware + Kali Linux lab.

Tested on: Kali GNU/Linux Rolling (2026.1), Python 3.13.12

Usage:
    sudo python mac_changer.py -i eth0 -m 00:11:22:33:44:55
    sudo python mac_changer.py --interface eth0 --mac 00:11:22:33:44:55
    sudo python mac_changer.py --help

Only use this on hardware/VMs you own or are explicitly authorized to test.
"""

import subprocess
import optparse
import re


# ---------------------------------------------------------------------------
# Original code
# ---------------------------------------------------------------------------

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                       help="interface to change its Mac Address")
    parser.add_option("-m", "--mac", dest="new_mac",
                       help="new mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify the correct interface name or get the information through --help")
    elif not options.new_mac:
        parser.error("[-] Please specify the correct Mac Address or get the information through --help")
    return options


def mac_changing(interface, new_mac):
    print("[+] changing mac address for " + interface + " to " + new_mac)
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])


# ---------------------------------------------------------------------------
# Additions (optional, on top of the original — safe to remove)
# ---------------------------------------------------------------------------

def validate_mac(mac):
    """Return True if mac matches the XX:XX:XX:XX:XX:XX format."""
    return bool(re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", mac))


def get_current_mac(interface):
    """Read back the interface's current MAC address via ifconfig."""
    result = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
    match = re.search(r"ether ([0-9A-Fa-f:]{17})", result.stdout)
    return match.group(1) if match else None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

options = get_arguments()

if not validate_mac(options.new_mac):
    print("[-] Invalid MAC address format. Expected XX:XX:XX:XX:XX:XX")
    exit(1)

mac_changing(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac and current_mac.lower() == options.new_mac.lower():
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address does not appear to have been changed.")
