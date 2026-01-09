import os
from fastmcp import FastMCP
from smithery.decorators import smithery
from dotenv import load_dotenv

from .tools.google_auth import get_credentials
from .tools.calendar_tools import register_calendar_tools

# 로컬 .env 및 Smithery 환경 변수 통합 지원
load_dotenv()

@smithery.server()
def app():
    # 서버 실행 즉시 Google Calendar OAuth 인증 팝업 실행
    print("🚀 Google 통합 시스템 인증 확인 중...")
    try:
        get_credentials()
    except Exception as e:
        print(f"❌ 인증 실패: {e}")

    mcp = FastMCP("Schedule MCP(GOOGLE CALENDAR)")
    
    # 캘린더 기반 통합 도구 등록 (일정 + 메모)
    register_calendar_tools(mcp)
    
    return mcp

mcp = app()