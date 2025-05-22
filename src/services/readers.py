from src.exceptions import ObjectNotFoundException
from src.schemas.readers import ReaderCreateDTO
from src.services.base import BaseService


class ReaderService(BaseService):
    async def create_reader(self, reader_data: ReaderCreateDTO):
        reader = await self.db.readers.add(reader_data)
        await self.db.commit()
        return reader







