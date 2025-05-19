"""
Create
Read
Update
Delete
"""

import logging
from typing import Dict, List

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)
from core.config import SHORT_URLS_STORAGE_FILE_PATH

log = logging.getLogger(__name__)

redis_short_urls = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_SHORT_URLS,
    decode_responses=True,
)


class ShortUrlStorage(BaseModel):
    slug_to_short_url: Dict[str, ShortUrl] = {}

    def init_storage_from_state(self) -> None:
        try:
            data = ShortUrlStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error.")
            return

        self.slug_to_short_url.update(
            data.slug_to_short_url,
        )
        log.warning("Recovered data from storage file.")

    def save_state(self) -> None:
        SHORT_URLS_STORAGE_FILE_PATH.write_text(self.model_dump_json(indent=2))
        log.info("Save short url to storage file.")

    @classmethod
    def from_state(cls) -> "ShortUrlStorage":
        if not SHORT_URLS_STORAGE_FILE_PATH.exists():
            log.info("No short url storage file.")
            return ShortUrlStorage()
        return cls.model_validate_json(SHORT_URLS_STORAGE_FILE_PATH.read_text())

    def get(self) -> List[ShortUrl]:
        if json_list := redis_short_urls.hvals(name=config.REDIS_SHORT_URLS_HASH_NAME):
            return [ShortUrl.model_validate_json(elem) for elem in json_list if elem]
        return []

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        if short_url_json := redis_short_urls.hget(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=slug,
        ):
            return ShortUrl.model_validate_json(short_url_json)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url: ShortUrl = ShortUrl(**short_url_in.model_dump())
        redis_short_urls.hset(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )
        log.info(f"Created short url %s", short_url)
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)

    def delete(self, short_url_in: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url_in.slug)

    # noinspection PyMethodMayBeStatic
    def update(self, short_url: ShortUrl, short_url_in: ShortUrlUpdate) -> ShortUrl:
        for field, value in short_url_in:
            setattr(short_url, field, value)
        return short_url

    def partial_update(
        self, short_url: ShortUrl, short_url_in: ShortUrlPartialUpdate
    ) -> ShortUrl:
        for field, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field, value)
        return short_url


storage = ShortUrlStorage()
