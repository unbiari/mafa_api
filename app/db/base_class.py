from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # 자동으로 __tablename__을 생성합니다.
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
