import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Annotated
from pathlib import Path

# MCP 및 Smithery 관련 라이브러리
from fastmcp import FastMCP
from smithery.decorators import smithery
from pydantic import BaseModel, Field

# Windows 환경 한글 출력 보장
os.environ['PYTHONIOENCODING'] = 'utf-8'

# =============================================================================
# 데이터 경로 및 관리 유틸리티
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
NOTES_FILE = DATA_DIR / "notes.json"
TODOS_FILE = DATA_DIR / "todos.json"

DATA_DIR.mkdir(exist_ok=True)

def load_data(path: Path) -> dict:
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(path: Path, data: dict):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# =============================================================================
# 세션 설정 스키마
# =============================================================================
class ConfigSchema(BaseModel):
    user_name: Optional[str] = Field(default=None, description="사용자 이름 설정")

# =============================================================================
# Smithery 공식 호환 팩토리 함수
# =============================================================================

@smithery.server(config_schema=ConfigSchema)
def app():
    """모든 도구와 리소스를 포함한 MCP 서버 인스턴스를 생성합니다."""
    mcp = FastMCP("개인 메모 & 할 일 관리")

    # [호환성 패치] Smithery dev 도구의 AttributeError 방지
    if not hasattr(mcp, "streamable_http_app"):
        mcp.streamable_http_app = mcp.http_app

    # -------------------------------------------------------------------------
    # [메모 도구]
    # -------------------------------------------------------------------------

    @mcp.tool(name="create_note")
    def create_note(
        title: Annotated[str, Field(description="메모 제목")],
        content: Annotated[str, Field(description="메모 상세 내용")],
        tags: Annotated[Optional[List[str]], Field(description="태그 목록")] = None
    ) -> str:
        """새로운 메모를 생성하고 저장합니다."""
        notes = load_data(NOTES_FILE)
        note_id = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        actual_tags = tags if tags is not None else []
        
        notes[note_id] = {
            "id": note_id,
            "title": title,
            "content": content,
            "tags": actual_tags,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        save_data(NOTES_FILE, notes)
        return f"✅ 메모 생성 완료 (ID: {note_id})"

    @mcp.tool(name="list_notes")
    def list_notes(
        tag: Annotated[Optional[str], Field(description="조회할 특정 태그")] = None
    ) -> List[dict]:
        """저장된 모든 메모 목록을 최신순으로 조회합니다."""
        notes = list(load_data(NOTES_FILE).values())
        if tag:
            notes = [n for n in notes if tag in n.get('tags', [])]
        notes.sort(key=lambda x: x['created_at'], reverse=True)
        return notes

    @mcp.tool(name="search_notes")
    def search_notes(
        query: Annotated[str, Field(description="검색 키워드 (제목/내용)")]
    ) -> List[dict]:
        """제목이나 내용에서 키워드로 메모를 검색합니다."""
        notes = load_data(NOTES_FILE)
        q = query.lower()
        results = [n for n in notes.values() if q in n['title'].lower() or q in n['content'].lower()]
        results.sort(key=lambda x: x['created_at'], reverse=True)
        return results

    @mcp.tool(name="update_note")
    def update_note(
        note_id: Annotated[str, Field(description="수정할 메모 ID")],
        title: Annotated[Optional[str], Field(description="새로운 제목")] = None,
        content: Annotated[Optional[str], Field(description="새로운 내용")] = None,
        tags: Annotated[Optional[List[str]], Field(description="새로운 태그 리스트")] = None
    ) -> str:
        """기존 메모의 내용을 수정합니다."""
        notes = load_data(NOTES_FILE)
        if note_id not in notes: return "❌ 메모를 찾을 수 없습니다."
        note = notes[note_id]
        if title: note['title'] = title
        if content: note['content'] = content
        if tags is not None: note['tags'] = tags
        note['updated_at'] = datetime.now().isoformat()
        save_data(NOTES_FILE, notes)
        return f"✅ 메모 수정 완료: {note_id}"

    @mcp.tool(name="delete_note")
    def delete_note(
        note_id: Annotated[str, Field(description="삭제할 메모 ID")]
    ) -> str:
        """메모를 목록에서 영구 삭제합니다."""
        notes = load_data(NOTES_FILE)
        if note_id in notes:
            del notes[note_id]
            save_data(NOTES_FILE, notes)
            return f"🗑️ 메모 삭제 성공: {note_id}"
        return "❌ 메모를 찾을 수 없습니다."

    # -------------------------------------------------------------------------
    # [할 일 도구]
    # -------------------------------------------------------------------------

    @mcp.tool(name="create_todo")
    def create_todo(
        title: Annotated[str, Field(description="할 일 제목")],
        description: Annotated[Optional[str], Field(description="상세 설명")] = None,
        due_date: Annotated[Optional[str], Field(description="마감일 (YYYY-MM-DD)")] = None,
        priority: Annotated[str, Field(description="우선순위 (low, medium, high)")] = "medium"
    ) -> str:
        """새로운 할 일을 추가합니다."""
        todos = load_data(TODOS_FILE)
        todo_id = f"todo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        todos[todo_id] = {
            "id": todo_id,
            "title": title,
            "description": description or "",
            "completed": False,
            "priority": priority,
            "due_date": due_date,
            "created_at": datetime.now().isoformat()
        }
        save_data(TODOS_FILE, todos)
        return f"✅ 할 일 등록 완료 (ID: {todo_id})"

    @mcp.tool(name="list_todos")
    def list_todos(
        status: Annotated[str, Field(description="필터 (all, pending, completed)")] = "all",
        sort_by: Annotated[str, Field(description="정렬 (created, due_date, priority)")] = "created"
    ) -> List[dict]:
        """할 일 목록을 조회하고 정렬합니다."""
        todos = load_data(TODOS_FILE)
        if status == "pending": items = [v for v in todos.values() if not v['completed']]
        elif status == "completed": items = [v for v in todos.values() if v['completed']]
        else: items = list(todos.values())

        if sort_by == "due_date": items.sort(key=lambda x: x.get('due_date') or '9999-12-31')
        elif sort_by == "priority":
            p_map = {"high": 0, "medium": 1, "low": 2}
            items.sort(key=lambda x: p_map.get(x['priority'], 1))
        else: items.sort(key=lambda x: x['created_at'], reverse=True)
        return items

    @mcp.tool(name="complete_todo")
    def complete_todo(
        todo_id: Annotated[str, Field(description="완료 처리할 할 일 ID")]
    ) -> str:
        """지정한 할 일을 완료 처리합니다."""
        todos = load_data(TODOS_FILE)
        if todo_id not in todos: return "❌ 할 일을 찾을 수 없습니다."
        todos[todo_id]["completed"] = True
        save_data(TODOS_FILE, todos)
        return f"🎉 완료: {todos[todo_id]['title']}"

    @mcp.tool(name="update_todo")
    def update_todo(
        todo_id: Annotated[str, Field(description="수정할 할 일 ID")],
        title: Annotated[Optional[str], Field(description="새 제목")] = None,
        due_date: Annotated[Optional[str], Field(description="새 마감일")] = None,
        priority: Annotated[Optional[str], Field(description="새 우선순위")] = None
    ) -> str:
        """기존 할 일의 정보를 수정합니다."""
        todos = load_data(TODOS_FILE)
        if todo_id not in todos: return "❌ 할 일을 찾을 수 없습니다."
        t = todos[todo_id]
        if title: t['title'] = title
        if due_date: t['due_date'] = due_date
        if priority: t['priority'] = priority
        save_data(TODOS_FILE, todos)
        return f"✅ 할 일 수정 완료: {todo_id}"

    @mcp.tool(name="delete_todo")
    def delete_todo(
        todo_id: Annotated[str, Field(description="삭제할 할 일 ID")]
    ) -> str:
        """할 일을 목록에서 삭제합니다."""
        todos = load_data(TODOS_FILE)
        if todo_id in todos:
            del todos[todo_id]
            save_data(TODOS_FILE, todos)
            return f"🗑️ 할 일 삭제 완료: {todo_id}"
        return "❌ 할 일을 찾을 수 없습니다."

    # -------------------------------------------------------------------------
    # [통계 및 리소스]
    # -------------------------------------------------------------------------

    @mcp.tool(name="get_statistics")
    def get_statistics() -> dict:
        """메모 개수 및 할 일 완료 현황 통계를 확인합니다."""
        notes = load_data(NOTES_FILE)
        todos = load_data(TODOS_FILE)
        comp = sum(1 for t in todos.values() if t['completed'])
        return {
            "total_notes": len(notes),
            "total_todos": len(todos),
            "completed": comp,
            "pending": len(todos) - comp,
            "last_updated": datetime.now().isoformat()
        }

    @mcp.resource("notes://all")
    def get_all_notes():
        """모든 메모를 MCP 리소스로 반환합니다."""
        return list(load_data(NOTES_FILE).values())

    @mcp.resource("todos://pending")
    def get_pending_todos():
        """미완료된 모든 할 일을 리소스로 반환합니다."""
        return [t for t in load_data(TODOS_FILE).values() if not t['completed']]

    return mcp

# Smithery 호환 인스턴스 노출
mcp = app()

if __name__ == "__main__":
    mcp.run()