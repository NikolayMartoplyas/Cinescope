import datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from constant.enums import LocationEnum

class MoviesModel(BaseModel):
    """Класс для валидации данных фильма при отправки на сервер"""
    name: str = Field(..., description="Название фильма")
    imageUrl: str = Field(..., description="URl картинки фильма")
    price: int = Field(..., description="Цена билета")
    description: str = Field(..., description="Описание фильма")
    location: LocationEnum = Field(..., description="локация фильма")
    published: bool = Field(..., description="Публикация фильма")
    genreId: int = Field(..., description="ID жанра фильма")

class MoviesModelResponse(BaseModel):
    """Класс для валидации данных ответа о фильме"""
    model_config = ConfigDict(use_enum_values=True) #преобразует в ответе <LocationEnum.SPB: 'SPB'> просто в строку SPB
    id: int = Field(..., description="ID Фильма")
    name: str = Field(..., description="название фильма")
    price: int = Field(..., description="цена билета на фильм")
    description: str = Field(..., description="Описание фильма")
    imageUrl: str = Field(..., description="URl картинки фильма")
    location: LocationEnum = Field(..., description="локация фильма")
    published: bool = Field(..., description="Публикация фильма")
    rating: int = Field(..., description="Рейтинг фильма")
    genreId: int = Field(..., description="ID жанра фильма")
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")
    genre: dict = Field(..., description="Название жанра фильма")

    @field_validator("createdAt")
    def validate_ctreated_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value

    class Cinfig:
        use_enum_values = True
        json_encoders = {
            LocationEnum: lambda v: v.value
        }
class MoviesModelErrorResponse(BaseModel):
    message:str | list[str] = Field(..., description="Сообщение об ошибке")
    error: Optional[str] = Field(default=None, description="Название ошибки")
    statusCode: int = Field(..., description="код ошибки")