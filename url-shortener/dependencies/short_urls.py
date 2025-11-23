from typing import Annotated

from fastapi import Depends

from core.config import settings
from storage.short_url import ShortUrlStorage

__all__ = ("GetShortUrlsStorage",)


def get_short_urls_storage() -> ShortUrlStorage:
    return ShortUrlStorage(
        hash_name=settings.redis.namespace.hash_names.short_url,
    )


GetShortUrlsStorage = Annotated[
    ShortUrlStorage,
    Depends(get_short_urls_storage),
]
