from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
  return {"data": "Welcome Raghia"}

@app.post("/detect")
def detect_ddos():
  return {"data": "DDOS Attack Detected"}
