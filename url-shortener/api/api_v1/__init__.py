from fastapi import APIRouter
from api.api_v1.short_urls.views.list_views import router as short_urls_router

router = APIRouter(prefix="/v1")

router.include_router(short_urls_router)
