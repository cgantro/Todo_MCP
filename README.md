# 📅 Smart Schedule & Note MCP Server

Google Calendar를 단일 저장소로 사용하여 일정과 메모를 스마트하게 관리하는 MCP 서버입니다.

## 🚀 주요 기능
- **즉시 인증**: 서버 구동 시 즉시 Google OAuth 브라우저를 띄워 인증합니다.
- **3대 카테고리 관리**: '개인', '업무', '경조사'를 색상(연두, 파랑, 빨강)으로 자동 분류합니다.
- **통합 메모**: 일정의 '설명(Description)' 필드를 메모장으로 활용합니다.
- **스마트 조회**: 기본 7일, 최대 30일까지 유연하게 일정을 조회합니다.
- **이메일 알림**: 2시간 이내의 급박한 일정을 체크하여 이메일로 발송합니다.

## 🎨 카테고리 색상 가이드
- **업무**: Blueberry (Blue)
- **개인**: Basil (Green)
- **경조사**: Tomato (Red)

## 📦 실행 방법
```bash
# 의존성 설치
pip install mcp fastmcp google-api-python-client google-auth-oauthlib python-dotenv

# 서버 실행
python main.py