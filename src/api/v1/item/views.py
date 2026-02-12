from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from typing import List

from .dependencies import create_item_user_case, get_current_user
from api.pydantic.item.models import ItemSchema, ItemSchemaResponse, Pagination
from usecase.item.implementation import PostgreSQLCreateItemUC

router = APIRouter(prefix="/users/items", tags=["Items"])


@router.post("", response_model=ItemSchemaResponse)
async def post_item(
        payload: ItemSchema,
        token: str = Depends(get_current_user),
        repo: PostgreSQLCreateItemUC = Depends(create_item_user_case),
    ) -> JSONResponse:

    item = await repo.create(payload, token)
    return item


@router.get("/{item_id}", response_model=ItemSchemaResponse)
async def get_info_item_by_id(
        item_id: int,
        token: str = Depends(get_current_user),
        repo: PostgreSQLCreateItemUC = Depends(create_item_user_case)
    ) -> JSONResponse:

    item = await repo.get(item_id, token)
    return item


@router.get("", response_model=List[ItemSchemaResponse])
async def get_info_items(
        pagination: Pagination = Depends(),
        token: str = Depends(get_current_user),
        repo: PostgreSQLCreateItemUC = Depends(create_item_user_case)
    ) -> JSONResponse:

    items = await repo.gets(limit=pagination.limit, offset=pagination.offset, token=token)
    return items


@router.delete("/{item_id}")
async def delete_item(
        item_id : int,
        token: str = Depends(get_current_user),
        repo: PostgreSQLCreateItemUC = Depends(create_item_user_case)
    ) -> JSONResponse:

    result = await repo.delete(item_id, token)
    return result


@router.put("/{item_id}", response_model=ItemSchemaResponse)
async def put_item(item_id : int,
        item: ItemSchema,
        token: str = Depends(get_current_user),
        repo: PostgreSQLCreateItemUC = Depends(create_item_user_case)
    ) -> JSONResponse:

    item = await repo.update(number=item_id, schema=item, token=token)
    return item
