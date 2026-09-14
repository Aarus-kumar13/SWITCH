import uuid
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from packages.shared.schemas import LearnedWorkflow, MemoryItem
from packages.memory.engine import MemoryEngine

logger = logging.getLogger("switch.learning.engine")

class PersonalLearningEngine:
    def __init__(self, memory_engine: MemoryEngine):
        self.memory_engine = memory_engine
        self.action_history: List[Dict[str, Any]] = []
        self.detected_patterns: Dict[str, Dict[str, Any]] = {}
        self.learned_workflows: Dict[str, LearnedWorkflow] = {}
        self._initialize_default_workflows()

    def _initialize_default_workflows(self):
        wf1 = LearnedWorkflow(
            id=str(uuid.uuid4()),
            name="Start React Project",
            description="Opens project in VS Code, installs dependencies if needed, starts dev server, and opens localhost browser.",
            trigger_command="start react project",
            steps=[
                {"tool": "computer.open_application", "args": {"application": "VS Code"}},
                {"tool": "developer.inspect_project", "args": {"project_path": "."}},
                {"tool": "developer.run_command", "args": {"command": "npm run dev", "cwd": "."}},
            ],
            confidence=0.95,
            user_approved=True,
        )
        self.learned_workflows[wf1.name] = wf1

    def capture_interaction_event(
        self,
        user_input: str,
        actions_taken: List[Dict[str, Any]],
        success: bool,
        user_feedback: Optional[str] = None,
    ):
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_input": user_input,
            "actions": actions_taken,
            "success": success,
            "feedback": user_feedback,
        }
        self.action_history.append(event)
        self._analyze_patterns()

    def handle_explicit_correction(self, original_action: str, correction: str):
        """Process explicit user correction as high-value learning signal."""
        logger.info(f"Learning from user correction: '{original_action}' -> '{correction}'")
        key = f"correction_{original_action.lower().replace(' ', '_')}"
        self.memory_engine.set_semantic_memory(
            key=key,
            value=correction,
            category="correction_preference",
            user_confirmed=True,
        )

    def _analyze_patterns(self):
        """Implicit pattern detection for sequence repetition."""
        if len(self.action_history) < 3:
            return

        # Check for repeated recent action sequences
        recent_inputs = [e["user_input"].lower().strip() for e in self.action_history[-10:]]
        from collections import Counter
        counts = Counter(recent_inputs)

        for input_text, count in counts.items():
            if count >= 3 and input_text not in self.detected_patterns:
                self.detected_patterns[input_text] = {
                    "pattern": input_text,
                    "occurrences": count,
                    "suggested_workflow": True,
                    "confidence": min(0.95, round(0.5 + (count * 0.1), 2)),
                }
                logger.info(f"Pattern detected: '{input_text}' repeated {count} times.")

    def get_candidate_workflows_for_approval(self) -> List[Dict[str, Any]]:
        """Return detected patterns that are eligible for user confirmation."""
        return [
            p for p in self.detected_patterns.values()
            if p.get("suggested_workflow") and p.get("confidence", 0) >= 0.80
        ]

    def create_workflow_from_pattern(self, name: str, trigger_command: str, steps: List[Dict[str, Any]]) -> LearnedWorkflow:
        wf = LearnedWorkflow(
            id=str(uuid.uuid4()),
            name=name,
            description=f"Automated workflow learned from repeated user activity for '{trigger_command}'.",
            trigger_command=trigger_command,
            steps=steps,
            confidence=1.0,
            user_approved=True,
        )
        self.learned_workflows[name] = wf
        logger.info(f"Formalized new learned workflow: '{name}'")
        return wf

    def get_learned_workflows(self) -> List[LearnedWorkflow]:
        return list(self.learned_workflows.values())

    def get_learning_summary(self) -> Dict[str, Any]:
        return {
            "total_interactions_analyzed": len(self.action_history),
            "detected_patterns_count": len(self.detected_patterns),
            "learned_workflows_count": len(self.learned_workflows),
            "active_preferences_count": len(self.memory_engine.list_all_memories()),
        }
