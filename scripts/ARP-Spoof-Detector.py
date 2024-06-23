#!/usr/bin/env python3

import sys
import scapy.all as scapy
import argparse

def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--interface",dest="interface",help="Input the interface you want to sniff packets from.")
    options = parser.parse_args()
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_final_request = broadcast/arp_request
    answered = scapy.srp(arp_final_request, timeout=1, verbose=False)[0]
    return answered[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False,prn=process_sniffed_packet)
    
def process_sniffed_packet(packet):
    try:
        if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                print("[*]You are under attack!!")
    except IndexError:
        pass
        
def main():
    if len((sys.argv)) > 1:
        options = get_argument()
        sniff(options.interface)
    else:
        print("Please input the arguments ... !")
        print("./packet-sniffer --help --> to view the help menu !")

if __name__ == "__main__":
    main()

