import logging

from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, ReaderNotRegisteredHTTPException
from src.services.readers import ReaderService
from src.schemas.readers import ReaderCreateDTO, ReaderUpdateDTO

router = APIRouter(prefix="/books", tags=["Управление книгами"])
logging.basicConfig(level=logging.INFO)


@router.post("")
async def create_reader(db: DBDep, reader_data: ReaderCreateDTO = Body()):
    reader = await ReaderService(db).create_reader(reader_data)
    return {"status": "OK", "data": reader}


@router.get("")
@cache(expire=10)
async def read_readers(user_id: UserIdDep, db: DBDep):
    logging.info(f"user {user_id}")
    return await ReaderService(db).read_readers()


@router.get("/{reader_id}")
async def read_readers_by_id(reader_id: int, db: DBDep):
    try:
        return await ReaderService(db).read_readers_by_id(reader_id)
    except ObjectNotFoundException:
        raise ReaderNotRegisteredHTTPException


@router.put("/{reader_id}")
async def edit_reader_by_id(reader_id: int, db: DBDep, reader_data: ReaderUpdateDTO = Body()):
    try:
        await ReaderService(db).edit_reader(reader_id, reader_data)
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise ReaderNotRegisteredHTTPException


@router.delete("/{reader_id}")
async def delete_reader(reader_id: int, db: DBDep):
    try:
        await ReaderService(db).delete_reader(reader_id)
        return {"status": "OK"}
    except ObjectNotFoundException:
        raise ReaderNotRegisteredHTTPException
