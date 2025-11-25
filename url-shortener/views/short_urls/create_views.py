from typing import Annotated, Any

from fastapi import APIRouter, Form, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from dependencies.short_urls import GetShortUrlsStorage
from schemas.short_url import ShortUrlCreate
from templating import templates

router = APIRouter(
    prefix="/create",
)


@router.get(
    path="/",
    name="short-urls:create-view",
)
def get_page_crate_short_url(
    request: Request,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = ShortUrlCreate.model_json_schema()
    context.update(model_schema=model_schema)

    return templates.TemplateResponse(
        name="short_urls/create.html",
        request=request,
        context=context,
    )


@router.post(
    path="/",
    name="short-urls:create",
)
def create_short_url(
    short_url_create: Annotated[
        ShortUrlCreate,
        Form(),
    ],
    storage: GetShortUrlsStorage,
    request: Request,
) -> RedirectResponse:
    storage.create_of_raise_if_exists(
        short_url_in=short_url_create,
    )
    return RedirectResponse(
        url=request.url_for("short-urls:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
