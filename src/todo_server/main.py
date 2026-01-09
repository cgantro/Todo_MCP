import os
import sys
from fastmcp import FastMCP
from smithery.decorators import smithery
from dotenv import load_dotenv

# 도구 모듈 임포트
from .tools.calendar_tools import register_calendar_tools
from .tools.helper import register_helper_tools

load_dotenv()

@smithery.server()
def app():
    # 1. 스캔 시 stdout 오염 방지 (모든 로그는 stderr로)
    print("🚀 Smart Manager Server 준비 중...", file=sys.stderr)
    
    mcp = FastMCP("Smart Schedule Manager")

    # 2. 도구 등록 (인증과 상관없이 도구 정의는 보여줘야 스캔이 성공함)
    register_calendar_tools(mcp)
    register_helper_tools(mcp)
    
    # 3. 중요: 스캔 중에는 get_credentials()를 절대 호출하지 않음
    # 실제 Claude Desktop 등에서 사용자가 도구를 클릭할 때만 인증이 작동하게 됨
    
    return mcp

mcp = app()