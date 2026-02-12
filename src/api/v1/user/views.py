from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from .dependencies import create_user_user_case
from api.pydantic.user.models import UserSchemaResponse, UserSchemaLogin, TokenAccessResponse
from usecase.user.implementation import PostgreSQLCreateUserUC

from api.pydantic.user.models import UserSchema
router = APIRouter(prefix="/users/auth", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/auth/login")

@router.post("/register", response_model=UserSchemaResponse)
async def register_user(
        payload: UserSchema,
        repo: PostgreSQLCreateUserUC = Depends(create_user_user_case),
    ) -> JSONResponse:

    user = await repo.create(payload)
    return user

@router.post("/login", response_model=TokenAccessResponse)
async def login_user(
        payload: OAuth2PasswordRequestForm = Depends(),
        repo: PostgreSQLCreateUserUC = Depends(create_user_user_case),
    ) -> JSONResponse:
    result = UserSchemaLogin(
        username=payload.username,
        password=payload.password,
    )
    user = await repo.login(result)
    return user

@router.get("/me", response_model=UserSchemaResponse)
async def get_info_by_me(
        token: str = Depends(oauth2_scheme),
        repo: PostgreSQLCreateUserUC = Depends(create_user_user_case)
    ) -> JSONResponse:

    user = await repo.get(token)
    return user