from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from api.api_v1.short_urls.crud import storage
from core.const import MAX_LENGTH_DESCRIPTION
from main import app
from schemas.short_url import ShortUrl
from testing.conftest import create_short_url


class TestUpdatePartial:

    @pytest.fixture()
    def short_url(self, request: SubRequest) -> Generator[ShortUrl]:
        slug, description = request.param
        short_url = create_short_url(slug=slug, description=description)
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        "short_url, new_description",
        # short_url - это tuple для создания объекта фикстуры,
        # а new_description - это следующий value, который идет сразу в функцию
        [
            pytest.param(
                ("foo", "some description"),
                "",
                id="some-description-to-no-description",
            ),
            pytest.param(
                ("bar", ""),
                "some description",
                id="non-description-to-som-description",
            ),
            pytest.param(
                ("max", "a" * MAX_LENGTH_DESCRIPTION),
                "",
                id="max-description-to-min-description",
            ),
            pytest.param(
                ("min", ""),
                "a" * MAX_LENGTH_DESCRIPTION,
                id="min-description-to-max-description",
            ),
        ],
        # indirect=True,  # значения не передаются в функцию,
        # а попадают в фикстуру с нужным полем
        indirect=[
            "short_url",
        ],  # теперь косвенно отправляем только short_url,
        # а new_description сразу в функцию
    )
    def test_update_short_url_partial(
        self,
        short_url: ShortUrl,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "partial_update_short_url",
            slug=short_url.slug,
        )
        response = auth_client.patch(url, json={"description": new_description})
        assert response.status_code == status.HTTP_200_OK, response.text
        short_url_db = storage.get_by_slug(short_url.slug)
        assert short_url_db
        assert short_url_db.description == new_description
