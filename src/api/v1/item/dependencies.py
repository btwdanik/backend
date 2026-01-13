from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.di.injection import build_item_uow
from infrastructure.databases.postgresql.session.session import get_async_session
from infrastructure.repository.postgresql.item.uow import PostgreSQLItemRepositoryUOW
from usecase.item.implementation import PostgreSQLCreateItemUC

# Реализация без UseCases
def _item_user_case(session: AsyncSession = Depends(get_async_session)
) -> PostgreSQLItemRepositoryUOW:

    return build_item_uow(session=session)


# Еще один способ реализации через определенные правила (UseCases)
def create_item_user_case(
    session: AsyncSession = Depends(get_async_session)
) -> PostgreSQLCreateItemUC:

    uow = _item_user_case(session=session)
    return PostgreSQLCreateItemUC(uow=uow)
