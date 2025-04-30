from typing import List

from fastapi import (
    APIRouter,
    status,
)
from api.api_v1.short_urls.crud import storage
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
)

router = APIRouter(
    prefix="/short-urls",
    tags=["short_urls"],
)


@router.post(
    path="/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrl:
    return storage.create(ShortUrl(**short_url_create.model_dump()))


@router.get(
    path="/",
    response_model=List[ShortUrl],
)
def read_short_urls_list() -> List[ShortUrl]:
    return storage.get()
