from src.exceptions import ObjectNotFoundException, UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, \
    ObjectAlreadyExistsException, ReaderBadIdHTTPException, BookAlreadyExistsException, BookBadIdHTTPException, \
    BookBadHTTPException, BookNotFoundHTTPException, BookIsbnAlreadyExistsHTTPException, BookBadCopyHTTPException
from src.schemas.books import BookCreateDTO, BookUpdateDTO
from src.schemas.readers import ReaderCreateDTO, ReaderUpdateDTO
from src.services.base import BaseService


class BookService(BaseService):
    async def create_book(self, book_data: BookCreateDTO):
        try:
            existing_isbn = await self.db.books.get_one_or_none(isbn = book_data.isbn)
            if existing_isbn:
                raise BookIsbnAlreadyExistsHTTPException
            book = await self.db.books.add(book_data)
            await self.db.commit()
            return book
        except (BookAlreadyExistsException):
            raise BookIsbnAlreadyExistsHTTPException

    async def get_books(self):
        return await self.db.books.get_all()


    async def get_book_by_id(self, book_id: int):
        try:
            return await self.db.books.get_one(id=book_id)
        except (ObjectNotFoundException):
            raise BookBadIdHTTPException


    async def edit_book_by_id(self, book_id: int, book_data: BookUpdateDTO):
        try:
            existing_book = await self.db.books.get_one_or_none(id = book_id)
            if existing_book:
                existing_isbn = await self.db.books.get_one_or_none(isbn = book_data.isbn)
                if not existing_isbn:
                    if book_data.copies < 0:
                        raise BookBadCopyHTTPException
                    await self.db.books.edit(book_data, id=book_id)
                    await self.db.commit()
                else:
                    raise BookIsbnAlreadyExistsHTTPException
            else:
                raise BookNotFoundHTTPException
        except (ObjectNotFoundException):
            raise BookNotFoundHTTPException



    async def delete_book(self, book_id: int):
        try:
            existing_book = await self.db.books.get_one_or_none(id = book_id)
            if existing_book:
                await self.db.books.delete(id=book_id)
                await self.db.commit()
            else:
                raise BookBadIdHTTPException
        except (ObjectNotFoundException):
            raise BookBadIdHTTPException


