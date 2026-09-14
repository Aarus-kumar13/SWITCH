import logging
from typing import Any, Dict, List, Optional
from packages.shared.schemas import AgentType, AgentTask, AgentState
from packages.ai.router import AIRouter
from packages.tools.registry import ToolRegistry
from packages.permissions.engine import PermissionEngine
from packages.memory.engine import MemoryEngine
from packages.learning.engine import PersonalLearningEngine
from packages.agents.base import BaseAgent
from packages.agents.specialized import (
    GeneralAssistantAgent,
    ComputerControlAgent,
    DeveloperAgent,
    ResearchAgent,
    TroubleshootingAgent,
    CommunicationAgent,
    SchedulingAgent,
    ProductivityAgent,
    MemoryAgent,
    VoiceAgent,
    VisionAgent,
    SecurityAgent,
    WorkflowAgent,
    PersonalLearningAgent,
)

logger = logging.getLogger("switch.agents.orchestrator")

class AgentOrchestrator:
    def __init__(
        self,
        ai_router: AIRouter,
        tool_registry: ToolRegistry,
        permission_engine: PermissionEngine,
        memory_engine: MemoryEngine,
        learning_engine: PersonalLearningEngine,
    ):
        self.ai_router = ai_router
        self.tool_registry = tool_registry
        self.permission_engine = permission_engine
        self.memory_engine = memory_engine
        self.learning_engine = learning_engine
        self.agents: Dict[AgentType, BaseAgent] = {}
        self._initialize_agents()

    def _initialize_agents(self):
        self.agents[AgentType.GENERAL_ASSISTANT] = GeneralAssistantAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.COMPUTER_CONTROL] = ComputerControlAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.DEVELOPER] = DeveloperAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.RESEARCH] = ResearchAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.TROUBLESHOOTING] = TroubleshootingAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.COMMUNICATION] = CommunicationAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.SCHEDULING] = SchedulingAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.PRODUCTIVITY] = ProductivityAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.MEMORY] = MemoryAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.VOICE] = VoiceAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.VISION] = VisionAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.SECURITY] = SecurityAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.WORKFLOW] = WorkflowAgent(self.ai_router, self.tool_registry, self.permission_engine)
        self.agents[AgentType.PERSONAL_LEARNING] = PersonalLearningAgent(self.ai_router, self.tool_registry, self.permission_engine)

    async def select_best_agent(self, user_input: str) -> AgentType:
        """Route user query to the most appropriate specialized agent."""
        inp_lower = user_input.lower()

        if any(w in inp_lower for w in ["code", "react", "node", "npm", "python", "project", "build", "git"]):
            return AgentType.DEVELOPER
        elif any(w in inp_lower for w in ["open", "close", "launch", "battery", "telemetry", "file", "folder", "cpu", "ram"]):
            return AgentType.COMPUTER_CONTROL
        elif any(w in inp_lower for w in ["error", "fix", "issue", "bug", "fail", "wrong", "troubleshoot"]):
            return AgentType.TROUBLESHOOTING
        elif any(w in inp_lower for w in ["search", "find", "research", "what is", "documentation", "how to"]):
            return AgentType.RESEARCH
        elif any(w in inp_lower for w in ["remember", "preference", "forget", "memory", "know about me"]):
            return AgentType.MEMORY
        elif any(w in inp_lower for w in ["workflow", "automate", "routine", "shortcut"]):
            return AgentType.WORKFLOW
        elif any(w in inp_lower for w in ["call", "phone", "speak", "voice"]):
            return AgentType.COMMUNICATION

        return AgentType.GENERAL_ASSISTANT

    async def process_user_request(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        agent_type = await self.select_best_agent(user_input)
        agent = self.agents[agent_type]

        logger.info(f"Orchestrator assigned request to agent: '{agent_type.value}'")

        # Create multi-step plan
        task = await agent.plan_task(user_goal=user_input, context=context)

        # Execute first step
        execution_results = []
        requires_approval = False
        approval_id = None

        for step in task.steps:
            res = await agent.execute_step(task, step)
            execution_results.append(res)
            if res.get("requires_approval"):
                requires_approval = True
                approval_id = res.get("approval_id")
                task.status = "WAITING_APPROVAL"
                break

        if not requires_approval:
            verified = await agent.verify_task_outcome(task)
            task.status = "COMPLETED" if verified else "FAILED"
            
            # Record in Learning Engine
            self.learning_engine.capture_interaction_event(
                user_input=user_input,
                actions_taken=[s.dict() for s in task.steps],
                success=verified,
            )

        # Generate response synthesis
        context_memories = [m.dict() for m in self.memory_engine.list_all_memories()[:3]]
        user_profile = self.memory_engine.get_user_profile()

        response_prompt = (
            f"User Goal: {user_input}\n"
            f"Assigned Agent: {agent_type.value}\n"
            f"Task Steps Status: {[s.dict() for s in task.steps]}\n"
            f"User Profile: {user_profile}\n"
            f"Context Memories: {context_memories}\n"
            "Synthesize a clear, concise, and helpful response for the user explaining what was done or needed."
        )

        response_text = await self.ai_router.route_and_generate(
            prompt=response_prompt,
            system_prompt="You are SWITCH, an autonomous personal AI OS. Speak naturally, concisely, and directly.",
        )

        return {
            "task": task.dict(),
            "agent_type": agent_type.value,
            "response": response_text,
            "requires_approval": requires_approval,
            "approval_id": approval_id,
            "current_state": AgentState.WAITING.value if requires_approval else AgentState.SUCCESS.value,
        }
