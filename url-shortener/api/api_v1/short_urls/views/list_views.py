import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from api.api_v1.short_urls.crud import ShortUrlAlreadyExistsError, storage
from api.api_v1.short_urls.dependencies import (
    api_token_or_basic_auth_required,
)
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlRead,
)

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/short-urls",
    tags=["short_urls"],
    dependencies=[
        Depends(api_token_or_basic_auth_required),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid API token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid auth. Only for unsafe methods.",
                    },
                },
            },
        },
    },
)


@router.get(
    path="/",
    response_model=list[ShortUrlRead],
)
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get()


@router.post(
    path="/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "You tried create already exist url",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Short URL with slug='name' already exists.",
                    },
                },
            },
        },
    },
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrl:
    try:
        return storage.create_of_raise_if_exists(short_url_create)
    except ShortUrlAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Short URL with slug={short_url_create.slug!r} already exists.",
        ) from None
