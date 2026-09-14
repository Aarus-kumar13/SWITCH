import os
import glob
import subprocess
import logging
from typing import Any, Dict, List

logger = logging.getLogger("switch.desktop.os_tools")

class OSTools:
    @staticmethod
    def open_application(app_name: str) -> Dict[str, Any]:
        """Launch local application safely."""
        logger.info(f"Desktop Agent launching application: '{app_name}'")
        try:
            if os.name == "nt":  # Windows
                os.system(f"start {app_name}")
            elif os.name == "posix":
                subprocess.Popen(["open", "-a", app_name])
            return {"success": True, "application": app_name, "message": f"Successfully launched {app_name}."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def search_files(directory: str, pattern: str) -> Dict[str, Any]:
        try:
            search_path = os.path.join(directory, f"**/{pattern}")
            matches = glob.glob(search_path, recursive=True)
            return {"success": True, "matches": matches[:30], "count": len(matches)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def read_file_preview(file_path: str, max_lines: int = 100) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File '{file_path}' does not exist."}
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [f.readline() for _ in range(max_lines)]
            return {"success": True, "content": "".join(lines), "path": file_path}
        except Exception as e:
            return {"success": False, "error": str(e)}
