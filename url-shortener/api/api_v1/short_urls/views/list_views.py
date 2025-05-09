from typing import List

from fastapi import (
    APIRouter,
    status,
    Depends,
)
from api.api_v1.short_urls.crud import storage
from api.api_v1.short_urls.dependencies import (
    save_storage_state,
    api_token_required,
    basic_user_auth_required,
)
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
    dependencies=[
        Depends(save_storage_state),
        # Depends(api_token_required), пока задокументировали, чтобы написать проверку по логин \ пароль
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid API token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token. Only for unsafe methods.",
                    },
                },
            },
        },
    },
)


@router.post(
    path="/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(basic_user_auth_required),
    ],
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
