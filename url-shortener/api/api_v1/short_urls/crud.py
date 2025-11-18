"""
Create
Read
Update
Delete
"""

__all__ = ("ShortUrlAlreadyExistsError", "storage")

import logging

from pydantic import BaseModel
from redis import Redis

from core.config import settings
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)

log = logging.getLogger(__name__)

redis_short_urls = Redis(
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.db.short_urls,
    decode_responses=True,
)


class ShortUrlBaseError(Exception):
    """Base exception for short url CRUD actions"""


class ShortUrlAlreadyExistsError(ShortUrlBaseError):
    """Raised when short url already exists"""

    def __init__(self, slug: str) -> None:
        self.slug = slug


class ShortUrlStorage(BaseModel):
    hash_name: str

    def save_state(self, short_url: ShortUrl) -> None:
        """
        Saves short url data to db

        Args:
            short_url (ShortUrl): data to be saved

        Returns:

        """
        redis_short_urls.hset(
            name=self.hash_name,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )
        log.info("Save short url to storage file.")

    def get(self) -> list[ShortUrl]:
        """
        Get all short urls from db

        Returns:
            list[ShortUrl]: list of all short urls

        """
        return [
            ShortUrl.model_validate_json(value)
            for value in redis_short_urls.hvals(
                name=self.hash_name,
            )
        ]

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        """
        Get short url by slug from db

        Args:
            slug (str): short url slug to find element in db

        Returns:
            ShortUrl | None. if short url exists with slug, else None

        """
        if short_url_json := redis_short_urls.hget(
            name=self.hash_name,
            key=slug,
        ):
            return ShortUrl.model_validate_json(short_url_json)

        return None

    def exists(self, slug: str) -> bool:
        """
        Check existence of short url in db

        Args:
            slug (str): short url slug to check

        Returns:
            bool. True if exists, else False

        """
        return bool(
            redis_short_urls.hexists(
                name=self.hash_name,
                key=slug,
            ),
        )

    def delete_by_slug(self, slug: str) -> None:
        """
        Delete short url by slug

        Args:
            slug (str): slug of short url

        Returns:

        """
        redis_short_urls.hdel(self.hash_name, slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        """
        Create short url

        Args:
            short_url_in (ShortUrlCreate): data to create short url

        Returns:
            ShortUrl - created data from db

        """
        short_url: ShortUrl = ShortUrl(**short_url_in.model_dump())
        self.save_state(short_url)
        log.info("Created short url %s", short_url)
        return short_url

    def create_of_raise_if_exists(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        """
        Check existence of short url. If exists, raise ShortUrlAlreadyExistsError,
        else create short url

        Args:
            short_url_in (ShortUrlCreate): data from front to create short url

        Returns:

        """
        if not self.exists(short_url_in.slug):
            return self.create(short_url_in)

        raise ShortUrlAlreadyExistsError(short_url_in.slug)

    def delete(self, short_url_in: ShortUrl) -> None:
        """
        Delete short url

        Args:
            short_url_in (ShortUrl): Short url from db to delete

        Returns:

        """
        self.delete_by_slug(slug=short_url_in.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        """
        Update short url

        Args:
            short_url (ShortUrl): Short url from db to update
            short_url_in (ShortUrlUpdate): data from front to update short url

        Returns:
            ShortUrl - updated data from db

        """
        for field, value in short_url_in:
            setattr(short_url, field, value)
        self.save_state(short_url)
        return short_url

    def partial_update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        """
        Partially update short url

        Args:
            short_url (ShortUrl): Short url from db to update
            short_url_in (ShortUrlPartialUpdate): data from front to update short url

        Returns:
            ShortUrl - updated data from db

        """
        for field, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field, value)

        self.save_state(short_url)
        return short_url


storage = ShortUrlStorage(hash_name=settings.redis.namespace.hash_names.short_url)
