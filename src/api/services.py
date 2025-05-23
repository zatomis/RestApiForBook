import logging
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, ReaderNotRegisteredHTTPException, BookBadHTTPException, \
    BookBadIdHTTPException
from src.schemas.books import BookCreateDTO
from src.schemas.readers import ReaderCreateDTO
from src.schemas.services import BorrowDTO
from src.services.books import BookService
from src.services.services import BorrowService

router = APIRouter(prefix="/services", tags=["Управление прием-выдача"])
logging.basicConfig(level=logging.INFO)


@router.post("/borrow/")
@cache(expire=10)
async def borrow_book(user_id: UserIdDep, db: DBDep, borrow_data: BorrowDTO = Body()):
    await BorrowService(db).borrow_book(borrow_data)
    return {"status": "Книга выдана"}

@router.post("/return/")
@cache(expire=10)
async def return_book(user_id: UserIdDep, db: DBDep, borrow_data: BorrowDTO = Body()):
    await BorrowService(db).return_book(borrow_data)
    return {"status": "Книга. Возврат"}

