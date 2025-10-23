import random
import string
from collections.abc import Generator
from os import getenv

import pytest
from pydantic import AnyHttpUrl

from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl, ShortUrlCreate

DESCRIPTION_FOR_TEST = "A short url"


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        pytest.exit(
            "Environment is not ready for testing",
        )  # тут тесты не запустятся вообще
        # pytest.fail("Environment is not ready for testing")
        # Тогда все тесты запустятся и свалятся с ошибкой


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
    target_url: str = "https://example.com",
) -> ShortUrlCreate:
    return ShortUrlCreate(
        slug=_generate_slug(),
        description=description,
        target_url=AnyHttpUrl(target_url),
    )


def create_short_url(
    slug: str,
    description: str = DESCRIPTION_FOR_TEST,
) -> ShortUrl:
    short_url_in = build_short_url_create(slug=slug, description=description)
    return storage.create(short_url_in)


def create_short_url_random_slug(
    description: str = DESCRIPTION_FOR_TEST,
    target_url: str = "https://example.com",
) -> ShortUrl:
    short_url_in = build_short_url_create_random_slug(
        description=description,
        target_url=target_url,
    )
    return storage.create(short_url_in)


@pytest.fixture()
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url_random_slug()
    yield short_url
    storage.delete(short_url)
