import os
import pathlib
import sys
from pathlib import WindowsPath

import pytest


@pytest.mark.skip(reason="user schema not implemented yet")
def test_user_schema() -> None:
    user_data = {"username": "foobar"}
    assert user_data["username"] == "spam"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="skip test due to some reason",
)
def test_platform() -> None:
    assert sys.platform != "win32"


@pytest.mark.skipif(
    os.name != "nt",
    reason="run only on windows",
)
def test_only_for_windows() -> None:
    path = pathlib.Path(__file__)
    assert isinstance(path, WindowsPath)
