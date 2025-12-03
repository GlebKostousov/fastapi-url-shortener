from logging import getLogger

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from schemas.short_url import ShortUrlUpdate
from services.short_urls import FormResponseHelper

logger = getLogger(__name__)
router = APIRouter(
    prefix="/{slug}/update",
)

form_response = FormResponseHelper(
    model=ShortUrlUpdate,
    template_name="short_urls/update.html",
)


@router.get(
    path="/",
    name="short-urls:update-views",
)
def get_page_update_short_url(
    request: Request,
) -> HTMLResponse:
    return form_response.render(
        request=request,
    )
