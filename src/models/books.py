from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, CheckConstraint, Integer
from src.database import Base

class BookModelORM(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    publication_year: Mapped[Optional[int]] = mapped_column(Integer)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    copies: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        server_default="1"  # Для баз данных, где нужен дефолт на уровне БД
    )
    __table_args__ = (
        CheckConstraint('copies >= 0'),
    )
