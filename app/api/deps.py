from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.db.session import SessionLocal
from app.core.config import settings
from app.models.user import User, UserRole
from app.repositories.user import UserRepository

import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.error("Token decode error: 'sub' not found in token payload")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}")
        raise credentials_exception
    user = UserRepository().get(db, id=int(user_id))
    if user is None:
        logger.error(f"User not found: ID {user_id}")
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user


def require_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role not in [UserRole.superuser, UserRole.admin]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user


def require_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role not in [UserRole.superuser, UserRole.admin, UserRole.user]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user
