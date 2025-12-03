from logging import getLogger

from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

logger = getLogger(__name__)
router = APIRouter(
    prefix="/{slug}/delete",
)


@router.post(
    path="/",
    name="short-urls:delete",
    response_model=None,
)
def delete_short_url(
    request: Request,
    # storage: GetShortUrlsStorage,
    # short_url: ShortUrlBySlug,
) -> RedirectResponse:
    return RedirectResponse(
        url=request.url_for("short-urls:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
