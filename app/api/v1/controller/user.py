from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import User, UserCreate, UserUpdateOwn, UserUpdateAdmin, UserListResponse
from app.api.deps import get_db, require_admin, require_superuser, require_user
from app.services.user import UserService
from app.repositories.user import UserRepository

router = APIRouter()
repository = UserRepository()
service = UserService(repository)


# 사용자 등록, 아무나
@router.post("/", response_model=User, description="사용자 등록, 권한 : 아무나")
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    # 권한 없음 - current_user: User = Depends(require_user),
):    
    user_in.is_active = 1 # 강제 설정
    user_in.role = "user" # 강제 설정
    db_user = service.get_user_by_username(db, username=user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = service.get_user_by_email(db, email=user_in.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(db, user_in)


# 사용자 등록, 관리자
@router.post("/admin", response_model=User, description="사용자 등록, 권한 : 관리자")
def create_user_admin(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin), # 관리자만 접근 가능
):    
    db_user = service.get_user_by_username(db, username=user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = service.get_user_by_email(db, email=user_in.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(db, user_in)


# 사용자 리스트, 관리자(admin)
@router.get("/", response_model=UserListResponse, description="사용자 리스트, 권한 : 관리자")
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin), # 관리자만 접근 가능
):
    users, total = service.get_users_with_count(db, skip=skip, limit=limit)
    return {"users": users, "total": total}


# 사용자 정보 보기, 슈퍼유저 이상(superuser)
@router.get("/{user_id}", response_model=User, description="사용자 정보 보기, 권한 : 슈퍼유저 이상")
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_superuser),
):
    db_user = service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 사용자 본인 정보 수정, 본인만
@router.put("/own/{user_id}", response_model=User, description="사용자 본인 정보 수정(password 포함), 권한 : 본인만")
def update_user_own(
    user_id: int,
    user_in: UserUpdateOwn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You can only update your own account(by id)"
        )
    if user_in.email != current_user.email or user_in.username != current_user.username:
        raise HTTPException(
            status_code=403, detail="You can only update your own account(by email, username)"
        )
    updated_user = service.update_user(db, user_id=user_id, user_in=user_in)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User update failed")
    return updated_user


# 관리자 사용자 정보 수정, 관리자 2
@router.put("/admin/{user_id}", response_model=User, description="관리자 사용자 정보 수정, 권한 : 관리자")
def update_user_admin(
    user_id: int,
    user_in: UserUpdateAdmin,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin), # 관리자만 접근 가능    
):
    db_user = service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="DB user not found")
    if user_in.email != db_user.email or user_in.username != db_user.username:
        raise HTTPException(status_code=403, detail="Admin can only update the user account(by email, username)")
    updated_user = service.update_user(db, user_id=user_id, user_in=user_in)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User update failed")
    return updated_user


# 본인만
@router.delete("/{user_id}", response_model=User, description="사용자 정보 삭제(is_active 변경), 권한 : 본인만")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_user),
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own account")
    deactivated_user = service.deactivate_user(db, user_id=user_id)
    if deactivated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deactivated_user


# 추가 함수

# 본인만
@router.get("/show/me", response_model=User, description="본인 정보 보기, 권한 : 본인만")
def read_user_me(current_user: User = Depends(require_user)):
    return current_user
