import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from ..database import get_path

# 구글 캘린더 전용 권한 범위
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    """OAuth 인증을 수행하고 자격 증명을 반환합니다."""
    token_path = get_path("google_token.json")
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError("⚠️ GOOGLE_CLIENT_ID 및 GOOGLE_CLIENT_SECRET 환경 변수가 필요합니다.")

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    if not creds or not creds.valid:
        client_config = {
            "installed": {
                "client_id": client_id, "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0) # 브라우저 실행
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds