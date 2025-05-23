from pydantic import BaseModel

class BookCreateDTO(BaseModel):
    title: str
    author: str
    publication_year: int | None = None
    isbn: str | None = None
    copies: int = 1

class BookTestDTO(BookCreateDTO):
    id: int


class BookDTO(BookCreateDTO):
    id: int
    class Config:
        orm_mode = True


class BookUpdateDTO(BaseModel):
    title: str | None = None
    author: str | None = None
    publication_year: int | None = None
    isbn: str | None = None
    copies: int | None = None
