#!/usr/bin/python

from scapy.all import Ether, IP, sendp, get_if_hwaddr, get_if_list, TCP, Raw, UDP
from youtube_ip_addresses import YouTube_list
import sys
import random, string


def randomword(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def random_ip():
    youtube_list = YouTube_list()
    ip_list = random.sample(youtube_list.list_youtube_ip(),50)
    ip_list.append("192.168.10.2")
    ip_list.append("8.8.8.8")
    ip_list.append("0.0.0.0")
    ip_list.append("127.89.44.0")
    return random.choice(ip_list)

def send_random_traffic(num_packets, interface):
    dst_mac = "00:00:00:00:00:01"
    src_mac= "0c:37:96:5f:8a:23"
    total_pkts = 0
    port = 1024
    for i in range(num_packets):
            data = randomword(22)
            randomIP = random_ip()
            p = Ether(dst=dst_mac,src=src_mac)/IP(dst=randomIP,src="192.168.10.1")
            p = p/UDP(sport= 50000, dport=port)/Raw(load=data)
            sendp(p, iface = interface, inter = 0.01)
            # If you want to see the contents of the packet, uncomment the line below
            # print(p.show())
            total_pkts += 1
    print("Sent %s packets in total" % total_pkts)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python send.py number_of_packets interface_name")
        sys.exit(1)
    else:
        num_packets = sys.argv[1]
        interface = sys.argv[2]
        send_random_traffic(int(num_packets), interface)
