from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdateOwn
from app.core.security import get_password_hash, verify_password
from typing import List

class UserRepository:
    def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password),  # 수정된 부분
            is_active=obj_in.is_active,
            role=obj_in.role,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def get(self, db: Session, id: int) -> User | None:
        return db.query(User).filter(User.id == id).first()

    def update(self, db: Session, db_obj: User, obj_in: UserUpdateOwn) -> User:
        obj_data = obj_in.model_dump(exclude_unset=True)
        if "password" in obj_data:
            hashed_password = get_password_hash(obj_data.pop("password"))  # 수정된 부분
            setattr(db_obj, "hashed_password", hashed_password)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def deactivate(self, db: Session, db_obj: User) -> User:
        db_obj.is_active = 0  # 또는 False
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj    

    # 추가된 함수    
    def delete(self, db: Session, id: int) -> User | None:
        obj = db.query(User).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def authenticate(self, db: Session, username: str, password: str) -> User | None:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return bool(user.is_active)

    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_multi_with_count(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> tuple[List[User], int]:
        query = db.query(User).filter(User.is_active == 1)
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        return users, total