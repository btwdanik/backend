from sqlalchemy.ext.asyncio import AsyncSession

from .item import PostgreSQLItemRepository

class PostgreSQLItemRepositoryUOW:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
        self.repository: PostgreSQLItemRepository | None = None

    async def __aenter__(self):
        self.repository = PostgreSQLItemRepository(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self._session.rollback()
        await self._session.commit()

        await self._session.close()
        self.repository = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()