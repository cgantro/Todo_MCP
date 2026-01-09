import os
import sys
import warnings
from fastmcp import FastMCP
from smithery.decorators import smithery
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional
# httplib2 경고 메시지가 거슬린다면 추가 (선택사항)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from .tools.calendar_tools import register_calendar_tools
from .tools.helper import register_helper_tools

load_dotenv()


class SmartManagerConfig(BaseModel):
    # Field(None, ...)으로 설정하여 스캔 시점에 값이 없어도 터지지 않게 합니다.
    GOOGLE_CLIENT_ID: Optional[str] = Field(None, description="Google OAuth Client ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(None, description="Google OAuth Client Secret")
    SENDER_EMAIL: Optional[str] = Field(None, description="Sender's Gmail address")
    SENDER_PASSWORD: Optional[str] = Field(None, description="Gmail App Password")
    SMITHERY_KEY: Optional[str] = Field(None, description="Smithery API Key")

@smithery.server(config_schema=SmartManagerConfig)
def app(config: SmartManagerConfig = None):
    # Smithery가 스키마만 확인하러 온 경우 (config가 None이거나 필드가 비어있음)
    if config is None or config.GOOGLE_CLIENT_ID is None:
        # 빈 도구 목록이라도 가진 MCP 객체를 반환해야 스캔이 성공합니다.
        return FastMCP("Smart Schedule Manager")

    # 실제 실행 시점 (환경변수가 주입됨)
    mcp = FastMCP("Smart Schedule Manager")
    register_calendar_tools(mcp)
    register_helper_tools(mcp)
    
    return mcp

# ⚠️ mcp = app() 호출은 반드시 제거 상태를 유지하세요.