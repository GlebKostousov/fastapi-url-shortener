from unittest import TestCase

from pydantic import AnyHttpUrl

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlPartialUpdate,
    ShortUrlUpdate,
)


class ShortUrlCreateTestCase(TestCase):
    def test_short_url_can_be_created_from_create_schema(self) -> None:
        short_url_in = ShortUrlCreate(
            slug="some-slug",
            description="Some description",
            target_url=AnyHttpUrl("https://example.com"),
        )
        short_url = ShortUrl.model_validate(
            short_url_in.model_dump(),
        )
        self.assertEqual(short_url_in.slug, short_url.slug)
        self.assertEqual(short_url_in.description, short_url.description)
        self.assertEqual(short_url_in.target_url, short_url.target_url)

    def test_short_url_can_be_created_from_update_schema(self) -> None:

        short_url_in = ShortUrlUpdate(
            target_url=AnyHttpUrl("https://example.com"),
            description="Some description",
        )

        short_url = ShortUrl(
            slug="some-slug",
            description="Some description1111",
            target_url=AnyHttpUrl("https://qqq.com"),
        )

        slug: str = short_url.slug

        for field, value in short_url_in:
            setattr(short_url, field, value)

        self.assertEqual(slug, short_url.slug)
        self.assertEqual(short_url_in.description, short_url.description)
        self.assertEqual(short_url_in.target_url, short_url.target_url)

    def test_short_url_can_be_created_from_partial_update_schema(self) -> None:
        short_url_in_param: list[tuple[str | None, str | None]] = [
            (
                "https://qqq.com",
                None,
            ),
            (
                None,
                "Some description1111",
            ),
            (
                "https://qqq.com",
                "Some description1111",
            ),
            (
                None,
                None,
            ),
        ]

        short_url = ShortUrl(
            slug="some-slug",
            target_url=AnyHttpUrl("https://example.com"),
            description="Some description",
        )

        slug: str = short_url.slug
        for target_url, description in short_url_in_param:
            with self.subTest(
                target_url=target_url,
                description=description,
            ):

                short_url_in = ShortUrlPartialUpdate(
                    target_url=target_url,
                    description=description,
                )

                for field, value in short_url_in.model_dump(exclude_unset=True).items():
                    setattr(short_url, field, value)

                self.assertEqual(slug, short_url.slug)
                self.assertEqual(
                    (
                        short_url_in.description
                        if short_url_in.description is not None
                        else short_url.description
                    ),
                    short_url.description,
                )
                self.assertEqual(
                    (
                        short_url_in.target_url
                        if short_url_in.target_url is not None
                        else short_url.target_url
                    ),
                    short_url.target_url,
                )
