import os
import sys
from typing import Optional
from fastmcp import FastMCP
from smithery.decorators import smithery
from pydantic import BaseModel, Field
# load_dotenv는 여기서 지웁니다.

from .tools.calendar_tools import register_calendar_tools
from .tools.helper import register_helper_tools

class SmartManagerConfig(BaseModel):
    GOOGLE_CLIENT_ID: Optional[str] = Field(None, description="Google OAuth Client ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(None, description="Google OAuth Client Secret")
    SENDER_EMAIL: Optional[str] = Field(None, description="Sender's Gmail address")
    SENDER_PASSWORD: Optional[str] = Field(None, description="Gmail App Password")
    SMITHERY_KEY: Optional[str] = Field(None, description="Smithery API Key")

@smithery.server(config_schema=SmartManagerConfig)
def app(config: SmartManagerConfig = None):
    mcp = FastMCP("Smart Schedule Manager")
    register_calendar_tools(mcp)
    register_helper_tools(mcp)

    # 1. Smithery 스캔(Discovery) 단계
    if config is None or config.GOOGLE_CLIENT_ID is None:
        # 스캔 시에는 실제 도구 로직이 실행되지 않으므로 환경 변수 주입 없이 mcp 객체만 반환
        os.environ["SMITHERY_SCANNING"] = "true"
        return mcp

    # 2. 실제 실행 단계: Smithery 대시보드에서 주입된 config 값을 시스템 환경 변수로 매핑
    os.environ["SMITHERY_SCANNING"] = "false"
    os.environ["GOOGLE_CLIENT_ID"] = str(config.GOOGLE_CLIENT_ID or "")
    os.environ["GOOGLE_CLIENT_SECRET"] = str(config.GOOGLE_CLIENT_SECRET or "")
    os.environ["SENDER_EMAIL"] = str(config.SENDER_EMAIL or "")
    os.environ["SENDER_PASSWORD"] = str(config.SENDER_PASSWORD or "")
    os.environ["SMITHERY_KEY"] = str(config.SMITHERY_KEY or "")

    # 모든 로그는 stderr로 출력하여 Smithery 연결 오염 방지
    print("🚀 Smithery 주입 설정으로 서버가 로드되었습니다.", file=sys.stderr)
    return mcp

# 로컬 실행 시에만 환경 변수 로드 및 서버 가동
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # 로컬에서만 .env 파일을 읽습니다.
    
    local_config = SmartManagerConfig(
        GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID"),
        GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET"),
        SENDER_EMAIL=os.getenv("SENDER_EMAIL"),
        SENDER_PASSWORD=os.getenv("SENDER_PASSWORD"),
        SMITHERY_KEY=os.getenv("SMITHERY_KEY")
    )
    
    server_instance = app(local_config)
    server_instance.run()