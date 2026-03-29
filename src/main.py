from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.routers import router
from src.container import Container
from src.settings import Settings

container = Container()
settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager = container.session_manager()
    # @localhost -> db, если в одной сети
    await sessionmanager.init(base_url=f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}")
    try:
        yield

    finally:
        await sessionmanager.close()

container.wire(
    modules=[
        "src.infrastructure.databases.postgresql.session.session",
        "src.api.v1.item.dependencies",
        "src.api.v1.user.dependencies"
    ]
)

main = FastAPI(tags=["api"], lifespan=lifespan)
main.include_router(router)