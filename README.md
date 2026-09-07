# MAC Address Changer (Python)

A command-line tool that changes the MAC address of a Linux network interface — built as part of my ethical hacking / penetration testing practice, in an isolated VMware + Kali Linux lab.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Platform](https://img.shields.io/badge/Platform-Linux-informational)
![License](https://img.shields.io/badge/License-MIT-green)

## Why this tool

During penetration testing, the first step is protecting your own identity while you work — testing anonymously so a target can't fingerprint or block you mid-engagement. Spoofing your MAC address is one basic building block of that. This project automates the process (rather than doing it manually) and reports findings responsibly to the relevant authority, in line with standard ethical hacking practice.

## Lab environment

| Component | Version |
|---|---|
| Hypervisor | VMware Workstation |
| Guest OS | Kali GNU/Linux Rolling (2026.1) |
| Language | Python 3.13.12 |

All testing was done in an isolated virtual machine — no production systems or third-party networks were touched.

## Features

- Change a given interface's MAC address from the command line
- Command-line arguments via `optparse` (`-i/--interface`, `-m/--mac`)
- Clear error messages when a required argument is missing
- Validates the MAC address format before attempting a change
- Verifies the change actually took effect (reads the MAC back with `ifconfig`)

## Usage

```bash
sudo python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
```

```
[i] Current MAC: 00:0c:29:aa:bb:cc
[+] Changing MAC address for eth0 to 00:11:22:33:44:55
[+] MAC address was successfully changed to 00:11:22:33:44:55
```

See all options:

```bash
sudo python3 mac_changer.py --help
```

## How it works

1. `optparse` reads `--interface` and `--mac` from the command line (`get_arguments()`), and errors out if either is missing.
2. The MAC address format is validated with a regex before anything is changed.
3. The interface is brought down (`ifconfig <iface> down`).
4. The new MAC is applied (`ifconfig <iface> hw ether <new_mac>`).
5. The interface is brought back up (`ifconfig <iface> up`).
6. The script re-reads the interface's MAC to confirm the change actually took effect.

### Project history

The script went through a few iterations while I was learning:

1. **Manual** — changing the MAC by hand with `ifconfig` commands.
2. **Interactive script** — a first Python version that used `input()` to ask for the interface and new MAC.
3. **`optparse` + CLI arguments** — moved to accepting `-i`/`-m` as real command-line arguments.
4. **Refactored into functions**, plus argument validation (missing-argument errors) and a hostname-resolution fix in the lab VM (`sudo: unable to resolve host kali` → fixed via `/etc/hosts` and `/etc/hostname`).
5. **Final version (this repo)** — the same `optparse`-based logic, with MAC-format validation and a post-change verification step added on top.

> Note: `optparse` is what this project was built and learned with, and it's kept as-is here. Python's docs point newer projects toward `argparse`, so that's worth trying as a follow-up exercise if you want to compare the two.

## Requirements

- Linux (uses `ifconfig`, part of `net-tools`)
- Python 3.x (standard library only — no external packages)
- Root privileges (`sudo`) to change a network interface

## Disclaimer

This tool only changes the MAC address of an interface on the machine it's run on. It's intended for use in your own lab environment, or against systems you are explicitly authorized to test. Always get written authorization before performing any security testing.

## License

MIT — see [LICENSE](LICENSE).
