import logging
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, ReaderNotRegisteredHTTPException
from src.schemas.books import BookCreateDTO
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
async def read_readers(user_id: UserIdDep, db: DBDep):
    logging.info(f"user {user_id}")
    return await BookService(db).read_readers()


@router.get("/{reader_id}")
async def read_readers_by_id(reader_id: int, db: DBDep):
    try:
        return await BookService(db).read_readers_by_id(reader_id)
    except ObjectNotFoundException:
        raise ReaderNotRegisteredHTTPException


@router.put("/{reader_id}")
async def edit_reader_by_id():
    pass
#async def edit_reader_by_id(reader_id: int, db: DBDep, reader_data: ReaderUpdateDTO = Body()):
#    try:
#        await BookService(db).edit_reader(reader_id, reader_data)
#        return {"status": "OK"}
#    except ObjectNotFoundException:
#        raise ReaderNotRegisteredHTTPException


@router.delete("/{reader_id}")
async def delete_reader(reader_id: int, db: DBDep):
    try:
        await BookService(db).delete_reader(reader_id)
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise ReaderNotRegisteredHTTPException
