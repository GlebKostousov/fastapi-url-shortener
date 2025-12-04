from logging import getLogger

from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from dependencies.short_urls import GetShortUrlsStorage
from misc.flash_message import create_flash_message
from schemas.short_url import ShortUrlCreate
from services.short_urls import FormResponseHelper
from storage.short_url.exceptions import ShortUrlAlreadyExistsError

logger = getLogger(__name__)
router = APIRouter(
    prefix="/create",
)

form_response = FormResponseHelper(
    model=ShortUrlCreate,
    template_name="short_urls/create.html",
)


@router.get(
    path="/",
    name="short-urls:create-view",
)
def get_page_crate_short_url(
    request: Request,
) -> HTMLResponse:
    return form_response.render(
        request=request,
    )


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
            return form_response.render(
                request=request,
                form_data=form,
                pydantic_error=validation_error,
                form_validated=True,
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
        create_flash_message(
            request=request,
            message=f"Short URL {short_url_create.slug!r} was created ",
            category="success",
        )
        return RedirectResponse(
            url=request.url_for("short-urls:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return form_response.render(
        request=request,
        form_data=form,
        errors=errors,
        form_validated=True,
    )
