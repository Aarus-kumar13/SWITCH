import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from packages.shared.schemas import RiskLevel, AuditLogEntry, AgentType

logger = logging.getLogger("switch.permissions.engine")

class SecurityPolicy(str):
    ALWAYS_ASK = "ALWAYS_ASK"
    ASK_FOR_RISKY = "ASK_FOR_RISKY"
    TRUSTED = "TRUSTED"
    NEVER_ALLOW = "NEVER_ALLOW"

class PermissionEngine:
    def __init__(self, policy: str = SecurityPolicy.ASK_FOR_RISKY):
        self.policy = policy
        self.pending_approvals: Dict[str, Dict[str, Any]] = {}
        self.audit_logs: List[AuditLogEntry] = []

    def classify_risk(self, tool_name: str, arguments: Dict[str, Any]) -> RiskLevel:
        """Categorize tool calls into LOW, MEDIUM, or HIGH risk level based on specification."""
        t_name = tool_name.lower()

        # HIGH Risk Actions
        high_risk_actions = ["delete", "remove", "financial", "security", "privileges", "install_system"]
        if any(h in t_name for h in high_risk_actions):
            return RiskLevel.HIGH
        
        # Check arguments for dangerous commands/paths
        arg_str = str(arguments).lower()
        if "rm -rf" in arg_str or "del /s" in arg_str or "format" in arg_str:
            return RiskLevel.HIGH

        # MEDIUM Risk Actions
        medium_risk_actions = ["modify_file", "create_file", "run_command", "send_email", "send_message", "schedule_meeting"]
        if any(m in t_name for m in medium_risk_actions):
            return RiskLevel.MEDIUM

        # LOW Risk Actions
        return RiskLevel.LOW

    async def evaluate_and_authorize(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        agent_type: AgentType,
        reasoning_summary: str,
        user_command: str = "",
    ) -> Dict[str, Any]:
        risk_level = self.classify_risk(tool_name, arguments)
        
        # LOW Risk: Auto-approved
        if risk_level == RiskLevel.LOW or self.policy == SecurityPolicy.TRUSTED:
            audit_id = self.log_action(
                user_command=user_command,
                agent_selected=agent_type,
                reasoning_summary=reasoning_summary,
                tool_used=tool_name,
                risk_level=risk_level,
                execution_result="AUTO_APPROVED",
            )
            return {"authorized": True, "risk_level": risk_level, "audit_id": audit_id, "requires_user_approval": False}

        # MEDIUM & HIGH Risk: Require Human Approval depending on Policy
        if self.policy in [SecurityPolicy.ALWAYS_ASK, SecurityPolicy.ASK_FOR_RISKY]:
            approval_id = str(uuid.uuid4())
            approval_request = {
                "approval_id": approval_id,
                "tool_name": tool_name,
                "arguments": arguments,
                "agent_type": agent_type,
                "risk_level": risk_level,
                "reasoning_summary": reasoning_summary,
                "user_command": user_command,
                "status": "PENDING",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            self.pending_approvals[approval_id] = approval_request
            logger.info(f"Created approval checkpoint {approval_id} for {tool_name} [{risk_level}]")
            
            return {
                "authorized": False,
                "risk_level": risk_level,
                "approval_id": approval_id,
                "requires_user_approval": True,
                "message": f"Action '{tool_name}' classified as {risk_level} risk requires human confirmation.",
            }

        # NEVER_ALLOW fallback
        return {"authorized": False, "risk_level": risk_level, "requires_user_approval": False, "message": "Policy blocks execution."}

    def confirm_action(self, approval_id: str, approved: bool) -> Optional[Dict[str, Any]]:
        if approval_id not in self.pending_approvals:
            return None
        
        request = self.pending_approvals.pop(approval_id)
        request["status"] = "APPROVED" if approved else "REJECTED"
        
        self.log_action(
            user_command=request["user_command"],
            agent_selected=request["agent_type"],
            reasoning_summary=request["reasoning_summary"],
            tool_used=request["tool_name"],
            risk_level=request["risk_level"],
            execution_result="USER_APPROVED" if approved else "USER_REJECTED",
        )
        return request

    def log_action(
        self,
        user_command: str,
        agent_selected: AgentType,
        reasoning_summary: str,
        tool_used: str,
        risk_level: RiskLevel,
        execution_result: str,
        error: Optional[str] = None,
    ) -> str:
        entry_id = str(uuid.uuid4())
        entry = AuditLogEntry(
            id=entry_id,
            user_command=user_command,
            agent_selected=agent_selected,
            reasoning_summary=reasoning_summary,
            tool_used=tool_used,
            risk_level=risk_level,
            execution_result=execution_result,
            error=error,
            timestamp=datetime.now(timezone.utc),
        )
        self.audit_logs.append(entry)
        return entry_id

    def get_recent_audit_logs(self, limit: int = 50) -> List[AuditLogEntry]:
        return sorted(self.audit_logs, key=lambda x: x.timestamp, reverse=True)[:limit]
