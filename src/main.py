from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.v1.routers import router
from container import Container
container = Container()

@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager = container.session_manager()
    await sessionmanager.init(base_url="postgresql+asyncpg://user:1234@localhost:5432/db_sql") #@localhost -> db, если в одной сети
    try:
        yield

    finally:
        await sessionmanager.close()

container.wire(
    modules=[
        "infrastructure.databases.postgresql.session.session",
        "api.v1.item.dependencies"
    ]
)

main = FastAPI(tags=["api"], lifespan=lifespan)
main.include_router(router)