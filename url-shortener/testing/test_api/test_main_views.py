from fastapi import status
from fastapi.testclient import TestClient
from pytest import mark


def test_root_view(client: TestClient) -> None:
    # TODO: fake date
    name = "John"
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    expected_message = f"Hello {name}!"
    assert response_data["message"] == expected_message, response_data


@mark.parametrize(
    "name",
    [
        "john",
        "",
        "!@#$",
        "Jpgm Smith",
    ],
)
def test_root_view_custom_name(name: str, client: TestClient) -> None:
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    expected_message = f"Hello {name}!"
    assert response_data["message"] == expected_message, response_data
