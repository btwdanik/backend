from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Depends
from typing import List

from .dependencies import create_user_user_case
from api.pydantic.user.models import Info, UserSchema, UserSchemaResponse
from usecase.user.implementation import PostgreSQLCreateUserUC

from api.pydantic.user.models import UserSchema
router = APIRouter(prefix="/users")

@router.get("/{user_id}", tags=[Info.user_id_info], response_model=UserSchemaResponse)
async def get_info_user_by_id(
        user_id: int,
        repo: PostgreSQLCreateUserUC = Depends(create_user_user_case)
    ) -> JSONResponse:

    user = await repo.get(user_id)

    if user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.model_dump())

@router.post("", tags=[Info.user_create], response_model=UserSchemaResponse)
async def post_user(
        payload: UserSchema,
        repo: PostgreSQLCreateUserUC = Depends(create_user_user_case),
    ) -> JSONResponse:

    user = await repo.create(payload)

    if user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=user.model_dump())


@router.delete("/{user_id}", tags=[Info.user_delete])
async def delete_user(
        user_id: int,
        repo: PostgreSQLCreateUserUC = Depends(create_user_user_case)
    ) -> JSONResponse:

    result = await repo.delete(user_id)

    if result is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=result)
