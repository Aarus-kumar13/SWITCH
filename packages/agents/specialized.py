import logging
from typing import Any, Dict, Optional
from packages.shared.schemas import AgentType
from packages.agents.base import BaseAgent
from packages.ai.router import AIRouter
from packages.tools.registry import ToolRegistry
from packages.permissions.engine import PermissionEngine

logger = logging.getLogger("switch.agents.specialized")

class GeneralAssistantAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.GENERAL_ASSISTANT, ai_router, tool_registry, permission_engine)


class ComputerControlAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.COMPUTER_CONTROL, ai_router, tool_registry, permission_engine)


class DeveloperAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.DEVELOPER, ai_router, tool_registry, permission_engine)


class ResearchAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.RESEARCH, ai_router, tool_registry, permission_engine)


class TroubleshootingAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.TROUBLESHOOTING, ai_router, tool_registry, permission_engine)


class CommunicationAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.COMMUNICATION, ai_router, tool_registry, permission_engine)


class SchedulingAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.SCHEDULING, ai_router, tool_registry, permission_engine)


class ProductivityAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.PRODUCTIVITY, ai_router, tool_registry, permission_engine)


class MemoryAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.MEMORY, ai_router, tool_registry, permission_engine)


class VoiceAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.VOICE, ai_router, tool_registry, permission_engine)


class VisionAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.VISION, ai_router, tool_registry, permission_engine)


class SecurityAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.SECURITY, ai_router, tool_registry, permission_engine)


class WorkflowAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.WORKFLOW, ai_router, tool_registry, permission_engine)


class PersonalLearningAgent(BaseAgent):
    def __init__(self, ai_router: AIRouter, tool_registry: ToolRegistry, permission_engine: PermissionEngine):
        super().__init__(AgentType.PERSONAL_LEARNING, ai_router, tool_registry, permission_engine)
