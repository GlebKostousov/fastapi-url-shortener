from fastapi import (
    APIRouter,
    status,
)

from dependencies.short_urls import ShortUrlBySlug
from schemas.short_url import (
    ShortUrl,
    ShortUrlPartialUpdate,
    ShortUrlRead,
    ShortUrlUpdate,
)
from storage.short_url.crud import storage

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "film not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "FILM 'slug' not found",
                    },
                },
            },
        },
    },
)


@router.get(path="/", response_model=ShortUrlRead)
def read_short_url(url: ShortUrlBySlug) -> ShortUrl:
    return url


@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_short_url",
)
def delete_short_url(
    url: ShortUrlBySlug,
) -> None:
    storage.delete(short_url_in=url)


@router.post(path="/transfer/")
def transfer_short_url() -> None:
    raise NotImplementedError


@router.put(path="/", response_model=ShortUrlRead)
def update_short_url_details(
    url: ShortUrlBySlug,
    url_in: ShortUrlUpdate,
) -> ShortUrl:
    return storage.update(short_url=url, short_url_in=url_in)


@router.patch(path="/", response_model=ShortUrlRead)
def partial_update_short_url(
    url: ShortUrlBySlug,
    url_in: ShortUrlPartialUpdate,
) -> ShortUrl:
    return storage.partial_update(short_url=url, short_url_in=url_in)
