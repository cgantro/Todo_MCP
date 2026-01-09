import datetime
from googleapiclient.discovery import build
from .google_auth import get_credentials
from .email_tools import send_alert_email

# 사용자 요청에 따른 카테고리 고정 및 색상 설정
CATEGORY_MAP = {
    "업무": "9",    # Blue (Blueberry)
    "개인": "10",   # Green (Basil)
    "경조사": "11"   # Red (Tomato)
}

def register_calendar_tools(mcp):
    def get_service():
        return build('calendar', 'v3', credentials=get_credentials())

    @mcp.tool()
    def add_schedule(title: str, content: str, start: str, end: str, category: str = "개인"):
        """
        일정을 등록합니다. 제목에 접두어를 붙이지 않고 색상으로 구분합니다.
        category: '개인', '업무', '경조사' 중 하나 선택
        """
        service = get_service()
        color_id = CATEGORY_MAP.get(category, "10") # 기본값 개인(Green)
        
        event = {
            'summary': title, # 접두어 없이 제목만 저장
            'description': content, # 세부 내용은 설명 칸에 저장
            'colorId': color_id,
            'start': {'dateTime': start, 'timeZone': 'Asia/Seoul'},
            'end': {'dateTime': end, 'timeZone': 'Asia/Seoul'},
        }
        res = service.events().insert(calendarId='primary', body=event).execute()
        return f"📅 {category} 일정 등록 완료: {res.get('htmlLink')}"

    @mcp.tool()
    def list_schedules(days: int = 7, category_filter: str = None):
        """
        일정 목록을 조회합니다 (7일~30일). 
        카테고리 필터링 시 색상 ID를 기준으로 판별합니다.
        """
        search_days = min(max(days, 1), 30)
        service = get_service()
        now = datetime.datetime.utcnow()
        time_min = now.isoformat() + 'Z'
        time_max = (now + datetime.timedelta(days=search_days)).isoformat() + 'Z'

        events_res = service.events().list(
            calendarId='primary', timeMin=time_min, timeMax=time_max,
            singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_res.get('items', [])

        # 색상 ID로 카테고리 역추적
        reverse_map = {v: k for k, v in CATEGORY_MAP.items()}

        output = [f"🗓️ 향후 {search_days}일간의 일정 목록:"]
        for e in events:
            color_id = e.get('colorId', '10')
            category = reverse_map.get(color_id, "기타")
            
            # 카테고리 필터가 있는 경우 걸러냄
            if category_filter and category != category_filter:
                continue

            time_info = e['start'].get('dateTime', e['start'].get('date'))
            output.append(
                f"- [{category}] {time_info}: {e.get('summary')}\n"
                f"  📝 세부내용: {e.get('description', '없음')}"
            )

        return "\n".join(output) if len(output) > 1 else "해당 기간에 일정이 없습니다."

    @mcp.tool()
    def check_urgent_schedules(hours: int = 2, receiver_email: str = None):
        """급박한 일정을 체크하여 세부 내용과 함께 이메일 알림을 보냅니다."""
        service = get_service()
        now = datetime.datetime.utcnow()
        time_max = (now + datetime.timedelta(hours=hours)).isoformat() + 'Z'
        
        events = service.events().list(
            calendarId='primary', timeMin=now.isoformat() + 'Z', timeMax=time_max,
            singleEvents=True, orderBy='startTime'
        ).execute().get('items', [])

        if not events: return f"⏰ {hours}시간 내 급박한 일정이 없습니다."

        msg = "⚠️ [긴급 일정 알림]\n\n"
        for e in events:
            msg += f"📌 {e.get('summary')}\n   시간: {e['start'].get('dateTime')}\n   내용: {e.get('description', '없음')}\n\n"

        if receiver_email:
            send_alert_email(receiver_email, "[긴급] 일정 안내", msg)
            return f"📧 {len(events)}개의 일정 알림을 {receiver_email}로 발송했습니다."
        return msg