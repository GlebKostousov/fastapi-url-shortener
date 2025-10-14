import random
import string
from collections.abc import Generator
from os import getenv

import pytest
from pydantic import AnyHttpUrl

from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl, ShortUrlCreate

DESCRIPTION_FOR_TEST = "A short url"

if getenv("TESTING") != "1":
    pytest.exit(
        "Environment is not ready for testing",
    )


def build_short_url_create(
    slug: str,
    description: str = DESCRIPTION_FOR_TEST,
) -> ShortUrlCreate:

    return ShortUrlCreate(
        slug=slug,
        description=description,
        target_url=AnyHttpUrl("https://example.com"),
    )


def _generate_slug() -> str:
    return "".join(
        random.choices(
            string.ascii_letters,
            k=8,
        ),
    )


def build_short_url_create_random_slug(
    description: str = DESCRIPTION_FOR_TEST,
) -> ShortUrlCreate:
    return ShortUrlCreate(
        slug=_generate_slug(),
        description=description,
        target_url=AnyHttpUrl("https://example.com"),
    )


def create_short_url(
    slug: str,
    description: str = DESCRIPTION_FOR_TEST,
) -> ShortUrl:
    short_url_in = build_short_url_create(slug=slug, description=description)
    return storage.create(short_url_in)


def create_short_url_random_slug(description: str = DESCRIPTION_FOR_TEST) -> ShortUrl:
    short_url_in = build_short_url_create_random_slug(description=description)
    return storage.create(short_url_in)


@pytest.fixture()
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url_random_slug()
    yield short_url
    storage.delete(short_url)
