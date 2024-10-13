from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 추가된 임포트

from app.api import api_router
from app.db.session import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    description="API for managing users",
    version="1.0.0",
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 접근 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
