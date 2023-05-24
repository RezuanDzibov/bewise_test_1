from sqlalchemy import DATETIME
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Question(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    at_api_id: Mapped[int] = mapped_column(unique=True)
    text: Mapped[str]
    answer: Mapped[str]
    created_at: Mapped[DATETIME] = mapped_column(type_=TIMESTAMP(timezone=True))
