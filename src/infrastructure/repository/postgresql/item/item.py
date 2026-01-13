from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

from api.pydantic.item.models import ItemSchema, ItemSchemaResponse
from infrastructure.databases.postgresql.models.item import Item

# Работа с сессией/базой данных
class PostgreSQLItemRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_item(self, schema: ItemSchema) -> ItemSchemaResponse:
        item = Item(
            name=schema.name,
            category=schema.category,
            count=schema.count,
            price=schema.price
        )
        self._session.add(item)
        await self._session.flush()

        response = ItemSchemaResponse(
            id=item.id,
            name=item.name,
            category=item.category,
            count=item.count,
            price=item.price
        )
        return response


    async def get_item(self, item_id: int) -> ItemSchemaResponse | None:
        item: Item | None = await self._session.get(Item, item_id)
        if item is not None:
            response = ItemSchemaResponse(
                id=item.id,
                name=item.name,
                category=item.category,
                count=item.count,
                price=item.price
            )
            return response
        return None



    async def get_items(self, *, limit: int = 100, offset: int = 0) -> List[ItemSchemaResponse] | None:
        responses: List[ItemSchemaResponse] = []
        for i in range(offset + 1, offset + limit + 1):
            item: Item | None = await self._session.get(Item, i)
            if item is not None:
                response_item = ItemSchemaResponse(
                    id=item.id,
                    name=item.name,
                    category=item.category,
                    count=item.count,
                    price=item.price
                )
                responses.append(response_item)
        if len(responses) != 0:
            return responses
        return None


    async def delete_item(self, item_id: int) -> Dict | None:
        item = await self._session.get(Item, item_id)
        if item is not None:
            await self._session.delete(item)
            await self._session.flush()
            return {"Item deleted": item_id}
        return None

    async def update_item(self, item_id: int, schema: ItemSchema) -> ItemSchemaResponse | None:
        item: Item | None = await self._session.get(Item, item_id)
        if item is not None:
            new_item = Item(
                id=item.id,
                name=schema.name,
                category=schema.category,
                count=schema.count,
                price=schema.price
            )
            await self._session.merge(new_item)
            await self._session.flush()

            response = ItemSchemaResponse(
                id=item.id,
                name=item.name,
                category=item.category,
                count=item.count,
                price=item.price
            )
            return response
        return None