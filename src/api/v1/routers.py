from fastapi import APIRouter

from api.v1.item import routers as item_router
from api.v1.authorization import routers as authorization_router
from api.v1.user import routers as user_router


router = APIRouter(prefix="/api/v1")
router.include_router(item_router.router)
router.include_router(authorization_router.router)
router.include_router(user_router.router)