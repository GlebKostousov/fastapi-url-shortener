from typing import Annotated

from fastapi import (
    Depends,
    BackgroundTasks,
)
from starlette import status

from api.api_v1.short_urls.crud import storage
from api.api_v1.short_urls.dependencies import prefetch_short_urls
from schemas.short_url import (
    ShortUrl,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
    ShortUrlRead,
)

from fastapi import APIRouter

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

ShortUrlBySlug = Annotated[ShortUrl, Depends(prefetch_short_urls)]


@router.get(path="/", response_model=ShortUrlRead)
def read_short_url(url: ShortUrlBySlug):
    return url


@router.delete(path="/", status_code=status.HTTP_204_NO_CONTENT)
def delete_short_url(
    url: ShortUrlBySlug,
    background_tasks: BackgroundTasks,
) -> None:
    storage.delete(short_url_in=url)
    background_tasks.add_task(storage.save_state)


@router.put(path="/", response_model=ShortUrlRead)
def update_short_url_details(
    url: ShortUrlBySlug,
    url_in: ShortUrlUpdate,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(storage.save_state)
    return storage.update(short_url=url, short_url_in=url_in)


@router.patch(path="/", response_model=ShortUrlRead)
def partial_update_short_url(
    url: ShortUrlBySlug,
    url_in: ShortUrlPartialUpdate,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(storage.save_state)
    return storage.partial_update(short_url=url, short_url_in=url_in)
