from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# MySQL 엔진 생성
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    # echo=True  # 디버깅을 위해 SQLAlchemy 로그를 활성화하려면 주석 해제
)

# 세션 로컬 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 정의
Base = declarative_base()
