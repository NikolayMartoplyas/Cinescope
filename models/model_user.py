import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from constant.enums import RolesEnum

class UserTest(BaseModel):
    """Класс для валидации данных юзера при отправки на сервер"""
    email: str = Field(..., description="Email пользователя")
    fullName: str = Field(..., description="Полное имя пользователя")
    password: str = Field(..., min_length=8, description="Пароль пользователя")
    passwordRepeat: str = Field(..., description="Подтверждение пароля")
    roles: list[RolesEnum] = Field(..., description="роль пользователя")
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    class Config:
        use_enum_values = True
        json_encoders = {
            RolesEnum: lambda v: v.value
        }

class RegisterUserResponse(BaseModel):
    """Класс для валидации ответа данных юзера"""
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str =  Field(min_length=1, max_length=100, description="Имя пользователя")
    roles: list[RolesEnum]
    verified: bool
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")
    banned: Optional[bool] = None

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        """Валидатор поля createdAt"""
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value

    class Config:
        use_enum_values = True
        json_encoders = {
            RolesEnum: lambda v: v.value
        }

class User(BaseModel):
    id: str = Field(..., description="ID пользователя")
    email: str = Field(..., description="Email пользователя")
    fullName: str = Field(..., description="Полное имя пользоваителя")
    roles: list[str] = Field(..., min_length=1, description="Роль пользователя")

class LoginUserResponse(BaseModel):
    user: User = Field(..., description="Данные пользователя")
    accessToken: str = Field(..., description="Токен пользователя")
    refreshToken: str = Field(..., description="Рефреш токен")
    expiresIn: int = Field(...)


