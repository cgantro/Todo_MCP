
# 📅 Google Calendar Smart Manager (MCP)

Turn Google Calendar into your intelligent assistant.
This MCP server lets you manage schedules and notes seamlessly through AI conversations, keeping everything organized in one place.

---

## 🌟 Core Guide

### 1. Unified Schedule & Notes Management

* **Description Field as Notes**
  No separate note-taking app needed. All details you provide when creating an event (agenda, preparation notes, links, etc.) are stored directly in the **Google Calendar “Description”** field.
* **Single Source of Truth**
  Everything lives in Google Calendar, fully synced across web and mobile.

---

### 2. Automatic Color-Based Categorization (3 Core Types)

The AI analyzes each event and automatically assigns a calendar color based on its purpose.
No tags in titles—your calendar stays clean and readable.

| Category            | Calendar Color      | Use Case                                |
| ------------------- | ------------------- | --------------------------------------- |
| **Work**            | 🔵 Blueberry (Blue) | Meetings, deadlines, project tasks      |
| **Personal**        | 🟢 Basil (Green)    | Hobbies, workouts, personal plans       |
| **Family / Events** | 🔴 Tomato (Red)     | Weddings, family gatherings, ceremonies |

---

### 3. Smart Search & Alerts

* **Flexible Queries**
  Retrieve today’s events, the next 7 days, or up to 30 days at once.
* **Urgent Email Alerts**
  If an event starts within the next 2 hours, a detailed notification (including notes) can be sent to a designated email address.
* **Natural Deletion**
  Say things like *“Cancel my afternoon schedule today”* or
  *“Delete the ‘Gym’ event I added yesterday”* — the server finds and removes the correct event.

---

## 💬 AI Assistant Conversation Examples

Once the MCP server is installed, use it with AI clients (e.g. Claude) like this:

> **Create an Event**
> “Add a work meeting today at 3 PM.
> In the notes, write ‘Meeting Room B, bring weekly report.’”
> *(Result: The event is saved in blue with notes included.)*

> **Custom Search**
> “Show me all family-related events scheduled for this week.”
> *(Result: Events are filtered using calendar color categorization.)*

> **Urgent Alert**
> “Check for events starting within the next 2 hours and send me an urgent email alert.”
> *(Result: An email is sent with detailed event information.)*

> **Help Request**
> “How do I use this server?”
> *(Result: The built-in helper tool explains all features and categories.)*

---

## 🔑 Notes

* **Initial Authorization**
  When you use the tools for the first time, a browser window will open for Google account authentication.
  After completing login once, future connections are automatic.




# 📅 Google Calendar Smart Manager (MCP)

구글 캘린더를 당신의 똑똑한 비서로 만들어주는 MCP 서버입니다. 복잡한 일정 관리와 흩어진 메모를 AI와 대화하며 한곳에서 체계적으로 관리하세요.

---

## 🌟 핵심 가이드

### 1. 일정 & 메모 통합 관리
* **설명(Description) 필드 활용**: 별도의 메모 앱이 필요 없습니다. 일정 등록 시 전달하는 모든 세부 사항(회의 안건, 준비물 등)은 구글 캘린더의 **'설명'** 칸에 즉시 저장됩니다.
* **통합 저장소**: 모든 데이터가 구글 캘린더 하나에 모이므로 모바일과 웹 어디서든 동기화된 일정을 확인할 수 있습니다.

### 2. 색상 기반 자동 분류 (3대 카테고리)
AI가 일정의 성격을 파악하여 캘린더의 색상을 자동으로 지정합니다. 제목 앞에 별도의 태그를 붙이지 않아 캘린더 뷰가 매우 깔끔합니다.

| 카테고리 | 캘린더 색상 | 용도 |
| :--- | :--- | :--- |
| **업무 (Work)** | 🔵 파란색 (Blueberry) | 회의, 마감일, 프로젝트 업무 등 |
| **개인 (Personal)** | 🟢 연두색 (Basil) | 취미, 운동, 개인 약속, 할 일 등 |
| **경조사 (Family)** | 🔴 빨간색 (Tomato) | 결혼식, 제사, 가족 모임 등 중요 행사 |

### 3. 스마트 검색 및 알림
* **유연한 조회**: 오늘, 이번 주(7일)는 물론 최대 30일치 일정을 한 번에 불러옵니다.
* **긴급 이메일 알림**: 2시간 이내에 시작되는 급박한 일정이 있다면, 상세 메모를 포함하여 지정된 이메일로 즉시 알림을 보냅니다.
* **간편한 삭제**: "오늘 오후 일정 취소됐어" 또는 "어제 등록한 '헬스장' 일정 삭제해줘"라고 하면 관련 일정을 찾아 정리합니다.

---

## 💬 AI 비서 대화 예시

설치된 MCP 도구를 활용해 AI(Claude 등)에게 다음과 같이 요청해 보세요.

> **일정 등록**
> "오늘 오후 3시에 팀 미팅 업무로 등록해줘. 메모에는 '회의실 B, 주간 보고서 지참'이라고 적어줘."
> *(결과: 파란색으로 일정과 메모가 함께 저장됩니다.)*

> **맞춤 조회**
> "이번 주에 잡힌 경조사 일정들만 싹 모아서 보여줘."
> *(결과: 색상 코드를 분석하여 경조사 카테고리만 필터링합니다.)*

> **긴급 알림**
> "지금부터 2시간 내에 있는 일정을 확인해서 내 메일로 긴급 알람 보내줘."
> *(결과: 2시간 내 일정을 체크하여 상세 내용과 함께 이메일을 발송합니다.)*

> **도움말 요청**
> "이 서버는 어떻게 쓰는 거야?"
> *(결과: 내장된 Helper 도구가 모든 기능과 카테고리 사용법을 안내합니다.)*

---

## 🔑 참고 사항
* **최초 인증**: 서버 연결 후 도구를 처음 사용할 때, 구글 계정 로그인을 위한 브라우저 창이 한 번 열립니다. 로그인을 완료하면 이후에는 자동으로 연결됩니다.
