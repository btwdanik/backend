from .abstract import AbstractCreateItemUC
from api.pydantic.item.models import ItemSchema

class PostgreSQLCreateItemUC(AbstractCreateItemUC):
    def __init__(self, uow):
        self._uow = uow

    async def create(self, schema: ItemSchema):
        async with self._uow as uow:
            item = await uow.repository.create_item(schema)
        return item

    async def get(self, number: int):
        async with self._uow as uow:
            item = await uow.repository.get_item(number)
        return item

    async def gets(self, limit: int, offset: int):
        async with self._uow as uow:
            items = await uow.repository.get_items(limit=limit, offset=offset)
        return items

    async def delete(self, number: int):
        async with self._uow as uow:
            item = await uow.repository.delete_item(number)
        return item

    async def update(self, number: int, schema: ItemSchema):
        async with self._uow as uow:
            item = await uow.repository.update_item(item_id=number, schema=schema)
        return item





