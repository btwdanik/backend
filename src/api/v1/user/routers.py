from fastapi import APIRouter

from api.v1.user.views import router as user_router

router = APIRouter()

router.include_router(user_router)