from sqlalchemy.ext.asyncio import AsyncSession

from container import Container
from infrastructure.repository.postgresql.item.uow import PostgreSQLItemRepositoryUOW

# Самая начальная точка
def build_item_uow(session: AsyncSession) -> PostgreSQLItemRepositoryUOW:
    return Container.session_item(session=session)