from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AgentState(str, Enum):
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    WAITING = "WAITING"
    CALLING = "CALLING"
    SPEAKING = "SPEAKING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class ModelCategory(str, Enum):
    FAST = "FAST"
    REASONING = "REASONING"
    VISION = "VISION"
    VOICE = "VOICE"
    EMBEDDING = "EMBEDDING"


class AgentType(str, Enum):
    ORCHESTRATOR = "orchestrator"
    GENERAL_ASSISTANT = "general_assistant"
    COMPUTER_CONTROL = "computer_control"
    DEVELOPER = "developer"
    RESEARCH = "research"
    TROUBLESHOOTING = "troubleshooting"
    COMMUNICATION = "communication"
    SCHEDULING = "scheduling"
    PRODUCTIVITY = "productivity"
    MEMORY = "memory"
    VOICE = "voice"
    VISION = "vision"
    SECURITY = "security"
    WORKFLOW = "workflow"
    PERSONAL_LEARNING = "personal_learning"


class UserMessage(BaseModel):
    id: str
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    multimodal_data: Optional[Dict[str, Any]] = None


class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    risk_level: RiskLevel
    agent_type: AgentType


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    agent_id: str
    reasoning: str


class ToolExecutionResult(BaseModel):
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    audit_id: Optional[str] = None


class AgentTaskStep(BaseModel):
    step_index: int
    agent_name: str
    action_description: str
    tool_name: Optional[str] = None
    arguments: Optional[Dict[str, Any]] = None
    status: str = "PENDING"  # PENDING, EXECUTING, COMPLETED, FAILED
    result_summary: Optional[str] = None


class AgentTask(BaseModel):
    task_id: str
    user_goal: str
    assigned_agent: AgentType
    steps: List[AgentTaskStep] = []
    status: str = "IN_PROGRESS"  # IN_PROGRESS, COMPLETED, FAILED, WAITING_APPROVAL
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SystemTelemetry(BaseModel):
    battery_percentage: float
    is_charging: bool
    cpu_usage_percent: float
    ram_usage_percent: float
    disk_free_gb: float
    active_window_title: str
    running_processes_count: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MemoryItem(BaseModel):
    id: str
    category: str  # "fact", "preference", "interaction", "workflow"
    key: str
    value: Any
    confidence: float = 1.0
    user_confirmed: bool = False
    observation_count: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class LearnedWorkflow(BaseModel):
    id: str
    name: str
    description: str
    trigger_command: str
    steps: List[Dict[str, Any]]
    confidence: float
    user_approved: bool
    execution_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PhoneCallRequest(BaseModel):
    to_phone_number: str
    context_summary: str
    initial_speech: str
    task_id: Optional[str] = None


class AuditLogEntry(BaseModel):
    id: str
    user_command: str
    agent_selected: AgentType
    reasoning_summary: str
    tool_used: str
    risk_level: RiskLevel
    execution_result: str
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
