from typing import Annotated, Any

from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

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
) -> dict[str, str]:
    return short_url_create.model_dump(mode="json")
