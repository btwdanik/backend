from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from api.pydantic.user.models import UserSchema, UserSchemaResponse
from infrastructure.databases.postgresql.models.user import User

# Работа с сессией/базой данных
class PostgreSQLUserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, schema: UserSchema) -> UserSchemaResponse:
        user = User(
            username=schema.username,
            password=schema.password,
            email=schema.email,
            title=schema.title,
        )
        self._session.add(user)
        await self._session.flush()

        response = UserSchemaResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            title=user.title
        )
        return response


    async def get_user(self, user_id: int) -> UserSchemaResponse | None:
        user: User | None = await self._session.get(User, user_id)
        if user is not None:
            response = UserSchemaResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                title=user.title
            )
            return response
        return None

    async def delete_user(self, user_id: int) -> Dict | None:
        user = await self._session.get(User, user_id)
        if user is not None:
            await self._session.delete(user)
            await self._session.flush()
            return {"User deleted" : user_id}
        return None