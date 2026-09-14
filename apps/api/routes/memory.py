from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/api/memory", tags=["memory"])

@router.get("")
async def get_all_memories():
    from main import memory_engine
    return {
        "user_profile": memory_engine.get_user_profile(),
        "semantic_memories": [m.dict() for m in memory_engine.list_all_memories()],
    }

@router.post("")
async def set_memory(payload: dict):
    from main import memory_engine
    key = payload.get("key")
    value = payload.get("value")
    category = payload.get("category", "fact")

    if not key or value is None:
        raise HTTPException(status_code=400, detail="Key and value required")

    mem = memory_engine.set_semantic_memory(key=key, value=value, category=category, user_confirmed=True)
    return mem.dict()

@router.delete("/{key}")
async def delete_memory(key: str):
    from main import memory_engine
    success = memory_engine.delete_semantic_memory(key)
    if not success:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"deleted": True, "key": key}
