import sys
from pathlib import Path

# Add desktop-agent folder to sys.path
agent_dir = Path(__file__).resolve().parent
if str(agent_dir) not in sys.path:
    sys.path.insert(0, str(agent_dir))

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from computer.os_tools import OSTools
from system.telemetry import TelemetryCollector
from vision.screen import ScreenVision

app = FastAPI(title="SWITCH Local Desktop Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "online", "service": "switch-desktop-agent"}

@app.get("/telemetry")
def get_telemetry():
    return TelemetryCollector.get_system_telemetry()

@app.post("/app/open")
def open_app(payload: dict):
    app_name = payload.get("application")
    if not app_name:
        raise HTTPException(status_code=400, detail="Missing application parameter")
    return OSTools.open_application(app_name)

@app.post("/files/search")
def search_files(payload: dict):
    directory = payload.get("directory", ".")
    pattern = payload.get("pattern", "*")
    return OSTools.search_files(directory, pattern)

@app.get("/screen/capture")
def capture_screen():
    return ScreenVision.analyze_screen_semantics()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
