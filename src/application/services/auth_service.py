from datetime import timedelta

from src.core.config import settings
from src.core.security import create_access_token, get_password_hash, verify_password
from src.domain.entities import User
from src.domain.repositories import IUnitOfWork
from src.presentation.schemas import TokenResponse


class AuthService:
    """Сервис аутентификации"""

    @staticmethod
    async def register(uow: IUnitOfWork, username: str, email: str, password: str) -> User:
        """Регистрация нового пользователя"""
        existing = await uow.users.get_by_email(email)  # проверка занят ли email
        if existing:
            raise ValueError("User with this email already exists")

        # Создание пользователя
        password_hash = get_password_hash(password)
        user = User.create(username, email, password_hash)
        await uow.users.add(
            user
        )  # TODO Имеет ли смысл использовать uow, если SQLAlchemy использует этот паттерн внутри своих механизмов
        await uow.commit()
        return user

    @staticmethod
    async def authenticate(uow: IUnitOfWork, email: str, password: str):
        """Аутентификация пользователя"""
        user = await uow.users.get_by_email(email)

        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    async def create_token_response(user: User) -> TokenResponse:
        """Создание ответа с JWT токеном для аутентифицированного пользователя"""
        # Генерация токена и формирование ответа
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email.value},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        )
        return TokenResponse(access_token=access_token)
