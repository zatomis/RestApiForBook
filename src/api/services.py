import logging
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, ReaderNotRegisteredHTTPException, BookBadHTTPException, \
    BookBadIdHTTPException
from src.schemas.books import BookCreateDTO
from src.services.books import BookService

router = APIRouter(prefix="/services", tags=["Управление прием-выдача"])
logging.basicConfig(level=logging.INFO)


@router.post("")
@cache(expire=10)
async def create_book(user_id: UserIdDep, db: DBDep, book_data: BookCreateDTO =  Body()):
    pass




@router.delete("/{book_id}")
@cache(expire=10)
async def delete_book(book_id: int,user_id: UserIdDep, db: DBDep):
    try:
        await BookService(db).delete_book(book_id)
        return {"detail": "Книга удалена успешно"}
    except ObjectNotFoundException:
        raise ReaderNotRegisteredHTTPException
