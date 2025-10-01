from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.short_url import ShortUrl, ShortUrlCreate


def test_create_short_url(
    auth_client: TestClient,
    short_url: ShortUrl,
) -> None:
    url = app.url_path_for("create_short_url")
    short_url_create = ShortUrlCreate(**short_url.model_dump())
    data = short_url_create.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = {
        "target_url": response_data["target_url"],
        "description": response_data["description"],
        "slug": response_data["slug"],
    }
    assert received_values == data, response_data


def test_create_short_url_already_exists(
    auth_client: TestClient,
    short_url: ShortUrl,
) -> None:
    url = app.url_path_for("create_short_url")
    short_url_create = ShortUrlCreate(**short_url.model_dump())
    data = short_url_create.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
