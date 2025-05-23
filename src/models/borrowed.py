from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, CheckConstraint, Integer, ForeignKey, Date, func
from src.database import Base

class BorrowedBookORM(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.id"), nullable=False
    )
    reader_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("readers.id"), nullable=False
    )
    borrow_date: Mapped[datetime] = mapped_column(
        Date, server_default=func.now()
    )
    return_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)

    book: Mapped["Book"] = relationship(
        back_populates="borrowed_books", lazy="joined"
    )
    reader: Mapped["Reader"] = relationship(
        back_populates="borrowed_books", lazy="joined"
    )