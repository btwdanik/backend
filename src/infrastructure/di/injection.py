from sqlalchemy.ext.asyncio import AsyncSession

from container import Container
from infrastructure.repository.postgresql.item.uow import PostgreSQLItemRepositoryUOW
from infrastructure.repository.postgresql.user.uow import PostgreSQLUserRepositoryUOW

# Самая начальная точка
def build_item_uow(session: AsyncSession) -> PostgreSQLItemRepositoryUOW:
    return Container.session_item(session=session)

def build_user_uow(session: AsyncSession) -> PostgreSQLUserRepositoryUOW:
    return Container.session_user(session=session)