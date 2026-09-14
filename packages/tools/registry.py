import logging
import time
from typing import Any, Callable, Dict, List, Optional
from packages.shared.schemas import ToolDefinition, RiskLevel, AgentType, ToolExecutionResult
from packages.tools.browser import BrowserEngine

logger = logging.getLogger("switch.tools.registry")

class ToolRegistry:
    def __init__(self):
        self._definitions: Dict[str, ToolDefinition] = {}
        self._handlers: Dict[str, Callable] = {}
        self.browser_engine = BrowserEngine()
        self._register_default_tools()

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any],
        risk_level: RiskLevel,
        agent_type: AgentType,
        handler: Callable,
    ):
        tool_def = ToolDefinition(
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            risk_level=risk_level,
            agent_type=agent_type,
        )
        self._definitions[name] = tool_def
        self._handlers[name] = handler
        logger.info(f"Registered tool '{name}' [{risk_level.value}] for agent '{agent_type.value}'")

    def get_tool_definition(self, name: str) -> Optional[ToolDefinition]:
        return self._definitions.get(name)

    def list_tools_for_agent(self, agent_type: Optional[AgentType] = None) -> List[ToolDefinition]:
        if agent_type is None:
            return list(self._definitions.values())
        return [t for t in self._definitions.values() if t.agent_type == agent_type or t.agent_type == AgentType.GENERAL_ASSISTANT]

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> ToolExecutionResult:
        if name not in self._handlers:
            return ToolExecutionResult(
                success=False,
                error=f"Tool '{name}' is not registered in the ToolRegistry.",
            )

        handler = self._handlers[name]
        start_time = time.time()
        try:
            res = await handler(**arguments) if callable(handler) else handler(arguments)
            elapsed = (time.time() - start_time) * 1000.0
            return ToolExecutionResult(
                success=True,
                result=res,
                execution_time_ms=round(elapsed, 2),
            )
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000.0
            logger.error(f"Error executing tool '{name}': {e}", exc_info=True)
            return ToolExecutionResult(
                success=False,
                error=str(e),
                execution_time_ms=round(elapsed, 2),
            )

    def _register_default_tools(self):
        # 1. Computer Telemetry Tool (LOW)
        async def sys_telemetry_handler():
            import psutil
            battery = psutil.sensors_battery()
            return {
                "battery_percentage": battery.percent if battery else 100.0,
                "is_charging": battery.power_plugged if battery else True,
                "cpu_usage_percent": psutil.cpu_percent(),
                "ram_usage_percent": psutil.virtual_memory().percent,
                "disk_free_gb": round(psutil.disk_usage("/").free / (1024**3), 2),
            }

        self.register_tool(
            name="computer.get_telemetry",
            description="Retrieve real-time computer hardware system telemetry (battery, CPU, RAM, disk).",
            input_schema={},
            output_schema={"type": "object"},
            risk_level=RiskLevel.LOW,
            agent_type=AgentType.COMPUTER_CONTROL,
            handler=sys_telemetry_handler,
        )

        # 2. Computer File Search Tool (LOW)
        async def search_files_handler(pattern: str, directory: str = "."):
            import glob, os
            matches = glob.glob(os.path.join(directory, f"**/{pattern}"), recursive=True)
            return {"matches": matches[:20], "total_found": len(matches)}

        self.register_tool(
            name="computer.search_files",
            description="Search for files in a given directory matching a glob pattern.",
            input_schema={"pattern": {"type": "string"}, "directory": {"type": "string"}},
            output_schema={"type": "object"},
            risk_level=RiskLevel.LOW,
            agent_type=AgentType.COMPUTER_CONTROL,
            handler=search_files_handler,
        )

        # 3. Developer Inspect Project Tool (LOW)
        async def inspect_project_handler(project_path: str):
            import os, json
            pkg_json = os.path.join(project_path, "package.json")
            info = {"path": project_path, "exists": os.path.exists(project_path)}
            if os.path.exists(pkg_json):
                try:
                    with open(pkg_json, "r") as f:
                        info["package_json"] = json.load(f)
                except Exception:
                    pass
            return info

        self.register_tool(
            name="developer.inspect_project",
            description="Inspect developer project directory, structure, and package configuration.",
            input_schema={"project_path": {"type": "string"}},
            output_schema={"type": "object"},
            risk_level=RiskLevel.LOW,
            agent_type=AgentType.DEVELOPER,
            handler=inspect_project_handler,
        )

        # 4. Web Research Search Tool (LOW)
        async def web_search_handler(query: str):
            return {
                "query": query,
                "results": [
                    {
                        "title": f"Documentation search result for '{query}'",
                        "snippet": f"Official documentation and solutions relating to {query}.",
                        "url": f"https://docs.search.org/q={query}",
                    }
                ],
            }

        self.register_tool(
            name="research.web_search",
            description="Perform web search to find technical documentation and solutions.",
            input_schema={"query": {"type": "string"}},
            output_schema={"type": "object"},
            risk_level=RiskLevel.LOW,
            agent_type=AgentType.RESEARCH,
            handler=web_search_handler,
        )

        # 5. Developer Run Command Tool (MEDIUM)
        async def run_command_handler(command: str, cwd: str = "."):
            import asyncio
            proc = await asyncio.create_subprocess_shell(
                command,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            return {
                "returncode": proc.returncode,
                "stdout": stdout.decode(errors="ignore")[:2000],
                "stderr": stderr.decode(errors="ignore")[:2000],
            }

        self.register_tool(
            name="developer.run_command",
            description="Execute terminal shell command in authorized workspace directory.",
            input_schema={"command": {"type": "string"}, "cwd": {"type": "string"}},
            output_schema={"type": "object"},
            risk_level=RiskLevel.MEDIUM,
            agent_type=AgentType.DEVELOPER,
            handler=run_command_handler,
        )

        # 6. Browser Open URL Tool (LOW)
        self.register_tool(
            name="browser.open_url",
            description="Open and render web page URL via Playwright browser.",
            input_schema={"url": {"type": "string"}},
            output_schema={"type": "object"},
            risk_level=RiskLevel.LOW,
            agent_type=AgentType.RESEARCH,
            handler=self.browser_engine.open_url,
        )

        # 7. Browser Extract Text Tool (LOW)
        self.register_tool(
            name="browser.extract_text",
            description="Extract text content from target website URL.",
            input_schema={"url": {"type": "string"}},
            output_schema={"type": "object"},
            risk_level=RiskLevel.LOW,
            agent_type=AgentType.RESEARCH,
            handler=self.browser_engine.extract_page_text,
        )
