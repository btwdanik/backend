from fastapi.security import OAuth2PasswordRequestForm

from .abstract import AbstractCreateUserUC
from api.pydantic.user.models import UserSchema

class PostgreSQLCreateUserUC(AbstractCreateUserUC):
    def __init__(self, uow):
        self._uow = uow

    async def create(self, schema: UserSchema):
        async with self._uow as uow:
            user = await uow.repository.create_user(schema)
        return user

    async def login(self, schema: OAuth2PasswordRequestForm):
        async with self._uow as uow:
            user = await uow.repository.login_user(schema)
        return user

    async def get(self, token: str):
        async with self._uow as uow:
            user = await uow.repository.get_user(token)
        return user