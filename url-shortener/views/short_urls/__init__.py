from fastapi import APIRouter

from views.short_urls.list_views import router as list_router

router = APIRouter(
    prefix="/short-urls",
)
router.include_router(list_router)
