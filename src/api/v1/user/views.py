from fastapi import APIRouter

from api.pydantic.user.models import UserSchema
router = APIRouter(prefix="/users")

@router.post("/", tags=["users"])
async def create_user(
        user: UserSchema
):
