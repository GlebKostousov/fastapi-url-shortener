from logging import getLogger
from typing import Any

from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from starlette.datastructures import FormData

from dependencies.short_urls import GetShortUrlsStorage
from schemas.short_url import ShortUrlCreate
from storage.short_url.exceptions import ShortUrlAlreadyExistsError
from templating import templates

logger = getLogger(__name__)


def _create_view_validation_response(
    errors: dict[str, str],
    request: Request,
    form_data: FormData | ShortUrlCreate | None = None,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(
        model_schema=ShortUrlCreate.model_json_schema(),
        errors=errors,
        form_validated=True,
        form_data=form_data,
    )
    return templates.TemplateResponse(
        name="short_urls/create.html",
        request=request,
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


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


def _format_pydantic_errors(
    error: ValidationError,
) -> dict[str, str]:
    return {str(err["loc"][0]): err["msg"] for err in error.errors()}


@router.post(
    path="/",
    name="short-urls:create",
    response_model=None,
)
async def create_short_url(
    storage: GetShortUrlsStorage,
    request: Request,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            short_url_create = ShortUrlCreate.model_validate(form)
        except ValidationError as validation_error:
            errors = _format_pydantic_errors(validation_error)
            return _create_view_validation_response(
                errors=errors,
                request=request,
                form_data=form,
            )
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

    return _create_view_validation_response(
        errors=errors,
        request=request,
        form_data=short_url_create,
    )
