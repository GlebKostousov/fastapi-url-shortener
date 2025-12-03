from fastapi import APIRouter, Depends

from dependencies.auth import user_basic_auth_required_for_unsafe_methods
from views.short_urls.create_views import router as create_router
from views.short_urls.delete_views import router as delete_router
from views.short_urls.list_views import router as list_router
from views.short_urls.update_views import router as update_router

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs views"],
    dependencies=[Depends(user_basic_auth_required_for_unsafe_methods)],
)
router.include_router(list_router)
router.include_router(create_router)
router.include_router(update_router)
router.include_router(delete_router)
