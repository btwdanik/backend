from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.di.injection import build_user_uow
from infrastructure.databases.postgresql.session.session import get_async_session
from infrastructure.repository.postgresql.user.uow import PostgreSQLUserRepositoryUOW
from usecase.user.implementation import PostgreSQLCreateUserUC

def _user_user_case(session: AsyncSession = Depends(get_async_session)
) -> PostgreSQLUserRepositoryUOW:

    return build_user_uow(session=session)

def create_user_user_case(
    session: AsyncSession = Depends(get_async_session)
) -> PostgreSQLCreateUserUC:

    uow = _user_user_case(session=session)
    return PostgreSQLCreateUserUC(uow=uow)