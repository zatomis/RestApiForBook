from src.models import BorrowedBookORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ServicesDataMapper


class ServicesBorrowedRepository(BaseRepository):
    model = BorrowedBookORM
    mapper = ServicesDataMapper
