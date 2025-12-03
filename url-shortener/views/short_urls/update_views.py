from logging import getLogger

from fastapi import APIRouter
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from dependencies.short_urls import GetShortUrlsStorage, ShortUrlBySlug
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
    short_url: ShortUrlBySlug,
) -> HTMLResponse:
    form = ShortUrlUpdate(**short_url.model_dump())
    return form_response.render(
        request=request,
        form_data=form,
        short_url=short_url,
    )


@router.post(
    path="/",
    name="short-urls:update",
    response_model=None,
)
async def update_short_url(
    storage: GetShortUrlsStorage,
    request: Request,
    short_url: ShortUrlBySlug,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:

        try:
            short_url_update = ShortUrlUpdate.model_validate(form)
        except ValidationError as validation_error:
            return form_response.render(
                request=request,
                form_data=form,
                pydantic_error=validation_error,
                form_validated=True,
                short_url=short_url,
            )

        storage.update(
            short_url=short_url,
            short_url_in=short_url_update,
        )
        return RedirectResponse(
            url=request.url_for("short-urls:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
