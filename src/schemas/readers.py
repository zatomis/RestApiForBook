from pydantic import BaseModel, EmailStr


# Pydantic модели для валидации данных
class ReaderCreateDTO(BaseModel):
    name: str
    email: EmailStr  # Проверка формата email

class ReaderUpdateDTO(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class ReaderDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        orm_mode = True

