from typing import TYPE_CHECKING

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from dependencies.short_urls import GetShortUrlsStorage
from templating import templates

if TYPE_CHECKING:
    from schemas.short_url import ShortUrl

router = APIRouter()


@router.get(
    "/",
    name="short-urls:list",
    response_class=HTMLResponse,
)
def list_view(
    request: Request,
    storage: GetShortUrlsStorage,
) -> HTMLResponse:
    context: dict[str, list[ShortUrl]] = {}
    short_urls = storage.get()
    context.update(short_urls=short_urls)
    return templates.TemplateResponse(
        request=request,
        name="short_urls/list.html",
        context=context,
    )
