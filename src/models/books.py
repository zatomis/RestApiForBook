from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, CheckConstraint, Integer
from src.database import Base

class BookModelORM(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    publication_year: Mapped[Optional[int]] = mapped_column(Integer)
    isbn: Mapped[str] = mapped_column(String(30), nullable=False, unique=True, index=True)
    copies: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        server_default="1"  # Для бд где нужен дефолт на уровне БД
    )
    # Связь один-ко-многим с BorrowedBook
    borrowed_books: Mapped[List["BorrowedBookORM"]] = relationship(
        back_populates="book",  #Связь с BorrowedBook
        lazy="select",
        cascade="all, delete"
    )

    __table_args__ = (
        CheckConstraint('copies >= 0'),
    )
