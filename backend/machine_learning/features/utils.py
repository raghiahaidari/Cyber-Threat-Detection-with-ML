from scapy.layers.inet import IP, ICMP, TCP, UDP
import pandas as pd

PCAP_COLUMNS = ['ip.proto', 'ip.src.len.mean', 'ip.src.len.median', 'ip.src.len.var', 'ip.src.len.std', 'ip.src.len.entropy', 'ip.src.len.cv', 'ip.src.len.cvq', 'ip.src.len.unique_ratio', 'ip.dst.len.mean', 'ip.dst.len.median', 'ip.dst.len.var', 'ip.dst.len.std', 'ip.dst.len.entropy', 'ip.dst.len.cv', 'ip.dst.len.cvq', 'ip.dst.len.unique_ratio', 'sport.mean', 'sport.median', 'sport.var', 'sport.std', 'sport.entropy', 'sport.cv', 'sport.cvq', 'sport.unique_ratio', 'dport.mean', 'dport.median', 'dport.var', 'dport.std', 'dport.entropy', 'dport.cv', 'dport.cvq', 'dport.unique_ratio', 'tcp.flags.mean', 'tcp.flags.median', 'tcp.flags.var', 'tcp.flags.std', 'tcp.flags.entropy', 'tcp.flags.cv', 'tcp.flags.cvq', 'tcp.flags.unique_ratio']
PCAP_COLUMNS_DICT = {key: None for key in PCAP_COLUMNS}

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
    columns = ['frame_number', 'src_addr', 'dst_addr', 'src_port', 'dst_port', 'tcp_flags', 'protocol']
    df = pd.DataFrame(columns = columns)

    for i, pkt in enumerate(packets):
        fields = extract_fields(pkt)
        if fields:
            df.loc[i] = [i] + list(fields)

    df.to_csv(csv_file, index = False)
    return df

def str_to_int(str):
    if type(str) == int:
        return str

    res = 0
    for i in str:
        res += ord(i)

    return res

def ip_len(ip):
	ip = str(ip).split('.')
	length = 0
	for i in ip:
		length += len(i)
	return length

def generate_batch_df(df, status):
    # add ip.len column
    df['ip.src.len'] = df['src_addr'].apply(ip_len)
    df['ip.dst.len'] = df['dst_addr'].apply(ip_len)

    # remove ip.src and ip.dst
    df = df.drop(['src_addr', 'dst_addr'], axis = 1)

    # drop nas
    df = df.fillna(int(0))

    # convert tcp_flags to int
    df['tcp_flags'] = df['tcp_flags'].apply(str_to_int)

    # convert all columns data type to int
    df = df.astype(int)

    # sample random rows from df (all rows)
    df = df.sample(frac = .5, replace = False)

    # final dataframe with summary of pcap file
    df_summary = pd.DataFrame(PCAP_COLUMNS_DICT, index = [0])

    # calculate summary statistics
    df_summary['ip.proto'] = df['protocol'].mean()
    df_summary['ip.src.len.mean'] = df['ip.src.len'].mean()
    df_summary['ip.src.len.median'] = df['ip.src.len'].median()
    df_summary['ip.src.len.var'] = df['ip.src.len'].var()
    df_summary['ip.src.len.std'] = df['ip.src.len'].std()
    df_summary['ip.src.len.entropy'] = int(0)
    df_summary['ip.src.len.cv'] = df_summary['ip.src.len.std'][0] / df_summary['ip.src.len.mean'][0]
    df_summary['ip.src.len.cvq'] = int(0)
    df_summary['ip.src.len.unique_ratio'] = df['ip.src.len'].nunique() / df['ip.src.len'].size

    df_summary['ip.dst.len.mean'] = df['ip.dst.len'].mean()
    df_summary['ip.dst.len.median'] = df['ip.dst.len'].median()
    df_summary['ip.dst.len.var'] = df['ip.dst.len'].var()
    df_summary['ip.dst.len.std'] = df['ip.dst.len'].std()
    df_summary['ip.dst.len.entropy'] = int(0)
    df_summary['ip.dst.len.cv'] = df_summary['ip.dst.len.std'][0] / df_summary['ip.dst.len.mean'][0]
    df_summary['ip.dst.len.cvq'] = int(0)
    df_summary['ip.dst.len.unique_ratio'] = df['ip.dst.len'].nunique() / df['ip.dst.len'].size

    df_summary['sport.mean'] = df['src_port'].mean()
    df_summary['sport.median'] = df['src_port'].median()
    df_summary['sport.var'] = df['src_port'].var()
    df_summary['sport.std'] = df['src_port'].std()
    df_summary['sport.entropy'] = int(0)
    df_summary['sport.cv'] = df_summary['sport.std'][0] / df_summary['sport.mean'][0]
    df_summary['sport.cvq'] = int(0)
    df_summary['sport.unique_ratio'] = df['src_port'].nunique() / df['src_port'].size

    df_summary['dport.mean'] = df['dst_port'].mean()
    df_summary['dport.median'] = df['dst_port'].median()
    df_summary['dport.var'] = df['dst_port'].var()
    df_summary['dport.std'] = df['dst_port'].std()
    df_summary['dport.entropy'] = int(0)
    df_summary['dport.cv'] = df_summary['dport.std'][0] / df_summary['dport.mean'][0]
    df_summary['dport.cvq'] =  int(0)
    df_summary['dport.unique_ratio'] = df['dst_port'].nunique() / df['dst_port'].size

    df_summary['tcp.flags.mean'] = df['tcp_flags'].mean()
    df_summary['tcp.flags.median'] = df['tcp_flags'].median()
    df_summary['tcp.flags.var'] = df['tcp_flags'].var()
    df_summary['tcp.flags.std'] = df['tcp_flags'].std()
    df_summary['tcp.flags.entropy'] = int(0)
    df_summary['tcp.flags.cv'] = df_summary['tcp.flags.std'][0] / df_summary['tcp.flags.mean'][0]
    df_summary['tcp.flags.cvq'] = int(0)
    df_summary['tcp.flags.unique_ratio'] = df['tcp_flags'].nunique() / df['tcp_flags'].size

    df_summary['status'] = status
    return df_summary

def traffic_stats_summary(csv, status, batch_size=100):
    df = pd.read_csv(csv)
    data = []

    # pick batch_size packets at a time
    for j in range(0, (df.shape[0] - (df.shape[0] % batch_size)), batch_size):
        df_temp = df[j : j + batch_size]
        data.append(generate_batch_df(df_temp.copy(), status))

    # pick the left over packets (after forming batches of batch_size)
    df_temp = df[(df.shape[0] - (df.shape[0] % batch_size)) : df.shape[0]]
    df_temp = df[j : j + batch_size]
    data.append(generate_batch_df(df_temp.copy(), status))

    # drop the 1st row
    df_res = pd.concat(data, ignore_index = True)
    df_res = df_res.drop([0], axis = 0)
    return df_res