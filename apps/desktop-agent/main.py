import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from apps.desktop_agent.computer.os_tools import OSTools
from apps.desktop_agent.system.telemetry import TelemetryCollector
from apps.desktop_agent.vision.screen import ScreenVision

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
    uvicorn.run("apps.desktop-agent.main:app", host="127.0.0.1", port=8001, reload=True)
