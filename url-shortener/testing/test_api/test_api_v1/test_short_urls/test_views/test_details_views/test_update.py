from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.short_urls.crud import storage
from core.const import MAX_LENGTH_DESCRIPTION
from main import app
from schemas.short_url import ShortUrl, ShortUrlUpdate
from testing.conftest import create_short_url_random_slug


class TestUpdate:

    @pytest.fixture()
    def short_url(self, request: SubRequest) -> Generator[ShortUrl]:
        description, target_url = request.param
        short_url = create_short_url_random_slug(
            description=description,
            target_url=target_url,
        )

        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        argnames=["short_url", "new_description", "new_target_url"],
        argvalues=[
            pytest.param(
                (
                    "some_description",
                    "https://example.com",
                ),
                "some_description",
                "https://site.ru",
                id="some-description-and-new-target-url",
            ),
            pytest.param(
                (
                    "some_description",
                    "https://example.com",
                ),
                "some_new_description",
                "https://new_target_url.com",
                id="new-target-url-and-description",
            ),
            pytest.param(
                (
                    "some_description",
                    "https://example.com",
                ),
                "",
                "https://new_target_url.com",
                id="empty-description-and-new-target-url",
            ),
            pytest.param(
                (
                    "some_description",
                    "https://example.com",
                ),
                "a" * MAX_LENGTH_DESCRIPTION,
                "https://example.com",
                id="max-description-length-and-same-target-url",
            ),
        ],
        indirect=["short_url"],
    )
    def test_update_short_url(
        self,
        short_url: ShortUrl,
        new_description: str,
        new_target_url: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "update_short_url_details",
            slug=short_url.slug,
        )
        update = ShortUrlUpdate(
            description=new_description,
            target_url=new_target_url,
        )
        response = auth_client.put(url, json=update.model_dump(mode="json"))
        assert response.status_code == status.HTTP_200_OK, response.text
        short_url_db = storage.get_by_slug(short_url.slug)
        assert short_url_db
        new_data = ShortUrlUpdate(**short_url_db.model_dump())
        assert new_data == update
