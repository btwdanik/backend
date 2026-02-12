from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Depends
from typing import List


from .dependencies import create_item_user_case
from api.pydantic.item.models import ItemSchema, ItemSchemaResponse, Pagination
from usecase.item.implementation import PostgreSQLCreateItemUC

#TODO: add user | another = Depends(current_active_user) in all endpoints

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/{item_id}", response_model=ItemSchemaResponse)
async def get_info_item_by_id(
        item_id: int,
        repo: PostgreSQLCreateItemUC = Depends(create_item_user_case)
    ) -> JSONResponse:

    item = await repo.get(item_id)

    if item is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    return JSONResponse(status_code=status.HTTP_200_OK, content=item.model_dump())


@router.get("", response_model=List[ItemSchemaResponse])
async def get_info_items(
        pagination: Pagination = Depends(),
        repo: PostgreSQLCreateItemUC = Depends(create_item_user_case)
    ) -> JSONResponse:

    items = await repo.gets(limit=pagination.limit, offset=pagination.offset)

    if items is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])
    return JSONResponse(status_code=status.HTTP_200_OK, content=[item.model_dump() for item in items])


@router.post("", response_model=ItemSchemaResponse)
async def post_item(
        payload: ItemSchema,
        repo: PostgreSQLCreateItemUC = Depends(create_item_user_case),
    ) -> JSONResponse:

    item = await repo.create(payload)

    if item is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item.model_dump())


@router.delete("/{item_id}")
async def delete_item(
        item_id : int,
        repo: PostgreSQLCreateItemUC = Depends(create_item_user_case)
    ) -> JSONResponse:

    result = await repo.delete(item_id)

    if result is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=result)


@router.put("/{item_id}", response_model=ItemSchemaResponse)
async def put_item(item_id : int,
        item: ItemSchema,
        repo: PostgreSQLCreateItemUC = Depends(create_item_user_case)
    ) -> JSONResponse:

    item = await repo.update(number=item_id, schema=item)

    if item is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=item.model_dump())
