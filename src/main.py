from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.routers import router
from container import Container
from settings import Settings

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
        "infrastructure.databases.postgresql.session.session",
        "api.v1.item.dependencies",
        "api.v1.user.dependencies"
    ]
)

main = FastAPI(tags=["api"], lifespan=lifespan)
main.include_router(router)