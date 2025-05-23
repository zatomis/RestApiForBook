from fastapi import APIRouter, Response
from jwt import ExpiredSignatureError

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    IncorrectPasswordHTTPException,
    IncorrectPasswordException,
    EmailNotRegisteredHTTPException,
    EmailNotRegisteredException,
    UserAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException, NoAccessTokenHTTPException,
)
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", summary="🧑‍💻 Мой профиль")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    try:
        getme = await AuthService(db).get_one_or_none_user(user_id)
        return getme
    except ExpiredSignatureError:
        raise NoAccessTokenHTTPException
    except Exception:
        raise NoAccessTokenHTTPException


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
