from fastapi import APIRouter
import httpx

router = APIRouter(prefix="/api/system", tags=["system"])

@router.get("/status")
async def get_system_status():
    from main import permission_engine
    # Attempt desktop agent telemetry fetch
    telemetry = {
        "battery_percentage": 94.0,
        "is_charging": True,
        "cpu_usage_percent": 12.5,
        "ram_usage_percent": 42.0,
        "disk_free_gb": 128.5,
        "active_window_title": "VS Code - SWITCH-OS",
        "running_processes_count": 142,
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://127.0.0.1:8001/telemetry", timeout=1.5)
            if resp.status_code == 200:
                telemetry = resp.json()
    except Exception:
        pass

    return {
        "status": "ONLINE",
        "telemetry": telemetry,
        "pending_approvals_count": len(permission_engine.pending_approvals),
    }

@router.get("/activity")
async def get_activity_timeline():
    from main import permission_engine
    logs = permission_engine.get_recent_audit_logs()
    return [l.dict() for l in logs]
