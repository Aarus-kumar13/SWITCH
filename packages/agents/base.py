import uuid
import logging
from abc import ABC
from typing import Any, Dict, List, Optional
from packages.shared.schemas import AgentType, AgentTask, AgentTaskStep, ToolExecutionResult, RiskLevel
from packages.ai.router import AIRouter
from packages.tools.registry import ToolRegistry
from packages.permissions.engine import PermissionEngine

logger = logging.getLogger("switch.agents.base")

class BaseAgent(ABC):
    def __init__(
        self,
        agent_type: AgentType,
        ai_router: AIRouter,
        tool_registry: ToolRegistry,
        permission_engine: PermissionEngine,
    ):
        self.agent_type = agent_type
        self.ai_router = ai_router
        self.tool_registry = tool_registry
        self.permission_engine = permission_engine

    async def plan_task(self, user_goal: str, context: Optional[Dict[str, Any]] = None) -> AgentTask:
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        prompt = (
            f"User Goal: {user_goal}\n"
            f"Context: {context or {}}\n"
            "Create a multi-step plan to achieve this goal. List each step clearly."
        )
        sys_prompt = f"You are the SWITCH {self.agent_type.value.upper()} Agent. Formulate structured execution steps."
        
        plan_res = await self.ai_router.route_and_generate_structured(
            prompt=prompt,
            system_prompt=sys_prompt,
            response_schema={
                "steps": [{"step_index": "int", "description": "str", "tool_name": "str"}]
            },
        )

        steps = []
        raw_steps = plan_res.get("steps") or [
            {"step_index": 1, "description": f"Analyze and prepare for: {user_goal}", "tool_name": None},
            {"step_index": 2, "description": f"Execute authorized tools for: {user_goal}", "tool_name": None},
            {"step_index": 3, "description": "Verify result and confirm completion", "tool_name": None},
        ]

        for s in raw_steps:
            steps.append(
                AgentTaskStep(
                    step_index=s.get("step_index", len(steps) + 1),
                    agent_name=self.agent_type.value,
                    action_description=s.get("description", "Execute step"),
                    tool_name=s.get("tool_name"),
                )
            )

        task = AgentTask(
            task_id=task_id,
            user_goal=user_goal,
            assigned_agent=self.agent_type,
            steps=steps,
            status="IN_PROGRESS",
        )
        return task

    async def execute_step(
        self,
        task: AgentTask,
        step: AgentTaskStep,
        tool_args: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        step.status = "EXECUTING"
        tool_name = step.tool_name

        if not tool_name:
            step.status = "COMPLETED"
            step.result_summary = "Step processed conceptually without tool invocation."
            return {"success": True, "step": step}

        # Permission check
        auth_res = await self.permission_engine.evaluate_and_authorize(
            tool_name=tool_name,
            arguments=tool_args or {},
            agent_type=self.agent_type,
            reasoning_summary=step.action_description,
            user_command=task.user_goal,
        )

        if not auth_res.get("authorized"):
            step.status = "WAITING_APPROVAL"
            step.result_summary = f"Requires user approval ({auth_res.get('risk_level')} risk)."
            return {
                "success": False,
                "requires_approval": True,
                "approval_id": auth_res.get("approval_id"),
                "step": step,
            }

        # Tool execution
        tool_result: ToolExecutionResult = await self.tool_registry.execute_tool(
            name=tool_name,
            arguments=tool_args or {},
        )

        if tool_result.success:
            step.status = "COMPLETED"
            step.result_summary = f"Execution successful: {str(tool_result.result)[:150]}"
        else:
            step.status = "FAILED"
            step.result_summary = f"Execution failed: {tool_result.error}"

        return {"success": tool_result.success, "result": tool_result, "step": step}

    async def verify_task_outcome(self, task: AgentTask) -> bool:
        """Self-verification engine to ensure task completion criteria are met."""
        completed_count = sum(1 for s in task.steps if s.status == "COMPLETED")
        return completed_count == len(task.steps)
