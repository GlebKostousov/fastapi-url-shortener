"""
Create
Read
Update
Delete
"""

import logging
from typing import List

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)

log = logging.getLogger(__name__)

redis_short_urls = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_SHORT_URLS,
    decode_responses=True,
)


class ShortUrlBaseError(Exception):
    """
    Base exception for short url CRUD actions
    """


class ShortUrlAlreadyExistsError(ShortUrlBaseError):
    """
    Raised when short url already exists
    """

    def __init__(self, slug: str):
        self.slug = slug
        super().__init__(f"Short URL with slug '{slug!r}' already exists")


class ShortUrlStorage(BaseModel):

    @classmethod
    def save_state(cls, short_url: ShortUrl) -> None:
        redis_short_urls.hset(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )
        log.info("Save short url to storage file.")

    @classmethod
    def get(cls) -> List[ShortUrl]:
        return [
            ShortUrl.model_validate_json(value)
            for value in redis_short_urls.hvals(name=config.REDIS_SHORT_URLS_HASH_NAME)
        ]

    @classmethod
    def get_by_slug(cls, slug: str) -> ShortUrl | None:
        if short_url_json := redis_short_urls.hget(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=slug,
        ):
            return ShortUrl.model_validate_json(short_url_json)

        return None

    @classmethod
    def exists(cls, slug: str) -> bool:
        return bool(
            redis_short_urls.hexists(
                name=config.REDIS_SHORT_URLS_HASH_NAME,
                key=slug,
            )
        )

    @classmethod
    def delete_by_slug(cls, slug: str) -> None:
        redis_short_urls.hdel(config.REDIS_SHORT_URLS_HASH_NAME, slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url: ShortUrl = ShortUrl(**short_url_in.model_dump())
        self.save_state(short_url)
        log.info(f"Created short url %s", short_url)
        return short_url

    def create_of_raise_if_exists(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        if not self.exists(short_url_in.slug):
            return self.create(short_url_in)

        raise ShortUrlAlreadyExistsError(short_url_in.slug)

    def delete(self, short_url_in: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url_in.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field, value in short_url_in:
            setattr(short_url, field, value)
        self.save_state(short_url)
        return short_url

    def partial_update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        for field, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field, value)

        self.save_state(short_url)
        return short_url


storage = ShortUrlStorage()
