from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.services.readers import ReaderService
from src.schemas.readers import ReaderCreateDTO

router = APIRouter(prefix="/readers", tags=["Управление читателями"])


@router.post("")
async def create_reader(db: DBDep, reader_data: ReaderCreateDTO = Body()):
    reader = await ReaderService(db).create_reader(reader_data)
    return {"status": "OK", "data": reader}

