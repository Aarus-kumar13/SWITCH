import sys
import os
import logging
from pathlib import Path

# Add root project path to Python sys.path
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("switch.api")

from packages.ai.router import AIRouter
from packages.tools.registry import ToolRegistry
from packages.permissions.engine import PermissionEngine
from packages.memory.engine import MemoryEngine
from packages.learning.engine import PersonalLearningEngine
from packages.agents.orchestrator import AgentOrchestrator
from packages.voice.provider import OpenAIVoiceProvider
from packages.telephony.provider import TwilioTelephonyProvider

# Singletons initialization
ai_router = AIRouter()
tool_registry = ToolRegistry()
permission_engine = PermissionEngine()
memory_engine = MemoryEngine()
learning_engine = PersonalLearningEngine(memory_engine=memory_engine)
orchestrator = AgentOrchestrator(
    ai_router=ai_router,
    tool_registry=tool_registry,
    permission_engine=permission_engine,
    memory_engine=memory_engine,
    learning_engine=learning_engine,
)
voice_provider = OpenAIVoiceProvider()
telephony_provider = TwilioTelephonyProvider()

app = FastAPI(
    title="SWITCH Autonomous Personal AI OS Backend",
    version="1.0.0",
    description="Backend API Gateway & Intelligence Layer for SWITCH",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
from apps.api.routes.chat import router as chat_router
from apps.api.routes.agent import router as agent_router
from apps.api.routes.tools import router as tools_router
from apps.api.routes.memory import router as memory_router
from apps.api.routes.learning import router as learning_router
from apps.api.routes.phone import router as phone_router
from apps.api.routes.system import router as system_router

app.include_router(chat_router)
app.include_router(agent_router)
app.include_router(tools_router)
app.include_router(memory_router)
app.include_router(learning_router)
app.include_router(phone_router)
app.include_router(system_router)

@app.get("/")
def root():
    return {
        "name": "SWITCH Autonomous Personal AI Operating System",
        "status": "online",
        "version": "1.0.0",
        "documentation": "/docs",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.api.main:app", host="0.0.0.0", port=8000, reload=True)
