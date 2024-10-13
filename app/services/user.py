from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdateOwn
from typing import List
from app.models.user import User

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, db: Session, user_id: int):
        return self.repository.get(db, user_id)

    def get_user_by_username(self, db: Session, username: str):
        return self.repository.get_by_username(db, username)

    def get_user_by_email(self, db: Session, email: str):
        return self.repository.get_by_email(db, email)
    
    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repository.get_multi(db, skip=skip, limit=limit)

    def create_user(self, db: Session, user_in: UserCreate):
        # 추가적인 비즈니스 로직 (예: 유효성 검사)을 여기에 추가할 수 있습니다.
        return self.repository.create(db, user_in)

    def update_user(self, db: Session, user_id: int, user_in: UserUpdateOwn):
        db_user = self.repository.get(db, user_id)
        if not db_user:
            return None
        return self.repository.update(db, db_user, user_in)

    def deactivate_user(self, db: Session, user_id: int):
        db_user = self.repository.get(db, user_id)
        if not db_user:
            return None
        return self.repository.deactivate(db, db_user)
    
    def get_users_with_count(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> tuple[List[User], int]:
        return self.repository.get_multi_with_count(db, skip=skip, limit=limit)    