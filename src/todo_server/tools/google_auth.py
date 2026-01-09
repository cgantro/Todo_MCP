import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from ..database import get_path

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():

    # 2. 기존 파일 방식 (로컬용)
    token_path = get_path("google_token.json")
    if token_path.exists():
        return Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # 3. 인증 정보가 아예 없는 경우
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        return None

    # 로컬인 경우에만 브라우저 실행
    flow = InstalledAppFlow.from_client_config({
        "installed": {"client_id": client_id, "client_secret": client_secret}
    }, SCOPES)
    creds = flow.run_local_server(port=0)
    
    with open(token_path, 'w') as token:
        token.write(creds.to_json())
        
    return creds