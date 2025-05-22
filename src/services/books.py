from src.exceptions import ObjectNotFoundException, UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, \
    ObjectAlreadyExistsException, ReaderBadIdHTTPException
from src.schemas.books import BookCreateDTO
from src.schemas.readers import ReaderCreateDTO, ReaderUpdateDTO
from src.services.base import BaseService


class BookService(BaseService):
    async def create_book(self, book_data: BookCreateDTO):
        try:
            existing_isbn = await self.db.books.get_one_or_none(email = reader_data.email)
            if existing_reader:
                raise UserAlreadyExistsException
            reader = await self.db.readers.add(reader_data)
            await self.db.commit()
            return reader
        except (UserAlreadyExistsException):
            raise UserEmailAlreadyExistsHTTPException

    async def get_books(self):
        return await self.db.readers.get_all()

    async def get_book_by_id(self, reader_id: int):
        return await self.db.readers.get_one(id=reader_id)

    async def edit_book(self, reader_id: int, reader_data: ReaderUpdateDTO):
        try:
            existing_reader = await self.db.readers.get_one_or_none(id = reader_id)
            if existing_reader:
                existing_reader_mail = await self.db.readers.get_one_or_none(email = reader_data.email)
                if not existing_reader_mail:
                    await self.db.readers.edit(reader_data, id=reader_id)
                    await self.db.commit()
                else:
                    raise UserEmailAlreadyExistsHTTPException
            else:
                raise ReaderBadIdHTTPException
        except (ObjectNotFoundException):
            raise ReaderBadIdHTTPException



    async def delete_book(self, reader_id: int):
        try:
            existing_reader = await self.db.readers.get_one_or_none(id = reader_id)
            if existing_reader:
                await self.db.readers.delete(id=reader_id)
                await self.db.commit()
            else:
                raise ReaderBadIdHTTPException
        except (ObjectNotFoundException):
            raise ReaderBadIdHTTPException


