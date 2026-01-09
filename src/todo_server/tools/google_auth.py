import os
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from ..database import get_path

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    token_path = get_path("google_token.json")
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ 환경 변수 미설정: GOOGLE_CLIENT_ID/SECRET", file=sys.stderr)
        return None

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    # 인증이 안 되어 있을 때만 브라우저 시도
    if not creds or not creds.valid:
        # Smithery 스캔 환경(브라우저 없음)에서는 여기서 에러를 내고 넘어가야 스캔이 성공함
        if os.getenv("SMITHERY_SCANNING") == "true":
            print("🔍 Smithery 스캔 모드: 인증 시도를 건너뜁니다.", file=sys.stderr)
            return None
            
        try:
            client_config = {
                "installed": {
                    "client_id": client_id, "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            }
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            print(f"❌ 인증 실패: {e}", file=sys.stderr)
            return None
    return creds