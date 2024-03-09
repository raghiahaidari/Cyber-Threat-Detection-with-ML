from utils import traffic_stats_summary
import os

# Create the output directory if they don't exist
os.makedirs("../data/batches", exist_ok=True)

# Process normal tcp and udp .csv files
df_normal = traffic_stats_summary('../data/csv/normal.csv', 'normal')
df_normal.to_csv('../data/batches/normal.csv', index = False)

# Process ddos tcp and udp .csv files
df_ddos = traffic_stats_summary('../data/csv/ddos.csv', 'ddos')
df_ddos.to_csv('../data/batches/ddos.csv', index = False)
