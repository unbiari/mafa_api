from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class UserRole(enum.Enum):
    admin = "admin"
    superuser = "superuser"
    user = "user"

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user)  # 권한 필드 추가
    is_active = Column(Integer, default=1)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    