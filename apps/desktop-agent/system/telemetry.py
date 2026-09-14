import psutil
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger("switch.desktop.telemetry")

class TelemetryCollector:
    @staticmethod
    def get_system_telemetry() -> Dict[str, Any]:
        """Collect real-time system metrics (Battery, CPU, RAM, Disk, Active Window)."""
        battery = psutil.sensors_battery()
        battery_pct = battery.percent if battery else 100.0
        is_charging = battery.power_plugged if battery else True
        
        cpu_pct = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        active_window = "VS Code - SWITCH-OS"
        try:
            import pygetwindow as gw
            win = gw.getActiveWindow()
            if win and win.title:
                active_window = win.title
        except Exception:
            pass

        telemetry = {
            "battery_percentage": round(battery_pct, 1),
            "is_charging": is_charging,
            "cpu_usage_percent": round(cpu_pct, 1),
            "ram_usage_percent": round(ram.percent, 1),
            "disk_free_gb": round(disk.free / (1024**3), 2),
            "active_window_title": active_window,
            "running_processes_count": len(psutil.pids()),
            "timestamp": datetime.utcnow().isoformat(),
        }
        return telemetry
