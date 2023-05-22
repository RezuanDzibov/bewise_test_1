from typing import TypeVar

from sqlalchemy import inspect
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.types import Integer


@as_declarative()
class Base:
    id: Integer
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    async def as_dict(self) -> dict:
        try:
            object_ = inspect(self).dict
            for key, value in object_.items():
                if isinstance(value, list) and value:
                    serialized_items = list()
                    for item in value:
                        if isinstance(item, Base):
                            serialized_items.append(item.as_dict())
                    object_[key] = serialized_items
        except NoInspectionAvailable:
            object_ = self.__dict__
        if hasattr(self, "_sa_instance_state"):
            object_.pop("_sa_instance_state")
        return object_


BaseModel = TypeVar("BaseModel", bound=Base)
