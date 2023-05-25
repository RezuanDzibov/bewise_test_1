from typing import TypeVar

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.types import Integer


@as_declarative()
class Base:
    id: Integer
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


BaseModel = TypeVar("BaseModel", bound=Base)
