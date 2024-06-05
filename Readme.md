1. 데이터베이스 초기화: 처음에 한 번 실행하여 엑셀 데이터를 데이터베이스에 로드

from app.database import initialize_database

initialize_database()


-> python initialize_db.py 명령실행

2. FastAPI 서버 실행

uvicorn app.main:app --reload
