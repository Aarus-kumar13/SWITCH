import uuid
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from packages.shared.schemas import MemoryItem, UserMessage, AgentTask

logger = logging.getLogger("switch.memory.engine")

class MemoryEngine:
    def __init__(self):
        self.short_term_messages: List[UserMessage] = []
        self.episodic_memories: List[Dict[str, Any]] = []
        self.semantic_memories: Dict[str, MemoryItem] = {}
        self.user_profile: Dict[str, Any] = {
            "preferred_editor": "VS Code",
            "communication_style": "concise, technical",
            "operating_system": "Windows",
            "primary_languages": ["Python", "TypeScript", "React", "Java"],
            "notifications_enabled": True,
        }
        self.active_tasks: Dict[str, AgentTask] = {}
        self._initialize_default_memories()

    def _initialize_default_memories(self):
        m1 = MemoryItem(
            id=str(uuid.uuid4()),
            category="preference",
            key="preferred_editor",
            value="VS Code",
            confidence=0.98,
            user_confirmed=True,
            observation_count=15,
        )
        m2 = MemoryItem(
            id=str(uuid.uuid4()),
            category="preference",
            key="explanation_style",
            value="step_by_step_technical",
            confidence=0.92,
            user_confirmed=True,
            observation_count=8,
        )
        self.semantic_memories[m1.key] = m1
        self.semantic_memories[m2.key] = m2

    def add_short_term_message(self, message: UserMessage):
        self.short_term_messages.append(message)
        if len(self.short_term_messages) > 50:
            self.short_term_messages.pop(0)

    def get_context_window(self, limit: int = 10) -> List[UserMessage]:
        return self.short_term_messages[-limit:]

    def add_episodic_event(self, action: str, result: str, details: Optional[Dict[str, Any]] = None):
        event = {
            "id": str(uuid.uuid4()),
            "action": action,
            "result": result,
            "details": details or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.episodic_memories.append(event)

    def set_semantic_memory(self, key: str, value: Any, category: str = "fact", user_confirmed: bool = False) -> MemoryItem:
        if key in self.semantic_memories:
            item = self.semantic_memories[key]
            item.value = value
            item.observation_count += 1
            item.confidence = min(1.0, item.confidence + 0.05)
            item.user_confirmed = item.user_confirmed or user_confirmed
            item.last_updated = datetime.now(timezone.utc)
        else:
            item = MemoryItem(
                id=str(uuid.uuid4()),
                category=category,
                key=key,
                value=value,
                confidence=0.8 if not user_confirmed else 1.0,
                user_confirmed=user_confirmed,
                observation_count=1,
            )
            self.semantic_memories[key] = item
        return item

    def get_semantic_memory(self, key: str) -> Optional[MemoryItem]:
        return self.semantic_memories.get(key)

    def delete_semantic_memory(self, key: str) -> bool:
        if key in self.semantic_memories:
            del self.semantic_memories[key]
            return True
        return False

    def list_all_memories(self) -> List[MemoryItem]:
        return list(self.semantic_memories.values())

    def update_user_profile(self, updates: Dict[str, Any]):
        self.user_profile.update(updates)

    def get_user_profile(self) -> Dict[str, Any]:
        return self.user_profile
