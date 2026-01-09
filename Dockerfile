# 1. uv가 포함된 공식 이미지를 빌드 스테이지로 사용
FROM astral-sh/uv:0.5 AS uv_build

# 2. 실행 환경으로 Python 3.13 slim 이미지 사용
FROM python:3.13-slim

# 작업 디렉토리 설정
WORKDIR /app

# uv 바이너리 복사
COPY --from=uv_build /uv /uvx /bin/

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SMITHERY_SCANNING=true

# 의존성 파일 복사 (pyproject.toml이 있다면 그것을 사용, 없다면 바로 설치)
COPY . .

# uv를 사용하여 시스템 환경에 직접 패키지 설치 (--system 플래그 사용)
# 캐시를 삭제하여 이미지 크기 최소화 (--no-cache)
RUN uv pip install --system --no-cache \
    mcp \
    fastmcp \
    google-api-python-client \
    google-auth-oauthlib \
    python-dotenv

# 서버 실행
ENTRYPOINT ["python", "-m", "todo_server.main"]