# Manual MAC Address Change (Kali Linux)

Before writing any automation, I first did this by hand to understand what the script needed to do.

## Steps

1. Check the current MAC address of the interface:

```bash
ifconfig
```

Output shows the interface (e.g. `eth0`) and its current `ether` (MAC) address:

```
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.21.140  netmask 255.255.255.0  broadcast 192.168.21.255
        ether 00:11:22:44:44:44  txqueuelen 1000  (Ethernet)
```

2. Bring the interface down (you can't change the MAC of an active interface):

```bash
sudo ifconfig eth0 down
```

3. Set the new MAC address:

```bash
sudo ifconfig eth0 hw ether 00:22:22:33:44:55
```

> Note: running this *without* `sudo` fails with `SIOCSIFHWADDR: Operation not permitted` — changing a MAC address requires root privileges.

4. Bring the interface back up:

```bash
sudo ifconfig eth0 up
```

5. Confirm the change:

```bash
ifconfig eth0
```

The `ether` line should now show the new MAC address.

## Why automate this

Doing this by hand every time means 4 separate commands, remembering the right order (down → change → up), and re-typing the interface name and MAC each time. `mac_changer.py` wraps this into one command:

```bash
sudo python mac_changer.py -i eth0 -m 00:22:22:33:44:55
```
