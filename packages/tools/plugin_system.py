import logging
from typing import Any, Callable, Dict, List, Optional
from packages.shared.schemas import RiskLevel, AgentType

logger = logging.getLogger("switch.tools.plugin_system")

class BasePlugin:
    def __init__(self, name: str, version: str, description: str):
        self.name = name
        self.version = version
        self.description = description
        self.tools: List[Dict[str, Any]] = []

    def register_action(
        self,
        action_name: str,
        description: str,
        risk_level: RiskLevel,
        handler: Callable,
    ):
        self.tools.append({
            "name": f"plugin.{self.name}.{action_name}",
            "description": description,
            "risk_level": risk_level,
            "handler": handler,
        })
        logger.info(f"Plugin '{self.name}' registered action '{action_name}' [{risk_level.value}]")


class PluginMarketplace:
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}

    def install_plugin(self, plugin: BasePlugin):
        self.plugins[plugin.name] = plugin
        logger.info(f"Installed plugin '{plugin.name}' (v{plugin.version}) into SWITCH engine.")

    def list_installed_plugins(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": p.name,
                "version": p.version,
                "description": p.description,
                "tool_count": len(p.tools),
            }
            for p in self.plugins.values()
        ]
