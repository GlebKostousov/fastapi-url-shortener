import random
import string
from typing import ClassVar, Final
from unittest import TestCase

from pydantic import AnyHttpUrl

from api.api_v1.short_urls.crud import storage
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)


def create_short_url() -> ShortUrl:
    short_url_in = ShortUrlCreate(
        target_url=AnyHttpUrl("https://google.com"),
        description="dsada",
        slug="".join(random.choices(string.ascii_letters, k=8)),
    )
    return storage.create(short_url_in)


class ShortUrlStorageUpdateTestCase(TestCase):

    def setUp(self) -> None:
        self.short_url = create_short_url()

    def tearDown(self) -> None:
        storage.delete(self.short_url)

    def test_update(self) -> None:
        short_url_update = ShortUrlUpdate(**self.short_url.model_dump())
        source_description = self.short_url.description

        short_url_update.description *= 2
        updated_short_url = storage.update(
            self.short_url,
            short_url_update,
        )

        self.assertNotEqual(
            source_description,
            updated_short_url.description,
        )

        self.assertEqual(
            short_url_update,
            ShortUrlUpdate(
                **updated_short_url.model_dump(),
            ),
        )

    def test_partial_update(self) -> None:
        short_url_partial_update = ShortUrlPartialUpdate(
            description=self.short_url.description * 2,
        )
        source_description = self.short_url.description

        partial_updated_short_url = storage.partial_update(
            short_url=self.short_url,
            short_url_in=short_url_partial_update,
        )

        self.assertNotEqual(
            source_description,
            partial_updated_short_url.description,
        )

        self.assertEqual(
            short_url_partial_update.description,
            partial_updated_short_url.description,
        )


class ShortUrlStorageGetTestCase(TestCase):

    SHORT_URLS_COUNTS: Final[int] = 3
    short_urls: ClassVar[list[ShortUrl]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.short_urls = [create_short_url() for _ in range(cls.SHORT_URLS_COUNTS)]

    @classmethod
    def tearDownClass(cls) -> None:
        for short_url in cls.short_urls:
            storage.delete(short_url)

    def test_get_list(self) -> None:
        short_urls = storage.get()
        slug_in_db = {si.slug for si in short_urls}

        expected_slug = {si.slug for si in self.short_urls}

        expected_dif: set[ShortUrl] = set()
        real_dif = expected_slug - slug_in_db
        self.assertEqual(
            expected_dif,
            real_dif,
        )

    def test_get_by_slug(self) -> None:
        for short_url in self.short_urls:
            with self.subTest(
                slug=short_url.slug,
                msg=f"Validate can get slug {short_url.slug!r}",
            ):
                db_short_url = storage.get_by_slug(short_url.slug)
                self.assertEqual(
                    short_url,
                    db_short_url,
                )
