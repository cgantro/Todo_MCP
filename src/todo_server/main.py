import os
import sys
from fastmcp import FastMCP
from smithery.decorators import smithery
from dotenv import load_dotenv

from .tools.google_auth import get_credentials
from .tools.calendar_tools import register_calendar_tools
from .tools.helper import register_helper_tools

# .env 로드
load_dotenv()

@smithery.server()
def app():
    # 로그는 stdout이 아닌 stderr로 출력해야 MCP 연결이 깨지지 않습니다.
    print("🚀 Google 캘린더 시스템 초기화 중...", file=sys.stderr)
    
    # Smithery 스캔 시에는 인증을 건너뛰도록 처리 (인터랙티브 브라우저 차단 방지)
    # 실제 Claude Desktop에서 실행될 때는 인증이 작동합니다.
    if os.getenv("SMITHERY_SCANNING") != "true":
        try:
            get_credentials()
        except Exception as e:
            print(f"❌ 초기 인증 시도 중 오류 (사용 시 재시도): {e}", file=sys.stderr)

    mcp = FastMCP("Google Calendar Smart Manager")
    
    # 도구 등록
    register_calendar_tools(mcp)
    register_helper_tools(mcp)
    
    return mcp

mcp = app()