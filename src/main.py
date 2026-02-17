from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from pathlib import Path

from api.v1.routers import router
from container import Container
from web.router import router as web_router

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
        "api.v1.item.dependencies",
        "api.v1.user.dependencies"
    ]
)


BASE_DIR = Path(__file__).resolve().parent

main = FastAPI(tags=["api"], lifespan=lifespan)
main.include_router(router)
main.include_router(web_router)
main.mount("/static", StaticFiles(directory="web/static"), name="static")