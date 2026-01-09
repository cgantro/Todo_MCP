import os
import sys
from typing import Optional
from fastmcp import FastMCP
from smithery.decorators import smithery
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 도구 등록 함수 임포트
from .tools.calendar_tools import register_calendar_tools
from .tools.helper import register_helper_tools

load_dotenv()

class SmartManagerConfig(BaseModel):
    GOOGLE_CLIENT_ID: Optional[str] = Field(None, description="Google OAuth Client ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(None, description="Google OAuth Client Secret")
    SENDER_EMAIL: Optional[str] = Field(None, description="Sender's Gmail address")
    SENDER_PASSWORD: Optional[str] = Field(None, description="Gmail App Password")
    SMITHERY_KEY: Optional[str] = Field(None, description="Smithery API Key")

@smithery.server(config_schema=SmartManagerConfig)
def app(config: SmartManagerConfig = None):
    # 1. 객체 생성 및 도구 무조건 등록 (스캔 시 목록 노출용)
    mcp = FastMCP("Smart Schedule Manager")
    register_calendar_tools(mcp)
    register_helper_tools(mcp)

    # 2. 스캔 단계일 경우 환경변수 없이 반환
    if config is None or config.GOOGLE_CLIENT_ID is None:
        os.environ["SMITHERY_SCANNING"] = "true"
        return mcp

    # 3. 실제 실행 단계: 환경변수 주입
    os.environ["SMITHERY_SCANNING"] = "false"
    os.environ["GOOGLE_CLIENT_ID"] = config.GOOGLE_CLIENT_ID
    os.environ["GOOGLE_CLIENT_SECRET"] = config.GOOGLE_CLIENT_SECRET
    os.environ["SENDER_EMAIL"] = config.SENDER_EMAIL
    os.environ["SENDER_PASSWORD"] = config.SENDER_PASSWORD
    os.environ["SMITHERY_KEY"] = config.SMITHERY_KEY

    print("🚀 서버가 환경변수와 함께 로드되었습니다.", file=sys.stderr)
    return mcp


if __name__ == "__main__":
    # 로컬에서 실행할 때는 Smithery가 주입해주는 config가 없으므로 
    # .env 파일 등에서 읽어온 값으로 가짜 config 객체를 만들어 넘깁니다.
    from pydantic import ValidationError
    
    try:
        # 로컬 환경변수를 기반으로 config 객체 생성
        local_config = SmartManagerConfig(
            GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID"),
            GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET"),
            SENDER_EMAIL=os.getenv("SENDER_EMAIL"),
            SENDER_PASSWORD=os.getenv("SENDER_PASSWORD"),
            SMITHERY_KEY=os.getenv("SMITHERY_KEY")
        )
        
        # 서버 인스턴스 생성 및 실행
        server_instance = app(local_config)
        server_instance.run() # FastMCP 서버 실행
        
    except ValidationError as e:
        print(f"❌ 로컬 설정 오류: {e}", file=sys.stderr)
        print("💡 .env 파일에 필요한 환경변수가 모두 있는지 확인하세요.", file=sys.stderr)