from scapy.layers.inet import IP, ICMP, TCP, UDP

def extract_fields(pkt):
    if IP in pkt:
        if TCP in pkt and not pkt.haslayer(ICMP):
            return (
                pkt[IP].src,
                pkt[IP].dst,
                pkt[TCP].sport,
                pkt[TCP].dport,
                pkt[TCP].flags,
                pkt[IP].proto
            )

        if UDP in pkt and not pkt.haslayer(ICMP):
            return (
                pkt[IP].src,
                pkt[IP].dst,
                pkt[UDP].sport,
                pkt[UDP].dport,
                None,
                pkt[IP].proto
            )

    return None

def write_to_csv(packets, csv_file):
    with open(csv_file, "w") as f:
        f.write("frame_number,src_addr,dst_addr,src_port,dst_port,tcp_flags,protocol\n")
        for i, pkt in enumerate(packets):
            fields = extract_fields(pkt)
            if fields:
                f.write(f"{i},{','.join(map(str, fields))}\n")
