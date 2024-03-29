from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from joblib import load
from time import time
from scapy.all import rdpcap

from machine_learning.features.utils import write_to_csv, traffic_stats_summary
from machine_learning.model.detect import classify_traffic

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
   return {"data": "Welcome Raghia"}

@app.post("/detect")
def detect_ddos(file: UploadFile):
    # Validate the file (.pcap)
    if not any(file.filename.endswith(ext) for ext in [".pcap", ".pcapng", ".cap"]):
        raise HTTPException(status_code=422, detail="Invalid file format. Must be a pcap traffic file.")

    # Save the file
    current_time = str(time()).replace(".", "")
    filename = f"./tmp/{current_time}-{file.filename}"
    with open(filename, "wb") as buffer:
        buffer.write(file.file.read())

    # Extract features from the file
    csv_filename = filename.split("/")[-1].split(".")[0] + ".csv"
    packets = rdpcap(filename)
    packets_df = write_to_csv(packets, f"./tmp/{csv_filename}")

    # Feature engineering
    relevant_features = ['ip.proto', 'ip.src.len.mean', 'ip.src.len.median', 'ip.src.len.var', 'ip.src.len.std', 'ip.src.len.cv', 'ip.src.len.rte', 'ip.dst.len.mean', 'ip.dst.len.median', 'ip.dst.len.var', 'ip.dst.len.std', 'ip.dst.len.cv', 'ip.dst.len.rte', 'sport.mean', 'sport.median', 'sport.var', 'sport.std', 'sport.cv', 'sport.rte', 'dport.mean', 'dport.median', 'dport.var', 'dport.std', 'dport.cv', 'dport.rte', 'tcp.flags.mean', 'tcp.flags.median', 'tcp.flags.var', 'tcp.flags.std', 'tcp.flags.cv', 'tcp.flags.rte', 'status']
    batches_file_name = "./tmp/batches-" + csv_filename
    df = traffic_stats_summary(f"./tmp/{csv_filename}", None)
    df = df[relevant_features]
    df.to_csv(batches_file_name, index = False)
    

    # Classify the traffic
    df = classify_traffic(df, "./machine_learning/model.sav")

    # Build the response object
    response = df.to_dict(orient="records")
    for item, i in zip(response, range(len(response))):
        item["from"] = i * 100 + 1
        item["to"] = (i + 1) * 100
        item["status"] = item["status"]

        # Extract the content of the batch
        batch = packets_df.iloc[(item["from"] - 1):item["to"]]
        batch = batch.to_dict(orient="records")

        # Add the batch to the response
        item["content"] = []
        for packet in batch:
            item["content"].append({
                "frame": packet["frame_number"],
                "ip": {
                    "src": packet["src_addr"],
                    "dst": packet["dst_addr"]
                },
                "port": {
                    "src": packet["src_port"],
                    "dst": packet["dst_port"]
                },
                "protocol": "TCP" if packet["protocol"] == 6 else "UDP",
            })

    return {"data": response}
