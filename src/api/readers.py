from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.services.readers import ReaderService
from src.schemas.readers import ReaderCreateDTO

router = APIRouter(prefix="/readers", tags=["Управление читателями"])


@router.post("")
async def create_reader(db: DBDep, reader_data: ReaderCreateDTO = Body()):
    reader = await ReaderService(db).create_reader(reader_data)
    return {"status": "OK", "data": reader}


@router.get("")
@cache(expire=10)
async def read_readers(db: UserIdDep):
    return await ReaderService(db).read_readers()
