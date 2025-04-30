from typing import Annotated

from fastapi import Depends
from starlette import status

from api.api_v1.short_urls.crud import storage
from api.api_v1.short_urls.dependencies import prefetch_short_urls
from schemas.short_url import ShortUrl

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


@router.get(
    path="/",
    response_model=ShortUrl,
)
def read_short_url(
    url: Annotated[ShortUrl, Depends(prefetch_short_urls)],
):
    return url


@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_short_url(
    url: Annotated[ShortUrl, Depends(prefetch_short_urls)],
) -> None:
    storage.delete(short_url_in=url)
