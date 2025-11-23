from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from storage.short_url import ShortUrlStorage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # noinspection PyUnresolvedReferences
    app.state.short_urls_storage = ShortUrlStorage(
        hash_name=settings.redis.namespace.hash_names.short_url,
    )
    yield
