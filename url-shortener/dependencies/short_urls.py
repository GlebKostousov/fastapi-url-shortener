from typing import Annotated, cast

from fastapi import Depends, Request

from storage.short_url import ShortUrlStorage

__all__ = ("GetShortUrlsStorage",)


def get_short_urls_storage(
    request: Request,
) -> ShortUrlStorage:
    return cast(ShortUrlStorage, request.app.state.short_urls_storage)


GetShortUrlsStorage = Annotated[
    ShortUrlStorage,
    Depends(get_short_urls_storage),
]
