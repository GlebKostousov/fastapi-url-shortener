__all__ = ("prefetch_short_urls",)

from fastapi import (
    HTTPException,
    status,
)

from dependencies.short_urls import GetShortUrlsStorage
from schemas.short_url import ShortUrl


def prefetch_short_urls(slug: str, storage: GetShortUrlsStorage) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )
