import os
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from ..database import get_path

SCOPES = ['https://www.googleapis.com/auth/calendar']

# todo_server/tools/google_auth.py

def get_credentials():
    token_path = get_path("google_token.json")
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    
    if not client_id:
        print("❌ GOOGLE_CLIENT_ID가 없습니다.", file=sys.stderr)
        return None

    

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    if not creds or not creds.valid:
        # 브라우저 인증 시도
        try:
            client_config = {
                "installed": {
                    "client_id": client_id, 
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            }
            print("🌐 브라우저 인증창을 띄웁니다...", file=sys.stderr)
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            
            # 로컬에서 실행 시 여기서 멈추고 브라우저가 떠야 함
            creds = flow.run_local_server(port=0) 
            
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
            print("✅ 인증 성공! google_token.json이 생성되었습니다.", file=sys.stderr)
        except Exception as e:
            print(f"❌ 인증 실패: {e}", file=sys.stderr)
            return None
            
    return creds