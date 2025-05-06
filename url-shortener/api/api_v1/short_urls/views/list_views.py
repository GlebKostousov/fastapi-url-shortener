from typing import List

from fastapi import (
    APIRouter,
    status,
    BackgroundTasks,
    Depends,
)
from api.api_v1.short_urls.crud import storage
from api.api_v1.short_urls.dependencies import save_storage_state
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlRead,
)
import logging

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/short-urls",
    tags=["short_urls"],
    dependencies=[Depends(save_storage_state)],
)


@router.post(
    path="/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrl:
    return storage.create(short_url_create)


@router.get(
    path="/",
    response_model=List[ShortUrl],
)
def read_short_urls_list() -> List[ShortUrl]:
    return storage.get()
