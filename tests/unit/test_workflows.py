import pytest
import asyncio
from packages.workflows.runner import WorkflowRunner

@pytest.mark.asyncio
async def test_workflow_runner():
    runner = WorkflowRunner()
    executed = []

    def mock_action():
        executed.append("done")

    task_id = runner.schedule_task("test_battery_check", interval_seconds=1, action=mock_action, is_recurring=False)
    assert task_id in runner.tasks

    # Run loop briefly
    runner_task = asyncio.create_task(runner.start())
    await asyncio.sleep(1.5)
    runner.stop()
    await runner_task

    assert "done" in executed
