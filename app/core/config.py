from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
import json

# .env 파일 로드
load_dotenv()

# 필요한 변수들을 클래스 밖에서 정의
base_dir = os.path.dirname(os.path.abspath(__file__))
secret_file = os.path.join(base_dir, '..', '..', 'secret.json')
with open(secret_file) as f:
    Secret = json.load(f)
db = Secret["db"]

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{db.get('user')}:{db.get('password')}"
    f"@{db.get('host')}:{db.get('port')}/{db.get('database')}?charset=utf8mb4"
)

class Settings(BaseSettings):
    # 데이터베이스 URI 설정
    SQLALCHEMY_DATABASE_URI: str = SQLALCHEMY_DATABASE_URI
        
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 토큰 유효 기간 (분)
    ALGORITHM: str = "HS256"

    class Config:
        case_sensitive = True
        env_file = ".env"  # .env 파일을 지정

settings = Settings()
