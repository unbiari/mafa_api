from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token
from app.api.deps import get_db
from app.schemas.token import Token
from app.repositories.user import UserRepository

router = APIRouter()

# 사용자 로그인, 아무나
@router.post("/login", response_model=Token, description="사용자 로그인, 권한 : 아무나")
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = UserRepository().authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not UserRepository().is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token = create_access_token(user=user)
    return {"access_token": access_token, "token_type": "bearer"}
