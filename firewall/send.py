#!/usr/bin/python

from scapy.all import Ether, IP, sendp, get_if_hwaddr, get_if_list, TCP, Raw, UDP
import sys
import random, string

def list_youtube_ip():
    youtube_ip = []
    for i in range(232, 240):
        for j in range(0, 256):
            youtube_ip.append(f'199.223.{i}.{j}')
    for i in range(160, 176):
        for j in range(0, 256):
            youtube_ip.append(f'207.223.{i}.{j}')
    for i in range(152, 156):
        for j in range(0, 256):
            youtube_ip.append(f'208.65.{i}.{j}')
    for i in range(224, 256):
        for j in range(0, 256):
            youtube_ip.append(f'208.117.{i}.{j}')
    for i in range(128, 256):
        for j in range(0, 256):
            youtube_ip.append(f'209.85.{i}.{j}')
    for i in range(192, 224):
        for j in range(0, 256):
            youtube_ip.append(f'216.58.{i}.{j}')
    for i in range(32,64):
        for j in range(0, 256):
            youtube_ip.append(f'216.239.{i}.{j}')
    return youtube_ip


def randomword(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def send_random_traffic(num_packets, interface, src_ip, dst_ip, sport, dport):
    dst_mac = "00:00:00:00:00:01"
    src_mac= "00:00:00:00:00:02"
    total_pkts = 0
    for i in range(num_packets):
            data = randomword(22)
            p = Ether(dst=dst_mac,src=src_mac)/IP(dst=dst_ip,src=src_ip)
            p = p/UDP(sport, dport)/Raw(load=data)
            sendp(p, iface = interface, inter = 0.01)
            # If you want to see the contents of the packet, uncomment the line below
            # print(p.show())
            total_pkts += 1
    print("Sent %s packets in total" % total_pkts)

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python send.py number_of_packets interface_name src_ip_address dst_ip_address sport dport")
        sys.exit(1)
    else:
        num_packets = sys.argv[1]
        interface = sys.argv[2]
        src_ip = sys.argv[3]
        dst_ip = sys.argv[4]
        sport = sys.argv[5]
        dport = sys.argv[6]
        send_random_traffic(int(num_packets), interface, src_ip, dst_ip, sport, dport)
