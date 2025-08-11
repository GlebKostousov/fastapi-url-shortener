from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture()
def client() -> Generator[TestClient]:
    with TestClient(app=app) as test_client:
        yield test_client
