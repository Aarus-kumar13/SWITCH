import pytest
from packages.permissions.engine import PermissionEngine, SecurityPolicy
from packages.shared.schemas import RiskLevel, AgentType

@pytest.mark.asyncio
async def test_permission_risk_classification():
    engine = PermissionEngine(policy=SecurityPolicy.ASK_FOR_RISKY)

    # Low Risk
    res_low = await engine.evaluate_and_authorize(
        tool_name="computer.get_telemetry",
        arguments={},
        agent_type=AgentType.COMPUTER_CONTROL,
        reasoning_summary="Get battery telemetry",
    )
    assert res_low["authorized"] is True
    assert res_low["risk_level"] == RiskLevel.LOW

    # Medium Risk (Requires Approval)
    res_med = await engine.evaluate_and_authorize(
        tool_name="developer.run_command",
        arguments={"command": "npm run build"},
        agent_type=AgentType.DEVELOPER,
        reasoning_summary="Run npm build",
    )
    assert res_med["authorized"] is False
    assert res_med["requires_user_approval"] is True
    assert res_med["risk_level"] == RiskLevel.MEDIUM

    # Confirm action
    app_id = res_med["approval_id"]
    conf = engine.confirm_action(approval_id=app_id, approved=True)
    assert conf["status"] == "APPROVED"
