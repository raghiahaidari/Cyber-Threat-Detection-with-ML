from fastapi import FastAPI, UploadFile, HTTPException
from joblib import load
from time import time
from scapy.all import rdpcap

from machine_learning.features.utils import write_to_csv, traffic_stats_summary

app = FastAPI()

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
    write_to_csv(packets, f"./tmp/{csv_filename}")

    # Feature engineering
    batches_file_name = "./tmp/batches-" + csv_filename
    df = traffic_stats_summary(f"./tmp/{csv_filename}", None)
    df.to_csv(batches_file_name, index = False)

    # Load the model
    model = load("./machine_learning/model.sav")

    # TODO: Predict the class of the traffic
    # TODO: Transform the prediction back to a human-readable format
    # TODO: clear the tmp folder

    return {"data": "DDOS Attack Detected"}
