from fastapi import APIRouter

from api.v1.authorization.views import router as authorization_router

router = APIRouter()

router.include_router(authorization_router)