from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/api/tools", tags=["tools"])

@router.get("")
async def list_tools():
    from main import tool_registry
    return [t.dict() for t in tool_registry.list_tools_for_agent()]

@router.post("/confirm")
async def confirm_tool_action(payload: dict):
    from main import permission_engine, tool_registry
    approval_id = payload.get("approval_id")
    approved = payload.get("approved", False)

    if not approval_id:
        raise HTTPException(status_code=400, detail="Missing approval_id")

    req = permission_engine.confirm_action(approval_id=approval_id, approved=approved)
    if not req:
        raise HTTPException(status_code=44, detail="Approval request not found")

    if approved:
        # Execute approved tool
        res = await tool_registry.execute_tool(req["tool_name"], req["arguments"])
        return {"approved": True, "executed": True, "result": res.dict()}

    return {"approved": False, "executed": False, "message": "Action rejected by user."}
