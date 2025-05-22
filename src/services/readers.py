from src.exceptions import ObjectNotFoundException, UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, \
    ObjectAlreadyExistsException
from src.schemas.readers import ReaderCreateDTO
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
        readers = await self.db.readers.get_all()
        return readers









