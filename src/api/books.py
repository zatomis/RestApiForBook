import logging
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, ReaderNotRegisteredHTTPException, BookBadHTTPException, \
    BookBadIdHTTPException
from src.schemas.books import BookCreateDTO, BookUpdateDTO
from src.services.books import BookService

router = APIRouter(prefix="/books", tags=["Управление книгами"])
logging.basicConfig(level=logging.INFO)


@router.post("")
async def create_book(db: DBDep, book_data: BookCreateDTO =  Body(
        openapi_examples={
            "1": {
                "summary": "Война и Мир",
                "value": {
                    "title": "Война и Мир",
                    "author": "Толстой Л.",
                    "publication_year": 1997,
                    "isbn": "ISBN 978-5-699-12014-7",
                    "copies": 4,
                },
            },
            "2": {
                "summary": "Дети Капитана Гранта",
                "value": {
                    "title": "Дети Капитана Гранта",
                    "author": "Жюль Верн",
                    "publication_year": 2009,
                    "isbn": "ISBN 126-5-399-00014-5",
                    "copies": 10,
                },
            },
            "3": {
                "summary": "Пикни́к на обо́чине",
                "value": {
                    "title": "Пикни́к на обо́чине",
                    "author": "Стругацкие",
                    "publication_year": 2010,
                    "isbn": "ISBN 006-5-111-00012-1",
                    "copies": 7,
                },
            },
        }
    ),
):
    book = await BookService(db).create_book(book_data)
    return {"status": "OK", "data": book}


@router.get("")
@cache(expire=10)
async def get_books(user_id: UserIdDep, db: DBDep):
    logging.info(f"user {user_id}")
    return await BookService(db).get_books()


@router.get("/{book_id}")
async def get_book_by_id(book_id: int, db: DBDep):
    try:
        return await BookService(db).get_book_by_id(book_id)
    except ObjectNotFoundException:
        raise BookBadIdHTTPException


@router.put("/{book_id}")
async def edit_book_by_id(book_id: int, db: DBDep, book_data: BookUpdateDTO = Body()):
    try:
        await BookService(db).edit_book_by_id(book_id, book_data)
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise BookBadHTTPException


@router.delete("/{book_id}")
async def delete_book(book_id: int, db: DBDep):
    try:
        await BookService(db).delete_book(book_id)
        return {"detail": "Книга удалена успешно"}
    except ObjectNotFoundException:
        raise ReaderNotRegisteredHTTPException
