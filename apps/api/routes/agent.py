from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/api/agent", tags=["agent"])

@router.post("/task")
async def create_agent_task(payload: dict):
    from main import orchestrator
    goal = payload.get("goal")
    if not goal:
        raise HTTPException(status_code=400, detail="Missing task goal")
    res = await orchestrator.process_user_request(user_input=goal)
    return res

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    return {"task_id": task_id, "status": "COMPLETED", "progress_percentage": 100}
