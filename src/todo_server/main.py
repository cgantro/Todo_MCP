import os
import sys
from typing import Optional
from fastmcp import FastMCP
from smithery.decorators import smithery
from pydantic import BaseModel, Field

# 1. 로컬 개발 시에만 .env를 읽도록 설정 (파일이 없어도 에러는 안 납니다)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class SmartManagerConfig(BaseModel):
    GOOGLE_CLIENT_ID: Optional[str] = Field(None)
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(None)
    SENDER_EMAIL: Optional[str] = Field(None)
    SENDER_PASSWORD: Optional[str] = Field(None)
    GOOGLE_TOKEN_DATA: Optional[str] = Field(None, description="google_token.json의 JSON 내용 전체")

@smithery.server(config_schema=SmartManagerConfig)
def app(config: SmartManagerConfig = None):
    mcp = FastMCP("Smart Schedule Manager")
    
    # 2. 배포 환경(Smithery): 대시보드에서 입력한 config를 os.environ에 주입
    if config:
        if config.GOOGLE_CLIENT_ID: os.environ["GOOGLE_CLIENT_ID"] = config.GOOGLE_CLIENT_ID
        if config.GOOGLE_CLIENT_SECRET: os.environ["GOOGLE_CLIENT_SECRET"] = config.GOOGLE_CLIENT_SECRET
        if config.SENDER_EMAIL: os.environ["SENDER_EMAIL"] = config.SENDER_EMAIL
        if config.SENDER_PASSWORD: os.environ["SENDER_PASSWORD"] = config.SENDER_PASSWORD
        if config.GOOGLE_TOKEN_DATA: os.environ["GOOGLE_TOKEN_DATA"] = config.GOOGLE_TOKEN_DATA

    from .tools.calendar_tools import register_calendar_tools
    from .tools.helper import register_helper_tools
    
    register_calendar_tools(mcp)
    register_helper_tools(mcp)
    
    return mcp