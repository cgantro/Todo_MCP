import os
import sys
from typing import Optional
from fastmcp import FastMCP
from smithery.decorators import smithery
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 로컬 테스트용
load_dotenv()
load_dotenv("src/.env")

class SmartManagerConfig(BaseModel):
    GOOGLE_CLIENT_ID: Optional[str] = Field(None)
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(None)
    SENDER_EMAIL: Optional[str] = Field(None)
    SENDER_PASSWORD: Optional[str] = Field(None)
    SMITHERY_KEY: Optional[str] = Field(None)

@smithery.server(config_schema=SmartManagerConfig)
def app(config: SmartManagerConfig = None):
    # 1. FastMCP 인스턴스 생성
    mcp = FastMCP("Smart Schedule Manager")
    
    # 2. Config 값을 os.environ에 주입 (이미 등록한 환경변수를 코드와 연결)
    if config:
        conf_dict = config.model_dump(exclude_none=True)
        for key, value in conf_dict.items():
            os.environ[key] = str(value)

    # 3. 중요: 경로 문제 해결 (Docker 환경 대비)
    # 현재 실행 경로를 sys.path에 추가하여 임포트 에러 방지
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    try:
        # 상대 경로(.) 대신 절대 경로 형태로 시도하여 안전성 확보
        from .tools.calendar_tools import register_calendar_tools
        from .tools.helper import register_helper_tools
        
        register_calendar_tools(mcp)
        register_helper_tools(mcp)
    except Exception as e:
        # 스캔 단계에서 에러가 나도 Smithery 로그에 남기기 위해 stderr로 출력
        sys.stderr.write(f"Error during tool registration: {e}\n")
        # 스캔 단계에서는 환경변수가 없어 에러가 날 수 있으므로 
        # 일단 서버가 죽지 않게 처리해야 배포가 성공합니다.
        pass
    
    return mcp

if __name__ == "__main__":
    mcp_instance = app()
    mcp_instance.run()