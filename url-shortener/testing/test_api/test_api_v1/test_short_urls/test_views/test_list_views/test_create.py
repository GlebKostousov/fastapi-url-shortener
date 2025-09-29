import random
import string

from fastapi import status
from fastapi.testclient import TestClient
from pydantic import AnyHttpUrl

from main import app
from schemas.short_url import ShortUrlCreate


def test_create_short_url(auth_client: TestClient) -> None:
    url = app.url_path_for("create_short_url")
    data: dict[str, str] = ShortUrlCreate(
        target_url=AnyHttpUrl("https://google.com"),
        description="dsada",
        slug="".join(random.choices(string.ascii_letters, k=8)),
    ).model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = {
        "target_url": response_data["target_url"],
        "description": response_data["description"],
        "slug": response_data["slug"],
    }
    assert received_values == data, response_data
