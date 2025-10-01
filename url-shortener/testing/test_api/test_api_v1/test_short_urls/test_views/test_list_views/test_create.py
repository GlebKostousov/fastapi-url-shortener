import random
import string

import httpx
from fastapi import status
from fastapi.testclient import TestClient
from pydantic import AnyHttpUrl
from starlette.datastructures import URLPath

from main import app
from schemas.short_url import ShortUrlCreate

TEST_DESCRIPTION = "dsada"

TEST_WEBSITE = "https://google.com"


def generate_slug_for_test() -> str:
    return "".join(random.choices(string.ascii_letters, k=8))


def _get_url_for_test_create() -> URLPath:
    return app.url_path_for("create_short_url")


def _get_data_for_create_response() -> dict[str, str]:
    return ShortUrlCreate(
        target_url=AnyHttpUrl(TEST_WEBSITE),
        description=TEST_DESCRIPTION,
        slug=generate_slug_for_test(),
    ).model_dump(mode="json")


def _get_response_from_create_views(
    auth_client: TestClient,
    url: URLPath,
    data: dict[str, str],
) -> httpx.Response:
    response: httpx.Response = auth_client.post(url=url, json=data)
    return response


def test_create_short_url(auth_client: TestClient) -> None:
    url = _get_url_for_test_create()
    data = _get_data_for_create_response()
    response = _get_response_from_create_views(
        auth_client=auth_client,
        url=url,
        data=data,
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = {
        "target_url": response_data["target_url"],
        "description": response_data["description"],
        "slug": response_data["slug"],
    }
    assert received_values == data, response_data


def test_create_short_url_already_exists(auth_client: TestClient) -> None:
    url = _get_url_for_test_create()
    data = _get_data_for_create_response()
    _get_response_from_create_views(
        auth_client=auth_client,
        url=url,
        data=data,
    )
    response = _get_response_from_create_views(
        auth_client=auth_client,
        url=url,
        data=data,
    )
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
