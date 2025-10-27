import pytest
from starlette import status
from starlette.testclient import TestClient

from main import app


@pytest.mark.xfail(
    # REDIS_HOST != "localhost", 'это условие,
    # когда тест `падает`, а не `ожидаемо падает`
    reason="Not implemented yest",
    raises=NotImplementedError,
    # это вызовет ошибку в случаях, когда тест должен упасть, но он XPASS - прошел.
    strict=True,
)
@pytest.mark.apitest
def test_transfer_short_url(
    auth_client: TestClient,
) -> None:
    url = app.url_path_for("transfer_short_url", slug="some_slug")
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_200_OK, response.text
