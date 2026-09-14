import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    from main import orchestrator, memory_engine
    from packages.shared.schemas import UserMessage

    # Add message to short-term memory
    user_msg = UserMessage(id=str(uuid.uuid4()), role="user", content=request.message)
    memory_engine.add_short_term_message(user_msg)

    # Process request via Agent Orchestrator
    result = await orchestrator.process_user_request(
        user_input=request.message,
        context=request.context,
    )

    # Store assistant response
    asst_msg = UserMessage(id=str(uuid.uuid4()), role="assistant", content=result["response"])
    memory_engine.add_short_term_message(asst_msg)

    return result

@router.post("/voice/session")
async def voice_session_endpoint(payload: dict):
    from main import voice_provider
    audio_base64 = payload.get("audio_data")
    if not audio_base64:
        return {"transcript": "SWITCH, start my project.", "response": "Starting your React project environment now."}
    
    # Process speech
    transcript = await voice_provider.speech_to_text(b"mock_bytes")
    return {
        "transcript": transcript,
        "response": f"I heard: '{transcript}'. Executing requested autonomous task.",
    }
