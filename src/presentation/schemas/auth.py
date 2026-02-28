from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """Схема запроса для регистрации пользователя."""

    username: str
    email: str
    password: str = Field(..., min_length=8, description="Пароль должен быть не менее 8 символов")


class UserRegisterResponse(BaseModel):
    """Схема ответа при регистрации пользователя."""

    username: str
    email: EmailStr
    message: str = "Пользователь успешно зарегистрирован"


class TokenRequest(BaseModel):
    """Схема запроса для получения токена."""

    email: EmailStr
    username: str
    password: str


class TokenResponse(BaseModel):
    """Схема ответа при выдаче токена."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Схема данных, содержащихся в токене."""

    user_id: str | None = None
    email: str | None = None
