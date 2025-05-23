from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.database import Base

# Модель SQLAlchemy для читателя
class ReadersORM(Base):
    __tablename__ = "readers"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    # Связь один-ко-многим с BorrowedBook
    #borrowed_books: Mapped[List["BorrowedBookORM"]] = relationship(
    #    back_populates="reader",  #Связь с BorrowedBook
    #    lazy="select",
    #    cascade="all, delete"
    #)

