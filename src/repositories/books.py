from src.models.books import BookModelORM
from src.models.readers import ReadersORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper, BookDataMapper


class BooksRepository(BaseRepository):
    model = BookModelORM
    mapper = BookDataMapper
