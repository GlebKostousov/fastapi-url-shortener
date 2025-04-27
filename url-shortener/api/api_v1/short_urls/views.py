from typing import List, Annotated

from fastapi import Depends, APIRouter

from api.api_v1.short_urls.dependencies import prefetch_short_urls
from api.api_v1.short_urls.crud import SHORT_URLS
from schemas.short_url import ShortUrl

router = APIRouter(
    prefix="/short-urls",
    tags=["short_urls"],
)


@router.get(
    path="/",
    response_model=List[ShortUrl],
)
def read_short_urls_list():
    return SHORT_URLS


@router.get(
    path="{slug}",
    response_model=ShortUrl,
)
def read_short_url(
    url: Annotated[ShortUrl, Depends(prefetch_short_urls)],
):
    return url
