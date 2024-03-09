from fastapi import FastAPI, UploadFile, HTTPException
from joblib import load
from time import time

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

    # TODO: Extract features from the file
    # TODO: Feature engineering

    # Load the model
    model = load("./machine_learning/model.sav")

    # TODO: Predict the class of the traffic
    # TODO: Transform the prediction back to a human-readable format
    # TODO: clear the tmp folder

    return {"data": "DDOS Attack Detected"}
