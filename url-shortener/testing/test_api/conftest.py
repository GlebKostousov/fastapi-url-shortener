import random
import string
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from pydantic import AnyHttpUrl

from api.api_v1.auth.services import redis_tokens
from api.api_v1.short_urls.crud import storage
from main import app
from schemas.short_url import ShortUrl, ShortUrlCreate


def create_short_url() -> ShortUrl:
    short_url_in = ShortUrlCreate(
        target_url=AnyHttpUrl("https://google.com"),
        description="dsada",
        slug="".join(random.choices(string.ascii_letters, k=8)),
    )
    return storage.create(short_url_in)


@pytest.fixture()
def client() -> Generator[TestClient]:
    with TestClient(app=app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def auth_token() -> Generator[str]:
    token = redis_tokens.generate_and_save_token()
    yield token
    redis_tokens.delete_token(token)


@pytest.fixture(scope="module")
def auth_client(auth_token: str) -> Generator[TestClient]:
    headers = {"Authorization": f"Bearer {auth_token}"}
    with TestClient(app=app, headers=headers) as client:
        yield client


@pytest.fixture()
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url()
    yield short_url
    storage.delete(short_url)
