from src.models import BorrowedBookORM
from src.models.books import BookModelORM
from src.models.readers import ReadersORM
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.books import BookDTO
from src.schemas.readers import ReaderDTO
from src.schemas.users import User


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User

class BookDataMapper(DataMapper):
    db_model = BookModelORM
    schema = BookDTO

class ReaderDataMapper(DataMapper):
    db_model = ReadersORM
    schema = ReaderDTO

class ServicesDataMapper(DataMapper):
    db_model = BorrowedBookORM
    schema = ReaderDTO