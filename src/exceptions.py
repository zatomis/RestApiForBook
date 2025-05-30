from fastapi import HTTPException


class LibraryException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(LibraryException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(LibraryException):
    detail = "Похожий объект уже существует"


class IncorrectTokenException(LibraryException):
    detail = "Некорректный токен"


class EmailNotRegisteredException(LibraryException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(LibraryException):
    detail = "Пароль неверный"


class IncorrectException(LibraryException):
    detail = "Ошибка в указании Логин-Пароль"


class UserAlreadyExistsException(LibraryException):
    detail = "Пользователь уже существует"

class BookAlreadyExistsException(LibraryException):
    detail = "Такая книга уже существует"


class LibraryHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectTokenHTTPException(LibraryHTTPException):
    detail = "Некорректный токен"


class EmailNotRegisteredHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class ReaderNotRegisteredHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Пользователь не зарегистрирован"

class ReaderBadIdHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Пользователь не существует"

class BookBadHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Не верный id для обновления "

class BookBadIdHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Не верный id "



class BookBadCopyHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Копий не может быть меньше 0"

class BookNotFoundHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Такой книги не существует"



class UserEmailAlreadyExistsHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"

class BookIsbnAlreadyExistsHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Книга с таким isbn уже существует"


class IncorrectPasswordHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class NoAccessTokenHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"
