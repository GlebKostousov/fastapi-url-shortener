"""
Create
Read
Update
Delete
"""

from typing import Dict, List

from pydantic import BaseModel, AnyHttpUrl

from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlUpdate


class ShortUrlStorage(BaseModel):
    slug_to_short_url: Dict[str, ShortUrl] = {}

    def get(self) -> List[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url: ShortUrl = ShortUrl(**short_url_in.model_dump())
        self.slug_to_short_url[short_url.slug] = short_url
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


storage = ShortUrlStorage()
storage.create(
    short_url_in=ShortUrlCreate(
        target_url=AnyHttpUrl("https://example.com"),
        slug="example",
    )
)
storage.create(
    short_url_in=ShortUrlCreate(
        target_url=AnyHttpUrl("https://google.com"),
        slug="search",
    )
)
