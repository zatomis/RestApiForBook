# ruff: noqa: E402
import json
from typing import AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, async_session_maker_null_pool
from src.main import app
from src.models import *  # noqa
from httpx import AsyncClient

from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


#@pytest.fixture(scope="session", autouse=True)
#async def setup_database(check_test_mode):
#    async with engine_null_pool.begin() as conn:
#        await conn.run_sync(Base.metadata.drop_all)
#        await conn.run_sync(Base.metadata.create_all)

#    with open("tests/.json", encoding="utf-8") as file_rooms:
#        . = json.load(file_rooms)

#    .. = [..model_validate(room) for room in rooms]

#    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
#        await db_..add_bulk(rooms)
#        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac: AsyncClient, setup_database):
    await ac.post("/auth/register", json={"email": "kot@pes.com", "password": "1234"})


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac: AsyncClient):
    await ac.post("/auth/login", json={"email": "kot@pes.com", "password": "1234"})
    assert ac.cookies["access_token"]
    yield ac
