import os
import sys
# 1. 인코딩 및 출력 채널 강제 고정
os.environ['PYTHONIOENCODING'] = 'utf-8'

import logging
from typing import Optional
from fastmcp import FastMCP
from smithery.decorators import smithery
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 로컬 환경 변수 로드 (파일 없어도 무시됨)
load_dotenv()

class SmartManagerConfig(BaseModel):
    """스마트 스케줄 매니저의 인증 및 서비스 설정을 정의합니다."""
    GOOGLE_CLIENT_ID: Optional[str] = Field(None)
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(None)
    SENDER_EMAIL: Optional[str] = Field(None)
    SENDER_PASSWORD: Optional[str] = Field(None)
    SMITHERY_KEY: Optional[str] = Field(None)

@smithery.server(config_schema=SmartManagerConfig)
def app(config: SmartManagerConfig = None):
    # 2. 모든 로그는 stderr로 출력 (print 대신 sys.stderr.write 사용)
    sys.stderr.write("DEBUG: [SSAFY-Style] Initializing Server...\n")
    
    # FastMCP 인스턴스 생성
    mcp = FastMCP("Smart Schedule Manager")

    # 3. 환경변수 동기화 (Smithery 대시보드 변수 -> 시스템 환경변수)
    if config:
        config_dict = config.model_dump(exclude_none=True)
        for key, value in config_dict.items():
            os.environ[key] = str(value)
            sys.stderr.write(f"DEBUG: Config Mapping -> {key}\n")

    # 4. 경로 문제 완벽 해결
    # 현재 파일이 있는 todo_server 폴더를 검색 경로에 추가
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    
    # 루트 디렉토리도 추가 (상위 폴더 참조 대비)
    root_dir = os.path.dirname(current_dir)
    if root_dir not in sys.path:
        sys.path.append(root_dir)

    # 5. 도구 등록 (Import 에러 및 실행 에러 방어)
    try:
        # 경로를 명시적으로 지정하여 임포트
        from .tools.calendar_tools import register_calendar_tools
        from .tools.helper import register_helper_tools
        
        register_calendar_tools(mcp)
        register_helper_tools(mcp)
        sys.stderr.write("DEBUG: All tools registered successfully.\n")
    except Exception as e:
        # 에러가 나도 '서버 프로세스'는 살려둬야 스캔이 성공합니다.
        sys.stderr.write(f"ERROR during Scan/Registration: {str(e)}\n")

    return mcp

if __name__ == "__main__":
    # Smithery 외부 실행 시 (로컬 테스트용)
    from fastmcp import FastMCP
    mcp_instance = app()
    mcp_instance.run()