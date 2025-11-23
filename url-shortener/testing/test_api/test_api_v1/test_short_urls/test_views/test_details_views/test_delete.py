import pytest
from _pytest.fixtures import SubRequest
from pydantic import AnyHttpUrl
from starlette import status
from starlette.testclient import TestClient

from main import app
from schemas.short_url import ShortUrl, ShortUrlCreate
from storage.short_url.crud import storage


def create_short_url(slug: str) -> ShortUrl:
    short_url_in = ShortUrlCreate(
        slug=slug,
        description="A short url",
        target_url=AnyHttpUrl("https://example.com"),
    )
    return storage.create(short_url_in)


@pytest.fixture(
    params=[
        "some-slug",
        "qwerty-abc-foo-bar",
        "slug",
        pytest.param("abc", id="minimal-slug"),
        pytest.param("123131233", id="maximal-slug"),
    ],
)
def short_url(request: SubRequest) -> ShortUrl:
    # print(type(request))
    return create_short_url(request.param)


@pytest.mark.apitest
def test_delete(
    auth_client: TestClient,
    short_url: ShortUrl,
) -> None:
    url = app.url_path_for("delete_short_url", slug=short_url.slug)
    assert storage.exists(short_url.slug)
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(short_url.slug), response.text
