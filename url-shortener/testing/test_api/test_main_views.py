import pytest
from fastapi import status
from fastapi.testclient import TestClient

pytestmark = pytest.mark.templatetest


def test_home_page(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text

    template = getattr(response, "template", None)
    context = getattr(response, "context", None)

    assert template is not None, "Response should have template"
    assert context is not None, "Response should have context"

    assert template.name == "home.html"
    assert "features" in context
    assert isinstance(context["features"], list)
