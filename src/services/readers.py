from src.exceptions import ObjectNotFoundException, UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, \
    ReaderBadIdHTTPException
from src.schemas.readers import ReaderCreateDTO, ReaderUpdateDTO
from src.services.base import BaseService


class ReaderService(BaseService):
    async def create_reader(self, reader_data: ReaderCreateDTO):
        try:
            existing_reader = await self.db.readers.get_one_or_none(email = reader_data.email)
            if existing_reader:
                raise UserAlreadyExistsException
            reader = await self.db.readers.add(reader_data)
            await self.db.commit()
            return reader
        except (UserAlreadyExistsException):
            raise UserEmailAlreadyExistsHTTPException

    async def read_readers(self):
        return await self.db.readers.get_all()

    async def read_readers_by_id(self, reader_id: int):
        return await self.db.readers.get_one(id=reader_id)

    async def edit_reader(self, reader_id: int, reader_data: ReaderUpdateDTO):
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



    async def delete_reader(self, reader_id: int):
        try:
            existing_reader = await self.db.readers.get_one_or_none(id = reader_id)
            if existing_reader:
                await self.db.readers.delete(id=reader_id)
                await self.db.commit()
            else:
                raise ReaderBadIdHTTPException
        except (ObjectNotFoundException):
            raise ReaderBadIdHTTPException


