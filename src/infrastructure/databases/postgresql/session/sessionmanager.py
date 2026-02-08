from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from infrastructure.databases.postgresql.session.base import Base

class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._session: async_sessionmaker | None = None

    async def init(self, base_url: str):
        self._engine = create_async_engine(base_url)
        self._session = async_sessionmaker(autocommit=False, bind=self._engine, expire_on_commit=False)

        if self._session is None:
            raise Exception("INFO:     DatabaseSessionManager is not initialized")
        else:
            print('INFO:     DatabaseSessionManager is initialized')

            try:
                await self.create_tables()
                print("INFO:     Tables created")
            except Exception:
                raise Exception("Error, Tables creation failed")

    async def close(self) -> None:
        if self._engine is None:
            raise Exception("INFO:     DatabaseSessionManager is not initialized")

        # await self.delete_tables()
        # print("INFO:    Tables deleted") # drop all base, when you leave

        await self._engine.dispose()
        self._engine = None
        self._session = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncSession]:
        if self._engine is None:
            raise Exception("INFO:     DatabaseSessionManager is not initialized")

        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception:
                await conn.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session is None:
            raise Exception("INFO:     DatabaseSessionManager is not initialized")

        async with self._session() as session:
            yield session

    async def create_tables(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def delete_tables(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)