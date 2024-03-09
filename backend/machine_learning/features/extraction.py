from scapy.all import rdpcap
from utils import write_to_csv

import os

normal = "../data/dataset/normal-traffic.pcap"
ddos = "../data/dataset/ddos-traffic.pcap"

csv_normal = "../data/csv/normal.csv"
csv_ddos = "../data/csv/ddos.csv"

# Create the output directory if they don't exist
os.makedirs("../data/csv", exist_ok=True)

# Read normal traffic pcap file
packets_normal = rdpcap(normal)
# Filter and write to CSV
write_to_csv(packets_normal, csv_normal)

# Read DDoS traffic pcap file
packets_ddos = rdpcap(ddos)
# Filter and write to CSV
write_to_csv(packets_ddos, csv_ddos)
