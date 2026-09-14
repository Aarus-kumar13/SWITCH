import uuid
import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Callable, Optional

logger = logging.getLogger("switch.workflows.runner")

class ScheduledTask:
    def __init__(self, id: str, name: str, interval_seconds: int, action: Callable, is_recurring: bool = True):
        self.id = id
        self.name = name
        self.interval_seconds = interval_seconds
        self.action = action
        self.is_recurring = is_recurring
        self.last_run: Optional[datetime] = None
        self.run_count = 0


class WorkflowRunner:
    def __init__(self):
        self.tasks: Dict[str, ScheduledTask] = {}
        self.running = False

    def schedule_task(self, name: str, interval_seconds: int, action: Callable, is_recurring: bool = True) -> str:
        task_id = f"wf_{uuid.uuid4().hex[:8]}"
        st = ScheduledTask(task_id, name, interval_seconds, action, is_recurring)
        self.tasks[task_id] = st
        logger.info(f"Scheduled workflow task '{name}' (ID: {task_id}) every {interval_seconds}s")
        return task_id

    async def start(self):
        self.running = True
        logger.info("WorkflowRunner background daemon started.")
        while self.running:
            now = datetime.utcnow()
            for st in list(self.tasks.values()):
                if st.last_run is None or (now - st.last_run).total_seconds() >= st.interval_seconds:
                    try:
                        logger.info(f"Executing workflow task: '{st.name}'")
                        if asyncio.iscoroutinefunction(st.action):
                            await st.action()
                        else:
                            st.action()
                        st.last_run = datetime.utcnow()
                        st.run_count += 1
                        if not st.is_recurring:
                            del self.tasks[st.id]
                    except Exception as e:
                        logger.error(f"Error in workflow task '{st.name}': {e}")
            await asyncio.sleep(1)

    def stop(self):
        self.running = False
        logger.info("WorkflowRunner daemon stopped.")
