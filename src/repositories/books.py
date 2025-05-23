from src.models.books import BookModelORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookDataMapper


class BooksRepository(BaseRepository):
    model = BookModelORM
    mapper = BookDataMapper
