__all__ = ("router",)

from api.api_v1.short_urls.views.details_views import router as details_router
from api.api_v1.short_urls.views.list_views import router

router.include_router(details_router)
