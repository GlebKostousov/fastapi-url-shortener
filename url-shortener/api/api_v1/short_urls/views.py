from typing import List, Annotated

from fastapi import HTTPException, Depends, APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from schemas.short_url import ShortUrl

router = APIRouter(prefix="/short-urls")

SHORT_URLS = [
    ShortUrl(
        target_url="https://example.com",
        slug="example",
    ),
    ShortUrl(
        target_url="https://google.com",
        slug="search",
    ),
]


@router.get(
    path="/",
    response_model=List[ShortUrl],
)
def read_short_urls_list():
    return SHORT_URLS


def prefetch_short_urls(slug: str) -> ShortUrl:
    url: ShortUrl | None = next((url for url in SHORT_URLS if url.slug == slug), None)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


@router.get(path="/r/{slug}")
@router.get(path="/r/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_urls),
    ],
):
    return RedirectResponse(
        url=url.target_url,
    )


@router.get(
    path="{slug}",
    response_model=ShortUrl,
)
def read_short_url(
    url: Annotated[ShortUrl, Depends(prefetch_short_urls)],
):
    return url
