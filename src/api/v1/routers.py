from fastapi import APIRouter

from api.v1.item import routers as item_routers


router = APIRouter(prefix="/api/v1")
router.include_router(item_routers.router)