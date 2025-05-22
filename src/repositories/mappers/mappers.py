from src.models.readers import ReadersORM
from src.models.users import UsersOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.readers import ReaderDTO
from src.schemas.users import User


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User

class ReaderDataMapper(DataMapper):
    db_model = ReadersORM
    schema = ReaderDTO