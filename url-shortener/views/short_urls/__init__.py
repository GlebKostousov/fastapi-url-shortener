from fastapi import APIRouter

from views.short_urls.create_views import router as create_router
from views.short_urls.list_views import router as list_router

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs views"],
)
router.include_router(list_router)
router.include_router(create_router)
