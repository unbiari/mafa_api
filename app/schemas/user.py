from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole
from typing import List
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., example="johndoe")
    email: EmailStr = Field(..., example="johndoe@example.com")
    full_name: str | None = Field(None, example="John Doe")
    is_active: int | None = Field(1, example=1)

    class Config:
        from_attributes = True
        use_enum_values = True  # Enum 값을 문자열로 사용

class UserCreate(UserBase):
    password: str = Field(..., example="password123")
    role: UserRole | None = None  # 생성 시 권한 설정 가능

class UserUpdateOwn(UserBase):
    password: str | None = Field(None, example="newpassword123")

class UserUpdateAdmin(UserBase):
    password: str | None = Field(None, example="newpassword123")
    role: UserRole | None = None  # 업데이트 시 권한 변경 가능

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserListResponse(BaseModel):
    users: List[User]
    total: int

    class Config:
        from_attributes = True