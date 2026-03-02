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
            raise Exception("\033[32mINFO\033[0m:     DatabaseSessionManager is not initialized")
        else:
            try:
                await self.create_tables()
                print("\033[32mINFO\033[0m:     The connection was established")
                print("\033[32mINFO\033[0m:     Tables created")
            except Exception:
                print("\033[31mERROR\033[0m:     The connection was not established")
                print("\033[31mERROR\033[0m:     Tables creation failed")
                raise Exception("No connection")

    async def close(self) -> None:
        if self._engine is None:
            raise Exception("\033[31mERROR\033[0m:     DatabaseSessionManager is not initialized")

        # await self.delete_tables()
        # print("INFO:    Tables deleted") # drop all base, when you leave

        await self._engine.dispose()
        self._engine = None
        self._session = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncSession]:
        if self._engine is None:
            raise Exception("\033[31mERROR\033[0m:     DatabaseSessionManager is not initialized")

        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception:
                await conn.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session is None:
            raise Exception("\033[31mERROR\033[0m:     DatabaseSessionManager is not initialized")

        async with self._session() as session:
            yield session

    async def create_tables(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def delete_tables(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)