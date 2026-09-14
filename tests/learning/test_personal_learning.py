import pytest
from packages.memory.engine import MemoryEngine
from packages.learning.engine import PersonalLearningEngine

def test_personal_learning_pattern_detection():
    mem_engine = MemoryEngine()
    learning_engine = PersonalLearningEngine(memory_engine=mem_engine)

    # Simulate repeated interaction
    for _ in range(4):
        learning_engine.capture_interaction_event(
            user_input="Start React Project",
            actions_taken=[{"tool": "developer.inspect_project"}],
            success=True,
        )

    candidates = learning_engine.get_candidate_workflows_for_approval()
    assert len(candidates) >= 1
    assert candidates[0]["pattern"] == "start react project"

def test_explicit_user_correction():
    mem_engine = MemoryEngine()
    learning_engine = PersonalLearningEngine(memory_engine=mem_engine)

    learning_engine.handle_explicit_correction("create python script", "use java instead")
    mem = mem_engine.get_semantic_memory("correction_create_python_script")
    assert mem is not None
    assert mem.value == "use java instead"
