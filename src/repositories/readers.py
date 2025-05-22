from src.models.readers import ReadersORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper, ReaderDataMapper


class ReadersRepository(BaseRepository):
    model = ReadersORM
    mapper = ReaderDataMapper
