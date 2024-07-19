FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /workspace

# 현재 디렉토리의 파일들을 컨테이너의 /app에 복사
COPY . .

# 필요한 Python 패키지 설치
RUN pip install -r requirements.txt

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
