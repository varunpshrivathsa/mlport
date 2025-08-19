from fastapi import FastAPI
from pydantic import BaseModel
import time

SERVICE_NAME = "mlport-api"
_start_time = time.monotonic()

class Health(BaseModel):
    status: str
    uptime_sec: float
    service: str

app = FastAPI(title="MLPort API", version="0.0.1")

@app.get("/", summary="Root")
def read_root():
    return {"message": "MLPort API is up. See /v1/health"}

@app.get("/v1/health", response_model=Health, summary="Health check")
def health():
    uptime = time.monotonic() - _start_time
    return Health(status="ok", uptime_sec=round(uptime, 3), service=SERVICE_NAME)
