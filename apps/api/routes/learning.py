from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/api/learning", tags=["learning"])

@router.get("")
async def get_learning_status():
    from main import learning_engine
    return {
        "summary": learning_engine.get_learning_summary(),
        "candidate_workflows": learning_engine.get_candidate_workflows_for_approval(),
        "learned_workflows": [w.dict() for w in learning_engine.get_learned_workflows()],
    }

@router.post("/feedback")
async def post_user_feedback(payload: dict):
    from main import learning_engine
    original_action = payload.get("original_action")
    correction = payload.get("correction")

    if original_action and correction:
        learning_engine.handle_explicit_correction(original_action, correction)
        return {"status": "success", "learned_correction": f"{original_action} -> {correction}"}

    return {"status": "received"}

@router.post("/workflow/formalize")
async def formalize_workflow(payload: dict):
    from main import learning_engine
    name = payload.get("name")
    trigger = payload.get("trigger_command")
    steps = payload.get("steps", [])

    if not name or not trigger:
        raise HTTPException(status_code=400, detail="Workflow name and trigger required")

    wf = learning_engine.create_workflow_from_pattern(name=name, trigger_command=trigger, steps=steps)
    return wf.dict()
