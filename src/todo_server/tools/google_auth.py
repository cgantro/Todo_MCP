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
        # 로그는 반드시 stderr로 출력
        print("⚠️ 환경 변수(CLIENT_ID/SECRET)가 설정되지 않았습니다.", file=sys.stderr)
        return None

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    if not creds or not creds.valid:
        try:
            client_config = {
                "installed": {
                    "client_id": client_id, "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            }
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            # 로컬 환경이 아닐 경우(배포 스캔 중) 에러가 날 수 있으므로 대비
            creds = flow.run_local_server(port=0, open_browser=True)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            print(f"❌ 인증 프로세스 오류: {e}", file=sys.stderr)
            return None
    return creds