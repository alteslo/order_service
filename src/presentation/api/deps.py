from collections.abc import AsyncGenerator
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.core.security import decode_access_token
from src.domain.entities import User
from src.domain.repositories import IUnitOfWork
from src.infrastructure.database import AsyncSession, get_db_session
from src.infrastructure.database.uow import UnitOfWork


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")


async def get_uow(session: Annotated[AsyncSession, Depends(get_db_session)]) -> AsyncGenerator[IUnitOfWork, None]:
    """Зависимость для получения UnitOfWork."""
    async with UnitOfWork(session) as uow:
        yield uow


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
) -> User:
    """
    Зависимость для получения текущего пользователя из JWT токена.
    Возвращает HTTP 401 ошибку, если токен невалиден или пользователь не найден.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_access_token(token)
    if token_data is None or token_data.user_id is None:
        raise credentials_exception
    user = await uow.users.get_by_id(UUID(token_data.user_id))
    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
UnitOfWorkDep = Annotated[IUnitOfWork, Depends(get_uow)]
