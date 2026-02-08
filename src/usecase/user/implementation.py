from .abstract import AbstractCreateUserUC
from api.pydantic.user.models import UserSchema

class PostgreSQLCreateUserUC(AbstractCreateUserUC):
    def __init__(self, uow):
        self._uow = uow

    async def create(self, schema: UserSchema):
        async with self._uow as uow:
            user = await uow.repository.create_user(schema)
        return user

    async def get(self, number: int):
        async with self._uow as uow:
            user = await uow.repository.get_user(number)
        return user

    async def delete(self, number: int):
        async with self._uow as uow:
            user = await uow.repository.delete_user(number)
        return user