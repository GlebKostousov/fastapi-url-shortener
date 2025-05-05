"""
Create
Read
Update
Delete
"""

from typing import Dict, List

from pydantic import BaseModel, ValidationError

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)
from core.config import SHORT_URLS_STORAGE_FILE_PATH


class ShortUrlStorage(BaseModel):
    slug_to_short_url: Dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        SHORT_URLS_STORAGE_FILE_PATH.write_text(self.model_dump_json(indent=2))

    @classmethod
    def from_state(cls) -> "ShortUrlStorage":
        if not SHORT_URLS_STORAGE_FILE_PATH.exists():
            return ShortUrlStorage()
        return cls.model_validate_json(SHORT_URLS_STORAGE_FILE_PATH.read_text())

    def get(self) -> List[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url: ShortUrl = ShortUrl(**short_url_in.model_dump())
        self.slug_to_short_url[short_url.slug] = short_url
        self.save_state()
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)
        self.save_state()

    def delete(self, short_url_in: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url_in.slug)

    # noinspection PyMethodMayBeStatic
    def update(self, short_url: ShortUrl, short_url_in: ShortUrlUpdate) -> ShortUrl:
        for field, value in short_url_in:
            setattr(short_url, field, value)
        self.save_state()
        return short_url

    def partial_update(
        self, short_url: ShortUrl, short_url_in: ShortUrlPartialUpdate
    ) -> ShortUrl:
        for field, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field, value)
        self.save_state()
        return short_url


try:
    storage = ShortUrlStorage.from_state()
except ValidationError:
    storage = ShortUrlStorage()
