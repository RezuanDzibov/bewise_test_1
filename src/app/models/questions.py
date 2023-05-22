from sqlalchemy import DATETIME, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Question(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    answer: Mapped[str]
    created_at: Mapped[DATETIME] = mapped_column(DateTime)
