from typing import List
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from api.pydantic.item.models import ItemSchema, ItemSchemaResponse
from infrastructure.databases.postgresql.models.item import Item
from infrastructure.repository.postgresql.utils.token import decode_token

class PostgreSQLItemRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_item(self, schema: ItemSchema, token: str) -> JSONResponse:
        user_id = decode_token(token).get('id')
        item = Item(
            name=schema.name,
            category=schema.category,
            count=schema.count,
            price=schema.price,
            user_id=user_id
        )
        self._session.add(item)
        await self._session.flush()
        content = ItemSchemaResponse(
            id=item.id,
            name=item.name,
            category=item.category,
            count=item.count,
            price=item.price
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=content.model_dump()
        )


    async def get_item(self, item_id: int, token: str) -> JSONResponse:
        user_id = decode_token(token).get('id')
        item: Item | None = await self._session.get(Item, item_id)
        if (item is not None) and (item.user_id == user_id):
            content = ItemSchemaResponse(
                id=item.id,
                name=item.name,
                category=item.category,
                count=item.count,
                price=item.price
            )
            return JSONResponse(status_code=status.HTTP_200_OK, content=content.model_dump())
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Item not found"})


    async def get_items(self, *, limit: int = 100, offset: int = 0, token: str) -> JSONResponse:
        user_id = decode_token(token).get('id')
        content: List[ItemSchemaResponse] = []
        for i in range(offset + 1, offset + limit + 1):
            item: Item | None = await self._session.get(Item, i)
            if (item is not None) and (item.user_id == user_id):
                content_item = ItemSchemaResponse(
                    id=item.id,
                    name=item.name,
                    category=item.category,
                    count=item.count,
                    price=item.price
                )
                content.append(content_item)
        if len(content) != 0:
            return JSONResponse(status_code=status.HTTP_200_OK, content=[x.model_dump() for x in content])
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Items not found"})


    async def delete_item(self, item_id: int, token: str) -> JSONResponse:
        user_id = decode_token(token).get('id')
        item = await self._session.get(Item, item_id)
        if (item is not None) and (item.user_id == user_id):
            await self._session.delete(item)
            await self._session.flush()
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Item deleted"})
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Item not found"})


    async def update_item(self, item_id: int, schema: ItemSchema, token: str) -> JSONResponse:
        user_id = decode_token(token).get('id')
        item: Item | None = await self._session.get(Item, item_id)
        if (item is not None) and (item.user_id == user_id):
            new_item = Item(
                id=item.id,
                name=schema.name,
                category=schema.category,
                count=schema.count,
                price=schema.price,
                user_id=user_id
            )
            await self._session.merge(new_item)
            await self._session.flush()
            content = ItemSchemaResponse(
                id=item.id,
                name=item.name,
                category=item.category,
                count=item.count,
                price=item.price
            )
            return JSONResponse(status_code=status.HTTP_200_OK, content=content.model_dump())
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Item not found"})