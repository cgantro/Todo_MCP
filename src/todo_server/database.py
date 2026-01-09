import os
from pathlib import Path

# 사용자의 홈 디렉토리에 전용 데이터 폴더 생성
USER_DATA_DIR = Path.home() / ".smart_mcp_data"
USER_DATA_DIR.mkdir(exist_ok=True)

def get_path(filename: str) -> Path:
    """데이터 파일의 전체 경로를 반환합니다."""
    return USER_DATA_DIR / filename