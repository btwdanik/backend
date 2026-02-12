from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from starlette.responses import JSONResponse
from fastapi import status

from .utils import create_refresh_token, create_access_token, decode_token
from api.pydantic.user.models import *
from infrastructure.databases.postgresql.models.user import User

# Работа с сессией/базой данных
class PostgreSQLUserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, payload: UserSchema) -> JSONResponse:
        schema = select(User).where(
            or_(
                User.email == payload.email,
                User.username == payload.username
            )
        )
        result = await self._session.execute(schema)
        user = result.scalar_one_or_none()
        if user is not None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "User already exists"}
            )

        schema = UserSchemaRefreshToken(
            sub=payload.username,
        )
        user = User(
            username=payload.username,
            password=payload.password,
            email=payload.email,
            refresh_token=create_refresh_token(schema),
        )

        self._session.add(user)
        await self._session.flush()

        response = UserSchemaResponse(
            id=user.id,
            username=user.username,
            email=user.email,
        )
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=response.model_dump()
        )

    async def login_user(self, payload: UserSchemaLogin) -> JSONResponse:
        schema = select(User).where(
            and_(
                User.username == payload.username,
                User.password == payload.password
            )
        )

        result = await self._session.execute(schema)
        user = result.scalar_one_or_none()

        if user is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "User not found"}
            )
        response = TokenAccessResponse(
                access_token=create_access_token(UserSchemaAccessToken(sub=user.username)),
                token_type="bearer"
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response.model_dump()
        )


    async def get_user(self, token: str) -> JSONResponse:
        payload = decode_token(token)
        print(payload.get('sub'))
        schema = select(User).where(User.username == payload.get('sub'))
        result = await self._session.execute(schema)
        user = result.scalar_one_or_none()

        content = UserSchemaResponse(
            id=user.id,
            username=user.username,
            email=user.email,
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=content.model_dump()
        )