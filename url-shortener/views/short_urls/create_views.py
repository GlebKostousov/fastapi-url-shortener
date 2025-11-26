from logging import getLogger
from typing import Annotated, Any

from fastapi import APIRouter, Form, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from dependencies.short_urls import GetShortUrlsStorage
from schemas.short_url import ShortUrlCreate
from storage.short_url.exceptions import ShortUrlAlreadyExistsError
from templating import templates

logger = getLogger(__name__)
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
    response_model=None,
)
def create_short_url(
    short_url_create: Annotated[
        ShortUrlCreate,
        Form(),
    ],
    storage: GetShortUrlsStorage,
    request: Request,
) -> RedirectResponse | HTMLResponse:
    try:
        storage.create_of_raise_if_exists(
            short_url_in=short_url_create,
        )

    except ShortUrlAlreadyExistsError:
        errors = {
            "slug": f"Short url with slug {short_url_create.slug!r} already exists.",
        }
    else:
        return RedirectResponse(
            url=request.url_for("short-urls:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    context: dict[str, Any] = {}
    context.update(
        model_schema=ShortUrlCreate.model_json_schema(),
        errors=errors,
        form_validated=True,
        form_data=short_url_create,
    )
    return templates.TemplateResponse(
        name="short_urls/create.html",
        request=request,
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
