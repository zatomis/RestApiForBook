from pydantic import BaseModel


class BorrowDTO(BaseModel):
    book_id: int
    reader_id: int
