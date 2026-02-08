from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/authorization")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
