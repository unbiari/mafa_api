from fastapi import APIRouter

from .user import router as user_router
from .auth import router as auth_router  # 인증 라우터 임포트

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(user_router, prefix="/users", tags=["users"])
