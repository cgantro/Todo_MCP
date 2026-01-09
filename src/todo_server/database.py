import os
from pathlib import Path

USER_DATA_DIR = Path.cwd() / ".smart_mcp_data"
USER_DATA_DIR.mkdir(exist_ok=True)

def get_path(filename: str) -> Path:
    return USER_DATA_DIR / filename