from datetime import datetime

from pydantic import BaseModel


class BorrowDTO(BaseModel):
    book_id: int
    reader_id: int

class BorrowUpdateDTO(BaseModel):
    return_date: datetime
