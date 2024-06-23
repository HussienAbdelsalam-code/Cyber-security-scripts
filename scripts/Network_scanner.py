#!/usr/bin/env python3

import scapy.all as scapy
import argparse
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target",help="Give the network range you want to scan.")
    options = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_final_request = broadcast/arp_request
    answered = scapy.srp(arp_final_request, timeout=1, verbose=False)[0]
    clients_list = []
    for elemnt in answered:
        client_dictonary = {"ip":elemnt[1].psrc, "mac":elemnt[1].hwsrc}
        clients_list.append(client_dictonary)

    return clients_list

def print_result(result_list):
    print("IP\t\t\tMAC-address")
    print("-"*50)
    for client in result_list:
        print(client["ip"]+"\t\t"+client["mac"])


options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)