from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound

from src.exceptions import ObjectNotFoundException
from src.models import BorrowedBookORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ServicesDataMapper


class ServicesBorrowedRepository(BaseRepository):
    model = BorrowedBookORM
    mapper = ServicesDataMapper

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [model for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()


    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return model

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            return result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
