#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC")
    parser.add_option("-m","--mac",dest="mac_address",help="New mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-]Please specify an interface, use --help for info")
    elif not options.mac_address:
        parser.error("[-]Please specify an new mac-address, use --help for info")
    else:
        return options
    
def change_mac(interface, mac_address):
    print(f"[+]Changing the mac of interface {interface} to {mac_address}")
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw", "ether",mac_address])
    subprocess.call(["ifconfig",interface,"up"])

def get_current_mac(interface):
    ifconfig_output = subprocess.check_output(["ifconfig",interface]).decode()
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output).group(0)
    if mac_address_search_result:
        return mac_address_search_result
    else:
        print("Could not read mac address!")


options = get_arguments()

current_mac = str(get_current_mac(options.interface))

print(f"[+]Current MAC = {current_mac}")

change_mac(options.interface, options.mac_address)

current_mac = get_current_mac(options.interface)

if current_mac == options.mac_address:
    print(f"[+]Successfully changed to {options.mac_address}")
else:
    print("[-]Failed to change it")


