from fastapi import HTTPException, BackgroundTasks
from starlette import status

from schemas.short_url import ShortUrl
from api.api_v1.short_urls.crud import storage
import logging

log = logging.getLogger(__name__)


def prefetch_short_urls(slug: str) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


def save_storage_state(background_tasks: BackgroundTasks):
    yield
    log.debug("Add background tasks to save storage")
    background_tasks.add_task(storage.save_state)
